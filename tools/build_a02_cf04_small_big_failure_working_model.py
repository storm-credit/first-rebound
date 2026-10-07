"""Build a bounded fictional practice failure for A02-CF04."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e3_final_episode_function as previous_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_CF04_SMALL_BIG_FAILURE_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A02_CF04_SMALL_BIG_FAILURE_WORKING_MODEL_2026_10_07.md')
SOURCES = (
    'tools/build_a02_cf04_small_big_failure_working_model.py',
    str(previous_builder.OUTPUT).replace('\\', '/'),
    'design/A02_PREP_CONDITIONAL_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/TALENT_BQ_MODEL.md',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'canon/STORY_BIBLE.md',
    'research/COLLEGE_EXIT_PACKET.md',
    'canon/PROJECT_FREEZE.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF04_PINS = {
    'dominant_function': '작은 빅맨 방식의 실패',
    'cause': '생활 시간을 맞춰도 국내에서 몸으로 버티던 농구 방식은 그대로 남는다',
    'pressure': '더 큰 선수와 빠른 외곽 수비의 분업 속에서 익숙한 빅맨 방식만으로 자리를 얻기 어렵다',
    'choice': '익숙한 빅맨 방식으로 훈련 수행을 계속 시도한다',
    'direct_cost': '익숙한 방식에 훈련 기회를 쓰고 실패해 새 윙 과제를 시도할 시간을 그만큼 미룬다',
    'changed_state': '몸의 우위로 버티기보다 다른 역할을 배워야 할 문제가 드러난다',
    'next': 'A02-CF05',
    'next_dependency': '윙의 기본 과제를 배우기 위해 익숙한 지위를 내려놓는다',
}


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, previous_builder.OUTPUT)
    candidates = load(root, 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json')
    structure = load(root, 'design/CP2_ACT_SUBACT_PACKET.json')
    bq = (root / 'canon/TALENT_BQ_MODEL.md').read_text(encoding='utf-8-sig')
    assert not previous_builder.validate(previous, root=root), 'A02 E3 source stale'
    assert previous['episode_function_id'] == 'A02-EF-003'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (12, 39)
    assert previous['next_unit']['candidate_id'] == 'A02-CF04'
    assert previous['next_unit']['candidate_is_executed_here'] is False
    assert previous['whole_A02_S1_exit_certified'] is False
    assert previous['manuscript_allowed'] is False
    cf04 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF04')
    assert cf04['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf04['evidence_class'] == 'CANDIDATE'
    assert cf04['selected_event'] is False and cf04['author_locked'] is False
    assert cf04['subact'] == 'A02-S2'
    for key, expected in CF04_PINS.items():
        assert cf04[key] == expected, f'A02-CF04 source {key} changed'
    assert cf04['entry_state'] == '다음 출전·졸업 기회를 보존하려고 자기 시간을 조절하는 행동이 생긴다'
    cf05 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF05')
    assert cf05['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf05['selected_event'] is False and cf05['author_locked'] is False
    assert cf05['subact'] == 'A02-S2'
    s2 = next(s for s in structure['subacts'] if s['id'] == 'A02-S2')
    assert s2['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert '- 한 번 보고 완성 동작 복제' in bq
    assert '실패/제약 노출 → 원인 해석 → 코칭·훈련 → 반복 비용 → 경기 검증 → 상대의 새 카운터' in bq
    assert '| 자기 역할 이해 | 매우 낮음 | 제한된 역할을 받아들임 |' in bq
    hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
              for p in SOURCES}
    return {
        'schema': 'A02_CF04_SMALL_BIG_FAILURE_WORKING_MODEL_V1',
        'status': 'ROUTINE_PREP_POSITION_MISMATCH_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'FICTIONAL_SUPERVISED_PRACTICE_FAILURE_ONLY_NOT_TEAM_GAME_OR_SKILL_MASTERY',
        'source_function': 'A02-CF04', 'target_subact': 'A02-S2',
        'prior_A02_E3_exact_full_exit': previous['exit_state'],
        'entry_state': previous['exit_state'],
        'candidate_entry_summary_is_exact_projection': False,
        'single_function': '생활 순서를 한 번 맞춘 뒤에도 익숙한 골밑 우선 수행만으로는 맡은 코너와 페인트 도움 사이의 복귀 과제를 채우지 못함을, 감독이 따로 허용한 좁은 훈련에서 직접 확인한다',
        'session_authority': {
            'classification': 'ROUTINE_FICTIONAL_DESIGN',
            'separate_coach_permission_for_this_supervised_practice': True,
            'prior_E3_one_day_permission_automatically_extended': False,
            'official_team_roster_or_game_permission': False,
            'school_attendance_or_academic_eligibility_certified': False,
        },
        'bounded_drill_setup': {
            'classification': 'ROUTINE_FICTIONAL_DESIGN',
            'coach_instruction': '약측 코너의 선수를 맡아, 공을 가진 선수가 안으로 들어올 때 페인트 도움 위치를 보되 코너로 패스가 돌아가면 자기 담당 쪽으로 복귀하는 한 과제',
            'practice_ball_and_opponents': '이름·학교·실제 기록을 정하지 않은 가상 훈련 전달자와 코너 담당 상대',
            'paint_help_is_always_wrong': False,
            'official_game_or_measured_defensive_result': False,
        },
        'event_steps': [
            {'id': 'B1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '감독이 별도로 허용한 분업 훈련에서 약측 코너를 맡은 주인공은 공이 안으로 들어오자 익숙한 골밑 우선 위치에 오래 남는다. 공이 코너로 돌아가도 자기 담당 쪽으로 늦게 복귀한다',
             'observable_result': '코너 패스를 받은 훈련 상대와 자기 복귀 위치 사이 간격이 남는 것을 직접 본다. 문제는 도움 자체가 아니라 이 과제에서의 복귀 타이밍이다',
             'not_claimed': '공식 팀 경기·특정 상대·기술 숙련·과거 C2 실패의 소급 단정'},
            {'id': 'B2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'choice_options': ['코너 담당 위치와 복귀 시간을 먼저 의식하며 다른 방법을 시험한다', '익숙한 골밑 우선 접근을 한 번 더 쓴다'],
             'selected_choice': '익숙한 골밑 우선 접근을 한 번 더 쓴다',
             'action': '주인공은 같은 제한 과제에서 익숙한 골밑 우선 접근을 한 번 더 쓰고, 코너 쪽으로 공이 되돌아간 뒤에야 맡은 위치로 움직인다',
             'observable_result': '두 번째에도 담당 코너와 자기 사이 복귀 간격이 남는다. 이 시도의 실패는 새 윙 과제의 수행이나 실제 게임 패배를 증명하지 않는다',
             'not_claimed': '실제 수비 경기 결과·동료의 비공개 평가·부상·완성된 포지션 변경'},
        ],
        'partial_order': ['A02 E3 full exit < separately permitted CF04 practice < B1 mismatch < B2 familiar retry and observable mismatch < CF05 still unexecuted'],
        'direct_present_cost': '허용된 그 훈련 기회와 주의가 익숙한 골밑 우선 시도에 쓰여 새 윙 과제에 바로 투입하지 못한다. 생활 기회 상실이나 징계는 추가하지 않는다.',
        'selected_design_exit_state': '주인공은 생활 순서를 한 번 고쳤지만, 따로 허용된 분업 훈련에서 약측 코너 담당을 맡고도 익숙한 골밑 우선 접근을 되풀이해 공이 코너로 돌아올 때 복귀가 두 번 늦었다. 새 역할의 위치·판단 과제가 드러났을 뿐, 윙 기본 수행이나 실제 경기 결과는 아직 없다.',
        'reader_question_at_end': '익숙한 골밑 위치의 보상을 내려놓고 어떤 윙 기본 과제를 반복할 것인가',
        'next_candidate': {'id': 'A02-CF05', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'wing_basic_repetition_or_success_executed_here': False},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['감독이 자기에게 허용한 코너·도움·복귀 과제', '자기가 먼저 택한 골밑 위치', '훈련 공이 코너로 돌아올 때 직접 보이는 복귀 간격'],
            'not_available_without_access': ['감독·동료의 내면 평가', '공식 팀 선발 판단', '미래 경기 성과', '비공개 학교 판단'],
            'individual_scene_pov_verified': False, 'exact_dialogue': None,
        },
        'unassigned_details': {'fictional_school_or_staff_name': None, 'exact_date': None,
                               'practice_counterpart_identity': None, 'training_drill_name': None,
                               'score_or_minutes': None, 'roster_or_game_status': None},
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'This is a new bounded fictional practice choice within the locked prep-learning direction, not a selected real game or actual school record.',
            'E3 one-day permission is not extended; this task requires separate fictional coach permission and certifies no team roster or game access.',
            'The visible late return to the assigned corner belongs only to B1/B2; paint help is not generally wrong, and the mismatch is not retrojected to C2 or all basketball skill.',
            'CF05 wing repetition, long-term habit cure, academic eligibility and full A02-S2 exit remain unverified.',
            'The working model passed independent source and meaning review; a separate final-function review is required before promotion.',
        ],
        'actual_verified_blueprint_created': False,
        'final_episode_function_added': 0,
        'whole_A02_S1_exit_certified': False, 'whole_A02_S2_exit_certified': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'author_locked': False,
        'new_author_decisions': 0, 'manuscript_count': 0,
        'manuscript_allowed': False, 'design_gate': 'CLOSED',
    }


def render(data):
    return '\n'.join([
        '# A02 CF04: 작은 빅맨 방식의 좁은 훈련 실패', '',
        '**상태:** `ROUTINE_PREP_POSITION_MISMATCH_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 기존 프렙 학습 방향 안의 일상 가상 설계이며 독립 원천·의미 검문을 통과했다. 실제 경기·선수 등록·학교 사례를 인증하지 않으며 별도 기능 검문 전 최종 기능 수는 늘리지 않는다.', '',
        '## 한 과제', '',
        f"- 정확한 진입: {data['entry_state']}",
        f"- 기능: {data['single_function']}",
        f"- B1: {data['event_steps'][0]['action']} → {data['event_steps'][0]['observable_result']}",
        f"- B2: {data['event_steps'][1]['action']} → {data['event_steps'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 국소 출구: {data['selected_design_exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 권한과 한계', '',
        '- E3의 그날 훈련 허가는 자동 연장되지 않는다. 감독이 별도로 허용한 가상 기본 훈련 한 번만 택했고, 학교 출결·학업 자격·정식 경기·선수 명단은 확정하지 않는다.',
        '- 한정 과제: ' + data['bounded_drill_setup']['coach_instruction'] + '. 페인트 도움 자체가 잘못이라는 일반 판단은 하지 않는다.',
        '- 이 과제의 늦은 복귀를 국내 시절 C2에 소급하지 않는다. 실제 상대·점수·분·드릴 이름은 비우고, 윙 과제 반복·성공 및 A02-S2 전체 출구도 미실행이다.',
        '- 국소 Blueprint·최종 기능·Context Pack·원고0, 전체 G13 미완, 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound CF04 working model']


def self_test(data):
    mutations = [
        ('claim game permission', lambda d: d['session_authority'].update(official_team_roster_or_game_permission=True)),
        ('extend prior permission', lambda d: d['session_authority'].update(prior_E3_one_day_permission_automatically_extended=True)),
        ('claim wing success', lambda d: d['next_candidate'].update(wing_basic_repetition_or_success_executed_here=True)),
        ('claim all help wrong', lambda d: d['bounded_drill_setup'].update(paint_help_is_always_wrong=True)),
        ('retroject C2 failure', lambda d: d['event_steps'][0].update(observable_result='기존 C2가 이미 이 문제였다고 확정했다')),
        ('claim school attendance', lambda d: d['session_authority'].update(school_attendance_or_academic_eligibility_certified=True)),
        ('claim full S2', lambda d: d.update(whole_A02_S2_exit_certified=True)),
        ('promote function', lambda d: d.update(final_episode_function_added=1)),
        ('authorize manuscript', lambda d: d.update(manuscript_allowed=True)),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_load = load
    for name, key, value in [
        ('same-ID easy wing mastery', 'choice', '익숙한 빅맨 방식을 버리고 즉시 완벽한 윙 수비를 해낸다'),
        ('same-ID injury consequence', 'direct_cost', '큰 부상으로 시즌을 잃는다'),
        ('same-ID college offer', 'changed_state', '미국 대학 장학금과 윙 포지션이 확정된다'),
    ]:
        def changed_load(root, path):
            source = original_load(root, path)
            if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A02-CF04')[key] = value
            return source
        with patch(__name__ + '.load', side_effect=changed_load):
            assert validate(data), name
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
    print(json.dumps({'status': data['status'], 'final_episode_function_added': 0,
                      'negative_controls': tested, 'current': not errors, 'errors': errors},
                     ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
