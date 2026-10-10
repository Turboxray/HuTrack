

;###########################################################################
  .page 2
.instrument.0
; name Wave 1 envelope 00
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
  .db 1



;###########################################################################
  .page 2
.instrument.1
; name Wave 1 envelope 01
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
  .db 2
.instrument.1.volEnv.loop
  .db 255
.instrument.1.volEnv.data
  .db 23, 27


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
  .db 1



;###########################################################################
  .page 2
.instrument.2
; name Wave 1 envelope 02
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
  .db 9
.instrument.2.volEnv.loop
  .db 255
.instrument.2.volEnv.data
  .db 23, 27, 27, 27
  .db 27, 27, 27, 27
  .db 0


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
  .db 1



;###########################################################################
  .page 2
.instrument.3
; name Wave 2 envelope 03
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
  .db 9
.instrument.3.volEnv.loop
  .db 255
.instrument.3.volEnv.data
  .db 27, 27, 26, 26
  .db 24, 24, 22, 22
  .db 0


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
  .db 2



;###########################################################################
  .page 2
.instrument.4
; name Wave 2 envelope 04
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
  .db 7
.instrument.4.volEnv.loop
  .db 255
.instrument.4.volEnv.data
  .db 27, 27, 26, 26
  .db 24, 24, 22

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
  .db 2



;###########################################################################
  .page 2
.instrument.5
; name Wave 3 envelope 05
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
  .db 19
.instrument.5.volEnv.loop
  .db 255
.instrument.5.volEnv.data
  .db 23, 23, 22, 22
  .db 20, 20, 18, 18
  .db 16, 16, 14, 14
  .db 12, 12, 10, 10
  .db 8, 8, 0

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
  .db 3



;###########################################################################
  .page 2
.instrument.6
; name Wave 3 envelope 06
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
  .db 7
.instrument.6.volEnv.loop
  .db 255
.instrument.6.volEnv.data
  .db 23, 23, 22, 22
  .db 20, 20, 18

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
  .db 3



;###########################################################################
  .page 2
.instrument.7
; name Wave 3 envelope 07
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
  .db 15
.instrument.7.volEnv.loop
  .db 255
.instrument.7.volEnv.data
  .db 23, 23, 22, 22
  .db 20, 20, 18, 18
  .db 16, 16, 14, 14
  .db 12, 12, 10

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
  .db 3



;###########################################################################
  .page 2
.instrument.8
; name Wave 2 envelope 08
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
  .db 9
.instrument.8.volEnv.loop
  .db 255
.instrument.8.volEnv.data
  .db 22, 22, 21, 21
  .db 19, 19, 17, 17
  .db 0


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
  .db 2



;###########################################################################
  .page 2
.instrument.9
; name Wave 2 envelope 09
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
  .db 7
.instrument.9.volEnv.loop
  .db 255
.instrument.9.volEnv.data
  .db 22, 22, 21, 21
  .db 19, 19, 17

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
  .db 2



;###########################################################################
  .page 2
.instrument.10
; name Wave 0 envelope 10
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
  .db 1
.instrument.10.volEnv.loop
  .db 255
.instrument.10.volEnv.data
  .db 31


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
  .db 0



