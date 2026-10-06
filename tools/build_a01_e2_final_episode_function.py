"""Build A01-EF-002 from locked T1–T2 and selected fictional school procedure.

The old opening-boundary memo's cumulative E2 alternative is not reused.
No manuscript, case record, or real-world school permission is certified.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_a01_e1_final_episode_function as e1
import build_a01_trial_school_operating_path as school
import check_a01_opening_blueprint as blueprint_check


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_E2_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A01_E2_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a01_e2_final_episode_function.py',
    'design/A01_E1_FINAL_EPISODE_FUNCTION.json',
    'design/A01_TRIAL_SCHOOL_OPERATING_PATH_2026_10_07.json',
    'design/A01_FIRST_TRIAL_BLUEPRINT.json',
    'design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'design/A01_OPENING_EPISODE_BOUNDARY.md',
    'canon/STORY_BIBLE.md',
    'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json',
)
TRIAL_SEMANTIC_SHA256 = 'be9dd623fb75b4489a2658602e95e8f91bccb8520cde7451048c2d11e1a05b6b'
CONTRIBUTION_SEMANTIC_SHA256 = '362ef7fccfb99f00cb07b148ac7062cdb768fbb72ad63e1db8e055cef95641b9'


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
    previous = load(root, e1.OUTPUT)
    operating = load(root, school.OUTPUT)
    trial = load(root, 'design/A01_FIRST_TRIAL_BLUEPRINT.json')
    contribution = load(root, 'design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json')
    packet = load(root, 'design/CP2_ACT_SUBACT_PACKET.json')
    delegated = load(root, 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json')
    boundary = (root / 'design/A01_OPENING_EPISODE_BOUNDARY.md').read_text(encoding='utf-8-sig')
    assert not e1.validate(previous, root=root), 'E1 final function source is stale'
    assert not school.validate(operating, root=root), 'school operating design is stale'
    assert previous['episode_function_id'] == 'A01-EF-001'
    assert previous['final_function_order'] == previous['planned_allocation_slot'] == 1
    assert previous['exit_state'] == trial['entry_state']
    assert semantic_sha(trial) == TRIAL_SEMANTIC_SHA256
    assert semantic_sha(contribution) == CONTRIBUTION_SEMANTIC_SHA256
    assert trial['status'] == contribution['status'] == 'ACTUAL_VERIFIED'
    assert [b['id'] for b in trial['beats']] == ['T1', 'T2']
    assert sum(len(b['claims']) for b in trial['beats']) == 3
    assert trial['exit_state'] == contribution['entry_state']
    assert contribution['beats'][0]['id'] == 'C1'
    assert all(c['evidence_class'].startswith('AUTHOR_LOCKED_CANON_')
               for b in trial['beats'] for c in b['claims'])
    assert operating['status'] == 'ROUTINE_FICTIONAL_SETTING_DESIGN_SELECTED_WITH_CASE_EXECUTION_LIMIT'
    assert operating['assessment']['institutional_authority_model_specified'] is True
    assert operating['assessment']['condition_delivery_model_specified'] is True
    assert operating['assessment']['fictional_limited_trial_clearance_modeled'] is True
    assert operating['assessment']['real_world_individual_permission_certified'] is False
    conditions = operating['condition_handling']
    assert conditions['delivered_to_protagonist_before_T1_in_selected_model'] is True
    assert set(conditions['selected_model_pre_T1_condition_check']) == {
        'same_day_class_attendance', 'academic_supplement', 'punctuality'}
    assert all(value == 'SATISFIED_FOR_LIMITED_TRIAL_IN_FICTIONAL_MODEL'
               for value in conditions['selected_model_pre_T1_condition_check'].values())
    assert conditions['actual_real_school_or_student_verification'] is False
    assert conditions['specific_case_records_certified'] is False
    assert operating['final_episode_functions_completed_this_artifact'] == 0
    a01 = next(a for a in packet['acts'] if a['id'] == 'A01')
    a01_s1 = next(s for s in packet['subacts'] if s['id'] == 'A01-S1')
    assert (a01['planned_units'], a01['allocation_start'], a01['allocation_end']) == (36, 1, 36)
    assert a01_s1['parent_act'] == 'A01'
    assert delegated['selected']['style']['route'] == 'S1'
    assert trial['information_boundary']['pov_style_direction'] == 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY'
    assert 'E1, 감독의 방과 후 조건부 체험 제안에서 끝낸다' in boundary

    beats = []
    for beat in trial['beats']:
        beats.append({
            'id': beat['id'],
            'function_event': beat['event'],
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
        'episode_function_id': 'A01-EF-002',
        'function_label': 'E2_SECOND_FUNCTION_AFTER_E1',
        'old_boundary_E2_cumulative_first_episode_alternative_selected': False,
        'act': 'A01', 'subact': 'A01-S1',
        'final_function_order': 2,
        'planned_allocation_slot': 2,
        'published_episode_number': None,
        'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36,
            'prior_function_slots': 1,
            'this_function_slots': 1,
            'assigned_function_slots_through_this': 2,
            'remaining_planned_slots': 34,
            'allocation_is_final_published_episode_count': False,
        },
        'final_episode_functions_completed_this_record': 1,
        'local_contiguous_functions_through_this': 2,
        'previous_function': {'id': previous['episode_function_id'],
                              'path': str(e1.OUTPUT).replace('\\', '/'),
                              'exit_state': previous['exit_state']},
        'single_function': trial['single_function'],
        'entry_state': trial['entry_state'],
        'unit_choice': trial['unit_choice'],
        'exit_state': trial['exit_state'],
        'direct_present_cost': copy.deepcopy(trial['direct_present_cost']),
        'reader_question_at_end': '첫 완패 뒤 동갑에게 무시당한 자존심으로 다음 훈련에 남을 것인가',
        'reader_question_class': 'EDITORIAL_INFERENCE_FROM_LOCKED_C1_NOT_NEW_AUTHOR_DECISION',
        'internal_order': ['T1', 'T2'],
        'beats': beats,
        'next_unit': {'beat_id': 'C1', 'function_event': contribution['beats'][0]['event'],
                      'entry_state': contribution['entry_state'], 'is_in_this_function': False,
                      'handoff_to_blueprint': 'design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json'},
        'information_access': copy.deepcopy(trial['information_boundary']),
        'source_inferences': copy.deepcopy(trial['inferences']),
        'school_authority': {
            'fictional_school_operating_path_selected': True,
            'operating_path': str(school.OUTPUT).replace('\\', '/'),
            'pre_T1_all_three_conditions_checked_in_model': True,
            'modeled_condition_check': copy.deepcopy(conditions['selected_model_pre_T1_condition_check']),
            'first_training_entry_is_locked_story_event': True,
            'real_school_or_case_records_certified': False,
            'coach_solo_attendance_or_registration_authority': False,
            'retroactive_attendance_deletion': False,
            'official_registration_or_contest_eligibility_certified': False,
        },
        'unassigned_details': {
            'school_name': None, 'exact_grade': None, 'exact_date': None,
            'offer_day_equals_trial_day': None, 'exact_attendance_or_supplement_record': None,
            'trial_format_or_score': None, 'exact_dialogue': None,
            'rival_private_thought': None, 'individual_scene_pov': None,
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {p: sha((root / p).read_bytes()) for p in SOURCES},
        'source_semantic_projection_sha256': {
            'first_trial': TRIAL_SEMANTIC_SHA256,
            'first_contribution': CONTRIBUTION_SEMANTIC_SHA256,
        },
        'verification_limits': [
            'Fictional school operating path establishes a design-level route, not real-school or specific case-record proof.',
            'All three participation conditions are checked as satisfied in the selected model before T1; exact attendance and supplement records remain unknown.',
            'T1–T2 are locked story events; precise scene actions, dialogue and individual viewpoint execution remain unverified.',
            'Two planned slots do not establish published numbering or whole G13 completion.',
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
        '# A01 두 번째 최종 회차 기능 — T1–T2', '',
        '이 문서는 **원고가 아닌 회차 기능표**다. 첫 기능 A01-EF-001의 제안 종료 뒤, 첫 훈련 진입과 동갑 완패를 한 기능으로 배치한다. 과거 E1 경계 문서의 누적 대안 `E2`(첫 회차 B1–T2)는 채택하지 않았다.', '',
        '- 기능 `A01-EF-002`, A01-S1, 기능 순서/계획 슬롯 2. A01 계획 36슬롯 중 국소 두 기능 배정·잔여 34슬롯. 출판 회차 번호·전체 분량은 미정이다.', '',
        '## 기능·비용·인계', '',
        f"- 시작: {data['entry_state']}",
        f"- 단일 기능: {data['single_function']}",
        f"- 이미 잠긴 참여 선택: {data['unit_choice']}",
        f"- 직접 비용: {data['direct_present_cost']['claim']} 시간 중복 불가는 근거가 표시된 추론이고 완패는 잠긴 사건이다.",
        f"- 끝: {data['exit_state']}",
        f"- 남는 질문: {data['reader_question_at_end']} 다음 C1의 잠긴 사건을 첫 체험 기능 밖에 두는 편집 질문이다.", '',
        *rows, '',
        'E1 종료=이 기능 시작, 이 기능 종료=C1 Blueprint 시작을 문자 단위로 대조한다. C1의 다음 훈련 잔류·첫 리바운드/아웃렛은 이번 기능 밖이다.', '',
        '## 가상학교와 정보 접근', '',
        '- [학교 운영안](A01_TRIAL_SCHOOL_OPERATING_PATH_2026_10_07.md)은 가상학교의 학교 계획·담당권한 분리와 **T1 전 수업 출석·학업보충·시간 준수 세 조건 모두의 확인/충족** 경로를 설계했다. 학업보충을 이후 예정만으로 대체하지 않는다.',
        '- 운영안의 일회 체험 확인은 작품 속 설계 선택이다. 실제 학교나 특정 학생의 기록·개별 허가를 인증하지 않으며 기존 출결 불이익 삭제, 선수등록, 대회 자격을 뜻하지 않는다. 구두 수락·정확 출석/보충 기록·학교명·날짜는 미정이다.',
        '- S1 밀착 3인칭의 기능 단계 접근만 적용한다. 주인공의 참여 동기와 자기 수행·라이벌의 외부 대응을 구분하고 감독/라이벌의 비공개 내면을 알게 하지 않는다. 개별 장면 POV·동작·대사·점수는 미인증이다.', '',
        '## 완료 범위', '',
        '- [첫 체험 Blueprint](A01_FIRST_TRIAL_BLUEPRINT.json)의 2 Beat/3 잠긴 주장과 제한 추론 I1–I3을 구분해 사용했다. 정본 사건 추가·새 작가 잠금은 0건이다.',
        '- 국소 최종 기능 1개를 이번에 배치해 A01 연속 기능은 2개다. 전체 G13/G14, 실제 Pack, G15–G17, 원고 허가는 미완료다. 설계/원고 게이트 `CLOSED`, `manuscript_allowed:false`.',
        '- JSON의 출처 지문과 재구성 검사는 구조·현재성·권한을 검문하며 서술 품질이나 실제 학교 증빙을 보증하지 않는다.', '',
    ])


def validate(data, root=ROOT, currentness=True):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError) as exc:
        return [f'source construction: {exc}']
    errors = [] if data == expected else ['record differs from source-bound E2 function']
    if currentness:
        for unit in ('first-trial', 'first-contribution'):
            _, unit_errors = blueprint_check.check(root=root, unit=unit)
            errors.extend(f'{unit}: {e}' for e in unit_errors)
    return errors


def self_test(data):
    mutations = [
        ('wrong slot', lambda d: d.update(planned_allocation_slot=3)),
        ('altered defeat', lambda d: d['beats'][1].update(function_event='무승부')),
        ('wrong C1 handoff', lambda d: d['next_unit'].update(beat_id='C2')),
        ('missing supplement', lambda d: d['school_authority']['modeled_condition_check'].pop('academic_supplement')),
        ('real school proof', lambda d: d['school_authority'].update(real_school_or_case_records_certified=True)),
        ('private thought', lambda d: d['information_access']['not_available_without_new_access'].clear()),
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
        try:
            saved = load(ROOT, OUTPUT)
            errors.extend(validate(saved))
            if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
                errors.append('Markdown not synchronized')
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f'artifact read: {exc}')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'function': data['episode_function_id'], 'local_complete': 1,
                      'contiguous_functions': 2, 'remaining_planned_slots': 34,
                      'negative_controls': tested, 'current': not errors,
                      'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
