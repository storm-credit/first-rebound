"""Build the bounded fictional prep-to-Villanova institutional transition."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e9_final_episode_function as previous_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_CF10_COLLEGE_TRANSITION_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A02_CF10_COLLEGE_TRANSITION_WORKING_MODEL_2026_10_07.md')
SOURCES = (
    'tools/build_a02_cf10_college_transition_working_model.py',
    str(previous_builder.OUTPUT).replace('\\', '/'),
    'design/A02_PREP_CONDITIONAL_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/STORY_BIBLE.md',
    'canon/CAREER_TIMELINE.md',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'research/COLLEGE_EXIT_PACKET.md',
    'research/TIMELINE_ELIGIBILITY_LEDGER.md',
    'canon/PROJECT_FREEZE.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF10_PINS = {
    'dominant_function': '대학 경로로 이어지는 준비',
    'cause': '기존 프렙 추천과 반복 평가, 학업 진행이 Villanova 진학 경로에 연결된다',
    'entry_state': '자신의 준비와 학교·인증 기관이 처리해야 할 답변을 구분해 대학 절차를 이어 간다',
    'pressure': '프렙에서의 개선을 대학 주전과 자동 출전의 보장으로 기대할 수 있다',
    'choice': '기존 늦은 체육장학금·입학 경로의 준비를 이어 가며 대학의 제한 역할에 필요한 기본 훈련을 택한다',
    'direct_cost': '익숙한 프렙 역할을 과시해 즉시 평가받을 시간을 대학의 제한 역할에 필요한 기본 훈련에 쓴다',
    'changed_state': '프렙에서 배운 조건부 자기관리를 가진 채 대학의 제한 역할과 새 준비 과제로 넘어가려 한다',
    'next': 'A03-S1',
    'next_dependency': 'A03에서 대학 로스터의 제한 역할과 다른 사람이 믿을 수 있는 준비를 행동으로 시험한다',
}
HISTORICAL_NCAA_INDEX = 'https://web3.ncaa.org/lsdbi/search/proposalView?id=3061'
HISTORICAL_NCAA_CORE = 'https://web3.ncaa.org/lsdbi/search/proposalView?id=2983'


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, previous_builder.OUTPUT)
    candidates = load(root, 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json')
    structure = load(root, 'design/CP2_ACT_SUBACT_PACKET.json')
    story = (root / 'canon/STORY_BIBLE.md').read_text(encoding='utf-8-sig')
    timeline = (root / 'canon/CAREER_TIMELINE.md').read_text(encoding='utf-8-sig')
    college = (root / 'research/COLLEGE_EXIT_PACKET.md').read_text(encoding='utf-8-sig')
    ledger = (root / 'research/TIMELINE_ELIGIBILITY_LEDGER.md').read_text(encoding='utf-8-sig')
    assert not previous_builder.validate(previous, root=root), 'A02 E9 source stale'
    assert previous['episode_function_id'] == 'A02-EF-009'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (18, 45)
    assert previous['next_unit']['candidate_id'] == 'A02-CF10'
    assert previous['next_unit']['candidate_is_executed_here'] is False
    assert previous['whole_A02_S3_exit_certified'] is False
    assert previous['manuscript_allowed'] is False
    cf10 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF10')
    assert cf10['subact'] == 'A02-S3'
    assert cf10['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf10['evidence_class'] == 'CANDIDATE'
    assert cf10['selected_event'] is False and cf10['author_locked'] is False
    for key, value in CF10_PINS.items():
        assert cf10[key] == value, f'A02-CF10 source {key} changed'
    assert cf10['observational_access'] == ('주인공의 경험·본인 선택·허용된 학교/팀 안내·직접 요청에 대한 답. '
                                            '다른 사람의 내면·비공개 평가·입학 판단은 접근할 수 없다.')
    s3 = next(s for s in structure['subacts'] if s['id'] == 'A02-S3')
    assert s3['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert s3['window'] == '2016.03–2017.06'
    assert '2017년 5~6월 졸업' in story and '늦은 체육장학금으로 입학' in story
    assert 'academic redshirt가 아니라 첫 시즌 공식 출전이 가능한 Division I full qualifier' in timeline
    for term in ('2017년 봄 늦은 체육장학금 오퍼와 입학 승인',
                 '2017.05~06', 'Eligibility Center 학업·athletics 인증과 Villanova compliance 확인',
                 '정확한 핵심 GPA·SAT 한 점수·Villanova 입학 심사 내부 판단',
                 '실제 2017-18 장학금 명단과의 정확한 counter 감사'):
        assert term in college, f'college route pin missing: {term}'
    for eid in ('E-018', 'E-019', 'E-023', 'E-024'):
        assert eid in ledger, f'eligibility ledger entry missing: {eid}'
    hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
              for p in SOURCES}
    return {
        'schema': 'A02_CF10_COLLEGE_TRANSITION_WORKING_MODEL_V1',
        'status': 'ROUTINE_COLLEGE_TRANSITION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'FICTIONAL_INSTITUTION_OUTCOMES_WITH_DISTINCT_2017_SPRING_SUMMER_AUTHORITIES',
        'source_function': 'A02-CF10', 'target_subact': 'A02-S3',
        'prior_A02_E9_exact_full_exit': previous['exit_state'],
        'entry_state': previous['exit_state'],
        'candidate_entry_summary_is_exact_projection': False,
        'single_function': '프렙의 반복 평가와 학업 진행을 늦은 Villanova 영입 및 졸업 경로에 연결하되, 주인공은 즉시 과시보다 대학의 제한 역할을 위한 기본 준비를 택하고 대학·학교·NCAA의 서로 다른 결정을 차례로 확인한다',
        'historical_rule_evidence': {
            'ncaa_adopted_final_index_url': HISTORICAL_NCAA_INDEX,
            'ncaa_adopted_final_core_and_ten_seven_url': HISTORICAL_NCAA_CORE,
            'ncaa_index_effective_for_initial_enrollment_from': '2016-08-01',
            'ncaa_index_says_minimum_core_gpa_2_300_and_sliding_test': True,
            'ncaa_core_proposal_says_sixteen_and_ten_before_seventh_with_seven_ems': True,
            'ncaa_core_proposal_international_exception_scope': 'CERTIFICATION_BASED_ENTIRELY_ON_INTERNATIONAL_CREDENTIALS',
            'mixed_korean_and_us_schooling_exception_claimed': False,
            'sixteen_core_and_ten_seven_repo_ledger': 'research/TIMELINE_ELIGIBILITY_LEDGER.md#E-018',
            'international_us_mixed_case_source': 'research/TIMELINE_ELIGIBILITY_LEDGER.md#E-019',
            '2017_individual_course_mapping_certified_by_web': False,
            'current_ncaa_page_retroactively_applied_as_2017_case': False,
            'source_scope': 'HISTORICAL_RULE_BASELINE_NOT_A_REAL_STUDENT_CERTIFICATION',
        },
        'preexisting_route_foundation_not_new_episode_events': [
            '2016 봄 프렙 감독의 신체·수비 자료와 학점 예비 감사 전달',
            '허용된 평가 기간의 실전 관찰과 2016–17 리바운드·스위치·전환·학업 진행 재확인',
            '2017 마지막 학기 전 10/7을 확보하고 마지막 학기에 16개 총량과 졸업 부족분을 마감하는 기존 범주 경로',
        ],
        'institutional_sequence': [
            {'id': 'I1', 'window': '2017_SPRING_LATE', 'scope': 'A02_S3',
             'actor': 'FICTIONAL_VILLANOVA_RECRUITING_AND_ADMISSIONS_AUTHORITIES',
             'outcome': 'LATE_ATHLETIC_SCHOLARSHIP_OFFER_AND_ADMISSION_SELECTED_IN_FICTION',
             'offer_in_fiction': True, 'admission_in_fiction': True,
             'student_receives_authorized_notice': True,
             'actual_real_student_or_2017_archival_record_certified': False,
             'exact_offer_or_admission_date': None,
             'observable_boundary': '주인공은 공식 경로의 통지를 받고도 대학 선발·주전·첫 경기 출전을 보장받은 것으로 여기지 않는다'},
            {'id': 'I2', 'window': '2017_MAY_JUNE', 'scope': 'A02_S3',
             'actor': 'FICTIONAL_PREP_SCHOOL_ACADEMIC_AUTHORITY',
             'outcome': 'EARLY_GRADUATION_AND_FINAL_TRANSCRIPT_SENT_IN_FICTION',
             'graduation_in_fiction': True, 'final_transcript_sent_in_fiction': True,
             'individual_korean_course_conversion_or_gpa_certified_in_repo': False,
             'actual_document_copy_or_number_certified': False,
             'exact_graduation_or_submission_date': None,
             'observable_boundary': '학교 학업담당의 졸업 및 제출 완료 안내를 받아 학생의 질문 목록에서 학교 몫을 지운다'},
            {'id': 'I3', 'window': '2017_SUMMER', 'scope': 'INTER_ACT_INSTITUTIONAL_BRIDGE_NOT_A02_EPISODE_DATE',
             'actor': 'NCAA_ELIGIBILITY_CENTER_AND_FICTIONAL_VILLANOVA_COMPLIANCE',
             'outcome': 'FULL_QUALIFIER_CERTIFIED_AND_COMPLIANCE_CONFIRMED_IN_FICTION',
             'eligibility_center_academic_and_athletics_certified_in_fiction': True,
             'villanova_compliance_confirmed_in_fiction': True,
             'actual_private_ncaa_decision_or_villanova_record_certified': False,
             'exact_individual_core_gpa_sat_courses': None,
             'observable_boundary': '당사자에게 전달 가능한 자격·컴플라이언스 완료 결과만 확인한다. 내부 심사 내용은 알지 못한다'},
            {'id': 'I4', 'window': 'AFTER_2017_SUMMER_CERTIFICATION',
             'scope': 'A03_ENTRY_PREREQUISITE_NOT_A02_EPISODE_EVENT',
             'actor': 'FICTIONAL_VILLANOVA_ENROLLMENT_AND_TEAM',
             'outcome': 'ENROLLMENT_PATH_READY_OFFICIAL_PARTICIPATION_ONLY_AFTER_I3',
             'enrollment_or_first_game_executed_here': False,
             'starter_or_unrestricted_minutes_guaranteed': False,
             'exact_roster_counter_assignment_audited_here': False,
             'observable_boundary': '대학 등록·첫 공식 출전은 다음 Act의 별도 검문 대상으로 남긴다'},
        ],
        'student_choice': {
            'options': ['익숙한 프렙 역할을 과시해 한 번의 평가를 당장 더 받는다',
                        '대학의 후순위 수비·리바운드 역할을 위한 기본 위치·전환 준비를 계속한다'],
            'selected': '대학의 후순위 수비·리바운드 역할을 위한 기본 위치·전환 준비를 계속한다',
            'bounded_action': '주인공은 허용된 프렙 훈련 시간 한 부분을 즉시 보여 줄 공 소유 장면 대신 수비 위치와 리바운드 뒤 전환 연결의 기본 반복에 쓴다',
            'observable_result': '선택한 연습을 수행하지만 대학 경기의 안정성, 실전 minutes, 주전 경쟁 승리는 아직 보이지 않는다',
            'direct_present_cost': '익숙한 프렙 역할을 한 번 더 과시할 허용 훈련·평가 시간을 제한 역할의 기본 반복에 쓴다',
        },
        'partial_order': [
            'E9 exact full exit < I1 late spring offer/admission',
            'I1 late spring offer/admission < I2 May–June graduation and final transcript',
            'I2 final transcript < I3 summer EC certification and Villanova compliance',
            'I3 certification and compliance < I4 later enrollment and official participation',
            'A02 S3 episode window ends 2017 June; I3–I4 are inter-act and A03 conditions, not backdated A02 events',
        ],
        'selected_design_exit_state': '주인공은 자신이 준비한 목록과 프렙의 반복 평가·학업 진행을 바탕으로 2017년 봄 늦은 Villanova 체육장학금 오퍼와 입학 승인을 전달받고, 5~6월 가상 프렙 조기졸업 및 최종 성적표 제출 안내를 받았다. 그는 익숙한 프렙 역할을 과시할 기회보다 대학의 제한 역할을 위한 기본 위치·전환 준비를 택한다. 여름 Eligibility Center와 Villanova compliance의 별도 완료는 대학 등록·공식 출전 전에 확인되어야 하며, 현재 A02 회차의 사건이나 대학 경기 성공으로 소급하지 않는다.',
        'reader_question_at_end': '학교를 떠나는 준비와 기관의 여름 인증이 대학의 제한 역할이라는 다음 시험으로 어떻게 이어질 것인가',
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'may_know': ['자신에게 전달된 영입·입학 통지', '가상 프렙 학업담당의 졸업·제출 안내',
                         '자신이 선택해 수행한 제한 역할 기본 훈련과 그 시간 비용'],
            'may_later_know_after_authorized_notice': ['여름 EC 자격 결과', 'Villanova compliance 확인'],
            'cannot_know_from_this_episode': ['입학처 비공개 심사', 'NCAA 내부 과목별 환산',
                                               '실제 2017 Villanova counter 배분', '대학 첫 경기 출전 결과'],
            'individual_scene_pov_verified': False, 'exact_dialogue': None,
        },
        'unassigned_details': {
            'fictional_prep_name': None, 'exact_offer_or_nli_date': None,
            'exact_graduation_or_submission_date': None,
            'individual_korean_course_conversion': None, 'core_gpa_exact': None,
            'sat_point_score': None, 'school_or_ncaa_document_numbers': None,
            'villanova_scholarship_counter_exact_reconstruction': None,
            'specific_evaluation_opponent_score_minutes': None,
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'The locked fictional Villanova route has selected institutional outcomes, but this model cannot certify private records for a real 2017 student.',
            'Two adopted final NCAA proposals support the 2016-effective 16-core, 10-before-seventh, seven English/math/science and sliding-index baseline; E-019 keeps the mixed-school individual case unverified and no entirely-international exception is asserted.',
            'No exact grade, core-course conversion, SAT point, NLI date, counter assignment, actual private receipt, or original institutional document is invented.',
            'The summer EC/compliance outcome is an inter-act institutional bridge after the A02 June window, not an A02 episode event or a college game.',
        'Independent source and meaning review accepted this bounded model; a separate final-function review remains required before function promotion.',
        ],
        'actual_verified_blueprint_created': False, 'final_episode_function_added': 0,
        'whole_A02_S3_exit_certified': False, 'whole_g13_complete': False,
        'whole_g14_complete': False, 'actual_context_packs': 0,
        'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }


def render(data):
    lines = [
        '# A02 CF10: 프렙 종료와 Villanova 경로의 분리된 권한', '',
        '**상태:** `ROUTINE_COLLEGE_TRANSITION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 기존 잠긴 진학 방향을 구현한 가상 설계가 독립 검문을 통과했다. 최종 회차 기능 검문 전에는 기능 수를 늘리지 않는다.', '',
        '## 학생의 국소 선택', '',
        f"- 정확한 진입: {data['entry_state']}",
        f"- 단일 기능: {data['single_function']}",
        f"- 행동: {data['student_choice']['bounded_action']}",
        f"- 보이는 결과: {data['student_choice']['observable_result']}",
        f"- 현재 비용: {data['student_choice']['direct_present_cost']}", '',
        '## 기관 순서와 범위', '',
    ]
    for m in data['institutional_sequence']:
        lines.append(f"- {m['id']} `{m['window']}` / `{m['scope']}` / `{m['actor']}`: `{m['outcome']}`. {m['observable_boundary']}")
    lines.extend([
        '', f"- A02 국소 출구: {data['selected_design_exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 사실·허구·미확인', '',
        f"- 역사 규정: [NCAA LSDBi 채택 최종 2012-8]({HISTORICAL_NCAA_CORE})은 2016-08-01 적용 16개 핵심과목·7학기 전 10개 및 그중 영어·수학·과학 7개를 명시한다. [채택 최종 2013-11]({HISTORICAL_NCAA_INDEX})은 2.300 core GPA·시험 sliding index 근거다. 혼합 한국·미국 학적에 entirely-international 예외를 적용했다고 주장하지 않는다.",
        '- 가상 결과: 2017 봄 늦은 장학금 오퍼·입학, 5–6월 학교 졸업·최종 제출, 여름 NCAA/대학 compliance 완료를 기관별로 둔다. 여름 결과는 A02 회차 창 밖의 연결 조건이다.',
        '- 개인별 한국 과목 환산·정확 GPA/SAT·서류 원본·실제 Villanova 장학금 counter 재구성은 미확인이다. 현재 NCAA 웹 안내를 당시 개인 판정에 역투영하지 않는다.',
        '- 주전·대학 첫 경기·전체 A02-S3/G13/G14·Pack·원고는 인증하지 않는다. 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound CF10 transition model']


def self_test(data):
    changes = [
        ('admission before prior work', lambda d: d['institutional_sequence'][0].update(window='2016_SPRING')),
        ('unqualified college play', lambda d: d['institutional_sequence'][3].update(enrollment_or_first_game_executed_here=True)),
        ('real student certified', lambda d: d['institutional_sequence'][2].update(actual_private_ncaa_decision_or_villanova_record_certified=True)),
        ('coach certifies EC', lambda d: d['institutional_sequence'][2].update(actor='PREP_BASKETBALL_COACH')),
        ('summer backdated', lambda d: d['institutional_sequence'][2].update(scope='A02_S3')),
        ('invent GPA', lambda d: d['unassigned_details'].update(core_gpa_exact=2.75)),
        ('invent scholarship counter', lambda d: d['unassigned_details'].update(villanova_scholarship_counter_exact_reconstruction=13)),
        ('automatic starting', lambda d: d['institutional_sequence'][3].update(starter_or_unrestricted_minutes_guaranteed=True)),
        ('full S3', lambda d: d.update(whole_A02_S3_exit_certified=True)),
        ('function prepaid', lambda d: d.update(final_episode_function_added=1)),
        ('manuscript gate', lambda d: d.update(manuscript_allowed=True)),
    ]
    for name, mutate in changes:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_load = load
    for name, key, replacement in [
        ('same-ID automatic starter', 'choice', '늦은 영입으로 대학 주전과 즉시 출전을 보장받는다'),
        ('same-ID scholarship revoked', 'direct_cost', '감독에게 이미 받은 장학금을 몰수당한다'),
        ('same-ID coach certifies', 'changed_state', '프렙 감독이 졸업과 NCAA 자격을 직접 승인했다'),
    ]:
        def changed_load(root, path):
            source = original_load(root, path)
            if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A02-CF10')[key] = replacement
            return source
        with patch(__name__ + '.load', side_effect=changed_load):
            assert validate(data), name
    return len(changes) + 3


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
