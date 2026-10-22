"""Validate the finite Sienna design handoff and preservation of current prose.

This is a design/input integrity check, not a prose or independent review.
Run from any directory; --workspace can point to the current manuscript folder.
"""
import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DESIGN = REPO / 'design/sienna-hayes-20261022'
PACKS = REPO / 'context-packs/sienna-hayes-design'


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path,
                        default=Path(r'C:\Users\Storm Credit\Desktop\Novel\thefristrebound'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    checks = []

    def check(name, success, detail=None):
        checks.append({'name': name, 'pass': bool(success), 'detail': detail})

    design = read_json(DESIGN / 'DESIGN.json')
    mapping = read_json(DESIGN / 'TIMELINE_MAPPING.json')
    manifest = read_json(PACKS / 'manifest.json')
    ledger = read_json(REPO / 'research/SIENNA_HAYES_SOURCE_LEDGER_2026_10_22.json')
    receipts = read_json(REPO / 'research/SIENNA_HAYES_TOOL_RECEIPTS_2026_10_22.json')
    scope = read_json(DESIGN / 'AUTHOR_SCOPE.json')
    source_ids = {x['id'] for x in ledger['sources']}
    units = design['subacts']
    unit_ids = [u['id'] for u in units]
    acts = {a['id']: a for a in design['acts']}
    check('unique_6_relationship_acts_12_functions', len(acts) == 6 and len(unit_ids) == len(set(unit_ids)) == 12)
    check('actual_vs_design_pack_count', len(list((REPO / 'context-packs/threepeat-actual').glob('EP????.json'))) == 61
          and len(list(PACKS.glob('SH??.json'))) == 12
          and manifest['actual_episode_pack_count_added'] == 0)
    check('no_new_episode_numbers_or_prose', design['total_new_episode_count'] == 0
          and design['drafted_relationship_scene_count'] == 0
          and all(not p['prose_applied'] for p in units))
    check('author_scope_and_closed_gate', not scope['manuscript_allowed']
          and scope['design_gate'] == scope['manuscript_gate'] == 'CLOSED'
          and scope['freeze'] == 'v0.30 PARTIAL')

    current_manuscripts = {p.name for p in args.workspace.glob('EP????_draft.md')}
    baseline = mapping['protected_manuscript_baseline']
    changed = [name for name, h in baseline.items()
               if not (args.workspace / name).is_file() or sha(args.workspace / name) != h]
    check('all_100_manuscript_files_preserved', len(baseline) == 100
          and current_manuscripts == set(baseline))
    drift = read_json(REPO / 'reviews/SIENNA_HAYES_WORKSPACE_DRIFT_2026_10_22.json')
    # Other tasks may continue editing out-of-scope episodes while this runs.
    # Observe new deltas without overwriting prose or silently replacing baseline.
    drift['latest_observation'] = {
        'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'changes': [{'name': name, 'start_sha256': baseline[name],
                     'current_sha256': sha(args.workspace / name)} for name in changed
                    if (args.workspace / name).is_file()],
        'original_baseline_replaced': False,
    }
    (REPO / 'reviews/SIENNA_HAYES_WORKSPACE_DRIFT_2026_10_22.json').write_text(
        json.dumps(drift, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    check('workspace_drift_disclosed_not_rolled_back',
          drift['action'] == 'PRESERVE_CURRENT_FILES_NO_RESTORE'
          and not drift['latest_observation']['original_baseline_replaced'], changed)
    check('directly_read_41_44_inputs_byte_unchanged',
          not any(f'EP{n:04}_draft.md' in changed for n in [41, 42, 43, 44]))

    protected_changed = []
    for rel, expected in mapping['protected_design_baseline'].items():
        path = REPO / rel
        if not path.is_file():
            protected_changed.append(rel)
            continue
        if rel in ['design/ACT_MAP.md', 'design/SUB_ACT_MAP.md']:
            # The only authorized change to each old map is a dated addendum link.
            text = path.read_text(encoding='utf-8-sig')
            text = re.sub(r'(?m)^2026-10-22 \[시에나 헤이즈[^\n]*\n\n', '', text)
            possible = [text.encode('utf-8'), text.replace('\n', '\r\n').encode('utf-8')]
            if expected not in {hashlib.sha256(v).hexdigest() for v in possible}:
                protected_changed.append(rel)
        elif sha(path) != expected:
            protected_changed.append(rel)
    check('existing_61_packs_manifest_and_gate_unchanged', not protected_changed, protected_changed)

    bounds = next(row for row in mapping['rows'] if row['event'] == '시에나첫만남')
    check('date_event_mapping_not_equal_episode_number', bounds['manuscript_episode'] is None
          and bounds['between_manuscript_episodes'] == [42, 43]
          and bounds['design_episode_refs'] == [14, 15]
          and bounds['proposed_window'] == '2018-08'
          and mapping['number_collision']['manuscript_42'] != mapping['number_collision']['design_42'])
    stale = []
    for ref in mapping['source_design']:
        if sha(REPO / ref['path']) != ref['sha256']:
            stale.append(ref['path'])
    check('source_design_generation_unchanged', not stale, stale)

    for i, unit in enumerate(units):
        row = next((p for p in manifest['packs'] if p['id'] == 'SIENNA-' + unit['id']), None)
        check(unit['id'] + '_act_chain', unit['act_id'] in acts
              and unit['id'] in acts[unit['act_id']]['units']
              and unit['previous_unit_id'] == (unit_ids[i-1] if i else None)
              and unit['next_unit_id'] == (unit_ids[i+1] if i+1 < len(unit_ids) else None))
        if row is None:
            check(unit['id'] + '_manifest', False)
            continue
        path = PACKS / row['path']
        pack = read_json(path)
        check(unit['id'] + '_pack_integrity', sha(path) == row['sha256']
              and pack['function'] == unit and not pack['manuscript_allowed']
              and pack['episode_number'] is None and pack['exact_day'] is None
              and pack['purpose'] == 'RELATIONSHIP_DESIGN_CONTEXT_NOT_ACTUAL_EPISODE_PACK'
              and pack['source_json_pointer'] == '/subacts/' + str(i)
              and set(unit['source_refs']).issubset(source_ids))
        refs = ['source_design', 'author_scope_ref', 'source_ledger_ref', 'character_ref']
        check(unit['id'] + '_references', all((path.parent / pack[key]).resolve().is_file() for key in refs))

    json_files = list(DESIGN.glob('*.json')) + list(PACKS.glob('*.json'))
    for path in json_files:
        read_json(path)
    check('json_parse', True, len(json_files))
    errors = []
    docs = list(DESIGN.glob('*.md')) + [REPO / 'research/SIENNA_HAYES_SOURCE_LEDGER_2026_10_22.md',
           REPO / 'reviews/SIENNA_HAYES_DESIGN_REVIEW_2026_10_22.md']
    for path in docs:
        if not path.is_file():
            errors.append(str(path.relative_to(REPO)))
            continue
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            target = target.strip('<>').split('#', 1)[0]
            if not target or re.match(r'^[a-z]+://', target):
                continue
            if not (path.parent / target).resolve().exists():
                errors.append(str(path.relative_to(REPO)) + ' -> ' + target)
    check('local_markdown_links', not errors, errors)
    text = '\n'.join(p.read_text(encoding='utf-8') for p in DESIGN.glob('*.md'))
    check('rejected_name_not_active_cast', 'Nora' not in text and '노라' not in text)
    check('fiction_not_claimed_as_historical_shoot', not ledger['shoot_itself_historical']
          and not ledger['exact_shoot_day_verified'] and not ledger['new_contract_legal_certification'])
    check('actual_tool_receipts_not_inherited', receipts['antigravity']['response_recovered']
          and receipts['antigravity']['completed_search_calls'] == 4
          and receipts['antigravity']['body_read_calls'] == 0
          and receipts['notebooklm']['analysis_success']
          and len(receipts['notebooklm']['specified_source_ids']) == 5
          and receipts['notebooklm']['primary_url_imports_failed'] == 1
          and receipts['codex']['independent_agent'] == 'NOT_RUN_SELF_REVIEW_ONLY'
          and receipts['claude'] == 'NOT_RUN')
    report = {'scope': 'SIENNA_FINITE_DESIGN_AND_INPUT_INTEGRITY_NOT_PROSE_PASS',
              'passed': all(c['pass'] for c in checks),
              'check_count': len(checks), 'checks': checks,
              'manuscripts_unchanged': 100-len(changed),
              'workspace_changed_since_start': changed,
              'workspace_wide_immutability_claim': False,
              'task_episode_write_operations': drift['episode_write_operations_this_task'],
              'published_1_30_changed_since_start': [name for name in changed if int(name[2:6]) <= 30],
              'initial_check_failure_record': 'Local initial_validation.json retained; global immutability failed on concurrent 30-39 changes, so final scope verifies stable inputs and discloses drift.',
              'actual_episode_packs_unchanged': 61,
              'relationship_design_pack_count': len(manifest['packs']),
              'independent_review': 'NOT_RUN', 'prose_modified_by_this_task': False}
    if args.output:
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'passed': report['passed'], 'checks': len(checks),
                      'failures': [c for c in checks if not c['pass']],
                      'manuscripts_unchanged': report['manuscripts_unchanged']}, ensure_ascii=False))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
