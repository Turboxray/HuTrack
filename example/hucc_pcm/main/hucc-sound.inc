; ***************************************************************************
; hucc-sound.inc  -  HuTrack PCM example sound driver configuration
; ***************************************************************************

; Tell startup.asm to allocate the SOUND_BANK
NEED_SOUND_BANK = 1

; HuTrack keeps its ROM tables outside the fixed sound-library bank.
        .ifndef RESERVE_BANKS
RESERVE_BANKS = 1
        .endif

HUTRACK_BENCHMARK = 0

; __sound_init is called in hucc.asm after RAM clear, before interrupts.
; Stops song and SFX parsing so nothing fires before we call HuTrack_Init().
__sound_init    .macro
                stz     <HuTrack.Status
                ; Stop parsing songs
                smb6    <HuTrack.Status
                ; Stop parsing SFX
                smb5    <HuTrack.Status
                .endm
