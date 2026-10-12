"""Counterexamples for final approval binding and the CLOSED boundary."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from verify_threepeat_current_final_review import check_author_approval, SCOPE_ID
from build_threepeat_actual_context_packs import digest

class ApprovalBindingTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'repo';self.root.mkdir()
  (self.root/'story.json').write_text('{"selected":true}\n',encoding='utf-8')
  self.pins={'story.json':digest(self.root/'story.json')}
  self.evidence={'review.json':{'LF_sha256':'f'*64}}
  self.blob=b'Submitted title/design proposal, CLOSED retained.\n'
  self.record={'selected':True,'kind':'FORMAL_TITLE_AND_WHOLE_DESIGN_FINAL_APPROVAL','prose_count':0,'authority_class':'AUTHOR_SELECTED','status':'AUTHOR_APPROVED_CURRENT_SELECTED_DESIGN',
   'approval_origin':'HUMAN_CURRENT_THREAD_REPLY','author_response_literal':'Approve the submitted proposal','scope_id':SCOPE_ID,
   'formal_title_choice':{'choice_id':'G00T_FORMAL_TITLE','selected':True,'option':'A','formal_title':'First Rebound'},
   'whole_design_approval':{'choice_id':'G17_FINAL_DESIGN_ACCEPTANCE','selected':True,'G17':True,'selected_title_years':[2023,2024,2025],'main_story_end_year':2025,'brief_retirement_year':2035,'current_units':10,'current_used_exit_ports':42,'final_episode_count':61,'main_episode_count':60,'brief_epilogue_count':1},
   'design_gate':'CLOSED','manuscript_allowed':False,'freeze':'v0.30 PARTIAL','gate_OPEN_authorized':False,
   'publication_authorized':False,'schedules_authorized':False,'unresolved_used_dependencies':[],
   'review_evidence_sha256':{'review.json':'f'*64},'approved_story_data_sha256':self.pins.copy(),
   'proposal_birth_ref':{'normalized_LF_sha256':hashlib.sha256(self.blob).hexdigest()}}
 def check(self,record=None,blob=None):
  return check_author_approval(self.root,record or self.record,self.evidence,self.pins,self.blob if blob is None else blob)
 def test_complete_bound_approval_remains_closed(self):
  self.assertTrue(self.check());self.assertFalse(self.record['manuscript_allowed'])
 def test_title_only_cannot_complete_G17(self):
  r=copy.deepcopy(self.record);r['whole_design_approval']['selected']=False;r['whole_design_approval']['G17']=False
  with self.assertRaises(AssertionError):self.check(r)
 def test_same_flags_cannot_approve_changed_story(self):
  (self.root/'story.json').write_text('{"selected":false}\n',encoding='utf-8')
  with self.assertRaises(AssertionError):self.check()
 def test_replaced_review_receipt_is_not_the_reviewed_version(self):
  r=copy.deepcopy(self.record);r['review_evidence_sha256']['review.json']='a'*64
  with self.assertRaises(AssertionError):self.check(r)
 def test_different_submitted_proposal_is_rejected(self):
  with self.assertRaises(AssertionError):self.check(blob=b'Open manuscript instead.\n')
 def test_final_design_acceptance_cannot_open_manuscript(self):
  r=copy.deepcopy(self.record);r['design_gate']='OPEN';r['manuscript_allowed']=True
  with self.assertRaises(AssertionError):self.check(r)

 def rejected_outside_story(self,key):
  outside=self.root.parent/'outside.json';outside.write_text('{}\n',encoding='utf-8')
  r=copy.deepcopy(self.record);pins={key:digest(outside)};r['approved_story_data_sha256']=pins
  with self.assertRaises(ValueError):check_author_approval(self.root,r,self.evidence,pins,self.blob)
 def test_absolute_story_source_cannot_escape_repository(self):
  self.rejected_outside_story(str(self.root.parent/'outside.json'))
 def test_parent_story_source_cannot_escape_repository(self):
  self.rejected_outside_story('../outside.json')
 def test_unchanged_flags_do_not_authorize_a_different_story_scope(self):
  for field,value in [('selected_title_years',[2028,2031]),('main_story_end_year',2031),('brief_retirement_year',2036),('current_units',9),('current_used_exit_ports',41)]:
   with self.subTest(field=field):
    r=copy.deepcopy(self.record);r['whole_design_approval'][field]=value
    with self.assertRaises(AssertionError):self.check(r)
 def test_approval_record_cannot_claim_prose_written(self):
  r=copy.deepcopy(self.record);r['prose_count']=1
  with self.assertRaises(AssertionError):self.check(r)
 def test_other_choice_ids_are_not_final_design_or_title_approval(self):
  for field in ['formal_title_choice','whole_design_approval']:
   with self.subTest(field=field):
    r=copy.deepcopy(self.record);r[field]['choice_id']='C01_CALENDAR'
    with self.assertRaises(AssertionError):self.check(r)

if __name__=='__main__':unittest.main()
