
;###########################################################################

.data.table

  .dw $2       ; offset to bank table

  .dw .data.chan0


; Banks

  .db bank(.data.chan0)
