"""Two nominated regulation role executions; unresolved contracts remain HOLD.

The already selected Chicago date states are consumed from canon, not inferred
from the health proposal's historical generation metadata. No Jordan assignment,
Olynyk price, draft result, game result or overtime is selected here.
"""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch
import build_chicago_2021_22_opponent_capacity_dispatcher as dispatcher

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_chicago_detroit_2021_two_date_working_execution.py'
OUT = 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_WORKING_EXECUTION.json'
MD = OUT.replace('.json','.md')
BASELINE = '51ab52af234c67ec1f34fe4dade717ba2bad9561'
AUTH = 'canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json'
HEALTH = 'simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json'
OPERATING = 'research/DETROIT_2021_OPENING_NAMED_OPERATING_FAMILY_2026_10_07.json'
RESIDUAL = 'research/DETROIT_2021_INITIAL_RESIDUAL_COST_FAMILY_2026_10_07.json'
PAIR = dispatcher.DET
PINS = {
 AUTH:'51b24c8a6bc1eb703568adced46b3ffa15845e85e8da10da1242bddf941df960',
 HEALTH:'274a35e163c7f6fd7f0d3e5494b3c46753aaf9900036676be935f17a9d538c32',
 OPERATING:'7490b1a46a744088980c115680140383615a2e6ec92901e1fdd901c326861be0',
 RESIDUAL:'cf90a22c8fc7818a92a054c331347f836933ba0af83655464805048bcded5205',
 PAIR:'45f204a0f213ea51b9de0a1d0ae47b50568a8d990d339822d9cd49a6ca274a00',
 dispatcher.OUT:'e1659c32a53b2ad200b759ed88d7cabde2dfe50474569e9b7860a43497b2dfa5',
 dispatcher.SELF:'7737524c3e5c457d102de1f324bcc7db0ac3aadcd1eb6520d311f2535ec21f95',
}
IDS = ('0022100004','0022100030')
DATES = ('2021-10-20','2021-10-23')
STATE = 'COBY_OUT'
ROLE = 'A_garza_two_way_retained'
POSITIONS = ('PG','SG','SF','PF','C')

def require(ok,message):
    if not ok:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()

def load(root,path):
    return json.loads((root/path).read_text(encoding='utf-8-sig'))

def sources(root):
    out={}
    for path,pin in PINS.items():
        require(sha(root/path)==pin,'Source changed: '+path)
        if not path.endswith('.json'):
            continue
        obj=load(root,path)
        require(obj==json.loads((root/path).read_text(encoding='utf-8-sig')),'Loader changed source object')
        out[path]=obj
    a=out[AUTH]
    require(a['status']=='SELECTED_AND_82_CHICAGO_DATE_STATES_EXECUTED_OPPONENT_AND_RESULT_HOLD'
            and a['route']=='H21_CHI_BINARY_58_NORMAL_24_COBY_OUT','Canonical health authority changed')
    ref=a['selected']['selected_date_rows']
    require(ref=={'path':HEALTH,'pointer':'/selected_dates','sha256':PINS[HEALTH]},'Canonical selected rows binding changed')
    require(a['selected']['hypothetical_positive_player_availability_adopted']
            and a['selected']['hypothetical_Coby_absence_adopted'],'Canonical health selection missing')
    op=out[OPERATING]; x=out[RESIDUAL]
    require(op['certification']['independent_review_completed'] and not op['certification']['whole_source_supported_cost_family_pass'],'Operating family scope changed')
    require(op['named_cap_route_A']['same_route_room_deficit_with_that_delta']==4161378
            and not op['named_cap_route_A']['complete_path_closed'],'Original A room deficit overwritten')
    require(x['base_ledger']['sum']==100052228 and x['initial_X']['public_named_family_upper']==5361732
            and x['initial_X']['legal_q_family']==[3000000,7000040],'Reviewed economic domain changed')
    require(x['initial_X']['changed_longterm_contract_offer_is_unselected_consequential_comparison']
            and x['initial_X']['exact_q_selected'] is None,'Price comparison promoted')
    return out

def assert_clock(w,h):
    require(w['CHI_state']==STATE and w['DET_roster_candidate']==ROLE,'Wrong selected role')
    totals={'CHI':Counter(),'DET':Counter()}; position_seconds={t:Counter() for t in totals}; end=0
    for s in w['simultaneous_segments']:
        require(s['start_second']==end and s['end_second']-end==s['seconds']>0,'Bilateral elapsed clock gap')
        require(s['quarter']==end//720+1 and s['end_second']<=(end//720+1)*720,'Quarter binding changed')
        for team in totals:
            lineup=s[team]
            require(set(lineup)==set(POSITIONS) and len(set(lineup.values()))==5,'Five-position lineup invalid')
            n=w['nominations'][team]
            require(set(lineup.values())<=set(n['active'])<=set(n['standard']),'Positive lineup outside active roster')
            for pos,p in lineup.items():totals[team][p]+=s['seconds'];position_seconds[team][pos]+=s['seconds']
        end=s['end_second']
    require(end==2880,'Regulation clock incomplete')
    for team,n in w['nominations'].items():
        require(len(n['standard'])==15 and len(n['two_way'])==2 and len(set(n['standard']+n['two_way']))==17,'15+2 candidate identity invalid')
        require(len(n['active'])==12 and len(set(n['active']))==12 and len(n['inactive'])==3,'Active/inactive nomination invalid')
        require(set(n['active'])|set(n['inactive'])==set(n['standard']) and not set(n['active'])&set(n['inactive']),'STD nomination partition invalid')
        require(dict(totals[team])==n['positive_seconds'] and sum(totals[team].values())==14400,'Player seconds changed')
        require(dict(position_seconds[team])==dict.fromkeys(POSITIONS,2880),'Position clock changed')
    hn=h['working_chicago_operational_availability'];cn=w['nominations']['CHI']
    require(cn['active']==hn['working_active_nominees'] and cn['inactive']==hn['standard_inactive_nominees'],'Selected date nomination changed')
    require(cn['positive_seconds']=={p:m*60 for p,m in h['selected_regulation_player_minutes'].items()},'Selected CHI seconds changed')
    require(set(cn['positive_seconds'])==set(hn['positive_minute_players']),'Selected positive health domain changed')
    require('Patrick Williams' in w['nominations']['DET']['standard'] and 'Patrick Williams' not in cn['standard'],'DET Patrick Williams identity transplanted to CHI')

def make_row(h,w,index):
    return {
      'game_number':h['game_number'],'game_id':h['game_id'],'date':h['date'],'home':h['home'],'away':h['away'],
      'selected_chicago_state':STATE,'recommended_DET_role':ROLE,
      'source_pair_game_id':'0022100004','source_pair_witness_pointer':'/witnesses/'+str(index),
      'canonical_health_row_pointer':'/selected_dates/'+str(h['game_number']-1),
      'interval':{'start':'2021-10-20','end_inclusive':'2021-10-23','kind':'TWO_NAMED_GAME_ROLE_AND_POSITIVE_AVAILABILITY_MODEL',
                  'date_bridge_model':'Same A working roster, nominees and positive operational availability at both named dates; no new intervening role-affecting event selected. This is a two-date design model, not a historical no-event certificate.',
                  'continuous_all_contracts_executed':False,'contract_clearance_and_15plus2_condition':'DET_A_REGISTRATION_FINANCIAL_HOLD'},
      'working_role_and_clock_execution_prepared':True,'root_routine_recommendation_adopted':False,
      'CHI_date_health_authority_selected':True,'DET_positive_availability_recommended':True,
      'nominations':deepcopy(w['nominations']),
      'DET_positive_operational_availability':sorted(w['nominations']['DET']['positive_seconds']),
      'zero_minute_clinical_status':None,'clinical_medical_certificate':False,
      'simultaneous_segments':deepcopy(w['simultaneous_segments']),
      'regulation_elapsed_seconds':2880,'player_seconds_each_team':14400,
      'overtime_selected':False,'full_48plusOT_game_execution':False,'score':None,'winner':None,
      'actual_bilateral_contract_or_registration_execution':False,'whole_source_supported_bilateral_financial_execution':False,
    }

def assert_row(row,h,w,index):
    # The independent caller invokes this after make_row, including patched returns.
    require((row['game_number'],row['game_id'],row['date'],row['home'],row['away'])==
            tuple(h[k] for k in ('game_number','game_id','date','home','away')),'Returned date identity changed')
    require(row['selected_chicago_state']==h['selected_chicago_state']==STATE,'Returned selected CHI state changed')
    require(row['recommended_DET_role']==ROLE and row['source_pair_game_id']=='0022100004'
            and row['source_pair_witness_pointer']==f'/witnesses/{index}','Returned DET/source role changed')
    require(row['nominations']==w['nominations'] and row['simultaneous_segments']==w['simultaneous_segments'],'Returned paired roles/clock changed')
    require(row['DET_positive_operational_availability']==sorted(w['nominations']['DET']['positive_seconds']),'Returned DET availability changed')
    require(row['interval']['start']=='2021-10-20' and row['interval']['end_inclusive']=='2021-10-23'
            and row['interval']['kind']=='TWO_NAMED_GAME_ROLE_AND_POSITIVE_AVAILABILITY_MODEL'
            and not row['interval']['continuous_all_contracts_executed'],'Role interval promoted to contract execution')
    require(row['working_role_and_clock_execution_prepared'] and row['CHI_date_health_authority_selected']
            and row['DET_positive_availability_recommended'] and not row['root_routine_recommendation_adopted'],'Prepared/selected authority changed')
    require(row['zero_minute_clinical_status'] is None and not row['clinical_medical_certificate'],'Zero-minute medical inference')
    require(row['regulation_elapsed_seconds']==2880 and row['player_seconds_each_team']==14400,'Returned elapsed/totals changed')
    require(not any(row[k] for k in ('actual_bilateral_contract_or_registration_execution',
            'whole_source_supported_bilateral_financial_execution','overtime_selected','full_48plusOT_game_execution'))
            and row['score'] is None and row['winner'] is None,'Unselected financial/result authority promoted')

def economic_comparison(s):
    """Unselected A-preserving comparison. The original A deficit is not erased."""
    x=s[RESIDUAL]['initial_X']['public_named_family_upper']; base=s[RESIDUAL]['base_ledger']['sum']
    qmax=min(12195122,112414000-base-x)
    increments=[
      {'player':'Saben Lee','delta_upper':3000000-925258,'route':'NEW_MINIMUM_1_OR_2_YEARS_NO_BONUS'},
      {'player':'Frank Jackson','delta_upper':3000000-1939350,'route':'NEW_MINIMUM_1_OR_2_YEARS_NO_BONUS'},
      {'player':'Isaiah Livers','delta_upper':3000000,'route':'NEW_MINIMUM_1_OR_2_YEARS_NO_BONUS'},
      {'player':'Jalen Suggs','delta_upper':0,'route':'ROOKIE_UPC_AT_MOST_RETAINED_120PCT_HOLD'},
      {'player':'Cory Joseph','delta_upper':4910000,'route':'ROOM_MLE_TWO_YEARS_5PCT_NO_COMBINED_NTMLE'},
      {'player':'Rodney McGruder','delta_upper':3000000,'route':'NEW_MINIMUM_1_OR_2_YEARS_NO_BONUS'},
      {'player':'Hamidou Diallo','delta_upper':5200000-2079826,'route':'CONDITIONAL_CONTINUOUS_PRIOR_SERVICE_BIRD'},
      {'player':'Santi Aldama','delta_upper':3000000,'route':'VALID_NONACCEPTED_OPERATIVE_REQUIRED_TENDER_NOT_UPC'},
      {'player':'Trey Lyles','delta_upper':3000000,'route':'NEW_MINIMUM_2_YEARS_NO_BONUS_NOT_ORIGINAL_REPORTED_PRICE'},
    ]
    total=sum(i['delta_upper'] for i in increments)
    return {
      'classification':'UNSELECTED_PRICE_AND_REGISTRATION_COMPARISON_NOT_EXECUTED',
      'original_A_price_route_room_deficit':s[OPERATING]['named_cap_route_A']['same_route_room_deficit_with_that_delta'],
      'original_A_price_route_complete':False,'base_current_and_old_and_holds':base,
      'admitted_public_initial_X_interval':[0,x],'actual_X':None,
      'universal_sufficient_q_interval':[3000000,qmax],'exact_q_selected':None,
      'q_function':'q in [3000000,min(12195122,112414000-100052228-X)]',
      'changed_Olynyk_offer_requires_consequential_direction_resolution':True,
      'Lyles_and_other_new_minimum_prices_are_unselected_consent_proposals':True,
      'minimum_3000000_is_conservative_upper_not_salary_selection':True,
      'increments_after_q':increments,'increments_after_q_upper':total,
      'nonassignment_slot_clearance_comparison':{
        'date_hypothesis':'2021-09-01','players':['Sekou Doumbouya','Jahlil Okafor'],
        'method':'WAIVER_WITH_FULL_CURRENT_REPORTED_SALARY_RESERVED_NO_OFFSET_ASSUMED',
        'preserved_charge':3613680+2130023,'waiver_cost_removed':0,'actual_waivers':False,'proposal_selected':False,
        'new_Jordan_trade_selected':False,'Jordan_incoming_charge':0,
        'Jordan_cash_or_four_second_rights_copied':False},
      'cap_room_after_q_endpoint':112414000-(base+x+qmax),
      'final_normal_salary_screen_upper':base+x+qmax+total,
      'apron_comparison_only':{'apron':143002000,'margin':143002000-(base+x+qmax+total),
                             'below_apron_is_not_whole_financial_or_hardcap_certificate':True},
      'TW_Garza_and_Chris_Smith':'ZERO_TEAM_SALARY_CLASS_COMPONENT_NOT_ZERO_CASH_COMPENSATION; admitted legal TW eligibility/terms remain conditions',
      'Garza_standard_conversion_selected':False,
      'Aldama_pending_tender_is_salary_reservation_not_sixteenth_standard_player':True,
      'rights_DB1_admissions_are_not_author_locked_draft_choices':True,
      'new_financial_choice_or_actual_consent':False,'whole_financial_family_executed':False,
      'future_years_options_guarantees_and_new_notices_reopen':True,
    }

def assert_economics(e,s):
    require(e['original_A_price_route_room_deficit']==4161378 and not e['original_A_price_route_complete'],'A original financial HOLD erased')
    require(e['base_current_and_old_and_holds']==100052228 and e['admitted_public_initial_X_interval']==[0,5361732],'Initial economic scope changed')
    require(e['universal_sufficient_q_interval']==[3000000,7000040] and e['exact_q_selected'] is None,'Unselected q family changed')
    expected=[2074742,1060650,3000000,0,4910000,3000000,3120174,3000000,3000000]
    require([i['delta_upper'] for i in e['increments_after_q']]==expected and e['increments_after_q_upper']==sum(expected),'New prices/reservations changed')
    clear=e['nonassignment_slot_clearance_comparison']; original=s[RESIDUAL]['base_ledger']['current_8']
    require(clear['players']==['Sekou Doumbouya','Jahlil Okafor'] and clear['preserved_charge']==sum(original[p] for p in clear['players'])
            and clear['waiver_cost_removed']==0,'Waiver erased protected/current cost')
    require(not any(clear[k] for k in ('actual_waivers','proposal_selected','new_Jordan_trade_selected','Jordan_cash_or_four_second_rights_copied'))
            and clear['Jordan_incoming_charge']==0,'Unselected Jordan/waiver direction promoted')
    require(e['final_normal_salary_screen_upper']==135579566 and e['apron_comparison_only']['margin']==7422434,'Conditional economic screen changed')
    require(e['changed_Olynyk_offer_requires_consequential_direction_resolution']
            and not e['new_financial_choice_or_actual_consent'] and not e['whole_financial_family_executed'],'Unselected consequential prices promoted')

def build(root=ROOT):
    s=sources(root)
    # One accepted small dispatcher reconstruction, not the older financial DAG.
    d=dispatcher.build(root)
    require(s[dispatcher.OUT]==d,'Saved dispatcher differs from consumed primitive-source reconstruction')
    windex,w=next((i,x) for i,x in enumerate(s[PAIR]['witnesses']) if x['id']==STATE+'__'+ROLE)
    a=next(x for x in s[OPERATING]['roster_candidates'] if x['id']==ROLE)
    require(w['nominations']['DET']['standard']==a['standard_candidate']
            and w['nominations']['DET']['two_way']==a['two_way_candidate']
            and w['nominations']['DET']['active']==a['working_active_standard_12']
            and w['nominations']['DET']['inactive']==a['working_inactive_standard_3'],'Role roster differs from named A family')
    rows=[]
    for gid,date in zip(IDS,DATES):
        h=next(x for x in s[HEALTH]['selected_dates'] if x['game_id']==gid)
        require(h['date']==date and h['opponent']=='DET' and h['selected_chicago_state']==STATE,'Canonical two-date state changed')
        catalog=next(x for x in d['capacity_index'] if x['id']=='DET::'+STATE+'__'+ROLE)
        require(catalog['source_game_id']=='0022100004' and catalog['nominations']==w['nominations'],'Capacity source relabeled')
        assert_clock(w,h)
        row=make_row(h,w,windex); assert_row(row,h,w,windex); rows.append(row)
    e=economic_comparison(s);assert_economics(e,s)
    return {'id':'CHICAGO_DETROIT_2021_TWO_DATE_WORKING_EXECUTION','baseline_main':BASELINE,
      'status':'TWO_DATE_ROLE_AVAILABILITY_AND_REGULATION_EXECUTION_PREPARED_ROOT_REVIEW_PENDING_FINANCIAL_HOLD',
      'source_sha256':{**PINS,SELF:sha(root/SELF)},'hash_convention':'UTF8 BOM removed, CRLF/CR to LF; raw cache SHAs unchanged',
      'scope':{'classification':'DELEGATED_WORKING_ROLE_RECOMMENDATION_WITH_EXISTING_CANON_CHI_HEALTH',
               'actual_clinical_or_contract_execution':False,'new_result_or_OT':False,'new_consequential_transaction_or_price_selection':False,
               'role_selection_is_not_financial_admission_or_author_locked_destination':True},
      'authority':{'CHI_selected_date_authority':AUTH,'selected_date_rows':HEALTH,
                   'DET_routine_recommendation':'Adopt reviewed A roles, positive availability and active nominees only for Oct20/Oct23 under existing health/operating delegation; root review pending.',
                   'DET_economic_conditions':'Existing A original price HOLD remains. Nonassignment waiver/minimum/q comparison is unselected, not contract execution.',
                   'canonical_or_financial_selection_written':False},
      'rows':rows,'unselected_A_preserving_economic_comparison':e,
      'summary':{'dates':2,'regulation_role_clocks_prepared':2,'elapsed_seconds_each_date':2880,'each_team_player_seconds_each_date':14400,
                 'CHI_selected_COBY_OUT_dates':2,'DET_recommended_positive_players_each_date':10,
                 'standard_candidate_each_team':15,'TW_candidate_each_team':2,'active_standard_nominees_each_team':12,
                 'whole_bilateral_registration_or_financial_executions':0,'result_or_OT_selections':0},
      'remaining_named_inputs':[
        'Root review/adoption of the two-date routine DET role/positive availability recommendation; no renewed human health approval is required.',
        'Consequential Olynyk price/direction remains unselected; original A original-price room deficit4,161,378 has not been closed.',
        'A15 financial/registration prefix requires a selected lawful clearance implementation; the nonassignment two-waiver full-charge proposal is not executed.',
        'Trey Lyles/minimum counterparties and offers are comparisons, not automatic acceptance; future Lyles/Bagley consequences reopen after a financial selection.',
        'Suggs/Livers/Garza/Chris Smith/Aldama rights/UPC/Tender conditions remain explicit DB1 and operating-family admissions, not locked2021 draft or actual filing claims.',
        'The interval carries nominated role/positive availability across these two dates only; no opponent full-season health, game winner, score or OT is selected.'],
      'certification':{'independent_review_completed':False,'routine_DET_recommendation_selected_by_root':False,
                       'whole_bilateral_contract_or_registration':False,'actual_medical_or_acceptance':False,
                       'whole_macro3_complete':False,'new_author_lock':False,'central_or_REGISTER_changed':False,'manuscript_written':0}}

def validate(value,root=ROOT):
    try:return [] if value==build(root) else ['Saved object differs from source-bound two-date implementation']
    except (ValueError,KeyError,StopIteration) as exc:return [str(exc)]

def markdown(b):
    return '''# Chicago–Detroit 두 날짜 작업 실행\n\n상태: `'''+b['status']+'''`. 기준 main `'''+BASELINE+'''`.\n\n## 실제 연결한 범위\n\n- **10월20일 `0022100004` / 10월23일 `0022100030`**: 새 canon 권위의 `COBY_OUT`을 소비한다. Markkanen32 / Caruso18 / 주인공32를 보존한다.\n- DET A의 10명 양수 가용성·12active/3inactive·15STD2TW와 기존 역할을 두 날짜에 권고 실행했다. 각 날짜 양팀 동시 **2,880초 / 각240분**을 구성했다. root 권고 채택 검문 대기이며 전체 계약 실행은 아니다.\n- DET Patrick Williams는 DET 신원이다. CHI에 원역사 Patrick Williams나 그 부상창을 옮기지 않는다. 0분은 임상 결장 판단이 아니다.\n- 10월23일은 원10월20일 증인을 원포인터로 보존하면서 같은 양수 가용성/역할을 이 두 날짜에 적용하는 **명시적 가상 일정·감독 모델**이다. 실제 역사 출전·새 시즌 건강 자동 복사가 아니다.\n\n## 비용은 여전히 별도 HOLD\n\n원 A 가격 경로의 cap room 부족 **4,161,378달러**는 그대로다. 역할 A 권고는 Olynyk의 삭감 제안이나 Jordan 공동거래를 선택하지 않는다.\n\n비교 후보는 검문된 공개 X≤5,361,732 가족에서 q∈[3,000,000,7,000,040] 충분조건을 사용하고, Garza TW 유지/Lyles의 적법2년 최소급여 함수·보너스0를 제안한다. **3백만 달러는 최소함수의 보수 상단이지 합의 급여가 아니다.** 이 조건부 비교의 최종 normal screen 상단135,579,566, apron 비교 여유7,422,434이며 실제 전체 합법 비용 인증이 아니다.\n\nA15의 Sekou/Okafor 부재에는 별도 실행 경로가 필요하다. 미선택 비양도 waiver 비교는 두 현재 급여 **5,743,703달러 전액을 기존 base에 남긴다**. Jordan·현금·4개2R을 복사하지 않는다. 계약 clearance/수락은 미실행이며 이 후보가 기존 중요 공동거래 선택을 대체하지 않는다. Aldama의 유효 미수락 RequiredTender는 비용 예약이며16번째STD가 아니다. Suggs UPC/DB1 권리·Garza/Smith TW의 합법 자격은 계속 조건이다.\n\nOlynyk 가격은 장기 계약의 중요한 비교이며 선택되지 않았다. 새로운 Lyles 가격/뒤 Bagley 영향도 선택되지 않았다. 따라서 작업 역할/양수 건강·감독 계획만 준비됐고 **전체 양팀 날짜별 계약·등록 실행은0**이다. 결과/점수/OT도0이다.\n\n## 검문 및 남은 입력\n\n생성기는 canon의 선택행 SHA를 직접 소비하고, 작은 공통 dispatcher를 원primitive에 재대조한다. 두 날짜·신원·active·각 위치48분·선수 초합·반환 시계·미선택 재정 플래그를 caller에서 검문한다. 독립 검토는 아직 미완료다. 과거 비용192가족·전체 법적 조상 검문은 반복하지 않았다.\n\n남은 것은 root의 루틴 역할 권고 채택, A의 명명된 계약 clearance/가격 방향, 미서명권리/UPC/Tender 조건 및 이후 경기 입력이다. 미공개 장부·실수락 영수증·모든 미래 부재를 새 필수 조건으로 요구하지 않는다.\n\n## 현행 진행표\n\n[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md) / [현재 상태](../PROJECT_STATE.md).\n\n|번호|범위|현황|\n|---|---|---|\n|1|2020 드래프트 연쇄|완료 보존|\n|2|Chicago2020–21|완료 보존|\n|3|2021–23 거래·계약|두 DET 역할 실행 준비; 계약·중요 방향 HOLD|\n|4|장기 커리어|후속 시즌 입력 대기|\n|5|결말·전체 구조|기존 골격·후속 기능 연결 진행|\n|6|집필 규격·Context Pack|현행 누적 기능 등록 참조 / 실제Pack0|\n|7|통합·독립·작가 승인|부분 검문 진행 / 최종 미완료|\n\n미완료 큰 묶음 **5개**(6번까지4개). `v0.30 PARTIAL` / 설계·원고 `CLOSED` / 원고0. 중앙·원장·정본 선택 변경0.\n'''

def self_test(root=ROOT):
    tests=[]; original=make_row
    def wrong_state(h,w,i):
        r=original(h,w,i);r['selected_chicago_state']='NORMAL';return r
    with patch(__name__+'.make_row',wrong_state):
        try:build(root);raise AssertionError('Wrong selected state accepted')
        except ValueError:tests.append('CANON_COBY_OUT_RETURNED_ROW_NORMAL_REJECTED')
    orig_e=economic_comparison
    def free_waiver(s):
        e=orig_e(s);e['nonassignment_slot_clearance_comparison']['preserved_charge']=0;return e
    with patch(__name__+'.economic_comparison',free_waiver):
        try:build(root);raise AssertionError('Free waiver accepted')
        except ValueError:tests.append('WAIVER_CURRENT_PROTECTED_CHARGE_ZERO_REJECTED')
    return tests

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
    b=build()
    if args.write:(ROOT/OUT).write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(b),encoding='utf-8')
    if args.check:
        require(load(ROOT,OUT)==b,'Saved JSON stale');require((ROOT/MD).read_text(encoding='utf-8-sig').replace('\r\n','\n')==markdown(b),'Saved MD stale')
    tests=self_test() if args.self_test else []
    print(json.dumps({'current':True,'summary':b['summary'],'writer_negative_controls':tests},ensure_ascii=False))

if __name__=='__main__':main()
