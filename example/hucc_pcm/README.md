# HuCC WAV / PCM example

A six-sound menu using HuTrack's timer-driven DDA playback on PSG channel 5.
The WAV files are converted ahead of time into unpacked 5-bit PCM in ROM.

- Left/right selects a sound and stops current playback; selection wraps.
- I plays or restarts the selected sound.
- II stops playback.
- The status returns to STOPPED when the sample reaches its end marker.

## Build and run

Install HuC/HuCC with PCEAS, then run from the repository root:

```powershell
./example/hucc_pcm/main/build_hucc.bat
```

The script defaults to `C:\huc`. Set `HUCC_HOME` to your installation directory
if different. It locates this repository's `lib` directory automatically and
returns a nonzero exit code on failure.

Open `main/hucc_pcm_example.pce` in a PC Engine emulator or on compatible
hardware. The converted assets are included, so building requires no Python
packages. The example was built with HuCC/PCEAS v4.10.574.g54f5c73 and tested in
Mesen 2.2.1; physical-console listening has not been performed.

## Regenerate the samples

With Python, NumPy, resampy and tkinter available, run:

```powershell
python -m pip install -r requirements.txt
python example/hucc_pcm/convert_samples.py
```

This uses the current `utils/PCM_SFX/waveConvert.py` with 6960 Hz, `kaiser_best`,
unpacked 5-bit output and an `$80` end marker. Include paths are relative to
`main`, where assembly runs. The converter emits page directives throughout
the data so samples can cross ROM banks. `waveConvert_settings.jpg` retains
the original GUI settings reference; the script supplies the correct include
path for this folder layout.

## Integration

The example initializes HuTrack, reserves channel 5 with
`HuTrackEngine_chanReserve()`, and uses `HuTrackEngine_PcmRequest()`,
`HuTrackEngineSFXrest()` and `HuTrackEngine_PCMStatus()`. Stopping or finishing
a sample explicitly silences its channel while keeping the reservation. Playback needs no
HuSFX stream initialization or per-frame HuSFX processing. It keeps channel 5
reserved; a game sharing that channel with music should explicitly release it
when finished, following the [ownership contract](../../docs/compatibility.md#sfx-channel-ownership).

`hucc-sound.inc` reserves the separate ROM table bank required by the current
library. No library or converter source changes are needed by this example.

Imported from [PR #19](https://github.com/Turboxray/HuTrack/pull/19), head
`958d55bd9b78853c0c8bc49b64c92581b85cd95f`, and adapted to the current APIs.
Unused duplicate sample inclusions were removed. All six WAVs are preserved
byte-for-byte; PCM assets were regenerated with the corrected converter.
The corrected WAV reader excludes the RIFF padding byte from `emergency.wav`,
so its converted tail differs from the original PR output.

Mesen validation checked all six complete PCM streams against the PSG writes,
samples spanning up to four banks, stop/retrigger/selection behavior, and
playback status.
