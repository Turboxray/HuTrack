; ***************************************************************************
; ***************************************************************************
;
; hucc-final-extra.asm
;
; hucc-final.asm includes this file at the end of every pass in HuCC or SDCC.
;
; Copyright John Brandwood 2024.
;
; Distributed under the Boost Software License, Version 1.0.
; (See accompanying file LICENSE_1_0.txt or copy at
;  http://www.boost.org/LICENSE_1_0.txt)
;
; ***************************************************************************
; ***************************************************************************
;
; This is used to select which assembly-language library files to include in
; a HuCC project, using labels defined in the compiler's header files.
;
; ***************************************************************************
; ***************************************************************************

		.data
		include	"HuTrack/hutrack.inc"
		include "HuTrack/HuTrack_vars.inc"
		include "HuSFX/HuSFX_vars.inc"
		.code
		include "HuTrack/Huc_interface/HuTrackEngine.asm"

		; include	"farMemCopy.asm"
		; include	"getFarPointer.asm"
		; include	"scale2xSprite.asm"
