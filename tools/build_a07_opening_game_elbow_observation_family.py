"""Two bounded fictional game observations within preserved CHI/DET capacity.
No whole-game winner, future contract, full-season health or old observation
is promoted. These are new modeled samples, not recovered historical plays.
"""
import argparse,copy,hashlib,json
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_a07_opening_game_elbow_observation_family.py'
OUT='design/A07_OPENING_GAME_ELBOW_OBSERVATION_FAMILY_2026_10_07.json'
MD=OUT[:-5]+'.md'
CP2='design/CP2_ACT_SUBACT_PACKET.json'
BATCH='design/A07_FINITE_FUNCTION_BATCH_2026_10_07.json'
M1='simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json'
PAIR='research/CHICAGO_2021_22_OPENING_DET_PAIRED_INPUT_RECOVERY_2026_10_07.json'
DET='research/DETROIT_2021_OPENING_NAMED_OPERATING_FAMILY_2026_10_07.json'
RT='design/A08_S1_CURRENT_RT_COST_SLOT_FAMILY_2026_10_07.json'
PINS={CP2:'2b291bca588302cbb254fc3417652f7d7532c46d7094221cdcceac60619c9db9',BATCH:'5d04630993f95e218ed95fba78ad505854999e7c0179d407964ffcebc1c91e0e',M1:'73d51b630e9c9d4ec31b7e3952906165589bd8c49a48bb07c79bdc9ad02e8fca',PAIR:'e731ab02a83e1135137da08a5384afbc077111cddb5a7d6ad8a4ba8f921e9f70',DET:'7490b1a46a744088980c115680140383615a2e6ec92901e1fdd901c326861be0',RT:'ed87785bf0e40c568fa97c578d7d0c2102dadc0445006d475acb235bfa4156d5'}
def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def sources():
 s={p:load(p)for p in PINS}
 for p,h in PINS.items():assert sha(p)==h and s[p]==json.loads(text(p)),'Current source meaning changed: '+p
 sub={r['id']:r for r in s[CP2]['subacts']}
 assert sub['A07-S2']['success_criteria']==['캐치 위치·도움 방향·반환 경로·후속 슛을 함께 기록','득점 성공과 올바른 선택을 분리']
 assert sub['A07-S2']['irreversible_choice']=='실전에서 소모한 공격 기회와 늦은 반환의 실패를 자신의 표본에 남긴다'
 assert sub['A07-S3']['success_criteria']==['상대가 바꾼 수비에 따른 성공/실패를 함께 평가','32분 조합을 시즌 기록이나 QO 충족으로 환산하지 않음']
 assert s[BATCH]['independent_review_completed'] and s[M1]['certification']['independent_review_completed']
 assert s[PAIR]['verification']['independent_review_completed'] and s[DET]['certification']['independent_review_completed']
 row=[r for r in s[M1]['rows']if r['game_id']=='0022100004'and r['state']=='NORMAL']
 assert len(row)==1
 chi=row[0];pair=s[PAIR]['regulation_pair_comparison'];det=pair['DET_existing_G14_candidate']
 assert chi['candidate_date']=='2021-10-20'and chi['home']=='DET'and chi['away']=='CHI'
 assert chi['player_minutes']==pair['CHI_current_M1_NORMAL']['player_minutes']
 assert chi['regulation_team_minutes']==sum(chi['player_minutes'].values())==sum(det['player_minutes'].values())==240
 assert pair['pair_team_minutes']==480 and pair['joint_substitution_chronology_or_possessions_constructed']is False
 return s,chi,det

def modeled_samples():
 common={'classification':'NEW_AUTHOR_MODELED_BOUNDED_NBA_GAME_PLAY_NOT_HISTORICAL_FACT',
 'catch_player':'Protagonist','catch_position':'right_elbow','return_recipient':'LaMelo_pick4','return_recipient_position':'top_of_arc',
 'primary_defender':'Patrick Williams','help_defender':'Kira Lewis Jr.','help_direction':'strong_side_from_top_of_arc',
 'return_route':'right_elbow_to_top_of_arc','shot_player':'LaMelo_pick4','shot_type':'perimeter_jump_shot','shot_outcome':'MISS',
 'elapsed_game_clock_reservation_seconds':20,'catch_shot_clock_seconds':12,'points':0,
 'reengagement':'Protagonist clears the return lane and moves to weakside rebounding position',
 'rebound_winner_selected':False,'whole_possession_defensive_transition_selected':False,'actual_historical_play':False}
 return [{**common,'id':'EG1_LATE_RETURN','defensive_condition':'Help arrives before the elbow catch',
 'choice':'He delays the return while keeping the already closed short attack alive, then returns to LaMelo',
 'return_release_shot_clock_seconds':5,'receiver_shot_clock_seconds':4,'shot_release_shot_clock_seconds':2,
 'visible_cost':'LaMelo receives late and shoots under the remaining two-second constraint; the shot misses',
 'choice_was_timely_for_observed_help':False},
 {**common,'id':'EG2_EARLY_RETURN','defensive_condition':'The same strongside help again arrives before the elbow catch',
 'choice':'He cancels the short attack at the catch and returns immediately to LaMelo, then clears the lane',
 'return_release_shot_clock_seconds':10,'receiver_shot_clock_seconds':9,'shot_release_shot_clock_seconds':7,
 'visible_cost':'His own shot opportunity is relinquished; LaMelo has seven seconds and still misses',
 'choice_was_timely_for_observed_help':True}]
EXPECTED_SAMPLES=copy.deepcopy(modeled_samples())

def assert_samples(rows,chi,det):
 assert rows==EXPECTED_SAMPLES,'New samples must preserve actual action, recipient, clock and MISS meaning'
 assert len(rows)==2 and len({r['id']for r in rows})==2
 for r in rows:
  assert r['catch_player']in chi['player_minutes']and r['return_recipient']in chi['working_active_nominees']
  assert r['primary_defender']in det['player_minutes']and r['help_defender']in det['player_minutes']
  assert 24>=r['catch_shot_clock_seconds']>r['return_release_shot_clock_seconds']>r['receiver_shot_clock_seconds']>r['shot_release_shot_clock_seconds']>=0
  assert r['points']==0 and r['shot_outcome']=='MISS'and r['actual_historical_play']is False

def build():
 s,chi,det=sources();samples=modeled_samples();assert_samples(samples,chi,det)
 cb=chi['unordered_regulation_blocks'][0];db=det['unordered_regulation_blocks'][2]
 assert cb['positions']=={'PG':'LaMelo_pick4','SG':'LaVine','SF':'Protagonist','PF':'Markkanen','C':'Carter'}
 assert db['positions']=={'PG':'Kira Lewis Jr.','SG':'Josh Jackson','SF':'Patrick Williams','PF':'Jerami Grant','C':'Isaiah Stewart'}
 assert cb['minutes']==12 and db['minutes']==4
 lineups={'CHI':list(cb['positions'].values()),'DET':list(db['positions'].values())}
 for r in s[DET]['roster_candidates']:
  assert set(lineups['DET'])<=set(r['standard_candidate'])&set(r['working_active_standard_12'])
 reserve=sum(r['elapsed_game_clock_reservation_seconds']for r in samples)
 assert reserve==40 and reserve<min(cb['minutes'],db['minutes'])*60
 remaining={}
 for team,vector in [('CHI',chi['player_minutes']),('DET',det['player_minutes'])]:
  assert len(set(lineups[team]))==5
  remaining[team]={n:str(Fraction(v*60)-reserve*int(n in lineups[team]))for n,v in vector.items()}
  assert all(Fraction(v)>=0 for v in remaining[team].values())
  assert sum(map(Fraction,remaining[team].values()))==240*60-5*40
 return {'id':'A07_OPENING_GAME_ELBOW_OBSERVATION_FAMILY','status':'ROOT_REVIEWED_BOUNDED_WORKING_GAME_CALL_DESIGN_NOT_SEASON_SELECTED',
 'root_working_selection':{'two_calls_and_own_observation_route_selected':True,'authority':'Existing autonomous routine design authorization; source-conditioned common lineup capacity only. No new franchise, contract, health outcome, score or season choice.','conditional_legal_roster_and_common_lineup_availability_preserved':True,'whole_game_or_season_historical_lock':False},
 'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'Repository BOMstrip LF',
 'game_anchor':{'game_id':'0022100004','date':'2021-10-20','home':'DET','away':'CHI','source':PAIR,'calendar_hypothesis_preserved':True,'historical_score_or_possessions_copied':False},
 'working_coach_grant':{'classification':'ROOT_SELECTED_BOUNDED_FICTIONAL_ROUTINE_DESIGN','scope':'CHI coach calls the already prepared elbow return task twice, stops further short-attack calls when early help is observed','date_wide_NORMAL_health_selected':False,'full_game_minutes_changed':False,'whole_season_role_or_joint_ace_awarded':False},
 'lineup_capacity':{'source_CHI_block_index':0,'source_DET_block_index':2,'five_per_team':lineups,'original_team_minutes_each':240,'original_pair_minutes':480,'two_nonconsecutive_trial_windows_seconds_each':20,'consecutive_possessions_asserted':False,'new_capacity_reservation_seconds_per_named_player':40,'remaining_source_player_seconds_after_reservation':remaining,'DET_A_or_B_direction_selected':False,'full_chronology_or_5player_actual_registration_certificate':False},
 'new_modeled_game_observations':samples,
 'information_route':{'actor':'Protagonist','source':'own two game observations and footage available to him under modeled team permission','model_coach_review':'The coach shows late-return and early-return misses side by side; do not call either scoring success','agent_handoff':'Supplement existing A07 material with both new attempted returns and both misses, not a complete season efficiency report','real_person_inner_state_or_words_claimed':False},
 'precise_execution_conditions':[{'id':'COMMON_LINEUP_WINDOW','supported_input':'Both preserved240-minute vectors and same five active in bothDET A/B roster candidates','condition':'The chosen lawful roster path and these ten players are available for the two modeled windows; this is limited working availability, not all82 dates or actual clinical clearance.'},{'id':'COACH_TWO_CALLS','supported_input':'Previously permitted M1 limited task; root-selected routine game-call design constructed here','condition':'Root adopts the two calls and own observation route as bounded fiction within the common-lineup condition; no franchise, contract or whole-season result choice is entailed.'}],
 'criterion_projection':{'A07_S2_new_catch_help_return_shot_fields_complete':True,'scoring_success_is_choice_success':False,'old_practice_observations_relabelled_as_games':False,'original_audit_or_final_function_changed':False,'A07_S3_partial_two_samples_not_season_efficiency':True,'A08_S1_current_cost_link_ready_in_separate_root_owned_source':RT,'A08_S1_cost_link_applied_here':False,'A08_contract_institution_decision_or_joint_ace_authority_selected':False},
 'remaining_exact_scope':['Root-selected conditional two-play design supports S2 catch/help/recipient/shot criteria; the lawful roster and common-lineup condition is preserved and no full A07/season/QO claim follows.','A07 S3 still needs role evaluation scope appropriate to opponent adjustments, not all82 full-box certificates.','A08 S1 cost link is separate current cost family/agent transmission; A08 S2/S3 actual game-call models and E2 institutional decision remain separate.'],
 'certification':{'independent_review_completed':True,'independent_review_basis':'Root separately joined actual source game key and both player-minute vectors, independently recalculated each40-second reservation and14400 team-seconds. OriginalCP2 catch/help/recipient/shot and irreversible-game criteria read directly; same retry-to-MADE/different-team-recipient counterexamples rejected. Whole history/clinical roster acceptance not certified.','constructed_conditional_two_play_family_complete':True,'actual_historical_game_or_health_certified':False,'whole_2021_22_result_or_efficiency_selected':False,'new_contract_or_pick_or_important_direction_selected':False,'whole_A07_A08_or_G13_G14_complete':False,'new_final_function_or_registry_count':0,'actual_context_packs':0,'manuscript_count':0,'manuscript_allowed':False,'design_gate':'CLOSED','REGISTER_or_central_changed':False}}

def validate(o):
 try:assert o==build(),'Saved action/source family differs';return[]
 except(AssertionError,KeyError,ValueError,OSError)as e:return[str(e)]
def markdown(o):
 return '\n'.join(['# A07 개막 Chicago–Detroit 한정 실경기 2표본 설계','',o['status'],'',
 '## 이미 확보된 입력','',
 '기존0022100004/2021-10-20/DET홈·CHI원정은일정가설이다. 현M1 NORMAL의CHI240분·11블록과DET G14조건부240분·9블록을읽었다. CHI 첫12분블록(P/LaMelo/LaVine/Markkanen/Carter),DET 세번째4분블록(Kira/Josh/Patrick/Grant/Stewart)은고유5명이다. DET A/B 둘의표준·active명단에모두포함된다. Suggs새서명이나Garza/Lyles방향을이플레이5인에자동선택하지않는다.','',
 '두비연속20초창을각원블록에서예약해전원40초를빼도잔여분이양수이고원240분·양측480분을보존한다. 전체48분의동시교체순서나상대포제션을만들었다고주장하지않는다.','',
 '## 새 가상 경기 관측 두 개','',
 'Root가기존루틴설계위임으로가상코치의오른쪽엘보과제두호출과본인관측경로를한정작업설계로채택했다. Patrick의주수비와Kira의강한쪽조기도움에서 첫표본은P가늦게반환해LaMelo가2초남은급한외곽슛을실패한다. 다음표본은캐치때공격을접고빠르게LaMelo에게반환·재배치하며LaMelo는7초남은외곽슛도실패한다. 두번모두득점0으로두고빠른선택을득점성공으로재명명하지않는다. 잡은위치/도움방향/실명수신자/반환경로/후속슛과시계비용을함께기록한다.','',
 '기존연습을실전으로바꾸는것이아니라A07 훈련후·에이전트평가전넣을수있는새prospective경기관측이다. 본인에게허용된두표본영상을코치와대조하고두실패도에이전트에게전달하는정보경로만설계한다. 실존선수속마음·실제대사/원역사플레이/원88:94는복사하지않는다.','',
 '## 꼭 필요한 두 조건과 출구','',
 '①선택되는적법명단경로에서이10명이두창에가용한조건 ②가상감독한정2회호출및본인관측자료접근을root가한정설계로채택한조건이다. 두조건은구성가능한작업입력이며사적접수증·전체82건강·시즌승패확정을새필수게이트로요구하지않는다. 한정작업설계로채택한2표본은원S2의관측필드를지원한다. 현재출구감사는별도후속에서이조건부지원을계산하며등록기능0이다. S3전체실전효율/장기협상가격을2회슛으로인증하지않는다.','',
 'A08-S1의별도현재RTcost/slot family와에이전트자료전달은PR461에서root가검문했다. 여기서그계산을복제하지않으며계약결정·공동에이스·A08실전라이브패스권한은별도다. 중요한E2/전체시즌결과는후보다.','',
 '|번호|묶음|상태|','|---|---|---|','|1|2020드래프트연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23거래·계약|조건부비용·명단/중요방향미선택|','|4|장기커리어|후속시즌대기|','|5|결말·전체구조|한정실경기2표본후보·전체출구미완료|','|6|집필규격·ContextPack|현행등록기참조·Pack0|','|7|통합·독립·작가승인|최종CLOSED|','',
 '미완료큰묶음5 / v0.30 PARTIAL / 설계·원고CLOSED / 새기능등록0·원고0.',''])
def self_test():
 old=modeled_samples
 def wrong():
  r=old();r[1]['shot_outcome']='MADE';return r
 with patch(__name__+'.modeled_samples',side_effect=wrong):
  try:build();raise RuntimeError('FALSE_PASS retry_means_scoring_success')
  except AssertionError:pass
 def wrong():
  r=old();r[0]['return_recipient']='Suggs';return r
 with patch(__name__+'.modeled_samples',side_effect=wrong):
  try:build();raise RuntimeError('FALSE_PASS wrong_team_return_recipient')
  except AssertionError:pass
 return 2
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');args=ap.parse_args();o=build()
 if args.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
 if args.check:assert validate(load(OUT))==[]and text(MD)==markdown(o)
 print(json.dumps({'current':True,'new_game_samples':2,'source_team_minutes':480,'new_registry_functions':0,'controls':self_test()if args.self_test else None}))
