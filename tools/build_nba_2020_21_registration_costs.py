"""Reproduce reported late-season pay, keeping roster permission separate."""
import json
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/NBA_2020_21_REGISTRATION_COST_SOURCES.json'
LEDGER = ROOT / 'simulation/ORLANDO_2020_21_REGISTRATION_LEDGER.json'
OUT = ROOT / 'simulation/NBA_2020_21_REGISTRATION_COSTS.json'


def inclusive_days(start, end):
    days = (date.fromisoformat(end) - date.fromisoformat(start)).days + 1
    assert days > 0
    return days


def prorate(annual, days, season_days):
    assert annual >= 0 and 0 < days <= season_days
    return int((Decimal(annual) * days / season_days).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def calculate(row, source):
    season_days = inclusive_days(source['season']['start'], source['season']['end'])
    days = inclusive_days(row['pay_start'], row['pay_end'])
    annual = source['minimum_annual_usd'][str(row['entry_years_of_service'])]
    # Registration termination does not rewrite the contracted compensation period.
    compensation = prorate(annual, days, season_days)
    subsidized = row['contract_seasons'] == 1 and row['entry_years_of_service'] >= 3
    charge_annual = source['minimum_annual_usd']['2'] if subsidized else annual
    ordinary_charge = prorate(charge_annual, days, season_days)
    return {**row, 'pay_days': days, 'calculated_minimum_pay_usd': compensation,
            'one_year_veteran_reimbursement_rule_applies': subsidized,
            'ordinary_minimum_charge_usd': ordinary_charge,
            'calculated_pay_matches_report': compensation == row['reported_pay_usd'],
            'ordinary_charge_matches_report': ordinary_charge == row['reported_cap_hit_usd'],
            'reported_cap_minus_ordinary_usd': row['reported_cap_hit_usd'] - ordinary_charge,
            'alternate_exact_charge_usd': None,
            'registration_permission_granted_by_this_calculation': False}


def build(source=None, ledger=None):
    source = json.loads(SOURCE.read_text()) if source is None else source
    ledger = json.loads(LEDGER.read_text()) if ledger is None else ledger
    ids = {r['id'] for r in source['references']}
    assert len(ids) == len(source['references'])
    assert all(r['source_id'] in ids for r in source['contracts'])
    event_paths = [ROOT / p for p in source['existing_event_source_files']]
    event_ids = {r['id'] for p in event_paths for r in json.loads(p.read_text())['references']}
    assert all(r['existing_event_source_id'] in event_ids for r in source['contracts'])
    assert len({r['id'] for r in source['contracts']}) == len(source['contracts'])
    rows = [calculate(r, source) for r in source['contracts']]
    totals = {}
    for team in sorted({r['team'] for r in rows}):
        team_rows = [r for r in rows if r['team'] == team]
        totals[team] = {
            'reported_player_pay_usd': sum(r['reported_pay_usd'] for r in team_rows),
            'reported_cap_hit_sum_usd': sum(r['reported_cap_hit_usd'] for r in team_rows),
            'ordinary_minimum_charge_budget_usd': sum(r['ordinary_minimum_charge_usd'] for r in team_rows),
            'scope': 'LISTED_NEW_CONTRACTS_ONLY_NOT_TEAM_PAYROLL',
            'team_limit_cleared': False,
        }
    hall = next(r for r in rows if r['id'] == 'HALL_MAY09')
    assert hall['reported_cap_hit_usd'] == 0
    return {
        'stage': 'O-15F14-L_REGISTRATION_COSTS',
        'baseline_main': '9bbcf7138ca86325f19ad4c85096bc0d7f663ead',
        'classification': 'PUBLIC_REPORTS_REPRODUCED_NOT_ALTERNATE_CONTRACT_APPROVAL',
        'season_days': inclusive_days(source['season']['start'], source['season']['end']),
        'rows': rows, 'team_subtotals': totals,
        'hall_zero_charge': {
            'reported_usd': hall['reported_cap_hit_usd'],
            'ordinary_minimum_budget_usd': hall['ordinary_minimum_charge_usd'],
            'applicable_2020_21_exclusion_basis_verified': False,
            'alternate_adopted_usd': None,
            'zero_is_required_for_proposed_budget': False,
        },
        'registration_constraint': {
            'extra_slot_game_ids': ledger['extra_slot_game_ids'],
            'alternate_hardship_approved': False,
        },
        'unresolved': source['unresolved'],
        'pay_reproduction_mismatches': sum(not r['calculated_pay_matches_report'] for r in rows),
        'ordinary_charge_report_differences': [r['id'] for r in rows if not r['ordinary_charge_matches_report']],
        'requirements_closed': 0, 'author_locked': False, 'season_selected': False,
        'manuscript_allowed': False, 'independent_review': 'NOT_INDEPENDENT',
        'source_sha256': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in [SOURCE, LEDGER] + event_paths},
    }


if __name__ == '__main__':
    result = build()
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'PASS': result['pay_reproduction_mismatches'] == 0,
                      'contract_rows': len(result['rows']),
                      'pay_mismatches': result['pay_reproduction_mismatches'],
                      'ordinary_charge_differences': result['ordinary_charge_report_differences'],
                      'registration_cleared': False}))
