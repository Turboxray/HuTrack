

;###########################################################################
  .page 2
.instrument.0
; name Wave 0 envelope 00
; mode 0

.instrument.0.table
  .dw .instrument.0.volEnv
  .db bank(.instrument.0.volEnv)
  .dw .instrument.0.arpEnv
  .db bank(.instrument.0.arpEnv)
  .dw .instrument.0.waveFormEnv
  .db bank(.instrument.0.waveFormEnv)

;........................
  .page 2
.instrument.0.volEnv

.instrument.0.volEnv.size
  .db 9
.instrument.0.volEnv.loop
  .db 255
.instrument.0.volEnv.data
  .db 26, 24, 22, 22
  .db 21, 21, 21, 21
  .db 20


;........................
  .page 2
.instrument.0.arpEnv

.instrument.0.arpEnv.mode
  .db 0
.instrument.0.arpEnv.size
  .db 0
.instrument.0.arpEnv.loop
  .db 255
.instrument.0.arpEnv.data



;........................
  .page 2
.instrument.0.waveFormEnv

.instrument.0.waveFormEnv.size
  .db 1
.instrument.0.waveFormEnv.loop
  .db 255
.instrument.0.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.1
; name Wave 0 envelope 01
; mode 0

.instrument.1.table
  .dw .instrument.1.volEnv
  .db bank(.instrument.1.volEnv)
  .dw .instrument.1.arpEnv
  .db bank(.instrument.1.arpEnv)
  .dw .instrument.1.waveFormEnv
  .db bank(.instrument.1.waveFormEnv)

;........................
  .page 2
.instrument.1.volEnv

.instrument.1.volEnv.size
  .db 5
.instrument.1.volEnv.loop
  .db 255
.instrument.1.volEnv.data
  .db 26, 24, 22, 22
  .db 21


;........................
  .page 2
.instrument.1.arpEnv

.instrument.1.arpEnv.mode
  .db 0
.instrument.1.arpEnv.size
  .db 0
.instrument.1.arpEnv.loop
  .db 255
.instrument.1.arpEnv.data



;........................
  .page 2
.instrument.1.waveFormEnv

.instrument.1.waveFormEnv.size
  .db 1
.instrument.1.waveFormEnv.loop
  .db 255
.instrument.1.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.2
; name Wave 0 envelope 02
; mode 0

.instrument.2.table
  .dw .instrument.2.volEnv
  .db bank(.instrument.2.volEnv)
  .dw .instrument.2.arpEnv
  .db bank(.instrument.2.arpEnv)
  .dw .instrument.2.waveFormEnv
  .db bank(.instrument.2.waveFormEnv)

;........................
  .page 2
.instrument.2.volEnv

.instrument.2.volEnv.size
  .db 10
.instrument.2.volEnv.loop
  .db 255
.instrument.2.volEnv.data
  .db 20, 20, 19, 19
  .db 19, 19, 18, 18
  .db 18, 17


;........................
  .page 2
.instrument.2.arpEnv

.instrument.2.arpEnv.mode
  .db 0
.instrument.2.arpEnv.size
  .db 0
.instrument.2.arpEnv.loop
  .db 255
.instrument.2.arpEnv.data



;........................
  .page 2
.instrument.2.waveFormEnv

.instrument.2.waveFormEnv.size
  .db 1
.instrument.2.waveFormEnv.loop
  .db 255
.instrument.2.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.3
; name Wave 1 envelope 03
; mode 0

.instrument.3.table
  .dw .instrument.3.volEnv
  .db bank(.instrument.3.volEnv)
  .dw .instrument.3.arpEnv
  .db bank(.instrument.3.arpEnv)
  .dw .instrument.3.waveFormEnv
  .db bank(.instrument.3.waveFormEnv)

;........................
  .page 2
.instrument.3.volEnv

.instrument.3.volEnv.size
  .db 46
.instrument.3.volEnv.loop
  .db 255
.instrument.3.volEnv.data
  .db 25, 23, 21, 21
  .db 20, 20, 20, 20
  .db 19, 19, 19, 19
  .db 18, 18, 18, 18
  .db 17, 17, 17, 17
  .db 16, 16, 16, 16
  .db 15, 15, 15, 15
  .db 14, 14, 14, 14
  .db 13, 12, 11, 10
  .db 9, 8, 7, 6
  .db 5, 4, 3, 2
  .db 1, 0


;........................
  .page 2
.instrument.3.arpEnv

.instrument.3.arpEnv.mode
  .db 0
.instrument.3.arpEnv.size
  .db 0
.instrument.3.arpEnv.loop
  .db 255
.instrument.3.arpEnv.data



;........................
  .page 2
.instrument.3.waveFormEnv

.instrument.3.waveFormEnv.size
  .db 1
.instrument.3.waveFormEnv.loop
  .db 255
.instrument.3.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.4
; name Wave 1 envelope 04
; mode 0

.instrument.4.table
  .dw .instrument.4.volEnv
  .db bank(.instrument.4.volEnv)
  .dw .instrument.4.arpEnv
  .db bank(.instrument.4.arpEnv)
  .dw .instrument.4.waveFormEnv
  .db bank(.instrument.4.waveFormEnv)

;........................
  .page 2
.instrument.4.volEnv

.instrument.4.volEnv.size
  .db 10
.instrument.4.volEnv.loop
  .db 255
.instrument.4.volEnv.data
  .db 25, 23, 21, 21
  .db 20, 20, 20, 19
  .db 18, 17


;........................
  .page 2
.instrument.4.arpEnv

.instrument.4.arpEnv.mode
  .db 0
.instrument.4.arpEnv.size
  .db 0
.instrument.4.arpEnv.loop
  .db 255
.instrument.4.arpEnv.data



;........................
  .page 2
.instrument.4.waveFormEnv

.instrument.4.waveFormEnv.size
  .db 1
.instrument.4.waveFormEnv.loop
  .db 255
.instrument.4.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.5
; name Wave 1 envelope 05
; mode 0

.instrument.5.table
  .dw .instrument.5.volEnv
  .db bank(.instrument.5.volEnv)
  .dw .instrument.5.arpEnv
  .db bank(.instrument.5.arpEnv)
  .dw .instrument.5.waveFormEnv
  .db bank(.instrument.5.waveFormEnv)

;........................
  .page 2
.instrument.5.volEnv

.instrument.5.volEnv.size
  .db 9
.instrument.5.volEnv.loop
  .db 255
.instrument.5.volEnv.data
  .db 25, 23, 21, 21
  .db 20, 20, 20, 20
  .db 19


;........................
  .page 2
.instrument.5.arpEnv

.instrument.5.arpEnv.mode
  .db 0
.instrument.5.arpEnv.size
  .db 0
.instrument.5.arpEnv.loop
  .db 255
.instrument.5.arpEnv.data



;........................
  .page 2
.instrument.5.waveFormEnv

.instrument.5.waveFormEnv.size
  .db 1
.instrument.5.waveFormEnv.loop
  .db 255
.instrument.5.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.6
; name Wave 1 envelope 06
; mode 0

.instrument.6.table
  .dw .instrument.6.volEnv
  .db bank(.instrument.6.volEnv)
  .dw .instrument.6.arpEnv
  .db bank(.instrument.6.arpEnv)
  .dw .instrument.6.waveFormEnv
  .db bank(.instrument.6.waveFormEnv)

;........................
  .page 2
.instrument.6.volEnv

.instrument.6.volEnv.size
  .db 43
.instrument.6.volEnv.loop
  .db 255
.instrument.6.volEnv.data
  .db 19, 19, 18, 18
  .db 18, 18, 17, 17
  .db 17, 17, 16, 16
  .db 16, 16, 15, 15
  .db 15, 15, 14, 14
  .db 14, 14, 13, 13
  .db 13, 13, 12, 12
  .db 12, 12, 11, 11
  .db 10, 9, 8, 7
  .db 6, 5, 4, 3
  .db 2, 1, 0

;........................
  .page 2
.instrument.6.arpEnv

.instrument.6.arpEnv.mode
  .db 0
.instrument.6.arpEnv.size
  .db 0
.instrument.6.arpEnv.loop
  .db 255
.instrument.6.arpEnv.data



;........................
  .page 2
.instrument.6.waveFormEnv

.instrument.6.waveFormEnv.size
  .db 1
.instrument.6.waveFormEnv.loop
  .db 255
.instrument.6.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.7
; name Wave 1 envelope 07
; mode 0

.instrument.7.table
  .dw .instrument.7.volEnv
  .db bank(.instrument.7.volEnv)
  .dw .instrument.7.arpEnv
  .db bank(.instrument.7.arpEnv)
  .dw .instrument.7.waveFormEnv
  .db bank(.instrument.7.waveFormEnv)

;........................
  .page 2
.instrument.7.volEnv

.instrument.7.volEnv.size
  .db 10
.instrument.7.volEnv.loop
  .db 255
.instrument.7.volEnv.data
  .db 19, 19, 18, 18
  .db 18, 18, 17, 16
  .db 15, 14


;........................
  .page 2
.instrument.7.arpEnv

.instrument.7.arpEnv.mode
  .db 0
.instrument.7.arpEnv.size
  .db 0
.instrument.7.arpEnv.loop
  .db 255
.instrument.7.arpEnv.data



;........................
  .page 2
.instrument.7.waveFormEnv

.instrument.7.waveFormEnv.size
  .db 1
.instrument.7.waveFormEnv.loop
  .db 255
.instrument.7.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.8
; name Wave 1 envelope 08
; mode 0

.instrument.8.table
  .dw .instrument.8.volEnv
  .db bank(.instrument.8.volEnv)
  .dw .instrument.8.arpEnv
  .db bank(.instrument.8.arpEnv)
  .dw .instrument.8.waveFormEnv
  .db bank(.instrument.8.waveFormEnv)

;........................
  .page 2
.instrument.8.volEnv

.instrument.8.volEnv.size
  .db 20
.instrument.8.volEnv.loop
  .db 255
.instrument.8.volEnv.data
  .db 25, 23, 21, 21
  .db 20, 20, 20, 20
  .db 19, 19, 19, 19
  .db 18, 17, 16, 15
  .db 14, 13, 12, 11



;........................
  .page 2
.instrument.8.arpEnv

.instrument.8.arpEnv.mode
  .db 0
.instrument.8.arpEnv.size
  .db 0
.instrument.8.arpEnv.loop
  .db 255
.instrument.8.arpEnv.data



;........................
  .page 2
.instrument.8.waveFormEnv

.instrument.8.waveFormEnv.size
  .db 1
.instrument.8.waveFormEnv.loop
  .db 255
.instrument.8.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.9
; name Wave 1 envelope 09
; mode 0

.instrument.9.table
  .dw .instrument.9.volEnv
  .db bank(.instrument.9.volEnv)
  .dw .instrument.9.arpEnv
  .db bank(.instrument.9.arpEnv)
  .dw .instrument.9.waveFormEnv
  .db bank(.instrument.9.waveFormEnv)

;........................
  .page 2
.instrument.9.volEnv

.instrument.9.volEnv.size
  .db 30
.instrument.9.volEnv.loop
  .db 255
.instrument.9.volEnv.data
  .db 19, 19, 18, 18
  .db 18, 18, 17, 17
  .db 17, 17, 16, 16
  .db 16, 16, 15, 15
  .db 15, 15, 14, 13
  .db 12, 11, 10, 9
  .db 8, 7, 6, 5
  .db 4, 3


;........................
  .page 2
.instrument.9.arpEnv

.instrument.9.arpEnv.mode
  .db 0
.instrument.9.arpEnv.size
  .db 0
.instrument.9.arpEnv.loop
  .db 255
.instrument.9.arpEnv.data



;........................
  .page 2
.instrument.9.waveFormEnv

.instrument.9.waveFormEnv.size
  .db 1
.instrument.9.waveFormEnv.loop
  .db 255
.instrument.9.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.10
; name Wave 1 envelope 10
; mode 0

.instrument.10.table
  .dw .instrument.10.volEnv
  .db bank(.instrument.10.volEnv)
  .dw .instrument.10.arpEnv
  .db bank(.instrument.10.arpEnv)
  .dw .instrument.10.waveFormEnv
  .db bank(.instrument.10.waveFormEnv)

;........................
  .page 2
.instrument.10.volEnv

.instrument.10.volEnv.size
  .db 42
.instrument.10.volEnv.loop
  .db 255
.instrument.10.volEnv.data
  .db 25, 23, 21, 21
  .db 20, 20, 20, 20
  .db 19, 19, 19, 19
  .db 18, 18, 18, 18
  .db 17, 17, 17, 17
  .db 16, 16, 16, 16
  .db 15, 15, 15, 14
  .db 13, 12, 11, 10
  .db 9, 8, 7, 6
  .db 5, 4, 3, 2
  .db 1, 0


;........................
  .page 2
.instrument.10.arpEnv

.instrument.10.arpEnv.mode
  .db 0
.instrument.10.arpEnv.size
  .db 0
.instrument.10.arpEnv.loop
  .db 255
.instrument.10.arpEnv.data



;........................
  .page 2
.instrument.10.waveFormEnv

.instrument.10.waveFormEnv.size
  .db 1
.instrument.10.waveFormEnv.loop
  .db 255
.instrument.10.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.11
; name Wave 0 envelope 11
; mode 0

.instrument.11.table
  .dw .instrument.11.volEnv
  .db bank(.instrument.11.volEnv)
  .dw .instrument.11.arpEnv
  .db bank(.instrument.11.arpEnv)
  .dw .instrument.11.waveFormEnv
  .db bank(.instrument.11.waveFormEnv)

;........................
  .page 2
.instrument.11.volEnv

.instrument.11.volEnv.size
  .db 10
.instrument.11.volEnv.loop
  .db 255
.instrument.11.volEnv.data
  .db 21, 19, 17, 17
  .db 16, 15, 14, 13
  .db 12, 11


;........................
  .page 2
.instrument.11.arpEnv

.instrument.11.arpEnv.mode
  .db 0
.instrument.11.arpEnv.size
  .db 0
.instrument.11.arpEnv.loop
  .db 255
.instrument.11.arpEnv.data



;........................
  .page 2
.instrument.11.waveFormEnv

.instrument.11.waveFormEnv.size
  .db 1
.instrument.11.waveFormEnv.loop
  .db 255
.instrument.11.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.12
; name Wave 0 envelope 12
; mode 0

.instrument.12.table
  .dw .instrument.12.volEnv
  .db bank(.instrument.12.volEnv)
  .dw .instrument.12.arpEnv
  .db bank(.instrument.12.arpEnv)
  .dw .instrument.12.waveFormEnv
  .db bank(.instrument.12.waveFormEnv)

;........................
  .page 2
.instrument.12.volEnv

.instrument.12.volEnv.size
  .db 44
.instrument.12.volEnv.loop
  .db 255
.instrument.12.volEnv.data
  .db 23, 21, 19, 19
  .db 18, 18, 18, 18
  .db 17, 17, 17, 17
  .db 16, 16, 16, 16
  .db 15, 15, 15, 15
  .db 14, 14, 14, 14
  .db 13, 13, 13, 13
  .db 12, 12, 12, 12
  .db 11, 10, 9, 8
  .db 7, 6, 5, 4
  .db 3, 2, 1, 0



;........................
  .page 2
.instrument.12.arpEnv

.instrument.12.arpEnv.mode
  .db 0
.instrument.12.arpEnv.size
  .db 0
.instrument.12.arpEnv.loop
  .db 255
.instrument.12.arpEnv.data



;........................
  .page 2
.instrument.12.waveFormEnv

.instrument.12.waveFormEnv.size
  .db 1
.instrument.12.waveFormEnv.loop
  .db 255
.instrument.12.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.13
; name Wave 0 envelope 13
; mode 0

.instrument.13.table
  .dw .instrument.13.volEnv
  .db bank(.instrument.13.volEnv)
  .dw .instrument.13.arpEnv
  .db bank(.instrument.13.arpEnv)
  .dw .instrument.13.waveFormEnv
  .db bank(.instrument.13.waveFormEnv)

;........................
  .page 2
.instrument.13.volEnv

.instrument.13.volEnv.size
  .db 10
.instrument.13.volEnv.loop
  .db 255
.instrument.13.volEnv.data
  .db 23, 21, 19, 19
  .db 18, 18, 18, 17
  .db 16, 15


;........................
  .page 2
.instrument.13.arpEnv

.instrument.13.arpEnv.mode
  .db 0
.instrument.13.arpEnv.size
  .db 0
.instrument.13.arpEnv.loop
  .db 255
.instrument.13.arpEnv.data



;........................
  .page 2
.instrument.13.waveFormEnv

.instrument.13.waveFormEnv.size
  .db 1
.instrument.13.waveFormEnv.loop
  .db 255
.instrument.13.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.14
; name Wave 0 envelope 14
; mode 0

.instrument.14.table
  .dw .instrument.14.volEnv
  .db bank(.instrument.14.volEnv)
  .dw .instrument.14.arpEnv
  .db bank(.instrument.14.arpEnv)
  .dw .instrument.14.waveFormEnv
  .db bank(.instrument.14.waveFormEnv)

;........................
  .page 2
.instrument.14.volEnv

.instrument.14.volEnv.size
  .db 9
.instrument.14.volEnv.loop
  .db 255
.instrument.14.volEnv.data
  .db 23, 21, 19, 19
  .db 18, 18, 18, 18
  .db 17


;........................
  .page 2
.instrument.14.arpEnv

.instrument.14.arpEnv.mode
  .db 0
.instrument.14.arpEnv.size
  .db 0
.instrument.14.arpEnv.loop
  .db 255
.instrument.14.arpEnv.data



;........................
  .page 2
.instrument.14.waveFormEnv

.instrument.14.waveFormEnv.size
  .db 1
.instrument.14.waveFormEnv.loop
  .db 255
.instrument.14.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.15
; name Wave 0 envelope 15
; mode 0

.instrument.15.table
  .dw .instrument.15.volEnv
  .db bank(.instrument.15.volEnv)
  .dw .instrument.15.arpEnv
  .db bank(.instrument.15.arpEnv)
  .dw .instrument.15.waveFormEnv
  .db bank(.instrument.15.waveFormEnv)

;........................
  .page 2
.instrument.15.volEnv

.instrument.15.volEnv.size
  .db 41
.instrument.15.volEnv.loop
  .db 255
.instrument.15.volEnv.data
  .db 17, 17, 16, 16
  .db 16, 16, 15, 15
  .db 15, 15, 14, 14
  .db 14, 14, 13, 13
  .db 13, 13, 12, 12
  .db 12, 12, 11, 11
  .db 11, 11, 10, 10
  .db 10, 10, 9, 9
  .db 8, 7, 6, 5
  .db 4, 3, 2, 1
  .db 0


;........................
  .page 2
.instrument.15.arpEnv

.instrument.15.arpEnv.mode
  .db 0
.instrument.15.arpEnv.size
  .db 0
.instrument.15.arpEnv.loop
  .db 255
.instrument.15.arpEnv.data



;........................
  .page 2
.instrument.15.waveFormEnv

.instrument.15.waveFormEnv.size
  .db 1
.instrument.15.waveFormEnv.loop
  .db 255
.instrument.15.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.16
; name Wave 0 envelope 16
; mode 0

.instrument.16.table
  .dw .instrument.16.volEnv
  .db bank(.instrument.16.volEnv)
  .dw .instrument.16.arpEnv
  .db bank(.instrument.16.arpEnv)
  .dw .instrument.16.waveFormEnv
  .db bank(.instrument.16.waveFormEnv)

;........................
  .page 2
.instrument.16.volEnv

.instrument.16.volEnv.size
  .db 10
.instrument.16.volEnv.loop
  .db 255
.instrument.16.volEnv.data
  .db 17, 17, 16, 16
  .db 16, 16, 15, 14
  .db 13, 12


;........................
  .page 2
.instrument.16.arpEnv

.instrument.16.arpEnv.mode
  .db 0
.instrument.16.arpEnv.size
  .db 0
.instrument.16.arpEnv.loop
  .db 255
.instrument.16.arpEnv.data



;........................
  .page 2
.instrument.16.waveFormEnv

.instrument.16.waveFormEnv.size
  .db 1
.instrument.16.waveFormEnv.loop
  .db 255
.instrument.16.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.17
; name Wave 0 envelope 17
; mode 0

.instrument.17.table
  .dw .instrument.17.volEnv
  .db bank(.instrument.17.volEnv)
  .dw .instrument.17.arpEnv
  .db bank(.instrument.17.arpEnv)
  .dw .instrument.17.waveFormEnv
  .db bank(.instrument.17.waveFormEnv)

;........................
  .page 2
.instrument.17.volEnv

.instrument.17.volEnv.size
  .db 20
.instrument.17.volEnv.loop
  .db 255
.instrument.17.volEnv.data
  .db 23, 21, 19, 19
  .db 18, 18, 18, 18
  .db 17, 17, 17, 17
  .db 16, 15, 14, 13
  .db 12, 11, 10, 9



;........................
  .page 2
.instrument.17.arpEnv

.instrument.17.arpEnv.mode
  .db 0
.instrument.17.arpEnv.size
  .db 0
.instrument.17.arpEnv.loop
  .db 255
.instrument.17.arpEnv.data



;........................
  .page 2
.instrument.17.waveFormEnv

.instrument.17.waveFormEnv.size
  .db 1
.instrument.17.waveFormEnv.loop
  .db 255
.instrument.17.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.18
; name Wave 0 envelope 18
; mode 0

.instrument.18.table
  .dw .instrument.18.volEnv
  .db bank(.instrument.18.volEnv)
  .dw .instrument.18.arpEnv
  .db bank(.instrument.18.arpEnv)
  .dw .instrument.18.waveFormEnv
  .db bank(.instrument.18.waveFormEnv)

;........................
  .page 2
.instrument.18.volEnv

.instrument.18.volEnv.size
  .db 30
.instrument.18.volEnv.loop
  .db 255
.instrument.18.volEnv.data
  .db 17, 17, 16, 16
  .db 16, 16, 15, 15
  .db 15, 15, 14, 14
  .db 14, 14, 13, 13
  .db 13, 13, 12, 11
  .db 10, 9, 8, 7
  .db 6, 5, 4, 3
  .db 2, 1


;........................
  .page 2
.instrument.18.arpEnv

.instrument.18.arpEnv.mode
  .db 0
.instrument.18.arpEnv.size
  .db 0
.instrument.18.arpEnv.loop
  .db 255
.instrument.18.arpEnv.data



;........................
  .page 2
.instrument.18.waveFormEnv

.instrument.18.waveFormEnv.size
  .db 1
.instrument.18.waveFormEnv.loop
  .db 255
.instrument.18.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.19
; name Wave 0 envelope 19
; mode 0

.instrument.19.table
  .dw .instrument.19.volEnv
  .db bank(.instrument.19.volEnv)
  .dw .instrument.19.arpEnv
  .db bank(.instrument.19.arpEnv)
  .dw .instrument.19.waveFormEnv
  .db bank(.instrument.19.waveFormEnv)

;........................
  .page 2
.instrument.19.volEnv

.instrument.19.volEnv.size
  .db 40
.instrument.19.volEnv.loop
  .db 255
.instrument.19.volEnv.data
  .db 23, 21, 19, 19
  .db 18, 18, 18, 18
  .db 17, 17, 17, 17
  .db 16, 16, 16, 16
  .db 15, 15, 15, 15
  .db 14, 14, 14, 14
  .db 13, 13, 13, 12
  .db 11, 10, 9, 8
  .db 7, 6, 5, 4
  .db 3, 2, 1, 0



;........................
  .page 2
.instrument.19.arpEnv

.instrument.19.arpEnv.mode
  .db 0
.instrument.19.arpEnv.size
  .db 0
.instrument.19.arpEnv.loop
  .db 255
.instrument.19.arpEnv.data



;........................
  .page 2
.instrument.19.waveFormEnv

.instrument.19.waveFormEnv.size
  .db 1
.instrument.19.waveFormEnv.loop
  .db 255
.instrument.19.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.20
; name Wave 1 envelope 20
; mode 0

.instrument.20.table
  .dw .instrument.20.volEnv
  .db bank(.instrument.20.volEnv)
  .dw .instrument.20.arpEnv
  .db bank(.instrument.20.arpEnv)
  .dw .instrument.20.waveFormEnv
  .db bank(.instrument.20.waveFormEnv)

;........................
  .page 2
.instrument.20.volEnv

.instrument.20.volEnv.size
  .db 44
.instrument.20.volEnv.loop
  .db 255
.instrument.20.volEnv.data
  .db 23, 21, 19, 19
  .db 18, 18, 18, 18
  .db 17, 17, 17, 17
  .db 16, 16, 16, 16
  .db 15, 15, 15, 15
  .db 14, 14, 14, 14
  .db 13, 13, 13, 13
  .db 12, 12, 12, 12
  .db 11, 10, 9, 8
  .db 7, 6, 5, 4
  .db 3, 2, 1, 0



;........................
  .page 2
.instrument.20.arpEnv

.instrument.20.arpEnv.mode
  .db 0
.instrument.20.arpEnv.size
  .db 0
.instrument.20.arpEnv.loop
  .db 255
.instrument.20.arpEnv.data



;........................
  .page 2
.instrument.20.waveFormEnv

.instrument.20.waveFormEnv.size
  .db 1
.instrument.20.waveFormEnv.loop
  .db 255
.instrument.20.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.21
; name Wave 1 envelope 21
; mode 0

.instrument.21.table
  .dw .instrument.21.volEnv
  .db bank(.instrument.21.volEnv)
  .dw .instrument.21.arpEnv
  .db bank(.instrument.21.arpEnv)
  .dw .instrument.21.waveFormEnv
  .db bank(.instrument.21.waveFormEnv)

;........................
  .page 2
.instrument.21.volEnv

.instrument.21.volEnv.size
  .db 10
.instrument.21.volEnv.loop
  .db 255
.instrument.21.volEnv.data
  .db 23, 21, 19, 19
  .db 18, 18, 18, 17
  .db 16, 15


;........................
  .page 2
.instrument.21.arpEnv

.instrument.21.arpEnv.mode
  .db 0
.instrument.21.arpEnv.size
  .db 0
.instrument.21.arpEnv.loop
  .db 255
.instrument.21.arpEnv.data



;........................
  .page 2
.instrument.21.waveFormEnv

.instrument.21.waveFormEnv.size
  .db 1
.instrument.21.waveFormEnv.loop
  .db 255
.instrument.21.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.22
; name Wave 1 envelope 22
; mode 0

.instrument.22.table
  .dw .instrument.22.volEnv
  .db bank(.instrument.22.volEnv)
  .dw .instrument.22.arpEnv
  .db bank(.instrument.22.arpEnv)
  .dw .instrument.22.waveFormEnv
  .db bank(.instrument.22.waveFormEnv)

;........................
  .page 2
.instrument.22.volEnv

.instrument.22.volEnv.size
  .db 9
.instrument.22.volEnv.loop
  .db 255
.instrument.22.volEnv.data
  .db 23, 21, 19, 19
  .db 18, 18, 18, 18
  .db 17


;........................
  .page 2
.instrument.22.arpEnv

.instrument.22.arpEnv.mode
  .db 0
.instrument.22.arpEnv.size
  .db 0
.instrument.22.arpEnv.loop
  .db 255
.instrument.22.arpEnv.data



;........................
  .page 2
.instrument.22.waveFormEnv

.instrument.22.waveFormEnv.size
  .db 1
.instrument.22.waveFormEnv.loop
  .db 255
.instrument.22.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.23
; name Wave 1 envelope 23
; mode 0

.instrument.23.table
  .dw .instrument.23.volEnv
  .db bank(.instrument.23.volEnv)
  .dw .instrument.23.arpEnv
  .db bank(.instrument.23.arpEnv)
  .dw .instrument.23.waveFormEnv
  .db bank(.instrument.23.waveFormEnv)

;........................
  .page 2
.instrument.23.volEnv

.instrument.23.volEnv.size
  .db 41
.instrument.23.volEnv.loop
  .db 255
.instrument.23.volEnv.data
  .db 17, 17, 16, 16
  .db 16, 16, 15, 15
  .db 15, 15, 14, 14
  .db 14, 14, 13, 13
  .db 13, 13, 12, 12
  .db 12, 12, 11, 11
  .db 11, 11, 10, 10
  .db 10, 10, 9, 9
  .db 8, 7, 6, 5
  .db 4, 3, 2, 1
  .db 0


;........................
  .page 2
.instrument.23.arpEnv

.instrument.23.arpEnv.mode
  .db 0
.instrument.23.arpEnv.size
  .db 0
.instrument.23.arpEnv.loop
  .db 255
.instrument.23.arpEnv.data



;........................
  .page 2
.instrument.23.waveFormEnv

.instrument.23.waveFormEnv.size
  .db 1
.instrument.23.waveFormEnv.loop
  .db 255
.instrument.23.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.24
; name Wave 1 envelope 24
; mode 0

.instrument.24.table
  .dw .instrument.24.volEnv
  .db bank(.instrument.24.volEnv)
  .dw .instrument.24.arpEnv
  .db bank(.instrument.24.arpEnv)
  .dw .instrument.24.waveFormEnv
  .db bank(.instrument.24.waveFormEnv)

;........................
  .page 2
.instrument.24.volEnv

.instrument.24.volEnv.size
  .db 10
.instrument.24.volEnv.loop
  .db 255
.instrument.24.volEnv.data
  .db 17, 17, 16, 16
  .db 16, 16, 15, 14
  .db 13, 12


;........................
  .page 2
.instrument.24.arpEnv

.instrument.24.arpEnv.mode
  .db 0
.instrument.24.arpEnv.size
  .db 0
.instrument.24.arpEnv.loop
  .db 255
.instrument.24.arpEnv.data



;........................
  .page 2
.instrument.24.waveFormEnv

.instrument.24.waveFormEnv.size
  .db 1
.instrument.24.waveFormEnv.loop
  .db 255
.instrument.24.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.25
; name Wave 1 envelope 25
; mode 0

.instrument.25.table
  .dw .instrument.25.volEnv
  .db bank(.instrument.25.volEnv)
  .dw .instrument.25.arpEnv
  .db bank(.instrument.25.arpEnv)
  .dw .instrument.25.waveFormEnv
  .db bank(.instrument.25.waveFormEnv)

;........................
  .page 2
.instrument.25.volEnv

.instrument.25.volEnv.size
  .db 20
.instrument.25.volEnv.loop
  .db 255
.instrument.25.volEnv.data
  .db 23, 21, 19, 19
  .db 18, 18, 18, 18
  .db 17, 17, 17, 17
  .db 16, 15, 14, 13
  .db 12, 11, 10, 9



;........................
  .page 2
.instrument.25.arpEnv

.instrument.25.arpEnv.mode
  .db 0
.instrument.25.arpEnv.size
  .db 0
.instrument.25.arpEnv.loop
  .db 255
.instrument.25.arpEnv.data



;........................
  .page 2
.instrument.25.waveFormEnv

.instrument.25.waveFormEnv.size
  .db 1
.instrument.25.waveFormEnv.loop
  .db 255
.instrument.25.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.26
; name Wave 1 envelope 26
; mode 0

.instrument.26.table
  .dw .instrument.26.volEnv
  .db bank(.instrument.26.volEnv)
  .dw .instrument.26.arpEnv
  .db bank(.instrument.26.arpEnv)
  .dw .instrument.26.waveFormEnv
  .db bank(.instrument.26.waveFormEnv)

;........................
  .page 2
.instrument.26.volEnv

.instrument.26.volEnv.size
  .db 30
.instrument.26.volEnv.loop
  .db 255
.instrument.26.volEnv.data
  .db 17, 17, 16, 16
  .db 16, 16, 15, 15
  .db 15, 15, 14, 14
  .db 14, 14, 13, 13
  .db 13, 13, 12, 11
  .db 10, 9, 8, 7
  .db 6, 5, 4, 3
  .db 2, 1


;........................
  .page 2
.instrument.26.arpEnv

.instrument.26.arpEnv.mode
  .db 0
.instrument.26.arpEnv.size
  .db 0
.instrument.26.arpEnv.loop
  .db 255
.instrument.26.arpEnv.data



;........................
  .page 2
.instrument.26.waveFormEnv

.instrument.26.waveFormEnv.size
  .db 1
.instrument.26.waveFormEnv.loop
  .db 255
.instrument.26.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.27
; name Wave 1 envelope 27
; mode 0

.instrument.27.table
  .dw .instrument.27.volEnv
  .db bank(.instrument.27.volEnv)
  .dw .instrument.27.arpEnv
  .db bank(.instrument.27.arpEnv)
  .dw .instrument.27.waveFormEnv
  .db bank(.instrument.27.waveFormEnv)

;........................
  .page 2
.instrument.27.volEnv

.instrument.27.volEnv.size
  .db 40
.instrument.27.volEnv.loop
  .db 255
.instrument.27.volEnv.data
  .db 23, 21, 19, 19
  .db 18, 18, 18, 18
  .db 17, 17, 17, 17
  .db 16, 16, 16, 16
  .db 15, 15, 15, 15
  .db 14, 14, 14, 14
  .db 13, 13, 13, 12
  .db 11, 10, 9, 8
  .db 7, 6, 5, 4
  .db 3, 2, 1, 0



;........................
  .page 2
.instrument.27.arpEnv

.instrument.27.arpEnv.mode
  .db 0
.instrument.27.arpEnv.size
  .db 0
.instrument.27.arpEnv.loop
  .db 255
.instrument.27.arpEnv.data



;........................
  .page 2
.instrument.27.waveFormEnv

.instrument.27.waveFormEnv.size
  .db 1
.instrument.27.waveFormEnv.loop
  .db 255
.instrument.27.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.28
; name Wave 0 envelope 28
; mode 0

.instrument.28.table
  .dw .instrument.28.volEnv
  .db bank(.instrument.28.volEnv)
  .dw .instrument.28.arpEnv
  .db bank(.instrument.28.arpEnv)
  .dw .instrument.28.waveFormEnv
  .db bank(.instrument.28.waveFormEnv)

;........................
  .page 2
.instrument.28.volEnv

.instrument.28.volEnv.size
  .db 10
.instrument.28.volEnv.loop
  .db 255
.instrument.28.volEnv.data
  .db 20, 18, 16, 16
  .db 15, 14, 13, 12
  .db 11, 10


;........................
  .page 2
.instrument.28.arpEnv

.instrument.28.arpEnv.mode
  .db 0
.instrument.28.arpEnv.size
  .db 0
.instrument.28.arpEnv.loop
  .db 255
.instrument.28.arpEnv.data



;........................
  .page 2
.instrument.28.waveFormEnv

.instrument.28.waveFormEnv.size
  .db 1
.instrument.28.waveFormEnv.loop
  .db 255
.instrument.28.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.29
; name Wave 0 envelope 29
; mode 0

.instrument.29.table
  .dw .instrument.29.volEnv
  .db bank(.instrument.29.volEnv)
  .dw .instrument.29.arpEnv
  .db bank(.instrument.29.arpEnv)
  .dw .instrument.29.waveFormEnv
  .db bank(.instrument.29.waveFormEnv)

;........................
  .page 2
.instrument.29.volEnv

.instrument.29.volEnv.size
  .db 43
.instrument.29.volEnv.loop
  .db 255
.instrument.29.volEnv.data
  .db 22, 20, 18, 18
  .db 17, 17, 17, 17
  .db 16, 16, 16, 16
  .db 15, 15, 15, 15
  .db 14, 14, 14, 14
  .db 13, 13, 13, 13
  .db 12, 12, 12, 12
  .db 11, 11, 11, 11
  .db 10, 9, 8, 7
  .db 6, 5, 4, 3
  .db 2, 1, 0

;........................
  .page 2
.instrument.29.arpEnv

.instrument.29.arpEnv.mode
  .db 0
.instrument.29.arpEnv.size
  .db 0
.instrument.29.arpEnv.loop
  .db 255
.instrument.29.arpEnv.data



;........................
  .page 2
.instrument.29.waveFormEnv

.instrument.29.waveFormEnv.size
  .db 1
.instrument.29.waveFormEnv.loop
  .db 255
.instrument.29.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.30
; name Wave 0 envelope 30
; mode 0

.instrument.30.table
  .dw .instrument.30.volEnv
  .db bank(.instrument.30.volEnv)
  .dw .instrument.30.arpEnv
  .db bank(.instrument.30.arpEnv)
  .dw .instrument.30.waveFormEnv
  .db bank(.instrument.30.waveFormEnv)

;........................
  .page 2
.instrument.30.volEnv

.instrument.30.volEnv.size
  .db 10
.instrument.30.volEnv.loop
  .db 255
.instrument.30.volEnv.data
  .db 22, 20, 18, 18
  .db 17, 17, 17, 16
  .db 15, 14


;........................
  .page 2
.instrument.30.arpEnv

.instrument.30.arpEnv.mode
  .db 0
.instrument.30.arpEnv.size
  .db 0
.instrument.30.arpEnv.loop
  .db 255
.instrument.30.arpEnv.data



;........................
  .page 2
.instrument.30.waveFormEnv

.instrument.30.waveFormEnv.size
  .db 1
.instrument.30.waveFormEnv.loop
  .db 255
.instrument.30.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.31
; name Wave 0 envelope 31
; mode 0

.instrument.31.table
  .dw .instrument.31.volEnv
  .db bank(.instrument.31.volEnv)
  .dw .instrument.31.arpEnv
  .db bank(.instrument.31.arpEnv)
  .dw .instrument.31.waveFormEnv
  .db bank(.instrument.31.waveFormEnv)

;........................
  .page 2
.instrument.31.volEnv

.instrument.31.volEnv.size
  .db 9
.instrument.31.volEnv.loop
  .db 255
.instrument.31.volEnv.data
  .db 22, 20, 18, 18
  .db 17, 17, 17, 17
  .db 16


;........................
  .page 2
.instrument.31.arpEnv

.instrument.31.arpEnv.mode
  .db 0
.instrument.31.arpEnv.size
  .db 0
.instrument.31.arpEnv.loop
  .db 255
.instrument.31.arpEnv.data



;........................
  .page 2
.instrument.31.waveFormEnv

.instrument.31.waveFormEnv.size
  .db 1
.instrument.31.waveFormEnv.loop
  .db 255
.instrument.31.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.32
; name Wave 0 envelope 32
; mode 0

.instrument.32.table
  .dw .instrument.32.volEnv
  .db bank(.instrument.32.volEnv)
  .dw .instrument.32.arpEnv
  .db bank(.instrument.32.arpEnv)
  .dw .instrument.32.waveFormEnv
  .db bank(.instrument.32.waveFormEnv)

;........................
  .page 2
.instrument.32.volEnv

.instrument.32.volEnv.size
  .db 40
.instrument.32.volEnv.loop
  .db 255
.instrument.32.volEnv.data
  .db 16, 16, 15, 15
  .db 15, 15, 14, 14
  .db 14, 14, 13, 13
  .db 13, 13, 12, 12
  .db 12, 12, 11, 11
  .db 11, 11, 10, 10
  .db 10, 10, 9, 9
  .db 9, 9, 8, 8
  .db 7, 6, 5, 4
  .db 3, 2, 1, 0



;........................
  .page 2
.instrument.32.arpEnv

.instrument.32.arpEnv.mode
  .db 0
.instrument.32.arpEnv.size
  .db 0
.instrument.32.arpEnv.loop
  .db 255
.instrument.32.arpEnv.data



;........................
  .page 2
.instrument.32.waveFormEnv

.instrument.32.waveFormEnv.size
  .db 1
.instrument.32.waveFormEnv.loop
  .db 255
.instrument.32.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.33
; name Wave 0 envelope 33
; mode 0

.instrument.33.table
  .dw .instrument.33.volEnv
  .db bank(.instrument.33.volEnv)
  .dw .instrument.33.arpEnv
  .db bank(.instrument.33.arpEnv)
  .dw .instrument.33.waveFormEnv
  .db bank(.instrument.33.waveFormEnv)

;........................
  .page 2
.instrument.33.volEnv

.instrument.33.volEnv.size
  .db 10
.instrument.33.volEnv.loop
  .db 255
.instrument.33.volEnv.data
  .db 16, 16, 15, 15
  .db 15, 15, 14, 13
  .db 12, 11


;........................
  .page 2
.instrument.33.arpEnv

.instrument.33.arpEnv.mode
  .db 0
.instrument.33.arpEnv.size
  .db 0
.instrument.33.arpEnv.loop
  .db 255
.instrument.33.arpEnv.data



;........................
  .page 2
.instrument.33.waveFormEnv

.instrument.33.waveFormEnv.size
  .db 1
.instrument.33.waveFormEnv.loop
  .db 255
.instrument.33.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.34
; name Wave 0 envelope 34
; mode 0

.instrument.34.table
  .dw .instrument.34.volEnv
  .db bank(.instrument.34.volEnv)
  .dw .instrument.34.arpEnv
  .db bank(.instrument.34.arpEnv)
  .dw .instrument.34.waveFormEnv
  .db bank(.instrument.34.waveFormEnv)

;........................
  .page 2
.instrument.34.volEnv

.instrument.34.volEnv.size
  .db 20
.instrument.34.volEnv.loop
  .db 255
.instrument.34.volEnv.data
  .db 22, 20, 18, 18
  .db 17, 17, 17, 17
  .db 16, 16, 16, 16
  .db 15, 14, 13, 12
  .db 11, 10, 9, 8



;........................
  .page 2
.instrument.34.arpEnv

.instrument.34.arpEnv.mode
  .db 0
.instrument.34.arpEnv.size
  .db 0
.instrument.34.arpEnv.loop
  .db 255
.instrument.34.arpEnv.data



;........................
  .page 2
.instrument.34.waveFormEnv

.instrument.34.waveFormEnv.size
  .db 1
.instrument.34.waveFormEnv.loop
  .db 255
.instrument.34.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.35
; name Wave 0 envelope 35
; mode 0

.instrument.35.table
  .dw .instrument.35.volEnv
  .db bank(.instrument.35.volEnv)
  .dw .instrument.35.arpEnv
  .db bank(.instrument.35.arpEnv)
  .dw .instrument.35.waveFormEnv
  .db bank(.instrument.35.waveFormEnv)

;........................
  .page 2
.instrument.35.volEnv

.instrument.35.volEnv.size
  .db 30
.instrument.35.volEnv.loop
  .db 255
.instrument.35.volEnv.data
  .db 16, 16, 15, 15
  .db 15, 15, 14, 14
  .db 14, 14, 13, 13
  .db 13, 13, 12, 12
  .db 12, 12, 11, 10
  .db 9, 8, 7, 6
  .db 5, 4, 3, 2
  .db 1, 0


;........................
  .page 2
.instrument.35.arpEnv

.instrument.35.arpEnv.mode
  .db 0
.instrument.35.arpEnv.size
  .db 0
.instrument.35.arpEnv.loop
  .db 255
.instrument.35.arpEnv.data



;........................
  .page 2
.instrument.35.waveFormEnv

.instrument.35.waveFormEnv.size
  .db 1
.instrument.35.waveFormEnv.loop
  .db 255
.instrument.35.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.36
; name Wave 0 envelope 36
; mode 0

.instrument.36.table
  .dw .instrument.36.volEnv
  .db bank(.instrument.36.volEnv)
  .dw .instrument.36.arpEnv
  .db bank(.instrument.36.arpEnv)
  .dw .instrument.36.waveFormEnv
  .db bank(.instrument.36.waveFormEnv)

;........................
  .page 2
.instrument.36.volEnv

.instrument.36.volEnv.size
  .db 39
.instrument.36.volEnv.loop
  .db 255
.instrument.36.volEnv.data
  .db 22, 20, 18, 18
  .db 17, 17, 17, 17
  .db 16, 16, 16, 16
  .db 15, 15, 15, 15
  .db 14, 14, 14, 14
  .db 13, 13, 13, 13
  .db 12, 12, 12, 11
  .db 10, 9, 8, 7
  .db 6, 5, 4, 3
  .db 2, 1, 0

;........................
  .page 2
.instrument.36.arpEnv

.instrument.36.arpEnv.mode
  .db 0
.instrument.36.arpEnv.size
  .db 0
.instrument.36.arpEnv.loop
  .db 255
.instrument.36.arpEnv.data



;........................
  .page 2
.instrument.36.waveFormEnv

.instrument.36.waveFormEnv.size
  .db 1
.instrument.36.waveFormEnv.loop
  .db 255
.instrument.36.waveFormEnv.data
  .db 0



;###########################################################################
  .page 2
.instrument.37
; name Wave 1 envelope 37
; mode 0

.instrument.37.table
  .dw .instrument.37.volEnv
  .db bank(.instrument.37.volEnv)
  .dw .instrument.37.arpEnv
  .db bank(.instrument.37.arpEnv)
  .dw .instrument.37.waveFormEnv
  .db bank(.instrument.37.waveFormEnv)

;........................
  .page 2
.instrument.37.volEnv

.instrument.37.volEnv.size
  .db 45
.instrument.37.volEnv.loop
  .db 255
.instrument.37.volEnv.data
  .db 24, 22, 20, 20
  .db 19, 19, 19, 19
  .db 18, 18, 18, 18
  .db 17, 17, 17, 17
  .db 16, 16, 16, 16
  .db 15, 15, 15, 15
  .db 14, 14, 14, 14
  .db 13, 13, 13, 13
  .db 12, 11, 10, 9
  .db 8, 7, 6, 5
  .db 4, 3, 2, 1
  .db 0


;........................
  .page 2
.instrument.37.arpEnv

.instrument.37.arpEnv.mode
  .db 0
.instrument.37.arpEnv.size
  .db 0
.instrument.37.arpEnv.loop
  .db 255
.instrument.37.arpEnv.data



;........................
  .page 2
.instrument.37.waveFormEnv

.instrument.37.waveFormEnv.size
  .db 1
.instrument.37.waveFormEnv.loop
  .db 255
.instrument.37.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.38
; name Wave 1 envelope 38
; mode 0

.instrument.38.table
  .dw .instrument.38.volEnv
  .db bank(.instrument.38.volEnv)
  .dw .instrument.38.arpEnv
  .db bank(.instrument.38.arpEnv)
  .dw .instrument.38.waveFormEnv
  .db bank(.instrument.38.waveFormEnv)

;........................
  .page 2
.instrument.38.volEnv

.instrument.38.volEnv.size
  .db 10
.instrument.38.volEnv.loop
  .db 255
.instrument.38.volEnv.data
  .db 24, 22, 20, 20
  .db 19, 19, 19, 18
  .db 17, 16


;........................
  .page 2
.instrument.38.arpEnv

.instrument.38.arpEnv.mode
  .db 0
.instrument.38.arpEnv.size
  .db 0
.instrument.38.arpEnv.loop
  .db 255
.instrument.38.arpEnv.data



;........................
  .page 2
.instrument.38.waveFormEnv

.instrument.38.waveFormEnv.size
  .db 1
.instrument.38.waveFormEnv.loop
  .db 255
.instrument.38.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.39
; name Wave 1 envelope 39
; mode 0

.instrument.39.table
  .dw .instrument.39.volEnv
  .db bank(.instrument.39.volEnv)
  .dw .instrument.39.arpEnv
  .db bank(.instrument.39.arpEnv)
  .dw .instrument.39.waveFormEnv
  .db bank(.instrument.39.waveFormEnv)

;........................
  .page 2
.instrument.39.volEnv

.instrument.39.volEnv.size
  .db 9
.instrument.39.volEnv.loop
  .db 255
.instrument.39.volEnv.data
  .db 24, 22, 20, 20
  .db 19, 19, 19, 19
  .db 18


;........................
  .page 2
.instrument.39.arpEnv

.instrument.39.arpEnv.mode
  .db 0
.instrument.39.arpEnv.size
  .db 0
.instrument.39.arpEnv.loop
  .db 255
.instrument.39.arpEnv.data



;........................
  .page 2
.instrument.39.waveFormEnv

.instrument.39.waveFormEnv.size
  .db 1
.instrument.39.waveFormEnv.loop
  .db 255
.instrument.39.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.40
; name Wave 1 envelope 40
; mode 0

.instrument.40.table
  .dw .instrument.40.volEnv
  .db bank(.instrument.40.volEnv)
  .dw .instrument.40.arpEnv
  .db bank(.instrument.40.arpEnv)
  .dw .instrument.40.waveFormEnv
  .db bank(.instrument.40.waveFormEnv)

;........................
  .page 2
.instrument.40.volEnv

.instrument.40.volEnv.size
  .db 42
.instrument.40.volEnv.loop
  .db 255
.instrument.40.volEnv.data
  .db 18, 18, 17, 17
  .db 17, 17, 16, 16
  .db 16, 16, 15, 15
  .db 15, 15, 14, 14
  .db 14, 14, 13, 13
  .db 13, 13, 12, 12
  .db 12, 12, 11, 11
  .db 11, 11, 10, 10
  .db 9, 8, 7, 6
  .db 5, 4, 3, 2
  .db 1, 0


;........................
  .page 2
.instrument.40.arpEnv

.instrument.40.arpEnv.mode
  .db 0
.instrument.40.arpEnv.size
  .db 0
.instrument.40.arpEnv.loop
  .db 255
.instrument.40.arpEnv.data



;........................
  .page 2
.instrument.40.waveFormEnv

.instrument.40.waveFormEnv.size
  .db 1
.instrument.40.waveFormEnv.loop
  .db 255
.instrument.40.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.41
; name Wave 1 envelope 41
; mode 0

.instrument.41.table
  .dw .instrument.41.volEnv
  .db bank(.instrument.41.volEnv)
  .dw .instrument.41.arpEnv
  .db bank(.instrument.41.arpEnv)
  .dw .instrument.41.waveFormEnv
  .db bank(.instrument.41.waveFormEnv)

;........................
  .page 2
.instrument.41.volEnv

.instrument.41.volEnv.size
  .db 10
.instrument.41.volEnv.loop
  .db 255
.instrument.41.volEnv.data
  .db 18, 18, 17, 17
  .db 17, 17, 16, 15
  .db 14, 13


;........................
  .page 2
.instrument.41.arpEnv

.instrument.41.arpEnv.mode
  .db 0
.instrument.41.arpEnv.size
  .db 0
.instrument.41.arpEnv.loop
  .db 255
.instrument.41.arpEnv.data



;........................
  .page 2
.instrument.41.waveFormEnv

.instrument.41.waveFormEnv.size
  .db 1
.instrument.41.waveFormEnv.loop
  .db 255
.instrument.41.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.42
; name Wave 1 envelope 42
; mode 0

.instrument.42.table
  .dw .instrument.42.volEnv
  .db bank(.instrument.42.volEnv)
  .dw .instrument.42.arpEnv
  .db bank(.instrument.42.arpEnv)
  .dw .instrument.42.waveFormEnv
  .db bank(.instrument.42.waveFormEnv)

;........................
  .page 2
.instrument.42.volEnv

.instrument.42.volEnv.size
  .db 20
.instrument.42.volEnv.loop
  .db 255
.instrument.42.volEnv.data
  .db 24, 22, 20, 20
  .db 19, 19, 19, 19
  .db 18, 18, 18, 18
  .db 17, 16, 15, 14
  .db 13, 12, 11, 10



;........................
  .page 2
.instrument.42.arpEnv

.instrument.42.arpEnv.mode
  .db 0
.instrument.42.arpEnv.size
  .db 0
.instrument.42.arpEnv.loop
  .db 255
.instrument.42.arpEnv.data



;........................
  .page 2
.instrument.42.waveFormEnv

.instrument.42.waveFormEnv.size
  .db 1
.instrument.42.waveFormEnv.loop
  .db 255
.instrument.42.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.43
; name Wave 1 envelope 43
; mode 0

.instrument.43.table
  .dw .instrument.43.volEnv
  .db bank(.instrument.43.volEnv)
  .dw .instrument.43.arpEnv
  .db bank(.instrument.43.arpEnv)
  .dw .instrument.43.waveFormEnv
  .db bank(.instrument.43.waveFormEnv)

;........................
  .page 2
.instrument.43.volEnv

.instrument.43.volEnv.size
  .db 30
.instrument.43.volEnv.loop
  .db 255
.instrument.43.volEnv.data
  .db 18, 18, 17, 17
  .db 17, 17, 16, 16
  .db 16, 16, 15, 15
  .db 15, 15, 14, 14
  .db 14, 14, 13, 12
  .db 11, 10, 9, 8
  .db 7, 6, 5, 4
  .db 3, 2


;........................
  .page 2
.instrument.43.arpEnv

.instrument.43.arpEnv.mode
  .db 0
.instrument.43.arpEnv.size
  .db 0
.instrument.43.arpEnv.loop
  .db 255
.instrument.43.arpEnv.data



;........................
  .page 2
.instrument.43.waveFormEnv

.instrument.43.waveFormEnv.size
  .db 1
.instrument.43.waveFormEnv.loop
  .db 255
.instrument.43.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.44
; name Wave 1 envelope 44
; mode 0

.instrument.44.table
  .dw .instrument.44.volEnv
  .db bank(.instrument.44.volEnv)
  .dw .instrument.44.arpEnv
  .db bank(.instrument.44.arpEnv)
  .dw .instrument.44.waveFormEnv
  .db bank(.instrument.44.waveFormEnv)

;........................
  .page 2
.instrument.44.volEnv

.instrument.44.volEnv.size
  .db 36
.instrument.44.volEnv.loop
  .db 255
.instrument.44.volEnv.data
  .db 24, 22, 20, 20
  .db 19, 19, 19, 19
  .db 18, 18, 18, 18
  .db 17, 17, 17, 17
  .db 16, 16, 16, 16
  .db 15, 14, 13, 12
  .db 11, 10, 9, 8
  .db 7, 6, 5, 4
  .db 3, 2, 1, 0



;........................
  .page 2
.instrument.44.arpEnv

.instrument.44.arpEnv.mode
  .db 0
.instrument.44.arpEnv.size
  .db 0
.instrument.44.arpEnv.loop
  .db 255
.instrument.44.arpEnv.data



;........................
  .page 2
.instrument.44.waveFormEnv

.instrument.44.waveFormEnv.size
  .db 1
.instrument.44.waveFormEnv.loop
  .db 255
.instrument.44.waveFormEnv.data
  .db 1



;###########################################################################
  .page 2
.instrument.45
; name Wave 4 envelope 45
; mode 0

.instrument.45.table
  .dw .instrument.45.volEnv
  .db bank(.instrument.45.volEnv)
  .dw .instrument.45.arpEnv
  .db bank(.instrument.45.arpEnv)
  .dw .instrument.45.waveFormEnv
  .db bank(.instrument.45.waveFormEnv)

;........................
  .page 2
.instrument.45.volEnv

.instrument.45.volEnv.size
  .db 9
.instrument.45.volEnv.loop
  .db 255
.instrument.45.volEnv.data
  .db 19, 20, 21, 22
  .db 23, 24, 24, 22
  .db 20


;........................
  .page 2
.instrument.45.arpEnv

.instrument.45.arpEnv.mode
  .db 0
.instrument.45.arpEnv.size
  .db 0
.instrument.45.arpEnv.loop
  .db 255
.instrument.45.arpEnv.data



;........................
  .page 2
.instrument.45.waveFormEnv

.instrument.45.waveFormEnv.size
  .db 1
.instrument.45.waveFormEnv.loop
  .db 255
.instrument.45.waveFormEnv.data
  .db 4



;###########################################################################
  .page 2
.instrument.46
; name Wave 4 envelope 46
; mode 0

.instrument.46.table
  .dw .instrument.46.volEnv
  .db bank(.instrument.46.volEnv)
  .dw .instrument.46.arpEnv
  .db bank(.instrument.46.arpEnv)
  .dw .instrument.46.waveFormEnv
  .db bank(.instrument.46.waveFormEnv)

;........................
  .page 2
.instrument.46.volEnv

.instrument.46.volEnv.size
  .db 80
.instrument.46.volEnv.loop
  .db 255
.instrument.46.volEnv.data
  .db 19, 20, 21, 22
  .db 23, 24, 24, 22
  .db 20, 20, 20, 20
  .db 20, 20, 20, 20
  .db 20, 19, 19, 19
  .db 19, 19, 19, 19
  .db 19, 18, 18, 18
  .db 18, 18, 18, 18
  .db 18, 17, 17, 17
  .db 17, 17, 17, 17
  .db 17, 16, 16, 16
  .db 16, 16, 16, 16
  .db 16, 15, 15, 15
  .db 15, 15, 15, 15
  .db 15, 14, 14, 14
  .db 14, 14, 14, 14
  .db 14, 13, 13, 13
  .db 13, 13, 13, 12
  .db 12, 11, 11, 10
  .db 10, 9, 9, 8



;........................
  .page 2
.instrument.46.arpEnv

.instrument.46.arpEnv.mode
  .db 0
.instrument.46.arpEnv.size
  .db 0
.instrument.46.arpEnv.loop
  .db 255
.instrument.46.arpEnv.data



;........................
  .page 2
.instrument.46.waveFormEnv

.instrument.46.waveFormEnv.size
  .db 1
.instrument.46.waveFormEnv.loop
  .db 255
.instrument.46.waveFormEnv.data
  .db 4



;###########################################################################
  .page 2
.instrument.47
; name Wave 4 envelope 47
; mode 0

.instrument.47.table
  .dw .instrument.47.volEnv
  .db bank(.instrument.47.volEnv)
  .dw .instrument.47.arpEnv
  .db bank(.instrument.47.arpEnv)
  .dw .instrument.47.waveFormEnv
  .db bank(.instrument.47.waveFormEnv)

;........................
  .page 2
.instrument.47.volEnv

.instrument.47.volEnv.size
  .db 18
.instrument.47.volEnv.loop
  .db 255
.instrument.47.volEnv.data
  .db 19, 20, 21, 22
  .db 23, 24, 24, 22
  .db 20, 20, 20, 20
  .db 20, 20, 20, 20
  .db 20, 19


;........................
  .page 2
.instrument.47.arpEnv

.instrument.47.arpEnv.mode
  .db 0
.instrument.47.arpEnv.size
  .db 0
.instrument.47.arpEnv.loop
  .db 255
.instrument.47.arpEnv.data



;........................
  .page 2
.instrument.47.waveFormEnv

.instrument.47.waveFormEnv.size
  .db 1
.instrument.47.waveFormEnv.loop
  .db 255
.instrument.47.waveFormEnv.data
  .db 4



;###########################################################################
  .page 2
.instrument.48
; name Wave 4 envelope 48
; mode 0

.instrument.48.table
  .dw .instrument.48.volEnv
  .db bank(.instrument.48.volEnv)
  .dw .instrument.48.arpEnv
  .db bank(.instrument.48.arpEnv)
  .dw .instrument.48.waveFormEnv
  .db bank(.instrument.48.waveFormEnv)

;........................
  .page 2
.instrument.48.volEnv

.instrument.48.volEnv.size
  .db 79
.instrument.48.volEnv.loop
  .db 255
.instrument.48.volEnv.data
  .db 20, 20, 20, 20
  .db 20, 20, 20, 19
  .db 19, 19, 19, 19
  .db 19, 19, 19, 18
  .db 18, 18, 18, 18
  .db 18, 18, 18, 17
  .db 17, 17, 17, 17
  .db 17, 17, 17, 16
  .db 16, 16, 16, 16
  .db 16, 16, 16, 15
  .db 15, 15, 15, 15
  .db 15, 15, 15, 14
  .db 14, 14, 14, 14
  .db 14, 14, 14, 13
  .db 13, 13, 13, 13
  .db 13, 13, 13, 12
  .db 12, 12, 12, 12
  .db 12, 12, 11, 11
  .db 10, 10, 9, 9
  .db 8, 8, 7

;........................
  .page 2
.instrument.48.arpEnv

.instrument.48.arpEnv.mode
  .db 0
.instrument.48.arpEnv.size
  .db 0
.instrument.48.arpEnv.loop
  .db 255
.instrument.48.arpEnv.data



;........................
  .page 2
.instrument.48.waveFormEnv

.instrument.48.waveFormEnv.size
  .db 1
.instrument.48.waveFormEnv.loop
  .db 255
.instrument.48.waveFormEnv.data
  .db 4



;###########################################################################
  .page 2
.instrument.49
; name Wave 4 envelope 49
; mode 0

.instrument.49.table
  .dw .instrument.49.volEnv
  .db bank(.instrument.49.volEnv)
  .dw .instrument.49.arpEnv
  .db bank(.instrument.49.arpEnv)
  .dw .instrument.49.waveFormEnv
  .db bank(.instrument.49.waveFormEnv)

;........................
  .page 2
.instrument.49.volEnv

.instrument.49.volEnv.size
  .db 61
.instrument.49.volEnv.loop
  .db 255
.instrument.49.volEnv.data
  .db 20, 20, 20, 20
  .db 20, 20, 20, 19
  .db 19, 19, 19, 19
  .db 19, 19, 19, 18
  .db 18, 18, 18, 18
  .db 18, 18, 18, 17
  .db 17, 17, 17, 17
  .db 17, 17, 17, 16
  .db 16, 16, 16, 16
  .db 16, 16, 16, 15
  .db 15, 15, 15, 15
  .db 15, 15, 15, 14
  .db 14, 14, 14, 14
  .db 14, 13, 13, 12
  .db 12, 11, 11, 10
  .db 0


;........................
  .page 2
.instrument.49.arpEnv

.instrument.49.arpEnv.mode
  .db 0
.instrument.49.arpEnv.size
  .db 0
.instrument.49.arpEnv.loop
  .db 255
.instrument.49.arpEnv.data



;........................
  .page 2
.instrument.49.waveFormEnv

.instrument.49.waveFormEnv.size
  .db 1
.instrument.49.waveFormEnv.loop
  .db 255
.instrument.49.waveFormEnv.data
  .db 4



;###########################################################################
  .page 2
.instrument.50
; name Wave 4 envelope 50
; mode 0

.instrument.50.table
  .dw .instrument.50.volEnv
  .db bank(.instrument.50.volEnv)
  .dw .instrument.50.arpEnv
  .db bank(.instrument.50.arpEnv)
  .dw .instrument.50.waveFormEnv
  .db bank(.instrument.50.waveFormEnv)

;........................
  .page 2
.instrument.50.volEnv

.instrument.50.volEnv.size
  .db 31
.instrument.50.volEnv.loop
  .db 255
.instrument.50.volEnv.data
  .db 19, 20, 21, 22
  .db 23, 24, 24, 22
  .db 20, 20, 20, 20
  .db 20, 20, 20, 20
  .db 20, 19, 19, 19
  .db 19, 19, 19, 19
  .db 19, 18, 18, 18
  .db 18, 17, 0

;........................
  .page 2
.instrument.50.arpEnv

.instrument.50.arpEnv.mode
  .db 0
.instrument.50.arpEnv.size
  .db 0
.instrument.50.arpEnv.loop
  .db 255
.instrument.50.arpEnv.data



;........................
  .page 2
.instrument.50.waveFormEnv

.instrument.50.waveFormEnv.size
  .db 1
.instrument.50.waveFormEnv.loop
  .db 255
.instrument.50.waveFormEnv.data
  .db 4



;###########################################################################
  .page 2
.instrument.51
; name Wave 4 envelope 51
; mode 0

.instrument.51.table
  .dw .instrument.51.volEnv
  .db bank(.instrument.51.volEnv)
  .dw .instrument.51.arpEnv
  .db bank(.instrument.51.arpEnv)
  .dw .instrument.51.waveFormEnv
  .db bank(.instrument.51.waveFormEnv)

;........................
  .page 2
.instrument.51.volEnv

.instrument.51.volEnv.size
  .db 71
.instrument.51.volEnv.loop
  .db 255
.instrument.51.volEnv.data
  .db 20, 20, 20, 20
  .db 20, 20, 20, 19
  .db 19, 19, 19, 19
  .db 19, 19, 19, 18
  .db 18, 18, 18, 18
  .db 18, 18, 18, 17
  .db 17, 17, 17, 17
  .db 17, 17, 17, 16
  .db 16, 16, 16, 16
  .db 16, 16, 16, 15
  .db 15, 15, 15, 15
  .db 15, 15, 15, 14
  .db 14, 14, 14, 14
  .db 14, 14, 14, 13
  .db 13, 13, 13, 13
  .db 13, 13, 12, 12
  .db 11, 11, 10, 10
  .db 9, 9, 0

;........................
  .page 2
.instrument.51.arpEnv

.instrument.51.arpEnv.mode
  .db 0
.instrument.51.arpEnv.size
  .db 0
.instrument.51.arpEnv.loop
  .db 255
.instrument.51.arpEnv.data



;........................
  .page 2
.instrument.51.waveFormEnv

.instrument.51.waveFormEnv.size
  .db 1
.instrument.51.waveFormEnv.loop
  .db 255
.instrument.51.waveFormEnv.data
  .db 4



;###########################################################################
  .page 2
.instrument.52
; name Wave 4 envelope 52
; mode 0

.instrument.52.table
  .dw .instrument.52.volEnv
  .db bank(.instrument.52.volEnv)
  .dw .instrument.52.arpEnv
  .db bank(.instrument.52.arpEnv)
  .dw .instrument.52.waveFormEnv
  .db bank(.instrument.52.waveFormEnv)

;........................
  .page 2
.instrument.52.volEnv

.instrument.52.volEnv.size
  .db 59
.instrument.52.volEnv.loop
  .db 255
.instrument.52.volEnv.data
  .db 19, 20, 21, 22
  .db 23, 24, 24, 22
  .db 20, 20, 20, 20
  .db 20, 20, 20, 20
  .db 20, 19, 19, 19
  .db 19, 19, 19, 19
  .db 19, 18, 18, 18
  .db 18, 18, 18, 18
  .db 18, 17, 17, 17
  .db 17, 17, 17, 17
  .db 17, 16, 16, 16
  .db 16, 16, 16, 16
  .db 16, 15, 15, 15
  .db 15, 15, 14, 14
  .db 13, 13, 12

;........................
  .page 2
.instrument.52.arpEnv

.instrument.52.arpEnv.mode
  .db 0
.instrument.52.arpEnv.size
  .db 0
.instrument.52.arpEnv.loop
  .db 255
.instrument.52.arpEnv.data



;........................
  .page 2
.instrument.52.waveFormEnv

.instrument.52.waveFormEnv.size
  .db 1
.instrument.52.waveFormEnv.loop
  .db 255
.instrument.52.waveFormEnv.data
  .db 4



;###########################################################################
  .page 2
.instrument.53
; name Wave 4 envelope 53
; mode 0

.instrument.53.table
  .dw .instrument.53.volEnv
  .db bank(.instrument.53.volEnv)
  .dw .instrument.53.arpEnv
  .db bank(.instrument.53.arpEnv)
  .dw .instrument.53.waveFormEnv
  .db bank(.instrument.53.waveFormEnv)

;........................
  .page 2
.instrument.53.volEnv

.instrument.53.volEnv.size
  .db 39
.instrument.53.volEnv.loop
  .db 255
.instrument.53.volEnv.data
  .db 20, 20, 20, 20
  .db 20, 20, 20, 19
  .db 19, 19, 19, 19
  .db 19, 19, 19, 18
  .db 18, 18, 18, 18
  .db 18, 18, 18, 17
  .db 17, 17, 17, 17
  .db 17, 17, 17, 16
  .db 16, 16, 16, 16
  .db 15, 15, 14

;........................
  .page 2
.instrument.53.arpEnv

.instrument.53.arpEnv.mode
  .db 0
.instrument.53.arpEnv.size
  .db 0
.instrument.53.arpEnv.loop
  .db 255
.instrument.53.arpEnv.data



;........................
  .page 2
.instrument.53.waveFormEnv

.instrument.53.waveFormEnv.size
  .db 1
.instrument.53.waveFormEnv.loop
  .db 255
.instrument.53.waveFormEnv.data
  .db 4



;###########################################################################
  .page 2
.instrument.54
; name Wave 4 envelope 54
; mode 0

.instrument.54.table
  .dw .instrument.54.volEnv
  .db bank(.instrument.54.volEnv)
  .dw .instrument.54.arpEnv
  .db bank(.instrument.54.arpEnv)
  .dw .instrument.54.waveFormEnv
  .db bank(.instrument.54.waveFormEnv)

;........................
  .page 2
.instrument.54.volEnv

.instrument.54.volEnv.size
  .db 29
.instrument.54.volEnv.loop
  .db 255
.instrument.54.volEnv.data
  .db 20, 20, 20, 20
  .db 20, 20, 20, 19
  .db 19, 19, 19, 19
  .db 19, 19, 19, 18
  .db 18, 18, 18, 18
  .db 18, 18, 18, 17
  .db 17, 17, 17, 17
  .db 16


;........................
  .page 2
.instrument.54.arpEnv

.instrument.54.arpEnv.mode
  .db 0
.instrument.54.arpEnv.size
  .db 0
.instrument.54.arpEnv.loop
  .db 255
.instrument.54.arpEnv.data



;........................
  .page 2
.instrument.54.waveFormEnv

.instrument.54.waveFormEnv.size
  .db 1
.instrument.54.waveFormEnv.loop
  .db 255
.instrument.54.waveFormEnv.data
  .db 4



;###########################################################################
  .page 2
.instrument.55
; name Wave 4 envelope 55
; mode 0

.instrument.55.table
  .dw .instrument.55.volEnv
  .db bank(.instrument.55.volEnv)
  .dw .instrument.55.arpEnv
  .db bank(.instrument.55.arpEnv)
  .dw .instrument.55.waveFormEnv
  .db bank(.instrument.55.waveFormEnv)

;........................
  .page 2
.instrument.55.volEnv

.instrument.55.volEnv.size
  .db 20
.instrument.55.volEnv.loop
  .db 255
.instrument.55.volEnv.data
  .db 20, 20, 20, 20
  .db 20, 20, 20, 19
  .db 19, 19, 19, 19
  .db 19, 19, 19, 18
  .db 18, 18, 18, 17



;........................
  .page 2
.instrument.55.arpEnv

.instrument.55.arpEnv.mode
  .db 0
.instrument.55.arpEnv.size
  .db 0
.instrument.55.arpEnv.loop
  .db 255
.instrument.55.arpEnv.data



;........................
  .page 2
.instrument.55.waveFormEnv

.instrument.55.waveFormEnv.size
  .db 1
.instrument.55.waveFormEnv.loop
  .db 255
.instrument.55.waveFormEnv.data
  .db 4



;###########################################################################
  .page 2
.instrument.56
; name Wave 4 envelope 56
; mode 0

.instrument.56.table
  .dw .instrument.56.volEnv
  .db bank(.instrument.56.volEnv)
  .dw .instrument.56.arpEnv
  .db bank(.instrument.56.arpEnv)
  .dw .instrument.56.waveFormEnv
  .db bank(.instrument.56.waveFormEnv)

;........................
  .page 2
.instrument.56.volEnv

.instrument.56.volEnv.size
  .db 30
.instrument.56.volEnv.loop
  .db 255
.instrument.56.volEnv.data
  .db 19, 20, 21, 22
  .db 23, 24, 24, 22
  .db 20, 20, 20, 20
  .db 20, 20, 20, 20
  .db 20, 19, 19, 19
  .db 19, 19, 19, 19
  .db 19, 18, 18, 18
  .db 18, 17


;........................
  .page 2
.instrument.56.arpEnv

.instrument.56.arpEnv.mode
  .db 0
.instrument.56.arpEnv.size
  .db 0
.instrument.56.arpEnv.loop
  .db 255
.instrument.56.arpEnv.data



;........................
  .page 2
.instrument.56.waveFormEnv

.instrument.56.waveFormEnv.size
  .db 1
.instrument.56.waveFormEnv.loop
  .db 255
.instrument.56.waveFormEnv.data
  .db 4



;###########################################################################
  .page 2
.instrument.57
; name Wave 4 envelope 57
; mode 0

.instrument.57.table
  .dw .instrument.57.volEnv
  .db bank(.instrument.57.volEnv)
  .dw .instrument.57.arpEnv
  .db bank(.instrument.57.arpEnv)
  .dw .instrument.57.waveFormEnv
  .db bank(.instrument.57.waveFormEnv)

;........................
  .page 2
.instrument.57.volEnv

.instrument.57.volEnv.size
  .db 21
.instrument.57.volEnv.loop
  .db 255
.instrument.57.volEnv.data
  .db 19, 20, 21, 22
  .db 23, 24, 24, 22
  .db 20, 20, 20, 20
  .db 20, 20, 20, 20
  .db 20, 19, 19, 19
  .db 0


;........................
  .page 2
.instrument.57.arpEnv

.instrument.57.arpEnv.mode
  .db 0
.instrument.57.arpEnv.size
  .db 0
.instrument.57.arpEnv.loop
  .db 255
.instrument.57.arpEnv.data



;........................
  .page 2
.instrument.57.waveFormEnv

.instrument.57.waveFormEnv.size
  .db 1
.instrument.57.waveFormEnv.loop
  .db 255
.instrument.57.waveFormEnv.data
  .db 4



;###########################################################################
  .page 2
.instrument.58
; name Wave 4 envelope 58
; mode 0

.instrument.58.table
  .dw .instrument.58.volEnv
  .db bank(.instrument.58.volEnv)
  .dw .instrument.58.arpEnv
  .db bank(.instrument.58.arpEnv)
  .dw .instrument.58.waveFormEnv
  .db bank(.instrument.58.waveFormEnv)

;........................
  .page 2
.instrument.58.volEnv

.instrument.58.volEnv.size
  .db 8
.instrument.58.volEnv.loop
  .db 255
.instrument.58.volEnv.data
  .db 20, 20, 20, 20
  .db 20, 20, 20, 19



;........................
  .page 2
.instrument.58.arpEnv

.instrument.58.arpEnv.mode
  .db 0
.instrument.58.arpEnv.size
  .db 0
.instrument.58.arpEnv.loop
  .db 255
.instrument.58.arpEnv.data



;........................
  .page 2
.instrument.58.waveFormEnv

.instrument.58.waveFormEnv.size
  .db 1
.instrument.58.waveFormEnv.loop
  .db 255
.instrument.58.waveFormEnv.data
  .db 4



;###########################################################################
  .page 2
.instrument.59
; name Wave 2 envelope 59
; mode 0

.instrument.59.table
  .dw .instrument.59.volEnv
  .db bank(.instrument.59.volEnv)
  .dw .instrument.59.arpEnv
  .db bank(.instrument.59.arpEnv)
  .dw .instrument.59.waveFormEnv
  .db bank(.instrument.59.waveFormEnv)

;........................
  .page 2
.instrument.59.volEnv

.instrument.59.volEnv.size
  .db 7
.instrument.59.volEnv.loop
  .db 255
.instrument.59.volEnv.data
  .db 30, 27, 25, 22
  .db 20, 17, 0

;........................
  .page 2
.instrument.59.arpEnv

.instrument.59.arpEnv.mode
  .db 0
.instrument.59.arpEnv.size
  .db 0
.instrument.59.arpEnv.loop
  .db 255
.instrument.59.arpEnv.data



;........................
  .page 2
.instrument.59.waveFormEnv

.instrument.59.waveFormEnv.size
  .db 1
.instrument.59.waveFormEnv.loop
  .db 255
.instrument.59.waveFormEnv.data
  .db 2



;###########################################################################
  .page 2
.instrument.60
; name Wave 2 envelope 60
; mode 0

.instrument.60.table
  .dw .instrument.60.volEnv
  .db bank(.instrument.60.volEnv)
  .dw .instrument.60.arpEnv
  .db bank(.instrument.60.arpEnv)
  .dw .instrument.60.waveFormEnv
  .db bank(.instrument.60.waveFormEnv)

;........................
  .page 2
.instrument.60.volEnv

.instrument.60.volEnv.size
  .db 3
.instrument.60.volEnv.loop
  .db 255
.instrument.60.volEnv.data
  .db 30, 27, 0

;........................
  .page 2
.instrument.60.arpEnv

.instrument.60.arpEnv.mode
  .db 0
.instrument.60.arpEnv.size
  .db 0
.instrument.60.arpEnv.loop
  .db 255
.instrument.60.arpEnv.data



;........................
  .page 2
.instrument.60.waveFormEnv

.instrument.60.waveFormEnv.size
  .db 1
.instrument.60.waveFormEnv.loop
  .db 255
.instrument.60.waveFormEnv.data
  .db 2



;###########################################################################
  .page 2
.instrument.61
; name Wave 2 envelope 61
; mode 0

.instrument.61.table
  .dw .instrument.61.volEnv
  .db bank(.instrument.61.volEnv)
  .dw .instrument.61.arpEnv
  .db bank(.instrument.61.arpEnv)
  .dw .instrument.61.waveFormEnv
  .db bank(.instrument.61.waveFormEnv)

;........................
  .page 2
.instrument.61.volEnv

.instrument.61.volEnv.size
  .db 1
.instrument.61.volEnv.loop
  .db 255
.instrument.61.volEnv.data
  .db 25


;........................
  .page 2
.instrument.61.arpEnv

.instrument.61.arpEnv.mode
  .db 0
.instrument.61.arpEnv.size
  .db 0
.instrument.61.arpEnv.loop
  .db 255
.instrument.61.arpEnv.data



;........................
  .page 2
.instrument.61.waveFormEnv

.instrument.61.waveFormEnv.size
  .db 1
.instrument.61.waveFormEnv.loop
  .db 255
.instrument.61.waveFormEnv.data
  .db 2



;###########################################################################
  .page 2
.instrument.62
; name Wave 2 envelope 62
; mode 0

.instrument.62.table
  .dw .instrument.62.volEnv
  .db bank(.instrument.62.volEnv)
  .dw .instrument.62.arpEnv
  .db bank(.instrument.62.arpEnv)
  .dw .instrument.62.waveFormEnv
  .db bank(.instrument.62.waveFormEnv)

;........................
  .page 2
.instrument.62.volEnv

.instrument.62.volEnv.size
  .db 9
.instrument.62.volEnv.loop
  .db 255
.instrument.62.volEnv.data
  .db 26, 26, 25, 24
  .db 23, 23, 22, 21
  .db 20


;........................
  .page 2
.instrument.62.arpEnv

.instrument.62.arpEnv.mode
  .db 0
.instrument.62.arpEnv.size
  .db 0
.instrument.62.arpEnv.loop
  .db 255
.instrument.62.arpEnv.data



;........................
  .page 2
.instrument.62.waveFormEnv

.instrument.62.waveFormEnv.size
  .db 1
.instrument.62.waveFormEnv.loop
  .db 255
.instrument.62.waveFormEnv.data
  .db 2



;###########################################################################
  .page 2
.instrument.63
; name Wave 2 envelope 63
; mode 0

.instrument.63.table
  .dw .instrument.63.volEnv
  .db bank(.instrument.63.volEnv)
  .dw .instrument.63.arpEnv
  .db bank(.instrument.63.arpEnv)
  .dw .instrument.63.waveFormEnv
  .db bank(.instrument.63.waveFormEnv)

;........................
  .page 2
.instrument.63.volEnv

.instrument.63.volEnv.size
  .db 4
.instrument.63.volEnv.loop
  .db 255
.instrument.63.volEnv.data
  .db 26, 26, 25, 24



;........................
  .page 2
.instrument.63.arpEnv

.instrument.63.arpEnv.mode
  .db 0
.instrument.63.arpEnv.size
  .db 0
.instrument.63.arpEnv.loop
  .db 255
.instrument.63.arpEnv.data



;........................
  .page 2
.instrument.63.waveFormEnv

.instrument.63.waveFormEnv.size
  .db 1
.instrument.63.waveFormEnv.loop
  .db 255
.instrument.63.waveFormEnv.data
  .db 2



;###########################################################################
  .page 2
.instrument.64
; name Wave 2 envelope 64
; mode 0

.instrument.64.table
  .dw .instrument.64.volEnv
  .db bank(.instrument.64.volEnv)
  .dw .instrument.64.arpEnv
  .db bank(.instrument.64.arpEnv)
  .dw .instrument.64.waveFormEnv
  .db bank(.instrument.64.waveFormEnv)

;........................
  .page 2
.instrument.64.volEnv

.instrument.64.volEnv.size
  .db 5
.instrument.64.volEnv.loop
  .db 255
.instrument.64.volEnv.data
  .db 30, 28, 26, 24
  .db 22


;........................
  .page 2
.instrument.64.arpEnv

.instrument.64.arpEnv.mode
  .db 0
.instrument.64.arpEnv.size
  .db 0
.instrument.64.arpEnv.loop
  .db 255
.instrument.64.arpEnv.data



;........................
  .page 2
.instrument.64.waveFormEnv

.instrument.64.waveFormEnv.size
  .db 1
.instrument.64.waveFormEnv.loop
  .db 255
.instrument.64.waveFormEnv.data
  .db 2



;###########################################################################
  .page 2
.instrument.65
; name Wave 2 envelope 65
; mode 0

.instrument.65.table
  .dw .instrument.65.volEnv
  .db bank(.instrument.65.volEnv)
  .dw .instrument.65.arpEnv
  .db bank(.instrument.65.arpEnv)
  .dw .instrument.65.waveFormEnv
  .db bank(.instrument.65.waveFormEnv)

;........................
  .page 2
.instrument.65.volEnv

.instrument.65.volEnv.size
  .db 9
.instrument.65.volEnv.loop
  .db 255
.instrument.65.volEnv.data
  .db 30, 28, 26, 24
  .db 22, 20, 18, 16
  .db 0


;........................
  .page 2
.instrument.65.arpEnv

.instrument.65.arpEnv.mode
  .db 0
.instrument.65.arpEnv.size
  .db 0
.instrument.65.arpEnv.loop
  .db 255
.instrument.65.arpEnv.data



;........................
  .page 2
.instrument.65.waveFormEnv

.instrument.65.waveFormEnv.size
  .db 1
.instrument.65.waveFormEnv.loop
  .db 255
.instrument.65.waveFormEnv.data
  .db 2



;###########################################################################
  .page 2
.instrument.66
; name Wave 3 envelope 66
; mode 0

.instrument.66.table
  .dw .instrument.66.volEnv
  .db bank(.instrument.66.volEnv)
  .dw .instrument.66.arpEnv
  .db bank(.instrument.66.arpEnv)
  .dw .instrument.66.waveFormEnv
  .db bank(.instrument.66.waveFormEnv)

;........................
  .page 2
.instrument.66.volEnv

.instrument.66.volEnv.size
  .db 1
.instrument.66.volEnv.loop
  .db 255
.instrument.66.volEnv.data
  .db 0


;........................
  .page 2
.instrument.66.arpEnv

.instrument.66.arpEnv.mode
  .db 0
.instrument.66.arpEnv.size
  .db 0
.instrument.66.arpEnv.loop
  .db 255
.instrument.66.arpEnv.data



;........................
  .page 2
.instrument.66.waveFormEnv

.instrument.66.waveFormEnv.size
  .db 1
.instrument.66.waveFormEnv.loop
  .db 255
.instrument.66.waveFormEnv.data
  .db 3



