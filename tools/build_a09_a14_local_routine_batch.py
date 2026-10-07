"""Select six bounded routine observations without resolving six future season outcomes."""

import argparse
import hashlib
import json
from pathlib import Path

import build_a08_finite_function_batch as a08_builder
import build_a09_a14_bounded_function_preparation as scope_builder


ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a09_a14_local_routine_batch.py'
A08 = str(a08_builder.OUTPUT).replace('\\', '/')
SCOPE = str(scope_builder.OUTPUT).replace('\\', '/')
OUTPUT = Path('design/A09_A14_LOCAL_ROUTINE_BATCH_2026_10_07.json')
SOURCES = (SELF, A08, SCOPE)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def sha(raw):
    normalized = raw.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def build(root=ROOT):
    a08, scope = load(root, A08), load(root, SCOPE)
    assert a08 == a08_builder.load(root, a08_builder.OUTPUT)
    assert not a08_builder.validate(a08, root=root), 'A08 currentness required'
    assert a08['independent_review_completed'] and a08['functions'][-1]['global_function_order'] == 42
    assert scope == scope_builder.load(root, scope_builder.OUTPUT)
    assert not scope_builder.validate(scope, root=root), 'six-Act scope currentness required'
    assert scope['independent_review_completed']
    assert len(scope['groups']) == 18 and scope['source_conditional_candidate_count'] == 27
    selected = [x for x in scope['groups'] if x['subact'].endswith('-S1')]
    assert [x['subact'] for x in selected] == [f'A{i:02d}-S1' for i in range(9, 15)]
    assert a08['functions'][-1]['exit_state'] == '자기 공격과 이양 뒤 재관여를 함께 시험하는 준비를 다음 연차로 가져가지만 공동 에이스 지위·마무리 권한·팀 성과는 미정이다'
    observed = [
        ('A09-S1',
         '주인공은 자신에게 전달된 구단·대표팀 일정 안내를 구분하고 가상 에이전트에게 자기 제출자료와 허가·보험 담당권한을 묻는다. 공격 개인훈련 한 구간을 자료정리와 대표팀 역할 파악에 쓴다.',
         '자기 제출자료 목록과 두 기관에 남은 질문을 실제로 정리해 전달한다. 명단·구단 허가·보험·이동은 여전히 성립하지 않는다.'),
        ('A10-S1',
         '허용된 가상 팀 훈련에서 주인공은 짧은 발동작·운반으로 한 공격 창을 열어 보지만 안쪽 도움에 막히자 긴 돌파를 멈추고 가까운 동료에게 다시 연결한다. 익숙한 전환 반복과 한 공격 시간을 포기한다.',
         '짧은 직접 공격이 막히는 위치와 실제 중단·재연결 동작이 같은 좁은 연습에서 보인다. 첫 공격 옵션 권한·실전 효율은 주어지지 않는다.'),
        ('A11-S1',
         '가상 코치가 허용한 제한 훈련에서 주인공은 직접 시작할 첫 공을 동료에게 넘기고 스크린 뒤 빈 공간으로 이동해 리바운드 준비 위치를 차지한다. 직접 운반과 자기 첫 공격 표본 한 번을 포기한다.',
         '공을 맡기고 무볼로 다시 참여한 이동과 위치가 직접 보이지만 동료 득점·실제 시즌 분담·MVP 결과는 알 수 없다.'),
        ('A12-S1',
         '주인공은 공개 가능한 비용과 자신에게 실제 전달된 가상 에이전트 설명을 근거로 자기 요구와 필요한 연결·수비 기능을 같은 표에 놓는다. 자기 기술을 더 반복할 시간을 자료정리에 쓴다.',
         '가상 에이전트에게 자기 요구와 유지할 기능의 차이를 질문·전달한 사실만 보인다. 새 계약·동료 감액·트레이드·벤치 구성은 이루어지지 않았다.'),
        ('A13-S1',
         '허용된 가상 반복에서 리바운드를 잡은 주인공은 자기 운반을 더 늘리는 대신 앞선 동료에게 전진 연결을 선택하고 이양 뒤 다음 위치로 달린다. 자기 운반 기록 기회와 추가 몸의 수고가 비용이다.',
         '리바운드→전진 연결→재관여의 좁은 동작만 직접 보인다. 잠긴 파이널 7차전 행동·동료 결승 득점의 정확 시즌·상대·수신자는 실행하지 않았다.'),
        ('A14-S1',
         '잠긴 팀 승리 기능 이후라는 상대순서만 보존한 별도 가상 훈련에서 주인공은 받은 역할의 공격 시작을 동료에게 넘기고 무볼 마무리 위치로 움직인다. 다른 허용 반복에서는 박스아웃 뒤 짧은 첫 연결을 맞춘다.',
         '다른 조합에서 시작권을 나누고 위치·첫 연결을 다시 맞춘 두 국소 동작만 보인다. 추가 우승·노화 정도·후배의 실제 경력·계약·정확 은퇴 연차는 정하지 않는다.'),
    ]
    by_id = {x['subact']: x for x in selected}
    rows = []
    for sid, action, result in observed:
        source = by_id[sid]
        rows.append({
            'id': sid.replace('-S1', '-RF-001'), 'source_subact': sid,
            'source_candidate_ids': source['candidate_ids'],
            'original_cp2_choice': source['cp2_choice'],
            'original_cp2_cost': source['cp2_cost'],
            'original_cp2_exit': source['cp2_exit'],
            'selected_fictional_routine_action_and_present_cost': action,
            'direct_observation_and_limit': result,
            'local_routine_observation_selected': True,
            'source_whole_subact_exit_certified': False,
            'source_whole_act_exit_certified': False,
            'global_final_function_order': 43 if sid == 'A09-S1' else None,
            'registered_by_this_packet': False,
        })
    return {
        'schema': 'A09_A14_LOCAL_ROUTINE_BATCH_V1',
        'status': 'SIX_LOCAL_ROUTINE_OBSERVATIONS_INDEPENDENTLY_REVIEWED',
        'independent_review_completed': True,
        'exact_A08_EF003_exit': a08['functions'][-1]['exit_state'],
        'rows': rows,
        'interact_unselected_bridge_boundaries': ['A09-S2/S3 national-team permission and actual return',
                                                  'A10–A12 specific season outcomes',
                                                  'A13 Game7 coordinate',
                                                  'A14 exact late-career calendar'],
        'locked_Finals_Game7_and_Chicago_one_club_retirement_functions_preserved': True,
        'locked_ending_performed_by_this_batch': False,
        'exact_2023_gold_2025_26_Finals_loss_2028_opponent_2035_retirement_selected': False,
        'new_global_final_functions_registered': 0,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'manuscript_count': 0, 'manuscript_allowed': False,
        'author_locked': False, 'design_gate': 'CLOSED',
        'source_hash_method': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_sha256': {p: sha((root / p).read_bytes()) for p in SOURCES},
    }


def render(data):
    lines = ['# A09–A14 국소 일상 기능 6개', '',
             '기존 18소막 중 각 Act 첫 소막의 좁은 행동만 가상 설계로 선택했다. 뒤 소막과 막 사이 역사·기관 결과를 건너뛰어 전역 최종 기능으로 등록하지 않는다.', '']
    for row in data['rows']:
        lines += [f"## {row['id']} · {row['source_subact']}", '',
                  f"- 행동·비용: {row['selected_fictional_routine_action_and_present_cost']}",
                  f"- 가시 결과·한계: {row['direct_observation_and_limit']}", '']
    lines += ['잠긴 파이널 7차전 결승 패스와 Chicago 원클럽 은퇴 기능은 보존한다. 정확 시즌·상대·수신자·은퇴 연차는 선택하지 않았다.',
              '', '전역 기능 등록0·전체 G13/G14 미완료·실제 Context Pack0·원고0. 설계·원고 게이트 `CLOSED`.', '']
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        return [] if data == build(root) else ['local routine batch differs from source-bound build']
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
        errors = validate(saved)
        if (ROOT / OUTPUT.with_suffix('.md')).read_text(encoding='utf-8') != render(saved):
            errors.append('Markdown differs')
        print(json.dumps({'current': not errors, 'errors': errors, 'local_rows': len(saved['rows'])}))
        if errors:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
