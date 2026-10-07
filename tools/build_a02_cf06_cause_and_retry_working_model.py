"""Select a bounded cause comparison and retry for A02-CF06."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e5_final_episode_function as previous_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_CF06_CAUSE_AND_RETRY_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A02_CF06_CAUSE_AND_RETRY_WORKING_MODEL_2026_10_07.md')
SOURCES = (
    'tools/build_a02_cf06_cause_and_retry_working_model.py',
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
CF06_PINS = {
    'dominant_function': '실패 원인 확인과 재시도',
    'cause': '새 역할을 반복해도 무엇이 잘못됐는지 모르면 같은 실패가 이어질 수 있다',
    'pressure': '단순 운동능력으로는 자신의 위치·선택 문제를 설명할 수 없다',
    'choice': '자신이 겪은 실패를 허용된 영상·코칭과 대조하고 확인한 과제를 다음 반복에서 시험한다',
    'direct_cost': '성공 동작만 보여 줄 시간 대신 부족한 수행을 드러내고 수정 반복에 쓴다',
    'changed_state': '훈련이 막연한 반복에서 자기 실패에 대응하는 과제로 좁혀진다',
    'next': 'A02-CF07',
    'next_dependency': '대학이 볼 자료에도 한 번의 과시보다 반복 수행을 남겨야 한다',
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
    assert not previous_builder.validate(previous, root=root), 'A02 E5 source stale'
    assert previous['episode_function_id'] == 'A02-EF-005'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (14, 41)
    assert previous['next_unit']['candidate_id'] == 'A02-CF06'
    assert previous['next_unit']['candidate_is_executed_here'] is False
    assert previous['next_unit']['cause_analysis_or_game_proof_verified_here'] is False
    assert previous['whole_A02_S2_exit_certified'] is False
    assert previous['manuscript_allowed'] is False
    cf06 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF06')
    assert cf06['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf06['evidence_class'] == 'CANDIDATE'
    assert cf06['selected_event'] is False and cf06['author_locked'] is False
    assert cf06['subact'] == 'A02-S2'
    for key, expected in CF06_PINS.items():
        assert cf06[key] == expected, f'A02-CF06 source {key} changed'
    assert cf06['entry_state'] == '새 역할에서 반복해야 할 과제를 수행하기 시작한다'
    cf07 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF07')
    assert cf07['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf07['selected_event'] is False and cf07['author_locked'] is False
    s2 = next(s for s in structure['subacts'] if s['id'] == 'A02-S2')
    assert s2['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert '실패/제약 노출 → 원인 해석 → 코칭·훈련 → 반복 비용 → 경기 검증 → 상대의 새 카운터' in bq
    assert '- 영상만 보고 NBA 속도 적응' in bq
    hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
              for p in SOURCES}
    return {
        'schema': 'A02_CF06_CAUSE_AND_RETRY_WORKING_MODEL_V1',
        'status': 'ROUTINE_PREP_CAUSE_COMPARISON_AND_RETRY_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'FICTIONAL_ALLOWED_COACHING_AND_EXAMPLE_CLIP_NOT_PERSONAL_ARCHIVE_OR_GAME_PROOF',
        'source_function': 'A02-CF06', 'target_subact': 'A02-S2',
        'prior_A02_E5_exact_full_exit': previous['exit_state'],
        'entry_state': previous['exit_state'],
        'candidate_entry_summary_is_exact_projection': False,
        'single_function': '앞서 코너 복귀가 늦었던 관측을 감독이 허용한 일반 시범 영상·코칭과 대조해 복귀 시작 시점이라는 한 과제로 좁히고, 다음에 따로 허용된 기본 반복에서 그 단서를 시험한다',
        'information_source_authority': {
            'classification': 'ROUTINE_FICTIONAL_DESIGN',
            'coach_shows_allowed_generic_instructional_clip': True,
            'earlier_CF04_or_CF05_personal_practice_recording_retroactively_asserted': False,
            'clip_is_actual_2016_real_school_archive': False,
            'clip_proves_protagonist_game_performance': False,
            'coaching_tells_protagonist_his_own_bounded_task_only': True,
        },
        'retry_authority': {
            'separate_coach_permission_for_next_supervised_basic_rep': True,
            'prior_CF05_practice_permission_automatically_extended': False,
            'official_team_roster_or_game_permission': False,
            'school_or_NCAA_qualification_certified': False,
        },
        'event_steps': [
            {'id': 'C1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '주인공은 감독이 보여 주는 허용된 일반 시범 영상의 코너 패스·복귀 시작 지점을, 자기가 CF04에서 공이 코너로 돌아온 뒤에도 골밑에 남았던 관측과 대조한다. 감독은 이 제한 과제에서 복귀 시작을 패스가 이미 도착한 뒤까지 늦추지 말라는 단서를 준다',
             'observable_result': '주인공은 자기 실패를 막연한 몸싸움 부족이 아니라 코너 패스에 대한 자기 복귀 시작 시점이라는 시험 가능한 과제로 말할 수 있다',
             'not_claimed': '자기 훈련의 실제 촬영본·감독의 비공개 평가·모든 도움수비의 정답'},
            {'id': 'C2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'choice_options': ['익숙한 강점 장면만 다시 보여 준다', '늦었던 복귀 단서를 드러내고 그 시작 시점을 다음 기본 반복에서 시험한다'],
             'selected_choice': '늦었던 복귀 단서를 드러내고 그 시작 시점을 다음 기본 반복에서 시험한다',
             'action': '다음에 따로 허용된 감독 기본 반복에서 주인공은 코너 쪽 패스가 시작되는 순간 담당 위치로 복귀를 시작해 보며, 코치가 지적한 자기 시점 문제를 공개된 과제로 둔다',
             'observable_result': '복귀 시작 시점의 수정 시도는 보이지만 코너를 제때 막았는지, 경기에서 통했는지, 기술을 안정적으로 익혔는지는 아직 판정하지 않는다',
             'not_claimed': '실전 검증·상대 선발·완성된 수비·입학 평가 자료·CF07 추천 실행'},
        ],
        'partial_order': ['A02 E5 full exit < allowed generic clip and bounded coaching comparison C1 < separately permitted basic retry C2 < CF07 recommendation/evaluation not executed'],
        'direct_present_cost': '익숙한 골밑 동작을 다시 할 수 있는 허용 훈련·설명 시간 일부를 자기의 늦은 복귀를 드러내는 영상 대조와 한 번의 수정 시도에 쓴다. 실제 출전·입학 기회 박탈이나 새 징계는 만들지 않는다.',
        'selected_design_exit_state': '주인공은 골밑의 몸싸움만 더하는 대신, 자기 코너 복귀 지연을 허용된 시범 영상·코칭과 대조해 패스 뒤 늦게 움직인 시점 문제로 좁혔다. 다음에 따로 허용된 기본 반복에서 코너 패스가 시작될 때 복귀를 시도했지만, 제때 수비·실전 성공·기술 숙련은 아직 확인하지 않았다.',
        'reader_question_at_end': '이렇게 좁힌 과제를 여러 실제 역할 수행 속에서도 유지하고 평가에 보일 수 있는가',
        'next_candidate': {'id': 'A02-CF07', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'recommendation_or_actual_evaluation_executed_here': False},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['자신이 직접 본 CF04 코너 복귀 지연', '감독이 자신에게 허용한 일반 시범 영상과 지시', '자신이 다음 반복에서 시작한 복귀 시도'],
            'not_available_without_access': ['과거 훈련의 존재하지 않는 촬영본', '감독·대학 평가자의 내면', '실제 경기 성과', '비공개 입학 판단'],
            'individual_scene_pov_verified': False, 'exact_dialogue': None,
        },
        'unassigned_details': {'fictional_school_or_staff_name': None, 'exact_date': None,
                               'example_clip_creator_or_archive': None, 'personal_practice_footage': None,
                               'training_drill_name': None, 'score_or_minutes': None,
                               'roster_or_game_status': None},
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'A generic coach-permitted instructional clip is a fictional design choice, not proof that prior personal CF04/CF05 reps were recorded.',
            'The coach’s cue belongs to this corner-return task and does not mean paint help is always wrong.',
            'Starting earlier on the next bounded rep is a test, not proof of a timely stop, stable skill or actual game success.',
            'CF07 recommendation and university evaluation remain unexecuted; full A02-S2 and G13 remain open.',
            'The working model passed independent source and meaning review; a separate final-function review is required before promotion.',
        ],
        'actual_verified_blueprint_created': False, 'final_episode_function_added': 0,
        'whole_A02_S2_exit_certified': False, 'whole_g13_complete': False,
        'whole_g14_complete': False, 'actual_context_packs': 0,
        'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }


def render(data):
    return '\n'.join([
        '# A02 CF06: 실패 원인 대조와 한정 재시도', '',
        '**상태:** `ROUTINE_PREP_CAUSE_COMPARISON_AND_RETRY_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 이전 개인 훈련 영상의 존재를 소급하지 않고, 감독이 허용한 가상 일반 시범 영상·코칭으로 자기 관측을 대조하는 국소 모델이다. 독립 원천·의미 검문을 통과했으며 별도 기능 검문 전 기능 수는 늘리지 않는다.', '',
        '## 한 원인과 한 시도', '',
        f"- 정확한 진입: {data['entry_state']}",
        f"- 기능: {data['single_function']}",
        f"- C1: {data['event_steps'][0]['action']} → {data['event_steps'][0]['observable_result']}",
        f"- C2: {data['event_steps'][1]['action']} → {data['event_steps'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 국소 출구: {data['selected_design_exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 검문 경계', '',
        '- CF05 훈련 허가를 자동 연장하지 않는다. 다음 감독 허용의 기본 반복 한 번에서 수정 단서를 시험하며 제때 차단·기술 숙련·실제 경기·대학 평가를 인증하지 않는다.',
        '- 시범 영상은 특정 2016 실학교 자료나 주인공의 과거 촬영본이 아니다. 감독의 지시는 이 코너 복귀 과제에 한정되며 일반적인 도움수비 금지 규칙이 아니다.',
        '- CF07 추천·실제 평가와 A02-S2 전체 출구는 미실행이다. 최종 기능·Context Pack·원고0, 전체 G13 미완, 게이트 `CLOSED`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound CF06 working model']


def self_test(data):
    mutations = [
        ('invent old personal video', lambda d: d['information_source_authority'].update(earlier_CF04_or_CF05_personal_practice_recording_retroactively_asserted=True)),
        ('claim real 2016 archive', lambda d: d['information_source_authority'].update(clip_is_actual_2016_real_school_archive=True)),
        ('claim game proof from clip', lambda d: d['information_source_authority'].update(clip_proves_protagonist_game_performance=True)),
        ('extend CF05 permission', lambda d: d['retry_authority'].update(prior_CF05_practice_permission_automatically_extended=True)),
        ('claim actual game', lambda d: d['retry_authority'].update(official_team_roster_or_game_permission=True)),
        ('execute CF07 evaluation', lambda d: d['next_candidate'].update(recommendation_or_actual_evaluation_executed_here=True)),
        ('invent success', lambda d: d.update(selected_design_exit_state='코너를 완벽히 막고 대학 오퍼를 받았다')),
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
        ('same-ID automatic game proof', 'choice', '영상을 보기만 하고 경기에서 완성된 수비를 증명한다'),
        ('same-ID suspension cost', 'direct_cost', '팀에서 방출되어 미국 학교를 떠난다'),
        ('same-ID full mastery', 'changed_state', '한 번 본 뒤 모든 수비 로테이션을 완성한다'),
    ]:
        def changed_load(root, path):
            source = original_load(root, path)
            if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A02-CF06')[key] = value
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
