"""Build tenth A02 local function from the reviewed college transition model."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e9_final_episode_function as previous_builder
import build_a02_cf10_college_transition_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_E10_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A02_E10_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a02_e10_final_episode_function.py',
    str(previous_builder.OUTPUT).replace('\\', '/'),
    str(working_builder.OUTPUT).replace('\\', '/'),
    'design/A02_PREP_CONDITIONAL_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/STORY_BIBLE.md',
    'canon/CAREER_TIMELINE.md',
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
    # CF10 validates this same full E9 source object. A second tree traversal is redundant.
    assert previous == working_builder.load(root, previous_builder.OUTPUT), 'E9 input differs from CF10 validation input'
    assert not working_builder.validate(selected, root=root), 'reviewed CF10 source stale'
    assert previous['episode_function_id'] == 'A02-EF-009'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (18, 45)
    assert previous['next_unit']['candidate_id'] == 'A02-CF10'
    assert previous['next_unit']['candidate_is_executed_here'] is False
    assert previous['whole_A02_S3_exit_certified'] is False
    assert previous['whole_g13_complete'] is False and previous['manuscript_allowed'] is False
    assert selected['status'] == 'ROUTINE_COLLEGE_TRANSITION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert selected['prior_A02_E9_exact_full_exit'] == previous['exit_state']
    assert selected['entry_state'] == previous['exit_state']
    assert selected['candidate_entry_summary_is_exact_projection'] is False
    assert [m['id'] for m in selected['institutional_sequence']] == ['I1', 'I2', 'I3', 'I4']
    i1, i2, i3, i4 = selected['institutional_sequence']
    assert (i1['scope'], i2['scope']) == ('A02_S3', 'A02_S3')
    assert i1['offer_in_fiction'] and i1['admission_in_fiction']
    assert i2['graduation_in_fiction'] and i2['final_transcript_sent_in_fiction']
    assert i3['scope'] == 'INTER_ACT_INSTITUTIONAL_BRIDGE_NOT_A02_EPISODE_DATE'
    assert i3['eligibility_center_academic_and_athletics_certified_in_fiction'] is True
    assert i3['actual_private_ncaa_decision_or_villanova_record_certified'] is False
    assert i4['scope'] == 'A03_ENTRY_PREREQUISITE_NOT_A02_EPISODE_EVENT'
    assert i4['enrollment_or_first_game_executed_here'] is False
    assert i4['starter_or_unrestricted_minutes_guaranteed'] is False
    assert selected['final_episode_function_added'] == 0
    assert selected['whole_A02_S3_exit_certified'] is False
    assert selected['manuscript_allowed'] is False
    a02 = next(a for a in structure['acts'] if a['id'] == 'A02')
    s3 = next(s for s in structure['subacts'] if s['id'] == 'A02-S3')
    assert (a02['planned_units'], a02['allocation_start'], a02['allocation_end']) == (54, 37, 90)
    assert s3['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert s3['window'] == '2016.03–2017.06'
    assert structure['planned_episode_outlines_completed'] == 0
    hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
              for p in SOURCES}
    beats = [
        {'id': 'C1', 'classification': 'LOCKED_ROUTE_FICTIONAL_INSTITUTION_NOTICE',
         'action': '주인공은 2017년 늦은 봄 Villanova의 체육장학금 오퍼와 입학 승인이라는 기관별 통지를 받는다',
         'observable_result': '영입·입학 경로는 열렸지만 아직 학교 졸업과 NCAA 최종 인증은 남아 있다',
         'source_milestone': 'I1', 'not_claimed': '즉시 대학 주전·무제한 출전·실제 2017 기록'},
        {'id': 'C2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
         'choice_options': copy.deepcopy(selected['student_choice']['options']),
         'selected_choice': selected['student_choice']['selected'],
         'action': selected['student_choice']['bounded_action'],
         'observable_result': selected['student_choice']['observable_result'],
         'source_step': 'STUDENT_CHOICE',
         'not_claimed': '대학 실전 안정성·주전·첫 출전'},
        {'id': 'C3', 'classification': 'LOCKED_ROUTE_FICTIONAL_SCHOOL_OUTCOME',
         'action': '주인공은 2017년 5~6월 가상 프렙의 조기졸업과 최종 성적표 제출 완료 안내를 받는다',
         'observable_result': '학교의 학적 몫이 완료됐지만 여름 NCAA Eligibility Center 및 Villanova compliance는 별도 순서에 있다',
         'source_milestone': 'I2', 'not_claimed': '당시 실제 학생 문서·개별 점수·NCAA 판정·대학 경기'},
    ]
    for beat in beats:
        beat['source_path'] = str(working_builder.OUTPUT).replace('\\', '/')
        beat['author_locked'] = False
    blueprint = {
        'schema': 'A02_CF10_LOCAL_BLUEPRINT_V1', 'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_FICTIONAL_SPRING_OFFER_AND_GRADUATION_NOT_PRIVATE_RECORD_OR_COLLEGE_GAME',
        'entry_state': previous['exit_state'],
        'single_function': selected['single_function'],
        'unit_choice': selected['student_choice']['selected'],
        'exit_state': selected['selected_design_exit_state'],
        'beat_count': 3, 'beats': copy.deepcopy(beats),
        'institutional_sequence': copy.deepcopy(selected['institutional_sequence']),
        'partial_order': copy.deepcopy(selected['partial_order']),
        'direct_present_cost': selected['student_choice']['direct_present_cost'],
        'reader_question_at_end': selected['reader_question_at_end'],
        'information_access': copy.deepcopy(selected['information_access']),
        'historical_rule_evidence': copy.deepcopy(selected['historical_rule_evidence']),
        'unassigned_details': copy.deepcopy(selected['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': copy.deepcopy(hashes),
        'summer_EC_or_compliance_executed_as_A02_beat': False,
        'A03_enrollment_or_first_official_game_executed_here': False,
        'whole_A02_S3_exit_certified': False,
        'author_locked': False, 'manuscript_allowed': False,
    }
    return {
        'schema': 'A02_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A02-EF-010', 'act': 'A02', 'primary_subact': 'A02-S3',
        'source_conditional_function': 'A02-CF10',
        'final_function_order': 19, 'planned_allocation_slot': 46,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
            'a01_unassigned_planned_slots': 27,
            'a01_unassigned_slots_require_27_new_events_before_this': False,
            'a02_planned_slots': 54, 'a02_assigned_function_slots_through_this': 10,
            'a02_remaining_planned_slots': 44,
            'total_local_functions_through_this': 19,
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
        'internal_order': ['C1', 'C2', 'C3'], 'beats': copy.deepcopy(beats),
        'next_unit': {
            'id': 'A03-S1', 'status': 'NEXT_ACT_DEPENDENCY_NOT_EXECUTED_HERE',
            'summer_EC_and_Villanova_compliance_fictional_bridge_selected': True,
            'summer_bridge_executed_as_A02_beat': False,
            'enrollment_or_official_college_game_executed_here': False,
            'college_start_or_roster_role_certified_here': False,
            'exact_full_entry_for_A03_requires_separate_function_review': True,
        },
        'information_access': copy.deepcopy(blueprint['information_access']),
        'historical_rule_evidence': copy.deepcopy(blueprint['historical_rule_evidence']),
        'unassigned_details': copy.deepcopy(blueprint['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'ACTUAL_VERIFIED authenticates this local source-current design, not a real student, private Villanova/NCAA record, or a published chapter.',
            'Spring fictional Villanova offer/admission and May–June fictional prep graduation/final transcript are distinct institutional outcomes; exact dates and personal metrics remain null.',
            'Summer EC/compliance is a selected inter-act bridge after the A02 June window, not one of these three A02 beats; A03 enrollment and official play require separate later function review.',
            'A late athletic scholarship and admission do not guarantee college starting status, minutes, or competitive results.',
            'The whole A02-S3 exit and G13 remain unverified until parent audits all dependencies and registers the function.',
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
        '# A02 열 번째 국소 회차 기능: 프렙 졸업과 Villanova 경로', '',
        '**상태:** `FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE` / 국소 Blueprint `ACTUAL_VERIFIED`. 가상 진학 경로의 현재 정본 일치만 검문하며 여름 인증을 A02 회차 사건으로 소급하지 않는다.', '',
        '## 세 행동·결과', '',
        f"- E9 정확 출구: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- C1: {data['beats'][0]['action']} → {data['beats'][0]['observable_result']}",
        f"- C2: {data['beats'][1]['action']} → {data['beats'][1]['observable_result']}",
        f"- C3: {data['beats'][2]['action']} → {data['beats'][2]['observable_result']}",
        f"- 지금 비용: {data['direct_present_cost']}",
        f"- 정확 국소 출구: {data['exit_state']}", '',
        '## 다음 의존과 범위', '',
        '- 전체 국소 기능 순서 19, A02 계획 슬롯 46, A02 내 열 번째 배정. 계획 슬롯이 공개 회차번호나 새 사건 의무는 아니다.',
        '- 봄 Villanova 영입·입학과 5–6월 학교 졸업·성적표는 허구 기관의 결과다. 여름 EC/compliance는 A02 회차 바깥 연결 조건이고 A03 등록·공식 출전은 아직 별도 기능이다.',
        '- 개인 과목 환산·정확 GPA/SAT·실제 기관 문서·장학금 counter·대학 주전이나 경기 성적은 인증하지 않는다.',
        '- A02-S3 전체 출구, 전체 G13·Context Pack·원고는 미완료이고 게이트는 `CLOSED`다.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound tenth A02 function']


def self_test(data):
    changes = [
        ('fake real student', lambda d: d['local_blueprint']['institutional_sequence'][0].update(actual_real_student_or_2017_archival_record_certified=True)),
        ('prepay summer as episode', lambda d: d['local_blueprint'].update(summer_EC_or_compliance_executed_as_A02_beat=True)),
        ('prepay college game', lambda d: d['next_unit'].update(enrollment_or_official_college_game_executed_here=True)),
        ('claim starter', lambda d: d['local_blueprint']['institutional_sequence'][3].update(starter_or_unrestricted_minutes_guaranteed=True)),
        ('invent individual GPA', lambda d: d['unassigned_details'].update(core_gpa_exact=2.75)),
        ('invent counter', lambda d: d['unassigned_details'].update(villanova_scholarship_counter_exact_reconstruction=13)),
        ('claim whole S3', lambda d: d.update(whole_A02_S3_exit_certified=True)),
        ('inflate slots', lambda d: d['slot_accounting'].update(a02_assigned_function_slots_through_this=54)),
        ('manuscript open', lambda d: d.update(manuscript_allowed=True)),
    ]
    for name, mutate in changes:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    old_loader = working_builder.load

    def wrong_e9(root, path):
        source = old_loader(root, path)
        if path == previous_builder.OUTPUT:
            source = copy.deepcopy(source)
            source['whole_g13_complete'] = True
        return source
    with patch.object(working_builder, 'load', side_effect=wrong_e9):
        assert validate(data), 'different E9 object in two consumers'

    def wrong_cf10_choice(root, path):
        source = old_loader(root, path)
        if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
            source = copy.deepcopy(source)
            next(f for f in source['functions'] if f['id'] == 'A02-CF10')['choice'] = '즉시 대학 주전과 공식 출전을 승인받는다'
        return source
    with patch.object(working_builder, 'load', side_effect=wrong_cf10_choice):
        assert validate(data), 'same-ID CF10 source choice reversal'
    return len(changes) + 2


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
