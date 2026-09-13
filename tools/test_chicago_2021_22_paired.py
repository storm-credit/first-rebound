import copy
import json
import math
import unittest

import build_chicago_2021_22_paired as m


class PairedControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = m.load(m.CONFIG)
        cls.source = m.load(m.SOURCE)
        cls.rotations = {r['id']: r for r in cls.config['rotations']}
        cls.report = json.loads(m.build()[m.REPORT])

    def test_all_five_witnesses_and_raw_seconds(self):
        for r in self.rotations.values():
            if r['status'] == 'CONDITIONAL':
                c = m.certify(r)
                self.assertEqual(c['total_minutes'], 240)
                self.assertLessEqual(max(c['player_minutes'].values()), 36)
        self.assertEqual(len(self.report['certificates']), 5)
        self.assertEqual(sorted(h['seconds_residual'] for h in self.report['historical']), [0, 0, 1, 1, 1, 1])

    def test_duplicate_player_rejected(self):
        r = copy.deepcopy(self.rotations['CHI_0022100004'])
        r['lineup_witness'][0]['positions']['SG'] = r['lineup_witness'][0]['positions']['PG']
        with self.assertRaisesRegex(AssertionError, 'Duplicate player'):
            m.certify(r)

    def test_unavailable_recipient_rejected(self):
        r = copy.deepcopy(self.rotations['CHI_0022100878'])
        r['unavailable'].append('Green')
        with self.assertRaisesRegex(AssertionError, 'Unavailable recipient'):
            m.certify(r)

    def test_creator_requirement_is_enforced(self):
        r = copy.deepcopy(self.rotations['SAC_0022100878'])
        r['required_creator_any_of'] = ['Unregistered invented guard']
        with self.assertRaisesRegex(AssertionError, 'Creator coverage'):
            m.certify(r)

    def test_prior_rejects_future_season_and_date(self):
        rows = m.read_csv(m.PREOBS)
        for key, value in [('season', '2021-22'), ('date', '2022-02-16')]:
            bad = copy.deepcopy(rows)
            bad[0][key] = value
            with self.assertRaises(AssertionError):
                m.opponent_priors(bad, self.source['opponent_prior_players'], '2021-10-19')
        p = copy.deepcopy(m.load(m.PREBOOK)['priors']['Buddy Hield'])
        p['source_season'] = '2021-22'
        with self.assertRaises(AssertionError):
            m.rate_from_totals(p)

    def test_missing_rookie_prior_is_not_zero(self):
        r = self.rotations['DET_0022100004']
        cert = m.certify(r)
        rates = {p: m.rate_from_totals(v) for p, v in m.load(m.PREBOOK)['priors'].items()}
        result, rows = m.allocate(r, cert, rates, {'fga': 90, 'fta': 13, 'tov': 16}, self.config['policies'][0], [.75, 1.25])
        self.assertEqual(result, {'status': 'PRIOR_HOLD', 'missing_prior': ['Jalen Suggs']})
        self.assertEqual(rows, [])

    def test_protected_overflow_and_invalid_input(self):
        self.assertEqual(m.distribute({'P': 12, 'mate': 8}, 10, ['P']), (None, 'PROTECTED_EXCEEDS_BUDGET'))
        for bad in [-1, math.nan, math.inf]:
            with self.assertRaises(AssertionError):
                m.distribute({'P': bad}, 10, [])

    def test_zero_weight_and_zero_budget(self):
        self.assertEqual(m.distribute({'P': 0}, 2, []), (None, 'NO_FREE_WEIGHT'))
        self.assertEqual(m.distribute({'P': 0}, 0, []), ({'P': 0}, None))
        self.assertEqual(m.distribute({'P': 2}, 2, ['P']), ({'P': 2}, None))

    def test_conservation_and_featured_32_minutes(self):
        rows = m.read_csv(m.ALLOC)
        for t in self.report['team_policies']:
            if t['status'] != 'CONDITIONAL_NUMERIC':
                continue
            selected = [r for r in rows if r['rotation'] == t['rotation'] and r['policy'] == t['policy']]
            for k in m.BUDGET_KEYS:
                self.assertAlmostEqual(sum(float(r['allocated_' + k]) for r in selected), t['budget'][k])
            for r in selected:
                if r['protected'] == '1':
                    for k in m.BUDGET_KEYS:
                        self.assertEqual(r['raw_' + k], r['allocated_' + k])
                if r['player'] == 'Protagonist' and r['policy'] == 'B14A':
                    self.assertEqual(r['minutes'], '32')
                    self.assertAlmostEqual(float(r['allocated_tov']), 2.6 * 32 / 36)

    def test_orlando_bound_does_not_invent_guard_or_medical_status(self):
        r = self.rotations['ORL_0022100701']
        self.assertEqual(m.guard_deficit(r), 12)
        changed = copy.deepcopy(r)
        changed['minute_ceiling_design_only'] = 48
        self.assertEqual(m.guard_deficit(changed), 0)  # Bound depends on design rule.
        mitchell = next(e for report in self.source['reports'] for e in report['entries'] if e['player'] == 'Davion Mitchell')
        self.assertEqual(mitchell['historical_status'], 'Questionable')
        self.assertIsNone(self.config['selected_trade_policy'])

    def test_partial_pairs_do_not_become_outcomes(self):
        self.assertEqual(self.report['team_policy_counts'], {'CONDITIONAL_NUMERIC': 16, 'PRIOR_HOLD': 4, 'ROLE_HOLD': 4})
        self.assertEqual(self.report['numeric_pair_conditions'], 4)
        for p in self.report['pair_conditions']:
            self.assertIsNone(p['team_score'])
            self.assertIsNone(p['score_margin'])
            self.assertIsNone(p['winner'])
        for key in ('projected_points', 'team_efficiency', 'season_wins', 'selected_trade_policy'):
            self.assertIsNone(self.report[key])
        self.assertEqual(self.report['actual_minutes_selected'], 0)


if __name__ == '__main__':
    unittest.main()
