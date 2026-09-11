"""O-15F14-E: 939-game policy/availability queue, seven-path rescreen, 80 close games.
No outcome prediction in this screen. Source ingest is separate from impact calculation.
"""
import argparse
import csv
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
import build_chicago_2020_21_remaining_impact as d

S=d.S
OUT=S/'NBA_2020_21_POLICY_SCREEN.json'
QUEUE=S/'NBA_2020_21_POLICY_GAME_QUEUE.csv'
TEAM_QUEUE=S/'NBA_2020_21_POLICY_TEAM_QUEUE.csv'
OBS=S/'NBA_2020_21_FINAL_CLOSE_OBSERVATIONS.csv'
META=S/'NBA_2020_21_FINAL_CLOSE_PROVENANCE.json'
ALL_OBS_META=S/'NBA_2020_21_BOUNDARY_OBSERVATION_PROVENANCE.json'


def policy(team,day):
    post=day>='2021-03-25'
    # Phase boundary flags transaction review, not proof of same-day eligibility.
    rules={
        'MIN':('MIN_RIVAL','DIRECT_ROSTER_CONTACT','Fictional Rival','Anthony Edwards','EX07'),
        'CHA':('CHA_EDWARDS_TERRY','DIRECT_ROSTER_CONTACT','Anthony Edwards;Tyrell Terry','LaMelo Ball;Grant Riller','EX07'),
        'DET':('DET_PATRICK_KIRA','DIRECT_ROSTER_CONTACT','Patrick Williams;Kira Lewis Jr.','Saddiq Bey;Killian Hayes','EX07'),
        'NOP':('NOP_HAYES','DIRECT_ROSTER_CONTACT','Killian Hayes','Kira Lewis Jr.','EX07'),
        'DAL':('DAL_HAMPTON','DIRECT_ROSTER_CONTACT','R.J. Hampton','Tyrell Terry','EX07'),
        'DEN':('DEN_GORDON_A' if post else 'DEN_BEY_NNAJI','DIRECT_ROSTER_CONTACT','Saddiq Bey','R.J. Hampton;Zeke Nnaji;Gary Harris' if post else 'R.J. Hampton','EX02;EX07' if post else 'EX07'),
        'WAS':('WAS_TRENT_BROWN' if post else 'WAS_TRENT','DIRECT_ROSTER_CONTACT','Gary Trent Jr.;Troy Brown Jr.' if post else 'Gary Trent Jr.','Isaac Bonga;Chandler Hutchison','EX01;EX07' if post else 'EX07'),
        'POR':('POR_NO_POWELL_HOOD' if post else 'POR_NO_TRENT','DIRECT_ROSTER_CONTACT','Rodney Hood' if post else '', 'Gary Trent Jr.;Norman Powell','EX05;EX07' if post else 'EX07'),
        'GSW':('GSW_WIGGINS_HUTCHISON_INACTIVE','TRANSACTION_DEPENDENCY','','','EX06;EX07'),
        'LAL':('LAL_AD_CORE','TRANSACTION_DEPENDENCY','','','EX06;EX07')}
    if post:
        rules['ORL']=('ORL_VUCEVIC_GORDON_A','DIRECT_ROSTER_CONTACT','Nikola Vucevic;Zeke Nnaji','Wendell Carter Jr.;Otto Porter Jr.;R.J. Hampton','EX02;EX03;EX04;EX07')
        rules['TOR']=('TOR_POWELL','DIRECT_ROSTER_CONTACT','Norman Powell','Gary Trent Jr.;Rodney Hood','EX05;EX07')
        rules['BOS']=('BOS_FOURNIER_PATH','TRANSACTION_DEPENDENCY','','','EX01;EX03;EX04;EX07')
    pid,contact,added,removed,ex=rules.get(team,('INCUMBENT_CONDITIONAL','NO_DIRECT_DELTA_IDENTIFIED','','','EX07'))
    return {'policy_id':pid,'contact':contact,'conditional_newcomers':added,'removed_players':removed,'execution_conditions':ex,
            'phase':'DEADLINE_REVIEW' if post else 'PREDEADLINE', 'minute_allocation_status':'NOT_CALCULATED',
            'incumbent_rule':'observed date availability and incumbent transactions conditional; no new injury/event selected'}


def ingest(source_dir):
    expected=json.loads(ALL_OBS_META.read_text())
    pending={r['id'] for r in d.bi.cc.read(d.PENDING)}
    rows=[]
    for name,h in expected['full_file_sha256'].items():
        path=source_dir/name
        assert d.bi.cc.sha(path)==h,(name,'source hash mismatch')
        with path.open() as f:
            for r in csv.DictReader(f):
                if r['season_year']!='2020-21':continue
                m=r['matchup'].split();home,away=(m[0],m[2]) if m[1]=='vs.' else (m[2],m[0])
                gid=f"{r['game_date']}_{home}_{away}"
                rows.append({'event_id':gid,'game_id':r['gameId'].zfill(10),'date':r['game_date'],'home':home,'away':away,
                    'team':r['teamTricode'],'player':r['personName'],'person_id':r['personId'],'seconds':d.bi.cc.seconds(r),
                    'start':int(bool(r['position'])),'comment':r['comment'],'pts':int(float(r['points'] or 0)),
                    'plus_minus':int(float(r['plusMinusPoints'] or 0)),
                    'official_url':f"https://www.nba.com/game/{r['gameId'].zfill(10)}/box-score"})
    baseline={g['id']:g for g in d.bi.lb.normalized_games()}
    assert len(rows)==len({(r['event_id'],r['team'],r['person_id']) for r in rows})
    score=defaultdict(Counter);group=defaultdict(list)
    for r in rows:
        score[r['event_id']][r['team']]+=r['pts'];group[r['event_id'],r['team']].append(r)
    assert set(score)==set(baseline) and len(score)==1080
    for gid,g in baseline.items():
        assert abs(score[gid][g['home']]-score[gid][g['away']])==g['margin']
        assert max(score[gid],key=score[gid].get)==g['winner']
    teams=[]
    for gid in sorted(pending):
        g=baseline[gid]
        for t in (g['home'],g['away']):
            observed=group[gid,t];p=policy(t,g['date'])
            names={r['player'] for r in observed}
            teams.append({'event_id':gid,'date':g['date'],'team':t,**p,
                'observation_rows':len(observed),'observed_seconds':sum(r['seconds'] for r in observed),
                'positive_minute_players':sum(r['seconds']>0 for r in observed),
                'coach_dnp_players':';'.join(sorted(r['player'] for r in observed if r['comment']=="DNP - Coach's Decision")),
                'injury_protocol_dnp_players':';'.join(sorted(r['player'] for r in observed if r['seconds']==0 and any(x in r['comment'].lower() for x in ['injury','illness','protocol']))),
                'conditional_newcomers_without_row':';'.join(n for n in p['conditional_newcomers'].split(';') if n and n not in names),
                'observed_source_game_id':observed[0]['game_id']})
    close={gid for gid in pending if baseline[gid]['margin']<=3}
    selected=sorted([r for r in rows if r['event_id'] in close],key=lambda r:(r['event_id'],r['team'],r['player']))
    d.bi.cc.write_csv(OBS,selected);d.bi.cc.write_csv(TEAM_QUEUE,teams)
    meta={'stage':'O-15F14-E','source_commit':expected['commit'],'source_sha256':expected['full_file_sha256'],
        'all_baseline_games_checked':1080,'all_season_rows':len(rows),'pending_games':len(pending),
        'pending_observation_rows':sum(t['observation_rows'] for t in teams),
        'team_exposures':len(teams),'close_games':len(close),'close_rows':len(selected),
        'snapshot_sha256':d.bi.cc.sha(OBS),'team_queue_sha256':d.bi.cc.sha(TEAM_QUEUE),
        'upstream_pending_sha256':d.bi.cc.sha(d.PENDING),'selected':False,
        'scope':'939 availability observations indexed; only80 close games exported. Availability data is actual-world evidence, not alternate health approval.'}
    META.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    return meta


def rescreen():
    upstream=json.loads(d.OUT.read_text());actual=d.bi.lb.normalized_games()
    pending={r['id']:r for r in d.bi.cc.read(d.PENDING)}
    queue={gid:{'event_id':gid,'date':r['date'],'home':r['home'],'away':r['away'],'actual_margin':int(r['margin']),
                'home_policy':policy(r['home'],r['date'])['policy_id'],'away_policy':policy(r['away'],r['date'])['policy_id'],
                'contact_status':r['contact_status'],'direct_seed_cases':[],'playin_field_cases':[],
                'chicago_rank_cases':[],'seed_order_cases':[],'draft_record_group_cases':[],'later_tie_cases':[]}
           for gid,r in pending.items()}
    cases=[]
    for case in upstream['league_cases']:
        changed=set(case['changed_game_ids'])
        games=[d.bi.lb.changed_game(g) if g['id'] in changed else dict(g) for g in actual]
        base=d.ps.order(games);basewins=d.bi.lb.record_wins(games)
        recordgroups=d.ps.record_groups(d.ps.ALL,basewins)
        basegroups={t:(tuple(g['teams']),tuple(g['positions'])) for g in recordgroups for t in g['teams']}
        counts=Counter();witnesses={}
        for i,g in enumerate(games):
            if g['id'] not in pending:continue
            q=queue[g['id']];games[i]=d.bi.lb.changed_game(g)
            wins=d.bi.lb.record_wins(games)
            assert sum(wins.values())==1080 and wins['CHI']==basewins['CHI']
            newgroups={t:(tuple(group['teams']),tuple(group['positions'])) for group in d.ps.record_groups(d.ps.ALL,wins) for t in group['teams']}
            if newgroups!=basegroups:
                q['draft_record_group_cases'].append(case['id']);counts['draft_record_groups']+=1
            try:
                alt=d.ps.order(games)
                labels=[]
                if any(set(alt[c][:6])!=set(base[c][:6]) for c in base):labels.append('direct_seed')
                if any(set(alt[c][:10])!=set(base[c][:10]) for c in base):labels.append('playin_field')
                if alt['EAST'].index('CHI')!=base['EAST'].index('CHI'):labels.append('chicago_rank')
                if alt!=base:labels.append('seed_order')
                for label in labels:
                    q[label+'_cases'].append(case['id']);counts[label]+=1
                    if label not in witnesses:
                        witnesses[label]={'event_id':g['id'],'actual_winner':g['winner'],'hypothetical_winner':games[i]['winner'],
                                          'seeds':alt,'selected':False}
            except ValueError as e:
                q['later_tie_cases'].append(case['id']);counts['later_tie']+=1
                witnesses.setdefault('later_tie',{'event_id':g['id'],'reason':str(e),'selected':False})
            games[i]=g
        cases.append({'id':case['id'],'hypothetical_single_flip_trials':len(pending),'counts':dict(counts),
                      'witnesses':witnesses,'selected':False})
    rows=[]
    for q in queue.values():
        boundary=bool(q['direct_seed_cases'] or q['playin_field_cases'] or q['chicago_rank_cases'] or q['later_tie_cases'])
        close=q['actual_margin']<=3
        rows.append({**{k:';'.join(v) if isinstance(v,list) else v for k,v in q.items()},
            'priority':'CLOSE80_PAIRED_INPUT' if close else 'LARGE_MARGIN_BOUNDARY' if boundary else 'REMAINING_SEASON_POLICY',
            'impact_status':'NOT_CALCULATED','selected':False})
    result={'stage':'O-15F14-E','status':'POLICY_AND_SEVEN_PATH_SCREEN_COMPLETE_NOT_IMPACT',
        'source_cases':len(cases),'single_flip_trials':len(cases)*len(pending),'cases':cases,
        'priority_counts':dict(Counter(r['priority'] for r in rows)),
        'any_boundary_games':sum(bool(r['direct_seed_cases'] or r['playin_field_cases'] or r['chicago_rank_cases'] or r['later_tie_cases']) for r in rows),
        'any_seed_order_games':sum(bool(r['seed_order_cases']) for r in rows),
        'any_draft_record_group_games':sum(bool(r['draft_record_group_cases']) for r in rows),
        'draft_scope':'30-team regular-season equal-record groups and positions; not the final14-team lottery field, odds or draw',
        'scope':'Single flips are hypothetical sensitivity, not inferred margins. No multi-flip safety guarantee.',
        'upstream_sha256':{p.name:d.bi.cc.sha(p) for p in (d.OUT,d.PENDING,Path(__file__))},'manuscript_allowed':False}
    return result,rows


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path);p.add_argument('--write-screen',action='store_true');a=p.parse_args()
    if a.source_dir:print(json.dumps(ingest(a.source_dir)))
    if a.write_screen:
        data,rows=rescreen();OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');d.bi.cc.write_csv(QUEUE,rows)
        print(json.dumps({k:v for k,v in data.items() if k not in ('cases','upstream_sha256')}))
    if not a.source_dir and not a.write_screen:
        data,rows=rescreen();assert data==json.loads(OUT.read_text())
        assert d.bi.cc.read(QUEUE)==[{k:str(v) for k,v in row.items()} for row in rows]
        m=json.loads(META.read_text());assert d.bi.cc.sha(OBS)==m['snapshot_sha256'] and d.bi.cc.sha(TEAM_QUEUE)==m['team_queue_sha256']
        print('PASS policy screen and source hashes')
