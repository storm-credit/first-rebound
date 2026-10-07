"""Preserve the 46-function snapshot and consume reviewed A10 S2/S3."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import argparse,json
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_g13_a10_three_function_register.py'
BASE='control/G13_A10_FUNCTION_EXECUTION_REGISTER_2026_10_08.json'
BASE_PEER='reviews/G13_A10_FUNCTION_EXECUTION_REGISTER_G11_INDEPENDENT_REVIEW_2026_10_08.json'
NEW='design/A10_S2_S3_LOCAL_FUNCTION_SUPPORT_2026_10_08.json'
PEER='reviews/A10_S2_S3_LOCAL_FUNCTION_SUPPORT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json'
OUT='control/G13_A10_THREE_FUNCTION_REGISTER_2026_10_08.json';MD=OUT[:-5]+'.md'
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def h(p):return sha256(text(p).encode()).hexdigest()
def load(root,p):return json.loads(text(root/p))
def build(root=ROOT):
 b,f,bp,p=(load(root,q)for q in [BASE,NEW,BASE_PEER,PEER])
 for path,obj in zip([BASE,NEW,BASE_PEER,PEER],[b,f,bp,p]):
  assert obj==json.loads(text(root/path)),'Returned object differs from physical '+path
  for q,pin in obj['source_sha256'].items():assert h(root/q)==pin,'Source stale '+q
 assert bp['independent_review_completed']and p['independent_review_completed']
 assert b['counts']['registered_local_functions']==46 and len(b['functions'])==46
 assert f['fictional_practice_co_presence_selected']and not f['actual_2024_25_health_contract_roster_or_NBA_game_certified']
 assert len(f['functions'])==2
 v=deepcopy(b);rows=v['functions']
 for i,new in enumerate(f['functions']):
  assert new['global_function_order']==47+i and new['episode_function_id']==f'A10-EF-00{i+2}'
  assert new['planned_allocation_slot']==514+i and new['primary_subact']==f'A10-S{i+2}'
  assert new['previous_function']['id']==rows[-1]['id']and new['entry_state']==new['previous_function']['exact_full_exit']==rows[-1]['exact_exit']
  assert new['direct_present_cost']and len(new['beats'])>=2 and all(q['action']and q['observed_other']for q in new['beats'])
  assert all(new[k]is False for k in ['whole_A10_complete','whole_g13_complete','whole_g14_complete','manuscript_allowed','new_MVP_year_title_team_move_or_major_author_result'])
  rows.append({'id':new['episode_function_id'],'path':NEW,'record_pointer':f'/functions/{i}','order':47+i,'planned_slot':514+i,'act':'A10','subact':new['primary_subact'],'exact_entry':new['entry_state'],'exact_exit':new['exit_state'],'acceptance_review':PEER})
 assert len({q['planned_slot']for q in rows})==48 and len({q['subact']for q in rows})==30
 v['schema']='G13_A10_THREE_FUNCTION_REGISTER_V1'
 v['source_sha256']={**b['source_sha256'],**f['source_sha256'],BASE:h(root/BASE),BASE_PEER:h(root/BASE_PEER),NEW:h(root/NEW),PEER:h(root/PEER),SELF:h(root/SELF)}
 v['counts'].update(registered_local_functions=48,per_act=dict(Counter(q['act']for q in rows)),subacts_with_verified_local_function_route=30,subacts_without_verified_local_function_route=12,unassigned_planned_slots=732,source_pin_count_including_current_consumer=len(v['source_sha256']))
 v['prior_46_register_immutable']=True
 v['new_A10_three_function_scope']='A10 S1/S2/S3 selected local private practice routes; the full priority-core/title-window CP2 exits and 2024-25 league outcome remain unselected.'
 return v
def markdown(v):
 lines=['# G13 현행 등록 · A10 세 소막의 국소 기능','','원46개 기능을 그대로 보존하고 독립검문한 A10EF002/003을47/48에 연결했다. **48기능·30소막 경로·미경로12소막**이다. 국소경로 등록이 전체소막 출구의 달성이나 우승창 성공은 아니다.','','[원46등록](G13_A10_FUNCTION_EXECUTION_REGISTER_2026_10_08.md) · [후속기능](../design/A10_S2_S3_LOCAL_FUNCTION_SUPPORT_2026_10_08.md) · [독립검문](../'+PEER+')','','| 순서 | 기능 | 소막 | 계획slot |','|---|---|---|---|']
 lines += [f"| {q['order']} | {q['id']} | {q['subact']} | {q['planned_slot']} |"for q in v['functions']]
 lines += ['','732미배정 계획칸은732개 추가사건 의무가 아니다. 전체G13/G14 미완료·실제Pack0·원고0·v0.30 PARTIAL·CLOSED. 미완료큰묶음5/6번까지4.','']
 return '\n'.join(lines)
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if a.check:assert load(ROOT,OUT)==v and text(ROOT/MD)==markdown(v),'Saved register stale'
 print(json.dumps({'current':True,'counts':v['counts']}))
if __name__=='__main__':main()
