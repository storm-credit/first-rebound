"""Verify a conditional M1 unordered five-player witness, never actual minutes."""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
INPUT = 'simulation/CHICAGO_2021_M1_ROLE_WITNESS.json'
SOURCES = ['simulation/CHICAGO_2021_22_ROLE_PLAN_INPUTS.json', 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json', 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json', 'simulation/CHICAGO_2021_MARKKANEN_OFFER_STRESS.md', 'canon/PROJECT_FREEZE.md']
POSITIONS = ('PG','SG','SF','PF','C')
def load(p):
    return json.loads((ROOT/p).read_text(encoding='utf8'))
def sha(p):
    return hashlib.sha256((ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()
def budget():
    b=deepcopy(load(SOURCES[0])['cases'][0]['position_minutes'])
    b['SF']['Caruso']-=4
    b['SF']['Protagonist']+=4
    b['PF']['Markkanen']+=4
    b['PF']['Protagonist']-=4
    return b
def validate(d):
    errors=[]
    src=load(SOURCES[0]); expected=budget()
    if d.get('source_sha256') != {p:sha(p) for p in SOURCES}: errors.append('stale or missing source')
    if d.get('position_minutes') != expected: errors.append('M1 budget mismatch')
    player_totals=Counter()
    for vals in expected.values(): player_totals.update(vals)
    if d.get('derived_player_minutes') != dict(sorted(player_totals.items())):
        errors.append('player summary mismatch')
    if d.get('elapsed_minutes') != 48 or d.get('team_minutes') != 240:
        errors.append('clock summary mismatch')
    if load(SOURCES[1])['selected']['normal_availability_pf_minutes_candidate'] != expected['PF']['Markkanen']:
        errors.append('selected M1 role mismatch')
    if load(SOURCES[2])['selected']['route'] != 'G1A_PLUS_M1':
        errors.append('selected direction mismatch')
    if d.get('design_gate') != 'CLOSED': errors.append('design gate promotion')
    for k in ['actual_minutes_selected','season_selected','exact_execution_cleared','manuscript_allowed','registration_verified','health_verified','tactical_efficiency_verified','substitution_order_selected']:
        if d.get(k) is not False: errors.append('promotion '+k)
    if d.get('contract_acceptances_selected') != []: errors.append('contract promotion')
    if d.get('full_roster_selected') is not False: errors.append('roster promotion')
    for k in ['game_date','box_score','actual_venue','actual_overtime','substitution_timeline']:
        if d.get(k) is not None: errors.append('exact event '+k)
    seen={p:Counter() for p in POSITIONS}; elapsed=0
    for w in d['lineup_witness']:
        ps=w.get('positions',{}); m=w.get('minutes')
        if type(m) is not int or m<=0 or m%2: errors.append('duration');continue
        elapsed+=m
        if set(ps)!=set(POSITIONS) or len(set(ps.values()))!=5:errors.append('five distinct players')
        if not set(ps.values())&{'LaVine','LaMelo_pick4'}:errors.append('creator coverage')
        for pos,p in ps.items():
            if pos not in seen or p not in src['position_eligibility_design_only'].get(pos,[]): errors.append('eligibility');continue
            seen[pos][p]+=m
    if elapsed != 48 or any(dict(seen[p])!=expected[p] for p in POSITIONS):errors.append('witness totals')
    return errors
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.parse_args()
    errors=validate(load(INPUT))
    if errors:raise SystemExit('\n'.join(errors))
    print('PASS: M1 5-player unordered48/240 witness; registration/health/season HOLD')
