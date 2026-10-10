
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
; HuSFX
;
; \file HuSFX_lib.asm
;
; Ver: 0.1
;
; History:
; -------
;
;
;

;//...............................................................................................................
;//...............................................................................................................
;//...............................................................................................................
;//...............................................................................................................
;//
;int __fastcall HuSFXprocess();
_HuSFXprocess:

          jmp HuSFX.process

;//.........................................................
; int __fastcall HuSFXplay( char channel<__al>, unsigned char bank1<__fbank>, unsigned int addr1<__fptr>, unsigned char bank2<__cl>, unsigned int addr2<__bx>)
_HuSFXplay.5
        ldx <__al
        cpx #$06
      bcs .error

      php
      sei
      stz HuSFX.delay,x
      stz HuSFX.rawControl,x
      stz HuSFX.control,x
      lda #$ff
      sta HuSFX.rawPan,x
      stx $800
      stz $804
      stz $807
      cpx #2
    bcs .pointers
      stz $809
.pointers
      lda <__fptr
      sta HuSFX.stream.lo,x
      lda <__fptr + 1
      sta HuSFX.stream.hi,x
      lda <__cl
      sta HuSFX.wf.bnk
      lda <__bx
      sta HuSFX.wf.lo
      lda <__bx + 1
      sta HuSFX.wf.hi
      ; Publish the stream only after all pointers and caches are installed.
      lda <__fbank
      sta HuSFX.stream.bnk,x
      plp

        ; HuC returns high A / low X; HuCC returns high Y / low A.
        cla
        ldx #$01
        .ifdef HUCC
        sax
        sxy
        .endif
        clc
.out    
  rts

.error
        clx
        cla
        cly
        sec
  rts

;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
; Input EAX0.l
HuSFX.process

        clx
.loop
        lda HuSFX.stream.bnk,x
        cmp #$ff
      beq .skip_entry

        jsr .refresh.gain
        lda HuSFX.delay,x
      beq .do_entry
        dec HuSFX.delay,x
      bra .skip_entry

.do_entry
        jmp .process
.return_entry

.skip_entry
        inx
        cpx #$06
      bne .loop
  rts    


.refresh.gain
        lda HuSFX.rawControl,x
        HuSFX.MixVolume
        cmp HuSFX.control,x
      beq .refresh.pan
        sta HuSFX.control,x
        php
        sei
        stx $800
        sta $804
        plp
.refresh.pan
        lda HuSFX.rawPan,x
        HuSFX.MixPan
        cmp HuSFX.pan,x
      beq .refresh.done
        sta HuSFX.pan,x
        php
        sei
        stx $800
        sta $805
        plp
.refresh.done
        rts

.process
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


.decode_byte
        jsr .fetch_byte

        cmp #$A0
      bcs .next1
        ; The converter packs $C0..$DF DDA controls into $20..$3F.
        ; Raw A4 operands jump directly to .804 and must not be expanded.
        cmp #$20
      bcc .control.ready
        cmp #$40
      bcs .control.ready
        eor #$e0
.control.ready
        jmp .804
.next1
        cmp #$B0
      bcs .next2
        jmp .reg_update     ; < #$B0
.next2
      bne .next3
        jmp .wf_update      ; == #$B0
.next3
        cmp #$D0
      bcs .next4
        jmp .frq_update     ; < #$D0
.next4
        cmp #$fb
      bne .next5
        jmp .eof            ; == #$FB
.next5
        cmp #$fc
      bne .next6
        jmp .play_pcm
.next6
        cmp #$fd
      bne .next7
        jmp .stop_pcm
.next7
        cmp #$fe
      bne .next8
        jmp .wait_n_frames
.next8
        cmp #$ff
      bne .next9
        jmp .wait_1_frame
.next9


;..............
.804
        sta HuSFX.rawControl,x
        HuSFX.MixVolume
        sta HuSFX.control,x
            php
        sei
        stx $800
        sta $804
            plp
      jmp .decode_byte

;..............
.wf_update

        ;// This is a slow, but for now it works.

        lda #(HuSFX.DMA.TINop)
        sta HuSFX.DMA + 0
        lda #(HuSFX.DMA.RTSop)
        sta HuSFX.DMA + 7

        ; Fetch may advance the stream into the next bank. Save that updated
        ; mapping so decoding resumes at the bank containing the next opcode.
        jsr .fetch_byte
        tay
        tma #$02
        pha
        tma #$03
        pha
        tya

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
        adc HuSFX.wf.lo
        sta HuSFX.DMA + 1
        lda HuSFX.wf.hi
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

        lda HuSFX.wf.bnk

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

      jmp .decode_byte

;..............
.reg_update
        and #$0f
        tay
      jsr .fetch_byte
        ; AA/AB are pattern metadata, not PSG register writes.
        cpy #10
      bcc .register.hardware
        jmp .decode_byte
.register.hardware
        cpy #4
      bne .register.notControl
        jmp .804
.register.notControl
        cpy #5
      bne .register.write
        sta HuSFX.rawPan,x
        HuSFX.MixPan
        sta HuSFX.pan,x
.register.write
            php
        sei
        stx $800
        sta $800,y
            plp
      jmp .decode_byte


;..............
.frq_update
        and #$0f
        tay
      jsr .fetch_byte
            php
        sei
        stx $800
        sta $802
        sty $803
            plp
      jmp .decode_byte


;..............
.eof
        lda #$ff
        sta HuSFX.stream.bnk,x
          php
          sei
        stx $800
        stz $804
        stz $807
        cpx #2
      bcs .lfo.done
        stz $809
.lfo.done
          plp
      jmp .exit_parse

;..............
.play_pcm
      jsr .fetch_byte
      jsr .fetch_byte
        ; Skip PCM operands for now
      jmp .decode_byte

;..............
.stop_pcm
        ; TODO
      jmp .decode_byte

;..............
.wait_n_frames
      jsr .fetch_byte
      beq .wait.store
        dec a
.wait.store
        sta HuSFX.delay,x
      jmp .exit_parse
;..............
.wait_1_frame
        stz HuSFX.delay,x
      jmp .exit_parse


;.............................
.inc_ptr
            pha
        inc <HuSFX.A0
      bne .inc_ptr.out
        inc <HuSFX.A0 + 1
        lda <HuSFX.A0 + 1
        cmp #$60
      bne .inc_ptr.out
        and #$1f
        ora #$40
        sta <HuSFX.A0 + 1
        inc HuSFX.stream.bnk,x
        lda HuSFX.stream.bnk,x
        tam #$02
        inc a
        tam #$03
.inc_ptr.out
            pla
  rts

;..................
.fetch_byte
        lda [HuSFX.A0]
      jmp .inc_ptr


;..................
.exit_parse
        lda <HuSFX.A0
        sta HuSFX.stream.lo,x
        lda <HuSFX.A0 + 1
        sta HuSFX.stream.hi,x

        pla
        tam #$03
        pla
        tam #$02
    jmp .return_entry



;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

;...............................................
; Input EAX0.l

