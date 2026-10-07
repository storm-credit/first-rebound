"""Align provisional S1 operation with its preserved, validated T1/T2 route."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_a01_e2_final_episode_function as e2
import build_a01_e6_final_episode_function as e6
import build_a01_a02_subact_exit_audit as exits

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_S1_OPERATING_ALIGNMENT_2026_10_07.json')
MARKDOWN = OUTPUT.with_suffix('.md')
SOURCES = (
    'tools/build_a01_s1_operating_alignment.py',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'design/A01_E1_FINAL_EPISODE_FUNCTION.json',
    'design/A01_E2_FINAL_EPISODE_FUNCTION.json',
    'design/A01_E6_FINAL_EPISODE_FUNCTION.json',
    'design/A01_FIRST_TRIAL_BLUEPRINT.json',
    'AGENTS.md',
    'design/A01_A02_SUBACT_EXIT_AUDIT_2026_10_07.json',
    'tools/build_a01_a02_subact_exit_audit.py',
)

def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n').encode('utf-8')).hexdigest()

def build(root=ROOT):
    packet = load(root, SOURCES[1])
    first, trial, preparation = (load(root, p) for p in SOURCES[2:5])
    assert not e2.validate(trial, root=root), 'T1/T2 route must remain validated'
    assert not e6.validate(preparation, root=root), 'S2 preparation route must remain validated'
    assert packet['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    subacts = {s['id']: s for s in packet['subacts']}
    original = subacts['A01-S1']
    assert original['choice'] == '재능을 보여 달라는 기대만 붙들지 않고 농구부가 맡기는 기본 준비부터 해 본다'
    assert original['cost'] == '즉시 칭찬을 포기'
    assert original['exit_state'] == '참여와 회피가 분리됨'
    assert first['exit_state'] == trial['entry_state']
    assert trial['episode_function_id'] == 'A01-EF-002'
    assert trial['internal_order'] == ['T1', 'T2']
    assert trial['source_semantic_projection_sha256']['first_trial'] == e2.TRIAL_SEMANTIC_SHA256
    assert '첫 훈련 진입' in trial['unit_choice']
    assert '완패' in trial['exit_state']
    assert preparation.get('primary_subact', preparation.get('subact')) == 'A01-S2'
    assert '맡은 공 준비에 참여했다' in preparation['exit_state']
    original_audit = load(root, str(exits.OUTPUT).replace('\\', '/'))
    assert not exits.validate(original_audit, root=root), 'original six-exit audit must be current'
    assert original_audit['counts']['subact_bounded_pass'] == 5
    assert original_audit['counts']['subact_specific_hold'] == 1
    assert original_audit['subact_exit_rows'][0]['exit_audit_result'] == 'HOLD_CP2_CHOICE_AND_COST_NOT_OBSERVED_IN_S1'
    assert all(row['exit_audit_result'] == 'PASS_BOUNDED_CP2_FUNCTIONAL_EXIT'
               for row in original_audit['subact_exit_rows'][1:])
    effective = copy.deepcopy(original)
    effective['choice'] = trial['unit_choice']
    effective['cost'] = copy.deepcopy(trial['direct_present_cost'])
    effective['status'] = 'WORKING_EDITORIAL_DERIVATION_FROM_VALIDATED_T1_T2'
    return {
        'schema': 'A01_S1_OPERATING_ALIGNMENT_V1',
        'status': 'INDEPENDENTLY_REVIEWED_ROUTINE_OPERATING_ALIGNMENT_WITH_BOUNDED_EXIT_JOIN',
        'target': 'A01-S1',
        'authority': 'EDITORIAL_DERIVATION_WITHIN_APPROVED_DIRECTION_NOT_NEW_AUTHOR_LOCK',
        'original_provisional_row': original,
        'effective_operating_row': effective,
        'witness_function_ids': ['A01-EF-001', 'A01-EF-002'],
        'exact_trial_entry': trial['entry_state'],
        'exact_trial_exit': trial['exit_state'],
        'choice_and_cost_source': SOURCES[3],
        'cost_evidence_class': trial['direct_present_cost']['evidence_class'],
        'participation_exit_supported': True,
        'original_basic_preparation_and_praise_cost_certified_in_s1': False,
        'preparation_remains_at': {'subact': 'A01-S2', 'function_id': preparation['episode_function_id'],
                                  'exact_exit': preparation['exit_state']},
        'preserved': {'original_packet_file': True, 'a01_whole_act': True,
                      's1_entry_and_exit': True, 's2_and_s3_rows': True,
                      'all_existing_final_function_files': True},
        'meaning_review': '회피에서 조건부 체험으로 실제 들어가는 선택만 S1로 둔다. 기본 준비를 선택하는 책임은 기존 S2에 보존하며, 즉시 칭찬을 거절하는 새 사건을 T1/T2에 만들지 않는다.',
        'integrated_exit_audit': {
            'original_comparison_path': str(exits.OUTPUT).replace('\\', '/'),
            'original_provisional_comparison': {'bounded_pass': 5, 'hold': 1, 'remaining': 37},
            'operating_comparison': {'bounded_pass': 6, 'hold_in_first_six': 0, 'remaining': 36},
            's1_operating_result': 'PASS_BOUNDED_DERIVED_PARTICIPATION_CHOICE_AND_PRESENT_COST',
            'other_five_results': [{'subact_id': row['subact_id'], 'result': row['exit_audit_result']}
                                   for row in original_audit['subact_exit_rows'][1:]],
            'original_hold_preserved': True,
            'a02_to_a03_registration_and_first_function_hold_preserved': True,
            'whole_g13_promoted': False,
        },
        'counts': {'new_episode_functions': 0, 'new_events': 0,
                   'new_author_locks': 0, 'whole_subact_passes_promoted_by_this_record': 0},
        'consumer_rule': 'This source-bound join explicitly consumes the preserved original six-exit audit and the reviewed operating overlay. Original CP2 comparison retains its HOLD; only the operating first-six comparison has six bounded passes. Whole G13 remains incomplete.',
        'independent_review_completed': True,
        'independent_review_evidence': {'reviewer': '/root/g11_access', 'meaning_accepted': True,
                                        'source_mutations_rejected': ['same-ID S1 choice reversal', 'same-ID E2 participation choice reversal']},
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'manuscript_count': 0,
        'manuscript_allowed': False, 'design_gate': 'CLOSED', 'author_locked': False,
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {p: sha(root / p) for p in SOURCES},
    }

def render(d):
    return '\n'.join([
        '# A01-S1 잠정 계획과 실제 기능의 운영 정렬', '',
        '원고가 아닌 운영 설계다. 원 CP2와 기존 기능 파일을 보존하며 새 사건·회차·작가 잠금을 추가하지 않는다.', '',
        f"- 상태: `{d['status']}`",
        f"- 기존 잠정 선택: {d['original_provisional_row']['choice']}",
        f"- 기존 잠정 비용: {d['original_provisional_row']['cost']}",
        f"- 운영 선택: {d['effective_operating_row']['choice']}",
        f"- 운영 비용: {d['effective_operating_row']['cost']['claim']}",
        '- E1의 제안은 수락이 아니며 E2 T1의 실제 진입과 T2의 완패를 근거로 한다. 시간 중복 불가는 기존 표시된 추론, 완패는 잠긴 사건이다.',
        '- S1에 기본 준비나 칭찬 거절을 소급하지 않는다. 맡은 준비를 선택하는 기존 S2의 기능은 유지한다.',
        '- 독립 의미 검토와 동일 ID 원천변조 2종 거부를 확인했다. 이 생성기는 원 여섯 출구 감사와 overlay를 실제 읽어 통합한다.',
        '- 원 CP2 비교는 5 PASS/1 HOLD와 남은37을 보존한다. 검토된 운영 비교는 첫6 출구6 PASS·나머지36소막 미완으로 구분한다. A02→A03 등록·첫 기능 HOLD는 유지한다.',
        '- 전체 G13/G14 미완료·실제 Pack0·원고0·설계/원고 CLOSED.', '',
    ])

def validate(d, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, OSError, ValueError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if d == expected else ['operating alignment differs from preserved validated route']

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write', action='store_true')
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    d = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MARKDOWN).write_text(render(d), encoding='utf-8')
    errors = validate(d)
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors += validate(saved)
        if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    print(json.dumps({'current': not errors, 'errors': errors, 'counts': d['counts']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
