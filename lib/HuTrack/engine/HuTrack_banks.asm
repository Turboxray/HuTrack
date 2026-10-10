; Revision 1 assets use low/high/bank pointers. Each object fits two banks.
; Helpers preserve X; music scratch is never used by the timer IRQ.
HuTrack.Bank.map:
        lda HuTrack.F.ptr+1
        and #$1f
        ora #$40
        sta HuTrack.F.ptr+1
        lda HuTrack.F.bank
HuTrack.Bank.mapPair:
        tam #2
        inc a
        tam #3
        rts

; A=index (0..127). Read a three-byte pointer without losing carry at 255.
HuTrack.Bank.pointer:
        sta HuTrack.F.offset
        stz HuTrack.F.offset+1
        asl a
        rol HuTrack.F.offset+1
        clc
        adc HuTrack.F.offset
        sta HuTrack.F.offset
      bcc .offset
        inc HuTrack.F.offset+1
.offset
        jsr HuTrack.Bank.map
        clc
        lda HuTrack.F.ptr
        adc HuTrack.F.offset
        sta HuTrack.F.ptr
        lda HuTrack.F.ptr+1
        adc HuTrack.F.offset+1
        sta HuTrack.F.ptr+1
        cly
        lda [HuTrack.F.ptr],y
        sta HuTrack.F.value
        iny
        lda [HuTrack.F.ptr],y
        sta HuTrack.F.value+1
        iny
        lda [HuTrack.F.ptr],y
        sta HuTrack.F.bank
        lda HuTrack.F.value
        sta HuTrack.F.ptr
        lda HuTrack.F.value+1
        sta HuTrack.F.ptr+1
        rts

; Advance a normalized cached pointer, carrying into the bank byte.
HuTrack.Bank.advance:
        clc
        adc HuTrack.F.ptr
        sta HuTrack.F.ptr
        lda HuTrack.F.ptr+1
        adc #0
        cmp #$60
      bcc .store
        sbc #$20
        inc HuTrack.F.bank
.store
        sta HuTrack.F.ptr+1
        rts

; Copy the six root descriptors before remapping their source window.
HuTrack.Bank.attributes:
        jsr HuTrack.Bank.map
        ldy #17
.copy
        lda [HuTrack.F.ptr],y
        sta HuTrack.song.tables,y
        dey
      bpl .copy
        ldy #0
        jsr HuTrack.Bank.root
        jsr HuTrack.Bank.map
        lda HuTrack.F.ptr
        sta _hk.A1
        lda HuTrack.F.ptr+1
        sta _hk.A1+1
        rts

; Y=byte offset into the cached six-descriptor root.
HuTrack.Bank.root:
        lda HuTrack.song.tables,y
        sta HuTrack.F.ptr
        lda HuTrack.song.tables+1,y
        sta HuTrack.F.ptr+1
        lda HuTrack.song.tables+2,y
        sta HuTrack.F.bank
        rts

HuTrack.Bank.loadLists:
        lda HuTrack.song.tables+6
        sta HuTrack.instr.table
        lda HuTrack.song.tables+7
        sta HuTrack.instr.table+1
        lda HuTrack.song.tables+8
        sta HuTrack.instr.table.bank
        lda HuTrack.song.tables+9
        sta HuTrack.waveform.table
        lda HuTrack.song.tables+10
        sta HuTrack.waveform.table+1
        lda HuTrack.song.tables+11
        sta HuTrack.waveform.table.bank
        lda HuTrack.song.tables+15
        sta HuTrack.samples.table
        lda HuTrack.song.tables+16
        sta HuTrack.samples.table+1
        lda HuTrack.song.tables+17
        sta HuTrack.samples.table.bank
        clx
.channel
        ldy #3
        jsr HuTrack.Bank.root
        txa
        jsr HuTrack.Bank.pointer
        txa
        asl a
        tay
        lda HuTrack.F.ptr
        sta HuTrack.channel.patternList.table,y
        lda HuTrack.F.ptr+1
        sta HuTrack.channel.patternList.table+1,y
        lda HuTrack.F.bank
        sta HuTrack.channel.patternList.bank,x
        ldy #12
        jsr HuTrack.Bank.root
        txa
        jsr HuTrack.Bank.pointer
        lda HuTrack.F.ptr
        sta HuTrack.channel.patternTable.lo,x
        lda HuTrack.F.ptr+1
        sta HuTrack.channel.patternTable.hi,x
        lda HuTrack.F.bank
        sta HuTrack.channel.patternTable.bank,x
        inx
        cpx #6
      bcc .channel
        rts

HuTrack.Bank.pattern:
        txa
        asl a
        tay
        lda HuTrack.channel.patternList.table,y
        sta HuTrack.F.ptr
        lda HuTrack.channel.patternList.table+1,y
        sta HuTrack.F.ptr+1
        lda HuTrack.channel.patternList.bank,x
        sta HuTrack.F.bank
        jsr HuTrack.Bank.map
        ldy HuTrack.channel.pattern.num,x
        lda [HuTrack.F.ptr],y
        sta HuTrack.channel.pattern.idx,x
        lda HuTrack.channel.patternTable.lo,x
        sta HuTrack.F.ptr
        lda HuTrack.channel.patternTable.hi,x
        sta HuTrack.F.ptr+1
        lda HuTrack.channel.patternTable.bank,x
        sta HuTrack.F.bank
        lda HuTrack.channel.pattern.idx,x
        jsr HuTrack.Bank.pointer
        jsr HuTrack.Bank.map
        clc
        lda HuTrack.F.ptr
        adc HuTrack.channel.patternOffset.lo,x
        sta HuTrack.currentPattern
        lda HuTrack.F.ptr+1
        adc HuTrack.channel.patternOffset.hi,x
        sta HuTrack.currentPattern+1
        rts

HuTrack.Bank.instrument:
        lda HuTrack.instr.table
        sta HuTrack.F.ptr
        lda HuTrack.instr.table+1
        sta HuTrack.F.ptr+1
        lda HuTrack.instr.table.bank
        sta HuTrack.F.bank
        lda HuTrack.channel.instr,x
        jsr HuTrack.Bank.pointer
        lda HuTrack.F.ptr
        sta HuTrack.F.record
        lda HuTrack.F.ptr+1
        sta HuTrack.F.record+1
        lda HuTrack.F.bank
        sta HuTrack.F.record+2
        cla
        jsr HuTrack.Bank.envelope
        lda [HuTrack.F.ptr]
        sta HuTrack.VolEnv.len,x
        ldy #1
        lda [HuTrack.F.ptr],y
        sta HuTrack.VolEnv.repeat,x
        stz HuTrack.VolEnv.idx,x
        lda #2
        jsr HuTrack.Bank.advance
        lda HuTrack.F.ptr
        sta HuTrack.VolEnvPtr.lo,x
        lda HuTrack.F.ptr+1
        sta HuTrack.VolEnvPtr.hi,x
        lda HuTrack.F.bank
        sta HuTrack.VolEnv.bank,x
        lda #1
        jsr HuTrack.Bank.envelope
        lda [HuTrack.F.ptr]
        sta HuTrack.ArpEnv.mode,x
        ldy #1
        lda [HuTrack.F.ptr],y
        sta HuTrack.ArpEnv.len,x
        iny
        lda [HuTrack.F.ptr],y
        sta HuTrack.ArpEnv.repeat,x
        stz HuTrack.ArpEnv.idx,x
        stz HuTrack.ArpEnv.finished,x
        lda #3
        jsr HuTrack.Bank.advance
        lda HuTrack.F.ptr
        sta HuTrack.ArpEnvPtr.lo,x
        lda HuTrack.F.ptr+1
        sta HuTrack.ArpEnvPtr.hi,x
        lda HuTrack.F.bank
        sta HuTrack.ArpEnv.bank,x
        lda #2
        jsr HuTrack.Bank.envelope
        lda [HuTrack.F.ptr]
        sta HuTrack.WfEnv.len,x
        ldy #1
        lda [HuTrack.F.ptr],y
        sta HuTrack.WfEnv.repeat,x
        stz HuTrack.WfEnv.idx,x
        lda #2
        jsr HuTrack.Bank.advance
        lda HuTrack.F.ptr
        sta HuTrack.WfEnvPtr.lo,x
        lda HuTrack.F.ptr+1
        sta HuTrack.WfEnvPtr.hi,x
        lda HuTrack.F.bank
        sta HuTrack.WfEnv.bank,x
        rts

HuTrack.Bank.envelope:
        pha
        lda HuTrack.F.record
        sta HuTrack.F.ptr
        lda HuTrack.F.record+1
        sta HuTrack.F.ptr+1
        lda HuTrack.F.record+2
        sta HuTrack.F.bank
        pla
        jsr HuTrack.Bank.pointer
        jmp HuTrack.Bank.map

HuTrack.Bank.waveform:
        pha
        lda HuTrack.waveform.table
        sta HuTrack.F.ptr
        lda HuTrack.waveform.table+1
        sta HuTrack.F.ptr+1
        lda HuTrack.waveform.table.bank
        sta HuTrack.F.bank
        pla
        jsr HuTrack.Bank.pointer
        jsr HuTrack.Bank.map
        lda HuTrack.F.ptr
        sta HuTrack.A1
        lda HuTrack.F.ptr+1
        sta HuTrack.A1+1
        rts
