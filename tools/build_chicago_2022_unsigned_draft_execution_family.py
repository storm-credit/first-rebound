"""Two contingent 2022 claim/tender functions plus the selected Simonovic overlay.

No ancestor constructors, invented draft identities, or private receipt certificates.
"""
import argparse, copy, hashlib, json
from datetime import date
from pathlib import Path
from unittest.mock import patch
from bs4 import BeautifulSoup
import fitz

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_chicago_2022_unsigned_draft_execution_family.py'
OUT = 'research/CHICAGO_2022_UNSIGNED_DRAFT_EXECUTION_FAMILY_2026_10_07.json'
MD = OUT[:-5] + '.md'
CORE = 'simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json'
RIGHTS = 'research/CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT_2026_10_07.json'
RT = 'research/CHICAGO_2022_SECOND_TENDER_COST_REFINEMENT_2026_10_07.json'
SIM = 'research/SIMONOVIC_2022_23_SELECTED_RIGHTS_FAMILY_2026_10_07.json'
CAL = 'research/SIMONOVIC_2022_23_RIGHTS_CALENDAR_BOUNDARY_2026_10_07.json'
PINS = {
 CORE: 'e7d0f4b15bc06c7cd16a38d158b38a78871fb7372d412639e33bb20c31d225a7',
 RIGHTS: 'bf8087a89af09a817c0a3eb5d4df906a906575a56016c873912db00eccdca9db',
 RT: 'e82cf0a2a7f73eb4dd6ff90e75ee5b3c729b8c2ff000a4b667f901a728acd0ca',
 SIM: 'c404fc401f6c30809ed5098663dd2b277b1c4cb7844d15c697991460f1290ac4',
 CAL: '0c3946ac8cea8fd85bcf7d1a87bace9e52538611d67983a9a70b36ba77c4df66',
}
TMP = Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-chi-unsigned2022-20261007')
CALENDAR = [
 {'id': 'NBA_OPENING_2022', 'url': 'https://pr.nba.com/2022-23-nba-schedule/', 'cache_path': str(TMP/'opening.html'), 'raw_sha256': '9d1fd995db031dc2d3f4a87c0623a47d38df9901cbb96ac1589758d6472aa625', 'http_status': 200},
 {'id': 'NBA_DRAFT_2023', 'url': 'https://pr.nba.com/nba-announces-78-players-expected-to-attend-microsoft-surface-nba-draft-combine-2023/', 'cache_path': str(TMP/'draft2023.html'), 'raw_sha256': 'a84286b9f298eef1eeaf15b48bc90c6d8a02318870a3e4c4a150c83488965204', 'http_status': 200},
]
D22 = date(2022,6,23)
D23 = date(2023,6,22)
OPENING = date(2022,10,18)
PORTS = ['CHI2022_FIRST', 'CHI2022_COMPOSITE_SECOND']

def require(ok, message):
 if not ok: raise ValueError(message)

def sha(path):
 return hashlib.sha256(path.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()

def load(root, f):
 return json.loads((root/f).read_text(encoding='utf-8-sig'))

def chosen_policy():
 return {'new_ports': PORTS, 'holder_if_entitlement_resolves': 'CHI',
 'first_offer_date': '2022-07-08', 'first_acceptance_through': '2022-10-18',
 'first_salary': '100% of the applicable 2022 Rookie Scale Amount in each required year; no new bonus/loan; lawful two guaranteed seasons plus two team-option years, unexercised options.',
 'first_protection': 'At least the VIII1c(ii) mandatory 80% skill/injury protection in first two seasons and first option year, without prohibited individual limitations.',
 'second_offer_date': '2022-08-25', 'second_acceptance_through': '2022-10-15',
 'second_salary': 'One 2022-23 Season at applicable II6 Minimum Annual Salary for an exclusive Draft Rookie with credited YOS0; no new bonus.',
 'delivery': 'Team-signed UPC personally delivered to player or representative',
 'offers_withdrawn_or_rights_renounced': False, 'NBA_UPC_accepted': False,
 'player_receipt_or_nonacceptance_actual_certified': False,
 'new_NBA_registration': False, 'new_author_lock': False,
 'post_D23_exclusive_rights_automatically_inherited': False,
 'foreign_contract_or_early_entry_history_assumed_absent': False,
 'exact_future_pick_rank_or_player_selected': False,
 'selected_template_is_executed_draft': False}

FIXED_POLICY = copy.deepcopy(chosen_policy())

def sources(root):
 d = {}
 for f,h in PINS.items():
  require(sha(root/f)==h, 'Source changed: '+f)
  d[f]=load(root,f)
  require(d[f]==json.loads((root/f).read_text(encoding='utf-8-sig')), 'Physical source loader substitution: '+f)
 require(d[CORE]['summary']['standard']==15 and d[CORE]['summary']['two_way']==2, 'Core slots changed')
 require(d[RIGHTS]['policy']['first_count_upper']==1 and d[RIGHTS]['policy']['second_count_upper']==1, 'Named rights cardinality changed')
 require(d[RIGHTS]['policy']['original_named_claims_preserved_not_rewritten'] and not d[RIGHTS]['policy']['additional_POR_first_from_Markkanen_departure_copied'], 'Wrong new rights imported')
 require(d[SIM]['authority']['root_routine_family_selected'] and not d[SIM]['authority']['all268_families_promoted'], 'Simonovic selected overlay changed')
 require(d[SIM]['period_witness']['target_end']=='2023-06-30' and d[SIM]['period_witness']['one_year_end_in_selected_fiction']=='2023-08-14', 'Simonovic target period changed')
 require(d[RT]['policy']['normal_per_port_conditional_upper']==1018000 and d[RT]['policy']['apron_per_port_conditional_upper']==1837000, 'Minimum bounds changed')
 cal=[]
 for obs in CALENDAR:
  raw=Path(obs['cache_path']).read_bytes()
  require(hashlib.sha256(raw).hexdigest()==obs['raw_sha256'], 'Calendar raw changed')
  article=BeautifulSoup(raw,'html.parser').find('article')
  require(article is not None, 'Official article missing')
  body=article.get_text(' ',strip=True)
  if obs['id']=='NBA_OPENING_2022': require('Oct. 18, 2022' in body, 'Official season opening changed')
  else: require('May 9, 2023' in body and 'on June 22' in body, 'Official next draft changed')
  cal.append({**obs,'extraction':'BeautifulSoup article text; dates only, no real roster/results imported','normalized_extracted_text_sha256':hashlib.sha256(body.encode()).hexdigest()})
 law=d[SIM]['primary_law'];raw=Path(law['cache_path']).read_bytes()
 require(hashlib.sha256(raw).hexdigest()==law['raw_sha256'], 'CBA raw changed')
 pdf=fitz.open(stream=raw,filetype='pdf');pages={}
 for n in [30,210,241,293,294,295,303,304,305,306,307]:
  txt=pdf[n-1].get_text().replace('\r\n','\n').replace('\r','\n')
  pages[str(n)]=hashlib.sha256(txt.encode()).hexdigest()
 require('Subsequent Draft' in pdf[302].get_text() and 'July 15' in pdf[302].get_text(), 'X4 window unavailable')
 require('two (2) weeks before the September 5' in pdf[302].get_text(), 'Second tender window unavailable')
 require('shall exclude amounts with respect to' in pdf[240].get_text() and 'outstanding Required Tender' in pdf[240].get_text(), 'Apron first-tender rule unavailable')
 require('one hundred twenty percent (120%)' in pdf[209].get_text() and 'until the' in pdf[209].get_text(), 'Normal unsignedfirst hold unavailable')
 for obs in d[RIGHTS]['sources']:
  require(hashlib.sha256(Path(obs['cache_path']).read_bytes()).hexdigest()==obs['raw_sha256'], 'Rights provenance raw changed: '+obs['id'])
 return d,{'calendar':cal,'CBA':{**{k:law[k] for k in ['url','cache_path','raw_sha256']},'PDF1based_text_sha256':pages},'rights_provenance':copy.deepcopy(d[RIGHTS]['sources'])}

def instantiate(port, rank, entitled, participant_eligible, when, p=None):
 """Callable conditional execution; no unresolved entitlement becomes an identity.

 The caller must supply source-bound entitlement and PS22 legal participation,
 then use the actual future participant classification after the subsequent draft.
 """
 p=chosen_policy() if p is None else p
 require(p==FIXED_POLICY, 'Selected tender/authority policy changed')
 require(port in PORTS and isinstance(rank,int) and not isinstance(rank,bool), 'Wrong port/rank type')
 require((1<=rank<=30) if port==PORTS[0] else (31<=rank<=60), 'Wrong round or future rank')
 require(entitled is True and participant_eligible is True, 'Entitlement/eligible participant input missing')
 t=date.fromisoformat(when); require(D22<=t<=date(2023,6,30), 'Date outside FY22 source scope')
 first=port==PORTS[0];offer=date.fromisoformat(p['first_offer_date'] if first else p['second_offer_date'])
 accepted_until=date.fromisoformat(p['first_acceptance_through'] if first else p['second_acceptance_through'])
 return {'port':port,'rank_parameter':rank,'round':1 if first else 2,'holder_during_supported_interval':'CHI',
 'date':when,'participant_identity':None,'future_participant_eligible_admitted':True,
 'entitlement_resolved_as_input_not_invented':True,'first_subsequent_draft':D23.isoformat(),
 'rights_state':'SUPPORTED_X4_BASE_INTERVAL_SUBJECT_TO_PARTICIPANT_X5_X6' if t<D23 else 'HOLD_REQUIRED_X4_X5_X6_SUBSEQUENT_TRANSITION',
 'ordinary_X4_exclusive_until':D23.isoformat(),'post_D23_rights_certified':False,
 'tender_delivered_in_selected_function':t>=offer,'tender_outstanding_in_selected_function':offer<=t<=accepted_until,
 'offer_date':offer.isoformat(),'acceptance_through':accepted_until.isoformat(),
 'offer_form':'VIII1_ROOKIE_SCALE_TWO_GUARANTEED_TWO_TEAM_OPTIONS' if first else 'ONE_SEASON_II6_MINIMUM',
 'salary_function':p['first_salary'] if first else p['second_salary'],
 'normal_cap_mechanism':'120_PERCENT_APPLICABLE_ROOKIE_SCALE_WHILE_CHI_HOLDS_RIGHTS' if first else 'NO_UNACCEPTED_SECOND_TENDER_STATUTORY_SALARY_ASSERTED',
 'apron_mechanism':'OUTSTANDING_FIRST_REQUIRED_TENDER_INCLUDED_UNSIGNED_HOLD_EXCLUDED' if first else 'NO_UNACCEPTED_SECOND_TENDER_STATUTORY_SALARY_ASSERTED',
 'normal_reserved_upper':11060000 if first else 1018000,'apron_reserved_upper':11060000 if first else 1837000,
 'reservation_is_post_D23_complete_new_claim_cost_proof':False,'NBA_UPC':False,'STD_slots':0,'TW_slots':0,
 'actual_delivery_acceptance_or_private_terms_certified':False,'new_author_lock':False}

def assert_returned(row, port, rank, entitled, eligible, when, p):
 # Independent field checks at the caller, not a second call to patched constructor.
 t=date.fromisoformat(when);first=port==PORTS[0]
 offer=date.fromisoformat(p['first_offer_date'] if first else p['second_offer_date'])
 last=date.fromisoformat(p['first_acceptance_through'] if first else p['second_acceptance_through'])
 require(row['port']==port and row['rank_parameter']==rank and row['date']==when and row['round']==(1 if first else 2), 'Returned port/rank/date/round differs from caller')
 require(entitled and eligible and row['holder_during_supported_interval']=='CHI' and row['participant_identity'] is None, 'Returned source entitlement/identity changed')
 require(row['future_participant_eligible_admitted'] is True and row['entitlement_resolved_as_input_not_invented'] is True, 'Returned legal input classification changed')
 require(row['rights_state']==('SUPPORTED_X4_BASE_INTERVAL_SUBJECT_TO_PARTICIPANT_X5_X6' if t<D23 else 'HOLD_REQUIRED_X4_X5_X6_SUBSEQUENT_TRANSITION') and not row['post_D23_rights_certified'], 'Returned next draft rights promoted')
 require(row['first_subsequent_draft']==row['ordinary_X4_exclusive_until']==D23.isoformat(), 'Returned subsequent-draft date changed')
 require(row['offer_date']==offer.isoformat() and row['acceptance_through']==last.isoformat(), 'Returned tender dates changed')
 require(row['tender_delivered_in_selected_function']==(t>=offer) and row['tender_outstanding_in_selected_function']==(offer<=t<=last), 'Returned tender state changed')
 require(row['offer_form']==('VIII1_ROOKIE_SCALE_TWO_GUARANTEED_TWO_TEAM_OPTIONS' if first else 'ONE_SEASON_II6_MINIMUM'), 'Returned UPC offer form changed')
 require(row['salary_function']==(p['first_salary'] if first else p['second_salary']), 'Returned source salary function changed')
 require(row['normal_cap_mechanism']==('120_PERCENT_APPLICABLE_ROOKIE_SCALE_WHILE_CHI_HOLDS_RIGHTS' if first else 'NO_UNACCEPTED_SECOND_TENDER_STATUTORY_SALARY_ASSERTED'), 'Returned normal statutory classification changed')
 require(row['apron_mechanism']==('OUTSTANDING_FIRST_REQUIRED_TENDER_INCLUDED_UNSIGNED_HOLD_EXCLUDED' if first else 'NO_UNACCEPTED_SECOND_TENDER_STATUTORY_SALARY_ASSERTED'), 'Returned apron statutory classification changed')
 require(not row['reservation_is_post_D23_complete_new_claim_cost_proof'], 'Future new-claim cost certified')
 require((row['normal_reserved_upper'],row['apron_reserved_upper'])==((11060000,11060000) if first else (1018000,1837000)), 'Returned normal/apron reservation changed')
 require(not row['NBA_UPC'] and row['STD_slots']==row['TW_slots']==0 and not row['actual_delivery_acceptance_or_private_terms_certified'] and not row['new_author_lock'], 'Returned receipt or registration promoted')

def build(root=ROOT):
 d,observed=sources(root);p=chosen_policy();require(p==FIXED_POLICY,'Returned selected policy changed')
 require(date(2022,6,23)<=date.fromisoformat(p['first_offer_date'])<=date(2022,7,15),'First delivery outside X4a')
 require(date(2022,8,22)<=date.fromisoformat(p['second_offer_date'])<=date(2022,9,5),'Second delivery outside X4a')
 require(date.fromisoformat(p['first_acceptance_through'])>=OPENING and date.fromisoformat(p['second_acceptance_through'])>=date(2022,10,15),'Required acceptance window too short')
 preserved=copy.deepcopy(d[CORE]['unsigned_ports']);require([r['port'] for r in preserved]==PORTS+['SIMONOVIC2020_SECOND'],'Core port identity changed')
 keys=['2022-07-01','2022-07-07','2022-07-08','2022-08-25','2022-10-15','2022-10-18','2023-04-09','2023-06-21','2023-06-22','2023-06-30']
 rows=[]
 for port,rank in [(PORTS[0],1),(PORTS[1],31)]:
  for when in keys:
   r=instantiate(port,rank,True,True,when,p);assert_returned(r,port,rank,True,True,when,p);rows.append(r)
 return {'id':'CHICAGO_2022_UNSIGNED_DRAFT_EXECUTION_FAMILY','baseline_main':'15e0e1f2edcc9862b096cc190b752aecbe3aca31',
 'status':'SELECTED_LAWFUL_CONDITIONAL_TENDER_UNSIGNED_TEMPLATE_CURRENT_ENTITLEMENT_IDENTITY_AND_POSTD23_HOLD',
 'source_sha256':{**PINS,SELF:sha(root/SELF)},'source_hash_method':'UTF8 BOM stripped CRLF/CR normalized LF; external raw bytes separate',
 'sources':observed,'selected_policy':p,'source_ports_generation_snapshot':preserved,
 'claims':copy.deepcopy(d[RIGHTS]['positive_claim_bridge']),
 'conditional_interface':{'callable':'instantiate(port, rank, entitled, participant_eligible, when)',
 'rank_domains':{'CHI2022_FIRST':[1,30],'CHI2022_COMPOSITE_SECOND':[31,60]},
 'entitlement_input':'2021-22 selected results/order + preserved 2018 CHI/DET and 2019 WAS/LAL conditional rights; exact priority/exercise must be supplied from published preserved claim, not arbitrary24flags.',
 'participant_input':'Source-bound 2022 qualified selection identity and PS22 lawful participation. No historical Dalen Terry or forfeiture copied from incompatible original Lonzo route.',
 'participant_rights_qualification':'For the supported initial X4 interval supply any applicable X5 current retained period and X6 operative tender/entry/intercollegiate conditions. Eligible-only does not certify those facts; these are admitted lawful family inputs and require participant-specific dispatch when selected.',
 'selected_function_not_resolved_draft_execution':True,'legal_eligibility_is_admitted_candidate_not_actual_medical_paper':True,
 'examples_rank1_rank31_are_not_selected_picks':True},
 'dated_conditional_examples':rows,
 'Simonovic_selected_overlay':{'source':SIM,'period_end':'2023-08-14','FY22_to_June30_supported':True,'first_effective_notice':'2022-08-14','voluntary_offer':'2022-08-25','all268_PASS':False,'actual_foreignlaw_or_notice_absence_certified':False},
 'roster_and_cost':{'STD':15,'TW':2,'accepted_rookie_UPCs':0,'normal_three_port_overreserve':13096000,'apron_three_port_overreserve':14734000,
 'normal_total_source_upper':d[CORE]['summary']['normal_public_family_upper'],'apron_total_source_upper':d[CORE]['summary']['apron_public_family_upper'],
 'new_cost_increase':0,'reservation_is_actual_current_salary':False,'scale_120percent_le_11060000_and_minimum_le_bounds_is_source_family_condition':True,
 'signed_tender_needs_explicit_new_slot_action':True,'new_FY22_hardcap_trigger':False,'whole_post2023draft_new_claim_upper_certified':False},
 'exact_remaining_inputs':[
 {'id':'ENTITLEMENT_2022_TWO_PORTS','input':'Selected 2021-22 standings/draft order plus preserved conditional second-swap entitlement; rank/holder unresolved. Source-supported count1+1 closed, exact two claims not executed.'},
 {'id':'PARTICIPANT_2022_TWO_PORTS','input':'Two lawful draftee identities/entry-age/nonNBA/intercollegiate classification. Typed tender functions closed; no player invented.'},
 {'id':'POST_DRAFT2023_TRANSITION','input':'At2023June22 use participant X4/X5/X6 conditions and any source-selected SubsequentDraft decision; no annual-tender permanent rights or all268 import. Any new2023CHIclaim is separate cost/rights input.'}],
 'certification':{'selected_routine_conditional_offer_policy':True,'two_actual_draft_selections_executed':False,'post_D23_all_new_ports_rights_closed':False,'independent_review_completed':False,'actual_legal_notice_consent_or_receipt_certified':False,'whole_FY22_or_macro3_complete':False,'author_lock':False,'central_changed':False,'manuscript':0},
 'freeze':'v0.30 PARTIAL','gate':'CLOSED'}

def validate(v,root=ROOT):
 try:require(v==build(root),'Saved draft family differs from source-bound construction');return []
 except (ValueError,KeyError,OSError,StopIteration) as e:return [str(e)]

def markdown(v):
 return '\n'.join(['# Chicago 2022 미서명 지명권·Tender 실행 함수','',
 '**조건부 루틴 제안/미수락 함수 선택 · 실제 순번/두 선수/2023 다음Draft 전이는 HOLD.** 기존 코어15STD/2TW와 Simonović 선택 overlay를 보존한다. 독립 검문 대기.','',
 '## 실제 연결한 법적 범위','',
 '자체1R 한 장과 CHI/DET→WAS/LAL 스왑의 복합2R 한 장이라는 공개 명명 cardinality를 사용한다. 원2018·2019 조건은 새24flag로 선택하지 않으며 순번과 플레이어를 원역사에서 복사하지 않는다. 미완료2021–22 결과가 두 entitlement를 결정하면 `instantiate`에 원천 검문된 입력을 공급한다. 예시1/31은 함수 경계값이고 실제지명이 아니다.','',
 '선택한 법적 가상 동의: 첫라운드는 July8 team-signed VIII1 RSC 형식·법정scale100%·2보장+2팀옵션·필수80%보호·개인전달·Oct18까지 수락창을 제공한다. 둘째라운드는 Aug25 한시즌 II6 YOS0 minimum·새보너스0·Oct15 수락창이다. 선수는 자발적으로 NBAUPC를 수락하지 않고 철회/renounce도 하지 않는다. 제출/미수락/실제서명 증명이 아니다.','',
 'CBA I1ddd/X4a의 July15·Aug22–Sep5 및 수락창을 직접 검문했다. [NBA 공식 개막발표](https://pr.nba.com/2022-23-nba-schedule/)의 Oct18과 [다음 Draft 공식 발표](https://pr.nba.com/nba-announces-78-players-expected-to-attend-microsoft-surface-nba-draft-combine-2023/)의2023June22 원HTTP200 raw를 새2개 회수했다. 실제 시즌 승패/상대명단은 수입하지 않았다.','',
 'VII4e는 미서명1R normal120%hold, VII6m3E는 apron에서 일반unsignedhold를 제외하고 outstanding firstRT를 포함한다. 2R미수락제안을 signed급여로 만들지 않는다. 기존11.06m/1.018m/1.837m widened예약을 그대로 유지해 세포트normal13.096m/apron14.734m, 원팀상단170,845,541/172,483,541의 증분0이다. 법정 exactrounding 또는 실제 TeamSalary를 인증하지 않는다.','',
 '## 다음Draft의 실제 경계','',
 'X4a 일반 미서명 권리의 첫 기본구간은2022June23부터2023June22 직전까지다. EarlyEntry/X5의 필요한 유효Tender·원계약/통지 조건은 참가자별 입력으로 남고, 그 상태로의 변환은 실제선수 선정시 검문한다. 다음Draft에서 ordinaryrights 종료/재지명·X6자연연령·X5해외계약을 분기해야 한다. June30까지 자동영구보유라고 표시하지 않았다. 날짜20개 예시 중 이후4행은 명시HOLD이다. 새2023CHI지명 비용은 오래된2022포트가 아니며 별도입력이다.','',
 'Simonović는 기존 선택 no-clock 하위가족의 최초2022Aug14(i)→2023Aug14 기간을 그대로 소비하여 June30까지 별도지원한다. 기존268시계 재생성0/전체PASS0, 정확외국법·기관수락/통지부재 인증0.','',
 '남은 유한입력은 (1)2022 결과/순번/정확복합2R귀속 (2)두 적법참가자 이름·분류 (3)그 두 사람의2023Draft 전이/새2023권리다. 사적영수증이나 미공개전역장부를 새종료조건으로 추가하지 않았다.','',
 '## 검문/현황','',
 '물리원천5핀·공식raw2·기존CBA/권리raw와 소비필드를 직접 연결한다. returned port/rank/date/round/holder/offer형식·가용수락창·급여함수·예약·UPCs/슬롯/실제flag를 caller에서 재검문한다. 작성자 controls는 독립검문으로 세지 않는다.','',
 '|번호|작업|상태|','|---|---|---|','|1|2020 draft|완료|','|2|Chicago2020–21|완료|','|3|2021–23 거래·계약|미서명2포트 함수 선택·실제순번/선수/후속전이 미완|','|4|장기커리어|미완|','|5|전체구조|전체G13 미완|','|6|규격·Pack|S1 완료·실제Pack0|','|7|통합·독립·작가승인|전체 미완|','',
 '미완료5묶음 · [현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md) · v0.30 PARTIAL · 설계/원고 CLOSED · 원고0.',''])

def self_test():
 original=instantiate;names=[]
 for name,key,value in [('wrong_round','round',2),('wrong_holder','holder_during_supported_interval','WAS'),('UPC_promoted','NBA_UPC',True),('post_D23_promoted','post_D23_rights_certified',True)]:
  def bad(*a,key=key,value=value,**kw):
   r=original(*a,**kw);r[key]=value;return r
  with patch(__name__+'.instantiate',bad):
   try:build()
   except ValueError:names.append(name)
   else:raise AssertionError('False pass: '+name)
 return names

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();b=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(b),encoding='utf-8')
 if a.check:require(not validate(load(ROOT,OUT)),'Saved JSON not current');require((ROOT/MD).read_text(encoding='utf-8')==markdown(b),'MD not current')
 print(json.dumps({'current':True,'conditional_examples':len(b['dated_conditional_examples']),'new_STD':0,'new_TW':0,'remaining_named_inputs':len(b['exact_remaining_inputs']),'writer_controls':self_test() if a.self_test else []}))
