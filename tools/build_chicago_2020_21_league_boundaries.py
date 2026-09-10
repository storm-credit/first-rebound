"""O-15F14-A: complete non-CHI schedule screen and one-result sensitivity.
Hypothetical flips identify leverage, never predict or select game outcomes.
"""
import argparse
import csv
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
import build_chicago_2020_21_standings_board as sb

S = sb.S
OUT = S / 'CHICAGO_2020_21_LEAGUE_BOUNDARIES.json'
QUEUE = S / 'NBA_2020_21_NON_CHICAGO_CONTACT_SCREEN.csv'
DIVISIONS = [set(x.split()) for x in (
    'BOS BKN NYK PHI TOR', 'CHI CLE DET IND MIL', 'ATL CHA MIA ORL WAS')]
DIRECT_ALL = {
    'MIN': '2020 rival replaces Edwards', 'CHA': '2020 Edwards/Terry/center cascade',
    'DET': '2020 Patrick/Kira replace Hayes/Bey', 'NOP': '2020 Hayes replaces Kira',
    'DEN': '2020 Bey/Nnaji replace Nnaji/Hampton; Gordon package conditional',
    'DAL': '2020 Hampton replaces Terry', 'WAS': 'Trent replaces Bonga; Brown retained after deadline',
    'POR': 'Trent absent; Powell absent and Hood retained in working path'}
DIRECT_AFTER = {'ORL': 'Vucevic/Aminu retained; Harris/Nnaji conditional',
                'TOR': 'Powell retained; Trent/Hood not acquired in working path'}
CHAIN_ALL = {'GSW': 'Wiggins core/Hutchison supplemental asset unresolved',
             'LAL': 'AD upstream asset chain retained conditionally'}


def normalized_games():
    rows, _ = sb.baseline()
    return [{'id': f"{r['date']}_{r['home']}_{r['away']}", 'date': r['date'],
             'home': r['home'], 'away': r['away'],
             'winner': r['home'] if int(r['home_score']) > int(r['away_score']) else r['away'],
             'margin': abs(int(r['home_score']) - int(r['away_score']))} for r in rows]


def record_wins(games):
    return Counter(g['winner'] for g in games)


def chi_rank(games):
    """Resolve only Chicago's low-record tie group, not the whole conference order."""
    wins = record_wins(games)
    tied = {t for t in sb.EAST if wins[t] == wins['CHI']}
    # No division leader is in a reachable 31-33-win tie in this experiment.
    for division in DIVISIONS:
        assert max(wins[t] for t in division) > wins['CHI']
    ahead = sum(wins[t] > wins['CHI'] for t in sb.EAST)
    while len(tied) > 1:
        wp, gp = Counter(), Counter()
        for g in games:
            if g['home'] in tied and g['away'] in tied:
                gp.update((g['home'], g['away']))
                wp[g['winner']] += 1
        pct = {t: Fraction(wp[t], gp[t]) for t in tied}
        level = pct['CHI']
        ahead += sum(p > level for p in pct.values())
        remaining = {t for t, p in pct.items() if p == level}
        assert len(remaining) < len(tied), 'Full tie needs later NBA criteria; do not guess.'
        tied = remaining
    return 1 + ahead


def contact(g):
    direct, chain = [], []
    for t in (g['home'], g['away']):
        if t in DIRECT_ALL:
            direct.append(f'{t}: {DIRECT_ALL[t]}')
        if g['date'] >= '2021-03-25' and t in DIRECT_AFTER:
            direct.append(f'{t}: {DIRECT_AFTER[t]}')
        if t in CHAIN_ALL:
            chain.append(f'{t}: {CHAIN_ALL[t]}')
        if g['date'] >= '2021-03-25' and t == 'BOS':
            chain.append('BOS: Fournier/Wagner/Parker path conditional; observed roster can match')
    status = 'DIRECT_ROSTER_CONTACT' if direct else 'TRANSACTION_DEPENDENCY' if chain else 'NO_DIRECT_DELTA_IDENTIFIED'
    return status, direct, chain


def changed_game(g):
    return {**g, 'winner': g['away'] if g['winner'] == g['home'] else g['home']}


def build():
    actual = normalized_games()
    board = json.loads(sb.OUT.read_text())
    nonchi = [g for g in actual if 'CHI' not in (g['home'], g['away'])]
    assert len(nonchi) == 1008
    screen = []
    for g in nonchi:
        status, direct, chain = contact(g)
        screen.append({**g, 'contact_status': status, 'direct_reasons': '|'.join(direct),
                       'dependency_reasons': '|'.join(chain), 'impact_status': 'NOT_CALCULATED',
                       'selected': False})
    cases = []
    rank_changing_ids = set()
    for c in board['record_candidates']:
        games = []
        for g in actual:
            if 'CHI' in (g['home'], g['away']):
                winner = 'CHI' if c['outcomes'][g['date']] else (g['away'] if g['home'] == 'CHI' else g['home'])
                games.append({**g, 'winner': winner})
            else:
                games.append(g.copy())
        n = c['chicago_record'][0]
        initial = chi_rank(games)
        assert initial == c['east_regular_season_rank']
        transitions = Counter()
        witnesses = []
        for i, g in enumerate(games):
            if 'CHI' in (g['home'], g['away']):
                continue
            flipped = changed_game(g)
            games[i] = flipped
            new_rank = chi_rank(games)
            assert sum(record_wins(games).values()) == 1080 and record_wins(games)['CHI'] == n
            transitions[new_rank] += 1
            if new_rank != initial:
                status, _, _ = contact(g)
                witnesses.append({'game_id': g['id'], 'date': g['date'], 'actual_winner': g['winner'],
                    'hypothetical_winner': flipped['winner'], 'actual_margin': g['margin'],
                    'new_chicago_rank': new_rank, 'contact_status': status, 'selected': False})
                rank_changing_ids.add(g['id'])
            games[i] = g
        # Independent two-loss witness: keep CHI31 and change only CHA vs SAC/GSW.
        two_ids = ['2021-02-28_SAC_CHA', '2021-02-20_CHA_GSW']
        two_games = [changed_game(g) if g['id'] in two_ids else g for g in games]
        two_rank = chi_rank(two_games)
        thresholds = []
        for t in ('CHA', 'WAS', 'IND', 'BOS'):
            # Isolated competitor losses to West avoid boosting another East competitor.
            wins = record_wins(games)
            h2h = sb.head_to_head([{'home': g['home'], 'away': g['away'],
                'home_score': 1 if g['winner'] == g['home'] else 0,
                'away_score': 1 if g['winner'] == g['away'] else 0} for g in games], 'CHI', t)
            thresholds.append({'team': t, 'wins': wins[t], 'CHI_h2h': h2h,
                'losses_to_reach_CHI_record': max(0, wins[t]-n),
                'warning': 'Isolated record threshold, not independent simultaneous league changes.'})
        cases.append({'CHI_wins': n, 'initial_rank': initial,
            'one_flip_trials': 1008, 'one_flip_rank_counts': {str(k): v for k,v in sorted(transitions.items())},
            'rank_change_witnesses': witnesses, 'isolated_competitor_thresholds': thresholds,
            'two_CHA_losses_witness': {'game_ids': two_ids, 'CHI_rank': two_rank, 'selected': False}})
    for row in screen:
        row['changes_CHI_rank_in_one_flip_screen'] = row['id'] in rank_changing_ids
        row['review_priority'] = ('P1_BOUNDARY' if row['id'] in rank_changing_ids and row['margin'] <= 3
                                  else 'P2_BOUNDARY' if row['id'] in rank_changing_ids else 'P3_REMAINDER')
    return {'stage': 'O-15F14-A', 'status': 'CONTACT_SCREEN_AND_BOUNDARY_SENSITIVITY_COMPLETE',
        'upstream_sha256': hashlib.sha256(sb.OUT.read_bytes()).hexdigest(),
        'scope': 'Non-CHI game screening and hypothetical one-result flips; no new impact estimates or outcome selections.',
        'cutoff_policy': '2021-03-25 is a conservative transaction review boundary, not same-day eligibility.',
        'screen_counts': dict(Counter(r['contact_status'] for r in screen)),
        'priority_counts': dict(Counter(r['review_priority'] for r in screen)),
        'sensitivity_cases': cases,
        'boundary_game_ids': sorted(rank_changing_ids), 'manuscript_allowed': False}, screen


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--write', action='store_true')
    args = p.parse_args()
    result, rows = build()
    if args.write:
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        with QUEUE.open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
    else:
        assert json.loads(OUT.read_text()) == result
        with QUEUE.open() as stream:
            saved = list(csv.DictReader(stream))
        assert saved == [{k: str(v) for k,v in r.items()} for r in rows]
    print(json.dumps({'PASS': True, 'screen': result['screen_counts'], 'priority': result['priority_counts'],
        'ranks': {c['CHI_wins']: c['one_flip_rank_counts'] for c in result['sensitivity_cases']}}))
