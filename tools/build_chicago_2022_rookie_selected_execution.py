"""Select reviewed routine draft/rookie family; keep original candidates immutable."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from datetime import datetime,timedelta
import argparse,json
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_rookie_selected_execution.py'
OUT='simulation/CHICAGO_2022_ROOKIE_SELECTED_EXECUTION.json';MD=OUT[:-5]+'.md'
BOARD='research/NBA_2022_FULL_DRAFT_WORKING_BOARD_2026_10_08.json'
BP='reviews/NBA_2022_FULL_DRAFT_WORKING_BOARD_G11_INDEPENDENT_REVIEW_2026_10_08.json'
CHOICE='design/CHICAGO_2022_ROOKIE_EXECUTION_CHOICE.json'
CP='reviews/CHICAGO_2022_ROOKIE_EXECUTION_CHOICE_G11_INDEPENDENT_REVIEW_2026_10_08.json'
WINDOW='simulation/CHICAGO_2022_23_NAMED_CONTRACT_WINDOW.json'
WP='reviews/CHICAGO_2022_23_NAMED_CONTRACT_WINDOW_G11_INDEPENDENT_REVIEW_2026_10_08.json'
AUTH='control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md'
PINS={BOARD:'3bdad52ebaacda5abb23b9908b8ed3a9b85cfaa09d838819a959cd024a58e940',BP:'a1773813ee7c82b562ef9eddac2a31846c08600912f79f4f20c6162ec6477df6',CHOICE:'e5f46f2af0aeff3a624247708210b7f951c3340cfbdbddcfd1781a8818bc9c93',CP:'b616be2abc5b3866429f6ec1356db137e4b18c8172c62e89f6d8f84593df101e',WINDOW:'21e860056c2654d5e4837911dac39e7f45f4d26388d353bc57594afefcecf1f4',WP:'fe12a16eb1a4abcb3a78fe1258ab8bcec3e702e58ec5710ee8ab71160f2539a2',AUTH:'91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d'}
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def h(p):return sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(ROOT/p))if p.endswith('.json')else text(ROOT/p)
def physical(p):return json.loads(text(ROOT/p))if p.endswith('.json')else text(ROOT/p)
def inputs():
 s={}
 for p,pin in PINS.items():
  assert h(ROOT/p)==pin,'Physical source changed '+p
  v=load(p);assert v==physical(p),'Returned source differs from independent physical parse '+p;s[p]=v
 for p in [BP,CP,WP]:
  assert s[p]['independent_review_completed']
  for q,pin in s[p]['source_sha256'].items():assert h(ROOT/q)==pin,'Peer source stale '+q
 return s
def selected_board(b):
 rows=[]
 for i,x in enumerate(b['rows'],1):
  y=deepcopy(x)
  y['execution_class']='AUTHOR_DELEGATED_ROUTINE_WORKING_DRAFT_SELECTION'
  y['fictional_legal_participation_conditions_selected']=True
  y['actual_private_papers_or_NBA_physical_selection_certified']=False
  y['source_candidate_pointer']=BOARD+'#/rows/'+str(i-1)
  rows.append(y)
 return rows
def guard_board(rows,b):
 assert len(rows)==60 and len({x['player']for x in rows})==60
 for i,(y,x)in enumerate(zip(rows,b['rows']),1):
  expected=deepcopy(x);expected.update(execution_class='AUTHOR_DELEGATED_ROUTINE_WORKING_DRAFT_SELECTION',fictional_legal_participation_conditions_selected=True,actual_private_papers_or_NBA_physical_selection_certified=False,source_candidate_pointer=BOARD+'#/rows/'+str(i-1))
  assert y==expected,'Returned selected board differs from reviewed rank/actor/PS22 family'
 assert [(x['pick'],x['player'])for x in rows if x['selecting_team']=='CHI']==[(18,'Walker Kessler'),(57,'Keon Ellis')]
def selected_roster(w,t):
 rows=[deepcopy(x)for x in w['working_implementation']['named_contracts']if x['player']!='Stanley Johnson']
 rows.append({'player':'Walker Kessler','holder':'CHI','exclusive_current_UPC_claim':True,'roster_type':'STANDARD','mechanism':t['mechanism'],'modeled_acquisition_or_option_date':'2022-07-11','normal_upper':3191400,'apron_upper':3191400,'salary_function':'Selected RSC120%2022scalePick18; bonus/loan/buyout0; later options separate','first_covered_salary_capyear':2022,'last_guaranteed_salary_capyear':2023,'guaranteed_salary_capyears':[2022,2023],'guaranteed_fiscal_obligation_through':'2024-06-30','service_exact_end_not_inferred_from_fiscal_end':True,'unexercised_team_option_capyears':[2024,2025],'term':t['term'],'selected_contract_terms':deepcopy(t),'source_pointer':CHOICE+'#/rookie_terms','fictional_consensual_RSC_selected':True,'actual_private_UPC_or_receipt_certified':False})
 return rows
def guard_roster(rows,w,t,route):
 originals=w['working_implementation']['named_contracts']
 assert len(rows)==17 and len({x['player']for x in rows})==17
 assert sum(x['roster_type']=='STANDARD'for x in rows)==15 and sum(x['roster_type']=='TWO_WAY'for x in rows)==2
 assert [x for x in rows if x['player']!='Walker Kessler']==[x for x in originals if x['player']!='Stanley Johnson'],'Incumbent contract/obligation changed'
 n=next(x for x in rows if x['player']=='Walker Kessler')
 assert n['holder']=='CHI'and n['exclusive_current_UPC_claim']is True and n['roster_type']=='STANDARD'
 assert n['mechanism']==t['mechanism']and n['modeled_acquisition_or_option_date']=='2022-07-11'
 assert n['salary_function']=='Selected RSC120%2022scalePick18; bonus/loan/buyout0; later options separate'
 assert n['first_covered_salary_capyear']==2022 and n['last_guaranteed_salary_capyear']==2023
 assert n['source_pointer']==CHOICE+'#/rookie_terms'and n['term']==t['term']
 assert n['normal_upper']==n['apron_upper']==3191400 and n['guaranteed_salary_capyears']==[2022,2023]
 assert n['guaranteed_fiscal_obligation_through']=='2024-06-30' and n['service_exact_end_not_inferred_from_fiscal_end']is True
 assert n['unexercised_team_option_capyears']==[2024,2025] and n['selected_contract_terms']==t
 assert n['actual_private_UPC_or_receipt_certified']is False and n['fictional_consensual_RSC_selected']is True
 assert {x['player']for x in rows if x['roster_type']=='STANDARD'}==set(route['standard'])
 assert sum(x['normal_upper']for x in rows if x['roster_type']=='STANDARD')==142218409
 assert 'Keon Ellis'not in [x['player']for x in rows]
def execute(s):
 c=s[CHOICE];w=s[WINDOW];route=deepcopy(c['routes'][0]);t=deepcopy(c['rookie_terms']);e=deepcopy(c['Ellis_tender'])
 assert route['id']=='R1_WAIVE_STANLEY_KEEP_BRADLEY'and route['released']=='Stanley Johnson'
 rows=selected_board(s[BOARD]);guard_board(rows,s[BOARD]);registered=selected_roster(w,t);guard_roster(registered,w,t,route)
 distributed=datetime.fromisoformat('2022-07-08T09:00:00-04:00');expires=distributed+timedelta(hours=48);signed=datetime.fromisoformat('2022-07-11T09:00:00-04:00')
 assert expires.isoformat()=='2022-07-10T09:00:00-04:00'and signed>expires
 return {'selected_board_rows':rows,'selected_rookie_route':route,'registered_contracts':registered,
  'fictional_process':{'first_tender_date':'2022-07-08','first_100percent_Tender_accepted':False,'waiver_notice_distribution':distributed.isoformat(),'waiver_period_hours':48,'weekends_counted_under_2019Bylaws5_04':True,'waiver_expiry':expires.isoformat(),'no_other_team_claim_selected':True,'waiver_completed_in_selected_fiction':True,'new_RSC_assent_and_signing':signed.isoformat(),'new_RSC_separate_120percent_negotiation':True,'actual_distribution_claims_or_receipts_certified':False},
  'Ellis_selected_rights_path':{**e,'timely_delivery_and_nonacceptance_selected_as_fiction':True,'PS22_school_entry_not_foreign_professional_contract_selected':True,'real_player_refusal_or_foreign_contract_absence_certified':False},
  'dead_protection_reservation':{'player':'Stanley Johnson','full_original_family_upper':2351532,'bound_role':'Full current Year2 Salary upper inherited from source named contract; not a guaranteed-portion floor or certificate of actual100percent protection','actual_exact_guarantee_certified':False,'no_buyout_stretch_setoff_or_cash_discount':True,'new_team_or_assignment':None},
  'cost':{'live15_upper':142218409,'separate_old_waived_upper':2351532,'live_plus_old_waived_upper':144569941,'existing_stretch_upper':16371000,'first_reservation_11060000_replaced_once_by_RSC3191400':True,'old_first_plus_new_first_double_counted':False,'preserved_other_unsigned_normal':2036000,'preserved_other_unsigned_apron':3674000,'normal_family_upper_before_new_D23_charge':162976941,'apron_family_upper_before_new_D23_charge':164614941,'reservation_refinement_delta':-7868600,'actual_cash_saving_certified':False,'new_RSC_hardcap_trigger':False,'N23':None,'A23':None,'post_D23_total':None},
  'registration_summary':{'STD':15,'TW':2,'claims':17,'new_standard_rookie':1,'Ellis_standard_or_TW':0,'incumbents_except_released_preserved':16},
  'next_ports':['2022–23 dated role/minute/availability results; no future productivity imported','All other selected draft identities remain rights only; NPC new UPC/Tender/roster-slot transactions not automatically generated','2023 subsequent draft and new N23/A23 charges; no null-as-zero','Ellis future acceptance/newTW/foreign route/after subsequentDraft requires its own timely dispatch; no automatic retained rights']}
def guard_execution(v,s):
 c=s[CHOICE];route=c['routes'][0];guard_board(v['selected_board_rows'],s[BOARD]);guard_roster(v['registered_contracts'],s[WINDOW],c['rookie_terms'],route)
 assert v['selected_rookie_route']==route
 assert v['dead_protection_reservation']=={'player':'Stanley Johnson','full_original_family_upper':2351532,'bound_role':'Full current Year2 Salary upper inherited from source named contract; not a guaranteed-portion floor or certificate of actual100percent protection','actual_exact_guarantee_certified':False,'no_buyout_stretch_setoff_or_cash_discount':True,'new_team_or_assignment':None}
 p=v['fictional_process'];assert datetime.fromisoformat(p['waiver_expiry'])-datetime.fromisoformat(p['waiver_notice_distribution'])==timedelta(hours=48)
 assert p['waiver_notice_distribution']=='2022-07-08T09:00:00-04:00'and p['waiver_expiry']=='2022-07-10T09:00:00-04:00'and p['new_RSC_assent_and_signing']=='2022-07-11T09:00:00-04:00'
 assert p['waiver_completed_in_selected_fiction']and p['no_other_team_claim_selected']and p['weekends_counted_under_2019Bylaws5_04']
 assert p['actual_distribution_claims_or_receipts_certified']is False and p['first_tender_date']=='2022-07-08'and p['first_100percent_Tender_accepted']is False
 e=v['Ellis_selected_rights_path'];assert all(e[k]==a for k,a in c['Ellis_tender'].items())
 assert e['timely_delivery_and_nonacceptance_selected_as_fiction']and e['PS22_school_entry_not_foreign_professional_contract_selected']
 assert e['real_player_refusal_or_foreign_contract_absence_certified']is False
 cost=v['cost'];assert cost['live15_upper']+cost['separate_old_waived_upper']==144569941
 assert cost['normal_family_upper_before_new_D23_charge']==route['refined_normal_public_family_upper_before_D23']==142218409+2351532+16371000+2036000
 assert cost['apron_family_upper_before_new_D23_charge']==route['refined_apron_public_family_upper_before_D23']==142218409+2351532+16371000+3674000
 assert cost['reservation_refinement_delta']==-7868600 and cost['N23']is None and cost['A23']is None and cost['post_D23_total']is None
 assert cost['live15_upper']==142218409 and cost['separate_old_waived_upper']==2351532 and cost['live_plus_old_waived_upper']==144569941
 assert cost['existing_stretch_upper']==16371000 and cost['preserved_other_unsigned_normal']==2036000 and cost['preserved_other_unsigned_apron']==3674000
 assert cost['first_reservation_11060000_replaced_once_by_RSC3191400']is True
 assert cost['actual_cash_saving_certified']is False and cost['new_RSC_hardcap_trigger']is False and cost['old_first_plus_new_first_double_counted']is False
 assert v['registration_summary']=={'STD':15,'TW':2,'claims':17,'new_standard_rookie':1,'Ellis_standard_or_TW':0,'incumbents_except_released_preserved':16}
def build():
 s=inputs();v=execute(s);guard_execution(v,s)
 v['cost']['unsigned_buffer_convention']='Unequal normal/apron values are separately preserved conservative model reservations from the reviewed parent; neither is the actual statutory charge of an unaccepted second-round RequiredTender. No new cash/UPC or monetary legal charge inferred.'
 return {'id':'CHICAGO_2022_ROOKIE_SELECTED_EXECUTION','baseline_main':'ee0ff822aa127f8263cc69e03ba2a7184053e22e','classification':'NEW_ROUTINE_FICTIONAL_DRAFT_AND_ROOKIE_SELECTION_PENDING_INDEPENDENT_REVIEW','source_sha256':{**PINS,SELF:h(ROOT/SELF)},'authorization':AUTH,'selection_reason':'D22A backup rim protector/wing rights preserves approved Chicago growth core. R1 retains existing Bradley backup center while a rookie develops; compared R2 preserves Stanley instead, with identical protected-cost upper. No important core move/MVP/title/ending change.','working_execution':v,'fact_inference_candidate_author_boundaries':{'primary_rules_and_public_reference':'Source board/rookie comparison and peers; original candidate producer states preserved','selected_fiction':'60draft legal participation families plus CHI18 Kessler/R1 named waiver/RSC and CHI57 Ellis timely unaccepted RT','unselected_candidates':'Alternate Chicago board/route, all other new NPC UPCs, future options/season/awards/results','new_human_author_lock':False},'limits':{'independent_review_completed':False,'root_canonical_adoption_recorded':False,'actual_private_cost_consent_medical_or_history_certified':False,'whole_2022_23_FY_cost_results_or_macro3':False,'MVP_year_title_count_or_franchise_change_selected':False},'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','actual_context_packs':0,'manuscript_allowed':False}
def markdown(v):
 e=v['working_execution'];lines=['# Chicago 2022 신인 실행 · R1 작업 선택','','검문된 D22A와 R1을 새 루틴 가상 작업 선택으로 소비한다. 아직 독립검문/정본 채택 전 snapshot이며 원 후보3파일·기존17계약·원급여 예약 범위는 보존한다. 실제NBA 지명·서명·waiver·현금 지출 인증이 아니다.','','- 2022June23: 전체60인 작업 지명을 PS22 적법 참가 가족 아래 선택한다. CHI18 Kessler/57 Ellis. 다른58명의 UPC는 자동 생성하지 않는다.','- July8 09:00 ET: Stanley waiver notice가 전구단에 배포되는 가상 경로. 주말도 포함하는48시간 동안 청구 없음 →July10 09:00 완료.','- July11 09:00 ET: 별도 합의120% RSC로 Kessler 등록. 두 보장 시즌+서로 다른 두 미행사 팀 옵션.','- Aug25: Ellis1시즌 최소급여RT 적법 전달·Oct15까지 미수락을 가상 선택. STD/TW 추가0이며 실제 거절/해외계약 부재 인증은 아니다.','','## 명단·의무','','| 구분 | 인원/금액 |','|---|---|','| 현행 등록 | 15STD+2TW=17 |','| Kessler 첫해120% | 3,191,400 |','| live15 상단 | 142,218,409 |','| Stanley 원 보호 상단 별도 예약 | 2,351,532 |','| live+새 dead 예약 | 144,569,941 |','| legacy stretch+다른 unsigned normal/apron | 16,371,000+2,036,000 / 3,674,000 |','| normal/apron 가족 상단 | 162,976,941 / 164,614,941 |','','원first예약11.06m을 새RSC3.1914m으로 한 번 대체한 상단 정밀화다. 기존Stanley 금액을삭제하거나 두 번 더하지 않는다. 실제7.8686m현금절감·원정확Γ/장부 인증은 아니다. 새RSC는NTMLE/BAE/수취S&T를사용하지않으며 새hardcap을발생시키지않는다. N23/A23와2023draft이후 전체숫자는null이다.','','[원비교](../design/CHICAGO_2022_ROOKIE_EXECUTION_CHOICE.md) · [60인원후보](../research/NBA_2022_FULL_DRAFT_WORKING_BOARD_2026_10_08.md) · [기존17계약 기간](CHICAGO_2022_23_NAMED_CONTRACT_WINDOW.md)','','후속2022–23 역할/분·가용성/승패·2023후속·다른리그PO/우승은 미완료. 6번49기능/31경로/미경로11·Pack0. 미완료큰묶음5/6번까지4·v0.30 PARTIAL·CLOSED·원고0.','']
 return '\n'.join(lines)
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if a.check:assert load(OUT)==v and text(ROOT/MD)==markdown(v),'Saved execution stale'
 print(json.dumps({'current':True,'draft_rows':60,'CHI':[18,57],'STD':15,'TW':2,'normal':162976941,'apron':164614941,'whole_macro3':False}))
if __name__=='__main__':main()
