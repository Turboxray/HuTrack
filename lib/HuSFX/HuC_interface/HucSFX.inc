// ;////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ;
// ; HuSFX HuC macros for PC-Engine
// ;
// ; Ver: 1.0.0
// ;
// ; History:
// ; -------
// ;
// ;
// ;

//..........................................................................
//..........................................................................
//..........................................................................
//..........................................................................
void __fastcall __macro HuSFXstop_intf( char channel<__al> );
#asm
_HuSFXstop_intf.1   .macro

        ldx <__al
        cpx #$06
      bcs .error\@

        lda #$ff
        sta HuSFX.stream.bnk,x

            php
        sei
        lda #$d0
        stx $800
        stz $804
            plp

            php
        sei
        nop
        stx $800
        stz $807
            plp

        lda #$01
        tax
        clc
      bra .return\@
    
.error\@
        clx
        cla
        sec

.return\@
.endm

#endasm   

//..........................................................................
//..........................................................................
//..........................................................................
//..........................................................................
void __fastcall __macro HuSFX_Init_intf(void);
#asm
_HuSFX_Init_intf    .macro
        clx
        lda #$ff
.loop
        sta HuSFX.stream.bnk,x
        inx
        cpx #$06
      bne .loop
.endm

#endasm   

//..........................................................................
//..........................................................................
//..........................................................................
//..........................................................................
// HuSFXplay
int __fastcall __macro HuSFXplay_intf( char channel<__al>, unsigned char bank1<__fbank>, unsigned int addr1<__fptr>, unsigned char bank2<__cl>, unsigned int addr2<__bx>);
#asm
_HuSFXplay_intf.5 .macro
        ldx <__al
        cpx #$06
      bcs .error\@

        lda <__fbank
        sta HuSFX.stream.bnk,x
        lda <__fptr
        sta HuSFX.stream.lo,x
        lda <__fptr + 1
        sta HuSFX.stream.hi,x
        lda <__cl
        sta HuSFX.wf.bnk,x
        lda <__bx
        sta HuSFX.wf.lo,x
        lda <__bx + 1
        sta HuSFX.wf.hi,x

            php
        sei
        nop
        stx $800
        stz $807
            plp

            php
        sei
        nop
        stx $800
        stz $808
            plp

        lda #$01
        tax
        clc
      bra .return\@

.error\@
        clx
        cla
        sec

.return\@
.endm

#endasm

//..........................................................................
//..........................................................................
//..........................................................................
//..........................................................................
// HuSFXprocess
int __fastcall __macro HuSFXprocess_intf();
#asm
_HuSFXprocess_intf  .macro

          jsr .HuSFX.process\@
          clx
          cla
          sec
        jmp .return_huc\@

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
.HuSFX.process\@

        clx
.loop\@
        lda HuSFX.stream.bnk,x
        cmp #$ff
      beq .skip_entry\@

        lda HuSFX.delay,x
      bmi .skip_entry\@
      beq .do_entry\@
        dec HuSFX.delay,x
      bra .skip_entry\@

.do_entry\@
        jmp .process\@
.return_entry\@

.skip_entry\@
        inx
        cpx #$06
      bne .loop\@
;   rts    
    .db $60


.process\@
        ; Map in stream
        tma #$02
        pha
        tma #$03
        pha
        lda HuSFX.stream.bnk,x
        tam #$02
        inc a
        tam #$03

        ; Prep stream pointer
        lda HuSFX.stream.lo,x
        sta <HuSFX.A0
        lda HuSFX.stream.hi,x
        and #$1f
        ora #$40
        sta <HuSFX.A0 + 1


.decode_byte\@
        jsr .fetch_byte\@

        cmp #$A0
      bcs .next1\@
        jmp .804\@            ; < #$A0
.next1\@
        cmp #$B0
      bcs .next2\@
        jmp .reg_update\@     ; < #$B0
.next2\@
      bne .next3\@
        jmp .wf_update\@      ; == #$A0
.next3\@
        cmp #$D0
      bcs .next4\@
        jmp .frq_update\@     ; < #$D0
.next4\@
        cmp #$fb
      bne .next5\@
        jmp .eof\@            ; == #$FB
.next5\@
        cmp #$fc
      bne .next6\@
        jmp .play_pcm\@
.next6\@
        cmp #$fd
      bne .next7\@
        jmp .stop_pcm\@
.next7\@
        cmp #$fe
      bne .next8\@
        jmp .wait_n_frames\@
.next8\@
        cmp #$ff
      bne .next9\@
        jmp .wait_1_frame\@
.next9\@


;..............
.804\@
        sta HuSFX.control,x
            php
        sei
        stx $800
        sta $804
            plp
      jmp .decode_byte\@

;..............
.wf_update\@

        ;// This is a slow, but for now it works.

        lda #(HuSFX.DMA.TINop)
        sta HuSFX.DMA + 0
        lda #(HuSFX.DMA.RTSop)
        sta HuSFX.DMA + 7

        tma #$02
        pha
        tma #$03
        pha

      jsr .fetch_byte\@

          cly
          asl a
          say
          rol a
          say

          asl a
          say
          rol a
          say

          asl a
          say
          rol a
          say

          asl a
          say
          rol a
          say

          asl a
          say
          rol a
          say
          sty HuSFX.DMA + 2

        clc
        adc HuSFX.wf.lo,x
        sta HuSFX.DMA + 1
        lda HuSFX.wf.hi,x
        and #$1f
        ora #$40
        adc HuSFX.DMA + 2
        sta HuSFX.DMA + 2

        lda #low($806)
        sta HuSFX.DMA + 3
        lda #high($806)
        sta HuSFX.DMA + 4

        lda #low(32)
        sta HuSFX.DMA + 5
        lda #high(32)
        sta HuSFX.DMA + 6

        lda HuSFX.wf.bnk,x

        tam #$02
        inc a
        tam #$03

        lda HuSFX.control,x
        tay
        and #$1f
        ora #$40
          php
            sei
            stx $800
            sta $804
            tya
            and #$1f
            sta $804

            jsr HuSFX.DMA
            tya
            sta $804
          plp

        pla
        tam #$03
        pla
        tam #$02

      jmp .decode_byte\@

;..............
.reg_update\@
        and #$0f
        tay
      jsr .fetch_byte\@
            php
        sei
        stx $800
        sta $800,y
            plp
      jmp .decode_byte\@


;..............
.frq_update\@
        and #$0f
        tay
      jsr .fetch_byte\@
            php
        sei
        stx $800
        sta $802
        sty $803
            plp
      jmp .decode_byte\@


;..............
.eof\@
        lda #$ff
        sta HuSFX.stream.bnk,x

            php
        sei
        lda #$d0
        stx $800
        sta $804
            plp

            php
        sei
        nop
        stx $800
        stz $807
            plp

            php
        sei
        nop
        stx $800
        stz $808
            plp


      jmp .exit_parse\@

;..............
.play_pcm\@
      jsr .fetch_byte\@
      jsr .fetch_byte\@
        ; Skip PCM operands for now
      jmp .decode_byte\@

;..............
.stop_pcm\@
        ; TODO
      jmp .decode_byte\@

;..............
.wait_n_frames\@
      jsr .fetch_byte\@
        and #$7f
        sta HuSFX.delay,x
      jmp .exit_parse\@
;..............
.wait_1_frame\@
        stz HuSFX.delay,x
      jmp .exit_parse\@


;.............................
.inc_ptr\@
            pha
        inc <HuSFX.A0
      bne .inc_ptr.out\@
        inc <HuSFX.A0 + 1
        lda <HuSFX.A0 + 1
        cmp #$60
      bne .inc_ptr.out\@
        and #$1f
        ora #$40
        sta <HuSFX.A0 + 1
        inc HuSFX.stream.bnk,x
        lda HuSFX.stream.bnk,x
        tam #$02
        inc a
        tam #$03
.inc_ptr.out\@
            pla
;   rts
    .db $60

;..................
.fetch_byte\@
        lda [HuSFX.A0]
      jmp .inc_ptr\@


;..................
.exit_parse\@
        lda <HuSFX.A0
        sta HuSFX.stream.lo,x
        lda <HuSFX.A0 + 1
        sta HuSFX.stream.hi,x



        pla
        tam #$03
        pla
        tam #$02
    jmp .return_entry\@

.return_huc\@

.endm
#endasm


//..........................................................................
//..........................................................................
//..........................................................................
//..........................................................................
// HuSFXstatus
int __fastcall __macro HuSFXstatus_intf( char channel<__al> );
#asm
_HuSFXstatus_intf.1 .macro

        ldx <__al
        cpx #$06
      bcs .error\@

        lda HuSFX.stream.bnk,x
        cmp #$ff
      bra .noplay\@
        tax
        clc
      bra .return\@

.noplay\@
.error\@
        clx
        cla
        sec

.return\@
.endm

#endasm
