"""O-15F14-D: 40 remaining close boundary games, conditional paired impact.
Minute policies precede ratings. Reuses existing lineup and conference tools.
"""
import argparse
import copy
import itertools
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
import build_chicago_2020_21_boundary_impact as bi
import build_chicago_2020_21_postseason_routes as ps

S = bi.S
OBS = S / 'NBA_2020_21_REMAINING_BOUNDARY_OBSERVATIONS.csv'
OUT = S / 'CHICAGO_2020_21_REMAINING_PAIRED_IMPACT.json'
PENDING = S / 'NBA_2020_21_AFTER_40_PENDING_QUEUE.csv'
RIVAL = bi.ip.RIVAL
ROLES = copy.deepcopy(bi.ROLES)
for t in ('DAL', 'MIN'):
    ROLES[t] = copy.deepcopy(bi.ip.ROLES[t])
ROLES['MIN']['handler'] += ['D\'Angelo Russell']
ROLES['MIN']['wing'] += ['Jake Layman', 'Jarred Vanderbilt', 'Juancho Hernangomez']
ROLES['DEN']['handler'] += ['Austin Rivers', 'Shaquille Harrison']
ROLES['DEN']['wing'] += ['Aaron Gordon', 'Austin Rivers', 'Shaquille Harrison']
ROLES['DEN']['center'] += ['JaVale McGee']
ROLES['POR'] = {
    'handler': ['Damian Lillard', 'CJ McCollum', 'Anfernee Simons'],
    'center': ['Enes Freedom', 'Jusuf Nurkic', 'Harry Giles III', 'Robert Covington'],
    'wing': ['Carmelo Anthony', 'Derrick Jones Jr.', 'Nassir Little', 'Rodney Hood',
             'Robert Covington', 'CJ Elleby', 'Rondae Hollis-Jefferson']}
ROLES['ORL'] = {
    'handler': ['Michael Carter-Williams', 'Chasson Randle', 'Karim Mane'],
    'center': ['Nikola Vucevic', 'Mo Bamba', 'Khem Birch'],
    'wing': ['Dwayne Bacon', 'James Ennis III', 'Chuma Okeke', 'Gary Harris',
             'Al-Farouq Aminu', 'Zeke Nnaji']}


def groups():
    result = defaultdict(list)
    for r in bi.cc.read(OBS):
        result[r['event_id'], r['team']].append(r)
    return result


def policy(team, day, high, rival_minutes=28):
    if team == 'DAL':
        return ['Tyrell Terry'], {'R.J. Hampton': 18 if high else 12}, [
            ('Trey Burke', 0), ('Nate Hinton', 0), ('Josh Green', 6), ('JJ Redick', 8),
            ('Tim Hardaway Jr.', 20), ('Josh Richardson', 22), ('Jalen Brunson', 22),
            ('Dorian Finney-Smith', 30), ('James Johnson', 16)], [('Josh Green', 24)], {}
    if team == 'MIN':
        return ['Anthony Edwards'], {RIVAL: rival_minutes}, [
            ('Jake Layman', 12), ('Juancho Hernangomez', 12), ('Josh Okogie', 20)], [
            ('Jaden McDaniels', 28), ('Josh Okogie', 30), ('Jake Layman', 28),
            ('Juancho Hernangomez', 28)], {'Anthony Edwards': RIVAL}
    if team == 'POR':
        # Existing INCUMBENTS condition: Evans inactive, Powell absent; Hood stays.
        # Hood's new-team availability after deadline is a stated assumption.
        targets = {'Rodney Hood': 16 if high else 12} if day >= '2021-03-25' else {}
        return ['Gary Trent Jr.', 'Norman Powell'], targets, [
            ('CJ Elleby', 0), ('Nassir Little', 8), ('Carmelo Anthony', 24),
            ('Derrick Jones Jr.', 16)], [
            ('Anfernee Simons', 32 if high else 30), ('Nassir Little', 28),
            ('Rodney Hood', 30), ('Derrick Jones Jr.', 36), ('Carmelo Anthony', 38),
            ('CJ Elleby', 12), ('Rondae Hollis-Jefferson', 28)], {}
    if team == 'ORL' and day >= '2021-03-25':
        # Same Vucevic-stays/Gordon-A branch as the CHI ledger; no invented Hall contract.
        return ['Wendell Carter Jr.', 'Otto Porter Jr.', 'R.J. Hampton'], {
            'Nikola Vucevic': 30, 'Zeke Nnaji': 12 if high else 8}, [
            ('Karim Mane', 0), ('Khem Birch', 12), ('Chasson Randle', 20)], [
            ('Chasson Randle', 30), ('Michael Carter-Williams', 24),
            ('Chuma Okeke', 34), ('Dwayne Bacon', 36), ('James Ennis III', 32)], {}
    if team == 'DEN' and day >= '2021-03-25':
        # Gordon A retains Gordon/Clark; Harris/Nnaji leave. Actual Rivers/McGee etc conditional.
        return ['R.J. Hampton', 'Zeke Nnaji', 'Gary Harris'], {'Saddiq Bey': 24 if high else 20}, [
            ('Vlatko Cancar', 0), ('Shaquille Harrison', 6), ('PJ Dozier', 16),
            ('Will Barton', 28), ('Michael Porter Jr.', 28), ('JaMychal Green', 12),
            ('Paul Millsap', 8)], [], {}
    return bi.policies(team, day, high)


def specs():
    result = []
    for (gid, team), rows in sorted(groups().items()):
        day = rows[0]['date']
        base, duration, clock = bi.baseline(rows)
        removed, targets, *_ = policy(team, day, False)
        changed = bool(targets or set(removed) & set(base))
        profiles = bi.PROFILES if changed else ('OBSERVED_HELD',)
        for profile, rival in itertools.product(profiles, (24, 28, 32) if team == 'MIN' else (None,)):
            removed, targets, donors, recipients, swaps = policy(team, day, profile == 'HIGH_MINUTES', rival)
            alt = {p: n for p, n in base.items() if p not in removed}
            alt.update({p: n * 60 for p, n in targets.items()})
            eligible = bi.allowed(rows) | set(targets)
            moves = []
            if changed:
                deficit = max(0, duration - sum(alt.get(p, 0) for p in ROLES[team]['center']))
                if deficit:
                    candidates = [p for p in ROLES[team]['center'] if p in eligible and p in alt]
                    p = max(candidates, key=lambda p: alt[p])
                    alt[p] += deficit
                    moves.append({'player': p, 'seconds': deficit, 'reason': 'CONDITIONAL_CENTER_COVERAGE_NOT_CLOCK_CORRECTION'})
            gap = 5 * duration - sum(alt.values())
            for p, limit in recipients if gap > 0 else donors:
                if p not in eligible or p in targets or p in removed:
                    continue
                old = alt.get(p, 0)
                delta = min(gap, max(0, limit * 60 - old)) if gap > 0 else -min(-gap, max(0, old - limit * 60))
                if delta:
                    alt[p] = old + delta
                    gap -= delta
                    moves.append({'player': p, 'seconds': delta, 'limit_minutes': limit})
                if gap == 0:
                    break
            assert gap == 0, (gid, team, profile, rival, gap)
            alt = {p: n for p, n in sorted(alt.items()) if n > 0}
            starters = [swaps.get(r['player'], r['player']) for r in rows if r['start'] == '1']
            # Replacement starter policies use roles/availability, never game score or ratings.
            if team == 'POR' and any(p in removed for p in starters):
                replacement = next(p for p in ['Anfernee Simons', 'Rodney Hood', 'Nassir Little', 'Derrick Jones Jr.']
                                   if alt.get(p, 0) >= 180 and p not in starters)
                starters = [replacement if p in removed else p for p in starters]
            if team == 'ORL' and changed:
                starters = ['Nikola Vucevic' if p == 'Khem Birch' else p for p in starters]
            if changed:
                # A required three-minute start with two center-role players needs
                # 48+3 center-role minutes, not just 48. Fund the overlap explicitly.
                centers = set(ROLES[team]['center'])
                overlap = 180 * max(0, len(set(starters) & centers) - 1)
                deficit = max(0, duration + overlap - sum(alt.get(p, 0) for p in centers))
                if deficit:
                    recipient = max((p for p in centers if p in alt), key=lambda p: alt[p])
                    donor = max((p for p in alt if p not in centers and p not in targets), key=lambda p: alt[p])
                    assert alt[donor] - deficit >= (180 if donor in starters else 0)
                    alt[recipient] += deficit
                    alt[donor] -= deficit
                    moves.append({'player': recipient, 'seconds': deficit, 'donor': donor,
                                  'reason': 'CONDITIONAL_STARTER_CENTER_OVERLAP_NOT_CLOCK_CORRECTION'})
                alt = dict(sorted(alt.items()))
            assert len(set(starters)) == 5 and set(starters) <= set(alt), (gid, starters)
            assert max(alt.values()) <= duration, (gid, team, alt)
            result.append({'event_id': gid, 'date': day, 'team': team, 'profile': profile,
                'rival_minutes': rival, 'changed': changed, 'game_duration_seconds': duration,
                'clock_correction': clock, 'actual_seconds': base, 'alternate_seconds': alt,
                'removed_players': removed, 'newcomers': sorted(targets), 'starters': sorted(starters),
                'balance_moves': moves,
                'delta_seconds': {p: alt.get(p, 0) - base.get(p, 0) for p in sorted(set(base) | set(alt)) if alt.get(p, 0) != base.get(p, 0)},
                'status': 'CONDITIONAL_MINUTES_NOT_AVAILABILITY_OR_TRANSACTION_APPROVAL'})
    return result


def verify_minutes(branches, witnesses):
    raw = groups()
    for b, witness in zip(branches, witnesses, strict=True):
        assert sum(b['delta_seconds'].values()) == 0
        assert sum(b['alternate_seconds'].values()) == 5 * b['game_duration_seconds']
        assert not set(b['removed_players']) & set(b['alternate_seconds'])
        eligible = bi.allowed(raw[b['event_id'], b['team']]) | set(b['newcomers'])
        assert all(p in eligible for p, n in b['delta_seconds'].items() if n > 0)
        if not b['changed']:
            assert witness is None and not b['delta_seconds']
            continue
        total = 0
        seen = defaultdict(float)
        start = 0
        for w in witness:
            assert len(w['players']) == 5 and bi.valid(w['players'], b['team'], ROLES)
            assert w['seconds'] > 0
            total += w['seconds']
            if sorted(w['players']) == b['starters']:
                start += w['seconds']
            for p in w['players']:
                seen[p] += w['seconds']
        assert abs(total - b['game_duration_seconds']) < 1e-5 and start >= 180 - 1e-5
        assert set(seen) == set(b['alternate_seconds'])
        assert all(abs(seen[p] - n) < 1e-5 for p, n in b['alternate_seconds'].items())


def paired_inputs(branches):
    actual = bi.lb.normalized_games()
    byid = {g['id']: g for g in actual}
    maps = bi.cc.rating_maps()
    env = bi.cc.envelopes(maps)
    # Link archive names by the common player ID, not by a guessed fuzzy match.
    alias = next(r for r in bi.cc.read(bi.cc.BPM) if r['player_id'] == 'kanteen01')
    assert alias['nba_player'] == 'Enes Freedom'
    source = next(r for r in bi.cc.read(bi.cc.paired.RAPTOR) if r['player_id'] == 'kanteen01')
    maps['RAPTOR_RS_EB'][bi.cc.paired.norm(alias['nba_player'])] = maps['RAPTOR_RS_EB'][bi.cc.paired.norm(source['player_name'])]
    schedule = defaultdict(list)
    for g in actual:
        for t in (g['home'], g['away']):
            schedule[t].append(g['date'])
    b2b = {(t, d): i > 0 and (date.fromisoformat(d) - date.fromisoformat(ds[i-1])).days == 1
           for t, days in schedule.items() for ds in [sorted(days)] for i, d in enumerate(ds)}
    raw = groups()
    lookup = defaultdict(list)
    for b in branches:
        lookup[b['event_id'], b['team']].append(b)
    inputs = []
    for gid in sorted({b['event_id'] for b in branches}):
        g = byid[gid]
        h, a, day = g['home'], g['away'], g['date']
        margin = sum(int(r['pts']) for r in raw[gid, h]) - sum(int(r['pts']) for r in raw[gid, a])
        assert abs(margin) == g['margin'] and (h if margin > 0 else a) == g['winner']
        for profile, rival in itertools.product(bi.PROFILES, (24, 28, 32) if 'MIN' in (h, a) else (None,)):
            def choose(t):
                found = [b for b in lookup[gid, t] if b['profile'] in (profile, 'OBSERVED_HELD') and b['rival_minutes'] in (None, rival)]
                assert len(found) == 1
                return found[0]
            hs, aws = choose(h), choose(a)
            assert hs['game_duration_seconds'] == aws['game_duration_seconds']
            for method, fatigue in itertools.product(bi.METHODS, (0, .5, 1)):
                home, hu = bi.cc.form(hs['delta_seconds'], maps[method], {})
                away, au = bi.cc.form(aws['delta_seconds'], maps[method], {})
                terms = {p: hu.get(p, 0) - au.get(p, 0) for p in set(hu) | set(au) if hu.get(p, 0) != au.get(p, 0)}
                assert set(terms) <= {RIVAL}, (gid, terms)
                hp = sum(max(0, n) for n in hs['delta_seconds'].values()) / 2880 if b2b[h, day] else 0
                ap = sum(max(0, n) for n in aws['delta_seconds'].values()) / 2880 if b2b[a, day] else 0
                constant = margin + home - away - fatigue * hp + fatigue * ap
                band = bi.cc.band(constant, terms, env[method])
                inputs.append({'event_id': gid, 'profile': profile, 'rival_minutes': rival,
                    'method': method, 'fatigue': fatigue, 'actual_home_margin': margin,
                    'home_margin_constant': round(constant, 8), 'away_margin_constant': round(-constant, 8),
                    'unknown_coefficients': terms, 'home_margin_band': band,
                    'conditional_sign': 'HOME' if band[0] > 0 else 'AWAY' if band[1] < 0 else 'UNRESOLVED',
                    'workload_coefficients': [hp, ap], 'selected': False})
    return inputs


def bridges(inputs):
    upstream = json.loads(bi.OUT.read_text())
    actual = bi.lb.normalized_games()
    result = []
    for ix, previous in enumerate(upstream['season_bridge']):
        c = previous['source_condition']
        profile, rival, _ = c['path_id'].split('/')
        rival = int(rival.split('_')[1])
        chosen = [r for r in inputs if (r['profile'], r['method'], r['fatigue']) == (profile, c['method'], c['fatigue']) and r['rival_minutes'] in (None, rival)]
        assert len(chosen) == 40
        lo, hi = c['rating_open_interval']
        cuts = sorted({-r['home_margin_constant']/r['unknown_coefficients'][RIVAL] for r in chosen if RIVAL in r['unknown_coefficients']})
        bounds = [lo, *[cut for cut in cuts if lo < cut < hi], hi]
        zero_boundaries = [{'rating': cut, 'event_ids': [r['event_id'] for r in chosen if r['unknown_coefficients'] and abs(r['home_margin_constant'] + r['unknown_coefficients'].get(RIVAL, 0) * cut) < 1e-7]} for cut in cuts if lo <= cut <= hi]
        lookup = {r['event_id']: r for r in chosen}
        for low, high in zip(bounds, bounds[1:]):
            rating = (low + high) / 2  # Sign partition only, not a chosen player prior.
            games = []
            changed = set(previous['changed_game_ids'])
            for g in actual:
                winner = bi.lb.changed_game(g)['winner'] if g['id'] in changed else g['winner']
                if g['id'] in lookup:
                    r = lookup[g['id']]
                    value = r['home_margin_constant'] + r['unknown_coefficients'].get(RIVAL, 0) * rating
                    assert abs(value) > 1e-8
                    winner = g['home'] if value > 0 else g['away']
                games.append({**g, 'winner': winner})
            wins = bi.lb.record_wins(games)
            assert sum(wins.values()) == 1080 and wins['CHI'] == previous['team_wins']['CHI']
            delta = {t: wins[t] - previous['team_wins'][t] for t in wins if wins[t] != previous['team_wins'][t]}
            assert sum(delta.values()) == 0
            try:
                seeds = ps.order(games)
                tie_hold = None
            except ValueError as e:
                seeds = None
                tie_hold = str(e)
            result.append({'source_condition_index': ix, 'source_condition': c,
                'shared_rival_rating_open_interval': [low, high], 'zero_boundaries_unresolved': zero_boundaries,
                'team_wins': dict(sorted(wins.items())), 'win_deltas_vs_B': delta,
                'seeds': seeds, 'later_tie_hold': tie_hold,
                'chicago_rank': seeds['EAST'].index('CHI') + 1 if seeds else None,
                'changed_game_ids': sorted(g['id'] for g in games if g['winner'] != next(x['winner'] for x in actual if x['id'] == g['id'])),
                'other_games_held': 939, 'selected': False})
    return result


def build(witnesses):
    branches = specs()
    verify_minutes(branches, witnesses)
    inputs = paired_inputs(branches)
    actual = {g['id']: g for g in bi.lb.normalized_games()}
    summaries = []
    for gid in sorted({r['event_id'] for r in inputs}):
        rows = [r for r in inputs if r['event_id'] == gid]
        g = actual[gid]
        actual_sign = 'HOME' if g['winner'] == g['home'] else 'AWAY'
        signs = {r['conditional_sign'] for r in rows}
        status = 'ALL_TESTED_RETAIN' if signs == {actual_sign} else 'ALL_TESTED_REVERSE' if signs == ({'HOME', 'AWAY'} - {actual_sign}) else 'MODEL_DISAGREEMENT_OR_UNRESOLVED'
        summaries.append({'event_id': gid, 'home': g['home'], 'away': g['away'],
            'actual_winner': g['winner'], 'status': status, 'selected': False,
            'both_observed_held': all(not b['changed'] for b in branches if b['event_id'] == gid),
            'method_bands': {m: [min(r['home_margin_band'][0] for r in rows if r['method'] == m), max(r['home_margin_band'][1] for r in rows if r['method'] == m)] for m in bi.METHODS}})
    bridge = bridges(inputs)
    grouped = defaultdict(list)
    for i, row in enumerate(bridge):
        grouped[tuple(row['changed_game_ids'])].append(i)
    cases = []
    for i, (changed, indices) in enumerate(sorted(grouped.items()), 1):
        row = bridge[indices[0]]
        case = {'id': f'D{i:02d}', 'bridge_indices': indices, 'changed_game_ids': list(changed),
                'team_wins': row['team_wins'], 'seeds': row['seeds'], 'selected': False}
        if row['seeds']:
            seeds, wins = row['seeds'], row['team_wins']
            east, west = ps.playin(seeds['EAST']), ps.playin(seeds['WEST'])
            case.update({'east_playin': east, 'west_playin': west})
            fields = {}
            for e, w in itertools.product(east, west):
                playoff = set(seeds['EAST'][:6] + seeds['WEST'][:6] + e['qualifiers'] + w['qualifiers'])
                lottery = ps.ALL - playoff
                assert len(lottery) == 14 and len(playoff) == 16
                fields[tuple(sorted(lottery))] = {'lottery_teams': sorted(lottery),
                    'lottery_record_groups': ps.record_groups(lottery, wins),
                    'playoff_record_groups': ps.record_groups(playoff, wins, 15), 'draw_selected': False}
            case['distinct_lottery_fields'] = list(fields.values())
            case['joint_playin_outcome_count'] = len(east) * len(west)
        cases.append(case)
    return {'stage': 'O-15F14-D', 'status': 'REMAINING_40_CONDITIONAL_IMPACT_COMPLETE_SEASON_HOLD',
        'branches': branches, 'lineup_witnesses': witnesses, 'paired_inputs': inputs,
        'game_summary': summaries, 'season_bridge': bridge, 'league_cases': cases,
        'roles': ROLES, 'manuscript_allowed': False, 'selected': False,
        'scope': 'CHI72 + prior29 + new40. Other939 actual-held, including240 larger-margin boundaries and699 other games; no final standings or probabilities.',
        'conditions': ['POR Evans inactive; incumbents cover Trent; no Powell trade; Hood retained and conditionally available after deadline',
            'DAL Hampton12/18 replaces Terry; incumbent deadline transactions retained conditionally',
            'ORL Vucevic30/Nnaji8or12, GordonA; Harris has no March28 appearance row; conditionally inactive, not a health finding; Aminu inactive; Fournier departure separate',
            'DEN GordonA; Nnaji absent; Bey20/24; Rivers/McGee incumbent transactions/availability conditionally retained',
            'MIN same effective rival rating and24/28/32 policy as each upstream Chicago source condition; no added synergy bonus',
            'GSW/LAL and other observed-held rows are conditional incumbent rosters, not no-impact proof',
            'Actual overtime duration retained as diagnostic exposure, not alternate overtime prediction',
            'Retrospective RAPTOR/BPM proxies and workload sensitivity; minute feasibility is not health approval'],
        'upstream_sha256': {p.name: bi.cc.sha(p) for p in (OBS, bi.OUT, ps.QUEUE, bi.cc.BPM, bi.cc.paired.RAPTOR, Path(bi.__file__), Path(ps.__file__), Path(__file__))}}


def pending(data):
    done = {g['event_id'] for g in data['game_summary']}
    return [{**r, 'boundary_screen_basis': 'O-15F14-C_OLD_FIVE_PATHS_NOT_RESCREENED',
             'impact_status': 'NOT_CALCULATED'} for r in bi.cc.read(ps.QUEUE) if r['id'] not in done]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    if args.write:
        data = build([bi.solve(b, ROLES) for b in specs()])
        OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        bi.cc.write_csv(PENDING, pending(data))
    else:
        data = json.loads(OUT.read_text())
        assert data == build(data['lineup_witnesses'])
        assert bi.cc.read(PENDING) == pending(data)
    print(json.dumps({'PASS': True, 'branches': len(data['branches']), 'changed': sum(b['changed'] for b in data['branches']),
        'inputs': len(data['paired_inputs']), 'games': dict(Counter(r['status'] for r in data['game_summary'])),
        'bridge': len(data['season_bridge']), 'ranks': sorted({r['chicago_rank'] for r in data['season_bridge'] if r['chicago_rank']})}))
