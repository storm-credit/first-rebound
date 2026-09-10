import unittest
import json
import build_chicago_2020_21_league_boundaries as lb


class LeagueBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result, cls.screen = lb.build()
        cls.actual = lb.normalized_games()
        cls.cases = json.loads(lb.sb.OUT.read_text())['record_candidates']

    def games(self, wins, flips=()):
        c = next(c for c in self.cases if c['chicago_record'][0] == wins)
        rows = []
        for g in self.actual:
            if 'CHI' in (g['home'], g['away']):
                winner = 'CHI' if c['outcomes'][g['date']] else (g['away'] if g['home'] == 'CHI' else g['home'])
                g = {**g, 'winner': winner}
            rows.append(lb.changed_game(g) if g['id'] in flips else g.copy())
        return rows

    def test_all_non_chicago_games_are_partitioned_without_clearance(self):
        self.assertEqual(len({r['id'] for r in self.screen}), 1008)
        self.assertEqual(sum(self.result['screen_counts'].values()), 1008)
        self.assertTrue(all('CHI' not in (r['home'], r['away']) for r in self.screen))
        self.assertTrue(all(r['impact_status'] == 'NOT_CALCULATED' and not r['selected'] for r in self.screen))

    def test_32_wins_can_enter_without_changing_a_chicago_game(self):
        games = self.games(32, ['2021-02-20_CHA_GSW'])
        self.assertEqual(lb.record_wins(games)['CHI'], 32)
        self.assertEqual(lb.record_wins(games)['CHA'], 32)
        self.assertEqual(lb.chi_rank(games), 10)

    def test_opponent_gain_can_offset_charlotte_gain(self):
        # CHA gains, but WAS loses and CHI wins the remaining tied comparison.
        games = self.games(33, ['2021-05-16_WAS_CHA'])
        self.assertEqual(lb.chi_rank(games), 10)
        self.assertEqual(sum(lb.record_wins(games).values()), 1080)
        # A different CHA gain really does push CHI below the play-in boundary.
        self.assertEqual(lb.chi_rank(self.games(33, ['2021-01-14_TOR_CHA'])), 11)

    def test_31_wins_need_more_than_one_flip_in_this_experiment(self):
        c = self.result['sensitivity_cases'][0]
        self.assertEqual(c['one_flip_rank_counts'], {'11': 1008})
        self.assertEqual(lb.chi_rank(self.games(31, ['2021-02-20_CHA_GSW', '2021-02-28_SAC_CHA'])), 10)

    def test_full_tie_requires_later_criteria_instead_of_arbitrary_sort(self):
        # Three-way mini-league cycle: this deliberately limited resolver must stop.
        games = []
        for home, away in [('CHI','CHA'), ('CHA','WAS'), ('WAS','CHI')]:
            games.append({'home': home, 'away': away, 'winner': home})
        for team in ('MIL','PHI','ATL'):
            games.extend([{'home': team, 'away': 'HOU', 'winner': team}] * 2)
        with self.assertRaisesRegex(AssertionError, 'Full tie'):
            lb.chi_rank(games)


if __name__ == '__main__':
    unittest.main()
