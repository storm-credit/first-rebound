"""O-15F7: immutable observations and conditional box attribution, no outcomes.

--source-files accepts all three public mirror CSVs (or their 2020-21 subsets).
--write generates candidate attribution from saved evidence. Default verifies.
"""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'simulation'
SNAP=S/'CHICAGO_2020_21_POSTDEADLINE_BOTH_TEAMS_ACTUAL.csv'
RATES=S/'CHICAGO_2020_21_POSTDEADLINE_OBSERVED_PRIORS.csv'
META=S/'CHICAGO_2020_21_POSTDEADLINE_INPUT_PROVENANCE.json'
OUT=S/'CHICAGO_2020_21_POSTDEADLINE_BOX_INPUTS.json'
QUEUE=S/'CHICAGO_2020_21_POSTDEADLINE_OPPONENT_QUEUE.csv'
LINEUPS=S/'CHICAGO_2020_21_POSTDEADLINE_LINEUP_AUDIT.json'
CORE=S/'CHICAGO_2020_21_PREDEADLINE_PRODUCTION_PRIORS.csv'
ACTUAL=S/'CHICAGO_2020_21_POSTDEADLINE_ACTUAL.csv'
MIRROR='https://github.com/NocturneBear/NBA-Data-2010-2024'
HEAD='a5f108b5b1f08074d78b9e8e901926a9ce4c06c5'
METRICS={'pts':'points','reb':'reboundsTotal','ast':'assists','stl':'steals','blk':'blocks','tov':'turnovers','pf':'foulsPersonal'}
SHOTS={'fgm':'fieldGoalsMade','fga':'fieldGoalsAttempted','fg3m':'threePointersMade','fg3a':'threePointersAttempted','ftm':'freeThrowsMade','fta':'freeThrowsAttempted'}
FIELDS=METRICS|SHOTS

def read(p):return list(csv.DictReader(p.open()))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def seconds(r):return round(sum(float(v)*60**i for i,v in enumerate(reversed(r['minutes'].split(':'))))) if r['minutes'] else 0
def write(p,rows):
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)


def ingest(paths):
    raw=[r for p in paths for r in read(Path(p)) if r['season_year']=='2020-21']
    assert len(raw)==len({(r['gameId'],r['teamTricode'],r['personId']) for r in raw})
    assert len({r['gameId'] for r in raw})==1080 and len({r['teamTricode'] for r in raw})==30
    pre=[r for r in raw if r['game_date']<='2021-03-24']
    assert sum(seconds(r) for r in pre if r['teamTricode']=='CHI')==625202
    queue={r['game_id']:r for r in read(QUEUE)}
    selected=[r for r in raw if r['gameId'].zfill(10) in queue]
    snapshot=[]
    for r in sorted(selected,key=lambda r:(r['game_date'],r['teamTricode'],r['personName'])):
        gid=r['gameId'].zfill(10)
        snapshot.append({'event_id':queue[gid]['event_id'],'game_id':gid,'date':r['game_date'],'team':r['teamTricode'],
                         'player':r['personName'],'seconds':seconds(r),'start':int(bool(r['position'])),'comment':r['comment'],
                         **{k:int(float(r[v] or 0)) for k,v in FIELDS.items()},'plus_minus':int(float(r['plusMinusPoints'] or 0)),
                         'official_url':f'https://www.nba.com/game/{gid}/box-score'})
    names={r['player'] for r in snapshot}|{'Wendell Carter Jr.','Otto Porter Jr.','Saddiq Bey','Zeke Nnaji','Tyrell Terry','Norman Powell','Gary Harris','Aaron Gordon'}
    rates=[]
    for p in sorted(names):
        rows=[r for r in pre if r['personName']==p and seconds(r)>0]
        sec=sum(seconds(r) for r in rows)
        totals={k:sum(int(float(r[v] or 0)) for r in rows) for k,v in FIELDS.items()}
        rates.append({'player':p,'teams':';'.join(sorted({r['teamTricode'] for r in rows})),
                      'cutoff':'2021-03-24','last_observed_date':max((r['game_date'] for r in rows),default=''),
                      'gp':len(rows),'seconds':sec,**totals,
                      **{k+'36':round(totals[k]*2160/sec,8) if sec else '' for k in METRICS},
                      'sample_status':'NO_PREDEADLINE_SAMPLE' if not sec else 'LIMITED_UNDER_120_MIN' if sec<7200 else 'OBSERVED_NOT_CAUSAL'})
    write(SNAP,snapshot);write(RATES,rates)
    meta={'stage':'O-15F7','cutoff':'2021-03-24','mirror':MIRROR,'mirror_head_observed_after_download':HEAD,
          'source_urls':[f'{MIRROR}/blob/{HEAD}/regular_season_box_scores_2010_2024_part_{i}.csv' for i in (1,2,3)],
          'input_sha256':[sha(Path(p)) for p in paths],'input_scope':'2020-21 filtered mirror files',
          'snapshot_sha256':sha(SNAP),'rates_sha256':sha(RATES),'raw_season_rows':len(raw),
          'raw_season_games':1080,'chi_predeadline_seconds':625202,
          'note':'Secondary public NBA V3 mirror; official game-page identity checked, HTML did not expose full numeric boxes.'}
    META.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')


def build():
    rates={r['player']:r for r in read(RATES)}
    core={(r['player'],r['scenario']):r for r in read(CORE)}
    actual=defaultdict(dict)
    for r in read(ACTUAL):actual[r['date']][r['player']]=int(r['actual_seconds'])
    q={r['date']:r for r in read(QUEUE)}
    games=[];budget=defaultdict(lambda:defaultdict(float))
    for g in json.loads(LINEUPS.read_text())['games']:
        alt=g['minimum_change_candidate']['player_seconds'];base=dict(actual[g['date']])
        correction=g['clock_correction']
        if correction['player']:base[correction['player']]+=correction['seconds']
        assert sum(base.values())==14400
        players=sorted(set(base)|set(alt))
        for scenario in ('LOW','BASE','HIGH'):
            totals={name:{k:0.0 for k in METRICS} for name in ('expected_actual','expected_alternate','delta')}
            for p in players:
                old=base.get(p,0);new=alt.get(p,0)
                if p in ('Protagonist','LaMelo Ball'):
                    rating={k:float(core[(p,scenario)][k+'36']) for k in METRICS}
                    kind='PREDEADLINE_ROLE_PRIOR_CARRIED_FORWARD'
                else:
                    assert p in rates and rates[p]['seconds']!='0', p
                    rating={k:float(rates[p][k+'36']) for k in METRICS}
                    kind=rates[p]['sample_status']
                key=(g['scenario'],scenario,p,kind)
                budget[key]['actual_seconds']+=old;budget[key]['alternate_seconds']+=new
                for k in METRICS:
                    before=old/2160*rating[k];after=new/2160*rating[k]
                    totals['expected_actual'][k]+=before;totals['expected_alternate'][k]+=after;totals['delta'][k]+=after-before
                    budget[key]['expected_actual_'+k]+=before;budget[key]['expected_alternate_'+k]+=after
            games.append({'event_id':q[g['date']]['event_id'],'date':g['date'],'availability_scenario':g['scenario'],'production_scenario':scenario,
                          'status':'BOX_ATTRIBUTION_ONLY_OUTCOME_HOLD','clock_correction':correction,
                          **{name:{k:round(v,8) for k,v in values.items()} for name,values in totals.items()}})
    players=[{'availability_scenario':a,'production_scenario':s,'player':p,'rate_kind':kind,**{k:round(v,8) for k,v in values.items()}} for (a,s,p,kind),values in sorted(budget.items())]
    return {'stage':'O-15F7','status':'CONDITIONAL_BOX_INPUTS_NOT_SCORE_DELTAS',
            'input_sha256':{p.name:sha(p) for p in (SNAP,RATES,QUEUE,LINEUPS,CORE,ACTUAL)},'games':games,'player_budgets':players}


def verify(data):
    meta=json.loads(META.read_text())
    assert meta['snapshot_sha256']==sha(SNAP) and meta['rates_sha256']==sha(RATES)
    queue=read(QUEUE);snap=read(SNAP);rates=read(RATES)
    assert len(queue)==29 and len({r['opponent'] for r in queue})==19
    assert len(snap)==len({(r['game_id'],r['team'],r['player']) for r in snap})
    observed={(r['date'],r['player']):r for r in snap if r['team']=='CHI'}
    old=read(ACTUAL)
    assert set(observed)=={(r['date'],r['player']) for r in old}
    for r in old:
        x=observed[(r['date'],r['player'])]
        assert int(x['seconds'])==int(r['actual_seconds']) and int(x['pts'])==int(r['points'])
        assert x['start']==r['actual_start'] and x['comment']==r['comment'] and x['plus_minus']==r['plus_minus']
    assert sum(q['opponent_input_status']!='NO_NEW_DIRECT_CHANGE_IDENTIFIED' for q in queue)==10
    for q in queue:
        for ref in q['canon_evidence'].split(';'):assert (ROOT/ref).is_file(), ref
        assert q['alternate_opponent_minutes_status']=='NOT_ALLOCATED' and q['outcome_status']=='HOLD'
        contact_names=set(q['named_contact_players'].split(';'))
        exposure=sum(int(r['seconds']) for r in snap if r['game_id']==q['game_id'] and r['team']==q['opponent'] and r['player'] in contact_names)
        assert int(q['named_actual_contact_seconds'])==exposure
        rows=[r for r in snap if r['game_id']==q['game_id']]
        assert {r['team'] for r in rows}=={'CHI',q['opponent']}
        team_points={}
        for team in ('CHI',q['opponent']):
            rs=[r for r in rows if r['team']==team]
            assert abs(sum(int(r['seconds']) for r in rs)-14400)<=2
            assert sum(int(r['start']) for r in rs)==5
            team_points[team]=sum(int(r['pts']) for r in rs)
            for r in rs:
                assert int(r['pts'])==2*int(r['fgm'])+int(r['fg3m'])+int(r['ftm'])
        for team,other in (('CHI',q['opponent']),(q['opponent'],'CHI')):
            assert sum(int(r['plus_minus']) for r in rows if r['team']==team)==5*(team_points[team]-team_points[other])
    for r in rates:
        assert r['cutoff']=='2021-03-24' and r['last_observed_date']<='2021-03-24'
        sec=int(r['seconds'])
        for k in METRICS:
            if sec:assert abs(float(r[k+'36'])-int(r[k])*2160/sec)<1e-7
            else:assert r[k+'36']==''
    assert data==build()
    assert len(data['games'])==174
    for g in data['games']:
        for k in METRICS:
            assert abs(g['expected_alternate'][k]-g['expected_actual'][k]-g['delta'][k])<1e-6
    print(f'PASS: {len(snap)} observed player rows, 29 paired games, {len(rates)} cutoff priors, 174 conditional box inputs; no outcomes')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-files',nargs=3);parser.add_argument('--write',action='store_true');args=parser.parse_args()
    if args.source_files:ingest(args.source_files)
    data=build() if args.write else json.loads(OUT.read_text());verify(data)
    if args.write:OUT.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
