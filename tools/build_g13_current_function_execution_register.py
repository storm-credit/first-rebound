"""Consume preserved verified functions and separately reviewed new execution.

Historical generators retain their historical inputs; this consumer does not
claim every ancestral generator rebuilds against later unrelated decisions.
"""
import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_g13_current_function_execution_register.py'
OUT='control/G13_CURRENT_FUNCTION_EXECUTION_REGISTER_2026_10_08.json'
MD=OUT[:-5]+'.md'
OLD='control/G13_FINAL_FUNCTION_REGISTER.json'
CP2='design/CP2_ACT_SUBACT_PACKET.json'
NEW='design/A09_JOINT_ATTEMPT_SELECTED_EXECUTION_2026_10_08.json'
PEER='reviews/A09_JOINT_ATTEMPT_SELECTED_EXECUTION_ROOT_INDEPENDENT_REVIEW_2026_10_08.json'
OLD_SHA='fcfc543010aad2e4122425192ed7f2c7dc5929fde3697d907056512d07ce21be'
CAREER='canon/CAREER_TIMELINE.md'
OLD_CAREER_SHA='c6420cc02031b138103fe83dc02437dd209a3925d005e9a063855a66ee467eca'

def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def h(p):return sha256(text(p).encode()).hexdigest()
def load(root,p):return json.loads(text(root/p))
def need(ok,why):
 if not ok:raise ValueError(why)
def checked(root,p):
 value=load(root,p);need(value==json.loads(text(root/p)),'Returned object differs from physical '+p);return value
def pointer(v,p):
 for part in p.strip('/').split('/') if p else []:v=v[int(part)] if isinstance(v,list) else v[part.replace('~1','/').replace('~0','~')]
 return v

def build(root=ROOT):
 need(h(root/OLD)==OLD_SHA,'Historical43 register changed')
 old=checked(root,OLD);cp=checked(root,CP2);new=checked(root,NEW);peer=checked(root,PEER)
 need(peer['independent_review_completed'],'New two functions need independent acceptance')
 for p,pin in peer['source_sha256'].items():need(h(root/p)==pin,'A09 reviewed generation changed: '+p)
 for p,pin in old['source_rev_sha256'].items():need(h(root/p)==pin,'Preserved53 direct source pins changed: '+p)
 for p,pin in new['source_sha256'].items():need(h(root/p)==pin,'New function current source changed: '+p)
 rows=deepcopy(old['functions']);need(len(rows)==43 and [q['order'] for q in rows]==list(range(1,44)),'Preserved43 domain')
 for row in rows:
  f=pointer(checked(root,row['path']),row.get('record_pointer',''))
  need(row['id']==f.get('episode_function_id',f.get('id')) and row['order']==f.get('final_function_order',f.get('global_function_order')),'Function identity/order')
  need(row['planned_slot']==f['planned_allocation_slot'] and row['subact']==f.get('primary_subact',f.get('subact')),'Function slot/subact')
  need(row['exact_entry']==f.get('entry_state',f.get('entry_after_fictional_bridge')) and row['exact_exit']==f['exit_state'],'Exact current functional meaning changed')
  need(f.get('manuscript_allowed',False) is False,'Historical function opened prose')
 # A later availability section was inserted after the unchanged canonical title.
 # Compare the complete remaining canon; never permit arbitrary missing sections.
 canon=text(root/CAREER);title,body=canon.split('\n\n',1)
 marker='## 2026-10-07 최신 가용성 선택\n\n';need(body.startswith(marker),'Expected explicit later availability section')
 rest=body[len(marker):];section,older=rest.split('\n\n',1)
 need('2021–22' in section and 'NORMAL58/COBY_OUT24' in section and '게이트는 CLOSED' in section,'Later scope/gate changed')
 recovered=title+'\n\n'+older
 need(sha256(recovered.encode()).hexdigest()==OLD_CAREER_SHA,'Original complete canon changed beyond declared later availability addition')
 funcs=new['functions'];need(len(funcs)==2 and [f['global_function_order']for f in funcs]==[44,45],'New two-function domain')
 need(new['selected_institutional_bridge'] and new['manuscript_allowed'] is False,'New selection or prose boundary')
 need(new['institutional_execution']['public_tournament_game_performance_selected'] is False,'Public-event legal classification cannot be silently promoted')
 for i,f in enumerate(funcs):
  need(f['previous_function']['id']==rows[-1]['id'] and f['previous_function']['exact_full_exit']==f['entry_state']==rows[-1]['exact_exit'],'New exact handoff')
  need(f['direct_present_cost'] and len(f['beats'])>=3 and all(b['action'] and b['observable']for b in f['beats']),'Selected action/cost/observation missing')
  rows.append({'id':f['episode_function_id'],'path':NEW,'record_pointer':f'/functions/{i}','order':f['global_function_order'],'planned_slot':f['planned_allocation_slot'],'act':'A09','subact':f['primary_subact'],'exact_entry':f['entry_state'],'exact_exit':f['exit_state'],'acceptance_review':PEER})
 acts={q['id']:q for q in cp['acts']};subacts={q['id']:q for q in cp['subacts']}
 need(len(subacts)==42 and len(acts)==14 and len({q['planned_slot']for q in rows})==45,'CP2 allocation/domain')
 for q in rows:need(subacts[q['subact']]['parent_act']==q['act'] and acts[q['act']]['allocation_start']<=q['planned_slot']<=acts[q['act']]['allocation_end'],'Parent allocation relation')
 coverage={q['subact']for q in rows};need(len(coverage)==27,'Two new distinct subact routes')
 sources={**old['source_rev_sha256'],**new['source_sha256'],OLD:h(root/OLD),NEW:h(root/NEW),PEER:h(root/PEER),SELF:h(root/SELF)}
 return {'schema':'G13_CURRENT_FUNCTION_EXECUTION_REGISTER_V1','classification':'CURRENT_PARTIAL_LOCAL_FUNCTION_EXECUTION_WITH_PRESERVED_HISTORICAL_INPUTS','source_sha256':sources,'historical_register_preserved':{'path':OLD,'sha256':OLD_SHA,'first43_rows_byte_equivalent_after_JSON_parse':True,'historical_direct_pins_current':53,'all_ancestral_generators_against_current_canon_certified':False,'known_legacy_failure':'A05 conditional historic CAREER pin predates explicit later2021–22 H21 addition. Legacy --check failures are preserved, not reclassified as passing.','full_original_canon_recovered_without_later_availability_section_sha256':OLD_CAREER_SHA},'functions':rows,'counts':{'registered_local_functions':45,'per_act':dict(Counter(q['act']for q in rows)),'subacts_with_verified_local_function_route':27,'subacts_without_verified_local_function_route':15,'planned_allocation_slots':780,'unassigned_planned_slots':735,'planned_slots_are_mandatory_new_events':False,'source_pin_count_including_current_consumer':len(sources)},'new_two_function_scope':'Selected authorized private joint practice and separately permitted return; public tournament legality/games/medals/military and whole A09 outcome remain unselected.','whole_g13_complete':False,'whole_g14_complete':False,'actual_context_packs':0,'manuscript_count':0,'manuscript_allowed':False,'new_author_lock':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED'}

def validate(v,root=ROOT):return [] if v==build(root) else ['Current register differs from physical preserved/reviewed functions']
def markdown(v):
 lines=['# G13 현행 기능 실행 등록 — 2026-10-08','','원43개 등록을그대로보존하고별도독립검문한A09 공동훈련·복귀 두기능44/45를연결했다. 기능45개·경로27소막·미경로15소막이다. 전체G13/G14완료가아니다.','','기존53direct source pin과43개원기능의ID/slot/entry/exit를물리파일에대조한다. 조상generator를최신전체연표로재실행한것은아니며기존실패를PASS로바꾸지않는다. CAREER의후행H21추가를제외한전체원문이원SHA와같다는보존증인을검문한다. 현재인계에는최신가용/계약·선택범위를별도로같이넘긴다.','','A09의공식대회public출전합법성/경기·메달·병역은미선택이다. 선택된허가훈련·직접실패/수정·팀복귀한정재시험의국소기능만등록한다. 원14막/42소막·780계획칸은유지하고735미배정칸을735추가사건의무로만들지않는다.','','| 순서 | 기능 | 막/소막 | 계획slot |','|---|---|---|---|']
 lines += [f"| {q['order']} | {q['id']} | {q['act']}/{q['subact']} | {q['planned_slot']} |"for q in v['functions']]
 lines += ['','[원43등록](G13_FINAL_FUNCTION_REGISTER.md) · [두새기능](../design/A09_JOINT_ATTEMPT_SELECTED_EXECUTION_2026_10_08.md) · [독립검문](../'+PEER+') · [로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','','미완료큰묶음5/6번까지4. 실제Pack0·원고0·v0.30 PARTIAL·설계/원고CLOSED。','']
 return '\n'.join(lines)
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if a.check:need(checked(ROOT,OUT)==v and text(ROOT/MD)==markdown(v),'Saved current register stale')
 print(json.dumps({'current':True,'counts':v['counts']}))
if __name__=='__main__':main()
