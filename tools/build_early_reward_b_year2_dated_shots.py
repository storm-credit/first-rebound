"""Read pinned official gamebooks and build a bounded expected shot witness.

Keeps the original minute/credit model as ancestry. No integer boxes, causal
ratings, game results, learning efficacy or full possession clock are certified.
"""
import argparse
import csv
from datetime import date
import hashlib
import io
import json
import re
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = 'research/raw/EARLY_REWARD_B_YEAR2_PRIMARY_BOXES_2026_10_11.csv'
SOURCES = 'research/raw/EARLY_REWARD_B_YEAR2_PRIMARY_SOURCES_2026_10_11.json'
ALLOCATION = 'simulation/EARLY_REWARD_B_YEAR2_DATED_SHOTS_2026_10_11.csv'
MODEL = 'simulation/EARLY_REWARD_B_YEAR2_DATED_SHOTS_2026_10_11.json'
PARENT = 'simulation/EARLY_REWARD_B_YEAR2_CREDIT_BUDGET_2026_10_11.json'
LEDGER = 'simulation/CHICAGO_2019_20_PLAYER_GAME_MINUTE_LEDGER.csv'
DONORS = 'simulation/CHICAGO_2019_20_PLAYER_GAME_DONOR_VECTOR.csv'
ROSTER = 'simulation/CHICAGO_2019_20_ROSTER_BASELINE.csv'
STAT = ['fgm', 'fga', 'three_pm', 'three_pa', 'ftm', 'fta', 'orb', 'drb',
        'reb', 'ast', 'pf', 'stl', 'tov', 'blk', 'plus_minus', 'pts']
WEIGHTS = {'Zach LaVine': F(2, 5), 'Coby White': F(1, 5),
           'Lauri Markkanen': F(1, 5), 'Thaddeus Young': F(1, 10),
           'Tomas Satoransky': F(1, 10)}


def read(p):
    return (ROOT / p).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def sha(p):
    return hashlib.sha256(read(p).encode()).hexdigest()


def csvrows(p):
    return list(csv.DictReader(io.StringIO(read(p))))


def csvbytes(rows):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode()


def jsonbytes(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()


def rounded(x):
    return round(float(x), 9)


def parse_book(rec, cache):
    raw = (cache / Path(rec['cache_path']).name).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == rec['sha256_raw_bytes'], rec['url']
    doc = fitz.open(stream=raw, filetype='pdf')
    assert len(doc) == 1
    text = doc[0].get_text(sort=True)
    day = date.fromisoformat(rec['date'])
    assert f'{day.strftime("%B")} {day.day}, {day.year}' in text, rec['date']
    headers = list(re.finditer(r'(?m)^\s*(VISITOR|HOME):\s*(.+)$', text))
    head = next(h for h in headers if 'CHICAGO BULLS' in h.group(2).upper())
    index = headers.index(head)
    assert (headers[index][1] == 'VISITOR') == (' @ ' in rec['matchup'])
    end = headers[index + 1].start() if index + 1 < len(headers) else text.index('SCORE BY PERIOD')
    players, total = [], None
    for line in text[head.end():end].splitlines():
        row = re.match(r'^\s*\d+\s+(.+?)\s+(?:[FCG]\s+)?(\d{1,2}:\d{2})\s+((?:-?\d+\s+){15}-?\d+)\s*$', line)
        if row:
            seconds = sum(int(v) * f for v, f in zip(row[2].split(':'), [60, 1]))
            players.append({'player': row[1].strip(), 'seconds': seconds,
                            'starter': int(bool(re.search(r'\s[FCG]\s+\d{1,2}:\d{2}', line))),
                            **dict(zip(STAT, map(int, row[3].split())))})
        team = re.match(r'^\s*(\d{3}:\d{2})\s+((?:-?\d+\s+){15}-?\d+)\s*$', line)
        if team:
            total = dict(zip(STAT, map(int, team[2].split())))
            total['seconds'] = sum(int(v) * f for v, f in zip(team[1].split(':'), [60, 1]))
    assert players and total, rec['date']
    assert sum(p['seconds'] for p in players) == total['seconds']
    assert len({p['player'] for p in players}) == len(players)
    assert sum(p['starter'] for p in players) == 5
    for key in STAT:
        if key != 'plus_minus':
            assert sum(p[key] for p in players) == total[key], (rec['date'], key)
    for p in players:
        assert p['fgm'] >= p['three_pm'] and p['fga'] >= p['three_pa']
        assert 2 * p['fgm'] + p['three_pm'] + p['ftm'] == p['pts']
    return players, total


def allocate(values, target, active):
    """Take/give category opportunities to active players, using bounded waterfill.

    Core shares are preferences, not five donors presumed present every date.
    On exhaustion use only other present players with positive category capacity.
    """
    result = dict(values)
    adjustment = sum(values.values()) - target
    fallback = []
    if adjustment < 0:
        eligible = [p for p in active if p in WEIGHTS and values[p] > 0]
        if not eligible:
            eligible = [p for p in active if values[p] > 0]
            fallback = list(eligible)
        if not eligible:
            raise ValueError('No active positive category recipient')
        weight = {p: WEIGHTS.get(p, F(1)) for p in eligible}
        for p in eligible:
            result[p] += -adjustment * weight[p] / sum(weight.values())
    else:
        remaining = adjustment
        for core_only in [True, False]:
            while remaining > 0:
                eligible = [p for p in active if result[p] > 0 and (p in WEIGHTS if core_only else True)]
                if not eligible:
                    break
                weight = {p: WEIGHTS.get(p, F(1)) for p in eligible}
                debit = {p: min(result[p], remaining * weight[p] / sum(weight.values())) for p in eligible}
                for p, value in debit.items():
                    result[p] -= value
                    if not core_only and p not in WEIGHTS and value:
                        fallback.append(p)
                remaining -= sum(debit.values())
            if remaining == 0:
                break
        assert remaining == 0, 'P demand exceeds active team category budget'
    assert sum(result.values()) == target and all(v >= 0 for v in result.values())
    return result, sorted(set(fallback))


def build(cache):
    retrieval = json.loads((cache / 'retrieval.json').read_text(encoding='utf-8-sig'))
    games = csvrows(LEDGER)
    donors = {(x['event_id'], x['player']): x for x in csvrows(DONORS)}
    parent = json.loads(read(PARENT))
    assert len(games) == len(retrieval) == 65
    assert {x['event_id'] for x in games} == {x['event_id'] for x in retrieval}
    by_event = {x['event_id']: x for x in retrieval}
    assert len(by_event) == 65
    primary_rows, allocation_rows, summaries, precision = [], [], [], []
    p_rate = F(12 * 65 * 36, 1395)
    ts, three_pa, three_p, fta, ft = F('0.560'), F(3), F('0.320'), F(5), F('0.720')
    fga = p_rate / (2 * ts) - F('0.44') * fta
    two_pa = fga - three_pa
    two_pm = (p_rate - 3 * three_pa * three_p - fta * ft) / 2
    coactor_points = defaultdict(F)
    original_points = defaultdict(F)
    for game in games:
        event = game['event_id']
        rec = by_event[event]
        assert rec['game_id'] == game['game_id'] and rec['date'] == game['date']
        players, total = parse_book(rec, cache)
        for p in players:
            primary_rows.append({'event_id': event, 'game_id': game['game_id'],
                                 'date': game['date'], **p})
        active, ratios, old_pts = [], {}, {}
        for p in players:
            donor = donors.get((event, p['player']))
            if donor:
                ratio = F(donor['alternate_seconds']) / F(donor['actual_seconds'])
                if int(donor['actual_seconds']) != p['seconds']:
                    precision.append({'event_id': event, 'player': p['player'],
                                      'legacy_seconds': int(donor['actual_seconds']),
                                      'official_book_seconds': p['seconds']})
            else:
                ratio = F(1)
            ratios[p['player']] = ratio
            old_pts[p['player']] = p['pts'] * ratio
            if ratio > 0:
                active.append(p['player'])
        pm = F(game['protagonist_seconds']) / 2160
        p_budget = {'two_pa': two_pa * pm, 'three_pa': three_pa * pm,
                    'fta': fta * pm, 'tov': F(2) * pm}
        allocations, fallback = {}, {}
        for key in p_budget:
            values = {p['player']: (p['fga'] - p['three_pa'] if key == 'two_pa' else p[key]) * ratios[p['player']] for p in players}
            target = F(total['fga'] - total['three_pa'] if key == 'two_pa' else total[key]) - p_budget[key]
            assert target >= 0
            allocations[key], fallback[key] = allocate(values, target, active)
        for p in players:
            name = p['player']
            a = {k: allocations[k][name] for k in p_budget}
            two_pct = F(p['fgm'] - p['three_pm'], p['fga'] - p['three_pa']) if p['fga'] > p['three_pa'] else F(0)
            three_pct = F(p['three_pm'], p['three_pa']) if p['three_pa'] else F(0)
            ft_pct = F(p['ftm'], p['fta']) if p['fta'] else F(0)
            exp_pts = 2 * a['two_pa'] * two_pct + 3 * a['three_pa'] * three_pct + a['fta'] * ft_pct
            assert ratios[name] > 0 or sum(a.values()) == 0
            row = {'event_id': event, 'date': game['date'], 'player': name,
                   'historical_seconds': p['seconds'], 'legacy_retention_ratio': rounded(ratios[name]),
                   'expected_two_pa': rounded(a['two_pa']), 'expected_three_pa': rounded(a['three_pa']),
                   'expected_fga': rounded(a['two_pa'] + a['three_pa']),
                   'expected_fta': rounded(a['fta']), 'expected_tov': rounded(a['tov']),
                   'expected_two_pm': rounded(a['two_pa'] * two_pct),
                   'expected_three_pm': rounded(a['three_pa'] * three_pct),
                   'expected_ftm': rounded(a['fta'] * ft_pct), 'expected_pts': rounded(exp_pts),
                   'minute_scaled_before_expected_pts': rounded(old_pts[name]),
                   'actual_box_or_causal_effect': False}
            allocation_rows.append(row)
            coactor_points[name] += exp_pts
            original_points[name] += old_pts[name]
        p_pts = p_rate * pm
        allocation_rows.append({'event_id': event, 'date': game['date'], 'player': 'Protagonist',
            'historical_seconds': 0, 'legacy_retention_ratio': '',
            'expected_two_pa': rounded(p_budget['two_pa']), 'expected_three_pa': rounded(p_budget['three_pa']),
            'expected_fga': rounded(fga * pm), 'expected_fta': rounded(fta * pm),
            'expected_tov': rounded(F(2) * pm), 'expected_two_pm': rounded(two_pm * pm),
            'expected_three_pm': rounded(three_pa * three_p * pm), 'expected_ftm': rounded(fta * ft * pm),
            'expected_pts': rounded(p_pts), 'minute_scaled_before_expected_pts': rounded(F(12) * pm),
            'actual_box_or_causal_effect': False})
        summaries.append({'event_id': event, 'date': game['date'],
            'observed_team_FGA': total['fga'], 'observed_team_3PA': total['three_pa'],
            'observed_team_FTA': total['fta'], 'observed_player_TOV_sum': total['tov'],
            'four_categories_exactly_conserved': True, 'fallback_category_donors': fallback,
            'official_team_seconds': total['seconds'], 'legacy_team_seconds': int(game['actual_team_seconds']),
            'historical_team_pts': total['pts'],
            'new_expected_team_pts': rounded(sum(F(str(x['expected_pts'])) for x in allocation_rows if x['event_id'] == event)),
            'winner_or_score_selected': False})
    roster = csvrows(ROSTER)
    for p in roster:
        assert sum(x['pts'] for x in primary_rows if x['player'] == p['player']) == int(p['pts'])
        assert sum(x['starter'] for x in primary_rows if x['player'] == p['player']) == int(p['gs'])
    sources = {'id': 'EARLY_REWARD_B_YEAR2_PRIMARY_SOURCES_2026_10_11',
        'scope': '65 NBA official final boxes, Chicago positive-minute rows only; DNP/inactive injury narratives not transferred to fiction',
        'retrieved_date_local': '2026-10-11', 'primary_rows': len(primary_rows),
        'sources': [{k: x[k] for k in ['event_id', 'game_id', 'date', 'matchup', 'url', 'sha256_raw_bytes', 'bytes']} for x in retrieval],
        'visual_pages_checked': ['2019-10-23', '2019-12-08', '2020-03-10'],
        'other_pages_method': 'Column extraction with per-player scoring equation/all-stat team sums and exact printed team-minute sums checked on each complete page',
        'observed_season_totals': {k: sum(x[k] for x in primary_rows) for k in ['fga', 'three_pa', 'fta', 'tov', 'pts']}}
    model = {'id': 'EARLY_REWARD_B_YEAR2_DATED_SHOTS_2026_10_11',
        'status': 'WORKING_65_DATE_SHOT_AND_PLAYER_TOV_BUDGET_WITNESS_CAUSAL_JOIN_PENDING',
        'source_sha256': {p: sha(p) for p in [PARENT, LEDGER, DONORS, ROSTER]},
        'parent_credit_model': {'path': PARENT, 'LF_SHA256': sha(PARENT),
            'scope_correction': 'PR539 season315/fixed five debits is an initial credit proposal. This witness supersedes those fixed debits for shot ownership: actual active players and category constraints change expected scoring shares. No silent claim of preserving315 or unchanged team PTS.'},
        'authority': 'Implementation of selected B direction, same12PPG P working vector and existing minutes; no author-locked exact stat/result/award.',
        'data_vintage': 'Ex-post historical game boxes are counterfactual allocation references, not advance knowledge or measured future efficiency. Historical same-game conversion fractions are explicit fictional retention assumptions.',
        'precision_policy': '27 old donor second differences are recorded. Use legacy alternate/actual retention ratio for shots rather than subtracting a legacy second count from a different primary clock. This does not certify full lineup/elapsed-clock compatibility.',
        'legacy_donor_second_differences': precision,
        'P_expected_season_pts': 780, 'P_Games': 65, 'P_GS': 18, 'P_minutes': 1395,
        'coactor_scoring_changes': [{'player': name, 'minute_scaled_before_expected_pts': rounded(original_points[name]),
            'dated_shot_expected_pts': rounded(coactor_points[name]),
            'expected_pts_change': rounded(coactor_points[name] - original_points[name])} for name in sorted(coactor_points)],
        'dates': summaries,
        'verified_scope': ['65 raw PDF hashes/complete final pages', '691 historical positive-minute rows',
            '17 players historical seasonPTS match old roster', 'no DNP recipient or negative category budget',
            'FGA/3PA/FTA/playerTOV sums conserve each observed team budget as expected fractional counts'],
        'not_verified': ['integer event boxes', 'historical field-goal percentages remaining causal under new shot context',
            'ORB/DRB/assists/foul-event and team-turnover possession joins', 'five-player concurrent clock and opportunity ownership',
            'new causal rating/result/draft keeper join', 'MIP or other award', 'whole B years1/3/4 implementation'],
        'gates': {'freeze': 'v0.30 PARTIAL', 'design': 'CLOSED', 'manuscript_allowed': False, 'actual_Pack': 0},
        'tools': 'Codex HTTP primary retrieval/PDF extraction/root checks; no AGY/NLM/Claude/independent agent execution'}
    return {PRIMARY: csvbytes(primary_rows), SOURCES: jsonbytes(sources),
            ALLOCATION: csvbytes(allocation_rows), MODEL: jsonbytes(model)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache-dir', type=Path, default=ROOT / 'Temp/early_reward_b_year2_gamebooks')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    outputs = build(args.cache_dir)
    if args.check:
        for path, content in outputs.items():
            assert (ROOT / path).read_bytes().replace(b'\r\n', b'\n') == content, path
        print('PASS65 primary boxes/691 rows/756 expected allocations; dated category budgets; causal/clock joins pending')
    else:
        assert all(not (ROOT / p).exists() for p in outputs), 'Refusing to overwrite existing outputs'
        for path, content in outputs.items():
            (ROOT / path).parent.mkdir(parents=True, exist_ok=True)
            (ROOT / path).write_bytes(content)
        print('WROTE4 primary/dataset/model files')
