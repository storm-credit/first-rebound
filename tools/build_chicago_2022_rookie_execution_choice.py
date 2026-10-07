"""Two named, unselected rookie/waiver candidates; no historical contract copying."""
from __future__ import annotations
import argparse, copy, hashlib, json, math, re
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_rookie_execution_choice.py'
OUT='design/CHICAGO_2022_ROOKIE_EXECUTION_CHOICE.json'
MD=OUT.replace('.json','.md')
BASELINE='bebabcf65be6af0d73d39b5a290249de52952397'
CORE='simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json'
WINDOW='simulation/CHICAGO_2022_23_NAMED_CONTRACT_WINDOW.json'
BOARD='research/NBA_2022_FULL_DRAFT_WORKING_BOARD_2026_10_08.json'
TENDER='research/CHICAGO_2022_UNSIGNED_DRAFT_EXECUTION_FAMILY_2026_10_07.json'
PINS={'simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json': 'e7d0f4b15bc06c7cd16a38d158b38a78871fb7372d412639e33bb20c31d225a7', 'simulation/CHICAGO_2022_23_NAMED_CONTRACT_WINDOW.json': '21e860056c2654d5e4837911dac39e7f45f4d26388d353bc57594afefcecf1f4', 'research/NBA_2022_FULL_DRAFT_WORKING_BOARD_2026_10_08.json': '3bdad52ebaacda5abb23b9908b8ed3a9b85cfaa09d838819a959cd024a58e940', 'research/CHICAGO_2022_UNSIGNED_DRAFT_EXECUTION_FAMILY_2026_10_07.json': '7c2ea95557f96a9156709aabb8574fcaea8993831aed5f2f6cc626be6829bafd'}
CBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
NEWCBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-2023-cba-boundary-20261007/cba2023.pdf')
BYLAWS=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-2019-bylaws.pdf')
RAW_SHA={str(CBA):'66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a',str(NEWCBA):'bf178ca0f2d64f9dfe6fde095d3ae43d576b12e19ce7a679618d632584f7ab32',str(BYLAWS):'6accb3d9633e15e8559d13228c27ae7b3b0b81eac0894050b06256eea6da3464'}
SCALE=[2659500,2792300,2925400]
YEAR1=3191400
WAIVE_AMOUNTS={'Stanley Johnson':2351532,'Tony Bradley':2036328}

def norm(s): return s.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
def sha(p): return hashlib.sha256(norm((ROOT/p).read_text(encoding='utf-8-sig')).encode()).hexdigest()
def dump(x): return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def physical():
    for p,h in PINS.items(): assert sha(p)==h, 'Pinned source changed: '+p
    return {p:json.loads((ROOT/p).read_text(encoding='utf-8-sig')) for p in PINS}
def source_inputs(): return physical()
def assert_sources(s):
    assert s==physical(), 'Source objects differ from pinned physical documents'
    rows=s[CORE]['selected_contracts']
    assert len(rows)==17 and sum(x['source_row']['roster_type']=='STANDARD' for x in rows)==15
    for n,a in WAIVE_AMOUNTS.items():
        x=next(x['source_row'] for x in rows if x['source_row']['player']==n)
        assert x['normal_upper']==x['apron_upper']==a and x['roster_type']=='STANDARD'
    assert s[CORE]['cost_on_2022_07_07']['live15_normal_upper']==141378541
    b=s[BOARD]
    assert len(b['rows'])==60 and len({x['player'] for x in b['rows']})==60
    for pick,name in [(18,'Walker Kessler'),(57,'Keon Ellis')]:
        x=next(x for x in b['rows'] if x.get('pick',x.get('overall_pick',x.get('overall')))==pick)
        assert x['player']==name
        assert x['selecting_team']==x['conditional_final_rights_holder']=='CHI'
        assert x['available_before_selection'] is True and x['new_NBA_UPC_or_RequiredTender'] is False
        assert x['actual_historical_order_team_or_trade_imported'] is False
        assert x['execution_class']=='UNSELECTED_CHICAGO_CORE_PRESERVING_RECOMMENDATION'
    p=s[TENDER]['selected_policy']
    assert p['first_offer_date']=='2022-07-08' and p['second_offer_date']=='2022-08-25'
    assert p['second_acceptance_through']=='2022-10-15'
    c=s[WINDOW]['working_implementation']['cost']
    assert c['normal_preserved_family_upper_before_new_D23_charge']==170845541
    assert c['apron_preserved_family_upper_before_new_D23_charge']==172483541
    assert c['N23'] is None and c['A23'] is None

def primary():
    import fitz
    result=[]
    for path,pages,url,role in [
      (CBA,[27,30,35,54,55,74,75,202,206,210,232,240,241,292,293,294,295,303,304,403],
       'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','OPERATIVE_2022_CONTRACT_RULES'),
      (NEWCBA,[32,33,631],
       'https://imgix.cosmicjs.com/25da5eb0-15eb-11ee-b5b3-fbd321202bdf-Final-2023-NBA-Collective-Bargaining-Agreement-6-28-23.pdf','RETROSPECTIVE_2022_BASELINE_NUMERIC_EVIDENCE_ONLY_NOT_2023_LAW_APPLIED_TO_2022'),
      (BYLAWS,[75,76,77],
       'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf','PUBLIC_WAIVER_PROCEDURE_TEMPLATE_NO_ACTUAL_2022_RECEIPT_CERTIFICATE')]:
        assert hashlib.sha256(path.read_bytes()).hexdigest()==RAW_SHA[str(path)]
        d=fitz.open(path); text={n:norm(d[n-1].get_text()) for n in pages}
        if path==NEWCBA:
            compact=' '.join(text[631].split())
            assert '18 2,659,500 2,792,300 2,925,400 53.8% 51.9%' in compact
            assert '2022-23 Salary Cap Year to the 2023-24' in text[32]
        if path==CBA:
            assert 'one hundred twenty percent (120%)' in text[294]
            assert 'July 15' in text[303] and 'two (2) weeks before the September 5' in text[303]
        if path==BYLAWS: assert 'forty-eight (48)' in text[76]
        result.append({'url':url,'cache_path':str(path),'raw_sha256':RAW_SHA[str(path)],'role':role,
          'PDF1based_normalized_fitz_text_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest() for n,t in text.items()}})
    return result

def rookie_terms():
    fourth=Fraction(3510480)*Fraction(1538,1000)
    return {'player':'Walker Kessler','candidate_pick':18,'mechanism':'VII6h_ROOKIE_EXCEPTION_VIII1',
      'first_covered_season':'2022-23','signing_candidate_date':'2022-07-11',
      'scale_first_three_years_dollars':SCALE,'plain_current_base_percent':120,
      'base_first_three_years':[3191400,3350760,3510480],
      'fourth_year_if_separately_exercised_exact_rational':str(fourth),
      'fourth_year_dollar_ceil_upper':math.ceil(fourth),'fourth_year_NBA_rounding_certified':False,
      'term':'Two guaranteed Seasons plus distinct unexercised team options for third/fourth Seasons',
      'skill_injury_protection_percent_of_candidate_base':100,
      'mandatory_80percent_protection_individual_limitations':False,
      'signing_bonus':0,'performance_bonus':0,'loan':0,'new_international_buyout':0,
      'old_100percent_RequiredTender_accepted':False,
      'new_120percent_RSC_separate_consensual_negotiation':True,
      'future_options_exercised':False,'actual_player_team_consent':None,
      'actual_NBA_UPC_or_exact_cents_certificate':False}

def assert_terms(t):
    # Literal lawful form check independent of a substituted terms constructor.
    assert t['player']=='Walker Kessler' and t['candidate_pick']==18
    assert t['mechanism']=='VII6h_ROOKIE_EXCEPTION_VIII1' and t['signing_candidate_date']=='2022-07-11'
    assert t['scale_first_three_years_dollars']==[2659500,2792300,2925400]
    assert t['plain_current_base_percent']==120 and t['base_first_three_years']==[3191400,3350760,3510480]
    assert t['fourth_year_if_separately_exercised_exact_rational']==str(Fraction(3510480)*Fraction(1538,1000))
    assert t['fourth_year_dollar_ceil_upper']==5399119
    assert t['skill_injury_protection_percent_of_candidate_base']==100
    assert not t['mandatory_80percent_protection_individual_limitations']
    assert all(t[k]==0 for k in ['signing_bonus','performance_bonus','loan','new_international_buyout'])
    assert t['term']=='Two guaranteed Seasons plus distinct unexercised team options for third/fourth Seasons'
    assert not t['future_options_exercised'] and not t['old_100percent_RequiredTender_accepted']
    assert t['new_120percent_RSC_separate_consensual_negotiation'] and t['actual_player_team_consent'] is None
    assert t['actual_NBA_UPC_or_exact_cents_certificate'] is False

def ellis_tender():
    return {'player':'Keon Ellis','candidate_pick':57,'holder':'CHI','source':'2017I1ddd/X4a',
      'offer_date':'2022-08-25','acceptance_open_through':'2022-10-15',
      'term':'One 2022-23 Season','salary':'Applicable II6 YOS0 minimum; no new bonus',
      'delivered_team_signed_UPC_form':'Candidate timely delivery by a method permitted in I1ddd',
      'accepted':False,'withdrawn':False,'rights_renounced':False,'STD_added':0,'TW_added':0,
      'normal_overreserve_preserved':1018000,'apron_overreserve_preserved':1837000,
      'unaccepted_second_tender_reserve_is_actual_statutory_charge':False,
      'actual_delivery_receipt_or_player_refusal_certified':False,
      'rights_after_SubsequentDraft2023_automatically_retained':False,
      'foreign_contract_X5_or_eligibility_change_automatically_assumed_absent':False}

def assert_ellis(e):
    assert e['player']=='Keon Ellis' and e['candidate_pick']==57 and e['holder']=='CHI'
    assert e['offer_date']=='2022-08-25' and e['acceptance_open_through']=='2022-10-15'
    assert e['term']=='One 2022-23 Season' and e['salary']=='Applicable II6 YOS0 minimum; no new bonus'
    assert not e['accepted'] and not e['withdrawn'] and not e['rights_renounced']
    assert e['STD_added']==e['TW_added']==0
    assert e['normal_overreserve_preserved']==1018000 and e['apron_overreserve_preserved']==1837000
    assert e['unaccepted_second_tender_reserve_is_actual_statutory_charge'] is False, 'Unaccepted RT overreserve is not an actual statutory charge'
    assert not e['rights_after_SubsequentDraft2023_automatically_retained']
    assert e['actual_delivery_receipt_or_player_refusal_certified'] is False
    assert e['foreign_contract_X5_or_eligibility_change_automatically_assumed_absent'] is False
    assert e['delivered_team_signed_UPC_form']=='Candidate timely delivery by a method permitted in I1ddd'

def routes(s,t,e):
    std=[x['source_row']['player'] for x in s[CORE]['selected_contracts'] if x['source_row']['roster_type']=='STANDARD']
    tw=[x['source_row']['player'] for x in s[CORE]['selected_contracts'] if x['source_row']['roster_type']=='TWO_WAY']
    cost=s[CORE]['cost_on_2022_07_07']; result=[]
    for rid,name in [('R1_WAIVE_STANLEY_KEEP_BRADLEY','Stanley Johnson'),('R2_WAIVE_BRADLEY_KEEP_STANLEY','Tony Bradley')]:
        a=WAIVE_AMOUNTS[name]; live=cost['live15_normal_upper']-a+YEAR1
        result.append({'id':rid,'classification':'UNSELECTED_WORKING_CANDIDATE','released':name,
          'waiver_method':'Nonassignment unclaimed waiver, conforming notice plus full waiver-period expiry before signing',
          'candidate_notice_date':'2022-07-08','candidate_completed_unclaimed_waiver_by':'2022-07-10',
          'notice_and_expiry_condition':'Commissioner/designee distribution early enough for full48hours before July11RSC; actual timestamp/claims/clearance null',
          'actual_waiver_clearance_or_NBA_process_receipt':None,
          'roster_steps':[{'action':'Before release','STD':15,'TW':2},{'action':'After lawful unclaimed waiver completion','STD':14,'TW':2},{'action':'After Kessler candidate RSC','STD':15,'TW':2}],
          'standard': [n for n in std if n!=name]+['Walker Kessler'],'two_way':tw,
          'Ellis_standard_or_TW_added':0,'assignment_or_trade_bonus_triggered_by_this_release':False,
          'preserved_full_old_year2_protection_Gamma_upper':a,'protection_amount_is_actual_exact_guarantee':False,
          'full_old_charge_retained_no_buyout_stretch_setoff_or_payment_reschedule_deduction':True,
          'no_new_expired_Veteran_Free_Agent_hold_added_for_this_waiver':'I1cc(iii) waived Free Agent differs from I1hhhh completed Veteran Free Agent; VII4a2 only latter. Old waivedSalary retained, no automaticnewhold/no newUFAre-signing.',
          'live15_normal_apron_upper':live,'separately_reserved_old_waived_charge_upper':a,
          'live_plus_old_waived_upper':live+a,'new_salary_obligation_vs_original_signed15_upper':YEAR1,
          'old_first_overreserve_removed_once':11060000,'new_first_RSC_upper':YEAR1,
          'refined_normal_public_family_upper_before_D23':cost['normal_public_family_upper']-11060000+YEAR1,
          'refined_apron_public_family_upper_before_D23':cost['apron_public_family_upper']-11060000+YEAR1,
          'bound_refinement_delta':YEAR1-11060000,'apron_screen_not_binding_without_trigger':156982000,
          'new_RSC_uses_NTMLE_BAE_or_receives_SandT':False,'new_FY22_hardcap_trigger':False,
          'N23':None,'A23':None,'whole_FY22_numeric_upper_after_new_D23':None,
          'independent_board_review_claimed_by_this_leaf':False,'actual_event_or_new_author_lock':False})
    return result

def assert_routes(rs,s):
    assert len(rs)==2
    base=[x['source_row']['player'] for x in s[CORE]['selected_contracts'][:15]]
    for r,name in zip(rs,['Stanley Johnson','Tony Bradley']):
        a=WAIVE_AMOUNTS[name]
        assert r['released']==name and r['classification']=='UNSELECTED_WORKING_CANDIDATE'
        assert r['standard']==[n for n in base if n!=name]+['Walker Kessler']
        assert len(r['standard'])==len(set(r['standard']))==15
        assert r['two_way']==['Devon Dotson','Tyler Cook']
        assert [x['STD'] for x in r['roster_steps']]==[15,14,15] and all(x['TW']==2 for x in r['roster_steps'])
        assert r['Ellis_standard_or_TW_added']==0
        assert r['candidate_notice_date']=='2022-07-08' and r['candidate_completed_unclaimed_waiver_by']=='2022-07-10'
        assert r['actual_waiver_clearance_or_NBA_process_receipt'] is None
        assert r['waiver_method']=='Nonassignment unclaimed waiver, conforming notice plus full waiver-period expiry before signing'
        assert r['notice_and_expiry_condition']=='Commissioner/designee distribution early enough for full48hours before July11RSC; actual timestamp/claims/clearance null'
        assert r['assignment_or_trade_bonus_triggered_by_this_release'] is False
        assert r['independent_board_review_claimed_by_this_leaf'] is False
        assert r['preserved_full_old_year2_protection_Gamma_upper']==r['separately_reserved_old_waived_charge_upper']==a
        assert r['protection_amount_is_actual_exact_guarantee'] is False, 'Preserved full protection upper is not an actual exact guarantee certificate'
        assert r['full_old_charge_retained_no_buyout_stretch_setoff_or_payment_reschedule_deduction'] is True
        assert r['no_new_expired_Veteran_Free_Agent_hold_added_for_this_waiver']=='I1cc(iii) waived Free Agent differs from I1hhhh completed Veteran Free Agent; VII4a2 only latter. Old waivedSalary retained, no automaticnewhold/no newUFAre-signing.'
        assert r['live15_normal_apron_upper']==141378541-a+3191400
        assert r['live_plus_old_waived_upper']==144569941
        assert r['new_salary_obligation_vs_original_signed15_upper']==3191400
        assert r['old_first_overreserve_removed_once']==11060000 and r['new_first_RSC_upper']==3191400
        assert r['refined_normal_public_family_upper_before_D23']==162976941
        assert r['refined_apron_public_family_upper_before_D23']==164614941
        assert r['bound_refinement_delta']==-7868600
        assert r['N23'] is None and r['A23'] is None and r['whole_FY22_numeric_upper_after_new_D23'] is None
        assert not r['new_FY22_hardcap_trigger'] and not r['new_RSC_uses_NTMLE_BAE_or_receives_SandT']
        assert not r['actual_event_or_new_author_lock']

def build():
    s=source_inputs();assert_sources(s);p=primary()
    t=rookie_terms();assert_terms(t);e=ellis_tender();assert_ellis(e)
    rs=routes(s,t,e);assert_routes(rs,s)
    return {'id':'CHICAGO_2022_ROOKIE_EXECUTION_CHOICE','baseline_main':BASELINE,
      'status':'TWO_NAMED_ROOKIE_EXECUTION_CANDIDATES_REVIEW_PENDING_NOT_SELECTED',
      'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8BOMstrip;CRLF/CRtoLF','primary':p,
      'source_locators':{'current17':CORE+'#/selected_contracts','same_cost':CORE+'#/cost_on_2022_07_07',
        'Stanley_Bradley_service_term':WINDOW+'#/working_implementation/named_contracts/7..8',
        'candidate_draft18_57':BOARD+'#/rows/17 and /56','RSC_law':'2017VIII1 PDF292–295; VII6h PDF232',
        'waived_salary_preserved':'2017VII4a1i PDF202; XXVII PDF403 setoff not deducted',
        'waiver_not_new_expired_VFA_hold':'2017I1cc(iii)/hhhh PDF27/35; VII4a2 PDF206',
        'waiver_procedure':'NBA2019Bylaws5.03/5.04 PDF76; publictemplate not actual2022clearance',
        'scale_numeric':'2023I1iii PDF32 plus ExB PDF631: 2022–23 baseline, not operative2023rules',
        'RT_form_and_window':'2017I1ddd PDF30; X4a/e/f/g PDF303–304'},
      'scale_source_boundary':{'table_prints_heading_dollar_thousands_but_cells_have_full_dollar_comma_values':True,
        'adopted_cells_are_dollar_baseline_not_multiplied_by1000':True,
        '2023_I1iii_links_baseline_to_2022_23_before_2023_24_cap_adjustment':True,
        'contemporaneous_crosscheck_search_only':'HoopsRumors July2022 rookie-scale article indexed #18 first3191400/next3350760/3510480; original body open502, not adopted original-body evidence',
        'original_2022_NBA_CBA101_table_recovered':False,'exact_NBA_rounding_algorithm_certified':False,
        'search_boundary':'Three distinct finite queries plus existing Bulls/Pacers2022guides found no2022NBA rookie numeric table; no repeat download. 2023NBPA original baseline used narrowly.'},
      'input_board_status_at_read':s[BOARD]['status'],'input_board_independent_flag_inherited_not_fabricated':s[BOARD].get('certification',{}).get('independent_review_completed'),
      'rookie_terms':t,'Ellis_tender':e,'routes':rs,
      'retained_unsigned_comparator':{'STD':15,'TW':2,'Kessler_new_UPC':False,'Ellis_new_UPC':False,
        'normal_original_conservative_upper':170845541,'apron_original_conservative_upper':172483541,
        'first100percent_tender_and120percent_normal_hold_are_distinct':True,
        'unsigned_ports_do_not_automatically_use_standard_slots':True},
      'quantifier':'For preserved reviewed public incumbent cost/protection families, either expressly conditional unclaimed-waiver candidate reserves the full outgoing year2 upper and permits one consensual new120%RSC; no actual source clearance/consent or direction selected.',
      'remaining_finite_inputs':['Parent review/selection of2022board and named release+newRSC candidate, not automatichistoricalTerry orUtahKesslercopy','Conforming actual fictional waiver process and player/teamRSC assent if candidate selected; no historicalprivate receipt certificate required','Ellis future RT delivery/unaccepted fictional path and X4 subsequentDraft boundary; acceptance requires another namedslot action','2022–23 minutes/availability/results and newD23 N23/A23 remain separate finite inputs'],
      'certification':{'independent_review_completed':False,'candidate_comparison_generated':True,'selected_route':None,
        'draft_author_lock':False,'waiver_or_new_UPC_selected':False,'third_TW_created':False,
        'actual_private_exact_costs_or_full_guarantee_certified':False,'actual_consent_medical_receipt_or_history_certified':False,
        'whole_FY22_or_macro3_complete':False,'central_REGISTER_promoted':False},
      'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0,'manuscript_allowed':False}

def render(j):
    rows='\n'.join('| '+r['id']+' | '+r['released']+' | '+format(r['live15_normal_apron_upper'],',')+' | '+format(r['separately_reserved_old_waived_charge_upper'],',')+' | 144,569,941 |' for r in j['routes'])
    return '''# Chicago 2022 신인 실행 비교 — 미선택 두 후보

현재 15STD+2TW에 후보 보드의 CHI18 Walker Kessler / CHI57 Keon Ellis를 연결한다. 원보드의 검문 상태는 JSON 그대로 읽고 독립 완료를 새로 인증하지 않는다. Dalen Terry의 실제 Chicago 계약이나 Kessler의 실제 Utah #22 계약, Ellis의 실제 TW 계약을 복사하지 않는다.

## Kessler와 명명된 자리

Stanley Johnson 또는 Tony Bradley의 **양도 없는 미청구 waiver가 적법하게 완료된 뒤** 15→14→15STD를 만든다. 후보 통지 July8 → 정상48시간 창 종료 July10 → 별도 합의 RSC July11. 이는 배포시각·청구 없음·clearance가 충족되는 가상 절차 후보이며, 요청만으로 새 자리가 생긴다고 인증하지 않는다. 다른 구단 청구가 생긴 분기는 이 비양도 가족에 포함시키지 않는다.

| 후보 | 방출 이름 | 새 live15 상단 | 기존 방출 Year2 전액 예약 | 합계 |
|---|---|---:|---:|---:|
'''+rows+'''

두 경로 모두 원 보호 Γ 범위의 **전액 상단**을 Chicago 비용에 남긴다. 실제 보장률 100%/원현금 지급을 사실로 선택하지 않는다. buyout 할인·stretch·setoff·새 수취팀을 만들어 원채무를 지우지 않는다. Bradley 유지안은 기존 백업 센터를 남기고 Stanley 유지안은 기존 윙을 남기는 명단 차이다. 출장·능력·팀 성과는 이 비교에서 선택하지 않는다.

## #18 계약과 숫자 원천

2017 VIII1/VII6h의 Rookie Exception으로 두 시즌+별도 두 팀 옵션, base120%, 새 bonus/loan/buyout0의 합의 **후보**를 만든다. 첫3년 3,191,400 / 3,350,760 / 3,510,480. 네 번째는 옵션 행사 시 53.8% 증가, 정확 유리수 5,399,118.24와 정수 상단5,399,119만 표시한다. 이후 옵션 행사는 미선택이다. 첫 두 시즌과 첫 옵션년의 필수80% 보호를 충족하는 후보100% 보호를 제안하며, 금지된 개별 제한은 없다. 기존100% Required Tender를 수락한 계약이라고 말하지 않는다.

공식 2023 CBA I1(iii), PDF32/ExB PDF631은 2022–23 기준 금액을 다음 해 cap 비율로 조정한다고 연결한다. #18 표의 첫3개 숫자 2,659,500 / 2,792,300 / 2,925,400을 2022 기준의 **후대 숫자 증거**로만 사용한다. 표 heading은 `$000’S`이나 실제 cell은 달러값 형태다. 이를 다시1000배하지 않는다. 당시 HoopsRumors 검색 색인은 첫3년120%와 일치하지만 본문 open은502였으므로 원본문 회수로 세지 않는다. 실제 적용법은2017이며2023법을2022에 소급 적용하지 않는다. 원2022 NBA 표 및 정확 반올림 알고리즘 미회수는 명시하고 실제 사적 센트 인증은 false다.

## 같은 비용 상단 연결

기존 서명15명 141,378,541에 신인 급여3,191,400을 더하면 live+원dead 합계144,569,941. 기존 상단에 이미 있던 원방출 선수 금액을 **두 번 가산하지 않는다**. 기존 first 예약11,060,000을 새 RSC3,191,400으로 한 번 대체하면 보존된 공개 가족의 normal162,976,941 / apron164,614,941로 예약 상단7,868,600을 줄인다. Keon·Marko의 기존 second 예약 및 legacy16,371,000은 그대로 남긴다. 이는 실제 장부 비용이7.87m 줄었다는 사실이 아니다.

RSC 자체는 NTMLE/BAE/수취 S&T를 사용하지 않아 새 FY22 hardcap을 유발하지 않는다. apron screen 초과는 이 가족의 실제 위법 증명이 아니다. 새2023draft N23/A23은 null이며, 그 이후 전체숫자 상단/시즌결과를 인증하지 않는다.

## Ellis: 새 자리0

Aug25 팀서명 1시즌 최소급여 tender를 I1ddd의 적법 전달방법으로 제공하고 Oct15까지 수락 창을 둔 **미수락 후보**다. 이는 실제 선수 거절 사실이 아니다. STD0/TW0를 추가하므로 Devon Dotson/Tyler Cook의 기존 TW2를 유지한다. tender를 수락하거나 새TW를 체결하는 경로는 별도 named slot 없이 실행하지 않는다. 원second normal1,018,000/apron1,837,000 초과예약은 실제 미수락 capcharge로 승격하지 않는다. 원외국계약/가용성 문제가 있으면 X5/X6 적용 입력으로 남기고, 다음Draft 이후 권리를 자동 연장하지 않는다.

## 현행 범위

| 대그룹 | 상태 |
|---|---|
| 1 드래프트 연쇄 | 완료 범위 보존 |
| 2 Chicago 2020–21 | S2 완료 보존 |
| 3 2021–23 계약·시즌 | 진행; 이번 신인 두 후보 미선택 |
| 4 장기 커리어 | 선행 시즌·후속 의존성 |
| 5 결말·전체 구조 | 진행 |
| 6 집필 규격·Pack | 진행·Pack0 |
| 7 통합·독립·작가 승인 | 미완료·CLOSED |

미완료 대그룹5, 6번까지4. v0.30 PARTIAL / 원고0. 중앙·REGISTER·새 보드/계약 작가잠금은 변경하지 않는다.
'''

def validate(j):
    errors=[]
    try:
        s=physical();assert_sources(s);assert_terms(j['rookie_terms']);assert_ellis(j['Ellis_tender']);assert_routes(j['routes'],s)
        assert j==build(), 'Saved artifact differs from reconstructed source-bound candidate'
    except (AssertionError,KeyError,ValueError) as e:errors.append(str(e) or 'Semantic assertion rejected')
    return errors

def self_test():
    base=build();s=physical();passed=[]
    def reject(label,helper,bad):
        try:
            with patch(__name__+'.'+helper,return_value=bad):build()
        except AssertionError:passed.append(label);return
        raise AssertionError('FALSE_PASS '+label)
    r=copy.deepcopy(base['routes']);r[0]['separately_reserved_old_waived_charge_upper']=0;reject('preserved_waived_charge_erased','routes',r)
    r=copy.deepcopy(base['routes']);r[0]['standard'].append('Stanley Johnson');reject('new_STD16_without_release','routes',r)
    e=copy.deepcopy(base['Ellis_tender']);e['TW_added']=1;reject('Ellis_third_TW','ellis_tender',e)
    t=copy.deepcopy(base['rookie_terms']);t['base_first_three_years'][0]=2696400;reject('actual_Utah_pick22_copied','rookie_terms',t)
    r=copy.deepcopy(base['routes']);r[0]['refined_normal_public_family_upper_before_D23']-=2351532;reject('old_waiver_cash_discounted','routes',r)
    t=copy.deepcopy(base['rookie_terms']);t['term']='Four guaranteed Seasons';reject('rookie_options_made_guaranteed','rookie_terms',t)
    bad=copy.deepcopy(s);x=next(x for x in bad[BOARD]['rows'] if x.get('pick',x.get('overall_pick',x.get('overall')))==18);x['player']='Dalen Terry';reject('board_same_pick_wrong_player','source_inputs',bad)
    r=copy.deepcopy(base['routes']);r[0]['protection_amount_is_actual_exact_guarantee']=True;reject('protection_upper_promoted_to_actual_guarantee','routes',r)
    e=copy.deepcopy(base['Ellis_tender']);e['unaccepted_second_tender_reserve_is_actual_statutory_charge']=True;reject('unaccepted_RT_reserve_promoted_to_statutory_charge','ellis_tender',e)
    return passed

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args()
    j=build()
    if a.write:(ROOT/OUT).write_text(dump(j),encoding='utf-8');(ROOT/MD).write_text(render(j),encoding='utf-8')
    errors=[]
    if a.check:
        errors=validate(json.loads((ROOT/OUT).read_text(encoding='utf-8-sig')))
        if norm((ROOT/MD).read_text(encoding='utf-8-sig'))!=render(j):errors.append('Markdown not current')
    negatives=self_test() if a.self_test else []
    print(dump({'current':not errors,'errors':errors,'routes':len(j['routes']),'negatives':negatives,'normal':162976941,'apron':164614941,'selected_route':None}))
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
