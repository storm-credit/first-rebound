"""New bounded game defense changes, not growth/season/contract success.
The prior two early-help samples remain unchanged. Capacity reservations are
additive and the evaluation retains adverse decisions and unresolved outcomes.
"""
import argparse,copy,hashlib,json
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import build_a07_opening_game_elbow_observation_family as old
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_a07_changed_defense_role_evaluation.py'
OUT='design/A07_CHANGED_DEFENSE_ROLE_EVALUATION_2026_10_07.json'
MD=OUT[:-5]+'.md'
CP2='design/CP2_ACT_SUBACT_PACKET.json'
BATCH='design/A07_FINITE_FUNCTION_BATCH_2026_10_07.json'
PINS={old.OUT:'f72d2ea63ebde3bdb0d9b0cfc2d28d4b35250e74d1160811c1cb6fc60ffe192e',old.SELF:'100bc7986b25f15db3a8a12fdf2dc90b38715471d6fd4a889026f4312838e2da',CP2:'2b291bca588302cbb254fc3417652f7d7532c46d7094221cdcceac60619c9db9',BATCH:'5d04630993f95e218ed95fba78ad505854999e7c0179d407964ffcebc1c91e0e'}
def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def sources():
 for p,h in PINS.items():assert sha(p)==h,'Unreviewed source: '+p
 o=load(old.OUT);assert o==old.build(),'Accepted two-game source meaning changed'
 assert o['root_working_selection'] and o['certification']['independent_review_completed']
 assert len(o['new_modeled_game_observations'])==2
 assert all(r['defensive_condition'].startswith(('Help arrives before','The same strongside help'))for r in o['new_modeled_game_observations'])
 sub={r['id']:r for r in load(CP2)['subacts']}
 assert sub['A07-S3']['success_criteria']==['상대가 바꾼 수비에 따른 성공/실패를 함께 평가','32분 조합을 시즌 기록이나 QO 충족으로 환산하지 않음']
 assert sub['A07-S3']['choice']=='좋은 경기만 고르지 않은 자료로 역할 확대를 요구하고 가격 협상은 에이전트에게 맡긴다'
 assert sub['A07-S3']['cost']=='실패와 효율 변동을 공개한 채 자신의 가격 기대를 조정할 수 있어야 함'
 return o,sub

def observations():
 common={'classification':'NEW_FICTIONAL_NBA_GAME_ACTION_NOT_HISTORICAL_FACT','catch_player':'Protagonist','catch_position':'right_elbow',
 'primary_defender':'Patrick Williams','secondary_defender':'Kira Lewis Jr.','return_recipient':'LaMelo_pick4','return_route':'right_elbow_to_top_of_arc',
 'catch_shot_clock_seconds':12,'game_clock_reservation_seconds':20,'subsequent_shot_outcome':None,'points':None,'turnover_or_transition_points':None,
 'new_skill_mastery_or_efficiency_growth':False,'actual_opponent_intent_or_coach_instructions_known':False}
 return [{**common,'id':'CD1_INSIDE_STAY_FAILURE','visible_defense':'Patrick remains on the inside path to the basket; Kira stays with the top-of-arc recipient instead of helping before the catch',
 'action':'Protagonist tries his prepared short inward step into the path Patrick already occupies, stops without passing the defender, then returns to LaMelo',
 'return_release_shot_clock_seconds':5,'receiver_shot_clock_seconds':4,
 'local_choice_evaluation':'The short-attack request was unsuitable for the observed occupied inside path; keeping it alive spent seven seconds before the return',
 'local_decision_supported':False,'irreversible_cost':'LaMelo receives only four seconds; the spent opportunity/time is kept in the evaluation, not relabelled as successful offense',
 'reengagement_observation':'After return he leaves the passing lane and moves toward weakside rebound position; no rebound outcome is selected'},
 {**common,'id':'CD2_DELAYED_HELP_STOP','visible_defense':'Patrick initially leaves room for one prepared step; Kira stays near the top-of-arc recipient at the catch, then visibly rotates toward the elbow after that step',
 'action':'Protagonist takes only the already prepared short step, sees the delayed rotation approaching the path, stops the attack and returns to LaMelo before trying another inward step',
 'return_release_shot_clock_seconds':9,'receiver_shot_clock_seconds':8,
 'local_choice_evaluation':'Stopping once the new delayed help is visible preserves eight seconds for the recipient; this is a timely bounded decision, not a scoring or skill-growth result',
 'local_decision_supported':True,'irreversible_cost':'He relinquishes his own remaining attempt and uses time/energy to return and reposition; the teammate finish remains unselected',
 'reengagement_observation':'He clears the return lane and occupies the weakside rebound/re-entry position; subsequent catch or rebound is unselected'}]
EXPECTED=copy.deepcopy(observations())
def assert_observations(rows,o):
 assert rows==EXPECTED,'Changed-defense action/decision/cost meaning changed'
 assert len(rows)==2 and len({r['id']for r in rows})==2
 lineup=o['lineup_capacity']['five_per_team']
 for r in rows:
  assert {r['catch_player'],r['return_recipient']}<=set(lineup['CHI'])
  assert {r['primary_defender'],r['secondary_defender']}<=set(lineup['DET'])
  assert r['catch_shot_clock_seconds']>r['return_release_shot_clock_seconds']>r['receiver_shot_clock_seconds']>=0
  assert r['game_clock_reservation_seconds']==20 and r['points']is None and r['subsequent_shot_outcome']is None
 assert rows[0]['local_decision_supported']is False and rows[1]['local_decision_supported']is True

def build():
 o,sub=sources();rows=observations();assert_observations(rows,o)
 c=o['lineup_capacity'];lineup=c['five_per_team'];extra=sum(r['game_clock_reservation_seconds']for r in rows)
 assert extra==40 and c['new_capacity_reservation_seconds_per_named_player']==40
 _,chi,det=old.sources()
 assert (c['source_CHI_block_index'],c['source_DET_block_index'])==(0,2)
 assert 40+extra<min(chi['unordered_regulation_blocks'][0]['minutes'],det['unordered_regulation_blocks'][2]['minutes'])*60
 remaining={}
 for team,vector in c['remaining_source_player_seconds_after_reservation'].items():
  remaining[team]={n:str(Fraction(v)-extra*int(n in lineup[team]))for n,v in vector.items()}
  assert all(Fraction(v)>=0 for v in remaining[team].values())
  assert sum(map(Fraction,remaining[team].values()))==14400-5*80
 # Four samples are a bounded local record, never four games or82*32minutes.
 evaluation=[{'sample':r['id'],'visible_defense':r.get('defensive_condition',r.get('visible_defense')),
  'receiver_shot_clock_seconds':r['receiver_shot_clock_seconds'],
  'decision_supported':r.get('choice_was_timely_for_observed_help',r.get('local_decision_supported')),
  'shot_outcome':r.get('shot_outcome',r.get('subsequent_shot_outcome')),
  'game_count_or_season_rate':None}for r in [*o['new_modeled_game_observations'],*rows]]
 assert len(evaluation)==4 and sum(r['decision_supported']for r in evaluation)==2
 return {'id':'A07_CHANGED_DEFENSE_ROLE_EVALUATION','status':'INDEPENDENTLY_REVIEWED_CONDITIONAL_CHANGED_DEFENSE_WORKING_DESIGN_NOT_ROLE_EXPANSION_GRANTED',
 'root_working_selection':{'two_new_coach_calls_and_own_mixed_record_transfer_selected':True,'basis':'Delegated routine design within original CP2 task; existing lawful common-lineup availability remains conditional.','whole_game_season_contract_or_role_award_selected':False},
 'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'Repository BOMstrip LF','game_anchor':o['game_anchor'],
 'prior_two_pre_catch_help_samples_preserved':o['new_modeled_game_observations'],
 'prior_two_are_opponent_defense_change_evidence':False,
 'new_limited_coach_calls':{'classification':'ROUTINE_CONDITIONAL_FICTIONAL_WORKING_DESIGN_SELECTED','scope':'One inside-stay attempt, one delayed-help attempt of the already prepared short step/return; stop further trial on closed path','new_training_skill_or_full_game_role_selected':False,'date_wide_or_full_season_health_selected':False},
 'new_changed_defense_observations':rows,
 'cumulative_capacity':{'five_per_team':lineup,'previous_reserved_seconds_per_player':40,'new_reserved_seconds_per_player':40,'total_reserved_seconds_per_player':80,'remaining_player_seconds':remaining,'team_minutes_each_preserved':240,'pair_minutes_preserved':480,'absolute_times_or_whole_chronology_selected':False},
 'bounded_role_evaluation':evaluation,
 'coach_and_agent_transfer':{'classification':'CONDITIONAL_FICTIONAL_OWN_MATERIAL_HANDOFF_WORKING_DESIGN_SELECTED','coach_direct_action':'Coach and protagonist compare the two unchanged early-help returns with inside-stay and delayed-help trials; mark the unsuitable inside continuation and late return as failures, timely stop as a bounded decision only.',
 'agent_direct_action':'Protagonist delivers allfour own permitted observations and the adverse time/opportunity costs, requests conditional role evaluation, and leaves pricing to the agent.',
 'irreversible_cost':'He gives up presenting only the timely decisions and takes time from another own-attack practice/showcase opportunity to prepare the mixed record.',
 'institution_or_other_players_hidden_knowledge':False,'market_answer_or_contract_price':None,'actual_receipt_certified':False},
 'explicit_nonconversions':{'P32_capacity_to82_game_minutes':False,'starter_criteria_or_QO_met':False,'two_old_samples_to_changed_defense':False,'timely_decision_to_made_shot_or_skill_mastery':False,'four_possessions_to_whole_season_efficiency':False,'mixed_handoff_to_negotiated_price_or_role_award':False},
 'exit_scope':{'original_S3_success_criteria':sub['A07-S3']['success_criteria'],'four_local_decision_observations_constructed':True,'source_adjusted_defense_success_failure_comparison_supported_conditionally':True,'full_A07_Act_exit_or_season_efficiency_certified':False,'remaining_precise_boundary':'Root may adopt the two new coach calls and own mixed-record transfer as bounded fiction under the existing common-lineup availability/legal roster condition; a complete season evaluation or consequential contract remains separate.'},
 'certification':{'independent_review_completed':True,'independent_review_basis':'g11 separately read original CP2 choice/cost and ten source-player vectors, recomputed cumulative 80 seconds and 240/480 minutes, and rejected actual loader-return CD2 null-to-MADE and CP2 failure-cost-hidden mutations. Root read producer and retained every adverse observation; author self-tests are not independent checks.','actual_historical_play_or_clinical_clearance':False,'new_contract_or_pick_or_season_winner_selected':False,'whole_A07_A08_G13_G14_complete':False,'new_final_function_or_registry_count':0,'actual_context_packs':0,'manuscript_count':0,'manuscript_allowed':False,'design_gate':'CLOSED','REGISTER_or_central_changed':False}}

def validate(o):
 try:assert o==build(),'Saved defense evaluation differs';return[]
 except(AssertionError,KeyError,ValueError,OSError)as e:return[str(e)]
def markdown(o):
 return '\n'.join(['# A07 상대 수비 변화와 역할 평가의 한정 추가 관측','',o['status'],'',
 '기존2021-10-20 Chicago–Detroit 두표본은둘다캐치전조기도움이므로수비변화자료로재명명하지않는다. 원240/240분과CHI12분·DET4분공통5인블록에새두20초비연속창을예약한다. 기존각40초와합쳐각80초이며나머지선수분은양수·팀240분그대로다. 전체교체순서/승패/임상사실은선택하지않는다.','',
 '## 추가 경기 표본','',
 '1. **안쪽유지의실패**: Patrick이골밑으로가는길을지키고Kira는LaMelo쪽에남는다. P가준비한짧은안쪽첫걸음을고집하다Patrick앞에서멈추고늦게반환해LaMelo에게4초만남는다. 불리한판단·소모된시간과기회를자료에그대로남긴다. 이후슛/득점/턴오버결과는선택하지않는다.','2. **늦은도움의중단**: Patrick앞에첫걸음정도공간이있고Kira는캐치때LaMelo쪽에있다가첫걸음뒤엘보쪽으로움직인다. P는그이동을직접보고추가안쪽시도를멈춰반환,LaMelo에게8초를남기고반환경로를비워재관여위치로간다. 이는국소중단판단이며새드리블기술·패스성공률·득점성공은아니다.','',
 '가상감독의새두한정호출과자기혼합자료전달은root가routine조건부작업설계로채택했다. 상대의숨은작전/의도를읽는것이아니라직접보이는위치와이동을기록한다. 새기술개발·실전안정성·공동에이스권한을선지급하지않는다.','',
 '## 평가와 정보 경로','',
 'P와코치는기존조기도움2개와새안쪽유지/늦은도움2개를한자료에놓는다. P는두적절한중단/반환만추리지않고늦은반환과막힌안쪽선택도에이전트에게전달한다. 자신의완성형공격수과시기회를내려놓고자료정리시간을쓴다. 가격협상권한과답은에이전트에게남기며실제접수/계약결과를인증하지않는다.','',
 '원CP2 S3의상대수비변화별성공/실패평가는여기서**국소선택의적절성/실패비용**으로구별한다. 기존MISS두개는보존하고새2개의슛결과는미선택이다. P32는조건부분용량이며82게임기록·시즌효율·선발/QO충족으로환산하지않는다. 네표본을완전한시즌실적/시장평가로부르지않고root의후속한정출구검문에넘긴다.','',
 '같은적법명단/두창가용조건은보존한다. 새감독한정호출·본인자료전달은작업설계로채택됐으나실제명단등록/시장수락은인증하지않는다. 사적영수증·전체82임상결과를추가필수게이트로요구하지않는다. A08 계약/기관결정과전체Act출구는별도다.','',
 '|번호|묶음|상태|','|---|---|---|','|1|2020드래프트연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23거래·계약|조건부family·중요선택미완료|','|4|장기커리어|후속시즌대기|','|5|결말·전체구조|수비변화국소2표본채택·전체출구미완료|','|6|집필규격·ContextPack|현행등록기참조·Pack0|','|7|통합·독립·작가승인|최종CLOSED|','',
 '미완료큰묶음5 / v0.30 PARTIAL / 설계·원고CLOSED / 새등록0·원고0.',''])
def self_test():
 orig=observations
 def bad():
  r=orig();r[0]['local_decision_supported']=True;return r
 with patch(__name__+'.observations',side_effect=bad):
  try:build();raise RuntimeError('FALSE_PASS failed_attack_relabelled_success')
  except AssertionError:pass
 def bad():
  r=orig();r[1]['new_skill_mastery_or_efficiency_growth']=True;return r
 with patch(__name__+'.observations',side_effect=bad):
  try:build();raise RuntimeError('FALSE_PASS decision_to_skill_growth')
  except AssertionError:pass
 return 2
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');args=ap.parse_args();o=build()
 if args.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
 if args.check:assert validate(load(OUT))==[]and text(MD)==markdown(o)
 print(json.dumps({'current':True,'new_defense_samples':2,'prior_early_help_samples':2,'total_reserved_seconds_per_player':80,'controls':self_test()if args.self_test else None}))
