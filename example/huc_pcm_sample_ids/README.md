# HuC PCM sample-ID example

This is a complete, ready-to-build HuC 4.x project. It includes the actual C
program, converted PCM samples, waveforms, assembly setup and build script.
No asset conversion, file creation or copying from another example is needed.
It uses the HuTrack and HuSFX library sources in this repository's `lib` folder,
just like the other examples.

## Build and run

With HuC 4.x installed at `C:\huc`, run:

```powershell
./example/huc_pcm_sample_ids/main/build_huc.bat
```

If HuC is installed elsewhere, set `HUC_HOME` to that installation directory.
The script finds this project's files and the repository library automatically.
Open `main/pcm_sample_ids.pce` in a PC Engine emulator or compatible hardware.

- Left/right cycles through three samples in sequence, PCM followed by a
  waveform tone, and PCM with a volume envelope. Changing selection stops
  the current effect.
- I plays or restarts the effect. II stops it.

## Included files

```text
huc_pcm_sample_ids/
  README.md
  main/
    pcm_sample_ids.c       Complete program; start reading here
    build_huc.bat
    huc_reserved_banks.inc
    lib_exclude.asm
    libslot1.asm
    sound.inc
  assets/sfx/
    main.wf.inc
    sample2/hypercocoon.inc       + hypercocoon.data.inc
    sample3/stageclear.inc        + stageclear.data.inc
    sample4/ShubibinmanIII.inc    + ShubibinmanIII.data.inc
```

## C example

[main/pcm_sample_ids.c](main/pcm_sample_ids.c) registers sample labels at runtime
with `HuSFX_QueuePCM()`. Registration stores the sample bank/address and returns
an ID without playing the sound. The first three registrations assign IDs 0,
1 and 2; the code checks those return values before enabling playback.

`three_samples_sfx` is one HuSFX stream that plays those three IDs in sequence.
`pcm_then_wave_sfx` plays ID 0 and then the included square wave for half a
second. Waveform 0 contains 16 samples at 31 and 16 at 0.
`pcm_envelope_sfx` starts ID 2 once, then uses volume commands and waits to
give it a quiet attack, a full-volume hold and a gradual fade. All three use channel 5.
The game reserves it once, processes HuSFX every frame, and releases it when
the effect finishes or the user stops it. No song plays in this example.

The stream macros emit ROM bytes. Their IDs must match the runtime registration
order. `HuPlayPCM` starts or replaces a sample; `HuEndOfStream` stops any remaining
PCM. The game then detects `HU_SFX_STOPPED` and releases the channel.

The waits fit the included samples at approximately 6960 Hz PCM and 60 HuSFX
updates per second. The third sample uses two waits, 255 and 20 updates, because
each wait operand is one byte. Timing is controlled by frame waits, so short
samples leave a gap and long samples are cut off at the next command. These are
not automatic completion waits or gapless concatenation.

## PCM with a volume envelope

Select **PCM ID 2 + volume envelope**, then press I. The stream starts the long
Shubibinman sample only once. `HuDDAvol(level)` changes its hardware playback
volume while the timer keeps reading subsequent sample bytes. It does not
restart the recording or reduce the precision of those bytes.

The attack uses levels 12, 20 and 27 for six updates each, then holds 31 for
36 updates. The fade uses 27, 23, 19, 15, 11, 7 and 3 for 12 updates each.
Finally level 0 is held for six updates before `HuEndOfStream` stops PCM.
That is 144 updates, or about 2.4 seconds at 60 updates/second. The source is
longer than the envelope, so this intentionally cuts off its remaining audio.

31 is full volume and 0 is silent; intermediate values are logarithmic hardware
steps, not percentages. The changes form a simple stepped envelope rather than
a smooth sample-by-sample ramp. Smaller changes with shorter waits can make it
more gradual. HuSFX per-channel and SFX-group volume settings can reduce it further.
At level 0, PCM still advances and uses timer time until it is stopped.

Keep calling `HuSFXprocess()` once per frame to advance the envelope. Use
`HuDDAvol` for PCM; `HuWFvol` selects waveform mode and stops owned PCM.
If you substitute a shorter recording, volume commands cannot extend it or
bring it back after it finishes. Use a suitably long recording, or deliberately
use `HuLoopPCM` with a nonempty sample designed to loop.

See the [illustrated PCM preparation guide](../../docs/huc/huc_hutrack_doc.html#pcm-gain-staging)
for pre-gain, clipping, quiet-tail noise and hardware-volume compensation.

For HuCC, use the separate [complete HuCC project](../hucc_pcm_sample_ids/README.md).
