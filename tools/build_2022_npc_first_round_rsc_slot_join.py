"""Select29 NPC first RSCs and25 zero-budget reserve clearances; preserve all original costs."""
import argparse
import copy
import hashlib
import json
import re
from collections import Counter
from datetime import datetime,timedelta
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_npc_first_round_rsc_slot_join.py'
OUT='simulation/NBA_2022_NPC_FIRST_ROUND_RSC_SLOT_JOIN.json'
MD=OUT[:-5]+'.md'
PORT='simulation/NBA_2022_23_NPC_CONTRACT_PORTFOLIO.json'
PEER='reviews/NBA_2022_23_NPC_CONTRACT_PORTFOLIO_G11_INDEPENDENT_REVIEW_2026_10_08.json'
GLOBAL='simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json'
CHI='simulation/CHICAGO_2022_ROOKIE_SELECTED_EXECUTION.json'
AUTH='control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md'
PINS={PORT:'123d07df572ac4350e9528b3f0b913b3013ad4d51584c88a94e78051b9c7af19',
 PEER:'2cefc7d4e8d3af806975418e88e1c11cc6969a2b1e982b55cb32823fb02d8e05',
 GLOBAL:'93264d2dff86a58ad10ca6975315c6c2167961f94f2517b6f5f79fa3113f2af8',
 CHI:'3c06967cf8c7171f815819efd3b4a71fb88ac77db3ae8798b34afeeeae93ce1c',
 AUTH:'91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d'}
TEMP=Path('C:/Users/Storm Credit/AppData/Local/Temp')
PRIMARY=[
 ('2017_CBA',TEMP/'first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf','66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a',[210,241,294,295,303], 'Operative2022 rules: rookie exception, two guaranteed seasons/two separate options,120pct and hold replacement.'),
 ('2023_CBA_RETROSPECTIVE_SCALE_ONLY',TEMP/'fr-2023-cba-boundary-20261007/cba2023.pdf','bf178ca0f2d64f9dfe6fde095d3ae43d576b12e19ce7a679618d632584f7ab32',[32,631],'Retrospective2022-23 numeric baseline only;2023 rules not applied to2022 signings.'),
 ('2019_PUBLIC_BYLAWS_TEMPLATE',TEMP/'first-rebound-2019-bylaws.pdf','6accb3d9633e15e8559d13228c27ae7b3b0b81eac0894050b06256eea6da3464',[76],'Public48-hour waiver template, not a receipt or absence-of-claim certificate.')]
WAIVERS={'ATL':['Tony Snell'],'BOS':['Carsen Edwards'],'CLE':['Damyean Dotson'],
 'DEN':['Bol Bol'],'DET':['Rodney McGruder'],'GSW':['Kent Bazemore'],
 'HOU':['Avery Bradley','Khyri Thomas'],'IND':['Aaron Holiday'],
 'MEM':['Jontay Porter','John Konchar'],'MIL':['Mamadi Diakite'],'MIN':['Jake Layman'],
 'NOP':['Didi Louzada','Wes Iwundu'],'NYK':['Frank Ntilikina'],
 'OKC':['Charlie Brown Jr','Ty Jerome'],'ORL':['Ignas Brazdeikis'],'PHI':['George Hill'],
 'POR':['Harry Giles III'],'SAC':['Robert Woodard II'],'SAS':['DaQuan Jeffries'],
 'TOR':['Sam Dekker'],'WAS':['Anthony Gill']}
FORBIDDEN_RELEASES={'Jamal Murray','James Wiseman','Nahshon Hyland','Trey Murphy','Kai Jones','Ziaire Williams','Zach Collins','Ayo Dosunmu','Quentin Grimes','Udonis Haslem'}
NOTICE='2022-07-08T09:00:00-04:00';CLEAR='2022-07-10T09:00:00-04:00';SIGN='2022-07-11T09:00:00-04:00'

def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def h(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def sources():return {p:load(p) if p.endswith('.json') else text(p) for p in PINS}
def assert_sources(s):
 for p,pin in PINS.items():
  assert h(p)==pin,'Source pin differs '+p
  raw=text(p);assert s[p]==(json.loads(raw) if p.endswith('.json') else raw),'Returned source differs '+p
 assert s[PEER]['independent_review_completed']
 assert s[PEER]['source_sha256'][PORT]==PINS[PORT]
 for p,pin in s[PORT]['source_sha256'].items():assert h(p)==pin,'Portfolio source stale '+p
 assert len(s[PORT]['NPC_contract_rows'])==442 and len(s[PORT]['NPC_2022_rights'])==58
 assert s[PORT]['boundaries']['same_owner_routine_implementation_family_constructed']

def primary():
 import fitz
 evidence=[];bodies={}
 for name,p,pin,pages,scope in PRIMARY:
  assert hashlib.sha256(p.read_bytes()).hexdigest()==pin,'Primary bytes changed '+name
  doc=fitz.open(p);ts={n:doc[n-1].get_text().replace('\r\n','\n').replace('\r','\n') for n in pages}
  bodies[name]=ts
  evidence.append({'id':name,'cache_path':str(p),'raw_sha256':pin,'read_scope':scope,
   'PDF_one_based_page_text_LF_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest() for n,t in ts.items()}})
 t=bodies['2023_CBA_RETROSPECTIVE_SCALE_ONLY'][631]
 values=re.findall(r'(?m)^\s*(\d+)\s*\n\s*([\d,]+)\s*\n\s*([\d,]+)\s*\n\s*([\d,]+)\s*\n\s*(\d+\.\d+)%\s*\n\s*(\d+\.\d+)%',t)
 table={int(n):[int(a.replace(',','')),int(b.replace(',','')),int(c.replace(',','')),Fraction(x),Fraction(y)] for n,a,b,c,x,y in values}
 assert sorted(table)==list(range(1,31)) and table[18][:3]==[2659500,2792300,2925400]
 assert [int(Fraction(v)*6/5) for v in table[18][:3]]==[3191400,3350760,3510480]
 assert table[1][:3]==[9212600,9673400,10134000]
 assert 'one hundred twenty percent (120%)' in bodies['2017_CBA'][294]
 assert 'July 15' in bodies['2017_CBA'][303]
 assert 'forty-eight (48)' in bodies['2019_PUBLIC_BYLAWS_TEMPLATE'][76]
 return table,evidence

def roster_plan(s):
 p=s[PORT];g=s[GLOBAL]
 first=[r for r in p['NPC_2022_rights'] if r['round']==1]
 assert len(first)==29 and 18 not in [r['pick'] for r in first]
 by_holder={t:[r for r in first if r['candidate_owner']==t] for t in p['team_functions']}
 out={}
 for t,old in p['team_functions'].items():
  std=old['standard'];rs=by_holder[t];release=list(WAIVERS.get(t,[]))
  assert len(release)==max(0,len(std)+len(rs)-15),'Wrong number of clearances '+t
  assert set(release)<=set(old.get('zero_minute_standard_reserves',[])),'Waiver changes positive role '+t
  assert not (set(release)&FORBIDDEN_RELEASES),'High-cost future core released by zero-budget heuristic'
  new=[n for n in std if n not in release]+[r['player'] for r in rs]
  assert 14<=len(new)<=15 and len(set(new))==len(new)
  templates=[]
  for oldt in old.get('capacity_templates',[]):
   positive=oldt['positive_player_seconds']
   assert not (set(positive)&set(release)) and set(positive)<=set(new)
   active=list(positive)+[n for n in new if n not in positive][:max(0,12-len(positive))]
   assert 12<=len(active)<=15 and set(active)<=set(new)
   templates.append({'source_template':oldt['id'],'source_clock_pointer':oldt['source_clock_pointer'],
    'unchanged_positive_player_seconds':copy.deepcopy(positive),'nominal_active':active,
    'nominal_inactive':[n for n in new if n not in active],'new_rookie_positive_minutes_selected':False,
    'old_FY21_health_or_winners_admitted_as_FY22':False})
  out[t]={'standard':new,'TW':copy.deepcopy(old['TW']),'source_standard':copy.deepcopy(std),
   'cleared_reserves':release,'first_RSC_players':[r['player'] for r in rs],
   'first_RSC_picks':[r['pick'] for r in rs],'nominal_template_carriers':templates,
   'calendar_dates_unchanged':len(old['dates'])==82,'roster_effective_from':SIGN,
   'rookie_participation_or_health_selected':False}
 assert sum(len(q['standard']) for q in out.values())==449
 assert sum(len(q['TW']) for q in out.values())==2
 assert out['CHI']['standard']==p['team_functions']['CHI']['standard'] and out['CHI']['TW']==p['team_functions']['CHI']['TW']
 return first,out

def contract(r,table):
 a,b,c,x,y=table[r['pick']];bases=[int(Fraction(v)*6/5) for v in [a,b,c]]
 return {'pick':r['pick'],'player':r['player'],'owner':r['candidate_owner'],
  'required_tender_date':'2022-07-07','RT100_then_separate_consensual_RSC120':True,
  'signed_at':SIGN,'roster_class':'STANDARD','standard_slots_added':1,
  'law':'2017_VII6h_VIII1','first_season':'2022-23','guaranteed_capyears':[2022,2023],
  'guaranteed_fiscal_obligation_through':'2024-06-30','service_end_not_inferred_from_fiscal_end':True,
  'unexercised_option_capyears':[2024,2025],'base_percent':120,'scale_values_dollars':[a,b,c],
  'base_first_three_years_dollars':bases,'year4_if_option_exercised_exact':str(Fraction(bases[2])*(1+x/100)),
  'year4_NBA_rounding_certified':False,'year4_and_QO_percent_increases':[str(x),str(y)],
  'new_bonuses_loan_buyout':0,'first_two_base_protection_percent':100,
  'future_options_automatically_exercised':False,
  'cap_hold_replacement':{'prior_normal_unsigned_first':int(Fraction(a)*6/5),
   'prior_apron_outstanding_RT100':a,'signed_normal_and_apron_salary':bases[0],
   'normal_delta_signed_minus_same_claim_hold':0,'apron_delta_signed_minus_RT':bases[0]-a,
   'same_claim_unsigned_hold_removed_once':True,'waived_incumbent_liabilities_subtracted_as_cash_saving':False},
  'fictional_consent_and_legal_participation_selected':True,'actual_receipt_or_real_player_consent_certified':False,
  'full82_minutes_starts_awards_or_statistics_selected':False}

def waiver(player,team,port):
 r=next(q for q in port['NPC_contract_rows'] if q['player']==player and q['candidate_owner']==team)
 return {'player':player,'owner_before_clearance':team,'notice_at':NOTICE,'claim_deadline_at':CLEAR,
  'claim_window_elapsed_hours':48,'fictional_no_claim_selected':True,'new_owner_or_assignment':None,
  'original_contract_row_id':r['id'],'original_contract_fields':copy.deepcopy(r['original_contract_fields']),
  'all_original_Gamma_reserved':True,'all_new_July7_renewal_or_option_protected_liabilities_reserved':True,
  'protected_salary_reservation_function':'All original Gamma plus full protected Salary/bonuses of any selected July7 minimum renewal or existing timely option. Live-to-dead reclassification does not cancel them.',
  'remaining_guaranteed_future_salary_reserved':True,'cash_buyout_stretch_setoff_or_refund_selected':False,
  'exact_protection_or_cash_payment_certified':False,'actual_waiver_receipt_or_no_claim_certified':False,
  'old_all_template_positive_regulation_seconds':0}

def build():
 s=sources();assert_sources(s);table,evidence=primary();first,teams=roster_plan(s)
 assert datetime.fromisoformat(CLEAR)-datetime.fromisoformat(NOTICE)==timedelta(hours=48)
 assert datetime.fromisoformat(SIGN)>datetime.fromisoformat(CLEAR)
 contracts=[contract(r,table) for r in first]
 for q,r in zip(contracts,first,strict=True):
  assert q['owner']==r['candidate_owner'] and q['player']==r['player'] and q['pick']==r['pick']
  a,b,c,x,y=table[r['pick']]
  assert q['signed_at']==SIGN and q['standard_slots_added']==1 and q['base_percent']==120
  assert q['base_first_three_years_dollars']==[int(Fraction(v)*6/5) for v in [a,b,c]]
  assert q['guaranteed_capyears']==[2022,2023] and q['unexercised_option_capyears']==[2024,2025]
  assert q['new_bonuses_loan_buyout']==0 and q['first_two_base_protection_percent']==100 and not q['future_options_automatically_exercised']
  hold=q['cap_hold_replacement'];assert hold=={'prior_normal_unsigned_first':int(Fraction(a)*6/5),'prior_apron_outstanding_RT100':a,'signed_normal_and_apron_salary':int(Fraction(a)*6/5),'normal_delta_signed_minus_same_claim_hold':0,'apron_delta_signed_minus_RT':int(Fraction(a)*6/5)-a,'same_claim_unsigned_hold_removed_once':True,'waived_incumbent_liabilities_subtracted_as_cash_saving':False}
 clearances=[waiver(n,t,s[PORT]) for t,names in WAIVERS.items() for n in names]
 assert len(clearances)==25
 for q in clearances:
  assert q['notice_at']==NOTICE and q['claim_deadline_at']==CLEAR and q['claim_window_elapsed_hours']==48
  assert q['all_original_Gamma_reserved'] and q['all_new_July7_renewal_or_option_protected_liabilities_reserved'] and q['remaining_guaranteed_future_salary_reserved']
  assert q['new_owner_or_assignment']is None and not q['cash_buyout_stretch_setoff_or_refund_selected']
  src=next(r for r in s[PORT]['NPC_contract_rows'] if r['id']==q['original_contract_row_id'])
  assert q['original_contract_fields']==src['original_contract_fields'] and q['player']==src['player'] and q['owner_before_clearance']==src['candidate_owner']
 # Verify roster output against physical portfolio, rather than trusting a substituted roster constructor.
 pp=json.loads(text(PORT))
 for t,q in teams.items():
  old=pp['team_functions'][t]
  picks=[r for r in first if r['candidate_owner']==t]
  expected=[n for n in old['standard'] if n not in WAIVERS.get(t,[])]+[r['player'] for r in picks]
  assert q['standard']==expected and q['cleared_reserves']==WAIVERS.get(t,[]) and q['first_RSC_picks']==[r['pick'] for r in picks]
  assert q['TW']==old['TW'] and q['source_standard']==old['standard']
  for carrier,orig in zip(q['nominal_template_carriers'],old.get('capacity_templates',[]),strict=True):
   assert carrier['unchanged_positive_player_seconds']==orig['positive_player_seconds']
   assert set(carrier['nominal_active'])<=set(expected) and 12<=len(carrier['nominal_active'])<=15
   assert set(orig['positive_player_seconds'])<=set(carrier['nominal_active'])
   assert carrier['source_clock_pointer']==orig['source_clock_pointer'] and carrier['source_template']==orig['id']
   assert set(carrier['nominal_inactive'])==set(expected)-set(carrier['nominal_active'])
 owners=[(n,t) for t,q in teams.items() for n in q['standard']+q['TW']]
 assert len(owners)==len({n for n,_ in owners})==451
 return {'id':'NBA_2022_NPC_FIRST_ROUND_RSC_SLOT_JOIN','baseline_main':'d6bd960568fce5687bd2843da6f51d0fe9c18d3c',
  'status':'ROOT_SELECTED_ROUTINE_FIRST_RSC_AND_SLOTS_PENDING_INDEPENDENT_REVIEW',
  'source_sha256':{**PINS,SELF:h(SELF)},'hash_method':'UTF8_BOM_STRIPPED_CRLF_CR_TO_LF',
  'primary_evidence':evidence,'selection_basis':'Existing delegated NPC contract/roster implementation; no new important protagonist direction.',
  'scale_units':'Use the comma-formatted dollar values in official2022-23 numeric baseline; the PDF ($000S) heading does not justify multiplying these values. Cross-check pick18 original selected3191400 at120pct.',
  'selected_first_RSCs':contracts,'selected_zero_budget_reserve_clearances':clearances,'team_registration':teams,
  'summary':{'NPC_first_RSCs':29,'all_first_RSCs_including_CHI':30,'NPC_zero_budget_reserve_clearances':25,
   'existing_empty_STD_slots_used':4,'all_live_STD':449,'NPC_live_STD':434,'all_live_TW':2,'all_unique_live_owners':451,
   'first_year_new_RSC_salary_total':sum(q['base_first_three_years_dollars'][0] for q in contracts),
   'normal_first_claim_hold_replacement_delta_total':0,
   'apron_signed_minus_existing_RT_delta_total':sum(q['cap_hold_replacement']['apron_delta_signed_minus_RT'] for q in contracts),
   'unchanged_old_positive_template_carriers':sum(len(q['nominal_template_carriers']) for q in teams.values()),
   'new_rookie_participation_or_complete_games_selected':0,'NPC_second_round_rights_remaining':29},
  'remaining_finite_inputs':['Chosen rookie positive role/minute/availability/productivity and recompiled paired48/240 clocks/results',
   'Credible core renewal price family for applicable expiry cases; a legal minimum sensitivity is not market plausibility PASS',
   'Full normal/apron original Gamma and six-cost family; protected waiver obligations never a cash saving',
   'Second-round timed tender/acceptance or other lawful route and post2023draft rights/costs'],
  'bounds':{'whole_FY22_23_cost_health_or_results_complete':False,'independent_review_completed':False,
   'old_FY21_results_or_health_automatically_reused':False,'actual_player_consent_or_private_receipts_certified':False,
   'CHI_Kessler_Ellis_R1_and_H22_changed':False,'new_franchise_MVP_title_count_or_ending_change':False,
   'N23':None,'A23':None,'whole_macro3_G13_G14_complete':False},
  'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','actual_context_packs':0,'manuscript_allowed':False}

def render(d):
 s=d['summary'];lines=['# 2022 NPC 첫 RSC와 슬롯 실행','',
 '첫RSC29명의 루틴 가상 합의를 선택해 전원 미입단 조건을 해소한다. 계약·등록 선택이며 모든 신인의82경기 기용 완료는 아니다. CHI Kessler/Ellis/R1/H22는 보존한다.','',
 '| 항목 | 현행 |','|---|---:|']
 lines += [f'| {k} | {v} |' for k,v in s.items()]
 lines += ['', '| pick | 선수 | 팀 | 첫해120% base |','|---:|---|---|---:|']
 lines += [f"| {q['pick']} | {q['player']} | {q['owner']} | {q['base_first_three_years_dollars'][0]:,} |" for q in d['selected_first_RSCs']]
 lines += ['', '## 날짜와 원비용', '',
  '가상July7 RT100% 뒤 필요한 zero-positive reserve25명에 July8금09ET waiver→July10일09ET48시간 미청구→July11월09ET 별도합의120% RSC를 연결했다. 기존빈STD4칸도 쓴다. 첫2년 보장·다음2년 별도옵션이며 미래옵션 자동행사0이다.',
  '원Gamma와July7 신규minimum/옵션의 보호채무 및 미래보장액을 전부 보존한다. 방출을 현금할인·보장삭제·stretch로 만들지 않는다. 원firstclaim normal120% hold는 새signed120%로 한 번 교체하고 apron RT100%도signed120%로 한 번 교체한다. 이 delta를 전체TeamSalary 인증이나서명전reserve0으로 해석하지 않는다.',
  '2023 CBA631은2022–23 숫자회수에만 쓰며 계약법은2017이다. Pick18의 기존Kessler3,191,400과단위를대조했다. PDF헤더로 값에1000을곱하지 않는다.', '',
  '## 남은 실행', '',
  '신인 역할·분·가용과 신규5인 동시시계 및 전체결과를 다음 소비자가 선택해야 한다. 기존33개 시계의 양수선수는 제거하지 않았다. 핵심선수 시장가격/동의 가족, 전체6비용,2R29권리와2023후속은 미완료이다. 임상/실제접수/현실stats나 전체시즌 완료를 주장하지 않는다.', '',
  '[원NPC 포트폴리오](NBA_2022_23_NPC_CONTRACT_PORTFOLIO.md) · [포트폴리오 독립검문](../'+PEER+')', '',
  '미완료 큰 묶음5 /6번까지4. Pack0·원고0·v0.30 PARTIAL·설계/원고CLOSED.', '']
 return '\n'.join(lines)

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();d=build()
 if a.write:
  (ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
  (ROOT/MD).write_text(render(d),encoding='utf-8',newline='\n')
 if a.check:assert load(OUT)==d and text(MD)==render(d),'Saved artifact differs'
 print(json.dumps({'current':True,'summary':d['summary']},ensure_ascii=False))

if __name__=='__main__':main()
