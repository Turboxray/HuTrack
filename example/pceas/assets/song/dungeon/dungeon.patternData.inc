

;###########################################################################
.pattern.table
  .dw .pattern.table.chan0
  .dw .pattern.table.chan1
  .dw .pattern.table.chan2
  .dw .pattern.table.chan3
  .dw .pattern.table.chan4
  .dw .pattern.table.chan5


  .db bank(.pattern.table.chan0)
  .db bank(.pattern.table.chan1)
  .db bank(.pattern.table.chan2)
  .db bank(.pattern.table.chan3)
  .db bank(.pattern.table.chan4)
  .db bank(.pattern.table.chan5)


;.....................................................
.pattern.table.chan0
  .dw .pattern.table.chan0.pattern0
  .dw .pattern.table.chan0.pattern1
  .dw .pattern.table.chan0.pattern2
  .dw .pattern.table.chan0.pattern3
  .dw .pattern.table.chan0.pattern4
  .dw .pattern.table.chan0.pattern5


;###########################################################################


;.....................................................
.pattern.table.chan1
  .dw .pattern.table.chan1.pattern0
  .dw .pattern.table.chan1.pattern1
  .dw .pattern.table.chan1.pattern2
  .dw .pattern.table.chan1.pattern3
  .dw .pattern.table.chan1.pattern4


;###########################################################################


;.....................................................
.pattern.table.chan2
  .dw .pattern.table.chan2.pattern0
  .dw .pattern.table.chan2.pattern1


;###########################################################################


;.....................................................
.pattern.table.chan3
  .dw .pattern.table.chan3.pattern0


;###########################################################################


;.....................................................
.pattern.table.chan4
  .dw .pattern.table.chan4.pattern0
  .dw .pattern.table.chan4.pattern1


;###########################################################################


;.....................................................
.pattern.table.chan5
  .dw .pattern.table.chan5.pattern0


;###########################################################################


;........................................................................
;........................................................................

;......................................
.pattern.table.chan0.pattern0

  .db $fe
  .db $fe
  .db $e4


;......................................
.pattern.table.chan0.pattern1

  .db $d, $18, $9, $1d
  .db $ef
  .db $9a
  .db $ef
  .db $9c
  .db $ef
  .db $98
  .db $ef


;......................................
.pattern.table.chan0.pattern2

  .db $e0
  .db $fe
  .db $fe
  .db $e3


;......................................
.pattern.table.chan0.pattern3

  .db $9a
  .db $ee
  .db $e0
  .db $9a
  .db $f7
  .db $98
  .db $e7
  .db $9a
  .db $e7
  .db $98
  .db $e7


;......................................
.pattern.table.chan0.pattern4

  .db $9a
  .db $e7
  .db $9c
  .db $e7
  .db $98
  .db $ee
  .db $e0
  .db $fe
  .db $e2


;......................................
.pattern.table.chan0.pattern5

  .db $e2
  .db $5, $1a, $9
  .db $ee
  .db $e0
  .db $9a
  .db $ef
  .db $98
  .db $e7
  .db $9a
  .db $e7
  .db $98
  .db $ed


;........................................................................
;........................................................................

;......................................
.pattern.table.chan1.pattern0

  .db $fe
  .db $fe
  .db $e4


;......................................
.pattern.table.chan1.pattern1

  .db $5, $29, $9
  .db $fe
  .db $e1
  .db $b0
  .db $f7
  .db $af
  .db $e7


;......................................
.pattern.table.chan1.pattern2

  .db $e8
  .db $a9
  .db $f7
  .db $ab
  .db $ef
  .db $ad
  .db $ef


;......................................
.pattern.table.chan1.pattern3

  .db $a9
  .db $ef
  .db $30, $a, $1
  .db $f0
  .db $e0
  .db $fe


;......................................
.pattern.table.chan1.pattern4

  .db $9a
  .db $ee
  .db $e0
  .db $9a
  .db $ef
  .db $98
  .db $e7
  .db $5, $1a, $9
  .db $e7
  .db $5, $18, $9
  .db $e7
  .db $5, $1a, $9
  .db $e7


;........................................................................
;........................................................................

;......................................
.pattern.table.chan2.pattern0

  .db $d, $5, $7, $1b
  .db $e7
  .db $84
  .db $e3
  .db $91
  .db $eb
  .db $85
  .db $e7
  .db $84
  .db $e3
  .db $91
  .db $fb


;......................................
.pattern.table.chan2.pattern1

  .db $fe
  .db $fe
  .db $e4


;........................................................................
;........................................................................

;......................................
.pattern.table.chan3.pattern0

  .db $d, $2, $7, $1b
  .db $e7
  .db $81
  .db $e3
  .db $35, $2, $7, $2, $35
  .db $eb
  .db $82
  .db $e7
  .db $81
  .db $e3
  .db $5, $2, $7
  .db $fb


;........................................................................
;........................................................................

;......................................
.pattern.table.chan4.pattern0

  .db $d, $27, $5, $19
  .db $ef
  .db $a7
  .db $ef
  .db $a7
  .db $ef
  .db $a7
  .db $ef


;......................................
.pattern.table.chan4.pattern1

  .db $fe
  .db $fe
  .db $e4


;........................................................................
;........................................................................

;......................................
.pattern.table.chan5.pattern0

  .db $fe
  .db $fe
  .db $e4




