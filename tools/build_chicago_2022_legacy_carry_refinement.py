"""Remove a second old-camp reservation, preserving the global stretch bound.

This is a forward projection of the admitted public event family. It is not
proof that no private grievance exists, nor that all old waived Salary is zero.
"""
import argparse,copy,hashlib,json
from pathlib import Path
from unittest.mock import patch
import fitz
import build_chicago_2022_named_draft_rights_cost_refinement as named
import build_2021_chicago_a_full_cost_family as original

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_legacy_carry_refinement.py'
OUT='research/CHICAGO_2022_LEGACY_CARRY_REFINEMENT_2026_10_07.json'
MD=OUT[:-5]+'.md'
LEG='research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json'
OLD='research/CHICAGO_2022_FULL_COST_ROSTER_FAMILY_2026_10_07.json'
CBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
GUIDE=named.GUIDE
PAGES=[202,203,204,205,206,249,250]
CAMP=4372601
STRETCH=16371000

def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))

def policy():
 return {'target_capyear':'2022-23','new_waiver_or_grievance_resolution_selected':False,
 'all_valid_prior_stretch_annual_upper_preserved':STRETCH,
 'old_camp_fullcash_second_reservation_removed':CAMP,
 'original_private_payments_or_grievances_absence_certified':False,
 'ordinary_contract_expiry_is_payment_zero':False,
 '2020_modified_stretch_window_date_selected':None,
 '2020_camp_possible_stretch_is_covered_by_global_bound':True,
 'new_named_cost_or_resolution_reopens_projection':True,
 'whole_FY22_or_contract_choice_selected':False}
POLICY=copy.deepcopy(policy())

def source_inputs():return {'named':load(named.OUT),'legacy':load(LEG),'original':load(OLD)}

def checked_sources():
 s=source_inputs();n,l,o=(s[k]for k in ['named','legacy','original'])
 assert n==named.build(),'Reviewed named rights source differs'
 assert n['certification']['independent_review_completed']
 assert l==original.build(),'Original endpoint source differs'
 assert l['whole_source_supported_cost_family_pass']
 assert o==named.prior.build(),'Reviewed six-category source differs'
 assert o['certification']['independent_review_completed']
 b=l['legacy_remaining']['named_endpoint_bridge']
 assert b['all_named_camp_cash_and_resolution_reserved']==CAMP
 assert b['all_valid_prior_future_stretch_annual_upper']==STRETCH
 assert l['legacy_remaining']['aggregate_upper_usd']==CAMP+STRETCH
 assert o['candidate_policy']['no_new_waiver_settlement_grievance_or_cap_reducing_resolution_event_selected']is True
 assert o['candidate_policy']['legacy_reservation_preserved']==CAMP+STRETCH
 endpoints=b['ordinary_contracts']
 assert len(endpoints)==13
 assert all(int(r['last_ordinary_year'].split('-')[0])<=2020 for r in endpoints),'Ordinary FY22 contract cannot be removed'
 assert {r['player']for r in endpoints if r['last_ordinary_year']=='2020-21'}=={'Noah Vonleh','Zach Norvell Jr.','Simisola Shittu secondCHI'}
 return s

def evidence():
 assert hashlib.sha256(CBA.read_bytes()).hexdigest()==CBA_SHA
 with fitz.open(CBA)as d:
  pages={str(i):hashlib.sha256(d[i-1].get_text().encode()).hexdigest()for i in PAGES}
  a=' '.join(d[201].get_text().split())
  assert 'without regard to any revised payment schedule'in a
  assert 'Stretched Salary Amounts'in a
  g=' '.join(d[204].get_text().split())
  assert 'Salary Cap Year in which the Grievance is resolved'in g
  t=' '.join(d[249].get_text().split())
  assert 'all of the Team’s waived players (and any other former players)'in t
  assert 'fifteen percent (15%)'in t
 assert hashlib.sha256(GUIDE.read_bytes()).hexdigest()==named.GUIDE_SHA
 with fitz.open(GUIDE)as d:
  t=d[398].get_text()
  assert all(name in t for name in ['Sean Kilpatrick','Julyan Stone','Paul Zipser','Omer Asik'])
  page399={'PDF_1based':399,'printed_page':397,'text_sha256':hashlib.sha256(t.encode()).hexdigest()}
 return {'CBA':{'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(CBA),'raw_sha256':CBA_SHA,'PDF1based_text_sha256':pages,'clauses':['VII4(a)(1)(i) payment schedule vs Salary attribution','VII4(a)(1)(iii)(A)-(C) grievance-resolution-year charge','VII7(d)(6)(A)-(B) stretch timing','VII7(d)(6) all future waived/former Salary fifteen-percent limit']},
 'Bulls_official_guide':{'url':'https://chibullsdigital.com/mediaGuide/2022_ChicagoBulls_MG_NBA_HI.pdf','cache_path':str(GUIDE),'raw_sha256':named.GUIDE_SHA,'page':page399,'scope':'Positive 2018 named waiver events only; neither actual stretch election nor guaranteed money is inferred.'}}

def project(s,p):
 rows=[]
 for c in s['named']['refined_compact_cost_cells']:
  for r in c['states']:
   rows.append({'case':c['case'],'Carter':c['Carter'],'Protagonist':c['Protagonist'],
    'date':r['date'],'source_leaf_stage':r['source_leaf_stage'],
    'source_normal_upper':r['normal_full_public_category_outer'],
    'source_apron_upper':r['apron_full_public_category_outer'],
    'removed_duplicate_camp_reservation':CAMP,
    'normal_upper':r['normal_full_public_category_outer']-CAMP,
    'apron_upper':r['apron_full_public_category_outer']-CAMP,
    'preserved_all_old_stretch_upper':STRETCH,
    'contract_or_roster_selected':False})
 return rows

def assert_projection(rows,s):
 src={(c['case'],c['Carter'],c['Protagonist'],r['source_leaf_stage']):r for c in s['named']['refined_compact_cost_cells']for r in c['states']}
 assert len(rows)==len(src)==576
 assert len({(r['case'],r['Carter'],r['Protagonist'],r['source_leaf_stage'])for r in rows})==576
 for r in rows:
  a=src[(r['case'],r['Carter'],r['Protagonist'],r['source_leaf_stage'])]
  assert r['date']==a['date']
  assert r['removed_duplicate_camp_reservation']==CAMP and r['preserved_all_old_stretch_upper']==STRETCH
  assert r['source_normal_upper']==a['normal_full_public_category_outer'] and r['normal_upper']==a['normal_full_public_category_outer']-CAMP
  assert r['source_apron_upper']==a['apron_full_public_category_outer'] and r['apron_upper']==a['apron_full_public_category_outer']-CAMP
  assert r['contract_or_roster_selected']is False

def build():
 p=policy();assert p==POLICY,'Projection event/cash/stretch scope changed'
 s=checked_sources();ev=evidence();rows=project(s,p);assert_projection(rows,s)
 return {'id':'CHICAGO_2022_LEGACY_CARRY_REFINEMENT','status':'INDEPENDENTLY_REVIEWED_NO_SECOND_CAMP_RESERVATION_GLOBAL_STRETCH_PRESERVED',
 'source_sha256':{f:sha(f)for f in [named.OUT,named.SELF,LEG,original.SELF,OLD,named.prior.SELF,SELF]},
 'hash_convention':'Repository UTF8 BOMstrip LF; external bytes separate','sources':ev,'policy':p,
 'ordinary_endpoints':s['legacy']['legacy_remaining']['named_endpoint_bridge']['ordinary_contracts'],
 'projection_argument':[
 'All thirteen admitted ordinary contract terms end by2020-21. Fullcash was preserved in the earlier source model, not certified paid or unprotected.',
 'VII4a1i attributes former-player Salary to capyear regardless of revised cash-payment schedule; written Salary stretch is the explicit exception.',
 'Every valid future stretched Salary, including any2020 camp stretch surviving2022-23, is already inside the preserved global16.371m bound. Its timing need not be set to the ordinary2017 dates to count it inside that bound.',
 'A new resolution of past compensation in2022 can create a resolution-year charge underVII4a1iii. The existing inputfamily selects no such new event. A newly identified preserved award/settlement or new chosen event reopens this projection, not a privateabsence certificate.',
 'Potential2018 multiyear waivers can survive2022; they prohibit removing the generic stretch envelope using just the thirteenordinary endpoints. Preserve16.371m rather than assume those elections neveroccurred.',
 'Therefore legacy normal/apron reservation is16.371m in this same admitted future eventfamily, removing only the separate4.372601m camp fullcash duplicate.'
 ],
 'finite_counterexample_to_zero_all_stretch':{'named_events':['2018-07-12 Sean Kilpatrick waiver','2018-07-14 Paul Zipser waiver','2018-07-14 Julyan Stone waiver'],'conditional_example':'If two seasons remain at a July2018 waiver, VII7d6B allocates across five capyears2018-19 through2022-23. This is a timing counterexample to endpoint-only proof, not a claim that any player actually had those remaining terms or was stretched.','actual_election_or_debt_claimed':False},
 'refined_rows':rows,'summary':{'rows':len(rows),'compact_source_cells':192,'removed_reservation':CAMP,'legacy_upper_before':CAMP+STRETCH,'legacy_upper_after':STRETCH,'normal_range':[min(r['normal_upper']for r in rows),max(r['normal_upper']for r in rows)],'apron_range':[min(r['apron_upper']for r in rows),max(r['apron_upper']for r in rows)]},
 'scope':{'source_supported_public_preserved_family_only':True,'raw_original_CBA_scope_not_full2020_amendment_certificate':True,'2020_stretch_date_both_windows_overcovered_by_unchanged_global_bound':True,'all_other_categories_and_cardinality_and_slots_unchanged':True,'valid_2018_or2020_stretch_not_zeroed':True,'late_cash_is_not_automatic_new_capyear_salary':True,'new_grievance_charge_automatically_zero':False,'negative_apron_means_illegal':False,'new_private_receipt_or_all_hidden_clause_gate':False},
 'independent_review_basis':{'reviewer':'root','direct_original_CBA_PDF_pages':[202,203,204,205,206,249,250],'source_pin_comparisons':7,'external_raw_SHA':2,'independent_row_key_cost_comparisons':576,'controls_counted_as_independent':False,'accepted_scope':'Same admitted public event family, no new resolution, all prior future stretch 16371000 retained; remove only duplicate camp 4372601.'},
 'certification':{'independent_review_completed':True,'whole_FY22_selected_roster_cost_or_results':False,'actual_private_payment_or_grievance_absence_certified':False,'contract_or_pick_or_exact_amount_selected':None,'new_author_lock':False,'whole_macro3_complete':False,'REGISTER_or_central_changed':False,'manuscript_written':0}}

def validate(o):
 try:assert o==build(),'Saved projection/source differs';return[]
 except(AssertionError,KeyError,ValueError,OSError)as e:return[str(e)]

def markdown(o):
 x=o['summary'];return '\n'.join(['# Chicago FY22: 캠프 현금과 미래 stretch의 중복 예약 정밀화','',o['status'],'',
 '## 동일한 공개 보존 가족의 연도 연결','',
 '기존 13 ordinary계약의 끝점은2020–21 이전이다. 이는 지급0/보장0이라는 뜻이 아니다. [2017 CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) PDF202의VII4a1i는 지급일 변경과Salary연도 귀속을 구별하고, 서면Salary stretch를별도계산한다. PDF249–250의VII7d6은 **모든** 미래 waived/former-player Salary를연간15%cap제약으로검문한다. 기존16,371,000 상단은그전체범주를그대로남기므로2020캠프의가능한후속stretch도그안이다.2020개정calendar의정확stretch기한을새로인증하지않는다.','',
 'PDF203–206의VII4a1iii는과거보상 grievance가나중해결되면해결연도 비용이생길수있음을명시한다. 현재원후보정책은그런새waiver/award/settlement/resolution을선택하지않았다. 기존공개보존비용이나새사건이식별되면그항목을재개방한다. 사적분쟁이현실에없다거나실제지급이없다고인증하지않고, 무한한새미보고미래사건을현재family에추가하지않는다.','',
 '## 전체stretch 제거는 하지 않는다','',
 '[Bulls 공식가이드](https://chibullsdigital.com/mediaGuide/2022_ChicagoBulls_MG_NBA_HI.pdf) PDF399의2018Kilpatrick/Zipser/JulyanStone방출은기간이둘남았다면2018–19부터5년stretch가2022–23까지남을수있다는유한반례를준다. 실제잔여기간/보장/선택을사실로채우지않는다. 원13 ordinary끝점만보고16.371m전체를0으로줄이지않으며이상단을보존한다.','',
 f'따라서 동일family에서과거legacy예약20,743,601 중 캠프fullcash4,372,601을별도이중예약하지않고16,371,000을남기는 조건부계산이다. 기존192셀/576상태에서각Normal·apron에{CAMP:,} 감소만적용했다. Normal{x["normal_range"][0]:,}–{x["normal_range"][1]:,}, apron{x["apron_range"][0]:,}–{x["apron_range"][1]:,}. 다른다섯범주·권리수·명단슬롯·계약선택은바꾸지않는다. 이것은실제채무나전체FY22완료, 정확rounding·2020개정전문인증이아니다.','',
 '미완료큰묶음5 / v0.30 PARTIAL / 설계·원고CLOSED / 계약·픽·시즌미선택 / Pack0·원고0.',''])

def self_test():
 p=policy();p['all_valid_prior_stretch_annual_upper_preserved']=0
 with patch(__name__+'.policy',return_value=p):
  try:build();raise RuntimeError('FALSE_PASS remove_all_stretch')
  except AssertionError:pass
 p=policy();p['new_waiver_or_grievance_resolution_selected']=True
 with patch(__name__+'.policy',return_value=p):
  try:build();raise RuntimeError('FALSE_PASS new_resolution_without_cost')
  except AssertionError:pass
 orig=project
 def wrong(s,p):
  rows=orig(s,p);rows[0]['apron_upper']-=1;rows[1]['apron_upper']+=1;return rows
 with patch(__name__+'.project',side_effect=wrong):
  try:build();raise RuntimeError('FALSE_PASS same_total_cost_reallocation')
  except AssertionError:pass
 return 3

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');args=a.parse_args();o=build()
 if args.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
 if args.check:assert validate(load(OUT))==[] and text(MD)==markdown(o)
 print(json.dumps({'current':True,**o['summary'],'controls':self_test()if args.self_test else None}))
