"""Three retrospective paired controls, not a forecast or season runner.

Saved lineup witnesses need only the standard library. Opponent witnesses were
found once with an integer solver; their order is not a substitution timeline.
"""
import argparse
from collections import Counter
import csv
import math
from pathlib import Path

import build_chicago_2021_22_inputs as prior
import build_chicago_2021_22_growth as growth

ROOT = prior.ROOT
S = prior.S
CONFIG = S / 'CHICAGO_2021_22_PAIRED_INPUTS.json'
SOURCE = ROOT / 'research/CHICAGO_2021_22_PAIRED_SOURCES.json'
OBS = S / 'NBA_2021_22_THREE_GAME_OBSERVATIONS.csv'
PREOBS = S / 'NBA_2020_21_OPPONENT_PRIOR_OBSERVATIONS.csv'
META = S / 'CHICAGO_2021_22_PAIRED_PROVENANCE.json'
PREBOOK = S / 'CHICAGO_2021_22_OPPONENT_PRIORS.json'
REPORT = S / 'CHICAGO_2021_22_PAIRED_REVIEW.json'
ALLOC = S / 'CHICAGO_2021_22_OPPORTUNITY_ALLOCATIONS.csv'
BUDGET_KEYS = ('fga', 'fta', 'tov')
load, sha, read_csv = prior.load, prior.sha, prior.read_csv


def ingest(folder):
    source, mirror = load(SOURCE), load(prior.SOURCE)
    ids = {g['game_id'] for g in source['games']}
    names = set(source['opponent_prior_players'])
    obs, pre = [], []
    for filename, expected in mirror['full_file_sha256'].items():
        path = folder / filename
        assert sha(path) == expected, 'Pinned mirror changed'
        with path.open() as stream:
            for r in csv.DictReader(stream):
                target = r['season_year'] == '2021-22' and r['gameId'].zfill(10) in ids
                previous = r['season_year'] == '2020-21' and r['personName'] in names
                if not (target or previous):
                    continue
                row = dict(season=r['season_year'], date=r['game_date'],
                    game_id=r['gameId'].zfill(10), team=r['teamTricode'], player=r['personName'],
                    person_id=r['personId'], seconds=prior.seconds(r['minutes']),
                    start=int(bool(r['position'])), comment=r['comment'],
                    **{k: int(float(r[v] or 0)) for k, v in prior.STATS.items()})
                (obs if target else pre).append(row)
    for path, rows in ((OBS, obs), (PREOBS, pre)):
        path.write_text(prior.csv_text(sorted(rows, key=lambda r: (r['date'], r['game_id'], r['team'], r['player']))))
    META.write_text(prior.json_text(dict(stage='O-15G14', source_commit=mirror['source_commit'],
        full_file_sha256=mirror['full_file_sha256'], source_sha256=sha(SOURCE),
        mirror_manifest_sha256=sha(prior.SOURCE), rows={OBS.name: len(obs), PREOBS.name: len(pre)},
        snapshot_sha256={p.name: sha(p) for p in (OBS, PREOBS)},
        source_scope='PINNED_PUBLIC_MIRROR_NOT_FRESH_PRIMARY_NUMERIC_BOX_CHECK')))


def validate_observations(rows, season):
    assert rows and len({(r['game_id'], r['team'], r['person_id']) for r in rows}) == len(rows)
    for r in rows:
        assert r['season'] == season
        assert int(r['seconds']) >= 0
        stats = {k: int(r[k]) for k in prior.STATS}
        assert all(v >= 0 for v in stats.values())
        growth.check_shooting(stats)
        assert stats['orb'] + stats['drb'] == stats['reb']


def opponent_priors(rows, names, cutoff):
    """Only the previous regular season enters the prior; target games never do."""
    validate_observations(rows, '2020-21')
    assert {r['player'] for r in rows} == set(names)
    assert all('2020-12-22' <= r['date'] <= '2021-05-16' < cutoff for r in rows), 'Prior date leakage'
    return {name: prior.prior_for(name, rows, cutoff) for name in names}


def rate_from_totals(p):
    # G12 display rates are rounded; use exact source totals for identities.
    assert p['source_season'] == '2020-21' and p['last_source_date'] <= '2021-05-16'
    return {k: v * 2160 / p['total_seconds'] for k, v in p['totals'].items()}


def certify(rotation):
    assert rotation['status'] == 'CONDITIONAL'
    totals = Counter()
    by_position = {s: Counter() for s in ('PG', 'SG', 'SF', 'PF', 'C')}
    for w in rotation['lineup_witness']:
        assert isinstance(w['minutes'], int) and w['minutes'] > 0
        ps = w['positions']
        assert set(ps) == set(by_position) and len(set(ps.values())) == 5, 'Duplicate player / missing position'
        assert not set(ps.values()) & set(rotation['unavailable']), 'Unavailable recipient'
        assert set(ps.values()) & set(rotation['required_creator_any_of']), 'Creator coverage'
        for pos, name in ps.items():
            assert name in rotation['eligibility'][pos], 'Position eligibility'
            totals[name] += w['minutes']
            by_position[pos][name] += w['minutes']
    assert sum(w['minutes'] for w in rotation['lineup_witness']) == 48
    assert sum(totals.values()) == 240 and max(totals.values()) <= rotation['minute_ceiling_design_only']
    assert by_position == rotation['position_minutes'], 'Position budget mismatch'
    assert all(sum(ns.values()) == 48 for ns in by_position.values())
    return dict(player_minutes=dict(sorted(totals.items())), position_minutes=by_position,
                total_minutes=240, witness_count=len(rotation['lineup_witness']))


def guard_deficit(rotation):
    assert rotation['status'] == 'ROLE_HOLD'
    guards = rotation['available_designated_primary_guards']
    assert len(guards) == len(set(guards)) and not set(guards) & set(rotation['unavailable'])
    return max(0, rotation['required_guard_minutes'] - len(guards) * rotation['minute_ceiling_design_only'])


def distribute(weights, budget, protected):
    """Keep protected raw values, proportionally allocate the nonnegative residual."""
    assert math.isfinite(budget) and budget >= 0
    assert all(math.isfinite(v) and v >= 0 for v in weights.values())
    fixed = set(protected) & set(weights)
    free = set(weights) - fixed
    residual = budget - sum(weights[p] for p in sorted(fixed))
    if residual < -1e-9:
        return None, 'PROTECTED_EXCEEDS_BUDGET'
    denominator = sum(weights[p] for p in sorted(free))
    if residual > 1e-9 and denominator <= 0:
        return None, 'NO_FREE_WEIGHT'
    result = {p: (w if p in fixed else max(0, residual) * w / denominator if denominator else 0)
              for p, w in weights.items()}
    assert all(v >= 0 for v in result.values())
    assert abs(sum(result.values()) - budget) < 1e-7
    return result, None


def allocate(rotation, cert, rates, budget, policy, ratio_bounds):
    minutes = cert['player_minutes']
    missing = sorted(p for p in minutes if p not in rates)
    if missing:
        return dict(status='PRIOR_HOLD', missing_prior=missing), []
    raw = {p: {k: rates[p][k] * n / 36 for k in BUDGET_KEYS} for p, n in minutes.items()}
    protection = dict(featured=rotation['featured'], core=rotation['core'], none=[],
                      noncore=sorted(set(minutes) - set(rotation['core'])))[policy['protect']]
    allocations = {}
    for k in BUDGET_KEYS:
        values, reason = distribute({p: r[k] for p, r in raw.items()}, budget[k], protection)
        if reason:
            return dict(status='BUDGET_HOLD', failed_measure=k, reason=reason), []
        allocations[k] = values
    rows = []
    for p, n in minutes.items():
        r = dict(game_id=rotation['game_id'], team=rotation['team'], rotation=rotation['id'],
                 policy=policy['id'], player=p, minutes=n, protected=int(p in protection))
        stress = []
        for k in BUDGET_KEYS:
            a, w = allocations[k][p], raw[p][k]
            r.update({f'raw_{k}': w, f'allocated_{k}': a, f'adjustment_{k}': a - w,
                      f'ratio_{k}': a / w if w else ''})
            if w and not ratio_bounds[0] <= a / w <= ratio_bounds[1]:
                stress.append(k)
        rate = rates[p]
        assert 0 <= rate['fg3a'] <= rate['fga']
        r['allocated_fg3a_fixed_prior_mix'] = r['allocated_fga'] * rate['fg3a'] / rate['fga'] if rate['fga'] else 0
        r['design_ratio_stress'] = '|'.join(stress)
        rows.append(r)
    return dict(status='CONDITIONAL_NUMERIC', raw_totals={k: sum(r[k] for r in raw.values()) for k in BUDGET_KEYS},
        budget=budget, allocated_totals={k: sum(allocations[k].values()) for k in BUDGET_KEYS},
        protected_players=sorted(set(protection) & set(minutes)),
        stress_player_count=sum(bool(r['design_ratio_stress']) for r in rows),
        adjustment_scope='VS_UNCONSTRAINED_PRIOR_WEIGHTS_NOT_CAUSAL_GROWTH_DONORS'), rows


def build():
    config, source, meta = load(CONFIG), load(SOURCE), load(META)
    assert meta['source_sha256'] == sha(SOURCE) and meta['mirror_manifest_sha256'] == sha(prior.SOURCE)
    for name, expected in meta['snapshot_sha256'].items():
        assert sha(S / name) == expected, 'Stale observations'
    assert not any(config['guardrails'][k] for k in ('author_locked', 'season_selected', 'exact_execution_cleared', 'manuscript_allowed'))
    assert all(config[k] is None for k in ('selected_production_pair', 'selected_budget_policy', 'selected_trade_policy'))
    assert {p['id'] for p in config['policies']} == {'B14A', 'B14B', 'B14C', 'B14D'}
    assert [(p['sabonis_package'], p['four_team_package']) for p in config['trade_conditions']] == [(False, False), (True, False), (False, True), (True, True)]
    observations, preobs = read_csv(OBS), read_csv(PREOBS)
    for path, rows in ((OBS, observations), (PREOBS, preobs)):
        assert len(rows) == meta['rows'][path.name]
    validate_observations(observations, '2021-22')
    assert {r['game_id'] for r in observations} == {g['game_id'] for g in source['games']}
    priors = opponent_priors(preobs, source['opponent_prior_players'], config['opening_information_cutoff'])
    assert all(priors.values())
    rates = {p['player']: rate_from_totals(p['historical_prior']) for p in load(prior.PRIORS)['players'] if p['historical_prior']}
    rates.update({p: rate_from_totals(r) for p, r in priors.items()})
    g13book = load(growth.BOOK)
    assert g13book['opening_information_cutoff'] == config['opening_information_cutoff']
    assert config['recommended_production_pair'] == g13book['recommended_pair']
    rates.update({p['player']: p['per36'] for p in g13book['candidates'] if p['id'] in config['recommended_production_pair']})
    for r in rates.values():
        growth.check_shooting(r)
    rotations = {r['id']: r for r in config['rotations']}
    assert len(rotations) == len(config['rotations']) == 6
    role = load(prior.ROLE)
    old_coby = load(prior.REPORT)['coby_absence_example']
    old_growth = {r['id']: r for r in load(growth.REPORT)['replacement_cases']}
    for r in rotations.values():
        if r['team'] == 'CHI':
            old = old_coby if r['source_case'] == old_coby['id'] else old_growth[r['source_case']]
            assert r['lineup_witness'] == old.get('lineup_witness', old.get('witness'))
            assert r['unavailable'] == old['unavailable'] and r['eligibility'] == role['position_eligibility_design_only']
    certificates = {r['id']: certify(r) for r in rotations.values() if r['status'] == 'CONDITIONAL'}
    orl = rotations['ORL_0022100701']
    assert guard_deficit(orl) == orl['conditional_missing_guard_minutes'] == 12
    historical, budgets = [], {}
    baseline = {r['game_id']: r for r in read_csv(prior.LEAGUE)}
    for g in source['games']:
        rows = [r for r in observations if r['game_id'] == g['game_id']]
        assert {r['date'] for r in rows} == {g['date']}
        assert {r['team'] for r in rows} == {g['home'], g['away']}
        old = baseline[g['game_id']]
        assert (old['date'], old['home'], old['away']) == (g['date'], g['home'], g['away'])
        for side in ('home', 'away'):
            team = g[side]
            team_rows = [r for r in rows if r['team'] == team]
            totals = {k: sum(int(r[k]) for r in team_rows) for k in prior.STATS}
            seconds = sum(int(r['seconds']) for r in team_rows)
            assert seconds == int(old[side + '_observed_seconds']) and abs(seconds - 14400) <= 5
            assert totals['pts'] == int(old[side + '_pts']) and int(old['inferred_historical_ot']) == 0
            budget = {k: totals[k] for k in BUDGET_KEYS}
            budgets[(g['game_id'], team)] = budget
            historical.append(dict(game_id=g['game_id'], date=g['date'], team=team,
                player_rows=len(team_rows), observed_seconds=seconds, seconds_residual=seconds - 14400,
                player_box_totals=totals, budget_scope='OBSERVED_PLAYER_SUM_CONTROL_NOT_OFFICIAL_TEAM_TURNOVERS_OR_POSSESSIONS'))
    team_policies, allocation_rows = [], []
    for r in config['rotations']:
        for policy in config['policies']:
            if r['status'] == 'ROLE_HOLD':
                result, rows = dict(status='ROLE_HOLD', missing_guard_minutes=guard_deficit(r)), []
            else:
                result, rows = allocate(r, certificates[r['id']], rates, budgets[(r['game_id'], r['team'])],
                                        policy, config['stress_ratio_design_only'])
            team_policies.append(dict(game_id=r['game_id'], team=r['team'], rotation=r['id'], policy=policy['id'], **result))
            allocation_rows.extend(rows)
    pairs = []
    for g in source['games']:
        for policy in config['policies']:
            matching = [r for r in team_policies if r['game_id'] == g['game_id'] and r['policy'] == policy['id']]
            assert len(matching) == 2 and {r['team'] for r in matching} == {g['home'], g['away']}
            pairs.append(dict(game_id=g['game_id'], policy=policy['id'],
                team_statuses={r['team']: r['status'] for r in matching},
                both_numeric=all(r['status'] == 'CONDITIONAL_NUMERIC' for r in matching),
                team_score=None, score_margin=None, winner=None))
    dependencies = (CONFIG, SOURCE, OBS, PREOBS, META, prior.LEAGUE, prior.PRIORS, prior.ROLE,
                    prior.REPORT, growth.BOOK, growth.REPORT)
    report = dict(stage='O-15G14', status='PARTIAL_PAIRED_CONTROL_NOT_SEASON_EXECUTION',
        observed_games=3, observation_rows=len(observations), opponent_prior_players=len(priors),
        opponent_prior_rows=len(preobs), fresh_primary_numeric_box_checks=0,
        historical=historical, certificates=certificates, orlando_guard_hold=orl,
        team_policy_counts=dict(Counter(r['status'] for r in team_policies)), team_policies=team_policies,
        pair_conditions=pairs, numeric_pair_conditions=sum(r['both_numeric'] for r in pairs),
        allocation_rows=len(allocation_rows), recommended_budget_policy=config['recommended_budget_policy'],
        selected_budget_policy=None, selected_trade_policy=None, actual_minutes_selected=0,
        projected_points=None, team_efficiency=None, season_wins=None,
        guardrails=config['guardrails'],
        input_sha256={str(p.relative_to(ROOT)): sha(p) for p in dependencies})
    prebook = dict(stage='O-15G14', cutoff=config['opening_information_cutoff'], priors=priors,
                   scope='HISTORICAL_NBA_PRIOR_NOT_ALTERNATE_PRODUCTION', selected=False)
    return {PREBOOK: prior.json_text(prebook), REPORT: prior.json_text(report), ALLOC: prior.csv_text(allocation_rows)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    assert not (args.source_dir and args.check)
    if args.source_dir:
        ingest(args.source_dir)
    for path, content in build().items():
        if args.check:
            assert path.read_text() == content, 'Stale output: ' + path.name
        else:
            path.write_text(content)
    print('PASS: 3 paired controls, 5 conditional minute witnesses; ORL role hold preserved')


if __name__ == '__main__':
    main()
