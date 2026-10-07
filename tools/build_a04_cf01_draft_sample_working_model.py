"""Select a bounded draft sample-preparation action without certifying a scout result."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a03_e3_final_episode_function as previous_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A04_CF01_DRAFT_SAMPLE_WORKING_MODEL_2026_10_07.json')
MARKDOWN = OUTPUT.with_suffix('.md')
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
BRIDGE = 'design/A03_POST_TOURNAMENT_HISTORY_BRIDGE_2026_10_07.json'
CANDIDATES = 'design/A04_DRAFT_CONDITIONAL_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
TIMELINE = 'canon/CAREER_TIMELINE.md'
STORY = 'canon/STORY_BIBLE.md'
TALENT = 'canon/TALENT_BQ_MODEL.md'
PICK22 = 'research/CHICAGO_2018_PICK22_PLAUSIBILITY.md'
ACT_MAP = 'design/ACT_MAP.md'
SOURCES = ('tools/build_a04_cf01_draft_sample_working_model.py', PREVIOUS, BRIDGE,
           CANDIDATES, CP2, TIMELINE, STORY, TALENT, PICK22, ACT_MAP)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def normalized_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def source_bytes(root, path):
    return (root / path).read_bytes()


def validate_bridge(root, previous, bridge):
    assert bridge['schema'] == 'A03_POST_TOURNAMENT_HISTORY_BRIDGE_V1'
    assert bridge['previous_function']['id'] == previous['episode_function_id'] == 'A03-EF-003'
    assert bridge['previous_function']['exact_full_exit'] == previous['exit_state']
    for path, expected in bridge['source_sha256'].items():
        assert normalized_sha(source_bytes(root, path)) == expected, 'post-tournament source SHA changed: ' + path
    for item in bridge['official_sources']:
        raw = Path(item['temporary_cache']).read_bytes()
        assert len(raw) == item['raw_bytes']
        assert hashlib.sha256(raw).hexdigest() == item['raw_sha256']
        assert item['http_status'] == 200
    events = bridge['official_public_sequence']
    assert [(e['date'], e['historical_score']) for e in events] == [
        ('2018-03-25', '71-59'), ('2018-03-31', '95-79'), ('2018-04-02', '79-62')]
    assert events[0]['title_won_on_this_date'] is False
    assert events[2]['official_final_four_mop'] == 'Donte DiVincenzo'
    assert bridge['bounded_handoff_proposal']['A04_source_next'] == 'A04-S1'
    assert bridge['bounded_handoff_proposal']['full_A03_S3_or_act_exit_now_certified'] is False
    assert bridge['bounded_handoff_proposal']['actual_alternate_final_four_200_minute_vectors_certified'] is False
    assert bridge['limits']['alternate_Kansas_or_Michigan_win_mechanically_reproved'] is False


def build(root=ROOT):
    previous = load(root, PREVIOUS)
    bridge = load(root, BRIDGE)
    candidates = load(root, CANDIDATES)
    cp2 = load(root, CP2)
    assert previous == previous_builder.load(root, previous_builder.OUTPUT)
    assert not previous_builder.validate(previous, root=root), 'A03 E3 must be source-current'
    validate_bridge(root, previous, bridge)
    assert candidates['status'] == 'SIX_CONDITIONAL_DRAFT_CAUSAL_FUNCTIONS_NOT_FINAL_G13'
    assert candidates['final_episode_functions'] == 0
    cf = candidates['functions'][0]
    expected = {
        'id': 'A04-CF01', 'subact': 'A04-S1',
        'dominant_function': '프로 평가에 내놓을 표본 선택',
        'cause': 'Texas Tech의 팀 기여를 남겼지만 낮은 사용률과 자가 창조 질문은 남는다',
        'entry_state': '우승팀 기여와 NBA 공격 능력 증명을 분리',
        'pressure': '우승과 운동능력만 강조하면 현재 공격 표본의 부족을 숨기는 소개가 된다',
        'choice': '자신이 수행한 수비·리바운드·연결 표본과 아직 보여 줄 공격 과제를 나누어 평가 준비에 담는다',
        'direct_cost': '우승팀 경력과 보기 좋은 장면만으로 자신을 포장할 기회를 줄이고 부족한 부분을 드러낸다',
        'changed_state': '보여 줄 역할 증거와 새 평가에서 시험할 기술 과제가 구분된다',
        'next': 'A04-CF02',
        'next_dependency': '역할 영상과 별개로 신체 측정을 받을 준비가 필요하다',
    }
    assert {key: cf[key] for key in expected} == expected
    assert cf['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf['selected_event'] is False and cf['author_locked'] is False
    assert all(cf[key] is None for key in ('draft_pick', 'combine_invitation', 'measurement_results',
                                          'medical_test_results', 'workout_or_measurement_date',
                                          'agent_name', 'coach_or_front_office_private_thoughts'))
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    s1 = next(row for row in cp2['subacts'] if row['id'] == 'A04-S1')
    assert s1['entry_state'] == '신체 측정만으로 순번을 확신'
    assert s1['choice'] == '신체 측정으로 순번을 단정하지 않고 준비한 기술의 가능한 범위와 한계를 평가에 내놓는다'
    assert s1['cost'] == '불확실한 평가 수용'
    assert s1['exit_state'] == '보여줄 기술 표본 명확화'
    assert s1['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    timeline = source_bytes(root, TIMELINE).decode('utf-8-sig')
    story = source_bytes(root, STORY).decode('utf-8-sig')
    talent = source_bytes(root, TALENT).decode('utf-8-sig')
    pick = source_bytes(root, PICK22).decode('utf-8-sig')
    act = source_bytes(root, ACT_MAP).decode('utf-8-sig')
    assert '실제 22순위는 최우선 후보지만 정확 순번은 HOLD' in timeline
    assert '토너먼트 핵심 공로와 Final Four MOP를 주인공에게 이전하지 않는다' in timeline
    assert '리바운드→직접 운반/전진 패스→림 압박이 고유 공격의 시작' in story
    assert '풀업과 1대1 자가 창조는 라이벌과 프랜차이즈 득점원의 최상위 수준에 도달하지 않는다' in talent
    assert '25~40순위권의 고위험 원석' in pick and 'CONDITIONAL_PASS / EXACT_PICK_HOLD' in pick
    assert '공을 오래 잡지 않는 원패스 연결' in pick and '코너 3점과 원드리블 공격의 최소 발전성' in pick
    assert '| A04 | 2018 Draft | 시장의 선택 | 12 |' in act

    actions = [
        {'id': 'D1', 'type': 'SELECTED_FICTIONAL_PRIVATE_PREPARATION',
         'action': 'He records his own bounded switch/boxout contribution and the teammate securing the ball in one column of an evaluation card; self-created offense is separately labeled unproved.',
         'observable_result': 'His card visibly separates the narrow role contribution from the unproved offensive task. Team membership supplies the title context; DiVincenzo’s Final Four MOP is not claimed as his own achievement.',
         'actual_Texas_Tech_PBP_clip_or_official_personal_stat_certified': False},
        {'id': 'D2', 'type': 'SELECTED_BOUNDED_FICTIONAL_SKILL_REHEARSAL',
         'action': 'In an allowed private practice block, he rehearses a corner catch into one dribble toward the rim and records the attempt together with the point where the next self-created move stalls.',
         'observable_result': 'He can show an attempted one-dribble attack and its visible stopping point, not a proven make, live-defender win, elbow counter, advanced live pass or NBA translation.',
         'official_combine_or_team_workout': False,
         'shot_make_or_live_defender_success_assigned': False,
         'private_scout_or_medical_feedback_claimed': False},
        {'id': 'D3', 'type': 'DIRECT_COST_AND_LIMITED_PREPARATION_RESULT',
         'choice': cf['choice'],
         'direct_present_cost': 'He uses this available review/practice block to keep a visible failed offensive limit beside the narrow role sample instead of presenting only title credentials and athletic highlights.',
         'observable_result': 'His own preparation now identifies a bounded defensive/rebound role claim and one offensive task still to test; no outside evaluator has accepted them or assigned a draft grade.',
         'draft_order_or_contract_selected': False},
    ]
    result = (
        '주인공은 Texas Tech전의 좁은 수비·박스아웃 기여와 우승팀 소속 사실을 자기 공격 완성의 증명으로 합치지 않았다. '
        '그는 허용된 개인 준비에서 코너 캐치 뒤 한 드리블 공격을 시도하고 다음 자가 창조가 막히는 지점을 함께 기록해, '
        '평가에 제시할 역할 증거와 아직 시험받아야 할 공격 과제를 분리했다. 구단의 비공개 판단·공식 측정·정확 순번은 여전히 미확인이다.'
    )
    return {
        'schema': 'A04_CF01_DRAFT_SAMPLE_WORKING_MODEL_V1',
        'status': 'SELECTED_ROUTINE_DRAFT_SAMPLE_PREPARATION_INDEPENDENTLY_REVIEWED',
        'independent_review_completed': True,
        'scope': 'ONE_PRIVATE_FICTIONAL_PREPARATION_BLOCK_NOT_COMBINE_SCOUT_WORKOUT_OR_PICK',
        'previous_exact_full_exit': previous['exit_state'],
        'public_history_bridge_path': BRIDGE,
        'public_history_after_events_only': True,
        'cp2_provisional_entry': s1['entry_state'],
        'cp2_provisional_entry_inherited_as_observed_belief': False,
        'operating_entry': 'Texas Tech 국소 역할 선택과 이후 공개된 Villanova 우승은 있지만, 자기 공격 표본과 프로 평가 결과는 미검증이다.',
        'source_function_id': 'A04-CF01',
        'source_candidate_entry_used_as_certified_actual_state': False,
        'one_function': '수비·리바운드 역할 증거와 개인 공격의 미검증 과제를 한 준비자료에서 구분한다',
        'actions': actions,
        'direct_present_cost': actions[2]['direct_present_cost'],
        'selected_design_exit_state': result,
        'next_candidate': {'id': 'A04-CF02', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'official_combine_invitation_measurement_or_pick_prepaid': False},
        'information_access': {
            'pov': 'PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'may_know': ['자기가 기록한 가상 국소 역할과 개인 준비의 실패 지점', '공개된 Villanova 우승 결과와 기존 실제 선수 공로'],
            'cannot_know': ['Chicago 또는 타 구단의 비공개 보드', '공식 Combine 초청·측정·의료 결과', '실존 스카우트 내면·실제 발언', '정확 2018 지명 순번과 계약'],
            'scout_dialogue': None, 'agent_name_or_contract': None,
        },
        'limits': {
            'official_combine_invitation_or_measurement_certified': False,
            'real_team_workout_or_real_scout_feedback_certified': False,
            'exact_pick_22_author_locked_or_selected': False,
            'medical_clearance_or_agent_contract_certified': False,
            'later_elbow_or_live_pass_counter_prepaid': False,
            'historical_box_or_title_credit_reassigned_to_protagonist': False,
            'new_2018_game_or_NCAA_record_added': False,
            'first_A04_final_episode_function_completed': False,
            'whole_A04_S1_or_Act_exit_certified': False,
            'whole_g13_complete': False, 'whole_g14_complete': False,
            'actual_context_packs': 0, 'author_locked': False,
            'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {path: normalized_sha(source_bytes(root, path)) for path in SOURCES},
    }


def render(data):
    lines = [
        '# A04 보드 질문: 역할 증거와 공격 과제 분리', '',
        '**범위:** 우승 이후 개인 준비의 가상 작업안. 실제 Combine 초청·팀 워크아웃·측정·의료·구단보드·지명 결정은 아니다.', '',
        f"- 정확 직전 출구: {data['previous_exact_full_exit']}",
        '- 공개 역사 인계: 3월 31일 Kansas전, 4월 2일 Michigan전 결과는 해당 경기 뒤 공개 가능한 역사 사실이다. 주인공의 대체 결승 공로나 비공개 스카우트 판단은 아니다.',
        f"- 원 CP2 잠정 진입 문구: {data['cp2_provisional_entry']} — 현행 선택 진입 사실로 상속하지 않는다.",
        f"- 현행 작업 진입: {data['operating_entry']}",
        f"- 단일 기능: {data['one_function']}", '',
        '| 단계 | 선택·행동 | 직접 결과·한계 |', '| --- | --- | --- |',
    ]
    for step in data['actions']:
        lines.append(f"| {step['id']} | {step.get('choice', step.get('action'))} | {step['observable_result']} |")
    lines += [
        '', f"- 직접 비용: {data['direct_present_cost']}",
        f"- 국소 출구: {data['selected_design_exit_state']}",
        '- 코너 캐치·한 드리블은 이미 검토된 2018 후보 기술 범위의 개인 시도다. 성공한 슛·실전 수비수 상대 승리·후년 엘보/라이브 패스·공식 평가 성적을 선지급하지 않는다.',
        '- Chicago 방향은 기존 승인 범위지만 정확 22순위, 측정 후보치, 팀 보드, Hutchison 재배치, 계약 세부는 현행 HOLD다.',
        '- CF02·A04 첫 최종 기능·A04 전체·G13/G14·실제 Pack·원고는 미완료, 게이트 `CLOSED`.', '',
    ]
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A04 sample-preparation model differs from source-bound selection']


def self_test(data, root=ROOT):
    cases = [
        ('provisional certainty inherited', lambda x: x.update(cp2_provisional_entry_inherited_as_observed_belief=True)),
        ('prepay official Combine', lambda x: x['limits'].update(official_combine_invitation_or_measurement_certified=True)),
        ('prepay exact pick', lambda x: x['limits'].update(exact_pick_22_author_locked_or_selected=True)),
        ('prepay later elbow', lambda x: x['limits'].update(later_elbow_or_live_pass_counter_prepaid=True)),
        ('claim actual workout', lambda x: x['actions'][1].update(official_combine_or_team_workout=True)),
        ('hide offensive failure', lambda x: x['actions'][1].update(observable_result='프로 선발 공격을 완벽히 증명했다')),
    ]
    for name, mutate in cases:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed, root), name
    original_load = load
    for name, path, mutate in [
        ('E3 title and NBA offense inserted', PREVIOUS,
         lambda x: x.update(exit_state='결승 MVP와 완성된 NBA 공격 능력을 이미 얻었다')),
        ('A04 same-ID CF01 choice reversed', CANDIDATES,
         lambda x: x['functions'][0].update(choice='우승만 보여주고 공격 약점은 감춘다')),
        ('CP2 cost replaced with exact pick', CP2,
         lambda x: next(row for row in x['subacts'] if row['id'] == 'A04-S1').update(cost='Chicago 22순위 지명 확정')),
        ('public bridge alternate final result certified', BRIDGE,
         lambda x: x['limits'].update(alternate_Kansas_or_Michigan_win_mechanically_reproved=True)),
    ]:
        def altered(root, requested, path=path, mutate=mutate):
            src = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                src = copy.deepcopy(src)
                mutate(src)
            return src
        with patch(__name__ + '.load', side_effect=altered):
            assert validate(data, root), name
    return len(cases) + 4


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MARKDOWN).write_text(render(data), encoding='utf-8')
    errors = validate(data)
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors += validate(saved)
        if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'current': not errors, 'errors': errors, 'negative_controls': tested,
                      'status': data['status']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
