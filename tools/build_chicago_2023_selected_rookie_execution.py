"""Selected J16 dated RSC/registration/charge join; legal prepared amounts typed."""
from __future__ import annotations
import argparse,copy,hashlib,json,math
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import fitz
from bs4 import BeautifulSoup
import build_chicago_2023_selected_routine_execution as routine
import build_chicago_2023_routine_cost_domain as cost
import build_chicago_2023_rookie_candidate_family as candidate

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2023_selected_rookie_execution.py'
OUT='simulation/CHICAGO_2023_SELECTED_ROOKIE_EXECUTION.json'
SELECT='canon/DELEGATED_CHICAGO_2023_ROOKIE_DESIGN_SELECTION_2026_10_08.json'
PEER='reviews/CHI_2023_ROOKIE_CANDIDATE_FAMILY_ROOT_INDEPENDENT_REVIEW_2026_10_08.json'
COST_PEER='reviews/CHICAGO_2023_ROUTINE_COST_DOMAIN_G11_INDEPENDENT_REVIEW_2026_10_08.json'
PINS={SELECT:'760a89713400eb4e52de67139d7b708fce1df14d5ad694a4908299b3b49b70ba',
 candidate.OUTPUT:'aff589693b19e632ed8528a789a15ed81c362b002081060c79ebba53d506f1e9',
 candidate.SELF:'e719b6775be3ed91b7e116339b36314c74a1e218aea4299e74031dfa5742c305',
 PEER:'d77cc10b1e23502de0371011e630469c9249d01fe73f3d4f96cd191ccda698f5',
 routine.OUT:'9a4f6db21d6ad50e2c6d6897f1c2dedbdf440cee89bae47019f4bd131f341790',
 routine.SELF:'ba7ae8fcd0cf7ecb969c74aac1199ec761ec70319e508613339b02bb3c70b6df',
 cost.OUT:'13448f381896ee9da4da16e9716b98f7bb511ecd42b527dcba26802a64ba1f8d',
 cost.SELF:'c9adee889f9c90c5890bb944f7c322983e30440dcca5665efae31474b4202c68',
 COST_PEER:'a05b70a2234dd9efd4f3243f2f6a0e03cc7402f91ec477b12b3864ff626a3fb7',
 candidate.DRAW_ADOPTION:'6df7f62328263c0b3864e2d4a05cb4a5b56edbd332d5d31556627c6b421d9292',
 routine.SLOT:'abbcdaaa6ff14d277f88d47fa600320fc6458ec4b057e5a7b73b414b6fbabf30',
 candidate.PRIOR21:'f8c78e99cce1b02a051c94339b550fdb52205d3988db8bbe69b780559c3bc306',
 candidate.PRIOR22:'3bdad52ebaacda5abb23b9908b8ed3a9b85cfaa09d838819a959cd024a58e940'}
PLAYER='Jaime Jaquez Jr.'
POOL=['Amen Thompson','Anthony Black','Ausar Thompson','Bilal Coulibaly','Brandon Miller',
 'Cason Wallace','Dereck Lively II','Gradey Dick','Jarace Walker','Jett Howard','Jordan Hawkins',
 'Kobe Bufkin','Scoot Henderson','Taylor Hendricks','Victor Wembanyama']
RATIO=Fraction(767,500)
PAGES=[31,32,57,58,90,210,211,214,215,243,263,314,316,317,323,631]
OLDLAW=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
OLD_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
NBA_RAW=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-chi-2023-rookie-20261008/NBA2023results.raw')
NBA_SHA='65e8d8050780c179244fbe145784e8922819529ffe563516bd59a98392514e0f'

def norm(t):return t.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(norm((ROOT/p).read_text(encoding='utf-8-sig')).encode()).hexdigest()
def serial(o):return json.dumps(o,ensure_ascii=False,indent=2)+'\n'
def physical():
    for p,h in PINS.items():assert sha(p)==h,'Pinned physical input changed: '+p
    return {p:json.loads((ROOT/p).read_text(encoding='utf-8-sig')) for p in PINS if p.endswith('.json')}
def source_inputs():return physical()
def assert_sources(s):
    assert s==physical(),'Returned source differs from physical selected input'
    z=s[SELECT]
    assert z['selected_form']=='J16' and z['selected_player']==PLAYER and not z['new_human_author_lock']
    a=z['selected_antecedent_family']
    assert a['fictional_not_historical'] and a['prior_pick_positions']==list(range(1,16))
    assert a['distinct_eligible_players_required']==15 and a['selected_player_excluded_from_prior15']
    assert a['unordered_positive_witness_pool']==POOL
    assert not a['witness_is_actual_order_or_team_assignment'] and not a['team_specific_prior15_assignments_executed']
    assert z['selected_fictional_events']=={'draft_rights_selection_date':'2023-06-22','origin':'CHI','holder':'CHI','pick':16,
      'draft_selection_STD_delta':0,'June22_current_STD_count':None,'Required_Tender_date':'2023-07-07',
      'Required_Tender_salary':'max(4/5*S23(16,y), M23(service_y)) with legal year4 linkage',
      'RSC_signature_date':'2023-07-07','RSC_signature_after_required_tender':True,
      'selected_fictional_player_and_team_agreement':True,'salary_multiplier':'6/5','base_salary_first3':'6/5*S23(16,y)',
      'year4_base_salary':'year3_base_salary*767/500','first2_seasons_guaranteed':True,'team_options_years':[3,4],
      'future_option_notices_executed':False,'new_bonuses_or_loan':0,'full_base_skill_injury_protection':True,
      'exception':'OWN_FIRST_ROUND_ROOKIE_SCALE','new_hardcap_trigger':False,
      'July7_nonrookie_STD':14,'July7_post_signature_STD':15,'July7_TW':0}
    for p,h in z['source_sha256'].items():assert sha(p)==h,'Selection ancestor changed: '+p
    assert s[PEER]['independent_review_completed'] and s[PEER]['source_sha256'][candidate.OUTPUT]==PINS[candidate.OUTPUT]
    assert s[COST_PEER]['independent_review_completed']
    assert s[COST_PEER]['source_sha256'][cost.OUT]==PINS[cost.OUT]
    j=next(x for x in s[candidate.OUTPUT]['candidate_rows'] if x['id']=='J16')
    assert j['player']==PLAYER and j['historical_team']=='MIA' and j['historical_pick']==18
    assert not s[candidate.OUTPUT]['certification']['rookie_draft_or_UPC_selected']
    assert s[routine.SLOT]['Chicago_origin_first_slot']==16 and s[routine.SLOT]['Chicago_selected_holder']=='CHI'
    draw=s[candidate.DRAW_ADOPTION]['selected_thirty_first_and_thirty_second_origin_orders_before_holder_sanctions']
    assert next(x for x in draw if x['round']==1 and x['origin']=='CHI')['potential_origin_rank']==16
    state=next(x for x in s[routine.OUT]['dated_states'] if x['date']=='2023-07-07')
    assert state['STD_count']==14 and state['live_TW_UPC_count']==0 and state['reserved_first_STD_slot']==1
    assert s[routine.OUT]['cost_family']['July7_normal_apron_base_before_R23_first_hold_FRN_conditional_upper']==157912834
    assert s[cost.OUT]['domains']['R23']['interval']==[0,16371000]
    assert not s[cost.OUT]['event_frame']['new_offer_sheet_or_FirstRefusalExerciseNotice']
    priorplayers={r['player'] for r in s[candidate.PRIOR21]['selected_rows']}|{r['player'] for r in s[candidate.PRIOR22]['rows']}
    assert not priorplayers.intersection(set(POOL)|{PLAYER})

def primary():
    assert hashlib.sha256(candidate.CBA.read_bytes()).hexdigest()==candidate.CBA_SHA
    assert hashlib.sha256(OLDLAW.read_bytes()).hexdigest()==OLD_SHA
    assert hashlib.sha256(NBA_RAW.read_bytes()).hexdigest()==NBA_SHA
    d=fitz.open(candidate.CBA);old=fitz.open(OLDLAW)
    texts={n:norm(d[n-1].get_text()) for n in PAGES};body=BeautifulSoup(NBA_RAW.read_bytes(),'html.parser').get_text(' ',strip=True)
    assert all(n in body for n in POOL+[PLAYER]) and '2023 NBA Draft' in body
    assert 'July 15' in old[302].get_text() and 'Negotiating Rights' in old[302].get_text()
    assert '53.4%' in texts[631] and '2,946,800' in texts[631]
    return {'CBA2023':{'url':candidate.CBA_URL,'cache_path':str(candidate.CBA),'raw_sha256':candidate.CBA_SHA,
      'PDF1based_text_LF_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest() for n,t in texts.items()}},
      'CBA2017_June22_rights':{'cache_path':str(OLDLAW),'raw_sha256':OLD_SHA,
        'PDF1based_text_LF_sha256':{'303':hashlib.sha256(norm(old[302].get_text()).encode()).hexdigest()}},
      'NBA_eligible_witness':{'url':'https://cdn-uat.nba.com/news/2023-nba-draft-order','cache_path':str(NBA_RAW),
        'raw_sha256':NBA_SHA,'HTTP200_body_read':True,'body_locator':'First Round names; scope participation, excludes historical order/team assignment'},
      'source_scope':'CBA legal forms and historical eligible participation; actual fictional receipts and future NBA productivity uncertified'}
def assert_primary(p):
    # Physical identity and all cited page texts are re-read at caller boundary.
    assert p['source_scope']=='CBA legal forms and historical eligible participation; actual fictional receipts and future NBA productivity uncertified', 'Primary source scope exceeds verified legal forms and participation'
    assert p['CBA2023']['cache_path']==str(candidate.CBA) and p['CBA2023']['raw_sha256']==hashlib.sha256(candidate.CBA.read_bytes()).hexdigest()==candidate.CBA_SHA
    assert p['CBA2023']['url']==candidate.CBA_URL
    d=fitz.open(candidate.CBA)
    assert p['CBA2023']['PDF1based_text_LF_sha256']=={str(n):hashlib.sha256(norm(d[n-1].get_text()).encode()).hexdigest() for n in PAGES}
    old=fitz.open(OLDLAW)
    assert p['CBA2017_June22_rights']=={'cache_path':str(OLDLAW),'raw_sha256':hashlib.sha256(OLDLAW.read_bytes()).hexdigest(),
      'PDF1based_text_LF_sha256':{'303':hashlib.sha256(norm(old[302].get_text()).encode()).hexdigest()}}
    assert p['CBA2017_June22_rights']['raw_sha256']==OLD_SHA
    n=p['NBA_eligible_witness']
    assert n['cache_path']==str(NBA_RAW) and n['raw_sha256']==hashlib.sha256(NBA_RAW.read_bytes()).hexdigest()==NBA_SHA
    assert n['url']=='https://cdn-uat.nba.com/news/2023-nba-draft-order' and n['HTTP200_body_read']
    assert n['body_locator']=='First Round names; scope participation, excludes historical order/team assignment'

def availability():
    return {'selected_player':PLAYER,'prior_positions':list(range(1,16)),'witness_pool':POOL,
      'prior15_rule':'Injection of positions1..15 into selected eligible15 pool excluding Jaquez',
      'admitted_injection_count':math.factorial(15),'unique_pool':15,'Jaquez_available_at16':True,
      'witness_is_historical_first15_team_order':False,'specific_NPC_assignments_selected':False,
      'counterfactual_family_selected':True,'all60_holders_or_board_complete':False}
def assert_availability(a):
    assert a['selected_player']==PLAYER and a['prior_positions']==list(range(1,16))
    assert a['witness_pool']==POOL and len(set(a['witness_pool']))==15 and PLAYER not in a['witness_pool']
    assert a['prior15_rule']=='Injection of positions1..15 into selected eligible15 pool excluding Jaquez'
    assert a['admitted_injection_count']==math.factorial(15) and a['unique_pool']==15 and a['Jaquez_available_at16']
    assert a['counterfactual_family_selected'] and not a['witness_is_historical_first15_team_order'] and not a['specific_NPC_assignments_selected'] and not a['all60_holders_or_board_complete']

def contract():
    return {'player':PLAYER,'team':'CHI','origin':'CHI','selected_pick':16,'draft_date':'2023-06-22',
      'first_salary_capyear':2023,'RSC_signature_date':'2023-07-07','RSC_signature_after_valid_RT':True,
      'mechanism':'2023_VII6h_OWN_FIRST_ROUND_ROOKIE_SCALE','base_multiplier':'6/5',
      'base_functions':['6/5*S23(16,1)','6/5*S23(16,2)','6/5*S23(16,3)','6/5*S23(16,3)*767/500'],
      'minimum_conditions':'For each operative contractyear, prepared statutory M23(service_y)<=6/5*S23(16,y), y4 reference derived fromyear3',
      'first2_guaranteed_seasons':[2023,2024],'team_option_seasons':[2025,2026],
      'option_notices_exercised':False,'option_windows':'Third afterfirstSeason throughfollowingOct31; fourth aftersecondSeason throughfollowingOct31; lawfulXLII2 adjustment',
      'nonpayment_terms_year4_unchanged_from_year3':True,'full_base_skill_and_injury_protection':True,
      'new_signing_trade_performance_international_payment_bonus_or_loan':0,
      'last_possible_fiscal_end_if_both_options_exercised':'2027-06-30','fiscal_end_is_service_term_certificate':False,
      'new_hardcap_trigger':False,'STD_delta_at_UPC':1,'TW_delta':0,
      'actual_salary_cents_or_prepared_rounding_certified':False,'actual_assent_or_delivery_receipts':None,
      'selected_fictional_agreement':True,'future_minutes_health_BPM_awards_selected':False}
def assert_contract(c):
    assert c['player']==PLAYER and c['team']==c['origin']=='CHI' and c['selected_pick']==16
    assert c['draft_date']=='2023-06-22' and c['first_salary_capyear']==2023 and c['RSC_signature_date']=='2023-07-07' and c['RSC_signature_after_valid_RT']
    assert c['mechanism']=='2023_VII6h_OWN_FIRST_ROUND_ROOKIE_SCALE' and c['base_multiplier']=='6/5'
    assert c['base_functions']==['6/5*S23(16,1)','6/5*S23(16,2)','6/5*S23(16,3)','6/5*S23(16,3)*767/500']
    assert c['minimum_conditions']=='For each operative contractyear, prepared statutory M23(service_y)<=6/5*S23(16,y), y4 reference derived fromyear3'
    assert c['first2_guaranteed_seasons']==[2023,2024] and c['team_option_seasons']==[2025,2026] and not c['option_notices_exercised']
    assert c['option_windows']=='Third afterfirstSeason throughfollowingOct31; fourth aftersecondSeason throughfollowingOct31; lawfulXLII2 adjustment'
    assert c['nonpayment_terms_year4_unchanged_from_year3'] and c['full_base_skill_and_injury_protection']
    assert c['new_signing_trade_performance_international_payment_bonus_or_loan']==0
    assert c['last_possible_fiscal_end_if_both_options_exercised']=='2027-06-30' and not c['fiscal_end_is_service_term_certificate']
    assert c['STD_delta_at_UPC']==1 and c['TW_delta']==0 and not c['new_hardcap_trigger']
    assert not c['actual_salary_cents_or_prepared_rounding_certified'] and c['actual_assent_or_delivery_receipts'] is None
    assert c['selected_fictional_agreement'] and not c['future_minutes_health_BPM_awards_selected']

def events(s):
    names=next(x for x in s[routine.OUT]['dated_states'] if x['date']=='2023-07-07')['named_live_STD']
    return [
      {'order':1,'date':'2023-06-22','event':'SELECTED_J16_DRAFT_RIGHTS','STD':None,'TW':None,'STD_delta':0,'new_UPC':False,
       'NBA_salary_cash':0,'named_STD':None,'FY23_forward_unsigned_normal':'6/5*S23(16,1)','June22_exact_current_salary_certified':False},
      {'order':2,'date':'2023-07-07','event':'BEFORE_REQUIRED_TENDER','STD':14,'TW':0,'STD_delta':0,'new_UPC':False,
       'NBA_salary_cash':0,'named_STD':names,'FY23_normal_rookie':'6/5*S23(16,1)','FY23_apron_rookie':0},
      {'order':3,'date':'2023-07-07','event':'VALID_CONFORMING_REQUIRED_TENDER_BEFORE_RSC','STD':14,'TW':0,'STD_delta':0,'new_UPC':False,
       'NBA_salary_cash':0,'named_STD':names,'FY23_normal_rookie':'6/5*S23(16,1)','FY23_apron_rookie':'alpha_RT*S23(16,1)',
       'RT_alpha':'max(4/5,max_y M23(service_y)/S23(16,y)); commonalpha<=6/5, y4 linked',
       'acceptance_window':'At least firstRegularDay2023-24; later replaced by separately agreedRSC, not minimumRT acceptance',
       'delivery_form':'Team signed personal/email/certified/registered/overnight notice byJuly15; modeledJuly7',
       'actual_delivery':None},
      {'order':4,'date':'2023-07-07','event':'SELECTED_120_PERCENT_RSC_AFTER_TENDER','STD':15,'TW':0,'STD_delta':1,'new_UPC':True,
       'NBA_salary_cash':'6/5*S23(16,1)','named_STD':names+[PLAYER],'FY23_normal_rookie':'6/5*S23(16,1)',
       'FY23_apron_rookie':'6/5*S23(16,1)','same_unsigned_hold_and_RT_replaced_once':True,
       'original14_Gamma_R23_FA_QO_cost_preserved':True,'actual_assent_receipt':None}]
def assert_events(e,s):
    names=next(x for x in s[routine.OUT]['dated_states'] if x['date']=='2023-07-07')['named_live_STD']
    assert len(e)==4 and [x['order'] for x in e]==[1,2,3,4]
    assert e[0]=={'order':1,'date':'2023-06-22','event':'SELECTED_J16_DRAFT_RIGHTS','STD':None,'TW':None,'STD_delta':0,'new_UPC':False,
      'NBA_salary_cash':0,'named_STD':None,'FY23_forward_unsigned_normal':'6/5*S23(16,1)','June22_exact_current_salary_certified':False}
    for x,n,k,label in zip(e[1:],[14,14,15],[0,0,1],['BEFORE_REQUIRED_TENDER','VALID_CONFORMING_REQUIRED_TENDER_BEFORE_RSC','SELECTED_120_PERCENT_RSC_AFTER_TENDER']):
        assert x['date']=='2023-07-07' and x['event']==label and x['STD']==n and x['TW']==0 and x['STD_delta']==k and x['new_UPC']==bool(k)
        assert x['named_STD']==(names if not k else names+[PLAYER]) and len(set(x['named_STD']))==n
        assert x['FY23_normal_rookie']=='6/5*S23(16,1)' and x['NBA_salary_cash']==('6/5*S23(16,1)' if k else 0)
    assert e[1]['FY23_apron_rookie']==0
    assert e[2]['FY23_apron_rookie']=='alpha_RT*S23(16,1)' and e[2]['RT_alpha']=='max(4/5,max_y M23(service_y)/S23(16,y)); commonalpha<=6/5, y4 linked'
    assert e[2]['acceptance_window']=='At least firstRegularDay2023-24; later replaced by separately agreedRSC, not minimumRT acceptance'
    assert e[2]['delivery_form']=='Team signed personal/email/certified/registered/overnight notice byJuly15; modeledJuly7' and e[2]['actual_delivery'] is None
    assert e[3]['FY23_apron_rookie']=='6/5*S23(16,1)' and e[3]['same_unsigned_hold_and_RT_replaced_once']
    assert e[3]['original14_Gamma_R23_FA_QO_cost_preserved'] and e[3]['actual_assent_receipt'] is None

def cost_join():
    return {'conditional_nonrookie_base_upper':157912834,'R23_interval':[0,16371000],
      'signed_normal_apron_annual_outer':'157912834+R23+6/5*S23(16,1)',
      'normal_unsigned_to_signed_delta':'0: same6/5*S claim replaced once',
      'apron_RT_to_signed_delta':'(6/5-alpha_RT)*S23(16,1)>=0; not automaticallyzero',
      'rookie_new_cash_obligation':'6/5*S23(16,1), positive; RT/draft rights priorcash0 is not Salary0 afterUPC',
      'prior_all_performance_Gamma_protection_FA_QO_R23_and_renunciation_frame_preserved':True,
      'QO_postOct2_lifecycle':cost.OUT+'#/hold_lifecycle_through_FY23',
      'current_new_hardcap_trigger':False,'negative_apron_margin_is_automatic_illegality':False,
      'unused_RT_or_unsigned_claim_added_again_after_RSC':False,
      'RSC_is_FA_0YOS_apron_floor_contract':False,
      'Tax':'New annualplayerSalary within6/5S; exact lastRegular audit and allprioradjustments followparentcost, not synonymousnormal/apron',
      'N23_unsigned_actual_amount':None,'A23_pre_RSC_RT_actual_amount':None,'S23_actual_table_cents':None,
      'symbolic_player_and_team_cost_function_complete':True,'whole_actual_private_tax_or_cash_certificate':False}
def assert_cost_join(c,s):
    assert c['conditional_nonrookie_base_upper']==s[routine.OUT]['cost_family']['July7_normal_apron_base_before_R23_first_hold_FRN_conditional_upper']==157912834
    assert c['R23_interval']==s[cost.OUT]['domains']['R23']['interval']==[0,16371000]
    assert c['signed_normal_apron_annual_outer']=='157912834+R23+6/5*S23(16,1)'
    assert c['normal_unsigned_to_signed_delta']=='0: same6/5*S claim replaced once'
    assert c['apron_RT_to_signed_delta']=='(6/5-alpha_RT)*S23(16,1)>=0; not automaticallyzero'
    assert c['rookie_new_cash_obligation']=='6/5*S23(16,1), positive; RT/draft rights priorcash0 is not Salary0 afterUPC'
    assert c['prior_all_performance_Gamma_protection_FA_QO_R23_and_renunciation_frame_preserved']
    assert c['QO_postOct2_lifecycle']==cost.OUT+'#/hold_lifecycle_through_FY23'
    assert c['Tax']=='New annualplayerSalary within6/5S; exact lastRegular audit and allprioradjustments followparentcost, not synonymousnormal/apron', 'Tax scope must preserve positive player salary and parent adjustments'
    for k in ['current_new_hardcap_trigger','negative_apron_margin_is_automatic_illegality','unused_RT_or_unsigned_claim_added_again_after_RSC','RSC_is_FA_0YOS_apron_floor_contract','whole_actual_private_tax_or_cash_certificate']:assert c[k] is False
    assert all(c[k] is None for k in ['N23_unsigned_actual_amount','A23_pre_RSC_RT_actual_amount','S23_actual_table_cents'])
    assert c['symbolic_player_and_team_cost_function_complete']

def evaluate(scale,contract_year_minimum,R23):
    ss=list(map(Fraction,scale));mm=list(map(Fraction,contract_year_minimum))
    assert len(ss)==len(mm)==4 and all(x>0 for x in ss+mm)
    assert ss[3]==ss[2]*RATIO,'Year4 scale reference must preserve source53.4% linkage'
    alpha=max(Fraction(4,5),max(m/s for m,s in zip(mm,ss)))
    assert alpha<=Fraction(6,5),'No lawful120percent RSC below statutory minimum'
    assert R23 is not None and 0<=Fraction(R23)<=16371000
    signed=[Fraction(6,5)*x for x in ss];tender=[alpha*x for x in ss]
    return {'input_domain':'Lawful NBA-prepared2023 firstthree-year scale and applicable contractyearminimum; fourth reference derived, no private cents certificate',
      'RT_common_alpha':str(alpha),'RT_base_each_year':list(map(str,tender)),
      'selected_RSC_base_each_year':list(map(str,signed)),
      'normal_unsigned_hold':str(signed[0]),'normal_signed_player_salary':str(signed[0]),
      'apron_pre_signature_RT':str(tender[0]),'apron_signed_player_salary':str(signed[0]),
      'normal_claim_replacement_delta':'0','apron_claim_replacement_delta':str(signed[0]-tender[0]),
      'conditional_normal_apron_team_outer':str(Fraction(157912834)+Fraction(R23)+signed[0]),
      'new_annual_player_cash_obligation':str(signed[0]),'actual_prepared_rounding_or_cash_receipt':False}

def build():
    s=source_inputs();assert_sources(s);p=primary();assert_primary(p)
    a=availability();assert_availability(a);c=contract();assert_contract(c)
    e=events(s);assert_events(e,s);j=cost_join();assert_cost_join(j,s)
    return {'id':'CHICAGO_2023_SELECTED_ROOKIE_EXECUTION','status':'REVIEW_PENDING_SELECTED_J16_DATED_RSC_REGISTRATION_AND_COST_FUNCTION',
      'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8_BOM_STRIPPED_CRLF_CR_TO_LF_EXTERNAL_RAW_SEPARATE',
      'primary':p,'selected_antecedent_availability_family':a,'selected_contract':c,'dated_events':e,
      'post_signature_named_STD':e[3]['named_STD'],'post_signature_STD':15,'post_signature_TW':0,
      'cost_join':j,'evaluator':SELF+'::evaluate',
      'future_ports':{'Jaquez_FY23_role_clock_health_BPM_awards':'UNSELECTED_NEW_INPUT',
        'MIA_replacement':'Jaquez unavailable toMIA; nextnamedconsumer, noautomaticplayer/compensation',
        'rookie_option_notices':'Laterlawfulsourcewindows; currentnotice0',
        'other59_draft_assignments':'Existing selectedantecedentinjectionfamily only; wholeboard/holders notcertified'},
      'certification':{'selected_fictional_J16_draft_RT_and_RSC':True,'dated_15STD_registration_and_charge_family_complete':True,
        'independent_consumer_review_completed':False,'new_human_author_lock':False,
        'actual_contract_player_assent_delivery_salary_cents_or_clinical_certificate':False,
        'future_full_team_cost_results_or_60board':False,'new_protagonist_franchise_MVP_title_or_ending':False,
        'whole_macro3':False,'REGISTER_promotion':False,'manuscript':False},
      'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0}
def validate(o):
    try:
        assert o==build(),'Saved rookie consumer differs from physical selected reconstruction'
        s=physical();assert_primary(o['primary']);assert_availability(o['selected_antecedent_availability_family'])
        assert_contract(o['selected_contract']);assert_events(o['dated_events'],s);assert_cost_join(o['cost_join'],s)
        return []
    except (AssertionError,KeyError,ValueError,TypeError) as e:return [str(e)]
def md(o):
    return '\n'.join(['# Chicago 2023 선택 J16 신인 실행','',o['status'],'',
      '**Jaime Jaquez Jr.·CHI 자체16번**을 root가 선택한 가상 draft→RT→RSC로 연결했다. 원 세 후보 파일의 미선택 표시와 peer 당시 앞선15 미선택 이력은 수정하지 않는다. 이후 canon이 선택한 가족과 이번 소비자가 별도 실행권위다. 실제 NBA의MIA18·원계약·차기 성과를 복사하지 않는다.','',
      '## 앞선15와 명단','',
      '선택된 NBA 원참가15명 pool에서 앞선1..15를 고유하게 배정하는 **15! injection 가족**은 Jaquez를 제외한다. 원NBA 본문은 참가 이름의 양성근거로만 쓰고 원팀·순서의 실제배정으로 쓰지 않는다. 지명 당시CHI보유16·원2021/2022선택보드와 중복0을 연결한다. 전체60보드의정확선수/권리/양도는 이번 증인의 완료주장이 아니다.','',
      '| 순서 | 날짜 | 법적 실행 | STD/TW | 새 cash |','|---|---|---|---|---|',
      '| 1 | June22 | J16 지명권만; 당시2017법 | null/null, delta0 | 0 |',
      '| 2 | July7 RT 전 | 기존14STD; FY23 unsigned firsthold | 14/0 | 0 |',
      '| 3 | July7 | 팀서명 유효 Required Tender, 수락창>=정규첫날 | 14/0 | 미수락offer0 |',
      '| 4 | July7 RT 뒤 | 별도 합의한120% RSC | 15/0 | 양수1.2S23(16,1) |','',
      'June22의 current명단·급여는 인증하지 않는다. July7의 숫자는 이후FY23 명명명단이며 과거로 소급하지 않는다. 현재15명은 원14+Jaquez이고 Dotson/Cook 권리·Bradley 원보호채무는 새UPC 슬롯으로 세지 않는다. 선수등록을 임상/active/실제receipt로 인증하지 않는다.','',
      '## RT와 계약가격','',
      '`S23(16,1..3)`은 실제법에 따른 NBA-prepared 값이다. 4년차는 독립값이 아니라 `S3×767/500`(53.4% 증가)이다. 법정 table/cents/반올림을 실제발행표 인증으로 부르지 않는다. 법정최소 각년도를 함께 입력해 **RT commonalpha=max(80%, 모든년 M/S)**가120%이하인지 검사하고 연동된4년차도 지킨다. RT는 이를 충족하는 제안이고 이후RSC가격은 **정확선택배수120%**다. 개별 RT floor가 80%보다 높아지는 경우를 누락하지 않으며 RT최저를 서명가격으로 잘못 교체하지 않는다.','',
      '2023VII6h/VIII1: 첫2Season guaranteed,3/4Teamoptions·full base skill/injury protection·신규bonus/loan0. 옵션통지는 미래 첫/둘째Season 종료 다음날~다음Oct31의 법정창이고 현재행사0이다. 당해 기본금액은 `1.2S1/1.2S2/1.2S3`; 옵션4는 `1.2S3×767/500`. 실제 원MIA18가격은 사용하지 않는다.','',
      '## 같은 비용·급여·현금','',
      'Normal의 unsigned1.2S가 signed1.2S로 한 번 교체되어 **normal delta0**다. Apron은 미서명RT alphaS→UPC1.2S이므로 delta=(1.2-alpha)S>=0이다. RT/hold를 새UPC에 다시 더하지 않는다. 조건부 최소screen의 원기준157,912,834+R23[0,16,371,000]+신인1.2S를 그대로 이어 받되 정확private total로 확정하지 않는다. 원Γ·모든성과·보호지급·unrenounced FA/QO와Oct2이후 lifecycle·unusedrenounce는 parentcost범위를 보존한다. Tax와actualcash는 별도 정의이며 새 신인 현금의무는 양수이고 미수락offer0cash와 구분한다.','',
      '이 서명은 ownfirst RSC Exception으로 새hardcap을 유발하지 않는다. 기존민감도상단의apron 초과를 자동위법으로 바꾸지 않는다. Rookie RSC는0YOS FA계약의apronfloor로 재분류하지 않는다. 아직 미래 옵션행사·FY23신인역할/건강/awards·MIA대체선수/전체시즌을 선택하지 않았다. 실제영수증·임상미회수는 합법가상설계의 새완료gate가 아니다.','',
      '## 원천·검문','',
      '[공식 NBA 참가본문](https://cdn-uat.nba.com/news/2023-nba-draft-order) raw65e8d805…e0f를 직접 읽고 참가15+Jaquez를 대조했다. 2017X4 PDF303으로June22 rights를, 2023I/II/VII/VIII/X PDF31–32/57–58/90/210–215/243/263/314/316–317/323와ExB631을RT·RSC·cost에 연결했다. 원문raw와 LF추출page지문을 구분하고 반환source/명단/법형식/cost를 caller에서 직접검문한다. 작성자음성은 독립검문이 아니다.','',routine.prior.progress()])+'\n'
def self_test():
    s=source_inputs();done=[]
    for label,helper,mutate in [
      ('wrong_rookie_owner','contract',lambda x:x.update(team='MIA')),
      ('options_preexercised','contract',lambda x:x.update(option_notices_exercised=True)),
      ('minimum_RT_is_signed_UPC','contract',lambda x:x.update(base_multiplier='4/5')),
      ('Jaquez_already_prior15','availability',lambda x:x['witness_pool'].__setitem__(0,PLAYER)),
      ('double_unsigned_claim','cost_join',lambda x:x.update(unused_RT_or_unsigned_claim_added_again_after_RSC=True)),
      ('erase_original_Gamma','cost_join',lambda x:x.update(prior_all_performance_Gamma_protection_FA_QO_R23_and_renunciation_frame_preserved=False)),
      ('June22_future_STD15','events',lambda x:x[0].update(STD=15)),
      ('primary_identity_changed','primary',lambda x:x['CBA2023'].update(raw_sha256='0'*64)),
      ('Tax_actual_zero_and_salary_erasure','cost_join',lambda x:x.update(Tax='Exact total tax is zero and no player salary applies')),
      ('primary_scope_actual_receipts_and_exact_cents','primary',lambda x:x.update(source_scope='NBA official receipt and exact salary cents certified'))]:
        b=globals()[helper](s) if helper=='events' else globals()[helper]();mutate(b)
        try:
            with patch(__name__+'.'+helper,return_value=b):build()
        except AssertionError:done.append(label)
        else:raise AssertionError('FALSE PASS '+label)
    try:evaluate([100,105,110,Fraction(110)*RATIO],[121,1,1,1],0)
    except AssertionError:done.append('120percent_below_legalminimum')
    else:raise AssertionError('FALSE PASS legal minimum')
    return done
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();o=build()
    if a.write:
        (ROOT/OUT).write_text(serial(o),encoding='utf8',newline='\n');(ROOT/OUT.replace('.json','.md')).write_text(md(o),encoding='utf8',newline='\n')
    err=[]
    if a.check:
        saved=json.loads((ROOT/OUT).read_text(encoding='utf-8-sig'));err=validate(saved)
        if norm((ROOT/OUT.replace('.json','.md')).read_text(encoding='utf-8-sig'))!=md(saved):err.append('Markdown stale')
    tests=self_test() if a.self_test else []
    print(json.dumps({'current':not err,'errors':err,'selected':'J16','post_STD':15,'post_TW':0,'future_roles_selected':False,'negative_controls':tests},ensure_ascii=False))
    if err:raise SystemExit(1)
if __name__=='__main__':main()
