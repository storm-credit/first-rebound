import json
import unittest
from copy import deepcopy
from build_2021_draft_assets import INPUT,ROOT,build,project,settle_2023,settle_2025,transfer


class AssetTests(unittest.TestCase):
    def test_origins_not_old_ordinals(self):
        x=build();rows=x['scenarios'][0]['rows'];owners={r['pick']:r['owner'] for r in rows}
        self.assertEqual({p:owners[p] for p in [16,34,35,37,38,39,40,49,52,53,57,58]},dict(zip([16,34,35,37,38,39,40,49,52,53,57,58],['OKC','NOP','OKC','DET','DET','CHI','NOP','MEM','NOP','DET','NYK','CHA'])))
        self.assertEqual(len({(r['round'],r['origin']) for r in rows}),60)

    def test_nop_trade_maps_four_identities(self):
        a,b=build()['scenarios'][:2];delta=[(x['pick'],x['owner'],y['owner']) for x,y in zip(a['rows'],b['rows']) if x['owner']!=y['owner']]
        self.assertEqual(delta,[(9,'NOP','MEM'),(17,'MEM','NOP'),(40,'NOP','MEM'),(49,'MEM','NOP')])
        self.assertFalse(b['G4_top14_compatible']);self.assertTrue(b['requires_new_top14_board'])

    def test_cash_sale_is_separate_dated_event(self):
        p=json.loads(INPUT.read_text());d=json.loads((ROOT/p['parent']).read_text());s=p['scenarios'][0]
        p['cash_sale_dal_second']=True;rows=project(p,d,s)['rows']
        self.assertEqual(rows[51]['owner'],'PHI');self.assertEqual(rows[52]['owner'],'DET')
        with self.assertRaises(ValueError):transfer(rows,2,'DAL','NOP','PHI','duplicate')

    def test_2025_complements_do_not_double_spend(self):
        for ranks in [dict(BOS=40,MEM=50),dict(BOS=50,MEM=40)]:
            yes=settle_2025(ranks,True);no=settle_2025(ranks,False)
            self.assertEqual([r['owner'] for r in yes],['OKC','ORL']);self.assertEqual([r['owner'] for r in no],['BOS','ORL'])
            self.assertEqual(len({r['origin'] for r in yes}),2)

    def test_2023_nested_selector_not_worst_of_four(self):
        for row in build()['future_2023_permutations']:
            r=row['ranks'];eligible=[r['OKC'],r['WAS'],min(r['DAL'],r['MIA'])]
            self.assertEqual(row['recipient_BOS_if_kemba']['pick'],max(eligible))
        special=dict(OKC=31,WAS=32,DAL=59,MIA=60)
        self.assertEqual(settle_2023(special)['origin'],'DAL')
        with self.assertRaises(ValueError):settle_2025(dict(BOS=40,MEM=40),True)
        with self.assertRaises(ValueError):settle_2023(dict(OKC=1,WAS=32,DAL=59,MIA=60))

    def test_no_canon_or_full_draft_promotion(self):
        x=build();self.assertEqual(x['projection_rows'],240)
        for k in ['author_locked','season_selected','exact_execution_cleared','manuscript_allowed','final_60_pick_control_verified','original_lottery_rerun']:
            self.assertFalse(x[k])
        self.assertIsNone(x['selected_scenario']);self.assertIsNone(x['actual_future_ranks'])
        self.assertEqual({(s['boston_kemba'],s['nop_mem']) for s in x['scenarios']},{(a,b) for a in [True,False] for b in [True,False]})


if __name__=='__main__':unittest.main()
