"""Select bounded wing-task repetitions after the small-big practice mismatch."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e4_final_episode_function as previous_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_CF05_WING_BASIC_REPETITION_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A02_CF05_WING_BASIC_REPETITION_WORKING_MODEL_2026_10_07.md')
SOURCES = (
    'tools/build_a02_cf05_wing_basic_repetition_working_model.py',
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
CF05_PINS = {
    'dominant_function': '윙 기본 과제의 반복',
    'cause': '빅맨 지위만으로 새 경쟁에서 버티기 어렵다는 실패가 남았다',
    'pressure': '새 역할을 배우는 동안 눈에 띄는 자기 과시와 익숙한 자리의 보상을 기대하기 어렵다',
    'choice': '익숙한 빅맨 지위를 고집하지 않고 윙의 기본 과제를 반복해 본다',
    'direct_cost': '익숙한 빅맨 동작을 반복할 훈련 시간을 윙 기본 과제에 쓰며 포지션 자존심을 내려놓는다',
    'changed_state': '새 역할에서 반복해야 할 과제를 수행하기 시작한다',
    'next': 'A02-CF06',
    'next_dependency': '반복 동작이 실제 실패 원인을 바꾸는지 확인해야 한다',
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
    assert not previous_builder.validate(previous, root=root), 'A02 E4 source stale'
    assert previous['episode_function_id'] == 'A02-EF-004'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (13, 40)
    assert previous['next_unit']['candidate_id'] == 'A02-CF05'
    assert previous['next_unit']['candidate_is_executed_here'] is False
    assert previous['next_unit']['wing_repetition_or_success_verified_here'] is False
    assert previous['whole_A02_S2_exit_certified'] is False
    assert previous['manuscript_allowed'] is False
    cf05 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF05')
    assert cf05['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf05['evidence_class'] == 'CANDIDATE'
    assert cf05['selected_event'] is False and cf05['author_locked'] is False
    assert cf05['subact'] == 'A02-S2'
    for key, expected in CF05_PINS.items():
        assert cf05[key] == expected, f'A02-CF05 source {key} changed'
    assert cf05['entry_state'] == '몸의 우위로 버티기보다 다른 역할을 배워야 할 문제가 드러난다'
    cf06 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF06')
    assert cf06['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf06['selected_event'] is False and cf06['author_locked'] is False
    s2 = next(s for s in structure['subacts'] if s['id'] == 'A02-S2')
    assert s2['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert '| 자기 역할 이해 | 매우 낮음 | 제한된 역할을 받아들임 |' in bq
    assert '실패/제약 노출 → 원인 해석 → 코칭·훈련 → 반복 비용 → 경기 검증 → 상대의 새 카운터' in bq
    assert '- 한 번 보고 완성 동작 복제' in bq
    hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
              for p in SOURCES}
    return {
        'schema': 'A02_CF05_WING_BASIC_REPETITION_WORKING_MODEL_V1',
        'status': 'ROUTINE_PREP_WING_BASIC_REPETITION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'FICTIONAL_SUPERVISED_WING_TASK_START_ONLY_NOT_GAME_PROOF_OR_MASTERY',
        'source_function': 'A02-CF05', 'target_subact': 'A02-S2',
        'prior_A02_E4_exact_full_exit': previous['exit_state'],
        'entry_state': previous['exit_state'],
        'candidate_entry_summary_is_exact_projection': False,
        'single_function': '코너 복귀가 늦었던 좁은 훈련 실패를 지닌 채, 다음에 따로 허용된 기본 훈련에서 익숙한 골밑 집중 시간을 포기하고 맡은 코너·공의 위치를 확인하는 윙 기본 과제를 반복하기 시작한다',
        'session_authority': {
            'classification': 'ROUTINE_FICTIONAL_DESIGN',
            'separate_coach_permission_for_this_supervised_practice': True,
            'prior_CF04_practice_permission_automatically_extended': False,
            'official_team_roster_or_game_permission': False,
            'school_attendance_or_academic_eligibility_certified': False,
        },
        'bounded_task': {
            'classification': 'ROUTINE_FICTIONAL_DESIGN',
            'instruction': '감독이 허용한 다음 기본 분업 훈련에서 약측 코너 담당 상대와 공의 이동을 각각 확인하고, 공이 코너로 돌아오면 그 담당 쪽으로 복귀를 시작하는 과제',
            'practice_counterpart': '이름과 실제 기록이 없는 가상 훈련 전달자·담당 상대',
            'on_time_recovery_or_stop_certified': False,
            'full_wing_role_or_game_skill_certified': False,
        },
        'event_steps': [
            {'id': 'W1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'choice_options': ['익숙한 골밑 우선 동작만 다시 요구한다', '골밑 집중 시간을 줄이고 맡은 코너·공 확인 과제를 따른다'],
             'selected_choice': '골밑 집중 시간을 줄이고 맡은 코너·공 확인 과제를 따른다',
             'action': '주인공은 감독에게 따로 허용받은 기본 훈련에서 코너 담당 위치와 공의 위치를 먼저 확인하는 과제를 받아들인다',
             'observable_result': '골밑에서 익숙한 동작을 계속할 수 있는 훈련 시간을 새 위치 확인 과제에 쓰기 시작한다',
             'not_claimed': '윙 기술 습득·공식 경기 출전·포지션 전환 확정'},
            {'id': 'W2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '동일한 제한 과제를 거듭하며, 공이 안으로 갔다가 코너로 돌아오는 순서마다 자신이 맡은 코너를 다시 확인하고 그쪽으로 복귀를 시작한다',
             'observable_result': '과제를 반복하기 시작한 행동이 보이지만 복귀가 제때 끝났는지, 수비가 통했는지 또는 실패 원인을 고쳤는지는 아직 검증하지 않는다',
             'not_claimed': '완성된 수비·경기 검증·CF06 원인 분석·동료의 비공개 평가'},
        ],
        'partial_order': ['A02 E4 full exit < separately permitted CF05 practice < W1 familiar-status cost choice < W2 bounded repetition begins < CF06 cause analysis unexecuted'],
        'direct_present_cost': '허용된 이 훈련에서 익숙한 골밑 동작에 쓸 시간을 코너 담당·공 위치를 확인하는 기본 과제에 돌리고, 몸으로 바로 앞서는 만족을 미룬다. 실제 출전시간이나 자격을 잃는 새 처분은 없다.',
        'selected_design_exit_state': '주인공은 직전 훈련의 코너 복귀 지연을 지운 척하지 않고, 다음에 따로 허용된 기본 훈련에서 골밑에 머물던 익숙한 시간을 줄여 공과 맡은 코너를 확인하고 복귀를 시작하는 과제를 거듭했다. 새 역할의 반복은 시작했지만 제때 복귀·경기 검증·기술 숙련은 아직 확인하지 못했다.',
        'reader_question_at_end': '반복을 시작한 이 과제가 앞서 늦었던 복귀의 실제 원인을 바꾸는가',
        'next_candidate': {'id': 'A02-CF06', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'cause_interpretation_or_game_proof_executed_here': False},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['감독에게 허용받은 자기 훈련 과제', '자신이 택한 훈련 시간의 사용', '자기 눈에 보인 공과 담당 코너·복귀 시작'],
            'not_available_without_access': ['감독·동료의 비공개 평가', '공식 선발·입학 판단', '실전 수비 성과', '미래 포지션 성공'],
            'individual_scene_pov_verified': False, 'exact_dialogue': None,
        },
        'unassigned_details': {'fictional_school_or_staff_name': None, 'exact_date': None,
                               'practice_counterpart_identity': None, 'training_drill_name': None,
                               'score_or_minutes': None, 'roster_or_game_status': None},
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'The selected task is a separate bounded fictional coach-supervised practice, not an actual team game or school record.',
            'A visible start of assigned corner/ball checks is not proof of timely recovery, full wing mastery or corrected failure cause.',
            'Prior CF04 late return remains a known local failure; CF06 interpretation and game proof remain future work.',
            'The protagonist gives up familiar training focus, not a certified roster spot or an invented disciplinary opportunity.',
            'The working model passed independent source and meaning review; a separate final-function review is required before promotion.',
        ],
        'actual_verified_blueprint_created': False,
        'final_episode_function_added': 0,
        'whole_A02_S2_exit_certified': False, 'whole_g13_complete': False,
        'whole_g14_complete': False, 'actual_context_packs': 0,
        'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }


def render(data):
    return '\n'.join([
        '# A02 CF05: 윙 기본 과제의 반복 시작', '',
        '**상태:** `ROUTINE_PREP_WING_BASIC_REPETITION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 기존 프렙 학습 방향 안에서 실패 뒤 기본 과제를 시작하는 일상 가상 설계이며 독립 원천·의미 검문을 통과했다. 별도 기능 검문 전 최종 기능 수는 늘리지 않는다.', '',
        '## 한 과제의 반복', '',
        f"- 정확한 진입: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- 과제: {data['bounded_task']['instruction']}",
        f"- W1: {data['event_steps'][0]['action']} → {data['event_steps'][0]['observable_result']}",
        f"- W2: {data['event_steps'][1]['action']} → {data['event_steps'][1]['observable_result']}",
        f"- 현재 비용: {data['direct_present_cost']}",
        f"- 국소 출구: {data['selected_design_exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 권한과 한계', '',
        '- CF04의 한정 훈련 허가는 자동 연장되지 않는다. 별도로 허용한 다음 가상 기본 훈련만 선택하고 학교 출결·학업자격·정식 명단·경기 허가는 인증하지 않는다.',
        '- 직전 코너 복귀 지연을 해결했다고 단정하지 않는다. 반복 시작과 제때 복귀·기술 숙련·경기 증명은 분리한다. CF06 원인 분석과 A02-S2 전체 출구도 아직 미실행이다.',
        '- 국소 Blueprint·최종 기능·Context Pack·원고0, 전체 G13 미완, 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound CF05 working model']


def self_test(data):
    mutations = [
        ('extend CF04 permission', lambda d: d['session_authority'].update(prior_CF04_practice_permission_automatically_extended=True)),
        ('claim team game', lambda d: d['session_authority'].update(official_team_roster_or_game_permission=True)),
        ('claim on-time recovery', lambda d: d['bounded_task'].update(on_time_recovery_or_stop_certified=True)),
        ('claim full wing skill', lambda d: d['bounded_task'].update(full_wing_role_or_game_skill_certified=True)),
        ('execute CF06', lambda d: d['next_candidate'].update(cause_interpretation_or_game_proof_executed_here=True)),
        ('claim actual school record', lambda d: d['session_authority'].update(school_attendance_or_academic_eligibility_certified=True)),
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
        ('same-ID immediate wing mastery', 'choice', '첫 훈련에서 윙 수비를 완성해 경기 출전을 보장받는다'),
        ('same-ID invented injury', 'direct_cost', '부상으로 세 달 결장한다'),
        ('same-ID scholarship result', 'changed_state', '대학 장학금과 입학이 확정된다'),
    ]:
        def changed_load(root, path):
            source = original_load(root, path)
            if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A02-CF05')[key] = value
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
