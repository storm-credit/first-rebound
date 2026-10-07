"""Finite Chicago A working execution; no complete-cost or macro3 certificate.

Reuse fixed origins and G7 recommendations. Model new dates/order explicitly;
do not copy actual negotiation, invent #16 ownership or turn missing costs into0.
"""
import argparse
import copy
import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_2021_approved_a_draft_signing_execution.py'
OUT = 'simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json'
MD = OUT[:-5] + '.md'
A3 = 'simulation/NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json'
G7 = 'simulation/NBA_2021_FULL_DRAFT_COMPARISON.json'
M1 = 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json'
A = 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json'
SEQ = 'simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE_INPUTS.json'
G8 = 'simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json'
BASE = 'simulation/CHICAGO_2021_23_CONTINUATION.json'
ROLE = 'simulation/CHICAGO_2021_M1_ROLE_WITNESS.json'
SOURCES = [A3, G7, M1, A, SEQ, G8, BASE, ROLE, 'AGENTS.md',
           'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json',
           'research/CHICAGO_2021_23_CONTRACT_SEQUENCE_SOURCES.json',
           'research/CHICAGO_2021_23_CONTINUATION_SOURCES.json',
           'research/O15G15BF_GREEN_2021_RFA_ORDER_AND_QO_CHARGE.md',
           'research/O15G15AY_CHICAGO_2021_TWO_WAY_SLOT_SCREEN.md',
           'research/O15G15AZ_SIMONOVIC_2021_ACTIVATION_SLOT_GATE.md',
           'tools/build_2020_21_result_and_pick_execution_bridge.py',
           'tools/build_2021_full_draft_comparison.py']
REVIEWED_INPUT_SHA256 = {'simulation/NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json': '3e35fd2abfeb32e2bc5b66b7796f843ca117359be1a419d037844d29177a26d8', 'simulation/NBA_2021_FULL_DRAFT_COMPARISON.json': '31e524c981a07240c835150e7db1d753191c92e205a03bc5207208aca07dbb8f', 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json': '253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088', 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json': '9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce', 'simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE_INPUTS.json': '4b66d96a274fa4d31e41f6256192449e8b43a6dfc00e8f4e44f4cbd76e83bf78', 'simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json': '7d3ab9d0d9e4234e728d4549616acaf84d5b57c4110603cf0114c8bf2c55b8d4', 'simulation/CHICAGO_2021_23_CONTINUATION.json': '3156582b1753953bd9f79c96231a476c0483671d0f1335048b276cc1536d9cca', 'simulation/CHICAGO_2021_M1_ROLE_WITNESS.json': '26b73b6ba0a87449f60774fa3a631374679e0fd5bc6547e5bbecf013232ddf0c', 'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2', 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json': '4ee9b74e37903a43b0bd50b35c7f24cbabdac13728097a848b553f874bbeef80', 'research/CHICAGO_2021_23_CONTRACT_SEQUENCE_SOURCES.json': '39e6abad44a3f23184ca40d7bad81c8897b9c5ed01797bf623b2c4b414527cc8', 'research/CHICAGO_2021_23_CONTINUATION_SOURCES.json': '4dc3cfb7416174c0fea5c2710e9915a729d362dc553f216f4e9c861b373e9db3', 'research/O15G15BF_GREEN_2021_RFA_ORDER_AND_QO_CHARGE.md': '4c237ce9dea2a644a435404013c3264d2c877fa53e25c9d8f9749d3bc7a82cb4', 'research/O15G15AY_CHICAGO_2021_TWO_WAY_SLOT_SCREEN.md': '8362115d2a18b27cabaf725728903b010b6a05535768d9e43c1653e0f5a7d020', 'research/O15G15AZ_SIMONOVIC_2021_ACTIVATION_SLOT_GATE.md': '32fe3fe14a559e115129444a3912a88bb0179ba3deb1fc68ac9ec11b292324ea', 'tools/build_2020_21_result_and_pick_execution_bridge.py': '9b4a9d4de430c6f16480d1704c9397131a4fbba84b1405cfa049eba337670256', 'tools/build_2021_full_draft_comparison.py': '86066ec12904a34abfceea2c449707ecb2b0ee8b0dc02d89b6a47527641d54e3'}


def text(p):
    return (ROOT / p).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def sha(p): return hashlib.sha256(text(p).encode()).hexdigest()
def load(p): return json.loads(text(p))


def sources(reader=load, hasher=sha):
    assert set(REVIEWED_INPUT_SHA256) == set(SOURCES), 'Source coverage'
    for p in SOURCES:
        assert hasher(p) == REVIEWED_INPUT_SHA256[p], 'Unreviewed source change: ' + p
    return {p: reader(p) for p in SOURCES if p.endswith('.json')}


def draft_join(s):
    control = s[A3]['pick_control_snapshot']['rows']
    assert [x['pick'] for x in control] == list(range(1, 61))
    g = s[G7]
    assert g['recommended_comparison'] == 'DB1' and g['recommended_CHI39_option'] == 'C39A'
    db = next(x for x in g['scenarios'] if x['id'] == 'DB1')
    c39 = next(x for x in g['CHI39_options'] if x['id'] == 'C39A')
    assert db['board'] == c39['board'], 'DB1/C39A identities differ'
    board = db['board']
    assert [x['pick'] for x in board] == list(range(1, 61))
    assert len({x['proposed_player'] for x in board}) == 60, 'Duplicate draft player'
    assert (board[9]['team'], board[9]['proposed_player']) == ('CHI', 'Chris Duarte')
    assert (board[38]['team'], board[38]['proposed_player']) == ('CHI', 'Joe Wieskamp')
    rows, mismatches = [], []
    for b, c in zip(board, control):
        assert b['pick'] == c['pick']
        matching = b['team'] == c['control_holder']
        if not matching:
            mismatches.append({'pick': b['pick'], 'current_control_holder': c['control_holder'],
                               'candidate_holder': b['team'], 'player': b['proposed_player']})
        chi = b['pick'] in (10, 39)
        if chi:
            assert matching and c['origin'] == 'CHI', 'Chicago owned draft right missing'
        rows.append({'pick': b['pick'], 'round': c['round'], 'origin': c['origin'],
                     'frozen_control_holder': c['control_holder'], 'candidate_team': b['team'],
                     'player': b['proposed_player'], 'same_current_holder': matching,
                     'classification': 'AUTHOR_MODELED_ROUTINE_CHICAGO_WORKING_SELECTION' if chi else 'EXISTING_G7_CANDIDATE_NOT_SELECTED',
                     'working_selection': chi, 'new_draft_author_lock': False,
                     'actual_draft_or_registration_certified': False})
    assert mismatches == [{'pick': 16, 'current_control_holder': 'BOS',
                           'candidate_holder': 'HOU', 'player': 'Alperen Sengun'}], 'Unexpected owner gap'
    return rows, mismatches, db


def contract_family(s, db):
    m, a, p = s[M1], s[A], s[SEQ]
    assert m['selected']['route'] == 'M1' and a['selected']['route'] == 'G1A_PLUS_M1'
    mark = m['selected']['proposed_salary_by_season_usd']
    assert mark == {'2021-22': 17000000, '2022-23': 18360000, '2023-24': 19720000, '2024-25': 21080000}
    assert m['selected']['proposed_total_usd'] == sum(mark.values()) == 76160000
    assert all(y-x == mark['2021-22']*8//100 for x,y in zip(mark.values(), list(mark.values())[1:]))
    assert p['recommended_route'] == 'SQ1' and p['cap2021'] == 112414000
    assert p['apron2021'] == 143002000 and p['ntmle2021'] == 9536000
    proposed = copy.deepcopy(db['named_roster_without_protagonist'])
    assert len(proposed) == 14 and proposed['Markkanen'] == 15690909
    proposed['Markkanen'] = mark['2021-22']
    pro = s[BASE]['rookie_fourth_cases']
    assert len(pro) == 30 and len({(x['pick'],x['percent']) for x in pro}) == 30
    assert min(x['salary'] for x in pro) == 2392564 and max(x['salary'] for x in pro) == 4915857
    assert proposed['Caruso'] == 8600000 and proposed['Chris Duarte'] == 4373040
    assert proposed['Joe Wieskamp'] == 925258 and proposed['Green'] == 1669178
    assert proposed['Tony Bradley'] == 1789256 and proposed['Stanley Johnson'] == 2089448
    assert proposed['Denzel Valentine'] == 1939350
    retained = ['LaVine', 'LaMelo_pick4', 'Coby', 'Carter', 'Young', 'Satoransky', 'Protagonist']
    signing = ['Chris Duarte', 'Green', 'Caruso', 'Markkanen', 'Joe Wieskamp',
               'Tony Bradley', 'Stanley Johnson', 'Denzel Valentine']
    assert len(set(retained + signing)) == 15
    roster = []
    for n in retained + signing:
        roster.append({'player': n, 'classification': 'RETAINED_EXISTING_CONTRACT_FAMILY' if n in retained else
                       'ALREADY_AUTHOR_SELECTED_M1' if n == 'Markkanen' else 'AUTHOR_MODELED_ROUTINE_A_IMPLEMENTATION',
                       'first_year_proposal_or_retained_reference': None if n == 'Protagonist' else proposed[n],
                       'first_year_interval_from_existing_model': [2392564,4915857] if n == 'Protagonist' else None,
                       'new_exact_author_lock': False, 'actual_signed_contract': None,
                       'actual_player_acceptance_or_league_receipt': None})
    tw = [{'player': n, 'type': 'TWO_WAY', 'classification': 'AUTHOR_MODELED_ROUTINE_EXISTING_HISTORICAL_TYPE',
           'working_signing_date': '2021-08-13', 'working_term_seasons': 1,
           'flat_salary_rule_usd': p['rookie_min2021']//2,
           'entering_YOS_eligibility_family': [0,1,2,3], 'exact_actual_YOS_certificate': None,
           'regular_active_game_limit': 50, 'active_games_selected': None,
           'standard_conversion': None, 'actual_acceptance': None} for n in ['Devon Dotson','Tyler Cook']]
    assert p['rookie_min2021'] == 925258 and all(x['flat_salary_rule_usd'] == 462629 for x in tw)
    return proposed, pro, roster, tw


def events_and_cases(s, final, pro):
    p = s[SEQ]
    late = p['late_minimum_order']
    assert late == ['Joe Wieskamp','Tony Bradley','Stanley Johnson','Denzel Valentine']
    # Dates and within-day order are NEW fictional routine implementation,
    # never the original releases' legal-effective dates. After moratorium.
    definitions = [('CAP_YEAR_START', '2021-08-03', None, None),
                   ('SIGN_DUARTE', '2021-08-06', 'Chris Duarte', 'ROOKIE_EXCEPTION'),
                   ('SIGN_GREEN', '2021-08-06', 'Green', 'TWO_YEAR_MINIMUM_EXCEPTION'),
                   ('SIGN_CARUSO', '2021-08-09', 'Caruso', 'NTMLE'),
                   ('SIGN_MARKKANEN', '2021-08-10', 'Markkanen', 'BIRD'),
                   ('RENOUNCE_UNUSED_RIGHTS', '2021-08-11', None, 'RENOUNCE'),
                   *[(f'SIGN_{n.upper().replace(" ","_")}', '2021-08-12', n, 'MINIMUM_EXCEPTION') for n in late]]
    events = []
    for i,(id,day,n,method) in enumerate(definitions):
        if n: assert date.fromisoformat(day) >= date(2021,8,6)
        events.append({'id': id,'date': day,'within_model_order': i,'player': n,'method': method,
                       'date_classification': 'AUTHOR_MODELED_ROUTINE_DATE_NOT_ORIGINAL_ANNOUNCEMENT',
                       'actual_legal_effective_date': None})
    cases = []
    for r in pro:
        for bonus in [0,1000000]:
            contracts = {n:final[n] for n in ['LaVine','LaMelo_pick4','Coby','Carter','Young','Satoransky']}
            contracts['Protagonist'] = r['salary']
            holds = dict(p['retained_FA'])
            assert holds == {'Markkanen':20194524,'Theis':9500000,'Denzel Valentine':8821320}
            unsigned = {'Chris Duarte': final['Chris Duarte']}
            nt = p['ntmle2021']; hard = False; rows = []
            for e in events:
                n = e['player']; method = e['method']
                before_lower = sum(contracts.values()) + sum(holds.values()) + sum(unsigned.values()) + bonus
                if n:
                    assert n not in contracts
                    if method == 'NTMLE':
                        assert nt >= final[n] and before_lower+nt > p['cap2021'], 'NTMLE entry lost'
                        nt -= final[n]; hard = True
                    if method == 'BIRD': assert n in holds
                    contracts[n] = final[n]; holds.pop(n,None); unsigned.pop(n,None)
                if method == 'RENOUNCE':
                    holds.clear()
                    # Expressly relinquish UNUSED remainder. No inference of
                    # automatic extinguishment from a partial salary below cap.
                    nt = 0
                incomplete = max(0,12-len(contracts)-len(holds)-len(unsigned))
                known_normal = sum(contracts.values()) + sum(holds.values()) + sum(unsigned.values()) + bonus + incomplete*p['rookie_min2021']
                known_apron = sum(contracts.values()) + bonus + (p['Markkanen_apron_QO_upper_reference'] if 'Markkanen' in holds else 0)
                rows.append({'event_id':e['id'],'date':e['date'],'standard_contracts':len(contracts),
                             'contract_players':sorted(contracts),'retained_named_FA':copy.deepcopy(holds),
                             'unsigned_first_reference':copy.deepcopy(unsigned),
                             'known_normal_terms_including_incomplete':known_normal,
                             'incomplete_roster_count_in_named_submodel':incomplete,
                             'incomplete_roster_usd':incomplete*p['rookie_min2021'],
                             'known_apron_reference_terms':known_apron,
                             'normal_complete_salary':None,'apron_complete_salary_upper':None,
                             'unused_NTMLE_nominal':nt,'hard_cap_triggered_in_working_family':hard,
                             'conditional_extra_apron_allowance':p['apron2021']-known_apron if hard else None,
                             'whole_cost_pass':False})
            assert len(contracts) == 15 and not holds and not unsigned and hard and nt == 0
            assert set(contracts) == set(final) | {'Protagonist'}
            cases.append({'protagonist_existing_model':r,'Young_existing_bonus_reference':bonus,'states':rows,
                          'final_named_annual_budget':sum(contracts.values())+bonus})
    assert len(cases) == 60
    return events, cases


def build(reader=load, hasher=sha):
    s = sources(reader,hasher)
    board,gaps,db = draft_join(s)
    final,pro,roster,tw = contract_family(s,db)
    events,cases = events_and_cases(s,final,pro)
    budget = [x['final_named_annual_budget'] for x in cases]
    assert max(budget) == 108171174 and min(budget) == 104647881
    role = s[ROLE]
    assert role['position_minutes']['PF']['Markkanen'] == 32 and role['derived_player_minutes']['Caruso'] == 18
    assert role['elapsed_minutes'] == 48 and role['team_minutes'] == 240
    assert all(sum(x.values())==48 for x in role['position_minutes'].values())
    assert set(role['derived_player_minutes']) <= {x['player'] for x in roster}
    return {'status':'INDEPENDENTLY_REVIEWED_WORKING_CHICAGO_DRAFT_AND_SQ1_SEQUENCE_COMPLETE_COST_HOLD',
            'source_sha256':{p:hasher(p) for p in SOURCES+[SELF]},
            'hash_convention':'UTF8_BOM_STRIPPED_CRLF_CR_NORMALIZED_LF',
            'authority':{'already_selected':['M1_FOUR_YEAR_GUARANTEED_CHICAGO_76160000','G1A_CARUSO_GROWTH_CORE_DIRECTION'],
                         'routine_working_implementation':['CHI10_DUARTE','CHI39_WIESKAMP_STANDARD_TWO_YEAR_MINIMUM','SQ1_NAMED_ORDER_AND_DATES','DOTSON_COOK_TWO_WAY_TYPE_FAMILY'],
                         'other_58_draftees_selected':False,'new_draft_author_lock':False,
                         'actual_private_contracts_receipts_medical_or_acceptance_certified':False},
            'public_rule_observations':[
                {'url':'https://www.nba.com/news/nba-announces-start-date-for-2021-free-agency','date':'2021-04-19',
                 'method':'DIRECT_WEB_BODY_READ_2026_10_07','locator':'body negotiation/moratorium paragraph',
                 'fact':'Negotiation August2 18:00 ET; ordinary FA signing August6 12:01 ET.'},
                {'url':'https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season','date':'2021-08-02',
                 'method':'DIRECT_WEB_BODY_READ_2026_10_07','locator':'official-release salary-cap/exception paragraphs',
                 'fact':'Cap112414000; tax136606000; NTMLE9536000; cap-year startsAugust3.'},
                {'url':'https://pr.nba.com/nba-board-of-governors-play-in-roster-rules-2021-22-season/','date':'2021-07-27',
                 'method':'DIRECT_WEB_BODY_READ_2026_10_07','locator':'Roster-Related Rules paragraphs',
                 'fact':'STD15/TW2; game active15; TW regularactive50; TWsalary50percentrookieminimum; noJanuary15deadline.'},
                {'url':'https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf',
                 'raw_sha256':'66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a',
                 'method':'DIRECT_CACHED_PRIMARY_PDF_TEXT_READ_2026_10_07',
                 'locator':'VII5(c)PDF218;VII6(b)223;VII6(e)228-229;VII6(i)232-233;VII6(m)239-241;VII7(d)(3)248',
                 'scope':'Bird8percent;NTMLE4years+Salary/Unlikelyaggregate;minimummax2years/noanybonus;annualapronA-G;unusedexceptionrenounce;oldcontract6monthrestriction.'}],
            'draft_date_model':'2021-07-29','draft_rows':board,'owner_mismatches':gaps,
            'unexecuted_optional_asset_chain':{'pick':16,'chain':['BOS_TO_OKC_AP1_KEMBA','OKC_TO_HOU_SG16'],
                                               'all_60_world_draft_complete':False,'new_actual_trade_selected':False},
            'standard_roster_working':roster,'two_way_working':tw,
            'Simonovic':{'rights_retained_working':True,'standard_contract_added':False,
                         'reason':'15 chosen standard slots; original2021NBAactivationnotcopied',
                         'overseasrights_tenderbridge_not_yet_proved':True},
            'working_events':events,'named_cost_family_cases':cases,
            'cost_boundary':{'named_budget_range': [min(budget),max(budget)],
                             'conditional_final_extra_apron_allowance_min':143002000-max(budget),
                             'complete_normal_salary':None,'complete_apron_upper':None,'complete_tax_salary':None,
                             'unknown_cost_selected_zero':False,'whole_cost_pass':False,
                             'uncovered_finite_categories':['preservedcontract_currentSalary/allperformance/assignmentcarry2021mapping',
                                 'newproposal_signing/performancebonuses_and_NTMLEaggregate','legacy_dead_salary_or_resolved_grievancecarry',
                                 'other_named_FA/unsigned_draftrights_charge_before_renounce','requiredtenders_and_Green/MarkQO_firstrefusalstates',
                                 'DPE/TPE/BAE_history_normalcharge_and_explicitunusedrightsclosure'],
                             'NTMLE_remainder_policy':'936000 afterCaruso; expresslyrenouncedAugust11;hardcapremains',
                             'cash_cap_tax_apron_equated':False,
                             'Caruso_firstyear_Salary_plus_Unlikely_must_not_exceed':9536000,
                             'no_minimum_contract_bonus_allowed':True},
            'normal_day_role_reference':{'source':ROLE,'position_minutes':role['position_minutes'],
                                          'player_minutes':role['derived_player_minutes'],'team_minutes':240,
                                          'actual_dated_minutes_or_health_certified':False},
            'finite_remaining':[
                {'id':'FULL60_OWNER_EXECUTION','scope':'#16BOS→OKC→HOUoptionalchain;other58G7recommendationsnotselected'},
                {'id':'WHOLE2021_NORMAL_APRON_COST','scope':'named108m is partial; map finite categories and every signing state toclosedinterval'},
                {'id':'SIMONOVIC_RIGHTS_WINDOW','scope':'2020#44rights retained;overseas/tender2021finitebridge before claiming validstash'},
                {'id':'2022_23_CONTINUATION','scope':'CX1/RT1/P/LaVine/Young and lateroptions/cost/seasonmodelsstillconditional'}],
            'summary':{'draft_candidate_rows':60,'draft_working_selections':2,'matching_control_rows':59,
                       'optional_chain_gaps':1,'working_signing_state_count':10,'standard_slots':15,'two_way_slots':2,
                       'named_cost_cases':60,'whole_cost_pass_count':0},
            'six_month_descendant_boundary':{'source':'VII7(d)(3)/acceptedCHI_F1family',
                                            'old_contract_extension_renegotiation_floor':'max(2021-09-25,otherwiseeligible)',
                                            'new_expired_contract_FA_not_automatically_old_extension':True,
                                            'no_new_private_waiver_selection':True},
            'macro3_complete':False,'exact_execution_cleared':False,'new_REGISTER_promotion':False,
            'independent_review_completed':True,'season_selected':False,'design_gate':'CLOSED','manuscript_allowed':False}


def validate(d, reader=load, hasher=sha):
    try: expected=build(reader,hasher)
    except (AssertionError,KeyError,ValueError) as e: return ['Source construction: '+str(e)]
    return [] if d==expected else ['Artifact differs from source-bound working construction']


def markdown(d):
    lines=['# Chicago 2021 승인 A — 드래프트·SQ1 작업 실행', '',
           '**국소 작업 모델 / 독립 검문 수용 / 전체 비용 HOLD.** M1·A 재승인 없이 기존 방향의 일상 구현을 선택했다. 새 작가 지명 잠금·실제 서명/접수 인증·3번 종료는 아니다.', '',
           '## 선택 권위와 픽 연결', '',
           '작가확정: M1 Chicago 4년 완전보장 76.16m·A 성장 코어. 새 작업 선택: CHI10 Duarte/CHI39 Wieskamp, SQ1 날짜·순서와 Dotson/Cook TW 계약 유형 가족. 다른58인은 기존 G7 후보 그대로다.', '',
           'A3 원소유/control60과 G7 DB1/C39A는 59행 소유가 일치한다. #16은 현재 BOS, 후보 HOU여서 BOS→OKC AP1와 OKC→HOU SG16의 두 거래 실행이 남는다. Chicago 두 픽 소유와 앞선 후보 선수의 중복 없음은 검문하지만 전체60의 실제 지명을 완료했다고 하지 않는다.', '',
           '## 새 날짜별 작업 순서', '', '| 작업 사건 | 가상 날짜 | 방법 |','|---|---|---|']
    lines += [f"| {e['id']} | {e['date']} | {e['method'] or '신규 cap year'} |" for e in d['working_events']]
    lines += ['', '8/6의 두 사건 및 8/12의 네 사건은 표 순서의 가상 내부 순서다. 실제 발표일/정확 접수시각으로 인증하지 않는다. Green 2년 최소 예외는 새 FA 계약이며, 이전 계약의 보너스 면제 뒤 연장·재협상 제한을 새 계약에 무조건 적용하지 않는다.', '',
              '최종 일반계약15: '+', '.join(x['player'] for x in d['standard_roster_working'])+'.',
              'TW2: Devon Dotson/Tyler Cook의 1년 유형 가족; 실제 선수연수 서류나 활성50경기를 인증하지 않는다. Simonović는 일반계약으로 추가하지 않았다. 지명권 보유 가설의 해외계약/tender 연속성은 남은 유한 경계다.', '',
              '## 장부 경계', '',
              f"기존 P 급여30조건×Young0/1m 비교60조건의 알려진 연간 예산은 ${d['cost_boundary']['named_budget_range'][0]:,}–${d['cost_boundary']['named_budget_range'][1]:,}. 마지막 apron의 조건부 추가비용 여유 최소는 ${d['cost_boundary']['conditional_final_extra_apron_allowance_min']:,}. **전체 상단은 null이며 전체 비용 PASS0**이다.", '',
              'normal에는 유지 FA와 미서명1R·12명 미달 차지를 표시하고 apron에는 별도 RFA QO 참고상단을 넣는다. 일반계약/FA/지명권을 명단 한 자리로 혼용하지 않는다. 표시된 금액은 기존 후보 비교값이며 Green/기타 권리·현재Salary/보너스·과거 잔액/중재·예외의 전체 상단이 아니다.', '',
              'Caruso 뒤 NTMLE 명목잔액936000은 8/11 **명시 포기**한다. 부분합이 cap 아래라는 이유만으로 자동 소멸을 단정하지 않는다. 이미 발생한 해당연도 hardcap은 유지한다. Caruso Salary+Unlikely 합계9536000 한도·최소 예외 계약의 보너스 금지·전체apron은 후속 상단 검문에 포함한다.', '',
              'M1 정상일 모델 Markkanen32/Caruso18, 팀240분을 연결했다. 경기별 실제 분·건강·전술 성공은 별도다.', '',
              '## 직접 읽은 공개 규칙', '']
    lines += [f"- [{x['date'] if 'date'in x else '2017 CBA'}]({x['url']}): {x.get('fact',x.get('scope'))} 원문 위치: {x['locator']}." for x in d['public_rule_observations']]
    lines += ['', '서명/급여는 사실·후보·가상 실행·작가확정을 구분한다. 지문은 BOM 제거와 LF 정규화이며 새 SHA만 바꾼 의미변조도 고정 입력핀에서 거부한다. 기존2번은 다시 열지 않는다.', '',
              '## 전체 7행', '', '| 번호 | 작업 | 상태 |','|---|---|---|',
              '| 1 | 2020 드래프트 연쇄 | 완료 |','| 2 | Chicago 2020–21 | S2 완료 |',
              '| 3 | 2021–23 거래·계약 | 이 국소 작업 실행; 전체비용/후속 미완료 |',
              '| 4 | 장기 커리어 | 선행 시즌 이후 계속 |','| 5 | 결말·전체 구조 | 골격/기능표 진행 |',
              '| 6 | 집필 규격·Context Pack | 국소 기능19; 전체 기능/Pack 미완료 |',
              '| 7 | 통합·독립·작가 승인 | 미완료 |', '',
              '**미완료 큰 묶음5개.** v0.30 PARTIAL·설계/원고 CLOSED·실제Pack0·원고0. 이 파일은 REGISTER/중앙 문서를 변경하지 않는다.', '']
    return '\n'.join(lines)


def self_test(d):
    mutations=[('missing hold',lambda x:x['named_cost_family_cases'][0]['states'][0]['retained_named_FA'].pop('Theis')),
               ('whole partial cost promoted',lambda x:x['cost_boundary'].update(whole_cost_pass=True,complete_apron_upper=108171174)),
               ('wrong16holder',lambda x:x['draft_rows'][15].update(frozen_control_holder='OKC')),
               ('duplicate draftee',lambda x:x['draft_rows'][38].update(player='Chris Duarte')),
               ('before moratorium signing',lambda x:x['working_events'][3].update(date='2021-08-02')),
               ('three TW',lambda x:x['two_way_working'].append(copy.deepcopy(x['two_way_working'][0]))),
               ('wrong old M0 retained',lambda x:x['standard_roster_working'][10].update(first_year_proposal_or_retained_reference=15690909)),
               ('financial lock',lambda x:x['authority'].update(new_draft_author_lock=True))]
    for label,mutate in mutations:
        x=copy.deepcopy(d); mutate(x); assert validate(x), label
    bad=copy.deepcopy(load(G7)); bad['scenarios'][0]['board'][9]['proposed_player']='Moses Moody'
    reader=lambda p:bad if p==G7 else load(p)
    hasher=lambda p:hashlib.sha256(json.dumps(bad).encode()).hexdigest() if p==G7 else sha(p)
    assert validate(d,reader,hasher),'Fresh-SHA sameID upstream meaning'
    return len(mutations)+1


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    d=build()
    if a.write:
        (ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
        (ROOT/MD).write_text(markdown(d),encoding='utf-8',newline='\n')
    errors=validate(load(OUT)) if a.check else validate(d)
    if a.check and text(MD)!=markdown(d): errors.append('Markdown stale')
    controls=self_test(d) if a.self_test else None
    print(json.dumps({'current':not errors,'summary':d['summary'],'negative_controls':controls,'errors':errors},ensure_ascii=False))
    raise SystemExit(bool(errors))
