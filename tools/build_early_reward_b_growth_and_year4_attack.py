"""B-direction working growth inputs and dated year4 shot costs.

Prior vintages and alternate minutes are explicit; no awards, game scores, or
rating improvement are inferred. The original null P prior stays immutable.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import json
from pathlib import Path

from build_early_reward_b_year2_dated_shots import csvrows, csvbytes, jsonbytes, read, sha, rounded

ROOT = Path(__file__).resolve().parents[1]
MODEL = 'simulation/EARLY_REWARD_B_GROWTH_AND_YEAR4_ATTACK_2026_10_11.json'
OUTPUT = 'simulation/EARLY_REWARD_B_YEAR4_DATED_ATTACK_2026_10_11.csv'
SELECTED = 'simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json'
CARRIER = 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json'
PRIOR = 'simulation/CHICAGO_2021_22_PRESEASON_PRIORS.json'
PRE3 = 'simulation/CHICAGO_2020_21_PREDEADLINE_MINUTE_LEDGER.csv'
YEAR1 = 'simulation/LC1_CHICAGO_2018_2019_USED_DEVELOPMENT_AND_RESULT_CONTACT_IMPLEMENTATION_2026_10_09.json'
YEAR2 = 'simulation/EARLY_REWARD_B_YEAR2_CREDIT_BUDGET_2026_10_11.json'
AUTHOR = 'canon/EARLY_REWARD_B_AUTHOR_SELECTION_2026_10_11.json'
PINS = [SELECTED, CARRIER, PRIOR, PRE3, YEAR1, YEAR2, AUTHOR,
        'simulation/EARLY_REWARD_B_YEAR2_COURT_IMPACT_2026_10_11.json',
        'simulation/CHICAGO_2020_21_PREDEADLINE_PRODUCTION_PRIORS.csv',
        'simulation/CHICAGO_2020_21_POSTDEADLINE_BOX_INPUTS.json',
        'simulation/CHICAGO_2018_19_PLAYER_PRODUCTION_PRIORS.md']
WEIGHTS = {'LaVine': F(3, 10), 'LaMelo_pick4': F(1, 4),
           'Markkanen': F(1, 5), 'Coby': F(3, 20), 'Young': F(1, 10)}
TARGET = {'two_pa': F(55), 'three_pa': F(35), 'fta': F(24), 'tov': F(15)}


def coherent(pts36, ts, three_pa, three_p, fta, ft, tov):
    vals = list(map(F, [pts36, ts, three_pa, three_p, fta, ft, tov]))
    pts, ts, three_pa, three_p, fta, ft, tov = vals
    fga = pts / (2 * ts) - F(11, 25) * fta
    two_pa = fga - three_pa
    two_pm = (pts - 3 * three_pa * three_p - fta * ft) / 2
    assert 0 <= two_pm <= two_pa and 0 <= three_p <= 1 and 0 <= ft <= 1
    return {'pts': pts, 'two_pa': two_pa, 'three_pa': three_pa, 'fta': fta, 'tov': tov,
            'two_p': two_pm / two_pa, 'three_p': three_p, 'ft': ft, 'ts': ts}


def rebalance(values, target):
    values = dict(values)
    active = {p for p, v in values.items() if v > 0}
    needed = sum(values.values()) - target
    assert target >= 0 and active
    original = dict(values)
    if needed < 0:
        names = sorted(active & set(WEIGHTS)) or sorted(active)
        weights = {p: WEIGHTS.get(p, F(1)) for p in names}
        total = sum(weights.values())
        for p in names:
            values[p] += -needed * weights[p] / total
    else:
        names = active & set(WEIGHTS)
        while needed:
            names = {p for p in names if values[p] > 0} or {p for p in active if values[p] > 0}
            assert names, 'No recipient capacity'
            weight = sum(WEIGHTS.get(p, F(1)) for p in names)
            demand = needed
            for p in sorted(names):
                take = min(values[p], demand * WEIGHTS.get(p, F(1)) / weight)
                values[p] -= take
                needed -= take
    assert sum(values.values()) == target and min(values.values()) >= 0
    return values, {p: values[p] - original[p] for p in values}


def make():
    assert json.loads(read(AUTHOR))['B']['selected_option'] == 'B'
    priors = json.loads(read(PRIOR))
    assert priors['opening_information_cutoff'] == '2021-10-19'
    by_prior = {p['player']: p for p in priors['players']}
    assert by_prior['Protagonist']['alternate_2021_22_per36'] is None
    # Explicit working choices inside the already selected B direction. These
    # replace no historical values and are not an author lock of exact records.
    growth = {
        'year1': coherent('16.50192302660841', '.530', '2.3', '.280', '4', '.700', '1.8'),
        'year3': coherent('21.1', '.580', '3.6', '.335', '5.4', '.750', '2.3'),
        'year4': coherent('22.5', '.580', '4.5', '.350', '5.5', '.780', '2.5')}
    # Rookie role precision: exact 1274:02 rather than old rounded proxy.
    exact1_min = F(1274 * 60 + 2, 60)
    growth['year1'] = coherent(F(8 * 73 * 36) / exact1_min, '.530', '2.3', '.280', '4', '.700', '1.8')
    prior_rows = []
    for year, role_min, games in [('year1', exact1_min, 73), ('year3', F(1219), 43),
                                   ('year4', F(82 * 32), 82)]:
        vector = growth[year]
        prior_rows.append({'NBA_year': int(year[-1]), 'per36': {k: rounded(v) for k, v in vector.items()},
                           'role_scope': 'predeadline43only' if year == 'year3' else 'regulation82only' if year == 'year4' else 'selected73GPexact1274:02',
                           'reference_minutes': rounded(role_min), 'reference_games': games,
                           'expected_pts_in_scope': rounded(vector['pts'] * role_min / 36),
                           'expected_ppg_in_scope': rounded(vector['pts'] * role_min / (36 * games)),
                           'exact_season_box_selected': False})
    # NCAA-to-NBA translation is a declared model, not missing NBA data=zero.
    duarte = coherent('13.5', '.550', '4', '.350', '3', '.750', '2')
    rates = {'Protagonist': growth['year4'], 'Chris Duarte': duarte}
    for name, entry in by_prior.items():
        observed = entry.get('historical_prior')
        if observed:
            v = {k: F(str(x)) for k, x in observed['per36'].items()}
            rates[name] = {'pts': v['pts'], 'two_pa': v['fga'] - v['fg3a'],
                           'three_pa': v['fg3a'], 'fta': v['fta'], 'tov': v['tov'],
                           'two_p': (v['fgm'] - v['fg3m']) / (v['fga'] - v['fg3a']),
                           'three_p': v['fg3m'] / v['fg3a'] if v['fg3a'] else F(0),
                           'ft': v['ftm'] / v['fta'] if v['fta'] else F(0)}
            assert observed['last_source_date'] < '2021-10-20'
    selected = json.loads(read(SELECTED))['selected_dates']
    carrier = json.loads(read(CARRIER))['rows']
    output, dates, before_totals, after_totals = [], [], defaultdict(F), defaultdict(F)
    assert len(selected) == 82 and len({g['game_id'] for g in selected}) == 82
    for game in selected:
        role = game['selected_regulation_player_minutes']
        assert role['Protagonist'] == 32 and role['Markkanen'] == 32 and role['Caruso'] == 18
        assert sum(role.values()) == 240 and set(role) <= set(rates)
        witness = carrier[int(game['selected_carrier_source']['pointer'].split('/')[-1])]
        assert witness['candidate_date'] == game['date'] and witness['state'] == game['selected_chicago_state']
        totals = defaultdict(F)
        for block in witness['unordered_regulation_blocks']:
            names = list(block['positions'].values())
            assert len(set(names)) == 5
            for p in names:
                totals[p] += F(str(block['minutes']))
        assert dict(totals) == {p: F(v) for p, v in role.items()}
        assert sum(F(str(b['minutes'])) for b in witness['unordered_regulation_blocks']) == 48
        scaled = {p: {k: rates[p][k] * F(minutes) / 36 for k in TARGET}
                  for p, minutes in role.items()}
        allocated = defaultdict(dict)
        adjustments = defaultdict(dict)
        for category, target in TARGET.items():
            # Fixed team scenario envelope, not historical same-date cap.
            remaining, delta = rebalance({p: v[category] for p, v in scaled.items() if p != 'Protagonist'},
                                         target - scaled['Protagonist'][category])
            for p in scaled:
                allocated[p][category] = scaled[p][category] if p == 'Protagonist' else remaining[p]
                adjustments[p][category] = F(0) if p == 'Protagonist' else delta[p]
            assert sum(allocated[p][category] for p in scaled) == target
        team_pts = F(0)
        for p in sorted(scaled):
            a, r = allocated[p], rates[p]
            pts = 2 * a['two_pa'] * r['two_p'] + 3 * a['three_pa'] * r['three_p'] + a['fta'] * r['ft']
            previous = 2 * scaled[p]['two_pa'] * r['two_p'] + 3 * scaled[p]['three_pa'] * r['three_p'] + scaled[p]['fta'] * r['ft']
            before_totals[p] += previous
            after_totals[p] += pts
            team_pts += pts
            output.append({'game_id': game['game_id'], 'date': game['date'], 'state': game['selected_chicago_state'],
                           'actor': p, 'regulation_minutes': role[p],
                           **{f'expected_{k}': rounded(v) for k, v in a.items()},
                           'expected_fga': rounded(a['two_pa'] + a['three_pa']),
                           **{f'coactor_delta_{k}': rounded(v) for k, v in adjustments[p].items()},
                           'expected_two_pm': rounded(a['two_pa'] * r['two_p']),
                           'expected_three_pm': rounded(a['three_pa'] * r['three_p']),
                           'expected_ftm': rounded(a['fta'] * r['ft']),
                           'expected_pts': rounded(pts), 'scaled_before_rebalance_pts': rounded(previous),
                           'actual_box_or_result': False})
        dates.append({'game_id': game['game_id'], 'date': game['date'], 'state': game['selected_chicago_state'],
                      'expected_team_pts': rounded(team_pts), 'expected_P_pts': 20,
                      'role_court_replayed': True, 'result_from_growth_selected': False})
    pre3 = csvrows(PRE3)
    early3 = [r for r in pre3 if r['date'] < '2021-02-23']
    early4 = [g for g in selected if g['date'] < '2022-02-03']
    same4 = [g['game_id'] for g in selected if g['date'] == '2022-02-03']
    assert len(pre3) == 43 and all(r['date'] <= '2021-03-24' for r in pre3)
    data = {'id': 'EARLY_REWARD_B_GROWTH_AND_YEAR4_ATTACK_2026_10_11',
            'status': 'WORKING_B_GROWTH_INPUTS_YEAR4_DATED_ROLE_SHOT_COSTS_IMPLEMENTED_IMPACT_AWARDS_PENDING',
            'authority': 'Implementation of B direction; fictional working growth/input choices. No exact stat or individual award author lock.',
            'source_sha256': {p: sha(p) for p in PINS}, 'growth_vectors': prior_rows,
            'year2_current_input': {'path': YEAR2, 'target_ppg': 12, 'current_court_impact_path': 'simulation/EARLY_REWARD_B_YEAR2_COURT_IMPACT_2026_10_11.json'},
            'year3_post29_illustration_only': {'minutes': 870, 'PTS36': 21.1,
                                             'expected_pts': rounded(growth['year3']['pts'] * 870 / 36),
                                             'exact_post_health_or_minutes_selected_here': False,
                                             'combined_reference_not_full_official_season': True},
            'year1_and_year3_dated_opportunity_costs_complete': False,
            'year4': {'scope': '82 selected regulation-role dates, normal58/CobyOut24; no OT extension',
                      'P_expected_regulation_points': rounded(after_totals['Protagonist']),
                      'P_expected_regulation_ppg': 20, 'original_P_null_not_changed_or_treated_as_zero': True,
                      'Duarte_declared_rookie_translation_per36': {k: rounded(v) for k, v in duarte.items()},
                      'coactor_initial_rates': '2020–21 historical per36 available at2021Oct19, scaled to current alternative roles; conversion fractions retained as explicit model assumption, not causal efficacy',
                      'team_declared_regulation_opportunity_envelope': {'FGA': 90, '3PA': 35, 'FTA': 24, 'player_TOV': 15},
                      'envelope_classification': 'FICTIONAL_WORKING_MODEL_CHOICE_NOT_RULE_OR_HISTORICAL_GAME_CAP',
                      'core_cut_preference': {p: rounded(v) for p, v in WEIGHTS.items()},
                      'P_reb_ast_not_invented_from_scoring': True,
                      'dates': dates, 'coactor_cost_totals': [{'actor': p, 'before_rebalance_expected_pts': rounded(before_totals[p]),
                                                             'after_rebalance_expected_pts': rounded(after_totals[p]),
                                                             'delta': rounded(after_totals[p] - before_totals[p])} for p in sorted(after_totals)],
                      'whole_possession_or_result_join_certified': False},
            'recognition_clock_inputs': {'year3_before_Feb23_ET_day': {'count': len(early3),
                'minutes': sum(int(r['protagonist_seconds']) for r in early3) / 60,
                'excluded_from_reserve_selection_evidence': 'Feb23 same-day unknown announcement chronology and all later games; March24 full43 is not selection evidence'},
                'year4_before_Feb3_ET_day': {'count': len(early4), 'P_regulation_minutes': 32 * len(early4),
                'same_day_game_ids_excluded': same4, 'excluded_from_reserve_selection_evidence': 'Feb3 same-day unknown timing and later games; season52wins/PHI7 not selection-day evidence'},
                'selected_awards': [], 'votes_not_manufactured': True},
            'preserved': ['RookieDec7 opportunity loss/weakhand first wall', 'year2 seed7/pick4/LaMelo',
                          'year3 31–41/WAS win/IND loss as existing selected endpoints requiring impact join',
                          'year4 Mark32/Caruso18/LMprimaryPG/current52–30/PHI loss/2022fixed E2 prices',
                          'individualHigherMax conditional, no award or salary escalator selected'],
            'remaining': ['Year1/year3 dated attack/coactor opportunity budgets', 'new fictional impact assumptions and used result consumer joins',
                          'selected recognition outcome with competing players/slots', '2023growth baseline double counting check',
                          'C01/current history/finalallocation/Blueprint/Pack'],
            'gates': {'freeze': 'v0.30 PARTIAL', 'design': 'CLOSED', 'manuscript': 'CLOSED', 'actual_Pack': 0}}
    assert Counter(g['selected_chicago_state'] for g in selected) == {'NORMAL': 58, 'COBY_OUT': 24}
    assert after_totals['Protagonist'] == 1640
    return {MODEL: jsonbytes(data), OUTPUT: csvbytes(output)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = make()
    if args.check:
        for p, b in output.items():
            assert (ROOT / p).read_bytes().replace(b'\r\n', b'\n') == b, p
        print('PASS3 coherent growth vectors/82 selected role courts/4 daily opportunity budgets; recognition cutoff partition; awards pending')
    else:
        assert all(not (ROOT / p).exists() for p in output), 'Refusing overwrite'
        for p, b in output.items():
            (ROOT / p).write_bytes(b)
        print('WROTE2 B growth/year4 attack files')
