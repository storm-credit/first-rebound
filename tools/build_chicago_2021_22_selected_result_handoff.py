"""Consume accepted dated results without rewriting immutable predecessor history."""
from __future__ import annotations
import argparse,hashlib,json
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2021_22_selected_result_handoff.py'
OUT='simulation/CHICAGO_2021_22_SELECTED_RESULT_HANDOFF_2026_10_07.json'
MD=OUT[:-5]+'.md'
FILES=['simulation/CHICAGO_2021_22_CURRENT_OPPONENT_EXECUTION_INDEX.json', 'simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json', 'reviews/T1_SELECTED_DRAFT_INDEPENDENT_REVIEW_2026_10_07.json', 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS.json', 'reviews/DET2_SELECTED_BPM_ROOT_INDEPENDENT_REVIEW_2026_10_07.json', 'simulation/TORONTO_2021_SELECTED_T1_OPERATING_FAMILY_2026_10_07.json', 'research/TORONTO_MIAMI_2021_SELECTED_ATOM_LEGAL_BRIDGE_2026_10_07.json']
PINS={'simulation/CHICAGO_2021_22_CURRENT_OPPONENT_EXECUTION_INDEX.json': '6f232ef81c0e3be5d84e8dba5b9fe68b08dc55b00a743b7c8ab4ebf53a00cfa3', 'simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json': 'f8c78e99cce1b02a051c94339b550fdb52205d3988db8bbe69b780559c3bc306', 'reviews/T1_SELECTED_DRAFT_INDEPENDENT_REVIEW_2026_10_07.json': 'e2b48c568e8244bffca71f05167edbb3e0d78d1813486a86393765ed19c32e05', 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS.json': '66c1c862a179648aa72dd81ff13a07345b36889043995ecb583ae57019618c80', 'reviews/DET2_SELECTED_BPM_ROOT_INDEPENDENT_REVIEW_2026_10_07.json': '00daab618ceaaabdab9e62c12150fd20e8c6115dd5fd27063d6b95a797042d17', 'simulation/TORONTO_2021_SELECTED_T1_OPERATING_FAMILY_2026_10_07.json': '676cb350acdd632dfc0a0b4cc82d8f1d085b243f21fe511caeb11bcc2b993118', 'research/TORONTO_MIAMI_2021_SELECTED_ATOM_LEGAL_BRIDGE_2026_10_07.json': '719b2ff19583d6373a2c165988c9fc55b298fce3728dc8763df2d3f327357278'}
RESOLVED={'BOS':'AP1_KEMBA_HORFORD_BROWN_16_UNSELECTED','OKC':'AP1_SG16_ACTORS_ASSETS_UNSELECTED','HOU':'SG16_PICK16_SENGUN_ASSIGNMENT_UNSELECTED'}
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()
def read(root,p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def build(root=ROOT):
    data={}
    for p,h in PINS.items():
        need(sha(root/p)==h,'Reviewed source changed: '+p)
        data[p]=read(root,p)
        need(data[p]==json.loads((root/p).read_text(encoding='utf-8-sig')),'Loader differs from physical source: '+p)
    base,draft,draft_review,det,det_review,tor,mia=(data[p] for p in FILES)
    need(draft['chosen_path']=='T1_AP1_AND_SG16' and len(draft['selected_rows'])==60,'T1 working selection absent')
    need(draft_review['verdict']=='ACCEPT_SOURCE_BOUND_ROUTINE_DRAFT_MODEL_EXECUTION','T1 review absent')
    need(draft_review['source_sha256'][FILES[1]]==PINS[FILES[1]],'T1 review targets another source')
    need(det_review['input_normalized_sha256'][FILES[3]]==PINS[FILES[3]],'DET review targets another source')
    need(det_review['accepted_two_model_winners']==['CHI','CHI'],'DET reviewed winners changed')
    by_id={r['game_id']:r for r in base['rows']}
    need(len(base['rows'])==len(by_id)==82,'Calendar duplicate or missing key')
    detrows={r['game_id']:r for r in det['rows']}
    need(set(detrows)=={'0022100004','0022100030'},'DET reviewed two dates changed')
    need({r['game_id']:r['winner'] for r in det_review['direct_games']}=={k:r['selected_regulation_winner'] for k,r in detrows.items()},'Independent result disagrees')
    rows=[]
    for old in base['rows']:
        r=deepcopy(old)
        r['predecessor_generation_reference']={'path':FILES[0],'game_id':r['game_id']}
        r['selected_regulation_winner']=None
        r['working_regulation_result_reviewed']=False
        r['private_receipt_or_actual_game_certificate']=False
        r['resolved_precursor_branch_flags']=[]
        flag=RESOLVED.get(r['opponent'])
        if flag:
            need(flag in r['important_unselected_branch_inputs'],'Expected precursor flag absent')
            r['important_unselected_branch_inputs'].remove(flag)
            r['resolved_precursor_branch_flags'].append({'flag':flag,'current_selection':FILES[1],'current_review':FILES[2]})
        if r['game_id'] in detrows:
            q=detrows[r['game_id']]
            need((q['date'],q['home'],q['away'],q['CHI_state'])==(r['date'],r['home'],r['away'],r['selected_CHI_state']),'Result/calendar/health mismatch')
            need(q['score'] is None and q['overtime_selection'] is None and not q['historical_score_diagnostic_only']['used_to_decide_winner'],'Historical score/OT imported')
            need(q['each_team_player_seconds']==14400 and q['source_role_clock_seconds']==2880,'Regulation scope changed')
            r['remaining_inputs']=[]
            r['selected_regulation_winner']=q['selected_regulation_winner']
            r['working_regulation_result_reviewed']=True
            r['working_result_source']={'path':FILES[3],'game_id':r['game_id'],'review':FILES[4]}
            r['score']=None
            r['winner']=q['selected_regulation_winner']
            r['OT_selected']=False
            # This legacy certificate field remains false: a fictional working winner is not a private/real-game receipt.
            r['full_date_legal_registration_health_result_executed']=False
        rows.append(r)
    need(rows==reconcile_physical(root),'Returned overlay differs from physically pinned source bindings')
    pending=[r['game_id'] for r in rows if not r['working_regulation_result_reviewed']]
    need(len(pending)==80 and pending[0]=='0022100022','Remaining chronology changed')
    need(not mia['toronto_four_date_handoff']['TOR_four_date_legal_execution_complete'],'Miami still conditional; explicit next adoption needed')
    return {'id':'CHICAGO_2021_22_SELECTED_RESULT_HANDOFF_2026_10_07','baseline_main':'593c82df95eb765d521004f063021fa41ed66376','source_sha256':{**PINS,SELF:sha(root/SELF)},'rows':rows,'summary':{'calendar_keys':82,'reviewed_fictional_regulation_winners':2,'remaining_keys':80,'next_game_id':pending[0],'TOR_selected_role_dates':tor['date_count'],'TOR_legal_trade_executed_dates':0,'whole_season_results_or_standings_certified':False},'remaining_game_ids_in_calendar_order':pending,'scope':'Delegated fictional regulation winners only. Not calibrated final score, overtime or historical medical/private receipt. T1 selection resolves precursor AP1/SG16 flags, not remaining named operating contracts.','whole_macro3_G13_G14_G16_complete':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}
def reconcile_physical(root):
    # Independent caller binding; no constructor or returned-loader reuse.
    b=json.loads((root/FILES[0]).read_text(encoding='utf-8-sig'))
    ds={q['game_id']:q for q in json.loads((root/FILES[3]).read_text(encoding='utf-8-sig'))['rows']}
    out=[]
    for x in b['rows']:
        y=deepcopy(x);gid=y['game_id'];y.update(predecessor_generation_reference={'path':FILES[0],'game_id':gid},selected_regulation_winner=None,working_regulation_result_reviewed=False,private_receipt_or_actual_game_certificate=False,resolved_precursor_branch_flags=[])
        f=RESOLVED.get(y['opponent'])
        if f:
            y['important_unselected_branch_inputs'].remove(f)
            y['resolved_precursor_branch_flags']=[{'flag':f,'current_selection':FILES[1],'current_review':FILES[2]}]
        if gid in ds:
            q=ds[gid];y.update(remaining_inputs=[],selected_regulation_winner=q['selected_regulation_winner'],working_regulation_result_reviewed=True,working_result_source={'path':FILES[3],'game_id':gid,'review':FILES[4]},score=None,winner=q['selected_regulation_winner'],OT_selected=False,full_date_legal_registration_health_result_executed=False)
        out.append(y)
    return out
def dispatch(game_id,root=ROOT):
    out=[r for r in build(root)['rows'] if r['game_id']==game_id]
    need(len(out)==1,'Unknown game id');return out[0]
def markdown(x):
    return '\n'.join(['# Chicago 2021–22 현재 선택 결과 인계','','Detroit 두 날짜의 독립검문된 **가상 정규시간 승패 2/82**, 잔여 **80**을 현재 소비기에 연결한다. 두 결과는 Chicago 승리다. 최종 점수·연장·82전체 standings/pick 인증은 아니다.','','다음 chronology 키는 **0022100022 (New Orleans)**다. Toronto 네 역할 날짜는 선택됐지만 Miami apron의 S2 추가비용 조건이 미검산이므로 법적실행 0이다.','','BOS/OKC/HOU의 AP1/SG16 미선택 표기는 기존 T1 선택·독립검문으로 해소한다. 명명된 계약/가용성 입력은 보존한다. 동결된 부모의 작성 당시 상태는 수정하지 않는다.','','v0.30 PARTIAL · 설계/원고 CLOSED · 원고0 · 전체 미완료5묶음/6번까지4.',''])
def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();x=build()
    if a.write:
        (ROOT/OUT).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(x),encoding='utf-8')
    if a.check:
        need(read(ROOT,OUT)==x,'Saved handoff stale');need((ROOT/MD).read_text(encoding='utf-8')==markdown(x),'Saved MD stale')
    print(json.dumps(x['summary']))
if __name__=='__main__':main()
