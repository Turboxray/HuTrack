
.data.chan2


;..........................
; frame 0

  .db $5f                                       ; 804 -> $5f
  .db $1f                                       ; 804 -> $1f
  .db $b0, $0                                   ; Waveform update #$0
  .db $a5, $ff                                  ; 805 -> $ff
  .db $9f                                       ; 804 -> $9f
  .db $5f                                       ; 804 -> $5f
  .db $1f                                       ; 804 -> $1f
  .db $b0, $1                                   ; Waveform update #$1
  .db $9f                                       ; 804 -> $9f
  .db $c0, $e0                                  ; 802 -> $0, 803 -> $e0
  .db $a8, $ff                                  ; 808 -> $ff
  .db $a9, $0                                   ; 809 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 1

  .db $ff                                       ; Wait vblank

;..........................
; frame 2

  .db $ff                                       ; Wait vblank

;..........................
; frame 3

  .db $ff                                       ; Wait vblank

;..........................
; frame 4

  .db $9c                                       ; 804 -> $9c
  .db $ff                                       ; Wait vblank

;..........................
; frame 5

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 6

  .db $96                                       ; 804 -> $96
  .db $ff                                       ; Wait vblank

;..........................
; frame 7

  .db $93                                       ; 804 -> $93
  .db $ff                                       ; Wait vblank

;..........................
; frame 8

  .db $9f                                       ; 804 -> $9f
  .db $9c                                       ; 804 -> $9c
  .db $c0, $fc                                  ; 802 -> $0, 803 -> $fc
  .db $ff                                       ; Wait vblank

;..........................
; frame 9

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 10

  .db $96                                       ; 804 -> $96
  .db $ff                                       ; Wait vblank

;..........................
; frame 11

  .db $93                                       ; 804 -> $93
  .db $ff                                       ; Wait vblank

;..........................
; frame 12

  .db $90                                       ; 804 -> $90
  .db $ff                                       ; Wait vblank

;..........................
; frame 13

  .db $8d                                       ; 804 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 14

  .db $ff                                       ; Wait vblank

;..........................
; frame 15

  .db $ff                                       ; Wait vblank

;..........................
; frame 16

  .db $9f                                       ; 804 -> $9f
  .db $9f                                       ; 804 -> $9f
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

  .db $9c                                       ; 804 -> $9c
  .db $ff                                       ; Wait vblank

;..........................
; frame 21

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 22

  .db $9f                                       ; 804 -> $9f
  .db $9f                                       ; 804 -> $9f
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

  .db $9c                                       ; 804 -> $9c
  .db $ff                                       ; Wait vblank

;..........................
; frame 29

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 30

  .db $ff                                       ; Wait vblank

;..........................
; frame 31

  .db $ff                                       ; Wait vblank

;..........................
; frame 32

  .db $ff                                       ; Wait vblank

;..........................
; frame 33

  .db $ff                                       ; Wait vblank

;..........................
; frame 34

  .db $9f                                       ; 804 -> $9f
  .db $9f                                       ; 804 -> $9f
  .db $ff                                       ; Wait vblank

;..........................
; frame 35

  .db $ff                                       ; Wait vblank

;..........................
; frame 36

  .db $9c                                       ; 804 -> $9c
  .db $ff                                       ; Wait vblank

;..........................
; frame 37

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 38

  .db $9f                                       ; 804 -> $9f
  .db $9f                                       ; 804 -> $9f
  .db $ff                                       ; Wait vblank

;..........................
; frame 39

  .db $ff                                       ; Wait vblank

;..........................
; frame 40

  .db $9f                                       ; 804 -> $9f
  .db $c0, $fc                                  ; 802 -> $0, 803 -> $fc
  .db $ff                                       ; Wait vblank

;..........................
; frame 41

  .db $ff                                       ; Wait vblank

;..........................
; frame 42

  .db $9c                                       ; 804 -> $9c
  .db $ff                                       ; Wait vblank

;..........................
; frame 43

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 44

  .db $9f                                       ; 804 -> $9f
  .db $9f                                       ; 804 -> $9f
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

  .db $9f                                       ; 804 -> $9f
  .db $c1, $27                                  ; 802 -> $1, 803 -> $27
  .db $ff                                       ; Wait vblank

;..........................
; frame 49

  .db $c1, $23                                  ; 802 -> $1, 803 -> $23
  .db $ff                                       ; Wait vblank

;..........................
; frame 50

  .db $c1, $23                                  ; 802 -> $1, 803 -> $23
  .db $ff                                       ; Wait vblank

;..........................
; frame 51

  .db $ff                                       ; Wait vblank

;..........................
; frame 52

  .db $9f                                       ; 804 -> $9f
  .db $c1, $1b                                  ; 802 -> $1, 803 -> $1b
  .db $ff                                       ; Wait vblank

;..........................
; frame 53

  .db $ff                                       ; Wait vblank

;..........................
; frame 54

  .db $9f                                       ; 804 -> $9f
  .db $c1, $2b                                  ; 802 -> $1, 803 -> $2b
  .db $ff                                       ; Wait vblank

;..........................
; frame 55

  .db $ff                                       ; Wait vblank

;..........................
; frame 56

  .db $9c                                       ; 804 -> $9c
  .db $ff                                       ; Wait vblank

;..........................
; frame 57

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 58

  .db $ff                                       ; Wait vblank

;..........................
; frame 59

  .db $ff                                       ; Wait vblank

;..........................
; frame 60

  .db $9f                                       ; 804 -> $9f
  .db $9f                                       ; 804 -> $9f
  .db $ff                                       ; Wait vblank

;..........................
; frame 61

  .db $ff                                       ; Wait vblank

;..........................
; frame 62

  .db $9c                                       ; 804 -> $9c
  .db $ff                                       ; Wait vblank

;..........................
; frame 63

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 64

  .db $ff                                       ; Wait vblank

;..........................
; frame 65

  .db $fb                                       ; End of channel stream