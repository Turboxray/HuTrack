"""PCM command IDs/flags and configurable runtime catalog storage."""
from contextlib import redirect_stdout
import importlib.util
import io
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('vgm_converter', ROOT/'utils/PSG_SFX/VGM2SFX.py')
vgm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vgm)


class SfxPcmTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT/'tests/.tmp'
        scratch.mkdir(exist_ok=True)
        temp = tempfile.TemporaryDirectory(prefix='sfx-pcm-', dir=scratch)
        assert Path(temp.name).resolve().is_relative_to(scratch.resolve())
        self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name)

    def convert(self, sample, flags):
        header = bytearray(64)
        header[:4] = b'Vgm '
        struct.pack_into('<I', header, 8, 0x171)
        # An FB-valued period operand must remain data after the PCM command.
        stream = bytes([0x95, 0, sample & 255, sample >> 8, flags,
                        0xb9, 2, 0xfb, 0xb9, 3, 1, 0x66])
        source = self.folder/'commands.vgm'
        source.write_bytes(header + stream)
        options = SimpleNamespace(filein=str(source), destfolder=str(self.folder), dir='',
                                  sfxname='commands', chanproc=[0], disablecomment=True,
                                  debugBin=True, debugLog=False, debugConsole=False, waveformlist='')
        with redirect_stdout(io.StringIO()):
            self.assertTrue(vgm.ConvertVGM(options).process())

    def test_sample_ids_and_loop_flags_survive_both_exports(self):
        for sample in (0, 1, 7, 254, 255):
            for loop in (0, 1):
                with self.subTest(sample=sample, loop=loop):
                    self.convert(sample, loop)
                    expected = bytes([0xfc, sample, loop, 0xc1, 0xfb, 0xff, 0xfb])
                    self.assertEqual((self.folder/'commands.chan0.bin').read_bytes(), expected)
                    assembly = (self.folder/'commands.chan0.inc').read_text()
                    data = []
                    for line in assembly.splitlines():
                        if '.db ' in line:
                            data.extend(int(n, 16) for n in re.findall(r'\$([\da-fA-F]+)', line.split(';')[0]))
                    self.assertEqual(bytes(data), expected)

    def test_unrepresentable_pcm_commands_are_rejected(self):
        for sample, flags in ((256, 0), (65535, 1), (0, 2), (0, 16), (0, 17)):
            with self.subTest(sample=sample, flags=flags), self.assertRaises(ValueError):
                self.convert(sample, flags)

    def test_catalog_capacity_and_storage(self):
        assembler = os.environ.get('PCEAS') or shutil.which('pceas')
        if not assembler:
            self.skipTest('Set PCEAS to the 4.x assembler executable')
        for capacity in (0, 1, 64, 255, 256):
            source = self.folder/'capacity.asm'
            source.write_text(f'''HUSFX_PCM_SLOTS = {capacity}
HUTRACK_SFX_VOLUME = 1
 .include "HuSFX/HuSFX_vars.inc"
 .if (HuSFXEngine.VarEnd-HuSFX.pcm.count != 3*HUSFX_PCM_SLOTS+8)
 .fail Incorrect PCM catalog storage size.
 .endif
 .code
 .bank 0
 .org $8000
 .db 0
''', encoding='utf-8')
            result = subprocess.run([assembler, '-raw', str(source)], cwd=self.folder,
                                    env=dict(os.environ, PCE_INCLUDE=str(ROOT/'lib')),
                                    capture_output=True, text=True, timeout=30)
            with self.subTest(capacity=capacity):
                self.assertEqual(result.returncode == 0, 1 <= capacity <= 255,
                                 result.stdout + result.stderr)

    def test_register_only_decoder_still_builds_without_hutrack(self):
        assembler = os.environ.get('PCEAS') or shutil.which('pceas')
        if not assembler:
            self.skipTest('Set PCEAS to the 4.x assembler executable')
        decoder = (ROOT/'lib/HuSFX/HuSFX_lib.asm').read_text(encoding='utf-8')
        source = self.folder/'standalone.asm'
        source.write_text(' .include "HuSFX/HuSFX_vars.inc"\n .code\n .bank 0\n .org $8000\n'
                          + 'HuSFX.process\n' + decoder.split('\nHuSFX.process\n', 1)[1], encoding='utf-8')
        result = subprocess.run([assembler, '-raw', str(source)], cwd=self.folder,
                                env=dict(os.environ, PCE_INCLUDE=str(ROOT/'lib')),
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
