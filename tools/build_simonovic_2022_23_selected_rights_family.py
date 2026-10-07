"""Select one preserved no-clock family; do not rerun or certify all 268 clocks."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from datetime import date
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_simonovic_2022_23_selected_rights_family.py'
OUT = 'research/SIMONOVIC_2022_23_SELECTED_RIGHTS_FAMILY_2026_10_07.json'
MD = OUT.replace('.json', '.md')
PRIOR = 'research/SIMONOVIC_2021_22_RIGHTS_CONTINUATION_2026_10_07.json'
BOUNDARY = 'research/SIMONOVIC_2022_23_RIGHTS_CALENDAR_BOUNDARY_2026_10_07.json'
RT = 'research/CHICAGO_2022_SECOND_TENDER_COST_REFINEMENT_2026_10_07.json'
CORE = 'simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json'
PINS = {
 PRIOR: '605e23f01c818b63a1782246824738c253591fd056bd8b66790c3409036a9937',
 BOUNDARY: '0c3946ac8cea8fd85bcf7d1a87bace9e52538611d67983a9a70b36ba77c4df66',
 RT: 'e82cf0a2a7f73eb4dd6ff90e75ee5b3c729b8c2ff000a4b667f901a728acd0ca',
 CORE: 'e7d0f4b15bc06c7cd16a38d158b38a78871fb7372d412639e33bb20c31d225a7',
}
BRANCH = 'G_NO_CLOCK_NO_PENDING_OLD_CYCLE_NOTICE'
SIGN = date(2021, 9, 2)
SERVICE_END = date(2022, 8, 13)
NOTICE = date(2022, 8, 14)
TARGET = date(2023, 6, 30)

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n').encode()).hexdigest()

def read(root, relative):
    return json.loads((root / relative).read_text(encoding='utf-8-sig'))

def selected_policy():
    return {
      'Gamma_subfamily': BRANCH,
      'prior_effective_5a_i_notice_exists_in_selected_model': False,
      'prior_or_pending_5a_ii_notice_exists_in_selected_model': False,
      'by_July1_2022_5b_notice_issued_in_selected_model': False,
      'actual_past_notice_absence_certified': False,
      'given_notice_deleted_or_replaced': False,
      'foreign_signing': '2021-09-02',
      'foreign_service_end': '2022-08-13',
      'lawful_NBA_impediment_preserved_until': '2022-08-13',
      'lawful_release_of_all_NBA_impediments': '2022-08-14',
      'first_effective_immediate_5a_i_notice': '2022-08-14',
      'future_season_intention_5a_ii_notice_added': False,
      'new_2022_NonNBA_signing_or_extension': False,
      'additional_period_e_plus_one_selected': False,
      'professional_service_pay': 'F > separately identified living-expense stipend; F > 0',
      'legal_employer': 'The correct admitted employer, or a duly substituted entity under every legally necessary consent; Mega is proposed playing organization only.',
      'all_required_foreign_consents_and_validity': 'Explicit admitted lawful fiction: player, correct employer, all relevant lenders/loaning/receiving clubs and other rights holders agree to necessary services/release. No entity identity or foreign signing freedom inferred from NBA availability.',
      'NBA_funded_service_or_release_payment': False,
      'actual_foreign_fee_zero_certified': False,
      'bona_fide_CHI_negotiation': 'Preserve genuine review of minimum NBA terms and role; voluntarily do not accept; no forced refusal or sham tender.',
      '2020_and_2021_tenders': 'Preserve prior operative W20/W21/B21/A21 lawful team-signed, timely, minimum-or-greater offers and applicable X6 conditions through natural2021 SubsequentDraft. Do not invent original modified dates.',
      '2022_offer': {
        'delivery_date': '2022-08-25',
        'classification': 'VOLUNTARY_CONFORMING_REQUIRED_TENDER_FORM_OFFER_NOT_AN_AUTOMATIC_ANNUAL_X4_DEADLINE',
        'team_signed': True,
        'one_Season': '2022-23',
        'salary': 'Applicable II6 statutory Minimum Annual Salary for an exclusive Draft Rookie, zero new bonus proposal; exact private cents unselected.',
        'delivery': 'Personal delivery to player or authorized representative',
        'acceptance_open_through_at_least': '2022-10-15',
        'player_accepted': False,
        'withdrawal': False,
        'exclusive_rights_renunciation': False,
        'actual_delivery_or_nonacceptance_certified': False,
      },
      'notice_delivery': 'Written personal delivery to Chicago principal office attention General Manager and NBA League Office attention General Counsel under X5(g).',
      'NBA_UPC_accepted_through_2023_June30': False,
      'new_professional_team_contract_after_2022_Aug14_through_target': False,
      'actual_foreign_law_or_institutional_acceptance_certified': False,
      'new_author_lock': False,
    }

FIXED_POLICY = copy.deepcopy(selected_policy())

def assert_policy(p):
    require(p == FIXED_POLICY, 'Returned selected notice/foreign/tender policy changed')
    require(p['Gamma_subfamily'] == BRANCH and not p['given_notice_deleted_or_replaced'], 'Wrong Gamma or deleted original notice')
    require(not p['prior_effective_5a_i_notice_exists_in_selected_model'] and not p['prior_or_pending_5a_ii_notice_exists_in_selected_model'], 'Selected no-clock branch has earlier notice')
    require(p['first_effective_immediate_5a_i_notice'] == NOTICE.isoformat() and p['lawful_release_of_all_NBA_impediments'] == NOTICE.isoformat(), 'Availability/date binding changed')
    require(not p['by_July1_2022_5b_notice_issued_in_selected_model'] and not p['future_season_intention_5a_ii_notice_added'], 'Earlier conditional/Draft basis added')
    require(not p['actual_past_notice_absence_certified'] and not p['actual_foreign_law_or_institutional_acceptance_certified'], 'Actual private absence or foreign law certified')
    offer = p['2022_offer']
    require(offer['team_signed'] and not offer['player_accepted'] and not offer['withdrawal'] and not offer['exclusive_rights_renunciation'], 'Tender failure/acceptance changes exclusive family')
    require(date.fromisoformat(offer['delivery_date']) >= NOTICE and date.fromisoformat(offer['acceptance_open_through_at_least']) >= date(2022, 10, 15), 'Offer delivery/acceptance window changed')

def build(root=ROOT):
    for f, expected in PINS.items():
        require(sha(root / f) == expected, 'Source changed: ' + f)
    d = {f: read(root, f) for f in PINS}
    for f, value in d.items():
        require(value == json.loads((root / f).read_text(encoding='utf-8-sig')), 'Loaded source differs from physical file: ' + f)
    prior, boundary, core = d[PRIOR], d[BOUNDARY], d[CORE]
    source_branch = next(g for g in prior['Gamma_domains'] if g['id'] == BRANCH)
    require(source_branch['whole_target_under_these_conditions_supported'] is True, 'Original possible no-clock family missing')
    require(prior['candidate_written_terms']['new_service_term'] == [SIGN.isoformat(), SERVICE_END.isoformat()], 'Preserved service proposal changed')
    require(prior['candidate_written_terms']['fresh_effective_availability_notice']['no_new_effective_notice_before'] == SIGN.isoformat(), 'Prior notice lower boundary changed')
    require(boundary['identity']['birth_year'] == 1999 and boundary['identity']['pick'] == 44 and boundary['identity']['prior_holder'] == 'CHI', 'Wrong player/right identity')
    require(boundary['single_remaining_condition']['id'] == 'PERIOD_TO_2023_JUNE30', 'Boundary condition changed')
    require(len(prior['Gamma_domains'][0]['cells']) == 268, 'Frozen source domain count changed')
    policy = selected_policy()
    assert_policy(policy)
    # Read rules only, not any ancestor builder or 268-state constructor.
    law = prior['primary_transition_rule']
    raw = Path(law['cache_path']).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == law['raw_sha256'], 'CBA raw changed')
    pdf = fitz.open(stream=raw, filetype='pdf')
    pages = []
    for n in (30, 32, 303, 304, 305, 306, 307):
        txt = pdf[n-1].get_text().replace('\r\n', '\n').replace('\r', '\n')
        pages.append({'PDF_1based': n, 'text_sha256': hashlib.sha256(txt.encode()).hexdigest()})
    a = ' '.join(pdf[304].get_text().split())
    require('earlier of the following two dates' in ' '.join(pdf[303].get_text().split()) and 'available to sign a Player Contract' in a, 'X5a rule unavailable')
    require('additional one-year periods as measured in and' in a, 'X5d boundary unavailable')
    require('by July 1 of any year' in a and 'by September 10 of such year' in a, 'X5b conditional deadline unavailable')
    expiry = NOTICE.replace(year=NOTICE.year + 1)
    require(SIGN < SERVICE_END < NOTICE < TARGET < expiry and (expiry - TARGET).days == 45, 'Direct one-year calculation changed')
    ports = core['unsigned_ports']
    sim = next(x for x in ports if x['port'] == 'SIMONOVIC2020_SECOND')
    require((sim['NBA_UPC'], sim['slot_consumption'], sim['normal_reservation'], sim['apron_conservative_reservation']) == (False, 0, 1018000, 1837000), 'Reserved unregistered port changed')
    require(core['summary']['standard'] == 15 and core['summary']['two_way'] == 2, 'Core slot count changed')
    return {
      'id': 'SIMONOVIC_2022_23_SELECTED_RIGHTS_FAMILY',
      'baseline_main': 'a87d94c',
      'status': 'ROOT_SELECTED_ROUTINE_NO_CLOCK_SUBFAMILY_DIRECT_X5A_TARGET_SUPPORTED_REVIEW_PENDING',
      'source_hash_method': 'UTF8_BOM_STRIPPED_LF_SHA256',
      'source_sha256': {**PINS, SELF: sha(root / SELF)},
      'selected_Gamma_source': {'file': PRIOR, 'pointer': '/Gamma_domains/1', 'id': BRANCH, 'source_record': copy.deepcopy(source_branch)},
      'selected_policy': policy,
      'authority': {'root_routine_family_selected': True, 'selection_basis': 'Explicit existing orchestration instruction chooses a possible no-clock subfamily and lawful existing2021 foreign proposal; not a health-delegation price approval.', 'old_given_Gamma_notice_erased': False, 'all268_families_promoted': False, 'new_author_lock': False},
      'primary_law': {'url': law['url'], 'cache_path': law['cache_path'], 'raw_sha256': law['raw_sha256'], 'pages': pages, 'rule': 'X5(a)(i) effective immediate availability; X5(a)(ii) no notice issued in selected fiction; X5(b) by-July1 trigger false in selected fiction; I1(ddd) offer form; X4(f)/(g), X5(f)/(g), X6 subject5.'},
      'timeline': [
        {'date': '2020-11-18', 'event': 'PRESERVE_CHI44_INITIAL_RIGHT_AND_OPERATIVE_VALID_TENDER', 'actual_receipt': None},
        {'date': '2021-07-29', 'event': 'PRESERVE_NATURAL_SUBSEQUENT_X6_SUBJECT_TO_X5_NO_REENTRY', 'redrafted': False},
        {'date': SIGN.isoformat(), 'event': 'SELECT_EXISTING_LAWFUL_NONNBA_SERVICE_AND_GENUINE_CHI_NEGOTIATION_PROPOSAL', 'service_end': SERVICE_END.isoformat(), 'correct_employer_and_required_consents_admitted': True, 'actual_institutional_acceptance': None},
        {'date': '2022-07-07', 'event': 'PRESERVE_SELECTED_CORE_UNREGISTERED_PORT', 'STD': 15, 'TW': 2, 'new_NBA_UPC': False},
        {'date': NOTICE.isoformat(), 'event': 'LAWFUL_IMPEDIMENT_RELEASE_AND_FIRST_EFFECTIVE_IMMEDIATE_NOTICE', 'notice_type': 'X5a_i', 'notice_type_ii_issued': False, 'actual_receipt': None},
        {'date': '2022-08-25', 'event': 'VOLUNTARY_TEAM_SIGNED_ONE_SEASON_MINIMUM_OFFER', 'accepted': False, 'acceptance_open_through_at_least': '2022-10-15', 'period_extension_created_by_tender_alone': False},
        {'date': TARGET.isoformat(), 'event': 'STOP_BOUNDED_SELECTED_RIGHTS_COVERAGE_NO_UPC_ACCEPTANCE'},
      ],
      'period_witness': {'basis': 'FIRST_EFFECTIVE_X5a_i_NOTICE', 'basis_date': NOTICE.isoformat(), 'no_effective_ii_notice_in_selected_family': True, 'one_year_end_in_selected_fiction': expiry.isoformat(), 'target_start': '2022-07-01', 'target_end': TARGET.isoformat(), 'margin_days': 45, 'selected_subfamily_full_target_supported': True, 'actual_contract_or_rights_expiry_certified': False, 'X5d_e_plus_one_or_new_2022_signing_used': False, 'tender_alone_extends_period': False},
      'tender_legal_boundary': {'X5b_September10_deadline_triggered_in_selected_family': False, 'reason': 'No by-July1 conditional notice was issued in this admitted fiction. This is not an actual past absence certificate.', 'X4_two_week_window_automatically_reapplied_in2022': False, 'offer_timing': 'Aug25 is after effectiveavailability and also lies in the ordinary Aug22–Sep5 second-round form window; that numerical overlap is not a claim that X4 requires an annual2022 tender. The conforming voluntary offer does not create the retained period.', 'offer_salary_function': policy['2022_offer']['salary'], 'cash_not_chosen_as_zero': True, 'acceptance_or_withdrawal_or_renunciation_reopens': True},
      'roster_and_cost': {'standard_preserved': 15, 'two_way_preserved': 2, 'new_NBA_UPC_or_registration': False, 'unsigned_port_normal_reservation': 1018000, 'unsigned_port_apron_overreserve': 1837000, 'reservation_scope': 'Preserve existing exclusiveDraftRookie minimum proposal bounds and wider possibleRookieFA apron overscreen. Unaccepted offer is not asserted a signed salary or a slot.', 'NBA_funded_foreign_service_or_release_selected': False, 'actual_foreign_cash_zero_certified': False, 'future_accepted_contract_cannot_create_STD16_without_new_named_slot_action': True},
      'unselected_other_domain_boundary': {'active_source_cells': 268, 'active_source_cells_reexecuted': 0, 'all268_FY23_PASS': False, 'preserved_notice_histories': 'Existing active/pending given-Gamma branches remain in frozen source, not edited or silently relabeled. Selecting another branch would require its own period proof.', 'B_all_preserved_Gamma_X5d_route': 'Not closed: a2022 June23 Draft basis can giveJune23,2023, seven days short. No exact additional measurement or foreignagreement is invented to erase that input.'},
      'reopen_after_scope': ['X5f consequence at selected one-year end; no forever retention or2023-24 inheritance.', 'Any earlier or type-ii notice, accepted NBA offer, waiver/withdrawal/renounce, another professional signing, or changed foreign legal impediment requires fresh source-bound evaluation.', 'PostJune30,2023 applicable CBA/calendar and any new NBA/foreign contract; not automatically certified by this leaf.'],
      'independent_review_completed': False,
      'whole_actual_foreign_law_or_private_consents_certified': False,
      'whole_macro3_or_season_complete': False,
      'central_or_REGISTER_changed': False,
      'freeze': 'v0.30 PARTIAL', 'design_gate': 'CLOSED', 'manuscript_allowed': False,
    }

def validate(value, root=ROOT):
    try:
        require(value == build(root), 'Saved selected family differs from source-bound construction')
        return []
    except (ValueError, KeyError, StopIteration, OSError) as e:
        return [str(e)]

def markdown(v):
    return '\n'.join([
      '# Simonović 2022–23: 선택한 no-clock 권리 가족', '',
      '**Root 루틴 작업 선택·X5a 직접 기간 지원 / 독립 검문 대기.** 원권리 CHI2020#44·1999년생 선수를 유지한다. 실제 소속·외국법/급여·기관 수락·임상·사적 통지 부재는 인증하지 않는다.', '',
      '## 선택한 입력과 직접 기간', '',
      f"기존 [2021 후보]({PRIOR.split('/')[-1]})의 `{BRANCH}`를 선택했다. 268개 active 원시계와 다른 pending 통지는 변경하지 않았다. 선택한 하위가족은 과거 유효 즉시/다음시즌 통지가 없는 명시적 가상 입력이다. 실제 과거 통지가 없었다는 주장이 아니다.", '',
      '기존 2021-09-02→2022-08-13 서비스 제안을 적법한 실행 모델로 채택한다. 올바른 고용주 및 필요한 모든 원권리자·임대 당사자와 선수의 적법 동의를 조건으로 NBA 계약/플레이 장애를 서비스 끝까지 유지하고, 8월14일 모두 해소한다. Mega playing organization과 법적 고용주를 자동 동일시하지 않는다. 보수 F는 별도 생활비 수당보다 큰 양수 프로 서비스 대가이고 외국 당사자가 법적 비용을 부담한다. 정확 급여/해제금은 미선택이며 NBA 재원 지급도 선택하지 않았다.', '',
      '2022-08-14 Chicago GM과 NBA League Office에 X5g의 유효 서면 즉시 가용 통지를 전달한다. 다음시즌 의사통지(ii)는 이 하위가족에서 발행하지 않는다. 따라서 X5a의 두 기준 중 유일한 유효 기준은 (i) 8월14일이며 그 1년 끝은 **2023-08-14**다. 목표 2023-06-30보다 **45일 뒤**다. 기존 no-clock 기간부터 이 첫 유효 통지 뒤까지 연속되며 새2022 해외연장, 원끝+1년, X5d 추가말단을 만들 필요가 없다.', '',
      '## Offer와 실제 급여·슬롯', '',
      '기존 W20/W21/B21/A21의 적법 offer와 자연2021 SubsequentDraft까지의 X6 조건을 유지한다. 성실 Chicago 협상 뒤 2022-08-25 team-signed 2022–23 한 시즌·법정 minimum 이상·개인전달·최소10월15일까지 수락 가능한 제안을 제공하고 선수는 수락하지 않는다. 당시 법정 minimum 함수와 기존 보수 상한을 사용하며 정확 현금0이나 실제 제출 사실로 표시하지 않는다.', '',
      '이 선택 입력에는 July1까지의 X5b 조건부 통지가 없으므로 September10 의무를 자동 추가하지 않는다. Aug25의 통상 Aug22–Sep5 형식창 내 위치는 날짜 비교일 뿐 X4의 Initial/Subsequent 의무를 매년 되살리는 법규가 아니다. 자발적인 동일 RequiredTender 형식 제안은 권리기간을 만들어내는 원인이 아니다. 수락·철회·renounce와 새 통지는 해당 시점에 재개방한다.', '',
      f"[선택 코어]({'../simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json'})의 15STD/2TW·미서명 Simonović 포트와 normal1,018,000/apron1,837,000 예약을 보존한다. 미수락 제안을 signed salary/STD16으로 만들지 않는다. 2023–24·무기한 독점·실제 만료는 인증하지 않는다.", '',
      '## 적용하지 않은 분기와 검문', '',
      '[기존 FY23 연표 경계](SIMONOVIC_2022_23_RIGHTS_CALENDAR_BOUNDARY_2026_10_07.md)의 PERIOD_TO_2023_JUNE30은 **선택한 하위가족에 한해** 직접 지원한다. 기존 268 전체 PASS는0이다. 보존된2022Draft(ii) 기준의2023-06-23→6/30 7일 차이는 다른 입력의 경계로 남으며 통지 소거나 허구 X5d 측정으로 제거하지 않는다.', '',
      '2017CBA I1ddd(PDF30), X4/5/6/7(PDF303–307), capyear(PDF32)의 원PDF SHA와 쪽 지문을 직접 연결했다. 원268/조상 생성기 재실행0·새수집0. `--check --self-test`는 current source/정책 반환 검문이며 독립 감리로 계산하지 않는다.', '',
      '| 번호 | 작업 | 상태 |', '|---|---|---|',
      '|1|2020 draft|완료|', '|2|Chicago2020–21|S2 실행 완료|',
      '|3|2021–23 거래·계약|선택 권리 하위가족 지원·두시즌 후속 진행|',
      '|4|장기 커리어|후속 실행 미완료|', '|5|전체 구조|전체G13 미완료|',
      '|6|규격·Pack|S1 완료·실제Pack0|', '|7|통합·독립·작가 승인|전체 미완료|', '',
      '미완료5묶음·[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)·v0.30 PARTIAL·설계/원고 CLOSED·원고0.', '',
    ])

def self_test():
    original = selected_policy
    tests = []
    for name, change in (
      ('earlier_type_ii_notice', lambda x: x.update(prior_or_pending_5a_ii_notice_exists_in_selected_model=True)),
      ('actual_past_absence', lambda x: x.update(actual_past_notice_absence_certified=True)),
      ('accepted_tender_slot', lambda x: x['2022_offer'].update(player_accepted=True)),
    ):
        bad = original()
        change(bad)
        globals()['selected_policy'] = lambda bad=bad: copy.deepcopy(bad)
        try:
            build()
        except ValueError:
            tests.append(name)
        else:
            raise AssertionError('False pass: ' + name)
        finally:
            globals()['selected_policy'] = original
    return tests

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--write', action='store_true'); p.add_argument('--check', action='store_true'); p.add_argument('--self-test', action='store_true')
    a = p.parse_args(); b = build()
    if a.write:
        (ROOT / OUT).write_text(json.dumps(b, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MD).write_text(markdown(b), encoding='utf-8')
    if a.check:
        require(not validate(read(ROOT, OUT)), 'Saved JSON not current')
        require((ROOT / MD).read_text(encoding='utf-8') == markdown(b), 'MD not current')
    print(json.dumps({'selected_branch': BRANCH, 'margin_days': 45, 'all268_PASS': False, 'writer_negative_controls': self_test() if a.self_test else []}))
