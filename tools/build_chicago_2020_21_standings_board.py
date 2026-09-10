"""O-15F13: conditional standings, using O-15F12 BASE paths without re-solving minutes."""
import argparse
import csv
import hashlib
import json
from collections import Counter
import build_chicago_2020_21_integrated_paths as ip

S = ip.S
GAMES = S / 'NBA_2020_21_REGULAR_GAME_BASELINE.csv'
OUT = S / 'CHICAGO_2020_21_STANDINGS_PICK_BOARD.json'
EAST = set('PHI BKN MIL NYK ATL MIA BOS WAS IND CHA CHI TOR CLE ORL DET'.split())


def baseline():
    with GAMES.open() as stream:
        rows = list(csv.DictReader(stream))
    wins, played = Counter(), Counter()
    assert len(rows) == len({(r['date'], r['home'], r['away']) for r in rows}) == 1080
    for r in rows:
        h, a = r['home'], r['away']
        hs, aws = int(r['home_score']), int(r['away_score'])
        assert hs != aws
        wins[h if hs > aws else a] += 1
        played.update((h, a))
    assert len(played) == 30 and set(played.values()) == {72} and sum(wins.values()) == 1080
    return rows, dict(wins)


def head_to_head(rows, first, second):
    record = [0, 0]
    for r in rows:
        if {r['home'], r['away']} == {first, second}:
            winner = r['home'] if int(r['home_score']) > int(r['away_score']) else r['away']
            record[int(winner != first)] += 1
    return record


def lottery_band(wins, nonplayoff, team='CHI'):
    """Pre-draw record ranks only. Postseason H2H must never order lottery ties."""
    if team not in nonplayoff:
        return None
    lower = sum(wins[t] < wins[team] for t in nonplayoff)
    tied = sorted(t for t in nonplayoff if wins[t] == wins[team])
    return {'record_rank_band': [lower + 1, lower + len(tied)], 'tied_teams': tied,
            'exact_pick': None, 'odds': None, 'draft_tiebreak': 'UNSELECTED'}


def build():
    rows, actual = baseline()
    provenance = json.loads((S / 'NBA_2020_21_STANDINGS_PROVENANCE.json').read_text())
    assert hashlib.sha256(GAMES.read_bytes()).hexdigest() == provenance['extract_sha256']
    data = json.loads(ip.OUT.read_text())
    cross = json.loads(ip.cc.OUT.read_text())
    close = json.loads(ip.close.OUT.read_text())
    chi_actual = {}
    for r in rows:
        if 'CHI' in (r['home'], r['away']):
            home = r['home'] == 'CHI'
            chi_actual[r['date']] = (r['away'] if home else r['home'],
                (int(r['home_score']) - int(r['away_score'])) * (1 if home else -1))
    assert len(chi_actual) == 72
    groups = {}
    total = 0
    for scenario in data['season_scenarios']:
        if scenario['prior'] != 'BASE':
            continue
        games = ip.season_games(data['remaining_pre_paired_inputs'], cross, close,
            *scenario['path_id'].split('/'), scenario['availability'], scenario['method'],
            scenario['prior'], scenario['fatigue'])
        assert {g['date']: (g['opponent'], g['actual_margin']) for g in games} == chi_actual
        for interval in scenario['rating_intervals']:
            assert not interval['zero_margin_dates']
            r = sum(interval['rating_open_interval']) / 2
            outcomes = {}
            for g in games:
                margin = g['constant'] + g['coefficient'] * r
                if g.get('other_unknown_coefficients'):
                    lo, hi = g['other_unknown_margin_band']
                    assert lo > 0 or hi < 0
                    win = lo > 0
                else:
                    assert abs(margin) > 1e-7
                    win = margin > 0
                outcomes[g['date']] = bool(win)
            n = sum(outcomes.values())
            assert n == interval['positive_margin_games']
            deltas = Counter()
            for g in games:
                deltas[g['opponent']] += int(g['actual_margin'] > 0) - int(outcomes[g['date']])
            deltas = {t: d for t, d in sorted(deltas.items()) if d}
            assert deltas == interval['opponent_win_deltas_from_chicago_games']
            assert n - actual['CHI'] + sum(deltas.values()) == 0
            witness = {k: scenario[k] for k in ('path_id', 'availability', 'method', 'prior', 'fatigue')}
            witness['rating_open_interval'] = interval['rating_open_interval']
            if n not in groups:
                groups[n] = {'chicago_record': [n, 72-n], 'selected': False,
                    'outcomes': outcomes, 'opponent_win_deltas': deltas, 'source_conditions': []}
            group = groups[n]
            assert group['outcomes'] == outcomes and group['opponent_win_deltas'] == deltas
            group['source_conditions'].append(witness)
            total += 1
    assert set(groups) == {31, 32, 33} and total == 72
    for n, g in sorted(groups.items()):
        wins = actual.copy()
        wins['CHI'] = n
        for t, d in g['opponent_win_deltas'].items():
            wins[t] += d
        assert sum(wins.values()) == 1080 and all(0 <= w <= 72 for w in wins.values())
        g['conditional_team_records'] = {t: [w, 72-w] for t, w in sorted(wins.items())}
        cha_dates = sorted(d for d, (t, _) in chi_actual.items() if t == 'CHA')
        cha_wins = sum(g['outcomes'][d] for d in cha_dates)
        g['chicago_charlotte_h2h'] = {'dates': cha_dates, 'record': [cha_wins, len(cha_dates)-cha_wins]}
        tied = [t for t in EAST if wins[t] == n and t != 'CHI']
        rank = 1 + sum(wins[t] > n for t in EAST)
        assert tied == ([] if n < 33 else ['CHA']) and cha_wins == 3
        g['east_regular_season_rank'] = rank
        g['play_in_entry'] = 7 <= rank <= 10
        g['changed_games'] = [{'date': d, 'opponent': t, 'actual_win': m > 0,
            'conditional_win': g['outcomes'][d]} for d, (t, m) in sorted(chi_actual.items())
            if (m > 0) != g['outcomes'][d]]
        # All teams below 33 wins miss play-in in this held-other-games diagnostic.
        # West play-in can change membership above CHI; enumerate SAS admission separately.
        pool = {t for t, w in wins.items() if w < 33} | {'CHI', 'CHA'}
        assert all(w > n for t, w in wins.items() if t not in pool | {'SAS'})
        g['lottery_if_chicago_misses_playoffs'] = [
            {'sas_playoff_qualification': status, **lottery_band(wins, pool | ({'SAS'} if status == 'NO' else set()))}
            for status in ('NO', 'YES')]
        g['lottery_if_chicago_qualifies'] = None
        g['lottery_comparison_scope'] = 'Only lower/equal records are required; not a complete 14-team field.'
        g['east_was_ind_h2h'] = head_to_head(rows, 'WAS', 'IND')
        g['playoff_qualification'] = 'UNSELECTED' if rank == 10 else 'NO_IN_THIS_DIAGNOSTIC'
        g['own_first_owner'] = {'2021': 'CHI', '2023': 'CHI'}
        g['west_boundary'] = {'POR_record': [wins['POR'], 72-wins['POR']],
            'LAL_record': [wins['LAL'], 72-wins['LAL']],
            'GSW_record': [wins['GSW'], 72-wins['GSW']],
            'GSW_MEM_h2h': head_to_head(rows, 'GSW', 'MEM'),
            'POR_play_in': wins['POR'] < wins['LAL'],
            'play_in_results': 'UNSELECTED'}
    return {'stage': 'O-15F13', 'status': 'CONDITIONAL_STANDINGS_PICK_BOARD / FINAL_SEASON_HOLD',
        'scope': 'Chicago games changed; other 1008 games held observed. NOT_FULL_ALTERNATE_LEAGUE.',
        'upstream_sha256': hashlib.sha256(ip.OUT.read_bytes()).hexdigest(),
        'baseline_games': 1080, 'baseline_records': {t: [w, 72-w] for t, w in sorted(actual.items())},
        'base_conditions': total, 'record_candidates': [groups[n] for n in sorted(groups)],
        'unknown_rating_policy': 'Interior witness of each upstream interval; no rating selected. Nuisance signs use proven bands.',
        'zero_boundaries': 'Upstream unresolved boundaries excluded, not counted as losses.',
        'lottery_policy': 'Record rank bands only, conditional on nonplayoff membership; no exact pick, odds, or random draw.',
        'manuscript_allowed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.write:
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    else:
        assert json.loads(OUT.read_text()) == result
    print('PASS O-15F13: 1080 games, 72 BASE conditions, 3 diagnostic records; final season HOLD')
