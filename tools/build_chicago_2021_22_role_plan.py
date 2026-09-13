"""Verify explicit five-player witnesses; no solver or season extrapolation.

The input witnesses were found with an integer solver. Their ordering is not a
substitution timeline. Reproduction and validation use only the standard library.
"""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = 'simulation/CHICAGO_2021_22_ROLE_PLAN_INPUTS.json'
OUTPUT = 'simulation/CHICAGO_2021_22_ROLE_PLAN.json'
POSITIONS = ('PG', 'SG', 'SF', 'PF', 'C')


def load(path, root=ROOT):
    return json.loads((root / path).read_text())


def totals(budget):
    out = Counter()
    for players in budget.values():
        out.update(players)
    return dict(sorted(out.items()))


def validate(data, root=ROOT):
    errors = []
    for path, expected in data['source_content_sha256'].items():
        if hashlib.sha256((root / path).read_bytes()).hexdigest() != expected:
            errors.append('STALE ' + path)
    for key in ['author_locked', 'season_selected', 'exact_execution_cleared', 'manuscript_allowed']:
        if data.get(key) is not False:
            errors.append('promotion ' + key)
    for key in ['season_GP', 'season_GS', 'season_minutes', 'season_wins', 'selected_policy']:
        if data.get(key) is not None:
            errors.append('unsupported season/selection ' + key)
    roster = set(data['roster'])
    if len(roster) != 15 or len(data['roster']) != 15:
        errors.append('roster count')
    old = load('simulation/CHICAGO_2021_NAMED_ROSTER_OPTIONS.json', root)
    draft = load('simulation/NBA_2021_FULL_DRAFT_COMPARISON.json', root)
    board = next(s['board'] for s in draft['scenarios'] if s['id'] == draft['recommended_comparison'])
    picks = {r['pick']: r['proposed_player'] for r in board}
    aliases = {'Moses Moody': picks[10], 'Kessler Edwards': picks[39]}
    inherited_roster = {aliases.get(p, p) for p in old['named_roster_without_protagonist']} | {'Protagonist'}
    if roster != inherited_roster:
        errors.append('G7 roster mismatch')
    baseline = {pos: {aliases.get(p, p): m for p, m in players.items()}
                for pos, players in old['primary_healthy_position_budget'].items()}
    if next(c for c in data['cases'] if c['id'] == 'R21A')['position_minutes'] != baseline:
        errors.append('G1A baseline mismatch')
    ids = [c['id'] for c in data['cases']]
    if len(set(ids)) != len(ids):
        errors.append('duplicate case')
    for c in data['cases']:
        prefix = c['id'] + ': '
        budget = c['position_minutes']
        if set(budget) != set(POSITIONS) or any(sum(budget.get(pos, {}).values()) != 48 for pos in POSITIONS):
            errors.append(prefix + 'position total')
        for pos, players in budget.items():
            for p, minutes in players.items():
                if p not in roster or p not in data['position_eligibility_design_only'].get(pos, []):
                    errors.append(prefix + 'eligibility ' + p)
                if not isinstance(minutes, int) or minutes <= 0:
                    errors.append(prefix + 'invalid minutes')
        if any(m > data['player_minute_ceiling_design_only'] for m in totals(budget).values()):
            errors.append(prefix + 'player load ceiling')
        observed = {pos: Counter() for pos in POSITIONS}
        elapsed = 0
        for w in c['lineup_witness']:
            ps, minutes = w['positions'], w['minutes']
            if not isinstance(minutes, int) or minutes <= 0 or minutes % data['unit_minutes']:
                errors.append(prefix + 'witness duration')
            elapsed += minutes
            if set(ps) != set(POSITIONS) or len(set(ps.values())) != 5:
                errors.append(prefix + 'five distinct players')
            if not set(ps.values()) & set(c['required_creator_any_of']):
                errors.append(prefix + 'creator coverage')
            if set(ps.values()) & set(c['unavailable']):
                errors.append(prefix + 'unavailable player')
            for pos, p in ps.items():
                if pos in observed:
                    observed[pos][p] += minutes
        if elapsed != 48 or any(dict(observed[pos]) != budget.get(pos, {}) for pos in POSITIONS):
            errors.append(prefix + 'witness budget mismatch')
    hold = data['infeasible_stress']
    eligible = set(data['position_eligibility_design_only']['C']) - set(hold['unavailable'])
    if set(hold['center_ceiling_design_only']) != eligible:
        errors.append('center bound eligibility')
    deficit = hold['required_center_minutes'] - sum(hold['center_ceiling_design_only'].values())
    if deficit <= 0 or deficit != hold['expected_unfilled_center_minutes']:
        errors.append('center shortage bound')
    return errors


def build(data):
    baseline = totals(next(c['position_minutes'] for c in data['cases'] if c['id'] == 'R21A'))
    rows = []
    for c in data['cases']:
        actual = totals(c['position_minutes'])
        delta = {p: actual.get(p, 0) - baseline.get(p, 0) for p in data['roster']}
        rows.append(dict(id=c['id'], player_minutes=actual,
                         delta_from_R21A={p: m for p, m in delta.items() if m},
                         active_rotation_players=len(actual),
                         distinct_lineups=len(c['lineup_witness']),
                         elapsed_minutes=48, player_minutes_sum=sum(actual.values()),
                         status='POSITION_AND_LINEUP_CERTIFICATE_PASS'))
    return dict(stage=data['stage'], status=data['status'], cases=rows,
                infeasible_stress=copy.deepcopy(data['infeasible_stress']),
                source_content_sha256={**data['source_content_sha256'], INPUT: hashlib.sha256((ROOT / INPUT).read_bytes()).hexdigest()},
                author_locked=False, season_selected=False, exact_execution_cleared=False,
                manuscript_allowed=False, independent_review='NOT_INDEPENDENT',
                season_results=None, substitution_timeline=None, tactical_efficiency=None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = load(INPUT)
    errors = validate(data)
    if errors:
        raise SystemExit('\n'.join(errors))
    content = json.dumps(build(data), ensure_ascii=False, indent=2) + '\n'
    if args.check:
        if (ROOT / OUTPUT).read_text() != content:
            raise SystemExit('STALE generated role plan')
    else:
        (ROOT / OUTPUT).write_text(content)
    print('PASS: 7 lineup certificates; 1 conditional center shortage; no season results')


if __name__ == '__main__':
    main()
