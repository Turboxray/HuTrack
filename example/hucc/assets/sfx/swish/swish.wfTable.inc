
;###########################################################################

.waveform.table

  .dw $4       ; offset to bank table

  .dw .wf.block0
  .dw .wf.block1


; Banks

  .db bank(.wf.block0)
  .db bank(.wf.block1)
