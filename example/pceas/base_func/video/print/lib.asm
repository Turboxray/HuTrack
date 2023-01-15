
include "../base_func/video/print/print.inc"

;...............................................................................
;//Print string ascii string
;///////////////////////////
; vram addr in X:A
; string addr in R0
;
PrintString:
    bcs .skip
        stz <vdc_reg
        st0 #$00
        sta $0002
        stx $0003
.skip
        lda #$02
        sta <vdc_reg
        st0 #$02
        cly

.ll01
        lda [R0],y
      beq .out
        sec
        sbc #$20
        sta $0002
        st2 #$01
        iny
    bra .ll01
.out
  rts


;...............................................................................
;//Print variable to x,y location
;/ X:A vram addr
;/ y=value
;/ Carry; 1=append last location, 0=location in X:A
PrintByte:
    bcs .skip
        stz <vdc_reg
        st0 #$00
        sta $0002
        stx $0003
.skip
        lda #$02
        sta <vdc_reg
        st0 #$02
        tya
        tax
        lsr a
        lsr a
        lsr a
        lsr a
        tay
        lda hex_conv,y
        sec
        sbc #$20
        sta $0002
        st2 #$01
        txa
        and #$0f
        tay
        lda hex_conv,y
        sec
        sbc #$20
        sta $0002
        st2 #$01
  rts

print_lo_nibble:
    bcs .skip
        stz <vdc_reg
        st0 #$00
        sta $0002
        stx $0003
.skip
        lda #$02
        sta <vdc_reg
        st0 #$02
        tya
        and #$0f
        tay
        lda hex_conv,y
        sec
        sbc #$20
        sta $0002
        st2 #$01
  rts

print_hi_nibble:
    bcs .skip
        stz <vdc_reg
        st0 #$00
        sta $0002
        stx $0003
.skip
        lda #$02
        sta <vdc_reg
        st0 #$02
        tya
        lsr a
        lsr a
        lsr a
        lsr a
        tay
        lda hex_conv,y
        sec
        sbc #$20
        sta $0002
        st2 #$01
  rts

print_indent:
.ll01
        st1 #$00
        st2 #$00
        dey
    bne .ll01
  rts

;near data table
hex_conv:
    .db '0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'


;...............................................................................
;//Clears the screen with blank space
;/ Note: no arguments, no whining.
;/ Note: This the 64x32 version.
ClearScreen:
            st0 #$00
            st1 #$00
            st2 #$00
            st0 #$02
            lda #$02
            sta <vdc_reg
            clx
            ldy #$08
            st1 #$00
.loop
            st2 #$01
            inx
        bne .loop
            dey
        bne .loop
    rts

;...............................................................................
;//Clears the screen with blank space
;/ Note: no arguments, no whining.
;/ Note: This the 32x32 version.
ClearScreen.32x32:
            st0 #$00
            st1 #$00
            st2 #$00
            st0 #$02
            lda #$02
            sta <vdc_reg
            clx
            ldy #$04
            st1 #$00
.loop
            st2 #$01
            inx
        bne .loop
            dey
        bne .loop
    rts

;...............................................................................
;//Clears the screen with blank space
;/ Note: no arguments, no whining.
;/ Note: This the 64x32 version.
ClearScreen.64x32:
            st0 #$00
            st1 #$00
            st2 #$00
            st0 #$02
            lda #$02
            sta <vdc_reg
            clx
            ldy #$08
            st1 #$00
.loop
            st2 #$01
            inx
        bne .loop
            dey
        bne .loop
    rts

;...............................................................................
;//Clears the screen with blank space
;/ Note: no arguments, no whining.
;/ Note: This the 64x32 version.
ClearScreen.64x64:
            st0 #$00
            st1 #$00
            st2 #$00
            st0 #$02
            lda #$02
            sta <vdc_reg
            clx
            ldy #$10
            st1 #$00
.loop
            st2 #$01
            inx
        bne .loop
            dey
        bne .loop
    rts

;...............................................................................
;//Clears the screen with blank space
;/ Note: no arguments, no whining.
;/ Note: This the 64x32 version.
PrintByteDec:

    bcs .skip
        stz <vdc_reg
        st0 #$00
        sta $0002
        stx $0003
.skip
        lda #$02
        sta <vdc_reg
        st0 #$02

            tya
            cmp #200
        bcc .not200
            sec
            sbc #200
            ldx #$12
        bra .drawUpper
.not200
            cmp #100
        bcc .lowerDigits
            sec
            sbc #100
            ldx #$11

.drawUpper
        stx $0002
        st2 #$01

.lowerDigits
            cly
            cmp #10
        bcc .done
.loop
            iny
            sec
            sbc #10
            cmp #10
        bcs .loop
.done
            say
            clc
            adc #$10
            sta $0002
            st2 #$01
            say
            clc
            adc #$10
            sta $0002
            st2 #$01
    rts

;...............................................................................
;//Clears the screen with blank space
;/ Note: no arguments, no whining.
;/ Note: This the 64x32 version.
PrintChar:

    bcs .skip
        stz <vdc_reg
        st0 #$00
        sta $0002
        stx $0003
.skip
        lda #$02
        sta <vdc_reg
        st0 #$02


            tya
            sec
            sbc #$20
            sta $0002
            st2 #$01
    rts


;//...............................................................................................
;//Internal ZP reg
    .ifndef R0
        .zp
            R0:     .ds 2
R0.l = R0
R0.h = R0+1
    .endif