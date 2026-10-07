"""Official preseason schedule, not played scores or adopted alternate dates."""
from pathlib import Path
from datetime import datetime
from collections import Counter
import argparse, csv, hashlib, io, json, re
import fitz

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_nba_2022_23_published_calendar.py'
OUT = 'simulation/NBA_2022_23_PUBLISHED_CALENDAR_PROVENANCE.json'
MD = OUT[:-5] + '.md'
LEAGUE = 'simulation/NBA_2022_23_PUBLISHED_CALENDAR.csv'
CHI = 'simulation/CHICAGO_2022_23_PUBLISHED_CALENDAR.csv'
CACHE = Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-2022-23-calendar-20261007')
DOCS = {
    'league_bydate': ('https://pr.nba.com/wp-content/uploads/sites/46/2022/08/2022-23-NBA-Schedule-By-Date-8-17-22.pdf', 'f98d5b6273d3c7793a74b356f1fceba1f1a47656572b2825645bf5794ac9ef81', 23),
    'league_byteam': ('https://pr.nba.com/wp-content/uploads/sites/46/2022/08/2022-23-NBA-Schedule-By-Team-8-17-22.pdf', 'e7d774794df47fe54887ff9505471ebed12f1a740a692ecc6096fb104ac927ad', 30),
    'CHI_printable': ('https://cdn.nba.com/teams/uploads/sites/1610612741/2022/10/Bulls_2223_Schedule.pdf', 'e6a1cd1ce797c88896871b6df0fb98588464be269a5a25a164b5f8e3ff48194a', 1),
}
NAMES = dict(zip(
    ['Atlanta','Boston','Brooklyn','Charlotte','Chicago','Cleveland','Dallas','Denver','Detroit','Golden State','Houston','Indiana','LA Clippers','L.A. Lakers','Memphis','Miami','Milwaukee','Minnesota','New Orleans','New York','Oklahoma City','Orlando','Philadelphia','Phoenix','Portland','Sacramento','San Antonio','Toronto','Utah','Washington'],
    ['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS']))
DAY_PATTERN = r'(?m)^(\d{1,4})\n(Mon\.|Tue\.|Wed\.|Thu\.|Fri\.|Sat\.|Sun\.)\n(\d{1,2}/\d{1,2}/\d{2})\n([^\n]+)\n([^\n]+)\n([^\n]+)\n([^\n]+)'
TEAM_PATTERN = r'(?m)^(\d{1,2})\n(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\n(\d{1,2}/\d{1,2}/\d{2})\n([^\n]+)\n([^\n]+)'
ARENAS = {'A': 'Mexico City Arena, Mexico City', 'B': 'Alamodome, San Antonio', 'C': 'Accor Arena, Paris', 'D': 'Moody Center, Austin'}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def normalized(p):
    return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')


def sha(p):
    return hashlib.sha256(normalized(p).encode()).hexdigest()


def pages(key):
    url, checksum, count = DOCS[key]
    p = CACHE / (key + '.pdf')
    need(hashlib.sha256(p.read_bytes()).hexdigest() == checksum, 'Primary raw PDF changed: ' + key)
    with fitz.open(p) as d:
        need(len(d) == count, 'Primary page count changed')
        return [pg.get_text().replace('\r\n','\n').replace('\r','\n') for pg in d]


def iso(s):
    return datetime.strptime(s, '%m/%d/%y').date().isoformat()


def csv_text(rows):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader(); writer.writerows(rows)
    return stream.getvalue()


def build(root=ROOT):
    raw = {k: pages(k) for k in DOCS}
    league = []
    for page, t in enumerate(raw['league_bydate'], 1):
        matches = list(re.finditer(DAY_PATTERN, t))
        for i, m in enumerate(matches):
            no = int(m[1]); date = iso(m[3]); away, home = NAMES[m[4]], NAMES[m[5]]
            need(home != away, 'Schedule self-match')
            need(datetime.strptime(date,'%Y-%m-%d').strftime('%a') + '.' == m[2], 'Printed weekday/date mismatch')
            end = matches[i+1].start() if i+1 < len(matches) else len(t)
            # Only the isolated marker after a game is its arena note.
            marker = [s.strip() for s in t[m.end():end].splitlines() if s.strip() in ARENAS]
            need(len(marker) <= 1, 'Ambiguous arena marker')
            mark = marker[0] if marker else ''
            league.append({'published_game_number': no, 'calendar_key': f'PUBLISHED_2022_{no:04}', 'published_date': date, 'home': home, 'away': away,
                           'published_home_local_time': m[6], 'published_ET': m[7], 'bydate_PDF_page': page,
                           'original_arena_marker': mark, 'original_venue_note': ARENAS.get(mark,''),
                           'actual_NBA_game_id': '', 'actual_played_date': '', 'alternate_date_selected': '', 'alternate_result_selected': ''})
    need([x['published_game_number'] for x in league] == list(range(1,1231)), 'Published 1230 game order changed')
    need(len({(x['published_date'],x['home'],x['away']) for x in league}) == 1230, 'Duplicate published matchup')
    memberships = Counter(t for x in league for t in (x['home'],x['away']))
    home_counts = Counter(x['home'] for x in league); away_counts = Counter(x['away'] for x in league)
    need(set(memberships) == set(NAMES.values()) and set(memberships.values()) == {82}, '30x82 membership mismatch')
    need(set(home_counts.values()) == set(away_counts.values()) == {41}, 'Published 41+41 mismatch')
    bykey = {(x['published_date'],x['home'],x['away']): x for x in league}
    comparisons = []; chicago_team = []
    for page, t in enumerate(raw['league_byteam'], 1):
        team = t.splitlines()[0]; need(team in memberships, 'Unknown team PDF heading')
        found = []
        for m in re.finditer(TEAM_PATTERN, t):
            away = m[4].startswith('at '); opp = NAMES[m[4][3:] if away else m[4]]
            key = (iso(m[3]), opp if away else team, team if away else opp)
            need(key in bykey, 'Independent team/date/home/away disagreement')
            found.append({'team_game_number': int(m[1]), 'published_date': key[0], 'home': key[1], 'away': key[2],
                          'calendar_key': bykey[key]['calendar_key'], 'opponent': opp, 'byteam_PDF_page': page})
        found.sort(key=lambda x: x['team_game_number'])
        need([x['team_game_number'] for x in found] == list(range(1,83)), 'Independent team82 ordinal mismatch')
        need(found == sorted(found,key=lambda x:x['published_date']), 'Team schedule chronological order mismatch')
        need(len({x['calendar_key'] for x in found}) == 82, 'Duplicate team row')
        comparisons.append({'team': team, 'page': page, 'matched_game_count': len(found)})
        if team == 'CHI':
            chicago_team = found
    need(len(comparisons) == 30 and len({x['team'] for x in comparisons}) == 30, 'All-team schedule match incomplete')
    chi = [{**x, 'original_venue_note': bykey[(x['published_date'],x['home'],x['away'])]['original_venue_note'],
            'actual_NBA_game_id': '', 'actual_played_date': '', 'alternate_date_selected': '', 'alternate_result_selected': ''} for x in chicago_team]
    need(len(chi)==82 and chi[0]['published_date']=='2022-10-19' and chi[-1]['published_date']=='2023-04-09', 'Chicago82 bounds changed')
    paris = next(x for x in chi if x['published_date']=='2023-01-19')
    need((paris['home'],paris['away'],paris['original_venue_note']) == ('DET','CHI','Accor Arena, Paris'), 'Nominal home versus Paris arena lost')
    outputs = {LEAGUE: csv_text(league), CHI: csv_text(chi)}
    v = {'id': 'NBA_2022_23_PUBLISHED_CALENDAR_PROVENANCE', 'baseline_main': 'd111ddb9a0246345b1c04784404c829bf3202576',
         'status': 'PRIMARY_PUBLISHED_SCHEDULE_FACTS_INDEPENDENT_REVIEW_PENDING_NOT_ALTERNATE_ADOPTION',
         'publication': '2022-08-17', 'source_sha256': {SELF: sha(root/SELF)},
         'primary_support': {k: {'url': DOCS[k][0], 'cache_path': str(CACHE/(k+'.pdf')), 'HTTP_status_observed': 200, 'raw_sha256': DOCS[k][1],
                               'pages':len(ts), 'page_text_LF_sha256':{str(i):hashlib.sha256(t.encode()).hexdigest() for i,t in enumerate(ts,1)}} for k,ts in raw.items()},
         'verification': {'league_games':1230, 'teams':30, 'games_each':82, 'nominal_home_each':41, 'nominal_away_each':41,
                          'independent_byteam_rows_joined':2460, 'all_team_crosschecks':comparisons, 'Chicago_games':82, 'Paris_nominal_home_vs_venue_preserved':paris},
         'derived_text_sha256':{f:hashlib.sha256(s.encode()).hexdigest()for f,s in outputs.items()},
         'scope': 'Direct official preseason publication, not actual played dates/IDs/scores or clinical observations. PUBLISHED keys are our publication identifiers, not fabricated NBA game IDs. Later reschedules or venues reopen their affected rows. Original publication is SUBJECT TO CHANGE.',
         'original_international_venue_notes': [x for x in league if x['original_arena_marker']],
         'next_consumption': 'Connect the already selected FY22 15STD2TW and a chosen dated role/health model to these schedule facts; separately choose working chronology and opponent changes. Jan19 nominal DET home in Paris is not ordinary Detroit arena advantage.',
         'alternate_calendar_or_results_selected':False, 'whole_macro3_complete':False, 'manuscript_allowed':False, 'design_gate':'CLOSED', 'freeze':'v0.30 PARTIAL'}
    return v, outputs


def markdown(v):
    return '\n'.join(['# NBA 2022–23 공식 발표 일정 입력', '',
        'NBA 공식8/17 날짜별23쪽·팀별30쪽·Chicago10월공식표1쪽의 실제PDF bytes를 회수했다. **1230경기·30팀×82, 팀별2460행 교차 일치·Chicago82**를 검문한다.', '',
        '발표된 예정 일정이며 실제 played date/game-ID/점수·대체세계 채택과 구분한다. PUBLISHED_2022 키는 자체 문서키다. 실제NBA ID를 발표번호로 만들어 넣지 않는다.', '',
        'Chicago첫예정10/19 Miami원정, 마지막4/9 Detroit명목홈. Jan19는 DET명목홈/Accor Arena Paris의 장소를 보존한다. DET홈이라는 이유만으로 Detroit홈코트효과를 자동적용하지 않는다.', '',
        f'[리그 예정표](NBA_2022_23_PUBLISHED_CALENDAR.csv) · [Chicago82 예정표](CHICAGO_2022_23_PUBLISHED_CALENDAR.csv)', '',
        '[원 공식 발표](https://pr.nba.com/2022-23-nba-schedule/) · [날짜별 원PDF]('+DOCS['league_bydate'][0]+') · [팀별 원PDF]('+DOCS['league_byteam'][0]+')', '',
        '별도 FY22 코어 계약 선택 소비기에서15+2를 연결하고 날짜별 역할/건강·명명된 상대 변화·작업 일정을 선택하는 다음 실행을 진행한다. 원역사 연기/임상/선수 거래나 두시즌 승패를 이표로 확정하지 않는다.', '',
        '신규 외부CLI NOT_RUN. 전체3번/독립G16/원고 인증0·v0.30 PARTIAL·설계/원고 CLOSED·미완료5/6번까지4.', ''])


def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');o=a.parse_args();v,outputs=build();outputs[OUT]=json.dumps(v,ensure_ascii=False,indent=2)+'\n';outputs[MD]=markdown(v)
    if o.write:
        for f,s in outputs.items(): (ROOT/f).write_text(s,encoding='utf-8')
    if o.check:
        for f,s in outputs.items(): need(normalized(ROOT/f)==s,'Published schedule artifact stale: '+f)
    print(json.dumps({'published_games':1230,'independent_team_rows':2460,'Chicago':82,'actual_game_IDs_or_results':0,'alternate_adoption':False}))


if __name__=='__main__': main()
