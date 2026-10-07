"""Named original WAS legacy endpoints and legal cleanup functions; not a whole ledger."""
import argparse,copy,hashlib,itertools,json,re
from pathlib import Path
from fractions import Fraction
from unittest.mock import patch
from bs4 import BeautifulSoup
import fitz
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_washington_2021_legacy_cleanup_cost_family.py'
OUT='research/WASHINGTON_2021_LEGACY_CLEANUP_COST_FAMILY_2026_10_07.json'
MD=OUT[:-5]+'.md'
PRIOR='research/WASHINGTON_2021_REMAINING_INVENTORY_FAMILY_2026_10_07.json'
NAMED='research/WASHINGTON_2021_NAMED_RESIDUAL_COST_COMPONENTS_2026_10_07.json'
PREFIX='research/BKN_WAS_2021_PRE_JORDAN_NAMED_EXECUTION_FAMILY_2026_10_07.json'
FOLDER=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-was-legacy-cleanup-20261007')
CBA17=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA11=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-was-rights-tw-20261007/2011_CBA.pdf')
VENDOR_MEANING_SHA='a397c77ce04a012028e5778a2f29b20c074dcc8bc347ffbe86166da6d398a3eb'
RAW_META={'sources.json':'377fff59219b5aa3effdec582ee1b5bd831aa7535e1ba45b8d15f93b7831d16d','additional_sources.json':'c3bbdaff27eff3be51f7b70fa7741343f7b775478a648339cad2810457dee80d','tarik_source.json':'14af4bcaa66006506088e167bfc6f00d9e9932cb86437a027439285010cbef41','observations.json':'6b1dcaade250a2bff9c2eab75d28531e1fcbc8a766847e051d4bf5a5356bed83'}
def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def rawsha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ceil(x):return -(-x.numerator//x.denominator)
def compact(p):return BeautifulSoup(Path(p).read_bytes(),'html.parser').get_text(' ',strip=True)
def contracts(p):
 rows=[]
 for table in BeautifulSoup(Path(p).read_bytes(),'html.parser').find_all('table'):
  meta=table.parent.get_text(' ',strip=True)
  if not meta.startswith('Length :'):continue
  team=re.search(r'Signing Team : (\w+)',meta);dt=re.search(r'Signing Date : (.+?) Source :',meta)
  if not team or not dt:continue
  r=[[x.get_text(' ',strip=True)for x in tr.find_all('td')]for tr in table.find_all('tr')]
  rows.append({'team':team.group(1),'signing_date_reported':dt.group(1),'rows':[x for x in r if len(x)==8 and x[0][:4].isdigit()]})
 return rows
def source_inputs():
 for p,h in PINS.items():assert sha(p)==h,'Repository source changed: '+p
 s={p:load(p)for p in [PRIOR,NAMED,PREFIX]}
 for p,v in s.items():assert v==json.loads(text(p)),'Source loader changed content'
 assert s[PRIOR]['certification']['independent_review_completed']is True
 assert s[PRIOR]['summary']['dated_rows']==24 and len(s[PRIOR]['dated_joint_rows'])==24
 assert s[NAMED]['residual_function']['new_fixed_before_Din_and_other_residual']==127809326
 assert s[PREFIX]['WAS']['closing_fixed_without_Din_or_residual']==126026705
 meta={}
 for name,h in RAW_META.items():
  assert rawsha(FOLDER/name)==h,'External source metadata changed';meta[name]=json.loads((FOLDER/name).read_bytes())
 attempts=meta['sources.json']+meta['additional_sources.json']+[meta['tarik_source.json']]
 for r in attempts:
  if 'cache_path'in r:assert rawsha(r['cache_path'])==r['raw_sha256'],'External raw changed'
 assert len(attempts)==20
 for slug in ['gary-payton-ii','jarell-eddie','daniel-ochefu']:assert 'player not found'in compact(FOLDER/(slug+'.html')).lower()
 for slug in ['jemerrio-jones','tarik-phillip','jonathon-simmons']:assert not [c for c in contracts(FOLDER/(slug+'.html'))if c['team']=='WAS'],'Expected missing vendor historical row changed'
 assert 'through 2020 with Washington'in compact(FOLDER/'sham_tarik.html')
 assert 'through 2017 with Washington'in compact(FOLDER/'sham_eddie.html')
 assert '$5.7 million'in compact(FOLDER/'simmons_original_report.html')
 assert '$1,416,852'in compact(FOLDER/'tarik_last_salary.html')
 assert rawsha(CBA17)=='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
 assert rawsha(CBA11)=='239e7b41fad3637fef1dde926ec1cd3df4e86c41f798ec515d1ffb3246d61fbb'
 docs=[]
 for tag,p,pages in [('2017',CBA17,[202,203,204,205,206,207,212,213,240,241,249,250]),('2011',CBA11,[191,192])]:
  with fitz.open(p)as doc:t={str(i):doc[i-1].get_text().replace('\r\n','\n').replace('\r','\n')for i in pages}
  joined=' '.join(' '.join(t.values()).split())
  assert 'twice the number of Seasons'in joined and 'September 1 through the following June 30'in joined
  if tag=='2017':
   for phrase in ['rights to use an Exception','Qualifying Veteran Free Agent','renounce','grievance','then-current']:assert phrase in joined
  docs.append({'agreement':tag,'raw_cache_path':str(p),'raw_sha256':rawsha(p),'PDF1based_text_LF_sha256':{i:hashlib.sha256(v.encode()).hexdigest()for i,v in t.items()},'extraction':'PyMuPDF get_text; CRLF/CR to LF, UTF8 SHA'})
 return s,meta,attempts,docs
def vendor_inventory():
 return {slug:[g for g in contracts(FOLDER/(slug+'.html'))if g['team']=='WAS']for slug in ['justin-robinson','gary-paytonii','johnathan-williams','phil-booth','justin-anderson','chasson-randle','danuel-house-jr','sheldon-mac']}
def maximum_original_stretch_end(start,seasons):
 # Any July-August waiver during this finite original term: N remaining years => 2N+1.
 ends=[y+2*(start+seasons-y)for y in range(start,start+seasons)]
 # September-June: current unchanged, only N later years => 2N+1 starting next year.
 ends += [y+1+2*(start+seasons-y-1)for y in range(start,start+seasons)if start+seasons-y-1>0]
 return f'{max(ends)+1}-06-30'
def inventory(v,observed):
 rows=[]
 for slug in ['gary-paytonii','johnathan-williams','phil-booth','justin-anderson']:
  assert all(len(g['rows'])==1 and g['rows'][0][0][:4]=='2019'for g in v[slug])
  # Their observed December/January or October waiver timing preserves only current 2019.
  rows.append({'player':{'gary-paytonii':'Gary Payton II','johnathan-williams':'Johnathan Williams','phil-booth':'Phil Booth','justin-anderson':'Justin Anderson'}[slug],'original_ordinary_last_cap_year':2019,'original_contract_rows':v[slug],'current_family_component':0,'reason':'Original one-season 2019 term: source October/December/January dates; no later original cap year to stretch.'})
 for slug,start,n in [('chasson-randle',2018,1),('danuel-house-jr',2016,2),('sheldon-mac',2016,2)]:
  end=maximum_original_stretch_end(start,n);assert end<='2021-06-30'
  rows.append({'player':{'chasson-randle':'Chasson Randle','danuel-house-jr':'Danuel House Jr.','sheldon-mac':'Sheldon Mac'}[slug],'original_contract_rows':v[slug],'maximum_original_cap_stretch_end':end,'current_family_component':0,'reason':'Original finite term plus even earliest July full-term stretch ends before FY2021–22; cash timing is not cap attribution.'})
 rows += [
 {'player':'Jarell Eddie','reported_term_start':2015,'reported_seasons':2,'term_source':'sham_eddie.html','maximum_original_cap_stretch_end':maximum_original_stretch_end(2015,2),'current_family_component':0,'waive_day_certified':False},
 {'player':'Daniel Ochefu','reported_term_start':2016,'reported_seasons':3,'term_source':'OCHEFU_TERM collegiate conference own interview','waive_date':'2017-10-09','current_cap_year':2017,'post_current_seasons':[2018],'original_stretch_years':[2018,2019,2020],'maximum_original_cap_stretch_end':'2021-06-30','current_family_component':0},
 {'player':'Jemerrio Jones','reported_term_start':2018,'reported_seasons':2,'term_source':'JONES_TERM secondary reported template','waive_date':'2019-10-16','current_cap_year':2019,'post_current_seasons':[],'current_family_component':0,'source_vendor_missing_history_is_zero_proof':False}]
 assert len(rows)==10 and all(r['current_family_component']==0 for r in rows)
 return rows
def cost_profiles(v):
 j=v['justin-robinson'][0]['rows'];j20=int(j[1][3].replace('$','').replace(',',''));j21=int(j[2][3].replace('$','').replace(',',''))
 return {'JR_ORDINARY_FULL_REPORTED':j21,'JR_STRETCH_FULL_REPORTED':ceil(Fraction(j20+j21,5)),'SIMMONS_ORIGINAL_ORDINARY_ENDED':0,'SIMMONS_ORIGINAL_STRETCH_REPORTED_BASE':ceil(Fraction(5700000,3)),'PHILLIP_ORIGINAL_ORDINARY_ENDED':0,'PHILLIP_ORIGINAL_STRETCH_REPORTED_BASE':ceil(Fraction(1416852,3))}
def cleanup_policy():
 return {'kind':'UNSELECTED_ROUTINE_VALID_CLEANUP_CANDIDATE','expired_FA_names':['Ish Smith','Robin Lopez','Raul Neto','Alex Len','Ian Mahinmi','Jordan McRae','Isaiah Thomas','Shabazz Napier','Gary Payton II','Johnathan Williams','Chasson Randle','Trevor Ariza','Jeff Green','Bobby Portis','Jabari Parker','Sam Dekker','Devin Robinson'], 'action':'NBA-valid written renunciation of any still-present expired FA amount at comparison time','only_if_no_effective_QO_or_first_refusal_notice':True,'Mathews_Winston_open_QO_excluded':True,'Bonga_open_RT_excluded':True,'retained_live_15_STD_excluded':True,'expired_FA_actual_hold_presence_or_renunciation_certified':False,'unused_exceptions_action':'Use P1 created TPE for the admitted Dinwiddie assignment first; validly renounce any remaining current non-minimum exception amount afterwards. Reopen if a later permitted transaction creates a new exception.','exception_hold_normal_zero_only_after_valid_renunciation':True,'exception_hold_apron_excluded_under_VII6m3F_independent_of_normal':True,'old_guaranteed_salary_debt_erased_by_renunciation':False,'unsigned_Kispert_Butler_or_Bonga_RT_deleted':False,'new_STD_or_TW_signed':0,'incomplete_charge_15STD_candidate':0,'actual_cleanup_selected_or_receipt_certified':False}
FIXED_POLICY=copy.deepcopy(cleanup_policy())
def build():
 s,meta,attempts,docs=source_inputs();v=vendor_inventory();actual_v={slug:[g for g in contracts(FOLDER/(slug+'.html'))if g['team']=='WAS']for slug in v}
 assert v==actual_v,'Returned vendor contract identity/rows changed'
 assert hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==VENDOR_MEANING_SHA,'Published WAS per-player contract meaning changed'
 assert len(v['justin-robinson'])==1 and [r[0]for r in v['justin-robinson'][0]['rows']]==['2019-20 W','2020-21 W','2021-22 W']
 assert v['justin-robinson'][0]['rows'][2][3]=='$1,782,621'and v['justin-robinson'][0]['rows'][2][5]=='$0'
 assert meta['observations.json'][0]['waive_date']=='2020-01-05'
 assert meta['observations.json'][2]['waive_date']=='2019-10-16'
 assert meta['observations.json'][3]['start_cap_year']==2016 and meta['observations.json'][3]['seasons']==3
 assert meta['observations.json'][4]['waive_date']=='2017-10-09'
 assert meta['observations.json'][5]['start_cap_year']==2018 and meta['observations.json'][5]['seasons']==2
 assert meta['observations.json'][6]['start_cap_year']==2017 and meta['observations.json'][6]['seasons']==3
 ended=inventory(v,meta['observations.json']);assert len(ended)==10
 known={'Gary Payton II':'gary-paytonii','Johnathan Williams':'johnathan-williams','Phil Booth':'phil-booth','Justin Anderson':'justin-anderson','Chasson Randle':'chasson-randle','Danuel House Jr.':'danuel-house-jr','Sheldon Mac':'sheldon-mac'}
 assert {r['player']for r in ended}==set(known)|{'Jarell Eddie','Daniel Ochefu','Jemerrio Jones'},'Returned ended inventory identity changed'
 for r in ended:
  if r['player']in known:assert r['original_contract_rows']==v[known[r['player']]],'Ended inventory no longer carries source contract rows'
  if r['player']in ['Chasson Randle','Danuel House Jr.','Sheldon Mac','Jarell Eddie']:
   expected_end={'Chasson Randle':'2021-06-30','Danuel House Jr.':'2021-06-30','Sheldon Mac':'2021-06-30','Jarell Eddie':'2020-06-30'}
   assert r['maximum_original_cap_stretch_end']==expected_end[r['player']],'Original maximum stretch boundary changed'
  if r['player']=='Daniel Ochefu':assert (r['reported_term_start'],r['reported_seasons'],r['post_current_seasons'],r['original_stretch_years'],r['maximum_original_cap_stretch_end'])==(2016,3,[2018],[2018,2019,2020],'2021-06-30'),'Ochefu source/calendar boundary changed'
  if r['player']=='Jemerrio Jones':assert (r['reported_term_start'],r['reported_seasons'],r['post_current_seasons'])==(2018,2,[]),'Jones source/calendar boundary changed'
 # This result-only function is checked against independent calendar bounds at consumption.
 for r in ended:
  if 'waive_date'in r:assert r['waive_date']=={'Daniel Ochefu':'2017-10-09','Jemerrio Jones':'2019-10-16'}[r['player']]
  assert r['current_family_component']==0
 cp=cost_profiles(v);assert cp=={'JR_ORDINARY_FULL_REPORTED':1782621,'JR_STRETCH_FULL_REPORTED':660121,'SIMMONS_ORIGINAL_ORDINARY_ENDED':0,'SIMMONS_ORIGINAL_STRETCH_REPORTED_BASE':1900000,'PHILLIP_ORIGINAL_ORDINARY_ENDED':0,'PHILLIP_ORIGINAL_STRETCH_REPORTED_BASE':472284},'Reported salary/stretch component changed'
 clean=cleanup_policy();assert clean==FIXED_POLICY,'Cleanup policy changed'
 assert set(clean['expired_FA_names']).isdisjoint(s[PREFIX]['WAS']['modeled_final_standard']),'Cleanup would renounce retained live contract family'
 old=s[PRIOR]['dated_joint_rows'];rows=[]
 for oldrow,j,sm,tp in itertools.product(old,['JR_ORDINARY_FULL_REPORTED','JR_STRETCH_FULL_REPORTED'],['SIMMONS_ORIGINAL_ORDINARY_ENDED','SIMMONS_ORIGINAL_STRETCH_REPORTED_BASE'],['PHILLIP_ORIGINAL_ORDINARY_ENDED','PHILLIP_ORIGINAL_STRETCH_REPORTED_BASE']):
  parts={k:cp[k]for k in [j,sm,tp]};cost=sum(parts.values());allcost=oldrow['named_apron_upper']+cost
  rows.append({'date':oldrow['date'],'QO_RT_branches':oldrow['branches'],'legacy_branches':[j,sm,tp],'reported_legacy_components':parts,'legacy_reported_point_upper':cost,'named_total_reported_point_upper':allcost,'normal_reported_point_upper_after_valid_cleanup':127809326+allcost,'apron_reported_point_upper_before_Din':127809326+allcost,'Din_r_upper_for_reported_point':143002000-127809326-allcost,'extra_family_charge_E_actual':None,'all_r_sufficient_E_upper':143002000-127809326-allcost-8451384,'some_r_sufficient_E_upper':143002000-127809326-allcost-3000000,'actual_full_ledger_or_private_salary_certified':False})
 assert len(rows)==192 and max(r['legacy_reported_point_upper']for r in rows)==4154905 and max(r['named_total_reported_point_upper']for r in rows)==7994905
 assert len({(r['date'],*r['QO_RT_branches'],*r['legacy_branches'])for r in rows})==192
 return {'id':'WASHINGTON_2021_LEGACY_CLEANUP_COST_FAMILY','status':'INDEPENDENTLY_REVIEWED_REPORTED_ORIGINAL_FAMILY_UNSELECTED_CLEANUP','baseline_main':'1b7d7b980506fc3e3dffefd468eb7098e4a3bd3c','source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'Repository BOM stripped CRLF/CR to LF; external caches raw unchanged','new_source_attempts':attempts,'raw_metadata':{n:{'cache_path':str(FOLDER/n),'raw_sha256':h}for n,h in RAW_META.items()},'attributed_web_observations':meta['observations.json'],'new_vendor_placeholder_bodies_not_evidence':['gary-payton-ii','jarell-eddie','daniel-ochefu'],'vendor_correct_title_without_historical_WAS_tables_not_zero_evidence':['jemerrio-jones','tarik-phillip','jonathon-simmons'],'source_rules':docs,'original_family_zero_endpoints':ended,'original_nonzero_family_inputs':{'Justin_Robinson':{'reported_three_season_rows':v['justin-robinson'],'waive_date':'2020-01-05','then_current_2019_20_salary_not_deleted':True,'remaining_years':[2020,2021],'stretch_years':[2020,2021,2022,2023,2024],'full_reported_remaining_sum':3300602,'reported_ordinary_2021_upper':1782621,'reported_stretch_2021_ceiling':660121,'protected_column_zero_is_full_salary_zero':False,'actual_election_or_post_waiver_protection':None},'Jonathon_Simmons':{'term_start':2017,'term_seasons':3,'ordinary_last_year':2019,'source_reported_final_base_salary':5700000,'current_reported_ordinary_component':0,'possible_current_stretch_years':[2019,2020,2021],'source_reported_stretch_base_ceiling':1900000,'exact_waive_date_or_stretch_election':None,'actual_extra_salary_bonus_award':None,'reported_total_18m_vs_20m_not_used_as_whole_upper':True},'Tarik_Phillip':{'reported_original_term':[2018,2019],'reported_2019_full_salary':1416852,'source_reported_waive_date':'2019-08-15','July_August_remaining_one_year_means_three_cap_years':[2019,2020,2021],'reported_stretch_base_ceiling':472284,'protected_zero_is_current_stretch_zero':False,'actual_bonus_protection_or_stretch_election':None}},'reported_component_profiles':cp,'published_vendor_per_player_contract_projection_sha256':VENDOR_MEANING_SHA,'routine_cleanup_candidate':clean,'dated_comparison_rows':rows,'cost_function':{'base_already_includes_Homesley_and_Pasecniks':127809326,'same_prior_24_QO_RT_cases_preserved':True,'named_reported_max':7994905,'full_apron_function':'127809326 + r + named_reported_components + E','E':'Nonnegative extra charge: named unreported salary components after applicable attribution, any other sourced legacy current component, later resolution/amendment, reopened draft/tender or signed-event costs. Not actual private-zero.','actual_E_upper':None,'whole_WAS_X_upper_closed':False,'worst_reported_point_r_ceiling':7197769,'worst_reported_point_all_r_E_upper':-1253615,'worst_reported_point_some_r_E_upper':4197769,'negative_all_r_screen_is_actual_illegality':False},'summary':{'new_named_actor_count':13,'original_ended_families':10,'nonzero_possible_current_families':3,'prior_QO_RT_rows':24,'new_comparison_rows':192,'reported_point_legacy_max':4154905,'reported_point_total_max':7994905,'new_signed_STD_or_TW':0,'minutes_or_results_changed':False},'scope':{'named_13_original_inventory_closed_under_reported_terms_and_calendar':True,'historical_all_WAS_contract_census_certified':False,'reported_salary_points_are_all_private_contract_components':False,'cleanup_and_stretch_branches_selected':False,'whole_WAS_cost_or_P1_direction_selected':False,'concrete_remaining_inputs':['An E upper for the selected public implementation family, including any newly sourced current legacy components; this packet only closes its 13 named original families.','Valid cleanup branch and Mathews/Winston/Bonga QO/RT case selection, without restoring erased debts or adding a signed slot.','P1 important direction and preserved 2023/2024 rights complement are separate; source-backed positive named alternatives are not actual acceptance.']},'certification':{'independent_review_completed':True,'independent_review_basis':'g11 read cached 2011/2017 CBA rules and raw/source distinctions, independently recalculated all192 rows and rejected the same real Booth-to-Anderson and Anderson-to-Booth parser-result swap after the fixed per-player raw meaning guard repair. Maximum reported point is not actual E upper or complete WAS ledger; author self-tests not counted as independent checks.','actual_private_receipt_or_contract_cents':False,'new_author_lock':False,'whole_macro3_complete':False,'REGISTER_changed':False,'manuscript_written':0}}
def validate(o):
 try:assert o==build(),'Saved leaf differs from source-bound construction';return[]
 except(AssertionError,KeyError,ValueError,OSError)as e:return[str(e)]
def markdown(o):
 return '\n'.join(['# WAS 2021 과거 계약·정리행동 비용 가족','',o['status'],'','## 사실 / 추론 / 후보 / 작가확정','',
 '원 13명 가족을 회수했다. SalarySwish raw는 보도된 계약표 입력이며 실제 UPC cents 인증이 아니다. 20 새 다운로드 시도 중 HTTP200의 Player Not Found 3개와 올바른 제목만 있고 과거 WAS 계약표가 없는 3개는 그 계약의 증거로 쓰지 않는다. Ochefu의 3년은 Big East 자체 인터뷰 관측, waiver는 당시 기자의 원보도다. Jones의 2년은 명시한 2차 보고 템플릿이다. 제공자 raw와 web 귀속 관측 8개를 구분한다. CBA 원문은 실제 cached PDF를 직접 읽고 해당 쪽 지문으로 묶었다.','',
 '## 자동0이 아닌 세 명','',
 'Justin Robinson: 2019 세 시즌 표에는2021–22 전체1,782,621/보호0이 있다. Jan5,2020 waiver에서 current2019–20은 유지되고 남은2020/2021 두 해를 cap stretch하면5년2020..2024다. 전액 잔여3,300,602/5의 ceiling660,121와 ordinary1,782,621을 모두 남긴다. 실제 보호·stretch 선택은 null이다.','',
 'Simmons: 원2017 세 시즌의 마지막 ordinary는2019–20이지만 그 마지막해를 적법하게 stretch하면2019/2020/2021까지 갈 수 있다. Kyle Neubeck의 직접 취재 원보도에서5.7m을 읽었다. 보고 기본급 비교점은1.9m이며 원 total18m/20m 불일치를 완전 상단으로 쓰지 않는다. 미보고 성분·실제 stretch·양도 비용 전체 인증은 없다.','',
 'Phillip: 원2018–19 잔여+2019–20 계약과 Aug15,2019 waiver라는 보고 가족이다. July–August 한 잔여해는3년2019/2020/2021이므로 보호0이나 ordinary 만료만으로2021–22를0으로 만들 수 없다. 보고 최소 기본급1,416,852의 비교점은472,284다. 보장·bonus·실제 선택은 null이다.','',
 '## 끝난 원계약과 정리 함수','',
 'PaytonII·Williams·Booth·Anderson은 각 보고된 원2019 한 시즌의 October/December/January 사건이라 원 ordinary 또는 그 current 이후 cap stretch가 없다. Randle2018 한 시즌, House/Mac2016 두 시즌, Eddie2015 두 시즌은 가능한 가장 이른 전체기간 stretch조차2021–22 전에 끝난다. Ochefu는 Oct2017 current를 남기고2018 한 해만3년2018..2020으로 늘려도 Jun30,2021 끝이다. Jones는 Oct2019 current가 원2년의 마지막이라 후속해가 없다. 이10개 종료는 oldcash나 새로운 판정·추가계약의 부재 인증이 아니다.','',
 '정리 후보는 살아 있는 QO/First Refusal notice 없는 expired FA의 NBA-valid 서면 renunciation이다. Mathews/Winston open QO 및 Bonga RT는24 분기로 따로 보존하고 live15STD/unsignedRSC를 지우지 않는다. P1의 새 TPE는 Dinwiddie 양도에 먼저 사용한 뒤 남은 unused exception을 적법하게 renounce한다. 정상 비용의0은 이 행동을 조건으로 하며 apron의 FA/exception 제외는 VII6(m)(3) 별도 규칙이다. 정리·서명·중요P1·stretch는 미선택이고 새 STD/TW0이다.','',
 '## 실제 192행과 한계','',
 '앞24 QO/RT 날짜행×세 ordinary/stretch2가지=192다. 새 원계약 보고 성분 최대4,154,905, 앞 QO/RT 포함 최대7,994,905다. base127,809,326에는 Homesley/Pasecniks가 한 번씩 이미 있으므로 중복0이다. 최대 보고점에서 r의 ceiling7,197,769, 모든r에 대한 다른E 문턱−1,253,615/일부r 존재 문턱4,197,769이다. −문턱은 보수 screen의 실패이며 실제 불법 증명이 아니다.','',
 '`apron = 127809326 + r + named_reported_components + E`. E는 미보고 성분의 해당연도 귀속, 추가로 회수될 명명 계약/새 판정/다시 열린 tender 비용이고 실제 상단은 null이다. 따라서 보고 비교점이나13명 목록 종료를 전체 WAS X·전체 원계약 census·실제 사적0으로 승격하지 않는다. 다음 유한 입력은 선택 가족의 E 상단과 routine 정리/QO/RT 분기다. 비공개 모든 영수증 부재를 새 gate로 요구하지 않는다.','',
 '[Simmons 원취재](https://www.phillyvoice.com/nba-draft-2019-what-are-sixers-accomplishing-or-signaling-jonathon-simmons-trade/) · [Phillip 보고 표](https://www.shamsports.com/players/tarik-phillip) · [Eddie 보고 표](https://www.shamsports.com/players/jarell-eddie) · [Ochefu 자체 인터뷰](https://www.bigeast.com/news/2016/8/2/MBB_0802164754.aspx) · [2017 CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) · [앞24행](WASHINGTON_2021_REMAINING_INVENTORY_FAMILY_2026_10_07.md) · [현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','',
 '|번호|묶음|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23거래·계약|WAS13명 원계약/192 비교행; E/P1 미완|','|4|장기커리어|후속시즌 대기|','|5|결말·전체구조|전체 기능표 미완|','|6|집필규격·ContextPack|현행 등록기·Pack0|','|7|통합·독립·작가승인|최종 CLOSED|','','미완료 큰 묶음5 / v0.30 PARTIAL / 설계·원고 CLOSED / 원고0.',''])
def self_test():
 n=0
 fn=cost_profiles
 def delete_future(v):
  d=fn(v);d['JR_ORDINARY_FULL_REPORTED']=0;return d
 with patch(__name__+'.cost_profiles',side_effect=delete_future):
  try:build();raise RuntimeError('FALSE_PASS protected_zero_deleted_full_future')
  except AssertionError:n+=1
 fn2=cleanup_policy
 def erase_QO():
  d=fn2();d['Mathews_Winston_open_QO_excluded']=False;return d
 with patch(__name__+'.cleanup_policy',side_effect=erase_QO):
  try:build();raise RuntimeError('FALSE_PASS open_QO_renounced')
  except AssertionError:n+=1
 fn3=vendor_inventory
 def wrong_team():
  d=fn3();d['justin-robinson'][0]['team']='GSW';return d
 with patch(__name__+'.vendor_inventory',side_effect=wrong_team):
  try:build();raise RuntimeError('FALSE_PASS vendor_actor_return')
  except AssertionError:n+=1
 fn4=contracts
 def swap_raw_actor(p):
  p=Path(p)
  if p.name=='phil-booth.html':p=p.with_name('justin-anderson.html')
  elif p.name=='justin-anderson.html':p=p.with_name('phil-booth.html')
  return fn4(p)
 with patch(__name__+'.contracts',side_effect=swap_raw_actor):
  try:build();raise RuntimeError('FALSE_PASS same_parser_Booth_Anderson_swap')
  except AssertionError:n+=1
 return n
PINS={'research/WASHINGTON_2021_REMAINING_INVENTORY_FAMILY_2026_10_07.json': 'aff173a27d8338382699ef2981d1e376945e1dd60a98beb6b8453f3a175898ce', 'tools/build_washington_2021_remaining_inventory_family.py': '98daa5f7c48380942866987915daa5970746fc0f9740d7cb152227379be3d80e', 'research/WASHINGTON_2021_NAMED_RESIDUAL_COST_COMPONENTS_2026_10_07.json': '1235a3dfef34898b9f43edaee3a9fd45b18edbee1e107a5b7b21fdc5af783498', 'research/BKN_WAS_2021_PRE_JORDAN_NAMED_EXECUTION_FAMILY_2026_10_07.json': 'a0e9ede786047a43abac4d21785b68ae55190e3d768096618ed010147906017b'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();o=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
 if a.check:assert not validate(load(OUT))and text(MD)==markdown(o)
 count=self_test()if a.self_test else None
 print(json.dumps({'current':True,'named':13,'rows':192,'reported_point_max':7994905,'whole_WAS':False,'self_controls':count}))
