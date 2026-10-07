"""Select one bounded Chicago contact-to-summer routine after A04 E3."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a04_e3_final_episode_function as previous_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A04_CF05_CF06_CONTACT_SUMMER_WORKING_MODEL_2026_10_07.json')
MARKDOWN = OUTPUT.with_suffix('.md')
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
CANDIDATES = 'design/A04_DRAFT_CONDITIONAL_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
TIMELINE = 'canon/CAREER_TIMELINE.md'
CHICAGO = 'design/CHICAGO_FRANCHISE_REOPEN.md'
SOURCES = ('tools/build_a04_cf05_cf06_contact_summer_working_model.py',
           PREVIOUS, CANDIDATES, CP2, TIMELINE, CHICAGO)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def normalized_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


EXPECTED_CF05 = {
    'id': 'A04-CF05', 'subact': 'A04-S2',
    'dominant_function': 'Chicago 연락과 계약·개발 설명 확인',
    'cause': '평가 준비와 수정 시도 뒤 기존 Chicago 지명 방향의 연락 단계에 들어간다',
    'entry_state': '정답을 알았다는 설명 대신 수정 시도의 행동을 평가에 내놓는다',
    'pressure': '지명받는 것과 실제 팀의 주전·공격 권한을 얻는 것은 다르다',
    'choice': 'Chicago 쪽 연락과 가상 에이전트의 설명에서 자신이 준비할 계약·개발 과제를 묻고 1라운드 표준계약 방향의 입단 준비를 이어 가려 한다',
    'direct_cost': '쉬거나 개인 활동에 쓸 시간을 계약·개발 일정의 미확인 항목을 묻고 확인하는 데 쓴다',
    'changed_state': '받은 설명과 아직 확인되지 않은 계약·개발 일정 항목을 구분해 입단 준비를 이어 간다',
    'next': 'A04-CF06',
    'next_dependency': '여름 시간을 대표팀 활동과 구단 개발에 동시에 쓸 수 없는 선택으로 이어진다',
}
EXPECTED_CF06 = {
    'id': 'A04-CF06', 'subact': 'A04-S3',
    'dominant_function': '구단 개발 일정에 남는 여름 선택',
    'cause': '받은 설명과 미확인 계약·개발 일정 항목을 구분해 입단 준비를 이어 가고 있다',
    'entry_state': '받은 설명과 아직 확인되지 않은 계약·개발 일정 항목을 구분해 입단 준비를 이어 간다',
    'pressure': '여름 시간을 한국대표팀 활동과 Chicago 루키 준비에 모두 쓸 수는 없다',
    'choice': '기존 2018 아시안게임 불참 방향대로 Chicago 개발 일정에 남아 맡을 준비를 이어 간다',
    'direct_cost': '그 여름을 한국대표팀 도전에 쓸 길을 택하지 않는다. 이는 대표팀 자리를 보장받았다가 양보한다는 뜻이 아니다',
    'changed_state': 'Chicago의 새 속도·역할을 배울 준비를 택하지만 공격·자기관리의 빈틈은 남는다',
    'next': 'A05-S1',
    'next_dependency': 'A05에서 루키 역할과 NBA 준비의 실제 수행을 시험한다',
}


def build(root=ROOT):
    previous = load(root, PREVIOUS)
    candidates = load(root, CANDIDATES)
    cp2 = load(root, CP2)
    assert previous == previous_builder.load(root, previous_builder.OUTPUT)
    assert not previous_builder.validate(previous, root=root), 'A04 E3 must be source-current'
    assert previous['episode_function_id'] == 'A04-EF-003'
    assert previous['final_function_order'] == 25 and previous['planned_allocation_slot'] == 147
    assert previous['next_unit']['id'] == 'A04-CF05'
    assert previous['next_unit']['private_board_or_pick_response_prepaid'] is False
    assert previous['bounded_A04_S1_preparation_audit']['source_CP2_literal_presentation_to_external_evaluator_observed'] is False
    assert previous['whole_A04_S1_exit_certified'] is False
    assert previous['whole_g13_complete'] is False and previous['manuscript_allowed'] is False
    assert candidates['status'] == 'SIX_CONDITIONAL_DRAFT_CAUSAL_FUNCTIONS_NOT_FINAL_G13'
    cf05, cf06 = candidates['functions'][4:6]
    for source, expected in ((cf05, EXPECTED_CF05), (cf06, EXPECTED_CF06)):
        assert {key: source[key] for key in expected} == expected, source['id']
        assert source['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
        assert source['selected_event'] is False and source['author_locked'] is False
        assert source['observational_access'] == (
            '주인공 경험·직접 시도·허용된 평가 피드백·본인이 받은 연락/설명만 후보 접근. '
            '구단의 비공개 보드·타인 내면·의료 판정·미래 결과는 모른다.')
        assert all(source[key] is None for key in (
            'draft_pick', 'draft_call_date_or_words', 'contract_signing_date',
            'contract_salary_or_scale_rate', 'agent_name', 'score_or_box_stats',
            'national_team_roster_place', 'medical_test_results'))
    assert cf05['next'] == cf06['id'] and cf05['changed_state'] == cf06['entry_state']
    assert cf05['subacts_covered'] == ['A04-S2', 'A04-S3']
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    s2, s3 = [next(row for row in cp2['subacts'] if row['id'] == name)
              for name in ('A04-S2', 'A04-S3')]
    assert s2['entry_state'] == 'Chicago 입단을 즉시 주전으로 읽음'
    assert s2['choice'] == 'Chicago 입단을 주전 약속으로 읽지 않고 구단이 요구하는 개발 과제부터 확인한다'
    assert s2['institutional_constraint'] == '정확 순번·하류 보드·rookie 계약 HOLD'
    assert s3['entry_state'] == '프로 계약을 보상으로만 읽음'
    assert s3['choice'] == '표준계약의 보상만 보지 않고 기존 2018 개발 일정과 대표팀 불참 방향의 비용을 받아들인다'
    assert s3['exit_state'] == '2018 개발 일정에 남음'
    timeline = (root / TIMELINE).read_text(encoding='utf-8-sig')
    chicago = (root / CHICAGO).read_text(encoding='utf-8-sig')
    assert 'NBA Draft를 통해 Chicago 진입, 1라운드 표준계약·아시안게임 불참' in timeline
    assert '실제 22순위는 최우선 후보지만 정확 순번은 HOLD' in timeline
    assert '2018 주인공은 Chicago의 Summer League와 루키 개발 일정에 남는다' in timeline
    assert '한국의 실제 동메달을 유지한다' in timeline
    assert 'Chicago 팀 선택과 22순위 확정은 분리' in chicago
    assert '1라운드 rookie-scale' in chicago

    steps = [
        {
            'id': 'C0', 'source_function': 'A04-CF05',
            'kind': 'EXISTING_LANDING_DIRECTION_CONDITIONAL_BRIDGE',
            'action': 'Place the fictional preparation exchange after the already approved Chicago first-round landing direction has become publicly knowable in the alternate story. Leave the exact pick, draft call, date, agent identity and signed UPC unspecified.',
            'observable_result': 'The protagonist can ask about onboarding and developmental preparation without gaining access to a private board or automatically becoming a starter.',
            'new_exact_draft_event_certified': False,
        },
        {
            'id': 'C1', 'source_function': 'A04-CF05',
            'kind': 'BOUNDED_FICTIONAL_CONTACT_AND_QUESTION',
            'action': 'Through an unnamed fictional representative, he receives a Chicago-side general preparation contact and asks which first-round contract documents, medical/eligibility checks and rookie development steps still require authorized confirmation.',
            'observable_result': 'The contact identifies categories to verify; no person supplies a final salary, medical clearance, roster place or guaranteed offensive role.',
            'actual_NBA_employee_identity_or_quote_certified': False,
        },
        {
            'id': 'C2', 'source_function': 'A04-CF05',
            'kind': 'DISTINGUISH_EXPLANATION_FROM_INSTITUTIONAL_EXECUTION',
            'action': 'The fictional representative separates the general first-round rookie-scale form and team development expectation from unsigned details and makes a short unanswered checklist for formal club/player processes.',
            'observable_result': 'He has an explanation and his own follow-up questions, not a signed contract, verified calendar, medical approval or a club promise of starting.',
            'representative_can_bind_Chicago_or_sign_UPC': False,
        },
        {
            'id': 'S1', 'source_function': 'A04-CF06',
            'kind': 'ONE_SUMMER_TIME_ALLOCATION_CHOICE',
            'action': 'Looking at the competing summer uses of his time, he chooses the already approved Chicago rookie-development path and does not pursue the 2018 Korean Asian Games route.',
            'observable_result': 'His planned summer blocks point to Chicago preparation. This foregoes the opportunity to try for a national-team route; it does not surrender an awarded roster place.',
            'guaranteed_Korea_roster_place_relinquished': False,
        },
        {
            'id': 'S2', 'source_function': 'A04-CF06',
            'kind': 'BOUNDED_PREPARATION_NOT_SEASON_PERFORMANCE',
            'action': 'He lists basic role and schedule questions for the Chicago development period while retaining the one-dribble attack limit and unresolved self-management work as the next demands.',
            'observable_result': 'The choice to prepare is visible; exact team schedule, formal registration, first NBA minutes and future role success remain unproved.',
            'A05_rookie_performance_prepaid': False,
        },
    ]
    exit_state = (
        '주인공은 승인된 Chicago 1라운드 진입 방향 뒤의 가상 준비 연락에서 계약 서류·검사·구단 개발 순서 중 '
        '누가 확인해야 할 항목인지 묻고, 설명받은 일반 범주와 아직 기관이 확정하지 않은 세부를 나누었다. '
        '그는 2018년 여름을 Chicago 루키 개발 준비에 쓰고 한국 아시안게임 경로를 추진하지 않기로 했다. '
        '대표팀 자리를 얻었다가 포기한 적은 없으며, 실제 계약 서명·의료 적합·정확 지명 순번·주전 권한도 이 연락으로 얻지 못했다. '
        '짧은 공격과 자기관리의 빈틈은 다음 루키 수행에서 남는다.'
    )
    return {
        'schema': 'A04_CF05_CF06_CONTACT_SUMMER_WORKING_MODEL_V1',
        'status': 'SELECTED_ROUTINE_CONTACT_SUMMER_INDEPENDENTLY_REVIEWED',
        'independent_review_completed': True,
        'scope': 'ONE_CONDITIONAL_POST_LANDING_FICTIONAL_INFORMATION_ROUTE_PLUS_APPROVED_SUMMER_TIME_CHOICE',
        'previous_exact_full_exit': previous['exit_state'],
        'source_function_ids': ['A04-CF05', 'A04-CF06'],
        'original_CP2_provisional_beliefs_inherited_as_observed': {
            'S2_immediate_starter_assumption': False,
            'S3_contract_only_as_reward_assumption': False,
        },
        'approved_direction_vs_unselected_institutional_details': {
            'Chicago_first_round_rookie_scale_direction': 'APPROVED_CANON_DIRECTION',
            '2018_Asian_Games_nonparticipation': 'APPROVED_CANON_DIRECTION',
            'exact_pick_and_downstream_draft_reassignment': None,
            'actual_draft_call_and_UPC_receipt': None,
            'exact_Chicago_development_calendar': None,
            'national_team_roster_selection': None,
        },
        'fictional_authority': {
            'unnamed_representative': 'May explain general contract/document categories and relay the protagonist’s questions; cannot bind Chicago, sign a UPC, certify medical clearance or promise a role.',
            'Chicago_side_general_contact': 'Fictional informational preparation contact conditional on the approved landing direction; no identified real executive, exact call wording, official receipt or private draft-board knowledge.',
            'formal_club_and_player_process': 'Only a separately authorized contract, medical, roster and calendar process could settle the unresolved particulars.',
            'national_team': 'No selection, guarantee or surrendered roster place is claimed.',
        },
        'source_candidate_choices_and_costs': {
            'CF05_choice': cf05['choice'], 'CF05_direct_cost': cf05['direct_cost'],
            'CF06_choice': cf06['choice'], 'CF06_direct_cost': cf06['direct_cost'],
        },
        'steps': steps,
        'direct_present_cost': {
            'CF05': 'He uses time otherwise free for rest or personal activity to ask and record unresolved contract/development categories.',
            'CF06': 'He does not spend this summer pursuing the Korean national-team route; there is no already awarded place to surrender.',
        },
        'selected_design_exit_state': exit_state,
        'next_unit': {'id': 'A05-S1', 'status': 'FUTURE_ROOKIE_FUNCTION_NOT_EXECUTED',
                      'NBA_minutes_or_starter_role_prepaid': False},
        'limits': {
            'actual_exact_pick_22_or_downstream_board_certified': False,
            'real_draft_call_date_or_words_claimed': False,
            'signed_UPC_exact_salary_option_bonus_or_agent_name_certified': False,
            'medical_clearance_or_official_team_roster_receipt_certified': False,
            'guaranteed_Korea_national_team_place_surrendered': False,
            'Chicago_development_schedule_exact_dates_certified': False,
            'A05_season_result_or_starting_position_prepaid': False,
            'new_consequential_author_lock': False,
            'final_episode_function_created_here': False,
            'whole_A04_S2_S3_or_Act_exit_certified': False,
            'whole_g13_complete': False, 'whole_g14_complete': False,
            'actual_context_packs': 0, 'manuscript_count': 0,
            'manuscript_allowed': False, 'design_gate': 'CLOSED',
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {path: normalized_sha((root / path).read_bytes()) for path in SOURCES},
    }


def render(data):
    lines = [
        '# A04 CF05·CF06 연락과 여름 선택 운영안', '',
        '**범위:** Chicago 1라운드 진입과 2018 아시안게임 불참이라는 승인 방향 안의 가상 준비 경로. 정확 지명·드래프트 호출·계약 서명·구단 일정의 실제 증명이 아니다.', '',
        f"- 상태: `{data['status']}`",
        f"- E3 정확 출구: {data['previous_exact_full_exit']}",
        '- 원 CP2의 “즉시 주전”과 “계약은 보상뿐”이라는 잠정 진입 심리는 현행 E3의 관측 사실로 상속하지 않는다.', '',
        '| 단계 | 국소 행동 | 직접 결과와 한계 |', '| --- | --- | --- |',
    ]
    for step in data['steps']:
        lines.append(f"| {step['id']} | {step['action']} | {step['observable_result']} |")
    lines += [
        '', '- 정보 권한: 이름 없는 가상 대리인은 일반 서류·개발 항목을 설명하고 질문을 전달한다. 가상 Chicago측 연락은 준비 범주만 전하며 공식 서명·의료·출전 권한을 행사하지 않는다.',
        f"- CF05 비용: {data['direct_present_cost']['CF05']}",
        f"- CF06 비용: {data['direct_present_cost']['CF06']}",
        f"- 국소 출구: {data['selected_design_exit_state']}",
        '- 대표팀에 보장된 자리를 양보한 적이 없다. 아시안게임 불참 방향과 한국의 실제 동메달은 보존한다.',
        '- A05 루키 수행, 전체 A04-S2/S3·Act, G13/G14·실제 Pack·원고는 이 모델로 완료되지 않으며 설계/원고 게이트 `CLOSED`다.', '',
    ]
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A04 contact/summer route differs from source-bound selection']


def self_test(data, root=ROOT):
    cases = [
        ('pick 22 prepaid', lambda x: x['limits'].update(actual_exact_pick_22_or_downstream_board_certified=True)),
        ('signed salary fabricated', lambda x: x['limits'].update(signed_UPC_exact_salary_option_bonus_or_agent_name_certified=True)),
        ('medical certified by contact', lambda x: x['limits'].update(medical_clearance_or_official_team_roster_receipt_certified=True)),
        ('national roster sacrifice invented', lambda x: x['steps'][3].update(guaranteed_Korea_roster_place_relinquished=True)),
        ('starter guarantee', lambda x: x['next_unit'].update(NBA_minutes_or_starter_role_prepaid=True)),
        ('intermediary signs contract', lambda x: x['steps'][2].update(representative_can_bind_Chicago_or_sign_UPC=True)),
        ('exact dates fabricated', lambda x: x['approved_direction_vs_unselected_institutional_details'].update(exact_Chicago_development_calendar='2018-07-07')),
        ('erase CF06 choice cost', lambda x: x['direct_present_cost'].update(CF06='')),
    ]
    for name, mutation in cases:
        changed = copy.deepcopy(data)
        mutation(changed)
        assert validate(changed, root), name
    original_load = load
    for name, path, mutation in [
        ('E3 exact exit flipped', PREVIOUS,
         lambda x: x.update(exit_state='Chicago 보드와 22순위가 공식 확정됐다')),
        ('CF05 same-ID choice becomes starting promise', CANDIDATES,
         lambda x: x['functions'][4].update(choice='Chicago가 즉시 주전을 보장했다고 선언한다')),
        ('CF06 same-ID cost becomes surrendered place', CANDIDATES,
         lambda x: x['functions'][5].update(direct_cost='확정된 국가대표 자리를 반납한다')),
        ('S3 CP2 exit becomes guaranteed title', CP2,
         lambda x: next(row for row in x['subacts'] if row['id'] == 'A04-S3').update(exit_state='루키 우승 보장')),
    ]:
        def altered(root, requested, path=path, mutation=mutation):
            source = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                source = copy.deepcopy(source)
                mutation(source)
            return source
        with patch(__name__ + '.load', side_effect=altered):
            assert validate(data, root), name
    return len(cases) + 4


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MARKDOWN).write_text(render(data), encoding='utf-8')
    errors = validate(data)
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors += validate(saved)
        if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'current': not errors, 'errors': errors,
                      'negative_controls': tested, 'status': data['status']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
