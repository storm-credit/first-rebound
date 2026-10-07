"""Build fourth A02 local function from the reviewed small-big practice failure."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e3_final_episode_function as previous_builder
import build_a02_cf04_small_big_failure_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_E4_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A02_E4_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a02_e4_final_episode_function.py',
    str(previous_builder.OUTPUT).replace('\\', '/'),
    str(working_builder.OUTPUT).replace('\\', '/'),
    'design/A02_PREP_CONDITIONAL_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/TALENT_BQ_MODEL.md',
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
    # CF04 validates the same complete E3 object; check both loaders see that object.
    assert previous == working_builder.load(root, previous_builder.OUTPUT), 'E3 input differs from CF04 validation input'
    assert not working_builder.validate(selected, root=root), 'reviewed CF04 source stale'
    assert previous['episode_function_id'] == 'A02-EF-003'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (12, 39)
    assert previous['whole_A02_S1_exit_certified'] is False
    assert previous['whole_g13_complete'] is False and previous['manuscript_allowed'] is False
    assert selected['status'] == 'ROUTINE_PREP_POSITION_MISMATCH_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert selected['prior_A02_E3_exact_full_exit'] == previous['exit_state']
    assert selected['entry_state'] == previous['exit_state']
    assert selected['candidate_entry_summary_is_exact_projection'] is False
    assert selected['session_authority']['prior_E3_one_day_permission_automatically_extended'] is False
    assert selected['session_authority']['official_team_roster_or_game_permission'] is False
    assert selected['bounded_drill_setup']['paint_help_is_always_wrong'] is False
    assert selected['bounded_drill_setup']['official_game_or_measured_defensive_result'] is False
    assert selected['next_candidate']['wing_basic_repetition_or_success_executed_here'] is False
    assert selected['final_episode_function_added'] == 0
    assert selected['whole_A02_S2_exit_certified'] is False
    assert selected['author_locked'] is False and selected['manuscript_allowed'] is False
    assert [s['id'] for s in selected['event_steps']] == ['B1', 'B2']
    assert all(s['classification'] == 'ROUTINE_FICTIONAL_DESIGN' for s in selected['event_steps'])
    a02 = next(a for a in structure['acts'] if a['id'] == 'A02')
    s2 = next(s for s in structure['subacts'] if s['id'] == 'A02-S2')
    assert (a02['planned_units'], a02['allocation_start'], a02['allocation_end']) == (54, 37, 90)
    assert s2['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert structure['planned_episode_outlines_completed'] == 0
    cf05 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF05')
    assert cf05['subact'] == 'A02-S2'
    assert cf05['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf05['selected_event'] is False and cf05['author_locked'] is False
    hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
              for p in SOURCES}
    beats = [{
        'id': s['id'], 'classification': s['classification'],
        'action': s['action'], 'observable_result': s['observable_result'],
        'choice_options': copy.deepcopy(s.get('choice_options')),
        'selected_choice': s.get('selected_choice'),
        'not_claimed': s['not_claimed'],
        'source_path': str(working_builder.OUTPUT).replace('\\', '/'),
        'source_step': s['id'], 'author_locked': False,
    } for s in selected['event_steps']]
    blueprint = {
        'schema': 'A02_CF04_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_LOCAL_FICTIONAL_PRACTICE_NOT_ACTUAL_GAME_OR_SKILL_MASTERY',
        'entry_state': previous['exit_state'],
        'single_function': selected['single_function'],
        'bounded_drill_setup': copy.deepcopy(selected['bounded_drill_setup']),
        'session_authority': copy.deepcopy(selected['session_authority']),
        'unit_choice': selected['event_steps'][1]['selected_choice'],
        'exit_state': selected['selected_design_exit_state'],
        'beat_count': 2, 'beats': beats,
        'partial_order': copy.deepcopy(selected['partial_order']),
        'direct_present_cost': selected['direct_present_cost'],
        'reader_question_at_end': selected['reader_question_at_end'],
        'information_access': copy.deepcopy(selected['information_access']),
        'unassigned_details': copy.deepcopy(selected['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': copy.deepcopy(hashes),
        'prior_E3_session_permission_extended': False,
        'wing_repetition_or_game_result_certified': False,
        'whole_A02_S2_exit_certified': False,
        'author_locked': False, 'manuscript_allowed': False,
    }
    return {
        'schema': 'A02_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A02-EF-004', 'act': 'A02', 'primary_subact': 'A02-S2',
        'source_conditional_function': 'A02-CF04',
        'final_function_order': 13, 'planned_allocation_slot': 40,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
            'a01_unassigned_planned_slots': 27,
            'a01_unassigned_slots_require_27_new_events_before_this': False,
            'a02_planned_slots': 54, 'a02_assigned_function_slots_through_this': 4,
            'a02_remaining_planned_slots': 50,
            'total_local_functions_through_this': 13,
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
        'direct_present_cost': blueprint['direct_present_cost'],
        'reader_question_at_end': blueprint['reader_question_at_end'],
        'internal_order': ['B1', 'B2'], 'beats': copy.deepcopy(beats),
        'next_unit': {
            'candidate_id': 'A02-CF05', 'candidate_subact': 'A02-S2',
            'candidate_status': cf05['status'],
            'candidate_entry_non_authoritative_summary': cf05['entry_state'],
            'candidate_summary_is_exact_or_verified_projection': False,
            'exact_full_entry_if_next_unit_selected': blueprint['exit_state'],
            'candidate_is_executed_here': False,
            'wing_repetition_or_success_verified_here': False,
        },
        'information_access': copy.deepcopy(blueprint['information_access']),
        'session_authority': copy.deepcopy(blueprint['session_authority']),
        'unassigned_details': copy.deepcopy(blueprint['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'ACTUAL_VERIFIED authenticates source-current local fictional practice, not an actual roster, game or school case.',
            'E3’s one-day permission does not carry over; CF04 requires a separate bounded fictional coach-supervised practice permission.',
            'A weak-side corner late return is visible twice in this drill; paint help itself is not always wrong and the failure is not retrojected to C2.',
            'CF05 wing fundamentals, game proof, qualification and the entire A02-S2 exit remain unexecuted or unverified.',
        ],
        'whole_A01_act_exit_certified': False,
        'whole_A02_S1_exit_certified': False, 'whole_A02_S2_exit_certified': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'g15_complete': False,
        'g16_complete': False, 'g17_complete': False,
        'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }


def render(data):
    return '\n'.join([
        '# A02 네 번째 국소 회차 기능: 작은 빅맨 방식의 좁은 실패', '',
        '**상태:** `FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE` / 국소 Blueprint `ACTUAL_VERIFIED`. 독립 검문된 가상 모델의 현재성만 인증하며 실제 경기·학교기록, 전체 G13, 작가 잠금이나 원고를 인증하지 않는다.', '',
        '## 기능과 경계', '',
        f"- A02 E3 정확 출구: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- 한정 과제: {data['local_blueprint']['bounded_drill_setup']['coach_instruction']}",
        f"- B1: {data['beats'][0]['action']} → {data['beats'][0]['observable_result']}",
        f"- B2: {data['beats'][1]['action']} → {data['beats'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 정확한 국소 출구: {data['exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 배분과 다음 후보', '',
        '- 전체 국소 기능 순서 13, A02 계획 슬롯 40, A02 내 네 번째 배정이다. A01의 미배정 계획 칸은 새 사건 의무가 아니며 공개 회차번호·실제 원고 분량은 정하지 않는다.',
        '- E3의 하루 훈련 허가는 자동 연장되지 않는다. 새로 한정 허용된 가상 기본 훈련에서 코너 복귀가 두 번 늦은 것만 보이고 페인트 도움 일반 오답·과거 C2 실패를 단정하지 않는다.',
        '- CF05 윙 과제 반복·실제 경기/명단/학점·NCAA 판단은 미실행 또는 미인증이다. A02-S2 전체 출구, 전체 G13·Context Pack·원고는 미완료이고 게이트는 `CLOSED`다.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound fourth A02 function']


def self_test(data):
    mutations = [
        ('extend E3 permission', lambda d: d['session_authority'].update(prior_E3_one_day_permission_automatically_extended=True)),
        ('claim full game', lambda d: d['local_blueprint']['bounded_drill_setup'].update(official_game_or_measured_defensive_result=True)),
        ('claim all help wrong', lambda d: d['local_blueprint']['bounded_drill_setup'].update(paint_help_is_always_wrong=True)),
        ('claim wing success', lambda d: d['next_unit'].update(wing_repetition_or_success_verified_here=True)),
        ('execute CF05', lambda d: d['next_unit'].update(candidate_is_executed_here=True)),
        ('promote candidate summary', lambda d: d['next_unit'].update(candidate_summary_is_exact_or_verified_projection=True)),
        ('retroject C2', lambda d: d['beats'][0].update(observable_result='고교 C2에서 같은 실패를 이미 했다')),
        ('certify S2 whole exit', lambda d: d.update(whole_A02_S2_exit_certified=True)),
        ('inflate planned count', lambda d: d['slot_accounting'].update(a02_assigned_function_slots_through_this=54)),
        ('authorize manuscript', lambda d: d.update(manuscript_allowed=True)),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    old_loader = working_builder.load

    def wrong_e3(root, path):
        source = old_loader(root, path)
        if path == previous_builder.OUTPUT:
            source = copy.deepcopy(source)
            source['whole_g13_complete'] = True
        return source
    with patch.object(working_builder, 'load', side_effect=wrong_e3):
        assert validate(data), 'different E3 object in two consumers'
    old_source_loader = working_builder.load

    def wrong_cf04_choice(root, path):
        source = old_source_loader(root, path)
        if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
            source = copy.deepcopy(source)
            next(f for f in source['functions'] if f['id'] == 'A02-CF04')['choice'] = '처음부터 완벽한 윙 수비를 수행한다'
        return source
    with patch.object(working_builder, 'load', side_effect=wrong_cf04_choice):
        assert validate(data), 'same-ID CF04 choice reversal'
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
    print(json.dumps({'local_function_order': data['final_function_order'],
                      'allocation_slot': data['planned_allocation_slot'],
                      'negative_controls': tested, 'current': not errors,
                      'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
