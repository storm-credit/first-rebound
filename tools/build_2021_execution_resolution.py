"""Evaluate reported pick terms and funding alternatives without choosing outcomes."""
import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/NBA_2021_EXECUTION_RESOLUTION_SOURCES.json'
OUT = ROOT / 'simulation/NBA_2021_EXECUTION_RESOLUTION.json'


def gordon_after_first_delivery(predecessor_year, slots, terms):
    if predecessor_year is None:
        return dict(status='PREDECESSOR_LINK_UNRESOLVED', asset=None)
    if type(predecessor_year) is not int or predecessor_year not in (2023, 2024, 2025):
        raise ValueError('Expected actual preceding first-round delivery year, not conversion')
    first = max(terms['first_year'], predecessor_year + 2)
    for year in range(first, terms['last_year'] + 1):
        pick = slots.get(year)
        if pick is None:
            return dict(status='WAIT_FOR_OUTCOME', year=year, asset=None)
        if type(pick) is not int or not 1 <= pick <= 30:
            raise ValueError('Need final first-round slot')
        if pick > terms['protected_through']:
            return dict(status='CONDITIONAL_DELIVERY', year=year,
                        asset=dict(origin='DEN', round=1, year=year, pick=pick))
    return dict(status='CONDITIONAL_REPORTED_EXTINCTION', year=terms['last_year'], asset=None)


def mcgee_second(year, pick, terms):
    if year not in (2023, 2027):
        raise ValueError('Not an asset in this trade')
    if pick is None:
        return dict(status='WAIT_FOR_OUTCOME', asset=None)
    if type(pick) is not int or not 31 <= pick <= 60:
        raise ValueError('Need final second-round slot')
    if year == 2023 and pick <= terms['second_2023_protected_through']:
        return dict(status='PROTECTED_TERMINAL_UNRESOLVED', asset=None)
    return dict(status='CONDITIONAL_DELIVERY', asset=dict(origin='DEN', round=2, year=year, pick=pick))


def funding(terms):
    # Most permissive low-salary matching case. A failure also fails the tax case.
    allowance = Fraction(7, 4) * terms['hartenstein_test_charge_usd'] + 100000
    incoming = terms['mcgee_test_charge_usd']
    nominal = terms['reported_grant_tpe_nominal_usd']
    exact = terms['exact_available_grant_tpe_usd']
    return dict(simple_175_allowance_usd=float(allowance), incoming_test_usd=incoming,
                simple_matching_pass=incoming <= allowance,
                shortfall_usd=float(incoming - allowance),
                reported_nominal_tpe_margin_usd=nominal-incoming,
                exact_tpe_full_charge_coverage=None if exact is None else exact >= incoming,
                hartenstein_not_added_to_grant_tpe=True, gordon_not_pooled=True,
                cba_additional_trade_tolerance_not_used=True, complete_trade_legality=None)


def build():
    s = json.loads(SOURCE.read_text())
    assert not any(s[k] for k in ('author_locked', 'season_selected', 'manuscript_allowed'))
    assert not s['gordon']['terms_adopted'] and not s['mcgee']['terms_adopted']
    examples = [(2023,{2025:6}), (2023,{2025:5,2026:5,2027:5}),
                (2024,{2026:6}), (2025,{2027:6}), (2025,{2027:5}), (None,{})]
    return dict(stage=s['stage'], baseline_main=s['baseline_main'],
                reported_gordon_terminal=s['gordon']['reported_terminal'],
                gordon_examples_not_outcomes=[dict(preceding_first_delivery_year=y, test_slots=p,
                    result=gordon_after_first_delivery(y,p,s['gordon'])) for y,p in examples],
                gordon_after_preceding_second_conversion=None,
                selected_gordon_asset=None,
                mcgee_reported_2027_protection=s['mcgee']['second_2027_protection_reported'],
                mcgee_2023_terminal=None, selected_mcgee_assets=None,
                mcgee_funding=funding(s['mcgee']),
                chicago_camp=s['waived_camp'], chicago_actual_residual_usd=None,
                requirements_closed=0, exact_execution_cleared=False,
                author_locked=False, season_selected=False, manuscript_allowed=False,
                review='NOT_INDEPENDENT', input_sha256=sha256(SOURCE.read_bytes()).hexdigest())


if __name__ == '__main__':
    r = build()
    OUT.write_text(json.dumps(r, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(PASS=True, simple_matching_pass=r['mcgee_funding']['simple_matching_pass'],
                         future_assets_selected=0, exact_execution_cleared=False)))
