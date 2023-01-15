;///////////////////////////////////////////////////////////////////////////////
;///////////////////////////////////////////////////////////////////////////////
;///////////////////////////////////////////////////////////////////////////////
;
; MACROS
;

PRINT_STR		.macro
      lda #low(\1)
      sta <R0
      lda #high(\1)
      sta <R0+1
      lda #low((\3 * $40)+(\2 & $3f))
      ldx #high((\3 * $40)+(\2 & $3f))
 			clc
      jsr PrintString
	.endm



PRINT_STR_q		.macro
      lda #low((\2 * $40)+(\1 & $3f))
      ldx #high((\2 * $40)+(\1 & $3f))
			clc
      jsr PrintString
	.endm

PRINT_STR_s		.macro
			lda \1
			and #$3f
			sta <D7
			lda \2
			asl a
			asl a
			asl a
			asl a
			asl a
			asl a
			clc
			adc <D7
			sax
			lda \2
			lsr a
			lsr a
			sax
			clc
      jsr PrintString
	.endm


PRINT_STR_a		.macro
			sec
      jsr PrintString
	.endm

PRINT_STR_a_ptr		.macro
      lda #low(\1)
      sta <R0
      lda #high(\1)
      sta <R0+1
			sec
      jsr PrintString
	.endm

PRINT_STR_i   .macro
      bra .y_\@
.x_\@:
      .db \1,0
.y_\@:
      lda #low(.x_\@)
      sta <R0
      lda #high(.x_\@)
      sta <R0+1
			lda #low((\3 * $40)+(\2 & $3f))
			ldx #high((\3 * $40)+(\2 & $3f))
      clc
      jsr PrintString
  .endm


PRINT_STR_i_a   .macro
      bra .y_\@
.x_\@:
      .db \1,0
.y_\@:
      lda #low(.x_\@)
      sta <R0
      lda #high(.x_\@)
      sta <R0+1
      sec
      jsr PrintString
  .endm

PRINT_STR_a_i  .macro
      bra .y_\@
.x_\@:
      .db \1,0
.y_\@:
      lda #low(.x_\@)
      sta <R0
      lda #high(.x_\@)
      sta <R0+1
      sec
      jsr PrintString
  .endm

;...........................................

PRINT_BYTEdec		.macro
      lda #low((\3 * $40)+(\2 & $3f))
      ldx #high((\3 * $40)+(\2 & $3f))
      ldy \1
			clc
      jsr PrintByteDec
	.endm

PRINT_BYTEdec_q		.macro
      lda #low((\2 * $40)+(\1 & $3f))
      ldx #high((\2 * $40)+(\1 & $3f))
			clc
      jsr PrintByteDec
	.endm

PRINT_BYTEdec_a_q		.macro
			ldy \1
			sec
      jsr PrintByteDec
	.endm

PRINT_BYTEhex_a_q		.macro
			ldy \1
			sec
      jsr PrintByte
	.endm

PRINT_LO_Nibblehex_a_q		.macro
			ldy \1
			sec
      jsr print_lo_nibble
	.endm

PRINT_HI_Nibblehex_a_q		.macro
			ldy \1
			sec
      jsr print_hi_nibble
	.endm



PRINT_BYTEhex		.macro
      lda #low((\3 * $40)+(\2 & $3f))
      ldx #high((\3 * $40)+(\2 & $3f))
      ldy \1
			clc
      jsr PrintByte
	.endm

PRINT_BYTEhex_q		.macro
      lda #low((\2 * $40)+(\1 & $3f))
      ldx #high((\2 * $40)+(\1 & $3f))
			clc
      jsr PrintByte
	.endm


;...........................................
PRINT_CHAR_s		.macro
			lda \1
			and #$3f
			sta <D7
			lda \2
			asl a
			asl a
			asl a
			asl a
			asl a
			asl a
			clc
			adc <D7
			sax
			lda \2
			lsr a
			lsr a
			sax
			clc
      jsr PrintChar
	.endm


PRINT_CHAR		.macro
      lda #low((\2 * $40)+(\1 & $3f))
      ldx #high((\2 * $40)+(\1 & $3f))
			clc
      jsr PrintChar
	.endm


PRINT_CHAR_a		.macro
			sec
      jsr PrintChar
	.endm

PRINT_CHAR_a_q		.macro
			ldy \1
			sec
      jsr PrintChar
	.endm

PRINT_CHAR_a_Acc		.macro
			tay
			sec
      jsr PrintChar
	.endm

PRINT_CHAR_a_X		.macro
			sxy
			sec
      jsr PrintChar
	.endm

;...........................................
PRINT_DBYTEhex_a		.macro
			ldy \1+1
			sec
      jsr PrintByte
			ldy \1
			sec
      jsr PrintByte
	.endm


;...........................................

PRINT_STATUS	.macro
			lda #\2
			sta <D3
			lda #\3
			sta <D3+1

			lda #low(\1)
			sta <A1
			lda #high(\1)
			sta <A1+1

		jsr PrintStatus
	.endm




