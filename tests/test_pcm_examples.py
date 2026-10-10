"""Catch silent or missing waveform assets in the playable PCM demos."""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PcmExampleTests(unittest.TestCase):
    def test_pcm_transition_selects_an_audible_waveform(self):
        for compiler in ('huc', 'hucc'):
            with self.subTest(compiler=compiler):
                project = ROOT / 'example' / (compiler + '_pcm_sample_ids')
                source = (project / 'main/pcm_sample_ids.c').read_text(encoding='utf-8')
                stream = re.search(r'const char pcm_then_wave_sfx\[\] = \{(.*?)\};', source, re.S)[1]
                wave_id = int(re.search(r'HuChanWFupdate\((\d+)\)', stream)[1])
                values = []
                for line in (project / 'assets/sfx/main.wf.inc').read_text(encoding='utf-8').splitlines():
                    line = line.split(';', 1)[0]
                    if '.db' in line:
                        values.extend(int(v, 16) for v in re.findall(r'\$([\da-fA-F]+)', line))
                wave = values[32 * wave_id:32 * (wave_id + 1)]
                self.assertEqual(len(wave), 32, 'selected waveform is missing or incomplete')
                self.assertTrue(all(0 <= v <= 31 for v in wave), 'waveform is not 5-bit')
                self.assertGreater(max(wave), min(wave), 'selected waveform is constant and silent')


if __name__ == '__main__':
    unittest.main()
