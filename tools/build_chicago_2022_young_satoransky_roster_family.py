"""Two expired veterans: unselected named forms and additive FY22 roster/cost inputs."""
import argparse,copy,hashlib,json
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import fitz
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_young_satoransky_roster_family.py'
OUT='research/CHICAGO_2022_YOUNG_SATORANSKY_ROSTER_FAMILY_2026_10_07.json'
MD=OUT[:-5]+'.md'
MATRIX='research/CHICAGO_2022_COMBINED_CONTRACT_COST_MATRIX_2026_10_07.json'
CONT='simulation/CHICAGO_2021_23_CONTINUATION_INPUTS.json'
A='canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json'
PINS={'research/CHICAGO_2022_COMBINED_CONTRACT_COST_MATRIX_2026_10_07.json': '1ba9e120872bdfab40f26fe2b56a6cff8c6265d94280ea84b5970ffb0d537d33', 'tools/build_chicago_2022_combined_contract_cost_matrix.py': 'be8787d57ff56b60e93326b073321a32333aa4fef6d5f48a520ceb3957a65259', 'simulation/CHICAGO_2021_23_CONTINUATION_INPUTS.json': '5632957e5e0a02f2d6f241900a3bef2c5790a8993c3494986e383ca3cbff1be3', 'research/CHICAGO_2021_23_CONTINUATION_SOURCES.json': '4dc3cfb7416174c0fea5c2710e9915a729d362dc553f216f4e9c861b373e9db3', 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json': '9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce', 'research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json': '7244beff7a120c5ca246a04e72b61586f3cfbe245487d5fc6479f5245fd78d9f', 'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2'}
CBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
PAGES=[37,38,39,40,54,55,56,57,58,59,64,65,74,75,80,197,198,200,208,209,210,212,213,218,219,220,221,223,232,233,240,241,252,253,299,309,315,317,398,399,412,561]
TEMP=Path('C:/Users/Storm Credit/AppData/Local/Temp')
RAW=[{'id':'YOUNG_REUSED_CONTRACT_REPORT','url':'https://www.salaryswish.com/players/thaddeus-young','path':str(TEMP/'fr-chi-2021-retained-thaddeus-young-20261007.html'),'sha':'59113868938e938d8c78cc924891ae242dd407b2e35af2f833798b3f152a9b80'}, {'id':'SATORANSKY_REUSED_CONTRACT_REPORT','url':'https://www.salaryswish.com/players/tomas-satoransky','path':str(TEMP/'fr-chi-2021-retained-tomas-satoransky-20261007.html'),'sha':'786358ed1a147e00b7f835aea084308acf481828d1be8c642c0f63ccd9a624c5'}, {'id':'MINIMUM_REUSED_SECONDARY','url':'https://www.salaryswish.com/minimum-salary-faq','path':str(TEMP/'first-rebound-minimum-year2-20261007/salaryswish_minimum.html'),'sha':'0c808010bd97008e17d7b59c2a610270bc528e7f3f04b48f12a8ec6ceb70eefe'}, {'id':'NBA_CAP2022_REUSED_PRIMARY','url':'https://pr.nba.com/nba-salary-cap-2022-23-season/','path':str(TEMP/'first-rebound-chi-core2022-20261007/NBA_CAP2022.html'),'sha':'2e76093cfc91b6257f18cddd25441090118f36bd8a942259fbc340438ff5e57f'}]

def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
MATRIX_MEANING_SHA='01d05685fb87a936879c1bccc18e1b8dc0a1b49476faca884998ab97847dd268'
def source_inputs():return load(CONT),load(A),load(MATRIX)
def forms():
    common={'classification':'UNSELECTED_CONSENSUAL_FORM_CANDIDATE','proposed_execution_ET':'2022-07-07T12:00:00-04:00','effective_not_before_execution':True,'actual_consent':None,'contract_selected':False,'full_base_skill_injury_protection':True,'standard_CBA_conditions_and_payment':True,'options':[],'ETO':False,'signing_promotional_loan_or_international_additions':0}
    y=[{'id':'Y_BIRD_8M','player':'Thaddeus Young','action':'DIRECT_CHICAGO_FULL_BIRD','years':2,'base_schedule':[8000000,8000000],'performance_bonus_proposal':0,'trade_bonus_rate_interval':['0','3/20'],'actual_trade_bonus_rate':None,**common}, {'id':'Y_MINIMUM','player':'Thaddeus Young','action':'LEGAL_MINIMUM_EXCEPTION','years':1,'base_schedule':'L_2022_23(creditedYOS,Year1)','all_bonuses':0,**common}, {'id':'Y_RENOUNCE','player':'Thaddeus Young','action':'NO_NEW_UPC_AND_VALID_VII4g_RENUNCIATION','effective_candidate':'2022-07-07','destination':None,'contract_selected':False,'actual_consent':None}, {'id':'Y_HOLD_OPEN','player':'Thaddeus Young','action':'NO_NEW_UPC_KEEP_FA_HOLD_AND_BIRD','destination':None,'contract_selected':False,'actual_consent':None}]
    s=[{'id':'S_MINIMUM','player':'Tomas Satoransky','action':'LEGAL_MINIMUM_EXCEPTION','years':1,'base_schedule':'L_2022_23(creditedYOS,Year1)','all_bonuses':0,**common}, {'id':'S_RENOUNCE','player':'Tomas Satoransky','action':'NO_NEW_UPC_AND_VALID_VII4g_RENUNCIATION','effective_candidate':'2022-07-07','destination':None,'contract_selected':False,'actual_consent':None}, {'id':'S_HOLD_OPEN','player':'Tomas Satoransky','action':'NO_NEW_UPC_KEEP_FA_HOLD_AND_BIRD','destination':None,'contract_selected':False,'actual_consent':None}]
    return y,s

FORM_MEANING={'sha': '350417726b320f5f9e53ad143e3ed16e726612f7cc1712d2a85b0b98f438917f'} # fixed candidate semantic digest
def check_forms(y,s):
    assert hashlib.sha256(json.dumps([y,s],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==FORM_MEANING['sha'],'Named contract mechanism/terms/timing changed'
    assert len(y)==4 and len(s)==3
    for f in y+s:
      assert f['contract_selected']is False and f['actual_consent']is None
      if f['action']=='LEGAL_MINIMUM_EXCEPTION':assert f['years']==1 and f['all_bonuses']==0
    assert y[0]['base_schedule']==[8000000,8000000] and y[0]['performance_bonus_proposal']==0

def component(f,done):
    young=f['player']=='Thaddeus Young';hold=28861000 if young else 19000000
    if not done or f['action']=='NO_NEW_UPC_KEEP_FA_HOLD_AND_BIRD':return {'normal_upper':hold,'apron_upper':0,'new_STD':0,'FA_hold_live':True,'re_signing_Bird_retained':True,'live_UPC':False,'actual_total_player_payment':None}
    if f['action']=='NO_NEW_UPC_AND_VALID_VII4g_RENUNCIATION':return {'normal_upper':0,'apron_upper':0,'new_STD':0,'FA_hold_live':False,'re_signing_Bird_retained':False,'live_UPC':False,'actual_total_player_payment':None,'zero_scope':'THIS_FA_HOLD_ONLY; ACCRUED/LEGACY_PAYMENT_NOT_ERASED'}
    cost=8000000 if f['action']=='DIRECT_CHICAGO_FULL_BIRD'else 3000000
    return {'normal_upper':cost,'apron_upper':cost,'new_STD':1,'FA_hold_live':False,'re_signing_Bird_retained':True,'live_UPC':True,'actual_salary':None,'actual_total_player_payment':None,'upper_is_chosen_salary':False,'minimum_full_cash_overreserve_not_reimbursement_certified':f['action']=='LEGAL_MINIMUM_EXCEPTION'}

def assert_component(f,done,row):
    # Independent caller contract: source form identifies the permitted component.
    # Keep the conservative minimum screen independent of component()'s return.
    hold=28861000 if f['player']=='Thaddeus Young' else 19000000
    live=done and f['action'] in ('DIRECT_CHICAGO_FULL_BIRD','LEGAL_MINIMUM_EXCEPTION')
    open_hold=not done or f['action']=='NO_NEW_UPC_KEEP_FA_HOLD_AND_BIRD'
    cost=hold if open_hold else (8000000 if live and f['id']=='Y_BIRD_8M' else 3000000 if live else 0)
    expected=(cost,0 if open_hold else cost,int(live),open_hold,open_hold or live,live)
    keys=('normal_upper','apron_upper','new_STD','FA_hold_live','re_signing_Bird_retained','live_UPC')
    assert tuple(row[k]for k in keys)==expected,'Source form and derived cost/slot/hold/Bird component disagree'
    assert row['actual_total_player_payment']is None and row.get('actual_salary')is None,'Component must not select private payments'
    if live:
      assert row['upper_is_chosen_salary']is False
      assert row['minimum_full_cash_overreserve_not_reimbursement_certified']==(f['action']=='LEGAL_MINIMUM_EXCEPTION')
    elif not open_hold:
      assert row['zero_scope']=='THIS_FA_HOLD_ONLY; ACCRUED/LEGACY_PAYMENT_NOT_ERASED'

def build():
    for p,h in PINS.items():assert sha(p)==h,'Unreviewed input '+p
    c,a,m=source_inputs()
    assert hashlib.sha256(json.dumps(m,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==MATRIX_MEANING_SHA,'Reviewed matrix cost/contract meaning changed'
    assert a['selected']['route']=='G1A_PLUS_M1' and 'later contracts' in str(a['not_approved'])
    assert c['salary_reference_2021_2022']['Young']==[14190000,8000000] and c['salary_reference_2021_2022']['Satoransky']==[10000000,None]
    assert c['young_2022_including_bonus_candidates']==[2000000,8650000]
    assert m['coverage']['numeric_branches']==165 and m['coverage']['dated_cost_rows']==660
    assert m['certification']['independent_review_completed']is True and m['certification']['whole_FY22_roster_cost_or_results']is False
    assert len(m['conditional_rows'])==165 and len({r['id']for r in m['conditional_rows']})==165
    assert all(r['dated_states'][-1]['signed_standard_contracts_in_named_family']==13 and r['dated_states'][-1]['X_actual']is None for r in m['conditional_rows'])
    y,s=forms();check_forms(y,s)
    observations=[]
    for r in RAW:
      b=Path(r['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==r['sha'];doc=BeautifulSoup(b,'html.parser');plain=doc.get_text(' ',strip=True)
      if r['id']=='YOUNG_REUSED_CONTRACT_REPORT':
        tabs=[t.get_text(' ',strip=True)for t in doc.find_all('table')]
        assert any('2021-22 $14,190,000'in t and '$1,000,000'in t for t in tabs)
        assert any('2022-23 $8,000,000'in t and '$650,000'in t for t in tabs)
        locator='2019three-year table last2021-22 row;2022TOR tablebase8m/unlikely650k, terms/report notalternateconsent'
      elif r['id']=='SATORANSKY_REUSED_CONTRACT_REPORT':
        assert any('2019-20 $10,000,000'in t.get_text(' ',strip=True) and '2021-22 W $10,000,000' in t.get_text(' ',strip=True) for t in doc.find_all('table'))
        locator='2019WAS→CHI three-year last2021-22 row; laterSASbuyout/WAS468119 notimported'
      elif r['id']=='MINIMUM_REUSED_SECONDARY':
        rows=doc.select('tbody#cba_2023 tr');last=[td.get_text(' ',strip=True)for td in rows[-1].find_all('td')]
        assert last[0]=='10' and last[1]=='$2,905,851'
        locator='tbody#cba_2023 Year1; data-year2023 labels2022-23. data-year2022 is2021-22 andNOTused.'
      else:assert '$123.655 million'in plain and 'noon ET on Wednesday, July 6'in plain;locator='June30 NBArelease cap/calendar openingparagraphs'
      observations.append({**r,'raw_bytes':len(b),'class':'PRIMARY_NBA_RELEASE_REUSED_DIRECT_READ'if r['id'].startswith('NBA')else'SECONDARY_REUSED_DIRECT_TABLE_READ','locator':locator})
    assert hashlib.sha256(CBA.read_bytes()).hexdigest()==CBA_SHA
    with fitz.open(CBA)as d:
      pages=[{'PDF_1based':n,'text_LF_sha256':hashlib.sha256(d[n-1].get_text().replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()}for n in PAGES]
      assert 'specific numerical' in d[37].get_text() and 'three (3) or fewer' in d[316].get_text()
      assert 'four (4) or more' in d[73].get_text() and 'with no bonuses' in d[232].get_text()
    minimum_proxy=Fraction(2328652*123655000,99093000);proxyceil=-(-minimum_proxy.numerator//minimum_proxy.denominator)
    assert 2000000<minimum_proxy<3000000 and 650000<Fraction(8000000*15,100)
    cases=[];joined=[];joinedcount=0
    for yf in y:
      for sf in s:
        states=[]
        for i,(date,event)in enumerate([('2022-07-01','EXPIRED_KEEP_BOTH_UFA_HOLDS'),('2022-07-07','AFTER_PRIMARY_THREE_FORMS_THEN_Y_ACTION'),('2022-07-07','AFTER_S_ACTION')]):
          yc=component(yf,i>=1);sc=component(sf,i>=2)
          assert_component(yf,i>=1,yc);assert_component(sf,i>=2,sc)
          states.append({'date':date,'within_leaf_order':i,'event':event,'Young':yc,'Satoransky':sc,'normal_sum_upper':yc['normal_upper']+sc['normal_upper'],'apron_added_upper':yc['apron_upper']+sc['apron_upper'],'added_STD':yc['new_STD']+sc['new_STD'],'base_contract_count':'MATRIX_STATE0_IF_JULY1_ELSE_MATRIX_STATE3; NOT13BEFOREPRIMARYFORMS'})
        caseid=yf['id']+'__'+sf['id'];case={'id':caseid,'Young_form':yf['id'],'Satoransky_form':sf['id'],'states':states,'post_primary_plus_veterans_STD':13+states[-1]['added_STD'],'remaining_STD_slots':2-states[-1]['added_STD'],'TW_slots_not_used_by_veterans':2,'remaining_offseason_slots_if_no_other_signed_players_and_TW2':20-13-states[-1]['added_STD']-2,'direction_selected':False}
        assert 13<=case['post_primary_plus_veterans_STD']<=15
        cases.append(case)
        for p in m['matrix']:
          originals=[r for r in m['conditional_rows']if r['Carter']['policy']==p['Carter']and r['Protagonist']['policy']==p['Protagonist']]
          cells=[]
          for stage,vs in enumerate(states):
            vals=[]
            for r in originals:
              b=r['dated_states'][0 if stage==0 else 3]
              normal=b['normal_cost_known_upper_including_unrenounced_Young_Satoransky_holds']-47861000+vs['normal_sum_upper']
              apron=b['apron_cost_known_upper_excluding_UFA_holds']+vs['apron_added_upper']
              signed=b['signed_standard_contracts_in_named_family']+vs['added_STD']
              assert signed<=15
              vals.append((normal,apron,signed));joinedcount+=1
            upper=max(t[1]for t in vals);normalupper=max(t[0]for t in vals)
            cells.append({'leaf_stage':stage,'date':vs['date'],'all_source_branches':len(vals),'normal_known_upper':normalupper,'apron_known_upper':upper,'signed_STD_range':[min(t[2]for t in vals),max(t[2]for t in vals)],'X_OTHER_sufficient_upper':156982000-upper,'X_OTHER_actual':None,'whole_FY22_PASS':False,'Young_reported_650k_extra_stress_X_allowance':156982000-upper-(650000 if stage>=1 and yf['id']=='Y_BIRD_8M'else 0)})
          joined.append({'case':caseid,'Carter':p['Carter'],'Protagonist':p['Protagonist'],'stages':cells,'original_165_branch_data_not_duplicated':True})
    assert len(cases)==12 and len(joined)==192 and joinedcount==5940
    return {'id':'CHICAGO_2022_YOUNG_SATORANSKY_ROSTER_FAMILY_2026_10_07','status':'INDEPENDENTLY_REVIEWED_UNSELECTED_NAMED_VETERAN_FORMS_AND_COST_INPUTS','baseline_main':'e8070d14e7cfa43eab17c7e1cf62c5cbc71bba85','source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8 BOMstrip CRLF/CR toLF; rawbytes hashes separate','raw_body_observations':observations,'CBA2017':{'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(CBA),'raw_sha256':CBA_SHA,'direct_text_pages':pages},'source_authority':{'approved':'2021A retains both through lastcontractyear only; no2022newcontract/destination authorlock.','secondary':'Youngprior14.19m+up1m;Sato10m; oldTORnew8m+650konlycomparison. No originalTORcriteria/likely/privateguarantee/acceptance inherited.','candidate':'NewplainYoung8m×2 fullBird and statutoryminimum1year forms; renounceorretainuncontractedrights. No new performancecriterion selected.','inference':'Priorservice>3/completedservices+unbrokenprior-teamcontracts admit UFA/fullBird family; actualclinical/receipt not certified.'},
      'admitted_contract_window':{'prior_term_end':'2022-06-30','services_condition':'CompletedpriorStandardcontracts by renderingservices; noXI3withholding/differentFAteamchange; alreadychosenChicago2021contractyeardirection preserved.','Young_credit_class':'>=10YOS reference15','Satoransky_credit_class':'>3YOS reference6','exact_future_YOS_medical_or_services_certified':False,'UFA_no_QO_or_ROFR':True,'two_way_allowed_for_either_veteran':False,'Bird_condition':'Three covered priorseasons withCHI/no disqualifyingFAteamchange; Sato2019assignment preservesexistingrights. ValidJuly1+renunciation intentionally removesexceptionright.','new_signing_candidate_ET':'2022-07-07T12:00:00-04:00','primary_moratorium_ends':'2022-07-06T12:00:00-04:00','Bird_signing_window_opens':'2022-07-06T12:01:00-04:00','leaf_actor_order_after_primary_forms':True,'new_contracts_not_backdated_toJune30_orJuly1':True},
      'forms':{'Young':y,'Satoransky':s},'hold_domain':{'Young_prior_Salary_for_VII4d_only':[14190000,15190000],'Young_generic_FA_safe_upper':28861000,'Young_reported_150pct_base_only_hold':21285000,'Young_earned1m_or_EstimatedAverage_test_not_selected':True,'Satoransky_prior_Salary':10000000,'Satoransky_generic_FA_safe_upper':19000000,'hold_renounce_effect':'Hold/component andBirdright only; accruedprotected/legacy costs stay inpriorwholecategoryreservation. Foreignteamcontract alone notlisted as automaticNBAFAhold removal.','ordinary_UFA_hold_component_apron':0,'uncontracted_free_agent_is_STD':False},
      'minimum_rule':{'signing_scale_cap_year':'2022-23','contract_year':1,'salary':'EXACT_APPLICABLE_II6_EXC_FUNCTION; NO_BONUSES_ALLKINDS; NOT_ARBITRARY3M_AGREEDBASE','credit_YOS_exact_selected':None,'maximum_table_reference_10plus_Year1':2905851,'ExC2017_highest_Year1_scaled_rational':{'numerator':minimum_proxy.numerator,'denominator':minimum_proxy.denominator},'proxy_ceil':proxyceil,'fullcash_upper_if_statutorytable_at_or_below_screen':3000000,'exact_statutory_rounding_or_negotiated_cents_certified':False,'old_2m_replacement_reserve_is_Young_minimum_contract':False,'one_year_veteran_min_reimbursement':'VII3(f)/IV6(g)(2) qualifyingone-year veteran cost may exclude league-fund reimbursed amount; thisscreen keepsfullcash andusesnosubtraction. This is not a2mcap-identity or3mactualsalary.','year2_2023_scale_not_needed_for_one_year_form':True,'normal_and_apron_floor':'Bothveteranscredit>3, theirlegalminimum≥2YOSfloor; no0/1YOSupliftcircumvention;TWcannotfreeSTDslot.'},
      'Bird_8m_form_checks':{'base_schedule':[8000000,8000000],'new_performance_bonus':0,'all_new_other_additions_except_future_Ex4_family':0,'maximum_35pct_first_cap_reference':43279250,'base_below_even_25pct_cap_reference':True,'8pct_raise_limit':640000,'actual_raise':0,'term2_below_fullBird5':True,'full_protection_proposal_not_historical_year2_1mguarantee':True,'budget_report_sensitivity':{'base':8000000,'reported_extra_bonus_closed_interval':[0,650000],'all_performance_apron_outer':8650000,'not_a_selected_new_clause':True,'if_clause_later_proposed':'II3b numericalpositiveNBAstatistics andVII5d15%unlikelylimit/3d likelyclassification; no rostereligibilitybonus. Reopensexactformbutboundedcoststressalreadycomputed.','classification_and_earned_actual':None},'direct_same_team_retention_does_not_trigger_its_trade_bonus':True,'actual_Ex4_rate':None},
      'trade_descendants':{'no_new_trade_selected':True,'FA_forms_earliest_ordinary_trade':'max(sign+3months,2022-12-15)','Jan15_rule':'PlainYoung8m<120%prior14.19m;minforms expresslyexemptVII8d3. No selectedfuturetrade/matchingcertificate.','one_year_min_form_prior_Bird_consent':'VII8b requiresplayerconsent; iftraded countsFAchange andBirdcontinuityreopens. Actualconsentnull.','minimum_forms_Ex4_bonus':0,'minimum_zero_reason':'These new minimum-form candidates expressly choose all bonuses zero, including Ex4. II6(f) permits specified exceptions to no-bonuses language; statutory minimum alone is not proof every trade bonus is impossible or an old private bonus is absent.'},
      'cases':cases,'joined_policy_cost_inputs':joined,'coverage':{'named_cases':12,'actor_date_states':36,'compact_policy_cells':192,'joined_underlying_cost_checks':5940,'all165_baseline_branches_preserved':True,'new_contracts_selected':0},
      'slot_and_remaining_category_map':{'STD_base_after_three_primary_forms':13,'STD_capacity_regular':15,'TW_capacity':2,'offseason_capacity_includes_TW':20,'two_veteran_signatures':'STD15 leavesnoSTDplacefor2022signedrookieunlessa namedexistingcontractchange is separatelymodeled.','one_or_zero_veteran_signatures':'1or2STDspaces remain; hold-openplayerisnotliveUPC and canstillnegotiatewithoutoccupyingstandardroster.','hold_and_incomplete':'10core+3primarylivecontracts already13; allcasespostprimary haveincompletecapcharge0 evenbothrenounce, not renounce-generatedminimumfakecost.','Y_depart_2m_replacement':'Original2m comparisonreserve notnamedreplacement orsignedcost. Draftrookieorvetreplacement needslegalfloor/contractandcannotbeautoadded.','X_OTHER':'Allnonmodeled2022rookie/tender,DotsonCookTWexpiryQO/FRN/youngFAfloor,annualgenericexceptionincorporation/usage/renounce,newwaivercosts ornamed preservedliability beyondacceptedcarryfamily. Xactualnull; prior20.743601m reservation remainsinmatrix.','no_hardcap_2021_carry':True,'ordinaryBird_or_minimum_alone_new_hardcap':False,'complete_FY22_privateorpubliccost_certified':False},'next_finite_work':['Selectcomparativecontractdirections onlyatconsequentialdecision; keeproutine2022draft/tender/TW/annualexceptionmapping moving.','Assignnamed2022rookiecontracts againstremainingSTDspaces; retentionbothveteranscannotbecombinedwithunmodified13+newrookies.','JoinothercostsX_OTHER withall5940dateinputs andnewactualtriggers; a negativeconservativescreen is notillegalordinaryBirdorlowerboundproof.'],
      'certification':{'independent_review_completed':True,'actual_player_team_contract_consent':None,'actual_private_terms_or_cents_certified':False,'selected_Young_or_Satoransky_direction':None,'whole_FY22_roster_cost_or_results':False,'whole_macro3_complete':False,'new_author_lock':False,'central_or_REGISTER_promotion':False,'manuscript_written':0}}

def validate(o):
    try:assert o==build(),'Output not current source/meaning';return []
    except(AssertionError,KeyError,ValueError,OSError)as e:return[str(e)]
def markdown(o):
    lines=['# Chicago2022 Young·Satoransky: 만료·명단 두 칸의 후보 가족','',o['status'],'','A의 작가 선택은2021 마지막 계약연도를 유지하는 방향이며2022 재계약·행선지를 선택하지 않았다. 이번12개 조합은 모두 CANDIDATE이고 실제 선수·팀 동의나 미래 계약을 확정하지 않는다.','', '## 제안과 공개 보고의 차이','', 'Young 새plain Bird 후보는 $8m×2년, 새성과보너스0·전액skill/injury보호·표준조건·옵션없음이다. 기존TOR 계약표의 $8m+650k는 역사적 비교 보고이며, 그 성과조건/likely분류/부분보장/동의를 Chicago에 상속하지 않는다. $650k 추가범위는 별도 apron 비용 감도로만 남겨 모든 합산에 연결했다. 원제안에 없는 새 minutes 문턱을 만들지 않았다.','Young의 다른 후보는 법정 최소1년, 미서명권리 보유,7월7일 유효권리 포기다. Satoransky는 법정 최소1년/미서명권리 보유/권리 포기 세 후보다. 기존2m는 **replacement예비비**이며 Young 계약급여나 이름 없는 대체선수 계약이 아니다.','법정최소는2022서명 Year1 적용 함수다. [공개최소표](https://www.salaryswish.com/minimum-salary-faq)의2022–23최고10+ 행 $2,905,851과ExC scaling을 대조했고3m는 조건부 fullcash상단으로만 예약했다. 실제3m급여·정확법정반올림·reimbursement비율을 확정하지 않는다. 최소 후보는1년이고 새 합의안에서 모든 보너스를0으로 명시한다. II6(f)의 trade-bonus 예외를 없다고 주장하지 않으며, Bird8m2년과별도이고NTMLE/RoomMLE 예산을 소비하는 계약이 아니다.','', '## 12명명 조합 / 36 actor-date 상태','', '|Young|Satoransky|두 계약 실행 뒤 STD|남은 STD|','|---|---|---:|---:|']
    for c in o['cases']:lines.append(f"|{c['Young_form']}|{c['Satoransky_form']}|{c['post_primary_plus_veterans_STD']}|{c['remaining_STD_slots']}|")
    lines+=['','July1 원기간 만료 뒤 두FAhold 유지 → July7 기존 세 핵심계약 후보 이후Young 행동 → Sato 행동의 조건부 순서다. July1에 먼저13계약을 소급하지 않고matrix의실제conditionallive계약수와연결한다. 같은날순서는가상작업용이며실접수0, 새계약은실행전기간으로backdate하지않는다.','>3YOS의완료된standard계약군이어서 QO/ROFR없는UFA다. 최근3시즌Chicago 계약·completedservices·불적격FAteamchange없음은허용가족조건이며실임상/개인서류인증이아니다. 둘은4+YOS이므로TW로옮겨표준슬롯을비울수없다.','Young normalhold상단28,861,000은 priorRegular14.19m+earnedperformance0..1m의190%상단, Sato19m은10m의190%다. 미서명유지면 hold남고STD를차지하지않는다. 권리포기는해당hold/Bird권리만지우고과거보장부채를지우지않는다. 외국구단서명만으로NBAFAhold가자동없어진다고쓰지않는다. UFAhold자체apron0과실제계약/과거지급0은다르다.','새minimum1년은같은priorBird를다음해유지할수있는계약이므로미래양도에VII8b 선수동의가필요하고양도후FAteamchange로권리가바뀐다. 실제양도/동의/수락은미선택이다.','', '## 기존165가족과 전체 비용의 연결','', '12조합을16정책셀에compact연결했다. 실제5940개(12×165×3) underlying 날짜별 normal/apron/STD 계산을검산하고원165벡터를복제하지않는다. 일반cap에서기존Young/Satohold47,861,000을먼저빼고현재live-or-hold성분을넣으며, apron에는새계약상단만추가하여중복hold를피한다.','두베테랑서명이면13+2=15STD라2022신인UPC를추가할수없다. 신인/TW/unsignedtender는별도명명계약·권리기간·자격·비용을모델링해야한다. 둘중1명또는0명이서명하면1칸또는2칸이남으며미서명hold를명단선수로세지않는다. offseason20은TW를포함한다.','X_OTHER는신인/tender·Dotson/CookTW만료및QO/FRN/floor·예외산입/포기/사용·새방출비용등의남은명명범주이며실제상단null이다. 기존legacy20,743,601은유지한다. 부채없는0/미보고미래합의를무한추가하는족/사적증서필수gate를만들지않았다. 2021hardcap은2022로이월하지않고Bird/최소예외자체로새hardcap을추가하지않는다. 수치여유와전체FY22통과는구별한다.','', '[2017CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) II3/5/6/7/11, VII3(d)/4(d)(f)(g)/5/6(b)(i)(m)/8,IX1,XI1/3/4,XXIV2,XXIX1 및 [NBA2022cap/calendar](https://pr.nba.com/nba-salary-cap-2022-23-season/) 원자료를대조했다. 기존vendor3/primaryNBA1 raw를재사용해읽었으며새회수/외부독립검문성공을미리계수하지않는다.','', '|번호|묶음|상태|','|---|---|---|','|1|2020드래프트연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23계약·거래|베테랑12후보·36상태;선택/전체cost 남음|','|4|장기커리어|후속입력대기|','|5|결말·전체구조|전체기능표미완료|','|6|집필규격·ContextPack|현행누적등록기참조·Pack0|','|7|통합·독립·작가승인|최종CLOSED|','','미완료큰묶음5 / v0.30 PARTIAL / 설계·원고CLOSED / 원고0.','']
    return '\n'.join(lines)
def self_test():
    y,s=forms();bad=copy.deepcopy(y);bad[0]['performance_bonus_proposal']=650000
    with patch(__name__+'.forms',return_value=(bad,s)):
      try:build();raise RuntimeError('FALSE_PASS inventedbonus')
      except AssertionError:pass
    bad=copy.deepcopy(s);bad[0]['action']='TWO_WAY'
    with patch(__name__+'.forms',return_value=(y,bad)):
      try:build();raise RuntimeError('FALSE_PASS veteranTW')
      except AssertionError:pass
    o=build()
    for f in [lambda z:z['hold_domain'].update(Young_generic_FA_safe_upper=0),lambda z:z['minimum_rule'].update(old_2m_replacement_reserve_is_Young_minimum_contract=True),lambda z:z['certification'].update(selected_Young_or_Satoransky_direction='Y_BIRD_8M'),lambda z:z['joined_policy_cost_inputs'][0]['stages'][-1].update(X_OTHER_actual=0)]:
      z=copy.deepcopy(o);f(z);assert validate(z)
    c,a,m=source_inputs();bad=copy.deepcopy(m);bad['conditional_rows'][0]['dated_states'][3]['apron_cost_known_upper_excluding_UFA_holds']-=100000
    with patch(__name__+'.source_inputs',return_value=(c,a,bad)):
      try:build();raise RuntimeError('FALSE_PASS upstreamcost')
      except AssertionError:pass
    original_component=component
    def altered_component(f,done):
      row=original_component(f,done)
      if done and f['id']=='Y_MINIMUM':row.update(normal_upper=2000000,apron_upper=2000000)
      return row
    with patch(__name__+'.component',side_effect=altered_component):
      try:build();raise RuntimeError('FALSE_PASS old2mreserve replacing minimum fullcash upper')
      except AssertionError:pass
    return 8
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();o=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(o),encoding='utf-8')
    if a.check:assert validate(load(OUT))==[] and text(MD)==markdown(o)
    print(json.dumps({'current':True,'cases':12,'actor_dates':36,'compact_policy_cells':192,'underlying_cost_checks':5940,'wholeFY22':False,'negative_controls':self_test()if a.self_test else None}))
