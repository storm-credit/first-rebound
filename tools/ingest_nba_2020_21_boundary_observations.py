"""Reproduce the 29-game snapshot from the pinned public NBA V3 mirror CSVs."""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
import crosscheck_chicago_2020_21_impact as cc
import build_chicago_2020_21_standings_board as sb

S=cc.S
OUT=S/'NBA_2020_21_BOUNDARY_PAIRED_OBSERVATIONS.csv'
META=S/'NBA_2020_21_BOUNDARY_OBSERVATION_PROVENANCE.json'


def ingest(source_dir):
    raw=[];hashes={}
    for i in (1,2,3):
        p=source_dir/f'regular_season_box_scores_2010_2024_part_{i}.csv'
        hashes[p.name]=cc.sha(p)
        with p.open() as stream:
            raw.extend(r for r in csv.DictReader(stream) if r['season_year']=='2020-21')
    assert hashes == {
        'regular_season_box_scores_2010_2024_part_1.csv': 'ca9636d08c577e3d752f69e32f90b173f4c3374c15f4dc8494b655049fdfc557',
        'regular_season_box_scores_2010_2024_part_2.csv': '5643af8a9f15ce3540dced759375ca79e77c71644e23270136f23b7a57fc182d',
        'regular_season_box_scores_2010_2024_part_3.csv': '65a01fee3df865a272e578cf4b365dce7dbc62eef2ce6f15f0844cf6694ef375',
    }, 'Source differs from pinned mirror'
    assert len(raw)==len({(r['gameId'],r['teamTricode'],r['personId']) for r in raw})==28859
    baseline,_=sb.baseline()
    expected={(r['date'],r['home'],r['away']):(int(r['home_score']),int(r['away_score'])) for r in baseline}
    totals=defaultdict(lambda:defaultdict(int));identities={}
    for r in raw:
        m=r['matchup'].split();h,a=(m[0],m[2]) if m[1]=='vs.' else (m[2],m[0])
        key=(r['game_date'],h,a)
        totals[key][r['teamTricode']]+=int(float(r['points'] or 0))
        identities[key]=r['gameId'].zfill(10)
    assert len(totals)==len(set(identities.values()))==1080
    assert {(d,h,a):(v[h],v[a]) for (d,h,a),v in totals.items()}==expected
    queue=cc.read(S/'NBA_2020_21_NON_CHICAGO_CONTACT_SCREEN.csv')
    selected_ids={r['id'] for r in queue if r['review_priority']=='P1_BOUNDARY'}
    result=[]
    for r in raw:
        m=r['matchup'].split();h,a=(m[0],m[2]) if m[1]=='vs.' else (m[2],m[0])
        gid=f"{r['game_date']}_{h}_{a}"
        if gid not in selected_ids:continue
        result.append({'event_id':gid,'game_id':r['gameId'].zfill(10),'date':r['game_date'],
            'home':h,'away':a,'team':r['teamTricode'],'player':r['personName'],'person_id':r['personId'],
            'seconds':cc.seconds(r),'start':int(bool(r['position'])),'comment':r['comment'],
            'pts':int(float(r['points'] or 0)),'plus_minus':int(float(r['plusMinusPoints'] or 0)),
            'official_url':f"https://www.nba.com/game/{r['gameId'].zfill(10)}/box-score"})
    assert len(result)==776 and {r['event_id'] for r in result}==selected_ids and len(selected_ids)==29
    cc.write_csv(OUT,sorted(result,key=lambda r:(r['date'],r['team'],r['player'])))
    meta={'stage':'O-15F14-B','retrieved':'2026-09-10',
        'source_repository':'https://github.com/NocturneBear/NBA-Data-2010-2024',
        'commit':'a5f108b5b1f08074d78b9e8e901926a9ce4c06c5',
        'source_type':'Public NBA V3 mirror; not primary boxscore HTML extraction',
        'full_file_sha256':hashes,'all_2020_21_rows':len(raw),'all_1080_game_scores_match_O15F13_baseline':True,
        'selected_rows':len(result),'selected_games':29,'snapshot_sha256':cc.sha(OUT),
        'game_selection':'All O15F14A P1_BOUNDARY games, not only favorable Charlotte results',
        'primary_page_scope':'URLs identify NBA games. Numeric player rows are from the pinned public mirror.'}
    META.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    return meta


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path);args=p.parse_args()
    if args.source_dir:meta=ingest(args.source_dir)
    else:
        meta=json.loads(META.read_text())
        assert cc.sha(OUT)==meta['snapshot_sha256']
        assert len(cc.read(OUT))==meta['selected_rows']==776
    print('PASS: pinned source / 1080-score baseline / 29 selected games / 776 rows')
