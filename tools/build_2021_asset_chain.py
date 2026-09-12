"""Resolve reported asset branches; never choose future draft outcomes."""
import json
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/NBA_2021_L_ASSET_CHAIN_SOURCES.json'
PRIOR = ROOT / 'research/NBA_2020_21_L_EXECUTION_TERMS_SOURCES.json'
OUT = ROOT / 'simulation/NBA_2021_ASSET_CHAIN.json'


def split_boston_memphis(bos, mem):
    if bos is None or mem is None:
        return None
    if any(type(p) is not int or not 31 <= p <= 60 for p in (bos, mem)) or bos == mem:
        raise ValueError('Need distinct final second-round slots, not tied records')
    later = ('BOS', bos) if bos > mem else ('MEM', mem)
    earlier = ('MEM', mem) if bos > mem else ('BOS', bos)
    return {'ORL_if_terms_adopted': {'origin': later[0], 'pick': later[1]},
            'BOS_retained_before_other_obligations': {'origin': earlier[0], 'pick': earlier[1]}}


def preceding_denver(slots, terms):
    for year in range(terms['first_year'], terms['last_year'] + 1):
        pick = slots.get(year)
        if pick is None:
            return {'status': 'WAIT_FOR_OUTCOME', 'year': year, 'asset': None}
        if type(pick) is not int or not 1 <= pick <= 30:
            raise ValueError('Need final first-round slot')
        if pick > terms['protected_through_pick']:
            return {'status': 'CONDITIONAL_FIRST_ROUND_DELIVERY', 'year': year,
                    'asset': {'team': 'DEN', 'year': year, 'round': 1, 'pick': pick}}
    return {'status': 'CONDITIONAL_REPORTED_SECOND_ROUND_CONVERSION',
            'year': terms['last_year'], 'asset': terms['reported_terminal_conversion']}


def tpe_remaining(opening, charge, prior_use):
    if prior_use is None:
        return None
    if min(opening, charge, prior_use) < 0:
        raise ValueError('Amounts must be nonnegative')
    return opening - prior_use - charge


def build(source, prior):
    assert not any(source[k] for k in ['author_locked', 'season_selected', 'manuscript_allowed'])
    assert not source['denver_preceding_pick']['alternate_terms_adopted']
    assert prior['public_pick_terms']['fournier']['first_second'] == '2025 less favorable BOS/MEM'
    assert source['gordon_following_pick']['terminal_conversion'] is None
    tpe = source['boston_tpe']
    comparisons = [{'charge_test_usd': c,
                    'balance_if_no_prior_use_usd': tpe_remaining(tpe['opening_usd'], c, 0),
                    'matches_later_snapshot_arithmetically':
                        tpe_remaining(tpe['opening_usd'], c, 0) == tpe['later_reported_balance_usd']}
                   for c in tpe['fournier_test_charges_usd']]
    examples = [{2023: 15}, {2023: 14, 2024: 15},
                {2023: 14, 2024: 14, 2025: 15}, {2023: 14, 2024: 14, 2025: 14}]
    return {
        'stage': source['stage'], 'baseline_main': source['baseline_main'],
        'Boston': {
            'MEM_2025_origin_supported_by_primary_source': True,
            'Bane30_route_already_approved': True,
            'fournier_historical_tpe_use_reported': tpe['used_for_fournier_reported'],
            'tpe_comparisons': comparisons,
            'inferred_consumption_if_same_exception_and_no_other_uses_usd':
                tpe['opening_usd'] - tpe['later_reported_balance_usd'],
            'exact_trade_date_charge_verified': False,
            'exact_alternate_tpe_balance_usd': tpe_remaining(tpe['opening_usd'], 17450000, None),
            'pick_split_examples_not_outcomes': [split_boston_memphis(60, 31), split_boston_memphis(31, 60)],
            'selected_2025_split': split_boston_memphis(None, None),
            'BOS_2027_2R_full_priority_and_terms_verified': False,
        },
        'Denver': {
            'preceding_reported_terminal_conversion': source['denver_preceding_pick']['reported_terminal_conversion'],
            'preceding_examples_not_outcomes': [preceding_denver(s, source['denver_preceding_pick']) for s in examples],
            'selected_preceding_result': preceding_denver({}, source['denver_preceding_pick']),
            'conditional_nonconsecutive_calendar': [{'preceding_delivery_year': y, 'earliest_gordon_test_year': y + 2}
                                                    for y in [2023, 2024, 2025]],
            'gordon_after_preceding_conversion': None,
            'gordon_terminal_conversion': None,
            'complete_stepien_and_ownership_certified': False,
        },
        'author_locked': False, 'season_selected': False, 'manuscript_allowed': False,
        'exact_execution_cleared': False, 'requirements_closed': 0, 'review': 'NOT_INDEPENDENT',
    }


def main():
    source, prior = [json.loads(p.read_text()) for p in [SOURCE, PRIOR]]
    result = build(source, prior)
    result['input_sha256'] = {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in [SOURCE, PRIOR]}
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'PASS': True, 'tpe_comparisons': 3, 'preceding_pick_branches': 4,
                      'selected_future_outcomes': 0, 'exact_execution_cleared': False}))


if __name__ == '__main__':
    main()
