import copy
import unittest
from fractions import Fraction

import build_chicago_2020_21_execution_terms as t


class ExecutionTermsTest(unittest.TestCase):
    def test_hardship_requires_four_standard_absences_not_just_zero_minutes(self):
        sources, reg, lineups = [t.json.loads(p.read_text()) for p in t.INPUTS]
        good = t.hardship_evidence(sources, reg, lineups)
        self.assertTrue(good['documentary_absence_prerequisite_supported'])
        sources['final_box_absences'][0]['did_play'] = True
        self.assertFalse(t.hardship_evidence(sources, reg, lineups)['documentary_absence_prerequisite_supported'])

    def test_three_games_must_be_immediately_before_hall_return(self):
        sources, reg, lineups = [t.json.loads(p.read_text()) for p in t.INPUTS]
        row = next(r for r in lineups['rows'] if r['event_id'][:10] == '2021-05-07')
        row['control_minutes']['Terrence Ross'] = 1
        self.assertFalse(t.hardship_evidence(sources, reg, lineups)['documentary_absence_prerequisite_supported'])

    def test_tax_status_is_material_to_chicago(self):
        self.assertEqual(t.allowance(3767981, False) - 6517981, Fraction(703943, 4))
        self.assertEqual(t.allowance(3767981, True) - 6517981, Fraction(-6832019, 4))
        self.assertEqual(t.allowance(10000000, False), 15000000)

    def test_gordon_known_bonus_stress_and_no_outgoing_bonus_credit(self):
        rows = t.build()['gordon_matching']
        worst = {r['team']: r for r in rows if r['mode'].endswith('STRESS')}
        self.assertEqual(worst['ORL']['margin_usd'], 1382928)
        self.assertEqual(worst['DEN']['margin_usd'], 5656378.5)
        self.assertFalse(any(r['outgoing_incentive_credit_taken'] for r in rows))

    def test_cash_tpe_and_draft_terms_do_not_fill_unknown_fields(self):
        d = t.build()
        self.assertEqual(d['Hall_cash']['ORL_reported_contract_total_usd'], 277256)
        self.assertIsNone(d['Hall_cash']['exact_team_charge_usd'])
        self.assertEqual([r['remaining_usd'] for r in d['Fournier_TPE']['remaining_if_unused_before_trade']],
                         [11500000, 11350000, 11050000])
        self.assertIsNone(d['picks']['public_terms']['den_gordon']['terminal_conversion'])
        self.assertEqual([r['earliest_nonconsecutive_gordon_year_within_reported_window'] for r in
                          d['picks']['conditional_calendar_not_complete_stepien_certification']], [2025, 2026, 2027])

    def test_evidence_cannot_become_commissioner_or_author_approval(self):
        for keys in [('hardship', 'alternate_world_approval_recorded'), ('author_locked',),
                     ('season_selected',), ('manuscript_allowed',), ('Hall_cash', 'reported_zero_cap_hit_adopted')]:
            bad = copy.deepcopy(t.build())
            target = bad
            for key in keys[:-1]:
                target = target[key]
            target[keys[-1]] = True
            with self.assertRaises(AssertionError):
                t.validate(bad)


if __name__ == '__main__':
    unittest.main()
