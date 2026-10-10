# Legacy DMF compatibility and SFX

HuTrack targets **official Furnace 0.6.8.3's import and playback of PC Engine legacy DMF**, with its default DMF compatibility settings. The reference is upstream `tildearrow/furnace`, tag `v0.6.8.3`, commit `f2619dbd988c92bf9c7173648d191648f60aecbf`.

Period slides and effect state follow that released legacy model. Notes, normal vibrato and E5 fine tuning retain **HuTrack's original fast approximations**, as requested. The original quarter-square interpolation and sine magnitudes are preserved; slides add an integer period offset after interpolation. This intentionally differs from Furnace's rounded notes and post-slide pitch scaling, especially when combining large slides with modulation. There is no per-tick period-to-note conversion.

Volume-envelope scaling, effect memory/priority, note scheduling and arpeggio behavior were checked against the release.

## Pin the reference when editing songs

Later official development removed partial pitch linearity at Furnace engine/file-format revision 237. Upstream commit [`29929beea`](https://github.com/tildearrow/furnace/commit/29929beeac0454a89f842947fc807afb13d8107c), dated 2025-10-22, removes the mixed calculation. The DMF importer still selects `linearPitch=1`, which then means fully linear pitch. This is present in the checked `dev255` snapshot (`22d8876505ff4a2bb87cca5dc41324938c1f5c56`). Revision 237 is not a DMF version number.

Use Furnace 0.6.8.3 for playback comparisons and export legacy DMF for conversion. A constant period slide changes the musical interval differently at different notes; adopting the later linear model would change existing songs. A newer reference must therefore be evaluated explicitly. Native Furnace features are not automatically available through DMF export.

## Metadata strings

Song titles and author names export as at most 47 text bytes plus NUL each. Longer fields are truncated with a converter warning; an embedded NUL ends the field and discards its suffix. The runtime still accepts older exports with up to 255 bytes plus NUL per field, but rejects unterminated fields instead of scanning beyond that limit. Both C copy APIs require a writable buffer of at least 48 bytes. See [metadata string limits](huc/huc_hutrack_doc.html#metadata-strings).

## Effect support

Values below are hexadecimal. The converter supports four effect columns and preserves independently present effect arguments. Nonzero pattern breaks seek through compressed rows without executing skipped effects.

| Effect | Implemented behavior |
| --- | --- |
| `00`, `E0` | Three-note arpeggio and tick speed; new-note yield and slide interaction |
| `01`, `02`, `03` | Period slides up/down and target portamento; shared state, clamps and legacy priority/memory |
| `04`, `E3`, `E4` | Vibrato, shape and full-byte fine depth; original HuTrack normal-wave phase/magnitude |
| `05`, `06` | Volume slide plus remembered vibrato / remembered portamento, respectively |
| `07`, `0A` | Tremolo and fractional volume slide, including pre-v25 underflow behavior |
| `08` | Channel stereo pan |
| `09`, `0F` | Alternating row speeds; timebase folded in by the converter |
| `0B`, `0D` | Order jump / next-order row break; all channel cursors reset together |
| `0C`, `EC`, `ED` | Retrigger, note cut and delayed row/note |
| `10`, `11` | Wave selection and noise mode; hardware noise is limited to channels 4/5 |
| `12`, `13` | Hardware LFO mode and speed (`255 - argument` register mapping) |
| `17`, `EB` | PCM mode and twelve-sample bank selection within HuTrack's fixed-rate PCM path |
| `E1`, `E2` | Short slides: high nibble times four period units, low nibble target distance |
| `E5` | Fine tuning; pre-v20 values receive Furnace's import-time conversion |
| `E6`, `E8`, `E9`, `EA` | Legacy delayed legato, delayed up/down legato, and legato mode |
| `EE` | Publish the argument in `HuTrack.externalValue` and set `HuTrack.externalPending`; the application reads and clears the pending flag |
| `EF` | Cumulative signed global fine tuning, including negative rounding and deferred adoption on a pitch update |

`E7` has no release point to trigger in the legacy instrument format and is a no-op. Custom experimental `18`, `19`, `20`, native Furnace effects and other unsupported codes are not implemented; the converter warns for unsupported codes. `EE` holds the most recent event, not a queue.

`EC` stops the music PCM writer as well as silencing the channel. An `ED` delay
keeps a preceding `0C` retrigger running until the delayed row actually executes,
matching the released Furnace order of operations. Music attenuation also applies
to temporary control writes during waveform uploads, so changing waves does not
briefly bypass a mute or fade.

## SFX channel ownership

Reserve a channel before an SFX writes to it. Music continues advancing its logical state while the channel belongs to SFX. Release **silences the channel and waits for a fresh music note**. It does not resume the middle of a held note.

On that fresh note, HuTrack restarts the instrument envelopes, restores pan/noise/PCM mode, and reloads all 32 waveform samples even when the instrument did not change. Effect-only rows, cuts and retriggers do not end the wait. An `ED`-delayed note ends it when the note actually triggers. A fresh note with portamento also ends it. Repeated release is harmless; channel numbers outside 0..5 are ignored.

| Interface | Reserve | Release |
| --- | --- | --- |
| HuC/HuCC | `HuTrackEngine_chanReserve(channel)` | `HuTrackEngine_chanRelease(channel)` |
| Assembly | Set `_hk.EAX0.l`, call `HuTrackEngine.setChanForSFX` | Set `_hk.EAX0.u`, call `HuTrackEngine.chanReleaseSFX` |

C status results now follow each compiler's register convention. `HuTrackEngine_SFXmode()` returns bits 0..5 for the reserved channels; its channel overload returns 1 when reserved and 0 otherwise. `HuTrackEngine_PCMStatus(channel)` returns 1 while streaming, 0 when stopped, and 2 for an invalid/unreserved channel.

Call the assembly routines through the usual bank-call convention. A typical C sequence is:

```c
HuTrackEngine_chanReserve(channel);
HuSFXplay(channel, stream_bank, stream_address);
/* Keep calling HuSFXprocess() at the SFX tick rate. */
/* When HuSFXstate(channel) reports HU_SFX_STOPPED: */
HuTrackEngine_chanRelease(channel);
```

Reservation is explicit: `HuSFXplay()` does not reserve, and stream EOF does not release. Applications can retain a channel between consecutive sounds. Release cancels an active HuSFX stream when `HuSFX_vars.inc` is included before the HuTrack implementation; stop an external/custom SFX writer before releasing.

Hardware LFO couples channels 0/1. HuTrack suspends it while either is reserved or waiting for a note, then reapplies the stored mode/speed when both are available. Borrowing channels 2..5 does not disable it. Pause, Stop and song changes preserve reserved SFX channels. Pause/Resume also preserve music PCM positions; after an SFX release, Resume still waits for a fresh music note. Only HuTrack_Init performs a full engine/reservation reset and must be coordinated with other SFX writers.

PCM requests explicitly enable DDA again after a rest, unless PauseDDA has globally suspended streaming. The C PCM API takes the existing three-byte-header asset pointer; the assembly SFX PCM API takes its existing raw-data pointer. These conventions are not interchangeable. HuSFX stream commands `FC`/`FD` start/stop samples registered at runtime through `HuSFX_QueuePCM(label)`. `FC` takes an ID and a flag (0 once, 1 loop); the same effect can continue with waveform/noise commands after PCM. Both decoders stop the timer writer before a waveform/mode transition and clean up owned PCM on stop, replacement, EOF or release. Empty loops are rejected. `HuSFX_ClearPCM()` clears future ID lookups without changing an already-playing sample. Default capacity is 64; configurable `HUSFX_PCM_SLOTS` uses three bytes per entry plus eight bytes of bookkeeping. HuSFX's waveform pool is shared, so concurrent streams must use the same pool.

HuSFX command lengths and C byte-stream macros are documented in [the control-code format](../utils/PSG_SFX/decode.txt). `FB` ends the stream with no operand; `FC` consumes two operands: registered sample ID and loop flag. `FE` supports unsigned waits of 1..255 updates (zero means one), and `FF` waits one. Compact DDA volume `20..3F` expands to `C0..DF`; raw `A4` operands do not expand. Re-export old binary streams containing `FC`: the former binary writer omitted an operand byte, which could misdecode later data as EOF. Assembler exports already emitted both bytes. Re-export VGM PCM effects as well: the importer formerly selected the high byte of the sample ID and forced looping. It now preserves IDs 0..255 and the actual loop flag, rejecting larger IDs and unsupported reverse flags. Register matching converted PCM labels in that order; the VGM tool does not automatically register or resample PCM.

## Format constraints and deliberate differences

- DMF revisions 11..27 have explicit import branches; captured PCE fixtures cover 13, 14, 15, 16, 19, 20, 23, 24, 25, 26 and 27. Intermediate noise-envelope fields are still consumed despite the historical lack of a version increment.
- Compressed notes are C0..B6; patterns contain 1..256 rows, orders 1..127, effect columns 1..4, and effective row speeds 1..255. Instrument/wave/sample pointer tables each support 128 entries. Unrepresentable values are rejected instead of silently truncated.
- Relative arpeggio steps fit signed bytes; fixed notes are 0..195. Internal pitch bases cover notes -60..195 using 16-bit periods. Extreme combinations outside that range or very large global detunes can differ from Furnace's wider arithmetic. Final PSG periods clamp to 1..4095.
- Waveforms must contain 32 samples. Empty tables and the historical single zero-length placeholder get Furnace's constant-15 null wave; empty instrument tables get a no-envelope instrument. Missing waveform references are rejected. Arbitrary Furnace wave lengths/synthesis are unsupported.
- Noise uses the same calculated 0..31 channel volume as waveform playback, matching the released Furnace behavior. The former `HUTRACK_OLD_NOISE_VOL` option and runtime compensation table have been removed.
- Vibrato shapes 0..11 are implemented. Shape 7 uses a deterministic small PRNG, not Furnace's host `rand()` sequence; its modulation is not trace-identical.
- PCM remains converted, five-bit, fixed-rate playback. Dynamic sample pitch and all Furnace sample features are outside this runtime. Import now applies legacy gain, pitch preprocessing, depth and cut metadata. Actual resampling and interrupt-driven playback have been exercised, but listening quality has not been assessed.
- PAL and custom-Hz modules require the application to supply the proper music tick rate. The VBlank hook does not reschedule itself; conversion warns.

## Export and integration changes

DMF, WAV and VGM assembly exports prepare all output before replacing files.
An ordinary write or installation failure restores the previous bundle,
including debug output and shared VGM waveforms. This protects against partial
exports; it is not a power-loss or concurrent-writer guarantee. DMF instrument
names are sanitized for assembly comments, so embedded line breaks cannot add
data or move instrument descriptors.

VGM PCM routing follows each `90` stream setup: the stream ID is independent
of its destination PSG channel. Starts/stops use that mapping, including IDs
above five, and `94 FF` stops active mapped streams. Only the first HuC6280,
channels 0–5 and DAC register 6 are supported. Older setup-free inputs retain
the former stream-ID-as-channel convention for IDs 0–5; after an explicit setup,
each referenced stream must have its own setup. Register converted PCM labels
in sample-ID order; this routing change does not generate the runtime catalog.
Repeated starts on the same stream/channel are supported, as used by Furnace.
The converter does not simulate natural sample completion: remapping a started
stream or reusing its channel under a different stream ID requires an explicit
VGM stop first, even after a one-shot would have ended. Unsupported overlaps
are rejected rather than silently converted into a different sound.

New exports use **banked asset format revision 1** and require this engine. A zero word and revision byte identify the header; the following address/bank points to six root descriptors. Every order list, pattern table, pattern, instrument descriptor, envelope and waveform has its own address/bank pointer. Readers normalize addresses into a two-bank window. The converter rebases each object without moving its physical output, so long songs do not wrap a 16-bit CPU address.

Old exports remain readable through the original layout and corrected mapping base. Old assets still have the addressing limits inherent in their near pointers; **reconvert large songs** to obtain the new addressing. Attributes retain the zero marker, initial arpeggio speed and legacy-volume mode, with defaults for old exports. Canonical and bundled converter support files match.

PCM has separate playback state and a full-byte bank field; crossing `$7F` to `$80` no longer stops playback. Crossing the end of bank `$FF` stops instead of wrapping to bank zero. The cartridge/platform must actually map the requested banks to sample data. Music PCM resets its control/loop state after SFX. Its historical two-byte size field is informational (low 16 bits); the stream ends at its control marker, so converted samples can exceed 64 KB.

All direct C PcmRequest overloads reject a header whose sample start would wrap
past bank FF, and a sample beginning with a marker that its selected masks would
repeat forever. These failures return 0 without replacing existing playback.
Empty one-shots remain valid and stop at their first marker. The API does not
scan or validate the complete asset; it still requires valid converter output.

The lookup data occupies 2,868 bytes outside the fixed library and music code. HuC uses its constants bank and restores the constants' normal page afterward. HuCC needs `RESERVE_BANKS >= 1` defined before startup allocates banks; the supplied `hucc-sound.inc` reserves one bank for these tables. Standalone PCEAS integration must include `HuTrack_pitch_tables.inc` at an 8 KB boundary assembled for `$8000`, as the example does. Assembly assertions guard table and music-code overflow. Tables change ROM placement, not the period-slide representation.

For standalone PCEAS, keep `HuTrack_lib.asm` and `HuTrack_parser.asm` in the
same music code bank: the loader calls the parser's banked-data helpers.
The example's main program and music bank both execute at `$C000`, so calls
between them use fixed-bank trampolines. Mapping the music bank directly from
main would replace the caller before its call instruction could execute.
The example selects SMB3 and four game music transcriptions in banked format;
the native playback test exercises each entire song and its loop. PCEAS places
its standalone SFX sample after the complete song bundle, so larger songs and
their PCM data cannot overlap a hard-coded sample bank. The dense transcriptions
still have high peak CPU costs; see the [track guide](../example/music/README.md).

Source tests, native builds, Mesen playback and benchmarks pass; physical-console listening and an exhaustive worst-case frame/IRQ budget remain unverified. Playback status, pause/resume, music fades, independent music/SFX group volumes, EE event polling and non-stealing channel reservation are documented in the [integration guide](huc/huc_hutrack_doc.html#huc_functions). The unused save/load-position and FadeToContinue placeholders were removed. Group volumes subtract attenuation from each final 5-bit channel volume with a zero clamp; they do not change the hardware master volume.

The optional assembly note constants now give F its correct semitone value, with
F-sharp available in both spellings (`F0.S` / `F0_sharp`, through octave 7).
The existing E-sharp aliases still mean F. This fixes handwritten assembly
patterns; converted DMF notes and the pitch tables are unchanged.
