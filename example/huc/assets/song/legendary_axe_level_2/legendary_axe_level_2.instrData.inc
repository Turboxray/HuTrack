

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
  .db 1
.instrument.0.volEnv.loop
  .db 255
.instrument.0.volEnv.data
  .db 0


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
  .db 6
.instrument.1.volEnv.loop
  .db 255
.instrument.1.volEnv.data
  .db 25, 27, 27, 26
  .db 25, 24


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
  .db 8
.instrument.2.volEnv.loop
  .db 255
.instrument.2.volEnv.data
  .db 25, 27, 27, 26
  .db 25, 24, 24, 0



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
; name Wave 0 envelope 03
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
  .db 6
.instrument.3.volEnv.loop
  .db 255
.instrument.3.volEnv.data
  .db 23, 25, 25, 24
  .db 23, 22


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
  .db 0



;###########################################################################
  .page 2
.instrument.4
; name Wave 0 envelope 04
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
  .db 8
.instrument.4.volEnv.loop
  .db 255
.instrument.4.volEnv.data
  .db 23, 25, 25, 24
  .db 23, 22, 22, 0



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
  .db 0



;###########################################################################
  .page 2
.instrument.5
; name Wave 4 envelope 05
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
  .db 8
.instrument.5.volEnv.loop
  .db 255
.instrument.5.volEnv.data
  .db 27, 29, 29, 28
  .db 27, 27, 26, 25



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
  .db 4



;###########################################################################
  .page 2
.instrument.6
; name Wave 4 envelope 06
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
  .db 1
.instrument.6.volEnv.loop
  .db 255
.instrument.6.volEnv.data
  .db 25


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
  .db 4



;###########################################################################
  .page 2
.instrument.7
; name Wave 4 envelope 07
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
  .db 8
.instrument.7.volEnv.loop
  .db 255
.instrument.7.volEnv.data
  .db 27, 29, 29, 28
  .db 27, 27, 26, 0



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
  .db 4



;###########################################################################
  .page 2
.instrument.8
; name Wave 4 envelope 08
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
  .db 5
.instrument.8.volEnv.loop
  .db 255
.instrument.8.volEnv.data
  .db 27, 29, 29, 28
  .db 27


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
  .db 4



;###########################################################################
  .page 2
.instrument.9
; name Wave 4 envelope 09
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
  .db 3
.instrument.9.volEnv.loop
  .db 255
.instrument.9.volEnv.data
  .db 27, 26, 25

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
  .db 4



;###########################################################################
  .page 2
.instrument.10
; name Wave 4 envelope 10
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
  .db 8
.instrument.10.volEnv.loop
  .db 255
.instrument.10.volEnv.data
  .db 25, 25, 25, 25
  .db 25, 25, 25, 0



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
  .db 4



;###########################################################################
  .page 2
.instrument.11
; name Wave 4 envelope 11
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
  .db 7
.instrument.11.volEnv.loop
  .db 255
.instrument.11.volEnv.data
  .db 27, 29, 29, 28
  .db 27, 27, 26

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
  .db 4



;###########################################################################
  .page 2
.instrument.12
; name Wave 4 envelope 12
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
  .db 15
.instrument.12.volEnv.loop
  .db 255
.instrument.12.volEnv.data
  .db 27, 29, 29, 28
  .db 27, 27, 26, 25
  .db 25, 25, 25, 25
  .db 25, 25, 0

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
  .db 4



;###########################################################################
  .page 2
.instrument.13
; name Wave 1 envelope 13
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
  .db 1
.instrument.13.volEnv.loop
  .db 255
.instrument.13.volEnv.data
  .db 0


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
  .db 1



;###########################################################################
  .page 2
.instrument.14
; name Wave 1 envelope 14
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
  .db 5
.instrument.14.volEnv.loop
  .db 255
.instrument.14.volEnv.data
  .db 23, 24, 23, 23
  .db 22


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
  .db 1



;###########################################################################
  .page 2
.instrument.15
; name Wave 1 envelope 15
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
  .db 8
.instrument.15.volEnv.loop
  .db 255
.instrument.15.volEnv.data
  .db 23, 24, 23, 23
  .db 22, 22, 22, 0



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
  .db 1



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
  .db 5
.instrument.16.volEnv.loop
  .db 255
.instrument.16.volEnv.data
  .db 23, 24, 23, 23
  .db 22


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
  .db 1
.instrument.17.volEnv.loop
  .db 255
.instrument.17.volEnv.data
  .db 22


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
  .db 8
.instrument.18.volEnv.loop
  .db 255
.instrument.18.volEnv.data
  .db 22, 22, 22, 22
  .db 22, 22, 22, 0



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
  .db 8
.instrument.19.volEnv.loop
  .db 255
.instrument.19.volEnv.data
  .db 23, 24, 23, 23
  .db 22, 22, 22, 0



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
; name Wave 0 envelope 20
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
  .db 15
.instrument.20.volEnv.loop
  .db 255
.instrument.20.volEnv.data
  .db 23, 24, 23, 23
  .db 22, 22, 22, 22
  .db 22, 22, 22, 22
  .db 22, 22, 0

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
  .db 0



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
  .db 7
.instrument.21.volEnv.loop
  .db 255
.instrument.21.volEnv.data
  .db 27, 29, 29, 28
  .db 27, 27, 26

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
  .db 8
.instrument.22.volEnv.loop
  .db 255
.instrument.22.volEnv.data
  .db 27, 29, 29, 28
  .db 27, 27, 26, 0



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
; name Wave 2 envelope 23
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
  .db 21
.instrument.23.volEnv.loop
  .db 255
.instrument.23.volEnv.data
  .db 29, 29, 28, 28
  .db 27, 27, 26, 26
  .db 25, 25, 25, 25
  .db 24, 24, 24, 24
  .db 23, 23, 23, 23
  .db 22


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
  .db 2



;###########################################################################
  .page 2
.instrument.24
; name Wave 2 envelope 24
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
  .db 8
.instrument.24.volEnv.loop
  .db 255
.instrument.24.volEnv.data
  .db 29, 29, 28, 28
  .db 27, 27, 26, 0



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
  .db 2



;###########################################################################
  .page 2
.instrument.25
; name Wave 2 envelope 25
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
  .db 13
.instrument.25.volEnv.loop
  .db 255
.instrument.25.volEnv.data
  .db 29, 29, 28, 28
  .db 27, 27, 26, 26
  .db 25, 25, 25, 25
  .db 24


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
  .db 2



;###########################################################################
  .page 2
.instrument.26
; name Wave 2 envelope 26
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
  .db 7
.instrument.26.volEnv.loop
  .db 255
.instrument.26.volEnv.data
  .db 29, 29, 28, 28
  .db 27, 27, 26

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
  .db 2



;###########################################################################
  .page 2
.instrument.27
; name Wave 2 envelope 27
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
  .db 21
.instrument.27.volEnv.loop
  .db 255
.instrument.27.volEnv.data
  .db 30, 30, 29, 29
  .db 28, 28, 27, 27
  .db 26, 26, 26, 26
  .db 25, 25, 25, 25
  .db 24, 24, 24, 24
  .db 23


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
  .db 2



;###########################################################################
  .page 2
.instrument.28
; name Wave 2 envelope 28
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
  .db 8
.instrument.28.volEnv.loop
  .db 255
.instrument.28.volEnv.data
  .db 30, 30, 29, 29
  .db 28, 28, 27, 0



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
  .db 2



;###########################################################################
  .page 2
.instrument.29
; name Wave 2 envelope 29
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
  .db 7
.instrument.29.volEnv.loop
  .db 255
.instrument.29.volEnv.data
  .db 30, 30, 29, 29
  .db 28, 28, 27

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
  .db 2



;###########################################################################
  .page 2
.instrument.30
; name Wave 2 envelope 30
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
  .db 6
.instrument.30.volEnv.loop
  .db 255
.instrument.30.volEnv.data
  .db 27, 26, 26, 26
  .db 26, 25


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
  .db 2



;###########################################################################
  .page 2
.instrument.31
; name Wave 2 envelope 31
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
  .db 7
.instrument.31.volEnv.loop
  .db 255
.instrument.31.volEnv.data
  .db 25, 25, 24, 24
  .db 24, 24, 23

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
  .db 2



;###########################################################################
  .page 2
.instrument.32
; name Wave 2 envelope 32
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
  .db 13
.instrument.32.volEnv.loop
  .db 255
.instrument.32.volEnv.data
  .db 30, 30, 29, 29
  .db 28, 28, 27, 27
  .db 26, 26, 26, 26
  .db 25


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
  .db 2



;###########################################################################
  .page 2
.instrument.33
; name Wave 2 envelope 33
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
  .db 25
.instrument.33.volEnv.loop
  .db 255
.instrument.33.volEnv.data
  .db 30, 30, 29, 29
  .db 28, 28, 27, 27
  .db 26, 26, 26, 26
  .db 25, 25, 25, 25
  .db 24, 24, 24, 24
  .db 23, 23, 23, 23
  .db 22


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
  .db 2



;###########################################################################
  .page 2
.instrument.34
; name Wave 2 envelope 34
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
  .db 15
.instrument.34.volEnv.loop
  .db 255
.instrument.34.volEnv.data
  .db 30, 30, 29, 29
  .db 28, 28, 27, 27
  .db 26, 26, 26, 26
  .db 25, 25, 0

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
  .db 2



;###########################################################################
  .page 2
.instrument.35
; name Wave 3 envelope 35
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
  .db 1
.instrument.35.volEnv.loop
  .db 255
.instrument.35.volEnv.data
  .db 26


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
  .db 3



;###########################################################################
  .page 2
.instrument.36
; name Wave 3 envelope 36
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
  .db 2
.instrument.36.volEnv.loop
  .db 255
.instrument.36.volEnv.data
  .db 25, 0


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
  .db 3



;###########################################################################
  .page 2
.instrument.37
; name Wave 3 envelope 37
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
  .db 5
.instrument.37.volEnv.loop
  .db 255
.instrument.37.volEnv.data
  .db 24, 21, 18, 15
  .db 12


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
  .db 3



;###########################################################################
  .page 2
.instrument.38
; name Wave 3 envelope 38
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
  .db 1
.instrument.38.volEnv.loop
  .db 255
.instrument.38.volEnv.data
  .db 9


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
  .db 3



;###########################################################################
  .page 2
.instrument.39
; name Wave 3 envelope 39
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
  .db 1
.instrument.39.volEnv.loop
  .db 255
.instrument.39.volEnv.data
  .db 6


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
  .db 3



;###########################################################################
  .page 2
.instrument.40
; name Wave 3 envelope 40
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
  .db 2
.instrument.40.volEnv.loop
  .db 255
.instrument.40.volEnv.data
  .db 6, 0


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
  .db 3



;###########################################################################
  .page 2
.instrument.41
; name Wave 3 envelope 41
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
  .db 1
.instrument.41.volEnv.loop
  .db 255
.instrument.41.volEnv.data
  .db 25


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
  .db 3



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
  .db 7
.instrument.42.volEnv.loop
  .db 255
.instrument.42.volEnv.data
  .db 24, 26, 26, 25
  .db 24, 24, 23

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
  .db 8
.instrument.43.volEnv.loop
  .db 255
.instrument.43.volEnv.data
  .db 24, 26, 26, 25
  .db 24, 24, 23, 0



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
; name Wave 4 envelope 44
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
  .db 1
.instrument.44.volEnv.loop
  .db 255
.instrument.44.volEnv.data
  .db 0


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
  .db 4



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
  .db 36
.instrument.45.volEnv.loop
  .db 255
.instrument.45.volEnv.data
  .db 27, 29, 29, 28
  .db 27, 27, 26, 25
  .db 25, 25, 25, 25
  .db 25, 25, 25, 25
  .db 25, 25, 25, 25
  .db 25, 25, 25, 25
  .db 25, 25, 25, 25
  .db 25, 25, 25, 25
  .db 25, 25, 25, 0



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



