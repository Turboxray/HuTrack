
  .include "HuTrack/engine/HuTrack_engine.asm"


  ;// This is a quick fix because current version of HuC doesn't have the proper VDC mask hanlder code.


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
        plp
      
      lda #$00
      sta $c00
  rts

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
_HuTrackEngine_Pause:
        tma #$06
        pha
        lda #bank(HuTrackEngine.pause)
        tam #$06
        jsr HuTrackEngine.pause
        pla
        tam #$06

        ldx #05
        lda #$DF
.loop
        stx $800
        sta $804
        stz $807
        stz $808
        stz $809
      dex
        bpl .loop
  rts

;...............................................
;
; #pragma fastcall HuTrackEngine_Stop();
_HuTrackEngine_Stop:
        tma #$06
        pha
        lda #bank(HuTrackEngine.pause)
        tam #$06
        jsr HuTrackEngine.pause
        pla
        tam #$06

        ldx #05
        lda #$DF
.loop
        stx $800
        sta $804
        stz $807
        stz $808
        stz $809
      dex
        bpl .loop
  rts

;...............................................
;
;#pragma fastcall HuTrackEngine_SetGlobal(byte acc);
_HuTrackEngine_SetGlobal.1:
        sax
        sta HuTrack.Global.SetVolume
        lda #$80
        sta HuTrack.Global.VolUpdate
  rts

;#pragma fastcall HuTrackEngine_SetGlobal(byte __al, byte __ah);
_HuTrackEngine_SetGlobal.2:
        lda <__al
        lsr a
        lsr a
        lsr a
        lsr a
        sta HuTrack.Global.SetVolume
        lda <__ah
        lsr a
        lsr a
        lsr a
        lsr a
        and HuTrack.Global.SetVolume
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


; #pragma fastcall HuTrackEngine_chanSetSFX(byte __al);
_HuTrackEngine_chanSetSFX.1:

        ldx <__al
        cpx #06
      bcs .out
        lda #$80
        sta HuTrack.SFX.inProgress, x
        sta <HuTrack.dda.bank, x

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

.out
    rts

; #pragma fastcall HuTrackEngine_chanReleaseSFX(byte __al);
_HuTrackEngine_chanReleaseSFX.1:
        ldx <__al
        cpx #06
      bcs .out
        stz HuTrack.SFX.inProgress, x
.out
    rts

  .bank SOUND_BANK, "HuTrack"
  .page $06

    .include "HuTrack/engine/HuTrack_parser.asm"
    .include "HuTrack/HuTrack_lib.asm"

  .bank LIB1_BANK


