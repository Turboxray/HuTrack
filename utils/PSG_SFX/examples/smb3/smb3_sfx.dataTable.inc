
;###########################################################################

.data.table

  .dw $2       ; offset to bank table

  .dw .data.chan5


; Banks

  .db bank(.data.chan5)
