

;.......................................................
;
SATB.reset

        clx
.loop
        stz cell.Y.lo,x
        stz cell.Y.hi,x

        ; stz cell.X.lo,x
        ; stz cell.X.hi,x

        ; stz cell.attribs.lo,x
        ; stz cell.attribs.hi,x

        ; stz cell.pattern.lo,x
        ; stz cell.pattern.hi,x

        inx
        cpx #SpriteGroupSize
      bne .loop
        stz SATB.openslot
        lda #$40
        sta SATB.openslot.hpriority

  rts


;.......................................................
;
SATB.dma
        VDC.reg MAWR, SATB.vramAddr
        VDC.reg VRWR

        ;debug box
        ; lda player.camera.y
        ; clc
        ; adc #low(0)
        ; sta $0002
        ; lda player.camera.y+1
        ; adc #high(0)
        ; sta $0003

        ; lda player.camera.x
        ; clc
        ; adc #low(0)
        ; sta $0002
        ; lda player.camera.x+1
        ; adc #high(0)
        ; sta $0003

        ; lda #low($f0*2)
        ; sta $0002
        ; lda #high($f0*2)
        ; sta $0003

        ; lda #low(NO_H_FLIP | NO_V_FLIP | PRIOR_H | SIZE16_32 | SPAL1)
        ; sta $0002
        ; lda #high(NO_H_FLIP | NO_V_FLIP | PRIOR_H | SIZE16_32 | SPAL1)
        ; sta $0003


        ldx SATB.openslot.hpriority
        txa
        sec
        sbc #$40
        tay
        ldx #$40
        jsr .xfer.sprites

        clx
        lda SATB.openslot.hpriority
        sec
        sbc #$40
        eor #$ff
        inc a
        clc
        adc #$40
        tay
        jsr .xfer.sprites

        stz SATB.openslot
        lda #$40
        sta SATB.openslot.hpriority

  rts

.xfer.sprites

        cpy #$00
      beq .out

        MOVE.b cell.Y.lo,x , vdata_port.l
        MOVE.b cell.Y.hi,x , vdata_port.h

        MOVE.b cell.X.lo,x , vdata_port.l
        MOVE.b cell.X.hi,x , vdata_port.h

        MOVE.b cell.pattern.lo,x , vdata_port.l
        MOVE.b cell.pattern.hi,x , vdata_port.h

        MOVE.b cell.attribs.lo,x , vdata_port.l
        MOVE.b cell.attribs.hi,x , vdata_port.h

        inx
        dey
      bne .xfer.sprites

.out

  rts

;.......................................................
;
SATB.hide

  rts


