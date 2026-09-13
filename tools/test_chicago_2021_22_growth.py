import copy
import csv
import io
import json
import unittest

import build_chicago_2021_22_growth as m


class GrowthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs = m.build()
        cls.book = json.loads(cls.outputs[m.BOOK])
        cls.report = json.loads(cls.outputs[m.REPORT])
        cls.queue = list(csv.DictReader(io.StringIO(cls.outputs[m.QUEUE])))

    def test_saved_outputs_reproduce_and_stay_unselected(self):
        for path, content in self.outputs.items():
            self.assertEqual(path.read_text(), content)
        self.assertIsNone(self.book['selected_pair'])
        self.assertEqual(self.report['actual_game_minutes_selected'], 0)
        self.assertTrue(all(r['alternate_available'] == r['alternate_minutes'] == 'HOLD' for r in self.queue))

    def test_future_vintage_and_mislabelled_dates_rejected(self):
        config, source, rows = m.load(m.CONFIG), m.load(m.SOURCE), m.read_csv(m.OBS)
        for field, value in [('season', '2021-22'), ('date', '2022-02-16')]:
            bad = copy.deepcopy(rows)
            bad[0][field] = value
            with self.assertRaises(AssertionError):
                m.produce_candidates(config, source, bad)
        source['college']['last_game_date'] = '2022-03-28'
        with self.assertRaises(AssertionError):
            m.produce_candidates(config, source, rows)

    def test_future_injury_report_cannot_change_opening_production(self):
        source = m.load(m.SOURCE)
        source['reports'] = [{'arbitrary_future_report': '2030-01-01'}]
        self.assertEqual(m.produce_candidates(m.load(m.CONFIG), source, m.read_csv(m.OBS)), self.book)

    def test_shooting_arithmetic_and_cost_of_growth(self):
        p = next(c for c in self.book['candidates'] if c['id'] == 'P21A')
        self.assertAlmostEqual(p['role_expected']['pts'], 16)
        self.assertAlmostEqual(p['delta_vs_same_32_minutes']['pts'], 3.5 * 32 / 36)
        self.assertGreater(p['delta_vs_same_32_minutes']['tov'], 0)
        self.assertGreater(p['additional_shot_ending_proxy_at_32'], 0)
        for c in self.book['candidates']:
            r = c['per36']
            self.assertAlmostEqual(r['pts'], 2 * r['fgm'] + r['fg3m'] + r['ftm'])
            self.assertLessEqual(r['fgm'] - r['fg3m'], r['fga'] - r['fg3a'])
        self.assertTrue(all(p['team_score_delta'] is None for p in self.book['pairs']))

    def test_college_translation_is_not_college_efficiency_copy(self):
        c = m.load(m.SOURCE)['college']
        self.assertEqual(445, 2 * c['totals']['fgm'] + c['totals']['fg3m'] + c['totals']['ftm'])
        self.assertEqual(120, c['totals']['orb'] + c['totals']['drb'])
        d = next(x for x in self.book['candidates'] if x['id'] == 'D21A')['per36']
        self.assertLess(d['fg3m'] / d['fg3a'], 61 / 144)
        self.assertLess(d['pts'], self.book['college_per36']['pts'])
        self.assertEqual(len(self.book['comparisons']), 5)
        self.assertIn('Josh Green', [c['player'] for c in self.book['comparisons']])

    def test_seventy_minutes_preserve_creators_and_reject_unavailable_recipient(self):
        case = next(c for c in self.report['replacement_cases'] if c['id'].endswith('_70'))
        totals = case['certificate']['player_minutes']
        self.assertEqual((totals['Protagonist'], totals['LaMelo_pick4'], totals['Coby']), (32, 32, 36))
        self.assertEqual(sum(-v for v in case['delta'].values() if v < 0), 70)
        self.assertEqual(sum(v for v in case['delta'].values() if v > 0), 70)
        self.assertTrue(all(set(w['positions'].values()) & {'LaMelo_pick4', 'Coby'} for w in case['witness']))
        with self.assertRaises(AssertionError):
            m.certify(case['witness'], case['unavailable'] + ['Green'], m.load(m.prior.ROLE))

    def test_report_dates_status_and_assignment_do_not_become_clearance(self):
        q = {(r['date'], r['player']): r for r in self.queue}
        mark = q['2022-01-24', 'Markkanen']
        self.assertEqual(mark['report_date'], '2022-01-23')
        self.assertEqual(mark['report_game_date'], '2022-01-24')
        self.assertEqual(q['2021-11-15', 'Chris Duarte']['historical_status'], 'Questionable')
        self.assertEqual(q['2022-02-16', 'Green']['historical_status'], 'Probable')
        self.assertEqual(q['2022-02-16', 'Joe Wieskamp']['action'], 'REVIEW_ASSIGNMENT_CONTRACT')
        self.assertNotIn(('2022-01-23', 'Markkanen'), q)

    def test_joint_absence_not_sum_of_single_absence_solutions(self):
        role = m.load(m.prior.ROLE)
        lavine = next(c for c in role['cases'] if c['kind'] != 'policy' and c['unavailable'] == ['LaVine'])
        with self.assertRaises(AssertionError):
            m.certify(lavine['lineup_witness'], ['LaVine', 'Caruso', 'Chris Duarte'], role)
        january = next(c for c in self.report['date_connections'] if c['date'] == '2022-01-23')
        jan_case = next(c for c in self.report['replacement_cases'] if c['id'] == january['case'])
        self.assertNotIn('Green', jan_case['certificate']['player_minutes'])
        self.assertEqual(jan_case['certificate']['player_minutes']['Stanley Johnson'], 10)
        self.assertEqual(jan_case['certificate']['player_minutes']['Chris Duarte'], 14)
        self.assertIsNone(jan_case['team_score_delta'])


if __name__ == '__main__':
    unittest.main()
