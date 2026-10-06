"""Select one bounded game-versus-preparation choice after the fifth function.

This is routine fictional design. It does not cure school attendance or gaming,
establish an autonomous prep-school routine, or promote CF10.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a01_e5_final_episode_function as e5
import build_a01_followup_school_path as followup


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_CF09_GAME_PRIORITY_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A01_CF09_GAME_PRIORITY_WORKING_MODEL_2026_10_07.md')
SOURCES = (
    'tools/build_a01_cf09_game_priority_working_model.py',
    'design/A01_E5_FINAL_EPISODE_FUNCTION.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'canon/STORY_BIBLE.md',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'AGENTS.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, e5.OUTPUT)
    candidates = load(root, 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json')
    story = (root / 'canon/STORY_BIBLE.md').read_text(encoding='utf-8-sig')
    arc = (root / 'canon/CHARACTER_RESPONSIBILITY_ARC.md').read_text(encoding='utf-8-sig')
    agents = (root / 'AGENTS.md').read_text(encoding='utf-8-sig')
    assert not e5.validate(previous, root=root), 'E5 source-current function is stale'
    assert previous['episode_function_id'] == 'A01-EF-005'
    assert previous['whole_g13_complete'] is False
    cf09 = next(f for f in candidates['functions'] if f['id'] == 'A01-CF09')
    assert cf09['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf09['selected_event'] is False
    assert cf09['evidence_class'] == 'CANDIDATE'
    assert cf09['author_locked'] is False
    assert cf09['subact'] == 'A01-S2'
    assert cf09['function'] == '게임 보상을 뒤로 미루기'
    assert cf09['entry_state'] == e5.CF09_ENTRY_PIN
    assert cf09['cause'] == e5.CF09_CAUSE_PIN
    assert cf09['pressure'] == '게임을 계속하면 맡은 준비를 미루게 되는 상황이다'
    assert cf09['choice'] == e5.CF09_CHOICE_PIN
    assert cf09['cost'] == '지금 이어갈 게임의 보상을 나중으로 미룬다'
    assert cf09['changed_state'] == '취미를 지우지 않고 한 약속의 순서를 바꾸는 행동이 생긴다'
    assert cf09['next'] == 'A01-CF10'
    assert cf09['next_dependency'] == '훈련 약속을 지키는 행동을 일부 경험한 채 다음 환경을 비교할 기준이 필요해진다'
    assert '친한 친구들과 PC방에서 게임하고 필요한 농담은 하지만' in story
    assert '게임을 악역이나 즉시 버려야 할 중독으로 만들지 않는다.' in story
    assert '농구가 주인공을 즉시 교정하거나 게임을 끊게 만들지 않는다.' in story
    assert '게임은 계속 즐긴다. 다만 수면·훈련·학업 의무를 침범하지 않도록 관리하는 법을 배운다.' in arc
    assert 'Escalate only a consequential author choice' in agents
    return {
        'schema': 'A01_CF09_ONE_TIME_GAME_PRIORITY_WORKING_MODEL_V1',
        'status': 'ROUTINE_CONCRETE_ACTION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'FICTIONAL_EDITORIAL_IMPLEMENTATION_NOT_AUTHOR_LOCK_OR_VERIFIED_BLUEPRINT',
        'source_function': 'A01-CF09', 'subact': 'A01-S2',
        'entry_state': previous['exit_state'],
        'canon_locked_direction': '게임을 없애지 않고 약속의 순서를 한 번 시험한다. 한국 단계에서 생활 전체의 자율 루틴을 완성하지 않는다.',
        'routine_choice_versus_locked_fact': {
            'locked_fact': 'Gaming remains a valued pastime; one school-stage test must not erase it or instantly repair attendance and sleep.',
            'new_design_choice': 'At an unnamed PC-room game session, decline one more short round and arrive for one already assigned team-preparation occasion.',
            'new_author_lock': False,
            'consequential_long_term_outcome_selected': False,
        },
        'single_function': '한 판 더 할 수 있는 즉시 재미 앞에서 이번 한 번은 맡은 공동 준비 약속을 먼저 선택한다',
        'time_and_access_model': {
            'relative_time': 'E5 뒤의 별도 한 준비 기회. 정확 날짜와 시각은 미정',
            'short_game_window_before_preparation_selected': True,
            'game_title_platform_or_service_reward': None,
            'pc_room_name_or_route': None,
            'actual_transport_or_minutes_certified': False,
            'preparation_start_met_in_fictional_design': True,
        },
        'event_steps': [
            {'id': 'G1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '친구들과 PC방에서 하던 짧은 게임이 끝난 뒤 한 판을 더 시작할 수 있는 시점에 약속된 공 준비 시간이 다가온 것을 확인한다',
             'observable_result': '계속하면 공동 준비 시작에 늦을 수 있다는 현재의 두 선택을 인식한다',
             'not_claimed': '정확 게임명·승패·현금/아이템 보상·친구의 권유나 속마음'},
            {'id': 'G2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'choice_options': ['짧은 게임을 한 판 더 이어간다', '이번에는 게임을 멈추고 맡은 공 준비를 먼저 한다'],
             'selected_choice': '이번에는 게임을 멈추고 맡은 공 준비를 먼저 한다',
             'action': '새 판을 시작하지 않고 PC방을 나와 그 한 번의 허용 준비 기회에 맞춰 맡은 공 준비에 참여한다',
             'observable_result': '게임의 다음 즉시 재미를 뒤로 두고 약속된 준비 일을 먼저 수행한 현재 행동을 확인한다',
             'not_claimed': '게임 포기·밤샘/지각/결석 완치·미국 프렙 자율 루틴·팀 전체 신뢰'},
        ],
        'direct_present_cost': '한 판 더 이어갈 즉시 재미와 승부 기회를 이번에는 미루며, 그 시간에 이미 맡은 공동 준비를 한다. 실제 게임 승리나 아이템 보상 포기는 주장하지 않는다.',
        'selected_design_exit_state': '주인공이 게임 한 판을 더 시작하지 않고 이번 한 번 맡은 공 준비에 참여했다. 게임은 계속 좋아하고 수면·출석·생활 전체의 반복 통제는 아직 확인되지 않았다.',
        'reader_question_at_end': '즉시 보상이 더 큰 날에도 이 순서를 다시 지킬 수 있는가',
        'next_candidate': {'id': 'A01-CF10', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'us_environment_comparison_not_selected_here': True},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['현재 게임 종료와 다음 판 선택', '자신이 받은 준비 약속', '본인이 도착해 수행한 일'],
            'not_available_without_access': ['친구 속마음', '감독의 비공개 평가', '향후 생활 습관 안정', '미국 환경의 실제 수락'],
            'individual_scene_pov_verified': False,
            'exact_dialogue': None,
        },
        'school_access': {
            'E5_clearance_automatically_extends_to_CF09': False,
            'bounded_one_preparation_occasion_selected': True,
            'pre_participation_condition_check': {
                'same_day_class_attendance': followup.SATISFIED,
                'academic_supplement': followup.SATISFIED,
                'punctuality': followup.SATISFIED,
            },
            'coach_supervision_and_safety': True,
            'actual_real_school_or_case_records_certified': False,
            'registration_or_contest_eligibility_certified': False,
        },
        'unassigned_details': {
            'game_title_or_reward': None, 'friends_individual_identity': None,
            'pc_room_and_school_name': None, 'exact_date_or_time': None,
            'travel_route_or_duration': None, 'real_attendance_or_supplement_records': None,
            'next_US_school_application_or_acceptance': None,
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
                              for p in SOURCES},
        'verification_limits': [
            'The PC-room exit and preparation priority are one new routine fictional choice, not preexisting author-locked canon.',
            'No real game title, release schedule or collectible reward is selected.',
            'One timely preparation occasion does not certify sustained attendance, sleep control, school improvement or gaming abstinence.',
            'The school conditions are fictional operating checks, not individual real records.',
            'CF10 US-environment comparison is unexecuted and no acceptance or move is selected.',
            'Independent review accepted this one-time routine design; Blueprint/function authority requires separate source-current validation.',
        ],
        'actual_verified_blueprint_created': False,
        'final_episode_function_added': 0,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'author_locked': False,
        'new_author_decisions': 0, 'manuscript_count': 0,
        'manuscript_allowed': False, 'design_gate': 'CLOSED',
    }


def render(data):
    return '\n'.join([
        '# A01 CF09 게임 한 판보다 맡은 준비', '',
        '**상태:** `ROUTINE_CONCRETE_ACTION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 한 번의 가상 일상 선택 모델이며 이 파일 자체는 별도 Blueprint·최종 회차 기능·작가 잠금·원고가 아니다.', '',
        '## 입력과 한 번의 충돌', '',
        f"- E5 전체 종료 입력: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- G1: {data['event_steps'][0]['action']} → {data['event_steps'][0]['observable_result']}",
        f"- G2 선택: {data['event_steps'][1]['choice_options'][0]} / {data['event_steps'][1]['choice_options'][1]} 중 후자.",
        f"- G2: {data['event_steps'][1]['action']} → {data['event_steps'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 출구: {data['selected_design_exit_state']}", '',
        '## 한계와 다음 인계', '',
        '- 정확 게임명·친구 신원·게임 아이템/현금 보상·PC방/학교 이름·이동 시간은 정하지 않는다. 게임 자체를 끊거나 중독 치료를 주장하지 않는다.',
        '- 이번 준비 참여는 별도 한 기회다. 출석·학업보충·시간준수 세 조건을 다시 확인하는 가상 계획일 뿐, 실제 학교 기록·등록·대회 자격을 인증하지 않는다.',
        '- CF10 미국 환경 비교는 조건부 후보다. 학교 이전/수락·미국 프렙 자율 루틴·수면/출석 전체 개선을 여기서 실행하지 않는다.',
        '- 이 파일은 국소 Blueprint/기능6 추가 0, 전체 G13/G14·실제 Pack·원고 미완료, 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound CF09 working model']


def self_test(data):
    mutations = [
        ('false author lock', lambda d: d.update(author_locked=True)),
        ('false function6', lambda d: d.update(final_episode_function_added=1)),
        ('game abstinence', lambda d: d['event_steps'][1].update(observable_result='게임을 완전히 끊었다')),
        ('erase game choice', lambda d: d['event_steps'][1].pop('choice_options')),
        ('skip school supplement', lambda d: d['school_access']['pre_participation_condition_check'].pop('academic_supplement')),
        ('reuse E5 clearance', lambda d: d['school_access'].update(E5_clearance_automatically_extends_to_CF09=True)),
        ('false school records', lambda d: d['school_access'].update(actual_real_school_or_case_records_certified=True)),
        ('execute CF10', lambda d: d['next_candidate'].update(us_environment_comparison_not_selected_here=False)),
        ('false source SHA', lambda d: d['source_rev_sha256'].update({'canon/STORY_BIBLE.md': '0' * 64})),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        assert validate(candidate), name
    original_load = load
    for name, key, value in [
        ('same-ID game cure', 'changed_state', '게임을 완전히 끊고 출석과 잠을 즉시 고친다'),
        ('same-ID game injury cost', 'cost', '게임 때문에 무릎을 다쳐 농구를 그만둔다'),
    ]:
        def changed_source(root, path):
            source = original_load(root, path)
            if path == 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A01-CF09')[key] = value
            return source
        with patch(__name__ + '.load', side_effect=changed_source):
            assert validate(data), name
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
    print(json.dumps({'status': data['status'], 'final_episode_function_added': 0,
                      'negative_controls': tested, 'current': not errors,
                      'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
