"""Separate conditional FA-hold exclusions from unresolved retained salary."""
import json
from datetime import date
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/CHICAGO_2020_21_RESIDUAL_SOURCES.json'
BOUND = ROOT / 'simulation/CHICAGO_2020_21_TAX_BOUND.json'
OUT = ROOT / 'simulation/CHICAGO_2020_21_RESIDUAL_COMPONENTS.json'


def previous_team_fa_amount(event, as_of, same_route):
    if not same_route or not event.get('source_id'):
        return None
    if date.fromisoformat(event['signed_date']) > date.fromisoformat(as_of):
        return None
    return 0


def build(source, bound):
    assert source['author_locked'] is False
    assert source['season_selected'] is False
    assert source['manuscript_allowed'] is False
    refs = {r['id'] for r in source['references']}
    conditions = source['conditions']
    rows = []
    for event in source['fa_events']:
        assert event['source_id'] in refs
        rows.append({**event, 'conditional_previous_team_fa_amount_usd':
                     previous_team_fa_amount(event, source['as_of'],
                                             conditions['same_external_signing_routes']),
                     'waived_salary_excluded_by_this_result': False})
    assert len({r['player'] for r in rows}) == len(rows)
    unresolved = source['unresolved_components']
    assert len({r['id'] for r in unresolved}) == len(unresolved)
    # This file classifies a partial inventory, never certifies a complete ledger.
    return {
        'stage': source['stage'], 'baseline_main': source['baseline_main'],
        'as_of': source['as_of'], 'conditions': conditions,
        'fa_rows': rows,
        'incomplete_roster_charge_usd': 0 if conditions['season_started'] or
            conditions['standard_roster_count'] >= 12 else None,
        'unresolved_components': unresolved,
        'complete_residual_inventory_verified': False,
        'exact_residual_charge_usd': None, 'actual_non_tax_status': None,
        'retained_prior_residual_limit_usd': bound['max_residual_for_all_tested_cases_usd'],
        'deduction_from_prior_known_salary_usd': 0,
        'explanation': 'Excluded holds were not included in the prior known salary; do not subtract them again.',
        'exact_trade_cleared': False, 'requirements_closed': 0,
        'author_locked': False, 'season_selected': False,
        'manuscript_allowed': False, 'review': 'NOT_INDEPENDENT',
    }


def main():
    result = build(json.loads(SOURCE.read_text()), json.loads(BOUND.read_text()))
    result['input_sha256'] = {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                              for p in (SOURCE, BOUND)}
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'PASS': True, 'conditional_fa_rows': len(result['fa_rows']),
                      'complete_residual_inventory_verified': False,
                      'actual_non_tax_status': None}))


if __name__ == '__main__':
    main()
