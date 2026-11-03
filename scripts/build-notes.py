"""Build Field Notes from Markdown, then sync everything to public/.

Write posts in content/notes/<slug>.md. Each post starts with a front matter
block between two '---' lines:

    ---
    title: Building this site with AI coding assistants
    date: 2026-11-03
    summary: One or two sentences for cards, search results and link previews.
    tags: [ai, product-management]
    draft: false
    ---

This script generates (all committed, all served by Firebase):
  notes/index.html          the Field Notes listing
  notes/<slug>/index.html   one page per post, served at /notes/<slug>/
  feed.xml                  RSS feed
  sitemap.xml               every public page, for search engines
  index.html                the "Latest field note" card between its markers

Then it runs scripts/sync-public.py. Use --check (CI) to fail when generated
files are out of date, without writing anything.
"""
import argparse
from datetime import date, datetime, timezone
from email.utils import format_datetime
import html
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys

import markdown

SITE_URL = 'https://nicolascl.dev'
SITE_NAME = 'Nicolas Kleovoulou'
AUTHOR = 'Nicolas Kleovoulou'
NOTES_TITLE = 'Field Notes'
NOTES_DESCRIPTION = ('Field Notes by Nicolas Kleovoulou: what I am learning across operations, '
                     'AI, automation and technology, written up as I go.')
DEFAULT_IMAGE = SITE_URL + '/assets/og-default.png'
WORDS_PER_MINUTE = 220
CARD_START, CARD_END = '<!-- latest-note:start -->', '<!-- latest-note:end -->'
REQUIRED = ('title', 'date', 'summary')
# Hand-written pages that are not part of the public site map.
SITEMAP_EXCLUDE = {'404.html'}


class NoteError(Exception):
    pass


def esc(value):
    return html.escape(str(value), quote=True)


def parse_front_matter(text, name):
    """Return (fields, body). Supports 'key: value' and 'key: [a, b]' lines."""
    match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z', text, re.S)
    if not match:
        raise NoteError(f'{name}: must start with a front matter block between two --- lines')
    fields = {}
    for number, line in enumerate(match[1].splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if ':' not in line:
            raise NoteError(f'{name} line {number}: expected "key: value", got {line!r}')
        k, v = (part.strip() for part in line.split(':', 1))
        if v.startswith('[') and v.endswith(']'):
            v = [t.strip().strip('"\'') for t in v[1:-1].split(',') if t.strip()]
        elif len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
            v = v[1:-1]
        fields[k.lower()] = v
    return fields, match[2]


def reading_minutes(body_html):
    words = re.findall(r"[\w’'-]+", re.sub(r'<[^>]+>', ' ', body_html))
    return max(1, math.ceil(len(words) / WORDS_PER_MINUTE))


def load_notes(root):
    notes = []
    for path in sorted((root / 'content' / 'notes').glob('*.md')):
        fields, body = parse_front_matter(path.read_text(encoding='utf-8'), path.name)
        missing = [f for f in REQUIRED if not fields.get(f)]
        if missing:
            raise NoteError(f'{path.name}: missing {", ".join(missing)} in front matter')
        if str(fields.get('draft', 'false')).lower() == 'true':
            continue
        try:
            published = date.fromisoformat(fields['date'])
        except ValueError:
            raise NoteError(f'{path.name}: date must look like 2026-11-03, got {fields["date"]!r}')
        slug = fields.get('slug') or path.stem
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
            raise NoteError(f'{path.name}: slug {slug!r} may only use lowercase letters, digits and hyphens')
        tags = fields.get('tags') or []
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',') if t.strip()]
        body_html = markdown.markdown(body, extensions=['extra', 'sane_lists', 'smarty', 'toc'],
                                      extension_configs={'toc': {'toc_depth': '2-3'}})
        notes.append({
            'slug': slug, 'title': fields['title'], 'summary': fields['summary'], 'date': published,
            'tags': [t.lower() for t in tags], 'html': body_html, 'minutes': reading_minutes(body_html),
            'url': f'{SITE_URL}/notes/{slug}/', 'image': fields.get('image') or DEFAULT_IMAGE,
        })
    slugs = [n['slug'] for n in notes]
    duplicates = {s for s in slugs if slugs.count(s) > 1}
    if duplicates:
        raise NoteError('duplicate slugs: ' + ', '.join(sorted(duplicates)))
    return sorted(notes, key=lambda n: (n['date'], n['slug']), reverse=True)


def human_date(d):
    return f'{d.day} {d:%B %Y}'


def tag_list(tags):
    if not tags:
        return ''
    return '<ul class="tag-list" aria-label="Tags">' + ''.join(f'<li>#{esc(t)}</li>' for t in tags) + '</ul>'


def meta_line(note):
    return (f'<time datetime="{note["date"].isoformat()}">{human_date(note["date"])}</time>'
            f'<span>{note["minutes"]} min read</span>')


def page(*, title, description, url, og_type, image, body, extra_head=''):
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{esc(url)}">
  <meta property="og:site_name" content="{esc(SITE_NAME)}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:url" content="{esc(url)}">
  <meta property="og:image" content="{esc(image)}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="alternate" type="application/rss+xml" title="{esc(NOTES_TITLE)} — {esc(SITE_NAME)}" href="/feed.xml">
  <meta name="theme-color" content="#F8F7FA">
  <link rel="icon" type="image/png" sizes="64x64" href="/assets/favicon.png">
  <link rel="preconnect" href="https://use.typekit.net" crossorigin>
  <link rel="stylesheet" href="https://use.typekit.net/dea3jlm.css">
  <link rel="stylesheet" href="/thelab.css">
  <script src="/script.js" defer></script>
{extra_head}</head>
<body class="project-detail notes-page">
  <div class="page">
    <header><a class="mark" href="/" aria-label="Nicolas Kleovoulou — homepage"><img src="/assets/elephant-logo.png" width="72" height="51" alt="Purple and grey origami elephant"></a><span class="domain">nicolascl.dev</span></header>
    <main>
{body}
    </main>
    <footer>
      <span>Nicolas Kleovoulou</span>
      <div class="footer-links"><a href="/notes/">Field Notes</a><a href="/feed.xml">RSS</a><a href="https://www.linkedin.com/in/nkleovoulou">LinkedIn</a><a href="https://github.com/nicolascl86">GitHub</a></div>
      <span>© 2026</span>
    </footer>
  </div>
</body>
</html>
'''


def note_card(note, heading='h3'):
    return (f'<li><a class="project-card note-card" href="/notes/{note["slug"]}/">'
            f'<span class="card-meta note-meta">{meta_line(note)}</span>'
            f'<{heading}>{esc(note["title"])}</{heading}><p>{esc(note["summary"])}</p>'
            f'{tag_list(note["tags"])}<span class="card-action">Read the note <span aria-hidden="true">→</span></span></a></li>')


def listing_page(notes):
    if notes:
        items = '\n          '.join(note_card(n) for n in notes)
        listing = f'<ul class="project-cards note-cards">\n          {items}\n        </ul>'
    else:
        listing = '<p class="intro">The first note is on its way.</p>'
    body = f'''      <section class="hero" aria-labelledby="notes-title">
        <a href="/">← Back to home</a>
        <p class="eyebrow">Writing</p>
        <h1 id="notes-title">{NOTES_TITLE}</h1>
        <p class="intro">Notes from the field: what I am learning while working across operations, AI, automation and technology — written up as I go.</p>
        <div class="project-meta"><span>{len(notes)} {"note" if len(notes) == 1 else "notes"}</span><a href="/feed.xml">Subscribe via RSS</a></div>
      </section>
      <section class="section" aria-labelledby="all-notes-title">
        <h2 class="section-title" id="all-notes-title">ALL NOTES</h2>
        {listing}
      </section>'''
    return page(title=f'{NOTES_TITLE} — {SITE_NAME}', description=NOTES_DESCRIPTION,
                url=f'{SITE_URL}/notes/', og_type='website', image=DEFAULT_IMAGE, body=body)


def share_links(note):
    from urllib.parse import quote
    u, t = quote(note['url'], safe=''), quote(note['title'], safe='')
    links = [
        ('LinkedIn', f'https://www.linkedin.com/sharing/share-offsite/?url={u}'),
        ('X', f'https://x.com/intent/post?url={u}&amp;text={t}'),
        ('Email', f'mailto:?subject={t}&amp;body={u}'),
    ]
    return ''.join(f'<a href="{href}" rel="noopener" target="_blank">{label}</a>' if label != 'Email'
                   else f'<a href="{href}">{label}</a>' for label, href in links)


def post_page(note, newer, older):
    data = {
        '@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': note['title'],
        'description': note['summary'], 'datePublished': note['date'].isoformat(),
        'url': note['url'], 'mainEntityOfPage': note['url'], 'image': note['image'],
        'keywords': note['tags'], 'wordCount': len(re.findall(r'\S+', re.sub(r'<[^>]+>', ' ', note['html']))),
        'author': {'@type': 'Person', 'name': AUTHOR, 'url': SITE_URL + '/'},
        'publisher': {'@type': 'Person', 'name': AUTHOR, 'url': SITE_URL + '/'},
    }
    json_ld = json.dumps(data, ensure_ascii=False, indent=2).replace('</', '<\\/')
    extra_head = (f'  <meta property="article:published_time" content="{note["date"].isoformat()}">\n'
                  + ''.join(f'  <meta property="article:tag" content="{esc(t)}">\n' for t in note['tags'])
                  + f'  <script type="application/ld+json">\n{json_ld}\n  </script>\n')
    nav = ['<a href="/notes/">← All notes</a>']
    if older:
        nav.append(f'<a href="/notes/{older["slug"]}/">Older: {esc(older["title"])}</a>')
    if newer:
        nav.append(f'<a href="/notes/{newer["slug"]}/">Newer: {esc(newer["title"])} →</a>')
    body = f'''      <article class="note" aria-labelledby="note-title">
        <section class="hero">
          <a href="/notes/">← All notes</a>
          <p class="eyebrow">{NOTES_TITLE}</p>
          <h1 id="note-title">{esc(note["title"])}</h1>
          <p class="intro">{esc(note["summary"])}</p>
          <div class="project-meta note-meta">{meta_line(note)}</div>
          {tag_list(note["tags"])}
        </section>
        <div class="section detail-copy note-body">
{note["html"]}
        </div>
        <aside class="section note-share" aria-label="Share this note">
          <h2 class="section-title">SHARE THIS NOTE</h2>
          <div class="footer-links">{share_links(note)}<a href="/feed.xml">RSS</a></div>
        </aside>
      </article>
      <nav class="project-navigation" aria-label="Notes navigation">
        {''.join(nav)}
      </nav>'''
    return page(title=f'{note["title"]} — {NOTES_TITLE}', description=note['summary'], url=note['url'],
                og_type='article', image=note['image'], body=body, extra_head=extra_head)


def rss(notes):
    def rfc822(d):
        return format_datetime(datetime(d.year, d.month, d.day, tzinfo=timezone.utc))
    items = ''.join(f'''
    <item>
      <title>{esc(n["title"])}</title>
      <link>{n["url"]}</link>
      <guid isPermaLink="true">{n["url"]}</guid>
      <pubDate>{rfc822(n["date"])}</pubDate>
      <description>{esc(n["summary"])}</description>
{''.join(f"      <category>{esc(t)}</category>{chr(10)}" for t in n["tags"])}      <content:encoded><![CDATA[{absolute_links(n["html"]).replace("]]>", "]]]]><![CDATA[>")}]]></content:encoded>
    </item>''' for n in notes)
    updated = f'\n    <lastBuildDate>{rfc822(notes[0]["date"])}</lastBuildDate>' if notes else ''
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>{esc(NOTES_TITLE)} — {esc(SITE_NAME)}</title>
    <link>{SITE_URL}/notes/</link>
    <description>{esc(NOTES_DESCRIPTION)}</description>
    <language>en</language>
    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>{updated}{items}
  </channel>
</rss>
'''


def absolute_links(body_html):
    """Feed readers show posts outside the site, so root-relative links need the domain."""
    return re.sub(r'((?:href|src)=")/(?!/)', r'\1' + SITE_URL + '/', body_html)


def sitemap(root, notes):
    pages = sorted(p.name for p in root.glob('*.html') if p.name not in SITEMAP_EXCLUDE)
    urls = [(SITE_URL + '/' if name == 'index.html' else f'{SITE_URL}/{name}', None) for name in pages]
    urls.append((f'{SITE_URL}/notes/', notes[0]['date'] if notes else None))
    urls += [(n['url'], n['date']) for n in notes]
    entries = ''.join(f'\n  <url><loc>{esc(u)}</loc>{f"<lastmod>{d.isoformat()}</lastmod>" if d else ""}</url>'
                      for u, d in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}\n</urlset>\n'


def homepage_card(note):
    if not note:
        return f'{CARD_START}{CARD_END}'
    return f'''{CARD_START}
      <section class="section latest-note" aria-labelledby="latest-note-title">
        <div class="section-heading"><h2 class="section-title" id="latest-note-title">LATEST FIELD NOTE</h2><a class="text-link" href="notes/">All field notes <span aria-hidden="true">→</span></a></div>
        <a class="work-card latest-note-card" href="notes/{note["slug"]}/">
          <span class="card-meta">{meta_line(note)}</span>
          <h3>{esc(note["title"])}</h3>
          <p>{esc(note["summary"])}</p>
          <span class="card-action">Read the note <span aria-hidden="true">→</span></span>
        </a>
      </section>
      {CARD_END}'''


def generate(root):
    """Return {relative path: text} for every generated file."""
    notes = load_notes(root)
    files = {'notes/index.html': listing_page(notes), 'feed.xml': rss(notes), 'sitemap.xml': sitemap(root, notes)}
    for i, note in enumerate(notes):
        newer = notes[i - 1] if i > 0 else None
        older = notes[i + 1] if i + 1 < len(notes) else None
        files[f'notes/{note["slug"]}/index.html'] = post_page(note, newer, older)
    index = root / 'index.html'
    if index.exists():
        text = index.read_text(encoding='utf-8')
        pattern = re.compile(re.escape(CARD_START) + '.*?' + re.escape(CARD_END), re.S)
        if not pattern.search(text):
            raise NoteError(f'index.html: add {CARD_START}{CARD_END} where the latest note card belongs')
        files['index.html'] = pattern.sub(lambda _: homepage_card(notes[0] if notes else None), text, count=1)
    return files


def normalise(text):
    """The sync step adds ?v= cache versions afterwards; ignore them when comparing."""
    return re.sub(r'\?v=[a-f0-9]{12}', '', text)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--check', action='store_true', help='Fail if generated files are stale; write nothing.')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    try:
        files = generate(root)
    except NoteError as error:
        parser.exit(1, f'Field Notes error: {error}\n')
    expected_dirs = {str(Path(p).parent) for p in files if p.startswith('notes/') and p != 'notes/index.html'}
    notes_dir = root / 'notes'
    leftovers = [d for d in notes_dir.iterdir() if d.is_dir() and f'notes/{d.name}' not in expected_dirs] if notes_dir.exists() else []
    if args.check:
        stale = [p for p, text in files.items()
                 if not (root / p).exists() or normalise((root / p).read_text(encoding='utf-8')) != normalise(text)]
        stale += [f'notes/{d.name}/ (no matching post)' for d in leftovers]
        if stale:
            parser.exit(1, 'Field Notes are out of date: ' + ', '.join(stale) + '\nRun python3 scripts/build-notes.py\n')
        print('Field Notes are up to date.')
        return
    for p, text in files.items():
        target = root / p
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or normalise(target.read_text(encoding='utf-8')) != normalise(text):
            target.write_text(text, encoding='utf-8')
    for d in leftovers:
        shutil.rmtree(d)
    print(f'Built {NOTES_TITLE}: {len([p for p in files if p.count("/") == 2])} published note(s).')
    sys.exit(subprocess.call([sys.executable, str(root / 'scripts' / 'sync-public.py')]))


if __name__ == '__main__':
    main()
