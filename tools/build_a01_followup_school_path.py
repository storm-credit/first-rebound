"""Bound the fictional school procedure for A01's locked follow-up practice.

Extends the selected one-trial procedure only across C1–C3's required
supervised activity. It is neither indefinite club membership nor real proof.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_a01_trial_school_operating_path as first_path
import check_a01_opening_blueprint as blueprint_check


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_FOLLOWUP_SCHOOL_PATH_2026_10_07.json')
MARKDOWN = Path('design/A01_FOLLOWUP_SCHOOL_PATH_2026_10_07.md')
SOURCES = (
    'tools/build_a01_followup_school_path.py',
    'design/A01_TRIAL_SCHOOL_OPERATING_PATH_2026_10_07.json',
    'design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'canon/STORY_BIBLE.md',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'research/A01_KOREA_2015_SCHOOL_TRIAL_BOUNDARY.json',
)
CONTRIBUTION_SEMANTIC_SHA256 = '362ef7fccfb99f00cb07b148ac7062cdb768fbb72ad63e1db8e055cef95641b9'
SATISFIED = 'SATISFIED_FOR_LIMITED_SUPERVISED_ACTIVITY_IN_FICTIONAL_MODEL'


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def semantic_sha(data):
    projection = {k: v for k, v in data.items() if k != 'source_rev_sha256'}
    return hashlib.sha256(json.dumps(projection, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    first = load(root, first_path.OUTPUT)
    contribution = load(root, 'design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json')
    candidates = load(root, 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json')
    assert not first_path.validate(first, root=root), 'first-trial operating path stale'
    assert first['selected_fictional_operating_plan']['scope'] == 'ONE_CONDITIONAL_AFTER_CLASS_TRIAL_ONLY'
    assert semantic_sha(contribution) == CONTRIBUTION_SEMANTIC_SHA256
    assert [beat['id'] for beat in contribution['beats']] == ['C1', 'C2', 'C3']
    assert sum(len(beat['claims']) for beat in contribution['beats']) == 5
    assert contribution['status'] == 'ACTUAL_VERIFIED'
    cf = {f['id']: f for f in candidates['functions']}
    assert cf['A01-CF05']['subact'] == 'A01-S1'
    assert cf['A01-CF06']['subact'] == 'A01-S2'
    assert cf['A01-CF07']['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    return {
        'schema': 'A01_FICTIONAL_FOLLOWUP_SCHOOL_PATH_V1',
        'status': 'ROUTINE_FICTIONAL_FOLLOWUP_DESIGN_SELECTED',
        'classification': 'DELEGATED_DESIGN_SELECTION_NOT_AUTHOR_LOCK_OR_REAL_SCHOOL_FACT',
        'extends_path': str(first_path.OUTPUT).replace('\\', '/'),
        'extension_reason': 'The first path permits T1 only; locked C1 returns to a later training opportunity.',
        'scope': 'SUPERVISED_AFTER_CLASS_ACTIVITY_REQUIRED_FOR_LOCKED_C1_C2_C3_ONLY',
        'same_fictional_school_operating_plan': True,
        'first_trial_permission_automatically_recurs': False,
        'renewed_limited_clearance_required_for_each_participated_session': True,
        'exact_session_count_or_calendar_dates': None,
        'C1_and_C2_same_session_certified': False,
        'next_day_revisit_in_canon_preserved': True,
        'next_day_revisit_exact_correspondence_to_C1_assigned': False,
        'roles': {
            'school_plan_authority': 'Existing fictional after-class activity envelope; no new standing team membership.',
            'school_attendance_and_academic_functions': 'Recheck all three trial-day conditions before each participated session; keep records and any disciplinary decisions separate.',
            'coach': 'Receive limited participation clearance, arrange supervised activity and safety; no unilateral attendance, registration or contest authority.',
        },
        'modeled_pre_participation_check_each_session': {
            'same_day_class_attendance': SATISFIED,
            'academic_supplement': SATISFIED,
            'punctuality': SATISFIED,
        },
        'academic_supplement_is_future_promise_only': False,
        'fictional_limited_clearance_for_locked_followup_events': True,
        'actual_real_school_or_case_records_certified': False,
        'exact_attendance_supplement_or_clearance_records': None,
        'exact_guardian_notice_or_consent_rule': None,
        'exact_training_format_or_facility_route': None,
        'official_team_membership_certified': False,
        'league_registration_certified': False,
        'contest_eligibility_certified': False,
        'retrospective_attendance_deletion': False,
        'locked_C1_C2_C3_unchanged': True,
        'new_dramatized_school_event_or_dialogue': False,
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {p: sha((root / p).read_bytes()) for p in SOURCES},
        'assessment': {
            'school_authority_route_for_followup_design_specified': True,
            'all_three_conditions_rechecked_in_fictional_model': True,
            'real_individual_approval_or_records_verified': False,
            'third_final_function_added_by_this_artifact': False,
            'independent_review_required_before_function_promotion': True,
        },
        'final_episode_functions_completed_this_artifact': 0,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'author_locked': False,
        'new_author_decisions': 0, 'manuscript_count': 0,
        'manuscript_allowed': False, 'design_gate': 'CLOSED',
    }


def render(data):
    return '\n'.join([
        '# A01 첫 기여까지의 후속 훈련 운영 경로', '',
        '이 문서는 [첫 체험 운영안](A01_TRIAL_SCHOOL_OPERATING_PATH_2026_10_07.md)의 **가상학교 설계 확장**이다. 첫 체험의 일회 허용을 다음 모든 훈련의 자동 허가로 읽지 않는다.', '',
        '## 선택한 범위', '',
        '- 같은 가상학교 방과 후 농구 운영계획을 C1–C3에 필요한 감독 지도·안전 범위에서 사용한다. 첫 체험 뒤 새 상시 선수 신분이나 대회 출전 자격을 만들지 않는다.',
        '- 다음에 참여하는 각 훈련 앞에서 학교의 출석/학업 담당 기능이 **당일 수업 출석·학업보충·시간 준수 세 조건 모두를 다시 확인해 충족**한 경우에만 감독이 제한된 지도·안전 감독을 맡는다. 보충을 단순 미래 약속으로 대체하지 않는다.',
        '- 첫 완패 다음 날의 자발적 체육관 재방문은 정본에서 보존한다. 그 재방문이 C1의 정확한 다음 훈련과 같은 날인지는 배정하지 않는다. C1과 C2가 같은 세션인지, 총 몇 회 참여했는지, 정확 날짜·시설 이동·훈련 형식도 미정이다.',
        '- C1 잔류, C2 리바운드→아웃렛→팀 득점, C3 필요하다는 자기 느낌은 기존 잠긴 사건이다. 운영안은 새 장면·대사·동료 반응을 만들지 않는다.', '',
        '## 권한과 검증 한계', '',
        '- 감독은 훈련 일정과 안전을 맡되 출결·징계·보충기록·선수등록·대회 자격을 단독 처리하지 않는다. 학교의 출결 결과와 학업보충의 정확 기록은 실증하지 않는다.',
        '- 이 절차는 2015 공식자료가 명령한 전국 공통 양식이 아니라 [2015 근거 원장](../research/A01_KOREA_2015_SCHOOL_TRIAL_BOUNDARY.md)의 권한 경계와 양립하도록 선택한 가상학교 운영 모델이다.',
        '- 이 문서는 학교 권한의 반복 경로만 지정한다. 세 번째 최종 회차 기능이나 기존 후보 CF07을 완료/등록하지 않는다. 전체 G13/G14·실제 Pack·원고는 미완료, `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError) as exc:
        return [f'source construction: {exc}']
    errors = [] if data == expected else ['record differs from current bounded follow-up model']
    _, blueprint_errors = blueprint_check.check(root=root, unit='first-contribution')
    errors.extend(f'first-contribution: {e}' for e in blueprint_errors)
    return errors


def self_test(data):
    mutations = [
        ('automatic recurrence', lambda d: d.update(first_trial_permission_automatically_recurs=True)),
        ('skip supplement', lambda d: d['modeled_pre_participation_check_each_session'].pop('academic_supplement')),
        ('future only', lambda d: d.update(academic_supplement_is_future_promise_only=True)),
        ('real record', lambda d: d.update(actual_real_school_or_case_records_certified=True)),
        ('false registration', lambda d: d.update(league_registration_certified=True)),
        ('C1 date invention', lambda d: d.update(next_day_revisit_exact_correspondence_to_C1_assigned=True)),
        ('false gate', lambda d: d.update(manuscript_allowed=True)),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        assert validate(candidate), name
    return len(mutations)


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
    print(json.dumps({'followup_path': data['status'], 'third_function_added': 0,
                      'negative_controls': tested, 'current': not errors,
                      'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
