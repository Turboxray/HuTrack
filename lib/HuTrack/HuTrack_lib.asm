;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
; HuTrack music engine for PC-Engine
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

        lda #$ff
        sta HuTrack.Global.SetVolume
        stz HuTrack.Global.VolUpdate

        stz <HuTrack.Status

HuTrackEngine.Reset

        ;#TODO this ultimately needs to change. But for now, starting a new song
        smb5 <HuTrack.Status
        ; Stop parsing songs
        smb6 <HuTrack.Status

        ; Disable playback of samples
        lda #$80+$3f
        sta HuTrack.DDAprocess


        ; Set tempo to default
        lda #$05
        sta HuTrack.tick
        sta HuTrack.tickReload      ; Default both tick counter
        sta HuTrack.tickReload+1
        stz HuTrack.TickIdx

        stz HuTrack.channel.patternBreak

        lda #$ff
        sta $801

        clx
.loop
        stx $800
        lda #$ff
        sta $805
        lda #$9f
        sta $804
        lda #$df
        sta $804
        lda #$9f
        sta $804
        stz $804
        stz $807

        lda #$00
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806

        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806
        sta $806

        lda #$80
        sta HuTrack.channel.detune,x
        stz HuTrack.channel.relativeVolume,x
        lda #$1f
        stz HuTrack.channel.directVolume,x
        lda #$ff
        sta HuTrack.channel.instr,x
        lda #$80
        sta HuTrack.channel.vibrato.idx,x
        stz HuTrack.Enabled,x

        lda #$00
        sta HuTrack.channel.directWaveform,x
        lda #$ff
        sta HuTrack.channel.lastEnvWaveform,x

        lda #$80
        sta <HuTrack.dda.bank,x

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
        lda <_hk.EAX0.l
        sta song_ptr.lo,x
        lda <_hk.EAX0.m
        sta song_ptr.hi,x
        lda <_hk.EAX0.h
        sta song_bank,x

        inc song_slot

  rts


;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.pause:

        smb6 <HuTrack.Status

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.FadeToPause:

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.FadeOut:

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.FadeIn:

;         cmp #$20
;       bcc .skip
;         lda #$1f
; .skip
;         ora #$80
;         sta HuTrackEngine.FadeToLevel
  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.SetVolume:
        sta HuTrack.Global.SetVolume
        lda #$80
        sta HuTrack.Global.VolUpdate
  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.stop:

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.Continue:

        rmb6 <HuTrack.Status

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.FadeToContinue:

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.SaveSongPosition:

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
;
HuTrackEngine.LoadSongPosition:

  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
; Input EAX0.l
HuTrackEngine.playSong:

        stz HuTrackEngine.VarStart
        tii HuTrackEngine.VarStart,HuTrackEngine.VarStart+1, (HuTrackEngine.VarEnd - HuTrackEngine.VarStart) - 1

        jsr HuTrackEngine.Reset

        lda <_hk.EAX0.m
        sta song_repeat

        _htk.MOVE.b <_hk.EAX0.l, current_song
        _htk.MOVE.b <_hk.EAX0.l, REG_X


        _htk.PUSHBANK.4 _htk.PAGE_4000
        _htk.MAP_BANK.4 song_bank,x , _htk.PAGE_4000
        _htk.MOVE.sw song_ptr, REG_X, <_hk.R1
        _htk.LEA.2  #$4000, <_hk.R1

        ;  _hk.R1 now pointing to the six track pointers
        cly
        clx

        _htk.MOVE.w [_hk.R1], <_hk.A0
        _htk.ADD.w #$04, <_hk.R1

        ; copy over the song and author names
        cly
        clx
.name.loop
        lda [_hk.R1],y
      beq .author
        iny
        sta HuTrack.songName,x
        inx
        cpx #47
      bne .name.loop
.author
        iny
        stz HuTrack.songName,x

        clx
.author.loop
        lda [_hk.R1],y
      beq .author.end
        iny
        sta HuTrack.songAuthor,x
        inx
        cpx #47
      bne .author.loop
.author.end
        stz HuTrack.songAuthor,x


.debug001
        ; get Pattern table
        _htk.MOVE.w [_hk.A0], <_hk.A1

        _htk.DEBUG_NOP

        ; get attributes..
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


        _htk.DEBUG_NOP

        ; get PatternList table
        _htk.ADD.w #$02, <_hk.A0
        _htk.MOVE.w [_hk.A0], <_hk.A1
        _htk.MOVE.w [_hk.A1], HuTrack.channel.patternList.table + 0
        _htk.ADD.w #$02, <_hk.A1
        _htk.MOVE.w [_hk.A1], HuTrack.channel.patternList.table + 2
        _htk.ADD.w #$02, <_hk.A1
        _htk.MOVE.w [_hk.A1], HuTrack.channel.patternList.table + 4
        _htk.ADD.w #$02, <_hk.A1
        _htk.MOVE.w [_hk.A1], HuTrack.channel.patternList.table + 6
        _htk.ADD.w #$02, <_hk.A1
        _htk.MOVE.w [_hk.A1], HuTrack.channel.patternList.table + 8
        _htk.ADD.w #$02, <_hk.A1
        _htk.MOVE.w [_hk.A1], HuTrack.channel.patternList.table + 10

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

        _htk.ADD.w #$01, <_hk.A0    ; Skip this attribute bank for now (it was already handle above). #TODO: need to figure out if this should be used or not.

        _htk.MOVE.b [_hk.A0], HuTrack.patternList.table.bank
        _htk.ADD.w #$01, <_hk.A0
        _htk.MOVE.b [_hk.A0], HuTrack.instr.table.bank
        _htk.ADD.w #$01, <_hk.A0
        _htk.MOVE.b [_hk.A0], HuTrack.waveform.table.bank
        _htk.ADD.w #$01, <_hk.A0
        _htk.MOVE.b [_hk.A0], HuTrack.pattern.table.bank
        _htk.ADD.w #$01, <_hk.A0
        _htk.MOVE.b [_hk.A0], HuTrack.samples.table.bank


        clx
.loop

        lda #$80
        sta <HuTrack.dda.bank,x

        inx
        cpx #$06
      bne .loop

        rmb6 <HuTrack.Status     ;// start song

        _htk.PULLBANK.4 _htk.PAGE_4000
  rts

