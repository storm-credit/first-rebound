"""Read-only currentness check for the reviewed local opening Blueprint.

The reviewed artifact digest binds the human semantic audit. This script does
not approve narrative access, episode placement, history, or Pack generation.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = 'design/A01_OPENING_BLUEPRINT.json'
REVIEW = 'reviews/A01_OPENING_BLUEPRINT_REVIEW_2026_10_04.json'


def sha(data):
    text = data.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def boundaries(data):
    errors = []
    if data.get('status') != 'ACTUAL_VERIFIED':
        errors.append('local currentness not verified')
    if data.get('verification_scope', {}).get('classification') != 'CURRENT_CANON_LOCAL_CORE_EVENTS_ONLY':
        errors.append('verification scope mismatch')
    for key in ['global_episode_assignment_locked', 'manuscript_allowed', 'author_locked']:
        if data.get(key) is not False:
            errors.append(key + ': authority promotion')
    for key in ['final_episode_functions_added', 'actual_context_packs']:
        if type(data.get(key)) is not int or data[key] != 0:
            errors.append(key + ': completion promotion')
    if data.get('final_episode_number') is not None:
        errors.append('final episode assignment')
    info = data.get('information_boundary', {})
    if info.get('individual_scene_pov_verified') is not False:
        errors.append('individual scene access promotion')
    for key in ['exact_date', 'school_name', 'school_administrative_disposition']:
        if key not in info or info[key] is not None:
            errors.append(key + ': unreviewed detail')
    beats = data.get('beats', [])
    if data.get('beat_count') != 4 or [b.get('id') for b in beats] != ['B1', 'B2', 'B3', 'B4']:
        errors.append('reviewed beat domain mismatch')
    if sum(len(b.get('claims', [])) for b in beats) != 5:
        errors.append('reviewed claim domain mismatch')
    paths = [s['path'] for s in data.get('derived_from', [])]
    if len(paths) != len(set(paths)) or set(paths) != set(data.get('source_rev_sha256', {})):
        errors.append('source domain mismatch')
    return errors


def check(root=ROOT):
    raw = (root / BLUEPRINT).read_bytes()
    data = json.loads(raw.decode('utf-8-sig'))
    review = json.loads((root / REVIEW).read_text(encoding='utf-8-sig'))
    errors = boundaries(data)
    if sha(raw) != review.get('blueprint_sha256'):
        errors.append('reviewed Blueprint body changed')
    for path, expected in data['source_rev_sha256'].items():
        source = Path(path) if Path(path).is_absolute() else root / path
        if not source.is_file() or sha(source.read_bytes()) != expected:
            errors.append('missing or stale source: ' + path)
    return data, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    data, errors = check()
    rejected = 0
    if args.self_test:
        mutations = [('global_episode_assignment_locked', True),
                     ('manuscript_allowed', True), ('author_locked', True),
                     ('final_episode_functions_added', 1),
                     ('actual_context_packs', 1), ('final_episode_number', 1)]
        for key, value in mutations:
            candidate = copy.deepcopy(data)
            candidate[key] = value
            assert boundaries(candidate), key
            rejected += 1
        candidate = copy.deepcopy(data)
        candidate['beats'].append(copy.deepcopy(candidate['beats'][0]))
        assert boundaries(candidate), 'duplicate Beat'
        rejected += 1
    print(json.dumps({'scope': 'LOCAL_REVIEWED_CANON_CURRENTNESS_NOT_EPISODE_AUTHORITY',
                      'current': not errors, 'sources': len(data['source_rev_sha256']),
                      'beats': len(data['beats']), 'negative_controls_rejected': rejected,
                      'final_episode_functions': 0, 'actual_context_packs': 0,
                      'manuscript_allowed': False, 'errors': errors}, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
