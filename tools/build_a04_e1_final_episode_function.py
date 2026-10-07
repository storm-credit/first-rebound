"""Build A04's first local function from the reviewed draft sample preparation."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a03_e3_final_episode_function as previous_builder
import build_a04_cf01_draft_sample_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A04_E1_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = OUTPUT.with_suffix('.md')
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
WORKING = str(working_builder.OUTPUT).replace('\\', '/')
BRIDGE = 'design/A03_POST_TOURNAMENT_HISTORY_BRIDGE_2026_10_07.json'
CANDIDATES = 'design/A04_DRAFT_CONDITIONAL_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
ACT_MAP = 'design/ACT_MAP.md'
SOURCES = ('tools/build_a04_e1_final_episode_function.py', PREVIOUS, WORKING,
           BRIDGE, CANDIDATES, CP2, ACT_MAP)


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
    bridge = load(root, BRIDGE)
    candidates = load(root, CANDIDATES)
    cp2 = load(root, CP2)
    assert previous == working_builder.load(root, previous_builder.OUTPUT), 'E3 differs from CF01 validation input'
    assert bridge == working_builder.load(root, BRIDGE), 'bridge differs from CF01 validation input'
    assert not working_builder.validate(selected, root=root), 'CF01 must be source-current'
    assert previous['episode_function_id'] == 'A03-EF-003'
    assert previous['final_function_order'] == 22 and previous['planned_allocation_slot'] == 93
    assert previous['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE'
    assert previous['whole_A03_S3_exit_certified'] is False
    assert previous['next_unit']['id'] == 'A04-S1'
    assert previous['next_unit']['March25_title_or_season_end_evaluation_completed'] is False
    assert bridge['previous_function']['exact_full_exit'] == previous['exit_state']
    assert bridge['official_public_sequence'][1]['date'] == '2018-03-31'
    assert bridge['official_public_sequence'][2]['date'] == '2018-04-02'
    assert bridge['limits']['alternate_Kansas_or_Michigan_win_mechanically_reproved'] is False
    assert selected['status'] == 'SELECTED_ROUTINE_DRAFT_SAMPLE_PREPARATION_INDEPENDENTLY_REVIEWED'
    assert selected['independent_review_completed'] is True
    assert selected['previous_exact_full_exit'] == previous['exit_state']
    assert selected['public_history_bridge_path'] == BRIDGE
    assert selected['source_function_id'] == 'A04-CF01'
    assert selected['cp2_provisional_entry_inherited_as_observed_belief'] is False
    assert selected['source_candidate_entry_used_as_certified_actual_state'] is False
    assert [step['id'] for step in selected['actions']] == ['D1', 'D2', 'D3']
    assert selected['actions'][0]['actual_Texas_Tech_PBP_clip_or_official_personal_stat_certified'] is False
    assert selected['actions'][1]['official_combine_or_team_workout'] is False
    assert selected['actions'][1]['shot_make_or_live_defender_success_assigned'] is False
    assert selected['next_candidate']['id'] == 'A04-CF02'
    assert selected['next_candidate']['official_combine_invitation_measurement_or_pick_prepaid'] is False
    assert selected['limits']['exact_pick_22_author_locked_or_selected'] is False
    assert selected['limits']['later_elbow_or_live_pass_counter_prepaid'] is False
    assert selected['limits']['first_A04_final_episode_function_completed'] is False
    assert candidates['status'] == 'SIX_CONDITIONAL_DRAFT_CAUSAL_FUNCTIONS_NOT_FINAL_G13'
    cf01 = candidates['functions'][0]
    assert (cf01['id'], cf01['subact'], cf01['next']) == ('A04-CF01', 'A04-S1', 'A04-CF02')
    assert cf01['choice'] == selected['actions'][2]['choice']
    assert cf01['changed_state'] == '보여 줄 역할 증거와 새 평가에서 시험할 기술 과제가 구분된다'
    assert cf01['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    s1 = next(row for row in cp2['subacts'] if row['id'] == 'A04-S1')
    assert s1['entry_state'] == selected['cp2_provisional_entry'] == '신체 측정만으로 순번을 확신'
    assert s1['choice'] == '신체 측정으로 순번을 단정하지 않고 준비한 기술의 가능한 범위와 한계를 평가에 내놓는다'
    assert s1['exit_state'] == '보여줄 기술 표본 명확화'
    assert '| A04 | 2018 Draft | 시장의 선택 | 12 |' in source_bytes(root, ACT_MAP).decode('utf-8-sig')

    beats = [{
        'id': 'H0', 'classification': 'PUBLIC_POST_GAME_HISTORY_CONTEXT_NOT_NEW_PROTAGONIST_GAME_ACTION',
        'action': 'After their respective games, the public Kansas semifinal and Michigan championship results can enter the protagonist’s preparation context.',
        'observable_result': 'Villanova team title is public; the protagonist’s changed Final Four minutes, boxes and individual core credit are not assigned.',
        'source_path': BRIDGE,
        'not_claimed': '새 대표 경기·대체 역사 승패 기계검증·우승 핵심 공로',
    }]
    for step in selected['actions']:
        beats.append({
            'id': step['id'], 'classification': step['type'],
            'action': step.get('choice', step.get('action')),
            'observable_result': step['observable_result'],
            'source_path': WORKING,
            'not_claimed': ('공식 Texas Tech 개인 박스·실존 스카우트 평가'
                            if step['id'] == 'D1' else '실제 Combine·측정·팀 워크아웃·정확 지명'),
        })
    blueprint = {
        'schema': 'A04_CF01_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_PRIVATE_FICTIONAL_SAMPLE_PREPARATION_NOT_REAL_SCOUT_DECISION',
        'entry_state': previous['exit_state'],
        'entry_after_public_history_bridge': selected['operating_entry'],
        'source_CP2_provisional_entry_not_inherited': selected['cp2_provisional_entry'],
        'single_function': selected['one_function'],
        'unit_choice': cf01['choice'],
        'direct_present_cost': selected['direct_present_cost'],
        'exit_state': selected['selected_design_exit_state'],
        'beats': copy.deepcopy(beats),
    }
    return {
        'schema': 'A04_E1_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_A04_S1_OR_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A04-EF-001', 'act': 'A04', 'primary_subact': 'A04-S1',
        'source_conditional_function': 'A04-CF01',
        'final_function_order': previous['final_function_order'] + 1,
        'planned_allocation_slot': 145,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
            'a02_planned_slots': 54, 'a02_locally_assigned_function_slots': 10,
            'a03_planned_slots': 54, 'a03_locally_assigned_function_slots': 3,
            'a04_planned_slots': 12, 'a04_locally_assigned_function_slots': 1,
            'a04_remaining_planned_slots': 11,
            'total_local_functions_through_this': 23,
            'unassigned_plan_slots_are_not_mandatory_new_events': True,
            'allocation_is_final_published_episode_count': False,
            'A04_slot_per_subact_uniform_distribution_certified': False,
        },
        'final_episode_functions_completed_this_record': 1,
        'previous_function': {'id': previous['episode_function_id'], 'source_path': PREVIOUS,
                              'exact_full_exit': previous['exit_state']},
        'public_history_bridge': {'path': BRIDGE,
                                  'public_results_after_games_only': True,
                                  'fictional_Final_Four_game_actions_or_alternate_box_certified': False},
        'local_blueprint': blueprint,
        'single_function': blueprint['single_function'],
        'entry_state': blueprint['entry_state'],
        'entry_after_public_history_bridge': blueprint['entry_after_public_history_bridge'],
        'cp2_provisional_entry_inherited_as_actual_belief': False,
        'unit_choice': blueprint['unit_choice'],
        'exit_state': blueprint['exit_state'],
        'direct_present_cost': blueprint['direct_present_cost'],
        'reader_question_at_end': '몸의 장점이 남은 개인 공격 표본의 빈칸을 어디까지 메울 수 있는가',
        'internal_order': ['H0', 'D1', 'D2', 'D3'], 'beats': beats,
        'next_unit': {'id': 'A04-CF02', 'status': 'MEASUREMENT_PREPARATION_CONDITIONAL_NOT_EXECUTED',
                      'Combine_invitation_official_measurement_or_pick_prepaid': False},
        'information_access': copy.deepcopy(selected['information_access']),
        'verification_limits': [
            'ACTUAL_VERIFIED means reviewed source-current fictional preparation, not an actual scout, agent, medical or club decision.',
            'The CP2 sentence about certainty from physical measurements is provisional source wording and not the selected protagonist’s current belief.',
            'The public title follows the March 31 and April 2 actual games; E3’s March 25 local role choice is not a national-title game or an alternate Final Four box certification.',
            'The one-dribble corner attempt retains a visible stopping point; it is not a made shot, live-defender win, NBA-ready self-creation, later elbow or live-pass counter.',
            'Chicago first-round direction is retained while exact pick 22, measurements, private board, Hutchison placement and contract details remain HOLD.',
        ],
        'bounded_A04_S1_sample_split_observed': True,
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
        '# A04 첫 국소 기능 — 드래프트 표본의 범위', '',
        '**범위:** 원고가 아닌 기능표 1건. A03 E3의 정확 출구와 이후 공개 우승 결과를 분리하고, 개인 준비의 역할 증거·공격 빈칸을 한 행동으로 정리한다.', '',
        f"- 상태: `{data['status']}` / 출처현재성 `{data['local_blueprint']['status']}`",
        f"- 전역 기능 {data['final_function_order']}, A04 계획 슬롯 {data['planned_allocation_slot']} (출판 회차 아님)",
        f"- 직전 정확 출구 = 이번 원진입: {data['entry_state']}",
        f"- 공개 역사 뒤 작업 진입: {data['entry_after_public_history_bridge']}",
        '- CP2 잠정 신체측정 확신은 현재 주인공의 실제 믿음으로 채택하지 않는다.',
        f"- 한 기능: {data['single_function']}",
        f"- 선택: {data['unit_choice']}",
        f"- 직접 비용: {data['direct_present_cost']}", '',
        '| 단계 | 행동 | 직접 결과·접근 한계 |', '| --- | --- | --- |',
    ]
    for beat in data['beats']:
        lines.append(f"| {beat['id']} | {beat['action']} | {beat['observable_result']} |")
    lines += [
        '', f"- 정확 출구: {data['exit_state']}",
        f"- 다음 독자 질문: {data['reader_question_at_end']}",
        '- 개인 자료카드와 코너 캐치·한 드리블 실패 지점은 허용된 가상 준비다. 공식 Combine·팀 워크아웃·실존 스카우트/에이전트·의료·측정·정확 22순위·계약 인증이 아니다.',
        '- 계획 슬롯 145와 전역 기능 23은 출판 번호나 780개 새 사건 의무가 아니다. CF02·A04-S1/Act 전체·G13/G14·Pack·원고 미완료, 게이트 `CLOSED`.', '',
    ]
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A04 E1 differs from source-bound reviewed sample preparation']


def self_test(data, root=ROOT):
    mutations = [
        ('CP2 certainty inherited', lambda x: x.update(cp2_provisional_entry_inherited_as_actual_belief=True)),
        ('bridge treated as alternate box', lambda x: x['public_history_bridge'].update(fictional_Final_Four_game_actions_or_alternate_box_certified=True)),
        ('official measurement prepaid', lambda x: x['next_unit'].update(Combine_invitation_official_measurement_or_pick_prepaid=True)),
        ('whole S1 prepaid', lambda x: x.update(whole_A04_S1_exit_certified=True)),
        ('remove failure beat', lambda x: x['beats'].pop(2)),
        ('slot inflation', lambda x: x['slot_accounting'].update(a04_locally_assigned_function_slots=12)),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed, root), name
    original_load = load
    for name, path, mutate in [
        ('E3 full exit swapped', PREVIOUS,
         lambda x: x.update(exit_state='Texas Tech전 전체박스와 NBA 자가창조를 완성했다')),
        ('CF01 failed attempt made perfect', WORKING,
         lambda x: x['actions'][1].update(observable_result='NBA 실전 공격을 완벽하게 증명했다')),
        ('CP2 provisional entry promoted to exact pick', CP2,
         lambda x: next(row for row in x['subacts'] if row['id'] == 'A04-S1').update(entry_state='Chicago 22순위 보장')),
    ]:
        def altered(root, requested, path=path, mutate=mutate):
            src = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                src = copy.deepcopy(src)
                mutate(src)
            return src
        with patch(__name__ + '.load', side_effect=altered):
            assert validate(data, root), name
    return len(mutations) + 3


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
