"""Preserve E1-E4 alternatives as consensual forms, never select a franchise path."""
import argparse
import copy
import hashlib
import json
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import fitz
from bs4 import BeautifulSoup
import build_carter_2021_extension_candidate_family as carter
import build_chicago_2022_rookie_rfa_qo_family as qo

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_protagonist_2022_contract_candidate_family.py'
OUT='research/PROTAGONIST_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07.json'
MD=OUT[:-5]+'.md'
BASELINE='16167cf4f6f2da50cbb1c054b948f9efedee3ddc'
PINS={'simulation/CHICAGO_2021_23_CONTINUATION.json': '3156582b1753953bd9f79c96231a476c0483671d0f1335048b276cc1536d9cca', 'simulation/CHICAGO_2021_23_CONTINUATION_INPUTS.json': '5632957e5e0a02f2d6f241900a3bef2c5790a8993c3494986e383ca3cbff1be3', 'simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE_INPUTS.json': '4b66d96a274fa4d31e41f6256192449e8b43a6dfc00e8f4e44f4cbd76e83bf78', 'research/CHICAGO_2022_ROOKIE_RFA_QO_FAMILY_2026_10_07.json': 'ceac38803f42eabff9032023a20ddbbcd1f739d4831a22fcba6e62fea096a14d', 'tools/build_chicago_2022_rookie_rfa_qo_family.py': '8ec5d15b04069d300f5b7bd5a70459f757c23a297ca966145045689d66a8cc2b', 'research/CARTER_2021_EXTENSION_CANDIDATE_FAMILY_2026_10_07.json': '070f1393070644540642284e9f1a6b49a2c6d1c1903fade2610d8570344d1f21', 'tools/build_carter_2021_extension_candidate_family.py': '3270d087a499240723ba0e8aba3a887aae4f144cc1b23da51121c658b75022f8', 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json': '253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088', 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json': '9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce', 'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2'}
SCHEDULES={'E1':[18000000,19440000,20880000,22320000], 'E2':[22000000,23760000,25520000,27280000], 'E3':[30913750,33386850,35859950,38333050,40806150], 'E4':None}
SOURCE_STRUCTURES={'E1':'2021 extension, 2022 start','E2':'2022 direct Bird RFA, recommended budget','E3':'2022 five-year Bird max, conditional earned value','E4':'2022 one-year QO then 2023 UFA'}
CBA=qo.CBA
CBAPAGES=[29,38,40,44,54,55,57,58,60,61,81,206,207,208,209,218,219,223,240,245,246,248,252,253,255,256,299,309,310,311,315,316,317,318,398,399,561]
RAW={'id':'NBA_CAP2022','url':'https://pr.nba.com/nba-salary-cap-2022-23-season/','cache_path':'C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-chi-core2022-20261007/NBA_CAP2022.html','http_status':200,'raw_sha256':'2e76093cfc91b6257f18cddd25441090118f36bd8a942259fbc340438ff5e57f','bytes':109871,'classification':'REUSED_PRIMARY_NBA_OFFICIAL_RELEASE_DIRECT_BODY_READ','published_date':'2022-06-30'}
FAILED={'url':RAW['url'],'http_status':None,'http_status_not_preserved':True,'observed_response_body':'ACCESS_DENIED_ERROR_PAGE; HTTP200_PRIMARY_BODY_ASSERTION_FAILED','cache_path':'C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-protagonist-contract-20261007/NBA_CAP2022.html','bytes':425,'raw_sha256':'e698701b774df6b30ee5f4f0a6c89cec4e87a0f43d8e7d85955704f024b9eb27','body_used':False,'repeat_attempts':0,'successful_web_open_primary_body_read':True}
POLICY={'source_alternative_ids':['E1','E2','E3','E4'],'selected_contract':None,'exact2018pick':None,'pick_domain':list(range(16,31)),
 'first_NBA_contract_season':'2018-19','same_franchise':'Chicago','fourth_rookie_year_options_valid_and_services_completed':'ADMITTED_CANDIDATE_CONDITION_NOT_ACTUAL_CERTIFICATE',
 'full_Bird_continuity':'RETAIN_SAME_CHICAGO_WITHOUT_RIGHTS_RENUNCIATION_OR_BREAK_IN_QUALIFYING_SERVICE; CONDITIONAL',
 'E1_candidate_execution_ET':'2021-10-15T12:00:00','E2_E3_candidate_execution_ET':'2022-07-07T12:00:00',
 'E4_QO_issue_candidate':'2022-06-29','E4_QO_issue_window_condition':'NBA_SEASON_HAS_ENDED; XI4a1_WINDOW_IS_OPEN',
 'E4_acceptance_candidate_ET':'2022-07-07T12:00:00','E4_withdrawn_or_replaced_before_acceptance':False,
 'E4_MaximumQO_selected':False,'offer_sheet_FirstRefusal_SandT_or_franchise_move_selected':False,
 'future_starter_statistics_selected':False,'original_contract_or_Hutchison_exact_terms_selected':False,
 'actual_team_player_consent':None,'actual_contract_acceptance_or_receipt':None,'whole2022_23_cost_PASS':False,
 'new_author_lock':False,'macro3_complete':False,'REGISTER_promoted':False,'manuscript_allowed':False}
NEW_TERMS={'E1_E2_E3':{'protection':'FULL_BASE_FOR_LACK_OF_SKILL_AND_INJURY_ILLNESS_SUBJECT_TO_STANDARD_CBA_CONDITIONS','payment':'UPC_PARAGRAPH3_STANDARD',
 'option':None,'ETO':None,'signing_bonus':0,'likely_performance_bonus':0,'unlikely_performance_bonus':0,'promotional_bonus':0,'new_assignment_bonus':0,'loan':0,'new_NBA_buyout':0,
 'all_salaries_subject_to_mandatory_minimum_maximum_and_CBA_conformity':True},
 'E1_original_bonus':'PRESERVE_ORIGINAL_TERM; IF_UNEARNED_ORIGINAL_BONUS_EXISTS_MUTUAL_XXIV2a5_REPLACEMENT_EX4_EXCLUDES_EXTENDED_TERM_ONLY',
 'E4_terms':'XI1c(i),(ii),(v): ONE_YEAR_QO; FULL_BASE_SKILL_INJURY_PROTECTION_STANDARD_PAYMENT; ALLOWABLE_OLD_TERMS_UNCHANGED; OLD_BONUSES_NOT_ASSERTED_ZERO',
 'exact_prior_assignment_bonus_percentage':None,'old_accrued_or_dead_obligations_erased':False,'E4_compensation_continues_exact_QO_function_not_flat7921300':True}

def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def rat(q):return {'numerator':q.numerator,'denominator':q.denominator}
def ceil(q):return -(-q.numerator//q.denominator)
def policy():return copy.deepcopy(POLICY)
def terms():return copy.deepcopy(NEW_TERMS)
def source_options():return load('simulation/CHICAGO_2021_23_CONTINUATION.json')['contract_options']

def source_evidence():
    assert hashlib.sha256(CBA.read_bytes()).hexdigest()==carter.CBA_SHA
    with fitz.open(CBA) as d:
        pages=[{'PDF_1based':n,'fitz_text_LF_sha256':hashlib.sha256(d[n-1].get_text().replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()} for n in CBAPAGES]
        bodies={n:' '.join(d[n-1].get_text().split()) for n in CBAPAGES}
    for n,words in {29:['Qualifying Veteran Free Agent'],55:['Minimum Annual Salary Scale','first Season'],57:['twenty-five percent'],218:['eight percent'],223:['12:01 p.m.','Prior Team'],245:['Rookie Scale Extensions'],246:['second Option Year'],252:['one-year Contract','consent'],253:['January 15','one hundred twenty'],256:['average of the aggregate Salaries'],299:['five (5) Seasons'],399:['extended term']}.items():
        for w in words:assert w in bodies[n],f'CBA anchor {n}/{w}'
    for raw in [RAW,FAILED]:
        b=Path(raw['cache_path']).read_bytes();assert hashlib.sha256(b).hexdigest()==raw['raw_sha256'] and len(b)==raw['bytes']
    soup=BeautifulSoup(Path(RAW['cache_path']).read_bytes(),'html.parser')
    for x in soup(['script','style']):x.decompose()
    body=' '.join(soup.get_text(' ',strip=True).split())
    assert '$123.655 million' in body and '6:00 p.m. ET' in body and 'noon ET on Wednesday, July 6' in body
    calendar_sources=[r for r in load(carter.OUT)['raw_sources'] if r['id'] in ['NBA_2021_SCHEDULE','CALENDAR_CAP']]
    for r in calendar_sources:assert hashlib.sha256(Path(r['cache_path']).read_bytes()).hexdigest()==r['raw_sha256']
    return {'CBA':{'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(CBA),'raw_sha256':carter.CBA_SHA,'pages':pages},
      '2021_calendar_sources':calendar_sources,'2022_official_calendar':RAW,'fresh_attempt':FAILED,
      '2022_primary_observations':{'cap':123655000,'tax':150267000,'FA_negotiation_start_ET':'2022-06-30T18:00:00','cap_effective_ET':'2022-07-01T00:01:00','moratorium_ends_ET':'2022-07-06T12:00:00','Bird_contract_window_starts_ET':'2022-07-06T12:01:00'},
      'source_scope':'2017 applicable contract-form rules plus official2021/2022 calendars; later CBA amendments and actual2023+ execution not certified'}

def build():
    for p,h in PINS.items():assert sha(p)==h,'Source changed '+p
    c=load(carter.OUT);q=load(qo.OUT)
    assert not carter.validate(c) and not qo.validate(q),'Reviewed upstream currentness required'
    assert c['independent_review']['completed'] if 'independent_review' in c else c['summary']['independent_review_completed']
    assert q['certification']['independent_review_completed']
    opts=source_options();assert [o['id'] for o in opts]==['E1','E2','E3','E4']
    assert {o['id']:o['salary'] for o in opts}==SCHEDULES,'Original E schedules changed'
    assert {o['id']:o['structure'] for o in opts}==SOURCE_STRUCTURES,'Original E contract mechanism changed'
    assert [o['total'] for o in opts]==[80640000,98560000,179299750,None]
    assert load('simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE_INPUTS.json')['starter_reference_pick']==9
    p=policy();t=terms();assert p==POLICY and t==NEW_TERMS,'Routine policy or financial form changed'
    assert datetime.fromisoformat('2021-08-06T12:01:00')<=datetime.fromisoformat(p['E1_candidate_execution_ET'])<=datetime.fromisoformat('2021-10-18T18:00:00')
    assert datetime.fromisoformat(p['E2_E3_candidate_execution_ET'])>=datetime.fromisoformat('2022-07-06T12:01:00')
    assert datetime.fromisoformat(p['E4_acceptance_candidate_ET'])>=datetime.fromisoformat('2022-07-06T12:01:00') and p['E4_acceptance_candidate_ET'][:10]<='2022-10-01'
    assert p['E4_QO_issue_candidate']<='2022-06-29'
    src=source_evidence();max25=123655000//4
    for id,s in SCHEDULES.items():
        if s is None:continue
        assert s[0]<=max25 and all(abs(s[i]-s[i-1])<=Fraction(8*s[0],100) for i in range(1,len(s)))
        assert len(s)+(1 if id=='E1' else 0)<=5
    # Conservative numerical minimum stress, not an exact statutory rounding claim.
    # Every first-five-year ExC cell is below this envelope under cap2022 scaling.
    min_envelope=ceil(Fraction(2794384*123655000,99093000))+10
    assert min(SCHEDULES['E1'])>min_envelope and min(SCHEDULES['E2'])>min_envelope and min(SCHEDULES['E3'])>min_envelope
    old=[]
    for k in p['pick_domain']:
        row=qo.checked_scale()[k];f,_=qo.factors(row);lo=Fraction(4*row[2],5)*f;hi=Fraction(6*row[2],5)*f
        old.append({'pick':k,'current_Salary_plus_Unlikely_120_exact_upper':rat(hi),'current_base_80_exact_lower':rat(lo),
          'current_whole_dollar_component_screen_upper':ceil(hi)+2,'actual_current_salary':None,
          'E1_poisonpill_basic_Salary_reference':{'outgoing':'CURRENT_SALARY_VARIABLE; NOT_FIVE_YEAR_AVERAGE',
           'incoming_average_lower':rat((lo+sum(SCHEDULES['E1']))/5),'incoming_average_screen_upper':rat(Fraction(ceil(hi)+2+sum(SCHEDULES['E1']),5)),
           'unknown_original_unearned_assignment_bonus_not_certified_zero':True,'whole_matching_PASS':False}})
    qo_rows=[r for r in q['branch_rows'] if r['player']=='Protagonist']
    assert len(qo_rows)==30 and {r['pick'] for r in qo_rows}==set(p['pick_domain'])
    alternatives=[]
    for id,s in SCHEDULES.items():
        extension=id=='E1';one=id=='E4'
        a={'id':id,'classification':'CANDIDATE_CONSENSUAL_IMPLEMENTATION_OF_EXISTING_OPTION','author_selected':False,
           'recommended_by_old_comparison':id=='E2','recipient':'Chicago','franchise_move_or_offer_sheet_selected':False,
           'execution_candidate_ET':p['E1_candidate_execution_ET'] if extension else p['E4_acceptance_candidate_ET'] if one else p['E2_E3_candidate_execution_ET'],
           'mechanism':'VII7b_ROOKIE_EXTENSION' if extension else 'ACCEPT_VALID_XI1c_ORDINARY_QO' if one else 'VII6b1_DIRECT_FULL_BIRD_RFA_NEW_CONTRACT',
           'salary_2022_onward':s,'total_known_schedule':sum(s) if s else None,'new_term_years':len(s) if s else 1,
           'first_new_salary_cap_year_begins':'2022-07-01',
           'candidate_new_contract_effective_date':None if extension else p['E4_acceptance_candidate_ET'][:10] if one else p['E2_E3_candidate_execution_ET'][:10],
           'extension_new_term_begins_after_old_term':'2022-07-01' if extension else None,
           'no_new_contract_backdated_before_execution':True,
           'new_term_end':'2026-06-30' if id in ['E1','E2'] else '2027-06-30' if id=='E3' else '2023-06-30',
           'terms_ref':'E1_E2_E3' if not one else 'E4_terms','new_signing_performance_promotional_and_assignment_bonuses':0 if not one else None,
           'original_terms_preserved_ref':'E1_original_bonus' if extension else 'E4_terms' if one else 'EXPIRED_ORIGINAL_ACCRUED_OBLIGATIONS_NOT_ERASED; NEW_PLAIN_CONTRACT',
           'first_new_year_below_or_equal_25pct_cap':s[0]<=max25 if s else None,
           'eight_percent_raise_limit_checked':True if s else 'QO_ONE_YEAR_NO_ANNUAL_RAISE',
           'full_Bird_and_options_services_eligibility_condition_required':True,'actual_player_team_consent':None,
           'normal_cost_after_valid_contract':'LIVE_SALARY; ORIGINAL_FA_HOLD/QO_REPLACED_NOT_ADDED' if not one else 'ACCEPTED_QO_LIVE_SALARY_PLUS_ACTUAL_APPLICABLE_BONUSES',
           'apron_cost':'PLAIN_NEW_SALARY; WHOLE_TEAM_COST_NOT_PROVED' if not one else 'FULL_QO_COMPONENTS_AND_ANY_OTHER_APPLICABLE_COST; NOT_NORMAL_FA_HOLD',
           'new_MLE_SandT_or_apron_trigger_selected':False,'whole_cost_or_roster_certified':False}
        if extension:
            a['trade_boundary']={'blanket_VII8f_7a_six_month_bar_applied':False,'VII8g_poisonpill_until':'2022-07-01','reference_rows':'original_rookie_current_family','actual_trade_or_bonus_waiver_selected':False}
            a['2022_RFA_QO_scope']='NO_RFA_IF_VALID_EXTENSION_REMAINS_LIVE; NOT_A_RENUNCIATION'
        else:
            a['trade_boundary']={'general_FA_no_trade_before':'MAX(SIGNING_PLUS_THREE_MONTHS,2022-12-15)',
              'above_cap_Bird_salary_greater_than120pct_prior_no_trade_before':'MAX(SIGNING_PLUS_THREE_MONTHS,2023-01-15)',
              'above_cap_status_selected':False,'applicable_at_or_below_cap_versus_above_cap_branches_preserved':True,
              'one_year_Bird_trade_consent_required':one,'one_year_consent_actual':None,
              'if_one_year_QO_traded_Bird_continuity_changes':'VII8b_COUNTS_AS_FA_TEAM_CHANGE_NOT_TRADE' if one else None,
              'actual_trade_selected':False}
            a['2022_RFA_QO_scope']='TIMELY_ORDINARY_QO_RETAINS_ROFR_UNTIL_VALID_CHICAGO_NEW_CONTRACT' if not one else 'VALID_OUTSTANDING_QO_ACCEPTANCE; NOT_MAXIMUM_QO_OR_FIRST_REFUSAL'
        if one:
            a['QO_branch_inputs_ref']='accepted_ordinary_QO_family_30_branches'
            a['2023_UFA_condition']='ONE_YEAR_QO_COMPLETED_BY_RENDERING_SERVICES; NO_NEW_CONTRACT_OR_EXTENSION; MORE_THAN3YOS; WITHHOLDING_XI3_IS_NOT_AUTO_COMPLETION'
            a['2023_new_contract_salary_or_franchise']=None
        if id=='E3':a['max_scope']='EXISTING25PCT_BASELINE_MAX_5YEAR_DIRECT_BIRD; NOT_DESIGNATED_ROOKIE_EXTENSION; NO_30PCT_AWARD_SELECTION'
        alternatives.append(a)
    return {'id':'PROTAGONIST_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07','status':'INDEPENDENTLY_REVIEWED_EXISTING_E1_E4_CONSENSUAL_FORMS_NO_AUTHOR_SELECTION',
      'source_main_snapshot':BASELINE,'source_sha256':{**PINS,SELF:sha(SELF)},'source_hash_method':'UTF8 BOM stripped; CRLF/CR to LF',
      'sources':src,'policy':p,'candidate_terms':t,'alternatives':alternatives,'original_rookie_current_family':old,'accepted_ordinary_QO_family_30_branches':qo_rows,
      'rule_boundaries':{'E1':'2021rookieextension deadline/options/Bird eligibility; four new plus one old season; oldterm unchanged, extendedterm originalbonus exclusion only by lawful mutualEx4.',
       'E2_E3':'FullBird at12:01pm moratorium lastday, sameChicago;8%raises; up tofive newseasons. Directre-signing is not an offer-sheet match or S&T.',
       'minimum':'II6/ExC applicable first-contract/extended-term minimum and II5conformity preserved. Conservative first-five-year ExC cell stress below all proposed salaries; statutory rounding/actual future amended rules not certified.',
       'maximum':'II7a/c first-new-year25%cap=30913750 dominates105%late-pick priorfamily. ExistingE3 is that baseline;30%eligible-award upside is not selected or certified.',
       'QO':'Both options/completedservices plus timelyvalidQO; futureStarter branch and originalcomponents stay symbolic. E4 is separately conditionalacceptance, not automaticacceptance onQOissuance.',
       'old_private_costs':'No oldaccrued/dead obligations erased; no originaltradebonusabsence claimed. This newcontract-form leaf does not reopen or certify an entire private ledger.',
       'trade':'No newtrade selected. Direct Bird/QO FA signing has Dec15/conditionalJan15 waiting and QOone-year consent. Matchingcharges/actualΓ rechecked if a futuretrade selected.',
       'future':'2023+ market/nextCBA/actualregistration/wholecareer outputs are unselected. Dates/schedules are candidate terms, not historical acceptance.'},
      'summary':{'existing_alternatives':4,'known_schedules':3,'E1_total':80640000,'E2_total':98560000,'E3_total':179299750,
       'original_pick_domain_size':15,'QO_starter_branches':30,'QO_screen_upper':q['summary']['protagonist_QO_screen_upper_usd'],
       'baseline_max2022':max25,'minimum_numeric_stress_upper':min_envelope,'selected_contract':None,'actual2018pick':None,
       'independent_review_completed':True,'whole2022_23_cost_or_matching_PASS':False,'macro3_complete':False,'REGISTER_promoted':False},
      'remaining_named_inputs':['Consequential E1/E2/E3/E4 choice remains unselected; old E2 recommendation is not approval.','Exact2018pick and futureStarter branch/contractcomponents remain unselected within admitted family.','LaVine/Carter/Young/Satoransky and completeFY22 portfolio still need their own selected implementation.','2021-22 minutes/results and later financial/legal execution are not closed by this contract-form leaf.'],
      'certification':{'actual_private_cents':False,'actual_medical_or_receipts':False,'actual_team_player_consent':None,'new_author_lock':False,'whole_season':False,'manuscript_written':0}}

def validate(o):
    try:assert o==build(),'Artifact differs from current source-bound candidate';return []
    except (AssertionError,KeyError,ValueError) as e:return [str(e)]

def render(o):
    return '\n'.join(['# 주인공2022 E1–E4 계약 구현 후보','',f"상태: {o['status']}. 추천≠작가확정, 실제 수락·정확지명·전체비용 인증0.",'',
      '|기존안|형태|2022 시작 연봉·급여 일정 USD|합계|','|---|---|---|---:|',
      '|E1|2021 rookie 연장, 새4년|18m /19.44m /20.88m /22.32m|80.64m|',
      '|E2|2022 Chicago 직접 Bird RFA4년, 기존 권고|22m /23.76m /25.52m /27.28m|98.56m|',
      '|E3|2022 Chicago 직접 Bird5년·기존25% 최대 기준|30.91375m /33.38685m /35.85995m /38.33305m /40.80615m|179.29975m|',
      '|E4|유효 보통QO1년 수락→서비스완료조건2023UFA|16–30순위×선발/비선발30가지 함수 유지|미선택|','',
      '## 조건부 법적 구현','',
      'E1은2021-10-15 12:00ET 후보, 유효 창은8/6 12:01–10/18 18:00ET이다. 옵션과 Bird자격을 보존하며 현재2021–22 원급여를 새18m로 바꾸지 않는다. 새4년과 현재1년을 합해5시즌, 각 증가는 첫해8%이다. 실제 계약은 미서명이다.',
      'E2/E3는2022-07-07 12:00ET 같은Chicago 직접계약 후보다. [NBA2022공식 발표](https://pr.nba.com/nba-salary-cap-2022-23-season/)에서 cap123.655m,6/30 18시FA협상,7/6 noon모라토리움 종료를 확인하고 CBA의 Bird12:01pm 시작과 연결했다. E3 직접5년 계약을 Designated Rookie5년 연장이나30%성과 최대급으로 표시하지 않는다.',
      'E1–E3는 전액 기본급 skill/injury 보호와 표준 지급, 옵션/ETO·새 서명/성과/홍보/트레이드 보너스·대여/새 buyout0을 제안한다. 이는 새 상호합의 후보의 조건이다. 원계약의 미지 bonus를0으로 인증하지 않는다. E1은 원기간을 보존하며 unearned원bonus가 있으면 XXIV2a5의 상호합의 Ex4로 연장기간만 제외하는 후보다. 기존 발생·잔여채무를 삭제하지 않는다.',
      '18/22/30.91375m 첫해는25%max 이하이고 새4/5년의8% 일정과 기간을 검문했다. minimum은 II6/ExC와 법정 conformity를 보존하며 표의 보수적 첫5년 cell stress보다 제안액이 높다. 정확 NBA rounding이나 후년 새CBA의 실행액은 인증하지 않는다.',
      '', '## QO·거래 후손','',
      'E4는 시즌이 끝나 XI4a창이 열렸다는 조건에서6/29 유효QO 제시와7/7 수락을 별도 모델링한다. 새 미래통계 없이16–30×2분기와 원성분 함수만 재사용한다. QO발행이 수락은 아니며 두번째 옵션/서비스완료·미철회가 필요하다. 기본급보호·표준지급/허용 원조건을 유지하고 MaxQO/offer sheet/FirstRefusal을 새로 선택하지 않는다. 2023UFA는 실제 서비스완료를 전제로 하며 다른 구단·2023연봉은 null이다.',
      'E1은7/1 2022 전까지 acquiring기준 평균과 outgoing현재Salary를 분리한다. VII8f의7a six-month 일반규제를7b rookie연장에 자동 적용하지 않는다. 기존의 Γ가0이라는 주장이나 전체matchingPASS는 없다.',
      'E2/E3/E4는 FA서명 뒤3개월/12/15 규제, above-cap Bird+120%초과 조건이면1/15 규제를 보존한다. 위/아래cap 상태를 선택하지 않는다. E4는1년 Bird계약의 거래동의와 거래시 Bird연속성 변경도 별도다. 모든 실제 거래·동의는 미선택이다.',
      '', '## 재현·권위','',
      '[원CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) 및 검문된 Carter/QO leaf를 직접 재구성한다. raw/쪽/원정본 SHA는JSON에 있다. 새2022PR 직접요청은 AccessDenied본문이었고 원HTTP상태는 보존되지 않았다. 재시도0이며 기존HTTP200 원캐시와 실제webopen본문을 재검문했다. 실패본문은 근거로 사용하지 않는다.',
      '`python -B tools/build_protagonist_2022_contract_candidate_family.py --check --self-test`.',
      '', '## 현행7행 진행표','',
      '미완료 큰 묶음5; v0.30 PARTIAL, 설계/원고 CLOSED, Pack0·원고0. 현행 로드맵·누적 등록기 참조.',
      '|번호|상태|','|---|---|','|1 2020드래프트연쇄|완료|','|2 Chicago2020–21|완료|','|3 2021–23거래·계약|M1/A 유지; E1–E4 후보, 중요선택/전체실행 미완료|','|4 장기커리어|후속시즌 설계 미완료|','|5 결말·전체구조|골격 유지, 전체기능표 미완료|','|6 집필규격·Context Pack|현행 등록기 참조, 전체G13/Pack 미완료|','|7 통합·독립·작가승인|최종게이트 미완료|',''])

def self_test():
    o=build();tests=[]
    for name,fn in [('recommendation_selected',lambda x:x['summary'].update(selected_contract='E2')),('E3_as_designated_extension',lambda x:x['alternatives'][2].update(mechanism='DESIGNATED_ROOKIE_EXTENSION')),('E4_QO_as_acceptance_fact',lambda x:x['certification'].update(actual_team_player_consent=True)),('exact2018pick_chosen',lambda x:x['policy'].update(exact2018pick=22)),('whole2022cost_pass',lambda x:x['summary'].update(whole2022_23_cost_or_matching_PASS=True))]:
        bad=copy.deepcopy(o);fn(bad);assert validate(bad),name;tests.append(name)
    for name,fn,what in [('E1_after_deadline',lambda x:x.update(E1_candidate_execution_ET='2021-10-18T18:00:01'),'policy'),('RFA_before_window',lambda x:x.update(E2_E3_candidate_execution_ET='2022-07-06T12:00:00'),'policy'),('old_bonus_erased',lambda x:x.update(E1_original_bonus='ORIGINAL_BONUS_ZERO_FACT'),'terms'),('new_bonus_without_budget',lambda x:x['E1_E2_E3'].update(unlikely_performance_bonus=100000),'terms')]:
        b=policy() if what=='policy' else terms();fn(b)
        with patch(__name__+'.'+what,return_value=b):
            try:build()
            except AssertionError:tests.append(name)
            else:raise AssertionError('Accepted '+name)
    b=source_options();b[1]['salary'][0]+=1;b[1]['salary'][1]-=1
    with patch(__name__+'.source_options',return_value=b):
        try:build()
        except AssertionError:tests.append('same_total_original_E2_schedule_mutation')
        else:raise AssertionError('Accepted original schedule meaning mutation')
    for index,structure in [(2,'2021 designated rookie extension, 30 percent'),(3,'2022 full Bird five-year guaranteed contract')]:
        b=source_options();b[index]['structure']=structure
        with patch(__name__+'.source_options',return_value=b):
            try:build()
            except AssertionError:tests.append('original_'+b[index]['id']+'_mechanism_reversal')
            else:raise AssertionError('Accepted original contract mechanism mutation')
    return tests

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();o=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(render(o),encoding='utf8')
    if a.check:assert not validate(load(OUT));assert text(MD)==render(o),'Markdown stale'
    tests=self_test() if a.self_test else []
    print(json.dumps({'current':True,'summary':o['summary'],'negative_controls':tests},ensure_ascii=False))
if __name__=='__main__':main()
