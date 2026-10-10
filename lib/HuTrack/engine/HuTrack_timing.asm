; Pre-effects are evaluated even when ED defers the remainder of a row.
HuTrack.FX.preRow:
        stz HuTrack.P.rowDelay,x
        lda HuTrack.channel.update.extFX
        sta HuTrack.P.pendingExt,x
        lda HuTrack.channel.change,x
        sta HuTrack.P.pendingChange,x
        bit #8
      beq .fx2
        lda HuTrack.channel.temp.fxArg1,x
        sta HuTrack.channel.current.fxArg
        lda HuTrack.channel.temp.fx1,x
        jsr HuTrack.FX.preEffect
.fx2
        lda HuTrack.P.pendingExt,x
        bit #1
      beq .fx3
        lda HuTrack.channel.temp.fxArg2,x
        sta HuTrack.channel.current.fxArg
        lda HuTrack.channel.temp.fx2,x
        jsr HuTrack.FX.preEffect
.fx3
        lda HuTrack.P.pendingExt,x
        bit #4
      beq .fx4
        lda HuTrack.channel.temp.fxArg3,x
        sta HuTrack.channel.current.fxArg
        lda HuTrack.channel.temp.fx3,x
        jsr HuTrack.FX.preEffect
.fx4
        lda HuTrack.P.pendingExt,x
        bit #16
      beq .out
        lda HuTrack.channel.temp.fxArg4,x
        sta HuTrack.channel.current.fxArg
        lda HuTrack.channel.temp.fx4,x
        jsr HuTrack.FX.preEffect
.out
        lda HuTrack.P.rowDelay,x
      beq .ready
        sec
        rts
.ready
        clc
        rts

HuTrack.FX.preEffect:
        cmp #$09
      beq .speed1
        cmp #$0f
      beq .speed2
        cmp #$0b
      beq .jump
        cmp #$0d
      beq .break
        cmp #$ed
      beq .delay
        rts
.speed1
        lda HuTrack.channel.current.fxArg
      beq .out
        sta HuTrack.tickReload+1
      bra .speed
.speed2
        lda HuTrack.channel.current.fxArg
      beq .out
        sta HuTrack.tickReload
.speed
        ldy HuTrack.TickIdx
        lda HuTrack.tickReload,y
        sta HuTrack.tick
        rts
.jump
        lda HuTrack.channel.patternBreak
        cmp #$ff
      bne .out
        lda HuTrack.channel.current.fxArg
        sta HuTrack.channel.patternBreak
        stz HuTrack.breakRow
        rts
.break
        ; Released DMF compatibility ignores Dxx in the final order.
        lda HuTrack.channel.pattern.num,x
        inc a
        cmp HuTrack.patternListlen
      bcs .out
        lda HuTrack.channel.current.fxArg
        sta HuTrack.breakRow
        lda #$fe
        sta HuTrack.channel.patternBreak
        rts
.delay
        lda HuTrack.channel.current.fxArg
      beq .out
        cmp HuTrack.P.rowTicks
      bcs .out
        inc a
        sta HuTrack.P.rowDelay,x
.out
        rts

HuTrack.FX.delayedRow:
        lda HuTrack.P.rowDelay,x
      beq .out
        dec HuTrack.P.rowDelay,x
      bne .out
        lda HuTrack.P.pendingChange,x
        sta HuTrack.channel.change,x
        lda HuTrack.P.pendingExt,x
        sta HuTrack.channel.update.extFX
        jsr HuTrackEngine.Channel.update
        jsr HuTrackEngine.Channel.output
.out
        rts

HuTrack.FX.noteCut:
        lda HuTrack.channel.current.fxArg
      beq .out
        cmp HuTrack.P.rowTicks
      bcs .out
        inc a
        sta HuTrack.P.cutTick,x
.out
        rts
HuTrackEngine.channel.DelayAndCut:
        lda HuTrack.P.cutTick,x
      beq .ready
        dec HuTrack.P.cutTick,x
      bne .ready
        stz HuTrack.Enabled,x
        jsr HuTrackEngine._htk.WSG.DDAstop
        lda #0
        jsr HuTrackEngine._htk.WSG.control
        clc
        rts
.ready
        sec
        rts
