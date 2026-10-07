"""Current dated working result ledger; no ancestor constructors or actual-game receipts."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2021_22_selected_results_ledger.py'
OUT='simulation/CHICAGO_2021_22_SELECTED_RESULTS_LEDGER.json'
MD=OUT[:-5]+'.md'
FILES=['simulation/CHICAGO_2021_22_SELECTED_RESULT_HANDOFF_2026_10_07.json', 'simulation/CHICAGO_TORONTO_2021_22_SELECTED_BPM_RESULTS_2026_10_07.json', 'reviews/TOR4_BPM_INDEPENDENT_REVIEW_2026_10_07.json', 'simulation/CHICAGO_NEW_ORLEANS_2021_SELECTED_KEEPER_RESULT.json', 'reviews/NOP_KEEPER_SELECTED_RESULT_G11_INDEPENDENT_REVIEW_2026_10_07.json', 'research/MIAMI_2021_SELECTED_APRON_CLOSURE_2026_10_07.json', 'reviews/MIA_SELECTED_APRON_ROOT_INDEPENDENT_REVIEW_2026_10_07.json']
PINS={'simulation/CHICAGO_2021_22_SELECTED_RESULT_HANDOFF_2026_10_07.json': '5a6da17a8d98d0fd991a0f9286380b71dbc1c6a3ae714a7f66ce58b51379ff74', 'simulation/CHICAGO_TORONTO_2021_22_SELECTED_BPM_RESULTS_2026_10_07.json': '333f5bd496ed59260d21e26bb42615b13cb0a11560409a798c9f905cfe66dac6', 'reviews/TOR4_BPM_INDEPENDENT_REVIEW_2026_10_07.json': '3d3f84715e9fe67c4bc796356f8f01039bd86acc70ba88dc5936ae356f1a4a69', 'simulation/CHICAGO_NEW_ORLEANS_2021_SELECTED_KEEPER_RESULT.json': 'd1975077c8879807d63763d77d58a2d89f8b481ec6c2964f0a6a9bf7a96138fd', 'reviews/NOP_KEEPER_SELECTED_RESULT_G11_INDEPENDENT_REVIEW_2026_10_07.json': 'b146d0b98603e5d965a8b8e7bab3eb1bb3428f1e5b8c406a48940890e82c5670', 'research/MIAMI_2021_SELECTED_APRON_CLOSURE_2026_10_07.json': '3007e4a2407a02e97998826c3cb8ee352ac2a75353b3c8c5822c16aa55fdbb48', 'reviews/MIA_SELECTED_APRON_ROOT_INDEPENDENT_REVIEW_2026_10_07.json': '164f0b4f5ab72f40a003840d6c7a7a3d4998f58002a37d699abd51585d5f6d39'}
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()
def read(root,p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def build(root=ROOT):
    src={}
    for p,h in PINS.items():
        need(sha(root/p)==h,'Reviewed input changed: '+p);src[p]=read(root,p)
        need(src[p]==json.loads((root/p).read_text(encoding='utf-8-sig')),'Returned input differs from physical source: '+p)
    old,tor,tr,nop,nr,mia,mr=(src[p] for p in FILES)
    need(tr['independent_review_completed'] and tr['source_sha256'][FILES[1]]==PINS[FILES[1]],'TOR independent review stale')
    need(nr['independent_review_completed'] and nr['source_sha256'][FILES[3]]==PINS[FILES[3]],'NOP independent review stale')
    need(mr['input_normalized_sha256'][FILES[5]]==PINS[FILES[5]] and mia['selected_route_feasible_under_reported_contract_family'],'MIA selected family review stale')
    chosen={r['game_id']:{'winner':r['selected_regulation_winner'],'source':r['working_result_source']['path'],'review':r['working_result_source']['review']} for r in old['rows'] if r['working_regulation_result_reviewed']}
    additions=[(r,FILES[1],FILES[2]) for r in tor['rows']]+[(nop['selected_result'],FILES[3],FILES[4])]
    calendar={r['game_id']:r for r in old['rows']};need(len(calendar)==82,'Calendar domain changed')
    for q,path,review in additions:
        key=q['game_id'];need(key in calendar and key not in chosen,'Unknown or duplicate result')
        r=calendar[key]
        need((q['date'],q['home'],q['away'],q['CHI_state'])==(r['date'],r['home'],r['away'],r['selected_CHI_state']),'Dated selected result differs from calendar/health')
        need(q['score'] is None and q['overtime_selection'] is None,'Exact score/OT unexpectedly imported')
        need(q['selected_regulation_winner'] in (q['home'],q['away']),'Winner not playing in game')
        chosen[key]={'winner':q['selected_regulation_winner'],'source':path,'review':review}
    rows=[]
    for oldrow in old['rows']:
        gid=oldrow['game_id'];c=chosen.get(gid)
        rows.append({'game_id':gid,'date':oldrow['date'],'home':oldrow['home'],'away':oldrow['away'],'opponent':oldrow['opponent'],'selected_CHI_state':oldrow['selected_CHI_state'],'working_regulation_result':c,'score':None,'overtime_selection':None,'actual_medical_private_contract_or_game_receipt_certified':False,'remaining_inputs':[] if c else oldrow['remaining_inputs'],'unresolved_membership_and_branch_flags':oldrow.get('important_unselected_branch_inputs',[])})
    remaining=[r['game_id'] for r in rows if r['working_regulation_result'] is None]
    need(len(chosen)==7 and len(remaining)==75,'Expected DET2+NOP1+TOR4 scope changed')
    return {'id':'CHICAGO_2021_22_SELECTED_RESULTS_LEDGER','baseline_main':'560e507db94f2d52c1fb56eeaccc62bb1675e726','source_sha256':{**PINS,SELF:sha(root/SELF)},'rows':rows,'summary':{'calendar_keys':82,'independently_reviewed_fictional_regulation_results':7,'CHI_working_wins':sum(c['winner']=='CHI' for c in chosen.values()),'opponent_working_wins':sum(c['winner']!='CHI' for c in chosen.values()),'remaining_keys':75,'next_game_id':remaining[0],'next_date':next(r['date'] for r in rows if r['game_id']==remaining[0])},'remaining_game_ids':remaining,'scope':'Only consumed selected named lawful families and dated roles. No final scores/OT/probability, full standings/2022pick, calibrated individual growth or historical/private certification. Frozen predecessor pending flags remain history.','whole_macro3_G13_G14_G16_certified':False,'manuscript_allowed':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED'}
def dispatch(game_id,root=ROOT):
    matches=[r for r in build(root)['rows'] if r['game_id']==game_id];need(len(matches)==1,'Unknown game key');return matches[0]
def markdown(v):
    s=v['summary'];lines=['# Chicago 2021–22 현재 선택 결과 원장','','독립 검문된 가상 정규시간 승패 **7/82**, 남은 **75**. DET2 + NOP1 + TOR4를 날짜별 Chicago 건강 상태와 연결한다.','','| 날짜 | 키 | 상대 | 선택 작업 승자 |','|---|---|---|---|']
    lines += [f"| {r['date']} | {r['game_id']} | {r['opponent']} | {r['working_regulation_result']['winner']} |" for r in v['rows'] if r['working_regulation_result']]
    lines += ['',f"다음 달력 입력: **{s['next_game_id']} / {s['next_date']}**. 아직 완성되지 않은 경기의 명단·계약·가용성 입력만 계속한다.",'','실제 점수·연장·전체 순위·2022픽·사적계약·임상은 인증하지 않는다. 골격/독서/규격 완료와 전체Pack0을 구분한다. 전체 미완료5묶음 /6번까지4. v0.30 PARTIAL·설계/원고 CLOSED·원고0.','']
    return '\n'.join(lines)
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');o=a.parse_args();v=build()
    if o.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
    if o.check:need(read(ROOT,OUT)==v and (ROOT/MD).read_text(encoding='utf-8')==markdown(v),'Current result ledger stale')
    print(json.dumps(v['summary']))
if __name__=='__main__':main()
