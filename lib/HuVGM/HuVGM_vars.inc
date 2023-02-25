
;TODO: Need to fix the name of these ZP vars for namespace collision

    .zp

_hV.R0:                         .ds 2
_hV.D0:                         .ds 2
_hV.A0:                         .ds 2
_hV.A1:                         .ds 2sfx
_hV.A2:                         .ds 2

_hV.EAX0:                       .ds 4


HuVGM.Enabled:                  .ds (1* 6)

HuVGM.A0:                       .ds 2
HuVGM.A1:                       .ds 2
HuVGM.ptr:                      .ds 2


HuVGM.FXptr0:                   .ds 2
HuVGM.FXptr1:                   .ds 2
HuVGM.FXptr2:                   .ds 2
HuVGM.FXptr3:                   .ds 2

      .bss

HuVGM.addr.bank:                .ds 6
HuVGM.addr.lo:                  .ds 6
HuVGM.addr.hi:                  .ds 6

HuVGM.wf:                       .ds 6
HuVGM.vol:                      .ds 6
HuVGM.pan:                      .ds 6

HuVGM.sfx.bank                  .ds 30
HuVGM.sfx.hi                    .ds 30
HuVGM.sfx.lo                    .ds 30
HuVGM.sfx.len                   .ds 1

HuVGM.sfx.status                .ds 1
HuVGM.sfx.enabled               .ds 1

