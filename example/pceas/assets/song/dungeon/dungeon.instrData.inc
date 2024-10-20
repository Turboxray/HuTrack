

;###########################################################################
.instrument.0
; name bass decay
; mode 0

.instrument.0.table
  .dw .instrument.0.volEnv
  .dw .instrument.0.arpEnv
  .dw .instrument.0.waveFormEnv

;........................
.instrument.0.volEnv

.instrument.0.volEnv.size
  .db 8
.instrument.0.volEnv.loop
  .db 255
.instrument.0.volEnv.data
  .db 19, 18, 16, 14
  .db 11, 7, 2, 0



;........................
.instrument.0.arpEnv

.instrument.0.arpEnv.mode
  .db 0
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
  .db 0



;###########################################################################
.instrument.1
; name bass
; mode 0

.instrument.1.table
  .dw .instrument.1.volEnv
  .dw .instrument.1.arpEnv
  .dw .instrument.1.waveFormEnv

;........................
.instrument.1.volEnv

.instrument.1.volEnv.size
  .db 10
.instrument.1.volEnv.loop
  .db 255
.instrument.1.volEnv.data
  .db 26, 25, 24, 23
  .db 22, 22, 21, 21
  .db 21, 20


;........................
.instrument.1.arpEnv

.instrument.1.arpEnv.mode
  .db 0
.instrument.1.arpEnv.size
  .db 0
.instrument.1.arpEnv.loop
  .db 255
.instrument.1.arpEnv.data



;........................
.instrument.1.waveFormEnv

.instrument.1.waveFormEnv.size
  .db 1
.instrument.1.waveFormEnv.loop
  .db 255
.instrument.1.waveFormEnv.data
  .db 0



;###########################################################################
.instrument.2
; name bell
; mode 0

.instrument.2.table
  .dw .instrument.2.volEnv
  .dw .instrument.2.arpEnv
  .dw .instrument.2.waveFormEnv

;........................
.instrument.2.volEnv

.instrument.2.volEnv.size
  .db 21
.instrument.2.volEnv.loop
  .db 255
.instrument.2.volEnv.data
  .db 24, 22, 20, 19
  .db 17, 16, 14, 12
  .db 11, 10, 9, 8
  .db 7, 6, 5, 4
  .db 3, 3, 2, 1
  .db 0


;........................
.instrument.2.arpEnv

.instrument.2.arpEnv.mode
  .db 0
.instrument.2.arpEnv.size
  .db 0
.instrument.2.arpEnv.loop
  .db 255
.instrument.2.arpEnv.data



;........................
.instrument.2.waveFormEnv

.instrument.2.waveFormEnv.size
  .db 1
.instrument.2.waveFormEnv.loop
  .db 255
.instrument.2.waveFormEnv.data
  .db 9



;###########################################################################
.instrument.3
; name brass
; mode 0

.instrument.3.table
  .dw .instrument.3.volEnv
  .dw .instrument.3.arpEnv
  .dw .instrument.3.waveFormEnv

;........................
.instrument.3.volEnv

.instrument.3.volEnv.size
  .db 7
.instrument.3.volEnv.loop
  .db 255
.instrument.3.volEnv.data
  .db 25, 27, 26, 24
  .db 22, 21, 20

;........................
.instrument.3.arpEnv

.instrument.3.arpEnv.mode
  .db 0
.instrument.3.arpEnv.size
  .db 0
.instrument.3.arpEnv.loop
  .db 255
.instrument.3.arpEnv.data



;........................
.instrument.3.waveFormEnv

.instrument.3.waveFormEnv.size
  .db 1
.instrument.3.waveFormEnv.loop
  .db 255
.instrument.3.waveFormEnv.data
  .db 8



;###########################################################################
.instrument.4
; name hihat - closed
; mode 0

.instrument.4.table
  .dw .instrument.4.volEnv
  .dw .instrument.4.arpEnv
  .dw .instrument.4.waveFormEnv

;........................
.instrument.4.volEnv

.instrument.4.volEnv.size
  .db 5
.instrument.4.volEnv.loop
  .db 255
.instrument.4.volEnv.data
  .db 24, 13, 2, 1
  .db 0


;........................
.instrument.4.arpEnv

.instrument.4.arpEnv.mode
  .db 0
.instrument.4.arpEnv.size
  .db 0
.instrument.4.arpEnv.loop
  .db 255
.instrument.4.arpEnv.data



;........................
.instrument.4.waveFormEnv

.instrument.4.waveFormEnv.size
  .db 0
.instrument.4.waveFormEnv.loop
  .db 255
.instrument.4.waveFormEnv.data




;###########################################################################
.instrument.5
; name kick
; mode 0

.instrument.5.table
  .dw .instrument.5.volEnv
  .dw .instrument.5.arpEnv
  .dw .instrument.5.waveFormEnv

;........................
.instrument.5.volEnv

.instrument.5.volEnv.size
  .db 6
.instrument.5.volEnv.loop
  .db 255
.instrument.5.volEnv.data
  .db 28, 26, 21, 16
  .db 6, 0


;........................
.instrument.5.arpEnv

.instrument.5.arpEnv.mode
  .db 0
.instrument.5.arpEnv.size
  .db 7
.instrument.5.arpEnv.loop
  .db 255
.instrument.5.arpEnv.data
  .db 0, 254, 252, 250
  .db 248, 246, 0

;........................
.instrument.5.waveFormEnv

.instrument.5.waveFormEnv.size
  .db 1
.instrument.5.waveFormEnv.loop
  .db 255
.instrument.5.waveFormEnv.data
  .db 2



;###########################################################################
.instrument.6
; name overdriven guitar
; mode 0

.instrument.6.table
  .dw .instrument.6.volEnv
  .dw .instrument.6.arpEnv
  .dw .instrument.6.waveFormEnv

;........................
.instrument.6.volEnv

.instrument.6.volEnv.size
  .db 7
.instrument.6.volEnv.loop
  .db 255
.instrument.6.volEnv.data
  .db 23, 21, 22, 22
  .db 21, 21, 20

;........................
.instrument.6.arpEnv

.instrument.6.arpEnv.mode
  .db 0
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
  .db 7



;###########################################################################
.instrument.7
; name piano
; mode 0

.instrument.7.table
  .dw .instrument.7.volEnv
  .dw .instrument.7.arpEnv
  .dw .instrument.7.waveFormEnv

;........................
.instrument.7.volEnv

.instrument.7.volEnv.size
  .db 7
.instrument.7.volEnv.loop
  .db 255
.instrument.7.volEnv.data
  .db 24, 24, 23, 21
  .db 19, 18, 17

;........................
.instrument.7.arpEnv

.instrument.7.arpEnv.mode
  .db 0
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
  .db 4



;###########################################################################
.instrument.8
; name snare
; mode 0

.instrument.8.table
  .dw .instrument.8.volEnv
  .dw .instrument.8.arpEnv
  .dw .instrument.8.waveFormEnv

;........................
.instrument.8.volEnv

.instrument.8.volEnv.size
  .db 13
.instrument.8.volEnv.loop
  .db 255
.instrument.8.volEnv.data
  .db 30, 30, 29, 28
  .db 26, 24, 22, 19
  .db 16, 13, 9, 5
  .db 0


;........................
.instrument.8.arpEnv

.instrument.8.arpEnv.mode
  .db 0
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
  .db 1



;###########################################################################
.instrument.9
; name strings
; mode 0

.instrument.9.table
  .dw .instrument.9.volEnv
  .dw .instrument.9.arpEnv
  .dw .instrument.9.waveFormEnv

;........................
.instrument.9.volEnv

.instrument.9.volEnv.size
  .db 8
.instrument.9.volEnv.loop
  .db 255
.instrument.9.volEnv.data
  .db 17, 20, 18, 19
  .db 18, 18, 18, 17



;........................
.instrument.9.arpEnv

.instrument.9.arpEnv.mode
  .db 0
.instrument.9.arpEnv.size
  .db 0
.instrument.9.arpEnv.loop
  .db 255
.instrument.9.arpEnv.data



;........................
.instrument.9.waveFormEnv

.instrument.9.waveFormEnv.size
  .db 1
.instrument.9.waveFormEnv.loop
  .db 255
.instrument.9.waveFormEnv.data
  .db 3



;###########################################################################
.instrument.10
; name trumpet
; mode 0

.instrument.10.table
  .dw .instrument.10.volEnv
  .dw .instrument.10.arpEnv
  .dw .instrument.10.waveFormEnv

;........................
.instrument.10.volEnv

.instrument.10.volEnv.size
  .db 8
.instrument.10.volEnv.loop
  .db 255
.instrument.10.volEnv.data
  .db 21, 23, 22, 22
  .db 21, 21, 20, 19



;........................
.instrument.10.arpEnv

.instrument.10.arpEnv.mode
  .db 0
.instrument.10.arpEnv.size
  .db 0
.instrument.10.arpEnv.loop
  .db 255
.instrument.10.arpEnv.data



;........................
.instrument.10.waveFormEnv

.instrument.10.waveFormEnv.size
  .db 1
.instrument.10.waveFormEnv.loop
  .db 255
.instrument.10.waveFormEnv.data
  .db 5



;###########################################################################
.instrument.11
; name violin
; mode 0

.instrument.11.table
  .dw .instrument.11.volEnv
  .dw .instrument.11.arpEnv
  .dw .instrument.11.waveFormEnv

;........................
.instrument.11.volEnv

.instrument.11.volEnv.size
  .db 7
.instrument.11.volEnv.loop
  .db 255
.instrument.11.volEnv.data
  .db 21, 20, 19, 18
  .db 17, 17, 18

;........................
.instrument.11.arpEnv

.instrument.11.arpEnv.mode
  .db 0
.instrument.11.arpEnv.size
  .db 0
.instrument.11.arpEnv.loop
  .db 255
.instrument.11.arpEnv.data



;........................
.instrument.11.waveFormEnv

.instrument.11.waveFormEnv.size
  .db 1
.instrument.11.waveFormEnv.loop
  .db 255
.instrument.11.waveFormEnv.data
  .db 6



