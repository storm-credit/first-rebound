import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import check_chicago_2021_m1_role_witness as m
class M1WitnessTests(unittest.TestCase):
    def setUp(self):self.d=m.load(m.INPUT)
    def test_original(self):self.assertEqual(m.validate(self.d),[])
    def test_duplicate_player(self):
        w=self.d['lineup_witness'][0]['positions'];w['PF']=w['SF'];self.assertTrue(m.validate(self.d))
    def test_minutes_and_delta(self):
        self.d['lineup_witness'][0]['minutes']+=2;self.assertTrue(m.validate(self.d))
        self.d=m.load(m.INPUT);self.d['position_minutes']['PF']['Markkanen']-=4;self.assertTrue(m.validate(self.d))
    def test_creator_removed(self):
        w=self.d['lineup_witness'][0]['positions'];w['PG']='Caruso';w['SG']='Coby';self.assertIn('creator coverage',m.validate(self.d))
    def test_promotion_and_stale(self):
        for field in ['actual_minutes_selected','season_selected','registration_verified','health_verified','substitution_order_selected','full_roster_selected','manuscript_allowed']:
            d=copy.deepcopy(self.d);d[field]=True;self.assertTrue(m.validate(d))
        self.d['source_sha256'].pop(next(iter(self.d['source_sha256'])));self.assertTrue(m.validate(self.d))
    def test_summaries_not_authority(self):
        self.d['derived_player_minutes']['Caruso']=22;self.assertTrue(m.validate(self.d))
        self.d=m.load(m.INPUT);self.d['elapsed_minutes']=50;self.assertTrue(m.validate(self.d))
    def test_illegal_position(self):
        self.d['lineup_witness'][0]['positions']['C']='Protagonist';self.assertTrue(m.validate(self.d))
    def test_no_actual_event(self):
        self.d['game_date']='2021-10-20';self.assertTrue(m.validate(self.d))
        self.d=m.load(m.INPUT);self.d['contract_acceptances_selected']=['Caruso'];self.assertTrue(m.validate(self.d))
if __name__=='__main__':unittest.main()
