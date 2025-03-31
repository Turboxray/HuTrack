
;###########################################################################

.data.table

  .dw $c       ; offset to bank table

  .dw .data.chan0
  .dw .data.chan1
  .dw .data.chan2
  .dw .data.chan3
  .dw .data.chan4
  .dw .data.chan5


; Banks

  .db bank(.data.chan0)
  .db bank(.data.chan1)
  .db bank(.data.chan2)
  .db bank(.data.chan3)
  .db bank(.data.chan4)
  .db bank(.data.chan5)
