"""Negative controls for substring ambiguity and component overcounting."""
import json
import unittest
from check_g11_delivery import ROOT, DATA, BASE, audit

class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.data,self.base=[json.loads((ROOT/p).read_text(encoding='utf-8')) for p in (DATA,BASE)]
    def check(self):return audit(self.data,self.base)
    def test_valid_references(self):self.assertEqual(self.check(),[])
    def test_twenty_component_chapters_is_overcount(self):
        self.data['component_chapters']=20;self.assertTrue(self.check())
    def test_literal_substring_is_not_unique_entity(self):
        self.data['literal_count_is_distinct_entity_count']=True;self.assertTrue(self.check())
    def test_homograph_exception_cannot_disappear(self):
        self.data['exceptions'].pop(1);self.assertTrue(self.check())
    def test_first_match_cannot_exceed_paragraph(self):
        self.data['selected_terms'][0]['first_in_cohort']['utf16_offset']=100000;self.assertTrue(self.check())
    def test_case_anchor_cannot_point_to_title(self):
        self.data['selected_cases'][0]['anchors']=[0];self.assertTrue(self.check())
    def test_density_cannot_be_inferred_from_selected_literals(self):
        self.data['professional_action_density']=0.4;self.assertTrue(self.check())
    def test_mechanical_checks_cannot_authenticate_wrong_meaning(self):
        self.data['selected_cases'][0]['own_functional_paraphrase']='협회 방문과 계약 체결을 완료했다.'
        self.assertEqual(self.check(),[])

if __name__=='__main__':unittest.main()
