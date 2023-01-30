;     Test build framework for HuTrack release packages
;
;    {Assemble with PCEAS: ver 3.23 or higher}
;
;   Turboxray '21
;



;..............................................................................................................
;..............................................................................................................
;..............................................................................................................
;..............................................................................................................

    list
    mlist

;..................................................
;                                                 .
;  Logical Memory Map:                            .
;                                                 .
;            $0000 = Hardware bank                .
;            $2000 = Sys Ram                      .
;            $4000 = Subcode                      .
;            $6000 = Data 0 / Cont. of Subcode    .
;            $8000 = Data 1                       .
;            $A000 = Data 2                       .
;            $C000 = Main                         .
;            $E000 = Fixed Libray                 .
;                                                 .
;..................................................


;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;
;//  Vars

    .include "../base_func/vars.inc"
    .include "../base_func/video/vdc/vars.inc"
    .include "HuTrack/HuTrack_vars.inc"
    .include "../base_func/IO/gamepad/vars.inc"
    .include "../lib/controls/vars.inc"
    .include "../lib/control_vars/vars.inc"
    .include "../base_func/IO/irq_controller/vars.inc"
    .include "../base_func/IO/mapper/mapper.inc"

;....................................
    .code

    .bank $00, "Fixed Lib/Start up"
    .org $e000
;....................................

;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;
;// Support files: equates and macros
    .include "../base_func/base.inc"
    .include "../base_func/video/video.inc"
    .include "../base_func/video/vdc/vdc.inc"
    .include "../base_func/video/vce/vce.inc"
    .include "HuTrack/hutrack.inc"
    .include "../base_func/IO/gamepad/gamepad.inc"
    .include "../lib/controls/controls.inc"
    .include "../base_func/timer/timer.inc"
    .include "../base_func/IO/irq_controller/irq.inc"


;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;
;// Startup and fix lib @$E000

startup:
        ;................................
        ;Main initialization routine.
        InitialStartup
        CallFarWide init_audio
        CallFarWide init_video

        stz $2000
        stz $2001
        stz $2002
        tii $2000,$2001,$2000

        ;................................
        ;Set video parameters
        VCE.reg MID_RES|H_FILTER_ON
        VDC.reg HSR  , #$0404
        VDC.reg HDR  , #$0629
        VDC.reg VSR  , #$0F02
        VDC.reg VDR  , #$00ef
        VDC.reg VDE  , #$0003
        VDC.reg DCR  , #AUTO_SATB_ON
        VDC.reg CR   , #$0000
        VDC.reg SATB , #$7F00
        VDC.reg MWR  , #SCR64_64

        IRQ.control IRQ2_ON|VIRQ_ON|TIRQ_OFF

        TIMER.port  _7.00khz
        TIMER.cmd   TMR_OFF

        MAP_BANK #MAIN, MPR6
        jmp MAIN

;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;
;// Data / fixed bank


;Stuff for printing on screen
    .include "../base_func/video/print/lib.asm"

;other basic functions
    .include "../base_func/video/vdc/lib.asm"
    .include "HuTrack/engine/HuTrack_engine.asm"
    .include "../base_func/IO/gamepad/lib.asm"
    .include "../lib/controls/lib.asm"
;end DATA
;//...................................................................

;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;
;// Interrupt routines

;//........
TIRQ.custom
    jmp [timer_vect]

TIRQ:   ;// Not used
        BBS2 <vector_mask, TIRQ.custom
        stz $1403
        rti

;//........
BRK.custom
    jmp [brk_vect]
BRK:
        BBS1 <vector_mask, BRK.custom
        rti

;//........
VDC.custom
    jmp [vdc_vect]

VDC:
        BBS0 <vector_mask, VDC.custom
          pha
        lda IRQ.ackVDC
        sta <vdc_status
        bit #$20
        bne VDC.vsync
VDC.hsync
        BBS4 <vector_mask, VDC.custom.hsync
        BBS5 <vdc_status, VDC.vsync
          pla
        rti

VDC.custom.hsync
    jmp [vdc_hsync]

VDC.custom.vsync
    jmp [vdc_vsync]

VDC.vsync
        phx
        phy
        BBS3 <vector_mask, VDC.custom.vsync

VDC.vsync.rtn
        ply
        plx
        pla
      stz __vblank
  rti

;//........
NMI:
        rti

;end INT

;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;
;// INT VECTORS

  .org $fff6

    .dw BRK
    .dw VDC
    .dw TIRQ
    .dw NMI
    .dw startup

;..............................................................................................................
;..............................................................................................................
;..............................................................................................................
;..............................................................................................................
;Bank 0 end





;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;
;// Main code bank @ $C000

;....................................
    .bank $01, "MAIN"
    .org $c000
;....................................


MAIN:

        ;................................
        ;Turn display on
        VDC.reg CR , #(BG_ON|SPR_ON|VINT_ON|HINT_ON)

        ;...............................
        ; Initialize gamepad IO and controls
        call Controls.Init
        call Gamepad.Init

        ;................................
        ;Load font
        loadCellToVram Font, $1000
        loadCellToCram.BG Font, 0


        HuTrack.setDDAvector timer_vect

        ; ;...............................
        ; Set the DDA routine and music engine ISRs
        ISR.setVector TIMER_VEC , HuTrackEngine.7khz.IRQ
        ISR.setVecMask TIMER_VEC

        ISR.setVector VDC_VSYNC , HuTrackEngine.EngineCall
        ISR.setVecMask VDC_VSYNC

        HuTrack.setVDCreturnVector #VDC.vsync.rtn, HuTrack.returnVec


        ;................................
        ;Clear map
        jsr ClearScreen.64x32

        ;...............................
        ; Reset the variables for the music engine
        HuTrack.CallFar HuTrackEngine.Init

        ;...............................
        ; TIRQ is already enabled, but TIMER needs to be as well
        TIMER.port  _7.00khz
        TIMER.cmd   TMR_ON
        IRQ.control IRQ2_ON|VIRQ_ON|TIRQ_ON

        ;...............................
        ; load in song
        LEA.l Song, $4000, _hk.EAX0
        HuTrack.CallFar HuTrackEngine.QueueSong


        ;...............................
        ; Play in song
        MOVE.b #$00, <_hk.EAX0.l
        MOVE.b #$00, <_hk.EAX0.m
        HuTrack.CallFar HuTrackEngine.playSong

        ;................................
        ;start the party
        Interrupts.enable

        PRINT_STR_i "HuTrack ver: 0.8.8",2,2

        PRINT_STR_i "Song: ",2,4
        PRINT_STR_a_ptr HuTrack.songName
        PRINT_STR_i "author: ",2,5
        PRINT_STR_a_ptr HuTrack.songAuthor
        PRINT_STR_i "Number of instruments: ",2,7
        PRINT_BYTEhex_a_q  HuTrack.instrLen
        PRINT_STR_i "Number of patterns: ",2,8
        PRINT_BYTEhex_a_q HuTrack.patternListlen
        PRINT_STR_i "Number of waveforms: ",2,9
        PRINT_BYTEhex_a_q HuTrack.waveformLen
        PRINT_STR_i "Number of samples: ",2,10
        PRINT_BYTEhex_a_q HuTrack.sampleListLen

        stz sampleStart

        WAITVBLANK 10


main_loop:
        WAITVBLANK
        call Gamepad.READ_IO.single_controller
        call Controls.ProcessInput

        PRINT_STR_i "Current Tick 1: ",2,12
        PRINT_BYTEhex_a_q  HuTrack.tickReload + 1
        PRINT_STR_i "Current Tick 2: ",2,13
        PRINT_BYTEhex_a_q  HuTrack.tickReload

        PRINT_STR_i "Channel 0 Note: ",2,14
        ldx #$00
        lda HuTrack.channel.note,x
        jsr showNote
        PRINT_STR_a_i "  Octave: "
        ldx #$00
        PRINT_LO_Nibblehex_a_q HuTrack.channel.octave,x
        PRINT_STR_a_i "  "
        PRINT_STR_i "Channel 1 Note: ",2,15
        ldx #$01
        lda HuTrack.channel.note,x
        jsr showNote
        PRINT_STR_a_i "  Octave: "
        ldx #$01
        PRINT_LO_Nibblehex_a_q HuTrack.channel.octave,x
        PRINT_STR_a_i "  "
        PRINT_STR_i "Channel 2 Note: ",2,16
        ldx #$02
        lda HuTrack.channel.note,x
        jsr showNote
        PRINT_STR_a_i "  Octave: "
        ldx #$02
        PRINT_LO_Nibblehex_a_q HuTrack.channel.octave,x
        PRINT_STR_a_i "  "
        PRINT_STR_i "Channel 3 Note: ",2,17
        ldx #$03
        lda HuTrack.channel.note,x
        jsr showNote
        PRINT_STR_a_i "  Octave: "
        ldx #$03
        PRINT_LO_Nibblehex_a_q HuTrack.channel.octave,x
        PRINT_STR_a_i "  "
        PRINT_STR_i "Channel 4 Note: ",2,18
        ldx #$04
        lda HuTrack.channel.note,x
        jsr showNote
        PRINT_STR_a_i "  Octave: "
        ldx #$04
        PRINT_LO_Nibblehex_a_q HuTrack.channel.octave,x
        PRINT_STR_a_i "  "
        PRINT_STR_i "Channel 5 Note: ",2,19
        ldx #$05
        lda HuTrack.channel.note,x
        jsr showNote
        PRINT_STR_a_i "  Octave: "
        ldx #$05
        PRINT_LO_Nibblehex_a_q HuTrack.channel.octave,x
        PRINT_STR_a_i "  "

        PRINT_STR_i "Channel 0 Pattern #: ",2,20
        ldx #$00
        PRINT_BYTEhex_a_q HuTrack.channel.pattern.idx,x
        PRINT_STR_i "Channel 1 Pattern #: ",2,21
        ldx #$01
        PRINT_BYTEhex_a_q HuTrack.channel.pattern.idx,x
        PRINT_STR_i "Channel 2 Pattern #: ",2,22
        ldx #$02
        PRINT_BYTEhex_a_q HuTrack.channel.pattern.idx,x
        PRINT_STR_i "Channel 3 Pattern #: ",2,23
        ldx #$03
        PRINT_BYTEhex_a_q HuTrack.channel.pattern.idx,x
        PRINT_STR_i "Channel 4 Pattern #: ",2,24
        ldx #$04
        PRINT_BYTEhex_a_q HuTrack.channel.pattern.idx,x
        PRINT_STR_i "Channel 5 Pattern #: ",2,25
        ldx #$05
        PRINT_BYTEhex_a_q HuTrack.channel.pattern.idx,x

        PRINT_STR_i "  Index: ",25,20
        ldx #$00
        PRINT_BYTEhex_a_q HuTrack.channel.pattern.num,x
        PRINT_STR_i "  Index: ",25,21
        ldx #$01
        PRINT_BYTEhex_a_q HuTrack.channel.pattern.num,x
        PRINT_STR_i "  Index: ",25,22
        ldx #$02
        PRINT_BYTEhex_a_q HuTrack.channel.pattern.num,x
        PRINT_STR_i "  Index: ",25,23
        ldx #$03
        PRINT_BYTEhex_a_q HuTrack.channel.pattern.num,x
        PRINT_STR_i "  Index: ",25,24
        ldx #$04
        PRINT_BYTEhex_a_q HuTrack.channel.pattern.num,x
        PRINT_STR_i "  Index: ",25,25
        ldx #$05
        PRINT_BYTEhex_a_q HuTrack.channel.pattern.num,x


        jsr playSample

      jmp main_loop

showNote:
        and #$0f
        asl a
        asl a
        tay
        adc #low(noteDisplay)
        sta <R0
        lda #high(noteDisplay)
        adc #$00
        sta <R0+1
        PRINT_STR_a
  rts

playSample:

        ldx #$05
        lda <HuTrack.dda.bank,x
      bpl .skip
        lda #$05
        CallFar HuTrackEngine.chanReleaseSFX
        stz sampleStart
.skip

.b1.check
        lda input_state.buttons
        and #control.b1.mask
        cmp #control.b1.pressed
      beq .load_sample
        jmp .out

.load_sample
        lda #$05
        sta <_hk.EAX0.l
        CallFar HuTrackEngine.setChanForSFX
        lda #$80
        sta sampleStart

          PUSHBANK.2 $02
          MAP_BANK.2 #Sample1, MPR2

        ldy #$05
        lda #$df
          php
          sei
        sty $800
        sta $804
          plp

        lda #$ff
          php
          sei
        sty $800
        sta $805
          plp


        cly
        lda Sample1,y
        sta <_hk.EAX0.l
        lda Sample1+1,y
        sta <_hk.EAX0.m
        lda Sample1+2,y
        sta <_hk.EAX0.h
        lda #$05
        sta <_hk.EAX0.u
        CallFar HuTrackEngine.SfxPcmRequest

          PULLBANK.2 $02

.out
  rts


;Main end
;//...................................................................

noteDisplay:
    .db "C ",0,0
    .db "C#",0,0
    .db "D ",0,0
    .db "D#",0,0
    .db "E ",0,0
    .db "F ",0,0
    .db "F#",0,0
    .db "G ",0,0
    .db "G#",0,0
    .db "A ",0,0
    .db "A#",0,0
    .db "B ",0,0
    .db "??",0,0
    .db "??",0,0
    .db "??",0,0
    .db "??",0,0

;//...................................................................

    .include "HuTrack/HuTrack_lib.asm"


;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;

;....................................
    .code
    .bank $02, "Subcode 1"
    .org $8000
;....................................

  IncludeBinary Font.cell, "../base_func/video/print/font.dat"

Font.pal: .db $00,$00,$33,$01,$ff,$01,$ff,$01,$ff,$01,$ff,$01,$ff,$01,$f6,$01
Font.pal.size = sizeof(Font.pal)

    ;// Support files for MAIN

;...................................
init_audio
                ldx #$05
.loop
                stx $800
                stz $801
                stz $802
                stz $803
                stz $804
                stz $805
                stz $806
                stz $807
                stz $808
                stz $809
                dex
            bpl .loop
    rts

;...................................
init_video

                clx
                ldy #$80
                st0 #$00
                st1 #$00
                st2 #$00
                st0 #$02

.loop
                st1 #$00
                st2 #$00
                dex
            bne .loop
                dey
            bne .loop

                clx
                stz $402
                stz $403
.loop1
                stz $404
                stz $405
                inx
            bne .loop1

    rts





;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;

;....................................
    .code
    .bank $08, "HuTrack Engine"
    .org $c000
;....................................

    .include "HuTrack/engine/HuTrack_parser.asm"


;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;



;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;

;....................................
    .code
    .bank $10, "Song"
    .org $4000
;....................................

  .page 2
Song:
    .include "../assets/song/smb3_overworld/smb3_overworld.song.inc"
Song.end

;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;

;....................................
    .code
    .bank $20, "Samples"
    .org $4000
;....................................

  .page 2
Sample1:
    .include "../assets/sfx/sample1/test.inc"
Sample1.end


;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;/////////////////////////////////////////////////////////////////////////////////
;


