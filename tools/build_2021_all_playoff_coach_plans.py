"""Apply source-linked author coach/health models to the 88 working dates."""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import date
import hashlib
import json
from pathlib import Path

import apply_2021_working_playoff_calendar as calendar_check
import apply_2021_dated_playoff_results as result_check
import build_den_lal_dated_coach_plan as preserved_check

ROOT = Path(__file__).resolve().parents[1]
CALENDAR = 'simulation/NBA_2021_WORKING_PLAYOFF_CALENDAR.json'
RESULTS = 'simulation/NBA_2021_DATED_PLAYOFF_RESULT_MODELS.json'
OLD = 'simulation/DEN_LAL_2021_DATED_COACH_PLAN.json'
AUTHORITY = 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
EAST = 'research/EAST_2021_PLAYOFF_COACH_INPUTS_2026_10_07.json'
WEST = 'research/WEST_2021_PLAYOFF_COACH_INPUTS_2026_10_07.json'
SOURCES = [CALENDAR, RESULTS, OLD, AUTHORITY, EAST, WEST]
OUT = 'simulation/NBA_2021_ALL_DATED_PLAYOFF_COACH_PLANS.json'


def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))


def sha(path):
    value = (ROOT/path).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(value.encode()).hexdigest()


def source_templates():
    east, west, old = read(EAST), read(WEST), read(OLD)
    for source in (east,west):
        if source['source_sha256'] != {p:sha(p) for p in source['source_sha256']}:
            raise ValueError('stale source-packet repository bridge')
        if source['authority']!=AUTHORITY:
            raise ValueError('source input design authority changed')
        def no_certification(value):
            keys={'medical_certified','health_clearance_certified','actual_active_list_certified',
                  'actual_registration_certified','actual_active_lists_certified',
                  'whole_health_cleared','season_selected','manuscript_allowed'}
            if isinstance(value,dict):
                if any(value.get(key) is True for key in keys):
                    raise ValueError('working source input falsely certifies actual/whole execution')
                for item in value.values(): no_certification(item)
            elif isinstance(value,list):
                for item in value:no_certification(item)
        no_certification(source)
    teams = deepcopy(east['teams'])
    if set(teams) & set(west['teams']):
        raise ValueError('input conference overlap')
    teams.update(deepcopy(west['teams']))
    for team in ('DEN', 'LAL'):
        first = old['games'][0]['teams'][team]['players']
        teams[team] = dict(**old['working_rosters'][team],
            blocks=[b[team] for b in old['games'][0]['blocks']],
            modeled_available=[p for p,r in first.items() if r['mode']=='MODELED_AVAILABLE_PLANNED_ROTATION'],
            modeled_absent=[p for p,r in first.items() if r['mode']=='MODELED_ABSENT'],
            health_anchor_evidence=[OLD], overrides_by_date={},
            continuation_selection='AUTHOR_MODELED_NO_NEW_CONTACT_INJURY_FOR_FOLLOWUP_DATES',
            continuation_reason='Keep selected DEN-LAL plan; explicitly choose no new contact injury for LAL June7-19. Original PHX-series Davis injury is not imported.')
    if set(teams) != {'PHI','IND','BKN','BOS','MIL','MIA','NYK','ATL','UTA','MEM','PHX','POR','DEN','LAL','LAC','DAL'}:
        raise ValueError('sixteen-team roster input required')
    global_names=Counter(p for source in teams.values() for p in source['standard']+source['two_way'])
    if any(count!=1 for count in global_names.values()):
        raise ValueError('same player registered to multiple playoff working teams')
    return teams


def inputs():
    return source_templates()


def profile(team, on_date):
    selected = {key: deepcopy(team[key]) for key in ('blocks','modeled_available','modeled_absent')}
    override = team.get('overrides_by_date',{}).get(on_date)
    if override:
        selected.update({key:deepcopy(override[key]) for key in selected if key in override})
    roster = team['standard']+team['two_way']
    if (len(roster)!=len(set(roster)) or len(team['standard'])>15 or len(team['two_way'])>2):
        raise ValueError('source working roster duplicates/capacity')
    available, absent = set(selected['modeled_available']),set(selected['modeled_absent'])
    if available & absent or not available|absent <= set(roster):
        raise ValueError('health model outside roster or contradictory')
    blocks=selected['blocks']
    if len(blocks)!=8 or any(len(b)!=5 or len(set(b))!=5 or not set(b)<=available for b in blocks):
        raise ValueError('eight unique-five available lineups required')
    if available != set().union(*(set(b) for b in blocks)):
        raise ValueError('rotation availability must match planned positive minutes')
    return selected


def validate_templates(teams, calendar):
    if teams!=source_templates():
        raise ValueError('working templates differ from complete preserved source input, including contract/health evidence')
    for team, source in teams.items():
        dates = [dict(series=g['series'],game=g['game'],date_model=g['date_model'])
                 for g in calendar['games'] if team in g['teams']]
        actual_dates={g['date_model'] for g in dates}
        if not set(source.get('overrides_by_date',{})) <= actual_dates:
            raise ValueError('unused override date silently drops selected recovery restriction')
        if 'linked_calendar_games' in source and source['linked_calendar_games']!=dates:
            raise ValueError('source team/date coverage differs from adopted calendar')
        if 'model_applicability_dates' in source:
            start,end=source['model_applicability_dates']
            if any(not start<=day<=end for day in actual_dates):
                raise ValueError('dated health model outside selected applicability range')


def render():
    teams, old = inputs(), read(OLD)
    calendar, results = read(CALENDAR), read(RESULTS)
    calendar_check.validate(calendar)
    result_check.validate(results)
    preserved_check.validate(old)
    validate_templates(teams,calendar)
    result_rows={(g['series'],g['game']):g for g in results['games']}
    old_rows={g['game']:g for g in old['games']}
    games, series_minutes, all_minutes = [],defaultdict(lambda:defaultdict(Counter)),defaultdict(Counter)
    workloads=defaultdict(list)
    for row in calendar['games']:
        sid, number, on_date = row['series'],row['game'],row['date_model']
        selected=result_rows[(sid,number)]
        if (selected['date_model'],selected['home_team'],selected['teams']) != (on_date,row['home_team'],row['teams']):
            raise ValueError('dated coach/result/calendar mismatch')
        blocks=[dict(start=i*6,end=(i+1)*6) for i in range(8)]
        game_teams={}
        for team in row['teams']:
            source=teams[team]
            chosen=profile(source,on_date)
            minutes=Counter(p for lineup in chosen['blocks'] for p in lineup)
            minutes=Counter({p:n*6 for p,n in minutes.items()})
            for i,lineup in enumerate(chosen['blocks']): blocks[i][team]=lineup
            players={}
            for kind in ('standard','two_way'):
                for player in source[kind]:
                    mode=('MODELED_AVAILABLE_PLANNED_ROTATION' if player in chosen['modeled_available'] else
                          'MODELED_ABSENT' if player in chosen['modeled_absent'] else 'COACH_ZERO_HEALTH_UNSELECTED')
                    players[player]=dict(contract_class=kind,mode=mode,planned_minutes=minutes.get(player,0),
                        health_model=None if mode=='COACH_ZERO_HEALTH_UNSELECTED' else 'AUTHOR_MODELED',
                        medical_certified=False,actual_active_list_certified=False)
                    workloads[(team,player)].append(dict(series=sid,game=number,date_model=on_date,
                        planned_minutes=minutes.get(player,0),mode=mode,contract_class=kind))
            game_teams[team]=dict(planned_minutes=dict(minutes),players=players)
            series_minutes[sid][team].update(minutes)
            all_minutes[team].update(minutes)
        game=dict(series=sid,game=number,date_model=on_date,home_team=row['home_team'],
            selected_winner=selected['winner_model'],working_date_adopted=True,
            duration_model_minutes=48,overtime_model_periods=0,blocks=blocks,teams=game_teams,
            actual_box=None,medical_health_verified=False,legal_registration_cleared=False,
            adoption='PRESERVED_SIX_GAME_PLAN' if sid=='W3' else 'NEW_DATED_AUTHOR_COACH_PLAN')
        if sid=='W3':
            reference=old_rows[number]
            if any(game[key]!=reference[key] for key in reference):
                raise ValueError('DEN-LAL preserved six-game plan changed')
        games.append(game)
    calendar_workloads=[]
    for (team,player), rows in sorted(workloads.items()):
        rows.sort(key=lambda r:r['date_model'])
        previous=None
        for row in rows:
            day=date.fromisoformat(row['date_model'])
            row['calendar_non_game_days_since_previous']=None if previous is None else (day-previous).days-1
            if previous is not None and day<=previous:
                raise ValueError('same-player duplicate date or reversed workload')
            previous=day
        calendar_workloads.append(dict(team=team,player=player,planned_minutes_total=sum(r['planned_minutes'] for r in rows),dates=rows))
    return dict(status='ALL_88_DATED_AUTHOR_COACH_HEALTH_PLANS_APPLIED_WHOLE_SEASON_HOLD',
        baseline_main='1401b7482f0a1ca8b5600bba70d403091344b2b4',date_local='2026-10-07',
        authority=AUTHORITY,source_sha256={p:sha(p) for p in SOURCES},
        working_rosters={t:{k:s[k] for k in ('standard','two_way')} for t,s in teams.items()},
        health_continuation_selection='PREPLAYOFF_CONSTRAINTS_AND_EXPLICIT_NO_NEW_CONTACT_INJURY_WORKING_MODEL',
        health_profile_sources={t:OLD if t in ('DEN','LAL') else EAST if t in read(EAST)['teams'] else WEST for t in teams},
        registration_assumption_sources={'WEST':read(WEST)['registration_assumptions'],
            'EAST_scope_boundaries':read(EAST)['scope_boundaries']},
        registration_assumptions={t:(dict(source=WEST,
            output_pointer='/registration_assumption_sources/WEST') if t in read(WEST)['teams'] else
            dict(source=EAST,output_pointer='/registration_assumption_sources/EAST_scope_boundaries')
            if t in read(EAST)['teams'] else dict(source=OLD,actual_registration_cleared=False)) for t in teams},
        roster_scope='SOURCE_LINKED_WORKING_ROSTER_WITH_EXPLICIT_CONDITIONAL_REGISTRATION_ASSUMPTIONS_NOT_COMPLETE_ACTUAL_REGISTER',
        new_exact_contract_selection=False,
        games=games,series_planned_minutes={s:{t:dict(v) for t,v in tv.items()} for s,tv in series_minutes.items()},
        team_total_planned_minutes={t:dict(v) for t,v in all_minutes.items()},player_dated_workloads=calendar_workloads,
        dated_games_applied=len(games),new_dated_coach_games_applied=82,preserved_dated_coach_games=6,
        joint_clock_blocks_applied=sum(len(g['blocks']) for g in games),
        roster_player_cells=sum(len(t['players']) for g in games for t in g['teams'].values()),
        playoff_working_health_and_coach_model_applied=True,
        medical_certified=False,actual_active_lists_certified=False,whole_league_health_cleared=False,
        legal_execution_cleared=False,season_selected=False,manuscript_allowed=False)


def validate(packet):
    expected=render()
    if packet!=expected:
        raise ValueError('dated plan differs from source-linked explicit working selection')
    if len(packet['games'])!=88 or len(packet['working_rosters'])!=16:
        raise ValueError('whole-playoff coverage missing')
    occupied=set()
    for game in packet['games']:
        for team in game['teams']:
            key=(team,game['date_model'])
            if key in occupied: raise ValueError('team plays twice same date')
            occupied.add(key)
            minute_total=sum(game['teams'][team]['planned_minutes'].values())
            if minute_total!=240 or max(game['teams'][team]['planned_minutes'].values())>48:
                raise ValueError('team/player shared-clock conservation')
    for sid, totals in packet['series_planned_minutes'].items():
        length=sum(g['series']==sid for g in packet['games'])
        if any(sum(v.values())!=length*240 for v in totals.values()):
            raise ValueError('series workload conservation')


def negative_tests(packet):
    first=next(i for i,g in enumerate(packet['games']) if g['series']!='W3')
    mutations=[lambda p:p['games'][first]['blocks'][0][p['games'][first]['teams'].keys().__iter__().__next__()].__setitem__(0,'Invented Player'),
        lambda p:p['games'][first]['blocks'][0].__setitem__('end',7),
        lambda p:p['games'][first]['teams'][p['games'][first]['teams'].keys().__iter__().__next__()].__setitem__('planned_minutes',{}),
        lambda p:p['games'][first].__setitem__('medical_health_verified',True),
        lambda p:p['games'][first].__setitem__('legal_registration_cleared',True),
        lambda p:p['games'].pop(),lambda p:p.__setitem__('season_selected',True),
        lambda p:p.__setitem__('whole_league_health_cleared',True),
        lambda p:p['player_dated_workloads'][0].__setitem__('planned_minutes_total',99999)]
    for mutate in mutations:
        candidate=deepcopy(packet);mutate(candidate)
        try:validate(candidate)
        except ValueError:continue
        raise AssertionError('invalid whole-playoff plan accepted')
    # A misplaced date previously vanished silently and applied default36
    # instead of the selected Mitchell24 recovery plan on May26.
    from unittest.mock import patch
    corrupted=inputs()
    overrides=corrupted['UTA']['overrides_by_date']
    overrides['2021-05-27']=overrides.pop('2021-05-26')
    try:
        with patch(__name__+'.inputs',return_value=corrupted):
            render()
    except ValueError:
        pass
    else:
        raise AssertionError('unused recovery override silently accepted')
    mutations=[lambda t:t['PHI']['standard'].__setitem__(t['PHI']['standard'].index('Paul Reed'),'Rayjon Tucker'),
        lambda t:t['IND'].__setitem__('health_anchor_evidence',[]),
        lambda t:t['PHI'].__setitem__('reserve_health','MEDICALLY_CERTIFIED'),
        lambda t:t['PHI'].__setitem__('actual_active_list_certified',True)]
    for mutate in mutations:
        corrupted=inputs();mutate(corrupted)
        try:
            with patch(__name__+'.inputs',return_value=corrupted):render()
        except ValueError:continue
        raise AssertionError('modified health/contract source template silently accepted')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    result=render();validate(result)
    if args.check:assert read(OUT)==result
    else:(ROOT/OUT).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.self_test:negative_tests(result)
    print(f"PASS: {result['dated_games_applied']} dated games / {result['joint_clock_blocks_applied']} shared blocks / {result['roster_player_cells']} roster cells; working health/coach applied, overall legal/season HOLD")
