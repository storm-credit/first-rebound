import unittest

from build_chicago_long_core_cba import (
    award_requirement, build, contract_salary, frozen_pick,
    second_apron_at_last_game, transaction_apron_limits,
)


class LongCoreConditions(unittest.TestCase):
    def test_existing_option_and_unallocated_reserve_are_distinct(self):
        x=build()
        r=next(r for r in x['core_cases'] if r['cap_case']=='ACTUAL2026_REFERENCE' and r['price_case']=='BC1' and r['P_first_cap_percent']==30)
        self.assertEqual(r['LaVine_salary'],48967380)
        self.assertEqual(r['LaVine_option_minus_18pct_target'],19274400)
        self.assertEqual(r['player_budget'],205210600)
        self.assertEqual(r['player_budget_room_to_second'],16475400)
        self.assertEqual(r['full_envelope_room_to_second'],-20700)
        self.assertIsNone(r['actual_apron_team_salary'])
        self.assertFalse(r['actual_second_apron_team_selected'])

    def test_raises_use_original_first_salary_and_discount_needs_acceptance(self):
        self.assertEqual(contract_salary(35147000,5),[35147000,37958760,40770520,43582280,46394040])
        x=build();r=[r for r in x['core_cases'] if r['cap_case']=='ACTUAL2026_REFERENCE' and r['P_first_cap_percent']==30]
        self.assertEqual(r[1]['LaMelo_salary'],48924624)
        self.assertFalse(r[0]['requires_LaVine_opt_out_and_new_acceptance'])
        self.assertTrue(r[2]['requires_LaVine_opt_out_and_new_acceptance'])
        self.assertTrue(all(r['requires_P_pre_signing_35pct_eligibility'] for r in x['core_cases'] if r['P_first_cap_percent']==35))

    def test_apron_transition_preserves_next_year_and_prior_mle_conflict(self):
        self.assertEqual(transaction_apron_limits('H',2023)['current'],None)
        self.assertEqual(transaction_apron_limits('H',2023,True)['next_year'],'second')
        self.assertEqual(transaction_apron_limits('H',2024)['current'],'second')
        self.assertEqual(transaction_apron_limits('F',2023,prior_taxpayer_mle_used=True)['status'],'APRON_TABLE_SCOPE_ONLY')
        self.assertEqual(transaction_apron_limits('F',2024,prior_taxpayer_mle_used=True)['status'],'PRIOR_TAXPAYER_MLE_BLOCK')
        self.assertEqual(transaction_apron_limits('G',2024)['status'],'TRANSITION_TPE_ENDED_REQUIRES_OTHER_ROUTE')
        self.assertIsNone(transaction_apron_limits('B',2024,True)['next_year'])

    def test_freeze_uses_last_game_strict_threshold_and_chronology(self):
        self.assertFalse(second_apron_at_last_game(200,200))
        self.assertTrue(second_apron_at_last_game(201,200))
        self.assertIsNone(second_apron_at_last_game(None,200))
        self.assertIsNone(frozen_pick(2023,True,{})['pick_year'])
        self.assertEqual(frozen_pick(2024,True,{'2025':True,'2026':False,'2027':False,'2028':True})['status'],'FINAL_FIRST_ROUND_GROUP_PENALTY')
        r=frozen_pick(2024,True,{'2025':False,'2026':False,'2027':False})
        self.assertEqual((r['pick_year'],r['determined_after_season_start_year']),(2032,2027))
        r=frozen_pick(2024,True,{'2026':False,'2027':False,'2028':False})
        self.assertEqual(r['status'],'FROZEN_PENDING_CHRONOLOGICAL_INPUT')
        self.assertIsNone(r['exact_pick_number'])

    def test_award_minimum_minutes_and_only_two_short_games(self):
        self.assertTrue(award_requirement('MVP',2026,[20]*63+[15]*2)['standard_met'])
        r=award_requirement('MVP',2026,[20]*62+[15]*3)
        self.assertEqual(r['count'],64)
        self.assertFalse(r['standard_met'])
        self.assertFalse(award_requirement('MVP',2026,[20]*64+[14.99])['standard_met'])
        self.assertEqual(award_requirement('MVP',2026,[20]*64+[None])['status'],'MINUTES_UNKNOWN')

    def test_award_injury_exception_requires_verified_inputs(self):
        e={'qualified_games_before_injury':62,'team_games_before_injury':72,'joint_physician_season_ending_confirmed':True}
        self.assertTrue(award_requirement('MVP',2026,[20]*62,e)['injury_exception_met'])
        self.assertFalse(award_requirement('MVP',2026,[20]*61,{**e,'qualified_games_before_injury':61})['injury_exception_met'])
        self.assertFalse(award_requirement('MVP',2026,[20]*62,{**e,'team_games_before_injury':73})['injury_exception_met'])
        self.assertFalse(award_requirement('MVP',2026,[20]*62,{**e,'joint_physician_season_ending_confirmed':None})['injury_exception_met'])

    def test_finals_award_and_future_law_are_not_mvp_attendance(self):
        self.assertEqual(award_requirement('Finals MVP',2027,None)['status'],'65_GAME_RULE_NOT_APPLICABLE')
        self.assertEqual(award_requirement('Finals MVP',2030,None)['status'],'FUTURE_CBA_NOT_VERIFIED')
        self.assertEqual(award_requirement('MVP',2030,[30]*82)['status'],'FUTURE_CBA_NOT_VERIFIED')

    def test_no_budget_test_selects_contracts_seasons_or_frozen_picks(self):
        x=build()
        self.assertEqual((len(x['core_cases']),len(x['apron_table_cases'])),(40,44))
        self.assertEqual(x['actual_future_frozen_picks'],[])
        self.assertTrue(all(not r['rule_check']['result_selected'] for r in x['award_targets']))
        for key in ['author_locked','season_selected','exact_execution_cleared','manuscript_allowed','actual_contracts_agreed','CBA_after_2030_verified']:
            self.assertFalse(x[key],key)


if __name__=='__main__':unittest.main()
