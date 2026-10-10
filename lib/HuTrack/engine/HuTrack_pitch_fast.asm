; Original twelve-note periods, quarter-square interpolation and vibrato.
; Slides remain integer-period state. Bends precede the slide offset, as in
; the original driver; there is no period-to-note conversion on each tick.
HuTrack.Pitch.period:
        sta HuTrack.M.note
        tma #4
        pha
        lda #bank(HuTrack.Tables)
        tam #4
        stz HuTrack.M.pitch
        lda HuTrack.M.note
        jsr HuTrack.Pitch.interpolate
        pla
        tam #4
        rts

HuTrack.Pitch.setBase:
        sta HuTrack.P.basis,x
        jsr HuTrack.Pitch.period
        lda HuTrack.M.a
        sta HuTrack.P.baseLo,x
        sta HuTrack.P.unbentLo,x
        lda HuTrack.M.a+1
        sta HuTrack.P.baseHi,x
        sta HuTrack.P.unbentHi,x
        rts

; A=note+60, M.pitch low=original 1/256-semitone fraction. Tables mapped.
HuTrack.Pitch.interpolate:
        tay
        lda HuTrack.Pitch.Semitone,y
        sta HuTrack.M.note
        lda HuTrack.Pitch.Octave,y
        sec
        sbc #5
        sta HuTrack.M.octave
        stz HuTrack.M.delta
        lda HuTrack.M.pitch
      beq .wholeNote
        ldy HuTrack.M.note
        lda HuTrack.Pitch.Step,y
        sta HuTrack.process.temp0
        lda HuTrack.M.pitch
        sta HuTrack.process.temp1
        jsr HuTrackEngine.8x8mul
        sta HuTrack.M.delta
.wholeNote
        ldy HuTrack.M.note
        sec
        lda HuTrack.Pitch.BaseLo,y
        sbc HuTrack.M.delta
        sta HuTrack.M.a
        lda HuTrack.Pitch.BaseHi,y
        sbc #0
        sta HuTrack.M.a+1
        lda HuTrack.M.octave
      beq .done
      bmi .lower
.higher
        lsr HuTrack.M.a+1
        ror HuTrack.M.a
        dec HuTrack.M.octave
      bne .higher
.done
        rts
.lower
        asl HuTrack.M.a
        rol HuTrack.M.a+1
      bcs .maximum
        inc HuTrack.M.octave
      bne .lower
        rts
.maximum
        lda #255
        sta HuTrack.M.a
        sta HuTrack.M.a+1
        rts

; Same high-byte quarter-square multiplication as be21559.
HuTrackEngine.8x8mul:
        lda #high(HuTrack.Pitch.SquarePos)
        sta HuTrack.FXptr1+1
        lda #high(HuTrack.Pitch.SquareNeg)
        sta HuTrack.FXptr3+1
        lda HuTrack.process.temp0
        sta HuTrack.FXptr1
        eor #255
        sta HuTrack.FXptr3
        ldy HuTrack.process.temp1
        sec
        lda [HuTrack.FXptr1],y
        sbc [HuTrack.FXptr3],y
        rts

HuTrack.Pitch.frequency:
        lda HuTrack.SFX.inProgress,x
        ora HuTrack.channel.waitNote,x
      beq .owned
        rts
.owned
        bit HuTrack.channel.ddaState,x
      bpl .wsg
        rts
.wsg
        lda HuTrack.channel.noiseMode,x
      beq .period
        lda HuTrack.channel.appliedNoise,x
        jmp HuTrackEngine._htk.WSG.noise
.period
        lda HuTrack.P.dirty,x
        ora HuTrack.P.vibDepth,x
      bne .calculate
        lda HuTrack.channel.applied.period.hi,x
        ldy HuTrack.channel.applied.period.lo,x
        jmp HuTrackEngine._htk.WSG.freq
.calculate
        stz HuTrack.P.dirty,x
        tma #4
        pha
        lda #bank(HuTrack.Tables)
        tam #4
        lda HuTrack.P.vibDepth,x
      bne .bend
        lda HuTrack.channel.detune,x
        cmp #128
      bne .bend
        lda HuTrack.P.baseLo,x
        sta HuTrack.M.p
        lda HuTrack.P.baseHi,x
        sta HuTrack.M.p+1
        stz HuTrack.M.p+2
        stz HuTrack.M.p+3
        jmp .globalCheck
.bend
        jsr HuTrack.Pitch.vibrato
        lda HuTrack.channel.detune,x
        cmp #128
      bcs .fineUp
        ; Preserve the original E5 negative-side approximation (-254 at 00).
        eor #127
        asl a
        sta HuTrack.M.delta
        sec
        lda HuTrack.M.pitch
        sbc HuTrack.M.delta
        sta HuTrack.M.pitch
        lda HuTrack.M.pitch+1
        sbc #0
      bra .fineReady
.fineUp
        asl a
        clc
        adc HuTrack.M.pitch
        sta HuTrack.M.pitch
        lda HuTrack.M.pitch+1
        adc #0
.fineReady
        sta HuTrack.M.pitch+1
      bmi .negative
        clc
        adc HuTrack.P.basis,x
      bcc .interpolate
        lda #255
        stz HuTrack.M.pitch
      bra .interpolate
.negative
        clc
        adc HuTrack.P.basis,x
      bcs .interpolate
        cla
        stz HuTrack.M.pitch
.interpolate
        jsr HuTrack.Pitch.interpolate
        ; bent note + (sliding base - original unbent note), signed 24 bits.
        stz HuTrack.M.p+2
        stz HuTrack.M.p+3
        clc
        lda HuTrack.M.a
        adc HuTrack.P.baseLo,x
        sta HuTrack.M.p
        lda HuTrack.M.a+1
        adc HuTrack.P.baseHi,x
        sta HuTrack.M.p+1
        rol HuTrack.M.p+2
        sec
        lda HuTrack.M.p
        sbc HuTrack.P.unbentLo,x
        sta HuTrack.M.p
        lda HuTrack.M.p+1
        sbc HuTrack.P.unbentHi,x
        sta HuTrack.M.p+1
        lda HuTrack.M.p+2
        sbc #0
        sta HuTrack.M.p+2
      bcs .globalCheck
        stz HuTrack.M.p
        stz HuTrack.M.p+1
        stz HuTrack.M.p+2
.globalCheck
        lda HuTrack.P.globalPitch
        ora HuTrack.P.globalPitch+1
        ora HuTrack.P.globalPitch+2
        ora HuTrack.P.globalPitch+3
      beq .clamp
        ldy #10
.globalScale
        asl HuTrack.M.p
        rol HuTrack.M.p+1
        rol HuTrack.M.p+2
        rol HuTrack.M.p+3
        dey
      bne .globalScale
        ldy #3
.divisor
        lda HuTrack.P.divisor,y
        sta HuTrack.M.b,y
        dey
      bpl .divisor
        jsr HuTrack.Math.divideWide
.clamp
        lda HuTrack.M.p+3
        ora HuTrack.M.p+2
      bne .maximum
        lda HuTrack.M.p+1
        cmp #16
      bcs .maximum
        ora HuTrack.M.p
      bne .output
        inc HuTrack.M.p
      bra .output
.maximum
        lda #255
        sta HuTrack.M.p
        lda #15
        sta HuTrack.M.p+1
.output
        lda HuTrack.M.p
        sta HuTrack.channel.applied.period.lo,x
        lda HuTrack.M.p+1
        sta HuTrack.channel.applied.period.hi,x
        pla
        tam #4
        lda HuTrack.channel.applied.period.hi,x
        ldy HuTrack.channel.applied.period.lo,x
        jmp HuTrackEngine._htk.WSG.freq

; Return signed original fractional-semitone magnitude in M.pitch.
HuTrack.Pitch.vibrato:
        stz HuTrack.M.pitch
        stz HuTrack.M.pitch+1
        lda HuTrack.P.vibDepth,x
      bne .active
        rts
.active
        lda HuTrack.channel.vibrato.idx,x
        and #63
        tay
        lda HuTrack.channel.vibrato.mode,x
      bne .newShape
        lda HuTrack.Pitch.OldSine,y
        sta HuTrack.process.temp0
        tya
        clc
        adc HuTrack.channel.vibrato.inc,x
        and #63
        sta HuTrack.channel.vibrato.idx,x
        and #32
        sta HuTrack.M.sign
      bra .scale
.newShape
        tya
        clc
        adc HuTrack.channel.vibrato.inc,x
        and #63
        sta HuTrack.channel.vibrato.idx,x
        tay
        jsr HuTrack.Pitch.vibratoShape
        asl a
      bcc .shapeReady
        lda #255
.shapeReady
        sta HuTrack.process.temp0
.scale
        ldy HuTrack.P.vibDepth,x
        lda HuTrack.Pitch.Scale,y
        sta HuTrack.process.temp1
        jsr HuTrackEngine.8x8mul
        sta HuTrack.M.pitch
        ldy HuTrack.P.vibFine,x
        cpy #15
      beq .sign
        ; E4 accepts a full byte; it is not an index into the 16-depth table.
        sta HuTrack.M.a
        stz HuTrack.M.a+1
        sty HuTrack.M.b
        stz HuTrack.M.b+1
        jsr HuTrack.Math.multiply8
        lda #15
        sta HuTrack.M.b
        jsr HuTrack.Math.divideByte
        lda HuTrack.M.p
        sta HuTrack.M.pitch
        lda HuTrack.M.p+1
        sta HuTrack.M.pitch+1
.sign
        lda HuTrack.M.sign
      beq .out
        sec
        lda #0
        sbc HuTrack.M.pitch
        sta HuTrack.M.pitch
        lda #0
        sbc HuTrack.M.pitch+1
        sta HuTrack.M.pitch+1
.out
        rts

; Exact floor(driverVolume * envelope / 31), replacing the per-tick division.
HuTrack.Math.volume:
        sta HuTrack.M.delta
        lda HuTrack.P.driverVolume,x
        and #31
        sta HuTrack.M.index
        lsr a
        lsr a
        lsr a
        clc
        adc #high(HuTrack.Pitch.Volume)
        sta HuTrack.FXptr0+1
        lda HuTrack.M.index
        asl a
        asl a
        asl a
        asl a
        asl a
        ora HuTrack.M.delta
        sta HuTrack.FXptr0
        tma #4
        pha
        lda #bank(HuTrack.Tables)
        tam #4
        lda [HuTrack.FXptr0]
        sta HuTrack.M.delta
        pla
        tam #4
        lda HuTrack.M.delta
        rts
