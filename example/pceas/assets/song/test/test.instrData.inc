

;###########################################################################
.instrument.0
; name Trumpet
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
  .db 24


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
  .db 1



;###########################################################################
.instrument.1
; name Saw Bass
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
  .db 24


;........................
.instrument.1.arpEnv

.instrument.1.arpEnv.mode
  .db 1
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
  .db 2



;###########################################################################
.instrument.2
; name Piano
; mode 0

.instrument.2.table
  .dw .instrument.2.volEnv
  .dw .instrument.2.arpEnv
  .dw .instrument.2.waveFormEnv

;........................
.instrument.2.volEnv

.instrument.2.volEnv.size
  .db 33
.instrument.2.volEnv.loop
  .db 255
.instrument.2.volEnv.data
  .db 24, 24, 24, 23
  .db 23, 23, 22, 22
  .db 22, 21, 21, 21
  .db 20, 19, 18, 17
  .db 16, 15, 14, 13
  .db 12, 11, 10, 9
  .db 8, 7, 6, 5
  .db 4, 3, 2, 1
  .db 0


;........................
.instrument.2.arpEnv

.instrument.2.arpEnv.mode
  .db 1
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
  .db 0



;###########################################################################
.instrument.3
; name Drum
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
  .db 24, 24, 24, 24
  .db 24, 24, 0

;........................
.instrument.3.arpEnv

.instrument.3.arpEnv.mode
  .db 1
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
  .db 3



;###########################################################################
.instrument.4
; name Hat
; mode 0

.instrument.4.table
  .dw .instrument.4.volEnv
  .dw .instrument.4.arpEnv
  .dw .instrument.4.waveFormEnv

;........................
.instrument.4.volEnv

.instrument.4.volEnv.size
  .db 7
.instrument.4.volEnv.loop
  .db 255
.instrument.4.volEnv.data
  .db 24, 20, 16, 12
  .db 8, 4, 0

;........................
.instrument.4.arpEnv

.instrument.4.arpEnv.mode
  .db 1
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




