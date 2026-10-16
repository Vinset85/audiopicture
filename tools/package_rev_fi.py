"""Package the verified FI delta and raw evidence, without modifying old archives."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = 'f45808a49d7e4ceba46a800b765b528b9fde5046'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).splitlines()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    archive = args.out / 'audiopicture-rev-fi-supplement.zip'
    if archive.exists():
        raise FileExistsError('Use a fresh output directory; published archives are immutable.')
    raw = []
    for p in sorted((ROOT / 'evidence/rev-fi').rglob('*')):
        if p.is_file() and subprocess.run(['git', 'check-ignore', '-q', str(p.relative_to(ROOT))], cwd=ROOT).returncode == 0:
            raw.append({'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size, 'sha256': sha(p)})
    index = {
        'revision': 'Rev.FI', 'publication_verified': False,
        'release_tag': 'checkpoint-rev-fi-2026-10-16', 'checkpoint_parent_head': BASE,
        'baseline_release': 'https://github.com/Vinset85/audiopicture/releases/tag/checkpoint-rev-fa-2026-10-06',
        'scope': 'One serial refined-mesh LC4 right-corner screen on the unchanged FG frame. Two-level displacement consistency only, not full mesh convergence or production qualification. Extract over all four Rev.FA parts and Rev.FB/FC/FD/FE/FG/FH supplements.',
        'files': raw,
    }
    (ROOT / 'evidence/rev-fi/raw-artifact-index.json').write_text(json.dumps(index, indent=2) + '\n')
    files = set(git('diff', BASE, '--name-only') + git('ls-files', '--others', '--exclude-standard'))
    files.update(str(p.relative_to(ROOT)) for p in (ROOT / 'evidence/rev-fi').rglob('*') if p.is_file())
    files -= {'evidence/rev-fi/github-publication.json', 'evidence/rev-fi/archive-tree-verification.json'}
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name in sorted(files):
            z.write(ROOT / name, 'audiopicture/' + name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.infolist()) == len(files)
        for name in sorted(files):
            h = hashlib.sha256()
            with z.open('audiopicture/' + name) as f:
                for block in iter(lambda: f.read(1024 * 1024), b''):
                    h.update(block)
            assert h.hexdigest() == sha(ROOT / name), name
    digest = sha(archive)
    (args.out / 'SHA256SUMS.txt').write_text(digest + '  ' + archive.name + '\n')
    manifest = {'revision': 'Rev.FI', 'archive': archive.name, 'bytes': archive.stat().st_size,
                'sha256': digest, 'file_count': len(files), 'zip_crc': 'PASS',
                'all_members_sha256_verified': len(files), 'raw_members_individually_sha256_verified': len(raw),
                'baseline_release': index['baseline_release'], 'scope': index['scope']}
    (args.out / 'release-assets-sha256.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
