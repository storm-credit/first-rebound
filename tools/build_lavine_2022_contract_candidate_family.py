"""Existing LaVine budget -> consensual Bird legal-form candidate, not selection."""
import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import fitz
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_lavine_2022_contract_candidate_family.py'
OUT='research/LAVINE_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07.json'
MD=OUT[:-5]+'.md'
BASELINE='d0474a0cd15c4fea9b8041270e36ae20df969d67'
LONG='simulation/CHICAGO_LONG_CORE_CBA_INPUTS.json'
CONT='simulation/CHICAGO_2021_23_CONTINUATION_INPUTS.json'
SUMMER='simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json'
PINS={'simulation/CHICAGO_LONG_CORE_CBA_INPUTS.json':'7985e65cb5e184356aead888d4f016aca187dd2dd3185ea6de76527a6937fe0c','research/CHICAGO_LONG_CORE_CBA_SOURCES.json':'071c15eef691277c76075b933b655b2e12e3a46dc6d3061816f51dec568bbdf2','simulation/CHICAGO_2021_23_CONTINUATION_INPUTS.json':'5632957e5e0a02f2d6f241900a3bef2c5790a8993c3494986e383ca3cbff1be3','research/CHICAGO_2021_23_CONTINUATION_SOURCES.json':'4dc3cfb7416174c0fea5c2710e9915a729d362dc553f216f4e9c861b373e9db3','simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json':'11140e49baa665f18e267fa6419efa238302250b724fa51cfd3262b010b4a312','canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json':'253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088','canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json':'9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce','AGENTS.md':'67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2'}
CBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
PAGES=[29,30,36,37,38,40,44,54,55,57,58,64,65,193,194,195,196,206,208,218,219,223,240,241,252,253,257,299,334,335,336,398,399,561]
RAW=[{'id':'SS_LAVINE_REUSED','url':'https://www.salaryswish.com/players/zach-lavine','cache_path':'C:/Users/Storm Credit/AppData/Local/Temp/fr-chi-2021-retained-zach-lavine-20261007.html','raw_sha256':'1525dc4eeff64c5b25ab04b327dd78f2a3b96493f11e6efb1fd31a1faec0bb0a','classification':'SECONDARY_CONTRACT_HISTORY_BODY_DIRECT_READ; CURRENT_2026_CAP_NOT_2022_BASE'}, {'id':'NBA_CAP2022_REUSED','url':'https://pr.nba.com/nba-salary-cap-2022-23-season/','cache_path':'C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-chi-core2022-20261007/NBA_CAP2022.html','raw_sha256':'2e76093cfc91b6257f18cddd25441090118f36bd8a942259fbc340438ff5e57f','classification':'PRIMARY_NBA_RELEASE_DIRECT_BODY_READ'}]
FAILED={'url':'https://www.nba.com/bulls/news/bulls-re-sign-zach-lavine','http_status':403,'cache_path':'C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-lavine-contract-20261007/BULLS_LAVINE2022.html','raw_sha256':'81a811c1a63a9bee30d009e3e3e854009f6f339a0ed8a39b061f0781fa1862a7','bytes':425,'body_used':False,'repeat_attempts':0,'web_search_original_body_recovered':True,'web_direct_open_rendered_original_body':False,'classification':'FAILED_DIRECT_HTTP; SEARCH_INDEX_ORIGINAL_TEAM_BODY_SEPARATE'}
SCHEDULE=[37096500,40064220,43031940,45999660,48967380]

def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))

def terms():
    return {'mechanism':'NEW_DIRECT_FULL_BIRD_WITH_PRIOR_CHICAGO_NOT_EXTENSION_OR_SIGN_AND_TRADE','signing_candidate_ET':'2022-07-07T12:00:00-04:00','first_contract_cap_year':2022,'last_stated_term_cap_year':2025,'one_player_option_cap_year':2026,'salary':SCHEDULE.copy(),'regular_salary_equals_base':True,'skill_and_injury_protection_percent':100,'other_standard_CBA_protection_conditions_preserved':True,'option_termination_protection':'XII2a_A; OPTION_PROTECTION_AS_IF_EXERCISED_IF_TEAM_TERMINATES_BEFORE_EXERCISE','option_exercisable_once':True,'option_individually_conditioned':False,'contractual_option_notice_deadline':'2026-06-29','option_exercise_selected':None,'option_notice_actual':None,'ETO':False,'team_option':False,'signing_bonus':0,'performance_bonus':0,'physical_condition_academic_or_extra_promotion_bonus':0,'loan_or_international_payment':0,'trade_Exhibit4_rate_family':['0','3/20'],'actual_trade_Exhibit4_rate':None,'new_contract_or_amount_selected':False,'actual_consents_and_receipts':None}

def check_terms(t):
    assert t['mechanism']=='NEW_DIRECT_FULL_BIRD_WITH_PRIOR_CHICAGO_NOT_EXTENSION_OR_SIGN_AND_TRADE','Contract mechanism changed'
    assert t['salary']==SCHEDULE and len(t['salary'])==5 and sum(t['salary'])==215159700,'Reference budget changed'
    assert t['signing_candidate_ET']=='2022-07-07T12:00:00-04:00' and [t[k]for k in ['first_contract_cap_year','last_stated_term_cap_year','one_player_option_cap_year']]==[2022,2025,2026]
    assert t['regular_salary_equals_base']is True and t['skill_and_injury_protection_percent']==100 and t['other_standard_CBA_protection_conditions_preserved']is True
    assert t['option_termination_protection']=='XII2a_A; OPTION_PROTECTION_AS_IF_EXERCISED_IF_TEAM_TERMINATES_BEFORE_EXERCISE','Required option termination clause changed'
    assert t['option_exercisable_once']is True and t['option_individually_conditioned']is False
    assert t['contractual_option_notice_deadline']=='2026-06-29' and t['option_exercise_selected']is None and t['option_notice_actual']is None
    assert all(t[k]is False for k in ['ETO','team_option','new_contract_or_amount_selected'])
    assert all(t[k]==0 for k in ['signing_bonus','performance_bonus','physical_condition_academic_or_extra_promotion_bonus','loan_or_international_payment'])
    assert t['trade_Exhibit4_rate_family']==['0','3/20'] and t['actual_trade_Exhibit4_rate']is None and t['actual_consents_and_receipts']is None
    assert SCHEDULE[-1]>=SCHEDULE[-2] and all(Fraction(b-a)==Fraction(SCHEDULE[0]*8,100)for a,b in zip(SCHEDULE,SCHEDULE[1:]))

def sources():
    for p,h in PINS.items():assert sha(p)==h,'Unreviewed source '+p
    l=load(LONG);c=load(CONT);s=load(SUMMER)
    assert l['LaVine_2022_reference_base']==SCHEDULE and l['LaVine_2026_player_option']is True
    assert l['LaVine_real_world_trade_kicker_not_imported']==[1500000,1500000] and l['LaVine_new_contract_target_percent_after_opt_out']==18
    assert l['author_locked']is False and l['exact_execution_cleared']is False,'Comparison upgraded to lock'
    assert c['salary_reference_2021_2022']['LaVine']==[19500000,37096500] and c['cap2022']==123655000
    assert s['standard_roster_working'][0]['player']=='LaVine','Prior retained identity changed'
    assert load('canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json')['selected']['route']=='G1A_PLUS_M1'
    raw=[]
    for r in RAW:
        b=Path(r['cache_path']).read_bytes();assert hashlib.sha256(b).hexdigest()==r['raw_sha256'];plain=BeautifulSoup(b,'html.parser').get_text(' ',strip=True)
        if r['id']=='SS_LAVINE_REUSED':
            tables=[x.get_text(' ',strip=True)for x in BeautifulSoup(b,'html.parser').find_all('table')]
            assert any(all(f'${v:,}'in t for v in SCHEDULE)for t in tables),'Reported base table missing'
            assert 'Player Yes (Jun 29, 2026)'in plain and 'Signing Method : Bird Exception' in plain and 'July 7, 2022' in plain
            assert '$3,000,000 Trade Kicker Applied'in plain
        else:assert '$123.655 million'in plain and 'noon ET on Wednesday, July 6'in plain
        raw.append({**r,'bytes':len(b),'locator':'2022 veteran table Base Salary column, not Cap Hit or later option-used/trade-payment fields'if r['id']=='SS_LAVINE_REUSED'else'NBA official June30 release opening two paragraphs'})
    assert hashlib.sha256(CBA.read_bytes()).hexdigest()==CBA_SHA
    with fitz.open(CBA)as d:
        pages=[{'PDF_1based':n,'fitz_text_LF_sha256':hashlib.sha256(d[n-1].get_text().replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()}for n in PAGES]
        assert 'at least seven (7)'in d[57].get_text() and 'thirty percent (30%)'in d[57].get_text()
        assert 'five (5)'in d[298].get_text() and 'one hundred percent (100%)'in d[333].get_text()
        assert 'but not both' in d[334].get_text() and 'prior to the June 30' in d[335].get_text()
    b=Path(FAILED['cache_path']).read_bytes();assert hashlib.sha256(b).hexdigest()==FAILED['raw_sha256'] and len(b)==FAILED['bytes']
    return raw,pages

def build():
    raw,pages=sources();t=terms();check_terms(t)
    maximum=max(Fraction(123655000*30,100),Fraction(19500000*105,100));assert maximum==SCHEDULE[0]
    stress=Fraction(2794384*123655000,99093000);min_ceiling=-(-stress.numerator//stress.denominator)+10;assert all(x>min_ceiling for x in SCHEDULE)
    stated=sum(SCHEDULE[:4]);assert stated==166192320
    return {'id':'LAVINE_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07','status':'INDEPENDENTLY_REVIEWED_EXISTING_5YEAR_CONSENSUAL_FORM_NOT_SELECTED','source_main_snapshot':BASELINE,'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8 BOM stripped; CRLF/CR toLF','raw_body_observations':raw,'failed_direct_source_attempt':FAILED,'CBA2017':{'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(CBA),'raw_sha256':CBA_SHA,'directly_read_pages':pages},
      'classification':{'historical_fact':'Bulls July7 2022 re-signing announcement; published team terms undisclosed. Only short indexed team-body paraphrase used; directHTTP403 retained separately.','secondary_report':'SalarySwish five-year base/Player2026 option/Bird/history are reference reports, not source of alternate consent.','existing_candidate':'Long-core five-year schedule preserved; 2026 opt-out plus18% new-offer branch remains a separate unselected consequential possibility.','new_lawful_form_candidate':'Mutually negotiated direct Chicago fullBird four stated years plus one unconditional player option, full skill/injury protection and XII2a(A); zero signing/performance/promotion/international bonus proposed, original Ex4 rate left in permitted0..15% family.','author_locked_here':False},
      'terms_candidate':t,'admitted_inputs':{'prior_team':'CHI','prior_contract_expiry':'2022-06-30','prior_salary_reference':19500000,'credit_YOS_range':[7,9],'reference_YOS':8,'reference_YOS_is_actual_new_world_credit_certified':False,'required_service_credit':'I1(iiii): credited Active/Inactive day, no disqualifying withholding/disapproved contract; by June30. No actualfuturemedicalreceipt gate.','Bird_condition':'Three preceding covered seasons under Chicago contracts without a disqualifying free-agent team change; approved retention plus no-new-move contract family. If changed, five-year8% prior-team form reopens.','actual_2021_22_services_or_full82_results_certified':False,'actual_Bird_status_receipt_certified':False},
      'legal_checks':{'first_salary_max':int(maximum),'first_salary_max_expression':'max(30%123655000,105%19500000);7<=YOS<10; ordinarymaximum, no designated35% award assumption','annual_raise':2967720,'raise_base':'8% of first Regular Salary, not8% compounding','term_including_option':5,'minimum_all5_seasons_conservative_comparison_ceiling':min_ceiling,'minimum_comparison_scope':'2017ExC largest Year1..5 cell10+ scaled by signing2022cap/2017cap,+10 presentation guard; far below agreed base. Exactrounding notcertified; II5/II6 legalconformity remains.','Bird_signing_open_ET':'2022-07-06T12:01:00-04:00','calendar_primary_moratorium_ends_ET':'2022-07-06T12:00:00-04:00','candidate_after_both_boundaries':True,'regular_FA_trade_no_earlier_than':'2022-12-15','if_above_cap_immediately_after_Bird_signing_and_raise_over120pct_trade_no_earlier_than':'2023-01-15','above_cap_at_signing_is_selected':False,'trade_test_scope':'VII8d2/3 first eligible date only, not actualassignment/matching or laterlegalcost certificate. OrdinaryBird retention alone is not an NTMLE/BAE/S&T hardcap trigger; wholeFY22portfolio not certified.'},
      'FY22_named_cost_states':{'before_new_agreement_if_unrenounced_UFA':{'generic_FA_amount_reference_report':29250000,'VII4d1i_150pct_or190pct_public_domain':[29250000,37050000],'generic_FA_amount_safe_upper':37050000,'apron_UFA_hold_component':0,'apron_basis':'VII6m3D excludes UFA amount only; prior accrued/other obligations are not erased.','estimated_average_threshold_and_actual_hold_selected':False},'after_new_agreement_or_execution_in_candidate_family':{'current_salary_new_contract':37096500,'new_signing_performance_or_other_bonus':0,'new_assignment_bonus_at_direct_retention':0,'generic_and_apron_new_contract_component':37096500,'prior_accrued_cost_or_other_portfolio_cost':None,'whole_team_salary_or_apron_pass':False},'generic_increment_from_reference_150pct_hold':7846500,'generic_increment_from190pct_hold':46500},
      'option_cost_branches':[{'id':'EXERCISE_2026_PO','condition':'Player voluntarily gives valid exercise notice by contractdeadline; no earliertermination/assignment changes; future applicableCBA still checked.','stated4_base':stated,'option_base_2026':SCHEDULE[-1],'full5_base':sum(SCHEDULE),'actual_exercise_or_notice':None,'future_FY26_total_cap_or_apron_certified':False},{'id':'DECLINE_2026_PO','condition':'Player timely does not exercise under applicable notice rules; contract remained alive through fourthyear and no earliertermination; new2026contract entirely separate.','stated4_base':stated,'option_base_under_this_live_UPC':0,'new2026contract_salary':None,'FA_hold_or_other_FY26_cost':None,'existing_UPC_expiry_if_option_not_exercised':'2026-06-30','actual_decline_or_new18pct_acceptance':None,'zero_UPC_base_is_zero_team_salary':False}],
      'trade_bonus_family':{'rate_closed_interval':['0','3/20'],'rate_actual':None,'first_trade_only':True,'unexercised_option_excluded_from_remaining_base':True,'initial_unearned_stated4_fullannual_outer_bound':'24928848','if_option_exercised_and_all5_unearned_fullannual_outer_bound':'32273955','outer_bounds_are_actual_payment_or_cap_allocation':False,'at_assignment':'Need earned/protected remainder, currentmax II7f and VII3b/XXIV2 legalallocation; futureapplicableCBA and fullcounterparty costs reopen. No laterhistorical$1500000/$1500000 inheritance.','rate0_member_is_automatically_selected':False,'new_signing_no_assignment_charge_from_this_new_contract':True,'prior_contract_accrued_obligations_are_erased':False},
      'remaining_named_inputs':['Chicago retention amount/term is still candidate; no re-signing consent or newauthorlock selected.','Combine LaVine with Carter/protagonist/otherFY22 obligations and completecost/roster, rather than adding only37.0965m to a partialledger.','Choose futurePO exercise or decline/newoffer only at a consequential decision; do not apply18% haircut now.','Future2023+ rulechanges/assignment/max-adjustedGamma/optionnotice procedures require dated followup, not this2022 signingform.'],
      'certification':{'independent_review_completed':True,'selected_contract':None,'actual_player_team_consent':None,'actual_private_terms_or_cents':False,'actual2026_option_exercise':None,'whole_FY22_cost':False,'whole_macro3_complete':False,'new_author_lock':False,'central_or_REGISTER_promotion':False,'manuscript_written':0}}

def validate(o):
    try:assert o==build(),'Saved output differs from current source/meaning';return []
    except (AssertionError,KeyError,ValueError,OSError)as e:return[str(e)]

def markdown(o):
    return '\n'.join(['# LaVine 2022 잔류 계약: 기존 금액의 법적 후보 형식','',o['status'],'',
      '기존 5년 기본급 $37,096,500 / $40,064,220 / $43,031,940 / $45,999,660 / $48,967,380을 보존했다. 첫해 $123,655,000 cap의30%, 첫해의8%인 $2,967,720씩 증액, 총 $215,159,700이다. 원액의 Chicago 수락과 새 작가 잠금은 선택하지 않았다.',
      '', '## 제안과 원역사 구분','',
      '구체 합의 가능한 후보는 Chicago fullBird 4년+마지막 선수옵션1년이다. 승인된 잔류 계약군과7–9YOS 서비스 조건 아래 첫해max/5년/8%를 검문한다. 2021–22 새 의료·실서비스 인증을 요구하거나 생성하지 않는다. skill/injury 전액보호·표준CBA 조건·XII2(a) A형 옵션해지 보호, 새 signing/performance/promotion/international bonus0은 이번 합의 형식의 제안이다. 실제 원계약무보너스 인증이 아니다.',
      '원 공개 [계약표](https://www.salaryswish.com/players/zach-lavine)의 Base Salary를 읽었다. 후대 Cap Hit의 $1.5m씩 trade kicker와 이미 행사 표시된2026옵션은 상속하지 않는다. 원 구단 July7 재서명 발표와 금액 미공개는 검색색인의 짧은 본문 확인이고, 직접HTTP는403/원본문미회수로 기록했다.',
      '', '## 옵션과 거래 비용','',
      '|후보|이 계약 기본급|미선택 비용|','|---|---|---|','|2026옵션 행사|첫4년166,192,320 + 옵션48,967,380 =215,159,700|실제 행사/접수·미래 전체급여 미인증|','|2026옵션 비행사|첫4년166,192,320; 살아 있던 이 UPC 옵션급여0|새 계약/FAhold 미정; 팀비용0 아님|',
      '선수 옵션의 권리·한 번 행사·급여 비감소·조건부 옵션 금지를 지킨다. 제안 notice deadline은2026-06-29이며 실제후년 적용규칙을 이2017 원문 검문으로 확정하지 않는다. 계약을 앞서 해지하면 A형 보호조건이 작동하므로 무조건 비행사=무부채로 쓰지 않는다. 18% 감액·새 계약 수락은 별도 선택이다.',
      'Exhibit4의 trade bonus율은0..15% 허용가족으로 미선택이다. 최초 양도만/미행사옵션 제외/남은base 기준 상한을 보존한다. 전4년 unearned 외곽상한24,928,848, 행사된5년 전체 외곽상한32,273,955는 실제 Γ나 cap배분이 아니다. 첫해max와 trade시 현재max 축소·earned/protected잔여·미래 CBA 검문이 필요하다. 새 직접재서명은 이 계약의 양도보너스를 발생시키는 사건이 아니다.',
      '', '## 날짜와 검문 범위','',
      '[NBA2022 공식 cap/calendar](https://pr.nba.com/nba-salary-cap-2022-23-season/)의July6 정오 moratorium 종료와2017VII6(b)의12:01 Bird창보다 뒤인July7 정오를 후보로 구성했다. FA계약 양도는 원칙Dec15, 서명후abovecap/120%초과 Bird이면Jan15가 더 늦은 경계다. 실제거래/wholematching/전체FY22비용 PASS를 뜻하지 않는다.',
      '[2017CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) I1(yy)/(iiii),II3/5/6/7(a)(ii)/(f),VII5(c)(2)/6(b)/8(d)/9,IX1,XII2–5,XXIV2 원쪽34개·성공raw2+실패raw1관측과source8+SELF를 연결했다. `python -B tools/build_lavine_2022_contract_candidate_family.py --check --self-test`는 source 및 합의형식 의미 변조를 검문한다. 외부 분석/독립 검문 성공을 미리 주장하지 않는다.',
      '', '|번호|묶음|상태|','|---|---|---|','|1|2020드래프트 연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23거래·계약|LaVine 법적형식 후보; 선택/전체비용 미완료|','|4|장기 커리어|후속시즌 입력 대기|','|5|결말·전체 구조|전체기능표 미완료|','|6|집필규격·Context Pack|현행 누적 등록기 참조·Pack0|','|7|통합·독립·작가 승인|최종CLOSED|','', '미완료 큰 묶음5 / v0.30 PARTIAL / 설계·원고CLOSED / 원고0.',''])

def self_test():
    o=build();tests=[]
    for name,fn in [('future_option_exercised',lambda x:x['certification'].update(actual2026_option_exercise=True)),('wholecost_promoted',lambda x:x['certification'].update(whole_FY22_cost=True)),('18pct_haircut',lambda x:x['terms_candidate']['salary'].__setitem__(4,22257900))]:
        q=copy.deepcopy(o);fn(q);assert validate(q),name;tests.append(name)
    for name,fn in [('same_total_wrong_annuals',lambda x:x['salary'].__setitem__(slice(0,2),[40064220,37096500])),('team_option_not_player',lambda x:x.update(team_option=True)),('wrong_option_termination_clause',lambda x:x.update(option_termination_protection='NONE')),('new_bonus_unaccounted',lambda x:x.update(performance_bonus=100000)),('extension_wrong_mechanism',lambda x:x.update(mechanism='VETERAN_EXTENSION')),('actual_gamma_selected',lambda x:x.update(actual_trade_Exhibit4_rate='3/20'))]:
        q=terms();fn(q)
        with patch(__name__+'.terms',return_value=q):
            try:build()
            except AssertionError:tests.append(name)
            else:raise AssertionError('Bad constructor accepted '+name)
    real=load;l=copy.deepcopy(load(LONG));l['LaVine_2026_player_option']=False
    with patch(__name__+'.load',side_effect=lambda p:copy.deepcopy(l)if p==LONG else real(p)):
        try:build()
        except AssertionError:tests.append('sameID_original_option_reversed')
        else:raise AssertionError('Original option reversal accepted')
    return tests

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();o=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
    if a.check:assert not validate(load(OUT));assert text(MD)==markdown(o),'Markdown stale'
    print(json.dumps({'current':True,'first_salary':37096500,'four_stated_base':166192320,'five_base':215159700,'negative_controls':self_test()if a.self_test else[]},ensure_ascii=False))
if __name__=='__main__':main()
