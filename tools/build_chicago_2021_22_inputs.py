"""Pin historical evidence and preseason priors without selecting alternate events.

--source-dir ingests the three previously pinned public mirror files. Default
rebuilds derived ledgers from the saved evidence. --check writes nothing.
"""
import argparse
from collections import Counter, defaultdict
import copy
from datetime import date
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'simulation'
SOURCE = ROOT / 'research/CHICAGO_2021_22_INPUT_SOURCES.json'
OBS = S / 'NBA_2021_22_ROLE_OBSERVATIONS.csv'
LEAGUE = S / 'NBA_2021_22_REGULAR_BASELINE.csv'
META = S / 'CHICAGO_2021_22_INPUT_PROVENANCE.json'
CALENDAR = S / 'CHICAGO_2021_22_CALENDAR.csv'
AVAIL = S / 'CHICAGO_2021_22_AVAILABILITY.csv'
PRIORS = S / 'CHICAGO_2021_22_PRESEASON_PRIORS.json'
REPORT = S / 'CHICAGO_2021_22_INPUT_REVIEW.json'
ROLE = S / 'CHICAGO_2021_22_ROLE_PLAN_INPUTS.json'
STATS = {'pts': 'points', 'fgm': 'fieldGoalsMade', 'fga': 'fieldGoalsAttempted',
         'fg3m': 'threePointersMade', 'fg3a': 'threePointersAttempted',
         'ftm': 'freeThrowsMade', 'fta': 'freeThrowsAttempted',
         'orb': 'reboundsOffensive', 'drb': 'reboundsDefensive', 'reb': 'reboundsTotal',
         'ast': 'assists', 'stl': 'steals', 'blk': 'blocks',
         'tov': 'turnovers', 'pf': 'foulsPersonal'}


def load(path):
    return json.loads(path.read_text())


def read_csv(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_text(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'


def csv_text(rows):
    f = io.StringIO(newline='')
    writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return f.getvalue()


def seconds(value):
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(value.split(':')))) if value else 0


def ingest(folder):
    config = load(SOURCE)
    selected_names = {n for n in config['roster_names'].values() if n}
    prior_names = selected_names | set(config['historical_chicago_comparison_names'])
    observations, games = [], defaultdict(list)
    row_counts = Counter()
    keys = set()
    for filename, expected in config['full_file_sha256'].items():
        path = folder / filename
        assert sha(path) == expected, 'Pinned mirror changed: ' + filename
        with path.open() as stream:
            for r in csv.DictReader(stream):
                season = r['season_year']
                if season not in (config['observed_season'], config['prior_season']):
                    continue
                row_counts[season] += 1
                key = (season, r['gameId'], r['teamTricode'], r['personId'])
                assert key not in keys, 'Duplicate player-game source'
                keys.add(key)
                if season == config['observed_season']:
                    games[r['gameId'].zfill(10)].append(r)
                include = (season == config['prior_season'] and r['personName'] in prior_names) or (
                    season == config['observed_season'] and (r['personName'] in selected_names or r['teamTricode'] == 'CHI'))
                if include:
                    observations.append(dict(season=season, date=r['game_date'], game_id=r['gameId'].zfill(10),
                        team=r['teamTricode'], player=r['personName'], person_id=r['personId'],
                        seconds=seconds(r['minutes']), start=int(bool(r['position'])), comment=r['comment'],
                        **{k: int(float(r[v] or 0)) for k, v in STATS.items()}))
    baseline = []
    for gid, rows in games.items():
        dates = {r['game_date'] for r in rows}
        assert len(dates) == 1
        teams = {r['teamTricode'] for r in rows}
        assert len(teams) == 2
        home = {r['teamTricode'] for r in rows if ' vs. ' in r['matchup']}
        assert len(home) == 1
        home = home.pop()
        away = (teams - {home}).pop()
        for r in rows:
            assert set(r['matchup'].replace('vs.', '@').split(' @ ')) == teams
        points = {t: sum(int(float(r['points'] or 0)) for r in rows if r['teamTricode'] == t) for t in teams}
        team_seconds = {t: sum(seconds(r['minutes']) for r in rows if r['teamTricode'] == t) for t in teams}
        # The source rounds individual displayed seconds. Preserve residuals;
        # inferred periods are a historical diagnostic, not alternate overtime.
        ot = round((sum(team_seconds.values()) / 2 - 14400) / 1500)
        expected = 14400 + 1500 * ot
        assert ot >= 0 and all(abs(v - expected) <= 5 for v in team_seconds.values())
        baseline.append(dict(game_id=gid, date=next(iter(dates)), home=home, away=away,
            home_pts=points[home], away_pts=points[away],
            home_observed_seconds=team_seconds[home], away_observed_seconds=team_seconds[away],
            inferred_historical_ot=ot, home_seconds_residual=team_seconds[home] - expected,
            away_seconds_residual=team_seconds[away] - expected,
            official_reference_url=f'https://www.nba.com/game/{away.lower()}-vs-{home.lower()}-{gid}'))
    assert row_counts == {'2020-21': 28859, '2021-22': 31321}
    assert len(baseline) == 1230
    OBS.write_text(csv_text(sorted(observations, key=lambda x: (x['season'], x['date'], x['game_id'], x['player']))))
    LEAGUE.write_text(csv_text(sorted(baseline, key=lambda x: (x['date'], x['game_id']))))
    meta = dict(stage='O-15G12', source_commit=config['source_commit'], full_file_sha256=config['full_file_sha256'],
        input_source_sha256=sha(SOURCE), complete_season_source_rows=dict(row_counts),
        observation_rows=len(observations), snapshot_sha256={OBS.name: sha(OBS), LEAGUE.name: sha(LEAGUE)},
        source_scope=config['source_scope'])
    META.write_text(json_text(meta))


def observation_status(row):
    if row is None:
        return 'NO_SAME_DAY_ROW'
    if int(row['seconds']) > 0:
        return 'OBSERVED_PLAYED'
    comment = row['comment'].lower()
    if "coach's decision" in comment:
        return 'OBSERVED_COACH_DNP'
    if any(x in comment for x in ('injury', 'illness', 'protocol')):
        return 'OBSERVED_HEALTH_RESTRICTION'
    return 'OBSERVED_OTHER_ZERO'


def prior_for(name, observations, cutoff):
    rows = [r for r in observations if r['player'] == name and r['season'] == '2020-21']
    if any(r['date'] >= cutoff for r in rows):
        raise ValueError('Preseason lookahead: ' + str(name))
    total_seconds = sum(int(r['seconds']) for r in rows)
    if not total_seconds:
        return None
    total = {k: sum(int(r[k]) for r in rows) for k in STATS}
    return dict(source_season='2020-21', first_source_date=min(r['date'] for r in rows),
        last_source_date=max(r['date'] for r in rows), games_played=sum(int(r['seconds']) > 0 for r in rows),
        starts=sum(int(r['start']) for r in rows), observed_teams=sorted({r['team'] for r in rows}),
        total_seconds=total_seconds, totals=total,
        per36={k: round(v * 2160 / total_seconds, 6) for k, v in total.items()},
        three_point_fraction=round(total['fg3m'] / total['fg3a'], 6) if total['fg3a'] else None,
        scope='HISTORICAL_OBSERVATION_PRIOR_NOT_ALTERNATE_PRODUCTION')


def build():
    config, meta, role = load(SOURCE), load(META), load(ROLE)
    assert meta['input_source_sha256'] == sha(SOURCE), 'STALE source definitions'
    for filename, expected in meta['snapshot_sha256'].items():
        assert sha(S / filename) == expected, 'STALE saved evidence ' + filename
    observations, league = read_csv(OBS), read_csv(LEAGUE)
    assert len(observations) == meta['observation_rows']
    assert len({(r['season'], r['game_id'], r['person_id']) for r in observations}) == len(observations)
    assert len(league) == len({r['game_id'] for r in league}) == 1230
    team_games = Counter(t for r in league for t in (r['home'], r['away']))
    assert len(team_games) == 30 and set(team_games.values()) == {82}
    by_id = {r['game_id']: r for r in league}
    for check in config['official_date_checks']:
        assert all(by_id[check['game_id']][k] == check[k] for k in ('date', 'home', 'away'))
    assert set(config['roster_names']) == set(role['roster'])
    current = [r for r in observations if r['season'] == config['observed_season']]
    byplayer = defaultdict(list)
    for row in current:
        byplayer[row['player']].append(row)
    historical = [r for r in league if 'CHI' in (r['home'], r['away'])]
    historical.sort(key=lambda r: (r['date'], r['game_id']))
    official = {(e['date'], e['player']): (report['id'], e) for report in config['official_reports'] for e in report['entries']}
    calendar, availability = [], []
    normal = next(c for c in role['cases'] if c['id'] == 'R21A')
    baseline_minutes = Counter()
    for v in normal['position_minutes'].values():
        baseline_minutes.update(v)
    for n, game in enumerate(historical):
        day = date.fromisoformat(game['date'])
        previous_gap = (day - date.fromisoformat(historical[n - 1]['date'])).days if n else None
        last5 = sum(0 <= (day - date.fromisoformat(g['date'])).days <= 4 for g in historical)
        calendar.append(dict(game_number=n + 1, **game, opponent=game['away'] if game['home'] == 'CHI' else game['home'],
            previous_game_gap_days='' if previous_gap is None else previous_gap,
            historical_back_to_back_second=int(previous_gap == 1), historical_games_last5_days=last5,
            alternate_date='HOLD', alternate_result='HOLD', role_policy_reference='R21A_CONDITIONAL',
            opponent_roster_status='REVIEW_REQUIRED_G7_G8_AND_PRIOR_CASCADE'))
        for alias in role['roster']:
            name = config['roster_names'][alias]
            rows = byplayer.get(name, [])
            same = [r for r in rows if r['date'] == game['date']]
            assert len(same) <= 1
            row = same[0] if same else None
            before = [r for r in rows if r['date'] < game['date'] and int(r['seconds']) > 0]
            after = [r for r in rows if r['date'] > game['date'] and int(r['seconds']) > 0]
            before = max(before, key=lambda r: r['date']) if before else None
            after = min(after, key=lambda r: r['date']) if after else None
            report_id, report_entry = official.get((game['date'], name), ('', {}))
            evidence = observation_status(row) if name else 'FICTIONAL_NO_OBSERVATION'
            priority = 'NO_AUTOMATIC_INFERENCE'
            if report_entry.get('status') in ('Out', 'Questionable') or evidence == 'OBSERVED_HEALTH_RESTRICTION':
                priority = 'REVIEW_LISTED_REASON'
            elif name and evidence == 'NO_SAME_DAY_ROW':
                priority = 'REVIEW_MISSING_OBSERVATION'
            availability.append(dict(game_id=game['game_id'], date=game['date'], player=alias, source_player=name or '',
                normal_role_minutes=baseline_minutes.get(alias, 0), evidence=evidence,
                source_game_id=row['game_id'] if row else '', source_team=row['team'] if row else '',
                source_seconds=row['seconds'] if row else '', source_comment=row['comment'] if row else '',
                previous_played_date=before['date'] if before else '', next_played_date=after['date'] if after else '',
                primary_report_id=report_id, primary_report_team=report_entry.get('team', ''),
                primary_status=report_entry.get('status', ''), primary_reason=report_entry.get('reason_category', ''),
                priority=priority, alternate_available='HOLD', alternate_minutes='HOLD'))
    priors = []
    for alias, name in config['roster_names'].items():
        prior = prior_for(name, observations, config['opening_information_cutoff']) if name else None
        status = 'HISTORICAL_NBA_PRIOR' if prior else ('FICTIONAL_GROWTH_INPUT_HOLD' if name is None else 'ROOKIE_TRANSLATION_HOLD')
        priors.append(dict(player=alias, source_player=name, kind='PROPOSED_ROSTER', normal_role_minutes=baseline_minutes.get(alias, 0),
            status=status, historical_prior=prior, alternate_2021_22_per36=None))
    for name in config['historical_chicago_comparison_names']:
        prior = prior_for(name, observations, config['opening_information_cutoff'])
        assert prior is not None, 'Missing historical comparator ' + name
        priors.append(dict(player=name, source_player=name, kind='HISTORICAL_CHI_COMPARATOR_NOT_ALTERNATE_ROSTER',
            normal_role_minutes=None, status='HISTORICAL_NBA_PRIOR', historical_prior=prior, alternate_2021_22_per36=None))
    player_summary = []
    for alias, name in config['roster_names'].items():
        aa = [r for r in availability if r['player'] == alias]
        positive = sorted(r['date'] for r in byplayer.get(name, []) if int(r['seconds']) > 0)
        player_summary.append(dict(player=alias, source_rows=len(byplayer.get(name, [])),
            observed_GP=len(positive), historical_teams=sorted({r['team'] for r in byplayer.get(name, [])}),
            first_played=positive[0] if positive else None, last_played=positive[-1] if positive else None,
            calendar_evidence_counts=dict(sorted(Counter(r['evidence'] for r in aa).items())),
            primary_status_counts=dict(sorted(Counter(r['primary_status'] for r in aa if r['primary_status']).items()))))
    prior_packet = dict(stage='O-15G12', opening_information_cutoff=config['opening_information_cutoff'], players=priors,
        data_vintage='2020-21_REGULAR_ONLY; 2021-22_OBSERVATIONS_EXCLUDED',
        fictional_prior_references=['CHICAGO_2020_21_PREDEADLINE_PRODUCTION_PRIORS.csv', 'CHICAGO_2020_21_POSTDEADLINE_BOX_INPUTS.json'],
        rookie_scope='No NBA prior is not zero ability; NCAA translation and role acceptance remain unfilled',
        author_locked=False, season_selected=False, exact_execution_cleared=False, manuscript_allowed=False)
    report = dict(stage='O-15G12', status='HISTORICAL_CALENDAR_AND_PRIOR_INPUTS_NOT_SEASON_SELECTED',
        league_games=len(league), chicago_games=len(calendar), chicago_home=sum(r['home'] == 'CHI' for r in calendar),
        chicago_away=sum(r['away'] == 'CHI' for r in calendar), calendar_player_rows=len(availability),
        observed_mirror_rows=len(observations), historical_back_to_back_second_games=sum(r['historical_back_to_back_second'] for r in calendar),
        historical_four_in_five_end_dates=[r['date'] for r in calendar if r['historical_games_last5_days'] >= 4],
        historical_chi_record={'wins': sum((int(r['home_pts']) > int(r['away_pts'])) == (r['home'] == 'CHI') for r in calendar), 'losses': 0},
        team_time_residual_counts=dict(sorted(Counter(int(r[k]) for r in league for k in ('home_seconds_residual', 'away_seconds_residual')).items())),
        nonzero_time_residual_games=sum(any(int(r[k]) for k in ('home_seconds_residual', 'away_seconds_residual')) for r in league),
        player_summary=player_summary,
        missing_prior_for_normal_minutes=[r['player'] for r in priors if r['kind'] == 'PROPOSED_ROSTER' and r['normal_role_minutes'] and r['historical_prior'] is None],
        normal_minutes_without_nba_prior=sum(r['normal_role_minutes'] for r in priors if r['kind'] == 'PROPOSED_ROSTER' and r['historical_prior'] is None),
        official_game_date_checks=len(config['official_date_checks']), fresh_primary_numeric_box_checks=0,
        schedule_conflicts=config['schedule_conflicts'],
        source_content_sha256={str(p.relative_to(ROOT)): sha(p) for p in (SOURCE, META, OBS, LEAGUE, ROLE)},
        alternate_calendar_selected=False, alternate_availability_selected=False, alternate_production_selected=False,
        author_locked=False, season_selected=False, exact_execution_cleared=False, manuscript_allowed=False,
        independent_review='NOT_INDEPENDENT')
    report['historical_chi_record']['losses'] = 82 - report['historical_chi_record']['wins']
    # One new absent-player witness; every other player's availability is a
    # stated condition. Replace Coby's two slots with two eligible reserves.
    coby = copy.deepcopy(normal)
    coby.update(id='AV_Coby_EXAMPLE', kind='availability_stress', unavailable=['Coby'])
    coby['position_minutes']['PG']['Satoransky'] = coby['position_minutes']['PG'].pop('Coby')
    coby['position_minutes']['SG']['Denzel Valentine'] = coby['position_minutes']['SG'].pop('Coby')
    for witness in coby['lineup_witness']:
        for pos, player in list(witness['positions'].items()):
            if player == 'Coby':
                witness['positions'][pos] = 'Satoransky' if pos == 'PG' else 'Denzel Valentine'
    coby['interpretation_ko'] = '코비 비가용/나머지 가용 조건의 예시. Satoransky10·Valentine8을 넣으며 수비·창조/효율 보존은 미증명이다.'
    import build_chicago_2021_22_role_plan as role_validator
    trial = copy.deepcopy(role)
    trial['cases'].append(coby)
    assert role_validator.validate(trial) == [], 'Invalid Coby replacement witness'
    report['coby_absence_example'] = coby
    first_coby = next(r['first_played'] for r in player_summary if r['player'] == 'Coby')
    report['coby_first_observed_played_date'] = first_coby
    report['chicago_games_before_first_coby_played_observation'] = sum(r['date'] < first_coby for r in calendar)
    report['coby_gap_scope'] = 'Missing observations are not proof of an uninterrupted medical absence; example is not adopted for these dates.'
    return {CALENDAR: csv_text(calendar), AVAIL: csv_text(availability), PRIORS: json_text(prior_packet), REPORT: json_text(report)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.source_dir:
        if args.check:
            raise SystemExit('--check cannot ingest')
        ingest(args.source_dir)
    outputs = build()
    for path, content in outputs.items():
        if args.check:
            assert path.read_text() == content, 'STALE derived output: ' + path.name
        else:
            path.write_text(content)
    print('PASS: 1230 observed games / 82 CHI dates / 1230 player-date rows; prior vintage separated')


if __name__ == '__main__':
    main()
