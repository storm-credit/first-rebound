"""Two named one-year minimum tender reservations, without rights execution.
Reported minimum points support widened conditional cost bounds; no exact
rounding, actual tender, rookie identity or new foreign rights is certified.
"""
import argparse,copy,hashlib,json,re
from pathlib import Path
from unittest.mock import patch
from bs4 import BeautifulSoup
import fitz
import build_chicago_2022_legacy_carry_refinement as prior
import build_chicago_2022_full_cost_roster_family as full
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_second_tender_cost_refinement.py'
OUT='research/CHICAGO_2022_SECOND_TENDER_COST_REFINEMENT_2026_10_07.json'
MD=OUT[:-5]+'.md'
SIM='research/SIMONOVIC_2021_22_RIGHTS_CONTINUATION_2026_10_07.json'
MIN=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-minimum-year2-20261007/salaryswish_minimum.html')
MIN_SHA='0c808010bd97008e17d7b59c2a610270bc528e7f3f04b48f12a8ec6ceb70eefe'
CAP=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-chi-core2022-20261007/NBA_CAP2022.html')
CAP_SHA='2e76093cfc91b6257f18cddd25441090118f36bd8a942259fbc340438ff5e57f'
PINS={
 prior.OUT:'ec95c68e5f4fb0ae6a799f2c74705c5c733945719c740b0349bf128be6832c81',
 prior.SELF:'f14a786ff409916fc6d4ca3df468bd174c341cd388a19c7dbd6675879cd5f008',
 full.OUT:'16830b560cf4f2008053ac236202010ff87188f42536a5d36870433933feccf0',
 full.SELF:'13492290890cb954baef2f095aba13c316ea1b873547102f18950a02188f68e7',
 SIM:'605e23f01c818b63a1782246824738c253591fd056bd8b66790c3409036a9937'}
NORMAL=1018000
APRON=1837000
OLD=3000000

def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def policy():
 return {'named_ports':['CHI2022_COMPOSITE_SECOND','SIMONOVIC2020_SECOND'],
 'port_count':2,'never_signed_NBA_UPC_and_credited_YOS0_condition':True,
 'one_season_applicable_2022_minimum_no_bonus_form_only':True,
 'normal_per_port_conditional_upper':NORMAL,'apron_per_port_conditional_upper':APRON,
 'source_scale_within_widened_bounds_condition':True,
 'apron_RookieFA_possibility_overcovered_not_classified':True,
 'unaccepted_second_tender_is_asserted_statutory_charge':False,
 'other_minimum_filler_and_TW_QO_3m_reservations_changed':False,
 'annual2022_Simonovic_rights_or_tender_execution_selected':False,
 'actual_private_contract_or_legal_exact_rounding_certified':False}
FIXED=copy.deepcopy(policy())

def sources():
 for p,h in PINS.items():assert sha(p)==h,'Unreviewed source: '+p
 o=load(prior.OUT);assert o==prior.build(),'Reviewed legacy source differs'
 assert o['certification']['independent_review_completed']
 p=full.checked_policy()
 assert p['Simonovic_RT_fullcash_reservation']==OLD
 assert p['Simonovic_no_NBA_UPC'] and p['Simonovic_tender_accepted']is False
 assert p['new_second_RequiredTender_candidate']=='One-Season no-bonus statutory minimum; valid X4a lateAugust/September5 window, accepts through at least October15. Offer not automatically signed; actual dates/receipt null.'
 n=load(prior.named.OUT)
 assert n['cost_interface']['new_second_count_upper']==1 and n['cost_interface']['second_unaccepted_RT_fullcash_overreserve']==OLD
 assert n['cost_interface']['Simonovic_old_second_RT_reserved_separately']==OLD
 assert hashlib.sha256(MIN.read_bytes()).hexdigest()==MIN_SHA
 soup=BeautifulSoup(MIN.read_bytes(),'html.parser');tb=soup.find('tbody',id='cba_2023');assert tb
 rows={int(r.find_all('td')[0].get_text(strip=True)):[c.get_text(' ',strip=True)for c in r.find_all('td')]for r in tb.find_all('tr')if r.find_all('td')}
 z=int(re.sub('[^0-9]','',rows[0][1]));two=int(re.sub('[^0-9]','',rows[2][1]))
 assert(z,two)==(1017781,1836090) and z<NORMAL and two<APRON
 assert hashlib.sha256(CAP.read_bytes()).hexdigest()==CAP_SHA
 captext=BeautifulSoup(CAP.read_bytes(),'html.parser').get_text(' ',strip=True)
 assert '123.655'in captext
 assert hashlib.sha256(prior.CBA.read_bytes()).hexdigest()==prior.CBA_SHA
 with fitz.open(prior.CBA)as d:
  pages={str(n):hashlib.sha256(d[n-1].get_text().encode()).hexdigest()for n in [27,30,31,54,55,240,241,286,303,304]}
  assert 'Minimum Annual Salary then applicable'in ' '.join(d[29].get_text().split())
  assert 'never signed a Player'in d[30].get_text()
  assert 'Free Agent with zero'in d[285].get_text()
  assert 'two (2) weeks before the September 5'in d[302].get_text()
 return o,{'minimum_table':{'url':'https://www.salaryswish.com/minimum-salary-faq','cache_path':str(MIN),'raw_sha256':MIN_SHA,'locator':'tbody#cba_2023; creditedYOS0/2 rows, first salary column','classification':'PUBLIC_VENDOR_REPORTED_MINIMUM_NOT_OFFICIAL_ROUNDING_ALGORITHM','reported_points':{'YOS0':z,'YOS2':two}},'NBA_cap':{'url':'https://pr.nba.com/nba-salary-cap-2022-23-season/','cache_path':str(CAP),'raw_sha256':CAP_SHA,'official_cap':123655000},'CBA':{'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(prior.CBA),'raw_sha256':prior.CBA_SHA,'PDF1based_text_sha256':pages}}

def project(o,p):
 return [{**r,'source_normal_upper':r['normal_upper'],'source_apron_upper':r['apron_upper'],
 'normal_upper':r['normal_upper']-2*(OLD-NORMAL),'apron_upper':r['apron_upper']-2*(OLD-APRON),
 'replaced_two_tender_normal_reservation':2*NORMAL,'replaced_two_tender_apron_reservation':2*APRON,
 'draft_or_Simonovic_rights_or_UPC_selected':False}for r in o['refined_rows']]

def assert_rows(rows,o):
 key=lambda r:(r['case'],r['Carter'],r['Protagonist'],r['source_leaf_stage'])
 src={key(r):r for r in o['refined_rows']}
 assert len(rows)==len(src)==576 and len({key(r)for r in rows})==576
 for r in rows:
  s=src[key(r)]
  assert r['source_normal_upper']==s['normal_upper'] and r['source_apron_upper']==s['apron_upper']
  assert r['normal_upper']==s['normal_upper']-3964000 and r['apron_upper']==s['apron_upper']-2326000
  assert r['replaced_two_tender_normal_reservation']==2036000 and r['replaced_two_tender_apron_reservation']==3674000
  assert r['draft_or_Simonovic_rights_or_UPC_selected']is False
  # Every unrelated source field is preserved, including old camp removal.
  for k,v in s.items():
   if k not in ['normal_upper','apron_upper','source_normal_upper','source_apron_upper']:assert r[k]==v

def build():
 p=policy();assert p==FIXED,'Tender scope or cost bound changed'
 o,ev=sources();rows=project(o,p);assert_rows(rows,o)
 return {'id':'CHICAGO_2022_SECOND_TENDER_COST_REFINEMENT','status':'INDEPENDENTLY_REVIEWED_TWO_CONDITIONAL_MINIMUM_RESERVATIONS_NOT_RIGHTS_EXECUTION',
 'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'Repository BOMstrip LF; external raw bytes separate','sources':ev,'policy':p,
 'derivation':['I1ddd permits a one-season second-round Required Tender at the applicable minimum; the existing proposal already chooses that statutory no-bonus form, not an arbitrary above-minimum tender.',
 'I1fff defines Rookie by never signing an NBA UPC, rather than years abroad. Both named economic ports have conditional NBA YOS0; any changed UPC/creditedservice reopens this refinement.',
 'Exclusive DraftRookie is not automatically a Free Agent; afterrights expiry RookieFA is possible. For the apron, use the larger two-YOS floor envelope for both ports without asserting which classification actually applies.',
 'Unaccepted secondTender is not certified statutory TeamSalary. These amounts remain fullcash overreservations and cover a resulting minimumUPC only when applicable rights/consent/slot conditions are separately fulfilled.',
 'Simonovic previous continuation proves only the2021-22 window and a conservative endpoint beyondJune30; it does not prove laterAugust2022 rights or valid annualTender. The pending X5/6 event family remains unselected.'],
 'remaining_named_execution_condition':{'actor':'SIMONOVIC2020_SECOND','condition':'At any later annualTender/UPC date, apply surviving X5period/valid timelyannualTender or lawful RookieFA route. Earliest conservativeJuly29 endpoint does not certify lateAugust rights.','exact_future_period_end':None,'actual_tender_or_delivery':None,'permanent_exclusive_rights_certified':False},
 'refined_rows':rows,'summary':{'rows':576,'source_cells':192,'normal_reduction':3964000,'apron_reduction':2326000,'normal_range':[min(r['normal_upper']for r in rows),max(r['normal_upper']for r in rows)],'apron_range':[min(r['apron_upper']for r in rows),max(r['apron_upper']for r in rows)]},
 'certification':{'independent_review_completed':True,'independent_review_basis':'Root read original CBA30/31/286/303/304 plus previously54/55/240/241; separately parsed vendor0/2YOS table and checked3 raw bytes. Independently recalculated576 keyed rows; returned apron-floor-removal rejected. Simon later-August rights remain conditional, not an executed tender.','conditional_numeric_outer_only':True,'exact_statutory_rounding_or_private_cents_certified':False,'actual_rights_or_tender_or_UPC_selected':False,'whole_FY22_cost_or_roster_selected':False,'whole_macro3_complete':False,'REGISTER_or_central_changed':False,'manuscript_written':0}}

def validate(o):
 try:assert o==build(),'Saved source/refinement differs';return[]
 except(AssertionError,KeyError,OSError,ValueError)as e:return[str(e)]
def markdown(o):
 x=o['summary'];return '\n'.join(['# FY22 두 2라운드 최소계약 예약 정밀화','',o['status'],'',
 '새2022second1개와Simonović기존2020second1개의 **이미제안된1년·법정minimum·보너스0** fullcash예약만 좁힌다. [2017 CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) I1ddd/fff/ggg(PDF30–31),II6(PDF54–55),VII12f2ii(PDF286),VII6m3(PDF240–241)를 구별했다. RT는 최소보다높게 제안할수있지만 그모든다른임의제안을이family에추가하지않는다.','',
 '[SalarySwish공개표](https://www.salaryswish.com/minimum-salary-faq)의2022–23 YOS0보고점1,017,781/YOS2보고점1,836,090을 각각1,018,000/1,837,000 조건부상단으로넓혔다. [공식NBAcap](https://pr.nba.com/nba-salary-cap-2022-23-season/)123,655,000과서명capyear적용을대조했다. 공식반올림알고리즘·정확사적센트인증이아니며, 해당법정scale가넓힌상단안이라는조건을보존한다.','',
 'ExclusiveDraftRookie는FreeAgent와같지않다. 권리종료뒤RookieFA가능성까지과포괄하여 apron은두포트모두2YOSfloor상단을예약한다. 지위나새2022권리실행을선택하지않는다. 미수락2RT는실제법정capcharge라단정하지않는fullcash예약이며, 수락하면명명된유효권리/동의/STD슬롯조건이별도로필요하다.','',
 'Simonović후속2021–22기간의보수말단7월29일은늦은8월RT유효성을자동보증하지않는다. X5기간/가용통지와X6annualTender또는합법RookieFA경로가다음날짜에충족되어야한다. 실제통지·만료·해외연장·NBAUPC는미선택이다. genericminimumfiller/TW표준QO의3m예약,first11.06m,기존슬롯형식은불변이다.','',
 f'검문된192셀/576상태의 Normal은각3,964,000,apron은각2,326,000감소한다. Normal{x["normal_range"][0]:,}–{x["normal_range"][1]:,};apron{x["apron_range"][0]:,}–{x["apron_range"][1]:,}. 계약·드래프트·명단선택이나전체FY22완료로승격하지않고음수apron을위법으로판정하지않는다.','',
 '미완료큰묶음5 / v0.30 PARTIAL / 설계·원고CLOSED / Pack0·원고0.',''])
def self_test():
 p=policy();p['annual2022_Simonovic_rights_or_tender_execution_selected']=True
 with patch(__name__+'.policy',return_value=p):
  try:build();raise RuntimeError('FALSE_PASS rights_auto_extension')
  except AssertionError:pass
 old=project
 def bad(o,p):
  rows=old(o,p);rows[0]['apron_upper']-=819000;return rows
 with patch(__name__+'.project',side_effect=bad):
  try:build();raise RuntimeError('FALSE_PASS DraftRookie_apron_assumed_for_all')
  except AssertionError:pass
 return 2
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');args=ap.parse_args();o=build()
 if args.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
 if args.check:assert validate(load(OUT))==[]and text(MD)==markdown(o)
 print(json.dumps({'current':True,**o['summary'],'controls':self_test()if args.self_test else None}))
