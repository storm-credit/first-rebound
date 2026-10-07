"""Build A04's second local function from reviewed personal measurement preparation."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a04_e1_final_episode_function as previous_builder
import build_a04_cf02_measurement_preparation_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A04_E2_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = OUTPUT.with_suffix('.md')
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
WORKING = str(working_builder.OUTPUT).replace('\\', '/')
CANDIDATES = 'design/A04_DRAFT_CONDITIONAL_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
ACT_MAP = 'design/ACT_MAP.md'
SOURCES = ('tools/build_a04_e2_final_episode_function.py', PREVIOUS, WORKING,
           CANDIDATES, CP2, ACT_MAP)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def source_bytes(root, path):
    return (root / path).read_bytes()


def norm_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def build(root=ROOT):
    previous = load(root, PREVIOUS)
    selected = load(root, WORKING)
    candidates = load(root, CANDIDATES)
    cp2 = load(root, CP2)
    assert previous == working_builder.load(root, previous_builder.OUTPUT), 'E1 differs from CF02 validation input'
    assert not working_builder.validate(selected, root=root), 'CF02 must be source-current'
    assert previous['episode_function_id'] == 'A04-EF-001'
    assert previous['final_function_order'] == 23 and previous['planned_allocation_slot'] == 145
    assert previous['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE'
    assert previous['next_unit']['id'] == 'A04-CF02'
    assert previous['next_unit']['Combine_invitation_official_measurement_or_pick_prepaid'] is False
    assert previous['cp2_provisional_entry_inherited_as_actual_belief'] is False
    assert previous['whole_A04_S1_exit_certified'] is False
    assert selected['status'] == 'SELECTED_ROUTINE_NONOFFICIAL_MEASUREMENT_PREPARATION_INDEPENDENTLY_REVIEWED'
    assert selected['independent_review_completed'] is True
    assert selected['previous_exact_full_exit'] == previous['exit_state']
    assert selected['source_function_id'] == 'A04-CF02'
    assert [step['id'] for step in selected['actions']] == ['M1', 'M2', 'M3']
    assert selected['actions'][0]['candidate_ranges_copied_as_personal_results'] is False
    assert selected['actions'][1]['official_measurement_value'] is None
    assert selected['actions'][1]['actual_medical_clearance'] is None
    assert selected['actions'][1]['real_scout_or_team_staff_present'] is False
    assert selected['next_candidate']['id'] == 'A04-CF03'
    assert selected['next_candidate']['team_workout_live_defender_or_success_prepaid'] is False
    assert selected['limits']['official_combine_invitation_or_participation_certified'] is False
    assert selected['limits']['official_height_reach_jump_sprint_agility_results_certified'] is False
    assert selected['limits']['medical_clearance_or_club_grade_certified'] is False
    assert selected['limits']['exact_pick_22_or_Hutchison_reassignment_selected'] is False
    assert candidates['status'] == 'SIX_CONDITIONAL_DRAFT_CAUSAL_FUNCTIONS_NOT_FINAL_G13'
    cf02 = candidates['functions'][1]
    assert (cf02['id'], cf02['subact'], cf02['next']) == ('A04-CF02', 'A04-S1', 'A04-CF03')
    assert cf02['choice'] == selected['actions'][2]['choice']
    assert cf02['direct_cost'] == '자신이 고른 동작을 더 연습할 시간을 측정 항목·절차를 확인하는 준비에 쓴다'
    assert cf02['changed_state'] == '평가에 낼 영상 준비에서 몸의 장점과 약점도 드러낼 절차 준비로 시간을 옮긴다'
    assert cf02['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    s1 = next(row for row in cp2['subacts'] if row['id'] == 'A04-S1')
    assert s1['choice'] == '신체 측정으로 순번을 단정하지 않고 준비한 기술의 가능한 범위와 한계를 평가에 내놓는다'
    assert s1['cost'] == '불확실한 평가 수용'
    assert s1['exit_state'] == '보여줄 기술 표본 명확화'
    assert '| A04 | 2018 Draft | 시장의 선택 | 12 |' in source_bytes(root, ACT_MAP).decode('utf-8-sig')

    beats = []
    for step in selected['actions']:
        beats.append({
            'id': step['id'], 'classification': step['type'],
            'action': step.get('choice', step.get('action')),
            'observable_result': step['observable_result'],
            'source_path': WORKING,
            'not_claimed': ('공식 NBA 초청·측정·의료 결과·비공개 구단 보드'
                            if step['id'] != 'M3' else '확정 22순위·공식 워크아웃·공격 기술 완성'),
        })
    blueprint = {
        'schema': 'A04_CF02_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_NONOFFICIAL_PERSONAL_PREPARATION_NOT_NBA_MEASUREMENT',
        'entry_state': previous['exit_state'],
        'single_function': '자기 역할·공격 과제 자료 옆에 신체 항목의 빈칸을 두고 숫자 없는 개인 움직임 예행으로 평가의 불확실성을 준비한다',
        'unit_choice': cf02['choice'],
        'direct_present_cost': selected['direct_present_cost'],
        'exit_state': selected['selected_design_exit_state'],
        'beats': copy.deepcopy(beats),
    }
    return {
        'schema': 'A04_E2_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_A04_S1_OR_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A04-EF-002', 'act': 'A04', 'primary_subact': 'A04-S1',
        'source_conditional_function': 'A04-CF02',
        'final_function_order': previous['final_function_order'] + 1,
        'planned_allocation_slot': previous['planned_allocation_slot'] + 1,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
            'a02_planned_slots': 54, 'a02_locally_assigned_function_slots': 10,
            'a03_planned_slots': 54, 'a03_locally_assigned_function_slots': 3,
            'a04_planned_slots': 12, 'a04_locally_assigned_function_slots': 2,
            'a04_remaining_planned_slots': 10,
            'total_local_functions_through_this': 24,
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
        'reader_question_at_end': '몸의 장점을 공식 평가에 올려도 미완성 공격의 차이가 어디서 다시 드러날 것인가',
        'internal_order': ['M1', 'M2', 'M3'], 'beats': beats,
        'next_unit': {'id': 'A04-CF03', 'status': 'WORKOUT_SKILL_GAP_CONDITIONAL_NOT_EXECUTED',
                      'official_workout_or_live_defender_success_prepaid': False},
        'bounded_A04_S1_preparation_audit': {
            'status': 'PRIVATE_SAMPLE_AND_UNMEASURED_BODY_CATEGORY_PREPARATION_OBSERVED',
            'E1_role_evidence_vs_offense_gap_separated': True,
            'E2_body_categories_vs_basketball_skill_and_authority_separated': True,
            'CP2_showable_skill_sample_clarified_as_personal_preparation': True,
            'actual_sample_sent_to_evaluator_or_official_measurement_certified': False,
            'full_CP2_exit_or_Act_completion_inferred_from_private_rehearsal': False,
        },
        'information_access': copy.deepcopy(selected['information_access']),
        'verification_limits': [
            'ACTUAL_VERIFIED means current local fictional preparation, not official NBA Combine, a measurement result or medical clearance.',
            'E1 and E2 satisfy the bounded preparation question of what role proof, offensive failure and physical categories could be presented; no evaluator receipt or measured result is claimed.',
            'The Pick 22 research’s numeric ranges remain NOT_CANON; exact pick, Hutchison path and Chicago private board are unselected.',
            'A personal straight start or lateral rehearsal does not certify basketball BQ, live offensive success or the later elbow/live-pass counter.',
        ],
        'bounded_A04_S1_preparation_criterion_observed': True,
        'whole_A04_S1_exit_certified': False, 'whole_A04_act_exit_certified': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'g15_complete': False, 'g16_complete': False,
        'g17_complete': False, 'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {path: norm_sha(source_bytes(root, path)) for path in SOURCES},
    }


def render(data):
    lines = [
        '# A04 두 번째 국소 기능 — 측정 질문의 빈칸', '',
        '**범위:** 원고가 아닌 기능표 1건. E1의 역할/공격 구분에 숫자 없는 신체 항목과 개인 예행을 잇는다. 실제 Combine이나 의료·구단 평가가 아니다.', '',
        f"- 상태: `{data['status']}` / 출처현재성 `{data['local_blueprint']['status']}`",
        f"- 전역 기능 {data['final_function_order']}, A04 계획 슬롯 {data['planned_allocation_slot']} (출판 번호 아님)",
        f"- 정확 진입: {data['entry_state']}",
        f"- 선택: {data['unit_choice']}",
        f"- 직접 비용: {data['direct_present_cost']}", '',
        '| 단계 | 행동 | 직접 결과·권한 한계 |', '| --- | --- | --- |',
    ]
    for beat in data['beats']:
        lines.append(f"| {beat['id']} | {beat['action']} | {beat['observable_result']} |")
    lines += [
        '', f"- 정확 출구: {data['exit_state']}",
        f"- 다음 독자 질문: {data['reader_question_at_end']}",
        '- E1의 역할 증거/공격 미검증 구분과 E2의 신체 항목/농구 능력 구분은 A04-S1의 **개인 준비** 질문에 필요한 좁은 관측이다. 실제 평가기관에 자료를 제출했거나 공식 측정으로 지명 순번을 받았다는 뜻은 아니다.',
        '- CF03 워크아웃, 전체 A04-S1/Act, G13/G14·실제 Pack·원고는 미완료이고 게이트 `CLOSED`다.', '',
    ]
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A04 E2 differs from source-bound reviewed personal preparation']


def self_test(data, root=ROOT):
    changes = [
        ('whole S1 prepaid', lambda x: x.update(whole_A04_S1_exit_certified=True)),
        ('official result prepaid', lambda x: x['bounded_A04_S1_preparation_audit'].update(actual_sample_sent_to_evaluator_or_official_measurement_certified=True)),
        ('official workout prepaid', lambda x: x['next_unit'].update(official_workout_or_live_defender_success_prepaid=True)),
        ('numeric result fabricated', lambda x: x['beats'][1].update(observable_result='107cm official Combine vertical')),
        ('cost erased', lambda x: x.update(direct_present_cost='')),
        ('all plan slots used', lambda x: x['slot_accounting'].update(a04_locally_assigned_function_slots=12)),
    ]
    for name, mutate in changes:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed, root), name
    original_load = load
    for name, path, mutate in [
        ('E1 exact exit flipped', PREVIOUS,
         lambda x: x.update(exit_state='공식 측정 1위와 22순위를 얻었다')),
        ('CF02 source medical result prepaid', WORKING,
         lambda x: x['actions'][1].update(actual_medical_clearance=True)),
        ('CP2 S1 exit made exact pick', CP2,
         lambda x: next(row for row in x['subacts'] if row['id'] == 'A04-S1').update(exit_state='Chicago 22순위 확정')),
    ]:
        def altered(root, requested, path=path, mutate=mutate):
            src = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                src = copy.deepcopy(src)
                mutate(src)
            return src
        with patch(__name__ + '.load', side_effect=altered):
            assert validate(data, root), name
    return len(changes) + 3


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
