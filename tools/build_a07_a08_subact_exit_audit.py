"""Audit bounded CP2 exits for the six reviewed A07/A08 local functions."""

import argparse
import hashlib
import json
from pathlib import Path

import build_a07_finite_function_batch as a07_builder
import build_a08_finite_function_batch as a08_builder
import build_a07_opening_game_elbow_observation_family as game_builder
import build_a08_s1_current_rt_cost_slot_family as rt_builder
import build_a07_changed_defense_role_evaluation as defense_builder
import build_a08_conditional_game_call_family as call_builder


ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a07_a08_subact_exit_audit.py'
A07 = str(a07_builder.OUTPUT).replace('\\', '/')
A08 = str(a08_builder.OUTPUT).replace('\\', '/')
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
OUTPUT = Path('design/A07_A08_SUBACT_EXIT_AUDIT_2026_10_07.json')
GAME = game_builder.OUT
RT = str(rt_builder.OUTPUT).replace('\\', '/')
DEFENSE = defense_builder.OUT
CALLS = call_builder.OUT
SOURCES = (DEFENSE, defense_builder.SELF, CALLS, call_builder.SELF, SELF, A07, A08, CP2, GAME, game_builder.SELF, RT, str(rt_builder.SELF).replace('\\', '/'))
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

    defense, calls = load(root, DEFENSE), load(root, CALLS)
    assert defense == defense_builder.build()
    assert calls == call_builder.build()
    assert defense['certification']['independent_review_completed']
    assert defense['root_working_selection']['two_new_coach_calls_and_own_mixed_record_transfer_selected']
    assert calls['certification']['independent_review_completed']
    assert calls['certification']['root_conditional_working_design_selection']
    assert len(calls['bounded_game_calls']) == 5
    assert calls['cp2_contract']['S2_catch_immediate_vs_dribble_then_pass_comparison_modeled']
    assert calls['cp2_contract']['S3_source_success_criteria_condition_explanation_bounded_pass']
    assert not calls['cp2_contract']['S3_whole_subact_exit_or_game_authority_complete']
    assert not calls['certification']['E2_contract_price_or_acceptance_selected']

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
    updates = {
        'A07-S3': ('PASS_CONDITIONAL_CHANGED_DEFENSE_COMPARISON_CRITERIA',
                   '원 조기도움2와 새 안쪽유지/늦은도움2를 분리하고 국소판단 2적절/2실패를 모두 에이전트의 자기자료에 남긴다. 기존 두MISS와 새슛null, 원240/480분·M1동료 분기회비용을 보존한다.',
                   '전체 시즌 효율·실제 베테랑 DNP·시장가격/협상수락은 인증하지 않는다.', None),
        'A08-S2': ('PASS_CONDITIONAL_COMPARISON_DESIGN_ACTUAL_GAME_EXIT_HOLD',
                   '새5창 중 즉시캐치반환·드리블뒤막힌길TO/복귀·드리블뒤별도열린길재전개를 다른 조건부 표본으로 분류한다. 팀14,400초 수학적 용량은 실제 계약/명단/교대벡터가 아니다.',
                   '조건부 비교만 지원하며 실제 실전 실행·전체 소막은HOLD다.',
                   '선택된 적법2022계약/양측가용10인/실제창배치가 미완료. 82경기 건강이나 사적 접수증을 추가 요구하지 않는다.'),
        'A08-S3': ('PASS_BOUNDED_FINISH_CONDITION_EXPLANATION_GAME_AUTHORITY_HOLD',
                   '자기 짧은길 계속개방/동료의 더빠른열린길이라는 두마무리 조건을 설명하고 각자의 점유포기/다음판단/실패책임을 남긴다. 원 기준은 설명이며 양쪽 실제마무리 결과를 새 필수게이트로 넣지 않는다.',
                   '실제마무리·경기별공동에이스/클로징 권한·2028수신/득점은 미확정이다.',
                   '전체소막의 경기별권한과 준비책임은 미선택. 조건설명 지원과 전체출구HOLD를 구별한다.'),
    }
    specifications = [(sid, ids, *updates[sid]) if sid in updates else row
                      for row in specifications for sid, ids in [row[:2]]]
    rows = []
    for sid, ids, result, reason, bounded_not_claimed, gap in specifications:
        source = sub[sid]
        last = f[ids[-1]]
        assert last['primary_subact'] == sid
        rows.append({
            'subact_id': sid, 'cp2_entry_state': source['entry_state'],
            'cp2_choice': source['choice'], 'cp2_cost': source['cost'],
            'cp2_exit_state': source['exit_state'], 'evidence_function_ids': ids,
            'evidence_paths': [A07 if sid.startswith('A07') else A08] + ([GAME] if sid == 'A07-S2' else [DEFENSE, GAME] if sid == 'A07-S3' else [RT] if sid == 'A08-S1' else [CALLS] if sid in ('A08-S2', 'A08-S3') else []),
            'last_exact_exit': last['exit_state'],
            'observed_action_cost_authority_reason': reason,
            'bounded_not_claimed': bounded_not_claimed,
            'specific_gap': gap, 'exit_audit_result': result,
            'cp2_success_criteria': source.get('success_criteria', []),
            'source_criteria_bounded_pass': sid in ('A07-S1', 'A07-S2', 'A07-S3', 'A08-S1', 'A08-S2', 'A08-S3'),
            'source_criteria_conditional_family_only': sid in ('A07-S2', 'A07-S3', 'A08-S1', 'A08-S2', 'A08-S3'),
            'full_irreversible_contract_event_hold': sid == 'A08-S1',
            'whole_subact_execution_or_authority_hold': sid in ('A08-S1', 'A08-S2', 'A08-S3'),
            'local_function_action_observed': True,
            'whole_historical_season_or_NBA_game_certified': False,
        })
    act_rows = [
        {
            'act_id': 'A07', 'cp2_choice': act['A07']['choice'],
            'cp2_cost': act['A07']['cost'], 'cp2_exit_state': act['A07']['exit_state'],
            'evidence_function_ids': [f'A07-EF-{i:03d}' for i in range(1, 4)],
            'last_exact_exit': f['A07-EF-003']['exit_state'],
            'functional_exit_audit_result': 'PASS_CONDITIONAL_FIRST_CONTRACT_SAMPLE_WHOLE_SEASON_HOLD',
            'observed_reason': '동료 기회 비용을 보인 제한 과제→두 수비 조건의 실패/재시도→실패까지 포함해 에이전트에게 넘긴 표본은 첫 장기 계약 협상의 자기 자료로 성립한다.',
            'specific_gap': '원 Act의 실제압박 시험/효율변동은 한정4표본의 늦은시계·국소판단 성공/실패로, 베테랑분은 M1 정상/예외 배분의 조건부 기회비용으로 기록한다. 자기자료 전달을 채택해 첫 협상의 한정표본을 지원한다. 전체시즌/실제계약·명단 확정은 별도이고, 시장가격·수락·82실적을 원 표본출구의 새 요구로 만들지 않는다.',
            'bounded_not_claimed': '협상 결과·정확 계약 가격·시장 평가·시즌 승패는 인증하지 않는다.',
        },
        {
            'act_id': 'A08', 'cp2_choice': act['A08']['choice'],
            'cp2_cost': act['A08']['cost'], 'cp2_exit_state': act['A08']['exit_state'],
            'evidence_function_ids': [f'A08-EF-{i:03d}' for i in range(1, 4)],
            'last_exact_exit': f['A08-EF-003']['exit_state'],
            'functional_exit_audit_result': 'HOLD_CONTRACT_AND_GAME_AUTHORITY',
            'observed_reason': '역할/동료 기능의 예산 질문과 훈련의 첫 반환 차단·이양 후 재관여는 직접 보인다.',
            'specific_gap': 'E2 기관 결정·예산 책임과 실제 적법2022경기 배치/경기별공동공격권한은 미선택이다. 새5창 조건부사용/중단 및 두마무리 조건설명은 지원하며 이를 다시 미작성 공백으로 세지 않는다.',
            'bounded_not_claimed': '연습 수행을 계약 수락·실제 경기 배분·공동 에이스 지위로 읽지 않는다.',
        },
    ]
    return {
        'schema': 'A07_A08_SUBACT_EXIT_AUDIT_V1',
        'status': 'INDEPENDENTLY_REVIEWED_SOURCE_CRITERIA_EXIT_AUDIT',
        'independent_review_completed': True,
        'independent_review_basis': 'g11 separately read original CP2 and all current defense/call/RT sources. One bounded observation and five conditional criterion supports, zero new criterion-writing gaps, three full A08 execution/contract/authority HOLDs and two whole Act HOLDs were verified; conditional A07 first-contract sample support is not whole season completion. No dependency cycle. Actual loader-return CD1 failed-decision-to-success and S3 condition-explanation-to-actual-finishes mutations rejected. Author self-tests are not independent checks.',
        'counts': {'subact_exits_audited': 6, 'local_function_actions_observed': 6,
                   'subact_source_criteria_bounded_pass': 6,
                   'subact_source_criteria_conditional_family_pass': 5,
                   'full_irreversible_contract_event_hold': 1,
                   'subact_source_criteria_specific_hold': 0, 'whole_subact_execution_or_authority_hold': 3, 'act_conditional_first_contract_sample_supported': 1, 'act_exits_audited': 2,
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
             '기존6기능을 보존한다. 원성공기준의 한정관측1개와 조건부 설계지원5개를 구별한다. 추가 기준작성 공백0, A08 계약·실행·권한의 전체소막HOLD3, 두막의 실제시즌/계약HOLD2다. A07 첫협상의 한정4표본 출구지원1을 별도 기록하며 전체시즌 실적/시장수락으로 승격하지 않는다. 새등록기능0.', '',
             '|소막|판정|관측 근거|정확 남은 공백|', '|---|---|---|---|']
    for row in data['subact_exit_rows']:
        lines.append('|{}|{}|{}|{}|'.format(row['subact_id'], row['exit_audit_result'],
                                            row['observed_action_cost_authority_reason'],
                                            row['specific_gap'] or '국소 출구 공백 없음'))
    lines += ['', '|막|판정|남은 범위|', '|---|---|---|']
    for row in data['act_exit_rows']:
        lines.append('|{}|{}|{}|'.format(row['act_id'], row['functional_exit_audit_result'],
                                       row['specific_gap'] or row['bounded_not_claimed']))
    lines += ['', 'A07은 실패를 포함한 연습자료와 별도 조건부 개막 두관측을 구분한다. 기존두슛은MISS/새두슛은null, 국소판단은2적절/2실패다. 한정자료를 전체시즌효율/실제출전 집계로 확장하지 않는다. '
              'A08 G8의 현재비용 연결은 종료했지만 E2 기관결정/적법실경기 실행/경기별권한은 별도다. 새5창 조건부비교·마무리조건설명을 훈련이나 계약완료로 잘못 읽지 않는다.',
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
        errors = [] if saved == data else ['exit audit differs from fresh source-bound build']
        if (ROOT / OUTPUT.with_suffix('.md')).read_text(encoding='utf-8') != render(saved):
            errors.append('Markdown differs')
        print(json.dumps({'current': not errors, 'errors': errors,
                          'subacts': len(saved['subact_exit_rows'])}))
        if errors:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
