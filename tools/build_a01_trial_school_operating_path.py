"""Select a bounded fictional school operating path for A01's first trial.

This records a routine design model. It does not certify a real school, a
historical student's record, a new author lock, or a final episode function.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_TRIAL_SCHOOL_OPERATING_PATH_2026_10_07.json')
MARKDOWN = Path('design/A01_TRIAL_SCHOOL_OPERATING_PATH_2026_10_07.md')
SOURCES = (
    'tools/build_a01_trial_school_operating_path.py',
    'research/A01_KOREA_2015_SCHOOL_TRIAL_BOUNDARY.json',
    'research/A01_KOREA_2015_SCHOOL_TRIAL_BOUNDARY.md',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.md',
    'design/A01_FIRST_TRIAL_BLUEPRINT.json',
    'canon/STORY_BIBLE.md',
    'canon/CAREER_TIMELINE.md',
)
FACT_PINS = {
    'F03': {'classification': 'FACT', 'source_ids': ['S2'], 'locator': '제3조제3항',
            'statement_ko': '지도자 직무는 훈련계획·지도관리, 대회 지원·인솔, 경기력 분석·훈련일지, 훈련장 안전이다.'},
    'F07': {'classification': 'FACT', 'source_ids': ['S4'], 'locator': '인쇄25·30 / PDF27·32',
            'statement_ko': '학교운동부 운영계획은 학교장 수립과 학교운영위원회 심의, 정규수업 이외 운동 원칙을 명시한다. 특정 시설 부재 종목의 체험학습·결재 예외는 농구에 자동 적용되지 않는다.'},
    'F08': {'classification': 'FACT', 'source_ids': ['S3'], 'locator': '초중등 시행령 제9조; 인쇄86–87 / PDF74–75',
            'statement_ko': '학칙에 교과·수업일수·고사·과정수료 인정 및 학교생활 사항을 기재한다.'},
}
CANDIDATE_PIN = {
    'classification': 'SCHOOL_RULE_CANDIDATE_NOT_AUTHOR_LOCK',
    'statement_ko': '허용된 학교운영계획 안에서 체험 일시·안전수칙·담당교사 확인절차를 전달하고 조건확인 후 실제참가. 감독 단독승인 권한이나 전국 공통 절차로 인증하지 않음.',
    'exact_schedule': None,
    'guardian_consent_form': None,
    'trial_period': None,
    'coach_solo_authority_verified': False,
}


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def verify_research_semantics(research):
    facts = {f['id']: f for f in research['facts']}
    for fact_id, pin in FACT_PINS.items():
        assert {k: facts[fact_id][k] for k in pin} == pin, f'changed primary fact: {fact_id}'
    assert research['school_rule_candidate'] == CANDIDATE_PIN, 'changed school rule candidate'


def build(root=ROOT):
    research = load(root, 'research/A01_KOREA_2015_SCHOOL_TRIAL_BOUNDARY.json')
    trial = load(root, 'design/A01_FIRST_TRIAL_BLUEPRINT.json')
    conditional = (root / 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.md').read_text(encoding='utf-8-sig')
    story = (root / 'canon/STORY_BIBLE.md').read_text(encoding='utf-8-sig')
    assert research['status'] == 'PRIMARY_TEXT_RECOVERED_WITH_CASE_SPECIFIC_HOLD'
    verify_research_semantics(research)
    assert trial['status'] == 'ACTUAL_VERIFIED'
    assert [b['id'] for b in trial['beats']] == ['T1', 'T2']
    assert 'CF03의 실제 훈련에 앞서 체험일의 학교 허용 절차와 전달된 출석·학업보충·시간 조건을 확인해야 한다' in conditional
    assert '당일 수업 출석' in story and '학업보충' in story and '시간 준수' in story
    assert trial['information_boundary']['training_administrative_permission'] is None
    official = {s['id']: s['url'] for s in research['sources']}
    return {
        'schema': 'A01_FICTIONAL_SCHOOL_TRIAL_OPERATING_PATH_V1',
        'status': 'ROUTINE_FICTIONAL_SETTING_DESIGN_SELECTED_WITH_CASE_EXECUTION_LIMIT',
        'classification': 'DELEGATED_DESIGN_SELECTION_NOT_AUTHOR_LOCK_OR_REAL_SCHOOL_FACT',
        'purpose': 'Support the locked T1 first-trial participation without giving the coach attendance or registration authority.',
        'historical_source_scope': {
            'verified_in_prior_research': ['F03', 'F07', 'F08'],
            'support': {
                'F03': 'Coach duties include training plans, supervision and facility safety; no independent attendance pardon is inferred.',
                'F07': '2015 school-sport plan separates after-class exercise within a school operating plan from ordinary classes.',
                'F08': 'Attendance and school-life administration belong to school rules rather than a coach offer.',
            },
            'official_urls': {k: official[k] for k in ('S2', 'S3', 'S4')},
            'historical_rule_mandates_this_exact_local_procedure': False,
            'whole_2015_law_audit_complete': False,
        },
        'selected_fictional_operating_plan': {
            'school_name': None,
            'effective_exact_date': None,
            'premise': ('The fictional school has an after-class basketball activity plan '
                        'within its principal/committee operating process. The plan permits '
                        'a supervised one-time experience for a student who clears the '
                        'school-side condition check.'),
            'scope': 'ONE_CONDITIONAL_AFTER_CLASS_TRIAL_ONLY',
            'school_plan_preexists_T1_as_design_assumption': True,
            'not_a_nationwide_mandated_trial_form': True,
            'new_named_person_or_office': False,
        },
        'role_authority': [
            {'role': 'school_plan_authority', 'can': ['set the after-class activity and supervision envelope'],
             'cannot': ['retroactively erase attendance', 'certify league registration']},
            {'role': 'coach', 'can': ['offer a conditional trial', 'set its training time and safety boundaries',
                                     'conduct supervised first trial after school-side clearance'],
             'cannot': ['alone approve attendance status', 'erase warnings', 'make official team or league registration']},
            {'role': 'attendance_teacher_function', 'can': ['confirm and retain the actual school attendance record',
                                                            'communicate attendance condition status to the trial process'],
             'cannot': ['treat the coach offer as attendance correction']},
            {'role': 'academic_support_function', 'can': ['check satisfaction of the academic supplement condition before this trial'],
             'cannot': ['call a short trial-day promise completion of a statutory learning program']},
            {'role': 'student_affairs_function', 'can': ['handle warnings or dispositions separately under school rules'],
             'cannot': ['turn trial participation itself into retroactive deletion']},
        ],
        'operational_sequence': [
            {'id': 'P0', 'action': 'School activity plan and supervision envelope exist before any student trial.',
             'classification': 'FICTIONAL_DESIGN_SELECTION', 'dramatized_new_beat': False},
            {'id': 'P1', 'action': 'Coach conveys the existing B4 conditional offer: same-day class attendance, academic supplement and punctuality.',
             'classification': 'AUTHOR_LOCKED_OFFER_PLUS_DELIVERY_MODEL', 'dramatized_new_beat': False},
            {'id': 'P2', 'action': 'Before T1, school-side functions verify all three participation conditions for this one trial and communicate limited eligibility to the coach.',
             'classification': 'FICTIONAL_PROCEDURAL_BRIDGE_FOR_LOCKED_T1', 'dramatized_new_beat': False},
            {'id': 'P3', 'action': 'Coach supervises the single after-class trial under the plan; T1 locked entry precedes T2 locked defeat.',
             'classification': 'AUTHOR_LOCKED_STORY_EVENTS_WITH_ROUTINE_SUPERVISION', 'dramatized_new_beat': False},
            {'id': 'P4', 'action': 'Attendance warning, supplement completion, team membership, registration and contest eligibility stay separate.',
             'classification': 'AUTHORITY_BOUNDARY', 'dramatized_new_beat': False},
        ],
        'condition_handling': {
            'conditions_from_canon': ['same-day class attendance', 'academic supplement', 'punctuality'],
            'delivered_to_protagonist_before_T1_in_selected_model': True,
            'selected_model_pre_T1_condition_check': {
                'same_day_class_attendance': 'SATISFIED_FOR_LIMITED_TRIAL_IN_FICTIONAL_MODEL',
                'academic_supplement': 'SATISFIED_FOR_LIMITED_TRIAL_IN_FICTIONAL_MODEL',
                'punctuality': 'SATISFIED_FOR_LIMITED_TRIAL_IN_FICTIONAL_MODEL',
            },
            'limited_trial_clearance_in_fictional_model': 'SELECTED_FOR_LOCKED_T1_ONLY',
            'exact_attendance_periods_or_warning_stage': None,
            'exact_supplement_schedule_or_completion': None,
            'exact_trial_day_or_relation_to_offer_day': None,
            'guardian_notice_or_consent_rule': None,
            'facility_supervision_details': None,
            'case_file_or_signature': None,
            'actual_real_school_or_student_verification': False,
            'specific_case_records_certified': False,
            'past_attendance_retroactively_deleted': False,
        },
        'narrative_scope': {
            'locked_T1_T2_unchanged': True,
            'new_speech_or_action_scene': False,
            'new_school_name_person_grade_or_date': False,
            'exact_trial_movement_or_score_added': False,
            'individual_scene_pov_verified': False,
            'procedural_bridge_is_separate_story_beat': False,
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {p: sha((root / p).read_bytes()) for p in SOURCES},
        'assessment': {
            'institutional_authority_model_specified': True,
            'condition_delivery_model_specified': True,
            'fictional_limited_trial_clearance_modeled': True,
            'specific_attendance_supplement_records_certified': False,
            'real_world_individual_permission_certified': False,
            'e2_final_function_registered_or_completed_by_this_artifact': False,
            'review_needed_before_E2_promotion': True,
        },
        'final_episode_functions_completed_this_artifact': 0,
        'actual_context_packs': 0,
        'whole_g13_complete': False,
        'whole_g14_complete': False,
        'author_locked': False,
        'new_author_decisions': 0,
        'manuscript_count': 0,
        'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }


def render(data):
    rows = ['| 단계 | 가상학교 설계 선택 | 권한 경계 |', '| --- | --- | --- |']
    for item in data['operational_sequence']:
        rows.append(f"| {item['id']} | {item['action']} | {item['classification']} |")
    return '\n'.join([
        '# A01 첫 체험의 가상학교 운영 경로',
        '',
        '**상태:** `ROUTINE_FICTIONAL_SETTING_DESIGN_SELECTED_WITH_CASE_EXECUTION_LIMIT`. 잠긴 첫 훈련 T1을 가능하게 하는 가상학교의 단일 운영안을 선택했다. 실제 한국 학교의 학칙, 특정 학생의 허가 기록, 새 작가 잠금, 최종 E2 회차 기능을 인증한 문서가 아니다.',
        '',
        '## 근거와 선택의 구분',
        '',
        '- 당시 공식 근거 F03: 지도자의 훈련 지도·관리와 안전 직무. F07: 정규수업 밖 운동을 위한 학교 운영계획 구조. F08: 출석·학교생활은 학칙 영역. [근거 원장](../research/A01_KOREA_2015_SCHOOL_TRIAL_BOUNDARY.md)에 원문 위치·일자·지문이 있다.',
        '- [교육부 2015 학교체육 계획](https://www.moe.go.kr/boardCnts/viewRenew.do?boardID=316&boardSeq=59104&lev=0&m=0302&opType=N&page=1&s=moe&searchType=null&statusYN=C)은 위 권한 경계의 역사 자료다. 아래 정확한 학교 내부 절차를 전국 규칙으로 명령한 근거가 아니다.',
        '- **가상학교 설계 선택:** 학교의 방과 후 농구 운영계획 안에 지도·안전이 있는 일회 체험 경로를 둔다. 감독은 조건부 제안과 훈련 운영을 맡고, 출석 상태·학업보충 의무·학교생활 처리는 해당 학교 담당 기능이 분리해 확인한다. 인명·학교명·계획 시행일은 선택하지 않았다.',
        '',
        '## T1 앞의 운영 순서',
        '',
        *rows,
        '',
        'B4의 당일 수업 출석·학업보충·시간 준수 조건은 T1 전 주인공에게 전달되고 **세 조건 모두 체험 전 확인·충족**되는 가상학교 모델로 지정한다. 학업보충을 단순히 나중에 할 약속으로 바꾸지 않는다. 학교 측의 일회 체험 가능 확인은 이미 잠긴 T1 참가를 연결하는 설계 상태다. 확인 기록의 정확 수업·보충 내용, 개별 서명, 제안일과 체험일의 동일 여부는 인증하지 않는다. 보호자 통지·동의의 학교별 규칙과 시설 감독 세부도 미정이다. 출석 경고의 소급 삭제도 없다.',
        '',
        '감독은 체험을 제안하고 안전하게 지도할 수 있지만 출결 처분을 바꾸거나 정식 농구부 소속·단체등록·대회 출전을 보장하지 않는다. 첫 참가 T1과 첫 완패 T2는 기존 정본 그대로이고 새 대사·행정 장면·경기 동작을 쓰지 않는다.',
        '',
        '## G13 판정 범위',
        '',
        '학교 권한의 운영 경로와 조건 전달 경로를 **설계 수준에서 명시**했다. 이 문서만으로 E2 최종 회차 기능은 완료/등록하지 않는다. 국소 기능 배치 검문에서 가상학교 설계 선택의 적합성, E1→T1/T2→C1 정확 인계, 정보 접근을 별도로 확인해야 한다. 특정 학생의 출석·보충 기록이나 실제 학교 허가 인증을 요구하는 근거로 이 설계를 오해하지 않는다.',
        '',
        'G13 전체·G14·실제 Context Pack·G15–G17·원고는 미완료다. `CLOSED`, `manuscript_allowed:false`, 새 작가 잠금 0을 유지한다.',
        '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound operating design']


def self_test(data):
    mutations = [
        ('solo coach permission', lambda d: d['role_authority'][1]['can'].append('erase attendance warning')),
        ('real school claim', lambda d: d['condition_handling'].update(actual_real_school_or_student_verification=True)),
        ('retroactive deletion', lambda d: d['condition_handling'].update(past_attendance_retroactively_deleted=True)),
        ('official registration', lambda d: d['assessment'].update(real_world_individual_permission_certified=True)),
        ('false E2 completion', lambda d: d['assessment'].update(e2_final_function_registered_or_completed_by_this_artifact=True)),
        ('manuscript gate', lambda d: d.update(manuscript_allowed=True)),
        ('source mismatch', lambda d: d['source_rev_sha256'].update({'canon/STORY_BIBLE.md': '0' * 64})),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        assert validate(candidate), name
    source = load(ROOT, 'research/A01_KOREA_2015_SCHOOL_TRIAL_BOUNDARY.json')
    source_mutations = [
        ('coach source reversal', lambda d: next(f for f in d['facts'] if f['id'] == 'F03').update(statement_ko='감독 단독으로 출결 삭제 가능')),
        ('plan source reversal', lambda d: next(f for f in d['facts'] if f['id'] == 'F07').update(source_ids=['S1'])),
        ('bylaw source reversal', lambda d: next(f for f in d['facts'] if f['id'] == 'F08').update(locator='wrong page')),
        ('candidate promotion', lambda d: d['school_rule_candidate'].update(coach_solo_authority_verified=True)),
    ]
    for name, mutate in source_mutations:
        candidate = copy.deepcopy(source)
        mutate(candidate)
        try:
            verify_research_semantics(candidate)
        except AssertionError:
            continue
        raise AssertionError(name)
    return len(mutations) + len(source_mutations)


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
    print(json.dumps({'status': data['status'], 'institutional_design': True,
                      'e2_final_function_added': 0, 'negative_controls': tested,
                      'current': not errors, 'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
