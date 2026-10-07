"""Named 2022 Chicago draft-claim cardinality, not a new draft or rights choice."""
import argparse,copy,hashlib,itertools,json
from pathlib import Path
from unittest.mock import patch
import fitz
from bs4 import BeautifulSoup
import build_chicago_2022_full_cost_roster_family as prior
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_named_draft_rights_cost_refinement.py'
OUT='research/CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT_2026_10_07.json'
MD=OUT[:-5]+'.md'
A='canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json'
M1='canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json'
BRIDGE='simulation/NBA_2020_21_APPROVED_TRANSACTION_EXECUTION_BRIDGE.json'
BOARD='research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json'
TOP4='simulation/2020_DRAFT_TOP4_SEQUENTIAL_BOARD.csv'
GUIDE=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-bulls-guide.pdf')
GUIDE_SHA='113bf68ccc0d5b891f3bbc942a96f2c32b96caa6d3438299ebe92fc3ffebfe9e'
WIZ=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-chi2022-rights-20261007/wizards2019.raw')
WIZ_SHA='cbef465b9bb70f78c70985257ce29718210978f028f3cbaf462f79b769973a4d'
BI=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-chi-bi-cap-20210422.html')
BI_SHA='332a9ea81c3f01a934b31d61c2a57ea8a287c9cb1956741545c97b09ccdfb985'
PINS={A:'9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce',M1:'253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088',BRIDGE:'51755e614cd9827c7f60c0c07ef75851f1b20cdfdfb13348db7c512e84dcb968',BOARD:'90099928f9133c4087ee7871939ce58216d183bd186f5ebd3575a56c2348eeed',TOP4:'ee2cfced2cb1f026209806335b4146c68dca3ce6c30759069d4c903207633967',prior.OUT:'16830b560cf4f2008053ac236202010ff87188f42536a5d36870433933feccf0',prior.SELF:'13492290890cb954baef2f095aba13c316ea1b873547102f18950a02188f68e7'}
def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def policy():
 return {'year':2022,'first_count_upper':1,'second_count_upper':1,'new_2022_pick_transfer_selected':False,'exact_second_swap_exercise':None,'exact_2022_rank_or_player':None,'additional_POR_first_from_Markkanen_departure_copied':False,'DeRozan_second_outgoing_copied':False,'original_named_claims_preserved_not_rewritten':True,'whole_actual_portfolio_certified':False}
FIXED_POLICY=copy.deepcopy(policy())
def sources():
 assert all(sha(p)==h for p,h in PINS.items()),'Reviewed source changed'
 full=load(prior.OUT);assert not prior.validate(full),'Reviewed full-category envelope differs'
 assert full['certification']['independent_review_completed']
 assert load(A)['selected']['route']=='G1A_PLUS_M1'
 assert load(A)['mutually_exclusive_routes_not_selected']==['G1C_PLUS_M1_LONZO','G1D_PLUS_M1_DEROZAN']
 ev=next(e for e in load(BRIDGE)['events']if e['id']=='T2_VUCEVIC_NO_TRADE')
 assert ev['omitted_events']==['Historical CHI-ORL Vucevic assignment and its two first-round obligations']
 assert 'PRIMARY,4,Chicago Bulls,Patrick Williams,LaMelo Ball,AUTHOR_LOCKED' in text(TOP4)
 for path,h in [(GUIDE,GUIDE_SHA),(WIZ,WIZ_SHA),(BI,BI_SHA)]:assert hashlib.sha256(path.read_bytes()).hexdigest()==h
 with fitz.open(GUIDE)as d:
  pages={str(n):hashlib.sha256(d[n-1].get_text().encode()).hexdigest()for n in [398,400,402,403]}
  t400=' '.join(d[399].get_text().split())
  assert 'right to swap the Lakers’ pick for either Chicago’s or Detroit’s, whichever is more favorable' in t400
  assert 'Jameer Nelson' in d[397].get_text() and 'right to swap picks in the 2022 NBA Draft' in d[397].get_text()
  assert 'lottery protected 2022 first round pick to Chicago' in ' '.join(d[401].get_text().split())
  assert '18th overall pick in 2022 NBA Draft' in d[402].get_text()
 b=BeautifulSoup(BI.read_bytes(),'html.parser').select_one('#mvp-content-main').get_text(' ',strip=True)
 assert '2022 — The Bulls can swap second-rounders with the Detroit Pistons'in b
 assert 'May swap with the Los Angeles Lakers second-rounder from the Washington Wizards'in b
 w=BeautifulSoup(WIZ.read_bytes(),'html.parser').get_text(' ',strip=True)
 # NBA may put the article in serialized pageObject; check raw as well.
 assert 'right to swap 2022 second round picks'in WIZ.read_text(encoding='utf8')
 return full,[{'id':'BULLS_OFFICIAL_GUIDE_2022_23','url':'https://chibullsdigital.com/mediaGuide/2022_ChicagoBulls_MG_NBA_HI.pdf','cache_path':str(GUIDE),'raw_sha256':GUIDE_SHA,'PDF1based_text_sha256':pages,'locator':'PDF398/400 prior swaps;402 unchosen2021 departures;403 original2022 first selection','scope':'Retrospective named transaction endpoints; no alternate draft rank or player knowledge.'},{'id':'WIZARDS_ORIGINAL_2019_SATORANSKY_RELEASE','url':'https://www.nba.com/wizards/wizards-acquire-draft-pick-chicago','cache_path':str(WIZ),'raw_sha256':WIZ_SHA,'http_status':200,'publication_date':'2019-07-07','locator':'Opening transaction paragraph, 2022 swap; Lakers/Detroit detail omitted','counterparty_WAS_is_not_asserted_underlying_WAS_origin':True},{'id':'BI_ORIGINAL_DATED_PICK_SWAPS','url':'https://web.archive.org/web/20210422012709id_/http://www.basketballinsiders.com/chicago-bulls-team-salary/','cache_path':str(BI),'raw_sha256':BI_SHA,'body_updated':'2021-03-29','authority':'ORIGINAL_CAP_ANALYST_NOT_LEAGUE_LEDGER','locator':'#mvp-content-main/Pick Swaps/2022; one linked CHI/DET and LAL(WAS) swap entry; possible SAC residual','private_complete_portfolio_certified':False}]
def cardinality_cases():
 rows=[]
 for order in itertools.permutations(['CHI','DET','LAL']):
  # Ordinal placeholders are only relative ranks, not real2022 picks.
  rank={o:i for i,o in enumerate(order)}
  for exercise_chi,exercise_was in itertools.product([False,True],repeat=2):
   chi,det,lal='CHI','DET','LAL'
   if exercise_chi:chi,det=det,chi
   if exercise_was:chi,lal=lal,chi
   rows.append({'relative_order':list(order),'CHI_DET_swap_flag_superset':exercise_chi,'LAL_exchange_flag_superset':exercise_was,'Chicago_second_claim_count':1,'Chicago_underlying_origin_parameter':chi,'other_two_claims_not_Chicago':[det,lal],'exact_flags_selected':False,'these_flag_combinations_are_all_actual_legal_conditions':False})
 return rows
def assert_cases(rows):
 assert len(rows)==24 and len({(tuple(r['relative_order']),r['CHI_DET_swap_flag_superset'],r['LAL_exchange_flag_superset'])for r in rows})==24
 for r in rows:
  assert set(r['relative_order'])=={'CHI','DET','LAL'}
  chi,det,lal='CHI','DET','LAL'
  if r['CHI_DET_swap_flag_superset']:chi,det=det,chi
  if r['LAL_exchange_flag_superset']:chi,lal=lal,chi
  assert r['Chicago_underlying_origin_parameter']==chi and r['other_two_claims_not_Chicago']==[det,lal]
  assert r['Chicago_second_claim_count']==1 and len({chi,det,lal})==3,'A swap cannot mint another Chicago pick'
  assert not r['exact_flags_selected']and not r['these_flag_combinations_are_all_actual_legal_conditions']
def build():
 p=policy();assert p==FIXED_POLICY,'Named claims/count/choice scope changed'
 full,observed=sources();cases=cardinality_cases();assert_cases(cases)
 removed=(30-p['first_count_upper'])*prior.FIRST+(30-p['second_count_upper'])*prior.MINIMUM
 assert removed==407740000
 cells=[]
 for old in full['compact_joined_cost_cells']:
  new=copy.deepcopy(old)
  for r in new['states']:
   r['normal_full_public_category_outer']-=removed;r['apron_full_public_category_outer']-=removed
   r['all_current_draft_universe_reserved_not_registered']=False
   r['named_first_claim_upper']=1;r['named_second_claim_upper']=1
   r['economic_claims_reserved_not_live_UPCs']=True
  cells.append(new)
 assert len(cells)==192
 signed=[]
 for baseSTD in [13,14,15]:
  for f in full['TW_families']:
   slots=15-baseSTD-f['STD_added']
   if slots<0:continue
   for first_signed in range(min(1,slots)+1):
    for minimum_signed in range(min(2,slots-first_signed)+1):
     assert baseSTD+f['STD_added']+first_signed+minimum_signed<=15
     signed.append({'core_veteran_STD':baseSTD,'TW_family':f['id'],'first_signed':first_signed,'minimum_signed':minimum_signed,'first_unsigned':1-first_signed,'STD_total':baseSTD+f['STD_added']+first_signed+minimum_signed,'TW_total':f['TW_added'],'new_names_or_signatures_selected':False})
 return {'id':'CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT','status':'INDEPENDENTLY_REVIEWED_NAMED_PUBLIC_RIGHTS_CARDINALITY_NOT_DRAFT_SELECTED','source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'Repository BOMstrip LF; external raw bytes separate','sources':observed,'policy':p,'positive_claim_bridge':[{'id':'CHI2022_FIRST','count_upper':1,'basis':'Own-origin first survives accepted T2 omission; old2018 assignedfirst alreadyresolved in lockedboard; no new2022 assignment selected.'},{'id':'CHI2022_COMPOSITE_SECOND','count_upper':1,'origins_superset':['CHI','DET','LAL'],'basis':'Named2018 exchange then2019 Satoransky exchange preserve one residual economic slot; precise exercise/priority left unselected.'},{'id':'POR2022_CONDITIONAL_FIRST_NOT_IMPORTED','count_added':0,'basis':'Original2021 Markkanen departure is incompatible with approvedM1 retention; originalPORfirst not copied.'},{'id':'DEROZAN2022_OUTGOING_NOT_IMPORTED','count_removed':0,'basis':'RouteD is unselected; originalSAS outgoing is not a selected event.'}],
 'cardinality_superset_cases':cases,'case_scope':'These24 arbitrary exchange-flag/relative-order cases overcover public permitted exercise rules; cardinality is invariant for every subset. They do not certify an exact option exercise or all24 as actual legal outcomes.',
 'preserved_other_claims':'SAC/MEM/WAS/DET residual objects remain outside Chicago; their exact later holders are not automatically certified or newly reassigned.',
 'cost_interface':{'new_first_count_upper':1,'new_second_count_upper':1,'first_120pct_plus_all_performance_outer':prior.FIRST,'second_unaccepted_RT_fullcash_overreserve':prior.MINIMUM,'new_draft_envelope_total':prior.FIRST+prior.MINIMUM,'old_league_envelope_total':30*(prior.FIRST+prior.MINIMUM),'removed_overreservation':removed,'Simonovic_old_second_RT_reserved_separately':prior.MINIMUM,'new_2022_draftboard_or_contract_selected':False},'refined_compact_cost_cells':cells,'slot_family_forms':signed,
 'summary':{'compact_cells':192,'dated_states':576,'cardinality_cases':24,'first_rank_domain':[1,30],'second_rank_domain':[31,60],'available_signed_slot_forms':len(signed),'normal_range':[min(r['normal_full_public_category_outer']for c in cells for r in c['states']),max(r['normal_full_public_category_outer']for c in cells for r in c['states'])],'apron_range':[min(r['apron_full_public_category_outer']for c in cells for r in c['states']),max(r['apron_full_public_category_outer']for c in cells for r in c['states'])]},
 'scope':{'admitted_preserved_public_template_not_private_all_portfolio':True,'future_new_trade_or_new_known_claim_reopens_named_count':True,'first_lottery_rank_and_board_unselected':True,'second_exact_source_exercise_unselected':True,'all_live_UPCs_consume_STD_slots':True,'all60_as_Chicago_players_registered':False,'negative_apron_outer_is_illegal':False,'new_Bird_minimum_rookie_TW_hardcap':False,'FY21_hardcap_carried':False,'all_other_five_categories_preserved_from_reviewed_envelope':True},'independent_review_basis':{'reviewer':'den_pick_full_branch','direct_scope':'Three raw bodies and SHA; guidePDF398/400/402/403;7repository pins plus own;24cardinality cases;192cells/576states;1492slot forms;407740000 overreservation reduction. Prior5940 ancestor audit not recounted.','actual_constructor_rejections':['Two upstream compact cost cells +100000/-100000 preserving total rejected by reviewed full-category source guard.','Cardinality1 preserved but underlying origin replaced with WAS rejected by source-linked origin reconstruction.'],'own_three_controls_counted_as_independent':False,'actual_portfolio_or_exact_exercise_certified':False},'certification':{'independent_review_completed':True,'full_FY22_selected_roster_and_cost':False,'whole_macro3_complete':False,'actual_private_terms_or_real_portfolio_certified':False,'new_author_lock':False,'REGISTER_changed':False,'manuscript_written':0}}
def validate(o):
 try:assert o==build(),'Saved named-rights source/domain differs';return[]
 except(AssertionError,KeyError,ValueError,OSError)as e:return[str(e)]
def markdown(o):
 s=o['summary'];return '\n'.join(['# Chicago2022: 명명된 지명권 수와 신인 비용 예약 정밀화','',o['status'],'',
 '## 기존 양도에서 이어지는 한정 가족','',
 '기존 공개경제템플릿에서2022 자체1R 한 장과2022 복합2R 한 장을 비용입력으로 운반한다. 정확한2022승패·순번·선수·스왑행사는 선택하지 않았다. [Bulls 공식 가이드](https://chibullsdigital.com/mediaGuide/2022_ChicagoBulls_MG_NBA_HI.pdf) PDF398/400의2018·2019 스왑과 PDF402의 후속양도를 직접읽었고, [Wizards2019 원발표](https://www.nba.com/wizards/wizards-acquire-draft-pick-chicago) HTML도200본문을회수했다. 발표의WAS는상대팀이며 underlyingWAS자체픽이라고단정하지않는다. 가이드는 LAL과CHI/DET 비교권을명시한다. BI3/29단면의2022 PickSwaps 항목은이를명명하며 원리그영수증은아니다.','',
 '스왑은 원권리를 교환하며 Chicago에 두번째 권리를 새로 만들지 않는다. 세 출처의 상대순서6개와 두교환의가상flag4개로24개 상위경우를 검문했다. 정확행사제약보다넓은수학적상위집합이며24개모두실제합법옵션이라고인증하지않는다. 매경우 Chicago경제청구권은한장, 다른두권리는별도보존한다. SAC/MEM 등말단을새로정하지않는다.','',
 '승인된T2에서Vucevic거래와원두1R의무는생략됐으며 M1잔류에서POR2022first수취를복사하지않는다. A경로의DeRozan미선택은그2022second송출을복사하지않는다. 기존2020동결보드와2021작업60보드는그범위로만연결되며후대2022원18순위나선수는선택되지않는다. 새거래·알려진추가권리를채택하면명명항목을재계산하며모든미공표포트폴리오부재를검문문턱으로요구하지않는다.','',
 '## 비용·슬롯 연결','',f'기존league30+30예약421,800,000에서 한1R·한2R예약14,060,000으로 **407,740,000**을제거했다. 기존192정책셀·576날짜별비용에서다른다섯범주는그대로다. Normal범위{s["normal_range"][0]:,}–{s["normal_range"][1]:,}, apron범위{s["apron_range"][0]:,}–{s["apron_range"][1]:,}. 이것은계약상단예약이며실제채무·세금·전체FY22 PASS가아니다.',
 f'법정minimum3m 및first11.06m 조건부보고상단을유지하고 Simonovic기존RT3m는별도다. 신인첫UPC≤1, 추가minimum≤잔여슬롯을적용한{s["available_signed_slot_forms"]} 슬롯형식은max15STD/2TW 안이다. Unsigned/Tender는서명전명단선수가아니다. 이름·서명·2022보드미선택은그대로다. 기존Bird/minimum/rookie/TW는새hardcaptrigger없고 FY21trigger를이월하지않는다. 음수apron screen은그자체위법이아니다.','',
 '|번호|묶음|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23 거래·계약|명명된2022권리수 정밀화 후보·계약/시즌미선택|','|4|장기커리어|후속시즌대기|','|5|결말·전체구조|전체기능표미완료|','|6|집필규격·ContextPack|현행등록기참조·Pack0|','|7|통합·독립·작가승인|최종CLOSED|','','미완료큰묶음5 / v0.30 PARTIAL / 설계·원고CLOSED / 원고0.',''])
def self_test():
 old=cardinality_cases
 def wrong():
  r=old();r[0]['Chicago_second_claim_count']=2;return r
 with patch(__name__+'.cardinality_cases',side_effect=wrong):
  try:build();raise RuntimeError('FALSE_PASS swap_minted_pick')
  except AssertionError:pass
 p=policy();p['additional_POR_first_from_Markkanen_departure_copied']=True
 with patch(__name__+'.policy',return_value=p):
  try:build();raise RuntimeError('FALSE_PASS opposite_M1')
  except AssertionError:pass
 old=load
 def wrongsource(path):
  r=old(path)
  if path==A:r['selected']['route']='G1D_PLUS_M1'
  return r
 with patch(__name__+'.load',side_effect=wrongsource):
  try:build();raise RuntimeError('FALSE_PASS DeRozan_selected')
  except AssertionError:pass
 return 3
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();o=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
 if a.check:assert not validate(load(OUT));assert text(MD)==markdown(o)
 print(json.dumps({'current':True,**o['summary'],'controls':self_test()if a.self_test else None}))
