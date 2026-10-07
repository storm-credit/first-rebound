"""Build the first A02 local function after the reviewed fictional move bridge."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a01_e9_final_episode_function as previous_builder
import build_a02_cf01_academic_help_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_E1_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A02_E1_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a02_e1_final_episode_function.py',
    str(previous_builder.OUTPUT).replace('\\', '/'),
    str(working_builder.OUTPUT).replace('\\', '/'),
    str(working_builder.BRIDGE).replace('\\', '/'),
    'design/A02_PREP_CONDITIONAL_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/STORY_BIBLE.md',
    'canon/CAREER_TIMELINE.md',
    'canon/PROJECT_FREEZE.md',
    'research/COLLEGE_EXIT_PACKET.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, previous_builder.OUTPUT)
    selected = load(root, working_builder.OUTPUT)
    structure = load(root, 'design/CP2_ACT_SUBACT_PACKET.json')
    candidates = load(root, 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json')
    # CF01.validate rebuilds and validates the entire E9 predecessor. Match
    # the exact object consumed there instead of walking the ancestor chain twice.
    assert previous == working_builder.load(root, previous_builder.OUTPUT), \
        'E9 predecessor differs from CF01 validation input'
    assert not working_builder.validate(selected, root=root), 'CF01 selected design stale'
    assert previous['episode_function_id'] == 'A01-EF-009'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (9, 9)
    assert previous['whole_g13_complete'] is False
    assert selected['status'] == 'ROUTINE_PREP_ACADEMIC_HELP_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert selected['last_A01_full_exit'] == previous['exit_state']
    assert selected['bridge_steps_selected'] == ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']
    assert selected['bridge_real_case_certified'] is False
    assert selected['A02_provisional_entry_language_assumption_verified_by_E9'] is False
    assert selected['A02_S1_whole_entry_or_exit_certified'] is False
    assert selected['final_episode_function_added'] == 0
    assert selected['actual_verified_blueprint_created'] is False
    assert selected['author_locked'] is False and selected['manuscript_allowed'] is False
    assert [step['id'] for step in selected['event_steps']] == ['H1', 'H2']
    assert all(step['classification'] == 'ROUTINE_FICTIONAL_DESIGN'
               for step in selected['event_steps'])
    a02 = next(a for a in structure['acts'] if a['id'] == 'A02')
    s1 = next(s for s in structure['subacts'] if s['id'] == 'A02-S1')
    assert (a02['planned_units'], a02['allocation_start'], a02['allocation_end']) == (54, 37, 90)
    assert a02['status'] == 'CP2_PROVISIONAL_NOT_EPISODE_OUTLINE'
    assert s1['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert s1['window'] == '2016.03–2017.06'
    assert structure['planned_episode_outlines_completed'] == 0
    assert structure['final_episode_functions_completed'] >= 9
    cf02 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF02')
    assert cf02['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf02['selected_event'] is False and cf02['author_locked'] is False
    hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
              for p in SOURCES}
    beats = [{
        'id': step['id'], 'classification': step['classification'],
        'action': step['action'], 'observable_result': step['observable_result'],
        'choice_options': copy.deepcopy(step.get('choice_options')),
        'selected_choice': step.get('selected_choice'), 'not_claimed': step['not_claimed'],
        'source_path': str(working_builder.OUTPUT).replace('\\', '/'),
        'source_step': step['id'], 'author_locked': False,
    } for step in selected['event_steps']]
    blueprint = {
        'schema': 'A02_CF01_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_LOCAL_FICTIONAL_DESIGN_NOT_INDIVIDUAL_CASE_CERTIFICATION',
        'entry_previous_full_exit': previous['exit_state'],
        'intervening_fictional_authority_outcomes': ['F1', 'F2', 'F3', 'F4', 'F5', 'F6'],
        'intervening_bridge_source': str(working_builder.BRIDGE).replace('\\', '/'),
        'entry_state': selected['entry_state_after_fictional_bridge'],
        'A02_provisional_entry_language_assumption_verified_by_E9': False,
        'single_function': selected['single_function'],
        'unit_choice': selected['event_steps'][1]['selected_choice'],
        'exit_state': selected['selected_design_exit_state'],
        'beats': beats, 'beat_count': 2,
        'partial_order': ['E9 full exit < F1/F2 < F3 < F4 < F5 < F6 < H1 < H2; exact days unassigned'],
        'direct_present_cost': selected['direct_present_cost'],
        'reader_question_at_end': selected['reader_question_at_end'],
        'information_access': copy.deepcopy(selected['information_access']),
        'institutional_limits': copy.deepcopy(selected['institutional_limits']),
        'unassigned_details': copy.deepcopy(selected['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': copy.deepcopy(hashes),
        'whole_A01_act_or_A02_S1_exit_certified': False,
        'real_prep_or_student_case_certified': False,
        'author_locked': False, 'manuscript_allowed': False,
    }
    return {
        'schema': 'A02_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A02-EF-001', 'act': 'A02', 'primary_subact': 'A02-S1',
        'source_conditional_function': 'A02-CF01',
        'final_function_order': 10, 'planned_allocation_slot': 37,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
            'a01_unassigned_planned_slots': 27,
            'a01_unassigned_slots_require_27_new_events_before_this': False,
            'a02_planned_slots': 54, 'a02_first_slot': 37,
            'a02_assigned_function_slots_through_this': 1,
            'a02_remaining_planned_slots': 53,
            'total_local_functions_through_this': 10,
            'allocation_is_final_published_episode_count': False,
        },
        'final_episode_functions_completed_this_record': 1,
        'previous_function': {
            'id': previous['episode_function_id'],
            'path': str(previous_builder.OUTPUT).replace('\\', '/'),
            'exact_full_exit': previous['exit_state'],
            'intervening_outcomes_are_not_E9_actions': True,
        },
        'local_blueprint': blueprint,
        'single_function': blueprint['single_function'],
        'entry_previous_full_exit': blueprint['entry_previous_full_exit'],
        'entry_after_fictional_bridge': blueprint['entry_state'],
        'intervening_fictional_authority_outcomes': blueprint['intervening_fictional_authority_outcomes'],
        'unit_choice': blueprint['unit_choice'], 'exit_state': blueprint['exit_state'],
        'direct_present_cost': blueprint['direct_present_cost'],
        'reader_question_at_end': blueprint['reader_question_at_end'],
        'internal_order': ['H1', 'H2'], 'beats': copy.deepcopy(beats),
        'next_unit': {
            'candidate_id': 'A02-CF02', 'candidate_status': cf02['status'],
            'candidate_entry_non_authoritative_summary': cf02['entry_state'],
            'candidate_summary_is_exact_or_verified_projection': False,
            'exact_full_entry_if_next_unit_selected': blueprint['exit_state'],
            'candidate_is_executed_here': False,
            'actual_lost_opportunity_kind_selected_here': False,
        },
        'information_access': copy.deepcopy(blueprint['information_access']),
        'institutional_limits': copy.deepcopy(blueprint['institutional_limits']),
        'unassigned_details': copy.deepcopy(blueprint['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'ACTUAL_VERIFIED authenticates current source projection of one local fictional function, not real admissions, visa, credit or NCAA certification.',
            'A01 E9 intent and later F1–F6 fictional institutional outcomes are distinct; neither is silently inferred from the other.',
            'A02 provisional language misunderstanding is not treated as verified by E9 or automatically cured by this help request.',
            'A01 planned slots 10–36 remain unassigned but do not require invented functions before this A02 local unit.',
            'CF02 actual lost opportunity and subsequent habit change are unexecuted.',
        ],
        'whole_A01_act_exit_certified': False,
        'whole_A02_S1_exit_certified': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'g15_complete': False,
        'g16_complete': False, 'g17_complete': False,
        'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }


def render(data):
    return '\n'.join([
        '# A02 첫 국소 회차 기능: 학업 도움 요청', '',
        '**상태:** `FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE` / 국소 Blueprint `ACTUAL_VERIFIED`. 이 확인은 현행 원천과 가상 설계의 일치를 뜻한다. A01 전체 종료, A02-S1 전체 종료, 실제 학생 서류·입학·비자·학점·NCAA 자격, 전체 G13, 원고는 인증하지 않는다.', '',
        '## 정확한 진입 연결', '',
        f"- A01 E9 전체 출구: {data['entry_previous_full_exit']}",
        '- E9 의사와 별개로 기존 잠긴 2016년 3월 이동을 구현하는 가상 권한 결과 F1/F2→F3→F4→F5→F6를 거친다. F1/F2 세부 순서는 미정이고 실물 문서·실재 학교 기록 인증은 없다.',
        f"- A02 이 국소 기능의 시작: {data['entry_after_fictional_bridge']}", '',
        '## 기능과 선택', '',
        f"- 한 기능: {data['single_function']}",
        f"- H1: {data['beats'][0]['action']} → {data['beats'][0]['observable_result']}",
        f"- H2: {data['beats'][1]['action']} → {data['beats'][1]['observable_result']}",
        f"- 현재 비용: {data['direct_present_cost']}",
        f"- 정확한 국소 출구: {data['exit_state']}",
        f"- 다음 독자 질문: {data['reader_question_at_end']}", '',
        '## 계획 배분과 경계', '',
        '- 전체 국소 기능 순서 10, A02 첫 계획 슬롯 37이다. A01 계획 36칸 중 앞서 배정한 것은 9칸, 미배정 27칸이 남는다. 이 27칸은 27개 새 사건 의무나 출판 회차 27개를 뜻하지 않는다.',
        '- A02-CF02의 게임·수면 실패, 잃은 기회 종류와 이후 생활 순서는 이 기능에서 실행하지 않는다. A02 잠정 진입의 생활 영어/학업 자격 혼동도 E9가 증명한 상태로 소급하지 않는다.',
        '- [가상 전환 권한](../research/A01_A02_PREP_TRANSITION_AUTHORITY_BOUNDARY_2026_10_07.md)은 실재 사례 인증이 아니다. 학업 담당자의 도움은 학교 졸업감사·대학 입학·NCAA Eligibility Center 결정을 대체하지 않는다.',
        '- 실제 Context Pack·원고 0, 설계/원고 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound first A02 function']


def self_test(data):
    mutations = [
        ('collapse E9 intent into school admission', lambda d: d['previous_function'].update(intervening_outcomes_are_not_E9_actions=False)),
        ('false real prep case', lambda d: d['local_blueprint'].update(real_prep_or_student_case_certified=True)),
        ('false credit decision', lambda d: d['institutional_limits'].update(individual_Korean_course_conversion_certified=True)),
        ('false NCAA decision', lambda d: d['institutional_limits'].update(prep_adviser_certifies_NCAA_full_qualifier=True)),
        ('promote prior language summary', lambda d: d['local_blueprint'].update(A02_provisional_entry_language_assumption_verified_by_E9=True)),
        ('execute CF02 early', lambda d: d['next_unit'].update(candidate_is_executed_here=True)),
        ('invent lost opportunity', lambda d: d['next_unit'].update(actual_lost_opportunity_kind_selected_here=True)),
        ('inflate A01 slots', lambda d: d['slot_accounting'].update(a01_locally_assigned_function_slots=36)),
        ('wrong A02 slot', lambda d: d.update(planned_allocation_slot=10)),
        ('false whole G13', lambda d: d.update(whole_g13_complete=True)),
        ('false manuscript', lambda d: d.update(manuscript_allowed=True)),
        ('E9 full exit replaced by candidate summary', lambda d: d.update(entry_previous_full_exit='생활 영어를 학업 자격과 혼동')),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_working_load = working_builder.load
    def reversed_cf01(root, path):
        source = original_working_load(root, path)
        if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
            source = copy.deepcopy(source)
            next(f for f in source['functions'] if f['id'] == 'A02-CF01')['choice'] = '학업 담당자에게 묻지 않고 숨긴다'
        return source
    with patch.object(working_builder, 'load', side_effect=reversed_cf01):
        assert validate(data), 'CF01 academic choice reversal'
    original_load = load
    def executed_cf02(root, path):
        source = original_load(root, path)
        if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
            source = copy.deepcopy(source)
            next(f for f in source['functions'] if f['id'] == 'A02-CF02')['selected_event'] = True
        return source
    with patch(__name__ + '.load', side_effect=executed_cf02):
        assert validate(data), 'CF02 source candidate cannot become executed'
    def mismatched_e9(root, path):
        source = original_load(root, path)
        if path == previous_builder.OUTPUT:
            source = copy.deepcopy(source)
            source['source_rev_sha256']['canon/STORY_BIBLE.md'] = '0' * 64
        return source
    with patch(__name__ + '.load', side_effect=mismatched_e9):
        assert validate(data), 'E9 full-object mismatch between two loaders'
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
    print(json.dumps({'local_function_order': data['final_function_order'],
                      'allocation_slot': data['planned_allocation_slot'],
                      'negative_controls': tested, 'current': not errors,
                      'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
