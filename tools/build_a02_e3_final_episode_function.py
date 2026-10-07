"""Build third A02 local function for one day of obligations before gaming."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e2_final_episode_function as previous_builder
import build_a02_cf03_one_day_priority_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_E3_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A02_E3_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a02_e3_final_episode_function.py',
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
    assert not previous_builder.validate(previous, root=root), 'A02 E2 source stale'
    assert not working_builder.validate(selected, root=root), 'reviewed CF03 source stale'
    assert previous['episode_function_id'] == 'A02-EF-002'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (11, 38)
    assert previous['whole_A02_S1_exit_certified'] is False
    assert selected['status'] == 'ROUTINE_ONE_DAY_OBLIGATION_PRIORITY_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert selected['prior_CF02_full_exit'] == previous['exit_state']
    assert selected['lost_CF02_help_window_restored'] is False
    assert selected['institutional_day_path']['team_roster_or_game_authorization_certified'] is False
    assert selected['institutional_day_path']['school_authority_discards_CF02_missed_help_window'] is False
    assert selected['institutional_limits']['individual_attendance_or_grade_certified'] is False
    assert selected['institutional_limits']['team_registration_or_minutes_certified'] is False
    assert selected['institutional_limits']['NCAA_full_qualifier_or_graduation_certified'] is False
    assert selected['next_candidate']['basketball_position_performance_verified_here'] is False
    assert selected['final_episode_function_added'] == 0
    assert selected['whole_A02_S1_exit_certified'] is False
    assert selected['author_locked'] is False and selected['manuscript_allowed'] is False
    assert [s['id'] for s in selected['event_steps']] == ['P1', 'P2']
    assert all(s['classification'] == 'ROUTINE_FICTIONAL_DESIGN' for s in selected['event_steps'])
    a02 = next(a for a in structure['acts'] if a['id'] == 'A02')
    s1 = next(s for s in structure['subacts'] if s['id'] == 'A02-S1')
    assert (a02['planned_units'], a02['allocation_start'], a02['allocation_end']) == (54, 37, 90)
    assert s1['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert structure['planned_episode_outlines_completed'] == 0
    cf04 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF04')
    assert cf04['subact'] == 'A02-S2'
    assert cf04['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf04['selected_event'] is False and cf04['author_locked'] is False
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
        'schema': 'A02_CF03_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_LOCAL_FICTIONAL_DESIGN_NOT_HABIT_CURE_OR_ACTUAL_SCHOOL_RECORD',
        'entry_state': previous['exit_state'],
        'prior_lost_help_window_restored': False,
        'single_function': selected['single_function'],
        'unit_choice': selected['event_steps'][1]['selected_choice'],
        'exit_state': selected['selected_design_exit_state'],
        'beat_count': 2, 'beats': beats,
        'partial_order': copy.deepcopy(selected['partial_order']),
        'direct_present_cost': selected['direct_present_cost'],
        'reader_question_at_end': selected['reader_question_at_end'],
        'institutional_day_path': copy.deepcopy(selected['institutional_day_path']),
        'information_access': copy.deepcopy(selected['information_access']),
        'institutional_limits': copy.deepcopy(selected['institutional_limits']),
        'unassigned_details': copy.deepcopy(selected['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': copy.deepcopy(hashes),
        'long_term_habit_or_qualifier_certified': False,
        'whole_A02_S1_exit_certified': False,
        'author_locked': False, 'manuscript_allowed': False,
    }
    return {
        'schema': 'A02_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A02-EF-003', 'act': 'A02', 'primary_subact': 'A02-S1',
        'source_conditional_function': 'A02-CF03',
        'final_function_order': 12, 'planned_allocation_slot': 39,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
            'a01_unassigned_planned_slots': 27,
            'a01_unassigned_slots_require_27_new_events_before_this': False,
            'a02_planned_slots': 54, 'a02_assigned_function_slots_through_this': 3,
            'a02_remaining_planned_slots': 51,
            'total_local_functions_through_this': 12,
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
        'prior_lost_help_window_restored': False,
        'direct_present_cost': blueprint['direct_present_cost'],
        'reader_question_at_end': blueprint['reader_question_at_end'],
        'internal_order': ['P1', 'P2'], 'beats': copy.deepcopy(beats),
        'next_unit': {
            'candidate_id': 'A02-CF04', 'candidate_subact': 'A02-S2',
            'candidate_status': cf04['status'],
            'candidate_entry_non_authoritative_summary': cf04['entry_state'],
            'candidate_summary_is_exact_or_verified_projection': False,
            'exact_full_entry_if_next_unit_selected': blueprint['exit_state'],
            'candidate_is_executed_here': False,
            'basketball_position_performance_verified_here': False,
        },
        'information_access': copy.deepcopy(blueprint['information_access']),
        'institutional_limits': copy.deepcopy(blueprint['institutional_limits']),
        'unassigned_details': copy.deepcopy(blueprint['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'ACTUAL_VERIFIED authenticates one source-current fictional day, not a real attendance or eligibility record.',
            'The CF02 missed help time remains lost; this unit changes only one later day’s sequence.',
            'Required study hall and coach-permitted basic work precede optional gaming, without fixing their mutual clock order.',
            'One day does not certify sustained habit change, credits, graduation, NCAA qualification or basketball position skill.',
            'CF04 small-big-man performance candidate is not executed and A02-S1 whole exit is not certified.',
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
        '# A02 세 번째 국소 회차 기능: 의무를 먼저 하는 하루', '',
        '**상태:** `FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE` / 국소 Blueprint `ACTUAL_VERIFIED`. 기존 정본·검문된 가상 설계의 파일 현재성만 확인하며 실제 학생기록, 장기 습관 완치, NCAA 자격, A02-S1 전체, 원고를 인증하지 않는다.', '',
        '## 기능과 경계', '',
        f"- A02 E2 정확 출구: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- P1: {data['beats'][0]['action']} → {data['beats'][0]['observable_result']}",
        f"- P2: {data['beats'][1]['action']} → {data['beats'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 정확한 국소 출구: {data['exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 배분과 다음 후보', '',
        '- 전체 국소 기능 순서 12, A02 계획 슬롯 39, A02 내 세 번째 배정이다. A01의 27 미배정 계획 칸을 새 사건 의무로 읽지 않으며 공개 회차번호·실제 분량은 정하지 않는다.',
        '- CF02에서 놓친 한 예약 도움 시간은 소급 복구하지 않는다. 가상 학교 의무 스터디홀·감독 허용 기본 훈련의 한 번 실행만 보이고 실제 출석 기록·팀 등록·경기 출전·학점/NCAA 판단은 비운다.',
        '- A02-CF04의 농구 위치·판단 수행은 S2의 미실행 후보다. S1 전체 출구, 전체 G13·실제 Context Pack·원고는 미완료이고 게이트는 `CLOSED`다.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound third A02 function']


def self_test(data):
    mutations = [
        ('restore prior help window', lambda d: d.update(prior_lost_help_window_restored=True)),
        ('claim sustained habit cure', lambda d: d['local_blueprint'].update(long_term_habit_or_qualifier_certified=True)),
        ('claim attendance record', lambda d: d['institutional_limits'].update(individual_attendance_or_grade_certified=True)),
        ('claim team game status', lambda d: d['institutional_limits'].update(team_registration_or_minutes_certified=True)),
        ('claim NCAA qualifier', lambda d: d['institutional_limits'].update(NCAA_full_qualifier_or_graduation_certified=True)),
        ('execute CF04', lambda d: d['next_unit'].update(candidate_is_executed_here=True)),
        ('promote candidate entry summary', lambda d: d['next_unit'].update(candidate_summary_is_exact_or_verified_projection=True)),
        ('certify S1 whole exit', lambda d: d.update(whole_A02_S1_exit_certified=True)),
        ('inflate planned count', lambda d: d['slot_accounting'].update(a02_assigned_function_slots_through_this=54)),
        ('authorize manuscript', lambda d: d.update(manuscript_allowed=True)),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_working_load = working_builder.load
    def reversed_cf03(root, path):
        source = original_working_load(root, path)
        if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
            source = copy.deepcopy(source)
            next(f for f in source['functions'] if f['id'] == 'A02-CF03')['choice'] = '기상과 의무를 다시 미루고 게임한다'
        return source
    with patch.object(working_builder, 'load', side_effect=reversed_cf03):
        assert validate(data), 'CF03 same-ID choice reversal'
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
