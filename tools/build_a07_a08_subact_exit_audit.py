"""Audit bounded CP2 exits for the six reviewed A07/A08 local functions."""

import argparse
import hashlib
import json
from pathlib import Path

import build_a07_finite_function_batch as a07_builder
import build_a08_finite_function_batch as a08_builder
import build_a07_opening_game_elbow_observation_family as game_builder
import build_a08_s1_current_rt_cost_slot_family as rt_builder


ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a07_a08_subact_exit_audit.py'
A07 = str(a07_builder.OUTPUT).replace('\\', '/')
A08 = str(a08_builder.OUTPUT).replace('\\', '/')
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
OUTPUT = Path('design/A07_A08_SUBACT_EXIT_AUDIT_2026_10_07.json')
GAME = game_builder.OUT
RT = str(rt_builder.OUTPUT).replace('\\', '/')
SOURCES = (SELF, A07, A08, CP2, GAME, game_builder.SELF, RT, str(rt_builder.SELF).replace('\\', '/'))
CP2_SUCCESS_CRITERIA_SHA = 'b205b4d8eb3ff7e956ec8c2ce2fbb9018b0969bde4a9fb033ff295f1df53e902'


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def sha(raw):
    normalized = raw.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def build(root=ROOT):
    a07, a08, cp2 = (load(root, p) for p in (A07, A08, CP2))
    assert a07 == a07_builder.load(root, a07_builder.OUTPUT)
    assert a08 == a08_builder.load(root, a08_builder.OUTPUT)
    assert not a08_builder.validate(a08, root=root), 'A08 and A07 reviewed source-current required'
    assert a07['independent_review_completed'] and a08['independent_review_completed']
    f = {x['id']: x for x in a07['functions'] + a08['functions']}
    assert list(f) == [f'A07-EF-{i:03d}' for i in range(1, 4)] + [f'A08-EF-{i:03d}' for i in range(1, 4)]
    assert a07['functions'][-1]['exit_state'] == a08['functions'][0]['entry_state']
    assert a08['functions'][1]['source_CF03_actual_NBA_game_trial_executed'] is False
    assert a08['functions'][1]['full_A08_S2_cp2_exit_certified'] is False
    assert a08['A08_S2_actual_game_and_full_cp2_exit_hold']
    sub = {x['id']: x for x in cp2['subacts'] if x['parent_act'] in ('A07', 'A08')}
    act = {x['id']: x for x in cp2['acts'] if x['id'] in ('A07', 'A08')}
    assert len(sub) == 6 and len(act) == 2
    criteria_rows = [[x['id'], x.get('success_criteria', [])]
                     for x in cp2['subacts'] if x['parent_act'] in ('A07', 'A08')]
    criteria_raw = json.dumps(criteria_rows, ensure_ascii=False, sort_keys=True,
                              separators=(',', ':')).encode('utf-8')
    assert hashlib.sha256(criteria_raw).hexdigest() == CP2_SUCCESS_CRITERIA_SHA
    game, rt = load(root, GAME), load(root, RT)
    assert not game_builder.validate(game)
    assert game['certification']['independent_review_completed']
    assert game['root_working_selection']['two_calls_and_own_observation_route_selected']
    assert not game['root_working_selection']['whole_game_or_season_historical_lock']
    assert len(game['new_modeled_game_observations']) == 2
    assert rt == rt_builder.build(root)
    assert rt['independent_review_completed'] and len(rt['formula_rows']) == 192
    assert rt['summary']['current_policy_cell_rows'] == 768
    assert rt['fictional_agent_handoff']['same_E40_proposal_material']
    assert rt['RT_policy_selected'] is None and not rt['actual_FY22_roster_or_tax_bill_certified']

    specifications = [
        ('A07-S1', ['A07-EF-001'], 'PASS_BOUNDED_OPERATING_EXIT',
         'M1 정상/COBY_OUT의 역할 비용을 명시해 좁은 엘보 과제를 요청했고 가상 코치가 실제 허용 훈련의 과제를 맡겼다.',
         '특정 날짜 출전·양팀 분·실제 경기 공격 호출은 미인증.', None),
        ('A07-S2', ['A07-EF-002'], 'PASS_CONDITIONAL_BOUNDED_GAME_SAMPLE_CRITERIA',
         '기존 연습 뒤 개막CHI–DET 공통5인가용·적법명단 조건의 가상 두호출을 설계로 채택했다. 오른엘보/강한쪽조기도움/LaMelo반환/2초·7초 후속슛 모두MISS를 함께 기록하고 빠른 판단을 득점성공과 분리했다. 원240/480분은 보존한다.',
         'NBA 실경기 효율·득점·모든 수비 조건에서의 숙련은 미인증.',
         None),
        ('A07-S3', ['A07-EF-003'], 'BOUNDED_ACTION_OBSERVED_CP2_CRITERIA_HOLD',
         '실패 영상과 수정 시도를 함께 코치에게 제시하고 가상 에이전트에게 좋은/막힌 역할 자료를 건네는 선택과 과시 기회 비용이 보인다.',
         '시장 평점·협상 가격·계약 수락·프런트 동의는 미인증.',
         '좋은 경기만 고르지 않은 실제 출전·상대 대응/효율 변동의 역할 평가 자료는 아직 없다. 연습 영상의 실패만으로 시즌 평가를 대체하지 않는다.'),
        ('A08-S1', ['A08-EF-001'], 'PASS_CONDITIONAL_COST_LINK_CRITERIA_CONTRACT_EVENT_HOLD',
         'E40과 같은 자료에 현재192×4 동일6범주의RT1–RT4 자리/잔여비용 함수를 연결해 가상 에이전트가 접수했다. Bradley H_B와 Valentine 보호비용을 보존하고 동료할인/새UPC/프런트수락을 가정하지 않았다.',
         '에이전트 전달은 프런트 수락이나 정확 E2 가격·다른 선수 서명과 다르다.',
         '성공기준의 조건부 비용 연결은 종료했다. 원 irreversible_choice의 실제 자기계약 예산 사용·E2 기관 결정은 미선택이며 전체 소막 확정은 HOLD다.'),
        ('A08-S2', ['A08-EF-002'], 'HOLD_ACTUAL_GAME_TRIAL_FOR_FULL_CP2_EXIT',
         '첫 반환 차단 가상 팀훈련의 늦은 각도 오류·열린 수신자에게 수정 전달·다른 닫힌 길의 안전 재전개는 직접 수행했다.',
         '원 CF03의 NBA 실경기 시험, 실제 압박 속 정확성·턴오버·사용/중단 반복 표본은 인증하지 않는다.',
         '허용된 실제 경기의 첫 반환 차단 시험과 그 오류에 근거한 사용·중단 조건은 아직 없다.'),
        ('A08-S3', ['A08-EF-003'], 'HOLD_GAME_ROLE_FOR_FULL_CP2_EXIT',
         '허용된 가상 팀훈련에서 자기 짧은 창을 시험하고 동료 우위가 보인 다른 흐름에서는 공을 넘긴 뒤 재관여 위치로 움직였다.',
         '경기별 공격 권한·공동 에이스 지정·동료 마무리·클로징 배분을 관측하지 않았다.',
         '실제 맡은 경기 역할 안의 선택·재관여와 감독의 경기별 권한은 아직 없다.'),
    ]
    rows = []
    for sid, ids, result, reason, bounded_not_claimed, gap in specifications:
        source = sub[sid]
        last = f[ids[-1]]
        assert last['primary_subact'] == sid
        rows.append({
            'subact_id': sid, 'cp2_entry_state': source['entry_state'],
            'cp2_choice': source['choice'], 'cp2_cost': source['cost'],
            'cp2_exit_state': source['exit_state'], 'evidence_function_ids': ids,
            'evidence_paths': [A07 if sid.startswith('A07') else A08] + ([GAME] if sid == 'A07-S2' else [RT] if sid == 'A08-S1' else []),
            'last_exact_exit': last['exit_state'],
            'observed_action_cost_authority_reason': reason,
            'bounded_not_claimed': bounded_not_claimed,
            'specific_gap': gap, 'exit_audit_result': result,
            'cp2_success_criteria': source.get('success_criteria', []),
            'source_criteria_bounded_pass': sid in ('A07-S1', 'A07-S2', 'A08-S1'),
            'source_criteria_conditional_family_only': sid in ('A07-S2', 'A08-S1'),
            'full_irreversible_contract_event_hold': sid == 'A08-S1',
            'local_function_action_observed': True,
            'whole_historical_season_or_NBA_game_certified': False,
        })
    act_rows = [
        {
            'act_id': 'A07', 'cp2_choice': act['A07']['choice'],
            'cp2_cost': act['A07']['cost'], 'cp2_exit_state': act['A07']['exit_state'],
            'evidence_function_ids': [f'A07-EF-{i:03d}' for i in range(1, 4)],
            'last_exact_exit': f['A07-EF-003']['exit_state'],
            'functional_exit_audit_result': 'BOUNDED_AGENT_HANDOFF_OBSERVED_ACT_EXIT_HOLD',
            'observed_reason': '동료 기회 비용을 보인 제한 과제→두 수비 조건의 실패/재시도→실패까지 포함해 에이전트에게 넘긴 표본은 첫 장기 계약 협상의 자기 자료로 성립한다.',
            'specific_gap': '원 A07 Act 비용의 실전 효율 변동과 S3의 실제 출전/상대 대응 자료가 없어 첫 장기계약 협상의 전체 표본으로 확정할 수 없다. 82경기 전체 건강이나 사적 협상 접수증을 새 전제로 요구하지 않는다.',
            'bounded_not_claimed': '협상 결과·정확 계약 가격·시장 평가·시즌 승패는 인증하지 않는다.',
        },
        {
            'act_id': 'A08', 'cp2_choice': act['A08']['choice'],
            'cp2_cost': act['A08']['cost'], 'cp2_exit_state': act['A08']['exit_state'],
            'evidence_function_ids': [f'A08-EF-{i:03d}' for i in range(1, 4)],
            'last_exact_exit': f['A08-EF-003']['exit_state'],
            'functional_exit_audit_result': 'HOLD_CONTRACT_AND_GAME_AUTHORITY',
            'observed_reason': '역할/동료 기능의 예산 질문과 훈련의 첫 반환 차단·이양 후 재관여는 직접 보인다.',
            'specific_gap': 'E2 기관 결정·예산 책임과 NBA 실경기 사용/중단 및 경기별 공동 공격 권한이 아직 선택·관측되지 않았다.',
            'bounded_not_claimed': '연습 수행을 계약 수락·실제 경기 배분·공동 에이스 지위로 읽지 않는다.',
        },
    ]
    return {
        'schema': 'A07_A08_SUBACT_EXIT_AUDIT_V1',
        'status': 'INDEPENDENTLY_REVIEWED_SOURCE_CRITERIA_EXIT_AUDIT',
        'independent_review_completed': True,
        'independent_review_basis': 'g11 separately read original CP2 A07-S2/A08-S1 criteria and current source families. Conditional game/cost criteria pass with 3 remaining criteria and 2 act HOLDs; no dependency cycle. Actual loader-return MISS-to-MADE and RT4 Valentine protected2193930-to-zero mutations rejected. Author self-tests are not counted as independent checks.',
        'counts': {'subact_exits_audited': 6, 'local_function_actions_observed': 6,
                   'subact_source_criteria_bounded_pass': 3,
                   'subact_source_criteria_conditional_family_pass': 2,
                   'full_irreversible_contract_event_hold': 1,
                   'subact_source_criteria_specific_hold': 3, 'act_exits_audited': 2,
                   'act_source_exit_pass': 0, 'act_specific_hold': 2,
                   'registered_local_functions_reused': 6,
                   'new_episode_functions_added': 0,
                   'planned_A07_A08_slots': 120,
                   'planned_slots_are_mandatory_new_events': False},
        'subact_exit_rows': rows, 'act_exit_rows': act_rows,
        'a07_to_a08_exact_handoff': a07['functions'][-1]['exit_state'],
        'whole_A07_and_A08_historical_seasons_complete': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'manuscript_count': 0, 'manuscript_allowed': False,
        'new_author_lock': False, 'design_gate': 'CLOSED',
        'source_hash_method': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_sha256': {p: sha((root / p).read_bytes()) for p in SOURCES},
    }


def render(data):
    lines = ['# A07·A08 소막·막 출구 한정 감사', '',
             '기존6기능을 보존한다. 원성공기준의 한정관측1개와 조건부 설계 비교2개를 수용하고 남은기준3개는HOLD다. 조건부 두개는 개막40초의 두플레이 설계와 현재RT 비용연결이다. A08-S1 실제E2 예산사용/기관결정은 여전히HOLD이며 두막/전체시즌·계약 결과를 확정하지 않는다. 새등록기능0.', '',
             '|소막|판정|관측 근거|정확 남은 공백|', '|---|---|---|---|']
    for row in data['subact_exit_rows']:
        lines.append('|{}|{}|{}|{}|'.format(row['subact_id'], row['exit_audit_result'],
                                            row['observed_action_cost_authority_reason'],
                                            row['specific_gap'] or '국소 출구 공백 없음'))
    lines += ['', '|막|판정|남은 범위|', '|---|---|---|']
    for row in data['act_exit_rows']:
        lines.append('|{}|{}|{}|'.format(row['act_id'], row['functional_exit_audit_result'],
                                       row['specific_gap'] or row['bounded_not_claimed']))
    lines += ['', 'A07은 실패를 포함한 연습자료와 별도 조건부 개막 두관측을 구분한다. 두슛은 모두실패이며 이를 시즌효율/출전평가로 확장하지 않는다. '
              'A08 G8의 현재비용 연결은 종료했지만 E2 기관결정과 라이브패스 실경기/경기별역할은 훈련이나 비용표로 대체되지 않는다.',
              '', '82경기 건강·사적 영수증을 새로운 전제 게이트로 추가하지 않는다. '
              '전체 G13/G14·실제 Pack·원고는 미완료이며 설계·원고 게이트는 `CLOSED`다.', '']
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        return [] if data == build(root) else ['exit audit differs from source-bound build']
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
        print(json.dumps({'current': not errors, 'errors': errors,
                          'subacts': len(saved['subact_exit_rows'])}))
        if errors:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
