"""Prepare a bounded fictional presentation of A04-S1's existing skill sample."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a04_e3_final_episode_function as previous_builder


ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a04_s1_external_presentation_working_model.py'
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
AUDIT = 'design/A04_S1_PREPARATION_EXIT_AUDIT_2026_10_07.json'
OUTPUT = Path('design/A04_S1_EXTERNAL_PRESENTATION_WORKING_MODEL_2026_10_07.json')
SOURCES = (SELF, PREVIOUS, CP2, AUDIT)
CP2_CHOICE = '신체 측정으로 순번을 단정하지 않고 준비한 기술의 가능한 범위와 한계를 평가에 내놓는다'
CP2_COST = '불확실한 평가 수용'
CP2_EXIT = '보여줄 기술 표본 명확화'


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def build(root=ROOT):
    previous = load(root, PREVIOUS)
    cp2 = load(root, CP2)
    audit = load(root, AUDIT)
    assert previous == previous_builder.load(root, previous_builder.OUTPUT)
    assert not previous_builder.validate(previous, root=root), 'A04 E3 must be source-current'
    assert previous['episode_function_id'] == 'A04-EF-003'
    assert previous['next_unit']['id'] == 'A04-CF05'
    assert previous['whole_g13_complete'] is False and previous['manuscript_allowed'] is False
    subact = next(row for row in cp2['subacts'] if row['id'] == 'A04-S1')
    assert subact['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert subact['choice'] == CP2_CHOICE
    assert subact['cost'] == CP2_COST and subact['exit_state'] == CP2_EXIT
    assert audit['status'] == 'BOUNDED_OPERATING_PREPARATION_EXIT_PASS_ORIGINAL_LITERAL_PRESENTATION_UNOBSERVED'
    assert cp2['manuscript_allowed'] is False
    return {
        'schema': 'A04_S1_EXTERNAL_PRESENTATION_WORKING_MODEL_V1',
        'status': 'SELECTED_ROUTINE_EXTERNAL_PRESENTATION_INDEPENDENTLY_REVIEWED',
        'independent_review_completed': True,
        'scope': 'One bounded external presentation action after private coached preparation; not an extra mandatory episode or official NBA evaluation',
        'previous_function': {'id': previous['episode_function_id'], 'path': PREVIOUS,
                              'exact_full_exit': previous['exit_state']},
        'original_cp2': {'choice': subact['choice'], 'cost': subact['cost'],
                         'exit_state': subact['exit_state'],
                         'old_measurement_certainty_entry_not_inherited': True},
        'fictional_authority': {
            'observer': '가상 독립 사전 드래프트 평가 상담자',
            'outside_previous_private_coached_session': True,
            'NBA_club_or_Combine_official': False,
            'authorized_scope': '선수가 스스로 가져온 역할·공격 한계 자료와 짧은 비공식 동작 시연을 보고 질문한다',
            'official_board_medical_or_contract_authority': False,
        },
        'single_function': '준비한 좁은 역할 증거와 공격 한계를 외부 관찰자에게 함께 제시한다',
        'operating_actions': [
            {'id': 'P1', 'action': '주인공은 자신의 Texas Tech 역할 관측과 우승팀 소속 사실을 나누고, 코너 캐치 뒤 한 드리블이 막힌 지점 및 측정 수치가 빈 항목을 같은 요약에 둔다.',
             'evidence_scope': 'A04-EF-001~003의 개인 역할·공격 관측과 별도 공개 우승 역사; A03 기능이나 새 공식 수치가 아님'},
            {'id': 'P2', 'action': '비공식 외부 상담자는 그 요약을 받고 허용된 짧은 코너 한 드리블→가까운 동료 연결 시도를 직접 본다. 주인공은 성공 장면만 고르지 않고 다음 자가 창조가 아직 검증되지 않았다고 설명한다.',
             'evidence_scope': '가상 외부 제시·수령·관측; 구단 평가 또는 실전 결과 아님'},
            {'id': 'P3', 'action': '상담자는 실제 구단 순번이나 의료 판정을 내리지 않고, 이번 제시에서 확인 가능한 좁은 역할과 여전히 미답인 개인 공격을 분리해 되묻는다.',
             'evidence_scope': '상담자의 공개된 질문만; 사적 판단·점수·공식 피드백 아님'},
        ],
        'choice': '신체 장점이나 우승 맥락만 내세우지 않고 역할 증거와 공격 한계를 함께 외부에 제시한다',
        'direct_cost': '약점 노출을 감수하고 자신에게 유리한 장면만 고를 수 있는 홍보 기회를 줄인다',
        'bounded_exit': '준비한 기술 표본과 미증명 공격의 경계가 외부 관찰자에게 실제 제시되었다. 받은 것은 질문뿐이고 구단 평가·초청·순번 약속은 아니다.',
        'resolves_prior_audit_gap_only_if_selected_and_reviewed': '원 선택의 평가에 내놓는 행위 미관측',
        'new_final_episode_functions': 0,
        'published_episode_or_extra_slot_required': False,
        'official_Combine_invitation_or_measurement': False,
        'NBA_club_submission_or_grade': False,
        'medical_clearance_or_exact_pick_certified': False,
        'Chicago_2018_direction_changed': False,
        'new_author_lock': False,
        'whole_A04_Act_complete': False,
        'whole_g13_complete': False,
        'whole_g14_complete': False,
        'actual_context_packs': 0,
        'manuscript_count': 0,
        'manuscript_allowed': False,
        'design_gate': 'CLOSED',
        'source_hash_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_sha256': {str(p): sha((root / p).read_bytes()) for p in SOURCES},
    }


def render(data):
    lines = ['# A04-S1 외부 제시 공백의 가상 운영안', '',
             '**상태:** 국소 독립 검문을 거친 가상 운영 선택. A04-EF-003의 개인 지도 훈련과 구별되는 한 번의 비공식 외부 제시다. 새 필수 회차나 공식 NBA 평가를 만들지 않는다.', '',
             f"- 정확 진입: {data['previous_function']['exact_full_exit']}",
             f"- 관찰자 권한: {data['fictional_authority']['authorized_scope']}",
             f"- 선택: {data['choice']}", f"- 직접 비용: {data['direct_cost']}", '',
             '| 단계 | 직접 보이는 행동 |', '| --- | --- |']
    for row in data['operating_actions']:
        lines.append(f"| {row['id']} | {row['action']} |")
    lines += ['', f"- 제한 출구: {data['bounded_exit']}",
              '- 원 CP2의 신체 측정만으로 순번 확신은 주인공의 현재 믿음으로 상속하지 않는다. 공식 Combine 초청·측정·의료, NBA 구단 접수·등급·정확 지명·계약은 미확정이다.',
              '- 이 선택의 제한된 외부 제시 행위에 대한 현재 판정은 별도 추가 감사에 기록한다. 전체 A04/G13/G14·실제 Pack·원고는 미완료이고 게이트는 CLOSED다.', '']
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['external presentation model differs from source-bound build']


def self_test(data):
    cases = [
        ('club authority', lambda x: x['fictional_authority'].update(NBA_club_or_Combine_official=True)),
        ('exact pick', lambda x: x.update(medical_clearance_or_exact_pick_certified=True)),
        ('review erased', lambda x: x.update(independent_review_completed=False)),
    ]
    for name, mutation in cases:
        changed = copy.deepcopy(data)
        mutation(changed)
        assert validate(changed), name
    original_load = load
    for name, path, mutation in [
        ('CP2 selection reversed', CP2, lambda x: next(row for row in x['subacts'] if row['id'] == 'A04-S1').update(choice='신체 측정만으로 22순위를 보장받는다')),
        ('E3 prior exit falsely official', PREVIOUS, lambda x: x.update(exit_state='공식 구단 평가를 이미 받아 정확한 22순위를 확정했다')),
    ]:
        def altered(root, requested, path=path, mutation=mutation):
            source = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                source = copy.deepcopy(source)
                mutation(source)
            return source
        with patch(__name__ + '.load', side_effect=altered):
            assert validate(data), name
    return len(cases) + 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / OUTPUT.with_suffix('.md')).write_text(render(data), encoding='utf-8')
    errors = validate(data)
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors += validate(saved)
        if (ROOT / OUTPUT.with_suffix('.md')).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'current': not errors, 'errors': errors, 'negative_controls': tested,
                      'status': data['status']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
