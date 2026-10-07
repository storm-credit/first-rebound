"""Select bounded academic and exam-prep time after school-side referral."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e7_final_episode_function as previous_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_CF08_ACADEMIC_TIME_COST_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A02_CF08_ACADEMIC_TIME_COST_WORKING_MODEL_2026_10_07.md')
SOURCES = (
    'tools/build_a02_cf08_academic_time_cost_working_model.py',
    str(previous_builder.OUTPUT).replace('\\', '/'),
    'design/A02_PREP_CONDITIONAL_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'canon/STORY_BIBLE.md',
    'research/COLLEGE_EXIT_PACKET.md',
    'research/TIMELINE_ELIGIBILITY_LEDGER.md',
    'canon/PROJECT_FREEZE.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF08_PINS = {
    'dominant_function': '학업·시험 준비의 실제 시간 지불',
    'cause': '농구 수행을 남겨도 대학 자격과 입학에 필요한 학업은 별개의 과제로 이어져 왔다',
    'pressure': '평가가 좋아질수록 공부 시간을 농구나 게임에 돌리고 싶지만 졸업·다음 기회를 잃을 수 있다',
    'choice': '담당자의 학사 계획에 맞춰 남은 과목과 시험 준비를 수행한다',
    'direct_cost': '추가 훈련·외출·게임에 쓸 수 있는 시간을 스터디홀과 학습에 쓴다',
    'changed_state': '공부를 좋아해서가 아니라 다음 기회를 보존하려고 학습 의무를 수행한다',
    'next': 'A02-CF09',
    'next_dependency': '학습 수행과 공식 학업·졸업 증빙 처리를 구분해 마감해야 한다',
}


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, previous_builder.OUTPUT)
    candidates = load(root, 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json')
    structure = load(root, 'design/CP2_ACT_SUBACT_PACKET.json')
    college = (root / 'research/COLLEGE_EXIT_PACKET.md').read_text(encoding='utf-8-sig')
    assert not previous_builder.validate(previous, root=root), 'A02 E7 source stale'
    assert previous['episode_function_id'] == 'A02-EF-007'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (16, 43)
    assert previous['next_unit']['candidate_id'] == 'A02-CF08'
    assert previous['next_unit']['candidate_is_executed_here'] is False
    assert previous['next_unit']['academic_study_or_exam_preparation_verified_here'] is False
    assert previous['whole_A02_S3_exit_certified'] is False
    assert previous['manuscript_allowed'] is False
    cf08 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF08')
    assert cf08['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf08['evidence_class'] == 'CANDIDATE'
    assert cf08['selected_event'] is False and cf08['author_locked'] is False
    assert cf08['subact'] == 'A02-S3'
    for key, expected in CF08_PINS.items():
        assert cf08[key] == expected, f'A02-CF08 source {key} changed'
    assert cf08['entry_state'] == '자신이 평가에 보일 수 있는 후보 근거가 단일 하이라이트보다 반복된 역할 수행으로 넓어진다'
    cf09 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF09')
    assert cf09['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf09['selected_event'] is False and cf09['author_locked'] is False
    s3 = next(s for s in structure['subacts'] if s['id'] == 'A02-S3')
    assert s3['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert '2016 봄·가을' in college and 'E/M/S 7개 안전선' in college
    assert '최종 기능' in college and 'NCAA' in college
    hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
              for p in SOURCES}
    return {
        'schema': 'A02_CF08_ACADEMIC_TIME_COST_WORKING_MODEL_V1',
        'status': 'ROUTINE_PREP_ACADEMIC_TIME_COST_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'FICTIONAL_ACADEMIC_OFFICE_PLAN_AND_VISIBLE_STUDY_ONLY_NOT_FINAL_GRADE_OR_NCAA',
        'source_function': 'A02-CF08', 'target_subact': 'A02-S3',
        'prior_A02_E7_exact_full_exit': previous['exit_state'],
        'entry_state': previous['exit_state'],
        'candidate_entry_summary_is_exact_projection': False,
        'single_function': '프렙 추천 자료가 학교 측에서 보내졌더라도 학업은 별도라는 것을 받아들이고, 학업담당의 예비 범주 계획에 따라 허용된 스터디홀·과제·시험 연습에 추가 훈련과 게임에 쓸 수 있던 시간을 실제로 들인다',
        'academic_authority': {
            'fictional_prep_academic_office_sets_category_plan': True,
            'coach_sets_or_certifies_courses_or_grades': False,
            'plan_uses_preliminary_English_math_science_gaps': True,
            'exact_course_ids_units_or_school_grades_selected': False,
            'student_NCAA_full_qualifier_or_Villanova_admission_certified': False,
            'prior_E7_college_receipt_or_response_inferred': False,
        },
        'event_steps': [
            {'id': 'S1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '프렙 학업담당은 앞서 본 예비 감사표의 영어·수학·과학 빈칸 범주에 맞춘 수업·의무 스터디홀과 시험 연습의 순서를 본인에게 안내한다. 주인공은 필요한 공부가 감독의 농구 추천으로 사라지지 않음을 직접 확인한다',
             'observable_result': '주인공이 들은 범주별 할 일과 허용 학습시간은 보이지만 개별 과목명·학점인정·최종 성적은 아직 없다',
             'not_claimed': '감독의 학업결정·정확 SAT 점수·NCAA 인증'},
            {'id': 'S2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'choice_options': ['허용된 추가 개인훈련·게임 시간을 먼저 쓰고 학습을 뒤로 민다', '허용된 학습시간에 남은 과제와 시험 연습을 먼저 한다'],
             'selected_choice': '허용된 학습시간에 남은 과제와 시험 연습을 먼저 한다',
             'action': '주인공은 선택할 수 있는 추가 개인훈련·게임 시간을 줄이고 의무 스터디홀에 앉아 학업담당이 준 영어 읽기 과제와 수학 오답 정리를 수행한 뒤, 별도의 허용 학습시간에도 시험 읽기 연습을 이어 간다',
             'observable_result': '서로 다른 허용 학습시간에 과제와 시험 연습을 실제 수행한 행동은 보이나 공식 학점·시험 결과·반복 장기성적은 아직 보이지 않는다',
             'not_claimed': '정확 과목 이수·SAT 점수 달성·졸업·입학·성실성 완치'},
        ],
        'partial_order': ['A02 E7 school-side referral full exit < academic-office S1 category plan < S2 permitted study and separate exam-prep time < CF09 official academic evidence not executed'],
        'direct_present_cost': '추가 개인훈련이나 게임에 사용할 수 있던 허용 시간을 스터디홀의 영어 읽기·수학 오답 정리와 별도 시험 읽기 연습에 쓴다. 이미 필수인 농구 훈련이나 학사 권한을 감독이 일방 취소하지 않는다.',
        'selected_design_exit_state': '주인공은 학교 측 추천 자료가 보내졌어도 학업담당의 예비 영어·수학·과학 빈칸 계획을 별도 의무로 받아들였다. 추가 개인훈련·게임에 쓸 수 있던 허용 시간을 줄여 스터디홀 과제와 별도 시험 읽기 연습을 실제 수행했지만, 개별 과목 이수·학점·점수·NCAA 자격·대학 입학은 아직 확정되지 않았다.',
        'reader_question_at_end': '쓴 공부 시간이 학교의 공식 학점·졸업 증빙과 자격 검문으로 이어질 수 있는가',
        'next_candidate': {'id': 'A02-CF09', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'official_credits_graduation_or_eligibility_certified_here': False},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['학업담당이 본인에게 안내한 예비 빈칸 범주와 학습시간', '자신이 수행한 두 종류의 과제·시험 연습', '스스로 줄인 선택 가능한 훈련·게임 시간'],
            'not_available_without_access': ['최종 학점·졸업 심사', 'NCAA Eligibility Center 판정', 'Villanova 입학 심사', '대학 자료 수신·비공개 평가'],
            'individual_scene_pov_verified': False, 'exact_dialogue': None,
        },
        'unassigned_details': {'fictional_school_or_staff_name': None, 'exact_date_or_block_clock': None,
                               'course_ids_or_credit_values': None, 'grades_or_SAT_score': None,
                               'exam_attempt_date_or_result': None,
                               'college_reply_or_decision': None},
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'This routine selects visible study time within a fictional academic-office plan; it does not certify final school credits, graduation or NCAA eligibility.',
            'English/math/science are category gaps from the locked prep plan; exact classes, grades, SAT point score and individual transcript remain open.',
            'Optional extra training and games are the time cost; mandatory supervised basketball obligations are not arbitrarily cancelled.',
            'Villanova receipt or reaction to E7 material is not inferred; CF09 formal document processing is separate.',
            'The working model passed independent source and meaning review; a separate final-function review is required before promotion.',
        ],
        'actual_verified_blueprint_created': False, 'final_episode_function_added': 0,
        'whole_A02_S3_exit_certified': False, 'whole_g13_complete': False,
        'whole_g14_complete': False, 'actual_context_packs': 0,
        'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }


def render(data):
    return '\n'.join([
        '# A02 CF08: 학업과 시험 준비의 실제 시간 지불', '',
        '**상태:** `ROUTINE_PREP_ACADEMIC_TIME_COST_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 가상 프렙 학업담당의 예비 범주 계획 아래서 허용 학습시간에 과제·시험 연습을 수행하는 국소 모델이며 독립 원천·의미 검문을 통과했다. 개별 학점·시험 점수·입학을 인증하지 않고 별도 기능 검문 전 기능 수를 늘리지 않는다.', '',
        '## 보이는 시간 선택', '',
        f"- 정확한 진입: {data['entry_state']}",
        f"- 기능: {data['single_function']}",
        f"- S1: {data['event_steps'][0]['action']} → {data['event_steps'][0]['observable_result']}",
        f"- S2: {data['event_steps'][1]['action']} → {data['event_steps'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 국소 출구: {data['selected_design_exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 학사 권한과 한계', '',
        '- 학교 학업담당은 범주별 공부 계획만 안내한다. 감독은 과목·점수·NCAA 자격을 확정할 수 없고, E7 자료의 대학 수신도 확인되지 않았다.',
        '- 영어·수학·과학은 부족분 범주이며 정확 과목·학점·성적·시험 점수는 정하지 않는다. CF09 공식 증빙과 전체 S3/G13은 미완료다.',
        '- 최종 기능·Context Pack·원고0, 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound CF08 working model']


def self_test(data):
    mutations = [
        ('coach certifies credits', lambda d: d['academic_authority'].update(coach_sets_or_certifies_courses_or_grades=True)),
        ('claim final credits', lambda d: d['academic_authority'].update(exact_course_ids_units_or_school_grades_selected=True)),
        ('claim NCAA', lambda d: d['academic_authority'].update(student_NCAA_full_qualifier_or_Villanova_admission_certified=True)),
        ('claim college receipt', lambda d: d['academic_authority'].update(prior_E7_college_receipt_or_response_inferred=True)),
        ('execute CF09', lambda d: d['next_candidate'].update(official_credits_graduation_or_eligibility_certified_here=True)),
        ('invent SAT result', lambda d: d['unassigned_details'].update(grades_or_SAT_score=1320)),
        ('claim full S3', lambda d: d.update(whole_A02_S3_exit_certified=True)),
        ('promote function', lambda d: d.update(final_episode_function_added=1)),
        ('authorize manuscript', lambda d: d.update(manuscript_allowed=True)),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_load = load
    for name, key, value in [
        ('same-ID automatic admission', 'choice', '시험 없이 감독 추천으로 바로 입학한다'),
        ('same-ID perfect GPA', 'changed_state', '하루 공부한 뒤 모든 학점과 SAT 1320이 확정된다'),
        ('same-ID rescind cost', 'direct_cost', '이미 받은 장학금이 취소된다'),
    ]:
        def changed_load(root, path):
            source = original_load(root, path)
            if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A02-CF08')[key] = value
            return source
        with patch(__name__ + '.load', side_effect=changed_load):
            assert validate(data), name
    return len(mutations) + 3


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
