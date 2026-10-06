"""Apply delegated game-result models to adopted dates; no observed scores."""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALENDAR = 'simulation/NBA_2021_WORKING_PLAYOFF_CALENDAR.json'
SERIES = 'simulation/NBA_2021_DELEGATED_PLAYOFF_RESULTS.json'
PRESERVED = 'simulation/DEN_LAL_2021_DATED_COACH_PLAN.json'
AUTHORITY = 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
OUT = 'simulation/NBA_2021_DATED_PLAYOFF_RESULT_MODELS.json'
# W=selected series winner; L=selected series loser. These are new working
# design choices, not extraction of historical game outcomes.
PATTERNS = {
    'E1': 'WWLWW', 'E2': 'WWLWW', 'E3': 'WWWW', 'E4': 'WLWWW',
    'W1': 'LWWWW', 'W2': 'WLWLWW', 'W4': 'LLWWLWW',
    'E5': 'WLLWLWW', 'E6': 'LLWWLWW', 'W5': 'LLWWWW',
    'W6': 'WWLLWLW', 'E7': 'LWWLWW', 'W7': 'WWLWLW', 'F1': 'LLWWWW',
}
REASONS = {
    'E1': 'PHI wins both opening home games; IND earns one home win before PHI closes. New opponent requires new execution.',
    'E2': 'BKN wins opening home games; BOS earns one home win. Brown availability is a separate input, not a score proof.',
    'E3': 'MIL four-game advance preserves the selected sweep; each game still needs a basketball execution model.',
    'E4': 'ATL wins two road games including the closeout; NYK wins game2. No historical shots or scores are imported.',
    'W1': 'MEM carries play-in momentum into game1; UTA answers with four wins. Mitchell health must be separately modeled.',
    'W2': 'PHX organizes two opening games around a split, POR splits at home, PHX closes two. No original Paul shoulder event is imported.',
    'W4': 'DAL wins opening two; LAC answers on the road, DAL takes game5, LAC closes two. Hampton and Oturu roles remain explicit; Carey33 was rejected.',
    'E5': 'ATL splits opening road games, PHI takes game3, ATL takes game4, PHI game5, ATL closes home then away; pressure execution is modeled separately.',
    'E6': 'BKN opens with two home wins, MIL answers at home; BKN game5, MIL closes home then away. No automatic Irving or Harden injury explanation.',
    'W5': 'UTA opens with two home wins; LAC changes matchup coverage for four wins. No automatic Leonard contact injury.',
    'W6': 'Home teams win all seven; PHX home advantage resolves selected seven-game result with James/Davis health separately modeled.',
    'E7': 'ATL wins game1, MIL wins games2/3, ATL game4, MIL closes home then away. No automatic original Young or Giannis injury.',
    'W7': 'PHX takes opening two, LAC answers at home; PHX wins game4, LAC game5, PHX closes away. Paul protocol and Leonard health are separate designs.',
    'F1': 'PHX opens with two home wins, MIL answers with four through rim pressure and defense; changed prior workload is carried by coach plans.',
}


def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))


def sha(path):
    text = (ROOT/path).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(text.encode()).hexdigest()


def expected_games():
    series = {s['id']: s for s in read(SERIES)['series']}
    old = {g['game']: g for g in read(PRESERVED)['games']}
    result = []
    for game in read(CALENDAR)['games']:
        sid, number = game['series'], game['game']
        selected = series[sid]
        winner = (old[number]['selected_winner'] if sid == 'W3' else
                  selected['winner'] if PATTERNS[sid][number-1] == 'W' else selected['loser'])
        result.append(dict(series=sid, game=number, date_model=game['date_model'],
            teams=game['teams'], home_team=game['home_team'], winner_model=winner,
            classification='AUTHOR_DELEGATED_WORKING_GAME_RESULT',
            authority=AUTHORITY, actual_box=None, score_model=None,
            historical_result_certified=False, medical_certified=False))
    return result


def validate(result):
    if (result['authority'] != AUTHORITY
            or result['status'] != 'ALL_88_DATED_GAME_RESULT_MODELS_APPLIED_EXECUTION_HOLD'
            or result['baseline_main'] != '1401b7482f0a1ca8b5600bba70d403091344b2b4'):
        raise ValueError('working result authority/status/baseline changed')
    if result['patterns'] != PATTERNS or result['selection_reasons'] != REASONS:
        raise ValueError('selected pattern/reason metadata changed')
    if result['source_sha256'] != {p: sha(p) for p in (CALENDAR, SERIES, PRESERVED, AUTHORITY)}:
        raise ValueError('stale result sources')
    if result['games'] != expected_games():
        raise ValueError('dated result differs from explicitly selected pattern')
    if any(g['winner_model'] != g['home_team'] for g in result['games'] if g['series']=='W6'):
        raise ValueError('selected PHX-LAL home-win rationale not applied to actual adopted home dates')
    if sum(g['winner_model']=='ATL' and g['home_team']!='ATL' for g in result['games'] if g['series']=='E4') != 2:
        raise ValueError('ATL selected road-win count mismatch')
    series = read(SERIES)['series']
    if len(result['games']) != 88 or len(series) != 15:
        raise ValueError('whole playoff coverage required')
    for selected in series:
        rows = [r for r in result['games'] if r['series'] == selected['id']]
        wins = Counter()
        for row in rows:
            if max(wins.values(), default=0) >= 4:
                raise ValueError('game played after series already decided')
            if row['winner_model'] not in selected['teams']:
                raise ValueError('nonparticipant winner')
            wins[row['winner_model']] += 1
        if (wins[selected['winner']] != 4 or wins[selected['loser']] != selected['loser_wins']
                or rows[-1]['winner_model'] != selected['winner']):
            raise ValueError('series result/length changed')
    if (result['dated_result_models_applied'] != 88 or result['new_game_results_applied'] != 82
            or result['preserved_game_results'] != 6 or result['series_results_changed'] != 0):
        raise ValueError('coverage metadata mismatch')
    if any(result[key] for key in ('whole_health_cleared', 'legal_execution_cleared',
                                   'season_selected', 'manuscript_allowed')):
        raise ValueError('game design promoted to overall clearance')


def build():
    result = dict(status='ALL_88_DATED_GAME_RESULT_MODELS_APPLIED_EXECUTION_HOLD',
        baseline_main='1401b7482f0a1ca8b5600bba70d403091344b2b4', date_local='2026-10-07',
        authority=AUTHORITY, source_sha256={p: sha(p) for p in (CALENDAR, SERIES, PRESERVED, AUTHORITY)},
        patterns=PATTERNS, pattern_key='W=selected series winner; L=selected series loser',
        selection_reasons=REASONS, games=expected_games(), dated_result_models_applied=88,
        new_game_results_applied=82, preserved_game_results=6, series_results_changed=0,
        whole_health_cleared=False, legal_execution_cleared=False,
        season_selected=False, manuscript_allowed=False)
    validate(result)
    return result


def negative_tests(result):
    mutations = [lambda r: r['games'][0].__setitem__('winner_model', 'DEN'),
        lambda r: r['games'][4].__setitem__('winner_model', 'IND'),
        lambda r: r['games'][0].__setitem__('date_model', '2021-07-20'),
        lambda r: r['games'][0].__setitem__('score_model', [120, 100]),
        lambda r: r['games'][0].__setitem__('medical_certified', True),
        lambda r: r.__setitem__('season_selected', True), lambda r: r['games'].pop(),
        lambda r:r.__setitem__('authority','invented-authority.json'),
        lambda r:r.__setitem__('status','ALL_LEGAL_PASS'),
        lambda r:r.__setitem__('baseline_main','invented')]
    for mutate in mutations:
        candidate = deepcopy(result)
        mutate(candidate)
        try:
            validate(candidate)
        except ValueError:
            continue
        raise AssertionError('invalid working result accepted')


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
    print('PASS: 88 dated results / 82 new / 6 preserved / 15 selected series unchanged; scores/health/legal/season HOLD')
