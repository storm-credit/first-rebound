"""Execute one reviewed Chicago core-retention family, not all alternatives.

The selected consents/notices are explicit lawful story implementation models.
No private receipts, awards, later options or whole-season results are certified.
"""
from __future__ import annotations
import argparse,hashlib,json
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_core_retention_selected_family.py'
OUT='simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json'
MD=OUT.replace('.json','.md')
JOIN='research/CHICAGO_2022_JULY7_NAMED_ROSTER_CONTRACT_COST_JOIN_2026_10_07.json'
CX='research/CARTER_2021_EXTENSION_CANDIDATE_FAMILY_2026_10_07.json'
P='research/PROTAGONIST_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07.json'
Z='research/LAVINE_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07.json'
V='research/CHICAGO_2022_YOUNG_SATORANSKY_ROSTER_FAMILY_2026_10_07.json'
CORE='research/CHICAGO_2022_23_APPROVED_CORE_CONTRACT_EXECUTION_2026_10_07.json'
PINS={'research/CHICAGO_2022_JULY7_NAMED_ROSTER_CONTRACT_COST_JOIN_2026_10_07.json': '9f3e19c38f7be2a7259158cf4ba8f7440aca400593092d400cac23fa2917074a', 'research/CARTER_2021_EXTENSION_CANDIDATE_FAMILY_2026_10_07.json': '070f1393070644540642284e9f1a6b49a2c6d1c1903fade2610d8570344d1f21', 'research/PROTAGONIST_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07.json': '84040384319b79d9bd2d87575d3f7061337c8978775278e1fa4dd8677e5b3228', 'research/LAVINE_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07.json': '2c7cf936b8387521e46f67cd245358bbd5c8191c99c466da9ae8b4b7c7d635d0', 'research/CHICAGO_2022_YOUNG_SATORANSKY_ROSTER_FAMILY_2026_10_07.json': '9a1e49c1f0b9d3c95279ff675ac3c42c2a72384c8ed6d11cbeb917e5903ac363', 'research/CHICAGO_2022_23_APPROVED_CORE_CONTRACT_EXECUTION_2026_10_07.json': '2cc7aeaeaef530f1c3fac5846348792c3d516eb1479af1ce56617deb2e7cb2b5'}
CHOICE={'Carter':'CX1','Protagonist':'E2','LaVine':'EXISTING_DIRECT_BIRD5YEAR_FORM','Young':'Y_BIRD_8M','Satoransky':'S_MINIMUM'}
def require(v,m):
 if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()
def read(root,p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def selected_contract(row):
 return {'source_row':deepcopy(row),'model_status':'SELECTED_LAWFUL_FICTIONAL_CONTRACT_IMPLEMENTATION','modeled_mutual_consent':True,'actual_private_consent_or_notice_receipt':None,'author_locked':False}
def assert_contract(r,s):
 require(r['source_row']==s,'Returned contract differs from physical named row')
 require(r['model_status']=='SELECTED_LAWFUL_FICTIONAL_CONTRACT_IMPLEMENTATION' and r['modeled_mutual_consent'] is True,'Returned contract model not selected')
 require(r['actual_private_consent_or_notice_receipt'] is None and r['author_locked'] is False,'Private consent or new author lock falsely certified')
def build(root=ROOT):
 for p,h in PINS.items():require(sha(root/p)==h,'Reviewed source changed: '+p)
 d={p:read(root,p) for p in PINS}
 for p,v in d.items():require(v==json.loads((root/p).read_text(encoding='utf-8-sig')),'Loaded physical source substituted: '+p)
 j,c,p,z,v,core=(d[k] for k in (JOIN,CX,P,Z,V,CORE))
 require(j['date']=='2022-07-07' and all(j['probe_policy'][k]==val for k,val in CHOICE.items()),'Selected existing policy changed')
 require(not j['probe_policy']['new_FY22_hardcap_trigger'] and not j['probe_policy']['FY21_hardcap_carried_toFY22'],'Annual hardcap policy changed')
 cx=c['alternatives'][0];e=p['alternatives'][1];zt=z['terms_candidate']
 require(cx['id']=='CX1' and e['id']=='E2' and e['recipient']=='Chicago','Core-retention selection changed')
 require(list(cx['extension_regular_salary_schedule'].values())==[14150000,13050000,11950000,10850000] and cx['total_extended_regular_salary']==50000000,'Carter terms changed')
 require(e['salary_2022_onward']==[22000000,23760000,25520000,27280000] and e['new_term_end']=='2026-06-30','P E2 terms changed')
 require(zt['salary']==[37096500,40064220,43031940,45999660,48967380] and zt['one_player_option_cap_year']==2026 and zt['option_exercise_selected'] is None,'LaVine price or future PO changed')
 require(c['calendar']['start_ET']<'2021-10-15T12:00:00'<c['calendar']['deadline_ET'],'Carter date outside legal extension window')
 require(cx['2021_22_current_charge_unchanged_before_any_hypothetical_trade']==6920027 and not cx['2022_QO_RFA_or_FAhold_arises_if_extension_is_actually_implemented'],'Carter current charge or RFA status changed')
 rows=j['named_contract_rows'];require(len(rows)==17 and len({r['player'] for r in rows})==17,'Duplicate named players')
 require(sum(r['roster_type']=='STANDARD' for r in rows)==15 and sum(r['roster_type']=='TWO_WAY' for r in rows)==2,'July7 STD/TW slots changed')
 selected=[]
 for raw in rows:
  r=selected_contract(raw);assert_contract(r,raw);selected.append(r)
 normal=sum(r['normal_upper'] for r in rows);apron=sum(r['apron_upper'] for r in rows)
 require(normal==apron==141378541,'Live named salary upper differs')
 cost=deepcopy(j['joined_cost'])
 require(normal+cost['legacy_original_stretch_upper']+cost['named_first_and_two_second_reservations_normal']==cost['normal_public_family_upper']==170845541,'Normal category join changed')
 require(apron+cost['legacy_original_stretch_upper']+cost['named_first_and_two_second_reservations_apron']==cost['apron_public_family_upper']==172483541,'Apron category join changed')
 require(cost['TW_actualcash_excluded_not_zeroed'] and cost['removed_all_TW_standard_QO_family_max_reservation']==6000000 and cost['apron_no_FY22_trigger'],'TW cash or hardcap policy changed')
 require(all(q['NBA_UPC'] is False and q['slot_consumption']==0 for q in j['rights_and_unregistered_ports']),'Unsigned ports consume STD slots')
 events=[
  {'date':'2021-10-01','event':'EXERCISE_NEXT_ROOKIE_OPTIONS','players':['LaMelo Ball','Coby White'],'source':CORE,'legal_notice_model':True,'actual_receipt':None},
  {'date':'2021-10-15','time_ET':'12:00','event':'CARTER_CX1_MUTUAL_EXTENSION','player':'Wendell Carter Jr.','source_pointer':CX+'#/alternatives/0','old_2021_22_salary_unchanged':6920027,'new_period':['2022-07-01','2026-06-30'],'model_mutual_consent':True,'actual_receipt':None},
  {'date':'2022-06-29','event':'TIMELY_P_ORDINARY_QO_AND_NO_DOTSON_COOK_QOS','P_QO':'Preserved applicable pick/starter/old-component legal function, not one flat salary. No offer sheet/MaxQO or first-refusal notice chosen.','TW_QOs_never_issued_in_selected_model':True,'actual_private_absence_certified':False},
  {'date':'2022-07-01','event':'CARRY_11_AND_EXPIRED_FA_RIGHTS','live_standard_count':11,'expired_contracts':['Protagonist','Zach LaVine','Thaddeus Young','Tomas Satoransky','Devon Dotson','Tyler Cook'],'expired_FA_holds_not_deleted_before_valid_contract':True},
 ]
 for i,player in enumerate(['Zach LaVine','Protagonist','Thaddeus Young','Tomas Satoransky','Devon Dotson','Tyler Cook']):
  r=next(x for x in rows if x['player']==player)
  events.append({'date':'2022-07-07','time_ET':'AT_OR_AFTER12:00','same_day_order':i,'event':'SIGN_NEW_CONTRACT_MODEL','player':player,'mechanism':r['mechanism'],'modeled_mutual_consent':True,'actual_receipt':None,'replaces_own_FAhold_QO_without_duplicate':True,'resulting_STD_count':12+min(i,3),'resulting_TW_count':max(0,i-3)})
 events.append({'date':'2022-07-07','same_day_order':6,'event':'VALID_UNUSED_ANNUAL_EXCEPTION_WRITTEN_RENUNCIATION','legal_model':True,'actual_receipt':None,'actual_prior_incorporation_absence_certified':False})
 require(len(events)==11 and events[-2]['resulting_STD_count']==15 and events[-2]['resulting_TW_count']==2,'Named prefix slots changed')
 return {'id':'CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY','baseline_main':'b44b8d36868bda605c3c159cfe80d016edfd193f','source_sha256':{**PINS,SELF:sha(root/SELF)},
  'classification':'ROOT_ROUTINE_DESIGN_IMPLEMENTATION_SELECTED','status':'CX1_E2_LAVINE_YOUNG_SATO_AND_TWO_TW_LAWFUL_CONSENSUAL_MODEL_SELECTED_AND_JULY7_JOINED',
  'authority':'Previously recommended Chicago retained-core path; no franchise/core departure, MVP/title/ending change. Selection is routine legal story implementation, not new human exact-financial author lock or health-delegation price authority.',
  'selected_policy':CHOICE,'selection_reason':{'E2':'Existing4year retained-franchise recommended path ending2026 matches prior2026 contract bridge; does not buy lower core authority or suppress growth. E1/E3/E4 remain unchosen alternatives.','CX1':'Existing4year50m retained-Carter recommendation; avoid arbitrary40m discount or core departure.','LaVine':'Preserve existing5year FullBird4+1PO form; no advance2026 exercise/nonexercise or cap-hit kicker import.','Young_Sato_TW':'One reviewed15STD2TW continuity family; no new waived starter or replacement core trade.'},
  'selected_contracts':selected,'contract_terms':{'Carter':{'source_terms':deepcopy(cx),'common_terms':deepcopy(c['candidate_common_terms']),'current_term_bonus_if_any_preserved':True},'Protagonist':{'source_terms':deepcopy(e),'common_terms':deepcopy(p['candidate_terms']['E1_E2_E3']),'old_accrued_obligations_preserved':True},'LaVine':deepcopy(zt),'Young_Satoransky_source_forms':deepcopy(v['forms'])},
  'event_trace':events,'cost_on_2022_07_07':cost,'unsigned_ports':deepcopy(j['rights_and_unregistered_ports']),
  'summary':{'named_players':17,'standard':15,'two_way':2,'chronological_events':11,'new_standard_contracts_July7':4,'new_two_way_contracts_July7':2,'rookie_UPCs_added':0,'old_stretch_preserved':16371000,'normal_public_family_upper':170845541,'apron_public_family_upper':172483541,'new_FY22_hardcap_trigger':False},
  'implementation_scope':'Lawful mutually-consented fictional implementation and named July7 finite cost family. Statutory min/max, actual services/eligibility model, unchanged protected original components and no intervening unmodeled contract event remain admitted source conditions. Prior-source unselected flags remain generation history, not current selection.',
  'future_boundaries':['2022rank/player/firstTender byJuly15 and secondTender/unaccepted-rights clock; no slot16 by acceptance.','SimonovicX5/X6 beyondJuly29 requires existing lawful continuation family, not expired rights automaticcarry.','2022-23 datedavailability/roles/results and2023CobyRFA/LaMeloextension/CBA.','2026Pnewcontract and LaVinePO outcome remain separate; no future option exercise or exactnewprice chosen.'],
  'actual_private_receipts_or_exact_ledger_certified':False,'new_author_locks':0,'whole_FY22_or_macro3_complete':False,'design_gate':'CLOSED','freeze':'v0.30 PARTIAL','manuscript_allowed':False}
def validate(x,root=ROOT):
 try:require(x==build(root),'Saved selection differs from source-bound construction');return []
 except (ValueError,KeyError,IndexError) as e:return [str(e)]
def markdown(x):
 return '\n'.join(['# Chicago 2022 코어 잔류 계약 가족 선택·실행','','검문된 기존 권고 CX1/E2/LaVine5년Bird 및 Young8m/Sato법정minimum/두TW 가족을 루틴 설계로 선택했다. Chicago원클럽·성장코어를 유지하고 가격으로 코어권한을 낮추지 않는다. 인간 exact금액 작가잠금·실제사적동의 인증·2026PO행사·MVP/우승 선택은 아니다.','','Coby/LaMelo option→Oct15 Carter연장→June29 P유효ordinaryQO/두TWnoQO→July1 live11/FA권리 보존→July7 LaVine/P/Young/Sato/두TW→유효예외renounce의11사건이다. 날짜·보호·Bonus가족·미서명3port를 원source에 연결했다. 가상 적법 동의/통지 모델을 명시적으로 선택하고 실제접수는null로 남긴다.','','같은July7 15STD2TW의normal상단170,845,541/apron상단172,483,541이다. 원stretch16,371,000·unsigned/tender예약을 보존하며 TWcash0으로 처리하지 않는다. 새2022NTMLE/BAE/수취S&T를 쓰지 않아apron음수screen을 자동불법으로 읽지 않는다. 선수현금/실제원장/wholeFY22 인증이 아니다.','','다음: 선택결과에 연결되는2022권리/rookieTender·실명포트와2023후속. 82상대전체초별시계를 계약의 별도선행게이트로 추가하지 않는다. 전체macro3미완료·v0.30 PARTIAL·CLOSED·원고0.',''])
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');a=ap.parse_args();b=build()
 if a.write:
  (ROOT/OUT).write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(b),encoding='utf-8')
 else:require(not validate(read(ROOT,OUT)),'Invalid saved family')
 print(json.dumps(b['summary'],ensure_ascii=False))
