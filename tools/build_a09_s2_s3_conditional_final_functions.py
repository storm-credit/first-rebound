"""Build two bounded A09 function routes without certifying national-team access."""

import argparse
import hashlib
import json
from pathlib import Path

import build_a09_e1_final_episode_function as previous_builder
import build_a09_a14_bounded_function_preparation as scope_builder


ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a09_s2_s3_conditional_final_functions.py'
PREVIOUS = 'design/A09_E1_FINAL_EPISODE_FUNCTION.json'
SCOPE = 'design/A09_A14_BOUNDED_FUNCTION_PREPARATION_2026_10_07.json'
CF = 'design/A09_2023_24_CONDITIONAL_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
GATE = 'control/NATIONAL_TEAM_MILITARY_SCOPE_GATE.md'
OUTPUT = Path('design/A09_S2_S3_CONDITIONAL_FINAL_FUNCTIONS_2026_10_07.json')
SOURCES = (SELF, PREVIOUS, SCOPE, CF, CP2, GATE)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def sha(raw):
    normalized = raw.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def build(root=ROOT):
    previous, scope, cf, cp2 = (load(root, p) for p in (PREVIOUS, SCOPE, CF, CP2))
    assert previous == previous_builder.load(root, previous_builder.OUTPUT)
    assert not previous_builder.validate(previous, root=root) and previous['independent_review_completed']
    assert scope == scope_builder.load(root, scope_builder.OUTPUT)
    assert not scope_builder.validate(scope, root=root) and scope['independent_review_completed']
    assert cf == scope_builder.load(root, CF), 'candidate loader differs from reviewed source'
    assert sha((root / CF).read_bytes()) == scope['source_sha256'][CF]
    assert cp2 == scope_builder.load(root, CP2), 'CP2 loader differs from reviewed source'
    assert sha((root / CP2).read_bytes()) == scope['source_sha256'][CP2]
    candidates = {row['id']: row for row in cf['functions']}
    subacts = {row['id']: row for row in cp2['subacts']}
    for sid, ids in [('A09-S2', ['A09-CF02', 'A09-CF03']),
                     ('A09-S3', ['A09-CF04', 'A09-CF05'])]:
        assert [candidates[i]['subact'] for i in ids] == [sid] * len(ids)
        assert sid in subacts and not subacts[sid]['manuscript_allowed']
    assert candidates['A09-CF02']['entry_state'] == previous['exit_state']
    assert candidates['A09-CF03']['entry_state'] == candidates['A09-CF02']['changed_state']
    assert candidates['A09-CF04']['entry_state'] == candidates['A09-CF03']['changed_state']
    assert candidates['A09-CF05']['entry_state'] == candidates['A09-CF04']['changed_state']
    assert candidates['A09-CF05']['next'] == 'A10-S1'
    gate = (root / GATE).read_text(encoding='utf-8-sig')
    assert '2023_path: joint_attempt_selected' in gate
    assert '2023_gold: R09_CAUSALITY_HOLD' in gate

    e2 = {
        'proposed_episode_function_id': 'A09-EF-002', 'proposed_global_function_order': 44,
        'planned_allocation_slot': 444, 'primary_subact': 'A09-S2',
        'source_conditional_functions': ['A09-CF02', 'A09-CF03'],
        'previous_function': {'id': previous['episode_function_id'], 'path': PREVIOUS,
                              'exact_full_exit': previous['exit_state']},
        'entry_state': previous['exit_state'],
        'single_function': '조건부 공동 훈련에서 맡은 권한을 나누어 시험하고 자신의 어긋남을 한 번 고친다',
        'institutional_prerequisite': '실제 대표팀 합류, 구단 허가·보험, 훈련 참여와 역할 전달이 별도로 성립한 경우에만 이 가상 국소 수행을 배치한다',
        'conditional_entry_gate': 'A09-CF01 이후 실제 합류·훈련허용·역할전달이 별도 선택되기 전에는 A09-S2 국소 수행이 발생하지 않는다',
        'selected_institutional_bridge': False,
        'institutional_prerequisite_executed_or_certified': False,
        'unit_choice': candidates['A09-CF02']['choice'],
        'direct_present_cost': candidates['A09-CF02']['direct_cost'] + ' 이후 ' + candidates['A09-CF03']['direct_cost'],
        'beats': [
            {'id': 'A09-S2-P1', 'action': '전달받은 제한 역할 안에서 라이벌의 실제 첫 이점과 가까운 동료 위치를 확인한다. 자기 공격을 더 가져갈 수 있어도 공을 연결하고 스크린 뒤 다음 위치를 찾는다.', 'scope': 'SELECTED_FICTIONAL_CONDITIONAL_TRAINING_ACTION'},
            {'id': 'A09-S2-P2', 'action': '한 번의 같은 허용 훈련에서 자신이 공을 넘긴 뒤 다음 위치를 늦게 잡아 연결이 끊기는 모습을 직접 본다. 타인의 심리나 승패를 해석하지 않는다.', 'scope': 'SELECTED_FICTIONAL_OWN_ERROR_OBSERVATION'},
            {'id': 'A09-S2-P3', 'action': '허용된 영상과 받은 지시에서 자기 위치 오류를 대조하고 감독에게 다음 위치를 확인해 묻는다. 같은 제한 과제에서 공을 다시 연결한 뒤 이번에는 다음 위치로 먼저 이동한다.', 'scope': 'SELECTED_FICTIONAL_BOUNDED_RETRY_NOT_RELATION_RESOLUTION'},
        ],
        'exit_state': candidates['A09-CF03']['changed_state'],
        'cp2_exit_target': subacts['A09-S2']['exit_state'],
        'whole_subact_exit_certified': False,
        'next_conditional_function': 'A09-CF04',
    }
    e3 = {
        'proposed_episode_function_id': 'A09-EF-003', 'proposed_global_function_order': 45,
        'planned_allocation_slot': 445, 'primary_subact': 'A09-S3',
        'source_conditional_functions': ['A09-CF04', 'A09-CF05'],
        'previous_function': {'id': e2['proposed_episode_function_id'], 'path': str(OUTPUT).replace('\\', '/'),
                              'exact_full_exit': e2['exit_state']},
        'entry_state': e2['exit_state'],
        'single_function': 'Chicago 복귀 준비를 대표팀 성과와 구분해 다시 배정하고 제한된 미드포스트 과제를 시험한다',
        'institutional_prerequisite': '대표팀 참가와 Chicago 복귀, 구단이 전달한 훈련 일정·허용 범위가 실제 성립한 경우에만 이 가상 국소 수행을 배치한다',
        'conditional_entry_gate': 'A09-S2 가상 수행만으로 실제 대표팀 참가·이동·Chicago 복귀가 성립하지 않으며 그 별도 선택 전에는 A09-S3 국소 수행이 발생하지 않는다',
        'selected_institutional_bridge': False,
        'institutional_prerequisite_executed_or_certified': False,
        'unit_choice': candidates['A09-CF04']['choice'] + ' 이어서 ' + candidates['A09-CF05']['choice'],
        'direct_present_cost': candidates['A09-CF04']['direct_cost'] + ' 이후 ' + candidates['A09-CF05']['direct_cost'],
        'beats': [
            {'id': 'A09-S3-P1', 'action': '전달받은 Chicago 훈련 과제와 실제 놓친 준비 항목을 대조해 개인 신기술 시간을 줄이고 팀의 허용된 연결 반복 한 구간에 배정한다.', 'scope': 'SELECTED_FICTIONAL_CONDITIONAL_RETURN_PREPARATION'},
            {'id': 'A09-S3-P2', 'action': '별도로 허용된 미드포스트 반복에서 짧은 발위치와 공 보유를 시도한다. 정렬된 수비 앞 공격 길이 닫히면 공을 기존 팀 연결로 반환한다.', 'scope': 'SELECTED_FICTIONAL_BOUNDED_SKILL_TRIAL'},
            {'id': 'A09-S3-P3', 'action': '반환 선택과 팀 연결은 관측하지만 개인 공격 완성이나 실제 NBA 경기 효율은 이 한 구간에서 알 수 없다고 남긴다.', 'scope': 'OBSERVED_LOCAL_BOUNDARY'},
        ],
        'exit_state': candidates['A09-CF05']['changed_state'],
        'cp2_exit_target': subacts['A09-S3']['exit_state'],
        'whole_subact_exit_certified': False,
        'next_conditional_function': 'A10-S1',
    }
    return {
        'schema': 'A09_S2_S3_CONDITIONAL_FINAL_FUNCTIONS_V1',
        'status': 'CONDITIONAL_FUNCTION_FAMILY_NOT_REGISTERABLE_UNTIL_INSTITUTIONAL_BRIDGES',
        'independent_review_completed': True,
        'independent_review_basis': 'Root read original CF02-05, CP2 institutional constraints, selected joint-attempt gate and E1 exact exit. Both entry bridges remain unselected, institution-dependent actions remain hypothetical and final-register increment stays zero. Source-bound check passed; this does not certify participation, return, medal, military status or whole subact exit.',
        'functions': [e2, e3],
        'local_function_route_prepared': True,
        'selected_institutional_bridge': False,
        'registered_final_function_count_increment': 0,
        'institutional_participation_or_return_executed': False,
        'national_team_roster_permission_insurance_travel_or_medal_certified': False,
        'military_status_certified': False,
        'actual_nba_game_minutes_score_or_efficiency_certified': False,
        'rival_reconciliation_or_team_win_certified': False,
        'skill_mastery_or_major_growth_certified': False,
        'whole_A09_complete': False, 'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'published_episode_number': None,
        'manuscript_word_count': None, 'manuscript_count': 0, 'manuscript_allowed': False,
        'new_author_lock': False, 'design_gate': 'CLOSED',
        'source_hash_method': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_sha256': {p: sha((root / p).read_bytes()) for p in SOURCES},
    }


def render(data):
    lines = ['# A09 S2·S3 조건부 기능 가족', '',
             '두 기능은 상위 기관 조건이 성립할 때 사용할 수 있는 가상 행동 설계다. 현재 대표팀 명단·허가·보험·실제 이동 및 Chicago 복귀를 인증하지 않는다. 등록 가능한 최종 기능 증분은 0이다.', '']
    for row in data['functions']:
        lines += [f"## {row['proposed_episode_function_id']} 후보 — {row['primary_subact']}", '',
                  f"- 진입: {row['entry_state']}", f"- 기능: {row['single_function']}",
                  f"- 선행조건: {row['institutional_prerequisite']}",
                  f"- 진입 게이트: {row['conditional_entry_gate']}",
                  f"- 선택: {row['unit_choice']}", f"- 즉시 비용: {row['direct_present_cost']}"]
        lines += [f"- {beat['id']}: {beat['action']}" for beat in row['beats']]
        lines += [f"- 국소 출구: {row['exit_state']}",
                  f"- CP2 전체 소막 출구 목표: {row['cp2_exit_target']} (미인증)", '']
    lines += ['제안된 계획 슬롯 444·445는 출판 회차도 등록 기능도 아니다. 참가·복귀·실제 NBA 경기·라이벌 화해·대회 결과·금메달·병역·기술 완성은 미인증이다.',
              '원 CF·기관조건·E1 정확출구를 root가 별도 검문했다. 기관 진입 연결은 여전히 미선택이며 누적 최종등록 증분0이다. 전체 A09/G13/G14·실제 Pack·원고 미완료, 게이트 `CLOSED`.', '']
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        return [] if data == build(root) else ['A09 S2/S3 differs from source-bound build']
    except (AssertionError, KeyError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / OUTPUT.with_suffix('.md')).write_text(render(data), encoding='utf-8')
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors = [] if saved == data else ['A09 S2/S3 differs from fresh source-bound build']
        if (ROOT / OUTPUT.with_suffix('.md')).read_text(encoding='utf-8') != render(saved):
            errors.append('Markdown differs')
        print(json.dumps({'current': not errors, 'errors': errors}))
        if errors:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
