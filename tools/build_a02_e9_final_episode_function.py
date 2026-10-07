"""Build ninth A02 local function from reviewed official-check preparation."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e8_final_episode_function as previous_builder
import build_a02_cf09_official_check_preparation_working_model as working_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_E9_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A02_E9_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a02_e9_final_episode_function.py',
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
    # CF09 validates the same complete E8 object read here.
    assert previous == working_builder.load(root, previous_builder.OUTPUT), 'E8 input differs from CF09 validation input'
    assert not working_builder.validate(selected, root=root), 'reviewed CF09 source stale'
    assert previous['episode_function_id'] == 'A02-EF-008'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (17, 44)
    assert previous['whole_A02_S3_exit_certified'] is False
    assert previous['whole_g13_complete'] is False and previous['manuscript_allowed'] is False
    assert selected['status'] == 'ROUTINE_PREP_OFFICIAL_CHECK_PREPARATION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert selected['prior_A02_E8_exact_full_exit'] == previous['exit_state']
    assert selected['entry_state'] == previous['exit_state']
    assert selected['candidate_entry_summary_is_exact_projection'] is False
    assert selected['authority_map']['prep_coach_issues_final_transcript_or_eligibility'] is False
    assert selected['authority_map']['school_final_transcript_or_diploma_issued_here'] is False
    assert selected['authority_map']['NCAA_eligibility_center_certified_here'] is False
    assert selected['authority_map']['Villanova_admission_or_compliance_decision_here'] is False
    assert selected['authority_map']['prior_E7_college_receipt_or_reply_inferred'] is False
    assert selected['next_candidate']['offer_admission_or_college_role_executed_here'] is False
    assert selected['final_episode_function_added'] == 0
    assert selected['whole_A02_S3_exit_certified'] is False
    assert selected['author_locked'] is False and selected['manuscript_allowed'] is False
    assert [s['id'] for s in selected['event_steps']] == ['D1', 'D2']
    assert all(s['classification'] == 'ROUTINE_FICTIONAL_DESIGN' for s in selected['event_steps'])
    a02 = next(a for a in structure['acts'] if a['id'] == 'A02')
    s3 = next(s for s in structure['subacts'] if s['id'] == 'A02-S3')
    assert (a02['planned_units'], a02['allocation_start'], a02['allocation_end']) == (54, 37, 90)
    assert s3['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert structure['planned_episode_outlines_completed'] == 0
    cf10 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF10')
    assert cf10['subact'] == 'A02-S3'
    assert cf10['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf10['selected_event'] is False and cf10['author_locked'] is False
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
        'schema': 'A02_CF09_LOCAL_BLUEPRINT_V1',
        'status': 'ACTUAL_VERIFIED',
        'authority_scope': 'SOURCE_CURRENT_STUDENT_CHECKLIST_AND_SCHOOL_PROCESS_REPLY_NOT_FINAL_CERTIFICATION',
        'entry_state': previous['exit_state'],
        'single_function': selected['single_function'],
        'authority_map': copy.deepcopy(selected['authority_map']),
        'unit_choice': selected['event_steps'][0]['selected_choice'],
        'exit_state': selected['selected_design_exit_state'],
        'beat_count': 2, 'beats': beats,
        'partial_order': copy.deepcopy(selected['partial_order']),
        'direct_present_cost': selected['direct_present_cost'],
        'reader_question_at_end': selected['reader_question_at_end'],
        'information_access': copy.deepcopy(selected['information_access']),
        'unassigned_details': copy.deepcopy(selected['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': copy.deepcopy(hashes),
        'final_school_or_NCAA_decision_certified': False,
        'whole_A02_S3_exit_certified': False,
        'author_locked': False, 'manuscript_allowed': False,
    }
    return {
        'schema': 'A02_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A02-EF-009', 'act': 'A02', 'primary_subact': 'A02-S3',
        'source_conditional_function': 'A02-CF09',
        'final_function_order': 18, 'planned_allocation_slot': 45,
        'published_episode_number': None, 'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36, 'a01_locally_assigned_function_slots': 9,
            'a01_unassigned_planned_slots': 27,
            'a01_unassigned_slots_require_27_new_events_before_this': False,
            'a02_planned_slots': 54, 'a02_assigned_function_slots_through_this': 9,
            'a02_remaining_planned_slots': 45,
            'total_local_functions_through_this': 18,
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
        'internal_order': ['D1', 'D2'], 'beats': copy.deepcopy(beats),
        'next_unit': {
            'candidate_id': 'A02-CF10', 'candidate_subact': 'A02-S3',
            'candidate_status': cf10['status'],
            'candidate_entry_non_authoritative_summary': cf10['entry_state'],
            'candidate_summary_is_exact_or_verified_projection': False,
            'exact_full_entry_if_next_unit_selected': blueprint['exit_state'],
            'candidate_is_executed_here': False,
            'offer_admission_or_college_role_verified_here': False,
        },
        'information_access': copy.deepcopy(blueprint['information_access']),
        'authority_map': copy.deepcopy(blueprint['authority_map']),
        'unassigned_details': copy.deepcopy(blueprint['unassigned_details']),
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'ACTUAL_VERIFIED authenticates source-current student checklist and school process reply, not issuance of a transcript or diploma.',
            'The prep coach cannot certify credits or NCAA eligibility; NCAA and Villanova decisions remain with their own authorities.',
            'Exact deadlines, individual grades, SAT point score and official documents remain unselected.',
            'CF10 college path, the whole A02-S3 exit and G13 remain unexecuted or unverified.',
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
        '# A02 아홉 번째 국소 회차 기능: 공식 확인을 위한 준비와 문의', '',
        '**상태:** `FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE` / 국소 Blueprint `ACTUAL_VERIFIED`. 학생 준비와 학교 절차 답변의 원천 현재성만 인증하며 실제 서류 발급·NCAA·대학 입학·원고를 인증하지 않는다.', '',
        '## 기능과 경계', '',
        f"- A02 E8 정확 출구: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- D1: {data['beats'][0]['action']} → {data['beats'][0]['observable_result']}",
        f"- D2: {data['beats'][1]['action']} → {data['beats'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 정확한 국소 출구: {data['exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 배분과 다음 후보', '',
        '- 전체 국소 기능 순서 18, A02 계획 슬롯 45, A02 내 아홉 번째 배정이다. 미배정 계획 칸을 새 사건 의무로 만들지 않으며 공개 회차번호·원고 분량은 정하지 않는다.',
        '- 학교 학업담당의 절차 답변은 실제 졸업장·성적표 발급이나 NCAA/Villanova 심사를 대신하지 않는다. CF10의 대학 경로는 아직 미실행이다.',
        '- A02-S3 전체 출구, 전체 G13·Context Pack·원고는 미완료이고 게이트는 `CLOSED`다.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound ninth A02 function']


def self_test(data):
    mutations = [
        ('claim transcript issued', lambda d: d['authority_map'].update(school_final_transcript_or_diploma_issued_here=True)),
        ('claim NCAA pass', lambda d: d['local_blueprint']['authority_map'].update(NCAA_eligibility_center_certified_here=True)),
        ('claim coach credit power', lambda d: d['authority_map'].update(prep_coach_issues_final_transcript_or_eligibility=True)),
        ('claim university admission', lambda d: d['authority_map'].update(Villanova_admission_or_compliance_decision_here=True)),
        ('execute CF10', lambda d: d['next_unit'].update(candidate_is_executed_here=True)),
        ('promote candidate entry', lambda d: d['next_unit'].update(candidate_summary_is_exact_or_verified_projection=True)),
        ('claim full S3', lambda d: d.update(whole_A02_S3_exit_certified=True)),
        ('inflate planned count', lambda d: d['slot_accounting'].update(a02_assigned_function_slots_through_this=54)),
        ('authorize manuscript', lambda d: d.update(manuscript_allowed=True)),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    old_loader = working_builder.load

    def wrong_e8(root, path):
        source = old_loader(root, path)
        if path == previous_builder.OUTPUT:
            source = copy.deepcopy(source)
            source['whole_g13_complete'] = True
        return source
    with patch.object(working_builder, 'load', side_effect=wrong_e8):
        assert validate(data), 'different E8 object in two consumers'

    def wrong_cf09_choice(root, path):
        source = old_loader(root, path)
        if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
            source = copy.deepcopy(source)
            next(f for f in source['functions'] if f['id'] == 'A02-CF09')['choice'] = '감독에게서 입학과 NCAA 자격을 승인받는다'
        return source
    with patch.object(working_builder, 'load', side_effect=wrong_cf09_choice):
        assert validate(data), 'same-ID CF09 choice reversal'
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
