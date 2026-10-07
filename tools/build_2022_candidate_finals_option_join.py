"""Append two conditional date witnesses, without selecting the candidate Finals.

Existing eight witnesses and notices remain immutable source snapshots. No
ancestor builder calls; original CBA bytes/page projections checked directly.
"""
from pathlib import Path
from datetime import date,timedelta
from copy import deepcopy
from unittest.mock import patch
import argparse,hashlib,json,fitz

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_candidate_finals_option_join.py'
OUT='research/NBA_2022_CANDIDATE_FINALS_OPTION_JOIN_2026_10_08.json';MD=OUT[:-5]+'.md'
WINDOW='simulation/CHICAGO_2022_ROOKIE_OPTION_WINDOW_JOIN.json'
WP='reviews/CHI2022_OPTION_WINDOW_JOIN_G11_INDEPENDENT_REVIEW_2026_10_07.json'
PO='design/NBA_2022_FULL_POSTSEASON_CANDIDATE.json'
PP='reviews/NBA_2022_FULL_POSTSEASON_CANDIDATE_G11_INDEPENDENT_REVIEW_2026_10_08.json'
PINS={'simulation/CHICAGO_2022_ROOKIE_OPTION_WINDOW_JOIN.json': 'e506efd28a54ceb61e34a8dfc107fb82236f783700f3aa610cd68ff4d62ba2cc', 'reviews/CHI2022_OPTION_WINDOW_JOIN_G11_INDEPENDENT_REVIEW_2026_10_07.json': '0dfb04928dfbd1760de6df33ab195f8620e6cab2f096627d78e1715bfd160871', 'design/NBA_2022_FULL_POSTSEASON_CANDIDATE.json': 'dcefe931a0f82e3733f577cc47a314cc66ad9162a9988d15d7514302424023f5', 'reviews/NBA_2022_FULL_POSTSEASON_CANDIDATE_G11_INDEPENDENT_REVIEW_2026_10_08.json': 'c4f528cf0526e0277e78dc0ac49e107aa122e9dabce83b860c4c1dcdd5df5f59'}
BASELINE='ee0ff822aa127f8263cc69e03ba2a7184053e22e'

def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(root,p):return json.loads(text(root/p))
def sources(root):
 out={}
 for p,h in PINS.items():
  assert sha(root/p)==h,'Physical source changed '+p
  v=load(root,p);assert v==json.loads(text(root/p)),'Returned source differs from independent physical '+p
  out[p]=v
 for rp,p in [(WP,WINDOW),(PP,PO)]:
  assert out[rp]['independent_review_completed'] is True
  assert out[rp]['source_sha256'][p]==PINS[p],'Independent source snapshot mismatch'
 return out

def primary(rule):
 p=Path(rule['raw_cache']);assert hashlib.sha256(p.read_bytes()).hexdigest()==rule['raw_sha256']
 with fitz.open(p) as d:pages={str(n):d[n-1].get_text().replace('\r\n','\n').replace('\r','\n') for n in [32,292]}
 assert {n:hashlib.sha256(t.encode()).hexdigest() for n,t in pages.items()}==rule['page_text_LF_sha256']
 season=' '.join(pages['32'].split());options=' '.join(pages['292'].split())
 assert 'ending immediately after the last game of the NBA Finals' in season
 assert all(x in options for x in ['day following the last day of the first Season','last day of the second Season','October 31','signed by the Team','sent by email'])
 return {'raw_cache':str(p),'raw_sha256':rule['raw_sha256'],'PDF_1based_pages':[32,292],
  'page_text_LF_sha256':deepcopy(rule['page_text_LF_sha256']),
  'rules':'I1(ooo): Season ends immediately after last Finals game; VIII1(a): third-year option after first Season, fourth-year option after second Season, through following Oct31; valid team-signed notice/email.',
  'October31_2022_weekday':'Monday; no weekend deadline extension needed',
  'exact_Finals_ending_clock_timezone_or_actual_notice_receipt_certified':False}

def witness(n,last,index,series_length):
 end=date.fromisoformat(last);opening=end+timedelta(days=1);notice=date.fromisoformat(n['date']);deadline=date(end.year,10,31)
 return {'witness_number':index,'player':n['player'],'original_RSC_first_season':n['original_RSC_first_season'],
  'option_number':n['option_number'],'option_season_number':n['option_season_number'],'added_season':n['added_season'],
  'required_preceding_option_basis_Season':'2021-22','preceding_Season_number_in_original_UPC':2 if n['option_season_number']==4 else 1,
  'candidate_Finals_last_game':last,'candidate_series_length':series_length,'window_start':opening.isoformat(),
  'notice_date':notice.isoformat(),'deadline':deadline.isoformat(),'timely_if_candidate_last_game_adopted':opening<=notice<=deadline,
  'days_after_window_open':(notice-opening).days,'days_before_deadline':(deadline-notice).days,
  'condition':'Candidate final last game is adopted as the 2021-22 NBA Season endpoint; no later Finals rescheduling selected.',
  'candidate_Finals_endpoint_currently_selected':False,'actual_receipt':None,'new_price_bonus_UPC_or_registration_slot':0}

def assert_witness(v,n,last,index,length):
 # Reconstruct returned meanings independently of witness() and any helper loader.
 end=date.fromisoformat(last);notice=date.fromisoformat(n['date']);start=end+timedelta(days=1);deadline=date(2022,10,31)
 assert (v['witness_number'],v['player'],v['original_RSC_first_season'],v['option_number'],v['option_season_number'],v['added_season'])==(index,n['player'],n['original_RSC_first_season'],n['option_number'],n['option_season_number'],n['added_season']),'Returned option identity/UPC changed'
 assert v['required_preceding_option_basis_Season']=='2021-22'
 assert v['preceding_Season_number_in_original_UPC']==(2 if n['option_season_number']==4 else 1),'Wrong first/second Season basis'
 assert v['candidate_Finals_last_game']==last and v['candidate_series_length']==length
 assert (v['window_start'],v['notice_date'],v['deadline'])==(start.isoformat(),notice.isoformat(),deadline.isoformat()),'Returned option window changed'
 assert v['timely_if_candidate_last_game_adopted']==(start<=notice<=deadline)
 assert (v['days_after_window_open'],v['days_before_deadline'])==((notice-start).days,(deadline-notice).days)
 assert v['condition']=='Candidate final last game is adopted as the 2021-22 NBA Season endpoint; no later Finals rescheduling selected.'
 assert v['candidate_Finals_endpoint_currently_selected'] is False and v['actual_receipt'] is None and v['new_price_bonus_UPC_or_registration_slot']==0,'Candidate/price/receipt promoted'

def build(root=ROOT):
 src=sources(root);old=src[WINDOW];po=src[PO];rule=primary(old['primary_rule'])
 assert len(old['window_witnesses'])==8 and all(q['timely'] for q in old['window_witnesses'])
 notices=old['preserved_parent_notices']
 assert [(q['player'],q['original_RSC_first_season'],q['option_season_number'],q['date'],q['deadline']) for q in notices]==[('LaMelo Ball','2020-21',4,'2022-10-01','2022-10-31'),('Chris Duarte','2021-22',3,'2022-10-01','2022-10-31')]
 assert all(q['team']=='CHI' and q['new_registration_slot']==0 and q['new_price_or_bonus_selected'] is False and q['actual_notice_receipt'] is None for q in notices)
 finals=[v for v in po['series'] if v['round']=='F'];assert len(finals)==1
 last=finals[0]['games'][-1]['date'];assert last==po['candidate_last_Finals_date']=='2022-06-20'
 assert len(finals[0]['games'])==7 and finals[0]['classification']=='UNSELECTED_NEW_CANDIDATE'
 assert po['certification']['NBA_Season_end_and_eight_options_selected'] is False and po['certification']['championship_author_locked'] is False
 additions=[]
 for i,n in enumerate(notices,9):
  v=witness(n,last,i,len(finals[0]['games']));assert_witness(v,n,last,i,7);assert v['timely_if_candidate_last_game_adopted'] is True;additions.append(v)
 return {'id':'NBA_2022_CANDIDATE_FINALS_OPTION_JOIN_2026_10_08','baseline_main':BASELINE,
  'status':'TEN_TIMELINESS_WITNESSES_EIGHT_PRESERVED_TWO_CONDITIONAL_CANDIDATE_ONLY',
  'source_sha256':{**PINS,SELF:sha(root/SELF)},'hash_method':'UTF8_BOM_STRIP_CRLF_CR_TO_LF',
  'direct_primary_check':rule,'preserved_eight_window_witnesses':deepcopy(old['window_witnesses']),
  'preserved_parent_notices':deepcopy(notices),'additional_ninth_tenth_conditional_witnesses':additions,
  'candidate_endpoint':{'date':last,'series_id':finals[0]['id'],'games':7,'participants':deepcopy(finals[0]['teams']),
   'champion':po['candidate_champion'],'endpoint_classification':'UNSELECTED_NEW_FICTIONAL_CANDIDATE_NOT_THE_ORIGINAL_FOUR_PUBLISHED_ENDINGS',
   'adopted_as_actual_alternate_Season_end':False,'physical_NBA_Finals_result_certified':False},
  'preserved_roster_snapshot':deepcopy(old['preserved_roster']),
  'preserved_old_option_join_cost_snapshot':deepcopy(old['preserved_2022_23_cost_family']),
  'price_and_UPC_effect':{'new_price_bonus_protection_or_contract_term_selected':False,
   'original_pick4_2020_RSC_and_pick10_2021_RSC_carried':True,
   'original_added_year_regular_salary':'ORIGINAL_UPC_OPTION_YEAR_REGULAR_SALARY_FUNCTION',
   'all_original_components_and_Gamma_preserved':True,'new_STD_TW_slot':0,
   'cost_snapshot_is_historical_consumed_option_join_not_latest_rookie_repricing':True,
   'new_LaMelo_extension_or_Duarte_fourth_year_option_selected':False},
  'summary':{'old_timely_witnesses_preserved':8,'new_conditional_timely_witnesses':2,'combined_timeliness_support':10,
   'candidate_opening':'2022-06-21','preserved_notice':'2022-10-01','deadline':'2022-10-31',
   'both_new_notice_days_after_open':102,'both_new_notice_days_before_deadline':30,
   'all_ten_date_inequalities_pass':True,'new_option_or_price_selections':0},
  'certification':{'independent_review_completed':False,'root_adoption_recorded':False,
   'candidate_Finals_last_game_selected':False,'new_champion_or_title_selected':False,
   'all_eight_options_actual_NBA_execution_certified':False,'actual_private_notice_receipts_certified':False,
   'whole_macro3_G13_G16_or_manuscript':False},
  'remaining_finite_input':'Choose the league Finals endpoint/title separately; date support already holds conditionally for Jun20. Existing option notice/model/price stays unchanged; no source absence or real receipt gate added.',
  'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}

def validate(v,root=ROOT):return [] if v==build(root) else ['Saved candidate option join differs from bound physical sources']
def markdown(v):
 lines=['# 후보 Finals 말단과 두 원옵션 통지','','기존8개 날짜 증인은 보존한다. 새 전체 PO 후보의 **2022-06-20** 말단은 미선택이며, 이 말단이 채택될 경우의 **9·10번째 조건부 증인**만 추가했다. 6/20을 원 NBA 사실이나 기존4개 발표 말단의 선택으로 바꾸지 않는다.','','| 증인 | 선수 | 원옵션 | 이전 UPC 시즌 근거 | 조건부 창 시작 | 원 통지 | 마감 | 조건부 적기 |','|---|---|---|---|---|---|---|---|']
 lines += [f"| {w['witness_number']} | {w['player']} | {w['option_season_number']}년차 | {w['preceding_Season_number_in_original_UPC']}번째 Season 말단 | {w['window_start']} | {w['notice_date']} | {w['deadline']} | {w['timely_if_candidate_last_game_adopted']} |" for w in v['additional_ninth_tenth_conditional_witnesses']]
 lines += ['','원CBA I1(ooo)/VIII1(a), PDF32·292를 직접 읽고 지문을 대조했다. NBA Season은 마지막 Finals 직후 끝나며 샐러리연도 June30과 다르다. LaMelo의2020–21 UPC 네 번째 옵션은 두 번째2021–22 Season 뒤, Duarte의2021–22 UPC 세 번째 옵션은 첫2021–22 Season 뒤에 열린다. 다음날6/21부터10/31까지10/1 통지는 창 시작102일 뒤·마감30일 전이다. 10/31/2022는 월요일이다.','','기존8+추가조건2의 날짜 부등식10개 모두 PASS. 이는8개 옵션의 실제 NBA 행사/접수 인증이 아니다. 기존 두 team-signed 이메일 통지의 가상 선택을 보존하고 실제 영수증은 null이다. 원pick4/pick10 UPC·옵션연도 급여함수·모든 bonus/protection/Γ 및15+2는 변하지 않는다. 새가격/등록/LaMelo연장/Duarte네 번째 옵션0.','','동결된 이전 비용표는 원옵션 연결의 소비 스냅숏이며 최신 신인 가격표를 재평가하거나 바꾸지 않는다. 후보우승/기간 채택과 전체3번은 남는다.','','[기존8증인](../simulation/CHICAGO_2022_ROOKIE_OPTION_WINDOW_JOIN.md) · [전체 PO 후보](../design/NBA_2022_FULL_POSTSEASON_CANDIDATE.md) · [2017 CBA](https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf) · [현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','','| 묶음 | 상태 |','|---|---|','| 1 드래프트 연쇄 | 완료 |','| 2 Chicago2020–21 | 완료 |','| 3 2021–23 | PO·새말단 옵션 조건부 연결, 채택/후속 미완료 |','| 4 장기커리어 | 진행 |','| 5 전체구조 | 현행 기능등록기 참조 |','| 6 규격·Context Pack | 현행 source등록기 참조·Pack0 |','| 7 통합·작가승인 | 미완료 |','','미완료 큰묶음5/6번까지4 · v0.30 PARTIAL · CLOSED · 원고0.','']
 return '\n'.join(lines)

def self_test():
 original=witness
 for field,value in [('window_start','2022-10-02'),('preceding_Season_number_in_original_UPC',0),('candidate_Finals_endpoint_currently_selected',True)]:
  def bad(*a,field=field,value=value,**kw):
   v=original(*a,**kw);v[field]=value;return v
  with patch(__name__+'.witness',bad):
   try:build()
   except AssertionError:pass
   else:raise AssertionError('FALSE_PASS '+field)
 return 3
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();v=build()
 if a.write:
  (ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if a.check:assert load(ROOT,OUT)==v and text(ROOT/MD)==markdown(v),'Candidate option join stale'
 print(json.dumps({'current':True,'summary':v['summary'],'writer_controls':self_test() if a.self_test else None}))
if __name__=='__main__':main()
