"""Dispatch the selected Chicago82 dates without carrying last year's NPC contracts."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import argparse,csv,io,json
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_23_chicago_paired_dispatch.py'
OUT='simulation/CHICAGO_2022_23_PAIRED_DATE_DISPATCH.json'
MD=OUT[:-5]+'.md'
CHI='simulation/CHICAGO_2022_23_SELECTED_DATED_ROLES.json'
PEER='reviews/CHICAGO_2022_23_SELECTED_DATED_ROLES_G11_INDEPENDENT_REVIEW_2026_10_08.json'
PRIOR='simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json'
CAL='simulation/CHICAGO_2022_23_PUBLISHED_CALENDAR.csv'
PROV='simulation/NBA_2022_23_PUBLISHED_CALENDAR_PROVENANCE.json'
AUTH='control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md'
PINS={CHI:'c0650dbb07b75cc1523bf7ccc7f658576ac5b9a8784f1e80cc97178897703170',PEER:'bf867086e367fc90bf851c00cce2ac620e968b32c4a3ebc390a2e36b39a4e4e0',PRIOR:'93264d2dff86a58ad10ca6975315c6c2167961f94f2517b6f5f79fa3113f2af8',CAL:'bd78708fb1d58e4decede3723bd14829863d395366d30d202565e3c7f7729f4b',PROV:'b0ed4235d17653b1272636f8197cb9eca3daacc1e279a157376f9ae227496e78',AUTH:'91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d'}
def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def h(p):return sha256(text(p).encode()).hexdigest()
def physical():
 for p,pin in PINS.items():assert h(p)==pin,'Physical source changed '+p
 return {p:json.loads(text(p)) for p in [CHI,PEER,PRIOR,PROV]}
def inputs():return physical()
def dates(s):
 c=list(csv.DictReader(io.StringIO(text(CAL))))
 assert len(c)==82 and len({x['calendar_key']for x in c})==82
 assert s[CHI]['summary']['executed_H22_date_selections']==82 and s[CHI]['summary']['results_selected']==0
 assert s[PEER]['independent_review_completed']
 for p,pin in s[PEER]['source_sha256'].items():assert h(p)==pin,'Current selected-role peer stale '+p
 assert s[PROV]['derived_text_sha256'][CAL]==h(CAL)
 for a,b in zip(c,s[CHI]['dated_rows']):
  assert all(a[k]==b[k]for k in ['published_date','calendar_key','home','away','opponent'])
  assert b['working_date_adopted'] and b['H22_state_selected_for_date']
 return c
def opponent_ports(s,c):
 old=s[PRIOR];freq=Counter(x['opponent']for x in c);result=[]
 for team in sorted(freq):
  keys=sorted(k for k,v in old['shared_role_templates'].items()if v['team']==team)
  assert keys,'Missing predecessor references '+team
  ds=[x['published_date']for x in c if x['opponent']==team]
  result.append({'team':team,'Chicago_fixture_count':freq[team],'first_required_date':min(ds),'last_required_date':max(ds),
   'predecessor_role_keys_reference_only':keys,'predecessor_input_salary_capyear':2021,'required_input_salary_capyear':2022,
   'predecessor_UPC_health_clock_productivity_or_winner_automatically_adopted':False,
   'named_roster_contract_and_retained_obligations_family':None,'new_FY22_availability_and_nomination_policy':None,
   'new_FY22_regulation_clock_and_productivity_inputs':None,'current_FY22_peer_acceptance':None,
   'working_admission':'NOT_ADMITTED_FOR_2022_23','paired_results_ready':False,
   'new_2023_draft_N23_A23_required_for_these_regular_dates':False,
   'scope':'A source-pinned lawful fictional operating family must cover these dates; actual private receipts or clinical histories are not certification requirements.'})
 return result
def dispatch(s,c,ports):
 by={x['team']:x for x in ports};rows=[]
 for i,x in enumerate(c,1):
  rows.append({'team_game_number':i,'date':x['published_date'],'calendar_key':x['calendar_key'],'home':x['home'],'away':x['away'],'opponent':x['opponent'],
   'selected_Chicago_role_pointer':CHI+'#/selected_role_template','selected_Chicago_date_pointer':CHI+'#/dated_rows/'+str(i-1),
   'current_Chicago_registered_STANDARD':15,'current_Chicago_registered_TWO_WAY':2,'Chicago_active_STANDARD':12,
   'Chicago_regulation_seconds':2880,'Chicago_player_seconds':14400,
   'opponent_input_port':OUT+'#/opponent_ports/'+str(ports.index(by[x['opponent']])),
   'new_opponent_roster_family':None,'new_opponent_role_clock':None,'new_opponent_productivity':None,
   'simultaneous_paired_clock':None,'working_regulation_winner':None,'actual_score_or_OT':None,
   'paired_result_ready':False,'old_2021_22_result_copied':False,
   'post_D23_N23_A23_is_dependency':False})
 return rows
def guard(s,c,ports,rows):
 assert s==physical(),'Returned source differs from independent physical parse'
 assert c==list(csv.DictReader(io.StringIO(text(CAL)))),'Returned calendar differs from physical CSV'
 for x,y in zip(c,s[CHI]['dated_rows']):
  assert all(x[k]==y[k]for k in ['published_date','calendar_key','home','away','opponent']),'Returned calendar differs from selected Chicago date'
 freq=Counter(x['opponent']for x in c)
 assert [x['team']for x in ports]==sorted(freq)
 for x in ports:
  ds=[d['published_date']for d in c if d['opponent']==x['team']]
  assert x['Chicago_fixture_count']==freq[x['team']] and x['first_required_date']==min(ds) and x['last_required_date']==max(ds)
  assert x['predecessor_role_keys_reference_only']==sorted(k for k,v in s[PRIOR]['shared_role_templates'].items()if v['team']==x['team'])
  assert x['predecessor_input_salary_capyear']==2021 and x['required_input_salary_capyear']==2022
  assert x['predecessor_UPC_health_clock_productivity_or_winner_automatically_adopted']is False
  assert x['working_admission']=='NOT_ADMITTED_FOR_2022_23' and x['paired_results_ready']is False
  assert all(x[k]is None for k in ['named_roster_contract_and_retained_obligations_family','new_FY22_availability_and_nomination_policy','new_FY22_regulation_clock_and_productivity_inputs','current_FY22_peer_acceptance'])
  assert x['new_2023_draft_N23_A23_required_for_these_regular_dates']is False
 for i,(x,d)in enumerate(zip(rows,c)):
  assert x['team_game_number']==i+1 and x['date']==d['published_date']
  assert all(x[k]==d[k]for k in ['calendar_key','home','away','opponent'])
  assert x['selected_Chicago_role_pointer']==CHI+'#/selected_role_template'
  assert x['selected_Chicago_date_pointer']==CHI+'#/dated_rows/'+str(i)
  pi=next(n for n,p in enumerate(ports)if p['team']==d['opponent'])
  assert x['opponent_input_port']==OUT+'#/opponent_ports/'+str(pi)
  assert (x['current_Chicago_registered_STANDARD'],x['current_Chicago_registered_TWO_WAY'],x['Chicago_active_STANDARD'],x['Chicago_regulation_seconds'],x['Chicago_player_seconds'])==(15,2,12,2880,14400)
  assert all(x[k]is None for k in ['new_opponent_roster_family','new_opponent_role_clock','new_opponent_productivity','simultaneous_paired_clock','working_regulation_winner','actual_score_or_OT'])
  assert x['old_2021_22_result_copied']is False
 assert len(ports)==29 and sum(x['Chicago_fixture_count']for x in ports)==82
 assert len(rows)==82 and sum(x['home']=='CHI'for x in rows)==sum(x['away']=='CHI'for x in rows)==41
 assert [x['team_game_number']for x in rows]==list(range(1,83))
 assert rows[0]['date']=='2022-10-19' and rows[-1]['date']=='2023-04-09'
 assert all(x['date']<'2023-06-01' for x in rows)
 assert all(x['paired_result_ready']is False and x['post_D23_N23_A23_is_dependency']is False for x in rows)
def build():
 s=inputs();assert s==physical();c=dates(s);ports=opponent_ports(s,c);rows=dispatch(s,c,ports);guard(s,c,ports,rows)
 return {'id':'CHICAGO_2022_23_PAIRED_DATE_DISPATCH','baseline_main':'31e424c1662f5fa03c2a27c9d0b3a88f8c420a78',
  'status':'CURRENT_CHICAGO_82_DISPATCH_29_OPPONENT_PORTS_READY_NO_PAIRED_RESULTS',
  'source_sha256':{**PINS,SELF:h(SELF)},'opponent_ports':ports,'rows':rows,
  'summary':{'working_Chicago_dates':82,'opponent_teams':29,'selected_Chicago_side_roles':82,'home_dates':41,'away_dates':41,'unadmitted_opponent_team_ports':29,'paired_clocks':0,'paired_regulation_results':0,'post_D23_prices_required_for_pre_D23_regular_results':0},
  'execution_order':['Cover actual required regular dates with named lawful FY22 NPC operating families and retained obligations; reuse proven rules, do not silently carry FY21 terms','Select new FY22 availability/nomination and source or explicitly fictional productivity inputs; no automatic future NBA performance copy','Join the two ordered2880second clocks, verify unique current owners and five positions, then compute regulation result','Resolve OT/stat credit inputs separately; regular results need no later D23 price before their own dates'],
  'boundaries':{'existing_2021_22_1230_and_2022_PO_draft_or_Chicago_roster_changed':False,'prototype_is_new_fiscal_year_admission':False,'same_clinical_or_NYC_legal_ban_imported':False,'actual_registration_clinical_private_price_or_box_certificate':False,'new_NPC_UPC_Tender_or_title_selected':False,'whole_macro3_G13_or_context_pack_complete':False},
  'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}
def markdown(v):
 lines=['# Chicago2022–23 양팀 날짜 입력 연결','','기존 H22/Chicago82작업날짜를 현재 source 지문과 함께 연결한다. 원2021–22 상대 시계는 이전연도 참고만이며 새2022–23 계약·명단·건강·승패로 상속하지 않는다.','','| 범위 | 현재 |','|---|---|','| Chicago 역할/발표 작업날짜 | 82 |','| 상대팀 입력 포트 | 29 |','| 양팀 시계/규정시간 결과 | 0/82 |','| 이후D23가격을 정규경기 선행요건으로 추가 | 0 |','','## 유한 상대별 범위','','| 상대 | 경기수 | 첫 필요 날짜 | 마지막 필요 날짜 |','|---|---:|---|---|']
 for x in v['opponent_ports']:lines.append(f"| {x['team']} | {x['Chicago_fixture_count']} | {x['first_required_date']} | {x['last_required_date']} |")
 lines+=['','29팀 각각은 필요한 날짜까지를 덮는 명명된 적법 가상운영 가족·원채무·새가용/active·240분/생산성 입력과 현재peer가 필요하다. 모든 실제비공개 UPC/접수/임상 증명을 새요건으로 요구하지 않는다. 루틴계약·운영은 기존위임 안에서 검문 후 선택할 수 있으며 중요한 코어/장기방향충돌만 별도 처리한다.','','정규말단4/9보다 뒤의2023드래프트N23/A23가null이라는 이유로 앞82결과를 막지 않는다. 이는 뒤 비용을0으로 둔다는 뜻도, 실제FY22전체계약/결과가 끝났다는 뜻도 아니다. OT/가상공식credit/QO/2023CBA후속은 각사용시점에서 별도로 검문한다.','','[선택 Chicago 역할](CHICAGO_2022_23_SELECTED_DATED_ROLES.md) · [공식 발표일정 근거](NBA_2022_23_PUBLISHED_CALENDAR_PROVENANCE.md) · [이전 전역 결과](NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.md)','','미완료큰묶음5/6번까지4 · v0.30 PARTIAL · CLOSED · Pack0 · 원고0.','']
 return '\n'.join(lines)
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if a.check:assert json.loads(text(OUT))==v and text(MD)==markdown(v)
 print(json.dumps({'current':True,**v['summary']}))
if __name__=='__main__':main()
