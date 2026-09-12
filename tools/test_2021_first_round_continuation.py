import json
import unittest
from copy import deepcopy
from build_2021_first_round_continuation import INPUT,ROOT,build,resolve,future_settlement


class ContinuationTests(unittest.TestCase):
    def test_target_loss_cancels_trade_and_preserves_future_assets(self):
        a,b,c,d=build()['scenarios']
        self.assertEqual([s['board'][15]['team'] for s in [a,b,c,d]],['HOU','HOU','HOU','OKC'])
        self.assertEqual(d['transaction_proposals'],[]);self.assertEqual(d['future_DET_WAS_rights_owner_after_proposal'],'HOU')
        self.assertEqual([r['proposed_player'] for r in d['board'][14:17]],['Trey Murphy','Ziaire Williams','James Bouknight'])
        self.assertEqual([r['proposed_player'] for r in a['board'][14:17]],['Trey Murphy','Alperen Sengun','Ziaire Williams'])

    def test_three_actual_remaining_candidates_every_pick(self):
        for s in build()['scenarios']:
            taken=set()
            for r in s['board']:
                self.assertGreaterEqual(len(r['available_comparison']),3)
                self.assertFalse(taken.intersection(r['available_comparison']))
                self.assertNotIn(r['proposed_player'],taken);taken.add(r['proposed_player'])
            self.assertEqual(len(taken),30)

    def test_no_unseen_candidate_drops_from_top14(self):
        p=json.loads(INPUT.read_text());g4=json.loads((ROOT/p['parent_board']).read_text())
        for old,new in zip(g4['scenarios'],build()['scenarios']):
            compared={n for r in new['board'][14:] for n in r['available_comparison']}
            self.assertTrue(set(old['tracked_candidates_not_yet_picked']).issubset(compared))

    def test_incompatible_assets_are_rejected(self):
        p=json.loads(INPUT.read_text());g4=json.loads((ROOT/p['parent_board']).read_text());g5=json.loads((ROOT/p['parent_assets']).read_text())
        with self.assertRaises(ValueError):resolve(g4['scenarios'][0],g5['scenarios'][1],p)
        with self.assertRaises(ValueError):resolve(g4['scenarios'][0],g5['scenarios'][0],p,{'15':['Trey Murphy']})

    def test_future_protection_threshold_and_termination(self):
        det,was=json.loads(INPUT.read_text())['sengun_future_picks']
        self.assertEqual(future_settlement(det,{'2022':17})['status'],'CONVEYS_FIRST')
        early=future_settlement(det,{'2022':16,'2023':19});self.assertEqual(early['asset']['year'],2023);self.assertEqual(early['later_obligations'],[])
        for t in [det,was]:
            allprotected=dict(t['first_protection_by_year']);out=future_settlement(t,allprotected)
            self.assertEqual(out['status'],'CONVERTS_TO_SECONDS');self.assertEqual(out['assets'],t['if_never_conveys'])
            last=max(allprotected);allprotected[last]+=1
            self.assertEqual(future_settlement(t,allprotected)['status'],'CONVEYS_FIRST')
        self.assertEqual(future_settlement(was,{'2026':9})['status'],'HOLD_MISSING_EARLIER_YEAR')

    def test_no_39_availability_or_canon_promotion(self):
        x=build();self.assertEqual(x['new_comparison_rows'],64);self.assertEqual(x['unjudged_second_round_picks'],30)
        for k in ['first_round_finally_selected','author_locked','season_selected','exact_execution_cleared','manuscript_allowed','original_lottery_rerun']:
            self.assertFalse(x[k])
        for s in x['scenarios']:
            self.assertIsNone(s['CHI39_proposed_player']);self.assertFalse(s['CHI39_availability_verified'])
            self.assertFalse(s['actual_contracts_agreed'])


if __name__=='__main__':unittest.main()
