"""Selected LM1 rookie extension; future cap and qualifying awards stay typed."""
from __future__ import annotations
import argparse,copy,hashlib,json
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import build_chicago_2023_24_existing_contract_window as prior

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_lamelo_2023_selected_extension.py'
OUT='simulation/LAMELO_2023_SELECTED_EXTENSION.json'
SELECT='canon/DELEGATED_LAMELO_2023_EXTENSION_DESIGN_SELECTION_2026_10_08.json'
REVIEW='reviews/CHI_2023_CONTRACT_WINDOW_G11_INDEPENDENT_REVIEW_2026_10_08.json'
PINS={SELECT:'577cda6c17d836413834a8254364bf13328a521e7b8558a9b70e47c4abcbbc64',
 prior.OUT:'cf65846136975dd8b7f301505ad7fa06b564837f7962a607681632b84489d092',
 prior.ACTION:'542457d0b30ec2991faf0efa6c92a050dcd9120dfd929473ed29b90b7155f383',
 prior.SELF:'9af9056e8656df84c894b7ede00d91d0f3ef0c92c867089f1cb5ff2f400f7b8b',
 REVIEW:'d791ac98b6196a5ff8bf98e1ccd62e7868ec01019dd120cffc73ac323bf6bf3f',
 'control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md':'91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d'}
PAGES=[30,31,37,49,50,51,53,57,58,60,62,63,64,65,66,89,214,215,251,252,255,278,288,289,314,317,319]
YEARS=[2024,2025,2026,2027,2028]
MULT=[Fraction(1)+Fraction(2*i,25) for i in range(5)]

def norm(t):return t.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(norm((ROOT/p).read_text(encoding='utf-8-sig')).encode()).hexdigest()
def serial(o):return json.dumps(o,ensure_ascii=False,indent=2)+'\n'
def physical():
    for p,h in PINS.items():assert sha(p)==h,'Pinned source changed: '+p
    return {p:json.loads((ROOT/p).read_text(encoding='utf-8-sig')) for p in PINS if p.endswith('.json')}
def source_inputs():return physical()
def assert_sources(s):
    assert s==physical(),'Source objects differ from pinned physical input'
    assert prior.validate(s[prior.OUT],s[prior.ACTION])==[]
    z=s[SELECT];t=z['selected_terms']
    assert z['selected_form']=='LM1' and z['fictional_extension_signature_date']=='2023-07-07'
    assert z['selected_fictional_player_and_team_agreement'] and not z['new_human_author_lock']
    assert t=={'extended_salary_capyears':YEARS,
      'first_salary':'(1/4)*C24; (3/10)*C24 only if HigherMax criteria are legally met as defined in 2023 CBA ArticleII7',
      'annual_increases':'(2/25)*FIRST_EXTENDED_SALARY each following year, not compound8%',
      'new_bonuses':0,'protection':'FULL_SKILL_INJURY_FOR_ALL_FIVE_EXTENDED_SEASONS','options':'NONE',
      'first_higher_max_outcome_selected':False,'future_qualifying_award_or_NBA_MVP_year_selected':False,
      'FY23_new_salary':0,'FY23_new_STD_slot':0,'original2020_pick4_2023_fourth_RSC_year_preserved':True,
      'same_owner_Bird_service_not_reset':True}
    assert [(x['form'],x['selected']) for x in z['comparisons']]==[('LM1',True),('LM2',False),('LM3',False),('LM4',False)]
    original=next(r for r in s[prior.OUT]['named_contracts'] if r['player']=='LaMelo Ball')
    assert original['holder']=='CHI' and original['mechanism']=='2020_PICK4_EXERCISED_FOURTH_RSC_YEAR'
    assert original['FY23_salary_plus_all_performance_upper']==9835881 and original['last_selected_salary_capyear_start']==2023
    lm=s[prior.ACTION]['LaMelo_extension_forms'][0]
    assert lm['id']=='LM1' and lm['term']==5 and lm['raises']=='2/25' and lm['new_bonus']==0
    assert not lm['consent_selected'],'Original comparative history must remain unselected'
    assert z['source_sha256'][prior.OUT]==PINS[prior.OUT] and z['source_sha256'][prior.ACTION]==PINS[prior.ACTION]
    assert s[REVIEW]['independent_review_completed'] and not z['limits']['actual_private_player_or_team_acceptance_receipt_certified']

def primary():
    import fitz
    law=prior.LAW;raw=prior.RAW[str(law)]
    assert hashlib.sha256(law.read_bytes()).hexdigest()==raw
    d=fitz.open(law);texts={n:norm(d[n-1].get_text()) for n in PAGES};flat={n:' '.join(t.split()) for n,t in texts.items()}
    assert 'following July 6' in flat[30] and '12:00 p.m.' in flat[30]
    assert '12:01 p.m. eastern time' in flat[278] and 'second Option Year' in flat[278]
    assert 'will not be a Qualifying Veteran Free Agent' in flat[278]
    assert 'six (6) Seasons' in flat[319] and 'Rookie Scale Contract' in flat[319]
    assert 'may not include any Incentive Compensation' in flat[66]
    assert 'eight percent (8%)' in flat[251] and 'extended term' in flat[251]
    return {'url':'https://imgix.cosmicjs.com/25da5eb0-15eb-11ee-b5b3-fbd321202bdf-Final-2023-NBA-Collective-Bargaining-Agreement-6-28-23.pdf',
      'raw_cache_path':str(law),'raw_sha256':raw,
      'PDF1based_text_LF_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest() for n,t in texts.items()},
      'original_full_private_contract_or_future_awards_certified':False}

def assert_primary(p):
    import fitz
    law=prior.LAW;actual=hashlib.sha256(law.read_bytes()).hexdigest()
    assert p['raw_cache_path']==str(law) and p['raw_sha256']==actual==prior.RAW[str(law)],'Returned primary identity differs from physical 2023 CBA'
    assert p['url']=='https://imgix.cosmicjs.com/25da5eb0-15eb-11ee-b5b3-fbd321202bdf-Final-2023-NBA-Collective-Bargaining-Agreement-6-28-23.pdf'
    d=fitz.open(law)
    expected={str(n):hashlib.sha256(norm(d[n-1].get_text()).encode()).hexdigest() for n in PAGES}
    assert p['PDF1based_text_LF_sha256']==expected,'Returned page evidence differs from physical CBA text'
    assert not p['original_full_private_contract_or_future_awards_certified']

def terms(s):
    return {'player':'LaMelo Ball','team':'CHI','mechanism':'2023_VII7b_ROOKIE_SCALE_EXTENSION_II7d_PERCENT_FORM',
      'selected_form':'LM1','signature_date':'2023-07-07','signature_time_ET':'12:01:00',
      'opening_ET':'2023-07-06T12:01:00','closing_ET':'18:00 day before firstRegularDay of2023 secondOptionSeason',
      'closing_calendar_is_typed_not_exact_selected_date':True,
      'current_RSC_second_option_exercised':True,'current_second_option_salary_capyear':2023,
      'original_pick':4,'original_RSC_start':2020,'rendering_service_capyears':[2020,2021,2022,2023],
      'prospective_Qualifying_Bird':True,'service_condition':'Preserve original same-owner UPC/rendering family and no disqualifying service/right-reset event; no actual private receipt certification',
      'extended_salary_capyears':YEARS,'original_year_plus_extended_term':6,
      'last_extended_salary_capyear_start':2028,'last_extended_fiscal_end':'2029-06-30','fiscal_end_is_exact_service_term_end':False,
      'protection':'FULL_SKILL_INJURY_FOR_ALL_FIVE_EXTENDED_SEASONS','options':'NONE',
      'new_signing_trade_performance_or_other_bonus':0,'regular_salary_annual_raise_fraction':'2/25',
      'annual_multiplier_of_first':[str(x) for x in MULT],'raise_is_compound':False,
      'C24':'Lawfully prepared Salary Cap on2024-07-01, positive typed input, not2023cap',
      'first_salary_branches':{'ordinary':'C24/4','qualified_HigherMax':'3*C24/10'},
      'HigherMax_predicate':'2023II7a(i),c(i),d(i)-(ii) applicable completedfourYears/PriorTeam/award conditions at prescribed dates; not arbitrary flag',
      'award_windows':{'assessment':'2024-07-01 following fourthSeason',
        'criteria':'AllNBA1/2/3 or DPOY immediatelyprecedingSeason or2ofpreceding3; MVP1ofpreceding3',
        'already_qualifying_at_signature':'II7d(i) agreed30% form subjectII7c legalapplication',
        'not_yet_qualifying_at_signature':'II7d(ii) 25% or30% upon applicableHigherMax duringfourthRSCSeason'},
      'award_outcome_or_MVP_year_selected':False,'first_salary_actual_outcome':None,
      'future_salary_specific_amounts_deemed_on':'2024-07-01 underII7d; II7c max conformity applies',
      'FY23_new_salary':0,'new_STD_slot':0,'current_FY23_all_component_upper_preserved':9835881,
      'old_Gamma_and_original_protected_payments_preserved':True,'new_assignment_or_renegotiation_selected':False,
      'later_trade':'Unselected; if selected before2024Jul1, VII8g,higherMax assumption and104.5% currentcap acquisition average must be rechecked',
      'actual_private_assent_UPC_or_payment_receipt':None,'selected_fictional_agreement':True,
      'full_protection_is_death_protection_unlimited':False}

def assert_terms(t,s):
    assert t['player']=='LaMelo Ball' and t['team']=='CHI' and t['selected_form']=='LM1'
    assert t['mechanism']=='2023_VII7b_ROOKIE_SCALE_EXTENSION_II7d_PERCENT_FORM'
    assert t['signature_date']=='2023-07-07' and t['signature_time_ET']=='12:01:00'
    assert datetime.fromisoformat(t['signature_date']+'T'+t['signature_time_ET'])>datetime.fromisoformat('2023-07-06T12:01:00')
    assert t['opening_ET']=='2023-07-06T12:01:00' and t['closing_ET']=='18:00 day before firstRegularDay of2023 secondOptionSeason'
    assert t['closing_calendar_is_typed_not_exact_selected_date']
    assert t['current_RSC_second_option_exercised'] and t['current_second_option_salary_capyear']==2023
    assert t['original_pick']==4 and t['original_RSC_start']==2020 and t['rendering_service_capyears']==[2020,2021,2022,2023]
    assert t['prospective_Qualifying_Bird'] and t['service_condition']=='Preserve original same-owner UPC/rendering family and no disqualifying service/right-reset event; no actual private receipt certification'
    assert t['extended_salary_capyears']==YEARS and t['original_year_plus_extended_term']==6
    assert t['last_extended_salary_capyear_start']==2028 and t['last_extended_fiscal_end']=='2029-06-30' and not t['fiscal_end_is_exact_service_term_end']
    assert t['protection']=='FULL_SKILL_INJURY_FOR_ALL_FIVE_EXTENDED_SEASONS' and t['options']=='NONE'
    assert t['new_signing_trade_performance_or_other_bonus']==0 and t['regular_salary_annual_raise_fraction']=='2/25'
    assert t['annual_multiplier_of_first']==['1','27/25','29/25','31/25','33/25'] and not t['raise_is_compound']
    assert t['C24']=='Lawfully prepared Salary Cap on2024-07-01, positive typed input, not2023cap'
    assert t['first_salary_branches']=={'ordinary':'C24/4','qualified_HigherMax':'3*C24/10'}
    assert t['HigherMax_predicate']=='2023II7a(i),c(i),d(i)-(ii) applicable completedfourYears/PriorTeam/award conditions at prescribed dates; not arbitrary flag'
    assert t['award_windows']=={'assessment':'2024-07-01 following fourthSeason',
      'criteria':'AllNBA1/2/3 or DPOY immediatelyprecedingSeason or2ofpreceding3; MVP1ofpreceding3',
      'already_qualifying_at_signature':'II7d(i) agreed30% form subjectII7c legalapplication',
      'not_yet_qualifying_at_signature':'II7d(ii) 25% or30% upon applicableHigherMax duringfourthRSCSeason'}
    assert not t['award_outcome_or_MVP_year_selected'] and t['first_salary_actual_outcome'] is None
    assert t['future_salary_specific_amounts_deemed_on']=='2024-07-01 underII7d; II7c max conformity applies'
    assert t['FY23_new_salary']==t['new_STD_slot']==0 and t['current_FY23_all_component_upper_preserved']==9835881
    assert t['old_Gamma_and_original_protected_payments_preserved'] and not t['new_assignment_or_renegotiation_selected']
    assert t['later_trade']=='Unselected; if selected before2024Jul1, VII8g,higherMax assumption and104.5% currentcap acquisition average must be rechecked','Later trade requires its own VII8g matching and cap review'
    assert t['actual_private_assent_UPC_or_payment_receipt'] is None and t['selected_fictional_agreement']
    assert not t['full_protection_is_death_protection_unlimited']

def schedule_branches():
    result=[]
    for name,rate in [('ORDINARY_25_PERCENT',Fraction(1,4)),('LEGALLY_QUALIFIED_30_PERCENT',Fraction(3,10))]:
        result.append({'id':name,'condition':'Applicable HigherMax false' if rate==Fraction(1,4) else 'Applicable HigherMax legally satisfied; outcome not selected',
          'salary_coefficients_of_C24':[str(rate*m) for m in MULT],
          'total_coefficient_of_C24':str(sum(rate*m for m in MULT)),
          'annual_raise_coefficient_of_C24':str(rate*Fraction(2,25)),
          'new_bonus':0,'normal_equals_apron_player_component':True,'current_FY23_increment':0,
          'future_team_normal_apron_tax_costs_certified':False})
    return result
def assert_schedules(b):
    assert len(b)==2
    for row,name,rate in zip(b,['ORDINARY_25_PERCENT','LEGALLY_QUALIFIED_30_PERCENT'],[Fraction(1,4),Fraction(3,10)]):
        assert row['id']==name and row['salary_coefficients_of_C24']==[str(rate*(1+Fraction(2*i,25))) for i in range(5)]
        assert row['condition']==('Applicable HigherMax false' if rate==Fraction(1,4) else 'Applicable HigherMax legally satisfied; outcome not selected')
        assert row['total_coefficient_of_C24']==str(rate*Fraction(29,5)) and row['annual_raise_coefficient_of_C24']==str(rate*Fraction(2,25))
        assert row['new_bonus']==row['current_FY23_increment']==0 and row['normal_equals_apron_player_component']
        assert not row['future_team_normal_apron_tax_costs_certified']

def evaluate(C24,legally_qualified_HigherMax):
    """Numeric projection only after lawful cap and II7 eligibility supplied."""
    assert C24 is not None and Fraction(C24)>0 and type(legally_qualified_HigherMax) is bool
    rate=Fraction(3,10) if legally_qualified_HigherMax else Fraction(1,4)
    amounts=[Fraction(C24)*rate*m for m in MULT]
    assert all(amounts[i]-amounts[i-1]==amounts[0]*Fraction(2,25) for i in range(1,5))
    return {'annual_salary':[str(x) for x in amounts],'total':str(sum(amounts)),
      'normal_apron_player_component':[str(x) for x in amounts],
      'input_semantics':'C24 must be lawfulpreparedcap and boolean must be lawfullyresolvedII7 predicate; arbitrarypositivecap/award is not admitted',
      'actual_salary_or_future_team_cost_certificate':False}

def build():
    s=source_inputs();assert_sources(s);t=terms(s);assert_terms(t,s);b=schedule_branches();assert_schedules(b);p=primary();assert_primary(p)
    return {'id':'LAMELO_2023_SELECTED_EXTENSION','status':'REVIEW_PENDING_SELECTED_LM1_TYPED_ROOKIE_EXTENSION',
      'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8_BOM_STRIPPED_CRLF_CR_TO_LF_EXTERNAL_PDF_RAW_SEPARATE',
      'primary':p,'selected_terms':t,'future_salary_branches':b,'evaluator':SELF+'::evaluate',
      'legal_scope':{'signature':'July7 after July6 moratoriumend12:01ET, during RSC second-option extensionwindow; no new2017 signing rule applied',
        'eligibility':'Prior selected original2020CHI RSC with exercised2023fourthyear; prospectively QualifyingBird from sameowner precedingthreeSeasons',
        'term':'One remaining originalSeason+five extendedSeasons=IX1maximumsix, no options',
        'maximum':'II7c/d on2024Jul1; 25%ordinary/30%onlylawfulHigherMax, new incentive0 asII7drequires',
        'minimum':'Lawfulpreparedcap/minimum family: each salary also satisfies applicableII6; not arbitrary tiny C24 input',
        'raises':'VII5a3 annual8% FIRST extendedRegularSalary, no compound growth',
        'full_protection':'Skill and injury/illness in every extendedSeason; no unlimited death protection assertion',
        'cost':'FY23 newSalary0/STD0, unchanged fourthRSC upper9835881; future five Salary+Unlikely=base only',
        'hardcap':'Extension alone introduces no VII2eA-K transaction; future team expenses and later moves separately checked',
        'later_trade_not_selected':'VII8g acquisition average has special104.5%currentcap/noHigherMax assumption before firstextendedcapyear; no ordinary Salary shortcut'},
      'completion_scope':{'selected_fictional_agreement':True,'bounded_legal_extension_and_salary_function_complete':True,
        'independent_review_completed':False,'actual_contract_signature_receipt_or_player_acceptance':False,
        'future_prepared_cap_or_award_outcome_selected':False,'FY24_whole_team_cost':False,
        'franchise_MVP_year_title_count_or_ending_changed':False,'whole_macro3_or_career':False,
        'REGISTER_promotion':False,'manuscript':False},'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0}

def validate(o):
    try:
        assert o==build(),'Saved extension differs from source-bound reconstruction'
        assert_terms(o['selected_terms'],physical());assert_schedules(o['future_salary_branches']);assert_primary(o['primary']);return []
    except (AssertionError,KeyError,ValueError,TypeError) as e:return [str(e)]
def md(o):
    return '\n'.join(['# LaMelo 2023 선택 LM1 연장 실행','',o['status'],'',
      'Root의 기존 Chicago 성장코어 위임으로 **LM1, 가상 July7 5년 fully skill/injury protected·옵션0·신규보너스0** 합의를 소비한다. LM2/3/4 비교 이력은 선택으로 바꾸지 않는다. 실제 선수 수락·계약 접수·미래 cap/수상 결과는 인증하지 않는다.','',
      '## 현재와 연장기간','',
      '2020 Chicago#4 원 RSC의 2023–24 네 번째 해를 그대로 유지한다. 현재 모든성분 상단 **$9,835,881**, 연장에 따른 **FY23 Salary0/STD0 추가**다. 2024–25부터 2028–29까지 새 다섯 해가 붙어 서명일 기준 원 남은 한 해+연장5=6년이며 IX1 한도와 맞는다. Fiscal 끝점은 마지막 연장해 2029June30이고 실제 서비스 종료일을 인증하지 않는다.','',
      '2023CBA VII7b(PDF278)는 마지막 moratorium날 12:01ET 이후부터 RSC 두 번째 옵션해 정규시즌 첫날 전날18:00ET까지를 허용한다. I1mm(PDF30)의 July6 정오 종료 다음날 **July7 12:01ET** 가상서명이다. 원 same-owner UPC·실제 작품 서비스 가족이 유지되어 계약종료 때 QualifyingBird가 되는 범위를 소비한다. 미래개인 영수증은 이 구성의 새로운 gate가 아니다.','',
      '## 미래 가격 함수','',
      '| 분기 | FY24..28의 C24 계수 | 총계 |','|---|---|',
      '| 법정 ordinary | 1/4, 27/100, 29/100, 31/100, 33/100 | 29/20 C24 |',
      '| 법정 HigherMax 충족 | 3/10, 81/250, 87/250, 93/250, 99/250 | 87/50 C24 |','',
      '`C24`는 **2024July1의 적법한 준비 cap**이다. 2023 cap을 대신 넣지 않는다. 매년 `firstSalary×8%`를 더하며 8% 복리나 차년도 cap 재계산이 아니다. II7d(PDF64–66)의 이미 요건 충족/아직 미충족 서명형식을 구별하고 II7c/a에 따른 시점·4YOS·PriorTeam·AllNBA/DPOY/MVP 요건을 충족하는 경우에만 30%를 적용한다. 수상 여부·MVP 연도·정확 미래급여는 미선택이다. Incentive Compensation은 해당 법형식에서 금지되고 새 signing/trade/기타bonus도0인 선택형태다.','',
      '## 비용·후손 범위','',
      '원 모든Γ와 기존 보호채무를 보존하며 새 이적/재협상은 선택하지 않는다. 연장만으로 당해 apron hardcap을 유발하지 않는다. 새 다섯 해의 player normal/apron 성분은 보너스 없는 baseSalary지만 **전체 FY24 팀장부/Tax 비용을 인증하지 않는다**. 후행 이적을 선택하면 VII8g(PDF288–289)의 acquiring 평균·104.5% cap·HigherMax미충족 가정 등 별도matching이 필요하며 그 양도를 여기서 자동 허용하지 않는다.','',
      '현재 선택된 계약형태와 두 합법적 미래함수 분기를 구현한 소범위다. 실제 cap/수상/임상·시즌승패/전체macro3·원고는 별도다.','',prior.progress()])+'\n'
def self_test():
    s=source_inputs();done=[]
    for label,field,value in [('current_year_charge','FY23_new_salary',1000000),('unearned_HigherMax','award_outcome_or_MVP_year_selected',True),
      ('compound_raise','annual_multiplier_of_first',['1','27/25','729/625','19683/15625','531441/390625']),
      ('wrong_signature_year','signature_date','2022-07-07'),('drop_old_Gamma','old_Gamma_and_original_protected_payments_preserved',False)]:
        t=terms(s);t[field]=value
        try:
            with patch(__name__+'.terms',return_value=t):build()
        except AssertionError:done.append(label)
        else:raise AssertionError('FALSE PASS '+label)
    b=schedule_branches();b[1]['salary_coefficients_of_C24'][0]='7/20'
    try:
        with patch(__name__+'.schedule_branches',return_value=b):build()
    except AssertionError:done.append('illegal_35_percent')
    else:raise AssertionError('FALSE PASS max')
    t=terms(s);t['later_trade']='automatic trade legal with no matching or cap review'
    try:
        with patch(__name__+'.terms',return_value=t):build()
    except AssertionError:done.append('automatic_future_trade')
    else:raise AssertionError('FALSE PASS future trade')
    p=primary();p['raw_sha256']='0'*64
    try:
        with patch(__name__+'.primary',return_value=p):build()
    except AssertionError:done.append('primary_identity_reversal')
    else:raise AssertionError('FALSE PASS primary identity')
    return done
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');args=a.parse_args();o=build()
    if args.write:
        (ROOT/OUT).write_text(serial(o),encoding='utf8',newline='\n');(ROOT/OUT.replace('.json','.md')).write_text(md(o),encoding='utf8',newline='\n')
    errors=[]
    if args.check:
        saved=json.loads((ROOT/OUT).read_text(encoding='utf-8-sig'));errors=validate(saved)
        if norm((ROOT/OUT.replace('.json','.md')).read_text(encoding='utf-8-sig'))!=md(saved):errors.append('Markdown stale')
    tests=self_test() if args.self_test else []
    print(json.dumps({'current':not errors,'errors':errors,'selected':'LM1','future_capyears':5,'FY23_increment':0,'negative_controls':tests},ensure_ascii=False))
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
