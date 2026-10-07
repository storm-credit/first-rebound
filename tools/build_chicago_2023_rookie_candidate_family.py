"""Chicago #16: three conditional rookie choices; no draft/UPC selection."""
from __future__ import annotations
import argparse, copy, hashlib, json
from fractions import Fraction
from pathlib import Path
import fitz
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_chicago_2023_rookie_candidate_family.py'
OUTPUT = 'research/CHICAGO_2023_ROOKIE_CANDIDATE_FAMILY_2026_10_08.json'
MD = OUTPUT[:-5] + '.md'
ROUTINE = 'simulation/CHICAGO_2023_SELECTED_ROUTINE_EXECUTION.json'
SLOT = 'research/CHICAGO_2023_FIRST_ROUND_SLOT_16_2026_10_08.json'
CLAIMS = 'research/CHICAGO_2023_NAMED_DRAFT_CLAIMS_AND_COST_PORTS_2026_10_08.json'
DRAW = 'simulation/NBA_2023_DRAFT_ORIGIN_ORDER.json'
H22 = 'simulation/CHICAGO_2022_23_SELECTED_DATED_ROLES.json'
PRIMARY = 'research/MACRO3_2023_CBA_BOUNDARY_PRIMARY_SOURCES_2026_10_07.json'
DRAW_ADOPTION = 'canon/DELEGATED_2023_DRAFT_ORIGIN_DRAW_DECISION_2026_10_08.json'
ROUTINE_PEER = 'reviews/CHI_2023_SELECTED_ROUTINE_EXECUTION_G11_INDEPENDENT_REVIEW_2026_10_08.json'
PRIOR21 = 'simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json'
PRIOR22 = 'research/NBA_2022_FULL_DRAFT_WORKING_BOARD_2026_10_08.json'
PRIOR22_ADOPTION = 'canon/DELEGATED_2022_DRAFT_AND_CHICAGO_ROOKIE_DECISION_2026_10_08.json'
PINS = {
    ROUTINE: '9a4f6db21d6ad50e2c6d6897f1c2dedbdf440cee89bae47019f4bd131f341790',
    SLOT: 'abbcdaaa6ff14d277f88d47fa600320fc6458ec4b057e5a7b73b414b6fbabf30',
    CLAIMS: 'b139af4af09a48dd1c9e345d17d05fc8e38f4cb021193f32bc3a09ed537f49e3',
    DRAW: 'e51f36a83e8961aa2d81cd342cce812f91353427cb26999e9bb0cd56275d4320',
    H22: 'c0650dbb07b75cc1523bf7ccc7f658576ac5b9a8784f1e80cc97178897703170',
    PRIMARY: '59b03c494187eb29177640806ae97427a837abff38bf4516f588758fc87a0112',
    DRAW_ADOPTION: '6df7f62328263c0b3864e2d4a05cb4a5b56edbd332d5d31556627c6b421d9292',
    ROUTINE_PEER: 'e9bfc3699dd2da3c4cfd6871e05f1b729748674018e617f098f3e5138065f169',
    PRIOR21: 'f8c78e99cce1b02a051c94339b550fdb52205d3988db8bbe69b780559c3bc306',
    PRIOR22: '3bdad52ebaacda5abb23b9908b8ed3a9b85cfaa09d838819a959cd024a58e940',
    PRIOR22_ADOPTION: 'a32dfc265a7250bc89df366c14b43444645438675674f4be66feda2b6a053eba',
}
CACHE = Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-chi-2023-rookie-20261008')
CBA = Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-2023-cba-boundary-20261007/cba2023.pdf')
CBA_SHA = 'bf178ca0f2d64f9dfe6fde095d3ae43d576b12e19ce7a679618d632584f7ab32'
CBA_URL = 'https://imgix.cosmicjs.com/25da5eb0-15eb-11ee-b5b3-fbd321202bdf-Final-2023-NBA-Collective-Bargaining-Agreement-6-28-23.pdf'
PAGE_PINS = {
    31: 'f1cf878da1d9b554ff242e52975f67f0bda1127300045f04b5188ebd4e506b52',
    32: '36dcc728a20e458fcbce59867c8005c9c97ee60a299e7b1de1608dd27ac67d07',
    33: '397f25af16b982f0ab5a0199789aab9c9b9e577fe0fd3b010fdb0f5fc3012d5e',
    90: 'b3ddf20fa2f483cb332e7f79736d759c0dae4905b25f26e860e691fc0b734d65',
    243: 'dbbd018d9ac268a74a2783409b3dbd6c67f4e2bd433c75fe6d61b61f9bb56238',
    263: 'b59e862b18edab17257a4144a81756f2cc4ee22353962f1eeb889decf825fb3d',
    314: 'ba6cbb014b01eeff2e41de886f7caf82a583aafa57b3f7e1fce8d89c77fe6cbe',
    316: '911b6ee4c99c608bd22675715b0732d96528ce0b81cca4a35e22df051d8d2303',
    317: '52dc9099c112651e81d03ad5a18743fe012760f205d4c636ee065e2931234a6b',
    323: '58d024e3f6fff5c433d7e8839302c940c891131ba1afe29f5cbc983c87971a8d',
    631: 'a299cb98e6f5465d546cfdff55b960b9d659275c4b4460109e01b06ecfb624c9',
}
COLLEGE = {
    'UCLA.raw': ('eebea48632b886bb9dae8c93f4ec1d46bdc87f1f9297d4477f501fde02ee7b89', 'https://uclabruins.com/news/2023/06/22/jaquez-jr-bailey-clark-selected-in-2023-nba-draft', ['Jaquez', '17.8', '8.2', '37', 'Miami', '18']),
    'SCU_bio.raw': ('a0f68e0555c1ce4ff6dad6c2b08b146546adcb0dc7f9ae299cf6bf630a53752b', 'https://santaclarabroncos.com/sports/mens-basketball/roster/brandin-podziemski/7673', ['Podziemski', '19.9', '8.8', '43.8', 'Sophomore', '32']),
    'IOWA.raw': ('42b36f7cc18765b8c945d4bc76ddf1446c70c53ae788c8bd4c37234d52ca6f44', 'https://hawkeyesports.com/news/2023/06/22/kris-murray-picked-23rd-by-portland-trail-blazers', ['Kris Murray', '20.2', '7.9', '23rd', 'Portland']),
}
CORE_MINUTES = {'Protagonist': 32, 'Lauri Markkanen': 32, 'Alex Caruso': 18}
CANDIDATES = [
    {'id': 'J16', 'player': 'Jaime Jaquez Jr.', 'position': 'SG/SF', 'college': 'UCLA', 'college_stage': 'senior',
     'historical_pick': 18, 'historical_team': 'MIA', 'college_2022_23': {'GP': 37, 'PPG': '17.8', 'RPG': '8.2'},
     'evidence': 'UCLA.raw', 'recommended': True,
     'fit_inference': '4년 대학 경험을 가진 보조 윙. 주인공의 볼 점유·리더십을 대체하지 않는 벤치 연결 역할을 권고한다.',
     'growth_limit': '수비 적응과 외곽 정확도는 새 NBA 성장 입력. 실제 2023–24 성과·수상은 사용하지 않는다.',
     'minute_delta_comparison_only': {'Jaime Jaquez Jr.': 6, 'Chris Duarte': -2, 'Thaddeus Young': -4},
     'opportunity_cost': 'Duarte/Young/Green/Valentine 윙 기회를 일부 사용. Duarte의 성장 서사를 없애는 주전 교체는 이 후보에 없다.',
     'original_team_port': 'MIA #18은 Jaquez를 재지명할 수 없음. 새 대체 후보/계약/분/성과는 별도 후손이며 자동 보상자산 없음.'},
    {'id': 'P16', 'player': 'Brandin Podziemski', 'position': 'PG/SG', 'college': 'Santa Clara', 'college_stage': 'sophomore',
     'historical_pick': 19, 'historical_team': 'GSW', 'college_2022_23': {'GP': 32, 'PPG': '19.9', 'RPG': '8.8', 'APG': '3.7', 'three_point_percent': '43.8'},
     'evidence': 'SCU_bio.raw', 'recommended': False,
     'fit_inference': '슈팅·리바운드가 있는 보조 가드. LaMelo/Coby/Caruso와 역할이 겹쳐 세 후보 중 분 배치 비용이 크다.',
     'growth_limit': '대학 성공을 NBA 생산성으로 환산하지 않음. NBA 첫해 평점과 출장량은 미선택.',
     'minute_delta_comparison_only': {'Brandin Podziemski': 6, 'Coby White': -4, 'Tomas Satoransky': -2},
     'opportunity_cost': 'Coby 재계약 후 벤치 성장 분을 일부 줄임. Caruso18/LaMelo 주전 방향은 유지한다.',
     'original_team_port': 'GSW #19 새 지명자 포트. 실제 Podziemski 신인 계약·이후 트레이드 가치/분을 GSW에 남겨둘 수 없음.'},
    {'id': 'M16', 'player': 'Kris Murray', 'position': 'SF/PF', 'college': 'Iowa', 'college_stage': 'junior',
     'historical_pick': 23, 'historical_team': 'POR', 'college_2022_23': {'PPG': '20.2', 'RPG': '7.9'},
     'evidence': 'IOWA.raw', 'recommended': False,
     'fit_inference': '벤치 포워드·Mark 휴식 구간 보완. 포지션 여유는 있으나 윙 연결보다 Young의 PF 기회를 더 사용한다.',
     'growth_limit': '대학 득점량은 NBA 득점/즉시전력 인증이 아니다. 신인 NBA 평점·성장은 미선택.',
     'minute_delta_comparison_only': {'Kris Murray': 6, 'Thaddeus Young': -6},
     'opportunity_cost': 'Mark32 유지, Young 보조 포워드 분 감소. 형제의 원 NBA 소속·지명순서를 선택 세계에 이식하지 않음.',
     'original_team_port': 'POR #23 새 후보 포트. 실제 Murray 계약/양수 분 및 이후 거래는 그대로 복사하지 않음.'},
]
FIXED_CANDIDATES = json.dumps(CANDIDATES, sort_keys=True, ensure_ascii=False)

def text(p):
    return Path(p).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')

def sha(p):
    return hashlib.sha256(text(p).encode()).hexdigest()

def direct(root, p):
    return json.loads(text(root / p))

def sources(root):
    result = {}
    for p, h in PINS.items():
        assert sha(root / p) == h, f'Source stale: {p}'
        result[p] = direct(root, p)
    return result

def primary_support():
    assert hashlib.sha256(CBA.read_bytes()).hexdigest() == CBA_SHA, 'CBA raw changed'
    with fitz.open(CBA) as d:
        for page, h in PAGE_PINS.items():
            assert hashlib.sha256(d[page-1].get_text().encode()).hexdigest() == h, f'CBA page changed: {page}'
    captures = []
    for file, (h, url, tokens) in COLLEGE.items():
        raw = (CACHE/file).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == h, f'College raw changed: {file}'
        body = BeautifulSoup(raw, 'html.parser').get_text(' ', strip=True)
        assert all(t in body for t in tokens), f'College body meaning changed: {file}'
        captures.append({'path': str(CACHE/file), 'url': url, 'raw_sha256': h, 'HTTP_status': 200,
                         'body_directly_read': True, 'fact_scope': 'college season and historical draft; not future NBA productivity'})
    # Failed raw bytes stay separate from indexed/web observations.
    failures = [dict(x, body_evidence=False) for x in json.loads(text(CACHE/'sources.json')) if not x['raw_body_adopted']]
    for x in failures:
        assert hashlib.sha256(Path(x['cache_path']).read_bytes()).hexdigest() == x['raw_sha256']
    return {'CBA': {'url': CBA_URL, 'raw_cache': str(CBA), 'raw_sha256': CBA_SHA,
                    'page_text_sha256': {str(k):v for k,v in PAGE_PINS.items()}, 'extraction': 'PyMuPDF page.get_text() UTF8, raw extracted text; no LF normalization for page text'},
            'college_raw': captures, 'failed_raw_not_body': failures,
            'NBA_draft_web_observation': {'url': 'https://www.nba.com/news/2023-nba-draft-order',
                'observation': 'NBA indexed result: Jaquez MIA18; Podziemski GSW19; Murray POR23.',
                'indexed_text_observed': True, 'HTTP_raw_body_certified': False,
                'actual_2023_order_is_fictional_first15_authority': False},
            'source_disagreement': {'Kris_Murray_college_PPG': 'Iowa 20.2; NBA prospect profile 20.7. Iowa primary adopted; no silent reconciliation.'}}

PRIMARY_MEANING_SHA = '7356fa7218749a84e3925bb9aacf21868b0e71a4c877b192a2fc9222d66daecb'
COLLEGE_METADATA_SHA = '851148d538064e4637651190f69d561fbccf2115b63d204e2dc61a7f2d73fc02'

def assert_primary_return(v):
    assert hashlib.sha256(CBA.read_bytes()).hexdigest() == CBA_SHA, 'Physical CBA changed'
    assert sha(CACHE/'sources.json') == COLLEGE_METADATA_SHA, 'Physical capture metadata changed'
    for file, (h, url, tokens) in COLLEGE.items():
        assert hashlib.sha256((CACHE/file).read_bytes()).hexdigest() == h, 'Physical college raw changed'
    with fitz.open(CBA) as d:
        for page, h in PAGE_PINS.items():
            assert hashlib.sha256(d[page-1].get_text().encode()).hexdigest() == h, 'Physical CBA page changed'
    assert hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest() == PRIMARY_MEANING_SHA, 'Returned primary support differs from physical reviewed metadata'

def scale_family():
    return {'selection_number': 16, 'first_Season': '2023-24', 'prepared_exact_table_or_rounding_certified': False,
        'S23': 'NBA-prepared positive first-three-year S23(16,y), y=1..3, I1(hhh)/(iii); S23(16,4)=S23(16,3)*767/500 derived reference, not independent table price',
        'alpha_domain': '[max(4/5, max_y M_y/S23(16,y)), 6/5], subject to nonempty lawful prepared scale',
        'current_base_y1_y2_y3': 'alpha*S23(16,y); full base protection; zero new bonuses/signing bonus/loan',
        'year4': 'base3*767/500 (53.4% increase); Exhibit B #16/PDF631 and VIII1(c)(iii); unchanged non-payment terms',
        'guaranteed_Seasons': 2, 'team_option_Seasons': [3,4], 'future_options_exercised': False,
        'third_option_window': 'day after last day of first Season through immediately following Oct31; XLII2 adjustment',
        'fourth_option_window': 'day after last day of second Season through immediately following Oct31; XLII2 adjustment',
        'normal_unsigned_hold': '6/5*S23(16,1)', 'signed_normal_and_apron': 'alpha*S23(16,1), same claim replaced once',
        'unused_RSC_hold_or_old_first_RT_double_count': False, 'new_hardcap_trigger': False,
        'mechanism': '2023 VII6(h) Rookie Scale Exception', 'actual_salary_cents': None}

FIXED_SCALE = json.dumps(scale_family(), sort_keys=True)

def evaluate(scale, minimum, alpha):
    """Callable typed family. Input cents must be lawful prepared table, not invented here."""
    s, m, a = list(map(Fraction, scale)), list(map(Fraction, minimum)), Fraction(alpha)
    assert len(s) == len(m) == 4 and all(x > 0 for x in s+m), 'Four positive scale/minimum inputs required'
    assert Fraction(4,5) <= a <= Fraction(6,5) and all(a*x >= y for x,y in zip(s,m)), 'RSC floor/120% limit'
    assert s[3] == s[2]*Fraction(767,500), 'Year4 reference must equal Year3 plus Exhibit B #16 53.4%'
    salaries = [a*x for x in s[:3]]
    salaries.append(salaries[2]*Fraction(767,500))
    return {'current_base_exact': list(map(str,salaries)), 'normal_unsigned': str(Fraction(6,5)*s[0]),
            'signed_normal': str(salaries[0]), 'signed_apron': str(salaries[0]),
            'numeric_inputs_are_actual_NBA_prepared_scale_certified': False}

def candidates():
    return copy.deepcopy(CANDIDATES)

def draft_selection_event():
    return {'order':1,'date':'2023-06-22','event':'CONDITIONAL_CHI16_DRAFT_SELECTION',
        'STD':None,'TW':None,'registration_delta':0,'drafted_rights':1,'new_UPC':False,
        'FY23_July7_projection_STD':14,'projection_is_June22_current_registration':False,
        'prior_service_registration_reference':'ROUTINE June28 original_service_contracts_before_July1; nine is forward-fiscal, not current registration',
        'actual_registration_certified':False}

def build(root=ROOT):
    src = sources(root)
    for p in PINS:
        assert src[p] == json.loads(text(root/p)), f'Returned source differs from physical source: {p}'
    state = next(x for x in src[ROUTINE]['dated_states'] if x['date'] == '2023-07-07')
    assert state['STD_count'] == 14 and state['live_TW_UPC_count'] == 0 and len(set(state['named_live_STD'])) == 14
    assert state['first_round_pick'] == 16 and state['reserved_first_STD_slot'] == 1 and state['rookie_identity'] is None
    assert state['original_Gamma_and_R23_preserved'] and state['R23_interval'] == [0,16371000]
    assert src[SLOT]['Chicago_record'] == {'wins':46,'losses':36} and src[SLOT]['lottery_count'] == 14
    assert src[SLOT]['Chicago_origin_first_slot'] == 16 and src[SLOT]['Chicago_selected_holder'] == 'CHI'
    claims = src[CLAIMS]['named_claims']
    assert claims[0]['origin'] == 'CHI' and claims[0]['round'] == 1 and claims[0]['selected_holder'] == 'CHI'
    assert claims[1]['round'] == 2 and claims[1]['selected_holder'] == 'WAS'
    assert src[DRAW_ADOPTION]['source_sha256'][DRAW] == PINS[DRAW]
    assert src[ROUTINE]['cost_family']['July7_normal_apron_base_before_R23_first_hold_FRN_conditional_upper'] == 157912834
    old = src[H22]['selected_role_template']['player_minutes']
    assert all(old[p] == m for p,m in CORE_MINUTES.items()) and sum(old.values()) == 240
    support = primary_support()
    assert_primary_return(support)
    rows, family = candidates(), scale_family()
    assert json.dumps(rows,sort_keys=True,ensure_ascii=False) == FIXED_CANDIDATES, 'Returned candidate comparison changed'
    assert json.dumps(family,sort_keys=True) == FIXED_SCALE, 'Returned RSC law/form changed'
    assert len({x['player'] for x in rows}) == 3 and all(x['historical_pick'] > 16 for x in rows)
    prior_players = [x['player'] for x in src[PRIOR21]['selected_rows']] + [x['player'] for x in src[PRIOR22]['rows']]
    assert len(src[PRIOR21]['selected_rows']) == len(src[PRIOR22]['rows']) == 60
    assert src[PRIOR22_ADOPTION]['selected']['working_draft_identities'] == 60
    assert not set(prior_players).intersection(x['player'] for x in rows), 'Candidate already drafted in preserved prior board'
    outputs = []
    for x in rows:
        draft_event = draft_selection_event()
        assert draft_event == {'order':1,'date':'2023-06-22','event':'CONDITIONAL_CHI16_DRAFT_SELECTION',
            'STD':None,'TW':None,'registration_delta':0,'drafted_rights':1,'new_UPC':False,
            'FY23_July7_projection_STD':14,'projection_is_June22_current_registration':False,
            'prior_service_registration_reference':'ROUTINE June28 original_service_contracts_before_July1; nine is forward-fiscal, not current registration',
            'actual_registration_certified':False}, 'June22 rights event must not certify future July7 registration'
        delta = x['minute_delta_comparison_only']
        assert sum(delta.values()) == 0 and all(delta.get(p,0) == 0 for p in CORE_MINUTES)
        assert x['player'] not in state['named_live_STD']
        outputs.append({'choice': x['id'], 'player':x['player'], 'candidate_holder':'CHI', 'selection_number':16,
            'admitted_conditions': ['2023 eligible participant under applicable Article X; timely early entry/nonwithdrawal if needed',
                'not selected in preceding15; CHI retains own first right at selection',
                'lawful fictional player/CHI assent to conforming RSC; no prior incompatible UPC',
                'lawful NBA-prepared S23 and minimum table supplied to evaluate(); alpha in nonempty domain'],
            'first15_not_yet_selected': True, 'historical_rank_does_not_prove_counterfactual_availability': True,
            'events': [draft_event,
                {'order':2,'date':'2023-07-07','event':'TEAM_SIGNED_VALID_REQUIRED_TENDER_DELIVERY','STD':14,'TW':0,
                 'offer_acceptance_end':'at least first day of 2023-24 Regular Season','deadline_condition':'July7 precedes July15 (and any applicable business-day adjustment)',
                 'Salary_function':'same scale_family, alpha=max(4/5,max_y M_y/S_y), including year4 linkage; no new bonuses', 'actual_delivery':None},
                {'order':3,'date':'2023-07-07T12:00:00-04:00','event':'FICTIONAL_RSC_SIGNING_AFTER_TENDER','STD':15,'TW':0,'new_UPC':True,
                 'original_14_Gamma_and_R23_preserved':True,'same_unsigned_claim_replaced_once':True,'actual_assent_receipt':None}],
            'new_salary_function':family,'registration_delta':1,'core_minutes_comparison_preserved':CORE_MINUTES,
            'source_H22_role_is_not_new_FY24_role_selection':True,'new_FY24_health_minutes_results_selected':False,
            'selected':False,'author_locked':False,'trade_or_cash_transfer_proposed':False})
    return {'id':'CHICAGO_2023_ROOKIE_CANDIDATE_FAMILY','status':'THREE_SOURCE_SUPPORTED_CONDITIONAL_CHOICES_PENDING_SELECTION_AND_PEER_REVIEW',
        'baseline_source_checkpoint':'PR499 241821ba; source-current immutable later leaves consumed without baseline rewriting',
        'source_sha256':dict(PINS,**{SELF:sha(root/SELF)}),'primary_support':support,
        'source_refresh_record': {'old_ROUTINE_pin':'b78a8217f32f28db00364534cbaa1cdc98d76e9cf391ce773ea7af706ad89661',
            'old_pin_check':'REJECTED_STALE_BEFORE_FIRST_SUCCESSFUL_GENERATION',
            'new_generation_input':PINS[ROUTINE], 'root_frozen_reviewed_input_acknowledged':True,
            'old_failed_output_certified_current':False},
        'source_join': {'July7_named_STD14':state['named_live_STD'],'live9_plus_routine5':True,'TW':0,'CHI_owned_first':16,'CHI_owned_second_count':0,
            '2023_origin_draw_selected_by_separate_root_record':True,'CHI16_independently_derived_without_whole_draw':True,
            'origin_candidate_generation_status_rewritten':False,'whole_2023_holders_forfeitures_draftees_certified':False,
            'prior_selected_2021_and_2022_boards_checked':120,'candidate_prior_draft_duplicate_count':0,
            'source_routine_candidate_false_flags_are_generation_history':True},
        'candidate_rows':rows,'execution_families':outputs,'recommendation':{'choice':'J16','selected':False,
            'reason':'보조 윙 경험을 우선하며 주인공/Mark/Caruso 분을 보호. Podziemski는 재계약 Coby와 가드 혼잡, Murray는 Young PF 기회 비용.'},
        'cost_join':{'source_conditional_base_before_R23_rookie_FRN':157912834,'R23_interval':[0,16371000],
            'normal_unsigned':'157912834 + R23 + 1.2*S23(16,1), plus separately applicable FRN changes',
            'signed_normal_apron':'157912834 + R23 + alpha*S23(16,1), plus separately applicable FRN changes',
            'all_other_named_FA_QO_holds_and_Gamma_preserved':True,'additional_original_team_trade_compensation':None,
            'prepared_S23_exact_cents':None,'whole_FY23_cost_certified':False,'renounce_is_not_protected_cash_deletion':True},
        'remaining_finite_inputs':['root routine rookie choice after peer; not franchise/MVP/title/core/military change',
            'preceding15 selection must leave chosen player available; no whole60 rights certification prerequisite for CHI16',
            'lawful prepared S23(16) and minimum inputs for exact numeric cost; not required for symbolic family comparison',
            'new FY24 position/240-minute/availability carrier; old H22 includes expired Bradley and is not copied',
            'MIA18/GSW19/POR23 replacement selection and downstream economics only for the chosen original team'],
        'certification':{'candidate_lawful_function_prepared':True,'rookie_draft_or_UPC_selected':False,'actual_participation_paper':False,
            'actual_contract_salary_assent_or_league_receipt':False,'independent_review_completed':False,'military_or_protagonist_core_changed':False,
            'whole_macro3_complete':False,'manuscript_allowed':False,'design_gate':'CLOSED','Pack_count':0}}

def render(o):
    s = ['# Chicago 2023 자체 16번 신인 후보 가족','',
        '세 후보 비교와 계약/권리/슬롯의 실행 함수를 준비했다. **J16 Jaquez 권고·선택0·독립 검문 pending**. 원 NBA 실제 16번, 앞선15 지명 또는 원 팀의 다음 계약을 복사하지 않는다. 새 root draw 채택 기록을 생성 입력으로 연결했으며 원 추첨 후보의 generation 미선택 표기는 수정하지 않았다.','',
        '## 비교','', '| 후보 | 실제 원형 | 대학 2022–23 관측 | Chicago 후보 역할/비용 |','|---|---|---|---|']
    for x in o['candidate_rows']:
        stats=x['college_2022_23']
        s.append(f"| {x['player']} ({x['position']}) | {x['college']} {x['college_stage']}; 원 {x['historical_team']} #{x['historical_pick']} | {stats['PPG']}점 / {stats['RPG']}리바운드 | {x['fit_inference']} {x['opportunity_cost']} |")
    s += ['', '학교 원문은 대학 성과와 원역사 지명의 양성 근거다. 기존2021/2022 선택 보드120행과 세 이름의 중복0을 직접 연결했다. NBA 첫해 평점·건강·수상·실력 성장은 입력하지 않았다. Murray 대학 득점은 Iowa20.2/NBA프로필20.7 불일치를 보존한다. 6분 donation은 순변화0의 비교안이며 새 FY24 감독 시계/240분/건강을 선택한 것이 아니다. 주인공32·Mark32·Caruso18 침해0; Bradley 만료 때문에 old H22 전체 시계 자동 운반0.','',
        '## 명명 법적 실행 함수','',
        'July7의 live9+루틴5=14STD/0TW, 자체1R16/2R0/예약1. June22 지명권 선택은 새 UPC/등록delta0이며 그날 currentSTD/TW는 null이다. 미래July7 숫자를 June22의 등록으로 인증하지 않는다. 각 후보는 앞선15 미지명·CHI권리·참가적격 조건 아래 6/22 지명권→7/7 유효 team-signed Required Tender→같은 날 정오 가상 RSC 합의로 14→15STD/0TW가 된다. 7/7은 July15 이전이며 RSC는 moratorium 중에도 II15(b)(ii)로 허용된다. RT의 수락창은 다음 정규시즌 첫날 이상이고 실제 전달·수락은 null이다. 새 거래/이적료/원선수 방출이 필요하지 않은 빈 슬롯 경로다.','',
        '`S23(16,y)`는 I1(hhh)/(iii)의 NBA-prepared 표. 정확 표/반올림/cents는 미인증이다. VIII1(c)의 base≥max(80%scale,minimum), Salary+Unlikely≤120%를 모두 지킨 동일 α 가족; 첫3년 αS, 4년차는 3년차×767/500(53.4% 증가)로 연동한다. Exhibit B의 4년차 열은 독립 급여가 아닌 증가율이다. 첫2Season·팀옵션3/4, full base protection·새bonus/loan0을 후보로 명시했다. 옵션은 첫/둘째 Season 종료 다음날부터 그 다음 Oct31까지의 후속 통지이며 현재행사0. 원2023–24 가격을 MIA18/GSW19/POR23 실제 계약에서 복사하지 않는다.','',
        'VII6(h) RSC Exception 사용; 이 RSC 자체는 새 hardcap trigger가 아니다. normal 미서명hold=1.2S를 서명 αS로 같은 청구권 한 번 교체; apron RT→UPC도 한 번 교체. 조건부 기초157,912,834+R23[0,16,371,000]+신인함수(및 적용 FRN 변화)를 보존하며 whole cost PASS는 아니다. 기존 FA/QO/보호채무·잔존stretch를 지우지 않는다.','',
        '## 원 팀 나비효과 / 다음 입력','']
    for x in o['candidate_rows']:s.append('- '+x['original_team_port'])
    s += ['', 'J16/P16/M16은 상호 배타적 같은 슬롯 대안이다. 선택 후 앞선15에서 해당 선수 가용성을 연결하고, 선택된 원 팀의 대체 후보를 별도 처리한다. Chicago 군복무·주인공 연장/프랜차이즈·MVP/titlecount/core 방향을 바꾸지 않는다. 실제 해외/의료/기관 영수증 전수 부재 인증을 새 gate로 추가하지 않는다.','',
        '## 실제 원천 및 검문 범위','']
    for x in o['primary_support']['college_raw']:s.append(f"- [{x['url'].split('/')[2]}]({x['url']}): raw `{x['raw_sha256']}` / `{x['path']}`")
    s += [f"- [NBA 원 지명 결과](https://www.nba.com/news/2023-nba-draft-order): indexed 관측 MIA18/GSW19/POR23만. direct HTTP403은 본문 근거0.",
        f"- [2023 CBA]({CBA_URL}): raw `{CBA_SHA}` / `{CBA}`; PDF31–33·90·243·263·314·316–317·323·631 원문 직접 대조. page.get_text UTF8 원문 SHA와 저장 파일 LF SHA를 구분한다.",
        f"- failed raw {len(o['primary_support']['failed_raw_not_body'])}개(프로필3, SCU기사404, NBA결과403)와 raw200 학교3개 구분. SCU기사 과거 web 관측/이번 재열기 timeout은 raw200인증이 아니다.",
        '- 함수 `evaluate(scale[4], minimum[4], alpha)`는 법정 가격 범위/4년차 연동을 계산한다. source physical parser 대조와 반환 candidate/RSC/primary metadata caller guard 포함. 네 번째 scale 입력은 독립 가격이 아니라 s3×767/500과 정확히 같아야 한다. 작성자 자체 음성은 독립 검문으로 세지 않는다.',
        '- 첫 생성 전 ROUTINE 옛 b78a8217… pin은 stale로 거부됐다. root가 동결한9a4f6db2…와 신규 peer e9bfc369…를 새 입력으로 대조했다. 실패 출력의 현재성 세탁0; 조상 constructor 재실행0.',
        '', '## 현행 프로젝트 인계','', '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md) / [현행 기능 등록](../control/G13_FINAL_FUNCTION_REGISTER.md). 본 leaf 한정 비교·계약 함수 준비만 완료.','',
        '| 행 | 상태 |','|---|---|','| 1 드래프트2020 | 완료 보존 |','| 2 Chicago2020–21 | 완료 보존 |',
        '| 3 거래·계약2021–23 | 진행: 이번 rookie 비교; 최종 선택/후속 비용 남음 |','| 4 장기 커리어 | 미완료 |','| 5 결말·전체 구조 | 미완료; 현행 누적 등록기 참조 |',
        '| 6 집필 규격·Pack | 전체 미완료 / Pack0 |','| 7 통합·독립·작가 승인 | 전체 미완료 |','',
        '미완료 큰묶음5 / 6번까지4 · v0.30 PARTIAL · CLOSED · manuscript0. 현행 parent/canon/원장/Git 수정0.','']
    return '\n'.join(s)

def validate(o,root=ROOT):
    return [] if o == build(root) else ['Saved candidate family differs from current expected']

def self_test(root=ROOT):
    global candidates, scale_family, sources, draft_selection_event, primary_support
    c,s,l=candidates,scale_family,sources
    cases=[]
    def run(label, target, mutate):
        global candidates,scale_family,sources
        if target=='c':
            def bad():
                v=c();mutate(v);return v
            candidates=bad
        elif target=='s':
            def bad():
                v=s();mutate(v);return v
            scale_family=bad
        else:
            def bad(r):
                v=l(r);mutate(v);return v
            sources=bad
        try:
            try:build(root)
            except AssertionError:cases.append(label);return
            raise RuntimeError('FALSE_PASS '+label)
        finally:candidates,scale_family,sources=c,s,l
    run('RECOMMENDED_PLAYER_ORIGINAL_OWNER_SUBSTITUTION','c',lambda v:v[0].update(historical_team='CHI'))
    run('CORE_MINUTE_INVASION','c',lambda v:v[0]['minute_delta_comparison_only'].update(Protagonist=-6))
    run('OPTIONS_PREEXERCISED','s',lambda v:v.update(future_options_exercised=True))
    run('LOADED_14STD_SLOT_OPTIMISM','l',lambda v:v[ROUTINE]['dated_states'][2].update(STD_count=13))
    try:evaluate([100]*4,[1]*4,Fraction(121,100))
    except AssertionError:cases.append('TYPED_SCALE_121_PERCENT')
    else:raise RuntimeError('FALSE_PASS typed price upper')
    e = draft_selection_event
    def bad_event():
        v=e();v.update(STD=14,TW=0,projection_is_June22_current_registration=True);return v
    draft_selection_event=bad_event
    try:
        try:build(root)
        except AssertionError:cases.append('JUNE22_FUTURE_REGISTRATION_COPIED')
        else:raise RuntimeError('FALSE_PASS June22 future registration')
    finally:draft_selection_event=e
    primary = primary_support
    def bad_primary():
        v=primary();v['college_raw'][0]['raw_sha256']='0'*64;return v
    primary_support=bad_primary
    try:
        try:build(root)
        except AssertionError:cases.append('RETURNED_PRIMARY_RAW_SHA_SUBSTITUTION')
        else:raise RuntimeError('FALSE_PASS primary raw metadata')
    finally:primary_support=primary
    try:evaluate([100,105,110,1000],[1]*4,1)
    except AssertionError:cases.append('YEAR4_INDEPENDENT_PRICE_SUBSTITUTION')
    else:raise RuntimeError('FALSE_PASS Year4 scale linkage')
    assert evaluate([100,105,110,Fraction(110)*Fraction(767,500)],[1]*4,1)['current_base_exact'][3] == str(Fraction(110)*Fraction(767,500))
    return cases

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    o=build()
    if a.write:
        (ROOT/OUTPUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (ROOT/MD).write_text(render(o),encoding='utf-8')
    if a.check:
        assert not validate(json.loads(text(ROOT/OUTPUT)))
        assert text(ROOT/MD)==render(o),'MD stale'
    if a.self_test:print(json.dumps({'self_negative_rejected':self_test()},ensure_ascii=False))
    print(json.dumps({'current':True,'candidate_count':3,'recommended':'J16','selected':False,'STD_after_conditional_RSC':15,'price_cents':None}))
