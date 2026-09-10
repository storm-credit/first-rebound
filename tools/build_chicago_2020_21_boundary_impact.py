"""O-15F14-B: paired conditional impact for all 29 priority games.
New minute policies are constructed without consulting impact ratings or results.
"""
import argparse
import csv
import itertools
import json
from collections import defaultdict
from datetime import date
from pathlib import Path
import crosscheck_chicago_2020_21_impact as cc
import build_chicago_2020_21_integrated_paths as ip
import build_chicago_2020_21_league_boundaries as lb

S = cc.S
OBS = S / 'NBA_2020_21_BOUNDARY_PAIRED_OBSERVATIONS.csv'
OUT = S / 'CHICAGO_2020_21_BOUNDARY_PAIRED_IMPACT.json'
METHODS = ('RAPTOR_RS_EB', 'BPM_MAR25_EB')
PROFILES = ('LOW_MINUTES', 'HIGH_MINUTES')
ROLES = {t: {k: list(v) for k,v in roles.items()} for t,roles in ip.ROLES.items() if t in ('CHA','WAS','DET','DEN','NOP')}
ROLES['CHA']['handler'] += ['Brad Wanamaker']
ROLES['CHA']['center'] += ['Vernon Carey Jr.', 'Nick Richards']
ROLES['CHA']['wing'] += ['Jalen McDaniels', 'Nate Darling']
ROLES['DET']['handler'] += ['Cory Joseph']
ROLES['DET']['center'] += ['Jahlil Okafor', 'Tyler Cook']
ROLES['DET']['wing'] += ['Hamidou Diallo', 'Deividas Sirvydis']
ROLES['WAS']['center'] += ['Daniel Gafford']
ROLES['WAS']['wing'] += ['Troy Brown Jr.', 'Jerome Robinson']
ROLES['NOP']['wing'] += ['James Johnson', 'Naji Marshall', 'Wes Iwundu', 'Wenyen Gabriel']
ROLES['TOR'] = {
    'handler': ['Fred VanVleet','Kyle Lowry','Malachi Flynn','Jalen Harris',"DeAndre' Bembry",'Pascal Siakam'],
    'center': ['Khem Birch','Freddie Gillespie','Chris Boucher','Aron Baynes'],
    'wing': ['Norman Powell','Stanley Johnson','Yuta Watanabe','O.G. Anunoby',"DeAndre' Bembry"]}


def groups():
    result = defaultdict(list)
    for r in cc.read(OBS):
        result[(r['event_id'], r['team'])].append(r)
    return result


def baseline(rows):
    raw = {r['player']: int(r['seconds']) for r in rows if int(r['seconds'])}
    raw_sum = sum(raw.values())
    ot = round((raw_sum-14400)/1500)
    duration = 2880 + 300*ot
    assert ot >= 0 and abs(raw_sum-5*duration) <= 2
    correction = 5*duration-raw_sum
    fixed = max(raw,key=lambda p:(raw[p],p)) if correction else None
    base = raw.copy()
    if fixed:
        base[fixed] += correction
    return base, duration, {'player':fixed,'seconds':correction,'raw_total_seconds':raw_sum}


def allowed(rows):
    return {r['player'] for r in rows if int(r['seconds']) > 0 or r['comment'] == "DNP - Coach's Decision"}


def policies(team, day, high):
    if team == 'CHA':
        return ['LaMelo Ball','Grant Riller'], {'Anthony Edwards':28 if high else 24,'Tyrell Terry':6}, \
            [('Caleb Martin',6),('Cody Martin',6),('Jalen McDaniels',8),('Miles Bridges',16),('Malik Monk',16),('Gordon Hayward',32),("Devonte' Graham",24),('Brad Wanamaker',16)], \
            [('Caleb Martin',12),('Cody Martin',24),('Jalen McDaniels',24),('Miles Bridges',36),('Malik Monk',36),("Devonte' Graham",36),('Brad Wanamaker',32)], \
            {'LaMelo Ball':'Anthony Edwards'}
    if team == 'WAS':
        targets={'Gary Trent Jr.':28 if high else 24}
        if day >= '2021-03-25': targets['Troy Brown Jr.']=12 if high else 8
        return ['Isaac Bonga','Chandler Hutchison'],targets, \
            [('Troy Brown Jr.',0),('Jerome Robinson',0),('Garrison Mathews',0),('Davis Bertans',20),('Deni Avdija',16),('Raul Neto',12),('Ish Smith',12),('Rui Hachimura',28),('Bradley Beal',32)], \
            [('Garrison Mathews',20),('Deni Avdija',28),('Raul Neto',32),('Ish Smith',24)], {'Isaac Bonga':'Gary Trent Jr.','Garrison Mathews':'Gary Trent Jr.'}
    if team == 'DET':
        return ['Saddiq Bey','Killian Hayes'],{'Patrick Williams':30 if high else 28,'Kira Lewis Jr.':24 if high else 20}, \
            [('Saben Lee',0),('Dennis Smith Jr.',6),('Rodney McGruder',0),('Delon Wright',16),('Wayne Ellington',16),('Josh Jackson',20),('Svi Mykhailiuk',16),('Frank Jackson',20)], \
            [('Saben Lee',32),('Sekou Doumbouya',36),('Deividas Sirvydis',24),('Frank Jackson',36)], \
            {'Saddiq Bey':'Patrick Williams','Killian Hayes':'Kira Lewis Jr.'}
    if team == 'DEN':
        return ['R.J. Hampton'],{'Saddiq Bey':24 if high else 20}, \
            [('Vlatko Cancar',0),('JaMychal Green',16),('Will Barton',16),('Gary Harris',24),('Michael Porter Jr.',32),('Monte Morris',24)], [], {}
    if team == 'NOP':
        return ['Kira Lewis Jr.'],{'Killian Hayes':20 if high else 16}, \
            [('Eric Bledsoe',28),('JJ Redick',20),('Nickeil Alexander-Walker',12),('Josh Hart',24),('Naji Marshall',24),('Lonzo Ball',28),('James Johnson',24)], \
            [('Nickeil Alexander-Walker',24),('Lonzo Ball',36),('Naji Marshall',36),('Eric Bledsoe',36)], {'Kira Lewis Jr.':'Killian Hayes'}
    if team == 'TOR' and day >= '2021-03-25':
        return ['Gary Trent Jr.','Rodney Hood'],{'Norman Powell':32 if high else 28}, \
            [('Jalen Harris',6),('Malachi Flynn',12),("DeAndre' Bembry",16),('Stanley Johnson',20)], \
            [('Jalen Harris',24),('Malachi Flynn',28),("DeAndre' Bembry",32),('Stanley Johnson',36)], {'Gary Trent Jr.':'Norman Powell'}
    return [],{},[],[],{}


def valid(players, team):
    return len(set(players)) == 5 and all(set(players)&set(role) for role in ROLES[team].values())


def specs():
    result=[]
    for (gid,team),rows in sorted(groups().items()):
        day=rows[0]['date'];base,duration,clock=baseline(rows)
        changed=bool(policies(team,day,False)[1])
        for profile in PROFILES if changed else ('OBSERVED_HELD',):
            removed,targets,donors,recipients,swaps=policies(team,day,profile=='HIGH_MINUTES')
            alt=base.copy();newcomers=set(targets);eligible=allowed(rows)|newcomers
            for player in removed:alt.pop(player,None)
            alt.update({p:m*60 for p,m in targets.items()})
            moves=[]
            # Explicit role policy: preserve one interior defender; record any extra seconds and fund them.
            if changed:
                deficit=max(0,duration-sum(alt.get(p,0) for p in ROLES[team]['center']))
                if deficit:
                    candidates=[p for p in ROLES[team]['center'] if p in eligible and p in base]
                    player=max(candidates,key=lambda p:base[p])
                    alt[player]+=deficit
                    moves.append({'player':player,'seconds':deficit,'reason':'CONDITIONAL_CENTER_COVERAGE_NOT_CLOCK_CORRECTION'})
            gap=5*duration-sum(alt.values())
            for p,limit in recipients if gap>0 else donors:
                if p not in eligible or p in targets or p in removed:continue
                old=alt.get(p,0)
                delta=min(gap,max(0,limit*60-old)) if gap>0 else -min(-gap,max(0,old-limit*60))
                if delta:alt[p]=old+delta;gap-=delta;moves.append({'player':p,'seconds':delta,'limit_minutes':limit})
                if gap==0:break
            assert gap==0,(gid,team,profile,gap)
            alt={p:v for p,v in sorted(alt.items()) if v>0}
            starters=sorted(swaps.get(r['player'],r['player']) for r in rows if r['start']=='1')
            assert set(starters)<=set(alt),(gid,team,profile,starters)
            assert max(alt.values()) <= duration
            result.append({'event_id':gid,'date':day,'team':team,'profile':profile,'changed':changed,
                'game_duration_seconds':duration,'clock_correction':clock,'actual_seconds':base,
                'alternate_seconds':alt,'delta_seconds':{p:alt.get(p,0)-base.get(p,0) for p in sorted(set(base)|set(alt)) if alt.get(p,0)!=base.get(p,0)},
                'newcomers':sorted(newcomers),'starters':starters,'balance_moves':moves,
                'status':'CONDITIONAL_MINUTES_NOT_AVAILABILITY_OR_TRANSACTION_APPROVAL'})
    return result


def solve(b):
    if not b['changed']:return None
    import numpy as np
    from scipy.optimize import linprog
    players=list(b['alternate_seconds'])
    lineups=[c for c in itertools.combinations(players,5) if valid(c,b['team'])]
    start=tuple(b['starters']);assert start in lineups,(b['event_id'],b['team'],start)
    mat=np.array([[int(p in c) for c in lineups] for p in players]+[[1]*len(lineups)])
    target=list(b['alternate_seconds'].values())+[b['game_duration_seconds']]
    result=linprog(np.zeros(len(lineups)),A_eq=mat,b_eq=target,bounds=[(180 if c==start else 0,None) for c in lineups],method='highs')
    assert result.success,(b['event_id'],b['team'],b['profile'],result.message)
    return [{'players':list(c),'seconds':round(float(v),8)} for c,v in zip(lineups,result.x) if v>1e-6]


def verify_branches(branches,witnesses):
    raw=groups()
    for b,w in zip(branches,witnesses,strict=True):
        assert sum(b['delta_seconds'].values())==0
        assert sum(b['alternate_seconds'].values())==5*b['game_duration_seconds']
        eligible=allowed(raw[(b['event_id'],b['team'])])|set(b['newcomers'])
        assert all(p in eligible for p,n in b['delta_seconds'].items() if n>0)
        if not b['changed']:
            assert not b['delta_seconds'] and w is None
            continue
        total=0;seen=defaultdict(float);start=0
        for l in w:
            assert valid(l['players'],b['team']) and l['seconds']>0
            total+=l['seconds']
            if sorted(l['players'])==b['starters']:start+=l['seconds']
            for p in l['players']:seen[p]+=l['seconds']
        assert abs(total-b['game_duration_seconds'])<1e-5 and start>=180-1e-5
        assert set(seen)==set(b['alternate_seconds'])
        assert all(abs(seen[p]-v)<1e-5 for p,v in b['alternate_seconds'].items())


def build(witnesses):
    branches=specs();verify_branches(branches,witnesses)
    maps=cc.rating_maps();envelopes=cc.envelopes(maps);raw=groups()
    actual=lb.normalized_games();byid={g['id']:g for g in actual};schedule=defaultdict(list)
    for g in actual:
        for t in (g['home'],g['away']):schedule[t].append(g['date'])
    b2b={(t,d): i>0 and (date.fromisoformat(d)-date.fromisoformat(ds[i-1])).days==1
         for t,days in schedule.items() for ds in [sorted(days)] for i,d in enumerate(ds)}
    inputs=[];profiles=defaultdict(list)
    for b in branches:profiles[(b['event_id'],b['team'])].append(b)
    for gid in sorted({b['event_id'] for b in branches}):
        game=byid[gid];h,a=game['home'],game['away'];day=game['date']
        score={t:sum(int(r['pts']) for r in raw[(gid,t)]) for t in (h,a)}
        margin=score[h]-score[a]
        assert abs(margin)==game['margin'] and (h if margin>0 else a)==game['winner']
        for profile in PROFILES:
            hs=next(b for b in profiles[(gid,h)] if b['profile'] in (profile,'OBSERVED_HELD'))
            aws=next(b for b in profiles[(gid,a)] if b['profile'] in (profile,'OBSERVED_HELD'))
            assert hs['game_duration_seconds']==aws['game_duration_seconds']
            for method in METHODS:
                home,hu=cc.form(hs['delta_seconds'],maps[method],{})
                away,au=cc.form(aws['delta_seconds'],maps[method],{})
                terms={p:hu.get(p,0)-au.get(p,0) for p in set(hu)|set(au) if hu.get(p,0)!=au.get(p,0)}
                for fatigue in (0,0.5,1):
                    # Added-workload sensitivity for BOTH teams; actual baseline already contains actual fatigue.
                    hp=sum(max(0,n) for n in hs['delta_seconds'].values())/2880 if b2b[(h,day)] else 0
                    ap=sum(max(0,n) for n in aws['delta_seconds'].values())/2880 if b2b[(a,day)] else 0
                    constant=margin+home-away-fatigue*hp+fatigue*ap
                    band=cc.band(constant,terms,envelopes[method])
                    sign='HOME' if band[0]>0 else 'AWAY' if band[1]<0 else 'UNRESOLVED'
                    inputs.append({'event_id':gid,'profile':profile,'method':method,'fatigue':fatigue,
                        'actual_home_margin':margin,'home_margin_constant':round(constant,8),'away_margin_constant':round(-constant,8),
                        'unknown_coefficients':terms,'home_margin_band':band,'away_margin_band':[-band[1],-band[0]],
                        'home_b2b':b2b[(h,day)],'away_b2b':b2b[(a,day)],'workload_coefficients':[hp,ap],
                        'conditional_sign':sign,'selected':False})
    summary=[]
    for gid in sorted({r['event_id'] for r in inputs}):
        rows=[r for r in inputs if r['event_id']==gid];g=byid[gid]
        signs={r['conditional_sign'] for r in rows};actual_sign='HOME' if g['winner']==g['home'] else 'AWAY'
        opposite='AWAY' if actual_sign=='HOME' else 'HOME'
        status='ALL_TESTED_RETAIN' if signs=={actual_sign} else 'ALL_TESTED_REVERSE' if signs=={opposite} else 'MODEL_DISAGREEMENT_OR_UNRESOLVED'
        summary.append({'event_id':gid,'home':g['home'],'away':g['away'],'actual_winner':g['winner'],
            'actual_margin':g['margin'],'status':status,'method_bands':{m:[min(r['home_margin_band'][0] for r in rows if r['method']==m),max(r['home_margin_band'][1] for r in rows if r['method']==m)] for m in METHODS},'selected':False})
    bridge=[]
    previous=json.loads(lb.sb.OUT.read_text())
    for c in previous['record_candidates']:
        for condition in c['source_conditions']:
            profile=condition['path_id'].split('/')[0]
            selection={r['event_id']:r for r in inputs if (r['profile'],r['method'],r['fatigue'])==(profile,condition['method'],condition['fatigue'])}
            assert len(selection)==29
            games=[];deltas=defaultdict(int);changed=[];unresolved=[]
            for g in actual:
                if 'CHI' in (g['home'],g['away']):
                    winner='CHI' if c['outcomes'][g['date']] else (g['away'] if g['home']=='CHI' else g['home'])
                elif g['id'] in selection:
                    sign=selection[g['id']]['conditional_sign']
                    if sign=='UNRESOLVED':unresolved.append(g['id']);continue
                    winner=g['home'] if sign=='HOME' else g['away']
                else:winner=g['winner']
                games.append({**g,'winner':winner})
                if winner!=g['winner']:
                    deltas[winner]+=1;deltas[g['winner']]-=1;changed.append(g['id'])
            record={'source_condition':condition,'other_games_held':979,'selected':False,'unresolved_games':unresolved}
            if not unresolved:
                wins=lb.record_wins(games)
                assert sum(wins.values())==1080 and wins['CHI']==c['chicago_record'][0] and sum(deltas.values())==0
                try:rank=lb.chi_rank(games)
                except AssertionError:rank=None
                record.update({'team_wins':dict(sorted(wins.items())),'chicago_rank':rank,
                    'win_deltas_vs_actual':dict(sorted(deltas.items())),'changed_game_ids':changed})
            bridge.append(record)
    assert len(bridge)==72
    return {'stage':'O-15F14-B','status':'PRIORITY_29_PAIRED_CONDITIONAL_INPUTS_COMPLETE_FINAL_SEASON_HOLD',
        'branches':branches,'lineup_witnesses':witnesses,'paired_inputs':inputs,'game_summary':summary,
        'season_bridge':bridge,'bridge_scope':'CHI72 plus priority29 updated; other979 held. Same metric/profile/stress parameter, no favorable date mixing. Not full league canon.',
        'rating_policy':'Existing full-season RAPTOR RS shrink and March25 BPM shrink; retrospective proxies, not date-known ability.',
        'fatigue_policy':'Added positive delta seconds /2880, for each team on a true full-schedule back-to-back. Sensitivity only, not medical fatigue estimate.',
        'upstream_sha256':{p.name:cc.sha(p) for p in (OBS,cc.BPM,cc.paired.RAPTOR,lb.sb.OUT)},
        'manuscript_allowed':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    if args.write:
        branches=specs();data=build([solve(b) for b in branches]);OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    else:
        data=json.loads(OUT.read_text());assert data==build(data['lineup_witnesses'])
    from collections import Counter
    print(json.dumps({'PASS':True,'branches':len(data['branches']),'changed':sum(b['changed'] for b in data['branches']),
        'inputs':len(data['paired_inputs']),'games':dict(Counter(r['status'] for r in data['game_summary']))}))
