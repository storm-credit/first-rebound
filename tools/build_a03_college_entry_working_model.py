"""Select a bounded fictional A02→A03 registration and first practice role trial."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e10_final_episode_function as e10_builder
import build_a02_cf10_college_transition_working_model as college_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A03_COLLEGE_ENTRY_WORKING_MODEL_2026_10_07.json')
MARKDOWN = OUTPUT.with_suffix('.md')
E10 = str(e10_builder.OUTPUT).replace('\\', '/')
COLLEGE = str(college_builder.OUTPUT).replace('\\', '/')
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
A03_CANDIDATES = 'design/A03_CONDITIONAL_EPISODE_FUNCTIONS.json'
SCOPE_GATE = 'control/COLLEGE_ARC_SCOPE_GATE.md'
COLLEGE_EXIT = 'research/COLLEGE_EXIT_PACKET.md'
ROTATION = 'research/VILLANOVA_ELIGIBILITY_ROTATION_MODEL.md'
SKILL = 'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md'
SOURCES = ('tools/build_a03_college_entry_working_model.py', E10, COLLEGE, CP2,
           A03_CANDIDATES, SCOPE_GATE, COLLEGE_EXIT, ROTATION, SKILL)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def source_bytes(root, path):
    target = Path(path)
    return (target if target.is_absolute() else root / target).read_bytes()


def normalized_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def build(root=ROOT):
    previous = load(root, E10)
    selected = load(root, COLLEGE)
    cp2 = load(root, CP2)
    candidates = load(root, A03_CANDIDATES)
    assert previous == e10_builder.load(root, e10_builder.OUTPUT), 'E10 input differs from producer source'
    assert selected == college_builder.load(root, college_builder.OUTPUT), 'college input differs from E10 producer source'
    assert not e10_builder.validate(previous, root=root), 'A02 E10 must be source-current'
    assert not college_builder.validate(selected, root=root), 'college I1–I4 must be source-current'
    assert previous['episode_function_id'] == 'A02-EF-010'
    assert previous['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE'
    assert previous['next_unit']['id'] == 'A03-S1'
    assert previous['next_unit']['summer_EC_and_Villanova_compliance_fictional_bridge_selected'] is True
    assert previous['next_unit']['summer_bridge_executed_as_A02_beat'] is False
    assert previous['next_unit']['enrollment_or_official_college_game_executed_here'] is False
    assert previous['whole_g13_complete'] is False and previous['manuscript_allowed'] is False
    assert selected['selected_design_exit_state'] == previous['exit_state']
    i1, i2, i3, i4 = selected['institutional_sequence']
    assert [i['id'] for i in (i1, i2, i3, i4)] == ['I1', 'I2', 'I3', 'I4']
    assert i1['scope'] == i2['scope'] == 'A02_S3'
    assert i1['offer_in_fiction'] and i1['admission_in_fiction']
    assert i2['graduation_in_fiction'] and i2['final_transcript_sent_in_fiction']
    assert i3['scope'] == 'INTER_ACT_INSTITUTIONAL_BRIDGE_NOT_A02_EPISODE_DATE'
    assert i3['eligibility_center_academic_and_athletics_certified_in_fiction'] is True
    assert i3['villanova_compliance_confirmed_in_fiction'] is True
    assert i3['actual_private_ncaa_decision_or_villanova_record_certified'] is False
    assert i4['scope'] == 'A03_ENTRY_PREREQUISITE_NOT_A02_EPISODE_EVENT'
    assert i4['enrollment_or_first_game_executed_here'] is False
    assert i4['starter_or_unrestricted_minutes_guaranteed'] is False
    assert i4['exact_roster_counter_assignment_audited_here'] is False
    assert selected['whole_g13_complete'] is False and selected['manuscript_allowed'] is False
    a03_s1 = next(row for row in cp2['subacts'] if row['id'] == 'A03-S1')
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    assert a03_s1['entry_state'] == '우승팀 소속을 자기 실력과 혼동'
    assert a03_s1['choice'] == '우승팀 소속이라는 이름 대신 자신이 수행할 수 있는 좁은 벤치 역할을 맡는다'
    assert a03_s1['cost'] == '자기 쇼케이스'
    assert a03_s1['exit_state'] == '제한된 역할을 수락'
    assert candidates['status'] == 'THREE_CONDITIONAL_FUNCTIONS_NOT_FINAL_G13'
    assert candidates['final_episode_functions'] == 0
    first_candidate = candidates['functions'][0]
    assert (first_candidate['id'], first_candidate['subact'], first_candidate['function']) == (
        'A03-F01', 'A03-S1', '초기 실패')
    assert first_candidate['status'] == 'CONDITIONAL_EPISODE_FUNCTION_CANDIDATE'
    assert '구체 경기/포제션 HOLD' in first_candidate['observation_limit']
    assert first_candidate['choice'] == '영상으로 자신이 동료에게 넘긴 부담을 확인하고 다음 훈련의 제한 역할을 수락'
    scope = source_bytes(root, SCOPE_GATE).decode('utf-8-sig')
    exit_packet = source_bytes(root, COLLEGE_EXIT).decode('utf-8-sig')
    rotation = source_bytes(root, ROTATION).decode('utf-8-sig')
    assert 'B. 최소 완결' in scope and '대표 경기 기능 | 3개' in scope
    assert '40경기 전체 분·스탯 재계산' in scope
    assert '2017 여름 | Eligibility Center' in exit_packet
    assert '선발 0회' in rotation and '32~36경기' in rotation
    assert '실제 200분 분배' in rotation

    # These are selected fictional routine outcomes after the already selected summer bridge.
    # They do not revise the original I4 record, which describes the earlier A02 boundary.
    sequence = [
        {'id': 'A03-I4-1', 'type': 'FICTIONAL_INSTITUTIONAL_OUTCOME',
         'after': 'I3 selected summer full-qualifier and compliance result',
         'actor': 'FICTIONAL_VILLANOVA_ENROLLMENT_OFFICE',
         'selected_outcome': 'The student is enrolled for the 2017–18 college year after the selected I3 clearance.',
         'student_observable_access': 'The student receives an enrollment-complete notice; no private NCAA rationale or student file is reproduced.',
         'fictional_enrollment_completed': True,
         'real_student_enrollment_or_document_certified': False},
        {'id': 'A03-I4-2', 'type': 'FICTIONAL_TEAM_PRACTICE_ACCESS',
         'after': 'A03-I4-1', 'actor': 'FICTIONAL_VILLANOVA_TEAM_STAFF',
         'selected_outcome': 'The enrolled student is assigned a bounded, supervised reserve-forward practice task.',
         'student_observable_access': 'The protagonist receives only his own task and can observe the practice result.',
         'team_staff_certifies_NCAA_eligibility': False,
         'starter_or_unrestricted_minutes_guaranteed': False,
         'official_game_or_box_score_executed': False},
        {'id': 'A03-R1', 'type': 'ROUTINE_FICTIONAL_FIRST_ROLE_TRIAL',
         'after': 'A03-I4-2',
         'assigned_task': 'In a supervised defensive drill, keep the assigned weak-side help position while a ball-side drive develops.',
         'observable_action': 'He watches the ball first and moves late toward the assigned help position.',
         'observable_result': 'A teammate has to cover the open help space in this drill; no made basket or real-game possession is asserted.',
         'causal_limit': 'The missed assigned cue in this one drill is his visible failure. It does not prove help defense is always wrong or that an A02 drill failed retroactively.',
         'exact_opponent_teammate_coach_quote_or_score': None,
         'historical_villanova_practice_or_game_certified': False},
    ]
    exact_entry = (
        'A02의 봄 오퍼·입학 승인과 5~6월 프렙 졸업·최종 성적표 뒤, 별도로 선택된 여름 I3 자격·컴플라이언스 완료를 거쳐 '
        '가상 Villanova 등록이 실행되었다. 주인공은 선발·공식 출전·역할 안정성을 보장받지 않은 제한 역할 연습에 들어간다.'
    )
    trial_exit = (
        '대학의 첫 허용된 제한 수비 연습에서 주인공은 공을 먼저 보느라 맡은 약한 쪽 도움 위치로 늦게 움직였고, '
        '동료가 빈 공간을 메워야 했다. 그는 자기 과제의 가시적 결함만 확인했으며 출전 분·동료 신뢰·다음 훈련의 수정 성공은 아직 얻지 못했다. '
        '여름 I3의 자격·컴플라이언스 완료는 유지되고, 학기 전체 학업 수행은 이 연습으로 증명되지 않는다.'
    )
    return {
        'schema': 'A03_COLLEGE_ENTRY_WORKING_MODEL_V1',
        'status': 'SELECTED_ROUTINE_FICTIONAL_ENTRY_AND_FIRST_PRACTICE_MODEL_INDEPENDENTLY_REVIEWED',
        'independent_review_completed': True,
        'review_scope': 'FICTIONAL_REGISTRATION_AND_ONE_SUPERVISED_ROLE_FAILURE_ONLY',
        'scope': 'A02_TO_A03_I4_ENROLLMENT_AND_BOUNDED_A03_S1_PRACTICE_CANDIDATE',
        'evidence_classes': {'I1_I3': 'PRIOR_SELECTED_FICTIONAL_DESIGN',
                             'A03_I4_R1': 'NEW_ROUTINE_FICTIONAL_DESIGN_SELECTION',
                             'real_NCAA_or_Villanova_records': 'NOT_CERTIFIED'},
        'prior_A02_E10_exact_full_exit': previous['exit_state'],
        'original_I4_unexecuted_in_A02': copy.deepcopy(i4),
        'new_sequence': sequence,
        'exact_A03_entry_after_fictional_registration': exact_entry,
        'first_local_trial_exit': trial_exit,
        'next_candidate': {'id': 'A03-F01', 'status': 'CONDITIONAL_NOT_FINAL_EPISODE_FUNCTION',
                           'available_next_action': 'Review the visible help-position miss and decide whether to accept a bounded corrective task.',
                           'film_review_or_role_acceptance_executed_here': False,
                           'A03_S1_CP2_exit_certified_here': False},
        'limits': {
            'summer_I3_backdated_as_A02_episode': False,
            '2017_18_official_college_game_or_box_score_completed': False,
            'actual_real_student_case_or_private_NCAA_record_certified': False,
            'selected_I3_full_qualifier_or_compliance_revoked_here': False,
            'exact_roster_counter_assignment_certified': False,
            'starter_or_unrestricted_minutes_guaranteed': False,
            'A03_three_representative_function_cap_changed': False,
            'new_representative_games_added': 0,
            'full_college_season_or_40_game_encyclopedia_completed': False,
            'private_coach_teammate_inner_state_or_quote_certified': False,
            'A03_first_final_episode_function_completed': False,
            'A03_S1_whole_exit_completed': False,
        },
        'author_locked': False, 'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {p: normalized_sha(source_bytes(root, p)) for p in SOURCES},
    }


def render(d):
    lines = ['# A02→A03 가상 대학 등록·첫 제한 역할 연습', '',
             '**범위:** 원고가 아닌 가상 대학 진입 작업모델. A02 E10의 정확 출구 뒤 여름 I3를 별도 인계로 소비하고, A03 등록·첫 허용 연습만 선택한다.', '',
             f"- 상태: `{d['status']}`",
             f"- 진입: {d['exact_A03_entry_after_fictional_registration']}",
             '- 학교 등록은 가상 입학실의 결과이며 농구 코치가 NCAA 자격을 인증하지 않는다. 실제 학생·학교 문서와 개별 환산 결과는 인증하지 않는다.', '',
             '| 순서 | 가상 기능 | 관측 경계 |', '| --- | --- | --- |']
    for step in d['new_sequence']:
        lines.append(f"| {step['id']} | {step.get('selected_outcome', step.get('assigned_task'))} | {step.get('student_observable_access', step.get('observable_result'))} |")
    lines += ['', f"- 첫 국소 연습 출구: {d['first_local_trial_exit']}",
              '- A03-F01의 영상 검토·수정 과제 선택은 다음 단위다. 이번 모델은 A03-S1의 제한 역할 수락이나 공식 경기 출전을 선지급하지 않는다.',
              '- 기존 A03 대표 기능 3개 상한과 선발 0회·후순위 로테이션 경계를 유지한다. 이 기록은 새 대표 경기나 40경기 경기별 기록을 만들지 않는다.',
              '- 가상 기관 등록·연습과 실제 NCAA/Villanova 개인 기록을 구분한다. 학업 성적·장학금 counter·박스스코어·실존 인물 발언을 확정하지 않는다.',
              '- 전체 G13/G14·실제 Context Pack·원고는 미완료, 설계/원고 게이트 `CLOSED`.', '']
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, ValueError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A03 entry model differs from source-bound working selection']


def self_test(data):
    changes = [
        ('prepay official game', lambda x: x['limits'].update({'2017_18_official_college_game_or_box_score_completed': True})),
        ('coach certifies NCAA', lambda x: x['new_sequence'][1].update(team_staff_certifies_NCAA_eligibility=True)),
        ('claim real private record', lambda x: x['limits'].update(actual_real_student_case_or_private_NCAA_record_certified=True)),
        ('revoke selected I3 certification', lambda x: x['limits'].update(selected_I3_full_qualifier_or_compliance_revoked_here=True)),
        ('prepay A03 S1 exit', lambda x: x['next_candidate'].update(A03_S1_CP2_exit_certified_here=True)),
        ('turn practice into history', lambda x: x['new_sequence'][2].update(historical_villanova_practice_or_game_certified=True)),
    ]
    for name, mutate in changes:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_load = load
    for name, path, mutate in [
        ('I3 certification removed', COLLEGE, lambda x: x['institutional_sequence'][2].update(villanova_compliance_confirmed_in_fiction=False)),
        ('I4 prepaid in A02', COLLEGE, lambda x: x['institutional_sequence'][3].update(enrollment_or_first_game_executed_here=True)),
        ('A03 F01 made final', A03_CANDIDATES, lambda x: x['functions'][0].update(status='FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE')),
        ('A03 F01 same-key role refusal', A03_CANDIDATES,
         lambda x: x['functions'][0].update(choice='영상으로 동료에게 넘긴 부담을 보고도 다음 훈련의 제한 역할을 거부하고 무제한 출전을 요구한다')),
    ]:
        def changed_load(root, requested, path=path, mutate=mutate):
            source = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                source = copy.deepcopy(source)
                mutate(source)
            return source
        with patch(__name__ + '.load', side_effect=changed_load):
            assert validate(data), name
    return len(changes) + 4


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
    print(json.dumps({'current': not errors, 'errors': errors, 'negative_controls': tested,
                      'status': data['status']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
