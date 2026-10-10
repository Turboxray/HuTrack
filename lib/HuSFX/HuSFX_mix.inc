; Apply logarithmic attenuation to stream values. 31 / $ff is unity gain.
; These helpers preserve X and Y; A is the mixed PSG register value.
    .ifndef HUSFX_MIX_DEFINED
HUSFX_MIX_DEFINED = 1
HuSFX.MixVolume .macro
        pha
        and #$e0
        sta HuSFX.mix.mode
        pla
        and #31
        clc
        adc HuSFX.vol.chan,x
        sec
        sbc #31
      bcs .volume\@
        cla
.volume\@
        .ifdef HUTRACK_SFX_VOLUME
        sec
        sbc HuTrack.sfxAttenuation
      bcs .group\@
        cla
.group\@
        .endif
        ora HuSFX.mix.mode
    .endm

HuSFX.MixPan .macro
        sta HuSFX.mix.raw
        and #15
        sta HuSFX.mix.low
        lda HuSFX.vol.pan,x
        and #15
        clc
        adc HuSFX.mix.low
        sec
        sbc #15
      bcs .right\@
        cla
.right\@
        sta HuSFX.mix.low
        lda HuSFX.mix.raw
        and #$f0
        sta HuSFX.mix.raw
        lda HuSFX.vol.pan,x
        and #$f0
        clc
        adc HuSFX.mix.raw
      bcs .left\@
        cmp #$f0
      bcs .left\@
        cla
      bra .pan\@
.left\@
        sec
        sbc #$f0
.pan\@
        ora HuSFX.mix.low
    .endm
    .endif
