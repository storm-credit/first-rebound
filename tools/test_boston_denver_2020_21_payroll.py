import json
import unittest
from build_boston_denver_2020_21_payroll import SOURCE, build


class PayrollTests(unittest.TestCase):
    def test_roster_compatibility_with_existing_minutes(self):
        for team in build()['teams'].values():
            self.assertEqual(team['positive_minute_registration_conflicts'], [])
            self.assertTrue(all(c['standard'] <= 15 and c['twoway'] <= 2 for c in team['dated_roster_counts']))

    def test_expired_contracts_and_bonuses_stay_in_budget(self):
        r = build()['teams']
        self.assertEqual(r['BOS']['previous_contract_charge_budget_usd'], 2161920)
        self.assertEqual(r['DEN']['previous_contract_charge_budget_usd'], 2000000)
        self.assertEqual(r['BOS']['all_disclosed_bonus_usd'], 3628572)
        self.assertEqual(r['DEN']['all_disclosed_bonus_usd'], 3225001)
        self.assertEqual(r['BOS']['peak']['residual_allowance_usd'], 5381195)
        self.assertEqual(r['DEN']['peak']['residual_allowance_usd'], 6684733)

    def test_draft_contracts_are_not_free_agent_contracts(self):
        r = build()['teams']
        for team, player in [('BOS', 'Carsen Edwards'), ('DEN', 'Vlatko Cancar')]:
            row = next(x for x in r[team]['core_players'] if x['player'] == player)
            self.assertEqual(row['entry_route'], 'DRAFT_CONTRACT_NOT_FA')
            self.assertEqual(row['young_fa_floor_addition_usd'], 0)
        bey = next(x for x in r['DEN']['core_players'] if x['player'] == 'Saddiq Bey')
        self.assertEqual(bey['base_usd'], 2379840)

    def test_partial_bound_cannot_approve_and_bad_sources_fail(self):
        r = build()
        self.assertFalse(r['season_selected'])
        for x in r['teams'].values():
            self.assertIsNone(x['exact_apron_compliance'])
            self.assertFalse(x['complete_other_charge_inventory_verified'])
            self.assertTrue(x['reported_mle_path_implies_apron_limit'])
            self.assertEqual(x['mle_used_usd'], 9258000)
        source = json.loads(SOURCE.read_text())
        source['core_players']['BOS'][0]['source_id'] = 'NOT_A_SOURCE'
        with self.assertRaises(AssertionError):
            build(source)


if __name__ == '__main__':
    unittest.main()
