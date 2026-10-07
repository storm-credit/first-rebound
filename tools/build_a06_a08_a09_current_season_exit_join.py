"""Nine bounded Act exits joined to current selected fictional execution sources.
No producer ancestors are rebuilt. New A08 calls are 100 seconds of observation,
not added court time or a new score/productivity model.
"""
from __future__ import annotations
import argparse, copy, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_a06_a08_a09_current_season_exit_join.py'
OUTPUT='design/A06_A08_A09_CURRENT_SEASON_EXIT_JOIN_2026_10_08.json'
MD=OUTPUT[:-5]+'.md'
PINS={'design/CP2_ACT_SUBACT_PACKET.json': '2b291bca588302cbb254fc3417652f7d7532c46d7094221cdcceac60619c9db9', 'control/G13_WHOLE_ACT_EXIT_FINITE_AUDIT_2026_10_08.json': 'a61af318fd1e365fcd127b6eaf88118ea6c50a02a57a43246746e80e21b79eb0', 'design/A06_2020_21_FINITE_FUNCTION_BATCH_2026_10_07.json': '5d19ee7d3c59c914655e29c5c96aaa3a86c396339d28ae2acff937de1c7961c9', 'design/A08_FINITE_FUNCTION_BATCH_2026_10_07.json': 'b84f4d08ede9015934b6d91287c21588bee9443fbaa8bf9ae6d3b1804f8c3b07', 'design/A09_E1_FINAL_EPISODE_FUNCTION.json': '0a0e4cf2c3f41fd16131f8cf43310ab44ae4ec1b26d7361f128889f14b4eaf58', 'design/A09_JOINT_ATTEMPT_SELECTED_EXECUTION_2026_10_08.json': '038b0227a74c7abbb94061776f9cf5c0cc33841bd6de3d5694ffdb6f7341b3be', 'design/A08_CONDITIONAL_GAME_CALL_FAMILY_2026_10_07.json': '4fa439c8330e42cd06d5e305b5226e4a540ff23c1f25b263b0afa5cea4a1a6a4', 'simulation/NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json': '3e35fd2abfeb32e2bc5b66b7796f843ca117359be1a419d037844d29177a26d8', 'simulation/NBA_2020_21_TRANSACTION_EXECUTION_CLOSURE_WITNESS.json': '2efec5f5e57c02accf5d5bed3ce364ef6f9eeddab55a05d631f1bc24d6b55307', 'simulation/NBA_2020_21_HEALTH_COACH_EXECUTION_FAMILY.json': '501cebe54dda5206a0692e5bbb9570baa89b186ea556dfdf354e79c65175be3c', 'control/CHICAGO_2020_21_D1_S2_REGISTER.json': '81d7bc83eda33d43cb0ede6d5e9111558de3a94814d3f58c4888738e46a63d2c', 'reviews/S2_FINITE_SEASON_CLOSURE_AND_A02_E8_E10_REVIEW_2026_10_07.md': '843b97ccd7851c8d47fe69fc695ab2530d9d9fcfbb9ed616a8acb28c6fb7aeff', 'simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json': 'f8c78e99cce1b02a051c94339b550fdb52205d3988db8bbe69b780559c3bc306', 'simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json': 'e7d0f4b15bc06c7cd16a38d158b38a78871fb7372d412639e33bb20c31d225a7', 'simulation/CHICAGO_2022_SELECTED_CORE_CONTRACT_CARRIER.json': 'cc586a6f801a1e61d60bd9eddbe0e8bfa57415963c2d0d76669683a690551d6c', 'simulation/CHICAGO_2022_ROOKIE_SELECTED_EXECUTION.json': '3c06967cf8c7171f815819efd3b4a71fb88ac77db3ae8798b34afeeeae93ce1c', 'simulation/CHICAGO_2022_23_SELECTED_DATED_ROLES.json': 'c0650dbb07b75cc1523bf7ccc7f658576ac5b9a8784f1e80cc97178897703170', 'simulation/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS.json': '8e2a778fe646de3c6070be7dd3acc64199fe2a7c813e780916e380b099fa3889'}
CP2='design/CP2_ACT_SUBACT_PACKET.json'
AUDIT='control/G13_WHOLE_ACT_EXIT_FINITE_AUDIT_2026_10_08.json'
A06='design/A06_2020_21_FINITE_FUNCTION_BATCH_2026_10_07.json'
A08='design/A08_FINITE_FUNCTION_BATCH_2026_10_07.json'
A09E1='design/A09_E1_FINAL_EPISODE_FUNCTION.json'
A09='design/A09_JOINT_ATTEMPT_SELECTED_EXECUTION_2026_10_08.json'
CALL='design/A08_CONDITIONAL_GAME_CALL_FAMILY_2026_10_07.json'
RESULT='simulation/NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json'
TRANSACTION='simulation/NBA_2020_21_TRANSACTION_EXECUTION_CLOSURE_WITNESS.json'
HEALTH='simulation/NBA_2020_21_HEALTH_COACH_EXECUTION_FAMILY.json'
REGISTER='control/CHICAGO_2020_21_D1_S2_REGISTER.json'
S2REVIEW='reviews/S2_FINITE_SEASON_CLOSURE_AND_A02_E8_E10_REVIEW_2026_10_07.md'
DRAFT='simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json'
CORE='simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json'
CARRIER='simulation/CHICAGO_2022_SELECTED_CORE_CONTRACT_CARRIER.json'
ROOKIE='simulation/CHICAGO_2022_ROOKIE_SELECTED_EXECUTION.json'
H22='simulation/CHICAGO_2022_23_SELECTED_DATED_ROLES.json'
GLOBAL='simulation/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS.json'
KEY='PUBLISHED_2022_0007'
CORE5={'PG':'LaMelo Ball','SG':'Zach LaVine','SF':'Protagonist','PF':'Lauri Markkanen','C':'Wendell Carter Jr.'}
CALL_IDS=['G0_IMMEDIATE_CATCH_RETURN','G1_BLOCKED_FIRST_RETURN','G2_STOP_AND_SAFE_RESET','G3A_OWN_SHORT_ATTEMPT_AND_STOP','G3B_TEAMMATE_ADVANTAGE_HANDOFF']
WINDOWS=[(0,20),(40,60),(80,100),(120,140),(160,180)]

def text(p):return Path(p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def physical(root,p):return json.loads(text(root/p)) if p.endswith('.json') else text(root/p)
def sources(root):
    for p,h in PINS.items():assert sha(root/p)==h,f'Source stale: {p}'
    return {p:physical(root,p) for p in PINS}

def source_game(src):
    return next(x for x in src[GLOBAL]['rows'] if x['calendar_key']==KEY)

def position_at(blocks,second):
    x=next(x for x in blocks if x['start_second']<=second<x['end_second'])
    return x['positions']

def s2_join(src):
    r,t,h,reg=src[RESULT],src[TRANSACTION],src[HEALTH],src[REGISTER]
    assert reg['season_selected'] is True and len(reg['legal_proofs'])==12
    assert set(reg['k_closed'])=={'K_HEALTH','K_REGISTRATION','K_TRANSACTIONS','K_METHOD_EVENTS'}
    assert len(r['games'])==1174 and len(r['pick_control_snapshot']['rows'])==60
    assert t['summary']['selected_team_games']==2348 and t['summary']['approved_events']==8
    assert len(h['bindings'])==2348 and len(h['compact_binding_schema'])==6
    f1=next(x for x in t['selected_execution']['approved_event_links'] if x['id']=='F1_FIVE_PLAYER_ATOMIC')
    assert f1['date']=='2021-03-25'
    assert {(x['movement']['player'],x['movement']['from'],x['movement']['to']) for x in f1['movement_state_links']}=={
        ('Daniel Gafford','CHI','WAS'),('Luke Kornet','CHI','BOS'),('Moritz Wagner','WAS','BOS'),('Daniel Theis','BOS','CHI'),('Javonte Green','BOS','CHI')}
    selected=[]
    for game,winner in [('2021-05-18_WAS_CHI','CHI'),('2021-05-20_IND_CHI','IND')]:
        g=next(x for x in r['games'] if x['id']==game)
        assert g['phase']=='PLAY_IN' and g['winner']==winner and g['score'] is None
        b=next(x for x in t['selected_execution']['dated_result_roster_links'] if x['id']==game)
        assert b['date']==g['date'] and b['selected_winner']==winner
        assert b['teams']['CHI']['positive_membership_covered'] and b['teams']['CHI']['game_night_active_upper']==15
        selected.append({'result':g,'registration_link':b['teams']['CHI']})
    picks=[]
    for pick,player,round_ in [(10,'Chris Duarte',1),(39,'Joe Wieskamp',2)]:
        p=next(x for x in r['pick_control_snapshot']['rows'] if x['pick']==pick)
        d=next(x for x in src[DRAFT]['selected_rows'] if x['pick']==pick)
        assert p['origin']==p['control_holder']=='CHI' and p['round']==round_
        assert d['player']==player and d['selecting_team']==d['conditional_final_draft_rights_holder']=='CHI'
        assert d['lawful_PS21_participant_model_selected'] and not d['new_NBA_UPC_or_RequiredTender']
        picks.append({'season_control':p,'later_selected_draft_right':d})
    return copy.deepcopy({'finite_current_season_selected':True,'legal_proofs':12,'method_gates':3,'K_closed':4,
        'games':1174,'team_games':2348,'F1_atomic_movement':f1,'Chicago_L2_sequence':selected,
        'season_control_then_later_draft':picks,'five_player_usage_rights':src[A06]['five_player_usage_rights'],
        'provisional_CP2_exit_wording_preserved_as_generation_snapshot':True,
        'old_PR155_execution_closeout_used_as_current':False,'private_receipt_or_individual_box_certified':False})

def contract_join(src):
    terms=src[CORE]['contract_terms']
    p=terms['Protagonist']
    assert p['source_terms']['id']=='E2' and p['source_terms']['recipient']=='Chicago'
    assert p['source_terms']['salary_2022_onward']==[22000000,23760000,25520000,27280000]
    assert p['old_accrued_obligations_preserved']
    assert terms['Carter']['current_term_bonus_if_any_preserved']
    c=src[CARRIER]['named_contract_cost_rows']
    costs={x['player']:x for x in c}
    for player,upper in [('Protagonist',22000000),('Wendell Carter Jr.',14150000),('Zach LaVine',37096500),('Lauri Markkanen',18360000),('Alex Caruso',9030000)]:
        assert costs[player]['normal_upper']==upper and costs[player]['roster_type']=='STANDARD'
    rook=src[ROOKIE]['working_execution']
    assert rook['cost']['first_reservation_11060000_replaced_once_by_RSC3191400']
    assert rook['cost']['separate_old_waived_upper']==2351532
    assert rook['cost']['normal_family_upper_before_new_D23_charge']==162976941
    assert rook['cost']['apron_family_upper_before_new_D23_charge']==164614941
    assert rook['cost']['preserved_other_unsigned_normal']==2036000
    assert rook['cost']['preserved_other_unsigned_apron']==3674000
    return copy.deepcopy({'selected_E2_source_terms':p,'selected_Carter_terms':terms['Carter'],'selected_LaVine_terms':terms['LaVine'],
        'named_core_cost_rows':[costs[x] for x in ['Protagonist','Wendell Carter Jr.','Zach LaVine','Lauri Markkanen','Alex Caruso']],
        'July7_core_cost_snapshot':src[CARRIER]['preserved_public_cost_family'],
        'later_selected_rookie_cost_snapshot':rook['cost'],'protected_waiver_reservation':rook['dead_protection_reservation'],
        'two_RT_reservations_are_not_actual_unaccepted_tender_salary':True,
        'negative_apron_screen_is_not_illegality_without_trigger':True,
        'front_office_authority_or_actual_salary_receipt_granted_to_protagonist':False})

def game_calls(src):
    g=source_game(src)
    calls=[]
    for i,(base,(start,end)) in enumerate(zip(src[CALL]['bounded_game_calls'],WINDOWS)):
        seg=next(x for x in g['simultaneous_segments'] if x['start_second']<=start and end<=x['end_second'])
        calls.append({'id':base['id'],'source_call_pointer':CALL+'#/bounded_game_calls/'+str(i),
            'source_semantics':copy.deepcopy(base),'game_key':KEY,'date':g['published_date'],'home':g['home'],'away':g['away'],
            'start_second':start,'end_second':end,'seconds':20,'quarter':1,
            'positions':{team:copy.deepcopy(seg[team]) for team in ['CHI','MIA']},'fictional_coach_permission_for_this_window_selected':True,
            'window_conditions_explicitly_instantiated_in_fiction':True,
            'observed_by_character_is_fictional_not_NBA_play_by_play':True,
            'better_teammate_in_G3B':'LaMelo Ball' if i==4 else None,
            'new_score_assist_BPM_or_winner_credit':False,'permanent_joint_ace_or_closing_authority':False,
            'actual_NBA_game_event_certified':False})
    return calls

def assert_game_calls(calls,src):
    g=source_game(src);templates=src[GLOBAL]['shared_team_templates']
    assert g['published_date']=='2022-10-19' and (g['home'],g['away'])==('MIA','CHI') and g['winner']=='MIA'
    assert len(calls)==5
    occupied=set()
    for i,c in enumerate(calls):
        start,end=WINDOWS[i]; base=src[CALL]['bounded_game_calls'][i]
        assert c['id']==CALL_IDS[i] and c['source_semantics']==base,'Returned call meaning differs from source permission/lane/action/cost'
        assert (c['start_second'],c['end_second'],c['seconds'],c['quarter'])==(start,end,20,1),'Returned call date/window changed'
        assert (c['game_key'],c['date'],c['home'],c['away'])==(KEY,'2022-10-19','MIA','CHI')
        assert c['source_call_pointer']==CALL+'#/bounded_game_calls/'+str(i)
        assert c['fictional_coach_permission_for_this_window_selected'] and c['window_conditions_explicitly_instantiated_in_fiction']
        assert c['observed_by_character_is_fictional_not_NBA_play_by_play']
        assert c['better_teammate_in_G3B']==('LaMelo Ball' if i==4 else None)
        assert not any(c[x] for x in ['new_score_assist_BPM_or_winner_credit','permanent_joint_ace_or_closing_authority','actual_NBA_game_event_certified'])
        for second in range(start,end):
            assert second not in occupied;occupied.add(second)
            expected={t:position_at(templates[t]['blocks'],second) for t in ['CHI','MIA']}
            assert c['positions']==expected,'Returned call position differs from selected physical source clock'
            assert expected['CHI']==CORE5
        for team in ['CHI','MIA']:
            template=templates[team]
            assert len(set(c['positions'][team].values()))==5
            assert set(c['positions'][team].values())<=set(template['standard'])&set(template['active'])
            assert not set(c['positions'][team].values())&set(template['TW'])
            assert sum(template['positive_player_seconds'].values())==14400
            assert all(template['positive_player_seconds'][p]>=20 for p in c['positions'][team].values())
    assert len(occupied)==100
    assert calls[0]['source_semantics']['dribble_before_return'] is False
    assert calls[1]['source_semantics']['chosen_return_lane']!=calls[2]['source_semantics']['chosen_return_lane']

def private_join(src):
    a=src[A09];e=a['institutional_execution']
    assert a['fictional_private_joint_training_and_return_selected']
    assert not a['public_tournament_game_performance_selected']
    assert not e['NBA_written_approval_or_public_game_insurance_accepted_selected']
    assert [x['id'] for x in e['authorities']]==['B1-1','B1-2','B1-3','B1-4','B1-5','B2-1','B2-2','B2-3']
    assert e['time_order']==[
        'fictional_roster_and_two_club_private_training_permissions_before_2023_09_26',
        'risk_and_private_access_before_joint_training',
        'private_training_window_ends_no_later_than_2023_10_06',
        'separate_club_return_by_2023_10_09','separate_allowed_training_from_2023_10_10']
    assert len(e['selected_fictional_twelve'])==len(set(e['selected_fictional_twelve']))==12
    assert [x['episode_function_id'] for x in a['functions']]==['A09-EF-002','A09-EF-003']
    assert a['functions'][0]['previous_function']['exact_full_exit']==src[A09E1]['exit_state']
    return copy.deepcopy({'selected_private_institutional_execution':e,'selected_cooperation_and_return_functions':a['functions'],
        'source_E1_prepermission_exit':src[A09E1]['exit_state'],
        'private_permissions_resolve_only_bounded_preparation_window':True,
        'risk_price_and_medical_letter_are_actual_certificates':False,
        'public_tournament_medal_military_are_local_exit_prerequisites':False,
        '2023_24_NBA_minutes_or_return_game_outcome_invented':False})

def exit_rows(src):
    rows=[]
    for row in src[AUDIT]['subact_exit_rows']:
        if row['act'] not in ['A06','A08','A09']:continue
        r={k:copy.deepcopy(row[k]) for k in ['id','act','entry','choice','cost','source_cp2_exit','local_function_witness']}
        r.update(bounded_current_execution_join_prepared=True,original_audit_missing_action_preserved=row['missing_finite_action_for_whole_exit'],
            join_pointer={'A06':'#/A06_current_S2_join','A08':'#/A08_selected_contract_and_game_join','A09':'#/A09_private_cooperation_return_join'}[row['act']],
            actual_historical_exit_certified=False,whole_Act_or_all_history_certified=False)
        rows.append(r)
    return rows

def build(root=ROOT):
    src=sources(root)
    for p in PINS:
        raw=Path(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
        expected=json.loads(raw) if p.endswith('.json') else raw
        assert src[p]==expected,f'Returned source differs from independent physical parse: {p}'
    assert len(src[CP2]['acts'])==14 and len(src[AUDIT]['subact_exit_rows'])==42
    assert sum(x['act'] in ['A06','A08','A09'] for x in src[AUDIT]['subact_exit_rows'])==9
    s2=s2_join(src);cost=contract_join(src);calls=game_calls(src);assert_game_calls(calls,src)
    private=private_join(src);rows=exit_rows(src)
    # Constructor-return patches must not mutate the input objects and then
    # compare successfully against those same contaminated aliases.
    for p in PINS:
        raw=Path(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
        expected=json.loads(raw) if p.endswith('.json') else raw
        assert src[p]==expected, f'Join constructor mutated consumed physical source: {p}'
    # Caller binds derived returns to original objects, rather than invoking a
    # possibly patched constructor twice as its own expected value.
    assert s2['F1_atomic_movement']==next(x for x in src[TRANSACTION]['selected_execution']['approved_event_links'] if x['id']=='F1_FIVE_PLAYER_ATOMIC')
    assert (s2['games'],s2['team_games'],s2['legal_proofs'],s2['K_closed'])==(1174,2348,12,4)
    assert s2['five_player_usage_rights']==src[A06]['five_player_usage_rights']
    for entry,game in zip(s2['Chicago_L2_sequence'],['2021-05-18_WAS_CHI','2021-05-20_IND_CHI']):
        assert entry['result']==next(x for x in src[RESULT]['games'] if x['id']==game)
        assert entry['registration_link']==next(x for x in src[TRANSACTION]['selected_execution']['dated_result_roster_links'] if x['id']==game)['teams']['CHI']
    for entry,pick in zip(s2['season_control_then_later_draft'],[10,39]):
        assert entry['season_control']==next(x for x in src[RESULT]['pick_control_snapshot']['rows'] if x['pick']==pick)
        assert entry['later_selected_draft_right']==next(x for x in src[DRAFT]['selected_rows'] if x['pick']==pick)
    assert cost['selected_E2_source_terms']==src[CORE]['contract_terms']['Protagonist']
    assert cost['selected_Carter_terms']==src[CORE]['contract_terms']['Carter']
    assert cost['selected_LaVine_terms']==src[CORE]['contract_terms']['LaVine']
    cost_source_rows=json.loads(Path(root/CARRIER).read_text(encoding='utf-8-sig'))['named_contract_cost_rows']
    assert cost['named_core_cost_rows']==[next(x for x in cost_source_rows if x['player']==player) for player in ['Protagonist','Wendell Carter Jr.','Zach LaVine','Lauri Markkanen','Alex Caruso']], 'Returned named core cost differs from physical selected contract rows'
    assert cost['July7_core_cost_snapshot']==src[CARRIER]['preserved_public_cost_family']
    assert cost['later_selected_rookie_cost_snapshot']==src[ROOKIE]['working_execution']['cost']
    assert cost['protected_waiver_reservation']==src[ROOKIE]['working_execution']['dead_protection_reservation']
    assert not cost['front_office_authority_or_actual_salary_receipt_granted_to_protagonist']
    assert private['selected_private_institutional_execution']==src[A09]['institutional_execution'], 'Returned private execution differs from selected scope'
    assert private['selected_cooperation_and_return_functions']==src[A09]['functions']
    assert private['source_E1_prepermission_exit']==src[A09E1]['exit_state']
    assert private['private_permissions_resolve_only_bounded_preparation_window']
    assert not any(private[x] for x in ['risk_price_and_medical_letter_are_actual_certificates','public_tournament_medal_military_are_local_exit_prerequisites','2023_24_NBA_minutes_or_return_game_outcome_invented'])
    for r in rows:
        for w in r['local_function_witness']:
            f=src[w['path']]
            for key in (w['record_pointer'] or '').strip('/').split('/'):
                if key:f=f[int(key)] if isinstance(f,list) else f[key]
            assert f.get('id',f.get('episode_function_id'))==w['id']
            assert f['exit_state']==w['local_exact_exit'], 'Original exact function exit differs from current audit'
    original=[r for r in src[AUDIT]['subact_exit_rows'] if r['act'] in ['A06','A08','A09']]
    assert len(rows)==9
    for r,b in zip(rows,original):
        assert all(r[k]==b[k] for k in ['id','act','entry','choice','cost','source_cp2_exit','local_function_witness'])
        assert r['bounded_current_execution_join_prepared'] and not r['actual_historical_exit_certified'] and not r['whole_Act_or_all_history_certified']
    template=src[GLOBAL]['shared_team_templates']['CHI'];h=src[H22]['selected_role_template'];g=source_game(src)
    assert len(template['standard'])==15 and len(template['TW'])==2
    assert {x['player'] for x in src[GLOBAL]['owner_catalog'] if x['team']=='CHI' and x['registration']=='STANDARD'}==set(template['standard'])
    assert template['standard']==h['registered_STANDARD']
    assert template['positive_player_seconds']=={p:m*60 for p,m in h['player_minutes'].items()}
    assert [h['player_minutes'][p] for p in ['Protagonist','Lauri Markkanen','Alex Caruso']]==[32,32,18]
    assert next(x for x in src[H22]['dated_rows'] if x['calendar_key']==KEY)['published_date']==g['published_date']
    return {'id':'A06_A08_A09_CURRENT_SEASON_EXIT_JOIN','status':'NINE_BOUNDED_CURRENT_EXECUTION_JOINS_PREPARED_PENDING_INDEPENDENT_REVIEW',
        'source_sha256':dict(PINS,**{SELF:sha(root/SELF)}),'source_hash_convention':'UTF8 BOM stripped, CRLF/CR normalized to LF; no ancestor constructors rerun',
        'source_generation_flags_not_rewritten':True,'scope':{'original_Acts':14,'original_subacts':42,'new_bounded_joins':9,'new_episode_function_registrations':0},
        'CP2_Act_exits':[x for x in src[CP2]['acts'] if x['id'] in ['A06','A08','A09']],
        'subact_exit_rows':rows,'A06_current_S2_join':s2,
        'A08_selected_contract_and_game_join':{'contracts_and_budget':cost,'selected_dated_game_key':KEY,'date':'2022-10-19','selected_winner_preserved':'MIA',
            'source_game_semantic_sha256':hashlib.sha256(json.dumps(g,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
            'source_clocks_roster_rating_winner_unchanged':True,'registered_STD':15,'registered_TW':2,'CHI_positive_player_seconds':template['positive_player_seconds'],
            'new_bounded_coached_game_calls':calls,'elapsed_sample_seconds':100,'added_team_seconds':0,
            'coach_window_nomination_selected_in_this_working_design':True,
            'calls_are_fictional_observations_not_actual_NBA_possessions':True,'whole_game_co_ace_status_or_closing_authority_selected':False,
            'score_BPM_winner_awards_changed':False,'whole_FY22_budget_or_new_private_salary_certified':False},
        'A09_private_cooperation_return_join':private,
        'operating_exit_interpretation':{'A06':'선택된 탈락·권리10/39와 제한 수행 표본을 다음 훈련/agent평가에 인계. agent의 새 평가/계약 성과 미확정.',
            'A08':'선택 E2의 동료 예산 비용과 경기별 한정 공격/이양/중단 책임을 연결. 공동 에이스는 한정 역할 준비이며 영구지위·클로징권·수상 아님.',
            'A09':'가상 허가/위험관리 비용을 낸 비공개 협력과 제한 복귀 부하를 연결. 완전 화해·공개 대회·메달·군복무 또는 새 NBA 성과 아님.'},
        'certification':{'source_current_finite_joins_prepared':True,'independent_review_completed':False,'whole_A06_A08_A09_history_certified':False,
            'whole_g13_complete':False,'whole_g14_complete':False,'whole_macro3_complete':False,'new_author_lock':False,
            'actual_private_consent_salary_medical_receipt_certified':False,'actual_context_packs':0,'manuscript_allowed':False,'manuscript_count':0,'design_gate':'CLOSED'}}

def render(o):
    rows=o['subact_exit_rows']
    s=['# A06/A08/A09 현행 시즌과 한정 출구 연결','',
       '기존 14막/42소막 감사에서 세 막의 아홉 출구를 현행 선택 실행 원천에 연결했다. 새 에피소드 등록0, 독립 검문 pending. 이전 원천의 generation 당시 미선택/HOLD 문구는 원본 그대로 보존한다.','',
       '## A06: 현행 S2','',
       'PR155의 옛 EXECUTION_CLOSEOUT 대신 현행 S2 register의 season_selected·법적12·A3/K4와 1,174경기/2,348팀경기 원천을 사용한다. March25 Theis/Green A는 다섯 명 원자 양도/유지 범위다. Chicago의 5/18 WAS 원정 승리와 5/20 IND 패배를 정확한 등록 링크에 연결하고, 시즌 결산의 자체10/39→7/29 Duarte/Wieskamp 선택 권리로 구분한다. 개인 박스·득점·주인공 단독 승리 인과·실제6/22권리 접수는 인증하지 않는다.','',
       '## A08: 선택 계약 비용과 실제 가상 경기의 다섯 호출','',
       'E2 4년22/23.76/25.52/27.28m, Carter CX1, LaVine5년·Mark18.36m·Caruso9.03m의 동료 비용을 연결한다. July7 코어 상단170,845,541/172,483,541은 당시 스냅샷이다. 이후 Kessler RSC와 Stanley 방출 전액2,351,532 보존 후 162,976,941/164,614,941 상단은 다른 시점의 공개 가족이며 실제 사적 원장이 아니다. 두 unsigned RT 예약2,036,000/3,674,000도 실제 미수락 제안의 법정 급여라고 읽지 않는다. apron 초과 screen은 당해 trigger 없는 불법 판정이 아니다. 선수의 동료 요구는 프런트 계약 권한을 주지 않는다.','',
       '새 FY22/H22 NORMAL 날짜 원천 PUBLISHED_2022_0007(2022-10-19 CHI@MIA)의 코어5 공통0–360초에 다음 다섯20초를 배치한다. 정규 총시간2,880·팀선수초14,400와 주인공32/Mark32/Caruso18, 기존 승자MIA·평점·0OT 모델은 변하지 않는다. 100초는 기존 시계 안의 표본이며 추가 출장초가 아니다. 코트5명과 source position/active/STD를 매초 직접 대조한다. 원조건의 open/closed lane와 감독 허용은 이 leaf의 명시적 가상 작업 입력이며 NBA 관측 사실이 아니다.','',
       '| 호출 | 구간(초) | 선택 행동/직접 비용 |','|---|---:|---|']
    for c in o['A08_selected_contract_and_game_join']['new_bounded_coached_game_calls']:
        b=c['source_semantics'];s.append(f"| {c['id']} | {c['start_second']}–{c['end_second']} | {b['observed_action']} {b['cost']} |")
    s+=['','G0 무드리블 comparator/G1 닫힌 첫 길의 turnover·회복/G2 다른 열린 후방 reset/G3A 자기 짧은 시도와 중단/G3B LaMelo 이양·재관여를 구분한다. 제한 책임을 실제 가상 경기 시계에 인계하지만 새 성공 득점·assist·BPM·승패·영구 공동 에이스/클로징 권한을 만들지 않는다. 오래된 훈련-only EF002의 generation 미실행 문구를 소급 수정하지 않는다.','',
        '## A09: 이미 선택된 비공개 협력/복귀','',
        '선택된 12명·두 구단의 9/26–10/6 비공개 훈련 허가·훈련 전 위험관리·10/9 별도 복귀·10/10 제한 반복을 순서대로 연결한다. 위험 함수는 기존UPC 보장 위험액+치료/귀환비 최대1m이며 실제 보험료/급여/의료승인은 null이다. 한 번의 오류 수정과 원구단 연결/부하 반복은 기존 EF002/003에 이미 선택된 비용이다. 공개 Asian Games 출전·NBA 서면승인·FIBA분류·메달·군복무·다음 NBA경기의 분/성과를 이 출구의 새 선행 gate로 넣지 않는다. 비공개 허용을 공개 경기 허가로 바꾸지도 않는다.','',
        '## 아홉 출구와 원감사 보존','', '| 소막 | 원 CP2 출구 | 현행 인계 |','|---|---|---|']
    for r in rows:s.append(f"| {r['id']} | {r['source_cp2_exit']} | {r['join_pointer']} |")
    s+=['','원 choice/cost/정확 local exit는 JSON에 그대로 있다. 세 막의 한정 운영 출구 연결 준비와 전체 인생/관계/기술 완성·14막/G13 완결은 다른 주장이다. 새 writer controls는 독립 검문으로 세지 않는다. 저장물 exact-current와 반환 원천/호출 뜻/position 변조를 fail-closed로 검문한다. 피어가 회수한 P 계약비용0 반환과 F1 선수교체/원입력 alias 동시오염은 새 deep-copy 반환·생성 후 독립 물리 재대조·named core 원행 guard로 거부한다.','',
        '## 원천','']
    for p,h in PINS.items():s.append(f'- [{p}](../{p}): LF SHA `{h}`')
    s+=['','## 프로젝트 진행','', '[현행 로드맵](WORLD_BIBLE_COMPLETION_ROADMAP.md) / [현행 기능 등록](../control/G13_FINAL_FUNCTION_REGISTER.md)','',
        '| 행 | 상태 |','|---|---|','| 1 드래프트2020 | 완료 보존 |','| 2 Chicago2020–21 | 완료 보존 |',
        '| 3 거래·계약2021–23 | 현행 선택 실행 보존; 전체 미완료 |','| 4 장기 커리어 | 미완료 |',
        '| 5 결말·전체 구조 | 미완료; 이번 세 막의 한정 출구 연결 |','| 6 집필 규격·Pack | 전체 미완료 / Pack0 |',
        '| 7 통합·독립·작가 승인 | 전체 미완료 |','', '미완료 큰묶음5 / 6번까지4 · v0.30 PARTIAL · CLOSED · 원고0. 중앙/canon/Git 변경0.','']
    return '\n'.join(s)

def validate(o,root=ROOT):return [] if o==build(root) else ['Saved current-season join differs from current expected']

def self_test(root=ROOT):
    global sources,game_calls
    loader,constructor=sources,game_calls;passed=[]
    def probe(label,site,mutation):
        global sources,game_calls
        if site=='source':
            def bad(r):v=loader(r);mutation(v);return v
            sources=bad
        else:
            def bad(s):v=constructor(s);mutation(v);return v
            game_calls=bad
        try:
            try:build(root)
            except AssertionError:passed.append(label)
            else:raise RuntimeError('FALSE_PASS '+label)
        finally:sources,game_calls=loader,constructor
    probe('RETURNED_GLOBAL_DATE_SAME_CLOCK_SUBSTITUTION','source',lambda s:next(x for x in s[GLOBAL]['rows'] if x['calendar_key']==KEY).update(published_date='2021-10-19'))
    probe('G0_DRIBBLE_AUTHORITY_PROMOTION','call',lambda c:c[0]['source_semantics'].update(dribble_before_return=True))
    probe('SAME_FIVE_POSITION_SUBSTITUTION','call',lambda c:c[0]['positions']['CHI'].update(PG='Zach LaVine',SG='LaMelo Ball'))
    probe('PRIVATE_PERMISSION_TO_PUBLIC_TOURNAMENT_PROMOTION','source',lambda s:s[A09]['institutional_execution'].update(public_tournament_game_performance_selected=True))
    s2,contracts=s2_join,contract_join
    def bad_s2(s):
        v=s2(s);v['F1_atomic_movement']['movement_state_links'][0]['movement']['player']='Other Player';return v
    def bad_contracts(s):
        v=contracts(s);next(x for x in v['named_core_cost_rows'] if x['player']=='Protagonist')['normal_upper']=0;return v
    globals()['s2_join']=bad_s2
    try:
        try:build(root)
        except AssertionError:passed.append('RETURNED_F1_PLAYER_MUTABLE_ALIAS')
        else:raise RuntimeError('FALSE_PASS F1 player return')
    finally:globals()['s2_join']=s2
    globals()['contract_join']=bad_contracts
    try:
        try:build(root)
        except AssertionError:passed.append('RETURNED_PROTAGONIST_CONTRACT_COST_ZERO')
        else:raise RuntimeError('FALSE_PASS core cost return')
    finally:globals()['contract_join']=contracts
    return passed

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    o=build()
    if a.write:
        (ROOT/OUTPUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (ROOT/MD).write_text(render(o),encoding='utf-8')
    if a.check:
        assert validate(json.loads(text(ROOT/OUTPUT)))==[]
        assert text(ROOT/MD)==render(o),'MD stale'
    if a.self_test:print(json.dumps({'writer_negative_rejected':self_test()},ensure_ascii=False))
    print(json.dumps({'current':True,'Acts':3,'subacts':9,'A08_calls':5,'sample_seconds':100,'added_seconds':0,'independent_review':False,'whole_G13':False}))
