"""Check G candidate calibration, complete-path consistency and approval scope."""
import json
import statistics
import unittest
import build_chicago_2020_21_author_packet as g


class AuthorPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet=g.build()
        cls.source=json.loads(g.f.OUT.read_text())

    def test_benchmarks_are_explicit_and_reconstructed(self):
        self.assertEqual(json.loads(g.OUT.read_text()),self.packet)
        for c in self.packet['rival_candidates']:
            for method,r in c['methods'].items():
                values=[self.packet['benchmark_players'][p][method] for p in c['players']]
                expected=max(values) if c['aggregation']=='max' else statistics.median(values)
                self.assertAlmostEqual(expected,r['effective_rating'])
        self.assertEqual([c['minutes'] for c in self.packet['rival_candidates']],[28,24,32,32])
        self.assertNotIn('Luka Doncic',g.BROAD_CREATORS)
        self.assertFalse(self.packet['rival_candidates'][3]['recommended'])

    def test_both_availability_branches_keep_one_whole_league_case(self):
        schedule=g.f.bi.lb.normalized_games()
        for candidate in self.packet['rival_candidates']:
            for r in candidate['methods'].values():
                case=next(c for c in self.source['league_cases'] if c['id']==r['case_id'])
                self.assertEqual(set(r['bridge_indices'])&set(case['bridge_indices']),set(r['bridge_indices']))
                self.assertEqual(len(r['bridge_indices']),2)
                self.assertEqual(r['team_wins'],case['team_wins'])
                wins={team:0 for team in r['team_wins']}
                for game in schedule:
                    winner=game['winner']
                    if game['id'] in r['changed_game_ids']:
                        winner=game['away'] if winner==game['home'] else game['home']
                    wins[winner]+=1
                self.assertEqual(wins,r['team_wins'])
                self.assertEqual(sum(wins.values()),1080)

    def test_cross_method_difference_and_local_sensitivity(self):
        self.assertEqual(len(self.packet['cross_method_changed_game_ids']),5)
        self.assertEqual([x for x in self.packet['cross_method_changed_game_ids'] if 'CHI' in x],['2021-01-30_CHI_POR'])
        r=self.packet['rival_candidates'][0]['methods']
        self.assertEqual(r['BPM_MAR25_EB']['plus_minus_half_point_stress']['minnesota_wins'],[24,25,26])
        self.assertEqual(r['RAPTOR_RS_EB']['plus_minus_half_point_stress']['minnesota_wins'],[23,24])
        for item in r.values():
            self.assertIn(item['case_id'],item['plus_minus_half_point_stress']['case_ids'])

    def test_approval_and_health_are_not_inferred(self):
        self.assertFalse(self.packet['selected'])
        self.assertFalse(self.packet['manuscript_allowed'])
        self.assertTrue(all(not c['selected'] for c in self.packet['rival_candidates']))
        self.assertEqual(len(self.packet['approval_scope']['not_approved_by_this_choice']),5)
        self.assertEqual(len(self.packet['conditional_target_calendar']),14)
        for item in self.packet['conditional_target_calendar']:
            self.assertEqual(item['target_game_count'],len(set(item['event_ids'])))
            self.assertIn('not observed GP',item['meaning'])
        for filename,digest in self.packet['upstream_sha256'].items():
            matches=list(g.f.S.glob(filename))+list(g.f.S.parent.glob('tools/'+filename))
            self.assertEqual(len(matches),1)
            self.assertEqual(g.f.bi.cc.sha(matches[0]),digest)


if __name__=='__main__':
    unittest.main()
