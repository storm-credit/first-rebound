"""Build A04's Chicago contact function without prepaying the summer choice."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a04_e3_final_episode_function as previous_builder
import build_a04_cf05_cf06_contact_summer_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A04_E4_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = OUTPUT.with_suffix('.md')
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
WORKING = str(working_builder.OUTPUT).replace('\\', '/')
CANDIDATES = 'design/A04_DRAFT_CONDITIONAL_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
ACT_MAP = 'design/ACT_MAP.md'
SOURCES = ('tools/build_a04_e4_final_episode_function.py', PREVIOUS, WORKING,
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
    assert previous == working_builder.load(root, previous_builder.OUTPUT), 'E3 differs from CF05/06 validation input'
    assert not working_builder.validate(selected, root=root), 'CF05/06 model must be source-current'
    assert previous['episode_function_id'] == 'A04-EF-003'
    assert previous['final_function_order'] == 25 and previous['planned_allocation_slot'] == 147
    assert previous['next_unit']['id'] == 'A04-CF05'
    assert previous['next_unit']['private_board_or_pick_response_prepaid'] is False
    assert previous['whole_A04_S1_exit_certified'] is False
    assert selected['status'] == 'SELECTED_ROUTINE_CONTACT_SUMMER_INDEPENDENTLY_REVIEWED'
    assert selected['independent_review_completed'] is True
    assert selected['previous_exact_full_exit'] == previous['exit_state']
    assert selected['source_function_ids'] == ['A04-CF05', 'A04-CF06']
    assert [step['id'] for step in selected['steps']] == ['C0', 'C1', 'C2', 'S1', 'S2']
    assert [step['source_function'] for step in selected['steps']] == ['A04-CF05']*3 + ['A04-CF06']*2
    assert selected['steps'][0]['new_exact_draft_event_certified'] is False
    assert selected['steps'][1]['actual_NBA_employee_identity_or_quote_certified'] is False
    assert selected['steps'][2]['representative_can_bind_Chicago_or_sign_UPC'] is False
    assert selected['original_CP2_provisional_beliefs_inherited_as_observed']['S2_immediate_starter_assumption'] is False
    assert selected['limits']['final_episode_function_created_here'] is False
    assert selected['limits']['actual_exact_pick_22_or_downstream_board_certified'] is False
    assert selected['limits']['signed_UPC_exact_salary_option_bonus_or_agent_name_certified'] is False
    assert selected['limits']['medical_clearance_or_official_team_roster_receipt_certified'] is False
    assert candidates['status'] == 'SIX_CONDITIONAL_DRAFT_CAUSAL_FUNCTIONS_NOT_FINAL_G13'
    cf05, cf06 = candidates['functions'][4:6]
    assert (cf05['id'], cf05['next'], cf05['subact']) == ('A04-CF05','A04-CF06','A04-S2')
    assert cf05['choice'] == selected['source_candidate_choices_and_costs']['CF05_choice']
    assert cf05['direct_cost'] == selected['source_candidate_choices_and_costs']['CF05_direct_cost']
    assert cf05['changed_state'] == cf06['entry_state']
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    s2 = next(row for row in cp2['subacts'] if row['id'] == 'A04-S2')
    assert s2['entry_state'] == 'Chicago 입단을 즉시 주전으로 읽음'
    assert s2['choice'] == 'Chicago 입단을 주전 약속으로 읽지 않고 구단이 요구하는 개발 과제부터 확인한다'
    assert s2['institutional_constraint'] == '정확 순번·하류 보드·rookie 계약 HOLD'
    assert '| A04 | 2018 Draft | 시장의 선택 | 12 |' in (root / ACT_MAP).read_text(encoding='utf-8-sig')

    beats = [{
        'id': step['id'], 'classification': step['kind'],
        'action': step['action'], 'observable_result': step['observable_result'],
        'source_path': WORKING,
    } for step in selected['steps'][:3]]
    exit_state = (
        '주인공은 앞선 개인 훈련의 좁은 수정 행동을 구단의 비공개 평가로 착각하지 않았다. '
        '승인된 Chicago 1라운드 진입 방향 뒤의 가상 준비 연락에서 계약 서류·검사·구단 개발 과제 중 '
        '누가 확인해야 할 항목인지 묻고, 이름 없는 대리인의 일반 설명과 아직 기관이 확정하지 않은 세부를 나누었다. '
        '그는 쉬거나 개인 활동에 쓸 시간을 이 미확인 항목 정리에 썼지만, 정확 지명 순번·실제 서명·의료 적합·주전 권한은 얻지 못했다.'
    )
    blueprint = {
        'schema': 'A04_CF05_CONTACT_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_FICTIONAL_PREPARATION_CONTACT_NOT_UPC_OR_ROSTER_RECEIPT',
        'entry_state': previous['exit_state'],
        'single_function': 'Chicago 방향의 가상 준비 연락에서 계약·개발 질문과 아직 확인되지 않은 기관 항목을 분리한다',
        'unit_choice': cf05['choice'],
        'direct_present_cost': selected['direct_present_cost']['CF05'],
        'exit_state': exit_state,
        'beats': copy.deepcopy(beats),
    }
    return {
        'schema': 'A04_E4_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_CONDITIONAL_CHICAGO_CONTACT_NOT_FULL_A04',
        'episode_function_id': 'A04-EF-004', 'act': 'A04', 'primary_subact': 'A04-S2',
        'source_conditional_function': 'A04-CF05',
        'final_function_order': previous['final_function_order'] + 1,
        'planned_allocation_slot': previous['planned_allocation_slot'] + 1,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
            'a02_planned_slots': 54, 'a02_locally_assigned_function_slots': 10,
            'a03_planned_slots': 54, 'a03_locally_assigned_function_slots': 3,
            'a04_planned_slots': 12, 'a04_locally_assigned_function_slots': 4,
            'a04_remaining_planned_slots': 8,
            'total_local_functions_through_this': 26,
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
        'reader_question_at_end': '설명과 미확인 항목을 나눈 뒤 그는 제한된 여름 시간을 어디에 쓸 것인가',
        'internal_order': ['C0','C1','C2'], 'beats': beats,
        'next_unit': {'id': 'A04-CF06', 'status': 'SUMMER_TIME_CHOICE_CONDITIONAL_NOT_EXECUTED',
                      'Asian_Games_nonparticipation_choice_prepaid_by_E4': False,
                      'guaranteed_national_team_place_claimed': False},
        'conditional_public_landing_bridge': {
            'approved_Chicago_first_round_direction': True,
            'exact_pick_draft_call_words_and_date_certified': False,
            'official_UPC_or_roster_receipt_certified': False,
        },
        'original_CP2_S2_immediate_starter_belief_inherited_as_observed': False,
        'information_access': {
            'pov': 'PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'may_know': ['자기가 받은 가상 준비 안내의 일반 범주', '대리인에게 한 질문과 미확인 서류·개발 항목'],
            'cannot_know': ['Chicago의 비공개 보드·정확 22순위', '공식 서명·의료·로스터 수락이 끝났다는 증명',
                            '실존 인물의 발언·주전 약속'],
            'real_scout_or_executive_dialogue': None,
        },
        'verification_limits': [
            'ACTUAL_VERIFIED means current source-bound fictional information contact, not an actual NBA transaction or contract receipt.',
            'CF06 summer decision remains unperformed; the combined working model’s final exit is not the E4 exit.',
            'Approved Chicago first-round direction does not select the exact pick or formal draft-call and signing details.',
        ],
        'whole_A04_S2_exit_certified': False, 'whole_A04_act_exit_certified': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'g15_complete': False, 'g16_complete': False,
        'g17_complete': False, 'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {path: norm_sha((root / path).read_bytes()) for path in SOURCES},
    }


def render(data):
    lines = [
        '# A04 네 번째 국소 기능 — 연락과 미확인 항목', '',
        '**범위:** 원고가 아닌 기능표 1건. 승인된 Chicago 진입 방향 뒤의 가상 준비 안내만 다룬다. 정확 드래프트 호출·계약 서명·의료·주전 약속은 아니다.', '',
        f"- 상태: `{data['status']}` / 국소 출처현재성 `{data['local_blueprint']['status']}`",
        f"- 전역 기능 {data['final_function_order']}, A04 계획 슬롯 {data['planned_allocation_slot']} (출판 번호 아님)",
        f"- E3 정확 진입: {data['entry_state']}",
        f"- 선택: {data['unit_choice']}",
        f"- 직접 비용: {data['direct_present_cost']}", '',
        '| 단계 | 직접 행동 | 관측·권한 한계 |', '| --- | --- | --- |',
    ]
    for beat in data['beats']:
        lines.append(f"| {beat['id']} | {beat['action']} | {beat['observable_result']} |")
    lines += [
        '', f"- 정확 출구: {data['exit_state']}",
        f"- 다음 독자 질문: {data['reader_question_at_end']}",
        '- CF06의 아시안게임 불참·여름 시간 선택은 E4에서 실행하지 않는다. 원 CP2의 즉시 주전 잠정 진입도 현재 믿음으로 상속하지 않는다.',
        '- 전체 A04-S2/Act·G13/G14·실제 Pack·원고 미완료, 설계/원고 게이트 `CLOSED`.', '',
    ]
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A04 E4 differs from source-bound reviewed contact']


def self_test(data, root=ROOT):
    cases = [
        ('E4 preselects summer', lambda x: x['next_unit'].update(Asian_Games_nonparticipation_choice_prepaid_by_E4=True)),
        ('starter promise invented', lambda x: x.update(original_CP2_S2_immediate_starter_belief_inherited_as_observed=True)),
        ('draft call certified', lambda x: x['conditional_public_landing_bridge'].update(exact_pick_draft_call_words_and_date_certified=True)),
        ('agent signed UPC', lambda x: x['beats'][2].update(observable_result='The agent signs the Chicago UPC.')),
        ('combined model final exit copied early', lambda x: x.update(exit_state='그는 아시안게임에 불참하고 Chicago 여름 개발을 택했다')),
        ('cost erased', lambda x: x.update(direct_present_cost='')),
    ]
    for name, mutation in cases:
        changed = copy.deepcopy(data)
        mutation(changed)
        assert validate(changed, root), name
    original_load = load
    for name, path, mutation in [
        ('E3 exit altered', PREVIOUS,
         lambda x: x.update(exit_state='공식 Chicago 22순위 계약을 체결했다')),
        ('working C1 becomes contract receipt', WORKING,
         lambda x: x['steps'][1].update(observable_result='He receives a signed and paid UPC.')),
        ('same-ID CF05 choice becomes guaranteed starter', CANDIDATES,
         lambda x: x['functions'][4].update(choice='Chicago가 주전 계약을 보장했다')),
    ]:
        def altered(root, requested, path=path, mutation=mutation):
            source = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                source = copy.deepcopy(source)
                mutation(source)
            return source
        with patch(__name__ + '.load', side_effect=altered):
            assert validate(data, root), name
    return len(cases) + 3


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
    print(json.dumps({'current': not errors, 'errors': errors,
                      'negative_controls': tested, 'function': data['episode_function_id'],
                      'order': data['final_function_order'], 'slot': data['planned_allocation_slot']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
