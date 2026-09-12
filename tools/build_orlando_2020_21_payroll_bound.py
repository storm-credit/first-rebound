"""Bound listed Orlando commitments; do not certify a complete NBA cap ledger."""
import json
from hashlib import sha256
from pathlib import Path

from build_nba_2020_21_registration_costs import inclusive_days, prorate

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/ORLANDO_2020_21_PAYROLL_SOURCES.json'
COSTS = ROOT / 'simulation/NBA_2020_21_REGISTRATION_COSTS.json'
LEDGER = ROOT / 'simulation/ORLANDO_2020_21_REGISTRATION_LEDGER.json'
OUT = ROOT / 'simulation/ORLANDO_2020_21_PAYROLL_BOUND.json'


def apron_contract(row, source):
    days = inclusive_days(row['pay_start'], row['pay_end'])
    # Paid contract period, including guaranteed pay after a roster release.
    floor = prorate(source['minimum_annual_usd']['2'], days, source['season_days'])
    ordinary = row['ordinary_minimum_charge_usd']
    adjusted = max(ordinary, floor) if row['entry_years_of_service'] < 2 else ordinary
    return {**row, 'pay_days': days, 'apron_budget_usd': adjusted,
            'young_free_agent_adjustment_usd': adjusted - ordinary,
            'exact_alternate_apron_charge_usd': None}


def residual_fits(budget, residual, apron):
    return None if residual is None else budget + residual <= apron


def build(source=None, costs=None, ledger=None):
    source = json.loads(SOURCE.read_text()) if source is None else source
    costs = json.loads(COSTS.read_text()) if costs is None else costs
    ledger = json.loads(LEDGER.read_text()) if ledger is None else ledger
    reference_paths = [ROOT / p for p in source['existing_reference_files']]
    ids = {r['id'] for r in source['references']}
    assert len(ids) == len(source['references'])
    ids |= {r['id'] for p in reference_paths for r in json.loads(p.read_text())['references']}
    core = source['core_players']
    expected_core = {r['player'] for r in ledger['contracts']
                     if r['source'] == 'CONDITIONAL_CARRY_FORWARD_BASELINE' and r['type'] == 'STANDARD'}
    assert len(core) == len({r['player'] for r in core}) == len(expected_core)
    assert {r['player'] for r in core} == expected_core
    imported = [r for r in costs['rows'] if r['team'] == 'ORL']
    short = source['earlier_short_contracts'] + imported
    assert len(short) == len({r['id'] for r in short})
    assert all(r.get('source_id') in ids for r in core if r['player'] != 'Zeke Nnaji')
    assert all(r['source_id'] in ids for r in short + source['previous_contract_budgets'] + source['camp_stress'])
    assert all(prorate(source['minimum_annual_usd'][str(r['entry_years_of_service'])],
                       inclusive_days(r['pay_start'], r['pay_end']), source['season_days'])
               == r['reported_pay_usd'] for r in short)
    rows = sorted([apron_contract(r, source) for r in short], key=lambda r: (r['pay_start'], r['id']))
    base = sum(r['base_usd'] for r in core)
    bonus = sum(r['reported_likely_usd'] + r['reported_unlikely_usd'] for r in core)
    previous = sum(r['budget_usd'] for r in source['previous_contract_budgets'])
    camp = sum(r['annual_base_usd'] for r in source['camp_stress'])
    apron = source['thresholds']['apron_usd']
    epochs = []
    dates = sorted({'2021-04-12'} | {r['pay_start'] for r in rows if r['pay_start'] >= '2021-04-12'})
    for day in dates:
        signed = [r for r in rows if r['pay_start'] <= day]
        amount = base + bonus + previous + sum(r['apron_budget_usd'] for r in signed)
        epochs.append({'date': day, 'signed_short_contract_ids': [r['id'] for r in signed],
                       'listed_apron_budget_usd': amount,
                       'with_camp_full_annual_stress_usd': amount + camp,
                       'residual_allowance_with_camp_stress_usd': apron - amount - camp})
    peak = max(epochs, key=lambda e: e['with_camp_full_annual_stress_usd'])
    paths = [SOURCE, COSTS, LEDGER] + reference_paths
    return {
        'stage': 'O-15F14-L_ORLANDO_PAYROLL_BOUND',
        'baseline_main': '9ed8b288c2d664133efaace05f3bd3f37db3ba51',
        'classification': 'LISTED_COMMITMENT_BOUND_NOT_COMPLETE_TEAM_CLEARANCE',
        'scope': {'start': '2021-04-12', 'end': '2021-05-16',
                  'basis': 'CUMULATIVE_CONTRACT_COMMITMENTS_NOT_CASH_PAID_TO_DATE',
                  'checks_trade_day_or_pre_april_hard_cap': False},
        'core_players': core, 'core_base_usd': base, 'all_disclosed_core_bonus_usd': bonus,
        'short_contracts': rows,
        'short_ordinary_budget_usd': sum(r['ordinary_minimum_charge_usd'] for r in rows),
        'short_apron_budget_usd': sum(r['apron_budget_usd'] for r in rows),
        'young_fa_apron_adjustment_usd': sum(r['young_free_agent_adjustment_usd'] for r in rows),
        'previous_contract_budgets': source['previous_contract_budgets'],
        'previous_contract_budget_total_usd': previous,
        'camp_full_annual_stress_usd': camp, 'camp_stress_is_actual_charge_or_complete_upper_bound': False,
        'epochs': epochs, 'peak': peak, 'thresholds': source['thresholds'],
        'residual_actual_usd': None,
        'exact_team_apron_charge_usd': None,
        'actual_apron_compliance': residual_fits(peak['with_camp_full_annual_stress_usd'], None, apron),
        'complete_component_inventory_verified': False,
        'hard_cap_trigger_verified': False,
        'mle_history': source['mle_history'],
        'mle_used_before_trade_usd': sum(r['usd'] for r in source['mle_history']['reported_uses']),
        'mle_used_after_clark_trade_usd': sum(r['usd'] for r in source['mle_history']['reported_uses']),
        'hall_zero_charge_required_for_budget': False,
        'hall_extra_slot_game_ids': ledger['extra_slot_game_ids'],
        'alternate_hardship_approved': False,
        'requirements_closed': 0, 'author_locked': False, 'season_selected': False,
        'manuscript_allowed': False, 'independent_review': 'NOT_INDEPENDENT',
        'unresolved': source['remaining_ko'],
        'source_sha256': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
    }


if __name__ == '__main__':
    result = build()
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'PASS': result['peak']['residual_allowance_with_camp_stress_usd'] >= 0,
                      'core_players': len(result['core_players']),
                      'short_contracts': len(result['short_contracts']),
                      'epochs': len(result['epochs']),
                      'residual_allowance_usd': result['peak']['residual_allowance_with_camp_stress_usd'],
                      'actual_apron_compliance': result['actual_apron_compliance']}))
