

;###########################################################################
.instrument.0
; name Tom Noise
; mode 0

.instrument.0.table
  .dw .instrument.0.volEnv
  .dw .instrument.0.arpEnv
  .dw .instrument.0.waveFormEnv

;........................
.instrument.0.volEnv

.instrument.0.volEnv.size
  .db 2
.instrument.0.volEnv.loop
  .db 255
.instrument.0.volEnv.data
  .db 31, 31


;........................
.instrument.0.arpEnv

.instrument.0.arpEnv.mode
  .db 1
.instrument.0.arpEnv.size
  .db 1
.instrument.0.arpEnv.loop
  .db 0
.instrument.0.arpEnv.data
  .db 7


;........................
.instrument.0.waveFormEnv

.instrument.0.waveFormEnv.size
  .db 0
.instrument.0.waveFormEnv.loop
  .db 255
.instrument.0.waveFormEnv.data




;###########################################################################
.instrument.1
; name Kick 3
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
  .db 31, 31, 30, 30
  .db 27, 23, 18, 14
  .db 10, 6, 2, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0



;........................
.instrument.1.arpEnv

.instrument.1.arpEnv.mode
  .db 1
.instrument.1.arpEnv.size
  .db 3
.instrument.1.arpEnv.loop
  .db 2
.instrument.1.arpEnv.data
  .db 24, 20, 10

;........................
.instrument.1.waveFormEnv

.instrument.1.waveFormEnv.size
  .db 2
.instrument.1.waveFormEnv.loop
  .db 1
.instrument.1.waveFormEnv.data
  .db 0, 1



;###########################################################################
.instrument.2
; name Noise Snare 4
; mode 0

.instrument.2.table
  .dw .instrument.2.volEnv
  .dw .instrument.2.arpEnv
  .dw .instrument.2.waveFormEnv

;........................
.instrument.2.volEnv

.instrument.2.volEnv.size
  .db 32
.instrument.2.volEnv.loop
  .db 255
.instrument.2.volEnv.data
  .db 31, 31, 29, 28
  .db 27, 26, 25, 24
  .db 23, 22, 21, 20
  .db 19, 18, 17, 16
  .db 15, 14, 13, 12
  .db 11, 10, 9, 8
  .db 7, 6, 5, 4
  .db 3, 2, 1, 0



;........................
.instrument.2.arpEnv

.instrument.2.arpEnv.mode
  .db 1
.instrument.2.arpEnv.size
  .db 4
.instrument.2.arpEnv.loop
  .db 3
.instrument.2.arpEnv.data
  .db 35, 30, 31, 31



;........................
.instrument.2.waveFormEnv

.instrument.2.waveFormEnv.size
  .db 2
.instrument.2.waveFormEnv.loop
  .db 255
.instrument.2.waveFormEnv.data
  .db 0, 1



;###########################################################################
.instrument.3
; name Closed Hi-Hat 2
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
  .db 26, 22, 14, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0
  .db 0, 0, 0, 0



;........................
.instrument.3.arpEnv

.instrument.3.arpEnv.mode
  .db 1
.instrument.3.arpEnv.size
  .db 1
.instrument.3.arpEnv.loop
  .db 0
.instrument.3.arpEnv.data
  .db 8


;........................
.instrument.3.waveFormEnv

.instrument.3.waveFormEnv.size
  .db 0
.instrument.3.waveFormEnv.loop
  .db 255
.instrument.3.waveFormEnv.data




;###########################################################################
.instrument.4
; name Ins 4
; mode 0

.instrument.4.table
  .dw .instrument.4.volEnv
  .dw .instrument.4.arpEnv
  .dw .instrument.4.waveFormEnv

;........................
.instrument.4.volEnv

.instrument.4.volEnv.size
  .db 2
.instrument.4.volEnv.loop
  .db 255
.instrument.4.volEnv.data
  .db 29, 26


;........................
.instrument.4.arpEnv

.instrument.4.arpEnv.mode
  .db 1
.instrument.4.arpEnv.size
  .db 2
.instrument.4.arpEnv.loop
  .db 1
.instrument.4.arpEnv.data
  .db 7, 53


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
; name Tom 3
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
  .db 31, 31, 30, 29
  .db 28, 27, 26, 25
  .db 24, 23, 22, 21
  .db 20, 19, 18, 17
  .db 16, 15, 14, 13
  .db 12, 11, 10, 9
  .db 8, 7, 6, 5
  .db 4, 3, 2, 0



;........................
.instrument.5.arpEnv

.instrument.5.arpEnv.mode
  .db 0
.instrument.5.arpEnv.size
  .db 20
.instrument.5.arpEnv.loop
  .db 255
.instrument.5.arpEnv.data
  .db 0, 255, 254, 253
  .db 252, 251, 250, 249
  .db 248, 247, 246, 245
  .db 244, 243, 242, 241
  .db 240, 239, 238, 237



;........................
.instrument.5.waveFormEnv

.instrument.5.waveFormEnv.size
  .db 2
.instrument.5.waveFormEnv.loop
  .db 1
.instrument.5.waveFormEnv.data
  .db 0, 1



;###########################################################################
.instrument.6
; name Ins 6
; mode 0

.instrument.6.table
  .dw .instrument.6.volEnv
  .dw .instrument.6.arpEnv
  .dw .instrument.6.waveFormEnv

;........................
.instrument.6.volEnv

.instrument.6.volEnv.size
  .db 3
.instrument.6.volEnv.loop
  .db 255
.instrument.6.volEnv.data
  .db 31, 31, 28

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
; name Ins 7
; mode 0

.instrument.7.table
  .dw .instrument.7.volEnv
  .dw .instrument.7.arpEnv
  .dw .instrument.7.waveFormEnv

;........................
.instrument.7.volEnv

.instrument.7.volEnv.size
  .db 12
.instrument.7.volEnv.loop
  .db 255
.instrument.7.volEnv.data
  .db 31, 31, 30, 29
  .db 28, 27, 26, 26
  .db 26, 26, 26, 26



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
; name Ins 8
; mode 0

.instrument.8.table
  .dw .instrument.8.volEnv
  .dw .instrument.8.arpEnv
  .dw .instrument.8.waveFormEnv

;........................
.instrument.8.volEnv

.instrument.8.volEnv.size
  .db 8
.instrument.8.volEnv.loop
  .db 255
.instrument.8.volEnv.data
  .db 31, 29, 27, 25
  .db 23, 21, 19, 17



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
; name Ins 9
; mode 0

.instrument.9.table
  .dw .instrument.9.volEnv
  .dw .instrument.9.arpEnv
  .dw .instrument.9.waveFormEnv

;........................
.instrument.9.volEnv

.instrument.9.volEnv.size
  .db 12
.instrument.9.volEnv.loop
  .db 255
.instrument.9.volEnv.data
  .db 29, 31, 31, 30
  .db 30, 29, 28, 27
  .db 26, 26, 26, 26



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
; name Ins 6
; mode 0

.instrument.10.table
  .dw .instrument.10.volEnv
  .dw .instrument.10.arpEnv
  .dw .instrument.10.waveFormEnv

;........................
.instrument.10.volEnv

.instrument.10.volEnv.size
  .db 3
.instrument.10.volEnv.loop
  .db 255
.instrument.10.volEnv.data
  .db 31, 31, 28

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
  .db 2
.instrument.10.waveFormEnv.loop
  .db 255
.instrument.10.waveFormEnv.data
  .db 3, 7



