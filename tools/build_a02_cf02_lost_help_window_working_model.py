"""Select one bounded prep opportunity lost to gaming and sleep after academic help."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_cf01_academic_help_working_model as prior_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_CF02_LOST_HELP_WINDOW_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A02_CF02_LOST_HELP_WINDOW_WORKING_MODEL_2026_10_07.md')
SOURCES = (
    'tools/build_a02_cf02_lost_help_window_working_model.py',
    str(prior_builder.OUTPUT).replace('\\', '/'),
    'design/A02_PREP_CONDITIONAL_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'canon/STORY_BIBLE.md',
    'research/COLLEGE_EXIT_PACKET.md',
    'canon/PROJECT_FREEZE.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF02_PINS = {
    'dominant_function': '게임·수면 실패의 기회 상실',
    'cause': '도움을 요청했어도 한국의 익숙한 사람과 외부 관리가 약해진 환경에서 즉시 게임 보상에 흔들린다',
    'pressure': '게임을 더 이어 가면 수면과 다음 의무에 필요한 준비를 뒤로 밀게 된다',
    'choice': '게임을 계속하며 수면·의무 준비를 뒤로 미뤄 한 차례 실제 기회를 놓친다',
    'direct_cost': '게임을 계속하고 수면·의무 준비를 미룬 행동 때문에 한 차례 참여할 의무 기회를 놓친다',
    'changed_state': '정시에 참여했어야 할 의무를 놓친 경험이 남고 기존 시간 습관의 비용을 마주한다',
    'next': 'A02-CF03',
    'next_dependency': '실제 잃은 기회를 지운 보상 대신 다음 준비를 선택해야 한다',
}


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, prior_builder.OUTPUT)
    candidates = load(root, 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json')
    structure = load(root, 'design/CP2_ACT_SUBACT_PACKET.json')
    responsibility = (root / 'canon/CHARACTER_RESPONSIBILITY_ARC.md').read_text(encoding='utf-8-sig')
    college = (root / 'research/COLLEGE_EXIT_PACKET.md').read_text(encoding='utf-8-sig')
    assert not prior_builder.validate(previous, root=root), 'reviewed CF01 source stale'
    assert previous['status'] == 'ROUTINE_PREP_ACADEMIC_HELP_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert previous['final_episode_function_added'] == 0
    assert previous['A02_S1_whole_entry_or_exit_certified'] is False
    assert previous['bridge_real_case_certified'] is False
    assert previous['manuscript_allowed'] is False
    cf02 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF02')
    assert cf02['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf02['evidence_class'] == 'CANDIDATE'
    assert cf02['selected_event'] is False and cf02['author_locked'] is False
    assert cf02['subact'] == 'A02-S1'
    for key, expected in CF02_PINS.items():
        assert cf02[key] == expected, f'A02-CF02 source {key} changed'
    s1 = next(s for s in structure['subacts'] if s['id'] == 'A02-S1')
    assert s1['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert s1['window'] == '2016.03–2017.06'
    assert '한 차례 실제 기회 상실' in responsibility
    assert '기숙사와 의무 스터디홀' in college
    hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
              for p in SOURCES}
    return {
        'schema': 'A02_CF02_LOST_HELP_WINDOW_WORKING_MODEL_V1',
        'status': 'ROUTINE_ONE_LOST_SUPPORT_WINDOW_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'FICTIONAL_PREP_ONE_SCHEDULED_HELP_OPPORTUNITY_NOT_PUNISHMENT_OR_ELIGIBILITY',
        'source_function': 'A02-CF02', 'target_subact': 'A02-S1',
        'prior_CF01_full_exit': previous['selected_design_exit_state'],
        'entry_state': previous['selected_design_exit_state'],
        'single_function': '게임의 즉시 보상으로 수면·다음 의무를 미뤄, 요청해 둔 학업 도움의 한 번 정해진 기회를 실제로 놓친다',
        'lost_opportunity_kind': 'FICTIONAL_SCHEDULED_ACADEMIC_HELP_FOLLOWUP_ONE_WINDOW',
        'lost_opportunity_scope': '요청 뒤 배정된 첫 후속 도움 시간 한 번은 지나가며 그 시간을 소급 사용하지 못한다. 이후 도움 자체의 영구 박탈이나 학업 자격 실패는 아니다.',
        'event_steps': [
            {'id': 'W1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '가상 프렙 학업 담당자가 앞선 도움 요청에 이어 다음 학업 지원 확인 시간을 하나 정하고 주인공에게 알린다',
             'observable_result': '주인공에게 지켜야 할 한 번의 정해진 지원 기회가 보인다',
             'not_claimed': '실재 학생 상담기록·정확 시간표·과목 판정·유일한 평생 도움 기회'},
            {'id': 'W2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'choice_options': ['게임을 멈추고 수면·다음 의무를 준비한다', '한 판을 더 이어 가고 수면·다음 의무 준비를 미룬다'],
             'selected_choice': '한 판을 더 이어 가고 수면·다음 의무 준비를 미룬다',
             'action': '그날 게임을 더 이어 가면서 스스로 정해 둔 수면·다음 날 준비 시점을 넘긴다',
             'observable_result': '다음 학업 지원 약속에 정시에 참여할 준비를 잃는다',
             'not_claimed': '게임 중독 진단·강제 야간 규정 위반·생활 전체 재발'},
            {'id': 'W3', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '다음 날 예약된 도움 시간 뒤에 깨어 정시 참석을 놓쳤음을 자기 일정에서 확인한다',
             'observable_result': '한 차례 실제 지원 기회를 잃은 사실과 자신이 미룬 수면·준비의 비용이 남는다',
             'not_claimed': '정확 지각 분·학교 징계·성적 하락·팀 명단/출전시간 박탈'},
        ],
        'direct_present_cost': '앞서 직접 요청해 배정받은 지원 시간 한 번을 게임 뒤 수면·준비 실패로 잃는다. 그 시간의 소급 복구는 없다.',
        'selected_design_exit_state': '주인공은 게임을 더 이어 가며 수면·다음 의무를 미뤄, 스스로 요청한 학업 지원 시간 한 번에 정시로 참여하지 못했다. 그 기회는 지나갔고 다음 의무를 먼저 지키는 습관은 아직 생기지 않았다.',
        'reader_question_at_end': '다음 정해진 의무 앞에서는 게임보다 먼저 자기 시간을 지킬 수 있는가',
        'next_candidate': {'id': 'A02-CF03', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'one_missed_window_retroactively_recovered': False,
                           'habit_correction_executed_here': False},
        'relative_time': {'after_CF01_help_request': True,
                          'within_A02_S1_window': '2016.03–2017.06',
                          'exact_days_or_clock_times': None},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['자신이 요청한 후속 시간의 안내', '자신의 게임·수면 선택', '정시 참여 실패와 지난 한 번의 시간'],
            'not_available_without_access': ['담당자의 비공개 평가', '학교의 미발표 징계', 'NCAA 자격 판정', '미래 팀 명단과 출전시간'],
            'individual_scene_pov_verified': False, 'exact_dialogue': None,
        },
        'institutional_limits': {
            'prep_adviser_can_schedule_fictional_followup': True,
            'one_window_lost_is_permanent_help_denial': False,
            'school_discipline_or_actual_attendance_record_certified': False,
            'individual_grade_or_credit_affected_certified': False,
            'basketball_eligibility_or_minutes_affected_certified': False,
            'NCAA_full_qualifier_decision_certified': False,
            'real_prep_or_student_case_certified': False,
        },
        'unassigned_details': {
            'fictional_prep_or_staff_name': None, 'course_or_subject': None,
            'appointment_day_or_time': None, 'exact_game_duration_or_sleep_hours': None,
            'lateness_minutes_or_school_record': None, 'next_help_appointment': None,
            'discipline_or_game_restriction': None, 'grade_or_roster_consequence': None,
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'One requested help follow-up is a new routine fictional design within the existing single lost opportunity arc.',
            'The appointment is neither the fictional school final graduation audit nor a real student record.',
            'The single missed window is not restored, while later help and eligibility remain open.',
            'CF03 later habit action, school discipline, games, scores and playing time are not executed or certified.',
            'Independent review is required before Blueprint or final function promotion.',
        ],
        'actual_verified_blueprint_created': False,
        'final_episode_function_added': 0,
        'whole_A02_S1_exit_certified': False, 'whole_g13_complete': False,
        'whole_g14_complete': False, 'actual_context_packs': 0,
        'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }


def render(data):
    return '\n'.join([
        '# A02 CF02: 게임 뒤 잃은 한 번의 학업 도움 시간', '',
        '**상태:** `ROUTINE_ONE_LOST_SUPPORT_WINDOW_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 기존 [CF02 후보](A02_PREP_CONDITIONAL_FUNCTIONS.md)의 한 차례 실제 기회 상실을 가상 프렙의 예약된 학업 도움 시간 한 번으로 구현한 일상 설계다. 부모의 원천·의미 독립 검문을 통과했다. 실제 기록·최종 기능·원고가 아니다.', '',
        '## 인과와 현재 비용', '',
        f"- CF01 정확 출구: {data['prior_CF01_full_exit']}",
        f"- 한 기능: {data['single_function']}",
        f"- W1: {data['event_steps'][0]['action']} → {data['event_steps'][0]['observable_result']}",
        f"- W2: {data['event_steps'][1]['action']} → {data['event_steps'][1]['observable_result']}",
        f"- W3: {data['event_steps'][2]['action']} → {data['event_steps'][2]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 국소 출구: {data['selected_design_exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 범위', '',
        '- 잃은 것은 주인공이 직접 요청했던 예약 도움 시간 **한 번**이다. 놓친 시간을 소급해 쓰지 않지만 이후 도움을 영구 박탈하거나 학점·졸업·NCAA 자격을 실패로 확정하지 않는다.',
        '- 가상 학교 학업 담당자는 후속 시간을 안내할 수 있다. 감독/담당자가 성적·졸업·NCAA 인증을 대신 결정하지 않는다. 정확 시간·과목·기숙사 규율 위반·징계·팀 명단·출전시간은 미정이다.',
        '- 다음 CF03의 자기 시간 순서 개선은 여기서 실행하지 않는다. 실제 학교/학생 기록·국소 Blueprint·최종 기능·Context Pack·원고0, 전체 G13 미완, 게이트 `CLOSED`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound CF02 working model']


def self_test(data):
    mutations = [
        ('erase missed window', lambda d: d['next_candidate'].update(one_missed_window_retroactively_recovered=True)),
        ('prepay habit correction', lambda d: d['next_candidate'].update(habit_correction_executed_here=True)),
        ('invent real case', lambda d: d['institutional_limits'].update(real_prep_or_student_case_certified=True)),
        ('invent graduation ruling', lambda d: d['institutional_limits'].update(individual_grade_or_credit_affected_certified=True)),
        ('invent roster consequence', lambda d: d['institutional_limits'].update(basketball_eligibility_or_minutes_affected_certified=True)),
        ('invent permanent help denial', lambda d: d['institutional_limits'].update(one_window_lost_is_permanent_help_denial=True)),
        ('invent hours', lambda d: d['unassigned_details'].update(exact_game_duration_or_sleep_hours=3)),
        ('false final function', lambda d: d.update(final_episode_function_added=1)),
        ('false whole S1', lambda d: d.update(whole_A02_S1_exit_certified=True)),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_load = load
    for name, key, value in [
        ('same-ID no missed chance reversal', 'choice', '게임을 멈추고 정해진 의무에 모두 참여한다'),
        ('same-ID punishment inflation', 'direct_cost', '영구 퇴학과 NCAA 자격 상실'),
    ]:
        def changed_load(root, path):
            source = original_load(root, path)
            if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A02-CF02')[key] = value
            return source
        with patch(__name__ + '.load', side_effect=changed_load):
            assert validate(data), name
    return len(mutations) + 2


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
    print(json.dumps({'status': data['status'], 'lost_opportunity_kind': data['lost_opportunity_kind'],
                      'final_episode_function_added': 0, 'negative_controls': tested,
                      'current': not errors, 'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
