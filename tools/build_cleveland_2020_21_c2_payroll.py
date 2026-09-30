"""A reproducible listed-cost screen; never an exact league payroll clearance."""
import argparse
import json
from decimal import Decimal, ROUND_HALF_UP
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/CLEVELAND_2020_21_C2_PAYROLL_SOURCES.json'
OUT = ROOT / 'simulation/CLEVELAND_2020_21_C2_PAYROLL_SCREEN.json'
DECISIONS = [ROOT / 'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json',
             ROOT / 'canon/CLEVELAND_2021_VAREJAO_C2_DECISION.json']


def build():
    source = json.loads(SOURCE.read_text(encoding='utf-8'))
    f5, c2 = [json.loads(p.read_text(encoding='utf-8')) for p in DECISIONS]
    assert f5['author_response']['F5'] == '거래 생략 (추천)'
    assert c2['selected']['route'] == 'C2_VAREJAO_NO_RETURN_SIGNING'
    rows = source['standard']
    players = {row['player'] for row in rows}
    assert len(rows) == len(players) == 15
    assert 'JaVale McGee' in players
    assert not players.intersection({'Isaiah Hartenstein', 'Anderson Varejao'})
    earlier = source['earlier_obligations']
    assert len({r['id'] for r in earlier}) == len(earlier)
    reported_core = sum(r['reported_cap_hit_usd'] for r in rows)
    likely_in_cap = sum(r['likely_usd'] for r in rows)
    additional_unlikely = sum(r['unlikely_usd'] for r in rows)
    earlier_sum = sum(r['reported_cap_hit_usd'] for r in earlier)
    # Reported cap hits already include the disclosed likely incentives.
    listed = reported_core + additional_unlikely + earlier_sum
    floor = source['kabengele_fa_minimum_apron_screen']
    minimum_amounts = [int((Decimal(floor['annual_two_year_minimum_usd']) * days /
                           floor['season_days']).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
                       for days in floor['contract_days']]
    kab_report = sum(r['reported_cap_hit_usd'] for r in earlier if r['id'].startswith('KABENGELE'))
    kab_report += next(r['reported_cap_hit_usd'] for r in rows if r['player'] == 'Mfiondu Kabengele')
    floor_delta = max(0, sum(minimum_amounts) - kab_report)
    conditional_floor = listed + floor_delta
    drummond = next(r for r in earlier if r['id'] == 'DRUMMOND_BUYOUT')
    no_buyout_saving = drummond['full_previous_annual_usd'] - drummond['reported_cap_hit_usd']
    dell = next(r for r in rows if r['player'] == 'Matthew Dellavedova')
    no_dell_reimbursement = dell['reported_base_usd'] - dell['reported_cap_hit_usd']
    stress = conditional_floor + no_buyout_saving + no_dell_reimbursement
    dated = source['dated_dead_money_comparison']
    assert dated['snapshot_date'] == '2021-04-16'
    ids = dated['comparable_obligation_ids']
    expected = {'DRUMMOND_BUYOUT', 'JR_STRETCH', 'COOK_1', 'COOK_2',
                'MAKER_WAIVED', 'TUCKER_WAIVED', 'FERRELL_HARDSHIP'}
    assert len(ids) == len(set(ids)) == 7 and set(ids) == expected
    assert set(dated['comparison_rows_usd']) == expected
    selected = [r for r in earlier if r['id'] in expected]
    assert len(selected) == 7
    assert all(r['date'] <= dated['snapshot_date'] for r in selected if 'date' in r)
    reported_subtotal = sum(r['reported_cap_hit_usd'] for r in selected)
    comparison_subtotal = sum(dated['comparison_rows_usd'].values())
    changes = {r['id']: dated['comparison_rows_usd'][r['id']] - r['reported_cap_hit_usd']
               for r in selected if dated['comparison_rows_usd'][r['id']] != r['reported_cap_hit_usd']}
    dated_result = dict(snapshot_date=dated['snapshot_date'], comparable_obligation_count=7,
                        existing_reported_subtotal_usd=reported_subtotal,
                        alternate_reported_subtotal_usd=comparison_subtotal,
                        article_team_total_usd=dated['reported_team_dead_money_usd'],
                        alternate_rows_minus_article_usd=comparison_subtotal - dated['reported_team_dead_money_usd'],
                        article_minus_existing_rows_usd=dated['reported_team_dead_money_usd'] - reported_subtotal,
                        row_deltas_usd=changes,
                        classification=dated['comparison_classification'],
                        legal_attribution_verified=False, complete_domain=False)
    # A fourth sensitivity uses the two other reported rows; it is not an upper bound.
    alternate_rows_stress = stress + sum(changes.values())
    comparison = source['comparison_only']
    mcgee = next(r for r in rows if r['player'] == 'JaVale McGee')
    difference = (mcgee['reported_cap_hit_usd'] - comparison['hartenstein_reported_cap_usd'] -
                  comparison['varejao_conditional_cap_usd'])
    cases = []
    for name, amount in [('REPORTED_LIST_PLUS_ALL_DISCLOSED_BONUS', listed),
                         ('PLUS_CONDITIONAL_KABENGELE_FA_FLOOR', conditional_floor),
                         ('NO_DRUMMOND_BUYOUT_SAVING_NO_DELL_REIMBURSEMENT_STRESS', stress),
                         ('PLUS_ALTERNATE_REPORTED_MAKER_FERRELL_ROWS_NOT_UPPER_BOUND', alternate_rows_stress)]:
        cases.append(dict(case=name, listed_budget_usd=amount,
                          tax_reference_gap_usd=source['limits']['tax_usd'] - amount,
                          apron_reference_gap_usd=source['limits']['apron_usd'] - amount,
                          actual_tax_compliance=None, actual_apron_compliance=None))
    return dict(stage='CLEVELAND_C2_LISTED_COST_SCREEN', baseline_main=source['baseline_main'],
                classification='CONDITIONAL_PUBLIC_INPUT_ARITHMETIC_NOT_COMPLETE_BOUND',
                standard_count=15, reported_core_cap_sum_usd=reported_core,
                disclosed_likely_already_in_core_usd=likely_in_cap,
                additional_unlikely_stress_usd=additional_unlikely,
                listed_earlier_obligation_usd=earlier_sum,
                kabengele_conditional_floor_contract_amounts_usd=minimum_amounts,
                kabengele_conditional_floor_delta_usd=floor_delta,
                no_buyout_saving_stress_delta_usd=no_buyout_saving,
                no_dell_reimbursement_stress_delta_usd=no_dell_reimbursement,
                dated_dead_money_comparison=dated_result,
                c2_minus_reported_original_same_other_inputs_usd=difference,
                cases=cases, unresolved=source['unresolved'],
                actual_residual_usd=None, exact_team_salary_usd=None,
                exact_execution_cleared=False, season_selected=False, manuscript_allowed=False,
                source_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
                               for p in [SOURCE] + DECISIONS})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text(encoding='utf-8') == rendered, 'stale payroll screen'
    else:
        OUT.write_text(rendered, encoding='utf-8')
    print(json.dumps({'cases':result['cases'], 'residual':result['actual_residual_usd']}, ensure_ascii=False))
