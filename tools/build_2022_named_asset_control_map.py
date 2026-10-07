"""Selected standings to sixty origin ports and finite named control dependencies.

This is a control-function input map, not a hidden lottery/forfeiture/holder choice.
No ancestor constructors or original 2022 selected players are imported.
"""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from unittest.mock import patch
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_named_asset_control_map.py'
OUT='simulation/NBA_2022_NAMED_ASSET_CONTROL_MAP.json';MD=OUT[:-5]+'.md'
SEED='simulation/NBA_2021_22_STANDINGS_PLAYIN_AND_2022_RIGHTS.json'
T1='simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json'
CHI='research/CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT_2026_10_07.json'
GLOBAL='simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json'
NOP='simulation/CHICAGO_NEW_ORLEANS_2021_SELECTED_KEEPER_RESULT.json'
BKN='simulation/CHICAGO_BROOKLYN_2021_22_SELECTED_KEEPER_RESULTS.json'
RETURN='research/NBA_2021_PICK16_BOS_OKC_HOU_WORKING_EXECUTION_2026_10_07.json'
PINS={'simulation/NBA_2021_22_STANDINGS_PLAYIN_AND_2022_RIGHTS.json': '139c1d6a90d1bd7ee672020af96e03bf6767599637902c329b1e772fdfcf63d9', 'simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json': 'f8c78e99cce1b02a051c94339b550fdb52205d3988db8bbe69b780559c3bc306', 'research/CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT_2026_10_07.json': 'bf8087a89af09a817c0a3eb5d4df906a906575a56016c873912db00eccdca9db', 'simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json': '93264d2dff86a58ad10ca6975315c6c2167961f94f2517b6f5f79fa3113f2af8', 'simulation/CHICAGO_NEW_ORLEANS_2021_SELECTED_KEEPER_RESULT.json': 'd1975077c8879807d63763d77d58a2d89f8b481ec6c2964f0a6a9bf7a96138fd', 'simulation/CHICAGO_BROOKLYN_2021_22_SELECTED_KEEPER_RESULTS.json': 'b29b621991a541396e952d2cdbbceda1a9025bbc9bc79598b8da3c735ae5743a', 'research/NBA_2021_PICK16_BOS_OKC_HOU_WORKING_EXECUTION_2026_10_07.json': '86b9989daa20eced72106c25b14fb8d8b3b32d201132a0b87ba466b0ce51fba0'};MEANING={'simulation/NBA_2021_22_STANDINGS_PLAYIN_AND_2022_RIGHTS.json': '89d7b56450b7d7ec2031a2c0dcc182edd184ef7f79e7d160ae44722b52671c41', 'simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json': '426de339ff1a1270eb41ed6b81caee8e10099e55e2176c4e9f31bd196da853d5', 'research/CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT_2026_10_07.json': '3517d47b6c788e8670506aea8797e90f1bcc625e3a0f80daf7f9cb77b3d4adec', 'simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json': '48d257db6ab6986a3acc1b5d8095ebdd8a9712fce3f06b93133a91c4d7740718', 'simulation/CHICAGO_NEW_ORLEANS_2021_SELECTED_KEEPER_RESULT.json': '5bd89b70fd046f758f6830f427502188efff74d6282c1172e1ca81d0164b3495', 'simulation/CHICAGO_BROOKLYN_2021_22_SELECTED_KEEPER_RESULTS.json': 'f1bd95da027cf1b247960290fec4c0ac5d182abdc7235332fd4983ace5c3cbf4', 'research/NBA_2021_PICK16_BOS_OKC_HOU_WORKING_EXECUTION_2026_10_07.json': '0ccbde96089b2c7256abacd787f2d5a32424e34d79189f246218d900b0507046'}
FILES=(SEED,T1,CHI,GLOBAL,NOP,BKN,RETURN)
# Only nonidentity observations from the official April18 original-world order.
# These are not copied as the alternate world's holders or ranks.
HIST_FIRST={'LAL':'NOP','LAC':'OKC','NOP':'CHA','BKN':'HOU','TOR':'SAS','UTA':'MEM','BOS':'SAS','PHX':'OKC'}
HIST_SECOND={'HOU':'IND','DET':'TOR','IND':'ORL','LAL':'SAS','SAS':'CLE','WAS':'MIN','BKN':'DET','CHI':'SAC','DEN':'MIN','TOR':'GSW','UTA':'NOP','PHI':'MIA','DAL':'WAS','MIA':'CLE','MEM':'POR','PHX':'IND'}
OBSERVATIONS=[
 {'id':'NBA_APR18_ORDER','url':'https://api-hub.nba.com/news/nba-draft-2022-ties-broken-official-release','date':'2022-04-18','channel':'INDEXED_OFFICIAL_BODY_READ','web_ref':'turn2286search3','scope':'Origin/holder and forfeiture contrasts only; original ranks/results not transported.','raw_body_adopted':False},
 {'id':'NBA_PG2019','url':'https://www.nba.com/thunder/news/acquisitions-190710','date':'2019-07-10','channel':'INDEXED_TEAM_BODY_READ_OPEN_IFRAME','web_ref':'turn2288search8','scope':'LAC2022 first toOKC unprotected.','raw_body_adopted':False},
 {'id':'NBA_HARDEN2021','url':'https://www.nba.com/rockets/rockets-complete-three-team-trade','date':'2021-01-13','channel':'INDEXED_TEAM_BODY_READ_OPEN_IFRAME','web_ref':'turn2288search6','scope':'BKN2022 first toHOU; MIL2022 also acquired, subject to later Tucker return.','raw_body_adopted':False},
 {'id':'NBA_TUCKER_RETURN','url':'https://www.nba.com/bucks/news/milwaukee-bucks-acquire-pj-tucker-and-rodions-kurucs-houston-rockets','date':'2021-03-19','channel':'INDEXED_TEAM_BODY_READ','web_ref':'turn2289search0','scope':'MIL2022 first returned toMIL; do not stop its chain at the January Harden event.','raw_body_adopted':False},
 {'id':'NBA_MIL_PENALTY','url':'https://www.nba.com/news/nba-imposes-penalty-on-bucks-for-early-free-agency-discussions','date':'2020-12-21','channel':'INDEXED_OFFICIAL_BODY_READ','web_ref':'turn2291search0','scope':'Original Bogdanovic-timing sanction rescinds MIL2022 second. No selected-world causal determination.','raw_body_adopted':False},
 {'id':'NBA_CHI_MIA_PENALTY','url':'https://www.nba.com/news/chicago-bulls-miami-heat-free-agency-violations','date':'2021-12-01','channel':'INDEXED_OFFICIAL_BODY_READ','web_ref':'turn2289search3','scope':'Next available second for CHI Lonzo and MIA Lowry discussions, not both original2022 own-origin seconds.','raw_body_adopted':False},
 {'id':'NBA_LEVERT2022','url':'https://www.nba.com/news/cavaliers-pacers-caris-levert-ricky-rubio-trade','date':'2022-02-07','channel':'INDEXED_NBA_BODY_READ','web_ref':'turn2291search1','scope':'HOU2022 second CLE→IND and MIA2022 second IND→CLE belong to the unselected Rubio/LeVert event.','raw_body_adopted':False},
 {'id':'NBA_AD2019','url':'https://www.nba.com/lakers/releases/190706-lakers-acquire-davis','date':'2019-07-06','channel':'INDEXED_TEAM_BODY_READ','web_ref':'turn2287search5','scope':'Completed prior AD asset family; exact first deferral predicate must remain condition-bearing.','raw_body_adopted':False},
 {'id':'NBA_CP2020','url':'https://www.nba.com/news/reports-thunder-agree-to-trade-chris-paul-to-suns','date':'2020-11-16','channel':'INDEXED_NBA_BODY_READ','web_ref':'turn2287search4','scope':'Named PHX2022 first toOKC. Exact protection not recovered from this observation.','raw_body_adopted':False},
 {'id':'NBA_CONLEY2019','url':'https://www.nba.com/news/report-grizzlies-trade-conley-jazz','date':'2019-06-19','channel':'INDEXED_NBA_REPORT_BODY_READ','web_ref':'turn2287search0','scope':'UTA prior2020/21 first conditional convey and later first; not actual alternate prior settlement.','raw_body_adopted':False},
 {'id':'NBA_OKC2018','url':'https://www.nba.com/thunder/news/acquisitions-180725','date':'2018-07-25','channel':'INDEXED_TEAM_BODY_READ','web_ref':'turn2287search1','scope':'Named protected OKC2022 first toATL; exact fallback preserved as a condition port.','raw_body_adopted':False}]
FIXED=(deepcopy(HIST_FIRST),deepcopy(HIST_SECOND),deepcopy(OBSERVATIONS))
def need(x,m):
 if not x:raise AssertionError(m)
def txt(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(txt(p).encode()).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def disk(root,p):return json.loads(txt(root/p))
def physical(root,p):return disk(root,p)
def sources(root):
 need((HIST_FIRST,HIST_SECOND,OBSERVATIONS)==FIXED,'Public observation meaning changed')
 o={}
 for p in FILES:
  need(sha(root/p)==PINS[p],'Source stale '+p);v=physical(root,p)
  need(v==disk(root,p)and digest(v)==MEANING[p],'Returned physical source altered '+p);o[p]=v
 return o
def origin_domains(s):
 out={}
 for k,t in enumerate(s['nonplayoff_lottery_origins'],1):
  out[(1,t)]=sorted(set(range(1,5))|set(range(max(5,k),min(14,k+4)+1)))
 for b in s['first_round_nonlottery_origin_buckets']:
  for t in b['origins']:out[(1,t)]=b['possible_pre_draw_ranks']
 for b in s['second_round_origin_buckets']:
  for t in b['origins']:out[(2,t)]=b['possible_pre_draw_ranks']
 return out
def control_row(round_number,t,ranks,src):
 historical=(HIST_FIRST if round_number==1 else HIST_SECOND).get(t,t)
 r={'id':f'{t}_2022_R{round_number}','origin':t,'round':round_number,'origin_rank_domain':ranks,'historical_public_holder_contrast':historical,'final_selected_holder':None,'exact_rank':None,'player':None,'UPC_or_Tender_selected':False,'historical_holder_automatically_copied':False,'control_kind':'PRESERVED_PUBLIC_TEMPLATE_REPLAY_PORT','required_input':'Adopt preserved named prior claim and evaluate its2022 allocation at chosen rank; no new offseason/deadline asset move.','all_hidden_claim_absence_required':False}
 if historical==t:
  r.update(control_kind='IDENTITY_PUBLIC_TEMPLATE_ROUTINE_FAMILY',supported_candidate_holder=t,source='NBA_APR18_ORDER',required_input=None,admitted_family='Retain positive public own-origin allocation template; no incompatible selected prior claim or new assignment. Candidate template, not actual private portfolio certification.')
 if round_number==1:
  if t in ('BKN','LAC'):
   r.update(control_kind='NAMED_UNPROTECTED_PRIOR_FIRST',supported_holder='HOU'if t=='BKN'else'OKC',required_input=None,source='NBA_HARDEN2021'if t=='BKN'else'NBA_PG2019')
  elif t=='DET':
   threshold=next(c for c in src[RETURN]['conditional_return_claims']if c['origin']=='DET')['first_protection_by_year']['2022']
   r.update(control_kind='SELECTED_T1_PROTECTED_FIRST',claim_holder='OKC',current_underlying_pick_retained_by='DET',protection2022=f'1–{threshold}',required_input=None,source=T1,protection_source=RETURN+'#/conditional_return_claims/0/first_protection_by_year/2022')
  elif t=='CHI':r.update(control_kind='SELECTED_CHI_RETAINED_OWN_FIRST',supported_holder='CHI',required_input=None,source=CHI)
  elif t in ('BOS','TOR','NOP','PHI','CLE'):
   why={'BOS':'White/Richardson/Langford event not selected.','TOR':'Young staysCHI; Dragic/Young event not selected.','NOP':'Graham and Adams/Bledsoe/JV optional atoms not selected.','PHI':'Harden/Simmons event not selected.','CLE':'Rubio/LeVert event not selected.'}[t]
   r.update(control_kind='SELECTED_KEEPER_REJECTS_LATER_HISTORICAL_TRANSFER',keeper_holder=t,required_input='Replay prior public own-first family, retaining any existing burden; do not add the omitted outgoing atom.',omitted_event_reason=why)
  elif t in ('UTA','PHX','LAL','OKC'):
   r.update(control_kind='NAMED_PRIOR_PROTECTION_OR_ROLLOVER',claim_holder={'UTA':'MEM','PHX':'OKC','LAL':'NOP','OKC':'ATL'}[t],source={'UTA':'NBA_CONLEY2019','PHX':'NBA_CP2020','LAL':'NBA_AD2019','OKC':'NBA_OKC2018'}[t],required_input='Preserved prior contract2022 protection/rollover allocation predicate plus prior2020/21 settlement where applicable. Exact numeric source still a finite input, not private full-ledger evidence.')
  elif t=='MIL':r.update(control_kind='NAMED_PRIOR_FIRST_RETURN',keeper_holder='MIL',source='NBA_TUCKER_RETURN',required_input='Bind completedMarch19 common S2Tucker atomic return; January MIL→HOU is not the terminal holder.')
 else:
  if t in ('CHI','DET','LAL'):r.update(control_kind='JOINT_THREE_ORIGIN_COMPOSITE_CLAIM',joint_group='CHI_DET_LAL2018_2019',source=CHI,required_input='Original2018 exchange then2019 LALcomparison exercise/priority and both counterpart residual claims. Never add three Chicago picks.')
  elif t=='BKN':r.update(control_kind='JORDAN_ATOM_NOT_SELECTED',keeper_holder='BKN',required_input='Preserve prior own2R template; do not transport originalDETrecipient from the unselectedJordan cash+fourclaims atom.')
  elif t=='DAL':r.update(control_kind='PORZINGIS_ATOM_NOT_SELECTED',keeper_holder='DAL',required_input='Preserve existing prior2Rconditions; do not copy originalWASrecipient from unselectedKP/Dinwiddie atom.')
  elif t in ('HOU','MIA'):r.update(control_kind='LEVERT_ATOM_NOT_SELECTED',prefix_holder='CLE'if t=='HOU'else'IND',source='NBA_LEVERT2022',required_input='Bind actual earlier named priorclaim and retain conditions; no CLE/INDLeVert swap copied.')
  elif t=='WAS':r.update(control_kind='RUBIO_ATOM_NOT_SELECTED',prefix_holder='CLE',required_input='Bind original priorWASclaim heldCLE before unselectedRubio→CLE2021 event; keeperRubioMIN cannot support originalMINreceipt.')
  elif t=='MIL':r.update(control_kind='ORIGINAL_SANCTION_CAUSAL_PORT',historical_public_holder_contrast='FORFEITED',source='NBA_MIL_PENALTY',required_input='Determine whether originalDec2020 Bogdanovic early-contact cause is preserved in selectedS2; do not invent an actual disciplinary receipt or copy it from a player-freeagency endpoint.')
  elif t=='PHI':r.update(control_kind='MIA_NEXT_AVAILABLE_SANCTION_CAUSAL_PORT',historical_public_holder_contrast='MIA_FORFEITED',source='NBA_CHI_MIA_PENALTY',required_input='Bind PHI→DEN→MIA earlier claim and selectedMIA lawful negotiation timing; originalLowry sanction not automatically repeated.')
 return r
SOURCE_CONTROL_ROW=control_row
def assert_row(r,n,t,ranks,src):
 need(r==SOURCE_CONTROL_ROW(n,t,ranks,src),'Returned control port differs from fixed source-supported mapping')
 # Distinct fixed boundaries avoid validating only one patched constructor.
 need((r['origin'],r['round'],r['origin_rank_domain'])==(t,n,ranks),'Returned origin/rank changed')
 need(r['final_selected_holder']is None and r['player']is None and r['UPC_or_Tender_selected']is False,'Unchosen rank/holder/player promoted')
 if(n,t)==(1,'DET'):need(r['current_underlying_pick_retained_by']=='DET'and r['claim_holder']=='OKC','Protected claim confused with underlying ownership')
 if(n,t)==(2,'MIL'):need(r['control_kind']=='ORIGINAL_SANCTION_CAUSAL_PORT'and r['historical_public_holder_contrast']=='FORFEITED','MIL sanction replaced with CHI origin')
 if(n,t)==(2,'PHI'):need(r['control_kind']=='MIA_NEXT_AVAILABLE_SANCTION_CAUSAL_PORT','MIA forfeiture origin wrong')
def build(root=ROOT):
 src=sources(root);s=src[SEED];domains=origin_domains(s);need(len(domains)==60,'Origin domain not60')
 need(src[T1]['summary']['working_draft_choices']==60,'T1draft selection source changed')
 need(any(a['asset']=='DET_FIRST_OR_2027_SECOND'and a['owner']=='OKC'for a in src[T1]['final_asset_ownership']),'DETconditional claim holder changed')
 need(src[NOP]['selected_policy']['new_counterparty_trade']is False,'NOPkeeper omitted trades changed')
 rows=[]
 for n,t in sorted(domains):
  r=control_row(n,t,domains[(n,t)],src);assert_row(r,n,t,domains[(n,t)],src);rows.append(r)
 need(max(domains[(1,'DET')])<=16,'DETprotected current domain couldconvey')
 claims=src[CHI]['positive_claim_bridge'];need(claims[0]['count_upper']==1 and claims[1]['count_upper']==1,'CHIcardinality changed')
 pending=[r['id']for r in rows if r['required_input']is not None]
 return {'id':'NBA_2022_NAMED_ASSET_CONTROL_MAP','baseline_main':'d74ffd6efcdb18a07285a23ea7a59a014400c32b','status':'SIXTY_SOURCE_BOUND_ORIGIN_PORTS_NAMED_PUBLIC_CONTROL_REPLAY_NOT_FINAL_ALLOCATION','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_observations':deepcopy(OBSERVATIONS),'direct_HTTP_failed_bytes_metadata':'C:/Users/Storm Credit/AppData/Local/Temp/fr-control2022-20261007/sources.json','failed403_bodies_adopted':False,'typed_control_rows':rows,'coupled_draft_ties':{'first_second_CHI':[[17,48],[18,47]],'second_tied_reverse_first':True,'independent_second_draw':False},'Chicago_economic_ports':{'first_count':1,'composite_second_count':1,'separate_three_origins_not_three_Chicago_picks':True,'first_rank':[17,18],'composite_origin_domains':s['Chicago_2022_rights']['CHI_second']['origin_domains'],'exact_composite_counterpart_allocation':None},'discipline_scope':{'original_2022_missing_origins':['MIL','PHI'],'original_MIA_forfeited_claim_origin':'PHI','original_CHI_penalty':'next_available_second_not_direct2022own_origin','selected_CHI_Lonzo_trade':False,'selected_MIA_or_MIL_actual_illegal_contact_or_discipline':None,'alternative_pick_count_58_or_60_selected':False},'summary':{'origin_ports':60,'first_origin_ports':30,'second_origin_ports':30,'exact_first_rank_selected':0,'named_supported_nonidentity_first_holders':2,'resolved_CHI_own_first_and_DET_protected_retention':2,'control_kind_counts':dict(Counter(r['control_kind']for r in rows)),'remaining_typed_control_ports':len(pending)},'remaining_finite_inputs':{'rank_parameters':'Four distinct lottery winners and record-tie1R order (2R reverse); no originalORL/OKC/HOU/SAC or draftees copied.','protection_ports':['UTA2022priorConley','PHX2022priorPaul','LAL2022priorAD','OKC2022priorSchroder'],'joint_exchange_port':'CHI/DET/LAL2018–2019 precise sourcefunction and all counterpart claims','prefix_second_ports':['HOUpriorCLE','MIApriorIND','WASpriorCLE','INDpriorORL','SASpriorCLE','DENpriorMIN','TORpriorGSW','UTApriorNOP','MEMbeforeBagley','PHXpriorIND'],'discipline_ports':['MILoriginalDec2020cause','MIAselectedlawfulLowrytiming/PHIclaim'],'all_pending_ids':pending,'port_count_is_not_new_author_approval_count':True,'identity_template_family_is_routine_candidate_not_permanent_private_HOLD':True},'certification':{'sixty_origin_rank_functions_constructed':True,'sixty_final_holders_or_complete_prior_claim_functions_certified':False,'existing_public_named_claims_deleted':False,'private_all_ledger_or_receipt_required':False,'new_asset_trade_or_draw_selected':False,'independent_review_completed':False,'whole_macro3':False,'manuscript':False},'freeze':'v0.30 PARTIAL','design_gate':'CLOSED'}
def validate(v,root=ROOT):return []if v==build(root)else['Control input map differs from source']
def markdown(v):
 lines=['# 2022 지명권: 60원점과 명명된 소유조건 입력지도','',v['status'],'','선택된1230결과·6playin에서60origin 순번함수를 연결했다. lottery4개·동률1R순서와2R역순·교환권 행사는 미선택이다. 모르는 보유자를 own으로 채우지 않았고, 원2022 공개소유표는 대조용이다.','', 'Chicago 자체1R17/18과복합2R 한 장은보존한다. 17↔48·18↔47 연동. DETfirst 현재1–6은선택T1의top16보호안이므로 underlying DET보유/조건부claim OKC를구분한다. BKNfirst→HOU·LACfirst→OKC는명명된원양도다.','', '[원2022 공식표](https://api-hub.nba.com/news/nba-draft-2022-ties-broken-official-release)에서실제누락은MILown2R와PHI→MIA2R이다. Chicago원징계는next-available이며2022직접누락으로쓰지않는다. 원징계원인/선택된적법협상은별도조건이고실제58픽을대체58/60으로복사하지않는다.','', '[Bucks3/19 공식반환](https://www.nba.com/bucks/news/milwaukee-bucks-acquire-pj-tucker-and-rodions-kurucs-houston-rockets)은MIL2022first를MIL로돌린다. Harden1월소유단면에서멈추지않는다. TORYoung/BOSWhite/PHIHarden/NOPGraham·JV/CLELeVert/DALKP/Jordan 등원미선택거래로권리를이동시키지않는다.','', '공식표와원구단본문은indexed관측으로구분했다. 새직접HTTP4개는403이고본문증거0;원byteSHAs/실패경로별도보존. 이전검문완료조상생성기재실행0.','', '| 원점 | R | 순번가능집합 | 연결종류 | 필요한입력 |','|---|---|---|---|---|']
 lines += [f"| {r['origin']} | {r['round']} | {r['origin_rank_domain']} | {r['control_kind']} | {'없음(명명범위)'if r['required_input']is None else '명명된원권리함수/선행event'} |"for r in v['typed_control_rows']]
 lines += ['','60행을만든것은60최종보유자완료가아니다. 다음은네prior1R조건·세원점교환의상대잔여권리·열named2Rprefix·두징계인과다. 새원계약전체/모든비공개청구부재/실제영수증을요구하지않는다. 가격·새거래·2022선수지명·Tender/UPC선택0.','', '[현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','', '| 묶음 | 상태 |','|---|---|','| 1 드래프트연쇄 | 완료 |','| 2 Chicago2020–21 | 완료 |','| 3 2021–23 | 1230·순위·playin선택/2022권리최종배정미완료 |','| 4 장기커리어 | 진행 |','| 5 전체구조 | 진행 |','| 6 규격·ContextPack | 진행·Pack0 |','| 7 통합·작가승인 | 미완료 |','','미완료큰묶음5/6번까지4. v0.30 PARTIAL·CLOSED·원고0.','']
 return '\n'.join(lines)
def main():
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');q=a.parse_args();v=build()
 if q.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if q.check:need(disk(ROOT,OUT)==v and txt(ROOT/MD)==markdown(v),'Savedmap stale')
 controls=0
 if q.self_test:
  original=control_row
  for which in ('holder','origin'):
   def bad(n,t,ranks,src):
    r=original(n,t,ranks,src)
    if(n,t)==(1,'BKN'):
     if which=='holder':r['supported_holder']='BKN'
     else:r['origin_rank_domain']=[1]
    return r
   with patch(__name__+'.control_row',side_effect=bad):
    try:build()
    except AssertionError:controls+=1
    else:raise AssertionError('Returned control '+which+' false-pass')
 print(json.dumps({'current':True,'summary':v['summary'],'writer_controls':controls if q.self_test else None}))
if __name__=='__main__':main()
