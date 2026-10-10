# Example soundtrack and music sources

The HuC, HuCC and PCEAS music projects all include these five songs, with
converted assets ready to build. The four game music transcriptions replace
the generated compositions. SMB3 keeps its existing conversion.

| Index | Track | Legacy DMF source | Loop at 60 Hz |
| --- | --- | --- | --- |
| 0 | SMB3 Overworld | Existing converted asset | Unchanged |
| 1 | Air Zonk, stage 1: Aqua Base | [air_zonk_aqua_base.dmf](source/air_zonk_aqua_base.dmf) | 92.23 s |
| 2 | The Legendary Axe (first game), level 2 | [legendary_axe_level_2.dmf](source/legendary_axe_level_2.dmf) | 44.80 s |
| 3 | Aero Blasters, stage 1: Seaside Front | [aero_blasters_seaside_front.dmf](source/aero_blasters_seaside_front.dmf) | 74.67 s |
| 4 | Bonk's Adventure, first level: Round 1 | [bonks_adventure_round_1.dmf](source/bonks_adventure_round_1.dmf) | 34.13 s |

## Build and play

Build the usual projects; each contains all the assets it needs. No Python
installation, original game ROM or conversion step is necessary to build.

- **HuC:** `example/huc/main/build_huc_v4.bat`. In Song mode, use up/down to
  select 0–4, then I to start. II fades music; Run pauses/resumes. Select toggles
  between the song and SFX controls.
- **HuCC:** `example/hucc/main/build_hucc.bat`, with the same controls.
- **PCEAS:** `example/pceas/main/build_asm_rom.bat`. SMB3 starts automatically.
  Up/down immediately switches songs; I plays the standalone PCM sound effect.

Each project's `assets/song/` folder contains `smb3_overworld/`,
`air_zonk_aqua_base/`, `legendary_axe_level_2/`, `aero_blasters_seaside_front/`
and `bonks_adventure_round_1/`. The new assets use HuTrack's banked format and
pack consecutively, including objects across 8 KB boundaries.

In PCEAS, the song loader and parser share the music bank. Calls from the main
program pass through small fixed-bank routines so switching that bank cannot
replace the code currently executing. Keep this arrangement when adapting the
example; `HuTrack.CallFar` alone is not a trampoline between two banks assembled
at the same CPU address. The standalone SFX sample starts in the bank after
`SongAssetsEnd`; its position follows the size of the music bundle.

## Edit in Furnace and convert

Open a file in `source/` in Furnace. These are editable legacy DMF modules,
transcribed from native driver playback. Use official Furnace 0.6.8.3 legacy
playback as the comparison reference; see [compatibility](../../docs/compatibility.md).
Save/export the edited song as legacy DMF, keeping its filename, then run from
the repository root:

```powershell
python -m pip install -r requirements.txt
python example/music/build_music.py
```

This converts all four supplied DMFs without rewriting their musical content
and refreshes their bundles in all three projects. SMB3 is left unchanged.
Each bundle includes files through `../assets/song/`, relative to its project's
`main` directory. The old score generator and its `--compose` option have been
removed; conversion only requires the supplied DMFs and repository tools.

## Instruments and PCM

Air Zonk includes its original RLE percussion decoded into PCM. The selected
Legendary Axe and Aero Blasters tracks use waveform and noise synthesis,
without PCM. Bonk's Adventure uses five waveform channels and PCM percussion
on channel 0. Its four original uncompressed 5-bit sample slots are preserved;
three are used by this track. Bonk's samples are resampled from the original
timer rate (about 3496 Hz) to a legacy DMF sample rate of 8000 Hz. Air Zonk's
samples likewise use the 8000 Hz DMF rate after retiming from the native driver.
HuTrack's converter resamples both sets to its configured 6960 Hz playback rate.

The Legendary Axe, Aero Blasters and Bonk's Adventure volume envelopes are
reconstructed as instrument macros. Pitch changes are represented with notes
and finetune effects. All four use one music update per row, 256 rows per
pattern and an explicit `0B00` loop at the actual final row. Their order counts
are 22, 11, 18 and 8 respectively. These tracks do not insert `EExx` game events;
see the API documentation for adding music synchronization events to your own
songs.

## Playback differences and performance

These transcriptions preserve native driver output at music-update resolution;
they are not the original tracker projects. Legacy DMF's PCE noise-note table
cannot represent every hardware noise rate. In Legendary Axe and Aero Blasters,
noise register values 28 and 30 are approximated by 27 and 31 respectively, so
some percussion timbres differ. Bonk's Adventure needs no noise approximations.
Furnace's anti-click waveform handling, fixed DMF sample rates, 60 Hz retiming
and HuTrack's retained fast pitch calculations also prevent sample-exact
playback equivalence.

These dense transcriptions have **high peak CPU costs**. Earlier single-song
HuC measurements reached about 38000–39000 cycles per update for Air Zonk,
Legendary Axe and Aero Blasters. Bonk averaged about 7851 cycles, with a 44282-cycle
startup and 34830-cycle later peak. Those elapsed measurements include timer
interrupts. These are listening and integration examples; the conversions still
need performance optimization before treating them as game-ready CPU budgets.
No additional pitch conversion was added to the library for these tracks.

## References and checks

The Legendary Axe, Aero Blasters and Bonk's Adventure selections follow the
native HES playlists distributed by Zophar's Domain:
[The Legendary Axe](https://www.zophar.net/music/hes/legendary-axe-the-[makyou-densetsu].html),
[Aero Blasters](https://www.zophar.net/music/turbografx-16-hes/aero-blasters) and
[Bonk's Adventure](https://www.zophar.net/music/hes/bonk-s-adventure-%5Bpc-genjin%5D.html).
Their driver/data banks were checked against local game ROMs; Bonk's match is
the Japanese PC Genjin version. Air Zonk's original driver and decoded RLE
samples were checked directly against native playback.

All four DMFs were rendered with official Furnace 0.6.8.3 and played through
complete loops in HuC/HuTrack test ROMs. Checks allow the documented noise
mapping, waveform phase differences and HuTrack pitch rounding. Bonk's 144 PCM
triggers per loop were checked in Furnace; the HuTrack sample selections and
captured PCM data-port writes matched the converted samples.

For the integration check that builds all three example projects, uses their
menus and plays every new song through its loop, see
[the playback test](../../tests/README.md#music-example-playback). Reports and
extraction scratch files are kept outside the tracked example assets. Emulator
checks do not replace listening on physical hardware.
