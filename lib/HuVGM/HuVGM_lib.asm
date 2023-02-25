;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;
; HuTrack music engine for PC-Engine
;
; Ver: 0.1
;
; History:
; -------
;
;
;

    .include "HuTrack/HuTrack_version.inc"



;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;// Initialize DDA and engine                                                                               /
;////////////////////////////////////////////////////////////////////////////////////////////////////////////
;#init

HuVGM.Init:

            stz HuVGM.song.len
            stz HuVGM.sfx.status
            stz HuVGM.sfx.enabled

            ldx 5
.loop
            stz HuVGM.addr.lo,x
            stz HuVGM.addr.hi,x
            stz HuVGM.addr.bank,x
            dex
          bpl .loop


  rts

HuVGM.Queue:

        ldx HuVGM.song.len

        lda <_hV.EAX0.l
        sta HuVGM.sfx.lo,x
        lda <_hV.EAX0.m
        sta HuVGM.sfx.hi,x
        lda <_hV.EAX0.h
        sta HuVGM.sfx.bank,x

        inc HuVGM.song.len

  rts


HuVGM.status:


  rts
  
HuVGM.stop:


  rts
  
HuVGM.pause:


  rts
  
HuVGM.resume:


  rts
  
HuVGM.play:


  rts
  
