"""O-15F6B: conditional lineup certificates, never historical rotations.

Run from any directory with Python + numpy/scipy. --write saves the audit;
without --write the stored witnesses are checked without running a solver.
"""
import argparse
import csv
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'simulation/CHICAGO_2020_21_POSTDEADLINE_CAPACITY_VECTOR.csv'
OUTPUT = ROOT / 'simulation/CHICAGO_2020_21_POSTDEADLINE_LINEUP_AUDIT.json'
BIG = {'Wendell Carter Jr.', 'Daniel Theis', 'Thaddeus Young', 'Lauri Markkanen', 'Cristiano Felicio'}
CENTER = BIG - {'Lauri Markkanen'}
HANDLER = {'LaMelo Ball', 'Coby White', 'Tomas Satoransky', 'Zach LaVine', 'Ryan Arcidiacono', 'Devon Dotson'}
WING = {'Protagonist', 'Otto Porter Jr.', 'Garrett Temple', 'Denzel Valentine', 'Javonte Green', 'Zach LaVine', 'Adam Mokoka'}
FIXED = {'Protagonist', 'LaMelo Ball', 'Wendell Carter Jr.', 'Otto Porter Jr.', 'Zach LaVine'}
FLOORS = {'Tomas Satoransky': 600, 'Denzel Valentine': 360, 'Coby White': 1200, 'Garrett Temple': 960,
          'Daniel Theis': 900, 'Thaddeus Young': 1080, 'Lauri Markkanen': 1080}


def valid(lineup, limit):
    s = set(lineup)
    return len(lineup) == len(s) == 5 and bool(s & CENTER) and bool(s & HANDLER) and bool(s & WING) and len(s & BIG) <= limit


def inputs():
    games = defaultdict(list)
    for row in csv.DictReader(SOURCE.open()):
        if row['scenario'] in ('PORTER_ZERO', 'PORTER_CAPPED'):
            games[(row['scenario'], row['date'])].append(row)
    return games


def target_for(rows):
    target = {r['player']: int(r['alternate_seconds']) for r in rows if int(r['alternate_seconds']) > 0}
    residual = sum(target.values()) - 14400
    assert residual in (0, 1), 'Unexpected raw clock residual'
    # Existing raw data is untouched; only the 48-minute certificate uses this correction.
    player = sorted((p for p in target if p not in FIXED), key=lambda p: (-target[p], p))[0]
    target[player] -= residual
    return target, {'player': player if residual else None, 'seconds': -residual}


def role_bounds(target, rows):
    actual = {r['player']: int(r['actual_seconds']) for r in rows}
    result = {}
    for p, seconds in target.items():
        if p in FIXED:
            result[p] = (seconds, seconds)
        else:
            lower = min(seconds, FLOORS.get(p, 30))
            # Same-date perimeter receiver sensitivity: observed + at most six minutes,
            # capped at 36 minutes unless the input already exceeds that. No new active player.
            extra = 360 if p not in BIG else 0
            upper = max(seconds, min(2160 if p not in BIG else 1800, actual.get(p, 0) + extra))
            if p == 'Daniel Theis':
                upper = min(1440, upper)
            result[p] = (lower, upper)
    return result


def solve(target, starters, limit, bounds=None):
    import numpy as np
    from scipy.optimize import linprog
    players = sorted(target)
    combos = [c for c in itertools.combinations(players, 5) if valid(c, limit)]
    opening = tuple(sorted(starters))
    if opening not in combos:
        return {'status': 'INFEASIBLE', 'reason': 'STARTING_GROUP_OUTSIDE_POLICY'}
    matrix = np.array([[int(p in c) for c in combos] for p in players], dtype=float)
    n, m = matrix.shape
    xbounds = [(180 if c == opening else 0, None) for c in combos]
    rhs = np.array([target[p] for p in players], dtype=float)
    if bounds is None:
        equality = np.vstack([matrix, np.ones(m)])
        result = linprog(np.zeros(m), A_eq=equality, b_eq=np.r_[rhs, 2880], bounds=xbounds, method='highs')
    else:
        # Minimum total absolute player-minute change; no score/outcome input.
        equality = np.block([[matrix, -np.eye(n), np.eye(n)], [np.ones((1, m)), np.zeros((1, 2*n))]])
        inequalities = np.block([[matrix, np.zeros((n, 2*n))], [-matrix, np.zeros((n, 2*n))]])
        limit_rhs = np.array([bounds[p][1] for p in players] + [-bounds[p][0] for p in players])
        result = linprog(np.r_[np.zeros(m), np.ones(2*n)], A_eq=equality, b_eq=np.r_[rhs, 2880],
                         A_ub=inequalities, b_ub=limit_rhs, bounds=xbounds + [(0, None)]*(2*n), method='highs')
    if not result.success:
        assert result.status == 2, result.message
        return {'status': 'INFEASIBLE', 'reason': 'LINEUP_POLICY_AND_ROLE_CONSTRAINTS'}
    segments = [{'players': list(c), 'seconds': round(float(t), 8)} for c, t in zip(combos, result.x[:m]) if t > 1e-7]
    totals = {p: round(sum(s['seconds'] for s in segments if p in s['players']), 8) for p in players}
    return {'status': 'CONDITIONAL_CERTIFICATE_PASS', 'segments': segments, 'player_seconds': totals,
            'l1_seconds': round(sum(abs(totals[p]-target[p]) for p in players), 8)}


def build():
    records = []
    for (scenario, date), rows in sorted(inputs().items()):
        target, correction = target_for(rows)
        starters = sorted(r['player'] for r in rows if int(r['alternate_start']))
        strict = solve(target, starters, 2)
        relaxed = solve(target, starters, 3)
        bounds = role_bounds(target, rows)
        candidate_starters = starters[:]
        if not valid(candidate_starters, 2):
            # Explicit candidate for the LaVine/Coby/Temple absence on March 31.
            assert date == '2021-03-31' and 'Thaddeus Young' in starters and 'Tomas Satoransky' in target
            candidate_starters = sorted((set(starters) - {'Thaddeus Young'}) | {'Tomas Satoransky'})
        repaired = solve(target, candidate_starters, 2, bounds)
        records.append({'scenario': scenario, 'date': date, 'raw_team_seconds': sum(int(r['alternate_seconds']) for r in rows),
                        'clock_correction': correction, 'target_seconds': target, 'starters': starters,
                        'big_seconds': sum(v for p, v in target.items() if p in BIG),
                        'strict_two_big': strict, 'three_big_sensitivity': relaxed,
                        'repair_bounds': bounds, 'candidate_starters': candidate_starters, 'minimum_change_candidate': repaired})
    return {'stage': 'O-15F6B', 'status': 'CONDITIONAL_AUDIT_NOT_CANON', 'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'policy': {'clock_seconds': 2880, 'opening_group_min_seconds': 180, 'max_big_base': 2, 'max_big_sensitivity': 3,
                       'note': 'Analytical lineup categories, not NBA eligibility rules. Segments are unordered existence witnesses, not play-by-play.'},
            'games': records}


def verify(data):
    assert data['source_sha256'] == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    expected = inputs()
    assert len(data['games']) == len(expected) == 58
    assert len({(g['scenario'], g['date']) for g in data['games']}) == 58
    for game in data['games']:
        rows = expected[(game['scenario'], game['date'])]
        target, correction = target_for(rows)
        assert target == game['target_seconds'] and correction == game['clock_correction']
        assert game['raw_team_seconds'] == sum(int(r['alternate_seconds']) for r in rows)
        assert game['starters'] == sorted(r['player'] for r in rows if int(r['alternate_start']))
        assert game['big_seconds'] == sum(v for p, v in target.items() if p in BIG)
        expected_starters = game['starters']
        if game['date'] == '2021-03-31':
            expected_starters = sorted((set(expected_starters)-{'Thaddeus Young'}) | {'Tomas Satoransky'})
        assert game['candidate_starters'] == expected_starters
        assert sum(target.values()) == 14400
        bounds = role_bounds(target, rows)
        assert {p: tuple(v) for p, v in game['repair_bounds'].items()} == bounds
        for key, limit in [('strict_two_big', 2), ('three_big_sensitivity', 3), ('minimum_change_candidate', 2)]:
            result = game[key]
            if result['status'] == 'INFEASIBLE':
                # For stored strict failures this inequality is an independent certificate.
                assert key == 'strict_two_big' and sum(v for p, v in target.items() if p in BIG) > 5760
                continue
            segments = result['segments']
            assert abs(sum(s['seconds'] for s in segments)-2880) < 1e-5
            for segment in segments:
                assert segment['seconds'] > 0 and valid(segment['players'], limit)
                assert set(segment['players']) <= set(target)
            start = game['candidate_starters'] if key == 'minimum_change_candidate' else game['starters']
            assert sum(s['seconds'] for s in segments if sorted(s['players']) == start) >= 180 - 1e-5
            for p in target:
                value = sum(s['seconds'] for s in segments if p in s['players'])
                assert abs(value - result['player_seconds'][p]) < 1e-5
                if key == 'minimum_change_candidate':
                    assert bounds[p][0]-1e-5 <= value <= bounds[p][1]+1e-5
                else:
                    assert abs(value-target[p]) < 1e-5
            assert abs(result['l1_seconds']-sum(abs(result['player_seconds'][p]-target[p]) for p in target)) < 1e-5
            if key == 'minimum_change_candidate':
                # Moving each excess big second to a perimeter player costs two L1 seconds.
                # Achieving this independent lower bound proves optimality for this policy.
                assert abs(result['l1_seconds']/2 - max(0, game['big_seconds']-5760)) < 1e-5
    assert not list(ROOT.glob('manuscripts/**/*'))


def main():
    args = argparse.ArgumentParser()
    args.add_argument('--write', action='store_true')
    write = args.parse_args().write
    data = build() if write else json.loads(OUTPUT.read_text())
    verify(data)
    if write:
        OUTPUT.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':'))+'\n')
    for scenario in ('PORTER_ZERO', 'PORTER_CAPPED'):
        games = [g for g in data['games'] if g['scenario'] == scenario]
        print(scenario, {key: dict(Counter(g[key]['status'] for g in games)) for key in ('strict_two_big','three_big_sensitivity','minimum_change_candidate')})
        print('strict failures:', [(g['date'], g['big_seconds']-5760) for g in games if g['strict_two_big']['status']=='INFEASIBLE'])
        print('candidate one-way transferred seconds:', round(sum(g['minimum_change_candidate']['l1_seconds']/2 for g in games), 4))
    print('PASS: witnesses checked independently of solver; availability, defensive matchups and outcomes remain HOLD')


if __name__ == '__main__':
    main()
