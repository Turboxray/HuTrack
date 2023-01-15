
include "../base_func/video/vdc/equ.inc"

;//................................................................................
;// MACROS


;//................
WAITVBLANK        .macro
        .if (\#=0)
            ldx #1
        .endif

        .if (\#>0)
            ldx #\1
        .endif


        jsr __wait_vblank
    .endm

;//................
VDC1    .macro            ;hardware I/O page must be mapped to the first bank

    stz $000E

    .endm


;//................
VDC2    .macro            ;hardware I/O page must be mapped to the first bank

    inc $000E

    .endm

;//................
MAWR_ADDR .macro
    st0 #$00
    st1 #LOw(\1)
    st2 #HIGH(\1)

    .endm

;//................
MARR_ADDR .macro
    st0 #$01
    st1 #LOw(\1)
    st2 #HIGH(\1)

    .endm

;//................
VDC.data .macro
    st0 #$02

    .endm

;//................
VDC.reg     .macro

    .if    (\?2=1)
    st0 #\1
    sta $0002
    stz $0003
    .endif

    .if    (\#=1)
    st0 #\1
    .endif

    .if    (\#=2 & \?2 = 2)
    st0 #\1
    st1 #LOW(\2)
    st2 #HIGH(\2)
     .endif

    .if    (\#=3 & \?2 = 6)
    st0 #\1
    lda \2
    sta $0002
    lda \3
    sta $0003
    .endif

    .if    (\#=2 & \?2 = 6)
    st0 #\1
    lda \2
    sta $0002
    lda \2+1
    sta $0003
    .endif

    .if    (\#=2 & \?2 = 3)
    st0 #\1
    lda \2
    sta $0002
    lda \2+1
    sta $0003
    .endif

    .endm

;//................
VDC2.reg .macro                ;macro for SuperGrafx

    .if    (\?2=1)
    st0 #\1
    sta $0012
    stz $0013
    .endif

    .if    (\#=1)
    st0 #\1
    .endif

    .if    (\#=2 & \?2 != 1)
    st0 #\1
    st1 #LOW(\2)
    st2 #HIGH(\2)
     .endif

    .if    (\#=3 & \?3 != 1)
    st0 #\1
    lda \2
    sta $0012
    lda \3
    sta $0013
    .endif

    .endm

;//................
LOAD_RCR .macro

    st0 #RCR
    lda \1
    clc
    adc #$40
    sta $0002
    lda \1+1
    adc #$00
    sta $0003

    .endm

;//................
UPDATE_RCR .macro        ;this is for special H-line parallax scroll routine
                ; - destroys REG A
    st0 #RCR
    sta $0002
    lda <RCR_MSB
    sta $0003

     .endm

;//................
ST1.w .macro

     st1 #LOW(\1)
     st2 #HIGH(\1)

    .endm

;//................
MOVE.YA.port .macro

     sta $0002
     sty $0003

    .endm

;//................
MOVE.YA.port2 .macro

     sta $0012
     sty $0013

    .endm


;//................
VREG_Select .macro

    st0 #\1
    lda #\1
    sta <vdc_reg

    .endm


;//................
sVDC_REG     .macro

    .if    (\?2=1)
    lda #\1
    sta <vdc_reg
    st0 #\1
    sta $0002
    stz $0003
    .endif

    .if    (\#=1)
    lda #\1
    sta <vdc_reg
    st0 #\1
    .endif

    .if    (\#=2 & \?2 != 1)
    lda #\1
    sta <vdc_reg
    st0 #\1
    st1 #LOW(\2)
    st2 #HIGH(\2)
     .endif

    .if    (\#=3 & \?3 != 1)
    lda #\1
    sta <vdc_reg
    st0 #\1
    lda \2
    sta $0002
    lda \3
    sta $0003
    .endif

    .endm

;//................
iVDC_PORT     .macro

    st1 #LOW(\1)
    st2 #HIGH(\1)

    .endm

;//................
sVDC_INC     .macro

    lda #$05
    sta <vdc_reg
    st0 #$05
    st2 #\1

    .endm

