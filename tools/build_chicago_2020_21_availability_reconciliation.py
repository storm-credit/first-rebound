"""H: adopted direction scope and observed evidence for target-date availability.
Observations are historical; no injury is transferred between alternate teams.
"""
import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
import build_chicago_2020_21_author_packet as g

S=g.f.S
ROOT=S.parent
APPROVAL=ROOT/'canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json'
OBS=S/'NBA_2020_21_MOVED_PLAYER_OBSERVATIONS.csv'
META=S/'NBA_2020_21_MOVED_PLAYER_PROVENANCE.json'
CAL=S/'CHICAGO_2020_21_AVAILABILITY_RECONCILIATION.csv'
OUT=S/'CHICAGO_2020_21_EXECUTION_ADOPTION.json'
CHI_WATCH=['LaMelo Ball','Wendell Carter Jr.','Otto Porter Jr.','Fictional Protagonist']
FICTIONAL={'Fictional Rival','Fictional Protagonist'}


def ingest(folder):
    packet=json.loads(g.OUT.read_text())
    players={x['player'] for x in packet['conditional_target_calendar']}|set(CHI_WATCH)
    original=json.loads(g.f.e.queue.ALL_OBS_META.read_text())
    rows=[]
    for name,digest in original['full_file_sha256'].items():
        path=folder/name
        assert g.f.bi.cc.sha(path)==digest
        for r in g.f.bi.cc.read(path):
            if r['season_year']!='2020-21' or r['personName'] not in players:continue
            a,separator,b=r['matchup'].split()
            home,away=(a,b) if separator=='vs.' else (b,a)
            rows.append({'event_id':f"{r['game_date']}_{home}_{away}",
                'game_id':r['gameId'].zfill(10),'date':r['game_date'],'team':r['teamTricode'],
                'player':r['personName'],'person_id':r['personId'],
                'seconds':g.f.bi.cc.seconds(r),'comment':r['comment'],
                'official_reference_url':f"https://www.nba.com/game/{r['gameId'].zfill(10)}/box-score"})
    rows.sort(key=lambda r:(r['player'],r['date'],r['event_id']))
    assert len(rows)==len({(r['person_id'],r['game_id']) for r in rows})
    g.f.bi.cc.write_csv(OBS,rows)
    meta={'source_repository':original['source_repository'],'source_commit':original['commit'],
        'full_file_sha256':original['full_file_sha256'],'snapshot_sha256':g.f.bi.cc.sha(OBS),
        'rows':len(rows),'players':len({r['person_id'] for r in rows}),
        'scope':'Pinned public NBA V3 mirror extraction, not fresh primary-page extraction. Missing rows do not prove inactivity or health.'}
    META.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')


def status(row):
    if int(row['seconds'])>0:return 'SAME_DAY_PLAYED'
    if row['comment']=="DNP - Coach's Decision":return 'SAME_DAY_COACH_DNP'
    if any(x in row['comment'].lower() for x in ('injury','illness','not with team','suspension','protocol')):
        return 'SAME_DAY_RESTRICTED'
    return 'SAME_DAY_OTHER_ZERO'


def build():
    packet=json.loads(g.OUT.read_text());approval=json.loads(APPROVAL.read_text())
    source=g.f.bi.cc.read(OBS);byplayer=defaultdict(list)
    for r in source:byplayer[r['player']].append(r)
    for rows in byplayer.values():rows.sort(key=lambda r:r['date'])
    schedule={x['id']:x for x in g.f.bi.lb.normalized_games()}
    requests=[('NEW_TEAM_TARGET',x['team'],x['player'],gid)
              for x in packet['conditional_target_calendar'] for gid in x['event_ids']]
    requests += [('CHI_WATCH_ONLY','CHI',p,gid) for p in CHI_WATCH for gid,x in schedule.items()
                 if 'CHI' in (x['home'],x['away'])]
    calendar=[]
    for scope,team,player,gid in sorted(requests):
        day=schedule[gid]['date'];rows=byplayer[player]
        same=[r for r in rows if r['date']==day];assert len(same)<=1
        before=[r for r in rows if r['date']<day];after=[r for r in rows if r['date']>day]
        previous=before[-1] if before else None;following=after[0] if after else None
        evidence=status(same[0]) if same else ('FICTIONAL_NO_OBSERVATIONS' if player in FICTIONAL else 'NO_SAME_DAY_ROW')
        gap=(date.fromisoformat(following['date'])-date.fromisoformat(previous['date'])).days if previous and following else None
        edge_gap=abs((date.fromisoformat(day)-date.fromisoformat((previous or following)['date'])).days) if bool(previous)!=bool(following) else None
        priority='RESTRICTED_SOURCE_REVIEW' if evidence=='SAME_DAY_RESTRICTED' else (
            'LONG_OBSERVATION_GAP_REVIEW' if evidence=='NO_SAME_DAY_ROW' and gap and gap>14 else (
            'OPEN_ENDED_OBSERVATION_GAP_REVIEW' if evidence=='NO_SAME_DAY_ROW' and edge_gap and edge_gap>14 else 'NO_AUTOMATIC_HEALTH_INFERENCE'))
        calendar.append({'scope':scope,'event_id':gid,'date':day,'team':team,'player':player,
            'historical_evidence':evidence,'source_game_id':same[0]['game_id'] if same else '',
            'source_team':same[0]['team'] if same else '',
            'source_seconds':same[0]['seconds'] if same else '',
            'source_comment':same[0]['comment'] if same else '',
            'previous_source_date':previous['date'] if previous else '',
            'next_source_date':following['date'] if following else '',
            'bracketing_observation_gap_days':gap if gap is not None else '',
            'edge_observation_distance_days':edge_gap if edge_gap is not None else '',
            'priority':priority,'alternate_availability':'NOT_SELECTED',
            'action':'Review causal health/registration separately; never map missing row to healthy or injured'})
    summaries=[]
    for scope,team,player in sorted({(r['scope'],r['team'],r['player']) for r in calendar}):
        rr=[r for r in calendar if (r['scope'],r['team'],r['player'])==(scope,team,player)]
        historical=byplayer[player]
        summaries.append({'scope':scope,'team':team,'player':player,'dates':len(rr),
            'historical_source_rows':len(historical),'historical_positive_games':sum(int(r['seconds'])>0 for r in historical),
            'evidence_counts':dict(sorted(Counter(r['historical_evidence'] for r in rr).items())),
            'priority_counts':dict(sorted(Counter(r['priority'] for r in rr).items()))})
    queue=[{'scope':r['scope'],'team':r['team'],'player':r['player'],'event_id':r['event_id'],
            'priority':r['priority']} for r in calendar if r['priority']!='NO_AUTOMATIC_HEALTH_INFERENCE']
    data={'stage':'O-15F14-H','status':'DIRECTIONS_ADOPTED_AVAILABILITY_EVIDENCE_RECONCILED',
        'approved_direction_ids':list(approval['approved']),
        'approval_sha256':g.f.bi.cc.sha(APPROVAL),
        'candidate_rating_and_method_not_author_locked':True,
        'source_snapshot_sha256':g.f.bi.cc.sha(OBS),'source_metadata_sha256':g.f.bi.cc.sha(META),
        'upstream_candidate_sha256':g.f.bi.cc.sha(g.OUT),'upstream_full_season_sha256':g.f.bi.cc.sha(g.f.OUT),
        'generator_sha256':g.f.bi.cc.sha(Path(__file__)),
        'calendar_rows':len(calendar),'scope_counts':dict(Counter(r['scope'] for r in calendar)),
        'player_summary':summaries,'priority_queue':queue,
        'priority_game_ids':sorted({r['event_id'] for r in queue}),
        'contract_facts':{'new_exact_salary_or_pick_terms_recovered':False,
            'charge_matching':'HOLD','pick_obligation_terms':'HOLD',
            'direction_approval_is_not_execution_clearance':True},
        'rules':['Positive actual play is evidence on that date only, not alternate fitness or target minutes.',
            'Coach DNP is not a medical absence; zero minutes with another reason remain separate.',
            'No same-day row may reflect another schedule, inactive-list omission, roster change or missing data.',
            'A bracketing gap greater than14 days is a review priority only; no injury episode or recovery date is inferred.',
            'Open-ended missing records more than14 days from the last/first observation remain review priorities; no season-ending diagnosis is inferred.',
            'CHI watch rows do not assert positive target minutes on all72 dates.',
            'The priority queue does not exempt other dates or incumbent followup contracts.',
            'G remains the immutable pre-approval packet; current approval authority is the separate canon record.'],
        'next':'Reconcile priority causal health/registration episodes and T5 followups; revise affected dates only, then assess final season selection.',
        'season_selected':False,'manuscript_allowed':False}
    return data,calendar


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path);p.add_argument('--write',action='store_true');a=p.parse_args()
    if a.source_dir:ingest(a.source_dir)
    data,calendar=build()
    if a.write:
        g.f.bi.cc.write_csv(CAL,calendar)
        data['calendar_sha256']=g.f.bi.cc.sha(CAL)
        OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    else:
        data['calendar_sha256']=g.f.bi.cc.sha(CAL)
        assert json.loads(OUT.read_text())==data
        assert g.f.bi.cc.read(CAL)==[{k:str(v) for k,v in r.items()} for r in calendar]
    print(json.dumps({'PASS':True,'calendar_rows':len(calendar),'scopes':data['scope_counts'],
        'priority_rows':len(data['priority_queue']),'priority_games':len(data['priority_game_ids'])}))
