
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.Parser:

        ; Swap in alt tick counter, because other tick counter has expired.
        lda HuTrack.TickIdx
        eor #$01
        sta HuTrack.TickIdx
        tax
        lda HuTrack.tickReload,x
        sta HuTrack.tick
        sta HuTrack.P.rowTicks

          ; NOTE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          ; turning interrupts on..
          ; Call the engine once per VBlank; do not re-enter it from another ISR.
          cli

        ;........................
        ; Read in channel data

        clx
        stz HuTrack.current.channel

.debug.pattern

        _htk.MOVE.w HuTrack.pattern.table, <HuTrack.PatterPtr
        _htk.PUSHBANK.4 _htk.PAGE_4000
        _htk.MAP_BANK.4 HuTrack.song.windowBank, _htk.PAGE_4000


.readTracks

        stz HuTrack.channel.update
        stz HuTrack.entryParse.extFX
        stz HuTrack.entryParse
        stz HuTrack.rowIncrement

        ldx HuTrack.current.channel
        lda HuTrack.channel.rowSkip,x
      beq .fetch.row.entry
        dec HuTrack.channel.rowSkip,x
        lda HuTrack.channel.seekRemaining,x
      beq .skip.row.ready
        dec HuTrack.channel.seekRemaining,x
        jmp .readTracks
.skip.row.ready
        stz HuTrack.P.retrigSpeed,x
        jmp .row.position.tracking

.fetch.row.entry

        _htk.DEBUG_NOP

        lda HuTrack.song.format
      beq .legacy.pattern
        jsr HuTrack.Bank.pattern
        jmp .pattern.ready
.legacy.pattern

        lda HuTrack.current.channel
        asl a
        tax
        lda HuTrack.channel.patternList.table,x
        sta <HuTrack.PatternListPtr                     ; channel play list
        lda HuTrack.channel.patternList.table+1,x
        sta <HuTrack.PatternListPtr+1

        _htk.DEBUG_NOP

        ldx HuTrack.current.channel
        ldy HuTrack.channel.pattern.num,x
        lda [HuTrack.PatternListPtr],y                  ; get the current pattern num for this channel

        sta HuTrack.channel.pattern.idx,x
        asl a
        pha

        _htk.DEBUG_NOP

        txa
        asl a
        tay
        lda [HuTrack.PatterPtr],y
        iny
        sta <_hk.A0
        lda [HuTrack.PatterPtr],y
        sta <_hk.A0+1

        _htk.DEBUG_NOP
        ply
        lda [_hk.A0],y
        iny
        sta <HuTrack.currentPattern
        lda [_hk.A0],y
        sta <HuTrack.currentPattern+1

        _htk.DEBUG_NOP

        ldx HuTrack.current.channel

        ; Add the pattern offset
        lda <HuTrack.currentPattern
        clc
        adc HuTrack.channel.patternOffset.lo,x
        sta <HuTrack.currentPattern
        lda <HuTrack.currentPattern+1
        adc HuTrack.channel.patternOffset.hi,x
        sta <HuTrack.currentPattern+1

        _htk.DEBUG_NOP

.pattern.ready
        ; DEBUG this needs to change. It's a default for now
        ; NOTE need a function that clears these variables on new pattern entry



        ;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        jsr HuTrackEngine.ParseEntry
        sty HuTrack.rowIncrement
        lda HuTrack.channel.seekRemaining,x
      bne .advance.pattern.offset
        jsr HuTrack.FX.preRow
      bcs .advance.pattern.offset
        jsr HuTrackEngine.Channel.update
        jsr HuTrackEngine.Channel.output
        ;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        _htk.DEBUG_NOP

.advance.pattern.offset
        ldx HuTrack.current.channel
        ; update offset
        lda HuTrack.channel.patternOffset.lo,x
        clc
        adc HuTrack.rowIncrement
        sta HuTrack.channel.patternOffset.lo,x
        lda HuTrack.channel.patternOffset.hi,x
        adc #$00
        sta HuTrack.channel.patternOffset.hi,x

        _htk.DEBUG_NOP
        lda HuTrack.channel.seekRemaining,x
      beq .row.position.tracking
        dec HuTrack.channel.seekRemaining,x
        jmp .readTracks

.row.position.tracking
        inc HuTrack.channel.rowPos,x
        inc HuTrack.current.channel
        lda HuTrack.current.channel
        cmp #6
      bcs .check.patternBreak
        jmp .readTracks

.check.patternBreak
        ; Resolve flow once, after every channel has consumed the row.
        lda HuTrack.channel.patternBreak
        cmp #$fe
      beq .pattern.break
        cmp #$ff
      bne .pattern_jmp_fx_0B
        lda HuTrack.channel.rowPos
        cmp HuTrack.rowLen
      bne .parser.return
        stz HuTrack.breakRow
.pattern.break
        lda HuTrack.channel.pattern.num
        inc a
        cmp HuTrack.patternListlen
      bcc .transition
        lda force_no_repeat
      beq .wrap.order
        inc HuTrack.endPending
.wrap.order
        cla
      bra .transition
.pattern_jmp_fx_0B
        cmp HuTrack.patternListlen
      bcc .transition
        cla
.transition
        pha
        lda HuTrack.rowLen
      beq .valid.row              ; zero in the header represents 256 rows
        cmp HuTrack.breakRow
      bcc .reset.row
      bne .valid.row
.reset.row
        stz HuTrack.breakRow
.valid.row
        pla
        ldx #5
.transition.loop
        sta HuTrack.channel.pattern.num,x
        stz HuTrack.channel.patternOffset.lo,x
        stz HuTrack.channel.patternOffset.hi,x
        stz HuTrack.channel.rowSkip,x
        pha
        lda HuTrack.breakRow
        sta HuTrack.channel.rowPos,x
        sta HuTrack.channel.seekRemaining,x
        pla
        dex
      bpl .transition.loop
        lda #$ff
        sta HuTrack.channel.patternBreak
.parser.return
        _htk.PULLBANK.4 _htk.PAGE_4000
  rts

;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#




;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#




;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Parse entry for channel                                                                                 /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;

; Parse the current channel row and decompressed values into proper entries.
HuTrackEngine.ParseEntry:

        stz HuTrack.channel.update.extFX
        cly
        stz HuTrack.channel.temp.fxArg1,x

.parseChannel
        lda [HuTrack.currentPattern],y
        iny
        cmp #$80
      bcs .check.noteCombo
        jmp .decode.mask

.check.noteCombo
        cmp #225
      bcs .check.skipEntry
        cmp #212
      bcc .note.octave
        cmp #224
      beq .note.cut
.unsupported
      jmp .decode.out
.note.cut
      bra .set.note

.note.octave
        sec
        sbc #128
.set.note
        sta HuTrack.channel.temp.note,x
        lda #$01
        tsb HuTrack.channel.update
      jmp .decode.out

.check.skipEntry
        cmp #$ff
      bcs .do.reserved
        sec
        sbc #225
        sta HuTrack.channel.rowSkip,x
      jmp .decode.out
.sfx.rowskip

      jmp .decode.out

.do.reserved
      jmp .decode.out

.decode.mask
        sta HuTrack.entryParse

.decode.note
        lda HuTrack.entryParse
        bit #$01
      beq .skip.note
        lda [HuTrack.currentPattern],y
        sta HuTrack.channel.temp.note,x
        iny
        lda #$01
        tsb HuTrack.channel.update
.skip.note

.decode.instr
        lda HuTrack.entryParse
        bit #$04
      beq .skip.instr
        lda [HuTrack.currentPattern],y
        sta HuTrack.channel.temp.instr,x
        iny
        lda #$20
        tsb HuTrack.channel.update
.skip.instr

.decode.volume
        lda HuTrack.entryParse
        bit #$08
      beq .skip.volume
        lda [HuTrack.currentPattern],y
        sta HuTrack.channel.temp.volume,x
        iny
        lda #$04
        tsb HuTrack.channel.update
.skip.volume

.decode.fx1
        lda HuTrack.entryParse
        bit #$10
      beq .decode.fx1.arg
        lda [HuTrack.currentPattern],y
        sta HuTrack.channel.temp.fx1,x
        iny
        lda #($08 | $10)                   ;// TXray - 5/19/2024: If FX, then arg forced to 00. Update both.
        tsb HuTrack.channel.update
.skip.fx1

.decode.fx1.arg
        lda HuTrack.entryParse
        bit #$20
      beq .skip.fx1.arg
        lda [HuTrack.currentPattern],y
        sta HuTrack.channel.temp.fxArg1,x
        iny
        lda #$10
        tsb HuTrack.channel.update
.skip.fx1.arg

.decode.fx234
        lda HuTrack.entryParse
        bit #$40
      beq .skip.fx234
        lda [HuTrack.currentPattern],y
        sta HuTrack.entryParse.extFX
        iny

        jsr HuTrackEngine.parse.extFX

        lda #$40
        tsb HuTrack.channel.update
.skip.fx234

.decode.out

        lda HuTrack.channel.update
        sta HuTrack.channel.change,x

  rts


;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
HuTrackEngine.parse.extFX
        stz HuTrack.channel.update.extFX
        stz HuTrack.channel.temp.fxArg2,x
        stz HuTrack.channel.temp.fxArg3,x
        stz HuTrack.channel.temp.fxArg4,x

.do.fx2
        bit #$01
      beq .do.fxarg2
        lda [HuTrack.currentPattern],y
        sta HuTrack.channel.temp.fx2,x
        iny
        lda #$01
        tsb HuTrack.channel.update.extFX
.do.fxarg2
        lda HuTrack.entryParse.extFX
        bit #$02
      beq .do.fx3
        lda [HuTrack.currentPattern],y
        sta HuTrack.channel.temp.fxArg2,x
        iny

.do.fx3
        lda HuTrack.entryParse.extFX
        bit #$04
      beq .do.fxarg3
        lda [HuTrack.currentPattern],y
        sta HuTrack.channel.temp.fx3,x
        iny
        lda #$04
        tsb HuTrack.channel.update.extFX
.do.fxarg3
        lda HuTrack.entryParse.extFX
        bit #$08
      beq .do.fx4
        lda [HuTrack.currentPattern],y
        sta HuTrack.channel.temp.fxArg3,x
        iny

.do.fx4
        lda HuTrack.entryParse.extFX
        bit #$10
      beq .do.fxarg4
        lda [HuTrack.currentPattern],y
        sta HuTrack.channel.temp.fx4,x
        iny
        lda #$10
        tsb HuTrack.channel.update.extFX
.do.fxarg4
        lda HuTrack.entryParse.extFX
        bit #$20
      beq .out
        lda [HuTrack.currentPattern],y
        sta HuTrack.channel.temp.fxArg4,x
        iny

.out
  rts


;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
HuTrackEngine.Channel.update:
        ; ED postpones the whole row, including clearing the previous 0C.
        ; Compressed empty rows clear it separately when their row begins.
        stz HuTrack.P.retrigSpeed,x
        stz HuTrack.P.lastSlide
        stz HuTrack.P.trigger
        stz HuTrack.P.shortRow
        stz HuTrack.channel.output,x


        lda HuTrack.channel.change,x
      beq .out


.note
        lda HuTrack.channel.change,x
        bit #$01
      beq .instrument
        lda HuTrack.P.arp,x
        sta HuTrack.P.arpYield,x
        lda #1
        sta HuTrack.P.trigger
        lda HuTrack.channel.temp.note,x
        cmp #84
      bcs .instrument
        lda HuTrack.P.anchor,x
        sta HuTrack.P.oldNote,x
        lda HuTrack.channel.temp.note,x
        clc
        adc #60
        sta HuTrack.P.anchor,x



.instrument
        lda HuTrack.channel.change,x
        bit #$20
      beq .volume
        jsr HuTrackEngine.Channel.update.Instrument

.volume
        lda HuTrack.channel.change,x
        bit #$04
      beq .fx
        jsr HuTrackEngine.Channel.update.Volume


.fx
        lda HuTrack.channel.change,x
        bit #$08
      beq .fx234
        jsr HuTrackEngine.Channel.update.FX


.fx234
        lda HuTrack.channel.change,x
        bit #$40
      beq .commit.note
        jsr HuTrackEngine.Channel.update.FX234

.commit.note
        lda HuTrack.P.trigger
      beq .out
        jsr HuTrack.Pitch.commitNote
.out
  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


;...........................................................
HuTrackEngine.Channel.update.Note

        stz HuTrack.VolEnv.idx,x

        lda #$ff
        sta HuTrack.channel.pcmIndex,x

        lda HuTrack.channel.temp.note,x
        cmp #84
      bcc .do.note_octave
        cmp #224
      beq .cut
        ; else error
        jmp .out
.cut
        stz HuTrack.Enabled,x
        stz HuTrack.P.cutTick,x
        stz HuTrack.channel.volSlideDown,x
        stz HuTrack.channel.volSlideUp,x
        bit HuTrack.channel.ddaState,x
      bpl .note.cut
.sample.cut
        lda #$80
        jsr HuTrackEngine._htk.WSG.DDAstop
      bra .out

.note.cut

        stz HuTrack.Enabled,x
        lda #0
        jsr HuTrackEngine._htk.WSG.control
      bra .out

.do.note_octave
        pha
        lda HuTrack.Enabled,x
      bne .already.on
        jsr HuTrack.FX.restoreLegacyVolume
.already.on
        lda #1
        sta HuTrack.Enabled,x
        jsr HuTrack.Pitch.newNote
        pla
        ; Only an actual note after release may hand the hardware back to music.
        ; Notes parsed while SFX owns it still advance the song's logical state.
        pha
        bit HuTrack.SFX.inProgress,x
      bmi .note.owned
        bit HuTrack.channel.waitNote,x
      bpl .note.owned
        stz HuTrack.channel.waitNote,x
        lda #$ff
        sta HuTrack.channel.uploadedWaveform,x
        lda HuTrack.channel.panState,x
        jsr HuTrackEngine._htk.WSG.pan
        lda HuTrack.channel.noiseMode,x
      beq .note.restore.noise
        lda HuTrack.channel.appliedNoise,x
        ora #$80
.note.restore.noise
        jsr HuTrackEngine._htk.WSG.noise
.note.owned
        pla
        sta HuTrack.channel.note,x

        bit HuTrack.channel.ddaState,x
      bpl .decode.note

        jsr HuTrack.Pitch.decodeNote
        clc
        adc HuTrack.P.sampleBank
        sta HuTrack.channel.pcmIndex,x
            lda HuTrack.channel.output,x
            ora #$04
            sta HuTrack.channel.output,x
      jmp .return

.decode.note
        jsr HuTrack.Pitch.decodeNote
        sta HuTrack.channel.note,x

        tya
        sta HuTrack.channel.octave,x


.out
            stz HuTrack.WfEnv.idx,x
            stz HuTrack.VolEnv.idx,x
            stz HuTrack.ArpEnv.idx,x
        stz HuTrack.ArpEnv.finished,x
            lda HuTrack.channel.output,x
            ora #$01
            sta HuTrack.channel.output,x
.return
  rts


;...........................................................
HuTrackEngine.Channel.update.Volume
        lda HuTrack.channel.temp.volume,x
        cmp HuTrack.channel.directVolume,x
      beq .keep.fraction
        stz HuTrack.P.volumeFrac,x
        stz HuTrack.P.volumeTail,x
.keep.fraction
        sta HuTrack.channel.directVolume,x
        jsr HuTrack.FX.applyVolume
        lda HuTrack.channel.change,x
        eor #4
        sta HuTrack.channel.change,x
        rts


HuTrackEngine.Channel.update.FX:
        lda HuTrack.channel.change,x
        eor #($08 | $10)
        sta HuTrack.channel.change,x

        lda HuTrack.channel.temp.fxArg1,x

        sta HuTrack.channel.current.fxArg

        lda HuTrack.channel.temp.fx1,x


        jsr HuTrack.channel.FX.handler
.out
  rts


;...........................................................
HuTrackEngine.Channel.update.FX234

        lda HuTrack.channel.change,x
        eor #$40
        sta HuTrack.channel.change,x

        lda HuTrack.channel.update.extFX
        bit #$01
      beq .fx3
        lda HuTrack.channel.temp.fxArg2,x

        sta HuTrack.channel.current.fxArg

        lda HuTrack.channel.temp.fx2,x


        jsr HuTrack.channel.FX.handler


.fx3
        lda HuTrack.channel.update.extFX
        bit #$04
      beq .fx4
        lda HuTrack.channel.temp.fxArg3,x

        sta HuTrack.channel.current.fxArg

        lda HuTrack.channel.temp.fx3,x


        jsr HuTrack.channel.FX.handler


.fx4
        lda HuTrack.channel.update.extFX
        bit #$10
      beq .out
        lda HuTrack.channel.temp.fxArg4,x

        sta HuTrack.channel.current.fxArg

        lda HuTrack.channel.temp.fx4,x


        jsr HuTrack.channel.FX.handler


.out
          stz HuTrack.channel.update.extFX
  rts

;...........................................................
HuTrackEngine.Channel.update.Instrument
        lda HuTrack.channel.change,x
        eor #$20
        sta HuTrack.channel.change,x

        lda HuTrack.channel.temp.instr,x
        cmp HuTrack.channel.instr,x
      beq .out
        sta HuTrack.channel.instr,x
        jsr HuTrack.FX.restoreLegacyVolume
        lda HuTrack.channel.output,x
        ora #$20
        sta HuTrack.channel.output,x

.out
  rts




;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#




;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Handle Channel FX                                                                                       /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;

HuTrack.channel.FX.handler:

;............................
;............................
; Handle the basic FX
.fx
        cmp #$10
      bcs .platformFX
        asl a
          phx
        tax
        jmp [.fx.table,x]


;............................
;............................
; PCE platform specific FX
.platformFX

;............................
.setWave.fx
        cmp #$10
      bne .noise.fx
        lda #$00
        bra .do.platFX

;............................
.noise.fx
        cmp #$11
      bne .LFOmode.fx
        lda #$02
        bra .do.platFX

;............................
.LFOmode.fx
        cmp #$12
      bne .LFOspeed.fx
        lda #$04
        bra .do.platFX

;............................
.LFOspeed.fx
        cmp #$13
      bne .samplePCM.fx
        lda #$06
        bra .do.platFX

;............................
.samplePCM.fx
        cmp #$17
      bne .overload.fx
        lda #$08
        bra .do.platFX

;............................
.overload.fx
        cmp #$18
      bne .corruption.fx
        lda #$0A
        bra .do.platFX

;............................
.corruption.fx
        cmp #$19
      bne .hardsync.fx
        lda #$0C
        bra .do.platFX

;............................
.hardsync.fx
        cmp #$20
      bne .extFX
        lda #$0E
        bra .do.platFX


;............................
.do.platFX
          phx
        tax
        jmp [.platformFX.table,x]

;............................
;............................
; All the extended FX
.extFX
        tay
        and #$F0
        cmp #$E0
      bne .out
        tya
        and #$0f
        asl a
          phx
        tax
        jmp [.extFX.table,x]


.out
  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

.fx.table
   ; regular FX
  .dw .FX.Arp, .FX.PortaUp, .FX.PortaDown, .FX.PortaNote
  .dw .FX.vibrato, .FX.PortaNote_volSlide, .FX.vibrato_volSlide, .FX.tremolo
  .dw .FX.pan, .FX.setSpeed1, .FX.volSlide, .FX.jump
  .dw .FX.retrig, .FX.break, .FX.extended, .FX.SetSpeed2

.extFX.table
  ; extended FX
  .dw .extFX.ArpSpeed, .extFX.NoteSlideUp, .extFX.NoteSlideDown, .extFX.VibratoMode
  .dw .extFX.VibratoDepth, .extFX.FineTune, .extFX.E6, .extFX.E7
  .dw .extFX.E8, .extFX.E9, .extFX.EA, .extFX.EB
  .dw .extFX.NoteCut, .extFX.NoteDelay, .extFX.Sync, .extFX.GlobFineTune

.platformFX.table
  ; platform FX
  .dw .platFX.setWave, .platFX.Noise, .platFX.LFOmode, .platFX.LFOspeed
  .dw .platFX.SamplePCM, .platFX.overload, .platFX.corruption, .platFX.hardsync

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


;...........................................................
;...........................................................
; 00xx
.FX.Arp
        plx
        jmp HuTrack.FX.arpeggio

;...........................................................
;...........................................................
; 01xx
.FX.PortaUp
        plx
        jmp HuTrack.FX.up

;...........................................................
;...........................................................
; 02xx
.FX.PortaDown
        plx
        jmp HuTrack.FX.down

;...........................................................
;...........................................................
; 03xx
.FX.PortaNote
        plx
        jmp HuTrack.FX.portamento

;...........................................................
;...........................................................
; 04xx
.FX.vibrato
        plx
        jmp HuTrack.FX.vibrato

;...........................................................
;...........................................................
; 05xx
.FX.PortaNote_volSlide
        plx
        jmp HuTrack.FX.vibratoVolume

;...........................................................
;...........................................................
; 06xx
.FX.vibrato_volSlide
        plx
        jmp HuTrack.FX.portaVolume

;...........................................................
;...........................................................
; 07xx
.FX.tremolo
        plx
        jmp HuTrack.FX.tremolo

;...........................................................
;...........................................................
; 08xx
.FX.pan
          plx
        lda HuTrack.channel.current.fxArg
        sta HuTrack.channel.panState,x
        jsr HuTrackEngine._htk.WSG.pan

.FX.pan.out

  rts

;...........................................................
;...........................................................
; 09xx
.FX.setSpeed1
        plx
        rts                     ; handled by preRow

;...........................................................
;...........................................................
; 0Axx
.FX.volSlide
        plx
        jmp HuTrack.FX.volume

;...........................................................
;...........................................................
; 0Bxx
.FX.jump
        plx
        rts                     ; handled by preRow

;...........................................................
;...........................................................
; 0Cxx
.FX.retrig
        plx
        jmp HuTrack.FX.retrigger

;...........................................................
;...........................................................
; 0Dxx
.FX.break
        plx
        rts                     ; handled by preRow

;...........................................................
;...........................................................
; 0Exx
.FX.extended
          plx
  ; This is a null entry because this case scenario is already handled.
  rts

;...........................................................
;...........................................................
; 0Fxx
.FX.SetSpeed2
        plx
        rts                     ; handled by preRow

;...........................................................
;...........................................................
; E0xx
.extFX.ArpSpeed
        plx
        jmp HuTrack.FX.arpSpeed

;...........................................................
;...........................................................
; E1xy
;
;   x = speed
;   y = number of semitones
.extFX.NoteSlideUp
        plx
        jmp HuTrack.FX.shortUp

;...........................................................
;...........................................................
; E2xx
.extFX.NoteSlideDown
        plx
        jmp HuTrack.FX.shortDown

;...........................................................
;...........................................................
; E3xx - vibrato mode (0, 1, 2)
.extFX.VibratoMode
        plx
        jmp HuTrack.FX.vibMode

;...........................................................
;...........................................................
; E4xx - vibrato fine depth
.extFX.VibratoDepth
        plx
        jmp HuTrack.FX.vibFine

;...........................................................
;...........................................................
; E5xx
.extFX.FineTune
          plx
        lda #1
        sta HuTrack.P.dirty,x

        lda HuTrack.channel.current.fxArg
        sta HuTrack.channel.detune,x

        lda HuTrack.channel.output,x
        ora #$01
        sta HuTrack.channel.output,x

.extFX.FineTune.out

  rts

;...........................................................
;...........................................................
; E6xx
.extFX.E6
        plx
        jmp HuTrack.FX.legatoOld

;...........................................................
;...........................................................
; E7xx
.extFX.E7
          plx
          ;null
  rts

;...........................................................
;...........................................................
; E8xx
.extFX.E8
        plx
        jmp HuTrack.FX.legatoUp

;...........................................................
;...........................................................
; E9xx
.extFX.E9
        plx
        jmp HuTrack.FX.legatoDown

;...........................................................
;...........................................................
; EAxx
.extFX.EA
        plx
        jmp HuTrack.FX.legatoMode

;...........................................................
;...........................................................
; EBxx
.extFX.EB
        plx
        jmp HuTrack.FX.sampleBank

;...........................................................
;...........................................................
; ECxx
.extFX.NoteCut
        plx
        jmp HuTrack.FX.noteCut

;...........................................................
;...........................................................
; EDxx
.extFX.NoteDelay
        plx
        rts                     ; handled by preRow

;...........................................................
;...........................................................
; EExx
.extFX.Sync
        plx
        jmp HuTrack.FX.external

;...........................................................
;...........................................................
; EFxx
.extFX.GlobFineTune
        plx
        jmp HuTrack.FX.globalFine

;...........................................................
;...........................................................
; 10xx
.platFX.setWave
          plx
        lda #1
        sta HuTrack.P.dirty,x
.direct.waveform.change
        lda HuTrack.channel.current.fxArg
        sta HuTrack.channel.directWaveform,x

        lda HuTrack.WfEnv.len,x
      beq .platFX.setWave.out

        lda HuTrack.WfEnv.idx,x
        cmp HuTrack.WfEnv.len,x
      bcc .platFX.setWave.out
        lda HuTrack.WfEnv.repeat,x
        cmp #$ff
      bne .platFX.setWave.out
        lda HuTrack.channel.current.fxArg
        sta HuTrack.channel.lastEnvWaveform,x

.platFX.setWave.out

  rts

;...........................................................
;...........................................................
; 11xx
.platFX.Noise
          plx
        cpx #4
      bcs .noise.channel
        rts
.noise.channel
        lda #1
        sta HuTrack.P.dirty,x
        lda HuTrack.channel.current.fxArg

      beq .turnoff.noise
.turnon.noise
        ldy HuTrack.channel.note,x
        lda NoiseTable,y
        jsr HuTrackEngine._htk.WSG.noise

        sta HuTrack.channel.appliedNoise,x
        lda #$80
        sta HuTrack.channel.noiseMode,x
        lda HuTrack.channel.proccessState,x
        and #$1f
        ora #$80
        jsr HuTrackEngine._htk.WSG.control
        stz HuTrack.channel.ddaState,x
        ; Both noise channels can also stream PCM. Stop that stream when
        ; switching to noise, so the timer cannot keep writing to its PSG port.
        lda #$80
        jsr HuTrackEngine._htk.WSG.DDAstop

      jmp .platFX.Noise.out

.turnoff.noise
        lda #$00
        jsr HuTrackEngine._htk.WSG.noise
        stz HuTrack.channel.noiseMode,x
        ; Restore the selected waveform/DDA mode when noise is disabled.

        ; This check is needed because a previous FX might have turned on DDA playback
        lda HuTrack.channel.ddaState,x
      bne .setToDDA
        lda HuTrack.channel.proccessState,x
        jsr HuTrackEngine._htk.WSG.control
        bra .platFX.Noise.out

.setToDDA
        lda #$DF
        jsr HuTrackEngine._htk.WSG.control

.platFX.Noise.out

  rts

;...........................................................
;...........................................................
; 12xx
.platFX.LFOmode
        plx
        jmp HuTrack.FX.lfoMode

;...........................................................
;...........................................................
; 13xx
.platFX.LFOspeed
        plx
        jmp HuTrack.FX.lfoSpeed

;...........................................................
; 17xx
.platFX.SamplePCM
          plx

        lda HuTrack.channel.current.fxArg

        cmp #$00    ; redundant
      bne .dda.mode
.dda.off
        sta HuTrack.channel.ddaState,x
        lda #$80
        jsr HuTrackEngine._htk.WSG.DDAstop

        stz HuTrack.Enabled,x
        jmp .platFX.SamplePCM.out
.dda.mode
        ora #$80
        sta HuTrack.channel.ddaState,x
        lda #$df
        jsr HuTrackEngine._htk.WSG.control

        stz HuTrack.channel.noiseMode,x
        lda #$00
        jsr HuTrackEngine._htk.WSG.noise

        lda #$ff
        sta HuTrack.channel.pcmIndex,x

        stz HuTrack.Enabled,x


.no.note
.platFX.SamplePCM.out

  rts


;...........................................................
;...........................................................
; 18xy overload. X = speed, Y == amount. X = 0, effect is paused. Y = 0, internal accumulator is reset to 0.
; Reserved old experiments; these were never active playback effects.
.platFX.overload
.platFX.corruption
.platFX.hardsync
        plx
        rts


HuTrackEngine.Channel.output:

        lda HuTrack.channel.output,x
      beq .out

        bit #$01
      beq .instr
.note
        lda HuTrack.channel.instr,x
        cmp #$ff
      bne .instr
        stz HuTrack.channel.instr,x
        jsr HuTrackEngine.Channel.instrument

.instr
        lda HuTrack.channel.output,x
        bit #$20
      beq .dda
        jsr HuTrackEngine.Channel.instrument

.dda
        lda HuTrack.channel.output,x
        bit #$04
      beq .out
        jsr HuTrackEngine.Channel.setSample
.out

  rts




;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Reload new instrument                                                                                   /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
HuTrackEngine.Channel.instrument

        lda HuTrack.song.format
      beq .channel
        jmp HuTrack.Bank.instrument
        ; bit HuTrack.SFX.inProgress,x
.channel
        _htk.MOVE.w HuTrack.instr.table, <HuTrack.A0

        lda HuTrack.channel.instr,x
        asl a
        clc
        adc <HuTrack.A0
        sta <HuTrack.A0
        cla
        adc <HuTrack.A0+1
        sta <HuTrack.A0+1

        _htk.MOVE.w [HuTrack.A0], <HuTrack.A1

        cly

        ; Volume envelope
        lda [HuTrack.A1],y
        sta <HuTrack.A0
        iny
        lda [HuTrack.A1],y
        sta <HuTrack.A0+1
        iny
        lda [HuTrack.A0]
        sta HuTrack.VolEnv.len,x
        stz HuTrack.VolEnv.idx,x
        _htk.INC.w HuTrack.A0
        lda [HuTrack.A0]
        sta HuTrack.VolEnv.repeat,x
        _htk.INC.w HuTrack.A0
        lda <HuTrack.A0
        sta HuTrack.VolEnvPtr.lo,x
        lda <HuTrack.A0 + 1
        sta HuTrack.VolEnvPtr.hi,x

        ; arp envelope
        lda [HuTrack.A1],y
        sta <HuTrack.A0
        iny
        lda [HuTrack.A1],y
        sta <HuTrack.A0+1
        iny
        lda [HuTrack.A0]
        sta HuTrack.ArpEnv.mode,x
        _htk.INC.w HuTrack.A0
        lda [HuTrack.A0]
        sta HuTrack.ArpEnv.len,x
        _htk.INC.w HuTrack.A0
        stz HuTrack.ArpEnv.idx,x
        stz HuTrack.ArpEnv.finished,x
        lda [HuTrack.A0]
        sta HuTrack.ArpEnv.repeat,x
        _htk.INC.w HuTrack.A0
        lda <HuTrack.A0
        sta HuTrack.ArpEnvPtr.lo,x
        lda <HuTrack.A0 + 1
        sta HuTrack.ArpEnvPtr.hi,x


        ; waveform envelope
        lda [HuTrack.A1],y
        sta <HuTrack.A0
        iny
        lda [HuTrack.A1],y
        sta <HuTrack.A0+1
        lda [HuTrack.A0]
        sta HuTrack.WfEnv.len,x
        stz HuTrack.WfEnv.idx,x
        _htk.INC.w HuTrack.A0
        lda [HuTrack.A0]
        sta HuTrack.WfEnv.repeat,x
        _htk.INC.w HuTrack.A0
        lda <HuTrack.A0
        sta HuTrack.WfEnvPtr.lo,x
        lda <HuTrack.A0 + 1
        sta HuTrack.WfEnvPtr.hi,x



.use.override

.out

  rts


;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Output Sample/PCM                                                                                       /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
HuTrackEngine.Channel.setSample

.sample.ptr.bank.offset = HuTrack.process.temp0

.temp.addr.lo  = HuTrack.process.temp0
.temp.addr.hi  = HuTrack.process.temp1
.temp.addr.bnk = HuTrack.process.temp2

        lda HuTrack.channel.pcmIndex,x
        cmp HuTrack.sampleListLen
      bcc .sample.valid
        lda #$80
        jmp HuTrackEngine._htk.WSG.DDAstop
.sample.valid
        _htk.PUSHBANK.2 _htk.PAGE_4000

.channel
        _htk.MAP_BANK.2 HuTrack.samples.table.bank, _htk.PAGE_4000
        _htk.MOVE.w HuTrack.samples.table, <HuTrack.A0     ; Note: I think this should probably be an LEA
.cont

    lda <HuTrack.A0 + 1
    and #$1F
    ora #$40
    sta <HuTrack.A0 + 1

    ; Get the sample bank for the DDA routine
    _htk.MOVE.w [HuTrack.A0], .sample.ptr.bank.offset
    _htk.ADD.w #$02, <HuTrack.A0
    _htk.MOVE.w <HuTrack.A0, <HuTrack.A1
    _htk.ADD.w .sample.ptr.bank.offset, <HuTrack.A1
    ldy HuTrack.channel.pcmIndex,x
    lda [HuTrack.A1],y
    sta .temp.addr.bnk

    ; Get the sample pointer for the DDA routine
    tya
    asl a
    tay
    lda [HuTrack.A0],y
    clc
    adc #$02                  ; move past the 'size' .dw value
    sta .temp.addr.lo
    iny
    lda [HuTrack.A0],y
    and #$1f
    ora #$40
    adc #$00
    cmp #$60
  bcc .skip
    inc .temp.addr.bnk
    and #$1F
    ora #$40
.skip
    sta .temp.addr.hi

    jsr HuTrackEngine.EnableDDA

    bit HuTrack.SFX.inProgress,x
  bmi .skip.pcm
    bit HuTrack.channel.waitNote,x
  bmi .skip.pcm

      sei
    stz <HuTrack.dda.cntr0,x
    lda #$8f
    sta <HuTrack.dda.cntr1,x
    lda .temp.addr.lo
    sta <HuTrack.dda.addr.lo,x
    sta <HuTrack.dda.addr.loop.lo,x
    lda .temp.addr.hi
    sta <HuTrack.dda.addr.hi,x
    sta <HuTrack.dda.addr.loop.hi,x
    lda .temp.addr.bnk
    sta <HuTrack.dda.loop.bank,x
    jsr HuTrackEngine._htk.WSG.DDA
      cli

.skip.pcm

        _htk.PULLBANK.2 _htk.PAGE_4000

  rts





;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#





;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// update waveform                                                                                         /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
HuTrackEngine.Channel.waveformEnv

        bit HuTrack.channel.ddaState,x
      bpl .cont
.fast.out
        jmp .return

.cont
        lda HuTrack.WfEnvPtr.lo,x
        sta <HuTrack.A0
        lda HuTrack.WfEnvPtr.hi,x
        sta <HuTrack.A0+1


        lda HuTrack.WfEnv.len,x       ; There's nothing in the waveform macro.. use direct waveform
      beq .get.direct.waveform

        lda HuTrack.WfEnv.idx,x
        cmp HuTrack.WfEnv.len,x
      bcs .check.loop.reload
.current.waveform.index
        tay
        inc HuTrack.WfEnv.idx,x
      bra .get.macro.waveform

.check.loop.reload
        lda HuTrack.WfEnv.repeat,x
        cmp #$ff
      beq .load.last.waveform
        sta HuTrack.WfEnv.idx,x
      bra .current.waveform.index


.get.direct.waveform
        lda HuTrack.channel.directWaveform,x
      bra .check.last.waveform

        ; The envelope index has expired. output the last one found. NOTE: 10xx replaces this if envelope expired.
.load.last.waveform
        lda HuTrack.channel.lastEnvWaveform,x
      bra .check.last.waveform


.get.macro.waveform
        lda HuTrack.song.format
      beq .wave.read
        lda HuTrack.WfEnv.bank,x
        jsr HuTrack.Bank.mapPair
.wave.read
        lda [HuTrack.A0],y

.check.last.waveform
        sta HuTrack.channel.lastEnvWaveform,x
        bit HuTrack.SFX.inProgress,x
      bmi .wave.blocked
        bit HuTrack.channel.waitNote,x
      bmi .wave.blocked
        cmp HuTrack.channel.uploadedWaveform,x
      bne .update.cont
.wave.blocked
        jmp .out
.update.cont
        sta HuTrack.channel.uploadedWaveform,x
        pha
        lda HuTrack.song.format
      beq .legacy.wave
        pla
        jsr HuTrack.Bank.waveform
        jmp .copy.wave
.legacy.wave
        pla
        asl a
        tay

        bit HuTrack.SFX.inProgress,x
      bpl .write.port
        jmp .out
.write.port

        lda HuTrack.waveform.table
        sta <HuTrack.A0
        lda HuTrack.waveform.table+1
        sta <HuTrack.A0+1

        lda [HuTrack.A0],y
        iny
        sta <HuTrack.A1
        lda [HuTrack.A0],y
        sta <HuTrack.A1+1

.copy.wave
        ; Both readers leave the complete waveform mapped, including a bank
        ; crossing. Patch the dedicated RAM stub for one direct ROM-to-PSG TIN.
        lda <HuTrack.A1
        sta HuTrack.DMA+1
        lda <HuTrack.A1+1
        sta HuTrack.DMA+2

        bit HuTrack.SFX.inProgress,x
      bmi .out

        ; Upload control writes must obey the music fade too: restoring the
        ; raw level would briefly unmute a silent song on every wave change.
        lda HuTrack.channel.proccessState,x
        and #$1f
        sec
        sbc HuTrack.musicAttenuation
      bcs .upload.volume
        cla
.upload.volume
        sta HuTrack.M.delta
        ora #$40
        tay
        lda HuTrack.channel.proccessState,x
        and #$e0
        ora HuTrack.M.delta
        ; Protect channel selection, upload and control restoration together:
        ; the timer IRQ can select another PSG channel. Restore the caller's
        ; interrupt state rather than unconditionally enabling interrupts.
          php
          sei
        stx $800
        sta $804
        sty $804
        tay
        and #$1f
        sta $804
        jsr HuTrack.DMA
        sty $804
          plp

.return
.out
  rts



;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Update volume                                                                                           /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
; Legacy Furnace combines envelope and channel volume with floor(v*env/31).
; Once an envelope ends, its output holds until a changed volume command.
HuTrackEngine.Channel.volumeEnv
        lda HuTrack.channel.directVolume,x
        sec
        sbc HuTrack.P.tremAttenuation,x
      bcs .driver
        cla
.driver
        jsr HuTrack.FX.applyVolume
.unchanged
        bit HuTrack.channel.ddaState,x
      bmi .direct
        lda HuTrack.VolEnv.len,x
      beq .direct
        lda HuTrack.VolEnv.idx,x
        cmp HuTrack.VolEnv.len,x
      bcc .entry
        lda HuTrack.VolEnv.repeat,x
        cmp #255
      beq .output
        sta HuTrack.VolEnv.idx,x
.entry
        tay
        inc HuTrack.VolEnv.idx,x
        lda HuTrack.VolEnvPtr.lo,x
        sta <HuTrack.A0
        lda HuTrack.VolEnvPtr.hi,x
        sta <HuTrack.A0+1
        lda HuTrack.song.format
      beq .volume.read
        lda HuTrack.VolEnv.bank,x
        jsr HuTrack.Bank.mapPair
.volume.read
        lda [HuTrack.A0],y
        cmp #32
      bcc .scale
        lda #31
.scale

        jsr HuTrack.Math.volume
      bra .store
.direct
        lda HuTrack.P.driverVolume,x
.store
        sta HuTrack.P.outputVolume,x
.output
        lda HuTrack.P.outputVolume,x
        ora #$80
        sta HuTrack.channel.proccessState,x
        and #31
        ora #$80
        bit HuTrack.channel.ddaState,x
      bpl .control
        ora #$40
.control
        jmp HuTrackEngine._htk.WSG.control


HuTrackEngine.Channel.arpEnv
        bit HuTrack.channel.ddaState,x
      bpl .start
        rts
.start
        lda HuTrack.ArpEnv.finished,x
      bne .done
        lda HuTrack.ArpEnv.len,x
      bne .enabled
        rts
.enabled
        lda HuTrack.ArpEnv.idx,x
        cmp HuTrack.ArpEnv.len,x
      bcc .entry
        lda HuTrack.ArpEnv.repeat,x
        cmp #$ff
      bne .loop
        lda #1
        sta HuTrack.ArpEnv.finished,x
        lda HuTrack.ArpEnv.mode,x
      bne .fixed.end
.done
        rts
.fixed.end
        ; Keep the length intact so a new note/retrigger can restart it.
        ; Furnace appends relative zero only when the length is below 255.
        lda HuTrack.ArpEnv.len,x
        cmp #255
      beq .done
        lda HuTrack.P.anchor,x
        jmp .apply
.loop
        sta HuTrack.ArpEnv.idx,x
.entry
        tay
        inc HuTrack.ArpEnv.idx,x
        lda HuTrack.ArpEnvPtr.lo,x
        sta <HuTrack.A0
        lda HuTrack.ArpEnvPtr.hi,x
        sta <HuTrack.A0+1
        lda HuTrack.song.format
      beq .arp.read
        lda HuTrack.ArpEnv.bank,x
        jsr HuTrack.Bank.mapPair
.arp.read
        lda [HuTrack.A0],y

        pha
        lda HuTrack.ArpEnv.mode,x
      beq .relative
        pla
        clc
        adc #60
      bcc .apply
        lda #255
      bra .apply
.relative
        pla
        cmp #$80
      bcc .positive
        clc
        adc HuTrack.P.anchor,x
      bcs .apply
        cla
      bra .apply
.positive
        clc
        adc HuTrack.P.anchor,x
      bcc .apply
        lda #255
.apply
        pha
        lda #1
        sta HuTrack.P.dirty,x
        lda HuTrack.P.inPorta,x
      beq .period
        pla
        rts
.period
        pla
        pha
        jsr HuTrack.Pitch.noiseNote
        pla
        jsr HuTrack.Pitch.setBase
        rts


HuTrackEngine.Channel.SetFrequency
        jmp HuTrack.Pitch.frequency


HuTrackEngine.Process.envelopes
        jsr HuTrack.FX.lfoApply

        _htk.PUSHBANK.4 _htk.PAGE_4000
        _htk.MAP_BANK.4 HuTrack.song.windowBank, _htk.PAGE_4000

        clx
.channel.loop
        jsr HuTrack.FX.delayedRow
        lda HuTrack.Enabled,x
      beq .skip
        jsr HuTrackEngine.channel.DelayAndCut
      bcc .skip
        jsr HuTrackEngine.Channel.exeFX
        jsr HuTrackEngine.Channel.arpEnv
        jsr HuTrackEngine.Channel.SetFrequency
        jsr HuTrackEngine.Channel.waveformEnv
        jsr HuTrackEngine.Channel.volumeEnv

.skip
        inx
        cpx #$06
      bcc .channel.loop

        _htk.PULLBANK.4 _htk.PAGE_4000

  rts



;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#





;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Handle multiple FX for each channel                                                                     /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
; These are for the on going FX like slides and LFOs
HuTrackEngine.Channel.exeFX
        jsr HuTrack.FX.legatoTick
        jsr HuTrack.Pitch.slide
        jsr HuTrack.Pitch.arpeggio
        jsr HuTrack.FX.volumeTick
        jsr HuTrack.FX.tremoloTick
        jsr HuTrack.FX.retriggerTick
        rts


HuTrackEngine._htk.WSG.control:

        bit HuTrack.SFX.inProgress,x
      bmi .out
        bit HuTrack.channel.waitNote,x
      bmi .out
.cont
        sta HuTrack.channel.write.volume,x ; cache the unattenuated control
        ldy HuTrack.musicAttenuation
      beq .write
        pha
        and #31
        sec
        sbc HuTrack.musicAttenuation
      bcs .attenuated
        cla
.attenuated
        sta HuTrack.M.delta
        pla
        and #$e0
        ora HuTrack.M.delta
.write
          php
          sei
        stx $800
        sta $804
          plp
.out

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine._htk.WSG.freq:

        bit HuTrack.SFX.inProgress,x
      bmi .out
        bit HuTrack.channel.waitNote,x
      bmi .out
.cont
          php
          sei
        stx $800
        sty $802
        sta $803
          plp

.out

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine._htk.WSG.DDA:

        bit HuTrack.SFX.inProgress,x
      bmi .out
        bit HuTrack.channel.waitNote,x
      bmi .out
.cont

        sta <HuTrack.dda.bank,x
        stz <HuTrack.dda.inactive,x

.out

  rts

HuTrackEngine._htk.WSG.DDAstop:
        bit HuTrack.SFX.inProgress,x
      bmi .out
        bit HuTrack.channel.waitNote,x
      bmi .out
        lda #$80
        sta <HuTrack.dda.inactive,x
        sta <HuTrack.dda.bank,x
.out
        rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine._htk.WSG.pan:

        sta HuTrack.channel.panState,x
        bit HuTrack.SFX.inProgress,x
      bmi .out
        bit HuTrack.channel.waitNote,x
      bmi .out
.cont
          php
          sei
        stx $800
        sta $805
          plp

.out

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine._htk.WSG.noise:

        bit HuTrack.SFX.inProgress,x
      bmi .out
        bit HuTrack.channel.waitNote,x
      bmi .out
.cont
          php
          sei
        stx $800
        sta $807
          plp

.out

  rts



;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#





;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Utility Routines                                                                                        /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; Legacy noise pitch by semitone.
NoiseTable:
    ;   C, C#,  D, D#,  E,  F, F#,  G, G#,  A, A#,  B
  .db    $84,$8D,$8F,$92,$95,$97,$99,$9B,$9D,$9F,$80,$82

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



    .include "HuTrack/engine/HuTrack_pitch.asm"
    .include "HuTrack/engine/HuTrack_banks.asm"
