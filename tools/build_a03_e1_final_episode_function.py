"""Build one local A03 function from reviewed registration, practice failure and role response."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a03_college_entry_working_model as entry_builder
import build_a03_cf01_role_response_working_model as response_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A03_E1_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = OUTPUT.with_suffix('.md')
ENTRY = str(entry_builder.OUTPUT).replace('\\', '/')
RESPONSE = str(response_builder.OUTPUT).replace('\\', '/')
E10 = entry_builder.E10
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
CANDIDATES = 'design/A03_CONDITIONAL_EPISODE_FUNCTIONS.json'
ACT_MAP = 'design/ACT_MAP.md'
SKILL = 'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md'
SOURCES = ('tools/build_a03_e1_final_episode_function.py', ENTRY, RESPONSE, E10,
           CP2, CANDIDATES, ACT_MAP, SKILL)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def source_bytes(root, path):
    target = Path(path)
    return (target if target.is_absolute() else root / target).read_bytes()


def norm_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def build(root=ROOT):
    entry = load(root, ENTRY)
    response = load(root, RESPONSE)
    previous = load(root, E10)
    cp2 = load(root, CP2)
    candidates = load(root, CANDIDATES)
    assert entry == response_builder.load(root, entry_builder.OUTPUT), 'entry differs from response validation input'
    assert not response_builder.validate(response, root=root), 'reviewed role response must be source-current'
    assert previous == entry_builder.load(root, E10), 'E10 differs from entry validation input'
    assert previous['exit_state'] == entry['prior_A02_E10_exact_full_exit']
    assert entry['first_local_trial_exit'] == response['prior_exact_entry_trial_exit']
    assert entry['status'] == 'SELECTED_ROUTINE_FICTIONAL_ENTRY_AND_FIRST_PRACTICE_MODEL_INDEPENDENTLY_REVIEWED'
    assert response['status'] == 'SELECTED_ROUTINE_ROLE_RESPONSE_INDEPENDENTLY_REVIEWED'
    assert entry['independent_review_completed'] and response['independent_review_completed']
    assert previous['final_function_order'] == 19
    assert previous['planned_allocation_slot'] == 46
    assert previous['episode_function_id'] == 'A02-EF-010'
    assert previous['next_unit']['id'] == 'A03-S1'
    assert previous['next_unit']['exact_full_entry_for_A03_requires_separate_function_review'] is True
    assert previous['manuscript_allowed'] is False and previous['whole_g13_complete'] is False
    assert entry['new_sequence'][0]['fictional_enrollment_completed'] is True
    assert entry['new_sequence'][1]['official_game_or_box_score_executed'] is False
    assert entry['limits']['selected_I3_full_qualifier_or_compliance_revoked_here'] is False
    assert response['prior_selected_I3_full_qualifier_retained'] is True
    assert response['response'][0]['id'] == 'V1' and response['response'][1]['id'] == 'V2'
    assert response['response'][1]['new_punishment_injury_or_school_cost_event'] is False
    assert response['CP2_S1_whole_exit_or_final_episode_function_certified'] is False
    assert response['limits']['formal_college_game_or_box_score_claimed'] is False
    assert response['limits']['A03_S2_trust_or_repeated_success_completed'] is False
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    subact = next(row for row in cp2['subacts'] if row['id'] == 'A03-S1')
    assert (subact['choice'], subact['cost'], subact['exit_state']) == (
        '우승팀 소속이라는 이름 대신 자신이 수행할 수 있는 좁은 벤치 역할을 맡는다',
        '자기 쇼케이스', '제한된 역할을 수락')
    assert candidates['status'] == 'THREE_CONDITIONAL_FUNCTIONS_NOT_FINAL_G13'
    assert candidates['final_episode_functions'] == 0
    source_f01 = candidates['functions'][0]
    assert (source_f01['id'], source_f01['subact'], source_f01['next']) == ('A03-F01', 'A03-S1', 'A03-F02')
    assert source_f01['choice'] == '영상으로 자신이 동료에게 넘긴 부담을 확인하고 다음 훈련의 제한 역할을 수락'
    assert source_f01['cost'] == '출전 보상 없이 영상·역할 훈련에 시간을 쓰며 학업 의무도 유지'
    assert source_f01['status'] == 'CONDITIONAL_EPISODE_FUNCTION_CANDIDATE'
    act_map = source_bytes(root, ACT_MAP).decode('utf-8-sig')
    assert '| A01 | 2015–2016.02 | 농구를 계속할 이유 | 36 |' in act_map
    assert '| A02 | 2016.03–2017.06 | 포지션을 잃는 비용 | 54 |' in act_map
    assert '| A03 | 2017–18 | 맡은 역할의 크기 | 54 |' in act_map
    assert [row['id'] for row in entry['new_sequence']] == ['A03-I4-1', 'A03-I4-2', 'A03-R1']
    assert [row['id'] for row in response['response']] == ['V1', 'V2']

    beats = [
        {'id': 'R1', 'classification': 'REVIEWED_ROUTINE_FICTIONAL_PRACTICE',
         'action': entry['new_sequence'][2]['observable_action'],
         'visible_result': entry['new_sequence'][2]['observable_result'],
         'source_path': ENTRY, 'not_claimed': '실제 Villanova 연습·경기·득점 결과'},
        {'id': 'V1', 'classification': 'REVIEWED_ROUTINE_FICTIONAL_FILM_ACCESS',
         'action': response['response'][0]['observable_action'],
         'visible_result': response['response'][0]['authorized_access'],
         'source_path': RESPONSE, 'not_claimed': response['response'][0]['not_accessed']},
        {'id': 'V2', 'classification': 'REVIEWED_ROUTINE_FICTIONAL_ROLE_CHOICE',
         'action': response['response'][1]['choice'],
         'visible_result': response['response'][1]['observed_result'],
         'source_path': RESPONSE, 'not_claimed': '반복 성공·동료 신뢰·공식 출전 확대'},
    ]
    local_blueprint = {
        'schema': 'A03_F01_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_FIRST_COLLEGE_PRACTICE_ROLE_FUNCTION_NOT_PRIVATE_RECORD_OR_GAME',
        'entry_state': entry['exact_A03_entry_after_fictional_registration'],
        'single_function': '첫 제한 수비 연습 실패를 허용된 영상으로 확인하고 다음 좁은 역할 과제를 수락한다',
        'choice': response['response'][1]['choice'],
        'direct_present_cost': response['response'][1]['direct_present_cost'],
        'exit_state': response['selected_design_exit_state'],
        'beats': copy.deepcopy(beats),
        'inter_act_not_episode_beats': ['I3 summer full qualifier/compliance', 'A03-I4-1 fictional enrollment',
                                        'A03-I4-2 team practice access'],
    }
    return {
        'schema': 'A03_E1_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A03-EF-001', 'act': 'A03', 'primary_subact': 'A03-S1',
        'source_conditional_function': 'A03-F01',
        'final_function_order': previous['final_function_order'] + 1,
        'planned_allocation_slot': 91,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
                            'a02_planned_slots': 54, 'a02_locally_assigned_function_slots': 10,
                            'a03_planned_slots': 54, 'a03_locally_assigned_function_slots': 1,
                            'a03_remaining_planned_slots': 53,
                            'total_local_functions_through_this': 20,
                            'allocation_is_final_published_episode_count': False,
                            'unused_90_a01_a02_planned_slots_must_be_filled_before_A03': False},
        'final_episode_functions_completed_this_record': 1,
        'previous_function': {'id': previous['episode_function_id'], 'source_path': E10,
                              'exact_full_exit': previous['exit_state']},
        'inter_act_bridge': {'summer_I3_selected_outside_A02_episode': True,
                             'I3_certification_retained': True,
                             'fictional_registration_completed_after_I3': True,
                             'institutional_source_path': ENTRY,
                             'real_personal_NCAA_or_Villanova_case_certified': False,
                             'official_game_executed': False},
        'local_blueprint': local_blueprint,
        'single_function': local_blueprint['single_function'],
        'entry_state': local_blueprint['entry_state'],
        'unit_choice': local_blueprint['choice'],
        'exit_state': local_blueprint['exit_state'],
        'direct_present_cost': local_blueprint['direct_present_cost'],
        'reader_question_at_end': '다음 허용 훈련에서 맡은 위치와 동료 연결을 반복해 보일 수 있는가',
        'internal_order': ['R1', 'V1', 'V2'], 'beats': beats,
        'next_unit': {'id': 'A03-F02', 'status': 'NEXT_CONDITIONAL_ROLE_REPETITION_NOT_EXECUTED',
                      'success_or_trust_prepaid': False,
                      'college_game_or_starting_role_prepaid': False},
        'information_access': {'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
                               'may_know': ['자기 등록 완료·허용 연습 과제의 전달',
                                            '직접 본 연습 결과와 허용된 자기 수비 영상',
                                            '자기가 선택한 다음 역할 과제와 이번 시간 비용'],
                               'cannot_know': ['NCAA 비공개 개별 환산·실제 개인 파일',
                                               '코치의 비공개 로테이션 평가·실존 동료 속마음',
                                               '향후 출전 분·공식 경기 결과'],
                               'individual_scene_pov_verified': False,
                               'exact_dialogue': None},
        'verification_limits': [
            'ACTUAL_VERIFIED means source-current local design, not real 2017 practice film, a real student record or published prose.',
            'I3 summer certification and fictional college registration are inter-act preconditions; neither is an A02 beat nor a first college official game.',
            'The first practice miss is fictional and bounded to one assigned help-position cue; no real Villanova game, box score, start or minute redistribution is certified.',
            'The CP2 A03-S1 provisional entry about belonging to a championship team is not backdated into this first college practice before the 2017–18 title.',
            'One accepted next role task is not repeated success, teammate trust, A03-S1 whole-exit approval or full G13.',
            'The 54 planned A03 slots remain an allocation, not 54 newly mandatory events or a fixed publication count.',
        ],
        'whole_A03_S1_exit_certified': False, 'whole_A03_act_exit_certified': False,
        'provisional_A03_S1_championship_entry_executed_here': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'g15_complete': False, 'g16_complete': False,
        'g17_complete': False, 'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {p: norm_sha(source_bytes(root, p)) for p in SOURCES},
    }


def render(data):
    rows = ['# A03 첫 국소 회차 기능 — 등록 뒤 제한 연습 실패와 역할 선택', '',
            '**범위:** 원고가 아닌 최종 국소 기능표 1건. 가상 대학 등록은 앞선 여름 자격 인계 뒤의 전제이며, 이 기능의 연습·영상·선택을 공식 경기로 바꾸지 않는다.', '',
            f"- 상태: `{data['status']}` / 출처현재성 `{data['local_blueprint']['status']}`",
            f"- 기능 순서 {data['final_function_order']}, A03 계획 배분 슬롯 {data['planned_allocation_slot']} (공개 회차 번호 미확정)",
            f"- 정확 진입: {data['entry_state']}",
            f"- 한 기능: {data['single_function']}",
            f"- 선택: {data['unit_choice']}",
            f"- 직접 비용: {data['direct_present_cost']}", '',
            '| 순서 | 행동 | 보이는 결과 |', '| --- | --- | --- |']
    for beat in data['beats']:
        rows.append(f"| {beat['id']} | {beat['action']} | {beat['visible_result']} |")
    rows += ['', f"- 정확 출구: {data['exit_state']}",
             f"- 다음 독자 질문: {data['reader_question_at_end']}",
             '- 여름 I3 full qualifier/compliance는 유지된다. A03 등록은 가상 기관 선택이며 개인 실제 서류·counter·경기 기록을 인증하지 않는다.',
             '- 영상·훈련은 가상 국소 기능이고 기존 대표 경기 3개 상한 밖 새 경기를 만들지 않는다. 다음 반복의 성공·동료 신뢰·선발·출전 분은 미실행이다.',
             '- 전체 A03/G13/G14·실제 Context Pack·원고는 미완료, 설계/원고 게이트 `CLOSED`.', '']
    return '\n'.join(rows)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, ValueError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A03 E1 differs from source-bound reviewed local function']


def self_test(data):
    changes = [
        ('official game claim', lambda x: x['inter_act_bridge'].update(official_game_executed=True)),
        ('loss of I3', lambda x: x['inter_act_bridge'].update(I3_certification_retained=False)),
        ('prepay repeated trust', lambda x: x['next_unit'].update(success_or_trust_prepaid=True)),
        ('prepay whole S1', lambda x: x.update(whole_A03_S1_exit_certified=True)),
        ('backdate championship identity', lambda x: x.update(provisional_A03_S1_championship_entry_executed_here=True)),
        ('inflate all A03 slots', lambda x: x['slot_accounting'].update(a03_locally_assigned_function_slots=54)),
    ]
    for name, mutate in changes:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_load = load
    for name, path, mutate in [
        ('previous E10 exit altered', E10, lambda x: x.update(exit_state='대학 공식 경기에서 즉시 선발 출전했다')),
        ('reviewed role choice flipped', RESPONSE, lambda x: x['response'][1].update(choice='영상 뒤 좁은 역할을 거부하고 무제한 출전을 요구한다')),
        ('A03 candidate changed to game', CANDIDATES, lambda x: x['functions'][0].update(choice='영상 대신 첫 공식 경기에서 MVP가 된다')),
    ]:
        def changed_load(root, requested, path=path, mutate=mutate):
            source = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                source = copy.deepcopy(source)
                mutate(source)
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
