; Period slides follow released-Furnace legacy state semantics.
; Fast note, fine-tune and vibrato numerics retain the original HuTrack model.

; Unsigned 16 * 8 -> 32. Inputs M.a (word), M.b (byte); output M.p.
; Preserves X. Scratch belongs to the music tick, never the DDA interrupt.
HuTrack.Math.multiply8:
        ldy #8
HuTrack.Math.multiplyStart:
        stz HuTrack.M.a+2
        stz HuTrack.M.a+3
        stz HuTrack.M.p
        stz HuTrack.M.p+1
        stz HuTrack.M.p+2
        stz HuTrack.M.p+3

.loop
        lsr HuTrack.M.b+1
        ror HuTrack.M.b
      bcc .shift
        clc
        lda HuTrack.M.p
        adc HuTrack.M.a
        sta HuTrack.M.p
        lda HuTrack.M.p+1
        adc HuTrack.M.a+1
        sta HuTrack.M.p+1
        lda HuTrack.M.p+2
        adc HuTrack.M.a+2
        sta HuTrack.M.p+2
        lda HuTrack.M.p+3
        adc HuTrack.M.a+3
        sta HuTrack.M.p+3
.shift
        asl HuTrack.M.a
        rol HuTrack.M.a+1
        rol HuTrack.M.a+2
        rol HuTrack.M.a+3
        dey
      bne .loop
        rts

; Unsigned 32 / 32 -> 32 quotient in M.p. Divisor M.b must be nonzero.
HuTrack.Math.divideWide:
        stz HuTrack.M.r
        stz HuTrack.M.r+1
        stz HuTrack.M.r+2
        stz HuTrack.M.r+3
        ldy #32
.loop
        asl HuTrack.M.p
        rol HuTrack.M.p+1
        rol HuTrack.M.p+2
        rol HuTrack.M.p+3
        rol HuTrack.M.r
        rol HuTrack.M.r+1
        rol HuTrack.M.r+2
        rol HuTrack.M.r+3
      bcs .subtract
        lda HuTrack.M.r+3
        cmp HuTrack.M.b+3
      bcc .next
      bne .subtract
        lda HuTrack.M.r+2
        cmp HuTrack.M.b+2
      bcc .next
      bne .subtract
        lda HuTrack.M.r+1
        cmp HuTrack.M.b+1
      bcc .next
      bne .subtract
        lda HuTrack.M.r
        cmp HuTrack.M.b
      bcc .next
.subtract
        sec
        lda HuTrack.M.r
        sbc HuTrack.M.b
        sta HuTrack.M.r
        lda HuTrack.M.r+1
        sbc HuTrack.M.b+1
        sta HuTrack.M.r+1
        lda HuTrack.M.r+2
        sbc HuTrack.M.b+2
        sta HuTrack.M.r+2
        lda HuTrack.M.r+3
        sbc HuTrack.M.b+3
        sta HuTrack.M.r+3
        inc HuTrack.M.p
.next
        dey
      bne .loop
        rts

; Divide a 24-bit numerator by the nonzero byte in M.b.
; Keeping the remainder in A avoids the general four-byte division loop.
HuTrack.Math.divideByte:
        cla
        ldy #24
.loop
        asl HuTrack.M.p
        rol HuTrack.M.p+1
        rol HuTrack.M.p+2
        rol a
      bcs .subtract
        cmp HuTrack.M.b
      bcc .next
.subtract
        sbc HuTrack.M.b
        inc HuTrack.M.p
.next
        dey
      bne .loop
        rts

; Combined note -> A=semitone, Y=octave; replaces two redundant lookup tables.
HuTrack.Pitch.decodeNote:
        cly
.octave
        cmp #12
      bcc .out
        sbc #12
        iny
      bra .octave
.out
        rts

HuTrack.Pitch.newNote:
        lda #1
        sta HuTrack.P.dirty,x
        lda HuTrack.P.anchor,x
        jsr HuTrack.Pitch.noiseNote
        lda HuTrack.P.anchor,x
        jsr HuTrack.Pitch.setBase
        stz HuTrack.channel.vibrato.idx,x
        rts

; Legacy PCE noise ignores octave and has its own twelve-entry note map.
HuTrack.Pitch.noiseNote:
        cmp #60
      bcs .note
        lda #60
.note
        sec
        sbc #60
.modulo
        cmp #12
      bcc .store
        sbc #12
      bra .modulo
.store
        tay
        lda NoiseTable,y
        sta HuTrack.channel.appliedNoise,x
        rts

; Return unsigned waveform magnitude in A and its sign in M.sign.
HuTrack.Pitch.vibratoShape:
        stz HuTrack.M.sign
        lda HuTrack.channel.vibrato.mode,x
        cmp #3
      bcc .sine
        cmp #12
      bcs .sine
        cmp #3
      beq .triangle
        cmp #4
      beq .ramp
        cmp #5
      beq .negativeRamp
        cmp #6
      beq .square
        cmp #7
      beq .random
        cmp #8
      beq .squareUp
        cmp #9
      beq .squareDown
        ; E30A/E30B: one half-sine spread across the entire cycle.
        tya
        lsr a
        tay
        lda HuTrack.channel.vibrato.mode,x
        cmp #11
      bne .sine
        tya
        ora #32
        tay
.sine
        lda HuTrack.Pitch.Sine,y
        pha
        lda HuTrack.channel.vibrato.mode,x
        cmp #1
      beq .up
        cmp #2
      beq .down
        pla
      bra .signed
.up
        pla
      bpl .signed
        cla
        rts
.down
        pla
      bmi .signed
        cla
        rts
.signed
        cmp #128
      bcc .out
        inc HuTrack.M.sign
        eor #$ff
        inc a
.out
        rts
.triangle
        tya
        and #32
        sta HuTrack.M.sign
        tya
        and #31
        cmp #16
      bcc .triangleScale
        eor #31
        inc a
.triangleScale
        asl a
        asl a
        asl a
        rts
.negativeRamp
        inc HuTrack.M.sign
.ramp
        tya
        asl a
        rts
.square
        tya
        and #32
        sta HuTrack.M.sign
        lda #127
        rts
.squareDown
        inc HuTrack.M.sign
.squareUp
        tya
        cmp #32
      bcs .zero
        lda #127
        rts
.zero
        cla
        rts
.random
        ; Furnace uses the host C rand(); HuTrack uses a reproducible full-cycle
        ; eight-bit generator. Distribution/range match; random sequences differ.
        lda HuTrack.P.random
        asl a
        asl a
        clc
        adc HuTrack.P.random
        inc a
        sta HuTrack.P.random
        eor #128
        bra .signed

    .include "HuTrack/engine/HuTrack_fx.asm"
    .include "HuTrack/engine/HuTrack_timing.asm"
    .include "HuTrack/engine/HuTrack_pitch_fast.asm"
