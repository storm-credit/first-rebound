"""Build A03's third local function from the reviewed Texas Tech role test."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a03_e2_final_episode_function as previous_builder
import build_a03_cf03_tournament_role_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A03_E3_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = OUTPUT.with_suffix('.md')
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
WORKING = str(working_builder.OUTPUT).replace('\\', '/')
CANDIDATES = 'design/A03_CONDITIONAL_EPISODE_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
ACT_MAP = 'design/ACT_MAP.md'
SOURCES = ('tools/build_a03_e3_final_episode_function.py', PREVIOUS, WORKING,
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
    assert previous == working_builder.load(root, previous_builder.OUTPUT), 'E2 differs from CF03 validation input'
    assert not working_builder.validate(selected, root=root), 'CF03 must be source-current'
    assert previous['episode_function_id'] == 'A03-EF-002'
    assert previous['final_function_order'] == 21 and previous['planned_allocation_slot'] == 92
    assert previous['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE'
    assert previous['next_unit']['id'] == 'A03-F03'
    assert previous['next_unit']['Texas_Tech_result_or_exact_box_prepaid'] is False
    assert previous['whole_A03_act_exit_certified'] is False
    assert selected['status'] == 'SELECTED_ROUTINE_FICTIONAL_TOURNAMENT_ROLE_INDEPENDENTLY_REVIEWED'
    assert selected['independent_review_completed'] is True
    assert selected['previous_exact_full_exit'] == previous['exit_state']
    assert selected['source_function_id'] == 'A03-F03'
    assert [beat['id'] for beat in selected['fictional_action_sequence']] == ['T1', 'T2', 'T3']
    assert selected['fictional_action_sequence'][1]['official_rebound_awarded_to_protagonist'] is False
    assert selected['fictional_action_sequence'][1]['paschall14_or_cosby7_event_level_preservation_proved'] is False
    assert selected['candidate_changed_state_verified_on_march25'] is False
    assert selected['march25_texas_tech_game_is_national_title_game'] is False
    assert selected['later_title_and_pro_evaluation_bridge']['status'] == 'OUTSIDE_THIS_LOCAL_MODEL_NOT_EXECUTED'
    assert selected['preservation_targets_not_certifications']['alternate_event_level_box_or_score_verified'] is False
    assert selected['limits']['F03_final_episode_function_completed_here'] is False
    assert selected['limits']['whole_A03_S3_or_A03_act_exit_certified'] is False
    assert candidates['status'] == 'THREE_CONDITIONAL_FUNCTIONS_NOT_FINAL_G13'
    f03 = candidates['functions'][2]
    assert (f03['id'], f03['subact'], f03['next']) == ('A03-F03', 'A03-S3', 'A04-S1')
    assert f03['choice'] == selected['unit_choice'] == '맡은 상대의 박스아웃과 스위치 연결을 먼저 수행'
    assert f03['cost'] == '전국 무대에서도 개인 공격 표본을 극대화하지 못해 NBA 자가 창조 질문이 남음'
    assert f03['changed_state'] == selected['candidate_changed_state_as_later_target']
    assert f03['status'] == 'CONDITIONAL_EPISODE_FUNCTION_CANDIDATE'
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    s3 = next(row for row in cp2['subacts'] if row['id'] == 'A03-S3')
    assert s3['choice'] == '토너먼트의 결정적 개인 공로를 요구하지 않고 맡은 좁은 역할을 수행한 근거를 프로 평가에 넘긴다'
    assert s3['cost'] == '자기 기록 우선권'
    assert s3['exit_state'] == 'NCAA 우승 기능과 프로 평가를 분리'
    assert '| A03 | 2017–18 | 맡은 역할의 크기 | 54 |' in source_bytes(root, ACT_MAP).decode('utf-8-sig')

    beats = [{
        'id': 'T0', 'classification': selected['official_vs_fictional_window']['classification'],
        'action': selected['official_vs_fictional_window']['fictional_selection'],
        'observable_result': selected['official_vs_fictional_window']['information_access'],
        'source_path': WORKING,
        'not_claimed': '실제 2018 교체 시각·포제션·변경된 71–59 결과',
    }]
    for beat in selected['fictional_action_sequence']:
        beats.append({
            'id': beat['id'], 'classification': beat['classification'],
            'action': beat.get('choice', beat.get('action', beat.get('direct_present_cost'))),
            'observable_result': beat['observable_result'], 'source_path': WORKING,
            'not_claimed': ('공식 개인 기록·PBP·동료 내면·NBA 비공개 평점'
                            if beat['id'] != 'T3' else '프로 평가 결론·자기 공격 완성'),
        })
    blueprint = {
        'schema': 'A03_F03_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_FICTIONAL_ELEVEN_MINUTE_ROLE_CHOICE_NOT_REAL_GAME_EVENT_CERTIFICATION',
        'entry_state': previous['exit_state'],
        'single_function': selected['single_function'],
        'unit_choice': selected['unit_choice'],
        'direct_present_cost': selected['direct_present_cost'],
        'exit_state': selected['selected_design_exit_state'],
        'beats': copy.deepcopy(beats),
    }
    return {
        'schema': 'A03_E3_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_A03_S3_OR_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A03-EF-003', 'act': 'A03', 'primary_subact': 'A03-S3',
        'source_conditional_function': 'A03-F03',
        'final_function_order': previous['final_function_order'] + 1,
        'planned_allocation_slot': previous['planned_allocation_slot'] + 1,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
            'a02_planned_slots': 54, 'a02_locally_assigned_function_slots': 10,
            'a03_planned_slots': 54, 'a03_locally_assigned_function_slots': 3,
            'a03_remaining_planned_slots': 51,
            'total_local_functions_through_this': 22,
            'allocation_is_final_published_episode_count': False,
            'A03_slot_per_subact_uniform_distribution_certified': False,
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
        'reader_question_at_end': '이 한 번의 좁은 수비 기여를 프로 평가에서 개인 공격 능력의 증명과 어떻게 구분할 것인가',
        'internal_order': ['T0', 'T1', 'T2', 'T3'], 'beats': beats,
        'next_unit': {
            'id': 'A04-S1', 'status': 'AFTER_SEPARATE_POST_GAME_TITLE_AND_EVALUATION_HISTORY_BRIDGE_NOT_EXECUTED',
            'March25_title_or_season_end_evaluation_completed': False,
            'candidate_changed_state_verified_in_this_function': False,
        },
        'source_candidate_changed_state_as_later_target': selected['candidate_changed_state_as_later_target'],
        'source_candidate_changed_state_verified_here': False,
        'information_access': copy.deepcopy(selected['information_access']),
        'verification_limits': [
            'ACTUAL_VERIFIED means current local source/design consistency, not a certified historical possession or alternate 2018 box.',
            'The Villanova 71–59 Texas Tech result and Paschall 14/Cosby-Roundtree 7 rebounds are actual box facts and fictional preservation targets; this action has no proven alternate event attribution.',
            'A teammate securing one ball is a selected fictional local observation, not a newly verified official rebound or all-team trust.',
            'Earlier permitted practice repetition does not guarantee tournament execution or an NBA offensive skill sample.',
            'The source candidate’s team-championship-vs-pro-evaluation separation requires a later history and season-end bridge. No March 25 title, full team contribution, private scouting grade or A04 action is prepaid.',
        ],
        'bounded_A03_S3_role_choice_observed': True,
        'whole_A03_S3_exit_certified': False, 'whole_A03_act_exit_certified': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'g15_complete': False, 'g16_complete': False,
        'g17_complete': False, 'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {path: norm_sha(source_bytes(root, path)) for path in SOURCES},
    }


def render(data):
    rows = [
        '# A03 세 번째 국소 기능 — Texas Tech전 역할 선택', '',
        '**범위:** 원고가 아닌 기능표 1건. 공식 경기 박스·가상 11분 시간표를 분리한 뒤, 좁은 수비 선택과 동료 공 확보 한 번만 이번 기능의 관측 출구로 둔다.', '',
        f"- 상태: `{data['status']}` / 출처현재성 `{data['local_blueprint']['status']}`",
        f"- 전역 기능 {data['final_function_order']}, A03 계획 슬롯 {data['planned_allocation_slot']} (공개 회차 번호 아님)",
        f"- 정확 진입: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- 선택: {data['unit_choice']}",
        f"- 직접 비용: {data['direct_present_cost']}", '',
        '| 단계 | 행동 | 직접 보이는 결과 또는 접근 한계 |', '| --- | --- | --- |',
    ]
    for beat in data['beats']:
        rows.append(f"| {beat['id']} | {beat['action']} | {beat['observable_result']} |")
    rows += [
        '', f"- 이번 출구: {data['exit_state']}",
        f"- 다음 독자 질문: {data['reader_question_at_end']}",
        '- Villanova 71–59 Texas Tech와 Paschall 14·Cosby-Roundtree 7리바운드는 역사 박스 및 보존 목표다. 가상 동료 공 확보를 실제 포제션에 대입하거나 개인 기록·대체 승패로 인증하지 않는다.',
        '- 원 F03 후보의 우승팀 기여와 NBA 공격 능력 분리는 이후 역사·시즌 후 평가 인계의 목표다. 3월 25일 전국 우승·전체 공로·스카우트 판단을 이번 출구에 포함하지 않는다.',
        '- 계획 슬롯 93은 새 공개 93화나 54개 A03 사건 의무가 아니다. 대표 기능3 상한 유지, 전체 A03-S3/Act/G13/G14·실제 Pack·원고 미완료, 게이트 `CLOSED`.', '',
    ]
    return '\n'.join(rows)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A03 E3 differs from source-bound reviewed tournament model']


def self_test(data, root=ROOT):
    changes = [
        ('March 25 title prepaid', lambda x: x['next_unit'].update(March25_title_or_season_end_evaluation_completed=True)),
        ('whole S3 prepaid', lambda x: x.update(whole_A03_S3_exit_certified=True)),
        ('candidate changed state prepaid', lambda x: x.update(source_candidate_changed_state_verified_here=True)),
        ('official box equivalence inserted', lambda x: x['verification_limits'].append('Alternate box and real possession proven.')),
        ('slot inflation', lambda x: x['slot_accounting'].update(a03_locally_assigned_function_slots=54)),
        ('teammate observation omitted', lambda x: x['beats'].pop(2)),
    ]
    for name, mutate in changes:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed, root), name
    original_load = load
    for name, path, mutate in [
        ('E2 full exit replaced', PREVIOUS,
         lambda x: x.update(exit_state='훈련으로 Texas Tech전 전체 승리와 공격 숙련을 이미 증명했다')),
        ('CF03 local cost replaced', WORKING,
         lambda x: x.update(direct_present_cost='정확 NBA 공격 등급과 스카우트 보증을 얻었다')),
        ('CP2 S3 exit changed to title already done', CP2,
         lambda x: next(row for row in x['subacts'] if row['id'] == 'A03-S3').update(exit_state='Texas Tech전 당일 전국 우승')),
    ]:
        def altered(root, requested, path=path, mutate=mutate):
            source = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                source = copy.deepcopy(source)
                mutate(source)
            return source
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
