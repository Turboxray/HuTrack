
.data.chan5


;..........................
; frame 0

  .db $5f                                       ; 804 -> $5f
  .db $1f                                       ; 804 -> $1f
  .db $b0, $0                                   ; Waveform update #$0
  .db $a5, $ff                                  ; 805 -> $ff
  .db $a5, $fa                                  ; 805 -> $fa
  .db $9f                                       ; 804 -> $9f
  .db $81                                       ; 804 -> $81
  .db $5f                                       ; 804 -> $5f
  .db $1f                                       ; 804 -> $1f
  .db $b0, $1                                   ; Waveform update #$1
  .db $81                                       ; 804 -> $81
  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $a8, $ff                                  ; 808 -> $ff
  .db $a9, $0                                   ; 809 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 1

  .db $86                                       ; 804 -> $86
  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 2

  .db $8b                                       ; 804 -> $8b
  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 3

  .db $93                                       ; 804 -> $93
  .db $c5, $f4                                  ; 802 -> $5, 803 -> $f4
  .db $a7, $8f                                  ; 807 -> $8f
  .db $ff                                       ; Wait vblank

;..........................
; frame 4

  .db $95                                       ; 804 -> $95
  .db $c5, $9e                                  ; 802 -> $5, 803 -> $9e
  .db $a7, $92                                  ; 807 -> $92
  .db $ff                                       ; Wait vblank

;..........................
; frame 5

  .db $a5, $df                                  ; 805 -> $df
  .db $98                                       ; 804 -> $98
  .db $c5, $9e                                  ; 802 -> $5, 803 -> $9e
  .db $a7, $92                                  ; 807 -> $92
  .db $ff                                       ; Wait vblank

;..........................
; frame 6

  .db $9a                                       ; 804 -> $9a
  .db $c5, $9e                                  ; 802 -> $5, 803 -> $9e
  .db $a7, $92                                  ; 807 -> $92
  .db $ff                                       ; Wait vblank

;..........................
; frame 7

  .db $9b                                       ; 804 -> $9b
  .db $c5, $9e                                  ; 802 -> $5, 803 -> $9e
  .db $a7, $92                                  ; 807 -> $92
  .db $ff                                       ; Wait vblank

;..........................
; frame 8

  .db $9d                                       ; 804 -> $9d
  .db $c5, $9e                                  ; 802 -> $5, 803 -> $9e
  .db $a7, $92                                  ; 807 -> $92
  .db $ff                                       ; Wait vblank

;..........................
; frame 9

  .db $9d                                       ; 804 -> $9d
  .db $c5, $9e                                  ; 802 -> $5, 803 -> $9e
  .db $a7, $92                                  ; 807 -> $92
  .db $ff                                       ; Wait vblank

;..........................
; frame 10

  .db $9d                                       ; 804 -> $9d
  .db $c5, $9e                                  ; 802 -> $5, 803 -> $9e
  .db $a7, $92                                  ; 807 -> $92
  .db $ff                                       ; Wait vblank

;..........................
; frame 11

  .db $9b                                       ; 804 -> $9b
  .db $c5, $f4                                  ; 802 -> $5, 803 -> $f4
  .db $a7, $8f                                  ; 807 -> $8f
  .db $ff                                       ; Wait vblank

;..........................
; frame 12

  .db $98                                       ; 804 -> $98
  .db $c5, $f4                                  ; 802 -> $5, 803 -> $f4
  .db $a7, $8f                                  ; 807 -> $8f
  .db $ff                                       ; Wait vblank

;..........................
; frame 13

  .db $94                                       ; 804 -> $94
  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 14

  .db $87                                       ; 804 -> $87
  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 15

  .db $84                                       ; 804 -> $84
  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 16

  .db $82                                       ; 804 -> $82
  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 17

  .db $80                                       ; 804 -> $80
  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 18

  .db $80                                       ; 804 -> $80
  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 19

  .db $80                                       ; 804 -> $80
  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 20

  .db $80                                       ; 804 -> $80
  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 21

  .db $80                                       ; 804 -> $80
  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 22

  .db $80                                       ; 804 -> $80
  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 23

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 24

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 25

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 26

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 27

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 28

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 29

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 30

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 31

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 32

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 33

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 34

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 35

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 36

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 37

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 38

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 39

  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $8d                                  ; 807 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 40

  .db $fd                                       ; Stop sample
  .db $c6, $4e                                  ; 802 -> $6, 803 -> $4e
  .db $a7, $0                                   ; 807 -> $0
  .db $0                                        ; 804 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 41

  .db $ff                                       ; Wait vblank

;..........................
; frame 42

  .db $ff                                       ; Wait vblank

;..........................
; frame 43

  .db $ff                                       ; Wait vblank

;..........................
; frame 44

  .db $ff                                       ; Wait vblank

;..........................
; frame 45

  .db $ff                                       ; Wait vblank

;..........................
; frame 46

  .db $ff                                       ; Wait vblank

;..........................
; frame 47

  .db $ff                                       ; Wait vblank

;..........................
; frame 48

  .db $ff                                       ; Wait vblank

;..........................
; frame 49

  .db $ff                                       ; Wait vblank

;..........................
; frame 50

  .db $ff                                       ; Wait vblank

;..........................
; frame 51

  .db $ff                                       ; Wait vblank

;..........................
; frame 52

  .db $ff                                       ; Wait vblank

;..........................
; frame 53

  .db $ff                                       ; Wait vblank

;..........................
; frame 54

  .db $ff                                       ; Wait vblank

;..........................
; frame 55

  .db $ff                                       ; Wait vblank

;..........................
; frame 56

  .db $ff                                       ; Wait vblank

;..........................
; frame 57

  .db $ff                                       ; Wait vblank

;..........................
; frame 58

  .db $ff                                       ; Wait vblank

;..........................
; frame 59

  .db $ff                                       ; Wait vblank

;..........................
; frame 60

  .db $ff                                       ; Wait vblank

;..........................
; frame 61

  .db $ff                                       ; Wait vblank

;..........................
; frame 62

  .db $ff                                       ; Wait vblank

;..........................
; frame 63

  .db $ff                                       ; Wait vblank

;..........................
; frame 64

  .db $ff                                       ; Wait vblank

;..........................
; frame 65

  .db $ff                                       ; Wait vblank

;..........................
; frame 66

  .db $ff                                       ; Wait vblank

;..........................
; frame 67

  .db $ff                                       ; Wait vblank

;..........................
; frame 68

  .db $ff                                       ; Wait vblank

;..........................
; frame 69

  .db $ff                                       ; Wait vblank

;..........................
; frame 70

  .db $ff                                       ; Wait vblank

;..........................
; frame 71

  .db $ff                                       ; Wait vblank

;..........................
; frame 72

  .db $ff                                       ; Wait vblank

;..........................
; frame 73

  .db $ff                                       ; Wait vblank

;..........................
; frame 74

  .db $ff                                       ; Wait vblank

;..........................
; frame 75

  .db $ff                                       ; Wait vblank

;..........................
; frame 76

  .db $ff                                       ; Wait vblank

;..........................
; frame 77

  .db $ff                                       ; Wait vblank

;..........................
; frame 78

  .db $ff                                       ; Wait vblank

;..........................
; frame 79

  .db $ff                                       ; Wait vblank

;..........................
; frame 80

  .db $ff                                       ; Wait vblank

;..........................
; frame 81

  .db $fb                                       ; End of channel stream