"""Extract the 40 remaining close boundary games from the same pinned source."""
import argparse,csv,json
from pathlib import Path
import build_chicago_2020_21_postseason_routes as pr
import ingest_nba_2020_21_boundary_observations as prior
S=pr.S
OUT=S/'NBA_2020_21_REMAINING_BOUNDARY_OBSERVATIONS.csv'
META=S/'NBA_2020_21_REMAINING_BOUNDARY_PROVENANCE.json'

def ingest(source):
    queue=pr.bi.cc.read(pr.QUEUE)
    ids={r['id'] for r in queue if r['priority']=='BOUNDARY_OR_TIE_REVIEW' and int(r['margin'])<=3}
    expected=json.loads(prior.META.read_text())['full_file_sha256'];rows=[]
    baseline={g['id']:g for g in pr.bi.lb.normalized_games()}
    for name,h in expected.items():
        p=source/name;assert pr.bi.cc.sha(p)==h
        with p.open() as f:
            for r in csv.DictReader(f):
                if r['season_year']!='2020-21':continue
                m=r['matchup'].split();home,away=(m[0],m[2]) if m[1]=='vs.' else (m[2],m[0])
                gid=f"{r['game_date']}_{home}_{away}"
                if gid not in ids:continue
                rows.append({'event_id':gid,'game_id':r['gameId'].zfill(10),'date':r['game_date'],
                    'home':home,'away':away,'team':r['teamTricode'],'player':r['personName'],'person_id':r['personId'],
                    'seconds':pr.bi.cc.seconds(r),'start':int(bool(r['position'])),'comment':r['comment'],
                    'pts':int(float(r['points'] or 0)),'plus_minus':int(float(r['plusMinusPoints'] or 0)),
                    'official_url':f"https://www.nba.com/game/{r['gameId'].zfill(10)}/box-score"})
    assert len(ids)==40 and {r['event_id'] for r in rows}==ids
    assert len(rows)==len({(r['event_id'],r['team'],r['person_id']) for r in rows})
    for gid in ids:
        g=baseline[gid];score={t:sum(r['pts'] for r in rows if r['event_id']==gid and r['team']==t) for t in (g['home'],g['away'])}
        assert abs(score[g['home']]-score[g['away']])==g['margin']
        assert max(score,key=score.get)==g['winner']
    pr.bi.cc.write_csv(OUT,sorted(rows,key=lambda r:(r['event_id'],r['team'],r['player'])))
    meta={'stage':'O-15F14-C','source_commit':json.loads(prior.META.read_text())['commit'],
        'source_provenance':prior.META.name,'source_sha256':expected,'queue_sha256':pr.bi.cc.sha(pr.QUEUE),
        'snapshot_sha256':pr.bi.cc.sha(OUT),'games':40,'rows':len(rows),'selected':False,
        'scope':'All <=3 point remaining boundary games. Observations ready; new impacts NOT_CALCULATED.'}
    META.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');return meta

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path);a=p.parse_args()
    if a.source_dir:m=ingest(a.source_dir)
    else:
        m=json.loads(META.read_text());assert pr.bi.cc.sha(OUT)==m['snapshot_sha256'] and pr.bi.cc.sha(pr.QUEUE)==m['queue_sha256']
        assert len(pr.bi.cc.read(OUT))==m['rows']
    print(json.dumps({'PASS':True,'games':m['games'],'rows':m['rows']}))
