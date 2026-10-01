import json,unittest
from check_g11_component_cohort import ROOT,EXTRA_DATA,audit,canonical
class ExtraTests(unittest.TestCase):
    def setUp(self):
        self.d=json.loads((ROOT/EXTRA_DATA).read_text(encoding='utf-8'));self.ledger=json.loads((ROOT/'research/STYLE_READING_OBSERVATIONS.json').read_text(encoding='utf-8'))
    def check(self):return audit(self.d,self.ledger,'EXTRA')
    def test_valid(self):self.assertEqual(self.check(),[])
    def test_shared_scope_overcount(self):self.d['component_chapters']=75;self.assertIn('component/reading overcount',self.check())
    def test_footer_included(self):self.d['metrics'][0]['paragraph_meta'].append([98,38]);self.assertTrue(self.check())
    def test_robot_is_not_person(self):
        v=self.d['metrics'][3]['voice_indexes'];v['CHARACTER_SPEECH'].append(106);v['MEDIATED_MACHINE_SPEECH']=[];self.d['metrics'][3]['canonical_sha256']=canonical(self.d['metrics'][3]);self.assertIn('context exception lost',self.check())
    def test_unmeasured_inner_ratio(self):self.d['total_inner_share']=0;self.assertIn('unmeasured semantic ratio',self.check())
    def test_selected_term_address(self):self.d['terms'][0]['first']=[1,9,0];self.assertIn('literal position out of bounds',self.check())
    def test_missing_function_region(self):self.d['episodes'][4]['blocks'].pop(0);self.assertIn('functional blocks duplicate/gap/order',self.check())
    def test_scope_validator_does_not_certify_pov_meaning(self):
        self.d['episodes'][4]['expression']='다른 인물의 속생각을 주인공이 모두 알고 있다.';self.assertEqual(self.check(),[])
if __name__=='__main__':unittest.main()
