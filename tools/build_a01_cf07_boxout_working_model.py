"""Select one bounded CF07 training task without certifying a final episode.

The first boxout failure and retry are routine fictional design, not new
author-locked canon, skill mastery, or a manuscript scene.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a01_e3_final_episode_function as e3
import build_a01_followup_school_path as followup


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_CF07_BOXOUT_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A01_CF07_BOXOUT_WORKING_MODEL_2026_10_07.md')
SOURCES = (
    'tools/build_a01_cf07_boxout_working_model.py',
    'design/A01_E3_FINAL_EPISODE_FUNCTION.json',
    'design/A01_LEARNING_AND_TEAM_PREPARATION_BOUNDARIES.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'design/A01_FOLLOWUP_SCHOOL_PATH_2026_10_07.json',
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
    previous = load(root, e3.OUTPUT)
    boundary = load(root, 'design/A01_LEARNING_AND_TEAM_PREPARATION_BOUNDARIES.json')
    candidates = load(root, 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json')
    school = load(root, followup.OUTPUT)
    story = (root / 'canon/STORY_BIBLE.md').read_text(encoding='utf-8-sig')
    agents = (root / 'AGENTS.md').read_text(encoding='utf-8-sig')
    assert not e3.validate(previous, root=root), 'third function source is stale'
    assert not followup.validate(school, root=root), 'school follow-up source is stale'
    assert previous['episode_function_id'] == 'A01-EF-003'
    assert previous['whole_g13_complete'] is False
    assert boundary['status'] == 'TWO_WORKING_BOUNDARIES_CONCRETE_ACTIONS_CANDIDATE_REVIEW_PENDING'
    assert boundary['authority']['concrete_new_training_event_authority'] is None
    learning = next(b for b in boundary['boundaries'] if b['id'] == 'A01-LEARNING-WB')
    assert learning['source_function'] == 'A01-CF07'
    assert learning['entry_state'] == previous['exit_state']
    assert learning['editorial_recommendation'] == 'L-A'
    assert learning['concrete_action_selected'] is False
    assert {a['id'] for a in learning['action_candidates']} == {'L-A', 'L-B'}
    assert learning['working_boundary_selection'] == 'C3 뒤 기본 과제를 시도하는 범위까지만 다루고 반복 성공·기술 완성 전에 끝낸다'
    l_a = next(a for a in learning['action_candidates'] if a['id'] == 'L-A')
    assert l_a['status'] == 'CANDIDATE'
    assert l_a['action'] == '박스아웃·위치선정·패스 중 한 기본 과제를 먼저 시도하는 좁은 단위'
    assert l_a['missing'] == '세 과제 중 어느 것을 택할지·지시·시도 동작·관측 결과는 미선택'
    cf07 = next(f for f in candidates['functions'] if f['id'] == 'A01-CF07')
    assert cf07['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf07['selected_event'] is False
    assert cf07['evidence_class'] == 'CANDIDATE'
    assert cf07['subact'] == 'A01-S2'
    assert cf07['function'] == '첫 성공 뒤 위치 학습'
    assert cf07['cause'] == '첫 리바운드·아웃렛은 본능적 반응의 성공이며 반복 기술은 아니다'
    assert cf07['entry_state'] == e3.CF07_CANDIDATE_ENTRY_PIN
    assert cf07['pressure'] == '같은 도움을 다시 주려면 공이 오기 전 위치와 몸의 사용을 배워야 한다'
    assert cf07['choice'] == '성공 동작만 과시하지 않고 박스아웃·위치선정·패스의 기본 과제를 반복해 본다'
    assert cf07['cost'] == '눈에 띄는 점프와 첫 성공을 보여 줄 시간을 기본 동작 학습에 쓴다'
    assert cf07['changed_state'] == '팀 기여를 반복하기 위한 준비 과제가 생기고 미완성 기술이 남는다'
    assert cf07['next'] == 'A01-CF08'
    assert cf07['next_dependency'] == '준비를 피할 때 동료가 대신 떠안는 일을 보게 된다'
    assert '박스아웃·위치선정·패스 학습을 시작하게 하는 증거' in story
    assert 'Escalate only a consequential author choice' in agents
    assert school['scope'] == 'SUPERVISED_AFTER_CLASS_ACTIVITY_REQUIRED_FOR_LOCKED_C1_C2_C3_ONLY'
    return {
        'schema': 'A01_CF07_ROUTINE_TRAINING_WORKING_MODEL_V1',
        'status': 'ROUTINE_CONCRETE_ACTION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'FICTIONAL_EDITORIAL_IMPLEMENTATION_NOT_AUTHOR_LOCK_OR_VERIFIED_BLUEPRINT',
        'source_function': 'A01-CF07',
        'subact': 'A01-S2',
        'entry_state': previous['exit_state'],
        'canon_locked_direction': '첫 성공을 근거로 박스아웃·위치선정·패스 학습을 시작한다. 첫 성공 자체는 완성된 기술이나 천재 인증이 아니다.',
        'routine_choice_versus_locked_fact': {
            'locked_fact': 'Learning starts after first contribution; mastery is not yet achieved.',
            'new_design_choice': 'One first boxout positioning task, a directly observable first shortfall, and an adjustment attempt.',
            'new_author_lock': False,
            'consequential_long_term_outcome_selected': False,
        },
        'option_comparison': [
            {'id': 'BOXOUT_FIRST', 'selected': True,
             'reason': 'A separate body-position task tests how the instinctive contribution differs from learned preparation; it does not infer a defect in the earlier rebound.',
             'risk_control': 'No later successful rebound, mastery or rival comparison is inferred.'},
            {'id': 'POSITIONING_FIRST', 'selected': False,
             'reason': 'A broad positioning task overlaps the locked instinctive landing-spot moment unless an observable missing element is specified.'},
            {'id': 'PASS_FIRST', 'selected': False,
             'reason': 'An outlet drill is possible later, but doing it first could imply a repeatable skill from the one locked assist sequence.'},
        ],
        'single_function': '첫 본능적 기여와 반복 가능한 기본 박스아웃 준비가 다르다는 부족을 자기 시도와 재시도로 확인한다',
        'task_source': 'The existing coach may convey a bounded supervised boxout task; no exact speech or new named instructor is assigned.',
        'event_steps': [
            {'id': 'L1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '기본 박스아웃 과제를 전달받고 상대 위치보다 공을 먼저 좇는 첫 시도를 한다',
             'observable_result': '공을 먼저 보던 뒤 상대가 자신과 바스켓 사이에 먼저 자리한 것을 보고, 자기 발 위치를 제때 바꾸지 못해 그 사이 자리를 확보하지 못한 자기 수행의 부족을 확인한다',
             'not_claimed': '상대의 득점·공식 경기 패배·부상·감독 속마음'},
            {'id': 'L2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'choice_options': ['공을 먼저 좇는 기존 접근을 반복한다', '상대 위치를 먼저 확인하는 접근을 택한다'],
             'selected_choice': '상대 위치를 먼저 확인하는 접근을 택한다',
             'action': '다음 시도에서 공부터 좇는 접근을 반복하지 않고 상대 위치를 먼저 확인한 뒤 합법적 몸과 발 위치를 세워 보려 한다',
             'observable_result': '두 접근 중 상대 위치부터 보는 쪽을 택해 시도했다는 행동까지만 확인한다',
             'not_claimed': '박스아웃 성공·리바운드 확보·기술 숙련·라이벌 추월'},
        ],
        'direct_present_cost': '첫 성공을 다시 과시할 훈련 시간을 눈에 덜 띄는 기본 자리잡기 시도에 쓴다. 특정 득점 기회 상실은 주장하지 않는다.',
        'selected_design_exit_state': '첫 박스아웃 시도의 위치 부족을 직접 확인하고 다음 시도에서 상대 위치를 먼저 보려 했다. 반복 성공·기술 숙련은 확인되지 않았으며 팀 준비 약속의 구체 작업은 아직 후보로 남는다.',
        'reader_question_at_end': '이 기본 준비를 팀이 필요로 하는 반복 행동으로 연결할 수 있는가',
        'next_candidate': {'id': 'A01-CF08', 'status': 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE',
                           'exact_next_function_entry_required': 'selected_design_exit_state',
                           'candidate_not_promoted': True},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['실제로 전달받은 기본 과제', '자기 첫 시도와 상대의 보이는 위치', '자기 재시도 순서'],
            'not_available_without_access': ['감독·상대의 비공개 평가', '미래 숙련·성공', '동료 전원의 신뢰'],
            'individual_scene_pov_verified': False,
            'exact_dialogue': None,
        },
        'school_access': {
            'C1_C2_C3_clearance_automatically_extends_to_CF07': False,
            'bounded_CF07_learning_session_path_selected': True,
            'same_fictional_school_plan': True,
            'pre_session_condition_check_in_selected_model': {
                'same_day_class_attendance': followup.SATISFIED,
                'academic_supplement': followup.SATISFIED,
                'punctuality': followup.SATISFIED,
            },
            'coach_supervision_and_safety': True,
            'actual_real_school_or_case_records_certified': False,
            'registration_or_contest_eligibility_certified': False,
        },
        'unassigned_details': {
            'school_name': None, 'date_or_session_number': None,
            'training_partner_identity': None, 'exact_drill_or_contact': None,
            'score_rebound_or_possession_outcome': None,
            'academic_or_attendance_records': None,
            'team_preparation_task_or_burden_holder': None,
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes()) for p in SOURCES},
        'verification_limits': [
            'This is a selected routine design proposal, not an ACTUAL_VERIFIED Blueprint or final episode function.',
            'The observed first shortfall and retry are newly selected fictional action, not preexisting author-locked fact.',
            'The bounded school access model is a design path; real individual records remain unverified.',
            'The visible L1 cue and L2 choice passed independent re-review; Blueprint/function authority still requires separate source-current validation.',
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
        '# A01 CF07 첫 박스아웃 작업 모델', '',
        '**상태:** `ROUTINE_CONCRETE_ACTION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 기존 C3 이후 학습 시작이라는 정본 방향 안에서 첫 기본 과제 하나를 고른 설계 선택이다. 새 작가 잠금·실제 검증 Blueprint·최종 회차 기능·원고가 아니다.', '',
        '## 기존 사실과 새 설계 선택', '',
        '- 정본: 첫 리바운드/아웃렛의 성공은 기술 완성이 아니며 박스아웃·위치선정·패스 학습을 시작하는 근거다. [작업 경계](A01_LEARNING_AND_TEAM_PREPARATION_BOUNDARIES.md)는 L-A(한 과제)를 권고했으나 구체 행동은 아직 후보였다.',
        '- 권한: [AGENTS.md](../AGENTS.md)는 중요한 장기 결과의 작가 판단만 별도 올리며 일상 설계 작업은 계속하도록 한다. 공통 writing §13은 Beat/Event의 행동·반응·후폭풍을 요구하고 §22는 파일 존재·현재성·사용 권위를 구분한다. 이번 박스아웃 첫 과제는 위임된 일상 설계 선택이며 작가 확정 사실이라고 쓰지 않는다.',
        '- 비교: 박스아웃은 본능적 공 낙하지점 반응과 반복 준비의 차이를 한 관측 과제로 만든다. 넓은 위치선정은 첫 성공과 겹치기 쉽고, 패스부터 반복하면 한 번의 아웃렛을 이미 숙련으로 읽기 쉽다. 나머지 두 항목은 이후 학습 방향으로 보존한다.', '',
        '## 선택한 기능과 관측', '',
        f"- 정확 입력: {data['entry_state']}",
        f"- 기능: {data['single_function']}",
        '- L1: 전달된 기본 박스아웃 과제에서 공을 먼저 좇은 뒤 상대가 자신과 바스켓 사이에 먼저 있는 것을 본다. 자기 발 위치를 제때 바꾸지 못한 관측까지만 쓰며 공식 승패나 상대 득점은 만들지 않는다.',
        '- L2: 공을 먼저 좇는 접근을 반복할지 상대 위치를 먼저 확인할지 두 접근 중 후자를 골라 몸과 발 위치를 다시 세워 보려 한다. 선택·시도까지만 보며 박스아웃 성공·리바운드 확보·숙련은 인증하지 않는다.',
        f"- 현재 비용: {data['direct_present_cost']}",
        f"- 설계 출구: {data['selected_design_exit_state']}",
        f"- 독자 질문: {data['reader_question_at_end']}", '',
        '## 정보·학교·다음 인계', '',
        '- 주인공은 실제 전달된 과제와 자신의 시도, 상대의 보이는 위치만 알 수 있다. 감독·상대의 비공개 평가, 장래 숙련, 동료 전원의 신뢰를 알 수 없다. 개별 장면 POV·대사·드릴 정확 형식은 미인증이다.',
        '- 앞선 C1–C3의 참여 확인을 CF07에 자동 재사용하지 않는다. 같은 가상학교 계획 안의 **이번 학습 세션에 한정한** 감독 지도·안전과 출석·학업보충·시간준수 세 조건 재확인을 설계했다. 실제 개별 학교 기록·등록·대회 권한은 인증하지 않는다.',
        '- 다음 CF08은 팀 준비의 조건부 후보다. 누가 어떤 도구를 준비하고 누구의 부담이 줄었는지 아직 정하지 않았다. CF07의 학습 반복 성공이나 CF08의 수행을 여기서 선지급하지 않는다.', '',
        '관측·선택 보강까지 독립 검문을 통과했다. 이 파일 자체는 `ACTUAL_VERIFIED` Blueprint나 최종 회차 기능을 추가하지 않는다. 전체 G13/G14·실제 Pack·원고 0, 설계/원고 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound concrete working model']


def self_test(data):
    mutations = [
        ('false canon lock', lambda d: d.update(author_locked=True)),
        ('false verified blueprint', lambda d: d.update(actual_verified_blueprint_created=True)),
        ('false function count', lambda d: d.update(final_episode_function_added=1)),
        ('remove visible shortfall', lambda d: d['event_steps'][0].update(observable_result='이유 없이 실패했다')),
        ('erase changed-approach choice', lambda d: d['event_steps'][1].pop('choice_options')),
        ('mastery promotion', lambda d: d['event_steps'][1].update(observable_result='박스아웃 기술을 완성했다')),
        ('repeat clearance', lambda d: d['school_access'].update(C1_C2_C3_clearance_automatically_extends_to_CF07=True)),
        ('skip supplement', lambda d: d['school_access']['pre_session_condition_check_in_selected_model'].pop('academic_supplement')),
        ('private thoughts', lambda d: d['information_access']['not_available_without_access'].clear()),
        ('false source SHA', lambda d: d['source_rev_sha256'].update({'canon/STORY_BIBLE.md': '0' * 64})),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        assert validate(candidate), name
    original_load = load
    source_mutations = [
        ('same-ID choice mastery reversal', 'choice', '단숨에 박스아웃 숙련을 완성하고 라이벌을 추월한다'),
        ('same-ID cost injury reversal', 'cost', '부상으로 세 달 결장한다'),
    ]
    for name, key, value in source_mutations:
        def changed_source(root, path):
            source = original_load(root, path)
            if path == 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A01-CF07')[key] = value
            return source
        with patch(__name__ + '.load', side_effect=changed_source):
            assert validate(data), name
    return len(mutations) + len(source_mutations)


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
