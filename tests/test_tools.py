"""Converter regressions. Run: python -m unittest discover -s tests -v"""
from contextlib import redirect_stdout
import importlib.util
import io
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'utils'))
from support.dmfReader import ConvertDeflemask
from support.hutrackLib import HuTrackExportPCE

spec = importlib.util.spec_from_file_location('wave_converter', ROOT / 'utils/PCM_SFX/waveConvert.py')
pcm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pcm)


def module_bytes(title=b'', author=b'', noise=()):
    """One standard instrument, wave and eight empty rows in legacy DMF 24."""
    def macro(values):
        return bytes([len(values)]) + b''.join(struct.pack('<I', n) for n in values) + (b'\xff' if values else b'')
    header = b'.DelekDefleMask.' + bytes([24, 5, len(title)]) + title + bytes([len(author)]) + author
    header += bytes([4, 16, 0, 6, 6, 1, 0]) + b'060' + struct.pack('<I', 8) + bytes([1]) + bytes(6)
    instrument = bytes([1, 0, 0]) + macro([31]) + macro([]) + bytes([0]) + macro(noise) + macro([0])
    waves = bytes([1]) + struct.pack('<I', 32) + struct.pack('<32I', *range(32))
    row = struct.pack('<6H', 0, 0, 65535, 65535, 65535, 65535)
    return header + instrument + waves + (bytes([1]) + row * 8) * 6 + bytes([0])


def wave_bytes(samples, width=1):
    def chunk(name, value):
        return name + struct.pack('<I', len(value)) + value + (b'\0' if len(value) & 1 else b'')
    body = b'WAVE' + chunk(b'JUNK', b'abc')
    body += chunk(b'fmt ', struct.pack('<HHIIHH', 1, 1, 11025, 11025 * width, width, width * 8))
    body += chunk(b'data', samples) + chunk(b'LIST', b'not sample data')
    return b'RIFF' + struct.pack('<I', len(body)) + body


class ConverterTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / 'tests/.tmp'
        scratch.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='hutrack-test-', dir=scratch)
        assert Path(self.temp.name).resolve().is_relative_to(scratch.resolve())
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.params = dict(songName='song', subFolder='song', destinationPath=str(self.folder),
                           includePath='', debug=False, no_songname=False, no_author=False,
                           playback='6960', resampleFilter='kaiser_best')

    def decode(self, raw):
        reader = ConvertDeflemask(self.params)
        reader.dmf.setDMF(raw)
        with redirect_stdout(io.StringIO()):
            reader.decodeDMF()
        return reader

    def test_every_truncation_is_rejected(self):
        raw = module_bytes(noise=(3, 2, 1))
        self.assertEqual(self.decode(raw).dmf.index, len(raw))
        for length in range(len(raw)):
            with self.subTest(length=length), self.assertRaises(ValueError):
                self.decode(raw[:length])

    def test_intermediate_noise_envelope_keeps_following_fields_aligned(self):
        for noise in ((), (7,), (3, 2, 1)):
            reader = self.decode(module_bytes(noise=noise))
            instrument = reader.huTrack.instrumentData[0]
            self.assertEqual(instrument.noiseEnv, list(noise))
            self.assertEqual(instrument.wavetableEnv, [0])
            self.assertEqual(reader.huTrack.wavetableData, [list(range(32))])

    def test_failed_reload_clears_previous_song(self):
        path = self.folder / 'valid.dmf'
        path.write_bytes(zlib.compress(module_bytes()))
        reader = ConvertDeflemask(dict(self.params, filein=str(path)))
        with redirect_stdout(io.StringIO()):
            self.assertTrue(reader.process()[0])
            reader.params['filein'] = str(self.folder / 'missing.dmf')
            success, song = reader.process()
        self.assertFalse(success)
        self.assertIsNone(song)
        self.assertIsNone(reader.huTrack)

    def test_metadata_limits_and_embedded_zero(self):
        import re
        for size in (0, 1, 47, 48, 255):
            for suffix in (b'', b'\0discarded'):
                title = b'T' * min(size, 245) + suffix if suffix else b'T' * size
                song = self.decode(module_bytes(title, b'A' * size)).huTrack
                with redirect_stdout(io.StringIO()):
                    HuTrackExportPCE(song, self.params).process()
                header = (self.folder / 'song/song.header.inc').read_text()
                # Read all .db lines in each metadata field, including wrapped lines.
                fields = re.findall(r'^\.(?:songname|author)\n((?:  \.db [^\n]+\n)+)', header, re.M)
                self.assertEqual(len(fields), 2, header)
                for field, char, length in zip(fields, (ord('T'), ord('A')), (len(title.split(b'\0')[0]), size)):
                    values = [int(n) for n in re.findall(r'\d+', field)]
                    self.assertEqual(values, [char] * min(47, length) + [0])

    def test_export_rejects_invalid_names_before_writing(self):
        song = self.decode(module_bytes()).huTrack
        for name in ('', '.', '..', '../bad', 'dir\\bad', 'bad"name', 'bad\nname'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                HuTrackExportPCE(song, dict(self.params, songName=name)).process()
        self.assertEqual(list(self.folder.iterdir()), [])

    def test_riff_chunks_are_not_audio(self):
        for width, raw, expected in ((1, b'\0\x80\xff', [0, 128, 255]),
                                     (2, b'\0\0\xff\x7f\0\x80', [0, 32767, 32768])):
            path = self.folder / 'sample.wav'
            path.write_bytes(wave_bytes(raw, width))
            ok, message, header, samples = pcm.WavRead(path).readFile()
            self.assertTrue(ok, message)
            self.assertEqual(samples, expected)
            self.assertEqual(header['BitsPerSample'], width * 8)

    def test_incomplete_16bit_frame_is_rejected(self):
        path = self.folder / 'odd.wav'
        path.write_bytes(wave_bytes(b'\0\0\xff', 2))
        self.assertFalse(pcm.WavRead(path).readFile()[0])

    def test_pcm_writer_keeps_large_sample_and_terminator(self):
        import re
        values = list(range(32)) * 2200 + [128]
        pcm.writePCM(self.folder, 'long', '', values)
        output = (self.folder / 'long.data.inc').read_text()
        self.assertEqual([int(n, 16) for n in re.findall(r'\$([0-9a-f]{2})', output)], values)
        self.assertGreater(output.count('.page 2'), 16)

    def test_generated_songs_assemble_at_bank_boundary(self):
        assembler = os.environ.get('PCEAS') or shutil.which('pceas')
        if not assembler:
            self.skipTest('Set PCEAS to the 4.x assembler executable for ROM layout checks')
        song = self.decode(module_bytes(b'T' * 47, b'A' * 47)).huTrack
        # Both accepted formats, including a header crossing an 8 KB bank.
        for legacy in (False, True):
            for origin in (0x4000, 0x5ffd):
                with self.subTest(legacy=legacy, origin=origin), redirect_stdout(io.StringIO()):
                    HuTrackExportPCE(song, dict(self.params, legacy_format=legacy)).process()
                    source = self.folder / 'layout.asm'
                    source.write_text(f' .bank 0\n .org ${origin:04x}\nSong:\n .include "song/song.song.inc"\n', encoding='utf-8')
                    result = subprocess.run([assembler, '-raw', str(source)], cwd=self.folder,
                                            env=dict(os.environ, PCE_INCLUDE=str(self.folder)),
                                            capture_output=True, text=True, timeout=30)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertTrue(source.with_suffix('.pce').exists())

    def test_cli_export_errors_are_actionable(self):
        wav = self.folder / 'sample.wav'
        wav.write_bytes(wave_bytes(b'\0\x80\xff'))
        dmf = self.folder / 'song.dmf'
        dmf.write_bytes(zlib.compress(module_bytes()))
        for script, args in (
            ('utils/PCM_SFX/waveConvert.py', ['--noGui', '--filein', str(wav), '--playback', 'no_resample', '--overridename', '../bad']),
            ('utils/HuTrackConverter.py', ['--no_gui', '--filein', str(dmf), '--songname', 'bad"name']),
            ('example/pceas/assets/HuTrackConverter.py', ['--no_gui', '--filein', str(dmf), '--songname', 'bad"name']),
        ):
            with self.subTest(script=script):
                result = subprocess.run([sys.executable, str(ROOT/script), *args, '--destinationPath', str(self.folder/'output')],
                                        capture_output=True, text=True, timeout=45)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('Traceback', result.stderr)
                self.assertIn('Error:', result.stderr)


if __name__ == '__main__':
    unittest.main()
