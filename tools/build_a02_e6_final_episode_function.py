"""Build sixth A02 local function from reviewed cause comparison and retry."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e5_final_episode_function as previous_builder
import build_a02_cf06_cause_and_retry_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_E6_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A02_E6_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a02_e6_final_episode_function.py',
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
    # CF06 checks this entire E5 source object. Guard equality between loaders.
    assert previous == working_builder.load(root, previous_builder.OUTPUT), 'E5 input differs from CF06 validation input'
    assert not working_builder.validate(selected, root=root), 'reviewed CF06 source stale'
    assert previous['episode_function_id'] == 'A02-EF-005'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (14, 41)
    assert previous['whole_A02_S2_exit_certified'] is False
    assert previous['whole_g13_complete'] is False and previous['manuscript_allowed'] is False
    assert selected['status'] == 'ROUTINE_PREP_CAUSE_COMPARISON_AND_RETRY_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert selected['prior_A02_E5_exact_full_exit'] == previous['exit_state']
    assert selected['entry_state'] == previous['exit_state']
    assert selected['candidate_entry_summary_is_exact_projection'] is False
    assert selected['information_source_authority']['earlier_CF04_or_CF05_personal_practice_recording_retroactively_asserted'] is False
    assert selected['information_source_authority']['clip_is_actual_2016_real_school_archive'] is False
    assert selected['information_source_authority']['clip_proves_protagonist_game_performance'] is False
    assert selected['retry_authority']['prior_CF05_practice_permission_automatically_extended'] is False
    assert selected['retry_authority']['official_team_roster_or_game_permission'] is False
    assert selected['next_candidate']['recommendation_or_actual_evaluation_executed_here'] is False
    assert selected['final_episode_function_added'] == 0
    assert selected['whole_A02_S2_exit_certified'] is False
    assert selected['author_locked'] is False and selected['manuscript_allowed'] is False
    assert [s['id'] for s in selected['event_steps']] == ['C1', 'C2']
    assert all(s['classification'] == 'ROUTINE_FICTIONAL_DESIGN' for s in selected['event_steps'])
    a02 = next(a for a in structure['acts'] if a['id'] == 'A02')
    s2 = next(s for s in structure['subacts'] if s['id'] == 'A02-S2')
    assert (a02['planned_units'], a02['allocation_start'], a02['allocation_end']) == (54, 37, 90)
    assert s2['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert structure['planned_episode_outlines_completed'] == 0
    cf07 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF07')
    assert cf07['subact'] == 'A02-S3'
    assert cf07['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf07['selected_event'] is False and cf07['author_locked'] is False
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
        'schema': 'A02_CF06_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_LOCAL_FICTIONAL_COACHING_AND_RETRY_NOT_GAME_OR_EVALUATION_PROOF',
        'entry_state': previous['exit_state'],
        'single_function': selected['single_function'],
        'information_source_authority': copy.deepcopy(selected['information_source_authority']),
        'retry_authority': copy.deepcopy(selected['retry_authority']),
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
        'prior_CF05_practice_permission_extended': False,
        'personal_prior_video_or_actual_game_certified': False,
        'whole_A02_S2_exit_certified': False,
        'author_locked': False, 'manuscript_allowed': False,
    }
    return {
        'schema': 'A02_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A02-EF-006', 'act': 'A02', 'primary_subact': 'A02-S2',
        'source_conditional_function': 'A02-CF06',
        'final_function_order': 15, 'planned_allocation_slot': 42,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
            'a01_unassigned_planned_slots': 27,
            'a01_unassigned_slots_require_27_new_events_before_this': False,
            'a02_planned_slots': 54, 'a02_assigned_function_slots_through_this': 6,
            'a02_remaining_planned_slots': 48,
            'total_local_functions_through_this': 15,
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
        'internal_order': ['C1', 'C2'], 'beats': copy.deepcopy(beats),
        'next_unit': {
            'candidate_id': 'A02-CF07', 'candidate_subact': 'A02-S3',
            'candidate_status': cf07['status'],
            'candidate_entry_non_authoritative_summary': cf07['entry_state'],
            'candidate_summary_is_exact_or_verified_projection': False,
            'exact_full_entry_if_next_unit_selected': blueprint['exit_state'],
            'candidate_is_executed_here': False,
            'recommendation_or_actual_evaluation_verified_here': False,
        },
        'information_access': copy.deepcopy(blueprint['information_access']),
        'information_source_authority': copy.deepcopy(blueprint['information_source_authority']),
        'retry_authority': copy.deepcopy(blueprint['retry_authority']),
        'unassigned_details': copy.deepcopy(blueprint['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'ACTUAL_VERIFIED authenticates local source-current fictional comparison and one retry, not actual prior personal video, roster or game.',
            'The cue is bounded to a corner-return task; it does not prove timely defensive success or general paint-help error.',
            'CF05 permission does not carry over; CF06 needs a separate fictional supervised basic retry.',
            'CF07 recommendation and actual evaluation, qualification and the whole A02-S2 exit remain unexecuted or unverified.',
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
        '# A02 여섯 번째 국소 회차 기능: 실패 원인의 대조와 한정 재시도', '',
        '**상태:** `FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE` / 국소 Blueprint `ACTUAL_VERIFIED`. 가상 모델의 원천 현재성만 인증하며 실제 경기·학교기록, 전체 G13, 작가 잠금이나 원고를 인증하지 않는다.', '',
        '## 기능과 경계', '',
        f"- A02 E5 정확 출구: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- C1: {data['beats'][0]['action']} → {data['beats'][0]['observable_result']}",
        f"- C2: {data['beats'][1]['action']} → {data['beats'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 정확한 국소 출구: {data['exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 배분과 다음 후보', '',
        '- 전체 국소 기능 순서 15, A02 계획 슬롯 42, A02 내 여섯 번째 배정이다. A01의 미배정 계획 칸을 새 사건 의무로 만들지 않으며 공개 회차번호·원고 분량은 정하지 않는다.',
        '- 허용된 일반 시범 영상은 과거 개인 훈련 촬영본이나 실제 2016 실학교 자료가 아니다. 앞 훈련 허가를 자동 연장하지 않으며 다음 한정 기본 시도는 제때 수비·경기 성과를 인증하지 않는다.',
        '- CF07의 추천·평가 경로는 아직 미실행이다. A02-S2 전체 출구, 전체 G13·Context Pack·원고는 미완료이고 게이트는 `CLOSED`다.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound sixth A02 function']


def self_test(data):
    mutations = [
        ('invent personal practice video', lambda d: d['information_source_authority'].update(earlier_CF04_or_CF05_personal_practice_recording_retroactively_asserted=True)),
        ('claim real archive', lambda d: d['local_blueprint']['information_source_authority'].update(clip_is_actual_2016_real_school_archive=True)),
        ('claim game proof', lambda d: d['information_source_authority'].update(clip_proves_protagonist_game_performance=True)),
        ('extend CF05 permission', lambda d: d['retry_authority'].update(prior_CF05_practice_permission_automatically_extended=True)),
        ('execute CF07', lambda d: d['next_unit'].update(candidate_is_executed_here=True)),
        ('promote candidate entry', lambda d: d['next_unit'].update(candidate_summary_is_exact_or_verified_projection=True)),
        ('claim whole S2', lambda d: d.update(whole_A02_S2_exit_certified=True)),
        ('inflate allocated count', lambda d: d['slot_accounting'].update(a02_assigned_function_slots_through_this=54)),
        ('authorize manuscript', lambda d: d.update(manuscript_allowed=True)),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    old_loader = working_builder.load

    def wrong_e5(root, path):
        source = old_loader(root, path)
        if path == previous_builder.OUTPUT:
            source = copy.deepcopy(source)
            source['whole_g13_complete'] = True
        return source
    with patch.object(working_builder, 'load', side_effect=wrong_e5):
        assert validate(data), 'different E5 object in two consumers'

    def wrong_cf06_choice(root, path):
        source = old_loader(root, path)
        if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
            source = copy.deepcopy(source)
            next(f for f in source['functions'] if f['id'] == 'A02-CF06')['choice'] = '영상을 한 번 보고 모든 포지션을 숙달한다'
        return source
    with patch.object(working_builder, 'load', side_effect=wrong_cf06_choice):
        assert validate(data), 'same-ID CF06 choice reversal'
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
