"""Select A01-S3 move intent within the already locked prep route.

The decision here is the protagonist's bounded fictional action. It does not
certify school admission, guardian permission, credit audit, visa or departure.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a01_e8_final_episode_function as e8


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_CF12_MOVE_INTENT_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A01_CF12_MOVE_INTENT_WORKING_MODEL_2026_10_07.md')
SOURCES = (
    'tools/build_a01_cf12_move_intent_working_model.py',
    'design/A01_E8_FINAL_EPISODE_FUNCTION.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/STORY_BIBLE.md',
    'canon/CAREER_TIMELINE.md',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'canon/PROJECT_FREEZE.md',
    'AGENTS.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF12_PINS = {
    'function': '미국행 선택과 미완성 준비의 이월',
    'cause': '이동의 이유와 자신이 준비할 과제가 구분됐다',
    'pressure': '낯선 기술 경쟁을 택해도 주전·칭찬·학업 성공을 보장받지 못한다',
    'choice': '미국 프렙으로 옮기려는 방향을 택하고 남은 준비를 이어 간다',
    'cost': '국내에서 익숙한 신체 우위와 관계를 계속 누리는 길을 내려놓는다',
    'changed_state': '농구를 계속할 이유를 가진 채 낯선 환경을 선택하지만 기술·학업·생활 과제는 남는다',
    'next': 'A02-S1',
}


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, e8.OUTPUT)
    candidates = load(root, 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json')
    packet = load(root, 'design/CP2_ACT_SUBACT_PACKET.json')
    story = (root / 'canon/STORY_BIBLE.md').read_text(encoding='utf-8-sig')
    career = (root / 'canon/CAREER_TIMELINE.md').read_text(encoding='utf-8-sig')
    responsibility = (root / 'canon/CHARACTER_RESPONSIBILITY_ARC.md').read_text(encoding='utf-8-sig')
    freeze = (root / 'canon/PROJECT_FREEZE.md').read_text(encoding='utf-8-sig')
    assert not e8.validate(previous, root=root), 'E8 source-current function is stale'
    assert previous['episode_function_id'] == 'A01-EF-008'
    assert previous['next_unit']['candidate_id'] == 'A01-CF12'
    assert previous['next_unit']['candidate_is_executed_here'] is False
    assert previous['whole_g13_complete'] is False
    cf12 = next(f for f in candidates['functions'] if f['id'] == 'A01-CF12')
    assert (cf12['status'], cf12['evidence_class'], cf12['selected_event'], cf12['author_locked']) == (
        'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE', 'CANDIDATE', False, False)
    assert cf12['subact'] == 'A01-S3'
    for key, expected in CF12_PINS.items():
        assert cf12[key] == expected, f'CF12 source {key} changed'
    subact = next(s for s in packet['subacts'] if s['id'] == 'A01-S3')
    assert subact['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert subact['window'] == '2015–2016.02'
    assert '2016년 3월 가상 뉴잉글랜드 보딩 프렙으로 이동' in story
    assert '2016.03 | 가상 뉴잉글랜드 보딩 프렙 중도 편입·학점 감사' in career
    assert '필요한 학업과 서류를 자기 선택의 비용으로 수행한다' in responsibility
    assert '개별 과목의 NCAA 환산은 `HOLD`' in freeze
    source_hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
                     for p in SOURCES}
    return {
        'schema': 'A01_CF12_MOVE_INTENT_WORKING_MODEL_V1',
        'status': 'ROUTINE_MOVE_INTENT_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'EXISTING_AUTHOR_LOCKED_ROUTE_CHARACTER_INTENT_NOT_REAL_TRANSFER_CERTIFICATION',
        'source_function': 'A01-CF12', 'target_subact': 'A01-S3',
        'entry_state': previous['exit_state'],
        'prior_S2_whole_subact_exit_certified': False,
        'S3_full_entry_or_exit_certified': False,
        'existing_locked_route': '한국 고1 뒤 2016년 3월 가상 뉴잉글랜드 소규모 보딩 프렙 편입 방향',
        'route_reapproval_required': False,
        'routine_choice_versus_locked_fact': {
            'locked_fact': 'March 2016 fictional New England prep transfer direction is already author locked.',
            'new_design_choice': 'The protagonist explicitly communicates intent to pursue that route despite open conditions.',
            'new_author_lock': False,
            'actual_departure_or_admission_selected_by_this_model': False,
        },
        'relative_time_window': {
            'after_E8_exit': True,
            'before_locked_2016_03_prep_move': True,
            'exact_date_or_semester_position': None,
        },
        'single_function': '답이 남은 학업·이동 조건을 숨기지 않고 기존 미국 프렙 방향을 자기 의사로 선택해 준비를 계속한다',
        'event_steps': [
            {'id': 'D1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'choice_options': ['익숙한 한국 팀·동갑 승부 안에 남는 편한 방향을 택한다', '미답 조건을 표시한 채 기존 가상 프렙 이동 방향의 준비를 계속한다'],
             'selected_choice': '미답 조건을 표시한 채 기존 가상 프렙 이동 방향의 준비를 계속한다',
             'action': 'E8에서 남긴 국내 기록 확인 항목과 미국 프렙 권한자의 미답 질문을 다시 보고, 익숙한 국내 경쟁에만 남는 선택 대신 이미 정해진 가상 프렙 방향을 계속 준비하기로 정한다',
             'observable_result': '답이 없는 항목을 지우지 않고 자기 선택과 행정 결과를 구분한 준비 목록을 유지한다',
             'not_claimed': '미국 프렙 합격·보호자 동의·학점 인정·주전 보장·국내 관계 단절'},
            {'id': 'D2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '기존 한국 고교 감독에게 자신이 가상 프렙 이동 방향의 준비를 계속하겠다는 의사를 전한다',
             'observable_result': '주인공이 자기 의사를 말한 사실만 남고, 감독은 입학이나 학사 조건을 승인하지 않는다',
             'not_claimed': '감독의 실제 미국학교 권한·미국 프렙 제안·가족과 학교의 수락·출국'},
        ],
        'direct_present_cost': '익숙한 국내 신체 우위와 관계 안에만 남는 쉬운 선택을 내려놓고, 미답인 학업·이동 준비를 자기 몫으로 계속 감당하기로 한다.',
        'selected_design_exit_state': '주인공은 답이 남은 국내 기록·프렙 입학·학점 질문을 보존한 채 기존 가상 뉴잉글랜드 프렙 이동 방향의 준비를 계속하겠다고 직접 밝혔다. 실제 승인·이동은 아직 이 기능에서 실행되지 않았고 기술·학업·생활 과제는 남아 있다.',
        'reader_question_at_end': '답이 남은 조건과 낯선 경쟁 속에서 실제로 자기 몫을 감당할 수 있는가',
        'next_candidate': {'id': 'A02-S1', 'status': 'CP2_PROVISIONAL_NOT_EXECUTED',
                           'prep_arrival_and_academic_conditions_not_resolved_here': True},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['자신의 이동 의사', '자신이 보존한 준비·미답 목록', '감독에게 의사를 전한 자신의 행동'],
            'not_available_without_access': ['감독의 비공개 평가', '미국 프렙의 입학 판단', '보호자 속마음과 재정 선택', '향후 미국팀 역할'],
            'individual_scene_pov_verified': False, 'exact_dialogue': None,
        },
        'institutional_limits': {
            'Korean_coach_can_approve_prep_admission_or_credit': False,
            'actual_US_prep_admission_or_enrollment_certified': False,
            'guardian_consent_or_finance_selected': False,
            'credit_audit_or_visa_certified': False,
            'actual_departure_or_A02_arrival_certified': False,
            'familiar_Korean_relationship_severed_certified': False,
        },
        'unassigned_details': {
            'fictional_prep_name': None,
            'Korean_coach_identity_or_exact_reply': None,
            'family_consent_or_financing': None,
            'actual_acceptance_or_enrollment_record': None,
            'individual_credit_conversion': None,
            'visa_or_departure_day': None,
            'A02_first_scene': None,
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': source_hashes,
        'verification_limits': [
            'The March 2016 fictional prep direction is existing canon; this new action is only the protagonist communicating intent.',
            'The coach receives the intent but cannot certify prep admission, credits, visa, guardian consent or departure.',
            'The open E8 academic and transfer questions are preserved rather than silently resolved.',
            'This one unit does not certify S3 whole completion or the A02 arrival and academic status.',
            'Independent review accepted this limited intent; source-current Blueprint and ninth function require separate validation.',
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
        '# A01 CF12 가상 프렙 이동 의사의 범위', '',
        '**상태:** `ROUTINE_MOVE_INTENT_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 미국 프렙 이동 방향은 이미 잠긴 정본이며, 여기서는 주인공의 의사 표현만 가상 설계한다. 실제 입학·편입·출국·원고 허가가 아니다.', '',
        '## 입력과 선택', '',
        f"- E8 전체 종료 입력: {data['entry_state']}",
        f"- 한 기능: {data['single_function']}",
        f"- D1: {data['event_steps'][0]['action']} → {data['event_steps'][0]['observable_result']}",
        f"- D2: {data['event_steps'][1]['action']} → {data['event_steps'][1]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 출구: {data['selected_design_exit_state']}",
        f"- 독자 질문: {data['reader_question_at_end']}", '',
        '## 권위와 인계', '',
        '- 감독에게 의사를 전하지만 감독이 입학·학점·비자·보호자 결정을 대신하지 않는다. 한국 관계의 실제 단절·미국 출국도 선지급하지 않는다.',
        '- E8의 미답 질문은 그대로 남는다. A02-S1의 실제 프렙 도착·학사 조건은 이번 국소 모델로 인증하지 않는다.',
        '- 국소 Blueprint/기능9 추가 0, S3 전체 완료·전체 G13/G14·실제 Context Pack·원고 미완료, 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound CF12 working model']


def self_test(data):
    mutations = [
        ('false author lock', lambda d: d.update(author_locked=True)),
        ('false ninth function', lambda d: d.update(final_episode_function_added=1)),
        ('false prep admission', lambda d: d['institutional_limits'].update(actual_US_prep_admission_or_enrollment_certified=True)),
        ('coach admission power', lambda d: d['institutional_limits'].update(Korean_coach_can_approve_prep_admission_or_credit=True)),
        ('false guardian consent', lambda d: d['institutional_limits'].update(guardian_consent_or_finance_selected=True)),
        ('false departure', lambda d: d['institutional_limits'].update(actual_departure_or_A02_arrival_certified=True)),
        ('false whole S3', lambda d: d.update(S3_full_entry_or_exit_certified=True)),
        ('remove E8 open questions', lambda d: d.update(selected_design_exit_state='모든 학점과 입학 조건이 해결됐다')),
        ('execute A02', lambda d: d['next_candidate'].update(prep_arrival_and_academic_conditions_not_resolved_here=False)),
        ('false source SHA', lambda d: d['source_rev_sha256'].update({'canon/CAREER_TIMELINE.md': '0' * 64})),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        assert validate(candidate), name
    original_load = load
    for name, key, value in [
        ('same-ID route reversal', 'choice', '미국 이동을 완전히 포기하고 국내 잔류를 정본으로 바꾼다'),
        ('same-ID guaranteed success', 'changed_state', '미국 프렙 입학과 주전·학업 성공을 확정한다'),
    ]:
        def changed_source(root, path):
            source = original_load(root, path)
            if path == 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A01-CF12')[key] = value
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
