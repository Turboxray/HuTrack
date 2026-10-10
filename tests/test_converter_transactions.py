"""Bundle rollback, DMF comment safety, and Furnace VGM stream routing."""
from contextlib import redirect_stdout
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
from unittest.mock import patch
import zlib

from test_tools import ROOT, module_bytes, pcm
from test_sfx_pcm import vgm
from support.dmfReader import ConvertDeflemask
from support.hutrackLib import HuTrackExportPCE
from support.outputBundle import OutputBundle


def vgm_bytes(commands):
    header = bytearray(64)
    header[:4] = b'Vgm '
    struct.pack_into('<I', header, 8, 0x171)
    struct.pack_into('<I', header, 4, 64 + len(commands) - 4)
    return header + bytes(commands)


def dmf_pcm_bytes(value, **song_fields):
    """Legal DMF24 module containing a named 16-bit sample at 32 kHz."""
    name = b'fixture sample'
    sample = struct.pack('<I', 64) + bytes([len(name)]) + name
    sample += bytes([5, 5, 50, 16]) + struct.pack('<64h', *([value] * 64))
    return module_bytes(**song_fields)[:-1] + bytes([1]) + sample


class ConverterRegressionTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / 'tests/.tmp/blue_converters'
        scratch.mkdir(parents=True, exist_ok=True)
        temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name)
        self.params = dict(songName='song', subFolder='song', destinationPath=str(self.folder),
                           includePath='', debug=False, no_songname=False, no_author=False,
                           playback='6960', resampleFilter='kaiser_best')

    def decode(self, raw):
        reader = ConvertDeflemask(self.params)
        reader.dmf.setDMF(raw)
        with redirect_stdout(io.StringIO()):
            reader.decodeDMF()
        return reader.huTrack

    def options(self, source, folder, **changes):
        values = dict(filein=str(source), destfolder=str(folder), dir='', sfxname='effect',
                      chanproc=list(range(6)), disablecomment=True, debugBin=True,
                      debugLog=True, debugConsole=False, waveformlist='')
        return SimpleNamespace(**dict(values, **changes))

    @staticmethod
    def snapshot(folder):
        return {str(path.relative_to(folder)): path.read_bytes()
                for path in folder.rglob('*') if path.is_file()}

    def prepare_export(self, converter):
        output = self.folder / converter
        output.mkdir()
        if converter == 'dmf':
            sources = []
            for index, value in enumerate((-10000, 10000)):
                source = self.folder / f'pcm-{index}.dmf'
                raw = dmf_pcm_bytes(value, title=(b'old title', b'new title')[index])
                source.write_bytes(zlib.compress(raw))
                sources.append(source)

            def export(index):
                params = dict(self.params, destinationPath=str(output), debug=True,
                              filein=str(sources[index]))
                success, song = ConvertDeflemask(params).process()
                self.assertTrue(success)
                self.assertEqual(song.samples[0].sampleName, 'fixture sample')
                self.assertEqual(song.samples[0].sampleSize, 64)
                HuTrackExportPCE(song, params).process()
            failure_name = 'song.debug.bin'
        elif converter == 'wav':
            def export(index):
                pcm.writePCM(output, 'sample', ('old/path', 'new/path')[index],
                             ([15, 128], [0, 31, 128])[index], ([128], [0, 255])[index])
            failure_name = 'sample.debug.5bit.bin'
        else:
            source = self.folder / 'source.vgm'
            source.write_bytes(vgm_bytes([0xb9, 4, 0x80, 0x66]))
            pool = output / 'shared.wf.inc'
            pool.write_text('.wf.block0\n .db ' + ','.join('$00' for _ in range(32)) + '\n')
            options = self.options(source, output, waveformlist=str(pool))

            def export(index):
                # Feed a different valid pool on re-export so rollback must
                # restore the externally shared waveform file, too.
                vgm.ConvertVGM(options).process([[index] * 32])
            failure_name = 'effect.debugLog.txt'
        with redirect_stdout(io.StringIO()):
            export(0)
        if converter == 'dmf':
            self.assertTrue((output / 'song/song.0.8bit.bin').is_file())
        return output, export, failure_name

    def test_debug_dmf_import_is_read_only_even_when_later_validation_fails(self):
        output = self.folder / 'uncreated-output'
        source = self.folder / 'pcm.dmf'
        source.write_bytes(zlib.compress(dmf_pcm_bytes(10000)))
        params = dict(self.params, destinationPath=str(output), debug=True, filein=str(source))
        with redirect_stdout(io.StringIO()):
            success, song = ConvertDeflemask(params).process()
        self.assertTrue(success)
        self.assertTrue(song.samples[0].sample8bit)
        self.assertFalse(output.exists())
        with self.assertRaises(ValueError):
            HuTrackExportPCE(song, dict(params, songName='bad/name')).process()
        self.assertFalse(output.exists())
        # A second sample fails validation after the first has been converted.
        raw = dmf_pcm_bytes(-10000)
        raw = raw[:len(module_bytes()) - 1] + bytes([2]) + raw[len(module_bytes()):]
        source.write_bytes(zlib.compress(raw))
        with redirect_stdout(io.StringIO()):
            success, song = ConvertDeflemask(params).process()
        self.assertFalse(success)
        self.assertIsNone(song)
        self.assertFalse(output.exists())

    def test_all_converters_restore_existing_bundle_on_stage_or_late_install_failure(self):
        for converter in ('dmf', 'wav', 'vgm'):
            output, export, failure_name = self.prepare_export(converter)
            before = self.snapshot(output)
            for failure in ('stage', 'install'):
                with self.subTest(converter=converter, failure=failure):
                    calls = []
                    if failure == 'stage':
                        real_open = Path.open

                        def fail_stage(path, *args, **kwargs):
                            if path.name.startswith('.hutrack-stage-') and path.name.endswith(failure_name):
                                calls.append(path)
                                raise PermissionError('injected staging write failure')
                            return real_open(path, *args, **kwargs)
                        fault = patch.object(Path, 'open', fail_stage)
                    else:
                        real_replace = os.replace

                        def fail_install(source, target):
                            if Path(source).name.startswith('.hutrack-stage-'):
                                calls.append(Path(target))
                                if Path(target).name == failure_name:
                                    raise PermissionError('injected late install failure')
                            return real_replace(source, target)
                        fault = patch('support.outputBundle.os.replace', fail_install)
                    with fault, redirect_stdout(io.StringIO()), self.assertRaises(PermissionError):
                        export(1)
                    self.assertTrue(calls, 'Failure injection must actually execute')
                    if failure == 'install':
                        self.assertGreater(len(calls), 2, 'Failure must occur after earlier installs')
                    self.assertEqual(self.snapshot(output), before)
            with redirect_stdout(io.StringIO()):
                export(1)
            self.assertNotEqual(self.snapshot(output), before)

    def test_failed_first_export_removes_new_files_and_staging_directories(self):
        output = self.folder / 'new' / 'nested'
        real_replace = os.replace

        def fail_second(source, target):
            if Path(target).name == 'sample.data.inc':
                raise PermissionError('injected install failure')
            return real_replace(source, target)
        with patch('support.outputBundle.os.replace', fail_second), self.assertRaises(PermissionError):
            pcm.writePCM(output, 'sample', '', [0, 128])
        self.assertFalse((self.folder / 'new').exists())

    @unittest.skipUnless(os.name == 'nt', 'Windows destination sharing-lock regression')
    def test_windows_locked_destination_rolls_back_real_late_install_failure(self):
        # Permit the backup read, but deny replacement of the final output.
        # Earlier files really install before Windows raises PermissionError.
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.CreateFileW.argtypes = (wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                                      wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD,
                                      wintypes.HANDLE)
        kernel.CreateFileW.restype = wintypes.HANDLE
        kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
        kernel.CloseHandle.restype = wintypes.BOOL
        for converter in ('dmf', 'wav', 'vgm'):
            with self.subTest(converter=converter):
                output, export, failure_name = self.prepare_export(converter)
                before = self.snapshot(output)
                target = next(output.rglob(failure_name))
                handle = kernel.CreateFileW(str(target), 0x80000000, 1, None, 3, 0x80, None)
                if handle == ctypes.c_void_p(-1).value:
                    raise ctypes.WinError(ctypes.get_last_error())
                try:
                    with redirect_stdout(io.StringIO()), self.assertRaises(PermissionError):
                        export(1)
                finally:
                    kernel.CloseHandle(handle)
                self.assertEqual(self.snapshot(output), before)

    def test_invalid_vgm_destination_preserves_shared_pool_and_existing_files(self):
        output, export, _ = self.prepare_export('vgm')
        before = self.snapshot(output)
        options = self.options(self.folder / 'source.vgm', output, sfxname='missing/subpath',
                               waveformlist=str(output / 'shared.wf.inc'))
        with self.assertRaises(ValueError):
            vgm.ConvertVGM(options).process([[1] * 32])
        self.assertEqual(self.snapshot(output), before)
        # An actual invalid filesystem destination also fails before any file
        # is installed, including the shared pool generated earlier.
        channel = output / 'effect.chan0.inc'
        channel.unlink()
        channel.mkdir()
        before = self.snapshot(output)
        with redirect_stdout(io.StringIO()), self.assertRaises(ValueError):
            export(1)
        self.assertEqual(self.snapshot(output), before)
        self.assertTrue(channel.is_dir())

    def test_output_aliases_are_rejected_before_writing(self):
        outputs = OutputBundle()
        path = self.folder / 'same.inc'
        with outputs.open(path) as output:
            output.write('first')
        with self.assertRaises(ValueError):
            with outputs.open(path.parent / '.' / path.name) as output:
                output.write('second')
        self.assertFalse(path.exists())

    def test_length_prefixed_instrument_name_cannot_inject_assembly(self):
        raw = module_bytes()
        # DMF24 header, six order cells, instrument count, then name length.
        offset = 16 + 2 + 2 + 10 + 4 + 1 + 6 + 1
        self.assertEqual(raw[offset], 0)
        name = b'first\r\n .db $aa\n .db $bb\r .db $cc\x00\x1a'
        named = raw[:offset] + bytes([len(name)]) + name + raw[offset + 1:]
        song = self.decode(named)
        self.assertEqual(song.instrumentData[0].name.encode('latin-1'), name)
        HuTrackExportPCE(song, self.params).process()
        instrument = (self.folder / 'song/song.instrData.inc').read_text()
        self.assertIn('; name first   .db $aa  .db $bb  .db $cc', instrument)
        self.assertNotRegex(instrument, r'(?m)^\s*\.db \$(?:aa|bb|cc)\b')

        assembler = os.environ.get('PCEAS') or shutil.which('pceas')
        if not assembler:
            self.skipTest('Set PCEAS to the 4.x assembler executable for pointer checks')
        source = self.folder / 'layout.asm'
        source.write_text(' .bank 0\n .org $4000\nSong:\n .include "song/song.song.inc"\n'
                          ' .if .instrument.0 != .instrument.0.table\n'
                          ' .fail Instrument label must point to its descriptor.\n .endif\n')

        def assemble():
            result = subprocess.run([assembler, '-raw', str(source)], cwd=self.folder,
                                    env=dict(os.environ, PCE_INCLUDE=str(self.folder)),
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return source.with_suffix('.pce').read_bytes()
        for legacy in (False, True):
            with self.subTest(legacy=legacy):
                params = dict(self.params, legacy_format=legacy)
                HuTrackExportPCE(song, params).process()
                named_binary = assemble()
                HuTrackExportPCE(self.decode(raw), params).process()
                self.assertEqual(named_binary, assemble())

    def convert_stream(self, commands, **changes):
        source = self.folder / 'streams.vgm'
        source.write_bytes(vgm_bytes(commands))
        output = self.folder / 'streams'
        with redirect_stdout(io.StringIO()):
            self.assertTrue(vgm.ConvertVGM(self.options(source, output, **changes)).process())
        channels = {}
        for ch in range(6):
            channels[ch] = (output / f'effect.chan{ch}.bin').read_bytes()
            assembly = (output / f'effect.chan{ch}.inc').read_text()
            assembled = bytes(int(n, 16) for line in assembly.splitlines() if '.db ' in line
                              for n in re.findall(r'\$([\da-fA-F]+)', line.split(';')[0]))
            self.assertEqual(channels[ch], assembled)
        return channels

    def test_furnace_stream_setup_routes_pcm_start_and_stop(self):
        # Furnace v0.6.8.3 PCE setup: chip 27, channel in the port byte, DAC 6.
        # https://github.com/tildearrow/furnace/blob/v0.6.8.3/src/engine/vgmOps.cpp#L2532-L2549
        for stream in (0, 7, 254):
            with self.subTest(stream=stream):
                channels = self.convert_stream([
                    0x67, 0x66, 5, 1, 0, 0, 0, 16,
                    0x90, stream, 0x1b, 5, 6,
                    0x91, stream, 5, 1, 0,
                    0x92, stream, 0x30, 0x1b, 0, 0,
                    0x95, stream, 0, 0, 1, 0x62,
                    0x94, stream, 0x66])
                self.assertEqual(channels[5], bytes([0xfc, 0, 1, 0xff, 0xfd, 0xff, 0xfb]))
                for channel in range(5):
                    self.assertNotIn(0xfc, channels[channel])
                    self.assertNotIn(0xfd, channels[channel])

    def test_stop_all_routes_to_each_active_mapped_channel(self):
        channels = self.convert_stream([
            0x90, 7, 0x1b, 2, 6, 0x90, 254, 0x1b, 5, 6,
            0x95, 7, 1, 0, 1, 0x95, 254, 2, 0, 1, 0x62,
            0x94, 255, 0x66])
        for channel, sample in ((2, 1), (5, 2)):
            self.assertEqual(channels[channel], bytes([0xfc, sample, 1, 0xff, 0xfd, 0xff, 0xfb]))
        self.assertNotIn(0xfd, channels[0])

    def test_stopping_inactive_alias_does_not_stop_channel_owner(self):
        channels = self.convert_stream([
            0x90, 0, 0x1b, 5, 6, 0x90, 1, 0x1b, 5, 6,
            0x95, 0, 0, 0, 1, 0x62,
            0x94, 1, 0x62, 0x94, 0, 0x66])
        self.assertEqual(channels[5], bytes([0xfc, 0, 1, 0xff, 0xff, 0xfd, 0xff, 0xfb]))

    def test_furnace_fixed_stream_retriggers_after_one_shot_without_stop(self):
        # Furnace sets 90 once per channel (vgmOps.cpp 2532-2549), then emits
        # repeated 95 starts for that stream (753-837), without needing 94.
        # Each one-byte block here has naturally finished before the next 62.
        channels = self.convert_stream([
            0x67, 0x66, 5, 1, 0, 0, 0, 16,
            0x67, 0x66, 5, 1, 0, 0, 0, 31,
            0x90, 7, 0x1b, 5, 6, 0x91, 7, 5, 1, 0,
            0x92, 7, 0x30, 0x1b, 0, 0,
            0x95, 7, 0, 0, 0, 0x62, 0x95, 7, 1, 0, 0, 0x66])
        self.assertEqual(channels[5], bytes([0xfc, 0, 0, 0xff, 0xfc, 1, 0, 0xff, 0xfb]))

    def test_channel_reuse_with_a_different_stream_or_mapping_requires_explicit_stop(self):
        setup = [0x90, 0, 0x1b, 5, 6, 0x90, 1, 0x1b, 5, 6,
                 0x95, 0, 0, 0, 0, 0x62]
        # Duration/frequency commands are not simulated by HuSFX conversion;
        # require an explicit stop for remaps and reuse by a different ID.
        for reuse in ([0x90, 0, 0x1b, 4, 6], [0x95, 1, 0, 0, 0]):
            with self.subTest(reuse=reuse), self.assertRaisesRegex(ValueError, 'automatic sample completion'):
                self.convert_stream(setup + reuse + [0x66])
        channels = self.convert_stream(setup + [0x94, 0, 0x95, 1, 0, 0, 0, 0x66])
        self.assertEqual(channels[5], bytes([0xfc, 0, 0, 0xff, 0xfd, 0xfc, 0, 0, 0xff, 0xfb]))

    def test_legacy_setup_free_streams_remain_channel_numbers(self):
        channels = self.convert_stream([0x95, 5, 255, 0, 0, 0x94, 255, 0x66])
        self.assertEqual(channels[5], bytes([0xfc, 255, 0, 0xfd, 0xff, 0xfb]))

    def test_unsupported_stream_setups_and_unknown_ids_are_rejected_before_output(self):
        for command in (
            [0x90, 0, 0x02, 5, 6],   # wrong chip
            [0x90, 0, 0x9b, 5, 6],   # second HuC6280
            [0x90, 0, 0x1b, 6, 6],   # invalid channel
            [0x90, 0, 0x1b, 5, 4],   # not the DAC register
            [0x90, 255, 0x1b, 5, 6], # reserved stream ID
            [0x95, 7, 0, 0, 0],      # no mapping or compatibility channel
            [0x90, 0, 0x1b, 5, 6, 0x95, 1, 0, 0, 0], # missing explicit setup
        ):
            with self.subTest(command=command), self.assertRaises(ValueError):
                self.convert_stream(command + [0x66])
            self.assertFalse((self.folder / 'streams').exists())


if __name__ == '__main__':
    unittest.main()
