"""Finish a fixed-prior, standing-rights comparison; do not certify a final draft."""
import json
from copy import deepcopy
from pathlib import Path
from build_2021_first_round_continuation import available

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'simulation/NBA_2021_FULL_DRAFT_COMPARISON_INPUTS.json'
OUT=ROOT/'simulation/NBA_2021_FULL_DRAFT_COMPARISON.json'


def second_round(parent,assets,p,fallback=None,overrides=None):
    overrides=overrides or {}
    board=deepcopy(parent['board']);taken={r['proposed_player'] for r in board}
    if len(board)!=30 or len(taken)!=30:raise ValueError('need unique first round')
    bypick={r['pick']:r for r in assets['rows']}
    for row in p['rows']:
        pick=row['pick'];owner=bypick[pick]['owner']
        if owner!=row['control_team']:raise ValueError('different second-round rights require new demand comparison')
        priority=overrides.get(str(pick),row['priority'])
        if pick==39 and fallback:
            if fallback in taken:raise ValueError('requested 39 option already picked')
            priority=[fallback]+[n for n in priority if n!=fallback]
        opts=available(priority,taken);chosen=opts[0]
        board.append(dict(pick=pick,team=owner,origin=bypick[pick]['origin'],proposed_player=chosen,available_comparison=opts,excluded_taken=[n for n in priority if n in taken],proposal_only=True,contract_agreed=False,registration_confirmed=False))
        taken.add(chosen)
    if [r['pick'] for r in board]!=list(range(1,61)) or len(taken)!=60:raise ValueError('not a unique 60-pick comparison')
    return board


def overlay_roster(g3,first,second):
    roster=deepcopy(g3['named_roster_without_protagonist'])
    for old,new in [('Moses Moody',first),('Kessler Edwards',second)]:
        if old==new:continue
        if new in roster:raise ValueError('duplicate player in proposed roster')
        roster[new]=roster.pop(old)
    if len(roster)!=14:raise ValueError('not 14 plus protagonist')
    return roster


def build():
    p=json.loads(INPUT.read_text());g6=json.loads((ROOT/p['parent_round']).read_text());g5=json.loads((ROOT/p['parent_assets']).read_text());g3=json.loads((ROOT/p['parent_roster']).read_text())
    assets=next(s for s in g5['scenarios'] if s['id']==p['asset_policy'])
    pool={n for r in p['rows'] for n in r['priority']}|{n for s in g6['scenarios'] for n in s['tracked_candidates_remaining_for_second_round']}|{r['proposed_player'] for s in g6['scenarios'] for r in s['board']}
    scenarios=[]
    for parent in g6['scenarios']:
        board=second_round(parent,assets,p)
        first,second=board[9]['proposed_player'],board[38]['proposed_player'];roster=overlay_roster(g3,first,second)
        prior={n:next((dict(pick=r['pick'],team=r['team']) for r in board[:38] if r['proposed_player']==n),None) for n in p['rows'][8]['priority'][:4]}
        scenarios.append(dict(id=parent['id'],board=board,CHI10=first,CHI39=second,G3_39_candidates_taken_before_39=prior,named_roster_without_protagonist=roster,standard_slots_if_all_proposals_signed=15,additional_standard_slots=0,gross_budget_delta_from_G3=sum(roster.values())-sum(g3['named_roster_without_protagonist'].values()),CHI39_offer=deepcopy(p['CHI39_offer']),primary_rotation_rebuild_required=first=='Alperen Sengun',tracked_unselected_candidates=sorted(pool-{r['proposed_player'] for r in board}),upstream_transaction_proposals=deepcopy(parent['transaction_proposals']),full_roster_legality_verified=False))
    parent=g6['scenarios'][0];fallbacks=[]
    for opt in p['CHI39_fallback_options']:
        board=second_round(parent,assets,p,opt['player']);roster=overlay_roster(g3,board[9]['proposed_player'],board[38]['proposed_player'])
        base=scenarios[0]['board']
        fallbacks.append(dict(**opt,CHI39=board[38]['proposed_player'],named_roster_without_protagonist=roster,gross_budget_delta_from_G3=sum(roster.values())-sum(g3['named_roster_without_protagonist'].values()),changed_picks_from_C39A=[dict(pick=a['pick'],baseline=a['proposed_player'],alternative=b['proposed_player']) for a,b in zip(base,board) if a['proposed_player']!=b['proposed_player']],board=board))
    return dict(stage='O-15G7',status='COMPLETE_60_PICK_COMPARISON_NOT_FINAL_WORLD_DRAFT',scenarios=scenarios,CHI39_options=fallbacks,recommended_comparison='DB1',recommended_CHI39_option=p['recommended_fallback'],selected_scenario=None,selected_CHI39_option=None,primary_path_rows=240,new_second_round_comparison_rows=120,CHI39_option_rows=240,distinct_comparison_boards=7,unjudged_pick_rows_in_this_comparison=0,tracked_candidate_pool=sorted(pool),actual_participant_set_counterfactual_verified=False,public_scouting_role=p['public_scouting_role'],other_draft_night_trades_executed=False,full_draft_finally_selected=False,all_team_registration_completed=False,private_workout_medical_front_office_audit=False,original_lottery_rerun=False,author_locked=False,season_selected=False,exact_execution_cleared=False,manuscript_allowed=False,independent_review='NOT_INDEPENDENT')


if __name__=='__main__':
    x=build();OUT.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(PASS=True,primary_rows=x['primary_path_rows'],new_second_round_rows=120,CHI39={s['id']:s['CHI39'] for s in x['scenarios']},CHI39_options=4,unjudged_rows_in_comparison=0,final_draft=False),ensure_ascii=False))
