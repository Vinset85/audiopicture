"""Compare every checkpoint ZIP member with its Git blob or raw-artifact index."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--raw-index', required=True, help='Repository-relative index path at the exact commit')
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]

    def git(*cmd):
        return subprocess.check_output(['git', *cmd], cwd=repo)

    commit = git('rev-parse', '--verify', args.commit + '^{commit}').decode().strip()
    tree = git('rev-parse', commit + '^{tree}').decode().strip()
    raw_list = json.loads(git('show', commit + ':' + args.raw_index))['files']
    raw = {r['path']: r for r in raw_list}
    assert len(raw) == len(raw_list), 'Duplicate raw-index paths'
    tracked = {}
    for entry in git('ls-tree', '-rz', commit).split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, kind, digest = meta.decode().split()
        if kind == 'blob':
            tracked[name.decode()] = digest
    checked_tracked = checked_raw = 0
    seen = set()
    with zipfile.ZipFile(args.archive) as z:
        assert z.testzip() is None, 'CRC check failed'
        for member in z.infolist():
            path = PurePosixPath(member.filename)
            assert not path.is_absolute() and '..' not in path.parts
            assert path.parts[0] == 'audiopicture' and len(path.parts) > 1
            name = str(PurePosixPath(*path.parts[1:]))
            assert name not in seen and not member.is_dir(), name
            seen.add(name)
            sha256 = hashlib.sha256()
            blob = hashlib.sha1(f'blob {member.file_size}\0'.encode())
            with z.open(member) as f:
                for block in iter(lambda: f.read(1024 * 1024), b''):
                    sha256.update(block)
                    blob.update(block)
            if name in raw:
                assert name not in tracked, 'Raw index mislabels a versioned artifact'
                assert member.file_size == raw[name]['bytes'] and sha256.hexdigest() == raw[name]['sha256'], name
                checked_raw += 1
            else:
                assert name in tracked and blob.hexdigest() == tracked[name], name
                checked_tracked += 1
    assert set(raw).issubset(seen), 'Raw artifacts missing from archive'
    assert args.raw_index in seen, 'Archive is missing its raw index'
    with args.archive.open('rb') as f:
        archive_hash = hashlib.file_digest(f, 'sha256').hexdigest()
    receipt = {'classification': 'PUBLICATION_PACKAGE_CONSISTENCY_NOT_DESIGN_QUALIFICATION',
               'status': 'PASS', 'engineering_commit': commit, 'engineering_tree': tree,
               'archive': args.archive.name, 'archive_sha256': archive_hash,
               'tracked_archive_members_matching_git_blobs': checked_tracked,
               'raw_members_individually_sha256_verified': checked_raw,
               'verified_by_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
