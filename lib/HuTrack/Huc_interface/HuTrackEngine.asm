
;//
;// file: HuTrackEngine.asm
;//
;//

  .include "HuTrack/engine/HuTrack_engine.asm"


  ;// This is a quick fix because current version of HuC doesn't have the proper VDC mask hanlder code.

HUTRACK_HUC_HUCC_RETURN .macro

  .ifndef HUCC
      sxy
      sax
  .endif

  .endm


;...............................................
;
;#pragma fastcall HuTrack_Init();
_HuTrack_Init:
      tma #$06
      pha
      lda #bank(HuTrackEngine.Init)
      tam #$06
      jsr HuTrackEngine.Init
      pla
      tam #$06

      ;// Enable user_int for TRIQ
        php
        sei
      SMB2 <irq_m
      lda #low(HuTrackEngine.7khz.IRQ)
      sta timer_jmp
      lda #high(HuTrackEngine.7khz.IRQ)
      sta timer_jmp+1
      .ifdef HUCC
      lda #low(_HuTrackEngine.CORE.VBL.IRQ)
      sta sound_hook
      lda #high(_HuTrackEngine.CORE.VBL.IRQ)
      sta sound_hook+1
      .endif

        plp
      
      lda #$00
      sta $c00
  rts

      .ifdef HUCC
_HuTrackEngine.CORE.VBL.IRQ:
      HutrackEngine.ManualCall
      rts
      .endif

;...............................................
;
;#pragma fastcall HuTrackEngine_QueueSong(farptr __fbank:__fptr);
_HuTrackEngine_QueueSong.1:
        lda __fptr
        sta <_hk.EAX0.l
        lda __fptr+1
        and #$1f
        ora #$40
        sta <_hk.EAX0.m
        lda __fbank
        sta <_hk.EAX0.h
        tma #$06
        pha
        lda #bank(HuTrackEngine.QueueSong)
        tam #$06
        jsr HuTrackEngine.QueueSong
        pla
        tam #$06
  rts


;...............................................
;
;#pragma fastcall HuTrackEngine_PlaySong(byte __al);
_HuTrackEngine_PlaySong.1:

        lda __al
        sta <_hk.EAX0.l
        lda #$00
        sta <_hk.EAX0.m

        tma #$06
        pha
        lda #bank(HuTrackEngine.playSong)
        tam #$06
        jsr HuTrackEngine.playSong
        pla
        tam #$06
  rts


;...............................................
;
;#pragma fastcall HuTrackEngine_PlayOnce(byte __al);
_HuTrackEngine_PlayOnce.1:

        lda __al
        sta <_hk.EAX0.l
        lda #$01
        sta <_hk.EAX0.m

        tma #$06
        pha
        lda #bank(HuTrackEngine.playSong)
        tam #$06
        jsr HuTrackEngine.playSong
        pla
        tam #$06
  rts

;...............................................
;
; #pragma fastcall HuTrackEngine_Pause();
_HuTrackEngine_Stop:
_HuTrackEngine_Pause:
        tma #$06
        pha
        lda #bank(HuTrackEngine.pause)
        tam #$06
        jsr HuTrackEngine.pause
        pla
        tam #$06
          php
          sei
        ldx #5
.loop
        bit HuTrack.SFX.inProgress,x
      bmi .next
        stx $800
        stz $804
        stz $807
        lda #$80
        sta <HuTrack.dda.inactive,x
        sta <HuTrack.dda.bank,x
        sta HuTrack.channel.waitNote,x
.next
        dex
      bpl .loop
        lda HuTrack.SFX.inProgress
        ora HuTrack.SFX.inProgress+1
      bne .out
        stz $809
.out
          plp
        rts

; Global stereo attenuation, either packed nibbles or two 8-bit levels.

_HuTrackEngine_SetGlobal.1:
        sta HuTrack.Global.SetVolume
        lda #$80
        sta HuTrack.Global.VolUpdate
  rts

;#pragma fastcall HuTrackEngine_SetGlobal(byte __al, byte __ah);
_HuTrackEngine_SetGlobal.2:
        lda <__al
        and #$f0
        sta HuTrack.Global.SetVolume
        lda <__ah
        lsr a
        lsr a
        lsr a
        lsr a
        ora HuTrack.Global.SetVolume
        sta HuTrack.Global.SetVolume
        lda #$80
        sta HuTrack.Global.VolUpdate
  rts

; #pragma fastcall HuTrackEngine_getCurrSongTitle(farptr __fbank:__fptr);
_HuTrackEngine_getCurrSongTitle.1:

        tma #$03
            pha
        tma #$04
            pha

        lda __fbank
        tam #$03
        inc a
        tam #$04

        cly
        lda __fptr
        sta <HuTrack.addr0
        lda __fptr+1
        and #$1f
        ora #$60
        sta <HuTrack.addr0+1

.loop
        lda HuTrack.songName,y
      beq .out
        sta [HuTrack.addr0],y
        iny
        cpy #47
      bcc .loop
.out

        cla
        sta [HuTrack.addr0],y

        pla
        tam #$04
        pla
        tam #$03

    rts

; #pragma fastcall HuTrackEngine_getCurrSongAuthor(farptr __fbank:__fptr);
_HuTrackEngine_getCurrSongAuthor.1:

        tma #$03
            pha
        tma #$04
            pha

        lda __fbank
        tam #$03
        inc a
        tam #$04

        cly
        lda __fptr
        sta <HuTrack.addr0
        lda __fptr+1
        and #$1f
        ora #$60
        sta <HuTrack.addr0+1

.loop
        lda HuTrack.songAuthor,y
      beq .out
        sta [HuTrack.addr0],y
        iny
        cpy #47
      bcc .loop
.out

        cla
        sta [HuTrack.addr0],y

        pla
        tam #$04
        pla
        tam #$03

    rts


; #pragma fastcall HuTrackEngine_chanReserve(byte __al);
_HuTrackEngine_chanReserve.1:

        ldx <__al
        cpx #06
      bcs .out
        lda #$80
        sta HuTrack.SFX.inProgress, x
        sta HuTrack.channel.waitNote, x
        sta <HuTrack.dda.inactive,x
        sta <HuTrack.dda.bank, x

          php
          sei
        stx $800
        stz $804
        stz $807
        ; The PSG LFO couples channels 0/1 only.
        cpx #2
      bcs .pan
        stz $809
.pan
        lda #$ff
        sta $805
          plp

.out
    rts

; #pragma fastcall HuTrackEngine_chanRelease(byte __al);
_HuTrackEngine_chanRelease.1:
        ldx <__al
        cpx #06
      bcs .out
        ; Repeated release must not silence a channel that music owns.
        bit HuTrack.SFX.inProgress,x
      bpl .out
          php
          sei
        lda #$80
        sta <HuTrack.dda.inactive,x
        sta <HuTrack.dda.bank,x
        sta HuTrack.channel.waitNote,x
        .ifdef HuSFX.stream.bnk
        lda #$ff
        sta HuSFX.stream.bnk,x
        stz HuSFX.delay,x
        .endif
        stx $800
        stz $804
        stz $807
        stz HuTrack.SFX.inProgress,x
        cpx #2
      bcs .lfo.done
        stz $809
.lfo.done
        lda #$ff
        sta HuTrack.channel.uploadedWaveform,x
          plp

.out
    rts

;//.........................................................
; int __fastcall HuTrackEngine_PCMStatus(unsigned char channel<__al>);
; NOTE: HuCC return style (Y:A). Return macro swaps back to HuC format (A:X).
_HuTrackEngine_PCMStatus.1:
      ldx <__al
        cpx #$06
      bcs .error
        bit HuTrack.SFX.inProgress,x
      bpl .error
        lda <HuTrack.dda.inactive,x
        cmp #$80 
      beq .nosfx      
        lda #1
        cly
      bra .return
.nosfx  
        cla 
        cly    
      bra .return
.error 
        lda #2
        cly 
  
.return
  HUTRACK_HUC_HUCC_RETURN
 rts

; int __fastcall HuTrackEngine_stopPcm (unsigned char channel<__al>);
_HuTrackEngine_stopPcm.1:
        ldx <__al
        cpx #$06
      bcs .error
        bit HuTrack.SFX.inProgress,x
      bpl .error

        lda #$80
        sta <HuTrack.dda.inactive,x
        sta <HuTrack.dda.bank,x

        ; No error
        lda #$01
        cly
        clc
.out
  HUTRACK_HUC_HUCC_RETURN
  rts

.error
        cly
        cla
        sec
  HUTRACK_HUC_HUCC_RETURN
  rts

; int __fastcall HuTrackEngine_PcmRequest(unsigned char channel<__al>, unsigned char bank<__fbank>, unsigned int addr<__fptr>);
; int __fastcall HuTrackEngine_PcmRequest(unsigned char channel<__al>, char far *pcm<__fbank:__fptr>);
_HuTrackEngine_PcmRequest.2:
_HuTrackEngine_PcmRequest.3:
        stz <__cl
        lda #$8f
        sta <__ch
; int __fastcall HuTrackEngine_PcmRequest(unsigned char channel<__al>, unsigned char bank<__fbank>, unsigned int addr<__fptr>, char mask1<__cl>, char mask2<__ch>);
; int __fastcall HuTrackEngine_PcmRequest(unsigned char channel<__al>, char far *pcm<__fbank:__fptr>, char mask1<__cl>, char mask2<__ch> );
_HuTrackEngine_PcmRequest.4:
_HuTrackEngine_PcmRequest.5:
        ldx <__al
        cpx #$06
      bcs .error
        bit HuTrack.SFX.inProgress,x
      bpl .error

        lda #$80
        sta <HuTrack.dda.inactive,x
        sta <HuTrack.dda.bank,x

        lda <__ch
        ora #$80
        sta <HuTrack.dda.cntr1,x

        lda <__cl
        sta <HuTrack.dda.cntr0,x

        lda <__fptr
        clc
        adc #$03
        sta <HuTrack.dda.addr.lo,x
        sta <HuTrack.dda.addr.loop.lo,x
        lda <__fptr+1
        and #$1f
        adc #$00
        tay
        and #$1f
        ora #$40
        sta <HuTrack.dda.addr.hi,x
        sta <HuTrack.dda.addr.loop.hi,x
        tya
        cmp #$20
        lda <__fbank
        adc #$00
        sta <HuTrack.dda.loop.bank,x
          php
          sei
        stx $800
        stz $807
        lda #$df
        sta $804
        lda #$10
        sta $806
        lda <HuTrack.dda.loop.bank,x
        sta <HuTrack.dda.inactive,x
        sta <HuTrack.dda.bank,x
        stz <HuTrack.dda.inactive,x
        rmb7 <HuTrack.DDAprocess
          plp

        ; No error
        lda #$01
        cly
        clc
.out
  HUTRACK_HUC_HUCC_RETURN
  rts

.error
        cly
        cla
        sec
  HUTRACK_HUC_HUCC_RETURN
  rts

_getFarBank.1
    ldx __bl
  rts

_getFarAddress.1
    lda __si+1
    ldx __si
  rts

;//.........................................................
; int __fastcall HuTrackEnginePauseDDA();
_HuTrackEnginePauseDDA:

        lda HuTrack.DDAprocess
        sta HuTrack.DDAprocessBackup
        ora #$80
        sta HuTrack.DDAprocess
  rts

;//.........................................................
; int __fastcall HuTrackEngineResumeDDA();
_HuTrackEngineResumeDDA:
        lda HuTrack.DDAprocessBackup
        sta HuTrack.DDAprocess
  rts


;//.........................................................
; int __fastcall HuTrackEngineSFXrest(unsigned char channel<__al>);
_HuTrackEngineSFXrest.1:

        ldx <__al
        cpx #$06
      bcs .error
        bit HuTrack.SFX.inProgress,x
      bpl .error

          php
          nop
          sei

        stx $800
        stz $804
        lda #$80
        sta <HuTrack.dda.inactive,x
        sta <HuTrack.dda.bank,x

          plp

        lda #$01
        cly
        clc
.out
  HUTRACK_HUC_HUCC_RETURN
  rts

.error
        cly
        cla
        sec
  HUTRACK_HUC_HUCC_RETURN
  rts

;//.........................................................
; int __fastcall HuTrackEngine_SFXmode();
_HuTrackEngine_SFXmode:
        ; Return bits 0..5, one per reserved channel, in the compiler ABI.
        clx
        cly
.loop
        lda HuTrack.SFX.inProgress,x
        cmp #$80
        tya
        ror a
        tay
        inx
        cpx #$06
      bcc .loop
        tya
        lsr a
        lsr a
        cly
        HUTRACK_HUC_HUCC_RETURN
  rts

;//.........................................................
; int __fastcall HuTrackEngine_SFXmode(unsigned char channel<__al>);
_HuTrackEngine_SFXmode.1:

        ldx <__al
        cpx #$06
      bcs .error
        bit HuTrack.SFX.inProgress,x
      bpl .error

        lda #$01
        cly
        clc
.out
  HUTRACK_HUC_HUCC_RETURN
  rts

.error
        cly
        cla
        sec
  HUTRACK_HUC_HUCC_RETURN
  rts

;//.........................................................

  .bank SOUND_BANK, "HuTrack"
  .page $06
  ; HuCC can pack procedures into this bank's spare space between passes.
  ; Keep the driver anchored when a code-size change alters that packing.
  .org $c000

    .include "HuTrack/engine/HuTrack_parser.asm"
    .include "HuTrack/HuTrack_lib.asm"
HuTrack.CodeEnd:
  .if (bank(HuTrack.CodeEnd-1)!=SOUND_BANK)
    .fail HuTrack music code exceeds SOUND_BANK.
  .endif

    ; Ordinary compiler data, outside both fixed libraries and music code.
  .ifdef HUCC
  .if RESERVE_BANKS < 1
    .fail HuTrack requires one reserved bank for its ROM tables.
  .endif
  .bank RESERVED_BANK, "HuTrack Tables"
  .org $8000
  .else
  .data
  .bank CONST_BANK
  .align $2000
  .page 4
  .endif
    .include "HuTrack/engine/HuTrack_pitch_tables.inc"
  .ifndef HUCC
    ; HuC permanently maps its following string constants through MPR2.
  .page 2
  .endif
  .code

  .ifdef HUCC
  .bank CORE_BANK
  .else
  .bank LIB1_BANK
  .endif
