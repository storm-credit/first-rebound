"""Build/check the selected B direction's year-two expected scoring-credit model.

This conserves expected PTS credit, not possessions or observed integer boxes.
No parent season ledger is overwritten. Shot allocation and causal impacts remain
separate required joins, explicitly recorded in the artifact.
"""
import argparse
import csv
import hashlib
import io
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = 'simulation/EARLY_REWARD_B_YEAR2_CREDIT_BUDGET_2026_10_11.json'
SOURCE_PATHS = [
    'canon/EARLY_REWARD_B_AUTHOR_SELECTION_2026_10_11.json',
    'simulation/CHICAGO_2019_20_ROSTER_BASELINE.csv',
    'simulation/CHICAGO_2019_20_PLAYER_GAME_DONOR_VECTOR.csv',
    'simulation/CHICAGO_2019_20_PLAYER_GAME_MINUTE_LEDGER.csv',
    'simulation/CHICAGO_2019_20_PRODUCTION_PRIORS.csv',
    'simulation/CHICAGO_2019_20_OUTCOME_LEDGER.csv',
]


def text(path):
    return (ROOT / path).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def rows(path):
    return list(csv.DictReader(io.StringIO(text(path))))


def n(value):
    return round(float(value), 9)


def build():
    decision = json.loads(text(SOURCE_PATHS[0]))
    if decision['B']['selected_option'] != 'B':
        raise ValueError('B author direction must be selected')
    roster, donors, games, priors, outcomes = [rows(p) for p in SOURCE_PATHS[1:]]
    base = next(x for x in priors if x['scenario'] == 'BASE')
    minutes = sum(F(x['protagonist_seconds']) / 60 for x in games)
    assert minutes == 1395 and len(games) == 65
    assert len(roster) == 17 and len({x['player'] for x in roster}) == 17
    assert len({x['event_id'] for x in games}) == 65
    assert len({x['game_id'] for x in games}) == 65
    assert {x['player'] for x in donors} <= {x['player'] for x in roster}
    for x in donors:
        assert F(x['alternate_seconds']) - F(x['actual_seconds']) == F(x['delta_seconds'])
    for game in games:
        assert sum(F(x['delta_seconds']) for x in donors if x['event_id'] == game['event_id']) == -F(game['protagonist_seconds'])
        assert game['actual_team_seconds'] == game['alternate_team_seconds']
    old_rate = F(base['pts36'])
    old_total = old_rate * minutes / 36
    # Adopt the approved option's lower target as a model input; no award assigned.
    target_ppg = F(12)
    new_total = target_ppg * len(games)
    new_rate = new_total * 36 / minutes
    added = new_total - old_total
    weights = {
        'Zach LaVine': F(2, 5), 'Coby White': F(1, 5),
        'Lauri Markkanen': F(1, 5), 'Thaddeus Young': F(1, 10),
        'Tomas Satoransky': F(1, 10),
    }
    assert sum(weights.values()) == 1
    credit_rows = []
    before_total = after_total = F(0)
    for player in roster:
        name = player['player']
        actual_seconds = F(player['seconds'])
        delta = sum(F(x['delta_seconds']) for x in donors if x['player'] == name)
        retained_seconds = actual_seconds + delta
        assert retained_seconds >= 0
        before = F(player['pts']) * retained_seconds / actual_seconds
        debit = added * weights.get(name, F(0))
        after = before - debit
        assert after >= 0, (name, after)
        if name in weights and name != 'Thaddeus Young':
            assert delta == 0  # scoring costs do not secretly take protected minutes
        before_total += before
        after_total += after
        credit_rows.append({
            'player': name, 'historical_pts': int(player['pts']),
            'historical_seconds': int(actual_seconds),
            'existing_minute_delta_seconds': int(delta),
            'retained_seconds_unchanged_by_B': int(retained_seconds),
            'before_expected_pts': n(before), 'B_expected_pts_debit': n(debit),
            'after_expected_pts': n(after),
            'debit_share_of_before_expected_pts': n(debit / before) if before else 0,
            'classification': 'FICTIONAL_EXPECTED_CREDIT_NOT_OBSERVED_BOX',
        })
    assert before_total + old_total == after_total + new_total
    # A coherent P-only shot witness. These are author-model inputs, not measured
    # shooting improvements. Missing old FGA/FTA prevents a claimed delta budget.
    ts, three_pa, three_p, fta, ft = F('0.560'), F(3), F('0.320'), F(5), F('0.720')
    three_pm, ftm = three_pa * three_p, fta * ft
    fga = new_rate / (2 * ts) - F('0.44') * fta
    two_pa = fga - three_pa
    two_pm = (new_rate - 3 * three_pm - ftm) / 2
    assert 0 <= two_pm <= two_pa and two_pa > 0
    assert 2 * two_pm + 3 * three_pm + ftm == new_rate
    assert new_rate / (2 * (fga + F('0.44') * fta)) == ts
    game_rows = [{
        'event_id': x['event_id'], 'game_id': x['game_id'], 'date': x['date'],
        'minutes_unchanged': n(F(x['protagonist_seconds']) / 60),
        'old_expected_pts': n(old_rate * F(x['protagonist_seconds']) / 2160),
        'B_expected_pts': n(new_rate * F(x['protagonist_seconds']) / 2160),
        'integer_box_selected': False, 'game_donor_shot_allocation': None,
    } for x in games]
    # This is the result model's actual dependency, not a recomputation claim.
    result_scope = {}
    for proxy in sorted({x['proxy'] for x in outcomes}):
        chosen = [x for x in outcomes if x['proxy'] == proxy and x['scenario'] == 'BASE']
        assert len(chosen) == len(games)
        result_scope[proxy] = {
            'existing_base_wins': sum(x['base_alt_wl'] == 'W' for x in chosen),
            'existing_P_rating': sorted({x['protagonist_rating'] for x in chosen}),
            'changed_rating_not_inferred_from_pts': None,
            'changed_results_not_certified': True,
        }
    return {
        'id': 'EARLY_REWARD_B_YEAR2_CREDIT_BUDGET_2026_10_11',
        'status': 'SELECTED_WORKING_P_AND_SEASON_CREDIT_INPUT_SHOT_AND_IMPACT_JOIN_PENDING',
        'classification': 'DELEGATED_B_IMPLEMENTATION_MODEL_NOT_EXACT_CANON_STATS',
        'source_hash_method': 'SHA256_UTF8_LF',
        'source_sha256': {p: hashlib.sha256(text(p).encode()).hexdigest() for p in SOURCE_PATHS},
        'authority': 'User selected B direction. Root implements its 12PPG lower target and finite coactor costs as a working model; exact stats/results/awards are not author-locked by this model.',
        'data_vintage': '2019–20 full-season observations are ex-post simulation references. They are not information a character/coach had at the opening or an award voting cutoff; no MIP result is certified here.',
        'role': {'GP': 65, 'GS': sum(int(x['protagonist_start']) for x in games),
                 'minutes': int(minutes), 'old_expected_pts': n(old_total),
                 'new_expected_pts': n(new_total), 'target_PPG': n(target_ppg),
                 'old_PTS36': n(old_rate), 'new_PTS36': n(new_rate),
                 'additional_expected_pts_credit': n(added)},
        'P_only_shot_witness': {
            'TS': n(ts), 'three_PA36': n(three_pa), 'three_P': n(three_p),
            'FTA36': n(fta), 'FT': n(ft), 'FTM36': n(ftm),
            'FGA36': n(fga), 'two_PA36': n(two_pa), 'two_PM36': n(two_pm),
            'two_P': n(two_pm / two_pa), 'three_PM36': n(three_pm),
            'old_FGA36': None, 'old_FTA36': None, 'delta_FGA36': None,
            'team_shots_or_possessions_conserved': False,
            'meaning': 'Coherent expected shooting vector; no measured training efficacy or integer/game shot budget certificate.',
        },
        'coactor_credit_rows': credit_rows, 'P_game_expected_rows': game_rows,
        'credit_conservation': {
            'before_team_expected_pts_credit': n(before_total + old_total),
            'after_team_expected_pts_credit': n(after_total + new_total),
            'exact_fraction_equality': True,
            'interpretation': 'PTS attribution equality only. Does not prove unchanged team efficiency, possession counts or win/loss.',
        },
        'development': {
            'new_reward': 'Closeout advantage can end in his own finish; a second defender closing early triggers the existing short pass.',
            'failure_kept': 'Weak-hand first-wall failure and drive-turnover cost remain; no fulltime primary creation or elite jumper added.',
            'coactor_cost': 'LaVine126/Coby63/Mark63/Young31.5/Satoransky31.5 expected season scoring credits move to P; core minutes stay. Their actions and responses need dated shot ownership.',
            'recognition': 'MIP competition, no award/vote/AllStar/HigherMax assigned.',
        },
        'outcome_model_dependency': result_scope,
        'next_required_joins': [
            'Recover/use dated player FGA/FTA/TOV and active lineups for the consumed shot allocation; aggregate points alone cannot certify shot availability.',
            'Allocate the 315 credit cost to actual available coactors on consumed dates; the season weights are not five donors present every game.',
            'Re-evaluate affected BPM/NET_EB and keeper/result/draft inputs after changed attack role is chosen; do not set causal rating = scoring gain.',
            'Join B year1/year3/year4 separately and use only information available at each award-selection cutoff.',
        ],
        'gates': {'freeze': 'v0.30 PARTIAL', 'design': 'CLOSED', 'manuscript_allowed': False,
                  'actual_Pack': 0, 'new_individual_awards': 0},
        'external_tools': 'Codex only; no fresh AGY/NotebookLM/Claude or independent agent review',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    content = (json.dumps(build(), ensure_ascii=False, indent=2) + '\n').encode()
    path = ROOT / OUT
    if args.check:
        if path.read_bytes().replace(b'\r\n', b'\n') != content:
            raise SystemExit('FAIL: artifact differs from computed model or source pins')
        print('PASS: 65 dated P rows, 17 coactors, exact credit conservation and coherent P-only shots; full shot/result joins pending')
    else:
        if path.exists():
            raise SystemExit('Refusing to overwrite existing artifact; use --check')
        path.write_bytes(content)
        print(f'WROTE {OUT}')
