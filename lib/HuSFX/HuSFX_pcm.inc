; Runtime sample catalog and HuTrack timer-player bridge.
; Expanded with the HuSFX caller, not placed in the fixed library bank.
    .ifndef HUSFX_PCM_DEFINED
HUSFX_PCM_DEFINED = 1
    .ifndef HUSFX_PCM_SLOTS
HUSFX_PCM_SLOTS = 64
    .endif
    .if (HUSFX_PCM_SLOTS<1 | HUSFX_PCM_SLOTS>255)
      .fail HUSFX_PCM_SLOTS must be 1 through 255.
    .endif

; Register a C-format PCM asset (three-byte header followed by samples).
; Arguments are bank, address-low and address-high memory operands.
; Return A:X = ID, or $ffff when full / header would cross bank $ff.
HuSFX.PCM.Queue .macro
        .ifdef HUTRACK_SFX_VOLUME
        php
        sei
        ldx HuSFX.pcm.count
        cpx #HUSFX_PCM_SLOTS
      bcs .full\@
        lda \2
        clc
        adc #3
        sta HuSFX.pcm.lo,x
        lda \3
        and #$1f
        adc #0
        tay
        and #$1f
        ora #$40
        sta HuSFX.pcm.hi,x
        tya
        cmp #$20
        lda \1
        adc #0
      bcs .full\@
        sta HuSFX.pcm.bank,x
        inc HuSFX.pcm.count
        plp
        cla
      bra .out\@
.full\@
        plp
        .endif
        lda #$ff
        tax
.out\@
    .endm

; Stop only PCM started by this HuSFX stream. Preserve A, X and Y.
HuSFX.PCM.Stop .macro
        .ifdef HUTRACK_SFX_VOLUME
        pha
        php
        sei
        lda HuSFX.pcm.owned,x
      beq .out\@
        lda #$80
        sta <HuTrack.dda.inactive,x
        sta <HuTrack.dda.bank,x
        stz HuSFX.pcm.owned,x
        stz HuSFX.rawControl,x
        stz HuSFX.control,x
        stx $800
        stz $804
.out\@
        plp
        pla
        .endif
    .endm

; A = sample ID, X = channel, Y = flags (0 once, 1 loop).
; Carry set rejects the command. Caller ends the invalid SFX stream.
HuSFX.PCM.Start .macro
        .ifdef HUTRACK_SFX_VOLUME
        cpy #2
      bcc .flags.valid\@
        jmp .error\@
.flags.valid\@
        cmp HuSFX.pcm.count
      bcc .id.valid\@
        jmp .error\@
.id.valid\@
        bit HuTrack.SFX.inProgress,x
      bmi .reserved\@
        jmp .error\@
.reserved\@
        sty HuSFX.pcm.flags
        tay
        php
        sei
        lda #$80
        sta <HuTrack.dda.inactive,x
        lda HuSFX.pcm.bank,y
        sta <HuTrack.dda.bank,x
        sta <HuTrack.dda.loop.bank,x
        lda HuSFX.pcm.lo,y
        sta <HuTrack.dda.addr.lo,x
        sta <HuTrack.dda.addr.loop.lo,x
        lda HuSFX.pcm.hi,y
        sta <HuTrack.dda.addr.hi,x
        sta <HuTrack.dda.addr.loop.hi,x
        ; A loop with no samples would spin forever inside the timer IRQ.
        lda HuSFX.pcm.flags
      beq .sample.ready\@
        tma #2
        pha
        lda <HuTrack.dda.bank,x
        tam #2
        lda <HuTrack.dda.addr.lo,x
        sta <HuTrack.dda.ptr
        lda <HuTrack.dda.addr.hi,x
        sta <HuTrack.dda.ptr+1
        lda [HuTrack.dda.ptr]
        tay
        pla
        tam #2
        tya
      bpl .sample.ready\@
        plp
        jmp .error\@
.sample.ready\@
        lda HuSFX.pcm.flags
        sta <HuTrack.dda.cntr0,x
        ora #$80
        sta <HuTrack.dda.cntr1,x
        stx $800
        stz $807
        ; Respect a DDA volume already supplied by the register stream.
        lda HuSFX.rawControl,x
        and #$c0
        cmp #$c0
      bne .default.volume\@
        lda HuSFX.rawControl,x
      bra .volume\@
.default.volume\@
        lda #$df
.volume\@
        sta HuSFX.rawControl,x
        HuSFX.MixVolume
        sta HuSFX.control,x
        sta $804
        lda #$10
        sta $806
        lda #1
        sta HuSFX.pcm.owned,x
        stz <HuTrack.dda.inactive,x
        lda HuTrack.DDApaused
      bne .suspended\@
        rmb7 <HuTrack.DDAprocess
.suspended\@
        plp
        clc
      bra .out\@
.error\@
        .endif
        sec
.out\@
    .endm

; Natural completion is silenced on the next HuSFX update.
HuSFX.PCM.CheckEnd .macro
        .ifdef HUTRACK_SFX_VOLUME
        lda HuSFX.pcm.owned,x
      beq .out\@
        bit <HuTrack.dda.inactive,x
      bpl .out\@
        HuSFX.PCM.Stop
.out\@
        .endif
    .endm

; Changing away from enabled DDA must stop the interrupt writer first.
HuSFX.PCM.Control .macro
        .ifdef HUTRACK_SFX_VOLUME
        pha
        and #$c0
        cmp #$c0
      beq .out\@
        HuSFX.PCM.Stop
.out\@
        pla
        .endif
    .endm
    .endif
