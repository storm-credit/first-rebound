"""Two later Detroit games reuse reviewed named legal family and source role clock."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from fractions import Fraction
from datetime import date,timedelta
from unittest.mock import patch
import argparse,csv,hashlib,io,json
import build_nyk_2021_keeper_and_chicago_selected_results as base
import build_chicago_detroit_2021_two_date_selected_bpm_results as det
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_det_2022_later_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_DETROIT_2022_LATER_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
ROLE='simulation/CHICAGO_DETROIT_2021_TWO_DATE_WORKING_EXECUTION.json'
ADOPT='simulation/DET_ROUTINE_OPERATING_FAMILY_SELECTION_2026_10_07.json'
ECON='research/DETROIT_2021_A_ROUTINE_OPERATING_EXECUTION_FAMILY_2026_10_07.json'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397',ROLE:'fc44fe1b28318c2004529fc68a3b3d6b090f9b3a100265ca5e9517c0da3676b3',ADOPT:'9f9c307f33975de3b3c05734e41f8401cad0439f0446f7bc87aa21d8c7752dc2',ECON:'855371610d0f2b776b773bdf2ff02f27a43684b6c1407b1d54f698c6e0f093ef'}
IDS=('0022100415','0022100982')
ROLE_MEANING_SHA='ec3f7b98866cf36b7e839a1d4b6d11a5c9997de8687d055916e0defe6bf0d21d'
need=base.need;sha=base.sha;text=base.text;physical=base.physical
POLICY={'selected_interval':['2022-01-11','2022-03-09'],'same_family':'Existing selected A roster/q interval/minimum/Bird/roomMLE/waiver/fullGamma family, no new transaction or signedprice selected.','same_dated_availability':'Source 10positive operational availability selected at these two later dates; no originalGrantthumb/Olynykinjury/Liversrehab/COVID automatically copied. Zero reserves clinicalnull.','retained_events':'No new role/cost affecting intervening event chosen in this finite fictional family; not actualhistoricalnoevent certificate.','unsigned_Aldama':'Valid originalRT with operativeacceptancewindow ending notbeforeOct15, chosenunaccepted atlawfulexpiry/noUPC ornewreceipt; source3m reservation kept. NewNonNBA/college/tender/rights facts reopen X5/X6, notforeverexclusive.','TW':'Garza/Smith oneSeason lawfulTW unchanged, no standardconversion/noNBAactivations onthese2dates, operative50gameallowance not actual activationcert.','actual_receipts_medical_prices':False}
FIXED_POLICY=deepcopy(POLICY)
def direct(root,p):
 t=(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
 return json.loads(t)if p.endswith('.json')else list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else t
def sources(root):return {p:physical(root,p)for p in PINS}
def source_role_blocks(src):
 segments=src[ROLE]['rows'][0]['simultaneous_segments'];out=[]
 for s in segments:
  b={'start_second':s['start_second'],'end_second':s['end_second'],'seconds':s['seconds'],'positions':deepcopy(s['DET'])}
  if out and out[-1]['positions']==b['positions'] and out[-1]['end_second']==b['start_second']:
   out[-1]['end_second']=b['end_second'];out[-1]['seconds']+=b['seconds']
  else:out.append(b)
 return out
def role_blocks(src):return source_role_blocks(src)
def assert_roles(src,blocks):
 need(blocks==source_role_blocks(src),'Returned later role differs from frozen source chronology');sec=Counter();end=0
 for b in blocks:
  need(b['start_second']==end and b['seconds']==b['end_second']-end and len(set(b['positions'].values()))==5 and set(b['positions'])=={'PG','SG','SF','PF','C'},'Role clock/positions invalid');end=b['end_second']
  for p in b['positions'].values():sec[p]+=b['seconds']
 need(end==2880 and sum(sec.values())==14400 and dict(sec)==src[ROLE]['rows'][0]['nominations']['DET']['positive_seconds'],'Source player seconds altered');return sec

def build(root=ROOT):
 src=sources(root)
 for p,h in PINS.items():need(sha(root/p)==h and src[p]==direct(root,p),'Returned physical source differs '+p)
 need(hashlib.sha256(json.dumps(src[ROLE],sort_keys=True,separators=(',',':')).encode()).hexdigest()==ROLE_MEANING_SHA,'Returned frozen role semantic differs from reviewed source')
 need(POLICY==FIXED_POLICY,'Later family policy altered')
 e=src[ECON];a=src[ADOPT];proof=e['complete_domain_proof']
 need(a['selected_q_interval']==[3000000,7000040] and not a['actual_private_cost_acceptance_clinical_or_receipt_certified'] and proof['nonempty_for_all_admitted_X'] and proof['entire_family_cap_and_exception_path_sufficient_within_named_admissions'],'Selected existing legal family altered')
 need(proof['X_interval']==[0,5361732] and proof['q_interval']==[3000000,7000040] and proof['normal_upper_after_all_events']==135579566 and not proof['new_2021_22_hardcap_trigger_selected'],'Reviewed public cost domain altered')
 seed=src[ROLE]['rows'][0]['nominations']['DET'];last=e['registration_and_cost_prefix'][-1];standard=seed['standard'];tw=seed['two_way']
 need(set(standard)==set(last['standard']) and set(tw)==set(last['two_way']) and len(standard)==15 and len(tw)==2,'Existing source registration/contract interval altered')
 drafts=[r for r in src[base.DRAFT]['selected_rows']if r['conditional_final_draft_rights_holder']=='DET']
 need([(r['pick'],r['player'])for r in drafts]==[(5,'Jalen Suggs'),(37,'Santi Aldama'),(38,'Isaiah Livers'),(53,'Luka Garza')],'Current Detroit rights altered')
 blocks=role_blocks(src);seconds=assert_roles(src,blocks);active=seed['active'];inactive=seed['inactive']
 need(len(active)==12 and len(set(active))==12 and set(seconds)<=set(active)<=set(standard) and set(inactive)==set(standard)-set(active),'Active membership altered')
 r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
 for gid in IDS:
  g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid)
  need(g['opponent']=='DET' and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Source date/state changed')
  c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHIhealth changed')
  pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['DET']=joint.pop('NYK')
  for b in pair:b['DET']=b.pop('NYK')
  need(not(set(joint['CHI'])&set(joint['DET'])) and set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'Ownership/CHI active invalid')
  for ps in joint.values():names.update(ps)
  prepared.append((g,h,pair,joint))
 need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'CHI authority altered')
 rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby'})
 if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
 for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Same selected singleBPM source altered')
 games=[]
 for g,h,pair,joint in prepared:
  impact={t:sum(Fraction(rates[p]['exact_fraction'])*n/2880 for p,n in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['DET'])-int(back['CHI']));margin=impact['CHI']-impact['DET']+home+fatigue;need(margin!=0,'SeparateOTselection needed')
  games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'DET_active':active,'DET_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_DET_impact_fraction':str(margin),'CHI_minus_DET_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'DET','score':None,'overtime_selection':None})
 return {'id':'CHICAGO_DETROIT_2022_LATER_SELECTED_KEEPER_RESULTS','baseline_main':'ab7f81a1d971a997c242bb88b3fcaaab25dbce3f','status':'SELECTED_LATER_TWO_DATES_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'selected_policy':deepcopy(POLICY),'existing_economic_family_projection':{'root_selection':a['status'],'public_cost_domain':deepcopy(proof),'preserved_contract_functions':deepcopy(e['contract_function_families']),'six_cost_categories_preserved':deepcopy(e['six_cost_categories']),'full_Sekou_Okafor_current_charge':5743703,'new_price_or_assignment_or_Jordan_trade_selected':False,'new_2021_22_hardcap_trigger':False},'selected_registration':{'standard':standard,'TW':tw,'STD':15,'TW_count':2,'active':active,'inactive':inactive,'zero_clinical_status':None,'TW_NBAactivations':0},'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'summary':{'selected_games':2,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'DET_wins':sum(g['selected_regulation_winner']=='DET'for g in games),'STD':15,'TW':2,'active_each':12,'positive_each':10,'role_blocks_each':len(blocks),'clock_seconds_each':2880,'player_seconds_each':14400},'butterfly_handoff':['Existing Lyles2year/Bagleyfuture causality preserved; no originalSACBagleytrade and noGrantPORtrade imported.','Existing full Sekou/Okafor nonassignmentwaiver charge kept; no BKNJordan/picks/cash atom retrospectively executed.','Aldama37unsignedRT/Garza53TW/Livers38 UPC andSuggs5RSC separate from original2021draft/UPC calendar.','These two dates choose same operatingavailability/contractfamily, not actualnointerveningevents/clinicalproof orfullseasonrights certificate.'],'certification':{'selected_fictional_lawful_NPC_family':True,'selected_two_later_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole82_or_macro3':False,'new_author_lock':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
 a=['# Detroit 후반 두 날짜 · 선택 결과','','검문된 기존 A 경제·명단·역할 가족 재사용, 두 날짜 가상 가용성과 현재 CHI 단일 BPM 결과 선택. 독립검문 대기.','','|날짜|키|CHI상태|승자|CHI영향/100|','|---|---|---|---|---|']
 for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_DET_impact_per100']:.9f}|")
 a+=['','원두DET결과/역할/가격 자료는 수정하지 않는다. q3m..7,000,040와 X0..5,361,732의 검문된 전체 family, 법정minimum/Bird/RoomMLE/보호비용/미서명RT·전6범주 보존. Sekou·Okafor5,743,703 전액 유지·후속 Jordan/BKN자산거래 자동복사0. 15STD2TW/active12·원양수10/역할초·양팀2880초/14400선수초를 정확히 재사용.','',
 'Aldama 원유효RT는 선택된 합법 수락창에서 미수락만료/noUPC, 최소Oct15 요건과3m 예약을 보존한다. 미래비NBA·권리·새tender사실 재개방이며 무기한독점 인증이 아니다. Garza/Smith TW 추가NBAactivation0/급여현금0인증 아님. Suggs5/Livers38/Aldama37의 선택권리를 원번호/실제계약으로 치환하지 않는다.','',
 'Grant/Olynyk 등 양수10 가용성은 두후반날짜 위임건강모델. 실제thumb/knee/COVID/수술을 복사하거나 부재인증하지 않는다. 무사건 family는 명시 선택된 모델이며 실제 중간사건 부재증명이 아니다. 원Bagley/Lyles 및GrantPOR 이동은 미실행. 현재CHI Mark32/Caruso18/P32·선택된건강·단일March25 EB/BPM·홈2/연전.5,score·OTnull.','',
 '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트|완료|','|2|2020–21|완료|','|3|2021–23|DET후반2 선택·검문대기|','|4|장기커리어|미완|','|5|결말·구조|미완|','|6|집필규격·Pack|현행 등록기·Pack0|','|7|통합승인|CLOSED|','',
 '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰묶음5/6번까지4·v0.30 PARTIAL/CLOSED/원고0·전체macro3/실제임상·private가격인증false.','']
 return '\n'.join(a)
def validate(d,root=ROOT):
 try:return []if d==build(root)else['Saved laterDET differs from source-bound model']
 except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
 old=role_blocks;controls=[]
 def wrong(src):
  x=old(src);x[1]['positions']['PG'],x[1]['positions']['SG']=x[1]['positions']['SG'],x[1]['positions']['PG'];return x
 with patch(__name__+'.role_blocks',wrong):
  try:build()
  except ValueError:controls.append('RETURNED_ROLE_POSITION_SWAP')
  else:raise AssertionError('FalsePASS roles')
 return controls
def main():
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
 if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
 if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'LaterDET stale')
 print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_DET_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
