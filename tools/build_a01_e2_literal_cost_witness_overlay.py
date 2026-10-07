"""Select one same-trial A01-S1 literal choice/cost witness without editing E2."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a01_e2_literal_cost_witness_overlay.py'
OUT = 'design/A01_E2_LITERAL_COST_WITNESS_SELECTED_OVERLAY_2026_10_08.json'
MD = OUT[:-5] + '.md'
MEMO = 'reviews/A01_S1_LITERAL_SCOPED_CLOSURE_MEMO_2026_10_08.md'
CANDIDATE = 'design/A01_S1_LITERAL_COST_WITNESS_CANDIDATE_2026_10_08.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
E1 = 'design/A01_E1_FINAL_EPISODE_FUNCTION.json'
E2 = 'design/A01_E2_FINAL_EPISODE_FUNCTION.json'
E3 = 'design/A01_E3_FINAL_EPISODE_FUNCTION.json'
AUDIT = 'design/A01_A02_SUBACT_EXIT_AUDIT_2026_10_07.json'
ALIGNMENT = 'design/A01_S1_OPERATING_ALIGNMENT_2026_10_07.json'
ALIGNMENT_MD = 'design/A01_S1_OPERATING_ALIGNMENT_2026_10_07.md'
SCHOOL = 'design/A01_TRIAL_SCHOOL_OPERATING_PATH_2026_10_07.json'
STORY = 'canon/STORY_BIBLE.md'
PIN = {
    CANDIDATE: '08073b1ba6b4786e371c97e9aa08597dafbea8d647aa435a6f76e71d6b567134',
    CP2: '2b291bca588302cbb254fc3417652f7d7532c46d7094221cdcceac60619c9db9',
    E1: '9c15706717053a274f254ada476c027ea619858e6cd4ae80d8d8b422b789405e',
    E2: '306dd7810fda0395dc722ab953ebac9ef1e4cf3db0cc4a9dc0266a8a2b2e5285',
    E3: 'edbccc96f145274f4dfcfc2bbaebdce1477b0f3f3426a5420848aadfde1f4911',
    AUDIT: 'f5c4375908ed849e2f577e7fdb0181707aba4609f759acd75a434deb0a8d8e89',
    ALIGNMENT: '1169c33c8f2a23ff6a5e19d9dc300cd9e17a4ed6e6a26bee6654843eb3b9f7b4',
    ALIGNMENT_MD: '68779eab4b2b15b84c128c854a65861a09b05728c153fe5f2eae8ac74abcefbc',
    SCHOOL: '181988c7426cf54e7d553d84fbda5106d3262247443acfcad713b8cdf4e1646b',
    STORY: '9eb986c089c07007caedc40eabe03d6d798f77f7a09fbd37d57c4242af1421be',
}
SELECTED_W = {
    'id': 'W',
    'temporal_order': 'locked T1 entry < selected same-trial W < locked T2 rival defeat',
    'selected_actor': 'protagonist',
    'assigning_actor': 'coach inside the separately cleared limited school trial',
    'selected_action': '주인공은 먼저 재능을 보이겠다는 요구 대신 연습 공을 출발 위치에 놓고 다음 짧은 반복을 위해 다시 가져다 놓는다.',
    'visible_result': '감독과 곁의 동료에게 다음 반복에 쓸 공이 준비된 것이 보인다.',
    'direct_present_cost': '주인공이 자신을 먼저 보일 수 있던 짧은 순번과 즉시 주목을 공 준비에 쓰며, 그 일로 칭찬이나 평가를 받지는 않는다.',
    'immediate_showcase_time_foregone': True,
    'immediate_praise_offered_or_received': False,
    'preparation_refused': False,
    'school_registration_attendance_or_discipline_changed': False,
    'official_team_or_contest_eligibility_granted': False,
    'new_session_or_game': False,
    'later_s2_rebound_outlet_prepaid': False,
    't1_pride_motive_rewritten': False,
    't2_locked_defeat_changed': False,
}


def norm_text(root, rel):
    return (root / rel).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def digest(root, rel):
    return hashlib.sha256(norm_text(root, rel).encode('utf-8')).hexdigest()


def load(root, rel):
    return json.loads(norm_text(root, rel))


def physical(root):
    for rel, expected in PIN.items():
        assert digest(root, rel) == expected, 'Physical source pin differs: ' + rel
    return {rel: json.loads(norm_text(root, rel)) for rel in PIN if rel.endswith('.json')}


def sources(root):
    return {rel: load(root, rel) for rel in PIN if rel.endswith('.json')}


def witness():
    return copy.deepcopy(SELECTED_W)


def assert_sources(s, root):
    assert s == physical(root), 'Returned source differs from physical source'
    cand, cp2, e1, e2, e3 = (s[x] for x in [CANDIDATE, CP2, E1, E2, E3])
    assert cand['source_sha256'] == {k: PIN[k] for k in [CP2, E1, E2, E3, AUDIT, ALIGNMENT_MD, SCHOOL, STORY]}
    assert cand['status'] == 'REVIEW_PENDING_NOT_SELECTED_NOT_REGISTERED'
    assert cand['one_routine_witness']['placement'].startswith('Within already selected supervised first trial')
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    s1 = next(x for x in cp2['subacts'] if x['id'] == 'A01-S1')
    assert s1['choice'] == '재능을 보여 달라는 기대만 붙들지 않고 농구부가 맡기는 기본 준비부터 해 본다'
    assert s1['cost'] == '즉시 칭찬을 포기'
    assert s1['exit_state'] == '참여와 회피가 분리됨'
    assert e1['exit_state'] == e2['entry_state']
    assert e2['exit_state'] == e3['entry_state']
    assert e2['episode_function_id'] == 'A01-EF-002' and e2['subact'] == 'A01-S1'
    assert e2['internal_order'] == [x['id'] for x in e2['beats']] == ['T1', 'T2']
    assert '완패' in e2['exit_state'] and e3['primary_subact'] == 'A01-S2'
    assert e2['school_authority']['fictional_school_operating_path_selected'] is True
    assert e2['school_authority']['real_school_or_case_records_certified'] is False
    assert s[SCHOOL]['condition_handling']['limited_trial_clearance_in_fictional_model'] == 'SELECTED_FOR_LOCKED_T1_ONLY'
    old = s[AUDIT]
    assert old['counts']['subact_bounded_pass'] == 5 and old['counts']['subact_specific_hold'] == 1
    assert old['subact_exit_rows'][0]['exit_audit_result'] == 'HOLD_CP2_CHOICE_AND_COST_NOT_OBSERVED_IN_S1'
    assert s[ALIGNMENT]['original_basic_preparation_and_praise_cost_certified_in_s1'] is False
    return cand, s1, e2


def assert_witness(w):
    assert w == SELECTED_W, 'Returned W meaning differs from selected routine'
    assert w['preparation_refused'] is False and w['immediate_praise_offered_or_received'] is False
    assert w['school_registration_attendance_or_discipline_changed'] is False


def build(root=ROOT):
    s = sources(root)
    cand, s1, e2 = assert_sources(s, root)
    w = witness()
    assert_witness(w)
    return {
        'schema': 'A01_E2_LITERAL_COST_WITNESS_SELECTED_OVERLAY_V1',
        'status': 'SELECTED_ROUTINE_SAME_TRIAL_WITNESS_PENDING_INDEPENDENT_REVIEW',
        'source_hash_method': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_sha256': {**PIN, SELF: digest(root, SELF)},
        'selection_basis': 'Root routine design selection after the review-pending candidate; no new author lock',
        'target_subact': 'A01-S1',
        'target_original_function': 'A01-EF-002',
        'original_cp2_choice': s1['choice'],
        'original_cp2_cost': s1['cost'],
        'original_cp2_exit': s1['exit_state'],
        'original_e2_exact_entry': e2['entry_state'],
        'original_e2_exact_exit': e2['exit_state'],
        'original_e2_locked_order': ['T1', 'T2'],
        'selected_overlay_order': ['T1', 'W', 'T2'],
        'selected_witness': w,
        'literal_choice_cost_scope': 'One same-trial visible choice and present time/attention cost; praise was neither offered nor received.',
        'literal_cp2_witness_selected': True,
        'literal_scoped_exit_supported_pending_independent_review': True,
        'literal_scoped_pass_certified': False,
        'original_audit_historical_result': '5 bounded passes / 1 A01-S1 literal HOLD',
        'operating_alignment_historical_result': '6 bounded operating exits without literal S1 preparation certification',
        'existing_e1_e2_e3_files_modified': False,
        'new_episode_function_count': 0,
        'new_published_episode_count': 0,
        'whole_g13_complete': False,
        'whole_g14_complete': False,
        'actual_context_packs': 0,
        'manuscript_allowed': False,
        'independent_review_completed': False,
        'freeze': 'v0.30 PARTIAL',
        'design_gate': 'CLOSED',
    }


def render(d):
    w = d['selected_witness']
    return '\n'.join([
        '# A01-E2 첫 체험의 원 CP2 선택·비용 관측 오버레이', '',
        '선택된 가상 루틴 W를 기존 T1과 T2 사이의 **같은 첫 체험**에 붙인다. 원 E2, 그 정확한 출구와 E3 인계는 수정하지 않는다.', '',
        f"- 관측 행동: {w['selected_action']}",
        f"- 눈앞 결과: {w['visible_result']}",
        f"- 현재 비용: {w['direct_present_cost']}",
        '- 칭찬 제안·실제 칭찬·감독의 평가·팀 등록·출결 삭제는 발생했다고 주장하지 않는다.',
        '- T1의 자존심 동기와 T2의 라이벌 앞 완패를 보존하고, E3의 다음 훈련 리바운드·아웃렛은 S2에 남긴다.',
        '- 원 A01-S1 감사의 `5 PASS / 1 HOLD`와 운영 정렬 `6 bounded PASS`는 역사로 유지한다. 이 오버레이의 원 CP2 literal 출구는 독립 검문 전까지 승인되지 않는다.',
        '- 기능·공개 회차 증분 0, 전체 G13/G14 false, Pack0, 원고 게이트 CLOSED, freeze v0.30 PARTIAL.', '',
    ])


def render_memo(d):
    return '\n'.join([
        '# A01-S1 원 CP2 literal 출구 범위 메모', '',
        '기존 감사의 HOLD는 E1–E2에 기본 준비와 즉시 칭찬 포기 행동이 없었던 당시 판정으로 보존한다. 운영 정렬 PASS는 첫 훈련 진입과 완패의 참여/회피 분리만 인정했다.', '',
        '선택된 새 오버레이 W는 **첫 체험의 T1 뒤·T2 앞**에서 주인공이 자기 과시 순번을 공 준비와 짧은 반복에 쓰는 직접 관측이다. 즉시 칭찬이 실제 제안되거나 거절당한 사건은 아니다. 원 CP2 비용은 칭찬을 좇을 시간과 주목을 사용한 선택으로 한정한다.', '',
        '루틴 선정과 source-current 생성은 완료됐으나 독립 검문 전이므로 literal CP2 `PASS` 계수는 아직 0이다. 검문 뒤에는 새 현행 소비자가 좁은 literal choice/cost/exit를 판정할 수 있다. 기존 E2/T1/T2와 E3, 첫 여섯 소막 감사 파일은 그대로 유지한다.', '',
        '원고 게이트 CLOSED · freeze v0.30 PARTIAL · 전체 G13/G14 false · 실제 Pack0.', '',
    ])


def validate(d, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, OSError, ValueError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if d == expected else ['overlay differs from source-bound selection']


def self_test():
    original_witness = globals()['witness']
    original_load = globals()['load']
    rejected = []
    for label, field, value in [
        ('preparation_refused', 'preparation_refused', True),
        ('praise_prepaid', 'immediate_praise_offered_or_received', True),
        ('school_state_promoted', 'school_registration_attendance_or_discipline_changed', True),
    ]:
        def changed(field=field, value=value):
            w = original_witness()
            w[field] = value
            return w
        globals()['witness'] = changed
        try:
            build()
        except AssertionError:
            rejected.append(label)
        else:
            raise AssertionError('False pass: ' + label)
        finally:
            globals()['witness'] = original_witness
    def wrong_e2(root, rel):
        obj = original_load(root, rel)
        if rel == E2:
            obj['exit_state'] = '첫 체험과 공식 팀 등록까지 완료했다'
        return obj
    globals()['load'] = wrong_e2
    try:
        build()
    except AssertionError:
        rejected.append('existing_E2_exit_mutation')
    else:
        raise AssertionError('False pass: existing E2 exit')
    finally:
        globals()['load'] = original_load
    return rejected


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write', action='store_true')
    p.add_argument('--check', action='store_true')
    p.add_argument('--self-test', action='store_true')
    args = p.parse_args()
    d = build()
    if args.write:
        (ROOT / OUT).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
        (ROOT / MD).write_text(render(d), encoding='utf-8', newline='\n')
        (ROOT / MEMO).write_text(render_memo(d), encoding='utf-8', newline='\n')
    errors = validate(d)
    if args.check:
        saved = load(ROOT, OUT)
        errors += validate(saved)
        if norm_text(ROOT, MD) != render(saved):
            errors.append('Markdown differs from selected overlay')
        if norm_text(ROOT, MEMO) != render_memo(saved):
            errors.append('Closure memo differs from selected overlay')
    controls = self_test() if args.self_test and not errors else []
    print(json.dumps({'current': not errors, 'errors': errors, 'writer_controls_rejected': controls}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
