"""Select bounded student-side preparation for later academic verification."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e8_final_episode_function as previous_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_CF09_OFFICIAL_CHECK_PREPARATION_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A02_CF09_OFFICIAL_CHECK_PREPARATION_WORKING_MODEL_2026_10_07.md')
SOURCES = (
    'tools/build_a02_cf09_official_check_preparation_working_model.py',
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
CF09_PINS = {
    'dominant_function': '공식 확인에 필요한 준비와 기한 대응',
    'cause': '수행한 학업이 있어도 최종 성적·졸업·인증의 기관 절차가 남는다',
    'pressure': '자신의 운동능력이나 감독의 추천이 학교와 인증 기관의 확인을 대신하지 않는다',
    'choice': '자신이 준비할 자료를 갖추고 학교·학업 담당자에게 제출과 확인에 필요한 사항을 묻는다',
    'direct_cost': '대학 평가에 들뜨거나 게임을 즐길 시간 대신 불편한 서류 확인과 준비를 한다',
    'changed_state': '자신의 준비와 학교·인증 기관이 처리해야 할 답변을 구분해 대학 절차를 이어 간다',
    'next': 'A02-CF10',
    'next_dependency': '추천·장학 경로와 입학·인증·등록의 권한을 나눈 채 다음 환경을 선택한다',
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
    assert not previous_builder.validate(previous, root=root), 'A02 E8 source stale'
    assert previous['episode_function_id'] == 'A02-EF-008'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (17, 44)
    assert previous['next_unit']['candidate_id'] == 'A02-CF09'
    assert previous['next_unit']['candidate_is_executed_here'] is False
    assert previous['next_unit']['official_credit_graduation_or_eligibility_verified_here'] is False
    assert previous['whole_A02_S3_exit_certified'] is False
    assert previous['manuscript_allowed'] is False
    cf09 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF09')
    assert cf09['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf09['evidence_class'] == 'CANDIDATE'
    assert cf09['selected_event'] is False and cf09['author_locked'] is False
    assert cf09['subact'] == 'A02-S3'
    for key, expected in CF09_PINS.items():
        assert cf09[key] == expected, f'A02-CF09 source {key} changed'
    assert cf09['entry_state'] == '공부를 좋아해서가 아니라 다음 기회를 보존하려고 학습 의무를 수행한다'
    cf10 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF10')
    assert cf10['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf10['selected_event'] is False and cf10['author_locked'] is False
    s3 = next(s for s in structure['subacts'] if s['id'] == 'A02-S3')
    assert s3['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert '졸업장·최종 성적표 제출' in college
    assert 'Eligibility Center 학업·athletics 인증과 Villanova compliance 확인' in college
    assert '정확한 핵심 GPA·SAT 한 점수·Villanova 입학 심사 내부 판단' in college
    hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
              for p in SOURCES}
    return {
        'schema': 'A02_CF09_OFFICIAL_CHECK_PREPARATION_WORKING_MODEL_V1',
        'status': 'ROUTINE_PREP_OFFICIAL_CHECK_PREPARATION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'STUDENT_PREPARATION_AND_SCHOOL_PROCESS_REPLY_NOT_DOCUMENT_ISSUANCE_OR_ELIGIBILITY',
        'source_function': 'A02-CF09', 'target_subact': 'A02-S3',
        'prior_A02_E8_exact_full_exit': previous['exit_state'],
        'entry_state': previous['exit_state'],
        'candidate_entry_summary_is_exact_projection': False,
        'single_function': '실제로 공부한 시간을 공식 학점·졸업·NCAA 확인과 혼동하지 않고, 학생 자신이 준비할 이전 학적·시험·현재 과목 자료의 목록을 정리해 학교 학업담당에게 발급·제출·확인 주체와 기한 범주를 직접 묻는다',
        'authority_map': {
            'student_prepares_request_and_tracks_reply': True,
            'fictional_prep_academic_office_answers_school_process_only': True,
            'prep_coach_issues_final_transcript_or_eligibility': False,
            'school_final_transcript_or_diploma_issued_here': False,
            'NCAA_eligibility_center_certified_here': False,
            'Villanova_admission_or_compliance_decision_here': False,
            'prior_E7_college_receipt_or_reply_inferred': False,
        },
        'event_steps': [
            {'id': 'D1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'choice_options': ['감독 추천과 자기가 공부한 시간을 최종 자격으로 여긴다', '이전 학교기록·현재 학사·시험의 제출 상태를 직접 확인할 목록을 만든다'],
             'selected_choice': '이전 학교기록·현재 학사·시험의 제출 상태를 직접 확인할 목록을 만든다',
             'action': '주인공은 게임이나 추가 훈련에 쓸 수 있는 허용 시간 일부를 써서 이미 보유하거나 요청해야 할 이전 학교 학적, 프렙 현재 과목, 시험 결과의 범주를 나눠 적고 아직 받지 못한 공식 자료는 미확인으로 표시한다',
             'observable_result': '학생 자신이 준비·질문할 목록과 미확인 항목은 보이지만 어떤 공식 성적표·졸업장·NCAA 결과도 발급되거나 통과하지 않았다',
             'not_claimed': '정확 과목/점수·서류 발급·졸업·NCAA 판정'},
            {'id': 'D2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '주인공은 그 목록을 학교 학업담당에게 보여 주고, 누가 마지막 프렙 성적표와 졸업 증빙을 내며 학생은 어떤 이전 기록과 시험 결과를 언제 확인해야 하는지 묻는다. 담당자는 학교가 처리할 발급·제출과 학생이 계속 추적할 미확인 항목의 구분만 알려 준다',
             'observable_result': '주인공은 자신 몫의 준비와 학교·인증기관이 나중에 내려야 할 답변을 구분한다. 정확 날짜, 발급 완료, 대학 판정은 아직 없다',
             'not_claimed': '감독의 학업 인증·공식 NCAA 합격·Villanova 입학승인'},
        ],
        'partial_order': ['A02 E8 study-time full exit < D1 student status checklist < D2 school academic-office process reply < final school/NCAA/college decisions not executed'],
        'direct_present_cost': '추가 개인훈련이나 게임에 쓸 수 있는 허용 시간 일부를, 아직 없는 성적·졸업·시험 확인 항목을 드러내는 목록과 학교 담당자 문의에 쓴다. 이미 받은 오퍼나 자격을 잃는 사건은 만들지 않는다.',
        'selected_design_exit_state': '주인공은 실제 학습 행동과 공식 자격 판정이 다름을 인정해 이전 학적·현재 과목·시험의 확인 목록을 만들고 학교 학업담당에게 발급·제출·추적 주체를 물었다. 자신이 준비할 항목과 학교·NCAA·대학이 훗날 처리할 답변을 구분했지만 최종 성적표·졸업 증빙·자격·입학 결과는 아직 확인하지 못했다.',
        'reader_question_at_end': '준비한 질문과 자료가 실제 학교 증빙·인증·대학의 제한 역할 경로로 언제 이어질 것인가',
        'next_candidate': {'id': 'A02-CF10', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'offer_admission_or_college_role_executed_here': False},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['자신이 만든 미확인 자료 목록', '학교 학업담당에게 직접 들은 발급·제출 절차 구분', '자신이 쓴 시간과 남은 질문'],
            'not_available_without_access': ['학교 최종 졸업 판정', 'NCAA Eligibility Center 내부 판단', 'Villanova 입학·compliance 비공개 결정', '아직 받지 않은 공식 성적표'],
            'individual_scene_pov_verified': False, 'exact_dialogue': None,
        },
        'unassigned_details': {'fictional_school_or_staff_name': None,
                               'exact_submission_or_reply_date': None,
                               'individual_course_or_credit_values': None,
                               'grades_or_test_score': None,
                               'issued_document_number_or_copy': None,
                               'college_reply_or_decision': None},
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'A student checklist and school process answer are visible acts, not proof of a final transcript, diploma or NCAA certification.',
            'The academic office explains its own future issuance/submission process; coach cannot issue credits or decide college admission.',
            'Exact courses, grades, SAT score, document numbers and deadlines remain unselected or unverified.',
            'CF10 offer/admission/role path and the entire A02-S3 exit remain future work.',
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
        '# A02 CF09: 공식 확인을 위한 학생의 자료·기한 질문', '',
        '**상태:** `ROUTINE_PREP_OFFICIAL_CHECK_PREPARATION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 학생이 준비할 항목과 학교·인증기관의 나중 판단을 구분하는 국소 가상 설계이며 독립 원천·의미 검문을 통과했다. 공식 서류 발급이나 자격 통과를 인증하지 않고 별도 기능 검문 전 기능 수를 늘리지 않는다.', '',
        '## 질문을 만드는 행동', '',
        f"- 정확한 진입: {data['entry_state']}",
        f"- 기능: {data['single_function']}",
        f"- D1: {data['event_steps'][0]['action']} → {data['event_steps'][0]['observable_result']}",
        f"- D2: {data['event_steps'][1]['action']} → {data['event_steps'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 국소 출구: {data['selected_design_exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 기관 권한', '',
        '- 학생은 미확인 목록을 만들고 학교 담당자에게 절차를 묻는다. 학교는 장차 성적표·졸업 증빙을 처리하고 NCAA/대학은 별도 결정을 한다. 이 단계에서 실제 발급·제출완료·자격결론은 없다.',
        '- 감독 추천이나 앞선 공부 시간이 학점·입학 인증을 대신하지 않는다. CF10 대학 경로와 전체 S3/G13도 아직 미실행이다.',
        '- 최종 기능·Context Pack·원고0, 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound CF09 working model']


def self_test(data):
    mutations = [
        ('claim diploma issued', lambda d: d['authority_map'].update(school_final_transcript_or_diploma_issued_here=True)),
        ('claim NCAA pass', lambda d: d['authority_map'].update(NCAA_eligibility_center_certified_here=True)),
        ('claim coach credit power', lambda d: d['authority_map'].update(prep_coach_issues_final_transcript_or_eligibility=True)),
        ('claim admission', lambda d: d['authority_map'].update(Villanova_admission_or_compliance_decision_here=True)),
        ('claim college reply', lambda d: d['authority_map'].update(prior_E7_college_receipt_or_reply_inferred=True)),
        ('execute CF10', lambda d: d['next_candidate'].update(offer_admission_or_college_role_executed_here=True)),
        ('invent SAT score', lambda d: d['unassigned_details'].update(grades_or_test_score=1300)),
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
        ('same-ID automatic certification', 'choice', '감독에게 NCAA 자격과 입학을 바로 승인받는다'),
        ('same-ID full diploma', 'changed_state', '당일 최종 졸업장과 SAT 1300을 받는다'),
        ('same-ID scholarship loss', 'direct_cost', '이미 확정된 장학금을 박탈당한다'),
    ]:
        def changed_load(root, path):
            source = original_load(root, path)
            if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A02-CF09')[key] = value
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
