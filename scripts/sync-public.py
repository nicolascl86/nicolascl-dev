"""Sync canonical root website sources to public/, or verify with --check."""
import argparse
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true', help='Fail if hosting copies differ.')
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
mismatches = []
for pattern in ('*.html', '*.css', '*.js'):
    for source in sorted(root.glob(pattern)):
        target = root / 'public' / source.name
        if args.check:
            if not target.exists() or source.read_bytes() != target.read_bytes():
                mismatches.append(source.name)
        else:
            shutil.copy2(source, target)
if mismatches:
    parser.exit(1, 'Outdated public/ copies: ' + ', '.join(mismatches) + '\nRun python3 scripts/sync-public.py\n')
print('Hosting copies match.' if args.check else 'Firebase public/ copies updated.')
