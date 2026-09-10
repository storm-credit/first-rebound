import csv
import json
import unittest
from collections import Counter
import build_chicago_2020_21_boundary_impact as bi


class BoundaryImpactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(bi.OUT.read_text())
        cls.rows = bi.cc.read(bi.OBS)

    def test_priority_coverage_includes_both_directions_and_overtime(self):
        with (bi.S / 'NBA_2020_21_NON_CHICAGO_CONTACT_SCREEN.csv').open() as f:
            screen = list(csv.DictReader(f))
        priority = {r['id'] for r in screen if r['review_priority'] == 'P1_BOUNDARY'}
        self.assertEqual({r['event_id'] for r in self.rows}, priority)
        self.assertEqual(len(self.rows), 776)
        groups = bi.groups()
        self.assertEqual(len(groups), 58)
        overtime = {gid for (gid, _), rows in groups.items() if bi.baseline(rows)[1] == 3180}
        self.assertEqual(len(overtime), 7)
        charlotte = [g for g in bi.lb.normalized_games() if g['id'] in priority and 'CHA' in (g['home'], g['away'])]
        self.assertEqual(Counter(g['winner'] == 'CHA' for g in charlotte), {True: 9, False: 4})

    def test_injury_rows_are_not_free_minutes(self):
        for b in self.data['branches']:
            eligible = bi.allowed(bi.groups()[(b['event_id'], b['team'])]) | set(b['newcomers'])
            self.assertTrue(all(p in eligible for p, n in b['delta_seconds'].items() if n > 0))
            if b['event_id'] == '2021-02-28_SAC_CHA' and b['team'] == 'CHA':
                self.assertEqual(b['alternate_seconds'].get('Gordon Hayward', 0), 0)
                self.assertEqual(b['alternate_seconds'].get('Cody Zeller', 0), 0)

    def test_center_policy_is_funded_and_separate_from_clock_residual(self):
        bi.verify_branches(self.data['branches'], self.data['lineup_witnesses'])
        b = next(b for b in self.data['branches'] if (b['event_id'], b['team'], b['profile']) == ('2021-01-31_WAS_BKN', 'WAS', 'LOW_MINUTES'))
        center = [m for m in b['balance_moves'] if m.get('reason') == 'CONDITIONAL_CENTER_COVERAGE_NOT_CLOCK_CORRECTION']
        self.assertEqual([(m['player'], m['seconds']) for m in center], [('Moritz Wagner', 305)])
        self.assertLessEqual(abs(b['clock_correction']['seconds']), 2)
        self.assertEqual(sum(b['delta_seconds'].values()), 0)

    def test_paired_margin_and_back_to_back_cost_have_opposite_signs(self):
        inputs = self.data['paired_inputs']
        self.assertEqual(len(inputs), 348)
        for r in inputs:
            self.assertAlmostEqual(r['away_margin_constant'], -r['home_margin_constant'])
            self.assertEqual(r['away_margin_band'], [-r['home_margin_band'][1], -r['home_margin_band'][0]])
            zero = next(z for z in inputs if (z['event_id'], z['profile'], z['method'], z['fatigue']) == (r['event_id'], r['profile'], r['method'], 0))
            hp, ap = r['workload_coefficients']
            self.assertAlmostEqual(r['home_margin_constant']-zero['home_margin_constant'], r['fatigue']*(ap-hp), places=7)
            self.assertFalse(r['selected'])

    def test_disagreement_is_preserved_instead_of_averaged(self):
        summary = self.data['game_summary']
        reverse = {r['event_id'] for r in summary if r['status'] == 'ALL_TESTED_REVERSE'}
        disagreement = {r['event_id'] for r in summary if r['status'] == 'MODEL_DISAGREEMENT_OR_UNRESOLVED'}
        self.assertEqual(reverse, {'2021-02-28_SAC_CHA', '2021-05-06_TOR_WAS'})
        self.assertEqual(disagreement, {'2020-12-27_CHA_BKN', '2021-02-20_CHA_GSW', '2021-05-08_IND_WAS'})
        self.assertTrue(all(not r['selected'] for r in summary))

    def test_limited_bridge_conserves_wins_without_season_selection(self):
        bridge = self.data['season_bridge']
        self.assertEqual(len(bridge), 72)
        for r in bridge:
            self.assertEqual(r['other_games_held'], 979)
            self.assertFalse(r['selected'])
            self.assertEqual(r['unresolved_games'], [])
            self.assertEqual(sum(r['team_wins'].values()), 1080)
            self.assertEqual(sum(r['win_deltas_vs_actual'].values()), 0)
            method = r['source_condition']['method']
            self.assertEqual(r['chicago_rank'], 10 if method == 'BPM_MAR25_EB' else 9)
            self.assertIn(r['team_wins']['CHI'], (31,) if method == 'BPM_MAR25_EB' else (32, 33))
        self.assertFalse(self.data['manuscript_allowed'])


if __name__ == '__main__':
    unittest.main()
