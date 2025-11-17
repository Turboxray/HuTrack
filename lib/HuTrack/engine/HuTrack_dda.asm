;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// DDA Playback                                                                                            /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;#int_routine

;##############################################################################
;##############################################################################

HuTrackEngine.7khz.IRQ:

                                            ;8 initial ISR call overhead
        stz _htk.IRQ.ackTIRQ                ;5
        bit <HuTrack.DDAprocess             ;4      ISR lock
      bvs .in_progress                      ;2
        cli                                 ;2
      bmi .HuTrack.disabled                 ;2

          pha
          phy 
        inc <HuTrack.DDAprocess            ;6
        stz <HuTrack.dda.BufferReload

.DDA
        phx                               ;3          
        ldx #$05                            ;2

          

.DDA.loop
      
      lda <HuTrack.dda.SamplePos,x 
      beq .next                             ;2
      inc <HuTrack.dda.SamplePos,x        
      tay                                     
      lda HuTrack.dda.buffer,y    
      sei
      stx _htk.WSG.ChannelSelect          ;5
      sta _htk.WSG.DDAport                ;5
      cli            
      bpl .next 
      inc <HuTrack.dda.BufferReload  
.next
      dex                                 ;2
      bpl .DDA.loop                       ;4 = 60


.finished
        lda HuTrack.dda.BufferReload
        bne  .DDA_replenish
.EndBuffer          
          plx                               ;
          ply
.return
        pla                               ;4
        dec <HuTrack.DDAprocess             ;6
.HuTrack.disabled

.in_progress
    rti                                     ;7 = 30

.DDA_replenish:   
    ldx #5   
.replenish_loop:    
    lda <HuTrack.dda.SamplePos,x         
    beq .next_replenish                             ;2
    tay                      
    dey ;Need to remove extra bump after getting samples               
    lda HuTrack.dda.buffer,y      
    bit #$20 ;Compressed 
    beq .DDA_checkend 
    jmp .DDA_compressloop  
.DDA_checkend   
    bit #$40 ;end 
    bne .DDA_uncompressed
    stz <HuTrack.dda.SamplePos,x 
    bra .next_replenish
.DDA_uncompressed:    
    lda SamplePosMatrix,x ;Get the "Zero point" for that channel, i.e. 1,43,85,127,169,211
    sta <HuTrack.dda.SamplePos,x 
    tay
    tma #$02 ;Get Bank
    pha  ;Save Bank 
    lda HuTrack.dda.bank,x 
    tam #$02     
    ;copy the pointer over
    lda HuTrack.dda.addr.lo,x          ;4
    sta <HuTrack.dda.ptr                ;4
    lda HuTrack.dda.addr.hi,x          ;4
    sta <HuTrack.dda.ptr + 1            ;4
    phx  ;save the channel for later   
    ldx #41 ;loop variable     
    dey ;We need to increment y after looping, so we start -1 
.uncompressed_loop:
    iny 
    lda [HuTrack.dda.ptr]    
  bmi .FinishUncompressed 
    sta HuTrack.dda.buffer,y
    inc HuTrack.dda.ptr
  beq .overflow1 
.next_uncomp:    
    dex  
  bpl .uncompressed_loop  
    lda HuTrack.dda.buffer,y ;Can get a race situation if we have to load a bank 
    ora #$80 
    sta HuTrack.dda.buffer,y ;Need to ensure we replenish the buffer
    plx 
    lda <HuTrack.dda.ptr 
    sta HuTrack.dda.addr.lo,x    
    lda <HuTrack.dda.ptr+1 
    sta HuTrack.dda.addr.hi,x    
    tma #$02 
    sta HuTrack.dda.bank,x 
    bra .next_replenish_bank

.FinishUncompressed:
    lda #$D0 ;8 + 4 + 1 8 for flag to do something, 4 for flag end, and 10 for "empty sample" 
    sta HuTrack.dda.buffer,y     
    plx 
    ;bra .next_replenish_bank ;Already there
.next_replenish_bank:
    pla 
    tam #$02
.next_replenish:     
    dex 
    bpl .replenish_loop
    jmp .EndBuffer

.overflow1:
        inc <HuTrack.dda.ptr+1
        lda <HuTrack.dda.ptr+1 
        cmp #$60
      bcc .next_uncomp
        lda #$40
        sta <HuTrack.dda.ptr+1 
        tma #$02         
        adc #0 
        tam #$02         
      bra .next_uncomp

    
.DDA_compressloop:
    lda SamplePosMatrix,x ;Get the "Zero point" for that channel, i.e. 1,43,85,127,169,211
    sta <HuTrack.dda.SamplePos,x 
    tay
    tma #$02 ;Get Bank
    pha  ;Save Bank 
    lda HuTrack.dda.bank,x 
    tam #$02     
    ;copy the pointer over
    lda HuTrack.dda.addr.lo,x          ;4
    sta <HuTrack.dda.ptr                ;4
    lda HuTrack.dda.addr.hi,x          ;4
    sta <HuTrack.dda.ptr + 1            ;4
    phx  ;save the channel for later   
    ldx #13;loop variable     
    dey ;We need to increment y after looping, so we start -1 
.compressed_loop: 
    iny 
    lda [HuTrack.dda.ptr]    
    sta <HuTrack.dda.BufferHold1
    and #$F8
    lsr a 
    lsr a 
    lsr a 
    sta HuTrack.dda.buffer,y    
    iny 
    lda <HuTrack.dda.BufferHold1
    and #7
    sta <HuTrack.dda.BufferHold1
    inc <HuTrack.dda.ptr
    beq .overflow2 
.next_comp1:    
    lda [HuTrack.dda.ptr] 
    sta <HuTrack.dda.BufferHold2
    and #$60
    lsr a 
    lsr a 
    ora <HuTrack.dda.BufferHold1        
    sta HuTrack.dda.buffer,y
    iny 
    lda <HuTrack.dda.BufferHold2
    bmi .finish_compressed_sample ;Ignore last sample value, 
    and #$1F  
    sta HuTrack.dda.buffer,y    
    inc <HuTrack.dda.ptr
    beq .overflow3
.next_comp2:    
    dex 
    bpl .compressed_loop
    lda HuTrack.dda.buffer,y
    ora #$A0 ;We're compressed, so set $20, also we need to loop so set $80
    sta HuTrack.dda.buffer,y
    plx 
    jmp .next_replenish_bank
.finish_compressed_sample:    
    lda #$D0 ;8 + 4 + 1 8 for flag to do something, 4 for flag end, and 10 for "empty sample" 
    sta HuTrack.dda.buffer,y     
    plx 
    jmp .next_replenish_bank
    
.overflow2:
        inc <HuTrack.dda.ptr+1
        lda <HuTrack.dda.ptr+1 
        cmp #$60
      bcc .next_comp1
        lda #$40
        sta <HuTrack.dda.ptr+1 
        tma #$02         
        adc #0 
        tam #$02         
      bra .next_comp1 

.overflow3:
        inc <HuTrack.dda.ptr+1
        lda <HuTrack.dda.ptr+1 
        cmp #$60
      bcc .next_comp2
        lda #$40
        sta <HuTrack.dda.ptr+1 
        tma #$02         
        adc #0 
        tam #$02         
      bra .next_comp2 




