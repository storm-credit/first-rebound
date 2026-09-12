import copy
import unittest
from fractions import Fraction

import build_chicago_2020_21_execution_closeout as l


class CloseoutTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = l.build()

    def test_rounded_matching_margin_cannot_be_spent(self):
        self.assertEqual(l.matching_margin(), Fraction(703943, 4))
        self.assertEqual(l.matching_margin(extra_incoming='175985.75'), 0)
        self.assertEqual(l.matching_margin(extra_incoming=175986), Fraction(-1, 4))
        self.assertEqual(l.matching_margin(extra_outgoing=1) - l.matching_margin(), Fraction(7, 4))

    def test_registration_boundaries_and_local_date(self):
        for date in ['2021-05-02', '2021-05-03', '2021-05-08']:
            self.assertFalse(l.date_allowed('Donta Hall', date))
        self.assertTrue(l.date_allowed('Donta Hall', '2021-05-09'))
        self.assertFalse(l.date_allowed('Robert Franks', '2021-04-27'))
        self.assertFalse(l.date_allowed('Moritz Wagner', '2021-04-26'))
        self.assertTrue(l.date_allowed('Jabari Parker', '2021-04-16'))

    def test_impossible_date_and_unearned_approval_rejected(self):
        for field in ['author_locked', 'season_selected', 'draw_selected', 'manuscript_allowed']:
            bad = copy.deepcopy(self.data)
            bad[field] = True
            with self.assertRaises(AssertionError):
                l.validate(bad)
        bad = copy.deepcopy(self.data)
        bad['registration_date_checks'][0]['violation'] = True
        with self.assertRaises(AssertionError):
            l.validate(bad)

    def test_two_win_rule_and_no_automatic_pick(self):
        for p in self.data['postseason_proposals']:
            chi_games = [g for g in p['east_games'] if 'CHI' in (g['home'], g['away'])]
            self.assertEqual(chi_games[0]['home'], 'WAS')
            wins = sum(g['winner'] == 'CHI' for g in chi_games)
            self.assertEqual(not p['CHI_in_lottery'], wins == 2)
            self.assertIsNone(p['final_CHI_pick'])
            self.assertIsNone(p['final_MIN_pick'])
        p = next(p for p in self.data['postseason_proposals'] if p['recommended'])
        self.assertEqual([g['winner'] for g in p['east_games']], ['BOS', 'CHI', 'IND'])
        self.assertEqual(p['CHI_record_positions'], [9, 10])
        self.assertEqual(p['MIN_record_positions'], [6, 6])

    def test_field_partition_and_facts_do_not_close_execution(self):
        for p in self.data['postseason_proposals']:
            self.assertEqual(len(set(p['lottery_teams'])), 14)
            self.assertEqual(len(set(p['playoff_teams'])), 16)
        self.assertFalse(any(r['closed'] for r in self.data['requirements']))
        self.assertEqual(self.data['primary_source_bodies'], 6)
        self.assertFalse(self.data['matching']['exact_matching_cleared'])


if __name__ == '__main__':
    unittest.main()
