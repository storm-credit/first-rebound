"""Apply the existing editorial clock-order policy to all twelve L2 team rows.

Preserve selected minutes, availability, starters, dates and winners. This is
an author working order, not actual substitutions or tactical clearance.
"""
from pathlib import Path
from copy import deepcopy
import argparse
import json
import build_2021_l2_working_minutes as selected
import build_2020_21_regular_working_chronology as order

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'simulation/NBA_2021_L2_WORKING_MINUTE_MODELS.json'
OUT = 'simulation/NBA_2021_L2_WORKING_CHRONOLOGY.json'
SOURCES = (SOURCE, 'tools/build_2021_l2_working_minutes.py',
           'tools/build_2020_21_regular_working_chronology.py',
           'tools/build_2021_l2_working_chronology.py')


def build():
    source = selected.read(SOURCE)
    if source != selected.build():
        raise ValueError('L2 source differs from original reconstruction')
    names = sorted({p for game in source['games'] for row in game['teams'].values()
                    for p in row['player_seconds']})
    ids = {p: i for i, p in enumerate(names)}
    plans = []
    for game in source['games']:
        for team, row in game['teams'].items():
            adapted = dict(event_id=game['event_id'], team=team,
                           game_duration_seconds=game['duration_model_seconds'],
                           player_seconds=row['player_seconds'], starters=row['starters'],
                           modeled_available=row['modeled_available'])
            plan = order.make_plan(adapted, ids)
            del plan['source_row_index']
            plan.update(event_id=game['event_id'], date=game['date'], team=team,
                        selected_winner=game['selected_winner'],
                        summary=order.verify_plan(plan, adapted, names))
            plans.append(plan)
    if len(plans) != 12 or len({(p['event_id'], p['team']) for p in plans}) != 12:
        raise ValueError('six games/twelve team plans required')
    return dict(status='TWELVE_L2_TEAM_WORKING_CLOCK_ORDERS_COMPLETE',
                source=SOURCE, source_hash_convention='SHA256_UTF8_NO_BOM_LF_NORMALIZED',
                source_sha256={p: order.sha(p) for p in SOURCES},
                authority=source['authority'],
                player_dictionary=names, working_plans=plans,
                block_schema='[end elapsed game seconds,five indexes into player_dictionary]',
                policy_reference='tools/build_2020_21_regular_working_chronology.py#make_plan',
                policy='starter prefix then deterministic minimum share deviation; <=180s blocks split at period boundaries',
                working_games=6, working_team_plans=12,
                assignment_blocks=sum(p['summary']['blocks'] for p in plans),
                minimum_opening_seconds=min(p['summary']['opening_seconds'] for p in plans),
                maximum_continuous_assignment_seconds=max(p['summary']['max_continuous_player_assignment_seconds'] for p in plans),
                original_witness_arrays_preserved_in_source=True,
                player_seconds_changed=0, health_states_changed=0, results_changed=0,
                working_chronology_complete=True, actual_substitution_sequence_certified=False,
                tactical_roles_certified=False, dead_ball_schedule_certified=False,
                full_roster_registration_complete=False, whole_reserve_health_selected=False,
                medical_certified=False, legal_execution_cleared=False,
                season_selected=False, manuscript_allowed=False)


def validate(data, expected=None):
    if data != (build() if expected is None else expected):
        raise ValueError('L2 working chronology does not reproduce complete source and policy')


def markdown(d):
    lines = ['# L2 여섯 경기·열두 팀의 작업용 교대 순서', '',
             '선택 날짜·승패·원선수 초·건강·선발은 변경0이다. 원래 존재증인을 상위 파일에 보존하고',
             '각 팀에 별도 작업 감독 순서를 선택했다. 원역사의 교대·포지션·타임아웃 인증은 아니다.', '',
             '| 날짜 | 경기 | 팀 | 블록 수 | 첫 선발 배치(초) |', '|---|---|---|---:|---:|']
    lines.extend(f"| {p['date']} | {p['event_id']} | {p['team']} | {p['summary']['blocks']} | {p['summary']['opening_seconds']:g} |" for p in d['working_plans'])
    lines += ['', f"전체 {d['working_team_plans']}팀 계획·{d['assignment_blocks']}블록. 각 블록 5인 고유, 양수 가용 선수만 사용하며 첫5인은 원선발이다.",
              '원선수 초와 팀합계14,400초, 48분 및 모든 쿼터 경계를 1e-5초 오차 이내에서 재현한다.',
              f"관측 최대 연속 선수 배치 {d['maximum_continuous_assignment_seconds']:g}초는 휴식 상한 인증이 아니다.",
              '180초는 표현 블록 상한이며 인접 블록에 같은 선수가 계속 있으면 쉬었다고 계산하지 않는다.',
              '승패는 이미 선택된 작가 사건이고 순서를 통해 예측하거나 바꾸지 않는다. 상대별 전술 효과를 BPM에 추가하지 않는다.',
              '전체 명단·예비 건강·계약·법적 게이트는 별도다. 실제 의료나 비공개 접수 원본을 이 작업 모델의 새 완료 조건으로 만들지 않는다.',
              '', '[기계 입력](NBA_2021_L2_WORKING_CHRONOLOGY.json) · [상위 분 모델](NBA_2021_L2_WORKING_MINUTE_MODELS.md)',
              '[공통 순서 정책](NBA_2020_21_REGULAR_WORKING_CHRONOLOGY.md) · [생성기](../tools/build_2021_l2_working_chronology.py)',
              '', '`python -B -X utf8 tools/build_2021_l2_working_chronology.py --check --self-test`',
              '', 'v0.30 PARTIAL·설계/원고 CLOSED·원고0.']
    return '\n'.join(lines)+'\n'


def self_test(base):
    for kind in ('start', 'duplicate', 'budget', 'winner', 'date', 'health', 'gate'):
        bad = deepcopy(base)
        if kind=='start': bad['working_plans'][0]['blocks'][0][0] += 1
        elif kind=='duplicate': bad['working_plans'][0]['blocks'][0][2] = bad['working_plans'][0]['blocks'][0][1]
        elif kind=='budget': bad['working_plans'][0]['blocks'][-1][0] -= 1
        elif kind=='winner': bad['working_plans'][0]['selected_winner'] = 'CHI'
        elif kind=='date': bad['working_plans'][0]['date'] = '2021-05-19'
        elif kind=='health': bad['health_states_changed'] = 1
        elif kind=='gate': bad['medical_certified'] = True
        try: validate(bad, expected=base)
        except ValueError: continue
        raise AssertionError('accepted false promotion: '+kind)
    return 7


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args=parser.parse_args()
    data=build(); validate(data, expected=data)
    body=json.dumps(data, ensure_ascii=False, indent=2)+'\n'
    md=markdown(data)
    if args.check:
        if selected.read(OUT)!=data or (ROOT/OUT).with_suffix('.md').read_text(encoding='utf-8-sig')!=md:
            raise ValueError('saved L2 chronology is stale')
    else:
        (ROOT/OUT).write_text(body, encoding='utf-8', newline='\n')
        (ROOT/OUT).with_suffix('.md').write_text(md, encoding='utf-8', newline='\n')
    tests=self_test(data) if args.self_test else 0
    print(json.dumps(dict(team_plans=data['working_team_plans'], blocks=data['assignment_blocks'],
                         negative_tests=tests, actual_substitutions=False, season=False)))
