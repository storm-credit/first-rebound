"""Map existing A07/A08 candidates to six bounded function groups, without promotion."""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a07_a08_finite_function_preparation.py'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
A07 = 'design/A07_2021_22_CONDITIONAL_FUNCTIONS.json'
A08 = 'design/A08_2022_23_CONDITIONAL_FUNCTIONS.json'
M1 = 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json'
OUTPUT = Path('design/A07_A08_FINITE_FUNCTION_PREPARATION_2026_10_07.json')
SOURCES = (SELF, CP2, A07, A08, M1)
CONSUMED_MEANING_SHA = '99781820e119eaf40cdbbc1e967c04e6e43241762a65a81d3b853c0897c78c78'


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def sha(raw):
    normalized = raw.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def build(root=ROOT):
    cp2, a07, a08, m1 = (load(root, p) for p in (CP2, A07, A08, M1))
    meaning = {'acts': [x for x in cp2['acts'] if x['id'] in ('A07','A08')],
               'subacts': [x for x in cp2['subacts'] if x['parent_act'] in ('A07','A08')],
               'functions': a07['functions'] + a08['functions']}
    digest = hashlib.sha256(json.dumps(meaning, ensure_ascii=False, sort_keys=True,
                                      separators=(',', ':')).encode('utf-8')).hexdigest()
    assert digest == CONSUMED_MEANING_SHA, 'consumed A07/A08 choice/cost/exit meaning changed; re-review required'
    acts = {x['id']: x for x in cp2['acts'] if x['id'] in ('A07', 'A08')}
    subacts = {x['id']: x for x in cp2['subacts'] if x['parent_act'] in ('A07', 'A08')}
    f07, f08 = a07['functions'], a08['functions']
    assert [x['id'] for x in f07] == [f'A07-CF{i:02d}' for i in range(1, 7)]
    assert [x['id'] for x in f08] == [f'A08-CF{i:02d}' for i in range(1, 6)]
    assert [x['subact'] for x in f07] == ['A07-S1'] * 2 + ['A07-S2'] * 2 + ['A07-S3'] * 2
    assert [x['subact'] for x in f08] == ['A08-S1'] + ['A08-S2'] * 3 + ['A08-S3']
    assert acts['A07']['exit_state'] == '첫 장기 계약 협상 표본'
    assert acts['A08']['exit_state'] == '공동 에이스 권한과 예산 책임'
    assert subacts['A07-S2']['exit_state'] == '통하는 조건과 중단할 조건이 구별된 엘보 카운터 표본'
    assert subacts['A08-S2']['exit_state'] == '압박 속 라이브 패스의 사용/중단 조건을 가진 표본'
    assert f07[-1]['changed_state'] == f08[0]['entry_state']
    for item in f07 + f08:
        assert item['evidence_class'] == 'CANDIDATE' and not item['selected_event']
        assert item['episode_number'] is None and not item['manuscript_allowed']
    assert m1['status'] == 'INDEPENDENTLY_REVIEWED_CONDITIONAL_82DATE_TWO_STATE_REGULATION_CARRIER'
    assert m1['summary']['date_keys'] == 82 and m1['summary']['rows'] == 164
    assert m1['summary']['unordered_blocks'] == 1804 and m1['summary']['hypothetical_player_block_cells'] == 9020
    assert m1['summary']['executed_date_state_choices'] == 0
    assert m1['summary']['actual_new_game_results'] == 0

    definitions = [
        ('A07-S1', ('A07-CF01', 'A07-CF02'),
         '조건부 M1 정상/COBY_OUT 역할표에서 동료의 시작·공간 몫을 보여 준 뒤 코치에게 제한 엘보 시험을 요청하고 허용된 준비를 수행한다.',
         '가상 코치가 기존 허용 훈련 안에서 좁은 엘보 시험을 실제로 맡기고 주인공이 캐치·반환 준비를 수행한다. 어느 날짜의 출전·양팀 분·정상가용성을 확정하지 않는다.',
         '리바운드 뒤 직접 전진을 반복할 기회와 동료의 시작·공간 비용을 보인다.'),
        ('A07-S2', ('A07-CF03', 'A07-CF04'),
         '안쪽 수비가 남는 조건의 짧은 자기 공격과 캐치 전 도움이 다가오는 별도 조건의 즉시 반환을 각각 허용된 시험에서 선택한다.',
         '두 다른 수비 도착 시점의 자기 창·반환 지연·다음 위치만 좁게 기록한다. 득점·실전 효율·상대 NBA 경기 결과는 열어 둔다.',
         '첫 공격 때 동료의 다른 전개, 반환 때 자기 슛과 남은 시계를 실제 선택 비용으로 남긴다.'),
        ('A07-S3', ('A07-CF05', 'A07-CF06'),
         '실제로 생긴 막힌 캐치/늦은 반환만 허용 영상에서 대조해 제한 호출을 수정하고 좋은 장면과 실패를 함께 역할 자료로 정리한다.',
         '코치에게 수정 범위를 요청하고 에이전트에게 자기 자료를 전달한 상태까지만 관측한다. 수락·시장 평점·계약값은 미선택이다.',
         '완성된 공격수로 보일 기회와 더 넓은 호출을 먼저 요구할 기회를 줄인다.'),
        ('A08-S1', ('A08-CF01',),
         '이전 조건부 자료로 자기 역할 요구와 연결·외곽·센터 기능 비용을 함께 에이전트에게 설명하고, 공개 가능한 비교만 질문한다.',
         '자기 요구/팀 필요 기능을 함께 제시한 기록까지만 관측한다. 에이전트·프런트의 승인, E2 가격·다른 선수 서명은 별도다.',
         '휴식이나 자기 기술 반복에 쓸 시간을 가격과 동료 기능의 자료 준비에 사용한다.'),
        ('A08-S2', ('A08-CF02', 'A08-CF03', 'A08-CF04'),
         '첫 반환이 닫힌 허용 훈련에서 짧은 드리블 각도·안전 재전개를 연습하고, 별도 허용 시험에서 관측된 오류만 사용/중단 기준으로 고친다.',
         '실제 허용 시험과 오류 자료가 있어야 실전 선택·수정 단계로 간다. 턴오버·성공·상시 라이브패스 권한은 미리 쓰지 않는다.',
         '기존 편한 반환 반복, 공격 시간, 실패 때 자기 만회 대신 수비 복귀의 몸과 시간을 비용으로 둔다.'),
        ('A08-S3', ('A08-CF05',),
         '받은 역할 안에서 자기 짧은 우위와 동료의 관측된 우위를 구별하고, 넘긴 뒤 재관여 위치를 다시 잡는 좁은 시험을 한다.',
         '그때의 공격/이양/재관여만 관측한다. 공동 에이스 직위·클로징 권한·팀 성과는 선택하거나 인증하지 않는다.',
         '자기 슛 기회 일부를 양도하고 공 없는 다음 위치와 실패 책임을 부담한다.'),
    ]
    groups = []
    for sid, ids, action, observation, cost in definitions:
        source = f07 if sid.startswith('A07') else f08
        selected = [x for x in source if x['id'] in ids]
        assert tuple(x['id'] for x in selected) == ids
        groups.append({
            'subact': sid, 'candidate_ids': list(ids), 'source_candidate_choices': [x['choice'] for x in selected],
            'source_candidate_costs': [x['direct_cost'] for x in selected],
            'operating_action_to_test': action, 'minimum_observable_witness': observation,
            'direct_cost_to_show': cost, 'source_cp2_exit': subacts[sid]['exit_state'],
            'fictional_operating_condition_selected': sid == 'A07-S1',
            'fictional_coach_narrow_practice_grant_observed': sid == 'A07-S1',
            'actual_nba_game_assignment_or_private_staff_receipt_certified': False,
            'final_episode_function_complete': False, 'whole_subact_exit_pass': False,
        })
    return {
        'schema': 'A07_A08_FINITE_FUNCTION_PREPARATION_V1',
        'status': 'INDEPENDENTLY_REVIEWED_SIX_REPRESENTATIVE_PREPARATION_GROUPS',
        'independent_review_completed': True,
        'entry_from_global_function': 36,
        'existing_conditional_candidates': 11, 'representative_groups': groups,
        'planned_allocation_units': {'A07': acts['A07']['planned_units'], 'A08': acts['A08']['planned_units']},
        'allocation_is_mandatory_new_event_count': False,
        'M1_carrier': {'path': M1, 'date_keys': 82, 'conditional_rows': 164,
                       'unordered_blocks': 1804, 'date_state_selected': False,
                       'opponent_dated_minutes_and_winners_selected': False},
        'cross_act_handoff': f07[-1]['changed_state'],
        'exact_E2_contract_or_staff_receipts_certified': False,
        'new_final_episode_functions_registered': 0,
        'important_future_results_selected': False, 'whole_A07_complete': False, 'whole_A08_complete': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED', 'author_locked': False,
        'source_hash_method': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_sha256': {p: sha((root / p).read_bytes()) for p in SOURCES},
    }


def render(data):
    lines = ['# A07·A08 유한 대표기능 준비', '',
             '기존 조건부 인과 기능 11개를 소막별 6개 기능 묶음으로 정리했다. 새 최종 기능·회차·경기 결과·계약 결과를 확정하지 않았다.', '',
             '2021–22 M1 날짜별 조건부 분 carrier는 이미 구현되어 있다. NORMAL/COBY_OUT 164행은 날짜별 가용성 선택이나 승패가 아니다.', '',
             '|소막|기존 후보|시험할 행동|최소 관측|직접 비용|', '|---|---|---|---|---|']
    for row in data['representative_groups']:
        lines.append('|{}|{}|{}|{}|{}|'.format(row['subact'], ', '.join(row['candidate_ids']),
                                               row['operating_action_to_test'], row['minimum_observable_witness'],
                                               row['direct_cost_to_show']))
    lines += ['', 'A07의 평가 자료는 A08의 질문으로 넘어갈 수 있지만 실제 계약·공동 에이스 권한은 아직 없다. '
              '작업 모델의 허용 훈련·시험은 실제 82경기 결과나 사적 영수증을 대신하지 않는다.',
              '', '전체 A07/A08, G13/G14, 실제 Context Pack, 원고는 미완료다. 설계·원고 게이트는 `CLOSED`다.', '']
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        return [] if data == build(root) else ['preparation differs from source-bound build']
    except (AssertionError, KeyError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
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
        print(json.dumps({'current': not errors, 'errors': errors, 'groups': len(saved['representative_groups'])}))
        if errors:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
