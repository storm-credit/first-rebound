"""One fixed-seed fictional 2022 draw; no physical NBA draw or draftee copy.

Consumes reviewed result/seed/public-control leaves, never ancestor build().
The counter stream is a reproducible simulation device, not a physical audit.
"""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from itertools import combinations
from fractions import Fraction
from unittest.mock import patch
import argparse,hashlib,json
import fitz
import build_2022_public_control_execution_family as control

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_selected_working_draw_and_control.py'
OUT='simulation/NBA_2022_SELECTED_WORKING_DRAW_AND_CONTROL.json';MD=OUT[:-5]+'.md'
GLOBAL='simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json'
SEED=control.SEED;FAMILY=control.OUT;PRIMARY='research/NBA_2022_STANDINGS_AND_DRAFT_PRIMARY_OBSERVATIONS_2026_10_07.json'
PINS={GLOBAL:'93264d2dff86a58ad10ca6975315c6c2167961f94f2517b6f5f79fa3113f2af8',SEED:'139c1d6a90d1bd7ee672020af96e03bf6767599637902c329b1e772fdfcf63d9',FAMILY:'86ac9e85b06a607363f5c7a6bd6fac29a8a5dbd89fff803e2a440897afd3337c',PRIMARY:'165e240a765ac07d98253b348654022978ef7e034c90bcfbd874694cd19dfda6',control.SELF:'42e5bd033e174a161587ef3ac6d82bf37946e64a6f759b1bceaa047db423785b'}
PUBLIC_SEED='first-rebound|2022-draft|routine-v1|2026-10-08'
WEIGHTS=(140,140,140,125,105,90,75,60,45,30,20,15,10,5)
BYLAWS=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-2019-bylaws.pdf')
RAW_SHA='6accb3d9633e15e8559d13228c27ae7b3b0b81eac0894050b06256eea6da3464'
PAGE_SHAS={85:'312b5df737e0460a3671e61291f403b9488ee32827d938cebea87867f3bf0239',86:'b39fe3c49719251a389390384fe243b457b50716a1f456c7e34f8771d07093f0',87:'43197a4945acf5176d9335d2ff911f7c516a1db82e623c4ca53bb264fc094e20'}

def need(v,m):
 if not v:raise AssertionError(m)
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def direct(root,p):return json.loads(text(root/p))
def physical(root,p):return direct(root,p)
def sources(root):
 out={}
 for p,h in PINS.items():
  need(sha(root/p)==h,'Source stale '+p)
  if p.endswith('.json'):
   v=physical(root,p)
   # physical() delegates to direct(); a patched direct() must not validate its
   # own returned mutation. Parse original disk text independently here.
   actual=json.loads(text(root/p));need(v==actual,'Returned source differs from physical '+p);out[p]=v
 need(PUBLIC_SEED=='first-rebound|2022-draft|routine-v1|2026-10-08' and WEIGHTS==(140,140,140,125,105,90,75,60,45,30,20,15,10,5),'Fixed seed/primary probability policy changed')
 return out

def primary():
 need(hashlib.sha256(BYLAWS.read_bytes()).hexdigest()==RAW_SHA,'Bylaws bytes changed')
 with fitz.open(BYLAWS)as d:
  for i,h in PAGE_SHAS.items():need(hashlib.sha256(d[i-1].get_text().encode()).hexdigest()==h,'Bylaws page changed')
 return {'official_raw':{'url':'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf','path':str(BYLAWS),'raw_sha256':RAW_SHA,'PDF_1based_text_sha256':{str(i):h for i,h in PAGE_SHAS.items()},'extraction':'PyMuPDF get_text() UTF8','scope':'7.02(a) 14 odds/top4/remainder;7.02(b)(c) inverse records and reverse ties'},'direct_primary_web_observations':[{'url':'https://pr.nba.com/2022-nba-draft-tiebreakers/','date':'2022-04-18','web_reference':'turn2347view0','locator':'lines14,26,31–46','scope':'2022 14 probabilities, random tie order, top4 and undrawn order; historical teams/results not copied','raw_body_adopted':False},{'url':'https://www.nba.com/wizards/nba-draft-lottery-2022-everything-you-need-know-about-wizards-odds','web_reference':'turn2344search1','scope':'2022 four-ball combinations and repeated-team rejection','raw_body_adopted':False,'normal_open':'IFRAME_ONLY'},{'url':'https://www.nba.com/pacers/news/how-the-nba-draft-lottery-works','web_reference':'turn2344search0','scope':'2022 1000 assigned combinations and one unassigned','raw_body_adopted':False,'normal_open':'IFRAME_ONLY'},{'url':'https://www.nba.com/hawks/features/hawks-lottery-odds-explained','date':'2019','web_reference':'turn2348search1','scope':'Lottery ties pool odds; current lottery records have no ties so branch not executed','raw_body_adopted':False}], 'failed_direct_HTTP_metadata':'C:/Users/Storm Credit/AppData/Local/Temp/fr-draw2022-20261008/metadata.json','failed_odds_HTTP_metadata':'C:/Users/Storm Credit/AppData/Local/Temp/fr-draw2022-20261008/official_odds.metadata.json','HTTP403_adopted_as_body':False}

class Stream:
 def __init__(self):self.counter=0;self.events=[]
 def below(self,n,label):
  bits=256;lim=(1<<bits)-((1<<bits)%n)
  while True:
   payload=(PUBLIC_SEED+'|'+str(self.counter)).encode();h=hashlib.sha256(payload).hexdigest();v=int(h,16);accepted=v<lim
   self.events.append({'counter':self.counter,'label':label,'n':n,'digest':h,'accepted_unbiased_integer':accepted,'value':v%n if accepted else None});self.counter+=1
   if accepted:return v%n

def draw_once(src):
 r=Stream();ties=[]
 for b in src[SEED]['first_round_nonlottery_origin_buckets']:
  if not b['same_record_draft_drawing_required']:continue
  order=list(b['origins']);steps=[]
  for i in range(len(order)-1,0,-1):
   j=r.below(i+1,'TIE_'+str(b['wins'])+'_'+str(i));steps.append({'i':i,'j':j});order[i],order[j]=order[j],order[i]
  ties.append({'id':'FIRST_TIE_'+str(b['wins']),'fictional_date':'2022-04-18','origins_before':list(b['origins']),'first_order':order,'fisher_yates_steps':steps})
 pool=src[SEED]['nonplayoff_lottery_origins'];comb=list(combinations(range(1,15),4));owners=[t for t,w in zip(pool,WEIGHTS)for _ in range(w)]+[None]
 won=[];attempts=[]
 while len(won)<4:
  need(len(attempts)<10000,'Bounded draw failure, never reseed')
  available=list(range(1,15));balls=[];steps=[]
  for i in range(4):
   j=r.below(len(available),'LOTTERY_'+str(len(attempts))+'_'+str(i));steps.append(j);balls.append(available.pop(j))
  c=tuple(sorted(balls));index=comb.index(c);owner=owners[index];accepted=owner is not None and owner not in won
  attempts.append({'attempt':len(attempts),'target_pick':len(won)+1,'ordered_balls':balls,'available_list_indices':steps,'combination':list(c),'combination_index0':index,'assigned_origin':owner,'accepted_new_origin':accepted,'discard_reason':None if accepted else('UNASSIGNED'if owner is None else'ALREADY_SELECTED')})
  if accepted:won.append(owner)
 return {'rng_events':r.events,'ties':ties,'lottery_attempts':attempts,'lottery_top4':won,'lottery_first14':won+[t for t in pool if t not in won]}

def assert_draw(d,src):
 # Independent caller replay consumes primitive hash values and source pools;
 # it never recalls draw_once or Stream.below as its own expected output.
 events=d['rng_events'];need(events,'No random stages');values=[]
 for i,e in enumerate(events):
  need(e['counter']==i and type(e['n'])is int and e['n']>0,'Random event counter/range changed')
  h=hashlib.sha256((PUBLIC_SEED+'|'+str(i)).encode()).hexdigest();v=int(h,16);lim=2**256-(2**256%e['n']);ok=v<lim
  need(e['digest']==h and e['accepted_unbiased_integer']==ok and e['value']==(v%e['n']if ok else None),'Primitive random stream altered')
  if ok:values.append((e['label'],e['n'],e['value']))
 cursor=0
 def take(label,n):
  nonlocal cursor
  need(cursor<len(values),'Random stage missing');e=values[cursor];cursor+=1;need(e[:2]==(label,n),'Random logical stage changed');return e[2]
 buckets=[b for b in src[SEED]['first_round_nonlottery_origin_buckets']if b['same_record_draft_drawing_required']]
 need(len(d['ties'])==len(buckets),'Tie draw count changed')
 for t,b in zip(d['ties'],buckets):
  order=list(b['origins']);steps=[]
  for i in reversed(range(1,len(order))):
   j=take('TIE_'+str(b['wins'])+'_'+str(i),i+1);steps.append({'i':i,'j':j});order[i],order[j]=order[j],order[i]
  need(t=={'id':'FIRST_TIE_'+str(b['wins']),'fictional_date':'2022-04-18','origins_before':b['origins'],'first_order':order,'fisher_yates_steps':steps},'Returned tie differs from primitive drawing')
 pool=src[SEED]['nonplayoff_lottery_origins'];comb=list(combinations(range(1,15),4));ticket=[t for t,w in zip(pool,WEIGHTS)for _ in range(w)]+[None];won=[]
 for a,x in enumerate(d['lottery_attempts']):
  need(len(won)<4,'Extra draw after fourth accepted origin');left=list(range(1,15));balls=[];indices=[]
  for i in range(4):
   j=take('LOTTERY_'+str(a)+'_'+str(i),14-i);indices.append(j);balls.append(left.pop(j))
  c=sorted(balls);k=comb.index(tuple(c));t=ticket[k];ok=t is not None and t not in won
  expected={'attempt':a,'target_pick':len(won)+1,'ordered_balls':balls,'available_list_indices':indices,'combination':c,'combination_index0':k,'assigned_origin':t,'accepted_new_origin':ok,'discard_reason':None if ok else('UNASSIGNED'if t is None else'ALREADY_SELECTED')}
  need(x==expected,'Returned lottery attempt differs from source/primitive stream')
  if ok:won.append(t)
 need(cursor==len(values)and len(won)==4 and d['lottery_top4']==won and d['lottery_first14']==won+[t for t in pool if t not in won],'Selected draw result/remainder changed')

def exact_ranks(d,src):
 ranks={(1,t):i+1 for i,t in enumerate(d['lottery_first14'])};tie={x['id']:x['first_order']for x in d['ties']}
 for b in src[SEED]['first_round_nonlottery_origin_buckets']:
  order=tie[b['first_round_tie_order_parameter_reference']]if b['same_record_draft_drawing_required']else b['origins']
  for n,t in zip(b['possible_pre_draw_ranks'],order):ranks[(1,t)]=n
 for b in src[SEED]['second_round_origin_buckets']:
  order=list(reversed(tie[b['first_round_tie_order_parameter_reference']]))if b['second_round_tied_order_is_reverse_first']else b['origins']
  for n,t in zip(b['possible_pre_draw_ranks'],order):ranks[(2,t)]=n
 return ranks

def build(root=ROOT):
 src=sources(root);prov=primary();g=src[GLOBAL];s=src[SEED]
 need(len(g['rows'])==1230 and len(g['team_records'])==30,'Selected regular source counts changed')
 wins=Counter(x['selected_regulation_winner']for x in g['rows']);need(all(wins[t]==x['wins']and x['played']==82 for t,x in g['team_records'].items()),'Result/record source join differs')
 pool=s['nonplayoff_lottery_origins'];need(len(pool)==14 and len(set(pool))==14 and pool==sorted(pool,key=lambda t:wins[t]),'Lottery source ordering changed')
 need(len(set(wins[t]for t in pool))==14,'New lottery record tie needs averaged probability implementation')
 for b in s['first_round_nonlottery_origin_buckets']+s['second_round_origin_buckets']:need(all(wins[t]==b['wins']for t in b['origins']),'Bucket source record changed')
 d=draw_once(src);assert_draw(d,src);r=exact_ranks(d,src)
 # Validate rank constructor against independent source bucket memberships and
 # actual primitive-selected first/tie order, not another call to exact_ranks.
 need(set(r)=={(n,t)for n in (1,2)for t in wins}and all(sorted(v for(n,t),v in r.items()if n==round)==list(range(1 if round==1 else 31,31 if round==1 else 61))for round in (1,2)),'Exact ranks duplicate/missing')
 need([t for t in sorted(pool,key=lambda t:r[(1,t)])]==d['lottery_first14'],'Exact lottery ranks altered')
 for b in s['first_round_nonlottery_origin_buckets']:
  expected=next(x['first_order']for x in d['ties']if x['id']==b['first_round_tie_order_parameter_reference'])if b['same_record_draft_drawing_required']else b['origins']
  need([r[(1,t)]for t in expected]==b['possible_pre_draw_ranks'],'Exact nonlottery tie ranks altered')
 for b in s['second_round_origin_buckets']:
  need(sorted(r[(2,t)]for t in b['origins'])==b['possible_pre_draw_ranks'],'Exact second source bucket changed')
  if b['second_round_tied_order_is_reverse_first']:
   f=sorted(b['origins'],key=lambda t:r[(1,t)]);need([r[(2,t)]for t in f]==list(reversed(b['possible_pre_draw_ranks'])),'Second ranks not reversed first')
 csrc=control.sources(root);rows=control.allocation_family(r,csrc);control.assert_allocation(rows,r)
 expected={x['id']:x for x in src[FAMILY]['sixty_origin_control_functions']}
 for x in rows:need(x['current_public_family_holder']==expected[x['id']]['current_public_family_holder']and x['rule']==expected[x['id']]['rule'],'Exact selected allocation differs from reviewed family')
 for x in rows:x['working_exact_rank']=x.pop('rank_parameter');x['physical_NBA_rank_certified']=False
 prob=Fraction(1)
 for t in d['lottery_top4']:
  before=d['lottery_top4'][:d['lottery_top4'].index(t)];prob*=Fraction(WEIGHTS[pool.index(t)],1000-sum(WEIGHTS[pool.index(v)]for v in before))
 return {'id':'NBA_2022_SELECTED_WORKING_DRAW_AND_CONTROL','baseline_main':'bebabcf65be6af0d73d39b5a290249de52952397','status':'SELECTED_FICTIONAL_DRAW_AND_SIXTY_EXACT_WORKING_RANKS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,**control.PINS,SELF:sha(root/SELF)},'primary_provenance':prov,'selection':{'authority':'Existing delegated season-result/routine simulation scope; root adoption after independent review','public_seed':PUBLIC_SEED,'seed_announcement_before_first_execution':True,'seed_sha256':hashlib.sha256(PUBLIC_SEED.encode()).hexdigest(),'algorithm':'SHA256(seed|decimal counter);256-bit modulo rejection; Fisher-Yates ties; four sequential balls without replacement; return all14 after attempt','selected_draw_date':'2022-05-17','fictional_combination_assignment':'Lexicographic combinations; contiguous inverse-record weighted team slots; final11/12/13/14 unassigned','official_physical_NBA_combination_mapping_copied':False,'unassigned_combo_choice_is_fictional_isomorphic_mapping':True,'reroll_to_fit_outcome':False,'source_probability_not_estimated_by_this_one_draw':True,'lottery_tie_averaging_rule_checked_but_no_current_tie':True},'lottery_probability_inputs':[{'inverse_record_rank':i+1,'origin':t,'selected_wins':wins[t],'assigned_combinations':WEIGHTS[i],'first_pick_probability_fraction':str(Fraction(WEIGHTS[i],1000))}for i,t in enumerate(pool)],'drawing_trace':d,'top4_order_event_probability_fraction':str(prob),'tie_joint_order_probability_fraction':'1/48','probability_of_hypothetical_independent_seed_stream_not_physical_rng_certified':True,'exact_sixty_rank_and_holder_rows':sorted(rows,key=lambda x:(x['round'],x['working_exact_rank'])),'summary':{'origin_rows':60,'ranks_unique_each_round':30,'lottery_origins':14,'top4_selected':d['lottery_top4'],'lottery_attempts':len(d['lottery_attempts']),'tie_groups':len(d['ties']),'CHI_working_owned_ranks':[x['working_exact_rank']for x in rows if x['current_public_family_holder']=='CHI'],'new_draftees_UPCs_Tenders':0},'scope':{'fictional_working_draw_selected':True,'root_adoption_recorded':False,'independent_review_completed':False,'actual_2022_NBA_draw_or_historical_draft_certified':False,'future_rank_or_private_acceptance_certified':False,'new_author_lock':False,'title_MVP_or_season_winners_modified':False,'whole_macro3':False},'remaining_finite_inputs':['2022 draftee/legal participation choices and any required new Tender function use; no forced60UPCs.','2021–22 postseason and2022–23/2023 implementation remain separate.'],'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0,'manuscript':False}

def validate(v,root=ROOT):return []if v==build(root)else['Selected draw/control differs from source-bound reconstruction']
def markdown(v):
 s=v['selection'];lines=['# 2022 가상 추첨과 정확한 작업 순번','',v['status'],'',f"공개 seed `{s['public_seed']}`는 첫 실행 전에 루트에 전달했다. 동일 seed·counter를 재생하여 같은 결과를 검산한다. 원하는 결과를 얻기 위한 재추첨은 하지 않았다. 실제 NBA의 물리 추첨·원역사 선수 지명과는 별개이다.",'','## 원 규칙과 구현','','[2022 NBA 공식 확률·일정](https://pr.nba.com/2022-nba-draft-tiebreakers/)과 원 2019규약 PDF85–87을 직접 대조했다. [당대 Wizards 방식 설명](https://www.nba.com/wizards/nba-draft-lottery-2022-everything-you-need-know-about-wizards-odds), [Pacers 설명](https://www.nba.com/pacers/news/how-the-nba-draft-lottery-works)은 색인 본문 관측이며 정상 open은 iframe, 직접HTTP는403이다. 실패 bytes는 본문 증거가 아니다.','','현재 lottery14팀은 성적 동률이 없으므로 확률 평균 배분을 실행할 필요가 없다. 각 순위의 공식 가중치를 원선수·실제팀 대신 선택된 역성적순14원점에 적용한다. 1001개 사중조합의 동등 추첨, 미배정/이미 당첨된 원점의 무효 반복, 4당첨 뒤 미당첨 역성적순을 구현한다. 조합의 세부 소유배열은 명시 가상 lexicographic 배정이며 실제 NBA 배열을 읽었다고 주장하지 않는다.','','비lottery52승2팀과64승4팀은 별도 무작위 순열이다. 2라운드는 독립 추첨하지 않고 원 기록순·동률 first순서 역방향으로 연결한다. 난수 primitive와 모든 승인/기각 단계·선택 순열을 JSON에 기록했다.','','## 선택 결과','', '| 순번 | 원점 | 공개가족 수령자 |','|---|---|']
 for x in v['exact_sixty_rank_and_holder_rows']:lines.append(f"| {x['working_exact_rank']} | {x['origin']} | {x['current_public_family_holder']} |")
 lines+=['',f"CHI가 보유하는 작업 순번: {v['summary']['CHI_working_owned_ranks']}. 당첨top4의 순서 사건 확률은 `{v['top4_order_event_probability_fraction']}`이며 두tie의 공동순열 확률은1/48이다. 이는 새확률 추정·실제 난수기 인증이 아니다.",'','직접 caller 검문은 returned draw의 primitive digest/선택단계/남은순서, exactrank의 원bucket·역순,60수령자의 검문된 명명함수를 각각 대조한다. 조상 전체 constructor·원승패모델·192/2880배정을 재실행하지 않는다. 원CHI82·전리그1230 결과와 비용·명단·건강은 불변이다.','','작가잠금·선수/Tender/UPC·미래전달·실접수·전체macro3는 미승격이다. 독립 검문 뒤 루트가 이 작업선택을 채택할 수 있다.','','[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','','| 묶음 | 현황 |','|---|---|','| 1 | 완료 |','| 2 | 완료 |','| 3 | 전역1230/순위/play-in·공개60함수 완료, 가상draw 후속 검문 |','| 4 | 진행 |','| 5 | 진행 |','| 6 | 진행·Pack0 |','| 7 | 미완료 |','','미완료5 /6번까지4. v0.30 PARTIAL·CLOSED·원고0.',''];return '\n'.join(lines)

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if a.check:need(direct(ROOT,OUT)==v and text(ROOT/MD)==markdown(v),'Saved draw/control stale')
 n=0
 if a.self_test:
  orig=draw_once
  for fault in ('balls','winner'):
   def bad(src):
    d=deepcopy(orig(src))
    if fault=='balls':d['lottery_attempts'][0]['ordered_balls'][0]=99
    else:d['lottery_top4'][0]='TOR'
    return d
   try:
    with patch(__name__+'.draw_once',bad):build()
   except AssertionError:n+=1
   else:raise AssertionError('Returned selected draw accepted '+fault)
  original=exact_ranks
  def badr(d,src):
   r=original(d,src);r[(2,'CHI')],r[(2,'GSW')]=r[(2,'GSW')],r[(2,'CHI')];return r
  try:
   with patch(__name__+'.exact_ranks',badr):build()
  except AssertionError:n+=1
  else:raise AssertionError('Independent second draw silently introduced')
 print(json.dumps({'current':True,**v['summary'],'writer_negative_controls':n}))
if __name__=='__main__':main()
