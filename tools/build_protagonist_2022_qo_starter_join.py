"""Join selected fictional credited regular clocks to the 2017 CBA QO branch."""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_protagonist_2022_qo_starter_join.py'
OUT = 'simulation/PROTAGONIST_2022_QO_STARTER_JOIN.json'
MD = OUT[:-5] + '.md'
GLOBAL = 'simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json'
PEER = 'reviews/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS_G11_INDEPENDENT_REVIEW_2026_10_07.json'
FAMILY = 'research/CHICAGO_2022_ROOKIE_RFA_QO_FAMILY_2026_10_07.json'
CARRIER = 'simulation/CHICAGO_2022_SELECTED_CORE_CONTRACT_CARRIER.json'
AUTH = 'reviews/MACRO3_FINITE_EXIT_AND_CORE_ROUTINE_AUTHORITY_AUDIT_2026_10_07.md'
PINS = {
 GLOBAL:'93264d2dff86a58ad10ca6975315c6c2167961f94f2517b6f5f79fa3113f2af8',
 PEER:'b79289283b05c01a7d55ef362032071a5b4b07a15da572c50fb1ab93adcc0443',
 FAMILY:'ceac38803f42eabff9032023a20ddbbcd1f739d4831a22fcba6e62fea096a14d',
 CARRIER:'cc586a6f801a1e61d60bd9eddbe0e8bfa57415963c2d0d76669683a690551d6c',
 AUTH:'22e422447f84051a18ffdfcef710f90d54c2bc7dc6d30fc9447936930646a83a',
}

def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def h(p):return sha256(text(p).encode()).hexdigest()
def load(root,p):return json.loads(text(root/p))
def need(ok,msg):
 if not ok:raise ValueError(msg)

def regular_sum(g):
 rows=[q for q in g['rows'] if 'CHI' in q['team_date_models']]
 need(len(rows)==82 and len({q['game_id'] for q in rows})==82,'CHI82 domain')
 totals=Counter();states=Counter();dated=[]
 for q in rows:
  m=q['team_date_models']['CHI'];blocks=g['shared_role_templates'][m['template']]['blocks']
  per=Counter();end=0
  for b in blocks:
   need(b['start_second']==end and end<b['end_second']<=2880,'Regular clock partition')
   ps=b['positions'];need(set(ps)=={'PG','SG','SF','PF','C'} and len(set(ps.values()))==5,'Five distinct roles')
   for p in ps.values():per[p]+=b['end_second']-end
   end=b['end_second']
  need(end==2880 and sum(per.values())==14400 and dict(per)==m['positive_player_seconds'],'Raw block/declared seconds join')
  need(per['Protagonist']==1920 and set(per)<=set(m['active']),'Bound P32 and active membership')
  totals.update(per);states[m['state']]+=1
  dated.append({'game_id':q['game_id'],'date':q['date'],'selected_regular_P_seconds':per['Protagonist']})
 need(states==Counter(NORMAL=58,COBY_OUT=24),'Prior health family preserved')
 return totals,dated

def build(root=ROOT):
 for p,pin in PINS.items():need(h(root/p)==pin,'Physical frozen source: '+p)
 src={p:load(root,p) for p in (GLOBAL,PEER,FAMILY,CARRIER)}
 for p,value in src.items():need(value==json.loads(text(root/p)),'Returned source differs from physical frozen input: '+p)
 g,peer,f,carrier=(src[p] for p in (GLOBAL,PEER,FAMILY,CARRIER))
 need(peer['independent_review_completed'] and peer['source_sha256'][GLOBAL]==PINS[GLOBAL],'Global independent acceptance')
 need(f['policy']['original_salary_cap_year']=='2018-19' and f['policy']['protagonist_pick_domain']==list(range(16,31)) and f['policy']['no2021_extension_branch'],'Fourth RSC season and late-pick family')
 events={q['date']:q['action'] for q in carrier['selected_working_events']}
 need('Coby fourth-year' in events['2021-10-01'] and 'LaMelo third-year' in events['2021-10-01'],'Original option seasons')
 need('Issue timely ordinary protagonist QO' in events['2022-06-29'] and 'unaccepted before E2' in events['2022-06-29'],'Original June29 ordinary offer and unaccepted state')
 need('E2 directBird4' in events['2022-07-07'],'Original July7 E2')
 forms=carrier['selected_working_forms']
 need(forms['Protagonist']['id']=='E2' and forms['Carter']['id']=='CX1' and not forms['Carter']['2022_QO_RFA_or_FAhold_arises_if_extension_is_actually_implemented'],'Selected E2/CX1 applicability')
 c=f['sources']['2017_CBA'];cache=Path(c['cache_path'])
 need(sha256(cache.read_bytes()).hexdigest()==c['raw_sha256'],'2017 CBA bytes')
 with fitz.open(cache) as book:
  page={n:book[n-1].get_text() for n in (310,311,314)}
 joined=' '.join((page[310]+page[311]).split())
 need('fourth Season' in joined and 'two thousand (2,000)' in joined and 'no bonuses of any kind' in joined and 'ninth player' in joined,'XI1c(ii)(A) anchors')
 need('Official NBA statistics' in ' '.join(page[314].split()),'Official credited-stat boundary')
 totals,dated=regular_sum(g);minutes=Fraction(totals['Protagonist'],60)
 need(minutes==2624 and totals['Coby']==62640,'Selected lower bound changed')
 starter=minutes>=2000;need(starter,'Fourth-year MIN branch fails')
 selected=[deepcopy(q) for q in f['branch_rows'] if q['player']=='Protagonist' and q['starter']]
 need(len(selected)==15 and {q['pick'] for q in selected}==set(range(16,31)) and all(q['rule']=='XI1c(ii)(A)_PICK9_BASE_ONLY' for q in selected),'Late-pick starter component branch')
 return {'id':'PROTAGONIST_2022_QO_STARTER_JOIN','classification':'SELECTED_FICTIONAL_CREDITED_STAT_JOIN_NOT_REAL_NBA_CERTIFICATE','source_sha256':{**PINS,SELF:h(root/SELF)},'sources':{'2017_CBA':{'url':c['url'],'cache_path':str(cache),'raw_sha256':c['raw_sha256'],'pages':[{'PDF_1based':n,'text_LF_sha256':sha256(t.replace('\r\n','\n').encode()).hexdigest()}for n,t in page.items()]}},'routine_selection':{'authority':AUTH,'official_credited_stat_model':'All physically selected Chicago regular seconds are credited in the fictional NBA regular-season statistics; unselected OT/additional credited minutes nonnegative. No claim about real-world NBA data.','original_RSC_cap_year':'2018-19','fourth_RSC_regular_season':'2021-22','fourth_year_minutes_lower_bound':2624,'unknown_additional_minutes_domain':'[0,+infinity)','starter_criteria_selected':True,'sufficient_OR_branch':'MIN4 >= 2000','starts_order_or_exact_OT_selected':False},'dated_regular_witnesses':dated,'selected_QO_component_family':{'late_pick_domain':list(range(16,31)),'exact_protagonist_original_pick':None,'rank9_base_only_exact_legal_input':deepcopy(f['anchors']['rank9']['base_only_exact']),'likely_bonus':0,'unlikely_bonus':0,'conservative_usd_screen':f['anchors']['rank9']['single_component_screen_upper_usd'],'actual_USD_or_rounding_algorithm_certified':False},'prior_execution_join':{'carrier':CARRIER,'June29_ordinary_QO_family_refined_without_new_offer':True,'QO_unaccepted_before_selected_July7_E2':True,'selected_E2_price_duration_roster_or_cost_changed':False,'Carter_CX1_selected_live_extension_no_new_Carter_QO':True},'Coby_boundary':{'selected_2021_22_regular_minutes':1044,'RSC_year':3,'2022_23_fourth_year_or_starter_selected':False,'nonstarter_from_lower_bound_inferred':False},'certification':{'P2022_working_starter_branch_closed':True,'real_official_GP_GS_total_minutes_or_medical_certified':False,'actual_QO_issue_delivery_or_acceptance_certified':False,'new_price_author_lock_or_title_selected':False,'independent_review_completed':False,'whole_macro3_G13_G14_or_manuscript':False},'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}

def validate(v,root=ROOT):return [] if v==build(root) else ['Saved starter join differs from physical source/selected credit boundary']
def markdown(v):return '''# 주인공 2022 QO starter 분기 연결

원2018–19 RSC의4년차2021–22에 Chicago82개의 실제 저장 블록을 합산하면157,440초=2,624분이다. 원CBA XI1c(ii)(A)(PDF310–311)의4년차2,000분 OR분기를 충족한다. 전체 선발횟수·OT를 새로 정할 필요가 없다.

**가상 공식통계 계상 선택**: 원모델의 정규시간이 작업세계 NBA 통계에 계상되고, 추가시간은0이상인 가족을 루틴 선택한다. CBA PDF314의 Official NBA statistics 요건을 모델값만으로 실제NBA인증한 것이 아니다. 실 GP/GS·임상·영수증은 미확인이다.

주인공 원pick16–30 전부는9번120% 법정 기본급함수·bonus0의 같은 starter QO 가지다. 원 June29 유효QO→미수락→July7 E2를 연결한다. 정확원pick·달러 반올림·실제발행·수락을 확정하지 않으며 E2 가격/기간/15+2/원비용을 바꾸지 않는다. Carter는선택CX1연장이라 새QO를추가하지않는다.

Coby1,044분은3년차 모델의 하한이며4년차/2년합·선발은미정이다. nonstarter 판정에 쓸 수 없다.

[현재 인계](../canon/NBA_CAREER_CURRENT_EXECUTION_2026_10_08.md) · [원QO함수](../research/CHICAGO_2022_ROOKIE_RFA_QO_FAMILY_2026_10_07.md) · [선택코어](CHICAGO_2022_SELECTED_CORE_CONTRACT_CARRIER.md) · [현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md).

미완료5묶음/6번까지4. v0.30 PARTIAL·설계/원고 CLOSED·원고0·실제Pack0. 작성자검사는독립감리로계수하지않는다.
'''

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if a.check:need(load(ROOT,OUT)==v and text(ROOT/MD)==markdown(v),'Saved join stale')
 print(json.dumps({'current':True,'P_regular_minutes':2624,'working_starter_branch':True,'Coby_nonstarter_certified':False}))
if __name__=='__main__':main()
