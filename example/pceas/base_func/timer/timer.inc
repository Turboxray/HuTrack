

include "../base_func/timer/equ.inc"

;................................................
TIMER.reg        .macro
        lda #\2
        sta \1
    .endm

;................................................
TIMER.cmd    .macro
        lda #\1
        sta TMR_CMD
    .endm

;................................................
TIMER.port    .macro
        lda #\1
        sta TMR_PORT
    .endm

