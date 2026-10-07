"""Join selected FY22 contracts to their finite fiscal/rights window, without a new draft.

The parent owns canon/REGISTER. This leaf does not select a new UPC, medical
state, 2022-23 result, future QO, extension, or draft identity.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_chicago_2022_23_named_contract_window.py'
OUT = 'simulation/CHICAGO_2022_23_NAMED_CONTRACT_WINDOW.json'
MD = OUT.replace('.json', '.md')
BASELINE = 'bebabcf65be6af0d73d39b5a290249de52952397'
PINS = {
 'simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json': 'e7d0f4b15bc06c7cd16a38d158b38a78871fb7372d412639e33bb20c31d225a7',
 'research/CHICAGO_2022_JULY7_NAMED_ROSTER_CONTRACT_COST_JOIN_2026_10_07.json': '9f3e19c38f7be2a7259158cf4ba8f7440aca400593092d400cac23fa2917074a',
 'reviews/CHICAGO_2022_CORE_SELECTION_INDEPENDENT_REVIEW_2026_10_07.json': 'd10b8cceda48fb0f24393697aafefa34538e9656845a9eb02ff164025d466c2f',
 'research/CHICAGO_2022_UNSIGNED_DRAFT_EXECUTION_FAMILY_2026_10_07.json': '7c2ea95557f96a9156709aabb8574fcaea8993831aed5f2f6cc626be6829bafd',
 'simulation/NBA_2022_PUBLIC_CONTROL_EXECUTION_FAMILY.json': '86ac9e85b06a607363f5c7a6bd6fac29a8a5dbd89fff803e2a440897afd3337c',
 'simulation/CHICAGO_2022_ROOKIE_OPTION_WINDOW_JOIN.json': 'e506efd28a54ceb61e34a8dfc107fb82236f783700f3aa610cd68ff4d62ba2cc',
 'research/SIMONOVIC_2022_23_SELECTED_RIGHTS_FAMILY_2026_10_07.json': 'c404fc401f6c30809ed5098663dd2b277b1c4cb7844d15c697991460f1290ac4',
 'research/COBY_2023_ORDINARY_QO_FUNCTION_2026_10_07.json': '5ee4c26f87c4e63b6cc812aff14382f2d1b522242707b5f65064b357f0522c54',
 'research/MACRO3_2023_CBA_BOUNDARY_BRIDGE_2026_10_07.json': '404fde08b9d5fc9168b64f082c57a4ed6dff14711cf4d5990839267dc8a878f4',
 'research/CHICAGO_2022_LEGACY_CARRY_REFINEMENT_2026_10_07.json': 'ec95c68e5f4fb0ae6a799f2c74705c5c733945719c740b0349bf128be6832c81',
 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json': '9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce',
}
CORE, JOIN, REVIEW, DRAFT, CONTROL, OPTIONS, MARKO, COBY, NEWLAW, LEGACY, AUTHOR = PINS
CBA = Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA_SHA = '66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
PAGES = [30, 32, 36, 37, 54, 55, 74, 75, 207, 208, 209, 210, 211, 216, 217, 239, 240, 241, 292, 293, 303, 304, 305, 306, 307, 310, 311, 314, 315, 412, 413, 513]
NAMES = ['Lauri Markkanen','Alex Caruso','LaMelo Ball','Coby White','Chris Duarte','Javonte Green','Joe Wieskamp','Tony Bradley','Stanley Johnson','Denzel Valentine','Wendell Carter Jr.','Protagonist','Zach LaVine','Thaddeus Young','Tomas Satoransky','Devon Dotson','Tyler Cook']
AMOUNTS = [18360000,9030000,7775400,7413955,4591680,1815687,1563529,2036328,2351532,2193930,14150000,22000000,37096500,8000000,3000000,0,0]
# Covered fiscal seasons, not a claim that UPC Paragraph1 says June30 termination.
LAST_SELECTED_CAPYEAR = [2024,2024,2023,2022,2023,2022,2022,2022,2022,2022,2025,2025,2026,2023,2022,2022,2022]

def norm(s):
    return s.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')

def sha(path):
    return hashlib.sha256(norm((ROOT/path).read_text(encoding='utf-8-sig')).encode()).hexdigest()

def physical():
    for p,h in PINS.items():
        if sha(p) != h: raise AssertionError('Pinned source changed: '+p)
    return {p:json.loads((ROOT/p).read_text(encoding='utf-8-sig')) for p in PINS}

def inputs():
    return physical()

def assert_inputs(s):
    # Source meaning remains checked even when a caller substitutes its loader.
    if s != physical(): raise AssertionError('Source objects differ from pinned physical inputs')
    c=s[CORE]
    assert c['selected_policy']=={'Carter':'CX1','Protagonist':'E2','LaVine':'EXISTING_DIRECT_BIRD5YEAR_FORM','Young':'Y_BIRD_8M','Satoransky':'S_MINIMUM'}
    rows=[r['source_row'] for r in c['selected_contracts']]
    assert [r['player'] for r in rows]==NAMES
    assert [r['normal_upper'] for r in rows]==AMOUNTS
    assert [r['apron_upper'] for r in rows]==AMOUNTS
    assert [r['roster_type'] for r in rows]==['STANDARD']*15+['TWO_WAY']*2
    assert s[OPTIONS]['join']['dated_notice_timeliness_join_closed'] is True
    assert s[MARKO]['selected_policy']['prior_or_pending_5a_ii_notice_exists_in_selected_model'] is False
    assert s[MARKO]['period_witness']['one_year_end_in_selected_fiction']=='2023-08-14'
    assert s[JOIN]['named_TW_prior_bridge']['Devon_Dotson']['total_same_CHI_TW_capyears']==3
    assert s[JOIN]['named_TW_prior_bridge']['Tyler_Cook']['one_year_not_two_year_new_TW'] is True

def primary():
    import fitz
    assert hashlib.sha256(CBA.read_bytes()).hexdigest()==CBA_SHA
    d=fitz.open(CBA)
    texts={n:norm(d[n-1].get_text()) for n in PAGES}
    assert 'immediately upon selection in the Draft' in texts[210]
    assert 'shall include the amount of any' in texts[241]
    assert 'more than three (3) Salary Cap Years' in ' '.join(texts[75].split())
    return {'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(CBA),'raw_sha256':CBA_SHA,
      'PDF1based_normalized_fitz_text_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest() for n,t in texts.items()},
      'source_role':'Reused primary PDF, directly read local pages; no new download or new historical evidence certificate',
      'locators':{'same_signing_year_minimum':'II6 PDF54–55','TW_eligibility_conversion':'II11f/g PDF74–75','capyear_Season_distinct':'I1nnn/ooo PDF32; UPC1 PDF513',
      'immediate_new_draft_hold':'VII4e1 PDF210, printed188','apron_RT_not_unsigned_hold':'VII6m3E/F/G PDF241, printed219','existing_unsigned_rights':'X4/X5/X6 PDF303–307',
      'option_period':'VIII1a PDF292','Coby_statistic_tests':'XI1c PDF310–311','QO_deadline':'XI4 PDF314–315'}}

def contract_rows(s):
    result=[]
    for i,r in enumerate(s[CORE]['selected_contracts']):
        a=copy.deepcopy(r['source_row'])
        a.update({'holder':'CHI','exclusive_current_UPC_claim':True,'source_pointer':CORE+'#/selected_contracts/'+str(i),
          'FY22_covered_capyear':'2022-07-01..2023-06-30','last_selected_salary_capyear_start':LAST_SELECTED_CAPYEAR[i],
          'last_selected_fiscal_year_end':str(LAST_SELECTED_CAPYEAR[i]+1)+'-06-30',
          'service_term_exact_end_not_inferred_from_fiscal_end':True,
          'term_support':CORE+'#/contract_terms' if i>=10 and i<15 else (OPTIONS+'#/preserved_parent_notices' if i in [2,4] else a.get('method_source_pointer')),
          'no_new_assignment_waiver_renegotiation_or_extra_compensation_in_this_continuation':True,
          'actual_medical_or_payment_receipt':None})
        if i in [5,6,7,8,9]:
            a['minimum_rule']='2021 signing-capyear scale, Year2 creditedYOS3/1/5/7/6 respectively; reviewed floor/ceil amount upper, not new2022 UPC scale'
        if i==12:a['future_option']='2026-27 player option retained; exercise outcome null; fiscal terminal2027 conditional on that option'
        if i>=15:
            a['eligibility_bridge']=copy.deepcopy(s[JOIN]['named_TW_prior_bridge']['Devon_Dotson' if i==15 else 'Tyler_Cook'])
            a['term_support']='Selected one-season2022–23 TW form, II11d/f; exact Season service-ending date not inferred as June30'
            a['mandatory_standard_conversion_option_present']=True
            a['conversion_exercised']=False
            a['NBA_playoff_eligible_without_standard_conversion']=False
            a['zero_cap_cost_is_zero_cash']=False
        result.append(a)
    assert_contract_rows(result,s)
    return result

def assert_contract_rows(rows,s):
    expected=[r['source_row'] for r in s[CORE]['selected_contracts']]
    assert len(rows)==17 and [r['player'] for r in rows]==NAMES
    for i,(r,a) in enumerate(zip(rows,expected)):
        for k in ['player','roster_type','mechanism','modeled_acquisition_or_option_date','normal_upper','apron_upper','salary_function']:
            assert r.get(k)==a.get(k), 'Selected contract identity/method/cost changed: '+k
        assert r['holder']=='CHI' and r['last_selected_salary_capyear_start']==LAST_SELECTED_CAPYEAR[i]
        assert r['last_selected_fiscal_year_end']==str(LAST_SELECTED_CAPYEAR[i]+1)+'-06-30', 'Contract fiscal endpoint changed'
        assert r['FY22_covered_capyear']=='2022-07-01..2023-06-30', 'Covered fiscal window changed'
        assert r['service_term_exact_end_not_inferred_from_fiscal_end'] is True, 'Fiscal endpoint became actual service-term certificate'
        expected_term=(CORE+'#/contract_terms' if 10<=i<15 else OPTIONS+'#/preserved_parent_notices' if i in [2,4] else a.get('method_source_pointer'))
        if i>=15:expected_term='Selected one-season2022–23 TW form, II11d/f; exact Season service-ending date not inferred as June30'
        assert r['term_support']==expected_term, 'Term support meaning changed'
        expected_option='2026-27 player option retained; exercise outcome null; fiscal terminal2027 conditional on that option' if i==12 else None
        assert r.get('future_option')==expected_option, 'Future option or exercise boundary changed'
        assert r['actual_medical_or_payment_receipt'] is None
        assert r['no_new_assignment_waiver_renegotiation_or_extra_compensation_in_this_continuation'] is True
        if i>=15:
            b=s[JOIN]['named_TW_prior_bridge']['Devon_Dotson' if i==15 else 'Tyler_Cook']
            assert r['eligibility_bridge']==b and r['conversion_exercised'] is False
            assert r['NBA_playoff_eligible_without_standard_conversion'] is False

def rights(s):
    rows=[copy.deepcopy(r) for r in s[CONTROL]['sixty_origin_control_functions'] if r['current_public_family_holder']=='CHI']
    assert [(r['id'],r['origin'],r['round'],r['rank_domain']) for r in rows]==[('CHI_2022_R1','CHI',1,[17,18]),('LAL_2022_R2','LAL',2,[54,55,56,57])]
    for r in rows:
        r.update({'source_pointer':CONTROL+'#/sixty_origin_control_functions/'+str(s[CONTROL]['sixty_origin_control_functions'].index(r)),
          'template_ref':DRAFT+'#/selected_policy','NBA_UPC_accepted':False,'current_standard_slot_consumption':0,
          'participant':None,'participant_specific_X5_X6_dispatch_required_when_selected':True,
          'acceptance_requires_named_standard_slot_change_before_STD16':True,
          'post_Subsequent_Draft_rights_not_automatically_carried':True})
    return rows

def cost_function(new2023_normal,new2023_apron):
    # Both amounts must be explicit nonnegative inputs. null is never zero.
    if new2023_normal is None or new2023_apron is None: raise AssertionError('New draft charge inputs must be supplied, not null-as-zero')
    assert type(new2023_normal) is int and type(new2023_apron) is int
    assert new2023_normal>=0 and new2023_apron>=0
    return {'normal_upper':170845541+new2023_normal,'apron_upper':172483541+new2023_apron}

def check_acceptance(registered,participant,accepted):
    assert participant not in registered, 'Participant already has a selected UPC'
    if accepted: assert len(registered)+1<=15, 'New standard acceptance needs a named freed slot'
    return len(registered)+(1 if accepted else 0)

def construct(s):
    c=s[CORE]['cost_on_2022_07_07']
    rows=contract_rows(s)
    assert_contract_rows(rows,s) # independent caller guard for substituted producer
    claims=rights(s)
    expected=[r for r in s[CONTROL]['sixty_origin_control_functions'] if r['current_public_family_holder']=='CHI']
    for r,e in zip(claims,expected):
        for k in ['id','year','round','origin','current_public_family_holder','rule','rank_domain']:assert r[k]==e[k]
        assert r['NBA_UPC_accepted'] is False and r['current_standard_slot_consumption']==0
    assert sum(r['normal_upper'] for r in rows)==141378541
    assert c['normal_public_family_upper']==170845541 and c['apron_public_family_upper']==172483541
    return {
      'named_contracts':rows,'current_2022_unsigned_claims':claims,
      'dated_events':[
       {'date':'2022-07-07','action':'REUSE_SELECTED_FOUR_STANDARD_AND_TWO_TW_SIGNINGS_AND_VALID_UNUSED_ANNUAL_EXCEPTION_RENUNCIATION','source':CORE+'#/event_trace','STD':15,'TW':2},
       {'date':'2022-07-08','action':'CONDITIONAL_FIRST_REQUIRED_TENDER','rank_domain':[17,18],'acceptance_through':'2022-10-18','player':None,'NBA_UPC_accepted':False,'source':DRAFT+'#/selected_policy'},
       {'date':'2022-08-14','action':'MARKO_FIRST_EFFECTIVE_X5a_i_NOTICE','selected_period_end':'2023-08-14','new_NBA_UPC':False,'source':MARKO+'#/period_witness'},
       {'date':'2022-08-25','action':'CONDITIONAL_SECOND_TENDER_AND_SELECTED_MARKO_VOLUNTARY_OFFER','acceptance_through':'2022-10-15','new_NBA_UPC':False,'source':[DRAFT+'#/selected_policy',MARKO+'#/selected_policy/2022_offer']},
       {'date':'2022-10-01','action':'REUSE_TWO_TIMELY_ORIGINAL_ROOKIE_OPTIONS_ADDING_2023_24_ONLY','players':['LaMelo Ball','Chris Duarte'],'current_year_cost_change':0,'new_UPC_slots':0,'source':OPTIONS+'#/join'},
       {'date':'2023-06-22','action':'SUBSEQUENT_DRAFT_TRANSITION_AND_NEW_FIRST_HOLD_PORT','date_role':'Preserved SubsequentDraft date in accepted unsigned template; exact new2023 selections not supplied','source':DRAFT+'#/dated_conditional_examples','primary_date_source':DRAFT+'#/sources/calendar/0'},
       {'date':'2023-06-29','action':'COBY_ORDINARY_QO_DEADLINE_UNEXECUTED_FUNCTION','source':COBY+'#/policy','issued':False,'new_current_FY22_UPC':False},
       {'date':'2023-06-30','action':'FY22_FISCAL_BOUNDARY_NOT_AN_ACTUAL_GAME_OR_UPC_RECEIPT_CERTIFICATE','named_standard_without_selected_FY23_salary':['Coby White','Javonte Green','Joe Wieskamp','Tony Bradley','Stanley Johnson','Denzel Valentine','Tomas Satoransky'],'QO_acceptance_or_renewal_selected':False},
       {'date':'2023-07-01','action':'2023_CBA_OPENS_OUTSIDE_FY22','source':NEWLAW+'#/facts'},
       {'date':'2023-07-06T12:01:00_ET','action':'LAMELO_EXTENSION_WINDOW_OPENS_CONDITIONALLY_OUTSIDE_FY22','source':NEWLAW+'#/facts','extension_selected':False}],
      'cost':{
       'live15_normal_and_apron_upper':141378541,'old_stretch_upper':16371000,
       'three_old_unsigned_ports_normal_reservation':13096000,'three_old_unsigned_ports_apron_reservation':14734000,
       'normal_preserved_family_upper_before_new_D23_charge':170845541,'apron_preserved_family_upper_before_new_D23_charge':172483541,
       'old_unsigned_reservations_kept_after_D23_as_conservative_finite_cost_reservations_not_rights_certificates':True,
       'cash_payment_delay_does_not_create_a_new_season_salary':True,'new_original_resolution_events_selected':False,
       'current_assignment_bonus_charge_added':0,'assignment_zero_reason':'No new assignment in this continuation. Existing currentSalary/all-performance upper preserved; clauses/rates are not certified zero.',
       'normal_new_D23_formula':'170845541 + N23, N23=sum(120% applicableScale for newly selected2023 firsts heldCHI), plus any other expressly selected new FY22 obligation not in source family',
       'apron_new_D23_formula':'172483541 + A23, A23=sum(current-capyear outstanding first RequiredTender amounts) + any other expressly selected new FY22 apron obligation',
       'N23':None,'A23':None,'new_D23_total_numeric_upper':None,
       'positive_draft_hold_rule':'2017VII4e1: included immediately upon selection, not deferred automatically to July1',
       'new_hold_is_a_required_standard_slot':False,
       'new_2022_23_NTMLE_BAE_or_receiving_SandT_selected':False,
       '2021_Caruso_NTMLE_hardcap_automatically_carries':False,'negative_apron_screen_is_actual_illegal':False,
       'unused_exception_family':'Selected July7 written renunciation remains effective withinFY22; no new TPE-producing assignment/DPE award selected. NewFY23 annual exceptions are separate.',
       'full_actual_TeamSalary_or_tax_certificate':False},
      'registration_scope':{
       'selected_named_contract_claims':17,'STD':15,'TW':2,'new_rookie_UPC':0,
       'model_window':'FY22 currentUPC fiscal obligations through2023June30 under no new intervening assignment/waiver/conversion. Service/end-of-Season dates distinct.',
       'active_list_or_48minute_game_roster_certified':False,'positive_minutes_or_reserve_health_certified':False,
       'game_dependent_TW50_and_standard_conversion':'If later used: bind season-specific 50NBA-active-games limit and noNBAPlayoffs unless timely standard conversion. No TW game dates chosen here.',
       'global_owner_join':'All17 UPCs remain exclusiveCHI in this continuation; reject participant already in selectedbank. Whole30team FY22 future membership not certified.',
       'named_optional_conversion_or_new_rookie_standard_acceptance_requires_prior_slot_action':True},
      'next_finite_inputs':[
       {'id':'D22_PLAYERS','scope':'Exact2022 participant identities and actor-specific X4/X5/X6 dispatch for CHI17/18 and LAL54–57. Current entitled origins/count already supplied. No historical Terry automatically copied.'},
       {'id':'FY22_GAMES','scope':'2022–23 dated availability, active lists, minutes, explicit starts/OT and results remain unselected; contract preservation does not require real medical receipts.'},
       {'id':'D23_NEW_CHARGES','scope':'June22–30 newly selected2023 draft origins/ranks/rights/tenders -> N23/A23. Do not reuse old170.845541/172.483541 as unchanged wholeTeamSalary after a new first selection.'},
       {'id':'COBY2023_QO','scope':'Two-seasons regular GP/GS/fullcreditedMIN(2021–22 and2022–23), source-component branch, timely QO and FY23 costs. No forced newstats just to retain the two-branch function.'},
       {'id':'LAMELO2023','scope':'Existing fourth-option retained; 2023newCBA window/first-extended-year cap/qualifying honors and consensual form must be chosen separately. No MVP or title selected.'}],
    }

def build():
    s=inputs();assert_inputs(s)
    body=construct(s)
    assert_contract_rows(body['named_contracts'],s)
    assert_working(body,s)
    return {'id':'CHICAGO_2022_23_NAMED_CONTRACT_WINDOW','baseline_main':BASELINE,
      'status':'SOURCE_SUPPORTED_SELECTED_17_CONTRACT_CONTINUATION_REVIEW_PENDING_WITH_EXPLICIT_D23_COST_PORT',
      'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'SHA256_UTF8_BOM_STRIPPED_CRLF_CR_TO_LF_REPOSITORY_FILES; externalPDF rawbytes separately',
      'primary':primary(),'quantifier':'For every admitted preserved currentcontract input within the accepted source cost family, the selected no-new-transaction continuation preserves the named17 obligations throughFY22. Newdraft participants/tenders and postD23 additions remain explicit conditional inputs; no quantified private all-history absence.',
      'working_implementation':body,
      'certification':{'selected_existing_contract_period_and_current_roster_join_complete':True,'whole_D23_numeric_cost_upper_certified':False,'new_important_contract_or_player_selection':False,'actual_private_Gamma_cents_or_consent':None,'actual_medical_or_filing':False,'whole_2022_23_season':False,'whole_macro3':False,'independent_review_completed':False,'REGISTER_promotion':False},
      'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0,'manuscript_allowed':False}

def assert_working(w,s):
    """Consumer checks legal/cost meaning, separately from the constructor."""
    c=w['cost'];a=s[CORE]['cost_on_2022_07_07']
    for dst,src in [('live15_normal_and_apron_upper','live15_normal_upper'),('old_stretch_upper','legacy_original_stretch_upper'),('three_old_unsigned_ports_normal_reservation','named_first_and_two_second_reservations_normal'),('three_old_unsigned_ports_apron_reservation','named_first_and_two_second_reservations_apron'),('normal_preserved_family_upper_before_new_D23_charge','normal_public_family_upper'),('apron_preserved_family_upper_before_new_D23_charge','apron_public_family_upper')]:
        assert c[dst]==a[src], 'Continuation cost differs from the selected public source'
    assert c['N23'] is None and c['A23'] is None and c['new_D23_total_numeric_upper'] is None
    assert c['current_assignment_bonus_charge_added']==0
    for k in ['new_2022_23_NTMLE_BAE_or_receiving_SandT_selected','2021_Caruso_NTMLE_hardcap_automatically_carries','negative_apron_screen_is_actual_illegal','full_actual_TeamSalary_or_tax_certificate','new_original_resolution_events_selected']:
        assert c[k] is False, 'Unselected financial event or authority added: '+k
    assert c['normal_new_D23_formula']=='170845541 + N23, N23=sum(120% applicableScale for newly selected2023 firsts heldCHI), plus any other expressly selected new FY22 obligation not in source family'
    assert c['apron_new_D23_formula']=='172483541 + A23, A23=sum(current-capyear outstanding first RequiredTender amounts) + any other expressly selected new FY22 apron obligation'
    assert [(r['id'],r['origin'],r['rank_domain'],r['NBA_UPC_accepted'],r['current_standard_slot_consumption']) for r in w['current_2022_unsigned_claims']]==[('CHI_2022_R1','CHI',[17,18],False,0),('LAL_2022_R2','LAL',[54,55,56,57],False,0)]
    assert [e['date'] for e in w['dated_events']]==['2022-07-07','2022-07-08','2022-08-14','2022-08-25','2022-10-01','2023-06-22','2023-06-29','2023-06-30','2023-07-01','2023-07-06T12:01:00_ET']
    assert w['dated_events'][4]['current_year_cost_change']==0 and w['dated_events'][4]['new_UPC_slots']==0
    assert w['dated_events'][6]['issued'] is False and w['dated_events'][9]['extension_selected'] is False
    assert w['registration_scope']['STD']==15 and w['registration_scope']['TW']==2 and w['registration_scope']['new_rookie_UPC']==0
    assert w['registration_scope']['active_list_or_48minute_game_roster_certified'] is False
    assert w['registration_scope']['positive_minutes_or_reserve_health_certified'] is False

def validate(x):
    try:
        assert x==build(),'Stored output differs from complete source-bound reconstruction'
        return []
    except (AssertionError,KeyError,ValueError) as e:return [str(e)]

def markdown(x):
    w=x['working_implementation'];lines=['# Chicago 2022–23 명명 계약 기간·권리 연결','',
      '상태: '+x['status'],'',
      '기존 선택 E2/CX1/M1/Caruso·LaVine·Young/Sato·두 TW를 보존한다. 새 중요 가격·신인·시즌 결과를 고르지 않는다. 2020–21 S2 완료는 재검문하지 않았다.','',
      '## 실제 추가한 연결','',
      'July7의 15STD+2TW를 각 계약 수단·서명일·FY22 급여 상단·선택된 후속 시즌에 연결했다. 2022Oct1 LaMelo/Duarte 옵션 통지는 이미 닫힌 8개 날짜창을 재사용하며 FY22 급여나 슬롯을 추가하지 않는다. 계약 서비스 term/Season과 July1–June30 fiscal year는 같다고 인증하지 않는다.','',
      '| 선수 | 형식 | FY22 normal/apron 상단 | 마지막 선택된 급여 capyear |','|---|---|---:|---|']
    for r in w['named_contracts']:lines.append(f"| {r['player']} | {r['roster_type']} | {r['normal_upper']:,} | {r['last_selected_salary_capyear_start']}–{str(r['last_selected_salary_capyear_start']+1)[2:]} |")
    lines += ['', 'Satoransky 3m는 법정 minimum의 보수 상단이며 합의된 정확 연봉이 아니다. 다섯 2021 최소계약의 Year2는 서명 capyear 표를 유지한다. Devon Dotson은 Damyean Dotson과 다른 선수이며 같은 CHI 세 capyear, Cook은 YOS≤3의 한 시즌 TW다. TW 비용 제외는 현금 0이 아니다. 둘의 표준 전환 옵션을 보존하되 실행하지 않아 NBA 플레이오프 사용을 인증하지 않는다.','',
      '## 신인·외국 권리','',
      '현행 공개60권리 함수에서 CHI own1R 순번17/18와 LAL-origin2R 순번54–57을 운반했다. 옛 CHI/DET/LAL 합성 후보에서 실제 원점을 불명으로 되돌리지 않는다. 두 신인 participant는 null이며 새 UPC도 0이다. 이미 15STD이므로 수락·TW전환 전 명명된 자리 조치가 필요하다. 기존 conditional tender의 기한과 X5/X6 적용 조건을 유지한다.','',
      'Marko Simonović는 선택된 no-clock 해외 의무해소·Aug14 최초 통지 가족으로 2023Aug14까지 지원된다. June30 여유45일, NBA UPC0. 실제 과거 notice 부재나 해외 지급액 0을 인증하지 않으며 기존 미선택268개 모든 가족이 통과한 것으로 쓰지 않는다.','',
      '## 비용 경계','',
      'live15 141,378,541 + 기존 stretch 16,371,000 + 기존 세 unsigned 포트 예약 normal13,096,000/apron14,734,000 = **170,845,541 / 172,483,541**. 새 원장 부재를 증명해서 0으로 만든 값이 아니다. 기존 기간 endpoint·새 resolution 사건 미선택의 공개 가족을 다음 날짜로 투영한다. 새 양도 없음은 clause가 없음과 다르다.','',
      '새 2023 1R가 June22 드래프트에서 선택되면 VII4(e)(1)에 따라 normal120%scale hold가 즉시 생긴다(PDF210/인쇄188). July1로 미루지 않는다. Apron은 VII6(m)(3)(E)에 따라 unsigned hold 제외·해당 capyear의 outstanding RT를 산입한다(PDF241/인쇄219). 따라서 이후 전체 숫자는 **170,845,541+N23 / 172,483,541+A23**이며 N23/A23은 null로 남겼다. null을0으로 바꾸거나 June22–30 전체 상단을 기존 고정값으로 인증하지 않는다. 기존 예약을 끝까지 유지하는 것은 권리 존속의 인증이 아니다.','',
      '선택 Bird/minimum 가족은 FY22 새 NTMLE/BAE/수취 S&T 트리거가 없다. 2021 Caruso hardcap을 FY22로 자동 이월하지 않는다. 음수 apron 여유는 이 가족의 실제 위법 판정이 아니다. July7 unused-exception renunciation을 보존하고 새 TPE/DPE 사건을 만들지 않았다.','',
      '## 정확한 다음 입력','']
    lines += ['- **'+r['id']+'**: '+r['scope'] for r in w['next_finite_inputs']]
    lines += ['', 'Coby는 June29 QO 함수가 이미 있으나 발행·수락하지 않았다. LaMelo 2023 extension은 새 CBA July6 12:01 창·실제 first-extended-year cap 및 성과 조건을 별도로 소비한다. 2023의65경기 상을2022–23에 소급하지 않는다. Mitchell/Gobert 원역사 거래를 복사하지 않는다.','',
      '## 검문과 권위','',
      '생산기 --check는 11개 원정본 SHA·자체 지문·실제17 source object·원계약 의미·TW 자격·원점과 비용을 재구성한다. CBA32쪽의 원바이트/쪽 텍스트 지문을 보존했다. 새 독립검문은 pending이며 기존 독립승인은 참고 원천일 뿐 새 승인으로 계수하지 않는다.','',
      '| 큰 묶음 | 상태 |','|---|---|','|1 2020 드래프트|완료 보존|','|2 Chicago2020–21|S2 유한 시즌 완료 보존|','|3 2021–23 계약·거래|기존17 기간 연결; 신인·두번째 시즌·2023 후속 남음|','|4 장기 커리어|선행 시즌 의존|','|5 전체 구조|현행 기능 등록기 참조; 전체 미완료|','|6 규격·Pack|Pack0; 전체 미완료|','|7 통합·독립·승인|진행|','',
      '미완료 큰 묶음5·6번까지4. v0.30 PARTIAL / CLOSED / 원고0. 사적 exactΓ·수락·영수증·의료·전체시즌·REGISTER 승격은 미인증.','']
    return '\n'.join(lines)

def self_test():
    import sys
    m=sys.modules[__name__];s=physical();base=build();n=0
    for mutate in [lambda z:z[CORE]['selected_contracts'][15]['source_row'].update(player='Damyean Dotson'),lambda z:z[CORE]['contract_terms']['Protagonist']['source_terms'].update(mechanism='NEW_NTMLE'),lambda z:z[CONTROL]['sixty_origin_control_functions'].__setitem__(next(i for i,v in enumerate(z[CONTROL]['sixty_origin_control_functions']) if v['id']=='LAL_2022_R2'),{**next(v for v in z[CONTROL]['sixty_origin_control_functions'] if v['id']=='LAL_2022_R2'),'origin':'WAS'})]:
        bad=copy.deepcopy(s);mutate(bad)
        with patch.object(m,'inputs',return_value=bad):
            try:build()
            except AssertionError:n+=1
            else:raise AssertionError('Source meaning mutation accepted')
    rows=contract_rows(s);rows[15]['conversion_exercised']=True
    with patch.object(m,'contract_rows',return_value=rows):
        try:build()
        except AssertionError:n+=1
        else:raise AssertionError('Substituted TW conversion accepted')
    try:check_acceptance(NAMES[:15],'Unnamed2022rookie',True)
    except AssertionError:n+=1
    else:raise AssertionError('STD16 accepted')
    try:cost_function(None,None)
    except AssertionError:n+=1
    else:raise AssertionError('Null draft charges became zero')
    bad=copy.deepcopy(base);bad['working_implementation']['cost']['new_D23_total_numeric_upper']=170845541
    assert validate(bad);n+=1
    original=construct
    def wrong_cost(z):
        w=original(z);w['cost']['normal_preserved_family_upper_before_new_D23_charge']-=100000;return w
    with patch.object(m,'construct',side_effect=wrong_cost):
        try:build()
        except AssertionError:n+=1
        else:raise AssertionError('Returned whole cost mutation accepted')
    def wrong_period(z):
        w=original(z);w['named_contracts'][11]['last_selected_fiscal_year_end']='2023-06-30';return w
    with patch.object(m,'construct',side_effect=wrong_period):
        try:build()
        except AssertionError:n+=1
        else:raise AssertionError('Returned Protagonist period truncation accepted')
    assert cost_function(1,2)=={'normal_upper':170845542,'apron_upper':172483543}
    return n

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();x=build()
    if a.write:
        (ROOT/OUT).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(x),encoding='utf8')
    errors=[]
    if a.check:
        errors=validate(json.loads((ROOT/OUT).read_text(encoding='utf8')))
        if (ROOT/MD).read_text(encoding='utf8')!=markdown(x):errors.append('MD differs')
    tests=self_test() if a.self_test else None
    print(json.dumps({'current':not errors,'errors':errors,'negative_controls':tests,'STD':15,'TW':2,'named_contracts':17,'conditional_owned2022_claims':2,'wholeFY22_cost_after_D23':False},ensure_ascii=False))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
