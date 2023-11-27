;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
; HuTrack music engine for PC-Engine
;
; Ver: 0.1
;
; History:
; -------
;
;
;

    .include "HuTrack/HuTrack_version.inc"



;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Initialize DDA and engine                                                                               /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;#init

HuTrackEngine.Init:

        ; Clear song list
        stz song_slot

        lda #$ff
        sta HuTrack.Global.SetVolume
        stz HuTrack.Global.VolUpdate

        stz <HuTrack.Status

HuTrackEngine.Reset

        ;#TODO this ultimately needs to change. But for now, starting a new song
        smb5 <HuTrack.Status
        ; Stop parsing songs
        smb6 <HuTrack.Status

        ; Disable playback of samples
        lda #$80+$3f
        sta HuTrack.DDAprocess


        ; Set tempo to default
        lda #$05
        sta HuTrack.tick
        sta HuTrack.tickReload      ; Default both tick counter
        sta HuTrack.tickReload+1
        stz HuTrack.TickIdx

        stz HuTrack.channel.patternBreak

        lda #$ff
        sta $801

        clx
.loop
        stx $800
        lda #$ff
        sta $805
        lda #$9f
        sta $804
        lda #$df
        sta $804
        lda #$9f
        sta $804
        stz $804
        stz $807

        lda #$00
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806

        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806

        lda #$80
        sta HuTrack.channel.detune,x
        stz HuTrack.channel.relativeVolume,x
        lda #$1f
        stz HuTrack.channel.directVolume,x
        lda #$ff
        sta HuTrack.channel.instr,x
        lda #$80
        sta HuTrack.channel.vibrato.idx,x
        stz HuTrack.Enabled,x

        lda #$00
        sta HuTrack.channel.directWaveform,x
        lda #$ff
        sta HuTrack.channel.lastEnvWaveform,x

        lda #$80
        sta <HuTrack.dda.bank,x
        lda #$8F
        sta <HuTrack.dda.cntr1

        lda #$ff
        sta HuTrack.channel.panState,x

        stz HuTrack.SFX.inProgress,x

        lda #$ff
        sta HuTrack.SFXstream.bnk,x

        inx
        cpx #$06
      bcs .out
        jmp .loop
.out
  rts


;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Interface                                                                                               /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;interface

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
; Queue up song into playlist.
; input _hk.EAX0
;
HuTrackEngine.QueueSong:

        ldx song_slot
        lda <_hk.EAX0.l
        sta song_ptr.lo,x
        lda <_hk.EAX0.m
        sta song_ptr.hi,x
        lda <_hk.EAX0.h
        sta song_bank,x

        inc song_slot

  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.pause:

        smb6 <HuTrack.Status

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.FadeToPause:

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.FadeOut:

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.FadeIn:

;         cmp #$20
;       bcc .skip
;         lda #$1f
; .skip
;         ora #$80
;         sta HuTrackEngine.FadeToLevel
  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.SetVolume:
        sta HuTrack.Global.SetVolume
        lda #$80
        sta HuTrack.Global.VolUpdate
  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.stop:

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.Continue:

        rmb6 <HuTrack.Status

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.FadeToContinue:

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.SaveSongPosition:

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.LoadSongPosition:

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.setChanForSFX:
;...............................................
; Input <_hk.EAX0.l     lower nybble -> chan #

        ldx <_hk.EAX0.l
        cpx #$06
bcc .skip
        ldx #$05
.skip
        lda #$80
        sta HuTrack.SFX.inProgress,x
        sta <HuTrack.dda.bank,x

        lda #$df
          php
          sei
        stx $800
        sta $804
          plp

          php
          sei
        stx $800
        stz $807
          plp

          php
          sei
        stx $800
        stz $809
          plp


  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.chanReleaseSFX:
;...............................................
; Input <_hk.EAX0.u

        sec
        ldx <_hk.EAX0.u
        cpx #$06
      bcs .out
        clc
        stz HuTrack.SFX.inProgress,x
.out
  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.SfxPcmRequest:
;...............................................
; Input <_hk.EAX0.l     bank#
; Input <_hk.EAX0.m     lsb
; Input <_hk.EAX0.h     msb
; Input <_hk.EAX0.h     chan #

        sec
        ldx <_hk.EAX0.u
        cpx #$06
      bcs .out
        bit HuTrack.SFX.inProgress,x
      bpl .out

        ; No error
        clc
        lda #$80
        sta <HuTrack.dda.bank,x
        lda <_hk.EAX0.m
        sta <HuTrack.dda.addr.lo,x
        lda <_hk.EAX0.h
        and #$1f
        ora #$40
        sta <HuTrack.dda.addr.hi,x
        lda <_hk.EAX0.l
        sta <HuTrack.dda.bank,x
        rmb7 <HuTrack.DDAprocess
.out
  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.SfxPcmStatus:
;...............................................
; Input <_hk.EAX0.h     chan #

        sec
        ldx <_hk.EAX0.u
        cpx #$06
      bcs .out
        bit HuTrack.SFX.inProgress,x
      bpl .out

        ; No error
        clc
        lda <HuTrack.dda.bank,x
        sta <_hk.EAX0.l
        lda <HuTrack.dda.addr.lo,x
        sta <_hk.EAX0.m
        lda <HuTrack.dda.addr.hi,x
        sta <_hk.EAX0.h
.out
  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
; Input EAX0.l
HuTrackEngine.playSong:

        stz HuTrackEngine.VarStart
        tii HuTrackEngine.VarStart,HuTrackEngine.VarStart+1, (HuTrackEngine.VarEnd - HuTrackEngine.VarStart) - 1

        jsr HuTrackEngine.Reset

        lda <_hk.EAX0.m
        sta song_repeat

        _htk.MOVE.b <_hk.EAX0.l, current_song
        _htk.MOVE.b <_hk.EAX0.l, REG_X


        _htk.PUSHBANK.4 _htk.PAGE_4000
        _htk.MAP_BANK.4 song_bank,x , _htk.PAGE_4000
        _htk.MOVE.sw song_ptr, REG_X, <_hk.R1
        _htk.LEA.2  #$4000, <_hk.R1

        ;  _hk.R1 now pointing to the six track pointers
        cly
        clx

        _htk.MOVE.w [_hk.R1], <_hk.A0
        _htk.ADD.w #$04, <_hk.R1

        ; copy over the song and author names
        cly
        clx
.name.loop
        lda [_hk.R1],y
      beq .author
        iny
        sta HuTrack.songName,x
        inx
        cpx #47
      bne .name.loop
.author
        iny
        stz HuTrack.songName,x

        clx
.author.loop
        lda [_hk.R1],y
      beq .author.end
        iny
        sta HuTrack.songAuthor,x
        inx
        cpx #47
      bne .author.loop
.author.end
        stz HuTrack.songAuthor,x


.debug001
        ; get Pattern table
        _htk.MOVE.w [_hk.A0], <_hk.A1

        _htk.DEBUG_NOP

        ; get attributes..
        _htk.MOVE.b [_hk.A1], HuTrack.tickReload+1
        _htk.INC.w <_hk.A1
        _htk.MOVE.b [_hk.A1], HuTrack.tickReload
        _htk.INC.w <_hk.A1
        _htk.MOVE.b [_hk.A1], HuTrack.rowLen
        _htk.INC.w <_hk.A1
        _htk.MOVE.b [_hk.A1], HuTrack.patternListlen
        _htk.INC.w <_hk.A1
        _htk.MOVE.b [_hk.A1], HuTrack.instrLen
        _htk.INC.w <_hk.A1
        _htk.MOVE.b [_hk.A1], HuTrack.waveformLen
        _htk.INC.w <_hk.A1
        _htk.MOVE.b [_hk.A1], HuTrack.sampleListLen

        _htk.MOVE.b HuTrack.tickReload, HuTrack.tick
        stz HuTrack.TickIdx


        _htk.DEBUG_NOP

        ; get PatternList table
        _htk.ADD.w #$02, <_hk.A0
        _htk.MOVE.w [_hk.A0], <_hk.A1
        _htk.MOVE.w [_hk.A1], HuTrack.channel.patternList.table + 0
        _htk.ADD.w #$02, <_hk.A1
        _htk.MOVE.w [_hk.A1], HuTrack.channel.patternList.table + 2
        _htk.ADD.w #$02, <_hk.A1
        _htk.MOVE.w [_hk.A1], HuTrack.channel.patternList.table + 4
        _htk.ADD.w #$02, <_hk.A1
        _htk.MOVE.w [_hk.A1], HuTrack.channel.patternList.table + 6
        _htk.ADD.w #$02, <_hk.A1
        _htk.MOVE.w [_hk.A1], HuTrack.channel.patternList.table + 8
        _htk.ADD.w #$02, <_hk.A1
        _htk.MOVE.w [_hk.A1], HuTrack.channel.patternList.table + 10

        _htk.DEBUG_NOP

        ; get instrument table
        _htk.ADD.w #$02, <_hk.A0
        _htk.MOVE.w [_hk.A0], HuTrack.instr.table

        _htk.DEBUG_NOP

        ; get waveform table
        _htk.ADD.w #$02, <_hk.A0
        _htk.MOVE.w [_hk.A0], HuTrack.waveform.table

        _htk.DEBUG_NOP

        ; get pattern table
        _htk.ADD.w #$02, <_hk.A0
        _htk.MOVE.w [_hk.A0], HuTrack.pattern.table

        _htk.DEBUG_NOP

        ; get samples table
        _htk.ADD.w #$02, <_hk.A0
        _htk.MOVE.w [_hk.A0], HuTrack.samples.table


        _htk.DEBUG_NOP


        ; get bank table
        _htk.ADD.w #$02, <_hk.A0    ; skip past the last ptr (sample)

        _htk.ADD.w #$01, <_hk.A0    ; Skip this attribute bank for now (it was already handle above). #TODO: need to figure out if this should be used or not.

        _htk.MOVE.b [_hk.A0], HuTrack.patternList.table.bank
        _htk.ADD.w #$01, <_hk.A0
        _htk.MOVE.b [_hk.A0], HuTrack.instr.table.bank
        _htk.ADD.w #$01, <_hk.A0
        _htk.MOVE.b [_hk.A0], HuTrack.waveform.table.bank
        _htk.ADD.w #$01, <_hk.A0
        _htk.MOVE.b [_hk.A0], HuTrack.pattern.table.bank
        _htk.ADD.w #$01, <_hk.A0
        _htk.MOVE.b [_hk.A0], HuTrack.samples.table.bank


        clx
.loop

        lda #$80
        sta <HuTrack.dda.bank,x

        inx
        cpx #$06
      bne .loop

        rmb6 <HuTrack.Status     ;// start song

        _htk.PULLBANK.4 _htk.PAGE_4000
  rts



;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
; Input EAX0.l
HuTrackEngineSFXprocess

        clx
.loop
        lda HuTrack.SFXstream.bnk,x
        cmp #$ff
      beq .skip_entry

        lda HuTrack.sfx.delay,x
      bmi .skip_entry
      beq .do_entry
        dec HuTrack.sfx.delay,x
      bra .skip_entry

.do_entry
        jmp .process
.return_entry

.skip_entry
        inx
        cpx #$06
      bne .loop
  rts    


.process
        ; Map in stream
        tma #$02
        pha
        tma #$03
        pha
        lda HuTrack.SFXstream.bnk,x
        tam #$02
        inc a
        tam #$03

        ; Prep stream pointer
        lda HuTrack.SFXstream.lo,x
        sta <HuTrack.A0
        lda HuTrack.SFXstream.hi,x
        and #$1f
        ora #$40
        sta <HuTrack.A0 + 1


.decode_byte
        jsr .fetch_byte

        cmp #$A0
      bcs .next1
        jmp .804            ; < #$A0
.next1
        cmp #$B0
      bcs .next2
        jmp .reg_update     ; < #$B0
.next2
      bne .next3
        jmp .wf_update      ; == #$A0
.next3
        cmp #$D0
      bcs .next4
        jmp .frq_update     ; < #$D0
.next4
        cmp #$fb
      bne .next5
        jmp .eof            ; == #$FB
.next5
        cmp #$fc
      bne .next6
        jmp .play_pcm
.next6
        cmp #$fd
      bne .next7
        jmp .stop_pcm
.next7
        cmp #$fe
      bne .next8
        jmp .wait_n_frames
.next8
        cmp #$ff
      bne .next9
        jmp .wait_1_frame
.next9


;..............
.804
        sta HuTrack.sfx.control,x
            php
        sei
        stx $800
        sta $804
            plp
      jmp .decode_byte

;..............
.wf_update

        ;// This is a slow, but for now it works.

        lda #(HuTrack.DMA.TINop)
        sta HuTrack.DMA + 0
        lda #(HuTrack.DMA.RTSop)
        sta HuTrack.DMA + 7

        tma #$02
        pha
        tma #$03
        pha

      jsr .fetch_byte

          cly
          asl a
          say
          rol a
          say

          asl a
          say
          rol a
          say

          asl a
          say
          rol a
          say

          asl a
          say
          rol a
          say

          asl a
          say
          rol a
          say
          sty HuTrack.DMA + 2

        clc
        adc HuTrack.SFXwf.lo,x
        sta HuTrack.DMA + 1
        lda HuTrack.SFXwf.hi,x
        and #$1f
        ora #$40
        adc HuTrack.DMA + 2
        sta HuTrack.DMA + 2

        lda #low($806)
        sta HuTrack.DMA + 3
        lda #high($806)
        sta HuTrack.DMA + 4

        lda #low(32)
        sta HuTrack.DMA + 5
        lda #high(32)
        sta HuTrack.DMA + 6

        lda HuTrack.SFXwf.bnk,x

        tam #$02
        inc a
        tam #$03

          php
        nop
        sei
        stx $800
        lda HuTrack.sfx.control,x
        and #$1f
        sta $804
        jsr HuTrack.DMA
        lda HuTrack.sfx.control,x
        sta $804
          plp

        pla
        tam #$03
        pla
        tam #$02

      jmp .decode_byte

;..............
.reg_update
        and #$0f
        tay
      jsr .fetch_byte
            php
        sei
        stx $800
        sta $800,y
            plp
      jmp .decode_byte


;..............
.frq_update
        and #$0f
        tay
      jsr .fetch_byte
            php
        sei
        stx $800
        sta $802
        sty $803
            plp
      jmp .decode_byte


;..............
.eof
        lda #$ff
        sta HuTrack.SFXstream.bnk,x
      jmp .exit_parse

;..............
.play_pcm
      jsr .fetch_byte
      jsr .fetch_byte
        ; Skip PCM operands for now
      jmp .decode_byte

;..............
.stop_pcm
        ; TODO
      jmp .decode_byte

;..............
.wait_n_frames
      jsr .fetch_byte
        and #$7f
        sta HuTrack.sfx.delay,x
      jmp .exit_parse
;..............
.wait_1_frame
        lda #$01
        sta HuTrack.sfx.delay,x
      jmp .exit_parse


;.............................
.inc_ptr
            pha
        inc <HuTrack.A0
      bne .inc_ptr.out
        inc <HuTrack.A0 + 1
        lda <HuTrack.A0 + 1
        cmp #$60
      bne .inc_ptr.out
        and #$1f
        ora #$40
        sta <HuTrack.A0 + 1
        inc HuTrack.SFXstream.bnk,x
        lda HuTrack.SFXstream.bnk,x
        tam #$02
        inc a
        tam #$03
.inc_ptr.out
            pla
  rts

;..................
.fetch_byte
        lda [HuTrack.A0]
      jmp .inc_ptr


;..................
.exit_parse
        lda <HuTrack.A0
        sta HuTrack.SFXstream.lo,x
        lda <HuTrack.A0 + 1
        sta HuTrack.SFXstream.hi,x

        pla
        tma #$03
        pla
        tma #$02
    jmp .return_entry



;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
; Input EAX0.l

