"""Conditional box priors and reason-linked minute witnesses; never a season runner."""
import argparse
from collections import Counter, defaultdict
import copy
import csv
import hashlib
import io
import json
from pathlib import Path

import build_chicago_2021_22_inputs as prior

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'simulation'
CONFIG = S / 'CHICAGO_2021_22_GROWTH_INPUTS.json'
SOURCE = ROOT / 'research/CHICAGO_2021_22_GROWTH_SOURCES.json'
OBS = S / 'NBA_2020_21_ROOKIE_COMPARISON_OBSERVATIONS.csv'
META = S / 'CHICAGO_2021_22_GROWTH_PROVENANCE.json'
BOOK = S / 'CHICAGO_2021_22_GROWTH_CANDIDATES.json'
QUEUE = S / 'CHICAGO_2021_22_PRIORITY_REASONS.csv'
REPORT = S / 'CHICAGO_2021_22_GROWTH_REVIEW.json'
KEYS = ('pts', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf')
load = prior.load
read_csv = prior.read_csv
sha = prior.sha
json_text = prior.json_text
csv_text = prior.csv_text


def ingest(folder):
    source, mirror = load(SOURCE), load(prior.SOURCE)
    names = set(source['comparison_players'])
    rows = []
    for name, expected in mirror['full_file_sha256'].items():
        path = folder / name
        assert sha(path) == expected, 'Pinned source changed'
        with path.open() as stream:
            for r in csv.DictReader(stream):
                if r['season_year'] == '2020-21' and r['personName'] in names:
                    rows.append(dict(season=r['season_year'], date=r['game_date'],
                        game_id=r['gameId'].zfill(10), team=r['teamTricode'], player=r['personName'],
                        seconds=prior.seconds(r['minutes']), comment=r['comment'],
                        **{k: int(float(r[v] or 0)) for k, v in prior.STATS.items()}))
    rows.sort(key=lambda r: (r['date'], r['game_id'], r['player']))
    OBS.write_text(csv_text(rows))
    META.write_text(json_text(dict(source_commit=mirror['source_commit'],
        full_file_sha256=mirror['full_file_sha256'], observation_sha256=sha(OBS),
        source_sha256=sha(SOURCE), observation_rows=len(rows),
        scope='PINNED_MIRROR_COMPARISONS_NOT_PRIMARY_BOX_OR_FITTED_MODEL')))


def check_shooting(r):
    for made, attempted in [('fgm', 'fga'), ('fg3m', 'fg3a'), ('ftm', 'fta')]:
        assert 0 <= r[made] <= r[attempted] + 1e-8
    assert 0 <= r['fgm'] - r['fg3m'] <= r['fga'] - r['fg3a'] + 1e-8
    assert abs(r['pts'] - (2 * r['fgm'] + r['fg3m'] + r['ftm'])) < 1e-7


def enrich_shooting(r):
    check_shooting(r)
    return dict(r, ts_proxy=r['pts'] / (2 * (r['fga'] + .44 * r['fta'])),
                shot_ending_proxy=r['fga'] + .44 * r['fta'] + r['tov'])


def produce_candidates(config, source, comparison_rows):
    """No 2021–22 observation, health-report or outcome input can enter this function."""
    cutoff = config['opening_information_cutoff']
    c = source['college']
    assert c['season'] == '2020-21' and c['last_game_date'] <= cutoff
    college = {k: v * 36 / c['minutes'] for k, v in c['totals'].items()}
    check_shooting(college)
    comparisons = []
    assert {r['player'] for r in comparison_rows} == set(source['comparison_players'])
    assert len({(r['game_id'], r['team'], r['player']) for r in comparison_rows}) == len(comparison_rows)
    for r in comparison_rows:
        assert r['season'] == '2020-21' and '2020-12-22' <= r['date'] <= '2021-05-16' <= cutoff
        check_shooting({k: int(r[k]) for k in prior.STATS})
    for player in source['comparison_players']:
        rows = [r for r in comparison_rows if r['player'] == player]
        secs = sum(int(r['seconds']) for r in rows)
        totals = {k: sum(int(r[k]) for r in rows) for k in prior.STATS}
        comparisons.append(dict(player=player, games=sum(int(r['seconds']) > 0 for r in rows),
            minutes=secs / 60, first_date=min(r['date'] for r in rows), last_date=max(r['date'] for r in rows),
            totals=totals, per36={k: v * 2160 / secs for k, v in totals.items()} if secs else None,
            scope='CONVENIENCE_COMPARISON_NOT_TRANSLATION_FIT'))
    old = next(r for r in read_csv(S / 'CHICAGO_2020_21_PREDEADLINE_PRODUCTION_PRIORS.csv')
               if r['player'] == 'Protagonist' and r['scenario'] == config['protagonist_prior_scenario'])
    old_rates = {k: float(old[k + '36']) for k in KEYS}
    old_ending = old_rates['pts'] / (2 * float(old['ts'])) + old_rates['tov']
    candidates = []
    for spec in config['protagonist_candidates']:
        r = {k: spec[k + '36'] for k in KEYS}
        r.update(fta=spec['fta36'], ftm=spec['fta36'] * spec['ftp'],
                 fg3a=spec['fg3a36'], fg3m=spec['fg3a36'] * spec['fg3p'])
        r['fga'] = r['pts'] / (2 * spec['ts']) - .44 * r['fta']
        r['fgm'] = (r['pts'] - r['fg3m'] - r['ftm']) / 2
        r = enrich_shooting(r)
        candidates.append(dict(id=spec['id'], player='Protagonist', minutes=32, per36=r,
            role_expected={k: v * 32 / 36 for k, v in r.items() if k != 'ts_proxy'},
            delta_vs_same_32_minutes={k: (r[k] - old_rates[k]) * 32 / 36 for k in KEYS},
            additional_shot_ending_proxy_at_32=(r['shot_ending_proxy'] - old_ending) * 32 / 36,
            status='CREATIVE_ASSUMPTION_NOT_OBSERVED', usage_rate=None))
    for spec in config['duarte_candidates']:
        r = {k: college[k] * spec[k + '_scale'] for k in KEYS if k != 'pts'}
        fg2a = (college['fga'] - college['fg3a']) * spec['fg2a_scale']
        r.update(fg3a=college['fg3a'] * spec['fg3a_scale'], fta=college['fta'] * spec['fta_scale'])
        r['fg3m'] = r['fg3a'] * spec['fg3p']
        r['ftm'] = r['fta'] * spec['ftp']
        r['fga'] = fg2a + r['fg3a']
        r['fgm'] = fg2a * spec['fg2p'] + r['fg3m']
        r['pts'] = 2 * r['fgm'] + r['fg3m'] + r['ftm']
        r = enrich_shooting(r)
        candidates.append(dict(id=spec['id'], player='Chris Duarte', minutes=14, per36=r,
            role_expected={k: v * 14 / 36 for k, v in r.items() if k != 'ts_proxy'},
            status='HAND_SET_COLLEGE_TRANSLATION_NOT_NBA_OBSERVATION', usage_rate=None))
    pairs = []
    for p in candidates[:4]:
        for d in candidates[4:]:
            pairs.append(dict(ids=[p['id'], d['id']], role_minutes=46,
                box_attribution={k: p['role_expected'][k] + d['role_expected'][k] for k in KEYS},
                team_score_delta=None, lineup_efficiency=None))
    return dict(stage='O-15G13', opening_information_cutoff=cutoff,
        prior_protagonist=old_rates, prior_protagonist_source='CHICAGO_2020_21_PREDEADLINE_PRODUCTION_PRIORS.csv',
        prior_scope='BASE_CANDIDATE_CARRIED_FORWARD_BY_POSTDEADLINE_RUNNER_NOT_SELECTED_SEASON_AVERAGE',
        college_per36=college, comparisons=comparisons, candidates=candidates, pairs=pairs,
        recommended_pair=config['recommended_pair'], selected_pair=config['selected_pair'],
        guardrails=config['guardrails'])


def certify(witness, unavailable, role):
    totals = Counter()
    by_position = {p: Counter() for p in role['position_eligibility_design_only']}
    assert sum(w['minutes'] for w in witness) == 48
    for w in witness:
        players = list(w['positions'].values())
        assert set(w['positions']) == set(by_position)
        assert len(set(players)) == 5 and not set(players) & set(unavailable)
        assert {'LaMelo_pick4', 'LaVine', 'Coby'} & set(players), 'No designated creator'
        for pos, player in w['positions'].items():
            assert player in role['position_eligibility_design_only'][pos]
            totals[player] += w['minutes']
            by_position[pos][player] += w['minutes']
    assert sum(totals.values()) == 240 and max(totals.values()) <= role['player_minute_ceiling_design_only']
    assert by_position['C']['Young'] <= 24
    return dict(total_minutes=240, player_minutes=dict(sorted(totals.items())), position_minutes=by_position)


def replacement_case(case_id, substitutions, role, additional_unavailable=()):
    """Split saved G11 witness into 2-minute units; consume explicit donor-slot quotas."""
    normal = next(c for c in role['cases'] if c['id'] == 'R21A')
    remaining = copy.deepcopy(substitutions)
    unavailable = sorted({donor for _, donor in substitutions} | set(additional_unavailable))
    pieces = []
    # These are unordered certificates. Allocate the guard-light Caruso-PG
    # group first so scarce Coby SG quota preserves a designated creator.
    ordered = sorted(normal['lineup_witness'], key=lambda w: w['positions']['PG'] != 'Caruso')
    for old in ordered:
        assert old['minutes'] % 2 == 0
        for _ in range(old['minutes'] // 2):
            positions = dict(old['positions'])
            for pos, donor in old['positions'].items():
                choices = remaining.get((pos, donor))
                if choices is None:
                    continue
                available = [p for p, n in choices.items() if n >= 2 and p not in positions.values()]
                assert available, 'Replacement slot conflict'
                chosen = available[0]
                choices[chosen] -= 2
                positions[pos] = chosen
            pieces.append(dict(minutes=2, positions=positions))
    assert all(n == 0 for choices in remaining.values() for n in choices.values())
    compact = {}
    for w in pieces:
        key = tuple(w['positions'].items())
        compact[key] = compact.get(key, 0) + w['minutes']
    witness = [dict(minutes=n, positions=dict(key)) for key, n in compact.items()]
    cert = certify(witness, unavailable, role)
    base = certify(normal['lineup_witness'], [], role)['player_minutes']
    delta = {p: cert['player_minutes'].get(p, 0) - base.get(p, 0) for p in role['roster']}
    return dict(id=case_id, unavailable=unavailable, witness=witness, certificate=cert,
        delta={p: n for p, n in delta.items() if n},
        required_available=list(cert['player_minutes']),
        scope='ALL_LISTED_RECIPIENTS_AVAILABLE_AND_REGISTERED_UNORDERED_WITNESS_NOT_ACTUAL_ROTATION')


def reason_queue(source, g12):
    rows = read_csv(prior.AVAIL)
    indexed = {(r['date'], r['source_player']): r for r in rows}
    primary = {}
    for report in g12['official_reports'] + source['reports']:
        for entry in report['entries']:
            key = (entry['date'], entry['player'])
            assert key in indexed and key not in primary
            assert report['report_date'] <= entry['date']
            primary[key] = dict(entry, report_id=report['id'], report_date=report['report_date'],
                report_time_et=report['report_time_et'], url=report['url'])
    selected = []
    for row in rows:
        key = (row['date'], row['source_player'])
        p = primary.get(key)
        coby_window = row['player'] == 'Coby' and row['date'] < '2021-11-15'
        if not p and row['evidence'] != 'OBSERVED_HEALTH_RESTRICTION' and not coby_window:
            continue
        if p:
            action = 'REVIEW_ASSIGNMENT_CONTRACT' if p['reason_category'] == 'G_LEAGUE_TWO_WAY' else 'REVIEW_CAUSE_AND_GAME_DATE'
        elif coby_window:
            action = 'SHOULDER_CONTEXT_NOT_DAILY_MEDICAL_PROOF'
        else:
            action = 'EXACT_REASON_UNRESOLVED'
        selected.append(dict(date=row['date'], game_id=row['game_id'], player=row['player'],
            normal_role_minutes=int(row['normal_role_minutes']), evidence=row['evidence'],
            source_comment=row['source_comment'], historical_team=p['team'] if p else row['source_team'],
            report_id=p['report_id'] if p else '', report_date=p['report_date'] if p else '',
            report_game_date=p['date'] if p else '', historical_status=p['status'] if p else '',
            reason=p['reason_category'] if p else '', url=p['url'] if p else '',
            page_1_based=p['page_1_based'] if p else '', action=action,
            alternate_available='HOLD', alternate_minutes='HOLD'))
    return selected


def build():
    config, source, meta = load(CONFIG), load(SOURCE), load(META)
    assert sha(SOURCE) == meta['source_sha256'] and sha(OBS) == meta['observation_sha256']
    book = produce_candidates(config, source, read_csv(OBS))
    assert len(book['candidates']) == 8 and len(book['pairs']) == 16
    assert book['selected_pair'] is None and not any(config['guardrails'][k] for k in
        ('author_locked', 'season_selected', 'exact_execution_cleared', 'manuscript_allowed'))
    role = load(prior.ROLE)
    cases = [
        replacement_case('DUARTE_OUT_14', {('SF', 'Chris Duarte'): {'Green': 8, 'Stanley Johnson': 6}}, role),
        replacement_case('CARUSO_OUT_22', {('PG', 'Caruso'): {'Satoransky': 6},
            ('SG', 'Caruso'): {'Denzel Valentine': 6}, ('SF', 'Caruso'): {'Green': 10}}, role),
        replacement_case('LAVINE_CARUSO_DUARTE_OUT_70', {
            ('SG', 'LaVine'): {'Coby': 12, 'Denzel Valentine': 22},
            ('PG', 'Caruso'): {'Satoransky': 6}, ('SG', 'Caruso'): {'Coby': 6},
            ('SF', 'Caruso'): {'Green': 10},
            ('SF', 'Chris Duarte'): {'Green': 6, 'Stanley Johnson': 8}}, role),
        replacement_case('LAVINE_CARUSO_GREEN_OUT_56', {
            ('SG', 'LaVine'): {'Coby': 12, 'Denzel Valentine': 22},
            ('PG', 'Caruso'): {'Satoransky': 6}, ('SG', 'Caruso'): {'Coby': 6},
            ('SF', 'Caruso'): {'Stanley Johnson': 10}}, role, additional_unavailable=['Green'])]
    rates = {p['player']: p['historical_prior']['per36'] for p in load(prior.PRIORS)['players']
             if p['historical_prior'] is not None}
    rates.update({c['player']: c['per36'] for c in book['candidates'] if c['id'] in config['recommended_pair']})
    for case in cases:
        assert all(p in rates for p in case['delta'])
        case['linear_box_attribution_delta'] = {
            k: sum(rates[p][k] * minutes / 36 for p, minutes in case['delta'].items()) for k in KEYS}
        case['production_scope'] = 'G12_HISTORICAL_NBA_RATES_PLUS_G13_RECOMMENDED_CANDIDATES_NOT_TEAM_SCORE_OR_DEFENSE'
        case['team_score_delta'] = None
    queue = reason_queue(source, load(prior.SOURCE))
    negative = []
    for c, absent in [(cases[2], ['LaVine', 'Caruso', 'Chris Duarte', 'Green']),
                       (cases[0], ['Chris Duarte', 'Green'])]:
        try:
            certify(c['witness'], absent, role)
        except AssertionError:
            negative.append(dict(case=c['id'], additional_unavailable='Green', result='REJECTED'))
        else:
            raise AssertionError('Unavailable recipient accepted')
    feb = {r['player']: r for r in queue if r['date'] == '2022-02-16'}
    assert all(feb[p]['historical_status'] == 'Out' for p in ('LaVine', 'Caruso', 'Chris Duarte'))
    assert feb['Green']['historical_status'] == 'Probable'
    report = dict(stage='O-15G13', candidates=8, pairs=16, comparison_players=len(book['comparisons']),
        comparison_observation_rows=meta['observation_rows'], priority_rows=len(queue),
        primary_reason_rows=sum(bool(r['report_id']) for r in queue),
        unresolved_generic_rows=sum(r['action'] == 'EXACT_REASON_UNRESOLVED' for r in queue),
        replacement_cases=cases, negative_recipient_checks=negative,
        date_connections=[
            dict(date='2021-11-15', case='DUARTE_OUT_14', historical_status='Questionable',
                 result='IF_OUT_AND_RECIPIENTS_AVAILABLE_ONLY_NOT_FINAL_HISTORICAL_OUT'),
            dict(date='2022-01-23', case='LAVINE_CARUSO_GREEN_OUT_56',
                 result='CONDITIONAL_DUARTE_RETAINED_STANLEY_SF10_NOT_GREEN'),
            dict(date='2022-02-16', case='LAVINE_CARUSO_DUARTE_OUT_70',
                 result='CONDITIONAL_GREEN_PROBABLE_IS_NOT_MEDICAL_CLEARANCE')],
        actual_game_minutes_selected=0, team_score_delta=None, season_wins=None,
        independent_review='NOT_INDEPENDENT', guardrails=config['guardrails'],
        input_sha256={str(p.relative_to(ROOT)): sha(p) for p in
            (CONFIG, SOURCE, OBS, META, prior.AVAIL, prior.ROLE, prior.PRIORS,
             S / 'CHICAGO_2020_21_PREDEADLINE_PRODUCTION_PRIORS.csv')})
    return {BOOK: json_text(book), QUEUE: csv_text(queue), REPORT: json_text(report)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    assert not (args.source_dir and args.check), 'Ingest and read-only check are separate'
    if args.source_dir:
        ingest(args.source_dir)
    for path, content in build().items():
        if args.check:
            assert path.read_text() == content, 'Stale output: ' + path.name
        else:
            path.write_text(content)
    print('PASS: 8 production candidates / 16 pairs / 4 conditional witnesses; season not selected')


if __name__ == '__main__':
    main()
