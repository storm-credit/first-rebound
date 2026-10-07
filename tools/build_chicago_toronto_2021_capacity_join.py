"""Four first-date TOR conditional clocks joined to selected CHI availability.

Extends the frozen 82-key dispatcher without reconstructing accepted ancestors.
Contract execution, TOR path/health and game results remain separate inputs.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from collections import Counter
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_toronto_2021_capacity_join.py'
OUT='simulation/CHICAGO_TORONTO_2021_FIRST_DATE_CAPACITY_JOIN.json'
MD=OUT.replace('.json','.md')
COMMON='simulation/CHICAGO_2021_22_OPPONENT_CAPACITY_DISPATCHER.json'
CAL='simulation/CHICAGO_2021_22_CALENDAR.csv'
AUTH='canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json'
HEALTH='simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json'
CHI='simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json'
TOR='simulation/TORONTO_2021_NAMED_ROSTER_CAPACITY_CONDITIONAL_FAMILY.json'
REVIEW='reviews/TOR_FOUR_ROLE_INDEPENDENT_REVIEW_2026_10_07.json'
PINS={'simulation/CHICAGO_2021_22_OPPONENT_CAPACITY_DISPATCHER.json': 'e1659c32a53b2ad200b759ed88d7cabde2dfe50474569e9b7860a43497b2dfa5', 'simulation/CHICAGO_2021_22_CALENDAR.csv': 'c59ea19a5515d64ed03cae8e0481847b6572d4087bbcefef15896bb7a2489183', 'canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json': '51b24c8a6bc1eb703568adced46b3ffa15845e85e8da10da1242bddf941df960', 'simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json': '274a35e163c7f6fd7f0d3e5494b3c46753aaf9900036676be935f17a9d538c32', 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json': '73d51b630e9c9d4ec31b7e3952906165589bd8c49a48bb07c79bdc9ad02e8fca', 'simulation/TORONTO_2021_NAMED_ROSTER_CAPACITY_CONDITIONAL_FAMILY.json': 'ef43ee3052540099aa33263dbe5688ca8a1231df61a6291e432894d2b61541dd', 'reviews/TOR_FOUR_ROLE_INDEPENDENT_REVIEW_2026_10_07.json': '7a8e50dae09067033b4757b4b599ea73e572ca8a5be33d3cb4aa44dbc1331214'}
POS=('PG','SG','SF','PF','C')
GID='0022100046'

def require(ok,msg):
    if not ok: raise ValueError(msg)
def sha(path):
    return hashlib.sha256(path.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()
def read(root,p): return json.loads((root/p).read_text(encoding='utf-8-sig'))
def inputs(root):
    for p,h in PINS.items(): require(sha(root/p)==h,'Reviewed source changed: '+p)
    data={p:read(root,p) for p in PINS if p!=CAL}
    for p,v in data.items(): require(v==json.loads((root/p).read_text(encoding='utf-8-sig')),'Loaded source differs: '+p)
    require(data[AUTH]['classification']=='AUTHOR_DELEGATED_DESIGN_SELECTION','Chicago authority lost')
    require(data[REVIEW]['independent_direct_checks_pass'],'TOR independent review absent')
    require(data[REVIEW]['source_sha256'][TOR]==PINS[TOR],'Review not bound to TOR rows')
    with (root/CAL).open(encoding='utf-8-sig',newline='') as f: calendar=list(csv.DictReader(f))
    require(len(calendar)==82 and len(data[HEALTH]['selected_dates'])==82,'82-key domain changed')
    return data,calendar

def chicago_clock(c):
    out=[];end=0
    for b in c['unordered_regulation_blocks']:
        sec=b['minutes']*60
        require(type(sec) is int and sec>0,'Noninteger CHI source budget')
        out.append({'start_second':end,'end_second':end+sec,'seconds':sec,'positions':deepcopy(b['positions'])});end+=sec
    require(end==2880,'CHI source is not regulation48')
    return out

def paired(c,t):
    cb=chicago_clock(c);tb=t['blocks']
    bounds=sorted({0,2880,*range(720,2880,720),*[b['end_second'] for b in cb],*[b['end_second'] for b in tb]})
    segments=[];counts={'CHI':Counter(),'TOR':Counter()};positions={'CHI':Counter(),'TOR':Counter()}
    for start,end in zip(bounds,bounds[1:]):
        picks={}
        for team,blocks in [('CHI',cb),('TOR',tb)]:
            matches=[b for b in blocks if b['start_second']<=start<end<=b['end_second']]
            require(len(matches)==1,'Source-clock join lost interval')
            p=matches[0]['positions'];require(set(p)==set(POS) and len(set(p.values()))==5,'Five positions/names changed')
            active=c['working_active_nominees'] if team=='CHI' else t['active']
            absent=c['conditional_unavailable'] if team=='CHI' else t['working_absent_condition']
            require(set(p.values())<=set(active) and not set(p.values())&set(absent),'Unavailable/nonactive player')
            picks[team]=deepcopy(p)
            for pos,n in p.items(): counts[team][n]+=end-start;positions[team][pos]+=end-start
        segments.append({'start_second':start,'end_second':end,'seconds':end-start,'quarter':start//720+1,'positions':picks})
    expected={'CHI':{n:m*60 for n,m in c['player_minutes'].items()},'TOR':t['player_seconds']}
    for team in counts:
        require(dict(counts[team])==expected[team],'Source player budget changed')
        require(sum(counts[team].values())==14400 and dict(positions[team])==dict.fromkeys(POS,2880),'240-minute role capacity changed')
    return segments,{k:dict(sorted(v.items())) for k,v in counts.items()}

def assert_joint_source(c,t,segments,seconds):
    """Check returned clocks against physical primitives at the caller boundary."""
    sources={'CHI':[],'TOR':[(b['start_second'],b['end_second'],b['positions']) for b in t['blocks']]}
    elapsed=0
    for b in c['unordered_regulation_blocks']:
        end=elapsed+b['minutes']*60
        sources['CHI'].append((elapsed,end,b['positions']));elapsed=end
    counts={'CHI':Counter(),'TOR':Counter()};position_counts={'CHI':Counter(),'TOR':Counter()};end=0
    for z in segments:
        require(z['start_second']==end and z['end_second']-end==z['seconds']>0,'Returned paired clock gap')
        require(z['quarter']==end//720+1==(z['end_second']-1)//720+1,'Returned quarter boundary changed')
        for team in counts:
            matches=[p for start,finish,p in sources[team] if start<=end<z['end_second']<=finish]
            require(len(matches)==1 and z['positions'][team]==matches[0],'Returned role differs from physical source position')
            require(set(z['positions'][team])==set(POS) and len(set(z['positions'][team].values()))==5,'Returned five-player role changed')
            for pos,n in z['positions'][team].items():
                counts[team][n]+=z['seconds'];position_counts[team][pos]+=z['seconds']
        end=z['end_second']
    require(end==2880,'Returned paired clock incomplete')
    expected={'CHI':{n:m*60 for n,m in c['player_minutes'].items()},'TOR':t['player_seconds']}
    for team in counts:
        require(dict(counts[team])==expected[team]==seconds[team],'Returned physical source player budget changed')
        require(dict(position_counts[team])==dict.fromkeys(POS,2880),'Returned position seconds changed')

def build(root=ROOT):
    d,cal=inputs(root);common=d[COMMON];hs=d[HEALTH]['selected_dates'];joined=[]
    require(len(common['dispatcher_rows'])==82 and len(d[TOR]['rows'])==4,'Input row domain changed')
    for i,(g,base,h) in enumerate(zip(cal,common['dispatcher_rows'],hs)):
        require(g['game_id']==base['game_id']==h['game_id'] and g['date']==base['candidate_date']==h['date'],'Date/source identity changed')
        require((g['home'],g['away'],g['opponent'])==(h['home'],h['away'],h['opponent']),'Date home/away/opponent changed')
        ptr=h['selected_carrier_source']['pointer'];c=d[CHI]['rows'][int(ptr.split('/')[-1])]
        require(c['game_id']==g['game_id'] and c['state']==h['selected_chicago_state'],'Selected state/carrier source changed')
        require(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected minute budget changed')
        row=deepcopy(base);row['selected_CHI_state']=h['selected_chicago_state'];row['CHI_authority_source']=AUTH
        row['selected_CHI_health_pointer']=f'/selected_dates/{i}';row['conditional_paired_clock_ids']=[]
        if g['opponent']=='TOR':
            row['status']='CONDITIONAL_TOR_FUNCTION_AVAILABLE_DATED_OPERATING_HOLD'
            row['conditional_capacity_source_available']=True;row['missing_port_id']=None
            row['remaining_HOLD']=[x for x in row['remaining_HOLD'] if x!='FULL_OPPONENT_FUNCTION_MISSING']
            row['remaining_HOLD']+=['TOR_PATH_COST_AND_DATE_AVAILABILITY_NOT_SELECTED']
            if g['game_id']==GID: row['conditional_paired_clock_ids']=[GID+'__'+t['path']+'__'+t['availability_parameter'] for t in d[TOR]['rows']]
            else: row['remaining_HOLD'].append('TOR_FIRST_DATE_PAIR_NOT_EXTENDED_TO_THIS_DATE')
        joined.append(row)
    h=next(x for x in hs if x['game_id']==GID);c=d[CHI]['rows'][int(h['selected_carrier_source']['pointer'].split('/')[-1])]
    require(h['date']=='2021-10-25' and h['selected_chicago_state']=='COBY_OUT','First TOR target health/date changed')
    pairs=[]
    for i,t in enumerate(d[TOR]['rows']):
        require(t['source_target_key']['game_id']==GID and t['source_target_key']['date']==h['date'],'TOR target changed')
        segments,seconds=paired(c,t)
        assert_joint_source(c,t,segments,seconds)
        pairs.append({'id':GID+'__'+t['path']+'__'+t['availability_parameter'],'game_id':GID,'date':h['date'],'home':'TOR','away':'CHI','CHI_selected_state':h['selected_chicago_state'],'TOR_path':t['path'],'TOR_availability_parameter':t['availability_parameter'],
          'source_pointers':{'CHI':h['selected_carrier_source']['pointer'],'TOR':f'/rows/{i}','CHI_health':'/selected_dates/3'},
          'chronological_CHI_order':'ROOT_ROUTINE_COACHING_ORDER_OF_EXISTING_BLOCKS_WITH_QUARTER_BOUNDARIES',
          'nominations':{'CHI':{'standard':c['standard_registered_candidate'],'two_way':c['two_way_registered_candidate'],'active':c['working_active_nominees'],'inactive':c['standard_inactive_nominees']},'TOR':{k:t[k] for k in ('standard','two_way','active','inactive')}},
          'simultaneous_segments':segments,'player_seconds':seconds,'elapsed_seconds':2880,'combined_player_seconds':28800,
          'required_TOR_legal_and_economic_inputs':deepcopy(t['required_legal_and_economic_inputs']),
          'CHI_date_state_selected':True,'TOR_date_state_or_contract_path_selected':False,'actual_registration_or_clinical_certified':False,'winner':None,'score':None,'OT_selected':False,'whole_game_or_season_complete':False})
    missing=sorted(set(common['missing_opponent_ports'])-{'TOR'})
    require(len(missing)==26 and Counter(x['selected_CHI_state'] for x in joined)=={'NORMAL':58,'COBY_OUT':24},'Coverage/state counts changed')
    return {'id':'CHICAGO_TORONTO_2021_FIRST_DATE_CAPACITY_JOIN','baseline_main':'e174ec1d30f11f8b786ae92cb249f8f0522ee017','source_sha256':{**PINS,SELF:sha(root/SELF)},
      'status':'SOURCE_BOUND_82_KEY_HEALTH_JOIN_WITH_FOUR_FIRST_TOR_CONDITIONAL_PAIRED_CLOCKS',
      'dispatcher_rows':joined,'TOR_first_date_pairs':pairs,'missing_opponent_ports':missing,
      'summary':{'calendar_keys':82,'CHI_selected_states':dict(Counter(x['selected_CHI_state'] for x in joined)),'new_TOR_role_function':1,'remaining_function_ports':26,'remaining_function_date_keys':sum(x['opponent'] in missing for x in joined),'TOR_source_date_pairs':4,'TOR_later_date_pairs_created':0,'new_selected_game_results':0},
      'authority':{'TOR_frozen_proposal_flags_describe_generation_state':True,'independent_conditional_capacity_review':REVIEW,'Lowry_direction_price_cost_health_or_game_result_selected':False,'whole_macro3_or_G16_certified':False,'manuscript_allowed':False},
      'consumer_api':'dispatch(game_id, root=ROOT): exact 82-key selected-CHI row and first-date conditional TOR pairs; unchanged DET/NOP capacities remain in frozen COMMON.'}

def validate(value,root=ROOT):
    try: require(value==build(root),'Output differs from physical source-bound rebuild');return []
    except (ValueError,KeyError,IndexError) as e:return [str(e)]
def dispatch(game_id,root=ROOT):
    b=build(root);rows=[r for r in b['dispatcher_rows'] if r['game_id']==game_id]
    require(len(rows)==1,'Unknown or duplicate game key')
    return {'row':rows[0],'TOR_conditional_pairs':[p for p in b['TOR_first_date_pairs'] if p['game_id']==game_id]}
def markdown(b):
    return '\n'.join(['# Toronto 첫 날짜·Chicago 선택 상태 공통 연결','','82키 Chicago NORMAL58/COBY_OUT24를 새 선택 기록에서 읽는다. TOR T0/T1 × Siakam 가용/불가용의 네 조건부 역할을 10월25일 COBY_OUT과 동시 시계로 연결했다. 각 48분·양 팀 각각240분이며 원 블록 배분과 명목 active12를 보존한다. 기존 Chicago 블록 순서를 가상 코칭 순서로 명시하고 쿼터 경계에서 나눈다.','','TOR 역할 함수는 독립 검수되어 missing27→26, 남은 함수 날짜72이다. 첫날 네 조건부 시계와 이후 TOR 세 날짜의 실제 적용을 구분한다. Lowry 방향·가격·전체 비용·TOR 건강 선택·실제 계약·승패·연장은 미완료다. 원 82키 공통 dispatcher는 동결하고 이 후속 API가 새 함수와 선택 상태를 연결한다. DET/NOP 원 용량을 지우거나 전체 시즌으로 승격하지 않는다.','','| 번호 | 상태 |','|---|---|','| 1 | 완료 |','| 2 | S2 완료 |','| 3 | TOR 첫4조건부 시계·상대26함수/72키 미완료 |','| 4 | 후속 계약·시즌 연결 미완료 |','| 5 | 전체 구조·기능 연결 미완료 |','| 6 | 독서/문체 완료·실제Pack0 |','| 7 | 전체 독립/최종 승인 미완료 |','','미완료5개 / 6번까지4개. Freeze v0.30 PARTIAL·설계/원고 CLOSED·원고0.',''])
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();b=build()
    if args.write:
        (ROOT/OUT).write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(b),encoding='utf-8')
    else: require(not validate(read(ROOT,OUT)),'Saved source-bound join invalid')
    print(json.dumps(b['summary'],ensure_ascii=False))
