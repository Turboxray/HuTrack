
;//...............................
DMASprites: .macro
    call SATB.dma
    .endm

;//...............................
ResetSprites: .macro
    call SATB.reset
    .endm


;//...............................
HideAllSprites: .macro
    .endm


;//...............................
ReorderAllSprites: .macro
    .endm


;//...............................
HideSingleSprite: .macro
    .endm


;//...............................
ShowSingleSprite: .macro
    .endm

;//...............................
SetSpriteAddr: .macro
    lda #low(\1)
    sta SATB.vramAddr
    lda #high(\1)
    sta SATB.vramAddr+1
    .endm

