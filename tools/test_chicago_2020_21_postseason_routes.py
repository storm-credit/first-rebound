import json,unittest
import build_chicago_2020_21_postseason_routes as p

class PostseasonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(p.OUT.read_text())
    def test_historical_ties_use_correct_two_and_three_team_precedence(self):
        o=p.order(p.bi.lb.normalized_games())
        self.assertEqual(o['WEST'][4:7],['DAL','POR','LAL'])
        self.assertEqual(o['EAST'][3:5],['NYK','ATL'])
        self.assertEqual(o['WEST'][2:4],['DEN','LAC'])
    def test_partial_three_way_tie_restarts_for_charlotte_washington(self):
        case=next(c for c in self.data['cases'] if c['wins']['CHI']==c['wins']['CHA']==c['wins']['WAS']==32)
        self.assertEqual(case['seeds']['EAST'][8:11],['CHI','CHA','WAS'])
    def test_playin_nine_ten_need_two_wins_and_cannot_both_qualify(self):
        for c in self.data['cases']:
            for conf,field in [('EAST','east_playin'),('WEST','west_playin')]:
                seeds=c['seeds'][conf];routes=c[field]
                self.assertEqual(len(routes),8)
                self.assertEqual(len({tuple(sorted(r['qualifiers'])) for r in routes}),5)
                for r in routes:
                    self.assertFalse(set(seeds[8:10])<=set(r['qualifiers']))
                    for t in seeds[8:10]:
                        if t in r['qualifiers']:self.assertEqual(sum(g['winner']==t for g in r['games']),2)
                    self.assertEqual(r['games'][2]['home'],next(t for t in seeds[6:8] if t!=r['qualifiers'][0]))
    def test_lottery_fields_and_record_ties_do_not_select_picks(self):
        self.assertEqual(sum(len(c['source_conditions']) for c in self.data['cases']),72)
        self.assertEqual(len(self.data['cases']),5)
        for c in self.data['cases']:
            self.assertEqual(len(c['postseason_routes']),64);self.assertEqual(c['distinct_lottery_fields'],25)
            for r in c['postseason_routes']:
                self.assertEqual(len(set(r['lottery_teams'])),14)
                self.assertEqual(sum(len(g['teams']) for g in r['lottery_record_groups']),14)
                self.assertEqual(r['CHI_pick_owner'],'CHI');self.assertFalse(r['draw_selected'])
                self.assertFalse(r['selected'])
                if r['CHI_in_lottery']:self.assertLessEqual(r['CHI_record_positions'][1],14)
                else:self.assertGreaterEqual(r['CHI_record_positions'][0],15)
        self.assertFalse(self.data['probabilities_assigned'])
    def test_remaining_queue_is_disjoint_and_not_impact_estimate(self):
        rows=p.bi.cc.read(p.QUEUE);old={r['event_id'] for r in p.bi.cc.read(p.bi.OBS)}
        self.assertEqual(len({r['id'] for r in rows}),979)
        self.assertFalse(old&{r['id'] for r in rows})
        self.assertTrue(all(r['impact_status']=='NOT_CALCULATED' for r in rows))
        self.assertEqual(sum(r['priority']=='BOUNDARY_OR_TIE_REVIEW' for r in rows),280)
        obs=p.bi.cc.read(p.S/'NBA_2020_21_REMAINING_BOUNDARY_OBSERVATIONS.csv')
        expected={r['id'] for r in rows if r['priority']=='BOUNDARY_OR_TIE_REVIEW' and int(r['margin'])<=3}
        self.assertEqual({r['event_id'] for r in obs},expected);self.assertEqual(len(expected),40)

if __name__=='__main__':unittest.main()
