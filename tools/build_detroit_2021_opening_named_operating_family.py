"""Finite named opening candidates: exact conditional ledger, not a whole cost certificate."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
from unittest.mock import patch
import argparse,copy,hashlib,json
import fitz
ROOT=Path(__file__).resolve().parents[1]
OUT='research/DETROIT_2021_OPENING_NAMED_OPERATING_FAMILY_2026_10_07.json'
MD=OUT[:-5]+'.md'
SELF='tools/build_detroit_2021_opening_named_operating_family.py'
REC='research/CHICAGO_2021_22_OPENING_DET_PAIRED_INPUT_RECOVERY_2026_10_07.json'
AF='research/O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.json'
SLOT='simulation/O15G15BM_DETROIT_OPENING_SLOT_OPTIONS.json'
AL='research/O15G15AL_DETROIT_PRE_OLYNYK_ROSTER_CHARGE_SEQUENCE.json'
AQ='research/O15G15AQ_DETROIT_LEE_CAP_ROOM_AND_NONBIRD_ROUTE.json'
AR='research/O15G15AR_DETROIT_NAMED_EXIT_AND_ROSTER_CHARGE.json'
PAIRED='simulation/CHICAGO_2021_22_PAIRED_INPUTS.json'
PATHS=[REC,AF,SLOT,AL,AQ,AR,PAIRED,'research/O15G15AK_DETROIT_AUG6_RIGHTS_AND_WAIVER_TIMING.md','research/O15G15AO_DETROIT_DISCLOSED_AGREEMENT_CAP_TIMING.md','research/O15G15BM_DETROIT_OPENING_SLOT_TWO_NAMED_OPTIONS.md','research/TWO_WAY_2021_22_RULE_PERIOD_EVIDENCE.json']
PINS={'research/CHICAGO_2021_22_OPENING_DET_PAIRED_INPUT_RECOVERY_2026_10_07.json': 'e731ab02a83e1135137da08a5384afbc077111cddb5a7d6ad8a4ba8f921e9f70', 'research/O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.json': 'eb90c8275ad5f3e57146fc3981f1739c9e0a23e687e3c5d2331e1117ac41a672', 'simulation/O15G15BM_DETROIT_OPENING_SLOT_OPTIONS.json': 'ba7ae4604a90c715130f96a127fcbe7616f4fd6430068fc3742729b1761a2ed9', 'research/O15G15AL_DETROIT_PRE_OLYNYK_ROSTER_CHARGE_SEQUENCE.json': 'cd0d31fced740134f94f34d1a6ce7b24c1205ce9360be3ae61e2d4abf43253b2', 'research/O15G15AQ_DETROIT_LEE_CAP_ROOM_AND_NONBIRD_ROUTE.json': '6b4806825d623e445f17a093239800a8f49f7841266244129818275681a622fa', 'research/O15G15AR_DETROIT_NAMED_EXIT_AND_ROSTER_CHARGE.json': '9f75d9af0af324303dc670249b023f69005dd3fb2624edf7322c4e2791469ac5', 'simulation/CHICAGO_2021_22_PAIRED_INPUTS.json': 'db727ddc89e354da7603c2563aaa4b58d9b543e124b0c4bd9de9df45d7ea9c6f', 'research/O15G15AK_DETROIT_AUG6_RIGHTS_AND_WAIVER_TIMING.md': '9c306fe85a0e85181cc6330dc06de36ea90db1a349caeca9ca72b04a7a8cb6ce', 'research/O15G15AO_DETROIT_DISCLOSED_AGREEMENT_CAP_TIMING.md': '87e71f8ceb114521ae92f143724bfa5873178d2b4c6ead145717c05164292c93', 'research/O15G15BM_DETROIT_OPENING_SLOT_TWO_NAMED_OPTIONS.md': '9bef308ed89ff7e4899bc0ffc3179305f61066e67c2a0df844ce0f6c84304d47', 'research/TWO_WAY_2021_22_RULE_PERIOD_EVIDENCE.json': 'e615d2cce356be8db1b0e65eb174b718789a4650a459c1ec2f69118be1cb1e26'}
CBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
MINRAW=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-minimum-year2-20261007/hoopsrumors_2021minimum.html')
CBA_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
MIN_SHA='e293e8e6be1e05be4f33cf8983feece21885da20d11fef9ff7f7483f2fb2aae4'
BASELINE='ae8cc87d1f35e86c6c52a68dfa5766422bb137a3'
def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def policy():
 return {'selected':False,'branch':'B_NO_LYLES_AND_MINIMUM_EXCEPTION_REPLACEMENTS','new_Lyles_agreement_or_contract':False,'NBA_first_tender_Aldama_must_be_accounted_separately':True,'Aldama_valid_tender_delivery_within_operative_window_and_not_accepted_at_opening':True,'room_MLE_for_Joseph_only':4910000,'room_MLE_years':2,'room_MLE_raise_percent':5,'NTMLE_or_BAE_combined_with_roomMLE':False,'new_minimum_exception_years':2,'new_minimum_exception_bonus':0,'new_Olynyk_years':3,'new_Olynyk_bonus':0,'new_Olynyk_raise_percent':5,'new_Olynyk_base_lower_candidate':3000000,'legacy_2020_rookie_base_reduction':False,'original_unreported_costs_set_zero':False,'whole_source_supported_cost_family_pass':False,'actual_acceptance':False}
FIXED=copy.deepcopy(policy())
def checked_policy():
 p=policy();assert p==FIXED,'Routine candidate policy changed';return p

def source_inputs():
 assert all(sha(p)==h for p,h in PINS.items()),'Source SHA stale'
 r=load(REC);assert r['verification']['independent_review_completed']is True
 # Rebind actual fields, not only hashes or cached summaries.
 al=load(AL);aq=load(AQ);ar=load(AR);slot=load(SLOT)
 assert (al['cap'],al['alternate_candidate_team_salary_before'],al['alternate_nominal_room_before'],al['olynyk_first_year_candidate'])==(112414000,100052228,12361772,12195122),'Named salary input changed'
 assert aq['saben_lee_incremental_team_salary_candidate']==563807 and aq['frank_qo_candidate']==1939350
 assert ar['historical_september_jordan_trade_only']['incoming_first_year_salary_candidate']==9881598
 assert ar['outgoing_salary_candidates']=={'Sekou Doumbouya':3613680,'Jahlil Okafor':2130023}
 assert slot['options']['B_lyles_not_signed']['remove_from_standard']=='Trey Lyles'
 det=next(x for x in load(PAIRED)['rotations']if x['id']=='DET_0022100004');assert det['position_minutes']==r['regulation_pair_comparison']['DET_existing_G14_candidate']['position_minutes']
 af=load(AF);std=af['historical_august_12_retained']+af['historical_august_12_added_or_resigned']
 for old,new in zip(af['conditional_same_other_events']['replaced_historical_players'],af['conditional_same_other_events']['replacement_players']):std[std.index(old)]=new
 std.append('Mason Plumlee');counts=[len(std)]
 for event in af['historical_events_after_august_12']:
  for name in event['out']:std.remove(name)
  std.extend(event['in']);counts.append(len(std))
 assert counts==[16,17,16,15,16] and std==r['opening_roster_recovery']['same_other_events_standard_candidate'],'Roster source transport changed'
 for row in r['opening_roster_recovery']['named_slot_candidates']:
  option=slot['options'][row['id']]
  assert row['standard_candidate']==[n for n in std if n!=option['remove_from_standard']] and row['two_way_candidate']==option['two_way'],'Named slot source changed'
 assert r['game']=={'game_id':'0022100004','candidate_date':'2021-10-20','home':'DET','away':'CHI','same_observed_calendar_is_hypothesis':True,'score':None,'winner':None,'health_selected':False}
 return r,al,aq,ar,slot,det

def rules():
 assert hashlib.sha256(CBA.read_bytes()).hexdigest()==CBA_SHA
 assert hashlib.sha256(MINRAW.read_bytes()).hexdigest()==MIN_SHA
 doc=fitz.open(CBA);pages=[55,54,206,207,208,209,210,211,212,213,223,231,232,233,238,239,240,241,249,250,303,304,412]
 hashes={str(n):hashlib.sha256(doc[n-1].get_text().encode()).hexdigest()for n in pages}
 assert 'not to exceed two (2)' in doc[231].get_text()
 assert 'with no bonuses' in doc[232].get_text()
 assert 'prohibited' in doc[231].get_text() and 'Bi-annual' in doc[231].get_text()
 return {'CBA':{'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(CBA),'raw_sha256':CBA_SHA,'PDF_1based_fitz_text_sha256':hashes},'minimum_table':{'url':'https://www.hoopsrumors.com/2021/08/nba-minimum-salaries-for-2021-22.html','cache_path':str(MINRAW),'raw_sha256':MIN_SHA,'class':'REUSED_SECONDARY_TABLE_NOT_PRIMARY_STATUTORY_ROUNDING','signed2021_max_table_Year1_2_3':[2641691,2773776,2905862],'admitted_rounding_screen_upper_each':3000000,'actual_minimum_cents_certified':False},'rule_connections':['VII6(g): room MLE maximum2 seasons, 5% increases; no later NTMLE/BAE/taxMLE.','VII6(i): minimum salary exception exact applicable minimum,1 or2years,no bonuses; it is not a3-year minimum exception.','VII4 and II13: retain valid pending QO/holds, include notified agreements, distinguish waiver clearance and protected residue.','VII6(h)/VIII1: Suggs unsigned1R hold can be replaced by candidate rookie salary no larger than preserved120% hold.','VII6(b)/I1: Diallo Bird path requires admitted prior-team/continuous service identity; no real acceptance certificate.','X4: Aldama required tender/unsigned2R costs are a separate explicit variable, not a free standard slot.','XXIX1–3 +2021opening rule: selected12STD active/3inactive and2TW separate at opening.']}

def roster_comparison(r,det):
 ten=set(r['regulation_pair_comparison']['DET_existing_G14_candidate']['player_minutes']);assert len(ten)==10
 out=[]
 for row in r['opening_roster_recovery']['named_slot_candidates']:
  std=row['standard_candidate'];tw=row['two_way_candidate'];assert len(std)==len(set(std))==15 and len(tw)==len(set(tw))==2 and not set(std)&set(tw) and ten<=set(std)
  nom=[n for n in std if n in ten]+[n for n in std if n not in ten][:2]
  inactive=[n for n in std if n not in nom]
  assert len(nom)==12 and len(inactive)==3
  out.append({'id':row['id'],'standard_candidate':std,'two_way_candidate':tw,'working_active_standard_12':nom,'working_inactive_standard_3':inactive,'positive_10_preserved':True,'zero_active_minute_clinical_status':None,'actual_active_medical_or_registration_certified':False,'selected':False})
 return out

def trace(x,q,al,aq,ar,p):
 """Numeric sufficient-condition trace. X is NOT asserted bounded by public inventory."""
 x=Fraction(x);q=Fraction(q);assert x>=0 and 3000000<=q<=12195122 and al['alternate_candidate_team_salary_before']+x+q<=al['cap'],'Candidate room domain infeasible'
 base=Fraction(al['alternate_candidate_team_salary_before'])+x
 states=[{'event':'Before Olynyk agreement/contract after effective named waivers/renunciations','date_hypothesis':'2021-08-09','team_salary_upper':-(-base.numerator//base.denominator),'basis':'NAMED_BASE_PLUS_UNCERTIFIED_RESIDUAL_X'}]
 def add(event,date,delta,method):
  nonlocal base;base+=Fraction(delta);delta=Fraction(delta);states.append({'event':event,'date_hypothesis':date,'team_salary_upper':-(-base.numerator//base.denominator),'delta_upper':-(-delta.numerator//delta.denominator),'method':method})
 add('Olynyk new three-year5% offer q','2021-08-09',q,'CAP_ROOM; no Lyles agreement or cost yet/ever in this branch')
 # New NBA minimum contracts use legal applicable-minimum functions; table-derived3m upper is an admitted screen, not exact minimum identity.
 add('Lee two-year minimum: replace retained925258 FA amount','2021-08-09',3000000-925258,'MINIMUM_EXCEPTION; no old3-year cap-room contract copied')
 add('Frank two-year minimum: replace retained1939350 QO charge','2021-08-10',3000000-1939350,'MINIMUM_EXCEPTION; exact minimum function, not arbitrary3m base')
 add('Livers new two-year minimum','2021-08-10',3000000,'MINIMUM_EXCEPTION; original42 money not copied into candidate38')
 add('Suggs candidate NBA rookie-scale contract replaces existing6592920 unsigned hold at no higher cost','2021-08-10',0,'ROOKIE_EXCEPTION; candidate pick5 admission and UPC consent, neither selected as fact')
 add('Joseph roomMLE two-year, first4910000; preserve old2400000 residue already in base','2021-08-10',4910000,'ROOM_MLE, no combined NTMLE/BAE')
 add('McGruder one-year minimum after effective old waiver','2021-08-11',3000000,'MINIMUM_EXCEPTION; full salary upper, reimbursement not subtracted from this screen')
 add('Diallo two-year Bird offer5200000 replaces retained2079826 QO','2021-08-19',5200000-2079826,'BIRD_CONDITIONAL_CONTINUOUS_PRIOR_TEAM_SERVICE; bonus0 newoffer')
 add('Aldama separate valid outstanding RequiredTender reservation','2021-09-01 IF within operative2021 tender window',3000000,'LEGAL_MINIMUM_TENDER_FUNCTION; completed team-signed valid tender and nonacceptance are candidate conditions, no16thUPC; no actual modifieddeadline/receipt claim')
 # Full current Jordan salary reserved even after waiver: no copied buyout reduction.
 add('Nets/Jordan assignment: remove Sekou+Okafor and add full Jordan9881598','2021-09-04',9881598-3613680-2130023,'PRESERVED_NAMED_PLAYERS_CANDIDATE; bothmatching andsource-supportedwholepartybudgets still require reviewedcarrier')
 add('Garza two-year standard minimum conversion','2021-09-24',3000000,'MINIMUM_EXCEPTION; branchB keeps original conversion direction as candidate')
 return states

def build():
 p=checked_policy();r,al,aq,ar,slot,det=source_inputs();rs=rules();rr=roster_comparison(r,det)
 assert rr[1]['id']=='B_lyles_not_signed' and 'Trey Lyles'not in rr[1]['standard_candidate']
 # Parameter range is derived feasibility, not manufactured evidence that all actual old obligations are in it.
 xmin=0; xmax=12361772-3000000
 cases=[]
 for x in [0,203571,xmax]:
  q=min(12195122,12361772-x);states=trace(x,q,al,aq,ar,p)
  assert states[1]['team_salary_upper']<=112414000
  schedule=[Fraction(q),Fraction(q)*105/100,Fraction(q)*110/100]
  cases.append({'uncertified_residual_X_usd':x,'Olynyk_offer_q_upper_usd':q,'Olynyk_three_year5percent_schedule_exact_dollar_fractions':[str(v) for v in schedule],'Olynyk_three_year5percent_schedule_upper':[-(-v.numerator//v.denominator) for v in schedule],'integer_schedule_is_upper_display_not_agreed_salary':True,'states':states,'selected':False,'all_legal_minimum_functions_screened_at3000000_not_chosen_salary':True,'full_apron_pass':False})
 # This conservative preliminary post upper deliberately reveals what still fails: cannot downgrade young minima/future-tender charge tozero.
 assert [c['Olynyk_offer_q_upper_usd']for c in cases]==[12195122,12158201,3000000]
 postmax=max(c['states'][-1]['team_salary_upper']for c in cases)
 assert postmax==139717461,'Conditional postscreen arithmetic changed'
 return {'id':'DETROIT_2021_OPENING_NAMED_OPERATING_FAMILY','status':'INDEPENDENTLY_REVIEWED_FINITE_CANDIDATE_PATHS_WHOLE_PUBLIC_COST_AND_DIRECTION_UNSELECTED','baseline_main':BASELINE,'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8 BOM stripped CRLF/CR toLF','rules':rs,'policy':p,'opening_game':r['game'],'roster_candidates':rr,'named_cap_route_A':{'Garza_TW_retained_Lyles_preserved':True,'original_all_cap_room_after_Olynyk_Lee_Lyles_Frank':-3957807,'extra_deadmoney_source_delta':203571,'same_route_room_deficit_with_that_delta':4161378,'named_salary_free_exit_counterparties_selected':False,'September_Jordan_not_an_August_salary_free_exit':True,'new_2020_rookie_salary_reduction':False,'complete_path_closed':False},'named_cap_route_B':{'Lyles_no_agreement_no_signature':True,'existing_alternative_not_new_author_lock':True,'new_minimum_contracts':['Saben Lee','Frank Jackson','Isaiah Livers','Rodney McGruder','Luka Garza'],'Olynyk_offer_function':'q in [3000000, min(12195122,12361772-X)]','q_nonempty_iff_X_leq':xmax,'X_definition':'All lawful residual initial cap charges in excess of preserved named100052228 AFTER effective named waiver/renunciation: original performance/protection, additional oldpay/settlements, remaining FA/offer/tender/exception/incomplete-roster charges and any changed notified agreements. X is not certified bounded orzero.','X_actual_or_public_inventory_upper':None,'Olynyk_room_at_old_reported_q_requires_X_leq':166650,'reported_deadmoney_source_sensitivity_requires_q_reduction':36921,'q_is_new_consensual_offer_not_real_originalterms':True,'pending_original_earned_or_protected_money_removed':False,'source_supported_whole_cost_family_pass':False,'cases':cases,'post_3m_each_minimum_screen_max':postmax,'2021_apron_comparison_only':{'apron':143002000,'preliminary_margin':143002000-postmax,'hardcap_trigger_not_invented_by_roomMLE':True,'whole_apron_adjusted_cost_still_unverified':True}},'joint_event_and_descendant_boundaries':{'Nets_Jordan_all_four_seconds_and_cash_required':'Original named2022/2024WAS/2025GSW/2027conditionalseconds+cash, no exactownership/cashterm replacement here; verify against DB1/Westbrookchanged actors before adoption.','BKN_2021_draft_asset_chain_not_assumed_same':True,'DET_Nets_raw_matching_base_conditions':{'DET_outgoing':5743703,'DET_nontax_limit':10743703,'Jordan_base_incoming':9881598,'DET_base_margin':862105,'BKN_tax_outgoing':9881598,'BKN_base_incoming':5743703,'performance_protection_bonus_family_waiver_and_6month_guards_not_yet_closed':True},'Jordan_waiver_full_cost_preserved':9881598,'actual_Nets_trade_receipt_or_private_budget_required':False,'Lyles_future2022_Bagley_bundle_no_longer_portable_in_B':True,'Pickett_TW_in_B_is_candidate_not_foreverrights':True,'Garza_DNP_or_Smith_knee_not_imported_health':True,'Aldama_unaccepted_tender_not_NBA_UPC_or_free_cost':True},'positive_minutes':r['regulation_pair_comparison']['DET_existing_G14_candidate']['player_minutes'],'unchanged_chicago_minutes':r['regulation_pair_comparison']['CHI_current_M1_NORMAL']['player_minutes'],'actual_next_finite_inputs':['Public DET priorordinary/camp endpoints and legal carry/stretch bounds needed to bound initialX; no unpublishedledger certificate required.','Candidate minimum functions legal cents/floor type:3m is a conservative admitted upper rather than a chosen NBA minimum salary.','Review continuous renunciation/waiver q and original retained protectedmoney; preserve QOcharges until accepted replacement.','Complete DET/BKN currentpublic cost/matching/fullreturnedasset jointfamily or compare a separate legal Jordan path; cannot call an unreviewed source-preservation assumption a PASS.','Authorcomparison of A versus B: B changes Lyles futuretrade and nominal Olynyk/Lee/Frank/Livers/Garza contracts, so do not promote from arithmetic alone.'],'certification':{'independent_review_completed':True,'whole_source_supported_cost_family_pass':False,'actual_registration_or_acceptance':False,'new_author_lock':False,'health_or_result_selected':False,'whole2021_22_or_macro3_complete':False,'REGISTER_changed':False,'manuscript_written':0},'progress':r['progress']}

def validate(o):
 try:assert o==build(),'Saved candidate differs from source-bound reconstruction';return []
 except(AssertionError,KeyError,OSError,ValueError)as e:return[str(e)]
def markdown(o):
 b=o['named_cap_route_B']
 return '\n'.join(['# Detroit2021 개막 실명 운영 후보: 두 경로와 비용 함수','',o['status'],'','## 실제 구현한 것','','기존 첫 Detroit 입력 복구를 이어 A/Garza TW와 B/Lyles 미서명의 각각15STD·2TW 명단을 구성했다. 양수10명 전원을12STD active에 넣고 남은3STD inactive, 두TW는 별도명단으로 둔다.0분/비활동을 질병으로 읽지 않는다. Chicago M1과 Detroit240분은 보존하며 스코어·건강 선택0이다.','', '## A와 B의 차이','','A는 Lyles와 기존 G14양수10을 보존하지만 같은 cap-room 서명 전부를 쓰면 기존부족3,957,807, 다른deadmoney원천까지4,161,378이다. Sekou/Okafor 무료이탈·미래Nets픽 조기지출·원2020rookie급여 소급삭감으로 메우지 않았다. 수신팀/반대급부는 아직 후보이다.','B는 기존Lyles미서명 대안을 구체화했다. Olynyk는 새3년/5%/bonus0의q 제안, Lee·Frank·Livers·Garza는 새법정최소2년/bonus0, McGruder는 최소1년이다. 법정최소를 임의3m계약으로 쓰지 않는다.3m는 보고표의3년최대2,905,862보다 큰 **조건부상단**이며 정확법정반올림 미회수다. Joseph는 roomMLE4.91m/2년/5%이고 old2.4m잔액은보존, Diallo는적법한Bird존속하5.2m/2년 제안이다. 원계약/실동의를 복사하지 않는다.','',f"초기 명명100,052,228외의 모든 적법잔여차지를 X라 두면 Olynyk q∈[3,000,000,min(12,195,122,12,361,772−X)]. 비공허 조건은 **X≤{b['q_nonempty_iff_X_leq']:,}**이다. X상단/0은 원천에서 인증하지 않았다. 이것을 실제wholecost PASS로 읽으면 안 된다.",'','|초기 X 시험|Olynyk 제안 상단|설명|','|---|---:|---|','|0|12,195,122|기존명명항목 시험; 실제추가비용0 인증아님|','|203,571|12,158,201|공개deadmoney원천차이를 보존하면36,921감액 제안 필요|','|9,361,772|3,000,000|함수의 비공허 끝점; 실제그비용관측아님|','',f"이후 Lee/Frank/신인/최소/roomMLE/Diallo와Jordan **전액9,881,598**·별도AldamaTender까지 상단을 누적했다. 세 시험 최대 **{b['post_3m_each_minimum_screen_max']:,}**,apron143,002,000과 차이는 **{b['2021_apron_comparison_only']['preliminary_margin']:,}**다. 여유숫자는초기X상단을입증하거나전체apron조정비용을인증하지 않는다. RoomMLE가그자체로hardcap을발동한다고 추가하지 않는다.",'','## 연속 사건의 법적 경계','','8/9 Olynyk후보는 모라토리엄과McGruder/명명권리포기 효과 뒤의 가상순서이다. 발표8/6을 실제동의·접수완료시각으로 옮기지 않는다. 유효Lee/Frank/DialloQO는대체서명이되기전까지소계에유지한다. Lee최소2년은기존3년계약을최소예외로잘못분류한것이아니라새후보다. RoomMLE와NTMLE/BAE의동시사용을거부한다. Suggs#5미서명hold는그보존120%이하의RSC로치환해야한다. Aldama#37권리/미수락RequiredTender는별도예산에보존하며표준16번째서명을자동생성하지않는다.','Nets후속은Sekou+Okafor/Jordan과네2R·현금전체가필요하다. 본문은기존두팀기본급matching조건만회수했고공동보너스/보호/6개월후손·Brooklyn비용·변경draft자산을닫지않았다. Jordanbuyout7,875,533를복사하지않고전액9,881,598를예약했다. 따라서지금B의명단/조건부cost함수완료와전체법적실행완료를구분한다.','B의Lyles생략은1월역할·2월Bagley거래와연결된다. Olynyk/Lee등조정계약도아직수락되지않은제안이다. 추천숫자만으로새장기방향을자동확정하지않았다.','', '## 실제 원천·검사와 다음 한 단계','','[2017CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) PDF223/231–233/238–241/412의예외·상한·활동명단원문을직독했다. 기존[최소급보고표](https://www.hoopsrumors.com/2021/08/nba-minimum-salaries-for-2021-22.html)raw는재사용된2차표이며정확법정반올림인증0. 같은P0-B의원자료/가이드검색반복없다. sourcepins·CBAraw/pageSHA·보고표raw 및실제source필드를검사하고자기통제는독립검문으로세지않는다.','다음은 **Detroit의6범주공개원천으로X상단을산출**하고DET/BKN전체반대급부/예외/비용을닫는일이다. unknown을0으로설정하거나비공개접수증명을새필수로요구하지않는다. 법정예외로넘기는연속후보를실제로만들었으나X의공개상단과중요방향선택을아직증명하지못했다.','', '[첫DET복구](CHICAGO_2021_22_OPENING_DET_PAIRED_INPUT_RECOVERY_2026_10_07.md) · [현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','', '|번호|묶음|상태|','|---|---|---|','|1|2020드래프트연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23거래·계약|DET명단두후보/연속cost함수완료;whole공개비용·방향미선택|','|4|장기커리어|후속시즌대기|','|5|결말·전체구조|전체기능표미완료|','|6|집필규격·ContextPack|현행누적등록기참조·Pack0|','|7|통합·독립·작가승인|최종CLOSED|','','미완료큰묶음5 / v0.30 PARTIAL / 설계·원고CLOSED / 원고0.',''])

def self_test():
 tests=[];o=build()
 for label,fn in [('wrong_positive_donor',lambda x:x['positive_minutes'].update(**{'Mason Plumlee':0})),('lost_legacy_protected_charge',lambda x:x['named_cap_route_B']['cases'][0]['states'][0].update(team_salary_upper=97652228)),('fake_whole_cost_PASS',lambda x:x['certification'].update(whole_source_supported_cost_family_pass=True))]:
  z=copy.deepcopy(o);fn(z);assert validate(z),label;tests.append(label)
 p=policy();p['NTMLE_or_BAE_combined_with_roomMLE']=True
 with patch(__name__+'.policy',return_value=p):
  try:build()
  except AssertionError:tests.append('constructor_roomMLE_plus_BAE')
  else:raise AssertionError('Combined mutuallyexclusive exceptions')
 old=load;z=copy.deepcopy(load(AL));z['alternate_candidate_team_salary_before']-=2400000
 with patch(__name__+'.load',side_effect=lambda p:copy.deepcopy(z)if p==AL else old(p)):
  try:build()
  except AssertionError:tests.append('constructor_source_old_Joseph_residue_removed')
  else:raise AssertionError('Source oldcharge dropped')
 try:trace(9361773,3000000,load(AL),load(AQ),load(AR),policy())
 except AssertionError:tests.append('one_dollar_over_room_domain')
 else:raise AssertionError('Infeasible end accepted')
 return tests

def main():
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');args=a.parse_args();o=build()
 if args.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
 if args.check:assert not validate(load(OUT));assert text(MD)==markdown(o)
 print(json.dumps({'current':True,'candidates':2,'states_per_conditional_trace':len(o['named_cap_route_B']['cases'][0]['states']),'postscreen':o['named_cap_route_B']['post_3m_each_minimum_screen_max'],'whole_cost_pass':False,'negative_controls':self_test()if args.self_test else[]},ensure_ascii=False))
if __name__=='__main__':main()
