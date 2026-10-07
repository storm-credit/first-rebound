"""Finite conditional date/roster/minute carrier; no82-game health execution."""
import argparse
import copy
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
from unittest.mock import patch
import fitz

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2021_22_m1_dated_working_minutes.py'
OUT='simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json'
MD=OUT[:-5]+'.md'
BASELINE='16167cf4f6f2da50cbb1c054b948f9efedee3ddc'
MAP='design/CHICAGO_2021_22_FINITE_IMPLEMENTATION_MAP_2026_10_07.json'
M1='simulation/CHICAGO_2021_M1_ROLE_WITNESS.json'
ROLE='simulation/CHICAGO_2021_22_ROLE_PLAN_INPUTS.json'
SUMMER='simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json'
COST='research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json'
CAL='simulation/CHICAGO_2021_22_CALENDAR.csv'
LEAGUE='simulation/NBA_2021_22_REGULAR_BASELINE.csv'
PINS={'design/CHICAGO_2021_22_FINITE_IMPLEMENTATION_MAP_2026_10_07.json': 'bd8c28ac0c2bd461a7b29932d0e6f33a0c8220ec9a0d4a109079ac9e188b4429', 'simulation/CHICAGO_2021_M1_ROLE_WITNESS.json': '26b73b6ba0a87449f60774fa3a631374679e0fd5bc6547e5bbecf013232ddf0c', 'simulation/CHICAGO_2021_22_ROLE_PLAN_INPUTS.json': '0b8f9e4ac212596d0966f82f7f8317f7a7c86645a239a5a73587dd121f77e171', 'simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json': '11140e49baa665f18e267fa6419efa238302250b724fa51cfd3262b010b4a312', 'research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json': '7244beff7a120c5ca246a04e72b61586f3cfbe245487d5fc6479f5245fd78d9f', 'simulation/CHICAGO_2021_22_CALENDAR.csv': 'c59ea19a5515d64ed03cae8e0481847b6572d4087bbcefef15896bb7a2489183', 'simulation/NBA_2021_22_REGULAR_BASELINE.csv': '92869bc987896a4172c5e54e3684d2604c5c24d828e9bcf3cc27af30ebc83644', 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json': '253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088', 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json': '9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce', 'research/O15G15AY_CHICAGO_2021_TWO_WAY_SLOT_SCREEN.md': '8362115d2a18b27cabaf725728903b010b6a05535768d9e43c1653e0f5a7d020', 'research/TWO_WAY_2021_22_RULE_PERIOD_EVIDENCE.json': 'e615d2cce356be8db1b0e65eb174b718789a4650a459c1ec2f69118be1cb1e26', 'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2'}
CBA=Path(r'C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
EXPECTED_STD=['LaVine','LaMelo_pick4','Coby','Carter','Young','Satoransky','Protagonist','Chris Duarte','Green','Caruso','Markkanen','Joe Wieskamp','Tony Bradley','Stanley Johnson','Denzel Valentine']
EXPECTED_TW=['Devon Dotson','Tyler Cook']
EXPECTED_POS={'PG':{'LaMelo_pick4':32,'Coby':10,'Caruso':6},'SG':{'LaVine':34,'Coby':8,'Caruso':6},'SF':{'Protagonist':28,'Caruso':6,'Chris Duarte':14},'PF':{'Markkanen':32,'Protagonist':4,'Young':12},'C':{'Carter':28,'Young':8,'Tony Bradley':12}}

def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def rows(p):return list(csv.DictReader(io.StringIO(text(p))))

def policy():
    return {'dates':'SAME_OBSERVED_DATE_ROUTINE_SCHEDULE_HYPOTHESIS_NOT_ACTUAL_ADOPTION',
        'contract_path':'PRESERVE_REVIEWED_SQ1_15STD2TW_THROUGH_EACH_DATE_CONDITIONALLY; NEW_MOVES_REOPEN',
        'states':['NORMAL','COBY_OUT'],'state_for_each_date_selected':None,
        'regulation_minutes':48,'historical_OT_inherited':False,'OT_extension_selected':False,
        'normal_role':'M1_MARK32_CARUSO18_P32_NOT_OLD_R21A28_22',
        'active_nominee_count':12,'legal_nomination_size_domain':[12,15],
        'TW_active_nominees_in_this_conditional_family':0,'TW_season_active_count':0,
        'zero_minute_reserve_clinical_status':None,'actual_future_health_or_results_selected':False,
        'actual_contract_receipt_or_active_list_certified':False,'AP1_SG16_direction_selected':False,
        'whole2021_22_execution_or_macro3_closed':False,'new_author_lock':False}
FIXED_POLICY=copy.deepcopy(policy())

def checked_policy():
    p=policy();assert p==FIXED_POLICY,'Schedule/state/nomination/OT/authority policy changed';return p

def source_inputs():
    for p,h in PINS.items():assert sha(p)==h,'Unreviewed source '+p
    mp=load(MAP)
    for p,h in mp['source_sha256'].items():assert sha(p)==h,'Map source stale '+p
    old=load(ROLE);m=load(M1);summer=load(SUMMER);cost=load(COST)
    assert summer['normal_day_role_reference']['position_minutes']==m['position_minutes']==EXPECTED_POS,'M1 normal role transport'
    assert load('canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json')['selected']['normal_availability_pf_minutes_candidate']==32
    assert load('canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json')['selected']['route']=='G1A_PLUS_M1'
    std=[x['player']for x in summer['standard_roster_working']];tw=[x['player']for x in summer['two_way_working']]
    assert std==EXPECTED_STD and tw==EXPECTED_TW and len(set(std+tw))==17,'Reviewed contract identity/class'
    assert all(x['type']=='TWO_WAY' and x['regular_active_game_limit']==50 for x in summer['two_way_working'])
    assert cost['whole_source_supported_cost_family_pass'] is True and cost['independent_review_completed'] is True
    assert cost['summary']['complete_apron_upper']==128914775,'Opening cost family changed'
    assert m['elapsed_minutes']==48 and m['team_minutes']==240 and m['actual_minutes_selected']is False
    assert len(m['lineup_witness'])==11,'M1 witness binding'
    cal=rows(CAL);league=rows(LEAGUE);li={x['game_id']:x for x in league}
    assert len(cal)==82 and len(li)==1230 and len({x['game_id']for x in cal})==82
    assert sum(x['home']=='CHI'for x in cal)==sum(x['away']=='CHI'for x in cal)==41
    for x in cal:
        assert all(x[k]==li[x['game_id']][k]for k in ['date','home','away']),'Date/team key differs from baseline'
        assert x['alternate_date']=='HOLD' and x['alternate_result']=='HOLD','Historical calendar silently adopted'
    assert {(x['game_id'],x['historical_observed_date'],x['home'],x['away'])for x in mp['Chicago_date_keys']}=={(x['game_id'],x['date'],x['home'],x['away'])for x in cal}
    return cal,m,old['position_eligibility_design_only'],std,tw

def cba_rule():
    assert hashlib.sha256(CBA.read_bytes()).hexdigest()==CBA_SHA
    with fitz.open(CBA) as d:t=d[411].get_text().replace('\r\n','\n').replace('\r','\n')
    plain=' '.join(t.split());assert 'twelve (12) or thirteen (13)' in plain and 'minimum of eight (8)'in plain and 'at least two (2)'in plain
    return {'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(CBA),'raw_sha256':CBA_SHA,'PDF_1based':412,'printed':390,'fitz_text_LF_sha256':hashlib.sha256(t.encode()).hexdigest(),
        'scope':'XXIX1/2: twelve active satisfies baseline active minimum; fifteenSTD minus twelve active leaves three standard inactive, at leasttwo. TW remain Two-Way Roster, neither Active nor Inactive here.',
        'opening2021_rule_source':'https://pr.nba.com/nba-board-of-governors-play-in-roster-rules-2021-22-season/',
        '2021_rule_source_family':'Reviewed SQ1 public rule observations; STD15/TW2/active maximum15 and initialTW50. LaterCOVID50+ exceptions not required because this carrier uses TWactive0.',
        'later_50plus_exception_exact_date_or_salary_not_certified':True}

def expected_positions(state):
    assert state in ('NORMAL','COBY_OUT');p=copy.deepcopy(EXPECTED_POS)
    if state=='COBY_OUT':
        p['PG']['Satoransky']=p['PG'].pop('Coby');p['SG']['Denzel Valentine']=p['SG'].pop('Coby')
    return p

def blocks_for(m,state):
    assert state in ('NORMAL','COBY_OUT');bs=copy.deepcopy(m['lineup_witness'])
    if state=='COBY_OUT':
        for b in bs:
            for pos,name in b['positions'].items():
                if name=='Coby':
                    assert pos in ('PG','SG');b['positions'][pos]='Satoransky'if pos=='PG'else'Denzel Valentine'
    return bs

def assert_row(x,g,state,m,eligibility,std,tw):
    assert x['game_id']==g['game_id'] and x['candidate_date']==g['date'] and x['home']==g['home'] and x['away']==g['away'] and x['team']=='CHI'
    assert x['game_number']==int(g['game_number']), 'Source game ordinal changed'
    assert x['historical_observed_OT_diagnostic']==int(g['inferred_historical_ot']), 'Source OT diagnostic moved between dates'
    assert x['state']==state and x['state_selected_for_date']is False and x['contract_holding_condition_met_is_hypothesis']is True
    assert x['standard_registered_candidate']==std and x['two_way_registered_candidate']==tw
    assert x['position_minutes']==expected_positions(state),'Wrong state position budget'
    bs=x['unordered_regulation_blocks'];assert bs==blocks_for(m,state),'Source witness order/content changed'
    actual={p:Counter()for p in EXPECTED_POS};players=Counter()
    assert len(bs)==11 and sum(b['minutes']for b in bs)==48
    for b in bs:
        assert isinstance(b['minutes'],int)and b['minutes']>0 and set(b['positions'])==set(EXPECTED_POS)
        assert len(set(b['positions'].values()))==5 and set(b['positions'].values())&{'LaMelo_pick4','LaVine'}
        for p,n in b['positions'].items():assert n in std and n in eligibility[p];actual[p][n]+=b['minutes'];players[n]+=b['minutes']
    assert all(dict(actual[p])==x['position_minutes'][p]and sum(actual[p].values())==48 for p in actual)
    assert x['player_minutes']==dict(sorted(players.items()))and sum(players.values())==240
    assert players['Markkanen']==32 and players['Caruso']==18 and players['Protagonist']==32
    positive=set(players);absent=set(x['conditional_unavailable']);assert absent==({'Coby'}if state=='COBY_OUT'else set())
    assert positive<=set(std) and not positive&absent
    nom=x['working_active_nominees'];assert len(nom)==len(set(nom))==12 and set(nom)<=set(std)and positive<=set(nom)and not set(nom)&absent
    assert x['working_available_for_nomination']==nom,'Candidate availability must bind actual nominees, not a medical assertion'
    assert x['zero_minute_active_nominees']==[n for n in nom if n not in positive]
    assert x['standard_inactive_nominees']==[n for n in std if n not in nom]and len(x['standard_inactive_nominees'])==3
    assert x['TW_active_nominees']==[] and x['TW_neither_active_nor_inactive']==tw
    assert x['positive_minute_availability_condition']==sorted(positive)and x['unused_reserve_clinical_status']is None
    assert x['regulation_elapsed_minutes']==48 and x['regulation_team_minutes']==240 and x['substitution_order_selected']is False
    assert x['overtime_extension']=={'selected':False,'periods':None,'minutes':None,'requires_new_5player_clock_and_available_nominees':True,'historical_OT_automatically_inherited':False}
    assert x['result']is None and x['actual_medical_registration_or_active_list_certified']is False

def construct(g,state,m,eligibility,std,tw):
    """Callable conditional carrier for ONE date/state, never a selected health event."""
    assert state in ('NORMAL','COBY_OUT');bs=blocks_for(m,state);counts=Counter()
    for b in bs:
        for n in b['positions'].values():counts[n]+=b['minutes']
    pos=set(counts);absent={'Coby'}if state=='COBY_OUT'else set()
    nominees=[n for n in std if n in pos]
    nominees += [n for n in std if n not in pos and n not in absent][:12-len(nominees)]
    x={'game_id':g['game_id'],'game_number':int(g['game_number']),'candidate_date':g['date'],'home':g['home'],'away':g['away'],'team':'CHI','state':state,'state_selected_for_date':False,
        'contract_holding_condition_met_is_hypothesis':True,'standard_registered_candidate':std,'two_way_registered_candidate':tw,
        'conditional_unavailable':sorted(absent),'positive_minute_availability_condition':sorted(pos),'working_available_for_nomination':nominees,
        'working_active_nominees':nominees,'zero_minute_active_nominees':[n for n in nominees if n not in pos],'standard_inactive_nominees':[n for n in std if n not in nominees],
        'TW_active_nominees':[],'TW_neither_active_nor_inactive':tw,'unused_reserve_clinical_status':None,
        'position_minutes':expected_positions(state),'player_minutes':dict(sorted(counts.items())),'unordered_regulation_blocks':bs,
        'regulation_elapsed_minutes':48,'regulation_team_minutes':240,'substitution_order_selected':False,
        'historical_observed_OT_diagnostic':int(g['inferred_historical_ot']),
        'overtime_extension':{'selected':False,'periods':None,'minutes':None,'requires_new_5player_clock_and_available_nominees':True,'historical_OT_automatically_inherited':False},
        'result':None,'actual_medical_registration_or_active_list_certified':False}
    assert_row(x,g,state,m,eligibility,std,tw);return x

def build():
    p=checked_policy();cal,m,eligibility,std,tw=source_inputs();rule=cba_rule()
    built=[construct(g,state,m,eligibility,std,tw)for g in cal for state in p['states']]
    for x,(g,state) in zip(built,((g,state)for g in cal for state in p['states'])):
        assert_row(x,g,state,m,eligibility,std,tw)
    assert len(built)==164 and len({(x['game_id'],x['state'])for x in built})==164
    assert sum(bool(x['historical_observed_OT_diagnostic'])for x in built)==2*sum(bool(int(g['inferred_historical_ot']))for g in cal)
    return {'id':'CHICAGO_2021_22_M1_DATED_WORKING_MINUTES','status':'INDEPENDENTLY_REVIEWED_CONDITIONAL_82DATE_TWO_STATE_REGULATION_CARRIER','source_main_snapshot':BASELINE,
        'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8 BOM stripped; CRLF/CR toLF','policy':p,'active_rule_source':rule,
        'quantifier':'For each observed game key, if retained SQ1 contract identities and the chosen state availability/nomination conditions hold, this regulation minute witness exists. No state assignment across82dates is selected.',
        'availability_domain':'NORMAL: every positive performer and named active filler available operationally. COBY_OUT: Coby unavailable for this candidate; all positive recipients and named active filler available. Unused reserves clinicalnull. Other/combined absences reopen this restricted carrier.',
        'registration_domain':'15STD+2TW retained only under no-new-move hypothesis; no automatic transfer of raw counterpart signing/waiver. This carrier chooses12STANDARD active and3STANDARD inactive per hypothetical row; bothTW remain Two-Way Roster. Greater active sizes in12..15 legal size domain are not all separately nominated here.',
        'OT_scope':'Only regulation48/240. Historical OT diagnostics remain explicit comparison metadata. Wholegame minutes require an explicit OT choice/extension or an explicitly adopted no-OT model, neither selected here.',
        'opening_family_source':COST,'opening_source_supported_apron_upper_usd':128914775,
        'summary':{'date_keys':82,'conditional_states_per_date':2,'rows':164,'unordered_blocks':1804,'hypothetical_player_block_cells':9020,'STD_slots':15,'TW_slots':2,'working_active_each_row':12,'working_STD_inactive_each_row':3,'positive_players_NORMAL':10,'positive_players_COBY_OUT':11,'historical_OT_game_keys':sum(bool(int(g['inferred_historical_ot']))for g in cal),'TW_active_count_per_any_82state_assignment_from_this_carrier':0,'executed_date_state_choices':0,'actual_new_game_results':0},
        'rows':built,'remaining_named_inputs':['Choose an actual dated working availability/state assignment under delegation; no clinical/private receipt gate.','Different absences require explicit named donor/recipient/nomination witnesses, not automatic NORMAL copy.','New in-season roster moves require lawful dated source family and costs.','Pair82 opponents with their changing-team deltas before productivity/result evaluation.','Select/adopt wholegame regulation/OT scope explicitly; observed overtime is not copied.','2021-22 scoring/impact method/results and #16important directions remain separate.'],
        'certification':{'independent_review_completed':True,'actual_health_or_active_list':False,'all82_dates_executed':False,'whole_game_OT_scope_complete':False,'whole2021_22_or_macro3_complete':False,'new_author_lock':False,'central_or_REGISTER_promotion':False,'manuscript_written':0}}

def validate(o):
    try:assert o==build(),'Saved carrier differs from source-bound reconstruction';return []
    except (AssertionError,KeyError,ValueError,OSError)as e:return[str(e)]

def markdown(o):
    return '\n'.join(['# Chicago2021–22 M1: 82날짜·두 상태 조건부 분 carrier','',o['status'],'',
        '82개 관측 game_id/date/home/away에 NORMAL과 COBY_OUT을 실제로 구성했다.164행·1,804개 순서없는5인 블록·9,020개 선수블록 셀이다. 날짜별 상태 선택0이며82경기를 모두 건강/출전/승패 확정한 원장은 아니다.',
        '', '## 실제 구성한 분과 명단','',
        '두 상태 모두 Markkanen32·Caruso18·주인공32, 포지션마다48분, 정규48분/240팀분,11블록/5명 중복0·LaMelo 또는LaVine 창조자 조건을 만족한다. NORMAL양수10명; COBY_OUT양수11명이며 Coby PG10→Satoransky10/SG8→Valentine8을 적용한다. 기존R21A28/22와 다른 M1이다.',
        '각 행은 reviewed SQ1의15STD·2TW를 유지하는 조건 아래 양수 전원과 std-first0분 수신자를12명 active로 구성하고 나머지3STD inactive를 명시했다. NORMAL0분 active2명, COBY_OUT0분 active1명이다. 최소12/최대15 size-domain 중 실제 구성은12명이다. 남은0분 임상상태는 null이며 inactive는 운영 분류, 부상 진단이 아니다.',
        'Coby-out은 Coby를 그 후보의 active/양수에서 제외하는 조건이다. 다른 복합 결장은 처리하지 않았다. active filler의 가용성은 admitted운영조건이고 실제 의학 사실이 아니다. TW2는 별도 Two-Way Roster에 남고 active/inactive에 넣지 않아 어느82상태 조합에도 TWactive0이다. 개막50제약 및 나중50초과 예외의 미확인 발효시점에 기대지 않는다.',
        '', '## 날짜·시간 경계','',
        '같은 관측 날짜를 쓰는 것은 routine schedule **가설**이다. 원일정의 감염·연기·접촉 사건을 복사하지 않는다. 기존원자료 재수집0, historical대체승패0. 원M1 FREEZE의 옛 SHA를 다시쓰지 않고 현행 승인32/18·실제position/5인 의미를 직접 대조한다.',
        f"역사적OT 진단이 있는 날짜{o['summary']['historical_OT_game_keys']}개를 각 행에 보존했다. 본 증인은 regulation-only이다. 역사적OT를 새OT로 승격하지 않으며 새OT가 없었다고도 선택하지 않는다. 전체경기 분을 완료하려면 명시적 no-OT 모델 혹은 새OT5인/가용성/clock 연장 증인이 필요하다.",
        '', '## 원천과 재현','',
        '[2017CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) PDF412/printed390 XXIX1–3 직접본문·raw/textSHA, reviewed [NBA2021로스터 규칙](https://pr.nba.com/nba-board-of-governors-play-in-roster-rules-2021-22-season/) 입력을 연결했다. 기본12active와3STDinactive를 실제 검사하며 실제리그접수 인증을 요구하거나 주장하지 않는다.',
        '`python -B tools/build_chicago_2021_22_m1_dated_working_minutes.py --check --self-test`. source지문·map31핀·normalM1 고정예산·날짜/회원/5인/수신자/active/OT/권위 변조를 거부한다. 자기통제는 독립검문으로 세지 않는다.',
        '다음은 날짜별 상태 선택/다른 결장, 상대82명의 dated roster+minute 쌍과 생산성/impact 방법의 조인이다. 여기서 결과·우승·2022계약·AP1/SG16을 선택하지 않았다.',
        '', '[입력지도](../design/CHICAGO_2021_22_FINITE_IMPLEMENTATION_MAP_2026_10_07.md) · [현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md) · [누적 기능 등록기](../control/G13_FINAL_FUNCTION_REGISTER.md)','',
        '|번호|묶음|상태|','|---|---|---|','|1|2020드래프트 연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23거래·계약|M1 날짜별 두 상태 carrier 완료; 실제 날짜별 모델/양팀/결과 미선택|','|4|장기 커리어|후속시즌 입력 대기|','|5|결말·전체 구조|전체기능표 미완료|','|6|집필규격·Context Pack|현행 누적등록기 참조·Pack0|','|7|통합·독립·작가 승인|최종CLOSED|','',
        '미완료 큰 묶음5. v0.30 PARTIAL / 설계·원고CLOSED / 원고0.',''])

def self_test():
    o=build();t=[]
    for name,fn in [('removed_Coby_positive',lambda x:x['rows'][1]['player_minutes'].update(Coby=18)),('oldR21A28_22',lambda x:x['rows'][0]['player_minutes'].update(Markkanen=28,Caruso=22)),('active_absent_donor',lambda x:x['rows'][1]['working_active_nominees'].__setitem__(0,'Coby')),('duplicate5player',lambda x:x['rows'][0]['unordered_regulation_blocks'][0]['positions'].update(SG='LaMelo_pick4')),('wrong_date_sameID',lambda x:x['rows'][0].update(candidate_date='2021-10-21')),('TW_STD_reclassification',lambda x:x['rows'][0]['standard_registered_candidate'].append('Tyler Cook')),('historical_OT_inherited',lambda x:x['rows'][0]['overtime_extension'].update(historical_OT_automatically_inherited=True)),('82health_selected',lambda x:x['certification'].update(all82_dates_executed=True))]:
        b=copy.deepcopy(o);fn(b);assert validate(b),name;t.append(name)
    cal,m,e,s,tw=source_inputs();g=cal[0]
    real=blocks_for;b=blocks_for(m,'COBY_OUT');b[0]['positions']['PF']='Coby'
    with patch(__name__+'.blocks_for',return_value=b):
        try:construct(g,'COBY_OUT',m,e,s,tw)
        except AssertionError:t.append('constructor_absent_into5man')
        else:raise AssertionError('Accepted absent donor')
    p=policy();p['active_nominee_count']=11
    with patch(__name__+'.policy',return_value=p):
        try:build()
        except AssertionError:t.append('constructor_under12_nomination')
        else:raise AssertionError('Accepted min11')
    real_load=load;bad=copy.deepcopy(load(M1));bad['position_minutes']['PF']['Markkanen']=28
    with patch(__name__+'.load',side_effect=lambda p:copy.deepcopy(bad)if p==M1 else real_load(p)):
        try:build()
        except AssertionError:t.append('sameID_source_wrong_M1_role')
        else:raise AssertionError('Accepted source oldrole')
    real_construct=construct
    def swapped_diagnostic(g,state,m,e,s,tw):
        x=real_construct(g,state,m,e,s,tw)
        if g['game_id']=='0022100430':x['historical_observed_OT_diagnostic']=0
        if g['game_id']=='0022100004':x['historical_observed_OT_diagnostic']=1
        return x
    with patch(__name__+'.construct',side_effect=swapped_diagnostic):
        try:build()
        except AssertionError:t.append('constructor_OT_dates_swapped_same_total')
        else:raise AssertionError('Accepted same-total OT date swap')
    return t

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();o=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
    if a.check:assert not validate(load(OUT));assert text(MD)==markdown(o),'Markdown stale'
    print(json.dumps({'current':True,'summary':o['summary'],'negative_controls':self_test()if a.self_test else[]},ensure_ascii=False))
if __name__=='__main__':main()
