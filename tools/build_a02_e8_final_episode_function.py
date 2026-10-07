"""Build eighth A02 local function from reviewed academic time-cost work."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e7_final_episode_function as previous_builder
import build_a02_cf08_academic_time_cost_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_E8_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A02_E8_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a02_e8_final_episode_function.py',
    str(previous_builder.OUTPUT).replace('\\', '/'),
    str(working_builder.OUTPUT).replace('\\', '/'),
    'design/A02_PREP_CONDITIONAL_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'canon/STORY_BIBLE.md',
    'research/COLLEGE_EXIT_PACKET.md',
    'research/TIMELINE_ELIGIBILITY_LEDGER.md',
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
    # CF08 validates this complete E7 object; both consumers must see it intact.
    assert previous == working_builder.load(root, previous_builder.OUTPUT), 'E7 input differs from CF08 validation input'
    assert not working_builder.validate(selected, root=root), 'reviewed CF08 source stale'
    assert previous['episode_function_id'] == 'A02-EF-007'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (16, 43)
    assert previous['whole_A02_S3_exit_certified'] is False
    assert previous['whole_g13_complete'] is False and previous['manuscript_allowed'] is False
    assert selected['status'] == 'ROUTINE_PREP_ACADEMIC_TIME_COST_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert selected['prior_A02_E7_exact_full_exit'] == previous['exit_state']
    assert selected['entry_state'] == previous['exit_state']
    assert selected['candidate_entry_summary_is_exact_projection'] is False
    assert selected['academic_authority']['coach_sets_or_certifies_courses_or_grades'] is False
    assert selected['academic_authority']['exact_course_ids_units_or_school_grades_selected'] is False
    assert selected['academic_authority']['student_NCAA_full_qualifier_or_Villanova_admission_certified'] is False
    assert selected['academic_authority']['prior_E7_college_receipt_or_response_inferred'] is False
    assert selected['next_candidate']['official_credits_graduation_or_eligibility_certified_here'] is False
    assert selected['final_episode_function_added'] == 0
    assert selected['whole_A02_S3_exit_certified'] is False
    assert selected['author_locked'] is False and selected['manuscript_allowed'] is False
    assert [s['id'] for s in selected['event_steps']] == ['S1', 'S2']
    assert all(s['classification'] == 'ROUTINE_FICTIONAL_DESIGN' for s in selected['event_steps'])
    a02 = next(a for a in structure['acts'] if a['id'] == 'A02')
    s3 = next(s for s in structure['subacts'] if s['id'] == 'A02-S3')
    assert (a02['planned_units'], a02['allocation_start'], a02['allocation_end']) == (54, 37, 90)
    assert s3['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert structure['planned_episode_outlines_completed'] == 0
    cf09 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF09')
    assert cf09['subact'] == 'A02-S3'
    assert cf09['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf09['selected_event'] is False and cf09['author_locked'] is False
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
        'schema': 'A02_CF08_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_LOCAL_FICTIONAL_STUDY_TIME_NOT_FINAL_CREDITS_OR_NCAA',
        'entry_state': previous['exit_state'],
        'single_function': selected['single_function'],
        'academic_authority': copy.deepcopy(selected['academic_authority']),
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
        'final_credit_or_exam_result_certified': False,
        'whole_A02_S3_exit_certified': False,
        'author_locked': False, 'manuscript_allowed': False,
    }
    return {
        'schema': 'A02_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A02-EF-008', 'act': 'A02', 'primary_subact': 'A02-S3',
        'source_conditional_function': 'A02-CF08',
        'final_function_order': 17, 'planned_allocation_slot': 44,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
            'a01_unassigned_planned_slots': 27,
            'a01_unassigned_slots_require_27_new_events_before_this': False,
            'a02_planned_slots': 54, 'a02_assigned_function_slots_through_this': 8,
            'a02_remaining_planned_slots': 46,
            'total_local_functions_through_this': 17,
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
        'internal_order': ['S1', 'S2'], 'beats': copy.deepcopy(beats),
        'next_unit': {
            'candidate_id': 'A02-CF09', 'candidate_subact': 'A02-S3',
            'candidate_status': cf09['status'],
            'candidate_entry_non_authoritative_summary': cf09['entry_state'],
            'candidate_summary_is_exact_or_verified_projection': False,
            'exact_full_entry_if_next_unit_selected': blueprint['exit_state'],
            'candidate_is_executed_here': False,
            'official_credit_graduation_or_eligibility_verified_here': False,
        },
        'information_access': copy.deepcopy(blueprint['information_access']),
        'academic_authority': copy.deepcopy(blueprint['academic_authority']),
        'unassigned_details': copy.deepcopy(blueprint['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'ACTUAL_VERIFIED authenticates source-current local fictional study action, not a final transcript, SAT result or university decision.',
            'The academic office plans category work; prep coach cannot certify courses or NCAA eligibility.',
            'Optional extra training and gaming time is spent on study without cancelling mandatory basketball or proving long-term habit cure.',
            'CF09 official documentation, the whole A02-S3 exit and G13 remain unexecuted or unverified.',
        ],
        'whole_A01_act_exit_certified': False,
        'whole_A02_S1_exit_certified': False, 'whole_A02_S2_exit_certified': False,
        'whole_A02_S3_exit_certified': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'g15_complete': False,
        'g16_complete': False, 'g17_complete': False,
        'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }


def render(data):
    return '\n'.join([
        '# A02 여덟 번째 국소 회차 기능: 학업·시험 준비의 시간 지불', '',
        '**상태:** `FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE` / 국소 Blueprint `ACTUAL_VERIFIED`. 가상 학업담당 계획 아래서 보인 공부 행동의 원천 현재성만 인증하며 점수·학점·대학 입학·원고를 인증하지 않는다.', '',
        '## 기능과 경계', '',
        f"- A02 E7 정확 출구: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- S1: {data['beats'][0]['action']} → {data['beats'][0]['observable_result']}",
        f"- S2: {data['beats'][1]['action']} → {data['beats'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 정확한 국소 출구: {data['exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 배분과 다음 후보', '',
        '- 전체 국소 기능 순서 17, A02 계획 슬롯 44, A02 내 여덟 번째 배정이다. 미배정 계획 칸을 새 사건 의무로 만들지 않으며 공개 회차번호·원고 분량은 정하지 않는다.',
        '- E7 자료의 대학 수신은 여전히 미확인이다. 학교 학업담당의 예비 계획과 스터디홀·시험 연습 실행만 보였고 정확 과목 이수·점수·NCAA·입학 결론은 비운다.',
        '- CF09 공식 학업 증빙, A02-S3 전체 출구, 전체 G13·Context Pack·원고는 미완료이고 게이트는 `CLOSED`다.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound eighth A02 function']


def self_test(data):
    mutations = [
        ('coach certifies credits', lambda d: d['academic_authority'].update(coach_sets_or_certifies_courses_or_grades=True)),
        ('invent SAT result', lambda d: d['unassigned_details'].update(grades_or_SAT_score=1320)),
        ('claim NCAA qualification', lambda d: d['local_blueprint']['academic_authority'].update(student_NCAA_full_qualifier_or_Villanova_admission_certified=True)),
        ('claim college receipt', lambda d: d['academic_authority'].update(prior_E7_college_receipt_or_response_inferred=True)),
        ('execute CF09', lambda d: d['next_unit'].update(candidate_is_executed_here=True)),
        ('promote candidate entry', lambda d: d['next_unit'].update(candidate_summary_is_exact_or_verified_projection=True)),
        ('claim S3 whole exit', lambda d: d.update(whole_A02_S3_exit_certified=True)),
        ('inflate planned count', lambda d: d['slot_accounting'].update(a02_assigned_function_slots_through_this=54)),
        ('authorize manuscript', lambda d: d.update(manuscript_allowed=True)),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    old_loader = working_builder.load

    def wrong_e7(root, path):
        source = old_loader(root, path)
        if path == previous_builder.OUTPUT:
            source = copy.deepcopy(source)
            source['whole_g13_complete'] = True
        return source
    with patch.object(working_builder, 'load', side_effect=wrong_e7):
        assert validate(data), 'different E7 object in two consumers'

    def wrong_cf08_choice(root, path):
        source = old_loader(root, path)
        if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
            source = copy.deepcopy(source)
            next(f for f in source['functions'] if f['id'] == 'A02-CF08')['choice'] = '감독 추천만 믿고 공부를 중단한다'
        return source
    with patch.object(working_builder, 'load', side_effect=wrong_cf08_choice):
        assert validate(data), 'same-ID CF08 choice reversal'
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
