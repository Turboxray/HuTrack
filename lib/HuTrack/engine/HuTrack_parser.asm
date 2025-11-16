
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

          ; NOTE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          ; turning interrupts on..
          ; TODO protection against double call (will probably never happen)
          cli

        ;........................
        ; Read in channel data

        clx
        stz HuTrack.current.channel

.debug.pattern

        _htk.MOVE.w HuTrack.pattern.table, <HuTrack.PatterPtr
        _htk.PUSHBANK.4 _htk.PAGE_4000
        _htk.MAP_BANK.4 HuTrack.patternList.table.bank, _htk.PAGE_4000


.readTracks

        stz HuTrack.channel.update
        stz HuTrack.entryParse.extFX
        stz HuTrack.entryParse
        stz HuTrack.rowIncrement

        ldx HuTrack.current.channel
        lda HuTrack.channel.rowSkip,x
      beq .fetch.row.entry
        dec HuTrack.channel.rowSkip,x
      jmp .row.position.tracking


.fetch.row.entry

        _htk.DEBUG_NOP

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

        ; DEBUG this needs to change. It's a default for now
        ; NOTE need a function that clears these variables on new pattern entry
        stz HuTrack.channel.noteDelay,x


        ;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        ; TODO disable old SFX handler
;         bit HuTrack.SFX.inProgress,x
;       bvc .real.parse
;         jsr HuTrackEngine.ParseEntry.disabled
;         sty HuTrack.rowIncrement
;       bra .check.patternBreak
; .real.parse
        jsr HuTrackEngine.ParseEntry
        sty HuTrack.rowIncrement
        jsr HuTrackEngine.Channel.update
        jsr HuTrackEngine.Channel.output
        ;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        _htk.DEBUG_NOP

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

.row.position.tracking
        inc HuTrack.channel.rowPos,x
        lda HuTrack.channel.rowPos,x
        cmp HuTrack.rowLen
      bcc .skip.pattern.reload
        stz HuTrack.channel.rowPos,x
        stz HuTrack.channel.patternOffset.lo,x
        stz HuTrack.channel.patternOffset.hi,x
        stz HuTrack.channel.rowSkip,x

        lda HuTrack.channel.pattern.num,x
        inc a
        cmp HuTrack.patternListlen
      bcc .skip
          ; NOTE: The STZ is already taken care of from above.
        cla       ; Reset the pattern playlist num back to the beginning
        lda force_no_repeat
      beq .skip
        smb6 <HuTrack.Status
.skip
        sta HuTrack.channel.pattern.num,x

.skip.pattern.reload

        inc HuTrack.current.channel
        lda HuTrack.current.channel
        cmp #6
      bcs .check.patternBreak
.do.readTracks
        jmp .readTracks

.check.patternBreak
        lda HuTrack.channel.patternBreak
        cmp #$fe
      beq .pattern.break
        cmp #$ff
      beq .parser.return 
        jmp .pattern_jmp_fx_0B
.parser.return
        _htk.PULLBANK.4 _htk.PAGE_4000

  rts

;.................................
;.................................
.pattern.break
        lda #$FF ;Be sure we erase any breaks 
        sta HuTrack.channel.patternBreak
        stz HuTrack.current.channel
        ldx #$05

.pattern.break.loop
        stz HuTrack.channel.rowPos,x
        stz HuTrack.channel.patternOffset.lo,x
        stz HuTrack.channel.patternOffset.hi,x
        stz HuTrack.channel.rowSkip,x

        lda HuTrack.channel.pattern.num,x
        inc a
        cmp HuTrack.patternListlen
      bcc .pattern.break.skip
        lda force_no_repeat
      beq .parser.return
        smb6 <HuTrack.Status
        jmp .parser.return

.pattern.break.skip
        sta HuTrack.channel.pattern.num,x
        dex
      bpl .pattern.break.loop
        jmp .parser.return

;.................................
;.................................
.pattern_jmp_fx_0B
        lda HuTrack.channel.patternBreak
        sta HuTrack.channel.pattern.num+0
        sta HuTrack.channel.pattern.num+1
        sta HuTrack.channel.pattern.num+2
        sta HuTrack.channel.pattern.num+3
        sta HuTrack.channel.pattern.num+4
        sta HuTrack.channel.pattern.num+5
        
        lda #$FF
        sta HuTrack.channel.patternBreak ;This is the new value for don't pattern break

        stz HuTrack.channel.rowPos,x
        stz HuTrack.channel.patternOffset.lo,x
        stz HuTrack.channel.patternOffset.hi,x
        stz HuTrack.channel.rowSkip,x      
.pattern_jmp_fx_0B.skip
        jmp .parser.return

;.................................
;.................................


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
      beq .skip.fx1.arg
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
HuTrackEngine.ParseEntry.disabled:

        cly

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
      jmp .decode.out

.note.octave
      sta HuTrack.channel.note.backup,x
      jmp .decode.out

.check.skipEntry
        cmp #$ff
      bcs .do.reserved
        sec
        sbc #225
        sta HuTrack.channel.rowSkip,x
      jmp .decode.out

.do.reserved
      jmp .decode.out

.decode.mask
      lsr a     ; note
    bcc .skip0
      iny
.skip0
      lsr a     ; unused bit
      lsr a     ; instrument
    bcc .skip1
        pha
      lda [HuTrack.currentPattern],y
      sta HuTrack.channel.instr.backup,x
      iny
        pla
.skip1
      lsr a     ; volume
    bcc .skip2
        pha
      lda [HuTrack.currentPattern],y
      sta HuTrack.channel.dVol.backup,x
      lda #$1f
      sec
      sbc HuTrack.channel.dVol.backup,x
      sta HuTrack.channel.rVol.backup,x
      iny
        pla
.skip2
      lsr a     ; fx
    bcc .skip3
        pha
      lda [HuTrack.currentPattern],y
      sta HuTrack.channel.temp.fxNum
        pla
      iny
.skip3
      lsr a     ; fx arg
    bcc .skip4
        pha
      lda [HuTrack.currentPattern],y
      sta HuTrack.channel.current.fxArg
      jsr HuTrackEngine.FX.disabled.store
        pla
      iny
.skip4
      lsr a     ; ext fx arg
    bcc .skip5
      lda [HuTrack.currentPattern],y
      iny
      jsr HuTrackEngine.parse.extFX.disabled
.skip5

.decode.out

  rts


;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Parse ext FX for channels                                                                               /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;

; Some FX still need to be tracked if channel is disabled for SFX
HuTrackEngine.FX.disabled.store:

      lda HuTrack.channel.temp.fxNum
        cmp #$08        ; Pan
      bne .skip0
      lda HuTrack.channel.current.fxArg
      sta HuTrack.channel.panState,x
    rts
.skip0
        cmp #$09        ; speed 1
      bne .skip1
      lda HuTrack.channel.current.fxArg
      sta HuTrack.tickReload+1
        phy
      ldy HuTrack.TickIdx
      lda HuTrack.tickReload,y
      sta HuTrack.tick
        ply
    rts
.skip1
        cmp #$0D        ; Pattern break
      bne .skip2
      lda HuTrack.channel.current.fxArg
      sta HuTrack.channel.panState,x
    jmp .out
.skip2
        cmp #$0B        ; Position jump
      bne .skip3
      lda HuTrack.channel.current.fxArg
      sta HuTrack.channel.panState,x
    rts
.skip3
        cmp #$0F        ; speed 2
      bne .skip4
      lda HuTrack.channel.current.fxArg
      sta HuTrack.tickReload
        phy
      ldy HuTrack.TickIdx
      lda HuTrack.tickReload,y
      sta HuTrack.tick
        ply
    rts
.skip4
        cmp #$17        ; PCM
      bne .skip5
        lda HuTrack.channel.current.fxArg
      bne .dda.mode
        lda #$ff
        sta HuTrack.channel.pcmIDX.backup,x
        stz HuTrack.channel.ddaST.backup,x
        lda #$80
        sta HuTrack.channel.ddaST.backup,x
    rts
.dda.mode
        stz HuTrack.channel.noiseST.backup,x
          phy
        ldy HuTrack.channel.note.backup,x
        lda HuTrackEngine.tables.noteFromCombo,y
        sta HuTrack.channel.pcmIDX.backup,x
          ply
    rts
.skip5

        cmp #$11        ; Noise
      bne .skip6
        lda HuTrack.channel.current.fxArg
      bne .noise.on
        stz HuTrack.channel.noiseST.backup,x
    rts
.noise.on
        lda #$80
        sta HuTrack.channel.noiseST.backup,x
        stz HuTrack.channel.ddaST.backup,x
    rts
.skip6
.out
  rts


;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#




;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Parse ext FX for channels                                                                               /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
HuTrackEngine.parse.extFX
        stz HuTrack.channel.update.extFX
        stz HuTrack.channel.temp.fxArg2,x
        stz HuTrack.channel.temp.fxArg3,x
        stz HuTrack.channel.temp.fxArg4,x

.do.fx2
        bit #$01
      beq .do.fx3
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
      beq .do.fx4
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
      beq .out
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
HuTrackEngine.parse.extFX.disabled

      lsr a       ; fx2
    bcc .skip0
        pha
      lda [HuTrack.currentPattern],y
      sta HuTrack.channel.temp.fxNum
        pla
      iny
.skip0
      lsr a       ; fx2 arg
    bcc .skip1
        pha
      lda [HuTrack.currentPattern],y
      sta HuTrack.channel.current.fxArg
      jsr HuTrackEngine.FX.disabled.store
        pla
      iny
.skip1
      lsr a       ; fx3
    bcc .skip2
        pha
      lda [HuTrack.currentPattern],y
      sta HuTrack.channel.temp.fxNum
        pla
      iny
.skip2
      lsr a       ; fx3 arg
    bcc .skip3
        pha
      lda [HuTrack.currentPattern],y
      sta HuTrack.channel.current.fxArg
      jsr HuTrackEngine.FX.disabled.store
        pla
      iny
.skip3
      lsr a       ; fx4
    bcc .skip4
        pha
      lda [HuTrack.currentPattern],y
      sta HuTrack.channel.temp.fxNum
        pla
      iny
.skip4
      lsr a       ; fx4 arg
    bcc .skip5
        pha
      lda [HuTrack.currentPattern],y
      sta HuTrack.channel.current.fxArg
      jsr HuTrackEngine.FX.disabled.store
        pla
      iny
.skip5

.out
  rts

;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#




;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Parse update channels                                                                                   /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;

; Process channel entries; note, vol, fx, etc.
HuTrackEngine.Channel.update:

        stz HuTrack.channel.output,x


        lda HuTrack.channel.change,x
      beq .out


.note
        lda HuTrack.channel.change,x
        bit #$01
      beq .octave
        lda #$01
        sta HuTrack.Enabled,x
        jsr HuTrackEngine.Channel.update.Note

.octave
        lda HuTrack.channel.change,x
        bit #$02
      beq .volume
        jsr HuTrackEngine.Channel.update.Octave


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
      beq .instrument
        jsr HuTrackEngine.Channel.update.FX234

.instrument
        lda HuTrack.channel.change,x
        bit #$20
      beq .out
        jsr HuTrackEngine.Channel.update.Instrument

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
        jsr HuTrackEngine.reset.overload
        stz HuTrack.channel.volSlideDown,x
        stz HuTrack.channel.volSlideUp,x
        bit HuTrack.channel.ddaState,x
      bpl .note.cut
.sample.cut
        lda #$80
        jsr HuTrackEngine._htk.WSG.DDA
      bra .out

.note.cut
        stz HuTrack.channel.noteDelay,x
        stz HuTrack.Enabled,x
        lda HuTrack.channel.proccessState,x
        ora #$c0
        jsr HuTrackEngine._htk.WSG.control
      bra .out

.do.note_octave
        sta HuTrack.channel.note,x
        sta HuTrack.channel.appliedNote,x
        bit HuTrack.channel.ddaState,x
      bpl .decode.note

        tay
        lda HuTrackEngine.tables.noteFromCombo,y
        sta HuTrack.channel.pcmIndex,x
            lda HuTrack.channel.output,x
            ora #$04
            sta HuTrack.channel.output,x
      jmp .return

.decode.note
        tay
        lda HuTrackEngine.tables.octaveFromCombo,y
        sta HuTrack.channel.octave,x
        sta HuTrack.channel.appliedOctave,x
        lda HuTrackEngine.tables.noteFromCombo,y
        sta HuTrack.channel.note,x
        sta HuTrack.channel.appliedNote,x

.out
            stz HuTrack.WfEnv.idx,x
            stz HuTrack.VolEnv.idx,x
            stz HuTrack.ArpEnv.idx,x
            stz HuTrack.channel.porta.up.lo,x
            stz HuTrack.channel.porta.up.hi,x
            stz HuTrack.channel.porta.down.lo,x
            stz HuTrack.channel.porta.down.hi,x

            stz HuTrack.channel.pitch.period.lo,x
            stz HuTrack.channel.pitch.period.hi,x

            lda HuTrack.channel.output,x
            ora #$01
            sta HuTrack.channel.output,x
.return
  rts


;...........................................................
HuTrackEngine.Channel.update.Octave

        ; TODO : This isn't supposed in Deflemask. Basically an octave request change without a note.
  rts


;...........................................................
HuTrackEngine.Channel.update.Volume
        lda HuTrack.channel.temp.volume,x
        sta HuTrack.channel.directVolume,x
        lda #$1f
        sec
        sbc HuTrack.channel.directVolume,x
        sta HuTrack.channel.relativeVolume,x
        lda HuTrack.channel.change,x
        eor #$04
        sta HuTrack.channel.change,x

        lda HuTrack.VolEnv.idx,x
        cmp HuTrack.VolEnv.len,x
      bcc .out
        lda HuTrack.VolEnv.repeat,x
        cmp #$ff
      bne .out
        lda HuTrack.channel.directVolume,x
        lda #$80
        sta HuTrack.channel.lastEnvVolume,x

.out

  rts


;...........................................................
HuTrackEngine.Channel.update.FX:
        lda HuTrack.channel.change,x
        eor #($08 | $10)
        sta HuTrack.channel.change,x

        lda HuTrack.channel.temp.fxArg1,x
        sta HuTrack.channel.fxArg1,x
        sta HuTrack.channel.current.fxArg

        lda HuTrack.channel.temp.fx1,x
        sta HuTrack.channel.fx1,x

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
        sta HuTrack.channel.fxArg2,x
        sta HuTrack.channel.current.fxArg

        lda HuTrack.channel.temp.fx2,x
        sta HuTrack.channel.fx2,x

        jsr HuTrack.channel.FX.handler


.fx3
        lda HuTrack.channel.update.extFX
        bit #$04
      beq .fx4
        lda HuTrack.channel.temp.fxArg3,x
        sta HuTrack.channel.fxArg3,x
        sta HuTrack.channel.current.fxArg

        lda HuTrack.channel.temp.fx3,x
        sta HuTrack.channel.fx3,x

        jsr HuTrack.channel.FX.handler


.fx4
        lda HuTrack.channel.update.extFX
        bit #$10
      beq .out
        lda HuTrack.channel.temp.fxArg4,x
        sta HuTrack.channel.fxArg4,x
        sta HuTrack.channel.current.fxArg

        lda HuTrack.channel.temp.fx4,x
        sta HuTrack.channel.fx4,x

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
  rts

;...........................................................
;...........................................................
; 01xx
.FX.PortaUp
          plx
        lda HuTrack.channel.current.fxArg
        eor #$ff
        clc
        adc #$01
        sta HuTrack.channel.porta.up.lo,x
        cla
        adc #$ff
        sta HuTrack.channel.porta.up.hi,x

        stz HuTrack.channel.porta.down.lo,x
        stz HuTrack.channel.porta.down.hi,x

  rts

;...........................................................
;...........................................................
; 02xx
.FX.PortaDown
          plx
        lda HuTrack.channel.current.fxArg
        sta HuTrack.channel.porta.down.lo,x
        stz HuTrack.channel.porta.down.hi,x

        stz HuTrack.channel.porta.up.lo,x
        stz HuTrack.channel.porta.up.hi,x
  rts

;...........................................................
;...........................................................
; 03xx
.FX.PortaNote
          plx
  rts

;...........................................................
;...........................................................
; 04xx
.FX.vibrato
          plx
        lda HuTrack.channel.current.fxArg
      bne .cont
        lda HuTrack.channel.vibrato.idx,x
        ora #$80
        sta HuTrack.channel.vibrato.idx,x
      bra .FX.vibrato.out

.cont
        lsr a
        lsr a
        lsr a
        lsr a
        sta HuTrack.channel.vibrato.inc,x
        lda HuTrack.channel.current.fxArg
        and #$0F
        tay
        lda VibratoScaleTable,y
        sta HuTrack.channel.vibrato.scale,x

        lda HuTrack.channel.vibrato.idx,x
        and #$3f
        sta HuTrack.channel.vibrato.idx,x

.FX.vibrato.out

  rts

;...........................................................
;...........................................................
; 05xx
.FX.PortaNote_volSlide
          ; This is redundant because volume slide is an auto-continuing FX
          plx
  rts

;...........................................................
;...........................................................
; 06xx
.FX.vibrato_volSlide
          plx
        ; NOTE: The vibrato part does nothing here. The manual is wrong from my tests.
        lda HuTrack.channel.current.fxArg
      beq .FX.vibrato_volSlide.disable
        tst #$f0, HuTrack.channel.current.fxArg
      bne .FX.vibrato_volSlide.check.vol.up
        sta HuTrack.channel.volSlideDown,x
        stz HuTrack.channel.volSlideUp,x
      bra .FX.vibrato_volSlide.out

.FX.vibrato_volSlide.check.vol.up
        tst #$0f, HuTrack.channel.current.fxArg
      bne .FX.vibrato_volSlide.disable        ; impossible combo
        stz HuTrack.channel.volSlideDown,x
        lsr a
        lsr a
        lsr a
        lsr a
        sta HuTrack.channel.volSlideUp,x
      bra .FX.vibrato_volSlide.out

.FX.vibrato_volSlide.disable
        stz HuTrack.channel.volSlideDown,x
        stz HuTrack.channel.volSlideUp,x

.FX.vibrato_volSlide.out

  rts

;...........................................................
;...........................................................
; 07xx
.FX.tremolo
          plx
  rts

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
        lda HuTrack.channel.current.fxArg
        sta HuTrack.tickReload+1
        ldy HuTrack.TickIdx
        lda HuTrack.tickReload,y
        sta HuTrack.tick

.FX.setSpeed1.out

  rts

;...........................................................
;...........................................................
; 0Axx
.FX.volSlide
        ; Same effect as 06xy so re-use that code
        jmp .FX.vibrato_volSlide

;...........................................................
;...........................................................
; 0Bxx
.FX.jump
        plx
        lda HuTrack.channel.current.fxArg        
        sta HuTrack.channel.patternBreak
  rts

;...........................................................
;...........................................................
; 0Cxx
.FX.retrig
          plx
  rts

;...........................................................
;...........................................................
; 0Dxx
.FX.break
          plx
        lda #$ff
        sta HuTrack.channel.patternBreak
  rts

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
        lda HuTrack.channel.current.fxArg
        sta HuTrack.tickReload
        ldy HuTrack.TickIdx
        lda HuTrack.tickReload,y
        sta HuTrack.tick

.FX.SetSpeed2.out

  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


;...........................................................
;...........................................................
; E0xx
.extFX.ArpSpeed
          plx
  rts

;...........................................................
;...........................................................
; E1xx
.extFX.NoteSlideUp
          plx
            lda HuTrack.channel.current.fxArg
            and #$0f
            sta HuTrack.channel.semitoneUP.op,x
            sta HuTrack.channel.semitoneUP.cent,x
            stz HuTrack.channel.semitoneUP.note,x
            lda HuTrack.channel.current.fxArg
            and #$f0
            asl a
            sta HuTrack.channel.semitoneUP.delta,x
  rts

;...........................................................
;...........................................................
; E2xx
.extFX.NoteSlideDown
          plx
           lda HuTrack.channel.current.fxArg
            and #$0f
            sta HuTrack.channel.semitoneDOWN.op,x
            sta HuTrack.channel.semitoneDOWN.cent,x
            stz HuTrack.channel.semitoneDOWN.note,x
            lda HuTrack.channel.current.fxArg
            and #$f0
            asl a
            sta HuTrack.channel.semitoneDOWN.delta,x
  rts

;...........................................................
;...........................................................
; E3xx - vibrato mode (0, 1, 2)
.extFX.VibratoMode
                ; TODO
          plx
  rts

;...........................................................
;...........................................................
; E4xx - vibrato fine depth
.extFX.VibratoDepth
                ; TODO
          plx
  rts

;...........................................................
;...........................................................
; E5xx
.extFX.FineTune
          plx

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
          ; null
  rts

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
          ;null
  rts

;...........................................................
;...........................................................
; E9xx
.extFX.E9
          plx
          ;null
  rts

;...........................................................
;...........................................................
; EAxx
.extFX.EA
          plx
          ;null
  rts

;...........................................................
;...........................................................
; EBxx
.extFX.EB
          plx
          ;null
  rts

;...........................................................
;...........................................................
; ECxx
.extFX.NoteCut
        ; This is not the same as 'OFF' which is an immediate effect. This has a delay.
          plx
        lda HuTrack.channel.current.fxArg
        ora #$80                        ; Setting these bits so this is processed later.
                                        ; NOTE: Because a value greater than the current row tick length is ignored
                                        ;       and a tick/speed change could happen on an FX column after this entry.
        sta HuTrack.channel.noteDelay,x

.extFX.NoteCut.out
  rts

;...........................................................
;...........................................................
; EDxx
.extFX.NoteDelay
          plx
        lda HuTrack.channel.current.fxArg
        ora #$80+$40                    ; Setting these bits so this is processed later.
                                        ; NOTE: Because a value greater than the current row tick length is ignored
                                        ;       and a tick/speed change could happen on an FX column after this entry.
        sta HuTrack.channel.noteDelay,x

  rts

;...........................................................
;...........................................................
; EExx
.extFX.Sync
          plx
  rts

;...........................................................
;...........................................................
; EFxx
.extFX.GlobFineTune
          plx
  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



;...........................................................
;...........................................................
; 10xx
.platFX.setWave
          plx
.direct.waveform.change
        ; HOTFIX: setting FX 0x10 disables. This might cause issues if it's called by itself.
        lda #$00
        jsr HuTrackEngine._htk.WSG.noise
        stz HuTrack.channel.noiseMode,x
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
        lda HuTrack.channel.current.fxArg

      beq .turnoff.noise
.turnon.noise
        ldy HuTrack.channel.note,x
        lda NoiseTable,y
        jsr HuTrackEngine._htk.WSG.noise
        sta HuTrack.channel.noisePeriod,x
        sta HuTrack.channel.appliedNoise,x
        lda #$80
        sta HuTrack.channel.noiseMode,x
        lda HuTrack.channel.proccessState,x
        and #$1f
        tay
        lda NoiseVolumeAdjust,y
        ora #$80
        jsr HuTrackEngine._htk.WSG.control
        stz HuTrack.channel.ddaState,x
        cpx #$05
      bne .platFX.Noise.out
        ; TODO this needs a separate function so it's not dependent on only channel 5
        lda #$80
        jsr HuTrackEngine._htk.WSG.DDA

      jmp .platFX.Noise.out

.turnoff.noise
        lda #$00
        jsr HuTrackEngine._htk.WSG.noise
        stz HuTrack.channel.noiseMode,x
        ; TODO this needs to come out. The envelopes should be turning the channel back on. But needs more state logic.

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
  rts

;...........................................................
;...........................................................
; 13xx
.platFX.LFOspeed
          plx
  rts

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
        jsr HuTrackEngine._htk.WSG.DDA
        ;stz HuTrack.channel.noteDelay,x
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

        lda HuTrack.channel.change,x
        bit #$01
      beq .no.note
        ldy HuTrack.channel.note,x
        lda HuTrackEngine.tables.noteFromCombo,y
        sta HuTrack.channel.pcmIndex,x

        lda HuTrack.channel.output,x
        ora #$04
        sta HuTrack.channel.output,x

.no.note
.platFX.SamplePCM.out

  rts


;...........................................................
;...........................................................
; 18xy overload. X = speed, Y == amount. X = 0, effect is paused. Y = 0, internal accumulator is reset to 0.
.platFX.overload
          plx
        lda HuTrack.channel.current.fxArg
      beq .platFX.overload.resetAll
        and #$f0
        lsr a
        lsr a
        lsr a
        lsr a
        sta HuTrack.channel.overload.spd,x
        lda HuTrack.channel.current.fxArg
        and #$0f
        sta HuTrack.channel.overload.amt,x
      bra .platFX.overload.out

.platFX.overload.resetAll
        jsr HuTrackEngine.reset.overload

.platFX.overload.out

  rts


;...........................................................
;...........................................................
; 19xy overload. X = speed, Y == amount. X = 0 mean pauses. Y = 0, internal accumulator is reset to 0.
.platFX.corruption
          plx
        lda HuTrack.channel.current.fxArg
      beq .platFX.corruption.resetAll
        and #$f0
        lsr a
        lsr a
        lsr a
        lsr a
        sta HuTrack.channel.corruption.spd,x
        lda HuTrack.channel.current.fxArg
        and #$0f
        sta HuTrack.channel.corruption.delta,x
      bra .platFX.overload.out

.platFX.corruption.resetAll
        jsr HuTrackEngine.reset.corruption

.platFX.corruption.out


  rts

;...........................................................
;...........................................................
; 20xy overload. X = speed, Y == amount. X = 0 mean pauses. Y = 0, internal accumulator is reset to 0.
.platFX.hardsync
          plx
        lda HuTrack.channel.current.fxArg
      beq .platFX.hardsync.resetAll
        and #$f0
        lsr a
        lsr a
        lsr a
        lsr a
        sta HuTrack.channel.hardsync.spd,x
        lda HuTrack.channel.current.fxArg
        and #$0f
        sta HuTrack.channel.hardsync.amt,x
      bra .platFX.overload.out

.platFX.hardsync.resetAll
        jsr HuTrackEngine.reset.hardsync

.platFX.hardsync.out


  rts




;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#





;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Output changes to channels                                                                              /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;

; Final stages of channel entry processing.
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

        _htk.PUSHBANK.2 _htk.PAGE_4000

        ; TODO disable old SFX handler
    ;     bit HuTrack.SFX.inProgress,x
    ;   bvc .channel
    ; rts

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

    rmb7 <HuTrack.DDAprocess

    bit HuTrack.SFX.inProgress,x
  bmi .skip.pcm

      sei
    lda .temp.addr.lo
    sta <HuTrack.dda.addr.lo,x
    lda .temp.addr.hi
    sta <HuTrack.dda.addr.hi,x
    lda .temp.addr.bnk
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


        lda HuTrack.channel.noiseMode,x
      bne .fast.out

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
        lda [HuTrack.A0],y

.check.last.waveform
        cmp HuTrack.channel.lastEnvWaveform,x
      bne .update.cont
        jmp .out
.update.cont
        sta HuTrack.channel.lastEnvWaveform,x
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

        ; Reset the waveform pointer: TODO this state logic of "when" to reset the waveform pointer needs to be more complex.
        cly
.loop
        lda [HuTrack.A1],y
        sta HuTrack.waveform.buffer,y
        iny
        lda [HuTrack.A1],y
        sta HuTrack.waveform.buffer,y
        iny
        lda [HuTrack.A1],y
        sta HuTrack.waveform.buffer,y
        iny
        lda [HuTrack.A1],y
        sta HuTrack.waveform.buffer,y
        iny
        lda [HuTrack.A1],y
        sta HuTrack.waveform.buffer,y
        iny
        lda [HuTrack.A1],y
        sta HuTrack.waveform.buffer,y
        iny
        lda [HuTrack.A1],y
        sta HuTrack.waveform.buffer,y
        iny
        lda [HuTrack.A1],y
        sta HuTrack.waveform.buffer,y
        iny
        cpy #$20
      bcc .loop

        bit HuTrack.SFX.inProgress,x
      bmi .out

        lda HuTrack.channel.proccessState,x
        and #$1f
        ora #$40
        tay
        lda HuTrack.channel.proccessState,x
          sei
        stx $800
        sta $804
        sty $804
        tay
        and #$1f
        sta $804
        tin HuTrack.waveform.buffer, $806, 32
        sty $804
          cli

.return
.out
  rts



;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Update volume                                                                                           /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
HuTrackEngine.Channel.volumeEnv

        bit HuTrack.channel.ddaState,x
      bmi .return

        lda HuTrack.VolEnvPtr.lo,x
        sta <HuTrack.A0
        lda HuTrack.VolEnvPtr.hi,x
        sta <HuTrack.A0+1


        lda HuTrack.VolEnv.len,x
      beq .do.direct.vol

        lda HuTrack.VolEnv.idx,x
        cmp HuTrack.VolEnv.len,x
      bcs .check.loop.reload
        bra .get.volEnv.entry

.check.loop.reload
        lda HuTrack.VolEnv.repeat,x
        cmp #$ff
      beq .do.last.vol
        sta HuTrack.VolEnv.idx,x

.get.volEnv.entry
        tay
        inc HuTrack.VolEnv.idx,x

.cont
        lda [HuTrack.A0],y
        sta HuTrack.channel.lastEnvVolume,x
.relative.volume
        sec
        sbc HuTrack.channel.relativeVolume,x
      bpl .update
.skipEntry
        cla

.update
        ora #$80
        sta HuTrack.channel.proccessState,x
        and #$1f
        tst #$ff, HuTrack.channel.noiseMode,x
      beq .regular.vol
        tay
        lda NoiseVolumeAdjust,y
.regular.vol
        ora #$80
        jsr HuTrackEngine._htk.WSG.control
.return
.out

  rts

;---------------
.do.direct.vol
        lda HuTrack.channel.directVolume,x
      bra .update

;---------------
.do.last.vol
        ; NOTE: there's a bug in deflemask in that if the volume is set right as the vol envelope expires,
        ;       it turns the instrument into direct volume.
        lda HuTrack.channel.lastEnvVolume,x
        cmp #$80
      bcs .do.direct.vol
      bra .relative.volume

;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Update Arpeggios                                                                                        /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
HuTrackEngine.Channel.arpEnv

        bit HuTrack.channel.ddaState,x
      bpl .start
.return
      jmp .out

.start
        lda HuTrack.ArpEnvPtr.lo,x
        sta <HuTrack.A0
        lda HuTrack.ArpEnvPtr.hi,x
        sta <HuTrack.A0+1


        lda HuTrack.ArpEnv.len,x
      beq .return

        lda HuTrack.channel.octave,x
        sta HuTrack.process.temp0

        lda HuTrack.ArpEnv.idx,x
        cmp HuTrack.ArpEnv.len,x
      bcc .get.entry

        lda HuTrack.ArpEnv.repeat,x
        cmp #$ff
      beq .last.entry
        sta HuTrack.ArpEnv.idx,x
        bra .get.entry

.last.entry
        lda HuTrack.channel.lastEnvApr,x
        bra .cont

.get.entry
        tay
        inc HuTrack.ArpEnv.idx,x

        lda [HuTrack.A0],y
        sta HuTrack.channel.lastEnvApr,x
.cont
        tst #$ff, HuTrack.ArpEnv.mode,x
      beq .mode.relative

;............................................
.mode.fixed
        stz HuTrack.process.temp0
      bra .noise.direct.value           ; jump to the start of the loop because we only want the modulo

;............................................
.mode.relative
        cmp #$80
      bcc .mode.relative.positiveNum
        eor #$ff
        inc a

.negativeNum.loop
        cmp #12
      bcc .negative.prep
        sbc #12
        dec HuTrack.process.temp0
      bra .negativeNum.loop
.negative.prep
        sta HuTrack.process.temp1
        lda HuTrack.channel.note,x
        sec
        sbc HuTrack.process.temp1
      bcs .negative.skip1
        clc
        adc #11
        dec HuTrack.process.temp0
        clc
.negative.skip1
        sta HuTrack.process.temp1
        lda HuTrack.process.temp0
        cmp #$80
      beq .negative.skip2
        stz HuTrack.process.temp0
.negative.skip2                         ; what a pain in the ass...
        lda HuTrack.process.temp1
      jmp .period.noise.check

;............................................
.mode.relative.positiveNum
        clc
        adc HuTrack.channel.note,x

.noise.direct.value
.positiveNum.loop
        cmp #12
      bcc .positiveNum.prep
        sbc #12
        inc HuTrack.process.temp0
      bra .positiveNum.loop

.positiveNum.prep
          pha
        lda HuTrack.process.temp0
        cmp #$07
      bcc .positiveNum.octave
        lda #$07
        sta HuTrack.process.temp0
.positiveNum.octave
          pla

;............................................
.period.noise.check
        tst #$ff, HuTrack.channel.noiseMode,x
      beq .period.done
.noise.done
        tay
        lda NoiseTable,y
        sta HuTrack.channel.appliedNoise,x
      bra .out

.period.done
        tay
        lda HuTrackEngine.tables.noteFromCombo,y
        sta HuTrack.channel.appliedNote,x
        lda HuTrack.process.temp0
        sta HuTrack.channel.appliedOctave,x

.out

  rts

;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Output final frequency                                                                                  /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
HuTrackEngine.Channel.SetFrequency

        bit HuTrack.channel.ddaState,x
      bpl .cont
        jmp .out

.cont
        tst #$ff, HuTrack.channel.noiseMode,x
      beq .period

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

.noise
        lda HuTrack.channel.appliedNoise,x
        jsr HuTrackEngine._htk.WSG.noise
      jmp .out

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

.period
        ; Octave:Note:NoteCent
        lda HuTrack.channel.detune,x
        cmp #$80
      bne .period.detune.delta.direction

;...................................
;...................................
.period.NoDetune
        lda HuTrack.channel.appliedCent,x
        sta HuTrack.channel.temp.noteCent
        lda HuTrack.channel.appliedNote,x
        sta HuTrack.channel.temp.note
        lda HuTrack.channel.appliedOctave,x
        sta HuTrack.channel.temp.octave
      jmp .period.slide


;...................................
;...................................
; Detune
.period.detune.delta.direction
      bcs .period.detune.up

;-------------------
; Goes up in frequency by subtracting from the base
.period.detune.down
        eor #$7f
        clc
        asl a
        sta HuTrack.channel.temp.noteCent

        lda HuTrack.channel.appliedCent,x
        sec
        sbc HuTrack.channel.temp.noteCent
        sta HuTrack.channel.temp.noteCent

        lda HuTrack.channel.appliedOctave,x
        sta HuTrack.channel.temp.octave

        lda HuTrack.channel.appliedNote,x
        sbc #$00
      bcs .period.detune.down.skip
        lda #11
        dec HuTrack.channel.temp.octave
.period.detune.down.skip
        sta HuTrack.channel.temp.note
      jmp .period.slide

;-------------------
; Goes down in frequency by adding from the base
.period.detune.up
        clc
        asl a
        clc
        adc HuTrack.channel.appliedCent,x
        sta HuTrack.channel.temp.noteCent

        lda HuTrack.channel.appliedOctave,x
        sta HuTrack.channel.temp.octave

        lda HuTrack.channel.appliedNote,x
        adc #$00
        cmp #12
      bcc .period.detune.up.skip
        cla
        inc HuTrack.channel.appliedOctave,x
.period.detune.up.skip
        sta HuTrack.channel.temp.note
      jmp .period.slide


;...................................
;...................................
; Slide
.period.slide
        ; This is already done on the FX side.

      jmp .period.vibrato



;...................................
;...................................
; Vibrato
.period.vibrato
        lda HuTrack.channel.vibrato.idx,x
        cmp #$80
      bcs .update.period
        cmp #32
      bcs .period.vibrato.subtract

;-------------------
.period.vibrato.add
        lda HuTrack.channel.vibrato.cent,x
        adc HuTrack.channel.temp.noteCent
        sta HuTrack.channel.temp.noteCent

        lda HuTrack.channel.temp.note
        adc #$00
        cmp #12
      bcc .period.vibrato.add.skip
        cla
        inc HuTrack.channel.temp.octave
.period.vibrato.add.skip
        sta HuTrack.channel.temp.note
      jmp .update.period

;-------------------
.period.vibrato.subtract

        lda HuTrack.channel.temp.noteCent
        sec
        sbc HuTrack.channel.vibrato.cent,x
        sta HuTrack.channel.temp.noteCent

        lda HuTrack.channel.temp.note
        sbc #$00
      bcs .period.vibrato.subtract.skip
        lda #11
        dec HuTrack.channel.temp.octave
.period.vibrato.subtract.skip
        sta HuTrack.channel.temp.note
      jmp .update.period



;...................................
;...................................
; Update Period
.update.period

      ; Handle Cents first
      ; NOTE: The higher the 'cents' number, the higher the frequency, which means need to subtract it
      ;       from the main note frequency.
        ldy HuTrack.channel.temp.note
        lda NoteCents.table,y
        sta HuTrack.process.temp0

        lda HuTrack.channel.temp.noteCent
        sta HuTrack.process.temp1

        jsr HuTrackEngine.8x8mul

        stz HuTrack.channel.applied.period.lo,x
        stz HuTrack.channel.applied.period.hi,x
      beq .no.offset
        eor #$ff
        inc a
        sta HuTrack.channel.applied.period.lo,x
        lda #$ff
        sta HuTrack.channel.applied.period.hi,x
.no.offset

      ; Handle note

        sec
        lda #$80
        sbc HuTrack.channel.temp.octave
        lda HuTrack.channel.temp.note
        adc #$00
        asl a
        tay
        lda BaseNoteFreq - 2,y
        clc
        adc HuTrack.channel.applied.period.lo,x
          pha
        lda BaseNoteFreq - 2 + 1,y
        adc HuTrack.channel.applied.period.hi,x
          ply

      ; Handle octave
.period.update.loop
        dec HuTrack.channel.temp.octave
      bmi .period.write
        lsr a
        say
        ror a
        say
      bra .period.update.loop

.period.write
        ; Add in pitch slide
        say
        clc
        adc HuTrack.channel.pitch.period.lo,x
        say
        adc HuTrack.channel.pitch.period.hi,x
        cmp #$10
      bcc .period.write.cont
        ldy #$ff
        lda #$0f
.period.write.cont
        ; TODO !!! The limit boundaries for porta up and porta down need to be checked here!
        ;      !!! If those boundaries have cross, saturate to said boundaries. And then cancel all slides?

        jsr HuTrackEngine._htk.WSG.freq


.return
.out
  rts

;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Output Delay                                                                                            /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
HuTrackEngine.channel.DelayAndCut:

        lda HuTrack.channel.noteDelay,x
      beq .delayExpired

.process.delay.check
      bpl .process.delay.NoteDelay
.process.delay.prep
        and #$7f
        sta HuTrack.channel.noteDelay,x         ; Clear the prep bit..
        ldy HuTrack.TickIdx
        and #$3f
        cmp HuTrack.tick,y
      bcc .noteDelayContinue
      beq .noteDelayContinue
        ; otherwise it's greater than the size of the tick, so ignore the delay.
        stz HuTrack.channel.noteDelay,x
      bra .delayExpired

.process.delay.NoteDelay
        bit HuTrack.channel.noteDelay,x
      bvs .process.delay.NoteDelay.downcount

.process.delay.NoteCutDelay.downcount
        lda HuTrack.channel.noteDelay,x
        dec a
        sta HuTrack.channel.noteDelay,x
        and #$3f
      bne .delayExpired
        jsr HuTrackEngine.reset.overload
        stz HuTrack.channel.noteDelay,x
        stz HuTrack.Enabled,x

        bit HuTrack.channel.ddaState,x
      bpl .process.note.cut
.process.sample.cut
        lda #$80
        jsr HuTrackEngine._htk.WSG.DDA
        clc
      bra .out

.process.note.cut
        stz HuTrack.channel.volSlideDown,x
        stz HuTrack.channel.volSlideUp,x

        lda #$00
        jsr HuTrackEngine._htk.WSG.control
        clc
      bra .out


.process.delay.NoteDelay.downcount
        lda HuTrack.channel.noteDelay,x
        dec a
        sta HuTrack.channel.noteDelay,x
        and #$3f
      bne .noteDelayContinue
        stz HuTrack.channel.noteDelay,x
      bra .delayExpired
.noteDelayContinue
        clc
      bra .out

.delayExpired
        sec
.out
  rts





;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#





;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Process all channels for audio output                                                                   /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;

; Set/update channel's audio registers/output.
HuTrackEngine.Process.envelopes

        _htk.PUSHBANK.4 _htk.PAGE_4000
        _htk.MAP_BANK.4 HuTrack.patternList.table.bank, _htk.PAGE_4000

        clx
.channel.loop
        ; TODO disable old SFX handler
    ;     bit HuTrack.SFX.inProgress,x
    ;   bvs .skip
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

.semiToneSlide.up
        lda HuTrack.channel.semitoneUP.op,x
      beq .semiToneSlide.down
        jsr HuTrackEngine.Channel.exeFX.semitone.UP

.semiToneSlide.down
        lda HuTrack.channel.semitoneDOWN.op,x
      beq .vibrato
        jsr HuTrackEngine.Channel.exeFX.semitone.DOWN

.vibrato
        lda HuTrack.channel.vibrato.idx,x
        cmp #$80
      bcs .portaSlideUp
        jsr HuTrackEngine.Channel.exeFX.vibrato

.portaSlideUp
        jsr HuTrackEngine.Channel.exeFX.portaSlideUp

.portaSlideDown
        jsr HuTrackEngine.Channel.exeFX.portaSlideDown

.portaSlideNote
      bra .arpeggio

.arpeggio
      bra .volumeSlideUp

.volumeSlideUp
        lda HuTrack.channel.volSlideUp,x
      beq .volumeSlideDown
        jsr HuTrackEngine.Channel.exeFX.volSlideUp

.volumeSlideDown
        lda HuTrack.channel.volSlideDown,x
      beq .overload
        jsr HuTrackEngine.Channel.exeFX.volSlideDown

.overload
        lda HuTrack.channel.overload.amt,x
      beq .corruption
        jsr HuTrackEngine.Channel.exeFX.overload

.corruption
        lda HuTrack.channel.corruption.spd,x
      beq .hardsync
        jsr HuTrackEngine.Channel.exeFX.corruption

.hardsync
        lda HuTrack.channel.hardsync.spd,x
      beq .next
        jsr HuTrackEngine.Channel.exeFX.hardsync

.next

 rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.Channel.exeFX.semitone.UP

        lda HuTrack.channel.semitoneUP.delta,x
        clc
        adc HuTrack.channel.semitoneUP.cent,x
        sta HuTrack.channel.semitoneUP.cent,x
      bcc .apply
        inc HuTrack.channel.semitoneUP.note,x
        lda HuTrack.channel.semitoneUP.note,x
      cmp HuTrack.channel.semitoneUP.op,x
        bcc .apply
.finished
        stz HuTrack.channel.semitoneUP.op,x

        lda HuTrack.channel.noteCent,x
        sta HuTrack.channel.appliedCent,x
        lda HuTrack.channel.semitoneUP.note,x
        clc
        adc HuTrack.channel.note,x
        cmp #12
      bcc .skip.octave.finished
        inc HuTrack.channel.octave,x
        cla
.skip.octave.finished
        sta HuTrack.channel.note,x
        sta HuTrack.channel.appliedNote,x
        lda HuTrack.channel.octave,x
        adc #$00
        sta HuTrack.channel.octave,x
        sta HuTrack.channel.appliedOctave,x
      bra .out

.apply
        lda HuTrack.channel.noteCent,x
        clc
        adc HuTrack.channel.semitoneUP.cent,x
        sta HuTrack.channel.appliedCent,x
        lda HuTrack.channel.semitoneUP.note,x
        adc HuTrack.channel.note,x
        cmp #12
      bcc .skip.octave.apply
        cla
.skip.octave.apply
        sta HuTrack.channel.appliedNote,x
        lda HuTrack.channel.octave,x
        adc #$00
        sta HuTrack.channel.appliedOctave,x

.out

  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.Channel.exeFX.semitone.DOWN

        lda HuTrack.channel.semitoneDOWN.delta,x
        clc
        adc HuTrack.channel.semitoneDOWN.cent,x
        sta HuTrack.channel.semitoneDOWN.cent,x
      bcc .apply
        inc HuTrack.channel.semitoneDOWN.note,x
        lda HuTrack.channel.semitoneDOWN.note,x
      cmp HuTrack.channel.semitoneDOWN.op,x
        bcc .apply
.finished
        stz HuTrack.channel.semitoneDOWN.op,x

        lda HuTrack.channel.noteCent,x
        sta HuTrack.channel.appliedCent,x
        lda HuTrack.channel.note,x
        sbc HuTrack.channel.semitoneDOWN.note,x
      bcs .skip.octave.finished
        lda #11
.skip.octave.finished
        sta HuTrack.channel.note,x
        sta HuTrack.channel.appliedNote,x
        lda HuTrack.channel.octave,x
        sbc #$00
        sta HuTrack.channel.octave,x
        sta HuTrack.channel.appliedOctave,x
      bra .out

.apply
        lda HuTrack.channel.noteCent,x
        sec
        sbc HuTrack.channel.semitoneDOWN.cent,x
        sta HuTrack.channel.appliedCent,x
        lda HuTrack.channel.note,x
        sbc HuTrack.channel.semitoneDOWN.note,x
      bcs .skip.octave.apply
        lda #11
.skip.octave.apply
        sta HuTrack.channel.appliedNote,x
        lda HuTrack.channel.octave,x
        sbc #$00
        sta HuTrack.channel.appliedOctave,x

.out

  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.Channel.exeFX.vibrato:

        tay
        lda VibratoTable,y
        sta HuTrack.process.temp0
        lda HuTrack.channel.vibrato.scale,x
        sta HuTrack.process.temp1
        jsr HuTrackEngine.8x8mul
        sta HuTrack.channel.vibrato.cent,x

        lda HuTrack.channel.vibrato.idx,x
        clc
        adc HuTrack.channel.vibrato.inc,x
        and #$3f
        sta HuTrack.channel.vibrato.idx,x

.out

  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.Channel.exeFX.volSlideUp:

        lda HuTrack.channel.delay,x
      beq .cont
        dec HuTrack.channel.delay,x
      bra .out

.cont
        lda #$02
        sta HuTrack.channel.delay,x

        lda HuTrack.channel.volSlideUp,x
        clc
        adc HuTrack.channel.directVolume,x
        cmp #$20
      bcc .skip
        lda #$1f
.skip
        sta HuTrack.channel.directVolume,x
        lda #$1f
        sec
        sbc HuTrack.channel.directVolume,x
        sta HuTrack.channel.relativeVolume,x
        lda #$80
        sta HuTrack.channel.lastEnvVolume,x

.out

  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.Channel.exeFX.volSlideDown:

        lda HuTrack.channel.delay,x
      beq .cont
        dec HuTrack.channel.delay,x
      bra .out

.cont
        lda #$02
        sta HuTrack.channel.delay,x

        lda HuTrack.channel.directVolume,x
        sec
        sbc HuTrack.channel.volSlideDown,x
      bcs .skip
        cla
        stz HuTrack.channel.volSlideDown,x      ;// TXray - 5/19/2024: if volume slide down has reached 0 volume, turn off volume slide.
.skip
        sta HuTrack.channel.directVolume,x
        lda #$1f
        sec
        sbc HuTrack.channel.directVolume,x
        sta HuTrack.channel.relativeVolume,x
        lda #$80
        sta HuTrack.channel.lastEnvVolume,x

.out

  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.Channel.exeFX.portaSlideUp:

        lda HuTrack.channel.porta.up.lo,x
        ora HuTrack.channel.porta.up.hi,x
      beq .out

        ; TODO does DDA or noise cancel this, pause this, or allow it to still run without affecting the channel?
        lda HuTrack.channel.pitch.period.lo,x
        clc
        adc HuTrack.channel.porta.up.lo,x
        sta HuTrack.channel.pitch.period.lo,x
        lda HuTrack.channel.pitch.period.hi,x
        adc HuTrack.channel.porta.up.hi,x
        sta HuTrack.channel.pitch.period.hi,x
      bvc .out
      bcs .out
        lda #$ff
        sta HuTrack.channel.pitch.period.lo,x
        sta HuTrack.channel.pitch.period.hi,x
.out

  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.Channel.exeFX.portaSlideDown:

        lda HuTrack.channel.porta.down.lo,x
        ora HuTrack.channel.porta.down.hi,x
      beq .out

        ; TODO does DDA or noise cancel this, pause this, or allow it to still run without affecting the channel?
        lda HuTrack.channel.pitch.period.lo,x
        clc
        adc HuTrack.channel.porta.down.lo,x
        sta HuTrack.channel.pitch.period.lo,x
        lda HuTrack.channel.pitch.period.hi,x
        adc HuTrack.channel.porta.down.hi,x
        sta HuTrack.channel.pitch.period.hi,x
        ; TODO: this works for now, but this needs to be moved into the set frequency proocessing routine
        cmp #$10
      bcc .out
        lda #$0f
        sta HuTrack.channel.pitch.period.lo,x
        lda #$ff
        sta HuTrack.channel.pitch.period.hi,x

.out

  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.Channel.exeFX.overload

;         bit HuTrack.channel.ddaState,x
;       bpl .check.params
;         jmp .out

;         lda HuTrack.channel.noiseMode,x
;       beq .check.params
;         jmp .out

; .exit.out
;         jmp .out

; ; base ..................
; .check.params
;         lda HuTrack.channel.overload.spd,x
;       beq .exit.out
;         lda HuTrack.channel.overload.cntr,x
;       beq .reload.counter
;         dec HuTrack.channel.overload.cntr,x
;         jmp .out

; .reload.counter
;         lda HuTrack.channel.overload.spd,x
;         sta HuTrack.channel.overload.cntr,x
;         dec HuTrack.channel.overload.cntr,x

;         lda HuTrack.channel.overload.accum,x
;         clc
;         adc HuTrack.channel.overload.amt,x
;         sta HuTrack.channel.overload.accum,x

;         lda HuTrack.WfEnvPtr.lo,x
;         sta <HuTrack.A0
;         lda HuTrack.WfEnvPtr.hi,x
;         sta <HuTrack.A0+1

; ; magic!!!
;         lda HuTrack.WfEnv.len,x       ; There's nothing in the waveform macro.. use direct waveform
;       beq .get.direct.waveform

;         lda HuTrack.WfEnv.idx,x
;         cmp HuTrack.WfEnv.len,x
;       bcs .check.loop.reload
; .current.waveform.index
;         tay
;       bra .get.macro.waveform

; .check.loop.reload
;         lda HuTrack.WfEnv.repeat,x
;         cmp #$ff
;       beq .load.last.waveform
;       bra .current.waveform.index


; .get.direct.waveform
;         lda HuTrack.channel.directWaveform,x
;       bra .update.waveform

; .load.last.waveform
;         lda HuTrack.channel.lastEnvWaveform,x
;       bra .update.waveform


; .get.macro.waveform
;         lda [HuTrack.A0],y

; .update.waveform
;         asl a
;         tay

;         lda HuTrack.waveform.table
;         sta <HuTrack.A0
;         lda HuTrack.waveform.table+1
;         sta <HuTrack.A0+1

;         lda [HuTrack.A0],y
;         iny
;         sta <HuTrack.A1
;         lda [HuTrack.A0],y
;         sta <HuTrack.A1+1

;         ; Reset the waveform pointer: TODO this state logic of when to reset the waveform pointer needs to be  more complex.
;         lda HuTrack.channel.proccessState,x
;           sei
;         stx $800
;         sta $804
;         ora #$40
;         sta $804
;         and #$3f
;         sta $804
;           cli
;         lda HuTrack.channel.overload.accum,x
;         sta <HuTrack.FXptr0

;         cly
;           sei
; .loop
;         lda [HuTrack.A1],y
;         clc
;         adc <HuTrack.FXptr0
;         sta $806
;         iny
;         lda [HuTrack.A1],y
;         clc
;         adc <HuTrack.FXptr0
;         sta $806
;         iny
;         lda [HuTrack.A1],y
;         clc
;         adc <HuTrack.FXptr0
;         sta $806
;         iny
;         lda [HuTrack.A1],y
;         clc
;         adc <HuTrack.FXptr0
;         sta $806
;         iny
;         cpy #$20
;       bcc .loop
;         lda HuTrack.channel.proccessState,x
;         sta $804
;         ;jsr HuTrackEngine._htk.WSG.control
;           cli

; .return


.out

  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.Channel.exeFX.corruption

;         bit HuTrack.channel.ddaState,x
;       bpl .check.params
;         jmp .out

;         lda HuTrack.channel.noiseMode,x
;       beq .check.params
;         jmp .out

; .exit.out
;         jmp .out

; ; base ..................
; .check.params
;         lda HuTrack.channel.corruption.spd,x
;       beq .exit.out
;         lda HuTrack.channel.corruption.cntr,x
;       beq .reload.counter
;         dec HuTrack.channel.corruption.cntr,x
;         jmp .out

; .reload.counter
;         lda HuTrack.channel.corruption.spd,x
;         sta HuTrack.channel.corruption.cntr,x
;         dec HuTrack.channel.corruption.cntr,x

;         lda HuTrack.channel.corruption.index,x
;         clc
;         adc HuTrack.channel.corruption.delta,x
;         cmp #$20
;       bcc .skip
;         cla
; .skip
;         sta HuTrack.channel.corruption.index,x

;         lda HuTrack.channel.corruption.wf,x
;         asl a
;         tay

;         lda HuTrack.waveform.table
;         sta <HuTrack.A0
;         lda HuTrack.waveform.table+1
;         sta <HuTrack.A0+1

;         lda [HuTrack.A0],y
;         iny
;         sta <HuTrack.A1
;         lda [HuTrack.A0],y
;         sta <HuTrack.A1+1


;         ldy HuTrack.channel.corruption.index,x

;         lda [HuTrack.A1],y
;           sei
;         stx $800
;         sta $806
;           cli

; .return

.out

  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.Channel.exeFX.hardsync

;         bit HuTrack.channel.ddaState,x
;       bpl .check.params
;         jmp .out

;         lda HuTrack.channel.noiseMode,x
;       beq .check.params
;         jmp .out

; .exit.out
;         jmp .out

; ; base ..................
; .check.params
;         lda HuTrack.channel.hardsync.spd,x
;       beq .exit.out
;         lda HuTrack.channel.hardsync.cntr,x
;       beq .reload.counter
;         dec HuTrack.channel.hardsync.cntr,x
;         jmp .out

; .reload.counter
;         lda HuTrack.channel.hardsync.spd,x
;         and #$07
;         sta HuTrack.channel.hardsync.cntr,x
;         dec HuTrack.channel.hardsync.cntr,x

;         lda HuTrack.channel.hardsync.delta,x
;         clc
;         adc HuTrack.channel.hardsync.amt,x
;         sta HuTrack.channel.hardsync.delta,x


;         lda HuTrack.WfEnvPtr.lo,x
;         sta <HuTrack.A0
;         lda HuTrack.WfEnvPtr.hi,x
;         sta <HuTrack.A0+1

; ; magic!!!
;         lda HuTrack.WfEnv.len,x       ; There's nothing in the waveform macro.. use direct waveform
;       beq .get.direct.waveform

;         lda HuTrack.WfEnv.idx,x
;         cmp HuTrack.WfEnv.len,x
;       bcs .check.loop.reload
; .current.waveform.index
;         tay
;       bra .get.macro.waveform

; .check.loop.reload
;         lda HuTrack.WfEnv.repeat,x
;         cmp #$ff
;       beq .load.last.waveform
;       bra .current.waveform.index


; .get.direct.waveform
;         lda HuTrack.channel.directWaveform,x
;       bra .update.waveform

; .load.last.waveform
;         lda HuTrack.channel.lastEnvWaveform,x
;       bra .update.waveform


; .get.macro.waveform
;         lda [HuTrack.A0],y

; .update.waveform
;         asl a
;         tay

;         lda HuTrack.waveform.table
;         sta <HuTrack.A0
;         lda HuTrack.waveform.table+1
;         sta <HuTrack.A0+1

;         lda [HuTrack.A0],y
;         iny
;         sta <HuTrack.A1
;         lda [HuTrack.A0],y
;         sta <HuTrack.A1+1

;         ; Reset the waveform pointer: TODO this state logic of when to reset the waveform pointer needs to be  more complex.
;         lda HuTrack.channel.proccessState,x
;         and #$3f
;         jsr HuTrackEngine._htk.WSG.control

;         lda HuTrack.channel.hardsync.delta,x
;         sta HuTrack.process.temp0
;         stz HuTrack.process.temp1


;           lda HuTrack.channel.hardsync.spd,x
;           and #$08
;         bne .no.wrap.around

;           sei

; .wrap.around
;           phx
;           ldx #$20
;         cly
; .loop
;         lda [HuTrack.A1],y
;         sta $806
;         lda HuTrack.process.temp1
;         clc
;         adc HuTrack.process.temp0
;         sta HuTrack.process.temp1
;         lsr a
;         lsr a
;         lsr a
;         and #$1f
;         tay
;         dex
;       bne .loop
;         lda HuTrack.channel.proccessState,x
;         sta $804
;         ;jsr HuTrackEngine._htk.WSG.control
;           plx
;           cli
;       jmp .out

; .no.wrap.around
; ;         lda HuTrack.channel.hardsync.delta,x
; ;         lsr a
; ;         lsr a
; ;         lsr a
; ;         cmp HuTrack.channel.hardsync.delta.old,x
; ;       bne .cont
; ;         jmp .out

; ; .cont
; ;         sta HuTrack.channel.hardsync.delta.old,x
;           sei
;           lda #$20
;           sta HuTrack.process.temp2
;         cly
; .no.wrap.loop
;         lda [HuTrack.A1],y

;         sta $806
;         lda HuTrack.process.temp0
;         lsr a
;         lsr a
;         clc
;         adc HuTrack.process.temp1
;         adc #$08
;         sta HuTrack.process.temp1
;         lsr a
;         lsr a
;         lsr a
;         and #$1f
;         tay
;         dec HuTrack.process.temp2
;       bne .no.wrap.loop
;         lda HuTrack.channel.proccessState,x
;         sta $804
;         ;jsr HuTrackEngine._htk.WSG.control
;           cli
;       jmp .out

.out

  rts

;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#





;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Reset state logic routines                                                                              /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.reset.overload:

        stz HuTrack.channel.overload.spd,x
        stz HuTrack.channel.overload.amt,x
        stz HuTrack.channel.overload.accum,x
        stz HuTrack.channel.overload.cntr,x
  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.reset.corruption:

        stz HuTrack.channel.corruption.spd,x
        stz HuTrack.channel.corruption.delta,x
        stz HuTrack.channel.corruption.index,x
        stz HuTrack.channel.corruption.cntr,x
  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.reset.hardsync:

        stz HuTrack.channel.hardsync.spd,x
        stz HuTrack.channel.hardsync.amt,x
        stz HuTrack.channel.hardsync.delta,x
        stz HuTrack.channel.hardsync.cntr,x
  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine._htk.WSG.control:

        bit HuTrack.SFX.inProgress,x
      bmi .out
.cont
          php
          sei
        stx $800
        sta $804
          plp
        sta HuTrack.channel.write.volume,x
.out

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine._htk.WSG.freq:

        bit HuTrack.SFX.inProgress,x
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
.cont

        sta <HuTrack.dda.bank,x

.out

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine._htk.WSG.pan:

        sta HuTrack.channel.panState,x
        bit HuTrack.SFX.inProgress,x
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
; This routine returns just the integer value of a decimal part multiplied by an integer part
; 8:0 x 0:8 -> 8:0
;
; Input:
;        A = HuTrack.process.temp0
;        B = HuTrack.process.temp1
;
; Output:
;       Acc
;
HuTrackEngine.8x8mul:


.square_ptr.pos.hi = HuTrack.FXptr1
.square_ptr.neg.hi = HuTrack.FXptr3


        lda    #high(square_pos_hi)
        sta    <.square_ptr.pos.hi + 1

        lda    #high(square_neg_hi)
        sta    <.square_ptr.neg.hi + 1


        lda HuTrack.process.temp0
        sta    <.square_ptr.pos.hi
        eor    #$FF
        sta    <.square_ptr.neg.hi

        ldy  HuTrack.process.temp1

        sec
        lda    [.square_ptr.pos.hi],y
        sbc    [.square_ptr.neg.hi],y
.out
    rts





;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
;@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#





;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Note conversion tables                                                                                  /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.tables.noteFromCombo

; octave 0
  .db 0
  .db 1
  .db 2
  .db 3
  .db 4
  .db 5
  .db 6
  .db 7
  .db 8
  .db 9
  .db 10
  .db 11

; octave 1
  .db 0
  .db 1
  .db 2
  .db 3
  .db 4
  .db 5
  .db 6
  .db 7
  .db 8
  .db 9
  .db 10
  .db 11

; octave 2
  .db 0
  .db 1
  .db 2
  .db 3
  .db 4
  .db 5
  .db 6
  .db 7
  .db 8
  .db 9
  .db 10
  .db 11

; octave 3
  .db 0
  .db 1
  .db 2
  .db 3
  .db 4
  .db 5
  .db 6
  .db 7
  .db 8
  .db 9
  .db 10
  .db 11

; octave 4
  .db 0
  .db 1
  .db 2
  .db 3
  .db 4
  .db 5
  .db 6
  .db 7
  .db 8
  .db 9
  .db 10
  .db 11

; octave 5
  .db 0
  .db 1
  .db 2
  .db 3
  .db 4
  .db 5
  .db 6
  .db 7
  .db 8
  .db 9
  .db 10
  .db 11

; octave 6
  .db 0
  .db 1
  .db 2
  .db 3
  .db 4
  .db 5
  .db 6
  .db 7
  .db 8
  .db 9
  .db 10
  .db 11

; octave 7
  .db 0
  .db 1
  .db 2
  .db 3
  .db 4
  .db 5
  .db 6
  .db 7
  .db 8
  .db 9
  .db 10
  .db 11

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HuTrackEngine.tables.octaveFromCombo

; octave 0
  .db 0
  .db 0
  .db 0
  .db 0
  .db 0
  .db 0
  .db 0
  .db 0
  .db 0
  .db 0
  .db 0
  .db 0

; octave 1
  .db 1
  .db 1
  .db 1
  .db 1
  .db 1
  .db 1
  .db 1
  .db 1
  .db 1
  .db 1
  .db 1
  .db 1

; octave 2
  .db 2
  .db 2
  .db 2
  .db 2
  .db 2
  .db 2
  .db 2
  .db 2
  .db 2
  .db 2
  .db 2
  .db 2

; octave 3
  .db 3
  .db 3
  .db 3
  .db 3
  .db 3
  .db 3
  .db 3
  .db 3
  .db 3
  .db 3
  .db 3
  .db 3

; octave 4
  .db 4
  .db 4
  .db 4
  .db 4
  .db 4
  .db 4
  .db 4
  .db 4
  .db 4
  .db 4
  .db 4
  .db 4

; octave 5
  .db 5
  .db 5
  .db 5
  .db 5
  .db 5
  .db 5
  .db 5
  .db 5
  .db 5
  .db 5
  .db 5
  .db 5

; octave 6
  .db 6
  .db 6
  .db 6
  .db 6
  .db 6
  .db 6
  .db 6
  .db 6
  .db 6
  .db 6
  .db 6
  .db 6

; octave 7
  .db 7
  .db 7
  .db 7
  .db 7
  .db 7
  .db 7
  .db 7
  .db 7
  .db 7
  .db 7
  .db 7
  .db 7



;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

; Octave 0, Note B
NOTE.base = 1812 * 2

; Octave 1 Notes
NOTE.C    = 3422
NOTE.Cs   = 3230
NOTE.D    = 3048
NOTE.Ds   = 2877
NOTE.E    = 2716
NOTE.F    = 2564
NOTE.Fs   = 2419
NOTE.G    = 2284
NOTE.Gs   = 2155
NOTE.A    = 2034
NOTE.As   = 1920
NOTE.B    = 1812

; Octave 2 Note C
NOTE.upperBase = 3422 / 2


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

BaseNoteFreq.base:
    .dw NOTE.base

BaseNoteFreq:
    .dw NOTE.C
    .dw NOTE.Cs
    .dw NOTE.D
    .dw NOTE.Ds
    .dw NOTE.E
    .dw NOTE.F
    .dw NOTE.Fs
    .dw NOTE.G
    .dw NOTE.Gs
    .dw NOTE.A
    .dw NOTE.As
    .dw NOTE.B


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

NoteCents.table.base:
    .db NOTE.base - NOTE.C

NoteCents.table:
    .db NOTE.C  - NOTE.Cs
    .db NOTE.Cs - NOTE.D
    .db NOTE.D  - NOTE.Ds
    .db NOTE.Ds - NOTE.E
    .db NOTE.E  - NOTE.F
    .db NOTE.F  - NOTE.Fs
    .db NOTE.Fs - NOTE.G
    .db NOTE.G  - NOTE.Gs
    .db NOTE.Gs - NOTE.A
    .db NOTE.A  - NOTE.As
    .db NOTE.As - NOTE.B
    .db NOTE.B  - NOTE.upperBase


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


VibratoTable:

    .dwl     $00,  $19,  $32,  $4A,  $62,  $78,  $8E,  $A2
    .dwl     $B4,  $C5,  $D4,  $E1,  $EC,  $F4,  $FA,  $FE
    .dwl     $FF,  $FE,  $FA,  $F4,  $EC,  $E1,  $D4,  $C5
    .dwl     $B4,  $A2,  $8E,  $78,  $62,  $4A,  $32,  $19
    ; NOTE: Not using 2s complement values because I want the full positive and negative range.
    ;       This lower half is simply subtracted from the noteCent.
    .dwl     $00,  $19,  $32,  $4A,  $62,  $78,  $8E,  $A2
    .dwl     $B4,  $C5,  $D4,  $E1,  $EC,  $F4,  $FA,  $FE
    .dwl     $FF,  $FE,  $FA,  $F4,  $EC,  $E1,  $D4,  $C5
    .dwl     $B4,  $A2,  $8E,  $78,  $62,  $4A,  $32,  $19


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


VibratoScaleTable:

  .db $00, $11, $22, $33, $44, $55, $66, $77
  .db $88, $99, $AA, $BB, $CC, $DD, $EE ,$FF

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    ; NOTE: Changed A to $1E because apparently $1F is an illegal values???
SampleNumDecode:
NoiseTable:
    ;   C, C#,  D, D#,  E,  F, F#,  G, G#,  A, A#,  B
  .db    $84,$8D,$8F,$92,$95,$97,$99,$9B,$9D,$9E,$81,$83

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

NoiseVolumeAdjust
  .ifdef HUTRACK_OLD_NOISE_VOL
  .if HUTRACK_OLD_NOISE_VOL == 1
    .db $00,$00,$00
  .endif
  .endif
  .db $00,$01,$02,$03,$04,$05,$06,$07,$08,$09,$0a,$0b,$0c,$0d,$0e,$0f
  .db $10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$1a,$1b,$1c,$1d,$1e,$1f


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    HuTrack.AlignByte256
      ;.ds    256 - (* & 255)


square_pos_hi:
    .db    $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
    .db    $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
    .db    $01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$02,$02
    .db    $02,$02,$02,$02,$02,$02,$02,$02,$03,$03,$03,$03,$03,$03,$03,$03
    .db    $04,$04,$04,$04,$04,$04,$04,$04,$05,$05,$05,$05,$05,$05,$05,$06
    .db    $06,$06,$06,$06,$06,$07,$07,$07,$07,$07,$07,$08,$08,$08,$08,$08
    .db    $09,$09,$09,$09,$09,$09,$0A,$0A,$0A,$0A,$0A,$0B,$0B,$0B,$0B,$0C
    .db    $0C,$0C,$0C,$0C,$0D,$0D,$0D,$0D,$0E,$0E,$0E,$0E,$0F,$0F,$0F,$0F
    .db    $10,$10,$10,$10,$11,$11,$11,$11,$12,$12,$12,$12,$13,$13,$13,$13
    .db    $14,$14,$14,$15,$15,$15,$15,$16,$16,$16,$17,$17,$17,$18,$18,$18
    .db    $19,$19,$19,$19,$1A,$1A,$1A,$1B,$1B,$1B,$1C,$1C,$1C,$1D,$1D,$1D
    .db    $1E,$1E,$1E,$1F,$1F,$1F,$20,$20,$21,$21,$21,$22,$22,$22,$23,$23
    .db    $24,$24,$24,$25,$25,$25,$26,$26,$27,$27,$27,$28,$28,$29,$29,$29
    .db    $2A,$2A,$2B,$2B,$2B,$2C,$2C,$2D,$2D,$2D,$2E,$2E,$2F,$2F,$30,$30
    .db    $31,$31,$31,$32,$32,$33,$33,$34,$34,$35,$35,$35,$36,$36,$37,$37
    .db    $38,$38,$39,$39,$3A,$3A,$3B,$3B,$3C,$3C,$3D,$3D,$3E,$3E,$3F,$3F
    .db    $40,$40,$41,$41,$42,$42,$43,$43,$44,$44,$45,$45,$46,$46,$47,$47
    .db    $48,$48,$49,$49,$4A,$4A,$4B,$4C,$4C,$4D,$4D,$4E,$4E,$4F,$4F,$50
    .db    $51,$51,$52,$52,$53,$53,$54,$54,$55,$56,$56,$57,$57,$58,$59,$59
    .db    $5A,$5A,$5B,$5C,$5C,$5D,$5D,$5E,$5F,$5F,$60,$60,$61,$62,$62,$63
    .db    $64,$64,$65,$65,$66,$67,$67,$68,$69,$69,$6A,$6A,$6B,$6C,$6C,$6D
    .db    $6E,$6E,$6F,$70,$70,$71,$72,$72,$73,$74,$74,$75,$76,$76,$77,$78
    .db    $79,$79,$7A,$7B,$7B,$7C,$7D,$7D,$7E,$7F,$7F,$80,$81,$82,$82,$83
    .db    $84,$84,$85,$86,$87,$87,$88,$89,$8A,$8A,$8B,$8C,$8D,$8D,$8E,$8F
    .db    $90,$90,$91,$92,$93,$93,$94,$95,$96,$96,$97,$98,$99,$99,$9A,$9B
    .db    $9C,$9D,$9D,$9E,$9F,$A0,$A0,$A1,$A2,$A3,$A4,$A4,$A5,$A6,$A7,$A8
    .db    $A9,$A9,$AA,$AB,$AC,$AD,$AD,$AE,$AF,$B0,$B1,$B2,$B2,$B3,$B4,$B5
    .db    $B6,$B7,$B7,$B8,$B9,$BA,$BB,$BC,$BD,$BD,$BE,$BF,$C0,$C1,$C2,$C3
    .db    $C4,$C4,$C5,$C6,$C7,$C8,$C9,$CA,$CB,$CB,$CC,$CD,$CE,$CF,$D0,$D1
    .db    $D2,$D3,$D4,$D4,$D5,$D6,$D7,$D8,$D9,$DA,$DB,$DC,$DD,$DE,$DF,$E0
    .db    $E1,$E1,$E2,$E3,$E4,$E5,$E6,$E7,$E8,$E9,$EA,$EB,$EC,$ED,$EE,$EF
    .db    $F0,$F1,$F2,$F3,$F4,$F5,$F6,$F7,$F8,$F9,$FA,$FB,$FC,$FD,$FE,$FF


square_neg_hi:
    .db    $3F,$3F,$3E,$3E,$3D,$3D,$3C,$3C,$3B,$3B,$3A,$3A,$39,$39,$38,$38
    .db    $37,$37,$36,$36,$35,$35,$35,$34,$34,$33,$33,$32,$32,$31,$31,$31
    .db    $30,$30,$2F,$2F,$2E,$2E,$2D,$2D,$2D,$2C,$2C,$2B,$2B,$2B,$2A,$2A
    .db    $29,$29,$29,$28,$28,$27,$27,$27,$26,$26,$25,$25,$25,$24,$24,$24
    .db    $23,$23,$22,$22,$22,$21,$21,$21,$20,$20,$1F,$1F,$1F,$1E,$1E,$1E
    .db    $1D,$1D,$1D,$1C,$1C,$1C,$1B,$1B,$1B,$1A,$1A,$1A,$19,$19,$19,$19
    .db    $18,$18,$18,$17,$17,$17,$16,$16,$16,$15,$15,$15,$15,$14,$14,$14
    .db    $13,$13,$13,$13,$12,$12,$12,$12,$11,$11,$11,$11,$10,$10,$10,$10
    .db    $0F,$0F,$0F,$0F,$0E,$0E,$0E,$0E,$0D,$0D,$0D,$0D,$0C,$0C,$0C,$0C
    .db    $0C,$0B,$0B,$0B,$0B,$0A,$0A,$0A,$0A,$0A,$09,$09,$09,$09,$09,$09
    .db    $08,$08,$08,$08,$08,$07,$07,$07,$07,$07,$07,$06,$06,$06,$06,$06
    .db    $06,$05,$05,$05,$05,$05,$05,$05,$04,$04,$04,$04,$04,$04,$04,$04
    .db    $03,$03,$03,$03,$03,$03,$03,$03,$02,$02,$02,$02,$02,$02,$02,$02
    .db    $02,$02,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01
    .db    $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
    .db    $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
    .db    $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
    .db    $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01
    .db    $01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$02,$02,$02
    .db    $02,$02,$02,$02,$02,$02,$02,$03,$03,$03,$03,$03,$03,$03,$03,$04
    .db    $04,$04,$04,$04,$04,$04,$04,$05,$05,$05,$05,$05,$05,$05,$06,$06
    .db    $06,$06,$06,$06,$07,$07,$07,$07,$07,$07,$08,$08,$08,$08,$08,$09
    .db    $09,$09,$09,$09,$09,$0A,$0A,$0A,$0A,$0A,$0B,$0B,$0B,$0B,$0C,$0C
    .db    $0C,$0C,$0C,$0D,$0D,$0D,$0D,$0E,$0E,$0E,$0E,$0F,$0F,$0F,$0F,$10
    .db    $10,$10,$10,$11,$11,$11,$11,$12,$12,$12,$12,$13,$13,$13,$13,$14
    .db    $14,$14,$15,$15,$15,$15,$16,$16,$16,$17,$17,$17,$18,$18,$18,$19
    .db    $19,$19,$19,$1A,$1A,$1A,$1B,$1B,$1B,$1C,$1C,$1C,$1D,$1D,$1D,$1E
    .db    $1E,$1E,$1F,$1F,$1F,$20,$20,$21,$21,$21,$22,$22,$22,$23,$23,$24
    .db    $24,$24,$25,$25,$25,$26,$26,$27,$27,$27,$28,$28,$29,$29,$29,$2A
    .db    $2A,$2B,$2B,$2B,$2C,$2C,$2D,$2D,$2D,$2E,$2E,$2F,$2F,$30,$30,$31
    .db    $31,$31,$32,$32,$33,$33,$34,$34,$35,$35,$35,$36,$36,$37,$37,$38
    .db    $38,$39,$39,$3A,$3A,$3B,$3B,$3C,$3C,$3D,$3D,$3E,$3E,$3F,$3F,$40


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


