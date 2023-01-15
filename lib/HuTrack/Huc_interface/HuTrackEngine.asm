
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




  .bank SOUND_BANK, "HuTrack"
  .page $06

    .include "HuTrack/engine/HuTrack_parser.asm"
    .include "HuTrack/HuTrack_lib.asm"

  .bank LIB1_BANK


