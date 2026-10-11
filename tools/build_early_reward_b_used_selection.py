"""Export the existing delegated B working implementation as a typed choice.

This selects repository fiction-model consumption, never awards or observed
player boxes. It neither issues current-history/Pack authority nor review.
"""
from pathlib import Path
import argparse,csv,hashlib,io,json,subprocess
from fractions import Fraction
from build_threepeat_actual_context_packs import selected_record

ROOT=Path(__file__).resolve().parents[1]
AUTHOR='canon/EARLY_REWARD_B_AUTHOR_SELECTION_2026_10_11.json'
DELEGATE='canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
POLICY='control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md'
FULL='simulation/EARLY_REWARD_B_CURRENT_FULL_ROLE_INPUTS_2026_10_12.json'
FULLCSV=FULL.replace('.json','.csv')
JOINT='simulation/EARLY_REWARD_B_JOINT_RESULT_RESPONSE_2026_10_12.json'
WORK=JOINT.replace('.json','_WORKING.csv')
Y13='simulation/EARLY_REWARD_B_YEAR1_YEAR3_DATED_ATTACK_2026_10_12.csv'
Y2='simulation/EARLY_REWARD_B_YEAR2_DATED_SHOTS_2026_10_11.csv'
Y4='simulation/EARLY_REWARD_B_YEAR4_DATED_ATTACK_2026_10_11.csv'
GROW='design/EARLY_REWARD_B_2023_CUMULATIVE_GROWTH_JOIN_2026_10_12.json'
OUT='canon/EARLY_REWARD_B_USED_IMPLEMENTATION_SELECTION_2026_10_12.json'
MD=OUT.replace('.json','.md')
REVIEW='reviews/EARLY_REWARD_B_USED_IMPLEMENTATION_SELECTION_2026_10_12_CODEX_CHECK.json'
PORTS=[f'FC{k:03}' for k in range(12,23)]

def norm(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()
def sha(p):return hashlib.sha256(norm(p)).hexdigest()
def load(p):return json.loads(norm(p))
def encode(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def rows(p):return list(csv.DictReader(io.StringIO(norm(p).decode())))
def ref(p,pointer=''):
 d={'path':p,'source_sha256':sha(p),'json_pointer':pointer}
 if not p.endswith('.json'):d.update(format='UTF8_TEXT',text_locator={'kind':'WHOLE_TEXT'})
 return d

def build():
 author=load(AUTHOR);full=load(FULL);joint=load(JOINT);grow=load(GROW)
 assert author['B']['selected_option']=='B' and author['B']['selected_individual_awards']==[]
 assert full['rows']==len(rows(FULLCSV))==292
 for source in (full,joint,grow):
  assert all(sha(p)==h for p,h in source['source_sha256'].items()),source['id']
 assert full['allocation_LF_SHA256']==sha(FULLCSV)
 assert all(sha(p)==h for p,h in joint['output_LF_SHA256'].items())
 working=joint['proposed_bounded_working_family'];wr=rows(WORK)
 assert working['status']=='SELECTED_ROUTINE_WORKING_FICTIONAL_MODEL_NOT_PERSONAL_AWARD_OR_CANON_SCORE'
 assert working['P_total_delta']=='1/2' and working['debit_actor_total_delta_each']=='-1/8'
 assert len(working['results'])==12 and joint['coefficient_rows']==len(wr)==821
 for row in wr:
  shift=Fraction(row['P_rating_delta_coefficient'])/2-Fraction(row['debit_group_rating_delta_coefficient'])/8
  assert Fraction(row['working_shift'])==shift
  assert Fraction(row['working_CHI_low'])==Fraction(row['base_CHI_low'])+shift
  assert Fraction(row['working_CHI_high'])==Fraction(row['base_CHI_high'])+shift
  assert row['working_wl']==row['base_wl']
 assert all(r['all_old_directions_preserved'] for r in working['results'])
 assert len(grow['selected82_replay'])==82 and all(r['additional_B_rating_or_score_delta']==0 for r in grow['selected82_replay'])
 wanted=['YEAR1_73_ROLE_DATES','YEAR2_MIP_ELIGIBLE_65_DATES','YEAR3_SELECTED72_ROLE_MODEL','YEAR4_REGULATION82']
 summaries=[next(s for s in full['summaries'] if s['scope']==key) for key in wanted]
 assert [s['positive_role_dates'] for s in summaries]==[73,65,72,82]
 inputs=[AUTHOR,DELEGATE,POLICY,FULL,FULLCSV,JOINT,WORK,Y13,Y2,Y4,GROW]
 resolution='B1–4년차의 날짜별 자기 공격·동료 기회 비용과 기존 비득점 기대 prior를 명시적 가상 작업 입력으로 사용한다. 총영향 P+1/2·실제 기회비용 동료각−1/8은 기존 선택 승패 방향을 보존하는 위임 모델이며 실측 평점이 아니다. 연차별 인정 경쟁은 사용하되 실제 수상·득표·정수 박스 기록은 사용하지 않는다. 2023 누적 성장에 B 보너스를 다시 더하지 않는다.'
 d={'id':'EARLY_REWARD_B_USED_IMPLEMENTATION_SELECTION_2026_10_12','choice_id':'EARLY_REWARD_IMPLEMENTATION',
    'kind':'EARLY_CAREER_REWARD','selected':True,'status':'SELECTED_FICTIONAL_USED_RESOLUTION',
    'authority_class':'DELEGATED_SELECTED','producer_id':'root_codex',
    'baseline_main':'7f68c712dd54e9020972eeac9686f102fd01d722','resolution':resolution,
    'unresolved_used_dependencies':[],'used_port_ids':PORTS,'covered_exit_port_ids':PORTS,
    'authority_basis':{'B_direction_ref':ref(AUTHOR,'/B'),'delegated_model_ref':ref(DELEGATE),'scope_interpretation_ref':ref(POLICY),
      'scope':'Normalize already implemented routine working-model use under selected B and delegated season execution. No new human award/medal/final-gate selection.'},
    'source_sha256':{p:sha(p) for p in inputs},'implementation_refs':[ref(p) for p in inputs if p not in (AUTHOR,DELEGATE,POLICY)],
    'dated_working_role_inputs':{'positive_P_role_dates':292,'full_role_input_ref':ref(FULL),'expected_season_summaries':summaries,
      'epistemic_mode':'AUTHOR_MODELED_EXPECTATION_INPUT_NOT_OBSERVED_INTEGER_BOXSCORE',
      'joint_REB_AST_event_ownership_certified':False,
      'non_scoring_use_boundary':'Explicit carry of prior expectations, not a claim that every rebound/assist/opponent event has been jointly assigned. Pack FACT or public player-knowledge claims may not use these expectations as realized records.'},
    'declared_total_impact_model':{'P_total_delta':'1/2','debit_actor_total_delta_each':'-1/8','coefficient_rows':821,'model_families':12,
      'source_ref':ref(JOINT,'/proposed_bounded_working_family'),'exact_box_to_rating_conversion':False,
      'old_game_directions_preserved':True,'new_exact_game_scores_selected':False},
    'recognition_use':{'mode':'COMPETITION_ONLY','announcement_outcomes_selected':False,'personal_award_use_mode':'NOT_USED',
      'selected_personal_awards':[],'fictional_ballot_totals_selected':False,'HigherMax_condition_changed':False},
    'preserved':{'year2_exact_record_selected':False,'year2_current_range':[21,22],'year2_seed7_pick4_LaMelo':True,
      'existing_minutes_and_start_rights':True,'contracts_and_postseason_routes':True,'2023_cumulative_additional_B_delta':0,
      'C01_medal_duty_calendar_selected':False,'original_source_bytes_rewritten':False},
    'authority_boundary':{'current_history_LOCK_issued':False,'independent_review_completed':False,'final_episode_N':None,
      'actual_Blueprint_count':0,'actual_Pack_count':0,'prose_count':0,
      'empty_dependencies_scope':'Only this working B implementation choice. C01 and final/current-generation review gates remain outside this resolved choice.'},
    'gates':{'manuscript_allowed':False,'design_gate':'CLOSED','freeze':'v0.30 PARTIAL'},
    'tools_this_pass':{'Codex':'LOCAL_SOURCE_REPLAY_AND_TYPED_SELECTION_EXPORT','Antigravity':'NOT_RUN','NotebookLM':'NOT_RUN','Claude':'NOT_RUN','independent_agent':'NOT_RUN'}}
 validate(d)
 lines=['# B안의 실제 사용 작업 모델 선택','',
  'B 방향과 기존 위임으로 이미 구현한 작업 입력을 Pack이 읽을 수 있는 선택 객체로 연결했다. 새로운 수상·금메달·최종 회차 수를 선택한 문서는 아니다.','',
  '## 선택한 사용 범위','',resolution,'',
  '|NBA 연차|시즌|기존 역할 날짜|기대 득점/경기|인정 경쟁|','|---|---|---|---|---|']
 for i,s in enumerate(summaries,1):lines.append(f'|{i}|{2017+i}–{str(2018+i)[-2:]}|{s["positive_role_dates"]}|{s["expected_per_game"]["pts"]:.2f}|'+['올루키','MIP','올스타','올스타·All-NBA'][i-1]+'|')
 lines+=['','위 수치는 작가용 기대 입력이며 실제 정수 박스 기록이나 선수의 현재 지식이 아니다. 리바운드·어시스트 사건의 공동 귀속까지 인증하지 않는다. 분·시작권·동료 기회 비용과 각 발표 이전 정보 창을 유지한다.','',
  '821개 영향 행을 분수로 재계산해 12개 기존 모델의 방향 보존을 확인했다. 2년차21–22승 범위의 정확 기록은 여전히 미선택이며, 2023 누적 성장에는 B 점수/평점 보너스0을 유지한다.','',
  '## 후행 연결','',
  '- 사용 포트: FC012–FC022(11개). 정규 수상은 NOT_USED; 경쟁 기능은 사용한다.',
  '- 현행 역사 연결이 이 원 선택 객체의 path/hash/pointer/resolution을 참조한다.',
  '- C01 FC031/032/040의 달력, 최종N·분류 정책, 현행 개별 설계의 독립 수락과 실제 Pack은 남는다.',
  '- 원고0·Pack0·v0.30 PARTIAL/CLOSED. 신규 외부 CLI·독립검수0.','']
 return d,'\n'.join(lines).encode()

def validate(d):
 selected_record(d,'EARLY_CAREER_REWARD')
 assert d['authority_class']=='DELEGATED_SELECTED' and d['used_port_ids']==PORTS
 assert d['recognition_use']['personal_award_use_mode']=='NOT_USED' and not d['recognition_use']['selected_personal_awards']
 assert not d['recognition_use']['announcement_outcomes_selected']
 assert not d['preserved']['year2_exact_record_selected'] and not d['preserved']['C01_medal_duty_calendar_selected']
 assert d['preserved']['2023_cumulative_additional_B_delta']==0
 assert not d['authority_boundary']['independent_review_completed'] and d['authority_boundary']['actual_Pack_count']==0
 assert all(sha(p)==h for p,h in d['source_sha256'].items())

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
 d,md=build();files={OUT:encode(d),MD:md}
 review={'id':'EARLY_REWARD_B_USED_IMPLEMENTATION_SELECTION_2026_10_12_CODEX_CHECK',
  'status':'LOCAL_TYPED_WORKING_SELECTION_CHECK_NOT_INDEPENDENT_ACCEPTANCE','producer_id':'root_codex',
  'source_sha256':d['source_sha256'],'positive_role_dates':292,'impact_rows_recomputed':821,'preserved_model_families':12,
  'current_2023_no_bonus_rows':82,'used_B_ports':11,'selected_record_contract_passed':True,
  'personal_awards_used':False,'C01_selected':False,'current_independent_review_completed':False,'actual_Pack_count':0,
  'output_LF_SHA256':{p:hashlib.sha256(raw).hexdigest() for p,raw in files.items()}}
 files[REVIEW]=encode(review)
 for p,raw in files.items():
  if (ROOT/p).exists():assert norm(p)==raw,('refuse different output',p)
  else:assert not args.check,('missing output',p)
 if not args.check:
  for p,raw in files.items():
   if not (ROOT/p).exists():
    with (ROOT/p).open('xb') as handle:handle.write(raw)
 print(json.dumps({'mode':'check' if args.check else 'write','B_used_choice_selected':True,'role_dates':292,'impact_rows':821,'families':12,'C01_selected':False,'Pack':0}))

if __name__=='__main__':main()
