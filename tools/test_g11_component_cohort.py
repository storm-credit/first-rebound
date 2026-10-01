import json,unittest
from check_g11_component_cohort import ROOT,DATA,audit,canonical
class CohortTests(unittest.TestCase):
    def setUp(self):
        self.d=json.loads((ROOT/DATA).read_text(encoding='utf-8'));self.ledger=json.loads((ROOT/'research/STYLE_READING_OBSERVATIONS.json').read_text(encoding='utf-8'))
    def check(self):return audit(self.d,self.ledger)
    def rehash(self,c):self.d['metrics'][c]['canonical_sha256']=canonical(self.d['metrics'][c])
    def test_valid(self):self.assertEqual(self.check(),[])
    def test_component_overcount(self):self.d['component_chapters']=50;self.assertTrue(self.check())
    def test_legacy_scope_difference(self):self.ledger['metrics']['chapters'][0]['paragraph_lengths'][-1]=14;self.assertIn('legacy scope reconciliation',self.check())
    def test_capture_payload_tamper(self):self.d['metrics'][0]['body_sha256']='0'*64;self.assertTrue(self.check())
    def test_raw_normalized_difference(self):self.d['metrics'][0]['viewer_whitespace_trimmed_utf16']=0;self.rehash(0);self.assertIn('viewer normalization accounting',self.check())
    def test_join_boundary_first1000(self):self.d['metrics'][3]['prefix_last_intersection']=[71,1000,10,1];self.rehash(3);self.assertIn('first1000 clipping',self.check())
    def test_block_gap(self):self.d['episodes'][0]['blocks'][0]['end']=53;self.assertIn('functional blocks duplicate/gap/order',self.check())
    def test_anchor_outside_block(self):self.d['episodes'][2]['blocks'][0]['selected_anchors']=[263];self.assertIn('functional anchor/inventory',self.check())
    def test_past_quote_moved_to_present(self):
        v=self.d['metrics'][1]['voice_indexes'];v['CHARACTER_SPEECH']+=v['PAST_REPORTED_SPEECH'];v['PAST_REPORTED_SPEECH']=[];self.rehash(1);self.assertIn('context exception lost',self.check())
    def test_gasp_as_dialogue(self):
        v=self.d['metrics'][3]['voice_indexes'];v['CHARACTER_SPEECH'].append(9);v['NONVERBAL']=[];self.rehash(3);self.assertIn('context exception lost',self.check())
    def test_term_outside_paragraph(self):self.d['terms'][0]['first'][2]=99999;self.assertIn('literal position out of bounds',self.check())
    def test_wrong_official_url(self):self.d['metrics'][0]['url']='https://example.com';self.rehash(0);self.assertIn('official chapter missing in reading ledger',self.check())
    def test_no_source_semantic_certification(self):
        self.d['episodes'][4]['reward']='실물 말과 기업 소유권을 이미 얻었다.';self.assertEqual(self.check(),[])
if __name__=='__main__':unittest.main()
