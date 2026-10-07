"""Select the existing T1 NPC family and execute its ordered 60-slot draft model.

Participant/legal consent families are explicit fiction. No real receipts or UPCs.
"""
from __future__ import annotations
import argparse,hashlib,json
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2021_t1_selected_draft_execution.py'
OUT='simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json'
MD=OUT.replace('.json','.md')
T1='research/NBA_2021_PICK16_T1_OPERATING_FAMILY_2026_10_07.json'
BOARD='research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json'
WORK='research/NBA_2021_PICK16_BOS_OKC_HOU_WORKING_EXECUTION_2026_10_07.json'
PINS={'research/NBA_2021_PICK16_T1_OPERATING_FAMILY_2026_10_07.json': 'ba20c3378be3fa2ed9883b3990d315f8b889455ab0bc429a8cee4ec99fb4d128', 'research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json': '90099928f9133c4087ee7871939ce58216d183bd186f5ebd3575a56c2348eeed', 'research/NBA_2021_PICK16_BOS_OKC_HOU_WORKING_EXECUTION_2026_10_07.json': '86b9989daa20eced72106c25b14fb8d8b3b32d201132a0b87ba466b0ce51fba0'}
FIELDS=('pick','round','origin','frozen_before_optional_offseason_holder','conditional_holder_at_selection','selecting_team','conditional_final_draft_rights_holder','player','prior_selected_player_count','available_when_selected_in_this_board','candidate_legal_participation_condition')
def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()
def read(root,p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def selected_row(source,index):
    return {**{k:deepcopy(source[k]) for k in FIELDS},'selection_index':index,'date':'2021-07-29','classification':'PRESERVED_CHI_WORKING_SELECTION' if source['selecting_team']=='CHI' else 'ROOT_ROUTINE_NPC_DRAFT_SELECTION',
      'lawful_PS21_participant_model_selected':True,'actual_counterfactual_eligibility_or_medical_certified':False,'new_NBA_UPC_or_RequiredTender':False,'new_author_lock':False}
def assert_selected_row(row,source,index):
    require(all(row[k]==source[k] for k in FIELDS),'Returned draft row differs from source pick/holder/player/availability')
    require(row['selection_index']==index and row['date']=='2021-07-29','Returned draft order/date changed')
    classification='PRESERVED_CHI_WORKING_SELECTION' if source['selecting_team']=='CHI' else 'ROOT_ROUTINE_NPC_DRAFT_SELECTION'
    require(row['classification']==classification and row['lawful_PS21_participant_model_selected'],'Returned routine/CHI/participant scope changed')
    require(not row['actual_counterfactual_eligibility_or_medical_certified'] and not row['new_NBA_UPC_or_RequiredTender'] and not row['new_author_lock'],'Draft choice promoted to actual contract or author lock')
def build(root=ROOT):
    for p,h in PINS.items():require(sha(root/p)==h,'Reviewed source changed: '+p)
    d={p:read(root,p) for p in PINS}
    for p,v in d.items():require(v==json.loads((root/p).read_text(encoding='utf-8-sig')),'Loaded source differs from physical: '+p)
    t,b,w=(d[p] for p in (T1,BOARD,WORK))
    require(t['working_order'][0]['date']=='2021-07-28' and t['working_order'][2]['date']=='2021-07-29','T1 date window changed')
    require(t['authority']['approved_Chicago_M1_A_preserved'] and t['authority']['frozen_macro2_S2_preserved'],'Existing approvals changed')
    require(b['policy']['conditional_asset_scenario']=='T1_AP1_AND_SG16' and len(b['rows'])==60,'Board scenario/domain changed')
    require([(z['pick'],z['selecting_team'],z['player']) for z in b['rows'] if z['selecting_team']=='CHI']==[(10,'CHI','Chris Duarte'),(39,'CHI','Joe Wieskamp')],'Prior Chicago choices changed')
    controls={r['pick']:r for r in w['draft_control_candidate_rows']}
    owners={('CURRENT_FIRST_SELECTION' if r['round']==1 else 'CURRENT_SECOND_SELECTION',f"{r['origin']}_2021_{r['pick']}"):r['frozen_before_optional_offseason_holder'] for r in b['rows']}
    for step in [t['working_order'][0],t['working_order'][2]]:
        for e in step['atomic_edges']:
            if e['kind'] not in ('CURRENT_FIRST_SELECTION','UNSIGNED_DRAFT_RIGHTS'):owners[(e['kind'],e['asset'])]=e['from']
    traces=[]
    def apply_atomic(step,expected_event):
        es=step['atomic_edges'];require(len({(e['kind'],e['asset']) for e in es})==len(es),'Duplicate atomic asset')
        for e in es:
            require(e['event']==expected_event and owners.get((e['kind'],e['asset']))==e['from'],'Atomic event/asset predecessor owner changed')
        for e in es:owners[(e['kind'],e['asset'])]=e['to']
        traces.append({'date':step['date'],'event':expected_event,'atomic':True,'edges':deepcopy(es),'private_receipt_certified':False})
    apply_atomic(t['working_order'][0],'AP1')
    selected=[];seen=set()
    for i,source in enumerate(b['rows']):
        row=selected_row(source,i);assert_selected_row(row,source,i)
        n=row['pick'];control=controls[n]
        require(n==i+1 and row['prior_selected_player_count']==i and row['player'] not in seen,'Draft pick order/duplicate availability')
        require(row['available_when_selected_in_this_board'] and row['candidate_legal_participation_condition'],'Unavailable or inadmissible participant')
        require((row['round'],row['origin'],row['frozen_before_optional_offseason_holder'],row['conditional_holder_at_selection'],row['conditional_final_draft_rights_holder'])==(control['round'],control['origin'],control['frozen_macro2_holder'],control['conditional_after_AP1_holder'],control['conditional_after_SG16_holder']),'Frozen control or T1 projection changed')
        slot=f"{row['origin']}_2021_{n}";key=('CURRENT_FIRST_SELECTION' if row['round']==1 else 'CURRENT_SECOND_SELECTION',slot)
        require(owners.pop(key)==row['selecting_team'],'Selection made by wrong holder')
        right=('UNSIGNED_DRAFT_RIGHTS',slot+':'+row['player']);require(right not in owners,'Duplicate born draft right');owners[right]=row['selecting_team']
        traces.append({'date':'2021-07-29','event':'SELECT','pick':n,'player':row['player'],'selecting_team':row['selecting_team'],'born_unsigned_right':right[1],'NBA_UPC_or_RequiredTender':False})
        seen.add(row['player']);selected.append(row)
        if n==16:apply_atomic(t['working_order'][2],'SG16')
        require(owners[right]==row['conditional_final_draft_rights_holder'],'Post-selection rights holder differs from source')
    require(len(selected)==60 and sum(r['classification']=='ROOT_ROUTINE_NPC_DRAFT_SELECTION' for r in selected)==58,'Routine selection count changed')
    require(len(traces)==62 and len(seen)==60,'Atomic/selection trace domain changed')
    require(not any(k.startswith('CURRENT_') for k,_ in owners),'Unconsumed draft selection slot')
    return {'id':'NBA_2021_T1_SELECTED_DRAFT_EXECUTION','baseline_main':'b44b8d36868bda605c3c159cfe80d016edfd193f','source_sha256':{**PINS,SELF:sha(root/SELF)},
      'classification':'ROOT_ROUTINE_DESIGN_SELECTION_AND_SOURCE_BOUND_FINITE_EXECUTION',
      'status':'T1_SELECTED_60_WORKING_DRAFTEES_AND_NINE_ASSET_MOVES_EXECUTED_WITHIN_ADMITTED_LEGAL_FAMILIES',
      'chosen_path':'T1_AP1_AND_SG16','authority':'NPC routine path preserving approved Chicago M1/A and completed S2. Existing technical unselected labels describe precursor generation. No new human exact-price or title/franchise approval asserted.',
      'participant_model':{'id':'PS21','legal_conditions':b['policy']['candidate_participation'],'all60_legal_participants_selected_as_fictional_model':True,'actual_private_eligibility_or_medical_certified':False},
      'contract_implementation_family':{'source':T1,'pointer':'/public_cost_family','lawful_hypothetical_consents_and_bonus_waivers_if_applicable_selected_as_model':True,'exact_Brown_q':None,'Brown_protection_interval':[423280,1701593],'actual_private_consent_or_amendment_receipt_certified':False},
      'selected_rows':selected,'event_trace':traces,'final_asset_ownership':[{'kind':kind,'asset':asset,'owner':owner} for (kind,asset),owner in sorted(owners.items())],
      'summary':{'working_draft_choices':60,'prior_CHI_choices_preserved':2,'new_NPC_choices':58,'unique_draftees':60,'atomic_trade_events':2,'asset_edges':9,'chronological_events':62,'new_UPCs_or_RequiredTenders':0,'new_author_locks':0},
      'remaining_inputs':['AfterAug3 named rookie Tender/UPC/foreign release where needed, dates/rosters/costs; no old-year numeric automatic carry.','BOS/OKC/HOU subsequent contract/role/fee and all other teams named operating intervals.','Preserve existing conditional claim protections; no exact future conveyance invented.'],
      'whole_macro3_or_82_game_season_complete':False,'design_gate':'CLOSED','freeze':'v0.30 PARTIAL','manuscript_allowed':False}
def validate(value,root=ROOT):
    try:require(value==build(root),'Saved selected execution differs from physical source-bound construction');return []
    except (ValueError,KeyError,IndexError) as e:return [str(e)]
def markdown(b):
    return '\n'.join(['# 2021 T1·60개 작업 지명 실행','','기존 비교안 중 T1을 승인 Chicago 방향 안의 NPC 루틴 설계로 선택했다. July28 AP1→July29 순차60선택/#16직후SG16의62사건과9자산 이동을 source-bound 원장으로 실행했다. Chicago 두 작업 지명을 보존하고 나머지58명은 공개2021 prospect의 적법참가 PS21 모델 안에서 선택했다. 원후보 파일의 unselected는 생성 당시 표기다.','','적법 참가·동의/필요 보너스 면제는 **명시적 가상 법적 구현 가족**이다. 실제 당사자·사적 종이·임상 인증이 아니다. 기존 공개 전체비용과 Brown 보호 q구간을 사용하며 하나의 정확 q는 선택하지 않는다. 지명 권리만 생성했고 UPC/Tender0이다. 기존 보호 청구의 조건을 지우거나 후년 전달을 정하지 않는다.','','Source 선택 행의 pick/round/origin·전/선택/최종 holder·선수·선행 count/가용성/참가조건을 caller에서 직접 대조한다. 동일 원자 자산의 중복과 잘못된 선행 소유자·child event 태그를 거부한다. 원6/18을 완료S2에 소급0, Aug3 뒤 비용 자동carry0.','','다음: 새 capyear의 신인 Tender/UPC·실명 계약/15+2·비용·변경된 상대 역할과 가용성. 전체3번 완료가 아니다. 원고0·v0.30 PARTIAL·CLOSED.',''])
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');a=ap.parse_args();b=build()
    if a.write:
        (ROOT/OUT).write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(b),encoding='utf-8')
    else:require(not validate(read(ROOT,OUT)),'Saved execution invalid')
    print(json.dumps(b['summary'],ensure_ascii=False))
