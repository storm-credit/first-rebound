"""Build a finite A05 operating route from the eight existing causal candidates."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a04_e5_final_episode_function as previous_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A05_EARLY_NBA_OPERATING_BATCH_2026_10_07.json')
MARKDOWN = OUTPUT.with_suffix('.md')
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
CANDIDATES = 'design/A05_EARLY_NBA_CONDITIONAL_FUNCTIONS.json'
A04_CANDIDATES = 'design/A04_DRAFT_CONDITIONAL_FUNCTIONS.json'
TIMELINE = 'canon/CAREER_TIMELINE.md'
RESPONSIBILITY = 'canon/CHARACTER_RESPONSIBILITY_ARC.md'
TALENT = 'canon/TALENT_BQ_MODEL.md'
DONOR = 'simulation/CHICAGO_2018_19_PLAYER_GAME_DONOR_VECTOR.md'
SOPHOMORE = 'research/CHICAGO_2019_20_ROSTER_MINUTE_BASELINE.md'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
SKILL = Path('C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md')
SOURCES = ('tools/build_a05_early_nba_operating_batch.py', PREVIOUS, CANDIDATES,
           A04_CANDIDATES, TIMELINE, RESPONSIBILITY, TALENT, DONOR, SOPHOMORE, CP2)
EXPECTED = {
    'A05-CF01': {
        'choice': '수비·리바운드·전환의 맡은 과제를 NBA 속도에서 수행하려 한다',
        'direct_cost': '자기 공격 표본을 먼저 늘릴 기회보다 제한 역할의 준비와 수행에 시간을 쓴다',
        'changed_state': '맡은 역할을 시도하며 NBA 속도에서 수정해야 할 수행 문제를 마주한다',
        'next': 'A05-CF02',
    },
    'A05-CF02': {
        'choice': '밤샘 게임을 이어 가며 수면을 밀어 다음 영상·컨디셔닝 일정에 늦는다',
        'direct_cost': '이미 예정된 NBA 로테이션 시험 기회를 한 차례 놓친다',
        'changed_state': '놓친 기회와 자신의 준비 실패가 남아 다음 준비를 다시 선택해야 한다',
        'next': 'A05-CF03',
    },
    'A05-CF03': {
        'choice': '본인이 놓친 준비를 짧게 설명하고 다음 수면·영상·컨디셔닝의 순서를 직접 맞춰 본다',
        'direct_cost': '게임과 편한 휴식에 쓸 시간을 다음 준비에 쓰고 외부 핑계로 실패를 덮는 길을 줄인다',
        'changed_state': '외부 규칙만 기다리는 대신 다음 약속의 준비를 직접 조절하는 행동이 생긴다',
        'next': 'A05-CF04',
    },
    'A05-CF04': {
        'choice': 'Windy City의 별도 개발 배정 설명에서 수행할 과제를 확인하고 그 환경에서 반복할 준비를 한다',
        'direct_cost': '그 개발창에 NBA 무대에 머물며 출전 기회를 기다리는 길 대신 다른 환경 적응에 시간을 쓴다',
        'changed_state': 'NBA 계약 신분을 유지하며 별도 환경에서 맡을 개발 과제를 준비한다',
        'next': 'A05-CF05',
    },
    'A05-CF05': {
        'choice': '세컨드사이드 판단과 POA·스크린 대응을 시도하고 실패를 허용된 영상에서 대조해 다시 반복한다',
        'direct_cost': '개발 무대의 개인 득점 표본을 키울 기회와 편한 수행을 줄여 부족한 과제의 실패를 노출한다',
        'changed_state': '고쳐 볼 판단·위치 과제를 직접 경험한 반복 근거가 생긴다',
        'next': 'A05-CF06',
    },
    'A05-CF06': {
        'choice': 'NBA 복귀가 정해진 경우 맡은 수비·리바운드·연결 과제를 다시 시도하고 직접 겪는 오류를 다음 준비에 반영하려 한다',
        'direct_cost': '자기 공격 표본을 늘릴 시간을 맡은 과제의 재시험과 직접 겪은 오류를 되짚는 준비에 쓴다',
        'changed_state': '개발 반복을 NBA 역할에 다시 적용하려는 행동이 생기며 속도·공격 과제는 계속 남는다',
        'next': 'A05-CF07',
    },
    'A05-CF07': {
        'choice': '익숙한 공격을 고집하며 약한 손으로 몰리는 수행의 한계를 직접 대면한다',
        'direct_cost': '그 공격에서 원하는 전진과 마무리 기회를 얻지 못하고 현재 약점을 드러낸다',
        'changed_state': '약한 손 운반과 첫 벽 이후 선택이 필요한 문제로 구체화된다',
        'next': 'A05-CF08',
    },
    'A05-CF08': {
        'choice': '약한 손의 직선 운반·클로즈아웃 공격을 반복하고 첫 벽이 서면 Coby 또는 Satoransky에게 조기 이양하는 좁은 선택을 시험한다',
        'direct_cost': '편한 손의 즉시 보상과 오래 공을 잡아 자기 공격으로 끝낼 기회를 줄여 약한 손의 실패·반복 시간을 지불한다',
        'changed_state': '직접 전진과 조기 이양을 구분하려는 제한적 대응의 행동이 생기지만 두 번째 도움수비에는 여전히 막힐 수 있다',
        'next': 'A06-S1',
    },
}


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def norm_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def build(root=ROOT):
    previous = load(root, PREVIOUS)
    candidates = load(root, CANDIDATES)
    a04 = load(root, A04_CANDIDATES)
    cp2 = load(root, CP2)
    assert previous == previous_builder.load(root, previous_builder.OUTPUT)
    assert not previous_builder.validate(previous, root=root), 'A04 E5 must be source-current'
    assert previous['episode_function_id'] == 'A04-EF-005'
    assert previous['next_unit']['id'] == 'A05-S1'
    assert previous['whole_g13_complete'] is False
    assert previous['approved_direction_and_unselected_details']['guaranteed_Korea_roster_place_surrendered'] is False
    assert candidates['status'] == 'EIGHT_CONDITIONAL_EARLY_NBA_CAUSAL_FUNCTIONS_NOT_FINAL_G13'
    assert candidates['allocation']['total_slots'] == 92
    assert candidates['allocation']['episode_function_assignment'] is None
    assert candidates['final_episode_functions'] == 0 and candidates['actual_context_packs'] == 0
    assert candidates['manuscript_allowed'] is False and candidates['design_gate'] == 'CLOSED'
    assert candidates['entry_from']['id'] == 'A04-CF06'
    assert a04['functions'][5]['changed_state'] == candidates['entry_from']['changed_state']
    assert len(candidates['functions']) == 8
    for i, row in enumerate(candidates['functions'], 1):
        id_ = f'A05-CF{i:02}'
        assert row['id'] == id_
        assert {key: row[key] for key in EXPECTED[id_]} == EXPECTED[id_], id_
        assert row['subact'] == ('A05-S1' if i <= 3 else 'A05-S2' if i <= 6 else 'A05-S3')
        assert row['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
        assert row['evidence_class'] == 'CANDIDATE'
        assert row['selected_event'] is False and row['author_locked'] is False
        if i > 1:
            assert row['entry_state'] == candidates['functions'][i-2]['changed_state']
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    for id_ in ('A05-S1','A05-S2','A05-S3'):
        assert next(row for row in cp2['subacts'] if row['id'] == id_)['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    timeline = (root / TIMELINE).read_text(encoding='utf-8-sig')
    responsibility = (root / RESPONSIBILITY).read_text(encoding='utf-8-sig')
    donor = (root / DONOR).read_text(encoding='utf-8-sig')
    sophomore = (root / SOPHOMORE).read_text(encoding='utf-8-sig')
    talent = (root / TALENT).read_text(encoding='utf-8-sig')
    assert '73경기·11선발·1,274:02' in timeline and '정확 기록 HOLD' in timeline
    assert '밤샘 게임 뒤 아침 영상·컨디셔닝 일정에 늦어 예정된 로테이션 시험 기회를 잃는다' in responsibility
    assert 'Windy City assignment 후보는 징계 자체가 아니라' in responsibility
    assert '73경기·11선발·1,274분' in donor and 'exact clock은 1,274:02' in donor
    assert 'MISSED_ROTATION' in donor and 'G_ASSIGNMENT_INACTIVE' in donor
    assert '배정 중에도 NBA 계약·급여·권리는 유지' in donor
    assert '주인공의 G League 선발·박스스코어·승패 영향은 `HOLD`' in donor
    assert 'Coby White' in sophomore and 'Satoransky' in sophomore
    assert '코칭, 영상, 실패, 반복' in talent
    skill = SKILL.read_bytes()
    assert norm_sha(skill) == candidates['common_skill']['sha256']
    assert '## 13. ★계층형 장편 설계 파이프라인' in skill.decode('utf-8-sig')
    assert '## 22. ★파일 존재와 실행 권위를 분리한다' in skill.decode('utf-8-sig')

    route = [
        {
            'id': 'R1', 'season_scope': '2018-19', 'subact': 'A05-S1',
            'source_ids': ['A05-CF01'],
            'function': 'NBA 속도에서 맡은 좁은 수비·리바운드·전환 역할을 한 번 시험한다',
            'observable_actions': [
                'In an existing rookie role opportunity he chooses the assigned defensive recovery and outlet before a self-created attack.',
                'A faster opposing action pulls him a step late to the next position; he can identify that specific timing gap without inventing a basket, opponent, date or score.',
            ],
            'cost': EXPECTED['A05-CF01']['direct_cost'],
            'bounded_exit': EXPECTED['A05-CF01']['changed_state'],
            'source_function_count': 1,
            'new_NBA_game_or_box_score_created': False,
        },
        {
            'id': 'R2', 'season_scope': '2018-19', 'subact': 'A05-S1',
            'source_ids': ['A05-CF02','A05-CF03'],
            'function': '밤샘 게임 뒤 한 번의 예정 기회 상실을 받아들이고 다음 준비 순서를 직접 조정한다',
            'observable_actions': [
                'He continues a game late into the night, delays sleep and arrives late to a scheduled video/conditioning check-in; one already planned NBA rotation try is lost and is not restored.',
                'For the next obligation he states his own missed preparation briefly and orders sleep, video and conditioning in advance; completing that next preparation does not erase the lost try or cure the habit.',
            ],
            'cost': [EXPECTED['A05-CF02']['direct_cost'], EXPECTED['A05-CF03']['direct_cost']],
            'bounded_exit': EXPECTED['A05-CF03']['changed_state'],
            'source_function_count': 2,
            'same_penalty_repeated': False,
            'assignment_is_punishment_for_recurrence': False,
        },
        {
            'id': 'R3', 'season_scope': '2018-19', 'subact': 'A05-S2',
            'source_ids': ['A05-CF04','A05-CF05','A05-CF06'],
            'function': '별도 개발 배정에서 판단·위치 과제를 반복하고, NBA 복귀가 정해질 때만 같은 역할을 다시 시험한다',
            'observable_actions': [
                'He hears an assignment explanation limited to a development task and checks the separate Windy City setting while keeping his NBA contract and roster rights.',
                'In a permitted development drill a screen leaves him behind the point of attack; he compares the defensive rotation with permitted video and repeats the same positioning question without declaring a successful stop or a G League box score.',
                'Only if a separate NBA return is scheduled does he test the defensive recovery, rebound positioning and simple connection at NBA speed; a new timing error remains possible.',
            ],
            'cost': [EXPECTED[f'A05-CF{i:02}']['direct_cost'] for i in (4,5,6)],
            'bounded_exit': EXPECTED['A05-CF06']['changed_state'],
            'source_function_count': 3,
            'NBA_contract_status_preserved': True,
            'new_assignment_or_return_date_certified': False,
            'new_G_League_score_box_or_starter_certified': False,
            'development_guarantees_NBA_return_or_success': False,
        },
        {
            'id': 'R4', 'season_scope': '2019-20', 'subact': 'A05-S3',
            'source_ids': ['A05-CF07','A05-CF08'],
            'function': '약한 손 첫 벽에서 두 비교 가능한 조기 이양을 관측하고 같은 좁은 역할을 다시 맡는다',
            'observable_actions': [
                'He tries his familiar strong-hand route, is pushed toward the weak-hand side and reaches a first defensive wall without proving a finish.',
                'In two comparable permitted 2019-20 role repetitions he carries straight with the weak hand toward the first wall and passes early to Coby or Satoransky before holding for a second self-created move; the receiving guard secures the ball both times, without a shot or scoring result.',
                'An authorized fictional team instruction gives him the same bounded carry-to-early-pass task at the next permitted role opportunity; this is a narrow observable repeat assignment, not an official game box, starting role, private coach thought, or guarantee of a successful possession.',
                'Within that same next permitted role opportunity he also recovers to his assigned defensive lane, places himself between a nearby opponent and the basket for one box-out, and makes a simple outlet connection to a guard after a teammate secures the ball; no personal rebound, stop, score, date, or new game is inferred.',
            ],
            'cost': [EXPECTED['A05-CF07']['direct_cost'], EXPECTED['A05-CF08']['direct_cost']],
            'bounded_exit': EXPECTED['A05-CF08']['changed_state'],
            'source_function_count': 2,
            'Coby_Satoransky_existing_guard_roles_preserved': True,
            'grab_and_go_short_roll_matured_early': False,
            'limited_trust_operating_witness': {
                'comparable_first_wall_handoffs_observed': 2,
                'receiving_guard_secures_ball_each_time': True,
                'next_narrow_task_reassigned_in_fictional_role_window': True,
                'official_game_or_private_receipt_certified': False,
                'made_shot_or_second_help_solution_certified': False,
                'whole_rotation_trust_certified': False,
                'next_assigned_role_sequence_directly_observed': True,
                'new_game_or_official_personal_box_from_sequence': False,
            },
        },
    ]
    assert [name for block in route for name in block['source_ids']] == list(EXPECTED)
    assert sum(block['source_function_count'] for block in route) == 8
    return {
        'schema': 'A05_EARLY_NBA_OPERATING_BATCH_V1',
        'status': 'SELECTED_ROUTINE_FOUR_FUNCTIONAL_GROUPS_INDEPENDENTLY_REVIEWED',
        'independent_review_completed': True,
        'R4_extension_independent_review_completed': True,
        'R4_role_sequence_independent_review_completed': True,
        'scope': 'FOUR_FINITE_OPERATING_GROUPS_SPANNING_EIGHT_EXISTING_CAUSAL_CANDIDATES_NOT_FINAL_EPISODES',
        'previous_exact_A04_E5_exit': previous['exit_state'],
        'original_A05_entry_projection': candidates['entry_from']['changed_state'],
        'A05_entry_projection_is_not_full_E5_exit': True,
        'planned_allocation': {'A05_slots': 92, 'existing_range': [157,248],
                               'final_episode_or_published_count_inferred': False},
        'route_groups': route,
        'direct_causal_boundaries': {
            'one_missed_rotation_opportunity_only': True,
            'missed_opportunity_restored_by_later_intent': False,
            'Windy_City_development_separate_from_discipline': True,
            'NBA_contract_and_roster_rights_survive_assignment': True,
            'conditional_NBA_return_not_earned_automatically': True,
            '2019_20_weak_hand_work_not_2018_19_rookie_payoff': True,
            'second_help_still_a_problem': True,
        },
        'historical_and_authority_limits': {
            'existing_rookie_role_line_reference': '73 GP / 11 starts / 1274:02 PROVISIONAL_LOCK; not a new game claim',
            'exact_canonical_scene_dates_or_opponents': None,
            'individual_scores_minutes_or_wins_from_this_model': None,
            'actual_2019_Windy_City_game_stats': None,
            'new_NBA_or_G_League_game_created': False,
            'Hutchison_injury_transferred_to_protagonist': False,
            'real_coach_private_thought_or_quote': None,
            'future_2020_21_advanced_offense_prepaid': False,
        },
        'next_A06': {'id': 'A06-S1', 'status': 'NOT_EXECUTED_HERE',
                     'LaMelo_arrival_or_offense_start_right_prepaid': False},
        'promotion_limits': {
            'new_final_episode_functions': 0, 'new_representative_games': 0,
            'whole_A05_subacts_or_Act_complete': False,
            'whole_g13_complete': False, 'whole_g14_complete': False,
            'actual_context_packs': 0, 'new_author_lock': False,
            'manuscript_count': 0, 'manuscript_allowed': False,
            'design_gate': 'CLOSED',
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {path: norm_sha((root / path).read_bytes()) for path in SOURCES},
        'writing_skill_sha256': norm_sha(skill),
    }


def render(data):
    lines = [
        '# A05 2018–20 초기 NBA 운영 배치', '',
        '**범위:** 기존 조건부 인과 8개를 네 기능군으로 묶은 독립 검토 설계 모델. 92 계획 슬롯이나 8후보를 새 회차 의무로 세지 않는다. 원고를 쓰지 않는다.', '',
        f"- 상태: `{data['status']}`",
        f"- A04 E5 정확 출구: {data['previous_exact_A04_E5_exit']}",
        '- 2018–19 역할선 73경기·11선발·1,274:02는 기존 역할 원장의 잠금 범위다. 이번에 개별 경기·분·점수·날짜를 새로 배정하지 않는다.', '',
        '| 기능군 | 원인과 행동 | 직접 비용·한정 출구 |', '| --- | --- | --- |',
    ]
    for block in data['route_groups']:
        actions = '<br>'.join(block['observable_actions'])
        cost = '; '.join(block['cost']) if isinstance(block['cost'], list) else block['cost']
        lines.append(f"| {block['id']} ({','.join(block['source_ids'])}) | {actions} | {cost}<br>출구: {block['bounded_exit']} |")
    lines += [
        '', '- R2의 기회 상실은 한 번만 발생하며 다음 준비가 그 기회를 복원하지 않는다. R3의 Windy City 배정은 별도 개발 경로다.',
        '- R3의 복귀 재시험은 실제 복귀가 별도로 정해질 때만 적용한다. R4는 2019–20 약한 손/첫 벽 과제이며 신인년으로 앞당기지 않는다.',
        '- 실존 코치 내면·정확 경기/상대/분·G League 박스·주인공 새 부상·2020–21 완성 기술은 인증하지 않는다.',
        '- S1–S3 및 A05 Act의 **한정 운영 출구**는 국소 관측 감사에서 판정한다. 전체 G13/G14·정확 개인 경기기록·실제 Pack·원고는 미완료, 설계/원고 게이트는 `CLOSED`다.', '',
    ]
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A05 operating batch differs from source-bound route']


def self_test(data, root=ROOT):
    cases = [
        ('92 slots become 92 episodes', lambda x: x['planned_allocation'].update(final_episode_or_published_count_inferred=True)),
        ('lost try restored', lambda x: x['direct_causal_boundaries'].update(missed_opportunity_restored_by_later_intent=True)),
        ('assignment becomes punishment', lambda x: x['direct_causal_boundaries'].update(Windy_City_development_separate_from_discipline=False)),
        ('rookie weak hand prepayment', lambda x: x['route_groups'][3].update(season_scope='2018-19')),
        ('NBA return guaranteed', lambda x: x['route_groups'][2].update(development_guarantees_NBA_return_or_success=True)),
        ('new game claimed', lambda x: x['historical_and_authority_limits'].update(new_NBA_or_G_League_game_created=True)),
        ('limited handoffs erased', lambda x: x['route_groups'][3]['limited_trust_operating_witness'].update(comparable_first_wall_handoffs_observed=0)),
        ('second help silently solved', lambda x: x['route_groups'][3]['limited_trust_operating_witness'].update(made_shot_or_second_help_solution_certified=True)),
        ('next role sequence erased', lambda x: x['route_groups'][3]['limited_trust_operating_witness'].update(next_assigned_role_sequence_directly_observed=False)),
    ]
    for name, mutation in cases:
        changed = copy.deepcopy(data)
        mutation(changed)
        assert validate(changed, root), name
    original_load = load
    for name, path, mutation in [
        ('E5 exact exit replaced', PREVIOUS,
         lambda x: x.update(exit_state='이미 NBA 득점왕과 대표팀 자리를 확정했다')),
        ('CF02 same-ID missed cost erased', CANDIDATES,
         lambda x: x['functions'][1].update(direct_cost='예정된 로테이션 기회는 그대로 유지된다')),
        ('CF04 same-ID assignment becomes discipline', CANDIDATES,
         lambda x: x['functions'][3].update(choice='지각 징계로 Windy City에 보내진다')),
    ]:
        def altered(root, requested, path=path, mutation=mutation):
            source = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                source = copy.deepcopy(source)
                mutation(source)
            return source
        with patch(__name__ + '.load', side_effect=altered):
            assert validate(data, root), name
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
        (ROOT / MARKDOWN).write_text(render(data), encoding='utf-8')
    errors = validate(data)
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors += validate(saved)
        if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'current': not errors, 'errors': errors,
                      'negative_controls': tested, 'status': data['status']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
