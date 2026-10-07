"""Build local CF11 Blueprint and eighth A01 function from the reviewed inquiry."""

import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_a01_cf11_academic_transfer_working_model as working
import build_a01_e7_final_episode_function as e7


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_E8_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A01_E8_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a01_e8_final_episode_function.py',
    'design/A01_CF11_ACADEMIC_TRANSFER_WORKING_MODEL_2026_10_07.json',
    'design/A01_E7_FINAL_EPISODE_FUNCTION.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/CAREER_TIMELINE.md',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'research/TIMELINE_ELIGIBILITY_LEDGER.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF12_PINS = {
    'function': '미국행 선택과 미완성 준비의 이월',
    'cause': '이동의 이유와 자신이 준비할 과제가 구분됐다',
    'choice': '미국 프렙으로 옮기려는 방향을 택하고 남은 준비를 이어 간다',
    'changed_state': '농구를 계속할 이유를 가진 채 낯선 환경을 선택하지만 기술·학업·생활 과제는 남는다',
    'next': 'A02-S1',
}


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, e7.OUTPUT)
    selected = load(root, working.OUTPUT)
    candidates = load(root, 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json')
    # The CF builder validates the same full predecessor; do not traverse it twice.
    # Independent loader patches must not substitute a different predecessor.
    assert previous == working.load(root, e7.OUTPUT), 'predecessor input differs from CF validation input'
    assert not working.validate(selected, root=root), 'CF11 selected source is stale'
    assert previous['episode_function_id'] == 'A01-EF-007'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (7, 7)
    assert previous['whole_g13_complete'] is False
    assert selected['status'] == 'ROUTINE_ACADEMIC_INQUIRY_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert selected['source_function'] == 'A01-CF11'
    assert selected['target_subact'] == 'A01-S3'
    assert selected['entry_state'] == previous['exit_state']
    assert selected['prior_S2_whole_subact_exit_certified'] is False
    assert selected['S3_full_entry_or_exit_certified'] is False
    assert selected['relative_time_window']['after_E7_exit'] is True
    assert selected['relative_time_window']['before_locked_2016_03_prep_move'] is True
    assert selected['fictional_school_contact']['may_certify_US_prep_acceptance_or_credit_conversion'] is False
    assert selected['fictional_school_contact']['actual_student_record_access_or_issuance_certified'] is False
    assert selected['institutional_limits']['fictional_US_prep_admission_or_credit_acceptance_certified'] is False
    assert selected['institutional_limits']['visa_or_NCAA_eligibility_certified'] is False
    assert selected['actual_verified_blueprint_created'] is False
    assert selected['final_episode_function_added'] == 0
    assert selected['author_locked'] is False
    assert selected['manuscript_allowed'] is False
    assert [step['id'] for step in selected['event_steps']] == ['A1', 'A2']
    assert all(step['classification'] == 'ROUTINE_FICTIONAL_DESIGN'
               for step in selected['event_steps'])
    cf12 = next(f for f in candidates['functions'] if f['id'] == 'A01-CF12')
    assert cf12['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert (cf12['evidence_class'], cf12['selected_event'], cf12['author_locked']) == (
        'CANDIDATE', False, False)
    assert cf12['subact'] == 'A01-S3'
    for key, expected in CF12_PINS.items():
        assert cf12[key] == expected, f'CF12 source {key} changed'
    source_hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
                     for p in SOURCES}
    beats = []
    for step in selected['event_steps']:
        beats.append({
            'id': step['id'],
            'classification': step['classification'],
            'action': step['action'],
            'observable_result': step['observable_result'],
            'not_claimed': step['not_claimed'],
            'protagonist_access': '자기가 직접 들은 국내 기록 절차 설명과 자기가 적고 질문한 항목에 한정',
            'source_path': str(working.OUTPUT).replace('\\', '/'),
            'source_step': step['id'],
            'author_locked': False,
        })
    blueprint = {
        'schema': 'A01_CF11_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_LOCAL_ROUTINE_DESIGN_ONLY_NOT_AUTHOR_LOCK_OR_FULL_G13',
        'source_currentness': 'Reviewed CF11 inquiry and E7 full exit validated against current source files',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': copy.deepcopy(source_hashes),
        'entry_state': previous['exit_state'],
        'single_function': selected['single_function'],
        'unit_choice': '국내 기록 절차를 직접 묻고 자기 확인 항목과 가상 프렙 권한자의 답이 필요한 항목을 나눈다',
        'exit_state': selected['selected_design_exit_state'],
        'beat_count': 2,
        'beats': beats,
        'partial_order': ['E7 full exit < A1 Korean-school explanation < A2 own questions and open foreign questions < 2016-03 move window'],
        'direct_present_cost': selected['direct_present_cost'],
        'existing_locked_route': selected['existing_locked_route'],
        'fictional_school_contact': copy.deepcopy(selected['fictional_school_contact']),
        'relative_time_window': copy.deepcopy(selected['relative_time_window']),
        'information_access': copy.deepcopy(selected['information_access']),
        'institutional_limits': copy.deepcopy(selected['institutional_limits']),
        'unassigned_details': copy.deepcopy(selected['unassigned_details']),
        'S2_whole_completion_certified': False,
        'S3_full_entry_or_exit_certified': False,
        'actual_student_records_or_prep_admission_certified': False,
        'author_locked': False,
        'manuscript_allowed': False,
    }
    assigned = previous['slot_accounting']['assigned_function_slots_through_this'] + 1
    assert assigned == 8
    planned = previous['slot_accounting']['a01_planned_slots']
    assert planned == 36
    return {
        'schema': 'A01_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A01-EF-008',
        'act': 'A01', 'primary_subact': 'A01-S3',
        'source_conditional_function': 'A01-CF11',
        'final_function_order': 8,
        'planned_allocation_slot': 8,
        'published_episode_number': None,
        'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': planned,
            'prior_function_slots': 7,
            'this_function_slots': 1,
            'assigned_function_slots_through_this': assigned,
            'remaining_planned_slots': planned - assigned,
            'allocation_is_final_published_episode_count': False,
        },
        'final_episode_functions_completed_this_record': 1,
        'local_contiguous_functions_through_this': 8,
        'previous_function': {
            'id': previous['episode_function_id'],
            'path': str(e7.OUTPUT).replace('\\', '/'),
            'exit_state': previous['exit_state'],
        },
        'local_blueprint': blueprint,
        'single_function': blueprint['single_function'],
        'entry_state': blueprint['entry_state'],
        'unit_choice': blueprint['unit_choice'],
        'exit_state': blueprint['exit_state'],
        'direct_present_cost': blueprint['direct_present_cost'],
        'reader_question_at_end': selected['reader_question_at_end'],
        'internal_order': ['A1', 'A2'],
        'beats': copy.deepcopy(beats),
        'next_unit': {
            'candidate_id': 'A01-CF12',
            'candidate_status': cf12['status'],
            'candidate_subact': cf12['subact'],
            'candidate_entry_non_authoritative_summary': cf12['entry_state'],
            'candidate_summary_is_exact_or_verified_projection': False,
            'exact_full_entry_if_next_unit_selected': blueprint['exit_state'],
            'candidate_is_executed_here': False,
            'candidate_is_final_episode_function': False,
            'move_intent_or_admission_resolved': False,
        },
        'existing_locked_route': blueprint['existing_locked_route'],
        'fictional_school_contact': copy.deepcopy(blueprint['fictional_school_contact']),
        'relative_time_window': copy.deepcopy(blueprint['relative_time_window']),
        'information_access': copy.deepcopy(blueprint['information_access']),
        'institutional_limits': copy.deepcopy(blueprint['institutional_limits']),
        'unassigned_details': copy.deepcopy(blueprint['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': source_hashes,
        'verification_limits': [
            'ACTUAL_VERIFIED only means this local Blueprint matches the reviewed fictional inquiry and current sources.',
            "The Korean school official explains only the school's own record categories; no individual record is issued or corrected here.",
            'US prep admission, course-credit conversion, guardian consent, visa and NCAA eligibility remain unanswered.',
            'The already locked March 2016 fictional prep direction is not proof that this episode completed admission or transfer.',
            'S2 whole completion and S3 full entry/exit remain unverified; CF12 remains a conditional candidate.',
        ],
        'prior_S2_whole_completion_certified': False,
        'S3_full_entry_or_exit_certified': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'g15_complete': False,
        'g16_complete': False, 'g17_complete': False,
        'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }


def render(data):
    b = data['local_blueprint']
    return '\n'.join([
        '# A01 여덟 번째 최종 회차 기능: 남은 조건을 직접 묻기', '',
        f"**상태:** 국소 Blueprint `{b['status']}` / 기능 `{data['status']}`. 선택된 가상 문의 행동과 현재 원천의 일치만 검증한다. 새 작가 잠금·전체 G13·원고 허가는 아니다.", '',
        '## 연속 입력과 단일 기능', '',
        f"- E7 전체 종료 입력: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- 선택: {data['unit_choice']}",
        f"- A1: {b['beats'][0]['action']} → {b['beats'][0]['observable_result']}",
        f"- A2: {b['beats'][1]['action']} → {b['beats'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 종료: {data['exit_state']}",
        f"- 독자 질문: {data['reader_question_at_end']}", '',
        '## 권위와 인계', '',
        '- 한국 학교 담당자는 자기 학교 기록의 일반 절차만 설명한다. 실제 학생 기록·소급 정정·미국 학점 인정·입학 권한을 부여하지 않는다.',
        '- CF12의 이동 의사와 미완성 준비는 미실행 후보다. 짧은 후보 진입 요약을 이번 기능 전체 출구의 검증된 투영으로 사용하지 않는다.',
        '- 이미 잠긴 2016년 3월 가상 프렙 이동 방향은 유지하지만 이번 기능에서 실제 입학·서류·비자·학점·보호자 동의를 완료했다고 주장하지 않는다.',
        '- S2 전체 종료와 S3 전체 진입/종료는 여전히 미인증이다.',
        f"- 계획 A01 36슬롯 중 기능 배정 8, 남은 {data['slot_accounting']['remaining_planned_slots']}; 출판 회차 번호는 미정.",
        '- 전체 G13/G14·실제 Context Pack·G15–G17·원고는 미완료, 설계/원고 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from current source-bound E8 function']


def self_test(data):
    mutations = [
        ('false author lock', lambda d: d.update(author_locked=True)),
        ('false whole G13', lambda d: d.update(whole_g13_complete=True)),
        ('false manuscript', lambda d: d.update(manuscript_allowed=True)),
        ('candidate summary instead of E7 full exit', lambda d: d.update(entry_state=d['next_unit']['candidate_entry_non_authoritative_summary'])),
        ('false Blueprint lock', lambda d: d['local_blueprint'].update(author_locked=True)),
        ('false S3 full exit', lambda d: d.update(S3_full_entry_or_exit_certified=True)),
        ('false Korean record issuance', lambda d: d['institutional_limits'].update(real_Korean_school_record_issued_or_verified=True)),
        ('false prep admission', lambda d: d['institutional_limits'].update(fictional_US_prep_admission_or_credit_acceptance_certified=True)),
        ('false school power', lambda d: d['fictional_school_contact'].update(may_certify_US_prep_acceptance_or_credit_conversion=True)),
        ('execute CF12', lambda d: d['next_unit'].update(candidate_is_executed_here=True)),
        ('inflate slots', lambda d: d['slot_accounting'].update(assigned_function_slots_through_this=36)),
        ('false source SHA', lambda d: d['source_rev_sha256'].update({'canon/CAREER_TIMELINE.md': '0' * 64})),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        assert validate(candidate), name
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
        saved = load(ROOT, OUTPUT)
        errors.extend(validate(saved))
        if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'function': data['episode_function_id'],
                      'local_blueprint': data['local_blueprint']['status'],
                      'local_complete': 1, 'whole_g13_complete': False,
                      'negative_controls': tested, 'current': not errors,
                      'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
