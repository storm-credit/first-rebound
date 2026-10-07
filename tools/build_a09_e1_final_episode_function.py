"""Build A09's first bounded function without conferring national-team permission."""

import argparse
import hashlib
import json
from pathlib import Path

import build_a08_finite_function_batch as previous_builder
import build_a09_a14_local_routine_batch as routine_builder
import build_a09_a14_bounded_function_preparation as scope_builder


ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a09_e1_final_episode_function.py'
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
ROUTINE = str(routine_builder.OUTPUT).replace('\\', '/')
SCOPE = str(scope_builder.OUTPUT).replace('\\', '/')
CF = 'design/A09_2023_24_CONDITIONAL_FUNCTIONS.json'
NATIONAL_GATE = 'control/NATIONAL_TEAM_MILITARY_SCOPE_GATE.md'
OUTPUT = Path('design/A09_E1_FINAL_EPISODE_FUNCTION.json')
SOURCES = (SELF, PREVIOUS, ROUTINE, SCOPE, CF, NATIONAL_GATE)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def sha(raw):
    normalized = raw.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def build(root=ROOT):
    previous, routine, scope, cf = (load(root, p) for p in (PREVIOUS, ROUTINE, SCOPE, CF))
    assert previous == previous_builder.load(root, previous_builder.OUTPUT)
    assert not previous_builder.validate(previous, root=root) and previous['independent_review_completed']
    assert routine == routine_builder.load(root, routine_builder.OUTPUT)
    assert not routine_builder.validate(routine, root=root)
    assert routine['independent_review_completed']
    assert scope == scope_builder.load(root, scope_builder.OUTPUT)
    assert not scope_builder.validate(scope, root=root) and scope['independent_review_completed']
    assert cf == scope_builder.load(root, CF), 'A09 candidate loader differs from reviewed source'
    assert sha((root / CF).read_bytes()) == scope['source_sha256'][CF], 'A09 candidate source changed'
    gate = (root / NATIONAL_GATE).read_text(encoding='utf-8-sig')
    assert '2023_path: joint_attempt_selected' in gate
    assert '2023_gold: R09_CAUSALITY_HOLD' in gate
    assert '2023 결과는 금메달을 포함해 R09가 전 경기를 재계산하기 전까지 확정하지 않는다' in gate
    prior_exit = previous['functions'][-1]['exit_state']
    original = cf['functions'][0]
    row = routine['rows'][0]
    assert original['id'] == 'A09-CF01' and original['entry_state'] == prior_exit
    assert row['source_subact'] == 'A09-S1' and row['source_candidate_ids'] == ['A09-CF01']
    assert original['id'] in scope['groups'][0]['candidate_ids']
    assert not original['selected_event'] and original['choice'] != ''
    assert row['local_routine_observation_selected'] and not row['source_whole_subact_exit_certified']
    return {
        'schema': 'A09_E1_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'independent_review_completed': True,
        'episode_function_id': 'A09-EF-001', 'global_function_order': 43,
        'planned_allocation_slot': 443, 'primary_subact': 'A09-S1',
        'source_conditional_functions': ['A09-CF01'],
        'previous_function': {'id': 'A08-EF-003', 'path': PREVIOUS, 'exact_full_exit': prior_exit},
        'entry_state': prior_exit,
        'single_function': '공동 대표팀 도전에서 본인이 할 준비와 기관 허가를 구분한다',
        'unit_choice': original['choice'],
        'direct_present_cost': original['direct_cost'],
        'beats': [
            {'id': 'A09-P1', 'action': '자신에게 전달된 Chicago 준비 일정과 대표팀 안내를 따로 읽고, 가상 에이전트에게 자신이 제출할 자료와 구단 허가·보험의 별도 담당권한을 묻는다.', 'classification': 'SELECTED_FICTIONAL_AUTHORITY_QUESTION'},
            {'id': 'A09-P2', 'action': row['selected_fictional_routine_action_and_present_cost'], 'classification': 'SELECTED_FICTIONAL_OWN_PREPARATION_AND_TIME_COST'},
            {'id': 'A09-P3', 'action': row['direct_observation_and_limit'], 'classification': 'OBSERVED_OWN_DOCUMENT_LIST_NOT_INSTITUTIONAL_APPROVAL'},
        ],
        'exit_state': original['changed_state'],
        'source_cp2_exit': row['original_cp2_exit'],
        'full_A09_S1_institutional_participation_exit_certified': False,
        'national_team_roster_permission_insurance_travel_or_medal_certified': False,
        'military_status_certified': False,
        'whole_A09_complete': False, 'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'published_episode_number': None,
        'manuscript_word_count': None, 'manuscript_count': 0, 'manuscript_allowed': False,
        'new_author_lock': False, 'design_gate': 'CLOSED',
        'source_hash_method': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_sha256': {p: sha((root / p).read_bytes()) for p in SOURCES},
    }


def render(data):
    return '\n'.join(['# A09 첫 국소 기능 — 기관 권한과 자기 준비', '',
                      f"- 직전 전체 출구: {data['entry_state']}",
                      f"- 기능: {data['single_function']}",
                      f"- 선택: {data['unit_choice']}",
                      f"- 직접 비용: {data['direct_present_cost']}",
                      *[f"- {beat['id']}: {beat['action']}" for beat in data['beats']],
                      f"- 출구: {data['exit_state']}", '',
                      '계획 슬롯 443은 출판 회차가 아니다. 구단 허가·보험·대표팀 명단·실제 이동·금메달·병역 결과는 모두 미인증이다.',
                      '독립검문한 국소 기능이며 누적 등록은 별도 등록기를 따른다. 전체 A09/G13/G14·실제 Pack·원고 미완료, 게이트 `CLOSED`.', ''])


def validate(data, root=ROOT):
    try:
        return [] if data == build(root) else ['A09 E1 differs from source-bound build']
    except (AssertionError, KeyError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / OUTPUT.with_suffix('.md')).write_text(render(data), encoding='utf-8')
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors = validate(saved)
        if (ROOT / OUTPUT.with_suffix('.md')).read_text(encoding='utf-8') != render(saved):
            errors.append('Markdown differs')
        print(json.dumps({'current': not errors, 'errors': errors}))
        if errors:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
