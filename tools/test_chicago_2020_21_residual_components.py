import copy
import json
import unittest

import build_chicago_2020_21_residual_components as b


class ResidualTests(unittest.TestCase):
    def setUp(self):
        self.source = json.loads(b.SOURCE.read_text())
        self.bound = json.loads(b.BOUND.read_text())

    def test_signing_date_and_route_are_required(self):
        e = self.source['fa_events'][0]
        self.assertIsNone(b.previous_team_fa_amount(e, '2020-11-27', True))
        self.assertEqual(b.previous_team_fa_amount(e, '2020-11-28', True), 0)
        self.assertIsNone(b.previous_team_fa_amount(e, '2021-03-25', False))
        self.assertIsNone(b.previous_team_fa_amount({**e, 'source_id': None}, '2021-03-25', True))

    def test_fa_exclusion_never_removes_dead_pay_or_increases_margin(self):
        r = b.build(self.source, self.bound)
        self.assertTrue(all(x['conditional_previous_team_fa_amount_usd'] == 0 for x in r['fa_rows']))
        self.assertTrue(all(not x['waived_salary_excluded_by_this_result'] for x in r['fa_rows']))
        self.assertEqual(r['retained_prior_residual_limit_usd'], 5609972)
        self.assertEqual(r['deduction_from_prior_known_salary_usd'], 0)
        self.assertIsNone(r['exact_residual_charge_usd'])
        self.assertIsNone(r['actual_non_tax_status'])
        changed = copy.deepcopy(self.source)
        for x in changed['unresolved_components']:
            x['amount_usd'] = 0
        self.assertFalse(b.build(changed, self.bound)['complete_residual_inventory_verified'])

    def test_incomplete_roster_and_source_integrity(self):
        changed = copy.deepcopy(self.source)
        changed['conditions']['standard_roster_count'] = 11
        self.assertEqual(b.build(changed, self.bound)['incomplete_roster_charge_usd'], 0)
        changed['conditions']['season_started'] = False
        self.assertIsNone(b.build(changed, self.bound)['incomplete_roster_charge_usd'])
        changed['fa_events'][0]['source_id'] = 'NONEXISTENT'
        with self.assertRaises(AssertionError):
            b.build(changed, self.bound)


if __name__ == '__main__':
    unittest.main()
