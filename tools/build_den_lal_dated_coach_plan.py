"""Apply the delegated six-game working plan; no historical box or medical claim."""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = 'simulation/DEN_LAL_2021_DATED_COACH_PLAN.json'
SOURCES = [
    'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json',
    'simulation/DEN_LAL_2021_DELEGATED_SERIES.json',
    'simulation/DEN_LAL_2021_SIX_DATE_CANDIDATE_BRIDGE.json',
    'simulation/NBA_2021_PLAYOFF_CALENDAR_CANDIDATE.json',
    'research/DEN_CLE_REGISTRATION_LEGAL_DOMAIN_2026_10_05.json',
    'research/DEN_LAL_2021_COACH_PLAN_SOURCE_BRIDGE.json',
]
ALIASES = {
    'Campazzo': 'Facundo Campazzo', 'Rivers': 'Austin Rivers',
    'Porter Jr.': 'Michael Porter Jr.', 'Gordon': 'Aaron Gordon',
    'Jokic': 'Nikola Jokic', 'Howard': 'Markus Howard',
    'Hartenstein': 'Isaiah Hartenstein', 'Murray': 'Jamal Murray',
    'Barton': 'Will Barton', 'Dozier': 'PJ Dozier',
    'Schroder': 'Dennis Schroder', 'Caldwell-Pope': 'Kentavious Caldwell-Pope',
    'James': 'LeBron James', 'Davis': 'Anthony Davis',
    'Drummond': 'Andre Drummond', 'Caruso': 'Alex Caruso',
    'Kuzma': 'Kyle Kuzma', 'Horton-Tucker': 'Talen Horton-Tucker',
    'Matthews': 'Wesley Matthews', 'Gasol': 'Marc Gasol',
}


def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))


def sha(path):
    value = (ROOT/path).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(value.encode()).hexdigest()


def canonical(name):
    return ALIASES.get(name, name)


def expected_rosters():
    source = read(SOURCES[5])
    den = [b['rows'][-1] for b in read(SOURCES[4])['branches'] if b['team'] == 'DEN']
    assert len(den) == 2 and den[0]['standard'] == den[1]['standard'] and den[0]['two_way'] == den[1]['two_way']
    return {'DEN': {'standard': den[0]['standard'], 'two_way': den[0]['two_way']},
            'LAL': {'standard': source['lakers_final_standard'], 'two_way': source['lakers_two_way']}}


def validate(packet):
    if packet['source_sha256'] != {p: sha(p) for p in SOURCES}:
        raise ValueError('stale working-plan source')
    series, dates = read(SOURCES[1]), read(SOURCES[2])
    rosters = packet['working_rosters']
    if rosters != expected_rosters():
        raise ValueError('working roster differs from preserved source')
    if len(packet['games']) != 6:
        raise ValueError('six dated games required')
    if len({g['date_model'] for g in packet['games']}) != 6:
        raise ValueError('duplicate game date')
    aggregate = {team: Counter() for team in ('DEN', 'LAL')}
    for n, game in enumerate(packet['games']):
        if (game['date_model'] != dates['games'][n]['date_candidate']
                or game['home_team'] != series['home_teams'][n]
                or game['selected_winner'] != series['game_winners'][n]):
            raise ValueError('date/home/result design drift')
        if not game['working_date_adopted'] or game['duration_model_minutes'] != 48:
            raise ValueError('missing modeled date or regulation duration')
        for team in ('DEN', 'LAL'):
            roster = rosters[team]['standard'] + rosters[team]['two_way']
            available = {canonical(p) for p in series['availability_model'][team+'_available']}
            absent = {canonical(p) for p in series['availability_model'].get(team+'_out', [])}
            if len(roster) != len(set(roster)) or len(rosters[team]['standard']) != 15 or len(rosters[team]['two_way']) != 2:
                raise ValueError('working roster duplicate/capacity')
            minutes = Counter()
            end = 0
            for block in game['blocks']:
                if block['start'] != end or block['end'] <= end:
                    raise ValueError('clock gap or reversed block')
                lineup = block[team]
                if len(lineup) != 5 or len(set(lineup)) != 5 or not set(lineup) <= set(roster):
                    raise ValueError('lineup membership/unique five')
                end = block['end']
                for player in lineup:
                    minutes[player] += block['end'] - block['start']
            if end != 48 or sum(minutes.values()) != 240:
                raise ValueError('shared-clock conservation')
            if dict(minutes) != game['teams'][team]['planned_minutes']:
                raise ValueError('planned minutes not generated from blocks')
            players = game['teams'][team]['players']
            if set(players) != set(roster):
                raise ValueError('whole working roster classification missing')
            for player, row in players.items():
                expected_mode = ('MODELED_AVAILABLE_PLANNED_ROTATION' if player in available
                    else 'MODELED_ABSENT' if player in absent else 'COACH_ZERO_HEALTH_UNSELECTED')
                expected_class = 'standard' if player in rosters[team]['standard'] else 'two_way'
                expected_health = 'AUTHOR_MODELED' if player in available|absent else None
                if (row['mode'] != expected_mode or row['contract_class'] != expected_class
                        or row['health_model'] != expected_health):
                    raise ValueError('availability or contract class differs from selected source')
                if row['planned_minutes'] != minutes.get(player, 0):
                    raise ValueError('player minutes mismatch')
                if row['mode'] == 'MODELED_ABSENT' and row['planned_minutes']:
                    raise ValueError('positive minutes for modeled absence')
                if row['mode'] == 'COACH_ZERO_HEALTH_UNSELECTED' and row['health_model'] is not None:
                    raise ValueError('zero/DNP converted to medical absence')
                if row['medical_certified'] or row['actual_active_list_certified']:
                    raise ValueError('medical/receipt authority promotion')
            if team == 'DEN' and any(p in players for p in ('Zeke Nnaji', 'JaVale McGee', 'R.J. Hampton')):
                raise ValueError('superseded Denver player imported')
            if not {'Isaiah Hartenstein', 'Saddiq Bey'} <= set(rosters['DEN']['standard']):
                raise ValueError('approved Denver directions lost')
            aggregate[team].update(minutes)
        if game['actual_box'] is not None or game['medical_health_verified'] or game['legal_registration_cleared']:
            raise ValueError('design adopted as actual/medical/legal execution')
    if {t: dict(v) for t, v in aggregate.items()} != packet['series_planned_minutes']:
        raise ValueError('series minute total mismatch')
    if any(sum(v.values()) != 1440 for v in aggregate.values()):
        raise ValueError('six-game team workload conservation')
    if (packet['dated_games_applied'] != 6 or packet['joint_clock_blocks_applied'] != 48
            or packet['roster_player_cells'] != sum(len(t['players']) for g in packet['games'] for t in g['teams'].values())):
        raise ValueError('execution metadata differs from actual rows')
    if packet['whole_calendar_selected'] or packet['season_selected'] or packet['manuscript_allowed']:
        raise ValueError('whole-season/gate promotion')


def build():
    series, dates = read(SOURCES[1]), read(SOURCES[2])
    rosters = expected_rosters()
    games = []
    totals = {team: Counter() for team in ('DEN', 'LAL')}
    for n, date_row in enumerate(dates['games']):
        blocks = deepcopy(series['rotation_witness']['blocks'])
        for block in blocks:
            for team in ('DEN', 'LAL'):
                block[team] = [canonical(p) for p in block[team]]
        teams = {}
        for team in ('DEN', 'LAL'):
            minutes = Counter()
            for block in blocks:
                for player in block[team]:
                    minutes[player] += block['end'] - block['start']
            available = {canonical(p) for p in series['availability_model'][team+'_available']}
            absent = {canonical(p) for p in series['availability_model'].get(team+'_out', [])}
            players = {}
            for kind, names in rosters[team].items():
                for player in names:
                    mode = ('MODELED_AVAILABLE_PLANNED_ROTATION' if player in available
                            else 'MODELED_ABSENT' if player in absent else 'COACH_ZERO_HEALTH_UNSELECTED')
                    players[player] = dict(contract_class=kind, mode=mode,
                        planned_minutes=minutes.get(player, 0),
                        health_model='AUTHOR_MODELED' if player in available|absent else None,
                        medical_certified=False, actual_active_list_certified=False)
            teams[team] = dict(planned_minutes=dict(minutes), players=players)
            totals[team].update(minutes)
        games.append(dict(game=n+1, date_model=date_row['date_candidate'],
            working_date_adopted=True, home_team=series['home_teams'][n],
            selected_winner=series['game_winners'][n], duration_model_minutes=48,
            overtime_model_periods=0, blocks=blocks, teams=teams,
            actual_box=None, medical_health_verified=False, legal_registration_cleared=False))
    result = dict(status='DATED_AUTHOR_MODELED_COACH_PLAN_APPLIED_6_GAMES',
        baseline_main='76cd80b085bf4b0b0a305fa944ee76e185efb4a8', adopted_date_local='2026-10-07',
        authority=SOURCES[0], authority_type='EXISTING_HEALTH_SEASON_COACHING_DELEGATION_WORKING_DESIGN',
        source_sha256={p: sha(p) for p in SOURCES}, working_rosters=rosters, games=games,
        series_planned_minutes={t: dict(v) for t, v in totals.items()},
        dated_games_applied=6, joint_clock_blocks_applied=48, roster_player_cells=204,
        medical_certified=False, actual_active_lists=None, exact_historical_boxes_adopted=False,
        whole_calendar_selected=False, season_selected=False, manuscript_allowed=False)
    validate(result)
    return result


def negative_tests(result):
    def invent_reserve(packet):
        names = packet['working_rosters']['DEN']['standard']
        names[names.index('Paul Millsap')] = 'Invented Reserve'
        for game in packet['games']:
            players = game['teams']['DEN']['players']
            players['Invented Reserve'] = players.pop('Paul Millsap')

    mutations = [
        lambda p: p['games'][0]['blocks'][0]['DEN'].__setitem__(0, 'Jamal Murray'),
        lambda p: p['games'][0]['blocks'][0]['DEN'].__setitem__(0, 'JaVale McGee'),
        lambda p: p['games'][0]['blocks'][0]['DEN'].__setitem__(0, 'Jokic'),
        lambda p: p['games'][1].__setitem__('date_model', p['games'][0]['date_model']),
        lambda p: p['games'][0]['blocks'][1].__setitem__('start', 7),
        lambda p: p['games'][0]['teams']['DEN']['players']['Paul Millsap'].__setitem__('health_model', 'ABSENT'),
        lambda p: p.__setitem__('season_selected', True),
        invent_reserve,
        lambda p: p['games'][0]['teams']['DEN']['players']['Jamal Murray'].update(
            mode='COACH_ZERO_HEALTH_UNSELECTED', health_model=None),
        lambda p: p['games'][0]['teams']['DEN']['players']['Markus Howard'].__setitem__('contract_class', 'standard'),
    ]
    for mutate in mutations:
        trial = deepcopy(result)
        mutate(trial)
        try:
            validate(trial)
        except ValueError:
            continue
        raise AssertionError('invalid execution design accepted')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.check:
        assert read(OUT) == result
    else:
        (ROOT/OUT).write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    if args.self_test:
        negative_tests(result)
    print('PASS: six dated working games / 48 shared blocks / 204 roster cells / 1440 planned minutes per team; medical/legal/whole season HOLD')
