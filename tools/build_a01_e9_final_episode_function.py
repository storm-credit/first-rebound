"""Build ninth A01 function for the protagonist's bounded prep-move intent."""

import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_a01_cf12_move_intent_working_model as working
import build_a01_e8_final_episode_function as e8


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_E9_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A01_E9_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a01_e9_final_episode_function.py',
    'design/A01_CF12_MOVE_INTENT_WORKING_MODEL_2026_10_07.json',
    'design/A01_E8_FINAL_EPISODE_FUNCTION.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/STORY_BIBLE.md',
    'canon/CAREER_TIMELINE.md',
    'canon/PROJECT_FREEZE.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, e8.OUTPUT)
    selected = load(root, working.OUTPUT)
    packet = load(root, 'design/CP2_ACT_SUBACT_PACKET.json')
    assert not e8.validate(previous, root=root), 'E8 source-current function is stale'
    assert not working.validate(selected, root=root), 'CF12 selected source is stale'
    assert previous['episode_function_id'] == 'A01-EF-008'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (8, 8)
    assert previous['whole_g13_complete'] is False
    assert selected['status'] == 'ROUTINE_MOVE_INTENT_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert selected['source_function'] == 'A01-CF12'
    assert selected['target_subact'] == 'A01-S3'
    assert selected['entry_state'] == previous['exit_state']
    assert selected['prior_S2_whole_subact_exit_certified'] is False
    assert selected['S3_full_entry_or_exit_certified'] is False
    assert selected['relative_time_window']['after_E8_exit'] is True
    assert selected['relative_time_window']['before_locked_2016_03_prep_move'] is True
    assert selected['route_reapproval_required'] is False
    assert selected['institutional_limits']['Korean_coach_can_approve_prep_admission_or_credit'] is False
    assert selected['institutional_limits']['actual_US_prep_admission_or_enrollment_certified'] is False
    assert selected['institutional_limits']['actual_departure_or_A02_arrival_certified'] is False
    assert selected['actual_verified_blueprint_created'] is False
    assert selected['final_episode_function_added'] == 0
    assert selected['author_locked'] is False
    assert selected['manuscript_allowed'] is False
    assert [step['id'] for step in selected['event_steps']] == ['D1', 'D2']
    assert all(step['classification'] == 'ROUTINE_FICTIONAL_DESIGN'
               for step in selected['event_steps'])
    next_subact = next(s for s in packet['subacts'] if s['id'] == 'A02-S1')
    assert next_subact['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert next_subact['window'] == '2016.03–2017.06'
    assert next_subact['title'] == '편입과 학사'
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
            'protagonist_access': '자신의 E8 미답 목록·현재 선택·감독에게 전한 자기 의사에 한정',
            'source_path': str(working.OUTPUT).replace('\\', '/'),
            'source_step': step['id'],
            'author_locked': False,
        })
    blueprint = {
        'schema': 'A01_CF12_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_LOCAL_ROUTINE_DESIGN_ONLY_NOT_AUTHOR_LOCK_OR_FULL_G13',
        'source_currentness': 'Reviewed CF12 move intent and E8 full exit validated against current source files',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': copy.deepcopy(source_hashes),
        'entry_state': previous['exit_state'],
        'single_function': selected['single_function'],
        'unit_choice': '미답 조건을 보존한 채 기존 가상 프렙 이동 방향을 준비할 의사를 정하고 한국 감독에게 전한다',
        'exit_state': selected['selected_design_exit_state'],
        'beat_count': 2,
        'beats': beats,
        'partial_order': ['E8 full exit < D1 intent with open conditions < D2 statement to existing Korean coach < 2016-03 transfer window'],
        'direct_present_cost': selected['direct_present_cost'],
        'existing_locked_route': selected['existing_locked_route'],
        'relative_time_window': copy.deepcopy(selected['relative_time_window']),
        'information_access': copy.deepcopy(selected['information_access']),
        'institutional_limits': copy.deepcopy(selected['institutional_limits']),
        'unassigned_details': copy.deepcopy(selected['unassigned_details']),
        'S2_whole_completion_certified': False,
        'S3_full_entry_or_exit_certified': False,
        'actual_prep_admission_or_departure_certified': False,
        'author_locked': False,
        'manuscript_allowed': False,
    }
    assigned = previous['slot_accounting']['assigned_function_slots_through_this'] + 1
    assert assigned == 9
    planned = previous['slot_accounting']['a01_planned_slots']
    assert planned == 36
    return {
        'schema': 'A01_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A01-EF-009',
        'act': 'A01', 'primary_subact': 'A01-S3',
        'source_conditional_function': 'A01-CF12',
        'final_function_order': 9,
        'planned_allocation_slot': 9,
        'published_episode_number': None,
        'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': planned,
            'prior_function_slots': 8,
            'this_function_slots': 1,
            'assigned_function_slots_through_this': assigned,
            'remaining_planned_slots': planned - assigned,
            'allocation_is_final_published_episode_count': False,
        },
        'final_episode_functions_completed_this_record': 1,
        'local_contiguous_functions_through_this': 9,
        'previous_function': {
            'id': previous['episode_function_id'],
            'path': str(e8.OUTPUT).replace('\\', '/'),
            'exit_state': previous['exit_state'],
        },
        'local_blueprint': blueprint,
        'single_function': blueprint['single_function'],
        'entry_state': blueprint['entry_state'],
        'unit_choice': blueprint['unit_choice'],
        'exit_state': blueprint['exit_state'],
        'direct_present_cost': blueprint['direct_present_cost'],
        'reader_question_at_end': selected['reader_question_at_end'],
        'internal_order': ['D1', 'D2'],
        'beats': copy.deepcopy(beats),
        'next_unit': {
            'candidate_id': 'A02-S1',
            'candidate_status': next_subact['status'],
            'candidate_window': next_subact['window'],
            'candidate_entry_non_authoritative_summary': next_subact['entry_state'],
            'candidate_summary_is_exact_or_verified_projection': False,
            'exact_full_entry_if_next_unit_selected': blueprint['exit_state'],
            'candidate_is_executed_here': False,
            'candidate_is_final_episode_function': False,
            'prep_arrival_and_academic_conditions_resolved': False,
        },
        'existing_locked_route': blueprint['existing_locked_route'],
        'relative_time_window': copy.deepcopy(blueprint['relative_time_window']),
        'information_access': copy.deepcopy(blueprint['information_access']),
        'institutional_limits': copy.deepcopy(blueprint['institutional_limits']),
        'unassigned_details': copy.deepcopy(blueprint['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': source_hashes,
        'verification_limits': [
            'ACTUAL_VERIFIED only means this local Blueprint matches reviewed intent design and current sources.',
            'The March 2016 fictional prep move direction was previously author locked; this unit adds only the protagonist intent.',
            'The Korean coach receives intent without prep admissions, credit, guardian, visa or departure authority.',
            'E8 open questions persist; A02 school arrival and academic conditions are not certified here.',
            'S2 whole completion and S3 full entry/exit remain unverified despite this local function.',
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
        '# A01 아홉 번째 최종 회차 기능: 미답을 안고 방향을 말하기', '',
        f"**상태:** 국소 Blueprint `{b['status']}` / 기능 `{data['status']}`. 기존 미국행 정본 안에서 주인공 의사 행동의 현재성만 검증한다. 새 작가 잠금·전체 G13·원고 허가는 아니다.", '',
        '## 연속 입력과 단일 기능', '',
        f"- E8 전체 종료 입력: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- 선택: {data['unit_choice']}",
        f"- D1: {b['beats'][0]['action']} → {b['beats'][0]['observable_result']}",
        f"- D2: {b['beats'][1]['action']} → {b['beats'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 종료: {data['exit_state']}",
        f"- 독자 질문: {data['reader_question_at_end']}", '',
        '## 권위와 인계', '',
        '- 기존 감독에게 말한 의사는 실제 학교 수락·보호자 동의·개별 학점 인정·비자·출국이 아니다. 국내 관계의 실제 단절도 선지급하지 않는다.',
        '- A02-S1은 아직 미실행 잠정 단위다. 그 짧은 진입 요약을 E9의 전체 출구로 인증하지 않으며 실제 프렙 도착·학사 조건은 후속 과제다.',
        '- S2 전체 종료와 S3 전체 진입/종료는 여전히 미인증이다.',
        f"- 계획 A01 36슬롯 중 기능 배정 9, 남은 {data['slot_accounting']['remaining_planned_slots']}; 출판 회차 번호는 미정.",
        '- 전체 G13/G14·실제 Context Pack·G15–G17·원고는 미완료, 설계/원고 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from current source-bound E9 function']


def self_test(data):
    mutations = [
        ('false author lock', lambda d: d.update(author_locked=True)),
        ('false whole G13', lambda d: d.update(whole_g13_complete=True)),
        ('false manuscript', lambda d: d.update(manuscript_allowed=True)),
        ('candidate summary instead of E8 full exit', lambda d: d.update(entry_state=d['next_unit']['candidate_entry_non_authoritative_summary'])),
        ('false Blueprint lock', lambda d: d['local_blueprint'].update(author_locked=True)),
        ('false S3 full exit', lambda d: d.update(S3_full_entry_or_exit_certified=True)),
        ('false prep admission', lambda d: d['institutional_limits'].update(actual_US_prep_admission_or_enrollment_certified=True)),
        ('false departure', lambda d: d['institutional_limits'].update(actual_departure_or_A02_arrival_certified=True)),
        ('false coach power', lambda d: d['institutional_limits'].update(Korean_coach_can_approve_prep_admission_or_credit=True)),
        ('execute A02', lambda d: d['next_unit'].update(candidate_is_executed_here=True)),
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
