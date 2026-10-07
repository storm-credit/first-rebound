"""Source-bound A10 GAME1: selected two role windows, not a full game/result."""
from __future__ import annotations
import argparse,copy,hashlib,json
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_a10_game1_selected_role_window.py'
OUT='simulation/A10_GAME1_SELECTED_ROLE_WINDOW.json'
PACK='research/A10_2024_25_GAME1_NAMED_INPUTS_2026_10_08.json'
SELECT='canon/DELEGATED_A10_GAME1_ROLE_WINDOW_SELECTION_2026_10_08.json'
PEER='reviews/A10_GAME1_NAMED_INPUTS_CHI_INDEPENDENT_REVIEW_2026_10_08.json'
ROLE='canon/DELEGATED_A10_2024_25_NAMED_ROLE_PLAN_SELECTION_2026_10_08.json'
CHI='simulation/CHICAGO_2024_A10_SELECTED_RENEWAL_EXECUTION.json'
PINS={PACK:'3934ed7610e478ea087234d87165d26bf824810862cf4f10a15bffc7c7fadfae',
SELECT:'3ae631359abb2358e22fe6242310fc038593b28e668cde432a0988e5b35923e2',
PEER:'5722d2011549e61020549e89ca6c29b4f67aa97bd10a57793c1b5bc5aa443cc9',
ROLE:'723bcfddae88fb4ed5e265db15a4f53542229c677a634370603f637604ddabda',
CHI:'ef48f0a1931037ec58ec59e53fde30baedddf8d96f13e2bc86120da2a7572cf5'}

def norm(t):return t.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(norm((ROOT/p).read_text(encoding='utf-8-sig')).encode()).hexdigest()
def serial(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def physical():
    for p,h in PINS.items():assert sha(p)==h,'A10 GAME1 input changed: '+p
    return {p:json.loads((ROOT/p).read_text(encoding='utf-8-sig')) for p in PINS}
def source_inputs():return physical()
def assert_inputs(s):
    assert s==physical(),'Returned source differs from independent physical input'
    q=s[PACK];z=s[SELECT]
    for p,h in q['source_sha256'].items():assert sha(p)==h,'Prepared dependency changed: '+p
    for p,h in z['source_sha256'].items():assert sha(p)==h,'Selected dependency changed: '+p
    assert z['source_packet_sha256']==PINS[PACK] and s[PEER]['source_sha256'][PACK]==PINS[PACK]
    assert s[PEER]['status']=='INDEPENDENTLY_ACCEPTED_SINGLE_DATE_SOURCE_BOUND_CONDITIONAL_NPC_FAMILY_PREPARATION_ONLY'
    assert (z['game_id'],z['game_date'],z['away'],z['home'])==('0022400069','2024-10-23','CHI','NOP')
    assert z['selected_CHI_role']==s[ROLE]['selected_plan']=='B_DEVELOPMENT_JAQUEZ20_RECOMMENDED'
    assert z['selected_NOP_plan']=='N24A_CONTINUITY_COUNTER_RECOMMENDED'
    assert z['named_UPC_function_conditions_and_option_notices_selected'] and z['nomination_and_bounded_role_observation_selected']
    assert z['original_XXIX1_bench_condition_preserved'] and z['weakside_Duarte_Jaquez_conditions_preserved']
    assert not z['admitted_fictional_contract_domain']['actual_signed_prices_receipts_or_all_branch_factual_certification']
    assert not z['first_option_success_efficiency_or_winning_basket_selected'] and not z['QUAL1_or_A10_S3_complete']
    assert not z['whole_A10_G13_G14_complete'] and z['whole_game_result'] is None and not z['new_human_author_lock']
    for r in q['NOP_FY24_contract_function']['two_carry_claims']+q['NOP_FY24_contract_function']['ten_same_owner_status_functions']:
        p,ptr=r['source_pointer'].split('#');v=json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
        for key in ptr.lstrip('/').split('/'):v=v[int(key)] if isinstance(v,list) else v[key]
        assert v['player']==r['player'] and v.get('candidate_owner',v.get('team'))=='NOP','Contract locator actor/owner differs'
        if 'source_row_id' in r:assert v['id']==r['source_row_id']
    for r in q['NOP_FY24_contract_function']['three_option_proposals']:
        assert r['window_start']<=r['proposal_team_signed_notice']<=r['window_deadline']
    kh=next(r for r in q['NOP_FY24_contract_function']['ten_same_owner_status_functions'] if r['player']=='Killian Hayes')['original_RSC_Year4_if_chosen_requires_notice']
    assert kh['window'][0]<=kh['proposal_team_signed_notice']<=kh['window'][1]
    assert q['NOP_FY24_contract_function']['existing_full_Gamma_and_nonassignment_waiver_cost_preserved']
    # External bytes used here are source identity checks; no repeated upstream producer/DAG traversal.
    pdf=q['primary']['official_schedule'];assert hashlib.sha256(Path(pdf['cache_path']).read_bytes()).hexdigest()==pdf['raw_sha256']
    assert 'Wed. Oct. 23' in Path(pdf['text_path']).read_text(encoding='utf-8')

def construct(s):
    q=s[PACK];z=s[SELECT];role=s[ROLE]
    alt=next(a for a in q['NOP_two_alternatives'] if a['id']==z['selected_NOP_plan'])
    rosters={};chi_names=s[CHI]['execution']['post_signature_named_STD']
    for t,names,addition in [('CHI',chi_names,'Javonte Green'),('NOP',alt['standard'],'Moses Moody')]:
        active=z['selected_'+t+'_active'];inactive=z['selected_'+t+'_inactive']
        rosters[t]={'standard':copy.deepcopy(names),'TW':[],'prepared_active12':copy.deepcopy(q['selected_CHI_parent']['active_candidate'] if t=='CHI' else alt['active']),
          'selected_active13':copy.deepcopy(active),'selected_inactive2':copy.deepcopy(inactive),'selected_available13':copy.deepcopy(z['selected_'+t+'_available']),
          'dated_zero_minute_addition':addition,'dressed':13,'court_players':5,'off_court_dressed':8,
          'original_XXIX1_bench_condition_retained':True,'actual_clinical_or_dressed_certificate':False}
    games=[]
    for p in z['selected_possessions']:
        games.append({'id':p['id'],'game_id':z['game_id'],'date':z['game_date'],'quarter':4,'start_second':p['start_second'],'end_second':p['end_second'],
          'CHI_positions':copy.deepcopy(role['selected_ordered_role_capacity'][-1]['positions']),'NOP_positions':copy.deepcopy(alt['counter_positions']),
          'team_player_seconds':{'CHI':40,'NOP':40},'unique_simultaneous_actors':10,'P_onball_seconds':p['P_seconds'],'LaVine_remaining_seconds':p['LaVine_seconds'],
          'selected_observable':p['observable'],'independent_actor_response_selected_as_fiction':p['independent_actor_response_selected_as_fiction'],'shot_or_score':None,
          'direct_creation_and_preparation_objective_met':False if p['P_seconds']==6 else None,
          'earlier_shared_handoff_completed':p['P_seconds']==3,'first_option_scoring_success_certified':False})
    return {'game':copy.deepcopy(q['game']),'selected_NOP_plan':alt['id'],'selected_CHI_role':role['selected_plan'],'dated_registration':rosters,
      'CHI_reference_regulation_capacity':copy.deepcopy(role['selected_ordered_role_capacity']),'CHI_reference_player_minutes':copy.deepcopy(role['selected_player_regulation_minutes']),
      'CHI_contract_cost_and_Gamma':{k:copy.deepcopy(s[CHI]['execution'][k]) for k in ['live10','selected_new_contracts5','cost_family']},
      'lawful_NPC_function_selected':copy.deepcopy(q['NOP_FY24_contract_function']),
      'selected_admitted_contract_domain':copy.deepcopy(z['admitted_fictional_contract_domain']),
      'contract_execution_scope':{'admitted_piecewise_function_and_valid_notices_selected':True,'conditional_if_original_term_and_service_predicates':True,
        'all_original_Gamma_and_prior_claims_preserved':True,'original_private_status_or_endpoints_resolved_as_fact':False,'actual_signed_prices_receipts':None,
        'new_Bird_or_minimum_is_not_double_UPC_or_automatic_expiry':True,'source_reported_salary_is_not_exact_private_cents':True,'floor_is_conditional_function_not_entire_cash_upper':True},
      'cost_conditions':copy.deepcopy(q['cost_conditions']),
      'selected_windows':games,'gap':{'start_second':2856,'end_second':2872,'seconds':16,'event':None,'possession_control':None,'shot_score':None,'unobserved_gap_invented':False},
      'onball_counterfactuals':copy.deepcopy(q['S1_S2_consumption']['onball_counterfactuals']),
      'selected_actual_cost_comparison':'CF_LV8_TO_P3_LV5','alternate_Melo_comparison_is_distinct_baseline_not_extra_cost':True,'costs_additive':False,
      'Duarte_Jaquez_weakside_conditions':copy.deepcopy(q['S1_S2_consumption']['weakside_read_boundary']),
      'execution':{'two_selected_shared_role_windows_executed_in_admitted_fiction':True,'failure_then_earlier_handoff_with_independent_receiver':True,
        'active13_and_five_plus_eight_capacity_checked':True,'paired_eight_seconds_each_side40_checked':True,'original_fullgame_CHI_clock_changed':False,
        'entire_NOP_48_240_clock_or_GAME1_result_executed':False,'both_team_fullgame_scores':None,'winner':None,'historical_observation':False},
      'remaining_ports':['QUAL1 separate qualification/series window; S3 not closed','No full GAME1 score/efficiency/winner or2024-25 season selected by these two windows','Any source-identified new contract/option/assignment changes reopen only its named service/cost predicate']}

def assert_payload(p,s):
    q=s[PACK];z=s[SELECT];role=s[ROLE];alt=next(a for a in q['NOP_two_alternatives'] if a['id']=='N24A_CONTINUITY_COUNTER_RECOMMENDED')
    assert p['game']==q['game'] and p['selected_NOP_plan']==alt['id'] and p['selected_CHI_role']==role['selected_plan']
    assert p['lawful_NPC_function_selected']==q['NOP_FY24_contract_function'],'Returned original contract/option/Gamma family altered'
    assert p['CHI_contract_cost_and_Gamma']=={k:s[CHI]['execution'][k] for k in ['live10','selected_new_contracts5','cost_family']},'Returned Chicago selected cost/Gamma family altered'
    assert p['selected_admitted_contract_domain']==z['admitted_fictional_contract_domain']
    assert p['cost_conditions']==q['cost_conditions'],'Returned price/unknown/FAhold/conditionalfloor differs'
    scope=p['contract_execution_scope']
    assert scope=={'admitted_piecewise_function_and_valid_notices_selected':True,'conditional_if_original_term_and_service_predicates':True,
        'all_original_Gamma_and_prior_claims_preserved':True,'original_private_status_or_endpoints_resolved_as_fact':False,'actual_signed_prices_receipts':None,
        'new_Bird_or_minimum_is_not_double_UPC_or_automatic_expiry':True,'source_reported_salary_is_not_exact_private_cents':True,'floor_is_conditional_function_not_entire_cash_upper':True}
    blocks=p['CHI_reference_regulation_capacity'];assert blocks==role['selected_ordered_role_capacity'],'Returned reference role chronology differs'
    assert p['CHI_reference_player_minutes']==role['selected_player_regulation_minutes']
    totals={};positions={k:0 for k in ['PG','SG','SF','PF','C']}
    for b in blocks:
        dur=b['end_second']-b['start_second'];assert len(set(b['positions'].values()))==5
        for k,a in b['positions'].items():positions[k]+=dur;totals[a]=totals.get(a,0)+dur
    assert set(positions.values())=={2880} and sum(totals.values())==14400
    assert {k:v//60 for k,v in totals.items()}==role['selected_player_regulation_minutes']
    for t,names,add in [('CHI',s[CHI]['execution']['post_signature_named_STD'],'Javonte Green'),('NOP',alt['standard'],'Moses Moody')]:
        d=p['dated_registration'][t];assert d['standard']==names and d['TW']==[] and len(set(names))==15
        assert d['selected_active13']==z['selected_'+t+'_active'] and d['selected_inactive2']==z['selected_'+t+'_inactive']
        assert d['selected_available13']==z['selected_'+t+'_available']==d['selected_active13']
        assert len(set(d['selected_active13']))==13 and len(d['selected_inactive2'])==2
        assert set(d['selected_active13']).isdisjoint(d['selected_inactive2']) and set(d['selected_active13'])|set(d['selected_inactive2'])==set(names)
        assert (d['dressed'],d['court_players'],d['off_court_dressed'])==(13,5,8)
        assert d['original_XXIX1_bench_condition_retained'] and not d['actual_clinical_or_dressed_certificate']
        assert d['dated_zero_minute_addition']==add and add in d['selected_active13']
        assert d['prepared_active12']==(q['selected_CHI_parent']['active_candidate'] if t=='CHI' else alt['active']) and len(d['prepared_active12'])==12
    assert not set(p['dated_registration']['CHI']['standard'])&set(p['dated_registration']['NOP']['standard'])
    assert len(p['selected_windows'])==len(z['selected_possessions'])==2
    for i,(r,a) in enumerate(zip(p['selected_windows'],z['selected_possessions'])):
        assert (r['id'],r['game_id'],r['date'],r['quarter'])==(a['id'],'0022400069','2024-10-23',4)
        assert (r['start_second'],r['end_second'])==[(2848,2856),(2872,2880)][i]
        assert r['CHI_positions']==role['selected_ordered_role_capacity'][-1]['positions'] and r['NOP_positions']==alt['counter_positions'],'Returned source role positions altered'
        assert len(set(r['CHI_positions'].values())|set(r['NOP_positions'].values()))==10
        for t in ['CHI','NOP']:assert set(r[t+'_positions'].values())<=set(p['dated_registration'][t]['selected_available13'])
        assert r['team_player_seconds']=={'CHI':40,'NOP':40} and r['unique_simultaneous_actors']==10
        assert (r['P_onball_seconds'],r['LaVine_remaining_seconds'])==[(6,2),(3,5)][i]
        assert r['selected_observable']==a['observable'] and r['independent_actor_response_selected_as_fiction'] is True
        assert r['shot_or_score'] is None and r['first_option_scoring_success_certified'] is False
        assert r['direct_creation_and_preparation_objective_met'] is (False if i==0 else None)
        assert r['earlier_shared_handoff_completed'] is (i==1)
        assert any(b['start_second']<=r['start_second']<r['end_second']<=b['end_second'] and b['positions']==r['CHI_positions'] for b in blocks)
        for t in ['CHI','NOP']:
            assert len(set(p['dated_registration'][t]['selected_available13'])-set(r[t+'_positions'].values()))==8
    assert p['gap']=={'start_second':2856,'end_second':2872,'seconds':16,'event':None,'possession_control':None,'shot_score':None,'unobserved_gap_invented':False}
    assert p['onball_counterfactuals']==q['S1_S2_consumption']['onball_counterfactuals'] and p['selected_actual_cost_comparison']=='CF_LV8_TO_P3_LV5'
    assert p['alternate_Melo_comparison_is_distinct_baseline_not_extra_cost'] and not p['costs_additive']
    for c in p['onball_counterfactuals']:
        assert sum(c['reference_seconds'].values())==sum(c['comparison_seconds'].values())==8
        assert {a:c['comparison_seconds'][a]-c['reference_seconds'][a] for a in c['reference_seconds']}==c['delta_seconds']
    assert p['Duarte_Jaquez_weakside_conditions']==q['S1_S2_consumption']['weakside_read_boundary']
    assert p['execution']=={'two_selected_shared_role_windows_executed_in_admitted_fiction':True,'failure_then_earlier_handoff_with_independent_receiver':True,
        'active13_and_five_plus_eight_capacity_checked':True,'paired_eight_seconds_each_side40_checked':True,'original_fullgame_CHI_clock_changed':False,
        'entire_NOP_48_240_clock_or_GAME1_result_executed':False,'both_team_fullgame_scores':None,'winner':None,'historical_observation':False}
    assert all(not p['certification'][k] for k in ['actual_private_contract_or_original_status_certificate','clinical_or_real_dressed_certificate','NBA_score_win_or_first_option_efficiency','whole_S1_S2_NBA_season_or_S3_qualification','whole_A10_or_macro4_complete','new_franchise_title_MVP_military_or_author_lock','manuscript_allowed'])
    assert p['certification']['selected_two_window_execution_in_admitted_lawful_fiction'] is True

def build():
    s=source_inputs();assert_inputs(s);p=construct(s)
    assert_inputs(s)  # A returned constructor must not contaminate the consumed source by alias.
    p.update(id='A10_GAME1_SELECTED_ROLE_WINDOW',status='SELECTED_TWO_SHARED_ROLE_WINDOWS_EXECUTED_WITHIN_ADMITTED_CONTRACT_FUNCTION_NOT_FULLGAME_RESULT',
      baseline_main='e0551d71f2b17a77df46b1502294adf5441c555d',source_sha256={**PINS,SELF:sha(SELF)},
      certification={'selected_two_window_execution_in_admitted_lawful_fiction':True,'actual_private_contract_or_original_status_certificate':False,
       'clinical_or_real_dressed_certificate':False,'NBA_score_win_or_first_option_efficiency':False,'whole_S1_S2_NBA_season_or_S3_qualification':False,
       'whole_A10_or_macro4_complete':False,'new_franchise_title_MVP_military_or_author_lock':False,'independent_consumer_review_completed':False,'manuscript_allowed':False},
      project_progress=[{'group':i,'status':'COMPLETE' if i<=3 else 'INCOMPLETE'} for i in range(1,8)],unfinished_major_groups=4,unfinished_through_group6=3,
      freeze='v0.30 PARTIAL',design_gate='CLOSED',Pack_count=0,manuscript_count=0)
    assert_payload(p,physical());return p

def validate(p):
    try:
        s=physical();assert_inputs(s);assert_payload(p,s)
        assert p==build(),'Saved output differs from current selected source-bound reconstruction'
        return []
    except (AssertionError,KeyError,ValueError) as e:return [str(e)]

def markdown(p):
    names=p['dated_registration']
    return '''# A10 GAME1 — 선택된 두 공동 역할 창

2024-10-23 CHI@NOP **0022400069**, root 선택 N24A / Chicago B(Jaquez20). 원 조건부준비 패킷과 새 root선택 canon/CHI독립법적review를 실제물리핀으로 소비했다. source preparation/루틴선택/이 consumer 실행을 구별한다.

## 계약과 등록 범위

같은 NOP15명의 두carry·세2023옵션·열same-owner live/expiry함수와 Killian2022옵션 조건을 **admitted lawful piecewise family**로 선택한다. originalUPC의 사적 끝·가격·Γ가 관측된 사실이라고 확정하지 않는다. 각 branch가 실제 정의한 term/option/expiry/service/max/min/retention 조건을 만족하는 범위에서만 live다. 새 겹침UPC·자동만료·계약가격0·D24/R24null=0·가짜전체market/cash 증명은 없다. 원FA/RT/unusedexception은 유효replacement/renounce 전까지 보존한다. 원Ingrammax가문의 조건부floor도 그대로다.

원 prepared active12는 변경하지 않았다. 선택당일 **양팀15STD0TW/active13·inactive2**이며 CHI Green/NOP Moody를0분 available reserve로 더했다. 각5인창 외 dressed8명이 남아 CBA XXIX1의 bench8 문구를 그대로 구현한다. 12명 후보가 불법이라는 판정이 아니며 available8을 법문으로 바꾸지 않는다. 두 추가선수는 실제원등록/당해조건부계약 명명목록에 있고0분은임상결장이 아니다. Chicago의24×120초 원48/240분 reference는 변하지 않는다. NOP전체48/240게임을 실행했다고 표시하지 않는다.

## 실행한 제한 관측

| 창 | Q4 elapsed clock | 공동역할 관측 | 양팀 선수초 |
|---|---|---|---|
| 첫 실패 |47:28–47:36|P6초→LaVine2초; 지정 직접창출/수신준비 목표 불충족|각40|
| 수정 |47:52–48:00|P3초→LaVine5초; LaVine 본인의 재진입·수신을 포함한 이른 공동 핸드오프만 완료|각40|

같은Chicagoclosing5(Melo/LaVine/P/Mark/Carter), NOP대응5(Lonzo/Bledsoe/Ingram/Zion/Adams), 각포지션5unique·동시10명이다. Ingram/Zion/Adams의 반응과 LaVine의 자발적 수신은 root선택된가상관측이며 실제 NBA 경기·임상·슈팅 성공 인증이 아니다. 중간16초47:36–47:52는 event/control/score null이다. 그 사이의 소유권·실점·턴오버를 만들지 않는다.

S2선택비교는 LV직접8초 기준→P3/LV5로 LV−3/P+3/Melo0이다. 별도 Melo3/LV5기준과 같은P3/LV5의 비교는 Melo−3/P+3/LV0이며 별도대안이력이다. 한소유권의 비용6초로 더하지 않는다. Duarte ownread와 Jaquez cutting선택 조건도 보존하되 이경기에 새수비성공을 인증하지 않는다.

## 확인과 남은 범위

before-write build에서 source-return alias를 재물리파싱으로 거부하고, returned 계약함수·원Γ·각날짜/두시계/포지션·13nomination·40초·독립cost·nullscore/wholeflags를 caller에서 대조한다. 조상 전체constructor는 실행하지 않았다. writer 음성은 독립peer로 세지 않는다. 새consumer 독립수용 전 metadata는 false이며 root가 별도review 후 현재성을 채택한다.

완료: **admitted fictional domain의 두 공동역할 수정 관측**. 첫옵션득점/효율/경기승리·wholeS1/S2·S3 QUAL1·wholeA10/매크로4·MVP/우승/미래시즌은 미선택이다. 실제계약접수/센트/진단·실제당일명단 인증도false다.

|큰묶음|상태|
|---|---|
|1|COMPLETE|
|2|COMPLETE|
|3|COMPLETE|
|4|INCOMPLETE|
|5|INCOMPLETE|
|6|INCOMPLETE|
|7|INCOMPLETE|

미완료4개/6번까지3개. v0.30 PARTIAL·CLOSED·Pack0·원고0.
'''

def self_test():
    old=construct;count=0
    def pos(s):
        p=old(s);d=p['selected_windows'][1]['NOP_positions'];d['PG'],d['SG']=d['SG'],d['PG'];return p
    def alias(s):
        p=old(s);s[PACK]['NOP_FY24_contract_function']['ten_same_owner_status_functions'][0]['old_Gamma_preserved']=False
        p['lawful_NPC_function_selected']['ten_same_owner_status_functions'][0]['old_Gamma_preserved']=False;return p
    def points(s):
        p=old(s);p['selected_windows'][1]['shot_or_score']=2;return p
    for f in [pos,alias,points]:
        with patch(__name__+'.construct',f):
            try:build()
            except AssertionError:count+=1
            else:raise AssertionError('Writer meaningful returned mutation accepted: '+f.__name__)
    return count

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args()
    p=build();assert validate(p)==[]
    if a.write:
        (ROOT/OUT).write_text(serial(p),encoding='utf-8');(ROOT/OUT).with_suffix('.md').write_text(markdown(p),encoding='utf-8')
    if a.check:
        saved=json.loads((ROOT/OUT).read_text(encoding='utf-8-sig'));assert validate(saved)==[]
        assert (ROOT/OUT).with_suffix('.md').read_text(encoding='utf-8-sig')==markdown(p),'MD stale'
    n=self_test() if a.self_test else None
    print(serial({'current':True,'selected_windows':2,'active_per_team':13,'team_player_seconds_per_window':40,'writer_returned_negative_controls':n,'whole_A10':False,'manuscript_allowed':False}))
if __name__=='__main__':main()
