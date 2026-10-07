"""A finite G1 operating family; no landing/financial/actual-consent promotion."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import argparse, hashlib, json, re
import fitz
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_gsw_g1_option3_ny_working_execution.py'
OUT = 'simulation/GSW_G1_OPTION3_NY_WORKING_EXECUTION.json'
MD = OUT[:-5] + '.md'
BASELINE = '75a1d526e78ef53fbf3e72fa7cad8899a57debf9'
PINS = {
 'AGENTS.md':'67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2',
 'control/AUTHORITY_MAP.md':'693ee88e93614a1bcaa470747f7986d267b6a35ec3bffd95aaff5e6467eaf4c1',
 'simulation/GSW_HUTCHISON_2018_2021_OPERATING_CANDIDATES.json':'8bf812b411ce61592d7221f91954479f596062cf7b501ca78292ebf9ce5e6a99',
 'research/GSW_G1_DATED_MATCHING_AND_HARDCAP_SCOPE_2026_10_07.json':'4cbff2683a696271321637564b61c2563e17eb10757e1ffeb6691876a28bbf7e',
 'research/GSW_G1_REMAINING_APRON_COSTS_2026_10_07.json':'917c0985ae77c71c28ffa4fedaf85da8f0c9c6d3a9f835cc4db34105b17574f0',
 'simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.json':'e1590fa1c652c7c9d2f04b70fba5453e62aac49531a104acc7aabf24f540b665',
 'simulation/NBA_2021_L2_WORKING_MINUTE_MODELS.json':'bd258f2dbb6642f7c6417b951d0c255e6b4e20f89942a74e7c4b35f2945f7f07',
 'simulation/NBA_2021_L2_NONPLAYOFF_ROSTER_SCOPE.json':'d0b61b0468b6388dcf8073d1b0d025bd866196a2cec25a0cce2099e9a53cb448',
}
TEMP = Path('C:/Users/Storm Credit/AppData/Local/Temp')
RAW = {
 'EVANS':(TEMP/'first-rebound-gsw-g1-followthrough-20261007/EVANS_CONTRACT.html','d92d03b42b0e291b93f90f8aa4a6d50bd80d5d1897ae6b074d70b0c2efea99af'),
 'DAVIS':(TEMP/'first-rebound-gsw-g1-followthrough-20261007/DAVIS_CONTRACT.html','e84b00438ed646575a478f1e45c75fc3ece84eca371325478c652b94554d9cfb'),
 'SPELLMAN':(TEMP/'first-rebound-gsw-g1-matching-20261007/SPELLMAN.html','21a830fae7ad38ec82a81ac8b575ce500f45a8861e30a03281bd6062db92342d'),
 'NBA_FEED':(TEMP/'fr-nba-player-movement-2026-10-04.json','3d9d7a6dd7ccd39ddfdd1799a26ef9901b44682d85a26f05239b468a8ae92e3a'),
 'CBA':(TEMP/'fr-2017-cba.pdf','66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'),
 'GSW_GUIDE':(TEMP/'first-rebound-gsw-hutchison-20261007/GSW_2324.pdf','1f229c48c478e78079a7c47ba1b9e0baa69f7867a1cfa8ff9c8185bca12dfd45'),
 'MIN_RELEASE_FAILED':(TEMP/'first-rebound-gsw-g1-followthrough-20261007/MIN_DAVIS_RELEASE.html','4180868531f8f9fbabc405468e7824aebabe4221c83983384d4e5d0d4807ae66'),
 'MIN_GUIDE':(TEMP/'first-rebound-gsw-g1-followthrough-20261007/MIN_2020_21_GUIDE.pdf','ac89b1241bf211c9ebed75c56a60f19a0e12c3aca516e827d960a596bf64568f'),
 'NBA_SCALE_2018':(TEMP/'first-rebound-gsw-hutchison-20261007/NBA_2018_19_CBA101.pdf','c5ce40b61ae6287afaf173d067b6eb20eee72a58a9dc3d24552c1a424dafb213'),
}
def norm(p): return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p): return hashlib.sha256(norm(p).encode()).hexdigest()
def load(f): return json.loads(norm(ROOT/f))
def money(s): return int(re.search(r'\$([\d,]+)',s).group(1).replace(',',''))
def salary_row(name, season):
    soup=BeautifulSoup(RAW[name][0].read_bytes(),'html.parser')
    for tab in soup.find_all('table'):
        rows=[[c.get_text(' ',strip=True) for c in tr.find_all(['td','th'])] for tr in tab.find_all('tr')]
        if rows and rows[0][:4]==['Season','Option','Option Used','Cap Hit']:
            found=[row for row in rows[1:] if row and row[0].startswith(season)]
            if found:return found[0]
    raise ValueError('contract table missing')
def build():
    for f,h in PINS.items(): assert sha(ROOT/f)==h, 'reviewed input changed: '+f
    for name,(p,h) in RAW.items(): assert hashlib.sha256(p.read_bytes()).hexdigest()==h, 'raw changed: '+name
    old=load('simulation/GSW_HUTCHISON_2018_2021_OPERATING_CANDIDATES.json')
    assert old['authority']['landing_author_locked'] is False
    g1=next(x for x in old['candidates'] if x['id']=='G1')
    assert g1['route']=='2020-02-06_HUTCHISON_TO_MIN' and not g1['author_locked']
    e1=salary_row('EVANS','2018-19');e2=salary_row('EVANS','2019-20'); e3=salary_row('EVANS','2020-21')
    s3=salary_row('SPELLMAN','2020-21'); d3=salary_row('DAVIS','2020-21')
    assert [money(e3[i]) for i in [3,4,5,6,7]]==[2017320,2017320,2017320,0,0]
    assert [money(e1[i]) for i in [3,4,5,6,7]]==[1644240,1644240,1644240,0,0]
    assert [money(e2[i]) for i in [3,4,5,6,7]]==[1925890,1925880,1925880,0,0]
    assert [money(s3[i]) for i in [3,4,5,6,7]]==[1988280,1988280,1988280,0,0]
    assert [money(d3[i]) for i in [3,4,6,7]]==[5005350,5005350,0,0]
    # Davis's malformed protection cell is positively excluded, not silently fixed.
    assert money(d3[5])==50053500
    spell,davis,upper=money(s3[4]),money(d3[4]),money(e3[4])
    lower=F(davis-100000,1)/F(5,4)-spell
    assert lower==1936000 and upper>=lower
    min_limit_low=F(5,4)*(lower+spell)+100000
    min_limit_high=F(5,4)*(upper+spell)+100000
    ny_limit=F(5,4)*davis+100000
    assert min_limit_low>=davis and ny_limit>=upper+spell
    feed=json.loads(norm(RAW['NBA_FEED'][0]))['NBA_Player_Movement']['rows']
    trade=[z for z in feed if z.get('GroupSort')=='Trade 2020010']
    expected={('ed-davis',1610612750),('omari-spellman',1610612752),('jacob-evans',1610612752),('',1610612752)}
    assert {(z['PLAYER_SLUG'],int(z['TEAM_ID'])) for z in trade}==expected
    waiver=[z for z in feed if z.get('GroupSort')=='Waive 1033884']
    assert len(waiver)==1 and waiver[0]['PLAYER_SLUG']=='jacob-evans' and int(waiver[0]['TEAM_ID'])==1610612752
    assert all(z['TRANSACTION_DATE']=='2020-11-24T00:00:00' for z in trade)
    assert waiver[0]['TRANSACTION_DATE']=='2020-12-09T00:00:00'
    with fitz.open(RAW['MIN_GUIDE'][0]) as pdf:
        min_text=pdf[227].get_text().replace('\r\n','\n').replace('\r','\n')
        assert '2026 Second Round Pick' in min_text and 'NOVEMBER 24 Acquired Ed Davis' in min_text
        min_sha=hashlib.sha256(min_text.encode()).hexdigest()
    with fitz.open(RAW['NBA_SCALE_2018'][0]) as pdf:
        scale_pages={str(n):hashlib.sha256(pdf[n-1].get_text().replace('\r\n','\n').replace('\r','\n').encode()).hexdigest() for n in [29,30]}
        assert '1,663,861' in pdf[29].get_text()
    # Original waiver source observes the full current dead row: no paid/payable erasure.
    soup=BeautifulSoup(RAW['EVANS'][0].read_bytes(),'html.parser')
    dead_tables=[t for t in soup.find_all('table') if t.get_text(' ',strip=True).startswith('SEASON BASE SALARY CAP HIT') and '2020-21' in t.get_text()]
    assert len(dead_tables)==1
    dr=[[c.get_text(' ',strip=True) for c in tr.find_all(['td','th'])] for tr in dead_tables[0].find_all('tr')]
    deadrow=next(z for z in dr if z and z[0]=='2020-21')
    assert money(deadrow[-2])==upper and money(deadrow[-1])==upper
    with fitz.open(RAW['CBA'][0]) as pdf:
        pages={str(n):hashlib.sha256(pdf[n-1].get_text().replace('\r\n','\n').replace('\r','\n').encode()).hexdigest() for n in [27,35,54,55,184,185,202,206,208,212,233,234,240,241,252,254,292,294,295]}
        assert 'one hundred twenty-five percent' in pdf[233].get_text()
        assert 'waiver procedure' in pdf[201].get_text()
        assert 'October 31' in pdf[291].get_text()
    reg=load('simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.json')['team_games']
    assert len(reg)==2160
    # Only Hutchison is the transported actor; Portland Jacob Evans is separate.
    positives=[{'event_id':x['event_id'],'team':x['team'],'seconds':v} for x in reg for n,v in x['player_seconds'].items() if n=='Chandler Hutchison' and v>0]
    assert positives==[]
    l2=load('simulation/NBA_2021_L2_WORKING_MINUTE_MODELS.json')['games']
    current={g['event_id']:g['teams']['GSW'] for g in l2 if 'GSW' in g['teams']}
    assert current==old['preserved_l2_gsw_team_inputs'] and len(current)==2
    for x in current.values(): assert sum(x['player_seconds'].values())==14400 and 'Chandler Hutchison' not in x['player_seconds']
    davis_games=[x['event_id'] for x in reg if x['team']=='MIN' and x['player_seconds'].get('Ed Davis',0)>0]
    assert len(davis_games)==23
    return {
      'status':'SELECTED_ROUTINE_G1_OPTION3_NY_EXECUTION_FAMILY_INDEPENDENT_REVIEWED',
      'baseline_main':BASELINE,'source_hash_method':'UTF8_BOM_STRIPPED_CRLF_CR_TO_LF; external raw unchanged',
      'source_sha256':{**PINS,SELF:sha(ROOT/SELF)},
      'raw_sources':{k:{'cache_path':str(p),'raw_sha256':h,'adopted':k!='MIN_RELEASE_FAILED'} for k,(p,h) in RAW.items()},
      'CBA_pdf_page_text_sha256':pages,'page_text_method':'PyMuPDF get_text(), LF normalized UTF8',
      'NBA_2018_scale_pdf_page_text_sha256':scale_pages,
      'historical_sources':{'MIN_NY_trade':trade,'NY_Evans_waiver':waiver,'MIN_release_web_search_verified_url':'https://www.nba.com/timberwolves/news/minnesota-timberwolves-acquire-ed-davis-new-york','MIN_release_raw_http403_not_evidence':True,'MIN_guide':{'url':'https://cdn.wolveslynx.com/timberwolves/communications/guides/2020-21_Wolves-MediaGuide.pdf','PDF_page':228,'text_sha256_LF':min_sha,'MIN_2026_second_original_outgoing_named_claim':True,'2024_second_Rubio_event_not_same_object':True,'future_2026_protection_or_delivery_selected':None,'all_private_claims_absence_certified':False}},
      'original_contract_observations':{'Evans_year1':e1,'Evans_year2':e2,'Evans_year3':e3,'Spellman_year3':s3,'Davis_current':d3,'Davis_protected_50053500_rejected_as_malformed':True,'Evans_year2_cap_base_difference_10_not_copied':True,'publisher_inputs_are_not_league_contract_memos':True},
      'authority':{'classification':'ROOT_SELECTED_ROUTINE_OPERATING_FAMILY_WITHIN_CONDITIONAL_GSW28_WORKING_LANDING','root_working_selection':True,'selection_basis':'Parent explicit selection after independent Codex source/semantic review, 2026-10-07; AGENTS autonomous routine implementation','landing_author_locked':False,'exact_landing_HOLD_preserved':True,'recommendation_author_locked':False,'new_financial_cent_selected':None,'actual_H_contract_or_waiver_certified':False,'root_adoption_required_for_operating_model':False,'consequential_direction_changed':False},
      'operating_events':[
        {'event':'2018_START_ROOKIE_CONTRACT','season':'2018-19','pick':28,'exact_date':None,'two_guaranteed_seasons':True,'no_extra_incentive_signing_or_assignment_bonus_in_constructed_family':True},
        {'event':'THIRD_OPTION_EXERCISE','model_deadline':'2019-10-31','exact_notice_time':None,'actual_exercise_certified':False},
        {'event':'G1_MIN_TRADE','working_date':'2020-02-06','outgoing':['D\u0027Angelo Russell','Omari Spellman','Chandler Hutchison'],'incoming_GSW':['Andrew Wiggins'],'existing_named_2021_first_second_objects_unchanged':True,'actual_acceptance':None},
        {'event':'MIN_NY_DAVIS_TRADE','working_date':'2020-11-24','MIN_outgoing':['Chandler Hutchison','Omari Spellman','MIN_2026_2R_named_original_claim'],'MIN_incoming':['Ed Davis'],'actual_acceptance':None},
        {'event':'NY_WORKING_WAIVER','working_date':'2020-12-09','waiver_completion_exact_time':None,'working_completion_condition':'cleared before 2020-12-22 opening; modeled routine administrative trace, not actual receipt','fourth_option_exercised':False,'fourth_option_nonexercise_is_explicit_working_decision_not_automatic_historical_copy':True,'fourth_option_2020_adjusted_deadline_exact':None,'full_current_protected_salary_retained':True,'future_unexercised_option_paid':False,'stretch':False,'new_setoff_or_claimant':None,'postwaiver_FA_class':'I1(cc)(iii) waived Veteran, not I1(hhhh) completed-contract Veteran Free Agent; VII4(a)(2) VFA hold does not replace or add to full current dead charge','NY_FA_rights_renunciation_required_for_this_waiver':False,'actual_renunciation_notice':None}
      ],
      'constructed_financial_family':{
        'years1_2':'max((4/5)*S_y, applicable II6 minimum_y) <= H_y <= min((6/5)*S_y, E_y_base, E_y_cap); same lawful original #28/2018-start scale',
        'years1_2_cap_comparison_upper':[min(money(e1[3]),money(e1[4])),min(money(e2[3]),money(e2[4]))],
        'year3_H_interval':[int(lower),upper],'year3_exact_H_salary':None,
        'year3_floor_support':'Original same-pick same-start fully protected no-incentive E3 is a valid 120% reference; H3 may equal E3, so family nonempty without invented operative scale rounding.',
        'year3_scale_public_source':'NBA CBA1012018 PDF29 #28 thirdyear display1681.1 in $000s; conservative magnitude1m–2m as in prior reviewed matching model;80%upper1.6m<familylower1.936m; exact operative dollar rounding null',
        'minimum_player_salary':'II6 PDF54/55 applies independently of rookie80%; years1/2 intersect applicable minimum, not all80%contracts lawful. Same-start/YOS original E supplies a legal nonempty endpoint. NBA2018 CBA101 PDF30 YOS0–2 published floors below1.936m, so selected year3 matching floor is above the applicable minimum.',
        'not_all_80_to_120_percent_year3_contracts_certified':True,
        'all_current_protection':True,'H_extra_bonus':0,'zero_bonus_is_constructed_contract_not_actual_absence_cert':True,
        'NY_current_dead_charge_interval':[int(lower),upper],'original_NY_observed_full_current_dead_row':deadrow,'NY_dead_charge_zero':False,'future_year4_option_charge':0,
        'private_common_cost_Gamma_preserved_not_set_zero':True,
        'cap_transport_relation':'For each existing feasible original common-cost realization Gamma(t), replace live/dead original E component with H<=E; Gamma+H<=Gamma+E. Before G1, GSW current cost cannot rise; G1 unchanged incoming/public actions; afterward GSW H charge absent. MIN H live current component and NY full protected dead component likewise cannot rise. This scalar cost relation does not assert all arbitrary Gamma are feasible or actual bonus outcomes unchanged.',
        'original_feasible_realization_anchor':'Official GSW guide completed original 2018 #28 signing /2019 Russell S&T /2020 G1 plus NBA completed MIN-NY and NY waiver; preserve named common events and current cost components, not actual H facts.',
        'whole_counterfactual_private_financial_trace_certified':False,
        'public_cost_residual_X_value':None,'existing_GSW_B_intervals_and_X_thresholds_not_discarded':True,
        'GSW_existing_deadmoney_preserved':'Livingston and Chriss etc untouched; new H waiver does not erase NY protected charge',
      },
      'matching_Nov24':{'universal_tax125_used_no_MIN_tax_assumption':True,'MIN_incoming_Davis':davis,'Spellman_outgoing':spell,'H3_lower':int(lower),'H3_upper':upper,'MIN_limit_at_lower':int(min_limit_low),'MIN_limit_at_upper':int(min_limit_high),'MIN_slack_interval':[int(min_limit_low-davis),int(min_limit_high-davis)],'NY_outgoing_Davis':davis,'NY_incoming_upper':upper+spell,'NY_limit':float(ny_limit),'NY_slack_lower':float(ny_limit-upper-spell),'both_contracts_MIN_since_Feb6_more_than_two_months':True,'NY_Davis_recent_acquisition_not_aggregated_with_other_outgoing_contract':True,'prior_G1_matching_reused_source':'research/GSW_G1_DATED_MATCHING_AND_HARDCAP_SCOPE_2026_10_07.json'},
      'minute_and_roster_effects':{'regular_team_games_read':2160,'positive_Hutchison_rows':positives,'MIN_Ed_Davis_positive_games_preserved':davis_games,'GSW_L2_objects':current,'GSW_May_standard':g1['may_standard'],'GSW_May_two_way':g1['may_two_way'],'GSW_May_standard_count':15,'GSW_May_two_way_count':2,'regular_or_L2_vectors_changed':0,'new_H_health_certificate':None,'Portland_Jacob_Evans_not_this_outgoing_actor':True,'full_actual_registration_certified':False},
      'rejected_N3_nonexercise_expiry':{'reason':'Removing H outgoing current salary can prevent MIN acquisition of Ed Davis; 23 selected positive Davis games require a live downstream trade bridge. Do not automatically copy expired H to NY waiver.','permanent_permission_barrier':False},
      'scope':{'whole_legal_PASS_added':0,'REGISTER_changed':False,'source_supported_operating_family_valid_for_review':True,'all_other_team_financial_history_certified':False,'minimum_team_salary_shortfall_automatic_erasure':False,'minimum_team_salary_rule_obligation_preserved_not_spending_exemption':True,'actual_consent':None,'actual_cents':None,'actual_landing':None,'season_recomputed':False,'manuscript_count':0,'actual_Pack_count':0,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_gate':'CLOSED'},
      'independent_review_complete':True,
      'independent_review':{'reviewer':'/root/chi_salary_domain','scope':'whole public operating family, not actual whole private financial trace','direct_sources':'raw6 SHA; MINguide228; NBA2018 scale29/30; CBA12pages','output_mutations_rejected':['restore_year4_charge','change_MIN2026_to2024'],'substantial_remaining_defect':0,'root_independent_endpoint_neighbor_and_three_output_controls_accepted':True,'Claude_analysis_completed':False,'whole_G16_closed':False}
    }
def validate(x):
    assert x==build(), 'saved witness differs from complete source reconstruction'
    return True
def markdown(x):
    m=x['matching_Nov24']
    return '\n'.join([
      '# GSW G1: 3년차 옵션·MIN→NY·보호 급여를 잇는 운영 구현 가족', '',
      '**Root selected routine working family / independent Codex review accepted.** 2026-10-07 부모가 직접 독립 검문 뒤 현재 conditional GSW28 baseline 안의 이 운영 가족을 선택했다. 기존 Golden State 28순위 working 착지의 `NOT_LOCKED / EXACT_LANDING_HOLD`, 실제 금액·통지·수락 null은 보존한다. 원장·중앙 파일 변경0.', '',
      '## 다음 실행 단위', '',
      '2018-start #28 rookie 계약 → 2019년 기한 내 3년차 옵션 행사 → 2020-02-06 G1 MIN 양도 → 2020-11-24 H/Spellman/기존 MIN2026 2R와 Ed Davis 교환 → 2020-12-09 NY 작업 waiver, 4년차 옵션 **명시적 미행사**. 실제 통지·승낙·정확 지급액·waiver 완료시각은 null이다. 2020 조정된 옵션 기한을 보통 October31로 오기하지 않는다. 개막 전 waiver 완료를 운영 조건으로 둔다. CBA I1(cc)(iii)/I1(hhhh)/VII4(a)(2): waived Veteran과 계약을 마친 Veteran Free Agent가 달라 이 waiver에 만료 VFA hold/renounce를 잘못 덧붙이지 않는다. 현재 protected dead salary는 유지한다. H와 Portland의 Jacob Evans는 다른 선수이며 실제 Evans의 미래를 자동 복사하지 않는다.', '',
      'N3(옵션 미행사·2020 만료)는 추천에서 제외: MIN의 Davis 거래 outgoing 급여를 없애므로 비용 감소만으로 matching이 보존되지 않는다. Davis 양수 출전23경기를 보존하는 위 경로를 선택 가능한 최소 운영안으로 제시한다.', '',
      '## 공개 입력·두 팀 matching', '',
      f'- 원 Davis 당해 base/cap {m["MIN_incoming_Davis"]:,}; 원 Spellman {m["Spellman_outgoing"]:,}. 새 H 당해 합법 가족은 {m["H3_lower"]:,}–{m["H3_upper"]:,}이며 그중 실제 급여는 선택하지 않았다.',
      f'- MIN: 과세 여부에 상관없이 125%+100,000 한도로 최소 {m["MIN_limit_at_lower"]:,}, 여유 0–{m["MIN_slack_interval"][1]:,}. NY: 한도 {m["NY_limit"]:,.1f}, incoming 최대 {m["NY_incoming_upper"]:,}, 여유 {m["NY_slack_lower"]:,.1f}.',
      '- 모든 80–120% 계약을 통과시킨 것이 아니다. 동일 #28/2018-start의 원 year3 상한이 비공허 구성 증인이다. 원 2019–20 Evans cap/base 10달러 차이와 Davis 보장열 50,053,500은 H 금액/보장 사실로 채택하지 않는다.', '',
      '## CBA와 비용', '',
      '직접 읽은 2017 CBA PDF292/294/295: two seasons/options, scale 80–120%, 보호 급여, bonus 한도. PDF233/234: 동시 합산·125%+100,000·2개월 제한. PDF202: waiver 뒤 paid/payable 급여도 Team Salary에 포함. PDF240/241/254: apron 조정 및 S&T 이후 연속 상한.', '',
      '원 lawful financial realization의 공통 비용 Γ(t)를 같은 모델 안에서 보존하고 H≤E로 구성하면 Γ+H≤Γ+E이다. 이는 실제 H의 원계약·모든 미래 성과급·모든 private 장부를 인증하거나 모든 임의 Γ를 합법으로 정의하는 증명이 아니다. 원 public cost interval과 미확인 X를 삭제하거나 X=0으로 만들지 않는다. NY 현재 protected dead charge도 H 전액을 유지하고 stretch/setoff/claiming-team을 만들지 않는다. years1/2는 rookie80% 외 II6 최저급여도 교집합으로 적용하고 상한은 min(Ebase,Ecap,120%scale)로 둔다. 독립 source/의미 검문과 root 직접 Fraction·현재성 검문 뒤 이 한정 운영 가족이 채택됐다.', '',
      '[MIN 공식 거래](https://www.nba.com/timberwolves/news/minnesota-timberwolves-acquire-ed-davis-new-york)는 web indexed 본문 확인. 직접 다운로드403 raw는 증거로 제외했다. 새 [MIN 2020–21 공식 guide](https://cdn.wolveslynx.com/timberwolves/communications/guides/2020-21_Wolves-MediaGuide.pdf) PDF228 원문에서 MIN2026 2R를 포함한 교환을 직접 확인했고, Rubio의 별도2024 2R와 구분한다. NBA frozen feed의 Trade2020010/Waive1033884와 원 Evans full2020–21 dead row도 대조했다. SS는 자체 편집 공개 입력이며 league memo가 아니다.', '',
      '## 출전·등록 영향', '',
      '현재 정규2160 팀게임 중 Hutchison 양수0; MIN Davis 양수23게임 유지. GSW 두 L2 전체 객체 동일·각14,400초·8명 보존. GSW May standard15/TW2 보존. 이는 actual 전체 등록·의료 인증이 아니다. 이전 두 후보와 중앙 파일을 수정하지 않았다.', '',
      '## 독립 검문', '',
      'Codex chi: 원raw6·MINguide228·NBA표29/30·CBA12쪽 및 code/MD/수학을 직접 대조, year4 charge 복구와 MIN2026→2024 변조 거부. Root: Fraction 양끝·최저보다1달러 낮은 값·min(base,cap) 및 NY charge/지명권/옵션 변조 거부. 실질 남은 결함0. [Claude 실행 기록](../reviews/GSW_G1_OPTION3_NY_CLAUDE_BLIND_2026_10_07.md)은 선택 전 입력의55.0548초 timeout·분석0을 보존하며 현재 선택/최저급여 교집합 등의 후속 수리와 구분한다. 전체G16 승격0.', '',
      '## 전체 진행', '',
      '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 이 leaf의 완료와 전체 작업 완료를 구분한다.', '',
      '| 번호 | 현재 범위 |', '|---|---|',
      '|1|2020 드래프트 연쇄 완료|', '|2|Chicago2020–21 법적12/12; A/K 전체 종료 검문·named 운영 경로 진행|',
      '|3|2021–23 승인 방향·후속 정확 실행 진행|', '|4|장기 커리어 선행 시즌 결산 연결 대기|',
      '|5|전체 구조 골격; 회차 기능표 진행|', '|6|집필 규격·Context Pack 기능13/780, 미배치767|', '|7|통합·독립·최종 작가 승인 대기|', '',
      '**미완료 큰 묶음6. v0.30 PARTIAL / 설계·원고 CLOSED / 원고0 / 실제Pack0.**', ''
    ])
def self_test():
    x=build(); mutations=[]
    for label,fn in [
      ('expired_contract_restored_to_NY',lambda y:y['operating_events'][1].update(event='THIRD_OPTION_NOT_EXERCISED')),
      ('wrong_incoming_actor',lambda y:y['operating_events'][3].update(MIN_incoming=['Andre Drummond'])),
      ('dead_salary_erased',lambda y:y['constructed_financial_family'].update(NY_dead_charge_zero=True)),
      ('salary_below_matching_floor',lambda y:y['matching_Nov24'].update(H3_lower=1900000)),
      ('actual_landing_promoted',lambda y:y['authority'].update(landing_author_locked=True)),
      ('source_positive_minutes_changed',lambda y:y['minute_and_roster_effects']['GSW_L2_objects']['2021-05-19_POR_GSW']['player_seconds'].update({'Chandler Hutchison':1})),
    ]:
      y=deepcopy(x);fn(y)
      try:validate(y)
      except AssertionError:mutations.append(label)
      else:raise AssertionError('false PASS: '+label)
    return mutations
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');args=a.parse_args()
    x=build()
    if args.write:
      (ROOT/OUT).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(x),encoding='utf-8')
    if args.check:validate(load(OUT));assert norm(ROOT/MD)==markdown(x);print('current/full reconstruction PASS')
    if args.self_test:print(json.dumps(self_test(),ensure_ascii=False))
