
;###########################################################################

.waveform.table

  .dw $e       ; offset to bank table

  .dw .wf.block0
  .dw .wf.block1
  .dw .wf.block2
  .dw .wf.block3
  .dw .wf.block4
  .dw .wf.block5
  .dw .wf.block6


; Banks

  .db bank(.wf.block0)
  .db bank(.wf.block1)
  .db bank(.wf.block2)
  .db bank(.wf.block3)
  .db bank(.wf.block4)
  .db bank(.wf.block5)
  .db bank(.wf.block6)
