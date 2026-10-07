"""A bounded overseas continuation proposal; no automatic foreign renewal.

NBA-CBA consequences are separated from the validity/consents of a new foreign
agreement. Exact additional-period measurement is exposed for review, not
defined to be legal by the desired final date.
"""
import argparse
import copy
import hashlib
import json
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch
import fitz
import build_simonovic_2021_rights_retention as initial

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_simonovic_2021_22_rights_continuation.py'
OUT='research/SIMONOVIC_2021_22_RIGHTS_CONTINUATION_2026_10_07.json'
MD=OUT[:-5]+'.md'
START=date(2021,8,13)
SCOPE_END=date(2022,6,30)
SENSITIVITY_END=date(2022,8,12)
NEW_SIGN=date(2021,9,2)
PINS={
 'research/SIMONOVIC_2021_RIGHTS_RETENTION_2026_10_07.json':'46b279094156c4ff66f8f7cf380061658b59cd049d4125804799e31d9d33fe0a',
 'tools/build_simonovic_2021_rights_retention.py':'fc0a341e94ebb280285859995107ec2ba2d7f94d5cc3a7ded032130ba881e83d',
 'simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json':'11140e49baa665f18e267fa6419efa238302250b724fa51cfd3262b010b4a312',
 'research/O15G15BE_SIMONOVIC_OLIMPIJA_MEGA_LOAN_CHAIN.md':'c7cdcc51e813cc9187af26b752f2f175205bdfb4b3d1db305e0abc7aa6cb5d6b',
 'canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json':'e0d8ed1f82c494a3610a91c779eef5573737f9b818088c903786cb12afae7dc9',
 'AGENTS.md':'67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2'}
SOURCES=[initial.OUT,initial.SELF,initial.SQ,
    'research/O15G15BE_SIMONOVIC_OLIMPIJA_MEGA_LOAN_CHAIN.md',
    'canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json','AGENTS.md']


def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))


def fixed_inputs():
    assert set(SOURCES)==set(PINS)
    for p,pin in PINS.items():assert sha(p)==pin,'Unreviewed upstream '+p
    prior=load(initial.OUT);assert not initial.validate(prior)
    assert prior['independent_review_completed']
    assert prior['summary']['scope_end']=='2021-08-12'
    assert prior['rights_clock']['earliest_possible_X5a_expiry']=='2021-11-18'
    assert prior['working_policy']['new_NonNBA_signings_from_initial_draft_through_scope_end']==0
    assert prior['roster_and_cost']['standard_contract_count_preserved']==15
    return prior


def proposal():
    return {'classification':'FICTION_CANDIDATE_NEW_NONNBA_AGREEMENT_NOT_AUTHOR_LOCKED',
      'new_foreign_signing_date':'2021-09-02',
      'proposed_playing_organization':'Mega Basket, Serbia — proposed affiliation only, not copied actual2021–22 employment',
      'legal_employer':'Existing admitted foreign employer if it lawfully agrees, or a duly substituted Mega entity under required lawful consents; exact corporate identity unselected',
      'Petrol_Cedevita_Mega_entities_automatically_equated':False,
      'new_service_term':['2021-09-02','2022-08-13'],
      'professional_service_pay':'F>0, negotiated compensation for professional basketball services in excess of a separately identified living-expense stipend',
      'foreign_transfer_release_and_service_pay_currency_amounts':None,
      'foreign_parties_not_NBA_pay_any_lawful_release_or_service_obligations':True,
      'NBA_funded_buyout_reimbursement_salary_or_new_UPC':False,
      'required_foreign_legal_conditions':[
          'Player and correct new employer agree to the new contract.',
          'Every existing employer, lender/loaning club and other relevant rights holder supplies any legally necessary release/consent, or the applicable restriction has already lawfully ended.',
          'No assumption that NBA availability releases restrictions on signing for another foreign club.',
          'The agreement is valid under applicable foreign law and covers part of the2021–22NBA Season.',
          'A proposed NBA-out permits a valid fresh NBA availability notice, but does not retroactively erase original foreign obligations. Any necessary release is part of the proposed consensual execution, not an original fact.'],
      'bona_fide_CHI_negotiation':'Player/representative genuinely reviews the one-Season minimum NBA tender, available role and availability with Chicago; does not accept it and chooses the proposed overseas services. Negotiation is not simulated merely by naming a tender.',
      'valid_annual_RequiredTender':{
          'team_signed':True,'one_Season_standard_UPC':True,'statutory_minimum_or_greater':True,
          'player_accepted':False,'withdrawal_or_renunciation':False,
          'delivery':'Personal delivery to player/representative in the applicable operative W21, on or before applicable B21 for X5b; acceptance open until at least operative A21.',
          'calendar':'W21/B21/A21 are applicable institutional rule inputs; exact modified endpoints and actual receipt are null.',
          'pending_July1_notice_and_September1_actual_availability_branch':{
              'condition':'Preserve every original by-July1 notice. If its September1 factual no-impediment condition is met, supply the required offer by September10 under5b, or the applicable legally adjusted B21.',
              'timely_5b_tender_supplied':True,
              'ordinary_5b_latest_date':'2021-09-10',
              'selection':'Choose a permitted timely delivery date in W21 satisfying B21; if a lawful earlier due date already fell in the accepted prior window, reuse that preserved compliant offer rather than inventing a later delivery.',
              'actual_delivery_or_unamended_calendar_certified':False},
          'if_a_2022_annual_tender_is_due_before_scope_end':'Supply the same compliant unaccepted offer in the applicable operative W22; no guessed2022 deadline.'},
      'fresh_effective_availability_notice':{
          'no_new_effective_notice_before':'2021-09-02',
          'immediate_notice_candidate':'2021-09-02 only if all contractual/legal NBA impediments are lawfully removed; otherwise choose the first later valid date within the new rule cycle, or keep it ineffective.',
          'delivery':'Written personal/certified/registered/overnight delivery to general manager and League Office under X5g.',
          'possible_next_season_notice_cycle':['2021-09-01','2022-08-30'],
          'actual_notice_or_foreign_release_certified':False},
      'prior_pending_availability_notices':'Preserve Γ; test whether each actually becomes effective at its stated condition date. Never discard a prior notice merely to obtain a later clock.',
      'new_NBA_UPC_through_scope_end':False,'new_rights_assignment':False,
      'actual_foreign_agreement_consents_or_payment_certified':False,
      'new_author_lock':False}


FIXED_PROPOSAL=copy.deepcopy(proposal())


def checked_proposal():
    p=proposal();assert p==FIXED_PROPOSAL,'New foreign/NBA/tender policy changed'
    assert p['new_foreign_signing_date']=='2021-09-02'
    assert not p['Petrol_Cedevita_Mega_entities_automatically_equated']
    assert p['new_service_term']==['2021-09-02','2022-08-13']
    t=p['valid_annual_RequiredTender']
    assert t['team_signed'] and t['one_Season_standard_UPC'] and t['statutory_minimum_or_greater']
    assert not t['player_accepted'] and not t['withdrawal_or_renunciation']
    assert t['pending_July1_notice_and_September1_actual_availability_branch']['timely_5b_tender_supplied']
    assert t['pending_July1_notice_and_September1_actual_availability_branch']['ordinary_5b_latest_date']=='2021-09-10'
    assert t['if_a_2022_annual_tender_is_due_before_scope_end']=='Supply the same compliant unaccepted offer in the applicable operative W22; no guessed2022 deadline.'
    assert not p['NBA_funded_buyout_reimbursement_salary_or_new_UPC']
    return p


def rules():
    raw=initial.CBA.read_bytes();assert hashlib.sha256(raw).hexdigest()==initial.CBA_SHA
    pdf=fitz.open(stream=raw,filetype='pdf');result=[]
    for n in [30,32,301,302,303,304,305,306,307]:
        t=pdf[n-1].get_text().replace('\r\n','\n').replace('\r','\n')
        result.append({'PDF_1based':n,'text_sha256':hashlib.sha256(t.encode()).hexdigest()})
    d=' '.join(pdf[304].get_text().split())
    assert 'additional one-year periods as measured in and' in d
    assert 'in accordance with the provisions of Section 5(a)' in d
    return {'url':initial.raw_sources()[-1]['url'],'cache_path':str(initial.CBA),
        'raw_sha256':initial.CBA_SHA,'pages':result,
        'capyear_source':'ArticleI1(nnn), PDF32/printed10: July1 through followingJune30; NBASeason is separately defined by1(ooo).',
        'interpretation_boundary':'X5d explicitly authorizes additionalone-year periods under5a, but does not say new signing itself is a notice, or specify that every original past notice is replaced. Exact endpoint mapping is a reviewable relation, not a factual expiry certificate.'}


def active_domain(prior):
    rows=[]
    for x in prior['rights_clock']['immediate_notice_cells']:
        begin=date.fromisoformat(x['hypothetical_effective_immediate_notice_date'])
        end=date.fromisoformat(x['X5a_one_year_expiry'])
        assert begin<NEW_SIGN<end
        rows.append({'original_clock_start':begin.isoformat(),'original_one_year_end':end.isoformat(),
            'new_nonNBA_signing_occurs_in_original_active_period':True,
            'X5d_conditions':'Lawful new NonNBA signing + bona fide NBA negotiation + compliant tender supplied; all proposed, actual agreements null.',
            'additional_one_year_authorized_by_rule':True,
            'exact_additional_period_start_or_end':None,
            'candidate_window_supported_by_rule_relation':True,
            'target_end_certified_from_old_clock_alone':end>SCOPE_END})
    assert len(rows)==268
    return rows


def build():
    prior=fixed_inputs();p=checked_proposal();raw=initial.raw_sources();rule=rules();active=active_domain(prior)
    # These are transparent clock sensitivity witnesses, not alternate private
    # contracts selected as facts. Their difference exposes the prior Aug13 bug.
    aug13_old_cycle=date(2021,7,29).replace(year=2022)
    fresh_min=date(2021,9,2).replace(year=2022)
    assert SCOPE_END<aug13_old_cycle<SENSITIVITY_END<fresh_min
    return {'id':'SIMONOVIC_2021_22_RIGHTS_CONTINUATION_2026_10_07',
        'schema':'SIMONOVIC_BOUNDED_NONNBA_CONTINUATION_CANDIDATE_V1',
        'status':'INDEPENDENTLY_REVIEWED_CONDITIONAL_NBA_CBA_WINDOW_SUFFICIENT_IMPLEMENTATION_FAMILY',
        'source_sha256':{**PINS,SELF:sha(SELF)},
        'source_hash_method':'UTF8BOMstripped;CRLF/CRtoLF',
        'raw_sources_reused':raw,'primary_transition_rule':rule,
        'new_retrieval_failure_not_used':{'url':'https://pr.nba.com/nba-draft-2022-presented-by-state-farm-by-the-numbers/',
            'http_status':403,'bytes':425,'cache_path':'C:/Users/Storm Credit/AppData/Local/Temp/fr-simonovic-nba-draft2022-20261007.html',
            'raw_sha256':'c05d4fbe97fcd54593543973544d8f2346fb84b0469902a1fe831df4d06ca4eb',
            'used_for_clock_certificate':False},
        'scope':{'start':'2021-08-13','target_end':SCOPE_END.isoformat(),
            'scope_definition':'The2021–22NBA SalaryCapYear, endingJune30; not an invented annualAugust12 completion gate.',
            'separate_post_cap_year_sensitivity_end':SENSITIVITY_END.isoformat(),
            'prior_Aug12_accepted_proof_preserved':True,'new_foreign_proposal_author_selected':False,
            'whole_macro3_complete':False,'whole_actual_foreign_law_certified':False,
            'actual_private_contracts_not_required_as_new_gate':True,'indefinite_rights':False,
            'actual2021_08_18_NBA_activation_copied':False,'independent_review_completed':True},
        'candidate_written_terms':p,
        'Gamma_domains':[
            {'id':'G_ACTIVE_OLD_CLOCK','cells':active,
             'proposal':'Sept2 lawful newNonNBA services, genuine Chicago negotiation and valid annual tender invoke X5d; preserve the exact original notice(s) Γ. Fresh notice is not assumed to replace every prior one.',
             'supported':'Rule-authorized additionalone-year continuation conditional on the written proposal conditions.',
             'NBA_CBA_capyear_window_sufficiently_supported':True,
             'exact_whole_window_certificate':'Candidate NBA-lawful conditions support the bounded window; exact original or additional expiry remains null.'},
            {'id':'G_NO_CLOCK_NO_PENDING_OLD_CYCLE_NOTICE','proposal':'Do not add an effective new availability notice beforeSept2. If available, give the valid Sept2 written notice; if still impeded, it becomes effective only after the impediment lawfully ends.',
             'fresh_clock_min_end':'2022-09-02',
             'support':'Within the Sept2021–Aug2022 new cycle, immediate basis isSept2 or later; a following-season draft basis cannot precedeSept2. No exact2022 draft date is needed for this ordering.',
             'whole_target_under_these_conditions_supported':True},
            {'id':'G_PENDING_OLD_CYCLE_OR_CONDITIONAL_NOTICE','proposal':'Preserve pending Γ notice. If it becomes effective beforeSept2, use activeold branch. If it remains ineffective due to original impediments, do not treat NBA availability as foreign signing permission; the new lawful foreign contract and its consents must be separately admitted.',
             'whole_target_automatically_supported':False,
             'NBA_CBA_capyear_window_supported_with_timely_5b_tender_and_admitted_foreign_q':True,
             'named_boundary':'Preserve any earlier original notice and timely5b tender branch; apply positive additional-period lower bound when needed. Exact expiry is not required to supportJune30; cannot overwrite Γ or extend the old contract by assertion.'}],
        'bounded_additional_period_relation':{
            'classification':'SOURCE_SUPPORTED_LEGAL_INFERENCE_UNDER_EXPLICIT_FOREIGN_AND_TENDER_CANDIDATE_CONDITIONS',
            'source':'X5d positive additional one-year measured under5a, PDF305; retained initialdraft anchor2020Nov18.',
            'structures':[
                {'id':'ORIGINAL_PERIOD_ADDITION','earliest_original_end':'2021-11-18','additional_duration_years':1,'sufficient_lower_end':'2022-11-18','actual_exact_e_plus_1_selected':False},
                {'id':'NEW_5a_MEASUREMENT','fresh_effective_basis_not_before':'2021-09-02','fresh_basis_sufficient_lower_end':'2022-09-02','conservatively_preserved_earlier_draft_basis':'2021-07-29','earlier_basis_sufficient_lower_end':'2022-07-29'}],
            'not_all_imaginable_legal_interpretations_certified':True,
            'old2020_draft_plus1_end_not_counted_as_new_additional_period':'Reusing2021Nov18 as the only endpoint erases5d additional duration; it is the original period, not the admitted continuation relation.',
            'common_sufficient_lower_end':'2022-07-29','capyear_end':'2022-06-30','strict_margin_days':29,
            'exact_actual_additional_start_and_expiry':None,
            'post_June30_2022_new_capyear_requires_separate_review':True,
            'August12_sensitivity_is_not_completion_requirement':True},
        'clock_counterexample_and_repair':{
            'Aug13_new_notice_plus_next2021_22_intent_can_use_July29_2021_draft_basis':True,
            'hypothetical_year_end':'2022-07-29','misses_optional_Aug12_sensitivity_by_days':(SENSITIVITY_END-aug13_old_cycle).days,
            'covers_capyear_target_by_days':(aug13_old_cycle-SCOPE_END).days,
            'not_an_actual_Simonovic_contract_claim':True,
            'new_proposal_sign_and_notice_date':'2021-09-02',
            'new_cycle_immediate_clock_model_end':fresh_min.isoformat(),
            'new_notice_does_not_automatically_delete_prior_notices':True},
        'foreign_admissibility':{
            'NBA_no_impediment_does_not_imply_free_to_sign_other_foreign_club':True,
            'required_parties':['player','correct original employer','any loaning/receiving club with legal rights','correct new employer','other legally relevant rights holders if any'],
            'full_foreign_validity_and_consents_are_proposal_conditions_not_historical_facts':True,
            'nonconstructible_input_example':'An unexpired exclusive foreign services obligation bars a new foreign signing and the required holder does not lawfully consent. That input is outside this new-signing proposal; no receipt/private-absence demand cures it.',
            'actual_nonconstructible_contract_reported':False,
            'quantifier':'For each admitted NBA clock Γ and a legally valid, consenting proposed foreign execution q satisfying the named X5d conditions, evaluate the NBA continuation consequence. Does not assert every imaginable foreign Γ permits q.'},
        'roster_cost':{'source_standard_roster':copy.deepcopy(prior['roster_and_cost']['source_working_standard_players']),
            'source_two_way_roster':copy.deepcopy(prior['roster_and_cost']['source_working_two_way_players']),
            'working_existing_standard_count':15,'working_existing_two_way_count':2,
            'new_Simonovic_NBA_UPC':False,'new_NBA_salary_or_buyout_usd':0,
            'scope':'No Simonovic NBA contract is executed; this preserves the existing SQ1 slots only. Other Chicago2021–22 roster changes remain separate inputs.',
            'foreign_pay_transfer_or_guarantee_zero_certified':False,'actual_roster_or_medical_certified':False},
        'remaining_named_conditions':[
            {'id':'FOREIGN_EXECUTION_ADMISSIBILITY','classification':'EXPLICIT_CANDIDATE_CONDITION_NOT_PRIVATE_CERTIFICATION_GATE',
             'needed':'Legally valid new foreign services with named required consents, plus genuine NBA negotiation and timely compliant tenders. If a specific admitted foreigninput forbids all consensual implementation, that branch lies outside this proposal; no actual refusal is reported.'},
            {'id':'POST_CAPYEAR_REOPENING','needed':'After2022June30 review new applicable calendar/contract events; no indefinite or exact future continuation is certified.'}],
        'summary':{'active_original_clock_cells':268,'Gamma_domain_classes':3,
            'active_cells_cover_capyear_from_original_clock_alone':sum(x['target_end_certified_from_old_clock_alone'] for x in active),
            'active_cells_needing_additional_period_relation':sum(not x['target_end_certified_from_old_clock_alone'] for x in active),
            'new_foreign_contract_candidates':1,'new_NBA_contracts':0,
            'positive_rule_continuation_proposal_prepared':True,
            'full_target_all_admitted_NBA_clock_Gamma_conditionally_supported':True,
            'full_target_all_Gamma_certified':False,
            'new_author_locks':0,'REGISTER_promotions':0,'macro3_complete':False},
        'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}


def validate(o):
    try:return [] if o==build() else ['Candidate terms/clock/source/authority differ from full reconstruction']
    except (AssertionError,KeyError,ValueError,TypeError,OSError) as e:return [str(e)]


def markdown(o):
    return f'''# Simonović 2021–22: 새 해외계약·권리기간의 유한 구현 후보

`{o['status']}`. 기존8/12 한정 수용을 유지합니다. 이후는 새 **fiction candidate**이며 actual 해외계약/법인승계/급여·서류·2021원NBA입단 복제가 아닙니다. wholemacro3/원장/작가잠금/원고0.

## 새 제안의 실제 조건

프로 playingclub은 **Mega Basket, Serbia 제안**; 법적 고용주는 기존 Γ의 올바른 당사자 또는 필요한 적법동의를 받은 새 Mega 법인입니다. Petrol/Cedevita/Mega를 같은 법인으로 읽지 않습니다. **2021-09-02→2022-08-13** 서비스 계약을 제안하며 보수F는 별도 생활비 수당보다 큰 프로 서비스 대가입니다. 정확 외국 통화/급여/이적·해제금과 합의는 null. NBA재원/신규NBA급여/이적료 지급은 선택하지 않습니다.

선수·원 고용주·임대 구단·새 고용주 및 실제 권리자가 필요한 해제/동의를 적법하게 하거나 제한이 이미 끝나야 합니다. **NBA에 가용함은 다른 해외구단에 서명할 자유와 동치가 아닙니다.** 이 조건을 충족하지 못하는 foreign Γ는 새계약 후보 밖이며 실제 그런 사적조건이 있었다고 주장하지 않습니다. 기존 계약을 무조건 연장하거나 강제 해제하지 않습니다.

진정한 Chicago 계약/역할/가용 협상 후 유효한1시즌 최소연봉 이상의 team-signed RequiredTender를 공급하되 선수 미수락·미철회·미renounce입니다. W21/B21/A21 및 필요하면W22는 적용되는 적법 기관창/마감 변수이며 실제2021 수정기한이나 접수를 날짜로 채우지 않습니다. NBA UPC가 실행되지 않아 기존 SQ1 표준15/TW2에서 Simonović를16번째 계약으로 만들지 않습니다. 실제 foreignfee0 인증과 구별합니다.

## 원문과 분기

2017CBA PDF305–306 **X5d**는 active one-year 동안 새NonNBA서명과 성실 NBA협상·유효Tender가 있으면5a에 따른 추가 one-year를 허용합니다. **정확 e+1 또는 signing+1이란 문구는 없으므로 그대로 확정하지 않습니다.** X5e 실패반례는 서명+성실협상+tender실패이며 새 후보는 적법Tender를 직접 조건에 넣습니다. X6 subject5/never-shorten, X4 철회·renounce 및 X5g 전달도 유지합니다. 원CBA9쪽+기존raw6를 직접재사용했습니다.

|Γ|구성/경계|
|---|---|
|이미 active 원1년|원268 시작일의 가장 이른끝은2021-11-18; 새Sept2서명은 모두 그 이전. 적법foreignq+협상+Tender가5d 추가기간을 지지하나 원notice를 지우지 않음. 추가기간의 보수적 하한은6/30창을 지지하며 정확 만료일은null.|
|시계미개시·이전 cycle의 pendingnotice 없음|새효력notice를Sept2이후로 선택. 즉시 가용이면Sept2, 장애가 계속되면 적법 종료 이후. 새로운cycle의 first immediate1년말단은2022Sept2로 캡year 끝2022Jun30보다 뒤.|
|이전 cycle의 pending/조건부notice|Sept1등에 실제효력을 갖게 되면 active로 연결. 계속장애면 자동가용/새foreign서명권한을 추론하지 않음. 이전draft기준을 보존하며 July1→Sept1 조건 충족이면5b의 적법기한 내Tender를 공급. 추가기간 하한으로6/30창을 검문.|

독립 반증에서 **Aug13 가용+2021–22 의사**는5a(ii)의2021Jul29 draft기준으로2022Jul29에 끝나 선택적8/12감도창보다14일 짧을 수 있음을 확인했습니다. 새서명/새notice를Sept2로 옮겨 해당 새cycle 반례를 피하지만 기존notice 자체를 삭제하는 수리는 아닙니다. 이는 실제 Simonović 행적 주장이 아닙니다.

새2022 NBA 날짜 다운로드1회는HTTP403(425B)이어서 원본문으로 계수하지 않았습니다. 새cycle의 draft가Sept1 이후라는 규칙 구조를 사용하며 그 응답으로 실제draft일을 인증하지 않습니다.

## 충분조건과 재개방

실제 검문 범위는 ArticleI1(nnn), PDF32/인쇄10의 **2021–22 SalaryCapYear 끝2022-06-30**입니다. NBA Season의 훈련캠프→Finals 정의와 구별합니다. 8/12는 별도 감도창이며 새 완료의무가 아닙니다.

5d의 **additional one-year**를 원말단 그대로 재표시하여 기간을 전혀 늘리지 않는 관계는 추가기간을 소거하므로 이 후보의 적법관계로 계수하지 않습니다. 원기간에 추가하는 구조의 최소말단은 원최소2021-11-18 뒤 추가1년의2022-11-18입니다. 새5a측정 구조는9/2 이후 유효기준으로2022-09-02 이후; 더 보수적으로 이전cycle의2021-07-29 draft기준을 남겨도2022-07-29입니다. 두 구조의 보수적 하한은 **2022-07-29**,6/30보다 **29일 뒤**입니다. 모든 상상가능 해석 포괄 인증이나 actual 정확 e+1/추가만료일 선택이 아닙니다.

268 active 시계 중 원말단만으로6/30을 넘는43셀은 직접 충분합니다. 나머지225셀은5d의 추가기간 관계를 사용합니다. 원notice이력을 삭제하지 않으며 July1까지 통지/September1 실제가용인 조건부 분기는 **September10 또는 적용되는 적법 수정 B21까지 유효Tender**를 공급하고 필요하면W22의 연간Tender도 공급합니다. 기관창/실접수일/actual 만료는null. 이 셀들은 실제268개계약/접수이력 인증이 아닙니다.

따라서 명시된 적법foreignq·성실협상·적법Tender조건을 충족하는 모든 인정된 NBA clock Γ에서6/30 창의 충분조건은true입니다. 실제 모든 외국계약/동의가 충족됐다는 인증과 fulltarget/allforeignΓ 실제인증은false입니다. 유효 foreignq가 불가능한 특정 입력은 이 새서명 후보 밖이며 비공개 전체 계약이나 receipt를 새 필수gate로 요구하지 않습니다.

수락된NBAUPC·Tender철회·권리renounce·새외국계약 실패·허용notice변경·6/30 이후 새캡year 및 target 이후는 다시 검문합니다. 무기한 rights/2022–23NBA입단/정확장기만료일을 자동 완성하지 않습니다.

|번호|묶음|상태|
|---|---|---|
|1|2020 draft연쇄|완료|
|2|Chicago2020–21|S2완료|
|3|2021–23 거래·계약|전체비용·#16 비교·Simonović continuation후보 검문|
|4|장기커리어|후속설계|
|5|결말·전체구조|전체기능표 미완료|
|6|집필규격·Context Pack|누적21 국소기능/Pack0|
|7|통합·독립·작가승인|final CLOSED|

미완료큰묶음5; 원고 CLOSED.
'''


def self_test(o):
    result=[]
    for label,change in [
        ('automatic_foreign_entity',lambda x:x['candidate_written_terms'].update(Petrol_Cedevita_Mega_entities_automatically_equated=True)),
        ('actual_foreign_fee_zero',lambda x:x['roster_cost'].update(foreign_pay_transfer_or_guarantee_zero_certified=True)),
        ('drop_prior_notice',lambda x:x['candidate_written_terms'].update(prior_pending_availability_notices='Discard')),
        ('full_target_unproved',lambda x:x['summary'].update(full_target_all_Gamma_certified=True)),
        ('new_NBA_UPC',lambda x:x['roster_cost'].update(new_Simonovic_NBA_UPC=True)),
        ('replace_additional_with_eplus1',lambda x:x['Gamma_domains'][0]['cells'][0].update(exact_additional_period_start_or_end='2022-11-18'))]:
        bad=copy.deepcopy(o);change(bad);assert validate(bad),label;result.append(label)
    for label,change in [
        ('constructor_aug13_notice',lambda x:x['fresh_effective_availability_notice'].update(no_new_effective_notice_before='2021-08-13')),
        ('constructor_pending_tender_failure',lambda x:x['valid_annual_RequiredTender']['pending_July1_notice_and_September1_actual_availability_branch'].update(timely_5b_tender_supplied=False)),
        ('constructor_drop2022_tender',lambda x:x['valid_annual_RequiredTender'].update(if_a_2022_annual_tender_is_due_before_scope_end=None)),
        ('constructor_no_tender',lambda x:x['valid_annual_RequiredTender'].update(team_signed=False))]:
        bad=proposal();change(bad)
        with patch(__name__+'.proposal',return_value=bad):
            try:build()
            except AssertionError:result.append(label)
            else:raise AssertionError(label)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();o=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
    if a.check:assert not validate(load(OUT));assert text(MD)==markdown(o)
    tests=self_test(o) if a.self_test else []
    print(json.dumps({'current':True,'active_cells':268,'Gamma_domains':3,'negative_controls':tests,'full_target_all_Gamma_certified':False,'REGISTER_promotions':0}))
