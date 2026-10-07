"""Build the source-current local CF10 Blueprint and seventh A01 function.

The 2016 fictional prep move is already canon. This one function selects a
bounded information comparison, without certifying either entire subact or
any admission, school record, player ranking, or manuscript.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_a01_cf10_prep_comparison_working_model as working
import build_a01_e6_final_episode_function as e6


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_E7_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A01_E7_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a01_e7_final_episode_function.py',
    'design/A01_CF10_PREP_COMPARISON_WORKING_MODEL_2026_10_07.json',
    'design/A01_E6_FINAL_EPISODE_FUNCTION.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'research/A01_CF10_2015_PREP_COMPETITION_SOURCE_2026_10_07.json',
    'canon/STORY_BIBLE.md',
    'canon/CAREER_TIMELINE.md',
    'canon/PROJECT_FREEZE.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF11_CAUSE = '농구 과제로 이동을 생각해도 학생 신분과 실제 이동 조건은 별개로 남는다'
CF11_CHOICE = '학업·서류 준비를 요구받아 설명을 들으며 본인이 확인할 항목을 정리하고 불명확한 조건을 질문한다'


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, e6.OUTPUT)
    selected = load(root, working.OUTPUT)
    candidates = load(root, 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json')
    # The CF builder validates the same full predecessor; do not traverse it twice.
    # Independent loader patches must not substitute a different predecessor.
    assert previous == working.load(root, e6.OUTPUT), 'predecessor input differs from CF validation input'
    assert not working.validate(selected, root=root), 'CF10 selected source is stale'
    assert previous['episode_function_id'] == 'A01-EF-006'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (6, 6)
    assert previous['whole_g13_complete'] is False
    assert selected['status'] == 'ROUTINE_COMPARISON_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert selected['source_function'] == 'A01-CF10'
    assert selected['target_subact'] == 'A01-S3'
    assert selected['entry_state'] == previous['exit_state']
    assert selected['prior_S2_whole_subact_exit_certified'] is False
    assert selected['S3_full_entry_or_exit_certified'] is False
    assert selected['relative_time_window']['after_E6_exit'] is True
    assert selected['relative_time_window']['after_2015_NEPSAC_final_date'] == '2015-03-08'
    assert selected['relative_time_window']['no_later_than'] == '2016-02'
    assert selected['fictional_information_delivery']['classification'] == 'ROUTINE_FICTIONAL_DESIGN_NOT_HISTORICAL_DOCUMENT_ACCESS_PROOF'
    assert selected['fictional_information_delivery']['exact_official_pdf_or_2022_URL_seen_by_character'] is False
    assert selected['competition_source']['US_individual_skill_superiority_proved'] is False
    assert selected['institutional_limits']['actual_application_or_acceptance_certified'] is False
    assert selected['actual_verified_blueprint_created'] is False
    assert selected['final_episode_function_added'] == 0
    assert selected['author_locked'] is False
    assert selected['manuscript_allowed'] is False
    assert [step['id'] for step in selected['event_steps']] == ['Q1', 'Q2']
    assert all(step['classification'].startswith('ROUTINE_FICTIONAL_DESIGN')
               for step in selected['event_steps'])
    assert '동일한 시간' in selected['direct_present_cost']
    cf11 = next(f for f in candidates['functions'] if f['id'] == 'A01-CF11')
    assert cf11['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf11['evidence_class'] == 'CANDIDATE'
    assert cf11['selected_event'] is False
    assert cf11['author_locked'] is False
    assert cf11['subact'] == 'A01-S3'
    assert cf11['cause'] == CF11_CAUSE
    assert cf11['choice'] == CF11_CHOICE
    assert cf11['next'] == 'A01-CF12'
    source_hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
                     for p in SOURCES}
    beats = []
    for step in selected['event_steps']:
        beats.append({
            'id': step['id'],
            'classification': step['classification'],
            'action': step['action'],
            'observable_result': step['observable_result'],
            'choice_options': copy.deepcopy(step.get('choice_options')),
            'selected_choice': step.get('selected_choice'),
            'not_claimed': step['not_claimed'],
            'protagonist_access': '전달받은 대진 구조와 자신의 T2/C2/E4 경험 및 모르는 항목에 한정',
            'source_path': str(working.OUTPUT).replace('\\', '/'),
            'source_step': step['id'],
            'author_locked': False,
        })
    blueprint = {
        'schema': 'A01_CF10_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_LOCAL_ROUTINE_DESIGN_ONLY_NOT_AUTHOR_LOCK_OR_FULL_G13',
        'source_currentness': 'Selected CF10 comparison, E6 full exit and official source limits validated against current files',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': copy.deepcopy(source_hashes),
        'entry_state': previous['exit_state'],
        'single_function': selected['single_function'],
        'unit_choice': '익숙한 즉시 승부의 한 기회 대신 전달된 2015 대회 구조와 자기 T2/C2/E4 수행을 그 시간에 대조한다',
        'exit_state': selected['selected_design_exit_state'],
        'beat_count': 2,
        'beats': beats,
        'partial_order': [
            'E6 full exit < Q1 supplied structure < Q2 self comparison',
            '2015-03-08 tournament end < Q1 supplied structure',
            'Q2 self comparison < 2016-02 window end',
            'E6 full exit versus 2015-03-08 tournament end: order unassigned',
        ],
        'direct_present_cost': selected['direct_present_cost'],
        'existing_locked_route': selected['existing_locked_route'],
        'competition_source': copy.deepcopy(selected['competition_source']),
        'fictional_information_delivery': copy.deepcopy(selected['fictional_information_delivery']),
        'relative_time_window': copy.deepcopy(selected['relative_time_window']),
        'personal_comparison_inputs': copy.deepcopy(selected['personal_comparison_inputs']),
        'information_access': copy.deepcopy(selected['information_access']),
        'institutional_limits': copy.deepcopy(selected['institutional_limits']),
        'unassigned_details': copy.deepcopy(selected['unassigned_details']),
        'S2_whole_completion_certified': False,
        'S3_full_entry_or_exit_certified': False,
        'actual_prep_admission_or_school_records_certified': False,
        'author_locked': False,
        'manuscript_allowed': False,
    }
    assigned = previous['slot_accounting']['assigned_function_slots_through_this'] + 1
    assert assigned == 7
    planned = previous['slot_accounting']['a01_planned_slots']
    assert planned == 36
    return {
        'schema': 'A01_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A01-EF-007',
        'act': 'A01', 'primary_subact': 'A01-S3',
        'source_conditional_function': 'A01-CF10',
        'final_function_order': 7,
        'planned_allocation_slot': 7,
        'published_episode_number': None,
        'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': planned,
            'prior_function_slots': 6,
            'this_function_slots': 1,
            'assigned_function_slots_through_this': assigned,
            'remaining_planned_slots': planned - assigned,
            'allocation_is_final_published_episode_count': False,
        },
        'final_episode_functions_completed_this_record': 1,
        'local_contiguous_functions_through_this': 7,
        'previous_function': {
            'id': previous['episode_function_id'],
            'path': str(e6.OUTPUT).replace('\\', '/'),
            'exit_state': previous['exit_state'],
        },
        'local_blueprint': blueprint,
        'single_function': blueprint['single_function'],
        'entry_state': blueprint['entry_state'],
        'unit_choice': blueprint['unit_choice'],
        'exit_state': blueprint['exit_state'],
        'direct_present_cost': blueprint['direct_present_cost'],
        'reader_question_at_end': selected['reader_question_at_end'],
        'internal_order': ['Q1', 'Q2'],
        'beats': copy.deepcopy(beats),
        'next_unit': {
            'candidate_id': 'A01-CF11',
            'candidate_status': cf11['status'],
            'candidate_subact': cf11['subact'],
            'candidate_entry_non_authoritative_summary': cf11['entry_state'],
            'candidate_summary_is_exact_or_verified_projection': False,
            'exact_full_entry_if_next_unit_selected': blueprint['exit_state'],
            'candidate_is_executed_here': False,
            'candidate_is_final_episode_function': False,
            'academic_transfer_requirements_resolved': False,
        },
        'existing_locked_route': blueprint['existing_locked_route'],
        'competition_source': copy.deepcopy(blueprint['competition_source']),
        'fictional_information_delivery': copy.deepcopy(blueprint['fictional_information_delivery']),
        'relative_time_window': copy.deepcopy(blueprint['relative_time_window']),
        'personal_comparison_inputs': copy.deepcopy(blueprint['personal_comparison_inputs']),
        'information_access': copy.deepcopy(blueprint['information_access']),
        'institutional_limits': copy.deepcopy(blueprint['institutional_limits']),
        'unassigned_details': copy.deepcopy(blueprint['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': source_hashes,
        'verification_limits': [
            'ACTUAL_VERIFIED only means this local Blueprint matches current selected design and source revisions.',
            'The 2015 bracket proves competition structure, not US-player superiority or exact 2015 URL access.',
            'The Korean-language coach handout is new fictional design, not historical school knowledge or admissions authority.',
            'Q1 and Q2 use one foregone familiar contest opportunity and serve one comparison function.',
            'The existing March 2016 fictional prep move does not certify application, credits, visa, admission or roster role here.',
            'S2 whole completion and S3 full entry/exit remain unverified; CF11 remains a conditional candidate.',
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
        '# A01 일곱 번째 최종 회차 기능: 미국행의 배울 이유', '',
        f"**상태:** 국소 Blueprint `{b['status']}` / 기능 `{data['status']}`. 선택된 가상 비교 설계와 현재 원천의 일치만 검증한다. 새 작가 잠금·전체 G13·원고 허가는 아니다.", '',
        '## 연속 입력과 단일 기능', '',
        f"- E6 전체 종료 입력: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- 선택: {data['unit_choice']}",
        f"- Q1: {b['beats'][0]['action']} → {b['beats'][0]['observable_result']}",
        f"- Q2: {b['beats'][1]['action']} → {b['beats'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 종료: {data['exit_state']}",
        f"- 독자 질문: {data['reader_question_at_end']}", '',
        '## 근거와 인계 범위', '',
        '- [NEPSAC 2015 대진 자료](../research/A01_CF10_2015_PREP_COMPETITION_SOURCE_2026_10_07.md)는 여섯 등급의 대회 구조만 입증한다. 미국 선수의 개인 기술 우위나 2015년 정확 웹주소 열람을 입증하지 않는다.',
        '- 기존 한국 고교 감독의 한국어 한 장 전달은 가상 설계다. 역사적 감독 지식·학교 입학 권한·실제 입학 통지를 만들지 않는다.',
        '- CF11 학업·이동 조건은 미실행 후보다. 후보의 짧은 진입 요약은 이 기능 전체 출구의 검증된 투영이 아니다.',
        '- S2 전체 종료와 S3 전체 진입/종료를 인증하지 않는다. 기존 2016년 3월 미국 프렙 이동 방향과 이번 한 기능을 구별한다.',
        f"- 계획 A01 36슬롯 중 기능 배정 7, 남은 {data['slot_accounting']['remaining_planned_slots']}; 출판 회차 번호는 미정.",
        '- 전체 G13/G14·실제 Context Pack·G15–G17·원고는 미완료, 설계/원고 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from current source-bound E7 function']


def self_test(data):
    mutations = [
        ('false author lock', lambda d: d.update(author_locked=True)),
        ('false whole G13', lambda d: d.update(whole_g13_complete=True)),
        ('false manuscript', lambda d: d.update(manuscript_allowed=True)),
        ('candidate summary instead of E6 full exit', lambda d: d.update(entry_state=d['next_unit']['candidate_entry_non_authoritative_summary'])),
        ('false Blueprint lock', lambda d: d['local_blueprint'].update(author_locked=True)),
        ('false S2 whole completion', lambda d: d.update(prior_S2_whole_completion_certified=True)),
        ('false S3 full exit', lambda d: d['local_blueprint'].update(S3_full_entry_or_exit_certified=True)),
        ('US superiority claim', lambda d: d['competition_source'].update(US_individual_skill_superiority_proved=True)),
        ('false exact 2015 URL access', lambda d: d['competition_source'].update(exact_2022_archive_url_viewed_in_2015_certified=True)),
        ('false admission', lambda d: d['institutional_limits'].update(actual_application_or_acceptance_certified=True)),
        ('execute CF11', lambda d: d['next_unit'].update(candidate_is_executed_here=True)),
        ('two full costs', lambda d: d.update(direct_present_cost='Q1 비용만 있고 Q2 비용은 없다')),
        ('inflate slots', lambda d: d['slot_accounting'].update(assigned_function_slots_through_this=36)),
        ('false source revision', lambda d: d['source_rev_sha256'].update({'canon/STORY_BIBLE.md': '0' * 64})),
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
