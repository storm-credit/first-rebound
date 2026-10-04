"""Compare the approved F5 path without pretending a partial payroll is complete."""
import argparse
from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'research/DEN_F5_COST_COMPARATOR_2026_10_05.json'
REGISTRATION = 'research/DEN_CLE_REGISTRATION_LEGAL_DOMAIN_2026_10_05.json'
PAYROLL = 'simulation/BOSTON_DENVER_2020_21_PAYROLL.json'
BRIDGE = 'simulation/CHICAGO_2020_21_F4_F5_SELECTED_BRIDGE.json'
AUTHORITY = 'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json'
FUNDING = 'simulation/NBA_2021_EXECUTION_RESOLUTION.json'


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def build():
    registration = read(REGISTRATION)
    payroll = read(PAYROLL)
    bridge = read(BRIDGE)
    core = {r['player']: r for r in payroll['teams']['DEN']['core_players']}
    # Existing #22 120% input is a conditional public-table input, not a
    # recovered historical contract or an author-selected alternative ratio.
    scale = Decimal(core['Saddiq Bey']['base_usd']) / Decimal('1.2')
    delta = scale * Decimal('0.4')
    funding = read(FUNDING)['mcgee_funding']
    retained = int((Decimal(str(funding['simple_175_allowance_usd']))-100000)/Decimal('1.75'))
    assert retained == 1620564  # Reuse the existing reported basic-salary input.
    omitted = core['JaVale McGee']['base_usd']
    saving = omitted - retained
    paths = [REGISTRATION, PAYROLL, BRIDGE, AUTHORITY, FUNDING]
    den_branches = [b for b in registration['branches'] if b['team'] == 'DEN']
    assert len(den_branches) == 2 and all(len(b['rows']) == 53 for b in den_branches)
    assert all(all('Saddiq Bey' in r['standard'] and 'Isaiah Hartenstein' in r['standard']
                   and 'Zeke Nnaji' not in r['standard'] and 'JaVale McGee' not in r['standard']
                   for r in b['rows']) for b in den_branches)
    return {
        'schema': 1,
        'baseline_main': '305104151e98d8570e1b8388e9a9583cbf00efa0',
        'classification': 'CONDITIONAL_COMPARATOR_NOT_COMPLETE_COST_DOMAIN',
        'scope': {'team': 'DEN', 'start': '2021-03-25', 'end': '2021-05-16',
                  'phase': 'AFTER_BOTH_HISTORICAL_GORDON_AND_MCGEE_EVENTS',
                  'excludes': ['F3 intervening trade order', 'CLE cost',
                               'matching', 'pick obligations', 'actual contract execution']},
        'shared_apron_definition': '2017 CBA VII 6(m)(3); applicable 2020 amendments unverified',
        'evidence_sha256': {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
        'approved_transformation': {
            'historical_retained_rookie': 'Zeke Nnaji at #22',
            'alternate_retained_rookie': 'Saddiq Bey at #22',
            'historical_sent_rookie': 'R.J. Hampton at #24',
            'alternate_sent_rookie': 'Zeke Nnaji at #24',
            'historical_center': 'JaVale McGee',
            'alternate_center': 'Isaiah Hartenstein',
            'new_author_locks': 0},
        'reported_input_bounds': {
            'rookie_22_scale_100_usd': int(scale),
            'each_rookie_ratio_interval': [0.8, 1.2],
            'historical_ratio_verified': False,
            'alternate_ratio_selected': False,
            'retained_hartenstein_base_usd': retained,
            'omitted_mcgee_base_usd': omitted,
            'center_base_saving_usd': saving,
            'rookie_base_delta_interval_usd': [-int(delta), int(delta)],
            'named_base_delta_interval_usd': [-saving-int(delta), -saving+int(delta)],
            'complete_contract_charge_verified': False},
        'symbolic_cost_equation': 'ALT_APRON = HIST_APRON + DELTA_BASE + GAMMA_GORDON + GAMMA_CLARK + DELTA_OTHER',
        'unmeasured_differences': [
            {'id': 'GAMMA_GORDON', 'definition': 'alternative minus historical current-year allocated trade/signing bonus',
             'lower': None, 'upper': None, 'source_verified': False},
            {'id': 'GAMMA_CLARK', 'definition': 'alternative minus historical current-year allocated trade/signing bonus',
             'lower': None, 'upper': None, 'source_verified': False},
            {'id': 'DELTA_OTHER', 'definition': 'all other non-common charge differences: contract adjustments, prior obligations, exception/rights treatment, subsequent contracts and residuals',
             'lower': None, 'upper': None, 'source_verified': False}],
        'closure_conditions': {
            'historical_same_date_full_apron_bound': None,
            'historical_applicable_limit_source_verified': False,
            'same_definition_and_complete_delta_inventory_verified': False,
            'dominance_if_combined_other_delta_upper_at_most_usd': saving-int(delta),
            'equal_rookie_ratios_candidate': {'selected': False,
                'dominance_if_combined_other_delta_upper_at_most_usd': saving},
            'general_rule': 'HIST_UPPER + MAX_DELTA_BASE + MAX_GAMMA_GORDON + MAX_GAMMA_CLARK + MAX_DELTA_OTHER <= 138928000'},
        'daily_link': {'registration_days_per_branch': len(den_branches[0]['rows']),
                      'clark_release_date_branches': sorted(b['clark_release_date'] for b in den_branches),
                      'registration_complete_domain': registration['complete_domain'],
                      'release_does_not_erase_prior_pay': True,
                      'actual_intraday_receipt_times_verified': False},
        'reused_bridge_comparison': {'selected_conditional_peak_usd': bridge['listed_apron_stress_only']['DEN']['selected_usd'],
                                    'residual_allowance_usd': bridge['listed_apron_stress_only']['DEN']['residual_allowance_usd'],
                                    'not_historical_full_cost_certificate': True},
        'complete_domain': False, 'source_verified': False,
        'legal_fields_promoted': [], 'season_selected': False, 'manuscript_allowed': False}


def validate(result):
    """Reject common false-closure transformations; no source certification here."""
    t = result['approved_transformation']
    assert t['alternate_retained_rookie'] == 'Saddiq Bey at #22'
    assert t['alternate_sent_rookie'] == 'Zeke Nnaji at #24'
    assert result['scope']['phase'] == 'AFTER_BOTH_HISTORICAL_GORDON_AND_MCGEE_EVENTS'
    assert {r['id'] for r in result['unmeasured_differences']} == {
        'GAMMA_GORDON', 'GAMMA_CLARK', 'DELTA_OTHER'}
    assert all(r['upper'] is None and r['source_verified'] is False
               for r in result['unmeasured_differences'])
    assert result['daily_link']['release_does_not_erase_prior_pay'] is True
    assert result['reported_input_bounds']['historical_ratio_verified'] is False
    assert result['closure_conditions']['historical_same_date_full_apron_bound'] is None
    assert result['complete_domain'] is False and result['source_verified'] is False
    assert result['legal_fields_promoted'] == [] and result['manuscript_allowed'] is False
    return result


def self_test(result):
    mutations = [
        lambda r: r['approved_transformation'].update(alternate_retained_rookie='Zeke Nnaji at #24'),
        lambda r: r['unmeasured_differences'].pop(),
        lambda r: r['unmeasured_differences'][0].update(upper=0, source_verified=True),
        lambda r: r['daily_link'].update(release_does_not_erase_prior_pay=False),
        lambda r: r['closure_conditions'].update(historical_same_date_full_apron_bound=129663831),
        lambda r: r.update(complete_domain=True, source_verified=True, legal_fields_promoted=['DEN_F5_COMPLETE_COST'])]
    for mutation in mutations:
        damaged = deepcopy(result)
        mutation(damaged)
        try:
            validate(damaged)
        except AssertionError:
            continue
        raise AssertionError('false closure accepted')
    return len(mutations)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    result = validate(build())
    if args.check:
        assert json.loads(OUT.read_text(encoding='utf-8')) == result, 'stored comparator differs'
    else:
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    rejected = self_test(result) if args.self_test else 0
    print(json.dumps({'named_base_delta': result['reported_input_bounds']['named_base_delta_interval_usd'],
                      'other_delta_dominance_ceiling': result['closure_conditions']['dominance_if_combined_other_delta_upper_at_most_usd'],
                      'false_closures_rejected': rejected, 'legal_fields_promoted': []}))
