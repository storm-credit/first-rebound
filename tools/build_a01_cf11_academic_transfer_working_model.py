"""Select a bounded CF11 inquiry, without certifying prep admission or credits."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a01_e7_final_episode_function as e7


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_CF11_ACADEMIC_TRANSFER_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A01_CF11_ACADEMIC_TRANSFER_WORKING_MODEL_2026_10_07.md')
SOURCES = (
    'tools/build_a01_cf11_academic_transfer_working_model.py',
    'design/A01_E7_FINAL_EPISODE_FUNCTION.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/STORY_BIBLE.md',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'canon/CAREER_TIMELINE.md',
    'canon/PROJECT_FREEZE.md',
    'research/TIMELINE_ELIGIBILITY_LEDGER.md',
    'AGENTS.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF11_PINS = {
    'function': '학업·이동 조건의 직접 확인과 준비',
    'cause': '농구 과제로 이동을 생각해도 학생 신분과 실제 이동 조건은 별개로 남는다',
    'pressure': '낮은 성적·수업 회피 습관이 필요한 학업과 서류 준비를 면제하지 않는다',
    'choice': '학업·서류 준비를 요구받아 설명을 들으며 본인이 확인할 항목을 정리하고 불명확한 조건을 질문한다',
    'cost': '농구만 하거나 게임을 즐길 시간을 불편한 준비 설명을 듣고 질문하는 데 쓴다',
    'changed_state': '자신이 할 준비와 아직 타인의 답이 필요한 항목을 구분하는 후보 행동이 생긴다',
    'next': 'A01-CF12',
}


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, e7.OUTPUT)
    candidates = load(root, 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json')
    packet = load(root, 'design/CP2_ACT_SUBACT_PACKET.json')
    story = (root / 'canon/STORY_BIBLE.md').read_text(encoding='utf-8-sig')
    responsibility = (root / 'canon/CHARACTER_RESPONSIBILITY_ARC.md').read_text(encoding='utf-8-sig')
    career = (root / 'canon/CAREER_TIMELINE.md').read_text(encoding='utf-8-sig')
    freeze = (root / 'canon/PROJECT_FREEZE.md').read_text(encoding='utf-8-sig')
    eligibility = (root / 'research/TIMELINE_ELIGIBILITY_LEDGER.md').read_text(encoding='utf-8-sig')
    assert not e7.validate(previous, root=root), 'E7 source-current function is stale'
    assert previous['episode_function_id'] == 'A01-EF-007'
    assert previous['next_unit']['candidate_id'] == 'A01-CF11'
    assert previous['next_unit']['candidate_is_executed_here'] is False
    assert previous['whole_g13_complete'] is False
    cf11 = next(f for f in candidates['functions'] if f['id'] == 'A01-CF11')
    assert (cf11['status'], cf11['evidence_class'], cf11['selected_event'], cf11['author_locked']) == (
        'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE', 'CANDIDATE', False, False)
    assert cf11['subact'] == 'A01-S3'
    for key, expected in CF11_PINS.items():
        assert cf11[key] == expected, f'CF11 source {key} changed'
    subact = next(s for s in packet['subacts'] if s['id'] == 'A01-S3')
    assert subact['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert subact['window'] == '2015–2016.02'
    assert '학업 습관' in story
    assert '필요한 학업과 서류를 자기 선택의 비용으로 수행한다' in responsibility
    assert '2016.03 | 가상 뉴잉글랜드 보딩 프렙 중도 편입·학점 감사' in career
    assert '개별 과목의 NCAA 환산은 `HOLD`' in freeze
    assert '주인공의 한국 고교→미국 프렙 학점 이전과 2017 졸업 인정 방식' in eligibility
    source_hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
                     for p in SOURCES}
    return {
        'schema': 'A01_CF11_ACADEMIC_TRANSFER_WORKING_MODEL_V1',
        'status': 'ROUTINE_ACADEMIC_INQUIRY_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'FICTIONAL_PRE_TRANSFER_INQUIRY_NOT_RECORD_ISSUANCE_OR_ADMISSION',
        'source_function': 'A01-CF11', 'target_subact': 'A01-S3',
        'entry_state': previous['exit_state'],
        'prior_S2_whole_subact_exit_certified': False,
        'S3_full_entry_or_exit_certified': False,
        'existing_locked_route': '한국 고1 후 2016년 3월 가상 뉴잉글랜드 보딩 프렙 편입 방향',
        'routine_choice_versus_locked_fact': {
            'locked_fact': 'The March 2016 move to a fictional New England boarding prep remains the chosen route.',
            'new_design_choice': 'Ask the current Korean school about its own record categories and separate self tasks from questions for the future prep.',
            'new_author_lock': False,
            'actual_prep_admission_selected': False,
        },
        'fictional_school_contact': {
            'classification': 'ROUTINE_FICTIONAL_DESIGN',
            'role': '기존 한국 고교의 학사 담당자',
            'authority_limited_to': '그 한국 고교가 설명할 수 있는 국내 출결·이수 기록 확인과 발급 절차 범주',
            'named_real_school_or_employee': None,
            'may_certify_US_prep_acceptance_or_credit_conversion': False,
            'may_erase_past_attendance_or_grades': False,
            'actual_student_record_access_or_issuance_certified': False,
        },
        'relative_time_window': {
            'after_E7_exit': True,
            'before_locked_2016_03_prep_move': True,
            'exact_day_or_semester_position': None,
            'historical_school_office_appointment_certified': False,
        },
        'single_function': '농구로 정한 이동 이유를 학업·기록 준비와 구분하고, 본인이 확인할 일과 학교 권한자의 답이 필요한 질문을 나눈다',
        'event_steps': [
            {'id': 'A1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '농구나 게임에 쓸 한 기회를 떼어 기존 한국 고교 학사 담당자에게 자기 학교의 출결·이수 기록을 확인하거나 요청하는 일반 범주를 듣는다',
             'observable_result': '국내 학교가 설명할 수 있는 자기 기록 절차와 미국 프렙의 입학·학점 인정 권한이 다른 곳에 있음을 확인한다',
             'not_claimed': '실제 개인 성적표 발급·결석 삭제·한국 학점의 미국 환산·미국 학교 합격'},
            {'id': 'A2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '자신이 한국 학교에 확인·요청할 기록 항목과 가상 프렙 담당자에게 향후 물어야 할 입학·학점 인정 항목을 나누어 적고, 국내 담당자에게 발급 범위에서 불명확한 점을 질문한다',
             'observable_result': '본인 행동 항목과 아직 해당 학교 권한자의 답을 받지 못한 항목이 구분된 질문 목록을 만든다',
             'not_claimed': '미국 프렙 담당자의 답변·보호자 수락·비자·졸업 감사 완료'},
        ],
        'direct_present_cost': '농구만 하거나 게임을 즐길 수 있는 한 기회를 불편한 국내 기록 설명과 자기 확인 질문에 쓴다.',
        'selected_design_exit_state': '주인공은 국내 학교에 스스로 확인·요청할 출결·이수 기록 범주와 가상 프렙의 권한 있는 답이 필요한 입학·학점 인정 질문을 구분했다. 실제 기록 발급·조건 충족·학교 수락은 아직 확인되지 않았다.',
        'reader_question_at_end': '그는 답이 비어 있는 조건을 안고도 필요한 준비를 계속할 것인가',
        'next_candidate': {'id': 'A01-CF12', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'move_intent_decision_not_executed': True},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['직접 들은 국내 기록 절차의 일반 범주', '자신이 적은 확인 질문', '아직 외부 권한자의 답을 모른다는 점'],
            'not_available_without_access': ['개별 학점 환산', '프렙 비공개 입학 판단', '보호자 선택', '실제 학생기록 처리 결과'],
            'individual_scene_pov_verified': False, 'exact_dialogue': None,
        },
        'institutional_limits': {
            'real_Korean_school_record_issued_or_verified': False,
            'Korean_attendance_or_grades_retrospectively_changed': False,
            'fictional_US_prep_admission_or_credit_acceptance_certified': False,
            'guardian_consent_or_finance_selected': False,
            'visa_or_NCAA_eligibility_certified': False,
            'US_prep_move_reversed_or_new_destination_selected': False,
        },
        'unassigned_details': {
            'school_name_or_staff_identity': None,
            'individual_grades_or_attendance_days': None,
            'actual_transcript_or_issuance_date': None,
            'US_prep_requirements_or_reply': None,
            'course_credit_conversion': None,
            'guardian_finance_or_consent': None,
            'visa_or_travel_steps': None,
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': source_hashes,
        'verification_limits': [
            'This fictional Korean-school explanation concerns only its own record categories; it does not certify any actual student case or US decision.',
            'The candidate academic and paperwork action is not a verified transcript, credit conversion, admission, visa or NCAA qualifier result.',
            'The already locked March 2016 fictional prep direction remains; no new school or move outcome is selected here.',
            'S2 whole completion and S3 full entry/exit remain unverified; CF12 remains unexecuted.',
            'Independent review accepted this limited inquiry; source-current Blueprint and eighth function require separate validation.',
        ],
        'actual_verified_blueprint_created': False,
        'final_episode_function_added': 0,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'author_locked': False,
        'new_author_decisions': 0, 'manuscript_count': 0,
        'manuscript_allowed': False, 'design_gate': 'CLOSED',
    }


def render(data):
    return '\n'.join([
        '# A01 CF11 학업·이동 조건 문의의 정보 범위', '',
        '**상태:** `ROUTINE_ACADEMIC_INQUIRY_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 이미 승인된 미국 프렙 이동 방향 안에서 국내 기록 설명·질문 행동만 가상 설계한다. 실제 발급·환산·입학·비자·원고 허가가 아니다.', '',
        '## 입력과 한 기능', '',
        f"- E7 전체 종료 입력: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- A1: {data['event_steps'][0]['action']} → {data['event_steps'][0]['observable_result']}",
        f"- A2: {data['event_steps'][1]['action']} → {data['event_steps'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 출구: {data['selected_design_exit_state']}",
        f"- 독자 질문: {data['reader_question_at_end']}", '',
        '## 권한과 인계', '',
        '- 한국 학교 담당자의 설명은 자기 학교 기록 확인·발급 절차 범위의 가상 장면이다. 실제 출결/성적표 발급, 소급 삭제, 미국 프렙 학점 인정은 인증하지 않는다.',
        '- 가상 미국 프렙 담당자의 답변, 보호자 동의·재정, 비자·NCAA 자격은 아직 미확인이다. 학교 실명·개별 과목·점수·정확 날짜도 정하지 않는다.',
        '- CF12 미국행 의사와 미완성 준비의 이월은 조건부 후보다. S2 전체 종료·S3 전체 진입/종료를 이 자료만으로 인증하지 않는다.',
        '- 국소 Blueprint/기능8 추가 0, 전체 G13/G14·실제 Context Pack·원고 미완료, 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound CF11 working model']


def self_test(data):
    mutations = [
        ('false author lock', lambda d: d.update(author_locked=True)),
        ('false eighth function', lambda d: d.update(final_episode_function_added=1)),
        ('false Korean student record', lambda d: d['institutional_limits'].update(real_Korean_school_record_issued_or_verified=True)),
        ('retroactive attendance erasure', lambda d: d['fictional_school_contact'].update(may_erase_past_attendance_or_grades=True)),
        ('false prep credit conversion', lambda d: d['fictional_school_contact'].update(may_certify_US_prep_acceptance_or_credit_conversion=True)),
        ('false prep admission', lambda d: d['institutional_limits'].update(fictional_US_prep_admission_or_credit_acceptance_certified=True)),
        ('false guardian consent', lambda d: d['institutional_limits'].update(guardian_consent_or_finance_selected=True)),
        ('false whole S3', lambda d: d.update(S3_full_entry_or_exit_certified=True)),
        ('execute CF12', lambda d: d['next_candidate'].update(move_intent_decision_not_executed=False)),
        ('false source SHA', lambda d: d['source_rev_sha256'].update({'canon/STORY_BIBLE.md': '0' * 64})),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        assert validate(candidate), name
    original_load = load
    for name, key, value in [
        ('same-ID no-academics choice', 'choice', '농구만 잘하면 모든 서류와 학업은 면제받는다'),
        ('same-ID guaranteed prep approval', 'changed_state', '미국 프렙 입학과 한국 학점 인정이 확정된다'),
    ]:
        def changed_source(root, path):
            source = original_load(root, path)
            if path == 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A01-CF11')[key] = value
            return source
        with patch(__name__ + '.load', side_effect=changed_source):
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
                      'negative_controls': tested, 'current': not errors,
                      'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
