"""Construct delegated same-owner FY22 NPC legal routine implementation families.

Year2 carry is supported. Current-valid and a later team's Under Contract list
are not an identity proof for an old UPC. All remaining ports are named.
"""
from __future__ import annotations
import argparse,copy,csv,hashlib,io,json,re,unicodedata
from collections import Counter,defaultdict
from pathlib import Path
from unittest.mock import patch
import fitz

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_23_npc_contract_portfolio.py'
OUT='simulation/NBA_2022_23_NPC_CONTRACT_PORTFOLIO.json'
MD=OUT.replace('.json','.md')
AUDIT='research/NBA_2022_23_ROLLOVER_FINITE_INPUT_AUDIT_2026_10_08.json'
AUDIT_SHA='39f26fc6404b1df2b7a53b56d9da4cd49530d4ba8c0c3207533d0146a641c785'
GLOBAL='simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json'
CHI='simulation/CHICAGO_2022_23_SELECTED_DATED_ROLES.json'
CAL='simulation/NBA_2022_23_PUBLISHED_CALENDAR.csv'
BASELINE='31e424c1662f5fa03c2a27c9d0b3a88f8c420a78'
TEMP=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-npc22-profiles-20261008')
EXTERNAL_PINS={'web_observations.json':'283777f602acf206fc63e087f3546560be4e055b7054ea4323c7b14f05d79647',
 'retrievals.json':'e76b0e07e5e5dd8b5f06ccd3c733f0bec3658e506b798a5b034e7647270548d4'}
POSITIONS=('PG','SG','SF','PF','C')
YEAR2={'2021_FIRST_RSC_GUARANTEED_YEAR2_REUSE','2021_EXPLICIT_MULTIYEAR_YEAR2_REUSE'}
EXPIRY='2021_ONE_SEASON_EXPIRY_RENEWAL_PORT'
OPTION='ORIGINAL_OPTION_TERM_AND_NEXT_OPTION_PORT'
TW='TW_EXPIRY_ELIGIBILITY_QO_AND_SLOT_PORT'
IMPORTANT={'James Harden','Kyrie Irving','Bradley Beal','Kawhi Leonard','Norman Powell',
 'Deandre Ayton','Collin Sexton','Miles Bridges','Jalen Brunson','Lonzo Ball','Josh Hart'}
ALIASES={'camthomas':'cameronthomas','boneshyland':'nahshonhyland','robertwilliamsiii':'robertwilliams',
 'joshuaprimo':'joshprimo','joshprimo':'joshprimo','garrisonmatthews':'garrisonmathews',
 'ludort':'luguentzdort','juan-toscanoanderson':'juantoscanoanderson','willhernangomez':'willyhernangomez',
 'moritzwagner':'mowagner','nahshonhyland':'nahshonhyland','isaiah thomas':'isaiahthomas'}

def norm(s):return s.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
def text(p):return norm((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def dump(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def key(s):
 s=unicodedata.normalize('NFKD',s.split(' (')[0]);s=''.join(c for c in s if not unicodedata.combining(c))
 s=re.sub('[^a-z0-9]','',s.lower());return ALIASES.get(s,s)
def physical():
 assert sha(AUDIT)==AUDIT_SHA,'Original finite audit snapshot changed'
 a=json.loads(text(AUDIT))
 for p,h in a['source_sha256'].items():assert sha(p)==h,'Pinned original source changed: '+p
 ext={}
 for name,h in EXTERNAL_PINS.items():
  p=TEMP/name;raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==h,'External observation changed: '+name
  ext[name]=json.loads(raw)
 for r in ext['retrievals.json']:
  if r.get('cache_path'):
   raw=Path(r['cache_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==r['raw_sha256']
  assert r['adopted_body'] is False,'403 response promoted to original body'
 return {'audit':a,'global':json.loads(text(GLOBAL)),'chi':json.loads(text(CHI)),
         'profiles':ext['web_observations.json'],'attempts':ext['retrievals.json'],
         'calendar':list(csv.DictReader(io.StringIO(text(CAL))))}
def inputs():return physical()
def assert_inputs(s):
 assert s==physical(),'Input object differs from pinned physical source'
 assert len(s['audit']['NPC_contract_input_rows'])==442
 assert len(s['audit']['selected_NPC_2022_draft_rights'])==58
 assert len(s['profiles'])==28 and len(s['attempts'])==29
 assert len(s['global']['owner_catalog'])==459
 assert s['chi']['selected_role_template']['registered_STANDARD'][-1]=='Walker Kessler'
 assert s['chi']['selected_role_template']['registered_TWO_WAY']==['Devon Dotson','Tyler Cook']

def profile_hits(name,s):
 result=[]
 for p in s['profiles']:
  for field in ('under_contract','free_agents'):
   for r in p[field]:
    if key(name)==key(r['name']):result.append({'url':p['url'],'class':field,
      'reported_name':r['name'],'web_body_line':r['web_body_line'],
      'source_role':p['source_role'],'same_original_UPC_identity_certified':False})
 return result
def execution_policy(group):
 """q changes no live original UPC; valid external status determines its branch.

 Original season terms expire at June30, not at an invented midseason date.
 Every renewal is an own-team consensual form, including an applicable RFA.
 This is a declared fictional implementation, not an original UPC fact.
 """
 if group in YEAR2:branches=['ORIGINAL_LIVE_FY22']
 elif group in (EXPIRY,OPTION):branches=['EXPIRED_BEFORE_FY22']
 elif group==TW:branches=['ORIGINAL_TW_LIVE','ORIGINAL_TW_EXPIRED']
 else:branches=['ORIGINAL_LIVE_FY22','VALID_ORIGINAL_FY22_OPTION','EXPIRED_BEFORE_FY22']
 return {'delegated_same_owner_routine_implementation_selected':True,
  'admitted_original_statuses':branches,'service_window':['2022-07-07','2023-04-09'],
  'ORIGINAL_LIVE_FY22':'Carry the legally operative original full FY22 UPC without changing any term or Gamma',
  'VALID_ORIGINAL_FY22_OPTION':'Exercise the existing one-season option by its original lawful deadline and retain every original term/Gamma; valid party consent/notice is a fictional execution condition',
  'EXPIRED_BEFORE_FY22':'Same prior team and player consensually sign one fully protected season on July7 under VII6i/II6; no bonus, option, S&T or competing accepted offer sheet',
  'ORIGINAL_TW_LIVE':'Ordinary lawful waiver and clearance before regular-season registration; preserve full original protected Gamma and all applicable rights/holds; no new UPC',
  'ORIGINAL_TW_EXPIRED':'No new UPC, preserve applicable FA/QO/rights and original Gamma; no automatic renunciation or zero-charge claim',
  'new_minimum_salary':'Applicable 2022 signing-year II6 minimum at credited YOS; positive symbolic amount, not zero',
  'new_minimum_term_seasons':1,'new_minimum_bonus':0,'new_minimum_option':False,
  'original_Gamma_preserved':True,'actual_original_endpoint_or_option_receipt_certified':False,
  'actual_agreement_or_waiver_clearance_certified':False,'franchise_move_selected':False,
  'FY22_implementation_function_covers_each_used_date':True,
  'all_price_agreements_are_fictional_not_market_likelihood_certificates':True}
def assert_execution_policy(p,group):
 assert p==execution_policy(group),'Same-owner routine law/term/Gamma policy changed'
 assert p['new_minimum_term_seasons']==1 and p['new_minimum_bonus']==0
 assert p['original_Gamma_preserved'] and p['actual_original_endpoint_or_option_receipt_certified']is False
def resolve_contract(row,status):
 p=row['execution_policy'];assert status in p['admitted_original_statuses'],'Original status outside named admitted domain'
 tw=row['prior_registration_class']=='TW'
 renew=status=='EXPIRED_BEFORE_FY22'
 return {'player':row['player'],'owner':row['candidate_owner'],'original_status':status,
  'registration':None if tw else 'STANDARD',
  'action':('LAWFUL_WAIVER_CLEARANCE_NO_NEW_UPC' if status=='ORIGINAL_TW_LIVE' else
    'EXPIRY_NO_NEW_UPC' if tw else 'OWN_TEAM_CONSENSUAL_ONE_YEAR_MINIMUM' if renew else
    'TIMELY_EXISTING_OPTION_EXERCISE_AND_CARRY' if status=='VALID_ORIGINAL_FY22_OPTION' else 'ORIGINAL_LIVE_UPC_CARRY'),
  'new_standard_UPC':renew,'new_TW_UPC':False,
  'new_price_function':'II6_2022_SIGNING_YEAR_CREDITED_YOS_MINIMUM' if renew else None,
  'new_bonuses':0,'new_term_seasons':1 if renew else None,
  'full_original_Gamma_preserved':True,'Gamma_exact':None,
  'FY22_regular_window_covered':True,
  'operative_contract_or_option_validity_required':not renew and not tw,
  'consensual_renewal_no_competing_accepted_offer_sheet_required':renew,
  'same_owner_FA_RFA_allowed_under_XI1a':renew,
  'waiver_clearance_before_opening_and_all_prior_protection_preserved_required':status=='ORIGINAL_TW_LIVE',
  'actual_receipt_or_consent_certified':False}
def assert_resolution(z,row,status):
 assert z['player']==row['player'] and z['owner']==row['candidate_owner'] and z['original_status']==status
 tw=row['prior_registration_class']=='TW';renew=status=='EXPIRED_BEFORE_FY22'
 assert z['registration']==(None if tw else 'STANDARD') and z['new_standard_UPC']==renew and z['new_TW_UPC']is False
 expected=('LAWFUL_WAIVER_CLEARANCE_NO_NEW_UPC' if status=='ORIGINAL_TW_LIVE' else
  'EXPIRY_NO_NEW_UPC' if tw else 'OWN_TEAM_CONSENSUAL_ONE_YEAR_MINIMUM' if renew else
  'TIMELY_EXISTING_OPTION_EXERCISE_AND_CARRY' if status=='VALID_ORIGINAL_FY22_OPTION' else 'ORIGINAL_LIVE_UPC_CARRY')
 assert z['action']==expected and z['full_original_Gamma_preserved']is True and z['Gamma_exact']is None
 assert z['new_price_function']==('II6_2022_SIGNING_YEAR_CREDITED_YOS_MINIMUM'if renew else None)
 assert z['new_bonuses']==0 and z['new_term_seasons']==(1 if renew else None)
 assert z['FY22_regular_window_covered']is True and z['actual_receipt_or_consent_certified']is False
 assert z['operative_contract_or_option_validity_required']==(not renew and not tw)
 assert z['consensual_renewal_no_competing_accepted_offer_sheet_required']==renew
 assert z['same_owner_FA_RFA_allowed_under_XI1a']==renew
 assert z['waiver_clearance_before_opening_and_all_prior_protection_preserved_required']==(status=='ORIGINAL_TW_LIVE')
def contract_rows(s):
 rows=[]
 for i,r in enumerate(s['audit']['NPC_contract_input_rows']):
  grp=r['group'];hits=profile_hits(r['player'],s)
  if grp in YEAR2:mechanism='CARRY_2021_UPC_YEAR2';term='SUPPORTED_2021_YEAR2_COVERS_FY22';gap=None
  elif grp==EXPIRY:mechanism='NEW_2022_ONE_SEASON_MINIMUM_CANDIDATE';term='ORIGINAL_ONE_SEASON_ENDS_2022_06_30';gap=None
  elif grp==OPTION:mechanism='EXERCISED_2021_LAST_OPTION_EXPIRES_THEN_RENEWAL_CANDIDATE';term='ORIGINAL_2021_OPTION_YEAR_ONLY';gap=None
  elif grp==TW:mechanism='NO_NEW_UPC_RIGHTS_QO_AND_ELIGIBLE_RENEWAL_PORT';term='TW_FY22_ENDPOINT_ELIGIBILITY_PORT';gap='TW_CURRENT_TERM_YOS_TEAM_CAPYEARS_PRIOR_LIST_USAGE'
  else:
   mechanism='ORIGINAL_UPC_END_OR_NEXT_OPTION_NAMED_FUNCTION';term='PUBLIC_FY22_CLASSIFICATION_WITH_SAME_UPC_LINK_PENDING' if hits else 'MISSING_TYPED_FY22_TERM';gap='ORIGINAL_UPC_FY22_YEAR_END_OPTION_OR_EXPLICIT_RENEWAL_FORM'
  x={'id':r['prior_owner']+':'+r['player'],'player':r['player'],'candidate_owner':r['prior_owner'],
    'prior_registration_class':r['prior_registration_class'],'original_group':grp,
    'original_source':r['source'],'original_locator':r['contract_locator'],
    'original_contract_fields':copy.deepcopy(r['source_contract_projection']),
    'original_term_fields':copy.deepcopy(r['explicit_term_fields']),
    'source_audit_pointer':AUDIT+'#/NPC_contract_input_rows/'+str(i),
    'mechanism':mechanism,'term_status':term,'named_missing_input':gap,
    'candidate_registration':None if grp==TW else 'STANDARD',
    'original_all_Gamma_reserved':True,'original_Gamma':None,
    'original_Gamma_domain':'All applicable preserved original contract liabilities; no charge deletion upon expiration/waiver',
    'FY22_current_salary':None,'FY22_current_salary_type':'Applicable original Year2/currentSalary if operative; otherwise explicit new legal form price function',
    'renewal_proposal':({'term_seasons':1,'signing_date':'2022-07-07','mechanism':'VII6(i)_MINIMUM_EXCEPTION',
       'salary_function':'II6 signing-year2022 scale for credited FY22 YOS, subject to valid mandatory minimum',
       'salary_amount':None,'bonuses':0,'full_base_protection_proposed':True,
       'no_player_or_team_option':True,'new_assignment_or_sign_and_trade':False,
       'ordinary_minimum_form_only_not_credible_star_price':r['player'] in IMPORTANT,
       'actual_agreement':False} if grp in (EXPIRY,OPTION) else None),
    'important_direction_or_price_candidate':r['player'] in IMPORTANT,
    'FY22_all_dates_covered_without_additional_term_input':grp in YEAR2,
    'function_domain':{'start':'2022-07-01','last_regular_date':'2023-04-09',
      'operative_UPC_covers_each_used_date_required':True,'future_term_or_original_option_year':None,
      'notice_before_original_contract_deadline_required':True,
      'new_renewal_not_entered_during_moratorium':True,
      'QO_receipt_if_RFA_claimed':None,'cap_hold_amount':None,'normal_or_apron_charge_not_zero_from_no_UPC':True},
    'TW_port':({'new_TW_selected':False,'new_standard_UPC_selected':False,'YOS_at_signing':None,
       'maximum_YOS_any_contract_season':3,'same_team_capyears_before_new_TW':None,
       'same_team_after_new_TW_max':3,'term_seasons_max':2,'future_conversion':None,
       'standard_QO_vs_TW_QO_requires_XI1c3_source_branch':True,
       'RFA_prior_active_or_inactive_15day_rule_and_2022_applicable_overlay_required':True,
       'QO_latest_issue':'2022-06-29','minimum_acceptance_date':'2022-10-01',
       'actual_QO_delivery':None,'active_games_selected':0,'medical_clearance':None} if grp==TW else None),
    'execution_policy':execution_policy(grp),
    'actual_contract_receipt_or_current_salary_certified':False,'NPC_policy_selected':True}
  rows.append(x)
 return rows
def assert_contract_rows(rows,s):
 orig=s['audit']['NPC_contract_input_rows'];assert len(rows)==len(orig)==442
 assert len({r['id']for r in rows})==442
 for r,a in zip(rows,orig):
  assert (r['player'],r['candidate_owner'],r['prior_registration_class'])==(a['player'],a['prior_owner'],a['prior_registration_class']),'Wrong player/year/owner'
  assert r['original_contract_fields']==a['source_contract_projection'] and r['original_term_fields']==a['explicit_term_fields'],'Original UPC meaning changed'
  assert r['original_source']==a['source'] and r['original_locator']==a['contract_locator']
  assert r['original_all_Gamma_reserved'] is True and r['original_Gamma'] is None,'Preserved original liabilities erased or selected'
  assert r['FY22_current_salary'] is None and r['actual_contract_receipt_or_current_salary_certified'] is False
  assert r['NPC_policy_selected'] is True and r['function_domain']['future_term_or_original_option_year'] is None
  assert_execution_policy(r['execution_policy'],a['group'])
  assert r['function_domain']['start']=='2022-07-01' and r['function_domain']['last_regular_date']=='2023-04-09'
  assert r['function_domain']['operative_UPC_covers_each_used_date_required'] is True
  assert r['public_2022_profile_classification']==profile_hits(a['player'],s)
  group=a['group']
  mechanism=('CARRY_2021_UPC_YEAR2' if group in YEAR2 else
    'NEW_2022_ONE_SEASON_MINIMUM_CANDIDATE' if group==EXPIRY else
    'EXERCISED_2021_LAST_OPTION_EXPIRES_THEN_RENEWAL_CANDIDATE' if group==OPTION else
    'NO_NEW_UPC_RIGHTS_QO_AND_ELIGIBLE_RENEWAL_PORT' if group==TW else
    'ORIGINAL_UPC_END_OR_NEXT_OPTION_NAMED_FUNCTION')
  assert r['mechanism']==mechanism,'Contract mechanism source meaning changed'
  assert r['FY22_all_dates_covered_without_additional_term_input']==(a['group']in YEAR2),'Generic current-valid extended to FY22'
  assert r['candidate_registration']==(None if a['group']==TW else 'STANDARD')
  if a['group'] in (EXPIRY,OPTION):
   p=r['renewal_proposal'];assert p['term_seasons']==1 and p['signing_date']=='2022-07-07' and p['mechanism']=='VII6(i)_MINIMUM_EXCEPTION'
   assert p['bonuses']==0 and p['salary_amount']is None and p['full_base_protection_proposed'] is True
   assert p['actual_agreement']is False and p['new_assignment_or_sign_and_trade']is False
  elif a['group']==TW:
   p=r['TW_port'];assert p['new_TW_selected']is False and p['new_standard_UPC_selected']is False
   assert p['YOS_at_signing']is None and p['same_team_capyears_before_new_TW']is None
   assert p['maximum_YOS_any_contract_season']==3 and p['same_team_after_new_TW_max']==3
   assert p['QO_latest_issue']=='2022-06-29' and p['active_games_selected']==0

def rights_rows(s):
 out=[]
 for d in s['audit']['selected_NPC_2022_draft_rights']:
  first=d['round']==1
  out.append({**copy.deepcopy(d),'candidate_owner':d['conditional_final_rights_holder'],
    'new_UPC_selected':False,'STD_added':0,'TW_added':0,
    'required_tender_candidate':{'offer_date':'2022-07-07' if first else '2022-08-25',
      'window_first':'2022-06-23' if first else '2022-08-22',
      'window_last':'2022-07-15' if first else '2022-09-05',
      'minimum_acceptance_until':'2022-10-18' if first else '2022-10-15',
      'form':'VIII1_RSC_FIRST2_PLUS2_OPTIONS' if first else 'ONE_SEASON_II6_ROOKIE_MINIMUM',
      'offer_and_player_nonacceptance_are_candidate_conditions':True,
      'no_UPC_acceptance_before_last_regular_date':'2023-04-09',
      'actual_delivery':None,'actual_nonacceptance':None},
    'rights_only_nonacceptance_is_conditional_sensitivity_not_collective_NBA_nonentry_selection':True,
    'normal_cap_hold_or_tender_cost':None,'apron_charge':None,
    'positive_unsigned_first_hold_preserved':first,
    'rights_exclusive_window_end':'SUBSEQUENT_2023_DRAFT_NOT_A_CALENDAR_DATE_ASSUMED_HERE',
    'foreign_contract_X5_X6_if_applicable':'SEPARATE_NAMED_CONDITION_NOT_AUTOMATIC_STASH',
    'future_year_rights_retained_automatically':False})
 return out
def assert_rights(rows,s):
 assert len(rows)==58 and len({r['player']for r in rows})==58
 for r,a in zip(rows,s['audit']['selected_NPC_2022_draft_rights']):
  assert all(r[k]==a[k]for k in a),'Selected draft identity/year/holder changed'
  assert r['candidate_owner']==a['conditional_final_rights_holder'] and r['candidate_owner']!='CHI'
  assert r['STD_added']==0 and r['TW_added']==0 and r['new_UPC_selected']is False,'Rights converted to registration'
  p=r['required_tender_candidate'];first=r['round']==1
  assert p['offer_date']==('2022-07-07'if first else '2022-08-25'),'Late or wrong-year tender'
  assert p['window_first']<=p['offer_date']<=p['window_last']
  assert p['window_last']==('2022-07-15'if first else '2022-09-05')
  assert p['minimum_acceptance_until']==('2022-10-18'if first else '2022-10-15')
  assert p['form']==('VIII1_RSC_FIRST2_PLUS2_OPTIONS'if first else 'ONE_SEASON_II6_ROOKIE_MINIMUM')
  assert r['normal_cap_hold_or_tender_cost']is None and r['apron_charge']is None
  assert r['future_year_rights_retained_automatically']is False
  assert r['rights_only_nonacceptance_is_conditional_sensitivity_not_collective_NBA_nonentry_selection']is True

def team_functions(s,contracts):
 result={};idx={r['player']:r for r in contracts}
 for team,old in sorted(s['global']['team_rosters'].items()):
  dates=[]
  for g in s['calendar']:
   if team in (g['home'],g['away']):dates.append({k:g[k]for k in ('calendar_key','published_date','home','away')})
  if team=='CHI':
   t=s['chi']['selected_role_template'];result[team]={'type':'EXISTING_SELECTED_CHI17_R1_AND_H22',
     'source':CHI+'#/selected_role_template','standard':t['registered_STANDARD'],'TW':t['registered_TWO_WAY'],
     'active':t['active_STANDARD'],'inactive':t['inactive_STANDARD'],'dates':dates,
     'clock_and_cost_recalculated_here':False,'new_N23':None,'new_A23':None};continue
  std=list(old['standard']);templates=[]
  for name,t in s['global']['shared_role_templates'].items():
   if t['team']!=team:continue
   active=list(t['positive_player_seconds'])
   active +=[n for n in std if n not in active][:12-len(active)]
   templates.append({'id':team+':'+t['state'],'source_clock_pointer':GLOBAL+'#/shared_role_templates/'+name,
     'source_state_name_not_new_health_adoption':t['state'],
     'blocks':copy.deepcopy(t['blocks']),'positive_player_seconds':copy.deepcopy(t['positive_player_seconds']),
     'active':active,'inactive':[n for n in std if n not in active],
     'all_positive_requires_available_current_UPC_input':True,
     'zero_reserve_medical_status':None,'actual_health_or_2022_minutes_certified':False,
     'FY22_health_state_or_results_selected':False})
  result[team]={'type':'FY22_SAME_OWNER_ROUTINE_CONTRACT_FUNCTION_WITH_UNSELECTED_CLOCK_STATE',
   'standard':std,'TW':[], 'expired_TW_no_new_UPC_ports':old['TW'],
   'dates':dates,'capacity_templates':templates,
   'contract_row_ids':[idx[n]['id']for n in std],
   'zero_minute_standard_reserves':[n for n in std if all(n not in t['positive_player_seconds']for t in templates)],
   'future_first_RSC_slot_join_completed':False,
   'admissibility_conditions':['The source-supported operative original status selects carry / timely original option / own-team consensual minimum renewal; every branch covers July7 through Apr9',
     'All original Gamma, cap holds, retained rights and dead liabilities remain in the corresponding cost function',
     'Each positive player is fictionally available; no old health state automatically adopted',
     'Same named owner retained; no actual2022 historical assignment imported',
     'Minimum renewal uses legal FY22 scale; same-team routine legal form selected, actual star willingness and market-price certification false',
     'Each original TW is expired or lawfully waived and cleared with protected Gamma/rights preserved, before no-new-UPC registration'],
   'important_candidates':[n for n in std if n in IMPORTANT],
   'named_core_market_price_family_pending':[n for n in std if n in IMPORTANT],
   'minimum_sensitivity_does_not_certify_core_market_agreement':True,
   'term_pending_players':[n for n in std if idx[n]['named_missing_input']is not None],
   'source_endpoint_fact_pending_is_not_private_receipt_execution_gate':True,
   'whole_cost_normal_upper':None,'whole_cost_apron_upper':None,'new_N23':None,'new_A23':None,
   'all_standard_current_contracts_certified':False,'operator_function_selected':True,
   'contract_execution_family_covers_FY22_window':True,
   'new_fictional_health_or_result_selection_in_this_packet':False}
 return result
def assert_teams(teams,s,contracts):
 assert set(teams)==set(s['global']['team_rosters']) and len(teams)==30
 catalog=[];idx={r['player']:r for r in contracts}
 for team,r in teams.items():
  assert 14<=len(r['standard'])<=15 and len(r['TW'])<=2
  assert len(r['standard'])==len(set(r['standard'])) and not(set(r['standard'])&set(r['TW']))
  assert len(r['dates'])==82 and len({x['calendar_key']for x in r['dates']})==82
  expected=[{k:g[k]for k in ('calendar_key','published_date','home','away')}for g in s['calendar']if team in (g['home'],g['away'])]
  assert r['dates']==expected
  assert r['new_N23']is None and r['new_A23']is None,'Future unknown cost zeroed'
  if team=='CHI':
   t=s['chi']['selected_role_template'];assert r['standard']==t['registered_STANDARD'] and r['TW']==t['registered_TWO_WAY']
   assert r['active']==t['active_STANDARD'] and r['inactive']==t['inactive_STANDARD']
  else:
   assert r['standard']==s['global']['team_rosters'][team]['standard'] and r['TW']==[],'Slot collision or unproved TW'
   assert r['zero_minute_standard_reserves']==[n for n in r['standard']if all(n not in t['positive_player_seconds']for t in r['capacity_templates'])]
   assert r['future_first_RSC_slot_join_completed']is False
   assert r['named_core_market_price_family_pending']==[n for n in r['standard']if n in IMPORTANT]
   assert r['minimum_sensitivity_does_not_certify_core_market_agreement']is True
   assert r['source_endpoint_fact_pending_is_not_private_receipt_execution_gate']is True
   assert r['all_standard_current_contracts_certified']is False and r['operator_function_selected']is True
   assert r['contract_execution_family_covers_FY22_window']is True and r['new_fictional_health_or_result_selection_in_this_packet']is False
   for t in r['capacity_templates']:
    original=s['global']['shared_role_templates'][t['source_clock_pointer'].split('/')[-1]]
    assert t['blocks']==original['blocks'] and t['positive_player_seconds']==original['positive_player_seconds'],'Source role clock changed'
    sums=Counter();pos=Counter();end=0
    for b in t['blocks']:
     assert b['start_second']==end and type(b['end_second'])is int and b['end_second']>end
     dt=b['end_second']-end;players=list(b['positions'].values())
     assert set(b['positions'])==set(POSITIONS) and len(set(players))==5 and set(players)<=set(t['active'])
     for p,n in b['positions'].items():sums[n]+=dt;pos[p]+=dt
     end=b['end_second']
    assert end==2880 and sum(sums.values())==14400 and dict(sums)==t['positive_player_seconds']
    assert set(pos.values())=={2880} and 12<=len(t['active'])<=15
    assert len(t['active'])==len(set(t['active'])) and len(t['inactive'])>=2
    assert set(t['active'])|set(t['inactive'])==set(r['standard']) and not set(t['active'])&set(t['inactive'])
    assert t['actual_health_or_2022_minutes_certified']is False and t['FY22_health_state_or_results_selected']is False
  catalog +=[(n,team,'STANDARD')for n in r['standard']]+[(n,team,'TW')for n in r['TW']]
 assert len({n for n,_,_ in catalog})==len(catalog),'Two current owners for one player'

def legal_evidence(s):
 a=s['audit'];law=copy.deepcopy(a['law']);p=Path(law['cache_path'])
 assert hashlib.sha256(p.read_bytes()).hexdigest()==law['raw_sha256'];d=fitz.open(p)
 pages=[30,54,55,71,74,75,232,233,292,294,295,303,309,310,317,318,319,334,335,336,412,413]
 law['direct_new_scope_pages']={str(n):hashlib.sha256(d[n-1].get_text().encode()).hexdigest()for n in pages}
 law['specific_read_scope']='II6 sign-year minimum; II11 TW eligibility/term; VII6i no-bonus min; VIII1 Year2/options; I1ddd/X4 RT dates; XI1c4 QO; XII original option; XXIX lists with season-specific active overlay'
 law['2017_45days_used_as_2022_50games']=False
 overlay=a['2022_23_active_rule_overlay'];gp=Path(overlay['cache_path']);raw=gp.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==overlay['raw_sha256']
 gd=fitz.open(gp);assert hashlib.sha256(gd[164].get_text().encode()).hexdigest()==overlay['page_text_sha256']
 return {'CBA':law,'active_overlay':overlay}
def build():
 s=inputs();assert_inputs(s);rows=contract_rows(s)
 for r in rows:r['public_2022_profile_classification']=profile_hits(r['player'],s)
 assert_contract_rows(rows,s);rights=rights_rows(s);assert_rights(rights,s)
 teams=team_functions(s,rows);assert_teams(teams,s,rows)
 resolutions=[]
 for r in rows:
  for status in r['execution_policy']['admitted_original_statuses']:
   z=resolve_contract(r,status);assert_resolution(z,r,status);resolutions.append(z)
 counts=Counter(r['term_status']for r in rows);missing=[{'player':r['player'],'team':r['candidate_owner'],'field':r['named_missing_input'],'source':r['original_source'],'locator':r['original_locator']}for r in rows if r['named_missing_input']]
 return {'id':'NBA_2022_23_NPC_CONTRACT_PORTFOLIO','baseline_main':BASELINE,
   'status':'REVIEW_PENDING_FINITE_30_TEAM_CONDITIONAL_CONTRACT_ROSTER_CLOCK_FUNCTIONS',
   'source_sha256':{AUDIT:AUDIT_SHA,**s['audit']['source_sha256'],SELF:sha(SELF)},
   'hash_convention':'SHA256_UTF8_BOM_STRIPPED_CRLF_CR_TO_LF; external bytes separately',
   'public_new_source_observations':{'cache_directory':str(TEMP),'observation_byte_pins':EXTERNAL_PINS,
     'provider_HTML_original_bodies_recovered':0,'direct_attempts':s['attempts'],
     'NBA_profile_web_body_observations':s['profiles'],'PHX_web_body_missing':True,
     'public_under_contract_is_not_same_UPC_or_new_owner_proof':True},
   'legal_evidence':legal_evidence(s),'NPC_contract_rows':rows,'NPC_2022_rights':rights,
   'constructive_status_resolution_check':{'cases':len(resolutions),'all_source_bound_caller_checks_passed':True,
     'status_counts':dict(Counter(z['original_status']for z in resolutions)),
     'resolutions_stored_as_callable_not_replicated_82_times':True},
   'team_functions':teams,'named_missing_term_inputs':missing,
  'whole_domain':'For every applicable source-supported original status/Gamma, same-owner q carries a live FY22 UPC, timely exercises its existing lawful option, or signs an own-team consensual one-season no-bonus minimum after expiry. Original TW is expired or lawfully waived/cleared with full Gamma/rights reserved. These are delegated fictional executions, not proof of private terms or actual market assent. Original endpoint facts stay typed unknown; no whole-cost/health/result selection follows.',
   'next_named_core_price_family':{'players':sorted(IMPORTANT),
     'required_scope':'Credible same-owner renewal range, positive Bird/EarlyBird/other mechanism and annual tax-cost mapping for applicable expiry cases',
     'legal_minimum_sensitivity_is_market_plausibility_PASS':False,
     'all_important_player_names_require_new_human_approval':False},
   'summary':{'teams':30,'NPC_input_rows':442,'NPC_prior_STD':430,'NPC_prior_TW_ports':12,
     'CHI_selected_STD':15,'CHI_selected_TW':2,'NPC_new_draft_rights':58,
     'NPC_explicit_one_season_minimum_routine_implementations':72,
     'NPC_original_status_dependent_retention_functions':284,
     'NPC_original_TW_expiry_or_waiver_no_new_UPC_functions':12,
     'NPC_new_draft_UPCs_selected':0,
     'first_RSC29_actual_implementation_slot_join_remaining':True,
     'guaranteed_or_explicit_2021_Year2_supported':counts['SUPPORTED_2021_YEAR2_COVERS_FY22'],
     'term_status_counts':dict(counts),'named_missing_term_inputs':len(missing),
     'candidate_NPC_live_STD':430,'candidate_NPC_live_TW':0,
     'all30_candidate_live_identities_including_CHI':447,
     'NPC_capacity_templates':sum(len(t.get('capacity_templates',[]))for t in teams.values()),
     'NPC_team_date_keys':2378,'all30_team_date_keys':2460,'unique_calendar_games':1230,
     'through_last_regular_date':'2023-04-09','result_or_OT_copied':False},
   'boundaries':{'independent_review_completed':False,'all_NPC_FY22_original_contract_term_facts_closed':False,
     'same_owner_routine_implementation_family_constructed':True,
     'all_NPC_UPCs_or_tenders_selected':False,'core_option_exact_price_or_franchise_move_selected':False,
     'FY22_health_or_result_adoption':False,'original_Gamma_deleted':False,
     'whole_normal_apron_cost_pass':False,'2023_N23_or_A23_selected':False,
     'actual_private_contracts_filings_medical_or_consents_certified':False,
     'whole_macro3_complete':False,'G13_G14_manuscript_gate_open':False},
   'progress':copy.deepcopy(s['audit']['progress']),'unfinished_macro_groups':5,
   'unfinished_through_6':4,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0,'manuscript_allowed':False}
def validate(v):
 try:
  expected=build();assert v==expected,'Stored artifact differs from source-bound construction';return []
 except (AssertionError,KeyError,TypeError,ValueError)as e:return [str(e)]
def render(v):
 q=v['summary'];lines=['# 2022–23 NPC 계약 포트폴리오','',
  '검문대기. Chicago의 선택17/R1/H22를 고정하고 NPC442 원행·58 지명권을 당해 실행 가족에 연결했다. **같은 팀 잔류의 루틴 구현 함수를 선택했으며, 실제 계약·시장 수락·정확 원기간·가용·승패 인증은 아니다.**','',
  '## 실제 연결 범위','',
  f"- 명시적2021 다년/RSC Year2 {q['guaranteed_or_explicit_2021_Year2_supported']}명은 당해 기간 근거가 있다.",
  '- 일년55명과 2021 마지막 옵션17명은 만료 후 같은 팀의 합의된 일년 최소연봉/no-bonus 형식을 구성한다. RFA도 원팀과 직접 합의할 수 있다(XI1a). 실제 핵심선수의 시장 수락이나 기존 가격을 최소액으로 보도했다는 뜻은 아니다.',
  '- 나머지284명은 원 UPC가 FY22에 살아 있으면 그대로 이월, 원 옵션이 있으면 원기한 내 유효 행사, 이미 만료했으면 같은 팀의 일년 최소 합의라는 명명 함수다. 원기간의 사실 미회수와 적법한 가상 구현 가능성을 분리한다. 유효 원계약을 임의 중도만료·삭감하지 않는다.',
  '- TW12명은 원기간이 살아 있으면 합법 방출·waiver clearance 후 기존 보장Γ/권리/hold 전액을 남기고 새UPC를 체결하지 않는다. 만료했으면 새UPC 없이 같은 경제·권리를 보존한다. 새TW3/4YOS·4번째동일팀capyear를 만들지 않는다.',
  f"- 사실상 말단/옵션/TW 민감도 {q['named_missing_term_inputs']}개는 선수·원source·locator로 반환한다. 이는 실행불가 판정이나 사적 전체UPC 수집이라는 새 gate가 아니다.",
  f"- 29팀 조건부 STD430/TW0, CHI15+2 고정, {q['NPC_capacity_templates']}개 NPC 시계 함수. 각 함수는 고유5인·2880초·5포지션14400초와 active12/inactive2이상을 직접 검문한다.",
  '- 원FY21 시계는 당해 후보의 수학적 위치 배정 원형이다. 옛 부상/가용/결과가 FY22로 자동 이월되지 않는다. 양수마다 당해 유효UPC와 가상가용 입력을 요구한다.',
  '- NPC58명 RT는 적시 공급·미수락을 조건으로 한 rights-only 민감도다. 첫RSC29명 전원 NBA 미입단을 선택하지 않았다. 다음 별도 실행은 July11 이후 120% RSC·기존 빈 슬롯 또는 양수 없는 reserve의 합법방출/전액Γ 보존을 연결해야 한다. 이 신규 slot join은 본체에 완료로 계수하지 않는다. 2R29명 미수락도 실제 player agency가 아닌 조건부 가족이며, 1R hold/채무는 null로 남긴다.',
  '- 1230 공식키=30×82, NPC2378키. 2023 신인지명 후 N23/A23 및 이후기간은 별도 null이며 Apr9 이전 결과를 막는 입력으로 쓰지 않는다.','',
  '## 새 원자료의 한계','',
  'NBA2022 profile28팀의 본문 분류를 관측했다. direct29는403이며 응답bytes만 보존하고 원본문으로 채택하지 않는다. PHX web본문은 미회수다. UnderContract는 다음 시즌 긍정분류로만 사용하며, 원UPC와 동일한 계약·새연장·다른구단 양도를 자동 인증하지 않는다. 각 실명 hit에 URL/본문line/동일UPC 미인증을 남겼다. 특히 원Harden/Gobert/Mitchell 거래를 가져오지 않는다.','',
  '## 법적 가족과 남은 실행','',
  '원Γ는 정확금액 미선택으로 모두 보존한다. 최소예외는2022 서명연도 최소표·YOS 함수, 한시즌/bonus0이며 지급액0이 아니다. 원 옵션은 적법한 당사자의 원기한 내 유효행사만 받으며 실제 통지는 인증하지 않는다. 어느 상태에서나 양수 등록선수의 FY22 UPC를 구성하는 함수와 당시 적법가용을 요구한다. 전체 TeamSalary/apron 상단은 null이며, 원bonus/legacy/FA hold를 없애지 않는다. 최소예외 자체는 새 NTMLE/BAE/S&T hardcap을 발생시키지 않지만 다른 기존 비용과 당해 제약은 별도 보존한다.','',
  f"실행함수의 원상태 분기 {v['constructive_status_resolution_check']['cases']}개를 호출하고 반환을 별도로 검문했다. 사실 unknown을 0으로 바꾸지 않는다. 다음 경계는 첫RSC29명 슬롯·서명 join 및 새로운 가상 FY22 건강/역할 선택 소비자이며, 원계약 사적 영수증이나 29개 개별PR은 필요조건이 아니다.",'',
  '## 진행표','', '| 번호 | 상태 |','|---|---|']
 for r in v['progress']:lines.append(f"| {r['group']} | {r['status']} |")
 lines+=['','미완료 큰 묶음5개·6번까지4개. v0.30 PARTIAL·CLOSED·Pack0·원고0.']
 return '\n'.join(lines)+'\n'
def self_test():
 s=inputs();assert_inputs(s);base=build();controls=[]
 def rejected(name,fun):
  try:fun()
  except (AssertionError,KeyError,ValueError):controls.append(name);return
  raise AssertionError('Negative false pass: '+name)
 def mutate_contract(field,value):
  r=contract_rows(s);r[0][field]=value
  with patch(__name__+'.contract_rows',return_value=r):build()
 rejected('original_Gamma_deleted',lambda:mutate_contract('original_all_Gamma_reserved',False))
 rejected('wrong_player_year',lambda:mutate_contract('player','Walker Kessler'))
 def slots():
  t=team_functions(s,base['NPC_contract_rows']);t['ATL']['standard'].append('Walker Kessler')
  with patch(__name__+'.team_functions',return_value=t):build()
 rejected('sixteenth_standard_and_global_owner_collision',slots)
 def late():
  r=rights_rows(s);r[0]['required_tender_candidate']['offer_date']='2022-09-06'
  with patch(__name__+'.rights_rows',return_value=r):build()
 rejected('late_required_tender',late)
 def zero():
  t=team_functions(s,base['NPC_contract_rows']);t['ATL']['new_N23']=0
  with patch(__name__+'.team_functions',return_value=t):build()
 rejected('future_N23_null_to_zero',zero)
 def generic():
  r=contract_rows(s);i=next(i for i,x in enumerate(r)if x['named_missing_input']);r[i]['FY22_all_dates_covered_without_additional_term_input']=True
  with patch(__name__+'.contract_rows',return_value=r):build()
 rejected('FY21_currentvalid_promoted_to_FY22',generic)
 def clock():
  t=team_functions(s,base['NPC_contract_rows']);b=t['ATL']['capacity_templates'][0]['blocks'][0]['positions'];b['PG'],b['SG']=b['SG'],b['PG']
  with patch(__name__+'.team_functions',return_value=t):build()
 rejected('same_total_position_swap_source_mismatch',clock)
 def tw():
  r=contract_rows(s);i=next(i for i,x in enumerate(r)if x['TW_port']);r[i]['TW_port']['new_TW_selected']=True
  with patch(__name__+'.contract_rows',return_value=r):build()
 rejected('unverified_TW_conversion',tw)
 def resolution_bad(field,value):
  original=resolve_contract
  def bad(row,status):
   z=original(row,status)
   if status=='EXPIRED_BEFORE_FY22':z[field]=value
   return z
  with patch(__name__+'.resolve_contract',side_effect=bad):build()
 rejected('returned_minimum_bonus_added',lambda:resolution_bad('new_bonuses',100000))
 rejected('returned_original_Gamma_erased',lambda:resolution_bad('full_original_Gamma_preserved',False))
 return controls
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(dump(v),encoding='utf-8');(ROOT/MD).write_text(render(v),encoding='utf-8')
 result={'summary':v['summary']}
 if a.check:
  errors=validate(json.loads(text(OUT)));assert not errors,errors;assert text(MD)==render(v),'MD stale';result['current']=True
 if a.self_test:result['negative_controls']=self_test()
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
