"""Project original pick identities through authored transaction options, not final trades."""
import json
from copy import deepcopy
from itertools import permutations
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'simulation/NBA_2021_DRAFT_ASSET_INPUTS.json'
OUT=ROOT/'simulation/NBA_2021_DRAFT_ASSETS.json'


def validate_ranks(ranks,teams):
    if set(ranks)!=set(teams) or len(set(ranks.values()))!=len(teams):
        raise ValueError('supply distinct final second-round positions for exactly these teams')
    if any(type(v) is not int or not 31<=v<=60 for v in ranks.values()):
        raise ValueError('not a final second-round position')


def settle_2025(ranks,kemba):
    validate_ranks(ranks,['BOS','MEM'])
    better,worse=sorted(ranks,key=ranks.get)
    return [dict(origin=better,pick=ranks[better],owner='OKC' if kemba else 'BOS'),dict(origin=worse,pick=ranks[worse],owner='ORL')]


def settle_2023(ranks):
    validate_ranks(ranks,['OKC','WAS','DAL','MIA'])
    dm=min(['DAL','MIA'],key=ranks.get)
    candidates=['OKC','WAS',dm]
    origin=max(candidates,key=ranks.get)
    return dict(origin=origin,pick=ranks[origin],eligible_origins=candidates)


def transfer(rows,round_number,origin,sender,recipient,event):
    matches=[r for r in rows if r['round']==round_number and r['origin']==origin]
    if len(matches)!=1 or matches[0]['owner']!=sender:
        raise ValueError('asset absent or sender does not control it')
    matches[0]['owner']=recipient
    matches[0]['events'].append(event)


def base_rows(p,parent):
    out=[]
    for rd,key,mapping in [(1,'first_round_origins',p['first_round_owner_by_origin_overrides']),(2,'second_round_origins',p['second_round_owner_by_origin_overrides'])]:
        for r in parent[key]:
            out.append(dict(round=rd,pick=r['pick'],origin=r['origin'],owner=mapping.get(r['origin'],r['origin']),events=[],status='CONDITIONAL_CARRY_FORWARD_NOT_FINAL_RIGHTS_AUDIT'))
    second={r['origin']:r for r in out if r['round']==2}
    if second['NOP']['pick']<second['CHI']['pick']:
        second['NOP']['owner']='CHI';second['CHI']['owner']='NOP'
    assert len(out)==60 and len({(r['round'],r['origin']) for r in out})==60
    return out


def project(p,parent,s):
    rows=base_rows(p,parent)
    if s['boston_kemba']:transfer(rows,1,'BOS','BOS','OKC','PROPOSED_KEMBA_HORFORD')
    if s['nop_mem']:
        for rd,origin,sender,to in [(1,'NOP','NOP','MEM'),(1,'MEM','MEM','NOP'),(2,'NOP','NOP','MEM'),(2,'POR','MEM','NOP')]:
            transfer(rows,rd,origin,sender,to,'PROPOSED_NOP_MEM')
    if p['cash_sale_dal_second']:transfer(rows,2,'DAL','NOP','PHI','PROPOSED_CASH_SALE')
    return dict(**s,rows=rows,G4_top14_compatible=not s['nop_mem'],requires_new_top14_board=s['nop_mem'],player_selection_executed=False,trade_legal_execution_verified=False,remaining_2022_LAL_obligation=({'recipient':'MEM','top_protection':10,'nonconveyance_termination':None,'status':'PROPOSED_EXACT_ENDING_HOLD'} if s['nop_mem'] else {'recipient':'NOP','status':'RETAIN_PREEXISTING_RIGHTS_NO_NEW_TRANSFER'}))


def build():
    p=json.loads(INPUT.read_text());parent=json.loads((ROOT/p['parent']).read_text())
    scenarios=[project(p,parent,s) for s in p['scenarios']]
    tests2023=[]
    for ranks_order in permutations(['OKC','WAS','DAL','MIA']):
        ranks={t:31+i for i,t in enumerate(ranks_order)}
        tests2023.append(dict(ranks=ranks,recipient_BOS_if_kemba=settle_2023(ranks),not_a_real_future_draw=True))
    tests2025=[dict(ranks=r,kemba=k,result=settle_2025(r,k)) for r in [dict(BOS=40,MEM=50),dict(BOS=50,MEM=40)] for k in [True,False]]
    return dict(stage='O-15G5',status='CONDITIONAL_ASSET_PROJECTION',scenarios=scenarios,recommended_scenario=p['recommended_scenario'],selected_scenario=None,projection_rows=sum(len(s['rows']) for s in scenarios),future_2023_permutations=tests2023,future_2023_formula='max(OKC, WAS, min(DAL, MIA)); numeric later position is worse',future_2025_order_cases=tests2025,actual_future_ranks=None,cash_sale_DAL_second=p['cash_sale_dal_second'],draft_night_trades_executed=p['other_draft_night_trades_executed'],final_60_pick_control_verified=False,original_lottery_rerun=False,author_locked=False,season_selected=False,exact_execution_cleared=False,manuscript_allowed=False,independent_review='NOT_INDEPENDENT')


if __name__=='__main__':
    x=build();OUT.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(PASS=True,projection_rows=x['projection_rows'],future_2023_orders=len(x['future_2023_permutations']),future_2025_orders=len(x['future_2025_order_cases']),final_rights_verified=False)))
