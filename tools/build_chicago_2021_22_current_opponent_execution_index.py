"""Current 82-key continuation index across immutable conditional predecessors.

No ancestor constructors, new contracts, health choices or game results run here.
"""
from __future__ import annotations
import argparse,hashlib,json
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2021_22_current_opponent_execution_index.py'
OUT='simulation/CHICAGO_2021_22_CURRENT_OPPONENT_EXECUTION_INDEX.json'
MD=OUT.replace('.json','.md')
BASE='simulation/CHICAGO_TORONTO_2021_FIRST_DATE_CAPACITY_JOIN.json'
OTHER='simulation/NBA_2021_22_COMMON_26_OPPONENT_CAPACITY.json'
DET='simulation/DET_ROUTINE_OPERATING_FAMILY_SELECTION_2026_10_07.json'
DET_FAMILY='research/DETROIT_2021_A_ROUTINE_OPERATING_EXECUTION_FAMILY_2026_10_07.json'
ORIGINAL='simulation/CHICAGO_2021_22_OPPONENT_CAPACITY_DISPATCHER.json'
PINS={'simulation/CHICAGO_TORONTO_2021_FIRST_DATE_CAPACITY_JOIN.json': 'af5a4fd7d374964ed83371a32d2e838c62138e3077c57bb583262b3dcc86a57e', 'simulation/NBA_2021_22_COMMON_26_OPPONENT_CAPACITY.json': 'a0ecb8e362e51344ca2cc2de53ff0713901bc4d50432a5efef621641fd0c00b7', 'simulation/DET_ROUTINE_OPERATING_FAMILY_SELECTION_2026_10_07.json': '9f9c307f33975de3b3c05734e41f8401cad0439f0446f7bc87aa21d8c7752dc2', 'research/DETROIT_2021_A_ROUTINE_OPERATING_EXECUTION_FAMILY_2026_10_07.json': '855371610d0f2b776b773bdf2ff02f27a43684b6c1407b1d54f698c6e0f093ef', 'simulation/CHICAGO_2021_22_OPPONENT_CAPACITY_DISPATCHER.json': 'e1659c32a53b2ad200b759ed88d7cabde2dfe50474569e9b7860a43497b2dfa5'}

def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()
def read(root,p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def build(root=ROOT):
    for p,h in PINS.items():require(sha(root/p)==h,'Reviewed source changed: '+p)
    d={p:read(root,p) for p in PINS}
    for p,v in d.items():require(v==json.loads((root/p).read_text(encoding='utf-8-sig')),'Loaded source differs from physical: '+p)
    b,o,a,f,c=(d[p] for p in [BASE,OTHER,DET,DET_FAMILY,ORIGINAL])
    require(set(b['missing_opponent_ports'])==set(o['team_functions']) and len(o['requested_dates'])==72,'Conditional function coverage does not match prior gaps')
    require(a['source_sha256'][DET_FAMILY]==PINS[DET_FAMILY] and a['accepted_game_ids']==['0022100004','0022100030'],'DET current adoption/source changed')
    require(not a['score_winner_OT_selected'] and a['DB1_conditional_draft_family_remains_conditional'],'DET selection scope promoted')
    other_dates={x['game_id']:x for x in o['requested_dates']};family_dates={x['game_id']:x for x in f['two_date_execution']}
    rows=[]
    for old in b['dispatcher_rows']:
        r={'game_id':old['game_id'],'date':old['candidate_date'],'home':old['home'],'away':old['away'],'opponent':old['opponent'],'selected_CHI_state':old['selected_CHI_state'],
           'CHI_authority_source':old['CHI_authority_source'],'CHI_selected_health_pointer':old['selected_CHI_health_pointer'],
           'conditional_role_function_available':True,'opponent_function_path':None,'opponent_function_pointer':None,
           'conditional_paired_clock_prepared_for_exact_date':False,'routine_operating_family_accepted_for_exact_date':False,
           'full_date_legal_registration_health_result_executed':False,'score':None,'winner':None,'OT_selected':False,'remaining_inputs':[]}
        team=r['opponent'];gid=r['game_id']
        if team in o['team_functions']:
            q=other_dates[gid];fixture=o['team_functions'][team]
            require((q['date'],q['home'],q['away'],q['opponent'],q['selected_CHI_state'])==(r['date'],r['home'],r['away'],team,r['selected_CHI_state']),'New function/date/selected health mismatch')
            require(q['opponent_conditional_function_id']==fixture['function_id'] and not q['named_legal_operating_interval_proven_on_date'],'Conditional function/interval scope changed')
            r['opponent_function_path']=OTHER;r['opponent_function_pointer']='/team_functions/'+team
            r['remaining_inputs']=['NAMED_LEGAL_OPERATING_INTERVAL','OPPONENT_AVAILABILITY_SELECTION','BILATERAL_CLOCK_FOR_SELECTED_OPERATING_FAMILY','RESULT_AND_OT_SELECTION']
            r['source_S2_event_id_not_requested_game_id']=fixture['source_S2_event_id']
            r['important_unselected_branch_inputs']=deepcopy(fixture['important_unselected_branch_inputs'])
        elif team=='TOR':
            r['opponent_function_path']='simulation/TORONTO_2021_NAMED_ROSTER_CAPACITY_CONDITIONAL_FAMILY.json';r['opponent_function_pointer']='/rows'
            r['conditional_paired_clock_prepared_for_exact_date']=bool(old['conditional_paired_clock_ids'])
            r['conditional_pair_references']=[{'path':BASE,'id':p} for p in old['conditional_paired_clock_ids']]
            r['remaining_inputs']=['TOR_NAMED_PATH_AND_LEGAL_COST','TOR_DATE_AVAILABILITY_SELECTION','RESULT_AND_OT_SELECTION']
            if not r['conditional_paired_clock_prepared_for_exact_date']:r['remaining_inputs'].append('PAIRED_CLOCK_ON_LATER_TOR_DATE')
        else:
            require(team in ('DET','NOP'),'Unknown source-covered opponent')
            capacities=[p for p in c['capacity_index'] if p['id'] in old['capacity_ids'] and p['CHI_state']==r['selected_CHI_state']]
            require(capacities,'No original conditional capacity for selected CHI state')
            r['opponent_function_path']=ORIGINAL;r['opponent_function_pointer']='/capacity_index'
            r['conditional_capacity_ids']=[p['id'] for p in capacities]
            r['conditional_paired_clock_prepared_for_exact_date']=old['original_pair_source_date_binding_verified']
            r['remaining_inputs']=['NAMED_OPERATING_AND_AVAILABILITY_INTERVAL','RESULT_AND_OT_SELECTION']
            if team=='DET' and gid in a['accepted_game_ids']:
                q=family_dates[gid]
                require(q['date']==r['date'] and q['CHI_state']==r['selected_CHI_state'],'DET accepted date/health changed')
                r['routine_operating_family_accepted_for_exact_date']=True;r['conditional_paired_clock_prepared_for_exact_date']=True
                r['accepted_operating_selection_source']=DET;r['accepted_family_date_reference']={'path':DET_FAMILY,'game_id':gid}
                r['remaining_inputs']=['DB1_CONDITIONAL_DRAFT_ROUTE_REMAINS_CONDITIONAL','RESULT_AND_OT_SELECTION']
        rows.append(r)
    teams={x['opponent'] for x in rows}
    require(len(rows)==82 and len({x['game_id'] for x in rows})==82 and len(teams)==29,'Current date/team domain changed')
    require(sum(x['conditional_paired_clock_prepared_for_exact_date'] for x in rows)==4,'Exact-date prepared pair key count changed')
    require(sum(x['routine_operating_family_accepted_for_exact_date'] for x in rows)==2,'Accepted routine scope widened')
    return {'id':'CHICAGO_2021_22_CURRENT_OPPONENT_EXECUTION_INDEX','baseline_main':'e174ec1d30f11f8b786ae92cb249f8f0522ee017','source_sha256':{**PINS,SELF:sha(root/SELF)},
      'status':'29_CONDITIONAL_ROLE_FUNCTIONS_AVAILABLE_DATE_LEGAL_AND_AVAILABILITY_EXECUTION_PENDING',
      'generation_state_flags_in_frozen_predecessors_do_not_cancel_current_separate_selections':True,
      'rows':rows,'summary':{'calendar_keys':82,'opponents':29,'conditional_role_function_coverage':29,'missing_conditional_role_functions':0,'new_other_team_functions':26,'other_team_requested_dates':72,'exact_date_paired_clock_prepared_keys':4,'DET_routine_family_accepted_date_keys':2,'new_scores_winners_OT':0,'whole_date_executions_certified':0},
      'remaining_scope':'Conditional old-roster role fixtures must be reconciled with actual chosen named contracts/transfers/health before dated result execution. 26 other teams/72 intervals remain; missing role fixture0 is not 82 complete NBA games.',
      'whole_macro3_G13_G14_G16_complete':False,'manuscript_allowed':False}

def dispatch(game_id,root=ROOT):
    rows=[r for r in build(root)['rows'] if r['game_id']==game_id];require(len(rows)==1,'Unknown or duplicate game');return rows[0]
def markdown(b):
    return '\n'.join(['# Chicago 2021–22 현재 상대 실행 인계','','동결된 선행 파일의 생성 당시 pending 표기와 현재 별도 채택을 구분한다. 실제 소비자는 이 인덱스의 `dispatch(game_id)`에서 82키·선택된 Chicago 상태·상대 함수·다음 입력을 한 번에 읽는다.','','- 조건부 역할 함수: **29/29팀**, 누락0. 원 DET/NOP2 + TOR1 + 새26.','- 정확한 요청일의 양팀 시계가 준비된 키: **4**. 첫DET/NOP + DET두번째 + TOR첫번째(4조건부 path).','- DET 공개 근거 루틴 가족과 역할을 함께 채택한 키: **2**. DB1조건부 방향과 승패/OT는 별도다.','- 다른26팀·72일의 계약/선수 이동·날짜별 가용성은 미실행이다. 원May16 명단을 실제2021계약으로 복사하지 않는다. 운영 명단이 바뀌면 해당 역할을 재구성한다.','','| 번호 | 상태 |','|---|---|','| 1 | 완료 |','| 2 | S2 유한 시즌 완료 |','| 3 | 조건부 상대 함수29/29·날짜별 계약/가용성/결과 미완료 |','| 4 | 장기 커리어 연결 미완료 |','| 5 | 전체 기능 연결 미완료 |','| 6 | 독서/문체 완료·실제Pack0 |','| 7 | 전체 검수·최종 승인 미완료 |','','미완료5개 / 6번까지4개. v0.30 PARTIAL·설계/원고CLOSED·원고0.',''])
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();b=build()
    if args.write:
        (ROOT/OUT).write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(b),encoding='utf-8')
    else:require(read(ROOT,OUT)==b,'Saved index stale')
    print(json.dumps(b['summary'],ensure_ascii=False))
