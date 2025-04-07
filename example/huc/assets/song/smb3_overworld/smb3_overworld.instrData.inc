

;###########################################################################
.instrument.0
; name Kick 3
; mode 0

.instrument.0.table
  .dw .instrument.0.volEnv
  .dw .instrument.0.arpEnv
  .dw .instrument.0.waveFormEnv

;........................
.instrument.0.volEnv

.instrument.0.volEnv.size
  .db 32
.instrument.0.volEnv.loop
  .db 255
.instrument.0.volEnv.data
  .db 31, 31, 30, 30
  .db 27, 23, 18, 14
  .db 10, 6, 2, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0



;........................
.instrument.0.arpEnv

.instrument.0.arpEnv.mode
  .db 1
.instrument.0.arpEnv.size
  .db 3
.instrument.0.arpEnv.loop
  .db 2
.instrument.0.arpEnv.data
  .db 24, 20, 10

;........................
.instrument.0.waveFormEnv

.instrument.0.waveFormEnv.size
  .db 1
.instrument.0.waveFormEnv.loop
  .db 0
.instrument.0.waveFormEnv.data
  .db 0



;###########################################################################
.instrument.1
; name Bongo 1
; mode 0

.instrument.1.table
  .dw .instrument.1.volEnv
  .dw .instrument.1.arpEnv
  .dw .instrument.1.waveFormEnv

;........................
.instrument.1.volEnv

.instrument.1.volEnv.size
  .db 32
.instrument.1.volEnv.loop
  .db 255
.instrument.1.volEnv.data
  .db 31, 27, 23, 19
  .db 15, 11, 7, 3
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0



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
  .db 1



;###########################################################################
.instrument.2
; name Snare Wave
; mode 0

.instrument.2.table
  .dw .instrument.2.volEnv
  .dw .instrument.2.arpEnv
  .dw .instrument.2.waveFormEnv

;........................
.instrument.2.volEnv

.instrument.2.volEnv.size
  .db 2
.instrument.2.volEnv.loop
  .db 255
.instrument.2.volEnv.data
  .db 31, 0


;........................
.instrument.2.arpEnv

.instrument.2.arpEnv.mode
  .db 0
.instrument.2.arpEnv.size
  .db 1
.instrument.2.arpEnv.loop
  .db 0
.instrument.2.arpEnv.data
  .db 23


;........................
.instrument.2.waveFormEnv

.instrument.2.waveFormEnv.size
  .db 1
.instrument.2.waveFormEnv.loop
  .db 255
.instrument.2.waveFormEnv.data
  .db 2



;###########################################################################
.instrument.3
; name Snare Noise
; mode 0

.instrument.3.table
  .dw .instrument.3.volEnv
  .dw .instrument.3.arpEnv
  .dw .instrument.3.waveFormEnv

;........................
.instrument.3.volEnv

.instrument.3.volEnv.size
  .db 32
.instrument.3.volEnv.loop
  .db 255
.instrument.3.volEnv.data
  .db 27, 26, 25, 24
  .db 22, 21, 20, 19
  .db 17, 16, 15, 14
  .db 12, 11, 10, 9
  .db 7, 6, 5, 4
  .db 2, 1, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0



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
  .db 0



;###########################################################################
.instrument.4
; name Ins 5
; mode 0

.instrument.4.table
  .dw .instrument.4.volEnv
  .dw .instrument.4.arpEnv
  .dw .instrument.4.waveFormEnv

;........................
.instrument.4.volEnv

.instrument.4.volEnv.size
  .db 32
.instrument.4.volEnv.loop
  .db 255
.instrument.4.volEnv.data
  .db 29, 28, 27, 26
  .db 24, 22, 20, 18
  .db 16, 14, 12, 10
  .db 8, 6, 4, 2
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0



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
; name Closed Hi-Hat 2
; mode 0

.instrument.5.table
  .dw .instrument.5.volEnv
  .dw .instrument.5.arpEnv
  .dw .instrument.5.waveFormEnv

;........................
.instrument.5.volEnv

.instrument.5.volEnv.size
  .db 32
.instrument.5.volEnv.loop
  .db 255
.instrument.5.volEnv.data
  .db 28, 24, 16, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0



;........................
.instrument.5.arpEnv

.instrument.5.arpEnv.mode
  .db 1
.instrument.5.arpEnv.size
  .db 1
.instrument.5.arpEnv.loop
  .db 0
.instrument.5.arpEnv.data
  .db 8


;........................
.instrument.5.waveFormEnv

.instrument.5.waveFormEnv.size
  .db 0
.instrument.5.waveFormEnv.loop
  .db 255
.instrument.5.waveFormEnv.data




;###########################################################################
.instrument.6
; name Bass
; mode 0

.instrument.6.table
  .dw .instrument.6.volEnv
  .dw .instrument.6.arpEnv
  .dw .instrument.6.waveFormEnv

;........................
.instrument.6.volEnv

.instrument.6.volEnv.size
  .db 32
.instrument.6.volEnv.loop
  .db 255
.instrument.6.volEnv.data
  .db 31, 31, 28, 28
  .db 28, 28, 27, 27
  .db 27, 27, 26, 26
  .db 26, 26, 25, 25
  .db 25, 25, 25, 25
  .db 25, 25, 25, 25
  .db 25, 25, 25, 25
  .db 24, 24, 24, 24



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
  .db 0
.instrument.6.waveFormEnv.loop
  .db 255
.instrument.6.waveFormEnv.data




;###########################################################################
.instrument.7
; name Bass 2
; mode 0

.instrument.7.table
  .dw .instrument.7.volEnv
  .dw .instrument.7.arpEnv
  .dw .instrument.7.waveFormEnv

;........................
.instrument.7.volEnv

.instrument.7.volEnv.size
  .db 32
.instrument.7.volEnv.loop
  .db 255
.instrument.7.volEnv.data
  .db 31, 28, 27, 27
  .db 27, 27, 26, 26
  .db 26, 26, 25, 25
  .db 25, 25, 24, 24
  .db 24, 24, 23, 23
  .db 23, 23, 22, 22
  .db 22, 22, 21, 21
  .db 21, 21, 20, 20



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
  .db 0
.instrument.7.waveFormEnv.loop
  .db 255
.instrument.7.waveFormEnv.data




;###########################################################################
.instrument.8
; name Trumpet
; mode 0

.instrument.8.table
  .dw .instrument.8.volEnv
  .dw .instrument.8.arpEnv
  .dw .instrument.8.waveFormEnv

;........................
.instrument.8.volEnv

.instrument.8.volEnv.size
  .db 12
.instrument.8.volEnv.loop
  .db 255
.instrument.8.volEnv.data
  .db 23, 29, 31, 31
  .db 30, 30, 29, 29
  .db 29, 29, 28, 28



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
  .db 0
.instrument.8.waveFormEnv.loop
  .db 255
.instrument.8.waveFormEnv.data




;###########################################################################
.instrument.9
; name Decay
; mode 0

.instrument.9.table
  .dw .instrument.9.volEnv
  .dw .instrument.9.arpEnv
  .dw .instrument.9.waveFormEnv

;........................
.instrument.9.volEnv

.instrument.9.volEnv.size
  .db 16
.instrument.9.volEnv.loop
  .db 255
.instrument.9.volEnv.data
  .db 26, 24, 22, 20
  .db 18, 16, 14, 12
  .db 10, 8, 6, 4
  .db 2, 0, 0, 0



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
  .db 0
.instrument.9.waveFormEnv.loop
  .db 255
.instrument.9.waveFormEnv.data




;###########################################################################
.instrument.10
; name Chime
; mode 0

.instrument.10.table
  .dw .instrument.10.volEnv
  .dw .instrument.10.arpEnv
  .dw .instrument.10.waveFormEnv

;........................
.instrument.10.volEnv

.instrument.10.volEnv.size
  .db 32
.instrument.10.volEnv.loop
  .db 255
.instrument.10.volEnv.data
  .db 31, 27, 23, 19
  .db 27, 23, 19, 15
  .db 19, 15, 13, 12
  .db 11, 10, 9, 8
  .db 7, 6, 5, 4
  .db 4, 3, 3, 2
  .db 2, 2, 2, 1
  .db 1, 1, 1, 0



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
  .db 0
.instrument.10.waveFormEnv.loop
  .db 255
.instrument.10.waveFormEnv.data




;###########################################################################
.instrument.11
; name St.Drum
; mode 0

.instrument.11.table
  .dw .instrument.11.volEnv
  .dw .instrument.11.arpEnv
  .dw .instrument.11.waveFormEnv

;........................
.instrument.11.volEnv

.instrument.11.volEnv.size
  .db 32
.instrument.11.volEnv.loop
  .db 255
.instrument.11.volEnv.data
  .db 27, 31, 28, 28
  .db 28, 27, 27, 27
  .db 26, 26, 26, 25
  .db 25, 25, 24, 24
  .db 24, 23, 23, 23
  .db 22, 22, 22, 21
  .db 21, 21, 20, 20
  .db 20, 19, 19, 19



;........................
.instrument.11.arpEnv

.instrument.11.arpEnv.mode
  .db 0
.instrument.11.arpEnv.size
  .db 2
.instrument.11.arpEnv.loop
  .db 255
.instrument.11.arpEnv.data
  .db 244, 0


;........................
.instrument.11.waveFormEnv

.instrument.11.waveFormEnv.size
  .db 0
.instrument.11.waveFormEnv.loop
  .db 255
.instrument.11.waveFormEnv.data




;###########################################################################
.instrument.12
; name Ins C
; mode 0

.instrument.12.table
  .dw .instrument.12.volEnv
  .dw .instrument.12.arpEnv
  .dw .instrument.12.waveFormEnv

;........................
.instrument.12.volEnv

.instrument.12.volEnv.size
  .db 32
.instrument.12.volEnv.loop
  .db 255
.instrument.12.volEnv.data
  .db 31, 31, 30, 30
  .db 29, 29, 28, 28
  .db 27, 26, 26, 25
  .db 24, 24, 23, 22
  .db 22, 21, 20, 20
  .db 19, 18, 18, 17
  .db 16, 16, 15, 14
  .db 14, 13, 12, 12



;........................
.instrument.12.arpEnv

.instrument.12.arpEnv.mode
  .db 0
.instrument.12.arpEnv.size
  .db 0
.instrument.12.arpEnv.loop
  .db 255
.instrument.12.arpEnv.data



;........................
.instrument.12.waveFormEnv

.instrument.12.waveFormEnv.size
  .db 0
.instrument.12.waveFormEnv.loop
  .db 255
.instrument.12.waveFormEnv.data




;###########################################################################
.instrument.13
; name Ins D
; mode 0

.instrument.13.table
  .dw .instrument.13.volEnv
  .dw .instrument.13.arpEnv
  .dw .instrument.13.waveFormEnv

;........................
.instrument.13.volEnv

.instrument.13.volEnv.size
  .db 3
.instrument.13.volEnv.loop
  .db 255
.instrument.13.volEnv.data
  .db 31, 31, 28

;........................
.instrument.13.arpEnv

.instrument.13.arpEnv.mode
  .db 0
.instrument.13.arpEnv.size
  .db 0
.instrument.13.arpEnv.loop
  .db 255
.instrument.13.arpEnv.data



;........................
.instrument.13.waveFormEnv

.instrument.13.waveFormEnv.size
  .db 0
.instrument.13.waveFormEnv.loop
  .db 255
.instrument.13.waveFormEnv.data




