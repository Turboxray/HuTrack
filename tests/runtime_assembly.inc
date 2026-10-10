; Fixed-bank bridge: HuCC may place ordinary .proc code in MPR6.
_assemblyPcm:
    php
    sei
    tma #6
    pha
    lda #bank(HuTrackEngine.SfxPcmRequest)
    tam #6
    lda #bank(_pcm)
    sta _hk.EAX0.l
    lda #low(_pcm+3)
    sta _hk.EAX0.m
    lda #high(_pcm+3)
    sta _hk.EAX0.h
    lda #5
    sta _hk.EAX0.u
    sta $800
    lda #$9f
    sta $807
    jsr HuTrackEngine.SfxPcmRequest
    php
    pla
    and #1
    sta _asmCarry
    stz _asmCarry+1
    pla
    tam #6
    plp
    rts

; Test the standalone assembly decoder as well as the C macro decoder.
_assemblySfx:
    tma #6
    pha
    lda #bank(HuSFX.process)
    tam #6
    jsr HuSFX.process
    pla
    tam #6
    rts
    .bank 60
    .org $c000
    .include "runtime_standalone.inc"
    .bank 62
    .org $5ffe
_edge_pcm:
    .db 0,0
    .page 2
    .db 0,31,1,16,0,$80
    .ifdef HUCC
    .bank CORE_BANK
    .else
    .bank LIB1_BANK
    .endif
