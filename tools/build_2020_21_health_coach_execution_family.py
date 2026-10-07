"""Join the finite registered health/coach family without copying source vectors.

Positive availability is an author model; unused reserve health stays null.
Two H00 incident games receive separate working early-exit clock plans.
"""
from pathlib import Path
from collections import Counter, defaultdict
from copy import deepcopy
import argparse, hashlib, json, math
import fitz
import build_2020_21_dated_roster_execution_bridge as roster
import build_2020_21_regular_working_chronology as chrono
import build_2021_l2_working_chronology as l2chrono
import build_h00_dated_health_application as h00builder
import build_h00_six_game_minute_bridge as sixbuilder

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2020_21_health_coach_execution_family.py'
OUT='simulation/NBA_2020_21_HEALTH_COACH_EXECUTION_FAMILY.json'
MD=OUT[:-5]+'.md'
H00='simulation/LAKERS_2020_21_H00_DATED_HEALTH_APPLICATION.json'
SIX='simulation/LAKERS_2020_21_H00_SIX_GAME_MINUTE_BRIDGE.json'
RCH='simulation/NBA_2020_21_REGULAR_WORKING_CHRONOLOGY.json'
LCH='simulation/NBA_2021_L2_WORKING_CHRONOLOGY.json'
AUTH='canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
INPUTS=[roster.OUT,roster.SELF,roster.REG,roster.L2,roster.POST,RCH,LCH,H00,SIX,
    AUTH,'canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json',
    'AGENTS.md','tools/build_2020_21_regular_working_chronology.py',
    'tools/build_2021_l2_working_chronology.py',
    'tools/build_h00_dated_health_application.py','tools/build_h00_six_game_minute_bridge.py',SELF]
TOL=1e-5

def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256((ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()
def key(g):return (g['phase'],g['event_id'],g['team'])

def k_witness(v,duration,k):
    """Uniform k-subset decomposition; every individual budget <= duration."""
    left={p:float(n) for p,n in v.items() if n>TOL};remain=float(duration);out=[]
    assert all(0<=n<=duration+TOL for n in left.values())
    assert abs(sum(left.values())-k*duration)<=TOL
    while remain>TOL:
        people=sorted(left,key=lambda p:(-left[p],p))[:k]
        assert len(people)==k
        other=max((left[p] for p in left if p not in people),default=0)
        step=min(min(left[p] for p in people),remain-other)
        assert step>TOL
        out.append((step,people))
        for p in people:left[p]-=step
        left={p:n for p,n in left.items() if n>TOL}
        remain-=step
    assert not left
    return out

def early_exit(row,actor):
    """Place the incident actor continuously before a modeled permanent exit.

    This is a new working order, not the observed injury time or contact event.
    After the 180s starter prefix choose q_i for the first actor-budget seconds:
    max(0, v_i-(T-a), starter_prefix) <= q_i <= min(v_i,a-prefix_if_nonstarter).
    sum q_i=4a; decompose remaining first phase in four-person sets, then five.
    """
    v={p:float(s) for p,s in row['player_seconds'].items() if s>0}
    T=row['game_duration_seconds'];a=v[actor];prefix=180.0
    starters=set(row['starters']);assert actor in starters and prefix<a<T
    others={p:n for p,n in v.items() if p!=actor}
    lo={p:max(0,n-(T-a),prefix if p in starters else 0) for p,n in others.items()}
    hi={p:min(n,a if p in starters else a-prefix) for p,n in others.items()}
    assert all(lo[p]<=hi[p]+TOL for p in others)
    need=4*a-sum(lo.values());assert need>=-TOL and need<=sum(hi[p]-lo[p] for p in others)+TOL
    q=dict(lo)
    for p in sorted(q):
        add=min(max(0,need),hi[p]-q[p]);q[p]+=add;need-=add
    assert abs(need)<=TOL
    first={p:q[p]-(prefix if p in starters else 0) for p in others}
    last={p:others[p]-q[p] for p in others}
    segments=[(prefix,sorted(starters))]
    segments += [(n,sorted(people+[actor])) for n,people in k_witness(first,a-prefix,4)]
    segments += [(n,sorted(people)) for n,people in k_witness(last,T-a,5)]
    elapsed=0.0;blocks=[]
    for budget,people in segments:
        while budget>TOL:
            boundary=next(t for t in chrono.period_ends(T) if t>elapsed+TOL)
            step=min(180.0,budget,boundary-elapsed);elapsed+=step;budget-=step
            blocks.append({'end_seconds':elapsed,'players':people})
    totals=defaultdict(float);start=0
    for block in blocks:
        assert len(set(block['players']))==5
        if start>=a-TOL:assert actor not in block['players'], 'incident actor returned after exit'
        for p in block['players']:totals[p]+=block['end_seconds']-start
        start=block['end_seconds']
    assert abs(start-T)<=TOL and set(blocks[0]['players'])==starters
    assert all(abs(totals[p]-n)<=TOL for p,n in v.items())
    return {'actor':actor,'modeled_permanent_exit_seconds':a,'actual_incident_clock_certified':False,
        'causal_contact_reproduced':False,'player_vector_changed':False,'source_chronology_overwritten':False,
        'blocks':blocks,'after_exit_return_count':0}

def validate_early_exit(plan,row,actor):
    """Independently check the constructed order against the retained clock.

    This guard remains outside the constructor: a replacement constructor or
    fresh-hash stored plan cannot turn a later return into a permanent exit.
    """
    v={p:float(n) for p,n in row['player_seconds'].items() if n>0}
    a=v[actor];T=row['game_duration_seconds'];totals=defaultdict(float);start=0.0
    assert plan['actor']==actor and plan['modeled_permanent_exit_seconds']==a
    for k in ['actual_incident_clock_certified','causal_contact_reproduced',
              'player_vector_changed','source_chronology_overwritten']:
        assert plan[k] is False
    assert plan['after_exit_return_count']==0
    assert set(plan['blocks'][0]['players'])==set(row['starters'])
    assert abs(plan['blocks'][0]['end_seconds']-180.0)<=TOL
    for block in plan['blocks']:
        end=block['end_seconds'];people=block['players']
        assert end>start and end-start<=180+TOL
        assert len(people)==len(set(people))==5 and set(people)<=set(v)
        if actor in people:assert end<=a+TOL,'incident actor returned after modeled exit'
        if start<a-TOL:assert actor in people,'continuous initial incident load missing'
        assert not any(start+TOL<t<end-TOL for t in chrono.period_ends(T))
        for p in people:totals[p]+=end-start
        start=end
    assert abs(start-T)<=TOL
    assert set(totals)==set(v) and all(abs(totals[p]-n)<=TOL for p,n in v.items())

def validate_active_nomination(names,current,positive,absent,bench):
    """Check nominal eligibility separately from modeled bench availability."""
    normalized=[roster.norm(p) for p in names]
    assert len(normalized)==len(set(normalized)), 'duplicate active nominee'
    assert 12<=len(names)<=15, 'working active nomination outside 12..15'
    selected=set(normalized)
    assert selected<=set(current), 'unregistered active nominee'
    assert not selected&set(absent), 'selected absent active nominee'
    assert set(positive)|{roster.norm(p) for p in bench}<=selected, 'mandatory bench participant omitted'

def build():
    authority=read(AUTH)
    assert authority['authority_type']=='AUTHOR_DELEGATED_SELECTION'
    assert authority['selected']['health']['route']=='H00'
    assert authority['selected']['regular_season']['route']=='K1_BPM_F038_WITH_APPROVED_F4_F5_C2_OVERRIDES'
    assert 'delegates health, season-result and style recommendations' in (ROOT/'AGENTS.md').read_text(encoding='utf-8-sig')
    registered=read(roster.OUT);assert not roster.validate(registered), 'dated roster bridge stale'
    assert not registered['named_gaps'], 'unresolved named roster path'
    assert registered['summary']['team_games']==2348 and registered['summary']['no_named_membership_or_slot_gap_team_games']==2348
    models=roster.input_models();lookup={key(g):g for g in models}
    regular=read(roster.REG);regular_by={(g['event_id'],g['team']):(i,g) for i,g in enumerate(regular['team_games'])}
    rchrono=read(RCH);chrono.validate(rchrono,regular)
    lchrono=read(LCH);l2chrono.validate(lchrono)
    lplans={(p['event_id'],p['team']):i for i,p in enumerate(lchrono['working_plans'])}
    h=read(H00);assert h==h00builder.build(),'H00 dated source application stale'
    assert h['selected_route']=='H00'
    h00by={(r['event_id'],p['player']):p for r in h['rows'] for p in r['players']}
    six=read(SIX);assert six==sixbuilder.build(),'H00 six-game minute source bridge stale'
    sixby={(r['event_id'],p['player']):p['held_candidate_seconds'] for r in six['rows'] for p in r['focal_loads']}
    incident_keys={('2021-02-14_DEN_LAL','Anthony Davis'):854,('2021-03-20_LAL_ATL','LeBron James'):636}
    assert {k:v for k,v in sixby.items() if k in incident_keys}==incident_keys
    playernames=sorted({p['player'] for s in registered['roster_states'].values() for p in s['players']})
    pid={p:i for i,p in enumerate(playernames)}
    bindings=[];counts=Counter();unknown_cells=0;extra_bench=[];incident_plans=[];hardship=defaultdict(list);h00_checks=[]
    tw_counts=Counter();active_date_owners={};nominal_date_owners={};extra_tw_nominees=[];nomination_sizes=Counter()
    for ri,b in enumerate(registered['team_game_bindings']):
        g=lookup[key(b)];state=registered['roster_states'][b['state_id']]
        current={roster.norm(p['player']):p for p in state['players']}
        positive={roster.norm(p):p for p,n in g['seconds'].items() if n>0}
        assert set(positive)<=set(current)
        absent={roster.norm(p):p for p in g['absent']}
        if g['team']=='LAL' and g['phase']=='REGULAR':
            for actor in ['Anthony Davis','LeBron James']:
                p=h00by[(g['event_id'],actor)]
                if p['mode']=='ABSENT':absent[roster.norm(actor)]=actor
                if p['mode']!='OUTSIDE_H00_SCOPE_HOLD':
                    s=g['seconds'].get(actor,0)
                    if p['mode']=='ABSENT':assert s==0
                    else:assert s==sixby[(g['event_id'],actor)]
                    h00_checks.append({'source_H00_event_id':g['event_id'],'player':actor,'mode':p['mode'],
                        'working_seconds':s,'medical_maximum_seconds':None,'selected_contact_reproduced':False})
        assert not(set(positive)&set(absent)), ('positive/selected absence conflict',key(g))
        # At least eight bench participants are selected, not medically diagnosed.
        # Prefer a standard unused player; no extra TW active game is needed.
        add=[]
        candidates=sorted((p for nk,p in current.items() if nk not in positive and nk not in absent),
            key=lambda p:(p['contract_class']!='STANDARD',p['player']))
        while len(positive)+len(add)<8:
            assert candidates, ('finite extra bench domain missing',key(g))
            p=candidates.pop(0);assert p['contract_class']=='STANDARD', 'avoid invented additional TW active service'
            add.append(p['player'])
        assert len(positive)+len(add)<=15, ('2020 active maximum',key(g))
        mandatory=set(positive)|{roster.norm(p) for p in add}
        nominees=[current[n]['player'] for n in sorted(mandatory)]
        eligible=sorted((p for n,p in current.items() if n not in mandatory and n not in absent),
            key=lambda p:(p['contract_class']!='STANDARD',p['player']))
        while len(nominees)<12:
            assert eligible, ('finite nominal active domain missing',key(g))
            nominees.append(eligible.pop(0)['player'])
        validate_active_nomination(nominees,current,positive,absent,add)
        nomination_sizes[len(nominees)]+=1
        for name in nominees:
            nk=roster.norm(name);datekey=(g['date'],nk)
            assert datekey not in nominal_date_owners, ('nominal active player used twice on one date',datekey)
            nominal_date_owners[datekey]=key(g)
            if current[nk]['contract_class']=='TWO_WAY' and nk not in positive:
                assert g['date']>='2021-03-11', 'new zero-minute TW nomination before rule change'
                extra_tw_nominees.append({'phase':g['phase'],'event_id':g['event_id'],'team':g['team'],
                    'player':name,'working_seconds':0,'actual_medical_status':None,'new_bench_availability_selected':False})
        for nk in set(positive)|{roster.norm(p) for p in add}:
            datekey=(g['date'],nk)
            assert datekey not in active_date_owners,('modeled bench player used twice on one date',datekey)
            active_date_owners[datekey]=key(g)
        unused=set(current)-set(positive)-set(absent)-{roster.norm(p) for p in add}
        counts['registered']+=len(current);counts['positive']+=len(positive);counts['modeled_absent']+=len(set(absent)&set(current))
        unknown_cells+=len(unused)
        if add:extra_bench.append({'phase':g['phase'],'event_id':g['event_id'],'team':g['team'],'players':add,
            'classification':'NEW_DELEGATED_WORKING_BENCH_AVAILABILITY_WITH_ZERO_MINUTES_NOT_DIAGNOSIS',
            'actual_medical_certificate':False,'minute_vector_changed':False})
        for nk in {roster.norm(p) for p in nominees}:
            if current[nk]['contract_class']=='TWO_WAY' and g['phase']=='REGULAR':tw_counts[(g['team'],current[nk]['player'],g['date']<'2021-03-11')]+=1
        if g['phase']=='REGULAR':
            ci,row=regular_by[(g['event_id'],g['team'])];csource=RCH
            for actor in ['Anthony Davis','LeBron James']:
                if g['team']=='LAL' and (g['event_id'],actor) in incident_keys:
                    override=early_exit(row,actor);validate_early_exit(override,row,actor)
                    override.update(event_id=g['event_id'],team='LAL',source_row_index=ci)
                    incident_plans.append(override)
        elif g['phase']=='PLAYIN':ci=lplans[(g['event_id'],g['team'])];csource=LCH
        else:ci=g['pointer'];csource=roster.POST
        bindings.append([ri,ci,csource,[pid[current[n]['player']] for n in sorted(set(absent)&set(current))],[pid[p] for p in add],[pid[p] for p in nominees]])
        for name in b['working_named_hardship_families']:hardship[name].append([g['date'],g['event_id'],g['team']])
    assert len(bindings)==2348 and counts['positive']==25061
    assert Counter(x['mode'] for x in h00_checks)=={'ABSENT':56,'PARTIAL_GAME_EXIT_LOAD_HOLD':2,'RETURN_LOAD_HOLD':4}
    assert len(incident_plans)==2 and len(extra_bench)==6
    assert all(n<=50 for (team,player,pre),n in tw_counts.items() if pre)
    cba=roster.TEMP/roster.RAW['cba2017'][0]
    assert hashlib.sha256(cba.read_bytes()).hexdigest()==roster.RAW['cba2017'][1]
    with fitz.open(cba) as pdf:
        cbatext=pdf[411].get_text();assert 'minimum of eight (8)' in cbatext
        assert 'twelve (12)' in cbatext
    return {'schema':'FINITE_REGISTERED_HEALTH_COACH_EXECUTION_FAMILY_V1',
        'status':'FULL_FINITE_WORKING_FAMILY_SELECTED_INDEPENDENTLY_REVIEWED',
        'source_hash_method':'SHA256_UTF8_BOM_STRIPPED_CRLF_CR_TO_LF','source_sha256':{p:sha(p) for p in INPUTS},
        'authority':'Existing delegated health/season/coach model execution, not real-world medical or active-list certificates.',
        'player_dictionary':playernames,
        'compact_binding_schema':['dated_roster_binding_index','coach_plan_index_or_pointer','coach_source','modeled_absent_player_ids','new_zero_minute_bench_player_ids','working_active_nominee_player_ids'],
        'bindings':bindings,'H00_dated_checks':h00_checks,'new_H00_early_exit_chronology_overrides':incident_plans,
        'new_zero_minute_bench_working_choices':extra_bench,
        'additional_zero_minute_two_way_nominees':extra_tw_nominees,
        'reserve_policy':{'positive_registered_player':'AUTHOR_MODELED_AVAILABLE_FOR_EXACT_PRESERVED_POSITIVE_LOAD',
            'source_selected_absent':'AUTHOR_MODELED_ABSENT_ZERO_PARTICIPATION_PRESERVED',
            'extra_bench_zero':'AUTHOR_MODELED_AVAILABLE_FOR_BENCH_NO_NEW_POSITIVE_MINUTES_NO_DIAGNOSIS',
            'all_other_registered_unused':'COACH_NOT_USED_HEALTH_UNSELECTED',
            'unused_medical_status':None,'actual_active_list_certified':False,'new_injury_diagnoses':0,
            'reserve_illness_inferred_from_zero':False,'formal_minimum_12_active_list_certified':False,
            'working_active_nomination_selected':True,'working_nomination_minimum':12,'working_nomination_maximum':15,
            'nomination_is_medical_or_bench_availability':False},
        'named_hardship_working_families':dict(hardship),
        'hardship_boundary':'Preserve positively reported named hardship implementation families and their registered source domains. Do not infer which unused player is injured, manufacture health certificates, or grant general extra roster capacity.',
        'two_way_regular_working_games':[{'team':t,'player':p,'before_2021_03_11':sum(v for (a,b,c),v in tw_counts.items() if (a,b,c)==(t,p,True)),
            'from_2021_03_11':sum(v for (a,b,c),v in tw_counts.items() if (a,b,c)==(t,p,False))} for t,p in sorted({(t,p) for t,p,z in tw_counts})],
        'public_rule_observations':{
            '2020_active_15':{'url':'https://www.nba.com/news/teams-allowed-to-carry-15-players-on-active-roster-for-2020-21-season',
                'date':'2020-12-18','locator':'direct web body L179','body_read':True,'limited_paraphrase':'The 2020–21 game-night active maximum increased from thirteen to fifteen.',
                'failed_http_status':403,'failed_response_is_body':False,'failed_cache':str(roster.TEMP/'fr-health-family-20261007/NBA_ACTIVE_2020.html'),
                'failed_raw_sha256':'154975b1fa25116d5bae390d0ea0613dacfef4302c3cd02a8bdb6d1b9a925997'},
            '2021_NBA_official_prior_rule_bridge':{'url':'https://pr.nba.com/nba-board-of-governors-play-in-roster-rules-2021-22-season/',
                'date':'2021-07-27','locator':'direct official web body L33/L36','body_read':True,
                'limited_paraphrase':'NBA describes the 2021–22 active-list flexibility as consistent with rules in place before 2020–21. This corroborates the earlier maximum; future two-way rules are not copied backward.',
                'failed_http_status':403,'failed_response_is_body':False,'failed_cache':str(roster.TEMP/'fr-health-family-20261007/NBA_PR_ACTIVE_2021.html'),
                'failed_raw_sha256':'b4d69ee16cc448aa06285c0c2fb43df8ffccdfa48d7e02f700475a1ca96442ea'},
            '2017_bench_minimum':{'url':'https://nbpa.com/cba','pdf_page':412,'printed_page':390,'clause':'XXIX1',
                'raw_sha256':roster.RAW['cba2017'][1],'page_text_sha256':hashlib.sha256(cbatext.encode()).hexdigest(),
                'scope':'Minimum twelve active nominees and eight bench members are separate conditions. Whole-domain working nominations conservatively use twelve to fifteen; the 2017 thirteen maximum is not copied into 2020 and actual active-list filing remains uncertified.'},
            '2021_two_way_change':{'raw_sha256':roster.RAW['tw2021'][1],'source':'Dated roster bridge raw_sources.tw2021',
                'scope':'March11 original reporter: game limit removed and playoff eligibility allowed. Pre-March11 nominated TW active counts are checked <=50; extra zero-minute TW nominations only occur after this change.'}},
        'summary':{'games':1174,'team_games':len(bindings),'teams':30,'registered_player_game_cells':counts['registered'],
            'positive_player_game_cells':counts['positive'],'modeled_absent_registered_cells':counts['modeled_absent'],
            'unused_registered_health_null_cells':unknown_cells,'extra_zero_bench_cells':sum(len(x['players']) for x in extra_bench),
            'new_H00_clock_overrides':2,'preserved_regular_chronology_plans':2158,'preserved_L2_chronology_plans':12,'preserved_playoff_chronology_plans':176,
            'missing_domain_rows':0,'positive_absence_conflicts':0,'same_date_positive_or_new_bench_duplicates':0,
            'working_active_nomination_team_games':len(bindings),'working_active_nomination_size_counts':{str(k):v for k,v in sorted(nomination_sizes.items())},
            'additional_zero_minute_TW_nominee_cells':len(extra_tw_nominees),
            'source_minutes_or_results_changed':0},
        'scope':{'finite_working_registered_availability_and_coach_domain_constructed':True,
            'actual_medical_or_actual_active_registration_certified':False,'all_reserve_health_diagnosed':False,
            'exact_real_injury_contacts_or_incident_clocks_certified':False,'tactical_or_position_appropriateness_certified':False,
            'A1_or_K_HEALTH_promoted_here':False,'independent_review_complete':True,'whole_season_selected':False,
            'manuscript_allowed':False,'design_gate':'CLOSED'}}

def validate(d,expected=None):
    if expected is None:
        try:expected=build()
        except (AssertionError,KeyError,ValueError,OSError) as exc:return ['source construction: '+str(exc)]
    return [] if d==expected else ['saved family differs from full finite source construction']

def render(d):
    s=d['summary']
    return '\n'.join(['# 2020–21 전체 등록 선수의 작업 건강·감독 실행 가족','',
        '기존 위임 범위의 가상 실행 선택 / 독립 검문 완료. 중앙 A1/K_HEALTH·시즌 판정은 별도 원장에서 수행하며 이 leaf 자체의 승격0.','',
        f"1174경기·2348팀·30팀, 등록 선수 {s['registered_player_game_cells']}칸과 양수 {s['positive_player_game_cells']}칸을 기존 명단/분/순서에 연결한다. 분·승패는 변경하지 않는다.",
        f"선택된 결장 {s['modeled_absent_registered_cells']}칸을 보존한다. 나머지 예비 {s['unused_registered_health_null_cells']}칸은 감독 미사용/건강 null이다. 의료 진단으로 채우지 않는다.",
        '## 유한 추가 실행','',
        '- 정규시즌 7명만 출전한 6개 팀 경기에는 해당 날짜 등록 명단의 제로분 표준계약 예비 한 명을 별도 작업 벤치 가용 모델로 선택한다. 이는 양수 참가나 현실 의료 허가를 추가하지 않는다.',
        '- H00의 Davis 2/14(854초), LeBron 3/20(636초)는 기존 일반 작업 순서에서 경기 뒤쪽에 재등장했다. 새 두 순서만 별도 leaf에 만들어 원 선발 180초·모든 선수 초를 유지하고 모델의 영구 이탈 뒤 재등장을 막는다. 실제 사고 시각·접촉·의료 한계는 미인증이다. 기존 107 원증인/2160 원 작업 순서는 덮어쓰지 않는다.',
        '- H00 부재56·부분 이탈2·복귀부하4를 날짜별로 대조하며, L2/플레이오프의 사전 결장·회복 모델도 그대로 연결한다. 전체 가족은 원자료 관측 의료 사실이 아니다.',
        '- 상위 작업 시계의 새 active15 보정4행을 그대로 연결한다. 앞선 25,065 양수칸은 보정 전 이력이며 현행 25,061칸이다. 이전 16명인 행을 건강 표시로 허용하거나 제로분 선수를 새 부상자로 바꾸지 않는다.',
        '- MEM/CLE/HOU/WAS의 긍정 보도로 지원된 명명 hardship 작업 가족은 해당 날짜·선수 범위를 보존한다. 제로분의 병명·미공표 모든 부상·현실 승인서를 새 필수 조건으로 만들지 않는다.','',
        '## 법규·사실 범위','',
        '[NBA 2020-12-18](https://www.nba.com/news/teams-allowed-to-carry-15-players-on-active-roster-for-2020-21-season)의 게임일 active 상한은 15명이다. [NBA 공식 2021-07-27](https://pr.nba.com/nba-board-of-governors-play-in-roster-rules-2021-22-season/)의 이전 규칙 연결은 보조 근거로만 사용한다. 두 페이지는 web 원본문을 읽었고 별도 다운로드403은 원본문으로 표시하지 않는다.',
        '- CBA XXIX1 PDF412의 active 최소12와 벤치 최소8을 별도로 검문한다. 전 2348팀 경기에 양수 참가자·추가 벤치6칸을 필수로 포함하고, 등록된 비결장 제로분 표준계약부터 보충한 12–15명 작업 명단을 선택한다. 명목 active 제로분은 임상 가용이나 추가 벤치 가용을 뜻하지 않으며 건강 null을 유지한다. 2017의 상한13을 2020에 복사하지 않고 실제 리그 명단 접수도 인증하지 않는다.',
        f"- 표준계약만으로 12명이 안 되는 {d['summary']['additional_zero_minute_TW_nominee_cells']}칸은 March11 이후 등록 TW 제로분 명목 후보로 채운다. March11 이전 TW 명목 active게임≤50을 전부 검사하고, 이후 기존 원보도의 한도 제거/플레이오프 허용을 연결한다. 새 출전분·승패·의료 진단은 0이다.",
        '- source SHA는 BOM 제거·LF 정규화이며 NBA/원PDF raw SHA와 구분한다. 큰 분·감독 JSON은 복제하지 않고 행 인덱스/포인터로 참조한다. 원고·최종시즌·실제의료·리그 접수는 false다.',''])

def self_test(d):
    cases=[('diagnose_unused',lambda x:x['reserve_policy'].update(unused_medical_status='INJURED')),
        ('medical_certificate',lambda x:x['scope'].update(actual_medical_or_actual_active_registration_certified=True)),
        ('missing_teamgame',lambda x:x['bindings'].pop()),
        ('drop_known_absence',lambda x:next(b for b in x['bindings'] if b[3]).__setitem__(3,[])),
        ('late_incident_return',lambda x:x['new_H00_early_exit_chronology_overrides'][0]['blocks'][-1]['players'].__setitem__(0,'Anthony Davis')),
        ('H00_future_healed',lambda x:x['H00_dated_checks'][0].update(medical_maximum_seconds=2880)),
        ('whole_gate',lambda x:x['scope'].update(A1_or_K_HEALTH_promoted_here=True))]
    for label,f in cases:
        altered=deepcopy(d);f(altered);assert validate(altered,expected=d),label
    regular=read(roster.REG)
    for p in d['new_H00_early_exit_chronology_overrides']:
        row=regular['team_games'][p['source_row_index']]
        bad=deepcopy(p);bad['blocks'][-1]['players'][0]=p['actor']
        try:validate_early_exit(bad,row,p['actor'])
        except AssertionError:pass
        else:raise AssertionError('Permanent exit constructor guard permits late return')
    current={'a':{'player':'A'}, **{str(i):{'player':str(i)} for i in range(11)}}
    valid=['A']+[str(i) for i in range(11)]
    validate_active_nomination(valid,current,{'a':'A'},{},[])
    for label,names,absent in [('short',valid[:-1],{}),('duplicate',valid[:-1]+['A'],{}),
                              ('absent',valid,{'a':'A'}),('unregistered',valid[:-1]+['Z'],{})]:
        try:validate_active_nomination(names,current,{'a':'A'},absent,[])
        except AssertionError:pass
        else:raise AssertionError('active nomination guard permits '+label)
    return len(cases)+6

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args()
    d=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(render(d),encoding='utf-8')
    errors=[]
    if a.check:
        if read(OUT)!=d:errors.append('JSON stale')
        if (ROOT/MD).read_text(encoding='utf-8-sig')!=render(d):errors.append('MD stale')
    print(json.dumps({'current':not errors,'errors':errors,'summary':d['summary'],'negative_controls':self_test(d) if a.self_test else 0},ensure_ascii=False))
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
