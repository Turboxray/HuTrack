"""Assemble public note symbols, including spellings used by handwritten patterns."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AssemblyTests(unittest.TestCase):
    def test_chromatic_note_constants(self):
        assembler = os.environ.get('PCEAS') or shutil.which('pceas')
        if not assembler:
            self.skipTest('Set PCEAS to the 4.x assembler executable for symbol checks')
        scratch = ROOT/'tests/.tmp'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='notes-', dir=scratch) as tmp:
            folder = Path(tmp)
            assert folder.resolve().is_relative_to(scratch.resolve())
            source = ' .include "HuTrack/HuTrack_equ.inc"\n .bank 0\n .org $8000\n'
            expected = []
            for octave in range(8):
                for normal, sharp in (('.', '.S'), ('_', '_sharp')):
                    notes = [f'{letter}{octave}{sharp if is_sharp else normal}'
                             for letter, is_sharp in (('C',False),('C',True),('D',False),('D',True),
                                                      ('E',False),('F',False),('F',True),('G',False),
                                                      ('G',True),('A',False),('A',True),('B',False))]
                    source += ' .db ' + ','.join(notes + [f'E{octave}{sharp}']) + '\n'
                    expected.extend(range(octave*12, octave*12+12))
                    expected.append(octave*12+5)  # E sharp is another name for F.
            path = folder/'notes.asm'
            path.write_text(source, encoding='utf-8')
            result = subprocess.run([assembler, '-raw', str(path)], cwd=folder,
                                    env=dict(os.environ, PCE_INCLUDE=str(ROOT/'lib')),
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(path.with_suffix('.pce').read_bytes()[:len(expected)], bytes(expected))


if __name__ == '__main__':
    unittest.main()
