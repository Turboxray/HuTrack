"""Keep the offline guide, public signatures and bundled converter in sync."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs/huc/huc_hutrack_doc.html'


class Guide(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.references, self.api, self.stack = [], [], [], []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag not in ('meta', 'link', 'img', 'br', 'hr', 'input'):
            self.stack.append(tag)
        if 'id' in attr:
            self.ids.append(attr['id'])
        if tag == 'a':
            self.references.append(attr['href'])
        if tag == 'img':
            self.references.append(attr['src'])
        if 'data-api' in attr:
            self.api.append((attr['data-api'], int(attr['data-argc'])))

    def handle_endtag(self, tag):
        if not self.stack or self.stack.pop() != tag:
            raise AssertionError(f'Mismatched HTML end tag: {tag}')


class DocumentationTests(unittest.TestCase):
    def setUp(self):
        self.guide = Guide()
        self.guide.feed(DOC.read_text(encoding='utf-8'))

    def test_local_links_images_and_html_structure(self):
        self.assertFalse(self.guide.stack)
        self.assertEqual(len(self.guide.ids), len(set(self.guide.ids)))
        for reference in self.guide.references:
            parts = urlsplit(reference)
            if parts.scheme:
                continue
            with self.subTest(reference=reference):
                if parts.path:
                    self.assertTrue((DOC.parent / unquote(parts.path)).is_file())
                elif parts.fragment:
                    self.assertIn(parts.fragment, self.guide.ids)

    def test_every_public_c_overload_is_documented_once(self):
        expected = []
        for name in ('lib/HuTrack/Huc_interface/HuTrack.c', 'lib/HuSFX/HuC_interface/HucSFX.h'):
            header = re.sub(r'//[^\n]*', '', (ROOT/name).read_text(encoding='utf-8'))
            for function, args in re.findall(r'\b(HuTrack\w+|HuSFX\w+|getDataPtr)\s*\(([^)]*)\)\s*(?:macro)?;', header):
                expected.append((function, 0 if args.strip() in ('', 'void') else len(args.split(','))))
        self.assertTrue(expected)
        self.assertEqual(Counter(expected), Counter(self.guide.api))

    def test_bundled_converter_matches_canonical_sources(self):
        for name in ('HuTrackConverter.py', 'support/dmfReader.py', 'support/huTrackBase.py', 'support/hutrackLib.py', 'support/outputBundle.py'):
            with self.subTest(name=name):
                self.assertEqual((ROOT/'utils'/name).read_bytes(), (ROOT/'example/pceas/assets'/name).read_bytes())


if __name__ == '__main__':
    unittest.main()
