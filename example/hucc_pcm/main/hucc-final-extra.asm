; ***************************************************************************
; hucc-final-extra.asm  -  GunhedSounds extra assembler data
; Included by hucc-final.asm at the end of every PCEAS pass.
; Modeled after Collab/MusicBoard/main/hucc-final-extra.asm
; ***************************************************************************

        .data
        include "HuTrack/hutrack.inc"
        include "HuTrack/HuTrack_vars.inc"
        include "HuSFX/HuSFX_vars.inc"
        .code
        include "HuTrack/Huc_interface/HuTrackEngine.asm"

                ; include       "getFarPointer.asm"
