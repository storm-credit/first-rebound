"""Select one bounded fictional Texas Tech role test after A03's two practices."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a03_e2_final_episode_function as previous_builder
import build_a03_texas_tech_game_source_and_insertion as game_builder
import build_a03_texas_tech_fictional_stint_witness as stint_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A03_CF03_TOURNAMENT_ROLE_WORKING_MODEL_2026_10_07.json')
MARKDOWN = OUTPUT.with_suffix('.md')
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
GAME = str(game_builder.OUTPUT).replace('\\', '/')
STINT = str(stint_builder.OUTPUT).replace('\\', '/')
CANDIDATES = 'design/A03_CONDITIONAL_EPISODE_FUNCTIONS.json'
SOURCES = ('tools/build_a03_cf03_tournament_role_working_model.py', PREVIOUS,
           GAME, STINT, CANDIDATES)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def normalized_sha(path):
    raw = path.read_bytes()
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def build(root=ROOT):
    previous = load(root, PREVIOUS)
    game = load(root, GAME)
    stint = load(root, STINT)
    candidates = load(root, CANDIDATES)
    assert previous == previous_builder.load(root, previous_builder.OUTPUT)
    assert not previous_builder.validate(previous, root=root), 'A03 E2 must be source-current'
    assert game == game_builder.build(root) and not game_builder.validate(game, root=root)
    assert stint == stint_builder.build(root) and not stint_builder.validate(stint, root=root)
    assert game['independent_review_completed'] is True
    assert stint['independent_review_completed'] is True
    assert previous['episode_function_id'] == 'A03-EF-002'
    assert previous['next_unit']['id'] == 'A03-F03'
    assert previous['next_unit']['Texas_Tech_result_or_exact_box_prepaid'] is False
    assert previous['whole_A03_S2_exit_certified'] is False
    assert stint['source_record'] == GAME
    assert stint['protagonist_minutes'] == game['fictional_working_insertion']['protagonist_minutes'] == 11
    assert stint['total_five_person_minutes'] == game['fictional_working_insertion']['team_player_minutes'] == 200
    assert stint['actual_play_by_play_or_possessions_certified'] is False
    assert stint['historical_71_59_or_player_box_preserved_under_fictional_stints_certified'] is False
    assert game['historical_official']['date'] == '2018-03-25'
    assert game['historical_official']['score'] == '71-59'
    assert candidates['status'] == 'THREE_CONDITIONAL_FUNCTIONS_NOT_FINAL_G13'
    assert candidates['final_episode_functions'] == 0
    f03 = candidates['functions'][2]
    expected = {
        'id': 'A03-F03', 'subact': 'A03-S3', 'function': 'Texas Tech 증명',
        'entry': '제한 역할의 근거를 얻었지만 전국 무대 압박에서의 유지가 미검문',
        'pressure': '공격이 원활하지 않은 날 개인 득점으로 존재감을 만들 유혹',
        'choice': '맡은 상대의 박스아웃과 스위치 연결을 먼저 수행',
        'cost': '전국 무대에서도 개인 공격 표본을 극대화하지 못해 NBA 자가 창조 질문이 남음',
        'observation_limit': 'Texas Tech는 기존 대표 경기; 실제 개인 기록/200분 재분배/교체초 HOLD',
        'changed_state': '우승팀 기여와 NBA 공격 능력 증명을 분리',
        'ending_question': '낮은 사용률을 숨기지 않고 프로 평가에서 어떤 기술 표본을 보여 줄 것인가',
        'next': 'A04-S1',
        'causal_link': '팀 소속 증명은 얻어도 공격 능력의 빈칸은 측정·워크아웃 과제로 넘어감',
    }
    assert {key: f03[key] for key in expected} == expected
    assert f03['status'] == 'CONDITIONAL_EPISODE_FUNCTION_CANDIDATE'
    assert f03['author_locked'] is False and f03['episode_number'] is None

    window = {
        'id': 'T0', 'classification': 'OFFICIAL_GAME_IDENTITY_PLUS_REVIEWED_FICTIONAL_CLOCK_WINDOW',
        'official_fact': '2018-03-25 Villanova 71–59 Texas Tech is the historical East Regional Final box.',
        'fictional_selection': 'The protagonist is a bench entrant for eleven modeled minutes in a 200-minute nine-player arithmetic clock.',
        'after': 'A03-EF-002 exact full exit; the two earlier practice possessions do not prove tournament success.',
        'information_access': 'The protagonist can know the opponent, date, his own assigned role and what he directly sees; exact future box and private evaluations are unavailable.',
        'real_2018_substitution_or_possession_claimed': False,
    }
    beats = [
        {'id': 'T1', 'classification': 'FICTIONAL_LOW_USAGE_VS_ASSIGNED_DEFENSE_PRESSURE',
         'action': 'In his modeled bench window, he has a bounded chance to ask for more individual offense while his assigned switch and nearby-opponent boxout still need execution.',
         'observable_result': 'He sees his own low individual attack involvement and the immediate defensive cue; shot attempts, touches and real historical play-by-play stay unassigned.',
         'individual_shots_or_touches_as_official_stat': None},
        {'id': 'T2', 'classification': 'SELECTED_FICTIONAL_ROLE_CHOICE_AND_ONE_VISIBLE_RESULT',
         'choice': 'He does not demand the extra self-created possession. He matches the visible switch cue, then takes inside position against the nearby opponent on the shot and blocks out.',
         'observable_result': 'One nearby teammate directly secures the ball while the protagonist holds the opponent away. Only this fictional local outcome is claimed, with no official rebound attribution.',
         'teammate_identity': None, 'opponent_identity': None,
         'official_rebound_awarded_to_protagonist': False,
         'paschall14_or_cosby7_event_level_preservation_proved': False},
        {'id': 'T3', 'classification': 'LOCAL_COST_AND_UNRESOLVED_PRO_QUESTION',
         'direct_present_cost': 'Within this modeled eleven-minute chance he spends the available task time on the switch and boxout rather than pressing to enlarge his individual attack sample.',
         'observable_result': 'He has one bounded team-possession contribution to point to, while his low-usage self-created offense remains untested for later professional evaluation.',
         'nba_scout_private_grade_known': False, 'individual_offense_proved': False},
    ]
    exit_state = (
        '주인공은 Texas Tech전의 가상 11분 창에서 추가 개인 공격 기회를 요구하기보다 맡은 스위치 연결과 가까운 상대 박스아웃을 먼저 택했다. '
        '한 동료가 공을 확보하는 국소 결과를 직접 봤지만, 공식 리바운드·실제 포제션·경기 전체 공로와 NBA용 자기 공격 능력은 아직 인증되지 않았다. '
        '이전 두 훈련 관측이 이 선택의 자동 성공을 보증한 것은 아니다.'
    )
    return {
        'schema': 'A03_CF03_TOURNAMENT_ROLE_WORKING_MODEL_V1',
        'status': 'SELECTED_ROUTINE_FICTIONAL_TOURNAMENT_ROLE_INDEPENDENTLY_REVIEWED',
        'independent_review_completed': True,
        'authority_scope': 'ONE_FICTIONAL_TEXAS_TECH_WINDOW_NOT_OFFICIAL_PBP_OR_FULL_ALTERNATE_GAME',
        'source_function_id': 'A03-F03',
        'previous_exact_full_exit': previous['exit_state'],
        'official_vs_fictional_window': window,
        'fictional_action_sequence': beats,
        'single_function': '낮은 개인 공격 표본과 맡은 수비 과제가 충돌하는 한 가상 출전 창에서 박스아웃·스위치 역할을 먼저 수행하고 동료 공 확보 한 번을 관측한다',
        'unit_choice': f03['choice'],
        'direct_present_cost': beats[2]['direct_present_cost'],
        'selected_design_exit_state': exit_state,
        'candidate_changed_state_as_later_target': f03['changed_state'],
        'candidate_changed_state_verified_on_march25': False,
        'march25_texas_tech_game_is_national_title_game': False,
        'later_title_and_pro_evaluation_bridge': {
            'status': 'OUTSIDE_THIS_LOCAL_MODEL_NOT_EXECUTED',
            'championship_and_postseason_evaluation_must_be_separate_from_March25': True,
            'official_title_result_or_private_scout_grade_inferred_here': False,
            'next_source_candidate': f03['next'],
            'next_question': f03['ending_question'],
        },
        'preservation_targets_not_certifications': {
            'historical_result': 'Villanova 71–59 Texas Tech',
            'Eric_Paschall_rebounds': 14,
            'Dhamir_Cosby_Roundtree_rebounds': 7,
            'alternate_event_level_box_or_score_verified': False,
        },
        'information_access': {
            'pov': 'PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'may_know': ['자기에게 전달된 역할', '가상 출전 창에서 자기 움직임과 공을 확보한 인접 동료의 직접 관측', '공개된 당시 경기 상대·날짜'],
            'cannot_know': ['실존 선수·감독의 내면 또는 실제 발언', '실제 2018 포제션과 가상 분 기증자의 정확 교체시점', '스카우트 비공개 평가·후속 지명 순번'],
            'specific_real_person_dialogue': None,
        },
        'limits': {
            'real_2018_player_action_or_PBP_certified': False,
            'actual_box_and_fictional_box_equivalent': False,
            'official_2018_win_reproved_under_alternate_events': False,
            'practice_repetition_guaranteed_tournament_success': False,
            'new_representative_game_added': False,
            'F03_final_episode_function_completed_here': False,
            'whole_A03_S3_or_A03_act_exit_certified': False,
            'whole_g13_complete': False, 'whole_g14_complete': False,
            'actual_context_packs': 0, 'author_locked': False,
            'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {path: normalized_sha(root / path) for path in SOURCES},
    }


def render(data):
    lines = [
        '# A03 Texas Tech전의 국소 역할 선택', '',
        '**범위:** 2018-03-25 [Villanova 공식 박스](https://villanova.com/sports/mens-basketball/stats/2017-18/texas-tech/boxscore/2694)는 역사 근거이고, 아래 출전 창과 행동은 별도 가상 설계다. 원고와 대체 경기 박스가 아니다.', '',
        f"- 정확 진입: {data['previous_exact_full_exit']}",
        f"- 단일 기능: {data['single_function']}",
        '- 공식 기록: Villanova 71–59 Texas Tech. 공식 양수 출전자 8명이며, 가상 주인공 포함 9인·200분·11분은 검토된 산술 시간표다. 실제 교체 시각·포제션 증거는 아니다.', '',
        '| 단계 | 가상 행동·선택 | 관측 또는 한계 |', '| --- | --- | --- |',
    ]
    for beat in data['fictional_action_sequence']:
        lines.append(f"| {beat['id']} | {beat.get('choice', beat.get('action', beat.get('direct_present_cost')))} | {beat['observable_result']} |")
    lines += [
        '', f"- 즉시 비용: {data['direct_present_cost']}",
        f"- 국소 출구: {data['selected_design_exit_state']}",
        '- Paschall 14리바운드·Cosby-Roundtree 7리바운드와 71–59는 공식 기록 및 보존 목표다. 동료 공 확보 한 번은 새 가상 관측이며 이 수치의 실제 포제션으로 인증하지 않는다.',
        '- 앞서 허용 훈련 두 번에서 박스아웃을 보였어도 토너먼트 성공이 자동 증명되지는 않는다. 개인 슛·터치·공식 리바운드·스카우트 평가는 미배정이다.',
        '- 원 후보의 우승팀 기여/프로 공격 분리는 이후 별도 역사 인계·시즌 후 평가 목표다. Texas Tech전 당일 우승이나 후속 우승·NBA 판단을 여기서 실행하지 않는다.',
        '- F03 최종 기능·소막/막 전체·G13/G14·Pack·원고는 미완료, 새 대표 경기 0, 게이트 `CLOSED`.', '',
    ]
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A03 Texas Tech local model differs from source-bound selection']


def self_test(data, root=ROOT):
    mutations = [
        ('prepay official rebound', lambda d: d['fictional_action_sequence'][1].update(official_rebound_awarded_to_protagonist=True)),
        ('prepay Paschall event preservation', lambda d: d['fictional_action_sequence'][1].update(paschall14_or_cosby7_event_level_preservation_proved=True)),
        ('claim March25 title', lambda d: d.update(march25_texas_tech_game_is_national_title_game=True)),
        ('prepay game box', lambda d: d['limits'].update(actual_box_and_fictional_box_equivalent=True)),
        ('prepay final function', lambda d: d['limits'].update(F03_final_episode_function_completed_here=True)),
        ('erase direct cost', lambda d: d.update(direct_present_cost='')),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed, root), name
    original_load = load
    for name, path, mutate in [
        ('E2 exit says automatic success', PREVIOUS,
         lambda d: d.update(exit_state='두 훈련으로 Texas Tech전 성공과 우승을 미리 보장받았다')),
        ('same-ID F03 choice reversal', CANDIDATES,
         lambda d: d['functions'][2].update(choice='박스아웃을 버리고 개인 득점만 먼저 시도한다')),
        ('clock witness claims actual PBP', STINT,
         lambda d: d.update(actual_play_by_play_or_possessions_certified=True)),
    ]:
        def altered(root, requested, path=path, mutate=mutate):
            source = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                source = copy.deepcopy(source)
                mutate(source)
            return source
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
    print(json.dumps({'current': not errors, 'errors': errors,
                      'negative_controls': tested, 'status': data['status']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
