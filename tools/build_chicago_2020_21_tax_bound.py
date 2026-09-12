"""Bound Chicago's post-trade salary without choosing the protagonist's pick."""
import csv
import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

from build_chicago_2020_21_execution_terms import allowance

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'research/CHICAGO_2020_21_TAX_BOUND_SOURCES.json'
PRIOR = ROOT / 'research/NBA_2020_21_L_EXECUTION_TERMS_SOURCES.json'
ROSTER = ROOT / 'simulation/CHICAGO_2021_POSTDEADLINE_ROSTER.csv'
OUT = ROOT / 'simulation/CHICAGO_2020_21_TAX_BOUND.json'


def non_tax_test(known_salary, residual, tax_level):
    """None means unverified; equality is eligible under VII 6(j)."""
    if residual is None:
        return None
    if residual < 0:
        raise ValueError('Do not invent a negative residual credit')
    return Fraction(known_salary) + Fraction(residual) <= tax_level


def build(sources, prior, roster):
    assert sources['author_locked'] is False
    assert sources['season_selected'] is False
    scale = sources['rookie_envelope']
    assert scale['author_pick'] is None and scale['author_salary_usd'] is None
    assert scale['contract_first_season'] == '2018-19'
    assert scale['option_season'] == '2020-21' and scale['option_year'] == 3
    assert scale['salary_percent_endpoints'] == [80, 120]
    scales = {int(k): v for k, v in scale['scale_100_percent_by_pick'].items()}
    assert set(scales) == set(range(16, 31))
    assert all(scales[p] >= scales[p + 1] for p in range(16, 30))
    for check in scale['crosschecks']:
        assert scales[check['pick']] * 120 // 100 == check['reported_option_salary_usd']
    rows = sources['salary_rows'] + [
        r for r in prior['salary_rows'] if r['player'] in {'Daniel Theis', 'Javonte Green'}]
    salaries = {r['player']: r for r in rows}
    assert len(salaries) == len(rows) == 14
    standard = [r['player'] for r in roster if r['contract_class'] == 'STANDARD']
    two_way = [r['player'] for r in roster if r['contract_class'] == 'TWO_WAY']
    assert len(standard) == len(set(standard)) == 15
    assert set(standard) == set(salaries) | {'Protagonist'}
    assert set(two_way) == {'Devon Dotson', 'Adam Mokoka'}
    assert all(r['season'] == '2020-21' for r in rows)
    assert all(r['reported_likely_usd'] == 0 for r in rows)
    assert all(r['base_usd'] >= 0 for r in rows)
    base = sum(r['base_usd'] for r in rows)
    bonus = sum(r['reported_unlikely_usd'] for r in rows)
    tax = sources['rule_sources'][0]['tax_level_usd']
    old = {r['player']: r for r in prior['salary_rows']}
    outgoing = sum(old[p]['base_usd'] for p in ['Daniel Gafford', 'Luke Kornet'])
    incoming = sum(salaries[p]['base_usd'] for p in ['Daniel Theis', 'Javonte Green'])
    cases = []
    for pick, amount in sorted(scales.items()):
        for percent in scale['salary_percent_endpoints']:
            rookie = amount * percent // 100
            for add_bonus in [0, bonus]:
                known = base + rookie + add_bonus
                cases.append({'pick_test_only': pick, 'scale_percent_test_only': percent,
                              'rookie_salary_test_usd': rookie, 'bonus_test_usd': add_bonus,
                              'post_trade_known_salary_usd': known,
                              'max_additional_charge_for_non_tax_usd': tax - known,
                              'non_tax_if_residual_zero': non_tax_test(known, 0, tax),
                              'actual_non_tax_status': non_tax_test(known, None, tax)})
    highest = max(c['post_trade_known_salary_usd'] for c in cases)
    camp = sum(r['reported_base_usd'] for r in sources['camp_contract_screen'])
    result = {
        'stage': sources['stage'], 'baseline_main': sources['baseline_main'],
        'standard_count': len(standard), 'two_way_excluded_count': len(two_way),
        'known_base_excluding_protagonist_usd': base,
        'known_pretrade_base_excluding_protagonist_usd': base - incoming + outgoing,
        'trade_net_salary_increase_usd': incoming - outgoing,
        'reported_bonus_stress_usd': bonus, 'tax_level_usd': tax,
        'rookie_envelope_usd': [min(c['rookie_salary_test_usd'] for c in cases),
                                max(c['rookie_salary_test_usd'] for c in cases)],
        'post_trade_known_salary_envelope_usd': [min(c['post_trade_known_salary_usd'] for c in cases), highest],
        'max_residual_for_all_tested_cases_usd': tax - highest,
        'cases': cases,
        'camp_full_face_value_stress': {
            'additional_test_charge_usd': camp, 'post_trade_with_max_rookie_and_bonus_usd': highest + camp,
            'remaining_margin_usd': tax - highest - camp,
            'actual_charge': False, 'complete_residual_bound': False},
        'matching_margin_if_non_tax_confirmed_usd': float(allowance(outgoing, False) - incoming),
        'matching_margin_if_taxpayer_usd': float(allowance(outgoing, True) - incoming),
        'exact_residual_charge_usd': None, 'actual_non_tax_status': None,
        'exact_trade_cleared': False, 'author_pick': None, 'author_salary_usd': None,
        'author_locked': False, 'season_selected': False,
        'requirements_closed': 0, 'review': 'NOT_INDEPENDENT',
        'manuscript_allowed': False,
    }
    assert all(c['non_tax_if_residual_zero'] for c in cases)
    return result


def main():
    sources, prior = [json.loads(p.read_text()) for p in (SOURCES, PRIOR)]
    with ROSTER.open() as f:
        roster = list(csv.DictReader(f))
    result = build(sources, prior, roster)
    result['input_sha256'] = {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                              for p in (SOURCES, PRIOR, ROSTER)}
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'PASS': True, 'conditions': len(result['cases']),
                      'max_residual_for_all_cases_usd': result['max_residual_for_all_tested_cases_usd'],
                      'actual_non_tax_status': result['actual_non_tax_status'],
                      'exact_trade_cleared': result['exact_trade_cleared']}))


if __name__ == '__main__':
    main()
