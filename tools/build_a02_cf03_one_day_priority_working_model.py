"""Select one bounded prep day of obligations before gaming after a lost window."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_cf02_lost_help_window_working_model as prior_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_CF03_ONE_DAY_PRIORITY_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A02_CF03_ONE_DAY_PRIORITY_WORKING_MODEL_2026_10_07.md')
SOURCES = (
    'tools/build_a02_cf03_one_day_priority_working_model.py',
    str(prior_builder.OUTPUT).replace('\\', '/'),
    'design/A02_PREP_CONDITIONAL_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'canon/STORY_BIBLE.md',
    'research/COLLEGE_EXIT_PACKET.md',
    'canon/PROJECT_FREEZE.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF03_PINS = {
    'dominant_function': '의무를 먼저 하는 자기 순서',
    'cause': '한 차례 기회 상실 뒤에도 게임 취미와 즉시 보상의 매력은 남는다',
    'pressure': '다음 의무를 지키려면 다른 사람이 깨우거나 챙겨 주는 데만 기댈 수 없다',
    'choice': '기상·스터디홀·훈련을 먼저 맞추고 남은 시간에 게임을 즐기는 순서를 직접 실행해 본다',
    'direct_cost': '원하는 때 바로 게임을 시작하고 계속할 자유를 줄인다',
    'changed_state': '다음 출전·졸업 기회를 보존하려고 자기 시간을 조절하는 행동이 생긴다',
    'next': 'A02-CF04',
    'next_dependency': '생활 순서의 개선이 현재 농구 수행을 대신해 주지는 않는다',
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
    assert not prior_builder.validate(previous, root=root), 'CF02 source stale'
    assert previous['status'] == 'ROUTINE_ONE_LOST_SUPPORT_WINDOW_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert previous['lost_opportunity_kind'] == 'FICTIONAL_SCHEDULED_ACADEMIC_HELP_FOLLOWUP_ONE_WINDOW'
    assert previous['next_candidate']['one_missed_window_retroactively_recovered'] is False
    assert previous['next_candidate']['habit_correction_executed_here'] is False
    assert previous['final_episode_function_added'] == 0
    assert previous['manuscript_allowed'] is False
    cf03 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF03')
    assert cf03['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf03['evidence_class'] == 'CANDIDATE'
    assert cf03['selected_event'] is False and cf03['author_locked'] is False
    assert cf03['subact'] == 'A02-S1'
    for key, expected in CF03_PINS.items():
        assert cf03[key] == expected, f'A02-CF03 source {key} changed'
    s1 = next(s for s in structure['subacts'] if s['id'] == 'A02-S1')
    assert s1['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert '먼저 해야 할 일을 마친 뒤 즐기는 방식으로 순서를 바꾼다' in responsibility
    assert '기숙사와 의무 스터디홀' in college
    hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
              for p in SOURCES}
    return {
        'schema': 'A02_CF03_ONE_DAY_PRIORITY_WORKING_MODEL_V1',
        'status': 'ROUTINE_ONE_DAY_OBLIGATION_PRIORITY_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'FICTIONAL_PREP_ONE_DAY_TIME_CHOICE_NOT_HABIT_CURE_OR_ELIGIBILITY',
        'source_function': 'A02-CF03', 'target_subact': 'A02-S1',
        'prior_CF02_full_exit': previous['selected_design_exit_state'],
        'entry_state': previous['selected_design_exit_state'],
        'lost_CF02_help_window_restored': False,
        'single_function': '지나간 도움 시간을 지우지 않은 채, 다음 허용 하루에는 스스로 기상·의무 스터디홀·허용된 기본 훈련을 먼저 맞추고 남은 시간에만 게임한다',
        'institutional_day_path': {
            'fictional_prep_study_hall_required_in_school_type': True,
            'fictional_coach_supervised_basic_practice_access_working_selection': True,
            'team_roster_or_game_authorization_certified': False,
            'study_hall_or_practice_exact_clock_selected': False,
            'school_authority_discards_CF02_missed_help_window': False,
        },
        'event_steps': [
            {'id': 'P1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '주인공이 다음 허용 하루의 학교 안내에 있는 의무 스터디홀과 감독 허용 기본 훈련 범위를 확인하고, 그날은 다른 사람의 기상 확인을 기다리지 않고 스스로 일어난다',
             'observable_result': '자기에게 열린 그날의 의무와 시작 순서를 직접 인지한다',
             'not_claimed': '실제 학교 출석기록·종일 생활 규율 완성·공식 팀 등록'},
            {'id': 'P2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'choice_options': ['게임을 먼저 시작하고 의무를 다시 미룬다', '스터디홀과 허용 기본 훈련을 먼저 하고 남은 시간에 게임한다'],
             'selected_choice': '스터디홀과 허용 기본 훈련을 먼저 하고 남은 시간에 게임한다',
             'action': '그날의 의무 스터디홀과 감독이 허용한 기본 훈련을 각각 마친 뒤 남는 시간이 있을 때 게임을 시작한다',
             'observable_result': '한 번의 학교·훈련 의무 우선 행동은 보이지만 CF02에서 놓친 도움 시간은 돌아오지 않는다',
             'not_claimed': '반복 습관 정착·학점 충족·기술 숙련·경기 출전·게임 취미 폐기'},
        ],
        'partial_order': ['CF02 full exit < P1 self-wake and read permitted day obligations < both study hall and supervised basic practice < optional game in remaining time; school block order unassigned'],
        'direct_present_cost': '즉시 게임을 시작하고 계속할 자유를 그날의 의무가 끝날 때까지 줄인다. 이미 놓친 한 번의 도움 시간은 보상으로 되돌리지 않는다.',
        'selected_design_exit_state': '주인공은 앞서 잃은 학업 도움 시간을 되돌리지 못한 채, 다음 허용 하루에는 스스로 일어나 의무 스터디홀과 허용 기본 훈련을 먼저 맞춘 다음 남는 시간에만 게임했다. 이 한 번의 선택은 장기 습관·학업 자격·농구 수행 완성을 증명하지 않는다.',
        'reader_question_at_end': '자기 시간의 한 번 순서 변경이 프렙에서 필요한 농구 위치·판단 기술까지 채울 수 있는가',
        'next_candidate': {'id': 'A02-CF04', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'basketball_position_performance_verified_here': False},
        'relative_time': {'after_CF02_lost_window': True,
                          'within_A02_S1_window': '2016.03–2017.06',
                          'exact_date_or_sequence_of_school_blocks': None},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['스스로 본 학교 일정', '감독에게 허용받은 해당 기본 훈련 범위', '자신의 기상·참여·게임 시작 순서'],
            'not_available_without_access': ['비공개 학업 판단', '감독의 내면 평가', '실제 NCAA 자격', '경기 출전·미래 능력'],
            'individual_scene_pov_verified': False, 'exact_dialogue': None,
        },
        'institutional_limits': {
            'fictional_adviser_controls_study_support_not_NCAA_certificate': True,
            'fictional_coach_grants_one_supervised_skill_session_not_roster_or_game': True,
            'individual_attendance_or_grade_certified': False,
            'team_registration_or_minutes_certified': False,
            'NCAA_full_qualifier_or_graduation_certified': False,
            'actual_real_prep_or_student_case_certified': False,
        },
        'unassigned_details': {'fictional_school_or_staff_name': None,
                               'exact_block_times_or_date': None,
                               'course_or_training_drill': None,
                               'one_day_game_minutes': None,
                               'attendance_or_grade_record': None,
                               'roster_or_game_status': None},
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'CF02 single lost academic-help window remains lost; one new day is not retroactive cure.',
            'The school type supports mandatory study hall, but exact local clock and individual attendance record remain unverified.',
            'The fictional coach allows one supervised basic session only; roster and game participation remain unassigned.',
            'One day of obligation-first behavior does not prove habit cure, academic qualification or basketball skill growth.',
            'Independent review is required before local Blueprint or final function promotion.',
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
        '# A02 CF03: 의무를 먼저 하는 허용 하루', '',
        '**상태:** `ROUTINE_ONE_DAY_OBLIGATION_PRIORITY_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. [CF02](A02_CF02_LOST_HELP_WINDOW_WORKING_MODEL_2026_10_07.md)에서 놓친 예약 학업 도움 시간 한 번은 되돌리지 않는다. 기존 책임 아크의 시간 순서 변경을 한 허용 하루로만 구체화한 가상 설계이며 독립 원천·의미 검문을 통과했다.', '',
        '## 한 번의 순서', '',
        f"- 진입: {data['prior_CF02_full_exit']}",
        f"- 기능: {data['single_function']}",
        f"- P1: {data['event_steps'][0]['action']} → {data['event_steps'][0]['observable_result']}",
        f"- P2: {data['event_steps'][1]['action']} → {data['event_steps'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 국소 출구: {data['selected_design_exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 권한과 한계', '',
        '- 가상 학교 유형의 의무 스터디홀과 감독이 허용한 해당 기본 훈련만 사용한다. 실제 학교 출석기록, 정식 농구 등록·경기 출전, 개별 학점·졸업·NCAA 판정은 인증하지 않는다.',
        '- 게임을 끊거나 성적 우등생·완성 선수로 바뀌지 않는다. 한 번 의무를 앞세운 행동만 보인다. 다음 A02-CF04의 위치·판단 수행은 아직 미실행이다.',
        '- 국소 Blueprint·최종 기능·Context Pack·원고0, 전체 G13 미완, 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound CF03 working model']


def self_test(data):
    mutations = [
        ('recover prior lost window', lambda d: d.update(lost_CF02_help_window_restored=True)),
        ('claim team game registration', lambda d: d['institutional_limits'].update(team_registration_or_minutes_certified=True)),
        ('claim NCAA decision', lambda d: d['institutional_limits'].update(NCAA_full_qualifier_or_graduation_certified=True)),
        ('claim habit cure', lambda d: d.update(selected_design_exit_state='습관을 영구 완치하고 농구 기술을 완성했다')),
        ('claim CF04 performance', lambda d: d['next_candidate'].update(basketball_position_performance_verified_here=True)),
        ('claim actual attendance', lambda d: d['institutional_limits'].update(individual_attendance_or_grade_certified=True)),
        ('claim full S1', lambda d: d.update(whole_A02_S1_exit_certified=True)),
        ('claim final function', lambda d: d.update(final_episode_function_added=1)),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_load = load
    for name, key, value in [
        ('same-ID games first reversal', 'choice', '의무를 더 미루고 종일 게임한다'),
        ('same-ID automatic qualifier reversal', 'changed_state', '한 번 순서를 지켜 NCAA 자격과 농구 기술이 확정된다'),
    ]:
        def changed_load(root, path):
            source = original_load(root, path)
            if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A02-CF03')[key] = value
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
    print(json.dumps({'status': data['status'], 'final_episode_function_added': 0,
                      'negative_controls': tested, 'current': not errors, 'errors': errors},
                     ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
