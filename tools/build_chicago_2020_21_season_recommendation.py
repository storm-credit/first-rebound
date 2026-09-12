"""K: one review candidate, explicit calendars and fixed-minute spacing audit.
No new player minutes, rating prior, health event or contract is author-locked.
"""
import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
import build_chicago_2020_21_availability_policy as j

S=j.S
OUT=S/'CHICAGO_2020_21_SEASON_RECOMMENDATION.json'
LINEUPS=S/'ORLANDO_2020_21_RETAINED_BACKUP_LINEUPS.json'
BIGS={'Nikola Vucevic','Mo Bamba','Zeke Nnaji','Donta Hall','Moritz Wagner'}
PROFILE='LOW_MINUTES'
AVAILABILITY='PORTER_ZERO'


def controls():
    schedule,_,branches,inputs,origins=j.load()
    witnesses={}
    for path in (j.f.e.d.OUT,j.f.e.OUT):
        data=json.loads(path.read_text())
        for b,w in zip(data['branches'],data['lineup_witnesses'],strict=True):
            witnesses[b['event_id'],b['team'],b['profile']]=w
    result=[]
    for key,b in sorted(branches.items()):
        gid,team,profile=key
        if team!='ORL' or profile!=PROFILE or schedule[gid]['date']<'2021-03-25':continue
        w=b.get('lineup_witness') or witnesses.get(key)
        assert w
        result.append((b,w,origins[key]))
    assert len(result)==28
    return result


def excess(w):
    return sum(x['seconds']*max(0,len(set(x['players'])&BIGS)-2) for x in w)


def solve():
    result=[]
    for b,w,source in controls():
        players=sorted(b['alternate_seconds']);roles=j.roles_for(b)
        combos=[list(c) for c in itertools.combinations(players,5) if j.bi.valid(c,'ORL',{'ORL':roles})]
        starter=b['starters'];assert starter in combos
        matrix=np.array([[int(p in c) for c in combos] for p in players]+[[1]*len(combos)])
        targets=[b['alternate_seconds'][p] for p in players]+[b['game_duration_seconds']]
        cost=[max(0,len(set(c)&BIGS)-2) for c in combos]
        opt=linprog(cost,A_eq=matrix,b_eq=targets,
            bounds=[(180 if c==starter else 0,None) for c in combos],method='highs')
        assert opt.success,(b['event_id'],opt.message)
        proof=[{'players':c,'seconds':float(n)} for c,n in zip(combos,opt.x) if n>1e-7]
        # Zero lower bound or total frontcourt minutes beyond two full slots.
        lower=max(0,sum(b['alternate_seconds'].get(p,0) for p in BIGS)-2*b['game_duration_seconds'])
        assert excess(proof)>=lower-1e-5 and excess(proof)<=excess(w)+1e-5
        result.append({'event_id':b['event_id'],'source':source,'control_minutes':b['alternate_seconds'],
            'duration':b['game_duration_seconds'],'starters':starter,'roles':roles,
            'old_excess_big_seconds':excess(w),'minimum_excess_big_seconds':excess(proof),
            'analytic_lower_bound_seconds':lower,'lower_bound_attained':abs(excess(proof)-lower)<1e-5,
            'lineup_witness':proof,'selected':False})
    return {'stage':'O-15F14-K','profile':PROFILE,'big_player_set':sorted(BIGS),'rows':result,
        'scope':'Abstract stint decomposition only; no chronological substitution plan or actual tactical efficiency claim.',
        'generator_sha256':j.cc.sha(Path(__file__))}


def verify(data):
    upstream={b['event_id']:b for b,_,_ in controls()}
    for r in data['rows']:
        assert r['control_minutes']==upstream[r['event_id']]['alternate_seconds']
        seen=Counter();total=start=0
        for w in r['lineup_witness']:
            assert w['seconds']>0 and j.bi.valid(w['players'],'ORL',{'ORL':r['roles']})
            total+=w['seconds'];start+=w['seconds'] if w['players']==r['starters'] else 0
            for p in w['players']:seen[p]+=w['seconds']
        assert abs(total-r['duration'])<1e-5 and start>=180-1e-5
        assert set(seen)==set(r['control_minutes'])
        assert all(abs(seen[p]-n)<1e-5 for p,n in r['control_minutes'].items())
        assert abs(excess(r['lineup_witness'])-r['minimum_excess_big_seconds'])<1e-5
        assert r['minimum_excess_big_seconds']>=r['analytic_lower_bound_seconds']-1e-5


def spacing_stress(data):
    schedule,_,_,inputs,_=j.load();env=j.cc.envelopes(j.f.rating_maps())
    ratings=json.loads(j.i.h.g.OUT.read_text())['rival_candidates'][0]['methods'];rows=[]
    chi={m:j.chi_inputs(PROFILE,m,AVAILABILITY) for m in j.METHODS}
    leave={(r['event_id'],r['method']):r for r in json.loads(j.OUT.read_text())['impacts'] if
        (r['policy'],r['profile'],r['availability'])==('J1_TERRY_LEAVE',PROFILE,AVAILABILITY)}
    for r in data['rows']:
        gid=r['event_id'];g=schedule[gid]
        for method in j.METHODS:
            if 'CHI' in (g['home'],g['away']):
                src=chi[method][g['date']];sign=1 if g['home']=='CHI' else -1
                c=sign*src['constant'];terms={p:sign*n for p,n in src['other_unknown_coefficients'].items()}
            else:
                src=inputs[gid,PROFILE,method];c=src['home_margin_constant'];terms=src['unknown_coefficients'].copy()
            if (gid,method) in leave:
                src=leave[gid,method];assert src['status']=='CONDITIONAL_IMPACT'
                c=src['home_margin_constant'];terms=src['unknown_coefficients'].copy()
            c+=terms.pop(j.f.e.RIVAL,0)*ratings[method]['effective_rating']
            before=j.cc.band(c,terms,env[method])
            sign=1 if g['home']=='ORL' else -1
            for penalty in (0,1,3,6):
                band=j.cc.band(c-sign*penalty*r['minimum_excess_big_seconds']/2880,terms,env[method])
                direction=lambda x:'HOME' if x[0]>0 else 'AWAY' if x[1]<0 else 'UNRESOLVED'
                rows.append({'event_id':gid,'method':method,'penalty_per48_excess_big_minutes':penalty,
                    'terry_leave_already_applied':(gid,method) in leave,
                    'home_margin_band':band,'base_home_margin_band':before,
                    'direction':direction(band),'base_direction':direction(before),
                    'changes_direction':direction(band)!=direction(before),'selected':False})
    return rows


def calendar():
    schedule={g['id']:g for g in j.bi.lb.normalized_games()}
    packet=json.loads(j.i.h.g.OUT.read_text());rows=[]
    for group in packet['conditional_target_calendar']:
        team,player=group['team'],group['player']
        for gid in group['event_ids']:
            _,targets,*_=j.f.e.policy(team,schedule[gid]['date'],False,28)
            assert player in targets
            seconds=0 if player=='Tyrell Terry' and schedule[gid]['date']>='2021-03-30' else targets[player]*60
            rows.append({'scope':'NEW_TEAM_TARGET','event_id':gid,'team':team,'player':player,'seconds':seconds,
                'basis':'J1_PRIVATE_LEAVE_SCENARIO' if seconds==0 else 'EXISTING_CONDITIONAL_TARGET',
                'author_locked':False})
    actual=j.cc.read(j.cc.PRE);donors=j.cc.read(S/'CHICAGO_2020_21_PREDEADLINE_DONOR_VECTOR.csv')
    pre=j.cc.read(S/'CHICAGO_2020_21_PREDEADLINE_MINUTE_LEDGER.csv')
    post=j.cc.read(S/'CHICAGO_2020_21_POSTDEADLINE_CAPACITY_VECTOR.csv')
    for gid,g in sorted(schedule.items()):
        if 'CHI' not in (g['home'],g['away']):continue
        day=g['date']
        for player in ('Protagonist','LaMelo Ball','Wendell Carter Jr.','Otto Porter Jr.'):
            if day<='2021-03-24':
                if player in ('Protagonist','LaMelo Ball'):
                    r=next(r for r in pre if r['date']==day)
                    seconds=int(r['protagonist_seconds' if player=='Protagonist' else 'lamelo_seconds'])
                else:
                    seconds=sum(int(r['seconds']) for r in actual if (r['date'],r['team'],r['player'])==(day,'CHI',player))
                    seconds+=sum(int(r['delta_seconds']) for r in donors if (r['date'],r['player'])==(day,player))
            else:
                r=next(r for r in post if (r['date'],r['player'],r['scenario'])==(day,player,AVAILABILITY))
                seconds=int(r['alternate_seconds'])
            rows.append({'scope':'CHI_FOUR_PLAYER_PROJECTION','event_id':gid,'team':'CHI','player':player,
                'seconds':seconds,'basis':'EXISTING_CHICAGO_MINUTE_MODEL','author_locked':False})
    summary=[]
    for scope,team,player in sorted({(r['scope'],r['team'],r['player']) for r in rows}):
        rr=[r for r in rows if (r['scope'],r['team'],r['player'])==(scope,team,player)]
        summary.append({'scope':scope,'team':team,'player':player,'dates':len(rr),
            'positive_minute_dates':sum(r['seconds']>0 for r in rr),'total_seconds':sum(r['seconds'] for r in rr),
            'zero_event_ids':[r['event_id'] for r in rr if not r['seconds']]})
    return rows,summary


def build(data):
    previous=json.loads(j.OUT.read_text());full=json.loads(j.f.OUT.read_text());schedule=j.bi.lb.normalized_games()
    candidates=[]
    for method in j.METHODS:
        r=next(r for r in previous['season_diagnostics'] if
            (r['policy'],r['profile'],r['method'],r['availability'])==('J1_TERRY_LEAVE',PROFILE,method,AVAILABILITY))
        case=next(c for c in full['league_cases'] if c['id']==r['base_case_id'])
        changed=set(r['changed_game_ids']);games=[]
        for g in schedule:
            winner=(g['away'] if g['winner']==g['home'] else g['home']) if g['id'] in changed else g['winner']
            games.append({**g,'winner':winner})
        assert j.bi.lb.record_wins(games)==r['team_wins'] and j.f.e.d.ps.order(games)==r['seeds']
        candidates.append({'role':'PRIMARY_RECOMMENDATION' if method=='BPM_MAR25_EB' else 'CROSSCHECK',
            **r,'regular_season_games':[{'event_id':g['id'],'winner':g['winner']} for g in games],
            'playin_seed_teams':case['playin_seed_teams'],
            'chicago_first_playin_pairings':case['chicago_first_playin_pairings'],
            'record_position_ranges_not_draft_picks':case['chicago_record_position_ranges']})
    rows,summary=calendar();stress=spacing_stress(data)
    hall_gap=[{'event_id':r['event_id'],'seconds':r['control_minutes'].get('Donta Hall',0)}
              for r in data['rows'] if '2021-05-02'<=r['event_id'][:10]<'2021-05-09']
    assert len(hall_gap)==3 and all(r['seconds']==0 for r in hall_gap)
    return {'stage':'O-15F14-K','status':'ONE_REGULAR_SEASON_RECOMMENDATION_READY_NOT_CANON',
        'working_proposal':{'id':'K1','policy':'J1_TERRY_LEAVE','profile':PROFILE,'porter':AVAILABILITY,
            'rival_role':'R1','rival_minutes':28,'fatigue':.5,'primary_method':'BPM_MAR25_EB',
            'crosscheck_method':'RAPTOR_RS_EB','orlando_backups':'HALL_AND_WAGNER_CONDITIONAL_ROUTE_RETAINED',
            'author_locked':False,'extra_spacing_cost_selected':False},
        'season_candidates':candidates,'calendar':rows,'calendar_summary':summary,
        'reported_hall_registration_gap_check':hall_gap,
        'orlando_fixed_minute_lineup_summary':[{k:v for k,v in r.items() if k not in ('lineup_witness','roles','control_minutes')} for r in data['rows']],
        'spacing_stress':stress,'spacing_stress_counterexamples':[r for r in stress if r['changes_direction']],
        'orlando_supporting_calendar':[{r['event_id']:{p:r['control_minutes'].get(p,0) for p in sorted(BIGS)}} for r in data['rows']],
        'remaining_requirements':[
            {'id':'K_HEALTH','type':'AUTHOR_SCENARIO_CHOICE','action':'Review the1079-row projection; it asserts no historical diagnosis or automatic full fitness.'},
            {'id':'K_REGISTRATION','type':'FACT_AND_SCENARIO','action':'Verify roster slots/exceptions/charges for Hall/Wagner/Parker/Rivers/McGee and other followups; a minute witness is not registration clearance.'},
            {'id':'K_TRANSACTIONS','type':'FACT_RECOVERY','action':'Exact Chicago/Gordon/Fournier charge, exception and pick obligations remain open; approved player directions are not reasked.'},
            {'id':'K_METHOD_EVENTS','type':'AUTHOR_SCENARIO_CHOICE','action':'Review the whole BPM F038 path and crosscheck differences before locking season/playin/lottery. Do not mix per-game methods.'}],
        'playin_recommendation_boundary':{'first_game':['WAS','CHI'],'if_chicago_wins':'Visit loser of BOS–IND; two wins are required for seed8.',
            'first_or_second_loss':'Lottery field remains dependent on both conferences; no draw selected.',
            'selected':False},
        'rules':['No new rating, health, exact contract or season is author-locked.',
            'All1079 rows are conditional exposure/target projections, not official GP or a complete all-player league health ledger.',
            'Fixed-minute lineup optimization changes abstract overlaps only; no chronology, defensive matchup or spacing efficiency is proved.',
            'The big-player set is a stress definition, not a claim that every listed player is a non-shooter or exclusive center.',
            'I Washington joint absence and F emergency-role penalties remain separate; do not silently combine or discard them.',
            'Frontcourt penalty0/1/3/6 is a sensitivity grid, not an empirical estimate or a selected coefficient.'],
        'source_sha256':{p.name:j.cc.sha(p) for p in (j.OUT,j.MINUTES,j.f.OUT,j.f.MINUTES,j.f.e.OUT,j.f.e.d.OUT,
            j.cc.paired.OUT,j.i.h.g.OUT,j.i.h.APPROVAL,j.cc.PRE,S/'CHICAGO_2020_21_PREDEADLINE_DONOR_VECTOR.csv',
            S/'CHICAGO_2020_21_PREDEADLINE_MINUTE_LEDGER.csv',S/'CHICAGO_2020_21_POSTDEADLINE_CAPACITY_VECTOR.csv',LINEUPS,Path(__file__))},
        'season_selected':False,'manuscript_allowed':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    if args.write:
        data=solve();LINEUPS.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    else:data=json.loads(LINEUPS.read_text())
    verify(data);result=build(data)
    if args.write:OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    else:assert result==json.loads(OUT.read_text())
    print(json.dumps({'PASS':True,'lineups':len(data['rows']),'calendar_rows':len(result['calendar']),
        'spacing_counterexamples':len(result['spacing_stress_counterexamples']),
        'unavoidable_overlap_games':sum(r['minimum_excess_big_seconds']>1e-5 for r in data['rows'])}))
