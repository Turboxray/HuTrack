"""Convert the four supplied legacy DMFs for the HuC, HuCC and PCEAS examples.

Preserves source edits made in Furnace. Requires the repository requirements.txt.
SMB3 retains its existing converted bundle; no original ROMs or audit files are
needed to regenerate the other songs.
"""
from pathlib import Path
import argparse
import contextlib
import io
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'utils'))
from support.dmfReader import ConvertDeflemask
from support.hutrackLib import HuTrackExportPCE

SONGS = (
    'air_zonk_aqua_base',
    'legendary_axe_level_2',
    'aero_blasters_seaside_front',
    'bonks_adventure_round_1',
)


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    for slug in SONGS:
        path = HERE / 'source' / (slug + '.dmf')
        params = dict(filein=str(path), songName=slug, subFolder='song/' + slug,
                      destinationPath=str(ROOT / 'example/huc/assets'),
                      includePath='../assets', debug=False,
                      no_songname=False, no_author=False,
                      playback='6960', resampleFilter='kaiser_best')
        with contextlib.redirect_stdout(io.StringIO()) as log:
            reader = ConvertDeflemask(params)
            ok, song = reader.process()
            if not ok or reader.warnings:
                raise ValueError(f'{path.name}: {reader.warnings}\n{log.getvalue()}')
            for compiler in ('huc', 'hucc', 'pceas'):
                target = dict(params, destinationPath=str(ROOT / 'example' / compiler / 'assets'))
                HuTrackExportPCE(song, target).process()
        print(f'{slug}: updated HuC, HuCC and PCEAS assets/song folders')


if __name__ == '__main__':
    main()
