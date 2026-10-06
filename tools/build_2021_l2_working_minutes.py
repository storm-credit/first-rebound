"""Select L2 six-game minute/availability models; no actual boxes or rosters."""
from collections import Counter
from copy import deepcopy
import argparse
import json
from pathlib import Path
import apply_2021_l2_working_calendar as calendar
import build_2020_21_regular_clock_completion as clock
import build_2021_all_playoff_coach_plans as playoff

ROOT = Path(__file__).resolve().parents[1]
CALENDAR = 'simulation/NBA_2021_L2_DATED_WORKING_CALENDAR.json'
REGULAR = 'simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.json'
PLAYOFF = 'simulation/NBA_2021_ALL_DATED_PLAYOFF_COACH_PLANS.json'
OUT = 'simulation/NBA_2021_L2_WORKING_MINUTE_MODELS.json'
LEV = 'https://www.nba.com/news/pacers-swingman-caris-levert-to-miss-play-in-game-vs-hornets'
AUTH = calendar.AUTH

def read(path):
    return calendar.read(path)

def build():
    dated = read(CALENDAR)
    if dated != calendar.build():
        raise ValueError('selected L2 date/result input changed')
    regular = read(REGULAR)
    clock.validate_against_sources(regular)
    postseason = read(PLAYOFF)
    playoff.validate(postseason)
    if postseason['source_sha256'] != {p:calendar.sha(p) for p in postseason['source_sha256']}:
        raise ValueError('stale playoff source bridge')
    donors = {}
    core = {'Protagonist','LaMelo Ball','Zach LaVine','Lauri Markkanen','Wendell Carter Jr.'}
    for team in ('CHI','WAS','GSW','SAS'):
        candidates = [r for r in regular['team_games'] if r['team']==team
            and (team!='CHI' or all(r['player_seconds'].get(p,0)>0 for p in core))]
        source = max(candidates,key=lambda r:r['date'])
        if source['game_duration_seconds']!=2880:
            raise ValueError('working regulation donor required')
        donors[team] = dict(player_seconds=deepcopy(source['player_seconds']),
            starters=deepcopy(source['starters']), witness=deepcopy(source['lineup_witness']),
            modeled_absent=[], zero_health={p:None for p,n in source['player_seconds'].items() if n==0},
            source=dict(path=REGULAR,event_id=source['event_id'],team=team),
            source_full_roster_included=False)
    for team in ('BOS','IND','POR','MEM'):
        first = next(g for g in postseason['games'] if team in g['teams'])
        source = first['teams'][team]
        players = {p:60*n for p,n in source['planned_minutes'].items()}
        witness = [{'players':deepcopy(b[team]),'seconds':60*(b['end']-b['start'])} for b in first['blocks']]
        donors[team] = dict(player_seconds=players, starters=deepcopy(first['blocks'][0][team]),
            witness=witness, modeled_absent=[p for p,v in source['players'].items() if v['mode']=='MODELED_ABSENT'],
            zero_health={p:None for p,v in source['players'].items() if v['mode']=='COACH_ZERO_HEALTH_UNSELECTED'},
            source=dict(path=PLAYOFF,series=first['series'],game=first['game'],team=team),
            source_full_roster_included=True)
    if 'Caris LeVert' not in donors['IND']['modeled_absent']:
        raise ValueError('explicit IND working absence required')
    games = []
    for selected in dated['games']:
        teams = {}
        for team in (selected['home'],selected['away']):
            donor = deepcopy(donors[team])
            clock.check_witness(donor['player_seconds'],2880,donor['witness'])
            if len(set(donor['starters']))!=5 or any(donor['player_seconds'].get(p,0)<=0 for p in donor['starters']):
                raise ValueError('working starters must belong to positive rotation')
            if set(donor['modeled_absent']) & set(donor['player_seconds']):
                raise ValueError('modeled absence in positive rotation')
            teams[team] = dict(**donor,
                modeled_available=sorted(p for p,n in donor['player_seconds'].items() if n>0),
                author_selection='NEW_L2_DATE_WORKING_AVAILABILITY_AND_MINUTE_ALLOCATION',
                selection_reason=('Use nearest final-week full-core donor; select LaVine available again and do not import Charlotte LaMelo wrist contact.'
                    if team=='CHI' else 'Reuse selected rotation as a new dated author model, not a claim of observed play-in minutes.'),
                no_new_contact_injury_selected=True, recovery_or_medical_certificate=False,
                actual_active_list_certified=False, legal_registration_cleared=False,
                actual_substitution_order_certified=False, lineup_scope='UNORDERED_FIVE_PLAYER_EXISTENCE_NOT_TACTICAL_OR_COACH_CHRONOLOGY')
        named = [p for row in teams.values() for p,n in row['player_seconds'].items() if n>0]
        if len(named)!=len(set(named)):
            raise ValueError('player used by both opponents')
        games.append(dict(event_id=selected['event_id'],date=selected['date'],
            home=selected['home'],away=selected['away'],selected_winner=selected['winner'],
            result_source=CALENDAR,duration_model_seconds=2880,overtime_model_periods=0,
            teams=teams, score=None,box=None,winner_derived_from_minutes=False,
            winner_author_selected=True,medical_certified=False,actual_result_certified=False))
    bracket = read(calendar.BRACKET)['conferences']
    first_round = {g['series']:g for g in postseason['games'] if g['game']==1 and g['series'] in ('E1','E2','E3','E4','W1','W2','W3','W4')}
    dependencies = []
    for conference in ('east','west'):
        expected = bracket[conference]['first_round']
        prefix = 'E' if conference=='east' else 'W'
        for index,pair in enumerate(expected,1):
            downstream = first_round[prefix+str(index)]
            if set(downstream['teams']) != {pair['higher_team'],pair['lower_team']}:
                raise ValueError('L2 qualifiers differ from existing playoff first round')
        finals = [g for g in games if g['event_id'] in {r['event_id'] for r in dated['games'] if r['conference']==conference}]
        for team in bracket[conference]['final_seeds'][6:8]:
            qualification = max((g for g in finals if g['selected_winner']==team),key=lambda g:g['date'])
            downstream = next(g for g in first_round.values() if team in g['teams'])
            if qualification['date']>=downstream['date_model']:
                raise ValueError('playoff date precedes play-in qualification')
            dependencies.append(dict(team=team,qualification_event=qualification['event_id'],
                qualification_date=qualification['date'],first_round_series=downstream['series'],
                first_playoff_date=downstream['date_model'],qualifier_unchanged_from_selected_l2=True))
    expected_qualification={'BOS':'2021-05-18_BOS_IND','IND':'2021-05-20_IND_CHI',
        'POR':'2021-05-19_POR_GSW','MEM':'2021-05-21_GSW_MEM'}
    if {r['team']:r['qualification_event'] for r in dependencies}!=expected_qualification:
        raise ValueError('9/10 preliminary victory cannot be mistaken for final seed8 qualification')
    return dict(status='SIX_L2_DATED_MINUTE_AVAILABILITY_MODELS_APPLIED_TACTICAL_ROSTER_HOLD',
        authority=AUTH,source_sha256={p:calendar.sha(p) for p in (CALENDAR,REGULAR,PLAYOFF,AUTH,
            'tools/build_2021_l2_working_minutes.py','tools/build_2020_21_regular_clock_completion.py')},
        health_anchor=dict(url=LEV,inspection_utc='2026-10-06',page_lines=[153,158,164],
            fact='NBA 보도: 2021-05-18 LeVert 건강·안전 절차 결장.',
            application='5/18 BOS전 및5/20 CHI전 지속은 새 작가 모델; 원역사 상대·실제 결과를 옮기지 않는다.',
            complete_body_cached=False,new_independent_historical_source=False),
        games=games,playoff_qualification_dependencies=dependencies,
        playoff_first_round_pairs_verified=8,playoff_qualifiers_changed=0,
        working_games_applied=6,working_team_vectors=12,
        team_minutes_per_game=240,working_winners_changed_from_l2=0,
        regulation_choice='AUTHOR_WORKING_48_MINUTES_OT0_NOT_HISTORICAL_OVERTIME_ASSERTION',
        chronological_coach_plans_applied=False,full_working_rosters_included=False,
        limits=['Positive-minute availability is author modeled; no medical clearance follows.',
            'The four non-playoff-team donor vectors do not contain full standard/TW registration rosters.',
            'The four playoff rotation donors are newly selected for earlier play-in dates; neither actual usage nor recovery is inferred.',
            'CHI donor is May13 full core; May16 LaVine nonparticipation is not automatically transferred to play-in.',
            'Unordered stint existence proves budget only; positional roles, matchups and tactical chronology remain unverified.',
            'Selected L2 wins are independent author events, not a prediction implied by the reused minute vectors.'],
        medical_certified=False,actual_active_lists_certified=False,
        legal_execution_cleared=False,whole_league_health_cleared=False,
        season_selected=False,manuscript_allowed=False)

def markdown(data):
    lines=['# L2 플레이인 6날짜 분·가용성 작업 모델','',
        '기존 L2 승패·날짜에 12개 팀 분 모델을 연결했다. 승패는 작가 선택이며 분으로 예측한 결과가 아니다.',
        '', '| 날짜 | 경기 | 작가 선택 승자 | 팀별 분 |','|---|---|---|---|']
    lines += [f"| {g['date']} | {g['home']}–{g['away']} | {g['selected_winner']} | 240 |" for g in data['games']]
    lines += ['', 'CHI는 마지막 전체 코어 양수분인5/13을 작업 입력으로 선택했다. LaVine 가용성을 새로 모델링하고,',
        '원역사 Charlotte의 LaMelo 손목 접촉이나5/16 비참여를 플레이인에 자동 이월하지 않는다.',
        'WAS/GSW/SAS는5/16 분을 새 날짜의 작업 배분으로 채택했다. BOS/IND/POR/MEM은 기존 playoff 배분을 앞선 날짜에 새로 채택했다.',
        f'[LeVert 5/18 공식 결장 보도]({LEV})와5/20 공개 입력은 출처 앵커다. 대체 BOS/CHI전 지속은 별도 작가 모델이다.',
        '', '48분·연장0은 작업 선택이다. 5인조 증인은 순서 없는 분 존재 증명이며 감독 교대 시계·매치업 증명이 아니다.',
        'CHI/WAS/GSW/SAS 전체15+2명단은 이 모델에 없다. 실제 등록·의료·점수·박스·전체시즌 인증을 하지 않는다.',
        '기존 L2 진출팀4·playoff 첫 대진8쌍 및 진출일→첫경기 날짜를 직접 대조했다. 진출팀 변경0이며 두 단계는 의존관계다.',
        'LeVert 절차 지속과 LaVine 가용은 모두 새 작가 선택이다. 같은 세계 소속의 공개 절차·기존 휴식/경쟁자팀 접촉 사건은 인과 조건이 다르다.',
        '정규시즌1080 / 플레이인6 / playoff88의 단계 구분을 유지한다. 원고0·v0.30 PARTIAL·설계/원고 CLOSED.',
        '', '[기계 입력](NBA_2021_L2_WORKING_MINUTE_MODELS.json)',
        '[날짜·결과 권위](NBA_2021_L2_DATED_WORKING_CALENDAR.md)',
        '[정규시즌 분 증인](NBA_2020_21_REGULAR_CLOCK_COMPLETION.md)',
        '[playoff 감독 모델](NBA_2021_ALL_DATED_PLAYOFF_COACH_PLANS.md)', '']
    return '\n'.join(lines)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    data=build();md=markdown(data)
    if args.check:
        if read(OUT)!=data or (ROOT/OUT).with_suffix('.md').read_text(encoding='utf-8-sig')!=md:
            raise ValueError('saved L2 working minutes stale')
    else:
        (ROOT/OUT).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (ROOT/OUT).with_suffix('.md').write_text(md,encoding='utf-8')
    print('PASS six L2 results/12 working minute vectors; medical/roster/tactical/whole-season remain unconfirmed')
