"""Extend the immutable reviewed 45-function snapshot with reviewed A10 E1."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import argparse,json
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_g13_a10_function_execution_register.py'
BASE='control/G13_CURRENT_FUNCTION_EXECUTION_REGISTER_2026_10_08.json'
BASE_PEER='reviews/G13_CURRENT_FUNCTION_EXECUTION_REGISTER_G11_INDEPENDENT_REVIEW_2026_10_08.json'
NEW='design/A10_E1_FINAL_EPISODE_FUNCTION.json'
PEER='reviews/A10_E1_FINAL_EPISODE_FUNCTION_ROOT_INDEPENDENT_REVIEW_2026_10_08.json'
OUT='control/G13_A10_FUNCTION_EXECUTION_REGISTER_2026_10_08.json';MD=OUT[:-5]+'.md'
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def h(p):return sha256(text(p).encode()).hexdigest()
def load(root,p):return json.loads(text(root/p))
def checked(root,p):
 v=load(root,p);assert v==json.loads(text(root/p)),'Physical source differs '+p;return v
def build(root=ROOT):
 b=checked(root,BASE);f=checked(root,NEW);bp=checked(root,BASE_PEER);p=checked(root,PEER)
 for path,value in zip([BASE,NEW,BASE_PEER,PEER],[b,f,bp,p]):
  assert value==json.loads(text(root/path)),'Returned consumer object differs from physical '+path
 assert bp['independent_review_completed']and p['independent_review_completed']
 for obj in [b,f,bp,p]:
  for path,pin in obj['source_sha256'].items():assert h(root/path)==pin,'Source stale '+path
 assert b['counts']['registered_local_functions']==45 and len(b['functions'])==45
 assert f['global_function_order']==46 and f['episode_function_id']=='A10-EF-001'
 assert f['entry_state']==f['previous_function']['exact_full_exit']==b['functions'][-1]['exact_exit']
 assert f['planned_allocation_slot']==513 and f['primary_subact']=='A10-S1'
 assert f['direct_present_cost']and len(f['beats'])==2
 assert all(f[k]is False for k in ['whole_A10_complete','whole_g13_complete','whole_g14_complete','manuscript_allowed','new_MVP_year_title_team_move_or_major_author_result'])
 v=deepcopy(b);rows=v['functions'];rows.append({'id':f['episode_function_id'],'path':NEW,'record_pointer':'','order':46,'planned_slot':513,'act':'A10','subact':f['primary_subact'],'exact_entry':f['entry_state'],'exact_exit':f['exit_state'],'acceptance_review':PEER})
 assert len({q['planned_slot']for q in rows})==46 and len({q['subact']for q in rows})==28
 v['schema']='G13_A10_FUNCTION_EXECUTION_REGISTER_V1'
 v['source_sha256']={**b['source_sha256'],**f['source_sha256'],BASE:h(root/BASE),BASE_PEER:h(root/BASE_PEER),NEW:h(root/NEW),PEER:h(root/PEER),SELF:h(root/SELF)}
 v['counts'].update(registered_local_functions=46,per_act=dict(Counter(q['act']for q in rows)),subacts_with_verified_local_function_route=28,subacts_without_verified_local_function_route=14,unassigned_planned_slots=734,source_pin_count_including_current_consumer=len(v['source_sha256']))
 v['prior_45_register_immutable']=True
 v['new_A10_scope']='One privately authorized eight-second task, visible teammate time cost and same-task retry; no whole first-option, season, MVP or title certification.'
 return v
def markdown(v):
 lines=['# G13 현행 등록 · A10 기능 추가','','기존45 등록은 고정 사본으로 보존하고 별도 독립검문한 A10-EF-001을 기능46/slot513에 연결했다. **46기능·28소막 경로·미경로14소막**이다. 국소 기능 경로가 전체 소막 출구 달성을 뜻하지 않는다.','','[원45 등록](G13_CURRENT_FUNCTION_EXECUTION_REGISTER_2026_10_08.md) · [A10 기능](../design/A10_E1_FINAL_EPISODE_FUNCTION.md) · [독립 검문](../'+PEER+')','','| 순서 | 기능 | 소막 | 계획slot |','|---|---|---|---|']
 lines += [f"| {q['order']} | {q['id']} | {q['subact']} | {q['planned_slot']} |"for q in v['functions']]
 lines += ['','734미배정 계획칸은734추가사건 의무가 아니다. 원43/조상생성기 범위는 이전 현행 등록의 제한을 유지한다. 전체G13/G14 미완료·실제Pack0·원고0·v0.30 PARTIAL·CLOSED. 미완료큰묶음5/6번까지4.','']
 return '\n'.join(lines)
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if a.check:assert checked(ROOT,OUT)==v and text(ROOT/MD)==markdown(v),'Saved register stale'
 print(json.dumps({'current':True,'counts':v['counts']}))
if __name__=='__main__':main()
