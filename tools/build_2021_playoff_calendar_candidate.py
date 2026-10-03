"""A chronology witness for selected series lengths, never a selected schedule."""
import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = 'simulation/NBA_2021_DELEGATED_PLAYOFF_RESULTS.json'
BRACKET = 'simulation/CHICAGO_2020_21_K1_L2_BRACKET.json'
LEAGUE = 'simulation/NBA_2020_21_FULL_SEASON.json'
DEN = 'simulation/DEN_LAL_2021_SIX_DATE_CANDIDATE_BRIDGE.json'
OUTPUT = 'simulation/NBA_2021_PLAYOFF_CALENDAR_CANDIDATE.json'
GUIDE = 'https://cdn.nba.com/teams/uploads/sites/1610612758/2022/07/kings_media_guide_2021-22_FINAL.pdf'
# Historical date skeletons, not alternate-game facts. Guide p100's misplaced
# BKN May30 row and absent PHX-LAL May27 are corrected by NBA game pages.
HISTORICAL = {
    'E1': ['05-23', '05-26', '05-29', '05-31', '06-02'],
    'E2': ['05-22', '05-25', '05-28', '05-30', '06-01'],
    'E3': ['05-22', '05-24', '05-27', '05-29'],
    'E4': ['05-23', '05-26', '05-28', '05-30', '06-02'],
    'W1': ['05-23', '05-26', '05-29', '05-31', '06-02'],
    'W2': ['05-23', '05-25', '05-27', '05-30', '06-01', '06-03'],
    'W3': ['05-22', '05-24', '05-27', '05-29', '06-01', '06-03'],
    'W4': ['05-22', '05-25', '05-28', '05-30', '06-02', '06-04', '06-06'],
    'E5': ['06-06', '06-08', '06-11', '06-14', '06-16', '06-18', '06-20'],
    'E6': ['06-05', '06-07', '06-10', '06-13', '06-15', '06-17', '06-19'],
    'W5': ['06-08', '06-10', '06-12', '06-14', '06-16', '06-18'],
    'W6': ['06-07', '06-09', '06-11', '06-13'],
    'E7': ['06-23', '06-25', '06-27', '06-29', '07-01', '07-03'],
    'W7': ['06-20', '06-22', '06-24', '06-26', '06-28', '06-30'],
    'F1': ['07-06', '07-08', '07-11', '07-14', '07-17', '07-20'],
}


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def sha(path):
    value = (ROOT / path).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(value.encode()).hexdigest()


def homecourt_team(series, ranks, wins):
    if series['id'] == 'F1':
        if wins[series['teams'][0]] == wins[series['teams'][1]]:
            raise ValueError('final homecourt tie requires a sourced tiebreak')
        return max(series['teams'], key=lambda t: wins[t])
    return min(series['teams'], key=lambda t: ranks[t])


def validate(packet):
    if len({s['id'] for s in packet['series']}) != len(packet['series']):
        raise ValueError('duplicate series ID')
    required_sources = (RESULTS, BRACKET, LEAGUE, DEN, 'simulation/DEN_LAL_2021_DELEGATED_SERIES.json')
    if packet['source_sha256'] != {p: sha(p) for p in required_sources}:
        raise ValueError('stale source revision')
    rows = {s['id']: s for s in packet['series']}
    results = {s['id']: s for s in read(RESULTS)['series']}
    ranks = {team: i for conf in read(BRACKET)['conferences'].values() for i, team in enumerate(conf['final_seeds'])}
    wins = next(s for s in read(LEAGUE)['league_cases'] if s['id'] == 'F038')['team_wins']
    if set(rows) != set(results):
        raise ValueError('series coverage')
    occupied = set()
    la_home_dates = set()
    for key, s in rows.items():
        result = results[key]
        games = s['games']
        if s['higher_homecourt_team_candidate'] != homecourt_team(result, ranks, wins):
            raise ValueError('homecourt source drift')
        if (s['teams'] != result['teams'] or s['parents'] != result['parents']
                or s['selected_winner'] != result['winner']
                or s['winner_wins'] != result['winner_wins'] or s['loser_wins'] != result['loser_wins']
                or len(games) != result['winner_wins'] + result['loser_wins']):
            raise ValueError('selected result or length drift')
        times = [date.fromisoformat(g['date_candidate']) for g in games]
        if times != sorted(set(times)):
            raise ValueError('dates not strictly increasing')
        if times[0] < date(2021, 5, 22) or times[-1] > date(2021, 7, 22):
            raise ValueError('outside published tentative playoff window')
        if any((b - a).days < 2 for a, b in zip(times, times[1:])):
            raise ValueError('candidate contains back-to-back dates')
        for i, g in enumerate(games):
            if (g['date_selected'] or g['score'] is not None or g['actual_overtime'] is not None
                    or g['health_verified'] or g['eligibility_verified'] or g['venue_booking_verified']):
                raise ValueError('authority promotion')
            higher_home = i in (0, 1, 4, 6)
            expected_home = s['higher_homecourt_team_candidate'] if higher_home else next(
                team for team in s['teams'] if team != s['higher_homecourt_team_candidate'])
            if g['home_team_candidate'] != expected_home:
                raise ValueError('2-2-1-1-1 home pattern')
            for team in s['teams']:
                token = (team, g['date_candidate'])
                if token in occupied:
                    raise ValueError('same team duplicate date')
                occupied.add(token)
            if g['home_team_candidate'] in ('LAL', 'LAC'):
                if g['date_candidate'] in la_home_dates:
                    raise ValueError('conservative shared-LA home date collision')
                la_home_dates.add(g['date_candidate'])
        for parent in s['parents']:
            end = date.fromisoformat(rows[parent]['games'][-1]['date_candidate'])
            if (times[0] - end).days < 2:
                raise ValueError('parent series does not finish before child with a non-game date')
            if rows[parent]['selected_winner'] not in s['teams']:
                raise ValueError('parent winner linkage')
    if packet['season_selected'] or packet['manuscript_allowed'] or packet['calendar_selected']:
        raise ValueError('whole packet promotion')
    den = read(DEN)['games']
    if [g['date_candidate'] for g in rows['W3']['games']] != [g['date_candidate'] for g in den]:
        raise ValueError('DEN date bridge drift')
    den_selected = read('simulation/DEN_LAL_2021_DELEGATED_SERIES.json')
    if ([g['home_team_candidate'] for g in rows['W3']['games']] != den_selected['home_teams']
            or [g['selected_game_winner'] for g in rows['W3']['games']] != den_selected['game_winners']):
        raise ValueError('DEN selected home/winner drift')
    return dict(series_count=len(rows), games=sum(len(s['games']) for s in rows.values()),
                team_date_collisions=0, LA_shared_home_date_collisions=0,
                parent_child_links=sum(len(s['parents']) for s in rows.values()),
                all_game_gaps_at_least_two_calendar_days=True, all_parent_gaps_at_least_two_calendar_days=True,
                selected_results_preserved=True, no_calendar_health_or_eligibility_promotion=True)


def build():
    bracket = read(BRACKET)['conferences']
    ranks = {team: i for conf in bracket.values() for i, team in enumerate(conf['final_seeds'])}
    wins = next(s for s in read(LEAGUE)['league_cases'] if s['id'] == 'F038')['team_wins']
    result = read(RESULTS)
    dates = {key: ['2021-' + d for d in ds] for key, ds in HISTORICAL.items()}
    dates['W6'] += ['2021-06-15', '2021-06-17', '2021-06-19']
    dates['W7'] = ['2021-06-22', '2021-06-24', '2021-06-26', '2021-06-28', '2021-06-30', '2021-07-02']
    packet = dict(status='ALL_15_SERIES_CHRONOLOGY_CANDIDATE_NOT_SELECTED_CALENDAR',
                  baseline_main='4b92e1191c9c36c78b5e1de18a6fa7941698c3f4', date='2026-10-04',
                  source_hash_convention='SHA256_UTF8_NO_BOM_LF_NORMALIZED',
                  source_sha256={p: sha(p) for p in (RESULTS, BRACKET, LEAGUE, DEN, 'simulation/DEN_LAL_2021_DELEGATED_SERIES.json')},
                  calendar_selected=False, new_author_decisions=0, season_selected=False,
                  manuscript_allowed=False, legal_execution_cleared=False, design_gate='CLOSED',
                  historical_source=dict(url=GUIDE, document_sha256='61613ab4d5d6868e406c0bae84d7f376256b96f4c5bd9e95012c20186a7132a5',
                                         printed_page=100, zero_based_page=99, access='DIRECT_PDF_TEXT_AND_RENDERED_PAGE',
                                         caveat='BKN May30 row misplaced in PHX block; PHX May27 row missing; NBA pages correct these. Historical G5 DEN-POR 2OT omitted by guide but separately verified.'),
                  corrections=[dict(url='https://www.nba.com/game/bkn-vs-bos-0042000114', claim='Historical BKN-BOS G4 May30 belongs in BKN block'),
                               dict(url='https://www.nba.com/game/phx-vs-lal-0042000153/box-score', claim='Historical PHX-LAL G3 May27 fills missing row')],
                  calendar_window_source=dict(url='https://official.nba.com/nba-announces-structure-and-format-for-2020-21-season/',
                                              claim='Nov17 2020 release tentative playoffs May22-Jul22 2021', access='DIRECT_OFFICIAL_PAGE'),
                  modeling_changes=['W6 replaces original DEN opponent by LAL and extends 4 to selected7 games on June15/17/19 candidates',
                                    'W7 first date shifts June20 to June22 to leave a non-game date after W6 June19; endsJuly2 candidate',
                                    'Original date skeletons for other series remain candidate, including changed first-round opponents'],
                  exclusions=['No historical scores, medical events, minute boxes or per-game winners copied',
                              'No venue/broadcast/travel/health/eligibility certification',
                              'Calendar date gaps are not hours of rest; Olympics readiness not certified',
                              'Candidate timings do not alter source exact_dates=null or F/A/K HOLD'], series=[])
    for s in result['series']:
        key = s['id']
        higher = homecourt_team(s, ranks, wins)
        games = []
        for i, dt in enumerate(dates[key]):
            games.append(dict(game=i+1, date_candidate=dt, date_selected=False,
                              home_team_candidate=higher if i in (0, 1, 4, 6) else next(t for t in s['teams'] if t != higher),
                              selected_game_winner=read('simulation/DEN_LAL_2021_DELEGATED_SERIES.json')['game_winners'][i] if key == 'W3' else None,
                              score=None, actual_overtime=None, health_verified=False,
                              eligibility_verified=False, venue_booking_verified=False,
                              historical_date_basis='2021-' + HISTORICAL[key][i] if i < len(HISTORICAL[key]) else None))
        parents = [dict(series=p, end_candidate=dates[p][-1], elapsed_calendar_days=(date.fromisoformat(dates[key][0])-date.fromisoformat(dates[p][-1])).days) for p in s['parents']]
        packet['series'].append(dict(id=key, teams=s['teams'], round=s['round'], parents=s['parents'],
                                     selected_winner=s['winner'], winner_wins=s['winner_wins'], loser_wins=s['loser_wins'],
                                     higher_homecourt_team_candidate=higher,
                                     homecourt_basis='F038 PHX51 > MIL46' if key == 'F1' else 'Existing selected bracket seed order',
                                     parent_gaps=parents, games=games))
    packet['checks'] = validate(packet)
    return packet


if __name__ == '__main__':
    packet = build()
    (ROOT / OUTPUT).write_text(json.dumps(packet, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(packet['checks']))
