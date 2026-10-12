"""Read-only proof of current whole design reviews; never approve G17."""
import json
from pathlib import Path
from build_threepeat_actual_context_packs import ROOT,digest
REVIEWS=[('reviews/THREEPEAT_CURRENT_G15_WHOLE_INTEGRATION_REVIEW_2026_10_12.json','PASS_CURRENT_SELECTED_DESIGN_INTEGRATION','source_sha256'),
 ('reviews/THREEPEAT_CURRENT_G16_WHOLE_DESIGN_INDEPENDENT_REVIEW_2026_10_12.json','PASS_CURRENT_SELECTED_WHOLE_DESIGN','reviewed_artifacts_sha256'),
 ('reviews/VILLANOVA_2017_18_CURRENT_AID_COUNTER_INDEPENDENT_REVIEW_2026_10_12.json','PASS_SELECTED_FICTIONAL_AID_COUNTER_FAMILY','source_sha256')]
def main():
 evidence={}
 for p,status,key in REVIEWS:
  a=json.loads((ROOT/p).read_text(encoding='utf-8-sig'));assert a['status']==status and a['reviewer_id']!='root_codex'
  for source,h in a[key].items():assert digest(ROOT/source)==h,(source,'stale review')
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
 for p,h in close['pack_file_sha256'].items():assert digest(ROOT/p)==h,(p,'changed Pack')
 return {'status':'CURRENT_G15_G16_COMPLETE_G17_AUTHOR_APPROVAL_PENDING','review_evidence':evidence,'used_blockers':0,'unchanged_actual_Packs':61,
  'remaining_technical_design_tasks':0,'remaining_author_approval':1,'G17':False,'manuscript_allowed':False,'design_gate':'CLOSED','freeze':'v0.30 PARTIAL'}
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False))
