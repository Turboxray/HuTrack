


4000
6000
8000
a000
c000
e000






; [INTERRUPT CODE]

rts:
	rts
rti:
	rti

; ----
; irq2
; ----
; IRQ2 interrupt handler
; ----

.if !(CDROM)
irq2:
	bbs0 <irq_m,.user
	rti
.user:
	jmp   [irq2_jmp]
.endif	; !(CDROM)

; ----
; irq1
; ----
; VDC interrupt handler
; ----

.if !(CDROM)

irq1:
	bbs1 <irq_m,user_irq1	; jump to the user irq1 vector if bit set
	; --
	pha			; save registers
	phx
	phy
	; --
	lda   video_reg		; get VDC status register
	sta  <vdc_sr		; save a copy

    ; ----
    ; vsync interrupt
    ;
.vsync:
	bbr5 <vdc_sr,.hsync
	; --
	inc   irq_cnt		; increment IRQ counter
	; --
	st0   #5		; update display control (bg/sp)
	lda  <vdc_crl
	sta   video_data_l
	; --
	bbr5 <irq_m,.vsync_default
    jmp [user_vsync]

  .vsync_default
	; --
	jsr  vsync_hndl
	; --
    ; ----
    ; hsync interrupt
    ;
.hsync:
	bbr2 <vdc_sr,.exit
	bbr7 <irq_m,.hsync_default
    jmp [user_hsync]

  .hsync_default
	; --
	jsr  hsync_hndl

    ; ----
    ; exit interrupt
    ;
.exit:
	lda  <vdc_reg		; restore VDC register index
	sta   video_reg
	; --
	ply
	plx
	pla
	rti

.endif	; !(CDROM)


    ; ----
    ; user routine hooks
    ;
user_irq1:
	jmp   [irq1_jmp]


; ----
; vsync_hndl
; ----
; Handle VSYNC interrupts
; ----
vsync_hndl:

.if  !(CDROM)
	ldx   disp_cr		; check display state (on/off)
	bne  .l1
	and   #$3F		; disable display
	st0   #5		; update display control (bg/sp)
	sta   video_data_l
	bra  .l2
	; --	
.else
        ; The CD-ROM version only acts if the display state has changed
        ; (disp_cr != 0).
        ldx	disp_cr
        beq	.l1
        stz	disp_cr
        dex
        beq	.m1
        jsr	ex_dspon
        bra	.l1
.m1:	jsr	ex_dspoff
.endif

.l1:	jsr   xfer_palette	; transfer queued palettes

	jsr   rcr_init		; init display list

.l2:	st0   #7		; scrolling
	stw   bg_x1,video_data
	st0   #8
	stw   bg_y1,video_data

	; --
	lda   clock_tt		; keep track of time
	inc   A
	cmp   #60
	bne   .lcltt
	lda   clock_ss
	inc   A
	cmp   #60
	bne   .lclss
	lda   clock_mm
	inc   A
	cmp   #60
	bne   .lclmm
	inc   clock_hh
	cla
.lclmm:	sta   clock_mm
	cla
.lclss:	sta   clock_ss
	cla
.lcltt:	sta   clock_tt
	; --

.if  (CDROM)
	jsr   ex_colorcmd
	; XXX: Why call this every vsync, when it's called from rand()
	; as needed anyway?
	inc   rndseed
	jsr   randomize
.endif

	; invoke the sound driver's vsync irq code

	__sound_vsync

.ifdef SUPPORT_MOUSE
	lda   msflag		; if mouse supported, and exists
	beq  .l3		; then read mouse instead of pad
	jsr   mousread
	bra  .out
.endif	; SUPPORT_MOUSE

.l3:	jsr   read_joypad	; else read joypad
.out:	rts


; ----
; hsync_hndl
; ----
; Handle HSYNC interrupts
; ----
    ; ----
    ; hsync scrolling handler
    ;
hsync_hndl:

	ldy   s_idx
	bpl  .r1
	; --
	lda  <vdc_crl
	and   #$3F
	sta  <vdc_crl
	stz   s_idx
	ldx   s_list
	lda   s_top,X
	jsr   rcr5
	rts
	; --
.r1:	ldx   s_list,Y
	lda  <vdc_crl
	and   #$3F
	ora   s_cr,X
	sta  <vdc_crl
	; --
	jsr   rcr_set
	; --
	lda   s_top,X
	cmp   #$FF
	beq  .out
	; --
	st0   #7
	lda   s_xl,X
	ldy   s_xh,X
	sta   video_data_l
	sty   video_data_h
	st0   #8
	lda   s_yl,X
	ldy   s_yh,X
	sub   #1
	bcs  .r2
	dey
.r2:	sta   video_data_l
	sty   video_data_h
.out:	rts

    ; ----
    ; init display list
    ;
rcr_init:
	maplibfunc   build_disp_list
	bcs  .r3
	rts
	; --
.r3:	smb   #7,<vdc_crl
	lda   #$FF
	sta   s_idx
	ldx   s_list
	ldy   s_top,X
	cpy   #$FF
	bne   rcr5
	; --
	ldy   s_xl,X
	sty   bg_x1
	ldy   s_xh,X
	sty   bg_x1+1
	ldy   s_yl,X
	sty   bg_y1
	ldy   s_yh,X
	sty   bg_y1+1
	stz   s_idx
	bra   rcr5

    ; ----
    ; program scanline interrupt
    ;
rcr_set:
	iny
	sty   s_idx
	lda   s_list,Y
	tay
	lda   s_top,Y
	cmp   scr_height
	bhs   rcr6
	cmp   s_bottom,X
	blo   rcr5
	; --
	lda   s_bottom,X
rcr4:	dec   A
	pha
	lda   #$F0
	sta   s_bottom,X
	stz   s_cr,X
	dec   s_idx
	pla
	; --
rcr5:	st0   #6		; set scanline counter
	add   #64
	sta   video_data_l
	cla
	adc   #0
	sta   video_data_h
	bra   __rcr_on
	;--
rcr6:	lda   s_bottom,X
	cmp   scr_height
	blo   rcr4
	bra   __rcr_off

; ----
; rcr_on
; ----
; enable scanline interrupt
; ----

_rcr_on:
 	lda   #5
	sta  <vdc_reg
__rcr_on:
	st0   #5
	lda  <vdc_crl
	ora   #$04
	sta  <vdc_crl
	sta   video_data_l
	rts

; ----
; rcr_off
; ----
; disable scanline interrupt
; ----

_rcr_off:
	lda   #5
	sta  <vdc_reg
__rcr_off:
	st0   #5
	lda  <vdc_crl
	and   #$FB
	sta  <vdc_crl
	sta   video_data_l
	rts



; ----
; timer
; ----
; timer interrupt handler
; ----

.if  !(CDROM)

timer_user:	jmp		[timer_jmp]

timer:		bbs2		<irq_m,timer_user
		pha
		phx
		phy

		sta		irq_status	; acknowledge interrupt

		; invoke the sound driver's timer irq code

		__sound_timer

		ply
		plx
		pla
		rti

.endif	; !(CDROM)

; ----
; nmi
; ----
; NMI interrupt handler
; ----

.if  !(CDROM)
nmi:
	bbs3 <irq_m,.user
	rti
.user:
	jmp   [nmi_jmp]
.endif	; !(CDROM)




