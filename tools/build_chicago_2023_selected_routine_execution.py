"""Selected fictional FY23 routine contracts; dated charges are legal functions."""
from __future__ import annotations
import argparse, copy, hashlib, json, math
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import build_chicago_2023_24_existing_contract_window as prior

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2023_selected_routine_execution.py'
OUT='simulation/CHICAGO_2023_SELECTED_ROUTINE_EXECUTION.json'
SELECT='canon/DELEGATED_CHI_2023_ROUTINE_CONTRACT_DESIGN_SELECTION_2026_10_08.json'
WINDOW=prior.OUT
ACTION=prior.ACTION
SLOT='research/CHICAGO_2023_FIRST_ROUND_SLOT_16_2026_10_08.json'
REVIEW='reviews/CHI_2023_CONTRACT_WINDOW_G11_INDEPENDENT_REVIEW_2026_10_08.json'
JOIN_REVIEW='reviews/CHI_2023_ROUTINE_SELECTION_JOIN_G11_INDEPENDENT_REVIEW_2026_10_08.json'
PINS={SELECT:'9847a74948b79bcafa991e4f91884f5dc5f5a83f144a65996f3daa5bae09334c',
 WINDOW:'cf65846136975dd8b7f301505ad7fa06b564837f7962a607681632b84489d092',
 ACTION:'542457d0b30ec2991faf0efa6c92a050dcd9120dfd929473ed29b90b7155f383',
 prior.SELF:'9af9056e8656df84c894b7ede00d91d0f3ef0c92c867089f1cb5ff2f400f7b8b',
 SLOT:'abbcdaaa6ff14d277f88d47fa600320fc6458ec4b057e5a7b73b414b6fbabf30',
 REVIEW:'d791ac98b6196a5ff8bf98e1ccd62e7868ec01019dd120cffc73ac323bf6bf3f',
 JOIN_REVIEW:'a5e78aa0bcfd285acb1d9293a69b9edda6967cd7adb968fc459b03b26064b7a1'}
MIN_NAMES={'Javonte Green':4,'Joe Wieskamp':2,'Denzel Valentine':7,'Tomas Satoransky':7}
TW_NAMES={'Devon Dotson':3,'Tyler Cook':4}
LIVE=prior.LIVE.copy()

def norm(t):return t.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(norm((ROOT/p).read_text(encoding='utf-8-sig')).encode()).hexdigest()
def serial(o):return json.dumps(o,ensure_ascii=False,indent=2)+'\n'
def physical():
    for p,h in PINS.items():assert sha(p)==h,'Pinned physical source changed: '+p
    return {p:json.loads((ROOT/p).read_text(encoding='utf-8-sig')) for p in PINS if p.endswith('.json')}
def source_inputs():return physical()
def assert_sources(s):
    assert s==physical(),'Consumed source objects differ from pinned physical source'
    assert prior.validate(s[WINDOW],s[ACTION])==[],'Prior complete reconstruction failed'
    z=s[SELECT];d=z['selected_design']
    assert z['id']=='DELEGATED_CHI_2023_ROUTINE_CONTRACT_DESIGN_SELECTION'
    assert d['Coby']=={'first_year_salary':12000000,'term_years':3,'annual_salary':[12000000]*3,'bonus':0,
      'protection':'FULL','option':'NONE','exception':'QUALIFYING_FULL_BIRD_FAMILY',
      'alternative_one_year_QO_acceptance_selected':False,'same_claim_FA_QO_hold_replaced_once':True,'contract_fictional_date':'2023-07-07'}
    assert [x['player'] for x in d['minimum_one_year_agreements']]==list(MIN_NAMES)
    for x in d['minimum_one_year_agreements']:
        assert x['first_salary']=='PREPARED_2023_LEGAL_MINIMUM_FOR_SELECTED_CREDITED_SERVICE_FAMILY'
        assert x['bonus']==0 and x['protection']=='FULL' and x['exception']=='MINIMUM'
        assert x['same_claim_hold_replaced_once'] and x['contract_fictional_date']=='2023-07-07'
    assert d['Tony Bradley']=={'new_UPC':False,'legal_FA_renunciation_selected_as_fiction':True,'fictional_date':'2023-07-07','all_original_protected_payment_obligations_preserved':True}
    for name,x in d['expired_TW'].items():
        assert name in TW_NAMES and not x.get('new_CHI_TW',x.get('new_TW')) and not x['new_STD']
        assert next(v for k,v in x.items() if k.startswith('valid_unaccepted')) is True
    assert set(d['expired_TW'])==set(TW_NAMES)
    assert d['LaMelo_extension']=='Current2023 extension shape still unselected; no new UPC or current2023 extra salary inferred'
    assert set(d['new_option_notices'])=={'Chris Duarte','Walker Kessler'}
    assert z['slot_join']['selected_nonrookie_standard']==14 and z['slot_join']['selected_TW_UPCs']==0
    assert z['slot_join']['first_round_slot']==16 and not z['slot_join']['new_rookie_UPC_or_identity_selected']
    assert z['all_original_Gamma_bonus_protection_stretch_and_unrenounced_holds_preserved']
    assert not z['actual_market_player_acceptance_private_UPC_or_receipt_certified'] and not z['whole_macro3_or_2023_24_cost_complete']
    assert s[SLOT]['Chicago_origin_first_slot']==16 and s[SLOT]['Chicago_selected_holder']=='CHI'
    assert not s[SLOT]['certification']['draftee_and_RSC_price_selected']
    assert s[JOIN_REVIEW]['selection_source']=={'path':SELECT,'sha256':PINS[SELECT]}
    assert s[JOIN_REVIEW]['independent_review_completed'] and s[JOIN_REVIEW]['status']=='INDEPENDENTLY_ACCEPTED_BOUNDED_ROUTINE_DESIGN_SELECTION_JOIN'
    assert not s[JOIN_REVIEW]['limits']['whole_2023_24_cost_or_registration'] and not s[JOIN_REVIEW]['limits']['actual_contract_receipt_or_player_acceptance']

def construct(s):
    rows=[]
    for src in s[WINDOW]['named_contracts']:
        n=src['player'];base={'player':n,'holder':'CHI','prior_window_pointer':WINDOW+'#/named_contracts/'+str(len(rows)),
          'original_Gamma_full_components_and_protected_cash_preserved':True,'actual_contract_receipt_or_player_assent':None,
          'actual_salary_cents_certified':False,'new_assignment_selected':False}
        if n in LIVE:
            value,end,method=LIVE[n]
            base.update(STD=1,TW=0,operation='PRESERVED_EXISTING_LIVE_UPC',starts='EXISTING',
              FY23_normal_upper=value,FY23_apron_upper=value,fullcash=src['FY23_salary_plus_all_performance_upper'],
              last_salary_capyear_start=end,last_fiscal_end=f'{end+1}-06-30',mechanism=method,
              service_end_not_inferred_from_fiscal_end=True,future_option_outcome=src.get('future_option_outcome'))
        elif n=='Coby White':
            base.update(STD=1,TW=0,operation='SELECTED_FICTIONAL_NEW_FULL_BIRD_UPC',starts='2023-07-07',
              salary_schedule=[12000000]*3,FY23_normal_upper=12000000,FY23_apron_upper=12000000,
              fullcash=12000000,bonuses=0,protection='FULL_SKILL_INJURY',option='NONE',term_years=3,
              last_salary_capyear_start=2025,last_fiscal_end='2026-06-30',mechanism='FULL_BIRD',
              service_capyears=[2020,2021,2022],Bird_rights_not_renounced=True,
              same_claim_FA_QO_replaced_once=True,QO_acceptance_also_selected=False)
        elif n in MIN_NAMES:
            y=MIN_NAMES[n]
            base.update(STD=1,TW=0,operation='SELECTED_FICTIONAL_NEW_ONE_SEASON_MINIMUM_UPC',starts='2023-07-07',
              statutory_salary=f'M23({y})',FY23_normal_upper=f'M23({y}) fullcash overreservation',
              FY23_apron_upper=f'M23({y}) fullcash overreservation',fullcash=f'M23({y})',
              credited_YOS_family=y,prepared_numeric_screen=copy.deepcopy(s[ACTION]['minimum_offer_inputs'][n]),
              bonuses=0,protection='FULL_SKILL_INJURY',option='NONE',term_years=1,
              last_salary_capyear_start=2023,last_fiscal_end='2024-06-30',mechanism='MINIMUM_EXCEPTION',
              same_claim_FA_QO_replaced_once=True)
        elif n=='Tony Bradley':
            base.update(STD=0,TW=0,operation='EXPIRED_NO_NEW_UPC_AND_VALID_WRITTEN_FA_RENUNCIATION',starts='2023-07-07',
              FA_hold_after_valid_renunciation=0,new_player_cash=0,zero_is_original_payment_balance=False,
              renunciation_is_fiction_selected=True,renunciation_erases_original_protected_obligation=False)
        else:
            y=TW_NAMES[n]
            base.update(STD=0,TW=0,operation='VALID_UNACCEPTED_STANDARD_QO_RIGHTS_AND_HOLD_RETAINED',
              QO_issued='2023-06-28',issuance_law='2017_XI1c_iii_A_or_C_and_XI4',
              QO_term_years=1,QO_salary=f'M23({y})',QO_new_bonuses=0,
              QO_protection='Applicable Two-Way Annual NBADL Salary for the QO Season under June28 operative2017 law; not automaticallynew90k',
              credited_YOS_family=y,QO_acceptance_selected=False,QO_withdrawal_or_FA_renunciation_selected=False,
              credited_YOS_is_exact_private_fact=False,
              FA_hold=f'max(M23(0),M23({y}),otherlawfuloutstandingFRN); no MaximumQO selected',
              apron_QO_plus_unlikely=f'M23({y})',new_player_cash=0,
              unaccepted_QO_is_actual_cash_or_UPC=False,ROFR_preserved=True,
              TW_rights_or_QO_is_live_TW_UPC=False,clinical_YOS_record_certified=False)
        rows.append(base)
    return rows

def assert_rows(rows,s):
    assert len(rows)==17 and [x['player'] for x in rows]==[x['player'] for x in s[WINDOW]['named_contracts']]
    assert sum(x['STD'] for x in rows)==14 and sum(x['TW'] for x in rows)==0
    for r in rows:
        n=r['player'];assert r['holder']=='CHI' and r['original_Gamma_full_components_and_protected_cash_preserved']
        assert r['actual_contract_receipt_or_player_assent'] is None and not r['actual_salary_cents_certified'] and not r['new_assignment_selected']
        if n in LIVE:
            value,end,method=LIVE[n]
            assert r['operation']=='PRESERVED_EXISTING_LIVE_UPC' and r['mechanism']==method
            assert r['FY23_normal_upper']==r['FY23_apron_upper']==r['fullcash']==value
            assert r['last_salary_capyear_start']==end and r['last_fiscal_end']==f'{end+1}-06-30'
            assert r['service_end_not_inferred_from_fiscal_end']
        elif n=='Coby White':
            assert r['salary_schedule']==[12000000]*3 and r['mechanism']=='FULL_BIRD'
            assert r['FY23_normal_upper']==r['FY23_apron_upper']==r['fullcash']==12000000
            assert r['service_capyears']==[2020,2021,2022] and r['Bird_rights_not_renounced']
            assert r['term_years']==3 and r['last_fiscal_end']=='2026-06-30' and not r['QO_acceptance_also_selected']
        elif n in MIN_NAMES:
            y=MIN_NAMES[n];assert r['credited_YOS_family']==y and r['statutory_salary']==f'M23({y})'
            assert r['fullcash']==f'M23({y})' and r['FY23_normal_upper']==r['FY23_apron_upper']==f'M23({y}) fullcash overreservation','Selected legal minimum cash and Salary cannot be deleted'
            assert r['prepared_numeric_screen']==s[ACTION]['minimum_offer_inputs'][n]
            assert r['mechanism']=='MINIMUM_EXCEPTION' and r['term_years']==1 and r['last_fiscal_end']=='2024-06-30'
        elif n=='Tony Bradley':
            assert not r['STD'] and not r['TW'] and r['FA_hold_after_valid_renunciation']==0
            assert r['renunciation_is_fiction_selected'] and not r['renunciation_erases_original_protected_obligation'] and not r['zero_is_original_payment_balance']
        else:
            y=TW_NAMES[n];assert not r['STD'] and not r['TW'] and r['QO_issued']=='2023-06-28'
            assert r['credited_YOS_family']==y and r['QO_salary']==f'M23({y})' and r['QO_new_bonuses']==0
            assert r['QO_term_years']==1 and not r['QO_acceptance_selected'] and not r['QO_withdrawal_or_FA_renunciation_selected']
            assert r['FA_hold']==f'max(M23(0),M23({y}),otherlawfuloutstandingFRN); no MaximumQO selected' and r['apron_QO_plus_unlikely']==f'M23({y})','Unaccepted standard QO legal charges cannot be deleted'
            assert r['new_player_cash']==0 and not r['credited_YOS_is_exact_private_fact'] and not r['clinical_YOS_record_certified']
            assert r['issuance_law']=='2017_XI1c_iii_A_or_C_and_XI4' and r['QO_protection']=='Applicable Two-Way Annual NBADL Salary for the QO Season under June28 operative2017 law; not automaticallynew90k'
            assert r['ROFR_preserved'] and not r['unaccepted_QO_is_actual_cash_or_UPC'] and not r['TW_rights_or_QO_is_live_TW_UPC']
        if n=='Coby White' or n in MIN_NAMES:
            assert r['starts']=='2023-07-07' and r['STD']==1 and r['TW']==0
            assert r['bonuses']==0 and r['protection']=='FULL_SKILL_INJURY' and r['option']=='NONE' and r['same_claim_FA_QO_replaced_once']

def option_notices():
    return [{'player':n,'fictional_notice_date':'2023-10-01','form':'TEAM_SIGNED_PERSONAL_OR_EMAIL_NOTICE',
      'option_number':k,'added_salary_capyear':2024,'FY24_salary_plus_bonus_upper':v,
      'season_end_before_notice_required':True,'notice_before_Oct31':True,
      'FY23_new_salary':0,'new_STD_slot':0,'actual_delivery_receipt':None}
      for n,k,v in [('Chris Duarte',2,6133005),('Walker Kessler',1,3510480)]]
def assert_options(o):
    assert len(o)==2
    for r,n,k,v in zip(o,['Chris Duarte','Walker Kessler'],[2,1],[6133005,3510480]):
        assert r['player']==n and r['option_number']==k and r['fictional_notice_date']=='2023-10-01'
        assert r['added_salary_capyear']==2024 and r['FY24_salary_plus_bonus_upper']==v
        assert r['FY23_new_salary']==r['new_STD_slot']==0 and r['actual_delivery_receipt'] is None
        assert r['season_end_before_notice_required'] and r['notice_before_Oct31'] and r['form']=='TEAM_SIGNED_PERSONAL_OR_EMAIL_NOTICE'

def evaluate_cost(*,prepared_minimums,prepared_scale16,first_RT_base,R23,remaining_FRN_normal=0,remaining_FRN_apron=0):
    """July7 costs after selected renunciations, before any newly selected first RSC."""
    assert set(prepared_minimums)=={0,2,3,4,7}
    for y,m in prepared_minimums.items():
        assert m is not None and Fraction(m)>0
        q=Fraction(prior.MIN_BASE[y]*136021000,123655000)
        assert math.floor(q)<=Fraction(m)<=math.ceil(q)+2,'Prepared minimum outside stated conditional screen'
    assert prepared_scale16 is not None and Fraction(prepared_scale16)>0,'Positive prepared16 scale required'
    s=Fraction(prepared_scale16)
    assert first_RT_base is not None and max(Fraction(4,5)*s,Fraction(prepared_minimums[0]))<=Fraction(first_RT_base)<=Fraction(6,5)*s
    assert R23 is not None and 0<=Fraction(R23)<=16371000
    assert all(x is not None and Fraction(x)>=0 for x in [remaining_FRN_normal,remaining_FRN_apron])
    minimum_cash=sum(Fraction(prepared_minimums[y]) for y in MIN_NAMES.values())
    qo=sum(Fraction(prepared_minimums[y]) for y in TW_NAMES.values())
    base=Fraction(sum(x[0] for x in LIVE.values())+12000000)+minimum_cash+qo+Fraction(R23)
    return {'normal_sufficient_upper':str(base+Fraction(6,5)*s+Fraction(remaining_FRN_normal)),
      'apron_sufficient_upper':str(base+Fraction(first_RT_base)+Fraction(remaining_FRN_apron)),
      'N23_unsigned_first_hold':str(Fraction(6,5)*s),'A23_unsigned_first_conforming_RT':str(Fraction(first_RT_base)),
      'unaccepted_first_RT_is_cash_payment':False,'unaccepted_standard_QO_is_cash_payment':False,
      'unused_exception_deemed_amount_after_selected_valid_renunciation':0,
      'actual_total_or_exact_tax_salary_certified':False,'hardcap_trigger_in_selected_family':False}

def dated_states(rows):
    signed=[r['player'] for r in rows if r['STD']]
    dates=['2023-06-28','2023-07-01','2023-07-07','2023-10-01']
    result=[]
    for date in dates:
        new=date>='2023-07-07'
        result.append({'date':date,'fiscal_regime':'2017_CBA_JUNE_ISSUANCE' if date<'2023-07-01' else '2023_CBA',
          'named_live_STD':signed if new else list(LIVE),'STD_count':14 if new else 9,'live_TW_UPC_count':0,
          'counts_are_FY23_projection_not_June28_current_registration':True,
          'new_2023_rookie_UPC':False,'reserved_first_STD_slot':1,'first_round_pick':16,'rookie_identity':None,
          'original_service_contracts_before_July1':'June28 nineFY23live is a forward-fiscal projection; prior17NBASeason service terms not erased' if date<'2023-07-01' else None,
          'Coby_Green_Wieskamp_Valentine_Sato_hold':'REPLACED_ONCE_BY_SELECTED_UPC' if new else 'OUTSTANDING_COMPLETE_FA_QO_FUNCTION',
          'Bradley_FA_hold':'VALID_WRITTEN_RENUNCIATION_NO_ORIGINAL_CASH_ERASURE' if new else 'OUTSTANDING_UFA_FA_AMOUNT',
          'Dotson_Cook':'VALID_UNACCEPTED_STANDARD_QO_WITH_RIGHTS_AND_POSITIVE_SALARY_HOLD',
          'original_Gamma_and_R23_preserved':True,'R23_interval':[0,16371000],
          'annual_unused_exceptions':'IF_INCORPORATED_INCLUDE_UNTIL_VALID_WRITTEN_RENUNCIATION' if not new else 'SELECTED_VALID_WRITTEN_RENUNCIATION_BEFORE_COST_COMPARISON',
          'options_for_FY24':'OCT1_SELECTED_NOTICES_ADD_FY24_ONLY' if date=='2023-10-01' else 'NOT_YET_NEW_NOTICE',
          'cost_function':'July7 evaluator' if new else 'LIVE9 + COMPLETE_NAMED_FA_QO_NORMAL/APRON_FUNCTIONS + POSITIVE_N23/A23 + R23 + INCORPORATED_UNUSED_NORMAL',
          'registration_is_actual_NBA_certificate':False,'FY23_health_or_result_selected_here':False})
    return result
def assert_states(states,rows):
    assert [s['date'] for s in states]==['2023-06-28','2023-07-01','2023-07-07','2023-10-01']
    signed=[r['player'] for r in rows if r['STD']]
    for s in states:
        new=s['date']>='2023-07-07'
        assert s['named_live_STD']==(signed if new else list(LIVE)) and s['STD_count']==(14 if new else 9)
        assert s['live_TW_UPC_count']==0 and s['reserved_first_STD_slot']==1 and s['first_round_pick']==16
        assert not s['new_2023_rookie_UPC'] and s['rookie_identity'] is None
        assert s['original_Gamma_and_R23_preserved'] and s['R23_interval']==[0,16371000]
        assert not s['registration_is_actual_NBA_certificate'] and not s['FY23_health_or_result_selected_here']
        assert s['options_for_FY24']==('OCT1_SELECTED_NOTICES_ADD_FY24_ONLY' if s['date']=='2023-10-01' else 'NOT_YET_NEW_NOTICE')
        assert s['fiscal_regime']==('2017_CBA_JUNE_ISSUANCE' if s['date']<'2023-07-01' else '2023_CBA')
        assert s['counts_are_FY23_projection_not_June28_current_registration']
        assert s['original_service_contracts_before_July1']==('June28 nineFY23live is a forward-fiscal projection; prior17NBASeason service terms not erased' if s['date']<'2023-07-01' else None)
        assert s['Coby_Green_Wieskamp_Valentine_Sato_hold']==('REPLACED_ONCE_BY_SELECTED_UPC' if new else 'OUTSTANDING_COMPLETE_FA_QO_FUNCTION'),'Same-claim hold replacement changed'
        assert s['Bradley_FA_hold']==('VALID_WRITTEN_RENUNCIATION_NO_ORIGINAL_CASH_ERASURE' if new else 'OUTSTANDING_UFA_FA_AMOUNT')
        assert s['Dotson_Cook']=='VALID_UNACCEPTED_STANDARD_QO_WITH_RIGHTS_AND_POSITIVE_SALARY_HOLD'
        assert s['annual_unused_exceptions']==('SELECTED_VALID_WRITTEN_RENUNCIATION_BEFORE_COST_COMPARISON' if new else 'IF_INCORPORATED_INCLUDE_UNTIL_VALID_WRITTEN_RENUNCIATION'),'Dated unused exception renunciation changed'
        assert s['cost_function']==('July7 evaluator' if new else 'LIVE9 + COMPLETE_NAMED_FA_QO_NORMAL/APRON_FUNCTIONS + POSITIVE_N23/A23 + R23 + INCORPORATED_UNUSED_NORMAL'),'FY24 option cannot become FY23 Salary'

def build():
    s=source_inputs();assert_sources(s)
    rows=construct(s);assert_rows(rows,s);options=option_notices();assert_options(options)
    states=dated_states(rows);assert_states(states,rows)
    min_screen={str(y):prior.checked_minimum(y)['conditional_floor_ceil_rounding_screen'] for y in [0,2,3,4,7]}
    base=132051061+12000000+sum(min_screen[str(y)][1] for y in MIN_NAMES.values())+sum(min_screen[str(y)][1] for y in TW_NAMES.values())
    return {'id':'CHICAGO_2023_SELECTED_ROUTINE_EXECUTION','status':'SELECTED_FICTIONAL_ROUTINE_CONTRACT_FAMILY_PENDING_CONSUMER_INDEPENDENT_REVIEW',
      'source_sha256':{**PINS,SELF:sha(SELF)},'repository_hash_convention':'UTF8_BOM_STRIPPED_CRLF_CR_TO_LF',
      'selection_authority':SELECT,'upstream_candidate_history_remains_unselected_flags':True,
      'selection_join_review':{'path':JOIN_REVIEW,'sha256':PINS[JOIN_REVIEW],'independent_review_completed':True,'is_new_consumer_review':False},
      'named_contracts_and_rights':rows,'dated_states':states,'selected_FY24_option_notices':options,
      'renewal_selection_scope':{'Coby_three_year_flat':[12000000]*3,'minimum_names':list(MIN_NAMES),
        'Bradley_FA_renunciation':True,'TW_new_UPCs':0,'Dotson_fourth_CHI_TW':False,
        'Cook_no_QO_prior_candidate_is_superseded_in_this_consumer_only':True,
        'Cook_standard_QO_reason':'FinishessecondconsecutiveoneSeasonCHI_TW2021/2022;2017XI1c(iii)standardQO irrespective eligiblethirdTW. IssueJune28 afterseasonend; YOS4 admittedcreditedservice branch notclinical0minuteinference.',
        'QO_issued_June28_all_components_preserved':True,'QO_acceptance_date_unselected':True,
        'acceptance_ordinary_deadline':'2023-10-02 undernewXI4+XLII2; extension/withdrawal laterrequireslawfulaction, not indefiniteROFRorQOamount',
        'new_QO_MAXimum_or_FRN_selected':False,'LaMelo_extension_selected':False},
      'rookie_and_cash_semantics':{'first_origin':'CHI','holder':'CHI','pick':16,'reserved_STD_slot':1,
        'new_RSC_price_or_draftee_selected':False,'S23_16':'PositiveNBA-prepared2023scale underI1hhh/iii; unroundedbaseline formula isnotpublishedadjustedtable certification',
        'N23_function':'1.2*S23(16) unsignedfirstnormalhold','A23_function':'ConformingunacceptedfirstRTSalary chosenonlyinthecostinputfamily;80..120%scale intersectminimum, no newbonus',
        'first_RT_form':'Two guaranteedSeasons+twoTeamoptions requiredVIII1; actualoffer/UPCidentity notcertified',
        'first_tender_deadline':'July15Saturday→July17,2023 underX4a+XLII2, candidatevalidtenderwithinwindow',
        'unsigned_hold_and_unaccepted_RT_cash_paid':False,'N23':None,'A23':None,
        'rookie_signing_replaces_same_hold_once_and_requires_remaining_STD_slot':True},
      'cost_family':{'live9_upper':132051061,'Coby_new_cash_and_Salary':12000000,
        'prepared_minimum_functions':min_screen,'prepared_exact_scale_table_or_rounding_certified':False,
        'July7_normal_apron_base_before_R23_first_hold_FRN_conditional_upper':base,
        'normal':'live9 +12m + min4 fullcash + Dotson/Cook standardQO_salary+Unlikely/FRN upper + R23 +1.2S23(16)',
        'apron':'sameconservativecashandRFAQOupper + R23 + conformingfirstRTSalary; UFAholds/unusedexceptionsexcluded',
        'R23':[0,16371000],'new_arbitrary_unreported_resolution_required_for_completion':False,
        'evaluator':SELF+'::evaluate_cost','preJuly7_FA_bank':copy.deepcopy(s[WINDOW]['FA_hold_function_bank']),
        'annual_unused_exceptions':copy.deepcopy(s[WINDOW]['annual_2023_exception_bank']),
        'unused_exception_renunciation_as_fictional_implementation_selected':True,
        'unused_exception_renunciation_scope':{'source_selection_literal_contains_this_step':False,
          'supplemental_routine_legal_means_under_existing_delegation':True,'candidate_date':'2023-07-07 before costcomparison',
          'objects':'Unused entitled/incorporated exception amounts only; no removal of signed contracts or Coby Bird service/FA right before signing',
          'validity':'2023VII6n2 express written validrenunciation; if a charge is not incorporated, no invented amount removed',
          'actual_written_notice_receipt_certified':False,'core_contract_or_draft_direction_changed':False},
        'removing_unused_exception_erases_signed_CarusoSalary':False,'old_hardcap_carries':False,
        'new_hardcap_trigger':False,'negative_apron_margin_automatically_illegal':False,
        'exact_tax':None,'whole_cost_upper':None,'whole_cost_is_complete':False},
      'certification':{'fictional_contract_execution_selected':True,'independent_consumer_review_completed':False,
        'actual_contract_player_acceptance_cash_receipt_or_clinical_certificate':False,'2023_rookie_or_LaMelo_extension_price_selected':False,
        'FY24_options_selected':True,'FY23_options_extra_salary':False,'whole_FY23_calendar_roles_or_results':False,
        'whole_macro3':False,'REGISTER_promotion':False,'new_manuscript':False},
      'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0}

def validate(o):
    try:
        assert o==build(),'Saved artifact differs from source-bound selected reconstruction'
        assert_rows(o['named_contracts_and_rights'],physical());assert_options(o['selected_FY24_option_notices']);assert_states(o['dated_states'],o['named_contracts_and_rights'])
        return []
    except (AssertionError,KeyError,ValueError,TypeError) as e:return [str(e)]
def md(o):
    return '\n'.join(['# Chicago 2023 선택 재계약 실행','',o['status'],'',
      '기존 root 위임으로 선택된 **Coby FullBird $12m×3**, Green/Wieskamp/Valentine/Sato의 한 시즌 법정최소 합의, Bradley의 유효 FA renounce, Dotson/Cook의 미수락 표준QO·권리 유지다. 원 비교 파일의 미선택 이력은 수정하지 않는다. 실제 선수 수락·UPC·지급 인증은 아니다.',
      '', '## 일자·명단','',
      'June28 QO 발행은 당시2017 CBA를 적용하고 Seasonend 이후 조건을 지킨다. July1 원9STD존속/6STD·2TW만료. July7 live9+새계약5=**14STD/0TW**, 새CHI16번 RSC를 위한 **STD1칸**을 남긴다. 권리만 보유한 두 선수를 UPC나 TW로 세지 않는다. 2023 regularSTD14–15/active12–15 검문은 후속 기용 함수의 별도 분야이며 여기서 임상·active 명단을 생성하지 않는다.',
      '', 'Cook은 원 두 연속1년CHI TW 종료로 표준QO를 발행한다. 이전 비교안의 noQO→새TW는 새 root 선택에서 쓰지 않는다. Dotson 네 번째CHI TW는 금지된다. Cook의YOS4 조건은 명명된 credited-service 가족이며0분=무YOS/임상증명으로 추론하지 않는다. 미수락QO에는 신규 급여 지급이나 UPC가 없지만 normal/apron의 법정 charge와 ROFR은 남는다. October2 이후 QO기간 연장·withdraw/renounce는 별도법적 조치가 필요하며 무기한 자동존속이 아니다.',
      '', 'October1 Duarte fourth/Kessler third 팀서명 통지는 FY24 옵션만 추가한다. upper Duarte **$6,133,005**, Kessler **$3,510,480**이며 FY23 비용0추가/STD0추가다. LaMelo 신규 extension은 계속 미선택, 현재 fourthyear만 유지한다.',
      '', '## 같은 비용과 지급의 구분','',
      f"존속9명 upper **$132,051,061**, Coby새$12m. 법정최소4명과 표준QO2명 fullcash/Salary 초과예약의 조건부 기준합은 **${o['cost_family']['July7_normal_apron_base_before_R23_first_hold_FRN_conditional_upper']:,}**이며 아직 `R23`, 신인hold/RT, 필요한FRN 입력 전이다.",
      '', '법정가격은 NBA가 준비한 `M23(YOS)`/`S23(16)` 함수다. 공개 ExC baseline×cap 법식의 floor..ceil+2는 명시된 조건부 수치screen이며 실제 준비표나 공식반올림을 인증하지 않는다. Normal unsigned first는 `1.2S23(16)`, apron은 실제 conformingRT Salary다. RT가격80–120%와 해당최소를 교차시킨 함수이며 신인·정확가격·수락을 선택하지 않는다. 미수락RT/QO의 장부charge를 현금지급으로 부르지 않는다.',
      '', 'Coby와 minimum 신규UPC는 같은 FA/QO claim을 한번 교체한다. Bradley renounce는 hold만 유효하게 없애고 원 보호 지급·Gamma를 지우지 않는다. Dotson/Cook hold·권리와 원 Gamma 유지, named legacy `R23∈[0,16.371m]`도 한 번 유지한다. 산입된 unused annual exceptions는 July7 비용비교 전 유효 서면renounce의 루틴 실행을 명시하고, 이미 서명된 Caruso급여는 제거하지 않는다. Bird/minimum/ownRSC/ownoptions만 쓰므로 새hardcap trigger0이며 기존hardcap을 이월하지 않는다. Apron 초과screen은 자동위법이 아니다.',
      '', '이 함수는 선택된 계약·통지의 실행 단위다. 전체 FY23 비용/상대/일정·건강·결과/LaMelo신규가격/장기계획은 인증하지 않는다. 실제private영수증은 작품설계 완료의 새gate가 아니다. 다음 실행은 법정 prepared 함수와 namedR23/FRN을 비용 evaluator에 공급하고 신인price/UPC를 남은 슬롯에 연결하는 한정 작업이다.',
      '',prior.progress()])+'\n'
def self_test():
    done=[];s=source_inputs()
    for label,name,field,val in [('same_owner_drop_Gamma','Protagonist','original_Gamma_full_components_and_protected_cash_preserved',False),
      ('Coby_min_replacement','Coby White','FY23_apron_upper',1200000),
      ('Dotson_fourth_live_TW','Devon Dotson','TW',1),('erase_Bradley_cash','Tony Bradley','renunciation_erases_original_protected_obligation',True)]:
        r=construct(s);next(x for x in r if x['player']==name)[field]=val
        try:
            with patch(__name__+'.construct',return_value=r):build()
        except AssertionError:done.append(label)
        else:raise AssertionError('FALSE PASS '+label)
    opt=option_notices();opt[0]['FY23_new_salary']=6133005
    try:
        with patch(__name__+'.option_notices',return_value=opt):build()
    except AssertionError:done.append('future_option_added_to_current_year')
    else:raise AssertionError('FALSE PASS FY23option')
    bad=copy.deepcopy(s);bad[SELECT]['selected_design']['Coby']['annual_salary']=[12000000,100000000,100000000]
    try:
        with patch(__name__+'.source_inputs',return_value=bad):build()
    except AssertionError:done.append('source_same_id_term_reversal')
    else:raise AssertionError('FALSE PASS source')
    try:evaluate_cost(prepared_minimums={y:prior.checked_minimum(y)['conditional_floor_ceil_rounding_screen'][1] for y in [0,2,3,4,7]},prepared_scale16=None,first_RT_base=1,R23=1)
    except AssertionError:done.append('null_unsigned_first_as_zero')
    else:raise AssertionError('FALSE PASS nullfirst')
    for label,name,fields in [('minimum_cash_deleted','Javonte Green',{'fullcash':0,'FY23_normal_upper':0,'FY23_apron_upper':0}),
      ('unaccepted_QO_charges_deleted','Devon Dotson',{'FA_hold':'0','apron_QO_plus_unlikely':'0'})]:
        r=construct(s);next(x for x in r if x['player']==name).update(fields)
        try:
            with patch(__name__+'.construct',return_value=r):build()
        except AssertionError:done.append(label)
        else:raise AssertionError('FALSE PASS '+label)
    for label,index,field,value in [('option_current_year_cost',3,'cost_function','FY23_OPTIONS_EXTRA_SALARY'),
      ('early_exception_renunciation',0,'annual_unused_exceptions','SELECTED_VALID_WRITTEN_RENUNCIATION_BEFORE_COST_COMPARISON'),
      ('double_count_signed_hold',2,'Coby_Green_Wieskamp_Valentine_Sato_hold','DOUBLE_COUNT')]:
        st=dated_states(construct(s));st[index][field]=value
        try:
            with patch(__name__+'.dated_states',return_value=st):build()
        except AssertionError:done.append(label)
        else:raise AssertionError('FALSE PASS '+label)
    return done
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args()
    o=build()
    if a.write:
        (ROOT/OUT).write_text(serial(o),encoding='utf8',newline='\n');(ROOT/OUT.replace('.json','.md')).write_text(md(o),encoding='utf8',newline='\n')
    err=[]
    if a.check:
        saved=json.loads((ROOT/OUT).read_text(encoding='utf-8-sig'));err=validate(saved)
        if norm((ROOT/OUT.replace('.json','.md')).read_text(encoding='utf-8-sig'))!=md(saved):err.append('Markdown stale')
    controls=self_test() if a.self_test else []
    print(json.dumps({'current':not err,'errors':err,'named':17,'STD':14,'TW':0,'reserved_first_slot':1,'dates':4,'negative_controls':controls},ensure_ascii=False))
    if err:raise SystemExit(1)
if __name__=='__main__':main()
