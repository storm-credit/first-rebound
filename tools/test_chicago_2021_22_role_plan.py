import copy
import unittest
import build_chicago_2021_22_role_plan as m


class RoleCertificateTests(unittest.TestCase):
    def setUp(self):
        self.data = copy.deepcopy(m.load(m.INPUT))

    def test_witnesses_and_signed_donor_cost(self):
        self.assertEqual(m.validate(self.data), [])
        output = m.build(self.data)
        for c in output['cases']:
            self.assertEqual(sum(c['delta_from_R21A'].values()), 0)
            self.assertEqual(c['player_minutes_sum'], 240)
        carter = next(c for c in output['cases'] if c['id'] == 'AV_Carter')
        self.assertEqual(carter['delta_from_R21A'], {'Carter': -28, 'Green': 12, 'Tony Bradley': 16})

    def test_same_player_cannot_fill_two_positions(self):
        c = self.data['cases'][0]
        w = c['lineup_witness'][0]['positions']
        w['SG'] = w['PG']
        self.assertTrue(any('five distinct' in e for e in m.validate(self.data)))

    def test_minute_and_position_invention_rejected(self):
        c = self.data['cases'][0]
        c['lineup_witness'][0]['minutes'] += 2
        c['position_minutes']['C']['Protagonist'] = c['position_minutes']['C'].pop('Carter')
        errors = m.validate(self.data)
        self.assertTrue(any('witness budget mismatch' in e for e in errors))
        self.assertTrue(any('eligibility Protagonist' in e for e in errors))

    def test_absence_and_creator_loss_rejected(self):
        c = next(c for c in self.data['cases'] if c['id'] == 'AV_Carter')
        c['unavailable'].append(c['lineup_witness'][0]['positions']['C'])
        c['required_creator_any_of'] = ['Carter']
        errors = m.validate(self.data)
        self.assertTrue(any('unavailable player' in e for e in errors))
        self.assertTrue(any('creator coverage' in e for e in errors))

    def test_stale_roster_and_season_promotion_rejected(self):
        self.data['roster'][0] = 'Moses Moody'
        self.data['season_GP'] = 82
        self.data['source_content_sha256'][next(iter(self.data['source_content_sha256']))] = '0' * 64
        errors = m.validate(self.data)
        self.assertTrue(any('G7 roster mismatch' in e for e in errors))
        self.assertTrue(any('unsupported season' in e for e in errors))
        self.assertTrue(any('STALE' in e for e in errors))

    def test_shortage_cannot_be_hidden(self):
        self.data['infeasible_stress']['expected_unfilled_center_minutes'] = 0
        self.assertIn('center shortage bound', m.validate(self.data))


if __name__ == '__main__':
    unittest.main()
