# HuTrack

HuTrack is a library and convertor for playing legacy DefleMask DMF files in HuC and PCEAS projects. The engine is lightweight and compact, and is intended to be inserted into game projects. Songs can be edited in Furnace and exported as supported legacy DMF files. HuTrack also requires that you install python and additional packages.

The compatibility reference for current development is **official Furnace 0.6.8.3's legacy-DMF playback**. The chosen design retains HuTrack's fast note, vibrato and fine-tune approximations while keeping period-based slides. See [Legacy DMF compatibility](docs/compatibility.md) for the pinned reference and implementation status, including the new banked asset format and long-song/shared-waveform support.

# Usage

Open the [HuC 4.x and HuCC integration guide](docs/huc/huc_hutrack_doc.html) in a browser. It covers Furnace export, DMF conversion, separate compiler setup files and build commands, ROM/RAM placement, music playback, PCM and HuSFX ownership. The guide and its screenshots work offline from a checkout.

Use the setup for your compiler: HuC installs the assembly through `libslot1.asm`, while HuCC uses `hucc-final-extra.asm` and a separate reserved bank for lookup data. Including `HuTrack.c` alone does not install the engine.

Channel handoff for SFX uses explicit reserve/release calls. After release, music waits silently for a fresh note and then restores the channel state. See [SFX ownership and the FX support matrix](docs/compatibility.md).

For WAV sound effects, the [HuCC PCM example](example/hucc_pcm/README.md) includes six samples, conversion and build scripts, and a menu for selecting, playing and stopping them through HuTrack's PCM API.
