import copy
import json
import unittest

import build_nba_2020_21_registration_costs as b


class RegistrationCostTests(unittest.TestCase):
    def setUp(self):
        self.source = json.loads(b.SOURCE.read_text())

    def test_nine_reports_and_rounding(self):
        result = b.build(self.source)
        self.assertEqual(result['season_days'], 146)
        self.assertEqual(len(result['rows']), 9)
        self.assertEqual(result['pay_reproduction_mismatches'], 0)
        self.assertEqual(result['ordinary_charge_report_differences'], ['HALL_MAY09'])
        self.assertEqual(b.prorate(1620564, 20, 146), 221995)
        self.assertNotEqual(b.prorate(1620564, 10, 146) * 2, 221995)

    def test_hall_paid_term_survives_early_roster_release(self):
        row = next(r for r in self.source['contracts'] if r['id'] == 'HALL_APR23')
        self.assertEqual(row['registration_end'], '2021-05-01')
        self.assertEqual(b.calculate(row, self.source)['pay_days'], 10)
        self.assertEqual(b.calculate(row, self.source)['calculated_minimum_pay_usd'], 99020)
        changed = {**row, 'pay_end': row['registration_end']}
        self.assertFalse(b.calculate(changed, self.source)['calculated_pay_matches_report'])

    def test_two_year_parker_has_no_one_year_subsidy(self):
        row = next(r for r in self.source['contracts'] if r['id'] == 'PARKER_APR16')
        self.assertEqual(b.calculate(row, self.source)['ordinary_minimum_charge_usd'], 430729)
        changed = {**row, 'contract_seasons': 1}
        self.assertFalse(b.calculate(changed, self.source)['ordinary_charge_matches_report'])
        river = next(r for r in self.source['contracts'] if r['id'] == 'RIVERS_APR30')
        self.assertEqual(b.calculate(river, self.source)['ordinary_minimum_charge_usd'], 188696)

    def test_reported_zero_cannot_approve_registration_or_erase_budget(self):
        result = b.build(self.source)
        self.assertEqual(result['hall_zero_charge']['ordinary_minimum_budget_usd'], 79216)
        self.assertIsNone(result['hall_zero_charge']['alternate_adopted_usd'])
        self.assertFalse(result['hall_zero_charge']['applicable_2020_21_exclusion_basis_verified'])
        self.assertEqual(len(result['registration_constraint']['extra_slot_game_ids']), 5)
        self.assertEqual(result['team_subtotals']['ORL']['ordinary_minimum_charge_budget_usd'], 647781)
        self.assertFalse(any(result[k] for k in ['author_locked', 'season_selected', 'manuscript_allowed', 'requirements_closed']))
        self.assertTrue(all(r['alternate_exact_charge_usd'] is None for r in result['rows']))

    def test_date_service_and_provenance_changes_are_visible(self):
        row = self.source['contracts'][0]
        self.assertFalse(b.calculate({**row, 'entry_years_of_service': 2}, self.source)['calculated_pay_matches_report'])
        changed = copy.deepcopy(self.source)
        changed['contracts'][0]['source_id'] = 'MISSING'
        with self.assertRaises(AssertionError):
            b.build(changed)


if __name__ == '__main__':
    unittest.main()
