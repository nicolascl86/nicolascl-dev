"""Regression checks for HTML/CSS release consistency, using an isolated copy."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'sync-public.py'

class AssetVersions(unittest.TestCase):
    def test_shared_style_change_versions_import_and_pages(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'scripts').mkdir()
            (root / 'public').mkdir()
            (root / 'assets').mkdir()
            shutil.copy2(SCRIPT, root / 'scripts' / SCRIPT.name)
            (root / 'styles.css').write_text('body { color: #cdc8d3; }\n')
            (root / 'thelab.css').write_text('@import url("styles.css");\n')
            (root / 'script.js').write_text('/* shared UI */\n')
            page = '<img src="assets/logo.png"><link href="https://use.typekit.net/dea3jlm.css"><link href="thelab.css"><script src="script.js"></script>'
            (root / 'index.html').write_text(page)
            (root / 'assets' / 'logo.png').write_bytes(b'brand asset fixture')
            command = [sys.executable, str(root / 'scripts' / SCRIPT.name)]
            def run(*args):
                return subprocess.run(command + list(args), capture_output=True)
            self.assertEqual(run().returncode, 0)
            self.assertEqual(run('--check').returncode, 0)
            before = (root / 'index.html').read_text()
            imported = (root / 'thelab.css').read_text()
            self.assertIn('thelab.css?v=', before)
            self.assertIn('script.js?v=', before)
            self.assertIn('assets/logo.png?v=', before)
            self.assertIn('styles.css?v=', imported)
            self.assertIn('href="https://use.typekit.net/dea3jlm.css"', before)
            self.assertEqual((root / 'assets' / 'logo.png').read_bytes(), (root / 'public' / 'assets' / 'logo.png').read_bytes())
            # A shared CSS edit must invalidate both the nested import and HTML.
            (root / 'styles.css').write_text('body { color: #aaa4b1; }\n')
            self.assertNotEqual(run('--check').returncode, 0)
            self.assertEqual(run().returncode, 0)
            self.assertNotEqual(before, (root / 'index.html').read_text())
            self.assertNotEqual(imported, (root / 'thelab.css').read_text())
            self.assertEqual(run('--check').returncode, 0)
            after = (root / 'index.html').read_bytes()
            self.assertEqual(run().returncode, 0)
            self.assertEqual(after, (root / 'index.html').read_bytes(), 'sync must be idempotent')
            # Replacing artwork must also invalidate cached image URLs.
            (root / 'assets' / 'logo.png').write_bytes(b'updated brand asset')
            self.assertNotEqual(run('--check').returncode, 0)
            self.assertEqual(run().returncode, 0)
            self.assertNotEqual(after, (root / 'index.html').read_bytes())
            # CI catches a stale deployed copy even with correct source versions.
            (root / 'public' / 'thelab.css').write_text(imported)
            self.assertNotEqual(run('--check').returncode, 0)

if __name__ == '__main__':
    unittest.main()
