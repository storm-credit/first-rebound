"""New-year seeds and six selected play-ins, with unresolved low-seed ports.

No ancestor constructors, historical outcomes or inferred points are consumed.
"""
from pathlib import Path
from collections import Counter,defaultdict
from copy import deepcopy
from datetime import date,timedelta
from fractions import Fraction
from unittest.mock import patch
import argparse,hashlib,json,fitz
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_23_standings_and_2023_playin.py'
OUT='simulation/NBA_2022_23_STANDINGS_AND_2023_PLAYIN.json';MD=OUT[:-5]+'.md'
BASELINE='241821ba24936ee788320844822af5a3f32ef69c'
GLOBAL='simulation/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS.json'
PEER='reviews/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS_G11_INDEPENDENT_REVIEW_2026_10_08.json'
CORE='canon/DELEGATED_2022_23_NPC_CORE_CONTRACT_EXECUTION_2026_10_08.json'
H22='simulation/CHICAGO_2022_23_SELECTED_DATED_ROLES.json'
PORT='simulation/NBA_2022_23_NPC_CONTRACT_PORTFOLIO.json'
RSC='simulation/NBA_2022_NPC_FIRST_ROUND_RSC_SLOT_JOIN.json'
OVERLAY='simulation/NBA_2022_23_EXPLICIT_NPC_AVAILABILITY_OVERLAY.json'
PRICE='research/NBA_2022_23_NPC_CORE_RENEWAL_PRICE_FAMILY.json'
FILES=(GLOBAL,PEER,CORE,H22,PORT,RSC,OVERLAY,PRICE)
PINS={'simulation/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS.json': '8e2a778fe646de3c6070be7dd3acc64199fe2a7c813e780916e380b099fa3889', 'reviews/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS_G11_INDEPENDENT_REVIEW_2026_10_08.json': 'fb6d63d9788ad4a612e15094adb6b73d647105e2569c79a52337c62df1752502', 'canon/DELEGATED_2022_23_NPC_CORE_CONTRACT_EXECUTION_2026_10_08.json': '0b03b3c9afa279b9537af21da44f70565407a284832dce71aeeb333489433da5', 'simulation/CHICAGO_2022_23_SELECTED_DATED_ROLES.json': 'c0650dbb07b75cc1523bf7ccc7f658576ac5b9a8784f1e80cc97178897703170', 'simulation/NBA_2022_23_NPC_CONTRACT_PORTFOLIO.json': '123d07df572ac4350e9528b3f0b913b3013ad4d51584c88a94e78051b9c7af19', 'simulation/NBA_2022_NPC_FIRST_ROUND_RSC_SLOT_JOIN.json': '9e72b7b6f277d62a1462eae93548903278631a155698ec39fcfef82fae200933', 'simulation/NBA_2022_23_EXPLICIT_NPC_AVAILABILITY_OVERLAY.json': '3bcb132b62595cef8490933d462b2c841ab3737777877cb4e687c8c60412a80b', 'research/NBA_2022_23_NPC_CORE_RENEWAL_PRICE_FAMILY.json': '9e0a6be7d5efb13724f76adf5aee30cd6ab2b376f486d3b15a8bf6dcd1507a1d'}
CAPTURE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-2023-standings-20261008')
RAW_META_SHA='0680f3cf4a18eca56d451e2f39b63375558be8529c4a163bf12718c3a70f14ad'
DIVISIONS={'Atlantic':['BOS','BKN','NYK','PHI','TOR'],'Central':['CHI','CLE','DET','IND','MIL'],
 'Southeast':['ATL','CHA','MIA','ORL','WAS'],'Northwest':['DEN','MIN','OKC','POR','UTA'],
 'Pacific':['GSW','LAC','LAL','PHX','SAC'],'Southwest':['DAL','HOU','MEM','NOP','SAS']}
DIV={t:d for d,ts in DIVISIONS.items() for t in ts}
CONF={t:('EAST' if DIV[t] in ('Atlantic','Central','Southeast') else 'WEST') for t in DIV}
DATES={'78':'2023-04-11','910':'2023-04-12','FINAL':'2023-04-14','playoffs_begin':'2023-04-15'}
POLICY={'selected_new_same_UPC_all_Gamma_no_new_event_family_through':'2023-04-14',
 'salary_year':'2022-23','CHI_state':'NORMAL','all_positive_participants_registered_STANDARD':True,
 'all_original_and_selected_salary_bonus_protection_obligations_preserved':True,
 'new_rookie_RSC_and_development_preserved':True,'no_TW_postseason_activation':True,
 'same_source_quarter_clock_and_nominations_selected_as_new_postregular_fiction':True,
 'Chet_OUT_Miles_no_UPC_exceptions_preserved':True,
 'new_regular_0OT_proxy_continued_for_six_playins':True,
 'same_Fraction_BPM_EB_home2_B2Bhalf':True,
 'actual_private_contract_medical_or_receipts_certified':False,
 'new_title_MVP_author_lock':False,'historical_NBA_playin_results_copied':False,
 'real_points_from_BPM_margin_inferred':False}
FIXED_POLICY=deepcopy(POLICY)
RANK_MEANING='fb5850621553bffc8bdc6ec1728f7d81463a1b2aeca48abb9bb5f6c342f9c10f'

def need(x,m):
 if not x:raise AssertionError(m)
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def physical(root,p):return json.loads(text(root/p))
def sources(root):
 need(POLICY==FIXED_POLICY,'Selected continuation policy altered')
 s={}
 for p in FILES:
  need(sha(root/p)==PINS[p],'Physical source stale '+p)
  v=physical(root,p)
  need(v==json.loads(text(root/p)),'Returned physical source altered '+p)
  s[p]=v
 need(s[PEER]['independent_review_completed'] is True and s[PEER]['source_sha256'][GLOBAL]==PINS[GLOBAL],'Global independent scope changed')
 need(s[GLOBAL]['summary']['CHI_wins']==46 and s[GLOBAL]['summary']['CHI_losses']==36 and s[GLOBAL]['summary']['unique_named_owners']==450,'Current regular source domain')
 need(len(s[CORE]['selected_core_execution'])==11,'Named core11 family missing')
 for r in s[CORE]['selected_core_execution']:
  if r['player']=='Miles Bridges':need(r['new_UPC'] is False and r['retained_FA_QO_hold_and_original_obligations'] is True,'Miles rights/obligations erased')
  else:
   case=r['verified_source_case'];pointer=r['verified_source_case_pointer']
   need(pointer.startswith(PRICE+'#/endpoint_function_checks/'),'Core source case pointer changed')
   need(case==s[PRICE]['endpoint_function_checks'][int(pointer.rsplit('/',1)[1])] and case['player']==r['player'],'Core selected price case differs from reviewed source endpoint')
   need(case['all_original_Gamma_preserved'] is True and case['actual_receipt'] is False,'Core old Gamma/actual scope')
 return s

def primary():
 need(hashlib.sha256((CAPTURE/'sources.json').read_bytes()).hexdigest()==RAW_META_SHA,'Primary metadata changed')
 raw=json.loads(text(CAPTURE/'sources.json'));bodies={};obs=[]
 for r in raw:
  b=Path(r['cache_path']).read_bytes()
  need(r['HTTP_status']==200 and hashlib.sha256(b).hexdigest()==r['raw_sha256'],'Primary raw changed '+r['id'])
  if r['id']=='tie_pdf':
   with fitz.open(r['cache_path']) as doc:
    ts=[p.get_text() for p in doc]
   need(len(ts)==2 and 'criteria restarts' in ts[0] and 'Conference won-lost percentage' in ts[0],'Original tie PDF rule missing')
   r={**r,'PDF_text_sha256':{str(i+1):hashlib.sha256(t.encode()).hexdigest() for i,t in enumerate(ts)},
    'scope':'2017 published first-four criteria and partial-restart support; no 2023 eligible10 clause inferred from 2017 wording'}
  else:
   soup=BeautifulSoup(b,'html.parser')
   for n in soup(['script','style']):n.decompose()
   bodies[r['id']]=soup.get_text(' ',strip=True)
  obs.append(r)
 need(all(x in bodies['playin'] for x in ('APRIL 11','APRIL 12','APRIL 14')),'2023 play-in phase dates missing')
 need('Saturday, April 15' in bodies['calendar'] and 'Sunday, April 9' in bodies['calendar'],'2023 endpoints missing')
 need('full-time basis' in bodies['permanent'] and '10' in bodies['permanent'],'Permanent 7-10 format missing')
 need('from the beginning' in bodies['tie_current'] and 'best 10 records' in bodies['tie_current'],'Current tie interpretation missing')
 return {'raw_sources':obs,'current_standings_observed_season':'2025-26_at_2026_10_08',
  'current_eligible10_clause_is_crosscheck_not_original_2023_publication_certification':True,
  'first_four_and_restart_have_prior_primary_PDF_support':True,
  'historical_schedule_page_result_actor_typo_not_consumed':True,
  'failed_unadopted_URLs':['https://www.nba.com/news/2023-nba-play-in-tournament-schedule',
   'https://pr.nba.com/nba-board-of-governors-approves-heightened-penalty-for-transition-take-foul/'],
  'calendar':deepcopy(DATES)}

def ratios(team,opponents,rows):
 games=[g for g in rows if team in (g['home'],g['away']) and (g['away'] if team==g['home'] else g['home']) in opponents]
 need(games,'Tie ratio has no denominator')
 return Fraction(sum(g['winner']==team for g in games),len(games))
def values(group,criterion,g,leaders,eligible):
 out={}
 for t in group:
  if criterion=='division_winner':out[t]=Fraction(int(t in leaders))
  else:
   opponents=(set(group)-{t} if criterion=='head_to_head' else set(DIVISIONS[DIV[t]])-{t} if criterion=='division_record' else
    {u for u in CONF if CONF[u]==CONF[t]}-{t} if criterion=='conference_record' else
    eligible[CONF[t]]-{t} if criterion=='eligible_own' else eligible['WEST' if CONF[t]=='EAST' else 'EAST'])
   out[t]=ratios(t,opponents,g['rows'])
 return out
def resolve(group,g,leaders,eligible,trace,scope,division=False):
 if len(group)==1:return [group]
 criteria=(['head_to_head','division_winner'] if len(group)==2 else ['division_winner','head_to_head'])+['division_record','conference_record','eligible_own']
 if len(group)==2:criteria+=['eligible_other']
 for c in criteria:
  if c=='division_winner' and division:continue
  if c=='division_record' and len({DIV[t] for t in group})!=1:continue
  v=values(group,c,g,leaders,eligible)
  trace.append({'scope':scope,'group':list(group),'criterion':c,'values':{t:str(v[t]) for t in group}})
  buckets=defaultdict(list)
  for t,p in v.items():buckets[p].append(t)
  if len(buckets)>1:return [x for p in sorted(buckets,reverse=True) for x in resolve(sorted(buckets[p]),g,leaders,eligible,trace,scope,division)]
 trace.append({'scope':scope,'group':list(group),'criterion':'POINT_DIFFERENTIAL_REQUIRED','input_available':False,
  'BPM_margin_not_a_real_score':True,'random_drawing_only_after_full_point_criterion':True})
 return [sorted(group)]
def rankings(g):
 trace=[];leaders=[];eligible={}
 for c in ('EAST','WEST'):
  teams=[t for t in CONF if CONF[t]==c];threshold=sorted((g['team_records'][t]['wins'] for t in teams),reverse=True)[9]
  eligible[c]={t for t in teams if g['team_records'][t]['wins']>=threshold}
 for d,ts in DIVISIONS.items():
  high=max(g['team_records'][t]['wins'] for t in ts)
  r=resolve(sorted(t for t in ts if g['team_records'][t]['wins']==high),g,set(),eligible,trace,'DIVISION:'+d,True)
  need(len(r[0])==1,'Division title unresolved '+d);leaders.append(r[0][0])
 seeds={}
 for c in ('EAST','WEST'):
  buckets=defaultdict(list)
  for t in CONF:
   if CONF[t]==c:buckets[g['team_records'][t]['wins']].append(t)
  groups=[grp for w in sorted(buckets,reverse=True) for grp in resolve(sorted(buckets[w]),g,set(leaders),eligible,trace,c)]
  rs=[];n=1
  for group in groups:
   dom=list(range(n,n+len(group)))
   for t in group:rs.append({'team':t,'seed':n if len(group)==1 else None,'seed_domain':dom,**g['team_records'][t]})
   n+=len(group)
  seeds[c]=rs
 return {'conference_seeds':seeds,'division_winners':leaders,'tiebreak_trace':trace,
  'eligible_for_postseason_ratio_domains':{c:sorted(ts) for c,ts in eligible.items()}}
def assert_rankings(r,g):
 need(digest(r)==RANK_MEANING,'Returned rank/ratio/partial seed projection altered')
 for c,rs in r['conference_seeds'].items():
  need(len(rs)==15 and {x['team'] for x in rs}=={t for t in CONF if CONF[t]==c},'Seed ownership/domain')
  need(all((x['wins'],x['losses'])==(g['team_records'][x['team']]['wins'],g['team_records'][x['team']]['losses']) for x in rs),'Rank record changed')
 for x in r['tiebreak_trace']:
  if x['criterion']=='POINT_DIFFERENTIAL_REQUIRED':continue
  v=values(x['group'],x['criterion'],g,set(r['division_winners']),{c:set(ts) for c,ts in r['eligible_for_postseason_ratio_domains'].items()})
  need(x['values']=={t:str(v[t]) for t in x['group']},'Tie ratio not reconstructed from selected winners')

def role(team,s):
 t=deepcopy(s[GLOBAL]['shared_team_templates'][team]);sec=Counter();end=0;roles=Counter()
 for b in t['blocks']:
  need(b['start_second']==end and b['end_second']>end and b['end_second']<=2880,'Source quarter clock continuity')
  need(set(b['positions'])=={'PG','SG','SF','PF','C'} and len(set(b['positions'].values()))==5,'Five source positions')
  need(end//720==(b['end_second']-1)//720,'Quarter boundary missing')
  for pos,p in b['positions'].items():sec[p]+=b['end_second']-end;roles[pos]+=b['end_second']-end
  end=b['end_second']
 need(end==2880 and sum(sec.values())==14400 and set(roles.values())=={2880},'48/240 position clock')
 need(dict(sec)==t['positive_player_seconds'] and set(sec)<=set(t['active'])<=set(t['standard']),'Positive/active/STANDARD join')
 need(12<=len(t['active'])<=15 and 14<=len(t['standard'])<=15,'Nomination/registration count')
 if team=='CHI':
  need(t['blocks']==[{k:deepcopy(b[k]) for k in ('start_second','end_second','positions')} for b in s[H22]['selected_role_template']['ordered_regulation_blocks']],'H22 NORMAL source clock')
 return {'team':team,'template':t['id'],'standard':t['standard'],'TW':t['TW'],'active':t['active'],
  'inactive':t['inactive'],'blocks':t['blocks'],'positive_player_seconds':dict(sec),
  'new_operating_interval':['2023-04-10','2023-04-14'],'same_source_UPCs_and_full_Gamma_preserved':True,
  'actual_medical_or_contract_receipt':False,'no_TW_positive_postseason_minutes':True}
def game(key,day,home,away,s,played):
 views={t:role(t,s) for t in (home,away)}
 back={t:(t,(date.fromisoformat(day)-timedelta(days=1)).isoformat()) in played for t in views}
 impacts={t:sum(Fraction(s[GLOBAL]['selected_productivity_inputs'][p]['fraction'])*n for p,n in v['positive_player_seconds'].items())/2880 for t,v in views.items()}
 m=impacts[home]-impacts[away]+2+Fraction(int(back[away])-int(back[home]),2)
 need(m!=0,'Exact play-in proxy tie requires selected tie policy')
 endpoints=sorted({0,720,1440,2160,2880}|{b['end_second'] for v in views.values() for b in v['blocks']})
 segments=[]
 for start,end in zip(endpoints,endpoints[1:]):
  segments.append({'start_second':start,'end_second':end,'quarter':start//720+1,
   'positions':{t:deepcopy(next(b['positions'] for b in v['blocks'] if b['start_second']<=start<b['end_second'])) for t,v in views.items()}})
 return {'id':key,'date':day,'home':home,'away':away,'team_models':views,'back_to_back':back,
  'simultaneous_segments':segments,
  'home_impact':str(impacts[home]),'away_impact':str(impacts[away]),'exact_home_margin':str(m),
  'winner':home if m>0 else away,'loser':away if m>0 else home,'selected_working_result':True,
  'overtime_periods':0,'score':None,'actual_NBA_game_id':None,'actual_receipt_certified':False}
def assert_game(x,key,day,home,away,s,played):
 need((x['id'],x['date'],x['home'],x['away'])==(key,day,home,away),'Returned play-in date/identity changed')
 impacts={}
 for t in (home,away):
  # Direct source projection, not a second call to potentially patched role().
  src=s[GLOBAL]['shared_team_templates'][t]
  expected={'team':t,'template':src['id'],'standard':src['standard'],'TW':src['TW'],'active':src['active'],
   'inactive':src['inactive'],'blocks':src['blocks'],'positive_player_seconds':src['positive_player_seconds'],
   'new_operating_interval':['2023-04-10','2023-04-14'],'same_source_UPCs_and_full_Gamma_preserved':True,
   'actual_medical_or_contract_receipt':False,'no_TW_positive_postseason_minutes':True}
  need(x['team_models'][t]==expected,'Returned play-in roles/registration/fullGamma altered')
  impacts[t]=sum(Fraction(s[GLOBAL]['selected_productivity_inputs'][p]['fraction'])*n for p,n in src['positive_player_seconds'].items())/2880
 boundaries=sorted({0,720,1440,2160,2880}|{b['end_second'] for t in (home,away) for b in s[GLOBAL]['shared_team_templates'][t]['blocks']})
 need(len(x['simultaneous_segments'])==len(boundaries)-1,'Returned simultaneous interval count')
 seconds={t:Counter() for t in (home,away)}
 for q,start,end in zip(x['simultaneous_segments'],boundaries,boundaries[1:]):
  positions={t:next(b['positions'] for b in s[GLOBAL]['shared_team_templates'][t]['blocks'] if b['start_second']<=start<b['end_second']) for t in (home,away)}
  need(q=={'start_second':start,'end_second':end,'quarter':start//720+1,'positions':positions},'Returned simultaneous chronology/positions altered')
  for t,ps in positions.items():
   for p in ps.values():seconds[t][p]+=end-start
 need(all(dict(seconds[t])==s[GLOBAL]['shared_team_templates'][t]['positive_player_seconds'] for t in seconds),'Simultaneous 240 budgets differ')
 back={t:(t,(date.fromisoformat(day)-timedelta(days=1)).isoformat()) in played for t in (home,away)}
 m=impacts[home]-impacts[away]+2+Fraction(int(back[away])-int(back[home]),2)
 need(x['back_to_back']==back and (x['home_impact'],x['away_impact'],x['exact_home_margin'])==tuple(str(z) for z in (impacts[home],impacts[away],m)),'Returned play-in Fraction arithmetic altered')
 need((x['winner'],x['loser'])==((home,away) if m>0 else (away,home)),'Returned selected winner changed')
 need(x['selected_working_result'] is True and x['overtime_periods']==0 and x['score'] is None and x['actual_NBA_game_id'] is None and x['actual_receipt_certified'] is False,'Actual/score/OT scope promoted')

def build(root=ROOT):
 s=sources(root);obs=primary();g=s[GLOBAL]
 need(obs['calendar']==DATES and obs['first_four_and_restart_have_prior_primary_PDF_support'] is True and
      obs['current_eligible10_clause_is_crosscheck_not_original_2023_publication_certification'] is True,'Returned primary dates/scope altered')
 counts=Counter();wins=Counter()
 for x in g['rows']:
  need(x['winner'] in (x['home'],x['away']) and x['loser'] in (x['home'],x['away']) and x['winner']!=x['loser'],'Regular selected winner identity')
  counts.update((x['home'],x['away']));wins[x['winner']]+=1
 need(len(g['rows'])==1230 and set(counts.values())=={82} and all(g['team_records'][t]=={'wins':wins[t],'losses':82-wins[t]} for t in counts),'1230 source record rebuild')
 r=rankings(g);assert_rankings(r,g);matches=[];final={};played={(t,x['published_date']) for x in g['rows'] for t in (x['home'],x['away'])}
 for c,rs in r['conference_seeds'].items():
  ts={x['seed']:x['team'] for x in rs if x['seed'] is not None};need(all(n in ts for n in range(1,11)),'Unresolved seed affects playoffs/play-in')
  q=[]
  for phase,h,a in [('78',ts[7],ts[8]),('910',ts[9],ts[10])]:
   key=c+':'+phase;day=DATES[phase];x=game(key,day,h,a,s,played);assert_game(x,key,day,h,a,s,played);q.append(x);played.update((t,day) for t in (h,a))
  key=c+':FINAL';day=DATES['FINAL'];h,a=q[0]['loser'],q[1]['winner'];x=game(key,day,h,a,s,played);assert_game(x,key,day,h,a,s,played);q.append(x);matches+=q
  final[c]=[{'seed':n,'team':ts[n]} for n in range(1,7)]+[{'seed':7,'team':q[0]['winner']},{'seed':8,'team':q[2]['winner']}]
 qualified={x['team'] for rs in final.values() for x in rs};lottery=sorted(set(CONF)-qualified)
 need(len(qualified)==16 and len(lottery)==14,'16/14 partition')
 chi=next(x for x in final['EAST'] if x['team']=='CHI');other=next(x for x in final['EAST'] if x['seed']==9-chi['seed'])
 bracket=[{'conference':c,'higher_seed':hi,'lower_seed':9-hi,
  'home_court_team':next(x['team'] for x in rs if x['seed']==hi),
  'away_team':next(x['team'] for x in rs if x['seed']==9-hi),'series_results_selected':False} for c,rs in final.items() for hi in range(1,5)]
 gaps=[{'conference':c,'teams':[x['team'] for x in rs if x['seed'] is None],
  'seed_domain':next((x['seed_domain'] for x in rs if x['seed'] is None),[]),
  'next_input':'Source-supported explicit fictional regular points difference, then random drawing only if still tied',
  'playin_or_CHI_first_PO_dependency':False} for c,rs in r['conference_seeds'].items() if any(x['seed'] is None for x in rs)]
 return {'id':'NBA_2022_23_STANDINGS_AND_2023_PLAYIN','baseline_main':BASELINE,
  'status':'SELECTED_SIX_PLAYIN_RESULTS_CHI_FIRST_PO_BOUND_WITH_LOW_SEED_POINT_PORT',
  'source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_provenance':obs,'selected_policy':deepcopy(POLICY),**r,
  'core_price_adoption':{'source':CORE,'generation_global_market_pending_superseded_by_current_selection':True,
   'full_price_case_objects':deepcopy(s[CORE]['selected_core_execution']),'whole_team_six_cost_certified':False},
  'playin_games':matches,'final_playoff_seeds':final,'nonplayoff_lottery_origins':lottery,'first_round_bracket':bracket,
  'Chicago_first_PO':{'seed':chi['seed'],'opponent':other['team'],'opponent_seed':other['seed'],
   'home_court_team':other['team'] if other['seed']<chi['seed'] else 'CHI',
   'league_playoffs_begin':'2023-04-15','exact_CHI_series_calendar_selected':False,'series_winner_selected':False},
  'unresolved_rank_ports':gaps,'summary':{'regular_games':1230,'CHI_regular_wins':46,'CHI_regular_losses':36,
   'seed_team_rows':30,'exact_regular_seed_rows':sum(x['seed'] is not None for rs in r['conference_seeds'].values() for x in rs),
   'division_winners':6,'playin_games':6,'playoff_qualifiers':16,'lottery_origins':14,'CHI_PO_seed':chi['seed']},
  'certification':{'working_seeds_except_named_low_tie_and_six_playins_executed':True,'independent_review_completed':False,
   'all30_exact_regular_seed_order_certified':not gaps,'actual_private_medical_contract_receipts':False,
   'new_title_MVP_or_manuscript_permission':False,'2023_full_pick_control_executed':False,'whole_macro3_complete':False},
  'remaining_finite_inputs':['Named low-seed points port, separate from six play-ins and CHI first bracket.',
   'CHI first-series dated/availability/result family and remaining PO; no title selected.',
   '2023 draft origin/right-control functions; no original historical draft order inherited.'],
  'model_limit':'Fixed zero-growth productivity is neither a calibrated prediction nor actual NBA points/statistics.',
  'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False,'Pack_count':0,
  'unfinished_macro_groups':5,'unfinished_through_6':4}
def render(v):
 lines=['# 2022–23 순위·2023 플레이인·Chicago 첫 PO','',v['status'],'',
  '새1230승자를 직접 집계하고 동률을 명명 비율로 푼다. 원2022 시드/날짜/COBY_OUT 또는 원NBA2023 결과는 복사하지 않았다.','',
  '[당대 NBA 일정 발표](https://pr.nba.com/2022-23-nba-schedule/)·[공식 플레이인 일정](https://www.nba.com/playoffs/2023/play-in-tournament/schedule)에서 날짜를 읽었다. 4/11 7–8, 4/12 9–10, 4/14 최종전·4/15 PO개막만 소비한다. 원페이지의 선수/승자/점수 및 Chicago관련 결과표기 오기는 소비하지 않는다.','',
  '[기존 공식 동률 PDF](https://ak-static-int.nba.com/wp-content/uploads/sites/2/2017/06/NBA_Tiebreaker_Procedures.pdf)의 첫4기준과 부분분리 재시작을 적용한다. 후행 eligible10은 현재 NBA 페이지 교차관측이며 원2023 문서 인증과 구분한다. 실제 점수차 없이 그 후행 조건까지 같은 하위 두팀의 순번을 만들어내지 않는다.','',
  '| East 순번 | West 순번 |','|---|---|']
 for e,w in zip(v['conference_seeds']['EAST'],v['conference_seeds']['WEST']):
  lines.append(f"| {e['seed'] or e['seed_domain']} {e['team']} {e['wins']}–{e['losses']} | {w['seed'] or w['seed_domain']} {w['team']} {w['wins']}–{w['losses']} |")
 lines+=['','## 새 가상 플레이인 실행','',
  '같은 당해 UPC·원Γ·선택 가격/보호급여를 4/14까지 유지하고 명명 역할·가용을 새 postregular 모델로 연장한다. CHI는 H22 NORMAL, 신인 기용 및 Chet OUT/Miles UPC0 예외를 유지한다. STANDARD 양수만 사용하며 TW 활성화/새이적/계약가격 변경은 없다. 기관실제 접수·임상·전체 재정금액의 인증이 아니다.','',
  '| 날짜 | 경기 | 가상 승자 | 정확 홈 마진 |','|---|---|---|---|']
 lines += [f"| {x['date']} | {x['home']}–{x['away']} | {x['winner']} | {x['exact_home_margin']} |" for x in v['playin_games']]
 lines+=['',f"Chicago 첫 PO: seed{v['Chicago_first_PO']['seed']} / {v['Chicago_first_PO']['opponent']} 상대. 시리즈 날짜·승자·우승은 미선택. 16qualifier/14lottery를 분리하고 2023 전체픽을 선행 새게이트로 요구하지 않는다.",'',
  '## 남은 유한 입력','']+['- '+s for s in v['remaining_finite_inputs']]
 lines+=['','[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','',
  '| 묶음 | 현황 |','|---|---|','| 1 | 완료 |','| 2 | 완료 |','| 3 | 진행 |','| 4 | 진행 |','| 5 | 대기 |','| 6 | 대기 |','| 7 | CLOSED |','',
  '미완료큰묶음5 · 6번까지4 · v0.30 PARTIAL · CLOSED · Pack0 · 원고0.']
 return '\n'.join(lines)+'\n'
def validate(v,root=ROOT):
 try:return [] if v==build(root) else ['Saved seed/play-in differs from physical current sources']
 except (AssertionError,KeyError,ValueError) as e:return [str(e)]
def self_test():
 labels=[]
 def reject(label):
  try:build()
  except (AssertionError,KeyError,ValueError):labels.append(label);return
  raise AssertionError('FALSE_PASS '+label)
 orig=rankings
 def rank(g):
  x=orig(g);x['conference_seeds']['EAST'][0]['seed']=2;return x
 with patch(__name__+'.rankings',side_effect=rank):reject('returned_rank_identity')
 origrole=role
 def rolefault(t,s):
  x=origrole(t,s);p=x['blocks'][0]['positions'];p['PG'],p['SG']=p['SG'],p['PG'];return x
 with patch(__name__+'.role',side_effect=rolefault):reject('returned_same_budget_role_position')
 origgame=game
 def wrongdate(*args):
  x=origgame(*args);x['date']='2022-04-12';return x
 with patch(__name__+'.game',side_effect=wrongdate):reject('returned_old_year_date')
 def wrongwin(*args):
  x=origgame(*args);x['winner']=x['loser'];return x
 with patch(__name__+'.game',side_effect=wrongwin):reject('returned_wrong_winner')
 return labels
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(render(v),encoding='utf-8')
 r={'summary':v['summary'],'CHI_first_PO':v['Chicago_first_PO'],'unresolved_rank_ports':v['unresolved_rank_ports']}
 if a.check:need(not validate(json.loads(text(ROOT/OUT))),'Saved stale');need(text(ROOT/MD)==render(v),'MD stale');r['current']=True
 if a.self_test:r['negative_controls']=self_test()
 print(json.dumps(r,ensure_ascii=False))
if __name__=='__main__':main()
