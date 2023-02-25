
;TODO: Need to fix the name of these ZP vars for namespace collision

    .zp

_hk.R1:        .ds 2
_hk.A0:        .ds 2
_hk.A1:        .ds 2

_hk.A2:        .ds 2
_hk.D0:        .ds 2

_hk.EAX0:      .ds 4


_hk.A0.l  .equ  _hk.A0
_hk.A0.h  .equ  _hk.A0+1
_hk.A1.l  .equ  _hk.A1
_hk.A1.h  .equ  _hk.A1+1
_hk.A2.l  .equ  _hk.A2
_hk.A2.h  .equ  _hk.A2+1

_hk.D0.l  .equ  _hk.D0
_hk.D0.h  .equ  _hk.D0+1
_hk.R1.l  .equ  _hk.R1
_hk.R1.h  .equ  _hk.R1+1


_hk.EAX0.l = _hk.EAX0
_hk.EAX0.m = _hk.EAX0+1
_hk.EAX0.h = _hk.EAX0+2
_hk.EAX0.u = _hk.EAX0+3



      .zp
HuTrack.DDAprocess:                 .ds 1
HuTrack.dda.bank:                   .ds (1* 6)
HuTrack.dda.addr.lo:                .ds (1* 6)
HuTrack.dda.addr.hi:                .ds (1* 6)
HuTrack.dda.loop.bank:              .ds (1* 6)
HuTrack.dda.addr.loop.lo:           .ds (1* 6)
HuTrack.dda.addr.loop.hi:           .ds (1* 6)
HuTrack.dda.ptr:                    .ds 2
HuTrack.dda.cntr0:                  .ds (1* 6)
HuTrack.dda.cntr1:                  .ds (1* 6)

HuTrack.dda.trackUsage:             .ds 1

HuTrack.Status:                     .ds 1
      .bss

HuTrack.returnVec:                  .ds 2

; Song list
song_bank:                          .ds 64
song_ptr.lo:                        .ds 64
song_ptr.hi:                        .ds 64
song_slot:                          .ds 1
; Current to play or is playing
current_song:                       .ds 1

song_repeat:                        .ds 1



HuTrack.channel.noiseST.backup:     .ds (1* 6)
HuTrack.channel.ddaST.backup:       .ds (1* 6)
HuTrack.channel.pcmIDX.backup:      .ds (1* 6)
HuTrack.channel.instr.backup:       .ds (1* 6)
HuTrack.channel.dVol.backup:        .ds (1* 6)
HuTrack.channel.rVol.backup:        .ds (1* 6)
HuTrack.channel.note.backup:        .ds (1* 6)


;,,,,,,,,,,,,,,,,,,,,,,,,,,.....................
HuTrack.Global.SetVolume:           .ds 1
HuTrack.Global.VolUpdate:           .ds 1

HuTrackEngine.VarStart

HuTrack.tick:                       .ds 1
HuTrack.tickReload:                 .ds 2
HuTrack.TickIdx:                    .ds 1

HuTrack.songName:                   .ds 48
HuTrack.songAuthor:                 .ds 48

HuTrack.rowLen:                     .ds 1
HuTrack.patternListlen:             .ds 1
HuTrack.instrLen:                   .ds 1
HuTrack.waveformLen:                .ds 1
HuTrack.sampleListLen:              .ds 1

HuTrack.channel.patternList.table:  .ds 2 * 6

HuTrack.pattern.table:              .ds 2
HuTrack.instr.table:                .ds 2
HuTrack.waveform.table:             .ds 2
HuTrack.samples.table:              .ds 2

HuTrack.patternList.table.bank:     .ds 1
HuTrack.pattern.table.bank:         .ds 1
HuTrack.instr.table.bank:           .ds 1
HuTrack.waveform.table.bank:        .ds 1
HuTrack.samples.table.bank:         .ds 1

HuTrack.channel.pattern.num:        .ds (1* 6)
HuTrack.channel.pattern.idx:        .ds (1* 6)

HuTrack.current.channel:            .ds 1

HuTrack.channel.pcmIndex:           .ds (1* 6)
HuTrack.channel.noisePeriod:        .ds (1* 6)
HuTrack.channel.appliedNoise:       .ds (1* 6)
HuTrack.channel.appliedCent:        .ds (1* 6)
HuTrack.channel.appliedNote:        .ds (1* 6)
HuTrack.channel.appliedOctave:      .ds (1* 6)
HuTrack.channel.noiseMode:          .ds (1* 6)
HuTrack.channel.detune:             .ds (1* 6)
HuTrack.channel.octave:             .ds (1* 6)
HuTrack.channel.note:               .ds (1* 6)
HuTrack.channel.noteCent:           .ds (1* 6)
HuTrack.channel.relativeVolume:     .ds (1* 6)
HuTrack.channel.directVolume:       .ds (1* 6)
HuTrack.channel.directWaveform:     .ds (1* 6)

HuTrack.channel.fx1:                .ds (1* 6)
HuTrack.channel.fx2:                .ds (1* 6)
HuTrack.channel.fx3:                .ds (1* 6)
HuTrack.channel.fx4:                .ds (1* 6)
HuTrack.channel.fxArg1:             .ds (1* 6)
HuTrack.channel.fxArg2:             .ds (1* 6)
HuTrack.channel.fxArg3:             .ds (1* 6)
HuTrack.channel.fxArg4:             .ds (1* 6)
HuTrack.channel.instr:              .ds (1* 6)


;----------------------------------------------
; FX that need to persist over time
HuTrack.channel.semitoneUP.op:      .ds (1* 6)
HuTrack.channel.semitoneUP.delta:   .ds (1* 6)
HuTrack.channel.semitoneUP.note:    .ds (1* 6)
HuTrack.channel.semitoneUP.cent:    .ds (1* 6)
HuTrack.channel.semitoneDOWN.op:    .ds (1* 6)
HuTrack.channel.semitoneDOWN.delta: .ds (1* 6)
HuTrack.channel.semitoneDOWN.note:  .ds (1* 6)
HuTrack.channel.semitoneDOWN.cent:  .ds (1* 6)

HuTrack.channel.porta.up.lo:        .ds (1* 6)
HuTrack.channel.porta.up.hi:        .ds (1* 6)
HuTrack.channel.porta.down.lo:      .ds (1* 6)
HuTrack.channel.porta.down.hi:      .ds (1* 6)

HuTrack.channel.vibrato.mode:       .ds (1* 6)
HuTrack.channel.vibrato.idx:        .ds (1* 6)
HuTrack.channel.vibrato.inc:        .ds (1* 6)
HuTrack.channel.vibrato.scale:      .ds (1* 6)
HuTrack.channel.vibrato.cent:       .ds (1* 6)

HuTrack.channel.noteDelay:          .ds (1* 6)
HuTrack.channel.noteCutDelay:       .ds (1* 6)

HuTrack.channel.pitch.period.lo:    .ds (1* 6)
HuTrack.channel.pitch.period.hi:    .ds (1* 6)

HuTrack.channel.volSlideDown:       .ds (1* 6)
HuTrack.channel.volSlideUp:         .ds (1* 6)
HuTrack.channel.delay:              .ds (1* 6)

HuTrack.channel.overload.spd:       .ds (1* 6)
HuTrack.channel.overload.cntr:      .ds (1* 6)
HuTrack.channel.overload.amt:       .ds (1* 6)
HuTrack.channel.overload.accum:     .ds (1* 6)

HuTrack.channel.corruption.spd:     .ds (1* 6)
HuTrack.channel.corruption.cntr:    .ds (1* 6)
HuTrack.channel.corruption.delta:   .ds (1* 6)
HuTrack.channel.corruption.index:   .ds (1* 6)
HuTrack.channel.corruption.wf:      .ds (1* 6)

HuTrack.channel.hardsync.spd:       .ds (1* 6)
HuTrack.channel.hardsync.cntr:      .ds (1* 6)
HuTrack.channel.hardsync.amt:       .ds (1* 6)
HuTrack.channel.hardsync.delta:     .ds (1* 6)
HuTrack.channel.hardsync.delta.old: .ds (1* 6)

;----------------------------------------------
; Pattern related stuff

HuTrack.channel.rowPos:             .ds (1* 6)
HuTrack.channel.patternOffset.lo:   .ds (1* 6)
HuTrack.channel.patternOffset.hi:   .ds (1* 6)

HuTrack.channel.patternBreak:       .ds 1


HuTrack.channel.waveform.num:       .ds (1* 6)
HuTrack.channel.instr.num:          .ds (1* 6)

HuTrack.channel.change:             .ds (1* 6)       ; TODO check if this really needs to be six entries
HuTrack.channel.update:             .ds 1
HuTrack.channel.update.extFX:       .ds 1
HuTrack.channel.output:             .ds (1* 6)       ; TODO this does NOT need to be 6 entries

HuTrack.channel.temp.noteCent:      .ds (1* 6)
HuTrack.channel.temp.note:          .ds (1* 6)
HuTrack.channel.temp.octave:        .ds (1* 6)
HuTrack.channel.temp.volume:        .ds (1* 6)
HuTrack.channel.temp.fx1:           .ds (1* 6)
HuTrack.channel.temp.fx2:           .ds (1* 6)
HuTrack.channel.temp.fx3:           .ds (1* 6)
HuTrack.channel.temp.fx4:           .ds (1* 6)
HuTrack.channel.temp.fxArg1:        .ds (1* 6)
HuTrack.channel.temp.fxArg2:        .ds (1* 6)
HuTrack.channel.temp.fxArg3:        .ds (1* 6)
HuTrack.channel.temp.fxArg4:        .ds (1* 6)
HuTrack.channel.temp.instr:         .ds (1* 6)

HuTrack.channel.temp.fxArg:         .ds 1
HuTrack.channel.temp.fxNum:         .ds 1

HuTrack.channel.applied.period.lo:  .ds (1* 6)
HuTrack.channel.applied.period.hi:  .ds (1* 6)

HuTrack.VolEnvPtr.lo:               .ds (1* 6)
HuTrack.VolEnvPtr.hi:               .ds (1* 6)
HuTrack.WfEnvPtr.lo:                .ds (1* 6)
HuTrack.WfEnvPtr.hi:                .ds (1* 6)
HuTrack.ArpEnvPtr.lo:               .ds (1* 6)
HuTrack.ArpEnvPtr.hi:               .ds (1* 6)


;----------------------------------------------
; envelope indexes, len, repeat position
HuTrack.VolEnv.idx:                 .ds (1* 6)
HuTrack.WfEnv.idx:                  .ds (1* 6)
HuTrack.ArpEnv.idx:                 .ds (1* 6)

HuTrack.ArpEnv.len:                 .ds (1* 6)
HuTrack.VolEnv.len:                 .ds (1* 6)
HuTrack.WfEnv.len:                  .ds (1* 6)

HuTrack.ArpEnv.repeat:              .ds (1* 6)
HuTrack.VolEnv.repeat:              .ds (1* 6)
HuTrack.WfEnv.repeat:               .ds (1* 6)

HuTrack.channel.lastEnvVolume:      .ds (1* 6)
HuTrack.channel.lastEnvApr:         .ds (1* 6)
HuTrack.channel.lastEnvWaveform:    .ds (1* 6)

HuTrack.ArpEnv.mode:                .ds (1* 6)

HuTrack.channel.proccessState:      .ds (1* 6)

HuTrack.channel.panState:           .ds (1* 6)

HuTrack.SFX.inProgress:             .ds (1* 6)
HuTrack.channel.ddaState:           .ds (1* 6)


HuTrack.entryParse:                 .ds 1
HuTrack.entryParse.extFX:           .ds (1* 6)

HuTrack.channel.rowSkip:            .ds (1* 6)

HuTrack.process.temp0:              .ds 1
HuTrack.process.temp1:              .ds 1
HuTrack.process.temp2:              .ds 1
HuTrack.process.temp3:              .ds 1

    ; Keeps track of how many rows were processed.
HuTrack.rowIncrement:               .ds 1

HuTrack.waveform.buffer:            .ds 32

HuTrackEngine.VarEnd
            ;----------------------------------------------

      .zp
HuTrack.PatternListPtr:             .ds 2
HuTrack.PatterPtr:                  .ds 2
HuTrack.currentPattern:             .ds 2

HuTrack.Enabled:                    .ds (1* 6)

HuTrack.A0:                         .ds 2
HuTrack.A1:                         .ds 2

;used for functions directly
HuTrack.addr0:                      .ds 2
HuTrack.addr1:                      .ds 2


HuTrack.FXptr0:                     .ds 2
HuTrack.FXptr1:                     .ds 2
HuTrack.FXptr2:                     .ds 2
HuTrack.FXptr3:                     .ds 2

      .bss