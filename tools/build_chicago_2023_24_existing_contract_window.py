"""Named FY23 carry and usable consensual follow-up functions; no canon adoption."""
from __future__ import annotations
import argparse, copy, hashlib, json, math
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2023_24_existing_contract_window.py'
OUT='simulation/CHICAGO_2023_24_EXISTING_NAMED_CONTRACT_WINDOW.json'
ACTION='research/CHICAGO_2023_FOLLOWUP_FINITE_ACTIONS_2026_10_08.json'
BASELINE='241821ba24936ee788320844822af5a3f32ef69c'
ROOKIE='simulation/CHICAGO_2022_ROOKIE_SELECTED_EXECUTION.json'
OPTIONS='simulation/CHICAGO_2022_ROOKIE_OPTION_WINDOW_JOIN.json'
STAT='simulation/CHICAGO_2023_SELECTED_STAT_CREDIT_AND_QO.json'
LONG='simulation/CHICAGO_LONG_CORE_CBA_INPUTS.json'
PINS={'simulation/CHICAGO_2022_ROOKIE_SELECTED_EXECUTION.json': '3c06967cf8c7171f815819efd3b4a71fb88ac77db3ae8798b34afeeeae93ce1c', 'simulation/CHICAGO_2022_23_NAMED_CONTRACT_WINDOW.json': '21e860056c2654d5e4837911dac39e7f45f4d26388d353bc57594afefcecf1f4', 'simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json': 'e7d0f4b15bc06c7cd16a38d158b38a78871fb7372d412639e33bb20c31d225a7', 'simulation/CHICAGO_2022_ROOKIE_OPTION_WINDOW_JOIN.json': 'e506efd28a54ceb61e34a8dfc107fb82236f783700f3aa610cd68ff4d62ba2cc', 'simulation/CHICAGO_2023_SELECTED_STAT_CREDIT_AND_QO.json': '142a9033d9c69b7ed96e176418fc32a7cabfd10f31188928528b22033e3a4d10', 'research/COBY_2023_QO_PRIMARY_INPUT_2026_10_07.json': 'ee2c866fb0a098c1d09f43f2288b9df27f0d20db2c4630e99353fba95612eb2e', 'research/MACRO3_2023_CBA_BOUNDARY_BRIDGE_2026_10_07.json': '404fde08b9d5fc9168b64f082c57a4ed6dff14711cf4d5990839267dc8a878f4', 'research/MACRO3_2023_CBA_BOUNDARY_PRIMARY_SOURCES_2026_10_07.json': '59b03c494187eb29177640806ae97427a837abff38bf4516f588758fc87a0112', 'simulation/CHICAGO_LONG_CORE_CBA_INPUTS.json': '7985e65cb5e184356aead888d4f016aca187dd2dd3185ea6de76527a6937fe0c', 'research/SIMONOVIC_2022_23_SELECTED_RIGHTS_FAMILY_2026_10_07.json': 'c404fc401f6c30809ed5098663dd2b277b1c4cb7844d15c697991460f1290ac4', 'research/CHICAGO_2022_23_APPROVED_CORE_CONTRACT_EXECUTION_2026_10_07.json': '2cc7aeaeaef530f1c3fac5846348792c3d516eb1479af1ce56617deb2e7cb2b5', 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json': '253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088', 'canon/DELEGATED_2022_DRAFT_AND_CHICAGO_ROOKIE_DECISION_2026_10_08.json': 'a32dfc265a7250bc89df366c14b43444645438675674f4be66feda2b6a053eba', 'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2'}
LAW=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-2023-cba-boundary-20261007/cba2023.pdf')
OLD=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
RAW={str(LAW):'bf178ca0f2d64f9dfe6fde095d3ae43d576b12e19ce7a679618d632584f7ab32',str(OLD):'66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'}
LIVE={
 'Lauri Markkanen':(19720000,2024,'M1_FULL_BIRD_2021_YEAR3'),
 'Alex Caruso':(9460000,2024,'NTMLE_2021_YEAR3_NO_NEW_EXCEPTION_USE'),
 'LaMelo Ball':(9835881,2023,'2020_PICK4_EXERCISED_FOURTH_RSC_YEAR'),
 'Chris Duarte':(4810200,2023,'2021_PICK10_EXERCISED_THIRD_RSC_YEAR'),
 'Wendell Carter Jr.':(13050000,2025,'CX1_EXTENSION_YEAR2'),
 'Protagonist':(23760000,2025,'E2_BIRD_YEAR2'),
 'Zach LaVine':(40064220,2026,'BIRD5_YEAR2_FUTURE2026_PO_UNSELECTED'),
 'Thaddeus Young':(8000000,2023,'2022_BIRD2_YEAR2_NO_NEW_BONUS'),
 'Walker Kessler':(3350760,2023,'2022_PICK18_RSC_SECOND_GUARANTEED_YEAR')}
EXPIRED=['Coby White','Javonte Green','Joe Wieskamp','Tony Bradley','Denzel Valentine','Tomas Satoransky']
TW=['Devon Dotson','Tyler Cook']
MIN_BASE=[1017781,1637966,1836090,1902133,1968175,2133278,2298385,2463490,2628597,2641682,2905851]

def norm(t):return t.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(norm((ROOT/p).read_text(encoding='utf-8-sig')).encode()).hexdigest()
def serial(o):return json.dumps(o,ensure_ascii=False,indent=2)+'\n'
def physical():
    for p,h in PINS.items():assert sha(p)==h,'Pinned source changed: '+p
    return {p:json.loads((ROOT/p).read_text(encoding='utf-8-sig')) for p in PINS if p.endswith('.json')}
def source_inputs():return physical()
def assert_sources(s):
    assert s==physical(),'Source semantic objects differ from pinned source'
    rows=s[ROOKIE]['working_execution']['registered_contracts']
    assert len(rows)==17 and {x['player'] for x in rows}==set(LIVE)|set(EXPIRED)|set(TW)
    assert sum(x['roster_type']=='STANDARD' for x in rows)==15
    assert 'Stanley Johnson' not in {x['player'] for x in rows}
    notices=s[OPTIONS]['preserved_parent_notices']
    assert [(x['player'],x['added_season'],x['date']) for x in notices]==[('LaMelo Ball','2023-24','2022-10-01'),('Chris Duarte','2023-24','2022-10-01')]
    q=s[STAT]['ordinary_QO_component_function']
    assert q['selected_starter'] is False and q['nonstarter_sufficient_integer_cost_upper']==7744602
    assert q['own_sufficient_integer_cost_upper']==9942120 and not q['original_exact_components_selected']
    assert s[STAT]['selected_policy']['Coby_starter_nominations_per_game']==0
    assert s[STAT]['selected_policy']['overtime_periods_selected_per_regular_game']==0

def primary():
    import fitz
    result=[]
    for p,ns,role in [(OLD,[311,312,313,314,315,316,317],'OPERATIVE_THROUGH_JUNE30_2023_QO_ISSUANCE'),(LAW,[31,32,33,37,57,58,60,62,64,65,76,77,78,89,90,211,212,214,215,219,220,234,240,241,242,255,256,270,278,314,316,317,319,322,323,324,338,339,340,342,343,344,453,454,584,631,632],'OPERATIVE_FROM_JULY1_2023')]:
        assert hashlib.sha256(p.read_bytes()).hexdigest()==RAW[str(p)]
        d=fitz.open(p);texts={n:norm(d[n-1].get_text()) for n in ns}
        flat={n:' '.join(t.split()) for n,t in texts.items()}
        if p==LAW:
            assert 'three (3) Salary Cap Years' in flat[78]
            assert '$90,000' in flat[339] and '2023-24' in flat[339]
            assert '2023-24 Salary Cap Year' in flat[58] and 'twelve (12)' in flat[453]
            assert 'July 15' in flat[323] and 'September 5' in flat[323]
            assert 'six (6) Seasons' in flat[319] and 'following business day' in flat[584]
            assert '2,946,800' in flat[631] and '2023-24 Salary Cap' in flat[32]
        else:assert 'June 29' in flat[315] and 'Two-Way Annual NBADL Salary' in flat[312]
        result.append({'cache_path':str(p),'raw_sha256':RAW[str(p)],'role':role,'PDF1based_normalized_fitz_text_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest() for n,t in texts.items()}})
    # Two same-rank vendor observations support the existing public numeric ceiling,
    # without copying their individual UPC/bonuses or option dates into Chicago.
    from bs4 import BeautifulSoup
    sources=physical()['research/CHICAGO_2022_23_APPROVED_CORE_CONTRACT_EXECUTION_2026_10_07.json']['raw_sources']
    for ident,value in [('patrick-williams_2021_ROW',9835881),('ziaire-williams',4810200)]:
        x=next(x for x in sources if x['id']==ident);p=Path(x['cache_path'])
        assert hashlib.sha256(p.read_bytes()).hexdigest()==x['raw_sha256']
        rows=[t.get_text(' | ',strip=True) for t in BeautifulSoup(p.read_bytes(),'html.parser').find_all('tr')]
        row=next(t for t in rows if t.startswith('2023-24 |'))
        assert f'${value:,}' in row
        result.append({'url':x['url'],'cache_path':str(p),'raw_sha256':x['raw_sha256'],'observed_row':row,'role':'VENDOR_SAME_RANK_SCALE_CEILING_ONLY_NOT_SAME_UPC_OR_BONUS_OR_NOTICE'})
    return result

def construct(s):
    result=[]
    for x in s[ROOKIE]['working_execution']['registered_contracts']:
        name=x['player'];live=name in LIVE
        row={'player':name,'holder':'CHI','previous_roster_type':x['roster_type'],'July1_2023_live':live,
          'current_UPC_STD_slot':int(live),'current_UPC_TW_slot':0,'prior_source_pointer':ROOKIE+'#/working_execution/registered_contracts/'+str(len(result)),
          'old_Gamma_and_full_original_components_preserved':True,'actual_private_contract_or_receipt_certified':False,
          'fiscal_end_is_not_exact_service_term_end':True,'new_assignment_selected':False}
        if live:
            v,y,m=LIVE[name];row.update(mechanism=m,FY23_salary_plus_all_performance_upper=v,
                normal_salary_upper=v,apron_salary_upper=v,last_selected_salary_capyear_start=y,
                last_selected_fiscal_year_end=f'{y+1}-06-30',FY23_covered_capyear='2023-07-01..2024-06-30',
                source_amount_is_exact_actual_private_cents=False,term_support=x.get('term_support',x['source_pointer']),
                future_option_outcome=None if name=='Zach LaVine' else 'NO_NEW_OPTION_EXERCISE_IN_THIS_PROJECTION')
        else:row.update(mechanism='EXPIRED_PRIOR_UPC_NO_NEW_UPC_AUTOMATIC',previous_fiscal_salary_coverage_end='2023-06-30',
                new_salary=None,FA_or_QO_hold_not_zero=True,service_completion='Preserved rendered-services family; no actual private completion receipt certificate')
        result.append(row)
    return result

def assert_contract_rows(rows,s):
    original=s[ROOKIE]['working_execution']['registered_contracts']
    assert len(rows)==17 and [x['player'] for x in rows]==[x['player'] for x in original]
    for row,src in zip(rows,original):
        name=row['player'];assert row['holder']=='CHI' and row['previous_roster_type']==src['roster_type']
        assert row['July1_2023_live']==(name in LIVE)
        assert row['current_UPC_STD_slot']==int(name in LIVE) and row['current_UPC_TW_slot']==0
        assert row['old_Gamma_and_full_original_components_preserved'] and not row['actual_private_contract_or_receipt_certified']
        assert row['fiscal_end_is_not_exact_service_term_end'] and not row['new_assignment_selected']
        if name in LIVE:
            value,end,method=LIVE[name]
            assert row['normal_salary_upper']==row['apron_salary_upper']==row['FY23_salary_plus_all_performance_upper']==value
            assert row['mechanism']==method and row['last_selected_salary_capyear_start']==end
            assert row['last_selected_fiscal_year_end']==f'{end+1}-06-30'
            assert row['FY23_covered_capyear']=='2023-07-01..2024-06-30' and row['term_support']==src.get('term_support',src['source_pointer'])
            assert not row['source_amount_is_exact_actual_private_cents']
            if name=='Zach LaVine':assert row['future_option_outcome'] is None
        else:assert row['new_salary'] is None and row['FA_or_QO_hold_not_zero']

def minimum(yos):
    assert type(yos)==int and 0<=yos<=10
    q=Fraction(MIN_BASE[yos]*136021000,123655000)
    return {'statutory_function':f'L_2023_24(YOS={yos},Year1)',
       'baseline_2022_23_ExC_Year1':MIN_BASE[yos], 'cap_adjustment_exact_rational':str(q),
       'conditional_floor_ceil_rounding_screen':[math.floor(q),math.ceil(q)+2],
       'official_rounding_or_actual_cents_certified':False,
       'numeric_screen_condition':'Applicable prepared NBA scale lies inside stated floor..ceil+2. Legal offer itself uses the statutory function, not the proxy.',
       'bonuses':0,'normal_apron_reservation':'Full player cash conservatively reserved; one-year reimbursement and nonrookie apron2YOS adjustments may lower counted Salary, never erase the payment.'}

def checked_minimum(yos):
    m=minimum(yos);q=Fraction(MIN_BASE[yos]*136021000,123655000)
    assert m['statutory_function']==f'L_2023_24(YOS={yos},Year1)' and m['baseline_2022_23_ExC_Year1']==MIN_BASE[yos]
    assert m['cap_adjustment_exact_rational']==str(q) and m['conditional_floor_ceil_rounding_screen']==[math.floor(q),math.ceil(q)+2]
    assert m['bonuses']==0 and not m['official_rounding_or_actual_cents_certified']
    return m

def web_observations():
    """Actual provider body reads; failed direct HTTP bodies never serve as evidence."""
    failed=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-chi-2023-window-20261008/sources.json')
    attempts=json.loads(failed.read_text(encoding='utf-8-sig'))
    assert len(attempts)==3 and all(x['http_status']==403 and not x['adopted_body'] for x in attempts)
    for x in attempts:
        body=Path(x['cache_path']).read_bytes()
        assert len(body)==x['bytes'] and hashlib.sha256(body).hexdigest()==x['raw_sha256']
    return {'classification':'PROVIDER_BODY_READ_OBSERVATIONS_NOT_RAW_HTML',
      'observed_2026_10_08':[
        {'id':'NBA_CAP_2023','url':'https://pr.nba.com/nba-salary-cap-for-2023-24-season-set-at-136-021-million/',
         'provider_ref':'turn2448view1','locator':'June30,2023 release lines14–20',
         'fact':'Cap136021000/tax165294000/firstapron172346000/second182794000; moratoriumendsJuly6noon;NTMLE12405000/TMLE5000000/Room7723000','role':'OFFICIAL_LEAGUE_RULE_CALENDAR_AMOUNTS'},
        {'id':'COBY_MARKET','url':'https://cdn-uat.nba.com/news/nba-offseason-roundup-2023',
         'provider_ref':'turn2446view0','locator':'June30 section lines438–440',
         'fact':'NBA News attributes Coby White three-year $40m agreement report to Adrian Wojnarowski.','role':'SECONDHAND_REPORTED_MARKET_COMPARATOR_NOT_PRIVATE_BASE_BONUS_SPLIT'},
        {'id':'LAMELO_MARKET','url':'https://www.nba.com/news/lamelo-ball-contract-extension-2023',
         'provider_ref':'turn2448view0','locator':'UpdatedJuly7,2023; lines138/148',
         'fact':'Hornets five-year extension reported up to $260m.','role':'REPORTED_MARKET_COMPARATOR_NOT_CHICAGO_ACCEPTANCE_AWARDS_HEALTH'}],
      'direct_HTTP_attempt_metadata_cache':str(failed),'direct_HTTP_attempts':attempts,
      'official_Bulls_Coby_body_verified':False,'failed_bodies_adopted':False}

def policy():
    return {'QO_model_date':'2023-06-28','QO_issuance_deadline':'2023-06-29',
      'QO_issuance_law':'2017_XI4','new_Bird_signing_date':'2023-07-07',
      'Coby':{'mechanism':'DIRECT_FULL_BIRD3_NEW_UPC_NOT_QO_ACCEPTANCE','first_year_range':[11000000,'40000000/3'],
        'recommended_schedule':[12000000,12000000,12000000],'new_performance_signing_trade_loan_buyout_bonuses':0,
        'full_skill_and_injury_protection':True,'options':False,'old_contract_replaced_once':True,
        'Bird_service_capyears':[2020,2021,2022],'rights_not_renounced_before_Bird_signing':True},
      'minimum_renewals':['Javonte Green','Joe Wieskamp','Denzel Valentine','Tomas Satoransky'],
      'minimum_form':'ONE_SEASON_2023_24_STATUTORY_MINIMUM_EXCEPTION_NO_BONUSES_FULL_PROTECTION',
      'Bradley':'NO_NEW_UPC_IN_RECOMMENDED_SLOT_FAMILY; retainFAhold until valid express written renunciation before firstRSC admission',
      'Dotson':'TIMELY_STANDARD_QO_UNACCEPTED_ROFR_AND_COST_RETAINED_NOT_FOURTH_CHI_TW',
      'Cook':'NO_QO_BY_JUNE29_NEW_CONSENSUAL_ONE_SEASON_TW_CONDITIONAL_ELIGIBILITY',
      'rookie_STD_slots_reserved':1,'new_2023_first_rookie_identity_or_rank':None,
      'actual_consent_or_UPC_receipt':None,'canon_selection_of_this_policy':False}

def assert_policy(p):
    assert p['QO_model_date']=='2023-06-28' and p['QO_issuance_deadline']=='2023-06-29' and p['QO_issuance_law']=='2017_XI4'
    assert p['new_Bird_signing_date']=='2023-07-07'
    c=p['Coby'];assert c['mechanism']=='DIRECT_FULL_BIRD3_NEW_UPC_NOT_QO_ACCEPTANCE'
    assert c['recommended_schedule']==[12000000]*3 and c['first_year_range']==[11000000,'40000000/3']
    assert c['new_performance_signing_trade_loan_buyout_bonuses']==0 and c['full_skill_and_injury_protection'] and not c['options']
    assert c['old_contract_replaced_once'] and c['Bird_service_capyears']==[2020,2021,2022] and c['rights_not_renounced_before_Bird_signing']
    assert p['minimum_renewals']==['Javonte Green','Joe Wieskamp','Denzel Valentine','Tomas Satoransky']
    assert p['minimum_form']=='ONE_SEASON_2023_24_STATUTORY_MINIMUM_EXCEPTION_NO_BONUSES_FULL_PROTECTION'
    assert p['Bradley']=='NO_NEW_UPC_IN_RECOMMENDED_SLOT_FAMILY; retainFAhold until valid express written renunciation before firstRSC admission'
    assert p['Dotson']=='TIMELY_STANDARD_QO_UNACCEPTED_ROFR_AND_COST_RETAINED_NOT_FOURTH_CHI_TW'
    assert p['Cook']=='NO_QO_BY_JUNE29_NEW_CONSENSUAL_ONE_SEASON_TW_CONDITIONAL_ELIGIBILITY'
    assert p['rookie_STD_slots_reserved']==1 and p['new_2023_first_rookie_identity_or_rank'] is None
    assert p['actual_consent_or_UPC_receipt'] is None and not p['canon_selection_of_this_policy']

def extension_forms():
    return [{'id':ident,'term':term,'first_extended_capyear':2024,'first_base_function':base,
      'raises':Fraction(8,100).__str__(),'new_bonus':0,'no_options_proposed':True,
      'higher_max_requires_II7_qualifying_awards':higher,'future_awards_selected':False,
      'adds_FY23_salary':0,'new_STD_slot':0,'consent_selected':False,'original_FY23_UPC_unchanged':True}
      for ident,term,base,higher in [('LM1',5,'25% C24; only qualifying HigherMax clause permits30% C24',True),('LM2',4,'25% C24; only qualifying HigherMax clause permits30% C24',True),('LM3',5,'25% C24 fixed',False),('LM4',0,'No extension; 2024 RFA/QO action remains separate',False)]]

def assert_extensions(es):
    assert len(es)==4
    for e,ident,n,h in zip(es,['LM1','LM2','LM3','LM4'],[5,4,5,0],[True,True,False,False]):
        assert e['id']==ident and e['term']==n and e['higher_max_requires_II7_qualifying_awards']==h
        assert e['first_extended_capyear']==2024 and e['adds_FY23_salary']==e['new_STD_slot']==e['new_bonus']==0
        assert e['raises']=='2/25' and e['original_FY23_UPC_unchanged'] and e['no_options_proposed']
        assert not e['future_awards_selected'] and not e['consent_selected']
    assert es[0]['first_base_function']=='25% C24; only qualifying HigherMax clause permits30% C24'
    assert es[1]['first_base_function']==es[0]['first_base_function']
    assert es[2]['first_base_function']=='25% C24 fixed'
    assert es[3]['first_base_function']=='No extension; 2024 RFA/QO action remains separate'

def two_way_routes():
    return {'Devon Dotson':{'prior_CHI_TW_capyears':[2020,2021,2022],'new_CHI_TW_2023_allowed':False,
      'ordinary_QO_family':'2017XI1c(iii) standard one-season applicable minimum with prior-law TWAnnualNBADLSalary protection; no bonus. IssueJune28 within old-law window; do not label new90k rule operativeJune28.',
      'July1_new_90k_rule_is_old_June_offer_fact':False,
      'routes':['Unaccepted valid standardQO: ROFR and max(FAhold,QO,FRN) retained; STD0, TW0',
        'Separate consensual one-season full-protected standard minimum July7: STD1, TW0, replacesQO/hold once and requires freeing named noncore/newrookie slot first'],
      'actual_acceptance':None},
      'Tyler Cook':{'prior_CHI_TW_capyears':[2021,2022],'new_CHI_TW_capyear':2023,
        'YOS3_branch':'CreditedYOS3 and no fourth creditedyear during one-season term; third CHI TW capyear allowed',
        'YOS4_exception_branch':'One-season only; at least one creditedSeason with zero NBA Regular/PlayIn/PO games and onRoster for entireRegularSeason under newII11eii; explicitly admitted fiction condition, not inferred from0minutes',
        'registration_equals_YOS':False,'new_contract_has_standard_conversion_option':True,
        'max_regular_active_games':50,'NBA_postseason_eligible_without_standard_conversion':False,
        'actual_YOS_clinical_or_conversion_receipt':None},
      'new_second_TW_named_option':{'player':'Keon Ellis','not_selected':True,
        'required_condition':'AfterSubsequentDraft2023: notredrafted→X4c RookieFA then lawfulNBAfree-oneSeasonTW ifYOS<4; ifredrafted, otherholder release/ownership mandatory beforeCHI signing; ifX5 foreigncontract actualapplicable rightsclock useX5 not automaticX4 expiry.',
        'old_2022_unaccepted_tender_renews_rights_automatically':False,
        '2023_CHI_redraft_then_required_tender':'Only if independently chosen2023board givesCHI a valid2R; offerinAug22..Sep5, oneSeason statutorymin openatleast earlier(firstRegular-4days,Oct15); not assumed to exist'},
      'legal_max_TW':3,'selected_TW_new_count':0,'recommended_conditional_TW_count':1,
      'third_TW_is_automatically_filled':False}

def assert_tw(t):
    d=t['Devon Dotson'];assert d['prior_CHI_TW_capyears']==[2020,2021,2022] and not d['new_CHI_TW_2023_allowed']
    assert d['actual_acceptance'] is None and not d['July1_new_90k_rule_is_old_June_offer_fact']
    c=t['Tyler Cook'];assert c['prior_CHI_TW_capyears']==[2021,2022] and c['new_CHI_TW_capyear']==2023
    assert c['new_contract_has_standard_conversion_option'] and c['max_regular_active_games']==50
    assert not c['registration_equals_YOS'] and not c['NBA_postseason_eligible_without_standard_conversion']
    assert c['actual_YOS_clinical_or_conversion_receipt'] is None
    assert 'entireRegularSeason' in c['YOS4_exception_branch'] and 'no fourth creditedyear' in c['YOS3_branch']
    e=t['new_second_TW_named_option'];assert e['player']=='Keon Ellis' and e['not_selected'] and not e['old_2022_unaccepted_tender_renews_rights_automatically']
    assert t['legal_max_TW']==3 and t['selected_TW_new_count']==0 and t['recommended_conditional_TW_count']==1 and not t['third_TW_is_automatically_filled']

def cost_state_function(*,N23,A23,R23,expired_holds_normal,expired_holds_apron,new_signed_normal,new_signed_apron,annual_deemed_normal=0):
    """Numeric evaluator only with supplied, nonnegative typed components; no null=0."""
    values=[N23,A23,R23,expired_holds_normal,expired_holds_apron,new_signed_normal,new_signed_apron,annual_deemed_normal]
    assert all(x is not None and Fraction(x)>=0 for x in values),'Every typed monetary input must be supplied, not null-as-zero'
    assert Fraction(R23)<=16371000,'Preserved named stretch family limit exceeded'
    live=sum(v[0] for v in LIVE.values())
    normal=Fraction(live)+sum(map(Fraction,[N23,R23,expired_holds_normal,new_signed_normal,annual_deemed_normal]))
    apron=Fraction(live)+sum(map(Fraction,[A23,R23,expired_holds_apron,new_signed_apron]))
    return {'normal_full_component_upper':str(normal),'apron_full_component_upper':str(apron),
      'tax_Salary_is_not_assumed_equal_to_normal_or_apron':True,'hardcap_trigger':False,
      'apron_excess_is_not_itself_illegality':True,'actual_total_certified':False}

def build():
    s=source_inputs();assert_sources(s);r=construct(s);assert_contract_rows(r,s)
    p=policy();assert_policy(p);es=extension_forms();assert_extensions(es);tw=two_way_routes();assert_tw(tw)
    primary_support=primary();live=sum(v[0] for v in LIVE.values())
    qo=copy.deepcopy(s[STAT]['ordinary_QO_component_function'])
    shared={'baseline_main':BASELINE,'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8_BOM_STRIPPED_CRLF_CR_TO_LF_REPOSITORY_BYTES_EXTERNAL_RAW_SEPARATE',
      'status':'REVIEW_PENDING_CONSTRUCTIBLE_NAMED_PUBLIC_FAMILY_ROUTINE_CANDIDATES',
      'certification':{'independent_review_completed':False,'canon_adoption':False,'actual_private_contract_bonus_receipt_or_player_assent':False,
        'whole_FY23_cost_or_registration':False,'whole_macro3':False,'future_awards_MVP_title_or_franchise_change':False,'new_manuscript':False},
      'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0,'manuscript_allowed':False}
    window={**shared,'id':'CHICAGO_2023_24_EXISTING_NAMED_CONTRACT_WINDOW','snapshot_date':'2023-07-01',
      'primary':primary_support,'web_body_observations':web_observations(),'named_contracts':r,'counts':{'source_STD15_TW2':17,'live_STD':9,'expired_STD':6,'expired_TW':2,'live_TW':0},
      'selected_core_preserved':['Protagonist','LaMelo Ball','Lauri Markkanen','Zach LaVine','Wendell Carter Jr.'],
      'salary_scope':{'live9_normal_and_apron_all_component_upper':live,'bound_not_actual_private_cents':True,
        'rookie_scope':'LaMelo original2020pick4 option uses previousyear3 amount and samecomponent26.5% increment; Duarte original2021pick10 thirdyear ceiling independent80..120; vendor comparable fullvalue is not copiedcontract or bonus. Kessler originalselected120% secondyear3350760.',
        'salary_lower_function':'Originalprotectedbase/ExCminimum whereapplicable; rookiebase>=80%scale. All3components nonnegative; original performance/assignment clauses preserved, no newassignment means no newbonus trigger here.',
        'legacy_stretch_R23':['0','16371000'],'legacy_scope':'Named prior validstretch outer retained once;13ordinarycontract endpoints<=2020–21 and2020campclosedperiods add no newFY23 Salary absent a selected newresolution. Delayofpayment is notnewSalary. Not actualremaining0 or allprivateabsence.',
        'Stanley_previous_full_Year2_reserved':2351532,'Stanley_FY22_salary_period_end':'2023-06-30','Stanley_payment_balance_certified_zero':False,
        'N23':None,'A23':None,'N23_domain':'Positive120%prepared2023scale after ownedfirstselection untilrenounce/sign. Root separately supplies slot16 witness; no exactpreparedtable certification or draftee/notices selection here. New signedrookie replaces samehold once.',
        'prepared_first_scale_port':{'pick':16,'conditional_separate_slot_witness':'research/CHICAGO_2023_FIRST_ROUND_SLOT_16_2026_10_08.json','NBA_published_adjusted_table_verified':False,'baseline_ExB_PDF631_first':2946800,'legal_function':'S23(16): I1(hhh)/(iii) NBA-prepared adjustedscale; baseline multipliedbycapratio, officialscale-rounding notyetcertifiedhere','normal_unsigned_hold':'1.2*S23(16)','apron_unsigned_first':'RTBase+allapplicablebonuses; conforming initialRT usesS23(16), not automatically1.2','actual_2023_draftee':None},
        'A23_domain':'CurrentfirstRequiredTender base + allapplicable bonuses; no unsignedsecond statutory charge inferred from cash overreserve.',
        'before_new_draft_total_is_whole_cost':False},
      'FA_hold_function_bank':[
        {'player':n,'normal':'max(FAAmount,QO_Salary_ifoutstanding,MaximumQO_ifissued,FRN_ifissued) forRFA; UFA FAAmount until validrenounce/re-sign/otherNBA-sign',
         'FAAmount_rule':'Coby250/300%originalpriorSalary cappedII7/floor; otherpriorlegalminimum⇒VII4d4 reimbursementlimitedthen-currentmin; expiredTW⇒VII4d7 zeroYOSmin. If exactsourcefamily differs useVII4d1–3 qualifyingclassification.',
         'apron':'UFAFAAmount excluded; RFA outstandingQO Salary+Unlikely orFRN, excludesTWQO; separately include acceptedUPC fullcurrentcomponents',
         'new_UPC_replaces_same_FA_QO_claim_once':True,'amount_unselected_not_zero':True}
        for n in EXPIRED+TW],
      'annual_2023_exception_bank':{'NTMLE_reference':12405000,'TMLE_reference':5000000,'RoomMLE_reference':7723000,
        'BAE_reference_function':'New2023VII6d amount, entitlement/use/annualavailability separate; no candidate BAE use',
        'unused_normal_deemed':'VII6n2 incorporation condition and valid writtenrenounce; candidate July7 expressrenounce unusedincorporatedexceptions before costscreen, not assumed automaticabovecap cancellation',
        'unused_apron':'VII2e excludes unusedexceptionamounts; do not subtract signedCarusoSalary',
        'TPE_DPE':'No newtrade/DPEselected; old annualexpiry finiteinventory carried from acceptednamedfamily, not freshprivateabsence certificate',
        'candidate_use':[],'first_apron_trigger_actions':'VII2e A–E: BAE/NTMLE/receivingS&T/qualifyingwaivedplayer/expandedTPE; post2023transitions separatelycheckF–J. Bird/min/RSCownextension alone hasnone.',
        '2021_or2022_hardcap_automatically_carries':False,'tax_is_hardcap':False},
      'public_cap_reference':{'cap':136021000,'tax':165294000,'first_apron':172346000,'second_apron':182794000,'fictional_cap_choice_certified':False},
      'rights':{'Marko Simonovic':'SelectedfirstX5a_iAug14,2022→Aug14,2023; thereafter X5 expiry/reopening, nofreepermanentcarry/newforeignagreementinvented',
        'Keon Ellis':'2022validRTunaccepted; subsequent2023draft/X4c orredraft/X4b orforeignX5 dispatch; priorCHIexclusiveclaim notautomaticforever',
        'CHI2023_first':'Named retainedownfirst interface; exactrank/player unselected',
        'CHI2023_second':'Original2019WAS/P1candidate claim chain remains rootseparateowner; no automaticCHIownsecond orDENincomingsecond'},
      'followup_artifact':ACTION}
    actions={**shared,'id':'CHICAGO_2023_FOLLOWUP_FINITE_ACTIONS','routine_policy':p,'Coby_ordinary_QO':qo,
      'Coby_implementation':{'issued_June28_candidate':'Team-signed oneSeason2017QO timelydeliveredafterchosenSeasonend; all3owncomponents and lesser-ofrank15 completepackages preserved. Fullbaseprotection; MaximumQOnotissued. Price upper7744602 notchosenprice.',
        'direct_Bird_candidate':'CobypriorCHI2020/21/22service+unrenouncedqualifyingrights; July7direct3yearUPCfullprotected/nooption/newbonus0, price11m..40m/3 firstyear and0..8%raises aslawallows, recommendation12mflat×3. Consentfictioncandidate/actualnull.',
        'ordinary_QO_acceptance_alternative':'SeparateoneSeasonJuly7acceptvalidoffer; originalpackage notelementwisemin. ConsumesSTD1. Never simultaneouslyaddBirdUPC.',
        'acceptance_clock':'AfterJuly1 newXI4c Oct1Sunday→Oct2 underXLII2; laterwrittenextension<=March1; withdrawalsJuly13 /laterwrittenassent /July14renounce. OldJuneissuance still2017.',
        'market_reference':'NBA2023roundup reports3year40m (includingreportuncertainty); explicit12mflatproposal is notactualreportedbase/bonus split or actualChicagoalternateacceptance',
        'future2026_contract_or_role_change':False},
      'minimum_offer_inputs':{n:checked_minimum(y) for n,y in [('Javonte Green',4),('Joe Wieskamp',2),('Tony Bradley',6),('Denzel Valentine',7),('Tomas Satoransky',7),('Devon Dotson',3)]},
      'minimum_service_scope':'NamedYOS rows are admitted creditedservice candidates, not registration-as-YOS. Recomputeifselectedcreditdiffers; II6actualfunction controlling. Fullcashupper moreconservative thanone-yearreimbursement; no bonuses byminimumform.',
      'Wieskamp_RFA':'Two creditedSeasons; June28old125%componentQO vsapplicableJuly1min+200k; starteroverride isseparateactualchosenstat port notinferredfromreserve. DirectJuly7minimumnewUPC requiresgenuineassent and replacesQO/hold once; no2023SecondRoundPickException retroactivelyapplied to2021UPC.',
      'two_way_routes':tw,'LaMelo_extension_forms':es,
      'LaMelo_extension_clock':{'opens':'2023-07-06T12:01:00_ET','closes':'18:00ET daybeforefirstRegularDay ofsecondoptionyear; conditionalactualcalendarport',
        'full_Bird_eligibility_service':[2020,2021,2022,2023],'service_rule':'OriginalRSCfirst4ChicagoSeasons; noBirdreset, subjectrenderingterms',
        'term_max':5,'first_salary_capyear':2024,'first_max_measured':'July1,2024cap/YOS/II7HigherMax criteria, no2023cap substitute',
        'market_comparator':'NBAJuly7,2023 news5year up-to260m Hornets report; totalconditional, differentactualpick/team/health/stats notimported',
        'extension_selected':False,'future_actual_award_or_private_assent':None},
      'next_option_notices':[{'player':n,'option_added_capyear':2024,'working_date':'2023-10-01','signed_personal_or_email_notice':True,
        'window_condition':'Dayafter2022–23NBASeasonends<=Oct1<=Oct31; actualFinalsoutcome/date notselectedhere',
        'notice_is_candidate_not_actual_receipt':True,'option_number':num,'current_FY23_change':0}
        for n,num in [('Chris Duarte',2),('Walker Kessler',1)]],
      'usable_roster_functions':[
        {'id':'CORE_KEEP_ROOKIE_SLOT','STD_names':list(LIVE)+['Coby White','Javonte Green','Joe Wieskamp','Denzel Valentine','Tomas Satoransky'],
         'STD_count':14,'conditional_new_first_STD_capacity':1,'new_first_identity':None,'TW_names_ifeligible':['Tyler Cook'],
         'Dotson':'UnacceptedstandardQO/ROFR+hold retained;notTW','Bradley':'ExpirednoUPC;validrenounceFAhold beforefirstRSC orcarryholdintotal',
         'current_source_Gamma_removed':False,'season_active_and_health_not_selected':True},
        {'id':'DOTSON_STANDARD_ALTERNATIVE','STD_names':list(LIVE)+['Coby White','Javonte Green','Joe Wieskamp','Denzel Valentine','Devon Dotson'],
         'STD_count':14,'conditional_new_first_STD_capacity':1,'new_first_identity':None,'TW_names_ifeligible':['Tyler Cook'],
         'Satoransky_Bradley':'ExpirednoUPC;holdsretaineduntilvalidrenounce; nooldsignedsalarywaivedaway',
         'current_source_Gamma_removed':False,'season_active_and_health_not_selected':True}],
      'cost_evaluator':{'callable':SELF+'::cost_state_function','live9_fullupper':live,
        'normal':'live9 + newSignednormal + remainingFA/QO/FRNnormal + R23 + N23 + unusedannualdeemednormal',
        'apron':'live9 + newSignedapron + remainingRFAQO+Unlikely/FRN + R23 + A23; noUFAhold/unusedexception',
        'tax':'ApplyVII2d actualattributedTaxSalary andearnedperformance/reimbursement/waived adjustments; normal/apronupper notexacttaxpoint',
        'new_hardcap_trigger_in_recommended_family':False,'exceeding_apron_screen_is_illegal':False,'whole_numeric_upper':None},
      'finite_next_execution':[
        'Adopt reviewed routine Coby/minimum/QO family underexistingdelegation; exactmarketpoint remainscandidate until rootadoption, not human-receiptgate',
        'Rootjoin retained2023first rank/player/RT with one reservedSTD slot; secondownership independent; noextraSTD16',
        'BindCookcreditedYOS3 or qualifying4 exception andEllis2023draftdispatch; DotsonfourthTWexcluded',
        'LaMeloLM1..4 comparativeextension remainsconsequentialpricefamily; nofutureHigherMaxawardselected',
        'Add currentN23/A23/R23/FAcomponentinput to cost_evaluator thenindependentfullFY23review; noemptyinput-as-zero',
        '2023–24calendar/health/roles/results notproducedbycontractfunctions']}
    return window,actions

def validate(o,a):
    try:
        expected=build()
        assert (o,a)==expected,'Saved output differs from complete source-bound reconstruction'
        assert_contract_rows(o['named_contracts'],physical());assert_policy(a['routine_policy']);assert_tw(a['two_way_routes']);assert_extensions(a['LaMelo_extension_forms'])
        for x in a['usable_roster_functions']:
            assert len(x['STD_names'])==len(set(x['STD_names']))==x['STD_count']==14
            assert x['STD_count']+x['conditional_new_first_STD_capacity']<=15
        assert o['salary_scope']['N23'] is None and o['salary_scope']['A23'] is None
        return []
    except (AssertionError,KeyError,TypeError,ValueError) as e:return [str(e)]

def progress():return '\n'.join(['| 묶음 | 상태 |','|---|---|','|1 드래프트 연쇄|완료 보존|','|2 S2 유한시즌|완료 보존|','|3 2021–23 실행·2023 후속|진행·이 패킷은 후보|','|4 장기 커리어|미완료|','|5 세계설정/출구|미완료|','|6 집필규격·Context Pack|미완료|','|7 통합·독립·최종승인|CLOSED|','','미완료 큰 묶음 **5**, 6번까지 **4**. 현행 등록기 참조·Pack0.'])
def window_md(o):
    lines=['# Chicago 2023–24 기존 명명 계약 창','',o['status'],'',f'기준 main `{BASELINE}`. 2023-07-01 원17명을 **STD9존속 / STD6만료 / TW2만료**로 분리한다. 새 재계약·임상·실수락 인증은 아니다.','', '| 선수 | July1 상태 | FY23 전체 성분 상단/함수 |','|---|---|---|']
    for r in o['named_contracts']:lines.append('|'+r['player']+'|'+('존속' if r['July1_2023_live'] else '만료·hold 유지')+'|'+(f"${r['normal_salary_upper']:,}" if r['July1_2023_live'] else '새 UPC null / FA·QO 별도')+'|')
    lines+=['',f"9존속 계약의 normal/apron 보수상단 합 **${o['salary_scope']['live9_normal_and_apron_all_component_upper']:,}**. LaMelo는 Chicago2020#4, Duarte2021#10, Kessler2022#18 원슬롯이다. Patrick/Ziaire 표는 같은 순번의 공개 상단 수치만 지원하며 개인 계약·보너스·원통지일을 복사하지 않는다.",'','원 성과/보호/Γ를 보존한다. 새 양도가 없으므로 새 assignment charge를 만들지 않으며 기존 조항 자체를0으로 인증하지 않는다. Stanley의 이전 Year2는2023-06-30 급여기간 종료이며 실제 지급잔액0이 아니다. 유효 legacy stretch `R23∈[0,16,371,000]`은 한 번 유지한다.','', 'Normal은 FA/QO/FRN 및 첫 신인hold와 산입된 unused exception을 포함한다. Apron은 UFA hold·unused exception을 제외하고 RFA QO+Unlikely/FRN 및 실제 신인RT를 분리한다. Tax는 별도 VII2d 정의다. N23/A23는 positive typed null이며 새2023 first 순번을 정하지 않는다.','', 'Bird/minimum/RSC/own extension만 쓰는 추천가족은 새 hardcap trigger가 없다. 과거 CarusoNTMLE hardcap을 2023에 이월하지 않는다. 새2023 연간 예외 entitlement/사용/renounce는 각각 별도다. Apron screen 초과를 자동위법으로 인증하지 않는다.','', '실사용 후보는 [후속 조치 패킷](../research/CHICAGO_2023_FOLLOWUP_FINITE_ACTIONS_2026_10_08.md)과 producer의 `cost_state_function`으로 연결한다.','',progress()]
    return '\n'.join(lines)+'\n'
def actions_md(a):
    return '\n'.join(['# Chicago 2023 유한 후속 조치','',a['status'],'','## 사용할 수 있는 계약·슬롯 가족','',
      'June28 팀서명 QO 전달은 June29 마감의2017법 가족이다. Coby는 선택된82GP/0GS/1,476분으로 nonstarter 패키지상단 **$7,744,602**다. Own상단$9,942,120와$2,197,518 차이는 선택가격이 아니다. 세 성분을 보존한 lesser-of 전체 패키지를 택하며 원소별 최솟값 UPC를 만들지 않는다.',
      '', 'Coby July7 **FullBird3년** 첫해$11m–$40m/3 구간, flat$12m×3 추천(새 bonus0/완전보호/옵션없음)을 명명한다. NBA2023 보도3년40m는 시장 비교이며 실제 base/bonus·대체수락은 아니다. ValidQO 한 시즌 수락은 다른 대안이고 새 Bird와 중복하지 않는다. QO 이후 새CBA 수락창 Oct1→Oct2 및 withdrawal/renounce를 별도 적용한다.',
      '', 'Green/Wieskamp/Valentine/Sato는 새 한 시즌 **해당2023법정최소** 합의후보다. II6 ExC×cap비율의 floor..ceil+2는 조건부 수치screen으로 실제공식반올림/센트 인증이 아니다. 법정함수로 제안하고 보너스없음·fullcash 초과예약을 명시한다. Wieskamp RFA QO/125%·min+200k와 starter override를 별도 보존하며2023 SecondRoundPickException을2021계약 갱신에 소급하지 않는다.',
      '', '원 live9+Coby+Green+Wieskamp+Valentine+Sato=**14STD**. Bradley는 만료 후 미서명이고 FAhold가 유효조치까지 남는다. 한 새1R 서명은15번째 STD를 쓴다. Dotson standard minimum 대안은 Sato 대신 같은 슬롯을 소비한다. 지급/Γ를 지우는 방출이나 새코어이탈을 자동 선택하지 않는다.',
      '', '## 투웨이·권리','',
      'Devon Dotson은CHI2020/21/22 세 capyear를 이미 사용했으므로 **2023 네 번째 CHI TW 금지**. StandardQO 미수락이면 권리·hold 유지/STD0/TW0, 별도 standard min 수락이면STD1이다. June28 QO는2017TWAnnualNBADLSalary 보호 규칙이며 새$90k를 과거 사실로 부르지 않는다. Cook은YOS3와 새4YOS 무NBA게임·전RegularRoster 예외를 분리하고 조건부 새한시즌 TW가족을 만든다. Roster존재/0분으로YOS나 예외 충족을 추정하지 않는다. 새legalTWmax3이나 자동세칸채움0이다.',
      '', 'Keon Ellis는2022 초기RT 미수락만으로2023독점권이 계속되지 않는다. SubsequentDraft 미지명→RookieFA TW 가능, 재지명→새holder/RT 필요, 원외국계약이면X5를 적용한다. 새CHI2R 자체는 아직 root별도권리 포트다. Marko 원notice는2023Aug14까지이며 새외국합의·무기한존속을 만들지 않는다.',
      '', '## 연장·통지','',
      'LaMelo LM1/2/3/4 원 비교안은5년25→조건부30 /4년25→조건부30 /5년25고정 /미연장이다. 2023July6 12:01ET부터 secondoptionyear 개막 전날18ET까지, 최대첫해는2024July1 cap·II7 요건으로 계산한다. 신규 extension은FY23 급여·슬롯에0추가다. 실제Hornets5년 up-to260m 보도는 비교만이며 원Chicago수락/미래상·30%를 정하지 않는다.',
      '', 'Duarte fourth /Kessler third FY24 옵션은2023Oct1 팀서명 통지 후보로 구체화한다. Seasonend 이후·Oct31이전 조건을 caller가 검문한다. LaMelo/Duarte 기존2022Oct1 통지는 보존하며 새통지를 과거에 소급하지 않는다.',
      '', '## 완료 범위와 다음 입력','',
      '원17 계약의2023기간/성분/일자와 재계약·QO·TW·옵션의 건설적 후보가 연결됐다. 현실접수/시장수락/임상은 작품설계 완료의 새 필수게이트가 아니다. 다음은 root의 routine 채택, 새1R 순번·선수·RT 한 슬롯, Cook creditedYOS 분기, LaMelo 연장가격안 및 N23/A23/R23/남은FA를 같은 비용함수로 소비하는 명명 작업이다. 전체 FY23 비용·등록·시즌·장기결과는 아직 이 패킷의 인증이 아니다.',
      '',progress()])+'\n'

def self_test():
    tests=[]
    s=source_inputs()
    for label,field,val in [('wrong_P_fiscal_end','last_selected_fiscal_year_end','2024-06-30'),('drop_Gamma','old_Gamma_and_full_original_components_preserved',False),('wrong_FY23_price','normal_salary_upper',1)]:
        rows=construct(s);next(r for r in rows if r['player']=='Protagonist')[field]=val
        try:
            with patch(__name__+'.construct',return_value=rows):build()
        except AssertionError:tests.append(label)
        else:raise AssertionError('FALSE PASS '+label)
    p=policy();p['QO_model_date']='2023-06-30'
    try:
        with patch(__name__+'.policy',return_value=p):build()
    except AssertionError:tests.append('late_QO')
    else:raise AssertionError('FALSE PASS late_QO')
    tw=two_way_routes();tw['Devon Dotson']['new_CHI_TW_2023_allowed']=True
    try:
        with patch(__name__+'.two_way_routes',return_value=tw):build()
    except AssertionError:tests.append('Dotson_fourth_TW')
    else:raise AssertionError('FALSE PASS Dotson_fourth_TW')
    es=extension_forms();es[0]['first_extended_capyear']=2023
    try:
        with patch(__name__+'.extension_forms',return_value=es):build()
    except AssertionError:tests.append('LM_extension_charged_early')
    else:raise AssertionError('FALSE PASS LM_extension_charged_early')
    try:cost_state_function(N23=None,A23=1,R23=1,expired_holds_normal=1,expired_holds_apron=1,new_signed_normal=1,new_signed_apron=1)
    except AssertionError:tests.append('null_draft_as_zero')
    else:raise AssertionError('FALSE PASS null_draft_as_zero')
    bad=copy.deepcopy(s);bad[STAT]['ordinary_QO_component_function']['selected_starter']=True
    try:
        with patch(__name__+'.source_inputs',return_value=bad):build()
    except AssertionError:tests.append('same_source_identity_starter_reversal')
    else:raise AssertionError('FALSE PASS source_reversal')
    return tests

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
    o,a=build()
    if args.write:
        for p,x,render in [(OUT,o,window_md),(ACTION,a,actions_md)]:
            (ROOT/p).write_text(serial(x),encoding='utf8',newline='\n');(ROOT/p.replace('.json','.md')).write_text(render(x),encoding='utf8',newline='\n')
    errors=[]
    if args.check:
        saved=[json.loads((ROOT/p).read_text(encoding='utf-8-sig')) for p in [OUT,ACTION]];errors=validate(*saved)
        for p,x,render in [(OUT,saved[0],window_md),(ACTION,saved[1],actions_md)]:
            if norm((ROOT/p.replace('.json','.md')).read_text(encoding='utf-8-sig'))!=render(x):errors.append('Markdown stale '+p)
    tests=self_test() if args.self_test else []
    print(json.dumps({'current':not errors,'errors':errors,'live_STD':9,'expired_STD':6,'expired_TW':2,'live9_upper':sum(v[0] for v in LIVE.values()),'negative_controls':tests},ensure_ascii=False))
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
