"""Finite NPC operating family for DET A; actual transactions remain unclaimed.

Only consumed fields of reviewed parents are checked. Their financial DAGs are
not rerun. q is a whole lawful offer interval and minimum salaries are functions,
not invented agreed dollar amounts. Root selection is pending independent review.
"""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from unittest.mock import patch
import fitz

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_detroit_2021_a_routine_operating_execution_family.py'
OUT='research/DETROIT_2021_A_ROUTINE_OPERATING_EXECUTION_FAMILY_2026_10_07.json'
MD=OUT.replace('.json','.md')
BASELINE='51ab52af234c67ec1f34fe4dade717ba2bad9561'
ROLE='simulation/CHICAGO_DETROIT_2021_TWO_DATE_WORKING_EXECUTION.json'
OPERATING='research/DETROIT_2021_OPENING_NAMED_OPERATING_FAMILY_2026_10_07.json'
RESIDUAL='research/DETROIT_2021_INITIAL_RESIDUAL_COST_FAMILY_2026_10_07.json'
AUTH='canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json'
HEALTH='simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json'
PAIR='simulation/CHICAGO_DETROIT_2021_OPENING_PAIRED_REGULATION_CARRIER.json'
ADOPTION='simulation/DET_TWO_DATE_ROLE_ADOPTION_2026_10_07.json'
PINS={ROLE:'fc44fe1b28318c2004529fc68a3b3d6b090f9b3a100265ca5e9517c0da3676b3',
 OPERATING:'7490b1a46a744088980c115680140383615a2e6ec92901e1fdd901c326861be0',
 RESIDUAL:'cf90a22c8fc7818a92a054c331347f836933ba0af83655464805048bcded5205',
 AUTH:'51b24c8a6bc1eb703568adced46b3ffa15845e85e8da10da1242bddf941df960',
 HEALTH:'274a35e163c7f6fd7f0d3e5494b3c46753aaf9900036676be935f17a9d538c32',
 PAIR:'45f204a0f213ea51b9de0a1d0ae47b50568a8d990d339822d9cd49a6ca274a00',
 ADOPTION:'8accb225b9414266cb3c7303643a85cae99751495d4d22933e675d15106a6c7e'}
CAP=112414000;APRON=143002000;X_MAX=5361732;MIN_UPPER=3000000
FIXED_POLICY={
 'classification':'ROOT_REVIEW_PENDING_ROUTINE_NPC_WORKING_FAMILY_WITHOUT_NEW_CORE_OR_ASSET_DIRECTION',
 'selected':False,'exact_price_selected':None,'q_interval':[3000000,7000040],
 'Olynyk':{'years':3,'annual_raise_fraction':'1/20','new_bonus':0,'options':0,'compensation_protection':'FULL_STANDARD_PROTECTION'},
 'minimum_players':{'Saben Lee':2,'Frank Jackson':2,'Isaiah Livers':2,'Rodney McGruder':1,'Trey Lyles':2},
 'minimum_function':'II6 legal applicable2021 signed scale for each year/YOS; first-year and second-year salary each at most3m admitted conservative ceiling, not chosen salary',
 'minimum_bonus':0,'minimum_options':0,
 'Joseph':{'years':2,'first_year':4910000,'second_year':5155500,'bonus':0,'route':'ROOM_MLE'},
 'Diallo':{'years':2,'first_year':5200000,'second_year':5200000,'bonus':0,'route':'BIRD_PRIOR_TEAM_CONTINUOUS_SERVICE'},
 'TW_players':['Luka Garza','Chris Smith'],'TW_years':1,'TW_bonus':0,'TW_options':0,
 'TW_compensation':'Legal operative2021-22 Two-Way compensation function, cash owed is not claimed zero; separate from excluded Team Salary',
 'TW_NBA_game_activation_on_two_dates':0,'TW_conversion_before_Oct23':False,
 'Suggs_RSC':'Lawful4-season Rookie Scale Contract at permitted80–120%, first-year at most already reserved6592920; option decisions not made here',
 'Aldama':'Valid completed team-signed RequiredTender within operative2021 second-round window; lawful minimum function≤3m, unaccepted throughOct23, no UPC/no STD slot',
 'first_agreements_for_new_players_after_q':True,
 'pre_room_cleanup':'Lawful effective Joseph/McGruder/Cook waiver before earliest applicable old guarantee trigger; owed/protected original money remains reserved. Explicit FA/exception renunciation before q.',
 'no_new_unreported_compensation_resolution_selected':True,
 'waive_without_assignment':['Sekou Doumbouya','Jahlil Okafor'],'waiver_request_hypothesis':'2021-09-01',
 'effective_clearance_before':'2021-10-19','reserve_both_full_current_salaries':True,'new_stretch_or_setoff':False,
 'Jordan_trade_selected':False,'Jordan_cash_or_four_second_rights_imported':False,
 'new_offer_sheet_or_First_Refusal_Notice':False,'new_NTMLE_TaxMLE_BAE_S_and_T_acquisition':False,
 'no_intervening_role_affecting_event_selected_between_two_dates':True,
 'actual_receipt_acceptance_or_private_absence_certified':False,
}

def require(ok,msg):
 if not ok:raise ValueError(msg)

def normalized_sha(path):
 return hashlib.sha256(path.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def load(root,path):return json.loads((root/path).read_text(encoding='utf-8-sig'))

def checked_sources(root):
 s={}
 for path,pin in PINS.items():
  require(normalized_sha(root/path)==pin,'Source changed: '+path)
  x=load(root,path);require(x==json.loads((root/path).read_text(encoding='utf-8-sig')),'Source loader substituted content');s[path]=x
 r=s[RESIDUAL];op=s[OPERATING];a=s[AUTH]
 require(r['base_ledger']['sum']==100052228 and r['initial_X']['public_named_family_upper']==X_MAX,'Reviewed economic base changed')
 require(sum(x['usd'] for x in r['source_contract_templates']['X_rows'])==X_MAX,'Residual named rows changed')
 require(len(r['six_category_map'])==6 and not r['policy']['unknown_private_costs_certified_zero'],'Public cost scope changed')
 require(r['policy']['preserved_RFA_QO_names']==['Saben Lee','Frank Jackson','Hamidou Diallo'],'Preserved RFA identities changed')
 require(op['named_cap_route_A']['same_route_room_deficit_with_that_delta']==4161378,'Original-price comparison changed')
 require(a['status']=='SELECTED_AND_82_CHICAGO_DATE_STATES_EXECUTED_OPPONENT_AND_RESULT_HOLD'
         and a['selected']['selected_date_rows']=={'path':HEALTH,'pointer':'/selected_dates','sha256':PINS[HEALTH]},'Canon CHI date-state authority changed')
 adoption=s[ADOPTION]
 require(adoption['status']=='SELECTED_TWO_DATE_ROLE_AVAILABILITY_AND_REGULATION_MODEL'
  and adoption['selected_role']=='A_garza_two_way_retained' and adoption['selected_game_ids']==['0022100004','0022100030']
  and adoption['source_sha256'][ROLE]==PINS[ROLE] and adoption['source_sha256'][AUTH]==PINS[AUTH]
  and not adoption['whole_financial_admission_selected'] and not adoption['score_winner_OT_selected'],'Root role/financial authority scope changed')
 return s

def cba_support(s):
 meta=s[OPERATING]['rules']['CBA'];p=Path(meta['cache_path']);require(hashlib.sha256(p.read_bytes()).hexdigest()==meta['raw_sha256'],'CBA raw changed')
 doc=fitz.open(p);pages=[39,40,54,55,71,72,74,75,202,206,211,212,213,216,217,223,231,232,233,239,240,241,303,304,412,561]
 text={n:doc[n-1].get_text() for n in pages}
 require('no bonuses of any kind' in text[233] and 'two (2)' in text[233],'Minimum exception source changed')
 require('renounce its rights to use an' in text[240] and 'Exception' in text[240],'Exception cleanup source changed')
 require('Two-Way Player Salaries shall be excluded' in text[216],'TW Salary exclusion source changed')
 require('four (4) or more' in text[74] and 'Option Year' in text[74],'TW eligibility/term source changed')
 require('shall be included' in text[202] and 'waiver' in text[202],'Waiver retained-cost source changed')
 require('2,328,652' in text[561] and '2,445,085' in text[561] and 'EXHIBIT C' in text[561],'Primary minimum scale ceiling changed')
 return {'url':meta['url'],'cache_path':str(p),'raw_sha256':meta['raw_sha256'],
         'reused_original_PDF_not_new_source_collection':True,
         'PDF_1based_fitz_text_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest() for n,t in text.items()},
         'connections':['II6/VII6i: exact legal minimum functions, maximum2seasons, no bonus; upper is not chosen money.',
          'II11/VII4j/XXIX: eligible two1-season TW with no option/bonus, excluded Team Salary, nonzero legal compensation; neither activated for these games.',
          'VII5b/6g/6m2: explicit prior renunciation, room use before new other agreements, Joseph uses only eligible roomMLE.',
          'VII4a1i/II13: preserve former salary and disclosed agreements; no waiver-to-zero, no new stretch/setoff.',
          'VII6b/I1: Diallo prior-team qualifying service admission preserved, no new S&T acquisition.',
          'VIII1/VII4e: Suggs rookie exception replaces preserved120%hold, ordinary legal term/options retained.',
          'X4/I1 RequiredTender: operative timely team-signed Aldama minimum offer/nonacceptance is distinct from UPC.',
          'VII6m3: include performance and youngFA floor when applicable; pendingRFA/RT retained, unsigned1R/FA/exception/incomplete adjustments separate; roomMLE alone is not hardcap.']}

def minimum_support(s):
 raw=Path('C:/Users/STORMC~1/AppData/Local/Temp/fr-det-routine-20261007/nba2017_cap.html')
 require(hashlib.sha256(raw.read_bytes()).hexdigest()=='afe1715faa754586a31b0f0ac6347fd538f8cb604c01049bc989f3628be4b08a','Official2017 cap raw changed')
 require('$99.093 million' in raw.read_text(encoding='utf-8'),'Official cap body changed')
 # This diagnostic is not a replacement for the league's prepared/rounded table.
 diagnostic=[Fraction(n*CAP,99093000) for n in (2328652,2445085)]
 meta=s[OPERATING]['rules']['minimum_table'];raw_table=Path(meta['cache_path'])
 require(hashlib.sha256(raw_table.read_bytes()).hexdigest()==meta['raw_sha256'],'Reused minimum table changed')
 require(all(v<MIN_UPPER for v in meta['signed2021_max_table_Year1_2_3'][:2]) and all(v<MIN_UPPER for v in diagnostic),'Minimum ceiling lacks support')
 return {'new_needed_primary_cap_anchor':{'url':'https://pr.nba.com/nba-salary-cap-2017-18-season/','cache_path':str(raw),
         'raw_sha256':'afe1715faa754586a31b0f0ac6347fd538f8cb604c01049bc989f3628be4b08a','HTTP':200,'original_cap':99093000},
         'CBA_2017_ExhibitC_PDF':561,'all_YOS_max_first_two_years':[2328652,2445085],
         '2021_cap':CAP,'II6_scale_adjustment_unrounded_diagnostic':[str(v) for v in diagnostic],
         'diagnostic_is_not_prepared_statutory_rounded_dollar_point':True,
         'reused_secondary_prepared_table':meta,'family_minimum_each_year_legal_function_ceiling':MIN_UPPER,
         'actual_cents_certified':False,'no_new_contract_salary_chosen':True}

def policy():return deepcopy(FIXED_POLICY)

def contract_forms(p):
 forms={}
 for name,years in p['minimum_players'].items():
  forms[name]={'kind':'STANDARD_MINIMUM','years':years,'salary_each_year':'APPLICABLE_LEGAL_2021_SIGNED_SCALE_AT_PLAYER_YOS',
               'each_year_upper':MIN_UPPER,'bonus':0,'options':0,'guarantee':'FULL_STANDARD_PROTECTION','consent':'HYPOTHETICAL_LAWFUL_PLAYER_TEAM_ACCEPTANCE'}
 forms['Kelly Olynyk']={'kind':'CAP_ROOM','years':3,'first_year_interval':p['q_interval'],
                     'future_salary_function':['q','floor(21*q/20)','floor(22*q/20)'],
                     'annual_increment_at_most':'q/20','bonus':0,'options':0,'guarantee':'FULL_STANDARD_PROTECTION','consent':'HYPOTHETICAL'}
 for n,k in [('Cory Joseph','Joseph'),('Hamidou Diallo','Diallo')]:forms[n]={'kind':p[k]['route'],**deepcopy(p[k]),'guarantee':'FULL_STANDARD_PROTECTION','options':0,'consent':'HYPOTHETICAL'}
 for n in p['TW_players']:forms[n]={'kind':'TWO_WAY','years':1,'YOS_at_start':0,'maximum_YOS_during_term':1,
        'prior_same_team_TW_salary_cap_years':0,'bonus':0,'options':0,'NBA_activation_at_two_dates':0,
        'salary_function':'OPERATIVE_2021_22_LEGAL_TW_COMPENSATION','cash_certified_zero':False,'Team_Salary_component':0,
        'consent':'HYPOTHETICAL','conversion_selected':False,'no_prior_same_team_standard_salary_above_TW_termination_disqualifier':True}
 forms['Jalen Suggs']={'kind':'ROOKIE_SCALE','years':4,'scale_percentage_interval':[80,120],'first_year_upper':6592920,
                      'NBA_UPC_proposed':True,'guarantee':'LEGAL_RSC_FIRST_TWO_YEARS','year3_year4_option_decisions':None,'actual_pick_or_money':None}
 forms['Santi Aldama']={'kind':'REQUIRED_TENDER_ONLY','salary_function':'APPLICABLE_LEGAL_MINIMUM','upper':MIN_UPPER,
      'team_signed':True,'operative_2021_window':'W21_DRAFT_MODIFIED_VALID_DELIVERY_WINDOW',
      'delivery_date':'tRT in W21 intersect [2021-07-29,2021-10-19]; Sep1 is a permitted display hypothesis only IF inside W21',
      'deadline_certificate':False,'lawful_tender_delivery_assumed_as_fictional_implementation':True,
      'acceptance_window':'LEGAL_OPERATIVE_SECOND_ROUND_TENDER_ACCEPTANCE_WINDOW','unaccepted_through':'2021-10-23',
      'not_withdrawn_or_renounced':True,'NBA_UPC':False,'standard_slot':0,'actual_receipt_or_nonacceptance_certified':False}
 return forms

def assert_forms(f,p):
 require(set(f)==set(p['minimum_players'])|set(p['TW_players'])|{'Kelly Olynyk','Cory Joseph','Hamidou Diallo','Jalen Suggs','Santi Aldama'},'Contract family identity changed')
 for n,y in p['minimum_players'].items():
  x=f[n];require(x['kind']=='STANDARD_MINIMUM' and x['years']==y<=2 and x['salary_each_year']=='APPLICABLE_LEGAL_2021_SIGNED_SCALE_AT_PLAYER_YOS'
   and x['each_year_upper']==MIN_UPPER and x['bonus']==0 and x['options']==0
   and x['guarantee']=='FULL_STANDARD_PROTECTION' and x['consent']=='HYPOTHETICAL_LAWFUL_PLAYER_TEAM_ACCEPTANCE','Minimum legal function/bonus/term changed')
 for n in p['TW_players']:
  x=f[n];require(x['kind']=='TWO_WAY' and x['years']==1 and x['YOS_at_start']==0 and x['maximum_YOS_during_term']<4
   and x['prior_same_team_TW_salary_cap_years']==0 and x['bonus']==0 and x['options']==0
   and x['NBA_activation_at_two_dates']==0 and not x['cash_certified_zero'] and x['Team_Salary_component']==0
   and not x['conversion_selected'] and x['no_prior_same_team_standard_salary_above_TW_termination_disqualifier'],'TW eligibility/compensation changed')
 require(f['Kelly Olynyk']['first_year_interval']==[3000000,7000040] and f['Kelly Olynyk']['years']==3
         and f['Kelly Olynyk']['kind']=='CAP_ROOM' and f['Kelly Olynyk']['bonus']==0 and f['Kelly Olynyk']['options']==0
         and f['Kelly Olynyk']['future_salary_function']==['q','floor(21*q/20)','floor(22*q/20)'],'q family changed')
 for n,k in [('Cory Joseph','Joseph'),('Hamidou Diallo','Diallo')]:
  require(all(f[n][key]==val for key,val in p[k].items()) and f[n]['options']==0 and f[n]['kind']==p[k]['route'],'Named exception term changed')
 require(f['Jalen Suggs']['kind']=='ROOKIE_SCALE' and f['Jalen Suggs']['years']==4 and f['Jalen Suggs']['first_year_upper']==6592920
         and f['Jalen Suggs']['year3_year4_option_decisions'] is None,'Unsigned1R cost/UPC changed')
 t=f['Santi Aldama'];require(t['kind']=='REQUIRED_TENDER_ONLY' and t['team_signed'] and t['upper']==MIN_UPPER
  and not t['NBA_UPC'] and t['standard_slot']==0 and t['unaccepted_through']=='2021-10-23'
  and t['salary_function']=='APPLICABLE_LEGAL_MINIMUM' and not t['deadline_certificate']
  and t['not_withdrawn_or_renounced'] and t['operative_2021_window']=='W21_DRAFT_MODIFIED_VALID_DELIVERY_WINDOW'
  and not t['actual_receipt_or_nonacceptance_certified'],'RT receipt/UPC/operative window changed')

def event_specs():
 # Prefix total amounts are ceilings, not promised contract amounts.
 return [
  ('2021-08-09','OLYNYK_CAP_ROOM','Kelly Olynyk','ADD_STD','q'),
  ('2021-08-09','LEE_MINIMUM','Saben Lee','ADD_STD',3000000-925258),
  ('2021-08-10','FRANK_MINIMUM','Frank Jackson','ADD_STD',3000000-1939350),
  ('2021-08-10','LIVERS_MINIMUM','Isaiah Livers','ADD_STD',3000000),
  ('2021-08-10','SUGGS_RSC_REPLACE_UNSIGNED_HOLD','Jalen Suggs','ADD_STD',0),
  ('2021-08-10','JOSEPH_ROOM_MLE','Cory Joseph','ADD_STD',4910000),
  ('2021-08-11','MCGRUDER_MINIMUM','Rodney McGruder','ADD_STD',3000000),
  ('2021-08-11','LYLES_TWO_YEAR_MINIMUM','Trey Lyles','ADD_STD',3000000),
  ('2021-08-16','GARZA_TW_NO_STANDARD_CONVERSION','Luka Garza','ADD_TW',0),
  ('2021-08-19','DIALLO_BIRD_REPLACE_QO','Hamidou Diallo','ADD_STD',5200000-2079826),
  ('2021-09-01','SEKOU_OKAFOR_WAIVER_FULL_CHARGE_RETAINED',['Sekou Doumbouya','Jahlil Okafor'],'REMOVE_STD',0),
  ('OPERATIVE_tRT_BEFORE_OPENING','ALDAMA_UNACCEPTED_REQUIRED_TENDER','Santi Aldama','RIGHT_ONLY',3000000),
  ('2021-09-24','CHRIS_SMITH_TW','Chris Smith','ADD_TW',0),
 ]

def trace(s,p):
 std=list(s[RESIDUAL]['base_ledger']['current_8']);tw=[];constant=100052228; qcoef=0;out=[]
 def row(i,date,event,player,delta):
  return {'index':i,'date_hypothesis':date,'event':event,'player':deepcopy(player),'normal_upper_constant':constant,
          'X_coefficient':1,'q_coefficient':qcoef,'domain_endpoint_normal_upper':constant+X_MAX+qcoef*7000040,
          'normal_salary_delta_upper':delta,'standard':std.copy(),'two_way':tw.copy(),'STD':len(std),'TW':len(tw),
          'offseason_players_including_TW':len(std)+len(tw),'money_is_bound_not_chosen_salary':True}
 out.append(row(0,'2021-08-09 BEFORE q','ROOM_CLEANUP_COMPLETED_WITH_OWED_COST_RESERVED',None,0))
 for i,(date,event,player,operation,delta) in enumerate(event_specs(),1):
  if operation=='ADD_STD':std.append(player)
  elif operation=='ADD_TW':tw.append(player)
  elif operation=='REMOVE_STD':
   for name in player:std.remove(name)
  if delta=='q':qcoef=1
  else:constant+=delta
  out.append(row(i,date,event,player,delta))
 return out

def assert_trace(rows,s,a):
 require(len(rows)==14,'Dated economic prefix size changed')
 std=list(s[RESIDUAL]['base_ledger']['current_8']);tw=[];constant=100052228;qcoef=0
 for i,r in enumerate(rows):
  if i:
   date,event,player,operation,delta=event_specs()[i-1]
   if operation=='ADD_STD':std.append(player)
   elif operation=='ADD_TW':tw.append(player)
   elif operation=='REMOVE_STD':
    for name in player:std.remove(name)
   if delta=='q':qcoef=1
   else:constant+=delta
   require((r['date_hypothesis'],r['event'],r['player'],r['normal_salary_delta_upper'])==(date,event,player,delta),'Returned event/actor/cost chain changed')
  else:
   require((r['date_hypothesis'],r['event'],r['player'],r['normal_salary_delta_upper'])==
    ('2021-08-09 BEFORE q','ROOM_CLEANUP_COMPLETED_WITH_OWED_COST_RESERVED',None,0),'Initial cleanup relabeled')
  require(r['index']==i and r['normal_upper_constant']==constant and r['q_coefficient']==qcoef and r['X_coefficient']==1,'Returned affine charge changed')
  require(r['domain_endpoint_normal_upper']==constant+X_MAX+qcoef*7000040,'Returned interval endpoint changed')
  require(r['standard']==std and r['two_way']==tw and r['STD']==len(std) and r['TW']==len(tw)
          and r['offseason_players_including_TW']==len(std)+len(tw)<=20,'Returned registration prefix changed')
  require(len(std)==len(set(std)) and len(tw)==len(set(tw))<=2 and not set(std)&set(tw),'Duplicate/class-overlap slot')
 require(set(std)==set(a['standard_candidate']) and tw==a['two_way_candidate'] and len(std)==15,'A opening roster not reached')
 require(constant==123217794 and rows[-1]['domain_endpoint_normal_upper']==135579566,'Final charge not source-connected')
 require(s[RESIDUAL]['base_ledger']['current_8']['Sekou Doumbouya']+s[RESIDUAL]['base_ledger']['current_8']['Jahlil Okafor']==5743703,'Waiver carry changed')

def date_execution(s,a,rows):
 witness=next(w for w in s[PAIR]['witnesses'] if w['id']=='COBY_OUT__A_garza_two_way_retained');out=[]
 for gid,date in [('0022100004','2021-10-20'),('0022100030','2021-10-23')]:
  h=next(x for x in s[HEALTH]['selected_dates'] if x['game_id']==gid)
  old=next(x for x in s[ROLE]['rows'] if x['game_id']==gid)
  require(h['date']==old['date']==date and h['selected_chicago_state']==old['selected_chicago_state']=='COBY_OUT','Date state join changed')
  require(old['nominations']==witness['nominations'] and old['simultaneous_segments']==witness['simultaneous_segments'],'Prepared clock source changed')
  counters={'CHI':Counter(),'DET':Counter()};end=0
  for block in witness['simultaneous_segments']:
   require(block['start_second']==end and block['end_second']-end==block['seconds']>0,'Bilateral clock gap')
   for t in counters:
    require(set(block[t])=={'PG','SG','SF','PF','C'} and len(set(block[t].values()))==5,'Five-position clock invalid')
    require(set(block[t].values())<=set(witness['nominations'][t]['active']),'Lineup outside active nominees')
    for person in block[t].values():counters[t][person]+=block['seconds']
   end=block['end_second']
  require(end==2880 and all(sum(x.values())==14400 for x in counters.values()),'Regulation capacities not reached')
  require(dict(counters['CHI'])=={n:m*60 for n,m in h['selected_regulation_player_minutes'].items()},'Canon CHI minutes changed')
  require(set(rows[-1]['standard'])==set(witness['nominations']['DET']['standard'])
          and rows[-1]['two_way']==witness['nominations']['DET']['two_way'],'Financial prefix/clock membership mismatch')
  for t in counters:
   n=witness['nominations'][t];require(len(n['active'])==12 and len(n['inactive'])==3
    and set(n['active'])|set(n['inactive'])==set(n['standard']) and not set(n['active'])&set(n['inactive']),'Legal nomination partition invalid')
  out.append({'game_id':gid,'date':date,'home':h['home'],'away':h['away'],'CHI_state':'COBY_OUT',
   'source_role_pointer':'/rows/'+str(s[ROLE]['rows'].index(old)),'role_source':ROLE,
   'economic_prefix_pointer':'/registration_and_cost_prefix/13','routine_contract_family_admitted_for_date':True,
   'nomination_and_positive_availability_implemented_within_family':True,
   'DET_positive_operational_availability':sorted(counters['DET']),'zero_minute_clinical_status':None,
   'nominations':deepcopy(witness['nominations']),'simultaneous_segments':deepcopy(witness['simultaneous_segments']),
   'regulation_seconds':2880,'player_seconds_each':14400,'root_role_selected':True,'root_role_adoption_source':ADOPTION,
   'root_family_selected':False,'actual_registration_or_medical':False,
   'overtime':None,'score':None,'winner':None})
 return out

def build(root=ROOT):
 s=checked_sources(root);p=policy();require(p==FIXED_POLICY,'Routine policy changed');cba=cba_support(s);mins=minimum_support(s)
 forms=contract_forms(p);assert_forms(forms,p)
 a=next(x for x in s[OPERATING]['roster_candidates'] if x['id']=='A_garza_two_way_retained')
 rows=trace(s,p);assert_trace(rows,s,a)
 dates=date_execution(s,a,rows)
 require(len(dates)==2 and [x['game_id'] for x in dates]==['0022100004','0022100030'],'Returned date domain changed')
 for x in dates:
  src=next(y for y in s[ROLE]['rows'] if y['game_id']==x['game_id']);h=next(y for y in s[HEALTH]['selected_dates'] if y['game_id']==x['game_id'])
  require(x['date']==h['date'] and x['home']==h['home'] and x['away']==h['away'] and x['CHI_state']==h['selected_chicago_state']=='COBY_OUT'
   and x['nominations']==src['nominations'] and x['simultaneous_segments']==src['simultaneous_segments'],'Returned date/clock meaning changed')
  require(x['routine_contract_family_admitted_for_date'] and x['nomination_and_positive_availability_implemented_within_family']
   and x['root_role_selected'] and x['root_role_adoption_source']==ADOPTION
   and not x['root_family_selected'] and not x['actual_registration_or_medical'] and x['winner'] is None and x['overtime'] is None,'Returned scope promoted')
  require(x['DET_positive_operational_availability']==sorted(src['nominations']['DET']['positive_seconds'])
    and x['zero_minute_clinical_status'] is None,'Returned positive availability or zero-minute clinical inference changed')
 # All quantities have nonnegative coefficients: endpoint inequalities prove the
 # complete X/q/minimum domain, not only a sampled corner grid.
 require(100052228+X_MAX+7000040==CAP and 3000000<=7000040,'Universal cap-room family empty')
 cats=deepcopy(s[RESIDUAL]['six_category_map'])
 cats[0]['this_A_family']='Retained8 base and old public economics unchanged. New Lyles minimum replaces B no-signature policy explicitly; no other early notified agreement before q. New offered bonuses0 are contractual choices, not old private bonus absence.'
 cats[1]['this_A_family']='All old5+X oldcash remain. Nonassignment Sekou/Okafor waive without stretch/setoff; full5,743,703 stays in base and does not create room.'
 cats[2]['this_A_family']='Lee/Frank/Diallo holds until valid accepted replacement, no free removal; unused named FA rights legally renounced/no outstanding QO at action; no other offer/FRN selected.'
 cats[3]['this_A_family']='Suggs120%unsignedhold becomes lawful RSC. Aldama operative unaccepted RT costs3m ceiling and noSTD slot. Other public old rights retain source window/no selected new UPC; any new valid tender reopens its charge.'
 cats[4]['this_A_family']='Before q12 cap-count identities; offseason maximum18 inclTW; after two full-charge waivers15STD2TW. Two dates12active/3inactive, TW not NBA-activated; no incomplete charge needed.'
 cats[5]['this_A_family']='Explicit eligible renunciation before room; no NTMLE/TaxMLE/BAE use in2021-22. Joseph only roomMLE and all other signings use their separate exceptions; no aggregate exception combination or new S&T hardcap.'
 return {'id':'DETROIT_2021_A_ROUTINE_OPERATING_EXECUTION_FAMILY','baseline_main':BASELINE,
  'status':'SOURCE_SUPPORTED_ROUTINE_A_FULL_PUBLIC_IMPLEMENTATION_FAMILY_ROOT_REVIEW_PENDING',
  'source_sha256':{**PINS,SELF:normalized_sha(root/SELF)},'hash_convention':'Normalized UTF8 BOM-strip/CRLF-or-CR-to-LF; external raw unchanged',
  'scope':'Admitted source-supported public named economic family plus explicit lawful hypothetical notices/consents/contracts. Not actual private ledger or actual foreign/team acceptance certification.',
  'authority_interpretation':'Existing author health/operating delegation and AGENTS permit root review/selection of routine NPC family preserving Chicago approved core and major asset direction. Earlier unselected/important labels record technical state, not immutable extra permission gates.',
  'root_role_adoption':{'source':ADOPTION,'selected':True,'scope':'two-date role/positive availability/active nominees/regulation clock; economic family review remains pending',
   'prepared_precursor_flags_are_generation_state':True,'review_artifacts_are_references_not_generation_dependencies':True},
  'policy':p,'CBA_direct_reused_support':cba,'minimum_function_ceiling_support':mins,'contract_function_families':forms,
  'initial_source_public_base':deepcopy(s[RESIDUAL]['base_ledger']),
  'residual_X_named_rows':deepcopy(s[RESIDUAL]['source_contract_templates']['X_rows']),
  'six_cost_categories':cats,'registration_and_cost_prefix':rows,'two_date_execution':dates,
  'lawful_implementation_conditions':{
   'prior_cleanup':'Effective original named Joseph/McGruder/Cook waivers before each earliest applicable old protection trigger, including carried old guarantees; hypothetical timing, not original-history receipt proof.',
   'renunciation':'Valid written notices before q for reviewed unused FA/exceptions; no still-outstanding QO renunciation; Lee/Frank/Diallo retained until replacing contracts.',
   'signing_sequence':'All new agreements including notified agreements occur at their depicted sequential step; lawful Commissioner approval/UPC/notice/waiver processing proposed, not actual receipt or unpaid-for future promise.',
   'Bird_identity':'Diallo admitted3 prior NBA seasons/continuous qualifying service transferred with original same prior-team rights; no free invented Bird years.',
   'DB1_rights':'Conditional existing working DB1 DET pick5Suggs/37Aldama/38Livers/50Garza holds valid drafted negotiating rights, no competing unexpired foreign/college constraint blocking proposed lawful acceptance; no draft direction chosen here.',
   'operative_tender':'Choose valid tRT in actual operative2021 W21 beforeOct20, complete legal team-signed minimum RequiredTender, and lawful player nonacceptance throughOct23. Exact original filing/date/acceptance is not certified.',
   'TW_identity':'Garza/Smith admitted2021 rookieYOS0; no prior same-team standard termination with disqualifying protected amount, no4YOS/over3same-team-TW-year bar; legal2021operative TW UPCs beforeOct20, no conversion/activation for these games.',
   'waiver':'Sekou/Okafor ordinary lawful waivers requestSep1 with valid processing/clearance byOct19; all current contractual salary retained, no new stretch/setoff or assignment into BKN. Registration effect alone releases DET roster slots.',
   'source_family_reopen':'An additional preserved named promise/bonus/tender/settlement or selected new event reopens its own cost. This is not a certificate of universal private absence.'},
  'complete_domain_proof':{'X_interval':[0,X_MAX],'q_interval':[3000000,7000040],
   'q_dynamic_upper':'min(12195122,112414000-100052228-X)','nonempty_for_all_admitted_X':True,
   'pre_q_initial_normal_upper':100052228+X_MAX,'q_room_minimum':7000040,
   'post_q_upper':CAP,'post_q_other_increment_upper':23165566,
   'normal_upper_after_all_events':135579566,'apron_upper_at_two_dates':135579566,
   'apron_adjustment_basis':'All new performance bonuses0; public retained template/residual same; young new FA lawful2YOS apron floor≤3m included; Aldama RT≤3m remains; all expired holds replaced/renounced; TW excluded, no unused exceptions or unsigned1R left at these dates.',
   'young_minimum_apron_floor_reserved_within_each_3m':True,'apron_comparison_margin':7422434,
   'room_MLE_is_not_hardcap_trigger':True,'new_2021_22_hardcap_trigger_selected':False,
   'entire_family_cap_and_exception_path_sufficient_within_named_admissions':True,
   'actual_X_or_exact_price':None,'original_A_price_deficit_comparison_preserved':4161378},
  'butterfly_effect_handoff':{
   'Sekou_Okafor':'No BKN assignment in this family. Future destination/price/health remains unselected; full DET current salary not removed.',
   'BKN_Jordan':'No DET incoming Jordan and no BKN outgoingJordan salary relief; original Nets own Jordan economic object retained pending separate BKN route. No historical Jordan waiver copied.',
   'Jordan_cash_four_seconds':'No DET cash receipt or2022BKN/2024WAS/2025GSW/2027BKN rights transfers copied. Earlier jointtrade witness remains comparison, not executed here.',
   'Lyles_Bagley':'Two-year Lyles minimum preserves possible2022livecontract/negotiation but changes matching salary from historical contract; originalBagley bundle cannot be reused before fresh matching/actor/rights check.',
   'Olynyk':'Three-year q family is a hypothetical source-supported routine offer range, exact price/actual willingness not inferred; role18min unchanged.',
   'original_Chicago_growth_core':'Mark32/Caruso18/P32 and selected two COBY_OUT dates unchanged; no Chicagoapproved major asset direction changed.'},
  'summary':{'six_cost_categories':6,'contract_function_families':len(forms),'registration_cost_prefix_states':len(rows),
   'offseason_players_including_TW_max':max(r['offseason_players_including_TW'] for r in rows),
   'opening_standard':15,'opening_two_way':2,'two_date_full_clock_function_executions':2,
   'root_selected_two_date_role_executions':2,
   'routine_family_selected_by_root':False,'actual_executions_certified':0},
  'certification':{'independent_review_completed':False,'root_routine_family_selection':False,
   'source_supported_public_implementation_family_sufficient_under_explicit_legal_admissions':True,
   'actual_contract_or_private_ledger_or_receipt_or_acceptance':False,'new_author_locked_draft_or_asset_direction':False,
   'whole_macro3_or_full2021_22_season':False,'central_REGISTER_changed':False,'manuscript_written':0}}

def validate(obj,root=ROOT):
 try:return [] if obj==build(root) else ['Saved family differs from current source-bound implementation']
 except (ValueError,KeyError,StopIteration) as exc:return [str(exc)]

def markdown(b):
 return '''# DET A 루틴 운영·경제 가족과 두 경기 실행\n\n상태: `'''+b['status']+'''`. 기준 main `'''+BASELINE+'''`. root 독립 검토·루틴 선택 대기이며 중앙 선택 변경0.\n\n## 이번에 완성한 입력\n\n기존 A15 명단을 유지하는 **공개 근거를 가진 가상 법적 구현 가족**이다. 기존 Chicago 성장 코어와 중요한 자산 방향을 바꾸지 않는다. 과거 후보 문구를 영구 작가 승인 장벽으로 사용하지 않는다. q·최소급여·통지·수락은 합법 가상 구현 변수이며 실제 계약·접수 사실은 아니다.\n\n- 공개 초기 base100,052,228 + X∈[0,5,361,732]. 보존 비용6범주를 각각 연결한다. 누락된 사적 비용을0이라고 인증하지 않는다.\n- **모든 q∈[3,000,000,7,000,040]**가 모든 위 X에서 cap-room 충분조건을 만족한다. 정확한 가격 하나를 선택하지 않는다. Olynyk3년·초년 기준5% 이내 증가/bonus0; 미래 연도 급여는 q의 함수다.\n- Lee/Frank/Livers/McGruder/Lyles는 실제 법정 최소급여 함수, 각각1/2년과bonus0. **3m는 급여 합의가 아니라 normal/youngFA apron floor를 포괄하는 보수 상단**이다. Lyles2년을 유지하지만 원역사 Bagley 매칭 금액을 복사하지 않는다.\n- Joseph2년 roomMLE4.91m/5.1555m, Diallo2년 Bird5.2m는 별도 합법 가상 제안이다. roomMLE와 NTMLE/TaxMLE/BAE를 결합하지 않는다.\n- Garza/Smith는 법적1년 TW 함수·YOS0·bonus0/option0, 이 두 경기 NBA activation0이다. **Team Salary 제외와 현금 급여0을 구분**한다. 원45일 서비스 규칙을2021 관측 사실로 자동 복사하지 않는다.\n- Suggs의 미서명120%hold6,592,920는 적법 RSC로 대체한다. Aldama는 operative2021 창 내 유효 team-signed RequiredTender와 미수락을 구현 조건으로 두며3m를 예약한다. RT는16번째STD가 아니고, 원제출일·개정deadline·실수락은 인증하지 않는다.\n\n## 서명·방출·비용·등록 순서\n\nq 전 법적 원계약 waiver/renunciation을 수행하되 원래 보호·미지급액을 base/X에 보존한다. 이후 notified agreement를 포함한 새 계약은 명시한 단계 순서로 구성한다. Lee/Frank/Diallo의 기존 FA/QO는 유효 대체 계약 전까지 남는다. 무효 renunciation·예외 은폐·계약약속의 선행 비용 삭제는 허용하지 않는다.\n\n등록/비용 prefix14상태: 초기8STD → Olynyk/Lee → Frank/Livers/Suggs/Joseph → McGruder/Lyles → GarzaTW → Diallo → Sekou/Okafor ordinary waiver → AldamaRT → SmithTW. offseason 최대 **18명(TW포함)**, 개막 **15STD+2TW**다.\n\nSekou/Okafor의 Sep1 요청→Oct19 이전 유효 clearance는 가상 구현 절차다. **5,743,703 현 연도 salary 전액은 그대로 보존**하며 새 stretch/setoff를 선택하지 않는다. 방출은 cap-room 확보 수단이 아니다. Jordan 거래·현금·4second권리를 같이 실행하지 않는다.\n\n최종 normal/apron 보수 상단 **135,579,566**, apron 비교 여유 **7,422,434**. 실제 teamtotal/접수/수락 인증이 아니며 nohardcap 상태에서 단순 apron 이하를 합법성 대신 쓰지 않는다. room사용→각 예외의 적법 경로로 충분성을 구성했다. 기존 A 원가격4,161,378 부족은 **원가격 비교**로 보존한다; 새 가족의 q/합법 최소함수 적용을 그 역사 숫자로 막지 않는다.\n\n## 두 날짜 실제 함수 적용\n\n`0022100004`(2021-10-20 DET–CHI), `0022100030`(10-23 CHI–DET)에 canon 선택 `COBY_OUT`을 연결했다. DET 양수10명/active12·inactive3와 동일 A 역할·가용성 모델을 두 날짜에 명시적으로 적용한다. 각 경기 양팀 동시 **2,880초 / 각240분**, Mark32/Caruso18/주인공32 그대로다. 0분 임상 상태null. 계약 가족 조건 아래의 작업 실행이며 실제 NBA 등록/의학/결과 인증이 아니다. 점수·승패·OT 선택0.\n\n최초 역할 조상의 준비 플래그는 생성 시점 상태다. 별도 `DET_TWO_DATE_ROLE_ADOPTION_2026_10_07.json`에서 root가 두 날짜 역할·가용·nomination·clock을 이미 채택했으며 새 가족은 그 기록을 직접 소비한다. 경제 가족의 독립 검토·채택은 아직 pending이다.\n\n법정 최소함수의3m ceiling 지원을 위해 기존 CBA ExhibitC PDF561·II6과 [NBA 공식2017cap99.093m](https://pr.nba.com/nba-salary-cap-2017-18-season/)의 새 raw를 연결했다. 2021cap112.414m 비례 진단/기존 표를 대조하되 정확 준비표 반올림값·실제 cents는 인증하지 않는다.\n\n## 나비효과 인계·재개방\n\n- Sekou/Okafor는 BKN 자동 이동하지 않는다. 이후 착지·가격·건강은 새 선택 시 검문한다.\n- Nets Jordan의 원경제 객체가 남으며 DET 거래로 생기는 Nets relief·뒤 waiver를 복사하지 않는다. 원 DET 현금/2022BKN·2024WAS·2025GSW·2027BKN2R 취득도 미실행이다.\n- Lyles2년 잔류는 뒤 Bagley의 가능성을 보존하지만 매칭 급여가 달라져 새 검문이 필요하다. 그 이후 거래를 여기서 선택하지 않는다.\n- 추가 보존된 명명 의무·보너스·tender·합의 또는 선택된 사건이 생기면 해당 비용만 재개방한다. 모든 미래 사적 부재 인증을 요구하지 않는다.\n\n## 검문·진행표\n\n검문은 소비7파일 원필드·직접 재사용 CBA26쪽 지문/원문 연결·14prefix 반환·cap/예외 충분식·15+2·두 날짜 clock/권위에 한정한다. 기존192/1740비용 가족 조상 재실행0. 자체 음성은 독립 검문으로 계수하지 않는다.\n\n[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md) / [현재 상태](../PROJECT_STATE.md).\n\n|번호|범위|현황|\n|---|---|---|\n|1|2020 드래프트 연쇄|완료 보존|\n|2|Chicago2020–21|완료 보존|\n|3|2021–23 거래·계약|DET A 공개 루틴 가족·두 날짜 구현 / root 독립 검토 대기|\n|4|장기 커리어|후속 시즌 입력 진행|\n|5|결말·전체 구조|기존 골격·기능 연결 진행|\n|6|집필 규격·Context Pack|현행 누적 등록기 참조 / Pack0|\n|7|통합·독립·작가 승인|부분 검문 / 최종 미완료|\n\n미완료 큰 묶음5(6번까지4). `v0.30 PARTIAL` / 설계·원고 `CLOSED` / 원고0.\n'''

def self_test(root=ROOT):
 tests=[];orig=contract_forms
 def wrong(f):
  x=orig(f);x['Trey Lyles']['bonus']=100000;return x
 with patch(__name__+'.contract_forms',wrong):
  try:build(root);raise AssertionError('Minimum bonus accepted')
  except ValueError:tests.append('RETURNED_LYLES_MINIMUM_BONUS100K_REJECTED')
 orig_t=trace
 def erased(s,p):
  x=orig_t(s,p);x[11]['normal_upper_constant']-=5743703;x[11]['domain_endpoint_normal_upper']-=5743703;return x
 with patch(__name__+'.trace',erased):
  try:build(root);raise AssertionError('Waiver free salary accepted')
  except ValueError:tests.append('RETURNED_WAIVER5743703_COST_ERASURE_REJECTED')
 return tests

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();b=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(b),encoding='utf-8')
 if a.check:require(load(ROOT,OUT)==b,'Saved JSON stale');require((ROOT/MD).read_text(encoding='utf-8-sig').replace('\r\n','\n')==markdown(b),'Saved MD stale')
 print(json.dumps({'current':True,'summary':b['summary'],'writer_negative_controls':self_test() if a.self_test else []},ensure_ascii=False))

if __name__=='__main__':main()
