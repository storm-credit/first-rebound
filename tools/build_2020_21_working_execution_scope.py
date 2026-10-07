"""Count completed working scopes separately from formal season gates."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import build_2020_21_regular_clock_completion as regular_check
import build_2021_l2_working_minutes as playin_check
import build_2021_all_playoff_coach_plans as playoff_check
import apply_2021_l2_working_calendar as common
import build_2020_21_regular_working_chronology as regular_order
import build_2021_l2_working_chronology as playin_order
import build_2021_l2_nonplayoff_roster_scope as roster_check
import check_chicago_d1_s2 as s2_check

ROOT = Path(__file__).resolve().parents[1]
REGULAR = 'simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.json'
PLAYIN = 'simulation/NBA_2021_L2_WORKING_MINUTE_MODELS.json'
PLAYOFF = 'simulation/NBA_2021_ALL_DATED_PLAYOFF_COACH_PLANS.json'
REGULAR_ORDER = 'simulation/NBA_2020_21_REGULAR_WORKING_CHRONOLOGY.json'
PLAYIN_ORDER = 'simulation/NBA_2021_L2_WORKING_CHRONOLOGY.json'
PLAYIN_ROSTER = 'simulation/NBA_2021_L2_NONPLAYOFF_ROSTER_SCOPE.json'
REGISTER = 'control/CHICAGO_2020_21_D1_S2_REGISTER.json'
OUT = 'simulation/NBA_2020_21_WORKING_EXECUTION_SCOPE.json'

def build():
    formal = s2_check.evaluate(common.read(REGISTER))
    regular, playin, playoff = (common.read(p) for p in (REGULAR,PLAYIN,PLAYOFF))
    regular_check.validate_against_sources(regular)
    if playin != playin_check.build():
        raise ValueError('play-in working source reconstruction differs')
    playoff_check.validate(playoff)
    regular_chronology, playin_chronology, roster = (common.read(p) for p in (REGULAR_ORDER,PLAYIN_ORDER,PLAYIN_ROSTER))
    regular_order.validate(regular_chronology,source=regular)
    playin_order.validate(playin_chronology)
    roster_check.validate(roster)
    phases = []
    player_dates = defaultdict(list)
    team_dates = defaultdict(list)
    regular_games = {g['event_id']:g for g in regular['regular_season_games']}
    for row in regular['team_games']:
        game = regular_games[row['event_id']]
        phases.append(('REGULAR',row['event_id'],row['date'],row['team'],row['game_duration_seconds'],row['player_seconds']))
    for game in playin['games']:
        for team,row in game['teams'].items():
            phases.append(('PLAYIN',game['event_id'],game['date'],team,game['duration_model_seconds'],row['player_seconds']))
    for game in playoff['games']:
        for team,row in game['teams'].items():
            phases.append(('PLAYOFF',f"{game['series']}-G{game['game']}",game['date_model'],team,
                60*game['duration_model_minutes'],{p:60*n for p,n in row['planned_minutes'].items()}))
    rows = Counter()
    positive = Counter()
    for phase,event,date,team,duration,vector in phases:
        if abs(sum(vector.values())-5*duration)>1e-5:
            raise ValueError('phase clock incomplete')
        rows[phase] += 1
        team_dates[date,team].append((phase,event))
        for person,seconds in vector.items():
            if seconds < 0 or seconds > duration+1e-5:
                raise ValueError('phase player clock capacity')
            if seconds>1e-7:
                player_dates[date,person].append((phase,event,team))
                positive[phase] += 1
    if dict(rows) != {'REGULAR':2160,'PLAYIN':12,'PLAYOFF':176}:
        raise ValueError('phase coverage incomplete')
    if any(len(v)!=1 for v in team_dates.values()) or any(len(v)!=1 for v in player_dates.values()):
        raise ValueError('team or positive player scheduled twice on same date')
    return dict(status='WORKING_MINUTE_AVAILABILITY_RESULT_SUBSCOPES_COMPLETE_FORMAL_SEASON_HOLD',
        source_sha256={p:common.sha(p) for p in (REGULAR,PLAYIN,PLAYOFF,REGULAR_ORDER,PLAYIN_ORDER,PLAYIN_ROSTER,REGISTER)},
        authority=common.AUTH,phase_games={'REGULAR':1080,'PLAYIN':6,'PLAYOFF':88},
        phase_team_rows=dict(rows),positive_modeled_player_dates=dict(positive),
        total_games=1174,total_team_games=len(phases),same_date_team_collisions=0,
        same_date_positive_player_collisions=0,
        regular_minutes_complete=True,regular_all_five_player_existence_witnesses_complete=True,
        regular_single_bpm_results_recomputed=True,regular_clock_corrections=6,
        regular_original_ot_preserved=True,regular_record={'CHI':[31,41],'MIN':[24,48]},
        regular_working_chronology_complete=True,
        regular_working_order_team_plans=regular_chronology['summary']['new_working_chronological_team_plans'],
        regular_working_order_blocks=regular_chronology['summary']['blocks'],
        original_regular_107_witnesses_preserved=True,
        playin_six_dated_minute_availability_result_models_complete=True,
        playin_first_round_pairs_verified=playin['playoff_first_round_pairs_verified'],
        playin_qualifier_changes=playin['playoff_qualifiers_changed'],
        playin_working_chronology_complete=True,
        playin_working_order_team_plans=playin_chronology['working_team_plans'],
        playin_working_order_blocks=playin_chronology['assignment_blocks'],
        playin_nonplayoff_roster_candidates=roster['working_team_roster_candidates'],
        playin_nonplayoff_candidate_player_dates=sum(len(r['entries']) for r in roster['dated_team_rosters']),
        playin_nonplayoff_registration_conflicts=['WAS_HOMESLEY_16TH_STANDARD','GSW_HUTCHISON_PATH'],
        playoff_eighty_eight_working_coach_health_result_models_complete=True,
        scope_completed='Positive rotation availability, complete minute budgets/existence witnesses, all regular/play-in working clock orders and chosen result continuity.',
        scopes_not_certified=['Regular/play-in positional matchups and actual dead-ball substitutions',
            'All registered/reserve-player health and final four non-playoff play-in roster registration',
            'Actual boxes/scores and future optional offseason rights delivery; finite season origin/control reviewed separately',
            'Remaining fictional dated roster/transaction execution; actual acceptance/private financial terms not certified'],
        formal_gate_prerequisite_register=REGISTER,
        pending_legal_rows=[key for key, verdict in formal['legal_fields'].items() if verdict != 'LEGAL_BOUND_PASS'],
        completed_legal_rows=sum(v == 'LEGAL_BOUND_PASS' for v in formal['legal_fields'].values()),
        completed_f_legal_groups=sum(v == 'LEGAL_BOUND_PASS' for v in formal['F_legal'].values()),
        completed_a_execution=sum(v == 'PASS' for v in formal['A_execution'].values()),
        a_execution_verdicts=formal['A_execution'],
        rule='S2 allows AUTHOR_MODELED health/coaching and REPRODUCTION_PASS quantities; actual medical or private receipt originals are not new completion requirements.',
        formal_a_k_season_depends_on_all_f_legal=True,
        completed_subscope_does_not_clear_missing_law=True,
        medical_certified=False,actual_registration_certified=False,
        full_legal_execution_cleared=False,season_selected=False,manuscript_allowed=False)

def markdown(d):
    return f"""# 2020–21 완료한 작업 모델 범위와 최종 게이트

| 단계 | 경기 | 팀 경기 | 양수분 작가 모델 칸 | 완료한 범위 |
|---|---:|---:|---:|---|
| 정규시즌 | 1080 | 2160 | {d['positive_modeled_player_dates']['REGULAR']} | 선택 분·6행 초 잔차 보정·전5인 존재 증인·전체 작업 교대 순서·단일BPM 승패 재계산 |
| 플레이인 | 6 | 12 | {d['positive_modeled_player_dates']['PLAYIN']} | 선택 날짜·분·양수 가용 모델·12팀 작업 순서·L2 결과와8첫대진 연결 |
| 플레이오프 | 88 | 176 | {d['positive_modeled_player_dates']['PLAYOFF']} | 날짜별 작가 감독·건강 모델·결과 |
| 합계 | 1174 | 2348 | {sum(d['positive_modeled_player_dates'].values())} | 동일날짜 팀·양수선수 중복0 |

완료한 소범위를 실제 의료 허가나 비공개 접수 원본 대기라는 이유로 다시 미완료로 표시하지 않는다.
S2의 `AUTHOR_MODELED`와 `REPRODUCTION_PASS` 적용 범위를 기록한다. 원래 정규시즌 연장을 보존하며
플레이인/플레이오프 승패를 Chicago31–41·Minnesota24–48에 더하지 않는다.

J1 27팀 효과는 기존 점수차에 이미 한 번 연결되어 있다. F4 5 + 최종F5 23 + C2 5 + 누락F5원분기4 = 추가37팀 효과다.
따라서 **27+37=64팀·고유62경기**다. 같은CHA–CLE경기 양팀 겹침2와 C2–F5 같은팀의 별도 전벡터 대체2를 구분한다.

정규시즌2160팀·{d['regular_working_order_blocks']}블록과 플레이인12팀·{d['playin_working_order_blocks']}블록에
별도 작업용 시계 순서를 선택했다. 기존107원증인은 보존하고 새107순서를 따로 만들었다.
선발·개인초·쿼터/연장 경계를 대조했으며 실제dead-ball 교대·전술·휴식 상한 인증은 아니다.
네 비플레이오프팀은6팀-날짜/102선수칸의15+2후보로 대조했다. WAS Homesley16명과 GSW Hutchison경로가 미선택이다.
최종등록·전체 예비선수 건강·남은 날짜별 거래 실행은 따로 남는다. A3의 유한 시즌 origin/control 결산은 별도 검문으로 통과했다.
실제 계약 수락·비공개 재무·의료는 인증하지 않으며 이를 가상 설계의 새 필수 원본 요건으로 추가하지 않는다.

공식A/K/시즌 집계는 [S2 검사기](../tools/check_chicago_d1_s2.py)의 모든F법적 선행조건을 따른다.
현재 법적{d['completed_legal_rows']}PASS/{len(d['pending_legal_rows'])}HOLD({', '.join(d['pending_legal_rows'])}), F법적{d['completed_f_legal_groups']}/5·A{d['completed_a_execution']}/3·K0/4·시즌false다.
법적 통과와 전체 거래/명단/건강 실행은 구분하며 정확 금융 선택/미래픽조건을 사실로 채우지 않는다. 미완료 큰묶음6·v0.30 PARTIAL·설계/원고 CLOSED·원고0.

[정규시즌](NBA_2020_21_REGULAR_CLOCK_COMPLETION.md) · [플레이인](NBA_2021_L2_WORKING_MINUTE_MODELS.md) · [플레이오프](NBA_2021_ALL_DATED_PLAYOFF_COACH_PLANS.md)
[기계 범위표](NBA_2020_21_WORKING_EXECUTION_SCOPE.json)
[정규 작업 순서](NBA_2020_21_REGULAR_WORKING_CHRONOLOGY.md) · [L2 작업 순서](NBA_2021_L2_WORKING_CHRONOLOGY.md) · [L2 명단 후보](NBA_2021_L2_NONPLAYOFF_ROSTER_SCOPE.md)
"""

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    data=build();md=markdown(data)
    if args.check:
        if common.read(OUT)!=data or (ROOT/OUT).with_suffix('.md').read_text(encoding='utf-8-sig')!=md:
            raise ValueError('working execution scope stale')
    else:
        (ROOT/OUT).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (ROOT/OUT).with_suffix('.md').write_text(md,encoding='utf-8')
    print(json.dumps({k:data[k] for k in ['total_games','total_team_games','phase_team_rows','positive_modeled_player_dates','same_date_positive_player_collisions']},ensure_ascii=False))
