; Call with the music bank mapped. Main-thread callers must protect the call
; with PHP / SEI / PLP; the C wrappers do this, preserving the caller's IRQ state.

HuTrackEngine.pause:
        php
        sei
        lda HuTrack.playbackState
        cmp #1
      bne .out
        lda #2
        sta HuTrack.playbackState
        smb6 <HuTrack.Status
        ldx #5
.loop
        bit HuTrack.SFX.inProgress,x
      bmi .next
        lda <HuTrack.dda.inactive,x
        sta HuTrack.pauseDDA,x
        lda #$80
        sta <HuTrack.dda.inactive,x
        stx $800
        stz $804
.next
        dex
      bpl .loop
.out
        plp
        rts

HuTrackEngine.Continue:
        php
        sei
        lda HuTrack.playbackState
        cmp #2
      bne .out
        lda #1
        sta HuTrack.playbackState
        rmb6 <HuTrack.Status
        ldx #5
.loop
        bit HuTrack.SFX.inProgress,x
      bmi .next
        bit HuTrack.channel.waitNote,x
      bmi .next
        lda HuTrack.pauseDDA,x
        sta <HuTrack.dda.inactive,x
      bmi .control
        jsr HuTrackEngine.EnableDDA
.control
        lda HuTrack.channel.write.volume,x
        jsr HuTrackEngine._htk.WSG.control
.next
        dex
      bpl .loop
.out
        plp
        rts

HuTrackEngine.stop:
        php
        sei
        stz HuTrack.playbackState
        stz HuTrack.endPending
        stz HuTrack.fadeInterval
        smb6 <HuTrack.Status
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

HuTrackEngine.EndSong:
        jsr HuTrackEngine.stop
        lda #3
        sta HuTrack.playbackState
        rts

; A = volume level (clamped 0..31), Y = frames per one-volume-unit step.
; Internally store attenuation = 31 - level; final music volume clamps at zero.
; Interval zero applies immediately. A new request replaces the previous fade.
HuTrackEngine.FadeTo:
        stz HuTrack.fadeAction
HuTrackEngine.StartFade:
        cmp #32
      bcc .valid
        lda #31
.valid
        eor #31
        sta HuTrack.fadeTarget
        sty HuTrack.fadeCounter
        sty HuTrack.fadeInterval
        cpy #0
      beq .immediate
        cmp HuTrack.musicAttenuation
      bne .out
.immediate
        sta HuTrack.musicAttenuation
        jmp HuTrackEngine.FadeComplete
.out
        rts

; Y = frames per step. FadeOut stops; FadeToPause holds a resumable position.
HuTrackEngine.FadeOut:
        lda #1
      bra HuTrackEngine.FadeDown
HuTrackEngine.FadeToPause:
        lda #2
HuTrackEngine.FadeDown:
        sta HuTrack.fadeAction
        cla
        jmp HuTrackEngine.StartFade

; Y = frames per step. Resume a paused song at zero gain, then fade to full.
HuTrackEngine.FadeIn:
        phy
        lda #31
        sta HuTrack.musicAttenuation
        jsr HuTrackEngine.Continue
        ply
        lda #31
        jmp HuTrackEngine.FadeTo

HuTrackEngine.FadeTick:
        dec HuTrack.fadeCounter
      bne .out
        lda HuTrack.fadeInterval
        sta HuTrack.fadeCounter
        lda HuTrack.musicAttenuation
        cmp HuTrack.fadeTarget
      beq HuTrackEngine.FadeComplete
      bcs .down
        inc a
      bra .store
.down
        dec a
.store
        sta HuTrack.musicAttenuation
        cmp HuTrack.fadeTarget
      beq HuTrackEngine.FadeComplete
.out
        rts
HuTrackEngine.FadeComplete:
        stz HuTrack.fadeInterval
        lda HuTrack.fadeAction
      beq .out
        cmp #1
      bne .pause
        jmp HuTrackEngine.stop
.pause
        jmp HuTrackEngine.pause
.out
        rts

; PCM requests may start while globally suspended; ResumeDDA enables them later.
HuTrackEngine.EnableDDA:
        lda HuTrack.DDApaused
      bne .out
        rmb7 <HuTrack.DDAprocess
.out
        rts

; A = SFX group level, 31 unchanged / 0 silent. The control-stream player
; subtracts the same attenuation after its per-channel mix on future updates.
; Refresh current PCM and HuSFX channels now, including streams on long waits.
HuTrackEngine.SetSFXVolume:
        php
        sei
        cmp #32
      bcc .valid
        lda #31
.valid
        eor #31
        sta HuTrack.sfxAttenuation
        ldx #5
.loop
        bit HuTrack.SFX.inProgress,x
      bpl .next
        .ifdef HuSFX.pcm.owned
        lda HuSFX.pcm.owned,x
      bne .stream
        .endif
        lda <HuTrack.dda.inactive,x
      bmi .stream
        lda #31
        sec
        sbc HuTrack.sfxAttenuation
        ora #$c0
      bra .write
.stream
        .ifdef HuSFX.stream.bnk
        lda HuSFX.stream.bnk,x
        cmp #$ff
      beq .next
        lda HuSFX.rawControl,x
        HuSFX.MixVolume
        sta HuSFX.control,x
      bra .write
        .else
        bra .next
        .endif
.write
        stx $800
        sta $804
.next
        dex
      bpl .loop
        plp
        rts
