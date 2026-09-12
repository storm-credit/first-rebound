import json
import unittest
from build_2021_full_draft_comparison import INPUT,ROOT,build,second_round,overlay_roster


class FullComparisonTests(unittest.TestCase):
    def test_every_pick_compares_three_available_no_duplicates(self):
        x=build()
        for s in x['scenarios']+x['CHI39_options']:
            taken=set()
            for r in s['board']:
                self.assertGreaterEqual(len(r['available_comparison']),3)
                self.assertFalse(taken.intersection(r['available_comparison']))
                self.assertNotIn(r['proposed_player'],taken);taken.add(r['proposed_player'])
            self.assertEqual(len(taken),60)

    def test_lost_G3_candidates_are_not_saved_for_chicago(self):
        s=build()['scenarios'][0]
        self.assertEqual(s['CHI39'],'Joe Wieskamp')
        self.assertEqual(s['G3_39_candidates_taken_before_39'],{'Kessler Edwards':{'pick':34,'team':'NOP'},'Ayo Dosunmu':{'pick':23,'team':'NYK'},'Herbert Jones':{'pick':33,'team':'ORL'},'JT Thor':{'pick':30,'team':'UTA'}})

    def test_alternative39_propagates_to_later_teams(self):
        a,b,c,d=build()['CHI39_options']
        self.assertEqual([o['CHI39'] for o in [a,b,c,d]],['Joe Wieskamp','Sam Hauser','Austin Reaves','David Johnson'])
        self.assertEqual(a['board'][43]['proposed_player'],'BJ Boston')
        for s in [b,c,d]:self.assertEqual(s['board'][43]['proposed_player'],'Joe Wieskamp')
        self.assertEqual(b['board'][47]['proposed_player'],'David Johnson')

    def test_unpicked_candidates_stay_visible_and_old_remaining_compared(self):
        x=build();p=json.loads(INPUT.read_text());old=json.loads((ROOT/p['parent_round']).read_text())
        for o,s in zip(old['scenarios'],x['scenarios']):
            compared={n for r in s['board'][30:] for n in r['available_comparison']}
            self.assertTrue(set(o['tracked_candidates_remaining_for_second_round']).issubset(compared))
            picked={r['proposed_player'] for r in s['board']};unpicked=set(s['tracked_unselected_candidates'])
            self.assertEqual(picked|unpicked,set(x['tracked_candidate_pool']));self.assertFalse(picked&unpicked)

    def test_unavailable39_rejected_and_slot_replacement_not_addition(self):
        p=json.loads(INPUT.read_text());old=json.loads((ROOT/p['parent_round']).read_text());assets=json.loads((ROOT/p['parent_assets']).read_text())['scenarios'][0]
        with self.assertRaises(ValueError):second_round(old['scenarios'][0],assets,p,'Kessler Edwards')
        for s in build()['scenarios']+build()['CHI39_options']:
            self.assertEqual(len(s['named_roster_without_protagonist'])+1,15);self.assertEqual(s['gross_budget_delta_from_G3'],0)

    def test_comparison_completion_does_not_clear_world_gates(self):
        x=build();self.assertEqual(x['unjudged_pick_rows_in_this_comparison'],0)
        for k in ['full_draft_finally_selected','all_team_registration_completed','actual_participant_set_counterfactual_verified','author_locked','season_selected','exact_execution_cleared','manuscript_allowed']:
            self.assertFalse(x[k])
        self.assertIsNone(x['selected_scenario']);self.assertIsNone(x['selected_CHI39_option'])


if __name__=='__main__':unittest.main()
