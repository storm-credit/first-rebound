"""Prepare substantive current episode repairs; never certify prose or own review."""
import argparse, copy, hashlib, json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OLD='design/THREEPEAT_51_PREPARED_EPISODE_BLUEPRINTS_2026_10_12.json'
HISTORY='design/THREEPEAT_CURRENT_USED_HISTORY_EXIT_JOIN_2026_10_12.json'
LATE='canon/DELEGATED_THREEPEAT_2024_25_USED_ROUTES_AND_FINAL_COURTS_SELECTION_2026_10_09.json'
EAST='simulation/THREEPEAT_2024_25_SIX_EAST_USED_COURT_JOIN_2026_10_09.json'
C01='canon/C01_GOLD_USED_CALENDAR_SELECTED_EXECUTION_2026_10_12.json'
ARC='canon/CHARACTER_RESPONSIBILITY_ARC.md'
ACCESS='design/THREEPEAT_CURRENT_SCENE_ACCESS_SELECTION_2026_10_12.json'
OUT='design/THREEPEAT_61_CURRENT_REPAIRED_DESIGN_2026_10_12.json'
UNITS=[f'M{i:02}' for i in range(1,10)]+['EPI']
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256((ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').encode()).hexdigest()
def ref(p,pointer='',text=False):
 d={'path':p,'source_sha256':sha(p),'json_pointer':pointer}
 if text:d.update(format='UTF8_TEXT',text_locator={'kind':'WHOLE_TEXT'})
 return d
def split(base,title,window,entry,action,cost,exit,refs):
 b=copy.deepcopy(base)
 for k in ['named_acquisition_checkpoints','information_boundary','claims']:
  b.pop(k,None)
 b.update(title=title,timeline_window=window,entry_state=entry,action_choice=action,
  durable_cost=cost,state_change=exit,source_refs=base['source_refs']+refs,
  density_reason='Distinct current role/pressure/response or observed progression; no invented score/shotclock/clinical cause; no per-game filler quota.')
 return b
def selected_access(b,number):
 selected=load(ACCESS);plan=selected['rows'][number-1]
 assert plan['episode']==number and plan.get('end_observation_text') and plan.get('entry_observation_text'),'Safe observations not supplied'
 claims=[];segments=[];witnesses=[]
 def claim(body,kind,refs):
  i=len(claims);claims.append({'text':body,'status':'AUTHOR_MODELED_DESIGN','temporal_kind':kind,
   'source_refs':refs,'requires_selected_choice_ids':b['consequential_choice_ids']});return i
 def scene(sid,order,when,indexes,kind,method,prior=False):
  segments.append({'segment_id':sid,'scene_order':order,'pov_character':'PROTAGONIST',
   'literal_when':when,'known_claim_indexes':indexes})
  witnesses.append({'segment_id':sid,'owner':'PROTAGONIST','scene_order':order,
   'acquired_order':0 if prior else order,'event_order':0 if prior else order if kind=='OBSERVED_EVENT' else None,
   'knowledge_kind':kind,'claim_indexes':indexes,'access_method':method,'literal_when':when})
 entry=claim(plan['entry_observation_text'],'OBSERVED_EVENT',[ref(ACCESS,'/rows/'+str(number-1)+'/entry_observation_text')]+b['source_refs'])
 scene('ENTRY',1,'회차진입;이미관찰/전달된직전상태',[entry],'OBSERVED_EVENT',
       '본인이이전참여/담당안내로이미알게된상태: '+plan['entry_observation_text'],True)
 intention=claim(plan['plan_text'],'CURRENT_PLAN',[ref(ACCESS,'/rows/'+str(number-1)+'/plan_text')]+b['source_refs'])
 scene('OWN_INTENTION',2,'해당수행전현재자기선택',[intention],'CURRENT_PLAN','현재자기선택: '+plan['plan_text'])
 order=2;linked=[];emitted_follow=set()
 def follow(fi):
  nonlocal order
  f=plan['follow_on_own_intentions'][fi];body=f['plan_text'];order+=1
  i=claim(body,'CURRENT_PLAN',[ref(ACCESS,'/rows/'+str(number-1)+'/follow_on_own_intentions/'+str(fi))]+b['source_refs'])
  scene('FOLLOW_ON_'+str(fi+1),order,f['available_only_after'],[i],'CURRENT_PLAN','앞관측을받은뒤현재자기계획: '+body)
  emitted_follow.add(fi)
 for mi,m in enumerate(selected['checkpoint_stage_map']):
  if m['episode']!=number:continue
  obs=m.get('expanded_sequential_observations') or [m]
  if m.get('must_expand_internal_action_order'):
   obs=[{'stage':'CHRONOLOGICAL_ACTION','literal_when':'2025Jun22remaining'+clock,
     'known_observation':body,'source_ref':{'path':LATE,'json_pointer':'/selected_2025_last_attack'}}
    for clock,body in [
     ('16.1','자신이LaMelo에게첫패스를릴리스했다.'),('15.6','LaMelo가첫패스를받은외형을본다.'),('12.8','LaMelo가자신에게공을반환하는것을본다.'),
     ('12.5','자신이반환된공을잡았다.'),('11.9','자신이Carter에게이양했다.'),('11.5','Carter가공을받은것을본다.'),
     ('9.6','공없이현재닫힌경로에서다시참여하려움직인다.'),('9.0','Carter가자신에게공을반환하는것을본다.'),
     ('8.6','자신이공을다시잡았다.'),('4.4','LaMelo의현재재배치위치를본다.'),('2.6','자신이현재LaMelo에게마지막공을넘긴다.'),
     ('2.0','LaMelo가공을받은것을본다.'),('1.3','LaMelo의드리블을본다.'),('1.0','드리블공이돌아오는외형을본다.'),
     ('0.8','LaMelo의수집동작을본다.'),('0.6/0.4','수집뒤두걸음이순서대로일어나는외형을본다.')]]
  for oi,o in enumerate(obs):
   extra=[]
   if 'source_ref' in o:extra=[ref(o['source_ref']['path'],o['source_ref']['json_pointer'])]
   i=claim(o['known_observation'],'OBSERVED_EVENT',[ref(ACCESS,'/checkpoint_stage_map/'+str(mi))]+b['source_refs']+extra)
   sid=f'CP{m["checkpoint_order"]}_{oi+1}'
   if o['stage']=='ENTRY':
    segments[0]['known_claim_indexes'].append(i)
    witnesses.append({'segment_id':'ENTRY','owner':'PROTAGONIST','scene_order':1,'acquired_order':0,'event_order':0,
     'knowledge_kind':'OBSERVED_EVENT','claim_indexes':[i],'literal_when':o['literal_when'],
     'access_method':'진입전에이미참여하거나본인에게전달된사항: '+o['known_observation']})
    sid='ENTRY'
   else:
    order+=1;scene(sid,order,o['literal_when'],[i],'OBSERVED_EVENT',
     '표시된사건/경기종료후본인의직접관찰또는해당기관/에이전트의전달: '+o['known_observation'])
   linked.append({'parent_checkpoint_order':m['checkpoint_order'],'actual_segment_id':sid,
    'claim_index':i,'literal_when':o['literal_when']})
   if number==60:
    if m['checkpoint_order']==4:follow(0)
    if m['checkpoint_order']==6 and o['literal_when']=='2025Jun22remaining11.5':follow(1)
    if m['checkpoint_order']==6 and o['literal_when']=='2025Jun22remaining4.4':follow(2)
 if plan.get('follow_on_trigger_observation'):
  trigger=plan['follow_on_trigger_observation'];order+=1
  ti=claim(trigger['text'],'OBSERVED_EVENT',[ref(ACCESS,'/rows/'+str(number-1)+'/follow_on_trigger_observation')]+b['source_refs'])
  scene('FOLLOW_ON_TRIGGER_OBSERVATION',order,trigger['literal_when'],[ti],'OBSERVED_EVENT','관측이먼저완료됨: '+trigger['text'])
  for fi in range(len(plan.get('follow_on_own_intentions',[]))):
   if fi not in emitted_follow:follow(fi)
 order+=1
 end=claim(plan['end_observation_text'],'OBSERVED_EVENT',[ref(ACCESS,'/rows/'+str(number-1)+'/end_observation_text')]+b['source_refs'])
 scene('END_OBSERVATION',order,'해당회차의마지막사용사건이종료된뒤',[end],'OBSERVED_EVENT',
  '종료뒤직접관찰/자기수행·공개안내의한정결과: '+plan['end_observation_text'])
 for fi in range(len(plan.get('follow_on_own_intentions',[]))):
  if fi not in emitted_follow:
   assert number not in [60,61],'Timed follow-on intention not placed at its actual gate'
   follow(fi)
 b['entry_state_scope']='NONDIEGETIC_AUTHOR_BOUNDARY;ACTOR_USES_ONLY_SAFE_ENTRY_OBSERVATION'
 b['action_choice_scope']='NONDIEGETIC_AUTHOR_CHRONOLOGY_NOT_AN_ACTOR_CLAIM_OR_FUTURE_KNOWLEDGE'
 b['state_change_scope']='AUTHOR_OUTCOME_PLUS_EDITORIAL_GUARDS;ACTOR_USES_ONLY_SAFE_END_OBSERVATION'
 b['claims']=claims;b['checkpoint_claim_consumption']=linked
 b['information_boundary']={'status':'CURRENT_REPAIRED_ACCESS_PENDING_INDEPENDENT_ACCEPTANCE',
  'pov_character':'PROTAGONIST','clock_basis':b['timeline_window']+';진입·자기현재선택·날짜별사건후관측·종료관측을별도로취득',
  'scene_segments':segments,'access_witnesses':witnesses,'prose_access_verified':False,
  'editorial_metadata_is_not_character_knowledge':True}
def build():
 old=load(OLD)['prepared_episode_blueprints'];rows=[]
 for number,base in enumerate(old,1):
  if number==45:
   common=[ref(LATE,'/selected_seasons/0'),ref(EAST,'/six_game_candidates')]
   variants=[
    ('방어 준비에서 비운 자리','2023–24 기존정규역할→2024ATL진입전',base['entry_state'],
     '복귀 뒤 전달된 제한 역할을 재확인하고, 귀국 교육으로 자신이 비운34분을 맡은 Jaquez·Duarte·Caruso·Green의 별도 수행을 영상·담당 설명으로 확인한다. 코치가 역할을 배정하며 주인공은 놓친 조합 반복부터 요청한다.',
     '한국 교육·봉사 귀국 창에는NBA분0이며 동료가34분과 준비 노동을 맡는다. 복귀는 잃은 반복을 돌려주지 않는다.',
     '기존 동부2위의 방어 진입은 남고, 자신의 부재 비용을 인정한 현재 과제가 생긴다. ATL결과는 아직 모른다.'),
    ('Atlanta의 첫 통로','2024년4월20–30일ATL5경기',
     '동부2위의 기존 진입과 전달된 역할만 가지고ATL을 만난다.',
     'Hunter가 자신에게 닫은 통로에서 LM에게 움직임을 넘기고, Mark의 팝·Carter의 롤이 Collins·Capela의 선택과 맞물리는 한정 사용창을 수행한다. 상대와 동료의 기여를 자신의 득점으로 회수하지 않는다.',
     'P의 직접 종료 기회와 동료의 시작권·위치 노동이 교환된다. 이15초창이 시리즈 승리의 단독 원인은 아니다.',
     'Apr30 뒤 선택된CHI4–1로BOS에 진입한다. 다음 대결의 결말은 아직 모른다.'),
    ('Boston과 갈라진 네 경기','2024년5월6·8·11·13일BOSG1–4',
     'ATL종료 뒤BOS의 새 수비 배정과 자기 역할을 전달받았다.',
     '초반에 받은 매치업 과제와 경기 뒤 실제로 본 공간 압력을 함께 평가한다. 좋은 공격과 막힌 공격을 모두 다음 준비 자료로 내놓는다. May19의 전용15초창은 이 시점의 사건으로 복사하지 않는다.',
     '원정 두 경기의 실패와 준비 시간을 되돌릴 수 없다. 네 경기에서 본 정보만 다음 역할에 쓴다.',
     'May13종료 뒤2–2다. G5부터 다시 현재 과제를 수행해야 한다.'),
    ('낮은 연결로 남기는 책임','2024년5월15·17·19일BOSG5–7',
     'BOS와2–2이고, 앞 네 경기의 막힌 통로가 평가 자료에 남았다.',
     'G7의 한정 창에서 Brown이 닫은 높은P통로를 고집하지 않고 낮은LV연결로 바꾼다. Smart의LM추적·Horford의내부 선택과 이미 배정된 동료의 비용을 따로 남긴다.',
     '낮은 연결은 자기 종료를 포기하고 LV가 다른 압력을 받게 한다. 교환된15초를 일곱 경기 전체 승리 원인으로 확대하지 않는다.',
     'May19종료 뒤CHI4–3과MIL진입이 남는다. 이겼다고 앞 실패가 없어지지 않는다.'),
    ('Milwaukee의 내부 앞에서','2024년5월22–6월1일MIL6경기',
     'BOS종료 뒤MIL의 기존 진입과 전달된 역할을 확인했다.',
     'Middleton이 높은P통로를 막는 한정 창에서 낮은Carter를 쓰고 Mark의팝과Lopez의림 선택을 구분한다. 동료가 맡는 접촉·확보·다음 연결을 보고 역할을 수행한다.',
     '직접 종료와 Carter의 내부 노동은 동등한 무료 보상이 아니다. 선행 경기의패배·동료기회 비용도 남는다.',
     'Jun1종료 뒤CHI4–2로DEN결승에 들어간다. 우승일·점수·성공은 아직 모른다.')]
   rows.extend(split(base,*v,common+[ref(C01,'/NBA_absence_windows')] if i==0 else common) for i,v in enumerate(variants))
  elif number==48:
   common=[ref(LATE,'/selected_seasons/1'),ref(EAST,'/six_game_candidates')]
   variants=[
    ('두 우승 뒤에도 새 시즌의 자리','2024–25 기존정규역할→2025MIA진입전',base['entry_state'],
     '다시 비운 교육·봉사 귀국 창의 역할 부담을 담당자와 동료에게 확인하고, 이미 배정된 공격·반환·수비 과제를 새 시즌에 수행한다. 이전 두 우승을 코치나 동료의 결정권으로 바꾸지 않는다.',
     '귀국 창에서는 자신은NBA분0이며 동료34분이 실제 역할 부담이다. 기존동부1위 진입은 전82경기 개인 출전 인증이 아니다.',
     'MIA진입 자격과 이번 역할만 알고 첫 대결을 준비한다.'),
    ('Miami의 도움과 짧은 반환','2025년4월19–29일MIA5경기',
     '새 시즌의 선택된 동부1위 진입과 전달된 역할이 있다.',
     'Butler가P통로를 막고Bam이Carter를돕는 한정 창에서 짧은롤 반환을 수행한다. 상대의 도움 선택과 Carter의 읽기를 독립 기여로 남긴다.',
     '공을 넘기면 자기 득점 종료를 잃고 Carter가 빠른 판단 부담을 맡는다. 선택된 시리즈 결과를 이15초의 득점으로 만들지 않는다.',
     'Apr29종료 뒤CHI4–1과BKN진입이다.'),
    ('Brooklyn의 서로 다른 추적','2025년5월4–15일BKN6경기',
     'MIA종료 뒤BKN과의 새 배정을 전달받는다.',
     'Kyrie의LM추적과Harden의LV압력을 한정 사용창에서 구분하고, 동료의 시작·마무리 역할이 유지되도록 현재 자기 연결 위치를 선택한다. 상대의 판단을 단순 이름 목록으로 줄이지 않는다.',
     '자기 종료 기회와 동료의 독립 운반·맞대응 부담이 나뉜다. 막힌 선택도 다음 평가에 남긴다.',
     'May15종료 뒤CHI4–2로PHI에 진입한다.'),
    ('Philadelphia와 다시 둘씩','2025년5월18·20·23·25일PHIG1–4',
     'BKN종료 뒤PHI와 받은 매치업 과제를 만난다.',
     '앞 네 경기의 좋은 공격과 실패를 함께 보고 자기 직접 공격과 조기 반환의 조건을 점검한다. May31의 전용 창·G7승리를 이 시점에 알거나 사용하지 않는다.',
     '원정 실패와 준비 시간이 남는다. 동료가 맡은 공 확보를 자기 공격 성공으로 합치지 않는다.',
     'May25종료 뒤2–2다. 마지막 세 경기의 결과는 아직 모른다.'),
    ('Philadelphia를 지난 다음 문턱','2025년5월27·29·31일PHIG5–7',
     'PHI와2–2이고 앞 실패에서 얻은 평가 자료가 있다.',
     'May31G7의 이미 선택된 상대 압력·동료 연결 창을 수행하고 끝난 뒤 진입 자격을 확인한다. 같은 상대를 넘었다는 이유로MIN의 선택도 해결됐다고 간주하지 않는다.',
     'PHI와 일곱 경기의 시간·선택 비용이 남고, MIN은 다른 상대에게서 얻은 읽기를 그대로 허용하지 않는다.',
     'May31종료 뒤CHI4–3으로MIN결승에 들어간다. 세 번째 우승은 아직 얻지 않았다.')]
   rows.extend(split(base,*v,common+[ref(C01,'/NBA_absence_windows')] if i==0 else common) for i,v in enumerate(variants))
   minvariants=[
    ('Minnesota와 다른 네 번의 응답','2025년6월5·8·11·13일FinalsG1–4',
     '동부를 통과해MIN과 첫 경기를 준비한다. 마지막 경기의 점수나21.6초는 아직 없다.',
     '전달된 안정 역할 안에서 자기 공격과 동료 이양을 수행하고 각 경기 후 현재 보이는 MIN의 압력과 자기 실패를 평가한다. 라이벌은 다른 상대의 실패를 이어받는 허수아비가 아니다.',
     '두 팀은 이미 쓴 네 경기의 역할·기회를 돌려받지 못한다. G7시간·패스·릴리스는 여기로 복사하지 않는다.',
     'Jun13종료 뒤2–2다. 다음 두 경기에서 수행을 다시 해야 한다.'),
    ('한 경기씩 남기는 결승','2025년6월16·19일FinalsG5–6',
     'MIN과2–2이고 앞 네 경기의 실제 평가만 있다.',
     '지금 전달된 역할을 다시 수행하고 G5·G6 종료 뒤 상대와 자기 선택의 결과를 확인한다. 마지막 공격을 미리 합의하거나 현재 손패스를 우승 장면의 예행 성공으로 만들지 않는다.',
     'G6패배와 다시 준비할 시간을 받아들인다. 서로의 자기 시작·마무리 권한을 독점하지 않는다.',
     'Jun19종료 뒤3–3, Jun22G7진입이다. 경기 마지막상태·승자는 아직 모른다.')]
   rows.extend(split(base,*v,[ref(LATE,'/selected_seasons/1/selected_used_series/3')]) for v in minvariants)
  else: rows.append(copy.deepcopy(base))
 assert len(rows)==61
 for i,b in enumerate(rows,1):
  old_num=b['proposed_episode'];b['original_prepared_episode']=old_num;b['episode']=i;b['proposed_episode']=i
  b['status']='CURRENT_REPAIRED_EPISODE_DESIGN_PENDING_INDEPENDENT_ACCEPTANCE'
  b['episode_function']=b['title'];b['consumed_exit_port_ids']=b['function_ids']
  if old_num in [43,44,51]:
   b['source_refs'].append(ref(C01));b['unresolved_used_dependencies']=[]
  if old_num==18:
   b['action_choice']+=' 의무와 다음 준비를 끝낸 뒤 짧게 게임을 즐기고 다음 일정 전 스스로 멈춘다. 취미가 곧 농구 문제 해결이나 영입 성공이 되지는 않는다.'
   b['durable_cost']+=' 편한 시간을 즐기되 다음 과제를 밀어낼 권한은 얻지 않는다.'
   b['source_refs'].append(ref(ARC,text=True))
   b['personal_scene']='의무 뒤의 작은 즐거움·자기중단 선택; 실패 교훈의 재연만으로 쓰지 않는다.'
  if old_num==28:
   b['action_choice']+=' 공개 NBA공지의 투표·발표 시점을 읽고, 별도로 창작된 온건한 외부평가가 자기 득점과LM/LV의 독립 역할을 다르게 묶는다는 점을 본다. 다음 평가 자료에 자신의 좋은 공격·실패와 동료 역할을 함께 남기기로 한다.'
   b['state_change']+=' 외부 시선 때문에 준비 자료의 초점이 달라지지만, 실제선정·실존기사·미래득표는 얻지 않는다.'
   b['media_scene']={'classification':'AUTHOR_FICTION_MEDIA_NOT_REAL_REPORT_OR_QUOTE','source_information':'OfficialDec8announcement known; Januarydates acquiredseparately, nofutureballots',
    'cause_response':'Opinionframing→Pchooses ownpreparation/evaluationfocus; nofabricatedscapegoat/frontofficeconflict.'}
  if old_num==26:
   b['staff_scene']='기존코치가 허용한 제한elbow시험의 권한과P의 현재수행/실패보고를 구분한다. 주인공은코치가아니다.'
  if old_num==43:
   b['timeline_window']+='→2023Sep14별도합의전달→Sep25기술회의전등록완료전달'
   b['state_change']='첫우승뒤자기자료를전달한단계에는공적승인이성립하지않는다. 이후Sep14별도NBA/FIBA/NBPA·구단보험합의안내와Sep25기술회의전등록완료안내를받은뒤해당문서의허가범위만확인했다. 본인의제출과기관승인을구분하며금메달·체육요원편입·544시간이행은아직얻지않았다.'
   b['named_acquisition_checkpoints']=[{'order':1,'when':'첫우승뒤본인자료준비','learned':'자기자료와기관질문만정리한다.'},
    {'order':2,'when':'Sep14별도합의와Sep25기술회의전등록뒤','learned':'에이전트가전달한해당행위자/문서범위의공적대회허가만안다. 금메달·편입·실적을아직얻지않는다.'}]
  if old_num==44:
   b['timeline_window']='2023사적공동과제→Sep26–Oct6선택된공적6경기→Oct9별도NBA복귀'
   b['action_choice']+=' 별도NBA/FIBA/NBPA·두구단합의와대표팀등록이전달된뒤 공적대회에서선택된 자기윙부담과 동료운반·내부공확보를 나누어 수행한다. 사적연습이공적승리인증은아니다.'
   b['state_change']='Oct6경기종료뒤 선택된한국금메달을관찰한다. Oct9별도구단복귀뒤에도교육·34개월·544시간의무는남고, 라이벌과완전화해·군역완료는얻지않는다.'
   b['durable_cost']+=' CHI미디어데이/캠프/첫프리시즌과MIN연습/AbuDhabi기회를잃는다. 기존변준형·양홍석등록/분및필리핀금메달기회변화도남는다.'
   b['named_acquisition_checkpoints']=[{'order':1,'when':'사적공동과제','learned':'사적훈련의분담만안다.'},
    {'order':2,'when':'Sep26–Oct6각공적경기종료','learned':'끝난경기의선택결과만안다. 다음경기·금메달을선인지하지않는다.'},
    {'order':3,'when':'Oct6결승종료→Oct9별도구단복귀','learned':'금메달과복귀절차는알지만체육요원의교육·544시간완료는아직없다.'}]
  if old_num==46:
   b['timeline_window']+='→Jun6G1별도종료관측'
   b['entry_state']='MIL종료뒤DEN결승에들어갔다. Jun6G1학습창이후관측전에는그경기승자도알지못한다.'
   b['state_change']='Jun6해당18초의노샷학습창을관측했다. 별도G1종료뒤선택된CHI1–0을확인하며그승리를학습창의득점으로돌리지않는다. 후행경기·두번째우승은아직얻지않았다.'
   b['source_refs'].append(ref(LATE,'/selected_seasons/0/selected_used_series/3'))
   b['named_acquisition_checkpoints']=[{'order':1,'when':'Jun1MIL종료','learned':'DEN결승진입만확인'},
    {'order':2,'when':'Jun6G1학습창종료','learned':'18초의노샷학습만확인'},
    {'order':3,'when':'Jun6G1종료','learned':'별도선택된CHI1–0. 다음경기결과는모름'}]
  if old_num==47:
   b['entry_state']='Jun6G1종료뒤1–0이다. 다음경기준비에는현재관측과전달된역할만쓴다.'
   b['timeline_window']='2024Jun9G2→Jun12G3→Jun14G4→Jun17G5→Jun20G6 종료의순차취득'
   b['action_choice']='Jun9종료뒤1–1,Jun12뒤1–2,Jun14뒤2–2,Jun17뒤3–2를차례로확인하며앞학습을현재수행조건으로만쓴다. 뒤의승리를소급해학습성공으로주장하지않는다. Jun20G6에서기존역할을수행하고끝난뒤두번째우승을확인한다.'
   b['durable_cost']+=' DEN에진두경기의실패와동료기회비용은우승뒤에도남는다.'
   b['source_refs'].append(ref(LATE,'/selected_seasons/0/selected_used_series/3'))
   b['named_acquisition_checkpoints']=[{'order':j+1,'when':day+'경기종료','learned':state+';다음결과선인지0'}
    for j,(day,state) in enumerate([('Jun9','1–1'),('Jun12','1–2'),('Jun14','2–2'),('Jun17','3–2'),('Jun20','CHI4–2두번째우승')])]
  if old_num==51:
   b['entry_state']='Jun18NBA서비스종료 통지를본뒤, 별도로허용된Jun19guest준비에 들어간다. 본인은현재의무·미국체류상태통지범위만안다.'
   b['nondiegetic_scope_policy']='짧은2035후일담;중간10년전경기·추가우승총수는본편의무가아님. 이편집지시는P의관측지식이아니다.'
   b['named_acquisition_checkpoints']=[{'order':1,'when':'Jun10행정통지','learned':'해당사용3일의의무·해외체류허가범위만안다.'},
    {'order':2,'when':'Jun18서비스종료','learned':'자기서비스종료통지'},
    {'order':3,'when':'Jun19별도guest','learned':'후배의관찰가능한준비행동. 사적생각·미래성공모름'},
    {'order':4,'when':'Jun20은퇴','learned':'전날이미본준비를기억한다.'}]
  for link in b.get('promise_consumption',[]):link['current_episode']=i
  if old_num==45 and i!=46:b['promise_consumption']=[]
  if old_num==48 and i!=56:b['promise_consumption']=[]
  b['exit_state_required']=b['state_change']
  b['basketball_goal']=b['action_choice']
  selected_access(b,i)
 for i,b in enumerate(rows):
  b['next_entry_state']=rows[i+1]['entry_state'] if i+1<len(rows) else None
  b['reader_question']=b['state_change']+' 이현재상태에서다음허용과제와동료부담을어떻게감당할것인가?'
 units=[];ports=[];oldh=load(HISTORY)
 for idx,u in enumerate(UNITS):
  es=[e for e in rows if e['unit_id']==u]
  nxt=[e for e in rows if e['unit_id']==UNITS[idx+1]] if idx<9 else []
  unit=copy.deepcopy(oldh['unit_exits'][idx]);unit.update(entry_state=es[0]['entry_state'],exit_state=es[-1]['state_change'],
   next_unit_id=UNITS[idx+1] if idx<9 else None,next_entry_state=nxt[0]['entry_state'] if nxt else None)
  unit['first_recommended_episode']=es[0]['episode'];unit['last_recommended_episode']=es[-1]['episode']
  unit['unresolved_used_dependencies']=[];unit['status']='CURRENT_REPAIRED_BOUNDARY_PENDING_INDEPENDENT_ACCEPTANCE'
  unit['source_refs']=[r for e in [es[0],es[-1]] for r in e['source_refs']]
  units.append(unit)
 for p in oldh['finite_used_exit_ports']:
  x=copy.deepcopy(p);es=[e for e in rows if p['port_id'] in e['function_ids']]
  x.update(entry_state=es[0]['entry_state'],changed_action=' / '.join(e['action_choice'] for e in es),
   durable_cost=' / '.join(e['durable_cost'] for e in es),exit_state=es[-1]['state_change'],
   used_recommended_episodes=[e['episode'] for e in es],status='SELECTED_CURRENT_DESIGN_PENDING_INDEPENDENT_ACCEPTANCE')
  if p['port_id'] in ['FC035','FC036','FC037','FC038','FC039']:
   for k in ['entry_state','changed_action','durable_cost','exit_state']:x[k]=p[k]
   x['fine_grained_phase_preserved']=True
  if p['port_id'] in ['FC031','FC032','FC040']:x['source_refs'].append(ref(C01))
  x['unresolved_used_dependencies']=[]
  x['source_refs'].extend([r for e in es for r in e['source_refs'] if r not in x['source_refs']])
  ports.append(x)
 assert len(ports)==42 and all(e['unresolved_used_dependencies']==[] for e in rows)
 return {'id':'THREEPEAT_61_CURRENT_REPAIRED_DESIGN_2026_10_12','producer_id':'root_codex',
  'status':'SUBSTANTIVE_CURRENT_DESIGN_REPAIRED_PENDING_INDEPENDENT_ACCEPTANCE',
  'scope_id':'THREEPEAT_2023_2025_NINE_ACTS_BRIEF2035_CURRENT',
  'recommended_episode_count':61,'main_episode_count':60,'brief_epilogue_count':1,
  'source_sha256':{p:sha(p) for p in [OLD,HISTORY,LATE,EAST,C01,ARC,ACCESS]},
  'derivation':'51+4distinct2024role/Eastphases+4distinct2025role/Eastphases+2missingMINfinalprogression; no newresult orquota padding.',
  'episodes':rows,'unit_exits':units,'finite_used_exit_ports':ports,
  'category_counts':dict(Counter(e['category'] for e in rows)),
  'strict_NBA_count':sum(e['category']=='NBA' for e in rows),'strict_NBA_percent':100*sum(e['category']=='NBA' for e in rows)/61,
  'NBA_draft_included':False,'independent_review_completed':False,'final_episode_count_locked':None,
  'prose_count':0,'actual_Pack_count':0,
  'gates':{'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--refresh-owned',action='store_true');p.add_argument('--expected-hash');a=p.parse_args()
 raw=json.dumps(build(),ensure_ascii=False,indent=2)+'\n';out=ROOT/OUT
 if a.check:assert out.read_text(encoding='utf-8-sig').replace('\r\n','\n')==raw
 elif out.exists():
  assert a.refresh_owned and a.expected_hash in {sha(OUT),hashlib.sha256(out.read_bytes()).hexdigest()}
  (ROOT/'Temp/repaired61_before.json').write_bytes(out.read_bytes());out.write_text(raw,encoding='utf-8')
 else:out.write_text(raw,encoding='utf-8')
 print(json.dumps({'prepared_episodes':61,'finite_ports':42,'strict_NBA':46,'NBA_percent':100*46/61,'independent_acceptance':False},ensure_ascii=False))
if __name__=='__main__':main()
