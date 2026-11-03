"""Version local CSS/JS references and sync root sources/assets to public/."""
import argparse
import hashlib
from pathlib import Path
import re
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true', help='Check asset versions and hosting copies without writing.')
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
# Hand-written pages and shared files live at the root; Field Notes pages are
# generated into notes/ by scripts/build-notes.py. Feeds and crawler files are
# copied unchanged.
sources = sorted({p for pattern in ('*.html', '*.css', '*.js', 'notes/**/*.html') for p in root.glob(pattern)})
plain_files = [root / name for name in ('feed.xml', 'sitemap.xml', 'robots.txt') if (root / name).exists()]
key = lambda p: p.relative_to(root).as_posix()
contents = {key(p): p.read_bytes() for p in sources}
contents.update({key(p): p.read_bytes() for p in (root / "assets").rglob("*.png")})
mismatches = []

def versioned(name):
    # Notes pages use root-absolute URLs (/styles.css); hash the same root file.
    return name + '?v=' + hashlib.sha256(contents[name.lstrip('/')]).hexdigest()[:12]

# Resolve the shared stylesheet first: its version is part of the Lab CSS hash.
for p in sources:
    if p.suffix == '.css':
        text = contents[key(p)].decode('utf-8')
        text = re.sub(r'(@import url\(")([^"?]+\.css)(?:\?v=[a-f0-9]+)?("\);)',
                      lambda m: m[1] + versioned(m[2]) + m[3], text)
        contents[key(p)] = text.encode('utf-8')

for p in sources:
    data = contents[key(p)]
    if p.suffix == '.html':
        text = data.decode('utf-8')
        # Local references only. Adobe manages its own stylesheet caching.
        text = re.sub(r'((?:href|src)=")([^":?]+\.(?:css|js|png))(?:\?v=[^"]+)?(")',
                      lambda m: m[1] + versioned(m[2]) + m[3], text)
        data = text.encode('utf-8')
    target = root / 'public' / key(p)
    if args.check:
        if p.read_bytes() != data:
            mismatches.append('unversioned source: ' + key(p))
        if not target.exists() or target.read_bytes() != data:
            mismatches.append('public/' + key(p))
    else:
        if p.read_bytes() != data:
            p.write_bytes(data)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

for source in sorted((root / 'assets').rglob('*')) + plain_files:
    if not source.is_file():
        continue
    target = root / 'public' / source.relative_to(root)
    if args.check:
        if not target.exists() or source.read_bytes() != target.read_bytes():
            mismatches.append(str(target.relative_to(root)))
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

# A deleted or renamed note must not stay online from an old hosting copy.
expected = {key(p) for p in sources}
for stale in sorted((root / 'public' / 'notes').rglob('*.html')) if (root / 'public' / 'notes').exists() else []:
    name = stale.relative_to(root / 'public').as_posix()
    if name in expected:
        continue
    if args.check:
        mismatches.append('stale hosting copy: public/' + name)
    else:
        stale.unlink()
        for parent in stale.parents:
            if parent == root / 'public' or any(parent.iterdir()):
                break
            parent.rmdir()

if mismatches:
    parser.exit(1, 'Stale asset versions or hosting copies: ' + ', '.join(mismatches) + '\nRun python3 scripts/build-notes.py\n')
print('Asset versions and hosting copies match.' if args.check else 'Asset versions and Firebase public/ copies updated.')
