"""Select one bounded A03 role-repetition practice after the first local function."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a03_e1_final_episode_function as previous_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A03_CF02_ROLE_REPETITION_WORKING_MODEL_2026_10_07.json')
MARKDOWN = OUTPUT.with_suffix('.md')
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
CANDIDATES = 'design/A03_CONDITIONAL_EPISODE_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
SCOPE = 'control/COLLEGE_ARC_SCOPE_GATE.md'
SOURCES = ('tools/build_a03_cf02_role_repetition_working_model.py', PREVIOUS,
           CANDIDATES, CP2, SCOPE)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def source_bytes(root, path):
    return (root / path).read_bytes()


def normalized_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def build(root=ROOT):
    previous = load(root, PREVIOUS)
    candidates = load(root, CANDIDATES)
    cp2 = load(root, CP2)
    assert previous == previous_builder.load(root, previous_builder.OUTPUT), 'E1 input differs from producer source'
    assert not previous_builder.validate(previous, root=root), 'A03 E1 must be source-current'
    assert previous['episode_function_id'] == 'A03-EF-001'
    assert previous['final_function_order'] == 20 and previous['planned_allocation_slot'] == 91
    assert previous['next_unit']['id'] == 'A03-F02'
    assert previous['next_unit']['success_or_trust_prepaid'] is False
    assert previous['whole_A03_S1_exit_certified'] is False
    assert previous['inter_act_bridge']['I3_certification_retained'] is True
    assert previous['inter_act_bridge']['official_game_executed'] is False
    assert candidates['status'] == 'THREE_CONDITIONAL_FUNCTIONS_NOT_FINAL_G13'
    assert candidates['final_episode_functions'] == 0
    f02 = candidates['functions'][1]
    expected = {
        'id': 'A03-F02', 'subact': 'A03-S2', 'function': '역할 획득',
        'entry': '역할 과제를 알지만 동료에게 맡겨질 반복 증거가 부족',
        'pressure': '개인 리바운드/볼 수신 기회와 팀에 필요한 위치·박스아웃의 경쟁',
        'choice': '볼 없는 준비 위치와 박스아웃을 먼저 수행해 동료의 공 확보를 돕는 반복',
        'cost': '자기 리바운드/공격 표본에 남지 않는 노동과 반복 훈련 시간',
        'changed_state': '관측 가능한 반복 수행이 제한 수비 기능을 맡길 근거가 됨',
        'next': 'A03-F03',
        'causal_link': '반복으로 획득한 역할을 토너먼트 압박에서 다시 시험',
        'observation_limit': '한 번의 칭찬을 신뢰 완성으로 쓰지 않음; 정확 경기/분 상승 HOLD',
    }
    assert {key: f02[key] for key in expected} == expected
    assert f02['status'] == 'CONDITIONAL_EPISODE_FUNCTION_CANDIDATE'
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    s2 = next(row for row in cp2['subacts'] if row['id'] == 'A03-S2')
    assert s2['choice'] == '개인 리바운드 수만 좇지 않고 동료가 공을 잡도록 박스아웃과 볼 없는 준비를 반복한다'
    assert s2['cost'] == '볼 없는 준비와 박스아웃'
    assert s2['exit_state'] == '동료가 맡기는 수비 기능'
    scope = source_bytes(root, SCOPE).decode('utf-8-sig')
    assert '대표 경기 기능 | 3개' in scope and '40경기 전체 분·스탯 재계산' in scope

    practice = [
        {'id': 'P1', 'type': 'FICTIONAL_STAFF_ASSIGNED_BOUNDED_PRACTICE',
         'actor': 'FICTIONAL_VILLANOVA_TEAM_STAFF',
         'after': 'A03-EF-001 accepted next limited role task',
         'assigned_task': 'At the next permitted defensive practice, keep the agreed help-space cue, locate the nearby opponent when a shot goes up, and block out before chasing the ball.',
         'access': 'The protagonist hears his assigned task and sees only his own and nearby teammates’ practice actions.',
         'NCAA_or_academic_clearance_decided_by_staff': False,
         'official_game_or_real_2017_practice_claimed': False},
        {'id': 'P2', 'type': 'FIRST_OBSERVED_REPETITION', 'after': 'P1',
         'choice': 'He holds the assigned position and blocks out instead of pursuing a rebound for his own count.',
         'observed_result': 'On the first loose-ball rebound in this drill, a teammate can secure the ball while he keeps the opponent away.',
         'individual_stat_or_game_rebound_awarded': False},
        {'id': 'P3', 'type': 'SECOND_OBSERVED_REPETITION_IN_SAME_PRACTICE', 'after': 'P2',
         'choice': 'On a second shot-and-rebound cue in the same permitted practice, he again checks position and blocks out first.',
         'observed_result': 'A teammate again secures the ball in this drill; only these two repetitions are observed.',
         'individual_stat_or_game_rebound_awarded': False},
    ]
    result = (
        '다음 허용 수비 훈련에서 주인공은 맡은 도움 위치를 확인한 뒤 두 번의 공 궤적마다 자기 리바운드를 쫓기보다 '
        '가까운 상대의 진로를 막아 동료가 공을 확보하게 했다. 같은 연습의 두 관측은 맡은 역할을 반복할 수 있다는 국소 근거지만, '
        '실전 신뢰·출전 분 상승·기술 숙련·시즌 전체의 안정성은 아직 확인되지 않았다.'
    )
    return {
        'schema': 'A03_CF02_ROLE_REPETITION_WORKING_MODEL_V1',
        'status': 'SELECTED_ROUTINE_ROLE_REPETITION_INDEPENDENTLY_REVIEWED',
        'independent_review_completed': True,
        'scope': 'ONE_FICTIONAL_PERMITTED_PRACTICE_TWO_VISIBLE_REPETITIONS_NOT_GAME',
        'source_function_id': 'A03-F02',
        'previous_exact_full_exit': previous['exit_state'],
        'why_two_observations': 'The source candidate calls for repetition rather than one praise moment. Two separate shot-and-rebound cues in the same practice are the minimum visible plural evidence; they do not certify season reliability.',
        'practice': practice,
        'direct_present_cost': 'He forgoes chasing two personal rebound chances and uses the permitted practice time on position and teammate possession; existing academic duties still remain.',
        'selected_design_exit_state': result,
        'next_candidate': {'id': 'A03-F03', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'Texas_Tech_result_or_200_minute_reconstruction_prepaid': False},
        'limits': {
            'actual_Villanova_game_or_practice_film_certified': False,
            'official_minutes_stats_or_start_certified': False,
            'all_teammates_trust_or_private_feelings_certified': False,
            'repeated_season_role_success_certified': False,
            'technical_mastery_or_guaranteed_roster_promotion': False,
            'existing_I3_full_qualifier_revoked': False,
            'new_academic_life_cost_event_added': False,
            'new_representative_games': 0,
            'three_representative_function_cap_changed': False,
            'A03_S2_whole_exit_or_final_function_completed_here': False,
            'Texas_Tech_or_A03_S3_executed': False,
        },
        'author_locked': False, 'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {path: normalized_sha(source_bytes(root, path)) for path in SOURCES},
    }


def render(data):
    rows = ['# A03 제한 역할의 두 관측 반복', '',
            '**범위:** 원고가 아닌 가상 팀의 다음 허용 연습 한 번. 이미 수락한 좁은 과제를 두 공 궤적에서 시험한다.', '',
            f"- 상태: `{data['status']}`",
            f"- 정확 진입: {data['previous_exact_full_exit']}",
            f"- 두 관측의 이유: {data['why_two_observations']}", '',
            '| 단계 | 할당·선택 | 관측 결과 |', '| --- | --- | --- |']
    for row in data['practice']:
        rows.append(f"| {row['id']} | {row.get('assigned_task', row.get('choice'))} | {row.get('access', row.get('observed_result'))} |")
    rows += ['', f"- 직접 비용: {data['direct_present_cost']}",
             f"- 국소 출구: {data['selected_design_exit_state']}",
             '- 이 한 연습의 두 박스아웃은 개인 공식 리바운드 2개나 팀 전체 신뢰를 뜻하지 않는다. 기존 학업 의무도 남는다.',
             '- 실존 Villanova 연습·경기·분·선발·선수 발언·Paschall 등의 기존 공로를 바꾸지 않는다.',
             '- 다음 Texas Tech 압력 검문·정확 200분 재분배는 선지급하지 않는다. 대표 기능3·새 대표 경기0, 전체 G13/G14 미완료·원고0·게이트 `CLOSED`.', '']
    return '\n'.join(rows)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A03 role repetition differs from source-bound selected design']


def self_test(data):
    cases = [
        ('prepay actual minutes', lambda x: x['limits'].update(official_minutes_stats_or_start_certified=True)),
        ('prepay everyone trust', lambda x: x['limits'].update(all_teammates_trust_or_private_feelings_certified=True)),
        ('claim game rebound', lambda x: x['practice'][1].update(individual_stat_or_game_rebound_awarded=True)),
        ('erase second repetition', lambda x: x['practice'].pop()),
        ('prepay Texas Tech', lambda x: x['next_candidate'].update(Texas_Tech_result_or_200_minute_reconstruction_prepaid=True)),
    ]
    for name, mutate in cases:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_load = load
    for name, path, mutate in [
        ('E1 exact exit altered', PREVIOUS, lambda x: x.update(exit_state='첫 공식 경기에서 선발로 우승했다')),
        ('F02 same-ID choice reversed', CANDIDATES,
         lambda x: x['functions'][1].update(choice='동료 공 확보 대신 자기 공격 표본을 독점한다')),
        ('CP2 S2 exit made all trust', CP2,
         lambda x: next(row for row in x['subacts'] if row['id'] == 'A03-S2').update(exit_state='동료 전원이 영구적으로 신뢰함')),
    ]:
        def altered(root, requested, path=path, mutate=mutate):
            source = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                source = copy.deepcopy(source)
                mutate(source)
            return source
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
