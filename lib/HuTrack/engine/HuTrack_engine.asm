
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

      BBS7 <HuTrack.Status, .engine.PAUSE       ; Music engine suspended

      BBS6 <HuTrack.Status, .process.sfx        ; Song is paused, check SFX
        lda HuTrack.fadeInterval
      beq .fade.done
        HuTrack.CallFar HuTrackEngine.FadeTick
        BBS6 <HuTrack.Status, .process.sfx
.fade.done
        dec HuTrack.tick
      bne .skip.song.parser
        lda HuTrack.endPending
      beq .parse
        HuTrack.CallFar HuTrackEngine.EndSong
        bra .process.sfx
.parse
        HuTrack.CallFar HuTrackEngine.Parser
.skip.song.parser
        BBS6 <HuTrack.Status, .process.sfx      ; recheck if song stopped itself.
        HuTrack.CallFar HuTrackEngine.Process.envelopes

.process.sfx

    ; HuSFX has its own explicit per-frame call: HuSFXprocess().

.process.done
;---------------------------------
.engine.PAUSE


        HuTrack.BenchmarkColorZero  0,0,0


  jmp [HuTrack.returnVec]

