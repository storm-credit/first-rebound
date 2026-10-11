"""Construct a fictional integer court witness; independently verify saved rows.

This is an existence construction, not recovered substitutions or a box-to-BPM
conversion. The impact sheet varies declared ratings instead of adding PTS to
historical margins. Source clocks and older source generations remain intact.
"""
import argparse
import csv
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix

from build_early_reward_b_year2_dated_shots import csvrows, csvbytes, jsonbytes, sha

ROOT = Path(__file__).resolve().parents[1]
STEM = 'simulation/EARLY_REWARD_B_YEAR2_COURT_IMPACT_2026_10_11'
COURT = STEM + '_COURT.csv'
IMPACT = STEM + '_SENSITIVITY.csv'
MODEL = STEM + '.json'
PRIMARY = 'research/raw/EARLY_REWARD_B_YEAR2_PRIMARY_BOXES_2026_10_11.csv'
SHOTS = 'simulation/EARLY_REWARD_B_YEAR2_DATED_SHOTS_2026_10_11.csv'
LEDGER = 'simulation/CHICAGO_2019_20_PLAYER_GAME_MINUTE_LEDGER.csv'
DONORS = 'simulation/CHICAGO_2019_20_PLAYER_GAME_DONOR_VECTOR.csv'
ROSTER = 'simulation/CHICAGO_2019_20_ROSTER_BASELINE.csv'
OUTCOME = 'simulation/CHICAGO_2019_20_OUTCOME_LEDGER.csv'
RAPTOR = 'simulation/CHICAGO_2019_20_RAPTOR_OUTCOME_LEDGER.csv'
LOTTERY = 'design/CHICAGO_2020_LOTTERY_DECISION_PACKET.md'
PINNED = [PRIMARY, SHOTS, LEDGER, DONORS, ROSTER, OUTCOME, RAPTOR, LOTTERY,
          'canon/EARLY_REWARD_B_AUTHOR_SELECTION_2026_10_11.json']
GUARDS = {'Tomas Satoransky', 'Coby White', 'Kris Dunn', 'Ryan Arcidiacono'}
BIGS = {'Lauri Markkanen', 'Thaddeus Young', 'Wendell Carter Jr.',
        'Daniel Gafford', 'Luke Kornet', 'Cristiano Felicio'}


def valid(five):
    return len(set(five)) == 5 and bool(set(five) & GUARDS) and bool(set(five) & BIGS)


def inputs():
    games = csvrows(LEDGER)
    by = defaultdict(list)
    for row in csvrows(PRIMARY):
        by[row['event_id']].append(row)
    donors = defaultdict(dict)
    for row in csvrows(DONORS):
        donors[row['event_id']][row['player']] = row
    limited = {r['player'] for r in csvrows(ROSTER)
               if r['donor_class'] == 'LIMITED_DONOR'}
    result = []
    for game in games:
        event = game['event_id']
        actual = by[event]
        official = sum(int(r['seconds']) for r in actual)
        assert official % 5 == 0
        clock = official // 5
        seconds = {r['player']: int(donors[event].get(r['player'], r).get(
            'alternate_seconds', r['seconds'])) for r in actual}
        seconds['P'] = int(game['protagonist_seconds'])
        excess = sum(seconds.values()) - official
        assert abs(excess) <= 5, (event, excess)
        correction = None
        if excess:
            # Explicit alternate-witness precision bridge: no real core changes.
            candidates = sorted((p for p in limited if seconds.get(p, 0) > abs(excess)
                                 and seconds[p] - excess <= clock),
                                key=lambda p: (-seconds[p], p))
            assert candidates, event
            correction = candidates[0]
            seconds[correction] -= excess
        seconds = {p: s for p, s in seconds.items() if s}
        assert sum(seconds.values()) == clock * 5
        assert all(0 < s <= clock for s in seconds.values())
        starting = [r['player'] for r in actual if r['starter'] == '1']
        if game['protagonist_start'] == '1':
            assert game['start_source'] in starting
            starting[starting.index(game['start_source'])] = 'P'
        assert valid(starting) and all(p in seconds for p in starting), event
        result.append((game, seconds, starting, clock, excess, correction))
    assert len(result) == 65
    assert sum(s['P'] for _, s, *_ in result) == 1395 * 60
    assert sum(int(g['protagonist_start']) for g, *_ in result) == 18
    return result


def construct(data):
    rows = []
    for game, targets, starting, clock, _, _ in data:
        remaining = dict(targets)
        blocks = [(tuple(starting), 1, 'STARTING_FIVE_EXISTENCE_ONLY')]
        for p in starting:
            remaining[p] -= 1
        rest_clock = clock - 1
        if game['date'] == '2019-11-23':
            for actor in ['Wendell Carter Jr.', 'Daniel Gafford']:
                candidates = [c for c in combinations(sorted(remaining), 5)
                              if 'P' in c and actor in c and valid(c)
                              and min(remaining[p] for p in c) >= 8]
                assert candidates
                chosen = max(candidates, key=lambda c: (min(remaining[p] for p in c), c))
                blocks.append((chosen, 8, 'B_NOV23_BIG_OPPORTUNITY_COST_WINDOW'))
                for p in chosen:
                    remaining[p] -= 8
                rest_clock -= 8
        names = sorted(p for p, s in remaining.items() if s)
        options = [c for c in combinations(names, 5) if valid(c)]
        assert options
        matrix = csc_matrix(np.array([[int(p in c) for c in options] for p in names], dtype=float))
        target = np.array([remaining[p] for p in names], dtype=float)
        # Integer seconds. Ranking only makes the witness reproducible on this
        # runtime; it does not optimize NBA tactics or estimate substitution time.
        solved = milp(np.arange(1, len(options) + 1, dtype=float),
                      integrality=np.ones(len(options)), bounds=Bounds(0, rest_clock),
                      constraints=LinearConstraint(matrix, target, target),
                      options={'time_limit': 20, 'mip_rel_gap': 0.01})
        assert solved.x is not None, (game['event_id'], solved.message)
        integer = np.rint(solved.x).astype(int)
        assert np.max(np.abs(solved.x - integer)) < 1e-5
        assert np.array_equal(matrix @ integer, target)
        blocks.extend((c, int(v), 'FICTIONAL_EXISTENCE_BLOCK')
                      for c, v in zip(options, integer) if v)
        cursor = 0
        for index, (five, duration, purpose) in enumerate(blocks, 1):
            rows.append({'event_id': game['event_id'], 'date': game['date'],
                         'block': index, 'start_elapsed_seconds': cursor,
                         'end_elapsed_seconds': cursor + duration, 'duration_seconds': duration,
                         **{f'actor_{i}': p for i, p in enumerate(five, 1)},
                         'purpose': purpose, 'historical_substitution': False})
            cursor += duration
        assert cursor == clock
    return rows


def verify_court(rows, data):
    by = defaultdict(list)
    for row in rows:
        by[row['event_id']].append(row)
    assert set(by) == {g['event_id'] for g, *_ in data}
    output = []
    for game, targets, starting, clock, excess, correction in data:
        blocks = by[game['event_id']]
        totals = Counter()
        overlap = Counter()
        cursor = 0
        for index, row in enumerate(blocks, 1):
            five = [row[f'actor_{i}'] for i in range(1, 6)]
            duration = int(row['duration_seconds'])
            assert row['date'] == game['date'] and int(row['block']) == index
            assert valid(five) and set(five) <= set(targets)
            assert int(row['start_elapsed_seconds']) == cursor and duration > 0
            cursor += duration
            assert int(row['end_elapsed_seconds']) == cursor
            for p in five:
                totals[p] += duration
                if 'P' in five and p != 'P':
                    overlap[p] += duration
        assert cursor == clock and dict(totals) == targets
        assert set(blocks[0][f'actor_{i}'] for i in range(1, 6)) == set(starting)
        if game['date'] == '2019-11-23':
            assert overlap['Wendell Carter Jr.'] >= 8 and overlap['Daniel Gafford'] >= 8
        output.append({'event_id': game['event_id'], 'date': game['date'],
                       'elapsed_seconds': clock, 'blocks': len(blocks),
                       'legacy_excess_player_seconds': excess,
                       'witness_precision_debit_actor': correction,
                       'P_shared_seconds': dict(sorted(overlap.items()))})
    return output


def sensitivity():
    outcome = csvrows(OUTCOME)
    rows, summaries, boundaries = [], [], []
    families = []
    for proxy in ['BPM', 'NET_EB']:
        base = [r for r in outcome if r['proxy'] == proxy and r['scenario'] == 'BASE']
        assert len(base) == 65
        for fatigue, field in [('0', 'base_alt_margin'), ('0.5', 'fatigue_05_alt_margin'),
                               ('1', 'fatigue_10_alt_margin')]:
            families.append((proxy, fatigue, [(r, F(r[field])) for r in base]))
    raptor = csvrows(RAPTOR)
    for fatigue in ['0', '0.5', '1']:
        base = [r for r in raptor if r['scenario'] == 'BASE'
                and F(r['fatigue_penalty']) == F(fatigue)]
        assert len(base) == 65
        families.append(('RAPTOR_EB1000', fatigue, [(r, F(r['alt_margin'])) for r in base]))
    for proxy, fatigue, base in families:
        thresholds = sorted((-margin / (F(r['protagonist_minutes']) / 48), r['event_id'])
                            for r, margin in base)
        lower, upper = thresholds[20], thresholds[22]
        assert lower[0] < 0 <= upper[0], (proxy, fatigue)
        boundaries.append({'proxy': proxy, 'fatigue_per48_second_night': float(F(fatigue)),
                           'lower_exclusive_exact': str(lower[0]), 'lower_event': lower[1],
                           'upper_inclusive_exact': str(upper[0]), 'upper_event': upper[1]})
        for shift in [F(-2), F(-1), F(0), F(1), F(2), F(3), F(4)]:
            wins, flips = 0, []
            for r, old in base:
                # Per-48 prior method inherited explicitly, no PTS->rating math.
                coefficient = F(r['protagonist_minutes']) / 48
                margin = old + coefficient * shift
                win = margin > 0
                wins += win
                if win != (old > 0):
                    flips.append(r['event_id'])
                rows.append({'event_id': r['event_id'], 'date': r['date'], 'proxy': proxy,
                             'fatigue_per48_second_night': float(F(fatigue)),
                             'declared_P_rating_delta_per48': float(shift),
                             'base_margin_from_saved_parent': float(old),
                             'new_sensitivity_margin': round(float(margin), 9),
                             'wl': 'W' if win else 'L',
                             'P_delta_at_zero_margin': round(float(-old / coefficient), 9),
                             'pts_added_to_margin': False, 'selected_result': False})
            summaries.append({'proxy': proxy, 'fatigue_per48_second_night': float(F(fatigue)),
                              'declared_P_rating_delta_per48': float(shift),
                              'wins': wins, 'losses': 65 - wins, 'changed_events': flips})
    assert len(rows) == 4095
    lower = max(F(b['lower_exclusive_exact']) for b in boundaries)
    upper = min(F(b['upper_inclusive_exact']) for b in boundaries)
    assert lower < 0 <= upper
    # Evaluate endpoints and an interior point in the actual 9 margin families.
    for shift, inside in [(lower, False), ((lower + upper) / 2, True),
                           (upper, True), (upper + F(1, 1000000), False)]:
        counts = [sum(margin + F(r['protagonist_minutes']) / 48 * shift > 0
                      for r, margin in base) for _, _, base in families]
        assert all(21 <= w <= 22 for w in counts) == inside
    compatible = {'scope': 'All three BASE proxies and three existing fatigue levels; saved six-decimal margins and original unchanged coactor ratings only',
                  'lower_exclusive_exact': str(lower), 'upper_inclusive_exact': str(upper),
                  'lower_approx': float(lower), 'upper_approx': float(upper),
                  'family_boundaries': boundaries,
                  'selected_rating_delta': None,
                  'author_selected_lottery_seed7_pick4_LaMelo_preserved': True,
                  'not_new_rating_evidence': True,
                  'meaning': 'A bounded fictional impact assumption in this intersection preserves21–22 in these models. A value outside is not permitted to silently overwrite the approved seed7/pick4 path. This is conditional algebra, not evidence selecting that assumption; changed coactor ratings require recomputation.'}
    return rows, summaries, compatible


def model(data, dates, summaries, compatible):
    return {'id': 'EARLY_REWARD_B_YEAR2_COURT_IMPACT_2026_10_11',
            'status': 'B_YEAR2_INTEGER_COURT_FEASIBLE_RATING_SENSITIVITY_RESULT_NOT_SELECTED',
            'source_sha256': {p: sha(p) for p in PINNED},
            'classification': {'official_final_boxes': 'FACT_EX_POST',
                               'existing_alternate_minutes_and_B_shots': 'FICTIONAL_WORKING_INPUT',
                               'court_rows': 'CONSTRUCTED_EXISTENCE_WITNESS_NOT_HISTORICAL_SUBSTITUTIONS',
                               'rating_grid': 'DECLARED_SENSITIVITY_NOT_ESTIMATED_BPM_OR_NET',
                               'new_exact_results_awards': 'NOT_SELECTED'},
            'court_policy': ['Five unique actors on court at every elapsed second',
                             'At least one Satoransky/White/Dunn/Arcidiacono ballcarrier and one listed big',
                             'No historical DNP/absent actor or removed Hutchison receives minutes',
                             'Existing 18 P starts and 1395 P minutes retained',
                             'Official elapsed clock controls this new witness; signed hybrid-clock differences separately bridged through limited bench donors. Legacy donor alternate seconds are retained before this explicit bridge; other actors use official seconds.',
                             'Starts get one existence second, not a claimed first substitution or plausible coaching stint',
                             'Nov23 both bigs have separate eight-second P coexistence witness, not factual action or observed foul'],
            'precision_bridge_total_player_seconds': sum(x[4] for x in data),
            'dates': dates, 'rating_sensitivity': summaries,
            'approved_result_compatibility_interval': compatible,
            'causal_boundary': 'Changing points without a specified impact assumption does not change the saved outcome model. Delta0 reproduces BASE22 wins, but neither unchanged rating nor positive growth is proven by the new box. The grid exposes event reversals; a new result/draft decision must consume an explicitly selected fictional impact input and its coactor costs.',
            'coactor_efficiency_boundary': 'Court existence does not validate keeping historical shooting conversion after changing shot context. Existing shot/TOV budget is unchanged; signed precision bridge is not silently applied to parent shots.',
            'not_claimed': ['tactical stint realism', 'actual PBP substitutions or five-position assignments',
                            'event-level shots/assists/rebounds/fouls or full possession reconstruction',
                            'new rating forecast or independent causal proof', 'new result/lottery/draft promotion',
                            'B years1/3/4 completion', 'MIP award or actual episode prose'],
            'tools': 'Codex local integer construction and separate CSV replay; no AGY/NotebookLM/Claude/independent agent execution',
            'gates': {'freeze': 'v0.30 PARTIAL', 'design': 'CLOSED', 'manuscript': 'CLOSED', 'actual_pack': 0}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--refresh-own-working-outputs', action='store_true')
    args = parser.parse_args()
    data = inputs()
    if args.check:
        court = csvrows(COURT)
    else:
        assert args.refresh_own_working_outputs or all(not (ROOT / p).exists() for p in [COURT, IMPACT, MODEL]), 'Refusing overwrite'
        court = construct(data)
    dates = verify_court(court, data)
    impacts, summaries, compatible = sensitivity()
    outputs = {IMPACT: csvbytes(impacts), MODEL: jsonbytes(model(data, dates, summaries, compatible))}
    if args.check:
        for p, content in outputs.items():
            assert (ROOT / p).read_bytes().replace(b'\r\n', b'\n') == content, p
        print(f'PASS65 court clocks/{len(court)} blocks/1395 P minutes/18 starts; 4095 sensitivity rows/9 compatibility families; no result selection')
    else:
        outputs[COURT] = csvbytes(court)
        for p, content in outputs.items():
            (ROOT / p).write_bytes(content)
        print(f'WROTE3 files: 65 court clocks/{len(court)} integer blocks; 4095 sensitivity rows')
