"""Consume B roles in existing result models with independently declared ratings.

PTS determines only which coactors lost shot credit. It is never a rating
coefficient or a margin addition. Rating deltas are declared fiction/stress.
"""
import argparse
import csv
import hashlib
import io
import json
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = 'simulation/EARLY_REWARD_B_JOINT_RESULT_RESPONSE_2026_10_12'
BASE_MAIN = 'cd041183b49478bd0cff39bc8c6d3f74aab1eaa1'
FULL = 'simulation/EARLY_REWARD_B_CURRENT_FULL_ROLE_INPUTS_2026_10_12.csv'
ATTACK13 = 'simulation/EARLY_REWARD_B_YEAR1_YEAR3_DATED_ATTACK_2026_10_12.csv'
ATTACK2 = 'simulation/EARLY_REWARD_B_YEAR2_DATED_SHOTS_2026_10_11.csv'
ATTACK4 = 'simulation/EARLY_REWARD_B_YEAR4_DATED_ATTACK_2026_10_11.csv'
COURT2 = 'simulation/EARLY_REWARD_B_YEAR2_COURT_IMPACT_2026_10_11_COURT.csv'
SENS2 = 'simulation/EARLY_REWARD_B_YEAR2_COURT_IMPACT_2026_10_11_SENSITIVITY.csv'
YEAR1 = 'simulation/LC1_CHICAGO_2018_2019_USED_DEVELOPMENT_AND_RESULT_CONTACT_IMPLEMENTATION_2026_10_09.json'
YEAR3 = 'simulation/NBA_2020_21_SELECTED_REGULAR_OVERLAY.json'
YEAR4 = 'simulation/CHICAGO_2021_22_SELECTED_RESULTS_LEDGER.json'
SOURCES = [FULL, FULL.replace('.csv', '.json'), ATTACK13, ATTACK2, ATTACK4, COURT2, SENS2, YEAR1, YEAR3, YEAR4,
           'tools/run_chicago_2019_20_outcomes.mjs', 'tools/crosscheck_chicago_2020_21_impact.py',
           'tools/build_sas_2021_keeper_and_chicago_selected_results.py',
           'canon/EARLY_REWARD_B_AUTHOR_SELECTION_2026_10_11.json',
           'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json']

WORKING_P_DELTA = F('1/2')
WORKING_DEBIT_DELTA = F('-1/8')


def normalized(path):
    return (ROOT / path).read_bytes().removeprefix(b'\xef\xbb\xbf').replace(b'\r\n', b'\n').replace(b'\r', b'\n')


def read(path):
    return json.loads(normalized(path))


def csvrows(path):
    return list(csv.DictReader(io.StringIO(normalized(path).decode())))


def csvbytes(rows):
    buf = io.StringIO(newline='')
    writer = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader(); writer.writerows(rows)
    return buf.getvalue().encode()


def direction(low, high):
    return 'W' if low > 0 else 'L' if high < 0 else 'HOLD'


def find_result(value, game_id):
    if isinstance(value, dict):
        if value.get('game_id') == game_id and any(k.startswith('exact') and 'impact' in k for k in value):
            return value
        for child in value.values():
            found = find_result(child, game_id)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_result(child, game_id)
            if found is not None:
                return found
    return None


def build():
    pins = {path: hashlib.sha256(normalized(path)).hexdigest() for path in SOURCES}
    full = {(int(row['NBA_year']), row['date']): row for row in csvrows(FULL)}
    losses = defaultdict(set)
    minutes = {}
    for row in csvrows(ATTACK13):
        year, day, actor = int(row['NBA_year']), row['date'], row['actor']
        minutes[(year, day, actor)] = F(row['selected_seconds'])
        if actor != 'Protagonist' and F(row['PTS_delta']) < F('-0.000001'):
            losses[(year, day)].add(actor)
    for row in csvrows(ATTACK2):
        if row['player'] != 'Protagonist' and F(row['expected_pts']) - F(row['minute_scaled_before_expected_pts']) < F('-0.000001'):
            losses[(2, row['date'])].add(row['player'])
    for row in csvrows(COURT2):
        for i in range(1, 6):
            actor = 'Protagonist' if row['actor_' + str(i)] == 'P' else row['actor_' + str(i)]
            key = (2, row['date'], actor)
            minutes[key] = minutes.get(key, F(0)) + F(row['duration_seconds'])
    for row in csvrows(ATTACK4):
        actor, day = row['actor'], row['date']
        minutes[(4, day, actor)] = F(row['regulation_minutes']) * 60
        if actor != 'Protagonist' and F(row['expected_pts']) - F(row['scaled_before_rebalance_pts']) < F('-0.000001'):
            losses[(4, day)].add(actor)
    coefficients = []
    def add(year, family, day, game_id, low, high, parent):
        low, high = F(str(low)), F(str(high))
        role = full.get((year, day))
        p_seconds = F(role['selected_seconds']) if role else F(0)
        debt = sorted(losses[(year, day)])
        debt_seconds = sum((minutes[(year, day, actor)] for actor in debt), F(0))
        assert low <= high and direction(low, high) != 'HOLD'
        if role:
            assert minutes[(year, day, 'Protagonist')] == p_seconds, (year, day, 'P clock mismatch')
        coefficients.append({'NBA_year': year, 'family': family, 'date': day, 'game_id': game_id,
                             'base_CHI_low': str(low), 'base_CHI_high': str(high),
                             'P_rating_delta_coefficient': str(p_seconds / 2880),
                             'debit_group_rating_delta_coefficient': str(debt_seconds / 2880),
                             'debit_actors': '|'.join(debt), 'base_wl': direction(low, high),
                             'source': parent, 'own_pts_or_rebounds_added_to_margin': False})
    for row in read(YEAR1)['selected_result_model']['all82_rows']:
        margin = row['joint_selected_margin_proxy']
        add(1, 'SELECTED_BPM_BASE', row['date'], row['event_id'], margin, margin, YEAR1)
    for row in csvrows(SENS2):
        if F(row['declared_P_rating_delta_per48']) == 0:
            family = row['proxy'] + '_FATIGUE_' + row['fatigue_per48_second_night']
            add(2, family, row['date'], row['event_id'], row['base_margin_from_saved_parent'], row['base_margin_from_saved_parent'], SENS2)
    overlay = read(YEAR3)
    for row in overlay['regular_season_games']:
        if 'CHI' not in [row['home'], row['away']]:
            continue
        low, high = row['home_margin_band']
        if row['away'] == 'CHI':
            low, high = -high, -low
        add(3, 'SELECTED_BPM_MAR25_EB', row['date'], row['event_id'], low, high, YEAR3)
    ledger = read(YEAR4)
    for row in ledger['rows']:
        path = row['working_regulation_result']['source']
        pins[path] = hashlib.sha256(normalized(path)).hexdigest()
        result = find_result(read(path), row['game_id'])
        assert result is not None, row['game_id']
        exact = [F(value) for key, value in result.items() if key.startswith('exact') and 'impact' in key and isinstance(value, str)]
        assert len(exact) == 1, (row['game_id'], exact)
        add(4, 'SELECTED_SINGLE_BPM', row['date'], row['game_id'], exact[0], exact[0], path)
        assert coefficients[-1]['base_wl'] == ('W' if row['working_regulation_result']['winner'] == 'CHI' else 'L')
    coefficients.sort(key=lambda r: (r['NBA_year'], r['family'], r['date'], r['game_id']))
    assert len(coefficients) == 821
    assert len({(r['NBA_year'], r['family'], r['game_id']) for r in coefficients}) == len(coefficients)
    groups = defaultdict(list)
    for row in coefficients:
        groups[(row['NBA_year'], row['family'])].append(row)
    grid = []
    for (year, family), group in sorted(groups.items()):
        for p_delta in map(F, ['-2', '-1', '-1/2', '0', '1/2', '1', '2']):
            for debit_delta in map(F, ['-1/2', '-1/4', '-1/8', '0']):
                changed = []; holds = []; wins = 0; losses_count = 0
                for row in group:
                    delta = p_delta * F(row['P_rating_delta_coefficient']) + debit_delta * F(row['debit_group_rating_delta_coefficient'])
                    new = direction(F(row['base_CHI_low']) + delta, F(row['base_CHI_high']) + delta)
                    wins += new == 'W'; losses_count += new == 'L'
                    if new == 'HOLD': holds.append(row['game_id'])
                    if new != row['base_wl']: changed.append(row['game_id'])
                grid.append({'NBA_year': year, 'family': family, 'declared_P_total_rating_delta': str(p_delta),
                             'declared_debit_actor_total_rating_delta_each': str(debit_delta),
                             'wins': wins, 'losses': losses_count, 'HOLD': len(holds),
                             'changed_games': '|'.join(changed), 'all_old_directions_preserved': not changed,
                             'fictional_model_response_not_empirical_rating_estimate': True})
    proposed = [row for row in grid if row['declared_P_total_rating_delta'] == '1/2' and row['declared_debit_actor_total_rating_delta_each'] == '-1/8']
    compatible = all(row['all_old_directions_preserved'] for row in proposed)
    assert compatible and len(proposed) == 12
    working = []
    for row in coefficients:
        delta = WORKING_P_DELTA * F(row['P_rating_delta_coefficient']) + WORKING_DEBIT_DELTA * F(row['debit_group_rating_delta_coefficient'])
        low, high = F(row['base_CHI_low']) + delta, F(row['base_CHI_high']) + delta
        assert direction(low, high) == row['base_wl']
        working.append({**row, 'working_CHI_low': str(low), 'working_CHI_high': str(high),
                        'working_shift': str(delta), 'working_wl': direction(low, high),
                        'classification': 'DECLARED_FICTIONAL_TOTAL_IMPACT_WORKING_NOT_ACTUAL_SCORE'})
    files = {STEM + '_COEFFICIENTS.csv': csvbytes(coefficients), STEM + '_GRID.csv': csvbytes(grid),
             STEM + '_WORKING.csv': csvbytes(working)}
    report = {'id': 'EARLY_REWARD_B_JOINT_RESULT_RESPONSE_2026_10_12', 'baseline_main': BASE_MAIN,
              'status': 'ALL_FOUR_RESULT_CONSUMERS_JOINED_DECLARED_JOINT_RATING_RESPONSE_NOT_EMPIRICAL_FIT',
              'source_sha256': pins, 'coefficient_rows': len(coefficients), 'model_families': len(groups), 'grid_cases': len(grid),
              'model_formula': 'CHI_band_new=CHI_band_parent+(selectedPseconds/2880)*declaredP_total_delta+(sum_current_positive_shot_debit_actor_seconds/2880)*declared_debit_total_delta_each',
              'why_separate_from_boxes': 'PTS/REB/AST/STL/BLK/TOV are not converted to BPM. Negative shot-credit identifies stress recipients only. Delta values are bounded fictional total-impact assumptions including offensive/defensive/off-ball costs, not regression estimates.',
              'debit_scope': 'Only existing B negative dated coactor shot-credit above1e-6 rounding noise. No additional shot debit, new injury or implicit clinical loss. All eligible actors receive the same declared proxy stress; no claim their real ability fell.',
              'denominator_and_source_precision': 'All consumed source rating responses use seconds/2880. Existing scalar/band parents retained; year1 original4sec precision and year3 unresolved rating bands not zero-imputed. Legacy model numbers are not NBA score forecasts.',
              'proposed_bounded_working_family': {'P_total_delta': '1/2', 'debit_actor_total_delta_each': '-1/8',
                                                'motivation': 'Modest total-role improvement for earlier own attack while charging each actual dated opportunity loser a separate small effective-impact/rhythm cost. Not picked by maximizing safe boundary or by a box-to-rating fit.',
                                                'all_twelve_families_direction_compatible': compatible,
                                                'status': 'SELECTED_ROUTINE_WORKING_FICTIONAL_MODEL_NOT_PERSONAL_AWARD_OR_CANON_SCORE',
                                                'authority': 'Existing B-direction approval and delegated routine season-model execution; no materially different game, draft, contract or postseason route selected.',
                                                'selection_limit': 'A compatibility-preserving declared assumption, not observed BPM or an empirical calibration. Grid alternatives remain stress candidates. No whole-season exact-score certification.',
                                                'results': proposed},
              'current_working_response': {'path': STEM + '_WORKING.csv', 'rows': len(working), 'new_tie_or_unknown_direction': 0,
                                           'changed_old_game_directions': 0, 'source_selected_routes_not_rewritten': True},
              'baseline_replay': [{'NBA_year': year, 'family': family, 'games': len(group), 'wins': sum(r['base_wl']=='W' for r in group), 'losses': sum(r['base_wl']=='L' for r in group)} for (year, family), group in sorted(groups.items())],
              'preserved': {'source_outputs_not_rewritten': True, 'exact_personal_awards_or_medal_selected': 0, 'current_draft_contract_postseason_routes_not_overwritten': True},
              'remaining': ['Working family does not certify an empirical rating; a changed future assumption requires date-level route and downstream recheck.', 'Joint rebound/assist event ownership not certified by this result response.', 'Full East/West recognition position and fictional vote reasons; C01 exact branch; finalepisode/Blueprint/Pack.'],
              'gates': {'freeze':'v0.30 PARTIAL','design':'CLOSED','manuscript':0,'actual_Pack':0},
              'tools': {'Codex':'local source consumer reads and rational response construction','BasketballReference_primary':'403; no BPM formula body read or empirical fit claimed','Antigravity':'NOT_RUN','NotebookLM':'NOT_RUN','Claude':'NOT_RUN','independent_agent':'NOT_RUN'},
              'unfinished_major_groups':4,'unfinished_through_group6':3}
    report['output_LF_SHA256'] = {path: hashlib.sha256(raw).hexdigest() for path, raw in files.items()}
    files[STEM + '.json'] = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode()
    return files, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    files, report = build()
    for path, raw in files.items():
        if args.check:
            assert normalized(path) == raw, ('replay mismatch', path)
        else:
            with (ROOT/path).open('xb') as handle: handle.write(raw)
    print(json.dumps({'status':'PASS_RESULT_RESPONSE_REPLAY' if args.check else 'CREATED_RESULT_RESPONSE',
                      'coefficient_rows':report['coefficient_rows'],'families':report['model_families'],'grid_cases':report['grid_cases'],
                      'proposed':report['proposed_bounded_working_family']},ensure_ascii=False))


if __name__ == '__main__':
    main()
