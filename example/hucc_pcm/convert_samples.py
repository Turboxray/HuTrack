"""Rebuild the six PCM assets using the repository's current WAV converter."""
from pathlib import Path
import subprocess
import sys


def main():
    folder = Path(__file__).resolve().parent
    converter = folder.parents[1] / 'utils/PCM_SFX/waveConvert.py'
    for name in ('emergency', 'explosion2', 'hypercocoon', 'lightning',
                 'stageclear', 'ShubibinmanIIIb'):
        subprocess.run([
            sys.executable, str(converter), '--noGui',
            '--filein', str(folder / 'wav' / (name + '.wav')),
            '--destinationPath', str(folder / 'assets/pcm'),
            '--includePath', '../assets/pcm',
            '--playback', '6960', '--resampleFilter', 'kaiser_best',
            '--bitDepth', '5bit',
        ], check=True)


if __name__ == '__main__':
    main()
