"""Read-only currentness check for reviewed local A01 Blueprints.

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
UNITS = {
    'opening': (BLUEPRINT, REVIEW, ('B1', 'B2', 'B3', 'B4'), 5),
    'first-trial': ('design/A01_FIRST_TRIAL_BLUEPRINT.json',
                    'reviews/A01_FIRST_TRIAL_BLUEPRINT_REVIEW_2026_10_05.json',
                    ('T1', 'T2'), 3),
    'first-contribution': ('design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json',
                          'reviews/A01_FIRST_CONTRIBUTION_BLUEPRINT_REVIEW_2026_10_05.json',
                          ('C1', 'C2', 'C3'), 5),
}


def sha(data):
    text = data.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def boundaries(data, beat_ids=('B1', 'B2', 'B3', 'B4'), claim_count=5):
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
    if data.get('beat_count') != len(beat_ids) or [b.get('id') for b in beats] != list(beat_ids):
        errors.append('reviewed beat domain mismatch')
    if sum(len(b.get('claims', [])) for b in beats) != claim_count:
        errors.append('reviewed claim domain mismatch')
    paths = [s['path'] for s in data.get('derived_from', [])]
    if len(paths) != len(set(paths)) or set(paths) != set(data.get('source_rev_sha256', {})):
        errors.append('source domain mismatch')
    return errors


def check(root=ROOT, unit='opening'):
    blueprint, review_path, beat_ids, claim_count = UNITS[unit]
    raw = (root / blueprint).read_bytes()
    data = json.loads(raw.decode('utf-8-sig'))
    review = json.loads((root / review_path).read_text(encoding='utf-8-sig'))
    errors = boundaries(data, beat_ids, claim_count)
    if review.get('blueprint_path') != blueprint:
        errors.append('review artifact path mismatch')
    if sha(raw) != review.get('blueprint_sha256'):
        errors.append('reviewed Blueprint body changed')
    for path, expected in data['source_rev_sha256'].items():
        source = Path(path) if Path(path).is_absolute() else root / path
        if not source.is_file() or sha(source.read_bytes()) != expected:
            errors.append('missing or stale source: ' + path)
    previous = {'first-trial': 'design/A01_OPENING_BLUEPRINT.json',
                'first-contribution': 'design/A01_FIRST_TRIAL_BLUEPRINT.json'}.get(unit)
    if previous:
        parent = json.loads((root / previous).read_text(encoding='utf-8-sig'))
        if data.get('entry_state') != parent.get('exit_state'):
            errors.append('previous local exit/entry mismatch')
    return data, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--unit', choices=UNITS, default='opening')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    data, errors = check(unit=args.unit)
    _, _, beat_ids, claim_count = UNITS[args.unit]
    rejected = 0
    if args.self_test:
        mutations = [('global_episode_assignment_locked', True),
                     ('manuscript_allowed', True), ('author_locked', True),
                     ('final_episode_functions_added', 1),
                     ('actual_context_packs', 1), ('final_episode_number', 1)]
        for key, value in mutations:
            candidate = copy.deepcopy(data)
            candidate[key] = value
            assert boundaries(candidate, beat_ids, claim_count), key
            rejected += 1
        candidate = copy.deepcopy(data)
        candidate['beats'].append(copy.deepcopy(candidate['beats'][0]))
        assert boundaries(candidate, beat_ids, claim_count), 'duplicate Beat'
        rejected += 1
    print(json.dumps({'scope': 'LOCAL_REVIEWED_CANON_CURRENTNESS_NOT_EPISODE_AUTHORITY',
                      'unit': args.unit, 'current': not errors, 'sources': len(data['source_rev_sha256']),
                      'beats': len(data['beats']), 'negative_controls_rejected': rejected,
                      'final_episode_functions': 0, 'actual_context_packs': 0,
                      'manuscript_allowed': False, 'errors': errors}, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
