import copy
import csv
import json
import unittest
from fractions import Fraction

import build_chicago_2020_21_tax_bound as b


class TaxBoundTests(unittest.TestCase):
    def setUp(self):
        self.sources = json.loads(b.SOURCES.read_text())
        self.prior = json.loads(b.PRIOR.read_text())
        with b.ROSTER.open() as f:
            self.roster = list(csv.DictReader(f))

    def run_build(self):
        return b.build(self.sources, self.prior, self.roster)

    def test_full_roster_and_bonus_envelope(self):
        d = self.run_build()
        self.assertEqual(d['known_base_excluding_protagonist_usd'], 122812428)
        self.assertEqual(d['trade_net_salary_increase_usd'], 2750000)
        self.assertEqual(d['rookie_envelope_usd'], [1325520, 3204600])
        self.assertEqual(d['max_residual_for_all_tested_cases_usd'], 5609972)
        self.assertEqual(len(d['cases']), 60)
        self.assertEqual(d['matching_margin_if_non_tax_confirmed_usd'], 175985.75)
        self.assertEqual(d['matching_margin_if_taxpayer_usd'], -1708004.75)

    def test_tax_boundary_and_unmeasured_residual(self):
        self.assertTrue(b.non_tax_test(127017028, 5609972, 132627000))
        self.assertFalse(b.non_tax_test(127017028, Fraction(560997201, 100), 132627000))
        self.assertIsNone(b.non_tax_test(127017028, None, 132627000))
        with self.assertRaises(ValueError):
            b.non_tax_test(127017028, -1, 132627000)

    def test_bonus_increase_reduces_headroom(self):
        self.sources['salary_rows'][-1]['reported_unlikely_usd'] += 1000000
        self.assertEqual(self.run_build()['max_residual_for_all_tested_cases_usd'], 4609972)

    def test_no_missing_or_double_counted_standard_player(self):
        original = copy.deepcopy(self.roster)
        self.roster = [r for r in original if r['player'] != 'Otto Porter Jr.']
        with self.assertRaises(AssertionError):
            self.run_build()
        self.roster = original + [original[0]]
        with self.assertRaises(AssertionError):
            self.run_build()

    def test_wrong_rookie_season_or_unearned_adoption_rejected(self):
        original = copy.deepcopy(self.sources)
        self.sources['rookie_envelope']['contract_first_season'] = '2020-21'
        with self.assertRaises(AssertionError):
            self.run_build()
        self.sources = original
        self.sources['rookie_envelope']['author_pick'] = 22
        with self.assertRaises(AssertionError):
            self.run_build()

    def test_stress_is_not_observed_charge_or_author_approval(self):
        d = self.run_build()
        self.assertEqual(d['camp_full_face_value_stress']['remaining_margin_usd'], 1237371)
        self.assertFalse(d['camp_full_face_value_stress']['complete_residual_bound'])
        self.assertIsNone(d['exact_residual_charge_usd'])
        self.assertIsNone(d['actual_non_tax_status'])
        self.assertFalse(d['exact_trade_cleared'])
        self.assertFalse(d['season_selected'])
        self.assertFalse(d['author_locked'])
        self.assertFalse(d['manuscript_allowed'])


if __name__ == '__main__':
    unittest.main()
