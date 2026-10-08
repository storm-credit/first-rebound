"""Compile all locked LC1 episode inputs while the manuscript gate stays CLOSED.

This compiler checks supplied authority/provenance and information boundaries.
It cannot turn a candidate, a source hash, or a reviewer's inference into canon.
"""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
ALLOCATION = 'design/LC1_FINAL_EPISODE_ALLOCATION_2026_10_08.json'
HISTORY = 'canon/LC1_FULL_SELECTED_HISTORY_AND_ACT_EXIT_LOCK_2026_10_08.json'
BLUEPRINT = 'control/LC1_FINAL_EPISODE_BLUEPRINT_AUTHORITY_2026_10_08.json'
OUT = 'context-packs/lc1-actual'
ALLOWED = {'CANON_FUNCTION', 'AUTHOR_MODELED_DESIGN', 'FACT', 'INFERENCE'}


def normalized(path):
    return path.read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def digest(path):
    return hashlib.sha256(normalized(path).encode()).hexdigest()


def load(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f'Invalid source path: {relative}')
    return json.loads(normalized(path))


def resolve_pointer(value, pointer):
    if pointer in ('', '/'):
        return value
    if not pointer.startswith('/'):
        raise ValueError('JSON pointer must be absolute')
    for token in pointer[1:].split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def require(condition, message):
    if not condition:
        raise ValueError(message)


def compile_inputs(root):
    allocation = load(root, ALLOCATION)
    history = load(root, HISTORY)
    authority = load(root, BLUEPRINT)
    require(allocation['status'] == 'LOCKED_FINAL_EPISODE_FUNCTION_TABLE', 'Final allocation is not locked')
    require(history['status'] == 'LOCKED_SELECTED_DESIGN_HISTORY', 'Whole history is not locked')
    require(history['whole_original_scope_complete'] is True, 'Partial history cannot generate actual packs')
    require(set(history['Act_ids']) == {f'A{i:02}' for i in range(1, 15)}, 'Original 14 Acts missing')
    require(set(history['SubAct_ids']) == {f'A{i:02}-S{j}' for i in range(1, 15) for j in range(1, 4)}, 'Original 42 SubActs missing')
    for value in (allocation, history, authority):
        require(value['manuscript_allowed'] is False and value['design_gate'] == 'CLOSED', 'Manuscript boundary changed')
        require(value['freeze'] == 'v0.30 PARTIAL', 'Freeze changed')
    review_ref = authority['independent_review']
    review = load(root, review_ref['path'])
    require(digest(root / review_ref['path']) == review_ref['source_sha256'], 'Independent review is stale')
    require(review['independent_review_completed'] is True and review['status'].startswith('ACCEPTED'), 'Independent acceptance missing')
    reviewed = review['reviewed_artifacts_sha256']
    for path in (ALLOCATION, HISTORY):
        require(reviewed.get(path) == digest(root / path), f'Whole-scope input not independently reviewed: {path}')
    episodes = allocation['episodes']
    require(len(episodes) == allocation['final_episode_count'] > 0, 'Episode count mismatch')
    require([e['episode'] for e in episodes] == list(range(1, len(episodes) + 1)), 'Episode numbering is not contiguous')
    blueprint_rows = authority['episode_authorities']
    require(len(blueprint_rows) == len(episodes), 'Authority count mismatch')
    by_episode = {r['episode']: r for r in blueprint_rows}
    require(len(by_episode) == len(episodes), 'Duplicate authority')
    nba = sum(e['category'] == 'NBA' for e in episodes)
    require(75 * len(episodes) <= 100 * nba <= 85 * len(episodes), 'NBA allocation is outside 75–85%')
    require(set(e['subact'] for e in episodes) == set(history['SubAct_ids']), 'Final allocation does not cover every SubAct')
    packs = []
    for episode in episodes:
        number = episode['episode']
        row = by_episode[number]
        require(row['qualified_status'] == 'ACTUAL_VERIFIED', f'Episode {number}: Blueprint is unverified')
        require(row['independent_review_completed'] is True, f'Episode {number}: independent review missing')
        ref = row['blueprint']
        source_document = load(root, ref['path'])
        require(digest(root / ref['path']) == ref['source_sha256'], f'Episode {number}: stale Blueprint')
        require(reviewed.get(ref['path']) == ref['source_sha256'], f'Episode {number}: current Blueprint not independently reviewed')
        blueprint = resolve_pointer(source_document, ref['json_pointer'])
        require(blueprint['episode'] == number and blueprint['subact'] == episode['subact'], 'Blueprint allocation mismatch')
        require(blueprint['episode_function'] == episode['episode_function'], 'Blueprint function mismatch')
        access = blueprint['information_boundary']
        require(access['status'] == 'LOCKED_SELECTED_SCENE_ACCESS', f'Episode {number}: access not locked')
        require(access['scene_segments'] and access['access_witnesses'], f'Episode {number}: individual scene access absent')
        require(access['pov_character'] and access['clock_order_verified'] is True, f'Episode {number}: POV/clock absent')
        devices = blueprint['narrative_devices']
        require(1 <= len(devices) <= 2, 'Device budget exceeded')
        claims = blueprint['fact_evidence']
        require(claims and all(c['status'] in ALLOWED for c in claims), f'Episode {number}: candidate or HOLD loaded as fact')
        claim_indexes = set(range(len(claims)))
        last_order = None
        for segment in access['scene_segments']:
            order = segment['scene_order']
            require(isinstance(order, (int, float)) and (last_order is None or last_order <= order), 'Scene order is reversed')
            last_order = order
            known = set(segment['known_claim_indexes'])
            require(known <= claim_indexes and segment['pov_character'], 'Scene knowledge index or POV invalid')
            witnesses = [w for w in access['access_witnesses'] if w['owner'] == segment['pov_character'] and w['scene_order'] == order]
            witnessed = set()
            for witness in witnesses:
                indexes = set(witness['claim_indexes'])
                require(indexes <= claim_indexes and witness['method'], 'Access witness malformed')
                require(witness['acquired_order'] <= order, 'Information acquired after the scene')
                if witness['kind'] == 'OBSERVED_EVENT':
                    require(witness['event_order'] <= witness['acquired_order'], 'Future event loaded as memory')
                else:
                    require(witness['kind'] in ('CURRENT_PLAN', 'EXPLICIT_INFERENCE'), 'Unsupported access kind')
                witnessed |= indexes
            require(known <= witnessed, 'POV knowledge lacks an individual access witness')
        pins = blueprint['source_content_sha256']
        require(pins, 'Source revisions absent')
        for path, pin in pins.items():
            source = (root / path).resolve()
            require(source.is_relative_to(root.resolve()) and source.is_file(), 'Source escapes repository or is missing')
            require(digest(source) == pin, f'Episode {number}: stale source {path}')
        for claim in claims:
            require(claim['source_paths'] and all(p in pins for p in claim['source_paths']), 'Claim provenance incomplete')
            require(claim['status'] != 'FACT' or claim.get('primary_provenance_verified') is True, 'FACT lacks primary evidence')
            require(claim['status'] != 'INFERENCE' or claim.get('inference_label_visible') is True, 'Inference lacks visible label')
        require(blueprint['entry_state'] == episode['entry_state'], 'Entry mismatch')
        require(blueprint['exit_state_required'] == episode['exit_state_required'], 'Exit mismatch')
        packs.append({
            'pack_id': f'LC1-EP-{number:04}', 'target_episode': number,
            'purpose': 'ACTUAL_PRE_MANUSCRIPT_EPISODE_CONTEXT_PACK',
            'manuscript_allowed': False, 'design_gate': 'CLOSED', 'freeze': 'v0.30 PARTIAL',
            'canon_authority': HISTORY, 'history_source_sha256': digest(root / HISTORY),
            'allocation_source_sha256': digest(root / ALLOCATION),
            'blueprint_reference': ref, 'blueprint_qualified_status': 'ACTUAL_VERIFIED',
            'act': episode['act'], 'subact': episode['subact'],
            **{key: blueprint[key] for key in (
                'timeline_window', 'entry_state', 'episode_function', 'act_question', 'subact_question',
                'narrative_devices', 'active_setup', 'payoff_or_defer', 'reader_expected_question',
                'information_boundary', 'fact_evidence', 'relationship_state', 'physical_state',
                'basketball_constraints', 'promises_to_pay', 'forbidden_moves', 'hold_fields',
                'exit_state_required', 'source_content_sha256')},
            'allowed_facts': [c for c in claims if c['status'] == 'FACT'],
            'allowed_canon_functions': [c for c in claims if c['status'] == 'CANON_FUNCTION'],
            'allowed_author_modeled_design': [c for c in claims if c['status'] == 'AUTHOR_MODELED_DESIGN'],
            'allowed_inferences': [c for c in claims if c['status'] == 'INFERENCE'],
            'allowed_knowledge': claims,
            'do_not_explain_device': True,
            'integrity_status': 'SUPPLIED_AUTHORITY_REVISION_AND_BOUNDARY_PASS_NOT_PRIMARY_OR_MANUSCRIPT_CERTIFICATE',
        })
    return packs, nba


def rendered(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    packs, nba = compile_inputs(ROOT)
    output = ROOT / OUT
    expected = {f'EP-{p["target_episode"]:04}.json': rendered(p) for p in packs}
    manifest = {'actual_episode_packs': len(packs), 'NBA_episodes': nba, 'design_gate': 'CLOSED',
                'freeze': 'v0.30 PARTIAL', 'manuscript_allowed': False,
                'history_locked': True, 'full_allocation_coverage': True,
                'pack_sha256': {name: hashlib.sha256(body.encode()).hexdigest() for name, body in expected.items()}}
    expected['manifest.json'] = rendered(manifest)
    physical = {p.name for p in output.glob('*.json')} if output.exists() else set()
    require(not physical - set(expected), 'Unexpected actual pack files; audit before replacing')
    if args.check:
        require(physical == set(expected), 'Actual pack inventory mismatch')
        for name, body in expected.items():
            require(normalized(output / name) == body, f'STALE compiled pack: {name}')
    else:
        output.mkdir(parents=True, exist_ok=True)
        for name, body in expected.items():
            target = output / name
            require(not target.exists() or normalized(target) == body, f'Existing different pack requires explicit regeneration audit: {name}')
            if not target.exists():
                target.write_text(body, encoding='utf-8')
    print(json.dumps({'packs': len(packs), 'NBA_episodes': nba, 'check': args.check, 'manuscript_allowed': False}))


if __name__ == '__main__':
    main()
