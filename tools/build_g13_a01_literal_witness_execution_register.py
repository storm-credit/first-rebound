"""Connect an independently reviewed same-trial witness to the immutable 49-function register."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_g13_a01_literal_witness_execution_register.py'
BASE='control/G13_A11_FUNCTION_EXECUTION_REGISTER_2026_10_08.json'
BASE_PEER='reviews/G13_A11_FUNCTION_EXECUTION_REGISTER_G11_INDEPENDENT_REVIEW_2026_10_08.json'
OVERLAY='design/A01_E2_LITERAL_COST_WITNESS_SELECTED_OVERLAY_2026_10_08.json'
PEER='reviews/A01_E2_LITERAL_COST_WITNESS_ROOT_INDEPENDENT_REVIEW_2026_10_08.json'
OUT='control/G13_A01_LITERAL_WITNESS_EXECUTION_REGISTER_2026_10_08.json'
MD=OUT[:-5]+'.md'
INPUTS=[BASE,BASE_PEER,OVERLAY,PEER]

def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def h(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(root,p):return json.loads(text(root/p))

def sources(root):return {p:load(root,p) for p in INPUTS}

def build(root=ROOT):
 s=sources(root)
 for p,obj in s.items():
  assert obj==json.loads(text(root/p)), 'Returned source differs from physical '+p
  for q,pin in obj['source_sha256'].items():assert h(root/q)==pin,'Stale source '+q
 b,bp,w,p=(s[q] for q in INPUTS)
 assert bp['independent_review_completed'] and p['independent_review_completed']
 assert p['source_sha256'][OVERLAY]==h(root/OVERLAY)
 assert p['literal_scoped_choice_cost_exit_supported'] and p['historical_literal_hold_preserved']
 assert not p['literal_cost_is_guaranteed_praise_receipt'] and not p['all_Act_exits_or_full_G13_certified']
 assert b['counts']['registered_local_functions']==len(b['functions'])==49
 assert b['counts']['subacts_with_verified_local_function_route']==31
 assert b['counts']['subacts_without_verified_local_function_route']==11
 original=next(q for q in b['functions'] if q['id']=='A01-EF-002')
 assert original['exact_entry']==w['original_e2_exact_entry'] and original['exact_exit']==w['original_e2_exact_exit']
 assert w['target_subact']=='A01-S1' and w['target_original_function']=='A01-EF-002'
 assert w['original_e2_locked_order']==['T1','T2'] and w['selected_overlay_order']==['T1','W','T2']
 assert w['selected_witness']['immediate_showcase_time_foregone'] and not w['selected_witness']['immediate_praise_offered_or_received']
 assert not w['selected_witness']['t2_locked_defeat_changed'] and not w['selected_witness']['later_s2_rebound_outlet_prepaid']
 assert w['new_episode_function_count']==0 and not w['existing_e1_e2_e3_files_modified']
 assert not w['literal_scoped_pass_certified'], 'Historical generation review status must stay unchanged'
 v=copy.deepcopy(b)
 v['schema']='G13_A01_LITERAL_WITNESS_EXECUTION_REGISTER_V1'
 v['prior_49_register_immutable']=True
 v['functions']=copy.deepcopy(b['functions'])
 v['current_function_overlays']=[{
  'target_function':'A01-EF-002','subact':'A01-S1','selected_overlay_path':OVERLAY,
  'acceptance_review':PEER,'selected_order':['T1','W','T2'],
  'exact_original_entry':original['exact_entry'],'exact_original_exit':original['exact_exit'],
  'bounded_literal_choice_cost_exit_accepted':True,
  'cost_scope':'Foregone immediate showcase time and attention; praise pursuit, not a guaranteed offered reward.',
  'original_audit_disposition':'Historical 5 bounded PASS/1 literal HOLD is preserved; this current witness is additional evidence.',
  'whole_A01_Act_exit_certified':False,
 }]
 v['source_sha256']={**b['source_sha256'],**w['source_sha256'],**p['source_sha256'],**{q:h(root/q) for q in INPUTS},SELF:h(root/SELF)}
 v['counts']['source_pin_count_including_current_consumer']=len(v['source_sha256'])
 assert v['functions']==b['functions']
 assert all(v[k] is False for k in ['whole_g13_complete','whole_g14_complete','manuscript_allowed','new_author_lock'])
 assert v['actual_context_packs']==v['manuscript_count']==0
 assert v['freeze']=='v0.30 PARTIAL' and v['design_gate']=='CLOSED'
 return v

def markdown(v):
 return '\n'.join([
  '# G13 현행 등록 · A01 첫 체험의 준비 비용', '',
  '독립 검문된 같은 체험의 W를 A01-EF-002에 연결했다. T1 뒤·T2 앞에서 자기 과시 순번을 공 준비에 쓰며, 실제 칭찬이나 평가를 보장하지 않는다. 원 E2 패배·E3 인계와 49기능 행은 보존한다.', '',
  '[원49기능](G13_A11_FUNCTION_EXECUTION_REGISTER_2026_10_08.md) · [선택 관측](../design/A01_E2_LITERAL_COST_WITNESS_SELECTED_OVERLAY_2026_10_08.md) · [독립 검문](../'+PEER+')', '',
  '| 항목 | 현행 |', '|---|---:|',
  '| 국소 기능 | 49 |', '| 경로 있는 소막 / 없는 소막 | 31 / 11 |',
  '| A01-S1 새 한정 literal 관측 | 1 독립 수용 |',
  '| 기능·공개 회차 증분 | 0 |',
  f"| 직접 원천 | {v['counts']['source_pin_count_including_current_consumer']} |", '',
  '기존 감사의 5 PASS/1 HOLD와 운영 정렬 6 bounded PASS는 당시 판정으로 유지한다. 이 관측은 A01 막 전체나 다른 41소막을 자동 통과시키지 않는다. 731 계획 미배정 칸은 추가 사건 의무가 아니다.', '',
  '전체 G13/G14 미완료·실제 Pack0·원고0·v0.30 PARTIAL·설계/원고 CLOSED. 미완료 큰 묶음5, 6번까지4.', '',
 ])

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();v=build()
 if a.write:
  (ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
  (ROOT/MD).write_text(markdown(v),encoding='utf-8',newline='\n')
 if a.check:assert load(ROOT,OUT)==v and text(ROOT/MD)==markdown(v),'Saved register differs'
 print(json.dumps({'current':True,'counts':v['counts'],'a01_literal_witness_accepted':True},ensure_ascii=False))

if __name__=='__main__':main()
