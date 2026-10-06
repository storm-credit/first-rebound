"""Adopt all existing date models as a working calendar without clearing season gates."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import build_2021_playoff_calendar_candidate as chronology

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'simulation/NBA_2021_PLAYOFF_CALENDAR_CANDIDATE.json'
COACH = 'simulation/DEN_LAL_2021_DATED_COACH_PLAN.json'
AUTHORITY = 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
OUT = 'simulation/NBA_2021_WORKING_PLAYOFF_CALENDAR.json'


def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256((ROOT/path).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n').encode()).hexdigest()


def validate(result):
    source = read(SOURCE)
    chronology.validate(source)
    if result['source_sha256'] != {p: sha(p) for p in (SOURCE, COACH, AUTHORITY)}:
        raise ValueError('stale calendar adoption inputs')
    expected = []
    for series in source['series']:
        for game in series['games']:
            expected.append(dict(series=series['id'], game=game['game'],
                date_model=game['date_candidate'], teams=series['teams'],
                home_team=game['home_team_candidate'], working_date_adopted=True,
                game_winner_model=game['selected_game_winner'],
                coach_plan=COACH if series['id'] == 'W3' else None,
                medical_verified=False, actual_active_list_certified=False,
                actual_venue_booking_certified=False))
    if result['games'] != expected:
        raise ValueError('working calendar not identical to validated source date models')
    den = [g for g in result['games'] if g['series'] == 'W3']
    plans = read(COACH)['games']
    if [(g['date_model'], g['home_team'], g['game_winner_model']) for g in den] != [
            (g['date_model'], g['home_team'], g['selected_winner']) for g in plans]:
        raise ValueError('six-game coach plan and adopted calendar disagree')
    if (not result['working_calendar_adopted'] or result['working_games_adopted'] != len(expected)
            or len(expected) != 88 or result['working_series_adopted'] != 15
            or result['coach_plan_games_applied'] != len(den)
            or result['other_coach_plan_games_remaining'] != len(expected)-len(den)):
        raise ValueError('working calendar coverage mismatch')
    if (result['actual_schedule_certified'] or result['whole_health_cleared']
            or result['whole_coach_plans_applied'] or result['season_selected']
            or result['manuscript_allowed']):
        raise ValueError('date adoption promoted to medical/coaching/season clearance')


def build():
    source = read(SOURCE)
    result = dict(status='ALL_15_SERIES_88_DATE_MODELS_ADOPTED_AS_WORKING_CALENDAR',
        baseline_main='76cd80b085bf4b0b0a305fa944ee76e185efb4a8', date_local='2026-10-07',
        authority=AUTHORITY, authority_type='EXISTING_SEASON_DESIGN_DELEGATION_ROUTINE_DATE_APPLICATION',
        source_sha256={p: sha(p) for p in (SOURCE, COACH, AUTHORITY)},
        working_calendar_adopted=True, working_series_adopted=15, working_games_adopted=88,
        coach_plan_games_applied=6, other_coach_plan_games_remaining=82,
        actual_schedule_certified=False, whole_health_cleared=False,
        whole_coach_plans_applied=False, season_selected=False, manuscript_allowed=False,
        games=[])
    for series in source['series']:
        for game in series['games']:
            result['games'].append(dict(series=series['id'], game=game['game'],
                date_model=game['date_candidate'], teams=series['teams'],
                home_team=game['home_team_candidate'], working_date_adopted=True,
                game_winner_model=game['selected_game_winner'],
                coach_plan=COACH if series['id'] == 'W3' else None,
                medical_verified=False, actual_active_list_certified=False,
                actual_venue_booking_certified=False))
    validate(result)
    return result


def negative_tests(result):
    mutations = [
        lambda r: r['games'][0].__setitem__('date_model', '2021-07-22'),
        lambda r: r['games'].pop(),
        lambda r: r['games'][0].__setitem__('home_team', 'DEN'),
        lambda r: r['games'][0].__setitem__('medical_verified', True),
        lambda r: r.__setitem__('whole_coach_plans_applied', True),
    ]
    for mutate in mutations:
        candidate = deepcopy(result)
        mutate(candidate)
        try:
            validate(candidate)
        except ValueError:
            continue
        raise AssertionError('invalid calendar adopted')


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
    print('PASS: 15 series / 88 working dates adopted / DEN-LAL6 linked; remaining82 coach plans and whole season HOLD')
