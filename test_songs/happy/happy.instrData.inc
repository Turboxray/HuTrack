

;###########################################################################
.instrument.0
; name Bass
; mode 0

.instrument.0.table
  .dw .instrument.0.volEnv
  .dw .instrument.0.arpEnv
  .dw .instrument.0.waveFormEnv

;........................
.instrument.0.volEnv

.instrument.0.volEnv.size
  .db 1
.instrument.0.volEnv.loop
  .db 255
.instrument.0.volEnv.data
  .db 31


;........................
.instrument.0.arpEnv

.instrument.0.arpEnv.mode
  .db 1
.instrument.0.arpEnv.size
  .db 0
.instrument.0.arpEnv.loop
  .db 255
.instrument.0.arpEnv.data



;........................
.instrument.0.waveFormEnv

.instrument.0.waveFormEnv.size
  .db 1
.instrument.0.waveFormEnv.loop
  .db 255
.instrument.0.waveFormEnv.data
  .db 7



;###########################################################################
.instrument.1
; name LowBongo
; mode 0

.instrument.1.table
  .dw .instrument.1.volEnv
  .dw .instrument.1.arpEnv
  .dw .instrument.1.waveFormEnv

;........................
.instrument.1.volEnv

.instrument.1.volEnv.size
  .db 1
.instrument.1.volEnv.loop
  .db 255
.instrument.1.volEnv.data
  .db 31


;........................
.instrument.1.arpEnv

.instrument.1.arpEnv.mode
  .db 1
.instrument.1.arpEnv.size
  .db 4
.instrument.1.arpEnv.loop
  .db 255
.instrument.1.arpEnv.data
  .db 31, 36, 24, 12



;........................
.instrument.1.waveFormEnv

.instrument.1.waveFormEnv.size
  .db 1
.instrument.1.waveFormEnv.loop
  .db 255
.instrument.1.waveFormEnv.data
  .db 1



;###########################################################################
.instrument.2
; name HighBongo
; mode 0

.instrument.2.table
  .dw .instrument.2.volEnv
  .dw .instrument.2.arpEnv
  .dw .instrument.2.waveFormEnv

;........................
.instrument.2.volEnv

.instrument.2.volEnv.size
  .db 1
.instrument.2.volEnv.loop
  .db 255
.instrument.2.volEnv.data
  .db 31


;........................
.instrument.2.arpEnv

.instrument.2.arpEnv.mode
  .db 1
.instrument.2.arpEnv.size
  .db 4
.instrument.2.arpEnv.loop
  .db 255
.instrument.2.arpEnv.data
  .db 31, 36, 24, 24



;........................
.instrument.2.waveFormEnv

.instrument.2.waveFormEnv.size
  .db 1
.instrument.2.waveFormEnv.loop
  .db 255
.instrument.2.waveFormEnv.data
  .db 1



;###########################################################################
.instrument.3
; name Click
; mode 0

.instrument.3.table
  .dw .instrument.3.volEnv
  .dw .instrument.3.arpEnv
  .dw .instrument.3.waveFormEnv

;........................
.instrument.3.volEnv

.instrument.3.volEnv.size
  .db 16
.instrument.3.volEnv.loop
  .db 255
.instrument.3.volEnv.data
  .db 5, 19, 31, 29
  .db 28, 26, 24, 22
  .db 20, 17, 15, 12
  .db 10, 8, 4, 0



;........................
.instrument.3.arpEnv

.instrument.3.arpEnv.mode
  .db 1
.instrument.3.arpEnv.size
  .db 3
.instrument.3.arpEnv.loop
  .db 255
.instrument.3.arpEnv.data
  .db 31, 36, 24

;........................
.instrument.3.waveFormEnv

.instrument.3.waveFormEnv.size
  .db 0
.instrument.3.waveFormEnv.loop
  .db 255
.instrument.3.waveFormEnv.data




;###########################################################################
.instrument.4
; name Harp1
; mode 0

.instrument.4.table
  .dw .instrument.4.volEnv
  .dw .instrument.4.arpEnv
  .dw .instrument.4.waveFormEnv

;........................
.instrument.4.volEnv

.instrument.4.volEnv.size
  .db 1
.instrument.4.volEnv.loop
  .db 255
.instrument.4.volEnv.data
  .db 31


;........................
.instrument.4.arpEnv

.instrument.4.arpEnv.mode
  .db 0
.instrument.4.arpEnv.size
  .db 3
.instrument.4.arpEnv.loop
  .db 0
.instrument.4.arpEnv.data
  .db 0, 7, 12

;........................
.instrument.4.waveFormEnv

.instrument.4.waveFormEnv.size
  .db 1
.instrument.4.waveFormEnv.loop
  .db 255
.instrument.4.waveFormEnv.data
  .db 2



;###########################################################################
.instrument.5
; name Shaker
; mode 0

.instrument.5.table
  .dw .instrument.5.volEnv
  .dw .instrument.5.arpEnv
  .dw .instrument.5.waveFormEnv

;........................
.instrument.5.volEnv

.instrument.5.volEnv.size
  .db 16
.instrument.5.volEnv.loop
  .db 255
.instrument.5.volEnv.data
  .db 0, 31, 150, 0
  .db 32, 0, 0, 0
  .db 0, 0, 0, 113
  .db 0, 0, 0, 0



;........................
.instrument.5.arpEnv

.instrument.5.arpEnv.mode
  .db 1
.instrument.5.arpEnv.size
  .db 1
.instrument.5.arpEnv.loop
  .db 255
.instrument.5.arpEnv.data
  .db 31


;........................
.instrument.5.waveFormEnv

.instrument.5.waveFormEnv.size
  .db 0
.instrument.5.waveFormEnv.loop
  .db 255
.instrument.5.waveFormEnv.data




;###########################################################################
.instrument.6
; name Gweetar
; mode 0

.instrument.6.table
  .dw .instrument.6.volEnv
  .dw .instrument.6.arpEnv
  .dw .instrument.6.waveFormEnv

;........................
.instrument.6.volEnv

.instrument.6.volEnv.size
  .db 36
.instrument.6.volEnv.loop
  .db 255
.instrument.6.volEnv.data
  .db 31, 31, 31, 31
  .db 31, 31, 30, 30
  .db 30, 29, 29, 28
  .db 26, 26, 24, 23
  .db 23, 21, 20, 19
  .db 18, 18, 17, 16
  .db 15, 14, 12, 10
  .db 8, 7, 6, 5
  .db 5, 4, 2, 1



;........................
.instrument.6.arpEnv

.instrument.6.arpEnv.mode
  .db 1
.instrument.6.arpEnv.size
  .db 0
.instrument.6.arpEnv.loop
  .db 255
.instrument.6.arpEnv.data



;........................
.instrument.6.waveFormEnv

.instrument.6.waveFormEnv.size
  .db 1
.instrument.6.waveFormEnv.loop
  .db 255
.instrument.6.waveFormEnv.data
  .db 8



;###########################################################################
.instrument.7
; name Brass1
; mode 0

.instrument.7.table
  .dw .instrument.7.volEnv
  .dw .instrument.7.arpEnv
  .dw .instrument.7.waveFormEnv

;........................
.instrument.7.volEnv

.instrument.7.volEnv.size
  .db 1
.instrument.7.volEnv.loop
  .db 255
.instrument.7.volEnv.data
  .db 31


;........................
.instrument.7.arpEnv

.instrument.7.arpEnv.mode
  .db 1
.instrument.7.arpEnv.size
  .db 0
.instrument.7.arpEnv.loop
  .db 255
.instrument.7.arpEnv.data



;........................
.instrument.7.waveFormEnv

.instrument.7.waveFormEnv.size
  .db 1
.instrument.7.waveFormEnv.loop
  .db 255
.instrument.7.waveFormEnv.data
  .db 0



;###########################################################################
.instrument.8
; name Brass2
; mode 0

.instrument.8.table
  .dw .instrument.8.volEnv
  .dw .instrument.8.arpEnv
  .dw .instrument.8.waveFormEnv

;........................
.instrument.8.volEnv

.instrument.8.volEnv.size
  .db 1
.instrument.8.volEnv.loop
  .db 255
.instrument.8.volEnv.data
  .db 31


;........................
.instrument.8.arpEnv

.instrument.8.arpEnv.mode
  .db 1
.instrument.8.arpEnv.size
  .db 0
.instrument.8.arpEnv.loop
  .db 255
.instrument.8.arpEnv.data



;........................
.instrument.8.waveFormEnv

.instrument.8.waveFormEnv.size
  .db 1
.instrument.8.waveFormEnv.loop
  .db 255
.instrument.8.waveFormEnv.data
  .db 6



