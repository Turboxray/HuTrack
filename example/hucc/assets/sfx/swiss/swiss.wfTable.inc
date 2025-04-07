
;###########################################################################

.waveform.table

  .dw $2       ; offset to bank table

  .dw .wf.block0


; Banks

  .db bank(.wf.block0)
