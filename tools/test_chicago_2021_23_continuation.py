import unittest
from build_chicago_2021_23_continuation import build,rookie_fourth,grow


class ContinuationTests(unittest.TestCase):
    def test_option_math_and_nonduplicated_roles(self):
        x=build()
        self.assertEqual(rookie_fourth(4540700,270,120),6920027)
        for option in x['offseason_2021'].values():self.assertEqual(option['standard_slots'],15)
        self.assertNotIn('Theis',x['offseason_2021']['G1A']['roster_without_protagonist'])
        self.assertNotIn('Markkanen',x['offseason_2021']['G1B']['roster_without_protagonist'])
        self.assertNotIn('Satoransky',x['offseason_2021']['G1D']['roster_without_protagonist'])

    def test_cap_room_is_not_mle_or_trade_approval(self):
        x=build()
        self.assertEqual(max(r['additional_real_cap_amount_required'] for r in x['ntmle_sequence']),878908)
        self.assertTrue(all(not r['eligibility_cleared'] for r in x['ntmle_sequence']))
        self.assertTrue(all(not r['transaction_approved'] for r in x['offseason_2021'].values()))
        self.assertIsNone(x['exact_nonroster_charge'])

    def test_rotation_capacity_and_future_financial_pressure(self):
        x=build();self.assertEqual(sum(x['healthy_rotation_player_budget'].values()),240)
        self.assertEqual(x['healthy_rotation_player_budget']['Protagonist'],32)
        rows=x['budget_2022_cases']
        self.assertEqual(len(rows),48)
        self.assertTrue(any(r['tax_room']<0 for r in rows))
        self.assertTrue(any(r['apron_room_if_triggered']<0 for r in rows))
        self.assertTrue(any(r['tax_room']>0 for r in rows))
        self.assertEqual(grow(22000000,4),[22000000,23760000,25520000,27280000])
        self.assertFalse(x['author_locked'] or x['season_selected'] or x['manuscript_allowed'])


if __name__=='__main__':unittest.main()
