"""Regenerate the guide's original PCM illustrations with NumPy and Matplotlib.

Install those optional documentation dependencies, then run this file.
Use --preview-dir PATH to also write PNGs for visual review. Game builds and
the converters do not need these packages beyond their own requirements.

These are explanatory models, not console measurements: a uniform 32-bin
quantizer with bin-centre reconstruction, ideal playback attenuation, and no
resampling, dither, analogue filtering or hardware noise. Gain is the TOTAL
gain before quantization, including the WAV converter's built-in 1.5x.
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
BG, PANEL, TEXT, MUTED = "#11171e", "#19232d", "#e3eaf1", "#adbbc9"
GREEN, ORANGE, RED, GRID = "#89d8c3", "#ffbd69", "#ff7c85", "#354454"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 13,
    "figure.facecolor": BG, "axes.facecolor": PANEL,
    "text.color": TEXT, "axes.labelcolor": MUTED,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": GRID, "axes.titleweight": "bold",
    "axes.titlesize": 15, "axes.titlepad": 15,
    "grid.color": GRID, "grid.alpha": .6,
    "svg.hashsalt": "hutrack-pcm-gain-v1",
})


def quantize(x):
    codes = np.clip(np.floor((x + 1) * 16), 0, 31).astype(int)
    return (codes + .5) / 16 - 1, codes


def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", linewidth=.7)
    ax.tick_params(length=0, pad=7)
    ax.set_axisbelow(True)


def save(fig, name, preview_dir):
    svg_path = HERE / (name + ".svg")
    fig.savefig(svg_path, metadata={"Date": None})
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    if preview_dir:
        preview_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(preview_dir / (name + ".png"), dpi=110)
    plt.close(fig)


def levels(preview_dir):
    t = np.linspace(0, 2, 1600)
    source = .12 * np.sin(2 * np.pi * t)
    quiet, quiet_codes = quantize(source)
    gained, gained_codes = quantize(8 * source)
    assert len(np.unique(quiet_codes)) == 4
    assert len(np.unique(gained_codes)) == 32
    assert np.max(np.abs(gained / 8 - source)) <= 1 / 256 + 1e-12

    fig, axes = plt.subplots(2, 2, figsize=(11, 8.8))
    fig.subplots_adjust(left=.10, right=.97, bottom=.14, top=.80,
                        hspace=.75, wspace=.29)
    fig.text(.04, .945, "Use the sample levels; set loudness afterward", size=21, weight="bold")
    fig.text(.04, .90, "The same quiet tone, stored two ways. Both still use 5-bit PCM.", color=MUTED)
    for i, (gain, out, codes, color) in enumerate([
        (1, quiet, quiet_codes, ORANGE), (8, gained, gained_codes, GREEN)
    ]):
        ax = axes[0, i]
        for v in (np.arange(32) + .5) / 16 - 1:
            ax.axhline(v, color=GRID, lw=.45, alpha=.7)
        ax.plot(t, source * gain, color=TEXT, ls="--", lw=1.6, zorder=3)
        ax.step(t, out, where="mid", color=color, lw=2)
        ax.set_title(f"{gain}× total gain: {len(np.unique(codes))} of 32 codes used", color=color)
        ax.set_ylim(-1.08, 1.08)
        ax.set_yticks([-1, 0, 1], ["−100%", "0", "+100%"])
        ax.set_xticks([])
        ax.set_ylabel("At conversion")
        style(ax)
        ax = axes[1, i]
        ax.plot(t, source, color=TEXT, ls="--", lw=1.6, label="Desired tone", zorder=3)
        ax.step(t, out / gain, where="mid", color=color, lw=2, label="5-bit result")
        ax.set_title("Normal playback level" if gain == 1 else "Playback amplitude ÷ 8", color=color)
        ax.set_ylim(-.15, .15)
        ax.set_yticks([-.12, 0, .12], ["−12%", "0", "+12%"])
        ax.set_xticks([0, 1, 2])
        ax.set_xlabel("Time (tone cycles)")
        ax.set_ylabel("At playback")
        style(ax)
    fig.text(.04, .035, "Dashed: desired waveform. Solid: quantized result. Ideal model; ÷8 is not a PSG register value.",
             color=MUTED, size=12)
    save(fig, "pcm_gain_levels", preview_dir)


def quiet_tail(preview_dir):
    t = np.linspace(0, 1, 500)
    envelope = .12 * np.exp(-4 * t)
    db = 20 * np.log10(envelope)
    ordinary_bound = 20 * np.log10(1 / 32)
    gained_bound = 20 * np.log10(1 / 256)
    assert np.isclose(ordinary_bound - gained_bound, 20 * np.log10(8))
    fig, ax = plt.subplots(figsize=(11, 6.2))
    fig.subplots_adjust(left=.10, right=.96, bottom=.19, top=.72)
    fig.text(.04, .935, "Quiet tails expose coarse quantization", size=21, weight="bold")
    fig.text(.04, .877, "One fading sound at the same intended playback level in both cases.", color=MUTED)
    ax.plot(t, db, color=TEXT, lw=3)
    ax.axhline(ordinary_bound, color=ORANGE, ls="--", lw=2)
    ax.axhline(gained_bound, color=GREEN, ls="--", lw=2)
    ax.text(.02, ordinary_bound + 1.3, "Error bound: no pre-gain", color=ORANGE, size=12)
    ax.text(.02, gained_bound + 1.3, "Error bound: 8× gain, then playback ÷ 8", color=GREEN, size=12)
    ax.text(.66, -36, "Sound's fading envelope", color=TEXT, size=12)
    ax.set_ylim(-59, -14)
    ax.set_xlim(0, 1)
    ax.set_yticks([-20, -30, -40, -50])
    ax.set_ylabel("Playback level (dB relative to full scale)")
    ax.set_xticks([0, .5, 1], ["Start / louder", "Time →", "End / quieter"])
    ax.get_xticklabels()[0].set_horizontalalignment("left")
    ax.get_xticklabels()[-1].set_horizontalalignment("right")
    style(ax)
    fig.text(.04, .085, "Dashed lines: maximum rounding error in this ideal model, not measured noise or hearing thresholds.",
             size=12, color=MUTED)
    fig.text(.04, .04, "Less sound to mask the error → more exposed grain or buzz. Pre-gain lowers the playback error bound.",
             size=12, color=MUTED)
    save(fig, "pcm_gain_quiet_tail", preview_dir)


def clipping(preview_dir):
    t = np.linspace(0, 1, 3000)
    body = .19 * np.sin(2 * np.pi * 12 * t) * np.exp(-.75 * t)
    source = body + .85 * np.exp(-((t - .19) / .012) ** 2)
    source *= .92 / np.max(np.abs(source))
    fig, axes = plt.subplots(3, 1, figsize=(11, 9.2))
    fig.subplots_adjust(left=.10, right=.96, bottom=.10, top=.82, hspace=.73)
    fig.text(.04, .945, "Clipping: spend a few peaks to preserve more body", size=20, weight="bold")
    fig.text(.04, .895, "The dashed outline is the boosted signal; the solid line is what survives clipping.", color=MUTED)
    for ax, gain, color, title in zip(axes, [1, 1.6, 8], [MUTED, GREEN, RED], [
        "Peak kept intact; much of the body stays small",
        "Brief peak clipped; more range available to the body",
        "Many cycles flattened; the sound changes substantially",
    ]):
        amplified = gain * source
        clipped = np.clip(amplified, -1, 1)
        mask = np.abs(amplified) > 1
        fraction = np.mean(mask)
        if gain == 1:
            assert fraction == 0
        elif gain == 1.6:
            assert 0 < fraction < .05
        else:
            assert fraction > .1
        ax.plot(t, amplified, color=MUTED, ls="--", lw=1.1)
        ax.plot(t, clipped, color=color, lw=2.2)
        ax.fill_between(t, -1, 1, where=mask, color=RED, alpha=.22)
        for y in (-1, 1):
            ax.axhline(y, color=ORANGE, ls=":", lw=1.4)
        ax.set_title(f"{gain:g}× total gain · {title}", loc="left", fontsize=13, color=color)
        ax.set_xlim(0, 1)
        ax.set_ylim(-1.65, 1.65)
        ax.set_yticks([-1, 0, 1], ["−100%", "0", "+100%"])
        ax.set_ylabel("At conversion", fontsize=11)
        ax.set_xticks([])
        style(ax)
    axes[-1].set_xticks([0, .5, 1], ["Start", "Time →", "End"])
    fig.text(.04, .025, "Red shading: clipped intervals. Compare by ear after lowering playback volume to match the body.",
             size=12, color=MUTED)
    save(fig, "pcm_gain_clipping", preview_dir)


def envelope(preview_dir):
    levels = [12, 20, 27, 31, 27, 23, 19, 15, 11, 7, 3, 0]
    durations = [6, 6, 6, 36, 12, 12, 12, 12, 12, 12, 12, 6]
    assert sum(durations) == 144
    edges = np.r_[0, np.cumsum(durations)] / 60
    fig, ax = plt.subplots(figsize=(11, 5.3))
    fig.subplots_adjust(left=.13, right=.96, bottom=.22, top=.72)
    fig.text(.04, .935, "One PCM playback, shaped by volume commands", size=20, weight="bold")
    fig.text(.04, .86, "Start once → quiet attack → full-volume hold → stepped fade → stop", color=MUTED)
    ax.stairs(levels, edges, baseline=None, color=GREEN, lw=3)
    ax.axvspan(0, .3, color=GREEN, alpha=.07)
    ax.axvspan(.3, .9, color=GREEN, alpha=.16)
    ax.axvspan(.9, 2.4, color=ORANGE, alpha=.07)
    ax.set_ylim(-1, 35)
    ax.set_xlim(0, 2.4)
    ax.set_yticks([0, 12, 20, 31], ["0 · silent", "12", "20", "31 · full"])
    ax.set_xticks([0, .3, .9, 1.5, 2.4])
    ax.set_xlabel("Seconds (60 HuSFX updates per second)")
    style(ax)
    fig.text(.04, .055, "Logarithmic hardware settings, not amplitude percentages. PCM keeps advancing even at volume zero.",
             size=12, color=MUTED)
    save(fig, "pcm_volume_envelope", preview_dir)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()
    levels(args.preview_dir)
    quiet_tail(args.preview_dir)
    clipping(args.preview_dir)
    envelope(args.preview_dir)


if __name__ == "__main__":
    main()
