"""Consume named prior claims and omitted trades for the 2023 Chicago budget.

Historical public transfers are evidence; preservation through the changed world
is an explicit delegated fictional choice. No unpublished contract certification.
"""
from pathlib import Path
from copy import deepcopy
import argparse, hashlib, json, re

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_chicago_2023_named_draft_claims.py'
OUT = 'research/CHICAGO_2023_NAMED_DRAFT_CLAIMS_AND_COST_PORTS_2026_10_08.json'
PINS = {
 'control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md':'91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d',
 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json':'253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088',
 'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json':'c0166bba7a0874aa08dfa88e7d00c0f0d0e237ca2090459ddd6167cf1353c5ea',
 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json':'9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce',
 'research/BKN_WAS_2021_P1_NAMED_RIGHTS_BRIDGE_2026_10_07.json':'fb5803cf261ca7f0f81bf20413276df997de492c007886410d984dc6fcc024d0',
 'research/CHICAGO_2021_THREE_ORIGINAL_TRADES_DOWNSTREAM_2026_10_07.json':'28cb75e82a8a0bb47309a5babb1daac0ae30dcdbb07d7218546c8bfe1327cdea',
 'simulation/NBA_2022_PUBLIC_CONTROL_EXECUTION_FAMILY.json':'86ac9e85b06a607363f5c7a6bd6fac29a8a5dbd89fff803e2a440897afd3337c',
}

def need(v, message):
 if not v: raise AssertionError(message)

def norm(p):
 return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')

def sha(p):
 return hashlib.sha256(norm(p).encode()).hexdigest()

def sources():
 s = {}
 for p, h in PINS.items():
  need(sha(ROOT/p)==h,'Physical source changed: '+p)
  if p.endswith('.json'): s[p]=json.loads(norm(ROOT/p))
 need(s['canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json']['selected']['route']=='M1','M1 route changed')
 need(s['canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json']['selected']['route']=='G1A_PLUS_M1','A route changed')
 f5=s['canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json']['selected']['F5_MCGEE']
 need('do not execute' in f5 and 'two-second-round' in f5,'F5 omission absent')
 effects=s['research/CHICAGO_2021_THREE_ORIGINAL_TRADES_DOWNSTREAM_2026_10_07.json']['transaction_effects']
 need(len(effects)==3 and all(x['selected_original_transaction_executed'] is False for x in effects),'Original Chicago trade copied')
 omitted=s['simulation/NBA_2022_PUBLIC_CONTROL_EXECUTION_FAMILY.json']['positive_and_omission_dependencies']['nonselected_original_deadline_atoms']
 need('WAS/SAS Dinwiddie-fiveway' in omitted,'P1 omission missing')
 return s

def primary(s):
 old=s['research/BKN_WAS_2021_P1_NAMED_RIGHTS_BRIDGE_2026_10_07.json']
 out=[]
 for source_id in ['PORTER2019','SATO2019']:
  r=deepcopy(next(x for x in old['sources'] if x['id']==source_id))
  b=Path(r['cache_path']).read_bytes()
  need(hashlib.sha256(b).hexdigest()==r['raw_sha256'],'Raw primary changed')
  match=re.search(r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>',b.decode('utf-8'),re.S)
  need(match is not None,'Serialized primary body missing')
  data=json.loads(match.group(1))['props']['pageProps']
  body=data['article']['contentText'] if source_id=='PORTER2019' else data['pageObject']['contentStructured'][0]['text']
  need(hashlib.sha256(body.encode()).hexdigest()==r['observed_field_UTF8_sha256'],'Primary field changed')
  need('2023' in body and ('protected' in body if source_id=='PORTER2019' else 'removed the protection' in body),'Historical claim term missing')
  r['current_consumer_body_read']=True
  out.append(r)
 return out

def claims():
 return [
  {'id':'CHI_2023_1R','origin':'CHI','year':2023,'round':1,'selected_holder':'CHI',
   'basis':'Original Chicago first retained; Vucevic outgoing edge omitted; selected no intervening transfer family.',
   'historical_ORL_11_copied':False,'selected_draft_position':None,'position_domain':'NONLOTTERY_IF_QUALIFIED_ELSE_LOTTERY_DRAW',
   'new_STD_rookie_reservation':1},
  {'id':'CHI_2023_2R','origin':'CHI','year':2023,'round':2,'selected_holder':'WAS',
   'public_prior_holder':'WAS','protection':'REMOVED_2019_07_07',
   'basis':'New explicitly selected prior-claim preservation family from public Porter/Satoransky releases; omitted P1 does not forward the claim to LAL.',
   'P1_candidate_E1_E2_selected':False,'historical_later_rank_copied':False,'new_CHI_STD_rookie_reservation':0},
  {'id':'DEN_2023_2R_TO_CHI_ORIGINAL_MARKKANEN','origin':'DEN','year':2023,'round':2,'selected_CHI_receipt':False,
   'basis':'M1 retains Markkanen in Chicago; the original three-team Markkanen transaction is absent.',
   'F5_DEN_CLE_transfer_executed':False,'DEN_final_holder_certified':False,'independent_prior_claims_unrelated_to_omitted_trades_preserved':True,
   'new_CHI_STD_rookie_reservation':0},
 ]

def budget(rows):
 by={x['id']:x for x in rows}
 need(len(rows)==3 and len(by)==3,'Named claims duplicated/deleted')
 first=by['CHI_2023_1R'];second=by['CHI_2023_2R'];incoming=by['DEN_2023_2R_TO_CHI_ORIGINAL_MARKKANEN']
 need(first['selected_holder']=='CHI' and first['new_STD_rookie_reservation']==1 and first['selected_draft_position'] is None and not first['historical_ORL_11_copied'],'Own first provenance/rank corrupted')
 need(second['selected_holder']=='WAS' and second['public_prior_holder']=='WAS' and second['protection']=='REMOVED_2019_07_07' and not second['P1_candidate_E1_E2_selected'],'Prior second forwarded/returned incorrectly')
 need(second['new_CHI_STD_rookie_reservation']==0,'Outgoing second minted as Chicago asset')
 need(incoming['selected_CHI_receipt'] is False and incoming['F5_DEN_CLE_transfer_executed'] is False and incoming['independent_prior_claims_unrelated_to_omitted_trades_preserved'] is True and incoming['new_CHI_STD_rookie_reservation']==0,'Omitted receipt/other lien corrupted')
 return {'CHI_own_retained_first':1,'CHI_own_second_available':0,'CHI_incoming_DEN_second':0,
         'CHI_new_rookie_STD_slots':1,'CHI_2023_drafted_second_rounders':0,
         'N23':{'kind':'POSITIVE_FIRST_ROUND_HOLD_OR_SALARY_FUNCTION','value':None,'null_is_zero':False},
         'A23':{'kind':'POSITIVE_FIRST_ROUND_APRON_CHARGE_FUNCTION','value':None,'null_is_zero':False},
         'first_rank_draftee_and_RSC_price_selected':False,'all_original_Gamma_and_other_costs_preserved':True}

def build():
 s=sources()
 physical_sources={p:json.loads(norm(ROOT/p)) for p in PINS if p.endswith('.json')}
 need(s==physical_sources,'Returned authority/source differs from pinned physical records')
 historical=primary(s); rows=claims()
 # Consumer verifies the metadata it actually publishes, after body validation.
 # A changed helper return must not reverse the observed historical summary.
 original=json.loads(norm(ROOT/'research/BKN_WAS_2021_P1_NAMED_RIGHTS_BRIDGE_2026_10_07.json'))
 expected=[{**next(x for x in original['sources'] if x['id']==ident),'current_consumer_body_read':True}
           for ident in ['PORTER2019','SATO2019']]
 need(historical==expected,'Returned primary metadata differs from pinned physical record')
 return {'id':'CHI_2023_NAMED_CLAIMS_AND_COST_PORTS','baseline_main':'241821ba24936ee788320844822af5a3f32ef69c',
  'status':'AUTHOR_DELEGATED_FICTIONAL_PRIOR_CLAIM_PRESERVATION_SELECTED',
  'source_sha256':{**PINS,SELF:sha(ROOT/SELF)},'historical_primary':historical,
  'classification':{'FACT':'Public 2019 protected transfer and removal of protection.',
   'INFERENCE':'Omitted original deals cannot create their outgoing or incoming pick edges.',
   'FICTION_DESIGN_SELECTED':'Named prior claim and no intervening transfer family carried into the selected 2023 world.',
   'AUTHOR_LOCKED':'M1 Markkanen retention; A growth core; F5 omission remain unchanged.'},
  'selected_preservation_family':{'dated_window_end':'2023-06-22','CHI_own_first_no_new_transfer':True,
   'CHI_prior_second_WAS_no_new_transfer':True,'no_new_unreported_claim_created':True,
   'public_history_is_not_alternative_private_ledger_certification':True},
  'named_claims':rows,'Chicago_cost_and_slot_ports':budget(rows),
  'sanction_causality':{'all_original_Markkanen_trade_edges_copied':False,'original_next_available_second_penalty_primary':'https://pr.nba.com/bulls-heat-penalties-free-agency/',
   'historical_original_Lonzo_contact_edge_copied':False,'new_fiction_lawful_contact_family':True,
   'no_historical_penalty_is_not_new_Chicago_asset':True,'all_NBA_2023_forfeitures_or_60_picks_certified':False},
  'other_historical_crosschecks':[{'url':'https://www.nba.com/news/cavs-acquire-lauri-markkanen-from-bulls-in-3-team-trade',
   'root_web_body_read':True,'fact_summary':'Original Markkanen transaction included a Denver-origin 2023 second for Chicago.',
   'raw_response_archived':False}],
  'remaining':['First-round rank and draftee selection after 2023 postseason/draw; positive N23/A23 price join.',
   'Global 2023 origin/control portfolio and any other Denver prior claims are outside this Chicago consumer.'],
  'certification':{'named_fictional_CHI_draft_asset_and_slot_scope_complete':True,'actual_private_asset_ledger_certified':False,
   'draft_price_and_total_cost_complete':False,'whole_cost_certified':False,'whole_career_complete':False,'manuscript_allowed':False,'gate':'CLOSED','freeze':'v0.30 PARTIAL'}}

def self_test():
 rows=claims();budget(rows); rejected=[]
 for name,idx,key,value in [('MINT_OWN_SECOND',1,'selected_holder','CHI'),('COPY_LAL_P1',1,'selected_holder','LAL'),
  ('COPY_DEN_RECEIPT',2,'selected_CHI_receipt',True),('COPY_ORL_RANK',0,'selected_draft_position',11),
  ('ERASE_OTHER_LIENS',2,'independent_prior_claims_unrelated_to_omitted_trades_preserved',False)]:
  x=deepcopy(rows);x[idx][key]=value
  try:budget(x)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('FALSE_PASS '+name)
 return rejected

def markdown(v):
 return '''# Chicago 2023 명명 드래프트 권리·비용 인계

2019 공개 양도와 보호 제거는 역사 사실이다. 그 선행 청구를 변경된 세계의 2023년까지 유지하는 것은 이번에 명시적으로 선택한 가상 가족이다. 이전 P1 후보를 실행된 거래로 승격하지 않는다.

| 청구 | 이번 선택 | Chicago 새 신인 슬롯 |
|---|---|---:|
| CHI 2023 1R | CHI 보유: 원 Vučević 거래 생략, 새 양도 없음 | 1 |
| CHI 2023 2R | WAS 보유: 2019 양도·보호 제거 유지, P1 생략 | 0 |
| DEN 2023 2R의 원 Markkanen 경유 수취 | M1 잔류로 원 수취 없음; F5 이전도 생략 | 0 |

따라서 선택된 Chicago 드래프트 예산은 **1R 1개 / 2R 0개 / 새 STD 예약 1칸**이다. 실제 ORL 11번, 실제 LAL 경유 순번, 원 Denver 최종 소유자는 복사하지 않았다. 생략한 Markkanen 거래의 모든 원 양도는 새 실행으로 복사하지 않는다. 그 거래와 독립적인 기존 청구·보호 채무는 유지한다.

원 Lonzo 관련 제재 원인을 복사하지 않는다는 이유로 새로운 Chicago 2R이 생기지는 않는다. 다른 팀의 2023 제재와 전체 60개 청구는 이 문서의 인증 범위가 아니다.

N23/A23는 순번·계약 선택 뒤 결합할 **양수 함수**로 남는다. null은 0이 아니며, 전체 급여·현실 영수증은 인증하지 않는다.

## 원천과 권위

- [2019 Porter 공개 교환](https://www.nba.com/news/bulls-trade-wizards-porter-official-release): CHI 2023 보호된 2R 양도.
- [2019 Satoransky 공개 교환](https://www.nba.com/wizards/wizards-acquire-draft-pick-chicago): 해당 2023 보호 제거. 두 원문은 캐시의 실제 serialized body와 SHA를 재검문했다.
- [원 Markkanen 거래](https://www.nba.com/news/cavs-acquire-lauri-markkanen-from-bulls-in-3-team-trade): Denver 경유 2023 수취. 이번 M1에서는 원거래 없음.
- [원 조기 협상 제재](https://pr.nba.com/bulls-heat-penalties-free-agency/): 다음 가능한 2R 제재. 가상 선택과 사실을 구별한다.
- [기존 위임](../control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md), [M1](../canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json), [A](../canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json), [F5](../canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json).

다음은 2023 PO·순번과 실제 새 계약 인계다. 장기 커리어·원고 완료 인증은 아니다. v0.30 PARTIAL / CLOSED / 원고 0.
'''

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
 v=build(); m=markdown(v)
 if args.self_test: print(json.dumps({'negative_cases_rejected':self_test()}))
 if args.write:
  (ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/OUT[:-5]).with_suffix('.md').write_text(m,encoding='utf-8')
 if args.check:
  need(json.loads(norm(ROOT/OUT))==v,'Frozen result stale');need(norm((ROOT/OUT[:-5]).with_suffix('.md'))==m,'MD stale')
 print(json.dumps({'claims':3,'CHI_R1':1,'CHI_R2':0,'new_STD_slots':1,'N23_A23_positive_unpriced':True}))
