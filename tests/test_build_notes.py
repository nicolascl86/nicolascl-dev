"""Field Notes build: Markdown to pages, feed, sitemap and homepage card, in an isolated copy."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'

POST = '''---
title: First note
date: 2026-11-03
summary: A short summary.
tags: [ai, web]
---

Hello **world**. ''' + 'word ' * 500

class BuildNotes(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = root = Path(self.directory.name)
        (root / 'scripts').mkdir()
        for name in ('build-notes.py', 'sync-public.py'):
            shutil.copy2(SCRIPTS / name, root / 'scripts' / name)
        for name in ('public', 'assets', 'content/notes'):
            (root / name).mkdir(parents=True)
        for image in ('favicon.png', 'elephant-logo.png'):
            (root / 'assets' / image).write_bytes(b'image fixture')
        (root / 'styles.css').write_text('body {}\n')
        (root / 'thelab.css').write_text('@import url("styles.css");\n')
        (root / 'script.js').write_text('/* ui */\n')
        (root / 'index.html').write_text('<link href="styles.css"><!-- latest-note:start --><!-- latest-note:end -->')
        (root / 'content/notes/first-note.md').write_text(POST)

    def tearDown(self):
        self.directory.cleanup()

    def run_build(self, *args):
        return subprocess.run([sys.executable, str(self.root / 'scripts' / 'build-notes.py'), *args],
                              capture_output=True, text=True)

    def test_builds_pages_feed_sitemap_and_card(self):
        result = self.run_build()
        self.assertEqual(result.returncode, 0, result.stderr)
        post = (self.root / 'notes/first-note/index.html').read_text()
        self.assertIn('<strong>world</strong>', post)
        self.assertIn('3 min read', post)  # 502 words at 220 words per minute
        self.assertIn('#ai', post)
        self.assertIn('"@type": "BlogPosting"', post)
        self.assertIn('KEEP EXPLORING', post)
        self.assertIn('href="/about.html"', post, 'the only note points readers to About')
        self.assertIn('class="site-nav"', post)
        self.assertIn('/thelab.css?v=', post, 'sync must version root-absolute asset URLs')
        self.assertIn('first-note', (self.root / 'notes/index.html').read_text())
        self.assertIn('https://nicolascl.dev/notes/first-note/', (self.root / 'feed.xml').read_text())
        self.assertIn('https://nicolascl.dev/notes/first-note/', (self.root / 'sitemap.xml').read_text())
        self.assertIn('href="notes/first-note/"', (self.root / 'index.html').read_text())
        self.assertTrue((self.root / 'public/notes/first-note/index.html').exists())
        self.assertTrue((self.root / 'public/feed.xml').exists())
        self.assertEqual(self.run_build('--check').returncode, 0)
        # Editing a post without rebuilding must fail CI.
        (self.root / 'content/notes/first-note.md').write_text(POST.replace('First note', 'Renamed'))
        self.assertNotEqual(self.run_build('--check').returncode, 0)

    def test_drafts_are_not_published_and_removed_posts_disappear(self):
        self.assertEqual(self.run_build().returncode, 0)
        (self.root / 'content/notes/first-note.md').write_text(POST.replace('tags:', 'draft: true\ntags:'))
        self.assertEqual(self.run_build().returncode, 0)
        self.assertFalse((self.root / 'notes/first-note').exists())
        self.assertFalse((self.root / 'public/notes/first-note').exists())
        self.assertNotIn('first-note', (self.root / 'index.html').read_text())

    def test_missing_front_matter_gives_a_clear_error(self):
        (self.root / 'content/notes/first-note.md').write_text('---\ntitle: No date\n---\nBody')
        result = self.run_build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('missing date, summary', result.stderr)

if __name__ == '__main__':
    unittest.main()
