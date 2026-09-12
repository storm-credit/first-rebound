import copy
import json
import unittest

from build_orlando_2020_21_payroll_bound import SOURCE, build, residual_fits


class OrlandoPayrollTests(unittest.TestCase):
    def test_roster_and_contracts_do_not_drop_inactive_or_expired_pay(self):
        result = build()
        self.assertEqual(len(result['core_players']), 13)
        self.assertEqual(result['core_base_usd'], 110880451)
        self.assertIn('Al-Farouq Aminu', {r['player'] for r in result['core_players']})
        self.assertEqual(len(result['short_contracts']), 9)
        final_ids = result['peak']['signed_short_contract_ids']
        self.assertTrue({'CANNADY_APR06', 'FRANKS_APR22', 'HALL_APR23'} <= set(final_ids))
        source = json.loads(SOURCE.read_text())
        source['core_players'].pop(1)
        with self.assertRaises(AssertionError):
            build(source=source)

    def test_young_fa_floor_and_contract_level_rounding(self):
        rows = {r['id']: r for r in build()['short_contracts']}
        self.assertEqual(rows['CANNADY_APR06']['ordinary_minimum_charge_usd'], 61528)
        self.assertEqual(rows['CANNADY_APR06']['apron_budget_usd'], 110998)
        self.assertEqual(rows['FRANKS_APR22']['pay_days'], 10)
        self.assertEqual(rows['FRANKS_APR22']['apron_budget_usd'], 110998)
        self.assertEqual(rows['HALL_APR23']['pay_end'], '2021-05-02')
        self.assertEqual(rows['WAGNER_APR27']['apron_budget_usd'], 221995)
        self.assertNotEqual(rows['WAGNER_APR27']['apron_budget_usd'], 2 * 110998)
        self.assertGreater(rows['HALL_MAY09']['apron_budget_usd'], 79216)

    def test_margin_boundary_is_conditional_not_clearance(self):
        r = build()
        budget = r['peak']['with_camp_full_annual_stress_usd']
        margin = r['peak']['residual_allowance_with_camp_stress_usd']
        apron = r['thresholds']['apron_usd']
        self.assertTrue(residual_fits(budget, margin, apron))
        self.assertFalse(residual_fits(budget, margin + 1, apron))
        self.assertIsNone(r['actual_apron_compliance'])
        self.assertFalse(r['complete_component_inventory_verified'])
        self.assertEqual(r['camp_full_annual_stress_usd'], 4140627)
        self.assertTrue(all(not r[k] for k in ['author_locked', 'season_selected', 'manuscript_allowed', 'alternate_hardship_approved']))
        self.assertEqual(len(r['hall_extra_slot_game_ids']), 5)

    def test_previous_pay_and_mle_are_not_refunded_or_double_counted(self):
        r = build()
        old = {x['id']: x for x in r['previous_contract_budgets']}
        self.assertEqual(old['BIRCH_PRIOR']['budget_usd'], 3000000)
        self.assertEqual(old['TEAGUE_PRIOR']['budget_usd'], 1620564)
        self.assertEqual(r['mle_used_before_trade_usd'], 5300000)
        self.assertEqual(r['mle_used_after_clark_trade_usd'], 5300000)
        self.assertEqual(r['mle_history']['michael_carter_williams_method'], 'EARLY_BIRD')
        self.assertFalse(r['mle_history']['unused_april_capacity_calculated'])

    def test_duplicate_contract_and_unknown_source_rejected(self):
        source = json.loads(SOURCE.read_text())
        duplicate = copy.deepcopy(source)
        duplicate['earlier_short_contracts'].append(duplicate['earlier_short_contracts'][0])
        with self.assertRaises(AssertionError):
            build(source=duplicate)
        source['core_players'][0]['source_id'] = 'UNVERIFIED_SOURCE'
        with self.assertRaises(AssertionError):
            build(source=source)


if __name__ == '__main__':
    unittest.main()
