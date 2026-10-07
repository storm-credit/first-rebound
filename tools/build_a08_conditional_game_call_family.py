"""Bounded fictional A08 game calls; no 2022-23 game or roster certification."""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a08_conditional_game_call_family.py'
OUT = 'design/A08_CONDITIONAL_GAME_CALL_FAMILY_2026_10_07.json'
MD = OUT[:-5] + '.md'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
BATCH = 'design/A08_FINITE_FUNCTION_BATCH_2026_10_07.json'
CF = 'design/A08_2022_23_CONDITIONAL_FUNCTIONS.json'
CORE = 'research/CHICAGO_2022_23_APPROVED_CORE_CONTRACT_EXECUTION_2026_10_07.json'
COST = 'research/CHICAGO_2022_FULL_COST_ROSTER_FAMILY_2026_10_07.json'
RT = 'design/A08_S1_CURRENT_RT_COST_SLOT_FAMILY_2026_10_07.json'
PINS = {
    CP2: '2b291bca588302cbb254fc3417652f7d7532c46d7094221cdcceac60619c9db9',
    BATCH: 'b84f4d08ede9015934b6d91287c21588bee9443fbaa8bf9ae6d3b1804f8c3b07',
    CF: '7e7d4891ea823eca87ebe949647eff2e4354cfc9021c79856922ab32a97ba3b3',
    CORE: '2cc7aeaeaef530f1c3fac5846348792c3d516eb1479af1ce56617deb2e7cb2b5',
    COST: '16830b560cf4f2008053ac236202010ff87188f42536a5d36870433933feccf0',
    RT: 'ed87785bf0e40c568fa97c578d7d0c2102dadc0445006d475acb235bfa4156d5',
}


def text(path):
    return (ROOT / path).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def sha(path):
    return hashlib.sha256(text(path).encode()).hexdigest()


def load(path):
    return json.loads(text(path))


def inputs():
    for path, expected in PINS.items():
        assert sha(path) == expected, f'Source changed: {path}'
    p = {path: load(path) for path in PINS}
    for path in PINS:
        assert p[path] == json.loads(text(path)), f'Source reader changed: {path}'
    sub = {r['id']: r for r in p[CP2]['subacts']}
    assert sub['A08-S2']['success_criteria'] == [
        '캐치 직후 반환과 드리블 유지 후 패스를 다른 표본으로 분류',
        '성공 패스뿐 아니라 공격 지연·턴오버·실패 뒤 복귀 책임 확인',
    ]
    assert sub['A08-S3']['success_criteria'] == [
        '주인공이 끝내는 경우와 LaMelo/LaVine이 끝내는 경우 모두 조건을 설명',
        'P3의 상호 비용을 남기되 2028 수취인/득점은 아직 잠그지 않음',
    ]
    assert p[BATCH]['functions'][1]['source_CF03_actual_NBA_game_trial_executed'] is False
    assert p[BATCH]['functions'][1]['full_A08_S2_cp2_exit_certified'] is False
    assert p[CORE]['routine_carry_candidate']['whole2022_roster_selected'] is False
    carry = {r['player'] for r in p[CORE]['core_carry_rows']}
    unsigned = {r['player'] for r in p[CORE]['expired_or_unselected_new_contract_inputs']
                if r['new2022_route_selected'] is False}
    assert {'Markkanen', 'LaMelo Ball'} <= carry
    assert {'Protagonist', 'LaVine', 'Wendell Carter Jr.'} <= unsigned
    assert p[COST]['certification']['whole_FY22_selected_roster_cost_results'] is False
    assert p[RT]['RT_policy_selected'] is None
    return p, sub


def assert_calls(calls):
    assert [r['criterion'] for r in calls] == ['A08-S2', 'A08-S2', 'A08-S2', 'A08-S3', 'A08-S3']
    assert [r['window_seconds'] for r in calls] == [20] * 5
    assert sum(r['window_seconds'] for r in calls) == 100, 'Partial game clock exceeded'
    assert calls[0]['return_class'] == 'CATCH_IMMEDIATE_NO_DRIBBLE'
    assert calls[0]['first_return_lane'] == 'observed_open_direct_top_arc_return_lane'
    assert calls[0]['dribble_before_return'] is False
    assert calls[1]['return_class'] == calls[2]['return_class'] == 'DRIBBLE_MAINTAINED_BEFORE_RETURN_DECISION'
    assert calls[1]['dribble_before_return'] is True and calls[2]['dribble_before_return'] is True
    assert calls[1]['first_return_lane'] == 'direct_top_arc_return_lane_closed'
    assert calls[2]['first_return_lane'] == calls[1]['first_return_lane']
    assert calls[2]['chosen_return_lane'] != calls[2]['first_return_lane'], 'Safe return cannot reuse blocked lane'
    assert calls[2]['chosen_return_lane'] == 'observed_open_rear_angle_reset_lane_to_LaMelo'
    assert calls[0]['observed_result'].startswith('IMMEDIATE_CATCH_RETURN')
    assert 'TURNOVER' in calls[1]['observed_result'] and 'SAFE_RESET' in calls[2]['observed_result']
    assert calls[3]['observed_result'].startswith('OWN_BOUNDED_ATTEMPT')
    assert calls[4]['observed_result'].startswith('TEAMMATE_ADVANTAGE_HANDOFF')
    assert all(r['classification'] == 'NEW_CONDITIONAL_FICTIONAL_NBA_GAME_CALL_NOT_HISTORICAL_PLAY'
               for r in calls)


def build():
    p, sub = inputs()
    chicago_five = ['Protagonist', 'LaMelo Ball', 'LaVine', 'Markkanen', 'Wendell Carter Jr.']
    opponent_five = [f'OPPONENT_SELECTED_{i}' for i in range(1, 6)]
    calls = [
        {
            'id': 'G0_IMMEDIATE_CATCH_RETURN', 'criterion': 'A08-S2',
            'condition': 'The direct return lane to LaMelo is visibly open at the right-elbow catch in one lawful permitted window.',
            'first_return_lane': 'observed_open_direct_top_arc_return_lane',
            'chosen_return_lane': 'observed_open_direct_top_arc_return_lane',
            'return_class': 'CATCH_IMMEDIATE_NO_DRIBBLE', 'dribble_before_return': False,
            'window_seconds': 20,
            'bounded_coach_permission': 'A catch-and-return comparator before any maintained dribble.',
            'observed_action': 'He returns to LaMelo directly at the catch without a dribble and clears the lane for the next connection.',
            'observed_result': 'IMMEDIATE_CATCH_RETURN_AND_REENGAGEMENT; no shot, assist, score, or possession finish selected.',
            'cost': 'He gives up a personal short-attack chance while LaMelo takes the next decision.',
            'classification': 'NEW_CONDITIONAL_FICTIONAL_NBA_GAME_CALL_NOT_HISTORICAL_PLAY',
        },
        {
            'id': 'G1_BLOCKED_FIRST_RETURN', 'criterion': 'A08-S2',
            'condition': 'A lawful, separately permitted NBA game window has Protagonist and LaMelo on court; first return lane closes at the catch.',
            'first_return_lane': 'direct_top_arc_return_lane_closed',
            'chosen_return_lane': 'direct_top_arc_return_lane_closed',
            'return_class': 'DRIBBLE_MAINTAINED_BEFORE_RETURN_DECISION', 'dribble_before_return': True,
            'window_seconds': 20,
            'bounded_coach_permission': 'One short-angle response trial, with transition-defense responsibility if the pass fails.',
            'observed_action': 'He holds the dribble to alter the angle, releases late into the blocked first route, loses the ball, and turns to recover his assigned defensive lane.',
            'observed_result': 'TURNOVER_AND_RECOVERY_ATTEMPT; no opponent score or possession end selected.',
            'cost': 'His lost attacking opportunity and the teammate relocation/transition burden stay in the sample.',
            'classification': 'NEW_CONDITIONAL_FICTIONAL_NBA_GAME_CALL_NOT_HISTORICAL_PLAY',
        },
        {
            'id': 'G2_STOP_AND_SAFE_RESET', 'criterion': 'A08-S2',
            'condition': 'A later lawful window again closes the direct top-of-arc route; Protagonist sees a different rear-angle reset lane to the nearby LaMelo.',
            'first_return_lane': 'direct_top_arc_return_lane_closed',
            'chosen_return_lane': 'observed_open_rear_angle_reset_lane_to_LaMelo',
            'return_class': 'DRIBBLE_MAINTAINED_BEFORE_RETURN_DECISION', 'dribble_before_return': True,
            'window_seconds': 20,
            'bounded_coach_permission': 'Retry once and stop forcing the angle when the return is closed.',
            'observed_action': 'He starts the short dribble, sees the direct top route stay closed, stops that pass, observes the separate rear-angle lane open, returns through it to LaMelo, then changes position for another connection.',
            'observed_result': 'SAFE_RESET_AND_REENGAGEMENT; no made basket, assist, possession finish, or repeated success awarded.',
            'cost': 'Own shot/creation time is surrendered and the team still spends attack clock.',
            'classification': 'NEW_CONDITIONAL_FICTIONAL_NBA_GAME_CALL_NOT_HISTORICAL_PLAY',
        },
        {
            'id': 'G3A_OWN_SHORT_ATTEMPT_AND_STOP', 'criterion': 'A08-S3',
            'condition': 'The already prepared short inside step is briefly available before the defender closes the path.',
            'window_seconds': 20,
            'bounded_coach_permission': 'One short-action comparison only, not a permanent joint-ace or closing assignment.',
            'observed_action': 'He takes the prepared short step while the opening is visible, sees the inside path close, and stops rather than adding an unprepared advanced move.',
            'observed_result': 'OWN_BOUNDED_ATTEMPT_AND_STOP; shot, points, assist and possession finish remain unselected.',
            'cost': 'He uses a limited attacking window without earning a scoring result or repeatable creator role.',
            'classification': 'NEW_CONDITIONAL_FICTIONAL_NBA_GAME_CALL_NOT_HISTORICAL_PLAY',
        },
        {
            'id': 'G3B_TEAMMATE_ADVANTAGE_HANDOFF', 'criterion': 'A08-S3',
            'condition': 'In a separate window LaMelo or LaVine has a visibly faster available route than Protagonist.',
            'window_seconds': 20,
            'bounded_coach_permission': 'Compare the teammate advantage and retain rebound/reconnection responsibility.',
            'observed_action': 'He passes to the observed better-positioned teammate, moves to the rebound/reconnection lane, and retains responsibility for the result.',
            'observed_result': 'TEAMMATE_ADVANTAGE_HANDOFF_AND_REENGAGEMENT_ONLY; teammate finish, score, assist and game authority remain unselected.',
            'cost': 'He relinquishes a personal attempt; the teammate accepts a bounded new decision burden.',
            'classification': 'NEW_CONDITIONAL_FICTIONAL_NBA_GAME_CALL_NOT_HISTORICAL_PLAY',
        },
    ]
    assert_calls(calls)
    reserved_per_player = sum(r['window_seconds'] for r in calls)
    selected_five_remainder_seconds = 24 * 60 - reserved_per_player
    five_other_roster_players_seconds = 24 * 60
    remaining_team_seconds = 5 * selected_five_remainder_seconds + 5 * five_other_roster_players_seconds
    assert reserved_per_player == 100 and remaining_team_seconds == 13900
    assert remaining_team_seconds + 5 * reserved_per_player == 240 * 60
    assert selected_five_remainder_seconds > 0
    return {
        'id': 'A08_CONDITIONAL_GAME_CALL_FAMILY',
        'status': 'WORKING_CONDITIONAL_GAME_CALL_INPUT_NOT_INDEPENDENTLY_REVIEWED',
        'entry_from': p[BATCH]['functions'][2]['exit_state'],
        'game_window': {
            'season': '2022-23', 'specific_date': None, 'opponent': None, 'game_id': None,
            'five_nonconsecutive_windows_are_separately_conditional': True,
            'lawful_signed_roster_and_both_team_ten_active_availability_required': True,
            'Protagonist_LaMelo_LaVine_presence_selected_for_whole_season': False,
            'common_five_for_2022_23_certified': False,
            'player_minute_vectors_or_240_team_minutes_certified': False,
            '2021_22_M1_lineup_reused_as_2022_23_fact': False,
            'selected_score_winner_or_full_game': False,
        },
        'partial_clock_existence_witness': {
            'source': 'Current FY22 conditional core/slot family plus newly modeled windows; not a selected 2022-23 game vector',
            'Chicago_conditional_five': chicago_five,
            'Chicago_unselected_other_five_identity_slots': [f'CHI_OTHER_LAWFUL_ACTIVE_{i}' for i in range(1, 6)],
            'opponent_conditional_five_identity_slots': opponent_five,
            'opponent_unselected_other_five_identity_slots': [f'OPPONENT_OTHER_LAWFUL_ACTIVE_{i}' for i in range(1, 6)],
            'source_supported_contract_scope': 'Markkanen/LaMelo are carry inputs; Protagonist/LaVine/Carter need a later lawful 2022 route before game use.',
            'selected_five_on_court_only_for_five_windows': True,
            'windows': 5, 'seconds_each': 20, 'reserved_seconds_per_named_or_parameter_player': reserved_per_player,
            'reserved_seconds_per_team': 5 * reserved_per_player,
            'abstract_24_minute_half_for_window_five_remainder_seconds_each': selected_five_remainder_seconds,
            'abstract_other_five_24_minute_each_seconds': five_other_roster_players_seconds,
            'unassigned_team_seconds_after_windows': remaining_team_seconds,
            'mathematical_team_seconds_completion': 240 * 60,
            'mathematical_pair_seconds_completion': 480 * 60,
            'actual_team_or_player_minutes_chosen': False,
            'actual_full_five_person_chronology_or_clinical_clearance_certified': False,
        },
        'bounded_game_calls': calls,
        'cp2_contract': {
            'A08_S2_choice': sub['A08-S2']['choice'],
            'A08_S2_cost': sub['A08-S2']['cost'],
            'A08_S2_exit': sub['A08-S2']['exit_state'],
            'A08_S3_choice': sub['A08-S3']['choice'],
            'A08_S3_cost': sub['A08-S3']['cost'],
            'A08_S3_exit': sub['A08-S3']['exit_state'],
            'S2_source_criteria_ready_only_if_conditions_executed_and_game_clock_roster_verified': True,
            'S2_catch_immediate_vs_dribble_then_pass_comparison_modeled': True,
            'S2_turnover_recovery_and_safe_reset_both_retained': True,
            'S3_finish_conditions_explained_without_result_selection': {
                'Protagonist_finish_condition': 'If his prepared short lane stays open after the first step and his advantage is better, he keeps the bounded finish decision; LaMelo/LaVine gives up that possession option and Protagonist owns failure responsibility. G3a instead sees closure and stops.',
                'LaMelo_or_LaVine_finish_condition': 'If one has the visibly faster open route, Protagonist relinquishes his shot option and hands off, then takes rebound/reconnection work; the receiver accepts the next decision and its failure risk. G3b models this handoff.',
                'mutual_possession_cost_retained': 'Protagonist and LaMelo/LaVine each relinquish control in the other condition; neither is relieved of the bounded failure responsibility by a hypothetical make.',
                '2028_receiver_or_scorer_locked': False,
                'actual_own_and_teammate_finishes_observed': False,
            },
            'S3_source_success_criteria_condition_explanation_bounded_pass': True,
            'S3_whole_subact_exit_or_game_authority_complete': False,
        },
        'required_next_input_for_execution': [
            'Choose lawful 2022-23 routes for Protagonist/LaVine/Carter and ten active eligible players per side, including the conditional five; no placeholder is an actual signed identity.',
            'Instantiate five 20-second windows in a lawful game; the 100-second and 13,900-second witness proves possible clock capacity only, not a selected 240-minute player vector.',
            'Keep the coach permission, own observation/footage access, turnover recovery and safe reset as fictional modeled events, distinct from historical play-by-play.',
        ],
        'source_sha256': {**PINS, SELF: sha(SELF)},
        'certification': {
            'independent_review_completed': True, 'new_final_function_registered': 0,
            'independent_review_basis': 'Root read original CP2 criteria and the actual five-call construction, recomputed 100/500/13900/14400 seconds and rejected actual immediate-return-to-dribble, safe-route-to-blocked-route, and 20-to-21-second caller mutations. Earlier chi review covered four calls; it is not counted as review of the newly added fifth call.',
            'root_conditional_working_design_selection': True,
            'root_selection_scope': 'Five bounded calls and mutual finish-condition explanation only, subject to lawful 2022 routes, ten active identities per side and clock instantiation. No actual season roster, finish result, contract or joint-ace authority.',
            'A08_S2_or_S3_exit_pass': False, 'whole_A08_or_G13_G14_complete': False,
            'actual_NBA_game_or_full_health_certified': False,
            'E2_contract_price_or_acceptance_selected': False,
            'joint_ace_or_closing_authority_awarded': False,
            'actual_context_packs': 0, 'manuscript_count': 0,
            'manuscript_allowed': False, 'design_gate': 'CLOSED', 'new_author_lock': False,
        },
    }


def render(x):
    return '\n'.join([
        '# A08 실경기 제한 호출 조건부 입력', '',
        '2022–23 경기 날짜·상대·양측 5인·분 벡터는 현재 정본에서 선택되지 않았다. '
        '2021–22 M1의 5인·240분을 다음 시즌 실경기 증명으로 옮기지 않는다. '
        '원 CP2 A08-S2는 실제 경기에서 반환 차단의 사용·중단을 관측해야 하지만 특정 날짜/상대명을 요구하지는 않는다.', '',
        '현재 FY22 비용·명단 가족에서 Markkanen/LaMelo의 carry와 주인공/LaVine/Carter의 아직 미선택 2022 적법 경로를 분리해 조건부 Chicago 5인으로 둔다. '
        '상대 5인과 양측 추가 5인은 실제 인물이 아닌 적법·가용 명단 변수다. 다섯 비연속 20초 창에서 각 창 5인에게 100초씩 예약하면 팀마다 500선수초, 나머지 13,900선수초다. '
        '나머지는 선택 5인 각 1,340초와 추가 5인 각 1,440초로 수학적 240분을 구성할 수 있으나 실제 출장·교대순서는 선택하지 않는다. '
        '가상 감독의 다섯 제한 호출을 한 배치의 조건부 설계 입력으로 둔다. '
        '첫 호출은 열린 직접 길을 보고 드리블 없이 캐치 직후 LaMelo에게 반환한다. '
        '둘째는 막힌 첫 경로에 드리블 뒤 늦게 패스해 턴오버와 자기 수비 복귀 시도를 남긴다. '
        '셋째는 같은 직접 경로가 막힌 것을 보고 짧게 각도를 바꾼 뒤 별도로 열린 후방 반환길을 관측해 LaMelo에게 안전하게 돌리고 재관여한다. '
        '넷째는 자신이 준비한 짧은 안쪽 걸음을 실제 시도하다 길이 닫히면 중단한다. '
        '다섯째는 동료에게 더 빠른 길이 보이자 공을 넘긴 뒤 리바운드·연결 위치를 잡는다. '
        '득점, 도움, 상대 점수, 동료의 성공, 공동 에이스 권한은 정하지 않는다.', '',
        'S2는 캐치 직후 반환과 드리블 뒤 패스/재전개를 별도 표본으로 설명한다. S3는 짧은 자기 길이 계속 열리고 자기 우위가 클 때만 자기 마무리 판단을 맡으며, 그때 동료는 해당 포제션의 선택권을 내려놓는다. '
        'LaMelo/LaVine에게 더 빠른 길이 보이면 주인공은 자기 시도를 포기하고 이양·재관여하며 동료는 다음 판단과 실패 위험을 맡는다. 양쪽 모두의 포제션 비용과 실패 책임을 남기고 2028 수신자·득점자는 잠그지 않는다. '
        '따라서 원 S3의 두 마무리 **조건 설명** 성공기준은 한정 충족한다. 양쪽 실제 마무리 결과 관측은 원 성공기준의 새 의무가 아니다. 실제 경기별 권한·전체 소막/막 출구와 득점 결과는 미확정이다.', '',
        '실행에 필요한 입력은 선택된 합법 명단과 양팀 가용 10인, 해당 경기에서 다섯 창의 실제 배치, '
        '한정 감독 허용과 본인 관측 경로다. 현재 비용·명단 원장은 조건부 범위이지 실제 경기 등록증이 아니다. '
        '따라서 이 패킷은 A08-S2/S3 출구 PASS나 새 회차를 등록하지 않는다. E2 계약 결정·시즌 승패·원고도 미확정이다.', '',
        '|번호|묶음|상태|', '|---|---|---|',
        '|1|2020 드래프트 연쇄|완료|', '|2|Chicago 2020–21|S2 완료|',
        '|3|2021–23 거래·계약|2022 비용 가족 준비, 최종 선택 미완|',
        '|4|장기 커리어|A08 조건부 실경기 입력 준비|',
        '|5|결말·전체 구조|전체 기능 출구 미완|',
        '|6|집필규격·Context Pack|Pack 0|',
        '|7|통합·독립·작가 승인|CLOSED|', '',
        '미완료 큰 묶음 5 / PROJECT_FREEZE v0.30 PARTIAL / 설계·원고 게이트 CLOSED / 원고 0.',
    ])


def validate(x):
    try:
        return [] if x == build() else ['saved input differs from source-bound construction']
    except (AssertionError, KeyError, OSError, ValueError, TypeError) as e:
        return [f'source construction: {e}']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    x = build()
    if a.write:
        (ROOT / OUT).write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MD).write_text(render(x), encoding='utf-8')
    if a.check:
        assert validate(load(OUT)) == []
        assert text(MD) == render(x)
    print(json.dumps({'current': True, 'calls': 5, 'conditional_pair_team_seconds': 28800,
                      'game_anchor_selected': False,
                      'S2_S3_exits_passed': False}))


if __name__ == '__main__':
    main()
