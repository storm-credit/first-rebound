"""Two named P1 asset gaps, source-supported conditional implementation only.

No selection of P1, future draft order, complete private portfolio or trade consent.
"""
import argparse, copy, hashlib, itertools, json
from pathlib import Path
from unittest.mock import patch
from bs4 import BeautifulSoup
import fitz

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_bkn_was_2021_p1_named_rights_bridge.py'
OUT = 'research/BKN_WAS_2021_P1_NAMED_RIGHTS_BRIDGE_2026_10_07.json'
MD = OUT[:-5]+'.md'
PREFIX = 'research/BKN_WAS_2021_PRE_JORDAN_NAMED_EXECUTION_FAMILY_2026_10_07.json'
JOINT = 'research/DETROIT_BROOKLYN_2021_JORDAN_JOINT_TRADE_FAMILY_2026_10_07.json'
RIGHTS = 'research/CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT_2026_10_07.json'
BOARD = 'research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json'
PINS = {
 PREFIX:'a0e9ede786047a43abac4d21785b68ae55190e3d768096618ed010147906017b',
 JOINT:'747fd807624c4e84242f8e8b3cc5935abe1133085dff3f7e3294eddb8bc1ea7a',
 RIGHTS:'bf8087a89af09a817c0a3eb5d4df906a906575a56016c873912db00eccdca9db',
 BOARD:'90099928f9133c4087ee7871939ce58216d183bd186f5ebd3575a56c2348eeed',
 'simulation/2020_DRAFT_VERNON_CAREY_RELANDING_BOARD.md':'50c2565f6f6c35248d6039c3ca72387f5021a47242faa68ba1af765b20ef79f6',
 'simulation/2020_DRAFT_NICK_RICHARDS_RELANDING_BOARD.md':'ec3e9eaf14b4565bc24bdaed7b00a60f21ef4a5ea0cd5f3e6d3a6eaad3e0282e',
 'simulation/2021_WASHINGTON_CHICAGO_PORTLAND_TRANSACTION_CASCADE.md':'70c7b3b944cd745496e940a9336ac521513002fe2c170ad0782aeb626ed8fa37',
}
TMP=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-p1-rights-20261007')
RAW = [
 ('PORTER2019','https://www.nba.com/news/bulls-trade-wizards-porter-official-release','0d512510507dbd81cadb1de4d1864e037b3dc9de9011012c822f47a6b68a9653'),
 ('SATO2019','https://www.nba.com/wizards/wizards-acquire-draft-pick-chicago','cbef465b9bb70f78c70985257ce29718210978f028f3cbaf462f79b769973a4d'),
 ('MEM2020','https://www.nba.com/wizards/cassius-winston-contract-childs-homesley-taylor-exhibit-10','f74de31a76c55604c6235b870e22d5a9078852457f0ece4d8cb2084671e33124'),
 ('NETS2021','https://www.nba.com/nets/news/2021/08/06/brooklyn-nets-acquire-future-draft-considerations-five-team-trade','9e89d704064427552ec520d3e66db90973f7bbfcf407d130eb61e8ee64fb93a0'),
 ('WAS2021','https://www.nba.com/wizards/washington-acquires-six-players-five-team-trade','2b819cbeed092e4588b4e9b951a06479f5d098f9917f4a0921e6ffb331f1419d'),
 ('LAL_HISTORY','https://www.salaryswish.com/trades/lakers','73b6513a7e0306435e1a56fb7006a6d5def4a76909491581933a1fdaf66bff18'),
]
BYLAW={'url':'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf',
 'path':'C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-2019-bylaws.pdf','raw_sha256':'6accb3d9633e15e8559d13228c27ae7b3b0b81eac0894050b06256eea6da3464'}
GUIDE={'url':'https://okcthunder.com/web-includes/ThunderMediaGuide2021-22.pdf',
 'path':'C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-den-primary-2026-10-07/OKC_2122.pdf',
 'raw_sha256':'94848cbdf59427f2dcd04db56bc6f924be88787ec4c5f252d917d7b378524564'}

def norm(s):return s.replace('\r\n','\n').replace('\r','\n')
def text(p):return norm((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def digest(o):return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load(p):return json.loads(text(p))

def raw_sources():
 sources=[]; bodies={}
 for key,url,h in RAW:
  p=TMP/(key+'.html');b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==h,'Raw source changed: '+key
  soup=BeautifulSoup(b,'html.parser')
  if key=='LAL_HISTORY':
   full=soup.get_text(' ',strip=True);start=full.index('Aug 6, 2021');end=full.index('Nov 23, 2020',start)
   s=full[start:end]
   assert '2023 2nd round pick (CHI' in s and 'LAL will receive the lower 2024 2nd round pick of WAS or MEM' in s
   bodies[key]=s
   sources.append({'id':key,'url':url,'cache_path':str(p),'raw_sha256':h,'http_status':200,
    'classification':'SECONDARY_VENDOR_RETROSPECTIVE_ORIGINAL_EVENT_TEMPLATE',
    'locator':'Visible Aug 6, 2021 trade block; Los Angeles Lakers Acquire subsection',
    'event_date':'2021-08-06','observed_summary':'보고된 LAL 수취청구는 CHI2023 및 MEM/WAS2024 덜유리한 쪽이다.',
    'future_resolved_rank_and_draftee_NOT_imported':True,'private_original_clause_certified':False})
   continue
  sc=soup.find('script',id='__NEXT_DATA__');assert sc is not None
  pp=json.loads(sc.string or sc.get_text())['props']['pageProps']
  if key=='PORTER2019':
   obj=pp['article'];s=obj['contentText'];locator='props.pageProps.article.contentText, opening transaction paragraph';date=obj['date']
   assert 'protected 2023 second-round draft pick' in s
  else:
   obj=pp['pageObject'];index={'SATO2019':0,'MEM2020':1,'NETS2021':0,'WAS2021':2}[key]
   s=obj['contentStructured'][index]['text'];date=obj['date'];locator=f'props.pageProps.pageObject.contentStructured[{index}].text'
  required={
   'SATO2019':['removed the protection on the 2023 second round pick','right to swap 2022 second round picks'],
   'MEM2020':['Memphis’ 2024 second round pick','owned by Oklahoma City','November 19th'],
   'NETS2021':['more favorable pick of Memphis or Washington','in 2024'],
   'WAS2021':['picks in 2023, 2024 and 2028 to the Los Angeles Lakers','2024 second-round pick','Brooklyn Nets'],
  }
  for needle in required.get(key,[]):assert needle in s,'Primary positive source statement changed: '+key
  bodies[key]=s
  summaries={'PORTER2019':'Porter 교환의 CHI발 2023 보호된 2라운드 청구.',
   'SATO2019':'이전2023 청구의 보호제거, 별도2022 swap.',
   'MEM2020':'11/19 OKC가 가진 MEM2024 2라운드를 WAS가 취득.',
   'NETS2021':'BKN은 MEM/WAS2024 더유리한 쪽을 취득.',
   'WAS2021':'LAL2023/24/28 및 BKN2024/2025swap 수취를 발표.'}
  sources.append({'id':key,'url':url,'cache_path':str(p),'raw_sha256':h,'http_status':200,
   'classification':'PRIMARY_ORIGINAL_OFFICIAL_RELEASE_SERIALIZED_BODY_DIRECT_READ',
   'publication_date_as_stored':date,'locator':locator,'observed_summary':summaries[key],
   'observed_field_UTF8_sha256':hashlib.sha256(s.encode()).hexdigest(),
   'browser_readable_shell_is_not_body':key!='PORTER2019','full_private_terms_certified':False})
 assert hashlib.sha256(Path(BYLAW['path']).read_bytes()).hexdigest()==BYLAW['raw_sha256']
 with fitz.open(BYLAW['path']) as d:
  s=d[86].get_text();assert '7.03. First Round Draft Choice.' in s and 'two (2)' in s
  sources.append({**BYLAW,'id':'NBA_BYLAWS2019','classification':'PRIMARY_RULE',
   'PDF1based':87,'printed_page':78,'page_text_LF_sha256':hashlib.sha256(norm(s).encode()).hexdigest(),
   'observed_summary':'§7.03 연속 미래1라운드 보유 제한. 본청구는 전부2라운드.'})
 # Guide scope is corroboration of origin contrast, not a transfer of WAS own2023 to LAL.
 gp=Path(GUIDE['path']);gb=gp.read_bytes();assert hashlib.sha256(gb).hexdigest()==GUIDE['raw_sha256']
 with fitz.open(gp) as d:
  p26=' '.join(d[25].get_text().split());p49=' '.join(d[48].get_text().split())
  assert 'Vít Krejcí' in p26 and 'Cassius Winston and a 2024 2nd round draft pick' in p26
  assert '2023 second-round draft pick (via Washington)' in p49 and 'from New Orleans' in p49
  sources.append({**GUIDE,'id':'OKC_2122_GUIDE_REUSED','classification':'PRIMARY_TEAM_RETROSPECTIVE_TRANSACTION_GUIDE',
   'raw_sha256':hashlib.sha256(gb).hexdigest(),'PDF1based':[26,49],'printed_pages':[50,51,96,97],
   'page_text_LF_sha256':{str(n):hashlib.sha256(norm(d[n-1].get_text()).encode()).hexdigest()for n in [26,49]},
   'observed_summary':'Krejci/Winston 거래와 별도 WAS발2023 청구의 OKC 수취.',
   'WAS_own2023_is_not_CHI2023':True})
 return sources

def source_inputs():
 for p,h in PINS.items():assert sha(p)==h,'Unreviewed source change: '+p
 objs={p:load(p)for p in [PREFIX,JOINT,RIGHTS,BOARD]}
 for p,o in objs.items():assert o==json.loads(text(p)),'Reader changed source semantics: '+p
 assert objs[PREFIX]['policy']['candidate']=='P1_SEPARATE_LAL_WAS_THEN_BKN_WAS_SAS' and not objs[PREFIX]['policy']['selected']
 assert objs[JOINT]['policy']['four_named_second_claims_preserve_existing_conditions']
 assert objs[RIGHTS]['policy']['year']==2022 and not objs[RIGHTS]['policy']['new_2022_pick_transfer_selected']
 prior2022=[r for r in objs[RIGHTS]['positive_claim_bridge']if r['id']=='CHI2022_COMPOSITE_SECOND']
 assert len(prior2022)==1 and prior2022[0]['basis']=='Named2018 exchange then2019 Satoransky exchange preserve one residual economic slot; precise exercise/priority left unselected.'
 board={x['pick']:x for x in objs[BOARD]['rows']}
 assert board[22]['player']=='Jared Butler' and board[22]['conditional_final_draft_rights_holder']=='LAL'
 assert '| 37 | Oklahoma City | Vít Krejčí |' in text('simulation/2020_DRAFT_VERNON_CAREY_RELANDING_BOARD.md')
 assert '| 53 | Washington | Cassius Winston |' in text('simulation/2020_DRAFT_NICK_RICHARDS_RELANDING_BOARD.md')
 return objs

def named_claims():
 return [
  {'id':'CHI_2023_2R','origin':'CHI','year':2023,'round':2,'pre_P1_holder':'WAS','protection':'REMOVED_2019_07_07_POSITIVE_RELEASE','E1_recipient':'LAL','E2_recipient':'LAL'},
  {'id':'MEM_2024_2R','origin':'MEM','year':2024,'round':2,'pre_P1_holder':'WAS','prior_acquisition':'OKC_TO_WAS_2020_11_19','private_full_terms_selected':False},
  {'id':'WAS_2024_2R','origin':'WAS','year':2024,'round':2,'pre_P1_holder':'WAS','prior_acquisition':'OWN_ORIGIN_IN_PUBLISHED_PAIR_TEMPLATE','private_full_terms_selected':False},
 ]
FIXED_CLAIMS=copy.deepcopy(named_claims())

def allocate(m,w):
 assert 31<=m<=60 and 31<=w<=60 and m!=w
 more='MEM_2024_2R' if m<w else 'WAS_2024_2R';less='WAS_2024_2R' if m<w else 'MEM_2024_2R'
 return {'MEM_rank':m,'WAS_rank':w,'E1_LAL_residual':less,'E1_WAS_retained_senior':more,
  'E2_BKN_senior':more,'E2_LAL_residual_preserved':less,'September_BKN_to_DET_same_senior':more}

def assert_case(c):
 m,w=c['MEM_rank'],c['WAS_rank'];assert 31<=m<=60 and 31<=w<=60 and m!=w
 more='MEM_2024_2R' if m<w else 'WAS_2024_2R';less='WAS_2024_2R' if m<w else 'MEM_2024_2R'
 assert c=={'MEM_rank':m,'WAS_rank':w,'E1_LAL_residual':less,'E1_WAS_retained_senior':more,
  'E2_BKN_senior':more,'E2_LAL_residual_preserved':less,'September_BKN_to_DET_same_senior':more},'Allocation differs from positive selector/conservation policy'
 assert {c['E2_BKN_senior'],c['E2_LAL_residual_preserved']}=={'MEM_2024_2R','WAS_2024_2R'}

def build():
 objs=source_inputs();sources=raw_sources();claims=named_claims();assert claims==FIXED_CLAIMS,'Named origin/year/protection/source bridge changed'
 cases=[allocate(m,w)for m,w in itertools.permutations(range(31,61),2)]
 for c in cases:assert_case(c)
 assert len(cases)==870 and len({(c['MEM_rank'],c['WAS_rank'])for c in cases})==870
 return {'id':'BKN_WAS_2021_P1_NAMED_RIGHTS_BRIDGE','baseline_main':'1b7d7b9',
  'status':'INDEPENDENTLY_REVIEWED_SOURCE_SUPPORTED_CONDITIONAL_TWO_GAP_BRIDGE',
  'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8_BOM_STRIPPED_CRLF_CR_TO_LF_REPOSITORY; EXTERNAL_RAW_BYTES_SEPARATE',
  'sources':sources,'named_claims':claims,
  'prior_claim_carry_authority':{
   'reviewed_2019_Satoransky_economic_family_reference':RIGHTS+'#/positive_claim_bridge/1',
   'existing_reference_scope':'2019 exchange preserved for one2022 economic slot; not a standalone2023 alternate dated ledger certification',
   'exact_CHI2023_to_WAS_and_unprotect_previously_author_locked_verified':False,
   'CHI2023_origin_role':'SECONDARY_EXPLICIT_ORIGIN_REPORT + PRIMARY_CHI_OUTGOING2023_AND_PROTECTION_REMOVAL',
   'MEM2024_prior_carry_role':'PRIMARY_ORIGINAL_ACQUISITION + CURRENT_KREJCI37_WINSTON53_RETENTION_TEMPLATE',
   'candidate_condition':'Preserve the named publicly reported earlier exchanges and their 2023/2024 economic claims in this conditional P1 family.',
   'historical_completion_is_not_alternate_execution_proof':True,
   'new_conditional_prior_claim_carry_is_not_canon_promotion':True},
  'dated_bridge':[
   {'event':'PORTER2019','release_date':'2019-02-07','edge':'CHI_2023_2R CHI→WAS','class':'HISTORICAL_FACT; FINITE_PRESERVED_PUBLIC_TEMPLATE'},
   {'event':'SATO2019','release_date':'2019-07-07','edge':'CHI_2023_2R protection removed; different 2022 swap untouched','class':'HISTORICAL_FACT; FINITE_PRESERVED_PUBLIC_TEMPLATE'},
   {'event':'WINSTON2020','event_date_reported':'2020-11-19','edge':'MEM_2024_2R OKC→WAS','class':'HISTORICAL_FACT; NO NEW_DRAFT_BOARD_SELECTION'},
   {'event':'P1_E1','candidate_date':'2021-08-06','edge':'CHI_2023_2R WAS→LAL; complementary MEM/WAS2024 residual WAS→LAL, senior retainedWAS','class':'CONDITIONAL_LEGAL_IMPLEMENTATION_CANDIDATE'},
   {'event':'P1_E2','candidate_date':'2021-08-06','edge':'MEM/WAS2024 senior WAS→BKN; LAL residual unchanged','class':'CONDITIONAL_LEGAL_IMPLEMENTATION_CANDIDATE'},
   {'event':'JORDAN_B_CANDIDATE','candidate_date':'2021-09-04','edge':'same BKN senior→DET; LAL residual unchanged','class':'OTHER_ALREADY_REVIEWED_UNSELECTED_FAMILY_REFERENCE'}],
  'conditional_joint_asset_terms':{
   'E1_prior_holder':'WAS','E1_LAL_receives':['CHI_2023_2R','LESS_FAVORABLE_2024_MEM_WAS'],
   'E1_WAS_retains':'MORE_FAVORABLE_2024_MEM_WAS','E2_WAS_assigns_to_BKN':'MORE_FAVORABLE_2024_MEM_WAS',
   'both_events_require_same_pair_definition_and_recognized_senior_encumbrance':True,
   'new_2024_underlying_protection_or_conversion_added':False,'original_private_selector_terms_certified':False,
   'LAL_less_selector_source_role':'POSITIVE_SECONDARY_TEMPLATE + PRIMARY_BKN_MORE + TWO_ORIGIN_CONSERVATION; NOT PRIMARY_EXACT_PRIVATE_CLAUSE',
   'original_2023_protection_removed_positive_primary':True,'known_other_2023_WAS_origin_not_reassigned':True,
   'prior_named_public_obligations_preserved':True,'no_arbitrary_private_portfolio_absence_gate':True},
  'scope':{'universal_rank_cases':870,'future_actual_ranks_selected':False,'original_resolved_vendor_players_imported':False,
   'Stepien_first_round_projection_unchanged':True,'all_new_claims_round':2,'NBA_UPC_or_player_option_change':False,
   'no_equation_of_draft_rights_with_signed_contract':True,'cash_salary_roster_or_hardcap_new_proof':False,
   '2028_original_claim_reused_not_newly_proved_here':True,
   '2020_2022_2025_prior_claims_preserved_not_duplicate_2023_2024':True,
   'original_source_dates_not_exact_league_receipt_times':True},
  'certification':{'named_origin_2023_supported':True,'conditional_complementary_2024_family_supported':True,
   'whole_P1_legal_or_financial_PASS':False,'whole_WAS_BKN_cost_PASS':False,'new_author_lock':False,
   'prior_claims_alternate_dated_execution_certified':False,
   'P1_selected':False,'actual_player_team_acceptance':None,'actual_private_original_terms':None,
   'future_exact_rank_owner_player':None,'independent_review_completed':True,
   'independent_review_basis':'Root separately read five serialized official bodies and their stored UTC publication dates, checked 870 rank pairs by independent sorted-origin allocation and rejected real same-origin duplication and CHI2023-to-WAS-origin mutations. Local calendar Aug6 and stored publication Aug7UTC are distinguished; Porter full stored timestamp corrected. Prior alternate claim carry remains conditional and P1 unselected. Author self-tests are not independent checks.',
   'macro3_complete':False,'manuscript_authorized':False,'register_promotion':False},
  'remaining': ['P1 important transaction direction remains unselected.',
   'WAS remaining whole-cost residual and other P1 actor obligations are independent existing scopes.',
   'LAL2024 exact original selector has secondary positive report; primary full clause not asserted. This packet verifies the explicit candidate complementary family.'],
  'permutation_cases':cases}

def validate(o):
 try:
  for c in o['permutation_cases']:assert_case(c)
  assert o==build(),'Saved/source-bound output differs'
  return []
 except (AssertionError,KeyError,ValueError) as e:return [str(e)]

def render(o):
 return '''# P1의 CHI2023 원픽·MEM/WAS2024 상보 청구

root 독립검문을 마친 공개 지원 후보다. P1을 선택하거나 실제 거래 접수/미래 순번을 인증하지 않는다.

## 두 공백에 연결한 새 본문

| 원자료 | 실독 위치·역할 |
|---|---|
| [Bulls Porter 공식발표](https://www.nba.com/news/bulls-trade-wizards-porter-official-release) | article.contentText 첫 거래문단: CHI→WAS의 보호된2023 청구 |
| [WAS Satoransky 공식발표](https://www.nba.com/wizards/wizards-acquire-draft-pick-chicago) | pageObject.contentStructured[0]: 2019-07-07 보호제거; 별도2022 swap 보존 |
| [WAS Winston 공식발표](https://www.nba.com/wizards/cassius-winston-contract-childs-homesley-taylor-exhibit-10) | [1]: 2020-11-19 OKC→WAS MEM2024 청구 |
| [Nets 2021 공식발표](https://www.nba.com/nets/news/2021/08/06/brooklyn-nets-acquire-future-draft-considerations-five-team-trade) | [0]: BKN의2024 더유리한 쪽 |
| [WAS 2021 공식발표](https://www.nba.com/wizards/washington-acquires-six-players-five-team-trade) | [2]: LAL2023/24/28·BKN2024 양도 발표 |
| [SalarySwish LAL 거래이력](https://www.salaryswish.com/trades/lakers) | Aug6,2021 LAL subsection: CHI2023·2024 덜유리한 쪽의 **2차 경제템플릿** |

일부 브라우저 open은 iframe만 보였다. 실제 HTTP200 raw의 __NEXT_DATA__ 해당필드를 따로 읽고 지문을 남겼다. 검색요약을 본문으로 계수하지 않는다. 공급자 표에 붙은 후대 순번·실제 지명선수·swap 행사 결과는 가져오지 않았다. 원자료의 발표 날짜와 실제 리그 접수 시각은 같다고 인증하지 않는다.

## 명명된 조건부 두 사건

2019 CHI2023 보호제거 및2020 MEM2024 취득을 보존한다는 **조건부 공개 가족 제안**이다. 현행 검문된 CHI2022 positive_claim_bridge는2019 Satoransky 교환과2022 경제슬롯을 보존하지만, 별도 CHI2023→WAS/보호제거의 대체세계 날짜별 원장행을 이미 잠갔다는 인증은 하지 않는다. CHI2023 정확 origin은2차 원거래 표, CHI의 송출·보호제거는 공식본문이 지원하는 범위를 나눈다. 기존2020 Krejci37/Winston53 유지 주안과도 연결하되 새로운2020 보드·선행권리의 정본 승격은 하지 않는다. 이 명명된 prior-claim carry 조건을 허용하는 P1가족을 검문하며 원역사 완료만으로 대체세계 전이를 인증하지 않는다.

E1에서 WAS는 CHI2023과2024의 덜유리한 청구를 LAL에 양도하고 같은 두 원권리의 더유리한 청구를 보유한다. E2에서 그 보유청구를 BKN으로 양도한다. E1 수취자는 BKN으로 갈 선순위 청구가 같은 원권리에 붙는다는 조건을 받아야 한다. 이는 새 합의의 법적 구현 후보이며 실제 승낙을 골랐다는 뜻이 아니다. 순서 변경으로 같은 원픽을 두 번 소비할 수 없다. 후속 검문된 Jordan B 후보는 BKN이 수취한 그 청구만 DET로 운반한다.

MEM·WAS 순번을31~60 중 서로 다르게 놓은870쌍 모두에서 min은 BKN/후속DET, max는 LAL이다. 두 자산 합집합은 원두권리와 일치하고 교집합은 비어 있다. 정확 원역사 LAL less 조항을 공식 원계약으로 인증하지 않는다. 공식 BKN more·WAS 수취개수와 직접 회수한2차 less 보고를 지원으로 삼아 이 **명시적 상보 후보**를 검문한다. 공개범위 밖 모든 숨은 조항의 부재나 사적 영수증을 새 완료요건으로 만들지 않는다.

OKC 공식가이드 PDF26/49가 별도의 WAS발2023 청구와 CHI2023의 혼동을 막는다. 2020에 전달된2R·별도2022 swap·기존2025 swap은 이2023/2024 배분과 같은 연도 원픽으로 중복 등록하지 않는다. 모든 새청구는2R이므로2019 NBA규약§7.03(PDF87/인쇄78)의 연속 미래1R 보유 투영은 불변이다. 이를 전체 Stepien/2028/다른 거래 인증으로 확대하지 않는다.

## 남은 범위

두 명명된 공백의 후보 입력을 공급한다. 중요한 P1 방향·다른 당사자 비용·WAS 잔여상단·실제 접수/승낙·정확 미래순번은 미선택이다. 기존 prefix나 원장에 PASS를 자동 반영하지 않았다.

| 전체7행 | 현황 |
|---|---|
|1 2020 드래프트 연쇄|완료 유지|
|2 Chicago2020–21|S2 완료 유지|
|3 2021–23 거래·계약|진행; P1 등 중요한 후보 미선택|
|4 장기 커리어|선행 확정 대기|
|5 결말·전체구조|한정 기능·출구 진행|
|6 집필규격·Context Pack|진행·Pack0|
|7 통합·독립·작가승인|미완료|

미완료 큰묶음5. v0.30 PARTIAL·설계/원고 CLOSED·원고0. 이 패킷은 새 작가잠금0이다.
'''

def self_test():
 good=build();n=0
 bad=copy.deepcopy(good);bad['named_claims'][0]['origin']='WAS';assert validate(bad);n+=1
 bad=copy.deepcopy(good);c=bad['permutation_cases'][0];c['E2_LAL_residual_preserved']=c['E2_BKN_senior'];assert validate(bad);n+=1
 original=named_claims
 def wrong_claim():
  x=original();x[0]['protection']='TOP36_UNCHANGED';return x
 with patch(__name__+'.named_claims',wrong_claim):
  try:build();raise RuntimeError('False PASS')
  except AssertionError:n+=1
 original_allocate=allocate
 def wrong_alloc(m,w):
  x=original_allocate(m,w);x['E1_LAL_residual']=x['E1_WAS_retained_senior'];return x
 with patch(__name__+'.allocate',wrong_alloc):
  try:build();raise RuntimeError('False PASS')
  except AssertionError:n+=1
 bad=copy.deepcopy(good);bad['certification']['P1_selected']=True;assert validate(bad);n+=1
 return n

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args()
 o=build()
 if a.write:
  (ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(render(o),encoding='utf8')
 if a.check:
  errors=validate(load(OUT));assert not errors,errors;assert text(MD)==render(o)
 print(json.dumps({'current':True,'cases':870,'new_author_lock':False,'negative_controls':self_test()if a.self_test else None}))
if __name__=='__main__':main()
