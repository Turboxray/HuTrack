
;###########################################################################

.waveform.table

  .dw $6       ; offset to bank table

  .dw .wf.block0
  .dw .wf.block1
  .dw .wf.block2


; Banks

  .db bank(.wf.block0)
  .db bank(.wf.block1)
  .db bank(.wf.block2)
