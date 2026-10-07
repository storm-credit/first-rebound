"""Source-supported Sep4 candidate joint transition; not a whole Brooklyn prior ledger."""
import argparse, copy, hashlib, itertools, json
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import fitz
import build_detroit_2021_initial_residual_cost_family as initial
import build_detroit_2021_opening_named_operating_family as operating
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_detroit_brooklyn_2021_jordan_joint_trade_family.py'
OUT='research/DETROIT_BROOKLYN_2021_JORDAN_JOINT_TRADE_FAMILY_2026_10_07.json'
MD=OUT[:-5]+'.md'
BASELINE='a05bd9d4ba36c4b078765135568e1fec2a8d439f'
CACHE=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-det-bkn-20261007')
BYLAWS=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-2019-bylaws.pdf')
BYLAWS_SHA='6accb3d9633e15e8559d13228c27ae7b3b0b81eac0894050b06256eea6da3464'
def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def fraction(x):return str(Fraction(x))
def policy():
 return {'selected':False,'date_hypothesis':'2021-09-04','branch':'B_NO_LYLES_CONDITIONAL',
 'minimum_first_year_full_cash_upper':2650000,'new_minimum_performance_or_signing_bonus':0,
 'original_performance_template_is_published_named_family_not_private_zero':True,
 'applicable_original_trade_bonus_fully_waived_by_player_and_assignor_candidate':True,
 'trade_bonus_waiver_extension_renegotiation_not_before':'2022-03-04_OR_LATER_OTHERWISE_ELIGIBLE',
 'original_protected_base_not_reduced':True,'Jordan_current_full_salary_even_after_candidate_waiver':9881598,
 'cash_q_positive_at_most_reported_approximation':5780000,'cash_paid_and_received_not_netted':True,
 'candidate_prior_BKN_paid_and_DET_received_cash_each_at_most':5000,
 'new_hardcap_trigger':False,'no_new_S_and_T_contract_in_this_event':True,
 'four_named_second_claims_preserve_existing_conditions':True,
 'actual_preexisting_BKN_budget_known':False,'other_BKN_cost_components_unchanged_under_local_transition':True,
 'new_unused_BKN_TPE_if_any_valid_written_renunciation_before_normal_budget_comparison':True,
 'normal_budget_comparison_is_instant_before_any_new_TPE_incorporation':False,
 'new_author_lock':False,'actual_acceptance':None}
FIXED_POLICY=copy.deepcopy(policy())
RIGHTS=[{'id':'BKN2022_2R','year':2022,'round':2,'origins':['BKN'],'selector':'OWN'},
 {'id':'MEM_WAS2024_BETTER_2R','year':2024,'round':2,'origins':['MEM','WAS'],'selector':'MORE_FAVORABLE'},
 {'id':'GSW_WAS2025_BETTER_2R','year':2025,'round':2,'origins':['GSW','WAS'],'selector':'MORE_FAVORABLE'},
 {'id':'BKN2027_2R','year':2027,'round':2,'origins':['BKN'],'selector':'OWN'}]
FIXED_RIGHTS=copy.deepcopy(RIGHTS)
def rights():return copy.deepcopy(RIGHTS)
def sources():
 assert all(sha(p)==h for p,h in PINS.items()),'Reviewed repository source changed'
 saved=load(initial.OUT)
 assert saved==initial.build(),'Initial public X carrier differs from full source reconstruction'
 assert saved['certification']['independent_review_completed']is True
 assert saved['initial_X']['public_named_family_upper']==5361732
 assert saved['base_ledger']['sum']==100052228
 assert 'James Wiseman AUTHOR_APPROVED / LOCKED' in text('simulation/2020_DRAFT_TOP4_SEQUENTIAL_BOARD.md')
 assert 'Golden State 2순위' in text('simulation/2020_DRAFT_TOP4_SEQUENTIAL_BOARD.md')
 observations=[]
 for r in OBSERVATIONS:
  b=Path(r['cache_path']).read_bytes();assert hashlib.sha256(b).hexdigest()==r['capture_sha256'],'Observation capture changed'
  o=json.loads(b);observations.append({**r,**o})
 s={o['id']:o for o in observations}
 assert s['NETS_SEP4']['terms']=={'second_years':[2022,2024,2025,2027],'via2024':'WAS','via2025':'GSW'}
 assert s['NETS_AUG6']['terms']=={'year2024':['MEM','WAS'],'year2025':['GSW','WAS'],'selector':'MORE_FAVORABLE'}
 assert s['PISTONS_SEP29']['terms']=={'2022':['BKN'],'2024':['MEM','WAS'],'2025':['GSW','WAS'],'2027':['BKN'],'selector':'MORE_FAVORABLE'}
 assert s['CAP2021']['cap']==112414000 and s['CAP2021']['tax']==136606000 and s['CAP2017']['cap']==99093000
 raw=[]
 for r in RAW:
  assert hashlib.sha256(Path(r['cache_path']).read_bytes()).hexdigest()==r['raw_sha256'],'Raw changed: '+r['id']
  raw.append({**r,'adopted_for_current_salary':r['id']in['Jordan','Sekou'],
    'not_adopted_reason':'TEAM_PAGE_CURRENT_2026_27_NOT_2021' if r['id']=='BKN_Salary' else 'HTTP403_NO_BODY' if r['status']==403 else None})
 # Parse real contract rows: do not replace protected original money with later buyout.
 def row(rid,amount):
  r=next(r for r in RAW if r['id']==rid)
  ts=initial.tables(Path(r['cache_path']).read_bytes())
  rr=[r for t in ts for r in t if r and r[0].startswith('2021-22') and '$'+format(amount,',') in r[1:6]]
  assert rr,'Source contract row missing '+rid
  r=rr[0];assert r[-2:]==['$0','$0'],'Public performance template changed '+rid
  return r
 contract={'Jordan':row('Jordan',9881598),'Sekou':row('Sekou',3613680)}
 v=initial.source_view();contract['Okafor']=initial.find_row(v,'jahlil-okafor','2021-22',2130023)
 assert contract['Okafor'][-2:]==['$0','$0']
 assert 'Yes (Dec 21, 2020)'in contract['Sekou'],'Year3 option source changed'
 assert hashlib.sha256(operating.CBA.read_bytes()).hexdigest()==operating.CBA_SHA
 assert hashlib.sha256(BYLAWS.read_bytes()).hexdigest()==BYLAWS_SHA
 with fitz.open(operating.CBA)as d:
  pp=[54,55,233,240,241,248,249,251,252,398,561]
  page={str(i):hashlib.sha256(d[i-1].get_text().replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()for i in pp}
  assert '2,328,652' in d[560].get_text() # Exhibit C, not vendor scale
  assert 'one hundred seventy-five percent (175%)'in ' '.join(d[232].get_text().split())
  assert 'shall not be' in d[250].get_text() and 'netted against each other'in d[250].get_text()
  assert 'six (6) months'in d[247].get_text()
  assert 'any time renounce' in ' '.join(d[239].get_text().split())
  assert 'exclude the amount of any Salary' in ' '.join(d[240].get_text().split())
 with fitz.open(BYLAWS)as d:
  bp={str(i):hashlib.sha256(d[i-1].get_text().replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()for i in [72,73,87]}
 assert load(operating.AR)==operating.load(operating.AR),'Source player matching inputs changed'
 return saved,observations,raw,contract,page,bp

def make_trace(x,q,p):
 old=operating.trace(x,q,load(operating.AL),load(operating.AQ),load(operating.AR),operating.policy())
 # Refine only the five pretrade Year1 minimum/tender upper functions.
 refined=[];reduction=0
 for i,r in enumerate(old):
  n=copy.deepcopy(r)
  if i in [2,3,4,7,9]:reduction+=3000000-p['minimum_first_year_full_cash_upper']
  n['team_salary_upper']=r['team_salary_upper']-reduction
  if i in [2,3,4,7,9]:n['delta_upper']=r['delta_upper']-(3000000-p['minimum_first_year_full_cash_upper'])
  n['legacy_3m_screen_upper']=r['team_salary_upper'];refined.append(n)
 assert refined[10]['team_salary_upper']==old[10]['team_salary_upper']-1750000
 return refined

def allocations(rr):
 """Claim assignment does not replace original future ranks or unrelated residual-right holders."""
 result=[]
 for r in rr:
  if len(r['origins'])==1:
   result.append({**r,'prior_claim_holder':'BKN','candidate_claim_holder':'DET','future_pick_number':None,'selector_cases':[{'selected_origin':r['origins'][0]}]})
  else:
   cases=[]
   for a,b in itertools.permutations(range(31,61),2):
    origin=r['origins'][0]if a<b else r['origins'][1]
    cases.append({'ranks':[a,b],'selected_origin':origin,'holder':'DET','year':r['year'],'round':2})
   result.append({**r,'prior_claim_holder':'BKN','candidate_claim_holder':'DET','future_pick_number':None,'selector_cases':cases,'other_residual_claim_objects_preserved_not_reassigned':True})
 return result

def assert_allocations(rows,rr):
 assert rr==FIXED_RIGHTS,'Public named right family changed'
 assert len(rows)==4
 for got,source in zip(rows,FIXED_RIGHTS):
  assert all(got[k]==source[k]for k in ['id','year','round','origins','selector']),'Claim source identity changed'
  assert got['prior_claim_holder']=='BKN'and got['candidate_claim_holder']=='DET'
  assert got['future_pick_number']is None
  cs=got['selector_cases']
  if len(source['origins'])==1:assert cs==[{'selected_origin':source['origins'][0]}]
  else:
   assert len(cs)==870 and len({tuple(c['ranks'])for c in cs})==870
   for c in cs:
    a,b=c['ranks'];assert 31<=a<=60 and 31<=b<=60 and a!=b
    assert c['selected_origin']==source['origins'][0 if a<b else 1]and c['holder']=='DET'and c['year']==source['year']and c['round']==2,'Published selector result changed'

def build():
 p=policy();assert p==FIXED_POLICY,'Candidate policy changed'
 src,obs,raw,contracts,cbpages,bpages=sources()
 minexact=Fraction(2328652*112414000,99093000)
 assert minexact<2650000 and p['minimum_first_year_full_cash_upper']==2650000
 x=src['initial_X']['public_named_family_upper'];q=src['initial_X']['legal_q_family'][1]
 t=make_trace(x,q,p)
 rawtrace=operating.trace(x,q,load(operating.AL),load(operating.AQ),load(operating.AR),operating.policy())
 assert len(t)==len(rawtrace)==12,'Dated event count changed'
 reductions={2:350000,3:350000,4:350000,7:350000,9:350000}
 accumulated=0
 for i,(returned,source)in enumerate(zip(t,rawtrace)):
  accumulated+=reductions.get(i,0)
  expected=copy.deepcopy(source)
  expected['legacy_3m_screen_upper']=source['team_salary_upper']
  expected['team_salary_upper']=source['team_salary_upper']-accumulated
  if i in reductions:expected['delta_upper']=source['delta_upper']-reductions[i]
  assert returned==expected,'Returned dated refinement differs from source event/delta chain'
 # Maximise X+q over the entire admitted initial domain: saturation <=cap.
 assert src['base_ledger']['sum']+x+q==112414000
 before=t[9]['team_salary_upper'];after=t[10]['team_salary_upper']
 assert (before,after)==(130829566,134967461)
 assert after<136606000
 out=3613680+2130023;incoming=9881598
 taxlimit=Fraction(out*5,4)+100000
 nontaxlimit=max(min(Fraction(out*7,4)+100000,out+5000000),taxlimit)
 assert nontaxlimit>=incoming and taxlimit<incoming
 bknlimit=Fraction(incoming*5,4)+100000
 assert bknlimit>=out
 rr=rights();aa=allocations(rr);assert_allocations(aa,rr)
 assert all(r['round']==2 and 2022<=r['year']<=2027 for r in rr)
 cash_exact=Fraction(5100000*112414000,99093000)
 cash_safe=5785000
 assert cash_exact>=cash_safe and p['cash_q_positive_at_most_reported_approximation']+p['candidate_prior_BKN_paid_and_DET_received_cash_each_at_most']<=cash_safe
 return {'id':'DETROIT_BROOKLYN_2021_JORDAN_JOINT_TRADE_FAMILY_2026_10_07','status':'INDEPENDENTLY_REVIEWED_SOURCE_BOUND_JOINT_TRANSITION_CANDIDATE','baseline_main':BASELINE,
 'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'Repo BOM stripped LF; external raw bytes and attributed web-observation captures separately typed',
 'policy':p,'source_observations':obs,'external_raw':raw,'original_contract_reported_rows':contracts,
 'CBA':{'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','raw_sha256':operating.CBA_SHA,'cache_path':str(operating.CBA),'PDF1based_text_LF_sha256':cbpages},
 'Bylaws':{'raw_sha256':BYLAWS_SHA,'cache_path':str(BYLAWS),'PDF1based_text_LF_sha256':bpages},
 'minimum_refinement':{'five_pretrade_Year1_functions':['Saben Lee','Frank Jackson','Isaiah Livers','Rodney McGruder','Aldama outstanding RequiredTender'],
 'ExhibitC2017_10plus_Year1':2328652,'CBA_scaled_exact_fraction':str(minexact),'legal_minimum_function_upper':2650000,'five_upper_reduction':1750000,'agreed_minimum_salary_is2650000':False,'official_exact_rounding_certified':False,'old_3m_ancestor_artifacts_changed':False},
 'DET':{'public_initial_X_interval':[0,x],'Olynyk_q_domain':'[3000000,min(12195122,12361772-X)]','exact_q_selected':None,'saturation_endpoint_q':q,
 'whole_domain_normal_salary_pretrade_upper':before,'whole_domain_normal_salary_posttrade_upper':after,'tax':136606000,'tax_margin':136606000-after,'nontax_matching_limit_exact':str(nontaxlimit),'nontax_incoming_margin_exact':str(nontaxlimit-incoming),
 'outgoing_salary':out,'incoming_salary':incoming,'dated_refined_trace':t,'legacy_3m_posttrade_broad_bound_tax_margin':136606000-(after+1750000),'broad_failed_tax_bound_is_actual_illegality':False,
 'matching_uses_normal_TeamSalary_not_apron':True,'ordinary_new_trade_hardcap':False,'Jordan_postwaiver_current_year_full_charge':9881598,'original_buyout_reduction_copied':False,
 'conditional_opening_roster_source':operating.OUT,'whole_actual_registration_certified':False},
 'BKN':{'outgoing_salary':incoming,'incoming_salary':out,'minimum_matching_limit_any_taxclass_exact':str(bknlimit),'incoming_margin_exact':str(bknlimit-out),'normal_and_adjusted_apron_delta':out-incoming,
 'other_costs_symbol':'B_preserved_other_components_after_TPE_cleanup','normal_relation_after_valid_renunciation_of_new_unused_TPE':['B+9881598','B+5743703'],
 'new_unused_TPE_if_any':'incorporation and valid VII6m2 written renunciation are candidate acts; not original absence',
 'normal_comparison_timestamp':'after valid renunciation, not raw immediate posttrade ledger',
 'apron_new_deemed_exception_component_excluded_under_VII6m3F':True,'apron_relation':'same preserved other components; new deemed exception excluded under VII6m3F; no new bonus; old applicable kicker consensually waived, incoming public performance template preserved',
 'valid_prior_budget_transition_preserves_headroom_after_candidate_TPE_renunciation':True,'new_hardcap_trigger':False,'negative_apron_without_hardcap_is_illegal':False,'whole_prior_budget_inventory_constructed':False,
 'pretrade_offseason_total_STD_TW_at_most_19_required':True,'posttrade_count_delta':1,'exact_prior_roster_selected':False},
 'joint_manifest':{'date_candidate':'2021-09-04','DET_to_BKN':['Sekou Doumbouya','Jahlil Okafor'],'BKN_to_DET':['DeAndre Jordan'] ,'claim_count':4,'claims':aa,'future_actual_ranks_or_recipients_certified':False,'first_round_right_objects_changed':0,'Stepien_first_coverage_changed':False,'latest_second_year':2027,'sevenyear_window_respected':True},
 'cash':{'historical_official_cash_exists':True,'historical_reporter_approx_usd':5780000,'candidate_q_domain':[1,5780000],'candidate_q_selected':None,
 'CBA_formula_annual_limit_exact_fraction':str(cash_exact),'safe_integer_screen_bound':cash_safe,'actual_league_rounded_limit_certified':False,
 'admitted_prior_BKN_paid_and_DET_received_each_interval':[0,5000],'BKN_paid_post_max':5785000,'DET_received_post_max':5785000,'other_direction_budget_separate':True,'netting_allowed':False,'actual_prior_cash_usage_certified':False,'cash_reduces_player_TeamSalary':False},
 'rights_provenance_and_boundaries':{'current_2025_existing_GSW_claim_positive_anchor':'NETS_AUG6','2019_exact_top20_conversion_clause_certified':False,'2019_full_conditions':None,
 'GSW2020pick2_preserved_canon':True,'2024_2025_onward_selector_positive_anchor':'PISTONS_SEP29','underlying_future_pick_owner_unconditional_certified':False,
 'original_completed_trade_is_positive_named_family_anchor_not_changed_world_acceptance':True,'all_original_private_terms_absent_or_identical_certified':False,
 'fiveway_original_Hutchison_WAS_to_SAS_automatically_copied':False},
 'remaining_named_scope':['A/B and reduced Olynyk/minimum offers remain unselected consequential directions.',
 'BKN prior selected complete roster/cost carrier is not reconstructed here; prove its valid public family and <=19 offseason count before whole-event adoption.',
 'Carry August6 named consideration through a reviewed changed-world Dinwiddie/WAS fiveway or equivalent source-supported prior-right assignment; original Hutchison WAS-to-SAS cannot be copied.',
 'Cash previous-use intervals are explicit candidate sufficient conditions, not a complete actual cash ledger.',
 'Any retained named performance component outside the published template reopens its own salary allocation; no arbitrary private absence gate.',
 '2019 exact conversion text remains a historical source limitation; current named2025 positive object is supported without choosing its unpublished upstream clause.'],
 'independent_review_basis':{'peer':'chi_salary_domain','source_read':'raw6+attributedcapture6/NBA3indexedbody/ABCreport/CBA11+Bylaws3','concrete_repair':'returned intermediate state3 minus1m with unchanged pre/post rejected by independent caller source-chain guard','same_TPE_cleanup_deletion_rejected':True,'writer_controls_counted_as_independent':0},
 'certification':{'independent_review_completed':True,'conditional_DET_nontax_matching_supported':True,'BKN_any_taxclass_matching_and_nonincreasing_budget_transition_supported':True,'four_published_conditional_rights_assignment_family_supported':True,'whole_joint_execution_PASS':False,'whole_BKN_cost_PASS':False,'actual_acceptance_or_private_notices':None,'author_selected_A_B_or_new_prior_trade':False,'whole_macro3':False,'REGISTER_changed':False,'manuscript_count':0},'progress':src['progress']}

def validate(o):
 try:assert o==build(),'Saved joint carrier differs from source reconstruction';return []
 except(AssertionError,KeyError,OSError,ValueError)as e:return[str(e)]
def markdown(o):
 d=o['DET'];b=o['BKN'];c=o['cash']
 lines=['# Detroit–Brooklyn 2021년 9월 4일 공동거래 후보','',o['status'],'','## 실제 새 근거와 권리','',
 '[Nets 9/4 공식 발표](https://www.nba.com/nets/news/2021/09/04/brooklyn-nets-complete-trade-detroit-pistons): Jordan·네 2R·현금은 Detroit로, Sekou·Okafor는 Brooklyn으로 간 원역사 완료 사건이다.',
 '[Nets 8/6 공식 발표](https://www.nba.com/nets/news/2021/08/06/brooklyn-nets-acquire-future-draft-considerations-five-team-trade)는 2024 MEM/WAS 비교권, 기존 GSW2025와 WAS2025 교환권을 명명한다.',
 '[Pistons 9/29 공식 설명](https://www.nba.com/pistons/chatmailbox/pistons-mailbag-september-29-2021)은 Detroit가 BKN2022/2027, MEM/WAS2024 및 GSW/WAS2025의 더 유리한 2R를 받는다고 확인한다.',
 '2024를 무조건 WAS 픽으로, 2025를 무조건 GSW 픽으로 바꾸지 않았다. 두 비교쌍의 각870 순서 입력에서 낮은 순번의 원 권리가 DET에 귀속되는지 원천 정책과 별도로 대조했다. 남은 반대편 권리객체는 기존 관계를 보존하고 수령자를 발명하지 않는다. 미래 실제 순번·선수·전달 결과를 복사하지 않는다.',
 '2019 정확 top20→2025 전환 문구는 미회수다. 지금의 근거는 2021년8/6 구단이 실제 기존 GSW2025 권리를 명명했다는 양성 사건과 동결 GSW2020 #2의 보존이다. 미회수 보호 숫자를 사실로 채우거나 모든 비공개 조항 부재를 새 종료조건으로 요구하지 않는다. 현재 후보는 이 명명 객체의 조건을 보존하는 양도이다.','',
 '## 양 팀 비용과 실제 구성한 충분조건','',
 f"기존 독립수용 초기 X∈[0,5,361,732] 및 q∈[3,000,000,min(12,195,122,12,361,772−X)]를 그대로 소비했다. CBA Exhibit C의 10+ Year1 최대2,328,652를 공식 cap 비율로 조정하면 {o['minimum_refinement']['CBA_scaled_exact_fraction']}다. 새 법정 최소/RequiredTender 다섯 함수에 **2,650,000** 상단을 적용했으며 이것은 합의된 급여가 아니다. 원3m 산출물은 변경하지 않았다.",
 f"전체 함수 영역의 DET 전/후 normal Team Salary 상단은 **{d['whole_domain_normal_salary_pretrade_upper']:,} → {d['whole_domain_normal_salary_posttrade_upper']:,}**다. Tax136,606,000까지 **{d['tax_margin']:,}** 여유가 있어 비납세 matching을 쓸 수 있다. Out5,743,703, incoming9,881,598, 법정 matching상한 {d['nontax_matching_limit_exact']}·여유 {d['nontax_incoming_margin_exact']}다. 기존3m broadscreen은 tax를111,461 넘어서 해당 sufficientbound만 실패한다. 실제 불법 반례로 읽지 않는다.",
 f"Brooklyn은 어느 납세등급이든 최소 matching상한 {b['minimum_matching_limit_any_taxclass_exact']} >incoming5,743,703. 이번 거래에서 새 unusedTPE가 생기면 VII6m2 유효 서면renounce를 먼저 구성한다. 거래 직후 산입잔액과 동일하다는 주장이 아니다. 그 정리 뒤 같은 나머지 비용 B를 보존하면 B+9,881,598 →B+5,743,703로 **4,137,895 감소**한다. 일반 양도 자체는 새 hardcap을 만들지 않는다. 이미 적법한 선행 예산에 대한 headroom 보존 관계이며, 선행 Brooklyn 전체 원장을 만들어 인증한 것과 다르다. Hardcap 없는 팀의 음수 apron여유를 불법으로 선언하지 않는다.",
 '새 deemed예외의 apron 제외는 VII6m3F로 별도 연결한다. TPE가 원래 없었다고 추론하지 않는다. 원 protected급여와 Jordan current9,881,598는 유지한다. 원 buyout7,875,533를 쓰지 않는다. 적용되는 원 tradebonus가 있다면 당사자·양도팀의 적법한 fullwaiver 후보를 명시하며, 연장/재협상은 max(2022-03-04,otherwise eligible) 이후이다. Published performance0 가족은 실제 private Γ0 인증이 아니다. 동일 prior경제가족 밖의 새 알려진 비용은 그 항목을 재개방한다.',
 '9/4는 offseason이다. BKN 양도 전 STD+TW≤19가 있어야 순증1 후20 이내이고, 이 문서는 BKN 전체 명단을 선택하지 않았다. DET 최종15STD2TW/양수10명/240분은 원 운영후보에 보존되며 현재 Jordan 전액을 waiver 후에도 삭제하지 않는다.','',
 '## 현금과 공개 수집의 한계','',
 '[Woj 원보도](https://abcnews.com/Sports/sources-deandre-jordan-intends-sign-los-angeles-lakers/story?id=79824755)의 $5.78m는 기자 보고값이며 구단의 정확 장부액 인증이 아니다. 후보 qcash∈[1,5,780,000], 이전 BKN 지급/DET 수령 각≤5,000이면 법규 비율상단 아래5,785,000을 넘지 않는다. 지급·수령을 서로 상계하지 않는다. 정확 q/현행 실제 사용액은 null이다. 현금은 선수 Team Salary를 깎지 않는다.',
 '구단 indexed 본문은 실제 관측했고 여섯 attribution observation cache에 지문을 남겼다. 이것은 공급자 raw HTML이라고 부르지 않는다. Jordan/Sekou vendor 원계약행과 CBA/규약 raw는 직접 바이트 검문했다. 팀 salary URL이200이어도 실제2026–27 페이지였으므로 2021장부 근거에서 제외했다. API403은 본문 근거0이다. AGY2019 전환 질의55.066초 timeout/최종본문0은 별도 루트 리뷰에 남으며 반복 질의하지 않았다.','',
 '## 남은 정확한 입력','']
 lines += ['- '+x for x in o['remaining_named_scope']]
 lines += ['', '원역사 Aug6의 Hutchison WAS→SAS를 그대로 복사하면 승인된 GSW/MIN/NY 경로와 충돌한다. 이 선행 fiveway 또는 동등한 적법 권리 양도 후보의 변경세계 실행은 별도 입력이다. 이 국소 전이가 전체 BKN 예산·앞선 거래까지 완결했다고 표시하지 않았다. 새 A/B나 이적 방향 선택·실수락·전체3번·원고 승격0이다.', '',
 '[DET 초기 X](DETROIT_2021_INITIAL_RESIDUAL_COST_FAMILY_2026_10_07.md) · [DET 운영 후보](DETROIT_2021_OPENING_NAMED_OPERATING_FAMILY_2026_10_07.md) · [현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)', '',
 '|번호|묶음|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|Chicago2020–21|S2 완료|','|3|2021–23 거래·계약|DET/BKN 국소 비용·네 권리 전이 후보; 선행 BKN/fiveway·방향 남음|','|4|장기 커리어|후속 시즌 대기|','|5|결말·전체 구조|전체 기능표 미완료|','|6|집필 규격·Context Pack|현행 누적 등록기 참조·Pack0|','|7|통합·독립·작가 승인|최종 CLOSED|','', '미완료 큰 묶음5 / v0.30 PARTIAL / 설계·원고 CLOSED / 원고0.','']
 return '\n'.join(lines)
def self_test():
 tests=[];o=build()
 for label,f in [('wrong_origin2022',lambda x:x['joint_manifest']['claims'][0].update(origins=['WAS'])),('cash_netted',lambda x:x['cash'].update(netting_allowed=True)),('BKN_decrease_claimed_whole',lambda x:x['certification'].update(whole_BKN_cost_PASS=True))]:
  z=copy.deepcopy(o);f(z);assert validate(z);tests.append(label)
 p=copy.deepcopy(FIXED_POLICY);p['minimum_first_year_full_cash_upper']=3000000
 with patch(__name__+'.policy',return_value=p):
  try:build()
  except AssertionError:tests.append('constructor_restored_broad_tax_screen')
  else:raise AssertionError('Broad screen silently nontax')
 old=allocations
 def bad(rr):
  z=old(rr);z[1]['selector_cases'][0]['selected_origin']='WAS'if z[1]['selector_cases'][0]['selected_origin']=='MEM'else'MEM';return z
 with patch(__name__+'.allocations',side_effect=bad):
  try:build()
  except AssertionError:tests.append('constructor_wrong_better_pick_result')
  else:raise AssertionError('Shared wrong selector accepted')
 oldload=load
 def badsource(p):
  z=oldload(p)
  if p==operating.AR:z['outgoing_salary_candidates']['Sekou Doumbouya']-=100000;z['outgoing_salary_candidates']['Jahlil Okafor']+=100000
  return z
 with patch(__name__+'.load',side_effect=badsource):
  try:build()
  except AssertionError:tests.append('constructor_source_same_sum_wrong_players')
  else:raise AssertionError('Same sum source actor change accepted')
 p=copy.deepcopy(FIXED_POLICY);p['new_unused_BKN_TPE_if_any_valid_written_renunciation_before_normal_budget_comparison']=False
 with patch(__name__+'.policy',return_value=p):
  try:build()
  except AssertionError:tests.append('constructor_TPE_cleanup_omitted')
  else:raise AssertionError('New unused TPE silently excluded from normal comparison')
 oldtrace=make_trace
 def wrongtrace(*args):
  z=oldtrace(*args);z[3]['team_salary_upper']-=1000000;return z
 with patch(__name__+'.make_trace',side_effect=wrongtrace):
  try:build()
  except AssertionError:tests.append('constructor_same_endpoint_wrong_intermediate_budget')
  else:raise AssertionError('Dated refinement validated itself')
 return tests

def main():
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');s=a.parse_args();o=build()
 if s.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
 if s.check:assert not validate(load(OUT));assert text(MD)==markdown(o)
 print(json.dumps({'current':True,'rights':4,'selector_rows':1740,'DET_post_upper':o['DET']['whole_domain_normal_salary_posttrade_upper'],'BKN_delta':o['BKN']['normal_and_adjusted_apron_delta'],'whole_joint':False,'controls':self_test()if s.self_test else[]},ensure_ascii=False))


PINS={'research/DETROIT_2021_INITIAL_RESIDUAL_COST_FAMILY_2026_10_07.json': 'cf90a22c8fc7818a92a054c331347f836933ba0af83655464805048bcded5205', 'tools/build_detroit_2021_initial_residual_cost_family.py': '1b83376483bab330e381b6d6d9072c5a09e414fc617f955b80a00f32b5ba5c01', 'research/DETROIT_2021_OPENING_NAMED_OPERATING_FAMILY_2026_10_07.json': '7490b1a46a744088980c115680140383615a2e6ec92901e1fdd901c326861be0', 'tools/build_detroit_2021_opening_named_operating_family.py': 'ff635732271be6c65959a4d60e5f8f72deb79eba01fe1fb1c69532d000375fe9', 'research/O15G15AL_DETROIT_PRE_OLYNYK_ROSTER_CHARGE_SEQUENCE.json': 'cd0d31fced740134f94f34d1a6ce7b24c1205ce9360be3ae61e2d4abf43253b2', 'research/O15G15AQ_DETROIT_LEE_CAP_ROOM_AND_NONBIRD_ROUTE.json': '6b4806825d623e445f17a093239800a8f49f7841266244129818275681a622fa', 'research/O15G15AR_DETROIT_NAMED_EXIT_AND_ROSTER_CHARGE.json': '9f75d9af0af324303dc670249b023f69005dd3fb2624edf7322c4e2791469ac5', 'simulation/2020_DRAFT_TOP4_SEQUENTIAL_BOARD.md': '39073ff5e3f7ad86110454ae967e745a889e1875861a5a066a3897c7eb77b3cc', 'simulation/NBA_2020_21_APPROVED_TRANSACTION_EXECUTION_BRIDGE.json': '51755e614cd9827c7f60c0c07ef75851f1b20cdfdfb13348db7c512e84dcb968', 'research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json': '90099928f9133c4087ee7871939ce58216d183bd186f5ebd3575a56c2348eeed'}
OBSERVATIONS=[{'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-bkn-20261007\\CAP2017_observation.json', 'capture_sha256': '65246c977ce474ed5079fc072fe5ed6d790b05ef42cfa97451dcfefdf735df0f'}, {'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-bkn-20261007\\CAP2021_observation.json', 'capture_sha256': 'b72a2bf741d02532923d55ede5e0194688c9b81adc2354e20ab8b2671172c7d1'}, {'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-bkn-20261007\\NETS_AUG6_observation.json', 'capture_sha256': '72da8d1dce8bf42233bf453a2a58980c8ba3bf4a7dc41e3f0fe99a3930fb4b5e'}, {'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-bkn-20261007\\NETS_SEP4_observation.json', 'capture_sha256': 'fd313165d929c2fc269199f1e45493d4c6f12088c5b71800b71d2efcc19a0c96'}, {'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-bkn-20261007\\PISTONS_SEP29_observation.json', 'capture_sha256': 'a530dde6648c53cbd2a755e51fa90bc69dfe1292cc2083d6b037494354e56549'}, {'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-bkn-20261007\\WOJ_SEP3_observation.json', 'capture_sha256': '2e7bb67687d19edb2351ef0ae4baf60c9383fe883c531d5302c7b5db7784cf72'}]
RAW=[{'id': 'Jordan', 'url': 'https://www.salaryswish.com/players/deandre-jordan', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-bkn-20261007\\Jordan.raw', 'raw_sha256': '7aa008c3bcfb17d0f476bc78d3e68240735225ae403c666ddad22ee885489827', 'bytes': 159420}, {'id': 'Sekou', 'url': 'https://www.salaryswish.com/players/sekou-doumbouya', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-bkn-20261007\\Sekou.raw', 'raw_sha256': 'b94410d2b4116bd6a23ce134eb3c0f63d4a39165b91733a7f267777031f6054a', 'bytes': 113059}, {'id': 'Patty', 'url': 'https://www.salaryswish.com/players/patty-mills', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-bkn-20261007\\Patty.raw', 'raw_sha256': '214e3a0f5482d8c6365c9691f5d1ebf420c1032d9a8af7f779cbbe070c416d1a', 'bytes': 143649}, {'id': 'Dinwiddie', 'url': 'https://www.salaryswish.com/players/spencer-dinwiddie', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-bkn-20261007\\Dinwiddie.raw', 'raw_sha256': 'f34ebd9ce56aef575f51e9347a03d79708e153a120feabfbf6cba28d97791158', 'bytes': 138262}, {'id': 'BKN_Salary', 'url': 'https://www.salaryswish.com/teams/nets/2022', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-bkn-20261007\\BKN_Salary.raw', 'raw_sha256': '423121956a160a2ed9c7e1627637de5b0516aa06bfc65259629ba581764b110c', 'bytes': 157674}, {'id': 'BKN_OfficialProxy', 'url': 'https://api-hub.nba.com/news/nets-trade-deandre-jordan-to-pistons', 'status': 403, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-bkn-20261007\\BKN_OfficialProxy.raw', 'raw_sha256': 'aa744a30a2d2aa91f6e5e48fb2dace82ea1d2703bc0791f2899fff803d244264', 'bytes': 438}]
if __name__=='__main__':main()
