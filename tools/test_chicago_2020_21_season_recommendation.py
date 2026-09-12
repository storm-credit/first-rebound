import copy
import json
import unittest
from collections import Counter
import build_chicago_2020_21_season_recommendation as k


class RecommendationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(k.OUT.read_text());cls.lineups=json.loads(k.LINEUPS.read_text())

    def test_fixed_minutes_and_corruption_rejected(self):
        k.verify(self.lineups)
        broken=copy.deepcopy(self.lineups);broken['rows'][0]['lineup_witness'][0]['seconds']+=1
        with self.assertRaises(AssertionError):k.verify(broken)

    def test_minimum_overlap_has_analytic_certificate(self):
        self.assertEqual(len(self.lineups['rows']),28)
        self.assertEqual(sum(r['minimum_excess_big_seconds']>1e-5 for r in self.lineups['rows']),4)
        for r in self.lineups['rows']:
            self.assertTrue(r['lower_bound_attained'])
            self.assertAlmostEqual(r['minimum_excess_big_seconds'],r['analytic_lower_bound_seconds'],places=5)
            self.assertLessEqual(r['minimum_excess_big_seconds'],r['old_excess_big_seconds']+1e-5)

    def test_stress_uses_recommended_leave_and_keeps_unknowns(self):
        rows=self.data['spacing_stress'];self.assertEqual(len(rows),224)
        self.assertEqual(k.spacing_stress(self.lineups),rows)
        self.assertEqual(self.data['spacing_stress_counterexamples'],[])
        self.assertEqual({r['event_id'] for r in rows if r['terry_leave_already_applied']},{'2021-05-07_CHA_ORL'})
        for r in rows:self.assertEqual(r['direction'],r['base_direction'])

    def test_full_paths_standings_and_crosscheck_are_separate(self):
        actual=k.j.bi.lb.normalized_games()
        paths={r['role']:r for r in self.data['season_candidates']}
        self.assertEqual(paths['PRIMARY_RECOMMENDATION']['base_case_id'],'F038')
        self.assertEqual(paths['CROSSCHECK']['base_case_id'],'F138')
        for r in paths.values():
            mapping={g['event_id']:g['winner'] for g in r['regular_season_games']}
            self.assertEqual(len(mapping),1080)
            games=[{**g,'winner':mapping[g['id']]} for g in actual]
            self.assertEqual(k.j.bi.lb.record_wins(games),r['team_wins'])
            self.assertEqual(k.j.f.e.d.ps.order(games),r['seeds'])
            self.assertEqual(sum(r['team_wins'].values()),1080)
        a,b=(paths[x] for x in ('PRIMARY_RECOMMENDATION','CROSSCHECK'))
        self.assertEqual(len(set(a['changed_game_ids'])^set(b['changed_game_ids'])),5)

    def test_calendar_is_projection_not_medical_approval(self):
        rows=self.data['calendar'];self.assertEqual(len(rows),1079)
        self.assertEqual(len({(r['scope'],r['team'],r['player'],r['event_id']) for r in rows}),1079)
        self.assertFalse(any(r['author_locked'] for r in rows))
        rr=[r for r in rows if r['player']=='Tyrell Terry']
        self.assertEqual(Counter(r['seconds'] for r in rr),{360:45,0:27})
        chi={r['player']:r for r in self.data['calendar_summary'] if r['team']=='CHI'}
        self.assertEqual(chi['Otto Porter Jr.']['positive_minute_dates'],25)
        self.assertEqual(chi['Wendell Carter Jr.']['positive_minute_dates'],61)
        self.assertFalse(self.data['season_selected']);self.assertFalse(self.data['manuscript_allowed'])

    def test_registration_gap_not_silently_filled(self):
        rr=self.data['reported_hall_registration_gap_check']
        self.assertEqual(len(rr),3);self.assertTrue(all(r['seconds']==0 for r in rr))
        self.assertEqual({r['id'] for r in self.data['remaining_requirements']},
            {'K_HEALTH','K_REGISTRATION','K_TRANSACTIONS','K_METHOD_EVENTS'})


if __name__=='__main__':unittest.main()
