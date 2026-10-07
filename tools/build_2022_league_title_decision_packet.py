"""Source-bound authority audit and two mutually exclusive NPC title candidates.

No title adoption, user question, transaction or exact salary selection. The
one-game tactical overlay is a declared fiction parameter, not observed BPM.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
from copy import deepcopy
from unittest.mock import patch
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_league_title_decision_packet.py'
OUT='design/NBA_2022_LEAGUE_TITLE_DECISION_PACKET.json';MD=OUT[:-5]+'.md'
PO='design/NBA_2022_FULL_POSTSEASON_CANDIDATE.json'
P22='reviews/NBA_2022_FULL_POSTSEASON_CANDIDATE_G11_INDEPENDENT_REVIEW_2026_10_08.json'
OPT='research/NBA_2022_CANDIDATE_FINALS_OPTION_JOIN_2026_10_08.json'
DRAW='simulation/NBA_2022_SELECTED_WORKING_DRAW_AND_CONTROL.json'
BOARD='research/NBA_2022_FULL_DRAFT_WORKING_BOARD_2026_10_08.json'
CORE='simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json'
AUTH='control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md'
ORIGINAL_AUTH='canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
BRACKET='canon/DELEGATED_2021_BRACKET_DRAW_DECISION.json'
DENLAL='simulation/DEN_LAL_2021_DELEGATED_SERIES.json'
ALL2021='simulation/NBA_2021_DELEGATED_PLAYOFF_RESULTS.json'
PINS={'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2', 'control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md': '91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d', 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json': '4ee9b74e37903a43b0bd50b35c7f24cbabdac13728097a848b553f874bbeef80', 'canon/DELEGATED_2021_BRACKET_DRAW_DECISION.json': 'd39733d89f7c668dee203df6da03ee9c5fcee1e4f0dee6e0296cc2114f2c2714', 'simulation/DEN_LAL_2021_DELEGATED_SERIES.json': '81332e263b01ef86f5b3c0abea408a89bc926ae36cc7eb4f30d2877fbd1b0354', 'simulation/NBA_2021_DELEGATED_PLAYOFF_RESULTS.json': 'dc1d47563f8381a4b1bd98409f198e8df088ce782622071e22556e8f0c7a7cdb', 'design/NBA_2022_FULL_POSTSEASON_CANDIDATE.json': 'dcefe931a0f82e3733f577cc47a314cc66ad9162a9988d15d7514302424023f5', 'reviews/NBA_2022_FULL_POSTSEASON_CANDIDATE_G11_INDEPENDENT_REVIEW_2026_10_08.json': 'c4f528cf0526e0277e78dc0ac49e107aa122e9dabce83b860c4c1dcdd5df5f59', 'research/NBA_2022_CANDIDATE_FINALS_OPTION_JOIN_2026_10_08.json': '8f253cd314203e281a206027ef4e4031f13144df4b8642331f86ff6c9c69ee18', 'simulation/NBA_2022_SELECTED_WORKING_DRAW_AND_CONTROL.json': '09d7c6613b3710a04600f567340e963d3a3d863851bafd1a8213618dee14ea39', 'research/NBA_2022_FULL_DRAFT_WORKING_BOARD_2026_10_08.json': '3bdad52ebaacda5abb23b9908b8ed3a9b85cfaa09d838819a959cd024a58e940', 'simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json': 'e7d0f4b15bc06c7cd16a38d158b38a78871fb7372d412639e33bb20c31d225a7'}
AUTHORITY_MEANING_SHA='f79a9c4d68aa0740818e9252b304b94729082f29663cb9ee7533a3541a4c75ca'
BASELINE='ee0ff822aa127f8263cc69e03ba2a7184053e22e'
CACHE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-title2022-20261008')
RAW_PINS={'jazz.html': 'be470d6521a2d053a211156219652cd037df4e24b3b57ca1e61e70606ac6f06b', 'release_shell_observation.json': 'd0f0cc6c76f7aea31e0e375212dc5d84ac6b170a5349ec4e0a311d4e30110683', 'sources.json': '6f8a1577e736a0c4148ef01f7637036eaf5c3e2b90cc4fe52dd2957e8cabaa07', 'tracker_web_observation.json': 'da63203a164a73d2ed0e3616fedd8eb2a5554f8da24560c07b584b2499478455', 'wolves.html': 'b09b44732adb543881df0e8b196805cf1192b17e0d3017738e9098f441025bd2', 'wolves_web_observation.json': 'adf67ab11876d2dff6759148407bd674c7b6ed883461b055587d4aa5c43d8a81'}
GOBERT_URL='https://www.nba.com/timberwolves/news/minnesota-timberwolves-acquire-center-rudy-gobert-from-utah-jazz'
TRACKER_URL='https://www.nba.com/news/2022-offseason-trade-tracker'

def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load(root,p):return json.loads(text(root/p)) if p.endswith('.json') else text(root/p)
def sources(root):
 out={}
 for p,h in PINS.items():
  assert sha(root/p)==h,'Pinned source changed '+p
  v=load(root,p);q=json.loads(text(root/p)) if p.endswith('.json') else text(root/p)
  assert v==q,'Returned source differs from physical '+p;out[p]=v
 for p,h in RAW_PINS.items():assert hashlib.sha256((CACHE/p).read_bytes()).hexdigest()==h,'Raw observation changed '+p
 assert out[P22]['independent_review_completed'] is True and out[P22]['source_sha256'][PO]==PINS[PO]
 return out

def title_option(code,po):
 finals=deepcopy(po['series'][-1]);games=deepcopy(finals['games']);counts=Counter()
 overlay=None
 if code=='P22B':
  original=games[-1];margin=Fraction(original['exact_home_proxy_margin']);delta=Fraction(9,4)
  assert original['home']=='MIL' and original['away']=='UTA' and margin>0 and margin-delta<0
  overlay={'applies_only_to':original['id'],'date':original['date'],'recipient_team':'UTA',
   'classification':'EXPLICIT_FICTIONAL_ONE_GAME_TEAM_TACTICAL_EXECUTION_PARAMETER_NOT_PLAYER_GROWTH_OR_OBSERVED_BPM',
   'team_impact_delta_fraction':str(delta),'base_home_proxy_margin':str(margin),
   'adjusted_home_proxy_margin':str(margin-delta),'threshold_for_UTA_win':'delta > '+str(margin),
   'threshold_decimal_diagnostic':float(margin),'numerical_minimum_positive_delta_exists':False,
   'reason':'A candidate improvement in Utah screening/roll spacing and matchup execution on one final game. This term illustrates a possible result choice; no calibrated probability or measured effect claimed.',
   'base_BPM_inputs_player_seconds_positions_registration_unchanged':True,
   'new_score_overtime_contact_injury_or_bonus_trigger_certified':False}
  games[-1]['candidate_regulation_winner']='UTA'
  games[-1]['candidate_tactical_overlay']=deepcopy(overlay)
 for q in games:counts[q['candidate_regulation_winner']]+=1
 return {'id':code,'status':'UNSELECTED_COMPARABLE_CANDIDATE','candidate_champion':'MIL' if code=='P22A' else 'UTA',
  'candidate_Finals_end':'2022-06-20','candidate_Finals_wins':dict(counts),
  'Finals_games':games,'single_game_overlay':overlay,
  'unchanged_first_fourteen_series_digest':digest(po['series'][:-1]),
  'roster_role_clock_template_pool_digest':digest(po['postseason_team_template_pool']),
  'new_contract_salary_Tender_UPC_trade_or_clinical_selection':False,
  'root_or_author_adopted':False,'protagonist_title_MVP_or_franchise_direction_changed':False}

def assert_option(v,code,po):
 assert v['id']==code and v['status']=='UNSELECTED_COMPARABLE_CANDIDATE'
 assert v['candidate_champion']==('MIL' if code=='P22A' else 'UTA')
 assert v['candidate_Finals_end']==po['candidate_last_Finals_date']=='2022-06-20'
 assert v['unchanged_first_fourteen_series_digest']==digest(po['series'][:-1])
 assert v['roster_role_clock_template_pool_digest']==digest(po['postseason_team_template_pool'])
 original=po['series'][-1]['games'];rows=v['Finals_games'];assert len(rows)==7
 assert rows[:6]==original[:6],'An earlier game changed'
 last=deepcopy(original[-1]);overlay=v['single_game_overlay']
 if code=='P22A':assert overlay is None and rows==original
 else:
  delta=Fraction(9,4);margin=Fraction(last['exact_home_proxy_margin']);assert delta>margin
  assert overlay['applies_only_to']==last['id'] and overlay['date']==last['date'] and overlay['recipient_team']=='UTA'
  assert overlay['team_impact_delta_fraction']==str(delta) and overlay['base_home_proxy_margin']==str(margin)
  assert overlay['adjusted_home_proxy_margin']==str(margin-delta)
  assert overlay['base_BPM_inputs_player_seconds_positions_registration_unchanged'] is True
  assert overlay['new_score_overtime_contact_injury_or_bonus_trigger_certified'] is False
  assert overlay['classification']=='EXPLICIT_FICTIONAL_ONE_GAME_TEAM_TACTICAL_EXECUTION_PARAMETER_NOT_PLAYER_GROWTH_OR_OBSERVED_BPM'
  assert overlay['threshold_for_UTA_win']=='delta > '+str(margin)
  assert overlay['threshold_decimal_diagnostic']==float(margin) and overlay['numerical_minimum_positive_delta_exists'] is False
  assert overlay['reason']=='A candidate improvement in Utah screening/roll spacing and matchup execution on one final game. This term illustrates a possible result choice; no calibrated probability or measured effect claimed.'
  last['candidate_regulation_winner']='UTA';last['candidate_tactical_overlay']=deepcopy(overlay)
  assert rows[-1]==last,'Returned one-game overlay changed source ingredients'
 assert v['candidate_Finals_wins']==dict(Counter(q['candidate_regulation_winner'] for q in rows))
 assert v['candidate_Finals_wins']==({'MIL':4,'UTA':3} if code=='P22A' else {'MIL':3,'UTA':4})
 assert v['new_contract_salary_Tender_UPC_trade_or_clinical_selection'] is False
 assert v['root_or_author_adopted'] is False and v['protagonist_title_MVP_or_franchise_direction_changed'] is False

def authority(src):
 agents=src['AGENTS.md'];scope=src[AUTH];p=src[ALL2021]
 assert 'championships and their league-wide butterfly effects' in agents
 assert '건강·시즌 결과·문체 권고안 선택을 위임' in scope
 assert '기술 산출물' in scope and '그 자체로 새 인간 승인을 요구하는 규칙이 아니다' in scope
 assert p['champion']=='MIL' and p['runner_up']=='PHX'
 assert p['authority']==ORIGINAL_AUTH and p['series'][-1]['winner']=='MIL'
 assert src[DENLAL]['authority']==ORIGINAL_AUTH and src[DENLAL]['selected_winner']=='LAL'
 assert src[BRACKET]['classification']=='AUTHOR_DELEGATED_DESIGN_SELECTION'
 return {'classification':'ROOT_SCOPE_DISPOSITION_REQUIRED_BEFORE_ADOPTION_NOT_A_NEW_HUMAN_APPROVAL_REQUEST',
  'positive_existing_delegation_evidence':[
   {'source':AUTH,'meaning':'Delegated health/season/style continues after the original H00/K1/L2 snapshot; routine qualified NPC family choices need no repeat permission.'},
   {'source':BRACKET,'meaning':'2021 bracket/draw is a later delegated selection; by itself it explicitly does not select series outcomes.'},
   {'source':DENLAL,'meaning':'Later delegated local series LAL4-2DEN adds modeled availability; no downstream title or private certification inferred.'},
   {'source':ALL2021,'meaning':'A complete 15-series delegated result source explicitly chose MIL4-2PHX championship as a design anchor. This is actual NPC champion-selection precedent, not a bracket-only inference.'}],
  'contrary_or_boundary_evidence':[
   {'source':'AGENTS.md','meaning':'Consequential choices include championships and league butterfly effects; franchise/core/MVP/long-ending changes cannot be self-approved.'},
   {'source':AUTH,'meaning':'Delegation does not automatically decide franchise moves, important core trades, title-count/long-ending changes, awards or final manuscript gate.'},
   {'source':ORIGINAL_AUTH,'meaning':'The Oct2 not-certified list includes exact title counts; this is its snapshot scope, not a categorical ban on later delegated result designs.'}],
  'substantive_findings':{
   'technical_unselected_flag_alone_is_new_author_permission_rule':False,
   'new_Chicago_franchise_core_MVP_year_or_protagonist_title_count_change_identified':False,
   'new_NPC_2022_title_is_material_league_history_change':True,
   'NPC_title_precedent_supports_root_delegated_result_selection_after_review':True,
   'both_options_preserve_Chicago_elimination_contracts_and_draft_controls':True,
   'root_final_interpretation_required':True,
   'human_approval_newly_proven_mandatory_for_all_NPC_champions':False,
   'Utah_rebuild_or_other_important_franchise_transaction_automatically_authorized':False},
  'recommendation':'Root may use the existing delegated-season precedent to adopt P22A as an NPC derived result if no concrete approved long-term direction conflicts. Do not add a blanket human-title gate from generation flags. If an actual approved franchise/title-count/ending collision is identified, retain that consequential promotion for the author with this packet; continue independent work without a new question here.',
  'root_disposition_recorded':False,'author_decision_requested_or_inferred':False}

def build(root=ROOT):
 src=sources(root);po=src[PO];auth=authority(src)
 assert digest(auth)==AUTHORITY_MEANING_SHA,'Returned authority differs from reviewed source interpretation'
 assert po['certification']['championship_author_locked'] is False and po['candidate_champion']=='MIL'
 assert src[OPT]['summary']['all_ten_date_inequalities_pass'] is True
 options=[]
 for code in ['P22A','P22B']:
  v=title_option(code,po);assert_option(v,code,po);options.append(v)
 failures=json.loads(text(CACHE/'sources.json'))
 assert all(v['http_status']==403 and v['adopted_raw_body'] is False for v in failures.values())
 # Whole web-tool observations remain observations; rejected direct HTML is never body.
 observed={k:json.loads(text(CACHE/k)) for k in ['wolves_web_observation.json','tracker_web_observation.json']}
 a=json.dumps(observed['wolves_web_observation.json'],ensure_ascii=False)
 b=json.dumps(observed['tracker_web_observation.json'],ensure_ascii=False)
 assert GOBERT_URL in a and 'July 6, 2022' in a and 'Walker Kessler' in a
 assert TRACKER_URL in b and 'Sept. 3' in b and 'Lauri Markkanen' in b and '2028 pick swap' in b
 return {'id':'NBA_2022_LEAGUE_TITLE_DECISION_PACKET','baseline_main':BASELINE,
  'status':'TWO_COMPLETE_COMPARABLE_NPC_TITLE_CANDIDATES_ROOT_AUTHORITY_DISPOSITION_PENDING',
  'source_sha256':{**PINS,SELF:sha(root/SELF)},'authority_audit':auth,'options':options,
  'recommended_option':'P22A','reason':'Retain one pre-existing fixed BPM/EB/home2 model and all computed games; P22B adds a declared, uncalibrated G7 tactical term only. Neither option can automatically supply Utah rebuild motivation, lawful return assets or future team rosters.',
  'primary_historical_reference_provenance':{
   'capture_directory':str(CACHE),'raw_or_web_capture_sha256':deepcopy(RAW_PINS),
   'direct_HTTP_failed_attempts':deepcopy(failures),
   'web_tool_body_observations_used_not_raw_NBA_bytes':True,
   'official_release_open_was_iframe_only':{'Cavaliers':'https://www.nba.com/cavaliers/news/releases-mitchell-trade-220903','Jazz':'https://www.nba.com/jazz/news/utah-jazz-acquire-agbaji-markkanen-sexton-and-future-draft-assets','body_certified':False},
   'historical_events_only':[
    {'date':'2022-07-06','source':GOBERT_URL,'scope':'Official team indexed body; NBA original event, not alternate execution',
     'to_MIN':'Rudy Gobert','to_UTA_players_or_rights':['Patrick Beverley','Malik Beasley','Jarred Vanderbilt','Leandro Bolmaro','Walker Kessler'],
     'MIN_first_years':[2023,2025,2027,2029],'swap_year':2026,'exact_protection_clause_certified_here':False},
    {'date':'2022-09-03','source':TRACKER_URL,'scope':'NBA official tracker web body corresponding entry; header date is not the event date',
     'to_CLE':'Donovan Mitchell','to_UTA_players':['Collin Sexton','Lauri Markkanen','Ochai Agbaji'],
     'CLE_first_years':[2025,2027,2029],'swap_years':[2026,2028],'exact_guarantees_bonus_or_protection_certified_here':False}]},
  'named_butterfly_ports':[
   {'event':'Original Gobert-to-MIN exchange','already_changed_input':'Kessler is current CHI18 working board candidate, not MIN historical22. MIN rival/roles and current rights also differ.','effect_A':'A finalist Utah season requires an explicit franchise decision and admissible return package before any rebuild.','effect_B':'A Utah championship increases a plausible retention incentive, but does not legally prohibit or logically prove any trade.','auto_import_in_either':False},
   {'event':'Original Mitchell-to-CLE exchange','already_changed_input':'Markkanen remains approved Chicago core; he is not a CLE-owned return asset. Agbaji/NBA2022 players are candidate rights only until selected.','effect_A':'Original Markkanen/Sexton/Agbaji bundle cannot be copied as alternate chain.','effect_B':'Same asset collision; Utah title is an additional motivation issue, not a new matching exception.','auto_import_in_either':False},
   {'event':'MIL championship core','effect_A':'Adds this NPC league title in a candidate history only; current roster/UPCs remain unchanged.','effect_B':'MIL loses only FinalsG7; no automatic coaching dismissal, new salary, MVP or star move.','auto_import_in_either':False}],
  'preservation':{'existing_first_fourteen_series_and_CHI_PHI_seven':True,'same_16_STD_rosters_active_and_source_role_clocks_240':True,
   '2021_22_1230_records_seeds_playin':True,'selected_2022_draw_origin_rank_holder_table':True,
   'Chicago_18_and_57_board_comparisons':True,'existing_original_salary_Gamma_and_current_core':True,
   'Finals_both_end_June20_and_option_open_June21':True,'two_original_Oct1_notices_timely_conditional':True,
   'new_price_trade_Tender_UPC_or_option_exercise':False,
   'original_contract_salary_and_bonus_functions_preserved_not_identical_realized_payments':True,
   'title_contingent_original_Gamma_payoff':'If an original championship bonus exists, evaluate its preserved function against the eventual chosen title; no bonus term, unknown component or realized payment is zeroed. Existing universal upper remains its source bound, not proof of equal actual payouts.'},
  'macro_effects':{'3':'Candidate2022closeout endpoint/title; 2022-23/2023 inputs and named Utah transaction ports remain separate.',
   '4':'No protagonist title-count/MVP/franchise-ending lock; future opponents/core incentives need causal choices before consumption.',
   '5':'Use title as conditional league background only; no new function/episode or automatic narrative result.',
   '6':'Context Pack cannot assert the NPC title or Utah rebuild as canon until the current choice is adopted; Pack0 stays.'},
  'certification':{'independent_review_completed':False,'root_adoption_recorded':False,'author_locked':False,
   'calibrated_probability_or_actual_score_clinical_private_receipt':False,'whole_macro3_G13_G16_or_manuscript':False},
  'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}

def validate(v,root=ROOT):return [] if v==build(root) else ['Title decision packet differs from bound sources and candidate math']
def markdown(v):
 b=v['options'][1]['single_game_overlay'];m=float(Fraction(b['base_home_proxy_margin']));n=float(Fraction(b['adjusted_home_proxy_margin']))
 return '\n'.join(['# 2022 리그 우승 · 권한 감사와 비교 후보','','**권고 P22A: MIL4–3UTA, 후보 말단6/20.** 현재 고정BPM/EB/home2의 모든결과를 보존한다. P22B는 같은 Finals 첫6게임과 모든 앞선14시리즈를 보존하고 G7만 Utah의 명시적 팀 전술효과9/4로 바꾸는 후보이다. 둘은 상호배타적이며 둘다 미채택이다.','','| 후보 | 우승 | Finals | 유일한 차이 |','|---|---|---|---|','| P22A 권고 | MIL | 4–3 / 6/20 | 기존 모델 그대로 |',f'| P22B | UTA | 4–3 / 6/20 | G7 MIL홈 proxy {m:.6f}에 UTA전술 +2.25 → {n:.6f} |','','B는 명시적 가상 스크린·롤 간격/매치업 실행효과의 한 경기 비교값이다. 원proxy는 실제점수차/승률이 아니며 팀효과가 관측됐다는 증거가 아니다. δ>원마진이 승자변경 조건이며 엄밀한 최소 양의 δ는 존재하지 않는다. 변경게임수는1이고 모든선수분/포지션/active/STD·240분/기존계약과Γ는 같다. 새건강/성장/가격/OT/실점수0. 법적 참가·급여를 바꾸지 않는 후보로 구성 가능하다.','','## 기존 권한의 양면 근거','','AGENTS는 우승과 리그 나비효과를 중요선택 예시로 둔다. control 위임은 시즌결과 후속 설계를 허용하되 기존 방향을 바꾸는 프랜차이즈·중요코어·우승횟수/장기결말을 자동 잠그지 않는다. 기술 unselected 자체는 새인간승인 규칙이 아니다.','','2021 bracket/draw는 시리즈결과를 선택하지 않았고 DEN–LAL은 국소시리즈만 선택했다. 그러나 별도 NBA_2021_DELEGATED_PLAYOFF_RESULTS의 전체15시리즈/F1은 같은위임으로 MIL4–2PHX 우승을 실제설계 선택한 직접선례다. 최초권위의 미인증 목록을 후속NPC우승 영구금지로 읽을 근거는 부족하다.','','이번 A/B에서 새 Chicago 프랜차이즈·성장코어·주인공 우승수/MVP/장기결말 잠금 충돌은 확인되지 않았다. NPC2022 우승은 리그역사에 중요한 차이지만 그 fact만으로 모든NPCchampion에 새사람승인을 만들 수 없다. **권고: root가 선례·구체후손충돌을 검문해 A의 파생결과를 기존시즌위임으로 선택할 수 있는지 최종판정한다.** 실제 승인방향충돌이 드러나면 해당중요승격만 작가결정 대상으로 보존한다. 이패킷은 새질문/재승인/자동채택을 하지 않는다.','','## Utah 원역사 사건과 현재 입력 충돌','','[Wolves 공식 Gobert 발표](https://www.nba.com/timberwolves/news/minnesota-timberwolves-acquire-center-rudy-gobert-from-utah-jazz)와 [NBA 공식2022거래표](https://www.nba.com/news/2022-offseason-trade-tracker)의 해당두사건을 유한비교 원자료로 보존했다. 날짜/실명/픽연도는 JSON historical_events_only에만 기록한다. 직접HTML2건403은 본문증거0, 팀원문indexed body/리그표web본문 관측을 분리한다. Cavaliers/Jazz release 일반open은iframe뿐이라 원raw본문 인증0.','','Gobert묶음의 Kessler는 현CHI18 작업보드와, Mitchell묶음의 Markkanen은 이미승인Chicago성장코어와 충돌한다. 이충돌은 타이틀A/B 이전에 존재하므로 어느안에서도 원Utah재건/자산/급여/순번을 그대로 복사할 수 없다. Utah 준우승/우승은 잔류·거래의 인센티브 차이를 설계할 이유지만 실제트레이드 불가/필수의 법규가 아니다. 새목적지/중요코어 거래는 별도원자행과 합법가족·인과검문이 필요하다.','','## 보존과 후속','','원정규1230/시드/플레이인/CHI4/30탈락·7경기와 두 원10/1옵션통지는 그대로다. 두안의말단6/20은 조건부창6/21을같이 지지하지만 현재실제Season말단은 아니다. 2022선택추첨/정확60origin-holder/CHI18·57 비교/15+2와 FY22원급여·보호는 불변. MVP/선수UPC/Tender/새현금/원Utah거래선택0.','','3번: 후보2022결산·다음시즌/Utah명명경로가 남는다. 4번: 주인공의정확우승·MVP·장기결말을 추가잠그지 않는다. 5번: 리그배경이 회차/기능확정으로 자동승격되지 않는다. 6번: 미채택우승/재건을 실제Context Pack fact로 쓰지 않으며 Pack0이다.','','[전체 PO 후보](NBA_2022_FULL_POSTSEASON_CANDIDATE.md) · [조건부 옵션 연결](../research/NBA_2022_CANDIDATE_FINALS_OPTION_JOIN_2026_10_08.md) · [현행 로드맵](WORLD_BIBLE_COMPLETION_ROADMAP.md)','','| 묶음 | 상태 |','|---|---|','| 1 드래프트 연쇄 | 완료 |','| 2 Chicago2020–21 | 완료 |','| 3 2021–23 | 우승 비교후보/권위감사, 채택·후속 미완료 |','| 4 장기커리어 | 진행 |','| 5 전체구조 | 현행 기능등록기 참조 |','| 6 규격·Context Pack | 현행 source등록기 참조·Pack0 |','| 7 통합·작가승인 | 미완료 |','','미완료 큰묶음5/6번까지4 · v0.30 PARTIAL · CLOSED · 원고0.',''])

def self_test():
 original=title_option
 for field,value in [('root_or_author_adopted',True),('candidate_champion','CHI')]:
  def wrong(*a,field=field,value=value,**kw):
   v=original(*a,**kw);v[field]=value;return v
  with patch(__name__+'.title_option',wrong):
   try:build()
   except AssertionError:pass
   else:raise AssertionError('FALSE_PASS '+field)
 def bad_delta(*a,**kw):
  v=original(*a,**kw)
  if a[0]=='P22B':v['single_game_overlay']['team_impact_delta_fraction']='0'
  return v
 with patch(__name__+'.title_option',bad_delta):
  try:build()
  except AssertionError:pass
  else:raise AssertionError('FALSE_PASS tactical delta')
 original_authority=authority
 def bad_authority(*a,**kw):
  v=original_authority(*a,**kw);v['root_disposition_recorded']=True
  v['substantive_findings']['human_approval_newly_proven_mandatory_for_all_NPC_champions']=True
  return v
 with patch(__name__+'.authority',bad_authority):
  try:build()
  except AssertionError:pass
  else:raise AssertionError('FALSE_PASS authority interpretation')
 return 4
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if a.check:assert load(ROOT,OUT)==v and text(ROOT/MD)==markdown(v),'Title packet stale'
 print(json.dumps({'current':True,'options':2,'recommendation':v['recommended_option'],'champions':[q['candidate_champion'] for q in v['options']],'adopted':False,'writer_controls':self_test() if a.self_test else None}))
if __name__=='__main__':main()
