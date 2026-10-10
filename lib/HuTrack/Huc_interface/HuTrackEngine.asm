
;//
;// file: HuTrackEngine.asm
;//
;//

HuTrack.FixedCodeStart:
  .include "HuTrack/engine/HuTrack_engine.asm"


  ; Translate a 16-bit result from HuCC Y:A to HuC A:X when needed.

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
        php
        sei
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
        plp
        txa
        cly
        cpx #64
      bcc .return
        lda #$ff
        tay
.return
        HUTRACK_HUC_HUCC_RETURN
  rts


;...............................................
;
;#pragma fastcall HuTrackEngine_PlaySong(byte __al);
_HuTrackEngine_PlaySong.1:
        php
        sei

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
        plp
  rts


;...............................................
;
;#pragma fastcall HuTrackEngine_PlayOnce(byte __al);
_HuTrackEngine_PlayOnce.1:
        php
        sei

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
        plp
  rts

;...............................................
;
; #pragma fastcall HuTrackEngine_Pause();
_HuTrackEngine_Stop:
        php
        sei
        HuTrack.CallFar HuTrackEngine.stop
        plp
        rts

_HuTrackEngine_Pause:
        php
        sei
        HuTrack.CallFar HuTrackEngine.pause
        plp
        rts

_HuTrackEngine_Resume:
        php
        sei
        HuTrack.CallFar HuTrackEngine.Continue
        plp
        rts

_HuTrackEngine_FadeIn.1:
        php
        sei
        ldy <__al
        HuTrack.CallFar HuTrackEngine.FadeIn
        plp
        rts

_HuTrackEngine_FadeOut.1:
        php
        sei
        ldy <__al
        HuTrack.CallFar HuTrackEngine.FadeOut
        plp
        rts

_HuTrackEngine_FadeToPause.1:
        php
        sei
        ldy <__al
        HuTrack.CallFar HuTrackEngine.FadeToPause
        plp
        rts

_HuTrackEngine_SetMusicVolume.1:
        stz <__ah
_HuTrackEngine_FadeTo.2:
        php
        sei
        tma #6
        pha
        lda #bank(HuTrackEngine.FadeTo)
        tam #6
        lda <__al
        ldy <__ah
        jsr HuTrackEngine.FadeTo
        pla
        tam #6
        plp
        rts

_HuTrackEngine_Status:
        lda HuTrack.playbackState
        cly
        HUTRACK_HUC_HUCC_RETURN
        rts

_HuTrackEngine_MusicVolume:
        lda HuTrack.musicAttenuation
        eor #31
        cly
        HUTRACK_HUC_HUCC_RETURN
        rts

_HuTrackEngine_SetSFXVolume.1:
        php
        sei
        tma #6
        pha
        lda #bank(HuTrackEngine.SetSFXVolume)
        tam #6
        lda <__al
        jsr HuTrackEngine.SetSFXVolume
        pla
        tam #6
        plp
        rts

_HuTrackEngine_SFXVolume:
        lda HuTrack.sfxAttenuation
        eor #31
        cly
        HUTRACK_HUC_HUCC_RETURN
        rts

; Latest EE event, including EE00; -1 means no unread event.
_HuTrackEngine_PollEvent:
        php
        sei
        lda HuTrack.externalPending
      beq .empty
        stz HuTrack.externalPending
        lda HuTrack.externalValue
        cly
      bra .return
.empty
        lda #$ff
        tay
.return
        plp
        HUTRACK_HUC_HUCC_RETURN
        rts

; Acquire only a free channel. Never interrupt an existing SFX owner.
_HuTrackEngine_TryReserve.1:
        php
        sei
        ldx <__al
        cpx #6
      bcs .busy
        lda HuTrack.SFX.inProgress,x
      bmi .busy
        jsr _HuTrackEngine_chanReserve.1
        lda #1
      bra .return
.busy
        cla
.return
        cly
        plp
        HUTRACK_HUC_HUCC_RETURN
        rts

; Global stereo attenuation, either packed nibbles or two 8-bit levels.

_HuTrackEngine_SetGlobal.1:
        .ifndef HUCC
        txa                     ; HuC's acc argument is low X / high A.
        .endif
        sta HuTrack.Global.SetVolume
        lda #$80
        sta HuTrack.Global.VolUpdate
  rts

;#pragma fastcall HuTrackEngine_SetGlobal(byte __al, byte __ah);
_HuTrackEngine_SetGlobal.2:
        php
        sei
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
        plp
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
        stz HuSFX.pcm.owned,x
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
        php
        sei
        ldx <__al
        cpx #$06
      bcc .channel.valid
        jmp .error
.channel.valid
        bit HuTrack.SFX.inProgress,x
      bmi .reserved
        jmp .error
.reserved

        ; Validate before replacing an existing stream. Skip the three-byte
        ; header without wrapping the physical bank past $ff.
        lda <__fptr
        clc
        adc #3
        sta <HuTrack.dda.ptr
        lda <__fptr+1
        and #$1f
        adc #0
        tay
        and #$1f
        ora #$40
        sta <HuTrack.dda.ptr+1
        tya
        cmp #$20
        lda <__fbank
        adc #0
      bcc .bank.valid
        jmp .error
.bank.valid
        tay
        phy
        tma #2
        pha
        tya
        tam #2
        lda [HuTrack.dda.ptr]
        tay
        pla
        tam #2
        tya
        ply                     ; Y = normalized sample bank
        cmp #$80
      bcc .sample.ready
        ; A marker at the first byte must stop. If the requested masks make
        ; it repeat, the timer would reread that marker forever in one IRQ.
        ora <__cl
        and <__ch
        and #$7f
      beq .sample.ready
        jmp .error
.sample.ready

        lda #$80
        sta <HuTrack.dda.inactive,x
        sta <HuTrack.dda.bank,x
        tya
        sta <HuTrack.dda.loop.bank,x

        lda <__ch
        ora #$80
        sta <HuTrack.dda.cntr1,x

        lda <__cl
        sta <HuTrack.dda.cntr0,x

        lda <HuTrack.dda.ptr
        sta <HuTrack.dda.addr.lo,x
        sta <HuTrack.dda.addr.loop.lo,x
        lda <HuTrack.dda.ptr+1
        sta <HuTrack.dda.addr.hi,x
        sta <HuTrack.dda.addr.loop.hi,x
        stx $800
        stz $807
        lda #31
        sec
        sbc HuTrack.sfxAttenuation
        ora #$c0
        sta $804
        lda #$10
        sta $806
        lda <HuTrack.dda.loop.bank,x
        sta <HuTrack.dda.bank,x
        stz <HuTrack.dda.inactive,x
        lda HuTrack.DDApaused
      bne .suspended
        rmb7 <HuTrack.DDAprocess
.suspended
          plp

        ; No error
        lda #$01
        cly
        clc
.out
  HUTRACK_HUC_HUCC_RETURN
  rts

.error
        plp
        cly
        cla
        sec
  HUTRACK_HUC_HUCC_RETURN
  rts

;//.........................................................
; int __fastcall HuTrackEnginePauseDDA();
_HuTrackEnginePauseDDA:
        php
        sei
        lda HuTrack.DDApaused
      bne .unchanged
        inc HuTrack.DDApaused
        smb7 <HuTrack.DDAprocess
        lda #1
      bra .return
.unchanged
        cla
.return
        cly
        plp
        HUTRACK_HUC_HUCC_RETURN
        rts

_HuTrackEngineResumeDDA:
        php
        sei
        lda HuTrack.DDApaused
      beq .return
        stz HuTrack.DDApaused
        ; Do not wake the 7 kHz channel scan when no stream is active.
        ldx #5
.scan
        lda <HuTrack.dda.inactive,x
      bpl .enable
        dex
      bpl .scan
        bra .changed
.enable
        rmb7 <HuTrack.DDAprocess
.changed
        lda #1
.return
        cly
        plp
        HUTRACK_HUC_HUCC_RETURN
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

HuTrack.FixedCodeEnd:
  .if (bank(HuTrack.FixedCodeEnd-1)!=bank(HuTrack.FixedCodeStart))
    .fail HuTrack fixed code exceeds its library bank.
  .endif

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
