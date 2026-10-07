"""Audit existing A01 coverage; extract only the selected, uncovered E2 W addendum.

No new event, dialogue, prose, Pack or ACTUAL_VERIFIED promotion. Mutable
central progress is checked through the consumed anchors, not a new full-file
current-hash prerequisite after every unrelated milestone.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, re, subprocess
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a01_remaining_verified_blueprint_bundle.py'
OUT = 'design/A01_REMAINING_VERIFIED_BLUEPRINT_BUNDLE_2026_10_08.json'
REGISTER = 'control/G13_A14_FUNCTION_EXECUTION_REGISTER_2026_10_08.json'
OVERLAY = 'design/A01_E2_LITERAL_COST_WITNESS_SELECTED_OVERLAY_2026_10_08.json'
PEER = 'reviews/A01_E2_LITERAL_COST_WITNESS_ROOT_INDEPENDENT_REVIEW_2026_10_08.json'
SCHOOL = 'design/A01_TRIAL_SCHOOL_OPERATING_PATH_2026_10_07.json'
ORIGINAL = ['design/A01_OPENING_BLUEPRINT.json', 'design/A01_FIRST_TRIAL_BLUEPRINT.json', 'design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json']
ORIGINAL_REVIEWS = ['reviews/A01_OPENING_BLUEPRINT_REVIEW_2026_10_04.json', 'reviews/A01_FIRST_TRIAL_BLUEPRINT_REVIEW_2026_10_05.json', 'reviews/A01_FIRST_CONTRIBUTION_BLUEPRINT_REVIEW_2026_10_05.json']
MUTABLE = {'canon/PROJECT_FREEZE.md', 'canon/CAREER_TIMELINE.md', 'control/DESIGN_GATE.md'}
PINS = {'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md': '04599ed159bb2d5a28ae24e58815606a37f9e263d184315b47b826e7c1c8aa57', 'canon/CHARACTER_RESPONSIBILITY_ARC.md': '6cf722df3c56c2063cc5d6268b8813a956031b88e91059ebd05d01eb9468acfb', 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json': '4ee9b74e37903a43b0bd50b35c7f24cbabdac13728097a848b553f874bbeef80', 'canon/STORY_BIBLE.md': '9eb986c089c07007caedc40eabe03d6d798f77f7a09fbd37d57c4242af1421be', 'context-packs/README.md': 'a28022af8967907acd59e206b381ac8079c393538b63fd70f17b9bc79a882704', 'design/A01_CF07_BOXOUT_WORKING_MODEL_2026_10_07.json': 'e15586f74a87b878dbae237f3b34d595d22a767254859193ca778b4a2cf5c91a', 'design/A01_CF08_TEAM_PREPARATION_WORKING_MODEL_2026_10_07.json': 'a84761b2b24f88f3729ab37742f8792c766278a976ee8863934a6fe7766dea61', 'design/A01_CF09_GAME_PRIORITY_WORKING_MODEL_2026_10_07.json': 'ec51129b069df8f174bb22c9d57da30bcfff2a28f1b488ba8b0acd11eb52f2b5', 'design/A01_CF10_PREP_COMPARISON_WORKING_MODEL_2026_10_07.json': '9ffe37bc2420295db50cdcbef6cd37664a53f885c49ef66f766c8b97e87253aa', 'design/A01_CF11_ACADEMIC_TRANSFER_WORKING_MODEL_2026_10_07.json': '553205157b675d46994393948bdda2371d9467a00471986a1ff1705688205598', 'design/A01_CF12_MOVE_INTENT_WORKING_MODEL_2026_10_07.json': 'cf8c0e62c1215244e359987cfa1633e2ab7cf2f5ebd48596fe8ebc4b123c376f', 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json': '25138342ff7503de33c502d080002ee2057200521cb2a00d629d53914965447a', 'design/A01_E1_FINAL_EPISODE_FUNCTION.json': '9c15706717053a274f254ada476c027ea619858e6cd4ae80d8d8b422b789405e', 'design/A01_E2_FINAL_EPISODE_FUNCTION.json': '306dd7810fda0395dc722ab953ebac9ef1e4cf3db0cc4a9dc0266a8a2b2e5285', 'design/A01_E2_LITERAL_COST_WITNESS_SELECTED_OVERLAY_2026_10_08.json': '20468d21275ff7136f38553c6b816a1828065738a010ab8bc42045f3d379049d', 'design/A01_E3_FINAL_EPISODE_FUNCTION.json': 'edbccc96f145274f4dfcfc2bbaebdce1477b0f3f3426a5420848aadfde1f4911', 'design/A01_E4_FINAL_EPISODE_FUNCTION.json': '2223050467378df34763f5211d88eb82951e85acb18f1afee3cfb61b2998fecf', 'design/A01_E5_FINAL_EPISODE_FUNCTION.json': '7d8a1e11a978ebe049d0079606fb0a7140520efc892a76241627389711c4609f', 'design/A01_E6_FINAL_EPISODE_FUNCTION.json': '673bf62f660a6b71bb358752875df67f24204e34e36b4d0ce799fd6033c29feb', 'design/A01_E7_FINAL_EPISODE_FUNCTION.json': '9c3c23821264c7c27c9a786c375bd812e3131dac79175b1ba6144ab001b9c4f0', 'design/A01_E8_FINAL_EPISODE_FUNCTION.json': 'e1eb6a51536dcb75f4c4a91cdc0504418b73140045dc5db790d89016c672b7ac', 'design/A01_E9_FINAL_EPISODE_FUNCTION.json': '23d4ab60ccac1b2ac2af855943ae6ca65b8e17f70ce7ea635a287043404b8455', 'design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json': '56d7bfd2ff2b1b7f5fc805f4ec959508d2a08cba207454d8d3b861d00f5e2656', 'design/A01_FIRST_TRIAL_BLUEPRINT.json': '745638c9764fe6bdbf5e885efaa26b8e477c0d141236abed8c00d137270c9945', 'design/A01_FOLLOWUP_SCHOOL_PATH_2026_10_07.json': '13cdaaec5495f0d33beedd059133d63c81abc5a98f0a7b5591a384bb4a95718b', 'design/A01_OPENING_BLUEPRINT.json': '7cae80dea76e56676d18a741c3e053648989b2596d43f24d98b5cdeb0e166251', 'design/A01_OPENING_EPISODE_BOUNDARY.md': '13732b8eff9d426c80f249971eda3f197bad2907f945102f045825095a0435e9', 'design/A01_TRIAL_SCHOOL_OPERATING_PATH_2026_10_07.json': '181988c7426cf54e7d553d84fbda5106d3262247443acfcad713b8cdf4e1646b', 'design/CP2_ACT_SUBACT_PACKET.json': '2b291bca588302cbb254fc3417652f7d7532c46d7094221cdcceac60619c9db9', 'design/HOUSE_STYLE_FOUNDATION.md': 'ab3b82c912b9c8c452ae36507adcdfb4991ed9ded4933cdf5d9b63dbd1089234', 'research/A01_CF10_2015_PREP_COMPETITION_SOURCE_2026_10_07.json': '9bf32d4be5cc26a0e2f259e03a9711e8b926441033d776fde9e56ac985b6d8ba', 'research/A01_KOREA_2015_SCHOOL_TRIAL_BOUNDARY.md': '83156de992885a4a7261fd0faa6fb9e14a10be5dbcb992a29b6c364a68177aa1', 'research/TIMELINE_ELIGIBILITY_LEDGER.md': '3975f04f7c9d6631140c1e1fd70b187b80a58f8a79b6c0207d9ea2aaadfa4763', 'reviews/A01_E2_LITERAL_COST_WITNESS_ROOT_INDEPENDENT_REVIEW_2026_10_08.json': 'c5b116db7107f89e784ebaee3a2191a633696de8ac2005c0117860ba1d586c76', 'tools/build_a01_e1_final_episode_function.py': 'e8b8ece609f74e1a42bfdb31ac6543a1dd73e3693cc03894940c867057ace3d7', 'tools/build_a01_e2_final_episode_function.py': 'b9053e69224182f3da87d7afa875ce2ccb07ac71d43d52a69708e02010721c17', 'tools/build_a01_e3_final_episode_function.py': '3413c092da19aced37a4c79f861b93fc3d48bfc3bdf1845a1080030980ff5b27', 'tools/build_a01_e4_final_episode_function.py': '26c1f725cab46b5fa8c63c13184a8adcb88d222a5bb6a570645f57bd95fb5425', 'tools/build_a01_e5_final_episode_function.py': 'd2aef8f579d51e230fc221da53e5a523c0b3d830b2d70342bc936b1daea59515', 'tools/build_a01_e6_final_episode_function.py': '9a3facac931aeba3ba2596c48d99840c3d0f487d2046bd6bd4bbb39b44fd6b97', 'tools/build_a01_e7_final_episode_function.py': '7568e8cf3e7112def0beb92f9c580f5198148d772a4e85528c1cfac66c20dda8', 'tools/build_a01_e8_final_episode_function.py': 'a243c0f5c4c3879af8fbe46365037c572c5dbd3684e1392e703e8fff1604cfc8', 'tools/build_a01_e9_final_episode_function.py': 'f5bf4782fa13e80e87e7af15465b905fb2e05bd5dd8ac45419059deaa6ba9bca', 'reviews/A01_OPENING_BLUEPRINT_REVIEW_2026_10_04.json': '2b6c526dfb81f59423eae272d85f4dc108ba83fa75b3dc41dc3cc1860be4f2ff', 'reviews/A01_FIRST_TRIAL_BLUEPRINT_REVIEW_2026_10_05.json': '550dc6cf70988a2f1dbb2d31f7323b512b05694a5f7da7ebad86056ecea4bf0c', 'reviews/A01_FIRST_CONTRIBUTION_BLUEPRINT_REVIEW_2026_10_05.json': '163f5395914738612e3ba7d33c22b6ef51c7ec973c0b6bb8b796d68712f37fad', 'design/A06_2020_21_FINITE_FUNCTION_BATCH_2026_10_07.json': '5d19ee7d3c59c914655e29c5c96aaa3a86c396339d28ae2acff937de1c7961c9'}
REGISTER_SCOPE_SHA = 'b0bc5101a18105125d945c8b763ee487752a797772c1ffaeefe72d925a989b90'
ANCHOR_SHA = {'canon/PROJECT_FREEZE.md': 'c80b9383185690fae978f5b2213b7afef6ea315c4ea7ffcc877ea6c7f2459afd', 'canon/CAREER_TIMELINE.md': '3921dc4e238d140c03f60adca97397385825503f1a5cf3c089f619ede916170c', 'control/DESIGN_GATE.md': '8ea7dd276b7e0e3e986cdbf3e50ebcbcdfdfe4841995d0874c425bfed3e2aea6'}
SNAPSHOTS = {
 'canon/PROJECT_FREEZE.md': ('6b67804bf911dca2df6f5825de914c5a203b9fe5', '71bbfb1177c846e754e41f8217f49c760421dfd77b63d06af6aaa9d1aa3de1cc'),
 'control/DESIGN_GATE.md': ('6b67804bf911dca2df6f5825de914c5a203b9fe5', '818190e69f651d3f48f10617133a48971fabec18ce8dd369f677592bed10fbd6'),
 'canon/CAREER_TIMELINE.md': ('9391faba1df3c981963d24e031d509dcc14bb4c6', 'c6420cc02031b138103fe83dc02437dd209a3925d005e9a063855a66ee467eca')}

def norm(t): return t.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
def digest(t): return hashlib.sha256(norm(t).encode()).hexdigest()
def jd(o): return hashlib.sha256(json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',',':')).encode()).hexdigest()
def text(p): return norm((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p): return digest(text(p))
def load(p): return json.loads(text(p))
def section(t, prefix):
    headers=list(re.finditer(r'^## .+$',t,re.M))
    i=next(i for i,m in enumerate(headers) if m.group().startswith(prefix))
    return t[headers[i].start():headers[i+1].start() if i+1<len(headers) else len(t)].strip()
def anchor_projection(p,t):
    if p=='canon/PROJECT_FREEZE.md':
        return {k:section(t,k) for k in ['## v0.7 LOCKED', '## v0.9 LOCKED', '## v0.10 LOCKED', '## v0.12 LOCKED']}
    if p=='canon/CAREER_TIMELINE.md':
        return [line for line in t.splitlines() if line.startswith('- 주인공은 한국 고1을 마친 뒤') or line.startswith('| 2016.03 |')]
    assert p=='control/DESIGN_GATE.md'
    return [line for line in t.splitlines() if line in ['status: CLOSED','manuscript_allowed: false']]
def assert_anchor(p,t):
    a=anchor_projection(p,t)
    assert jd(a)==ANCHOR_SHA[p], 'Consumed A01 anchor changed: '+p
    if p.endswith('DESIGN_GATE.md'): assert a==['status: CLOSED','manuscript_allowed: false']
    return a
def register_projection(reg):
    return {'functions':[r for r in reg['functions'] if r['act']=='A01'],
            'overlays':[r for r in reg.get('current_function_overlays',[]) if r['target_function'].startswith('A01-')]}
def physical():
    for p,h in PINS.items(): assert sha(p)==h, 'Pinned A01 source changed: '+p
    r=register_projection(load(REGISTER)); assert jd(r)==REGISTER_SCOPE_SHA, 'Current A01 register scope changed'
    for p,(c,h) in SNAPSHOTS.items():
        old=norm(subprocess.check_output(['git','show',c+':'+p],cwd=ROOT).decode('utf-8-sig'))
        assert digest(old)==h, 'Historical full-file snapshot mismatch'
        assert_anchor(p,old); assert_anchor(p,text(p))
    return {'register':r,'files':{p:load(p) for p in PINS if p.endswith('.json')}}
def source_inputs(): return physical()

def coverage(s):
    rows=[]
    for i,r in enumerate(s['register']['functions']):
        f=s['files'][r['path']]; b=s['files'][ORIGINAL[i]] if i<3 else f['local_blueprint']
        assert b['status']=='ACTUAL_VERIFIED'
        if i<3:
            reviewed=s['files'][ORIGINAL_REVIEWS[i]]
            assert reviewed['blueprint_path']==ORIGINAL[i] and reviewed['blueprint_sha256']==PINS[ORIGINAL[i]]
        assert f['entry_state']==r['exact_entry'] and f['exit_state']==r['exact_exit']
        assert (f['final_function_order'],f['planned_allocation_slot'])==(i+1,i+1)
        assert b['entry_state']==f['entry_state'] and b['exit_state']==f['exit_state']
        if i:
            assert r['exact_entry']==s['register']['functions'][i-1]['exact_exit']
        for p,h in b['source_rev_sha256'].items():
            if p in MUTABLE:
                assert h==SNAPSHOTS[p][1]
            else: assert sha(p)==h, 'Existing Blueprint dependency changed: '+p
        assert b['manuscript_allowed'] is False and b['author_locked'] is False
        rows.append({'function_id':r['id'],'function_path':r['path'],'function_sha256':PINS[r['path']],
          'blueprint_path':ORIGINAL[i] if i<3 else r['path'], 'json_pointer':'/' if i<3 else '/local_blueprint',
          'blueprint_semantic_sha256':jd(b),'existing_status':'ACTUAL_VERIFIED',
          'original_standalone_review_path':ORIGINAL_REVIEWS[i] if i<3 else None,
          'current_consumed_core':'CURRENT_ANCHORS_MATCH_EXISTING_VERIFIED_BODY',
          'physical_full_file_hash_drift_is_new_event_or_missing_blueprint':False,
          'source_revision_policy':'Historical complete fingerprints retained; current consumed anchor fingerprints separately tested',
          'beat_ids':[x['id'] for x in b['beats']], 'new_copy_created':False})
    assert len(rows)==9
    return rows

def addendum(s):
    f=s['files']['design/A01_E2_FINAL_EPISODE_FUNCTION.json']; w=s['files'][OVERLAY]['selected_witness']
    a=s['register']['overlays']; assert len(a)==1 and a[0]['bounded_literal_choice_cost_exit_accepted'] is True
    assert a[0]['selected_overlay_path']==OVERLAY and a[0]['acceptance_review']==PEER
    assert a[0]['selected_order']==['T1','W','T2']
    assert s['files'][PEER]['independent_review_completed'] is True
    assert s['files'][PEER]['source_sha256'][OVERLAY]==PINS[OVERLAY]
    assert s['files'][SCHOOL]['condition_handling']['limited_trial_clearance_in_fictional_model']=='SELECTED_FOR_LOCKED_T1_ONLY'
    claims=[]
    for key,access in [('selected_action','own action'),('visible_result','direct visible result'),('direct_present_cost','own spent turn/time')]:
        path={'selected_action':'자신이 전달받은 준비 과제와 직접 한 공 준비 동작',
              'visible_result':'다음 반복에 쓸 공이 준비된 현재 상태만 직접 관측; 타인의 평가·속마음은 모름',
              'direct_present_cost':'자신의 짧은 과시 순번·주의를 공 준비에 쓴 경험; 칭찬 제안이나 수령은 없음'}[key]
        claims.append({'claim':w[key],'status':'AUTHOR_MODELED_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED_SOURCE',
          'source_path':OVERLAY,'source_anchor':'/selected_witness/'+key,'source_sha256':PINS[OVERLAY],
          'protagonist_access':path,'other_character_access':'감독과 곁의 동료는 보이는 준비 동작·공 상태만 접근; 사적 판단 추가0'})
    return {'id':'A01-EF-002-W-BLUEPRINT-ADDENDUM','status':'PHYSICAL_UNVERIFIED_PENDING_ROOT_INDEPENDENT_REVIEW',
      'selected_function_id':'A01-EF-002','selected_function_is_newly_created':False,
      'coverage_gap':'Selected same-trial W has no standalone or embedded verification Blueprint; T1/T2 already covered',
      'authority':'SOURCE_BOUND_VERIFICATION_ADDENDUM_ONLY_NOT_NEW_EVENT_OR_PACK',
      'entry_state':f['entry_state'],'exit_state':f['exit_state'],'internal_order':['T1','W','T2'],
      'preserved_parent_beats':{'T1':{'source_path':ORIGINAL[1],'source_anchor':'/beats/0'},'T2':{'source_path':ORIGINAL[1],'source_anchor':'/beats/1'}},
      'newly_extracted_beat':{'id':'W','source_witness':copy.deepcopy(w),'claims':claims},
      'choice':w['selected_action'],'cost':w['direct_present_cost'],
      'information_boundary':{'style':'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY','pov_actor':'protagonist',
        'coach_task_authority':{'source_path':SCHOOL,'source_anchor':'/role_authority/1/can','status':'SELECTED_FICTIONAL_LIMITED_TRIAL_AUTHORITY'},
        'character_knows_all_reviewer_loaded_sources':False,'exact_date':None,'school_name':None,'exact_dialogue':None,
        'individual_scene_execution_or_real_school_record_certified':False,
        'forbidden_access':['감독·동료 비공개 평가','향후 C2 리바운드/아웃렛의 성공','실제 출결 처리·팀 등록']},
      'partial_order':['E1 proposal exit < separately modeled pre-T1 three-condition clearance < T1 < W < T2 < E3 next-training entry'],
      'clearance_bridge_is_new_dramatized_beat':False,'newly_generated_event_dialogue_or_prose':False,
      'ACTUAL_VERIFIED_promoted_by_writer':False,'author_locked':False,'manuscript_allowed':False}

def construct(s): return {'existing_function_coverage':coverage(s),'remaining_blueprints':[addendum(s)]}
def assert_payload(p):
    # Independently reload before accepting returned data; never compare two aliased objects.
    s=physical()
    assert p['existing_function_coverage']==coverage(s), 'Returned coverage differs from existing verified sources'
    assert p['remaining_blueprints']==[addendum(s)], 'Returned W addendum changes source meaning or authority'
    # Bind critical returned meaning directly, even if the extraction helper is patched.
    assert len(p['existing_function_coverage'])==9 and len(p['remaining_blueprints'])==1
    for i,(row,registered) in enumerate(zip(p['existing_function_coverage'],s['register']['functions'])):
        source=s['files'][ORIGINAL[i]] if i<3 else s['files'][registered['path']]['local_blueprint']
        assert row['function_id']==registered['id'] and row['blueprint_semantic_sha256']==jd(source)
        assert row['beat_ids']==[b['id'] for b in source['beats']] and row['new_copy_created'] is False
    b=p['remaining_blueprints'][0]; f=s['files']['design/A01_E2_FINAL_EPISODE_FUNCTION.json']; w=s['files'][OVERLAY]['selected_witness']
    assert b['status']=='PHYSICAL_UNVERIFIED_PENDING_ROOT_INDEPENDENT_REVIEW' and b['ACTUAL_VERIFIED_promoted_by_writer'] is False
    assert b['selected_function_id']=='A01-EF-002' and b['selected_function_is_newly_created'] is False
    assert b['entry_state']==f['entry_state'] and b['exit_state']==f['exit_state'] and b['internal_order']==['T1','W','T2']
    assert b['choice']==w['selected_action'] and b['cost']==w['direct_present_cost']
    assert b['newly_extracted_beat']['source_witness']==w
    claims=b['newly_extracted_beat']['claims']; assert len(claims)==3
    for c,k in zip(claims,['selected_action','visible_result','direct_present_cost']):
        assert c['claim']==w[k] and c['source_anchor']=='/selected_witness/'+k and c['source_path']==OVERLAY
        assert c['source_sha256']==PINS[OVERLAY] and c['status']=='AUTHOR_MODELED_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED_SOURCE'
    info=b['information_boundary'];assert info['style']=='S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY'
    assert all(info[k] is None for k in ['exact_date','school_name','exact_dialogue'])
    assert info['character_knows_all_reviewer_loaded_sources'] is False and info['individual_scene_execution_or_real_school_record_certified'] is False
    assert not any(b[k] for k in ['clearance_bridge_is_new_dramatized_beat','newly_generated_event_dialogue_or_prose','author_locked','manuscript_allowed'])
def build():
    s=source_inputs(); assert s==physical(),'Source input differs from independently read sources'
    p=construct(s); assert s==physical(),'Constructor changed its input sources'; assert_payload(p)
    return {'schema':'A01_REMAINING_VERIFIED_BLUEPRINT_BUNDLE_V1',
      'status':'COVERAGE_AUDITED_ONE_SELECTED_W_ADDENDUM_PENDING_INDEPENDENT_REVIEW',
      'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8_BOM_STRIPPED_CRLF_CR_NORMALIZED_LF',
      'mutable_source_scope':{'register_path':REGISTER,'A01_rows_and_selected_overlay_semantic_sha256':REGISTER_SCOPE_SHA,
        'current_consumed_anchor_sha256':ANCHOR_SHA,'historical_full_file_snapshots':{p:{'commit':c,'sha256':h} for p,(c,h) in SNAPSHOTS.items()},
        'whole_file_revision_is_current_gate':False,'unrelated_progress_append_creates_STALE':False},
      **p,'counts':{'existing_functions':9,'existing_standalone_blueprints':3,'existing_embedded_blueprints':6,
        'existing_core_blueprints_recreated':0,'selected_overlay_uncovered_before_this':1,'new_pending_addenda':1,
        'new_ACTUAL_VERIFIED_promotions':0,'new_functions':0,'new_events':0,'new_prose_or_dialogue':0},
      'next_unit_handoff':{'target':'A02 embedded Blueprint current-core coverage audit before any new generation',
        'known_physical_embedded_units':10,'next_physical_inventory_gap':'A06-EF-001 batch has no top-level local_blueprint; inspect batch per-function blueprint fields before calling missing',
        'A06_inspected_per_function_pointer':'design/A06_2020_21_FINITE_FUNCTION_BATCH_2026_10_07.json#/functions/0',
        'A06_inspected_record_status':'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'A06_next_verification_task':'Add claim-specific anchor/status/information-access evidence only if the existing batch fails current-core Blueprint requirements; no standalone-file requirement',
        'next_missing_verified_unit_certified':False,'audit_scope_does_not_expand_to_all_780_slots':True},
      'independent_review_completed':False,'whole_g13_complete':False,'whole_g14_complete':False,
      'final_published_episode_count':None,'actual_context_packs':0,'manuscript_allowed':False,'design_gate':'CLOSED','freeze':'v0.30 PARTIAL'}
def validate(o):
    try:
        assert o==build(),'Saved bundle differs from source-bound reconstruction'
        assert_payload(o);return []
    except (AssertionError,KeyError,ValueError,TypeError) as e:return [str(e)]
def md(o):
    lines=['# A01 기존 Blueprint 커버리지와 W 검증 보충','',o['status'],'',
      '기존9함수는 standalone3+embedded6으로 이미 커버된다. 새 복사본0. 전체파일 지문 차이와 A01 근거 변화는 분리했다. 새 대상은 후행 채택된 E2 같은 체험의 W 준비·현재 비용 한 개다. 선택된 사건은 이미 독립 검문됐지만 이번 Blueprint 자체는 root 독립 검문 전 PHYSICAL_UNVERIFIED다. ACTUAL_VERIFIED 승격0.','',
      '|함수|기존 Blueprint locator|Beat|현행 핵심|','|---|---|---|---|']
    for x in o['existing_function_coverage']:lines.append('|'+x['function_id']+'|'+x['blueprint_path']+x['json_pointer']+'|'+','.join(x['beat_ids'])+'|원문·현재 사용 anchor 일치|')
    b=o['remaining_blueprints'][0]
    lines+=['','## 새 검증 보충 한 개','',
      'E2 entry/exit와 T1→T2는 그대로. 이미 선택된 overlay 순서 T1→W→T2만 적용한다. 새 세션·일자·경기·등록·대사·문장·역사사실은 추가하지 않는다.','',
      '선택: '+b['choice'],'','현재 비용: '+b['cost'],'',
      '세 주장 각각 `/selected_witness/selected_action`, `/visible_result`, `/direct_present_cost` 원문·상태·SHA와 주인공 접근 경로를 연결했다. 감독의 전달 과제/자기 움직임/현재 공 상태까지만 안다. 감독과 동료의 마음·평가·전체 신뢰는 추가하지 않는다. 칭찬의 확실한 제안·수령이 아니라 즉시 과시 순번과 주의를 준비에 쓴 비용이다.','',
      'S1 주인공 밀착 3인칭 유지. 부분순서 E1 제안→T1 전 별도 가상 세 조건 확인→T1→W→T2→E3 다음 훈련만 보존하며 정확 날짜·교명·대사 null이다. 절차 확인을 새 장면 Beat로 만들지 않는다.','',
      '## 현재성과 과거 지문','',
      '원 freeze/gate 전체지문은6b67804, 연표는9391faba 역사 스냅샷으로 명명했다. 현재 freeze의 v0.7/0.9/0.10/0.12 근거와 연표의 한국 고1→2016.03 이동 문구, CLOSED/원고false만 별도 semantic fingerprint로 대조한다. 후행 H21·진척 추가가 같은 원천을 STALE로 만들지 않으며 민감 anchor 변경은 FAIL이다. 원3Blueprint 및6embedded 원문/지문은 수정하지 않는다. 기존 strict whole-file checker의 stale 경고를 PASS로 재명명하지 않는다.','',
      '## 다음 단위','',
      'A02의10embedded도 실제 존재하므로 새 Blueprint를 만들기 전에 같은 핵심/현재성 감리를 한다. A06 batch `/functions/0`은 FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE이며 entry/choice/cost/beats/exit가 있다. 다음 후보 검문은 그 기존 batch의 주장별 anchor·상태·인물 정보접근과 현재성이다. standalone 파일이나 local_blueprint 필드의 부재만으로 실제 누락을 확정하지 않는다. 이번 bundle은 A01만 검문하며780칸 자동생성0. 전체G13/회차확정/G14 및Pack 생성 선행조건은 미충족이다.','',
      '|단계|범위|상태|','|---|---|---|','|1|기반 정본|완료|','|2|S2 유한 시즌|완료|','|3|2021–23 계약·cap·픽|완료|','|4|후반 커리어|진행|','|5|Act·Sub-Act·기능|국소60/42경로·전체미완료|','|6|집필규격·Context Pack|검증보충1 대기·Pack0|','|7|통합·독립·최종승인|미완료·CLOSED|','',
      '미완료4 / 6번까지3 · v0.30 PARTIAL · CLOSED · 원고0.']
    return '\n'.join(lines)+'\n'
def self_test():
    passed=[]
    for name,mutate in [('false_verified_promotion',lambda p:p['remaining_blueprints'][0].update(status='ACTUAL_VERIFIED')),
      ('new_exact_date',lambda p:p['remaining_blueprints'][0]['information_boundary'].update(exact_date='2015-04-01')),
      ('praise_paid',lambda p:p['remaining_blueprints'][0]['newly_extracted_beat']['source_witness'].update(immediate_praise_offered_or_received=True))]:
        p=construct(physical());mutate(p)
        try:
            with patch(__name__+'.construct',return_value=p):build()
        except AssertionError:passed.append(name)
        else:raise AssertionError('FALSE PASS '+name)
    original=construct
    def alias(s):
        p=original(s);s['files'][OVERLAY]['selected_witness']['later_s2_rebound_outlet_prepaid']=True
        p['remaining_blueprints'][0]['newly_extracted_beat']['source_witness']['later_s2_rebound_outlet_prepaid']=True;return p
    try:
        with patch(__name__+'.construct',side_effect=alias):build()
    except AssertionError:passed.append('source_return_alias_mutation')
    else:raise AssertionError('FALSE PASS source alias')
    p='canon/PROJECT_FREEZE.md'
    try:assert_anchor(p,text(p).replace('체험 기회만 줄 수 있다','즉시 선수 자리를 보장한다'))
    except AssertionError:passed.append('current_A01_authority_anchor_reversal')
    else:raise AssertionError('FALSE PASS sensitive current anchor')
    assert_anchor(p,'후행 무관 진척 메모\n'+text(p));passed.append('unrelated_progress_append_preserved')
    return passed
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();o=build()
    if a.write:
        (ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
        (ROOT/OUT.replace('.json','.md')).write_text(md(o),encoding='utf8',newline='\n')
    errors=validate(load(OUT)) if a.check else []
    if a.check and text(OUT.replace('.json','.md'))!=md(o):errors.append('Markdown stale')
    controls=self_test() if a.self_test else []
    print(json.dumps({'current':not errors,'errors':errors,'existing_coverage':9,'new_pending_addenda':1,'writer_controls':controls},ensure_ascii=False))
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
