// PCM / DDA sound test for PC Engine / HuCC
//
//   - DDA/PCM voice samples:    HuTrack 7kHz timer-driven ISR
//
// Controls:
//   LEFT / RIGHT   — change selected sound number (stops current playback)
//   I              — play selected sound
//   II             — stop current sound
//
// Build: build_hucc.bat
// The build script locates HuTrack relative to this example.

// ---------------------------------------------------------------------------
// Include stack (order matters for HuCC)
// ---------------------------------------------------------------------------
#include "huc.h"
#include "HuTrack/Huc_interface/HuTrack.c"

// ---------------------------------------------------------------------------
// Sound definitions
// ---------------------------------------------------------------------------
#define SOUND_FIRST   1
#define SOUND_COUNT    6
#define CH_DDA    5   /* HuTrack DDA voice channel */

// ---------------------------------------------------------------------------
// DDA PCM voice samples
// ---------------------------------------------------------------------------
#incasmlabel(sound_1, "../assets/pcm/emergency.inc", 2)
#incasmlabel(sound_2, "../assets/pcm/explosion2.inc", 2)
#incasmlabel(sound_3, "../assets/pcm/hypercocoon.inc", 2)
#incasmlabel(sound_4, "../assets/pcm/lightning.inc", 2)
#incasmlabel(sound_5, "../assets/pcm/stageclear.inc", 2)
#incasmlabel(sound_6, "../assets/pcm/ShubibinmanIIIb.inc", 2)

// ---------------------------------------------------------------------------
// Bank/address lookup tables
// ---------------------------------------------------------------------------
const char pcm_banks[] = {
    ^sound_1, ^sound_2, ^sound_3, ^sound_4,
    ^sound_5, ^sound_6
};
const int *pcm_addrs[] = {
    &sound_1, &sound_2, &sound_3, &sound_4,
    &sound_5, &sound_6
};

// ---------------------------------------------------------------------------
// Playback state
// ---------------------------------------------------------------------------
unsigned char selectedSound;
char          isPlaying;

// Forward declarations
void stopAll(void);
void playSoundIdx(unsigned char idx);

// ---------------------------------------------------------------------------
// stopAll()
// ---------------------------------------------------------------------------
void stopAll(void)
{
    // Silence the output while keeping this PCM-only channel reserved.
    HuTrackEngineSFXrest(CH_DDA);
    isPlaying = 0;
}

// ---------------------------------------------------------------------------
// playSoundIdx(idx)
// ---------------------------------------------------------------------------
void playSoundIdx(unsigned char idx)
{
    stopAll();
    if (idx >= SOUND_COUNT) return;
    isPlaying = HuTrackEngine_PcmRequest(CH_DDA, pcm_banks[idx], (unsigned int)pcm_addrs[idx]) == 1;
}

// ---------------------------------------------------------------------------
// drawMenu()
// ---------------------------------------------------------------------------
void drawMenu(void)
{
    int soundNum;
    soundNum = selectedSound + SOUND_FIRST;

    cls();
    put_string("PCM/DDA SOUND TEST", 6, 2);
    put_string("-- HuCC / HuTrack --", 5, 3);
    put_string("SOUND:", 9, 8);
    put_number(soundNum, 3, 15, 8);
    put_string("STATUS:", 8, 10);
    if (isPlaying) {
        put_string("PLAYING (DDA) ", 15, 10);
    } else {
        put_string("STOPPED       ", 15, 10);
    }

    // Controls hint
    put_string("LEFT/RIGHT : SELECT + STOP", 3, 16);
    put_string("I          : PLAY         ", 3, 17);
    put_string("II         : STOP         ", 3, 18);
}

// ---------------------------------------------------------------------------
// main()
// ---------------------------------------------------------------------------
void main(void)
{
    int joy_trg;

    // Hardware init
    disp_off();
    cls();

    // Font: use HuCC default (no custom font needed)
    set_font_pal(0);

    // Sound engine init
    HuTrack_Init();
    // Keep channel 5 reserved for this PCM-only player. The timer ISR streams
    // samples independently of the music parser and HuSFX control streams.
    HuTrackEngine_chanReserve(CH_DDA);

    selectedSound = 0;
    isPlaying     = 0;

    disp_on();
    drawMenu();

    // ---------------------------------------------------------------------------
    // Main loop
    // ---------------------------------------------------------------------------
    for (;;) {
        vsync();

        // The end marker stops the timer stream; reflect that in the menu.
        if (isPlaying && HuTrackEngine_PCMStatus(CH_DDA) != 1) {
            stopAll();
            drawMenu();
        }

        joy_trg = joytrg(0);

        if (joy_trg & JOY_LEFT) {
            stopAll();
            if (selectedSound == 0)
                selectedSound = SOUND_COUNT - 1;
            else
                selectedSound--;
            drawMenu();
        }

        if (joy_trg & JOY_RIGHT) {
            stopAll();
            selectedSound++;
            if (selectedSound >= SOUND_COUNT)
                selectedSound = 0;
            drawMenu();
        }

        if (joy_trg & JOY_I) {
            playSoundIdx(selectedSound);
            drawMenu();
        }

        if (joy_trg & JOY_II) {
            stopAll();
            drawMenu();
        }
    }
}
