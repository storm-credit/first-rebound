"""A10 single-team contract capacity, lawful renewal candidates, typed FY24 cost."""
from __future__ import annotations
import argparse,copy,hashlib,json
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import fitz
import build_chicago_2023_24_existing_contract_window as prior

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2024_25_a10_named_role_window_cost_family.py'
OUT='research/CHICAGO_2024_25_A10_NAMED_ROLE_WINDOW_COST_FAMILY_2026_10_08.json'
CORE='simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json'
A='research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json'
ROUTINE='simulation/CHICAGO_2023_SELECTED_ROUTINE_EXECUTION.json'
COST='simulation/CHICAGO_2023_ROUTINE_COST_DOMAIN.json'
LM='simulation/LAMELO_2023_SELECTED_EXTENSION.json'
J='simulation/CHICAGO_2023_SELECTED_ROOKIE_EXECUTION.json'
CP2='design/CP2_ACT_SUBACT_PACKET.json'
PINS={CORE:'e7d0f4b15bc06c7cd16a38d158b38a78871fb7372d412639e33bb20c31d225a7',
A:'7244beff7a120c5ca246a04e72b61586f3cfbe245487d5fc6479f5245fd78d9f',
ROUTINE:'9a4f6db21d6ad50e2c6d6897f1c2dedbdf440cee89bae47019f4bd131f341790',
COST:'13448f381896ee9da4da16e9716b98f7bb511ecd42b527dcba26802a64ba1f8d',
LM:'98f03115f8a71a7f2e0ac3f9376aae5f94647d62c8ce6d942b63881af629483d',
J:'61979a4edc201e314cf7e523393fbe3131f8d3eec547b530ede260729a791511',
'reviews/CHI_2023_SELECTED_ROOKIE_EXECUTION_G11_INDEPENDENT_REVIEW_2026_10_08.json':'2cec63e86be97c86429667a1907312c59833e6d374b5cfc4617491abe337ee6c',
'reviews/LAMELO_2023_SELECTED_EXTENSION_G11_INDEPENDENT_REVIEW_2026_10_08.json':'abea927ebaac99d389a07d128b47d016adb0a387cc709e23a5e58b21597627d3',
'reviews/CHICAGO_2023_ROUTINE_COST_DOMAIN_G11_INDEPENDENT_REVIEW_2026_10_08.json':'a05b70a2234dd9efd4f3243f2f6a0e03cc7402f91ec477b12b3864ff626a3fb7',
CP2:'2b291bca588302cbb254fc3417652f7d7532c46d7094221cdcceac60619c9db9'}
LAW=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-2023-cba-boundary-20261007/cba2023.pdf')
LAW_SHA='bf178ca0f2d64f9dfe6fde095d3ae43d576b12e19ce7a679618d632584f7ab32'
PAGES=[31,32,57,58,210,211,214,215,241,242,244,245,249,251,263,264,272,314,316,317,344]
CAP_URL='https://pr.nba.com/2024-25-nba-season-salary-cap/'
CAP={'cap':140588000,'tax':170814000,'first_apron':178132000,'second_apron':188931000,'minimum_team_salary':126529000}
FIXED={'Lauri Markkanen':21080000,'Alex Caruso':9890000,'Wendell Carter Jr.':11950000,
       'Protagonist':25520000,'Zach LaVine':43031940,'Coby White':12000000,'Chris Duarte':6133005,'Walker Kessler':3510480}
RENEW={'Thaddeus Young':10,'Javonte Green':5,'Joe Wieskamp':3,'Denzel Valentine':8,'Tomas Satoransky':8}
CORE5=['Protagonist','LaMelo Ball','Zach LaVine','Lauri Markkanen','Wendell Carter Jr.']
ENDPOINTS={'Lauri Markkanen':2024,'Alex Caruso':2024,'Wendell Carter Jr.':2025,'Protagonist':2025,'Zach LaVine':2025,'Coby White':2025,'Chris Duarte':2024,'Walker Kessler':2024,'LaMelo Ball':2028,'Jaime Jaquez Jr.':2024}

def norm(t):return t.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(norm((ROOT/p).read_text(encoding='utf-8-sig')).encode()).hexdigest()
def serial(o):return json.dumps(o,ensure_ascii=False,indent=2)+'\n'
def physical():
    for p,h in PINS.items():assert sha(p)==h,'Pinned source changed: '+p
    return {p:json.loads((ROOT/p).read_text(encoding='utf-8-sig')) for p in PINS}
def source_inputs():return physical()
def assert_sources(s):
    assert s==physical(),'Returned source differs from physical contract family'
    t=s[CORE]['contract_terms']
    assert t['Protagonist']['source_terms']['salary_2022_onward']==[22000000,23760000,25520000,27280000]
    assert t['Carter']['source_terms']['extension_regular_salary_schedule']['2024-25']==11950000
    assert t['LaVine']['salary']==[37096500,40064220,43031940,45999660,48967380]
    assert t['Young_Satoransky_source_forms']['Young'][0]['base_schedule']==[8000000,8000000]
    n=s[A]['routine_implementation']['new_contracts']
    assert n['Markkanen']['first_year_regular_salary']==17000000 and n['Markkanen']['annual_raise']==1360000 and n['Markkanen']['years']==4
    assert n['Caruso']['proposed_regular_schedule']==[8600000,9030000,9460000,9890000]
    notices=s[ROUTINE]['selected_FY24_option_notices']
    assert [(x['player'],x['added_salary_capyear'],x['FY24_salary_plus_bonus_upper'],x['fictional_notice_date']) for x in notices]==[('Chris Duarte',2024,6133005,'2023-10-01'),('Walker Kessler',2024,3510480,'2023-10-01')]
    assert s[LM]['selected_terms']['selected_form']=='LM1' and s[LM]['selected_terms']['extended_salary_capyears']==[2024,2025,2026,2027,2028]
    assert s[J]['selected_contract']['player']=='Jaime Jaquez Jr.' and s[J]['post_signature_STD']==15
    assert s[COST]['domains']['R23']['interval']==[0,16371000]
    for p in PINS:
        if p.startswith('reviews/'):assert s[p]['independent_review_completed'] is True

def primary():
    assert hashlib.sha256(LAW.read_bytes()).hexdigest()==LAW_SHA
    d=fitz.open(LAW)
    failed=[('NBA2024cap.raw','2a5e792adc19270f80dc3c302632496dd1ba6af09a53458faeb1772d52658962',425),('NBA2024cba101.pdf','9aead1034955ab91cb82f0038f95119ca9dd1be0cb045747b85a8e09a25acebd',463)]
    attempts=[]
    for name,h,size in failed:
        p=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-a10-fy24-cost-20261008')/name
        assert hashlib.sha256(p.read_bytes()).hexdigest()==h and p.stat().st_size==size
        attempts.append({'cache_path':str(p),'raw_sha256':h,'bytes':size,'HTTP':403,'adopted_body':False})
    return {'CBA_cache':str(LAW),'CBA_raw_sha256':LAW_SHA,'PDF1based_text_LF_sha256':{str(n):hashlib.sha256(norm(d[n-1].get_text()).encode()).hexdigest() for n in PAGES},
       'NBA_cap_release':{'url':CAP_URL,'published':'2024-06-30','observed_with':'web.open actual indexed fullbody lines12..22','provider_HTML_raw_recovered':False,'levels':CAP,'moratorium_end_ET':'2024-07-06T12:00:00','quoted_article_verbatim':False},
       'failed_direct_attempts':attempts,'source_scope':'Lawful contract forms and public levels; no actual private assent, prepared salary cents or health certification'}
def assert_primary(p):
    assert p['CBA_cache']==str(LAW) and p['CBA_raw_sha256']==hashlib.sha256(LAW.read_bytes()).hexdigest()==LAW_SHA
    d=fitz.open(LAW);assert p['PDF1based_text_LF_sha256']=={str(n):hashlib.sha256(norm(d[n-1].get_text()).encode()).hexdigest() for n in PAGES}
    assert p['NBA_cap_release']=={'url':CAP_URL,'published':'2024-06-30','observed_with':'web.open actual indexed fullbody lines12..22','provider_HTML_raw_recovered':False,'levels':CAP,'moratorium_end_ET':'2024-07-06T12:00:00','quoted_article_verbatim':False}
    assert p['source_scope']=='Lawful contract forms and public levels; no actual private assent, prepared salary cents or health certification'
    assert all(x['HTTP']==403 and x['adopted_body'] is False and hashlib.sha256(Path(x['cache_path']).read_bytes()).hexdigest()==x['raw_sha256'] for x in p['failed_direct_attempts'])

def live_rows():
    rows=[{'player':n,'holder':'CHI','STD':1,'TW':0,'salary_capyear':2024,'annual_component_upper':v,'source_cents_are_actual_private':False,'original_Gamma_and_protection_preserved':True,'new_assignment':False} for n,v in FIXED.items()]
    rows += [{'player':'LaMelo Ball','holder':'CHI','STD':1,'TW':0,'salary_capyear':2024,'annual_component_upper':'C24/4 or3*C24/10 onlylawfulHigherMax','C24':140588000,'first_extension_year':True,'source_cents_are_actual_private':False,'original_Gamma_and_protection_preserved':True,'new_assignment':False},
             {'player':'Jaime Jaquez Jr.','holder':'CHI','STD':1,'TW':0,'salary_capyear':2024,'annual_component_upper':'6/5*S23(16,2)','rookie_signing_scale_year':2023,'minimum':'M_2023_signing_scale(serviceYOS1,Year2)','source_cents_are_actual_private':False,'original_Gamma_and_protection_preserved':True,'new_assignment':False}]
    for r in rows:
        r.update(FY24_covered_fiscal_window='2024-07-01..2025-06-30',last_currently_guaranteed_or_exercised_salary_capyear=ENDPOINTS[r['player']],
          fiscal_end_is_exact_service_term=False,service_window_condition='Preserved operative UPC/service family with no selected assignment/termination; actual future rendering not certified',
          future_option_exercise_selected=False)
    return rows
def assert_live(rows,s):
    assert len(rows)==10 and len({r['player'] for r in rows})==10
    assert {r['player']:r['annual_component_upper'] for r in rows[:8]}==FIXED
    for r in rows:assert r['holder']=='CHI' and r['STD']==1 and r['TW']==0 and r['salary_capyear']==2024 and r['original_Gamma_and_protection_preserved'] and not r['new_assignment'] and not r['source_cents_are_actual_private']
    assert rows[8]['player']=='LaMelo Ball' and rows[8]['C24']==140588000 and rows[8]['annual_component_upper']=='C24/4 or3*C24/10 onlylawfulHigherMax' and rows[8]['first_extension_year']
    assert rows[9]['player']=='Jaime Jaquez Jr.' and rows[9]['annual_component_upper']=='6/5*S23(16,2)' and rows[9]['rookie_signing_scale_year']==2023 and rows[9]['minimum']=='M_2023_signing_scale(serviceYOS1,Year2)'
    for r in rows:
        assert r['FY24_covered_fiscal_window']=='2024-07-01..2025-06-30' and r['last_currently_guaranteed_or_exercised_salary_capyear']==ENDPOINTS[r['player']]
        assert r['fiscal_end_is_exact_service_term'] is False and r['future_option_exercise_selected'] is False
        assert r['service_window_condition']=='Preserved operative UPC/service family with no selected assignment/termination; actual future rendering not certified'

def renewals():
    return [{'player':n,'holder':'CHI','expired_salary_capyear':2023,'last_fiscal_end':'2024-06-30','expiry_is_service_completion_family_not_real_receipt':True,
      'candidate_date':'2024-07-07','mechanism':'VII6i_ONE_SEASON_MINIMUM_EXCEPTION','minimum_scale_YOS_bucket':y,'credited_service_condition':'>=10' if n=='Thaddeus Young' else 'Preserved FY23 renderedservice family advances prior creditedYOS byone; noactualclinicalservice certificate','salary':'M24('+str(min(y,10))+',Year1)','YOS10_plus_uses10_scale':y>=10,
      'STD_added':1,'TW_added':0,'years':1,'all_bonuses':0,'protection':'FULL_SKILL_INJURY','options':[],
      'same_claim_FA_hold_replaced_once':True,'old_Gamma_and_accrued_obligations_preserved':True,'fictional_consent_if_candidate_adopted':True,'adopted_new_contract':False,'actual_assent_or_receipt':None,
      'no_same_regular_season_highsalary_waiver_buyout':True} for n,y in RENEW.items()]
def assert_renewals(rows,s):
    assert len(rows)==5 and {r['player']:r['minimum_scale_YOS_bucket'] for r in rows}==RENEW
    old={r['player']:r for r in s[ROUTINE]['named_contracts_and_rights']}
    for r in rows:
        n=r['player'];y=RENEW[n]
        assert r['holder']=='CHI' and r['expired_salary_capyear']==2023 and r['last_fiscal_end']=='2024-06-30' and r['expiry_is_service_completion_family_not_real_receipt']
        assert r['candidate_date']=='2024-07-07' and r['mechanism']=='VII6i_ONE_SEASON_MINIMUM_EXCEPTION' and r['years']==1 and r['salary']=='M24('+str(min(y,10))+',Year1)'
        assert r['STD_added']==1 and r['TW_added']==0 and r['all_bonuses']==0 and r['options']==[] and r['protection']=='FULL_SKILL_INJURY'
        assert r['same_claim_FA_hold_replaced_once'] and r['old_Gamma_and_accrued_obligations_preserved'] and r['no_same_regular_season_highsalary_waiver_buyout']
        assert not r['adopted_new_contract'] and r['actual_assent_or_receipt'] is None and r['fictional_consent_if_candidate_adopted']
        assert r['credited_service_condition']==('>=10' if n=='Thaddeus Young' else 'Preserved FY23 renderedservice family advances prior creditedYOS byone; noactualclinicalservice certificate')
        if n!='Thaddeus Young':assert old[n]['term_years']==1 and old[n]['credited_YOS_family']+1==y

def cost_forms():
    return {'fixed_eight_component_upper':133115425,'LM_ordinary':35147000,'LM_lawful_HigherMax':42176400,
      'Jaquez_Year2':'6/5*S23(16,2)','five_minimum_fullcash_outer':'M24(10)+M24(5)+M24(3)+2*M24(8)',
      'R24_interval':[0,16371000],'R24_frame':'Preserve original valid stretch allocation inside admitted public inventory; ordinary13 salary endpoints alreadyexpired; no newFY24settlement/resolution/stretch selected; not all private absence proof',
      'before_renewal_normal_FA_outer':'Young max150/190%*8m<=15.2m subjectmax/min; four expiredminimum FAholds countednonreimbursedcurrentminimum<=fullM24; Dotson/Cook completedTW FAhold M24(0) each untilvalidrenounce',
      'before_renewal_apron_FA':'UFAholds excluded; old QO expiredOct2_2023 doesnotdeleteFA/ROFR; no newQO/MaximumQO/OfferSheet/FRN selected in candidateframe',
      'candidate_rights_cleanup':'July7 validwrittenVII4g renounce DevonDotson/TylerCook FArights; Bradley priorvalidrenounce preserved; oldprotectedSalary/Γ noterased; actualreceiptfalse',
      'annual_exceptions':'FY24 fresh annualeligibility/nominal amounts notFY21NTMLE rollover; candidateJuly7 validVII6n2 unusedexceptionrenounce; noexceptionused beyond minimum/oldRSC/oldBird',
      'after_renewal_normal_apron_outer':'133115425+LM24+6/5*S23(16,2)+M24(10)+M24(5)+M24(3)+2*M24(8)+R24+D24_N_or_A',
      'D24_N_or_A':'Nonnegative typedcurrent2024unsigneddraft/RT claim port if existingownedrights; unknownnot0, no2024newUPC orrosterslot chosen',
      'new_hardcap_trigger':False,'over_apron_is_automatic_illegality':False,
      'tax':'Actual Tax has finalregular audit/adjustments; fullplayercashplusR24 is conservative componentouter, FA/RT notcash',
      'cash':'NewcandidatefivepositiveM24 cash; expired8m/oldminimum notnewFY24Salary but oldpaymentobligations preserved in correct year/frame',
      'exact_FY24_whole_actual_ledger':False}
def assert_cost(c,s):
    # Check the returned hold/cash layer against the pinned operative claims;
    # expiry ends future service Salary, not FA rights or accrued payment.
    old={r['player']:r for r in s[ROUTINE]['named_contracts_and_rights']}
    assert old['Thaddeus Young']['FY23_normal_upper']==8000000
    assert s[CORE]['contract_terms']['Young_Satoransky_source_forms']['Young'][0]['base_schedule']==[8000000,8000000]
    for name in ['Javonte Green','Joe Wieskamp','Denzel Valentine','Tomas Satoransky']:
        assert old[name]['operation']=='SELECTED_FICTIONAL_NEW_ONE_SEASON_MINIMUM_UPC' and old[name]['term_years']==1 and old[name]['same_claim_FA_QO_replaced_once']
    for name in ['Devon Dotson','Tyler Cook']:
        assert old[name]['operation']=='VALID_UNACCEPTED_STANDARD_QO_RIGHTS_AND_HOLD_RETAINED' and old[name]['ROFR_preserved'] and old[name]['QO_withdrawal_or_FA_renunciation_selected'] is False
    assert c['before_renewal_normal_FA_outer']=='Young max150/190%*8m<=15.2m subjectmax/min; four expiredminimum FAholds countednonreimbursedcurrentminimum<=fullM24; Dotson/Cook completedTW FAhold M24(0) each untilvalidrenounce', 'Expiry does not erase source-backed FA amounts before lawful renewal or renunciation'
    assert c['before_renewal_apron_FA']=='UFAholds excluded; old QO expiredOct2_2023 doesnotdeleteFA/ROFR; no newQO/MaximumQO/OfferSheet/FRN selected in candidateframe', 'Apron exclusions do not erase preserved rights'
    assert c['cash']=='NewcandidatefivepositiveM24 cash; expired8m/oldminimum notnewFY24Salary but oldpaymentobligations preserved in correct year/frame', 'Cash obligations and current-year Salary must remain distinct'
    assert c['fixed_eight_component_upper']==sum(FIXED.values())==133115425 and c['LM_ordinary']==CAP['cap']//4==35147000 and c['LM_lawful_HigherMax']==CAP['cap']*3//10==42176400
    assert c['Jaquez_Year2']=='6/5*S23(16,2)' and c['five_minimum_fullcash_outer']=='M24(10)+M24(5)+M24(3)+2*M24(8)'
    assert c['R24_interval']==s[COST]['domains']['R23']['interval']==[0,16371000]
    assert c['R24_frame']=='Preserve original valid stretch allocation inside admitted public inventory; ordinary13 salary endpoints alreadyexpired; no newFY24settlement/resolution/stretch selected; not all private absence proof'
    assert c['after_renewal_normal_apron_outer']=='133115425+LM24+6/5*S23(16,2)+M24(10)+M24(5)+M24(3)+2*M24(8)+R24+D24_N_or_A'
    assert c['new_hardcap_trigger'] is False and c['over_apron_is_automatic_illegality'] is False and c['exact_FY24_whole_actual_ledger'] is False
    assert c['tax']=='Actual Tax has finalregular audit/adjustments; fullplayercashplusR24 is conservative componentouter, FA/RT notcash'
    assert c['candidate_rights_cleanup']=='July7 validwrittenVII4g renounce DevonDotson/TylerCook FArights; Bradley priorvalidrenounce preserved; oldprotectedSalary/Γ noterased; actualreceiptfalse'
    assert c['annual_exceptions']=='FY24 fresh annualeligibility/nominal amounts notFY21NTMLE rollover; candidateJuly7 validVII6n2 unusedexceptionrenounce; noexceptionused beyond minimum/oldRSC/oldBird'
    assert c['D24_N_or_A']=='Nonnegative typedcurrent2024unsigneddraft/RT claim port if existingownedrights; unknownnot0, no2024newUPC orrosterslot chosen'

def evaluate(S23_year2,M24,R24,D24_N,D24_A,HigherMax=False,legally_qualified=False):
    ss=Fraction(S23_year2);m={int(k):Fraction(v) for k,v in M24.items()}
    assert set(m)=={0,2,3,5,8,10} and all(x>0 for x in m.values()) and [m[k] for k in sorted(m)]==sorted(m.values())
    assert ss>0 and 0<=Fraction(R24)<=16371000 and min(Fraction(D24_N),Fraction(D24_A))>=0
    assert not HigherMax or legally_qualified,'HigherMax requires applicableII7 legalpredicate; noawardoutcome selected'
    lm=Fraction(CAP['cap'])*(Fraction(3,10) if HigherMax else Fraction(1,4));q=sum(m[y] for y in [10,5,3,8,8])
    base=Fraction(133115425)+lm+ss*Fraction(6,5)+q+Fraction(R24)
    return {'normal_fullcash_component_outer':str(base+Fraction(D24_N)),'apron_fullcash_component_outer':str(base+Fraction(D24_A)),
      'minimum_cash_newfive':str(q),'Tax_actual_total_certified':False,'legal_parameter_condition':'Lawfullypreparedsigning2023Year2rookiescale andsigning2024minimum/services, not arbitrarypositive numbers',
      'roster_STD':15,'TW_UPC':0,'new_hardcap_trigger':False}

def build():
    s=source_inputs();assert_sources(s);p=primary();assert_primary(p);l=live_rows();assert_live(l,s);r=renewals();assert_renewals(r,s);c=cost_forms();assert_cost(c,s)
    names=[x['player'] for x in l+r];assert len(set(names))==15 and set(CORE5)<=set(names)
    return {'id':'CHICAGO_2024_25_A10_NAMED_ROLE_WINDOW_COST_FAMILY','status':'REVIEW_PENDING_LIVE10_PLUS_FIVE_CONSENSUAL_MINIMUM_CANDIDATE',
      'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'BOMstrip_CRLF_CR_to_LF_EXTERNAL_RAW_separate','primary':p,'live10':l,'expiry_and_renewal_candidates5':r,'cost_family':c,
      'window':{'capyear':'2024-07-01..2025-06-30','candidate_agreements_after_moratorium':'2024-07-07','specific_regular_game_date':None,'source_contracts_stay_operative_at_role_window':True,'court_core5':CORE5,'conditional_STD':15,'TW_UPC':0,'active12_to15_future_nomination':True,'available8_before_tip_condition':True,'ordered_minutes_active_health_or_actual_registration_selected':False},
      'finite_remainder':{'A10_coach_sample':'Root next: lawfulnomination/availability andcoachcall newboundedobservation, notsource fromold40seconds','five_newcontracts_and_cleanup':'Routine candidateforms awaitdelegatedadoption; nohumanreapprovalgate','FY24_prepared_price_service':'M24 andS23Year2 positivelegalfunctions; noexactprivatecentsgate','2024draft_claim':'D24N/A positivewhenapplicable; newrookiesnotgiven16thslot','future_major_choices':'MVP/title/coremove/2026extension unselected'},
      'certification':{'named_core_contract_support_family_complete':True,'conditional_15STD_plus_typed_cost_constructible':True,'new_five_renewals_or_cleanup_adopted':False,'independent_review_completed':False,'all30team_or_whole_actual_FY24_cost':False,'A10_performance_or_function_completed':False,'clinical_or_assent_receipts':False,'whole_macro3_or_career':False,'REGISTER_promotion':False,'manuscript':False},'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0}
def validate(o):
    try:
        assert o==build(),'Saved family differs from physical reconstruction'
        return []
    except (AssertionError,KeyError,ValueError,TypeError) as e:return [str(e)]
def md(o):
    rows='\n'.join('|'+r['player']+'|'+str(r['annual_component_upper'])+'|기존 live UPC·선택통지|' for r in o['live10'])
    return '\n'.join(['# A10 2024–25 명명 계약·역할 창 비용 가족','',o['status'],'',
      '새 역할이나 결과를 선택하지 않고 **기존 live10+same-owner 최소계약 후보5**로 A10 코어 다섯 명의 법적 기반을 구성했다. 만료는 자동갱신·원채무삭제가 아니다. 새 합의/서면 renounce는 루틴 가상 후보이고 실제 영수증을 완료 필수조건으로 삼지 않는다.','',
      '## 이월10','', '| 선수 | FY24 성분 상단/법정 함수 | 근거 |','|---|---|---|',rows,'',
      'P E2 Year3 25.52m, CX1 Year3 11.95m, M1 Year4 21.08m, Caruso Year4 9.89m·Coby12m을 보존한다. LaVine FY24 43.03194m은 live Year3이며2026 PO·원새tradeΓ를 실행하지 않는다. Duarte4/Kessler3은 기존2023Oct1 선택통지의 FY24 성분상단으로 새옵션행사가 아니다. LM1의 첫 연장급여는C24의25%, 법정HigherMax를 충족할 때만30%다. 실제 수상/MVP년도는 미선택이다. Jaquez는 **서명연도2023의Year2** 120%이며2024 새RSC가격을 이식하지 않는다.','',
      '## 만료5·권리·슬롯','',
      'Young의2022 8m×2 계약과2023 one-year minimum Green/Wieskamp/Valentine/Satoransky는 FY23로 끝난다. 동명 기존보호지급은 보존한다. 후보2024July7에 각1년 full skill/injury, bonus0, option0 minimum exception 합의를 제안한다. Young은10+ 최소표행, 나머지는 보존된FY23 서비스가 한 해 증가한5/3/8/8의 조건부 가족을 법정M24로 가격화한다. 실제미래출전·임상사실로 인증하지 않는다. Young이 UFA가 된 직후 normal의 Birdhold150/190%×8m는 최대15.2m까지 보존하며 법정max/min 조정을 함께 적용한다. 네 expiredminimum의FAhold는 VII4d4의 비환급 현재minimum이고 fullcashM24는 보수예약이다. Apron UFAhold 제외는 원지급소멸과 다르다.','',
      '완료된 Dotson/Cook TW의미수락QO기간 종료는 권리·FAhold 자동삭제가 아니다. 2024 후보 서면renounce를 별도 법적사건으로 선언하면 해당hold만 제외되며 oldGamma/보호채무는 남는다. Bradley 기존renounce도 원지급삭제로 읽지 않는다. live10+candidate5=15STD/TW0; 2024 신인계약을16번째로 추가하지 않는다. 필요 unsigned2024 draft/RT 비용 D24_N/A는 typed nonnegative 포트로 남기며 unknown을0으로 완결하지 않는다.','',
      '## 법적 비용·가격','',
      '8명 고정 성분합 **133,115,425**. LM ordinary **35,147,000**, qualified HigherMax **42,176,400**. 이후 같은 normal/apron 보수 성분상단은 `133115425+LM24+1.2*S23(16,2)+M24(10)+M24(5)+M24(3)+2*M24(8)+R24+D24_N_or_A`. R24[0,16.371m]는 원유효stretch의 잔여연도 publicfamily와 ordinary13 말단을 그대로 전진 투영한 상단이며 새settlement/회계사실을 창작하지 않는다. 이전의13ordinary 증명이 모든stretch0이라는 뜻은 아니다.','',
      '새minimum은 cap/apron 초과팀도 VII6i로 허용되는 양수 법정급여이며 bonus금지·최대2년 중1년이다. oldBird/liveRSC/extension/선택option 이월과 이러한minimum만으로 VII2e A–K 새hardcaptrigger는 없다. FY21 NTMLE hardcap을 FY24로 이월하지 않고 FY24 새annualexception을 명명한다. 미사용예외의normalcharge는 후보 유효renounce 후 제외되며 apron VII2e1viii와 별도다. 높은apron 상단은 자동위법이 아니다. Tax는 finalregular audit 정의, actualcash는 지급의무 정의로 각각 보존한다.','',
      '[공식NBA2024 발표](https://pr.nba.com/2024-25-nba-season-salary-cap/) indexed실본문으로 cap140.588m/tax170.814m/first178.132m/second188.931m/minteam126.529m과July6 noon moratorium 종료를 확인했다. 직접PR와CBA101 회수는 각각403이며 adopted원HTML/PDF0; 실패파일을 표로 오인하지 않는다. 2023 CBA II6/VII2e/4d·g/6i·n2/VIII1/XI4를 raw·21page지문으로 직접 읽었다. 준비표 M24/S23의 정확발행값·센트는 아직 인증하지 않지만 법정함수에 따른 합법 계약가족은 구성할 수 있다.','',
      '## A10 인계','',
      'P/LaMelo/LaVine/Mark/Carter가 함께 있는 한정 경기창을 받을 수 있다. 실제가용5/available8·active12–15·감독호출·정수240분은 다음 별도consumer 입력이며 이번leaf의 계약존속과 혼동하지 않는다. 날짜/대진 null이 계약가족 전체를 영구HOLD시키지 않는다. 새성공/클로징 권한승계/수상·우승·2026연장은 선택하지 않는다.','',prior.progress()])+'\n'
def self_test():
    done=[]
    cases=[('LM_current_salary_zero','live_rows',lambda x:x[8].update(annual_component_upper=0)),('Jaquez_wrong_signing_scale','live_rows',lambda x:x[9].update(rookie_signing_scale_year=2024)),('minimum_extra_bonus','renewals',lambda x:x[0].update(all_bonuses=100000)),('new_min_UPC_count_zero','renewals',lambda x:x[0].update(STD_added=0)),('erase_legacy','cost_forms',lambda x:x.update(R24_interval=[0,0])),('Bird_apron_auto_illegal','cost_forms',lambda x:x.update(over_apron_is_automatic_illegality=True)),('false_actual_scope','primary',lambda x:x.update(source_scope='All private cents and actual clinical clearance certified')),('expiry_erases_FA_claims','cost_forms',lambda x:x.update(before_renewal_normal_FA_outer='0: automatically expired FA claims disappear'))]
    for label,helper,mutate in cases:
        z=globals()[helper]();mutate(z)
        try:
            with patch(__name__+'.'+helper,return_value=z):build()
        except AssertionError:done.append(label)
        else:raise AssertionError('FALSE PASS '+label)
    return done
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();o=build()
    if a.write:(ROOT/OUT).write_text(serial(o),encoding='utf8',newline='\n');(ROOT/OUT.replace('.json','.md')).write_text(md(o),encoding='utf8',newline='\n')
    err=validate(json.loads((ROOT/OUT).read_text(encoding='utf-8-sig'))) if a.check else []
    if a.check and norm((ROOT/OUT.replace('.json','.md')).read_text(encoding='utf-8-sig'))!=md(o):err.append('Markdown stale')
    controls=self_test() if a.self_test else []
    print(json.dumps({'current':not err,'errors':err,'live':10,'candidate_renewals':5,'conditional_STD':15,'TW':0,'writer_controls':controls},ensure_ascii=False))
    if err:raise SystemExit(1)
if __name__=='__main__':main()
