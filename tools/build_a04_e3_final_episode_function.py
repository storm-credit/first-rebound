"""Build one A04 function from the reviewed CF03–CF04 private workout."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a04_e2_final_episode_function as previous_builder
import build_a04_cf03_cf04_workout_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A04_E3_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = OUTPUT.with_suffix('.md')
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
WORKING = str(working_builder.OUTPUT).replace('\\', '/')
CANDIDATES = 'design/A04_DRAFT_CONDITIONAL_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
ACT_MAP = 'design/ACT_MAP.md'
SOURCES = ('tools/build_a04_e3_final_episode_function.py', PREVIOUS, WORKING,
           CANDIDATES, CP2, ACT_MAP)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def norm_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def build(root=ROOT):
    previous = load(root, PREVIOUS)
    selected = load(root, WORKING)
    candidates = load(root, CANDIDATES)
    cp2 = load(root, CP2)
    assert previous == working_builder.load(root, previous_builder.OUTPUT), 'E2 differs from workout validation input'
    assert not working_builder.validate(selected, root=root), 'workout must be source-current'
    assert previous['episode_function_id'] == 'A04-EF-002'
    assert previous['final_function_order'] == 24 and previous['planned_allocation_slot'] == 146
    assert previous['next_unit']['id'] == 'A04-CF03'
    assert previous['next_unit']['official_workout_or_live_defender_success_prepaid'] is False
    assert previous['bounded_A04_S1_preparation_criterion_observed'] is True
    assert previous['whole_A04_S1_exit_certified'] is False
    assert selected['status'] == 'SELECTED_ROUTINE_SINGLE_PRIVATE_WORKOUT_INDEPENDENTLY_REVIEWED'
    assert selected['independent_review_completed'] is True
    assert selected['scope'] == 'ONE_FICTIONAL_PERMITTED_PRIVATE_COACHED_PRACTICE_NOT_OFFICIAL_NBA_WORKOUT'
    assert selected['previous_exact_full_exit'] == previous['exit_state']
    assert selected['source_function_ids'] == ['A04-CF03', 'A04-CF04']
    assert [step['id'] for step in selected['actions']] == ['W0', 'W1', 'W2', 'W3']
    assert selected['actions'][1]['phase'] == 'FIRST_ATTACK_ATTEMPT_WITH_LIMIT'
    assert selected['actions'][2]['phase'] == 'BOUNDED_INSTRUCTION'
    assert selected['actions'][3]['phase'] == 'ONE_BOUNDED_RETRY'
    assert selected['fictional_instruction_authority']['real_person_or_organization_identified'] is False
    assert selected['next_candidate']['id'] == 'A04-CF05'
    assert selected['next_candidate']['private_board_or_pick_response_known'] is False
    assert all(value is False for key, value in selected['limits'].items() if key not in ('actual_context_packs', 'manuscript_count', 'design_gate'))
    assert selected['limits']['actual_context_packs'] == 0
    assert selected['limits']['manuscript_count'] == 0 and selected['limits']['design_gate'] == 'CLOSED'
    assert candidates['status'] == 'SIX_CONDITIONAL_DRAFT_CAUSAL_FUNCTIONS_NOT_FINAL_G13'
    cf03, cf04 = candidates['functions'][2:4]
    assert [cf03['id'], cf04['id']] == selected['source_function_ids']
    assert cf03['choice'] == selected['source_candidate_selection']['CF03_choice']
    assert cf03['direct_cost'] == selected['source_candidate_selection']['CF03_cost']
    assert cf04['choice'] == selected['source_candidate_selection']['CF04_choice']
    assert cf04['direct_cost'] == selected['source_candidate_selection']['CF04_cost']
    assert cf03['changed_state'] == cf04['entry_state'] and cf03['next'] == cf04['id']
    assert cf04['next'] == 'A04-CF05'
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    s1 = next(row for row in cp2['subacts'] if row['id'] == 'A04-S1')
    assert s1['choice'] == '신체 측정으로 순번을 단정하지 않고 준비한 기술의 가능한 범위와 한계를 평가에 내놓는다'
    assert s1['exit_state'] == '보여줄 기술 표본 명확화'
    assert '| A04 | 2018 Draft | 시장의 선택 | 12 |' in (root / ACT_MAP).read_text(encoding='utf-8-sig')

    beats = [{
        'id': step['id'], 'classification': step['phase'],
        'actor': step['actor'], 'action': step['action'],
        'observable_result': step['observable_result'], 'source_path': WORKING,
    } for step in selected['actions']]
    blueprint = {
        'schema': 'A04_CF03_CF04_SINGLE_WORKOUT_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_FICTIONAL_PRIVATE_PREPARATION_NOT_CLUB_EVALUATION',
        'entry_state': previous['exit_state'],
        'single_function': '첫 미완성 공격의 막힘을 드러내고 직접 받은 한 가지 지시를 한 번의 재시도 행동으로 시험한다',
        'CF03_first_attempt_is_prerequisite_not_separate_event': True,
        'unit_choice': cf04['choice'],
        'direct_present_cost': selected['direct_present_cost'],
        'exit_state': selected['selected_design_exit_state'],
        'beats': copy.deepcopy(beats),
    }
    return {
        'schema': 'A04_E3_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_OFFICIAL_NBA_EVALUATION_OR_FULL_A04',
        'episode_function_id': 'A04-EF-003', 'act': 'A04', 'primary_subact': 'A04-S1',
        'source_conditional_functions': ['A04-CF03', 'A04-CF04'],
        'final_function_order': previous['final_function_order'] + 1,
        'planned_allocation_slot': previous['planned_allocation_slot'] + 1,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
            'a02_planned_slots': 54, 'a02_locally_assigned_function_slots': 10,
            'a03_planned_slots': 54, 'a03_locally_assigned_function_slots': 3,
            'a04_planned_slots': 12, 'a04_locally_assigned_function_slots': 3,
            'a04_remaining_planned_slots': 9,
            'total_local_functions_through_this': 25,
            'unassigned_plan_slots_are_not_mandatory_new_events': True,
            'allocation_is_final_published_episode_count': False,
            'A04_slot_per_subact_uniform_distribution_certified': False,
        },
        'final_episode_functions_completed_this_record': 1,
        'previous_function': {'id': previous['episode_function_id'], 'source_path': PREVIOUS,
                              'exact_full_exit': previous['exit_state']},
        'local_blueprint': blueprint,
        'single_function': blueprint['single_function'],
        'entry_state': blueprint['entry_state'],
        'unit_choice': blueprint['unit_choice'],
        'exit_state': blueprint['exit_state'],
        'direct_present_cost': blueprint['direct_present_cost'],
        'reader_question_at_end': '이 한 번의 단순 연결 수정이 구단의 저사용 공격 평가에서도 가치로 읽힐 것인가',
        'internal_order': ['W0', 'W1', 'W2', 'W3'], 'beats': beats,
        'next_unit': {'id': 'A04-CF05', 'status': 'NEXT_CONTACT_CONDITIONAL_NOT_EXECUTED',
                      'private_board_or_pick_response_prepaid': False},
        'bounded_A04_S1_preparation_audit': {
            'E1_E2_personal_sample_clarity_preserved': True,
            'private_coach_first_failure_and_one_correction_observed': True,
            'source_CP2_literal_presentation_to_external_evaluator_observed': False,
            'private_coach_feedback_is_NBA_evaluation': False,
            'private_practice_supplies_one_more_bounded_sample_not_official_grade': True,
        },
        'information_access': {
            'pov': 'PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'may_know': ['자기 첫 시도의 한 드리블 정지와 늦은 연결',
                         '가상 개인 지도자의 한 가지 지시와 무수비 재시도의 단순 패스'],
            'cannot_know': ['실제 NBA 워크아웃 초청·구단 평가·비공개 보드',
                            '공식 Combine·의료 결과·정확 지명 순번·계약',
                            '실전 수비 상대에서의 공격 성공·실존 스카우트 내면'],
            'real_scout_dialogue': None,
        },
        'verification_limits': [
            'ACTUAL_VERIFIED means source-current fictional private practice and one observed instruction-based attempt only.',
            'The first failed attempt is a prerequisite beat for the correction choice; these are not two separate events or functions.',
            'One unopposed pass does not establish made shots, live-defender skill, a club grade or reliable game transfer.',
            'The original CP2 verb to present to evaluation remains unobserved as an external receipt; the coach only gives private preparation feedback.',
        ],
        'bounded_A04_S1_preparation_criterion_observed': True,
        'whole_A04_S1_exit_certified': False, 'whole_A04_act_exit_certified': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'g15_complete': False, 'g16_complete': False,
        'g17_complete': False, 'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {path: norm_sha((root / path).read_bytes()) for path in SOURCES},
    }


def render(data):
    lines = [
        '# A04 세 번째 국소 기능 — 실패 뒤 한 가지 수정', '',
        '**범위:** 원고가 아닌 한 기능표. CF03 첫 공격 시도는 CF04 수정 선택의 전제이며 같은 가상 개인 지도 세션이다. NBA 구단 평가가 아니다.', '',
        f"- 상태: `{data['status']}` / 국소 출처현재성 `{data['local_blueprint']['status']}`",
        f"- 전역 기능 {data['final_function_order']}, A04 계획 슬롯 {data['planned_allocation_slot']} (출판 번호 아님)",
        f"- E2 정확 출구: {data['entry_state']}",
        f"- 선택: {data['unit_choice']}",
        f"- 직접 비용: {data['direct_present_cost']}", '',
        '| 순서 | 행동 | 관측 범위 |', '| --- | --- | --- |',
    ]
    for beat in data['beats']:
        lines.append(f"| {beat['id']} | {beat['action']} | {beat['observable_result']} |")
    lines += [
        '', f"- 정확 출구: {data['exit_state']}",
        f"- 다음 독자 질문: {data['reader_question_at_end']}",
        '- E1·E2의 보여줄 표본 준비 출구를 보존하고, 이번 개인 코치의 관측 한 가지를 더한다. 원 CP2의 외부 평가자에게 실제 제출했다는 주장은 여전히 하지 않는다.',
        '- CF05 미실행. 전체 A04-S1/Act·G13/G14·실제 Pack·원고는 미완료이고 게이트 `CLOSED`다.', '',
    ]
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A04 E3 differs from source-bound reviewed private workout']


def self_test(data, root=ROOT):
    changes = [
        ('split into two functions', lambda x: x['slot_accounting'].update(a04_locally_assigned_function_slots=4)),
        ('NBA evaluation prepaid', lambda x: x['bounded_A04_S1_preparation_audit'].update(private_coach_feedback_is_NBA_evaluation=True)),
        ('actual submission prepaid', lambda x: x['bounded_A04_S1_preparation_audit'].update(source_CP2_literal_presentation_to_external_evaluator_observed=True)),
        ('live skill prepaid', lambda x: x['beats'][3].update(observable_result='He beats an NBA defender in a game.')),
        ('cost erased', lambda x: x.update(direct_present_cost='')),
        ('CF05 prepaid', lambda x: x['next_unit'].update(private_board_or_pick_response_prepaid=True)),
        ('whole G13 prepaid', lambda x: x.update(whole_g13_complete=True)),
    ]
    for name, mutation in changes:
        changed = copy.deepcopy(data)
        mutation(changed)
        assert validate(changed, root), name
    original_load = load
    for name, path, mutation in [
        ('E2 exit becomes official result', PREVIOUS,
         lambda x: x.update(exit_state='NBA Combine에서 최고 수치와 22순위를 받았다')),
        ('reviewed workout first limit erased', WORKING,
         lambda x: x['actions'][1].update(action='He creates an unlimited offense without stopping.')),
        ('source CF04 choice reversed', CANDIDATES,
         lambda x: x['functions'][3].update(choice='지시를 거부하고 수정 시도를 하지 않는다')),
        ('CP2 preparation exit becomes pick', CP2,
         lambda x: next(row for row in x['subacts'] if row['id'] == 'A04-S1').update(exit_state='22순위 계약 체결')),
    ]:
        def altered(root, requested, path=path, mutation=mutation):
            value = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                value = copy.deepcopy(value)
                mutation(value)
            return value
        with patch(__name__ + '.load', side_effect=altered):
            assert validate(data, root), name
    return len(changes) + 4


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MARKDOWN).write_text(render(data), encoding='utf-8')
    errors = validate(data)
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors += validate(saved)
        if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'current': not errors, 'errors': errors, 'negative_controls': tested,
                      'function': data['episode_function_id'], 'order': data['final_function_order'],
                      'slot': data['planned_allocation_slot']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
