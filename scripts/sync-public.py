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
sources = sorted(p for pattern in ('*.html', '*.css', '*.js') for p in root.glob(pattern))
contents = {p.name: p.read_bytes() for p in sources}
mismatches = []

def versioned(name):
    return name + '?v=' + hashlib.sha256(contents[name]).hexdigest()[:12]

# Resolve the shared stylesheet first: its version is part of the Lab CSS hash.
for p in sources:
    if p.suffix == '.css':
        text = contents[p.name].decode('utf-8')
        text = re.sub(r'(@import url\(")([^"?]+\.css)(?:\?v=[a-f0-9]+)?("\);)',
                      lambda m: m[1] + versioned(m[2]) + m[3], text)
        contents[p.name] = text.encode('utf-8')

for p in sources:
    data = contents[p.name]
    if p.suffix == '.html':
        text = data.decode('utf-8')
        # Local references only. Adobe manages its own stylesheet caching.
        text = re.sub(r'((?:href|src)=")([^"/:?]+\.(?:css|js))(?:\?v=[a-f0-9]+)?(")',
                      lambda m: m[1] + versioned(m[2]) + m[3], text)
        data = text.encode('utf-8')
    target = root / 'public' / p.name
    if args.check:
        if p.read_bytes() != data:
            mismatches.append('unversioned source: ' + p.name)
        if not target.exists() or target.read_bytes() != data:
            mismatches.append('public/' + p.name)
    else:
        if p.read_bytes() != data:
            p.write_bytes(data)
        target.write_bytes(data)

for source in sorted((root / 'assets').rglob('*')):
    if not source.is_file():
        continue
    target = root / 'public' / source.relative_to(root)
    if args.check:
        if not target.exists() or source.read_bytes() != target.read_bytes():
            mismatches.append(str(target.relative_to(root)))
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
if mismatches:
    parser.exit(1, 'Stale asset versions or hosting copies: ' + ', '.join(mismatches) + '\nRun python3 scripts/sync-public.py\n')
print('Asset versions and hosting copies match.' if args.check else 'Asset versions and Firebase public/ copies updated.')
