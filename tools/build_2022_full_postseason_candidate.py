"""Finite postseason candidate; preserve selected CHI-PHI, never select a title.

Consumes physical pinned public/model inputs without rebuilding ancestors.
New dates, continued contracts and availability are an admitted fictional
candidate, not historical facts or an extension of ancestor medical scope.
"""
from pathlib import Path
from fractions import Fraction
from datetime import date, timedelta
from collections import Counter
from copy import deepcopy
from unittest.mock import patch
import argparse, hashlib, json

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_full_postseason_candidate.py'
OUT='design/NBA_2022_FULL_POSTSEASON_CANDIDATE.json'; MD=OUT[:-5]+'.md'
GLOBAL='simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json'
SEED='simulation/NBA_2021_22_STANDINGS_PLAYIN_AND_2022_RIGHTS.json'
FIRST='simulation/CHICAGO_PHI_2022_FIRST_ROUND.json'
PEER='reviews/CHICAGO_PHI_2022_FIRST_ROUND_G11_INDEPENDENT_REVIEW_2026_10_08.json'
FIRST_TOOL='tools/build_chicago_phi_2022_first_round.py'
PINS={'simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json': '93264d2dff86a58ad10ca6975315c6c2167961f94f2517b6f5f79fa3113f2af8', 'simulation/NBA_2021_22_STANDINGS_PLAYIN_AND_2022_RIGHTS.json': '139c1d6a90d1bd7ee672020af96e03bf6767599637902c329b1e772fdfcf63d9', 'simulation/CHICAGO_PHI_2022_FIRST_ROUND.json': 'a167d96c64fa790250908a5a071f3abe355be2d951fa47bbb7f9a928c464202b', 'reviews/CHICAGO_PHI_2022_FIRST_ROUND_G11_INDEPENDENT_REVIEW_2026_10_08.json': '5a2ad16de4af768591030ad4cb5a7dd0f052cca8962054ccb15c5136fb3f5679', 'tools/build_chicago_phi_2022_first_round.py': 'cc91eb42ab6796335c01d4b72dc1e12b3761e02314445baeb901f9f5e34b970d'}
BASELINE='bebabcf65be6af0d73d39b5a290249de52952397'
POSITIONS={'PG','SG','SF','PF','C'}
STARTS={'R1':'2022-04-16','R2':'2022-05-03','CF':'2022-05-20','F':'2022-06-06'}
OFFSETS=(0,2,5,7,9,12,14); HOME_PATTERN=(0,0,1,1,0,1,0)
POLICY={
 'model':'BPM_MAR25_EB_PLUS_HOME2_PLUS_B2B_HALF',
 'new_fourteen_series_class':'UNSELECTED_ADMITTED_FICTIONAL_POSTSEASON_CANDIDATE',
 'existing_CHI_PHI_selected_series_preserved':True,
 'same_salary_year_existing_UPCs_all_Gamma_and_named_cost_obligations_preserved':True,
 'contracts_cover_candidate_dates_by_explicit_lawful_continuation_condition':True,
 'no_new_trade_waiver_contract_bonus_or_TW_conversion':True,
 'standard_only_postseason_participants':True,
 'new_positive_availability_and_rotation_continuation_is_candidate':True,
 'no_new_contact_injury_or_productivity_growth_modeled':True,
 'CHI_normal_from_Apr16_only_is_existing_selected_family':True,
 'BKN_home_NYC_TOR_OUT_other_US_road_RETURN_lawful_host_access_condition':True,
 'historical_scores_OT_winners_or_real_clinical_diagnosis_imported':False,
 'new_calendar_selected_by_author':False,
 'new_other_series_health_selected_by_author':False,
 'championship_selected_root_or_author_lock':False,
 'NBA_Season_end_or_eight_option_windows_selected':False,
}
FIXED_POLICY=deepcopy(POLICY)

def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(root,p):return json.loads(text(root/p)) if p.endswith('.json') else text(root/p)
def sources(root):
 assert POLICY==FIXED_POLICY,'Candidate policy altered'
 result={}
 for p,h in PINS.items():
  assert sha(root/p)==h,'Physical source changed '+p
  v=load(root,p); physical=json.loads(text(root/p)) if p.endswith('.json') else text(root/p)
  assert v==physical,'Returned source differs from independent physical parse '+p
  result[p]=v
 peer=result[PEER]
 assert peer['independent_review_completed'] and peer['source_sha256'][FIRST]==PINS[FIRST]
 assert peer['source_sha256'][FIRST_TOOL]==PINS[FIRST_TOOL]
 return result

def clock(v,g):
 assert v['registration']==g['team_rosters'][v['team']], 'Role registration differs from original owner family'
 owners={(a['team'],a['source_name']):a['class'] for rows in g['owner_catalog'].values() for a in rows}
 for cls,names in [('standard',v['registration']['standard']),('TW',v['registration']['TW'])]:
  assert len(names)==len(set(names))
  assert all(owners.get((v['team'],p))==cls for p in names),'Source owner/class mismatch'
 assert 12<=len(v['active'])<=15 and len(set(v['active']))==len(v['active'])
 assert set(v['active'])<=set(v['registration']['standard'])
 assert not(set(v['active'])&set(v['registration']['TW']))
 end=0; people=Counter(); roles={k:Counter() for k in POSITIONS}
 for b in v['blocks']:
  assert b['start_second']==end and b['end_second']>end
  positions=b['positions']; assert set(positions)==POSITIONS and len(set(positions.values()))==5
  n=b['end_second']-end
  for role,p in positions.items():
   assert p in v['active'];people[p]+=n;roles[role][p]+=n
  end=b['end_second']
 assert end==2880 and sum(people.values())==14400
 assert dict(people)==v['positive_player_seconds']
 assert {k:dict(v) for k,v in roles.items()}==v['role_player_seconds']
 assert all(sum(v.values())==2880 for v in roles.values())
 assert v['actual_active_or_medical_certified'] is False
 return people

def template_key(team,home,away):
 if team=='CHI':state='NORMAL'
 elif team=='GSW':state='KLAY_WORKING_RETURN'
 elif team=='BKN':state='IRVING_AWAY_RETURN' if away=='BKN' and home not in ('BKN','NYK','TOR') else 'IRVING_INSTITUTIONAL_OUT'
 else:state='NORMAL'
 return team+':'+state

def higher_home(a,b,conference,seeds,g):
 if conference!='NBA':return (a,b) if seeds[conference][a]<seeds[conference][b] else (b,a)
 # No invented cross-conference tie resolver. The computed final has unequal records.
 wa=g['team_records'][a]['wins'];wb=g['team_records'][b]['wins']
 assert wa!=wb,'Finals equal-record home-court is a finite unresolved rule port'
 return (a,b) if wa>wb else (b,a)

def game(day,home,away,number,sid,g):
 keys={t:template_key(t,home,away) for t in (home,away)}
 impacts={t:sum(Fraction(g['selected_productivity_inputs'][p]['fraction'])*n for p,n in g['shared_role_templates'][key]['positive_player_seconds'].items())/2880 for t,key in keys.items()}
 margin=impacts[home]-impacts[away]+2
 assert margin!=0,'Exact tied productivity needs an explicit candidate result port'
 return {'id':sid+':G'+str(number),'date':day,'game_number':number,'home':home,'away':away,
  'team_template_keys':keys,'weighted_BPM_fraction':{t:str(v) for t,v in impacts.items()},
  'home_advantage_fraction':'2','back_to_back_fatigue_fraction':'0',
  'exact_home_proxy_margin':str(margin),'candidate_regulation_winner':home if margin>0 else away,
  'score':None,'overtime':None,'physical_NBA_game_id':None,'historical_winner_used':False,
  'actual_registration_clinical_or_receipt_certified':False}

def assert_game(v,day,home,away,number,sid,g):
 # Independent caller arithmetic and source binding, not a call to game().
 assert (v['id'],v['date'],v['game_number'],v['home'],v['away'])==(sid+':G'+str(number),day,number,home,away),'Returned candidate date/actor altered'
 keys={t:template_key(t,home,away) for t in (home,away)}
 assert v['team_template_keys']==keys,'Returned source role/availability altered'
 impacts={}
 for t,key in keys.items():
  q=g['shared_role_templates'][key]; clock(q,g)
  impacts[t]=sum(Fraction(g['selected_productivity_inputs'][p]['fraction'])*n for p,n in q['positive_player_seconds'].items())/2880
 m=impacts[home]-impacts[away]+Fraction(2)
 assert v['weighted_BPM_fraction']=={t:str(n) for t,n in impacts.items()}
 assert v['exact_home_proxy_margin']==str(m) and v['candidate_regulation_winner']==(home if m>0 else away),'Returned candidate result arithmetic altered'
 assert v['home_advantage_fraction']=='2' and v['back_to_back_fatigue_fraction']=='0'
 assert v['score'] is None and v['overtime'] is None and v['physical_NBA_game_id'] is None
 assert v['historical_winner_used'] is False and v['actual_registration_clinical_or_receipt_certified'] is False,'Actual/historical certification promoted'

def series(sid,conference,round_name,a,b,seeds,g,first):
 high,low=higher_home(a,b,conference,seeds,g);count=Counter();rows=[]
 for i,offset in enumerate(OFFSETS,1):
  if max(count.values(),default=0)==4:break
  home,away=(high,low) if HOME_PATTERN[i-1]==0 else (low,high)
  day=(date.fromisoformat(STARTS[round_name])+timedelta(days=offset)).isoformat()
  q=game(day,home,away,i,sid,g);count[q['candidate_regulation_winner']]+=1;rows.append(q)
 return {'id':sid,'conference':conference,'round':round_name,'teams':[a,b],'higher_home_court':high,
  'upstream_series_ids':[], 'classification':'IMMUTABLE_SELECTED_CHI_PHI_SOURCE' if {a,b}=={'CHI','PHI'} else 'UNSELECTED_NEW_CANDIDATE',
  'games':rows,'wins':dict(count),'candidate_winner':max(count,key=count.get),
  'original_selected_series':deepcopy(first) if {a,b}=={'CHI','PHI'} else None}

def assert_series(v,conference,round_name,a,b,sid,seeds,g,first,dependencies):
 assert (v['id'],v['conference'],v['round'],v['teams'])==(sid,conference,round_name,[a,b]),'Returned bracket actors changed'
 high,low=higher_home(a,b,conference,seeds,g)
 assert v['higher_home_court']==high and v['upstream_series_ids']==dependencies
 count=Counter()
 for i,q in enumerate(v['games'],1):
  assert i<=7 and max(count.values(),default=0)<4,'Game after series clinch'
  home,away=(high,low) if HOME_PATTERN[i-1]==0 else (low,high)
  day=(date.fromisoformat(STARTS[round_name])+timedelta(days=OFFSETS[i-1])).isoformat()
  assert_game(q,day,home,away,i,sid,g);count[q['candidate_regulation_winner']]+=1
 assert max(count.values())==4 and 4<=len(v['games'])<=7
 assert v['wins']==dict(count) and v['candidate_winner']==max(count,key=count.get)
 is_first={a,b}=={'CHI','PHI'}
 assert v['classification']==('IMMUTABLE_SELECTED_CHI_PHI_SOURCE' if is_first else 'UNSELECTED_NEW_CANDIDATE')
 if is_first:
  assert v['original_selected_series']==first,'Immutable first-series full object altered'
  assert [(q['date'],q['home'],q['away'],q['candidate_regulation_winner'],q['exact_home_proxy_margin'],q['team_template_keys']) for q in v['games']]==[(q['date'],q['home'],q['away'],q['selected_regulation_winner'],q['exact_home_proxy_margin'],q['team_template_keys']) for q in first['games']],'Selected seven-game calendar or result changed'
 else:assert v['original_selected_series'] is None

def build(root=ROOT):
 src=sources(root);g=src[GLOBAL];s=src[SEED];first=src[FIRST]['selected_series']
 assert g['summary']['league_games']==1230 and s['final_playoff_seeds']['EAST'][6]['team']=='CHI'
 seeds={c:{q['team']:q['seed'] for q in rows} for c,rows in s['final_playoff_seeds'].items()}
 assert all(sorted(d.values())==list(range(1,9)) for d in seeds.values())
 qualified=[t for d in seeds.values() for t in d];assert len(set(qualified))==16
 records=[];by_id={};conference_winners={}
 def add(conf,rnd,a,b,idx,deps):
  sid=f'ALT2022:{conf}:{rnd}:{idx}'
  v=series(sid,conf,rnd,a,b,seeds,g,first);v['upstream_series_ids']=deps
  assert_series(v,conf,rnd,a,b,sid,seeds,g,first,deps)
  records.append(v);by_id[sid]=v;return v
 for conf,d in seeds.items():
  by_seed={rank:t for t,rank in d.items()}
  r1=[add(conf,'R1',by_seed[a],by_seed[b],i,[]) for i,(a,b) in enumerate([(1,8),(4,5),(2,7),(3,6)],1)]
  r2=[add(conf,'R2',r1[a]['candidate_winner'],r1[b]['candidate_winner'],i,[r1[a]['id'],r1[b]['id']]) for i,(a,b) in enumerate([(0,1),(2,3)],1)]
  cf=add(conf,'CF',r2[0]['candidate_winner'],r2[1]['candidate_winner'],1,[v['id'] for v in r2]);conference_winners[conf]=cf
 finals=add('NBA','F',conference_winners['EAST']['candidate_winner'],conference_winners['WEST']['candidate_winner'],1,[v['id'] for v in conference_winners.values()])
 assert len(records)==15 and sum(v['classification']=='IMMUTABLE_SELECTED_CHI_PHI_SOURCE' for v in records)==1
 templates={key:deepcopy(g['shared_role_templates'][key]) for key in sorted({k for v in records for q in v['games'] for k in q['team_template_keys'].values()})}
 # Source-bound final pools; actual family registration is not certified.
 assert all(clock(v,g) for v in templates.values())
 final_day=finals['games'][-1]['date'];assert final_day<='2022-06-30'
 return {'id':'NBA_2022_FULL_POSTSEASON_CANDIDATE','baseline_main':BASELINE,
  'status':'COMPLETE_15_SERIES_CANDIDATE_ONE_IMMUTABLE_SELECTION_FOURTEEN_UNSELECTED',
  'source_sha256':{**PINS,SELF:sha(root/SELF)},'hash_method':'UTF8_BOM_STRIP_CRLF_CR_TO_LF',
  'policy':deepcopy(POLICY),'sixteen_playoff_seed_rows':deepcopy(s['final_playoff_seeds']),
  'postseason_team_template_pool':templates,'series':records,
  'candidate_champion':finals['candidate_winner'],'candidate_last_Finals_date':final_day,
  'calendar_classification':'NEW_FICTIONAL_ROUND_CALENDAR; no physical NBA dates except preserved selected CHI-PHI local calendar; starts are candidate only',
  'format_source_preserved':deepcopy(src[FIRST]['primary_format_observation']),
  'availability_candidate_scope':'Continue current standard registered positive roles into candidate dates without new contact injuries. GSW Klay-working-return and Wiseman-out continue; BKN only admitted non-NYC/non-TOR US away return, home remains out; CHI NORMAL is already selected fromApr16. No original medical facts or blanket actual foreign/access certification.',
  'legal_candidate_scope':'Same 2021-22 retained UPCs/Gamma/full waived-camp-stretch-FA-unsigned-exception obligations through candidate participation, no new amount or assignments. Postseason STD only. Existing per-date source legality is not silently certified beyond its prior interval; this explicit candidate continuation is separately reviewable.',
  'summary':{'qualified_teams':16,'series':15,'preserved_selected_series':1,'new_unselected_series':14,
   'candidate_games':sum(len(v['games']) for v in records),'candidate_team_dates':2*sum(len(v['games']) for v in records),
   'templates':len(templates),'regulation_seconds_per_team':2880,'player_seconds_per_team':14400,
   'selected_CHI_postseason_games_unchanged':7,'selected_CHI_elimination_unchanged':'2022-04-30',
   'regular_1230_playin_and_2022_rank_holder_changed':False},
  'remaining_finite_ports':[
   'Review and consequential selection of candidate league champion/title and dependent butterfly effects; no root or author adoption recorded here.',
   'New fourteen-series calendar and same-contract/availability candidate must be adopted separately; no actual clinical or foreign/venue receipt proof required.',
   'NBA Season ends after actual selected last Finals game; candidate date does not select the eight outstanding option windows. Keep each existing option consumer unresolved until that selection.',
   'Selected 2022 draw/rank/holder and board remain unchanged; no draftee/UPC/Tender/contract amount automatically selected by title candidate.'],
  'certification':{'independent_review_completed':False,'root_adoption_recorded':False,'new_calendar_or_other_series_health_author_selected':False,
   'championship_author_locked':False,'actual_contract_medical_or_institutional_acceptance':False,
   'all_source_global_private_conditions_certified':False,'NBA_Season_end_and_eight_options_selected':False,
   'whole_macro3_G13_G16_or_manuscript':False},'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}

def validate(v,root=ROOT):return [] if v==build(root) else ['Saved candidate differs from physical source-bound reconstruction']
def markdown(v):
 lines=['# 2022 전체 포스트시즌 · 단일 유한 후보','','확정 Chicago–Philadelphia 7경기를 그대로 보존한 15시리즈 후보이다. 나머지14시리즈·새 달력·가용성 연속·우승은 미채택 후보다. 같은 분수 BPM/EB와 홈2, 정규48분/5포지션/240분을 사용한다. 실제 점수·OT·우승사실은 인증하지 않는다.','','| 시리즈 | 대진 | 후보 승자 | 경기수 | 말단 날짜 |','|---|---|---|---|---|']
 lines += [f"| {x['id']} | {'–'.join(x['teams'])} | {x['candidate_winner']} | {len(x['games'])} | {x['games'][-1]['date']} |" for x in v['series']]
 lines += ['',f"후보 우승자 **{v['candidate_champion']}**, 후보 Finals 말단 **{v['candidate_last_Finals_date']}**. Root 채택/작가잠금 false다. 고정생산성·분산0의 시뮬레이션 산출이며 현실예측/확률/MVP 권한이 아니다.",'','계약은 기존2021–22 UPC·모든 Γ 및 명명 비용을 같은 샐러리연도에 보존하는 명시적 후보로 연속한다. 새 이적/금액/방출/TW 전환0, 양수 출전은 STD만이며 active12–15. BKN 홈/NYC/TOR OUT과 그 외 미국 원정의 적법 접근 조건·가상 RETURN을 구분한다. 원 임상/접수 인증0.','','Chicago NORMAL 4/16 이후와 4/30 탈락·기존7일·주인공 PO224분은 불변이며 정규 QO분에 더하지 않는다. 정규1230/플레이인/선택추첨·60순번과 소유/2022계약 금액은 변하지 않는다.','','NBA Season 말단은 선택된 마지막 Finals 뒤다. 이 후보날짜를 원 NBA 사실이나 현재 확정 말단으로 쓰지 않으며 미선택8옵션창을 보존한다. 14시리즈·우승의 채택과 후손 비용/사건은 남아 있다.','','출처 지문과 독립 물리 파서·원 소유카탈로그·선택 포지션 시계·반환 결과 가드를 검문한다. 조상 생성기 재실행0. 작성자 음성검문은 독립 검문으로 세지 않는다.','','[현행 로드맵](WORLD_BIBLE_COMPLETION_ROADMAP.md) · [확정 첫 시리즈](../simulation/CHICAGO_PHI_2022_FIRST_ROUND.md)','','| 묶음 | 상태 |','|---|---|','| 1 드래프트 연쇄 | 완료 |','| 2 Chicago2020–21 | 완료 |','| 3 2021–23 | 1230/시드/추첨·첫 PO시리즈 완료, 전체 PO 후보·후속 시즌 미완료 |','| 4 장기 커리어 | 진행 |','| 5 전체 구조 | 현행 기능등록기 참조, 전체 미완료 |','| 6 규격·Context Pack | 현행 source등록기 참조, Pack0 |','| 7 통합·작가 승인 | 미완료 |','','미완료 큰묶음5/6번까지4 · v0.30 PARTIAL · CLOSED · 원고0.','']
 return '\n'.join(lines)

def self_test():
 original=game
 for label,field,value in [('winner','candidate_regulation_winner','OKC'),('score','score',100),('clock','team_template_keys',{'MIL':'MIL:NONEXISTENT'})]:
  def bad(*a,field=field,value=value,**kw):
   v=original(*a,**kw);v[field]=value;return v
  with patch(__name__+'.game',bad):
   try:build()
   except AssertionError:pass
   else:raise AssertionError('FALSE_PASS '+label)
 original_load=load
 def wrong(root,p):
  v=original_load(root,p)
  if p==SEED:v['final_playoff_seeds']['EAST'][6]['team']='OKC'
  return v
 with patch(__name__+'.load',wrong):
  try:build()
  except AssertionError:pass
  else:raise AssertionError('FALSE_PASS physical substitution')
 return 4
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();v=build()
 if a.write:
  (ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if a.check:assert load(ROOT,OUT)==v and text(ROOT/MD)==markdown(v),'Saved candidate stale'
 print(json.dumps({'current':True,'summary':v['summary'],'candidate_champion':v['candidate_champion'],'writer_controls':self_test() if a.self_test else None}))
if __name__=='__main__':main()
