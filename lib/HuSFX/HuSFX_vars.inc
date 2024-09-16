; \file: HuSFX_vars.inc

      .zp

HuSFX.A0:                           .ds 2
HuSFX.A1:                           .ds 2
HuSFX.bnk:                          .ds 2

      .bss


HuSFX.inProgress:                   .ds (1* 6)

HuSFX.stream.bnk:                   .ds 6
HuSFX.stream.lo:                    .ds 6
HuSFX.stream.hi:                    .ds 6
HuSFX.wf.bnk:                       .ds 6
HuSFX.wf.lo:                        .ds 6
HuSFX.wf.hi:                        .ds 6
HuSFX.delay:                        .ds 6
HuSFX.control:                      .ds 6
HuSFX.DMA:                          .ds (1+2+2+2+1)   ; this needs to be initialized to TIN and RTS.

HuSFXEngine.VarEnd

HuSFX.DMA.TINop = $D3
HuSFX.DMA.RTSop = $60
