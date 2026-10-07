"""Source-bound 82-key lookup; conditional capacity is not dated execution.

No missing opponent functions or new operating/health/result choices are created.
Accepted ancestor constructors are not traversed again. Consumed primitive
identities, memberships and clocks are independently bound to source objects.
"""
from __future__ import annotations
import argparse
import ast
from collections import Counter
from copy import deepcopy
import csv
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_chicago_2021_22_opponent_capacity_dispatcher.py'
OUT = 'simulation/CHICAGO_2021_22_OPPONENT_CAPACITY_DISPATCHER.json'
MD = OUT.replace('.json', '.md')
BASELINE = '51ab52af234c67ec1f34fe4dade717ba2bad9561'
SCOPE = 'design/CHICAGO_2021_22_OPPONENT_FINITE_DISPATCH_SCOPE_2026_10_07.json'
CAL = 'simulation/CHICAGO_2021_22_CALENDAR.csv'
SEED = 'simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json'
BOARD = 'research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json'
CHI = 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json'
DET = 'simulation/CHICAGO_DETROIT_2021_OPENING_PAIRED_REGULATION_CARRIER.json'
NOP = 'simulation/CHICAGO_NEW_ORLEANS_2021_SECOND_PAIRED_REGULATION_CARRIER.json'
OLD = 'simulation/CHICAGO_2021_22_PAIRED_INPUTS.json'
DET_RECOVERY = 'research/CHICAGO_2021_22_OPENING_DET_PAIRED_INPUT_RECOVERY_2026_10_07.json'
PINS = {
 SCOPE:'a57bec4bc61e2bf2030ebc25f800f06e2c64cd86e9ed573a2ccc4c4d958af203',
 CAL:'c59ea19a5515d64ed03cae8e0481847b6572d4087bbcefef15896bb7a2489183',
 SEED:'cfa2f49bb82baa49b2298d90c97cd7fd8075e91380424d40bfd44772d8228a2b',
 BOARD:'90099928f9133c4087ee7871939ce58216d183bd186f5ebd3575a56c2348eeed',
 CHI:'73d51b630e9c9d4ec31b7e3952906165589bd8c49a48bb07c79bdc9ad02e8fca',
 DET:'45f204a0f213ea51b9de0a1d0ae47b50568a8d990d339822d9cd49a6ca274a00',
 NOP:'bbb3288f239d5a181be19e0f2ac615c4acb46b13f7d11eecfa1d90990b3cbc8e',
 OLD:'db727ddc89e354da7603c2563aaa4b58d9b543e124b0c4bd9de9df45d7ea9c6f',
 DET_RECOVERY:'e731ab02a83e1135137da08a5384afbc077111cddb5a7d6ad8a4ba8f921e9f70',
}
POSITIONS = ('PG','SG','SF','PF','C')

def require(ok, message):
    if not ok:
        raise ValueError(message)

def normalized_sha(path):
    return hashlib.sha256(path.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()

def load(root, path):
    return json.loads((root/path).read_text(encoding='utf-8-sig'))

def bound_load(root, path):
    value = load(root,path)
    physical = json.loads((root/path).read_text(encoding='utf-8-sig'))
    require(value == physical, 'Loaded object differs from physical source: '+path)
    return value

def assert_scope_sources(s, calendar, seed, board, feed, team_ids):
    """Rebuild consumed semantic identities, independent of scope's own counters."""
    require(len(calendar)==82 and len({x['game_id'] for x in calendar})==82,'Calendar domain changed')
    require(set(s['teams'])=={g['opponent'] for g in calendar},'Opponent domain changed')
    require(len(s['game_keys'])==82,'Scope game domain changed')
    for g,k in zip(calendar,s['game_keys']):
        expected=(int(g['game_number']),g['game_id'],g['date'],g['home'],g['away'],g['opponent'])
        require(tuple(k[f] for f in ('game_number','game_id','candidate_date','home','away','opponent'))==expected,'Calendar identity changed')
        require(k['historical_OT_diagnostic']==int(g['inferred_historical_ot']),'Historical OT moved between dates')
        require(k['opponent_input_pointer']=='teams.'+g['opponent'],'Opponent lookup relabeled')
        require(k['alternate_result'] is None and not k['dated_operating_membership_and_availability_adopted'],'Scope adopts result/date')
    for team,t in s['teams'].items():
        gs=[g for g in calendar if g['opponent']==team]
        require(t['all_game_ids']==[g['game_id'] for g in gs] and t['game_key_count']==len(gs),'Team game keys changed')
        require(t['remaining_game_ids']==[g['game_id'] for g in gs if int(g['game_number'])>2],'Remaining keys changed')
        require(t['remaining_game_key_count']==len(t['remaining_game_ids']),'Remaining count changed')
        indexed=[(i,x) for i,x in enumerate(seed['team_game_bindings']) if x['team']==team and x['date']<='2021-05-16']
        i,b=max(indexed,key=lambda p:(p[1]['date'],p[0])); original=seed['roster_states'][b['state_id']]
        a=t['seed_S2_May16']
        require(b['date']=='2021-05-16' and a['date']==b['date'] and a['binding_event_id']==b['event_id'],'Seed date/event changed')
        require(a['binding_pointer']==f'team_game_bindings[{i}]' and a['roster_state_pointer']=='roster_states.'+b['state_id'],'Seed pointer changed')
        for klass,field in [('STANDARD','STANDARD'),('TWO_WAY','TWO_WAY')]:
            names=[x['player'] for x in original['players'] if x['contract_class']==klass]
            require(a[field]==names,'Seed roster class/identity changed')
        require(a['standard_count']==len(a['STANDARD']) and a['two_way_count']==len(a['TWO_WAY']),'Seed count changed')
        require(a['named_hardship_working_families']==b.get('working_named_hardship_families',[]) and a['named_hardship_working_capacity']==b.get('working_named_hardship_capacity',0),'Seed hardship source changed')
        require(not a['2021_22_hardship_automatically_inherited'],'Prior hardship automatically inherited')
        expected=[]
        for x in board['rows']:
            if x['conditional_final_draft_rights_holder']==team:
                expected.append((x['pick'],x['player'],x['round'],x['selecting_team'],x['conditional_final_draft_rights_holder']))
        got=[tuple(x[k] for k in ('pick','player','round','selecting_team','conditional_rights_holder')) for x in t['DB1_conditional_draft_rights']]
        require(got==expected,'DB1 right holder/player/order changed')
        require(all(not x['NBA_UPC_created'] and not x['RequiredTender_created'] and not x['new_author_lock'] for x in t['DB1_conditional_draft_rights']),'Unsigned right promoted to contract')
        relevant=[(i,x) for i,x in enumerate(feed) if team_ids.get(int(x['TEAM_ID'])-1610610000)==team and '2021-05-17'<=x['TRANSACTION_DATE'][:10]<='2022-04-10']
        events=t['reported_event_source']['events']
        require(len(events)==len(relevant),'Feed event domain changed')
        for e,(i,x) in zip(events,relevant):
            expected=(i,f'NBA_Player_Movement.rows[{i}]',x['GroupSort'],x['TRANSACTION_DATE'][:10],x['Transaction_Type'],int(x['TEAM_ID']),int(x['PLAYER_ID']) if x.get('PLAYER_ID') else None,x['PLAYER_SLUG'])
            got=tuple(e[k] for k in ('source_row_index','source_pointer','GroupSort','reported_date','transaction_type','TEAM_ID','player_id','player_slug'))
            require(got==expected,'Feed consumed actor/date/type changed')
            require(not e['fictional_event_applied'] and e['exact_receipt_clock'] is None,'Reported event promoted to execution')
        wanted=('REVIEWED_CONDITIONAL_FULL_REGULATION_FUNCTION' if team in ('DET','NOP') else 'PARTIAL_OLD_CONDITIONAL_STENCIL_REQUIRES_REBUILD' if team in ('SAC','ORL') else 'NO_REVIEWED_2021_22_FULL_REGULATION_OPPONENT_FUNCTION')
        require(t['category']==wanted and t['role_function']['new_full_function_input_missing']==(team not in ('DET','NOP')),'Function coverage falsely promoted')
        require(not t['role_function']['all_remaining_dates_validated'],'Remaining dates promoted')
    require(s['counts']['new_role_functions_created']==0 and s['counts']['newly_certified_contract_families']==0,'Scope creates absent functions')

def inputs(root):
    for p,h in PINS.items():
        require(normalized_sha(root/p)==h,'Reviewed source changed: '+p)
    data={p:bound_load(root,p) for p in PINS if p!=CAL}
    scope=data[SCOPE]
    for p,h in scope['source_sha256'].items():
        require(normalized_sha(root/p)==h,'Scope ancestor currentness failed: '+p)
    with (root/CAL).open(encoding='utf-8-sig',newline='') as f:
        calendar=list(csv.DictReader(f))
    raw=Path(scope['raw_feed_source']['path']).read_bytes()
    require(hashlib.sha256(raw).hexdigest()==scope['raw_feed_source']['raw_sha256'],'Raw feed changed')
    feed=json.loads(raw.decode('utf-8-sig'))['NBA_Player_Movement']['rows']
    tree=ast.parse((root/'tools/build_2020_21_dated_roster_execution_bridge.py').read_text(encoding='utf-8-sig'))
    team_ids=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TEAM_IDS' for t in n.targets))
    assert_scope_sources(scope,calendar,data[SEED],data[BOARD],feed,team_ids)
    return data,calendar

def timeline(blocks):
    out=[]; elapsed=0
    for i,b in enumerate(blocks):
        seconds=b['minutes']*60
        require(isinstance(seconds,int) and seconds>0,'Noninteger/empty block')
        require(set(b['positions'])==set(POSITIONS) and len(set(b['positions'].values()))==5,'Block lacks five unique positions')
        out.append((elapsed,elapsed+seconds,i,deepcopy(b['positions'])))
        elapsed+=seconds
    require(elapsed==2880,'Regulation template is not 48 minutes')
    return out

def assert_nomination(nom, expected, positive):
    require(nom['standard']==expected['standard'] and nom.get('two_way',nom.get('TW'))==expected['two_way'],'Nomination membership/class changed')
    for field in ('active','inactive'):
        require(nom[field]==expected[field],'Nomination '+field+' changed')
    unavailable=nom.get('unavailable_condition',nom.get('unavailable'))
    require(unavailable==expected['unavailable'],'Unavailable condition changed')
    require(len(nom['standard'])==15 and len(nom['active'])==12 and len(set(nom['active']))==12,'Working slot/active count changed')
    require(set(nom['active']).isdisjoint(nom['inactive']) and set(nom['active'])|set(nom['inactive'])==set(nom['standard']),'Active/inactive partition changed')
    require(set(positive)<=set(nom['active']) and set(positive).isdisjoint(unavailable),'Positive role not actively available')

def assert_capacity(w, opponent, pair, data):
    """Bind every returned clock segment to primitive source blocks and nominations."""
    require(not w['selected_for_date'] and w['score'] is None and w['winner'] is None,'Capacity adopted execution/result')
    game=pair['game']; gid=game['game_id']
    rows=[x for x in data[CHI]['rows'] if x['game_id']==gid and x['state']==w['CHI_state']]
    require(len(rows)==1,'CHI capacity source missing')
    chi=rows[0]; ct=timeline(chi['unordered_regulation_blocks'])
    if opponent=='DET':
        role=next(x for x in data[OLD]['rotations'] if x['id']=='DET_0022100004')
        ot=timeline(role['lineup_witness'])
        branch=next(x for x in data[DET_RECOVERY]['opening_roster_recovery']['named_slot_candidates'] if x['id']==w['DET_roster_candidate'])
        source=w['nominations']['DET']
        positive=Counter({p:v*60 for p,v in data[DET_RECOVERY]['regulation_pair_comparison']['DET_existing_G14_candidate']['player_minutes'].items()})
        active=[p for p in branch['standard_candidate'] if p in positive]
        active += [p for p in branch['standard_candidate'] if p not in positive][:12-len(active)]
        expected={'standard':branch['standard_candidate'],'two_way':branch['two_way_candidate'],'active':active,'inactive':[p for p in branch['standard_candidate'] if p not in active],'unavailable':[]}
    else:
        role=pair['NOP_named_proposal']; ot=timeline(role['ordered_working_blocks']); source=w['nominations']['NOP']; positive=Counter(role['positive_player_seconds'])
        expected={'standard':role['standard_candidate'],'two_way':role['two_way_candidate'],'active':role['active_standard_12'],'inactive':role['inactive_standard_3'],'unavailable':role['operational_unavailable_condition']}
    chi_expected={'standard':chi['standard_registered_candidate'],'two_way':chi['two_way_registered_candidate'],'active':chi['working_active_nominees'],'inactive':chi['standard_inactive_nominees'],'unavailable':chi['conditional_unavailable']}
    assert_nomination(w['nominations']['CHI'],chi_expected,chi['player_minutes'])
    assert_nomination(source,expected,positive)
    totals={'CHI':Counter(),opponent:Counter()}; position_totals={'CHI':Counter(),opponent:Counter()}; cursor=0
    for seg in w['simultaneous_segments']:
        a,z=seg['start_second'],seg['end_second']; seconds=seg['seconds']
        require(a==cursor and z-a==seconds and 0<seconds and z<=2880,'Clock gap/overlap/duration changed')
        require(a//720==(z-1)//720 and seg['quarter']==a//720+1,'Quarter boundary changed')
        for team,t in [('CHI',ct),(opponent,ot)]:
            match=[x for x in t if x[0]<=a and z<=x[1]]
            require(len(match)==1 and seg[team]==match[0][3] and seg[team+'_block_index']==match[0][2],'Returned clock differs from primitive source block')
            for position,player in seg[team].items():
                totals[team][player]+=seconds; position_totals[team][position]+=seconds
        cursor=z
    require(cursor==2880,'Clock endpoint changed')
    require(dict(totals['CHI'])=={p:v*60 for p,v in chi['player_minutes'].items()} and totals[opponent]==positive,'Minute budgets changed')
    require(all(dict(v)==dict.fromkeys(POSITIONS,2880) for v in position_totals.values()),'Position coverage changed')
    require(all(sum(v.values())==14400 for v in totals.values()),'Team minutes changed')
    return {team:dict(sorted(v.items())) for team,v in totals.items()}

def capacity_record(w,opponent,pair,data):
    totals=assert_capacity(w,opponent,pair,data)
    return {'id':opponent+'::'+w['id'],'source_game_id':pair['game']['game_id'],'source_path':DET if opponent=='DET' else NOP,'source_pointer':'witnesses:id='+w['id'],'CHI_state':w['CHI_state'],'opponent_branch':w.get('DET_roster_candidate','NOP_ZION0_CONDITIONAL_RETAINED_CORE'),'simultaneous_segment_count':len(w['simultaneous_segments']),'regulation_seconds':2880,'player_seconds_each':14400,'positive_player_seconds':totals,'nominations':deepcopy(w['nominations']),'source_clock_verified':True,'hypothetical_operating_and_availability_conditions':True,'dated_state_adopted':False,'actual_medical_or_registration_certified':False,'score':None,'winner':None}

def assert_capacity_record(rec,w,opponent,pair,data):
    totals=assert_capacity(w,opponent,pair,data)
    require(rec['positive_player_seconds']==totals and rec['nominations']==w['nominations'],'Returned capacity changed source membership/minutes')
    require(rec['id']==opponent+'::'+w['id'] and rec['source_game_id']==pair['game']['game_id'] and rec['CHI_state']==w['CHI_state'],'Returned capacity identity changed')
    require(rec['source_path']==(DET if opponent=='DET' else NOP) and rec['source_pointer']=='witnesses:id='+w['id'],'Returned capacity source pointer changed')
    require(rec['opponent_branch']==w.get('DET_roster_candidate','NOP_ZION0_CONDITIONAL_RETAINED_CORE') and rec['hypothetical_operating_and_availability_conditions'],'Returned candidate branch changed')
    require(rec['simultaneous_segment_count']==len(w['simultaneous_segments']) and rec['regulation_seconds']==2880 and rec['player_seconds_each']==14400,'Returned capacity clock totals changed')
    require(rec['source_clock_verified'] and not rec['dated_state_adopted'] and not rec['actual_medical_or_registration_certified'] and rec['score'] is None and rec['winner'] is None,'Returned capacity falsely adopts date/result')

def typed_port(team,source):
    return {'id':'OPPONENT_INPUT::'+team,'team':team,'status':'MISSING_FULL_INPUT','game_ids':source['all_game_ids'],'existing_partial_pointer':deepcopy(source['role_function']),'required_fields':{'operating_interval':{'start_date':'ISO_DATE','end_date':'ISO_DATE_OR_REOPEN_BOUNDARY','STANDARD':'UNIQUE_NAMED_CONTRACT_FAMILY[] MAX15','TWO_WAY':'UNIQUE_NAMED_CONTRACT_FAMILY[] MAX2','rights_vs_UPC_vs_RequiredTender':'NAMED_SEPARATE_OBJECTS','economic_family':'SOURCE_SUPPORTED_BOUNDED_PARAMETERS_NOT_PRIVATE_RECEIPT','named_source_and_authority':'PATH+POINTER+CURRENT_SHA+CONSUMED_MEANING'},'availability':'EXPLICIT_HYPOTHETICAL_POSITIVE_AVAILABILITY_AND_MODELED_ABSENCE; ZERO_IS_NOT_DIAGNOSIS','nomination':'12..15 UNIQUE_ACTIVE, INACTIVE_PARTITION, TW_ELIGIBILITY/ANNUAL_COUNTS_IF_USED','role_blocks':'POSITIVE_INTEGER_SECONDS, FIVE_UNIQUE_PLAYERS_AND_POSITIONS, TOTAL2880/14400','role_eligibility_and_creators':'EXPLICIT_MODEL_RULES_WITH_SOURCE_SCOPE','dated_scope':'CANDIDATE_NOT_ACTUAL_HEALTH_OR_RESULT','OT_extension':'SEPARATE_IF_SELECTED; HISTORICAL_OT_NOT_AUTO_COPIED'},'named_current_gaps':source['named_causal_inputs'],'provided_function':None,'full_legal_contract_execution_certified':False,'new_direction_selected':False}

def dispatch_row(g,team,capacity_ids):
    number=int(g['game_number'])
    if number<=2: state='SOURCE_REVIEWED_ORIGINAL_DATE_CONDITIONAL_CAPACITY'
    elif g['opponent'] in ('DET','NOP'): state='CAPACITY_REUSE_CANDIDATE_DATED_INTERVAL_HOLD'
    elif g['opponent'] in ('SAC','ORL'): state='PARTIAL_STENCIL_NEEDS_FULL_OPPONENT_INPUT'
    else: state='MISSING_OPPONENT_FUNCTION'
    return {'game_number':number,'game_id':g['game_id'],'candidate_date':g['date'],'home':g['home'],'away':g['away'],'opponent':g['opponent'],'status':state,'capacity_ids':capacity_ids,'CHI_source_pointer':'rows:game_id='+g['game_id']+';state=NORMAL|COBY_OUT','CHI_source':CHI,'opponent_team_input_pointer':'teams.'+g['opponent'],'missing_port_id':None if g['opponent'] in ('DET','NOP') else 'OPPONENT_INPUT::'+g['opponent'],'conditional_capacity_source_available':bool(capacity_ids),'applicable_dated_operating_interval':None,'original_pair_source_date_binding_verified':number<=2,'dated_operating_interval_implementation_completed':False,'source_interval_proven_for_requested_date':False,'interval_is_a_conditional_proposal_not_executed_contract':True,'remaining_HOLD':['OPERATING_AND_AVAILABILITY_NOT_ADOPTED']+([] if number<=2 else ['DATED_SOURCE_INTERVAL_UNIMPLEMENTED'] if g['opponent'] in ('DET','NOP') else ['FULL_OPPONENT_FUNCTION_MISSING']),'executable_selected_date':False,'source_historical_OT_diagnostic':int(g['inferred_historical_ot']),'new_OT_selected':False,'score':None,'winner':None,'new_author_lock':False}

def assert_dispatch_row(row,g,ids):
    number=int(g['game_number']); opponent=g['opponent']
    require(tuple(row[k] for k in ('game_number','game_id','candidate_date','home','away','opponent'))==(int(g['game_number']),g['game_id'],g['date'],g['home'],g['away'],g['opponent']),'Returned dispatcher identity changed')
    require(row['capacity_ids']==ids and row['conditional_capacity_source_available']==bool(ids),'Returned dispatcher capacity relabeled')
    require(row['source_historical_OT_diagnostic']==int(g['inferred_historical_ot']),'Returned diagnostic date changed')
    require(not row['executable_selected_date'] and row['applicable_dated_operating_interval'] is None and not row['new_OT_selected'] and row['score'] is None and row['winner'] is None and not row['new_author_lock'],'Returned dispatcher falsely executes condition')
    require(row['original_pair_source_date_binding_verified']==(number<=2) and not row['source_interval_proven_for_requested_date'] and not row['dated_operating_interval_implementation_completed'],'Dated interval falsely certified')
    expected_status=('SOURCE_REVIEWED_ORIGINAL_DATE_CONDITIONAL_CAPACITY' if number<=2 else 'CAPACITY_REUSE_CANDIDATE_DATED_INTERVAL_HOLD' if opponent in ('DET','NOP') else 'PARTIAL_STENCIL_NEEDS_FULL_OPPONENT_INPUT' if opponent in ('SAC','ORL') else 'MISSING_OPPONENT_FUNCTION')
    require(row['status']==expected_status,'Returned source coverage status relabeled')
    require(row['CHI_source']==CHI and row['CHI_source_pointer']=='rows:game_id='+g['game_id']+';state=NORMAL|COBY_OUT' and row['opponent_team_input_pointer']=='teams.'+opponent,'Returned input pointer relabeled')
    require(row['missing_port_id']==(None if opponent in ('DET','NOP') else 'OPPONENT_INPUT::'+opponent),'Returned missing port relabeled')
    require('OPERATING_AND_AVAILABILITY_NOT_ADOPTED' in row['remaining_HOLD'],'Dated adoption HOLD removed')
    if number>2 and opponent in ('DET','NOP'):
        require(row['status']=='CAPACITY_REUSE_CANDIDATE_DATED_INTERVAL_HOLD' and 'DATED_SOURCE_INTERVAL_UNIMPLEMENTED' in row['remaining_HOLD'],'Reuse HOLD falsely removed')

def build(root=ROOT):
    data,calendar=inputs(root); scope=data[SCOPE]; catalog=[]
    # The constructor's returned source context cannot replace the physical
    # primitive objects after its own guards have already run.
    for path in PINS:
        if path!=CAL:
            require(data[path]==json.loads((root/path).read_text(encoding='utf-8-sig')),'Returned input context differs from physical source: '+path)
    with (root/CAL).open(encoding='utf-8-sig',newline='') as f:
        require(calendar==list(csv.DictReader(f)),'Returned calendar differs from source CSV')
    for opponent,path in [('DET',DET),('NOP',NOP)]:
        pair=data[path]
        require(pair['certification']['independent_review_completed'],'Pair independent review absent')
        for w in pair['witnesses']:
            rec=capacity_record(w,opponent,pair,data)
            assert_capacity_record(rec,w,opponent,pair,data)
            catalog.append(rec)
    require(len(catalog)==6 and len({x['id'] for x in catalog})==6,'Original pair combination domain changed')
    rows=[]
    for g in calendar:
        ids=[x['id'] for x in catalog if x['source_path']==(DET if g['opponent']=='DET' else NOP if g['opponent']=='NOP' else None)]
        row=dispatch_row(g,scope['teams'][g['opponent']],ids)
        assert_dispatch_row(row,g,ids); rows.append(row)
    ports={t:typed_port(t,s) for t,s in scope['teams'].items() if t not in ('DET','NOP')}
    require(len(ports)==27 and all(x['provided_function'] is None for x in ports.values()),'Missing functions invented')
    for team,port in ports.items():
        source=scope['teams'][team]
        require(port['id']=='OPPONENT_INPUT::'+team and port['team']==team and port['status']=='MISSING_FULL_INPUT' and port['game_ids']==source['all_game_ids'],'Returned typed port identity/coverage changed')
        require(port['existing_partial_pointer']==source['role_function'] and port['named_current_gaps']==source['named_causal_inputs'],'Returned typed port source requirements changed')
        require(not port['full_legal_contract_execution_certified'] and not port['new_direction_selected'],'Returned typed port falsely certified')
    counts=Counter(x['status'] for x in rows)
    require(list(counts.values()) and sorted(counts.values())==[2,4,6,70],'82-key coverage classes changed')
    source_sha={**scope['source_sha256'],**PINS,SELF:normalized_sha(root/SELF)}
    return {'schema':'CHICAGO_2021_22_OPPONENT_CAPACITY_DISPATCHER_V1','status':'INDEPENDENTLY_REVIEWED_SOURCE_BOUND_COMMON_DISPATCHER_NOT_DATED_EXECUTION','baseline_main':BASELINE,'source_sha256':source_sha,'hash_convention':'BOMstrip CRLF/CR->LF repository; unchanged raw bytes. Baseline fixed, not live HEAD.','raw_feed_source':deepcopy(scope['raw_feed_source']),'summary':{'game_keys':82,'opponent_teams':29,'reviewed_original_pair_keys':2,'original_conditional_capacity_records':6,'reuse_candidate_date_keys':4,'partial_stencil_date_keys':6,'other_missing_opponent_date_keys':70,'typed_missing_team_ports':27,'new_opponent_functions_created':0,'reported_event_rows_bound':1034,'actual_executable_selected_dates':0,'new_health_or_results':0},'capacity_index':catalog,'dispatcher_rows':rows,'missing_opponent_ports':ports,'consumer_api':{'signature':'dispatch(game_id, chi_state=None, include_clock=False, root=ROOT)','join_key':'Exact game_id; source date/home/away checked before lookup','CHI_state_domain':['NORMAL','COBY_OUT'],'separate_consumer_authority':'An independently selected dated CHI health state may request its existing role branch; this lookup does not make that selection.','unsupported_CHI_state':'CHI_STATE_OUTSIDE_VERIFIED_ROLE_DOMAIN requires a new source-backed CHI role function; do not force NORMAL.','clock_candidates':'include_clock=True returns source-game-tagged original witnesses; reuse requested date does not rename or certify original interval.','missing_opponent_output':'Empty capacity/clock list plus typed missing port, not zero minutes or fabricated roster.'},'teams_input_scope':{'path':SCOPE,'pointer':'teams','not_repeated_or_newly_selected_29_contract_families':True},'next_port_id':'OPPONENT_INPUT::TOR','next_game_id':'0022100046','remaining_scope':scope['whole3_remaining_scope'],'verification':{'writer_direct_source_semantics_checked':True,'accepted_ancestor_constructors_repeated':0,'independent_review_completed':True,'independent_review_basis':'reviews/COMMON_DISPATCHER_ROOT_REVIEW_2026_10_07.json: root independently checked82CSV identities,6combination primitive clocks and rejected PG/SG swap preserving player totals/membership. Writer controls not counted as independent.','actual_registration_or_medical_certified':False,'whole_macro3_complete':False,'central_or_register_changed':False,'new_author_choice':False},'progress_snapshot':scope['progress_snapshot']}

def dispatch(game_id,chi_state=None,include_clock=False,root=ROOT):
    packet=build(root)
    matches=[x for x in packet['dispatcher_rows'] if x['game_id']==game_id]
    require(len(matches)==1,'Unknown or duplicate game key')
    require(chi_state in (None,'NORMAL','COBY_OUT'),'CHI_STATE_OUTSIDE_VERIFIED_ROLE_DOMAIN')
    result=deepcopy(matches[0])
    capacities=[x for x in packet['capacity_index'] if x['id'] in result['capacity_ids'] and (chi_state is None or x['CHI_state']==chi_state)]
    result['requested_CHI_state']=chi_state
    result['CHI_state_selected_by_dispatcher']=False
    result['capacity_ids']=[x['id'] for x in capacities]
    result['capacity_candidates']=deepcopy(capacities)
    result['clock_candidates']=[]
    if include_clock:
        for cap in capacities:
            pair=bound_load(root,cap['source_path'])
            witness=next(x for x in pair['witnesses'] if cap['source_pointer']=='witnesses:id='+x['id'])
            result['clock_candidates'].append({'source_game_id':cap['source_game_id'],'requested_game_id':game_id,'same_original_source_game':cap['source_game_id']==game_id,'requested_interval_implementation_completed':False,'witness':deepcopy(witness)})
    return result

def validate(packet,root=ROOT):
    try:
        return [] if packet==build(root) else ['Saved dispatcher differs from source reconstruction']
    except (ValueError,KeyError,StopIteration,AssertionError) as e:
        return [str(e)]

def markdown(packet):
    lines=['# Chicago 2021–22 공통82키 dispatcher와 조건부 용량 색인','','기준 main `'+BASELINE+'`. 원CSV·S2 seed·DB1 권리·raw event의 소비 필드와 역할/명단/active/시계를 직접 연결했다. 기존 경제/시즌 조상 생성기는 다시 실행하지 않는다. root의82CSV/6조합초별 primitive 독립검문과 동일총분 PG/SG 교환반례 거부를 수용했다. 새 계약·건강·승패·중요방향 선택은0이다.','','## 조회와 범위','','`dispatch(game_id, chi_state=None, include_clock=False, root=ROOT)`는 정확 날짜·양팀·입력 포트·용량 후보와 HOLD를 반환한다. `chi_state="NORMAL"` 또는 `"COBY_OUT"`은 별도 소비자가 선택한 날짜 건강모델의 연결 키이며 dispatcher의 새 선택이 아니다. `include_clock=True`는 source_game_id를 보존한 원증인과 requested_game_id를 함께 반환한다. 재사용 날짜에 원증인 날짜를 덮어쓰지 않는다. 다른 CHI 상태는 `CHI_STATE_OUTSIDE_VERIFIED_ROLE_DOMAIN`으로 거부해 새 역할함수 필요를 드러낸다. [범위 입력](../design/CHICAGO_2021_22_OPPONENT_FINITE_DISPATCH_SCOPE_2026_10_07.md)을 소비하는 한 JSON이다.80개 문서를 만들지 않았다.','','| 날짜키 상태 | 키수 | 반환 내용 |','|---|---:|---|','| 원DET/NOP 한정 검문된 조건부 용량 | 2 | DET4/NOP2의6조합 색인·규정시간48/양팀240 |','| 후속DET/NOP 재사용 후보 | 4 | 동일 용량ID, 해당날짜 계약/소속/가용 interval HOLD |','| SAC/ORL 부분 stencil | 6 | 아직 전체 상대 함수가 없는 typed port |','| 기타25팀 | 70 | 팀별 미완typed port25개 |','','용량6개는 원11/DET9/NOP6블록의 매구간·선수분·active/소속을 직접 대조했다. 원2키의 `original_pair_source_date_binding_verified:true`는 원검문 증인 날짜 일치만 뜻한다. `dated_operating_interval_implementation_completed:false`와 `source_interval_proven_for_requested_date:false`는82전행에 남아 whole계약 날짜구현으로 승격하지 않는다. 나머지4재사용 날짜는 같은 용량의 수학적 사용 후보이며 날짜별 등록·가용 조건을 통과한 실행일이 아니다. `actual_executable_selected_dates:0`은 정직한 현재 범위이며 검토된 원용량이 없다는 뜻이 아니다. 원규정시간 증인을 실제 건강/날짜/OT/승패 선택으로 읽지 않는다.','','## 미완 입력의 typed port','','27개 port는 team·적용 interval·명명된STD/TW 계약가족·미서명권리/Tender/UPC·source/권위·양수가용 조건·active12–15·five-player 정수초 블록·position/creator 규칙·OT 분기를 요구한다. 새로운27가족을 창작하지 않았고 `provided_function:null`이다. 실제사적접수/장부 전체나 원건강 진단을 새 필수 gate로 넣지 않았다. 명명된 공개 제약과 합법한 가상 구현의 경제 구간을 받는다.','','첫 새port는TOR `0022100046`(10/25)이다. Powell/Trent/Hood/Bonga의 변경 선행과 DB1 Giddey8/Banton46/Hauser48의 권리/계약 구분은 scope 원천을 그대로 따른다. 바로 다음DET10/23은 reuse HOLD이다. reported1034행을 새가상거래로 적용하지 않는다.','','## 원천 검문','','고정source핀만 보지 않고 원CSV identity/OT, S2 May16 fullroster classification/hardship, DB1 holder/player/order/unsigned flags, rawfeed1034 actor/date/type/GroupSort/index를 재구축한다. Loaded object 및 반환 input context는 별도physical JSON/CSV와 동등해야 한다. 역할 시계는 실제 CHI primitive11·원DET9·NOP6블록과 구간별 직접 대조하고 반환객체를caller에서 재검사한다. 인덱스는 원source pointer를 유지하며 결과·가입·불확정 interval을 새확정값으로 바꾸지 않는다.','','## 7행 진행표 — 원scope 기준시점','','[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md) 우선. 아래는원scope가 보존한f90d3bc snapshot이다.','','| 번호 | 작업 | 상태 |','|---|---|---|']
    for x in packet['progress_snapshot']['rows']:
        lines.append(f"| {x['number']} | {x['group']} | {x['status']} |")
    lines+=['','미완료큰묶음5·6번까지4·v0.30 PARTIAL·설계/원고CLOSED·실제Pack0·원고0. 전체macro3/REGISTER/중앙/Git승격0.']
    return '\n'.join(lines)+'\n'

def self_test(root=ROOT):
    data,calendar=inputs(root); source=data[SCOPE]
    raw=Path(source['raw_feed_source']['path']).read_bytes(); feed=json.loads(raw)['NBA_Player_Movement']['rows']
    tree=ast.parse((root/'tools/build_2020_21_dated_roster_execution_bridge.py').read_text(encoding='utf-8-sig'))
    ids=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TEAM_IDS' for t in n.targets))
    labels=[]
    def rejects(label,fn):
        try: fn()
        except ValueError: labels.append(label); return
        raise AssertionError('FALSE_PASS: '+label)
    bad=deepcopy(source); bad['teams']['TOR']['DB1_conditional_draft_rights'][0]['conditional_rights_holder']='HOU'
    rejects('Same-count DB1 holder relabel',lambda:assert_scope_sources(bad,calendar,data[SEED],data[BOARD],feed,ids))
    bad=deepcopy(source); bad['teams']['TOR']['reported_event_source']['events'][0]['TEAM_ID']=1610612744
    rejects('Same-count reported event actor relabel',lambda:assert_scope_sources(bad,calendar,data[SEED],data[BOARD],feed,ids))
    w=deepcopy(data[DET]['witnesses'][0]); w['simultaneous_segments'][0]['DET']['PG']='Lonzo Ball'
    rejects('Source clock player replaced',lambda:assert_capacity(w,'DET',data[DET],data))
    w=deepcopy(data[NOP]['witnesses'][0]); w['nominations']['NOP']['active'][0]='Zion Williamson'
    rejects('Same-count active membership replacement',lambda:assert_capacity(w,'NOP',data[NOP],data))
    original=dispatch_row
    def false_execution(*a,**kw):
        value=original(*a,**kw)
        if int(a[0]['game_number'])==3: value['executable_selected_date']=True
        return value
    with patch.dict(globals(),{'dispatch_row':false_execution}):
        rejects('Returned reuse row false execution',lambda:build(root))
    return labels

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--write',action='store_true'); parser.add_argument('--check',action='store_true'); parser.add_argument('--self-test',action='store_true'); args=parser.parse_args()
    packet=build()
    if args.write:
        (ROOT/OUT).write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
        (ROOT/MD).write_text(markdown(packet),encoding='utf-8',newline='\n')
    result={'summary':packet['summary']}
    if args.check:
        errors=validate(load(ROOT,OUT)); require(not errors,str(errors)); require((ROOT/MD).read_text(encoding='utf-8-sig').replace('\r\n','\n')==markdown(packet),'MD stale'); result['current']=True
    if args.self_test: result['writer_negative_controls']=self_test()
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__': main()
