"""Named WAS endpoints and bounded post-draft tender/QO families, not whole cost."""
import argparse,copy,hashlib,itertools,json,re
from pathlib import Path
from datetime import date
from unittest.mock import patch
from bs4 import BeautifulSoup
import fitz
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_washington_2021_remaining_inventory_family.py'
OUT='research/WASHINGTON_2021_REMAINING_INVENTORY_FAMILY_2026_10_07.json'
MD=OUT[:-5]+'.md'
NAMED='research/WASHINGTON_2021_NAMED_RESIDUAL_COST_COMPONENTS_2026_10_07.json'
CW='research/CHA_WAS_FINITE_ROSTER_WORKING_FAMILY_2026_10_07.json'
BOARD='research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json'
PREFIX='research/BKN_WAS_2021_PRE_JORDAN_NAMED_EXECUTION_FAMILY_2026_10_07.json'
FOLDER=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-was-rights-tw-20261007')
CBA17=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
BELL=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-was-residual-20261007/jordan-bell.html')
CBA17_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
META_SHA='728899410a4af1b5cf499d67945a2fb9e425e0738b36398cdb7779a3c42ea4af'
OBS_SHA='53473fb02a51ed88c5d0da012fe3f83f8753163b8242a02c1ee1028c4b763005'
BELL_SHA='f13e9c98b4048b14af6df49b85ffe50d1cd9b5c79f6d39f66ae72304ec0f9108'
def txt(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(txt(p).encode()).hexdigest()
def load(p):return json.loads(txt(p))
def rawsha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def contracts(path):
 out=[]
 for table in BeautifulSoup(Path(path).read_bytes(),'html.parser').find_all('table'):
  metadata=table.parent.get_text(' ',strip=True)
  if not metadata.startswith('Length :'):continue
  team=re.search(r'Signing Team : (\w+)',metadata)
  dt=re.search(r'Signing Date : (.+?) Source :',metadata)
  if not team or not dt:continue
  rows=[]
  for tr in table.find_all('tr'):
   row=[td.get_text(' ',strip=True)for td in tr.find_all('td')]
   if len(row)==8 and row[0][:4].isdigit():rows.append(row)
  out.append({'team':team.group(1),'signing_date_reported':dt.group(1),'rows':rows})
 return out

def sources():
 for p,h in PINS.items():assert sha(p)==h,'Repository source changed: '+p
 src={p:load(p)for p in [NAMED,CW,BOARD,PREFIX]}
 for p,o in src.items():assert o==json.loads(txt(p)),'Source reader changed content'
 assert src[NAMED]['certification']['independent_review_completed']is True
 assert src[NAMED]['residual_function']['new_fixed_before_Din_and_other_residual']==127809326
 assert src[NAMED]['residual_function']['remaining_actual_residual']is None
 assert src[PREFIX]['WAS']['closing_fixed_without_Din_or_residual']==126026705
 b=src[CW]['selection']['WAS_BONGA']['finite_rights_execution']
 assert (b['initial_team'],b['initial_pick'],b['rights_scope_end'])==('WAS',44,'2021-05-18')
 assert b['naturally_eligible_draft_is_Subsequent_Draft_year']==2021
 assert b['after_2021_Subsequent_Draft_status_selected']is None
 assert not any(b['X5_branch_if_agreement_is_professional'][k]for k in ['effective_immediate_availability_notice_before_scope_end','availability_and_intention_notice_for_following_NBA_season_before_scope_end','July1_September1_available_notice_under_X5b_before_scope_end','additional_nonNBA_signing_or_renewal_selected'])
 assert len(src[BOARD]['rows'])==60 and not any(r['player']=='Isaac Bonga'for r in src[BOARD]['rows'])
 assert rawsha(FOLDER/'sources.json')==META_SHA and rawsha(FOLDER/'observations.json')==OBS_SHA
 raw=json.loads((FOLDER/'sources.json').read_bytes());obs=json.loads((FOLDER/'observations.json').read_bytes())
 assert len(raw)==8 and len(obs)==4
 for r in raw:
  if 'error'in r:assert r['error']=='ReadTimeout';continue
  assert rawsha(r['cache_path'])==r['raw_sha256']
 assert [r.get('status')for r in raw]==[200,200,200,200,None,None,403,403]
 assert obs[0]['four_season_family_start']==2013 and obs[0]['seasons']==4
 assert obs[1]['waive_date']=='2015-11-30'and obs[1]['reported_contract_seasons']==4
 assert obs[2]['WAS_Winston_two_way_signing']is True
 assert obs[3]['names_with_original_WAS_qualifying_offers']==['Garrison Mathews','Cassius Winston']
 assert all(not o['source_full_body_raw_recovered']for o in obs)
 assert '2011-NBA-NBPA-Collective-Bargaining-Agreement.pdf'in (FOLDER/'NBPA_CBA_INDEX.html').read_text(encoding='utf8')
 assert rawsha(CBA17)==CBA17_SHA and rawsha(BELL)==BELL_SHA
 pages={};docs=[]
 for name,p,indices in [('2011',FOLDER/'2011_CBA.pdf',[47,48,49,191,192]),('2017',CBA17,[74,75,207,208,209,212,213,240,241,302,303,304,305,306,307,312,313,317,318])]:
  with fitz.open(p)as d:
   extracted={str(i):d[i-1].get_text().replace('\r\n','\n').replace('\r','\n')for i in indices}
   pages[name]={i:hashlib.sha256(t.encode()).hexdigest()for i,t in extracted.items()}
   compact=' '.join(' '.join(extracted.values()).split())
   if name=='2011':assert 'twice the number of Seasons'in compact and 'not including the then-current Season'in compact and 'September 1 through the following June 30'in compact
   else:
    for phrase in ['second of two (2)','Standard NBA Contract','Two-Way Qualifying Offer','zero (0) Years of Service','only if the player agrees in writing','September 10']:
     assert phrase in compact,'CBA rule source missing: '+phrase
   docs.append({'agreement':name,'raw_cache_path':str(p),'raw_sha256':rawsha(p),'page_text_method':'PyMuPDF get_text, CRLF/CR normalized LF; SHA UTF8','PDF1based_text_LF_sha256':pages[name]})
 return src,raw,obs,docs

def webster_window():
 return {'source_family_start':2013,'original_seasons':[2013,2014,2015,2016],'waiver_date':'2015-11-30','applicable_CBA':'2011 VII7(d)(5)(A)','current_cap_year':2015,'current_not_stretched_into_future':True,'post_current_seasons':[2016],'twice_remaining_plus_one':3,'longest_cap_stretch_years':[2016,2017,2018],'latest_original_cap_stretch_end':'2019-06-30','original_ordinary_or_cap_stretch_2021_22_component':0,'actual_cap_stretch_election':None,'exact_protected_salary_or_bonus':None,'cash_payment_schedule_is_cap_year_attribution':False,'later_new_resolution_or_amendment_reopens':True}

def bell_inventory():
 allrows=contracts(BELL)
 chosen=[]
 for dt,team,first in [('December 18, 2020','WAS','2020-21 W'),('January 23, 2021','WAS','2020-21'),('April 14, 2021','WAS','2020-21'),('May 13, 2021','GSW','2020-21'),('September 25, 2021','GSW','2021-22 W'),('December 30, 2021','CHI','2021-22')]:
  found=[g for g in allrows if g['team']==team and g['signing_date_reported']==dt and len(g['rows'])==1 and g['rows'][0][0]==first]
  assert len(found)==1,'Bell named team/date/season missing';chosen.append(found[0])
 return {'reported_named_contracts':chosen,'original_WAS_ordinary_last_cap_year':2020,'original_WAS_2021_22_component':0,'WAS_Jan31_working_early_release_keeps_earned_or_guaranteed_2020_21_debt':True,'GSW_CHI_UPC_is_new_WAS_contract':False,'old_payment_or_later_resolution_certified_zero':False}

def tw_inventory():
 c=contracts(FOLDER/'Cassius.html');m=contracts(FOLDER/'Mathews.html')
 cw=[r for r in c if r['team']=='WAS'and len(r['rows'])==1 and r['rows'][0][0]=='2020-21']
 mw=[r for r in m if r['team']=='WAS'and len(r['rows'])==1 and r['rows'][0][0]in ['2019-20','2020-21']]
 assert len(cw)==1 and len(mw)==2
 assert all(r['rows'][0][3]=='$0'for r in cw+mw)
 assert sorted(r['rows'][0][0]for r in mw)==['2019-20','2020-21']
 return {'Winston_prior_WAS_TW':cw,'Mathews_prior_WAS_TW':mw,'Winston_next_QO_kind':'TWO_WAY','Mathews_next_QO_kind':'STANDARD','Mathews_STD_QO_protection':'next Two-Way Annual NBADL Salary, not $50000','Winston_TW_QO_protection':50000,'RFA_15_active_or_inactive_days_condition_admitted_not_boxscore_certified':True,'other_2021_UPCs_automatically_adopted':False,'current_contract_money_point_is_actual_WAS_UPC':False}

FIXED_CASES={
 'B0_DEVELOPMENT_ROOKIE_FA':{'actor':'Isaac Bonga','rule':'X6(a) subject X5; X4(c)','professional_NonNBA':False,'condition':'no NBA UPC, no redraft in candidate natural-eligibility 2021 board; old 2020 acceptance window lawfully closed','draft_rights_through_Sep4':'NONE_AFTER_2021_SUBSEQUENT_DRAFT','normal_upper':0,'apron_upper':0,'new_STD':0,'new_TW':0,'exact_expiry':None},
 'B1_PRO_NO_OPEN_RT':{'actor':'Isaac Bonga','rule':'X5(a),(b),(c),(e); X6(a) subject X5','professional_NonNBA':True,'condition':'old no-effective-notice through May18 preserved; any effective first notice >=May19; no new NonNBA signing; operative tender window permits lawful first delivery after Sep4, tender kept open when due','draft_rights_through_Sep4':'CONDITIONAL_EXCLUSIVE_X5','normal_upper':0,'apron_upper':0,'new_STD':0,'new_TW':0,'exact_expiry':None},
 'B1_PRO_OPEN_RT':{'actor':'Isaac Bonga','rule':'X5(a),(b),(c),(e); second-round Required Tender','professional_NonNBA':True,'condition':'same X5 family, current one-season no-bonus minimum Required Tender validly made and open, not accepted; applicable 2021 zero-YOS minimum <=1000000','draft_rights_through_Sep4':'CONDITIONAL_EXCLUSIVE_X5','normal_upper':1000000,'apron_upper':1000000,'new_STD':0,'new_TW':0,'exact_expiry':None},
 'M_PENDING_STD_QO':{'actor':'Garrison Mathews','rule':'XI1(c)(iii)(A); VII4(a)(2)(ii),4(d)(7),6(m)(3)(D)','offer_kind':'STANDARD','condition':'two same-team one-season TWs; 15-day RFA condition; valid operative W21 tender; no acceptance/offer sheet/First Refusal notice; statutory YOS2 minimum and normal FA amount <=1840000','normal_upper':1840000,'apron_upper':1840000,'new_STD':0,'new_TW':0,'protection':'next Two-Way Annual NBADL Salary'},
 'M_QO_WITHDRAW_RENOUNCE':{'actor':'Garrison Mathews','rule':'XI4(c); VII4(g)','offer_kind':'NONE_AFTER_LAWFUL_WITHDRAWAL','condition':'valid withdrawal, player written consent whenever operative W21 requires; only then valid NBA written FA renunciation; all old debt preserved','normal_upper':0,'apron_upper':0,'new_STD':0,'new_TW':0,'protection':None},
 'W_PENDING_TW_QO':{'actor':'Cassius Winston','rule':'XI1(c)(iii)(B); VII4(a)(2)(ii),4(d)(7)','offer_kind':'TWO_WAY','condition':'one first same-team one-season TW, YOS<4; 15-day RFA condition; valid W21 tender, no new acceptance/offer sheet; 0YOS FA floor and TW next salary <=1000000','normal_upper':1000000,'apron_upper':1000000,'new_STD':0,'new_TW':0,'protection':50000,'apron_upper_is_extra_conservative_reservation_not_TW_QO_standard_salary':True},
 'W_QO_WITHDRAW_RENOUNCE':{'actor':'Cassius Winston','rule':'XI4(c); VII4(g)','offer_kind':'NONE_AFTER_LAWFUL_WITHDRAWAL','condition':'valid withdrawal with required written consent, then valid FA renunciation; old debt not erased','normal_upper':0,'apron_upper':0,'new_STD':0,'new_TW':0,'protection':None}}
def case_profiles():return copy.deepcopy(FIXED_CASES)

def build():
 src,raw,obs,docs=sources();web=webster_window();bell=bell_inventory();tw=tw_inventory();cases=case_profiles()
 assert web['waiver_date']==obs[1]['waive_date']=='2015-11-30','Returned Webster waiver date differs from original event'
 assert web['source_family_start']==obs[0]['four_season_family_start']==2013 and web['original_seasons']==list(range(2013,2013+obs[0]['seasons'])),'Returned Webster original family changed'
 assert web['current_cap_year']==2015 and web['post_current_seasons']==[2016]and web['longest_cap_stretch_years']==[2016,2017,2018]
 assert web['applicable_CBA']=='2011 VII7(d)(5)(A)'and web['original_ordinary_or_cap_stretch_2021_22_component']==0 and web['actual_cap_stretch_election']is None
 assert bell['original_WAS_2021_22_component']==0 and bell['GSW_CHI_UPC_is_new_WAS_contract']is False
 for r,(team,dt,season)in zip(bell['reported_named_contracts'],[('WAS','December 18, 2020','2020-21 W'),('WAS','January 23, 2021','2020-21'),('WAS','April 14, 2021','2020-21'),('GSW','May 13, 2021','2020-21'),('GSW','September 25, 2021','2021-22 W'),('CHI','December 30, 2021','2021-22')]):
  assert (r['team'],r['signing_date_reported'],r['rows'][0][0])==(team,dt,season),'Bell returned contract attribution changed'
 original_cw=[r for r in contracts(FOLDER/'Cassius.html')if r['team']=='WAS'and len(r['rows'])==1 and r['rows'][0][0]=='2020-21']
 original_mw=[r for r in contracts(FOLDER/'Mathews.html')if r['team']=='WAS'and len(r['rows'])==1 and r['rows'][0][0]in ['2019-20','2020-21']]
 assert tw['Winston_prior_WAS_TW']==original_cw and tw['Mathews_prior_WAS_TW']==original_mw,'Returned same-team TW source team/date/rows changed'
 assert len(original_cw)==1 and len(original_mw)==2
 assert tw['Winston_next_QO_kind']=='TWO_WAY'and tw['Mathews_next_QO_kind']=='STANDARD','TW completion classification changed'
 assert tw['Mathews_STD_QO_protection']!='50000'and tw['Winston_TW_QO_protection']==50000
 assert cases==FIXED_CASES,'Returned case legal class/price/condition changed'
 # Original S2 boundary is May18: this is a dated lower bound, not the real German contract expiry.
 earliest_notice=date(2021,5,19);earliest_expiry=date(2022,5,19);scope_end=date(2021,9,4)
 assert earliest_expiry>scope_end
 rows=[];f=src[NAMED]['residual_function'];base=f['new_fixed_before_Din_and_other_residual']
 for dt,b,m,w in itertools.product(['2021-08-06','2021-09-04'],['B0_DEVELOPMENT_ROOKIE_FA','B1_PRO_NO_OPEN_RT','B1_PRO_OPEN_RT'],['M_PENDING_STD_QO','M_QO_WITHDRAW_RENOUNCE'],['W_PENDING_TW_QO','W_QO_WITHDRAW_RENOUNCE']):
  parts={k:cases[k]for k in [b,m,w]};n=sum(x['normal_upper']for x in parts.values());a=sum(x['apron_upper']for x in parts.values())
  rows.append({'date':dt,'branches':[b,m,w],'named_normal_upper':n,'named_apron_upper':a,'unaccepted_offers_add_STD':0,'unaccepted_offers_add_TW':0,'P1_STD_before_any_acceptance':15,'remaining_all_r_apron_sufficient_upper':143002000-base-8451384-a,'remaining_some_r_apron_sufficient_upper':143002000-base-3000000-a,'whole_X_upper_certified':False,'offers_are_not_executed_games_or_signed_roster':True})
 assert len(rows)==24 and max(r['named_apron_upper']for r in rows)==3840000
 return {'id':'WASHINGTON_2021_REMAINING_INVENTORY_FAMILY','status':'INDEPENDENTLY_REVIEWED_NAMED_DATED_CANDIDATE_NOT_WHOLE_WAS_EXECUTION','baseline_main':'4253ea8ecf442440474742b017fc857ae6db447b','source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'repository BOM stripped CRLF/CR to LF; raw caches unchanged','new_raw_attempts':raw,'attributed_web_observations':obs,'observed_indexed_body_is_provider_raw':False,'collection_meta_sha256':META_SHA,'observation_capture_sha256':OBS_SHA,'CBA_source_pages':docs,'reused_Bell_raw':{'url':'https://www.salaryswish.com/players/jordan-bell','cache_path':str(BELL),'raw_sha256':BELL_SHA,'source_tier':'SECONDARY_REPORTED_CONTRACT_TEMPLATE'},'Webster':web,'Bell':bell,'TW_completed_contract_inventory':tw,'Bonga_bridge':{'prior_scope_end':'2021-05-18','comparison_start':'2021-07-29','comparison_end':'2021-09-04','natural_draft_date_from_working_board':'2021-07-29','working_board_is_adopted_all60_choice':False,'professional_first_notice_lower_bound':'2021-05-19','professional_one_year_earliest_end_lower_bound':'2022-05-19','end_after_comparison_days':(earliest_expiry-scope_end).days,'actual_notice_or_foreign_contract_expiry':None,'new_NonNBA_signing_added':False,'old_required_tender_acceptance_period_closed_is_admitted_W20_condition':True,'July1_September1_notice_qualifies_tender_by_September10_under_X5b':True,'operative_W20_W21_calendar_actual_exact':None,'operative_tender_timeliness_is_candidate_condition_not_observed_receipt':True,'old_notice_facts_erased':False,'foreign_pay_professional_class_selected':None,'forever_exclusivity_certified':False},'case_profiles':cases,'dated_joint_rows':rows,'summary':{'dated_rows':24,'branch_combinations':12,'max_new_named_reserve':3840000,'max_case_remaining_all_r_sufficient_upper':2901290,'max_case_remaining_some_r_sufficient_upper':8352674,'Pasecniks_1782621_already_in_base_added_again':False,'new_signed_STD_or_TW':0,'working_dates_have_results_or_minutes_changed':False},'remaining_named_inputs':['WAS other historical waived/camp contracts and applicable stretch-family inventory outside the now-ended Webster/Miles originals; no generic actual zero assertion.','Effective written renunciation of all other expired FA holds/unused exceptions on P1 comparison dates, newly created TPE consumed before residual cleanup.','Exact operative W21 QO/tender calendars and optional acceptance/offer-sheet events remain explicit function parameters; Mathews STD acceptance would require a named slot-clearing event.','Unselected P1 Westbrook/Dinwiddie/Butler direction and prior 2023/2024 origin-rights complement remain separate from current named cost endpoints.'],'scope':{'Webster_original_family_current_cap_component_closed':True,'Bell_original_WAS_ordinary_current_component_closed':True,'Bonga_2021_beyond_May18_branch_selected':False,'Winston_Mathews_offer_routes_selected':False,'minimum_bounds_are_admitted_reserve_upper_not_actual_cents':True,'new_later_awards_or_private_obligations_certified_absent':False,'whole_WAS_X_upper_closed':False},'certification':{'independent_review_completed':True,'independent_review_basis':'g11 read actual 2011 PDF191-192, 2017 QO/draft-rights pages and vendor raw, independently recalculated 24 rows and rejected the same two real loader-return mutations after repair (Mathews WAS-to-GSW and Webster 2015-to-2020 waiver). Root read both CBA originals and producer. Author self-controls are not independent checks.','new_author_lock':False,'P1_direction_selected':False,'actual_receipt_acceptance_or_medical_certified':False,'whole_macro3_complete':False,'REGISTER_changed':False,'manuscript_written':0}}

def validate(o):
 try:assert o==build(),'Saved named family differs from current source-bound construction';return[]
 except(AssertionError,KeyError,ValueError,OSError)as e:return[str(e)]
def markdown(o):
 return '\n'.join(['# WAS 2021: Webster·Bell·Bonga·Winston·Mathews 명명 종료/제안 가족','',o['status'],'','## 실제 관측과 원자료','',
 'NBPA 공식 링크로 2011 CBA 원 PDF를 새로 받았다(25,970,448 bytes). 2013 Webster 네 시즌 계약과 2015-11-30 구단 발표 waiver는 당시 Washington Post 기자가 직접 보도한 본문을 web에서 읽었다. 직접 다운로드 두 건은 timeout이다. Winston 공식 체결과 NBA QO 명단은 indexed 본문 관측이며 직접 두 건은403이다. 실패 바이트·web 귀속 관측·성공 원문을 구분한다. TW 두 계약의 팀/시즌과 Bell 각 팀 계약은 SalarySwish 2차 보고 행으로 기록하며 실제 계약 cents 인증은 하지 않는다.','',
 '## 종료된 원계약 성분','',
 'Webster: 실제 당시 규칙 2011 VII7(d)(5)(A)에 따라 current 2015–16은 그대로 두고 남은 2016–17 한 시즌만 2N+1=3년으로 재귀속한다. 가장 늦은 원 cap stretch는2016–17/2017–18/2018–19, 끝은2019-06-30이다. 원 ordinary 또는 cap stretch의2021–22 성분은0이다. 실제 stretch 선택·보호 금액·cash 지급·후대 합의·새 계약의 부재를 인증하는 뜻은 아니다. 2017 조항을2015 사건에 소급하지 않았다.','',
 'Bell: WAS2020–21 camp/Jan23/Apr14 단기 가족 세 개를 보존한다. GSW May13 TW, Sep25 새 표준, CHI Dec30 hardship은 WAS 신계약이 아니다. Jan31의 기존 작업 조기 종료도 원년 earned/guaranteed 비용을 없애지 않는다. 원 WAS ordinary의2021–22 성분은0이며 뒤늦은 판정이나 cap stretch 전역0 주장은 없다.','',
 '## 단순 보유/만료가 아닌 분기','',
 'Bonga는2018 WAS44와 May18까지의 기존 annual tender/통지 없음 설계를 보존한다. 개발계약이 professional이 아니면 X6(a)의 자연2021 SubsequentDraft에서 미재지명/미NBA계약 조건일 때 RookieFA다. 현 작업60명 보드에는 Bonga가 없지만 그 보드를 전체 작가 확정으로 승격하지 않는다. Professional이면 첫 유효 통지는 기존 경계 뒤 가장 빨라도 May19이고 그1년은2022May19보다 빨리 끝나지 않는다. 새 NonNBA 서명은 넣지 않았다. July1 통지가 September1 가용을 밝히는 X5(b)의 tender는 September10 규칙이며 30일 규칙을 발명하지 않는다. 실제 W20/W21 달력·접수일은 null, old acceptance window 종료와 필요한 적시 tender는 법적 후보 조건이다. 열린 최소 tender1m 예약 / 적법한 첫 tender가 아직 열리지 않은 조건 / RookieFA를 별도 비교한다.','',
 'Mathews는 WAS 연속 두 1시즌 TW 완료이므로 XI1(c)(iii)(A)의 STANDARD QO다. 보호는 다음 Two-Way Annual NBADL Salary이지50k가 아니다. Winston은 첫 한 시즌 TW라 eligible 조건에서 TW QO/50k 보호다. 다만 Winston TW QO가 정상 cap의 QO금액 항목에서 제외되어도 VII4(d)(7)의0YOS 최소 FA hold가 남으므로 정상 비용을0으로 지우지 않는다. Mathews1.84m/Winston1m/Bonga RT1m는 명시 최소/hold 상단 조건하의 보수 예약이며 실제 급여 선택이 아니다. Winston apron도1m로 더 넓게 예약했으며 TW QO를 표준 급여라고 주장하지 않는다.','',
 '제안은 미수락·offer sheet/First Refusal notice 미추가로 비교한다. 다른 분기는 적법 withdrawal, 필요시 선수 서면동의, 그 다음 NBA에 유효 FA renunciation이다. 살아 있는 QO를 남긴 채 먼저 renounce하지 않는다. 새 표준/TW 계약은0, P1의15STD는 보존된다. Mathews가 수락하면16번째 STD가 될 수 있으므로 별도의 슬롯 해소와 비용 재개방이 필요하다.','',
 '## 유한 수치와 남은 입력','',
 '12 조합×Aug6/Sep4 두 날짜=24행이다. 추가 명명 예약은0..3,840,000. Pasecniks1,782,621와 Homesley1,517,981는 선행 base127,809,326에 이미 있으므로 다시 더하지 않는다. 최대 예약 조합에서 다른 X_remaining의 모든r 충분 문턱은2,901,290, 일부r 존재 문턱은8,352,674다. 이것은 X의 관측 상단이 아니라 충분조건이다.','',
 '남은 유한 작업은 다른 WAS 과거 waived/camp/stretch 명명 목록, 다른 expired FA/unusedexception의 정리행동, 선택된 P1 권리 complement다. 비공개 장부·모든 후대 영수증 부재를 새 필수 게이트로 만들지 않는다. 원계약 종료와 법적 제안 함수만 진전시켰으며 whole WAS/P1 선택은 아직 미완이다.','',
 '[2011 CBA 원문](https://cosmic-s3.imgix.net/3d8ade10-8e11-11e9-875d-3d44e94ae33f-2011-NBA-NBPA-Collective-Bargaining-Agreement.pdf) · [2017 CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) · [NBA QO 명단](https://www.nba.com/news/2021-free-agency-options-and-qualifying-offers) · [앞 명명 비용](WASHINGTON_2021_NAMED_RESIDUAL_COST_COMPONENTS_2026_10_07.md) · [현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','',
 '|번호|묶음|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23거래·계약|WAS 원계약 종료·24 제안 비교; 전체 X/P1 미선택|','|4|장기커리어|후속시즌 대기|','|5|결말·전체구조|전체 기능표 미완|','|6|집필규격·ContextPack|현행 등록기·Pack0|','|7|통합·독립·작가승인|최종 CLOSED|','','미완료 큰 묶음5 / v0.30 PARTIAL / 설계·원고 CLOSED / 원고0.',''])

def self_test():
 count=0
 for name,field,value in [('tw_inventory','Mathews_next_QO_kind','TWO_WAY'),('webster_window','longest_cap_stretch_years',[2015,2016,2017,2018,2019])]:
  fn=globals()[name]
  def bad(fn=fn,field=field,value=value):
   o=fn();o[field]=value;return o
  with patch(__name__+'.'+name,side_effect=bad):
   try:build();raise RuntimeError('FALSE_PASS '+name)
   except AssertionError:count+=1
 fn=bell_inventory
 def wrong_team():
  o=fn();o['reported_named_contracts'][4]['team']='WAS';return o
 with patch(__name__+'.bell_inventory',side_effect=wrong_team):
  try:build();raise RuntimeError('FALSE_PASS Bell_GSW_to_WAS')
  except AssertionError:count+=1
 for name,field,value in [('webster_window','waiver_date','2020-11-30'),('tw_inventory','Mathews_prior_WAS_TW',None)]:
  fn=globals()[name]
  def bad(fn=fn,field=field,value=value):
   o=fn()
   if value is None:o[field][1]['team']='GSW'
   else:o[field]=value
   return o
  with patch(__name__+'.'+name,side_effect=bad):
   try:build();raise RuntimeError('FALSE_PASS source_return_'+name)
   except AssertionError:count+=1
 return count
PINS={'research/WASHINGTON_2021_NAMED_RESIDUAL_COST_COMPONENTS_2026_10_07.json': '1235a3dfef34898b9f43edaee3a9fd45b18edbee1e107a5b7b21fdc5af783498', 'research/CHA_WAS_FINITE_ROSTER_WORKING_FAMILY_2026_10_07.json': 'b06b071a0bf77bbff05d01d8adfa62472b4c3b90cca8aa2373ced9034712899a', 'research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json': '90099928f9133c4087ee7871939ce58216d183bd186f5ebd3575a56c2348eeed', 'research/BKN_WAS_2021_PRE_JORDAN_NAMED_EXECUTION_FAMILY_2026_10_07.json': 'a0e9ede786047a43abac4d21785b68ae55190e3d768096618ed010147906017b'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();o=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
 if a.check:assert not validate(load(OUT)) and txt(MD)==markdown(o)
 n=self_test()if a.self_test else None
 print(json.dumps({'current':True,'named_date_rows':24,'new_attempts':8,'new_raw_success':4,'Webster_latest_stretch_end':'2019-06-30','max_named_reserve':3840000,'whole_WAS':False,'self_controls':n}))
