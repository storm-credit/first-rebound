import json,unittest
import check_g11_common_minimum as m
class ScopeTests(unittest.TestCase):
    def setUp(self):
        self.d=json.loads((m.ROOT/m.PATH).read_text(encoding='utf-8'));self.o=json.loads((m.ROOT/m.OPENING).read_text(encoding='utf-8'))
    def test_current_record(self):self.assertEqual(m.validate(self.d,self.o),[])
    def test_unmapped_prefix(self):
        for t in self.d['records'][0]['first1000_all_display_blocks_coded']:
            t['raw_p_indexes']=[i for i in t['raw_p_indexes'] if i!=3]
        self.assertIn('unmapped prefix block',m.validate(self.d,self.o))
    def test_full_paragraph_outside_cutoff_cannot_count(self):
        self.d['records'][2]['first1000_all_display_blocks_coded'][0]['raw_p_indexes'].append(24)
        self.assertIn('tag outside prefix or duplicated',m.validate(self.d,self.o))
    def test_changed_official_body(self):
        self.d['records'][0]['body_sha256']='0'*64
        self.assertIn('official identity/hash mismatch',m.validate(self.d,self.o))
    def test_no_whole_p3_from_one_work(self):
        self.d['whole_P3_final']=True
        self.assertIn('scope promotion: whole_P3_final',m.validate(self.d,self.o))
    def test_wrong_presence_fraction(self):
        self.d['records'][0]['first1000_all_display_blocks_coded'][0]['text_presence_fraction']=1
        self.assertIn('tag arithmetic mismatch',m.validate(self.d,self.o))
if __name__=='__main__':unittest.main()
