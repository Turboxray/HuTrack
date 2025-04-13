
;###########################################################################

.data.table

  .dw $2       ; offset to bank table

  .dw .data.chan2


; Banks

  .db bank(.data.chan2)
