"""Join two selected option notices to a finite fictional Finals calendar family."""
from pathlib import Path
from copy import deepcopy
from datetime import date, timedelta
import argparse, hashlib, json
import fitz

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_rookie_option_window_join.py'
OUT='simulation/CHICAGO_2022_ROOKIE_OPTION_WINDOW_JOIN.json'
MD=OUT[:-5]+'.md'
OPTION='simulation/CHICAGO_2022_ROOKIE_OPTION_CONTINUITY.json'
OPTION_PEER='reviews/CHI2022_ROOKIE_OPTION_CONTINUITY_G11_INDEPENDENT_REVIEW_2026_10_07.json'
DATES='research/FINALS_2022_PUBLISHED_DATE_WINDOW_2026_10_07.json'
DATES_PEER='reviews/FINALS_2022_PUBLISHED_DATE_WINDOW_G11_INDEPENDENT_REVIEW_2026_10_07.json'
PINS={OPTION:'73be5f3fba98adef435a1c93f3e8aba43fcc2f1e4c81f4aa57a25199eedc5dfe',OPTION_PEER:'c799645584ffea022db44aa0f4c0e64dfc06af946c1c27605191cf0152691c5b',DATES:'8fdf5f89c1e476ab9c1818713910b32f0c21cd0c79987222b27b08693adc45cd',DATES_PEER:'090f6e6139d02817962bab12224016c88409eb86dd91f4092fc1716b652761e7','reviews/MACRO3_FINITE_EXIT_AND_CORE_ROUTINE_AUTHORITY_AUDIT_2026_10_07.md':'22e422447f84051a18ffdfcef710f90d54c2bc7dc6d30fc9447936930646a83a'}
EXPECTED_DATES=['2022-06-02','2022-06-05','2022-06-08','2022-06-10','2022-06-13','2022-06-16','2022-06-19']

def need(ok,why):
    if not ok:raise ValueError(why)

def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def read(root,p):return json.loads(text(root/p)) if p.endswith('.json') else text(root/p)

def window_witness(notice,finals_last):
    n=date.fromisoformat(notice);last=date.fromisoformat(finals_last)
    opening=last+timedelta(days=1);deadline=date(last.year,10,31)
    need(opening<=n<=deadline,'Notice is outside post-Season option window')
    return {'last_Finals_game':last.isoformat(),'window_start':opening.isoformat(),'notice_date':n.isoformat(),'deadline':deadline.isoformat(),'timely':True}

def build(root=ROOT):
    src={}
    for p,h in PINS.items():
        need(sha(root/p)==h,'Accepted input changed: '+p);src[p]=read(root,p)
        direct=json.loads(text(root/p)) if p.endswith('.json') else text(root/p)
        need(src[p]==direct,'Returned input differs from physical source: '+p)
    option=src[OPTION];dates=src[DATES]
    for peer,p in [(src[OPTION_PEER],OPTION),(src[DATES_PEER],DATES)]:
        need(peer['independent_review_completed'] and peer['source_sha256'][p]==PINS[p],'Parent review stale: '+p)
    published=dates['sources'][1]['dates'];need(published==EXPECTED_DATES,'Published Finals calendar changed')
    need(dates['sources'][1]['conditional_games']==[5,6,7],'Conditional game domain changed')
    rule=option['primary_rule'];cache=Path(rule['raw_cache'])
    need(hashlib.sha256(cache.read_bytes()).hexdigest()==rule['raw_sha256'],'Primary CBA raw changed')
    with fitz.open(cache) as d:
        pages={str(n):d[n-1].get_text().replace('\r\n','\n').replace('\r','\n') for n in [32,292]}
    need({p:hashlib.sha256(t.encode()).hexdigest() for p,t in pages.items()}==rule['page_text_LF_sha256'],'Original CBA text changed')
    need('ending immediately after the last game of the NBA Finals' in ' '.join(pages['32'].split()),'Wrong Season end')
    flat=' '.join(pages['292'].split())
    need(all(x in flat for x in ['day following the last day of the first Season','last day of the second Season','October 31','signed by the Team','sent by email']),'Original option/notice rule missing')
    notices=deepcopy(option['selected_notices'])
    need([(q['player'],q['original_RSC_first_season'],q['option_season_number'],q['date']) for q in notices]==[('LaMelo Ball','2020-21',4,'2022-10-01'),('Chris Duarte','2021-22',3,'2022-10-01')],'Named option identity/year/date changed')
    need(all(q['deadline']=='2022-10-31' and q['team']=='CHI' and q['new_registration_slot']==0 for q in notices),'Original notices changed')
    witnesses=[{'player':q['player'],'option_season_number':q['option_season_number'],'series_length':g,**window_witness(q['date'],published[g-1])} for q in notices for g in [4,5,6,7]]
    return {'id':'CHICAGO_2022_ROOKIE_OPTION_WINDOW_JOIN','baseline_main':'18ab12a167a3e0885743171ff534c4573fa349ef','status':'ROOT_ROUTINE_CALENDAR_IMPLEMENTATION_SELECTED_ALL_FOUR_ENDINGS_TIMELY','source_sha256':{**PINS,SELF:sha(root/SELF)},
      'classification':{'published_dates':'FACT_PRIMARY_INPUT_FROM_ACCEPTED_PARENT','calendar_adoption':'ROOT_ROUTINE_FICTIONAL_SEASON_DESIGN_SELECTION','all_four_timely':'INFERENCE_FROM_SELECTED_CALENDAR_AND_ORIGINAL_NOTICE_DATES','author_locked_price_title_or_series_length':False},
      'selected_calendar_family':{'scheduled_Finals_games':deepcopy(published),'conditional_games':[5,6,7],'no_rescheduling':'SELECTED_WORKING_CALENDAR_FAMILY_NOT_REAL_EVENT_ABSENCE_CERTIFICATE','possible_last_games':published[3:],'specific_last_game':None,'participants':None,'champion':None},
      'primary_rule':deepcopy(rule),'preserved_parent_notices':notices,'window_witnesses':witnesses,
      'join':{'dated_notice_timeliness_join_closed':True,'all_two_notices_by_four_possible_endings':8,'last_game_or_champion_needed_to_prove_timeliness':False,'signed_notice_and_original_UPC_terms_reused':True,'actual_notice_receipts':None,'actual_alternate_Season_end':None},
      'preserved_roster':deepcopy(option['current_roster_preserved']),'preserved_2022_23_cost_family':deepcopy(option['current_2022_23_cost_family_preserved']),
      'boundaries':{'parent_pending_marker_retained_as_history':True,'whole_two_season_results_or_macro3_closed':False,'new_salary_or_UPC_slot':0,'new_2023_extension_or_Duarte_fourth_option_selected':False,'historical_medical_private_receipt_certified':False,'manuscript_allowed':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED'}}

def markdown(v):
    lines=['# Chicago2022 옵션 통지 날짜 연결','',
      '기존 LaMelo fourth/Duarte third 옵션 통지는 그대로 둔다. 공식 발표 Finals7일정을 2022 가상 시즌 달력으로 routine 채택하고, 재일정 없는 가족을 명시적으로 선택했다. 이는 실제 사건 부재/통지 영수증/우승팀 선택이 아니다.','',
      '**Finals G4–7 어느 종료일에서도 다음날부터 October31까지의 창 안에 October1 통지가 들어온다. 두 통지 × 네 종료일 = 8개 날짜 증인을 검문했다.** 특정 우승팀/시리즈 길이/마지막 날짜는 선택하지 않아도 이 날짜 조건은 닫힌다. June30을 Season 종료로 대체하지 않는다.','',
      '|선수|길이|Finals 종료|창 시작|원 통지|마감|','|---|---|---|---|---|---|']
    lines += [f"|{w['player']}|{w['series_length']}|{w['last_Finals_game']}|{w['window_start']}|{w['notice_date']}|{w['deadline']}|" for w in v['window_witnesses']]
    lines += ['', '[원 통지/원급여·보호·명단](CHICAGO_2022_ROOKIE_OPTION_CONTINUITY.md) · [공식 발표 날짜 입력](../research/FINALS_2022_PUBLISHED_DATE_WINDOW_2026_10_07.md) · [2017 CBA 원문](https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf)','',
      '원 UPC 성분과15STD2TW·FY22 전체비용 가족은 불변이다. 새 UPC/가격/옵션행사0이며 Duarte fourth/LaMelo 연장/두 시즌 결산은 별도 후속이다. 부모 PENDING label은 당시 이력으로 남고 현행 날짜 join은 이 소비기에서 수용한다. 전체3번/실제 사적통지/최종승인/원고를 열지 않는다.','',
      '미완료 큰 묶음5/6번까지4·v0.30 PARTIAL·설계/원고 CLOSED·원고0.','']
    return '\n'.join(lines)

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();v=build();out={OUT:json.dumps(v,ensure_ascii=False,indent=2)+'\n',MD:markdown(v)}
    if a.write:
        for f,t in out.items():(ROOT/f).write_text(t,encoding='utf-8')
    if a.check:
        for f,t in out.items():need(text(ROOT/f)==t,'Window artifact stale: '+f)
    print(json.dumps({'notices':2,'ending_dates':4,'timely_witnesses':8,'date_join_closed':True,'whole_macro3':False}))
if __name__=='__main__':main()
