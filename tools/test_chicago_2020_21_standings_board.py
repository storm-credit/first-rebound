import unittest
import build_chicago_2020_21_standings_board as board


class StandingsBoardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = board.build()

    def test_baseline_excludes_play_in_and_duplicate_perspectives(self):
        rows, wins = board.baseline()
        self.assertEqual(len(rows), 1080)
        self.assertLessEqual(max(r['date'] for r in rows), '2021-05-16')
        self.assertEqual((wins['CHI'], wins['CHA'], wins['POR'], wins['GSW']), (31, 33, 42, 39))
        self.assertEqual(board.head_to_head(rows, 'CHI', 'CHA'), [3, 0])

    def test_win_transfers_and_changed_dates(self):
        cases = self.data['record_candidates']
        self.assertEqual([c['east_regular_season_rank'] for c in cases], [11, 11, 10])
        self.assertEqual([[g['date'] for g in c['changed_games']] for c in cases],
                         [[], ['2021-01-30'], ['2020-12-27', '2021-01-30']])
        for c in cases:
            self.assertEqual(sum(w for w, _ in c['conditional_team_records'].values()), 1080)
            self.assertEqual(c['chicago_record'][0] - 31 + sum(c['opponent_win_deltas'].values()), 0)

    def test_postseason_h2h_does_not_choose_lottery_order(self):
        cases = self.data['record_candidates']
        expected = [[[8, 10], [8, 10]], [[10, 10], [10, 10]], [[10, 12], [10, 11]]]
        for c, bands in zip(cases, expected):
            self.assertEqual([b['record_rank_band'] for b in c['lottery_if_chicago_misses_playoffs']], bands)
            self.assertFalse(c['selected'])
            for b in c['lottery_if_chicago_misses_playoffs']:
                self.assertIsNone(b['exact_pick'])
                self.assertIsNone(b['odds'])
        self.assertEqual(cases[-1]['chicago_charlotte_h2h']['record'], [3, 0])
        self.assertIn('CHA', cases[-1]['lottery_if_chicago_misses_playoffs'][0]['tied_teams'])
        self.assertIsNone(board.lottery_band({'CHI': 33, 'CHA': 33}, {'CHA'}))

    def test_west_boundary_and_33_win_fragility(self):
        c31, c32, c33 = self.data['record_candidates']
        self.assertEqual([c['west_boundary']['POR_play_in'] for c in (c31, c32, c33)], [False, True, True])
        self.assertEqual(c33['west_boundary']['GSW_MEM_h2h'], [2, 1])
        self.assertTrue(all(c['fatigue'] == 0 and c['method'] == 'RAPTOR_RS_EB'
                            for c in c33['source_conditions']))
        self.assertEqual(c33['playoff_qualification'], 'UNSELECTED')
        self.assertFalse(self.data['manuscript_allowed'])


if __name__ == '__main__':
    unittest.main()
