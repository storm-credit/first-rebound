"""Build source-current local CF08 Blueprint and fifth final episode function.

P1/P2 are selected routine fiction. ACTUAL_VERIFIED certifies source currency,
not author lock, real school records, full G13, or manuscript permission.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_a01_cf08_team_preparation_working_model as working
import build_a01_e4_final_episode_function as e4
import build_a01_followup_school_path as followup


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_E5_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A01_E5_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a01_e5_final_episode_function.py',
    'design/A01_CF08_TEAM_PREPARATION_WORKING_MODEL_2026_10_07.json',
    'design/A01_E4_FINAL_EPISODE_FUNCTION.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF09_ENTRY_PIN = '라이벌뿐 아니라 자신을 기다리는 팀도 다시 나올 이유가 된다'
CF09_CAUSE_PIN = '팀의 준비 약속이 생겨도 게임의 즉시 보상은 여전히 매력적이다'
CF09_CHOICE_PIN = '이번에는 게임을 더 이어가는 대신 준비를 먼저 한다'


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, e4.OUTPUT)
    selected = load(root, working.OUTPUT)
    candidates = load(root, 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json')
    assert not e4.validate(previous, root=root), 'fourth function source is stale'
    assert not working.validate(selected, root=root), 'CF08 selected routine source is stale'
    assert previous['episode_function_id'] == 'A01-EF-004'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (4, 4)
    assert previous['whole_g13_complete'] is False
    assert selected['status'] == 'ROUTINE_CONCRETE_ACTION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert selected['authority_scope'] == 'FICTIONAL_EDITORIAL_IMPLEMENTATION_NOT_AUTHOR_LOCK_OR_VERIFIED_BLUEPRINT'
    assert selected['entry_state'] == previous['exit_state']
    assert selected['source_function'] == 'A01-CF08'
    assert selected['subact'] == 'A01-S2'
    assert [b['id'] for b in selected['event_steps']] == ['P1', 'P2']
    assert all(b['classification'] == 'ROUTINE_FICTIONAL_DESIGN'
               for b in selected['event_steps'])
    assert selected['burden_observation']['alternative_burden_holder'] == '이름 미정 동료 한 명'
    assert selected['burden_observation']['reduced_burden_observed_in_selected_fictional_design'] is True
    assert selected['burden_observation']['real_team_or_player_record_certified'] is False
    assert selected['school_access']['CF07_clearance_automatically_extends_to_CF08'] is False
    assert selected['school_access']['bounded_preparation_occasions_selected'] == 2
    assert set(selected['school_access']['pre_participation_condition_check_each_occasion']) == {
        'same_day_class_attendance', 'academic_supplement', 'punctuality'}
    assert all(v == followup.SATISFIED
               for v in selected['school_access']['pre_participation_condition_check_each_occasion'].values())
    assert selected['school_access']['actual_real_school_or_case_records_certified'] is False
    assert selected['school_access']['registration_or_contest_eligibility_certified'] is False
    assert selected['actual_verified_blueprint_created'] is False
    assert selected['final_episode_function_added'] == 0
    assert selected['author_locked'] is False
    cf09 = next(f for f in candidates['functions'] if f['id'] == 'A01-CF09')
    assert (cf09['status'], cf09['selected_event'], cf09['subact']) == (
        'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE', False, 'A01-S2')
    assert cf09['function'] == '게임 보상을 뒤로 미루기'
    assert cf09['entry_state'] == CF09_ENTRY_PIN
    assert cf09['cause'] == CF09_CAUSE_PIN
    assert cf09['choice'] == CF09_CHOICE_PIN
    assert cf09['next'] == 'A01-CF10'
    source_hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
                     for p in SOURCES}
    beats = []
    for step in selected['event_steps']:
        beats.append({
            'id': step['id'],
            'classification': step['classification'],
            'action': step['action'],
            'observable_result': step['observable_result'],
            'choice_options': copy.deepcopy(step.get('choice_options')),
            'selected_choice': step.get('selected_choice'),
            'not_claimed': step['not_claimed'],
            'protagonist_access': '자기 준비 수행과 이름 미정 동료가 옮기는 공의 보이는 몫만',
            'source_path': str(working.OUTPUT).replace('\\', '/'),
            'source_step': step['id'],
            'author_locked': False,
        })
    blueprint = {
        'schema': 'A01_CF08_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_LOCAL_ROUTINE_DESIGN_ONLY_NOT_AUTHOR_LOCK_OR_FULL_G13',
        'source_currentness': 'Selected CF08 model and E4 full exit validated against current source files',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': copy.deepcopy(source_hashes),
        'entry_state': previous['exit_state'],
        'single_function': selected['single_function'],
        'unit_choice': '이름 미정 동료가 맡던 공 준비 중 자기 몫을 전달받고 다음 허용 기회에 돌아와 수행한다',
        'exit_state': selected['selected_design_exit_state'],
        'beat_count': 2,
        'beats': beats,
        'partial_order': ['E4 full exit < P1 task assigned/burden observed < P2 return and completed share'],
        'direct_present_cost': selected['direct_present_cost'],
        'burden_observation': copy.deepcopy(selected['burden_observation']),
        'information_access': copy.deepcopy(selected['information_access']),
        'school_access': copy.deepcopy(selected['school_access']),
        'unassigned_details': copy.deepcopy(selected['unassigned_details']),
        'actual_real_school_or_case_records_certified': False,
        'team_wide_trust_or_school_life_repair_certified': False,
        'author_locked': False,
        'manuscript_allowed': False,
    }
    return {
        'schema': 'A01_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A01-EF-005',
        'act': 'A01', 'primary_subact': 'A01-S2',
        'source_conditional_function': 'A01-CF08',
        'final_function_order': 5,
        'planned_allocation_slot': 5,
        'published_episode_number': None,
        'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': previous['slot_accounting']['a01_planned_slots'],
            'prior_function_slots': 4,
            'this_function_slots': 1,
            'assigned_function_slots_through_this': 5,
            'remaining_planned_slots': 31,
            'allocation_is_final_published_episode_count': False,
        },
        'final_episode_functions_completed_this_record': 1,
        'local_contiguous_functions_through_this': 5,
        'previous_function': {
            'id': previous['episode_function_id'],
            'path': str(e4.OUTPUT).replace('\\', '/'),
            'exit_state': previous['exit_state'],
        },
        'local_blueprint': blueprint,
        'single_function': blueprint['single_function'],
        'entry_state': blueprint['entry_state'],
        'unit_choice': blueprint['unit_choice'],
        'exit_state': blueprint['exit_state'],
        'direct_present_cost': blueprint['direct_present_cost'],
        'reader_question_at_end': selected['reader_question_at_end'],
        'internal_order': ['P1', 'P2'],
        'beats': copy.deepcopy(beats),
        'next_unit': {
            'candidate_id': 'A01-CF09',
            'candidate_status': cf09['status'],
            'candidate_entry_non_authoritative_summary': cf09['entry_state'],
            'candidate_summary_is_exact_or_verified_projection': False,
            'exact_full_entry_if_next_unit_selected': blueprint['exit_state'],
            'candidate_is_executed_here': False,
            'candidate_is_final_episode_function': False,
            'game_reward_conflict_outcome': None,
        },
        'burden_observation': copy.deepcopy(blueprint['burden_observation']),
        'information_access': copy.deepcopy(blueprint['information_access']),
        'school_authority': copy.deepcopy(blueprint['school_access']),
        'unassigned_details': copy.deepcopy(blueprint['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': source_hashes,
        'verification_limits': [
            'ACTUAL_VERIFIED only means this local Blueprint matches current selected routine design and source revisions.',
            'P1/P2 and the unnamed teammate burden are new routine fictional design, not preexisting author-locked facts.',
            'The visible reduction is one teammate carrying fewer balls in the selected occasion, not team-wide trust or private reaction.',
            'The school conditions are a fictional plan rechecked on both occasions, not actual school records or registration.',
            'CF09 game reward conflict remains conditional and unexecuted.',
        ],
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'g15_complete': False,
        'g16_complete': False, 'g17_complete': False,
        'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }


def render(data):
    b = data['local_blueprint']
    return '\n'.join([
        '# A01 다섯 번째 최종 회차 기능: 공동 준비 몫', '',
        f"**상태:** 국소 Blueprint `{b['status']}` / 기능 `{data['status']}`. 선택된 가상 일상 설계와 현재 원천의 일치만 검증한다. 새 작가 잠금·전체 G13·원고 허가는 아니다.", '',
        '## 연속 입력과 기능', '',
        f"- E4의 전체 종료 입력: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- 선택: {data['unit_choice']}",
        f"- P1: {b['beats'][0]['action']} → {b['beats'][0]['observable_result']}",
        f"- P2: {b['beats'][1]['action']} → {b['beats'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 종료: {data['exit_state']}",
        f"- 독자 질문: {data['reader_question_at_end']}", '',
        '## 권위와 인계', '',
        '- 동료 한 명의 보이는 공 준비 몫만 전후로 비교한다. 동료 속마음·팀 전원 신뢰·학교생활 전체 개선은 결론으로 삼지 않는다.',
        '- 첫 준비와 다음 허용 준비 각각 출석·학업보충·시간준수를 재확인하는 가상 설계다. 실제 학교·개별 기록·등록·대회 자격을 인증하지 않는다.',
        '- CF09 게임 즉시 보상 갈등은 조건부 후보다. 다음 기능이 선택되면 이 기능의 전체 종료 상태에서 다시 검증한다.',
        f"- 계획 A01 36슬롯 중 기능 배정 5, 남은 {data['slot_accounting']['remaining_planned_slots']}; 출판 회차 번호는 미정.",
        '- 전체 G13/G14·실제 Context Pack·G15–G17·원고는 미완료, 설계/원고 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from current source-bound E5 function']


def self_test(data):
    mutations = [
        ('false author lock', lambda d: d.update(author_locked=True)),
        ('false whole G13', lambda d: d.update(whole_g13_complete=True)),
        ('false manuscript', lambda d: d.update(manuscript_allowed=True)),
        ('candidate summary instead of E4 full exit', lambda d: d.update(entry_state=CF09_ENTRY_PIN)),
        ('false Blueprint lock', lambda d: d['local_blueprint'].update(author_locked=True)),
        ('erase observed burden', lambda d: d['local_blueprint']['burden_observation'].pop('after')),
        ('false team trust', lambda d: d['local_blueprint'].update(team_wide_trust_or_school_life_repair_certified=True)),
        ('false school records', lambda d: d['school_authority'].update(actual_real_school_or_case_records_certified=True)),
        ('false next function promotion', lambda d: d['next_unit'].update(candidate_is_executed_here=True)),
        ('false source revision', lambda d: d['source_rev_sha256'].update({'canon/CHARACTER_RESPONSIBILITY_ARC.md': '0' * 64})),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        assert validate(candidate), name
    return len(mutations)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MARKDOWN).write_text(render(data), encoding='utf-8')
    errors = validate(data)
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors.extend(validate(saved))
        if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'function': data['episode_function_id'],
                      'local_blueprint': data['local_blueprint']['status'],
                      'local_complete': 1, 'whole_g13_complete': False,
                      'negative_controls': tested, 'current': not errors,
                      'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
