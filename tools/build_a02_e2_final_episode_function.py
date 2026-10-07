"""Build second A02 local function for one academic help opportunity lost."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e1_final_episode_function as previous_builder
import build_a02_cf02_lost_help_window_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_E2_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A02_E2_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a02_e2_final_episode_function.py',
    str(previous_builder.OUTPUT).replace('\\', '/'),
    str(working_builder.OUTPUT).replace('\\', '/'),
    'design/A02_PREP_CONDITIONAL_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'canon/STORY_BIBLE.md',
    'research/COLLEGE_EXIT_PACKET.md',
    'canon/PROJECT_FREEZE.md',
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
    assert not previous_builder.validate(previous, root=root), 'A02 E1 source stale'
    assert not working_builder.validate(selected, root=root), 'reviewed CF02 source stale'
    assert previous['episode_function_id'] == 'A02-EF-001'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (10, 37)
    assert previous['whole_A02_S1_exit_certified'] is False
    assert previous['whole_g13_complete'] is False
    assert selected['status'] == 'ROUTINE_ONE_LOST_SUPPORT_WINDOW_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert selected['prior_CF01_full_exit'] == previous['exit_state']
    assert selected['lost_opportunity_kind'] == 'FICTIONAL_SCHEDULED_ACADEMIC_HELP_FOLLOWUP_ONE_WINDOW'
    assert selected['next_candidate']['one_missed_window_retroactively_recovered'] is False
    assert selected['next_candidate']['habit_correction_executed_here'] is False
    assert selected['final_episode_function_added'] == 0
    assert selected['actual_verified_blueprint_created'] is False
    assert selected['whole_A02_S1_exit_certified'] is False
    assert selected['author_locked'] is False and selected['manuscript_allowed'] is False
    assert [s['id'] for s in selected['event_steps']] == ['W1', 'W2', 'W3']
    assert all(s['classification'] == 'ROUTINE_FICTIONAL_DESIGN' for s in selected['event_steps'])
    a02 = next(a for a in structure['acts'] if a['id'] == 'A02')
    s1 = next(s for s in structure['subacts'] if s['id'] == 'A02-S1')
    assert (a02['planned_units'], a02['allocation_start'], a02['allocation_end']) == (54, 37, 90)
    assert s1['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert structure['planned_episode_outlines_completed'] == 0
    cf03 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF03')
    assert cf03['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf03['selected_event'] is False and cf03['author_locked'] is False
    hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
              for p in SOURCES}
    beats = [{
        'id': s['id'], 'classification': s['classification'],
        'action': s['action'], 'observable_result': s['observable_result'],
        'choice_options': copy.deepcopy(s.get('choice_options')),
        'selected_choice': s.get('selected_choice'), 'not_claimed': s['not_claimed'],
        'source_path': str(working_builder.OUTPUT).replace('\\', '/'),
        'source_step': s['id'], 'author_locked': False,
    } for s in selected['event_steps']]
    blueprint = {
        'schema': 'A02_CF02_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_LOCAL_FICTIONAL_DESIGN_NOT_SCHOOL_DISCIPLINE_OR_NCAA',
        'entry_state': previous['exit_state'],
        'single_function': selected['single_function'],
        'unit_choice': selected['event_steps'][1]['selected_choice'],
        'exit_state': selected['selected_design_exit_state'],
        'lost_opportunity_kind': selected['lost_opportunity_kind'],
        'lost_opportunity_scope': selected['lost_opportunity_scope'],
        'beat_count': 3, 'beats': beats,
        'partial_order': ['A02 E1 full exit < W1 scheduled help < W2 games and postponed sleep < W3 missed one scheduled window; exact date and clock unassigned'],
        'direct_present_cost': selected['direct_present_cost'],
        'reader_question_at_end': selected['reader_question_at_end'],
        'information_access': copy.deepcopy(selected['information_access']),
        'institutional_limits': copy.deepcopy(selected['institutional_limits']),
        'unassigned_details': copy.deepcopy(selected['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': copy.deepcopy(hashes),
        'one_window_retroactively_restored': False,
        'later_help_permanently_denied': False,
        'habit_correction_executed': False,
        'whole_A02_S1_exit_certified': False,
        'author_locked': False, 'manuscript_allowed': False,
    }
    return {
        'schema': 'A02_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A02-EF-002', 'act': 'A02', 'primary_subact': 'A02-S1',
        'source_conditional_function': 'A02-CF02',
        'final_function_order': 11, 'planned_allocation_slot': 38,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
            'a01_unassigned_planned_slots': 27,
            'a01_unassigned_slots_require_27_new_events_before_this': False,
            'a02_planned_slots': 54, 'a02_assigned_function_slots_through_this': 2,
            'a02_remaining_planned_slots': 52,
            'total_local_functions_through_this': 11,
            'allocation_is_final_published_episode_count': False,
        },
        'final_episode_functions_completed_this_record': 1,
        'previous_function': {'id': previous['episode_function_id'],
                              'path': str(previous_builder.OUTPUT).replace('\\', '/'),
                              'exact_full_exit': previous['exit_state']},
        'local_blueprint': blueprint,
        'single_function': blueprint['single_function'],
        'entry_state': blueprint['entry_state'], 'unit_choice': blueprint['unit_choice'],
        'exit_state': blueprint['exit_state'],
        'lost_opportunity_kind': blueprint['lost_opportunity_kind'],
        'direct_present_cost': blueprint['direct_present_cost'],
        'reader_question_at_end': blueprint['reader_question_at_end'],
        'internal_order': ['W1', 'W2', 'W3'], 'beats': copy.deepcopy(beats),
        'next_unit': {
            'candidate_id': 'A02-CF03', 'candidate_status': cf03['status'],
            'candidate_entry_non_authoritative_summary': cf03['entry_state'],
            'candidate_summary_is_exact_or_verified_projection': False,
            'exact_full_entry_if_next_unit_selected': blueprint['exit_state'],
            'candidate_is_executed_here': False,
            'one_window_retroactively_restored': False,
            'habit_correction_executed_here': False,
        },
        'information_access': copy.deepcopy(blueprint['information_access']),
        'institutional_limits': copy.deepcopy(blueprint['institutional_limits']),
        'unassigned_details': copy.deepcopy(blueprint['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'ACTUAL_VERIFIED authenticates one current fictional function, not a real student attendance or academic record.',
            'Exactly one scheduled academic help opportunity is lost after the protagonist requested it; later help remains possible.',
            'The lost time is not retroactively restored or inflated into discipline, GPA, roster, minutes, graduation or NCAA failure.',
            'CF03 one-day obligation-first action remains unexecuted in this function.',
            'A01 unassigned planned slots do not mandate extra events and A02 S1 whole exit remains unverified.',
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
        '# A02 두 번째 국소 회차 기능: 잃은 학업 도움 시간', '',
        '**상태:** `FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE` / 국소 Blueprint `ACTUAL_VERIFIED`. 기존 정본·독립 검문된 가상 설계의 현재성만 확인한다. 실제 학교기록·학점·징계·NCAA·A02-S1 전체·전체 G13·원고 인증은 아니다.', '',
        '## 한 기능과 비용', '',
        f"- A02 E1 정확 출구: {data['entry_state']}",
        f"- 기능: {data['single_function']}",
        f"- W1: {data['beats'][0]['action']} → {data['beats'][0]['observable_result']}",
        f"- W2: {data['beats'][1]['action']} → {data['beats'][1]['observable_result']}",
        f"- W3: {data['beats'][2]['action']} → {data['beats'][2]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 정확한 국소 출구: {data['exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 배분과 경계', '',
        '- 전체 국소 기능 순서 11, A02 계획 슬롯 38, A02에서 배정한 기능 2개다. A01 미배정 27계획 슬롯을 새 사건 의무로 바꾸지 않는다. 출판 회차번호·실제 분량은 미정이다.',
        '- 한 번의 예약 도움 시간은 실제로 지나가며 소급 복구하지 않는다. 이후 도움을 영구 박탈하거나 학업·농구 자격을 실패로 확정하지 않는다.',
        '- 다음 CF03의 의무 우선 행동은 이 기능에서 실행되지 않는다. 실제 Context Pack·원고0, 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound second A02 function']


def self_test(data):
    mutations = [
        ('erase actual lost opportunity', lambda d: d['next_unit'].update(one_window_retroactively_restored=True)),
        ('permanent help denial', lambda d: d['local_blueprint'].update(later_help_permanently_denied=True)),
        ('fake NCAA decision', lambda d: d['institutional_limits'].update(NCAA_full_qualifier_decision_certified=True)),
        ('fake school discipline', lambda d: d['institutional_limits'].update(school_discipline_or_actual_attendance_record_certified=True)),
        ('prepay CF03', lambda d: d['next_unit'].update(habit_correction_executed_here=True)),
        ('make candidate summary exact', lambda d: d['next_unit'].update(candidate_summary_is_exact_or_verified_projection=True)),
        ('false full S1', lambda d: d.update(whole_A02_S1_exit_certified=True)),
        ('false manuscript', lambda d: d.update(manuscript_allowed=True)),
        ('wrong slot', lambda d: d.update(planned_allocation_slot=10)),
        ('wrong prior exit', lambda d: d.update(entry_state='도움을 거절했다')),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_working_load = working_builder.load
    def reversed_cf02(root, path):
        source = original_working_load(root, path)
        if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
            source = copy.deepcopy(source)
            next(f for f in source['functions'] if f['id'] == 'A02-CF02')['choice'] = '게임을 멈춰 기회를 잃지 않는다'
        return source
    with patch.object(working_builder, 'load', side_effect=reversed_cf02):
        assert validate(data), 'CF02 same-ID choice reversal'
    return len(mutations) + 1


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
                      'negative_controls': tested, 'current': not errors, 'errors': errors},
                     ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
