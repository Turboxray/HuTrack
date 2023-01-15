
include "../base_func/IO/irq_controller/equ.inc"

;................................................
IRQ.control     .macro

    lda #\1
    sta $1402

    .endm


;................................................
ISR.setVecMask   .macro

    lda #\1
    tsb <vector_mask

  .endm

;................................................
ISR.resetVecMask   .macro

    lda #(\1 ^ 0xff)
    trb <vector_mask

  .endm

;................................................
ISR.setVector   .macro

    php
    sei

    ; Convert {1,2,4,8,16} to {0,2,4,6,8}
    .if ( \1 = 1 | \1 = 2 | \1 = 4 | \1 = 8 | \1 = 16 )
        if ( \1 = 1 )
          ldx #0
        .endif
        if ( \1 = 2 )
          ldx #2
        .endif
        if ( \1 = 4 )
          ldx #4
        .endif
        if ( \1 = 8 )
          ldx #6
        .endif
        if ( \1 = 16 )
          ldx #8
        .endif
    .else
      .fail Value needs to be 1,2,4,8, or 16
    .endif

    lda #<\2
    sta <irq_vector_list,x
    lda #>\2
    sta <irq_vector_list+1,x
    plp

  .endm

