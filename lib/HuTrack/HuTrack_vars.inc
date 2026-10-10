
; \file HuTrack_vars.inc
; Shared _hk registers are the assembly interface scratch registers.
HUTRACK_SFX_VOLUME = 1

    .zp

_hk.R1:        .ds 2
_hk.A0:        .ds 2
_hk.A1:        .ds 2


_hk.EAX0:      .ds 4


_hk.A0.l  .equ  _hk.A0
_hk.A0.h  .equ  _hk.A0+1
_hk.A1.l  .equ  _hk.A1
_hk.A1.h  .equ  _hk.A1+1

_hk.R1.l  .equ  _hk.R1
_hk.R1.h  .equ  _hk.R1+1


_hk.EAX0.l = _hk.EAX0
_hk.EAX0.m = _hk.EAX0+1
_hk.EAX0.h = _hk.EAX0+2
_hk.EAX0.u = _hk.EAX0+3



      .zp

HuTrack.DDAprocess:                 .ds 1
HuTrack.dda.inactive:               .ds (1* 6) ; $80 stopped, zero active; bank is a full byte
HuTrack.dda.bank:                   .ds (1* 6)
HuTrack.dda.addr.lo:                .ds (1* 6)
HuTrack.dda.addr.hi:                .ds (1* 6)
HuTrack.dda.loop.bank:              .ds (1* 6)
HuTrack.dda.addr.loop.lo:           .ds (1* 6)
HuTrack.dda.addr.loop.hi:           .ds (1* 6)
HuTrack.dda.ptr:                    .ds 2
HuTrack.dda.cntr0:                  .ds (1* 6)
HuTrack.dda.cntr1:                  .ds (1* 6)


HuTrack.Status:                     .ds 1
      .bss

HuTrack.returnVec:                  .ds 2

; Song list
song_bank:                          .ds 64
song_ptr.lo:                        .ds 64
song_ptr.hi:                        .ds 64
song_slot:                          .ds 1

force_no_repeat:                    .ds 1 ; PlayOnce policy

HuTrack.DDApaused:                  .ds 1 ; explicit global PCM suspension
HuTrack.sfxAttenuation:             .ds 1 ; SFX group level survives song changes




;,,,,,,,,,,,,,,,,,,,,,,,,,,.....................
HuTrack.Global.SetVolume:           .ds 1
HuTrack.Global.VolUpdate:           .ds 1

; Reservations survive a song change; Init explicitly clears them.
HuTrack.SFX.inProgress:             .ds 6

HuTrackEngine.VarStart
HuTrack.playbackState:              .ds 1 ; 0 stopped, 1 playing, 2 paused, 3 ended
HuTrack.endPending:                 .ds 1 ; finish after the final row's ticks
HuTrack.musicAttenuation:           .ds 1 ; subtract 0..31 from final music volume
HuTrack.fadeTarget:                 .ds 1 ; target attenuation
HuTrack.fadeInterval:               .ds 1 ; zero = no active fade
HuTrack.fadeCounter:                .ds 1
HuTrack.fadeAction:                 .ds 1 ; 0 hold, 1 stop, 2 pause
HuTrack.pauseDDA:                   .ds 6 ; per-music-channel PCM state

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

HuTrack.instr.table.bank:           .ds 1
HuTrack.waveform.table.bank:        .ds 1
HuTrack.samples.table.bank:         .ds 1
; Bank mapped at $4000 for the song's original assembled pointer window.
; A table may itself be in a later bank without changing this mapping base.
HuTrack.song.windowBank:            .ds 1
HuTrack.song.format:                .ds 1
HuTrack.song.tables:                .ds 18
HuTrack.channel.patternList.bank:   .ds 6
HuTrack.channel.patternTable.lo:    .ds 6
HuTrack.channel.patternTable.hi:    .ds 6
HuTrack.channel.patternTable.bank:  .ds 6
HuTrack.VolEnv.bank:                .ds 6
HuTrack.ArpEnv.bank:                .ds 6
HuTrack.WfEnv.bank:                 .ds 6
HuTrack.F.bank:                     .ds 1
HuTrack.F.record:                   .ds 3
HuTrack.F.offset:                   .ds 2
HuTrack.F.value:                    .ds 2

HuTrack.channel.pattern.num:        .ds (1* 6)
HuTrack.channel.pattern.idx:        .ds (1* 6)

HuTrack.current.channel:            .ds 1

HuTrack.channel.pcmIndex:           .ds (1* 6)
HuTrack.channel.appliedNoise:       .ds (1* 6)
HuTrack.channel.noiseMode:          .ds (1* 6)
HuTrack.channel.detune:             .ds (1* 6)
HuTrack.channel.octave:             .ds (1* 6)
HuTrack.channel.note:               .ds (1* 6)
HuTrack.channel.directVolume:       .ds (1* 6)
HuTrack.channel.directWaveform:     .ds (1* 6)

HuTrack.channel.instr:              .ds (1* 6)


;----------------------------------------------
; FX that need to persist over time


HuTrack.channel.vibrato.mode:       .ds (1* 6)
HuTrack.channel.vibrato.idx:        .ds (1* 6)
HuTrack.channel.vibrato.inc:        .ds (1* 6)



; Released Furnace legacy pitch/effect state (periods before fine tune).
HuTrack.P.anchor:                  .ds 6
HuTrack.P.oldNote:                 .ds 6
HuTrack.P.baseLo:                  .ds 6
HuTrack.P.baseHi:                  .ds 6
HuTrack.P.basis:                   .ds 6
HuTrack.P.unbentLo:                .ds 6
HuTrack.P.unbentHi:                .ds 6
HuTrack.M.octave:                  .ds 1
HuTrack.M.note:                    .ds 1
HuTrack.P.target:                  .ds 6
HuTrack.P.speed:                   .ds 6
HuTrack.P.mode:                    .ds 6
HuTrack.P.inPorta:                 .ds 6
HuTrack.P.lastPorta:               .ds 6
HuTrack.P.lastVib:                 .ds 6
HuTrack.P.vibDepth:                .ds 6
HuTrack.P.vibFine:                 .ds 6
HuTrack.P.arp:                     .ds 6
HuTrack.P.arpStage:                .ds 6
HuTrack.P.arpTicks:                .ds 6
HuTrack.P.volumeFrac:              .ds 6
HuTrack.P.legacyVolume:             .ds 1
HuTrack.P.driverVolume:             .ds 6
HuTrack.P.outputVolume:             .ds 6
HuTrack.P.volumeTail:               .ds 6
HuTrack.P.arpYield:                 .ds 6
HuTrack.P.arpSpeed:                .ds 1
HuTrack.P.lastSlide:               .ds 1
HuTrack.P.trigger:                 .ds 1
HuTrack.P.shortRow:                .ds 1
HuTrack.P.globalPitch:             .ds 4
HuTrack.P.divisor:                 .ds 4
HuTrack.M.a:                       .ds 4
HuTrack.M.b:                       .ds 4
HuTrack.M.p:                       .ds 4
HuTrack.M.r:                       .ds 4
HuTrack.M.pitch:                   .ds 2
HuTrack.M.index:                   .ds 1
HuTrack.M.delta:                   .ds 1
HuTrack.M.sign:                    .ds 1
HuTrack.P.tremDepth:               .ds 6
HuTrack.P.tremRate:                .ds 6
HuTrack.P.tremPhase:               .ds 6
HuTrack.P.tremAttenuation:         .ds 6
HuTrack.P.retrigSpeed:             .ds 6
HuTrack.P.retrigTick:              .ds 6
HuTrack.P.sampleBank:              .ds 1
HuTrack.P.lfoMode:                 .ds 1
HuTrack.P.lfoSpeed:                .ds 1
HuTrack.externalValue:             .ds 1
HuTrack.externalPending:           .ds 1
HuTrack.P.rowDelay:                .ds 6
HuTrack.P.pendingChange:           .ds 6
HuTrack.P.pendingExt:              .ds 6
HuTrack.P.cutTick:                 .ds 6
HuTrack.P.rowTicks:                .ds 1
HuTrack.P.legato:                  .ds 6
HuTrack.P.legatoTick:              .ds 6
HuTrack.P.legatoDelta:             .ds 6
HuTrack.P.random:                  .ds 1
HuTrack.P.dirty:                   .ds 6

HuTrack.channel.volSlideDown:       .ds (1* 6)
HuTrack.channel.volSlideUp:         .ds (1* 6)




;----------------------------------------------
; Pattern related stuff

HuTrack.channel.rowPos:             .ds (1* 6)
HuTrack.channel.patternOffset.lo:   .ds (1* 6)
HuTrack.channel.patternOffset.hi:   .ds (1* 6)

HuTrack.channel.patternBreak:       .ds 1
HuTrack.breakRow:                   .ds 1
HuTrack.channel.seekRemaining:      .ds 6



HuTrack.channel.change:             .ds (1* 6)
HuTrack.channel.update:             .ds 1
HuTrack.channel.update.extFX:       .ds 1
HuTrack.channel.output:             .ds (1* 6)

HuTrack.channel.temp.note:          .ds (1* 6)
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

HuTrack.channel.current.fxArg:      .ds 1

HuTrack.channel.write.volume:       .ds (1* 6)


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
HuTrack.ArpEnv.finished:            .ds 6
HuTrack.ArpEnv.idx:                 .ds (1* 6)

HuTrack.ArpEnv.len:                 .ds (1* 6)
HuTrack.VolEnv.len:                 .ds (1* 6)
HuTrack.WfEnv.len:                  .ds (1* 6)

HuTrack.ArpEnv.repeat:              .ds (1* 6)
HuTrack.VolEnv.repeat:              .ds (1* 6)
HuTrack.WfEnv.repeat:               .ds (1* 6)

HuTrack.channel.lastEnvWaveform:    .ds (1* 6)

HuTrack.ArpEnv.mode:                .ds (1* 6)

HuTrack.channel.proccessState:      .ds (1* 6)

HuTrack.channel.panState:           .ds (1* 6)

; Released channels stay silent until the next actual music note.
HuTrack.channel.waitNote:           .ds (1* 6)
; Hardware cache is separate from the desired/held envelope waveform.
HuTrack.channel.uploadedWaveform:   .ds (1* 6)
HuTrack.channel.ddaState:           .ds (1* 6)


HuTrack.entryParse:                 .ds 1
HuTrack.entryParse.extFX:           .ds 1

HuTrack.channel.rowSkip:            .ds (1* 6)

HuTrack.process.temp0:              .ds 1
HuTrack.process.temp1:              .ds 1
HuTrack.process.temp2:              .ds 1

    ; Keeps track of how many rows were processed.
HuTrack.rowIncrement:               .ds 1

            ;-----------------------------------------------
HuTrack.DMA:                        .ds (1+2+2+2+1)   ; RAM TIN source,$0806,32 / RTS; initialized by Reset.

HuTrack.DMA.TINop = $D3
HuTrack.DMA.RTSop = $60

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


HuTrack.FXptr0:                     .ds 2
HuTrack.FXptr1:                     .ds 2
HuTrack.FXptr3:                     .ds 2
HuTrack.F.ptr:                      .ds 2

      .bss
