"""Existing CX1-4 consensual legal-form candidates, never an author selection."""
import argparse
import copy
import hashlib
import json
from datetime import date, datetime
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

import fitz
from bs4 import BeautifulSoup
import build_chicago_2022_23_approved_core_contract_execution as core

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_carter_2021_extension_candidate_family.py'
OUT = 'research/CARTER_2021_EXTENSION_CANDIDATE_FAMILY_2026_10_07.json'
MD = OUT[:-5] + '.md'
CBA = core.CBA
CBA_SHA = '66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
PINS = {
    'simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE_INPUTS.json': '4b66d96a274fa4d31e41f6256192449e8b43a6dfc00e8f4e44f4cbd76e83bf78',
    'simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json': '7d3ab9d0d9e4234e728d4549616acaf84d5b57c4110603cf0114c8bf2c55b8d4',
    'research/CHICAGO_2021_23_CONTINUATION_SOURCES.json': '4dc3cfb7416174c0fea5c2710e9915a729d362dc553f216f4e9c861b373e9db3',
    'research/CHICAGO_2022_23_APPROVED_CORE_CONTRACT_EXECUTION_2026_10_07.json': '2cc7aeaeaef530f1c3fac5846348792c3d516eb1479af1ce56617deb2e7cb2b5',
    'research/NBA_2021_PICK16_BOS_OKC_HOU_WORKING_EXECUTION_2026_10_07.json': '86b9989daa20eced72106c25b14fb8d8b3b32d201132a0b87ba466b0ce51fba0',
    'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json': '253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088',
    'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json': '9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce',
    'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2',
}
SCHEDULES = {
    'CX1': [14150000, 13050000, 11950000, 10850000],
    'CX2': [11320000, 10440000, 9560000, 8680000],
    'CX3': [16980000, 15660000, 14340000, 13020000],
}
RAW = [
    {'id': 'NBA_CARTER_EXTENSION', 'url': 'https://www.nba.com/news/orlando-magic-sign-wendell-carter-jr-to-contract-extension', 'http_status': 200, 'cache_path': 'C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-carter-extension-20261007/NBA_CARTER_EXTENSION.html', 'bytes': 315687, 'raw_sha256': '531d0338a78ef7f94e7829fa3632aeb0a97316da1bfc5db05749899ac039b172'},
    {'id': 'NBA_2021_SCHEDULE', 'url': 'https://pr.nba.com/2021-22-nba-schedule-75th-anniversary-season/', 'http_status': 200, 'cache_path': 'C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-carter-extension-20261007/NBA_2021_SCHEDULE.html', 'bytes': 118458, 'raw_sha256': 'f98bca221e1f30ed6d936e172dc316610e05e8c94e8f852ea32918f74e80174b'},
]


def text(p):
    return (ROOT / p).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def sha(p):
    return hashlib.sha256(text(p).encode()).hexdigest()


def load(p):
    return json.loads(text(p))


def ratio(q):
    return {'numerator': q.numerator, 'denominator': q.denominator}


def terms():
    return {
        'candidate_execution_ET': '2021-10-15T12:00:00',
        'original_2021_22_regular_salary': 6920027,
        'second_rookie_option_exercised': True,
        'full_Bird_eligibility_at_original_expiry_preserved': True,
        'original_term_expiry': '2022-06-30',
        'extension_new_term': ['2022-07-01', '2026-06-30'],
        'schedules': copy.deepcopy(SCHEDULES),
        'extension_protection': 'FULL_LACK_OF_SKILL_AND_INJURY_OR_ILLNESS_UNDER_STANDARD_CBA_CONDITIONS',
        'extension_options': [],
        'extension_ETO': False,
        'new_signing_performance_promotional_loan_or_buyout_additions': 0,
        'new_trade_bonus_percentage': 0,
        'existing_original_bonus_clause_if_any': 'PRESERVE_ORIGINAL_TERM; IF_UNEARNED_BONUS_EXISTS_USE_XXIV2a5_REPLACEMENT_EX4_EXCLUDING_EXTENDED_TERM_ONLY',
        'original_trade_bonus_actual_percentage': None,
        'trade_agreement_condition_on_extension': False,
        'modeled_mutual_consent_required_if_candidate_chosen': True,
        'actual_team_or_player_consent': None,
        'author_selected_CX': None,
        'historical_ORL_agreement_inherited': False,
    }


def assert_terms(t):
    # Independent literal expectations; comparing to a patched constructor is insufficient.
    assert t['candidate_execution_ET'] == '2021-10-15T12:00:00'
    assert t['original_2021_22_regular_salary'] == 6920027
    assert t['second_rookie_option_exercised'] is True
    assert t['full_Bird_eligibility_at_original_expiry_preserved'] is True
    assert t['original_term_expiry'] == '2022-06-30'
    assert t['extension_new_term'] == ['2022-07-01', '2026-06-30']
    assert t['schedules'] == {
        'CX1': [14150000, 13050000, 11950000, 10850000],
        'CX2': [11320000, 10440000, 9560000, 8680000],
        'CX3': [16980000, 15660000, 14340000, 13020000],
    }
    assert t['extension_protection'] == 'FULL_LACK_OF_SKILL_AND_INJURY_OR_ILLNESS_UNDER_STANDARD_CBA_CONDITIONS'
    assert t['extension_options'] == [] and t['extension_ETO'] is False
    assert t['new_signing_performance_promotional_loan_or_buyout_additions'] == 0
    assert t['new_trade_bonus_percentage'] == 0
    assert t['existing_original_bonus_clause_if_any'] == 'PRESERVE_ORIGINAL_TERM; IF_UNEARNED_BONUS_EXISTS_USE_XXIV2a5_REPLACEMENT_EX4_EXCLUDING_EXTENDED_TERM_ONLY'
    assert t['original_trade_bonus_actual_percentage'] is None
    assert t['trade_agreement_condition_on_extension'] is False
    assert t['modeled_mutual_consent_required_if_candidate_chosen'] is True
    assert t['actual_team_or_player_consent'] is None and t['author_selected_CX'] is None
    assert t['historical_ORL_agreement_inherited'] is False
    when = datetime.fromisoformat(t['candidate_execution_ET'])
    assert datetime(2021, 8, 6, 12, 1) <= when <= datetime(2021, 10, 18, 18)


def source_inputs():
    for p, pin in PINS.items():
        assert sha(p) == pin, 'Unreviewed source ' + p
    old = load(core.OUT)
    assert not core.validate(old), 'Approved core producer changed'
    assert next(x for x in old['expired_or_unselected_new_contract_inputs'] if x['player'] == 'Wendell Carter Jr.')['new2022_route_selected'] is False
    a = load('simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE_INPUTS.json')['Carter_options']
    b = load('simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json')['Carter_options']
    assert [x['id'] for x in a] == ['CX1', 'CX2', 'CX3', 'CX4']
    assert [x['salary_2022_to_2026'] for x in a] == [SCHEDULES['CX1'], SCHEDULES['CX2'], SCHEDULES['CX3'], None]
    assert [x['salary_2022_to_2026'] for x in b] == [SCHEDULES['CX1'], SCHEDULES['CX2'], SCHEDULES['CX3'], None]
    assert all(x['contract_agreed'] is False for x in b)
    assert a[0]['recommended'] is True
    assert load('simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json')['selected_Carter_contract'] is None
    raw = []
    for x in RAW:
        bb = Path(x['cache_path']).read_bytes()
        assert hashlib.sha256(bb).hexdigest() == x['raw_sha256'] and len(bb) == x['bytes']
        s = BeautifulSoup(bb, 'html.parser')
        for z in s(['script', 'style']):
            z.decompose()
        plain = ' '.join(s.get_text(' ', strip=True).split())
        if x['id'] == 'NBA_CARTER_EXTENSION':
            assert 'Per team policy, terms of the deal are not disclosed' in plain
            assert 'October 16, 2021' in plain
            observation = {'classification': 'PRIMARY_ORIGINAL_RELEASE_EVENT_ONLY', 'event_date': '2021-10-16', 'fact_paraphrase': 'Orlando announced Carter’s extension; team policy withheld terms.', 'reported_money_not_direct_club_disclosure': True, 'alternate_world_acceptance_inherited': False}
        else:
            assert 'Tuesday, Oct. 19, 2021' in plain
            observation = {'classification': 'PRIMARY_NBA_CALENDAR', 'published_date': '2021-08-20', 'first_regular_season_date': '2021-10-19', 'CBA_day_before_deadline': '2021-10-18T18:00:00_ET'}
        y = copy.deepcopy(x)
        y['observation'] = observation
        raw.append(y)
    calendar = next(x for x in load('research/NBA_2021_PICK16_BOS_OKC_HOU_WORKING_EXECUTION_2026_10_07.json')['raw_sources'] if x['id'] == 'CALENDAR_CAP')
    bb = Path(calendar['cache_path']).read_bytes()
    assert hashlib.sha256(bb).hexdigest() == calendar['raw_sha256'] and len(bb) == calendar['bytes']
    s = BeautifulSoup(bb, 'html.parser')
    for z in s(['script', 'style']):
        z.decompose()
    assert 'ends at noon ET on Friday, August 6' in ' '.join(s.get_text(' ', strip=True).split())
    y = copy.deepcopy(calendar)
    y['scope'] = 'REUSED_PRIMARY_2021_MORATORIUM_NOON_AUG6; CBA_ROOKIE_EXTENSION_WINDOW_START_IS12_01PM'
    raw.append(y)
    # Reuse the original public four-year rookie row, not the later ORL extension.
    oldcost = load('research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json')
    vendor = next(x for x in oldcost['raw_body_observations'] if x['id'] == 'wendell-carterjr_2021_ROW')
    bb = Path(vendor['cache_path']).read_bytes()
    assert hashlib.sha256(bb).hexdigest() == vendor['raw_sha256']
    plain = ' '.join(BeautifulSoup(bb, 'html.parser').get_text(' ', strip=True).split())
    assert '$6,920,027' in plain and '2021-22' in plain
    v = copy.deepcopy(vendor)
    v['scope'] = 'REUSED_VENDOR_ORIGINAL_ROOKIE_2021_22_6920027_ROW_ONLY; ORL_EXTENDED_TERM_AND_ACCEPTANCE_NOT_COPIED'
    raw.append(v)
    return a, raw


def rules():
    bb = CBA.read_bytes()
    assert hashlib.sha256(bb).hexdigest() == CBA_SHA
    d = fitz.open(stream=bb, filetype='pdf')
    ns = [38, 40, 44, 55, 60, 219, 245, 246, 247, 248, 255, 256, 299, 398, 399, 400]
    pages = []
    for n in ns:
        tx = d[n - 1].get_text().replace('\r\n', '\n').replace('\r', '\n')
        pages.append({'PDF_1based': n, 'printed': n - 22, 'fitz_text_LF_sha256': hashlib.sha256(tx.encode()).hexdigest()})
    def has(n, token):
        assert token in ' '.join(d[n - 1].get_text().split()), (n, token)
    has(245, 'Rookie Scale Extensions')
    has(246, 'prior to the first day of the Regular Season')
    has(219, 'eight percent (8%)')
    has(299, 'five (5) Seasons')
    has(255, 'Section 7(a) above')
    has(256, 'average of the aggregate Salaries')
    has(398, 'fifteen percent (15%)')
    has(399, 'not be applicable with respect to the extended term')
    has(248, 'six (6) months from the date of the trade')
    return {'url': 'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf', 'cache_path': str(CBA), 'raw_sha256': CBA_SHA, 'pages': pages,
            'scope': '2017 CBA applicable2021 extension execution; future changed CBA administration not independently certified.',
            'positive_clauses': {'eligibility_window': 'VII7b PDF245–246', 'annual_decrease': 'VII5c3 PDF219', 'term': 'IX1 PDF299', 'minimum_and_maximum': 'II6/7 PDF55/60', 'protection': 'II3g/4 PDF40/44', 'existing_bonus_preservation': 'XXIV2a PDF398–400', 'poison_pill': 'VII8g PDF256', 'six_month_general_extension_scope': 'VII8f PDF255 applies7a, not7b', 'consensual_bonus_waiver_successor_floor': 'VII7d3 PDF248; later oftrade+6months/otherwise-eligible'}}


def build():
    options, raw = source_inputs()
    t = terms()
    assert_terms(t)
    ev = rules()
    result = []
    for id, schedule in t['schedules'].items():
        total = sum(schedule)
        assert total == {'CX1': 50000000, 'CX2': 40000000, 'CX3': 60000000}[id]
        allowed = Fraction(schedule[0] * 8, 100)
        changes = [schedule[i + 1] - schedule[i] for i in range(3)]
        assert all(abs(x) <= allowed for x in changes)
        assert schedule[0] < Fraction(123655000, 4)
        assert len(schedule) + 1 == 5
        # Creation checks use known2022 max; later mandatory minimum/max terms remain statutory.
        assert min(schedule) > 2641691  # conservative2021 maximum-YOS minimum, not a2026 minimum certificate
        incoming = Fraction(t['original_2021_22_regular_salary'] + total, 5)
        result.append({'id': id, 'classification': 'UNSELECTED_EXISTING_DIRECTION_CONSENSUAL_IMPLEMENTATION_CANDIDATE',
                       'existing_recommendation': id == 'CX1', 'author_locked': False, 'contract_agreed': False,
                       'extension_regular_salary_schedule': dict(zip(['2022-23', '2023-24', '2024-25', '2025-26'], schedule)),
                       'total_extended_regular_salary': total, 'annual_changes': changes, 'eight_percent_first_extended_year_bound': ratio(allowed),
                       'first_year_2022_25percent_cap_bound': 30913750,
                       'extended_years': 4, 'original_plus_extended_seasons_at_execution': 5,
                       'full_base_protection_proposal_under_standard_CBA_conditions': True,
                       'no_new_bonus_or_options_proposal': True,
                       '2021_22_current_charge_unchanged_before_any_hypothetical_trade': 6920027,
                       '2022_23_normal_Salary_and_apron_base_in_this_no_bonus_live_contract_candidate': schedule[0],
                       '2022_QO_RFA_or_FAhold_arises_if_extension_is_actually_implemented': False,
                       '2022_required_QO_or_FirstRefusal_zero_by_live_contract_not_renunciation': True,
                       'pre_July1_2022_hypothetical_trade': {
                           'no_trade_selected': True,
                           'regular_salary_only_outgoing_assignor_reference': 6920027,
                           'regular_salary_only_incoming_assignee_poison_pill_reference': ratio(incoming),
                           'original_actual_trade_bonus_percentage': None,
                           'bonus_if_any_preserved_original_term_only_fullannual_upper': ratio(Fraction(6920027 * 15, 100)),
                           'trade_bonus_charge_allocation_and_unearned_fraction': 'Apply VII3b/XXIV2 to the hypothetical trade; these base references are not whole matching certification.',
                           'new_general_six_month_7a_extension_trade_ban_applied_to_7b': False,
                           'other_trade_prerequisites_not_automatically_satisfied': True},
                       'from_July1_2022_hypothetical_trade': {
                           'poison_pill_from_this_extension_ends': True,
                           'base_matching_reference_by_current_extended_season': 'Use that current season Salary; no new signing/assignment receipt or trade certified.',
                           'extended_term_new_or_carried_trade_bonus_in_candidate': 0,
                           'zero_reason': 'Consensual proposed no-new-kicker terms; if old unearned kicker exists, authorized replacement Ex4 excludes extended term. Not an absence finding about old private clause.'},
                       'future_statutory_minimum_maximum_amendments_preserved': True,
                       'whole_2022_roster_cost_or_matching_certificate': False})
    result.append({'id': 'CX4', 'classification': 'UNSELECTED_NO_2021_EXTENSION_RFA_BRANCH',
                   'author_locked': False, 'contract_agreed': False, 'extension_regular_salary_schedule': None,
                   'original_expiry': '2022-06-30', 'future_salary_not_assigned_zero': True,
                   '2022_QO_RFA_offer_sheet_and_starter_test': 'Delegated separate RFA/QO source family; conditional timely QO/nonrenunciation and2021-22 stats remain inputs.',
                   'unextended_trade_poison_pill_from_2021_extension': False,
                   'no_new_required_QO_amount_selected_here': True})
    return {'id': 'CARTER_2021_EXTENSION_CANDIDATE_FAMILY_2026_10_07',
            'status': 'INDEPENDENTLY_REVIEWED_FOUR_EXISTING_ALTERNATIVES_CONSENSUAL_LEGAL_FORM_CANDIDATES',
            'source_main_snapshot': '16167cf4f6f2da50cbb1c054b948f9efedee3ddc',
            'source_sha256': {**PINS, SELF: sha(SELF)}, 'hash_method': 'UTF8 BOM stripped; CRLF/CR toLF',
            'raw_sources': raw, 'primary_rules': ev, 'candidate_common_terms': t,
            'calendar': {'start_ET': '2021-08-06T12:01:00', 'deadline_ET': '2021-10-18T18:00:00',
                         'derivation': 'VII7b window + approved2021 moratorium + NBA officialOct19 season opening.',
                         'candidate_execution_ET': t['candidate_execution_ET'], 'actual_extension_execution_date': None,
                         'old_rookie_term_end': '2022-06-30', 'extended_term_start': '2022-07-01'},
            'alternatives': result,
            'summary': {'alternatives': 4, 'extension_schedules': 3, 'source_direction_changed': False,
                        'source_supported_candidate_term_raise_max_checks_pass': True,
                        'all_options_author_selected': False, 'selected_Carter_contract': None,
                        'actual_mutual_consent_or_private_contract_certified': False,
                        'whole_cost_or_trade_execution_PASS': False, 'macro3_complete': False,
                        'new_REGISTER_promotion': False, 'independent_review_completed': True,
                        'design_gate': 'CLOSED', 'manuscript_allowed': False},
            'next_boundary': 'Consequential choice CX1/CX2/CX3/CX4 remains unselected. RFA/QO calculations attach only toCX4; whole2022 cost consumes the chosen live salary or actual QO family after choice, without assuming approval.'}


def validate(o):
    try:
        expected = build()
    except (AssertionError, OSError, KeyError, ValueError) as e:
        return ['source_or_candidate_guard: ' + str(e)]
    return [] if o == expected else ['saved_candidate_differs_from_source_bound_reconstruction']


def markdown(o):
    lines = ['# Carter2021 연장: 기존 CX1–4의 계약 구현 후보', '',
             '`' + o['status'] + '`. M1/A 성장 코어를 보존하는 기존 비교안입니다. CX1 권고는 선택·합의가 아니며 세 연장안과 무연장 RFA안 중 어떤 것도 정본화하지 않았습니다.', '',
             '## 기존 금액과 구체 법적 형태', '',
             '|안|2022–23|2023–24|2024–25|2025–26|4년합계|매년감액|', '|---|---:|---:|---:|---:|---:|---:|']
    for r in o['alternatives'][:3]:
        lines.append('|' + r['id'] + '|' + '|'.join(format(v, ',') for v in r['extension_regular_salary_schedule'].values()) + '|' + format(r['total_extended_regular_salary'], ',') + '|' + format(-r['annual_changes'][0], ',') + '|')
    lines += ['|CX4|미선택|미선택|미선택|미선택|2022 RFA|무연장|', '',
              '3개 안은4새시즌·기존마지막2021–22와 총5시즌이며, 선수·Chicago의 조건부 동의를 전제로 표의 Regular Salary 전액을 lack-of-skill 및 injury/illness 표준 CBA 보호조건 아래 보장하는 제안입니다. 추가 signing/performance/promotional/loan/buyout bonus, 새 trade kicker, 옵션·ETO는 넣지 않는 유한 구현입니다. 이는 사적 계약의 실제조건을 인증하는 것이 아닙니다. CX2의 할인 수락은 자동 충성심 사실이 아닙니다.', '',
              '## 기한·급여·QO', '',
              '[2017 CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) VII7b(PDF245–246), VII5c3(PDF219), IX1(PDF299)을 직접 대조했습니다. 연장 제안 시각은2021-10-15 12:00 ET이며 허용창은Aug6 12:01 ET부터Oct18 18:00 ET까지입니다. 말단은 [NBA 공식2021 캘린더](https://pr.nba.com/2021-22-nba-schedule-75th-anniversary-season/)의Oct19 개막과 CBA의 전날 규칙으로 구했습니다. 실제접수일·동의는 null입니다.', '',
              '매년감액은 첫 연장년 급여의8% 이내이고 최대첫해16.98m도2022 cap25%인30.91375m보다 작습니다. 기존2021–22 급여6,920,027은 연장 서명으로 올리거나 줄이지 않습니다. 법정 minimum/max 자동조정과 향후 적용 규칙은 보존하며2025–26 실제행정·새 CBA 전체 검문으로 승격하지 않습니다. 새 MLE 사용/하드캡 발동도 이 연장으로 자동추론하지 않습니다.', '',
              '연장안이 실제 구현된 경우2022–23은 live contract여서2022 FAhold/QO/RFA가 새로 생기지 않습니다. 무연장CX4만2022-06-30 만료 후 QO·시장·offer sheet·starter test로 연결되며 그 계산은 별도 RFA/QO 가족에 맡깁니다. 무연장을 미래급여0이나 권리 renounce로 바꾸지 않습니다.', '',
              '## 거래 매칭과 원 보너스 권리', '',
              'VII8f(PDF255)의 일반6개월 연장 거래금지는 VII7a에 대한 조항입니다. 이번 VII7b rookie 연장에 그것을 자동 적용하지 않습니다. 다만 VII8g(PDF256)에 따라2022-07-01 전에는 수취 팀의 급여 참조가 원 마지막 해+4새년의 평균이 됩니다. 기본급만의 참조는 아래와 같고, 실제 trade·양측 매칭 전체 PASS가 아닙니다.', '',
              '|안|Chicago 송출 기본급 참조|수취 기본급 poison-pill 참조|', '|---|---:|---:|']
    for r in o['alternatives'][:3]:
        q = r['pre_July1_2022_hypothetical_trade']['regular_salary_only_incoming_assignee_poison_pill_reference']
        lines.append('|' + r['id'] + '|6,920,027|' + format(q['numerator'] / q['denominator'], ',.1f') + '|')
    lines += ['',
              '원 rookie 계약의 미지 trade bonus를 부재로 인증하지 않습니다. 존재하면서 아직 미지급이면 XXIV2a(v)(PDF399–400)가 허용한 같은 원조건의 대체 Exhibit4로 extended term만 bonus 적용에서 제외하는 제안입니다. 원기간의 권리는 보존합니다. 그 원기간 fullannual15% 넓은 상한은1,038,004.05이며 실제 earned·allocation·waiver는 null입니다. 가상 거래가 있다면 그 비용을 규칙대로 더해야 하므로 표의 기본급만으로 매칭을 인증하지 않습니다. bonus의 합의 면제를 별도로 택하는 거래에는 VII7d3의 후속 연장/재협상6개월 하한이 다시 적용됩니다.', '',
              '2022-07-01 이후 poison-pill이 끝나도 거래·상대팀 여유·접수는 자동완료가 아닙니다. 본 제안의 extended-term kicker0은 허용된 상호합의 조건의 후보이고 원현실 사적조항0 인증이 아닙니다. [NBA의 원 Carter 기사](https://www.nba.com/news/orlando-magic-sign-wendell-carter-jr-to-contract-extension)는 역사적 맥락만 제공하며 Chicago 수락을 상속하지 않습니다.', '',
              '## 검문 범위', '',
              '고정8repo+SELF/current core producer, 새official2raw·재사용2021moratorium과Carter rookie row·CBA16쪽 지문을 연결했습니다. source-schedule 의미반전, 창밖날짜, 기존bonus소거, 권위승격을 실제 negative controls로 검사합니다. 국소 계약형태와 기존 스케줄 검문이며 전체비용·거래 실행·macro3·원장 승격0입니다.', '',
              '[JSON](CARTER_2021_EXTENSION_CANDIDATE_FAMILY_2026_10_07.json) · [전체로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)', '',
              '|번호|묶음|상태|', '|---|---|---|', '|1|2020 드래프트 연쇄|완료|', '|2|Chicago2020–21|S2완료|',
              '|3|2021–23 거래·계약|기존Carter4안 법적형태 후보,중요선택 미완료|', '|4|장기 커리어|후속설계|',
              '|5|결말·전체 구조|전체기능표 미완료|', '|6|집필규격·Context Pack|현행 누적 등록기 참조·Pack0|',
              '|7|통합·독립·작가승인|최종게이트 CLOSED|', '', '미완료 큰 묶음 **5**. `v0.30 PARTIAL`/게이트`CLOSED`/원고0.']
    return '\n'.join(lines) + '\n'


def self_test(o):
    tests = []
    for name, mut in [
        ('CX1_author_selection', lambda x: x['summary'].update(selected_Carter_contract='CX1')),
        ('original_cash_changed', lambda x: x['alternatives'][0].update(**{'2021_22_current_charge_unchanged_before_any_hypothetical_trade': 14150000})),
        ('outgoing_wrong_poison_average', lambda x: x['alternatives'][0]['pre_July1_2022_hypothetical_trade'].update(regular_salary_only_outgoing_assignor_reference=11384005.4)),
        ('blanket_rookie_six_month_bar', lambda x: x['alternatives'][0]['pre_July1_2022_hypothetical_trade'].update(new_general_six_month_7a_extension_trade_ban_applied_to_7b=True)),
        ('actual_consent', lambda x: x['summary'].update(actual_mutual_consent_or_private_contract_certified=True)),
        ('RFA_future_zero', lambda x: x['alternatives'][3].update(extension_regular_salary_schedule=[0, 0, 0, 0])),
    ]:
        b = copy.deepcopy(o)
        mut(b)
        assert validate(b), name
        tests.append(name)
    for name, mut in [
        ('constructor_after_deadline', lambda x: x.update(candidate_execution_ET='2021-10-19T12:00:00')),
        ('constructor_same_total_wrong_schedule', lambda x: x['schedules']['CX1'].__setitem__(slice(0, 2), [14150001, 13049999])),
        ('constructor_erase_old_kicker', lambda x: x.update(existing_original_bonus_clause_if_any='ALL_OLD_BONUSES_ZERO')),
    ]:
        t = terms()
        mut(t)
        with patch(__name__ + '.terms', return_value=t):
            try:
                build()
            except AssertionError:
                tests.append(name)
            else:
                raise AssertionError(name)
    return tests


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--write', action='store_true')
    p.add_argument('--check', action='store_true')
    p.add_argument('--self-test', action='store_true')
    a = p.parse_args()
    o = build()
    if a.write:
        (ROOT / OUT).write_text(json.dumps(o, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
        (ROOT / MD).write_text(markdown(o), encoding='utf8')
    if a.check:
        assert not validate(load(OUT))
        assert text(MD) == markdown(o)
    print(json.dumps({'current': True, 'summary': o['summary'], 'negative_controls': self_test(o) if a.self_test else []}, ensure_ascii=False))
