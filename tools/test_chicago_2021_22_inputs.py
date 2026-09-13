import copy
import csv
import io
import json
import unittest
import build_chicago_2021_22_inputs as m


class SeasonInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs = m.build()
        cls.availability = list(csv.DictReader(io.StringIO(cls.outputs[m.AVAIL])))
        cls.priors = json.loads(cls.outputs[m.PRIORS])
        cls.report = json.loads(cls.outputs[m.REPORT])

    def test_saved_derivatives_reproduce(self):
        for path, text in self.outputs.items():
            self.assertEqual(path.read_text(), text, path.name)

    def test_schedule_and_game_identity(self):
        r = self.report
        self.assertEqual((r['league_games'], r['chicago_home'], r['chicago_away'], r['calendar_player_rows']), (1230, 41, 41, 1230))
        conflict = r['schedule_conflicts'][0]
        self.assertEqual(conflict['replacement_date_reported'], '2022-01-10')
        self.assertEqual(conflict['played_date_on_official_game_page'], '2022-01-11')
        self.assertFalse(r['alternate_calendar_selected'])

    def test_absence_is_not_automatically_health(self):
        self.assertEqual(m.observation_status(None), 'NO_SAME_DAY_ROW')
        self.assertEqual(m.observation_status({'seconds': '0', 'comment': "DNP - Coach's Decision"}), 'OBSERVED_COACH_DNP')
        self.assertEqual(m.observation_status({'seconds': '0', 'comment': 'DND - Injury/Illness'}), 'OBSERVED_HEALTH_RESTRICTION')
        self.assertTrue(all(r['alternate_available'] == 'HOLD' and r['alternate_minutes'] == 'HOLD' for r in self.availability))

    def test_report_game_date_and_nonmedical_assignment(self):
        coby = next(r for r in self.availability if r['date'] == '2021-11-14' and r['player'] == 'Coby')
        self.assertEqual((coby['primary_status'], coby['primary_reason']), ('Out', 'SHOULDER_INJURY_MANAGEMENT'))
        duarte = next(r for r in self.availability if r['date'] == '2021-11-15' and r['player'] == 'Chris Duarte')
        self.assertEqual(duarte['primary_status'], 'Questionable')
        prev = next(r for r in self.availability if r['date'] == '2021-11-14' and r['player'] == 'Chris Duarte')
        self.assertEqual(prev['primary_status'], '')
        joe = next(r for r in self.availability if r['date'] == '2021-11-14' and r['player'] == 'Joe Wieskamp')
        self.assertEqual(joe['primary_reason'], 'G_LEAGUE_TWO_WAY')

    def test_future_season_cannot_change_opening_prior(self):
        rows = m.read_csv(m.OBS)
        prior = m.prior_for('Coby White', rows, '2021-10-19')
        changed = copy.deepcopy(rows)
        for r in changed:
            if r['season'] == '2021-22':
                r['pts'] = '99999'
        self.assertEqual(prior, m.prior_for('Coby White', changed, '2021-10-19'))
        stale = next(r for r in changed if r['season'] == '2020-21' and r['player'] == 'Coby White')
        stale['date'] = '2021-10-20'
        with self.assertRaisesRegex(ValueError, 'lookahead'):
            m.prior_for('Coby White', changed, '2021-10-19')

    def test_prior_gaps_do_not_become_zero_talent(self):
        self.assertEqual(set(self.report['missing_prior_for_normal_minutes']), {'Chris Duarte', 'Protagonist'})
        self.assertEqual(self.report['normal_minutes_without_nba_prior'], 46)
        self.assertEqual(sum(p['historical_prior'] is not None for p in self.priors['players']), 16)
        self.assertTrue(all(p['alternate_2021_22_per36'] is None for p in self.priors['players']))

    def test_box_arithmetic_and_display_seconds_residuals(self):
        for p in self.priors['players']:
            if p['historical_prior']:
                t = p['historical_prior']['totals']
                self.assertEqual(t['pts'], 2 * t['fgm'] + t['fg3m'] + t['ftm'])
                self.assertEqual(t['reb'], t['orb'] + t['drb'])
        self.assertEqual(self.report['nonzero_time_residual_games'], 332)
        self.assertIn('5', self.report['team_time_residual_counts'])
        self.assertEqual(sum(self.report['team_time_residual_counts'].values()), 2460)

    def test_coby_example_pays_for_all_18_minutes(self):
        c = self.report['coby_absence_example']
        minutes = m.Counter()
        for players in c['position_minutes'].values():
            minutes.update(players)
        self.assertNotIn('Coby', minutes)
        self.assertEqual((minutes['Satoransky'], minutes['Denzel Valentine'], minutes['Protagonist']), (10, 8, 32))
        self.assertEqual(sum(minutes.values()), 240)
        self.assertEqual(self.report['chicago_games_before_first_coby_played_observation'], 13)
        self.assertFalse(self.report['season_selected'])


if __name__ == '__main__':
    unittest.main()
