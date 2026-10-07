"""Build four finite A05 local functions from the reviewed 2018–20 route."""

import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_a04_e5_final_episode_function as previous_builder
import build_a05_early_nba_operating_batch as working_builder


ROOT = Path(__file__).resolve().parents[1]
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
WORKING = str(working_builder.OUTPUT).replace('\\', '/')
CANDIDATES = 'design/A05_EARLY_NBA_CONDITIONAL_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
SELF = 'tools/build_a05_final_function_batch.py'
OUTPUTS = tuple(Path(f'design/A05_E{i}_FINAL_EPISODE_FUNCTION.json') for i in range(1, 5))
SOURCE_PATHS = (SELF, PREVIOUS, WORKING, CANDIDATES, CP2)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def normalized_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def serialized(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'


FUNCTIONS = (
    {
        'single_function': 'NBA 속도에서 맡은 좁은 수비·리바운드·전환 과제를 자기 공격보다 먼저 시험한다',
        'exit_state': 'Chicago 루키로서 주인공은 기존 역할 기회에서 자기 공격을 먼저 늘리기보다 맡은 수비 복귀·리바운드 위치·단순 연결을 택했다. NBA 속도의 다음 이동에 한 걸음 늦어 동료가 측면 통로를 메운 것을 직접 봤고, 그 위치 오차를 다음 준비 과제로 남겼다. 이 국소 관측은 개별 경기·득점·출전 분이나 팀 전체 평가를 새로 확정하지 않는다.',
        'reader_question': '농구 역할의 한계를 본 다음에도 자기 준비 시간을 지킬 수 있을까',
        'next_id': 'A05-CF02',
    },
    {
        'single_function': '밤샘 게임으로 잃은 예정 기회를 되돌리지 못한 채 다음 준비의 순서를 직접 바꾼다',
        'exit_state': '주인공은 밤샘 게임 뒤 수면을 미루고 영상·컨디셔닝 체크인에 늦어 이미 예정된 NBA 로테이션 시험 기회 한 번을 잃었다. 자기 준비 실패를 짧게 설명하고 다음 의무의 수면·영상·컨디셔닝 순서를 스스로 맞춰 보았지만, 지나간 기회는 돌아오지 않았다. 게임을 없애거나 자기관리 문제가 완치된 것도 아니다.',
        'reader_question': '생활 준비의 다음 시도와 별도로 부족한 농구 판단을 어디에서 반복할 것인가',
        'next_id': 'A05-CF04',
    },
    {
        'single_function': '징계와 분리된 Windy City 개발 과제를 반복하고 조건부 NBA 복귀 역할에서 다시 시험한다',
        'exit_state': '주인공은 Chicago NBA 계약 신분을 유지한 별도 Windy City 개발창에서 스크린 뒤 수비 위치와 세컨드사이드 판단의 지연을 허용된 영상과 직접 시도로 대조했다. 이후 기존 루키 역할선 안에서 별도 복귀 기회가 마련되는 가상 운영 조건에서 같은 수비 복귀·리바운드·단순 연결을 다시 시도했고, NBA 속도에서의 위치 오차는 여전히 다음 준비 과제로 남았다. 배정은 앞선 지각의 징계가 아니고, 정확 배정·복귀일과 G League·NBA 개인 박스 및 새 선발 권리는 확정하지 않았다.',
        'reader_question': '다음 연차에 상대가 약한 손을 열어 두면 그는 공을 어디까지 운반할 수 있을까',
        'next_id': 'A05-CF07',
    },
    {
        'single_function': '2019–20 약한 손 첫 벽에서 조기 이양을 두 번 관측하고 같은 좁은 과제를 다시 맡는다',
        'exit_state': '2019–20 주인공은 익숙한 손의 공격을 고집하다 약한 손 쪽 첫 벽에서 다음 전진이 막히는 지점을 직접 겪었다. 이후 허용된 비교 가능한 두 번의 역할 반복에서 약한 손으로 짧게 직선 운반하다 첫 벽 앞에서 Coby 또는 Satoransky에게 일찍 공을 넘겼고, 받는 가드가 두 번 모두 공을 확보하는 것을 직접 봤다. 다음 허용 역할 창에도 같은 한정 운반·조기 이양 과제가 전달되어 그 선택을 다시 맡는다. 이 좁은 반복 근거는 직선 전진과 다음 패스의 제한적 신뢰에만 해당하며, 슛·득점·실전 점유 결과, 두 번째 도움수비 해결, 전체 로테이션 신뢰, 주공격 창조자·1차 PG 권한을 인증하지 않는다.',
        'reader_question': 'LaMelo가 합류한 뒤 더 좁아진 공격 시작권에서 공 없는 다음 위치를 만들 수 있을까',
        'next_id': 'A06-S1',
    },
)


def build(root=ROOT):
    previous = load(root, PREVIOUS)
    selected = load(root, WORKING)
    candidates = load(root, CANDIDATES)
    cp2 = load(root, CP2)
    assert previous == working_builder.load(root, working_builder.PREVIOUS), 'E5 differs from A05 validation input'
    assert not working_builder.validate(selected, root=root), 'A05 route must be source-current'
    assert selected['status'] == 'SELECTED_ROUTINE_FOUR_FUNCTIONAL_GROUPS_INDEPENDENTLY_REVIEWED'
    assert selected['independent_review_completed'] is True
    assert selected['R4_extension_independent_review_completed'] is True
    assert selected['previous_exact_A04_E5_exit'] == previous['exit_state']
    assert [row['id'] for row in selected['route_groups']] == ['R1','R2','R3','R4']
    assert [row['season_scope'] for row in selected['route_groups']] == ['2018-19']*3+['2019-20']
    assert candidates['status'] == 'EIGHT_CONDITIONAL_EARLY_NBA_CAUSAL_FUNCTIONS_NOT_FINAL_G13'
    assert candidates['allocation']['total_slots'] == 92
    assert candidates['allocation']['episode_function_assignment'] is None
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    assert previous['episode_function_id'] == 'A04-EF-005'
    assert previous['next_unit']['id'] == 'A05-S1'
    assert previous['whole_g13_complete'] is False
    assert selected['direct_causal_boundaries']['one_missed_rotation_opportunity_only'] is True
    assert selected['direct_causal_boundaries']['missed_opportunity_restored_by_later_intent'] is False
    assert selected['direct_causal_boundaries']['Windy_City_development_separate_from_discipline'] is True
    assert selected['direct_causal_boundaries']['NBA_contract_and_roster_rights_survive_assignment'] is True
    assert selected['direct_causal_boundaries']['conditional_NBA_return_not_earned_automatically'] is True
    assert selected['direct_causal_boundaries']['2019_20_weak_hand_work_not_2018_19_rookie_payoff'] is True
    assert selected['historical_and_authority_limits']['new_NBA_or_G_League_game_created'] is False
    assert selected['promotion_limits']['new_final_episode_functions'] == 0
    assert selected['promotion_limits']['manuscript_allowed'] is False
    assert len(FUNCTIONS) == len(selected['route_groups']) == len(OUTPUTS)

    shared_sources = {path: normalized_sha((root / path).read_bytes()) for path in SOURCE_PATHS}
    built = []
    for index, (route, spec) in enumerate(zip(selected['route_groups'], FUNCTIONS), 1):
        assert route['source_ids'] == ([f'A05-CF01'] if index == 1 else
                                       ['A05-CF02','A05-CF03'] if index == 2 else
                                       ['A05-CF04','A05-CF05','A05-CF06'] if index == 3 else
                                       ['A05-CF07','A05-CF08'])
        assert route['bounded_exit'] == candidates['functions'][int(route['source_ids'][-1][-2:])-1]['changed_state']
        if index == 3:
            assert route['new_assignment_or_return_date_certified'] is False
            assert route['development_guarantees_NBA_return_or_success'] is False
            assert route['NBA_contract_status_preserved'] is True
        if index == 4:
            assert route['grab_and_go_short_roll_matured_early'] is False
            assert route['Coby_Satoransky_existing_guard_roles_preserved'] is True
            assert route['limited_trust_operating_witness'] == {
                'comparable_first_wall_handoffs_observed': 2,
                'receiving_guard_secures_ball_each_time': True,
                'next_narrow_task_reassigned_in_fictional_role_window': True,
                'official_game_or_private_receipt_certified': False,
                'made_shot_or_second_help_solution_certified': False,
                'whole_rotation_trust_certified': False,
            }
        prior = previous if index == 1 else built[-1]
        prior_path = PREVIOUS if index == 1 else str(OUTPUTS[index-2]).replace('\\', '/')
        beats = [{
            'id': f'{route["id"]}-{n}',
            'classification': 'SELECTED_BOUNDED_FICTIONAL_ACTION_WITH_SOURCE_SCOPE',
            'action': action,
            'source_path': WORKING,
        } for n, action in enumerate(route['observable_actions'], 1)]
        if index == 3:
            beats[-1]['separate_NBA_return_operating_condition'] = (
                'SELECTED_FICTIONAL_CONDITION_WITHIN_EXISTING_ROOKIE_ROLE_LINE; '
                'NO_EXACT_DATE_PRIVATE_CONSENT_OR_NEW_MINUTES_CERTIFIED'
            )
        blueprint = {
            'schema': f'A05_R{index}_LOCAL_BLUEPRINT_V1',
            'status': 'ACTUAL_VERIFIED',
            'authority_scope': 'SOURCE_CURRENT_BOUNDED_FICTIONAL_FUNCTION_NOT_GAME_BOX_OR_WHOLE_ACT',
            'entry_state': prior['exit_state'],
            'single_function': spec['single_function'],
            'unit_choice': [candidates['functions'][int(x[-2:])-1]['choice'] for x in route['source_ids']],
            'direct_present_cost': route['cost'],
            'exit_state': spec['exit_state'],
            'beats': copy.deepcopy(beats),
        }
        path_hashes = dict(shared_sources)
        if index > 1:
            path_hashes[prior_path] = normalized_sha(serialized(prior).encode('utf-8'))
        data = {
            'schema': f'A05_E{index}_FINAL_EPISODE_FUNCTION_V1',
            'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
            'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_WHOLE_A05_OR_CANONICAL_GAME_BOX',
            'episode_function_id': f'A05-EF-{index:03}',
            'act': 'A05', 'primary_subact': route['subact'],
            'source_conditional_functions': route['source_ids'],
            'final_function_order': 27 + index,
            'planned_allocation_slot': 156 + index,
            'published_episode_number': None, 'published_episode_title': None,
            'manuscript_word_count': None,
            'slot_accounting': {
                'a05_planned_slots': 92, 'a05_locally_assigned_function_slots_through_this': index,
                'a05_unassigned_planned_slots': 92-index,
                'total_local_functions_through_this': 27+index,
                'unassigned_plan_slots_are_not_mandatory_new_events': True,
                'allocation_is_final_published_episode_count': False,
                'A05_subact_slot_distribution_certified': False,
            },
            'final_episode_functions_completed_this_record': 1,
            'previous_function': {'id': prior['episode_function_id'], 'source_path': prior_path,
                                  'exact_full_exit': prior['exit_state']},
            'local_blueprint': blueprint,
            'single_function': blueprint['single_function'],
            'entry_state': blueprint['entry_state'],
            'unit_choice': blueprint['unit_choice'],
            'exit_state': blueprint['exit_state'],
            'direct_present_cost': blueprint['direct_present_cost'],
            'reader_question_at_end': spec['reader_question'],
            'internal_order': [beat['id'] for beat in beats], 'beats': beats,
            'next_unit': {'id': spec['next_id'], 'status': 'NEXT_FUNCTION_NOT_EXECUTED_HERE',
                          'future_outcome_prepaid': False},
            'source_candidate_bounded_exit': route['bounded_exit'],
            'route_group_id': route['id'],
            'season_scope': route['season_scope'],
            'limited_trust_operating_witness': (copy.deepcopy(route['limited_trust_operating_witness'])
                                                if index == 4 else None),
            'historical_limits': {
                'existing_rookie_role_line_reference': selected['historical_and_authority_limits']['existing_rookie_role_line_reference'],
                'new_game_date_opponent_score_player_minutes_selected': False,
                'new_G_League_box_or_starter_selected': False,
                'Hutchison_injury_transferred': False,
                'real_staff_quote_or_private_thought': None,
                '2020_21_advanced_offense_prepaid': False,
            },
            'conditional_NBA_return': {
                'applies_to_this_function': index == 3,
                'selected_fictional_operating_condition_within_existing_rookie_role_line': index == 3,
                'actual_private_return_receipt_or_exact_date_certified': False,
                'development_guarantees_NBA_return_or_success': False,
            },
            'direct_causal_limits': {
                'one_missed_rotation_opportunity_only': True,
                'lost_try_restored_by_later_intent': False,
                'Windy_City_assignment_is_discipline': False,
                'NBA_contract_and_roster_rights_preserved': True,
                'weak_hand_task_belongs_to_2019_20': True,
                'second_help_solved': False,
            },
            'whole_A05_subact_or_Act_exit_certified': False,
            'whole_g13_complete': False, 'whole_g14_complete': False,
            'actual_context_packs': 0, 'g15_complete': False, 'g16_complete': False,
            'g17_complete': False, 'author_locked': False, 'new_author_decisions': 0,
            'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
            'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
            'source_rev_sha256': path_hashes,
        }
        built.append(data)
    assert [x['final_function_order'] for x in built] == [28,29,30,31]
    assert [x['planned_allocation_slot'] for x in built] == [157,158,159,160]
    assert all(built[i]['entry_state'] == built[i-1]['exit_state'] for i in (1,2,3))
    return built


def render(data):
    lines = [
        f"# A05 기능 {data['episode_function_id']} — {data['single_function']}", '',
        '**범위:** 원고가 아닌 한정 기능표 1건. 현재 출처와 가상 행동의 정합성만 `ACTUAL_VERIFIED`로 검문한다.', '',
        f"- 전역 기능 {data['final_function_order']}, A05 계획 슬롯 {data['planned_allocation_slot']} (출판 번호 아님)",
        f"- 정확 진입: {data['entry_state']}",
        f"- 선택: {' / '.join(data['unit_choice'])}",
        f"- 직접 비용: {' / '.join(data['direct_present_cost']) if isinstance(data['direct_present_cost'],list) else data['direct_present_cost']}", '',
        '| 행동 | 근거 범위 |', '| --- | --- |',
    ]
    for beat in data['beats']:
        lines.append(f"| {beat['action']} | {beat['classification']} |")
    lines += [
        '', f"- 정확 출구: {data['exit_state']}",
        f"- 다음 독자 질문: {data['reader_question_at_end']}",
        '- 날짜·상대·개인 득점·분·승패·실존 코치 사적 발언은 새로 확정하지 않는다. R3의 복귀는 기존 루키 역할선 안의 **별도 가상 운영 조건**이며 개발 반복의 자동 보상이 아니다.',
        '- 전체 A05-S1/S2/S3·Act·G13/G14·실제 Pack·원고는 미완료이고 설계/원고 게이트 `CLOSED`다.', '',
    ]
    return '\n'.join(lines)


def validate_all(records, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if records == expected else ['A05 final function batch differs from source-bound route']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    records = build()
    if args.write:
        for path, record in zip(OUTPUTS, records):
            (ROOT / path).write_text(serialized(record), encoding='utf-8')
            (ROOT / path.with_suffix('.md')).write_text(render(record), encoding='utf-8')
    errors = validate_all(records)
    if args.check:
        saved = [load(ROOT, path) for path in OUTPUTS]
        errors += validate_all(saved)
        for path, record in zip(OUTPUTS, saved):
            if (ROOT / path.with_suffix('.md')).read_text(encoding='utf-8-sig') != render(record):
                errors.append(f'Markdown not synchronized: {path}')
    print(json.dumps({'current': not errors, 'errors': errors,
                      'functions': [x['episode_function_id'] for x in records],
                      'orders': [x['final_function_order'] for x in records],
                      'slots': [x['planned_allocation_slot'] for x in records]}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
