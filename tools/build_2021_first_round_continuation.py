"""Conditional first-round comparisons; no NBA transaction or canon execution."""
import json
from copy import deepcopy
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'simulation/NBA_2021_FIRST_ROUND_CONTINUATION_INPUTS.json'
OUT=ROOT/'simulation/NBA_2021_FIRST_ROUND_CONTINUATION.json'


def available(priority,taken):
    if len(priority)!=len(set(priority)):raise ValueError('duplicate ranked candidate')
    remaining=[n for n in priority if n not in taken]
    if len(remaining)<3:raise ValueError('fewer than three available prospects')
    return remaining


def resolve(parent,assets,p,overrides=None):
    overrides=overrides or {}
    board=deepcopy(parent['board']);taken={r['proposed_player'] for r in board}
    if len(board)!=14 or len(taken)!=14:raise ValueError('invalid top14')
    bypick={r['pick']:r for r in assets['rows']}
    for r in board:
        if r['team']!=bypick[r['pick']]['owner']:raise ValueError('incompatible top14 ownership')
    proposals=[]
    for r in p['rows']:
        pick=r['pick'];owner=bypick[pick]['owner'];team=owner
        if r['control_team']!=owner:raise ValueError('stale standing owner')
        seller_comparison=None;trade=False
        priority=overrides.get(str(pick),r['priority'])
        if pick==16:
            seller_comparison=available(priority,taken)
            trade='Alperen Sengun' not in taken
            if trade:
                team='HOU';priority=p['sengun_buyer_priority']
                proposals.append(dict(id='SG16',pick=16,from_team='OKC',to_team='HOU',target='Alperen Sengun',future_assets_from_HOU=deepcopy(p['sengun_future_picks']),agreement_verified=False,legal_execution_verified=False))
        options=available(priority,taken);chosen=options[0]
        board.append(dict(pick=pick,team=team,standing_owner=owner,proposed_player=chosen,available_comparison=options,excluded_taken=[n for n in priority if n in taken],seller_keep_comparison=seller_comparison,target_trade_proposed=trade,proposal_only=True))
        taken.add(chosen)
    if [r['pick'] for r in board]!=list(range(1,31)) or len(taken)!=30:raise ValueError('incomplete or duplicated first round')
    return dict(id=parent['id'],board=board,transaction_proposals=proposals,CHI10=board[9]['proposed_player'],CHI39_proposed_player=None,CHI39_availability_verified=False,Sengun_trade_status='PROPOSED_IF_BOTH_TEAMS_ACCEPT' if proposals else 'TARGET_ALREADY_TAKEN_NO_SUBSTITUTE_TRADE',future_DET_WAS_rights_owner_after_proposal='OKC' if proposals else 'HOU',actual_contracts_agreed=False,comparison_only=True)


def future_settlement(terms,positions):
    for year,protected in sorted(terms['first_protection_by_year'].items()):
        if year not in positions:return dict(status='HOLD_MISSING_EARLIER_YEAR',year=int(year))
        pos=positions[year]
        if type(pos) is not int or not 1<=pos<=30:raise ValueError('not a first-round position')
        if pos>protected:return dict(status='CONVEYS_FIRST',asset=dict(year=int(year),round=1,origin=terms['origin'],pick=pos),later_obligations=[])
    return dict(status='CONVERTS_TO_SECONDS',assets=deepcopy(terms['if_never_conveys']))


def build():
    p=json.loads(INPUT.read_text());g4=json.loads((ROOT/p['parent_board']).read_text());g5=json.loads((ROOT/p['parent_assets']).read_text())
    a=next(s for s in g5['scenarios'] if s['id']==p['asset_policy'])
    ss=[resolve(s,a,p) for s in g4['scenarios']]
    pool=set(g4['tracked_candidate_pool'])|{n for r in p['rows'] for n in r['priority']}|set(p['sengun_buyer_priority'])
    for s in ss:s['tracked_candidates_remaining_for_second_round']=sorted(pool-{r['proposed_player'] for r in s['board']})
    return dict(stage='O-15G6',status='FIRST_ROUND_STANDING_PICK_COMPARISONS_NOT_FINAL_DRAFT',asset_policy='AP1',scenarios=ss,recommended_comparison=p['recommended_comparison'],selected_scenario=None,first_round_comparison_rows=sum(len(s['board']) for s in ss),new_comparison_rows=64,unjudged_second_round_picks=30,other_first_round_trades=p['other_first_round_trades'],latest_CHI10_budget_unchanged=True,first_round_finally_selected=False,full_front_office_workout_medical_audit=False,actual_future_pick_positions=None,original_lottery_rerun=False,author_locked=False,season_selected=False,exact_execution_cleared=False,manuscript_allowed=False,independent_review='NOT_INDEPENDENT')


if __name__=='__main__':
    x=build();OUT.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(PASS=True,rows=x['first_round_comparison_rows'],Sengun_trade={s['id']:s['Sengun_trade_status'] for s in x['scenarios']},second_round_unjudged=30,author_locked=False),ensure_ascii=False))
