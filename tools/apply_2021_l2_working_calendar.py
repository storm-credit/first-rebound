"""Date the already selected L2 results; never infer boxes or medical clearance."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH = 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
SOURCE = 'simulation/CHICAGO_2020_21_EXECUTION_CLOSEOUT.json'
BRACKET = 'simulation/CHICAGO_2020_21_K1_L2_BRACKET.json'
OUT = 'simulation/NBA_2021_L2_DATED_WORKING_CALENDAR.json'
PAGE = 'https://www.nba.com/news/2021-nba-play-in-tournament-schedule'

def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))

def sha(path):
    value = (ROOT/path).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
    return hashlib.sha256(value.encode()).hexdigest()

def build():
    selected = read(AUTH)['selected']['play_in']
    if selected['route'] != 'L2' or selected['exact_scores_and_boxes'] is not None:
        raise ValueError('selected L2 authority required')
    proposal, = [p for p in read(SOURCE)['postseason_proposals'] if p['id']=='L2']
    bracket = read(BRACKET)['conferences']
    dates = {'east':['2021-05-18','2021-05-18','2021-05-20'],
             'west':['2021-05-19','2021-05-19','2021-05-21']}
    games = []
    for conference in ('east','west'):
        rows = proposal[conference+'_games']
        if len(rows)!=3:
            raise ValueError('three selected games per conference required')
        for index,(date,row) in enumerate(zip(dates[conference],rows,strict=True)):
            if row['winner'] not in (row['home'],row['away']):
                raise ValueError('invalid play-in winner')
            games.append(dict(event_id=f"{date}_{row['home']}_{row['away']}", date=date,
                conference=conference, stage=['SEVEN_EIGHT','NINE_TEN','FINAL_EIGHT'][index],
                **row, classification='AUTHOR_SELECTED_L2_RESULT_AUTHOR_MODELED_DATE',
                historical_calendar_slot_source=PAGE, actual_matchup_certified=False,
                score=None, box=None, duration_seconds=None, overtime_periods=None,
                coach_plan=None, medical_certified=False, registration_certified=False))
        a,b,c = rows
        loser = a['away'] if a['winner']==a['home'] else a['home']
        if (c['home'],c['away'])!=(loser,b['winner']):
            raise ValueError('final participants must follow selected preliminary results')
        if [a['winner'],c['winner']] != bracket[conference]['final_seeds'][6:8]:
            raise ValueError('selected result/bracket mismatch')
    if [(r['home'],r['away'],r['winner']) for r in games] != [
        ('BOS','IND','BOS'),('WAS','CHI','CHI'),('IND','CHI','IND'),
        ('POR','GSW','POR'),('MEM','SAS','MEM'),('GSW','MEM','MEM')]:
        raise ValueError('delegated L2 direction changed')
    return dict(status='SELECTED_L2_DATED_WORKING_RESULTS_COACH_EXECUTION_HOLD',
        authority=AUTH, source_sha256={p:sha(p) for p in (AUTH,SOURCE,BRACKET)},
        public_date_anchor=dict(url=PAGE, inspected_utc='2026-10-06',
            observation='동부 첫날5/18·최종5/20, 서부 첫날5/19·최종5/21',
            page_lines=[161,168,175,180], original_page_body_saved=False,
            independently_new_historical_source=False),
        author_date_selection='Preserve public conference date slots, apply the already selected alternate L2 participants/results.',
        games=games, working_game_count=6, coach_games_applied=0,
        coach_games_remaining=6, exact_scores_and_boxes=None,
        source_candidate_unchanged=True, medical_certified=False,
        whole_league_health_cleared=False, whole_legal_execution_cleared=False,
        season_selected=False, manuscript_allowed=False)

def markdown(packet):
    lines=['# L2 플레이인 6경기 작업 달력','',
        '기존 L2 승패를 위임 권위 아래 날짜에 연결했다. 후보 원본을 수정하지 않는다.',
        '', '| 날짜 | 홈 | 원정 | 선택 승자 |','|---|---|---|---|']
    lines += [f"| {r['date']} | {r['home']} | {r['away']} | {r['winner']} |" for r in packet['games']]
    lines += ['',f'[NBA 공식 날짜 틀]({PAGE})만 유지하며 대체 세계 참가팀·승패는 작가 설계다.',
        '2026-10-06 원문 행161/168/175/180을 재확인했다. 원문 전체 캐시/새 독립 출처로 계수하지 않는다.',
        '', '6경기 감독·건강·등록 작업계획은 아직 미적용이다. 점수·박스·연장 횟수·시간은 null이다.',
        '정규시즌 기록에는 플레이인 승패를 더하지 않는다. CHI는 WAS 원정 승리 뒤 IND 원정 패배다.',
        '정규시즌 1080경기, 플레이인 6경기, 플레이오프 88경기는 서로 다른 단계다.',
        '의료/전체 법적 실행/전체 시즌 인증 false. freeze v0.30 PARTIAL·설계/원고 CLOSED·원고0.',
        '', '[기계 입력](NBA_2021_L2_DATED_WORKING_CALENDAR.json)',
        '[기존 위임 권위](../'+AUTH+')', '[재현 도구](../tools/apply_2021_l2_working_calendar.py)', '']
    return '\n'.join(lines)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    data=build();md=markdown(data)
    if args.check:
        if read(OUT)!=data or (ROOT/OUT).with_suffix('.md').read_text(encoding='utf-8-sig')!=md:
            raise ValueError('saved L2 working calendar stale')
    else:
        (ROOT/OUT).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (ROOT/OUT).with_suffix('.md').write_text(md,encoding='utf-8')
    print('PASS L2 six dated results; six coach plans pending; boxes/medical/legal/season remain unconfirmed')
