"""Join current nine-act finite exits to supplied episode designs, without LOCKs."""
from __future__ import annotations
import argparse,copy,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A='design/THREEPEAT_51_EPISODE_DENSITY_ALLOCATION_2026_10_12.json'
B='design/THREEPEAT_51_PREPARED_EPISODE_BLUEPRINTS_2026_10_12.json'
LATE='canon/DELEGATED_THREEPEAT_2024_25_USED_ROUTES_AND_FINAL_COURTS_SELECTION_2026_10_09.json'
LAST='simulation/THREEPEAT_2025_SHARED_FINAL_COURT_AND_LAST_ATTACK_PREPARATION_2026_10_09.json'
MAP='design/THREEPEAT_NINE_ACT_HISTORY_AND_PACK_EXIT_MAP_2026_10_09.json'
ACCEPT='canon/DELEGATED_THREEPEAT_NINE_ACT_EXIT_MAP_ACCEPTANCE_2026_10_09.json'
C01='research/THREEPEAT_C01_PUBLIC_AND_DUTY_USED_CALENDAR_PREPARATION_2026_10_09.json'
EPI='simulation/THREEPEAT_BRIEF_2035_EPILOGUE_CURRENT_SCOPE_JOIN_2026_10_09.json'
EARLY='canon/EARLY_REWARD_B_AUTHOR_SELECTION_2026_10_11.json'
O='design/THREEPEAT_CURRENT_USED_HISTORY_EXIT_JOIN_2026_10_12.json'
MD=O.replace('.json','.md')
R='reviews/THREEPEAT_CURRENT_USED_HISTORY_EXIT_JOIN_2026_10_12_CODEX_CHECK.json'
UNITS=[f'M{i:02}' for i in range(1,10)]+['EPI']
def norm(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()
def sha(p):return hashlib.sha256(norm(p)).hexdigest()
def load(p):return json.loads(norm(p))
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def ref(p,pointer=''):return {'path':p,'source_sha256':sha(p),'json_pointer':pointer}
def distinct(values):return list(dict.fromkeys(values))

# Distinct functions share one selected scene. They are not five fresh
# possessions, five winning shots, or an assertion that Rival's miss was known.
FINAL={
 35:('공 확보 뒤 다른 위협은 아직 살아 있다.','21.6초 실제수비리바운드 뒤16.6초전방진입·이양·공없는재참여를현재관찰로잇는다.','긴자기운반·독점마무리기회를줄이고다시움직일시간을쓴다.','공획득·전진·재참여는자기공로이나마지막점유·득점을보장하지않는다.',[21.6,16.6]),
 36:('23.6초MIN Rival의공·샷클록2.6. 슛과리바운드결과는미래다.','22.7초릴리스의보이는공과자기리바운드길을좇는다. Carter/Mark의Towns/Vanderbilt박스아웃을P의단독수비공로로바꾸지않는다.','자기위협위치와리바운드준비를동시에부담한다. 두빅맨의추가공격억제는동료의시간·전환선두포기다.','22.0초에실제로림미스를본뒤에만공의튐을읽는다. 공격리바운드counter권리는보존된다.',[23.6,22.7,22.0]),
 37:('Rival의회복과막힌직접공격앞에서초기패스는완성정답이아니다.','16.1초LM첫이양→LM독립반환12.8→P12.5수신→Carter11.5수신→Carter9.0반환→P8.6재수신을현재보이는행동으로만소비한다.','자기익숙한리듬을고집할기회와반복시간을쓴다. LM/Carter반환의독립선택권을남긴다.','공을다시받아도직접슛이자동으로열리지않는다. 다음LM이동은4.4초에보이는뒤에만읽는다.',[16.1,12.8,12.5,11.5,9.0,8.6,4.4]),
 38:('앞선B장면의자기공격능력은있어도현재Rival압박에서직접종료우위는없다.','보이는압박과LM재배치/통로에따라2.6초에최종이양을고른다. LM의2.0초수신후슛·드리블선택은LM몫이다.','자기최종슛·직접결승득점기회와결과통제권을내려놓는다.','최종공은넘겼지만유효슛·성공·검토·최종점수는아직모른다.',[4.4,2.6,2.0]),
 39:('마지막수신은득점이나승리확정이아니다.','LM0.2초독립릴리스→혼→유효2점/추가시간없음의선택가상검토→공개110–109/4–3종료→상호보이는고개행동순서로끝낸다.','P득점0·LM슛책임·LV/Mark/Carter의공간/박스아웃/연결비용을남긴다.','2025CHI삼연패·LM독립결승2점과보이는신뢰만. 개인상·완전화해·타인속마음은부여하지않는다.',[0.2,0.0])}

def make():
 a=load(A);b=load(B);episodes=a['episodes'];ports=[]
 ids=distinct(fc for e in episodes for fc in e['function_ids'])
 assert len(ids)==42
 for fc in ids:
  used=[e for e in episodes if fc in e['function_ids']];unit=used[0]['unit_id']
  epids=[e['proposed_episode'] for e in used]
  sources=[ref(A,f'/episodes/{ep-1}') for ep in epids]+[ref(B,f'/prepared_episode_blueprints/{ep-1}') for ep in epids]
  p={'port_id':fc,'unit_id':unit,'used_recommended_episodes':epids,
     'status':'SOURCE_JOINED_PREPARATION_PENDING_CURRENT_HISTORY_ACCEPTANCE',
     'entry_state':used[0]['entry_state'],'changed_action':' / '.join(distinct(e['action_choice'] for e in used)),
     'durable_cost':' / '.join(distinct(e['durable_cost'] for e in used)),
     'exit_state':used[-1]['state_change'],'source_refs':sources,
     'source_claim_class':'AUTHOR_MODELED_DESIGN_NOT_REAL_NBA_OR_INSTITUTIONAL_FACT',
     'consequential_choice_ids':['EARLY_REWARD_IMPLEMENTATION'] if fc in [f'FC{k:03}' for k in range(12,23)] else [],
     'unresolved_used_dependencies':distinct(d for e in used for d in e['unresolved_used_dependencies']),
     'new_history_LOCK_or_ACTUAL_authority':False}
  if fc in ('FC031','FC032','FC040'):
   p.update(status='HOLD_C01_USED_CALENDAR',consequential_choice_ids=['C01_CALENDAR'])
   p['source_refs'].append(ref(C01,'/finite_remaining_ports'))
  if fc.startswith('FC') and int(fc[2:]) in FINAL:
   entry,action,cost,exit_,times=FINAL[int(fc[2:])]
   p.update(entry_state=entry,changed_action=action,durable_cost=cost,exit_state=exit_,remaining_clock_support=times,
            source_function_is_not_independent_possession=True)
   p['source_refs'] += [ref(LATE,'/selected_2025_last_attack'),ref(LAST,'/last_attack_candidate/live_events'),ref(LAST,'/individual_choices_and_visible_costs')]
  if fc=='FC040':p['source_refs'].append(ref(EPI,'/ordered_epilogue_ports'))
  ports.append(p)
 units=[]
 for i,u in enumerate(UNITS):
  es=[e for e in episodes if e['unit_id']==u];owned=[p for p in ports if p['unit_id']==u]
  units.append({'unit_id':u,'entry_state':es[0]['entry_state'],'exit_state':es[-1]['state_change'],
    'first_recommended_episode':es[0]['proposed_episode'],'last_recommended_episode':es[-1]['proposed_episode'],
    'port_ids':[p['port_id'] for p in owned],
    'next_unit_id':UNITS[i+1] if i<9 else None,
    'next_entry_state':next((e['entry_state'] for e in episodes if i<9 and e['unit_id']==UNITS[i+1]),None),
    'outgoing_cost_not_refunded':es[-1]['durable_cost'],
    'unresolved_used_dependencies':distinct(d for p in owned for d in p['unresolved_used_dependencies']),
    'status':'PREPARED_CURRENT_BOUNDARY_NOT_SELECTED_HISTORY_LOCK',
    'source_refs':[ref(A,f'/episodes/{es[0]["proposed_episode"]-1}'),ref(A,f'/episodes/{es[-1]["proposed_episode"]-1}')]})
 old=load(MAP)['nine_act_and_epilogue_exit_to_entry_rows']
 return {'id':'THREEPEAT_CURRENT_USED_HISTORY_EXIT_JOIN_2026_10_12','producer_id':'root_codex',
  'status':'CURRENT_42_PORT_AND_TEN_UNIT_HISTORY_JOIN_PREPARED_NOT_LOCKED',
  'baseline_main':'944f7677a097448410f8a4c6dd74dcde95d0e37a',
  'scope':'M01–M09 and brief2035EPI;42ports=40functions+2already-selected2025transitions, not original42SubActs',
  'source_sha256':{p:sha(p) for p in [A,B,LATE,LAST,MAP,ACCEPT,C01,EPI,EARLY]},
  'finite_used_exit_ports':ports,'unit_exits':units,
  'current_final_function_phase_order':['FC036','FC035','FC037','FC038','FC039'],
  'last_scene_clock_support':'MIN possession23.6→Rival release22.7→rim22.0→CHIrebound21.6→CHIfrontcourt16.6→LMrelease0.2→horn/review/publicend/nod',
  'boundary_changes_from_original_map':[{'unit_id':'M02','prior_literal_exit':old[1]['literal_exit'],'current_exit':units[1]['exit_state'],'institutional_order_consumed_in':'M03 currentepisode9 I1→I2→I3→I4, not college approval before ownreceipt'},
   {'unit_id':'M04','prior_window':old[3]['literal_source_window'],'current_window':'2018–19 rookie and2019–20 ownattack/rival publiccomparison beforeLM2020core','new_season_result_selected':False},
   {'unit_id':'M09','prior_literal_exit':old[8]['literal_exit'],'current_exit':units[8]['exit_state'],'current_selection_ref':ref(LATE,'/selected_2025_last_attack'),'old_birth_candidate_as_current_pending':False}],
  'C01_calendar_ports_remaining':['FC031','FC032','FC040'],
  'consequential_choice_preparation':[{'choice_id':'EARLY_REWARD_IMPLEMENTATION','direction':'B_SELECTED','source_ref':ref(EARLY),'used_port_ids':[f'FC{k:03}' for k in range(12,23)],'status':'DIRECTION_AND_WORKING_INPUTS_PREPARED_NOT_COMPILER_SELECTION_EXPORT'},
   {'choice_id':'C01_CALENDAR','status':'UNSELECTED_USED_CALENDAR_HOLD','source_ref':ref(C01,'/finite_remaining_ports'),'used_port_ids':['FC031','FC032','FC040']}],
  'personal_awards_use_mode':'NOT_USED','lifetime_title_total_through2035':None,
  'final_episode_N':None,'current_used_scope_complete':False,'independent_review_completed':False,
  'actual_Blueprint_authority_count':0,'actual_Pack_count':0,'prose_count':0,
  'gates':{'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False},
  'tools_this_pass':{'Codex':'DIRECT_SOURCE_JOIN_REPAIR_LOCAL_CHECK','Antigravity':'NOT_RUN','NotebookLM':'NOT_RUN_CURRENT_GENERATION','Claude':'NOT_RUN','independent_agent':'NOT_RUN'},
  'remaining':'C01 path/used dates and independent current-history/access acceptance; finalN/categorypolicy/actualauthority then compiler. No original14/42 or ten-year annual ledger expansion.',
  'unfinished_major_groups':4,'unfinished_through_group6':3}

def validate(d):
 a=load(A);b=load(B);ports=d['finite_used_exit_ports'];units=d['unit_exits'];ids=[p['port_id'] for p in ports]
 assert len(ports)==len(set(ids))==42
 assert set(ids)=={fc for e in a['episodes'] for fc in e['function_ids']}
 assert [u['unit_id'] for u in units]==UNITS
 for p in ports:
  for k in ('entry_state','changed_action','durable_cost','exit_state'):assert p[k]
  assert p['used_recommended_episodes']==[e['proposed_episode'] for e in a['episodes'] if p['port_id'] in e['function_ids']]
  assert all(a['episodes'][n-1]['unit_id']==p['unit_id'] for n in p['used_recommended_episodes'])
  for r in p['source_refs']:
   assert sha(r['path'])==r['source_sha256'];v=load(r['path'])
   for t in r['json_pointer'].split('/')[1:]:v=v[int(t)] if isinstance(v,list) else v[t]
 for i,u in enumerate(units):
  es=[e for e in a['episodes'] if e['unit_id']==u['unit_id']]
  assert u['entry_state']==es[0]['entry_state'] and u['exit_state']==es[-1]['state_change']
  assert set(u['port_ids'])=={p['port_id'] for p in ports if p['unit_id']==u['unit_id']}
  assert u['next_unit_id']==(UNITS[i+1] if i<9 else None)
  assert u['next_entry_state']==(units[i+1]['entry_state'] if i<9 else None)
 assert [p['port_id'] for p in ports if p['status']=='HOLD_C01_USED_CALENDAR']==['FC031','FC032','FC040']
 assert d['current_used_scope_complete'] is False and not d['independent_review_completed']
 assert d['final_episode_N'] is None and d['actual_Pack_count']==d['actual_Blueprint_authority_count']==d['prose_count']==0
 assert d['personal_awards_use_mode']=='NOT_USED' and d['lifetime_title_total_through2035'] is None
 by={p['port_id']:p for p in ports}
 assert d['current_final_function_phase_order']==['FC036','FC035','FC037','FC038','FC039']
 assert by['FC036']['remaining_clock_support']==[23.6,22.7,22.0]
 assert '미스' in by['FC036']['exit_state']
 assert by['FC035']['remaining_clock_support']==[21.6,16.6]
 source_clock={e['remaining_game_seconds'] for e in load(LAST)['last_attack_candidate']['live_events']}
 assert all(t in source_clock for p in ports for t in p.get('remaining_clock_support',[]))
 assert '유효슛·성공·검토·최종점수는아직모른다' in by['FC038']['exit_state']
 assert all(by[f'FC{k:03}']['used_recommended_episodes']==[50] for k in range(35,40))
 assert len(b['prepared_episode_blueprints'][49]['named_acquisition_checkpoints'])==9
 assert set(d['source_sha256'])=={A,B,LATE,LAST,MAP,ACCEPT,C01,EPI,EARLY}
 assert all(sha(p)==h for p,h in d['source_sha256'].items())

def render(d):
 lines=['# 현재9막·후일담 역사 출구 연결','',
 '**현재51회차 준비안에 맞춘42개 출구·10단위 연결이다. 역사 LOCK/최종N/ACTUAL/Pack이 아니다.**','',
 '42는 원42소막의 재현이 아니라40기능+이미선택된2025진입2개다. 분할된 회차는 같은 기능의 서로 다른 상태를 소비하며, 마지막5기능은 한 회차의 다른 역할로 겹쳐 쓰인다.','',
 '## 현재 경계','', '|막|권고 회차|출구|다음 진입|남은 사용 의존성|','|---|---|---|---|---|']
 for u in d['unit_exits']:
  lines.append('|'+ '|'.join([u['unit_id'],f'{u["first_recommended_episode"]}–{u["last_recommended_episode"]}',u['exit_state'],u['next_entry_state'] or '종결',','.join(u['unresolved_used_dependencies']) or '현재수락/정보접근검수'])+'|')
 lines+=['','## 제도·시간과 역할 경계','',
 '- M02는 오퍼/대학 자격 이전 평가·학업 진행에서 닫히고, M03의권고9가 I1→I2→I3→I4를 수행한다. 학교가자료를보내는일을EC승인으로바꾸지않는다.',
 '- M04는 신인 및2년차 공격·공개라이벌비교를소비하고M05의2020LM코어로넘어간다. 22–43/21–44는미선택이며정확기록을인물지식으로추가하지않는다.',
 '- 마지막회차의역할순서는FC036수비→FC035획득/전진→FC037경로전환→FC038직접종료대이양→FC039독립마무리/검토다. 기능번호를게임시계순서로읽지않는다.',
 '- MIN23.6초점유에서P는미스를모른다.22.7릴리스→22.0림미스→21.6실제CHI획득순서를따른다. 이는이미선택된원시계의복원이며새플레이추가가아니다.',
 '- CHI점유는21.6초부터이고샷클록OFF다. MIN의23.6초샷클록2.6을CHI새24초로옮기지않는다.',
 '- 자기공격능력의대조는앞선B장면의설치이며최종공격에서P의새클러치득점을만들지않는다. LM0.2초릴리스와유효2점/110–109확인은혼·검토뒤구별한다.',
 '- C01 FC031/032/040은사용달력HOLD. 준비·사적과제·guest를기관승인/금메달/복무완료로바꾸지않는다. 2035후일담은3일의유한의무조건이며중간10년전수원장을새로요구하지않는다.','',
 '## 출구별 실제 소비','']
 for p in d['finite_used_exit_ports']:
  lines+=[f'### {p["port_id"]} · {p["unit_id"]} · 권고{p["used_recommended_episodes"]}', '',f'- 진입: {p["entry_state"]}',f'- 선택/행동: {p["changed_action"]}',f'- 비용: {p["durable_cost"]}',f'- 출구: {p["exit_state"]}',f'- 상태: {p["status"]}','']
 lines+=['## 검증과 남은 일','',
 '현재9출처핀·42기능소비·10막의9연결·마지막5기능의독립역할/시간·C01역방향의존성을Codex가대조했다. 신규외부도구/독립검수/원고/Pack0. 최종권위발급전현재출구·취득·C01사용상태의독립수락이필요하다.','',
 '|번호|작업|상태|','|---|---|---|','|1|드래프트|완료|','|2|Chicago2020–21|완료|','|3|거래·계약|완료|','|4|커리어·B|인정/대표팀경로남음|','|5|구조|현재42출구·10막연결준비/최종N미LOCK|','|6|규격·Pack|51개별설계/최종수락·Pack미완료|','|7|통합·독립·작가승인|미완료|','',
 '미완료4개·6번까지3개·v0.30 PARTIAL/CLOSED.','']
 return '\n'.join(lines).encode()

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
 d=make();validate(d);rejected=[]
 def bad_hold(x):x['finite_used_exit_ports'][30]['status']='SELECTED_RESOLVED'
 def bad_release(x):next(p for p in x['finite_used_exit_ports'] if p['port_id']=='FC038')['exit_state']='LM성공과최종승리를이양순간이미안다.'
 for name,mut in [('COLLEGE_BEFORE_RECEIPT',lambda x:x['unit_exits'][1].update(exit_state='이미EC승인된대학생')),
   ('NEXT_ENTRY_MISMATCH',lambda x:x['unit_exits'][6].update(next_entry_state='옛2028첫우승이후')),
   ('C01_SILENTLY_RESOLVED',bad_hold),('RIVAL_DEFENSE_AFTER_REBOUND',lambda x:x.update(current_final_function_phase_order=['FC035','FC036','FC037','FC038','FC039'])),
   ('LM_WIN_KNOWN_AT_YIELD',bad_release),('FALSE_WHOLE_HISTORY_COMPLETE',lambda x:x.update(current_used_scope_complete=True))]:
  x=copy.deepcopy(d);mut(x)
  try:validate(x)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('false pass '+name)
 files={O:enc(d),MD:render(d)}
 review={'id':'THREEPEAT_CURRENT_USED_HISTORY_EXIT_JOIN_2026_10_12_CODEX_CHECK','status':'LOCAL_CURRENT_EXIT_JOIN_CHECK_NOT_INDEPENDENT_ACCEPTANCE','producer_id':'root_codex',
  'input_source_sha256':d['source_sha256'],'port_count':42,'unit_count':10,'transition_count':9,'C01_used_ports_remaining':3,
  'rejected_counterexamples':rejected,'output_LF_SHA256':{p:hashlib.sha256(c).hexdigest() for p,c in files.items()},
  'independent_review_completed':False,'actual_Pack_count':0,'prose_count':0}
 files[R]=enc(review)
 for p,data in files.items():
  path=ROOT/p
  if path.exists():assert norm(p)==data,('refuse different existing output',p)
  else:assert not args.check,('missing output',p);path.write_bytes(data)
 print(json.dumps({'mode':'check' if args.check else 'write','ports':42,'units':10,'transitions':9,'C01_remaining':3,'rejected':rejected,'Pack':0}))
if __name__=='__main__':main()
