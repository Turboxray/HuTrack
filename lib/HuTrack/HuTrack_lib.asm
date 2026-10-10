;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
; HuTrack music engine for PC-Engine
;
; \file HuTrack_lib.asm
;
; Ver: 0.1
;
; History:
; -------
;
;
;

    .include "HuTrack/HuTrack_version.inc"



;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Initialize DDA and engine                                                                               /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;#init

HuTrackEngine.Init:

        ; Clear song list
        stz song_slot
        stz HuTrack.DDApaused
        stz HuTrack.sfxAttenuation
        ldx #5
.clear.reservations
        stz HuTrack.SFX.inProgress,x
        dex
      bpl .clear.reservations

        lda #$ff
        sta HuTrack.Global.SetVolume
        stz HuTrack.Global.VolUpdate

        stz <HuTrack.Status

HuTrackEngine.Reset
        smb5 <HuTrack.Status
        smb6 <HuTrack.Status
        lda #$80+$3f
        sta HuTrack.DDAprocess
        stz HuTrackEngine.VarStart
        tii HuTrackEngine.VarStart,HuTrackEngine.VarStart+1, (HuTrackEngine.VarEnd - HuTrackEngine.VarStart) - 1

        ; RAM transfer stub: TIN source,$0806,32 / RTS. Reset cleared the
        ; source and length high byte; waveform uploads patch only the source.
        lda #HuTrack.DMA.TINop
        sta HuTrack.DMA
        lda #$06
        sta HuTrack.DMA+3
        lda #$08
        sta HuTrack.DMA+4
        lda #32
        sta HuTrack.DMA+5
        lda #HuTrack.DMA.RTSop
        sta HuTrack.DMA+7

        ; Set tempo to default
        lda #$05
        sta HuTrack.tick
        sta HuTrack.tickReload      ; Default both tick counter
        sta HuTrack.tickReload+1
        stz HuTrack.TickIdx
        lda #1
        sta HuTrack.P.arpSpeed
        sta HuTrack.P.legacyVolume

        

        lda #$ff
        sta HuTrack.channel.patternBreak ;New tech
        lda HuTrack.Global.SetVolume
        sta $801

        clx
.loop
        stz HuTrack.Enabled,x
        bit HuTrack.SFX.inProgress,x
      bmi .keep.sfx.hardware
        stx $800
        lda #$ff
        sta $805
        lda #$40
        sta $804
        stz $804
        stz $807

        lda #$00
        cly
.clear.wave
        sta $806
        iny
        cpy #32
      bcc .clear.wave

.keep.sfx.hardware
        lda #$80
        sta HuTrack.channel.detune,x
        lda #15
        sta HuTrack.P.vibFine,x
        lda #3
        sta HuTrack.P.volumeFrac,x
        lda #63
        sta HuTrack.P.volumeTail,x
        lda #60
        sta HuTrack.P.anchor,x
        sta HuTrack.P.oldNote,x
        lda #$ff
        sta HuTrack.P.arpStage,x
        lda #$1f
        sta HuTrack.channel.directVolume,x
        sta HuTrack.P.driverVolume,x
        sta HuTrack.P.outputVolume,x
        lda #$ff
        sta HuTrack.channel.instr,x
        lda #$80
        sta HuTrack.channel.vibrato.idx,x

        lda #$00
        sta HuTrack.channel.directWaveform,x
        lda #$ff
        sta HuTrack.channel.lastEnvWaveform,x
        sta HuTrack.channel.uploadedWaveform,x

        bit HuTrack.SFX.inProgress,x
      bmi .keep.sfx.pcm
        lda #$80
        sta <HuTrack.dda.inactive,x
        sta <HuTrack.dda.bank,x
        lda #$8F
        sta <HuTrack.dda.cntr1,x
      bra .pcm.ready
.keep.sfx.pcm
        lda #$80
        sta HuTrack.channel.waitNote,x
        lda <HuTrack.dda.inactive,x
      bmi .pcm.ready
        jsr HuTrackEngine.EnableDDA
.pcm.ready

        lda #$ff
        sta HuTrack.channel.panState,x



        inx
        cpx #$06
      bcs .out
        jmp .loop
.out
  rts


;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Interface                                                                                               /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;interface

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
; Queue up song into playlist.
; input _hk.EAX0
;
HuTrackEngine.QueueSong:

        ldx song_slot
        cpx #64
      bcs .out
        lda <_hk.EAX0.l
        sta song_ptr.lo,x
        lda <_hk.EAX0.m
        sta song_ptr.hi,x
        lda <_hk.EAX0.h
        sta song_bank,x

        inc song_slot
.out
  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
    .include "HuTrack/engine/HuTrack_controls.asm"

; Global PSG volume (music and SFX).
HuTrackEngine.SetVolume:
        sta HuTrack.Global.SetVolume
        lda #$80
        sta HuTrack.Global.VolUpdate
        rts

; Assembly reservation uses EAX0.l; release uses EAX0.u.
HuTrackEngine.setChanForSFX:

        ldx <_hk.EAX0.l
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
HuTrackEngine.chanReleaseSFX:
        ldx <_hk.EAX0.u
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

HuTrackEngine.SfxPcmRequest:
;...............................................
; Input <_hk.EAX0.l     bank#
; Input <_hk.EAX0.m     lsb
; Input <_hk.EAX0.h     msb
; Input <_hk.EAX0.u     chan #
; Raw sample address, without the C API's three-byte header. Always one-shot.
; Carry clear = accepted; carry set = invalid or unreserved channel.

        sec
        ldx <_hk.EAX0.u
        cpx #$06
      bcs .out
        bit HuTrack.SFX.inProgress,x
      bpl .error

        ; No error
        clc
        lda #$80
        sta <HuTrack.dda.cntr0,x
        sta <HuTrack.dda.cntr1,x

        sta <HuTrack.dda.inactive,x
        sta <HuTrack.dda.bank,x
        lda <_hk.EAX0.m
        sta <HuTrack.dda.addr.lo,x
        lda <_hk.EAX0.h
        and #$1f
        ora #$40
        sta <HuTrack.dda.addr.hi,x
          php
          sei
        stx $800
        stz $807
        lda #31
        sec
        sbc HuTrack.sfxAttenuation
        ora #$c0
        sta $804
        lda #$10
        sta $806
        lda <_hk.EAX0.l
        sta <HuTrack.dda.inactive,x
        sta <HuTrack.dda.bank,x
        stz <HuTrack.dda.inactive,x
        jsr HuTrackEngine.EnableDDA
          plp
.out
  rts
.error
        sec
  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.SfxPcmStatus:
;...............................................
; Input <_hk.EAX0.u     chan #
; Carry clear = valid reserved channel; carry set = invalid or unreserved.
; Output EAX0.l = bank, EAX0.m/h = cursor. Read dda.inactive for active/stopped.

        sec
        ldx <_hk.EAX0.u
        cpx #$06
      bcs .out
        bit HuTrack.SFX.inProgress,x
      bpl .error

        ; No error
        clc
        lda <HuTrack.dda.bank,x
        sta <_hk.EAX0.l
        lda <HuTrack.dda.addr.lo,x
        sta <_hk.EAX0.m
        lda <HuTrack.dda.addr.hi,x
        sta <_hk.EAX0.h
.out
  rts
.error
        sec
  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
; Input EAX0.l
HuTrackEngine.playSong:
        lda <_hk.EAX0.l
        cmp song_slot
      bcc .valid
        rts
.valid
        jsr HuTrackEngine.Reset

        lda <_hk.EAX0.m
        sta force_no_repeat

        _htk.MOVE.b <_hk.EAX0.l, REG_X


        _htk.PUSHBANK.4 _htk.PAGE_4000
        lda song_bank,x
        sta HuTrack.song.windowBank
        _htk.MAP_BANK.4 A, _htk.PAGE_4000
        _htk.MOVE.sw song_ptr, REG_X, <_hk.R1
        _htk.LEA.2  #$4000, <_hk.R1

        ;  _hk.R1 now pointing to the six track pointers
        cly
        clx

        _htk.MOVE.w [_hk.R1], <_hk.A0
        lda _hk.A0
        ora _hk.A0+1
      bne .old.header
        ldy #2
        lda [_hk.R1],y
        cmp #1
      beq .banked.header
        ; Unknown format: remain stopped rather than following invalid data.
.invalid.header
        _htk.PULLBANK.4 _htk.PAGE_4000
        rts
.banked.header
        sta HuTrack.song.format
        iny
        lda [_hk.R1],y
        sta HuTrack.F.ptr
        iny
        lda [_hk.R1],y
        sta HuTrack.F.ptr+1
        iny
        lda [_hk.R1],y
        sta HuTrack.F.bank
        _htk.ADD.w #2, <_hk.R1
.old.header
        _htk.ADD.w #$04, <_hk.R1

        ; Consume full strings, retaining at most 47 text bytes in RAM.
        ; Advancing the pointer also handles combined names longer than 255.
        ; Legacy DMF permits 255 bytes per field plus its exported terminator.
        ; Y wraps after 256 reads; reject an unterminated field at that point.
        clx
        cly
.name.loop
        jsr HuTrackEngine.readNameByte
      beq .author
        cpy #0
      beq .invalid.metadata
        cpx #47
      bcs .name.loop
        sta HuTrack.songName,x
        inx
      bra .name.loop
.author
        stz HuTrack.songName,x
        clx
        cly
.author.loop
        jsr HuTrackEngine.readNameByte
      beq .author.end
        cpy #0
      beq .invalid.metadata
        cpx #47
      bcs .author.loop
        sta HuTrack.songAuthor,x
        inx
      bra .author.loop
.author.end
        stz HuTrack.songAuthor,x
        bra .metadata.ready
.invalid.metadata
        stz HuTrack.songName
        stz HuTrack.songAuthor
        jmp .invalid.header
.metadata.ready


.debug001
        lda HuTrack.song.format
      beq .old.attributes
        jsr HuTrack.Bank.attributes
      bra .attributes.begin
.old.attributes
        ; get Pattern table
        _htk.MOVE.w [_hk.A0], <_hk.A1

        _htk.DEBUG_NOP

.attributes.begin
        ; A zero speed prefix marks extended attributes. Old exports start
        ; with a nonzero tick count and retain the Reset compatibility defaults.
        lda [_hk.A1]
      bne .attributes.basic
        _htk.INC.w <_hk.A1
        _htk.MOVE.b [_hk.A1], HuTrack.P.arpSpeed
        _htk.INC.w <_hk.A1
        _htk.MOVE.b [_hk.A1], HuTrack.P.legacyVolume
        _htk.INC.w <_hk.A1
.attributes.basic
        _htk.MOVE.b [_hk.A1], HuTrack.tickReload+1
        _htk.INC.w <_hk.A1
        _htk.MOVE.b [_hk.A1], HuTrack.tickReload
        _htk.INC.w <_hk.A1
        _htk.MOVE.b [_hk.A1], HuTrack.rowLen
        _htk.INC.w <_hk.A1
        _htk.MOVE.b [_hk.A1], HuTrack.patternListlen
        _htk.INC.w <_hk.A1
        _htk.MOVE.b [_hk.A1], HuTrack.instrLen
        _htk.INC.w <_hk.A1
        _htk.MOVE.b [_hk.A1], HuTrack.waveformLen
        _htk.INC.w <_hk.A1
        _htk.MOVE.b [_hk.A1], HuTrack.sampleListLen

        _htk.MOVE.b HuTrack.tickReload, HuTrack.tick
        stz HuTrack.TickIdx

        lda HuTrack.song.format
      beq .old.lists
        jsr HuTrack.Bank.loadLists
        jmp .song.loaded
.old.lists

        _htk.DEBUG_NOP

        ; get PatternList table
        _htk.ADD.w #$02, <_hk.A0
        _htk.MOVE.w [_hk.A0], <_hk.A1
        cly
.patternLists
        lda [_hk.A1],y
        sta HuTrack.channel.patternList.table,y
        iny
        cpy #12
      bcc .patternLists

        _htk.DEBUG_NOP

        ; get instrument table
        _htk.ADD.w #$02, <_hk.A0
        _htk.MOVE.w [_hk.A0], HuTrack.instr.table

        _htk.DEBUG_NOP

        ; get waveform table
        _htk.ADD.w #$02, <_hk.A0
        _htk.MOVE.w [_hk.A0], HuTrack.waveform.table

        _htk.DEBUG_NOP

        ; get pattern table
        _htk.ADD.w #$02, <_hk.A0
        _htk.MOVE.w [_hk.A0], HuTrack.pattern.table

        _htk.DEBUG_NOP

        ; get samples table
        _htk.ADD.w #$02, <_hk.A0
        _htk.MOVE.w [_hk.A0], HuTrack.samples.table


        _htk.DEBUG_NOP


        ; get bank table
        _htk.ADD.w #$02, <_hk.A0    ; skip past the last ptr (sample)

        _htk.INC.w <_hk.A0    ; Attributes were already read through the song window.

        ; Legacy pattern-list bank is unused: use the song window mapping.
        _htk.INC.w <_hk.A0
        _htk.MOVE.b [_hk.A0], HuTrack.instr.table.bank
        _htk.INC.w <_hk.A0
        _htk.MOVE.b [_hk.A0], HuTrack.waveform.table.bank
        _htk.INC.w <_hk.A0
        ; Legacy pattern bank is likewise represented by the song window.
        _htk.INC.w <_hk.A0
        _htk.MOVE.b [_hk.A0], HuTrack.samples.table.bank


.song.loaded
        ; Reset stopped music PCM and preserved any reserved SFX PCM.
        lda #1
        sta HuTrack.playbackState
        rmb6 <HuTrack.Status     ; start song

        _htk.PULLBANK.4 _htk.PAGE_4000
  rts



; Return the next metadata byte, advancing the pointer and Y's read count.
; Z reports whether the byte is NUL, not whether the counter wrapped.
HuTrackEngine.readNameByte:
        lda [_hk.R1]
        _htk.INC.w <_hk.R1
        iny
        ora #0
        rts
