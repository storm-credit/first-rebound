"""Select the first prep academic-help action after a scoped fictional move."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a01_e9_final_episode_function as e9


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_CF01_ACADEMIC_HELP_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A02_CF01_ACADEMIC_HELP_WORKING_MODEL_2026_10_07.md')
BRIDGE = Path('research/A01_A02_PREP_TRANSITION_AUTHORITY_BOUNDARY_2026_10_07.json')
SOURCES = (
    'tools/build_a02_cf01_academic_help_working_model.py',
    'design/A01_E9_FINAL_EPISODE_FUNCTION.json',
    'design/A02_PREP_CONDITIONAL_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    str(BRIDGE).replace('\\', '/'),
    'canon/STORY_BIBLE.md',
    'canon/CAREER_TIMELINE.md',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'canon/PROJECT_FREEZE.md',
    'research/TIMELINE_ELIGIBILITY_LEDGER.md',
    'AGENTS.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF01_PINS = {
    'dominant_function': '학업 요건의 도움 요청',
    'cause': '한국에서 농구를 계속할 이유를 얻었지만 학업·생활 과제가 남은 채 낯선 프렙에 들어간다',
    'pressure': '생활 영어가 가능해도 과목·학점·졸업 요건과 학술 읽기·쓰기까지 혼자 해결할 수는 없다',
    'choice': '학업 담당자에게 부족한 과목과 필요한 준비를 묻고 도움을 요청한다',
    'direct_cost': '모른다는 사실을 드러내며 혼자 버티거나 농구만 할 시간을 학습 도움에 쓴다',
    'changed_state': '생활 영어에 기대어 숨기던 학사 과제의 어려움을 드러내고 필요한 도움을 요청한 상태가 된다',
    'next': 'A02-CF02',
}
BRIDGE_STEP_PINS = {
    'F1': ('fictional private New England boarding prep',
           'The fictional school has an F-1-capable SEVP-certified program and accepts this student academically in time for the locked March 2016 transfer.'),
    'F2': ('fictional guardian and financing arrangement',
           "The student's guardian consents to the already locked move and a sufficient fictional funding route exists; its people, sums and paperwork remain unassigned."),
    'F3': ('fictional prep designated school official and SEVIS',
           'After school acceptance the fictional school creates the required student record and issues a Form I-20 for the academic F route.'),
    'F4': ('U.S. consular decision in the fictional case',
           'A student visa is granted after the school document step; no interview date, fee, number or personal ruling is specified.'),
    'F5': ('U.S. border admission in the fictional case',
           'The student is admitted for the canon March 2016 school arrival; a visa is not treated as identical to admission.'),
    'F6': ('fictional prep academic office',
           'On arrival the school has a provisional academic placement and an adviser who can discuss courses and support; exact Korean credit conversions and eventual graduation audit remain open.'),
}
BRIDGE_ORDER = [
    'F1 school acceptance and F2 guardian/funding arrangement precede F3 school record/I-20 and F4 visa; exact F1-versus-F2 order unassigned',
    'F3 school record/I-20 precedes F4 visa, which precedes F5 border admission',
    'F5 March 2016 arrival precedes F6 in-school academic help, with exact dates unassigned',
]


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, e9.OUTPUT)
    candidates = load(root, 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json')
    packet = load(root, 'design/CP2_ACT_SUBACT_PACKET.json')
    bridge = load(root, BRIDGE)
    story = (root / 'canon/STORY_BIBLE.md').read_text(encoding='utf-8-sig')
    career = (root / 'canon/CAREER_TIMELINE.md').read_text(encoding='utf-8-sig')
    responsibility = (root / 'canon/CHARACTER_RESPONSIBILITY_ARC.md').read_text(encoding='utf-8-sig')
    assert not e9.validate(previous, root=root), 'E9 source-current function is stale'
    assert previous['episode_function_id'] == 'A01-EF-009'
    assert previous['next_unit']['candidate_id'] == 'A02-S1'
    assert previous['next_unit']['candidate_is_executed_here'] is False
    assert previous['whole_g13_complete'] is False
    assert bridge['fictional_transition_working_path']['status'] == 'ROUTINE_FICTIONAL_AUTHORITY_OUTCOMES_SELECTED_WITHIN_LOCKED_MOVE_INDEPENDENTLY_REVIEWED'
    assert bridge['source_currentness'] == 'RECHECKED_AFTER_PARENT_CP2_8_9_INTEGRATION'
    assert bridge['central_source_sha256_certified'] is True
    assert set(bridge['repo_source_sha256']) == set(bridge['repo_sources'])
    assert all(bridge['repo_source_sha256'][p] == sha((root / p).read_bytes())
               for p in bridge['repo_sources']), 'fictional transition source revision stale'
    assert [s['id'] for s in bridge['fictional_transition_working_path']['steps']] == ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']
    for step in bridge['fictional_transition_working_path']['steps']:
        assert (step['authority'], step['working_selection']) == BRIDGE_STEP_PINS[step['id']], \
            f"fictional transition source meaning changed: {step['id']}"
    assert bridge['fictional_transition_working_path']['partial_order'] == BRIDGE_ORDER, \
        'fictional institutional order changed'
    assert [(r['order'], r['actor'], r['coach_or_protagonist_may_certify'])
            for r in bridge['institutional_sequence_as_conditional_model']] == [
                (1, 'fictional prep admissions and academic office', False),
                (2, 'fictional prep designated school official and SEVIS', False),
                (3, 'U.S. consular officer', False),
                (4, 'U.S. Customs and Border Protection', False),
                (5, 'fictional prep academic adviser', False),
                (6, 'NCAA Eligibility Center and later college admissions/compliance', False),
            ], 'institutional authority categories changed'
    assert bridge['fictional_transition_working_path']['A01_E9_intent_is_not_any_of_F1_to_F6'] is True
    assert bridge['fictional_transition_working_path']['historical_real_person_or_real_school_case_certified'] is False
    assert bridge['fictional_transition_working_path']['A02_CF01_final_episode_function_added'] == 0
    assert bridge['fictional_transition_working_path']['A02_S1_full_completion_certified'] is False
    assert bridge['manuscript_allowed'] is False
    cf01 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF01')
    assert cf01['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf01['evidence_class'] == 'CANDIDATE'
    assert cf01['selected_event'] is False
    assert cf01['author_locked'] is False
    assert cf01['subact'] == 'A02-S1'
    for key, expected in CF01_PINS.items():
        assert cf01[key] == expected, f'A02-CF01 source {key} changed'
    subact = next(s for s in packet['subacts'] if s['id'] == 'A02-S1')
    assert subact['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert subact['window'] == '2016.03–2017.06'
    assert subact['title'] == '편입과 학사'
    assert '생활 영어가 가능해도 Villanova 입학' in story
    assert '2016.03 | 가상 뉴잉글랜드 보딩 프렙 중도 편입·학점 감사' in career
    assert '생활 영어는 가능하지만 학업 일정·훈련 규율·기숙사 생활은 자동 해결되지 않는다' in responsibility
    source_hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
                     for p in SOURCES}
    return {
        'schema': 'A02_CF01_ACADEMIC_HELP_WORKING_MODEL_V1',
        'status': 'ROUTINE_PREP_ACADEMIC_HELP_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'FICTIONAL_PREP_AFTER_LOCKED_MOVE_NOT_INDIVIDUAL_ELIGIBILITY_OR_ADMISSION_CERTIFICATION',
        'source_function': 'A02-CF01', 'target_subact': 'A02-S1',
        'last_A01_full_exit': previous['exit_state'],
        'fictional_transition_bridge': str(BRIDGE).replace('\\', '/'),
        'bridge_steps_selected': ['F1', 'F2', 'F3', 'F4', 'F5', 'F6'],
        'bridge_real_case_certified': False,
        'entry_state_after_fictional_bridge': '이미 잠긴 2016년 3월 가상 프렙 이동이 가상 기관 절차로 실행돼 학교에 도착했지만, 주인공의 E9 미답 목록과 기술·학업·생활 과제는 남아 있다.',
        'A02_provisional_entry_language_assumption_verified_by_E9': False,
        'A02_S1_whole_entry_or_exit_certified': False,
        'single_function': '생활 영어와 학업 요건의 차이를 자기 앞의 과제로 발견하고 학업 담당자에게 도움을 요청한다',
        'event_steps': [
            {'id': 'H1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '가상 프렙의 첫 학업 안내에서 일상 대화는 따라가지만 수업·학점·졸업 준비 항목을 자기 과목 계획으로 옮기려다 빈칸을 발견한다',
             'observable_result': '생활 영어로 소통 가능한 것과 자기 학업 요건을 정확히 파악하는 것이 별개라는 현재 어려움이 드러난다',
             'not_claimed': '개별 핵심과목 수·학점 판정·입학 오류·학년 낙제·NCAA 자격 실패'},
            {'id': 'H2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'choice_options': ['모르는 부분을 숨기고 농구만 하며 버틴다', '가상 프렙 학업 담당자에게 부족한 준비를 묻고 도움을 요청한다'],
             'selected_choice': '가상 프렙 학업 담당자에게 부족한 준비를 묻고 도움을 요청한다',
             'action': '모른다는 사실을 학업 담당자에게 밝히고, 자기 시간표에서 무엇을 확인하고 어떤 도움을 먼저 받을 수 있는지 묻는다',
             'observable_result': '주인공이 직접 도움을 요청한 행동이 남고, 담당자의 실제 개별 학점·졸업·NCAA 결론은 아직 열어 두고 학습 지원의 다음 접점을 잡는다',
             'not_claimed': '정확한 과목명·점수·튜터 일정·졸업 보장·감독의 학사결정'},
        ],
        'direct_present_cost': '모른다는 점을 직접 드러내고, 농구만 하거나 혼자 버틸 수 있는 한 학습 기회를 담당자와의 도움 요청에 쓴다.',
        'selected_design_exit_state': '주인공은 생활 영어가 곧 학업 계획의 이해는 아니라는 어려움을 자기 일로 드러내고 프렙 학업 담당자에게 도움을 요청했다. 개별 학점·졸업·NCAA 인증과 생활 순서의 개선은 아직 확인되지 않았다.',
        'reader_question_at_end': '도움을 요청한 뒤에도 게임·수면과 정해진 의무를 충돌 없이 지킬 수 있는가',
        'next_candidate': {'id': 'A02-CF02', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'actual_lost_opportunity_kind_or_penalty_not_selected': True},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['자기 앞에 제시된 가상 학교 안내의 일반 범주', '자기가 이해하지 못한 항목', '자기 도움 요청과 공개된 답'],
            'not_available_without_access': ['담당자의 비공개 입학/졸업 판단', '실제 NCAA 심사결론', '프렙 감독의 속마음', '미래 팀 역할'],
            'individual_scene_pov_verified': False, 'exact_dialogue': None,
        },
        'institutional_limits': {
            'prep_academic_adviser_can_explain_support': True,
            'prep_adviser_certifies_NCAA_full_qualifier': False,
            'individual_Korean_course_conversion_certified': False,
            'individual_GPA_or_test_score_selected': False,
            'graduation_audit_complete': False,
            'basketball_registration_or_minutes_certified': False,
            'real_student_or_school_case_certified': False,
        },
        'unassigned_details': {
            'fictional_prep_name_or_staff_identity': None,
            'individual_course_names_or_credits': None,
            'actual_timetable_or_tutoring_time': None,
            'individual_GPA_or_SAT': None,
            'graduation_audit_or_NCAA_case': None,
            'basketball_roster_or_first_game': None,
            'exact_arrival_or_adviser_meeting_day': None,
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': source_hashes,
        'verification_limits': [
            'F1-F6 are reviewed fictional authority outcomes implementing the already locked move, not historical real-person documents.',
            'E9 is exact prior local exit, while F1-F6 are distinct intervening fictional institutional outcomes.',
            'The adviser meeting selects one routine help request without individual course, GPA, graduation or NCAA rulings.',
            'The A02-S1 provisional language assumption is neither inherited as an E9 fact nor automatically cured by one request.',
            'CF02 game/sleep lost opportunity remains unselected; no penalty or discipline is invented.',
            'Independent review is required before a local Blueprint or first A02 episode function can be considered.',
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
        '# A02 CF01 프렙 학업 도움 요청의 가상 설계', '',
        '**상태:** `ROUTINE_PREP_ACADEMIC_HELP_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 기존 잠긴 2016년 3월 이동을 [가상 권한 경로](../research/A01_A02_PREP_TRANSITION_AUTHORITY_BOUNDARY_2026_10_07.md) F1–F6로 잇고, 첫 학업 도움 요청 행동만 선택했다. 부모의 독립 원천·의미 검문을 통과했다. 실제 학생기록·졸업·NCAA 판정이나 최종 회차·원고가 아니다.', '',
        '## 입력과 기능', '',
        f"- E9의 실제 전체 종료: {data['last_A01_full_exit']}",
        f"- F1–F6 가상 전환 뒤의 진입: {data['entry_state_after_fictional_bridge']}",
        f"- 한 기능: {data['single_function']}",
        f"- H1: {data['event_steps'][0]['action']} → {data['event_steps'][0]['observable_result']}",
        f"- H2: {data['event_steps'][1]['action']} → {data['event_steps'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 출구: {data['selected_design_exit_state']}",
        f"- 독자 질문: {data['reader_question_at_end']}", '',
        '## 권위 경계', '',
        '- 생활 영어로 일상 대화가 가능하다는 정본과 학술 읽기·쓰기·과목 계획의 어려움을 함께 둔다. E9의 질문 목록이 A02 잠정 진입의 정확한 착각 또는 그 완치를 인증하지 않는다.',
        '- 학업 담당자는 도움 경로를 안내할 수 있으나 NCAA Eligibility Center, 졸업 감사, 대학 입학처를 대신하지 않는다. 정확 과목/학점·GPA·SAT·시간표는 미정이다.',
        '- CF02의 게임·수면 실패와 실제 기회 상실은 미실행 후보다. 종류·날짜·처분권한을 이 기능에서 만들지 않는다.',
        '- 국소 Blueprint/A02 최종 기능 추가0, A02-S1·전체 G13/G14 미완, 실제 Context Pack·원고0, 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound A02-CF01 working model']


def self_test(data):
    mutations = [
        ('false author lock', lambda d: d.update(author_locked=True)),
        ('false final function', lambda d: d.update(final_episode_function_added=1)),
        ('false actual school case', lambda d: d['institutional_limits'].update(real_student_or_school_case_certified=True)),
        ('false NCAA certification', lambda d: d['institutional_limits'].update(prep_adviser_certifies_NCAA_full_qualifier=True)),
        ('false course conversion', lambda d: d['institutional_limits'].update(individual_Korean_course_conversion_certified=True)),
        ('false graduation', lambda d: d['institutional_limits'].update(graduation_audit_complete=True)),
        ('false language certainty', lambda d: d.update(A02_provisional_entry_language_assumption_verified_by_E9=True)),
        ('false S1 completion', lambda d: d.update(A02_S1_whole_entry_or_exit_certified=True)),
        ('invent CF02 penalty', lambda d: d['next_candidate'].update(actual_lost_opportunity_kind_or_penalty_not_selected=False)),
        ('false source SHA', lambda d: d['source_rev_sha256'].update({str(BRIDGE): '0' * 64})),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        assert validate(candidate), name
    original_load = load
    for name, key, value in [
        ('same-ID no-help reversal', 'choice', '학업이 힘들어도 감독이 대신 해결하므로 묻지 않는다'),
        ('same-ID instant graduation', 'changed_state', '한 번 질문으로 모든 과목·졸업·NCAA 자격이 확정된다'),
    ]:
        def changed_source(root, path):
            source = original_load(root, path)
            if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A02-CF01')[key] = value
            return source
        with patch(__name__ + '.load', side_effect=changed_source):
            assert validate(data), name
    for name, step_id, key, value in [
        ('F3 coach cannot issue I-20', 'F3', 'authority', 'basketball coach issuing I-20'),
        ('F4 visitor visa cannot replace student visa', 'F4', 'working_selection',
         'Enter on visitor B visa for degree study without student visa'),
    ]:
        def changed_bridge(root, path):
            source = original_load(root, path)
            if path == BRIDGE:
                source = copy.deepcopy(source)
                next(s for s in source['fictional_transition_working_path']['steps']
                     if s['id'] == step_id)[key] = value
            return source
        with patch(__name__ + '.load', side_effect=changed_bridge):
            try:
                build()
            except AssertionError:
                pass
            else:
                raise AssertionError(name + ' regenerated source accepted')
            assert validate(data), name + ' saved record accepted'
    return len(mutations) + 4


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
