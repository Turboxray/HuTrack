

;###########################################################################

.samples.table

  ; offset to sample bank table.
  .dw $8

;.........................

  .dw .sample0
  .dw .sample1
  .dw .sample2
  .dw .sample3

;.........................

  .db bank(.sample0)
  .db bank(.sample1)
  .db bank(.sample2)
  .db bank(.sample3)


