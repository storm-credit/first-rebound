import copy
import unittest

import build_orlando_2020_21_registration_ledger as ledger


class RegistrationLedgerTest(unittest.TestCase):
    def test_inactive_and_zero_minutes_do_not_free_a_slot(self):
        r = ledger.roster_on('2021-05-09')
        self.assertEqual((r['standard_count'], r['two_way_count']), (16, 2))
        self.assertIn('Al-Farouq Aminu', r['standard'])
        self.assertFalse(r['ordinary_count_pass'])
        self.assertEqual(r['extra_standard_slots_needed'], 1)

    def test_cannady_changes_contract_class_not_two_simultaneous_slots(self):
        for date, standard, two_way in [('2021-04-12', True, False),
                                       ('2021-04-13', False, False),
                                       ('2021-04-16', False, True),
                                       ('2021-05-04', False, False)]:
            r = ledger.roster_on(date)
            self.assertEqual('Devin Cannady' in r['standard'], standard)
            self.assertEqual('Devin Cannady' in r['two_way'], two_way)

    def test_substitutions_and_hall_gap(self):
        for date in ['2021-05-02', '2021-05-08']:
            self.assertNotIn('Donta Hall', ledger.roster_on(date)['standard'])
        self.assertNotIn('Robert Franks', ledger.roster_on('2021-04-27')['standard'])
        self.assertIn('Moritz Wagner', ledger.roster_on('2021-04-27')['standard'])
        self.assertEqual(ledger.roster_on('2021-05-11')['standard'],
                         ledger.roster_on('2021-05-12')['standard'])

    def test_missing_continuation_is_detected(self):
        contracts = [c for c in ledger.intervals() if c['source'] != 'LR_BRAZ_ROS']
        self.assertIn('Ignas Brazdeikis', ledger.roster_on('2021-05-11', contracts)['standard'])
        self.assertNotIn('Ignas Brazdeikis', ledger.roster_on('2021-05-12', contracts)['standard'])
        duplicate = ledger.intervals() + [ledger.intervals()[0]]
        with self.assertRaises(AssertionError):
            ledger.roster_on('2021-05-09', duplicate)

    def test_existing_minutes_and_rivers_continuation(self):
        d = ledger.build()
        self.assertEqual(len(d['extra_slot_game_ids']), 5)
        positive = [r for r in d['rivers_date_checks'] if r['positive']]
        self.assertEqual(len(positive), 15)
        self.assertEqual({r['contract_window'] for r in positive}, {'TEN_DAY', 'REST_OF_SEASON'})
        self.assertFalse(any(r['unregistered_positive_players'] for r in d['orl_game_checks']))

    def test_count_pass_cannot_become_execution_or_author_approval(self):
        good = ledger.build()
        for path in [('author_locked',), ('season_selected',), ('manuscript_allowed',),
                     ('salary_route', 'exact_charge_cleared')]:
            bad = copy.deepcopy(good)
            target = bad
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = True
            with self.assertRaises(AssertionError):
                ledger.validate(bad)
        bad = copy.deepcopy(good)
        bad['epochs'][-1]['registration_cleared'] = True
        with self.assertRaises(AssertionError):
            ledger.validate(bad)


if __name__ == '__main__':
    unittest.main()
