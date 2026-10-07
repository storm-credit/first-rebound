"""Select a bounded personal measurement-preparation action after A04 E1."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a04_e1_final_episode_function as previous_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A04_CF02_MEASUREMENT_PREPARATION_WORKING_MODEL_2026_10_07.json')
MARKDOWN = OUTPUT.with_suffix('.md')
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
CANDIDATES = 'design/A04_DRAFT_CONDITIONAL_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
PICK22 = 'research/CHICAGO_2018_PICK22_PLAUSIBILITY.md'
TALENT = 'canon/TALENT_BQ_MODEL.md'
TIMELINE = 'canon/CAREER_TIMELINE.md'
SOURCES = ('tools/build_a04_cf02_measurement_preparation_working_model.py',
           PREVIOUS, CANDIDATES, CP2, PICK22, TALENT, TIMELINE)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def source_bytes(root, path):
    return (root / path).read_bytes()


def normalized_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def build(root=ROOT):
    previous = load(root, PREVIOUS)
    candidates = load(root, CANDIDATES)
    cp2 = load(root, CP2)
    assert previous == previous_builder.load(root, previous_builder.OUTPUT)
    assert not previous_builder.validate(previous, root=root), 'A04 E1 must be source-current'
    assert previous['episode_function_id'] == 'A04-EF-001'
    assert previous['final_function_order'] == 23 and previous['planned_allocation_slot'] == 145
    assert previous['next_unit']['id'] == 'A04-CF02'
    assert previous['next_unit']['Combine_invitation_official_measurement_or_pick_prepaid'] is False
    assert previous['whole_A04_S1_exit_certified'] is False
    assert previous['cp2_provisional_entry_inherited_as_actual_belief'] is False
    assert candidates['status'] == 'SIX_CONDITIONAL_DRAFT_CAUSAL_FUNCTIONS_NOT_FINAL_G13'
    cf = candidates['functions'][1]
    expected = {
        'id': 'A04-CF02', 'subact': 'A04-S1',
        'dominant_function': '측정 준비와 불확실한 결과 노출',
        'cause': '평가에 내놓을 수행 표본을 준비해도 몸의 잠재력은 별도 질문이다',
        'entry_state': '보여 줄 역할 증거와 새 평가에서 시험할 기술 과제가 구분된다',
        'pressure': '좋은 신체 반응을 스스로 확신해도 측정 결과와 지명 순번을 자신이 정할 수 없다',
        'choice': '개인 훈련 시간 일부를 허용된 측정 절차의 항목 확인과 참여 준비에 쓴다',
        'direct_cost': '자신이 고른 동작을 더 연습할 시간을 측정 항목·절차를 확인하는 준비에 쓴다',
        'changed_state': '평가에 낼 영상 준비에서 몸의 장점과 약점도 드러낼 절차 준비로 시간을 옮긴다',
        'next': 'A04-CF03',
        'next_dependency': '몸의 가능성과 실제 공격 수행의 간격을 워크아웃에서 시험한다',
    }
    assert {key: cf[key] for key in expected} == expected
    assert cf['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf['selected_event'] is False and cf['author_locked'] is False
    assert all(cf[key] is None for key in ('combine_invitation', 'measurement_results',
                                          'medical_test_results', 'workout_or_measurement_date',
                                          'draft_pick', 'agent_name'))
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    s1 = next(row for row in cp2['subacts'] if row['id'] == 'A04-S1')
    assert s1['choice'] == '신체 측정으로 순번을 단정하지 않고 준비한 기술의 가능한 범위와 한계를 평가에 내놓는다'
    assert s1['cost'] == '불확실한 평가 수용'
    assert s1['exit_state'] == '보여줄 기술 표본 명확화'
    pick = source_bytes(root, PICK22).decode('utf-8-sig')
    talent = source_bytes(root, TALENT).decode('utf-8-sig')
    timeline = source_bytes(root, TIMELINE).decode('utf-8-sig')
    assert '신체·운동능력 후보 범위 — NOT_CANON' in pick
    assert '점프·직선 가속·반복 도약은 최상위권, 측면 민첩성·핸들·장거리 슛은 미완성' in pick
    assert '공식 Combine 초청 후보' in pick and '깨끗한 메디컬' in pick
    assert '정확 22순위를 승격' in pick and '최종 `HOLD`' in pick
    assert '훈련·실패·전술 언어를 거치며 팀 전체를 읽는 능력으로 확장' in talent
    assert '정확 순번은 팀 보드·워크아웃과 22~60 재판정 전까지 HOLD' in timeline

    actions = [
        {'id': 'M1', 'type': 'FICTIONAL_PERSONAL_CATEGORY_CHECK',
         'action': 'He puts blank physical-category columns beside the E1 role/offense card: reach and jump, straight acceleration, and lateral change; every numeric result stays empty.',
         'observable_result': 'His own preparation distinguishes what a physical test might describe from defensive judgment, a live offensive skill sample and a club draft decision.',
         'candidate_ranges_copied_as_personal_results': False,
         'official_2018_NBA_protocol_or_invitation_claimed': False},
        {'id': 'M2', 'type': 'FICTIONAL_NONOFFICIAL_MOVEMENT_REHEARSAL',
         'action': 'He spends part of an otherwise permitted personal practice block on one takeoff, one straight start and one direction-change rehearsal around simple floor marks, without recording centimeters or seconds.',
         'observable_result': 'He can observe his own burst and less settled lateral recovery in this rehearsal; the marks are not a Combine lane drill, medical examination, team workout or measured grade.',
         'official_measurement_value': None, 'actual_medical_clearance': None,
         'real_scout_or_team_staff_present': False},
        {'id': 'M3', 'type': 'TIME_COST_AND_AUTHORITY_BOUNDARY',
         'choice': cf['choice'],
         'direct_present_cost': 'He uses this bounded review/practice time on the category checklist and unmeasured movement rehearsal instead of adding more repetitions to the corner one-dribble task he had chosen.',
         'observable_result': 'His preparation now includes body-potential questions and a visible lateral limitation, while all official measurement, medical and board answers remain outside his authority.',
         'pick_or_rookie_contract_guaranteed': False},
    ]
    result = (
        '주인공은 앞서 나눈 역할 증거와 미검증 공격 과제 옆에 점프·직선 가속·측면 이동의 빈 측정 항목을 놓고, '
        '허용된 개인 시간에서 간단한 출발·방향전환을 숫자 없이 예행했다. 자기 폭발력과 덜 안정적인 측면 회복은 직접 느꼈지만, '
        '정식 Combine 수치·의료 판정·구단 평가·정확 지명 순번은 얻지 못했다. 그 준비에 쓴 시간만큼 코너 한 드리블 과제의 추가 반복은 줄었다.'
    )
    return {
        'schema': 'A04_CF02_MEASUREMENT_PREPARATION_WORKING_MODEL_V1',
        'status': 'SELECTED_ROUTINE_NONOFFICIAL_MEASUREMENT_PREPARATION_INDEPENDENTLY_REVIEWED',
        'independent_review_completed': True,
        'scope': 'ONE_FICTIONAL_PERSONAL_CATEGORY_AND_MOVEMENT_REHEARSAL_NOT_OFFICIAL_COMBINE',
        'previous_exact_full_exit': previous['exit_state'],
        'source_function_id': 'A04-CF02',
        'candidate_numeric_ranges_status': 'NOT_CANON_AND_NOT_ASSIGNED_TO_PROTAGONIST',
        'measurement_categories_are_official_2018_protocol_certified': False,
        'actions': actions,
        'direct_present_cost': actions[2]['direct_present_cost'],
        'selected_design_exit_state': result,
        'next_candidate': {'id': 'A04-CF03', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'team_workout_live_defender_or_success_prepaid': False},
        'authority_matrix': {
            'self_observation': 'He may describe his own movement and list blank physical questions.',
            'official_NBA_or_event_staff': 'Only a real authorized event could certify a formal measurement or invitation; none is selected here.',
            'medical_professional': 'Only a qualified medical process could issue clearance; no medical answer is inferred from a movement rehearsal.',
            'NBA_club': 'Only the club and draft process can make board and pick decisions; the protagonist has no access to private rankings.',
        },
        'information_access': {
            'pov': 'PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'may_know': ['자기 빈 항목표와 숫자 없는 움직임 예행', '앞서 직접 기록한 역할/공격 시도 한계'],
            'cannot_know': ['공식 Combine 초청·측정값·의료결과', '팀 비공개 보드·정확 22순위', '타인 내면·실존 스카우트 발언'],
            'real_scout_dialogue': None,
        },
        'limits': {
            'official_combine_invitation_or_participation_certified': False,
            'official_height_reach_jump_sprint_agility_results_certified': False,
            'medical_clearance_or_club_grade_certified': False,
            'candidate_ranges_promoted_to_canon': False,
            'exact_pick_22_or_Hutchison_reassignment_selected': False,
            'later_elbow_or_live_pass_skill_prepaid': False,
            'first_A04_CF02_final_episode_function_completed': False,
            'whole_A04_S1_or_Act_exit_certified': False,
            'whole_g13_complete': False, 'whole_g14_complete': False,
            'actual_context_packs': 0, 'author_locked': False,
            'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {path: normalized_sha(source_bytes(root, path)) for path in SOURCES},
    }


def render(data):
    rows = [
        '# A04 측정 질문의 개인 준비', '',
        '**범위:** 허용된 개인 준비의 빈 항목표와 숫자 없는 움직임 예행. 실제 NBA Combine 초청·측정·의료 판정·팀 워크아웃·드래프트 결과가 아니다.', '',
        f"- E1 정확 출구: {data['previous_exact_full_exit']}",
        f"- 상태: `{data['status']}`",
        '- 2018 Pick 22 연구의 체격·도약·민첩성 숫자 범위는 `NOT_CANON`이다. 이번 인물 수치로 옮기지 않는다.', '',
        '| 단계 | 직접 행동 | 보이는 결과·권한 한계 |', '| --- | --- | --- |',
    ]
    for step in data['actions']:
        rows.append(f"| {step['id']} | {step.get('choice', step.get('action'))} | {step['observable_result']} |")
    rows += [
        '', f"- 직접 비용: {data['direct_present_cost']}",
        f"- 국소 출구: {data['selected_design_exit_state']}",
        '- 신체 반응을 느끼는 것과 공식 숫자·농구 BQ·의료 적합·구단 순번 선택은 권한이 다르다. 정확 날짜·수치·초청·실존 발언을 새로 만들지 않는다.',
        '- CF03 실제 워크아웃, A04-S1/Act 전체, G13/G14·실제 Pack·원고는 미완료이고 게이트 `CLOSED`다.', '',
    ]
    return '\n'.join(rows)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A04 measurement preparation differs from source-bound selection']


def self_test(data, root=ROOT):
    cases = [
        ('invent Combine invitation', lambda x: x['limits'].update(official_combine_invitation_or_participation_certified=True)),
        ('invent official value', lambda x: x['actions'][1].update(official_measurement_value='107 cm')),
        ('turn rehearsal into medical', lambda x: x['actions'][1].update(actual_medical_clearance=True)),
        ('promote candidate range', lambda x: x['limits'].update(candidate_ranges_promoted_to_canon=True)),
        ('prepay pick', lambda x: x['limits'].update(exact_pick_22_or_Hutchison_reassignment_selected=True)),
        ('erase practice time cost', lambda x: x.update(direct_present_cost='')),
    ]
    for name, mutate in cases:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed, root), name
    original_load = load
    for name, path, mutate in [
        ('E1 exact exit becomes pick', PREVIOUS,
         lambda x: x.update(exit_state='Chicago 22순위 지명이 이미 확정됐다')),
        ('CF02 same-ID choice becomes official medical', CANDIDATES,
         lambda x: x['functions'][1].update(choice='검사 없이 의료 적합과 공식 측정 1위를 선언한다')),
        ('CP2 A04 S1 choice reverses', CP2,
         lambda x: next(row for row in x['subacts'] if row['id'] == 'A04-S1').update(choice='측정만으로 22순위를 단정한다')),
    ]:
        def altered(root, requested, path=path, mutate=mutate):
            src = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                src = copy.deepcopy(src)
                mutate(src)
            return src
        with patch(__name__ + '.load', side_effect=altered):
            assert validate(data, root), name
    return len(cases) + 3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MARKDOWN).write_text(render(data), encoding='utf-8')
    errors = validate(data)
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors += validate(saved)
        if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'current': not errors, 'errors': errors,
                      'negative_controls': tested, 'status': data['status']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
