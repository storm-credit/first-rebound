"""Finite legal cost domain of the selected Chicago FY23 routine event family."""
from __future__ import annotations
import argparse, copy, hashlib, json
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import build_chicago_2023_selected_routine_execution as execution

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2023_routine_cost_domain.py'
OUT='simulation/CHICAGO_2023_ROUTINE_COST_DOMAIN.json'
EXEC=execution.OUT
EXEC_REVIEW='reviews/CHI_2023_SELECTED_ROUTINE_EXECUTION_G11_INDEPENDENT_REVIEW_2026_10_08.json'
PINS={EXEC:'9a4f6db21d6ad50e2c6d6897f1c2dedbdf440cee89bae47019f4bd131f341790',
 execution.SELF:'ba7ae8fcd0cf7ecb969c74aac1199ec761ec70319e508613339b02bb3c70b6df',
 execution.SELECT:'9847a74948b79bcafa991e4f91884f5dc5f5a83f144a65996f3daa5bae09334c',
 execution.WINDOW:'cf65846136975dd8b7f301505ad7fa06b564837f7962a607681632b84489d092',
 execution.ACTION:'542457d0b30ec2991faf0efa6c92a050dcd9120dfd929473ed29b90b7155f383',
 execution.SLOT:'abbcdaaa6ff14d277f88d47fa600320fc6458ec4b057e5a7b73b414b6fbabf30',
 execution.JOIN_REVIEW:'a5e78aa0bcfd285acb1d9293a69b9edda6967cd7adb968fc459b03b26064b7a1',
 EXEC_REVIEW:'e9bfc3699dd2da3c4cfd6871e05f1b729748674018e617f098f3e5138065f169'}
LAW=execution.prior.LAW
LAW_SHA=execution.prior.RAW[str(LAW)]
PAGES=[31,32,37,57,58,60,62,200,201,203,204,205,206,210,211,212,214,215,220,240,241,242,243,244,245,249,250,255,263,264,271,272,314,316,317,319,323,338,339,342,343,344,346,349,350,453,454,584,631,632]

def norm(t):return t.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(norm((ROOT/p).read_text(encoding='utf-8-sig')).encode()).hexdigest()
def serial(o):return json.dumps(o,ensure_ascii=False,indent=2)+'\n'
def semantic_sha(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def physical():
    for p,h in PINS.items():assert sha(p)==h,'Pinned source changed: '+p
    return {p:json.loads((ROOT/p).read_text(encoding='utf-8-sig')) for p in PINS if p.endswith('.json')}
def source_inputs():return physical()
def assert_sources(s):
    assert s==physical(),'Source semantic objects differ from pinned physical files'
    assert execution.validate(s[EXEC])==[],'Selected execution reconstruction failed'
    assert s[EXEC]['cost_family']['live9_upper']==132051061
    assert s[EXEC]['cost_family']['July7_normal_apron_base_before_R23_first_hold_FRN_conditional_upper']==157912834
    assert s[EXEC]['cost_family']['unused_exception_renunciation_as_fictional_implementation_selected']
    assert not s[EXEC]['renewal_selection_scope']['new_QO_MAXimum_or_FRN_selected']
    r=s[EXEC_REVIEW]
    assert r['status']=='INDEPENDENTLY_ACCEPTED_BOUNDED_SELECTED_FICTIONAL_CONTRACT_CONSUMER' and r['independent_review_completed']
    assert r['source_sha256'][EXEC]==PINS[EXEC] and r['source_sha256'][execution.SELF]==PINS[execution.SELF]
    assert r['saved_validate_current'] and not r['limits']['whole_FY23_legal_cost_or_results_complete']

def primary():
    import fitz
    assert hashlib.sha256(LAW.read_bytes()).hexdigest()==LAW_SHA
    p=fitz.open(LAW);texts={n:norm(p[n-1].get_text()) for n in PAGES}
    flat={n:' '.join(t.split()) for n,t in texts.items()}
    assert 'First Refusal Exercise Notice' in flat[240] and 'issued' in flat[240]
    assert 'shall be deemed to have entered into a Player Contract' in flat[349]
    assert 'Right of First Refusal shall continue' in flat[344]
    assert 'Minimum Player Salary Exception' in flat[264] and 'no bonuses of any kind' in flat[264]
    assert 'Existing Contracts' in flat[255] and 'Qualifying Veteran Free Agent' in flat[255]
    assert 'renounce its rights to use an Exception' in flat[272]
    assert 'Beginning with the 2024-25 Salary Cap Year' in flat[220]
    return {'url':'https://imgix.cosmicjs.com/25da5eb0-15eb-11ee-b5b3-fbd321202bdf-Final-2023-NBA-Collective-Bargaining-Agreement-6-28-23.pdf',
      'raw_cache_path':str(LAW),'raw_sha256':LAW_SHA,
      'PDF1based_text_LF_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest() for n,t in texts.items()},
      'source_text_not_full_private_UPC':True}

def event_frame():
    return {'selected_new_contracts':['Coby White','Javonte Green','Joe Wieskamp','Denzel Valentine','Tomas Satoransky'],
      'selected_other_events':['June28 valid standardQO Dotson/Cook','July7 Bradley FA renunciation',
        'July7 valid unused-exception renunciation','Oct1 Duarte fourth/Kessler third option notices'],
      'new_offer_sheet_or_FirstRefusalExerciseNotice':False,'new_MaximumQO':False,
      'new_trade_S_and_T_BAE_NTMLE_TMLE_or_restricted_buyout_signing':False,
      'new_waiver_retirement_medical_relief_cash_to_otherteam_or_grievance_resolution':False,
      'new_arbitrary_unreported_2023_events_admitted':False,
      'actual_historical_absence_of_all_unpublished_events_certified':False,
      'future_FRN_or_offer_sheet_reopens_UPC_exception_slot_and_cost_case':True}
def assert_frame(f):
    assert f['selected_new_contracts']==['Coby White','Javonte Green','Joe Wieskamp','Denzel Valentine','Tomas Satoransky']
    assert f['selected_other_events']==['June28 valid standardQO Dotson/Cook','July7 Bradley FA renunciation','July7 valid unused-exception renunciation','Oct1 Duarte fourth/Kessler third option notices']
    for key in ['new_offer_sheet_or_FirstRefusalExerciseNotice','new_MaximumQO',
      'new_trade_S_and_T_BAE_NTMLE_TMLE_or_restricted_buyout_signing',
      'new_waiver_retirement_medical_relief_cash_to_otherteam_or_grievance_resolution',
      'new_arbitrary_unreported_2023_events_admitted','actual_historical_absence_of_all_unpublished_events_certified']:
        assert f[key] is False,'Event frame admits an unaccounted new operation: '+key
    assert f['future_FRN_or_offer_sheet_reopens_UPC_exception_slot_and_cost_case']

def domain(s):
    return {'M23':{'type':'NBA_PREPARED_STATUTORY_MINIMUM_FUNCTION',
      'arguments':[0,2,3,4,7],'law':'II6 / IMinimumAnnualSalaryScale / ExC',
      'numerical_floor_ceil_plus2_is_only_conditional_diagnostic':True,
      'all_allowed_inputs_are_lawful_prepared_values_not_arbitrary_positive_numbers':True,
      'exact_prepared_table_or_rounding_certified':False},
      'S23_16':{'type':'NBA_PREPARED_FIRST_ROUND_SCALE_FUNCTION','holder':'CHI','pick':16,
        'law':'I1hhh/iii + VIII1','baseline_ExB631':2946800,
        'unrounded_design_rational':str(Fraction(2946800*136021000,123655000)),
        'nearest100_is_not_inferred_law':True,'published_adjusted_value_certified':False},
      'retained_current_Gamma':{'type':'PRESERVED_PUBLIC_CURRENT_SALARY_ALL_COMPONENT_FAMILY',
        'normal_apron_component_upper':132051061,'new_assignment':False,
        'old_capitalized_assignment_and_performance_in_upper_preserved':True,'actual_private_Gamma_selected':None},
      'R23':{'type':'NAMED_PREVIOUS_VALID_STRETCH_AND_ORIGINAL_OBLIGATION_BOUND','interval':[0,16371000],
        'ordinary13_salary_endpoints':'<=2020–21; past payment delay does not create newFY23 Salary',
        'Stanley_prior_fullFY22_cash_preserved':2351532,'Stanley_currentSalary_period_ended':'2023-06-30',
        'cash_balance_or_all_stretch_zero_certified':False},
      'FRN':{'type':'ISSUED_FIRST_REFUSAL_EXERCISE_NOTICE_EVENT_NOT_ROFR_RIGHT',
        'selected_current_family_charge':0,'zero_basis':'No newOfferSheet or issuedmatchingnotice in declared selectedeventfamily; not inferred privateabsence',
        'old2022_UPC_replaced_priorFA_QO_FRN_claim_once':True,'original_Gamma_is_new_FRN':False,
        'ROFR_rights_charge_and_QO_salary_remain_separate':True,
        'if_new_matching_notice_selected':'XI5g deems anewUPC; recheckVIII/II7/exception/STD15 and newSalary; outside unchangedfamily'},
      'QO':{'holders':['Devon Dotson','Tyler Cook'],'operative_issuance':'2017 lawJune28,2023',
        'selected_new_UPC_count':0,'statutory_base_functions':['M23(3)','M23(4)'],
        'bonuses':0,'until_offer_deadline':'2023-10-02, absent later validaction',
        'after_deadline_ROFR_continues':'XI4c(ii), subjectXI5a; originalunacceptedoffer doesnotremainoutstanding',
        'conservative_annual_charge_reservation_kept':'M23(3)+M23(4) allFY23; mayoverreservepostdeadline normal/apron, notactualcash'},
      'first_RSC_optional_case':{'ordinary_selected_case':'UNSIGNED_WITH_VALID_TENDER_AND_POSITIVE_NORMAL_HOLD',
        'comparison_case':'A laterconformingRSC canconsumeonlyreservedSTD1; notselectedhere',
        'q_first_salary_interval':'max(0.8*S23(16),M23(0))..1.2*S23(16)',
        'new_RSC_bonus':0,'two_guaranteed_seasons_two_team_options':True,
        'new_UPC_or_player_identity_selected':False}}
def assert_domain(d,s):
    assert d['M23']['arguments']==[0,2,3,4,7] and not d['M23']['exact_prepared_table_or_rounding_certified']
    assert d['M23']['all_allowed_inputs_are_lawful_prepared_values_not_arbitrary_positive_numbers']
    assert d['S23_16']['holder']=='CHI' and d['S23_16']['pick']==16 and d['S23_16']['baseline_ExB631']==2946800
    assert d['S23_16']['unrounded_design_rational']==str(Fraction(2946800*136021000,123655000)) and not d['S23_16']['published_adjusted_value_certified']
    assert d['retained_current_Gamma']['normal_apron_component_upper']==132051061 and not d['retained_current_Gamma']['new_assignment']
    assert d['retained_current_Gamma']['old_capitalized_assignment_and_performance_in_upper_preserved']
    assert d['R23']['interval']==[0,16371000] and not d['R23']['cash_balance_or_all_stretch_zero_certified']
    assert d['FRN']['selected_current_family_charge']==0 and not d['FRN']['original_Gamma_is_new_FRN']
    assert d['FRN']['ROFR_rights_charge_and_QO_salary_remain_separate']
    assert d['QO']['holders']==['Devon Dotson','Tyler Cook'] and d['QO']['statutory_base_functions']==['M23(3)','M23(4)']
    assert d['QO']['selected_new_UPC_count']==d['QO']['bonuses']==0
    r=d['first_RSC_optional_case'];assert not r['new_UPC_or_player_identity_selected'] and r['new_RSC_bonus']==0
    assert r['two_guaranteed_seasons_two_team_options'] and r['q_first_salary_interval']=='max(0.8*S23(16),M23(0))..1.2*S23(16)'

def hold_lifecycle():
    return {'scope_end':'2024-06-30; later FY24 events require their own named transition',
      'conditions':'No QO acceptance, withdrawal, agreed extension, OfferSheet, issued FRN or later FA renunciation selected',
      'QO_rows':[
        {'window':'2023-07-07 through ordinary acceptance deadline 2023-10-02',
         'normal':'For each completed TW: max(M23(0), outstanding standardQO M23(y)); y=3/4',
         'apron':'Outstanding standardQO M23(3)+M23(4), new unlikely bonus0',
         'outstanding_QO':True,'ROFR_continues':True,'new_UPC_cash':0},
        {'window':'After 2023-10-02 through FY23 opening and 2024-06-30',
         'normal':'Two unrenounced completed-TW Free Agent Amounts M23(0)+M23(0)',
         'apron':'FA Amounts excluded; expired QO is not outstanding; newFRN0 in declared event frame',
         'outstanding_QO':False,'ROFR_continues':True,'new_UPC_cash':0}],
      'first_RT':{'deadline':'2023-07-17 valid offer; conforming acceptance window at least first Regular Season day',
        'normal_until_sign_or_valid_renounce':'Unsigned CHI first#16 remains 1.2*S23(16); RT nonacceptance does not erase draft hold',
        'apron_while_outstanding':'Conforming firstRT Salary; not 120% unsigned normal hold',
        'apron_after_acceptance_period_expires':'No outstanding RT amount; no automatic newUPC',
        'cash_before_acceptance':0,'new_STD_before_acceptance':0,
        'future_annual_tender':'If remains unsigned, applicable X4 subsequent-year tender and rights deadlines must be supplied when that window opens; not automatic foreverrights'},
      'first_regular_day_is_lawful_calendar_parameter_not_clinical_fact':True,
      'annual_QO_and_first_RT_full_reservations_are_safe_upper_not_postexpiry_statutory_charges':True,
      'QO_expiry_deletes_FA_rights_or_hold':False,'FY24_options_add_FY23_salary':False,
      'actual_expiry_acceptance_or_receipts_certified':False}
def assert_lifecycle(x):
    # Independent literals bind charge transitions to VII4 and XI4/5; not a
    # second call to the mutable constructor.
    assert x['scope_end']=='2024-06-30; later FY24 events require their own named transition'
    assert x['conditions']=='No QO acceptance, withdrawal, agreed extension, OfferSheet, issued FRN or later FA renunciation selected'
    a,b=x['QO_rows'];assert len(x['QO_rows'])==2
    assert a=={'window':'2023-07-07 through ordinary acceptance deadline 2023-10-02',
      'normal':'For each completed TW: max(M23(0), outstanding standardQO M23(y)); y=3/4',
      'apron':'Outstanding standardQO M23(3)+M23(4), new unlikely bonus0',
      'outstanding_QO':True,'ROFR_continues':True,'new_UPC_cash':0}
    assert b=={'window':'After 2023-10-02 through FY23 opening and 2024-06-30',
      'normal':'Two unrenounced completed-TW Free Agent Amounts M23(0)+M23(0)',
      'apron':'FA Amounts excluded; expired QO is not outstanding; newFRN0 in declared event frame',
      'outstanding_QO':False,'ROFR_continues':True,'new_UPC_cash':0},'QO deadline does not delete unrenounced FA hold or rights'
    r=x['first_RT']
    assert r['deadline']=='2023-07-17 valid offer; conforming acceptance window at least first Regular Season day'
    assert r['normal_until_sign_or_valid_renounce']=='Unsigned CHI first#16 remains 1.2*S23(16); RT nonacceptance does not erase draft hold'
    assert r['apron_while_outstanding']=='Conforming firstRT Salary; not 120% unsigned normal hold'
    assert r['apron_after_acceptance_period_expires']=='No outstanding RT amount; no automatic newUPC'
    assert r['cash_before_acceptance']==r['new_STD_before_acceptance']==0
    assert r['future_annual_tender']=='If remains unsigned, applicable X4 subsequent-year tender and rights deadlines must be supplied when that window opens; not automatic foreverrights'
    assert x['first_regular_day_is_lawful_calendar_parameter_not_clinical_fact'] and x['annual_QO_and_first_RT_full_reservations_are_safe_upper_not_postexpiry_statutory_charges']
    assert not x['QO_expiry_deletes_FA_rights_or_hold'] and not x['FY24_options_add_FY23_salary'] and not x['actual_expiry_acceptance_or_receipts_certified']

def categories(s):
    return [
      {'id':'LIVE','actors':[r['player'] for r in s[EXEC]['named_contracts_and_rights'] if r['player'] in execution.LIVE],
       'normal_apron':'OriginalCurrentSalary+allperformance upper132051061, oldcapitalizedGamma preserved','legal_means':'VII6a existingcontracts','cash':'Fulloriginalobligation, notactualpaymentreceipt'},
      {'id':'NEW_SELECTED','actors':['Coby White']+list(execution.MIN_NAMES),
       'normal_apron':'12m+M23(4)+M23(2)+2M23(7), fullcashmoreconservative thanone-yearreimbursement','legal_means':'VII6b1 FullBird / VII6i one-seasonminimum noanybonus','cash':'Selectedfullprotectedannualcash obligation, notreceipt'},
      {'id':'EXPIRED_FA_QO','actors':execution.prior.EXPIRED+list(execution.TW_NAMES),
       'normal_apron':'Re-sign5sameholdreplacedonce;Bradleyvalidrenounce;DotsonCookstandardQO M23(3)+M23(4) conservativelyreserved;FRN0 selectedeventfamily','legal_means':'VII4a2,d,g / XI4c,5g','cash':'UnacceptedQOandFAhold are notnewcash/UPC; oldprotectedcash retained'},
      {'id':'DRAFT_RIGHTS','actors':['CHI2023 first#16 unnamedrookie','Marko Simonovic','Keon Ellis'],
       'normal_apron':'UnsignedfirstN23=1.2S; apronconformingRTSalary; Marko/Ellis noNBAUPC norunsignedsecondstatutorycapcharge','legal_means':'VII4e/VIII1/X4-6; RequiredTender legalcalendar','cash':'UnacceptedRT isnotcash;foreignactualfees notcertified0; no newNBAforeignpaymentselected'},
      {'id':'LEGACY','actors':['Originalnamedpriorwaiverinventory','Stanley Johnson priorFY22'],
       'normal_apron':'R23 within0..16371000; no doubleoldcampcashorordinaryexpiredSalary; preserved sourceframe','legal_means':'Originalordinaryperiodendpoints+validstretchcarry; no new2023resolutionevent','cash':'Pastbalance retainsseparatedebtobligation; currentSalaryperiodend isnotpaidbalance0'},
      {'id':'EXCEPTIONS_OTHER','actors':['UnusedannualNTMLE/TMLE/BAE/DPE/TPE entitlements','Incomplete roster','Tax minimum-team adjustments'],
       'normal_apron':'Beforeselectedrenounceincludeincorporatedunusedamount; aftervalidrenounce0chargedunused; apronexcludesunused; counted14STD+RFA+first>=12','legal_means':'VII6n2 / VII4f / VII2e,c,d; no newretirementorresolution selected','cash':'Unusedexception isnotcash; TaxliabilityseparatefromPlayerSalary'}]
def assert_categories(c,s):
    assert [x['id'] for x in c]==['LIVE','NEW_SELECTED','EXPIRED_FA_QO','DRAFT_RIGHTS','LEGACY','EXCEPTIONS_OTHER']
    assert c[0]['actors']==list(execution.LIVE) or set(c[0]['actors'])==set(execution.LIVE)
    assert c[1]['actors']==['Coby White']+list(execution.MIN_NAMES)
    assert c[2]['actors']==execution.prior.EXPIRED+list(execution.TW_NAMES)
    assert c[3]['actors']==['CHI2023 first#16 unnamedrookie','Marko Simonovic','Keon Ellis']
    assert c[0]['normal_apron']=='OriginalCurrentSalary+allperformance upper132051061, oldcapitalizedGamma preserved'
    assert s[EXEC]['cost_family']['live9_upper']==132051061
    assert semantic_sha(c)=='38993221dbf251c6e83118486492696372b66d6021bbcf69bc60884701efb58f','Returned six categories differ from fixed source-supported cost and legal meanings'

def symbolic_checks(s):
    # RSC salary may be below public120% ceiling; use80% lower for minimum-team proof.
    live_lower=Fraction(132051061)-Fraction(9835881,3)-Fraction(4810200,3)
    assert live_lower==127169034 and live_lower+12000000>122418000
    rows=s[EXEC]['named_contracts_and_rights'];assert sum(r['STD'] for r in rows)==14 and sum(r['TW'] for r in rows)==0
    return {'quantifier':'For every lawfulpreparedM23/S23(16), everypreservedoriginalGamma/componentfamily andR23 in bound, selectedroutinelegalmeans remainvalid. Parameters are notarbitrarypositive salaries.',
      'existing_contracts':'VII6a lawfuloriginalcurrentUPCs; no newassignment/renegotiation inframe',
      'Coby':'FullBird3service years/rights preserved;12m<=25%*136021000=34005250;3years<=Bird5;0raise<=8%;fullprotection,nooption/bonus',
      'minimum4':'ExactlystatutorypreparedMforselectedcreditedYOS,1Season<=2, no bonuses: VII6i remainsusableabovecap/aprons',
      'unsigned_or_optional_RSC':'VIII1/VII6h;possibleprice interval within80–120andminimum,2guaranteed+2options; STD14+1<=15; no simultaneousextraUPC',
      'option_notices':'Oct1 selectedoptions onlyFY24; currentFY23charged0additional; no extensionornewassignment',
      'hardcap':'None ofselectedoperations areVII2eA–K transactions. NoBAE/NTMLE/TMLE/S&T/restrictedbuyout/tradedexception/cashtrade. Historicalhardcap notannualcarry.',
      'second_apron_first_pick_penalty':'VII2f begins2024–25, notimposedon2023–24 sourcefamily; no newfuturefirstmovechosen',
      'minimum_team_salary_lower_proof':{'live9_lower':str(live_lower),'plus_selected_Coby':12000000,
        'combined_lower':str(live_lower+12000000),'required':122418000,'minimum4_legacy_QO_or_first_cash_not_needed':True,
        'statement':'LiveRSCcomponent80% lower + selectedfixedbaseothers. ConservativeMTSneednotrelyonholdorlegacydeadcash.'},
      'registration':'Selected14STD0TW offseason<=21/regular14..15; conditionalnewfirstSTD1 gives15; health/active12..15/coachfunctions separate, no roster-status==clinical proof',
      'constraints_satisfied_for_whole_selected_cost_domain':True,
      'actual_taxpayer_apron_status_or_private_receipts_certified':False}

def numerical_diagnostic(s):
    # No inventedadjustedtable: retain symbolicfirstscales and exactstatutoryforms.
    base=s[EXEC]['cost_family']['July7_normal_apron_base_before_R23_first_hold_FRN_conditional_upper']
    assert base==157912834
    return {'type':'CONDITIONAL_PUBLISHED_SCALE_ROUNDING_SCREEN_NOT_LEGAL_EXACT_TABLE',
      'base_before_R23_first_upper':base,'R23_upper':16371000,'base_plus_R23_upper':base+16371000,
      'unsigned_normal_expression':f'{base+16371000} +1.2*S23(16)',
      'unsigned_apron_expression':f'{base+16371000} + conformingRTSalary',
      'optional_signed_RSC_normal_apron_expression':f'{base+16371000} +1.2*S23(16)',
      'first_apron':172346000,'second_apron':182794000,'TaxLevel':165294000,
      'first_apron_margin_may_be_negative':True,'negative_margin_is_illegality':False,
      'screen_not_legal_price_selection':True,'actualpreparedscale_or_rounding_certified':False}

def assert_checks(c):
    assert c['hardcap']=='None ofselectedoperations areVII2eA–K transactions. NoBAE/NTMLE/TMLE/S&T/restrictedbuyout/tradedexception/cashtrade. Historicalhardcap notannualcarry.','Selected Bird/minimum/ownRSC does not create a hardcap'
    p=c['minimum_team_salary_lower_proof']
    lower=Fraction(132051061)-Fraction(9835881,3)-Fraction(4810200,3)
    assert p['live9_lower']==str(lower) and p['combined_lower']==str(lower+12000000) and p['required']==122418000
    assert c['constraints_satisfied_for_whole_selected_cost_domain'] and not c['actual_taxpayer_apron_status_or_private_receipts_certified']
    assert semantic_sha(c)=='6dc65333da90e162cc809ae1b3c797f759754ff713bc73e67d7edc4bc1b446c9','Returned legal checks differ from fixed primary-law meanings'

def assert_diagnostic(n,s):
    expected=s[EXEC]['cost_family']['July7_normal_apron_base_before_R23_first_hold_FRN_conditional_upper']
    assert expected==157912834 and n['base_before_R23_first_upper']==expected,'Returned base differs from physical selected cost family'
    assert n['R23_upper']==16371000 and n['base_plus_R23_upper']==expected+16371000
    assert n['unsigned_normal_expression']==f'{expected+16371000} +1.2*S23(16)'
    assert n['unsigned_apron_expression']==f'{expected+16371000} + conformingRTSalary'
    assert n['first_apron']==172346000 and n['second_apron']==182794000 and n['TaxLevel']==165294000
    assert not n['negative_margin_is_illegality'] and not n['actualpreparedscale_or_rounding_certified']
    assert semantic_sha(n)=='637e728a845c93cd9d537ece34be66535e0ad7df5a1c679e2c4eaf0d4a5905a8','Returned diagnostic differs from fixed conditional screen'

def build():
    s=source_inputs();assert_sources(s);f=event_frame();assert_frame(f);d=domain(s);assert_domain(d,s)
    c=categories(s);assert_categories(c,s);checks=symbolic_checks(s);assert_checks(checks)
    n=numerical_diagnostic(s);assert_diagnostic(n,s);l=hold_lifecycle();assert_lifecycle(l)
    return {'id':'CHICAGO_2023_ROUTINE_COST_DOMAIN','status':'REVIEW_PENDING_COMPLETE_TYPED_SELECTED_PUBLIC_COST_AND_LEGAL_OPERATION_DOMAIN',
      'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8_BOM_STRIPPED_CRLF_CR_TO_LF_EXTERNAL_PDF_RAW_SEPARATE',
      'primary':primary(),'event_frame':f,'domains':d,'six_categories':c,'hold_lifecycle_through_FY23':l,'symbolic_legal_checks':checks,
      'upstream_consumer_independent_review':{'path':EXEC_REVIEW,'sha256':PINS[EXEC_REVIEW],'completed':True,'is_new_cost_domain_review':False},
      'cost_forms':{'normal_afterJuly7_unsigned':'U_live9 +12000000 +M23(4)+M23(2)+2M23(7) +M23(3)+M23(4) +R23 +1.2*S23(16)',
        'apron_afterJuly7_unsigned':'SamefullcashandQOupper +R23 + conformingfirstRTSalary (<=1.2S); noUFAhold/unusedexception/incompleterosteramount',
        'optional_later_first_RSC':'Replace sameunsignednormalhold/apronRT once byRSC Salary+Unlikely<=1.2S; addSTD1only; noselectedsignatureinthisartifact',
        'prefix_beforeJuly7':'U_live9+allnamedFA/QOholds(Normal) orRFAQO+Unlikely(Apron)+positivefirsthold/RT+R23+incorporatedunusedexceptionsNormal. Eachlegaldefinitionkept; newminimum/BirdafterJuly7only.',
        'FA_max_QO_FRN':'NoMaximumQOornewFRN. OrdinaryQO positive. OutstandingFAclaims beforevalidreplacement/renounce preserved.',
        'tax':'VII2d lastRegular-start auditedTeamSalary plus earnedpreviouslyexcludedincentives minusunearnedlikely, latertrade/reinclusion,minus50%NBA suspensionreduction,+0/1YOSFA2YOSfloor. Wholeearnedamount withinreservedallperformance; noexactTaxSalary/nonpayer certificate.',
        'tax_safe_annual_player_salary_outer':'Livecurrentallcomponentupper +selectednew5fullcash +R23 +1.2S ifoptionalfirstsigns; QO/FA/RT notnewPlayercash. FinalauditedTaxdefinition retained ratherthanequalnormal/apron.',
        'cash':'Selectedlive/newUPCs createfullprotectedcash obligations. UnacceptedRT/QO/FAhold/unusedexception notactualcash. Original maturedpriorpayments preserveseparatedebtbank; timing doesnotchangeSalaryyear.',
        'exact_normal_total':None,'exact_apron_total':None,'exact_tax_total':None,'actual_cash_paid_or_old_balance':None},
      'numeric_diagnostic':n,
      'completion_scope':{'all_six_current_cost_category_functions_accounted':True,
        'all_selected_legal_operation_inputs_domain_covered':True,'new_private_all_absence_or_receipt_gate':False,
        'FRN_unknown_required_without_new_matching_event':False,
        'source_supported_family_is_all_imaginary_private_contracts':False,
        'independent_review_completed':False,'exact_M23_S23_table_point_or_rounding_certified':False,
        'whole_actual_private_cost_or_season_or_macro3':False,'new_draftee_or_LaMelo_price_selected':False,
        'REGISTER_promotion':False,'manuscript_allowed':False},
      'finite_later_actions':['If firstUPCisnextselected, consumeonlyreservedSTD1andsamepositiveS23claim; thisisnotanunknownprivatebill',
        'BindactualpreparedM/Saslawfunctionsfornumericalconsumer; separateconditionalroundingscreen',
        'If anOfferSheet/FRN/newexception/waiver/resolutionistrulyselected, reopenonlythatnamedcostandlegalcase',
        'BuildFY23calendar/health/active/roles/resultsseparately; costdomaincannotcertifythem'],
      'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0}

def validate(o):
    try:
        assert o==build(),'Stored cost domain differs from source-bound reconstruction'
        assert_frame(o['event_frame']);assert_domain(o['domains'],physical());assert_categories(o['six_categories'],physical());assert_lifecycle(o['hold_lifecycle_through_FY23'])
        assert_checks(o['symbolic_legal_checks']);assert_diagnostic(o['numeric_diagnostic'],physical())
        return []
    except (AssertionError,ValueError,TypeError,KeyError) as e:return [str(e)]
def md(o):
    lines=['# Chicago 2023 선택 계약의 유한 법적 비용 영역','',o['status'],'',
      '선택된 publicfamily의 **6비용범주 전체 함수**와 허용 계약수단을 연결한다. 법정가격 `M23(YOS)`/`S23(16)`는 NBA가 준비한 함수이며 임의 양수연봉이 아니다. 원 currentSalary/모든성과/기존Γ와 `R23∈[0,16.371m]`는 유지한다. 실제private장부·지급·표반올림·시즌 전체를 인증하지 않는다.','',
      '| 범주 | 포함 범위 |','|---|---|']
    for c in o['six_categories']:lines.append('|'+c['id']+'|'+c['normal_apron']+'|')
    lines+=['','## FRN은 별도 미가격 장부가 아니다','',
      'ROFR은 권리다. VII4a2(PDF240)의 FRN 금액은 **issued First Refusal Exercise Notice**이고, XI5g(PDF349)는 OfferSheet에 대한 matchingnotice로 새UPC가 성립한다고 한다. 선택된 가족에는 새OfferSheet/FRN/MaximumQO가 없다. 따라서 해당 **사건 항목0**은 작품의 유한 실행범위이며 실제비공개 notice 부재 인증이 아니다. 원 Γ를 FRN으로 다시 더하지 않는다. Dotson/Cook의 미수락 표준QO와 FAhold/ROFR은 계속 남는다. 새 matching을 선택하면 그 이름의 새UPC·예외·슬롯·급여를 별도 검문한다.','',
      'XI4c(ii)(PDF344)에 따라 QO수락기한이 지나도 ROFR은 조건부 계속된다. 기존 offer를 무기한 outstanding으로 인증하지 않는다. 현재 wholeannual 보수상단은 QO급여 두 개를 계속 예약하므로 후행종료에 따라 낮아질 비용을 누락하지 않는다.','',
      '**October2 이후–FY23 개막–2024June30**의 미연장·미수락·미포기 가족에서 Dotson/Cook의 normal은 completed-TW FAAmount 각 `M23(0)`으로 남고, apron은 만료QO/FAAmount를 실제 산입하지 않는다. Annualupper에 `M23(3)+M23(4)`를 계속 예약하는 것은 안전한 초과상단이다. 미수락 firstRT도 실제 유효 수락창이 끝나면 apron의 outstandingRT가 사라지지만 normal의 unsigned `1.2S23(16)`과 별도 draft권리는 자동삭제되지 않는다. 개막일은 적법한 달력 입력이며 임상·실제수락 사실이 아니다. 2024 후속 annualTender는 그 이름의 다음 법정창에서 다시 공급한다.','',
      '## 법적 구현 전범위','',
      '기존UPCs는 VII6a, Coby$12m×3는 qualifyingBird3/8%이하/II7최대이하, minimum4는 VII6i의 법정가격 한 시즌·보너스0다. 후행 RSC가 선택되면 VII6h/VIII1 범위80–120%와 최소의 교집합, 두 guaranteed+두 teamoptions, 남은STD1칸만 소비한다. 현재14STD0TW 또는 조건부15STD는 regular14–15/offseason21 이내다. 구체 active·임상·코칭은 이 비용함수의 인증이 아니다.','',
      'October옵션은FY24만 추가한다. 선택된 사건은 VII2e A–K hardcap 유발 거래가 없으므로 **어떤 허용 R23·성과 성분값에서도** 단순apron 초과가 계약위법으로 바뀌지 않는다. 2021hardcap의자동이월0, 2024–25부터의새second-apronfirst-pickpenalty를2023에소급0. 원RSC80% 하한을 사용한live9 하한$127,169,034+Coby$12m=$139,169,034로 minimumteam$122,418,000을 넘는다. Hold/waivedcash를 최소팀의 실제선수급여로 대신 넣지 않는다.','',
      'Normal/apron은 미수락 firstRT·FA/unusedexception 처리 차이를 보존한다. July7 유효unusedexception renounce는 signedCaruso급여나 CobyBird권리를 지우지 않는다. Tax는 VII2d의 lastRegular-start/earnedincentives/미지급likely·suspension·0/1YOSFAfloor 규칙으로 따로 계산한다. Taxpayer 확정이나 tax비용지급0을 주장하지 않는다. 현금은 실제UPC 보호지급 의무와 과거잔액을 보존하며 미수락RT/QO/hold를 실지급으로 부르지 않는다.','',
      '## 수치와 종료 범위','',
      '조건부 최소 floor..ceil+2 screen에서 기준$157,912,834+R상단$16,371,000=$174,283,834 **이후 first비용**이다. Normal은여기에1.2S23(16), apron은conformingRT가격을 더한다. 음수apron여유≠불법이며 prepared표/공식반올림 미회수는 lawfunction의 의미를0으로 바꿀 이유가 아니다.','',
      '이 패킷은 전체 **선택 법적 비용 도메인**을 닫는 검문 가능한 증인이다. 숫자 screen을 정확UPC가격으로 채택하지 않고, 모든상상가능미공표 미래합의도 가족에 추가하지 않는다. 이후 실제새 사건은 해당이름 하나만 재개방한다. 전체 달력·기용·임상·결과·LaMelo연장/드래프티·macro3완료는 별도다.','',execution.prior.progress()]
    return '\n'.join(lines)+'\n'
def self_test():
    done=[]
    for label,key,val in [('unaccounted_matching_notice','new_offer_sheet_or_FirstRefusalExerciseNotice',True),
      ('new_NTMLE_in_same_family','new_trade_S_and_T_BAE_NTMLE_TMLE_or_restricted_buyout_signing',True)]:
        f=event_frame();f[key]=val
        try:
            with patch(__name__+'.event_frame',return_value=f):build()
        except AssertionError:done.append(label)
        else:raise AssertionError('FALSE PASS '+label)
    s=source_inputs()
    for label,parent,key,val in [('delete_original_Gamma','retained_current_Gamma','normal_apron_component_upper',1),
      ('hold_rights_is_UPC','QO','selected_new_UPC_count',2),('wrong_first_origin','S23_16','holder','WAS'),
      ('drop_stretch_upper','R23','interval',[0,0])]:
        d=domain(s);d[parent][key]=val
        try:
            with patch(__name__+'.domain',return_value=d):build()
        except AssertionError:done.append(label)
        else:raise AssertionError('FALSE PASS '+label)
    l=hold_lifecycle();l['QO_rows'][1]['normal']='0'
    try:
        with patch(__name__+'.hold_lifecycle',return_value=l):build()
    except AssertionError:done.append('expiry_erases_unrenounced_FA_hold')
    else:raise AssertionError('FALSE PASS expiry hold')
    c=categories(s);c[0]['normal_apron']='Existing signed current salary 0'
    checks=symbolic_checks(s);checks['hardcap']='Coby Bird triggers automatic hardcap'
    diagnostic=numerical_diagnostic(s);diagnostic['base_before_R23_first_upper']=0
    for label,helper,bad in [('delete_signed_current_category','categories',c),
      ('invent_Bird_hardcap','symbolic_checks',checks),('delete_diagnostic_base','numerical_diagnostic',diagnostic)]:
        try:
            with patch(__name__+'.'+helper,return_value=bad):build()
        except AssertionError:done.append(label)
        else:raise AssertionError('FALSE PASS '+label)
    return done
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();o=build()
    if a.write:
        (ROOT/OUT).write_text(serial(o),encoding='utf8',newline='\n');(ROOT/OUT.replace('.json','.md')).write_text(md(o),encoding='utf8',newline='\n')
    e=[]
    if a.check:
        stored=json.loads((ROOT/OUT).read_text(encoding='utf-8-sig'));e=validate(stored)
        if norm((ROOT/OUT.replace('.json','.md')).read_text(encoding='utf-8-sig'))!=md(stored):e.append('Markdown stale')
    tests=self_test() if a.self_test else []
    print(json.dumps({'current':not e,'errors':e,'categories':6,'symbolic_domain_complete':True,'numeric_total_exact':False,'negative_controls':tests},ensure_ascii=False))
    if e:raise SystemExit(1)
if __name__=='__main__':main()
