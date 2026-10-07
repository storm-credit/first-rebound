"""One new FY23 bracket, explicit fictional chronology and selected outcomes.

Reads physical selected inputs only; never invokes ancestor constructors.
"""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from datetime import date,timedelta
from fractions import Fraction
from unittest.mock import patch
from bs4 import BeautifulSoup
import argparse,hashlib,json

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2023_selected_full_postseason.py'
OUT='simulation/NBA_2023_SELECTED_FULL_POSTSEASON.json';MD=OUT[:-5]+'.md'
BASELINE='241821ba24936ee788320844822af5a3f32ef69c'
SEED='simulation/NBA_2022_23_STANDINGS_AND_2023_PLAYIN.json'
GLOBAL='simulation/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS.json'
H22='simulation/CHICAGO_2022_23_SELECTED_DATED_ROLES.json'
CORE='canon/DELEGATED_2022_23_NPC_CORE_CONTRACT_EXECUTION_2026_10_08.json'
AUTH='canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
SCOPE='control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md'
CAREER='design/CHICAGO_MINNESOTA_LONG_CAREER_PACKET.md'
FILES=(SEED,GLOBAL,H22,CORE,AUTH,SCOPE,CAREER)
PINS={'simulation/NBA_2022_23_STANDINGS_AND_2023_PLAYIN.json': 'cecefbc4fbca8378cacdae2f77129f26644244529d11eb216072a8fba8d224a9', 'simulation/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS.json': '8e2a778fe646de3c6070be7dd3acc64199fe2a7c813e780916e380b099fa3889', 'simulation/CHICAGO_2022_23_SELECTED_DATED_ROLES.json': 'c0650dbb07b75cc1523bf7ccc7f658576ac5b9a8784f1e80cc97178897703170', 'canon/DELEGATED_2022_23_NPC_CORE_CONTRACT_EXECUTION_2026_10_08.json': '0b03b3c9afa279b9537af21da44f70565407a284832dce71aeeb333489433da5', 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json': '4ee9b74e37903a43b0bd50b35c7f24cbabdac13728097a848b553f874bbeef80', 'control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md': '91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d', 'design/CHICAGO_MINNESOTA_LONG_CAREER_PACKET.md': 'ec551b2f4700d9db4daca9885abdca123894c6841daadc0cb354c64baceac25b'}
CAPTURE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-2023-postseason-20261008')
PRIMARY_METADATA={'sources.json': '1757d3ee0b2ae88aad8a68ff75f1086aa297642f4a3389859046abe209aabff7', 'extra_sources.json': '42e6069cd62cf5e9c7732b74d13137d2f938424f06a5d7bdebc4d29b1c35ab6b'}
STARTS={'R1':'2023-04-15','R2':'2023-04-30','CF':'2023-05-15','F':'2023-06-01'}
OFFSETS={'R1':[0,2,4,6,8,10,12],'R2':[0,2,4,6,8,10,12],
 'CF':[0,2,4,6,8,10,12],'F':[0,2,5,7,10,12,15]}
HOME_PATTERN=[0,0,1,1,0,1,0]
POLICY={'selection':'ROOT_EXPLICIT_EXISTING_SEASON_DELEGATION_2023_FULL_POSTSEASON',
 'selected_new_calendar_and_same_UPC_Gamma_roles_until':'2023-06-16',
 'legal_salary_year':'2022-23','new_prices_transactions_waivers_TW_activation_selected':False,
 'same_H22_NORMAL_240_and_first_rookie_roles_preserved':True,
 'all_source_Chet_OUT_Miles_no_UPC_obligations_preserved':True,
 'postseason_0OT_is_new_fiction_not_observed_box':True,
 'Fraction_March25_EB_zero_growth_home2_no_B2B':True,
 'H2_2023_R2_target_is_revisable_recommendation_not_locked_result':True,
 'new_protagonist_title_MVP_or_franchise_change_selected':False,
 'actual_private_medical_contract_or_receipts_certified':False}
FIXED=deepcopy(POLICY)
def need(x,m):
 if not x:raise AssertionError(m)
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(root,p):return json.loads(text(root/p)) if p.endswith('.json') else text(root/p)
def sources(root):
 need(POLICY==FIXED,'Selected FY23 postseason scope changed')
 s={}
 for p in FILES:
  need(sha(root/p)==PINS[p],'Physical postseason source stale '+p)
  v=load(root,p);actual=json.loads(text(root/p)) if p.endswith('.json') else text(root/p)
  need(v==actual,'Returned postseason source differs from independent physical parse '+p);s[p]=v
 need(s[SEED]['summary']['playoff_qualifiers']==16 and s[SEED]['Chicago_first_PO']['opponent']=='MIL','Current first PO source')
 need(s[SEED]['source_sha256'][GLOBAL]==PINS[GLOBAL] and s[SEED]['source_sha256'][CORE]==PINS[CORE],'Current source graph binding')
 need(s[GLOBAL]['summary']['CHI_wins']==46 and s[GLOBAL]['summary']['unique_named_owners']==450,'Current FY23 regular source')
 need('계산했을 때 성립하지 않으면 해당 목표를 수정한다' in s[CAREER],'Career recommendation scope changed')
 return s
def primary():
 allmeta=[];bodies={}
 for name,h in PRIMARY_METADATA.items():
  p=CAPTURE/name;need(hashlib.sha256(p.read_bytes()).hexdigest()==h,'Primary capture metadata changed')
  v=json.loads(text(p));allmeta.extend(v if isinstance(v,list) else [v])
 for r in allmeta:
  b=Path(r['cache_path']).read_bytes();need(r['HTTP_status']==200 and hashlib.sha256(b).hexdigest()==r['raw_sha256'],'Primary raw changed')
  soup=BeautifulSoup(b,'html.parser')
  for e in soup(['script','style']):e.decompose()
  bodies[r.get('id','schedule')]=soup.get_text(' ',strip=True)
 need('home-court advantage' in bodies['homecourt'] and 'Head-to-head' in bodies['homecourt'],'Home-court source missing')
 need('2-2-1-1-1' in bodies['format'] and 'extra day between Games 6 and 7' in bodies['format'],'Finals format source missing')
 need('June 12th, 2023' in bodies['lastgame'],'Original last Finals date source missing')
 return {'raw_sources':allmeta,'original_NBA_last_Finals':'2023-06-12',
  'original_NBA_last_Finals_is_not_a_deadline_for_new_fiction':True,
  'original_actor_score_winner_champion_not_consumed':True,
  'format':'BEST_OF_SEVEN_FIRST_TO_FOUR_2_2_1_1_1',
  'home_court_rule_support':'NBA2015 PR seeding/home-court H2H then division; first-four continuation from independently-read official2017 tie PDF in seed input',
  'fictional_round_starts':deepcopy(STARTS),'fictional_game_offsets':deepcopy(OFFSETS)}
def template(team,s):
 v=deepcopy(s[GLOBAL]['shared_team_templates'][team]);owners={(x['team'],x['player']):x['registration'] for x in s[GLOBAL]['owner_catalog']}
 need(all(owners.get((team,p))=='STANDARD' for p in v['standard']),'Named current standard owner')
 need(12<=len(v['active'])<=15 and set(v['active'])<=set(v['standard']) and not(set(v['active'])&set(v['TW'])),'Postseason STD nominations')
 end=0;sec=Counter();roles=Counter()
 for b in v['blocks']:
  need(b['start_second']==end and b['end_second']>end and b['end_second']<=2880 and end//720==(b['end_second']-1)//720,'Postseason quarter clock')
  need(set(b['positions'])=={'PG','SG','SF','PF','C'} and len(set(b['positions'].values()))==5,'Selected 5 positions')
  for pos,p in b['positions'].items():need(p in v['active'],'Nonactive positive');sec[p]+=b['end_second']-end;roles[pos]+=b['end_second']-end
  end=b['end_second']
 need(end==2880 and dict(sec)==v['positive_player_seconds'] and sum(sec.values())==14400 and set(roles.values())=={2880},'48/240 positive source budget')
 if team=='CHI':need(v['blocks']==[{k:deepcopy(b[k]) for k in ('start_second','end_second','positions')} for b in s[H22]['selected_role_template']['ordered_regulation_blocks']],'H22 NORMAL exact source')
 v['new_postseason_interval']=['2023-04-15','2023-06-16'];v['all_UPC_and_original_full_Gamma_preserved']=True;v['actual_receipt_certified']=False
 return v
def ratio(t,opponents,g):
 rs=[r for r in g['rows'] if t in (r['home'],r['away']) and (r['away'] if r['home']==t else r['home']) in opponents]
 need(rs,'Home-court ratio zero games');return Fraction(sum(r['winner']==t for r in rs),len(rs))
def higher(a,b,conf,s):
 seed=s[SEED];g=s[GLOBAL]
 if conf!='NBA':
  order={x['team']:x['seed'] for x in seed['final_playoff_seeds'][conf]}
  return ((a,b) if order[a]<order[b] else (b,a)),{'criterion':'SELECTED_CONFERENCE_SEED','values':{a:order[a],b:order[b]}}
 trace=[]
 values={t:Fraction(g['team_records'][t]['wins'],82) for t in (a,b)}
 trace.append({'criterion':'regular_record','values':{t:str(v) for t,v in values.items()}})
 if values[a]==values[b]:
  confmap={x['team']:c for c,rs in seed['conference_seeds'].items() for x in rs}
  for c in ('head_to_head','division_winner','conference_record'):
   values={t:ratio(t,{b if t==a else a},g) if c=='head_to_head' else Fraction(int(t in seed['division_winners'])) if c=='division_winner' else
    ratio(t,{u for u in confmap if confmap[u]==confmap[t]}-{t},g) for t in (a,b)}
   trace.append({'criterion':c,'values':{t:str(v) for t,v in values.items()}})
   if values[a]!=values[b]:break
 need(values[a]!=values[b],'Finals equal home-court needs named later criterion')
 return ((a,b) if values[a]>values[b] else (b,a)),{'criteria_trace':trace,'source_rule_is_not_arbitrary_team_name_order':True}
def game(sid,number,day,home,away,templates,s):
 views={t:templates[t] for t in (home,away)};impacts={t:sum(Fraction(s[GLOBAL]['selected_productivity_inputs'][p]['fraction'])*n for p,n in v['positive_player_seconds'].items())/2880 for t,v in views.items()}
 m=impacts[home]-impacts[away]+2;need(m!=0,'New exact result tie')
 ends=sorted({0,720,1440,2160,2880}|{b['end_second'] for v in views.values() for b in v['blocks']})
 segments=[{'start_second':a,'end_second':b,'quarter':a//720+1,
  'positions':{t:deepcopy(next(q['positions'] for q in v['blocks'] if q['start_second']<=a<q['end_second'])) for t,v in views.items()}} for a,b in zip(ends,ends[1:])]
 return {'id':sid+':G'+str(number),'game_number':number,'date':day,'home':home,'away':away,
  'simultaneous_segments':segments,'exact_impacts':{t:str(v) for t,v in impacts.items()},'home_margin':str(m),
  'selected_winner':home if m>0 else away,'selected_loser':away if m>0 else home,
  'home_effect':'2','b2b_fatigue':'0','selected_OT_periods':0,'score':None,'actual_NBA_game_id':None,'actual_receipt_certified':False}
def assert_game(v,sid,n,day,h,a,s):
 need((v['id'],v['game_number'],v['date'],v['home'],v['away'])==(sid+':G'+str(n),n,day,h,a),'Returned postseason date/actor changed')
 impact={t:sum(Fraction(s[GLOBAL]['selected_productivity_inputs'][p]['fraction'])*sec for p,sec in s[GLOBAL]['shared_team_templates'][t]['positive_player_seconds'].items())/2880 for t in (h,a)}
 m=impact[h]-impact[a]+2
 need(v['exact_impacts']=={t:str(q) for t,q in impact.items()} and v['home_margin']==str(m) and (v['selected_winner'],v['selected_loser'])==((h,a) if m>0 else (a,h)),'Returned new postseason outcome arithmetic')
 need(v['home_effect']=='2' and v['b2b_fatigue']=='0' and v['selected_OT_periods']==0 and v['score'] is None and v['actual_NBA_game_id'] is None and v['actual_receipt_certified'] is False,'Returned actual/OT/score scope')
 endpoints=sorted({0,720,1440,2160,2880}|{b['end_second'] for t in (h,a) for b in s[GLOBAL]['shared_team_templates'][t]['blocks']})
 need(len(v['simultaneous_segments'])==len(endpoints)-1,'Returned simultaneous segments')
 seconds={t:Counter() for t in (h,a)}
 for q,start,end in zip(v['simultaneous_segments'],endpoints,endpoints[1:]):
  ps={t:next(b['positions'] for b in s[GLOBAL]['shared_team_templates'][t]['blocks'] if b['start_second']<=start<b['end_second']) for t in (h,a)}
  need(q=={'start_second':start,'end_second':end,'quarter':start//720+1,'positions':ps},'Returned ordered source role/quarter changed')
  for t,p in ps.items():
   for name in p.values():seconds[t][name]+=end-start
 need(all(dict(seconds[t])==s[GLOBAL]['shared_team_templates'][t]['positive_player_seconds'] for t in seconds),'Returned simultaneous positive budgets')
def series(sid,conf,rnd,a,b,deps,templates,s):
 (hi,lo),basis=higher(a,b,conf,s);wins=Counter();games=[]
 for n,offset in enumerate(OFFSETS[rnd],1):
  if max(wins.values(),default=0)==4:break
  h,aw=(hi,lo) if HOME_PATTERN[n-1]==0 else (lo,hi);day=(date.fromisoformat(STARTS[rnd])+timedelta(days=offset)).isoformat()
  q=game(sid,n,day,h,aw,templates,s);wins[q['selected_winner']]+=1;games.append(q)
 return {'id':sid,'conference':conf,'round':rnd,'teams':[a,b],'source_dependencies':deps,
  'higher_home':hi,'home_basis':basis,'games':games,'wins':{t:wins[t] for t in (a,b)},'selected_winner':max(wins,key=wins.get),
  'selection_class':'ROOT_DELEGATED_WORKING_POSTSEASON_RESULT','actual_title_or_receipt_certified':False}
def assert_series(v,sid,conf,rnd,a,b,deps,s):
 need((v['id'],v['conference'],v['round'],v['teams'],v['source_dependencies'])==(sid,conf,rnd,[a,b],deps),'Returned bracket/source dependency')
 (hi,lo),basis=higher(a,b,conf,s);need(v['higher_home']==hi and v['home_basis']==basis,'Returned home-court rule/source basis')
 counts=Counter();need(4<=len(v['games'])<=7,'Series count')
 for n,q in enumerate(v['games'],1):
  need(max(counts.values(),default=0)<4,'Game after clinch')
  h,aw=(hi,lo) if HOME_PATTERN[n-1]==0 else (lo,hi);day=(date.fromisoformat(STARTS[rnd])+timedelta(days=OFFSETS[rnd][n-1])).isoformat()
  assert_game(q,sid,n,day,h,aw,s);counts[q['selected_winner']]+=1
 need(max(counts.values())==4 and v['wins']=={t:counts[t] for t in (a,b)} and v['selected_winner']==max(counts,key=counts.get),'Returned series winner/count')
 need(v['selection_class']=='ROOT_DELEGATED_WORKING_POSTSEASON_RESULT' and v['actual_title_or_receipt_certified'] is False,'Returned institutional title promotion')
def build(root=ROOT):
 s=sources(root)
 for p in FILES:
  need(sha(root/p)==PINS[p],'Caller physical source stale '+p)
  actual=json.loads(text(root/p)) if p.endswith('.json') else text(root/p)
  need(s[p]==actual,'Returned consumed source differs from physical source '+p)
 obs=primary();qualified={x['team'] for rs in s[SEED]['final_playoff_seeds'].values() for x in rs}
 need(len(qualified)==16,'Qualified16')
 templates={t:template(t,s) for t in sorted(qualified)}
 for t,v in templates.items():
  original=s[GLOBAL]['shared_team_templates'][t];expected={**deepcopy(original),'new_postseason_interval':['2023-04-15','2023-06-16'],
   'all_UPC_and_original_full_Gamma_preserved':True,'actual_receipt_certified':False}
  need(v==expected,'Returned FY23 template differs from source role/Gamma')
 records=[];byid={}
 def add(c,rnd,a,b,i,deps):
  sid=f'ALT2023:{c}:{rnd}:{i}';v=series(sid,c,rnd,a,b,deps,templates,s);assert_series(v,sid,c,rnd,a,b,deps,s)
  for d in deps:need(byid[d]['games'][-1]['date']<v['games'][0]['date'],'Downstream round before predecessor end')
  records.append(v);byid[sid]=v;return v
 cf={}
 for c,rs in s[SEED]['final_playoff_seeds'].items():
  ts={x['seed']:x['team'] for x in rs};need(set(ts)==set(range(1,9)),'Current selected seed domain')
  first=[add(c,'R1',ts[a],ts[b],i,[]) for i,(a,b) in enumerate([(1,8),(4,5),(2,7),(3,6)],1)]
  for v in first:
   src=next(x for x in s[SEED]['first_round_bracket'] if x['conference']==c and x['home_court_team']==v['higher_home'])
   need(set(v['teams'])=={src['home_court_team'],src['away_team']},'First bracket source mismatch')
  second=[add(c,'R2',first[a]['selected_winner'],first[b]['selected_winner'],i,[first[a]['id'],first[b]['id']]) for i,(a,b) in enumerate([(0,1),(2,3)],1)]
  cf[c]=add(c,'CF',second[0]['selected_winner'],second[1]['selected_winner'],1,[x['id'] for x in second])
 final=add('NBA','F',cf['EAST']['selected_winner'],cf['WEST']['selected_winner'],1,[cf['EAST']['id'],cf['WEST']['id']])
 seen=set();latest={};gamecount=0
 for v in records:
  for q in v['games']:
   gamecount+=1
   for t in (q['home'],q['away']):
    need((t,q['date']) not in seen,'Two games same team/date');seen.add((t,q['date']))
    if t in latest:need((date.fromisoformat(q['date'])-date.fromisoformat(latest[t])).days>=2,'Postseason B2B not in selected model')
    latest[t]=q['date']
 need(len(records)==15 and final['games'][-1]['date']<='2023-06-16','Full fifteen-series calendar range')
 chi=next(v for v in records if 'CHI' in v['teams']);need(chi['selected_winner']!='CHI','Model changes protagonist title path: root consequential review required')
 return {'id':'NBA_2023_SELECTED_FULL_POSTSEASON','baseline_main':BASELINE,'status':'SELECTED_FIFTEEN_SERIES_WORKING_POSTSEASON_INDEPENDENT_REVIEW_PENDING',
  'source_sha256':{**PINS,SELF:sha(root/SELF)},'selected_policy':deepcopy(POLICY),'primary_provenance':obs,
  'qualified_seeds':deepcopy(s[SEED]['final_playoff_seeds']),'postseason_team_templates':templates,
  'selected_core_price_family_preserved':deepcopy(s[CORE]['selected_core_execution']),
  'series':records,'selected_champion':final['selected_winner'],'selected_runner_up':next(t for t in final['teams'] if t!=final['selected_winner']),
  'selected_last_Finals_date':final['games'][-1]['date'],
  'Chicago_postseason':{'opponent':'MIL','round':'R1','wins':chi['wins'],'last_game':chi['games'][-1]['date'],
   'H2_recommended_R2_not_preserved_as_fake_result':True,'protagonist_titlecount_increased':False,'MVP_selected':False,'core_or_franchise_changed':False},
  'summary':{'qualified_teams':16,'series':15,'selected_games':gamecount,'selected_team_dates':len(seen),
   'simultaneous_segments':sum(len(q['simultaneous_segments']) for v in records for q in v['games']),
   'each_team_regulation_seconds':2880,'each_team_player_seconds':14400,'calendar_conflicts':0,
   'source_regular_playin_records_changed':False,'historical_NBA_winners_copied':0},
  'certification':{'fifteen_series_working_results_selected':True,'independent_review_completed':False,
   'root_delegated_season_authority_applied':True,'new_human_author_lock':False,
   'actual_contract_clinical_title_private_receipts_certified':False,'whole_team_six_cost_certified':False,
   'protagonist_title_MVP_or_ending_changed':False,'2023_draft_control_selected':False,'whole_macro3_complete':False},
  'remaining_finite_inputs':['2023 final season-end join to QO/extension/options and first/second origin-right-control consumers.',
   'Future NBA roster/career butterfly effects remain separate; no automatic historical Utah rebuild or NPC transaction import.'],
  'model_limit':'Conservative fixed priors/zero-growth/no-variance/0OT proxy; working fiction, not historical standings, calibrated likelihood or actual medical proof.',
  'unfinished_macro_groups':5,'unfinished_through_6':4,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0,'manuscript_allowed':False}
def render(v):
 lines=['# 2023 전체 포스트시즌 · 선택 작업결과','',
  '새2023 플레이인 대진에서15시리즈를4승까지 계산했다. 같은FY23 NORMAL 역할·양팀48/240·STANDARD명명 등록·원Γ/가격을 새가상일정 말단까지 보존한다. TW기용·새이적·가격변경·원NBA승자복사0이다.','',
  '[NBA 발표 Finals 형식](https://pr.nba.com/nba-finals-format-change-2014/)의2-2-1-1-1과 [동률 홈코트 발표](https://pr.nba.com/nba-playoff-seeding-changes/)를 연결한다. 가상 일자별 간격은 별도선택이며 원NBA실제 캘린더를 사칭하지 않는다.','',
  '| 시리즈 | 대진 | 선택 승자 | 승수 | 말단 |','|---|---|---|---|---|']
 lines += [f"| {r['id']} | {'–'.join(r['teams'])} | {r['selected_winner']} | {r['wins']} | {r['games'][-1]['date']} |" for r in v['series']]
 lines+=['',f"가상 선택 우승: **{v['selected_champion']}** / 준우승 {v['selected_runner_up']} / 말단 {v['selected_last_Finals_date']}. NPC시즌 파생모델 선택이며 주인공 우승수·MVP·코어·프랜차이즈 방향은 변경하지 않는다.",'',
  '[원NBA2023 마지막 Finals](https://www.nba.com/game/mia-vs-den-0042200405/box-score)는6/12 관측이고 이 모델의 종료시한이나 승자가 아니다. 신규모델 날짜는 원결과와 구분하며 당해 샐러리연도6/30 안이다.','',
  f"Chicago는 MIL 상대 R1 {v['Chicago_postseason']['wins']}·{v['Chicago_postseason']['last_game']} 종료. 기존H2의2023 R2 목표는 성립하지 않으면 수정하는 추천이므로 승자를 조작해 맞추지 않았다. 주인공 첫우승·장기승계·정확수상 선택은 추가하지 않는다.",'',
  '같은UPC/원보호급여·보너스·새core11 선택가격을 보존하되 전체개별구단 재정상단이나 실제계약/임상/접수를 인증하지 않는다. 신인기용·Chet OUT/Miles UPC0·CHI H22 NORMAL을 보존한다. 새NBA가상기록은 정규 QO 통계에 PO분을 더하지 않는다.','',
  '## 남은 유한 입력','']+['- '+x for x in v['remaining_finite_inputs']]
 lines+=['','[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','',
  '| 묶음 | 현황 |','|---|---|','| 1 | 완료 |','| 2 | 완료 |','| 3 | 진행 |','| 4 | 진행 |','| 5 | 대기 |','| 6 | 대기 |','| 7 | CLOSED |','',
  '미완료큰묶음5 · 6번까지4 · v0.30 PARTIAL · CLOSED · Pack0 · 원고0.']
 return '\n'.join(lines)+'\n'
def validate(v,root=ROOT):
 try:return [] if v==build(root) else ['Saved postseason differs from physical selected reconstruction']
 except (AssertionError,KeyError,ValueError) as e:return [str(e)]
def self_test():
 labels=[]
 def reject(label):
  try:build()
  except (AssertionError,KeyError,ValueError):labels.append(label);return
  raise AssertionError('FALSE_PASS '+label)
 orig=game
 def winner(*a):
  v=orig(*a);v['selected_winner']=v['selected_loser'];return v
 with patch(__name__+'.game',side_effect=winner):reject('returned_winner')
 def clock(*a):
  v=orig(*a);p=next(iter(v['simultaneous_segments'][0]['positions'].values()));p['PG'],p['SG']=p['SG'],p['PG'];return v
 with patch(__name__+'.game',side_effect=clock):reject('returned_ordered_role')
 original_load=load
 def seeded(root,p):
  v=original_load(root,p)
  if p==SEED:v['final_playoff_seeds']['EAST'][0]['team']='OKC'
  return v
 with patch(__name__+'.load',side_effect=seeded):reject('returned_source_qualified_owner')
 def actual(*a):
  v=orig(*a);v['actual_receipt_certified']=True;return v
 with patch(__name__+'.game',side_effect=actual):reject('returned_actual_receipt')
 original_sources=sources
 def gamma(root):
  v=original_sources(root);v[CORE]['selected_core_execution'][0]['verified_source_case']['all_original_Gamma_preserved']=False;return v
 with patch(__name__+'.sources',side_effect=gamma):reject('returned_core_Gamma')
 return labels
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(render(v),encoding='utf-8')
 r={'summary':v['summary'],'champion':v['selected_champion'],'Finals_end':v['selected_last_Finals_date'],'CHI':v['Chicago_postseason']}
 if a.check:need(not validate(json.loads(text(ROOT/OUT))),'Saved postseason stale');need(text(ROOT/MD)==render(v),'MD stale');r['current']=True
 if a.self_test:r['negative_controls']=self_test()
 print(json.dumps(r,ensure_ascii=False))
if __name__=='__main__':main()
