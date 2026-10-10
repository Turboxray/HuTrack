/* Complete HuCC 4.x PCM sample-ID example.
 * Run build_hucc.bat in this folder; all project setup and assets are supplied.
 * See ../README.md for controls. Asset paths are relative to this main folder.
 */
#include "huc.h"
#include "HuTrack/Huc_interface/HuTrack.c"
#include "HuSFX/HuC_interface/HucSFX.c"
#include "HuSFX/HuC_interface/HuVGM_defs.h"
#include "HuCsupport/HuCsupport.h"

#define SFX_CHANNEL 5
#define PCM_HYPERCOCOON 0
#define PCM_STAGE_CLEAR 1
#define PCM_SHUBIBINMAN 2

#asm
.bank HUC_USER_RESERVED
#endasm

/* Pass the header labels to QueuePCM; it skips the header itself. */
#incasmlabel(hypercocoon, "../assets/sfx/sample2/hypercocoon.inc", 2);
#incasmlabel(stage_clear, "../assets/sfx/sample3/stageclear.inc", 2);
#incasmlabel(shubibinman, "../assets/sfx/sample4/ShubibinmanIII.inc", 2);
#incasmlabel(sfx_waveforms, "../assets/sfx/main.wf.inc", 2);

/* These macros build a ROM stream, not a series of C function calls.
 * Registration below must give each label the ID used here.
 * Waits assume one HuSFXprocess() per frame at about 60 frames/second.
 * A new HuPlayPCM replaces any PCM still playing on this channel.
 */
const char three_samples_sfx[] = {
    HuPlayPCM(PCM_HYPERCOCOON),
    HuWait_frames(54),            /* 6178 samples at about 6960 Hz. */
    HuPlayPCM(PCM_STAGE_CLEAR),
    HuWait_frames(49),            /* 5597 samples. */
    HuPlayPCM(PCM_SHUBIBINMAN),
    HuWait_frames(255),           /* 31663 samples need >255 frames. */
    HuWait_frames(20),            /* Split the wait into two commands. */
    HuEndOfStream                 /* Also stops any remaining PCM. */
};

const char pcm_then_wave_sfx[] = {
    HuPlayPCM(PCM_HYPERCOCOON),
    HuWait_frames(54),
    HuStopPCM,
    HuChanWFupdate(0),            /* Audible square wave in sfx_waveforms. */
    HuPeriod(1, 64),              /* Synthesized tone, period 0x140. */
    HuWFvol(31),                  /* Original maximum effect volume. */
    HuWait_frames(30),
    HuEndOfStream
};

/* A simple volume envelope around one uninterrupted PCM playback.
 * HuDDAvol changes hardware volume, not the PCM position or sample bytes.
 * Use the long sample so it is still running throughout this 144-frame
 * (about 2.4-second) attack, hold and fade. EndOfStream cuts off the rest.
 */
const char pcm_envelope_sfx[] = {
    HuDDAvol(12),                 /* Quiet start; 31 is full, 0 silent. */
    HuPlayPCM(PCM_SHUBIBINMAN),    /* Start ONCE. Later commands only set volume. */
    HuWait_frames(6),
    HuDDAvol(20),
    HuWait_frames(6),
    HuDDAvol(27),
    HuWait_frames(6),
    HuDDAvol(31),                 /* Hold full volume for about 0.6 seconds. */
    HuWait_frames(36),
    HuDDAvol(27),                 /* Fade in hardware volume steps. */
    HuWait_frames(12),
    HuDDAvol(23),
    HuWait_frames(12),
    HuDDAvol(19),
    HuWait_frames(12),
    HuDDAvol(15),
    HuWait_frames(12),
    HuDDAvol(11),
    HuWait_frames(12),
    HuDDAvol(7),
    HuWait_frames(12),
    HuDDAvol(3),
    HuWait_frames(12),
    HuDDAvol(0),                  /* Silent, but PCM keeps advancing. */
    HuWait_frames(6),
    HuEndOfStream                 /* Stop PCM; the game releases the channel. */
};

int hypercocoon_id, stage_clear_id, shubibinman_id;
int samples_ready;
int effect_active;
int selected_example;

void stop_example(void)
{
    if (!effect_active) return;
    /* Release stops this channel's HuSFX stream and its owned PCM. */
    HuTrackEngine_chanRelease(SFX_CHANNEL);
    effect_active = 0;
}

void play_example(void)
{
    int result;

    if (!samples_ready) return;
    stop_example();
    if (!HuTrackEngine_TryReserve(SFX_CHANNEL)) return;

    if (selected_example == 0)
        result = HuSFXplay(SFX_CHANNEL, getBank(three_samples_sfx),
                          getAddress(three_samples_sfx));
    else if (selected_example == 1)
        result = HuSFXplay(SFX_CHANNEL, getBank(pcm_then_wave_sfx),
                          getAddress(pcm_then_wave_sfx));
    else
        result = HuSFXplay(SFX_CHANNEL, getBank(pcm_envelope_sfx),
                          getAddress(pcm_envelope_sfx));

    if (result == HU_SFX_OK)
        effect_active = 1;
    else
        HuTrackEngine_chanRelease(SFX_CHANNEL);
}

void update_example(void)
{
    /* One call advances ALL active HuSFX channels. PCM bytes are played
     * independently by HuTrack's timer interrupt between game frames.
     */
    HuSFXprocess();
    if (effect_active && HuSFXstate(SFX_CHANNEL) == HU_SFX_STOPPED)
        stop_example();
}

void draw_example(void)
{
    if (selected_example == 0)
        put_string("Three PCM IDs: 0 -> 1 -> 2    ", 1, 11);
    else if (selected_example == 1)
        put_string("PCM ID 0 -> waveform 0       ", 1, 11);
    else
        put_string("PCM ID 2 + volume envelope   ", 1, 11);
    if (selected_example == 2)
        put_string("Soft attack -> hold -> fade  ", 1, 15);
    else
        put_string("                            ", 1, 15);
    if (!samples_ready)
        put_string("PCM registration failed      ", 1, 13);
    else if (effect_active)
        put_string("Playing on channel 5         ", 1, 13);
    else
        put_string("Stopped; channel released    ", 1, 13);
}

int main(void)
{
    int keys;

    disp_off();
    cls();
    load_default_font();
    HuTrack_Init();
    HuSFX_Init(getBank(sfx_waveforms), getAddress(sfx_waveforms));

    /* Runtime registration: each call stores a bank/address and returns
     * the next ID. It does not play or copy the sample. Failure returns -1.
     * HuSFX_Init has already cleared the catalog; register in this order.
     */
    hypercocoon_id = HuSFX_QueuePCM(hypercocoon);
    stage_clear_id = HuSFX_QueuePCM(stage_clear);
    shubibinman_id = HuSFX_QueuePCM(shubibinman);
    samples_ready = (hypercocoon_id == PCM_HYPERCOCOON &&
                     stage_clear_id == PCM_STAGE_CLEAR &&
                     shubibinman_id == PCM_SHUBIBINMAN);
    effect_active = 0;
    selected_example = 0;

    put_string("HuSFX PCM sample IDs", 1, 2);
    put_string("Runtime registrations:", 1, 4);
    put_string("ID 0: hypercocoon", 1, 6);
    put_string("ID 1: stage clear", 1, 7);
    put_string("ID 2: Shubibinman III", 1, 8);
    put_string("LEFT/RIGHT: choose example", 1, 17);
    put_string("I: play/restart   II: stop", 1, 18);
    put_string("Timing uses frame waits.", 1, 20);
    draw_example();
    disp_on();

    for (;;) {
        vsync();
        update_example();
        keys = joytrg(0);
        if (keys & JOY_RIGHT) {
            stop_example();
            selected_example++;
            if (selected_example > 2) selected_example = 0;
        } else if (keys & JOY_LEFT) {
            stop_example();
            selected_example--;
            if (selected_example < 0) selected_example = 2;
        }
        if (keys & JOY_II)
            stop_example();
        else if (keys & JOY_I)
            play_example();
        draw_example();
    }
    return 0;
}
