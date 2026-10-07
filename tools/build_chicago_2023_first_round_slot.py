"""Resolve Chicago's nonlottery origin slot without resolving unrelated draws."""
from pathlib import Path
import argparse,hashlib,json,fitz
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2023_first_round_slot.py'
OUT='research/CHICAGO_2023_FIRST_ROUND_SLOT_16_2026_10_08.json'
CLAIMS='research/CHICAGO_2023_NAMED_DRAFT_CLAIMS_AND_COST_PORTS_2026_10_08.json'
SEEDS='simulation/NBA_2022_23_STANDINGS_AND_2023_PLAYIN.json'
GLOBAL='simulation/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS.json'
PEER='reviews/CHI_2023_CLAIMS_AND_PLAYIN_G11_INDEPENDENT_REVIEW_2026_10_08.json'
RULE=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-2019-bylaws.pdf')

def norm(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(norm(p).encode()).hexdigest()
def read(p):return json.loads(norm(ROOT/p))
def need(v,m):
 if not v:raise AssertionError(m)

def build():
 peer=read(PEER);need(peer['independent_review_completed'],'Unreviewed predecessor')
 need(peer==json.loads(norm(ROOT/PEER)),'Returned independent review differs from physical record')
 for p in [CLAIMS,SEEDS,GLOBAL]:need(sha(ROOT/p)==peer['source_sha256'][p],'Reviewed input changed '+p)
 claims=read(CLAIMS);seeds=read(SEEDS);g=read(GLOBAL)
 for p,v in [(CLAIMS,claims),(SEEDS,seeds),(GLOBAL,g)]:
  need(v==json.loads(norm(ROOT/p)),'Returned named input differs from reviewed physical record '+p)
 need(claims['named_claims'][0]['selected_holder']=='CHI','Chicago own first not retained')
 need(hashlib.sha256(RULE.read_bytes()).hexdigest()=='6accb3d9633e15e8559d13228c27ae7b3b0b81eac0894050b06256eea6da3464','Draft rule raw changed')
 with fitz.open(RULE)as pdf:t=pdf[85].get_text()
 need('Teams that participate in the Playoffs' in t and 'inverse order of their consolidated standings' in t,'Draft rule body changed')
 teams=[x['team']for rows in seeds['final_playoff_seeds'].values()for x in rows]
 need(len(teams)==len(set(teams))==16 and len(seeds['nonplayoff_lottery_origins'])==14 and 'CHI'in teams,'Qualification domains')
 records=[{'origin':x,**g['team_records'][x]}for x in teams]
 chi=g['team_records']['CHI'];need(chi=={'wins':46,'losses':36},'Chicago record changed')
 earlier=[x['origin']for x in records if x['wins']<chi['wins']]
 tied=[x['origin']for x in records if x['wins']==chi['wins']and x['origin']!='CHI']
 need(earlier==['NOP'] and not tied,'Chicago slot no longer unique')
 slot=15+len(earlier);need(slot==16,'Chicago origin slot')
 return {'id':'CHI_2023_FIRST_ROUND_SLOT_16','baseline_main':'241821ba24936ee788320844822af5a3f32ef69c',
  'status':'DERIVED_FROM_SELECTED_FICTIONAL_REGULAR_AND_PLAYIN_RESULTS',
  'source_sha256':{p:sha(ROOT/p)for p in [SELF,CLAIMS,SEEDS,GLOBAL,PEER]},
  'primary_rule':{'url':'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf',
   'raw_cache':str(RULE),'raw_sha256':hashlib.sha256(RULE.read_bytes()).hexdigest(),'PDF1based':86,'printed_page':77,'section':'7.02(a)(iii)',
   'page_text_utf8_sha256':hashlib.sha256(t.encode()).hexdigest(),'body_directly_read':True,
   'fact_summary':'Playoff participants select after the lottery teams in reverse order of regular-season standings.',
   'current_FAQ_crosscheck_url':'https://cdn-uat.nba.com/news/nba-draft-faq','current_FAQ_body_read':True,
   'current_FAQ_is_original_2023_publication':False},
  'selected_qualified_origins_and_records':records,'lottery_count':14,'Chicago_record':chi,
  'qualified_origins_before_Chicago':earlier,'qualified_origins_tied_with_Chicago':tied,
  'calculation':'15 + count(qualified teams with fewer wins than CHI) = 15 + 1 = 16',
  'Chicago_origin_first_slot':slot,'Chicago_selected_holder':'CHI',
  'unrelated_regular_ties_lottery_draws_or_first_round_draws_required_for_this_slot':False,
  'exact_postseason_series_winner_required_for_this_slot':False,
  'cost_ports':{'new_STD_rookie_reservation':1,'round':1,'slot':16,'N23_positive_unpriced':True,'A23_positive_unpriced':True,'null_is_zero':False},
  'certification':{'Chicago_named_draft_slot_complete':True,'draftee_and_RSC_price_selected':False,'all_60_controls_complete':False,
   'actual_NBA_2023_Chicago_draft_rank_claimed':False,'whole_cost_or_macro3_complete':False,'manuscript_allowed':False,'gate':'CLOSED'}}

def md(v):return '''# Chicago 2023 자체 1R: 16번

검문한 가상 정규 결과·플레이인에서는 Chicago가 플레이오프 진출16팀에 포함된다. 그중 NOP40승만 CHI46승보다 적고 나머지14팀은49승 이상이다. CHI와 같은 승수의 진출팀은 없다.

따라서 로터리14팀 뒤 **15 + 앞선 진출팀1 = 자체 16번**이다. 보유자는 이미 선택한 선행청구 가족의 CHI다. 다른 팀 동률·로터리 추첨·시리즈 승자는 이 계산의 선행조건이 아니다.

- [검문한 순위·플레이인](../simulation/NBA_2022_23_STANDINGS_AND_2023_PLAYIN.md)
- [명명 보유청구](CHICAGO_2023_NAMED_DRAFT_CLAIMS_AND_COST_PORTS_2026_10_08.md)
- [원 NBA By-Laws](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf) PDF86/인쇄77 §7.02(a)(iii): 진출팀 정규 순위 역순. 기존 raw와 본문을 직접 읽었다.
- [현행 NBA FAQ](https://cdn-uat.nba.com/news/nba-draft-faq): 동일 규칙의 보조 대조이며 2023 원출간이라고 주장하지 않는다.

실제2023 Chicago 역사 순번이 아니다. 새 신인 STD 1칸의 순번을 정했으며 선수·RSC가격/N23·A23는 아직 미선택이다. null≠0, 전체60청구·총비용 인증0. 원고0/CLOSED.
'''

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');a=ap.parse_args();v=build();m=md(v)
 if a.write:
  (ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/OUT[:-5]).with_suffix('.md').write_text(m,encoding='utf-8')
 if a.check:need(read(OUT)==v,'Slot output stale');need(norm((ROOT/OUT[:-5]).with_suffix('.md'))==m,'Slot MD stale')
 print(json.dumps({'CHI_origin_first_slot':v['Chicago_origin_first_slot'],'draft_price_selected':False}))
