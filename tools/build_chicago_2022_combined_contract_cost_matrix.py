"""Unselected FY22 contract combinations: dated cost INPUTS, not whole cap clearance."""
import argparse, copy, hashlib, json
from pathlib import Path
from unittest.mock import patch
import fitz

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_combined_contract_cost_matrix.py'
OUT='research/CHICAGO_2022_COMBINED_CONTRACT_COST_MATRIX_2026_10_07.json'
MD=OUT[:-5]+'.md'
PINS={'research/CHICAGO_2022_23_APPROVED_CORE_CONTRACT_EXECUTION_2026_10_07.json': '2cc7aeaeaef530f1c3fac5846348792c3d516eb1479af1ce56617deb2e7cb2b5', 'research/CHICAGO_2022_ROOKIE_RFA_QO_FAMILY_2026_10_07.json': 'ceac38803f42eabff9032023a20ddbbcd1f739d4831a22fcba6e62fea096a14d', 'research/CARTER_2021_EXTENSION_CANDIDATE_FAMILY_2026_10_07.json': '070f1393070644540642284e9f1a6b49a2c6d1c1903fade2610d8570344d1f21', 'research/PROTAGONIST_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07.json': '84040384319b79d9bd2d87575d3f7061337c8978775278e1fa4dd8677e5b3228', 'research/LAVINE_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07.json': '2c7cf936b8387521e46f67cd245358bbd5c8191c99c466da9ae8b4b7c7d635d0', 'research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json': '7244beff7a120c5ca246a04e72b61586f3cfbe245487d5fc6479f5245fd78d9f', 'research/CHICAGO_2021_SIGNED_MINIMUM_YEAR2_NUMERIC_REFINEMENT_2026_10_07.json': '47ac976c5d20d6aa95a9d9cfad5e4430785a5975e4213557b57fe8b60d99e24f', 'simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE_INPUTS.json': '4b66d96a274fa4d31e41f6256192449e8b43a6dfc00e8f4e44f4cbd76e83bf78', 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json': '253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088', 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json': '9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce', 'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2', 'tools/build_2021_chicago_a_full_cost_family.py': 'de9a28dda0e26cf6fee95c889f910175355bc4b0ffb384f1b6662c8f08646574', 'tools/build_chicago_2022_23_approved_core_contract_execution.py': 'edfd73eab1d8617517447edd3093eb2647376e503263b5360890d87cfcc93c05', 'tools/build_chicago_2022_rookie_rfa_qo_family.py': '8ec5d15b04069d300f5b7bd5a70459f757c23a297ca966145045689d66a8cc2b', 'tools/build_carter_2021_extension_candidate_family.py': '3270d087a499240723ba0e8aba3a887aae4f144cc1b23da51121c658b75022f8', 'tools/build_protagonist_2022_contract_candidate_family.py': '82eacd9524a7eaacab960b022383025dafbc91229ac2c26c9e65b49a114a2a1e', 'tools/build_lavine_2022_contract_candidate_family.py': '24d963b1038eeb773d268710121e334b5aeb3c6d3b959ae582aa61ffac611dc9', 'tools/build_2021_approved_a_draft_signing_execution.py': '2e5c63ae32cc3897e1117c895687c047ed4fb1256e4addf888330697dc70c304'}
CORE='research/CHICAGO_2022_23_APPROVED_CORE_CONTRACT_EXECUTION_2026_10_07.json'
QO='research/CHICAGO_2022_ROOKIE_RFA_QO_FAMILY_2026_10_07.json'
C='research/CARTER_2021_EXTENSION_CANDIDATE_FAMILY_2026_10_07.json'
P='research/PROTAGONIST_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07.json'
L='research/LAVINE_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07.json'
LEG='research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json'
CBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
PAGES=[58,206,208,209,210,211,212,213,218,219,223,240,241,299,314,315,316,317,318,319,320,412,413]
EXPECTED_CORE=[('Markkanen',18360000),('Caruso',9030000),('LaMelo Ball',7775400),('Coby White',7413955),('Chris Duarte',4591680),('Green',1815687),('Joe Wieskamp',1563529),('Tony Bradley',2036328),('Stanley Johnson',2351532),('Denzel Valentine',2193930)]
C_SCHEDULES=[[14150000,13050000,11950000,10850000],[11320000,10440000,9560000,8680000],[16980000,15660000,14340000,13020000]]
P_SCHEDULES=[[18000000,19440000,20880000,22320000],[22000000,23760000,25520000,27280000],[30913750,33386850,35859950,38333050,40806150]]
CONSUMED_MEANING_PINS={'carter_terms': '65b8c11a1127bbd7cca69bf03df326d34ea92b7a5ea34e5dc55fc088ae70c8f3', 'carter_alternatives': '6948fd98ec2041d56ceae79c686697c69f42030c2bbb74f3596d1ad4f5bb4974', 'protagonist_terms': 'e4a194faac9aff3c1ce2e4587d09d98e0352e208787cdf11faf86a27160a0204', 'protagonist_alternatives': '5fa63d36c4f52fbaeabffe1e1fc1ad28ff902accbfb5ecdfbb00ccbb51ca0ee3', 'protagonist_policy': '10534bd8285c67c1b3638130118c3c4fd7007a319edca50b1dbbec42ba63ee15'}
APRON_SCREEN=156982000
LEGACY=20743601

def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def source_inputs():return {k:load(v) for k,v in [('core',CORE),('qo',QO),('carter',C),('protagonist',P),('lavine',L),('legacy',LEG)]}

def assert_sources(s):
    consumed={"carter_terms":s["carter"]["candidate_common_terms"],"carter_alternatives":s["carter"]["alternatives"],"protagonist_terms":s["protagonist"]["candidate_terms"],"protagonist_alternatives":s["protagonist"]["alternatives"],"protagonist_policy":s["protagonist"]["policy"]}
    for k,v in consumed.items():
        assert hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()==CONSUMED_MEANING_PINS[k],"Reviewed complete contract terms/timing/original-bonus conditions changed: "+k
    assert [(r['player'],r['2022_23_screen_upper_usd']) for r in s['core']['core_carry_rows']]==EXPECTED_CORE,'Core meaning changed'
    assert sum(v for _,v in EXPECTED_CORE)==57132041
    c=s['carter']['alternatives'];p=s['protagonist']['alternatives']
    assert [a['id'] for a in c]==['CX1','CX2','CX3','CX4'] and [a['id'] for a in p]==['E1','E2','E3','E4']
    assert [list(a['extension_regular_salary_schedule'].values()) for a in c[:3]]==C_SCHEDULES
    assert [a['salary_2022_onward'] for a in p[:3]]==P_SCHEDULES
    assert max(r['current_whole_dollar_component_screen_upper'] for r in s['protagonist']['original_rookie_current_family'])==4915859
    assert [a['mechanism'] for a in p]==['VII7b_ROOKIE_EXTENSION','VII6b1_DIRECT_FULL_BIRD_RFA_NEW_CONTRACT','VII6b1_DIRECT_FULL_BIRD_RFA_NEW_CONTRACT','ACCEPT_VALID_XI1c_ORDINARY_QO'],'Mechanism changed'
    assert all(a['author_selected']is False and a['actual_player_team_consent']is None for a in p)
    assert all(a['contract_agreed']is False for a in c)
    lt=s['lavine']['terms_candidate']
    assert lt['salary']==[37096500,40064220,43031940,45999660,48967380]
    assert lt['mechanism']=='NEW_DIRECT_FULL_BIRD_WITH_PRIOR_CHICAGO_NOT_EXTENSION_OR_SIGN_AND_TRADE'
    assert all(lt[k]==0 for k in ['signing_bonus','performance_bonus','physical_condition_academic_or_extra_promotion_bonus','loan_or_international_payment'])
    assert lt['trade_Exhibit4_rate_family']==['0','3/20'] and lt['actual_trade_Exhibit4_rate']is None
    assert s['lavine']['certification']['selected_contract']is None and s['lavine']['certification']['independent_review_completed']is True
    q=s['qo'];assert len(q['branch_rows'])==32
    assert q['policy']['protagonist_exact_pick']is None and q['policy']['Maximum_QO_selected']is False
    assert max(r['qo_charge_screen_upper_usd'] for r in q['branch_rows'] if r['player']=='Carter')==9279761
    assert hashlib.sha256(json.dumps(q['branch_rows'],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()=='c7232ba9b16fe8373e6876f052e73f1a361910191d36b9d094509a1903c2c13d','Reviewed QO component policy changed'
    assert len({(r['player'],r['pick'],r['starter']) for r in q['branch_rows']})==32
    assert sorted((r['pick'],r['starter']) for r in q['branch_rows'] if r['player']=='Protagonist')==[(n,b)for n in range(16,31)for b in [False,True]]
    assert s['legacy']['categories'][2]['legacy_total_upper']==LEGACY

def branches(s):
    cs=[{'id':a['id'],'policy':a['id'],'charge_upper':list(a['extension_regular_salary_schedule'].values())[0],'mechanism':'LIVE_2021_EXTENSION','live_July1':True,'starter':None}for a in s['carter']['alternatives'][:3]]
    ps=[{'id':a['id'],'policy':a['id'],'charge_upper':a['salary_2022_onward'][0],'mechanism':a['mechanism'],'live_July1':a['id']=='E1','pick':None,'starter':None}for a in s['protagonist']['alternatives'][:3]]
    for r in s['qo']['branch_rows']:
        a={'id':('CX4'if r['player']=='Carter'else'E4')+'_QO_'+str(r['pick'])+'_'+str(int(r['starter'])),'policy':'CX4'if r['player']=='Carter'else'E4','charge_upper':r['qo_charge_screen_upper_usd'],'mechanism':'ACCEPT_VALID_ORDINARY_QO','live_July1':False,'pick':r['pick'],'starter':r['starter'],'original_allowable_bonus_terms_retained':True}
        (cs if r['player']=='Carter'else ps).append(a)
    return cs,ps

def build():
    for p,h in PINS.items():assert sha(p)==h,'Unreviewed input '+p
    s=source_inputs();assert_sources(s);cs,ps=branches(s)
    assert len(cs)==5 and len(ps)==33
    base=57132041+LEGACY
    p_hold_upper=3*max(r['current_whole_dollar_component_screen_upper'] for r in s['protagonist']['original_rookie_current_family'])
    assert p_hold_upper==14747577
    rows=[]
    for c in cs:
      for p in ps:
        states=[]
        for i,(date,event) in enumerate([('2022-07-01','PRIOR_TERM_END_AND_NEW_CAPYEAR'),('2022-07-07','PROPOSE_LAVINE_BIRD'),('2022-07-07','PROPOSE_P_NEW_BIRD_OR_ACCEPT_QO'),('2022-07-07','PROPOSE_CARTER_QO_IF_CX4')]):
          plive=p['live_July1'] or i>=2;clive=c['live_July1'] or i>=3;llive=i>=1
          pn=p['charge_upper'] if plive else p_hold_upper;cn=c['charge_upper'] if clive else 20760081;ln=37096500 if llive else 37050000
          pa=p['charge_upper'] if plive else 7921302;ca=c['charge_upper'] if clive else c['charge_upper'];la=37096500 if llive else 0
          normal=base+pn+cn+ln+28861000+19000000
          apron=base+pa+ca+la
          signed=10+int(plive)+int(clive)+int(llive)
          states.append({'date':date,'within_date_order':i,'event':event,'signed_standard_contracts_in_named_family':signed,'normal_cost_known_upper_including_unrenounced_Young_Satoransky_holds':normal,'apron_cost_known_upper_excluding_UFA_holds':apron,'P_component':{'normal':pn,'apron':pa,'live':plive},'Carter_component':{'normal':cn,'apron':ca,'live':clive},'LaVine_component':{'normal':ln,'apron':la,'live':llive},'cap_counted_players_at_least':15,'incomplete_roster_charge':0,'incomplete_charge_zero_reason':'10 live core plus5 live/FA-counted identities, not merely signed count; VII4f','apron_sufficient_X_upper':APRON_SCREEN-apron,'X_actual':None,'whole_team_cost_PASS':False})
        after=states[-1];assert after['signed_standard_contracts_in_named_family']==13
        rows.append({'id':c['id']+'__'+p['id'],'Carter':c,'Protagonist':p,'LaVine':'UNSELECTED_REVIEWED_DIRECT_BIRD_5YEAR_FORM','dated_states':states,'remaining_STD_slots_if_all_three_implemented':2,'remaining_offseason_slots_if_no_TW':7,'ordinary_Bird_QO_extension_alone_triggers_hardcap':False,'whole_cost_or_author_selection':False})
    assert len(rows)==165 and len({r['id']for r in rows})==165
    policy=[]
    for cx in ['CX1','CX2','CX3','CX4']:
      for e in ['E1','E2','E3','E4']:
        rr=[r for r in rows if r['Carter']['policy']==cx and r['Protagonist']['policy']==e]
        upper=max(r['dated_states'][-1]['apron_cost_known_upper_excluding_UFA_holds']for r in rr)
        policy.append({'Carter':cx,'Protagonist':e,'branch_rows':len(rr),'known_apron_upper':upper,'all_screened_branch_sufficient_X_upper':APRON_SCREEN-upper,'numeric_upper_exceedance_is_legal_impossibility':False,'CX4_scope':'ORDINARY_QO_ACCEPTANCE_SUBFAMILY_ONLY'if cx=='CX4'else'EXISTING_EXTENSION_CANDIDATE'})
    assert hashlib.sha256(CBA.read_bytes()).hexdigest()==CBA_SHA
    with fitz.open(CBA)as d:
      pages=[{'PDF_1based':n,'text_LF_sha256':hashlib.sha256(d[n-1].get_text().replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()}for n in PAGES]
      assert 'twelve (12)' in d[211].get_text() and 'including Two-Way Players' in d[411].get_text()
    return {'id':'CHICAGO_2022_COMBINED_CONTRACT_COST_MATRIX_2026_10_07','status':'INDEPENDENTLY_REVIEWED_DATED_CATEGORY_MAP_UNSELECTED_CONTRACT_INPUTS','source_main_snapshot':'ae8cc87d1f35e86c6c52a68dfa5766422bb137a3','source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8 BOMstrip CRLF/CR toLF; rawCBA bytes separate','CBA':{'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(CBA),'raw_sha256':CBA_SHA,'direct_text_pages':pages},'source_scope':'Reuses independently reviewed public contract/category witnesses. No new primary retrieval or independent re-audit of their entire ancestors claimed.',
      'approved_direction':['Markkanen M1 four-year Chicago retention','Caruso/growth-core A route'],'candidate_inputs':['CX1/CX2/CX3 extension or CX4 RFA','E1/E2/E3 or E4 ordinaryQO','LaVine directBird existing5year schedule'],'core10':s['core']['core_carry_rows'],'legacy_carry':{'annual_stretch_upper':16371000,'camp_fullcash_reserved':4372601,'sum_upper':LEGACY,'scope':'Preserved public-category family with positive ordinary term endpoints; no new resolution/settlement/waiver event chosen. Prior valid annual stretch bounded; not proof of all private future absence. If a named preserved liability or new event is identified, this bound reopens.','actual_paid_or_absence_certified':False},
      'five_expired_prior_inputs':['LaVine','Protagonist','Wendell Carter Jr.','Thaddeus Young','Tomas Satoransky'],'six_category_map':[{'id':'CURRENT_AND_PROPOSED','covered':'10 reviewed carry plus all165 combinations of3 consensual contract forms','remaining':'Young/Satoransky new salary+all performance; any new contract/assignment cost X. They are unrenounced UFA before new proposal, not livecontract0.'},{'id':'LEGACY_DEAD_AND_CAMP','covered':'20,743,601 public priorcategory outer reservation','remaining':'New selected waiver/settlement/resolution would be named cost input; no invented future event.'},{'id':'FA_QO_FRN_FLOORS','covered':'5 expired names; valid liveextension suppresses FA, ordinaryQO outstanding before acceptance and replaces hold when accepted; Young28,861,000/Sato19,000,000 normal hold safeupper, apron isolatedhold0','remaining':'Dotson/Cook TWexpiry-tenure/ordinaryQO/FRN/young-FAfloor and cost need dated named model; not automatic zero.'},{'id':'DRAFT_AND_TENDERS','covered':'Unsignedfirst normal120%scale; ordinaryunsignedfirsthold excludedapron, RequiredFirstTender includedapron; roster contract only when signed','remaining':'2022 actualworking draftcontrol/rookie signatures and Simonovic new2022–23 X5/X6/tender window; no automaticallysignedSTD16.'},{'id':'ROSTER_AND_INCOMPLETE','covered':'Named5 live-orFA count makes incomplete0 in this unrenounced family;13signed after3forms,2STD spaces; offseason<=20 includingTW','remaining':'Final2STD and0..2TW contracts; Young+Sato use both STDspaces, any rookies require distinct replacement/change.'},{'id':'ANNUAL_EXCEPTIONS','covered':'2021hardcapexpiresJun30;2022 NTMLE10,490,000/TMLE6,479,000/room5,401,000 named annual public amounts; unused excludedapron','remaining':'Generic incorporation/renunciation/valid usage with datedsalary history must be modeled; annualNTMLE/BAE/S&T newtrigger and newroster salaries cannot be presumed zero.'}],
      'matrix':policy,'conditional_rows':rows,'coverage':{'policy_cells':16,'numeric_branches':165,'dated_states_per_branch':4,'dated_cost_rows':660,'named_signed_after_forms':13,'whole_FY22_cost_certified':False},
      'CX4_other_market_boundary':{'ordinaryQO_is_entire_CX4':False,'direct_Chicago_fullBird_baseline25pct_salary_plus_new_unlikely_budget_upper':30913750,'bound_condition':'Plain no-newbonus FullBird lawful candidate under baseline25%maximum; if added incentives, eligibility higher-max/otherterms change the domain, reopen. No exactterm/amount selected; not a validated newcontract form here.','supplemental_after_signing_X_upper_by_P_policy':{e:APRON_SCREEN-base-37096500-30913750-max(r['Protagonist']['charge_upper']for r in rows if r['Protagonist']['policy']==e)for e in ['E1','E2','E3','E4']},'offer_sheet_SandT_or_franchise_move':'Consequential unselected path; named counterparty/terms needed if selected, not private receipts.'},
      'sequence_and_rules':{'candidate_extensions':'2021Oct15 forms, only if that CX/E1 candidate is chosen; never retroactively assumed from2022continuation','QO_issue':'2022Jun29 conditionalNBASeasonended/validopenwindow, acceptanceJuly7 unwithdrawn; no MaximumQO/FRN selected','new_Bird_forms':'July7 noonET afterNBAJuly6moratorium andCBA12:01Birdwindow; within-day ordering fictionalproposal','no_backdating':True,'generic_FA_cost':'Hold OR live salary; never both. RFA outstandingQO/FRN apron vs normalcapFAhold differ. New applicablefloor may require component max, not everycashpayment prorating.','whole_normal_cap_room_PASS':False,'no2021_hardcap_carry':True,'2022_hardcap_actual':None,'apron_screen':APRON_SCREEN,'apron_screen_not_official_rounding_certificate':True,'apron_exceedance':'Negative X allowance is failure of this conservative sufficient screen, not an illegal ordinaryBird contract or lowerbound impossibility. Without a newtrigger this screen is optional budget comparison.'},
      'minimum_numeric_scope':{'used_core_screen':57132041,'condition':'Signing2021Year2 statutoryminimum amount<=priorceil+10 screens; exactrounding remains unverified','independently_reviewed_floorceil_sensitivity_only':{'core_upper_if_floorceil_condition_admitted':57131991,'all_X_allowances_increase_by':50},'refinement_condition_selected':False},
      'next_finite_execution':['Consequential CX/P/LaVine comparisons are ready but unselected; continue routine finalroster proposals while awaiting chosen path.','Specify Young/Satoransky retain-or-expire costs and competition with2022rookies for2STDslots.','Join2022draft+tenders, Dotson/CookTWexpiry and Simonovic nextwindow; carry their namedcost and actualpostsignroster.','Select lawful annualexception usage/renunciation family if needed, then solve X perdatedstate; no automaticR0 or privateabsence gate.'],
      'certification':{'independent_review_completed':True,'actual_contract_or_cents_certified':False,'actual_player_team_consent':None,'selected_Carter_or_Protagonist_or_LaVine_contract':None,'new_author_lock':False,'whole_macro3_complete':False,'whole_FY22_roster_cost_or_results':False,'central_or_REGISTER_promotion':False,'manuscript_written':0}}

def validate(o):
    try:assert o==build(),'Source/meaning/current output differs';return []
    except (AssertionError,KeyError,OSError,ValueError)as e:return[str(e)]

def markdown(o):
    lines=['# Chicago FY22: 기존 계약 선택지의 명단·비용 결합','',o['status'],'','M1·Caruso/A 방향은 승인 상태를 유지한다. Carter·주인공·LaVine 계약의 실제 선택·합의는 미정이다. 기존 10명 이월 $57,132,041와 공개 이전 범주 예약 $20,743,601을 모든 조합에 보존했다.','', '## 16 정책 조합 / 165 수치 분기 / 660 날짜별 비용 입력','', '|Carter|주인공|분기|알려진 apron 상단|추가 X 충분상한|','|---|---|---:|---:|---:|']
    for r in o['matrix']:lines.append(f"|{r['Carter']}|{r['Protagonist']}|{r['branch_rows']}|{r['known_apron_upper']:,}|{r['all_screened_branch_sufficient_X_upper']:,}|")
    lines+=['','CX4 열은 **유효한 보통 QO 수락 하위가족**이다. CX4 전체 RFA 시장을 닫았다는 뜻이 아니다. Chicago 새 Bird의 기본25% 한도 후보는 별도 상단 $30,913,750로 감도를 연결했으며, 정확 계약 형식·금액/외부 offer sheet·S&T·이적을 채택하지 않았다. E4는 원 지명16–30 × starter 여부30분기를 모두 보존한다. QO 상단을 실제 계약급여로 확정하지 않는다.','', '## 날짜·명단·hold','', '7월1일 원기간 종료/연장기간 시작 → 7월7일 LaVine 새 Bird → 주인공 새 Bird 또는 QO → CX4 Carter QO를 가상 합의 순서로 검산했다. 2021 연장 경로는 해당 기존 후보를 선택할 때만 살아 있다. 같은 날짜의 순서는 작업용 후보이며 실제 접수시각이 아니다. 유효 QO는 시즌 종료 조건 아래6월29일 발행/7월7일 미철회 수락을 전제로 한다.','새 세 계약을 구현하면 STD13명으로 2칸이 남는다. Young·Satoransky를 모두 재계약하면 두 칸을 사용하고, 2022 신인 추가는 별도 교체/명단 경로가 필요하다. 5 FA/live identities도 VII4(f) cap 산입 인원에 포함되므로 incomplete-roster 비용0은 단순 signed10명 계산이 아니다. TW는 offseason20에도 포함한다.','Young $28,861,000·Satoransky $19,000,000은 미renounce 일반 cap hold 상단이다. 이 UFA hold 자체는 apron에서 제외하지만 새 계약·과거 부채·young-FA floor를 지우지 않는다. P/C의 normal FAhold와 apron outstandingQO를 분리하고 새 계약 이후에는 hold와 salary를 중복 가산하지 않는다.','', '## 전체 여섯 범주와 실제 남은 입력','']
    for x in o['six_category_map']:lines += [f"- **{x['id']}**: {x['covered']}. 남음: {x['remaining']}"]
    lines+=['','X는 위 미구현 이름·범주의 추가 apron 비용이며 실제 값은 null이다. $156,982,000은 기존 보수적 apron screen이다. 2021 NTMLE hardcap이2022로 이월하지 않는다. 새 NTMLE/BAE/S&T 사건을 선택하지 않았으므로 음수 여유는 conservative 충분조건 실패이지 Bird 계약의 법적 불가능 판정이 아니다. 일반 cap 여유 역시 위 partial 비교로 인증하지 않는다.','최소계약은2021서명 Year2의 기존 ceil+10 조건을 유지한다. 별도 검문된 floor/ceil 조건을 적용할 경우 이월 상단50달러 감소·모든 X 여유50달러 증가지만 법정 반올림/조건 선택을 확정하지 않는다.','공개 이전 범주20,743,601은 positive ordinary기간 끝점+valid stretch16,371,000+campfullcash4,372,601의 보존가족이다. 새 미보고 미래 합의를 무한 추가하거나 실제 사적 지급 부재를 인증하지 않는다. 식별된 보존 의무나 새 사건이 생기면 해당 이름과 비용을 재개방한다.','', '[2017 CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) VII4(d)–(g),6(b)/(m),IX1,XI1/4,XXIX1–3 원쪽을 직접 대조했다. [NBA2022 cap/calendar](https://pr.nba.com/nba-salary-cap-2022-23-season/) 및 각 검문된 입력의 source/raw 연결을 재사용한다. 새 원문 회수나 원 조상 전체 독립검문을 수행했다고 계수하지 않는다.','', '|번호|묶음|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23 거래·계약|16조합 날짜별 후보 검산; 선택·전체비용 남음|','|4|장기 커리어|후속 시즌 입력 대기|','|5|결말·전체 구조|전체 기능표 미완료|','|6|집필규격·Context Pack|현행 누적 등록기 참조·Pack0|','|7|통합·독립·작가 승인|최종CLOSED|','','미완료 큰 묶음5 / v0.30 PARTIAL / 설계·원고CLOSED / 원고0.','']
    return '\n'.join(lines)

def self_test():
    s=source_inputs();bad=copy.deepcopy(s);bad['protagonist']['alternatives'][1]['mechanism']='SIGN_AND_TRADE'
    with patch(__name__+'.source_inputs',return_value=bad):
      try:build();raise RuntimeError('FALSE_PASS mechanism')
      except AssertionError:pass
    bad=copy.deepcopy(s);bad['core']['core_carry_rows'][0]['2022_23_screen_upper_usd']+=1;bad['core']['core_carry_rows'][1]['2022_23_screen_upper_usd']-=1
    with patch(__name__+'.source_inputs',return_value=bad):
      try:build();raise RuntimeError('FALSE_PASS same total')
      except AssertionError:pass
    bad=copy.deepcopy(s);bad['qo']['branch_rows'][2]['qo_charge_screen_upper_usd']+=1
    with patch(__name__+'.source_inputs',return_value=bad):
      try:build();raise RuntimeError('FALSE_PASS QO component')
      except AssertionError:pass
    bad=copy.deepcopy(s);bad['lavine']['terms_candidate']['performance_bonus']=100000
    with patch(__name__+'.source_inputs',return_value=bad):
      try:build();raise RuntimeError('FALSE_PASS LaVine additional bonus')
      except AssertionError:pass
    for actor,key,field in [("carter","candidate_common_terms","new_signing_performance_promotional_loan_or_buyout_additions"),("protagonist","candidate_terms","unlikely_performance_bonus")]:
      bad=copy.deepcopy(s)
      if actor=="carter":bad[actor][key][field]=100000
      else:bad[actor][key]["E1_E2_E3"][field]=100000
      with patch(__name__+".source_inputs",return_value=bad):
        try:build();raise RuntimeError("FALSE_PASS consumed bonus "+actor)
        except AssertionError:pass
    a=build()
    for edit in [lambda b:b['certification'].update(selected_Carter_or_Protagonist_or_LaVine_contract='E2'),lambda b:b['sequence_and_rules'].update(no2021_hardcap_carry=False),lambda b:b['conditional_rows'][0]['dated_states'][-1].update(X_actual=0),lambda b:b['CX4_other_market_boundary'].update(ordinaryQO_is_entire_CX4=True)]:
      b=copy.deepcopy(a);edit(b);assert validate(b),'FALSE_PASS output'
    return 10

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');args=ap.parse_args();o=build()
    if args.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(o),encoding='utf-8')
    if args.check:assert validate(load(OUT))==[] and text(MD)==markdown(o)
    print(json.dumps({'current':True,'policy_cells':16,'numeric_branches':165,'dated_rows':660,'whole_FY22_PASS':False,'negative_controls':self_test() if args.self_test else None}))
