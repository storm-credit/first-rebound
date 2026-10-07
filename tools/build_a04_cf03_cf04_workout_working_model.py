"""Select one bounded fictional coached workout for A04 CF03 and CF04."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a04_e2_final_episode_function as previous_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A04_CF03_CF04_WORKOUT_WORKING_MODEL_2026_10_07.json')
MARKDOWN = OUTPUT.with_suffix('.md')
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
CANDIDATES = 'design/A04_DRAFT_CONDITIONAL_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
PICK22 = 'research/CHICAGO_2018_PICK22_PLAUSIBILITY.md'
TALENT = 'canon/TALENT_BQ_MODEL.md'
TIMELINE = 'canon/CAREER_TIMELINE.md'
SOURCES = ('tools/build_a04_cf03_cf04_workout_working_model.py',
           PREVIOUS, CANDIDATES, CP2, PICK22, TALENT, TIMELINE)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def normalized_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


EXPECTED_CF03 = {
    'id': 'A04-CF03', 'subact': 'A04-S1',
    'dominant_function': '미완성 공격의 워크아웃 시도',
    'cause': '몸의 가능성을 평가받는 준비와 달리 대학의 저사용 공격 표본은 여전히 작다',
    'entry_state': '평가에 낼 영상 준비에서 몸의 장점과 약점도 드러낼 절차 준비로 시간을 옮긴다',
    'pressure': '익숙한 수비·리바운드만 보여 주면 자가 창조와 슈팅에 대한 질문이 남는다',
    'choice': '가능한 범위의 슈팅·짧은 공격·연결을 워크아웃 과제로 시도한다',
    'direct_cost': '잘하는 역할만 반복해 평가를 보호할 기회 대신 미완성 기술의 실패 위험을 감수한다',
    'changed_state': '공격의 가능한 범위와 막히는 부분을 직접 시험할 표본 후보가 생긴다',
    'next': 'A04-CF04',
    'next_dependency': '지시를 들은 뒤 다시 시도하는 행동이 현재 학습 과제로 이어진다',
}
EXPECTED_CF04 = {
    'id': 'A04-CF04', 'subact': 'A04-S1',
    'dominant_function': '지시 이후 수정 시도',
    'cause': '워크아웃 시도에서 확인해야 할 수행 문제가 생긴다',
    'entry_state': '공격의 가능한 범위와 막히는 부분을 직접 시험할 표본 후보가 생긴다',
    'pressure': '첫 시도의 인상을 지키려면 부족한 동작을 다시 드러내지 않고 끝내고 싶다',
    'choice': '직접 받은 지시를 확인하고 해당 위치·선택을 다음 시도에서 수정해 본다',
    'direct_cost': '처음 시도한 표본만 남기고 평가를 끝낼 기회를 포기하고 수정이 안 될 위험을 다시 노출한다',
    'changed_state': '정답을 알았다는 설명 대신 수정 시도의 행동을 평가에 내놓는다',
    'next': 'A04-CF05',
    'next_dependency': '그 행동을 Chicago의 비공개 보드나 지명 확약으로 읽지 않고 다음 연락을 기다린다',
}


def build(root=ROOT):
    previous = load(root, PREVIOUS)
    candidates = load(root, CANDIDATES)
    cp2 = load(root, CP2)
    assert previous == previous_builder.load(root, previous_builder.OUTPUT)
    assert not previous_builder.validate(previous, root=root), 'A04 E2 must be source-current'
    assert previous['episode_function_id'] == 'A04-EF-002'
    assert previous['final_function_order'] == 24 and previous['planned_allocation_slot'] == 146
    assert previous['next_unit']['id'] == 'A04-CF03'
    assert previous['whole_A04_S1_exit_certified'] is False
    assert previous['whole_g13_complete'] is False and previous['manuscript_allowed'] is False
    assert candidates['status'] == 'SIX_CONDITIONAL_DRAFT_CAUSAL_FUNCTIONS_NOT_FINAL_G13'
    cf03, cf04 = candidates['functions'][2:4]
    for source, expected in ((cf03, EXPECTED_CF03), (cf04, EXPECTED_CF04)):
        assert {key: source[key] for key in expected} == expected, source['id']
        assert source['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
        assert source['selected_event'] is False and source['author_locked'] is False
        assert source['observational_access'] == (
            '주인공 경험·직접 시도·허용된 평가 피드백·본인이 받은 연락/설명만 후보 접근. '
            '구단의 비공개 보드·타인 내면·의료 판정·미래 결과는 모른다.')
        assert all(source[key] is None for key in (
            'workout_or_measurement_date', 'combine_invitation', 'measurement_results',
            'medical_test_results', 'draft_pick', 'agent_name', 'score_or_box_stats'))
    assert cf03['next'] == cf04['id'] and cf04['entry_state'] == cf03['changed_state']
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    s1 = next(row for row in cp2['subacts'] if row['id'] == 'A04-S1')
    assert s1['entry_state'] == '신체 측정만으로 순번을 확신'
    assert s1['choice'] == '신체 측정으로 순번을 단정하지 않고 준비한 기술의 가능한 범위와 한계를 평가에 내놓는다'
    assert s1['exit_state'] == '보여줄 기술 표본 명확화'
    pick = (root / PICK22).read_text(encoding='utf-8-sig')
    talent = (root / TALENT).read_text(encoding='utf-8-sig')
    timeline = (root / TIMELINE).read_text(encoding='utf-8-sig')
    assert '작은 표본의 코너 캐치앤드슛' in pick
    assert '공을 오래 잡지 않는 원패스 연결' in pick
    assert '측면 민첩성·핸들·장거리 슛은 미완성' in pick
    assert '실패' in talent and '반복' in talent
    assert '정확 순번은 팀 보드·워크아웃과 22~60 재판정 전까지 HOLD' in timeline

    actions = [
        {
            'id': 'W0', 'phase': 'FICTIONAL_PERMISSION_AND_TASK',
            'actor': 'fictional private preparation coach',
            'action': 'One permitted private coached practice block is set for corner catch-and-shoot form, a short one-dribble attack, and a simple nearby outlet. The coach can instruct this practice, not certify an NBA workout or issue a club grade.',
            'observable_result': 'The protagonist knows the three tasks and that this is a personal preparation workout only.',
        },
        {
            'id': 'W1', 'phase': 'FIRST_ATTACK_ATTEMPT_WITH_LIMIT',
            'actor': 'protagonist',
            'action': 'From a corner catch he sets and releases a shot without a recorded make. On the next ball he takes one dribble toward the middle, stops before another self-created move, and waits too long to move the ball to the nearby practice partner.',
            'observable_result': 'The release is visible but its make rate is unknown; the one-dribble stop and delayed simple connection expose a specific decision limit. There is no live defender win.',
        },
        {
            'id': 'W2', 'phase': 'BOUNDED_INSTRUCTION',
            'actor': 'fictional private preparation coach',
            'action': 'The coach points to the observed stop and asks him to identify the nearby outlet before the next short attack, then make the simple pass if a second self-created action is not there.',
            'observable_result': 'He receives one instruction about a position and a choice in this practice; it is not a real scout quote, team feedback or official assessment.',
        },
        {
            'id': 'W3', 'phase': 'ONE_BOUNDED_RETRY',
            'actor': 'protagonist',
            'action': 'He repeats the corner start once, takes the same short dribble, stops at the same limit, looks to the pre-identified nearby partner and sends a simple pass rather than forcing a second creation.',
            'observable_result': 'One pass reaches the practice partner in an unopposed drill. The stopping point still exists; shot accuracy, live-read speed and game transfer remain unproved.',
        },
    ]
    cost = ('He spends this permitted block exposing a failed one-dribble continuation instead of repeating only his reliable defensive/rebounding role; '
            'he then uses one more attempt to reveal whether the correction is possible, with no grade or pick benefit promised.')
    exit_state = (
        '주인공은 허용된 가상 개인 지도 훈련에서 코너 캐치 슛을 시도했으나 성공률은 기록하지 않았다. '
        '짧은 한 드리블 뒤 다음 자가 창조가 막혀 가까운 동료에게 공을 늦게 연결한 첫 한계를 지도자가 직접 지적했다. '
        '그는 다음 한 번의 시도에서 같은 정지 지점을 만나자 미리 확인한 가까운 동료에게 단순 패스를 건넸다. '
        '이 국소 수정 행동은 보였지만 실제 수비 상대·경기·구단 평가·공식 측정·정확 지명 순번에서의 성공은 증명되지 않았다.'
    )
    return {
        'schema': 'A04_CF03_CF04_SINGLE_PRIVATE_WORKOUT_WORKING_MODEL_V1',
        'status': 'SELECTED_ROUTINE_SINGLE_PRIVATE_WORKOUT_INDEPENDENTLY_REVIEWED',
        'independent_review_completed': True,
        'scope': 'ONE_FICTIONAL_PERMITTED_PRIVATE_COACHED_PRACTICE_NOT_OFFICIAL_NBA_WORKOUT',
        'previous_exact_full_exit': previous['exit_state'],
        'source_function_ids': ['A04-CF03', 'A04-CF04'],
        'source_candidate_selection': {'CF03_choice': cf03['choice'], 'CF03_cost': cf03['direct_cost'],
                                       'CF04_choice': cf04['choice'], 'CF04_cost': cf04['direct_cost']},
        'fictional_instruction_authority': {
            'role': 'private preparation coach',
            'may': 'Set and observe this fictional practice task and give its one bounded correction.',
            'may_not': 'Issue an NBA invitation, club grade, medical clearance, combine result, draft promise or authentic scout statement.',
            'real_person_or_organization_identified': False,
        },
        'actions': actions,
        'direct_present_cost': cost,
        'selected_design_exit_state': exit_state,
        'next_candidate': {'id': 'A04-CF05', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'private_board_or_pick_response_known': False},
        'observed_vs_unknown': {
            'observed': ['corner catch shooting motion', 'one-dribble stop and delayed first outlet',
                         'coach instruction within private practice', 'one simple pass on bounded retry'],
            'unknown': ['shot make or shooting percentage', 'live defender read or game transfer',
                        'NBA club workout invitation or acceptance', 'medical clearance or official combine results',
                        'private team board, exact pick and contract'],
        },
        'limits': {
            'official_NBA_workout_invitation_or_participation_certified': False,
            'real_NBA_scout_or_team_staff_quote_claimed': False,
            'official_measurement_or_medical_certified': False,
            'game_or_live_defender_success_certified': False,
            'made_shots_or_box_stats_invented': False,
            'later_elbow_or_live_pass_skill_prepaid': False,
            'draft_pick_or_rookie_contract_selected': False,
            'CF05_executed': False,
            'final_episode_function_created_here': False,
            'whole_A04_S1_or_Act_exit_certified': False,
            'whole_g13_complete': False, 'whole_g14_complete': False,
            'actual_context_packs': 0, 'author_locked': False,
            'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {path: normalized_sha((root / path).read_bytes()) for path in SOURCES},
    }


def render(data):
    lines = [
        '# A04 CF03·CF04 개인 지도 훈련 운영안', '',
        '**범위:** 한 번의 허용된 가상 개인 지도 훈련. NBA 구단 워크아웃·Combine·의료·비공개 보드 결과가 아니다.', '',
        f"- 이전 E2 정확 출구: {data['previous_exact_full_exit']}",
        f"- 상태: `{data['status']}`", '- 원 후보 CF03의 공격 시도와 CF04의 지시 뒤 수정 시도를 한 세션의 연속 행동으로 연결한다.', '',
        '| 순서 | 직접 행동 | 관측·권한 경계 |', '| --- | --- | --- |',
    ]
    for action in data['actions']:
        lines.append(f"| {action['id']} | {action['action']} | {action['observable_result']} |")
    lines += [
        '', f"- 직접 비용: {data['direct_present_cost']}",
        f"- 국소 출구: {data['selected_design_exit_state']}",
        '- 지도자는 이 가상 개인 훈련 과제만 지시·관측한다. 실존 NBA 스카우트 발언이나 구단 공식 평가 권한을 갖지 않는다.',
        '- 첫 슛의 성공 여부, 실전 상대를 읽는 능력, 기술 완성, Chicago 보드와 정확 지명 결과는 확인되지 않았다.',
        '- CF05 미실행. 최종 회차 기능·전체 A04-S1/Act·G13/G14·실제 Pack·원고 승격 없음. 설계/원고 게이트 `CLOSED`.', '',
    ]
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A04 private workout differs from source-bound selection']


def self_test(data, root=ROOT):
    cases = [
        ('NBA event promotion', lambda x: x['limits'].update(official_NBA_workout_invitation_or_participation_certified=True)),
        ('scout quote promotion', lambda x: x['limits'].update(real_NBA_scout_or_team_staff_quote_claimed=True)),
        ('invent make', lambda x: x['actions'][1].update(observable_result='He makes all corner threes.')),
        ('invent game transfer', lambda x: x['limits'].update(game_or_live_defender_success_certified=True)),
        ('erase first failure', lambda x: x['actions'][1].update(action='He creates every attack without stopping.')),
        ('erase bounded retry', lambda x: x['actions'][3].update(observable_result='He never retries.')),
        ('prepay CF05', lambda x: x['limits'].update(CF05_executed=True)),
        ('erase cost', lambda x: x.update(direct_present_cost='')),
    ]
    for name, mutation in cases:
        altered = copy.deepcopy(data)
        mutation(altered)
        assert validate(altered, root), name
    original_load = load
    for name, path, mutation in [
        ('E2 exact exit becomes Combine success', PREVIOUS,
         lambda x: x.update(exit_state='정식 Combine에서 최고기록과 Chicago 22순위를 얻었다')),
        ('CF03 same-ID choice reverses', CANDIDATES,
         lambda x: x['functions'][2].update(choice='슈팅과 짧은 공격을 회피하고 수비만 보인다')),
        ('CF04 same-ID cost becomes contract', CANDIDATES,
         lambda x: x['functions'][3].update(direct_cost='수정 시도 대가로 보장계약을 받는다')),
        ('CP2 exit becomes official pick', CP2,
         lambda x: next(row for row in x['subacts'] if row['id'] == 'A04-S1').update(exit_state='정확 22순위 계약 확정')),
    ]:
        def changed(root, requested, path=path, mutation=mutation):
            value = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                value = copy.deepcopy(value)
                mutation(value)
            return value
        with patch(__name__ + '.load', side_effect=changed):
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
                      'negative_controls': tested, 'status': data['status']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
