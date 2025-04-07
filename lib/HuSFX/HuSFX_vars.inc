; \file: HuSFX_vars.inc

      .zp

HuSFX.A0:                           .ds 2
HuSFX.bnk:                          .ds 1

      .bss


HuSFX.inProgress:                   .ds (1* 6)

HuSFX.stream.bnk:                   .ds 6
HuSFX.stream.lo:                    .ds 6
HuSFX.stream.hi:                    .ds 6
HuSFX.wf.bnk:                       .ds 1
HuSFX.wf.lo:                        .ds 1
HuSFX.wf.hi:                        .ds 1
HuSFX.delay:                        .ds 6
HuSFX.control:                      .ds 6
HuSFX.vol.chan:                     .ds 6
HuSFX.vol.pan:                      .ds 6
HuSFX.DMA:                          .ds (1+2+2+2+1)   ; this needs to be initialized to TIN and RTS.

HuSFXEngine.VarEnd

HuSFX.DMA.TINop = $D3
HuSFX.DMA.RTSop = $60
