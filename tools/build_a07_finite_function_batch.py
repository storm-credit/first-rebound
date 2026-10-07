"""Build three narrow A07 function records from approved role and candidate sources."""

import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_a06_2020_21_finite_function_batch as previous_builder
import build_a07_a08_finite_function_preparation as preparation_builder
import build_chicago_2021_22_m1_dated_working_minutes as m1_builder


ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a07_finite_function_batch.py'
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
CONDITIONAL = 'design/A07_2021_22_CONDITIONAL_FUNCTIONS.json'
M1 = 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json'
PREPARATION = str(preparation_builder.OUTPUT).replace('\\', '/')
OUTPUT = Path('design/A07_FINITE_FUNCTION_BATCH_2026_10_07.json')
SOURCES = (SELF, PREVIOUS, CP2, CONDITIONAL, M1, PREPARATION)
SEMANTIC_SHA = '319bc331c4d687dc1c04dcd16b4cd09d4d50fa0666e87a3ec523ce6a1d47bdf0'
REVIEWED_M1_CARRIER_SHA = '73d51b630e9c9d4ec31b7e3952906165589bd8c49a48bb07c79bdc9ad02e8fca'


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def sha(raw):
    normalized = raw.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def semantic_digest(cp2, candidate):
    core = {
        'act': [[x[k] for k in ('id', 'choice', 'cost', 'exit_state')]
                for x in cp2['acts'] if x['id'] == 'A07'],
        'subs': [[x[k] for k in ('id', 'entry_state', 'choice', 'cost', 'exit_state')]
                 for x in cp2['subacts'] if x['parent_act'] == 'A07'],
        'candidate': [[x[k] for k in ('id', 'subact', 'cause', 'entry_state', 'choice',
                                      'direct_cost', 'changed_state')]
                      for x in candidate['functions']],
    }
    raw = json.dumps(core, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def build(root=ROOT):
    previous = load(root, PREVIOUS)
    cp2, candidate, m1, preparation = (load(root, p) for p in (CP2, CONDITIONAL, M1, PREPARATION))
    assert previous == previous_builder.load(root, previous_builder.OUTPUT)
    assert not previous_builder.validate(previous, root=root), 'A06 source-current required'
    assert preparation == preparation_builder.load(root, preparation_builder.OUTPUT)
    assert not preparation_builder.validate(preparation, root=root), 'A07/A08 preparation source-current required'
    assert preparation['independent_review_completed']
    assert [row['subact'] for row in preparation['representative_groups'][:3]] == ['A07-S1', 'A07-S2', 'A07-S3']
    assert m1 == m1_builder.load(m1_builder.OUT), 'M1 carrier loader differs from reviewed source'
    assert sha((root / M1).read_bytes()) == REVIEWED_M1_CARRIER_SHA, 'M1 reviewed carrier snapshot changed'
    assert previous['functions'][-1]['global_function_order'] == 36
    assert semantic_digest(cp2, candidate) == SEMANTIC_SHA, 'A07 CP2/candidate meaning changed'
    assert [x['id'] for x in candidate['functions']] == [f'A07-CF{i:02d}' for i in range(1, 7)]
    assert m1['status'] == 'INDEPENDENTLY_REVIEWED_CONDITIONAL_82DATE_TWO_STATE_REGULATION_CARRIER'
    assert (m1['summary']['date_keys'], m1['summary']['rows'], m1['summary']['unordered_blocks']) == (82, 164, 1804)
    assert m1['summary']['executed_date_state_choices'] == 0
    assert m1['summary']['actual_new_game_results'] == 0
    cf = candidate['functions']
    prior_exit = previous['functions'][-1]['exit_state']
    functions = [
        {
            'id': 'A07-EF-001', 'global_function_order': 37, 'planned_allocation_slot': 323,
            'primary_subact': 'A07-S1', 'source_conditional_functions': ['A07-CF01', 'A07-CF02'],
            'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
            'entry_state': prior_exit,
            'single_function': 'M1 역할 비용을 보인 뒤 제한 엘보 시험을 허용받아 준비한다',
            'unit_choice': [cf[0]['choice'], cf[1]['choice']],
            'direct_present_cost': [cf[0]['direct_cost'], cf[1]['direct_cost']],
            'beats': [
                {'id': 'A07-R1-B1', 'action': '주인공은 LaMelo의 시작·LaVine의 마무리·Markkanen의 공간을 줄이는 넓은 요청 대신 M1 정상/COBY_OUT 두 조건에서 자신에게 맡길 좁은 엘보 위치와 반환 과제를 코치에게 제시한다. 특정 날짜의 Coby 결장이나 실제 82경기 분은 확정하지 않는다.', 'classification': 'SELECTED_FICTIONAL_ROUTINE_WITH_CONDITIONAL_ROSTER_INPUT'},
                {'id': 'A07-R1-B2', 'action': '가상 코치는 기존 허용 팀 훈련 안에서 짧은 엘보 공격과 막힐 때 반환만 시험하는 한정 과제를 실제로 맡긴다. 주인공은 캐치 뒤 첫 동작과 미리 정한 반환 위치를 반복하며, 직접 전진만 더 보여 줄 준비 시간을 포기한다.', 'classification': 'SELECTED_FICTIONAL_COACH_PRACTICE_GRANT_AND_PREPARATION'},
            ],
            'exit_state': '주인공은 M1의 동료 역할 비용을 함께 보인 제한 엘보 시험을 가상 코치에게서 허용받고 캐치·반환의 준비를 수행했다. 공식 경기 호출·출전분·공격 성공은 아직 얻지 않았다.',
            'source_cp2_exit': '정상 조합과 예외 조건을 구분한 역할 제안',
            'published_episode_number': None, 'manuscript_word_count': None,
        },
        {
            'id': 'A07-EF-002', 'global_function_order': 38, 'planned_allocation_slot': 324,
            'primary_subact': 'A07-S2', 'source_conditional_functions': ['A07-CF03', 'A07-CF04'],
            'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
            'entry_state': None,
            'single_function': '다른 수비 도착 시점에서 자기 짧은 공격과 반환 실패·수정을 직접 구별한다',
            'unit_choice': [cf[2]['choice'], cf[3]['choice']],
            'direct_present_cost': [cf[2]['direct_cost'], cf[3]['direct_cost']],
            'beats': [
                {'id': 'A07-R2-B1', 'action': '허용된 가상 라이브 팀 훈련의 첫 시험에서 안쪽 수비가 남아 있는 것을 보고 짧게 전진하지만 수비 앞에서 더 밀고 들어갈 창이 닫힌다. 주인공은 동료에게 처음부터 넘길 수 있었던 전개 시간을 썼다는 사실을 직접 본다. 득점·실제 NBA 경기 통계는 정하지 않는다.', 'classification': 'SELECTED_FICTIONAL_LIVE_PRACTICE_LIMIT_OBSERVED'},
                {'id': 'A07-R2-B2', 'action': '별도 같은 허용 훈련의 시험에서는 도움이 캐치 전에 가까워진다. 주인공의 첫 반환 판단이 늦어져 동료가 늦은 시계를 받고, 그는 자신의 슛을 더 시험하려던 동작을 접는다.', 'classification': 'SELECTED_FICTIONAL_EARLY_HELP_RETURN_FAILURE_OBSERVED'},
                {'id': 'A07-R2-B3', 'action': '같은 좁은 과제를 다시 허용받은 다음 시험에서 주인공은 조기 도움을 보자 바로 반환하고 동료 전개를 가리지 않는 자리로 옮긴다. 이 재시도는 자기 판단·이동의 국소 수행만 보이며 동료 득점과 실전 반복 효율을 인증하지 않는다.', 'classification': 'SELECTED_FICTIONAL_BOUNDED_RETRY_NOT_GAME_RESULT'},
            ],
            'exit_state': '허용된 가상 라이브 팀 훈련에서 안쪽 유지 수비 앞 짧은 공격의 닫힌 창과 캐치 전 조기 도움 앞 늦은 반환을 각각 보았고, 다음 좁은 재시도에서 빠른 반환·재배치를 직접 수행했다. 득점·실제 경기 효율·항상 맞는 엘보 카운터는 아직 증명되지 않았다.',
            'source_cp2_exit': '통하는 조건과 중단할 조건이 구별된 엘보 카운터 표본',
            'published_episode_number': None, 'manuscript_word_count': None,
        },
        {
            'id': 'A07-EF-003', 'global_function_order': 39, 'planned_allocation_slot': 325,
            'primary_subact': 'A07-S3', 'source_conditional_functions': ['A07-CF05', 'A07-CF06'],
            'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
            'entry_state': None,
            'single_function': '좋은 재시도와 실패를 함께 역할 자료에 싣고 평가 권한을 넘긴다',
            'unit_choice': [cf[4]['choice'], cf[5]['choice']],
            'direct_present_cost': [cf[4]['direct_cost'], cf[5]['direct_cost']],
            'beats': [
                {'id': 'A07-R3-B1', 'action': '주인공은 허용된 자신의 연습 영상에서 닫힌 공격 창·늦은 반환과 다음 재시도를 같이 대조한다. 코치에게는 자기 호출을 넓혀 달라고 주장하기보다 안쪽 유지 때의 짧은 시험과 조기 도움 때의 빠른 반환이라는 한정 조건을 다시 요청한다.', 'classification': 'SELECTED_FICTIONAL_OWN_OBSERVATION_AND_COACH_REQUEST'},
                {'id': 'A07-R3-B2', 'action': '그는 자기에게 전달 가능한 좋은 장면과 실패·아직 미증명인 실전 반복성을 구분해 가상 에이전트에게 역할 평가 자료로 건넨다. 완성된 공격수처럼 실패를 가릴 기회를 포기하며, 에이전트의 가격 평가나 계약 답은 받지 않는다.', 'classification': 'SELECTED_FICTIONAL_MIXED_SAMPLE_HANDOFF_NO_MARKET_ANSWER'},
            ],
            'exit_state': cf[5]['changed_state'],
            'source_cp2_exit': '2022 역할 평가와 E2 협상에 넘길 조건부 자료 기준',
            'published_episode_number': None, 'manuscript_word_count': None,
        },
    ]
    for i in range(1, len(functions)):
        functions[i]['entry_state'] = functions[i - 1]['exit_state']
    return {
        'schema': 'A07_FINITE_FUNCTION_BATCH_V1',
        'status': 'THREE_LOCAL_FINAL_FUNCTIONS_INDEPENDENTLY_REVIEWED', 'independent_review_completed': True,
        'previous_function': {'id': 'A06-EF-005', 'path': PREVIOUS, 'exact_full_exit': prior_exit},
        'functions': functions, 'conditional_M1_carrier': {'path': M1, 'rows': 164, 'date_state_selected': False,
                                                            'historical_OT_copied_as_fiction': False},
        'operating_conditions': {'fictional_coach_limited_practice_grant_selected': True,
                                 'two_distinct_defensive_practice_conditions_selected': True,
                                 'practice_failure_and_one_retry_observed': True,
                                 'actual_NBA_games_or_performance_certified': False},
        'A08_entry_exact_candidate_state': cf[5]['changed_state'],
        'new_final_functions_registered': 0,
        'whole_A07_complete': False, 'bounded_A07_subact_operating_exits_proposed': 3,
        'actual_2021_22_date_availability_wins_or_efficiency_certified': False,
        'actual_contract_price_or_agent_market_answer_certified': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'manuscript_count': 0, 'manuscript_allowed': False,
        'author_locked': False, 'design_gate': 'CLOSED',
        'source_semantic_sha256': SEMANTIC_SHA,
        'source_hash_method': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_sha256': {p: sha((root / p).read_bytes()) for p in SOURCES},
    }


def render(data):
    lines = ['# A07 2021–22 세 대표 국소 기능', '',
             '기존 6개 인과 후보를 세 소막의 기능 3개로 묶었다. 가상 허용 팀 훈련의 행동과 실제 NBA 경기·분·효율·계약 답을 구분한다.', '']
    for row in data['functions']:
        lines += [f"## {row['id']} · {row['primary_subact']}", '',
                  f"- 입력: {row['entry_state']}", f"- 기능: {row['single_function']}"]
        lines += [f"- {beat['id']}: {beat['action']}" for beat in row['beats']]
        lines += [f"- 출구: {row['exit_state']}", '']
    lines += ['M1 82일×2조건부 분은 역할 가능성의 산술 입력이고 어느 날짜의 건강·경기 결과도 선택하지 않는다. '
              '계획 슬롯 323–325는 출판 회차가 아니며 나머지 57슬롯을 새 사건으로 채우지 않는다.',
              '', '세 국소 기능의 독립 검문 완료·중앙 등록 전 상태다. 전체 A07/G13/G14·실제 Context Pack·원고 미완료, 설계·원고 게이트 `CLOSED`.', '']
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        return [] if data == build(root) else ['A07 batch differs from source-bound build']
    except (AssertionError, KeyError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']


def self_test(data):
    for name, mutation in [
        ('season winners', lambda x: x.update(actual_2021_22_date_availability_wins_or_efficiency_certified=True)),
        ('contract market answer', lambda x: x.update(actual_contract_price_or_agent_market_answer_certified=True)),
        ('practice success hardcoded', lambda x: x['functions'][1].update(exit_state='실제 NBA 경기에서 엘보 카운터로 득점을 보장했다')),
    ]:
        changed = copy.deepcopy(data)
        mutation(changed)
        assert validate(changed), name
    original_load = load
    def altered_m1(root, path):
        value = original_load(root, path)
        if path == M1:
            value = copy.deepcopy(value)
            value['rows'][0]['player_minutes']['LaMelo_pick4'] = 0
            value['rows'][0]['player_minutes']['Protagonist'] = 64
        return value
    globals()['load'] = altered_m1
    try:
        try:
            build()
        except AssertionError:
            pass
        else:
            raise AssertionError('same-total M1 player identity reversal accepted')
    finally:
        globals()['load'] = original_load
    return 4


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / OUTPUT.with_suffix('.md')).write_text(render(data), encoding='utf-8')
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors = validate(saved)
        if (ROOT / OUTPUT.with_suffix('.md')).read_text(encoding='utf-8') != render(saved):
            errors.append('Markdown differs')
        print(json.dumps({'current': not errors, 'errors': errors, 'functions': len(saved['functions'])}))
        if errors:
            raise SystemExit(1)
    if args.self_test:
        print(json.dumps({'negative_controls': self_test(data)}))


if __name__ == '__main__':
    main()
