"""O-15F9: fixed-minute impact crosscheck and predeadline connection screen.

Default verifies saved evidence/output without solving lineups. --write rebuilds.
Ingest: --bpm-source archived players.csv --nba-sources three 2020-21 subsets.
"""
import argparse
import csv
import hashlib
import json
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path

import build_chicago_2020_21_paired_impact as paired

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'simulation'
P = 'CHICAGO_2020_21_'
BPM = S / (P + 'BPM_MAR25_SNAPSHOT.csv')
PRE = S / (P + 'PREDEADLINE_PAIRED_OBSERVATIONS.csv')
META = S / (P + 'O15F9_PROVENANCE.json')
OUT = S / (P + 'IMPACT_CROSSCHECK.json')
QUEUE = S / (P + 'PREDEADLINE_OPPONENT_SCREEN.csv')
DONORS = S / (P + 'PREDEADLINE_DONOR_VECTOR.csv')
ROLES = S / (P + 'PREDEADLINE_MINUTE_LEDGER.csv')
MARGINS = S / (P + 'PREDEADLINE_GAME_MARGIN_BASELINE.csv')
OLD_RATINGS = S / (P + 'PREDEADLINE_PLAYER_IMPACT_INPUTS.csv')
ARCHIVE = 'https://github.com/sdl60660/nba_player_movement/blob/78b30434bacbee4ffb2361b817969a5530c08dd3/data_processing/data/players.csv'
NBA_MIRROR = 'https://github.com/NocturneBear/NBA-Data-2010-2024/blob/a5f108b5b1f08074d78b9e8e901926a9ce4c06c5/'
METHODS = ('RAPTOR_RS_EB', 'BPM_MAR25_RAW', 'BPM_MAR25_EB')
SCENARIOS = ('LOW', 'BASE', 'HIGH')
FATIGUE = (0, 0.5, 1)

# These paths were already open before this audit. This screen is not a new draft board.
CONTACT = {
    'GSW': ([], ['Chandler Hutchison'], 'simulation/2018_DRAFT_28_43_EVANS_CASCADE.md', 'Wiggins 핵심 거래·Hutchison 가용성 조건'),
    'WAS': (['Isaac Bonga'], ['Gary Trent Jr.'], 'simulation/2021_WASHINGTON_CHICAGO_PORTLAND_TRANSACTION_CASCADE.md', 'Trent 유입·Bonga stash 후보의3년차 분 재계산'),
    'POR': (['Gary Trent Jr.'], ['Jacob Evans'], 'simulation/2018_DRAFT_28_43_EVANS_CASCADE.md', 'Trent 부재·Evans/기존 윙 분 재배분'),
    'LAL': ([], [], 'simulation/2018_DRAFT_37_60_TRENT_CASCADE.md', '2019 AD 연쇄 유지 조건; 2021 실제 접촉 분 자동 동일 판정 금지'),
    'CHA': (['LaMelo Ball', 'Grant Riller'], ['Anthony Edwards', 'Tyrell Terry'], 'simulation/2020_DRAFT_TYRELL_TERRY_RELANDING_BOARD.md', 'Edwards/Terry와 기존 가드/윙 분 재배분'),
    'MIN': (['Anthony Edwards'], ['Fictional Rival'], 'design/RIVAL_2020_WEST_TEAM_DECISION_PACKET.md', '라이벌 분·실력·Towns/Russell 공동 창출 비용'),
    'DET': (['Killian Hayes', 'Saddiq Bey'], ['Patrick Williams', 'Kira Lewis Jr.'], 'simulation/2020_DRAFT_ISAIAH_STEWART_RELANDING_BOARD.md', 'Patrick/Kira 분; Stewart 유지'),
    'DEN': (['R.J. Hampton'], ['Saddiq Bey'], 'simulation/2020_DRAFT_ZEKE_NNAJI_RELANDING_BOARD.md', 'Bey22/Nnaji24/Hampton Dallas31; Hampton0분도 Bey0분 증거 아님'),
    'DAL': (['Tyrell Terry'], ['R.J. Hampton'], 'simulation/2020_DRAFT_RJ_HAMPTON_RELANDING_BOARD.md', 'Hampton 분을 Terry의 실제 분에 고정하지 않음'),
    'NOP': (['Kira Lewis Jr.'], ['Killian Hayes'], 'simulation/2020_DRAFT_KIRA_LEWIS_RELANDING_BOARD.md', 'Hayes/Kira 이동; 실제 타팀 부상 일정 복사 금지'),
}


def read(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rows[0], lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seconds(r):
    return sum(int(x) * 60**i for i, x in enumerate(reversed(r['minutes'].split(':')))) if r['minutes'] else 0


def identity(name):
    s = ''.join(c for c in unicodedata.normalize('NFD', name) if not unicodedata.combining(c)).lower()
    for suffix in (' jr.', ' iii', ' ii', ' iv', ' sr.'):
        s = s.removesuffix(suffix)
    for char in ('.', "'", '-', ' '):
        s = s.replace(char, '')
    return {'nicolasclaxton': 'nicclaxton', 'juanhernangomez': 'juanchohernangomez',
            'wesleyiwundu': 'wesiwundu', 'eneskanter': 'enesfreedom',
            'sviatoslavmykhailiuk': 'svimykhailiuk'}.get(s, s)


def ingest(bpm_path, nba_paths):
    raw = [r for path in nba_paths for r in read(path) if r['season_year'] == '2020-21']
    assert len(raw) == 28859 and len({r['gameId'] for r in raw}) == 1080
    assert len(raw) == len({(r['gameId'], r['teamTricode'], r['personId']) for r in raw})
    observed = defaultdict(list)
    for r in raw:
        if r['game_date'] <= '2021-03-25' and r['minutes']:
            observed[identity(r['personName'])].append(r)
    snapshot = []
    for r in read(bpm_path):
        if not r.get('2021_bpm'):
            continue
        rows = observed[identity(r['player'])]
        names = {x['personName'] for x in rows}
        assert len(names) == 1
        total = sum(seconds(x) for x in rows)
        assert int(r['2021_g']) == len(rows), r['player']
        assert abs(int(r['2021_mp']) - total / 60) <= 1, r['player']
        snapshot.append({'player_id': r['player_id'], 'archive_player': r['player'], 'nba_player': rows[0]['personName'],
                         'season': 2021, 'observed_through': '2021-03-25', 'bpm': r['2021_bpm'],
                         'obpm': r['2021_obpm'], 'dbpm': r['2021_dbpm'], 'archive_gp': r['2021_g'],
                         'archive_minutes': r['2021_mp'], 'nba_gp_including_zero_clock': len(rows),
                         'nba_seconds': total, 'nba_last_date': max(x['game_date'] for x in rows),
                         'zero_clock_appearances': sum(seconds(x) == 0 for x in rows)})
    assert len(snapshot) == len(observed) == 505
    write_csv(BPM, sorted(snapshot, key=lambda r: r['player_id']))
    games = {r['game_id']: r for r in read(MARGINS)}
    pre = []
    for r in raw:
        gid = r['gameId'].zfill(10)
        if gid in games:
            pre.append({'event_id': games[gid]['event_id'], 'game_id': gid, 'date': r['game_date'], 'team': r['teamTricode'],
                        'player': r['personName'], 'seconds': seconds(r), 'start': int(bool(r['position'])),
                        'pts': int(float(r['points'] or 0)), 'plus_minus': int(float(r['plusMinusPoints'] or 0)),
                        'comment': r['comment']})
    write_csv(PRE, sorted(pre, key=lambda r: (r['date'], r['team'], r['player'])))
    # Check the re-downloaded source against the existing paired postdeadline evidence.
    keyed = {(r['gameId'].zfill(10), r['teamTricode'], r['personName']): r for r in raw}
    for r in read(paired.SNAP):
        x = keyed[(r['game_id'], r['team'], r['player'])]
        assert seconds(x) == int(r['seconds']) and int(float(x['points'] or 0)) == int(r['pts'])
    meta = {'stage': 'O-15F9', 'bpm_origin': 'https://www.basketball-reference.com/leagues/NBA_2021_advanced.html',
            'bpm_direct_access': '403; archived data used, not fresh primary-site verification',
            'archive_url': ARCHIVE, 'archive_sha256': sha(bpm_path),
            'nba_source_urls': [NBA_MIRROR + f'regular_season_box_scores_2010_2024_part_{i}.csv' for i in (1, 2, 3)],
            'nba_filtered_source_sha256': [sha(path) for path in nba_paths],
            'bpm_snapshot_sha256': sha(BPM), 'pre_observations_sha256': sha(PRE),
            'date_inference': 'All 505 player GP and cumulative minutes match NBA observations through 2021-03-25 within one integer minute; BPM itself is archived, not recomputed',
            'zero_clock_note': 'Tacko Fall 2021-02-23: minutes=0:00 with nonempty clock; included as appearance, never an added minute',
            'prior_cutoff_2021_03_24': 'unchanged; this snapshot is one day later and cannot be called predeadline information'}
    META.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n')


def pre_screen():
    groups = defaultdict(list)
    for r in read(PRE):
        groups[r['game_id']].append(r)
    result = []
    for g in read(MARGINS):
        rows = [r for r in groups[g['game_id']] if r['team'] != 'CHI']
        team = rows[0]['team']
        removed, added, ref, reason = CONTACT.get(team, ([], [], 'simulation/CHICAGO_2020_21_PREDEADLINE_OUTCOME_ROBUSTNESS.md', '검토 범위 내 새 직접 변경 미특정; 리그 무영향 아님'))
        result.append({'event_id': g['event_id'], 'game_id': g['game_id'], 'date': g['date'], 'opponent': team,
                       'status': 'OPPONENT_DELTA_UNALLOCATED' if team in CONTACT else 'LIMITED_BASELINE_CANDIDATE',
                       'removed_actual_players': ';'.join(removed), 'added_or_changed_players': ';'.join(added),
                       'removed_actual_seconds': sum(int(r['seconds']) for r in rows if r['player'] in removed),
                       'reason': reason, 'canon_evidence': ref, 'outcome_status': 'NOT_SELECTED'})
    return result


def rating_maps():
    bpm = {r['nba_player']: float(r['bpm']) for r in read(BPM)}
    eb = {r['nba_player']: float(r['bpm']) * int(r['archive_minutes']) / (int(r['archive_minutes']) + 1000) for r in read(BPM)}
    raptor = {r['source_player']: r['eb_1000'] for r in paired.rating_inputs().values()}
    return {k: {paired.norm(p): v for p, v in rs.items()} for k, rs in zip(METHODS, (raptor, bpm, eb))}


def envelopes(maps):
    bpm_names = [r['nba_player'] for r in read(BPM) if int(r['archive_minutes']) >= 120]
    raptor_names = [r['source_player'] for r in paired.rating_inputs().values() if r['minutes'] >= 120]
    result = {}
    for method in METHODS:
        values = [maps[method][paired.norm(p)] for p in (raptor_names if method == METHODS[0] else bpm_names)]
        result[method] = {'low': min(values), 'high': max(values), 'observed_players': len(values),
                          'status': 'EMPIRICAL_LEAGUE_RANGE_STRESS_NOT_PLAYER_PRIOR_OR_HARD_BOUND'}
    return result


def form(delta, rating, virtual):
    known = 0.0
    terms = {}
    for player, sec in sorted(delta.items()):
        if abs(sec) < 1e-7:
            continue
        if player in virtual:
            known += sec * virtual[player] / 2880
        elif paired.norm(player) in rating:
            known += sec * rating[paired.norm(player)] / 2880
        else:
            terms[player] = sec / 2880
    return known, terms


def band(constant, terms, envelope):
    lo = hi = constant
    for coefficient in terms.values():
        ends = [coefficient * envelope['low'], coefficient * envelope['high']]
        lo += min(ends)
        hi += max(ends)
    return [round(lo, 8), round(hi, 8)]


def build():
    previous = json.loads(paired.OUT.read_text())
    maps = rating_maps()
    env = envelopes(maps)
    priors = {(r['proxy'], r['scenario']): r for r in read(paired.PRIORS)}
    groups = paired.actuals()
    all_dates = sorted({r['date'] for r in read(MARGINS)} | {b['date'] for b in previous['opponent_branches']})
    b2b = {d: i > 0 and (date.fromisoformat(d) - date.fromisoformat(all_dates[i - 1])).days == 1 for i, d in enumerate(all_dates)}
    chi = {}
    for g in json.loads(paired.CHI.read_text())['games']:
        base = {r['player']: int(r['seconds']) for r in groups[(g['date'], 'CHI')]}
        fix = g['clock_correction']
        if fix['player']:
            base[fix['player']] += fix['seconds']
        alt = g['minimum_change_candidate']['player_seconds']
        delta = {p: alt.get(p, 0) - base.get(p, 0) for p in set(base) | set(alt)}
        assert abs(sum(delta.values())) < 1e-5
        chi[(g['date'], g['scenario'])] = delta
    post = []
    for b in previous['opponent_branches']:
        margin = sum(int(r['pts']) for r in groups[(b['date'], 'CHI')]) - sum(int(r['pts']) for r in groups[(b['date'], b['opponent'])])
        for availability in ('PORTER_ZERO', 'PORTER_CAPPED'):
            delta = chi[(b['date'], availability)]
            for method in METHODS:
                for scenario in SCENARIOS:
                    prior = priors[('RAPTOR_EB' if method == METHODS[0] else 'BPM', scenario)]
                    c, unknown_chi = form(delta, maps[method], {'Protagonist': float(prior['protagonist_rating']), 'LaMelo Ball': float(prior['lamelo_rating'])})
                    assert not unknown_chi, unknown_chi
                    o, terms = form(b['delta_seconds'], maps[method], {})
                    terms = {p: -v for p, v in terms.items()}
                    intercept = margin + c - o
                    fatigue = [(-penalty * (delta['Protagonist'] + delta['LaMelo Ball']) / 2880 if b2b[b['date']] else 0) for penalty in FATIGUE]
                    post.append({'date': b['date'], 'opponent': b['opponent'], 'branch': b['branch'], 'availability': availability,
                                 'method': method, 'prior': scenario, 'actual_margin': margin, 'chi_impact': round(c, 8),
                                 'opponent_constant': round(o, 8), 'margin_constant': round(intercept, 8),
                                 'unknown_rating_coefficients': {p: round(v, 8) for p, v in terms.items()},
                                 'fatigue_deltas': [round(f, 8) for f in fatigue],
                                 'margin_envelopes': [band(intercept + f, terms, env[method]) for f in fatigue],
                                 'opponent_margin_constant': round(-intercept, 8)})
    screen = pre_screen()
    screens = {r['event_id']: r for r in screen}
    roles = {r['event_id']: r for r in read(ROLES)}
    donors = defaultdict(dict)
    for r in read(DONORS):
        donors[r['event_id']][r['player']] = int(r['delta_seconds'])
    pre = []
    for g in read(MARGINS):
        role = roles[g['event_id']]
        delta = donors[g['event_id']] | {'Protagonist': int(role['protagonist_seconds']), 'LaMelo Ball': int(role['lamelo_seconds'])}
        assert sum(delta.values()) == 0
        assert int(g['b2b_second_night']) == b2b[g['date']]
        for method in METHODS:
            for scenario in SCENARIOS:
                prior = priors[('RAPTOR_EB' if method == METHODS[0] else 'BPM', scenario)]
                impact, terms = form(delta, maps[method], {'Protagonist': float(prior['protagonist_rating']), 'LaMelo Ball': float(prior['lamelo_rating'])})
                assert not terms
                margins = [float(g['actual_margin']) + impact - (penalty * (delta['Protagonist'] + delta['LaMelo Ball']) / 2880 if b2b[g['date']] else 0) for penalty in FATIGUE]
                pre.append({'event_id': g['event_id'], 'date': g['date'], 'opponent': screens[g['event_id']]['opponent'],
                            'method': method, 'prior': scenario, 'actual_margin': int(g['actual_margin']),
                            'opponent_held_margin': [round(x, 8) for x in margins],
                            'opponent_delta_coefficient': -1,
                            'connection_status': screens[g['event_id']]['status']})
    summary = []
    for method in METHODS:
        for availability in ('PORTER_ZERO', 'PORTER_CAPPED'):
            for scenario in SCENARIOS:
                rows = [r for r in post if (r['method'], r['availability'], r['prior']) == (method, availability, scenario)]
                pre_rows = [r for r in pre if (r['method'], r['prior']) == (method, scenario)]
                for index, penalty in enumerate(FATIGUE):
                    bydate = defaultdict(list)
                    for r in rows:
                        bydate[r['date']].append(r)
                    low_wins = high_wins = 0
                    uncertain = []
                    for d, rs in bydate.items():
                        lo = min(r['margin_envelopes'][index][0] for r in rs)
                        hi = max(r['margin_envelopes'][index][1] for r in rs)
                        low_wins += lo > 0
                        high_wins += hi > 0
                        if lo <= 0 <= hi:
                            uncertain.append(d)
                    pre_wins = sum(r['opponent_held_margin'][index] > 0 for r in pre_rows)
                    summary.append({'method': method, 'availability': availability, 'prior': scenario, 'fatigue': penalty,
                                    'post_conditional_win_envelope': [low_wins, high_wins], 'post_sensitive_dates': uncertain,
                                    'pre_opponent_held_wins': pre_wins,
                                    'season_arithmetic_only': [pre_wins + low_wins, pre_wins + high_wins],
                                    'season_status': 'NOT_CONNECTED_OPPONENT_PATHS_AND_AVAILABILITY_OPEN'})
    scope = []
    for r in read(OLD_RATINGS):
        p = r['player']
        old = float(r['raptor_total']) * float(r['raptor_minutes']) / (float(r['raptor_minutes']) + 1000)
        scope.append({'player': p, 'old_raptor_eb': old, 'new_all_team_raptor_eb': maps[METHODS[0]][paired.norm(p)],
                      'old_fullseason_bpm': float(r['bpm']), 'new_mar25_bpm': maps[METHODS[1]][paired.norm(p)]})
    paths = (BPM, PRE, META, paired.OUT, paired.CHI, paired.PRIORS, paired.RAPTOR, DONORS, ROLES, MARGINS, OLD_RATINGS, Path(__file__))
    return {'stage': 'O-15F9', 'status': 'TWO_FAMILY_CONDITIONAL_CROSSCHECK_SEASON_HOLD',
            'input_sha256': {p.name: sha(p) for p in paths}, 'families': {'RAPTOR': [METHODS[0]], 'BPM': list(METHODS[1:])},
            'statistical_independence': False, 'method_note': 'Two separately constructed measures, correlated basketball inputs; not two independent datasets or an independent human review',
            'snapshot_cutoff': '2021-03-25', 'fatigue_penalties': list(FATIGUE),
            'fatigue_scope': 'Existing predeadline two-player second-night stress carried to postdeadline; not observed fatigue or an opponent fatigue model',
            'post_b2b_dates': [d for d in all_dates[43:] if b2b[d]], 'normalization': 'Same 100 possessions per 48-minute normalization as O-15F8',
            'envelopes': env, 'scope_comparison': scope, 'post_inputs': post, 'pre_opponent_held_inputs': pre,
            'summary': summary, 'season_paths_selected': False, 'manuscript_allowed': False}


def verify(data):
    meta = json.loads(META.read_text())
    assert meta['bpm_snapshot_sha256'] == sha(BPM) and meta['pre_observations_sha256'] == sha(PRE)
    snapshot = read(BPM)
    assert len(snapshot) == len({r['player_id'] for r in snapshot}) == len({r['nba_player'] for r in snapshot}) == 505
    for r in snapshot:
        assert r['observed_through'] == '2021-03-25' and r['nba_last_date'] <= r['observed_through']
        assert r['archive_gp'] == r['nba_gp_including_zero_clock']
        assert abs(float(r['archive_minutes']) - int(r['nba_seconds']) / 60) <= 1
        assert abs(float(r['obpm']) + float(r['dbpm']) - float(r['bpm'])) <= 0.100001
    obs = read(PRE)
    assert len(obs) == len({(r['game_id'], r['team'], r['player']) for r in obs})
    assert sum(int(r['seconds']) for r in obs if r['team'] == 'CHI') == 625202
    for g in read(MARGINS):
        rows = [r for r in obs if r['game_id'] == g['game_id']]
        assert len({r['team'] for r in rows}) == 2
        points = {t: sum(int(r['pts']) for r in rows if r['team'] == t) for t in {r['team'] for r in rows}}
        other = next(t for t in points if t != 'CHI')
        assert points['CHI'] - points[other] == int(g['actual_margin'])
        for t in points:
            assert sum(int(r['start']) for r in rows if r['team'] == t) == 5
            assert sum(int(r['plus_minus']) for r in rows if r['team'] == t) == 5 * (points[t] - points[other if t == 'CHI' else 'CHI'])
    for r in read(DONORS):
        actual = next((x for x in obs if x['game_id'] == r['game_id'] and x['team'] == 'CHI' and x['player'] == r['player']), None)
        assert (int(actual['seconds']) if actual else 0) == int(r['actual_seconds'])
    assert read(QUEUE) == [{k: str(v) for k, v in r.items()} for r in pre_screen()]
    assert sum(r['status'] == 'OPPONENT_DELTA_UNALLOCATED' for r in pre_screen()) == 18
    for r in pre_screen():
        assert (ROOT / r['canon_evidence']).is_file()
    assert data == build()
    assert len(data['post_inputs']) == 702 and len(data['pre_opponent_held_inputs']) == 387
    previous = json.loads(paired.OUT.read_text())
    for old in previous['paired_inputs']:
        new = next(r for r in data['post_inputs'] if (r['date'], r['branch'], r['availability'], r['prior'], r['method']) == (old['date'], old['branch'], old['availability_scenario'], old['impact_scenario'], METHODS[0]))
        assert abs(old['margin_proxy_constant'] - new['margin_constant']) < 1e-6
        expected = {'Fictional Rival': old['paired_delta_coefficients']['rival_raptor_eb']} if old['paired_delta_coefficients'] else {}
        assert expected == new['unknown_rating_coefficients']
    for r in data['post_inputs']:
        assert abs(r['margin_constant'] + r['opponent_margin_constant']) < 1e-7
        assert r['fatigue_deltas'][0] == 0 and r['fatigue_deltas'][2] <= r['fatigue_deltas'][1] <= 0
        assert all(lo <= hi for lo, hi in r['margin_envelopes'])
    assert data['families'] == {'RAPTOR': [METHODS[0]], 'BPM': list(METHODS[1:])}
    print(f'PASS: BPM505; pre paired {len(obs)} rows/43 games; post702 x3 fatigue=2106; pre387 x3=1161; 18 opponent paths open; no season selected')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bpm-source', type=Path)
    parser.add_argument('--nba-sources', type=Path, nargs=3)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    if args.bpm_source or args.nba_sources:
        assert args.write and args.bpm_source and args.nba_sources
        ingest(args.bpm_source, args.nba_sources)
    if args.write:
        write_csv(QUEUE, pre_screen())
        data = build()
        verify(data)
        OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n')
    else:
        verify(json.loads(OUT.read_text()))
