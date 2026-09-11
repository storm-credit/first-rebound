"""F: finish the859-game input queue with metric-blind common capacity policies.
All allocations, transactions, availability and season outcomes remain conditional.
"""
import argparse
import copy
import csv
import itertools
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
import build_nba_2020_21_final_close_impact as e

bi=e.bi
S=e.S
OBS=S/'NBA_2020_21_FINAL859_OBSERVATIONS.csv'
META=S/'NBA_2020_21_FINAL859_PROVENANCE.json'
MINUTES=S/'NBA_2020_21_FINAL859_MINUTES.json'
OUT=S/'NBA_2020_21_FULL_SEASON.json'
INPUTS=S/'NBA_2020_21_FINAL859_IMPACT.csv'
BOARD=S/'CHICAGO_2020_21_SEASON_SELECTION_BOARD.json'
ROLES=copy.deepcopy(e.ROLES)
# Conditional coaching-role candidates for newly covered dates. Not historical
# stint claims. Unknown role players are never silently excluded from the LP.
ROLE_ADDITIONS={
 'DEN':{'handler':['Markus Howard'],'center':['Bol Bol'],'wing':['Zeke Nnaji','Gary Harris','Greg Whittington','Gary Clark']},
 'DAL':{'wing':['Tyler Bey','Nate Hinton','Nicolo Melli','JJ Redick']},
 'POR':{'wing':['Keljin Blevins','T.J. Leaf']},
 'NOP':{'handler':['Isaiah Thomas'],'center':['Will Magnay'],'wing':['Nicolo Melli']},
 'DET':{'wing':['Rodney McGruder','Blake Griffin']},
 'WAS':{'handler':['Cassius Winston'],'center':['Jordan Bell','Anzejs Pasecniks']},
 'ORL':{'handler':['Devin Cannady'],'wing':['Ignas Brazdeikis','Robert Franks','Sindarius Thornwell']},
 'MIN':{'handler':['Ashton Hagans']},'TOR':{'wing':['Paul Watson']}}
for team,roles in ROLE_ADDITIONS.items():
    for role,players in roles.items():ROLES[team][role]+=players
THREE_SECOND_RESIDUES={('2021-01-06_NYK_UTA','UTA'),('2021-01-12_OKC_SAS','OKC'),
 ('2021-01-24_LAC_OKC','OKC'),('2021-03-01_SAS_BKN','BKN'),('2021-04-17_MIL_MEM','MEM')}
EMERGENCY_ROLES={'POR':{'handler':['Rodney Hood']},'DET':{'center':['Blake Griffin']},
                 'ORL':{'handler':['Terrence Ross'],'center':['Zeke Nnaji']}}


def branch_roles(team,emergency=False):
    roles=copy.deepcopy(ROLES[team])
    if emergency:
        for role,players in EMERGENCY_ROLES.get(team,{}).items():roles[role]+=players
    return roles


def ingest(folder):
    expected=json.loads(e.queue.ALL_OBS_META.read_text())
    pending={r['event_id'] for r in bi.cc.read(e.PENDING)}
    rows=[];scores=defaultdict(Counter)
    for name,h in expected['full_file_sha256'].items():
        p=folder/name
        assert bi.cc.sha(p)==h
        for r in bi.cc.read(p):
            if r['season_year']!='2020-21':continue
            a,separator,b=r['matchup'].split()
            home,away=(a,b) if separator=='vs.' else (b,a)
            gid=f"{r['game_date']}_{home}_{away}"
            scores[gid][r['teamTricode']]+=int(float(r['points'] or 0))
            if gid not in pending:continue
            rows.append({'event_id':gid,'game_id':r['gameId'].zfill(10),'date':r['game_date'],
                'home':home,'away':away,'team':r['teamTricode'],'player':r['personName'],
                'person_id':r['personId'],'seconds':bi.cc.seconds(r),'start':int(bool(r['position'])),
                'observed_start_position':r['position'],'comment':r['comment'],
                'pts':int(float(r['points'] or 0)),'plus_minus':int(float(r['plusMinusPoints'] or 0)),
                'official_url':f"https://www.nba.com/game/{r['gameId'].zfill(10)}/box-score"})
    actual={g['id']:g for g in bi.lb.normalized_games()}
    assert len(scores)==1080 and set(scores)==set(actual)
    for gid,g in actual.items():
        assert max(scores[gid],key=scores[gid].get)==g['winner']
        assert abs(scores[gid][g['home']]-scores[gid][g['away']])==g['margin']
    rows.sort(key=lambda r:(r['event_id'],r['team'],r['player']))
    assert len(rows)==len({(r['event_id'],r['team'],r['person_id']) for r in rows})
    assert {r['event_id'] for r in rows}==pending and len(pending)==859
    bi.cc.write_csv(OBS,rows)
    meta={'stage':'O-15F14-F','source_commit':expected['commit'],
        'source_repository':expected['source_repository'],'source_sha256':expected['full_file_sha256'],
        'games':len(pending),'rows':len(rows),'all1080_scores_and_winners_checked':True,
        'snapshot_sha256':bi.cc.sha(OBS),'upstream_queue_sha256':bi.cc.sha(e.PENDING),
        'scope':'Pinned public NBA V3 mirror, not primary page extraction; actual observations do not authorize alternate health or registration.'}
    META.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    return meta


def groups():
    result=defaultdict(list)
    for r in bi.cc.read(OBS):result[r['event_id'],r['team']].append(r)
    return result


def baseline(rows):
    raw={r['player']:int(r['seconds']) for r in rows if int(r['seconds'])}
    total=sum(raw.values());ot=round((total-14400)/1500);duration=2880+300*ot
    # Source residues are audited before accepted values are listed here.
    exception=(rows[0]['event_id'],rows[0]['team']) in THREE_SECOND_RESIDUES
    assert ot>=0 and (abs(total-5*duration)<=2 or exception and total-5*duration==3),(rows[0]['event_id'],rows[0]['team'],total)
    correction=5*duration-total
    p=max(raw,key=lambda p:(raw[p],p)) if correction else None
    base=raw.copy()
    if p:base[p]+=correction
    return base,duration,{'player':p,'seconds':correction,'raw_total_seconds':total}


def allocate(rows,profile,rival,emergency=False):
    gid,team,day=(rows[0][k] for k in ('event_id','team','date'))
    base,duration,clock=baseline(rows)
    removed,targets,donors,receivers,swaps=e.policy(team,day,profile=='HIGH_MINUTES',rival or 28)
    changed=bool(targets or set(removed)&set(base))
    b={'event_id':gid,'team':team,'date':day,'profile':profile if changed else 'OBSERVED_HELD',
       'rival_minutes':rival,'changed':changed,'game_duration_seconds':duration,
       'actual_seconds':base,'clock_correction':clock,'removed_players':removed,
       'newcomers':sorted(targets),'selected':False,'role_tier':'EMERGENCY_CONDITIONAL' if emergency else 'BASE'}
    if not changed:
        return {**b,'alternate_seconds':base,'delta_seconds':{},'lineup_witness':None,
                'status':'OBSERVED_HELD_CONDITIONAL','starters':sorted(r['player'] for r in rows if r['start']=='1')}
    eligible=(bi.allowed(rows)|set(targets))-set(removed)
    players=sorted(eligible)
    roles=branch_roles(team,emergency)
    assert eligible<=set().union(*map(set,roles.values())),(gid,team,eligible-set().union(*map(set,roles.values())))
    lineups=[c for c in itertools.combinations(players,5) if bi.valid(c,team,{team:roles})]
    if not lineups:return {**b,'status':'CAPACITY_HOLD','reason':'NO_ROLE_LINEUP'}
    # Fixed target minutes, at most12 extra incumbent minutes and36 total regular
    # minutes (actual longer exposure retained); active coach-DNP ceiling20.
    # These are coaching assumptions, not medical caps or rules of the league.
    overtime=duration-2880
    bounds={p:(targets[p]*60,targets[p]*60) if p in targets else (0,
        max(base.get(p,0),min(2160+overtime,base[p]+720)) if p in base else 1200)
        for p in players}
    desired={swaps.get(r['player'],r['player']) for r in rows if r['start']=='1'}
    desired-=set(removed)
    # Choose a valid starting five by incumbent overlap, then existing exposure;
    # neither scores nor impact coefficients enter this choice.
    start=min(lineups,key=lambda c:(-len(set(c)&desired),
        -sum(base.get(p,targets.get(p,0)*60) for p in c),c))
    matrix=np.array([[int(p in c) for c in lineups] for p in players],dtype=float)
    n=len(lineups);k=len(players)
    eq=np.zeros((k+1,n+2*k));eq[:k,:n]=matrix;eq[:k,n:n+k]=-np.eye(k);eq[:k,n+k:]=np.eye(k);eq[k,:n]=1
    target=[base.get(p,0) for p in players]+[duration]
    ub=np.zeros((2*k,n+2*k));ub[:k,:n]=matrix;ub[k:,:n]=-matrix
    ub_values=[bounds[p][1] for p in players]+[-bounds[p][0] for p in players]
    donor_order={p:i for i,(p,_) in reversed(list(enumerate(donors)))}
    receiver_order={p:i for i,(p,_) in reversed(list(enumerate(receivers)))}
    up=[2+receiver_order[p]/100 if p in receiver_order else 5+i/1000 for i,p in enumerate(players)]
    down=[2+donor_order[p]/100 if p in donor_order else 5+i/1000 for i,p in enumerate(players)]
    objective=[0]*n+up+down
    result=linprog(objective,A_eq=eq,b_eq=target,A_ub=ub,b_ub=ub_values,
        bounds=[(180 if c==start else 0,None) for c in lineups]+[(0,None)]*(2*k),method='highs')
    if not result.success:return {**b,'status':'CAPACITY_HOLD','reason':result.message,'starters':list(start),'minute_bounds_seconds':bounds}
    witness=[{'players':list(c),'seconds':round(float(v),8)} for c,v in zip(lineups,result.x[:n]) if v>1e-6]
    values=matrix@result.x[:n]
    alt={p:round(float(v),8) for p,v in zip(players,values) if v>1e-6}
    delta={p:round(alt.get(p,0)-base.get(p,0),8) for p in sorted(set(base)|set(alt)) if abs(alt.get(p,0)-base.get(p,0))>1e-6}
    return {**b,'status':'CONDITIONAL_CAPACITY_PASS','alternate_seconds':alt,'delta_seconds':delta,
        'lineup_witness':witness,'starters':list(start),'desired_starters':sorted(desired),
        'minute_bounds_seconds':bounds,'objective_value':float(result.fun)}


def build_minutes():
    branches=[]
    for (gid,team),rows in sorted(groups().items()):
        removed,targets,*_=e.policy(team,rows[0]['date'],False)
        changed=bool(targets or set(removed)&{r['player'] for r in rows if int(r['seconds'])})
        for profile,rival in itertools.product(bi.PROFILES if changed else ('OBSERVED_HELD',),(24,28,32) if team=='MIN' else (None,)):
            b=allocate(rows,profile,rival)
            if b['status']=='CAPACITY_HOLD' and team in EMERGENCY_ROLES:
                initial=b
                b=allocate(rows,profile,rival,True)
                b['base_policy_failure']=initial
            branches.append(b)
    return {'stage':'O-15F14-F','branches':branches,'roles':ROLES,'selected':False,
            'observation_sha256':bi.cc.sha(OBS),'script_sha256':bi.cc.sha(Path(__file__))}


def verify_minutes(data):
    raw=groups()
    for b in data['branches']:
        if b['status']=='CAPACITY_HOLD':continue
        alt=b['alternate_seconds'];duration=b['game_duration_seconds']
        assert abs(sum(alt.values())-5*duration)<1e-5
        assert abs(sum(b['delta_seconds'].values()))<1e-5
        assert not set(b['removed_players'])&set(alt)
        eligible=(bi.allowed(raw[b['event_id'],b['team']])|set(b['newcomers']))-set(b['removed_players'])
        assert set(alt)<=eligible
        if not b['changed']:
            assert not b['delta_seconds'] and b['lineup_witness'] is None
            continue
        seconds=Counter();total=start=0
        roles=branch_roles(b['team'],b['role_tier']=='EMERGENCY_CONDITIONAL')
        for w in b['lineup_witness']:
            assert w['seconds']>0 and bi.valid(w['players'],b['team'],{b['team']:roles})
            total+=w['seconds']
            if w['players']==b['starters']:start+=w['seconds']
            for p in w['players']:seconds[p]+=w['seconds']
        assert abs(total-duration)<1e-5 and start>=180-1e-5
        assert set(seconds)==set(alt)
        assert all(abs(seconds[p]-n)<1e-5 for p,n in alt.items())
        for p,(lo,hi) in b['minute_bounds_seconds'].items():assert lo-1e-5<=alt.get(p,0)<=hi+1e-5


def rating_maps():
    maps=bi.cc.rating_maps()
    alias=next(r for r in bi.cc.read(bi.cc.BPM) if r['player_id']=='kanteen01')
    source=next(r for r in bi.cc.read(bi.cc.paired.RAPTOR) if r['player_id']=='kanteen01')
    maps['RAPTOR_RS_EB'][bi.cc.paired.norm(alias['nba_player'])]=maps['RAPTOR_RS_EB'][bi.cc.paired.norm(source['player_name'])]
    return maps


def paired_inputs(data):
    maps=rating_maps();env=bi.cc.envelopes(maps)
    actual={g['id']:g for g in bi.lb.normalized_games()};raw=groups()
    schedule=defaultdict(list)
    for g in actual.values():
        for t in (g['home'],g['away']):schedule[t].append(g['date'])
    b2b={(t,day):i>0 and (date.fromisoformat(day)-date.fromisoformat(ds[i-1])).days==1
         for t,days in schedule.items() for ds in [sorted(days)] for i,day in enumerate(ds)}
    lookup=defaultdict(list)
    for b in data['branches']:lookup[b['event_id'],b['team']].append(b)
    inputs=[]
    for gid in sorted({gid for gid,t in lookup}):
        g=actual[gid];h,a,day=(g[k] for k in ('home','away','date'))
        margin=sum(int(r['pts']) for r in raw[gid,h])-sum(int(r['pts']) for r in raw[gid,a])
        for profile,rival in itertools.product(bi.PROFILES,(24,28,32) if 'MIN' in (h,a) else (None,)):
            def choose(t):
                bs=[b for b in lookup[gid,t] if b['profile'] in (profile,'OBSERVED_HELD') and b['rival_minutes'] in (None,rival)]
                assert len(bs)==1
                return bs[0]
            hs,aws=choose(h),choose(a)
            for method,fatigue in itertools.product(bi.METHODS,(0,.5,1)):
                row={'event_id':gid,'profile':profile,'rival_minutes':rival,'method':method,'fatigue':fatigue,
                     'actual_home_margin':margin,'selected':False}
                if any(b['status']=='CAPACITY_HOLD' for b in (hs,aws)):
                    inputs.append({**row,'status':'CAPACITY_HOLD'});continue
                home,hu=bi.cc.form(hs['delta_seconds'],maps[method],{})
                away,au=bi.cc.form(aws['delta_seconds'],maps[method],{})
                terms={p:round(hu.get(p,0)-au.get(p,0),12) for p in sorted(set(hu)|set(au)) if abs(hu.get(p,0)-au.get(p,0))>1e-9}
                hp=sum(max(0,n) for n in hs['delta_seconds'].values())/2880 if b2b[h,day] else 0
                ap=sum(max(0,n) for n in aws['delta_seconds'].values())/2880 if b2b[a,day] else 0
                constant=round(margin+home-away-fatigue*hp+fatigue*ap,8)
                band=bi.cc.band(constant,terms,env[method])
                inputs.append({**row,'status':'CONDITIONAL_IMPACT','home_margin_constant':constant,
                    'away_margin_constant':-constant,'unknown_coefficients':terms,'home_margin_band':band,
                    'conditional_sign':'HOME' if band[0]>0 else 'AWAY' if band[1]<0 else 'UNRESOLVED',
                    'workload_coefficients':[hp,ap],
                    'emergency_role_teams':[b['team'] for b in (hs,aws) if b['role_tier']=='EMERGENCY_CONDITIONAL']})
    return inputs


def conditional_band(row,rating,envelope):
    terms={p:c for p,c in row['unknown_coefficients'].items() if p!=e.RIVAL}
    return bi.cc.band(row['home_margin_constant']+row['unknown_coefficients'].get(e.RIVAL,0)*rating,terms,envelope)


def bridges(inputs):
    upstream=json.loads(e.OUT.read_text());actual=bi.lb.normalized_games()
    env=bi.cc.envelopes(rating_maps());result=[]
    index=defaultdict(list)
    for r in inputs:index[r['profile'],r['method'],r['fatigue']].append(r)
    for ix,previous in enumerate(upstream['season_bridge']):
        c=previous['source_condition'];profile,rival,_=c['path_id'].split('/');rival=int(rival.split('_')[1])
        chosen=[r for r in index[profile,c['method'],c['fatigue']] if r['rival_minutes'] in (None,rival)]
        assert len(chosen)==859
        low,high=previous['shared_rival_rating_open_interval'];envelope=env[c['method']]
        cuts=set()
        for r in chosen:
            coefficient=r.get('unknown_coefficients',{}).get(e.RIVAL,0)
            if coefficient:
                # Non-rival missing ratings retain a stress envelope; partition both
                # endpoint roots and keep any middle unresolved interval explicitly.
                baseband=conditional_band(r,0,envelope)
                cuts.update(-v/coefficient for v in baseband if low<-v/coefficient<high)
        bounds=[low,*sorted(cuts),high]
        lookup={r['event_id']:r for r in chosen};upchanged=set(previous['changed_game_ids'])
        for lo,hi in zip(bounds,bounds[1:]):
            rating=(lo+hi)/2;games=[];unresolved=[];unknown_safe=[]
            for g in actual:
                winner=bi.lb.changed_game(g)['winner'] if g['id'] in upchanged else g['winner']
                if g['id'] in lookup:
                    r=lookup[g['id']]
                    if r['status']=='CAPACITY_HOLD':unresolved.append(g['id'])
                    else:
                        band=conditional_band(r,rating,envelope)
                        if band[0]>0:winner=g['home']
                        elif band[1]<0:winner=g['away']
                        else:unresolved.append(g['id'])
                        if set(r['unknown_coefficients'])-{e.RIVAL} and g['id'] not in unresolved:unknown_safe.append(g['id'])
                games.append({**g,'winner':winner})
            row={'source_bridge_index':ix,'source_condition':c,'shared_rival_rating_open_interval':[lo,hi],
                 'unresolved_games':unresolved,'nonrival_unknown_direction_safe_games':unknown_safe,
                 'selected':False,'zero_boundaries_unresolved':True}
            if unresolved:
                row.update({'team_wins':None,'seeds':None,'changed_game_ids':None,'chicago_rank':None,
                            'status':'INCOMPLETE_NO_ACTUAL_RESULT_FILL'})
            else:
                wins=bi.lb.record_wins(games)
                assert sum(wins.values())==1080 and wins['CHI']==previous['team_wins']['CHI']
                try:seeds=e.d.ps.order(games);tie=None
                except ValueError as err:seeds=None;tie=str(err)
                row.update({'team_wins':dict(sorted(wins.items())),'seeds':seeds,'later_tie_hold':tie,
                    'chicago_rank':seeds['EAST'].index('CHI')+1 if seeds else None,
                    'changed_game_ids':sorted(g['id'] for g,original in zip(games,actual) if g['winner']!=original['winner']),
                    'status':'FULL_CONDITIONAL_SCHEDULE','new_games_uncomputed':0})
            result.append(row)
    return result


def league_cases(bridge):
    grouped=defaultdict(list)
    for i,r in enumerate(bridge):
        if r['changed_game_ids'] is not None:grouped[tuple(r['changed_game_ids'])].append(i)
    cases=[]
    for i,(ids,indices) in enumerate(sorted(grouped.items()),1):
        r=bridge[indices[0]];seeds=r['seeds'];wins=r['team_wins']
        case={'id':f'F{i:03d}','bridge_indices':indices,'changed_game_ids':list(ids),'team_wins':wins,
              'seeds':seeds,'later_tie_hold':r['later_tie_hold'],'selected':False}
        if seeds:
            fields=set();positions={'LOTTERY':[],'PLAYOFF':[]};first=[]
            for east,west in itertools.product(e.d.ps.playin(seeds['EAST']),e.d.ps.playin(seeds['WEST'])):
                playoff=set(seeds['EAST'][:6]+seeds['WEST'][:6]+east['qualifiers']+west['qualifiers'])
                lottery=e.d.ps.ALL-playoff;assert len(lottery)==14
                fields.add(tuple(sorted(lottery)))
                kind='LOTTERY' if 'CHI' in lottery else 'PLAYOFF'
                groups=e.d.ps.record_groups(lottery,wins)+e.d.ps.record_groups(playoff,wins,15)
                positions[kind].extend(next(g['positions'] for g in groups if 'CHI' in g['teams']))
                for g in east['games'][:2]:
                    if 'CHI' in (g['home'],g['away']):first.append((g['home'],g['away']))
            case.update({'playin_seed_teams':{k:v[6:10] for k,v in seeds.items()},'joint_playin_outcome_count':64,
                'possible_distinct_lottery_fields':len(fields),
                'chicago_record_position_ranges':{k:[min(v),max(v)] for k,v in positions.items() if v},
                'chicago_first_playin_pairings':[list(x) for x in sorted(set(first))]})
        cases.append(case)
    return cases


def role_stress(data,inputs):
    exposure={}
    for b in data['branches']:
        if b['role_tier']!='EMERGENCY_CONDITIONAL' or b['status']=='CAPACITY_HOLD':continue
        roles=branch_roles(b['team'])
        loads={role:sum(w['seconds'] for w in b['lineup_witness'] if not set(w['players'])&set(roles[role]))
               for role in ('handler','center')}
        exposure[b['event_id'],b['team'],b['profile']]=loads
    actual={g['id']:g for g in bi.lb.normalized_games()};rows=[]
    for r in inputs:
        if not r.get('emergency_role_teams'):continue
        g=actual[r['event_id']]
        home=sum(exposure.get((g['id'],g['home'],r['profile']),{}).values())/2880
        away=sum(exposure.get((g['id'],g['away'],r['profile']),{}).values())/2880
        for penalty in (0,1,3,6):
            band=[round(v-penalty*home+penalty*away,8) for v in r['home_margin_band']]
            sign='HOME' if band[0]>0 else 'AWAY' if band[1]<0 else 'UNRESOLVED'
            rows.append({'event_id':g['id'],'profile':r['profile'],'method':r['method'],'fatigue':r['fatigue'],
                'role_penalty_per48_minutes':penalty,'home_role_load':home,'away_role_load':away,
                'home_margin_band':band,'conditional_sign':sign,'differs_from_zero_role_cost':sign!=r['conditional_sign'],
                'selected':False})
    return {'scope':'Independent stress of emergency role costs, not an estimated interaction coefficient or added fatigue. Main paths use zero extra role cost; nonzero scenarios are not silently folded in.',
            'rows':rows,'coefficient_selected':False}


def selection_board(output):
    bridge=output['season_bridge'];cases=output['league_cases'];families=[]
    for i,(profile,method) in enumerate(itertools.product(bi.PROFILES,bi.METHODS)):
        indices=[n for n,r in enumerate(bridge) if r['source_condition']['path_id'].startswith(profile+'/') and r['source_condition']['method']==method]
        rows=[bridge[n] for n in indices];ids=[c['id'] for c in cases if set(c['bridge_indices'])&set(indices)]
        def band(team):
            wins=[r['team_wins'][team] for r in rows if r['team_wins']]
            return [min(wins),max(wins)] if wins else None
        families.append({'id':chr(65+i),'profile':profile,'method':method,'bridge_indices':indices,'league_case_ids':ids,
            'chicago_wins':band('CHI'),'minnesota_wins':band('MIN'),
            'chicago_ranks':sorted({r['chicago_rank'] for r in rows if r['chicago_rank']}),'selected':False})
    return {'stage':'O-15F14-F','policy_families':families,
        'interpretation':'Four mutually exclusive minute/metric families, not four canon seasons. Fatigue and one common rival rating still need a coherent basis; interval counts are not probabilities.',
        'decision_sequence':['Resolve or explicitly retain the registered transaction/availability/role scenario.',
            'Set protagonist/rival growth and fatigue assumptions independently of desired standings; compare metrics without daily mixing.',
            'Choose one complete1080-game path only after the premises are accepted.',
            'Select play-in events, then derive14 lottery participants and draw; do not copy actual picks.'],
        'execution_conditions':[
            {'id':'EX01','status':'PLAYER_ROUTE_APPROVED_EXACT_CHARGE_HOLD','action':'Chicago A does not require reapproval; verify applicable bonus/charge treatment.'},
            {'id':'EX02','status':'GORDON_A_NOT_AUTHOR_LOCKED_EXACT_PICK_CHARGE_HOLD','action':'Choose Gordon package using existing four-option board; changed package invalidates DEN/ORL policy inputs.'},
            {'id':'EX03','status':'FOURNIER_BOSTON_CONDITIONAL','action':'Keep separate from Gordon; record alternate Orlando transaction objective.'},
            {'id':'EX04','status':'INCUMBENT_FOLLOWUP_REGISTRATION_CONDITIONAL','action':'Check Hall/Wagner/Parker and other incumbent contracts against the changed roster needs.'},
            {'id':'EX05','status':'POWELL_TORONTO_HOOD_PORTLAND_CONDITIONAL','action':'Do not automatically restore the actual Portland transaction.'},
            {'id':'EX06','status':'GSW_LAL_CORE_DEPENDENCY_CONDITIONAL','action':'Preserve core structure only with accessory asset/registration conditions stated.'},
            {'id':'EX07','status':'CAPACITY_COMPLETE_HEALTH_AND_TACTICS_UNSELECTED','action':'1252 new changed allocations pass declared constraints; approve neither health nor role efficiency from LP feasibility.'},
            {'id':'EX08','status':'FULL_REGULAR_SCHEDULE_CONNECTED_POSTSEASON_DRAW_UNSELECTED','action':'Use selected full path to derive seeds and subsequent lottery roster.'}],
        'no_new_game_input_batch_needed':output['uncomputed_game_count']==0,
        'selected':False,'manuscript_allowed':False}


def summarize(data,inputs):
    raw=groups();lookup=defaultdict(list)
    for r in inputs:lookup[r['event_id']].append(r)
    branch_lookup=defaultdict(list)
    for b in data['branches']:branch_lookup[b['event_id']].append(b)
    games=[]
    for gid,rows in sorted(lookup.items()):
        if any(r['status']=='CAPACITY_HOLD' for r in rows):status='CAPACITY_HOLD'
        else:
            actual_sign='HOME' if rows[0]['actual_home_margin']>0 else 'AWAY';signs={r['conditional_sign'] for r in rows}
            status='ALL_TESTED_RETAIN' if signs=={actual_sign} else 'ALL_TESTED_REVERSE' if signs==({'HOME','AWAY'}-{actual_sign}) else 'MODEL_DISAGREEMENT_OR_UNRESOLVED'
        games.append({'event_id':gid,'status':status,'both_observed_held':all(not b['changed'] for b in branch_lookup[gid]),
            'emergency_role_teams':sorted({b['team'] for b in branch_lookup[gid] if b['role_tier']=='EMERGENCY_CONDITIONAL'}),
            'method_bands':{m:[min(r['home_margin_band'][0] for r in rows if r['method']==m),max(r['home_margin_band'][1] for r in rows if r['method']==m)] for m in bi.METHODS} if status!='CAPACITY_HOLD' else {},
            'selected':False})
    bridge=bridges(inputs);cases=league_cases(bridge)
    return {'stage':'O-15F14-F','status':'FINAL859_CONDITIONAL_SCREEN_AND_FULL_SCHEDULE_CONNECTION',
        'game_summary':games,'season_bridge':bridge,'league_cases':cases,
        'emergency_role_stress':role_stress(data,inputs),
        'branch_status_counts':dict(Counter(b['status'] for b in data['branches'])),
        'impact_conditions':len(inputs),'observed_games':len(games),'observed_rows':sum(map(len,raw.values())),
        'missing_rating_envelopes':bi.cc.envelopes(rating_maps()),
        'uncomputed_game_count':sum(g['status']=='CAPACITY_HOLD' for g in games),
        'scope':'All1080 schedule winners connected under fixed Chicago/B/D/E inputs and new859 conditional common policies. Held incumbent policies are assumptions, not no-impact evidence.',
        'conditions':['No scores or ratings in minute objective; fixed LOW/HIGH newcomer targets and shared rival24/28/32 minutes.',
          'Incumbent increases capped12min and36min total plus actual overtime; longer actual minutes retained; coach-DNP ceiling20. These are coaching scenarios, not medical approvals.',
          'Emergency secondary initiator or interior roles only after base role failure; exact failed base record retained. No automatic cap relaxation or injured-player activation.',
          'Same rival effective rating across entire1080-game path; non-rival missing ratings retained symbolically and bounded only by empirical stress range, not zero-imputed.',
          'No probabilities, new health events, pace/interaction estimates, exact playoff events or lottery draws selected.'],
        'source_sha256':{p.name:bi.cc.sha(p) for p in (OBS,META,MINUTES,e.OUT,bi.cc.BPM,bi.cc.paired.RAPTOR,Path(__file__))},
        'selected':False,'manuscript_allowed':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path);p.add_argument('--write-minutes',action='store_true');p.add_argument('--write',action='store_true');a=p.parse_args()
    if a.source_dir:print(json.dumps(ingest(a.source_dir)))
    if a.write_minutes:
        data=build_minutes();MINUTES.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
        print(dict(Counter(b['status'] for b in data['branches'])))
    if a.write or not(a.source_dir or a.write_minutes):
        data=json.loads(MINUTES.read_text());verify_minutes(data);inputs=paired_inputs(data);output=summarize(data,inputs)
        rows=[{k:json.dumps(v,ensure_ascii=False,separators=(',',':')) if isinstance(v,(dict,list)) else v for k,v in r.items()} for r in inputs]
        if a.write:
            OUT.write_text(json.dumps(output,ensure_ascii=False,separators=(',',':'))+'\n');bi.cc.write_csv(INPUTS,rows)
            BOARD.write_text(json.dumps(selection_board(output),ensure_ascii=False,indent=2)+'\n')
        else:
            assert json.loads(OUT.read_text())==output
            assert json.loads(BOARD.read_text())==selection_board(output)
            assert bi.cc.read(INPUTS)==[{k:'' if v is None else str(v) for k,v in r.items()} for r in rows]
        print(json.dumps({'games':dict(Counter(r['status'] for r in output['game_summary'])),
            'inputs':len(inputs),'bridge':len(output['season_bridge']),'cases':len(output['league_cases']),
            'incomplete':sum(bool(r['unresolved_games']) for r in output['season_bridge']),
            'later_ties':sum(bool(r.get('later_tie_hold')) for r in output['season_bridge']),
            'CHI_ranks':sorted({r['chicago_rank'] for r in output['season_bridge'] if r['chicago_rank']})}))
