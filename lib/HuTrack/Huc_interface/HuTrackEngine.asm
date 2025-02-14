
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

        lda #$ff
          php
          sei
            stx $800
            sta $805
          plp

.out
    rts

; #pragma fastcall HuTrackEngine_chanReleaseSFX(byte __al);
_HuTrackEngine_chanReleaseSFX.1:
        ldx <__al
        cpx #06
      bcs .out
        stz HuTrack.SFX.inProgress, x

        lda HuTrack.channel.panState,x
          php
          sei
            stx $800
            sta $805
          plp

.out
    rts

; int __fastcall HuTrackEngine_stopPcm (unsigned char channel<__al>);
_HuTrackEngine_stopPcm.1:
        ldx <__al
        cpx #$06
      bcs .error
        bit HuTrack.SFX.inProgress,x
      bpl .error

        lda #$80
        sta <HuTrack.dda.bank,x

        ; No error
        lda #$01
        clx
        clc
.out    
  rts

.error
        clx
        cla
        sec
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
        adc #$00
        and #$1f
        ora #$40
        sta <HuTrack.dda.addr.hi,x
        sta <HuTrack.dda.addr.loop.hi,x
        lda <__fbank
        adc #$00
        sta <HuTrack.dda.bank,x
        sta <HuTrack.dda.loop.bank,x
        rmb7 <HuTrack.DDAprocess

        ; No error
        lda #$01
        clx
        clc
.out    
  rts

.error
        clx
        cla
        sec
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
        and #$7f
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

        lda HuTrack.DDAprocess
          pha
        and #$7f
        sta HuTrack.DDAprocess

        stx $800
        lda #$d0
        sta $804

          pla
        sta HuTrack.DDAprocess

        lda #$01
        clx
        clc
.out    
  rts

.error
        clx
        cla
        sec
  rts

;//.........................................................
; int __fastcall HuTrackEngine_SFXmode();
_HuTrackEngine_SFXmode:

        clx
.loop
        lda HuTrack.SFX.inProgress,x
        cmp #$80
        say
        ror 
        say

        inx
        cpx #$06
      bcc .loop 
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
        clx
        clc
.out    
  rts

.error
        clx
        cla
        sec
  rts

;//.........................................................
_getFarPointer.3

            lda __fbank
            sta [__ax]
            cly
            lda __fptr
            sta [__bx],y
            iny
            lda __fptr+1
            and #$1F
            sta [__bx],y
    rts

_getFarPointer2.3 .macro
            lda __fbank
            sta [__ax]
            cly
            lda __fptr
            sta [__bx],y
            iny
            lda __fptr+1
            and #$1F
            sta [__bx],y
  .endm

  .ifdef HUCC
_getDataPtr.1 .macro
            lda #$E0
            trb __ah
  .endm
  .endif

;//.........................................................

  .bank SOUND_BANK, "HuTrack"
  .page $06

    .include "HuTrack/engine/HuTrack_parser.asm"
    .include "HuTrack/HuTrack_lib.asm"

  .ifdef HUCC
  .bank CORE_BANK
  .else
    .include "HuSFX/HuSFX_lib.asm"
  .bank LIB1_BANK
  .endif
