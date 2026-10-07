"""Consume two admitted paired clocks into selected fictional BPM winner models.

No future season BPM, actual box score, overtime or whole-season result is
created. The legacy shrinkage and seconds/2880 form are reused, while the
absolute lineup/additive home model and fictional productivity are explicit
working selections rather than a calibrated score prediction.
"""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
import csv
from datetime import date, timedelta
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
from statistics import median
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_chicago_detroit_2021_two_date_selected_bpm_results.py'
OUT = 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS.json'
MD = OUT.replace('.json', '.md')
BASELINE = '15e0e1f2edcc9862b096cc190b752aecbe3aca31'
ROLE = 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_WORKING_EXECUTION.json'
ADOPTION = 'simulation/DET_TWO_DATE_ROLE_ADOPTION_2026_10_07.json'
ECON_SELECTION = 'simulation/DET_ROUTINE_OPERATING_FAMILY_SELECTION_2026_10_07.json'
ECON = 'research/DETROIT_2021_A_ROUTINE_OPERATING_EXECUTION_FAMILY_2026_10_07.json'
HEALTH_AUTH = 'canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json'
HEALTH = 'simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json'
CAL = 'simulation/CHICAGO_2021_22_CALENDAR.csv'
LEAGUE = 'simulation/NBA_2021_22_REGULAR_BASELINE.csv'
BPM = 'simulation/CHICAGO_2020_21_BPM_MAR25_SNAPSHOT.csv'
PRIOR = 'simulation/CHICAGO_2020_21_PREDEADLINE_IMPACT_PRIORS.csv'
GROWTH = 'simulation/CHICAGO_2021_22_GROWTH_INPUTS.json'
GROWTH_DERIVED = 'simulation/CHICAGO_2021_22_GROWTH_CANDIDATES.json'
DELEGATION = 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
SCOPE = 'control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md'
LEGACY_FORM = 'tools/crosscheck_chicago_2020_21_impact.py'
PINS = {
 ROLE:'fc44fe1b28318c2004529fc68a3b3d6b090f9b3a100265ca5e9517c0da3676b3',
 ADOPTION:'8accb225b9414266cb3c7303643a85cae99751495d4d22933e675d15106a6c7e',
 ECON_SELECTION:'9f9c307f33975de3b3c05734e41f8401cad0439f0446f7bc87aa21d8c7752dc2',
 ECON:'855371610d0f2b776b773bdf2ff02f27a43684b6c1407b1d54f698c6e0f093ef',
 HEALTH_AUTH:'51b24c8a6bc1eb703568adced46b3ffa15845e85e8da10da1242bddf941df960',
 HEALTH:'274a35e163c7f6fd7f0d3e5494b3c46753aaf9900036676be935f17a9d538c32',
 CAL:'c59ea19a5515d64ed03cae8e0481847b6572d4087bbcefef15896bb7a2489183',
 LEAGUE:'92869bc987896a4172c5e54e3684d2604c5c24d828e9bcf3cc27af30ebc83644',
 BPM:'1d1455f7f4ddd73ef46e3ce16752b558c392ed2d284434acd295ca6659e937ef',
 PRIOR:'0c5680d6d9ff4f3b38ab157697b2f625c96b8a751fbe0bcb28bb153b4c763dfa',
 GROWTH:'f961daae39a7dc6083ab20439edf7efed7a8cab9930eacc98854c2ad5416c5c3',
 GROWTH_DERIVED:'e51bd8eac3cfa9446c4e67787b836b3e184ce306b766636045249184d9682822',
 DELEGATION:'4ee9b74e37903a43b0bd50b35c7f24cbabdac13728097a848b553f874bbeef80',
 SCOPE:'91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d',
 LEGACY_FORM:'59f99be94ffeaef9854f586b1516fe79f106eb6aa4487947fdee3d8068485819',
}
IDS = ('0022100004', '0022100030')
ALIAS = {'LaVine':'Zach LaVine', 'LaMelo_pick4':'LaMelo Ball',
 'Carter':'Wendell Carter Jr.', 'Caruso':'Alex Caruso', 'Markkanen':'Lauri Markkanen',
 'Satoransky':'Tomas Satoransky', 'Young':'Thaddeus Young'}
COMPARATORS = ('Devin Vassell','Aaron Nesmith','Josh Green','Saddiq Bey','Desmond Bane')
FIXED_POLICY = {'method':'BPM_MAR25_EB', 'shrinkage_minutes':1000,
 'denominator_seconds':2880, 'selected_growth_pair':['P21A','D21A'],
 'protagonist_prior_BASE':-1.2, 'protagonist_working_growth_increment':0.7,
 'protagonist_selected_effective_rating':-0.5,
 'rookie_prior_rule':'MEDIAN_FIVE_EXISTING_PREOPENING_ROOKIE_COMPARATORS',
 'home_effect_per100_working':2.0, 'back_to_back_penalty_per100_working':0.5,
 'interaction_adjustment_working':0.0, 'overtime_used':False,
 'historical_scores_used_in_calculation':False, 'whole_season_selected':False}
POLICY_SHA = 'b60e01189b657201552cc59e3c5b3ac354990c4914ad9f958fc9938c56391459'

def require(ok, message):
    if not ok: raise ValueError(message)

def normalized(path):
    return path.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')

def sha(path):
    return hashlib.sha256(normalized(path).encode()).hexdigest()

def load(root, path):
    text = normalized(root/path)
    return json.loads(text) if path.endswith('.json') else list(csv.DictReader(io.StringIO(text))) if path.endswith('.csv') else text

def sources(root):
    out = {}
    for path, pin in PINS.items():
        require(sha(root/path)==pin, 'Source changed: '+path)
        obj = load(root,path)
        text = normalized(root/path)
        physical = json.loads(text) if path.endswith('.json') else list(csv.DictReader(io.StringIO(text))) if path.endswith('.csv') else text
        require(obj==physical, 'Physical source loader substitution: '+path)
        out[path] = obj
    require(out[ADOPTION]['selected_role']=='A_garza_two_way_retained' and out[ADOPTION]['selected_game_ids']==list(IDS), 'Role adoption changed')
    require(out[ECON_SELECTION]['accepted_game_ids']==list(IDS) and out[ECON_SELECTION]['status'].startswith('SELECTED_AND_'), 'Economic family not selected')
    require(out[HEALTH_AUTH]['selected']['selected_date_rows']['sha256']==PINS[HEALTH], 'Selected health source bridge changed')
    require(out[DELEGATION]['authority_type']=='AUTHOR_DELEGATED_SELECTION', 'Result authority changed')
    require(out[GROWTH]['recommended_pair']==['P21A','D21A'] and out[GROWTH_DERIVED]['recommended_pair']==['P21A','D21A'], 'Growth recommendation changed')
    prior = [x for x in out[PRIOR] if x['proxy']=='BPM' and x['scenario']=='BASE']
    require(len(prior)==1 and float(prior[0]['protagonist_rating'])==-1.2, 'Existing fictional protagonist BASE changed')
    return out

def assert_consumed_sources(src, root):
    # Caller binding protects against a wrapper that mutates after sources()
    # has completed its own checks. Only the consumed leaves are read.
    require(set(src)==set(PINS), 'Consumed source domain changed')
    for path,pin in PINS.items():
        require(sha(root/path)==pin,'Consumed physical source changed: '+path)
        text=normalized(root/path)
        physical=json.loads(text) if path.endswith('.json') else list(csv.DictReader(io.StringIO(text))) if path.endswith('.csv') else text
        require(src[path]==physical, 'Returned source differs from physical field binding: '+path)
    require(hashlib.sha256(json.dumps(FIXED_POLICY,sort_keys=True,separators=(',',':')).encode()).hexdigest()==POLICY_SHA,
      'Selected fictional method policy changed')

def expected_ratings(src, names):
    archive = {x['nba_player']:x for x in src[BPM]}
    require(len(archive)==len(src[BPM]), 'Duplicate observed BPM player')
    def observed(p):
        r = archive[p]
        require(r['observed_through']=='2021-03-25', 'Future BPM observation entered opening input')
        n = int(r['archive_minutes'])
        require(n>0, 'No observed minutes')
        return Fraction(r['bpm'])*n/(n+1000)
    comp = {p:observed(p) for p in COMPARATORS}
    novice = median(comp.values())
    result = {}
    for p in sorted(names):
        if p=='Protagonist':
            value = Fraction('-0.5'); kind = 'SELECTED_FICTIONAL_PRODUCTIVITY_PARAMETER'
            provenance = {'prior_BASE':-1.2, 'selected_increment':0.7, 'growth_input':'P21A',
              'not_a_box_to_BPM_fit':True, 'existing_LOW_HIGH_stress_bounds':[-3.0,0.3]}
        elif p in ('Chris Duarte','Jalen Suggs'):
            value = novice; kind = 'SELECTED_FICTIONAL_ROOKIE_PRIOR_NOT_OBSERVED_NBA_RATING'
            provenance = {'comparators_effective':{q:float(v) for q,v in comp.items()},
              'selected_statistic':'median', 'working_admissible_comparison_range':[float(min(comp.values())),float(max(comp.values()))],
              'Duarte_box_input':'D21A' if p=='Chris Duarte' else None,
              'not_college_BPM_or_NBA_translation_fit':True}
        else:
            target = ALIAS.get(p,p); value = observed(target)
            kind = 'SELECTED_ALTERNATE_HISTORY_PROXY_FROM_PREOPENING_HISTORICAL_OBSERVATION'
            r = archive[target]
            provenance = {'archive_player':target, 'reported_bpm':float(r['bpm']),
              'archive_minutes':int(r['archive_minutes']), 'observed_through':r['observed_through'],
              'reported_metric_is_not_primary_league_medical_or_alternate_ability_fact':True}
        result[p] = {'effective_rating':float(value), 'exact_fraction':str(value),
          'classification':kind, 'provenance':provenance}
    return result

def ratings(src,names):
    return expected_ratings(src,names)

def assert_role(row, health, economic):
    key = row['game_id']
    require(row['selected_chicago_state']==health['selected_chicago_state']=='COBY_OUT', 'Wrong selected CHI date state')
    require((row['date'],row['home'],row['away'])==(health['date'],health['home'],health['away']), 'Selected date/teams differ')
    require(economic['routine_contract_family_admitted_for_date'] and economic['nomination_and_positive_availability_implemented_within_family'], 'Date not in admitted economic implementation')
    require(economic['nominations']==row['nominations'] and economic['simultaneous_segments']==row['simultaneous_segments'], 'Economic role bridge differs')
    require(row['nominations']['CHI']['positive_seconds']=={p:int(m*60) for p,m in health['selected_regulation_player_minutes'].items()}, 'Health and minutes differ')
    require({p:row['nominations']['CHI']['positive_seconds'][p] for p in ['Protagonist','Markkanen','Caruso']}=={'Protagonist':1920,'Markkanen':1920,'Caruso':1080}, 'Old 28/22 role leaked')
    totals = {t:Counter() for t in ('CHI','DET')}; end = 0
    for s in row['simultaneous_segments']:
        require(s['start_second']==end and s['end_second']-end==s['seconds']>0, 'Common clock gap')
        require(s['quarter']==end//720+1 and s['end_second']<=(end//720+1)*720, 'Quarter crossing')
        for t in totals:
            require(set(s[t])=={'PG','SG','SF','PF','C'} and len(set(s[t].values()))==5, 'Role identity collision')
            for p in s[t].values():totals[t][p]+=s['seconds']
        end=s['end_second']
    require(end==2880, 'Not regulation clock')
    for t, seconds in totals.items():
        n=row['nominations'][t]
        require(len(n['standard'])==15 and len(set(n['standard']))==15 and len(n['two_way'])==2, '15+2 roster changed')
        require(not(set(n['standard'])&set(n['two_way'])) and len(n['active'])==12 and len(set(n['active']))==12, 'Nomination classification changed')
        require(set(n['active'])<=set(n['standard']) and not(set(n['active'])&set(n['inactive'])), 'Active identity invalid')
        require(dict(seconds)==n['positive_seconds'] and sum(seconds.values())==14400 and max(seconds.values())<=2880, 'Positive budget differs from clock')
        require(set(seconds)<=set(n['active']) and not(set(seconds)&set(n['unavailable_condition'])), 'Positive unavailable player')

def expected_game(role, rate, src):
    cal = next(x for x in src[CAL] if x['game_id']==role['game_id'])
    require((cal['date'],cal['home'],cal['away'])==(role['date'],role['home'],role['away']), 'Game source identity changed')
    day = date.fromisoformat(role['date']); yesterday = (day-timedelta(days=1)).isoformat()
    back = {t:any(x['date']==yesterday and t in (x['home'],x['away']) for x in src[LEAGUE]) for t in ('CHI','DET')}
    require(int(cal['historical_back_to_back_second'])==int(back['CHI']), 'Schedule fatigue diagnostic differs')
    ledger = {t:[{'player':p,'seconds':n,'effective_rating':rate[p]['effective_rating'],
      'contribution_per100':float(Fraction(rate[p]['exact_fraction'])*n/2880)}
      for p,n in sorted(role['nominations'][t]['positive_seconds'].items())] for t in ('CHI','DET')}
    team = {t:sum(Fraction(rate[x['player']]['exact_fraction'])*x['seconds']/2880 for x in ledger[t]) for t in ledger}
    home = Fraction(2 if role['home']=='CHI' else -2)
    fatigue = Fraction(1,2)*(int(back['DET'])-int(back['CHI']))
    margin = team['CHI']-team['DET']+home+fatigue
    require(margin!=0, 'Tied regulation proxy needs a separate result selection')
    return {'game_id':role['game_id'],'date':role['date'],'home':role['home'],'away':role['away'],
      'CHI_state':'COBY_OUT','role_source_pointer':'/rows/'+str(IDS.index(role['game_id'])),
      'player_contribution_ledger':ledger, 'team_weighted_BPM_per100':{t:float(v) for t,v in team.items()},
      'home_effect_in_CHI_direction_per100':float(home),'back_to_back_schedule_model':back,
      'fatigue_effect_in_CHI_direction_per100':float(fatigue),
      'CHI_minus_DET_regulation_impact_per100':float(margin),'exact_impact_fraction':str(margin),
      'selected_regulation_winner':'CHI' if margin>0 else 'DET',
      'classification':'AUTHOR_DELEGATED_SELECTED_FICTIONAL_REGULATION_WINNER_MODEL',
      'score':None,'overtime_selection':None,'actual_clinical_certificate':False,
      'historical_score_diagnostic_only':{'home_pts':int(cal['home_pts']),'away_pts':int(cal['away_pts']),
        'historical_inferred_OT':int(cal['inferred_historical_ot']),'used_to_decide_winner':False},
      'source_bound_nominations':deepcopy(role['nominations']),
      'positive_availability_is_selected_working_model':True,
      'active_nomination_is_selected_working_model':True,
      'source_role_clock_seconds':2880,'each_team_player_seconds':14400}

def selected_game(role, rate, src):
    return expected_game(role,rate,src)

def build(root=ROOT):
    src=sources(root)
    assert_consumed_sources(src,root)
    role_rows=src[ROLE]['rows']
    require(tuple(x['game_id'] for x in role_rows)==IDS, 'Two selected keys changed')
    health={x['game_id']:x for x in src[HEALTH]['selected_dates']}
    economics={x['game_id']:x for x in src[ECON]['two_date_execution']}
    names={p for r in role_rows for t in ('CHI','DET') for p in r['nominations'][t]['positive_seconds']}
    rate=ratings(src,names)
    require(rate==expected_ratings(src,names), 'Returned rating differs from source or selected working policy')
    games=[]
    for row in role_rows:
        assert_role(row,health[row['game_id']],economics[row['game_id']])
        result=selected_game(row,rate,src)
        require(result==expected_game(row,rate,src), 'Returned selected result differs from source clock/rating/calendar')
        games.append(result)
    growth={x['id']:x for x in src[GROWTH_DERIVED]['candidates'] if x['id'] in ('P21A','D21A')}
    return {'id':'CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS', 'baseline_main':BASELINE,
      'status':'TWO_REGULATION_WINNER_MODELS_SELECTED_INDEPENDENT_REVIEW_PENDING',
      'source_sha256':{**PINS,SELF:sha(root/SELF)},
      'hash_convention':'UTF8 BOM stripped; CRLF/CR to LF; existing raw caches unchanged',
      'authority':{'classification':'AUTHOR_DELEGATED_DESIGN_SELECTION', 'delegation_source':DELEGATION,
        'continuation_scope_source':SCOPE,'author_locked':False,'root_review_required_before_integrated_promotion':True},
      'selected_policy':deepcopy(FIXED_POLICY), 'player_ratings':rate,
      'selected_growth_productivity':{k:{'per36':v['per36'],'role_expected':v['role_expected'],
        'classification':v['status'],'scope':'Selected working productivity at these two dates only; not a derived BPM rating or actual box'} for k,v in growth.items()},
      'rows':games,
      'method_limits':['Absolute additive lineup BPM and home effect are selected working approximations, not the original 2020 delta-to-historical-margin model.',
        'Historical March25 priors precede October opening but arise in another team/history; using them here is a fictional proxy selection.',
        'Protagonist +0.7 improvement and rookie median are explicit productivity parameters, not a fitted NCAA-to-NBA conversion.',
        'No possession count, exact score, interaction fitting, probabilistic accuracy or overtime is certified.'],
      'remaining_consumer_ports':{'remaining_CHI_dates':80,
        'next_date_key':'0022100022','next_date':'2021-10-22','next_opponent':'NOP',
        'requirements_for_next_result':['Consume current selected CHI date state and reviewed admitted NOP paired role/operating family.',
          'Bind each positive-player preopening BPM or explicit fictional prior; supply source-current nominations/availability.',
          'Select date-specific single-method regulation result; OT only if separately modeled.'],
        'whole82_results_standings_pick_entitlement':'NOT_CERTIFIED'},
      'summary':{'selected_games':2,'CHI_model_wins':sum(x['selected_regulation_winner']=='CHI' for x in games),
        'DET_model_wins':sum(x['selected_regulation_winner']=='DET' for x in games), 'positive_rating_inputs':len(rate),
        'rating_methods':1,'RAPTOR_used':False,'historical_score_inheritance':False,'remaining_CHI_games':80},
      'certification':{'source_fields_and_returned_model_guarded':True,'independent_review_completed':False,
        'actual_games_or_scores_certified':False,'actual_medical_or_private_contract_receipts_certified':False,
        'full82_results_standings_picks_certified':False,'MVP_title_or_long_ending_selected':False,
        'whole_macro3_completed':False,'manuscript_allowed':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED'}}

def render(d):
    lines=['# Detroit–Chicago 두 날짜 선택 BPM 결과 작업모델', '',
      '현재 양팀 역할·명단·경제 가족과 Chicago COBY_OUT 선택을 소비하여 **두 경기의 규정시간 승자**를 선택했다. 독립 검문은 대기 중이다.', '',
      '| 날짜 | 홈 | Chicago−Detroit 작업 impact /100 | 선택 승자 |', '|---|---|---:|---|']
    for x in d['rows']:lines.append(f"| {x['date']} | {x['home']} | {x['CHI_minus_DET_regulation_impact_per100']:.9f} | {x['selected_regulation_winner']} |")
    lines += ['', '## 계산과 사실·모델 구분', '',
      '- 방법은 기존 `BPM_MAR25_EB` 하나다. 2021-03-25 관측 BPM에 `관측분/(관측분+1000)`을 적용하고 현재 선수초/2880을 곱해 팀별 합을 계산한다. 과거 2020 모델의 **기존 경기점수에 분 치환 delta를 더하는 방식**과 달리, 이번 절대 팀합·홈 효과는 명시적으로 선택한 작업 근사다.',
      '- 현재 M1은 주인공32·Markkanen32·Caruso18이다. 이전 28/22 역할을 쓰지 않았다. 양팀 48분/240분, 양수 선수·active12·15STD2TW가 선택된 원시계에 연결된다.',
      '- 주인공 BASE −1.2에서 +0.7인 −0.5를 비MVP 생산성 작업계수로 선택한다. P21A(18득점/36분)·D21A 생산성도 두 날짜 작업모델로 선택하지만 박스 수치를 BPM으로 환산했다고 주장하지 않는다.',
      '- Duarte·Suggs는 기존 Vassell/Nesmith/Green/Bey/Bane 축소 BPM 중앙값 −0.635807860262를 동일한 보수적 신인 작업 prior로 선택한다. 비교범위 −1.159461480927~−0.075853507138은 실제 신인 능력의 신뢰구간이 아니다. Suggs/Duarte의 NBA 실측·공식 스카우팅·college regression 계수가 아니다.',
      '- 나머지 선수의 과거 관측을 대체세계 생산성 proxy로 선택했다. LaMelo의 Charlotte 관측, Carter의 원역사 등은 현재 대체팀의 실제 성적 인증이 아니다. 2021–22 미래 실제 BPM을 쓰지 않았다.',
      '- 홈 +2/100, 연전 −0.5/100, 교대 상호작용 0은 선택한 가상 모델이다. 원 일정에서 Chicago는 10/22 뒤 10/23 연전, Detroit은 아니다. 첫 경기 impact +4.108526664479, 둘째 +7.608526664479이며 두 날짜 모두 Chicago 승자로 선택한다.',
      '- 원역사 88–94 및 97–82는 원 CSV의 진단값으로만 저장한다. 새 정확 점수·실제 박스·OT·득점 확률을 만들지 않았다. 이 impact 수치는 새 NBA 최종 점수 차이가 아니다.', '',
      '## 원천과 실제 검문', '',
      '[선택 역할](DET_TWO_DATE_ROLE_ADOPTION_2026_10_07.json), [선택 경제 가족](DET_ROUTINE_OPERATING_FAMILY_SELECTION_2026_10_07.json), [선택 Chicago 건강](../canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json), [현재 paired clock](CHICAGO_DETROIT_2021_TWO_DATE_WORKING_EXECUTION.json), [성장 입력](CHICAGO_2021_22_GROWTH_INPUTS.json), [BPM 관측](CHICAGO_2020_21_BPM_MAR25_SNAPSHOT.csv)을 고정 지문과 실제 소비 필드로 조인한다. 전체 조상 생성기를 재실행하지 않는다.',
      '반환 rating·승자·선수초·현실 인증의 변조를 caller가 별도 원천·고정 선택정책으로 거절한다. 작성자 검사는 독립 검문으로 계수하지 않는다.', '',
      '## 다음 유한 실행', '',
      '다음 미계산 키는 2021-10-22 NOP `0022100022`다. 검문된 NOP 양팀 시계에 현 Chicago 선택 상태와 명명된 NOP 루틴 계약·가용성을 연결하고 양수 선수 rating을 소비하면 된다. 82경기 중 결과 작업모델은 2, 나머지는 80이다. 전체 순위·2022 지명권 결산은 미완료다.', '',
      '## 7행 진행표', '',
      '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)을 따른다. 아래는 이 결과 소비기의 범위이며 중앙 현황을 변경하지 않는다.', '',
      '| 번호 | 작업 | 상태 |','|---|---|---|',
      '| 1 | 2020 드래프트 연쇄 | 완료 |','| 2 | Chicago 2020–21 | 완료 |',
      '| 3 | 2021–23 거래·계약 | 진행: DET 두 결과 작업모델 선택, 전체 미완료 |',
      '| 4 | 장기 커리어 | 진행·후속 시즌 입력 대기 |','| 5 | 결말·전체 구조 | 골격 완료·전체 미완료 |',
      '| 6 | 집필 규격·Context Pack | 기능 설계 진행·실제 Pack0 |','| 7 | 통합·독립·작가 승인 | 전체 미완료 |', '',
      '**미완료 큰 묶음 5개**, 6번까지 4개. Freeze **v0.30 PARTIAL**, 설계/원고 **CLOSED**, 원고0. 새 MVP·우승·장기 결말·중요 거래를 선택하지 않는다.', '']
    return '\n'.join(lines)

def validate(d,root=ROOT):
    try:return [] if d==build(root) else ['Saved output differs from source-bound selected model']
    except (ValueError,KeyError,StopIteration,AssertionError) as e:return [str(e)]

def self_test():
    original=selected_game; original_ratings=ratings; original_sources=sources; checks=[]
    def wrong_winner(*a):
        x=original(*a);x['selected_regulation_winner']='DET';return x
    def same_total_wrong_player(*a):
        x=original(*a);x['player_contribution_ledger']['CHI'][0]['seconds']+=60;x['player_contribution_ledger']['CHI'][1]['seconds']-=60;return x
    def actual_promotion(*a):
        x=original(*a);x['actual_clinical_certificate']=True;return x
    def wrong_rating(*a):
        x=original_ratings(*a);x['Protagonist']['effective_rating']=4.0;x['Protagonist']['exact_fraction']='4';return x
    for name,fn in [('WRONG_WINNER',wrong_winner),('SAME_TOTAL_WRONG_PLAYER_SECONDS',same_total_wrong_player),('ACTUAL_MEDICAL_PROMOTION',actual_promotion)]:
        with patch(__name__+'.selected_game',fn):
            try:build()
            except ValueError:checks.append(name)
            else:raise AssertionError('False PASS: '+name)
    with patch(__name__+'.ratings',wrong_rating):
        try:build()
        except ValueError:checks.append('FICTIONAL_MVP_RATING_SUBSTITUTION')
        else:raise AssertionError('False PASS: RATING')
    def wrong_source(*a):
        x=original_sources(*a);x[GROWTH_DERIVED]['candidates'][0]['per36']['pts']+=1;return x
    with patch(__name__+'.sources',wrong_source):
        try:build()
        except ValueError:checks.append('RETURNED_GROWTH_SOURCE_CHANGED_WITH_SAME_SHA')
        else:raise AssertionError('False PASS: SOURCE')
    return checks

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');args=p.parse_args()
    d=build()
    if args.write:
        (ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (ROOT/MD).write_text(render(d),encoding='utf-8')
    if args.check:
        require(json.loads((ROOT/OUT).read_text(encoding='utf-8-sig'))==d,'Saved JSON stale')
        require(normalized(ROOT/MD)==render(d),'Saved MD stale')
    print(json.dumps({'current':True,'summary':d['summary'],'results':[{k:r[k] for k in ['game_id','selected_regulation_winner','CHI_minus_DET_regulation_impact_per100']} for r in d['rows']], 'writer_negative_controls':self_test() if args.self_test else None},ensure_ascii=False))

if __name__=='__main__':main()
