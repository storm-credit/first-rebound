"""Finite Toronto regulation capacity; no economic direction/date/clinical adoption."""
from __future__ import annotations
import argparse, json, hashlib
from pathlib import Path
from collections import Counter,defaultdict
from copy import deepcopy
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_toronto_2021_named_roster_capacity.py'
BANK='research/TORONTO_2021_10_25_NAMED_OPERATING_INPUT_BANK_2026_10_07.json'
OUT='simulation/TORONTO_2021_NAMED_ROSTER_CAPACITY_CONDITIONAL_FAMILY.json'
MD=OUT.replace('.json','.md')
BANK_PIN='7b6cba6e74044f3b52a79fa966498bca1771294c8bf109bb2213e712210c7096'
POS=('PG','SG','SF','PF','C')
PATH_NAMES={
'T0':['Pascal Siakam','Fred VanVleet','OG Anunoby','Malachi Flynn','Chris Boucher','Aron Baynes',"DeAndre' Bembry",'Paul Watson','Freddie Gillespie','Yuta Watanabe','Norman Powell','Kyle Lowry','Khem Birch','Josh Giddey','Dalano Banton'],
'T1':['Pascal Siakam','Fred VanVleet','OG Anunoby','Malachi Flynn','Chris Boucher','Yuta Watanabe','Norman Powell','Khem Birch','Josh Giddey','Dalano Banton','Goran Dragic','Precious Achiuwa','Svi Mykhailiuk','Sam Dekker','Isaac Bonga']}
TW=['Sam Hauser','Justin Champagnie']
ALIASES={'L':'Kyle Lowry','F':'Fred VanVleet','N':'Norman Powell','O':'OG Anunoby','S':'Pascal Siakam','K':'Khem Birch','G':'Josh Giddey','C':'Chris Boucher','A':'Aron Baynes','B':"DeAndre' Bembry",'Y':'Yuta Watanabe','D':'Goran Dragic','P':'Precious Achiuwa','V':'Svi Mykhailiuk'}
# PG/SG/SF/PF/C. These are explicit fictional coaching choices, not historical boxes.
BASE={
'T0':[('L','N','O','S','K'),('L','N','O','S','K'),('F','N','G','S','K'),('F','N','O','C','A'),('G','F','B','C','A'),('G','F','O','Y','C'),('L','N','O','S','K'),('L','F','O','S','K'),('F','N','G','S','K'),('G','F','B','C','A'),('L','N','O','S','C'),('L','F','O','S','K')],
'T1':[('F','N','O','S','K'),('F','N','O','S','K'),('G','F','O','S','P'),('D','N','O','C','P'),('D','V','G','C','K'),('G','F','O','Y','C'),('F','N','O','S','K'),('F','N','O','S','P'),('G','N','O','S','K'),('D','V','G','C','P'),('F','N','O','S','C'),('F','N','O','S','K')]}
ELIGIBILITY={
'PG':['Kyle Lowry','Fred VanVleet','Josh Giddey','Goran Dragic','Malachi Flynn','Dalano Banton'],
'SG':['Norman Powell','Fred VanVleet','Svi Mykhailiuk','Josh Giddey','Dalano Banton'],
'SF':['OG Anunoby','Josh Giddey',"DeAndre' Bembry",'Yuta Watanabe','Isaac Bonga','Paul Watson','Sam Dekker','Sam Hauser','Justin Champagnie'],
'PF':['Pascal Siakam','Chris Boucher','Yuta Watanabe','OG Anunoby','Precious Achiuwa','Sam Dekker'],
'C':['Khem Birch','Aron Baynes','Chris Boucher','Precious Achiuwa','Freddie Gillespie']}
CREATORS=['Kyle Lowry','Fred VanVleet','Josh Giddey','Goran Dragic']
STATES=('SIAKAM_AVAILABLE','SIAKAM_UNAVAILABLE')
def require(v,msg):
 if not v:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()
def load(root=ROOT):return json.loads((root/BANK).read_text(encoding='utf-8-sig'))
def assert_bank(b,root):
 physical=json.loads((root/BANK).read_text(encoding='utf-8-sig'))
 require(b==physical,'Loaded bank differs from physical source')
 require(sha(root/BANK)==BANK_PIN,'Reviewed named bank changed')
 for p,h in b['source_sha256'].items():require(sha(root/p)==h,'Bank source-currentness failed:'+p)
 for k,names in PATH_NAMES.items():
  a=b['operating_paths'][k];require(a['standard']==names and a['two_way']==TW,'Named path identity/type changed')
 require(b['operating_paths']['both']['selected_path'] is None and not b['authority']['path_selected'],'Input path selected')
 require([(r['pick'],r['player']) for r in b['DB1_conditional_TOR_draft_ports']]==[(8,'Josh Giddey'),(46,'Dalano Banton'),(48,'Sam Hauser')],'DB1 rights changed')
 require(b['Bonga_finite_rights_boundary']['minimum_contract_start_YOS']==0,'Historical Bonga NBA seasons copied')
 require(b['whole_cost_boundary']['whole_normal_TeamSalary_upper'] is None and b['whole_cost_boundary']['whole_apron_TeamSalary_upper'] is None,'Whole cost boundary changed')
 require(b['target']=={'date':'2021-10-25','game_id':'0022100046','home':'TOR','away':'CHI','source_calendar':'simulation/CHICAGO_2021_22_CALENDAR.csv','original_score_and_OT_not_selected_as_alternate_result':True},'Target source meaning changed')
def expected_positions(path,state):
 require(path in BASE and state in STATES,'Unknown capacity path/state')
 bs=[]
 for i,row in enumerate(BASE[path]):
  p={s:ALIASES[n] for s,n in zip(POS,row)}
  if state=='SIAKAM_UNAVAILABLE' and p['PF']=='Pascal Siakam':p['PF']='Chris Boucher' if i%2==0 and p['C']!='Chris Boucher' else 'Yuta Watanabe'
  bs.append(p)
 return bs

def construct(path,state,b):
 bs=expected_positions(path,state);counts=Counter();positions={p:Counter() for p in POS};blocks=[]
 for i,p in enumerate(bs):
  for pos,n in p.items():counts[n]+=240;positions[pos][n]+=240
  blocks.append({'index':i,'start_second':240*i,'end_second':240*(i+1),'seconds':240,'positions':p,'primary_creator':p['PG']})
 standard=b['operating_paths'][path]['standard'];absent=['Pascal Siakam'] if state=='SIAKAM_UNAVAILABLE' else []
 active=[n for n in standard if n in counts];active += [n for n in standard if n not in active and n not in absent][:12-len(active)]
 inactive=[n for n in standard if n not in active]
 positive=sorted(counts)
 return {'path':path,'availability_parameter':state,'function_id':'TOR_NAMED_ROSTER_CAPACITY_CONDITIONAL_FAMILY','source_target_key':deepcopy(b['target']),'selected_for_source_date':False,'standard':deepcopy(standard),'two_way':deepcopy(TW),'active':active,'inactive':inactive,'two_way_not_on_active_or_inactive_list':deepcopy(TW),'TW_active_regular_game_usage_in_this_capacity':0,'working_positive_available':positive,'working_active_nomination_eligible':active,'working_absent_condition':absent,'reserve_zero_clinical_status':{n:None for n in standard+TW if n not in counts},'actual_medical_status':{n:None for n in standard+TW},'starters':list(bs[0].values()),'blocks':blocks,'player_seconds':dict(sorted(counts.items())),'position_seconds':{p:dict(sorted(v.items())) for p,v in positions.items()},'total_team_seconds':14400,'elapsed_seconds':2880,'score':None,'winner':None,'overtime_adopted':False,'actual_registration_certified':False,'source_bank_path':BANK,'source_bank_pointer':'operating_paths.'+path,'required_legal_and_economic_inputs':deepcopy(b['operating_paths'][path]['required_actions']),'whole_cost_certified':False}

def assert_row(a,b):
 path=a['path'];state=a['availability_parameter'];require(path in PATH_NAMES and state in STATES,'Unknown row keys')
 require(a['standard']==PATH_NAMES[path] and a['two_way']==TW,'Membership/class changed')
 require(len(a['standard'])==len(set(a['standard']))==15 and len(a['two_way'])==2 and not set(a['standard'])&set(a['two_way']),'15STD2TW count violation')
 expect=expected_positions(path,state);counts=Counter();pos={p:Counter() for p in POS}
 require(len(a['blocks'])==12,'Chronological block domain changed')
 for i,(z,e) in enumerate(zip(a['blocks'],expect)):
  require((z['index'],z['start_second'],z['end_second'],z['seconds'])==(i,i*240,(i+1)*240,240),'Integer clock changed')
  require(z['positions']==e,'Source-modeled role choice changed')
  require(set(z['positions'])==set(POS) and len(set(z['positions'].values()))==5,'Duplicate five-player lineup')
  require(z['primary_creator']==e['PG'] and z['primary_creator'] in CREATORS,'Creator missing/relabeled')
  for p,n in e.items():require(n in ELIGIBILITY[p] and n in a['active'],'Position/registered active eligibility');counts[n]+=240;pos[p][n]+=240
 require(a['player_seconds']==dict(sorted(counts.items())) and a['position_seconds']=={p:dict(sorted(v.items())) for p,v in pos.items()},'Same-total redistribution or position ledger changed')
 require(sum(counts.values())==14400 and all(sum(v.values())==2880 for v in pos.values()) and max(counts.values())<=2880,'Team/player clock capacity')
 expected_absent=['Pascal Siakam'] if state=='SIAKAM_UNAVAILABLE' else []
 require(a['working_absent_condition']==expected_absent and not set(counts)&set(expected_absent),'Unavailable player used')
 active=[n for n in PATH_NAMES[path] if n in counts];active += [n for n in PATH_NAMES[path] if n not in active and n not in expected_absent][:12-len(active)]
 require(a['active']==active and a['inactive']==[n for n in PATH_NAMES[path] if n not in active] and len(active)==12 and len(a['inactive'])==3,'Active/inactive nomination changed')
 require(a['working_positive_available']==sorted(counts) and a['working_active_nomination_eligible']==active,'Availability role projection changed')
 require(a['two_way_not_on_active_or_inactive_list']==TW and a['TW_active_regular_game_usage_in_this_capacity']==0,'TW not independently nominated')
 require(a['actual_medical_status']=={n:None for n in PATH_NAMES[path]+TW} and a['reserve_zero_clinical_status']=={n:None for n in PATH_NAMES[path]+TW if n not in counts},'Medical inferred from positive/zero capacity')
 require(a['starters']==list(expect[0].values()),'Starting five changed')
 require(a['required_legal_and_economic_inputs']==b['operating_paths'][path]['required_actions'],'Legal/economic conditions omitted')
 require(a['source_target_key']==b['target'] and not a['selected_for_source_date'] and a['score'] is None and a['winner'] is None and not a['overtime_adopted'] and not a['actual_registration_certified'] and not a['whole_cost_certified'],'Date/result/legal authority promoted')
 require(a['total_team_seconds']==14400 and a['elapsed_seconds']==2880,'Reported clock differs from five-player capacity')
 require(a['function_id']=='TOR_NAMED_ROSTER_CAPACITY_CONDITIONAL_FAMILY' and a['source_bank_path']==BANK and a['source_bank_pointer']=='operating_paths.'+path,'Function/source path changed')

PRIMARY=[{'id':'SIAKAM_SURGERY','url':'https://www.nba.com/news/raptors-pascal-siakam-undergoes-shoulder-surgery','date':'2021-06-11','classification':'OFFICIAL_RELEASE_DIRECT_WEB_BODY_PROVIDER_RAW_NOT_RECOVERED','locator':'body lines174–175','paraphrase':'May8 contact injury preceded shoulder surgery; projected rehabilitation about five months.','changed_contact_automatically_preserved':False,'raw_sha256':None},{'id':'GIDDEY_ROLE','url':'https://www.nba.com/draft/2021/prospects/josh-giddey','classification':'NBA_PRIMARY_SCOUTING_DIRECT_WEB_BODY','locator':'About Josh Giddey introductory and facilitator paragraphs','paraphrase':'Guard/point-forward with passing instincts; shooting and physical strength remain developmental.','actual_TOR_number8_or_minute_plan_supported':False,'raw_sha256':None},{'id':'POWELL_ROLE','url':'https://www.nba.com/news/report-raptors-trade-norman-powell-to-blazers','date':'2021-03-25','classification':'NBA_HOSTED_AP_INDEXED_BODY_SECONDARY_ROLE_REPORT','paraphrase':'Identifies Powell as a shooting guard.','original_trade_applied_to_changed_world':False,'raw_sha256':None}]

def build(root=ROOT):
 b=load(root);assert_bank(b,root)
 rows=[]
 for p in PATH_NAMES:
  for s in STATES:
   a=construct(p,s,b);assert_row(a,b);rows.append(a)
 return {'id':'TOR_NAMED_ROSTER_CAPACITY_CONDITIONAL_FAMILY','schema':1,'status':'REVIEW_PENDING_FINITE_FOUR_CAPACITIES_NOT_DATED_EXECUTION','source_sha256':{BANK:sha(root/BANK),SELF:sha(root/SELF)},'hash_convention':'SHA256_UTF8_BOM_STRIPPED_CRLF_CR_TO_LF','bank_ancestor_pins_checked_not_full_ancestors_reaudited':b['source_sha256'],'rows':rows,'position_eligibility_design_only':ELIGIBILITY,'creator_design_only':CREATORS,'primary_role_health_observations':PRIMARY,'source_failure':[{'url':'https://statsdmz.nba.com/pdfs/20210110/20210110_TORGSW_book.pdf','attempts':1,'bounded_seconds':20,'result':'READ_TIMEOUT_BODY_NOT_RECOVERED','retry':0,'role_used_as_actual_body':False}],'health_scope':{'positive_minutes_are_conditional_working_availability':True,'active_zero_nominees_eligible_not_clinical_certificate':True,'SIAKAM_UNAVAILABLE_is_conservative_capacity_parameter_not_fact_adoption':True,'SIAKAM_AVAILABLE_is_alternate_capacity_parameter_not_cure_fact':True,'historical_May8_MEM_contact_injury_copied':False,'all_remaining_TOR_season_availability_selected':False},'summary':{'conditional_paths':2,'availability_parameters_each':2,'rows':4,'blocks':48,'five_player_cells':240,'each_elapsed_seconds':2880,'each_team_seconds':14400,'new_full_TOR_function_created':1,'prior_missing_team_ports':27,'prospective_missing_after_independent_acceptance_and_dispatcher_integration':26,'central_dispatcher_updated_here':False},'authority':{k:False for k in ['Lowry_direction_selected','contract_price_selected','exact_contract_consents_certified','whole_TOR_cost_certified','dated_membership_execution_selected','actual_medical_certified','whole_2021_22_results_selected','actual_tactical_success_certified','macro3_complete','REGISTER_promoted','independent_review_completed','manuscript_allowed']},'freeze':'v0.30 PARTIAL / CLOSED'}

def validate(a,root=ROOT):
 errors=[]
 try:
  b=load(root);assert_bank(b,root)
  require([(r['path'],r['availability_parameter']) for r in a['rows']]==[(p,s) for p in PATH_NAMES for s in STATES],'Four-state domain changed')
  for r in a['rows']:assert_row(r,b)
  require(a==build(root),'Source-bound artifact differs')
 except (ValueError,KeyError,TypeError) as e:errors.append(str(e))
 return errors

def markdown(a):
 out=['# Toronto 명명 조건부 정규 capacity 함수','',a['status'],'','T0/T1의 중요한 Lowry 경로·계약가격은 미선택이며 두 경로의 Siakam 가용/비가용을 각각 조건부 입력으로 받는다. 양수 선수의 이 경기 작업 가용을 구성하되 실제 임상/전체 시즌 건강으로 읽지 않는다.','', '| 경로 | 가용 조건 | 양수 인원 | 명목 active/inactive | 팀분 |','|---|---|---:|---|---:|']
 for r in a['rows']:out.append(f"| {r['path']} | {r['availability_parameter']} | {len(r['player_seconds'])} | 12/3 STD + TW 미호명 | 240 |")
 out += ['', '## 선택한 국소 코칭 방법','', '12개의 240초 창을 순서대로 배열한다. PG/SG/SF/PF/C는 이 모델의 역할 배정이며 NBA 공식 포지션 인증이 아니다. 창마다 다섯 명·creator 한 명을 포함하고 각 역할48분/선수≤48분을 보존한다. T0는 Lowry/Fred/Giddey, T1은 Fred/Dragic/Giddey가 주 생성자다. Powell은 유지된 가드 득점 역할이며, Siakam 비가용일 때 Boucher/Yuta의 PF 몫으로 재배정한다. 새로운 기술 성공/효율/득점/승패는 없다.','', '12명 작업 active는 양수 인원 전부+명단순 0분 filler로 구성하며 3명 standard inactive와 완전 분할한다. TW 두 명은 NBA active/inactive 어느 쪽에도 올리지 않고 이 함수의 regular active 사용0을 기록한다. 0분·inactive의 의료 상태는 null. TW를 새로 투입하려면 독립 명목 호명·50경기 누적·XXIX inactive조정을 다시 적용해야 한다.','', '## 역사와 가상 선택 경계','', '[Siakam 공식 발표](https://www.nba.com/news/raptors-pascal-siakam-undergoes-shoulder-surgery)는 접촉 기원의 수술/회복 전망만 지지한다. 가용 두 값은 수정 세계의 조건부 입력이며 원접촉·수술·개막 결장을 자동 복사하지 않는다. [Giddey 공식 프로필](https://www.nba.com/draft/2021/prospects/josh-giddey)의 역할은 분배자 배정 근거이고 #8 TOR·성공을 지지하지 않는다. Powell의 가드 분류는 NBA에 실린 AP 보도 검색 관측이며 실제 원거래는 적용하지 않는다. 다른 세부 역할/분은 명명된 일상 가상 코칭 설계다. TORGSW gamebook 직접20초 시도1회 timeout/본문0/재시도0를 실패로 기록한다.','', '## 입력과 미완료','', '동결 이름은행의 T0/T1 정확15STD2TW·DB1·Bonga0YOS·법적 수단 목록을 source-bound caller에서 대조한다. 살아 있는 은행의 양도/서명/방출 조건과 전체비용HOLD는 그대로다. 가용 모형이 법적 계약을 대신하지 않는다. target0022100046/10-25는 원일정 참조키이며 해당 날짜의 거래/임상/실제 출장 또는 결과를 선택하지 않는다. 2020–21분 이월0·OT 자동이월0.','', '함수 API `TOR_NAMED_ROSTER_CAPACITY_CONDITIONAL_FAMILY(path, availability_parameter, root)`는 하나의 source-bound 국소 row를 반환한다. 27missing→26missing은 독립수용/공통dispatcher 통합 뒤의 예상 감소이며 이번 파일이 중앙 dispatcher를 변경하지 않는다. 전체 전시즌 적용도 미완료다.','', '## 진행표','', '| 묶음 | 상태 |','|---|---|','| 1 | 완료 |','| 2 | S2 완료 |','| 3 | TOR 조건부 함수1 신규·경제/중요 경로 미선택 |','| 4 | 선행 결과 의존 |','| 5 | 전체 미완료 |','| 6 | Pack0·미완료 |','| 7 | 최종 미완료 |','','미완료5 / 6번까지4. PARTIAL/CLOSED·원고0.']
 return '\n'.join(out)+'\n'

def TOR_NAMED_ROSTER_CAPACITY_CONDITIONAL_FAMILY(path,availability_parameter,root=ROOT):
 b=load(root);assert_bank(b,root);a=construct(path,availability_parameter,b);assert_row(a,b);return a

def self_test(root=ROOT):
 a=build(root);tests=[]
 def rejected(label,fn):
  x=deepcopy(a);fn(x);require(bool(validate(x,root)),'Negative falsely accepted:'+label);tests.append(label)
 rejected('same_total_player_redistribution',lambda x:x['rows'][0]['player_seconds'].update({'Norman Powell':x['rows'][0]['player_seconds']['Norman Powell']+1,'OG Anunoby':x['rows'][0]['player_seconds']['OG Anunoby']-1}))
 rejected('unavailable_Siakam_positive',lambda x:x['rows'][1]['blocks'][0]['positions'].update(PF='Pascal Siakam'))
 rejected('clinical_zero_certificate',lambda x:x['rows'][0]['reserve_zero_clinical_status'].update({'Sam Hauser':'CLEARED'}))
 rejected('Lowry_direction_promoted',lambda x:x['authority'].update(Lowry_direction_selected=True))
 rejected('TW_as_STANDARD',lambda x:x['rows'][0]['standard'].__setitem__(0,'Sam Hauser'))
 rejected('clock_241seconds',lambda x:x['rows'][0]['blocks'][0].update(seconds=241))
 real=construct
 def badconstruct(p,s,b):
  x=real(p,s,b);x['blocks'][0]['primary_creator']='Khem Birch';return x
 with patch(__name__+'.construct',side_effect=badconstruct):
  try:build(root)
  except ValueError:tests.append('constructor_creator_relabel')
  else:raise ValueError('Bad constructor accepted')
 real_load=load;bank=real_load(root);bank['operating_paths']['T1']['standard'][-1]='Scottie Barnes'
 with patch(__name__+'.load',return_value=bank):
  try:build(root)
  except ValueError:tests.append('source_same_count_Bonga_to_Barnes')
  else:raise ValueError('Bad source reader accepted')
 return tests

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');v=p.parse_args();a=build()
 if v.write:(ROOT/OUT).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(a),encoding='utf-8')
 if v.check:
  e=validate(json.loads((ROOT/OUT).read_text(encoding='utf-8-sig')));require(not e,';'.join(e));require((ROOT/MD).read_text(encoding='utf-8-sig').replace('\r\n','\n')==markdown(a),'MD stale')
 tests=self_test() if v.self_test else []
 print(json.dumps({'current':True,'rows':4,'blocks':48,'cells':240,'controls':tests},ensure_ascii=False))
if __name__=='__main__':main()
