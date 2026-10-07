"""Consume reviewed A11 local function; preserve immutable prior48 snapshot."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import argparse,json
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_g13_a11_function_execution_register.py'
BASE='control/G13_A10_THREE_FUNCTION_REGISTER_2026_10_08.json'
BASE_PEER='reviews/G13_A10_THREE_FUNCTION_REGISTER_G11_INDEPENDENT_REVIEW_2026_10_08.json'
NEW='design/A11_E1_FINAL_EPISODE_FUNCTION.json'
PEER='reviews/A11_E1_FINAL_EPISODE_FUNCTION_G11_INDEPENDENT_REVIEW_2026_10_08.json'
OUT='control/G13_A11_FUNCTION_EXECUTION_REGISTER_2026_10_08.json';MD=OUT[:-5]+'.md'
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def h(p):return sha256(text(p).encode()).hexdigest()
def load(root,p):return json.loads(text(root/p))
def build(root=ROOT):
 b,f,bp,p=(load(root,q)for q in [BASE,NEW,BASE_PEER,PEER])
 for path,obj in zip([BASE,NEW,BASE_PEER,PEER],[b,f,bp,p]):
  assert obj==json.loads(text(root/path)),'Returned object differs from physical '+path
  for q,pin in obj['source_sha256'].items():assert h(root/q)==pin,'Source stale '+q
 assert bp['independent_review_completed']and p['independent_review_completed']
 assert b['counts']['registered_local_functions']==48 and len(b['functions'])==48
 assert f['episode_function_id']=='A11-EF-001'and f['global_function_order']==49
 assert f['planned_allocation_slot']==583 and f['primary_subact']=='A11-S1'
 assert f['previous_function']['id']==b['functions'][-1]['id']=='A10-EF-003'
 assert f['entry_state']==f['previous_function']['exact_full_exit']==b['functions'][-1]['exact_exit']
 assert f['source_conditional_function']=='A11-CF01'and f['source_selected_routine']=='A11-RF-001'
 assert f['bounded_off_ball_reposition_observed']and len(f['beats'])==2 and f['direct_present_cost']
 assert f['beats'][0]['visible_failure']and f['beats'][1]['visible_correction']
 assert all(f[k]is False for k in ['whole_A11_S1_sustained_impact_certified','actual_2025_26_NBA_game_score_minutes_or_health_certified','MVP_year_or_Finals_loss_selected','new_major_author_result_or_team_move_selected','whole_A11_complete','whole_g13_complete','whole_g14_complete','manuscript_allowed','new_author_lock'])
 assert f['actual_context_packs']==0 and f['manuscript_count']==0 and f['design_gate']=='CLOSED'
 v=deepcopy(b);rows=v['functions']
 rows.append({'id':f['episode_function_id'],'path':NEW,'order':49,'planned_slot':583,'act':'A11','subact':'A11-S1','exact_entry':f['entry_state'],'exact_exit':f['exit_state'],'acceptance_review':PEER})
 assert len({q['planned_slot']for q in rows})==49 and len({q['subact']for q in rows})==31
 v['schema']='G13_A11_FUNCTION_EXECUTION_REGISTER_V1'
 v['source_sha256']={**b['source_sha256'],**f['source_sha256'],BASE:h(root/BASE),BASE_PEER:h(root/BASE_PEER),NEW:h(root/NEW),PEER:h(root/PEER),SELF:h(root/SELF)}
 v['counts'].update(registered_local_functions=49,per_act=dict(Counter(q['act']for q in rows)),subacts_with_verified_local_function_route=31,subacts_without_verified_local_function_route=11,unassigned_planned_slots=731,source_pin_count_including_current_consumer=len(v['source_sha256']))
 v['prior_48_register_immutable']=True
 v['new_A11_function_scope']='One selected private practice failure/correction observes off-ball reposition once. Whole sustained impact, season roster/health, MVP year and Finals result remain unselected.'
 return v
def markdown(v):
 lines=['# G13 현행 등록 · A11 첫 국소 기능','','독립검문된 A11EF001을 정확한 A10EF003 출구에서 기능49에 연결했다. 원48기능은 보존한다. **49기능·31소막 경로·미경로11소막**이다. 한 훈련의 위치 수정이 전체소막의 지속효율·시즌 성과를 증명하지 않는다.','','[원48등록](G13_A10_THREE_FUNCTION_REGISTER_2026_10_08.md) · [A11기능](../design/A11_E1_FINAL_EPISODE_FUNCTION.md) · [독립검문](../'+PEER+')','','| 순서 | 기능 | 소막 | 계획slot |','|---|---|---|---|']
 lines += [f"| {q['order']} | {q['id']} | {q['subact']} | {q['planned_slot']} |"for q in v['functions']]
 lines += ['',f"직접원천{v['counts']['source_pin_count_including_current_consumer']}개. 731미배정 계획칸은731새사건 의무가 아니다. 전체G13/G14 미완료·실제Pack0·원고0·v0.30 PARTIAL·CLOSED. 미완료큰묶음5/6번까지4.",'']
 return '\n'.join(lines)
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if a.check:assert load(ROOT,OUT)==v and text(ROOT/MD)==markdown(v),'Saved register stale'
 print(json.dumps({'current':True,'counts':v['counts']}))
if __name__=='__main__':main()
