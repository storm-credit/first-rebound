"""Build A03's second local function from reviewed role repetition."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a03_e1_final_episode_function as previous_builder
import build_a03_cf02_role_repetition_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A03_E2_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = OUTPUT.with_suffix('.md')
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
WORKING = str(working_builder.OUTPUT).replace('\\', '/')
CANDIDATES = 'design/A03_CONDITIONAL_EPISODE_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
ACT_MAP = 'design/ACT_MAP.md'
SOURCES = ('tools/build_a03_e2_final_episode_function.py', PREVIOUS, WORKING,
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
    assert previous['episode_function_id'] == 'A03-EF-001'
    assert previous['final_function_order'] == 20 and previous['planned_allocation_slot'] == 91
    assert previous['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE'
    assert previous['next_unit']['id'] == 'A03-F02'
    assert previous['next_unit']['success_or_trust_prepaid'] is False
    assert previous['whole_A03_S1_exit_certified'] is False
    assert previous['whole_g13_complete'] is False and previous['manuscript_allowed'] is False
    assert selected['status'] == 'SELECTED_ROUTINE_ROLE_REPETITION_INDEPENDENTLY_REVIEWED'
    assert selected['independent_review_completed'] is True
    assert selected['previous_exact_full_exit'] == previous['exit_state']
    assert selected['source_function_id'] == 'A03-F02'
    assert [step['id'] for step in selected['practice']] == ['P1', 'P2', 'P3']
    assert selected['practice'][1]['individual_stat_or_game_rebound_awarded'] is False
    assert selected['practice'][2]['individual_stat_or_game_rebound_awarded'] is False
    assert selected['next_candidate']['id'] == 'A03-F03'
    assert selected['next_candidate']['Texas_Tech_result_or_200_minute_reconstruction_prepaid'] is False
    assert selected['limits']['actual_Villanova_game_or_practice_film_certified'] is False
    assert selected['limits']['official_minutes_stats_or_start_certified'] is False
    assert selected['limits']['all_teammates_trust_or_private_feelings_certified'] is False
    assert selected['limits']['technical_mastery_or_guaranteed_roster_promotion'] is False
    assert selected['limits']['existing_I3_full_qualifier_revoked'] is False
    assert selected['limits']['A03_S2_whole_exit_or_final_function_completed_here'] is False
    assert candidates['status'] == 'THREE_CONDITIONAL_FUNCTIONS_NOT_FINAL_G13'
    f02 = candidates['functions'][1]
    assert (f02['id'], f02['subact'], f02['next']) == ('A03-F02', 'A03-S2', 'A03-F03')
    assert f02['choice'] == '볼 없는 준비 위치와 박스아웃을 먼저 수행해 동료의 공 확보를 돕는 반복'
    assert f02['cost'] == '자기 리바운드/공격 표본에 남지 않는 노동과 반복 훈련 시간'
    assert f02['status'] == 'CONDITIONAL_EPISODE_FUNCTION_CANDIDATE'
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    s2 = next(row for row in cp2['subacts'] if row['id'] == 'A03-S2')
    assert s2['choice'] == '개인 리바운드 수만 좇지 않고 동료가 공을 잡도록 박스아웃과 볼 없는 준비를 반복한다'
    assert s2['exit_state'] == '동료가 맡기는 수비 기능'
    act_map = source_bytes(root, ACT_MAP).decode('utf-8-sig')
    assert '| A01 | 2015–2016.02 | 농구를 계속할 이유 | 36 |' in act_map
    assert '| A02 | 2016.03–2017.06 | 포지션을 잃는 비용 | 54 |' in act_map
    assert '| A03 | 2017–18 | 맡은 역할의 크기 | 54 |' in act_map

    beats = [
        {'id': 'P1', 'classification': 'REVIEWED_ROUTINE_PRACTICE_ASSIGNMENT',
         'action': selected['practice'][0]['assigned_task'],
         'observable_result': selected['practice'][0]['access'],
         'source_path': WORKING, 'not_claimed': '실제 2017–18 연습·NCAA 학업 판단'},
        {'id': 'P2', 'classification': 'REVIEWED_FIRST_ROLE_REPETITION',
         'action': selected['practice'][1]['choice'],
         'observable_result': selected['practice'][1]['observed_result'],
         'source_path': WORKING, 'not_claimed': '공식 개인 리바운드·팀 전체 신뢰'},
        {'id': 'P3', 'classification': 'REVIEWED_SECOND_ROLE_REPETITION_SAME_PRACTICE',
         'action': selected['practice'][2]['choice'],
         'observable_result': selected['practice'][2]['observed_result'],
         'source_path': WORKING, 'not_claimed': '시즌 안정성·출전 분 상승·기술 숙련'},
    ]
    blueprint = {
        'schema': 'A03_F02_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_TWO_OBSERVED_PRACTICE_REPETITIONS_NOT_REAL_GAME_OR_SEASON_TRUST',
        'entry_state': previous['exit_state'],
        'single_function': '동료가 공을 확보하게 하는 볼 없는 위치·박스아웃을 같은 허용 연습에서 두 번 관측 가능한 선택으로 반복한다',
        'unit_choice': '자기 리바운드 추격보다 맡은 위치·상대 박스아웃과 동료의 공 확보를 우선한다',
        'direct_present_cost': selected['direct_present_cost'],
        'exit_state': selected['selected_design_exit_state'],
        'beats': copy.deepcopy(beats),
    }
    return {
        'schema': 'A03_E2_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A03-EF-002', 'act': 'A03', 'primary_subact': 'A03-S2',
        'source_conditional_function': 'A03-F02',
        'final_function_order': previous['final_function_order'] + 1,
        'planned_allocation_slot': previous['planned_allocation_slot'] + 1,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
                            'a02_planned_slots': 54, 'a02_locally_assigned_function_slots': 10,
                            'a03_planned_slots': 54, 'a03_locally_assigned_function_slots': 2,
                            'a03_remaining_planned_slots': 52,
                            'total_local_functions_through_this': 21,
                            'allocation_is_final_published_episode_count': False,
                            'A03_slot_per_subact_uniform_distribution_certified': False},
        'final_episode_functions_completed_this_record': 1,
        'previous_function': {'id': previous['episode_function_id'], 'source_path': PREVIOUS,
                              'exact_full_exit': previous['exit_state']},
        'local_blueprint': blueprint,
        'single_function': blueprint['single_function'],
        'entry_state': blueprint['entry_state'],
        'unit_choice': blueprint['unit_choice'],
        'exit_state': blueprint['exit_state'],
        'direct_present_cost': blueprint['direct_present_cost'],
        'reader_question_at_end': '이 두 번의 훈련 관측이 토너먼트 압력에서도 같은 역할로 이어질 수 있는가',
        'internal_order': ['P1', 'P2', 'P3'], 'beats': beats,
        'next_unit': {'id': 'A03-F03', 'status': 'TEXAS_TECH_CONDITIONAL_NOT_EXECUTED',
                      'historical_source_and_200_minute_reconstruction_required_before_game_claim': True,
                      'Texas_Tech_result_or_exact_box_prepaid': False},
        'information_access': {'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
                               'may_know': ['자신에게 전달된 다음 허용 훈련의 수비 과제',
                                            '두 공 궤적에서 자기 위치·박스아웃과 동료 공 확보의 직접 관측',
                                            '공을 직접 쫓지 않고 사용한 훈련 시간'],
                               'cannot_know': ['동료 전원의 속마음·비공개 코치 로테이션 평가',
                                               '실제 2017–18 경기 분·공식 박스',
                                               'Texas Tech전 포제션별 개인 기여'],
                               'individual_scene_pov_verified': False, 'exact_dialogue': None},
        'verification_limits': [
            'ACTUAL_VERIFIED means source-current local design, not actual 2017–18 Villanova film, game or private player record.',
            'Two shot-and-rebound cues in one fictional permitted practice are the minimum observed repetition, not two new games or season-long reliability.',
            'Teammate possession in this drill is not an official individual rebound, all-teammate trust, rotation minutes or perfected wing skill.',
            'The selected summer I3 full qualifier and academic duties remain; no new academic-life punishment or eligibility loss is inferred.',
            'Texas Tech is still a source-dependent next candidate; exact 200-minute redistribution and specific box/play-by-play are not selected here.',
        ],
        'bounded_A03_S2_role_basis_observed': True,
        'whole_A03_S2_exit_certified': False, 'whole_A03_act_exit_certified': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'g15_complete': False, 'g16_complete': False,
        'g17_complete': False, 'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {path: norm_sha(source_bytes(root, path)) for path in SOURCES},
    }


def render(data):
    rows = ['# A03 두 번째 국소 기능 — 제한 역할의 관측 반복', '',
            '**범위:** 원고가 아닌 기능표 1건. E1의 정확 출구 뒤 같은 허용 훈련의 두 공 궤적에서 박스아웃과 동료 공 확보만 기록한다.', '',
            f"- 상태: `{data['status']}` / 출처현재성 `{data['local_blueprint']['status']}`",
            f"- 전역 기능 {data['final_function_order']}, A03 계획 슬롯 {data['planned_allocation_slot']} (소막 균등배분·공개번호 미확정)",
            f"- 정확 진입: {data['entry_state']}",
            f"- 한 기능: {data['single_function']}",
            f"- 선택: {data['unit_choice']}",
            f"- 직접 비용: {data['direct_present_cost']}", '',
            '| 단계 | 행동 | 보이는 결과 |', '| --- | --- | --- |']
    for beat in data['beats']:
        rows.append(f"| {beat['id']} | {beat['action']} | {beat['observable_result']} |")
    rows += ['', f"- 정확 출구: {data['exit_state']}",
             f"- 다음 독자 질문: {data['reader_question_at_end']}",
             '- 한 연습의 두 관측은 좁은 역할의 근거일 뿐 실전 신뢰·정규시즌 분·선발·기술 숙련을 인증하지 않는다.',
             '- F03 Texas Tech와 200분 분배는 별도 원천·역사 검문 뒤에만 다룬다. 대표 경기·기능3 상한을 늘리지 않는다.',
             '- 전체 A03/G13/G14·실제 Pack·원고는 미완료, 설계/원고 게이트 `CLOSED`.', '']
    return '\n'.join(rows)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A03 E2 differs from source-bound reviewed repetition']


def self_test(data):
    changes = [
        ('official minutes paid', lambda x: x['next_unit'].update(Texas_Tech_result_or_exact_box_prepaid=True)),
        ('whole S2 paid', lambda x: x.update(whole_A03_S2_exit_certified=True)),
        ('mastery inserted', lambda x: x['verification_limits'].append('Wing mastery and guaranteed starts achieved.')),
        ('second observation omitted', lambda x: x['beats'].pop()),
        ('all 54 slots consumed', lambda x: x['slot_accounting'].update(a03_locally_assigned_function_slots=54)),
    ]
    for name, mut in changes:
        changed = copy.deepcopy(data)
        mut(changed)
        assert validate(changed), name
    original_load = load
    for name, path, mut in [
        ('E1 exit altered', PREVIOUS, lambda x: x.update(exit_state='첫 대학 경기에서 주전으로 우승했다')),
        ('CF02 second result reversed', WORKING, lambda x: x['practice'][2].update(observed_result='동료가 공을 잡지 못했고 전원에게 미움받았다')),
        ('F02 cost turned championship', CANDIDATES, lambda x: x['functions'][1].update(cost='이미 대학 우승 MVP가 되었다')),
    ]:
        def changed_load(root, requested, path=path, mut=mut):
            source = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                source = copy.deepcopy(source)
                mut(source)
            return source
        with patch(__name__ + '.load', side_effect=changed_load):
            assert validate(data), name
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
