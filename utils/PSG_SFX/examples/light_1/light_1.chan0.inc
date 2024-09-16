
.data.chan0


;..........................
; frame 0

  .db $0                                        ; 804 -> $0
  .db $a1, $ff                                  ; 801 -> $ff
  .db $a8, $ff                                  ; 808 -> $ff
  .db $a9, $0                                   ; 809 -> $0
  .db $a5, $ff                                  ; 805 -> $ff
  .db $a7, $0                                   ; 807 -> $0
  .db $a5, $df                                  ; 805 -> $df
  .db $a7, $0                                   ; 807 -> $0
  .db $9f                                       ; 804 -> $9f
  .db $a7, $0                                   ; 807 -> $0
  .db $5f                                       ; 804 -> $5f
  .db $1f                                       ; 804 -> $1f
  .db $b0, $0                                   ; Waveform update #$0
  .db $9f                                       ; 804 -> $9f
  .db $c2, $cf                                  ; 802 -> $2, 803 -> $cf
  .db $ff                                       ; Wait vblank

;..........................
; frame 1

  .db $9f                                       ; 804 -> $9f
  .db $a7, $0                                   ; 807 -> $0
  .db $c3, $c0                                  ; 802 -> $3, 803 -> $c0
  .db $ff                                       ; Wait vblank

;..........................
; frame 2

  .db $9f                                       ; 804 -> $9f
  .db $a7, $0                                   ; 807 -> $0
  .db $cf, $ff                                  ; 802 -> $f, 803 -> $ff
  .db $ff                                       ; Wait vblank

;..........................
; frame 3

  .db $a7, $81                                  ; 807 -> $81
  .db $a5, $ff                                  ; 805 -> $ff
  .db $a7, $82                                  ; 807 -> $82
  .db $99                                       ; 804 -> $99
  .db $98                                       ; 804 -> $98
  .db $5f                                       ; 804 -> $5f
  .db $1f                                       ; 804 -> $1f
  .db $b0, $1                                   ; Waveform update #$1
  .db $98                                       ; 804 -> $98
  .db $c3, $8a                                  ; 802 -> $3, 803 -> $8a
  .db $ff                                       ; Wait vblank

;..........................
; frame 4

  .db $98                                       ; 804 -> $98
  .db $ff                                       ; Wait vblank

;..........................
; frame 5

  .db $94                                       ; 804 -> $94
  .db $ff                                       ; Wait vblank

;..........................
; frame 6

  .db $93                                       ; 804 -> $93
  .db $ff                                       ; Wait vblank

;..........................
; frame 7

  .db $8c                                       ; 804 -> $8c
  .db $ff                                       ; Wait vblank

;..........................
; frame 8

  .db $88                                       ; 804 -> $88
  .db $ff                                       ; Wait vblank

;..........................
; frame 9

  .db $80                                       ; 804 -> $80
  .db $ff                                       ; Wait vblank

;..........................
; frame 10

  .db $80                                       ; 804 -> $80
  .db $ff                                       ; Wait vblank

;..........................
; frame 11

  .db $80                                       ; 804 -> $80
  .db $ff                                       ; Wait vblank

;..........................
; frame 12

  .db $80                                       ; 804 -> $80
  .db $ff                                       ; Wait vblank

;..........................
; frame 13

  .db $ff                                       ; Wait vblank

;..........................
; frame 14

  .db $ff                                       ; Wait vblank

;..........................
; frame 15

  .db $ff                                       ; Wait vblank

;..........................
; frame 16

  .db $ff                                       ; Wait vblank

;..........................
; frame 17

  .db $ff                                       ; Wait vblank

;..........................
; frame 18

  .db $ff                                       ; Wait vblank

;..........................
; frame 19

  .db $ff                                       ; Wait vblank

;..........................
; frame 20

  .db $ff                                       ; Wait vblank

;..........................
; frame 21

  .db $ff                                       ; Wait vblank

;..........................
; frame 22

  .db $ff                                       ; Wait vblank

;..........................
; frame 23

  .db $ff                                       ; Wait vblank

;..........................
; frame 24

  .db $ff                                       ; Wait vblank

;..........................
; frame 25

  .db $ff                                       ; Wait vblank

;..........................
; frame 26

  .db $ff                                       ; Wait vblank

;..........................
; frame 27

  .db $ff                                       ; Wait vblank

;..........................
; frame 28

  .db $fb                                       ; End of channel stream