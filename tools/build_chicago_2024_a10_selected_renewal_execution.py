"""Selected Y24_KEEP5_MINIMUM: dated contract/hold replacement, not game selection."""
from __future__ import annotations
import argparse,copy,hashlib,json
from pathlib import Path
from unittest.mock import patch
import build_chicago_2024_25_a10_named_role_window_cost_family as family

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2024_a10_selected_renewal_execution.py'
OUT='simulation/CHICAGO_2024_A10_SELECTED_RENEWAL_EXECUTION.json'
SELECT='canon/DELEGATED_CHICAGO_2024_A10_ROUTINE_RENEWAL_SELECTION_2026_10_08.json'
PEER='reviews/CHICAGO_2024_25_A10_NAMED_ROLE_WINDOW_COST_FAMILY_DEN_INDEPENDENT_REVIEW_2026_10_08.json'
PINS={SELECT:'a6e9c297f5377dea04ece760a9a6ff259572dd465b78498b7d76cafdf7ab7c25',
family.OUT:'af4f3b340841251a50646fb05aeefcc415e95c4fc07b3c2e02e3f9af8bb14bb1',
family.SELF:'ab4de10e3efed840495cf42327b112cb613bf3f2b6baa9b4685c0755058dc16f',
PEER:'036e340011ef12f3f2fc00a6690dde7fcf8ada5f7aa944ddb3c5b1b34fe00f93'}
BASE='133115425+LM24+6/5*S23(16,2)'
Q='M24(10)+M24(5)+M24(3)+2*M24(8)'
POST=BASE+'+'+Q+'+R24+D24_N_or_A'

def norm(t):return t.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(norm((ROOT/p).read_text(encoding='utf-8-sig')).encode()).hexdigest()
def serial(o):return json.dumps(o,ensure_ascii=False,indent=2)+'\n'
def physical():
    for p,h in PINS.items():assert sha(p)==h,'Selected renewal pinned source changed: '+p
    return {p:json.loads((ROOT/p).read_text(encoding='utf-8-sig')) for p in PINS if p.endswith('.json')}
def source_inputs():return physical()
def assert_sources(s):
    assert s==physical(),'Returned selection/family differs from physical input'
    old=s[family.OUT];z=s[SELECT]
    assert family.validate(old)==[],'Reviewed family no longer reconstructs from its sources'
    assert s[PEER]['independent_review_completed'] is True
    assert s[PEER]['source_sha256'][family.OUT]==PINS[family.OUT] and s[PEER]['source_sha256'][family.SELF]==PINS[family.SELF]
    assert z['selected_form']=='Y24_KEEP5_MINIMUM' and z['selected_signature_date']=='2024-07-07' and z['selected_fictional_player_and_team_agreements'] is True
    assert not z['new_human_author_lock'] and not z['live_prior_contracts_auto_renegotiated']
    expected=copy.deepcopy(old['expiry_and_renewal_candidates5'])
    for r in expected:r.update(adopted_new_contract=True,selected_fictional_agreement=True)
    assert z['selected_new_contract_rows']==expected,'Selection changes reviewed terms rather than selecting same family'
    assert z['selected_cleanup']=={'date':'2024-07-07','Dotson_Cook_valid_FA_right_renunciation':True,'unused_current_annual_exception_renunciation':True,
      'written_notices_selected_as_method_not_all_CBA_literal_requirement':True,'Bradley_prior_valid_renunciation_preserved':True,'current_live_Bird_or_RSC_contracts_erased':False,
      'all_original_Gamma_and_accrued_payment_obligations_preserved':True,'valid_old_stretch_R24_preserved':True,'D24_unsigned_draft_RT_claim_port_preserved_not_zeroed':True}
    assert z['source_cost_form']==POST and z['post_signature_STD']==15 and z['post_signature_TW']==0
    assert z['future_HigherMax_award_qualification_selected'] is False and z['new_Jaquez_third_option_or_2024_draft_RSC_selected'] is False
    assert z['first_option_game_date_minute_health_coach_calls_or_result_selected'] is False

def construct(s):
    f=s[family.OUT];z=s[SELECT]
    live=copy.deepcopy(f['live10']);renew=copy.deepcopy(z['selected_new_contract_rows'])
    for r in renew:
        r.update(effective_date='2024-07-07',FY24_covered_fiscal_window='2024-07-01..2025-06-30',
          last_salary_capyear_start=2024,last_fiscal_end='2025-06-30',fiscal_end_is_exact_service_term=False,
          new_player_fullcash=r['salary'],normal_fullcash_upper=r['salary'],apron_fullcash_upper=r['salary'])
    names=[r['player'] for r in live+renew]
    states=[]
    for date,label,cleanup,signed,std in [('2024-07-01','FY24_ROLLOVER_FA_HOLDS_PRESERVED',False,False,10),
        ('2024-07-07','BEFORE_SELECTED_RENEWALS_AND_RENUNCIATIONS',False,False,10),
        ('2024-07-07','AFTER_SELECTED_RIGHTS_AND_UNUSED_EXCEPTION_RENUNCIATIONS',True,False,10),
        ('2024-07-07','AFTER_FIVE_SELECTED_NEW_MINIMUM_UPCS',True,True,15)]:
        states.append({'date':date,'within_selected_model_order':len(states),'event':label,'STD':std,'TW_UPC':0,
          'named_STD':names if signed else [r['player'] for r in live],
          'five_expired_UPCs_automatically_renewed':False,'five_UFA_claims_replaced_by_new_UPCs':signed,
          'Dotson_Cook_FA_right_renunciation_effective':cleanup,'unused_FY24_exception_renunciation_effective':cleanup,
          'normal_cost_function':POST.replace('D24_N_or_A','D24_N') if signed else BASE+'+H24_five_UFA+R24+D24_N'+('' if cleanup else '+2*M24(0)+E24_unused'),
          'apron_fullcash_outer_function':POST.replace('D24_N_or_A','D24_A') if signed else BASE+'+R24+D24_A',
          'new_five_player_fullcash':Q if signed else 0,
          'old_Gamma_accrued_pay_and_R24_preserved':True,'draft_D24_ports_retained':True,
          'same_claim_UFA_and_new_salary_both_added':False,'model_order_is_actual_signature_time':False,
          'actual_assent_notice_receipt':None})
    return {'live10':live,'selected_new_contracts5':renew,'post_signature_named_STD':names,
      'dated_states':states,'cost_family':{'base_fixed8_upper':133115425,'LM24_ordinary_reference_not_award_selection':f['cost_family']['LM_ordinary'],
        'LM24_ordinary_or_lawful_HigherMax':'35147000 or42176400 onlyII7lawfulqualification; awardoutcome notselected',
        'Jaquez_Year2':'6/5*S23(16,2)','five_new_minimum_cash':Q,'normal_apron_fullcash_outer':POST,
        'before_renewal_normal_FA_outer':f['cost_family']['before_renewal_normal_FA_outer'],
        'before_renewal_apron_FA':f['cost_family']['before_renewal_apron_FA'],
        'R24_interval':[0,16371000],'R24_original_scope':f['cost_family']['R24_frame'],
        'D24_N_and_A':f['cost_family']['D24_N_or_A'],'D24_actual_amount':None,
        'unused_exceptions_after_selected_renunciation':0,'zero_is_actual_original_owed_payment':False,
        'Tax':f['cost_family']['tax'],'new_salary_cash':f['cost_family']['cash'],
        'new_hardcap_trigger':False,'over_apron_is_automatic_illegality':False,'whole_actual_private_FY24_ledger':False}}

def assert_payload(o,s):
    f=s[family.OUT];z=s[SELECT]
    assert o['live10']==f['live10'],'Selected consumer changes original live UPC/window/charges'
    r=o['selected_new_contracts5'];assert len(r)==5
    for actual,original in zip(r,z['selected_new_contract_rows']):
        expected=copy.deepcopy(original)
        expected.update(effective_date='2024-07-07',FY24_covered_fiscal_window='2024-07-01..2025-06-30',last_salary_capyear_start=2024,
          last_fiscal_end='2025-06-30',fiscal_end_is_exact_service_term=False,new_player_fullcash=original['salary'],
          normal_fullcash_upper=original['salary'],apron_fullcash_upper=original['salary'])
        assert actual==expected,'Selected positive minimum/term differs from physical selection'
    live_names=[r['player'] for r in f['live10']];names=live_names+[r['player'] for r in z['selected_new_contract_rows']]
    assert o['post_signature_named_STD']==names and len(set(names))==15 and set(family.CORE5)<=set(names)
    steps=o['dated_states'];assert len(steps)==4
    literals=[('2024-07-01','FY24_ROLLOVER_FA_HOLDS_PRESERVED',False,False,10),('2024-07-07','BEFORE_SELECTED_RENEWALS_AND_RENUNCIATIONS',False,False,10),
      ('2024-07-07','AFTER_SELECTED_RIGHTS_AND_UNUSED_EXCEPTION_RENUNCIATIONS',True,False,10),('2024-07-07','AFTER_FIVE_SELECTED_NEW_MINIMUM_UPCS',True,True,15)]
    for i,(date,label,cleanup,signed,std) in enumerate(literals):
        expected={'date':date,'within_selected_model_order':i,'event':label,'STD':std,'TW_UPC':0,'named_STD':names if signed else live_names,
          'five_expired_UPCs_automatically_renewed':False,'five_UFA_claims_replaced_by_new_UPCs':signed,
          'Dotson_Cook_FA_right_renunciation_effective':cleanup,'unused_FY24_exception_renunciation_effective':cleanup,
          'normal_cost_function':POST.replace('D24_N_or_A','D24_N') if signed else BASE+'+H24_five_UFA+R24+D24_N'+('' if cleanup else '+2*M24(0)+E24_unused'),
          'apron_fullcash_outer_function':POST.replace('D24_N_or_A','D24_A') if signed else BASE+'+R24+D24_A',
          'new_five_player_fullcash':Q if signed else 0,'old_Gamma_accrued_pay_and_R24_preserved':True,'draft_D24_ports_retained':True,
          'same_claim_UFA_and_new_salary_both_added':False,'model_order_is_actual_signature_time':False,'actual_assent_notice_receipt':None}
        assert steps[i]==expected,'Dated expiry/renunciation/positive cash/once-only cost replacement differs'
    c=o['cost_family']
    assert c=={'base_fixed8_upper':sum(family.FIXED.values()),'LM24_ordinary_reference_not_award_selection':140588000//4,
      'LM24_ordinary_or_lawful_HigherMax':'35147000 or42176400 onlyII7lawfulqualification; awardoutcome notselected',
      'Jaquez_Year2':'6/5*S23(16,2)','five_new_minimum_cash':Q,'normal_apron_fullcash_outer':z['source_cost_form'],
      'before_renewal_normal_FA_outer':f['cost_family']['before_renewal_normal_FA_outer'],'before_renewal_apron_FA':f['cost_family']['before_renewal_apron_FA'],
      'R24_interval':f['cost_family']['R24_interval'],'R24_original_scope':f['cost_family']['R24_frame'],'D24_N_and_A':f['cost_family']['D24_N_or_A'],
      'D24_actual_amount':None,'unused_exceptions_after_selected_renunciation':0,'zero_is_actual_original_owed_payment':False,
      'Tax':f['cost_family']['tax'],'new_salary_cash':f['cost_family']['cash'],'new_hardcap_trigger':False,
      'over_apron_is_automatic_illegality':False,'whole_actual_private_FY24_ledger':False},'Selected cost layer differs from physical reviewed family and design selection'

def evaluate(S23_year2,M24,R24,D24_N,D24_A,HigherMax=False,legally_qualified=False):
    return family.evaluate(S23_year2,M24,R24,D24_N,D24_A,HigherMax,legally_qualified)
def build():
    s=source_inputs();assert_sources(s);p=construct(s)
    assert_sources(s)
    assert_payload(p,physical())
    return {'id':'CHICAGO_2024_A10_SELECTED_RENEWAL_EXECUTION','status':'REVIEW_PENDING_SELECTED_Y24_KEEP5_MINIMUM_DATED_EXECUTION',
      'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8_BOM_STRIP_CRLF_CR_TO_LF_EXTERNAL_RAW_SEPARATE',
      'primary_source_and_finite_family_review':{'family':family.OUT,'peer':PEER,'raw_CBA_scope':s[family.OUT]['primary'],
        'original_candidate_adoption_flags_remain_historical':True,'new_selected_assent_is_fictional_not_actualreceipt':True},
      'selected_form':'Y24_KEEP5_MINIMUM','selection_authority':SELECT,'execution':p,'evaluator':SELF+'::evaluate',
      'conditional_role_window':{'named_core5':family.CORE5,'STD':15,'TW_UPC':0,'within_FY24_after_selected_signatures':True,
        'game_date_opponent_health_ordered_roles_coachcall_selected':False,'available8_active12_to15_condition_not_a_clinical_receipt':True},
      'completion_scope':{'selected_fictional_renewals_and_cleanup':True,'dated_contract_and_cost_replacement_family_complete':True,
        'independent_consumer_review_completed':False,'actual_prepared_cents_payment_signature_notice_or_health_certificate':False,
        'HigherMax_award_outcome_or_2024_new_rookie_UPC':False,'new_A10_role_efficiency_performance_result_or_MVP_title_selected':False,
        'whole_FY24_team_actual_cost_or_30team_career':False,'REGISTER_promotion':False,'manuscript':False},'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0}
def validate(o):
    try:
        assert o==build(),'Saved selected consumer differs from physical reconstruction'
        assert_payload(o['execution'],physical())
        return []
    except (AssertionError,KeyError,ValueError,TypeError) as e:return [str(e)]
def md(o):
    names='、'.join(o['execution']['post_signature_named_STD'])
    return '\n'.join(['# A10 선택된 2024 루틴 갱신 실행','',o['status'],'',
      '**Y24_KEEP5_MINIMUM** 선택을 후보이력과 별도로 실행한다. 루틴 가상 합의가 이미 선택됐으며 실제사적 영수증·새 인간승인을 기다리지 않는다. 원계약·후보파일의 과거미선택 flags는 재작성하지 않는다.','',
      '## 같은 날짜의 권리·등록','',
      '| 순서 | 날짜 | STD/TW | 비용/권리 변화 |','|---|---|---|',
      '|0|2024July1|10/0|만료5의normal FAhold·Dotson/Cook completedTW FAhold·unusedannualexception 보존|',
      '|1|July7 실행 전|10/0|정식renounce/새UPC 전 위청구 유지|',
      '|2|July7 선택cleanup|10/0|Dotson/Cook FA권리·unusedcurrentexception 유효renounce; 만료5hold는 유지|',
      '|3|July7 합의5UPC 후|15/0|Young/Green/Wieskamp/Valentine/Sato 양수minimum; 같은FAhold를한번교체|','',
      '동일날 모델순서는 실제 서명시각 인증이 아니다. 개별5개서명의 슬롯도10→11→12→13→14→15로15를 넘지 않는다. 신계약은1Season/full skill-injury/nooption/bonus0이며 FY24법정최소함수 M24(10)/M24(5)/M24(3)/M24(8)/M24(8)을 쓴다. Young10+와 나머지FY23서비스증가 조건은 원source 가족을 보존한다. 8m×2 Young과2023 1년min의 끝점이 새계약가격·미지급소멸을 대신하지 않는다.','',
      '선택표준15명: '+names+'. Dotson/Cook rights는liveTW계약이아니며 새TW0이다. 2024 신규신인UPC를16번째로 추가하지 않는다.','',
      '## 동일 비용 함수','',
      '고정8 상단133,115,425 + LM1 ordinary35,147,000 또는 적법HigherMax42,176,400 + Jaquez2023signingYear2 `1.2*S23(16,2)`를 보존한다. 선택된계약후 normal/apron fullcash outer는 `'+POST+'`이다. UFAhold와신Salary를동시에더하지 않는다.','',
      'cleanup 전normal H24_five_UFA는Young150/190%×8m(≤15.2m,법정max/min)와네expiredminimum의 비환급minimum부분이다. completedTW Dotson/Cook은각M24(0) FAhold가유효renounce까지남는다. 미수락2023QO기간종료≠FA/ROFR 자동삭제; 선택2024cleanup이새법적효과를준다. Apron UFAhold 제외와원보호채무 지급은서로다른계정이다.','',
      'R24[0,16.371m] 원validstretch publicfamily/ordinary말단/no새resolutionframe 보존. D24_N/A는현2024 unsigned/RT 권리의양수적용포트이며 정확액null≠0; evaluator는R24/D24를필수인자로받아미입력0을숨기지않는다. unspentannualexception도유효선택renounce전에normal에남고후에만제외된다. 모든oldGamma/보호지급은각원연도/범위로남는다. 최소계약·원liveBird/RSC와options이월은새hardcaptrigger가아니며apron초과를자동불법으로바꾸지않는다. Tax의finalregularaudit와actualcash는별도다.','',
      '## 후속 역할 창','',
      '선택된15STD가A10의P/LaMelo/LaVine/Mark/Carter 공통코어5를계약상지원한다. 실제2024–25 game/date·상대·available8/active12–15 nomination·건강·ordered240분·감독호출/성과는다음소비자로별도선택한다. HigherMax수상·Jaquez새옵션·2024신인·MVP년도·우승수·2026연장은미선택이다. 전체2023–24전역시즌재검문은이유한계약실행의새gate가아니다.','',
      '## 원천·검문','',
      '선택canon/수용된A10 sourcefamily/producer/DENpeer 네현재SHA와원family 물리재구성을소비한다. 반환명단·기간·법정가격식·expiry/cleanup/holdonce를caller에서새로 읽은 물리소스와직접대조한다. 원CBA본문·official2024cap indexed관측 및403미채택이력은sourcefamily로연결하며별도원자료수집성공을부풀리지않는다. 작성자검사는독립검문아님.','',
      '| 단계 | 범위 | 상태 |','|---|---|---|','|1|기반 정본|완료|','|2|S2 유한 시즌|완료|','|3|2021–23 계약·cap·픽|완료·원유한계약가족|','|4|후반 커리어|계약실행선택·peer대기/역할미완료|','|5|Act·Sub-Act·기능|국소 경로·전체미완료|','|6|집필규격·Context Pack|미완료·Pack0|','|7|통합·독립·최종승인|미완료·CLOSED|','',
      '미완료4 / 6번까지3 · v0.30 PARTIAL · CLOSED · 원고0.'])+'\n'
def self_test():
    s=source_inputs();done=[]
    for label,mutate in [('minimum_expression_zero',lambda x:x['selected_new_contracts5'][1].update(new_player_fullcash='0',normal_fullcash_upper='0',apron_fullcash_upper='0')),
      ('expiry_erases_hold_before_renounce',lambda x:x['dated_states'][0].update(normal_cost_function=BASE+'+R24+D24_N')),
      ('double_FA_and_new_UPC',lambda x:x['dated_states'][3].update(same_claim_UFA_and_new_salary_both_added=True)),
      ('cleanup_before_selected_date',lambda x:x['dated_states'][0].update(Dotson_Cook_FA_right_renunciation_effective=True)),
      ('draft_unknown_equals_zero',lambda x:x['cost_family'].update(D24_actual_amount=0)),
      ('highermax_outcome_preselected',lambda x:x['cost_family'].update(LM24_ordinary_or_lawful_HigherMax='42176400 guaranteedHigherMax'))]:
        b=construct(s);mutate(b)
        try:
            with patch(__name__+'.construct',return_value=b):build()
        except AssertionError:done.append(label)
        else:raise AssertionError('FALSE PASS '+label)
    return done
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();o=build()
    if a.write:(ROOT/OUT).write_text(serial(o),encoding='utf8',newline='\n');(ROOT/OUT.replace('.json','.md')).write_text(md(o),encoding='utf8',newline='\n')
    err=validate(json.loads((ROOT/OUT).read_text(encoding='utf-8-sig'))) if a.check else []
    if a.check and norm((ROOT/OUT.replace('.json','.md')).read_text(encoding='utf-8-sig'))!=md(o):err.append('Markdown stale')
    controls=self_test() if a.self_test else []
    print(json.dumps({'current':not err,'errors':err,'selected':'Y24_KEEP5_MINIMUM','STD':15,'TW_UPC':0,'writer_controls':controls},ensure_ascii=False))
    if err:raise SystemExit(1)
if __name__=='__main__':main()
