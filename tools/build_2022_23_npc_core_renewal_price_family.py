"""Constrain eleven same-owner FY22 core price functions; no actual market certificate."""
from __future__ import annotations
import argparse, copy, hashlib, json
from fractions import Fraction as F
from pathlib import Path
from unittest.mock import patch
import fitz
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_23_npc_core_renewal_price_family.py'
OUT='research/NBA_2022_23_NPC_CORE_RENEWAL_PRICE_FAMILY.json'
MD=OUT.replace('.json','.md')
PORT='simulation/NBA_2022_23_NPC_CONTRACT_PORTFOLIO.json'
TEMP=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-npc-core22-20261008')
CBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
OBS_SHA='e4a2e6e29cb0f1d548860a3084d8bcf978560d4028585a29d331e12f9fc48c82'
PINS={'research/LAVINE_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07.json': '2c7cf936b8387521e46f67cd245358bbd5c8191c99c466da9ae8b4b7c7d635d0', 'research/NBA_2022_23_ROLLOVER_FINITE_INPUT_AUDIT_2026_10_08.json': '39f26fc6404b1df2b7a53b56d9da4cd49530d4ba8c0c3207533d0146a641c785'}
PAGE_PINS={'26': 'ff6b36ecd67bcbc1491e464ebce0d85a5d4d07db36c82da1d0cc4ec32d32044a', '29': 'a7376434286a88c8b534c773c4dbf184c21df8a8a52c22718221ce39e9a08e75', '30': '9cf0f5b23523777c69220fc109f59a6b42dc1550c90082e39b48748f53a03338', '54': 'b002f3d4c97245ae75d89d3e8d390574ee71de51c38cf25de405c67f622da9a1', '55': 'ca2c17388d44346413fe2b288d5da395a02849cda5600738373b321cc1be80da', '57': 'a7aad971c53c9aeba55c6a8d5957bae0c64010395a433063c3cf44a303bc133b', '58': '6bfe75ec156ef879964d4f79660a3f4041a3a8f81a22ef2297c0590a6e4a3ba7', '59': '59aaa9a501bca93905cc6b6cd63d4aea141413c89baebc32797ebf8bbeb476e6', '206': 'e5c736cb6aae51bff5515753ed23070ec8e3079f47d7f966e3a3e5b40b54fb62', '207': 'd12be4b76bccaf8c4fe8885928e866f81e677074d930fcb1c96713ebd91ae0a0', '208': '6233d594134459740d61511b7f3ee62f00a60ae2388c387957bf26736af406c3', '209': '3a47b881e3d34ff50f7ad32a38792702ac43e77a9aa9383b5433ceba6bc84859', '210': '6f155805eebeb105501cc90b1f27ff41e222d3413033bd952f010e9b4daa3c3a', '218': 'f79ff7838664c65a9a960fc9a05537aca47b7acb38e92c969f31e766f55af50a', '223': '1036fb9ce58b602830b3dbd04ef902a09de8922f94671a2ba98a01e451919f3b', '224': '88bfd31d8dd7393b272a8bdfdc55da36a34f60aa87ae297f4435be53549bbe1c', '232': '38b400763b01a29678eaecbb413e01a318ca8460bf29ce7d884e6f0f140239b0', '233': '236194df68b0f343933e4b25e48bef4c80d2bbfba11006a87e9585687aae7ba3', '240': '894e9af9d73b50ed7208a6188c8fa7990be625dfe863b85945ff20c57ae85a65', '241': '43236045b17a96dc3b0a2fc34452c83b383a4b6aacc623d961ec8cdb7ebb6f60', '252': 'b086e518697b5b94795c341b154279e6734b22f61c6157d51ab05a4f668aaab0', '253': 'f35be5e4b1e7af94779ab9e72256c06ea86c5cfb17f0076aa159ada72badff9a', '284': 'fe3aa0a9f16d9e3325d0d2765be653fe815fb8a0485573aed48e26c2c1827ccb', '285': 'e583cbd5dd5f4401ffb11a9d5fe077205cc99ced9f939702f93d184bbf0b5150', '299': '1c24a5478462697177a9daca0be1935caa3f5207256b5b487f234dea4357748e', '334': 'ba8a1c35001f959a29bb419bfa0b6b00aabbe6890122a906f190b359e8dc9a39', '335': '8b894197d51fdd6f46bb6c9fa2fb7dfffb8db34a2f7be1180c29c65abac83420', '336': '4cfeb29b32641cde36e895b261686379093eb431f79223d7ceed6120a31a062f', '561': '7f13ec34eb63aa8d3ff7a74ed4ed1e9dba6ce50d7ad3b1f49edd8b09cd05f18e'}
CORE_DIGEST='8d0760d2a4704f27574b0c3ca8016c5802b2d95250a49474d838dfdf81991ff8'
CAP=123655000; TAX=150267000
FIELDS=('player','candidate_owner','original_group','original_source','original_locator','original_contract_fields','original_term_fields')
# Monetary endpoints are declared proposals, anchored to reported comparisons, not market facts.
# name: owner, completed YOS, first-year low/high, seasons, context source IDs, FA type.
SPECS={
 'James Harden':('BKN',13,33000000,43279250,2,['HARDEN','OPTIONS'],'UFA_OR_PO'),
 'Kyrie Irving':('BKN',11,36000000,43279250,3,['IRVING','OPTIONS'],'UFA_OR_PO'),
 'Miles Bridges':('CHA',4,25000000,30913750,4,['BRIDGES_QO','BRIDGES_CONTEXT','OPTIONS'],'RFA'),
 'Collin Sexton':('CLE',4,16000000,20000000,4,['SEXTON','OPTIONS'],'RFA'),
 'Jalen Brunson':('DAL',4,25000000,30913750,4,['BRUNSON'],'UFA'),
 'Kawhi Leonard':('LAC',11,40000000,43279250,4,['KAWHI'],'UFA_AFTER_SELECTED_LAST_PO'),
 'Josh Hart':('NOP',5,12000000,16000000,3,['HART'],'UFA_AFTER_SELECTED_ONE_YEAR_QO'),
 'Lonzo Ball':('NOP',5,20000000,25000000,4,['LONZO','REVIEW2021'],'UFA_AFTER_SELECTED_ONE_YEAR_QO'),
 'Deandre Ayton':('PHX',4,28000000,30913750,4,['AYTON','OPTIONS'],'RFA'),
 'Norman Powell':('TOR',7,18000000,22000000,4,['REVIEW2021'],'UFA_AFTER_SELECTED_LAST_PO'),
 'Bradley Beal':('WAS',10,40000000,43279250,5,['BEAL','OPTIONS'],'UFA_OR_PO')}

def norm(s):return s.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
def read(p):return norm((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(read(p).encode()).hexdigest()
def rawsha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def frac(x):return str(F(x))
def inputs():
 for p,h in PINS.items():assert sha(p)==h,'Pinned source changed: '+p
 obsraw=(TEMP/'observations.json').read_bytes();assert hashlib.sha256(obsraw).hexdigest()==OBS_SHA
 obs=json.loads(obsraw)
 for r in obs:
  assert rawsha(r['cache_path'])==r['raw_sha256']
  assert hashlib.sha256(norm(Path(r['body_cache_path']).read_text(encoding='utf-8')).encode()).hexdigest()==r['body_sha256']
  raw=Path(r['cache_path']).read_bytes();soup=BeautifulSoup(raw,'html.parser')
  if r['id']=='BRIDGES_QO':
   nd=json.loads(soup.find('script',id='__NEXT_DATA__').string)
   pieces=nd['props']['pageProps']['pageObject']['contentStructured']
   body='\n'.join([nd['props']['pageProps']['pageObject']['title']]+[BeautifulSoup(z['html'],'html.parser').get_text(' ',strip=True) for z in pieces if z.get('html')])+'\n'
   # Structured source is also pinned; article body cache was collected with that source.
   assert 'qualifying' in json.dumps(pieces).lower()
   assert hashlib.sha256(body.encode()).hexdigest()==r['body_sha256']
  else:
   a=soup.find('article') or soup.find('main');assert a is not None
   body='\n'.join(z.strip() for z in a.get_text('\n',strip=True).splitlines() if z.strip())+'\n'
   assert hashlib.sha256(body.encode()).hexdigest()==r['body_sha256']
  observed=Path(r['body_cache_path']).read_text(encoding='utf-8')
  for token in r['required_observation_tokens']:assert token in observed, 'Positive body observation changed'
 assert len(obs)==13 and rawsha(CBA)==CBA_SHA
 doc=fitz.open(CBA)
 for page,h in PAGE_PINS.items():assert hashlib.sha256(doc[int(page)-1].get_text().encode()).hexdigest()==h
 port=json.loads(read(PORT));rows=[{k:r[k] for k in FIELDS} for r in port['NPC_contract_rows'] if r['player'] in SPECS]
 assert len(rows)==11 and digest(rows)==CORE_DIGEST,'Core original contract/source meaning changed'
 for r in rows:
  assert sha(r['original_source'])==port['source_sha256'][r['original_source']]
 cap=json.loads(read('research/LAVINE_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07.json'))
 c=next(r for r in cap['raw_body_observations'] if r['id']=='NBA_CAP2022_REUSED')
 assert rawsha(c['cache_path'])==c['raw_sha256']
 body=BeautifulSoup(Path(c['cache_path']).read_bytes(),'html.parser').get_text(' ',strip=True)
 assert '123.655' in body and '150.267' in body
 return {'core':rows,'observations':obs,'cap':c,'portfolio_sha':sha(PORT)}

def qualification(name):
 t=SPECS[name][0]
 windows=[{'season':'2019-20','owner':t},{'season':'2020-21','owner':t},{'season':'2021-22','owner':t}]
 if name=='James Harden':windows[0]['owner']='HOU';windows[1]['owner']='HOU_THEN_BKN_BY_TRADE'
 return {'preceding_standard_contract_seasons':windows,'qualifying_seasons':3,
  'mechanism':'I1(yy), VII6(b)(1)',
  'preserved_service_history_is_family_input':True,'disqualifying_renunciation_or_intervening_FA_move':False,
  'actual_original_private_service_certificate':False,
  'legal_condition':'Contracts cover some/all of each preceding season; any team change satisfies I1(yy). No waived Bird rights.',
  'historical_current_profile_does_not_prove_original_UPC':True}

def allowed_statuses(name):
 return ['VALID_ORIGINAL_FY22_OPTION','VALID_EXPIRY_OR_DECLINE'] if SPECS[name][-1]=='UFA_OR_PO' else ['VALID_EXPIRY_OR_DECLINE']

def forms():
 rows=[]
 for name,(team,yos,lo,hi,years,ids,kind) in SPECS.items():
  pct=F(1,4) if yos<7 else F(3,10) if yos<10 else F(7,20)
  rows.append({'player':name,'team':team,'completed_YOS':yos,'FA_class_when_expired':kind,
   'source_comparator_ids':ids,'source_original_context_is_not_alternate_agreement':True,
   'source_supported_statuses':allowed_statuses(name),
   'price_interval_first_season':[lo,hi],'recommended_consensual_first_salary':hi,
   'price_lower_is_model_recommendation_not_statutory_floor':True,
   'legal_standard_percent':frac(pct),'cap_percent_sufficient_ceiling':int(CAP*pct),
   'full_II7_ceiling':'max(cap_percent*123655000,105%*actual_final_prior_contract_Salary)',
   'actual_prior_final_Salary':None,'award_designated_higher_max_not_assumed':True,
   'qualifying_service':qualification(name),'term_seasons':years,'raises_range':[0,'2/25'],
   'fully_protected':True,'new_likely_bonus':0,'new_unlikely_bonus':0,'new_signing_bonus':0,
   'new_assignment_bonus':0,'new_other_compensation_additions':0,
   'option_forms':['NO_OPTION','LAST_YEAR_PLAYER_OPTION_EX2A'],
   'candidate_signing_ET':'2022-07-07T12:00:00-04:00','accepted_offer_sheet':False,
   'existing_live_UPC_action':'PRESERVE_WITHOUT_NEW_RENEWAL',
   'existing_FY22_PO_action':'EXERCISE_OR_VALIDLY_DECLINE_AT_ORIGINAL_DEADLINE_BEFORE_RENEWAL',
   'original_deadline_exact':None,'actual_option_notice_or_consent':None,
   'all_original_Gamma_preserved':True,'new_franchise_move':False,
   'renewal_form_selected_for_execution':False,'actual_market_acceptance':False,
   'economic_comparator_support':'REPORTED_CONTEXT_WITH_DIFFERENT_TEAM_OR_CONTRACT_WHERE_NOTED',
   'model_interval_economically_recommended_not_market_CERT':True,
   'Miles_no_UPC_recommendation':name=='Miles Bridges',
   'team_other_normal_apron_and_tax_cost':None,'N23':None,'A23':None})
 return rows

def assert_forms(rows,s):
 assert len(rows)==11 and [r['player'] for r in rows]==list(SPECS)
 physical={r['player']:r for r in s['core']}
 for r in rows:
  name=r['player'];team,yos,lo,hi,years,ids,kind=SPECS[name]
  assert r['team']==team==physical[name]['candidate_owner']
  assert r['completed_YOS']==yos and r['FA_class_when_expired']==kind
  assert r['source_supported_statuses']==allowed_statuses(name),'Source expiry/option status family changed'
  assert r['price_interval_first_season']==[lo,hi] and r['recommended_consensual_first_salary']==hi
  assert r['source_comparator_ids']==ids and r['qualifying_service']==qualification(name),'Bird service input changed'
  q=r['qualifying_service'];assert q['qualifying_seasons']==3 and q['disqualifying_renunciation_or_intervening_FA_move'] is False
  expected_owners=['HOU','HOU_THEN_BKN_BY_TRADE','BKN'] if name=='James Harden' else [team]*3
  assert q['preceding_standard_contract_seasons']==[{'season':season,'owner':owner} for season,owner in zip(['2019-20','2020-21','2021-22'],expected_owners)]
  assert q['preserved_service_history_is_family_input'] is True and q['actual_original_private_service_certificate'] is False
  pct=F(1,4) if yos<7 else F(3,10) if yos<10 else F(7,20)
  assert r['full_II7_ceiling']=='max(cap_percent*123655000,105%*actual_final_prior_contract_Salary)'
  assert r['award_designated_higher_max_not_assumed'] is True and r['price_lower_is_model_recommendation_not_statutory_floor'] is True
  assert r['source_original_context_is_not_alternate_agreement'] is True and r['model_interval_economically_recommended_not_market_CERT'] is True
  assert r['legal_standard_percent']==str(pct) and r['cap_percent_sufficient_ceiling']==CAP*pct
  assert 4000000<lo<=hi<=CAP*pct and 1<=years<=5 and r['term_seasons']==years
  assert r['raises_range']==[0,'2/25'] and r['fully_protected'] is True
  for k in ('new_likely_bonus','new_unlikely_bonus','new_signing_bonus','new_assignment_bonus','new_other_compensation_additions'):assert r[k]==0,'New bonus changes source-supported price function'
  assert r['option_forms']==['NO_OPTION','LAST_YEAR_PLAYER_OPTION_EX2A']
  assert r['candidate_signing_ET']=='2022-07-07T12:00:00-04:00'
  assert r['all_original_Gamma_preserved'] and not r['new_franchise_move']
  assert r['existing_live_UPC_action']=='PRESERVE_WITHOUT_NEW_RENEWAL'
  assert r['existing_FY22_PO_action']=='EXERCISE_OR_VALIDLY_DECLINE_AT_ORIGINAL_DEADLINE_BEFORE_RENEWAL'
  for k in ('actual_prior_final_Salary','original_deadline_exact','actual_option_notice_or_consent','team_other_normal_apron_and_tax_cost','N23','A23'):assert r[k] is None
  for k in ('renewal_form_selected_for_execution','actual_market_acceptance','accepted_offer_sheet'):assert r[k] is False
  assert r['Miles_no_UPC_recommendation']==(name=='Miles Bridges')

def resolve(r,status,first=None,raise_rate=F(2,25),option='NO_OPTION'):
 assert status in r['source_supported_statuses'],'Contract status not supported by named expiry/option source'
 if status!='VALID_EXPIRY_OR_DECLINE':
  return {'player':r['player'],'action':'CARRY_ORIGINAL_FULL_UPC','new_UPC':False,
   'first_salary':None,'normal_apron':'Original full CurrentSalary/all Gamma, not the renewal recommendation',
   'all_original_Gamma_preserved':True,'actual_receipt':False,'N23':None}
 a=F(first if first is not None else r['recommended_consensual_first_salary']);rr=F(raise_rate)
 assert F(r['price_interval_first_season'][0])<=a<=r['price_interval_first_season'][1]
 assert 0<=rr<=F(2,25) and option in r['option_forms']
 schedule=[a*(1+rr*i) for i in range(r['term_seasons'])]
 return {'player':r['player'],'action':'OWN_BIRD_CONSENSUAL_PROPOSAL','new_UPC':True,
  'first_salary':frac(a),'schedule_exact_dollar_fractions':[frac(x) for x in schedule],
  'new_full_regular_protection':True,'new_bonus':0,'option':option,
  'option_year_only_last_and_same_protection':True,'option_Ex2A_if_any':option!='NO_OPTION',
  'future_option_exercise':None,'normal_current_new_charge':frac(a),'apron_current_new_charge':frac(a),
  'all_original_Gamma_preserved':True,'old_expired_live_salary_double_counted':False,
  'pre_signing_FA_QO_hold_replaced_not_added':True,'actual_receipt':False,'N23':None,
  'execution_admitted':False,'replaces_same_claim_portfolio_expiry_minimum_function':True,
  'extra_minimum_UPC_added':False,'Miles_price_sensitivity_only':r['player']=='Miles Bridges'}

def assert_resolution(v,r,status,first,rr,option):
 assert v['player']==r['player'] and v['all_original_Gamma_preserved'] is True
 assert v['actual_receipt'] is False and v['N23'] is None
 if status!='VALID_EXPIRY_OR_DECLINE':
  assert v['action']=='CARRY_ORIGINAL_FULL_UPC' and v['new_UPC'] is False and v['first_salary'] is None
  return
 assert v['action']=='OWN_BIRD_CONSENSUAL_PROPOSAL' and v['execution_admitted'] is False
 assert v['replaces_same_claim_portfolio_expiry_minimum_function'] is True and v['extra_minimum_UPC_added'] is False
 assert v['new_bonus']==0 and v['new_full_regular_protection'] is True
 assert v['schedule_exact_dollar_fractions']==[frac(F(first)*(1+F(rr)*i)) for i in range(r['term_seasons'])]
 assert v['normal_current_new_charge']==v['apron_current_new_charge']==frac(first)
 assert v['option']==option and v['option_year_only_last_and_same_protection'] is True
 assert v['option_Ex2A_if_any']==(option!='NO_OPTION') and v['future_option_exercise'] is None
 assert v['pre_signing_FA_QO_hold_replaced_not_added'] and not v['old_expired_live_salary_double_counted']
 assert v['Miles_price_sensitivity_only']==(r['player']=='Miles Bridges')

def tax(total,repeater=False):
 excess=max(F(0),F(total)-TAX);out=F(0);i=0
 while excess:
  part=min(excess,5000000);rate=[F(3,2),F(7,4),F(5,2),F(13,4)][i] if i<4 else F(15,4)+F(i-4,2)
  out+=part*(rate+int(repeater));excess-=part;i+=1
 return out

def hold(prior,above_average,rookie_second_option,max_salary,min_unreimbursed,qo=0,frn=0,restricted=False,maximum_qo=0):
 coeff=(F(5,2) if above_average else F(3)) if rookie_second_option else (F(3,2) if above_average else F(19,10))
 fa=max(F(min_unreimbursed),min(F(max_salary),coeff*F(prior)))
 return {'normal':max(fa,F(qo),F(maximum_qo),F(frn)) if restricted else fa,'apron':max(F(qo),F(frn)) if restricted else F(0)}

def build():
 s=inputs();assert digest(s['core'])==CORE_DIGEST,'Returned core source meaning changed'
 rows=forms();assert_forms(rows,s);cases=[]
 for r in rows:
  for status in r['source_supported_statuses']:
   if status=='VALID_EXPIRY_OR_DECLINE':continue
   # A status is operative only when the source contract permits it; not a claim that each source has every option.
   v=resolve(r,status);assert_resolution(v,r,status,None,F(0),'NO_OPTION');cases.append(v)
  for a in r['price_interval_first_season']:
   for rr in (F(0),F(2,25)):
    for option in r['option_forms']:
     v=resolve(r,'VALID_EXPIRY_OR_DECLINE',a,rr,option)
     assert_resolution(v,r,'VALID_EXPIRY_OR_DECLINE',a,rr,option);cases.append(v)
 sources={PORT:s['portfolio_sha'],**PINS,SELF:sha(SELF)}
 for r in s['core']:sources[r['original_source']]=sha(r['original_source'])
 return {'status':'REVIEW_PENDING_CONSTRAINED_CORE_PRICE_FUNCTIONS_NOT_SELECTED',
  'baseline_main':'d6bd960568fce5687bd2843da6f51d0fe9c18d3c','source_sha256':sources,
  'source_hash_convention':'UTF8_BOM_STRIPPED_LF_REPOSITORY; RAW_EXTERNAL_BYTES',
  'core_original_projection_semantic_sha256':CORE_DIGEST,'original_core_source_rows':s['core'],
  'contract_price_functions':rows,'endpoint_function_checks':cases,
  'summary':{'named_core':11,'price_function_endpoint_checks':len(cases),'new_price_agreements_selected':0,
   'Miles_UPC_recommended':False,'whole_market_acceptance_certified':False,'whole_team_cost_PASS':False,
   'actual_private_terms_or_receipts_certified':False,'independent_review_completed':False,
   'whole_macro3_complete':False,'season_complete':False,'N23':None,'A23':None,'manuscript':False},
  'scope':{'original_live_and_valid_option_carry_unchanged':True,
   'renewal_requires_valid_expiry_or_decline_full_Bird_and_consent':True,
   'Bird_qualifying_service_is_named_preserved_family_input_not_profile_proof':True,
   'prior_service_failure':'Use lawful limited EarlyBird/NonBird/minimum form only within its own ceiling; proposed high interval is not admitted without Bird.',
   'entire_II7_domain':'Retain max(percentCap,105%priorSalary); sufficient interval below percentCap does not select or erase the larger priorSalary branch.',
   'price_interval_not_all_lawful_prices_or_actual_market_bound':True,
   'Miles':'No new UPC recommended; preserve CHA FA/QO rights/holds. Price form sensitivity only; April2023 suspension not retroactive Oct2022 prohibition.',
   'minimum_salary':'II6/ExC signing-year table: all proposed salaries exceed4m. Even max2017 five-year table cell2794384×123655000/99093000 is below3.5m; no exact statutory rounding asserted.',
   'calendar':'July7 proposal follows reviewed July6 12:01ET Bird opening; original option deadlines/valid notices remain external named inputs.',
   'new_standard_slots':'Same player replaces own expired standard UPC: deltaSTD0, no new TW, no 16th player generated.',
   'portfolio_minimum_substitution':'Expired core minimum function is replaced by this same player own Bird price, not added as a second UPC. Live UPC/option branch stays original; B excludes that same player price but retains applicable originalGamma.',
   'remaining_named_qualification_conditions':[{'player':r['player'],'condition':'Preserved named preceding3 standard seasons/I1yy permitted trade bridge; no operative Bird renunciation; valid expiry/decline and consensual same-owner newUPC. No private-receipt certificate required.'} for r in rows],
   'hardcap':'Own Bird renewal creates no S&T/NTMLE/BAE trigger. Existing FY22 trigger and other whole team costs remain separate.',
   'future_assignment':'Exact date null; VII8(d)(ii)/(iii) apply separately, including possible Jan15 for qualifying prior-team raises.'},
  'unsigned_and_FA_cost_functions':{'priorSalary_definition':'VII4(d)(8): RegularSalary+allocated signing bonus+Incentive actually earned under final contract',
   'normal_Bird_hold_coefficients':{'ordinary_above_average':'3/2','ordinary_below_average':'19/10','after_second_RSC_option_above':'5/2','after_second_RSC_option_below':'3'},
   'clamps':'Minimum unreimbursed floor and applicable maximum ceiling; RFA normal=max(FAhold,QO,MaximumQO,FRN).',
   'apron':'UFAhold excluded; RFA max(QO Salary+Unlikely,FRN Salary+Unlikely), VII6m3C. MaximumQO not silently treated as ordinaryQO.',
   'new_signed_charge':'A+new bonuses0; replace applicable FAhold. Preserve all applicable originalGamma/dead/unpaid obligations and other team categories, not an arbitrary future settlement.',
   'missing_whole_team_cost_input':'B_normal/B_apron/B_tax by team and operative date; no zero substitution.'},
  'annual_tax_function':{'tax_level':TAX,'nonrepeater_rates':['3/2','7/4','5/2','13/4'],'additional_5m_after20m':'15/4 then +1/2 per additional band',
   'repeater_increment':1,'repeater_status_actual':None,
   'function':'tax(B_tax+A,repeater)-tax(B_tax,repeater); B_tax is same other lawful TaxTeamSalary, no FAhold substituted as tax.',
   'function_examples_not_actual_team_cost':[{'B_tax':b,'newSalary':a,'repeater':rep,'increment_exact':frac(tax(b+a,rep)-tax(b,rep))} for b in (TAX-20000000,TAX,TAX+10000000) for a in (12000000,43279250) for rep in (False,True)]},
  'fallback_exception_boundaries':{'full_Bird':'VII6b1 maxII7; IX1 up to5; VII5c2 up to8%first',
   'EarlyBird':'I1u two seasons; VII6b3 max(175%Regular+175%bonus components,105%average) cappedII7; at least2nonoption seasons.',
   'NonBird':'VII6b2 max(120%Regular+120%bonus components,120%minimum,RFAQO) cappedII7;5%raises;max4.',
   'minimum':'VII6i up to2years at II6 minimum and no bonuses; not economic certificate for a star.'},
  'raw_body_observations':s['observations']+[s['cap']],
  'Miles_official_followup':{'url':'https://www.nba.com/news/nba-suspends-miles-bridges-for-30-games-without-pay','published':'2023-04-14',
   'web_body_locator':'179','observed_fact':'No2022–23 UPC;82missed.',
   'web_original_body_read':True,'direct_HTTP_single_attempt':403,'raw_original_body_adopted':False,'retroactive_October_ban_adopted':False},
  'cba_primary':{'cache_path':str(CBA),'raw_sha256':CBA_SHA,'text_page_sha256':PAGE_PINS,
   'locators':{'Bird':'PDF29–30 I1yy; PDF223 VII6b1','max':'PDF57–59 II7','minimum':'PDF54–55 II6/561ExC','raises':'PDF218 VII5c2',
    'term':'PDF299 IX1','normal_holds':'PDF206–210 VII4c/d','apron':'PDF240–241 VII6m3','tax':'PDF284–285 VII12f','options':'PDF334–336 XII','later_trade':'PDF252–253 VII8d'}},
  'next_finite_execution':'Root chooses realistic same-owner renewal/option terms for each valid expiry/decline branch and joins symbolic B_tax/B_normal/B_apron. Miles noUPC/rights/hold overlay separately. Original live UPC is carried; price proposal is not a rewrite.'}

def render(x):
 lines=['# NBA 2022–23 핵심 잔류 가격 가족','',x['status'],'',
  '동결 NPC 포트폴리오의 명명된 11명에 가격 함수와 원 계약 분기를 연결했다. 새 합의·시장수락·팀 전체비용은 확정하지 않는다. 살아 있는 원 UPC/유효 옵션은 그대로 보존한다.','',
  '| 선수/팀 | 첫해 제안 구간 | 기간 | 원 만료/옵션 경계 |','|---|---:|---:|---|']
 for r in x['contract_price_functions']:lines.append(f"| {r['player']} / {r['team']} | ${r['price_interval_first_season'][0]:,}–${r['price_interval_first_season'][1]:,} | {r['term_seasons']}년 | {r['FA_class_when_expired']} |")
 lines+=['','## 법적 반환과 경제 권고','',
  '루트가 가격 합의 가족을 채택할 수 있도록 만료 분기의 기존 minimum 함수를 동일 선수 Bird 가격으로 교체하는 반환을 제공한다. 추가 minimum UPC나 두번째 슬롯을 더하지 않는다. 추천 상단으로 전액 보호·0–8% 인상·마지막 PO 또는 옵션 없음의 합의 형태를 실제 계산한다. 91개 함수 끝점 검문은 실제 계약 91개가 아니다. 각 원 계약이 허용하는 status만 적용한다. 새 보너스 0은 명시된 합의 제안이며 원 Γ 부재증명이 아니다.',
  'Harden/Irving/Beal의 FY22 옵션은 원 기한 내 행사 또는 적법 불행사 뒤 합의로 분리한다. Kawhi/Powell은 이미 선택된 FY21 마지막 PO, Hart/Lonzo는 선택된 1년 QO의 만료가 입력이다. 후대 다른 팀 새 UPC를 원 세계 계약으로 복사하지 않는다.',
  'Bird는 직전 3시즌 표준계약과 I1(yy)의 허용 양도 이력을 보존하는 명명된 가족 조건이다. Harden의 HOU→BKN trade는 자격 연속성을 끊는 FA 이동이 아니다. 단순 프로파일 UnderContract를 동일 UPC/자격 증명으로 쓰지 않는다. 자격 조건을 만족하지 않으면 높은 가격 함수는 실행되지 않고 해당 EarlyBird/NonBird/min 한도만 적용한다.',
  'II7 전체 최대는 cap25/30/35%와 prior Salary105% 중 큰 값이다. 제안 구간은 cap비율 이하의 충분부분집합이며 상위 priorSalary 분기를 0으로 지우지 않는다. 비상장 인센티브/서명·양도 보너스를 실제 0으로 인증하지 않는다.',
  'Bridges 가격은 감도만 남긴다. root 권고는 새 UPC 없음·CHA FA/QO 권리/보류액 보존이다. [NBA 공식 2023-04-14](https://www.nba.com/news/nba-suspends-miles-bridges-for-30-games-without-pay)의 미서명/82결장 보고를 읽었으나 April 징계를 Oct 금지로 소급하지 않았다. 직접 HTTP 1회403은 원본문 채택0이고 web 본문 관측과 구분했다.',
  '정규 hold150/190%, RSC 두번째 옵션 후250/300%, RFA QO/FRN와 apron 별도 정의를 보존한다. 새 서명은 해당 hold를 대체한다. 기존 Γ와 기타 비용은 유지하고 팀 다른 TaxTeamSalary B를 넣어 비반복/반복 tax 함수의 추가액을 계산한다. B=0이나 전체 팀 apron PASS는 선언하지 않는다.',
  '추천 구간은 실제 공개 계약의 비교 가격과 동일팀 유지 이익을 참고한 가상 합의 제안이다. 다른 팀의 보장/PO/노트레이드 조항·후대 부상·거래는 복사하지 않았다. Bridges는 제도적 불확실성을 포함하여 합의 실행 권고에서 제외한다.',
  '', '## 출처와 다음 유한 입력','']
 for r in x['raw_body_observations']:
  lines.append(f"- [{r['id']}]({r['url']}): raw `{r['raw_sha256']}`; 본문 locator `{r.get('direct_observation_body_lines',r.get('locator','official release'))}`. {r.get('bounded_fact_summary','2022cap/tax primary release.')}")
 lines+=['','13개 NBA 원 HTML은 계약금액의 보도 맥락이며 사적 UPC 원문이 아니다. Hornets QO 발표는 직접 구단 발표다. OPTIONS 페이지의 오래된 Aug1 자유계약 문장은 2022 일정 근거로 채택하지 않는다. 2022 Bird 창은 reviewed LaVine calendar를 재사용한다. 원 CBA29쪽의 raw/추출 SHA를 JSON에 보존했다.',
  '', '다음: 적법 expiry/decline 및 가격 합의 후보를 root가 채택하고 팀별 B_normal/B_apron/B_tax를 동일 날짜 원 Γ와 결합한다. N23/A23, 실제 notice/consent/fee, 전체 macro3/시즌/원고는 미인증이다.',
  '', '| 큰 묶음 | 현행 |','|---|---|','| 1 초기 설계 | 완료 |','| 2 S2 유한시즌 | 완료·재개0 |','| 3 후속 커리어 | 진행·가격 가족 후보 |','| 4 전체 경력 | 미완료 |','| 5 기능 설계 | 현행 누적 등록기 참조·Pack0 |','| 6 설정집 | PARTIAL |','| 7 원고 | CLOSED |','',
  '미완료 큰 묶음5 / 6번까지4. v0.30 PARTIAL·CLOSED·중앙/REGISTER/선택 승격0.']
 return '\n'.join(lines)+'\n'

def validate(x):
 try:assert x==build(),'Saved output differs from source-bound complete reconstruction';return []
 except AssertionError as e:return [str(e)]

def self_test():
 base=forms();count=0
 def rejects_form(field,value,index=0):
  nonlocal count
  bad=copy.deepcopy(base);bad[index][field]=value
  with patch(__name__+'.forms',return_value=bad):
   try:build()
   except AssertionError:count+=1;return
  raise AssertionError('FALSE_PASS '+field)
 q=copy.deepcopy(base[0]['qualifying_service']);q['qualifying_seasons']=2
 rejects_form('qualifying_service',q);rejects_form('new_unlikely_bonus',100000)
 rejects_form('price_interval_first_season',[33000000,50000000]);rejects_form('all_original_Gamma_preserved',False)
 rejects_form('actual_market_acceptance',True);rejects_form('N23',0)
 rejects_form('existing_live_UPC_action','NEW_MINIMUM_RENEWAL')
 rejects_form('Miles_no_UPC_recommendation',False,2)
 original=resolve
 def badresolve(*args,**kwargs):
  v=original(*args,**kwargs)
  if v['new_UPC']:v['normal_current_new_charge']='0'
  return v
 with patch(__name__+'.resolve',side_effect=badresolve):
  try:build()
  except AssertionError:count+=1
  else:raise AssertionError('FALSE_PASS returned price charge')
 assert hold(10000000,True,False,50000000,1000000)['normal']==15000000
 assert hold(10000000,False,True,50000000,1000000)['normal']==30000000
 assert hold(10000000,True,False,50000000,1000000,16000000,0,True)['apron']==16000000
 assert tax(TAX+11000000)==18750000 and tax(TAX+11000000,True)==29750000
 return count

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
 x=build()
 if args.write:(ROOT/OUT).write_text(dump(x),encoding='utf-8');(ROOT/MD).write_text(render(x),encoding='utf-8')
 if args.check:assert json.loads(read(OUT))==x and read(MD)==render(x),'Stored artifact stale'
 n=self_test() if args.self_test else None
 print(dump({'current':True,'core11':11,'endpoint_checks':len(x['endpoint_function_checks']),'negatives':n,'whole_cost_PASS':False,'new_price_selections':0}).strip())
if __name__=='__main__':main()
