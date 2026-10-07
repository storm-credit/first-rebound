"""Adopt P22A under recorded root delegation; preserve frozen candidate sources.

No ancestor constructors. Source-return and selection-return meanings are
checked independently at each caller. No actual medical/private certification.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
from datetime import date, timedelta
from copy import deepcopy
from unittest.mock import patch
from bs4 import BeautifulSoup
import argparse, hashlib, json

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_selected_full_postseason.py'
OUT='simulation/NBA_2022_SELECTED_FULL_POSTSEASON.json';MD=OUT[:-5]+'.md'
DECISION='canon/DELEGATED_2022_NPC_POSTSEASON_DECISION_2026_10_08.json'
PO='design/NBA_2022_FULL_POSTSEASON_CANDIDATE.json'
PACKET='design/NBA_2022_LEAGUE_TITLE_DECISION_PACKET.json'
OPT='research/NBA_2022_CANDIDATE_FINALS_OPTION_JOIN_2026_10_08.json'
GLOBAL='simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json'
AUTH='canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
SCOPE='control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md'
ALL2021='simulation/NBA_2021_DELEGATED_PLAYOFF_RESULTS.json'
POPEER='reviews/NBA_2022_FULL_POSTSEASON_CANDIDATE_G11_INDEPENDENT_REVIEW_2026_10_08.json'
OPTPEER='reviews/NBA_2022_CANDIDATE_FINALS_OPTION_JOIN_G11_INDEPENDENT_REVIEW_2026_10_08.json'
PINS={'design/NBA_2022_LEAGUE_TITLE_DECISION_PACKET.json': 'ce2264752c850bdef7a4359b4475415be8602f581d18ef7c507bd2075ea8b21b', 'design/NBA_2022_FULL_POSTSEASON_CANDIDATE.json': 'dcefe931a0f82e3733f577cc47a314cc66ad9162a9988d15d7514302424023f5', 'research/NBA_2022_CANDIDATE_FINALS_OPTION_JOIN_2026_10_08.json': '8f253cd314203e281a206027ef4e4031f13144df4b8642331f86ff6c9c69ee18', 'simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json': '93264d2dff86a58ad10ca6975315c6c2167961f94f2517b6f5f79fa3113f2af8', 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json': '4ee9b74e37903a43b0bd50b35c7f24cbabdac13728097a848b553f874bbeef80', 'control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md': '91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d', 'simulation/NBA_2021_DELEGATED_PLAYOFF_RESULTS.json': 'dc1d47563f8381a4b1bd98409f198e8df088ce782622071e22556e8f0c7a7cdb', 'reviews/NBA_2022_FULL_POSTSEASON_CANDIDATE_G11_INDEPENDENT_REVIEW_2026_10_08.json': 'c4f528cf0526e0277e78dc0ac49e107aa122e9dabce83b860c4c1dcdd5df5f59', 'reviews/NBA_2022_CANDIDATE_FINALS_OPTION_JOIN_G11_INDEPENDENT_REVIEW_2026_10_08.json': 'a277b231ff996046918684f052f98175ba9db6e17a627417d6e442ba90e1169c'}
TITLEPEER='reviews/NBA_2022_LEAGUE_TITLE_DECISION_PACKET_G11_INDEPENDENT_REVIEW_2026_10_08.json'
PINS[TITLEPEER]='46a6e1ff9e33eade09bb743df7573df3cf6eb09b3ddd9acc174bb3b5fdf8d117'
ROOKIE='canon/DELEGATED_2022_DRAFT_AND_CHICAGO_ROOKIE_DECISION_2026_10_08.json'
PINS[ROOKIE]='a32dfc265a7250bc89df366c14b43444645438675674f4be66feda2b6a053eba'
BASELINE='ee0ff822aa127f8263cc69e03ba2a7184053e22e'
EO_URL='https://www.nyc.gov/mayors-office/news/2022/03/emergency-executive-order-62'
EO_RAW=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-eo62-20261008/EO62.html')
EO_SHA='83763372a5820823d9e21444c4758106162d1ca28e00f44e8d6d33210d21d4f4'
ROOT_SELECTION={
 'recorded_local_date':'2026-10-08','selected_option':'P22A',
 'champion':'MIL','runner_up':'UTA','Finals_wins':{'MIL':4,'UTA':3},
 'last_Finals_date':'2022-06-20','new_fourteen_series_calendar_and_availability_selected':True,
 'selection_class':'ROOT_EXPLICIT_DELEGATED_SEASON_RESULT_DESIGN',
 'authority':AUTH,'instruction_basis':'Root explicitly selected P22A under existing season delegation and the 2021 NPC championship precedent; protagonist titlecount/MVP/core/ending changes zero. Utah major rebuild remains a separate descendant.',
 'root_selection_recorded':True,'new_human_author_lock':False,
 'actual_institutional_private_contract_medical_receipt_certified':False,
 'Utah_rebuild_or_other_important_transaction_selected':False,
 'regular_2021_22_sources_rewritten':False}
FIXED_SELECTION=deepcopy(ROOT_SELECTION)
POSITIONS={'PG','SG','SF','PF','C'}

def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def encoded(v):return json.dumps(v,ensure_ascii=False,indent=2)+'\n'
def load(root,p):return json.loads(text(root/p)) if p.endswith('.json') else text(root/p)
def sources(root):
 assert ROOT_SELECTION==FIXED_SELECTION,'Root selection parameters changed'
 out={}
 for p,h in PINS.items():
  assert sha(root/p)==h,'Pinned physical source changed '+p
  v=load(root,p);q=json.loads(text(root/p)) if p.endswith('.json') else text(root/p)
  assert v==q,'Returned source differs from physical parse '+p;out[p]=v
 for peer,source in [(POPEER,PO),(OPTPEER,OPT),(TITLEPEER,PACKET)]:
  assert out[peer]['independent_review_completed'] is True and out[peer]['source_sha256'][source]==PINS[source]
 assert out[PACKET]['recommended_option']=='P22A'
 assert out[ALL2021]['authority']==AUTH and out[ALL2021]['champion']=='MIL'
 assert out[PACKET]['authority_audit']['substantive_findings']['NPC_title_precedent_supports_root_delegated_result_selection_after_review'] is True
 return out

def eo62():
 assert hashlib.sha256(EO_RAW.read_bytes()).hexdigest()==EO_SHA,'EO62 raw changed'
 body=' '.join(BeautifulSoup(EO_RAW.read_bytes(),'html.parser').get_text(' ',strip=True).split())
 assert all(s in body for s in ['March 24, 2022','a professional athlete','as part of their regular employment','shall be exempt from the Order of the Commissioner of Health dated December 13, 2021','remain in effect for five (5) days'])
 return {'url':EO_URL,'raw_cache':str(EO_RAW),'raw_sha256':EO_SHA,'http_status':200,'raw_bytes':499484,
  'observed_at_local_date':'2026-10-08','issued_date':'2022-03-24',
  'sections':['3(d)(3)(iv)','3(e)','4'],'source_fact':'Professional athletes entering as regular employment are excluded from covered worker and exempt from the Dec13 workplace vaccination order; EO62 itself lasts five days unless earlier modified or terminated.',
  'extensions_after_five_days_independently_verified_here':False,
  'postseason_continuing_real_NYC_legal_ban_inferred':False,
  'individual_actual_vaccination_or_receipt_certified':False}

def clock(t,g):
 assert t['registration']==g['team_rosters'][t['team']]
 owner={(x['team'],x['source_name']):x['class'] for rows in g['owner_catalog'].values() for x in rows}
 for cls in ['standard','TW']:
  assert all(owner.get((t['team'],n))==cls for n in t['registration'][cls])
 assert 12<=len(t['active'])<=15 and len(set(t['active']))==len(t['active'])
 assert set(t['active'])<=set(t['registration']['standard']) and not(set(t['active'])&set(t['registration']['TW']))
 end=0;people=Counter();roles={p:Counter() for p in POSITIONS}
 for b in t['blocks']:
  assert b['start_second']==end and b['end_second']>end
  assert set(b['positions'])==POSITIONS and len(set(b['positions'].values()))==5
  n=b['end_second']-end
  for p,name in b['positions'].items():assert name in t['active'];people[name]+=n;roles[p][name]+=n
  end=b['end_second']
 assert end==2880 and sum(people.values())==14400 and dict(people)==t['positive_player_seconds']
 assert {p:dict(a) for p,a in roles.items()}==t['role_player_seconds']
 assert all(sum(a.values())==2880 for a in roles.values())
 assert t['actual_active_or_medical_certified'] is False

def participation(q):
 if 'BKN' not in (q['home'],q['away']):return None
 key=q['team_template_keys']['BKN'];out=key.endswith('IRVING_INSTITUTIONAL_OUT')
 return {'source_template_key':key,'source_legacy_label_is_generation_history':True,
  'selected_current_meaning':'FICTIONAL_TEAM_OPERATIONAL_AVAILABILITY_AND_ROLE_OUT' if out else 'FICTIONAL_US_ROAD_AVAILABILITY_WITH_LAWFUL_HOST_ACCESS_CONDITION',
  'Irving_selected_positive':not out,'real_NYC_legal_ban':False,
  'NYC_based_athlete_exemption_observed_in_March24_EO62':True,
  'EO62_five_day_extension_afterward_verified':False,
  'Canadian_access_condition':('TORONTO_LAWFUL_ENTRY_CONDITION_NOT_ESTABLISHED_FOR_THIS_RETURN_FAMILY; choose OUT, not NYC-law inference' if q['home']=='TOR' else 'NOT_A_CANADIAN_VENUE'),
  'team_role_choice_is_not_actual_Nets_policy_or_medical_history':True,
  'actual_vaccination_foreign_entry_or_receipt_certified':False}

def select_series(original):
 games=[]
 for q in original['games']:
  games.append({'source_candidate_game':deepcopy(q),'selected_regulation_winner':q['candidate_regulation_winner'],
   'selected_date':q['date'],'selected_role_template_keys':deepcopy(q['team_template_keys']),
   'BKN_participation_interpretation':participation(q),
   'new_actual_score_OT_or_clinical_receipt':False})
 return {'id':original['id'],'source_candidate_series':deepcopy(original),'selected_games':games,
  'selected_winner':original['candidate_winner'],'selected_wins':deepcopy(original['wins']),
  'selection_class':'PRESERVED_EXISTING_CHI_PHI_SELECTION' if original['classification']=='IMMUTABLE_SELECTED_CHI_PHI_SOURCE' else 'ROOT_DELEGATED_P22A_POSTSEASON_SELECTION',
  'actual_NBA_results_or_private_acceptance_certified':False}

def assert_series(v,original,templates,g):
 assert v['id']==original['id'] and v['source_candidate_series']==original,'Source full series changed'
 assert v['selected_winner']==original['candidate_winner'] and v['selected_wins']==original['wins']
 assert v['selection_class']==('PRESERVED_EXISTING_CHI_PHI_SELECTION' if original['classification']=='IMMUTABLE_SELECTED_CHI_PHI_SOURCE' else 'ROOT_DELEGATED_P22A_POSTSEASON_SELECTION')
 assert v['actual_NBA_results_or_private_acceptance_certified'] is False
 assert len(v['selected_games'])==len(original['games']);counts=Counter()
 for row,q in zip(v['selected_games'],original['games']):
  assert row['source_candidate_game']==q and row['selected_date']==q['date']
  assert row['selected_role_template_keys']==q['team_template_keys']
  assert row['selected_regulation_winner']==q['candidate_regulation_winner'],'Returned selected winner differs from P22A'
  assert row['new_actual_score_OT_or_clinical_receipt'] is False
  assert max(counts.values(),default=0)<4;counts[row['selected_regulation_winner']]+=1
  home=q['home'];away=q['away'];weights={}
  for team,key in q['team_template_keys'].items():
   t=templates[key];assert t['team']==team;clock(t,g)
   weights[team]=sum(Fraction(g['selected_productivity_inputs'][n]['fraction'])*s for n,s in t['positive_player_seconds'].items())/2880
  margin=weights[home]-weights[away]+2
  assert q['weighted_BPM_fraction']=={t:str(w) for t,w in weights.items()}
  assert q['exact_home_proxy_margin']==str(margin) and q['candidate_regulation_winner']==(home if margin>0 else away)
  assert q['home_advantage_fraction']=='2' and q['back_to_back_fatigue_fraction']=='0'
  assert q['score'] is None and q['overtime'] is None and q['actual_registration_clinical_or_receipt_certified'] is False
  p=row['BKN_participation_interpretation']
  if 'BKN' not in (home,away):assert p is None
  else:
   out=q['team_template_keys']['BKN'].endswith('IRVING_INSTITUTIONAL_OUT')
   assert p['source_template_key']==q['team_template_keys']['BKN']
   assert p['source_legacy_label_is_generation_history'] is True
   assert p['selected_current_meaning']==('FICTIONAL_TEAM_OPERATIONAL_AVAILABILITY_AND_ROLE_OUT' if out else 'FICTIONAL_US_ROAD_AVAILABILITY_WITH_LAWFUL_HOST_ACCESS_CONDITION')
   assert p['Irving_selected_positive']==(not out)
   assert p['real_NYC_legal_ban'] is False and p['EO62_five_day_extension_afterward_verified'] is False
   assert p['NYC_based_athlete_exemption_observed_in_March24_EO62'] is True
   assert p['Canadian_access_condition']==('TORONTO_LAWFUL_ENTRY_CONDITION_NOT_ESTABLISHED_FOR_THIS_RETURN_FAMILY; choose OUT, not NYC-law inference' if home=='TOR' else 'NOT_A_CANADIAN_VENUE')
   assert p['team_role_choice_is_not_actual_Nets_policy_or_medical_history'] is True and p['actual_vaccination_foreign_entry_or_receipt_certified'] is False
 assert dict(counts)==original['wins'] and max(counts.values())==4

def option_join(n,w):
 return {'source_notice':deepcopy(n),'source_conditional_witness':deepcopy(w),
  'chosen_Season_endpoint':'2022-06-20','window_open':'2022-06-21','notice_date':n['date'],'deadline':'2022-10-31',
  'preceding_original_UPC_Season_number':2 if n['option_season_number']==4 else 1,
  'timely_in_selected_Season':True,'days_after_open':102,'days_before_deadline':30,
  'existing_notice_applied_not_new_option_price_or_UPC':True,'actual_notice_receipt':None}

def assert_option(v,n,w):
 assert v['source_notice']==n and v['source_conditional_witness']==w
 assert (v['chosen_Season_endpoint'],v['window_open'],v['notice_date'],v['deadline'])==('2022-06-20','2022-06-21','2022-10-01','2022-10-31')
 end=date(2022,6,20);start=end+timedelta(days=1);notice=date.fromisoformat(n['date']);deadline=date(2022,10,31)
 assert v['timely_in_selected_Season']==(start<=notice<=deadline)
 assert v['days_after_open']==(notice-start).days==102 and v['days_before_deadline']==(deadline-notice).days==30
 assert v['preceding_original_UPC_Season_number']==(2 if n['option_season_number']==4 else 1)
 assert v['existing_notice_applied_not_new_option_price_or_UPC'] is True and v['actual_notice_receipt'] is None

def decision_record(src,root):
 return {'id':'DELEGATED_2022_NPC_POSTSEASON_DECISION_2026_10_08','baseline_main':BASELINE,
  'status':'SELECTED_ROOT_DELEGATED_P22A_FULL_POSTSEASON_DESIGN','selected':deepcopy(ROOT_SELECTION),
  'source_sha256':{**PINS,SELF:sha(root/SELF)},'consumer':OUT,
  'source_snapshot_unselected_flags_are_at_generation':True,
  'selected_scope':['14 additional series/calendar/same retained UPC-Gamma family and operational availability','Existing CHI-PHI seven games unchanged','MIL4-3UTA title and June20 alternate Season endpoint','Apply existing two Oct1 option notices through conditional witnesses9/10'],
  'preserved_boundaries':{'protagonist_titlecount_MVP_core_ending_changes':0,'Utah_major_rebuild_not_selected':True,
   'real_NYC_postseason_legal_ban':False,'actual_private_salary_medical_foreign_receipt_certified':False,
   'new_2022_draftee_UPC_or_price_selected':False,'whole_macro3_complete':False,'manuscript_allowed':False,'design_gate':'CLOSED'},
  'prior_regular_BKN_OUT_label_interpretation':{
   'applies_to_original_global_dates_from':'2022-03-24',
   'unchanged_source':GLOBAL,'original_results_registration_roles_unchanged':True,
   'legacy_institutional_label_is_continuing_actual_NYC_ban_evidence':False,
   'current_meaning':'Already selected fictional club nomination/role OUT; EO62 athlete exemption and untraced later extensions prevent an assertion of continuing actual NYC vaccination prohibition.',
   'new_regular_result_or_health_selection':False,'actual_vaccination_or_policy_certification':False},
  'independent_current_consumer_review_completed':False,'author_locked':False}

def build(root=ROOT):
 src=sources(root);po=src[PO];g=src[GLOBAL];eo=eo62()
 assert po['candidate_champion']=='MIL' and po['candidate_last_Finals_date']=='2022-06-20'
 assert src[PACKET]['options'][0]['Finals_games']==po['series'][-1]['games']
 assert src[PACKET]['options'][0]['candidate_Finals_wins']=={'MIL':4,'UTA':3}
 templates=deepcopy(po['postseason_team_template_pool']);series=[];done={}
 for original in po['series']:
  for dep in original['upstream_series_ids']:assert dep in done and done[dep] in original['teams'],'Bracket dependency changed'
  v=select_series(original);assert_series(v,original,templates,g);series.append(v);done[v['id']]=v['selected_winner']
 assert len(series)==15 and sum(len(s['selected_games']) for s in series)==93
 assert series[-1]['selected_winner']=='MIL' and series[-1]['selected_wins']=={'MIL':4,'UTA':3}
 first=[s for s in series if s['selection_class']=='PRESERVED_EXISTING_CHI_PHI_SELECTION'];assert len(first)==1 and len(first[0]['selected_games'])==7
 assert first[0]['selected_winner']=='PHI' and first[0]['selected_games'][-1]['selected_date']=='2022-04-30'
 opt=src[OPT];joined=[]
 for n,w in zip(opt['preserved_parent_notices'],opt['additional_ninth_tenth_conditional_witnesses']):
  assert n['player']==w['player'] and w['candidate_Finals_last_game']=='2022-06-20'
  v=option_join(n,w);assert_option(v,n,w);joined.append(v)
 assert [(v['source_notice']['player'],v['source_notice']['option_season_number']) for v in joined]==[('LaMelo Ball',4),('Chris Duarte',3)]
 d=decision_record(src,root)
 assert d['selected']==FIXED_SELECTION and d['author_locked'] is False
 assert d['id']=='DELEGATED_2022_NPC_POSTSEASON_DECISION_2026_10_08' and d['status']=='SELECTED_ROOT_DELEGATED_P22A_FULL_POSTSEASON_DESIGN'
 assert d['source_sha256']=={**PINS,SELF:sha(root/SELF)} and d['consumer']==OUT
 assert d['source_snapshot_unselected_flags_are_at_generation'] is True
 assert d['selected_scope']==['14 additional series/calendar/same retained UPC-Gamma family and operational availability','Existing CHI-PHI seven games unchanged','MIL4-3UTA title and June20 alternate Season endpoint','Apply existing two Oct1 option notices through conditional witnesses9/10']
 assert d['independent_current_consumer_review_completed'] is False
 assert d['prior_regular_BKN_OUT_label_interpretation']=={
   'applies_to_original_global_dates_from':'2022-03-24',
   'unchanged_source':GLOBAL,'original_results_registration_roles_unchanged':True,
   'legacy_institutional_label_is_continuing_actual_NYC_ban_evidence':False,
   'current_meaning':'Already selected fictional club nomination/role OUT; EO62 athlete exemption and untraced later extensions prevent an assertion of continuing actual NYC vaccination prohibition.',
   'new_regular_result_or_health_selection':False,'actual_vaccination_or_policy_certification':False}
 assert eo['url']==EO_URL and eo['raw_sha256']==EO_SHA and eo['sections']==['3(d)(3)(iv)','3(e)','4']
 assert eo['postseason_continuing_real_NYC_legal_ban_inferred'] is False and eo['extensions_after_five_days_independently_verified_here'] is False
 assert src[ROOKIE]['review_acceptance']['canonical_adoption_recorded_here'] is True
 assert src[ROOKIE]['selected']['Chicago_first']==[18,'Walker Kessler'] and src[ROOKIE]['selected']['Chicago_second']==[57,'Keon Ellis']
 assert d['preserved_boundaries']=={'protagonist_titlecount_MVP_core_ending_changes':0,'Utah_major_rebuild_not_selected':True,'real_NYC_postseason_legal_ban':False,'actual_private_salary_medical_foreign_receipt_certified':False,'new_2022_draftee_UPC_or_price_selected':False,'whole_macro3_complete':False,'manuscript_allowed':False,'design_gate':'CLOSED'}
 return {'id':'NBA_2022_SELECTED_FULL_POSTSEASON','baseline_main':BASELINE,
  'status':'SELECTED_DELEGATED_P22A_15_SERIES_MIL_TITLE_JUNE20_SEASON_END_CURRENT_CONSUMER_REVIEW_PENDING',
  'source_sha256':{**PINS,SELF:sha(root/SELF),DECISION:hashlib.sha256(encoded(d).encode()).hexdigest()},
  'hash_method':'UTF8_BOM_STRIP_CRLF_CR_TO_LF','root_selected_decision':d,
  'selected_policy':deepcopy(ROOT_SELECTION),'original_candidate_policy_at_generation':deepcopy(po['policy']),
  'source_candidate_and_title_packet_unchanged':True,'NYC_primary_boundary':eo,
  'selected_postseason_series':series,'postseason_team_template_pool':templates,
  'sixteen_playoff_seed_rows':deepcopy(po['sixteen_playoff_seed_rows']),
  'selected_champion':'MIL','selected_runner_up':'UTA','selected_NBA_Season_last_Finals_date':'2022-06-20',
  'selected_option_notice_application':joined,'preserved_eight_historical_conditional_windows':deepcopy(opt['preserved_eight_window_witnesses']),
  'contracts_cost_and_scope':{'same_2021_22_UPCs_and_all_original_Gamma_named_waiver_camp_stretch_FA_unsigned_exception_obligations_carried':True,
   'lawful_contract_duration_and_operational_availability_cover_selected_participation_dates':'Admitted fictional same-contract continuation through June20; no new trade, waiver, price, or TW conversion. Source per-date facts are not retroactively certified.',
   'all_positive_postseason_participants_standard_only':True,'zero_reserve_is_not_clinical_absence':True,
   'championship_bonus_functions_preserved_payoff_evaluated_against_MIL_title':'Any original title-contingent component remains payable according to its preserved function; no unknown bonus zeroed and no equal actual payout assertion.',
   'actual_private_salary_or_bonus_payment_certified':False},
  'summary':{'qualified_teams':16,'selected_series':15,'existing_CHI_PHI_preserved':1,'new_series_selected':14,
   'selected_games':93,'selected_team_dates':186,'source_role_templates':len(templates),
   'regulation_team_seconds':2880,'player_seconds':14400,'actual_scores_OT_new_draftee_UPCs':0,
   'existing_option_notices_applied':2,'original_eight_window_witnesses_preserved':8,
   'CHI_elimination':'2022-04-30','2022_regular_draw_rank_holder_changed':False},
  'separate_selected_2022_rookie_handoff':{'source':ROOKIE,'root_adoption_preserved':True,'selected':deepcopy(src[ROOKIE]['selected']),'new_adoption_or_cost_recalculation_by_this_consumer':False},
  'remaining_finite_ports':['The separately selected2022 rookie execution is preserved; this postseason does not create another rookie UPC/price.','2022-23 and2023 season inputs/results/qualifications require their own finite consumers.','Utah/Gobert/Mitchell and any other consequential franchise move require source-bound causal atomic assets; original trades are not copied.','Original title-triggered bonus functions may be consumed by future cost settlement; no actual private payouts certified.'],
  'certification':{'root_delegated_selection_recorded':True,'independent_current_consumer_review_completed':False,
   'championship_author_locked':False,'actual_NBA_result_contract_clinical_institutional_receipts':False,
   'EO62_later_extensions_or_continuing_legal_ban_certified':False,'whole_macro3_G13_G16_or_manuscript':False},
  'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}

def validate(v,root=ROOT):return [] if v==build(root) else ['Selected postseason differs from pinned sources and delegated selection']
def markdown(v):
 lines=['# 2022 전체 포스트시즌 · 위임 선택 실행','','Root는 기존 시즌 위임과 2021 NPC 우승 선택 선례를 검문해 **P22A: MIL4–3UTA, 2022년6월20일**을 선택했다. 새14시리즈·달력·동일계약 연속·가상 가용성과 기존 CHI–PHI7경기를 연결한다. 원 후보/비교 패킷의 미선택 필드는 생성 당시 스냅숏이며 변경하지 않는다. 새 인간 작가잠금·실제 NBA 경기/접수 인증은 아니다.','','| 시리즈 | 선택 승자 | 경기수 | 마지막 날짜 |','|---|---|---|---|']
 lines += [f"| {s['id']} | {s['selected_winner']} | {len(s['selected_games'])} | {s['selected_games'][-1]['selected_date']} |" for s in v['selected_postseason_series']]
 lines += ['','16팀·15시리즈·93경기·186팀 날짜. 기존17 역할 원형과 양팀48분/각240분·STD만 양수 참여·active12–15를 보존했다. 동일 분수 BPM/EB/home2 모델의 선택 설계이며 현실 예측/승률/실점수/OT/MVP 인증이 아니다. Chicago의4월30일 탈락·주인공 기존 PO분과 정규 QO분은 불변이다.','','## NYC와 가상 구단 선택 구분','','[NYC EO62 원문](https://www.nyc.gov/mayors-office/news/2022/03/emergency-executive-order-62)의3(d)(3)(iv)/3(e)는 직업상 경기장에 들어가는 프로선수 면제를 명시한다. 3월24일 명령 자체는5일이며 후속 연장은 여기서 확인하지 않았다. 따라서 기존 BKN 홈 역할 OUT을 포스트시즌의 실제 법적 출전금지라고 설명하지 않는다. 새 소비자는 같은 수치의 **가상 구단 운영 가용·역할 OUT**을 선택한다. 원정 RETURN은 합법 호스트 접근 조건을 갖춘 별도 가상 상태다.','','TOR/Canada는 이 NYC 면제로 허가된다고 추론하지 않는다. 이 가족의 Toronto 원정 RETURN 접근조건이 성립하지 않으면 OUT을 사용하는 별도 조건이며, 실제 출입국/백신/임상/구단 정책 증명은 아니다. 새 canon은 원정규 전역 모델의3월24일 이후 BKN OUT 라벨도 실제 NYC 법금지 지속 증거가 아니라 이미 선택된 가상 구단 nomination/역할로 명확히 한다. 기존 정규 수치·승패·등록은 바꾸거나 재개하지 않는다.','','## 선택된 Season 말단과 기존 통지','','선택6월20일 뒤6월21일 옵션창이 열리고, 원10월1일 통지는10월31일 마감 전이다. LaMelo4년차는 원UPC 두 번째 Season, Duarte3년차는 첫 Season을 근거로 한다. 두 notice는 창 시작102일 뒤·마감30일 전이다. 기존8증인과 조건부9/10은 그대로 두고 새 소비자에서 두 선택된 날짜 적용 record만 연결한다. 새가격/옵션/UPC/슬롯0, 실제 영수증 null.','','동일 기존 보호급여·모든 Γ·명명 비용과 원보너스 함수는 보존한다. MIL 우승에 의해 원 title bonus 함수의 지급조건이 달라질 수 있으므로 실제 지급액 동일이나 미지 보너스0을 주장하지 않는다. 2022 추첨·순번·소유·현재코어는 불변이며 별도 신규 canon의 Chicago Kessler18/Ellis57·R1 선택은 현재 사실로 인계하되 이 소비자가 추가 계약/가격을 선택하지 않는다. Utah 중요 재건·새 목적지·MVP·주인공 우승수/장기결말은 선택하지 않았다.','','작성자 검문은 원소유/역할시계·분수결과·반환값·날짜 적용과 source-current를 검사한다. 새 소비자의 독립 검문은 pending이며 기존 후보 peer를 새 독립 검문으로 재계수하지 않는다.','','[선택 기록](../canon/DELEGATED_2022_NPC_POSTSEASON_DECISION_2026_10_08.json) · [불변 후보](../design/NBA_2022_FULL_POSTSEASON_CANDIDATE.md) · [타이틀 비교](../design/NBA_2022_LEAGUE_TITLE_DECISION_PACKET.md) · [옵션 조건부 증인](../research/NBA_2022_CANDIDATE_FINALS_OPTION_JOIN_2026_10_08.md) · [현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','','| 묶음 | 상태 |','|---|---|','| 1 드래프트 연쇄 | 완료 |','| 2 Chicago2020–21 | 완료 |','| 3 2021–23 | 2022 PO·Season말단 위임 선택, 신인 별도선택 보존·후속 미완료 |','| 4 장기커리어 | 진행 |','| 5 전체구조 | 현행 기능등록기 참조 |','| 6 규격·Context Pack | 현행 source등록기 참조·Pack0 |','| 7 통합·작가승인 | 미완료 |','','미완료 큰묶음5/6번까지4 · v0.30 PARTIAL · CLOSED · 원고0.','']
 return '\n'.join(lines)

def self_test():
 original=select_series
 def winner_bad(*a,**kw):
  v=original(*a,**kw);v['selected_games'][0]['selected_regulation_winner']='CHI';return v
 with patch(__name__+'.select_series',winner_bad):
  try:build()
  except AssertionError:pass
  else:raise AssertionError('FALSE_PASS winner')
 original_p=participation
 def ban_bad(*a,**kw):
  v=original_p(*a,**kw)
  if v is not None:v['real_NYC_legal_ban']=True
  return v
 with patch(__name__+'.participation',ban_bad):
  try:build()
  except AssertionError:pass
  else:raise AssertionError('FALSE_PASS continuing NYC ban')
 original_o=option_join
 def notice_bad(*a,**kw):
  v=original_o(*a,**kw);v['actual_notice_receipt']='NBA_CONFIRMED';return v
 with patch(__name__+'.option_join',notice_bad):
  try:build()
  except AssertionError:pass
  else:raise AssertionError('FALSE_PASS actual option receipt')
 original_l=load
 def source_bad(root,p):
  v=original_l(root,p)
  if p==PO:v['series'][-1]['candidate_winner']='UTA'
  return v
 with patch(__name__+'.load',source_bad):
  try:build()
  except AssertionError:pass
  else:raise AssertionError('FALSE_PASS physical source substitution')
 return 4
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();v=build()
 if a.write:
  (ROOT/DECISION).write_text(encoded(v['root_selected_decision']),encoding='utf-8')
  (ROOT/OUT).write_text(encoded(v),encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if a.check:
  assert load(ROOT,OUT)==v and text(ROOT/MD)==markdown(v),'Selected postseason saved stale'
  assert load(ROOT,DECISION)==v['root_selected_decision'] and sha(ROOT/DECISION)==v['source_sha256'][DECISION],'Selected decision record stale'
 print(json.dumps({'current':True,'summary':v['summary'],'selected_champion':v['selected_champion'],'writer_controls':self_test() if a.self_test else None}))
if __name__=='__main__':main()
