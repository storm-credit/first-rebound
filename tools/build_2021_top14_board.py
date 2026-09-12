"""Sequential authored boards. No random draw, prediction, or canon promotion."""
import json
from copy import deepcopy
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'simulation/NBA_2021_TOP14_BOARD_INPUTS.json'
OUT=ROOT/'simulation/NBA_2021_TOP14_BOARD.json'


def resolve(rows,overrides=None):
    overrides=overrides or {}
    seen=set();out=[]
    for row in rows:
        priority=overrides.get(str(row['pick']),row['priority'])
        if len(priority)!=len(set(priority)):
            raise ValueError('duplicate candidate priority')
        available=[x for x in priority if x not in seen]
        if len(available)<3:
            raise ValueError('fewer than three available comparison candidates')
        chosen=available[0]
        out.append(dict(pick=row['pick'],team=row['control_team_if_no_new_trade'],proposed_player=chosen,available_comparison=available,excluded_taken=[n for n in priority if n in seen],proposal_only=True))
        seen.add(chosen)
    return out


def overlay_roster(parent,player):
    result=deepcopy(parent['named_roster_without_protagonist'])
    old='Moses Moody'
    if player!=old:
        if player in result:raise ValueError('duplicate roster candidate')
        result[player]=result.pop(old)
    return result


def build():
    p=json.loads(INPUT.read_text())
    d=json.loads((ROOT/p['parent_draft']).read_text())
    g=json.loads((ROOT/p['parent_roster']).read_text())
    assert [r['pick'] for r in p['rows']]==list(range(1,15))
    expected=[r['origin'] for r in d['first_round_origins'][:14]]
    assert expected[6]=='MIN'
    assert d['core_asset_settlement']['MIN_first']['owner']=='GSW'
    for row,origin in zip(p['rows'],expected):
        assert row['control_team_if_no_new_trade']==('GSW' if row['pick']==7 else origin)
    pool=sorted({n for r in p['rows'] for n in r['priority']}|{n for s in p['scenarios'] for v in s['priority_overrides'].values() for n in v})
    scenarios=[]
    for s in p['scenarios']:
        board=resolve(p['rows'],s['priority_overrides'])
        chosen={r['proposed_player'] for r in board}
        player=board[9]['proposed_player']
        roster=overlay_roster(g,player)
        assert len(roster)+1==15
        scenarios.append(dict(id=s['id'],label=s['label'],board=board,CHI10=player,GSW_pair=[board[6]['proposed_player'],board[13]['proposed_player']],tracked_candidates_not_yet_picked=[x for x in pool if x not in chosen],named_roster_example_without_protagonist=roster,CHI_rookie_first_salary_budget=roster[player],budget_delta_from_G3=0,rotation_rebuild_required=player=='Alperen Sengun',actual_contracts_agreed=False))
    return dict(stage='O-15G4',status='TOP14_FOUR_AUTHORED_OPTIONS_NOT_FINAL_DRAFT',scenarios=scenarios,recommended_scenario=p['recommended_scenario'],selected_scenario=None,tracked_candidate_pool=pool,origin_order_first14=expected,remaining_origin_order_first_round=d['first_round_origins'][14:],second_round_origin_order=d['second_round_origins'],CHI39_proposed_player=None,CHI39_G3_candidate='Kessler Edwards',CHI39_availability_verified=False,unresolved_pick_count=46,trade_assumption=p['trade_assumption'],probability_model=False,private_team_boards_verified=False,private_medical_clearance=None,original_lottery_rerun=False,author_locked=False,season_selected=False,exact_execution_cleared=False,manuscript_allowed=False,independent_review='NOT_INDEPENDENT')


if __name__=='__main__':
    x=build();OUT.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(PASS=True,scenario_rows=sum(len(s['board']) for s in x['scenarios']),CHI10={s['id']:s['CHI10'] for s in x['scenarios']},remaining_picks=x['unresolved_pick_count'],author_locked=False),ensure_ascii=False))
