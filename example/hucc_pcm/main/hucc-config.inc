; ***************************************************************************
; hucc-config.inc  -  GunhedSounds project HuCC library configuration
; See C:/PCEngine/huc/include/hucc/hucc-config.inc for full documentation.
; ***************************************************************************

        ; Get the sound driver's configuration settings from this directory.
        include "hucc-sound.inc"

; ---------------------------------------------------------------------------
; Stack size.  96 bytes is typical for small projects.
; ---------------------------------------------------------------------------

HUCC_STACK_SZ   =       96

; ---------------------------------------------------------------------------
; Stack pointer debugging.  Catches stack overflows at runtime.
; ---------------------------------------------------------------------------

HUCC_DEBUG_SP   =       1

; ---------------------------------------------------------------------------
; Number of split-screen scroll regions (HUC_NUM_SCROLLS)
; 4 is the typical minimum; increase if split-screen is needed.
; ---------------------------------------------------------------------------

        .ifndef HUC_NUM_SCROLLS
HUC_NUM_SCROLLS =       8
        .endif  HUC_NUM_SCROLLS

        .ifndef HUC_RESERVE_BANKS
HUC_RESERVE_BANKS =     8
        .endif  HUC_RESERVE_BANKS

; ---------------------------------------------------------------------------
; CD / ISO support — not needed for HuCard target
; ---------------------------------------------------------------------------

        .ifndef SUPPORT_2ISO
SUPPORT_2ISO    =       0
        .endif
