"""Build A01-EF-003 from locked C1–C3 and bounded school follow-up design.

The function bridges A01-S1 to A01-S2. The following CF07 remains a
conditional candidate and is not promoted by this record.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_a01_e2_final_episode_function as e2
import build_a01_followup_school_path as followup
import check_a01_opening_blueprint as blueprint_check


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_E3_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A01_E3_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a01_e3_final_episode_function.py',
    'design/A01_E2_FINAL_EPISODE_FUNCTION.json',
    'design/A01_FOLLOWUP_SCHOOL_PATH_2026_10_07.json',
    'design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/STORY_BIBLE.md',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json',
)
CONTRIBUTION_SEMANTIC_SHA256 = '362ef7fccfb99f00cb07b148ac7062cdb768fbb72ad63e1db8e055cef95641b9'
CF07_CANDIDATE_ENTRY_PIN = '동료의 득점으로 이어지면서 자신의 득점 없이 팀이 자신을 필요로 하는 첫 경험이 생긴다'


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def semantic_sha(data):
    projection = {k: v for k, v in data.items() if k != 'source_rev_sha256'}
    return hashlib.sha256(json.dumps(projection, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, e2.OUTPUT)
    path = load(root, followup.OUTPUT)
    contribution = load(root, 'design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json')
    candidates = load(root, 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json')
    packet = load(root, 'design/CP2_ACT_SUBACT_PACKET.json')
    delegated = load(root, 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json')
    assert not e2.validate(previous, root=root), 'E2 final function source is stale'
    assert not followup.validate(path, root=root), 'follow-up school path is stale'
    assert previous['episode_function_id'] == 'A01-EF-002'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (2, 2)
    assert previous['exit_state'] == contribution['entry_state']
    assert semantic_sha(contribution) == CONTRIBUTION_SEMANTIC_SHA256
    assert contribution['status'] == 'ACTUAL_VERIFIED'
    assert [b['id'] for b in contribution['beats']] == ['C1', 'C2', 'C3']
    assert sum(len(b['claims']) for b in contribution['beats']) == 5
    assert all(c['evidence_class'].startswith('AUTHOR_LOCKED_CANON_')
               for b in contribution['beats'] for c in b['claims'])
    assert path['status'] == 'ROUTINE_FICTIONAL_FOLLOWUP_DESIGN_SELECTED'
    assert path['same_fictional_school_operating_plan'] is True
    assert path['first_trial_permission_automatically_recurs'] is False
    assert path['renewed_limited_clearance_required_for_each_participated_session'] is True
    assert path['academic_supplement_is_future_promise_only'] is False
    assert path['actual_real_school_or_case_records_certified'] is False
    assert set(path['modeled_pre_participation_check_each_session']) == {
        'same_day_class_attendance', 'academic_supplement', 'punctuality'}
    assert all(v == followup.SATISFIED
               for v in path['modeled_pre_participation_check_each_session'].values())
    assert path['next_day_revisit_exact_correspondence_to_C1_assigned'] is False
    cf = {f['id']: f for f in candidates['functions']}
    assert cf['A01-CF05']['subact'] == 'A01-S1'
    assert cf['A01-CF06']['subact'] == 'A01-S2'
    assert cf['A01-CF07']['subact'] == 'A01-S2'
    assert cf['A01-CF07']['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf['A01-CF07']['selected_event'] is False
    assert cf['A01-CF07']['entry_state'] == CF07_CANDIDATE_ENTRY_PIN
    assert '자신의 득점 없이' not in contribution['exit_state']
    assert cf['A01-CF07']['next_dependency'] == '준비를 피할 때 동료가 대신 떠안는 일을 보게 된다'
    a01 = next(a for a in packet['acts'] if a['id'] == 'A01')
    assert (a01['planned_units'], a01['allocation_start'], a01['allocation_end']) == (36, 1, 36)
    assert delegated['selected']['style']['route'] == 'S1'
    assert contribution['information_boundary']['pov_style_direction'] == 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY'
    beats = []
    for beat in contribution['beats']:
        beats.append({
            'id': beat['id'], 'function_event': beat['event'],
            'relative_time': beat['relative_time'],
            'claims': [{k: claim[k] for k in ('claim', 'evidence_class', 'source_path',
                                             'source_anchor', 'protagonist_access',
                                             'other_person_access', 'unknown')}
                       for claim in beat['claims']],
        })
    return {
        'schema': 'A01_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A01-EF-003',
        'act': 'A01',
        'primary_subact': 'A01-S2',
        'entry_bridge_from_subact': 'A01-S1',
        'subact_boundary_basis': 'Existing conditional CF05 is S1; CF06 and CF07 are S2 candidates. C1–C3 remain one reviewed local core.',
        'final_function_order': 3,
        'planned_allocation_slot': 3,
        'published_episode_number': None,
        'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36,
            'prior_function_slots': 2,
            'this_function_slots': 1,
            'assigned_function_slots_through_this': 3,
            'remaining_planned_slots': 33,
            'allocation_is_final_published_episode_count': False,
        },
        'final_episode_functions_completed_this_record': 1,
        'local_contiguous_functions_through_this': 3,
        'previous_function': {'id': previous['episode_function_id'],
                              'path': str(e2.OUTPUT).replace('\\', '/'),
                              'exit_state': previous['exit_state']},
        'single_function': contribution['single_function'],
        'entry_state': contribution['entry_state'],
        'unit_choice': contribution['unit_choice'],
        'exit_state': contribution['exit_state'],
        'direct_present_cost': copy.deepcopy(contribution['direct_present_cost']),
        'reader_question_at_end': '첫 본능적 기여를 다시 할 수 있도록 위치·박스아웃·패스의 무엇을 배울 것인가',
        'reader_question_class': 'EDITORIAL_INFERENCE_FROM_LOCKED_LEARNING_DIRECTION_NOT_NEW_EVENT',
        'internal_order': ['C1', 'C2', 'C3'],
        'beats': beats,
        'next_unit': {
            'candidate_id': 'A01-CF07',
            'candidate_status': cf['A01-CF07']['status'],
            'candidate_function': cf['A01-CF07']['function'],
            'candidate_entry_non_authoritative_summary': cf['A01-CF07']['entry_state'],
            'exact_full_entry_for_next_function': contribution['exit_state'],
            'candidate_entry_is_exact_string_match': False,
            'candidate_summary_is_verified_projection_of_full_exit': False,
            'candidate_summary_unverified_extra_detail': ['자신의 득점 없이'],
            'locked_learning_direction': contribution['next_boundary']['locked_direction'],
            'is_executed_in_this_function': False,
            'candidate_is_final_episode_function': False,
        },
        'information_access': copy.deepcopy(contribution['information_boundary']),
        'source_inferences': copy.deepcopy(contribution['inferences']),
        'school_authority': {
            'fictional_followup_path_selected': True,
            'followup_path': str(followup.OUTPUT).replace('\\', '/'),
            'pre_participation_three_conditions_rechecked_each_session_in_model': True,
            'modeled_condition_check': copy.deepcopy(path['modeled_pre_participation_check_each_session']),
            'real_school_or_case_records_certified': False,
            'one_trial_clearance_automatically_reused': False,
            'standing_team_membership_or_registration_certified': False,
            'official_contest_eligibility_certified': False,
            'retrospective_attendance_deletion': False,
        },
        'unassigned_details': {
            'school_name': None, 'exact_date': None,
            'next_day_revisit_equals_C1': None,
            'C1_C2_same_session': None,
            'training_session_count': None,
            'exact_attendance_or_supplement_record': None,
            'trial_or_game_format': None,
            'score_or_receiver_scorer_name': None,
            'individual_scene_pov': None,
            'dialogue_or_team_private_reaction': None,
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {p: sha((root / p).read_bytes()) for p in SOURCES},
        'source_semantic_projection_sha256': {'first_contribution': CONTRIBUTION_SEMANTIC_SHA256},
        'verification_limits': [
            'C1–C3 are locked story events but precise practice timing, drills, score and scene execution are unverified.',
            'The school path is a fictional repeat-check model, not proof of actual attendance, supplement records or team registration.',
            'CF07 remains a candidate; its entry is not a verified projection and contains an unverified no-protagonist-score detail. Only the full C3 exit is exact next input.',
            'Three assigned planned slots do not establish published numbering or whole G13 completion.',
        ],
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'g15_complete': False,
        'g16_complete': False, 'g17_complete': False,
        'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }


def render(data):
    rows = ['| 순서 | 정본 Beat | 기능상 사건 |', '| --- | --- | --- |']
    for i, beat in enumerate(data['beats'], 1):
        rows.append(f"| {i} | {beat['id']} | {beat['function_event']} |")
    return '\n'.join([
        '# A01 세 번째 최종 회차 기능 — C1–C3', '',
        '이 문서는 **원고가 아닌 회차 기능표**다. 첫 완패 뒤 자존심으로 남는 선택, 한 연속 리바운드→아웃렛→팀 득점, 팀에 필요한 사람이라는 자기 느낌을 기존 정본 순서대로 한 기능에 묶는다.', '',
        '- 기능 `A01-EF-003`, 순서/계획 슬롯 3. A01 계획 36슬롯 중 국소 기능 3개 배정·잔여 33개. 출판 회차 번호와 전체 분량은 미정이다.',
        '- C1은 A01-S1의 조건부 CF05와 연결되는 입구이며 C2–C3의 첫 기여는 A01-S2의 CF06 후보와 만난다. 기능은 S1→S2 경계를 지나지만 기존 후보를 최종 회차나 작가 잠금으로 승격하지 않는다.', '',
        '## 기능과 인계', '',
        f"- 시작: {data['entry_state']}",
        f"- 단일 기능: {data['single_function']}",
        f"- 이미 잠긴 잔류 선택: {data['unit_choice']}",
        f"- 직접 비용: {data['direct_present_cost']['claim']} 시간/공 사용의 직접 비용은 원본의 표시된 추론이며 확정된 게임 약속 취소나 자기 득점 기회를 추가하지 않는다.",
        f"- 끝: {data['exit_state']}",
        f"- 다음 독자 질문: {data['reader_question_at_end']}", '',
        *rows, '',
        'E2 종료와 이 기능 시작은 문자 단위로 같다. 다음 `A01-CF07`은 여전히 조건부 후보이며 그 시작 상태는 **검증된 투영이 아니다**. 후보의 ‘자신의 득점 없이’는 정본/C3 전체 종료에서 보증하지 않는 추가 세부이므로 다음 입력 사실로 옮기지 않는다. 다음 최종 기능이 만들어지면 C3의 전체 종료 상태만 정확 입력으로 받아야 한다. 박스아웃·위치선정·패스 학습은 이번 기능에서 실행/숙련 완료로 쓰지 않는다.', '',
        '## 후속 훈련의 학교 권한과 정보', '',
        '- [학교 후속 운영안](A01_FOLLOWUP_SCHOOL_PATH_2026_10_07.md)은 첫 체험 일회 허용을 자동 반복하지 않는다. 필요한 후속 훈련마다 가상학교 계획 안에서 출석·학업보충·시간 준수 세 조건을 다시 충족 확인하고 감독이 지도·안전을 맡는다. 실제 학교·개별 기록·등록·대회 자격을 인증하지 않는다.',
        '- 패배 다음 날 자발적 체육관 재방문은 정본으로 보존하되 C1의 정확 훈련일과 등치하지 않는다. C1/C2 동세션, 세션 수, 경기 형식·동작·점수·대사·동료 속마음은 미정이다.',
        '- S1 밀착 3인칭 정보 경계에서 주인공은 자신의 잔류, 리바운드·아웃렛, 팀 득점과 자기 느낌만 안다. 팀 전원의 장기 신뢰나 감독의 비공개 평가를 인물 지식으로 넣지 않는다. 개별 장면 POV는 미인증이다.', '',
        '## 완료 범위', '',
        '- [첫 기여 Blueprint](A01_FIRST_CONTRIBUTION_BLUEPRINT.json)의 3 Beat/5 잠긴 주장과 비용 추론 I1–I2를 분리해 사용했다. 새 사건·작가 잠금은 0건이다.',
        '- 이번 국소 기능 1개, 연속 기능 3개. 전체 G13/G14·실제 Pack·G15–G17·원고 허가는 미완료다. 게이트 `CLOSED`, `manuscript_allowed:false`.',
        '- JSON 출처 지문과 재구성 검사는 현재성·경계·권한을 검문한다. 서술 품질이나 실제 학교 절차의 개별 증빙은 인증하지 않는다.', '',
    ])


def validate(data, root=ROOT, currentness=True):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError) as exc:
        return [f'source construction: {exc}']
    errors = [] if data == expected else ['record differs from source-bound third function']
    if currentness:
        _, blueprint_errors = blueprint_check.check(root=root, unit='first-contribution')
        errors.extend(f'first-contribution: {e}' for e in blueprint_errors)
    return errors


def self_test(data):
    mutations = [
        ('wrong slot', lambda d: d.update(planned_allocation_slot=4)),
        ('split C2', lambda d: d['internal_order'].insert(2, 'OUTLET_EXTRA_EPISODE')),
        ('wrong reward', lambda d: d['beats'][2].update(function_event='팀 전원의 장기 신뢰를 확정한다')),
        ('CF07 false promotion', lambda d: d['next_unit'].update(candidate_is_final_episode_function=True)),
        ('CF07 false projection', lambda d: d['next_unit'].update(candidate_summary_is_verified_projection_of_full_exit=True)),
        ('next-day C1 invention', lambda d: d['unassigned_details'].update(next_day_revisit_equals_C1=True)),
        ('skip supplement', lambda d: d['school_authority']['modeled_condition_check'].pop('academic_supplement')),
        ('real records', lambda d: d['school_authority'].update(real_school_or_case_records_certified=True)),
        ('false manuscript gate', lambda d: d.update(manuscript_allowed=True)),
        ('false source SHA', lambda d: d['source_rev_sha256'].update({'canon/STORY_BIBLE.md': '0' * 64})),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        assert validate(candidate, currentness=False), name
    return len(mutations)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MARKDOWN).write_text(render(data), encoding='utf-8')
    errors = validate(data)
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors.extend(validate(saved))
        if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'function': data['episode_function_id'], 'local_complete': 1,
                      'contiguous_functions': 3, 'remaining_planned_slots': 33,
                      'negative_controls': tested, 'current': not errors,
                      'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
