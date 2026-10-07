"""Build A04's summer choice from E4 and the reviewed CF05–CF06 route."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a04_e4_final_episode_function as previous_builder
import build_a04_cf05_cf06_contact_summer_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A04_E5_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = OUTPUT.with_suffix('.md')
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
WORKING = str(working_builder.OUTPUT).replace('\\', '/')
CANDIDATES = 'design/A04_DRAFT_CONDITIONAL_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
ACT_MAP = 'design/ACT_MAP.md'
SOURCES = ('tools/build_a04_e5_final_episode_function.py', PREVIOUS, WORKING,
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
    assert selected == previous_builder.load(root, previous_builder.WORKING), 'CF05/06 differs from E4 validation input'
    assert not previous_builder.validate(previous, root=root), 'A04 E4 must be source-current'
    assert previous['episode_function_id'] == 'A04-EF-004'
    assert previous['final_function_order'] == 26 and previous['planned_allocation_slot'] == 148
    assert previous['next_unit']['id'] == 'A04-CF06'
    assert previous['next_unit']['Asian_Games_nonparticipation_choice_prepaid_by_E4'] is False
    assert previous['next_unit']['guaranteed_national_team_place_claimed'] is False
    assert previous['whole_A04_S2_exit_certified'] is False
    assert selected['status'] == 'SELECTED_ROUTINE_CONTACT_SUMMER_INDEPENDENTLY_REVIEWED'
    assert selected['independent_review_completed'] is True
    assert selected['source_function_ids'] == ['A04-CF05', 'A04-CF06']
    assert [step['id'] for step in selected['steps']] == ['C0','C1','C2','S1','S2']
    assert [step['source_function'] for step in selected['steps'][3:]] == ['A04-CF06']*2
    assert selected['steps'][3]['guaranteed_Korea_roster_place_relinquished'] is False
    assert selected['steps'][4]['A05_rookie_performance_prepaid'] is False
    assert selected['approved_direction_vs_unselected_institutional_details']['2018_Asian_Games_nonparticipation'] == 'APPROVED_CANON_DIRECTION'
    assert selected['approved_direction_vs_unselected_institutional_details']['national_team_roster_selection'] is None
    assert selected['limits']['guaranteed_Korea_national_team_place_surrendered'] is False
    assert selected['limits']['signed_UPC_exact_salary_option_bonus_or_agent_name_certified'] is False
    assert selected['limits']['Chicago_development_schedule_exact_dates_certified'] is False
    assert selected['limits']['A05_season_result_or_starting_position_prepaid'] is False
    assert candidates['status'] == 'SIX_CONDITIONAL_DRAFT_CAUSAL_FUNCTIONS_NOT_FINAL_G13'
    cf05, cf06 = candidates['functions'][4:6]
    assert (cf06['id'], cf06['subact'], cf06['next']) == ('A04-CF06','A04-S3','A05-S1')
    assert cf05['changed_state'] == cf06['entry_state']
    assert cf06['choice'] == selected['source_candidate_choices_and_costs']['CF06_choice']
    assert cf06['direct_cost'] == selected['source_candidate_choices_and_costs']['CF06_direct_cost']
    assert cf06['changed_state'] == 'Chicago의 새 속도·역할을 배울 준비를 택하지만 공격·자기관리의 빈틈은 남는다'
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    s3 = next(row for row in cp2['subacts'] if row['id'] == 'A04-S3')
    assert s3['entry_state'] == '프로 계약을 보상으로만 읽음'
    assert s3['choice'] == '표준계약의 보상만 보지 않고 기존 2018 개발 일정과 대표팀 불참 방향의 비용을 받아들인다'
    assert s3['cost'] == '구단 일정과 대표팀 불참'
    assert s3['exit_state'] == '2018 개발 일정에 남음'
    assert '| A04 | 2018 Draft | 시장의 선택 | 12 |' in (root / ACT_MAP).read_text(encoding='utf-8-sig')

    beats = [{
        'id': step['id'], 'classification': step['kind'],
        'action': step['action'], 'observable_result': step['observable_result'],
        'source_path': WORKING,
    } for step in selected['steps'][3:]]
    blueprint = {
        'schema': 'A04_CF06_SUMMER_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_FICTIONAL_TIME_ALLOCATION_WITH_APPROVED_AG_NONPARTICIPATION',
        'entry_state': previous['exit_state'],
        'single_function': '계약·개발 설명의 미확인 항목을 안 채 한정된 2018 여름을 Chicago 준비에 쓰고 한국 아시안게임 경로를 추진하지 않는다',
        'unit_choice': cf06['choice'],
        'direct_present_cost': selected['direct_present_cost']['CF06'],
        'exit_state': selected['selected_design_exit_state'],
        'beats': copy.deepcopy(beats),
    }
    return {
        'schema': 'A04_E5_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_NATIONAL_ROSTER_SACRIFICE_OR_FULL_A04',
        'episode_function_id': 'A04-EF-005', 'act': 'A04', 'primary_subact': 'A04-S3',
        'source_conditional_function': 'A04-CF06',
        'final_function_order': previous['final_function_order'] + 1,
        'planned_allocation_slot': previous['planned_allocation_slot'] + 1,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
            'a02_planned_slots': 54, 'a02_locally_assigned_function_slots': 10,
            'a03_planned_slots': 54, 'a03_locally_assigned_function_slots': 3,
            'a04_planned_slots': 12, 'a04_locally_assigned_function_slots': 5,
            'a04_remaining_planned_slots': 7,
            'total_local_functions_through_this': 27,
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
        'reader_question_at_end': 'Chicago에서 맡을 루키 역할과 남은 공격·자기관리 과제를 실제 수행으로 바꿀 수 있을까',
        'internal_order': ['S1','S2'], 'beats': beats,
        'next_unit': {'id': 'A05-S1', 'status': 'ROOKIE_ROLE_FUNCTION_NOT_EXECUTED',
                      'rookie_minutes_or_starter_right_prepaid': False},
        'approved_direction_and_unselected_details': {
            'Chicago_first_round_rookie_scale_direction': 'APPROVED_CANON_DIRECTION',
            '2018_Asian_Games_nonparticipation': 'APPROVED_CANON_DIRECTION',
            'guaranteed_Korea_roster_place_surrendered': False,
            'exact_Chicago_schedule_or_draft_pick_certified': False,
            'signed_UPC_or_medical_certified': False,
        },
        'original_CP2_S3_contract_reward_only_belief_inherited_as_observed': False,
        'information_access': {
            'pov': 'PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'may_know': ['자기가 선택한 Chicago 준비와 한국 AG경로 미추진',
                         '앞서 직접 받은 일반 준비 설명 및 미확인 항목'],
            'cannot_know': ['보장된 국가대표 선발 결과', '정확 Chicago 개발 일정·공식 명단·첫 출전',
                            '구단 비공개 평가·정확 지명 순번·의료 결과'],
            'real_team_or_national_staff_dialogue': None,
        },
        'verification_limits': [
            'ACTUAL_VERIFIED means source-current fictional time choice under an already approved Chicago and AG direction.',
            'The protagonist foregoes pursuing a possible national-team route, not an awarded national-team place.',
            'A choice to prepare does not certify a signed contract, exact schedule, NBA role, minutes, or later season outcome.',
        ],
        'whole_A04_S3_exit_certified': False, 'whole_A04_act_exit_certified': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'g15_complete': False, 'g16_complete': False,
        'g17_complete': False, 'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {path: norm_sha((root / path).read_bytes()) for path in SOURCES},
    }


def render(data):
    lines = [
        '# A04 다섯 번째 국소 기능 — 여름 시간의 선택', '',
        '**범위:** 원고가 아닌 기능표 1건. CF06의 시간 선택만 다루며 국가대표 확정 자리를 양보한 사건이나 정확 구단 일정이 아니다.', '',
        f"- 상태: `{data['status']}` / 국소 출처현재성 `{data['local_blueprint']['status']}`",
        f"- 전역 기능 {data['final_function_order']}, A04 계획 슬롯 {data['planned_allocation_slot']} (출판 번호 아님)",
        f"- E4 정확 진입: {data['entry_state']}",
        f"- 선택: {data['unit_choice']}",
        f"- 직접 비용: {data['direct_present_cost']}", '',
        '| 단계 | 직접 행동 | 관측·권한 한계 |', '| --- | --- | --- |',
    ]
    for beat in data['beats']:
        lines.append(f"| {beat['id']} | {beat['action']} | {beat['observable_result']} |")
    lines += [
        '', f"- 정확 출구: {data['exit_state']}",
        f"- 다음 독자 질문: {data['reader_question_at_end']}",
        '- Chicago 개발 준비와 AG 불참 방향은 승인됐지만 정확 날짜·명단·서명·첫 시즌 성과는 미인증이다. 원 CP2의 계약을 보상으로만 읽는 잠정 심리는 현행 진입에 상속하지 않는다.',
        '- 전체 A04-S3/Act·G13/G14·실제 Pack·원고는 미완료이고 게이트 `CLOSED`다.', '',
    ]
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A04 E5 differs from source-bound reviewed summer choice']


def self_test(data, root=ROOT):
    cases = [
        ('national-team roster sacrifice', lambda x: x['approved_direction_and_unselected_details'].update(guaranteed_Korea_roster_place_surrendered=True)),
        ('signed UPC prepaid', lambda x: x['approved_direction_and_unselected_details'].update(signed_UPC_or_medical_certified=True)),
        ('exact schedule prepaid', lambda x: x['approved_direction_and_unselected_details'].update(exact_Chicago_schedule_or_draft_pick_certified=True)),
        ('NBA minutes prepaid', lambda x: x['next_unit'].update(rookie_minutes_or_starter_right_prepaid=True)),
        ('E4 full entry shortened', lambda x: x.update(entry_state='Chicago 입단을 즉시 주전으로 읽음')),
        ('cost erased', lambda x: x.update(direct_present_cost='')),
    ]
    for name, mutation in cases:
        changed = copy.deepcopy(data)
        mutation(changed)
        assert validate(changed, root), name
    original_load = load
    for name, path, mutation in [
        ('E4 exit changed to contract', PREVIOUS,
         lambda x: x.update(exit_state='이미 UPC 서명과 주전 등록이 끝났다')),
        ('working S1 becomes guaranteed roster surrender', WORKING,
         lambda x: x['steps'][3].update(guaranteed_Korea_roster_place_relinquished=True)),
        ('same-ID CF06 choice becomes AG play', CANDIDATES,
         lambda x: x['functions'][5].update(choice='2018 아시안게임 한국대표팀 출전을 선택한다')),
        ('CP2 S3 exit becomes NBA title', CP2,
         lambda x: next(row for row in x['subacts'] if row['id'] == 'A04-S3').update(exit_state='첫 NBA 우승을 확정')),
    ]:
        def altered(root, requested, path=path, mutation=mutation):
            source = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                source = copy.deepcopy(source)
                mutation(source)
            return source
        with patch(__name__ + '.load', side_effect=altered):
            assert validate(data, root), name
    return len(cases) + 4


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
