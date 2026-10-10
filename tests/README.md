# Regression tests

Run from the repository root after installing `requirements.txt`. These tests
generate their own small DMF/WAV fixtures; no Furnace checkout, downloaded song
collection or local audit directory is required. Generated files stay in the
ignored `tests/.tmp` directory.

## Converters and documentation

```powershell
python -m unittest discover -s tests -v
```

The suite checks truncated DMF input, the intermediate noise-envelope layout,
failed reloads, title/author boundaries, invalid export names, RIFF chunks,
incomplete PCM frames, samples over 64 KB, VGM sample IDs/loop flags, PCM catalog
capacity/storage, standalone HuSFX assembly, command-line failure messages,
the bundled converter copy, offline guide links/images and every public C overload.
It also checks staged-output and installation failures (including real Windows
file locks), restoration of shared waveform pools, instrument-name comment
safety in assembled output, and VGM stream IDs mapped to different channels.

To also check the public assembly note constants and assemble generated songs
in both supported asset formats, including headers across an 8 KB boundary,
select your installed 4.x assembler:

```powershell
$env:PCEAS = 'C:\huc\bin\pceas.exe'
python -m unittest discover -s tests -v
```

Without PCEAS the assembler tests are explicitly reported as skipped.

## Native HuC and HuCC playback

With a Windows HuC/HuCC 4.x toolchain and Mesen 2 installed:

```powershell
$env:HUC_HOME = 'C:\huc'
$env:MESEN = 'C:\Tools\Mesen\Mesen.exe'
python tests/run_runtime.py
python tests/run_runtime.py --check-failure-paths
```

The runner builds and executes separate HuC and HuCC ROMs from
`runtime_controls.c`. It checks C return values, song registration and invalid
IDs, pause/resume, natural completion, the full last row of PlayOnce, fades,
independent music/SFX volume, pending events, reservations, channel release,
PCM suspension, and an assembly PCM request after noise playback. Mesen checks
actual PSG channel state at 113 checkpoints per compiler, alongside 415 C
assertions. Both the C macro and standalone assembly HuSFX decoders run the
combined PCM/waveform cases: runtime registration, full/cleared lists, header
bank crossings, once/loop playback, empty loops, invalid IDs/flags, global PCM
suspension, volume changes, and stop/EOF/replacement/release. Waveform RAM is
checked after the transition to catch stray PCM writes. The runner also reports
music/fixed code sizes and rejects a bank overflow. It exits unsuccessfully if a
build or check fails.

The runtime checks also cover EC note cuts while another PCM channel keeps the
timer active, ED delays retaining the previous retrigger until the row executes,
and every waveform-upload control write at silent/reduced music volume. Stereo
settings must survive SFX release/reservation/replay; stopping channels 0/1 must
clear LFO without an unrelated channel stop changing it. Both master-volume
overloads are checked against actual PSG writes in each compiler.

Lua callbacks explicitly report failed assertions and stop the emulator. The
optional `--check-failure-paths` run deliberately fails both a PSG-write callback
and a playback checkpoint for each compiler, and requires the runner to reject
all four runs. Execution hooks check the mapped ROM bank as well as the CPU
address, so unrelated HuCC code at the same address cannot count as music work.

The direct PCM API also gets a header split across ROM banks, each invalid
header position at the end of bank FF, empty forced loops and empty one-shots.
Rejected requests must preserve an existing stream's address, bank and status.

`runtime_assembly.inc` puts its small call bridges in the fixed library bank
because they temporarily map another code bank. An ordinary HuCC `.proc` may
itself be placed in that same CPU page and cannot safely perform that remapping.
The standalone decoder and boundary-test sample occupy separate test ROM banks.

These tests do not claim exhaustive effect parity, a worst-case CPU budget,
audio quality or physical-console validation. The supplied example ROMs and
converted music still need listening checks on the intended hardware.

## Music example playback

```powershell
python tests/run_music_examples.py
```

With the same toolchain and `MESEN` setting, this builds the HuC, HuCC and PCEAS
music examples, starts SMB3, then uses the actual controller menus to select
Air Zonk, The Legendary Axe, Aero Blasters and Bonk's Adventure. It checks
titles, banked format, every order on all channels (22, 11, 18 and 8 orders),
audible channels, noise percussion, PCM data-port writes and the loop back to
order 0 at each song's actual final row. Aero Blasters' unused sixth channel
must stay silent after switching songs. PCEAS also plays its standalone SFX
sample to check its placement after the larger music bundle.
Reports stay under `tests/.tmp/music-examples`. Use `--compiler huc`, `hucc` or
`pceas` to check one integration. These checks establish playback and ordering;
they do not judge the musical arrangement or replace listening on hardware.

## HuSFX command boundaries

With the same toolchain and emulator settings, run:

```powershell
python tests/run_sfx_boundaries.py
python tests/run_sfx_boundaries.py --check-failure-paths
```

The runner generates streams across 8 KB bank boundaries and verifies both
decoders under HuC and HuCC. Its 88 checkpoints cover waveform, register,
period, wait and PCM operands; operands equal to FB; raw A4 controls; metadata;
and EOF at the last byte of a bank without processing trailing commands.
The optional failure checks deliberately fail write, checkpoint and end-frame
callbacks for each compiler; missing, duplicate or stale reports also fail.

## Playable PCM sample-ID examples

With the same toolchain and Mesen environment variables, run:

```powershell
python tests/run_pcm_examples.py
```

This builds both complete example projects, selects the PCM-to-waveform entry
through gamepad input, and checks the actual channel output. It verifies PCM
playback, 30 updates of nonconstant waveform data at the expected volume and
period, no late PCM writes into waveform RAM, and channel release afterward.
It then selects the PCM envelope, checks all 12 hardware-volume steps and their
144-update timing, verifies the sample position keeps advancing without a
restart (including at volume zero), and checks end-of-stream cleanup. It also
restarts and cancels the envelope with the gamepad and checks menu wraparound.
The ordinary unittest suite also checks that each example selects a present,
nonconstant 5-bit waveform; an all-zero waveform cannot produce the demo tone.
