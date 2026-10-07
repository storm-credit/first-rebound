"""Select a bounded delegated fictional first round after reviewed seed7.

No historical winners, scores, new contracts, MVP or championship selection.
Regular-season productivity is a finite story model, never a calibrated forecast.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
from copy import deepcopy
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_phi_2022_first_round.py'
OUT='simulation/CHICAGO_PHI_2022_FIRST_ROUND.json';MD=OUT[:-5]+'.md'
GLOBAL='simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json'
SEED='simulation/NBA_2021_22_STANDINGS_PLAYIN_AND_2022_RIGHTS.json'
GP='reviews/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS_G11_INDEPENDENT_REVIEW_2026_10_07.json'
SP='reviews/NBA_2021_22_STANDINGS_PLAYIN_AND_2022_RIGHTS_G11_INDEPENDENT_REVIEW_2026_10_07.json'
AUTH='control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md'
PINS={GLOBAL:'93264d2dff86a58ad10ca6975315c6c2167961f94f2517b6f5f79fa3113f2af8',SEED:'139c1d6a90d1bd7ee672020af96e03bf6767599637902c329b1e772fdfcf63d9',GP:'b79289283b05c01a7d55ef362032071a5b4b07a15da572c50fb1ab93adcc0443',SP:'db60e3b8f894bf59cc7b4619b9be5f34bef7203753c9856b5b7bb0667232fe1b',AUTH:'91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d'}
DAYS=('2022-04-16','2022-04-18','2022-04-21','2022-04-23','2022-04-25','2022-04-28','2022-04-30')
HOME=('PHI','PHI','CHI','CHI','PHI','CHI','PHI')
POLICY={'selected_chicago_state':'NORMAL','PHI_state':'NORMAL','scope':'NEW_AUTHOR_DELEGATED_DESIGN_SELECTION_FIRST_SERIES_ONLY','Coby_normal_positive_role_from':'2022-04-16','no_new_contact_injury_modeled':True,'existing_UPCs_Gamma_and_obligations_preserved_in_same_salary_year':True,'no_new_contract_waiver_trade_or_TW_conversion':True,'standard_only_postseason_participants':True,'constant_regular_productivity_and_existing_roles_reused_as_explicit_new_model':True,'home_advantage_fraction':'2','variance_or_tactical_efficiency_change_selected':False,'actual_clinical_clearance_and_receipts_certified':False,'championship_or_MVP_selected':False}
FIXED=deepcopy(POLICY)
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def h(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(root,p):return json.loads(text(root/p))if p.endswith('.json')else text(root/p)
def sources(root):
 assert POLICY==FIXED,'Selected first-series policy changed'
 out={}
 for p,pin in PINS.items():
  assert h(root/p)==pin,'Source changed '+p
  v=load(root,p);expected=json.loads(text(root/p))if p.endswith('.json')else text(root/p)
  assert v==expected,'Returned source differs from physical '+p;out[p]=v
 assert out[GP]['independent_review_completed']and out[SP]['independent_review_completed']
 for review in [out[GP],out[SP]]:
  for p in [GLOBAL,SEED]:
   if p in review['source_sha256']:assert review['source_sha256'][p]==PINS[p]
 return out
def clock(v):
 end=0;totals=Counter();roles=Counter()
 for b in v['blocks']:
  assert b['start_second']==end and b['end_second']>end
  p=b['positions'];assert set(p)=={'PG','SG','SF','PF','C'}and len(set(p.values()))==5
  n=b['end_second']-end
  for role,person in p.items():totals[person]+=n;roles[role]+=n
  end=b['end_second']
 assert end==2880 and sum(totals.values())==14400 and set(roles.values())=={2880}
 assert dict(totals)==v['positive_player_seconds']and set(totals)<=set(v['active'])<=set(v['registration']['standard'])
 assert 12<=len(v['active'])<=15 and not(set(v['active'])&set(v['registration']['TW']))
 return totals
def series(g,state,advantage=Fraction(2)):
 models={t:deepcopy(g['shared_role_templates'][t+':'+(state if t=='CHI'else'NORMAL')])for t in ['CHI','PHI']}
 assert len(set(models['CHI']['registration']['standard'])&set(models['PHI']['registration']['standard']))==0
 impacts={t:sum(Fraction(g['selected_productivity_inputs'][p]['fraction'])*n/2880 for p,n in clock(v).items())for t,v in models.items()}
 counts=Counter();rows=[]
 for i,(day,home)in enumerate(zip(DAYS,HOME),1):
  if max(counts.values(),default=0)==4:break
  away='CHI'if home=='PHI'else'PHI';margin=impacts[home]-impacts[away]+advantage
  assert margin!=0
  winner=home if margin>0 else away;counts[winner]+=1
  rows.append({'id':f'ALT2022:E:R1:PHI-CHI:G{i}','date':day,'game_number':i,'home':home,'away':away,'home_impact_fraction':str(impacts[home]),'away_impact_fraction':str(impacts[away]),'home_advantage_fraction':str(advantage),'back_to_back_fatigue_fraction':'0','exact_home_proxy_margin':str(margin),'selected_regulation_winner':winner,'series_wins_after_game':dict(counts),'team_template_keys':{'CHI':'CHI:'+state,'PHI':'PHI:NORMAL'},'score':None,'overtime':None,'physical_NBA_game_id':None,'historical_winner_used':False})
 assert max(counts.values())==4 and 4<=len(rows)<=7
 return {'Chicago_state':state,'home_advantage_fraction':str(advantage),'winner':max(counts,key=counts.get),'wins':dict(counts),'games':rows,'team_models':models,'weighted_impacts':{t:str(v)for t,v in impacts.items()}}
def assert_series(v,g,state,advantage):
 # Check returned meanings against original source, never another series() call.
 models={t:g['shared_role_templates'][t+':'+(state if t=='CHI'else'NORMAL')]for t in ['CHI','PHI']}
 assert v['team_models']==models,'Returned series template/STD/TW/clock altered'
 impacts={t:sum(Fraction(g['selected_productivity_inputs'][p]['fraction'])*n for p,n in q['positive_player_seconds'].items())/2880 for t,q in models.items()}
 assert v['weighted_impacts']=={t:str(q)for t,q in impacts.items()}
 counts=Counter();expected=[]
 for i,(day,home)in enumerate(zip(DAYS,HOME),1):
  if max(counts.values(),default=0)==4:break
  away='CHI'if home=='PHI'else'PHI';m=impacts[home]-impacts[away]+advantage;assert m!=0
  win=home if m>0 else away;counts[win]+=1
  expected.append({'id':f'ALT2022:E:R1:PHI-CHI:G{i}','date':day,'game_number':i,'home':home,'away':away,'home_impact_fraction':str(impacts[home]),'away_impact_fraction':str(impacts[away]),'home_advantage_fraction':str(advantage),'back_to_back_fatigue_fraction':'0','exact_home_proxy_margin':str(m),'selected_regulation_winner':win,'series_wins_after_game':dict(counts),'team_template_keys':{'CHI':'CHI:'+state,'PHI':'PHI:NORMAL'},'score':None,'overtime':None,'physical_NBA_game_id':None,'historical_winner_used':False})
 assert v['games']==expected and v['wins']==dict(counts)and v['winner']==max(counts,key=counts.get),'Returned series calendar/winner/arithmetic altered'
 assert v['Chicago_state']==state and v['home_advantage_fraction']==str(advantage)
def build(root=ROOT):
 src=sources(root);g=src[GLOBAL];s=src[SEED]
 assert g['summary']['league_games']==1230 and g['summary']['CHI_wins']==52
 east={x['seed']:x['team']for x in s['final_playoff_seeds']['EAST']}
 assert east[2]=='PHI'and east[7]=='CHI'
 assert g['team_records']['PHI']['wins']==65>g['team_records']['CHI']['wins']==52
 selected=series(g,POLICY['selected_chicago_state'])
 assert_series(selected,g,POLICY['selected_chicago_state'],Fraction(2))
 comparison=[]
 for state in ['NORMAL','COBY_OUT']:
  for adv in [Fraction(0),Fraction(1),Fraction(2),Fraction(3)]:
   v=series(g,state,adv);assert_series(v,g,state,adv);assert v['winner']=='PHI'
   comparison.append({'Chicago_state':state,'home_advantage_fraction':str(adv),'winner':v['winner'],'series_wins':v['wins'],'game_count':len(v['games']),'selected_family':state=='NORMAL'and adv==2})
 assert len(selected['games'])==7 and selected['wins']=={'PHI':4,'CHI':3}
 assert [x['selected_regulation_winner']for x in selected['games']]==['PHI','PHI','CHI','CHI','PHI','CHI','PHI']
 return {'id':'CHICAGO_PHI_2022_FIRST_ROUND','classification':'AUTHOR_DELEGATED_FICTIONAL_FIRST_SERIES_SELECTION_PENDING_INDEPENDENT_REVIEW','baseline_main':'bebabcf65be6af0d73d39b5a290249de52952397','source_sha256':{**PINS,SELF:h(root/SELF)},'new_policy':deepcopy(POLICY),'selected_series':selected,'eight_compared_health_and_home_families':comparison,'selection_reason':'Select normal positive availability fromApr16 as a new bounded fictional role return. Compared continuationCOBY_OUT and home0/1/2/3 all retain PHI serieswinner; normal preserves Coby development/participation without a new long injury. Length4/7 is model-sensitive. No medical fact inferred from regular played/missing rows.','primary_format_observation':{'URL':'https://cdn.nba.com/teams/uploads/sites/1610612760/2022/12/mediaguide-202223.pdf','PDF_1based':56,'locator':'2022 NBA playoff structure; Best of Seven and2-2-1-1-1','web_reference':'turn2355view0 lines6981–6992','raw_file_bytes_certified_by_this_tool':False,'outdated_2023_division_seeding_note_adopted':False},'calendar_classification':'NEW_FICTIONAL_SERIES_CALENDAR_WITHIN_ORIGINAL_APR16_PLAYOFF_START; not copied physical CHI/PHI schedule. Dates separated >=2days; Jun30 salary year/UPCs preserved.','team_legal_participation':'Existing selected standard UPC/obligation families include same2021–22 postseason; no new money/contract/two-way participation. Actual private consent/medical/active sheets not certified.','Chicago_eliminated_date':'2022-04-30','next_Chicago_career_consumer':'2022 draft rights18/57 and unchanged July7E2/CX1/FY22 retained core; playoff minutes are not added to regular-season QO starter criteria.','summary':{'games':7,'team_dates':14,'regulation_minutes_per_team_per_game':240,'CHI_selected_wins':3,'PHI_selected_wins':4,'P_additional_playoff_regulation_minutes':7*32,'regular_QO_2624_lower_bound_unchanged':True,'source_regular_1230_and_six_playin_changed':False},'limits':{'fixed_productivity_not_calibrated_game_or_series_probability':True,'home_margin_not_actual_score_margin':True,'new_contacts_actual_clinical_or_receipts_certified':False,'new_playoff_growth_or_tactical_efficiency_certified':False,'global_remaining_fourteen_series_or_champion_selected':False,'new_title_count_MVP_year_or_franchise_choice':False,'independent_review_completed':False,'root_adoption_recorded':False,'whole_macro3_G13_G14_or_manuscript':False},'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}
def markdown(v):
 lines=['# Chicago–Philadelphia · 2022 첫 라운드 작업 선택','','새 위임 설계 가족: Chicago는4월16일부터 NORMAL 양수역할을 선택한다. 원play-in의COBY_OUT과 regular58/24 입력은 보존한다. 실제 임상복귀·접수·경기 결과를 인증하지 않는다.','','원선택65승PHI 동부2와52승CHI PO7을연결한다. 가상calendar/best7·2-2-1-1-1·등록STD만/각240분·기존분수BPM+home2를사용해PHI4–3/CHI4월30탈락을선택했다. 고정생산성 모델이며정밀예측·실제점수차가아니다. 독립검문전이다.','','| 경기 | 가상 날짜 | 홈 | 작업 승자 |','|---|---|---|---|']
 lines += [f"| {q['game_number']} | {q['date']} | {q['home']} | {q['selected_regulation_winner']} |"for q in v['selected_series']['games']]
 lines += ['','NORMAL/COBY_OUT×home0/1/2/3의8가족에서PHI시리즈승자는같고기간은4/7경기로달라진다. 정상역할을선택하되승자불변을건강의실제정답으로읽지않는다. Coby OUT이BPM합은더높아도경기대응·개발·임상우위를증명하지않는다.','','주인공선택PO분224는regular2,624분QO기준에더하지않는다. 기존E2/CX1·June29 QO/July7·가격/15+2를바꾸지않는다. 남은14시리즈·리그우승자·2022신인과2022–23/2023후속은별도미완료이다.','','[원시드](NBA_2021_22_STANDINGS_PLAYIN_AND_2022_RIGHTS.md) · [후속계약](PROTAGONIST_2022_QO_STARTER_JOIN.md)','','미완료큰묶음5/6번까지4·v0.30 PARTIAL·CLOSED·Pack0·원고0。','']
 return '\n'.join(lines)
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if a.check:assert load(ROOT,OUT)==v and text(ROOT/MD)==markdown(v),'Saved first series stale'
 print(json.dumps({'current':True,'games':7,'CHI_wins':3,'PHI_wins':4,'comparisons':8}))
if __name__=='__main__':main()
