"""2022–23 approved-core carry and bounded pre-new-contract cost inputs.
No unselected LaVine, protagonist or Carter contract becomes an existing salary.
"""
import argparse
import copy
import hashlib
import html
import json
import re
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import fitz
import build_2021_chicago_a_full_cost_family as previous

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_23_approved_core_contract_execution.py'
OUT='research/CHICAGO_2022_23_APPROVED_CORE_CONTRACT_EXECUTION_2026_10_07.json'
MD=OUT[:-5]+'.md'
BASELINE='e1076617f72be15f72e6289d8af553481736e59e'
CAP22=123655000
TAX22=150267000
CAP21=112414000
CAP17=99093000
APRON21=143002000
TAX21=136606000
CBA=Path(r'C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
CACHE=Path(r'C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-chi-core2022-20261007')
PINS={'research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json': '7244beff7a120c5ca246a04e72b61586f3cfbe245487d5fc6479f5245fd78d9f', 'tools/build_2021_chicago_a_full_cost_family.py': 'de9a28dda0e26cf6fee95c889f910175355bc4b0ffb384f1b6662c8f08646574', 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json': '253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088', 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json': '9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce', 'canon/CAREER_TIMELINE.md': 'c6420cc02031b138103fe83dc02437dd209a3925d005e9a063855a66ee467eca', 'simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE_INPUTS.json': '4b66d96a274fa4d31e41f6256192449e8b43a6dfc00e8f4e44f4cbd76e83bf78', 'simulation/CHICAGO_LONG_CORE_CBA_INPUTS.json': '7985e65cb5e184356aead888d4f016aca187dd2dd3185ea6de76527a6937fe0c', 'simulation/CHICAGO_2021_M1_AUTHOR_BRIDGE.json': 'cdc9c0f5f751c09be48dce16e4471ef307fbacd649d3a1f08f7108ed8aa61b95', 'research/CHICAGO_2021_23_CONTINUATION_SOURCES.json': '4dc3cfb7416174c0fea5c2710e9915a729d362dc553f216f4e9c861b373e9db3', 'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2'}
RAW=[{'id': 'NBA_CAP2022', 'url': 'https://pr.nba.com/nba-salary-cap-2022-23-season/', 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-chi-core2022-20261007\\NBA_CAP2022.html', 'http_status': 200, 'raw_sha256': '2e76093cfc91b6257f18cddd25441090118f36bd8a942259fbc340438ff5e57f', 'bytes': 109871}, {'id': 'NBA_CAP2017', 'url': 'https://pr.nba.com/nba-salary-cap-2017-18-season/', 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-chi-core2022-20261007\\NBA_CAP2017.html', 'http_status': 200, 'raw_sha256': '267f33461fe7709d3d47d49ee708e96b8e7f5e7230971a8833e67a1ffd1157a3', 'bytes': 109930}, {'id': 'NBA_CAP2018', 'url': 'https://pr.nba.com/nba-salary-cap-2018-19-season/', 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-chi-core2022-20261007\\NBA_CAP2018.html', 'http_status': 200, 'raw_sha256': '333cc3f62b0ce070cf8aba907b07689237722cee2fccef6eedb97fe1738d6b84', 'bytes': 109846}, {'id': 'COBY_OPTION2021', 'url': 'https://www.nba.com/news/bulls-exercise-contract-options-on-coby-white-patrick-williams', 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-chi-core2022-20261007\\COBY_OPTION2021.html', 'http_status': 200, 'raw_sha256': 'ba75535908926b2b3bcca82db22efc6821df8799e55ce0afea4b65bb0f1e3697', 'bytes': 311845}, {'id': 'ziaire-williams', 'url': 'https://www.salaryswish.com/players/ziaire-williams', 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-chi-core2022-20261007\\ziaire-williams.html', 'http_status': 200, 'raw_sha256': '4054c0f7dfa77fa45cf26c512d431e490f5d2975f4d32725756adc988cbd2076', 'bytes': 105832, 'rows': ['2021-22 | $4,373,040 | $4,273,040 | $4,273,040 | $100,000 | $0', '2022-23 | $4,591,680 | $4,491,680 (+5%) | $4,491,680 | $100,000 | $0']}, {'id': 'alex-caruso', 'url': 'https://www.salaryswish.com/players/alex-caruso', 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-chi-core2022-20261007\\alex-caruso.html', 'http_status': 200, 'raw_sha256': 'ec0857bec1d1933e524efe62a298943dc001f12b86c8e1f78974200d21f913e3', 'bytes': 117408, 'rows': ['2021-22 | $8,600,000 | $8,600,000 | $8,600,000 | $0 | $0', '2022-23 | $9,030,000 | $9,030,000 (+5%) | $9,030,000 | $0 | $0']}]
FIXED_CARRY={'Markkanen':18360000,'Caruso':9030000,'LaMelo Ball':7775400,'Coby White':7413955,'Chris Duarte':4591680}
MIN_ROWS={'Green':(3,1600520),'Joe Wieskamp':(1,1378242),'Tony Bradley':(5,1795015),'Stanley Johnson':(7,2072867),'Denzel Valentine':(6,1933941)}
# A deliberately wider screen than integer-dollar table presentation. This is
# not a source-certified statutory rounding algorithm or a negotiated dollar.
ROUNDING_SCREEN=10
EXPIRED=['LaVine','Protagonist','Wendell Carter Jr.','Thaddeus Young','Tomas Satoransky']


def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def ceil(q):return -(-q.numerator//q.denominator)
def ratio(q):return {'numerator':q.numerator,'denominator':q.denominator}
def plain(b):return html.unescape(re.sub('<[^>]+>',' ',b.decode('utf8','replace')))


def routine():
    return {'classification':'SOURCE_SUPPORTED_ROUTINE_CARRY_CANDIDATE_WITHIN_M1_A_NOT_NEW_AUTHOR_LOCK',
        'Coby_fourth_year_option':{'exercise_candidate_date':'2021-10-01','signed_player_notice':True,'actual_receipt_certified':False},
        'LaMelo_third_year_option':{'exercise_candidate_date':'2021-10-01','signed_player_notice':True,'actual_receipt_certified':False},
        'two_year_minimum_contracts':'Preserve the reviewed2021 two-year minimum family; for this carry realization add no unselected player/team option, new bonus, waiver, renegotiation or extension.',
        'minimum_year2_scale':'2021–22 signing-year scale, credited YOS in2022–23, contractYear2 under II6; not the2022 new-contract Year1 scale.',
        'Duarte':'Preserve120% rookie Salary+Unlikely ceiling at#10; no Ziaire100000 performance bonus or individual contract copied.',
        'new_LaVine_Protagonist_Carter_Young_Satoransky_contract_selected':False,
        'P2018_exact_pick_selected':False,'P2018_team':'Chicago','P2018_pick_domain':[16,30],
        '2021_NTMLE_hardcap_automatically_carried_into2022':False,
        'new2022_hardcap_trigger_selected':False,'actual_private_contracts_or_delivery_certified':False,
        'whole2022_roster_selected':False,'new_author_lock':False}

FIXED_ROUTINE=copy.deepcopy(routine())


def fixed_inputs():
    for p,pin in PINS.items():assert sha(p)==pin,'Unreviewed source '+p
    old=load(previous.OUT);assert not previous.validate(old),'Previous whole public cost family changed'
    assert old['independent_review_completed'] and old['whole_source_supported_cost_family_pass']
    m1=load('canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json')
    assert m1['selected']['route']=='M1'
    assert m1['selected']['proposed_salary_by_season_usd']['2022-23']==18360000
    nc=old['routine_implementation']['new_contracts']
    assert nc['Caruso']['proposed_regular_schedule']==[8600000,9030000,9460000,9890000]
    assert nc['Caruso']['signing_performance_trade_promotional_loan_or_buyout_additions']==0
    for who in MIN_ROWS:
        assert nc[who]['years']==2 and nc[who]['all_bonuses']==0
    assert nc['Chris Duarte']['rookie_Salary_plus_Unlikely_ceiling']==4373040
    canon=text('canon/CAREER_TIMELINE.md')
    assert 'Chicago 진입' in canon and '정확 순번' in canon and 'HOLD' in canon
    assert '기존 `Atlanta 5시즌' in canon and '폐기 분기' in canon
    r=routine();assert r==FIXED_ROUTINE,'Carry options/bonus/important-choice authority changed'
    return old,r


def raw_evidence(old):
    result=[]
    for x in RAW:
        b=Path(x['cache_path']).read_bytes();assert hashlib.sha256(b).hexdigest()==x['raw_sha256'],x['id']
        assert len(b)==x['bytes'] and x['http_status']==200
        t=' '.join(plain(b).split())
        if x['id']=='NBA_CAP2022':
            for token in ['123.655','150.267','10.490','6.479','5.401','July 6']:assert token in t,token
        if x['id']=='NBA_CAP2017':assert '99.093' in t
        if x['id']=='NBA_CAP2018':assert '101.869' in t
        if x['id']=='COBY_OPTION2021':assert 'fourth' in t and 'Coby' in t and '2022-23' in t
        if x['id']=='ziaire-williams':assert all(z in t for z in ['$4,591,680','$4,491,680','$100,000'])
        if x['id']=='alex-caruso':assert '$9,030,000' in t
        result.append(copy.deepcopy(x))
    for x in old['raw_body_observations'][:6]:
        b=Path(x['cache_path']).read_bytes();assert hashlib.sha256(b).hexdigest()==x['raw_sha256']
        y=copy.deepcopy(x);y['classification']='REUSED_VENDOR_HISTORICAL_INPUT_NOT_LEAGUE_LEDGER';result.append(y)
    assert len(result)==12
    return result


def rule_evidence():
    raw=CBA.read_bytes();assert hashlib.sha256(raw).hexdigest()==CBA_SHA
    doc=fitz.open(stream=raw,filetype='pdf');pages=[]
    for n in [54,55,57,64,65,208,209,239,240,241,249,250,292,293,294,310,311,312,559,560,561]:
        t=doc[n-1].get_text().replace('\r\n','\n').replace('\r','\n')
        pages.append({'PDF_1based':n,'fitz_text_LF_sha256':hashlib.sha256(t.encode()).hexdigest()})
    def has(n,t):assert t in ' '.join(doc[n-1].get_text().split()).replace('one- half','one-half'),(n,t)
    has(55,'first Season covered');has(55,'shall be deemed amended');has(561,'1,600,520');has(561,'2,072,867')
    has(292,'following business day');has(294,'eighty percent');has(294,'one hundred twenty percent')
    has(240,'one-half the percentage');has(240,'outstanding Qualifying Offer');has(241,'outstanding Required Tender to a First Round Pick')
    has(311,'Starter Criteria');has(311,'ninth player');has(311,'fifteenth player')
    return {'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf',
        'raw_cache_path':str(CBA),'raw_sha256':CBA_SHA,'pages':pages,
        'extraction':'PyMuPDF get_text default; UTF8;CRLF/CR normalizedLF; pagehash is extractedtext, not rawPDF',
        'applicable_rules':'2017 CBA for2022–23. LONG_CORE_CBA_INPUTS references effective2023-07-01; its new second-apron and SecondRoundPickException are not applied here.',
        'minimum':'II6a/d and ExC PDF561: contract signing-year scale, later credited YOS/Year2 and statutory upward amendment.',
        'options':'VIII1a PDF292: signed notice during allowed post-season window throughOct31, moved to next business day forweekend/holiday; October1 working option realization is permitted, actual receiptnull.',
        'FA_QO':'VII4d and XI1c: capholds differ from salary, QO and firstrefusal. Starter criteria depend on2021–22 actual authored stats still unselected.',
        'apron':'VII6m3: excludes ordinary FAhold/unsigned1Rhold/unusedexception/emptyrosterhold, retains outstanding QO/FirstRefusal/RequiredFirstTender and youngFAfloor/Unlikely/grievance exposure.',
        'stretch':'VII7d6 PDF249–250: prior admitted public stretched groupscreen may be carried as an annual conservative ceiling; no new unreported settlements/waivers are invented.'}


def carry_rows():
    assert FIXED_CARRY=={'Markkanen':18360000,'Caruso':9030000,'LaMelo Ball':7775400,'Coby White':7413955,'Chris Duarte':4591680},'Source-carry actor/year/value changed'
    assert MIN_ROWS=={'Green':(3,1600520),'Joe Wieskamp':(1,1378242),'Tony Bradley':(5,1795015),'Stanley Johnson':(7,2072867),'Denzel Valentine':(6,1933941)},'ExC/YOS/contractYear mapping changed'
    rows=[{'player':p,'2022_23_screen_upper_usd':v,'source_type':'M1_AUTHOR_SELECTED' if p=='Markkanen' else 'REVIEWED2021_ROUTINE_CARRY_PLUS_PUBLIC_ROOKIE_TEMPLATE',
        'actual_contract_amount_certified':False} for p,v in FIXED_CARRY.items()]
    for p,(yos,base) in MIN_ROWS.items():
        q=Fraction(base*CAP21,CAP17);lo=q.numerator//q.denominator;hi=ceil(q)
        rows.append({'player':p,'credited_2022_23_YOS':yos,'contract_year':2,
            'contract_signing_scale_capyear':'2021-22','ExC2017Year2_usd':base,
            'unrounded_statutory_scale_proxy':ratio(q),'integer_proxy_interval':[lo,hi],
            'rounding_screen_allowance_usd':ROUNDING_SCREEN,'2022_23_screen_upper_usd':hi+ROUNDING_SCREEN,
            'exact_NBA_rounding_algorithm_or_cents_certified':False,
            'screen_condition':'Actual applicable official signing-year Year2 tableamount must lie at/below this widened numeric screen. Exact statutory table L remains symbolic, not replaced by a picked dollar.',
            'statutory_salary':'L_2021_22(YOS='+str(yos)+',Year2); no new bonus. II6d automatically raises any too-low prior amount.',
            'actual_contract_amount_certified':False})
    assert len(rows)==10 and len({x['player'] for x in rows})==10
    assert sum(x['2022_23_screen_upper_usd'] for x in rows)==57132041
    assert next(x for x in rows if x['player']=='Stanley Johnson')['2022_23_screen_upper_usd']>2351521
    return rows


def expired_inputs():
    return [
        {'player':'LaVine','2021_22_prior_regular_salary':19500000,'existing2022_23_salary':None,
         'original2022_max_contract_reference':37096500,'reference_not_carry_authority':True,
         'new2022_route_selected':False,'normal_Bird_FAhold_loose_upper':37050000,
         'hold_derivation':'1.9*19500000; conservative ordinary fullBird category maximum; actual average-salary branch not guessed. Normalhold is not an apron salary.'},
        {'player':'Protagonist','2018_pick_domain':[16,30],'exact_pick':None,'existing2022_23_salary':None,
         'new2022_route_selected':False,'old_candidates':['E1_2021_EXTENSION','E2_2022_DIRECT_BIRD','E3_2022_BIRD_MAX','E4_ONE_YEAR_QO'],
         'candidate22m_not_selected':True,'normal_FAhold':'min(2022MaximumSalary,max(rookie250or300percent*actualFourthYearSalary,applicableMinimum)); no ATL30 or Hutchison dollar substitution',
         'outstanding_QO_or_FirstRefusal':None,'rookie_starter_test_2021_22_selected':False},
        {'player':'Wendell Carter Jr.','2021_22_prior_regular_salary':6920027,'existing2022_23_salary':None,
         'new2022_route_selected':False,'old_candidates':['CX1_50m','CX2_40m','CX3_60m','CX4_RFA'],
         'original_ORL14_15m_extension_not_copied':True,'normal_Bird_FAhold_loose_upper':20760081,
         'hold_derivation':'3*6920027 loose rookie-Bird upper; no2021 extension is selected. QO/StarterCriteria remain a function.'},
        {'player':'Thaddeus Young','2021_22_prior_regular_salary':14190000,'prior_performance_earned_interval':[0,1000000],
         'existing2022_23_salary':None,'new2022_route_selected':False,'normal_Bird_FAhold_loose_upper':28861000,
         'hold_derivation':'1.9*(14190000+1000000); preserve uncertain earnedperformance rather than importing actual TOR8m contract.'},
        {'player':'Tomas Satoransky','2021_22_prior_regular_salary':10000000,'existing2022_23_salary':None,
         'new2022_route_selected':False,'normal_Bird_FAhold_loose_upper':19000000,
         'hold_derivation':'1.9*10000000 loose ordinaryBird upper; original2019three-year term ends. No laterwaiver/re-signing salary identity is copied.'}]


FIXED_EXPIRED_INPUTS=copy.deepcopy(expired_inputs())


def build():
    old,r=fixed_inputs();raw=raw_evidence(old);rules=rule_evidence();rows=carry_rows();exp=expired_inputs()
    assert exp==FIXED_EXPIRED_INPUTS,'Expired existing salaries/FAhold/important-choice mapping changed'
    assert [x['player'] for x in exp]==EXPIRED and all(x['existing2022_23_salary'] is None for x in exp)
    core=sum(x['2022_23_screen_upper_usd'] for x in rows)
    apron_amount=Fraction((APRON21-TAX21)*(2*CAP21+CAP22-CAP21),2*CAP21)
    legal_apron_proxy=TAX22+apron_amount
    conservative_apron_screen=(legal_apron_proxy.numerator//legal_apron_proxy.denominator//1000)*1000
    assert conservative_apron_screen==156982000
    legacy_stretch=previous.STRETCH_SCREEN;camp=previous.CAMP_RESERVE
    assert legacy_stretch==16371000 and camp==4372601
    qo_each=CAP22//4
    screen=core+legacy_stretch+camp+2*qo_each
    assert screen==139703142 and conservative_apron_screen-screen==17278858
    return {'id':'CHICAGO_2022_23_APPROVED_CORE_CONTRACT_EXECUTION_2026_10_07','schema':'APPROVED_CORE_CARRY_AND_NEXT_CAPYEAR_INPUT_SCREEN_V1',
        'status':'INDEPENDENTLY_REVIEWED_PARTIAL_CORE_CARRY_AND_BOUNDED_COST_INPUTS',
        'source_main_snapshot':BASELINE,'source_sha256':{**PINS,SELF:sha(SELF)},'source_hash_method':'UTF8BOMstripped;CRLF/CRtoLF',
        'raw_sources':raw,'primary_rule_evidence':rules,
        'retrieval_notes':[{'id':'NBA_CAP2022_initial_defaultUA_attempt','http_status':403,'cache_path':None,'body_used':False,'retry':'One MozillaUA retry yielded pinned200 body.'}],
        'source_authority':{'M1_direction_selected':True,'A_growth_core_Caruso_direction_selected':True,
            'Caruso_terms':'Reviewedadmitted2021routine implementation, not actualleague contract proof.',
            'old_contract_sequence':'Conditionalcomparisons; not a producer of approved2022 existing salaries.',
            'obsolete_ATL30_landing':'Rejectedhistory; currentChicago late1R exactpickHOLD. No new exact2018pick choice.',
            'new_exact_author_lock':False},
        'calendar_and_rules':{'capyear':['2022-07-01','2023-06-30'],'CBA':'2017',
            'official_cap':CAP22,'official_tax':TAX22,'official_NTMLE':10490000,'official_TMLE':6479000,'official_room_MLE':5401000,
            'official_capyear_effective_time':'2022-07-01 00:01 ET','official_FA_negotiation_start':'2022-06-30 18:00 ET','official_moratorium_end':'2022-07-06 12:00 ET',
            '2021_NTMLE_hardcap_end':'2022-06-30','2022_hardcap_trigger_selected':False,
            'apron_unrounded_primary_rule_proxy':ratio(legal_apron_proxy),
            'reported_secondary_apron_reference':156983000,'2022_NBA_PR_published_apron':False,
            'conservative_conditional_apron_screen':conservative_apron_screen,
            'actual_rounding_or_secondary_reference_officially_certified':False,
            'second_apron_or_new2023_second_round_exception_applied':False},
        'routine_carry_candidate':r,'core_carry_rows':rows,'expired_or_unselected_new_contract_inputs':exp,
        'QO_function':{'teams':['Chicago'],'eligible_candidates':['Protagonist','Wendell Carter Jr.'],
            'conditional_on_no2021_extension_and_timely_2022_QO':True,
            'qualifying_offer_and_2021_22_stats_selected':False,'deadline_or_receipt_certified':False,
            'statutory_test':'XI1c: ownrookiefourthsalary*scaleQO%; pick16–30 starter⇒ninthpick120%; pick7nonstarter⇒min(ownQO,fifteenthpick120%). 41starts/2000minutes fourthyear or third/fourthmean; not inferred from2020–21 alone.',
            'broad_screen_per_candidate':qo_each,
            'screen_not_actual_QO_or_salary':'At/below25%cap only a loose rookiecohort cost screen. Exact QO must be computed from admitted rookie scale and2021–22 stats; screen does not select acceptance.'},
        'six_category_next_year_map':[
            {'id':'C1_CURRENT_AND_ADDITIONS','carried_core_players':10,'new_expired_contract_paths':5,'new_contract_or_bonus_cost':'X_NEW>=0,unselected; cannot copyold148806968aggregate'},
            {'id':'C2_FORMER_PLAYERS','admitted_prior_future_stretch_annual_screen':legacy_stretch,'past_camp_full_cash_overreserve':camp,
             'ordinary_legacy_contracts':'Use reviewed13namedordinaryendpoints ending no later2020–21; term-end is not zero payment. Priorstretchscreen retained; no new unreported resolution selected.',
             'new2021_22_waiver_or_settlement_selected':False,'actual2022_dead_salary_or_camp_charge_certified':False},
            {'id':'C3_FREE_AGENT_AMOUNTS','normal_cap':'RemainingBirdholds/youngFAfloors/QO/firstrefusal as rulefunctions until validrenounce/newcontract; expired salary not0 caphold.',
             'apron':'NormalFAholdexcluded; greater outstanding QO/firstrefusal andyoungFAfloor included. Dotson/CookTW expiry/tender classification must be joined; no newstandardUPC selected.'},
            {'id':'C4_DRAFT_ROOKIES','2022_pick_control_or_selection_complete':False,
             'normal_cap':'Unsigned1Rscalehold remains whereowned; no2021frozen60-to2022draftcopy.',
             'apron':'Unsigned1Rholdexcluded; outstandingRequiredFirstTenderincluded. X_TENDER>=0 not silently0.',
             'Simonovic':'PriorAug12+reviewpendingconditionalcontinuation candidate stays noNBAUPC throughJune30,2022. New2022–23NBAUPC/Tender/foreignwindow needs later join, not slot16 automatically.'},
            {'id':'C5_INCOMPLETE_ROSTER','offseason_carried_standard_players':10,'whole2022_standard15_selected':False,
             'normal_cap':'Applicable minimum-roster capcharge below12 standard contracts; exactnewrookies/FA/contracts affect it.',
             'apron':'Incomplete-roster capcharges excluded underVII6m3; this does not waive regularseason minimumregistered/active-list rules.'},
            {'id':'C6_UNUSED_EXCEPTIONS','2022_NTMLE_nominal':10490000,'2022_TMLE_nominal':6479000,'2022_ROOM_nominal':5401000,
             'normal_cap':'Preserve/lapse/renounce each legallyavailableexception underVII6m; availability cannot be inferred from just10core salaries.',
             'apron':'Unusedexceptionexcluded; 2021CarusoNTMLEsalarycarries but expired2021unusedNTMLE/hardcap do not create2022trigger.'}],
        'bounded_pre_new_contract_screen':{'classification':'CONDITIONAL_ARITHMETIC_SUFFICIENT_TEST_NOT_WHOLE_COST_PASS',
            'stage':'2022capyear opening with selected2021core carried, before optional new2022FA/rookieUPC transactions',
            'core_numeric_screen':core,'prior_stretch_screen':legacy_stretch,'retained_past_camp_cash_overreserve':camp,
            'two_RFA_QO_screen_reserve':2*qo_each,'total_screen_before_remaining_X':screen,
            'remaining_X':'All applicable tender/youngFAfloor/new2022contract/Unlikely/grievance/otherselectedcurrentcost increments not already reserved; X>=0, exactvalueunselected.',
            'conditional_apron_sufficient_requirement':'X<=17278858 AND each actual statutoryyear2minimum<=its10-dollar widenedproxy screen, AND all admitted prior categories remain within preservedpublicfamily.',
            'conditional_apron_margin_before_X':conservative_apron_screen-screen,
            'normal_cap_or_tax_headroom_not_apron_margin':True,'normal_cap_complete':False,'whole_apron_complete':False,
            'screen_rounding_condition_is_not_new_gate':'Exact official scale or independentlysupported tighter rounding can replace this provisionalscreen; it is not a demand for privatecontracts.'},
        'summary':{'approved_core_carry_rows':10,'carry_proxy_plus10_screen_usd':core,
            'expired_unselected_new_contract_paths':5,'six_categories_mapped':6,'raw_observations':12,'CBA_pages':len(rules['pages']),
            'conditional_pre_new_contract_screen_usd':screen,'conditional_apron_residual_X_usd':conservative_apron_screen-screen,
            'partial_source_supported_execution_inputs_prepared':True,'whole2022_23_cost_or_roster_closed':False,
            'new_author_locks':0,'REGISTER_promotions':0,'macro3_complete':False},
        'next_named_inputs':[
            {'id':'CORE_LONGTERM_CHOICES','type':'IMPORTANT_UNSELECTED_DIRECTION','next':'ResolveP E1–E4/CarterCX1–4 andLaVine2022term/pay policy in concretecomparison; notautomaticroutineexistingcontracts.'},
            {'id':'2022_DRAFT_AND_TENDERS','type':'FINITE_PUBLIC_CONTROL_AND_CHOICE_JOIN','next':'Join2022origin/control/protections beforeUPC/RequiredFirstTender cost; leaveintegercentnewUPCchoice null.'},
            {'id':'TW_EXPIRY_AND_QO','type':'ROUTINE_LEGAL_CLASSIFICATION','next':'JoinDotson/Cook creditedYOS+one/two-yearTW tenure toXI1c standardvsTWQO; applicablefuturewindow thenroutinecandidate noactualreceiptgate.'},
            {'id':'MINIMUM_SCALE_ROUNDING','type':'PUBLIC_NUMERIC_REFINEMENT_NOT_PRIVATE_GATE','next':'Getpublished2021signing-yearYear2minimumtable or independentstandardrounding toreplace+10screen. Stanley2moldreserve is below2.351521mproxy.'},
            {'id':'NEXT_CAPYEAR_COST_FAMILY','type':'FOLLOWING_FINITE_PRODUCER','next':'Consumechosencontracts/draft/tender/FAevents into sixcategorydatedfamily; untilthenmissingX is retainedsymbolically.'}],
        'scope':{'actual_contract_receipts_consents_or_private_ledger_certified':False,'2021_22_or2022_23_season_selected':False,
            'wholemacro3':False,'independent_review_completed':True,'new_important_direction_selected':False},
        'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}


def validate(o):
    try:return [] if o==build() else ['Carry/rule/cost/source/authority differ from full source-bound reconstruction']
    except (AssertionError,KeyError,ValueError,TypeError,OSError) as e:return [str(e)]


def markdown(o):
    lines=['# Chicago2022–23: 승인 코어 이월과 다음 캡연도 비용 입력','',
        '`'+o['status']+'`. M1/A 승인 방향에서 이월 가능한10명 계약을 분리했습니다. LaVine·주인공·Carter·Young·Satoransky의 새 계약5개는 아직 선택하지 않았습니다. 전체비용·15+2·시즌·macro3·새정본·원고 완성은 아닙니다.','',
        '## 실제 회수한 수치와 권위','',
        'M1의2022–23 Markkanen **$18,360,000**은 작가 선택입니다. Caruso **$9,030,000**은 검문된2021 routine4년5% 인상 구현의 이월값입니다. 원실제 계약 접수/수락 인증과 다릅니다. Coby4년차/LaMelo3년차 옵션은2021-10-01 적법 signednotice 후보를 구성하며 실제수신 사실을 주장하지 않습니다. 현재Chicago late1R 주인공 정확2018순번은HOLD로 보존합니다. 폐기된ATL30 또는 Hutchison 급여를 복사하지 않습니다.','',
        '|이월 선수|2022–23 비용 screen($)|구분|','|---|---:|---|']
    for x in o['core_carry_rows']:lines.append('|'+x['player']+'|'+format(x['2022_23_screen_upper_usd'],',')+'|'+('2021서명Year2 법정scale proxy+10' if 'contract_year' in x else 'M1/기존routine·rookie template')+'|')
    lines += ['',
        '**10명 screen합계 $57,132,041.** II6는 최초서명2021–22 scale을 전체계약에 적용하므로2022 신규계약 minimum표로 교체하지 않습니다. ExC2017 Year2에112.414/99.093 비율을 적용한 법정실수 proxy를 계산하고 각 minimum에$10의 넓은 반올림 screen을 두었습니다. 실제NBA표의 반올림 알고리즘/정확센트는 미인증이며 해당법정표가 screen이하라는 수치조건을 명시합니다. 선택금액이나 전체법적 PASS로 표시하지 않습니다. Stanley의 기존$2m replacement reserve는 Year2 proxy 약$2.351521m보다 작아 그대로 이월하면 안 됩니다.','',
        '원Ziaire#10 표에는2022–23 총$4,591,680 안에 $100,000 performance가 있습니다. 숫자는#10 rookie120% 비용 template로만 사용하며 Duarte에게 그 bonus나 실제원계약을 복사하지 않습니다. 기존 Caruso 원표는9.03m과 일치하지만 이번 권위는 승인routine입니다.','',
        '[NBA2022 공식발표](https://pr.nba.com/nba-salary-cap-2022-23-season/): cap **$123.655m**, tax **$150.267m**, NTMLE **$10.490m**. TMLE/room은 별도입니다. 공식발표에 apron은 없습니다. CBA VII6m3의 전년apron−tax/half-cap-growth로 unrounded apron proxy를 산출하고 보수적 **$156.982m screen**을 사용합니다. 기존 secondary$156.983m를 NBA공식 본문인 것처럼 인증하지 않습니다.','',
        '2021CarusoNTMLE hardcap은2022-06-30 종료합니다. 이월Caruso급여가2022새NTMLE사용/새hardcap을 자동발동하지 않습니다. 2023CBA/secondapron/새SecondRoundPickException도2022–23에 소급하지 않습니다.','',
        '## 만료·후보를 비용0으로 바꾸지 않기','',
        '|선수|2022 새계약 입력|기존 비교값 처리|','|---|---|---|',
        '|LaVine|기간·연봉 미선택|37.0965m 원역사 max는 비교, existingcarry 아님|',
        '|주인공|E1–E4 미선택|22m 후보/ATL30 계약 미복사|',
        '|Carter|CX1–4 미선택|ORL14.15m extension 미복사|',
        '|Young|새계약 미선택|14.19m+성과0..1m 직전계약의 FAhold 분기 보존|',
        '|Satoransky|새계약 미선택|원3년기간 종료, 과거waive/re-sign 분할 미복사|','',
        '만료는 futureexisting salary가 없다는 뜻이며 caphold/새급여/과거채무0과 다릅니다. ordinary Birdhold는 normalcap에 남고 apron에서는 제외됩니다. 주인공/Carter의 outstandingQO/FirstRefusal은 apron에 남습니다. XI1c의41선발/2,000분 조건은2021–22 또는최근2년 표본이 필요하므로2020–21 결과만으로 대신하지 않습니다.','',
        '## 다음 유한 비용 증인에 공급하는 충분조건','',
        '6범주를 각기 연결했습니다: current+newcontract, formerplayer, FA/QO, draftrookie/tender, incomplete roster, unusedexceptions. 정상cap의 unsigned1Rhold/예외/빈자리와 apron의 outstandingRequiredFirstTender/youngFAfloor를 구분합니다. unsigned≠비용0이고 roster10은 offseason 이월상태일 뿐 정규시즌 최소명단 규칙 면제가 아닙니다.','',
        '보존된 priorstretch $16.371m와 과거camp fullcash$4.372601m overreserve를 계속 넣고, P/Carter QO 두개에 각25%cap의 넓은 screen을 예약하면 **$139,703,142**입니다. 정확QO 또는새계약 선택이 아닙니다. 미포함2022tender·youngFAfloor·신규계약·bonus·grievance 순증액을 **X**로 남깁니다. 위 명시minimum screen조건과 보존category조건 아래 **X≤$17,278,858**이면 보수적apron screen 이내라는 산술 충분조건입니다. X가 실제 이내라고 아직 인증하지 않습니다. normalcap/tax 전체합계나사용가능FA현금으로 읽으면 안 됩니다.','',
        '다음 실제입력은5새계약 중요방향,2022draftcontrol/Tender,Dotson/Cook TW QO 분류, minimum공개표 정밀화입니다. 비공개 장부/실제서류를 새필수gate로 요구하지 않습니다. 기존148.806968m 조건부합계를 wholePASS로 복사하지 않습니다.','',
        '## 원천·검문','',
        '기준 main `'+BASELINE+'`; 고정10repository pins+SELF, 새6raw/재사용6raw와CBA21쪽 지문을 직접검사합니다. 초회NBA defaultUA403은 미사용이며 1회200회수한 실제원본문만 원천에 둡니다. NBAhosted Coby옵션 기사는AP본문이며 구단원pressrelease로 표기하지 않습니다. selftests는 독립검문으로 계수하지 않습니다.','',
        '[현행전체로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 아래 표는 본leaf의 단계위치를 표시하며 중앙현황을 수정하지 않습니다.','',
        '|번호|묶음|상태|','|---|---|---|','|1|2020 draft연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23 거래·계약|2022–23 승인core 이월/미선택5계약 입력|','|4|장기커리어|후속설계|','|5|결말·전체구조|전체기능표 미완료|','|6|집필규격·Context Pack|누적기능등록 계속/Pack0|','|7|통합·독립·작가승인|최종게이트 CLOSED|','',
        '미완료큰묶음 **5**. `v0.30 PARTIAL`/게이트`CLOSED`/실제Pack0/원고0/원장승격0.']
    return '\n'.join(lines)+'\n'


def self_test(o):
    hits=[]
    for label,mut in [
        ('M1_wrong_year',lambda x:x['core_carry_rows'][0].update(**{'2022_23_screen_upper_usd':19720000})),
        ('oldLaVine_carry',lambda x:x['expired_or_unselected_new_contract_inputs'][0].update(existing2022_23_salary=37096500)),
        ('Stanley2m',lambda x:next(z for z in x['core_carry_rows'] if z['player']=='Stanley Johnson').update(**{'2022_23_screen_upper_usd':2000000})),
        ('2023rule',lambda x:x['calendar_and_rules'].update(CBA='2023')),
        ('oldhardcap',lambda x:x['calendar_and_rules'].update(**{'2022_hardcap_trigger_selected':True})),
        ('missingXzero',lambda x:x['bounded_pre_new_contract_screen'].update(remaining_X=0)),
        ('wholePASS',lambda x:x['summary'].update(whole2022_23_cost_or_roster_closed=True))]:
        b=copy.deepcopy(o);mut(b);assert validate(b),label;hits.append(label)
    for label,mut in [
        ('constructor_ATL30',lambda x:x.update(P2018_team='Atlanta',P2018_pick_domain=[30,30])),
        ('constructor_autoselectfive',lambda x:x.update(new_LaVine_Protagonist_Carter_Young_Satoransky_contract_selected=True)),
        ('constructor_rookie_notice_missing',lambda x:x['LaMelo_third_year_option'].update(signed_player_notice=False))]:
        b=routine();mut(b)
        with patch(__name__+'.routine',return_value=b):
            try:build()
            except AssertionError:hits.append(label)
            else:raise AssertionError(label)
    b=copy.deepcopy(FIXED_CARRY);b['Caruso']+=1;b['Coby White']-=1
    with patch(__name__+'.FIXED_CARRY',b):
        try:build()
        except AssertionError:hits.append('constructor_same_total_wrong_carry')
        else:raise AssertionError('same_total_wrong_carry')
    b=expired_inputs();b[0]['new2022_route_selected']=True
    with patch(__name__+'.expired_inputs',return_value=b):
        try:build()
        except AssertionError:hits.append('constructor_expired_route_selected')
        else:raise AssertionError('expired_route_selected')
    return hits


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();o=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
    if a.check:assert not validate(load(OUT));assert text(MD)==markdown(o)
    tests=self_test(o) if a.self_test else []
    print(json.dumps({'current':True,'summary':o['summary'],'negative_controls':tests},ensure_ascii=False))
