"""One game, four conditional paired clocks. No result or dated health adoption."""
from pathlib import Path
from collections import Counter
from unittest.mock import patch
import argparse, copy, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_chicago_detroit_2021_opening_paired_regulation_carrier.py'
OUT = 'simulation/CHICAGO_DETROIT_2021_OPENING_PAIRED_REGULATION_CARRIER.json'
MD = OUT[:-5] + '.md'
BASELINE = '6eaa251fb53c93e6a9534c907369e806f56329e7'
CHI = 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json'
DET = 'research/DETROIT_2021_OPENING_NAMED_OPERATING_FAMILY_2026_10_07.json'
REC = 'research/CHICAGO_2021_22_OPENING_DET_PAIRED_INPUT_RECOVERY_2026_10_07.json'
PAIRED = 'simulation/CHICAGO_2021_22_PAIRED_INPUTS.json'
ROLE = 'simulation/CHICAGO_2021_22_ROLE_PLAN_INPUTS.json'
EG = 'design/A07_OPENING_GAME_ELBOW_OBSERVATION_FAMILY_2026_10_07.json'
CD = 'design/A07_CHANGED_DEFENSE_ROLE_EVALUATION_2026_10_07.json'
PINS = {'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json': '73d51b630e9c9d4ec31b7e3952906165589bd8c49a48bb07c79bdc9ad02e8fca', 'research/DETROIT_2021_OPENING_NAMED_OPERATING_FAMILY_2026_10_07.json': '7490b1a46a744088980c115680140383615a2e6ec92901e1fdd901c326861be0', 'research/CHICAGO_2021_22_OPENING_DET_PAIRED_INPUT_RECOVERY_2026_10_07.json': 'e731ab02a83e1135137da08a5384afbc077111cddb5a7d6ad8a4ba8f921e9f70', 'simulation/CHICAGO_2021_22_PAIRED_INPUTS.json': 'db727ddc89e354da7603c2563aaa4b58d9b543e124b0c4bd9de9df45d7ea9c6f', 'simulation/CHICAGO_2021_22_ROLE_PLAN_INPUTS.json': '0b8f9e4ac212596d0966f82f7f8317f7a7c86645a239a5a73587dd121f77e171', 'design/A07_OPENING_GAME_ELBOW_OBSERVATION_FAMILY_2026_10_07.json': 'f72d2ea63ebde3bdb0d9b0cfc2d28d4b35250e74d1160811c1cb6fc60ffe192e', 'design/A07_CHANGED_DEFENSE_ROLE_EVALUATION_2026_10_07.json': 'a41e21e63bb83f8434e624c3609c89c7e758a3062143ab7314ac01252d1428df', 'tools/build_chicago_2021_22_m1_dated_working_minutes.py': 'fe26befaf33d0da47a5614021ec2ed7f403e5f087ecf1acdc0e63e91fd2e9e1b', 'tools/build_detroit_2021_opening_named_operating_family.py': 'ff635732271be6c65959a4d60e5f8f72deb79eba01fe1fb1c69532d000375fe9', 'tools/build_a07_opening_game_elbow_observation_family.py': '100bc7986b25f15db3a8a12fdf2dc90b38715471d6fd4a889026f4312838e2da', 'tools/build_a07_changed_defense_role_evaluation.py': '80b47ba15faf5e80cca08d5bbd29397dc4e8d1d87b19ad43ba46cae27ea1feac'}
POSITIONS = ('PG', 'SG', 'SF', 'PF', 'C')
GAME = {'game_id': '0022100004', 'date': '2021-10-20', 'home': 'DET', 'away': 'CHI'}

def text(p):
    return (ROOT / p).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')

def sha(p):
    return hashlib.sha256(text(p).encode()).hexdigest()

def load(p):
    return json.loads(text(p))

def source_inputs():
    assert PINS and all(sha(p) == h for p, h in PINS.items()), 'Reviewed source SHA changed'
    data = {p: load(p) for p in (CHI, DET, REC, PAIRED, ROLE, EG, CD)}
    # Separate physical-file read protects against patched loader returns with unchanged hashes.
    for p, value in data.items():
        assert value == json.loads(text(p)), 'Source loader return differs from pinned document'
    c, d, r = data[CHI], data[DET], data[REC]
    # Check carrier production inputs are still current without repeating all82 constructors.
    for upstream in (c, d):
        assert all(sha(p) == h for p,h in upstream['source_sha256'].items()), 'Upstream carrier source no longer current'
    assert c['certification']['independent_review_completed'] is True
    assert d['certification']['independent_review_completed'] is True
    assert r['verification']['independent_review_completed'] is True
    rows = [x for x in c['rows'] if x['game_id'] == GAME['game_id']]
    assert len(rows) == 2 and {x['state'] for x in rows} == {'NORMAL', 'COBY_OUT'}
    for x in rows:
        assert (x['candidate_date'], x['home'], x['away'], x['game_number']) == ('2021-10-20', 'DET', 'CHI', 1)
        assert x['state_selected_for_date'] is False and x['substitution_order_selected'] is False
        assert x['player_minutes']['Markkanen'] == 32 and x['player_minutes']['Caruso'] == 18 and x['player_minutes']['Protagonist'] == 32
    dr = next(x for x in data[PAIRED]['rotations'] if x['id'] == 'DET_0022100004')
    assert dr['lineup_witness'] == r['regulation_pair_comparison']['DET_existing_G14_candidate']['unordered_regulation_blocks']
    assert dr['position_minutes'] == r['regulation_pair_comparison']['DET_existing_G14_candidate']['position_minutes']
    assert d['positive_minutes'] == r['regulation_pair_comparison']['DET_existing_G14_candidate']['player_minutes']
    assert {x['id'] for x in d['roster_candidates']} == {'A_garza_two_way_retained', 'B_lyles_not_signed'}
    assert data[EG]['certification']['independent_review_completed'] and data[CD]['certification']['independent_review_completed']
    assert data[CD]['cumulative_capacity']['total_reserved_seconds_per_player'] == 80
    return data, rows, dr

def timeline(blocks):
    elapsed, out = 0, []
    for i, block in enumerate(blocks):
        sec = block['minutes'] * 60
        assert isinstance(sec, int) and sec > 0
        out.append({'block_index': i, 'start_second': elapsed, 'end_second': elapsed + sec, 'positions': copy.deepcopy(block['positions'])})
        elapsed += sec
    assert elapsed == 2880, 'Source blocks must cover exactly regulation'
    return out

def assert_timeline(out, blocks):
    assert len(out) == len(blocks)
    t = 0
    for i, (row, block) in enumerate(zip(out, blocks)):
        n = int(block['minutes']) * 60
        assert row == {'block_index': i, 'start_second': t, 'end_second': t+n, 'positions': block['positions']}, 'Returned clock differs from source block'
        t += n
    assert t == 2880

def nominations(c, d):
    return {'CHI': {'standard': c['standard_registered_candidate'], 'two_way': c['two_way_registered_candidate'],
                    'active': c['working_active_nominees'], 'inactive': c['standard_inactive_nominees'],
                    'unavailable_condition': c['conditional_unavailable'], 'positive_seconds': {k: v*60 for k,v in c['player_minutes'].items()}},
            'DET': {'standard': d['standard_candidate'], 'two_way': d['two_way_candidate'],
                    'active': d['working_active_standard_12'], 'inactive': d['working_inactive_standard_3'],
                    'unavailable_condition': [], 'positive_seconds': {}}}

def construct(c, d, ct, dt, det_minutes):
    bounds = sorted({0, 720, 1440, 2160, 2880} | {x['start_second'] for x in ct+dt} | {x['end_second'] for x in ct+dt})
    segments = []
    for a,b in zip(bounds,bounds[1:]):
        cc = next(x for x in ct if x['start_second'] <= a < x['end_second'])
        dd = next(x for x in dt if x['start_second'] <= a < x['end_second'])
        q = a//720+1
        segments.append({'start_second': a, 'end_second': b, 'seconds': b-a, 'quarter': q,
                         'quarter_clock_start_seconds_remaining': q*720-a,
                         'quarter_clock_end_seconds_remaining': q*720-b,
                         'CHI_block_index': cc['block_index'], 'DET_block_index': dd['block_index'],
                         'CHI': copy.deepcopy(cc['positions']), 'DET': copy.deepcopy(dd['positions'])})
    nom = nominations(c,d)
    nom['DET']['positive_seconds'] = {k:v*60 for k,v in det_minutes.items()}
    return {'id': c['state']+'__'+d['id'], 'CHI_state': c['state'], 'DET_roster_candidate': d['id'],
            'selected_for_date': False, 'nominations': copy.deepcopy(nom), 'simultaneous_segments': segments,
            'elapsed_seconds': 2880, 'team_player_seconds': {'CHI':14400,'DET':14400},
            'score': None, 'winner': None, 'new_author_lock': False}

def assert_pair(row, c, d, ct, dt, dr, role, observations):
    assert row['id'] == c['state']+'__'+d['id'] and row['CHI_state'] == c['state'] and row['DET_roster_candidate'] == d['id']
    expected_nom = nominations(c,d)
    expected_nom['DET']['positive_seconds'] = {k:v*60 for k,v in dr['player_minutes'].items()}
    assert row['nominations'] == expected_nom, 'Roster, active nomination or ownership changed'
    assert row['selected_for_date'] is False and row['score'] is None and row['winner'] is None and row['new_author_lock'] is False
    for team, n in row['nominations'].items():
        assert len(n['standard']) == len(set(n['standard'])) == 15 and len(n['two_way']) == len(set(n['two_way'])) == 2
        assert not set(n['standard']) & set(n['two_way'])
        assert len(n['active']) == len(set(n['active'])) == 12 and len(n['inactive']) == 3
        assert set(n['active']) | set(n['inactive']) == set(n['standard']) and not set(n['active']) & set(n['inactive'])
        assert set(n['positive_seconds']) <= set(n['active']) and not set(n['active']) & set(n['unavailable_condition'])
    assert not set(row['nominations']['CHI']['standard']+row['nominations']['CHI']['two_way']) & set(row['nominations']['DET']['standard']+row['nominations']['DET']['two_way'])
    bounds = sorted({0,720,1440,2160,2880} | {x['start_second'] for x in ct+dt} | {x['end_second'] for x in ct+dt})
    segs = row['simultaneous_segments']
    assert len(segs) == len(bounds)-1
    player = {'CHI': Counter(), 'DET':Counter()}
    position = {'CHI': {p:Counter() for p in POSITIONS}, 'DET':{p:Counter() for p in POSITIONS}}
    for j, seg in enumerate(segs):
        a,b = bounds[j:j+2]
        assert (seg['start_second'],seg['end_second'],seg['seconds']) == (a,b,b-a), 'Simultaneous clock gap, overlap or duration changed'
        q=a//720+1
        assert (seg['quarter'],seg['quarter_clock_start_seconds_remaining'],seg['quarter_clock_end_seconds_remaining']) == (q,q*720-a,q*720-b)
        for team, clock, eligibility, creator in [('CHI',ct,role,['LaMelo_pick4','LaVine']),('DET',dt,dr['eligibility'],dr['required_creator_any_of'])]:
            src = next(x for x in clock if x['start_second'] <= a < x['end_second'])
            assert b <= src['end_second'] and seg[team+'_block_index'] == src['block_index'] and seg[team] == src['positions'], 'Simultaneous lineup differs from its timed source block'
            line = seg[team]
            assert set(line) == set(POSITIONS) and len(set(line.values())) == 5
            assert set(line.values()) <= set(row['nominations'][team]['active'])
            assert set(line.values()) & set(creator)
            for p,n in line.items():
                assert n in eligibility[p], 'Position eligibility changed'
                player[team][n] += b-a
                position[team][p][n] += b-a
    for team, positions in [('CHI',c['position_minutes']),('DET',dr['position_minutes'])]:
        assert dict(player[team]) == row['nominations'][team]['positive_seconds'], 'Player seconds changed'
        assert sum(player[team].values()) == 14400
        for p in POSITIONS:
            assert dict(position[team][p]) == {n:v*60 for n,v in positions[p].items()} and sum(position[team][p].values()) == 2880
    # Existing four reserved plays occupy time already counted, never new player seconds.
    for w in observations:
        assert w['seconds'] == 20 and w['end_second']-w['start_second'] == 20
        for team in ('CHI','DET'):
            covered=0
            for seg in segs:
                overlap=max(0,min(w['end_second'],seg['end_second'])-max(w['start_second'],seg['start_second']))
                if overlap:
                    assert set(seg[team].values()) == set(w['five_per_team'][team]), 'Reserved play common lineup unavailable'
                    covered+=overlap
            assert covered == 20
    assert row['elapsed_seconds'] == 2880 and row['team_player_seconds'] == {'CHI':14400,'DET':14400}

def build():
    data, cr, source_det = source_inputs()
    recovery_det=data[REC]['regulation_pair_comparison']['DET_existing_G14_candidate']
    dr={**source_det,'player_minutes': recovery_det['player_minutes']}
    common=data[CD]['cumulative_capacity']['five_per_team']
    samples=data[CD]['prior_two_pre_catch_help_samples_preserved']+data[CD]['new_changed_defense_observations']
    assert [x['id'] for x in samples] == ['EG1_LATE_RETURN','EG2_EARLY_RETURN','CD1_INSIDE_STAY_FAILURE','CD2_DELAYED_HELP_STOP']
    windows=[{'sample_id':s['id'],'start_second':500+40*i,'end_second':520+40*i,'seconds':20,
              'five_per_team':common,'within_existing_minutes_not_extra_seconds':True,
              'absolute_placement_classification':'NEW_ROUTINE_CANDIDATE_CLOCK_NOT_HISTORICAL_FACT'} for i,s in enumerate(samples)]
    assert len(windows)==4 and windows[-1]['end_second']==640
    det_clock=timeline(source_det['lineup_witness'])
    assert_timeline(det_clock,source_det['lineup_witness'])
    rows=[]
    for c in cr:
        chi_clock=timeline(c['unordered_regulation_blocks'])
        assert_timeline(chi_clock,c['unordered_regulation_blocks'])
        for d in data[DET]['roster_candidates']:
            row=construct(c,d,chi_clock,det_clock,dr['player_minutes'])
            assert_pair(row,c,d,chi_clock,det_clock,dr,data[ROLE]['position_eligibility_design_only'],windows)
            rows.append(row)
    assert len(rows)==4 and len({r['id']for r in rows})==4
    progress=copy.deepcopy(data[REC]['progress'])
    progress['seven_rows'][2]['state']='첫 CHI–DET 전체 정규 시계4조합 독립수용; 경로/건강/성과 미선택'
    return {'id':'CHICAGO_DETROIT_2021_OPENING_PAIRED_REGULATION_CARRIER',
            'status':'INDEPENDENTLY_REVIEWED_CONDITIONAL_FULL_REGULATION_PAIR','baseline_main':BASELINE,
            'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'Repository UTF8 BOMstrip, CRLF/CR to LF',
            'game':GAME,'policy':{'clock_order':'Original unordered witness list order is a NEW routine candidate order; quarter cuts inserted without changing lineups or seconds.',
                                'quantifier':'For each of two CHI availability states and two DET roster alternatives, if named contract/availability/active conditions hold, one simultaneous regulation clock exists.',
                                'state_or_DET_direction_selected':False,'OT_selected':False,'regulation_only':True,
                                'zero_minutes_are_clinical_absence':False,'actual_receipt_or_medical_certified':False},
            'conditional_acquisition_and_availability':{'CHI':'Retain reviewed SQ1 15STD2TW and lawful A/M1 family. NORMAL or Coby-out is a conditional input; no dated health adoption. Mark32/Caruso18/P32 retained.',
                'DET':'2020 Williams7/Kira16/Stewart19 approved; 2021 Suggs5/Livers38/Aldama37/Garza53 draft and applicable contracts remain candidates. Plumlee retention and Jordan joint prefix/return assets are conditional, not author locks.',
                'A':'Garza TW/Smith TW, Lyles STD; slot and clock capacity only. Named cap-route A still lacks a completed continuous cost route.',
                'B':'Lyles unsigned, Garza STD, Pickett/Smith TW; reviewed minimum/roomMLE/Bird/q and DET/BKN cost families support narrower candidate routes, not selection or whole-party execution.',
                'active':'Source-nominated12STD active/3STD inactive and2TW separate in each team. All active nominees admitted operationally available; positive5 always active. Unused reserve clinical states null.',
                'no_source_collection_repeated':True},
            'existing_four_play_clock_embeddings':windows,'witnesses':rows,
            'summary':{'game_keys':1,'conditional_combinations':4,'source_CHI_blocks_each':11,'source_DET_blocks_each':9,
                       'simultaneous_segments_each':len(rows[0]['simultaneous_segments']),
                       'regulation_seconds_each':2880,'team_player_seconds_each':14400,'pair_player_seconds_each':28800,
                       'existing_play_seconds_embedded_not_added':80,'executed_state_or_direction_choices':0,'new_game_results':0},
            'verification_scope':{'upstream_CHI_13_source_digests_current':True,'upstream_DET_12_source_digests_current':True,
                                  'previous_82date_or_cost_case_constructors_repeated':False,
                                  'fresh_primary_collection_count':0,'writer_source_join_is_independent_review':False},
            'remaining_named_inputs':['Choose dated CHI availability state and DET A/B/P0B acquisition path only within existing authority; not done here.',
                'DET A continuous legal cost route remains incomplete; both alternatives here certify capacity conditional on lawful named contracts.',
                'Before an executed opening result, join candidate prior draft/returned assets and changing counterpart rosters/costs in adopted scope.',
                'Adopt regulation/OT game scope and productivity/result method separately. No historical overtime, box or winner inherited.',
                'Other81 opponents/dates, full season/contract choices and later titles remain outside this one-game carrier.'],
            'certification':{'simultaneous_regulation_capacity_constructed':True,'independent_review_completed':True,
                             'independent_review_basis':'Root independently read source JSON without importing this producer; checked all2880-second arrays against original CHI11/DET9 blocks, positive player budgets, ownership and active nomination, four80-second embeddings and unselected conditions. Writer3 negative controls are not counted as independent review.',
                             'full_legal_acquisition_execution_certified':False,'actual_registration_or_health_certified':False,
                             'whole_game_OT_or_result_selected':False,'whole82_games_or_macro3_complete':False,
                             'new_author_lock':False,'REGISTER_or_central_changed':False,'actual_context_packs':0,'manuscript_written':0},
            'progress':progress}

def validate(o):
    try:
        assert o==build(),'Saved pair differs from source-bound reconstruction'
        return []
    except (AssertionError,KeyError,OSError,ValueError,StopIteration) as e:
        return [str(e)]

def markdown(o):
    s=o['summary']
    lines=['# Chicago–Detroit 첫 경기: 정규시간 전체 동시 입력','',o['status'],'',
           '2021-10-20 / 0022100004 / DET 홈·CHI 원정. 같은 달력은 가설이다. 기존 독립 검문된 분배 증인으로 NORMAL·COBY_OUT × Detroit A·B의 네 조건부 조합을 구성했다. 방향·건강·스코어 선택은 없다.','',
           f"각 조합 **48분·팀별240분**, 양 팀 선수시간480분. Chicago11/Detroit9개 원블록의 목록 순서를 새 교대 순서 후보로 놓고 쿼터 및 양 팀 교대 경계를 합쳐 **{s['simultaneous_segments_each']}개 동시 구간**을 만들었다. 모든 구간은 양쪽 각각5명이며 동일 선수가 두 팀에 없고, 포지션마다48분·선수별 초·active12/STDinactive3/TW2를 원자료와 직접 대조했다.",'',
           '## 기존 관측과 시간 연결','',
           '원 EG1/EG2/CD1/CD2 네20초 표본을 경기 경과500–520, 540–560, 580–600, 620–640초에 **후보 배치**했다. 네 표본의 기존 공통5인이 동시에 있다. 기존 분에서 소비되는80초이며 새분을 가산하지 않는다. 표본의 플레이/성공·실패 내용은 수정하지 않는다. 이는 당시 실제 플레이시각이나 포제션 간격 인증이 아니다.','',
           '## 조건과 실제 남은 범위','',
           'Chicago는 M1 Mark32·Caruso18·주인공32를 보존한다. Coby-out은 조건부 인자이며 실제 부상/DNP를 복사하지 않는다. Detroit의 2020 지명3명은 승인, Suggs는 **2021 후보**다. Plumlee 잔류·Jordan 선행거래·반대급부·신인 UPC는 후보 조건이다. A는 Garza TW/Lyles STD, B는 Garza STD/Lyles 미서명이며 둘 다 양수10명을 보존한다. A의 연속 비용 경로는 미완료라 전체 합법 실행으로 승격하지 않는다. B의 검문된 비용 가족도 방향 선택/전체 수락을 뜻하지 않는다.','',
           '양수 출전자는 작업 가용성을 조건으로 하고, active의 무출전 선수도 작업 명목가용성만 둔다. 0분/STDinactive/TW를 임상 결장으로 읽지 않는다. 미공개 접수증명은 새 종료 요건이 아니다. 전체 정규 시계의 용량 준비는 완료, actual health/등록·연장·결과·82경기 실행은 미완료다.','',
           '## 검문·출처','',
           '기존 검문본의 정규화 지문과 별도 직접 JSON 원읽기를 대조한다. 원시계를 source블록에서 바인딩하고 construct 반환을 호출자에서 재검문한다. Root는 이 생성기를 import하지 않고 원CHI11/DET9 블록과2880초 배열 전수일치·선수분·소속/active·네80초 포함·미선택조건을 독립 검문해 수용했다. 새 웹/AGY/NLM/Claude 수집은 이 기계적 조인에서 실행하지 않았다. 작성자 음성3건을 독립 검문으로 계수하지 않는다.','',
           '[CHI 조건부 분 입력](CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.md) · [DET 운영 후보](../research/DETROIT_2021_OPENING_NAMED_OPERATING_FAMILY_2026_10_07.md) · [최신 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','',
           '## 7행 현황','', '| 번호 | 작업 | 상태 |','|---|---|---|']
    for r in o['progress']['seven_rows']:
        state=r['state'] if r['number']!=3 else '첫 CHI–DET 전체 정규 시계4조합 독립수용; 경로/건강/성과 미선택'
        lines.append(f"| {r['number']} | {r['group']} | {state} |")
    lines.extend(['','미완료 큰묶음5. freeze **v0.30 PARTIAL**, 설계·원고 **CLOSED**, 실제Pack0·원고0. 중앙/원장 변경0.',''])
    return '\n'.join(lines)

def self_test():
    count=0
    original=construct
    def bad_duration(*a):
        o=original(*a);o['simultaneous_segments'][0]['end_second']+=1;return o
    def bad_identity(*a):
        o=original(*a);o['simultaneous_segments'][0]['DET']['C']='Carter';return o
    for fn in (bad_duration,bad_identity):
        with patch(__name__+'.construct',fn):
            try:build()
            except AssertionError:count+=1
            else:raise AssertionError('Returned pair mutation falsely passed')
    oldload=load
    def bad_source(p):
        o=oldload(p)
        if p==DET:o['roster_candidates'][0]['standard_candidate'][0]='Carter'
        return o
    with patch(__name__+'.load',bad_source):
        try:build()
        except AssertionError:count+=1
        else:raise AssertionError('Source ownership mutation falsely passed')
    return count

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
    o=build()
    if args.write:
        (ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (ROOT/MD).write_text(markdown(o),encoding='utf-8')
    result={'summary':o['summary']}
    if args.check:
        assert load(OUT)==o and text(MD)==markdown(o),'Saved JSON/MD is stale'
        result['current']=True
    if args.self_test:result['writer_negative_controls_rejected']=self_test()
    print(json.dumps(result,ensure_ascii=False))
