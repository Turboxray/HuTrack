; Shared legacy period-slide state and effects. X is the music channel.
HuTrack.FX.up:
        lda HuTrack.P.lastSlide
        cmp #1
      beq .out
        cmp #3
      beq .out
        lda #1
        sta HuTrack.P.lastSlide
        lda #156                   ; C8, legacy upper slide limit
        sta HuTrack.P.target,x
        jmp HuTrack.FX.ramp
.out
        rts

HuTrack.FX.down:
        lda HuTrack.P.lastSlide
        cmp #2
      beq .out
        cmp #3
      beq .out
        lda #2
        sta HuTrack.P.lastSlide
        lda #60                    ; C0, legacy lower slide limit
        sta HuTrack.P.target,x
        jmp HuTrack.FX.ramp
.out
        rts

HuTrack.FX.ramp:
        lda HuTrack.channel.current.fxArg
        sta HuTrack.P.speed,x
      beq HuTrack.FX.stopSlide
        lda #1
        sta HuTrack.P.mode,x
        jmp HuTrack.FX.prePorta

HuTrack.FX.stopSlide:
        stz HuTrack.P.speed,x
        stz HuTrack.P.mode,x
        stz HuTrack.P.inPorta,x
        rts

HuTrack.FX.portamento:
        lda HuTrack.channel.current.fxArg
      beq HuTrack.FX.stopSlide
        sta HuTrack.P.lastPorta,x
HuTrack.FX.portamentoMemory:
        sta HuTrack.P.speed,x
        lda HuTrack.P.anchor,x
        sta HuTrack.P.target,x
        cmp HuTrack.P.oldNote,x
      bne .move
        lda HuTrack.P.mode,x
        cmp #2
      beq .move
        cmp #3
      beq .move
        stz HuTrack.P.speed,x       ; legacy same-note-after-slide quirk
.move
        lda #2
        sta HuTrack.P.mode,x
        lda #3
        sta HuTrack.P.lastSlide
        lda HuTrack.Enabled,x
      beq .start
        bit HuTrack.SFX.inProgress,x
      bmi .suppress
        bit HuTrack.channel.waitNote,x
      bmi .start
.suppress
        stz HuTrack.P.trigger      ; keep the existing note/envelopes alive
.start
        jmp HuTrack.FX.prePorta

HuTrack.FX.shortUp:
        lda HuTrack.channel.current.fxArg
        and #15
        clc
        adc HuTrack.P.anchor,x
      bcc .target
        lda #255
.target
        sta HuTrack.P.target,x
        jmp HuTrack.FX.shortSlide

HuTrack.FX.shortDown:
        lda HuTrack.channel.current.fxArg
        and #15
        sta HuTrack.M.delta
        sec
        lda HuTrack.P.anchor,x
        sbc HuTrack.M.delta
      bcs .target
        cla
.target
        sta HuTrack.P.target,x
HuTrack.FX.shortSlide:
        lda HuTrack.channel.current.fxArg
        and #$f0
        lsr a
        lsr a
        sta HuTrack.P.speed,x
        lda #3
        sta HuTrack.P.mode,x
        sta HuTrack.P.shortRow
        lda HuTrack.channel.current.fxArg
        and #15
      beq .zero
        lda #3
        sta HuTrack.P.lastSlide
        jmp HuTrack.FX.prePorta
.zero
        stz HuTrack.P.inPorta,x
        stz HuTrack.P.mode,x
        rts

HuTrack.FX.prePorta:
        lda HuTrack.P.inPorta,x
      bne .out
        lda HuTrack.ArpEnv.len,x
      beq .enable
        ; The PCE dispatch resets an active arpeggio to its unmodified note
        ; when first entering a slide. Do not rewind an already sliding note.
        lda HuTrack.channel.change,x
        bit #1
      beq .held
        lda HuTrack.P.oldNote,x
      bra .period
.held
        lda HuTrack.P.anchor,x
.period
        jsr HuTrack.Pitch.setBase
.enable
        lda #1
        sta HuTrack.P.inPorta,x
.out
        rts

HuTrack.Pitch.commitNote:
        lda HuTrack.channel.temp.note,x
        cmp #84
      bcc .note
        jmp HuTrackEngine.Channel.update.Note
.note
        ; A post-SFX note is a fresh hardware start, even with portamento.
        bit HuTrack.SFX.inProgress,x
      bmi .owned
        bit HuTrack.channel.waitNote,x
      bmi .fresh
.owned
        lda HuTrack.Enabled,x
      beq .trigger
        lda HuTrack.P.mode,x
        cmp #2
      beq .target
        cmp #3
      bne .trigger
        lda HuTrack.P.shortRow
      bne .trigger
        jsr HuTrack.FX.stopSlide
      bra .trigger
.target
        lda HuTrack.P.anchor,x
        sta HuTrack.P.target,x
        stz HuTrack.channel.vibrato.idx,x
        rts
.trigger
        lda HuTrack.channel.waitNote,x
      bne .fresh
        lda HuTrack.P.legato,x
      beq .fresh
        jmp HuTrack.Pitch.newNote
.fresh
        jmp HuTrackEngine.Channel.update.Note

HuTrack.Pitch.slide:
        lda HuTrack.P.speed,x
      bne .active
        rts
.active
        lda #1
        sta HuTrack.P.dirty,x
        lda HuTrack.P.target,x
        jsr HuTrack.Pitch.period
        lda HuTrack.P.baseHi,x
        cmp HuTrack.M.a+1
      bcc .increase
      bne .decrease
        lda HuTrack.P.baseLo,x
        cmp HuTrack.M.a
      bcc .increase
.decrease
        sec
        lda HuTrack.P.baseLo,x
        sbc HuTrack.P.speed,x
        sta HuTrack.P.baseLo,x
        lda HuTrack.P.baseHi,x
        sbc #0
        sta HuTrack.P.baseHi,x
      bcc .reached
        cmp HuTrack.M.a+1
      bcc .reached
      bne .out
        lda HuTrack.P.baseLo,x
        cmp HuTrack.M.a
      bcc .reached
      beq .reached
        rts
.increase
        clc
        lda HuTrack.P.baseLo,x
        adc HuTrack.P.speed,x
        sta HuTrack.P.baseLo,x
        lda HuTrack.P.baseHi,x
        adc #0
        sta HuTrack.P.baseHi,x
      bcs .reached
        cmp HuTrack.M.a+1
      bcc .out
      bne .reached
        lda HuTrack.P.baseLo,x
        cmp HuTrack.M.a
      bcc .out
.reached
        lda HuTrack.M.a
        sta HuTrack.P.baseLo,x
        sta HuTrack.P.unbentLo,x
        lda HuTrack.M.a+1
        sta HuTrack.P.baseHi,x
        sta HuTrack.P.unbentHi,x
        lda HuTrack.P.target,x
        sta HuTrack.P.basis,x
        lda HuTrack.P.anchor,x
        sta HuTrack.P.oldNote,x
        lda HuTrack.P.target,x
        sta HuTrack.P.anchor,x
        jsr HuTrack.FX.stopSlide
.out
        rts

HuTrack.FX.vibrato:
        lda HuTrack.channel.current.fxArg
      beq .set
        sta HuTrack.P.lastVib,x
.set
        jmp HuTrack.FX.setVibrato

HuTrack.FX.setVibrato:
        pha
        lda #1
        sta HuTrack.P.dirty,x
        pla
        pha
        and #15
        sta HuTrack.P.vibDepth,x
        pla
        lsr a
        lsr a
        lsr a
        lsr a
        sta HuTrack.channel.vibrato.inc,x
        rts

HuTrack.FX.vibMode:
        lda HuTrack.channel.current.fxArg
        sta HuTrack.channel.vibrato.mode,x
        rts
HuTrack.FX.vibFine:
        lda HuTrack.channel.current.fxArg
        sta HuTrack.P.vibFine,x
        rts
HuTrack.FX.vibratoVolume:
        lda HuTrack.channel.current.fxArg
      beq .set
        lda HuTrack.P.lastVib,x
.set
        jsr HuTrack.FX.setVibrato
        jmp HuTrack.FX.volume
HuTrack.FX.portaVolume:
        lda HuTrack.channel.current.fxArg
      beq .stop
        lda HuTrack.P.lastPorta,x
      beq .stop
        jsr HuTrack.FX.portamentoMemory
        jmp HuTrack.FX.volume
.stop
        jsr HuTrack.FX.stopSlide
        jmp HuTrack.FX.volume

HuTrack.FX.arpeggio:
        lda HuTrack.channel.current.fxArg
        sta HuTrack.P.arp,x
      bne .out

        lda #1
        sta HuTrack.P.dirty,x
        lda HuTrack.P.anchor,x
        jsr HuTrack.Pitch.setBase
.out
        rts
HuTrack.FX.arpSpeed:
        lda HuTrack.channel.current.fxArg
      beq .out
        sta HuTrack.P.arpSpeed
.out
        rts
HuTrack.Pitch.arpeggio:
        lda HuTrack.P.arpYield,x
        stz HuTrack.P.arpYield,x
      bne .out
        lda HuTrack.P.speed,x
      bne .out
        lda HuTrack.P.arp,x
      beq .out
        lda HuTrack.P.arpTicks,x
      beq .step
        dec HuTrack.P.arpTicks,x
      bne .out
.step
        lda #1
        sta HuTrack.P.dirty,x
        lda HuTrack.P.arpSpeed
        sta HuTrack.P.arpTicks,x
        inc HuTrack.P.arpStage,x
        lda HuTrack.P.arpStage,x
        cmp #3
      bcc .stage
        stz HuTrack.P.arpStage,x
        cla
.stage
        cmp #0
      beq .base
        cmp #1
      bne .low.load
        lda HuTrack.P.arp,x
        lsr a
        lsr a
        lsr a
        lsr a
        bra .low
.low.load
        lda HuTrack.P.arp,x
.low
        and #15
.base

        clc
        adc HuTrack.P.anchor,x
      bcc .period
        lda #255
.period
        jsr HuTrack.Pitch.setBase
.out
        rts

; Volume slides are quarter steps per tick, including the first tick.
HuTrack.FX.volume:
        stz HuTrack.channel.volSlideUp,x
        stz HuTrack.channel.volSlideDown,x
        lda HuTrack.channel.current.fxArg
      beq .out
        stz HuTrack.P.tremDepth,x
        stz HuTrack.P.tremAttenuation,x
        and #15
      beq .up
        sta HuTrack.channel.volSlideDown,x
        rts
.up
        lda HuTrack.channel.current.fxArg
        lsr a
        lsr a
        lsr a
        lsr a
        sta HuTrack.channel.volSlideUp,x
.out
        rts

HuTrack.FX.tremolo:
        lda HuTrack.P.tremDepth,x
      bne .set
        stz HuTrack.P.tremPhase,x
.set
        lda HuTrack.channel.current.fxArg
        and #15
        sta HuTrack.P.tremDepth,x
        stz HuTrack.P.tremAttenuation,x
      beq .rate
        stz HuTrack.channel.volSlideUp,x
        stz HuTrack.channel.volSlideDown,x
.rate
        lda HuTrack.channel.current.fxArg
        lsr a
        lsr a
        lsr a
        lsr a
        sta HuTrack.P.tremRate,x
        rts

HuTrack.FX.tremoloTick:
        lda HuTrack.P.tremDepth,x
      bne .active
        rts
.active
        sta HuTrack.M.b
        stz HuTrack.M.b+1
        clc
        lda HuTrack.P.tremPhase,x
        adc HuTrack.P.tremRate,x
        and #127
        sta HuTrack.P.tremPhase,x
        tay
        tma #4
        pha
        lda #bank(HuTrack.Tables)
        tam #4
        lda HuTrack.Pitch.Tremolo,y
        sta HuTrack.M.a
        pla
        tam #4
        stz HuTrack.M.a+1
        jsr HuTrack.Math.multiply8
        lda HuTrack.P.volumeFrac,x
        eor #3
        ror a
        ror a
        ror a
        ora #63
        sec
        sbc HuTrack.P.volumeTail,x
        clc
        adc HuTrack.M.p
        lda HuTrack.M.p+1
        adc #0
        sta HuTrack.P.tremAttenuation,x
        rts

HuTrack.FX.retrigger:
        lda HuTrack.channel.current.fxArg
        sta HuTrack.P.retrigSpeed,x
        stz HuTrack.P.retrigTick,x
        rts
HuTrack.FX.retriggerTick:
        lda HuTrack.P.retrigSpeed,x
      beq .out
        lda HuTrack.P.retrigTick,x
      beq .trigger
        dec HuTrack.P.retrigTick,x
        rts
.trigger
        lda HuTrack.P.retrigSpeed,x
        dec a
        sta HuTrack.P.retrigTick,x
        ; Retrigger macros/sample without changing pitch or reviving a note
        ; interrupted by an SFX. A real pattern note performs that handoff.
        lda HuTrack.channel.waitNote,x
      bne .out
        stz HuTrack.VolEnv.idx,x
        stz HuTrack.WfEnv.idx,x
        stz HuTrack.ArpEnv.idx,x
        stz HuTrack.ArpEnv.finished,x
        bit HuTrack.channel.ddaState,x
      bpl .out
        jmp HuTrackEngine.Channel.setSample
.out
        rts

HuTrack.FX.lfoMode:
        lda HuTrack.channel.current.fxArg
        sta HuTrack.P.lfoMode
        rts
HuTrack.FX.lfoSpeed:
        lda HuTrack.channel.current.fxArg
        eor #$ff
        sta HuTrack.P.lfoSpeed
        rts
HuTrack.FX.lfoApply:
        ; LFO uses both channels 0/1. Either reservation suspends it.
        lda HuTrack.SFX.inProgress
        ora HuTrack.SFX.inProgress+1
        ora HuTrack.channel.waitNote
        ora HuTrack.channel.waitNote+1
      bne .out
        lda HuTrack.P.lfoSpeed
        sta $808
        lda HuTrack.P.lfoMode
        sta $809
.out
        rts

HuTrack.FX.external:
        lda HuTrack.channel.current.fxArg
        sta HuTrack.externalValue
        lda #1
        sta HuTrack.externalPending
        rts

HuTrack.FX.globalFine:
        lda HuTrack.channel.current.fxArg
        sec
        sbc #128
        sta HuTrack.M.delta
        lda #0
      bcs .sign
        lda #$ff
.sign
        sta HuTrack.M.sign
        clc
        lda HuTrack.P.globalPitch
        adc HuTrack.M.delta
        sta HuTrack.P.globalPitch
        lda HuTrack.P.globalPitch+1
        adc HuTrack.M.sign
        sta HuTrack.P.globalPitch+1
        lda HuTrack.P.globalPitch+2
        adc HuTrack.M.sign
        sta HuTrack.P.globalPitch+2
        lda HuTrack.P.globalPitch+3
        adc HuTrack.M.sign
        sta HuTrack.P.globalPitch+3
        ldy #3
.copy
        lda HuTrack.P.globalPitch,y
        sta HuTrack.P.divisor,y
        dey
      bpl .copy
        ldy #6
.shift
        asl HuTrack.P.divisor
        rol HuTrack.P.divisor+1
        rol HuTrack.P.divisor+2
        rol HuTrack.P.divisor+3
        dey
      bne .shift
        lda HuTrack.P.globalPitch+3
      bpl .bias
        sec
        lda HuTrack.P.divisor+0
        sbc HuTrack.P.globalPitch+0
        sta HuTrack.P.divisor+0
        lda HuTrack.P.divisor+1
        sbc HuTrack.P.globalPitch+1
        sta HuTrack.P.divisor+1
        lda HuTrack.P.divisor+2
        sbc HuTrack.P.globalPitch+2
        sta HuTrack.P.divisor+2
        lda HuTrack.P.divisor+3
        sbc HuTrack.P.globalPitch+3
        sta HuTrack.P.divisor+3
        lda #6
      bra .bias.low
.bias
        cla
.bias.low
        clc
        adc HuTrack.P.divisor
        sta HuTrack.P.divisor
        lda HuTrack.P.divisor+1
        adc #4
        sta HuTrack.P.divisor+1
        lda HuTrack.P.divisor+2
        adc #0
        sta HuTrack.P.divisor+2
        lda HuTrack.P.divisor+3
        adc #0
        sta HuTrack.P.divisor+3
      bmi .minimum
        ora HuTrack.P.divisor+2
        ora HuTrack.P.divisor+1
        ora HuTrack.P.divisor
      bne .out
.minimum
        lda #1
        sta HuTrack.P.divisor
        stz HuTrack.P.divisor+1
        stz HuTrack.P.divisor+2
        stz HuTrack.P.divisor+3
.out
        rts

HuTrack.FX.legatoMode:
        lda HuTrack.channel.current.fxArg
        sta HuTrack.P.legato,x
        rts
HuTrack.FX.legatoOld:
        lda HuTrack.channel.current.fxArg
        and #$80
      beq HuTrack.FX.legatoUp
        lda HuTrack.channel.current.fxArg
        and #$7f
        sta HuTrack.channel.current.fxArg
        jmp HuTrack.FX.legatoDown
HuTrack.FX.legatoUp:
        lda HuTrack.channel.current.fxArg
        and #15
        sta HuTrack.P.legatoDelta,x
        jmp HuTrack.FX.legatoDelay
HuTrack.FX.legatoDown:
        lda HuTrack.channel.current.fxArg
        and #15
        eor #$ff
        inc a
        sta HuTrack.P.legatoDelta,x
HuTrack.FX.legatoDelay:
        stz HuTrack.P.legatoTick,x
        lda HuTrack.P.legatoDelta,x
      beq .out
        lda HuTrack.channel.current.fxArg
        lsr a
        lsr a
        lsr a
        lsr a
        inc a
        sta HuTrack.P.legatoTick,x
.out
        rts
HuTrack.FX.legatoTick:
        lda HuTrack.P.legatoTick,x
      beq .out
        dec HuTrack.P.legatoTick,x
      bne .out
        lda HuTrack.P.legatoDelta,x
      bmi .negative
        clc
        adc HuTrack.P.anchor,x
      bcc .note
        lda #255
      bra .note
.negative
        clc
        adc HuTrack.P.anchor,x
      bcs .note
        cla
.note
        sta HuTrack.P.anchor,x
        pha
        lda #1
        sta HuTrack.P.dirty,x
        pla
        pha
        jsr HuTrack.Pitch.noiseNote
        pla
        jsr HuTrack.Pitch.setBase
.out
        rts

HuTrack.FX.sampleBank:
        lda HuTrack.channel.current.fxArg
        sta HuTrack.M.delta
        cla
.bankLoop
        ldy HuTrack.M.delta
      beq .out
        clc
        adc #12
      bcs .previous
        cmp HuTrack.sampleListLen
      bcs .previous
        dec HuTrack.M.delta
      bra .bankLoop
.previous
        sec
        sbc #12
.out
        sta HuTrack.P.sampleBank
        rts
; PCE dispatch volume: completed envelopes hold until the driver volume changes.
HuTrack.FX.applyVolume:
        cmp HuTrack.P.driverVolume,x
      beq .out
        sta HuTrack.P.driverVolume,x
        pha
        jsr HuTrack.FX.volumeMacroActive
        pla
      bcs .out
        sta HuTrack.P.outputVolume,x
.out
        rts
HuTrack.FX.volumeMacroActive:
        bit HuTrack.channel.ddaState,x
      bmi .inactive
        lda HuTrack.VolEnv.len,x
      beq .inactive
        lda HuTrack.VolEnv.idx,x
        cmp HuTrack.VolEnv.len,x
      bcc .active
        lda HuTrack.VolEnv.repeat,x
        cmp #255
      beq .inactive
.active
        sec
        rts
.inactive
        clc
        rts

HuTrack.FX.volumeTick:
        lda HuTrack.channel.volSlideUp,x
        ora HuTrack.channel.volSlideDown,x
      beq .out
        jsr HuTrack.FX.volumeMacroActive
      bcs .step
        lda HuTrack.P.outputVolume,x
        sta HuTrack.channel.directVolume,x
.step
        lda HuTrack.channel.volSlideDown,x
      bne .down
        clc
        lda HuTrack.P.volumeFrac,x
        adc HuTrack.channel.volSlideUp,x
        sta HuTrack.P.volumeFrac,x
        lsr a
        lsr a
        clc
        adc HuTrack.channel.directVolume,x
        cmp #32
      bcc .store
        stz HuTrack.channel.volSlideUp,x
        lda #3
        sta HuTrack.P.volumeFrac,x
        lda #63
        sta HuTrack.P.volumeTail,x
        lda #31
      bra .store
.down
        sec
        lda HuTrack.P.volumeFrac,x
        sbc HuTrack.channel.volSlideDown,x
        sta HuTrack.P.volumeFrac,x
      bcs .out
        ; floor(signed fraction / 4) yields a negative whole-step delta.
        sec
        ror a
        sec
        ror a
        clc
        adc HuTrack.channel.directVolume,x
      bcs .store
        stz HuTrack.channel.volSlideDown,x
        stz HuTrack.P.volumeFrac,x
        stz HuTrack.P.volumeTail,x
        lda HuTrack.P.legacyVolume
      beq .store
        lda #32                    ; legacy underflow sentinel, PSG volume zero
.store
        sta HuTrack.channel.directVolume,x
        jsr HuTrack.FX.applyVolume
        lda HuTrack.P.volumeFrac,x
        and #3
        sta HuTrack.P.volumeFrac,x
.out
        rts

; Older DMFs reset the volume-underflow sentinel on a new instrument/key-on.
HuTrack.FX.restoreLegacyVolume:
        lda HuTrack.channel.directVolume,x
        cmp #32
      bne .out
        lda #3
        sta HuTrack.P.volumeFrac,x
        lda #63
        sta HuTrack.P.volumeTail,x
        lda #31
        sta HuTrack.channel.directVolume,x
        jmp HuTrack.FX.applyVolume
.out
        rts
