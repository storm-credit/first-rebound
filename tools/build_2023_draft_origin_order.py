"""Finite 2023 origin ordering and one unadopted fictional lottery candidate.

No ancestor constructors, historical lottery winners, draftees or inferred owners.
"""
from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction
from itertools import combinations,permutations
from copy import deepcopy
from unittest.mock import patch
import argparse,hashlib,json,math,fitz

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2023_draft_origin_order.py'
OUT='simulation/NBA_2023_DRAFT_ORIGIN_ORDER.json';MD=OUT[:-5]+'.md'
GLOBAL='simulation/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS.json'
SEED='simulation/NBA_2022_23_STANDINGS_AND_2023_PLAYIN.json'
SLOT='research/CHICAGO_2023_FIRST_ROUND_SLOT_16_2026_10_08.json'
CLAIMS='research/CHICAGO_2023_NAMED_DRAFT_CLAIMS_AND_COST_PORTS_2026_10_08.json'
PEER='reviews/CHI_2023_FIRST_ROUND_SLOT_DEN_INDEPENDENT_REVIEW_2026_10_08.json'
FILES=(GLOBAL,SEED,SLOT,CLAIMS,PEER)
PINS={'simulation/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS.json': '8e2a778fe646de3c6070be7dd3acc64199fe2a7c813e780916e380b099fa3889', 'simulation/NBA_2022_23_STANDINGS_AND_2023_PLAYIN.json': 'cecefbc4fbca8378cacdae2f77129f26644244529d11eb216072a8fba8d224a9', 'research/CHICAGO_2023_FIRST_ROUND_SLOT_16_2026_10_08.json': 'abbcdaaa6ff14d277f88d47fa600320fc6458ec4b057e5a7b73b414b6fbabf30', 'research/CHICAGO_2023_NAMED_DRAFT_CLAIMS_AND_COST_PORTS_2026_10_08.json': 'b139af4af09a48dd1c9e345d17d05fc8e38f4cb021193f32bc3a09ed537f49e3', 'reviews/CHI_2023_FIRST_ROUND_SLOT_DEN_INDEPENDENT_REVIEW_2026_10_08.json': '6b5e50993b2d916c8fdc15fc9db389118fee19c1bacb4db3485103fa0e48c7e6'}
PUBLIC_SEED='first-rebound|2023-draft-origin|candidate-v1|2026-10-08'
FIXED_SEED=PUBLIC_SEED
WEIGHTS=(140,140,140,125,105,90,75,60,45,30,20,15,10,5)
BYLAWS=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-2019-bylaws.pdf')
RAW_SHA='6accb3d9633e15e8559d13228c27ae7b3b0b81eac0894050b06256eea6da3464'
PAGE_SHA={85:'312b5df737e0460a3671e61291f403b9488ee32827d938cebea87867f3bf0239',86:'b39fe3c49719251a389390384fe243b457b50716a1f456c7e34f8771d07093f0',87:'43197a4945acf5176d9335d2ff911f7c516a1db82e623c4ca53bb264fc094e20'}
CAPTURE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-2023-draft-origin-20261008/sources.json')
META_SHA='18e4bd59036000a689c6bd46314b66fb817fc814ffe20a438697f7bd6976aa64'
OFFICIAL_URL='https://pr.nba.com/ties-broken-for-order-of-selection-in-nba-draft-2023-presented-by-state-farm/'

def need(x,m):
 if not x:raise AssertionError(m)
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(root,p):return json.loads(text(root/p))
def sources(root):
 need(PUBLIC_SEED==FIXED_SEED and WEIGHTS==(140,140,140,125,105,90,75,60,45,30,20,15,10,5),'Announced seed/primary weights changed')
 s={}
 for p in FILES:
  need(sha(root/p)==PINS[p],'Origin source stale '+p)
  v=load(root,p);need(v==json.loads(text(root/p)),'Returned source differs from physical '+p);s[p]=v
 return s
def primary():
 need(hashlib.sha256(BYLAWS.read_bytes()).hexdigest()==RAW_SHA,'Bylaws raw changed')
 with fitz.open(BYLAWS) as d:
  for i,h in PAGE_SHA.items():need(hashlib.sha256(d[i-1].get_text().encode()).hexdigest()==h,'Bylaws page changed')
 need(hashlib.sha256(CAPTURE.read_bytes()).hexdigest()==META_SHA,'Capture metadata changed')
 failed=json.loads(text(CAPTURE))
 for r in failed:need(r['HTTP_status']==403 and hashlib.sha256(Path(r['cache_path']).read_bytes()).hexdigest()==r['raw_sha256'] and r['actual_body_adopted'] is False,'Failed bytes misclassified')
 return {'Bylaws':{'url':'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf','raw_cache':str(BYLAWS),'raw_sha256':RAW_SHA,'PDF1based_text_SHA256':{str(i):h for i,h in PAGE_SHA.items()},'sections':'7.02(a)(b)(c)','direct_raw_and_text_read':True},
  'official_2023_web_observation':{'url':OFFICIAL_URL,'release_date':'2023-04-17','direct_web_body_read':True,'raw_body_acquired':False,'locators':'paragraphs before first table; first14 odds table; second table lottery ties shown as conditional ranks','observed_top4_then_inverse_records_and_random_ties':True,'historical_team_winners_owners_or_rank_order_consumed':False},
  'method_2023_official_indexed_observation':{'url':'https://www.nba.com/pacers/news/explaining-the-nba-draft-lottery-what-are-the-pacers-chances-of-landing-the-1-pick','indexed_body_observed':True,'normal_open':'IFRAME_ONLY','raw_body_acquired':False,'facts':'14 balls;1001 four-ball combinations;1000 assigned;ties pool weights with drawing winner taking any odd remainder'},
  'failed_HTTP_captures':failed,'current_2026_explainer_is_original_2023_evidence':False}

class Stream:
 def __init__(self):self.counter=0;self.events=[]
 def below(self,n,label):
  while True:
   h=hashlib.sha256((PUBLIC_SEED+'|'+str(self.counter)).encode()).hexdigest();v=int(h,16);ok=v<2**256-(2**256%n)
   self.events.append({'counter':self.counter,'label':label,'n':n,'digest':h,'accepted':ok,'value':v%n if ok else None});self.counter+=1
   if ok:return v%n

def buckets(wins):
 b=defaultdict(list)
 for t,w in wins.items():b[w].append(t)
 return [{'wins':w,'origins':sorted(b[w])} for w in sorted(b)]
def tie_and_weights(bs,lottery,r):
 ties=[];orders={}
 for b in bs:
  ts=list(b['origins']);steps=[]
  for i in reversed(range(1,len(ts))):
   j=r.below(i+1,'TIE_'+str(b['wins'])+'_'+str(i));steps.append({'i':i,'j':j});ts[i],ts[j]=ts[j],ts[i]
  orders[str(b['wins'])]=ts
  if len(ts)>1:ties.append({'wins':b['wins'],'origins_before':b['origins'],'prelottery_first_tie_order':ts,'steps':steps})
 pool=[t for b in bs for t in orders[str(b['wins'])] if t in lottery];weights={};cursor=0;weightgroups=[]
 for b in bs:
  ts=[t for t in orders[str(b['wins'])] if t in lottery]
  if not ts:continue
  need(set(ts)==set(b['origins']),'Mixed playoff/lottery record tie needs specific governing allocation')
  n=len(ts);total=sum(WEIGHTS[cursor:cursor+n]);base,extra=divmod(total,n)
  for i,t in enumerate(ts):weights[t]=base+(i<extra)
  weightgroups.append({'wins':b['wins'],'origins_in_drawn_tie_order':ts,'nominal_inverse_record_weights':list(WEIGHTS[cursor:cursor+n]),'pooled_combinations':total,'equal_base':base,'odd_remainder_awarded_in_draw_order':extra});cursor+=n
 need(cursor==14 and sum(weights.values())==1000,'Assigned combinations total')
 return ties,orders,pool,weights,weightgroups

def draw(bs,lottery):
 r=Stream();ties,orders,pool,w,groups=tie_and_weights(bs,lottery,r)
 combos=list(combinations(range(1,15),4));tickets=[t for t in pool for _ in range(w[t])]+[None];won=[];attempts=[]
 while len(won)<4:
  need(len(attempts)<10000,'Bounded lottery failure; do not reseed')
  left=list(range(1,15));balls=[]
  for i in range(4):balls.append(left.pop(r.below(14-i,'BALL_'+str(len(attempts))+'_'+str(i))))
  c=sorted(balls);k=combos.index(tuple(c));t=tickets[k];ok=t is not None and t not in won
  attempts.append({'attempt':len(attempts),'target_rank':len(won)+1,'ordered_balls':balls,'combination':c,'index0':k,'origin':t,'accepted':ok,'discard':None if ok else ('UNASSIGNED' if t is None else 'ALREADY_WON')})
  if ok:won.append(t)
 return {'rng':r.events,'ties':ties,'prelottery_orders':orders,'inverse_record_lottery_order':pool,'assigned_weights':w,'pooled_weights':groups,'attempts':attempts,'top4':won,'first14':won+[t for t in pool if t not in won]}

def assert_draw(d,bs,lottery):
 events=d['rng'];values=[]
 for i,e in enumerate(events):
  need(e['counter']==i and type(e['n']) is int and e['n']>0,'Counter/range changed')
  h=hashlib.sha256((PUBLIC_SEED+'|'+str(i)).encode()).hexdigest();q=int(h,16);ok=q<2**256-(2**256%e['n'])
  need(e['digest']==h and e['accepted']==ok and e['value']==(q%e['n'] if ok else None),'Primitive hash/value changed')
  if ok:values.append((e['label'],e['n'],e['value']))
 cursor=0
 def take(label,n):
  nonlocal cursor
  need(cursor<len(values),'Missing random event');v=values[cursor];cursor+=1;need(v[:2]==(label,n),'Random event stage changed');return v[2]
 ties=[];orders={}
 for b in bs:
  order=list(b['origins']);steps=[]
  for i in reversed(range(1,len(order))):
   j=take('TIE_'+str(b['wins'])+'_'+str(i),i+1);steps.append({'i':i,'j':j});order[i],order[j]=order[j],order[i]
  orders[str(b['wins'])]=order
  if len(order)>1:ties.append({'wins':b['wins'],'origins_before':b['origins'],'prelottery_first_tie_order':order,'steps':steps})
 pool=[t for b in bs for t in orders[str(b['wins'])] if t in lottery];weights={};groups=[];offset=0
 for b in bs:
  ts=[t for t in orders[str(b['wins'])] if t in lottery]
  if not ts:continue
  total=sum(WEIGHTS[offset:offset+len(ts)]);base,extra=divmod(total,len(ts))
  for i,t in enumerate(ts):weights[t]=base+int(i<extra)
  groups.append({'wins':b['wins'],'origins_in_drawn_tie_order':ts,'nominal_inverse_record_weights':list(WEIGHTS[offset:offset+len(ts)]),'pooled_combinations':total,'equal_base':base,'odd_remainder_awarded_in_draw_order':extra});offset+=len(ts)
 need(d['ties']==ties and d['prelottery_orders']==orders and d['assigned_weights']==weights and d['inverse_record_lottery_order']==pool and d['pooled_weights']==groups,'Returned tie/weight meaning altered')
 combos=list(combinations(range(1,15),4));tickets=[t for t in pool for _ in range(weights[t])]+[None];won=[]
 for a,x in enumerate(d['attempts']):
  need(len(won)<4,'Draw after top4');left=list(range(1,15));balls=[left.pop(take('BALL_'+str(a)+'_'+str(i),14-i)) for i in range(4)]
  c=sorted(balls);k=combos.index(tuple(c));t=tickets[k];ok=t is not None and t not in won
  need(x=={'attempt':a,'target_rank':len(won)+1,'ordered_balls':balls,'combination':c,'index0':k,'origin':t,'accepted':ok,'discard':None if ok else ('UNASSIGNED' if t is None else 'ALREADY_WON')},'Returned lottery event altered')
  if ok:won.append(t)
 need(cursor==len(values) and len(won)==4 and d['top4']==won and d['first14']==won+[t for t in pool if t not in won],'Returned top4/remainder altered')

def origin_rows(bs,d,lottery):
 first=list(d['first14'])+[t for b in bs for t in d['prelottery_orders'][str(b['wins'])] if t not in lottery]
 ranks={t:i+1 for i,t in enumerate(first)}
 # §7.02(c): reverse the order in which tied teams selected in FIRST,
 # including a lottery upset; not just the preliminary tie coin order.
 second=[t for b in bs for t in sorted(b['origins'],key=lambda t:ranks[t],reverse=True)]
 return [{'round':rd,'origin':t,'potential_origin_rank':i+start,'public_holder':None,'sanction_or_forfeiture_applied':False,'draftee_UPC_Tender_selected':False} for rd,ts,start in ((1,first,1),(2,second,31)) for i,t in enumerate(ts)]
def assert_rows(rows,bs,d,lottery):
 need(len(rows)==60 and all(len({x['origin'] for x in rows if x['round']==rd})==30 for rd in (1,2)),'Origin 30+30 domain')
 first=d['first14']+[t for b in bs for t in d['prelottery_orders'][str(b['wins'])] if t not in lottery];fr={t:i+1 for i,t in enumerate(first)}
 second=[]
 for b in bs:second.extend(sorted(b['origins'],key=lambda t:fr[t],reverse=True))
 for rd,order,start in ((1,first,1),(2,second,31)):
  rs=[x for x in rows if x['round']==rd]
  need(rs==[{'round':rd,'origin':t,'potential_origin_rank':i+start,'public_holder':None,'sanction_or_forfeiture_applied':False,'draftee_UPC_Tender_selected':False} for i,t in enumerate(order)],'Returned origin/order/rights scope altered')
 need(fr['CHI']==16,'Reviewed Chicago16 origin changed')

def joint(w,bs,d):
 # Entire ordered top4 law. Invalid/unassigned/repeated tickets integrate out.
 # Conditional on a tie permutation, P(t1..t4)=product w/(1000-used).
 mass=Fraction(0);marg={t:[Fraction(0) for _ in range(4)] for t in w};count=0
 for path in permutations(w,4):
  p=Fraction(1);used=0
  for t in path:p*=Fraction(w[t],1000-used);used+=w[t]
  mass+=p;count+=1
  for i,t in enumerate(path):marg[t][i]+=p
 need(count==24024 and mass==1 and all(sum(v[i] for v in marg.values())==1 for i in range(4)),'Joint probability incomplete')
 tie_states=math.prod(math.factorial(len(b['origins'])) for b in bs)
 p=Fraction(1);used=0
 for t in d['top4']:p*=Fraction(w[t],1000-used);used+=w[t]
 return {'representation':'EXACT_FACTORIZED_FULL_JOINT_NOT_ONE_DRAW_ESTIMATE','all_distinct_ordered_top4_paths':count,'tie_permutation_states':tie_states,'full_joint_states':count*tie_states,'joint_probability_formula':'(product over tied record buckets 1/|bucket|!) * product_{i=1..4} weight(t_i)/(1000-sum_{j<i}weight(t_j)); weights determined by pooled odds + tie permutation','top4_probability_mass_fraction':str(mass),'tie_probability_mass_fraction':'1','candidate_top4_probability_conditional_on_ties':str(p),'candidate_complete_ties_and_top4_probability':str(p/tie_states),'top4_position_marginals_conditioned_on_drawn_tie_weight_allocation':{t:[str(v) for v in q] for t,q in marg.items()},'remaining_first_order_function':'top4 then undrawn inverse-record origins in drawn tie priority','second_order_function':'all30 inverse-record; each same-record bucket reverses its ACTUAL candidate first-round selection order','physical_NBA_rng_or_combination_mapping_certified':False}

def assert_joint(v,w,bs,d):
 # Independent subset-state DP, not another call to the ordered-path producer.
 stage={frozenset():Fraction(1)};marg={t:[Fraction(0) for _ in range(4)] for t in w}
 for k in range(4):
  nxt=defaultdict(Fraction)
  for selected,p in stage.items():
   denominator=1000-sum(w[t] for t in selected)
   for t in w:
    if t in selected:continue
    q=p*Fraction(w[t],denominator);marg[t][k]+=q;nxt[selected|{t}]+=q
  stage=nxt
 need(sum(stage.values())==1 and v['top4_position_marginals_conditioned_on_drawn_tie_weight_allocation']=={t:[str(q) for q in values] for t,values in marg.items()},'Returned joint marginals differ from independent subset law')
 n=math.prod(math.factorial(len(b['origins'])) for b in bs);p=Fraction(1);used=0
 for t in d['top4']:p*=Fraction(w[t],1000-used);used+=w[t]
 expected={'representation':'EXACT_FACTORIZED_FULL_JOINT_NOT_ONE_DRAW_ESTIMATE','all_distinct_ordered_top4_paths':24024,'tie_permutation_states':n,'full_joint_states':24024*n,'joint_probability_formula':'(product over tied record buckets 1/|bucket|!) * product_{i=1..4} weight(t_i)/(1000-sum_{j<i}weight(t_j)); weights determined by pooled odds + tie permutation','top4_probability_mass_fraction':'1','tie_probability_mass_fraction':'1','candidate_top4_probability_conditional_on_ties':str(p),'candidate_complete_ties_and_top4_probability':str(p/n),'top4_position_marginals_conditioned_on_drawn_tie_weight_allocation':{t:[str(q) for q in values] for t,values in marg.items()},'remaining_first_order_function':'top4 then undrawn inverse-record origins in drawn tie priority','second_order_function':'all30 inverse-record; each same-record bucket reverses its ACTUAL candidate first-round selection order','physical_NBA_rng_or_combination_mapping_certified':False}
 need(v==expected,'Returned joint probability/scope changed')

def build(root=ROOT):
 s=sources(root)
 for p in FILES:need(sha(root/p)==PINS[p] and s[p]==json.loads(text(root/p)),'Returned consumed physical input changed '+p)
 prov=primary();g=s[GLOBAL];wins=Counter(r['winner'] for r in g['rows']);played=Counter(t for r in g['rows'] for t in (r['home'],r['away']))
 need(len(g['rows'])==1230 and len(wins)==30 and set(played.values())=={82} and wins==Counter({t:r['wins'] for t,r in g['team_records'].items()}),'Source regular results/records differ')
 qualified={x['team'] for rs in s[SEED]['final_playoff_seeds'].values() for x in rs};lottery=set(s[SEED]['nonplayoff_lottery_origins'])
 need(len(qualified)==16 and len(lottery)==14 and qualified.isdisjoint(lottery) and qualified|lottery==set(wins),'14/16 qualification changed')
 need(s[SLOT]['Chicago_origin_first_slot']==16 and s[SLOT]['Chicago_selected_holder']=='CHI' and s[PEER]['independent_review_completed'],'Chicago16 reviewed anchor')
 bs=buckets(wins);d=draw(bs,lottery);assert_draw(d,bs,lottery);rows=origin_rows(bs,d,lottery);assert_rows(rows,bs,d,lottery)
 probs=joint(d['assigned_weights'],bs,d);assert_joint(probs,d['assigned_weights'],bs,d)
 claims=deepcopy(s[CLAIMS]['named_claims'][:2]);need([(x['origin'],x['round'],x['selected_holder']) for x in claims]==[('CHI',1,'CHI'),('CHI',2,'WAS')],'Named claims changed')
 for c in claims:c['candidate_origin_rank']=next(x['potential_origin_rank'] for x in rows if x['round']==c['round'] and x['origin']==c['origin']);c['new_2023_draw_canon_adoption']=False
 return {'id':'NBA_2023_DRAFT_ORIGIN_ORDER','baseline_main':'241821ba24936ee788320844822af5a3f32ef69c','status':'DRAW_CANDIDATE_AND_SIXTY_ORIGIN_ORDERS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_provenance':prov,'candidate_policy':{'seed':PUBLIC_SEED,'seed_announced_before_first_execution':True,'fictional_tie_date':'2023-04-17','fictional_lottery_date':'2023-05-16','candidate_only_root_adoption_before_canon_required':True,'algorithm':'SHA256(seed|counter), modulo rejection, Fisher-Yates tie permutations,4 distinct balls/attempt,discard unassigned/repeated origin','lexicographic_combination_mapping_is_new_fiction':True,'outcome_fitting_rerolls':0},'selected_regular_records_preserved':deepcopy(g['team_records']),'playoff_origins':sorted(qualified),'lottery_origins':sorted(lottery),'inverse_record_buckets':bs,'lottery_joint_distribution':probs,'drawing_candidate':d,'potential_sixty_origin_orders':rows,'known_Chicago_claim_ports':claims,'summary':{'first_origins':30,'second_origins':30,'lottery_origins':14,'playoff_origins':16,'tie_buckets':len(d['ties']),'candidate_top4':d['top4'],'CHI_first_origin_rank':16,'CHI_second_origin_rank_to_WAS':claims[1]['candidate_origin_rank'],'actual_2023_draw_results_copied':0},'certification':{'origin_and_probability_functions_complete':True,'candidate_draw_executed_for_review':True,'fictional_draw_selected_or_canon_adopted':False,'independent_review_completed':False,'all60_public_holders_or_sanctions_certified':False,'actual_NBA_2023_draw_certified':False,'draftee_UPC_Tender_selected':False,'title_MVP_core_or_season_results_changed':False,'whole_macro3_complete':False,'manuscript_allowed':False},'remaining_named_ports':['Root review/adoption of candidate draw; does not condition known CHI16 on unrelated lottery adoption.','Public holder/conditional prior-right/sanction functions for each actually consumed non-CHI claim; no assumed actual 58-pick forfeitures.','CHI16 draftee/price and WAS-owned CHI second are separate downstream consumers.'],'unfinished_macro_groups':5,'unfinished_through_6':4,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0}

def md(v):
 lines=['# 2023 드래프트 원점 순서 · 가상 추첨 후보','','검문된1230 경기·16 PO/14 로터리를 사용한다. 정규 동률 대진순위와 드래프트 순열을 구분하며 CHA/WAS 미해결 점수차는 draft drawing을 막지 않는다.','',f"첫 실행 전 공개한 seed: `{PUBLIC_SEED}`. 원하는 결과로 다시 뽑지 않았다. 이번 결과는 **후보**이며 root 검문·채택 전 정본화0이다.",'',f'[원2023 NBA 발표]({OFFICIAL_URL})의 top4/기록순/동률추첨과 원2019규약PDF85–87§7.02를 직접 대조했다. 공식본문은 web관측이고 직접HTTP403 bytes는 실패로만 보존했다. NBA 실제2023 당첨팀·원순번·후대보유자·제재를 복사하지 않았다.','',
 'CHA/WAS14승은 inverse-record4·5의125+105개를 공동배분해 각115개다. 다른 네 PO 동률군과 함께 공정순열을 기록했다. 2R은 로터리 당첨 이후 **실제 가상1R 선택순서**의 역순이다. 선행coin순서만 뒤집으면 로터리upset 때 규약과 어긋난다.','',f"전체 top4 ordered 경로24,024개·동률순열{v['lottery_joint_distribution']['tie_permutation_states']}개 공동법칙을 정확한 factorization으로 보존한다. 모든top4경로 확률합1을 Fraction으로 계산했다. 이 한seed가 확률 추정이나 물리난수기 인증은 아니다.",'','| 잠재순번 | 원점 | 공개보유자 |','|---|---|---|']
 for x in v['potential_sixty_origin_orders']:lines.append(f"| {x['potential_origin_rank']} | {x['origin']} | 미평가 |")
 lines+=['',f"Chicago 자체1R은 검문된16번으로 불변이다. CHI원점2R의 후보순번은{v['summary']['CHI_second_origin_rank_to_WAS']}이며 명명된 보유자는WAS다. 전체60 보유권·제재 집행은 이 원점순서의 인증범위가 아니다. 선수·UPC·Tender·가격·우승/MVP/core 선택0.",'','## 남은 유한 입력','']+['- '+x for x in v['remaining_named_ports']]
 lines+=['','[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','','| 묶음 | 상태 |','|---|---|','| 1 | 완료 |','| 2 | 완료 |','| 3 | 진행 |','| 4 | 진행 |','| 5 | 대기 |','| 6 | 대기 |','| 7 | CLOSED |','','미완료큰묶음5 /6번까지4 · v0.30 PARTIAL · CLOSED · Pack0 · 원고0.']
 return '\n'.join(lines)+'\n'
def validate(v,root=ROOT):
 try:return [] if v==build(root) else ['Saved origin candidate differs from physical reconstruction']
 except (AssertionError,KeyError,ValueError) as e:return [str(e)]
def self_test():
 labels=[]
 def reject(n):
  try:build()
  except (AssertionError,KeyError,ValueError):labels.append(n);return
  raise AssertionError('FALSE_PASS '+n)
 old=draw
 def bad(bs,lot):
  d=old(bs,lot);d['assigned_weights']['CHA']+=1;return d
 with patch(__name__+'.draw',side_effect=bad):reject('returned_pooled_weight')
 oldrows=origin_rows
 def second(bs,d,lot):
  rs=oldrows(bs,d,lot);a,b=[x for x in rs if x['round']==2 and x['origin'] in ('CHA','WAS')];a['potential_origin_rank'],b['potential_origin_rank']=b['potential_origin_rank'],a['potential_origin_rank'];return rs
 with patch(__name__+'.origin_rows',side_effect=second):reject('returned_second_not_reverse_actual_first')
 oldsource=sources
 def source(root):
  s=oldsource(root);s[GLOBAL]['team_records']['CHI']['wins']=47;return s
 with patch(__name__+'.sources',side_effect=source):reject('returned_record')
 oldjoint=joint
 def marginal(w,bs,d):
  v=oldjoint(w,bs,d);v['top4_position_marginals_conditioned_on_drawn_tie_weight_allocation']['CHA'][0]='1';return v
 with patch(__name__+'.joint',side_effect=marginal):reject('returned_joint_marginal')
 return labels
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(md(v),encoding='utf-8')
 if a.check:need(not validate(load(ROOT,OUT)) and text(ROOT/MD)==md(v),'Saved origin/MD stale')
 r={'current':True,**v['summary']}
 if a.self_test:r['writer_negative_controls']=self_test()
 print(json.dumps(r))
if __name__=='__main__':main()
