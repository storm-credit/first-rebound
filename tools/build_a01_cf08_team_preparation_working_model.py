"""Select a narrow CF08 shared-preparation routine without episode promotion.

The burden holder and action are new fictional design, not preexisting canon.
E4's full exit is the only authoritative input; CF09 stays conditional.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a01_e4_final_episode_function as e4
import build_a01_followup_school_path as followup


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_CF08_TEAM_PREPARATION_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A01_CF08_TEAM_PREPARATION_WORKING_MODEL_2026_10_07.md')
SOURCES = (
    'tools/build_a01_cf08_team_preparation_working_model.py',
    'design/A01_E4_FINAL_EPISODE_FUNCTION.json',
    'design/A01_LEARNING_AND_TEAM_PREPARATION_BOUNDARIES.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
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
    previous = load(root, e4.OUTPUT)
    boundaries = load(root, 'design/A01_LEARNING_AND_TEAM_PREPARATION_BOUNDARIES.json')
    candidates = load(root, 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json')
    character = (root / 'canon/CHARACTER_RESPONSIBILITY_ARC.md').read_text(encoding='utf-8-sig')
    agents = (root / 'AGENTS.md').read_text(encoding='utf-8-sig')
    assert not e4.validate(previous, root=root), 'E4 source-current function is stale'
    assert previous['episode_function_id'] == 'A01-EF-004'
    assert previous['local_blueprint']['status'] == 'ACTUAL_VERIFIED'
    assert previous['whole_g13_complete'] is False
    boundary = next(b for b in boundaries['boundaries'] if b['id'] == 'A01-TEAM-PREPARATION-WB')
    assert boundary['source_function'] == 'A01-CF08'
    assert boundary['subact'] == 'A01-S2'
    assert boundary['status'] == 'WORKING_EDITORIAL_BOUNDARY_CONCRETE_EVENT_CANDIDATE'
    assert boundary['entry_summary_is_exact_handoff'] is False
    assert boundary['editorial_recommendation'] == 'P-A'
    assert boundary['concrete_action_selected'] is False
    assert boundary['single_function'] == '맡은 준비에 다시 참여하는 후보 행동과 동료 부담의 관측 조건을 분리한다'
    assert boundary['working_boundary_selection'] == '구체 준비 약속과 수행의 범위까지 다루며 게임 충돌 시험·생활 전체 개선 전에 끝낸다'
    assert boundary['next_source_function'] == 'A01-CF09'
    assert boundary['promise_link']['role'] == 'PLANT_ACTION_CANDIDATE'
    assert {a['id'] for a in boundary['action_candidates']} == {'P-A', 'P-B'}
    p_a = next(a for a in boundary['action_candidates'] if a['id'] == 'P-A')
    assert p_a['status'] == 'CANDIDATE'
    assert p_a['action'] == '팀 공동 훈련 도구의 준비·정리 중 맡은 일을 다시 수행하는 범위'
    assert p_a['advantage'] == '누가 대신 준비해야 하는지와 수행 뒤 남은 일을 관측할 수 있다'
    assert p_a['cost'] == '칭찬이나 승부가 없는 준비 시간에 참여한다'
    assert p_a['missing'] == '도구·작업·약속 시각·대신 맡을 동료·실제 부담 감소는 미선택'
    assert all(boundary['burden_observation_required'][k] is None for k in (
        'alternative_burden_holder', 'preparation_task', 'observable_before', 'observable_after'))
    assert boundary['burden_observation_required']['reduced_burden_certified'] is False
    assert boundary['burden_observation_required']['rule'] == '누군가 대신 떠안는 준비와 수행 뒤 줄어든 일을 관측할 입력 없이 팀 부담 감소를 사실로 쓰지 않는다'
    cf08 = next(f for f in candidates['functions'] if f['id'] == 'A01-CF08')
    assert cf08['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf08['selected_event'] is False
    assert cf08['evidence_class'] == 'CANDIDATE'
    assert cf08['subact'] == 'A01-S2'
    assert cf08['function'] == '팀 준비 시간의 약속'
    assert cf08['cause'] == '자신의 준비를 피하면 동료가 대신 떠안는 일이 생긴다'
    assert cf08['entry_state'] == e4.CF08_ENTRY_PIN
    assert cf08['pressure'] == '재미있는 날만 참여하면 팀이 자신을 준비에 계산하기 어렵다'
    assert cf08['choice'] == e4.CF08_CHOICE_PIN
    assert cf08['cost'] == '칭찬이나 즉시 승부가 없는 시간에도 준비를 하며 참여할 날을 기분대로 고르는 자유를 줄인다'
    assert cf08['changed_state'] == e4.CF08_CHANGED_PIN
    assert cf08['next'] == 'A01-CF09'
    assert cf08['next_dependency'] == '게임의 즉시 보상과 약속 시간이 충돌할 때 이 이유를 시험한다'
    assert cf08['author_locked'] is False
    assert '팀이 자신을 필요로 한다는 경험이 반복돼야 학교에 오는 이유가 라이벌 하나에서 사람들로 확장된다.' in character
    assert 'Escalate only a consequential author choice' in agents
    return {
        'schema': 'A01_CF08_ROUTINE_TEAM_PREPARATION_WORKING_MODEL_V1',
        'status': 'ROUTINE_CONCRETE_ACTION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'FICTIONAL_EDITORIAL_IMPLEMENTATION_NOT_AUTHOR_LOCK_OR_VERIFIED_BLUEPRINT',
        'source_function': 'A01-CF08', 'subact': 'A01-S2',
        'entry_state': previous['exit_state'],
        'canon_locked_direction': '팀에 필요한 경험은 반복되어야 하며 즉시 칭찬이나 승부가 없는 준비에도 책임을 보여야 한다. 전체 생활 개선이나 동료 전원 신뢰는 아직 아니다.',
        'routine_choice_versus_locked_fact': {
            'locked_fact': 'A repeatable team contribution matters after the first instinctive contribution.',
            'new_design_choice': 'Two bounded preparation occasions: an assigned share of training balls and visible before/after burden for one unnamed teammate.',
            'new_author_lock': False,
            'consequential_long_term_outcome_selected': False,
        },
        'option_comparison': [
            {'id': 'P-A', 'selected': True,
             'reason': 'A single shared equipment task permits a visible teammate burden comparison without asserting performance or full team trust.'},
            {'id': 'P-B', 'selected': False,
             'reason': 'A training-role task would need extra drill and ball-role decisions not required for this narrow promise.'},
        ],
        'single_function': '맡은 공 준비에 다음 허용 세션에도 다시 참여해 한 동료의 준비 부담이 실제 행동으로 줄어든 것을 직접 본다',
        'task': {
            'item': '훈련용 공',
            'specific_action': '공동 훈련용 공을 정해진 훈련 구역으로 모으는 일의 일부를 맡아 옮긴다',
            'exact_ball_count': None,
            'exact_storage_or_layout': None,
            'assignment_conveyance': '기존 감독이 감독된 방과후 훈련 계획 안에서 공동 준비 몫을 전달한다. 대사와 실제 학교 권한 문서는 미지정.',
        },
        'event_steps': [
            {'id': 'P1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '첫 허용 준비 기회에 감독에게 훈련용 공 준비 몫을 전달받고 이름 미정 동료 한 명이 아직 전체 공을 혼자 옮기는 모습을 본다',
             'observable_result': '본인이 비면 그 동료가 공동 준비 전체를 떠안는 전 상태를 자기 눈으로 확인한다',
             'not_claimed': '정확 공 수·동료 이름·학교 출결 기록·동료 속마음'},
            {'id': 'P2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'choice_options': ['즉시 승부가 없는 준비를 건너뛴다', '다음 허용 세션에 다시 와 맡은 몫을 수행한다'],
             'selected_choice': '다음 허용 세션에 다시 와 맡은 몫을 수행한다',
             'action': '다음 허용 세션의 조건 재확인 뒤 다시 나와 맡은 공 일부를 직접 옮긴다',
             'observable_result': '앞서 혼자 옮기던 동료가 이번에는 남은 공만 옮기는 것을 보고, 자신이 처리한 몫만큼 그 동료의 준비 일이 줄었다고 확인한다',
             'not_claimed': '동료 전원의 신뢰·팀 승패·훈련 기술 숙련·수업 생활 전체 개선'},
        ],
        'burden_observation': {
            'alternative_burden_holder': '이름 미정 동료 한 명',
            'before': '그 동료가 공동 훈련용 공 전체를 혼자 옮기는 모습',
            'protagonist_action': '다음 허용 세션에 맡은 일부를 직접 옮김',
            'after': '그 동료가 남은 공만 옮기는 모습',
            'reduced_burden_observed_in_selected_fictional_design': True,
            'real_team_or_player_record_certified': False,
        },
        'direct_present_cost': '즉시 칭찬·승부가 없는 준비 기회에도 다시 와 맡은 공 준비 시간을 쓴다. 수업·생활 전체를 고쳤다고 주장하지 않는다.',
        'selected_design_exit_state': '주인공이 맡은 공 준비에 다시 와 자기 몫을 수행했고, 전에는 혼자 준비하던 동료가 남은 몫만 처리하는 것을 직접 봤다. 팀 전체 신뢰·생활 개선·게임 보상 충돌은 아직 확인되지 않았다.',
        'reader_question_at_end': '즉시 승부가 없는 팀 준비를 다음에도 스스로 선택할 수 있는가',
        'next_candidate': {'id': 'A01-CF09', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'game_reward_conflict_not_prepayment': True},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['자신에게 전달된 준비 몫', '자기 수행', '동료가 옮기는 공의 눈에 보이는 몫'],
            'not_available_without_access': ['동료 속마음', '감독 비공개 평가', '팀 전원의 신뢰', '미래 반복 성공'],
            'individual_scene_pov_verified': False, 'exact_dialogue': None,
        },
        'school_access': {
            'CF07_clearance_automatically_extends_to_CF08': False,
            'bounded_preparation_occasions_selected': 2,
            'pre_participation_condition_check_each_occasion': {
                'same_day_class_attendance': followup.SATISFIED,
                'academic_supplement': followup.SATISFIED,
                'punctuality': followup.SATISFIED,
            },
            'coach_supervision_and_safety': True,
            'actual_real_school_or_case_records_certified': False,
            'registration_or_contest_eligibility_certified': False,
        },
        'unassigned_details': {
            'school_name': None, 'dates_or_times': None,
            'unnamed_teammate_identity': None,
            'exact_ball_count_or_storage': None,
            'exact_first_prep_relation_to_CF07_session': None,
            'exact_words_or_reaction': None,
            'real_attendance_or_supplement_records': None,
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
                              for p in SOURCES},
        'verification_limits': [
            'P1/P2 and the unnamed teammate are selected fictional action, not old author-locked canon.',
            'A visible smaller preparation share for one teammate does not certify team-wide trust.',
            'The school path is a bounded fictional design; real school records remain unverified.',
            'CF09 is not executed and no game incentive, match result or academic improvement is selected.',
            'Independent review accepted this bounded routine design; a source-current Blueprint and fifth function require separate validation.',
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
        '# A01 CF08 공동 준비 작업 모델', '',
        '**상태:** `ROUTINE_CONCRETE_ACTION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 새 일상 설계의 국소 비교이며 이 파일 자체는 별도 Blueprint·최종 회차 기능·작가 잠금·원고가 아니다.', '',
        '## 범위와 행동', '',
        f"- E4 전체 종료 입력: {data['entry_state']}",
        '- P-A 선택: 감독이 감독된 방과후 계획 안에서 훈련용 공의 공동 준비 일부를 맡긴다. 공 개수·장소·대사·동료 신원은 정하지 않는다.',
        f"- P1: {data['event_steps'][0]['action']} → {data['event_steps'][0]['observable_result']}",
        f"- P2 선택: {data['event_steps'][1]['choice_options'][0]} / {data['event_steps'][1]['choice_options'][1]} 중 후자.",
        f"- P2: {data['event_steps'][1]['action']} → {data['event_steps'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 출구: {data['selected_design_exit_state']}", '',
        '## 권위 경계', '',
        '- 부담 전후는 이름 미정 동료 한 명이 실제로 옮긴 공의 몫이라는 보이는 행동에만 한정한다. 동료 전원의 신뢰나 비공개 마음을 결론으로 삼지 않는다.',
        '- 두 준비 기회는 각각 출석·학업보충·시간준수 조건을 다시 확인하는 가상 운영 설계다. CF07 확인이 자동 연장되지 않으며 실제 학교 기록·등록·대회 자격을 인증하지 않는다.',
        '- CF09 게임 보상 충돌은 조건부 후보로 남는다. 정확 날짜·공 개수·동료 신원·새 성적·원고는 만들지 않는다.',
        '- 국소 Blueprint/기능5 추가 0, 전체 G13/G14·실제 Context Pack·원고 미완료, 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound CF08 working model']


def self_test(data):
    mutations = [
        ('false author lock', lambda d: d.update(author_locked=True)),
        ('false function5', lambda d: d.update(final_episode_function_added=1)),
        ('false teammate-wide trust', lambda d: d['event_steps'][1].update(observable_result='팀 전원이 그를 믿는다')),
        ('erase burden before', lambda d: d['burden_observation'].pop('before')),
        ('erase burden after', lambda d: d['burden_observation'].pop('after')),
        ('reuse CF07 clearance', lambda d: d['school_access'].update(CF07_clearance_automatically_extends_to_CF08=True)),
        ('skip supplement', lambda d: d['school_access']['pre_participation_condition_check_each_occasion'].pop('academic_supplement')),
        ('execute CF09', lambda d: d['next_candidate'].update(game_reward_conflict_not_prepayment=False)),
        ('false source SHA', lambda d: d['source_rev_sha256'].update({'canon/CHARACTER_RESPONSIBILITY_ARC.md': '0' * 64})),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        assert validate(candidate), name
    original_load = load
    for name, key, value in [
        ('same-ID burden cause reversal', 'cause', '동료가 방출해서 다른 학교로 이적한다'),
        ('same-ID future game payoff', 'changed_state', '게임 보상을 얻고 수업까지 고친다'),
        ('same-ID false cost injury', 'cost', '무릎 부상으로 출전이 끝난다'),
    ]:
        def changed_source(root, path):
            source = original_load(root, path)
            if path == 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A01-CF08')[key] = value
            return source
        with patch(__name__ + '.load', side_effect=changed_source):
            assert validate(data), name
    def changed_boundary(root, path):
        source = original_load(root, path)
        if path == 'design/A01_LEARNING_AND_TEAM_PREPARATION_BOUNDARIES.json':
            source = copy.deepcopy(source)
            boundary = next(b for b in source['boundaries'] if b['id'] == 'A01-TEAM-PREPARATION-WB')
            next(a for a in boundary['action_candidates'] if a['id'] == 'P-A')['cost'] = '부상으로 훈련을 그만둔다'
        return source
    with patch(__name__ + '.load', side_effect=changed_boundary):
        assert validate(data), 'same-ID boundary cost reversal'
    return len(mutations) + 4


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
