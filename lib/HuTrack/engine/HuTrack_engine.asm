
    .include "HuTrack/engine/HuTrack_dda.asm"


;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Music Engine                                                                                            /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;

; This needs to be called for each vblank ISR
HuTrackEngine.EngineCall:


        HuTrack.BenchmarkColorZero  7,0,7


        HuTrack.DDA.reSync                      ; Resync the DDA playback with vblank ISR

        lda HuTrack.Global.VolUpdate
      bpl .skip
        stz HuTrack.Global.VolUpdate
        lda HuTrack.Global.SetVolume
        sta $801
.skip

      BBS7 <HuTrack.Status, .engine.PAUSE       ; Everything is paused.. music and SFX

      BBS6 <HuTrack.Status, .process.sfx        ; Song is paused, check SFX
        dec HuTrack.tick
      bne .skip.song.parser
        HuTrack.CallFar HuTrackEngine.Parser
.skip.song.parser
        BBS6 <HuTrack.Status, .process.sfx      ; recheck if song stopped itself.
        HuTrack.CallFar HuTrackEngine.Process.envelopes

.process.sfx

    ;// TODO: Need handler/func pointer

.process.done
;---------------------------------
.engine.PAUSE


        HuTrack.BenchmarkColorZero  0,0,0


  jmp [HuTrack.returnVec]

