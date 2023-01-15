;//.......................................................
;                                                        .
;   Sprite structures in memory                          .
;                                                        .
;                                                        .
;.........................................................

    .include "../base_func/video/vdc/sprites/equ.inc"
    .bss

    ;..................................................

    cell.Y.lo:                      .ds SpriteGroupSize
    cell.Y.hi:                      .ds SpriteGroupSize

    cell.X.lo:                      .ds SpriteGroupSize
    cell.X.hi:                      .ds SpriteGroupSize

    cell.attribs.lo:                .ds SpriteGroupSize
    cell.attribs.hi:                .ds SpriteGroupSize

    cell.pattern.lo:                .ds SpriteGroupSize
    cell.pattern.hi:                .ds SpriteGroupSize

    SATB.vramAddr:                  .ds 2

    SATB.openslot:                  .ds 1

    SATB.openslot.hpriority:       .ds 1
