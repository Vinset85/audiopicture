"""Verify public checkpoint assets against local bytes and GitHub SHA-256 digests.

Reads public GitHub metadata only. Does not upload, change credentials or refs.
A receipt is written only after every expected file and the tag commit match.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request


def get_json(url):
    request = urllib.request.Request(url, headers={'Accept': 'application/vnd.github+json',
                                                  'User-Agent': 'AudioPicture-checkpoint-verifier'})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', default='Vinset85/audiopicture')
    parser.add_argument('--tag', required=True)
    parser.add_argument('--expected-commit', required=True)
    parser.add_argument('--assets', required=True, type=Path)
    parser.add_argument('--receipt', required=True, type=Path)
    args = parser.parse_args()
    base = f'https://api.github.com/repos/{args.repository}'
    release = get_json(f'{base}/releases/tags/{args.tag}')
    assert release['draft'] is False, 'Release remains a draft'
    ref = get_json(f'{base}/git/ref/tags/{args.tag}')['object']
    for _ in range(8):
        if ref['type'] == 'commit':
            break
        assert ref['type'] == 'tag', ref
        ref = get_json(f'{base}/git/tags/{ref["sha"]}')['object']
    assert ref['type'] == 'commit' and ref['sha'] == args.expected_commit, ref
    local = {p.name: p for p in args.assets.iterdir() if p.is_file()}
    remote = {a['name']: a for a in release['assets']}
    assert local, 'No expected local assets'
    assert len(remote) == len(release['assets']), 'Duplicate remote asset names'
    assert set(local) == set(remote), {'missing': sorted(set(local)-set(remote)),
                                      'unexpected': sorted(set(remote)-set(local))}
    results = []
    for name, path in sorted(local.items()):
        asset = remote[name]
        digest = file_sha256(path)
        assert asset['state'] == 'uploaded', asset
        assert path.stat().st_size == asset['size'], name
        assert asset.get('digest') == 'sha256:' + digest, (name, asset.get('digest'))
        results.append({'name': name, 'id': asset['id'], 'bytes': asset['size'],
                        'sha256': digest, 'github_digest': asset['digest'],
                        'url': asset['browser_download_url'], 'integrity_match': True})
    receipt = {'recorded_utc': datetime.now(timezone.utc).isoformat(),
               'repository': args.repository, 'release_id': release['id'],
               'release_url': release['html_url'], 'tag': args.tag,
               'tag_commit': ref['sha'], 'published_at': release['published_at'],
               'prerelease': release['prerelease'], 'assets': results,
               'verification': 'PASS: exact asset set, size and local SHA-256 match GitHub server digests',
               'verification_scope': 'Publication integrity only; does not qualify the engineering design',
               'verified_by_sha256': file_sha256(Path(__file__))}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'release_url': receipt['release_url'], 'tag_commit': ref['sha'],
                      'verified_assets': len(results), 'verification': receipt['verification']}, indent=2))


if __name__ == '__main__':
    main()
