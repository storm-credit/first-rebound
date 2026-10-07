"""Named current-year residual components; no whole Washington cost promotion."""
import argparse, copy, hashlib, json
from pathlib import Path
from unittest.mock import patch
from bs4 import BeautifulSoup
import fitz
import build_detroit_2021_initial_residual_cost_family as parser

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_washington_2021_named_residual_cost_components.py'
OUT='research/WASHINGTON_2021_NAMED_RESIDUAL_COST_COMPONENTS_2026_10_07.json'
MD=OUT[:-5]+'.md'
PREFIX='research/BKN_WAS_2021_PRE_JORDAN_NAMED_EXECUTION_FAMILY_2026_10_07.json'
CW='research/CHA_WAS_FINITE_ROSTER_WORKING_FAMILY_2026_10_07.json'
RAW_META=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-was-residual-20261007/sources.json')
CBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
MILES_FOLDER=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-miles-clock-20261007')
MILES_RAW_META_SHA='a055e72694bb739a359e83430d81aeddf063277ef62ba22d9c30913bc582b429'
MILES_OBSERVATION_SHA='c445d8edfda6785d029c9fd46dde2e607f4b69a8db9906a00d2923ee10011728'

def txt(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(txt(p).encode()).hexdigest()
def load(p):return json.loads(txt(p))
def normal_json(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def row_groups(body):
 return [[r for r in t if len(r)==8 and r[0][:4].isdigit()] for t in parser.tables(body)]

def sources():
 for p,h in PINS.items():assert sha(p)==h,'Current repository source changed: '+p
 prefix=load(PREFIX);cw=load(CW)
 assert prefix==json.loads(txt(PREFIX)) and cw==json.loads(txt(CW)),'Source reader changed semantics'
 assert prefix['WAS']['closing_fixed_without_Din_or_residual']==126026705
 assert prefix['WAS']['Homesley_waiver_full_2021_charge_reserved']==1517981
 assert prefix['WAS']['examples_are_source_X_upper_certificate']is False
 assert not prefix['certification']['whole_changed_fiveway_legal']
 assert hashlib.sha256(RAW_META.read_bytes()).hexdigest()==META_SHA,'Collection metadata changed'
 raw=json.loads(RAW_META.read_bytes());bodies={};records=[]
 assert len(raw)==14
 for r in raw:
  assert 'error'not in r and r['status']==200
  b=Path(r['cache_path']).read_bytes();assert hashlib.sha256(b).hexdigest()==r['raw_sha256']
  soup=BeautifulSoup(b,'html.parser');title=soup.title.get_text(' ',strip=True)
  assert 'Player not found'not in title,'No contract body: '+r['id']
  groups=row_groups(b);bodies[r['id']]=groups
  records.append({**r,'source_tier':'SECONDARY_REPORTED_CONTRACT_TEMPLATE','title':title,'all_contract_row_groups':groups,'title_success_is_complete_contract_history':False})
 assert hashlib.sha256(CBA.read_bytes()).hexdigest()==CBA_SHA
 pages={}
 with fitz.open(CBA)as d:
  for p in [197,198,202,203,204,205,206,240,241,248,249,250,302,303]:
   t=d[p-1].get_text().replace('\r\n','\n').replace('\r','\n')
   pages[str(p)]=hashlib.sha256(t.encode()).hexdigest()
  assert 'fifteen percent (15%)'in ' '.join(d[249].get_text().split())
 return prefix,cw,bodies,records,pages

def miles_sources():
 rp=MILES_FOLDER/'sources.json';op=MILES_FOLDER/'observations.json'
 assert hashlib.sha256(rp.read_bytes()).hexdigest()==MILES_RAW_META_SHA
 assert hashlib.sha256(op.read_bytes()).hexdigest()==MILES_OBSERVATION_SHA
 raw=json.loads(rp.read_bytes());obs=json.loads(op.read_bytes())
 assert [r['id']for r in raw]==[r['id']for r in obs]==['NBA_AP_2017','TOR_2017','WAS_2019','NBA_AP_2020']
 for r in raw:
  assert r['status']==403 and hashlib.sha256(Path(r['cache_path']).read_bytes()).hexdigest()==r['raw_sha256']
 assert obs[0]['reported_start_cap_year']==2017 and obs[0]['reported_seasons']==3
 assert obs[1]['official_multi_year_signing_confirmed']and not obs[1]['official_exact_seasons_or_money_disclosed']
 assert obs[2]['WAS_acquires_Miles_for_Howard']and obs[3]['WAS_waives_Miles']
 assert obs[3]['publication_date']=='2020-01-12'
 return {'failed_direct_raw_attempts':raw,'web_attribution_captures':obs,'capture_is_provider_full_body_raw':False,'observation_capture_sha256':MILES_OBSERVATION_SHA,'collection_meta_sha256':MILES_RAW_META_SHA}

def miles_window():
 # VII7(d)(6)(A): current year unchanged, only years AFTER current may stretch.
 return {'published_template_seasons':[2017,2018,2019],'waive_date':'2020-01-12','waive_salary_cap_year':2019,'waive_in_September_to_June_window':True,'post_current_remaining_seasons':[],'current_components_protected_or_bonus_kept_in_2019_20':True,'original_ordinary_or_stretched_2021_22_component':0,'money_25000000_is_bonus_or_protection_upper':False,'actual_private_current_payment_or_notice_certified':False,'later_new_resolution_or_new_UPC_reopens':True}

def ordinary_components(b):
 # Original reported waived-three-year family, not a $0 protected-column receipt.
 p=[g for g in b['anzejs-pasecniks']if len(g)==3 and g[0][0]=='2019-20'and g[1][0]=='2020-21 W'and g[2][0]=='2021-22 W']
 assert len(p)==1 and p[0][2][3:]==['$1,782,621','$1,782,621 (+55%)','$0','$0','$0'],'Pasecniks original future component changed'
 r=[g for g in b['jerome-robinson']if len(g)==4 and g[0][0]=='2018-19'and g[-1][0]=='2021-22 W']
 assert len(r)==1 and r[0][-1][1:3]==['Team','No (Dec 29, 2020)'],'Robinson option identity changed'
 expected={'ish-smith':(2,'2019-20','2020-21',6000000),'robin-lopez':(1,'2020-21','2020-21',7300000),'raul-neto':(1,'2020-21','2020-21',1620564),'alex-len':(1,'2020-21','2020-21',1265372),'ian-mahinmi':(4,'2016-17','2019-20',15450051),'yoeli-childs':(1,'2020-21 W','2020-21 W',898310),'marlon-taylor':(1,'2020-21 W','2020-21 W',898310)}
 ended=[]
 for actor,(length,first,last,cap)in expected.items():
  groups=[g for g in b[actor]if len(g)==length and g[0][0]==first and g[-1][0]==last and int(''.join(x for x in g[-1][3]if x.isdigit()))==cap]
  assert len(groups)==1,'Named ordinary contract endpoint absent: '+actor
  ended.append({'actor':actor,'reported_original_rows':groups[0],'ordinary_salary_last_season':last[:7],'next_year_new_team_or_new_UPC_not_imported':True,'later_award_stretch_or_current_payment_not_certified_zero':True})
 return {'Pasecniks':{'reported_three_year_rows':p[0],'candidate_full_2021_22_future_ordinary_reserve':1782621,'protected_column_zero_is_actual_payment_zero':False,'reserve_not_selected_actual_salary_or_paid_receipt':True},'Robinson':{'reported_rookie_rows':r[0],'candidate_year4_nonexercise_preserved':True,'hypothetical_unexercised_year4_5340914_not_current_salary':True,'old_year3_or_later_resolution_not_erased':True},'ordinary_ended':ended}

def check_components(o,b):
 expected=ordinary_components(b)
 assert o==expected,'Returned named contract component differs from source endpoint/charge'
 # This caller binds the charge independently of a replaceable constructor.
 assert o['Pasecniks']['candidate_full_2021_22_future_ordinary_reserve']==1782621
 assert o['Pasecniks']['protected_column_zero_is_actual_payment_zero']is False
 assert o['Robinson']['candidate_year4_nonexercise_preserved']is True
 assert [r['actor']for r in o['ordinary_ended']]==['ish-smith','robin-lopez','raul-neto','alex-len','ian-mahinmi','yoeli-childs','marlon-taylor']
 endpoints=[('2019-20','2020-21',2,6000000),('2020-21','2020-21',1,7300000),('2020-21','2020-21',1,1620564),('2020-21','2020-21',1,1265372),('2016-17','2019-20',4,15450051),('2020-21 W','2020-21 W',1,898310),('2020-21 W','2020-21 W',1,898310)]
 for r,(first,last,length,cap)in zip(o['ordinary_ended'],endpoints):
  src=[g for g in b[r['actor']]if len(g)==length and g[0][0]==first and g[-1][0]==last and int(''.join(x for x in g[-1][3]if x.isdigit()))==cap]
  assert r['reported_original_rows']==src[0] and r['ordinary_salary_last_season']==last[:7],'Returned ordinary endpoint differs from named source'
  assert r['next_year_new_team_or_new_UPC_not_imported']is True and r['later_award_stretch_or_current_payment_not_certified_zero']is True
 assert o['Pasecniks']['reported_three_year_rows']in b['anzejs-pasecniks']
 assert o['Pasecniks']['reported_three_year_rows'][2][0]=='2021-22 W'
 assert o['Robinson']['reported_rookie_rows']in b['jerome-robinson']
 assert o['Robinson']['reported_rookie_rows'][-1][1:3]==['Team','No (Dec 29, 2020)']

def build():
 prefix,cw,b,raw,pages=sources();o=ordinary_components(b);check_components(o,b)
 ms=miles_sources();mw=miles_window()
 assert mw['published_template_seasons']==[2017,2018,2019]and mw['waive_date']=='2020-01-12'and mw['waive_salary_cap_year']==2019
 assert mw['waive_in_September_to_June_window']is True and mw['post_current_remaining_seasons']==[]
 assert mw['current_components_protected_or_bonus_kept_in_2019_20']is True and mw['original_ordinary_or_stretched_2021_22_component']==0,'Current Salary incorrectly moved into future stretch years'
 assert mw['money_25000000_is_bonus_or_protection_upper']is False and mw['actual_private_current_payment_or_notice_certified']is False
 assert mw['later_new_resolution_or_new_UPC_reopens']is True
 applicable_events=[e for e in cw['relevant_public_events']if e.get('team')=='WAS'and e.get('player')in ['Anzejs Pasecniks','Jerome Robinson','Jordan Bell','Caleb Homesley']]
 assert any(e['player']=='Anzejs Pasecniks'and e['type']=='Waive'and e['date']=='2021-01-17'for e in applicable_events)
 assert any(e['player']=='Jerome Robinson'and e['type']=='Waive'and e['date']=='2021-04-08'for e in applicable_events)
 base=prefix['WAS']['closing_fixed_without_Din_or_residual'];reserved=o['Pasecniks']['candidate_full_2021_22_future_ordinary_reserve']
 revised=base+reserved;all_r=143002000-revised-8451384;some_r=143002000-revised-3000000
 assert (revised,all_r,some_r)==(127809326,6741290,12192674)
 broad=16371000
 rows=[]
 for r in [3000000,8451384]:
  total=revised+r+broad
  rows.append({'r':r,'remaining_public_legacy_overbound':broad,'conditional_screen_upper':total,'apron_margin':143002000-total,'upper_exceeds_apron_proves_actual_illegal':False})
 assert all(r['apron_margin']<0 for r in rows)
 return {'id':'WASHINGTON_2021_NAMED_RESIDUAL_COST_COMPONENTS','status':'INDEPENDENTLY_REVIEWED_NAMED_COMPONENTS_WHOLE_RESIDUAL_UNCLOSED','baseline_main':'8e7adfc66402def52e5409c7659f7fe53a8b2794','source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'repository BOM removed CRLF/CR to LF; external bytes unchanged','external_raw_attempts':raw,'collection_metadata_sha256':META_SHA,'CBA':{'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','raw_cache_path':str(CBA),'raw_sha256':CBA_SHA,'PDF1based_text_LF_sha256':pages},'named_ordinary_components':o,'Miles_primary_observations':ms,'Miles_published_contract_calendar_window':mw,'source_public_working_events':applicable_events,'residual_function':{'prefix_closing_fixed_with_Homesley_reserved_once':base,'additional_Pasecniks_reserve_not_in_PREFIX':reserved,'new_fixed_before_Din_and_other_residual':revised,'all_r_remaining_residual_sufficient_upper':all_r,'some_r_remaining_residual_sufficient_upper':some_r,'remaining_actual_residual':None,'public_source_upper_closed':False},'broad_prior_stretch_sensitivity':{'annual_15_percent_max_109140000':broad,'not_a_reported_WAS_stretch_debt':True,'requires_applicable_historical_stretch_epoch_and_all_former_player_portion_scope':True,'ordinary_endpoint_is_all_future_dead_zero':False,'screen_rows':rows},'remaining_categories':[{'id':'REPORTED_CURRENT_AND_PAST','named':'Homesley current reserved in PREFIX; Pasecniks future ordinary here; prior-year payment schedules are not automatically current-year Salary. Actual litigation/resolution year remains separate.'},{'id':'FA_HOLD_AND_RIGHTS','named':'Expired Ish/Lopez/Neto/Len holds require valid writtenrenunciation in P1; Trent live proposed Bird offer replaces hold. Bonga post-SubsequentDraft rights/RT and Winston/Mathews TW expiration/QO remain named inputs, not $0.'},{'id':'CAMP_AND_FORMER','named':'YoeliChilds/MarlonTaylor ordinary endpoints observed. JordanBell original WAS ten-day/camp contracts must be separated from later GSW/CHI contracts. CJMiles oldWAS contract and MartellWebster stretch family not recovered in these vendor tables; reported title success not complete history.'},{'id':'EXCEPTIONS','named':'P1 newlycreated TPE consumed before valid renunciation; all unused current exception holds require action. No arbitrary exception debt deletion.'},{'id':'DRAFT_AND_ROSTER','named':'Kispert12/Butler22 functions in PREFIX and 15STD candidate remain; BKN Todd43 does not belong to WAS, no redundant unsigned 1R charge after RSC. Unaccepted relevant RT fullcash and offseason incomplete rules must be accounted on own dates.'}],'facts_inferences_candidates':{'facts':['Vendor reports show original Pasecniks2021–22 future row and Robinson year4 option nonexercise, with source-tier boundary. Working S2 public dated waivers are preserved.'],'inferences':['Pasecniks full reported future salary can be reserved without claiming that its protected-zero column certifies current cash0. The remaining source-bound full residual upper is not established.'],'candidates':['No new salary/waiver/renunciation chosen here; only unselected P1 component function and conservative sufficient bounds are refined.']},'certification':{'independent_review_completed':True,'independent_review_basis':'g11 independently read14 actualraw/DOM contracts and CBA249–250, separated4 HTTP403 attempts from attributed web observations, recalculated Homesley once/Pasecniks1782621 and6741290/12192674 bounds. Same protected-zero/future-stretch constructor counterexamples rejected; whole residual remains unclosed.','conditional_named_component_only':True,'whole_WAS_cost_family_complete':False,'whole_P1_selected':False,'actual_private_financial_cents_or_receipt':False,'actual_rights_and_future_membership':False,'new_author_lock':False,'whole_macro3_complete':False,'REGISTER_changed':False,'manuscript_written':0}}

def validate(o):
 try:assert o==build(),'Saved component differs from current sources';return[]
 except(AssertionError,KeyError,ValueError,OSError)as e:return[str(e)]
def markdown(o):
 f=o['residual_function']
 return '\n'.join(['# Washington 2021: 남은 비용의 명명 성분','',o['status'],'','## 새로 회수한 실제 입력','',
 '새 vendor 원문14개를 보존하고 계약별 시즌 행을 읽었다. Pasecniks 원3년 계약에는2021–22 $1,782,621 행이 있다. 보호0을 실제 지급0으로 치환하지 않고 이 보고 가족의 fullfuture를 예약한다. 원Jan17 waiver는 S2 작업 source 이벤트로 연결했다. Homesley $1,517,981은 앞 패킷에 이미 들어 있어 두 번 추가하지 않는다.','',
 'Robinson은 원2018 계약의4년차 옵션 미행사(Dec29,2020)를 보존한다. 옵션을 행사한 것처럼 $5,340,914를 현재급여에 넣지 않는다. Ish/Lopez/Neto/Len 및 Mahinmi·Childs·Taylor의 명명 ordinary 끝점도 분리했다. 이 선수의 다른 팀 신계약은 WAS 비용이 아니다. 지급 일정과 Salary 귀속 연도, 뒤늦은 합의·판정·stretch는 서로 다르므로 ordinary끝점만 보고 모든future0을 인증하지 않는다.','',
 f'새 함수: {f["new_fixed_before_Din_and_other_residual"]:,}+r+X_remaining. 모든r∈[3m,8,451,384] 충분조건은 X_remaining≤{f["all_r_remaining_residual_sufficient_upper"]:,}, 일부r의 존재 충분조건은≤{f["some_r_remaining_residual_sufficient_upper"]:,}다. 이 문턱은 실제 X 상단의 증거가 아니다.','',
 '## Miles의 과거 계약 달력: 새로 닫은 범위','', 'NBA에 실린 AP 원보도의2017 3시즌 가족, Toronto의 공식multi-year체결, WAS2019취득, NBA2020Jan12 waiver를 새 web본문에서 읽었다. 직접 HTTP4회는403으로 원바이트만 보존했고 성공본문으로 계수하지 않았다. web attribution관측과 원HTML을 구분한다.', '', 'VII7(d)(6)(A)는 Sep–Jun waiver의 current SalaryCapYear를 그대로 두고 current 이후 남은 시즌만 stretch한다. 이2017–18/2018–19/2019–20 가족은 Jan2020 현재가마지막시즌이라 post-current가0개다. 원ordinary 또는그stretch가2021–22로 가는 성분은없다. 이는원계약가족의연도귀속이며 실제지급0·후대판정0·새계약0 인증이 아니다. 25m가보너스전체상단이라는 가정은필요없고 선택하지않았다. [AP2017 보도](https://www.nba.com/news/report-raptors-trade-cory-joseph-cj-miles-pacers) · [NBA2020 waiver](https://www.nba.com/news/wizards-waive-cj-miles-sign-anzejs-pasecniks)', '', '## 남은 범위와 차단 이유','',
 '적용 가능한 과거 마지막stretch연도 cap109.14m의15%라는 큰 감도16.371m를 별도로 넣으면 두 r 끝점 모두 apron을 넘는다. 이것은 비용 상단이 넓어 충분증명에 실패한다는 뜻이며 실제 불법의 반례가 아니다. 모든 과거stretch가0이라고 채우지도 않았다.','',
 '다음 유한 입력은 MartellWebster의 당시2011CBA 적용stretch 종료, Bell의 WAS 단기계약과 타팀 계약 구분, Bonga의2021후 권리와 Winston/Mathews 만료/QO, 새TPE 사용후 잔액 renunciation이다. 구SS 페이지의 제목은 존재하지만 Miles vendor는후대2021Boston계약만 제공하므로 새NBA/AP 원보도 가족으로분리했고, Webster는 계약행을 회수하지 못했다. 동일 URL 재시도 대신 이 정확한 공백을 유지했다. 이 패킷은 명명 futureordinary 성분 하나와 실제 충분조건을 진전시켰고 전체 잔여 상단은 미완이다.','',
 '원자료는 [SalarySwish Pasecniks](https://www.salaryswish.com/players/anzejs-pasecniks)·[Robinson](https://www.salaryswish.com/players/jerome-robinson)의2차 보고이며, 법규는 [2017 CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) VII4·7과 예외/권리 조항이다. 실제 계약 cents·장부·접수증을 인증하지 않는다.','',
 '[선행 후보](BKN_WAS_2021_PRE_JORDAN_NAMED_EXECUTION_FAMILY_2026_10_07.md) · [현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','',
 '|번호|묶음|상태|','|---|---|---|','|1|2020드래프트 연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23거래·계약|WAS Pasecniks명명 성분·잔여 충분조건 구성; 전체 상단 미완|','|4|장기커리어|후속시즌대기|','|5|결말·전체구조|전체 기능표 미완|','|6|집필규격·ContextPack|현행 등록기·Pack0|','|7|통합·독립·작가승인|최종 CLOSED|','','미완료 큰 묶음5 / v0.30 PARTIAL / 설계·원고 CLOSED / 원고0.',''])
def self_test():
 count=0
 fn=ordinary_components
 def hidden(b):
  o=fn(b);o['Pasecniks']['candidate_full_2021_22_future_ordinary_reserve']=0;return o
 with patch(__name__+'.ordinary_components',side_effect=hidden):
  try:build();raise RuntimeError('FALSE_PASS protected_zero_import')
  except AssertionError:count+=1
 mw=miles_window
 def wrong_phase():
  o=mw();o['original_ordinary_or_stretched_2021_22_component']=8333334;return o
 with patch(__name__+'.miles_window',side_effect=wrong_phase):
  try:build();raise RuntimeError('FALSE_PASS current_year_stretched_into_future')
  except AssertionError:count+=1
 return count

PINS={'research/BKN_WAS_2021_PRE_JORDAN_NAMED_EXECUTION_FAMILY_2026_10_07.json': 'a0e9ede786047a43abac4d21785b68ae55190e3d768096618ed010147906017b', 'research/CHA_WAS_FINITE_ROSTER_WORKING_FAMILY_2026_10_07.json': 'b06b071a0bf77bbff05d01d8adfa62472b4c3b90cca8aa2373ced9034712899a', 'tools/build_bkn_was_2021_pre_jordan_named_execution_family.py': '0ed5d61d86cb5cc4f2c8f8f8216f7cb5c01c7907ac0a574f3a2579d7e63c2d5e'}
META_SHA='3d0aa4c648b4b4e162b9d4dfe1ce46df3e359075c2c6aeaa3bf2506087ef615a'
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();o=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
 if a.check:assert not validate(load(OUT)) and txt(MD)==markdown(o)
 n=self_test()if a.self_test else None
 print(json.dumps({'current':True,'raw':14,'Pasecniks_fullfuture':1782621,'remaining_some_r_upper':12192674,'whole_residual':False,'self_controls':n}))
