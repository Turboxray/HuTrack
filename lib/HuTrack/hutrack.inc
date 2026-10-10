
include "HuTrack/HuTrack_equ.inc"

;................................................................
;................................................................
; Music Engine macros                                           .
;                                                               .
;................................................................

HuTrack.DDA.reSync .macro

    stz _htk.TMR_CMD
    stz _htk.IRQ.ackTIRQ
    lda #_htk.TMR_ON
    sta _htk.TMR_CMD
    .endm


HuTrack.setDDAvector  .macro

_htk.timer_vect = \1
  .endm

HuTrack.setVDCreturnVector  .macro

    lda #low(\1)
    sta \2
    lda #high(\1)
    sta \2+1
  .endm

;................................................................
;................................................................
; Pattern entry macros                                          .
;                                                               .
;................................................................


PatternEntry .macro
    ; note, instrument, volume, FX1, arg1, FX2, arg2, FX3, arg3.
    ; Empty arguments omit the corresponding independently encoded field.
    .db ((\?1!=0)*1)+((\?2!=0)*4)+((\?3!=0)*8)+((\?4!=0)*16)+((\?5!=0)*32)+(((\?6!=0)|(\?7!=0)|(\?8!=0)|(\?9!=0))*64)
    .if (\?1!=0)
      .db \1
    .endif
    .if (\?2!=0)
      .db \2
    .endif
    .if (\?3!=0)
      .db \3
    .endif
    .if (\?4!=0)
      .db \4
    .endif
    .if (\?5!=0)
      .db \5
    .endif
    .if ((\?6!=0)|(\?7!=0)|(\?8!=0)|(\?9!=0))
      .db ((\?6!=0)*1)+((\?7!=0)*2)+((\?8!=0)*4)+((\?9!=0)*8)
      .if (\?6!=0)
        .db \6
      .endif
      .if (\?7!=0)
        .db \7
      .endif
      .if (\?8!=0)
        .db \8
      .endif
      .if (\?9!=0)
        .db \9
      .endif
    .endif
    .endm

PatternEntry.skip .macro
    .if (\#=0)
      .db $e1
    .else
      .if (\1<1 | \1>30)
        .fail PatternEntry.skip accepts 1 through 30 rows.
      .endif
      .db 224+\1
    .endif
    .endm

; End the current pattern using D00 (there is no stream terminator byte).
PatternEntry.end .macro
    .db $10,$0d
    .endm

HuTrack.CallFar    .macro
                tma #page(\1)
                pha

                lda #bank(\1)
                tam #page(\1)
                jsr \1

                pla
                tam #page(\1)

    .endm

;......................
;HuTrack.CallFarRemap  label, page#
HuTrack.CallFarRemap .macro
.htk.remap\@:
    ; The callee must be assembled for this page, or be position independent.
    .if (\2=page(.htk.remap\@))
      .fail CallFarRemap cannot replace the page containing its return code.
    .endif
    tma #\2
    pha
    lda #bank(\1)
    tam #\2
    jsr ((\1 & $1fff) | (\2*$2000))
    pla
    tam #\2
    .endm

HuTrack.CallFarSafe .macro
.htk.safe\@:
    ; Keep expansion size independent of a forward target's bank/page.
    .if (page(\1)=page(.htk.safe\@))
      .if (bank(\1)!=bank(.htk.safe\@))
        .fail CallFarSafe cannot replace the executing bank. Use a fixed-page trampoline.
      .endif
    .endif
    HuTrack.CallFar \1
    .endm

;......................
HutrackEngine.ManualCall   .macro
        HuTrack.setVDCreturnVector  HutrackEngine.irq1.vsyncRTN\@, HuTrack.returnVec
        jmp HuTrackEngine.EngineCall
HutrackEngine.irq1.vsyncRTN\@:
    .endm

_HuTrackEngine_ManualCall   .macro
        HuTrack.setVDCreturnVector  HutrackEngine.irq1.vsyncRTN\@, HuTrack.returnVec
        jmp HuTrackEngine.EngineCall
HutrackEngine.irq1.vsyncRTN\@:
    .endm

;.................................................
HuTrack.AlignByte256    .macro

    .org ( (* + 255) & $ff00)

    .endm


HuTrack.BenchmarkColorZero   .macro

.ifdef HUTRACK_BENCHMARK
.if (HUTRACK_BENCHMARK = 1)
        stz $402
        lda #$01
        sta $403
        lda #low((\2<<6) + (\1<<3) + \3)
        sta $404
        lda #high((\2<<6) + (\1<<3) + \3)
        sta $405
.endif
.endif

    .endm
;..................................................................
;..................................................................


;................................................
_htk.LEA        .macro

    lda #low(\1)
    sta <(\3)
    lda #high((\1 & $1fff)+ \2)
    sta <(\3 + 1)

    .endm

;..........
_htk.LEA.2       .macro

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

_htk.LEA.l            .macro

    if (\3 = REG_AXY)
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


;......................
; MOVE.byte source, destination
_htk.MOVE.b    .macro

    .if (\#=0)
    .fail Macro requires two arguments
    .endif

    .if (\#=1)
    .fail Macro requires two arguments
    .endif

    .if (\#>2)
    .fail Macro requires two arguments
    .endif

    .if (\?2=6)
        .if (\2=REG_ACC)
x_\@ = 1
            lda \1
        .endif
    .endif

    .if (\?2=6)
        .if (\2=REG_X)
x_\@ = 2
            ldx \1
        .endif
    .endif

    .if (\?2=6)
        .if (\2=REG_Y)
x_\@ = 3
            ldy \1
        .endif
    .endif


    .if (\?2=3 & \2=REG_ACC)
x_\@ = 4
    lda \1
    .endif

    .if (\?2=3 & \2=REG_X)
x_\@ = 5
    ldx \1
    .endif

    .if (\?2=3 & \2=REG_Y)
x_\@ = 6
    ldy \1
    .endif


    .if (\?1=2)
    .if (\2!=REG_ACC & \2!=REG_X & \2!=REG_Y)
x_\@ = 7
    lda \1
    sta \2
    .endif
    .endif

    .if (\?1=3)
    .if (\2!=REG_ACC & \2!=REG_X & \2!=REG_Y)
x_\@ = 8
    lda \1
    sta \2
    .endif
    .endif

    .if (\?1=4)
    .if (\2!=REG_ACC & \2!=REG_X & \2!=REG_Y)
x_\@ = 9
    lda \1
    sta \2
    .endif
    .endif

    .if (\?1=6)
    .if (\2!=REG_ACC & \2!=REG_X & \2!=REG_Y)
x_\@ = 10
    lda \1
    sta \2
    .endif
    .endif

    .if (x_\@ > 0)
        ; MOVE.b macro defined
    .else
        .fail MOVE.b: no match found for macro arguments
    .endif
    .endm


;......................
; MOVE.word source, destination
_htk.MOVE.w    .macro
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
        .if (\1=A)
            .fail Cannot use A registers as source. Use STRING versions of "AX", "AY", or "XY"
        .else
            .fail Cannot use X or Y registers as source. Use STRING versions of "AX", "AY", or "XY"
        .endif
    .endif

    ;source=#, dest = address
    .if (\?1=2 & \?2!=4)
        .if (\?2!=5)
x_\@ = 1
            lda #low(\1)
            sta \2
            lda #high(\1)
            sta \2 + 1
        .endif
    .endif

    .if (\?1=2 & \?2=4)
x_\@ = 16
        lda #low(\1)
        sta \2
        phy
        ldy #1
        lda #high(\1)
        sta \2,y
        ply
    .endif

    ;source=#, dest = REG:PAIR AX
    .if (\?1 = 2 & \?2=5)
        .if (\2="AX")
x_\@ = 2
            ldx #low(\1)
            lda #high(\1)
        .endif
    .endif

    ;source=addr, dest = REG:PAIR AX
    .if ((\?1 = 3 | \?1 = 6) & \?2=5)
        .if (\2="AX")
x_\@ = 3
            ldx \1
            lda \1 + 1
        .endif
    .endif

    ;source=#, dest = REG:PAIR AY
    .if (\?1 = 2 & \?2=5)
        .if (\2 = "AY")
x_\@ = 4
            ldy #low(\1)
            lda #high(\1)
        .endif
    .endif

    ;source=addr, dest = REG:PAIR AY
    .if ((\?1 = 3 | \?1 = 6) & \?2=5)
        .if (\2 = "AY")
x_\@ = 5
            ldy \1
            lda \1 + 1
        .endif
    .endif

    ;source=#, dest = REG:PAIR XY
    .if (\?1 = 2 & \?2=5)
        .if (\2 = "XY")
x_\@ = 6
            ldy #low(\1)
            ldx #high(\1)
        .endif
    .endif

    ;source=addr, dest = REG:PAIR XY
    .if ((\?1 = 3 | \?1 = 6) & \?2=5)
        .if (\2 = "XY")
x_\@ = 7
            ldy \1
            ldx \1 + 1
        .endif
    .endif

    ;source=AX or AY or XY, dest = addr
    ; PCEAS versions classify named constants as either type 3 or type 6.
    .if ((\?2 = 3 | \?2 = 6) & (\?1=3 | \?1=6))
        .if (\1=REG_AX)
x_\@ = 8
            stx \2
            sta \2 + 1
        .endif
        .if (\1=REG_AY)
x_\@ = 9
            sty \2
            sta \2 + 1
        .endif
        .if (\1=REG_XY)
x_\@ = 10
            sty \2
            stx \2 + 1
        .endif
    .endif

    ;source=ADDR, dest = addr
    .if (\?1=3 & \?2!=5)
    .if (\1 != REG_AX & \1 != REG_AY & \1 != REG_XY)
        .if (\?2!=4)
x_\@ = 11
            lda \1
            sta \2
            lda \1 + 1
            sta \2 + 1
        .endif
    .endif
    .endif

    ;source=ADDR, dest = indirect
    .if (\?1=3 & \?2!=5)
    .if (\1 != REG_AX & \1 != REG_AY & \1 != REG_XY)
        .if (\?2=4)
x_\@ = 12
            lda \1
            sta \2
            phy
            ldy #$01
            lda \1 + 1
            sta \2,y
            ply
        .endif
    .endif
    .endif

    ;source=indirect, dest = addr
    .if (\?1=4 & \?2!=5)
        .if (\?2!=4)
x_\@ = 13
            lda \1
            sta \2
            phy
            ldy #$01
            lda \1,y
            ply
            sta \2 + 1
        .endif
    .endif

    ;source=indirect, dest = indirect
    .if (\?1=4 & \?2=4)
x_\@ = 14
        lda \1
        sta \2
        phy
        ldy #$01
        lda \1,y
        sta \2,y
        ply
    .endif

    ;source=label as direct address
    .if (\?1=6 & \?2!=5)
    .if (\1 != REG_AX & \1 != REG_AY & \1 != REG_XY)
x_\@ = 15
            lda \1
            sta \2
        .if (\?2=4)
            phy
            ldy #1
            lda \1+1
            sta \2,y
            ply
        .else
            lda \1+1
            sta \2+1
        .endif
    .endif
    .endif


    .if (x_\@ > 0)
        ; MOVE.w macro defined
    .else
        .fail MOVE.w: no match found for macro arguments
    .endif
    .endm


;......................
; MOVE.word source, destination
_htk.MOVE.sw    .macro

    .if (\#<1)
    .fail Macro requires at least two arguments
    .endif

    .if (\#>3)
    .fail Macro requires at least two arguments
    .endif

    .if (\#=3 & (\2!=REG_X & \2!=REG_Y))
    .fail For a split index, second argument needs to be an index reg REG_X or REG_Y
    .endif

    ; Do split with index
    .if (\#=3)

        .if (\3!=REG_AX & \3!=REG_AY & \3!=REG_XY)
            .if (\2=REG_X)
                lda \1.lo,x
                sta \3
                lda \1.hi,x
                sta \3+1
            .endif
            .if (\2=REG_Y)
                lda \1.lo,y
                sta \3
                lda \1.hi,y
                sta \3+1
            .endif
        .endif

        .if (\2=REG_X & \3=REG_AX)
            lda \1.hi,x
            ldx \1.lo,x
        .endif
        .if (\2=REG_X & \3=REG_AY)
            lda \1.hi,x
            ldy \1.lo,x
        .endif
        .if (\2=REG_X & \3=REG_XY)
            lda \1.hi,x
            ldy \1.lo,x
            tax
        .endif
        .if (\2=REG_Y & \3=REG_AX)
            lda \1.hi,y
            ldx \1.lo,y
        .endif
        .if (\2=REG_Y & \3=REG_AY)
            lda \1.hi,y
            ldy \1.lo,y
        .endif
        .if (\2=REG_Y & \3=REG_XY)
            lda \1.hi,y
            ldy \1.lo,y
            tax
        .endif
        .if (\?1=2)

        .endif

    .endif

    ; Do split with no index
    .if (\#=2)
        .if (\2!=REG_AX & \2!=REG_AY & \2!=REG_XY)
            lda \1.lo
            sta \2
            lda \1.hi
            sta \2+1
        .endif
        .if (\2=REG_AX)
            ldx \1.lo
            lda \1.hi
        .endif
        .if (\2=REG_AY)
            ldy \1.lo
            lda \1.hi
        .endif
        .if (\2=REG_XY)
            ldy \1.lo
            ldx \1.hi
        .endif
    .endif

    .if (\?1=1)
    .fail Cannot use A,X, or Y registers as source
    .endif

    .endm


;................................................
_htk.INC.w        .macro
            inc \1
            bne .x_\@
            inc \1 + 1
.x_\@
    .endm


;......................
;ADD.word source,destination. 16bit + 16bit->16bit
_htk.ADD.w        .macro

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
            lda #high(\1)
            adc \2 + 1
            sta \2 + 1
        .endif

        .if (\?2=4)    ;indirect dest
            lda #low(\1)
            clc
            adc \2
            sta \2
            phy
            ldy #$01
            lda #high(\1)
            adc \2,y
            sta \2,y
            ply
        .endif
    .endif

    .if (\?1=3 | \?1=6) ;src=addr/label
        .if (\?2=3 | \?2=6)
            lda \1
            clc
            adc \2
            sta \2
            lda \1 + 1
            adc \2 + 1
            sta \2 + 1
        .endif

        .if (\?2=4)    ;indirect dest
            lda \1
            clc
            adc \2
            sta \2
            phy
            ldy #$01
            lda \1 + 1
            adc \2,y
            sta \2,y
            ply
        .endif
    .endif

    .if (\?1=4) ;src=indirect
        .if (\?2=3 | \?2=6)
            lda \1
            clc
            adc \2
            sta \2
            phy
            ldy #$01
            lda \1,y
            adc \2 + 1
            sta \2 + 1
            ply
        .endif

        .if (\?2=4)    ;indirect dest
            lda \1
            clc
            adc \2
            sta \2
            phy
            ldy #$01
            lda \1,y
            adc \2,y
            sta \2,y
            ply
        .endif
    .endif


    .endm


;......................
;ADD.byte source,destination
_htk.ADD.b        .macro
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
;AND.byte source,destination. dest & src -> dest
_htk.AND.b  .macro

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
_htk.OR.b  .macro

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


;,........................................
_htk.DEBUG_NOP   .macro
    .ifdef hutrack.debug.enable
        nop
        nop
        nop
        nop
    .endif
  .endm



;......................
;PUSHBANK.1  addr
_htk.PUSHBANK.1        .macro
    .if (\#=0)
    .fail Macro requires one argument
    .endif

        tma #(\1)
        pha
    .endm

;......................
;PUSHBANK.2  addr
_htk.PUSHBANK.2        .macro
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
_htk.PUSHBANK.3        .macro
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
_htk.PUSHBANK.4        .macro
    .if (\#=0)
    .fail Macro requires one argument
    .endif


        tma #(\1)
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
_htk.PULLBANK.1        .macro
    .if (\#=0)
    .fail Macro requires one argument
    .endif


        pla
        tam #(\1)
    .endm

;......................
;PULLBANK.2 addr
_htk.PULLBANK.2        .macro
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
_htk.PULLBANK.3        .macro
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
_htk.PULLBANK.4        .macro
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
_htk.MAP_BANK        .macro                ;8k

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

_htk.MAP_BANK.2        .macro        ;16k

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


_htk.MAP_BANK.3        .macro        ;24k

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

_htk.MAP_BANK.4        .macro        ;32k

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

