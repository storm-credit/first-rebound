"""Read-only proof of current whole design reviews; never approve G17."""
import json
import hashlib
import subprocess
from pathlib import Path
from build_threepeat_actual_context_packs import ROOT,digest,safe_path
REVIEWS=[('reviews/THREEPEAT_CURRENT_G15_WHOLE_INTEGRATION_REVIEW_2026_10_12.json','PASS_CURRENT_SELECTED_DESIGN_INTEGRATION','source_sha256'),
 ('reviews/THREEPEAT_CURRENT_G16_WHOLE_DESIGN_INDEPENDENT_REVIEW_2026_10_12.json','PASS_CURRENT_SELECTED_WHOLE_DESIGN','reviewed_artifacts_sha256'),
 ('reviews/VILLANOVA_2017_18_CURRENT_AID_COUNTER_INDEPENDENT_REVIEW_2026_10_12.json','PASS_SELECTED_FICTIONAL_AID_COUNTER_FAMILY','source_sha256')]

APPROVAL = 'canon/FINAL_TITLE_AND_DESIGN_AUTHOR_APPROVAL_2026_10_12.json'
SCOPE_ID = 'THREEPEAT_2023_2025_NINE_ACTS_BRIEF2035_CURRENT'

def check_author_approval(root, approval, evidence, expected_pins, proposal_bytes):
 """Validate a persisted human decision against its submitted version and live data.
 This does not authenticate human authorship; the trusted chat is the authority.
 """
 assert approval['selected'] is True
 assert approval['kind'] == 'FORMAL_TITLE_AND_WHOLE_DESIGN_FINAL_APPROVAL'
 assert approval['authority_class'] == 'AUTHOR_SELECTED'
 assert approval['status'] == 'AUTHOR_APPROVED_CURRENT_SELECTED_DESIGN'
 assert approval['approval_origin'] == 'HUMAN_CURRENT_THREAD_REPLY'
 assert approval['author_response_literal'].strip()
 assert approval['scope_id'] == SCOPE_ID
 title = approval['formal_title_choice']
 assert title['selected'] is True and title['option'] == 'A' and title['formal_title'] == 'First Rebound'
 assert title['choice_id'] == 'G00T_FORMAL_TITLE'
 design = approval['whole_design_approval']
 assert design['selected'] is True and design['G17'] is True
 assert design['choice_id'] == 'G17_FINAL_DESIGN_ACCEPTANCE'
 assert design['selected_title_years'] == [2023,2024,2025]
 assert design['main_story_end_year'] == 2025 and design['brief_retirement_year'] == 2035
 assert design['current_units'] == 10 and design['current_used_exit_ports'] == 42
 assert approval['prose_count'] == 0
 assert (design['final_episode_count'], design['main_episode_count'], design['brief_epilogue_count']) == (61,60,1)
 assert approval['design_gate'] == 'CLOSED' and approval['manuscript_allowed'] is False
 assert approval['freeze'] == 'v0.30 PARTIAL'
 assert all(approval[k] is False for k in ['gate_OPEN_authorized','publication_authorized','schedules_authorized'])
 assert approval['unresolved_used_dependencies'] == []
 expected_reviews = {p: row['LF_sha256'] for p,row in evidence.items()}
 assert approval['review_evidence_sha256'] == expected_reviews, 'Approval binds different review receipts'
 assert approval['approved_story_data_sha256'] == expected_pins, 'Approval binds different story data'
 for source,h in expected_pins.items():
  assert digest(safe_path(Path(root),source)) == h, ('Stale approved story',source)
 normalized = proposal_bytes.decode('utf-8-sig').replace('\r\n','\n').replace('\r','\n')
 assert hashlib.sha256(normalized.encode()).hexdigest() == approval['proposal_birth_ref']['normalized_LF_sha256'], 'Submitted proposal differs'
 return True

def main():
 evidence={}
 for p,status,key in REVIEWS:
  a=json.loads((ROOT/p).read_text(encoding='utf-8-sig'));assert a['status']==status and a['reviewer_id']!='root_codex'
  for source,h in a[key].items():assert digest(safe_path(ROOT,source))==h,(source,'stale review')
  for source,h in a.get('common_guideline_sha256',{}).items():assert digest(Path(source))==h
  evidence[p]={'LF_sha256':digest(ROOT/p),'actual_review_status':status,'reviewer_id':a['reviewer_id'],'current_source_pins':len(a[key])}
 g16=json.loads((ROOT/REVIEWS[1][0]).read_text(encoding='utf-8-sig'));assert g16['independent_review_completed'] is True and g16['used_blocker_count']==0 and g16['G17_author_final_approval'] is False
 family=json.loads((ROOT/'canon/VILLANOVA_2017_18_SELECTED_AID_COUNTER_FAMILY_2026_10_12.json').read_text(encoding='utf-8-sig'))
 rows=family['named_allocation'];assert len(rows)==16 and len({r['actor'] for r in rows})==16 and sum(r['counter'] for r in rows)==12
 assert next(r for r in rows if r['actor']=='Dylan Painter')['counter']==1
 assert next(r for r in rows if r['actor']=='PROTAGONIST')['counter']==1
 for r in rows:
  if r['counter']==0:assert all(r[k]=='ZERO' for k in ['athletics_related_institutional_aid','other_institutional_aid','government_institutionally_administered_or_waiver_aid','NGB_USOC_or_foreign_equivalent_educational_aid','outside_athletics_based_or_booster_aid'])
 close=json.loads((ROOT/'reviews/THREEPEAT_CURRENT_MACRO1_6_CLOSEOUT_2026_10_12.json').read_text(encoding='utf-8-sig'))
 for p,h in close['pack_file_sha256'].items():assert digest(safe_path(ROOT,p))==h,(p,'changed Pack')
 approved = False
 approval_ref = None
 if (ROOT/APPROVAL).exists():
  approval = json.loads((ROOT/APPROVAL).read_text(encoding='utf-8-sig'))
  proposal = approval['proposal_birth_ref']
  assert len(proposal['git_commit']) == 40 and all(c in '0123456789abcdef' for c in proposal['git_commit'])
  assert proposal['path'] == 'design/THREEPEAT_CURRENT_FINAL_AUTHOR_REVIEW_PACKET_2026_10_12.md'
  blob = subprocess.check_output(['git','show',proposal['git_commit']+':'+proposal['path']],cwd=ROOT)
  approved = check_author_approval(ROOT,approval,evidence,g16['reviewed_artifacts_sha256'],blob)
  approval_ref = {'path':APPROVAL,'LF_sha256':digest(ROOT/APPROVAL)}
 return {'status':'CURRENT_SELECTED_DESIGN_AUTHOR_APPROVED_CLOSED' if approved else 'CURRENT_G15_G16_COMPLETE_G17_AUTHOR_APPROVAL_PENDING',
  'review_evidence':evidence,'used_blockers':0,'unchanged_actual_Packs':61,'remaining_technical_design_tasks':0,
  'remaining_author_approval':0 if approved else 1,'remaining_author_locks_count':0 if approved else 2,
  'G00T':approved,'formal_title':'First Rebound' if approved else None,'G17':approved,'author_approval_ref':approval_ref,
  'manuscript_allowed':False,'design_gate':'CLOSED','freeze':'v0.30 PARTIAL'}
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False))
