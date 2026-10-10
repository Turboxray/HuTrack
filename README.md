# HuTrack

HuTrack is a library and convertor for playing legacy DefleMask DMF files in HuC and PCEAS projects. The engine is lightweight and compact, and is intended to be inserted into game projects. Songs can be edited in Furnace and exported as supported legacy DMF files. The converters require Python 3.12 or newer with Tkinter. Install their tested Python dependencies from the repository root with `python -m pip install -r requirements.txt`.

The compatibility reference for current development is **official Furnace 0.6.8.3's legacy-DMF playback**. The chosen design retains HuTrack's fast note, vibrato and fine-tune approximations while keeping period-based slides. See [Legacy DMF compatibility](docs/compatibility.md) for the pinned reference and implementation status, including the new banked asset format and long-song/shared-waveform support.

# Usage

Open the [HuC 4.x and HuCC integration guide](docs/huc/huc_hutrack_doc.html) in a browser. It covers Furnace export, DMF conversion, separate compiler setup files and build commands, ROM/RAM placement, music playback, PCM and HuSFX ownership. The [complete API reference](docs/huc/huc_hutrack_doc.html#api-reference) lists every HuTrack C call and overload, with separate HuSFX and assembly references. The guide and its screenshots work offline from a checkout.

Use the setup for your compiler: HuC installs the assembly through `libslot1.asm`, while HuCC uses `hucc-final-extra.asm` and a separate reserved bank for lookup data. Including `HuTrack.c` alone does not install the engine.

The example build scripts use the installed 4.x toolchain at `C:\huc` by default. Set `HUC_HOME` for HuC/PCEAS or `HUCC_HOME` for HuCC to select another installation. Run the scripts from a terminal; they print build logs and return a nonzero exit code on failure.

The HuC, HuCC and PCEAS music examples include SMB3 plus [Air Zonk, The Legendary Axe, Aero Blasters and Bonk's Adventure](example/music/README.md), with editable legacy DMFs and ready-to-build converted assets. The track guide explains selection controls, conversion differences, performance limits and how to reconvert edits made in Furnace.

Channel handoff for SFX uses explicit reserve/release calls. After release, music waits silently for a fresh note and then restores the channel state. See [SFX ownership and the FX support matrix](docs/compatibility.md).

Music and SFX have independent volume controls. Music fades subtract attenuation from the final channel volumes, leaving SFX and hardware master volume unchanged. The API also provides playback status, pause/resume, EE event polling and `TryReserve()` for acquiring a free SFX channel.

For WAV sound effects, the [HuCC PCM example](example/hucc_pcm/README.md) includes six samples, conversion and build scripts, and a menu for selecting, playing and stopping them through HuTrack's PCM API.

The [illustrated WAV-to-PCM walkthrough](docs/huc/huc_hutrack_doc.html#pcm) covers the standalone converter app, supported WAV formats, every setting, saving the generated files and playback from C. Its [five-bit quality guide](docs/huc/huc_hutrack_doc.html#pcm-gain-staging) explains pre-gain, intentional peak clipping, noise in quiet passages, and hardware-volume compensation with comparison graphs. This workflow does not require a DMF song or Furnace.

The runtime PCM sample-ID demos are complete [HuC](example/huc_pcm_sample_ids/README.md) and [HuCC](example/hucc_pcm_sample_ids/README.md) projects, each with source, assets, compiler setup and a build script. They register three sample labels, play their IDs in one HuSFX sequence, demonstrate PCM followed by waveform playback, and shape one continuous PCM playback with a volume envelope.

Run `python -m unittest discover -s tests -v` for converter and documentation regressions. The [testing instructions](tests/README.md) also cover generated-asset assembly and native HuC/HuCC playback checks in Mesen.
