"""Build source-current local CF09 Blueprint and sixth final episode function.

The single game-versus-preparation choice is routine fictional design. It
does not establish real school records, lasting self-control, or US transfer.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_a01_cf09_game_priority_working_model as working
import build_a01_e5_final_episode_function as e5
import build_a01_followup_school_path as followup


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_E6_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A01_E6_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a01_e6_final_episode_function.py',
    'design/A01_CF09_GAME_PRIORITY_WORKING_MODEL_2026_10_07.json',
    'design/A01_E5_FINAL_EPISODE_FUNCTION.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'canon/STORY_BIBLE.md',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF10_ENTRY_PIN = '취미를 지우지 않고 한 약속의 순서를 바꾸는 행동이 생긴다'
CF10_CHOICE_PIN = '익숙한 훈련 승부 시간을 다음 환경의 농구 정보 확인에 써서 자신의 기술 격차를 기준으로 국내와 미국 환경을 비교한다'


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, e5.OUTPUT)
    selected = load(root, working.OUTPUT)
    candidates = load(root, 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json')
    # The CF builder validates the same full predecessor; do not traverse it twice.
    # Independent loader patches must not substitute a different predecessor.
    assert previous == working.load(root, e5.OUTPUT), 'predecessor input differs from CF validation input'
    assert not working.validate(selected, root=root), 'CF09 selected routine source is stale'
    assert previous['episode_function_id'] == 'A01-EF-005'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (5, 5)
    assert previous['whole_g13_complete'] is False
    assert selected['status'] == 'ROUTINE_CONCRETE_ACTION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert selected['authority_scope'] == 'FICTIONAL_EDITORIAL_IMPLEMENTATION_NOT_AUTHOR_LOCK_OR_VERIFIED_BLUEPRINT'
    assert selected['entry_state'] == previous['exit_state']
    assert selected['source_function'] == 'A01-CF09'
    assert selected['subact'] == 'A01-S2'
    assert [b['id'] for b in selected['event_steps']] == ['G1', 'G2']
    assert all(b['classification'] == 'ROUTINE_FICTIONAL_DESIGN'
               for b in selected['event_steps'])
    assert selected['time_and_access_model']['short_game_window_before_preparation_selected'] is True
    assert selected['time_and_access_model']['actual_transport_or_minutes_certified'] is False
    assert selected['school_access']['E5_clearance_automatically_extends_to_CF09'] is False
    assert selected['school_access']['bounded_one_preparation_occasion_selected'] is True
    assert set(selected['school_access']['pre_participation_condition_check']) == {
        'same_day_class_attendance', 'academic_supplement', 'punctuality'}
    assert all(v == followup.SATISFIED
               for v in selected['school_access']['pre_participation_condition_check'].values())
    assert selected['school_access']['actual_real_school_or_case_records_certified'] is False
    assert selected['school_access']['registration_or_contest_eligibility_certified'] is False
    assert selected['actual_verified_blueprint_created'] is False
    assert selected['final_episode_function_added'] == 0
    assert selected['author_locked'] is False
    cf10 = next(f for f in candidates['functions'] if f['id'] == 'A01-CF10')
    assert (cf10['status'], cf10['selected_event'], cf10['subact']) == (
        'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE', False, 'A01-S3')
    assert cf10['function'] == '미국 환경과 익숙한 우위의 비교'
    assert cf10['entry_state'] == CF10_ENTRY_PIN
    assert cf10['choice'] == CF10_CHOICE_PIN
    assert cf10['next'] == 'A01-CF11'
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
            'protagonist_access': '자신의 현재 게임 선택, 이미 받은 준비 약속과 본인이 수행한 일에 한정',
            'source_path': str(working.OUTPUT).replace('\\', '/'),
            'source_step': step['id'],
            'author_locked': False,
        })
    blueprint = {
        'schema': 'A01_CF09_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_LOCAL_ROUTINE_DESIGN_ONLY_NOT_AUTHOR_LOCK_OR_FULL_G13',
        'source_currentness': 'Selected CF09 model and E5 full exit validated against current source files',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': copy.deepcopy(source_hashes),
        'entry_state': previous['exit_state'],
        'single_function': selected['single_function'],
        'unit_choice': '게임을 한 판 더 이어갈 수 있어도 이번에는 PC방을 나와 이미 맡은 준비를 먼저 한다',
        'exit_state': selected['selected_design_exit_state'],
        'beat_count': 2,
        'beats': beats,
        'partial_order': ['E5 full exit < G1 game continuation opportunity < G2 decline and perform one assigned preparation'],
        'direct_present_cost': selected['direct_present_cost'],
        'time_and_access_model': copy.deepcopy(selected['time_and_access_model']),
        'information_access': copy.deepcopy(selected['information_access']),
        'school_access': copy.deepcopy(selected['school_access']),
        'unassigned_details': copy.deepcopy(selected['unassigned_details']),
        'actual_real_school_or_case_records_certified': False,
        'lasting_gaming_or_school_routine_repair_certified': False,
        'author_locked': False,
        'manuscript_allowed': False,
    }
    return {
        'schema': 'A01_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A01-EF-006',
        'act': 'A01', 'primary_subact': 'A01-S2',
        'source_conditional_function': 'A01-CF09',
        'final_function_order': 6,
        'planned_allocation_slot': 6,
        'published_episode_number': None,
        'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': previous['slot_accounting']['a01_planned_slots'],
            'prior_function_slots': 5,
            'this_function_slots': 1,
            'assigned_function_slots_through_this': 6,
            'remaining_planned_slots': 30,
            'allocation_is_final_published_episode_count': False,
        },
        'final_episode_functions_completed_this_record': 1,
        'local_contiguous_functions_through_this': 6,
        'previous_function': {
            'id': previous['episode_function_id'],
            'path': str(e5.OUTPUT).replace('\\', '/'),
            'exit_state': previous['exit_state'],
        },
        'local_blueprint': blueprint,
        'single_function': blueprint['single_function'],
        'entry_state': blueprint['entry_state'],
        'unit_choice': blueprint['unit_choice'],
        'exit_state': blueprint['exit_state'],
        'direct_present_cost': blueprint['direct_present_cost'],
        'reader_question_at_end': selected['reader_question_at_end'],
        'internal_order': ['G1', 'G2'],
        'beats': copy.deepcopy(beats),
        'next_unit': {
            'candidate_id': 'A01-CF10',
            'candidate_status': cf10['status'],
            'candidate_subact': cf10['subact'],
            'candidate_entry_non_authoritative_summary': cf10['entry_state'],
            'candidate_summary_is_exact_or_verified_projection': False,
            'exact_full_entry_if_next_unit_selected': blueprint['exit_state'],
            'candidate_is_executed_here': False,
            'candidate_is_final_episode_function': False,
            'us_environment_comparison_or_acceptance': None,
        },
        'time_and_access_model': copy.deepcopy(blueprint['time_and_access_model']),
        'information_access': copy.deepcopy(blueprint['information_access']),
        'school_authority': copy.deepcopy(blueprint['school_access']),
        'unassigned_details': copy.deepcopy(blueprint['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': source_hashes,
        'verification_limits': [
            'ACTUAL_VERIFIED only means this local Blueprint matches current selected routine design and source revisions.',
            'G1/G2 are one new fictional choice, not a preexisting author-locked PC-room episode.',
            'The next game round is delayed; no actual item, win, service title or permanent abstinence is claimed.',
            'One timely preparation attendance does not certify lasting sleep, class attendance or life control.',
            'The school conditions are fictional plan checks, not actual student records.',
            'CF10 US-environment comparison and transfer or acceptance remain unexecuted.',
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
        '# A01 여섯 번째 최종 회차 기능: 게임 한 판보다 약속', '',
        f"**상태:** 국소 Blueprint `{b['status']}` / 기능 `{data['status']}`. 선택된 가상 일상 설계와 현재 원천의 일치만 검증한다. 새 작가 잠금·전체 G13·원고 허가는 아니다.", '',
        '## 연속 입력과 기능', '',
        f"- E5의 전체 종료 입력: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- 선택: {data['unit_choice']}",
        f"- G1: {b['beats'][0]['action']} → {b['beats'][0]['observable_result']}",
        f"- G2: {b['beats'][1]['action']} → {b['beats'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 종료: {data['exit_state']}",
        f"- 독자 질문: {data['reader_question_at_end']}", '',
        '## 권위와 인계', '',
        '- 게임명·친구 신원·다음 판 승리·현금/아이템 보상·정확 시각·이동 경로는 미정이다. 게임을 포기하거나 생활 전체를 고친 결론이 아니다.',
        '- 이번 준비는 E5의 학교 확인을 자동 연장하지 않는 별도 한 기회다. 세 조건 재확인은 가상 운영 모델이며 실제 개별 기록·등록·대회 자격을 인증하지 않는다.',
        '- CF10 미국 환경 비교는 조건부 후보다. 비교, 학교 이전·수락, 미국 프렙 자율 루틴을 선지급하지 않는다.',
        f"- 계획 A01 36슬롯 중 기능 배정 6, 남은 {data['slot_accounting']['remaining_planned_slots']}; 출판 회차 번호는 미정.",
        '- 전체 G13/G14·실제 Context Pack·G15–G17·원고는 미완료, 설계/원고 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from current source-bound E6 function']


def self_test(data):
    mutations = [
        ('false author lock', lambda d: d.update(author_locked=True)),
        ('false whole G13', lambda d: d.update(whole_g13_complete=True)),
        ('false manuscript', lambda d: d.update(manuscript_allowed=True)),
        ('candidate summary instead of E5 full exit', lambda d: d.update(entry_state=CF10_ENTRY_PIN)),
        ('false Blueprint lock', lambda d: d['local_blueprint'].update(author_locked=True)),
        ('game abstinence', lambda d: d['local_blueprint'].update(lasting_gaming_or_school_routine_repair_certified=True)),
        ('erase game choice', lambda d: d['beats'][1].pop('selected_choice')),
        ('false school records', lambda d: d['school_authority'].update(actual_real_school_or_case_records_certified=True)),
        ('false next function promotion', lambda d: d['next_unit'].update(candidate_is_executed_here=True)),
        ('false source revision', lambda d: d['source_rev_sha256'].update({'canon/STORY_BIBLE.md': '0' * 64})),
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
