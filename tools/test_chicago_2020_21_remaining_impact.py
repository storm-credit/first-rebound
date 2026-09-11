"""Acceptance checks for new scope, conservation, dependencies and failure behavior."""
import copy
import json
import unittest
from collections import Counter
import build_chicago_2020_21_remaining_impact as r


class RemainingImpactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.j = json.loads(r.OUT.read_text())

    def test_complete_disjoint_scope_and_provenance(self):
        j = self.j
        ids = {g['event_id'] for g in j['game_summary']}
        old = {g['event_id'] for g in json.loads(r.bi.OUT.read_text())['game_summary']}
        obs = r.bi.cc.read(r.OBS)
        self.assertEqual(len(ids), 40)
        self.assertFalse(ids & old)
        self.assertEqual(len(obs), 1082)
        self.assertEqual(ids, {x['event_id'] for x in obs})
        metadata = json.loads((r.S / 'NBA_2020_21_REMAINING_BOUNDARY_PROVENANCE.json').read_text())
        self.assertEqual(r.bi.cc.sha(r.OBS), metadata['snapshot_sha256'])
        pending = r.pending(j)
        self.assertEqual(len(pending), 939)
        self.assertFalse(ids & {x['id'] for x in pending})
        self.assertTrue(all(x['impact_status'] == 'NOT_CALCULATED' for x in pending))

    def test_saved_lineups_and_corruption_rejected(self):
        j = self.j
        r.verify_minutes(j['branches'], j['lineup_witnesses'])
        bad = copy.deepcopy(j['lineup_witnesses'])
        ix = next(i for i, w in enumerate(bad) if w)
        bad[ix][0]['seconds'] += 1
        with self.assertRaises(AssertionError):
            r.verify_minutes(j['branches'], bad)

    def test_absent_players_and_conditional_newcomers(self):
        for b in self.j['branches']:
            self.assertFalse(set(b['removed_players']) & set(b['alternate_seconds']))
            if b['team'] == 'POR':
                self.assertNotIn('Gary Trent Jr.', b['alternate_seconds'])
                self.assertNotIn('Norman Powell', b['alternate_seconds'])
                if b['date'] == '2021-04-16':
                    self.assertNotIn('Damian Lillard', b['alternate_seconds'])
            if b['team'] == 'ORL':
                self.assertEqual(b['alternate_seconds']['Nikola Vucevic'], 1800)
                self.assertNotIn('Gary Harris', b['alternate_seconds'])
                self.assertNotIn('Donta Hall', b['alternate_seconds'])
        b = next(b for b in self.j['branches'] if b['event_id'] == '2021-04-20_POR_LAC' and b['team'] == 'POR')
        correction = next(m for m in b['balance_moves'] if m.get('reason') == 'CONDITIONAL_STARTER_CENTER_OVERLAP_NOT_CLOCK_CORRECTION')
        self.assertEqual(correction['seconds'], 129)
        self.assertEqual(correction['donor'], 'CJ McCollum')

    def test_metric_alias_symbolic_rival_and_paired_sign(self):
        self.assertEqual(len(self.j['paired_inputs']), 504)
        for x in self.j['paired_inputs']:
            self.assertAlmostEqual(x['home_margin_constant'], -x['away_margin_constant'])
            self.assertEqual(set(x['unknown_coefficients']), {r.RIVAL} if 'MIN' in x['event_id'] else set())
            if x['rival_minutes']:
                self.assertAlmostEqual(x['unknown_coefficients'][r.RIVAL], x['rival_minutes'] / 48)
            lo, hi = x['home_margin_band']
            self.assertEqual(x['conditional_sign'], 'HOME' if lo > 0 else 'AWAY' if hi < 0 else 'UNRESOLVED')

    def test_joint_paths_conserve_wins_and_shared_rating(self):
        old = json.loads(r.bi.OUT.read_text())['season_bridge']
        for x in self.j['season_bridge']:
            prior = old[x['source_condition_index']]
            self.assertEqual(x['source_condition'], prior['source_condition'])
            self.assertEqual(sum(x['team_wins'].values()), 1080)
            self.assertEqual(sum(x['win_deltas_vs_B'].values()), 0)
            self.assertEqual(x['team_wins']['CHI'], prior['team_wins']['CHI'])
            lo, hi = x['shared_rival_rating_open_interval']
            oldlo, oldhi = x['source_condition']['rating_open_interval']
            self.assertTrue(oldlo <= lo < hi <= oldhi)
            self.assertEqual(x['other_games_held'], 939)
            self.assertFalse(x['selected'])
        # Counterexample to retaining the previous West bracket: Dallas can fall to 7th.
        self.assertTrue(any(x['seeds']['WEST'].index('DAL') == 6 for x in self.j['season_bridge']))

    def test_playin_fields_and_no_final_selection(self):
        j = self.j
        self.assertFalse(j['selected'])
        self.assertFalse(j['manuscript_allowed'])
        for case in j['league_cases']:
            self.assertFalse(case['selected'])
            for field in case['distinct_lottery_fields']:
                self.assertEqual(len(set(field['lottery_teams'])), 14)
                self.assertFalse(field['draw_selected'])
                lottery = set(field['lottery_teams'])
                playoff = {t for g in field['playoff_record_groups'] for t in g['teams']}
                self.assertFalse(lottery & playoff)
                self.assertEqual(lottery | playoff, r.ps.ALL)
            for route in case['east_playin'] + case['west_playin']:
                lower = route['games'][1]
                self.assertFalse({lower['home'], lower['away']} <= set(route['qualifiers']))
        self.assertEqual(sum(c['joint_playin_outcome_count'] for c in j['league_cases']), 448)


if __name__ == '__main__':
    unittest.main()
