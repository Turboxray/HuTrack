

include "../base_func/equ.inc"

;................................................
INC_BIT .macro

    lda \1
    inc a
    and #$01
    sta \1

    .endm

;................................................
CallFar    .macro
                tma #page(\1)
                pha

                lda #bank(\1)
                tam #page(\1)
                jsr \1

                pla
                tam #page(\1)

    .endm

;................................................
CallFar.AXY    .macro
                sta <R0
                tma #page(\1)
                pha

                lda #bank(\1)
                tam #page(\1)
                lda <R0
                pha
                phx
                phy
                jsr \1

                pla
                tam #page(\1)

    .endm

CallFarDoubleBank    .macro
                tma #page(\1)
                pha
                tma #page(\1) + 1
                pha

                lda #bank(\1)
                tam #page(\1)
                inc a
                tam #page(\1) + 1
                jsr \1

                pla
                tam #page(\1) + 1
                pla
                tam #page(\1)

    .endm

CallFarWide    .macro
                tma #page(\1)
                pha
                tma #page(\1) + 1
                pha

                lda #bank(\1)
                tam #page(\1)
                inc a
                tam #page(\1) + 1
                jsr \1

                pla
                tam #page(\1) + 1
                pla
                tam #page(\1)

    .endm


;................................................
CLEAR.REG .macro

    cla
    cly
    clx

    .endm

;................................................
PUSH.all .macro

    pha
    phy
    phx

    .endm

;................................................
PULL.all .macro

    plx
    ply
    pla

    .endm


;................................................
PUSH.addr .macro

    lda #>(\1 - 1)
    pha
    lda #<(\1 - 1)
    pha

    .endm

;................................................
jsr.ind .macro
    PUSH.addr .return_\@
        jmp [\1]
.return_\@
  .endm

;................................................
jsr.ind.x .macro
    PUSH.addr .return_\@
        jmp [\1,x]
.return_\@
  .endm

;................................................
Interrupts.disable  .macro
    sei
  .endm

;................................................
Interrupts.enable  .macro
    cli
  .endm


;................................................
MAP_BANK        .macro                ;8k

    .if (\?1=2)
    lda #bank(\1)
    tam #(\2)
    .endif

    .if (\?1=3)
    lda \1
    tam #(\2)
    .endif

    .if (\?1=6)
    lda \1
    tam #(\2)
    .endif

    .if (\?1=1)
    tam #(\2)
    .endif

    .endm

MAP_BANK.2        .macro        ;16k

    .if (\?1=2)
    lda #bank(\1)
    tam #(\2)
    inc a
    tam #(\2 + 1)
    .endif

    .if (\?1=3)
    lda \1
    tam #(\2)
    inc a
    tam #(\2 + 1)
    .endif

    .if (\?1=6)
    lda \1
    tam #(\2)
    inc a
    tam #(\2 + 1)
    .endif

    .if (\?1=1)
    tam #(\2)
    inc a
    tam #(\2 + 1)
    .endif

    .endm


MAP_BANK.3        .macro        ;24k

    .if (\?1=2)
    lda #bank(\1)
    tam #(\2)
    inc a
    tam #(\2 + 1)
    inc a
    tam #(\2 + 2)
    .endif

    .if (\?1=3)
    lda \1
    tam #(\2)
    inc a
    tam #(\2 + 1)
    inc a
    tam #(\2 + 2)
    .endif

    .if (\?1=6)
    lda \1
    tam #(\2)
    inc a
    tam #(\2 + 1)
    inc a
    tam #(\2 + 2)
    .endif

    .if (\?1=1)
    tam #(\2)
    inc a
    tam #(\2 + 1)
    inc a
    tam #(\2 + 2)
    .endif

    .endm

MAP_BANK.4        .macro        ;32k

    .if (\?1=2)
    lda #bank(\1)
    tam #(\2)
    inc a
    tam #(\2 + 1)
    inc a
    tam #(\2 + 2)
    inc a
    tam #(\2 + 3)
    .endif

    .if (\?1=3)
    lda \1
    tam #(\2)
    inc a
    tam #(\2 + 1)
    inc a
    tam #(\2 + 2)
    inc a
    tam #(\2 + 3)
    .endif

    .if (\?1=6)
    lda \1
    tam #(\2)
    inc a
    tam #(\2 + 1)
    inc a
    tam #(\2 + 2)
    inc a
    tam #(\2 + 3)
    .endif

    .if (\?1=1)
    tam #(\2)
    inc a
    tam #(\2 + 1)
    inc a
    tam #(\2 + 2)
    inc a
    tam #(\2 + 3)
    .endif

    .endm

;................................................
LEA        .macro

    lda #low(\1)
    sta <(\3)
    lda #high((\1 & $1fff)+ \2)
    sta <(\3 + 1)

    .endm

;..........
LEA.2       .macro

    ; This is for single page boundary only!
    if (\# < 2 | \# > 3)
    .fail Macro needs to be two or three arguments
    .endif

    .if (\# = 3)
        .if (\?1=2)
            lda #low(\1)
            sta \3
            lda #high((\1 & $3fff)+ \2)
            sta \3+1
        .endif

        .if (\?1!=2 & \?2=2)
            lda \1
            sta \3
            lda \1+1
            and #$3f
            ora #high(\2)
            sta \3+1
        .endif
    .endif

    .if (\# = 2)
        .if (\?1=2)
            lda \2+1
            and #$3f
            ora #high(\1)
            sta \2+1
        .else
            lda \2+1
            and #$3f
            ora \1
            sta \2+1
        .endif
    .endif

    .endm

LEA.l            .macro

    if (\3 = AXY)
        lda #low(\1)
        ldx #high((\1 & $1fff)+ \2)
        ldy #bank(\1)
    .else
        lda #low(\1)
        sta (\3)
        lda #high((\1 & $1fff)+ \2)
        sta (\3 + 1)
        lda #bank(\1)
        sta (\3 + 2)
    .endif
    .endm


LEB            .macro

    lda #bank(\1)
    sta (\2)

    .endm


;................................................
INC.w        .macro
            inc \1
            bne .x_\@
            inc \1 + 1
.x_\@
    .endm

;................................................
DEC.w        .macro
            lda \1
            sec
            sbc #$01
            sta \1
            lda \1 + 1
            sbc #$00
            sta \1 + 1
    .endm

;//................................................
;// MOVE macros


;......................
; MOVE.byte source, destination
MOVE.b    .macro
    .if (\#=0)
    .fail Macro requires two arguments
    .endif

    .if (\#=1)
    .fail Macro requires two arguments
    .endif

    .if (\#>2)
    .fail Macro requires two arguments
    .endif

    .if (\?2=6 & \2=ACC)
    lda \1
    .endif

    .if (\?2=6 & \2=IX)
    ldx \1
    .endif

    .if (\?2=6 & \2=IY)
    ldy \1
    .endif


    .if (\?1=2 & (\2!=ACC & \2!=IX & \2!=IY))
    lda \1
    sta \2
    .endif

    .if (\?1=3 & (\2!=ACC & \2!=IX & \2!=IY))
    lda \1
    sta \2
    .endif

    .if (\?1=4 & (\2!=ACC & \2!=IX & \2!=IY))
    lda \1
    sta \2
    .endif

    .if (\?1=6 & (\2!=ACC & \2!=IX & \2!=IY))
    lda \1
    sta \2
    .endif

;    .if (\?1=5)
;        .if (\5='Acc')
;        sta \2
;        .endif
;        .if (\5='IX')
;        stx \2
;        .endif
;        .if (\5='IY')
;        sty \2
;        .endif
;    .endif

    .endm


;......................
; MOVE.byte source, destination
MOVE.b.w    .macro
    .if (\#=0)
    .fail Macro requires two arguments
    .endif

    .if (\#=1)
    .fail Macro requires two arguments
    .endif

    .if (\#>2)
    .fail Macro requires two arguments
    .endif

    .if (\?2=2)
    .fail destination cannot be an immediate
    .endif

    .if (\?2=1)
    .fail destination cannot be a huc6280 register
    .endif

    .if (\?2=5)
    .fail destination cannot be a 'string'
    .endif


    .if (\?2=3)
            lda \1
            sta \2
            lda #$00
            sta \2 + 1
    .endif

    .if (\?2=4)
            lda \1
            sta \2
            lda #$00
            ldy #$01
            sta \2,y
    .endif

    .if (\?2=6)
            lda \1
            sta \2
            lda #$00
            sta \2 + 1
    .endif


    .endm


;......................
; MOVE.byte source, destination
MOVEA.b    .macro
    ;.fail \?1
    .if (\#=0)
    .fail Macro requires one arguments
    .endif


    .if (\#>1)
    .fail Macro requires one arguments
    .endif


    .if (\?1=1)
    .fail Cannot use A,X, or Y registers as source
    .endif

    ;source=#
    .if (\?1=2)
    lda #low(\1)
    .endif

    ;source=full ADDR
    .if (\?1=3)
    lda \1
    .endif

    ;source=indirect
    .if (\?1=4)
    lda \1
    .endif

    ;source=string
    .if (\?1=5)
    .fail Cant use strings as arguments.
    .endif

    ;source=label as direct address
    .if (\?1=6)
    lda \1
    .endif


    .endm

;......................
; MOVE.word source, destination
MOVE.w    .macro
    ;.fail \?1
    .if (\#=0)
    .fail Macro requires two arguments
    .endif

    .if (\#=1)
    .fail Macro requires two arguments
    .endif

    .if (\#>2)
    .fail Macro requires two arguments
    .endif


    .if (\?1=1)
    .fail Cannot use A,X, or Y registers as source
    .endif

    ;source=#
    .if (\?1=2 & \2 != AX)
    lda #low(\1)
    sta \2
    lda #high(\1)
    sta \2 + 1
    .endif

    .if (\2 = AX & \?1 = 2)
    ldx #low(\1)
    lda #high(\1)
    .endif

    .if (\2 = AX & (\?1 = 3 | \?1 = 6))
    ldx \1
    lda \1 + 1
    .endif

    .if (\2 = AY & \?1 = 2)
    ldy #low(\1)
    lda #high(\1)
    .endif

    .if (\2 = AY & (\?1 = 3 | \?1 = 6))
    ldy \1
    lda \1 + 1
    .endif

    .if (\2 = XY & \?1 = 2)
    ldy #low(\1)
    ldx #high(\1)
    .endif

    .if (\2 = XY & (\?1 = 3 | \?1 = 6))
    ldy \1
    ldx \1 + 1
    .endif


    ;source=full ADDR
    .if (\?1=3 & \2 != AX )
    lda \1
    sta \2
    lda \1 + 1
    sta \2 + 1
    .endif

    ;source=indirect
    .if (\?1=4 & \2 != AX )
    lda \1
    sta \2
    phy
    ldy #$01
    lda \1,y
    ply
    sta \2 + 1
    .endif

    ;source=string
    .if (\?1=5)
    .fail Cant use strings as arguments.
    .endif

    ;source=label as direct address
    .if (\?1=6 & \2 != AX )
    lda \1
    sta \2
    lda \1 + 1
    sta \2 + 1
    .endif


    .endm

;......................
; MOVE.word source, destination
MOVE.sw    .macro

    .if (\#<1)
    .fail Macro requires at least two arguments
    .endif

    .if (\#>3)
    .fail Macro requires at least two arguments
    .endif

    .if (\#=3 & (\2!=IX & \2!=IY))
    .fail For a split index, second argument needs to be an index reg IX or IY
    .endif

    ; Do split with index
    .if (\#=3)

        .if (\3!=AX & \3!=AY & \3!=XY)
            .if (\2=IX)
                lda \1.lo,x
                sta \3
                lda \1.hi,x
                sta \3+1
            .endif
            .if (\2=IY)
                lda \1.lo,y
                sta \3
                lda \1.hi,y
                sta \3+1
            .endif
        .endif

        .if (\?1=2)

        .endif

    .endif

    ; Do split with no index
    .if (\#=2)
        lda \1.lo
        sta \2
        lda \1.hi
        sta \2+1
    .endif

    .if (\?1=1)
    .fail Cannot use A,X, or Y registers as source
    .endif

    .endm


;......................
; MOVE.word source, destination
MOVE.w.add    .macro

    .if (\#<3)
    .fail Macro requires three arguments
    .endif

    .if (\#>3)
    .fail Macro requires three arguments
    .endif


    .if (\?1=1)
    .fail Cannot use A,X, or Y registers as source
    .endif

    ;source=#
    .if (\?1=2)
    lda #low(\1+\3)
    sta \2
    lda #high(\1+\3)
    sta \2 + 1
    .endif

    ;source=full ADDR
    .if (\?1=3)
    lda \1
    clc
    adc #low(\3)
    sta \2
    lda \1 + 1
    adc #high(\3)
    sta \2 + 1
    .endif

    ;source=indirect
    .if (\?1=4)
    lda \1
    clc
    adc #low(\3)
    sta \2
    phy
    ldy #$01
    lda \1,y
    adc #high(\3)
    ply
    sta \2 + 1
    .endif

    ;source=string
    .if (\?1=5)
    .fail Cant use strings as arguments.
    .endif

    ;source=label as direct address
    .if (\?1=6)
    lda \1
    clc
    adc #low(\3)
    sta \2
    lda \1 + 1
    adc #high(\3)
    sta \2 + 1
    .endif


    .endm


;......................
; MOVE.X.byte source, destination
MOVE.X.b    .macro
    ldx \1
    sta \2
    .endm

;......................
; MOVE.Y.byte source, destination
MOVE.Y.b    .macro
    ldy \1
    sta \2
    .endm

;......................
; MOVE.IY.byte source, destination
MOVE.IY.b    .macro
    lda \1
    sta \2
    iny
    .endm

;......................
; MOVE.IY.byte source, destination
MOVE.DY.b    .macro
    lda \1
    sta \2
    dey
    .endm

;......................
; MOVE.AX A:X, destination
MOVE.AX    .macro
    sta \1
    stx \1 + 1

    .endm

;......................
; MOVE.AY A:Y, destination
MOVE.AY    .macro
    sta \1
    sty \1 + 1

    .endm

;......................
; MOVE.XY X:Y, destination
MOVE.XY    .macro
    stx \1
    sty \1 + 1

    .endm


;//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;//..............................................
;//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;// Old move macros
MOVE.r        .macro
        lda (\1)
        sta <(\2)
        lda (\1 + 1)
        sta <(\2 + 1)
    .endm

MOVE.r.l        .macro
        lda \1
        sta \2
        lda \1 + 1
        sta \2 + 1
        lda \1 + 2
        sta \2 + 2
    .endm

; MOVE.b        .macro
;     .if (\?1=4)

;         lda \1
;         sta \2
;     .endif

;     .if (\?1=3)
;         lda \1
;         sta \2
;     .endif

;     .if (\?1=2)
;         lda \1
;         sta \2
;     .endif

;     .if (\?1=6)
;         lda \1
;         sta \2
;     .endif

;     .endm

MOVE.Rx.b        .macro
    .if (\?1=4)

        ldx \1
        stx \2
    .endif

    .if (\?1=3)
        ldx \1
        stx \2
    .endif

    .if (\?1=2)
        ldx \1
        stx \2
    .endif

    .if (\?1=6)
        ldx \1
        stx \2
    .endif

    .if (\?1=1)
        stx \2
    .endif


    .endm

MOVE.R.A        .macro
    .if (\?1=4)

        lda \1
        sta \2
    .endif

    .if (\?1=3)
        lda \1
        sta \2
    .endif

    .if (\?1=2)
        lda \1
        sta \2
    .endif

    .if (\?1=6)
        lda \1
        sta \2
    .endif

    .if (\?1=1)
        sta \2
    .endif

    .endm

MOVRY        .macro
    .if (\?1=4)

        ldy \1
        sty \2
    .endif

    .if (\?1=3)
        ldy \1
        sty \2
    .endif

    .if (\?1=2)
        ldy #\1
        sty \2
    .endif

    .if (\?1=6)
        ldy \1
        sty \2
    .endif

    .if (\?1=1)
        sty \2
    .endif


    .endm


; MOVE.w        .macro
;     .if (\?1=4)

;         lda \1
;         sta \2
;         ldy #1
;         lda \1,y
;         sta \2 + 1
;     .endif

;     .if (\?1=3)
;         lda \1
;         sta \2
;         lda \1 + 1
;         sta \2 + 1
;     .endif

;     .if (\?1=2)
;         lda #low(\1)
;         sta \2
;         lda #high(\1)
;         sta \2 + 1
;     .endif

;     .if (\?1=6)
;         lda #low(\1)
;         sta \2
;         lda #high(\1 + 1)
;         sta \2 + 1
;     .endif

;     .endm


MOVE.IX.l        .macro

        ldx #\7-1
.x_\@
        lda \1,x
        sta \4,x
        lda \2,x
        sta \5,x
        lda \3,x
        sta \6,x
        dex
        bpl .x_\@
    .endm

MOVI_l        .macro

        lda \1
        sta \2
        lda \1 + 1
        sta \3
        lda \1 + 2
        sta \4
    .endm

; MOVE.Y.b    .macro
;         ldy \1
;     .endm

; MOVE.X.b    .macro
;         ldx \1
;     .endm


;//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;//..............................................
;//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

;................................................
DMA.word.port        .macro
        tia (\1 & $1fff)+\2,\3,\4
    .endm

DMA.byte.Pport        .macro
        tin (\1 & $1fff)+\2,\3,\4
    .endm


DMA.far.local        .macro
        tii (\1 & $1fff)+\2,\3,\4
    .endm

DMA.local        .macro
        tii \1,\2,\3
    .endm

;//................................................
;// ADD macros


;......................
;CMP.word source,destination. 16bit + 16bit->16bit
CMP.w        .macro

        ;first error checks
            .if (\#<>2)
            .fail Macro requires two arguments
            .endif
            .if (\?2=0)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=1)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=5)
            .fail destination must be label, absolute address, or indirect. 1
            .endif

    .if (\?1=2) ;src=#immd
        .if (\?2=2)    ;#immd
            lda #low(\1)
            cmp #low(\2)
            lda #high(\1)
            sbc #high(\2)
.skip_\@
        .endif

        .if (\?2=3 | \?2=6)
            lda #low(\1)
            cmp \2
            lda #high(\1)
            sbc \2 + 1
.skip_\@
        .endif

        .if (\?2=4)    ;indirect dest
            lda #low(\1)
            cmp \2
            ldy #$01
            lda #high(\1)
            sbc \2,y
.skip_\@
        .endif
    .endif



    .if (\?1=3 | \?1=6) ;src=addr/label
        .if (\?2=2)    ;#immd
            lda \1
            cmp #low(\2)
            lda \1 + 1
            sbc #high(\2)
.skip_\@
        .endif

        .if (\?2=3 | \?2=6)
            lda \1
            cmp \2
            lda \1 + 1
            sbc \2 + 1
.skip_\@
        .endif

        .if (\?2=4)    ;indirect dest
            ldy #$01
            lda \1
            cmp \2
            lda \1 + 1
            sbc \2,y
.skip_\@
        .endif
    .endif

    .if (\?1=4) ;src=indirect
        .if (\?2=2)
            ldy #$01
            lda \1
            cmp #low(\2)
            lda \1,y
            sbc #high(\2)
.skip_\@
        .endif

        .if (\?2=3 | \?2=6)
            ldy #$01
            lda \1
            cmp \2
            lda \1,y
            sbc \2 + 1
.skip_\@
        .endif

        .if (\?2=4)    ;indirect dest
            ldy #$01
            lda \1
            cmp \2
            lda \1,y
            sbc \2,y
.skip_\@
        .endif
    .endif


    .endm


;......................
;CMP.byte arg1, arg2  (8bit,8bit)
CMP.b        .macro

        ;first error checks
            .if (\#<>2)
            .fail Macro requires two arguments
            .endif
            .if (\?2=0)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=1)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=5)
            .fail destination must be label, absolute address, or indirect. 1
            .endif

    .if (\?1=2) ;src=#immd
        .if (\?2=2)    ;#immd
            lda #low(\1)
            cmp #low(\2)
        .endif

        .if (\?2=3 | \?2=6)
            lda #low(\1)
            cmp \2
        .endif

        .if (\?2=4)    ;indirect dest
            lda #low(\1)
            cmp \2
        .endif
    .endif



    .if (\?1=3 | \?1=6) ;src=addr/label
        .if (\?2=2)    ;#immd
            lda \1
            cmp #low(\2)
        .endif

        .if (\?2=3 | \?2=6)
            lda \1
            cmp \2
        .endif

        .if (\?2=4)    ;indirect dest
            lda \1
            cmp \2
        .endif
    .endif

    .if (\?1=4) ;src=indirect
        .if (\?2=2)
            lda \1
            cmp #\2
        .endif

        .if (\?2=3 | \?2=6)
            lda \1
            cmp \2
        .endif

        .if (\?2=4)    ;indirect dest
            lda \1
            cmp \2
        .endif
    .endif


    .endm



;//................................................
;// ADD macros

;......................
;ADD.byte source,destination
ADD.b        .macro
        ;first error checks
            .if (\#<>2)
            .fail Macro requires two arguments
            .endif
            .if (\?2=0)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=1)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=2)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=5)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?1=5)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?1=1)
            .fail destination must be label, absolute address, or indirect. 1
            .endif


    .if (\?1=2) ;src=#immd
        .if (\?2=3 | \?2=6)
            lda \2
            clc
            adc #low(\1)
            sta \2
        .endif

        .if (\?2=4)    ;indirect dest
            lda \2
            clc
            adc #low(\1)
            sta \2
        .endif
    .endif

    .if (\?1=3 | \?1=6) ;src=addr/label
        .if (\?2=3 | \?2=6)
            lda \2
            clc
            adc \1
            sta \2
        .endif

        .if (\?2=4)    ;indirect dest
            lda \2
            clc
            adc \1
            sta \2
        .endif
    .endif

    .if (\?1=4) ;src=indirect
        .if (\?2=3 | \?2=6)
            lda \2
            clc
            adc \1
            sta \2
        .endif

        .if (\?2=4)    ;indirect dest
            lda \2
            clc
            adc \1
            sta \2
        .endif
    .endif


    .endm


;......................
;ADD.word source,destination. 16bit + 16bit->16bit
ADD.w        .macro

        ;first error checks
            .if (\#<>2)
            .fail Macro requires two arguments
            .endif
            .if (\?2=0)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=1)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=2)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=5)
            .fail destination must be label, absolute address, or indirect. 1
            .endif

    .if (\?1=2) ;src=#immd
        .if (\?2=3 | \?2=6)
            lda #low(\1)
            clc
            adc \2
            sta \2
            ;bcc .skip\@
            lda #high(\1)
            adc \2 + 1
            sta \2 + 1
.skip\@
        .endif

        .if (\?2=4)    ;indirect dest
            lda #low(\1)
            clc
            adc \2
            sta \2
            ;bcc .skip\@
            phy
            ldy #$01
            lda #high(\1)
            adc \2,y
            sta \2,y
            ply
.skip\@
        .endif
    .endif

    .if (\?1=3 | \?1=6) ;src=addr/label
        .if (\?2=3 | \?2=6)
            lda \1
            clc
            adc \2
            sta \2
            ;bcc .skip\@
            lda \1 + 1
            adc \2 + 1
            sta \2 + 1
.skip\@
        .endif

        .if (\?2=4)    ;indirect dest
            lda \1
            clc
            adc \2
            sta \2
            ;bcc .skip\@
            phy
            ldy #$01
            lda \1 + 1
            adc \2,y
            sta \2,y
            ply
.skip\@
        .endif
    .endif

    .if (\?1=4) ;src=indirect
        .if (\?2=3 | \?2=6)
            lda \1
            clc
            adc \2
            sta \2
            ;bcc .skip\@
            phy
            ldy #$01
            lda \1,y
            adc \2 + 1
            sta \2 + 1
            ply
.skip\@
        .endif

        .if (\?2=4)    ;indirect dest
            lda \1
            clc
            adc \2
            sta \2
            ;bcc .skip\@
            phy
            ldy #$01
            lda \1,y
            adc \2,y
            sta \2,y
            ply
.skip\@
        .endif
    .endif


    .endm

;......................
;ADD.byte.word source,destination. 8bit + 16bit->16bit
ADD.b.w        .macro

        ;first error checks
            .if (\#<>2)
            .fail Macro requires two arguments
            .endif
            .if (\?2=0)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=1)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=2)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=5)
            .fail destination must be label, absolute address, or indirect. 1
            .endif

    .if (\?1=2) ;src=#immd
        .if (\?2=3 | \?2=6)
            lda #low(\1)
            clc
            adc \2
            sta \2
            bcc .skip\@
            inc \2 + 1
.skip\@
        .endif

        .if (\?2=4)    ;indirect dest
            lda #low(\1)
            clc
            adc \2
            sta \2
            bcc .skip\@
            phy
            ldy #$01
            lda \2,y
            inc a
            sta \2,y
            ply
.skip\@
        .endif
    .endif

    .if (\?1=3 | \?1=6) ;src=addr/label
        .if (\?2=3 | \?2=6)
            lda \1
            clc
            adc \2
            sta \2
            bcc .skip\@
            inc \2 + 1
.skip\@
        .endif

        .if (\?2=4)    ;indirect dest
            lda \1
            clc
            adc \2
            sta \2
            bcc .skip\@
            phy
            ldy #$01
            lda \2,y
            inc a
            sta \2,y
            ply
.skip\@
        .endif
    .endif

    .if (\?1=4) ;src=indirect
        .if (\?2=3 | \?2=6)
            lda \1
            clc
            adc \2
            sta \2
            bcc .skip\@
            phy
            ldy #$01
            lda \2 + 1
            inc a
            sta \2 + 1
            ply
.skip\@
        .endif

        .if (\?2=4)    ;indirect dest
            lda \1
            clc
            adc \2
            sta \2
            bcc .skip\@
            phy
            ldy #$01
            lda \2,y
            inc a
            sta \2,y
            ply
.skip\@
        .endif
    .endif


    .endm


;......................
;ADD.word.long source,destination. 16bit + 24bit->24bit
ADD.w.l.split        .macro

        ;first error checks
            .if (\#<>2)
            .fail Macro requires two arguments
            .endif
            .if (\?2=0)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=1)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=2)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=5)
            .fail destination must be label, absolute address, or indirect. 1
            .endif

    .if (\?1=2) ;src=#immd
            lda #low(\1)
            clc
            adc \2.lo
            sta \2.lo
            lda #high(\1)
            adc \2.mid
            sta \2.mid
        bcc .skip\@
            inc \2.hi
.skip\@
    .endif

    .if (\?1=3 | \?1=6) ;src=addr/label
            lda \1
            clc
            adc \2.lo
            sta \2.lo
            lda \1 + 1
            adc \2.mid
            sta \2.mid
        bcc .skip\@
            inc \2.hi
.skip\@
    .endif

    .if (\?1=4) ;src=indirect
            lda [\1]
            clc
            adc \2.lo
            sta \2.lo
            ldy #$01
            lda [\1],y
            adc \2.mid
            sta \2.mid
        bcc .skip\@
            inc \2.hi
.skip\@
    .endif


    .endm


;......................
;ADD.Y.word Y,destination. 8bit + 16bit->16bit
ADD.Y.w        .macro

        ;first error checks
            .if (\#<>1)
            .fail Macro requires two arguments
            .endif
            .if (\?1=0)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?1=1)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?1=2)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?1=5)
            .fail destination must be label, absolute address, or indirect. 1
            .endif


        .if (\?1=3 | \?1=6)
            tya
            clc
            adc \1
            sta \1
            bcc .skip\@
            inc \1 + 1
.skip\@
        .endif

        .if (\?1=4)    ;indirect dest
            tya
            clc
            adc \1
            sta \1
            bcc .skip\@
            phy
            ldy #$01
            lda \1,y
            inc a
            sta \1,y
            ply
.skip\@
        .endif


    .endm

;......................
;ADD.Y.word Y,destination. 8bit + 16bit->16bit
ADD.A.w        .macro

        ;first error checks
            .if (\#<>1)
            .fail Macro requires two arguments
            .endif
            .if (\?1=0)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?1=1)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?1=2)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?1=5)
            .fail destination must be label, absolute address, or indirect. 1
            .endif


        .if (\?1=3 | \?1=6)
            clc
            adc \1
            sta \1
            bcc .skip\@
            inc \1 + 1
.skip\@
        .endif

    .endm

;......................
;ADD.Y.word Y,destination. 8bit + 16bit->16bit
ADD.A.b        .macro

        ;first error checks
            .if (\#<>1)
            .fail Macro requires two arguments
            .endif
            .if (\?1=0)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?1=1)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?1=2)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?1=5)
            .fail destination must be label, absolute address, or indirect. 1
            .endif


        .if (\?1=3 | \?1=6)
            clc
            adc \1
            sta \1

        .endif

    .endm



;......................
;AND.word.long source,destination. 16bit + 24bit->24bit
AND.b.b.w  .macro

        ;first error checks
            .if (\#<>3)
            .fail Macro requires two arguments
            .endif

        lda \2
        and \1
        sta \3
        stz \3

    .endm


;......................
;AND.word source,destination. 16bit + 16bit->16bit
AND.w        .macro

        ;first error checks
            .if (\#<>2)
            .fail Macro requires two arguments
            .endif
            .if (\?2=0)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=1)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=2)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=5)
            .fail destination must be label, absolute address, or indirect. 1
            .endif

    .if (\?1=2) ;src=#immd
        .if (\?2=3 | \?2=6)
            lda #low(\1)
            and \2
            sta \2
            lda #high(\1)
            and \2 + 1
            sta \2 + 1
        .endif

        .if (\?2=4)    ;indirect dest
            lda #low(\1)
            and \2
            sta \2
            phy
            ldy #$01
            lda #high(\1)
            and \2,y
            sta \2,y
            ply
        .endif
    .endif

    .if (\?1=3 | \?1=6) ;src=addr/label
        .if (\?2=3 | \?2=6)
            lda \1
            and \2
            sta \2
            lda \1 + 1
            and \2 + 1
            sta \2 + 1
        .endif

        .if (\?2=4)    ;indirect dest
            lda \1
            and \2
            sta \2
            phy
            ldy #$01
            lda \1 + 1
            and \2,y
            sta \2,y
            ply
        .endif
    .endif

    .if (\?1=4) ;src=indirect
        .if (\?2=3 | \?2=6)
            lda \1
            and \2
            sta \2
            phy
            ldy #$01
            lda \1,y
            and \2 + 1
            sta \2 + 1
            ply
        .endif

        .if (\?2=4)    ;indirect dest
            lda \1
            and \2
            sta \2
            phy
            ldy #$01
            lda \1,y
            and \2,y
            sta \2,y
            ply
        .endif
    .endif


    .endm


;......................
;AND.byte source,destination. dest & src -> dest
AND.b  .macro

        ;first error checks
        .if (\#<2)
        .fail Macro requires two or three arguments
        .endif
        .if (\#>3)
        .fail Macro requires two or three arguments
        .endif

        .if (\#=3)
        lda \2
        and \1
        sta \3
        .endif

        .if (\#=2)
        lda \2
        and \1
        sta \2
        .endif


    .endm


;......................
;OR.byte source,destination. dest | src -> dest
OR.b  .macro

        ;first error checks
        .if (\#<2)
        .fail Macro requires two or three arguments
        .endif
        .if (\#>3)
        .fail Macro requires two or three arguments
        .endif

        .if (\#=3)
        lda \2
        ora \1
        sta \3
        .endif

        .if (\#=2)
        lda \2
        ora \1
        sta \2
        .endif


    .endm

;......................
;ASL.Y
ASL.Y.safe        .macro
        say
        asl a
        say
    .endm

ASL.2.Y.safe        .macro
        say
        asl a
        asl a
        say
    .endm

ASL.3.Y.safe        .macro
        say
        asl a
        asl a
        asl a
        say
    .endm

ASL.Y        .macro
        say
        asl a
        say
    .endm

ASL.2.Y        .macro
        say
        asl a
        asl a
        say
    .endm

ASL.3.Y        .macro
        say
        asl a
        asl a
        asl a
        say
    .endm

;......................
;ASL.X  
ASL.X.safe        .macro
        sax
        asl a
        sax
    .endm

ASL.2.X.safe        .macro
        sax
        asl a
        asl a
        sax
    .endm

ASL.3.X.safe        .macro
        sax
        asl a
        asl a
        asl a
        sax
    .endm

ASL.X        .macro
        sax
        asl a
        sax
    .endm

ASL.2.X        .macro
        sax
        asl a
        asl a
        sax
    .endm

ASL.3.X        .macro
        sax
        asl a
        asl a
        asl a
        sax
    .endm


;......................
;ASL.Y  
LSL.Y        .macro

        ;first error checks
            .if (\#<>1)
            .fail Macro requires two arguments
            .endif
            .if (\?1=0)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?1=1)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?1=2)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?1=5)
            .fail destination must be label, absolute address, or indirect. 1
            .endif


        say
        cmp #$80
        asl a
        say


    .endm

;......................
;LSR.b  
LSR.b        .macro
    lsr \1
    .endm

LSR.2.b        .macro
    lsr \1
    lsr \1
    .endm

LSR.3.b        .macro
    lsr \1
    lsr \1
    lsr \1
    .endm

LSR.4.b        .macro
    lsr \1
    lsr \1
    lsr \1
    lsr \1
    .endm

;......................
;LSR.w  
LSR.w        .macro
    lsr \1
    ror \1 + 1
    .endm

LSR.2.w        .macro
    lsr \1
    ror \1 + 1
    lsr \1
    ror \1 + 1
    .endm

LSR.3.w        .macro

    .if (\?1 = 6 & \1 = AX)
        lsr a
        sax
        ror a
        sax
        ror a
        sax
        ror a
        sax
        ror a
        sax
        ror a
        sax
    .endif

    .if (\?1 = 6 & \1 = AY)
        lsr a
        say
        ror a
        say
        ror a
        say
        ror a
        say
        ror a
        say
        ror a
        say
    .endif
    .endm

LSR.4.w        .macro
    lsr \1
    ror \1 + 1
    lsr \1
    ror \1 + 1
    lsr \1
    ror \1 + 1
    lsr \1
    ror \1 + 1
    .endm

;.......

;...............
;OR.w  src, dest
OR.w        .macro

        ;first error checks
            .if (\#<>2)
            .fail Macro requires two arguments
            .endif
            .if (\?2=0)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=1)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=5)
            .fail destination must be label, absolute address, or indirect. 1
            .endif

    .if (\?1=2) ;src=#immd
        .if (\?2=2)    ;#immd
            lda #low(\1)
            ora #low(\2)
            lda #high(\1)
            ora #high(\2)
.skip_\@
        .endif

        .if (\?2=3 | \?2=6)
            lda #low(\1)
            ora \2
            lda #high(\1)
            ora \2 + 1
.skip_\@
        .endif

        .if (\?2=4)    ;indirect dest
            lda #low(\1)
            ora \2
            ldy #$01
            lda #high(\1)
            ora \2,y
.skip_\@
        .endif
    .endif



    .if (\?1=3 | \?1=6) ;src=addr/label
        .if (\?2=2)    ;#immd
            lda \1
            ora #low(\2)
            lda \1 + 1
            ora #high(\2)
.skip_\@
        .endif

        .if (\?2=3 | \?2=6)
            lda \1
            ora \2
            lda \1 + 1
            ora \2 + 1
.skip_\@
        .endif

        .if (\?2=4)    ;indirect dest
            ldy #$01
            lda \1
            ora \2
            lda \1 + 1
            ora \2,y
.skip_\@
        .endif
    .endif

    .if (\?1=4) ;src=indirect
        .if (\?2=2)
            ldy #$01
            lda \1
            ora #low(\2)
            lda \1,y
            ora #high(\2)
.skip_\@
        .endif

        .if (\?2=3 | \?2=6)
            ldy #$01
            lda \1
            ora \2
            lda \1,y
            ora \2 + 1
.skip_\@
        .endif

        .if (\?2=4)    ;indirect dest
            ldy #$01
            lda \1
            ora \2
            lda \1,y
            ora \2,y
.skip_\@
        .endif
    .endif


    .endm


;................................................
BNE.l    .macro
        beq .x_\@
        jmp \1
.x_\@

    .endm

BEQ.l    .macro
        bne .x_\@
        jmp \1
.x_\@

    .endm

BPL.l    .macro
        BMI .x_\@
        jmp \1
.x_\@

    .endm

BMI.l    .macro
        bpl .x_\@
        jmp \1
.x_\@

    .endm

BCS.l    .macro
        bcc .x_\@
        jmp \1
.x_\@

    .endm

BCC.l    .macro
        bcs .x_\@
        jmp \1
.x_\@

    .endm

BVS.l    .macro
        bvc .x_\@
        jmp \1
.x_\@

    .endm

BVC.l    .macro
        bvs .x_\@
        jmp \1
.x_\@

    .endm


;................................................

;......................
;PUSHBANK.1  addr
PUSHBANK.1        .macro
    .if (\#=0)
    .fail Macro requires one argument
    .endif

        tma #(high(\1)>>5)
        pha
    .endm

;......................
;PUSHBANK.2  addr
PUSHBANK.2        .macro
    .if (\#=0)
    .fail Macro requires one argument
    .endif


        tma #(\1)
        pha
        tma #(\1 + 1)
        pha
    .endm

;......................
;PUSHBANK.3 addr
PUSHBANK.3        .macro
    .if (\#=0)
    .fail Macro requires one argument
    .endif


        tma #(\1)
        pha
        tma #(\1 + 1)
        pha
        tma #(\1 + 2)
        pha
    .endm

;......................
;PUSHBANK.4 addr
PUSHBANK.4        .macro
    .if (\#=0)
    .fail Macro requires one argument
    .endif


        tma #(\1 + 1)
        pha
        tma #(\1 + 1)
        pha
        tma #(\1 + 2)
        pha
        tma #(\1 + 3)
        pha
    .endm

;......................
;PULLBANK.1 addr
PULLBANK.1        .macro
    .if (\#=0)
    .fail Macro requires one argument
    .endif


        pla
        tam #(\1)
    .endm

;......................
;PULLBANK.2 addr
PULLBANK.2        .macro
    .if (\#=0)
    .fail Macro requires one argument
    .endif


        pla
        tam #(\1 + 1)
        pla
        tam #(\1)
    .endm

;......................
;PULLBANK.3 addr
PULLBANK.3        .macro
    .if (\#=0)
    .fail Macro requires one argument
    .endif


        pla
        tam #(\1 + 2)
        pla
        tam #(\1 + 1)
        pla
        tam #(\1)
    .endm


;......................
;PULLBANK.4 addr
PULLBANK.4        .macro
    .if (\#=0)
    .fail Macro requires one argument
    .endif

        pla
        tam #(\1 + 3)
        pla
        tam #(\1 + 2)
        pla
        tam #(\1 + 1)
        pla
        tam #(\1)
    .endm




;................................................

CPUslow_INTdisabled    .macro
            php
            sei
            csl
    .endm

CPU_slow    .macro
            php
            csl
    .endm


CPU_restored    .macro
            plp
    .endm

;................................................

InitialStartup    .macro

                sei
                cld
                csh
                ldx #$ff
                txs
                lda #$ff
                tam #$00
                lda #$f8
                tam #$01

    .endm



;.................................................
AlignByte256    .macro

    .org ( (* + 255) & $ff00)

    .endm

;.................................................
IncludeBinary    .macro

start_\@:
\1:  .incbin \2
end_\@:

\1.size = sizeof(\1)

    .endm

;.................................................
IncludeData    .macro

start_\@:
\1:  .include \2
end_\@:

\1.size = end_\@ - start_\@

    .endm

;.................................................
IncludeCode    .macro

\1:
        .include \2
.end_\@:

\1.size = .end_\@ - \1

    .endm


;.................................................
FOLLOW_ENTRY   .macro
        plx
        jmp [\1,x]
    .endm

;.................................................
CONNECT_ENTRY   .macro
        ldy #$01
        jmp \1
    .endm
;.................................................
ENTRY_POINT   .macro
.self_\@
        .dw .self_\@ + 2
    .endm


;.................................................
STOW_ENTRY.b   .macro
        lda #\1
        sta \2
    .endm

;.................................................
STOW_ENTRY.w   .macro
        lda #low(\1)
        sta \2
        lda #high(\1)
        sta \2 + 1
    .endm

;.................................................
STOW_ENTRY.addr   .macro
        lda #low(.addr_\@)
        sta \2
        lda #high(.addr_\@)
        sta \2 + 1
.addr_\@
    .endm

;.................................................
RTS_ENTRY   .macro
        lda #low(.addr_\@)
        ldx #high(.addr_\@)
.addr_\@
    rts
    .endm

;.................................................
RETURN_ENTRY.stack   .macro
        lda #low(.addr_\@)
        pha
        lda #high(.addr_\@)
        pha
.addr_\@
    jmp \2
    .endm

;.................................................
RETURN_ENTRY.AX   .macro
        lda #low(.addr_\@)
        ldx #high(.addr_\@)
    jmp \1
.addr_\@
    .endm


;.................................................
ADD_ENTRY.b   .macro
        lda \1
        clc
        adc #\2
        sta \3
    .endm

;.................................................
ADD_ENTRY.w   .macro
        lda \1
        clc
        adc #low(\2)
        sta \3 + 1
        lda \1 + 1
        adc #high(\2)
        sta \3 + 1
    .endm

;......................
;SUB.word source,destination. 16bit + 16bit->16bit
SUB.w        .macro

        ;first error checks
            .if (\#<>2)
            .fail Macro requires two arguments
            .endif
            .if (\?2=0)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=1)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=2)
            .fail destination must be label, absolute address, or indirect. 1
            .endif
            .if (\?2=5)
            .fail destination must be label, absolute address, or indirect. 1
            .endif

    .if (\?1=2) ;src=#immd
        .if (\?2=3 | \?2=6)
            lda \2
            sec
            sbc #low(\1)
            sta \2
            lda \2 + 1
            sbc #high(\1)
            sta \2 + 1
        .endif

        .if (\?2=4)    ;indirect dest
            lda \2
            sec
            sbc #low(\1)
            sta \2
                phy
            ldy #$01
            lda \2 + 1,y
            sbc #high(\1)
            sta \2 + 1,y
                ply
        .endif
    .endif

    .if (\?1=3 | \?1=6) ;src=addr/label
        .if (\?2=3 | \?2=6)
            lda \2
            sec
            sbc \1
            sta \2
            lda \2 + 1
            sbc \1 + 1
            sta \2 + 1
        .endif

        .if (\?2=4)    ;indirect dest
            lda \2
            sec
            sbc \1
            sta \2
                phy
            ldy #$01
            lda \2 + 1,y
            sbc \1
            sta \2 + 1,y
                ply
        .endif
    .endif

    .if (\?1=4) ;src=indirect
        .if (\?2=3 | \?2=6)
            lda \2
            sec
            sbc \1
            sta \2
                phy
            ldy #$01
            lda \2,y
            sbc \1 + 1
            sta \2,y
                ply
        .endif

        .if (\?2=4)    ;indirect dest
            lda \2
            sec
            sbc \1
            sta \2
                phy
            ldy #$01
            lda \2,y
            sbc \1,y
            sta \2,y
                ply
        .endif
    .endif


    .endm



;,........................................
DEBUG_NOP   .macro
    nop
    nop
    nop
    nop
  .endm

