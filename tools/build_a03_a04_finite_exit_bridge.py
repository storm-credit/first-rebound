"""Build two narrow fictional observations for A03/A04 Act exit gaps."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a03_e2_final_episode_function as college_builder
import build_a04_e5_final_episode_function as draft_builder


ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a03_a04_finite_exit_bridge.py'
A03_E2 = str(college_builder.OUTPUT).replace('\\', '/')
A04_E5 = str(draft_builder.OUTPUT).replace('\\', '/')
AUDIT = 'design/A03_A04_BOUNDED_EXIT_AUDIT_2026_10_07.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
TIMELINE = 'canon/CAREER_TIMELINE.md'
STORY = 'canon/STORY_BIBLE.md'
SKILL = Path('C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md')
OUTPUT = Path('design/A03_A04_FINITE_EXIT_BRIDGE_2026_10_07.json')
SOURCES = (SELF, A03_E2, A04_E5, AUDIT, CP2, TIMELINE, STORY)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def norm_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def build(root=ROOT):
    e2 = load(root, A03_E2)
    e5 = load(root, A04_E5)
    audit = load(root, AUDIT)
    cp2 = load(root, CP2)
    assert e2 == college_builder.load(root, college_builder.OUTPUT)
    assert e5 == draft_builder.load(root, draft_builder.OUTPUT)
    assert not college_builder.validate(e2, root=root), 'A03 E2 source-current required'
    assert not draft_builder.validate(e5, root=root), 'A04 E5 source-current required'
    assert e2['episode_function_id'] == 'A03-EF-002' and e5['episode_function_id'] == 'A04-EF-005'
    assert audit['status'] == 'INDEPENDENTLY_REVIEWED_BOUNDED_EXIT_AUDIT'
    assert [(row['id'], row['result']) for row in audit['rows'] if row['id'] in ('A03-S2','A04-S2','A04-S3')] == [
        ('A03-S2','HOLD_ONE_OBSERVABLE_TEAMMATE_ASSIGNMENT'),
        ('A04-S2','BOUNDED_PASS'),('A04-S3','BOUNDED_PASS')]
    assert all(norm_sha((root / p).read_bytes()) == digest
               for p, digest in audit['source_sha256'].items()), 'prior audit must be source-current'
    subacts = {row['id']: row for row in cp2['subacts'] if row['id'] in ('A03-S2','A04-S2','A04-S3')}
    acts = {row['id']: row for row in cp2['acts'] if row['id'] in ('A03','A04')}
    assert subacts['A03-S2']['exit_state'] == '동료가 맡기는 수비 기능'
    assert subacts['A03-S2']['choice'] == '개인 리바운드 수만 좇지 않고 동료가 공을 잡도록 박스아웃과 볼 없는 준비를 반복한다'
    assert acts['A03']['exit_state'] == '대학 소속과 드래프트 평가 자료'
    assert acts['A04']['exit_state'] == 'Chicago의 계약·개발 책임'
    assert acts['A04']['choice'] == '과장된 공격 완성도 대신 성장 증거 제시'
    timeline = (root / TIMELINE).read_text(encoding='utf-8-sig')
    story = (root / STORY).read_text(encoding='utf-8-sig')
    assert '2018 NBA Draft를 통해 Chicago에 진입' in timeline
    assert '1라운드 후반에서 지명하고 NBA rookie-scale 계약을 체결한다' in timeline
    assert '정확 순번은' in timeline and 'HOLD' in timeline
    assert '1라운드 rookie-scale 계약을 맺고 NBA를 본무대로 삼는다' in story
    skill = SKILL.read_text(encoding='utf-8-sig')
    assert '## 13. ★계층형 장편 설계 파이프라인' in skill
    assert '## 22. ★파일 존재와 실행 권위를 분리한다' in skill

    return {
        'schema': 'A03_A04_FINITE_EXIT_BRIDGE_V1',
        'status': 'INDEPENDENTLY_REVIEWED_TWO_BOUNDED_ROUTINE_OBSERVATIONS',
        'independent_review_completed': True,
        'scope': 'Two already approved direction gaps; local interstitial actions, not new final functions or mandatory slots',
        'historical_audit': {'path': AUDIT, 'original_status': audit['status'],
                             'original_A03_S2_hold_preserved_as_prior_snapshot': True,
                             'original_A04_act_hold_preserved_as_prior_snapshot': True},
        'A03_teammate_assignment': {
            'source_function': {'id': e2['episode_function_id'], 'path': A03_E2,
                                'exact_full_exit': e2['exit_state']},
            'relative_order': 'AFTER_A03_E2_BEFORE_A03_E3_WITHIN_ALREADY_PERMITTED_PRACTICE',
            'actor_authority': '이미 두 번 공을 확보한 동료가 허용된 같은 연습 안에서 다음 좁은 박스아웃 역할을 요청한다. 공식 출전 분이나 코치 로테이션 권한은 갖지 않는다.',
            'request_observed': '그 동료는 다음 공 궤적에서도 가까운 상대의 길을 막아 달라는 좁은 역할을 주인공에게 직접 맡긴다. 실존 인물의 실제 발언이나 마음속 신뢰를 인증하지 않는다.',
            'choice': '주인공은 다음 공을 직접 쫓는 대신 동료가 요청한 같은 상대 박스아웃을 맡는다.',
            'direct_cost': '같은 허용 연습의 다음 공에서 개인 리바운드 추격 한 기회를 줄이고 볼 없는 위치 노동에 시간을 쓴다.',
            'observable_result': '주인공이 상대와 바스켓 사이를 다시 차지하고 동료가 공을 확보한다. 동료의 역할 요청·수락·수행이 같은 연습에서 직접 보인다.',
            'bounded_exit': '동료가 다시 맡긴 수비·박스아웃 기능을 수행한 국소 근거가 생긴다.',
            'original_cp2_exit': subacts['A03-S2']['exit_state'],
            'new_practice_or_game_date': None,
            'official_rebound_game_box_or_extra_episode': False,
            'whole_season_teammate_trust_or_starter_right': False,
        },
        'A04_institutional_responsibility': {
            'source_function': {'id': e5['episode_function_id'], 'path': A04_E5,
                                'exact_full_exit': e5['exit_state']},
            'relative_order': 'AFTER_A04_E5_BEFORE_A05_E1_IN_EXISTING_2018_CHICAGO_ENTRY_DIRECTION',
            'actor_authority': '가상 Chicago 구단의 계약 담당은 1라운드 표준계약 가족의 선수 자리를, 개발 담당은 첫 제한 과제를 맡는다. 이름·사적 등록 영수증·정확 금액은 선택하지 않는다.',
            'institutional_action': '승인된 Chicago 1라운드 진입 방향 안에서 구단과 주인공은 가상 세계의 계약 필수항목을 채운 rookie-scale 표준계약을 체결한다. 이 설계 문서는 정확 순번·급여를 미기재 상태로 보존하며 빈 서류 자체를 유효 계약으로 취급하지 않는다. 구단은 그를 표준계약 선수로 책임지며 수비 위치·리바운드·단순 연결의 초기 개발 과제를 전달한다.',
            'choice': '주인공은 서류와 역할 과제를 받아 즉시 주전·공격 완성을 요구하기보다 그 제한 개발 책임을 수락한다.',
            'direct_cost': '구단은 표준계약 명단 자리와 개발 지도의 책임을 맡고, 주인공은 다음 허용 준비 시간을 혼자 공격 표본을 늘리는 대신 전달받은 수비·리바운드 과제에 쓴다.',
            'observable_result': '계약 담당의 가상 체결·표준계약 선수 인수와 개발 담당의 첫 과제 전달이 안내를 넘어 직접 보인다. 주인공이 그 과제를 받아 준비를 시작한다.',
            'bounded_exit': 'Chicago가 1라운드 표준계약과 초기 개발 책임을 가상 이야기 안에서 맡고 주인공이 제한 역할을 수락했다.',
            'original_cp2_act_exit': acts['A04']['exit_state'],
            'fictional_contract_family_selected_within_approved_direction': True,
            'exact_2018_pick_or_salary_selected': False,
            'actual_private_UPC_or_league_receipt_certified': False,
            'medical_clearance_or_starter_minutes_certified': False,
            'additional_standard_roster_player_displaced': False,
            'existing_late_first_round_donor_direction_preserved_exact_draft_and_full_roster_unselected': True,
        },
        'audit_promotion': {'A03_S2_bounded_exit_pass': True,
                            'A03_Act_bounded_exit_pass': True,
                            'A04_Act_bounded_exit_pass': True,
                            'reason': 'Root independently read E2/E5, CP2, current prior audit and timeline/story authority. A03 visible reassignment and A04 already approved fictional rookie-scale responsibility are accepted; individual rebound-count and exact Hutchison-slot ambiguities repaired. Whole historical/league execution remains outside this bounded exit.'},
        'new_final_episode_functions': 0, 'new_planned_slots': 0,
        'exact_existing_E3_E5_or_A05_entry_rewritten': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'new_author_lock': False,
        'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        'source_hash_method': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_sha256': {p: norm_sha((root / p).read_bytes()) for p in SOURCES},
        'writing_skill_sha256': norm_sha(SKILL.read_bytes()),
    }


def render(data):
    a = data['A03_teammate_assignment']
    b = data['A04_institutional_responsibility']
    return '\n'.join([
        '# A03·A04 남은 한정 출구의 운영 다리', '',
        '**상태:** 두 한정 운영 관측의 독립 검문 완료. 기존 A03·A04 감사의 HOLD는 이전 시점 이력으로 보존하고 새 최종 기능·계획 슬롯·원고를 만들지 않는다.', '',
        '## A03 동료의 다음 수비 요청', '',
        f"- 위치: {a['relative_order']}", f"- 정확 이전 출구: {a['source_function']['exact_full_exit']}",
        f"- 직접 요청: {a['request_observed']}", f"- 선택: {a['choice']}",
        f"- 비용: {a['direct_cost']}", f"- 관측: {a['observable_result']}",
        '- 동료는 실전 로테이션 권한자가 아니며 실제 발언·시즌 전체 신뢰·공식 리바운드 수를 인증하지 않는다.', '',
        '## A04 Chicago의 계약·개발 책임', '',
        f"- 위치: {b['relative_order']}", f"- 정확 이전 출구: {b['source_function']['exact_full_exit']}",
        f"- 기관 행동: {b['institutional_action']}", f"- 선수 선택: {b['choice']}",
        f"- 직접 비용: {b['direct_cost']}", f"- 관측: {b['observable_result']}",
        '- 가상 1라운드 표준계약 가족만 구현한다. 정확 지명 순번·급여·실제 사적 UPC·의료·주전 분은 인증하지 않는다.', '',
        '두 다리는 기존 정확 기능 출구를 소급 변경하지 않는다. A03-S2·A03 Act·A04 Act의 남은 한정 관측을 별도 재판정해 수용했다. 전체 G13/G14·실제 Pack·원고는 미완료이고 게이트는 `CLOSED`다.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['finite exit bridge differs from source-bound build']


def self_test(data):
    cases = [
        ('teammate assigns starter minutes', lambda x: x['A03_teammate_assignment'].update(whole_season_teammate_trust_or_starter_right=True)),
        ('exact pick chosen', lambda x: x['A04_institutional_responsibility'].update(exact_2018_pick_or_salary_selected=True)),
        ('actual UPC certified', lambda x: x['A04_institutional_responsibility'].update(actual_private_UPC_or_league_receipt_certified=True)),
        ('erase reviewed bounded audit', lambda x: x['audit_promotion'].update(A04_Act_bounded_exit_pass=False)),
    ]
    for name, mutate in cases:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_load = load
    for name, path, mutate in [
        ('A03 source loses two rebounds', A03_E2, lambda x: x.update(exit_state='동료는 아무 공도 잡지 못했고 박스아웃을 하지 않았다')),
        ('A04 source guarantees exact pick', A04_E5, lambda x: x.update(exit_state='실제 Chicago 22순위·의료·주전을 확정했다')),
        ('CP2 A04 contract exit reversed', CP2, lambda x: next(row for row in x['acts'] if row['id'] == 'A04').update(exit_state='Atlanta 투웨이 계약만 남음')),
    ]:
        def altered(root, requested, path=path, mutate=mutate):
            value = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                value = copy.deepcopy(value)
                mutate(value)
            return value
        with patch(__name__ + '.load', side_effect=altered):
            assert validate(data), name
    return len(cases) + 3


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
    print(json.dumps({'current': not errors, 'errors': errors,
                      'negative_controls': tested, 'status': data['status']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
