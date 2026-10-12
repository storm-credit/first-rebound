"""Review exact prospective payloads, then publish them without changing reviewed bytes."""
import argparse, copy, hashlib, json
from pathlib import Path
from build_threepeat_actual_context_packs import authority_payload_digest, digest
ROOT=Path(__file__).resolve().parents[1]
DESIGN='design/THREEPEAT_61_CURRENT_REPAIRED_DESIGN_2026_10_12.json'
C01='canon/C01_GOLD_USED_CALENDAR_SELECTED_EXECUTION_2026_10_12.json'
B='canon/EARLY_REWARD_B_USED_IMPLEMENTATION_SELECTION_2026_10_12.json'
NREVIEW='reviews/THREEPEAT_CURRENT_NARRATIVE_INDEPENDENT_REVIEW_2026_10_12.json'
CREVIEW='reviews/THREEPEAT_C01_CURRENT_SELECTION_INDEPENDENT_REVIEW_2026_10_12.json'
PREVIEW='control/THREEPEAT_CURRENT_PACK_INPUT_PREVIEW_2026_10_12.json'
REVIEW='reviews/THREEPEAT_CURRENT_PACK_INPUT_INDEPENDENT_ACCEPTANCE_2026_10_12.json'
POLICY='canon/THREEPEAT_CURRENT_EPISODE_POLICY_SELECTION_2026_10_12.json'
SCOPE='control/THREEPEAT_CURRENT_PACK_SCOPE_AUTHORITY.json'
HISTORY='canon/THREEPEAT_CURRENT_SELECTED_HISTORY_AND_EXIT_LOCK.json'
ALLOCATION='design/THREEPEAT_FINAL_EPISODE_ALLOCATION.json'
BUNDLE='design/THREEPEAT_CURRENT_ACTUAL_EPISODE_BLUEPRINTS.json'
AUTHORITY='control/THREEPEAT_CURRENT_EPISODE_BLUEPRINT_AUTHORITY.json'
TARGET='control/CURRENT_SELECTED_THREEPEAT_BY_2025_MAIN_STORY_SCOPE_2026_10_09.json'
DELEGATION='canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def encode(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(v):return hashlib.sha256(encode(v)).hexdigest()
def actualsha(p):return digest(ROOT/p)
def ref(p,pointer='',prospective=None):return {'path':p,'source_sha256':sha(prospective[p]) if prospective and p in prospective else actualsha(p),'json_pointer':pointer}
def review_pin_matches(review,path):
 pins=review.get('current_review',{}).get('source_sha256',review.get('source_sha256',review.get('reviewed_artifacts_sha256',{})))
 return pins.get(path)==actualsha(path)
def build_preview():
 d=load(DESIGN);nr=load(NREVIEW);cr=load(CREVIEW)
 assert nr.get('status')=='ACCEPTED_CURRENT_NARRATIVE_DESIGN','Current narrative acceptance not issued'
 assert cr.get('status')=='PASS_FINITE_SELECTED_FICTIONAL_USED_CALENDAR','Current C01 acceptance not issued'
 assert review_pin_matches(nr,DESIGN),'Narrative acceptance is stale'
 assert review_pin_matches(cr,C01),'C01 acceptance is stale'
 assert nr['reviewer_id']!='root_codex' and cr['reviewer_id']!='root_codex'
 sid=d['scope_id'];common={'scope_id':sid,'producer_id':'root_codex','manuscript_allowed':False,'design_gate':'CLOSED','freeze':'v0.30 PARTIAL'}
 policy={'minimum_percent':75,'maximum_percent':85,'denominator':'ALL_FINAL_EPISODES','counted_categories':['NBA']}
 # Labels describe editorial function; they are not character knowledge.
 policy['category_definitions']={'NBA':'NBA입단후 경기·역할·계약·훈련과NBA참여를 직접 바꾸는 대표활동/병역비용이 중심인 회차.',
  'NBA_DRAFT':'2018earlyentry/workout/draft와입단심사가중심인회차;NBA비율에세지않음.',
  'PRE_NBA':'NBA입단전 입문·prep·NCAA 경기/학업/관계가중심인회차.',
  'POST_NBA':'NBA서비스종료후 짧은2035guest/공개은퇴회차.'}
 selection={'selected':True,'status':'SELECTED_FICTIONAL_USED_RESOLUTION','authority_class':'DELEGATED_SELECTED','unresolved_used_dependencies':[],
  'producer_id':'root_codex','authority_basis':ref(DELEGATION),'independent_narrative_acceptance':ref(NREVIEW)}
 category=dict(selection,choice_id='CURRENT_EPISODE_CATEGORY_POLICY',kind='EPISODE_CATEGORY_POLICY',policy=policy,
  resolution='현재61회는NBA46회만75–85비율에세며드래프트3회는별도분류한다. 동일한명시적정의로모든회차를배정한다.')
 allocation_selection=dict(selection,choice_id='CURRENT_FINAL_EPISODE_ALLOCATION',kind='FINAL_EPISODE_ALLOCATION',
  final_episode_count=61,main_episode_count=60,brief_epilogue_count=1,
  resolution='독립수락된실질적61회수리를최종설계배치로선택한다. 2024/25동부대결·MIN결승진행은새승패없이개별선택/비용으로분리하며원고분량통과를뜻하지않는다.')
 files={POLICY:{'id':'THREEPEAT_CURRENT_EPISODE_POLICY_SELECTION_2026_10_12','producer_id':'root_codex',
  'status':'DELEGATED_SELECTED_CURRENT_EPISODE_POLICY','category_policy':category,'episode_allocation':allocation_selection}}
 scope=dict(common,status='LOCKED_CURRENT_PACK_SCOPE',active_unit_ids=[u['unit_id'] for u in d['unit_exits']],
  required_exit_port_ids=[p['port_id'] for p in d['finite_used_exit_ports']],selected_scope_ref=ref(TARGET,'/selected_design_targets'),
  category_policy=dict(policy,selection_source_ref=ref(POLICY,'/category_policy',files)),
  consequential_choice_requirements=[{'choice_id':'C01_CALENDAR','kind':'CALENDAR_AVAILABILITY','use_mode':'USED'},
   {'choice_id':'EARLY_REWARD_IMPLEMENTATION','kind':'EARLY_CAREER_REWARD','use_mode':'USED'}])
 files[SCOPE]=scope
 ports=copy.deepcopy(d['finite_used_exit_ports']);units=copy.deepcopy(d['unit_exits'])
 for p in ports:p['status']='SELECTED_RESOLVED'
 for u in units:u['status']='SELECTED_RESOLVED'
 choices=[]
 for cid,path,ids in [('C01_CALENDAR',C01,['FC031','FC032','FC040']),('EARLY_REWARD_IMPLEMENTATION',B,[f'FC{k:03}' for k in range(12,23)])]:
  choices.append({'choice_id':cid,'status':'RESOLVED_SELECTED','used_port_ids':ids,'selection_source_ref':ref(path),'resolution':load(path)['resolution']})
 files[HISTORY]=dict(common,status='LOCKED_CURRENT_SELECTED_HISTORY',current_used_scope_complete=True,
  finite_used_exit_ports=ports,unit_exits=units,consequential_choices=choices,
  acceptance_scope='Finite current used design, not all historical/private truth or future law.',
  current_design_source=ref(DESIGN),current_C01_acceptance=ref(CREVIEW),current_narrative_acceptance=ref(NREVIEW))
 blueprints=copy.deepcopy(d['episodes'])
 for e in blueprints:
  e.update(common,status='ACTUAL_VERIFIED')
  e['information_boundary']['status']='LOCKED_SELECTED_SCENE_ACCESS'
  e['information_boundary']['clock_order_verified']=True
  e['qualification_scope']='Independentlyaccepted current design/access; prose_NOT_REVIEWED.'
 files[BUNDLE]=dict(common,status='ACTUAL_VERIFIED_CURRENT_BLUEPRINT_BUNDLE',episode_blueprints=blueprints,
  design_ref=ref(DESIGN),narrative_acceptance=ref(NREVIEW),C01_acceptance=ref(CREVIEW),prose_verified=False)
 keys=['episode','unit_id','category','episode_function','action_choice','durable_cost','state_change','entry_state','exit_state_required','consumed_exit_port_ids','consequential_choice_ids']
 episode_rows=[{k:e[k] for k in keys} for e in blueprints]
 files[ALLOCATION]=dict(common,status='LOCKED_CURRENT_FINAL_EPISODE_FUNCTION_TABLE',final_episode_count=61,episodes=episode_rows,
  selection_source_ref=ref(POLICY,'/episode_allocation',files),current_design_ref=ref(DESIGN),prose_length_verified=False)
 auth=dict(common,status='ACTUAL_CURRENT_BLUEPRINT_AUTHORITY',episode_authorities=[
  {'episode':e['episode'],'qualified_status':'ACTUAL_VERIFIED','blueprint':ref(BUNDLE,'/episode_blueprints/'+str(i),files)} for i,e in enumerate(blueprints)],
  independent_review={'path':REVIEW,'source_sha256':'PENDING_EXACT_INDEPENDENT_ACCEPTANCE'})
 files[AUTHORITY]=auth
 used={}
 def walk(v):
  if isinstance(v,dict):
   if isinstance(v.get('path'),str) and 'source_sha256' in v and v['path']!=REVIEW:
    p=v['path'];expected=sha(files[p]) if p in files else actualsha(p)
    assert v['source_sha256']==expected,('Stale prospective source',p)
    used[p]=expected
   for x in v.values():walk(x)
  elif isinstance(v,list):
   for x in v:walk(x)
 for v in files.values():walk(v)
 for p in [SCOPE,HISTORY,ALLOCATION,BUNDLE]:used[p]=sha(files[p])
 return {'id':'THREEPEAT_CURRENT_PACK_INPUT_PREVIEW_2026_10_12','producer_id':'root_codex',
  'status':'PROSPECTIVE_REVIEW_PAYLOAD_NOT_ISSUED_AUTHORITY_OR_PACK',
  'publication_contract':'Reviewer inspects these exactprospectivepayloads andlive sources. Afteracceptancepublishunchangedfiles; onlyauthorityindependent_review hash excludedfrompayloadhash isfilledwithactualreceipt.',
  'prospective_files':files,'reviewed_artifacts_expected_sha256':used,
  'reviewed_authority_payload_expected_sha256':authority_payload_digest(auth),
  'actual_Pack_count':0,'manuscript_allowed':False}
def publish():
 preview=load(PREVIEW);review=load(REVIEW);files=copy.deepcopy(preview['prospective_files'])
 assert review['status']=='ACCEPTED_CURRENT_THREEPEAT_PACK_INPUTS' and review['independent_review_completed'] is True
 assert review['reviewer_id']!='root_codex'
 assert review['reviewed_authority_payload_sha256']==preview['reviewed_authority_payload_expected_sha256']
 for p,h in preview['reviewed_artifacts_expected_sha256'].items():
  assert review['reviewed_artifacts_sha256'][p]==h
  assert (sha(files[p]) if p in files else actualsha(p))==h
 files[AUTHORITY]['independent_review']['source_sha256']=actualsha(REVIEW)
 for p,v in files.items():
  path=ROOT/p
  if path.exists():assert digest(path)==sha(v),('Refusing different existing authority',p)
 for p,v in files.items():
  if not (ROOT/p).exists():(ROOT/p).write_bytes(encode(v))
 print(json.dumps({'published_authority_files':len(files),'manuscript_allowed':False}))
def main():
 p=argparse.ArgumentParser();p.add_argument('--publish',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--refresh-owned',action='store_true');p.add_argument('--expected-hash');a=p.parse_args()
 if a.publish:return publish()
 raw=encode(build_preview());path=ROOT/PREVIEW
 if a.check:assert path.read_bytes().replace(b'\r\n',b'\n')==raw
 elif path.exists():
  assert a.refresh_owned and a.expected_hash in {actualsha(PREVIEW),hashlib.sha256(path.read_bytes()).hexdigest()},'Exact owned preview hash required'
  (ROOT/'Temp/pack_preview_before_refresh.json').write_bytes(path.read_bytes());path.write_bytes(raw)
 else:path.write_bytes(raw)
 print(json.dumps({'preview_created':True,'actual_authorities_issued':False,'actual_Pack_count':0}))
if __name__=='__main__':main()
