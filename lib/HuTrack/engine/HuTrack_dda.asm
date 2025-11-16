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
        inc  <HuTrack.DDAprocess            ;6

.DDA

          phx                               ;3
        ldx #$05                            ;2

        tma #$02                            ;4
          pha                               ;3 = 33

.DDA.loop
        lda <HuTrack.dda.bank,x             ;4
      bmi .next                             ;2
        tam #$02                            ;5

        lda <HuTrack.dda.addr.lo,x          ;4
        sta <HuTrack.dda.ptr                ;4
        lda <HuTrack.dda.addr.hi,x          ;4
        sta <HuTrack.dda.ptr + 1            ;4
.re_entry
        lda [HuTrack.dda.ptr]               ;7
      bmi .control_flag                     ;2

          sei
        stx _htk.WSG.ChannelSelect          ;5
        sta _htk.WSG.DDAport                ;5
          cli

        inc <HuTrack.dda.addr.lo,x          ;6
      beq .overflow                         ;2

.next
        dex                                 ;2
      bpl .DDA.loop                         ;4 = 60


.finished
          pla                               ;4
        tam #$02                            ;5
          plx                               ;4

.return

          pla                               ;4
        dec <HuTrack.DDAprocess             ;6
.HuTrack.disabled

.in_progress
    rti                                     ;7 = 30

.overflow
        inc <HuTrack.dda.addr.hi,x
        lda <HuTrack.dda.addr.hi,x
        cmp #$60
      bcc .next
        lda #$40
        sta <HuTrack.dda.addr.hi,x
        inc <HuTrack.dda.bank,x
      bra .next

.control_flag
        ora <HuTrack.dda.cntr0,x
        and <HuTrack.dda.cntr1,x
        cmp #$80
      beq .stop
        lda <HuTrack.dda.loop.bank,x
        sta <HuTrack.dda.bank,x
        ;need to write a "zero" value to the DDA, not sufficient for it to be part of the waveform. 
        lda #$10 
        sei
        stx _htk.WSG.ChannelSelect          ;5
        sta _htk.WSG.DDAport                ;5
        cli
        tam #$02

        lda <HuTrack.dda.addr.loop.hi,x
        sta <HuTrack.dda.addr.hi,x
        sta <HuTrack.dda.ptr+1

        lda <HuTrack.dda.addr.loop.lo,x
        sta <HuTrack.dda.addr.lo,x
        sta <HuTrack.dda.ptr

      jmp .re_entry

.stop
        sta <HuTrack.dda.bank,x
        bra .next



