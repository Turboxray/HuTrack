
;###########################################################################

.waveform.table

  .dw $8       ; offset to bank table

  .dw .wf.block0
  .dw .wf.block1
  .dw .wf.block2
  .dw .wf.block3


; Banks

  .db bank(.wf.block0)
  .db bank(.wf.block1)
  .db bank(.wf.block2)
  .db bank(.wf.block3)
