"""Build one source-current A01 CF07 local Blueprint and final function.

The selected boxout attempt is routine fictional design. ACTUAL_VERIFIED
means the local Blueprint matches current sources, not author lock, real school
records, skill mastery, a full G13, or manuscript permission.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_a01_cf07_boxout_working_model as working
import build_a01_e3_final_episode_function as e3
import build_a01_followup_school_path as followup


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_E4_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A01_E4_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a01_e4_final_episode_function.py',
    'design/A01_CF07_BOXOUT_WORKING_MODEL_2026_10_07.json',
    'design/A01_E3_FINAL_EPISODE_FUNCTION.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'canon/STORY_BIBLE.md',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF08_ENTRY_PIN = '팀 기여를 반복하기 위한 준비 과제가 생기고 미완성 기술이 남는다'
CF08_CHOICE_PIN = '자신이 맡은 준비 시간에 다시 나와 그 일을 한다'
CF08_CHANGED_PIN = '라이벌뿐 아니라 자신을 기다리는 팀도 다시 나올 이유가 된다'


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, e3.OUTPUT)
    selected = load(root, working.OUTPUT)
    candidates = load(root, 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json')
    story = (root / 'canon/STORY_BIBLE.md').read_text(encoding='utf-8-sig')
    # The CF builder validates the same full predecessor; do not traverse it twice.
    # Independent loader patches must not substitute a different predecessor.
    assert previous == working.load(root, e3.OUTPUT), 'predecessor input differs from CF validation input'
    assert not working.validate(selected, root=root), 'CF07 selected design source is stale'
    assert previous['episode_function_id'] == 'A01-EF-003'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (3, 3)
    assert previous['whole_g13_complete'] is False
    assert selected['status'] == 'ROUTINE_CONCRETE_ACTION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert selected['authority_scope'] == 'FICTIONAL_EDITORIAL_IMPLEMENTATION_NOT_AUTHOR_LOCK_OR_VERIFIED_BLUEPRINT'
    assert selected['entry_state'] == previous['exit_state']
    assert selected['source_function'] == 'A01-CF07'
    assert selected['subact'] == 'A01-S2'
    assert [b['id'] for b in selected['event_steps']] == ['L1', 'L2']
    assert all(b['classification'] == 'ROUTINE_FICTIONAL_DESIGN'
               for b in selected['event_steps'])
    assert selected['school_access']['C1_C2_C3_clearance_automatically_extends_to_CF07'] is False
    assert selected['school_access']['bounded_CF07_learning_session_path_selected'] is True
    assert set(selected['school_access']['pre_session_condition_check_in_selected_model']) == {
        'same_day_class_attendance', 'academic_supplement', 'punctuality'}
    assert all(v == followup.SATISFIED
               for v in selected['school_access']['pre_session_condition_check_in_selected_model'].values())
    assert selected['school_access']['actual_real_school_or_case_records_certified'] is False
    assert selected['school_access']['registration_or_contest_eligibility_certified'] is False
    assert selected['actual_verified_blueprint_created'] is False
    assert selected['final_episode_function_added'] == 0
    assert selected['author_locked'] is False
    assert '한 번의 성공은 완성된 기술이나 천재 인증이 아니라 이후 박스아웃·위치선정·패스 학습을 시작하게 하는 증거다.' in story
    cf08 = next(f for f in candidates['functions'] if f['id'] == 'A01-CF08')
    assert (cf08['status'], cf08['selected_event'], cf08['subact']) == (
        'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE', False, 'A01-S2')
    assert cf08['entry_state'] == CF08_ENTRY_PIN
    assert cf08['choice'] == CF08_CHOICE_PIN
    assert cf08['changed_state'] == CF08_CHANGED_PIN
    assert cf08['next'] == 'A01-CF09'
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
            'protagonist_access': '자신에게 전달된 과제·자기 몸 움직임·상대의 보이는 위치에 한정',
            'source_path': str(working.OUTPUT).replace('\\', '/'),
            'source_step': step['id'],
            'author_locked': False,
        })
    blueprint = {
        'schema': 'A01_CF07_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_LOCAL_ROUTINE_DESIGN_ONLY_NOT_AUTHOR_LOCK_OR_FULL_G13',
        'source_currentness': 'Selected CF07 model and E3 full exit validated against current source files',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': copy.deepcopy(source_hashes),
        'entry_state': previous['exit_state'],
        'single_function': selected['single_function'],
        'unit_choice': '첫 기본 과제를 박스아웃으로 좁혀 눈에 보이는 자리잡기 부족을 확인하고 접근 순서의 재시도까지만 한다',
        'exit_state': selected['selected_design_exit_state'],
        'beat_count': 2,
        'beats': beats,
        'partial_order': ['E3 full exit < L1 first task/shortfall < L2 changed approach attempt'],
        'direct_present_cost': selected['direct_present_cost'],
        'information_access': copy.deepcopy(selected['information_access']),
        'school_access': copy.deepcopy(selected['school_access']),
        'unassigned_details': copy.deepcopy(selected['unassigned_details']),
        'actual_real_school_or_case_records_certified': False,
        'technique_mastery_or_repeat_success_certified': False,
        'author_locked': False,
        'manuscript_allowed': False,
    }
    return {
        'schema': 'A01_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A01-EF-004',
        'act': 'A01', 'primary_subact': 'A01-S2',
        'source_conditional_function': 'A01-CF07',
        'final_function_order': 4,
        'planned_allocation_slot': 4,
        'published_episode_number': None,
        'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': previous['slot_accounting']['a01_planned_slots'],
            'prior_function_slots': 3,
            'this_function_slots': 1,
            'assigned_function_slots_through_this': 4,
            'remaining_planned_slots': 32,
            'allocation_is_final_published_episode_count': False,
        },
        'final_episode_functions_completed_this_record': 1,
        'local_contiguous_functions_through_this': 4,
        'previous_function': {
            'id': previous['episode_function_id'],
            'path': str(e3.OUTPUT).replace('\\', '/'),
            'exit_state': previous['exit_state'],
        },
        'local_blueprint': blueprint,
        'single_function': blueprint['single_function'],
        'entry_state': blueprint['entry_state'],
        'unit_choice': blueprint['unit_choice'],
        'exit_state': blueprint['exit_state'],
        'direct_present_cost': blueprint['direct_present_cost'],
        'reader_question_at_end': selected['reader_question_at_end'],
        'internal_order': ['L1', 'L2'],
        'beats': copy.deepcopy(beats),
        'next_unit': {
            'candidate_id': 'A01-CF08',
            'candidate_status': cf08['status'],
            'candidate_entry_non_authoritative_summary': cf08['entry_state'],
            'candidate_summary_is_exact_or_verified_projection': False,
            'exact_full_entry_if_next_unit_selected': blueprint['exit_state'],
            'candidate_is_executed_here': False,
            'candidate_is_final_episode_function': False,
            'team_preparation_task_or_burden_holder': None,
        },
        'information_access': copy.deepcopy(blueprint['information_access']),
        'school_authority': copy.deepcopy(blueprint['school_access']),
        'unassigned_details': copy.deepcopy(blueprint['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': source_hashes,
        'verification_limits': [
            'ACTUAL_VERIFIED only means this local Blueprint matches current selected design and upstream source revisions.',
            'The selected L1 shortfall and L2 changed attempt are routine fictional design, not preexisting author-locked facts.',
            'A body-position deficiency in the earlier C2 rebound is not inferred from the new L1 failure.',
            'No successful repeat, mastery, rival outcome, contest result, injury, or actual school records are certified.',
            'CF08 remains unexecuted; its candidate entry is not automatically the exact full exit here.',
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
        '# A01 네 번째 최종 회차 기능: 첫 박스아웃 학습', '',
        f"**상태:** 국소 Blueprint `{b['status']}` / 기능 `{data['status']}`. 현재 원천과 선택된 일상 설계의 일치만 검증한다. 새 작가 잠금·전체 G13·원고 허가는 아니다.", '',
        '## 연속 입력과 기능', '',
        f"- 앞 기능 E3의 전체 종료를 그대로 입력: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- 선택: {data['unit_choice']}",
        f"- L1: {b['beats'][0]['action']} → {b['beats'][0]['observable_result']}",
        f"- L2: {b['beats'][1]['action']} → {b['beats'][1]['observable_result']}",
        f"- 현재 비용: {data['direct_present_cost']}",
        f"- 종료: {data['exit_state']}",
        f"- 독자 질문: {data['reader_question_at_end']}", '',
        '## 권위와 인계', '',
        '- L1의 부족과 L2의 변경 시도는 새 가상 일상 설계다. 앞선 C2 리바운드에 같은 결함이 있었다고 소급하지 않는다. 숙련·반복 성공·라이벌 추월은 미확인이다.',
        '- 학교 참여는 이번 세션에 한정해 출석·학업보충·시간준수를 다시 확인하는 설계 모델이며 실제 개별 기록·팀 등록·대회 자격은 인증하지 않는다.',
        '- CF08 팀 준비는 조건부 후보다. 구체 준비 작업·부담 주체·수행 결과를 이 기능에서 실행하지 않는다. 다음 기능이 선택된다면 현재 전체 종료 상태부터 다시 검증한다.',
        f"- 계획 A01 36슬롯 중 기능 배정 4, 남은 {data['slot_accounting']['remaining_planned_slots']}; 출판 회차 번호는 미정.",
        '- 전체 G13/G14·실제 Context Pack·G15–G17·원고는 미완료, 설계/원고 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from current source-bound E4 function']


def self_test(data):
    mutations = [
        ('false author lock', lambda d: d.update(author_locked=True)),
        ('false whole G13', lambda d: d.update(whole_g13_complete=True)),
        ('false manuscript', lambda d: d.update(manuscript_allowed=True)),
        ('old C3 summary instead of full exit', lambda d: d.update(entry_state='CF07 candidate summary')),
        ('false Blueprint authority', lambda d: d['local_blueprint'].update(author_locked=True)),
        ('false skill mastery', lambda d: d['local_blueprint'].update(technique_mastery_or_repeat_success_certified=True)),
        ('erase local action choice', lambda d: d['beats'][1].pop('selected_choice')),
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
