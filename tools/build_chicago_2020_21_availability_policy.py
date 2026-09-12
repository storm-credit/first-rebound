"""J: finite policy alternatives, replacement-only minutes and whole-season joins.

The Terry March30 cut is an explicit sensitivity boundary (H queue start), not
an inferred medical onset. No policy, diagnosis or season is author-selected.
"""
import argparse
import copy
import itertools
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
import build_chicago_2020_21_causal_availability as i

f=i.f
bi=f.bi
cc=bi.cc
S=f.S
OUT=S/'CHICAGO_2020_21_AVAILABILITY_POLICY.json'
MINUTES=S/'CHICAGO_2020_21_POLICY_REPLACEMENT_MINUTES.json'
PROFILES=bi.PROFILES
METHODS=bi.METHODS
POLICIES={
 'J0_CONTROL':{},
 'J1_TERRY_LEAVE':{'CHA':{'Tyrell Terry':'2021-03-30'}},
 'J2_LEAVE_NO_FOLLOWUPS':{'CHA':{'Tyrell Terry':'2021-03-30'},
     'ORL':{'Donta Hall':'2021-04-13','Moritz Wagner':'2021-04-27'},
     'BOS':{'Jabari Parker':'2021-04-16'}}}
FOLLOWUPS={'EX04_ORL':['Donta Hall','Moritz Wagner'],
           'EX04_BOS':['Jabari Parker'],
           'EX06_DEN':['Austin Rivers','JaVale McGee'],
           'EX06_GSW':['Chandler Hutchison']}


def load():
    schedule={g['id']:g for g in bi.lb.normalized_games()}
    raw={};branches={};inputs={};origins={}
    artifacts=[('B',bi.OUT,bi.groups()),('D',f.e.d.OUT,f.e.d.groups()),
               ('E',f.e.OUT,f.e.groups()),('F',f.MINUTES,f.groups())]
    for stage,path,groups in artifacts:
        assert not set(raw)&set(groups)
        raw.update(groups)
        data=json.loads(path.read_text())
        for b in data['branches']:
            if b.get('rival_minutes') not in (None,28):continue
            profiles=PROFILES if b['profile']=='OBSERVED_HELD' else (b['profile'],)
            for profile in profiles:
                key=b['event_id'],b['team'],profile
                removed,targets,*_=f.e.policy(b['team'],b['date'],profile=='HIGH_MINUTES',28)
                branches[key]={**b,'profile':profile,'removed_players':b.get('removed_players',removed),
                    'newcomers':b.get('newcomers',sorted(targets))}
                origins[key]={'stage':stage,'artifact':path.name,'source_profile':b['profile']}
        rows=cc.read(f.INPUTS) if stage=='F' else data['paired_inputs']
        for r in rows:
            if float(r['fatigue'])!=.5 or r.get('rival_minutes') not in (None,28,'','28'):continue
            rr=copy.deepcopy(r)
            for field in ('home_margin_constant',):rr[field]=float(rr[field])
            if isinstance(rr['unknown_coefficients'],str):rr['unknown_coefficients']=json.loads(rr['unknown_coefficients'])
            inputs[r['event_id'],r['profile'],r['method']]=rr
    paired=json.loads(cc.paired.OUT.read_text())
    for (day,team),rows in cc.paired.actuals().items():
        g=next(g for g in schedule.values() if g['date']==day and 'CHI' in (g['home'],g['away']))
        raw[g['id'],team]=[{**r,'event_id':g['id']} for r in rows]
    for b in paired['opponent_branches']:
        gid=next(g['id'] for g in schedule.values() if g['date']==b['date'] and 'CHI' in (g['home'],g['away']))
        for profile in PROFILES:
            choice=bi.ip.post_choice(b['opponent'],profile,'RIVAL_28','FOURNIER_PATH_RETAINED')
            if b['branch']!=choice:continue
            removed,targets,*_=f.e.policy(b['opponent'],b['date'],profile=='HIGH_MINUTES',28)
            branches[gid,b['opponent'],profile]={**b,'event_id':gid,'team':b['opponent'],
                'profile':profile,'game_duration_seconds':2880,'removed_players':removed,
                'newcomers':sorted(targets),'role_tier':'BASE'}
            origins[gid,b['opponent'],profile]={'stage':'CHI_POST','artifact':cc.paired.OUT.name,
                                                   'source_event_id':b['event_id'],'source_branch':b['branch']}
    return schedule,raw,branches,inputs,origins


def removals(policy,team,day):
    return sorted(p for p,start in POLICIES[policy].get(team,{}).items() if day>=start)


def roles_for(control):
    team=control['team']
    if team=='BOS':
        roles=copy.deepcopy(cc.paired.ROLES['BOS'])
        roles['center']+=['Robert Williams III','Moritz Wagner']
        return roles
    return f.branch_roles(team,control.get('role_tier')=='EMERGENCY_CONDITIONAL')


def replace(control,rows,absent):
    """Keep every survivor's old minutes as a floor and other targets fixed.

    Minimize the maximum added incumbent seconds, then stable name order.
    Only actual active/coach-DNP incumbents may take additional minutes.
    Existing exposure over common F limits is retained but not increased.
    """
    old=control['alternate_seconds'];actual=control['actual_seconds']
    duration=control['game_duration_seconds'];team=control['team']
    new=set(control.get('newcomers',[]))-set(absent)
    removed=set(control.get('removed_players',[]))|set(absent)
    eligible=(bi.allowed(rows)|new|set(old))-removed
    roles=roles_for(control)
    unknown=eligible-set().union(*map(set,roles.values()))
    assert not unknown,(team,unknown)
    players=sorted(eligible)
    lineups=[list(c) for c in itertools.combinations(players,5) if bi.valid(c,team,{team:roles})]
    result={'event_id':control['event_id'],'team':team,'profile':control['profile'],
            'absent_players':absent,'removed_players':sorted(removed),'newcomers':sorted(new),
            'game_duration_seconds':duration,'roles':roles,'selected':False}
    if not lineups:return {**result,'status':'CAPACITY_HOLD','reason':'NO_VALID_FIVE'}
    desired=set(control['starters'])-removed
    starter=min(lineups,key=lambda c:(-len(set(c)&desired),-sum(old.get(p,0) for p in c),c))
    mat=np.array([[p in c for c in lineups] for p in players],float)
    bounds={}
    for p in players:
        lo=old.get(p,0)
        common=max(actual.get(p,0),min(2160+duration-2880,actual[p]+720)) if p in actual else 1200
        hi=lo if p in new else max(lo,common)
        if p not in bi.allowed(rows) and p not in new:hi=lo
        bounds[p]=[lo,hi]
    n=len(lineups)
    A=[];rhs=[]
    for ix,p in enumerate(players):
        A.extend([np.r_[mat[ix],0],np.r_[-mat[ix],0],np.r_[mat[ix],-1]])
        rhs.extend([bounds[p][1],-bounds[p][0],old.get(p,0)])
    costs=np.r_[np.array([sum((players.index(p)+1)*1e-9 for p in c) for c in lineups]),1.]
    solved=linprog(costs,A_ub=np.array(A),b_ub=np.array(rhs),
        A_eq=np.array([np.r_[np.ones(n),0]]),b_eq=[duration],
        bounds=[(180 if c==starter else 0,None) for c in lineups]+[(0,None)],method='highs')
    role_upper={role:sum(bounds.get(p,[0,0])[1] for p in set(ps)) for role,ps in roles.items()}
    certificate={'total_upper_seconds':sum(v[1] for v in bounds.values()),
        'required_total_seconds':5*duration,'role_upper_seconds':role_upper,
        'required_role_seconds':duration,
        'role_shortfalls_seconds':{role:duration-n for role,n in role_upper.items() if n<duration-1e-5},
        'total_shortfall_seconds':max(0,5*duration-sum(v[1] for v in bounds.values()))}
    result.update({'minute_bounds_seconds':bounds,'starters':starter,'capacity_certificate':certificate})
    if not solved.success:return {**result,'status':'CAPACITY_HOLD','reason':solved.message}
    witness=[{'players':c,'seconds':float(v)} for c,v in zip(lineups,solved.x[:n]) if v>1e-7]
    alt={p:sum(w['seconds'] for w in witness if p in w['players']) for p in players}
    alt={p:n for p,n in alt.items() if n>1e-7}
    return {**result,'status':'REPLACEMENT_ONLY_CONDITIONAL','alternate_seconds':alt,
        'delta_seconds':{p:alt.get(p,0)-actual.get(p,0) for p in sorted(set(alt)|set(actual))
                         if abs(alt.get(p,0)-actual.get(p,0))>1e-7},
        'maximum_added_seconds':float(solved.x[-1]),'lineup_witness':witness}


def solve():
    schedule,raw,branches,_,origins=load();records=[]
    # Cache identical joint removals so J2 does not resolve the J1 Terry cases.
    cache={}
    for policy in list(POLICIES)[1:]:
        for (gid,team,profile),control in sorted(branches.items()):
            absent=removals(policy,team,schedule[gid]['date'])
            if not any(control['alternate_seconds'].get(p,0)>0 for p in absent):continue
            key=gid,team,profile,tuple(absent)
            if key not in cache:cache[key]=replace(control,raw[gid,team],absent)
            records.append({'policy':policy,'source':origins[gid,team,profile],
                            'control':control,'variant':cache[key]})
    return {'stage':'O-15F14-J','records':records,'selected':False,
            'replacement_policy':'SURVIVOR_FLOORS_FIXED_TARGETS_MINIMAX_EXTRA_SECONDS',
            'generator_sha256':cc.sha(Path(__file__))}


def verify_minutes(data):
    _,raw,_,_,_=load()
    for r in data['records']:
        b=r['variant'];old=r['control']['alternate_seconds']
        if b['status']=='CAPACITY_HOLD':continue
        alt=b['alternate_seconds'];duration=b['game_duration_seconds']
        assert abs(sum(alt.values())-5*duration)<1e-5
        assert abs(sum(b['delta_seconds'].values()))<1e-5
        assert not set(b['absent_players'])&set(alt)
        assert not set(b['removed_players'])&set(alt)
        seen=Counter();total=start=0
        for w in b['lineup_witness']:
            assert w['seconds']>0 and bi.valid(w['players'],b['team'],{b['team']:b['roles']})
            total+=w['seconds'];start+=w['seconds'] if w['players']==b['starters'] else 0
            for p in w['players']:seen[p]+=w['seconds']
        assert abs(total-duration)<1e-5 and start>=180-1e-5
        assert set(seen)==set(alt) and all(abs(seen[p]-n)<1e-5 for p,n in alt.items())
        for p,(lo,hi) in b['minute_bounds_seconds'].items():assert lo-1e-5<=alt.get(p,0)<=hi+1e-5
        for p,n in alt.items():
            if n>old.get(p,0)+1e-5:assert p in bi.allowed(raw[b['event_id'],b['team']]) and p not in b['newcomers']
        for p in b['newcomers']:assert abs(alt.get(p,0)-old.get(p,0))<1e-5


def chi_inputs(profile,method,availability):
    ip=bi.ip
    data=json.loads(ip.OUT.read_text())
    return {r['date']:r for r in ip.season_games(data['remaining_pre_paired_inputs'],
        json.loads(cc.OUT.read_text()),json.loads(ip.close.OUT.read_text()),profile,'RIVAL_28',
        'FOURNIER_PATH_RETAINED',availability,method,'BASE',.5)}


def impact_records(minutes):
    schedule,_,_,inputs,_=load();maps=f.rating_maps();env=cc.envelopes(maps)
    ratings=json.loads(i.h.g.OUT.read_text())['rival_candidates'][0]['methods']
    chis={(p,m,a):chi_inputs(p,m,a) for p,m,a in itertools.product(PROFILES,METHODS,('PORTER_ZERO','PORTER_CAPPED'))}
    result=[]
    for item in minutes['records']:
        b=item['variant'];control=item['control'];gid=b['event_id'];g=schedule[gid];team=b['team'];profile=b['profile']
        dates=sorted(x['date'] for x in schedule.values() if team in (x['home'],x['away']))
        ix=dates.index(g['date']);b2b=ix>0 and (date.fromisoformat(dates[ix])-date.fromisoformat(dates[ix-1])).days==1
        for method,availability in itertools.product(METHODS,('PORTER_ZERO','PORTER_CAPPED')):
            r={'policy':item['policy'],'event_id':gid,'team':team,'profile':profile,'method':method,
               'availability':availability,'fatigue':.5,'selected':False}
            if b['status']=='CAPACITY_HOLD':result.append({**r,'status':'CAPACITY_HOLD'});continue
            if 'CHI' in (g['home'],g['away']):
                source=chis[profile,method,availability][g['date']];sign=1 if g['home']=='CHI' else -1
                constant=sign*source['constant'];terms={p:sign*n for p,n in source.get('other_unknown_coefficients',{}).items()}
                if source['coefficient']:terms[f.e.RIVAL]=sign*source['coefficient']
                # Upstream CHI postdeadline fatigue charges Chicago only.
                # Do not silently change that model while testing Terry/registrations.
                fatigue_enabled=False
            else:
                source=inputs[gid,profile,method];constant=source['home_margin_constant'];terms=source['unknown_coefficients'].copy()
                fatigue_enabled=True
            oldconstant=constant;oldterms=terms.copy()
            diff={p:b['delta_seconds'].get(p,0)-control['delta_seconds'].get(p,0)
                  for p in sorted(set(b['delta_seconds'])|set(control['delta_seconds']))}
            effect,unknown=cc.form(diff,maps[method],{})
            sign=1 if team==g['home'] else -1
            workload=lambda x:sum(max(0,n) for n in x['delta_seconds'].values())/2880 if b2b and fatigue_enabled else 0
            penalty=.5*(workload(b)-workload(control))
            constant+=sign*(effect-penalty)
            for p,n in unknown.items():terms[p]=terms.get(p,0)+sign*n
            terms={p:n for p,n in terms.items() if abs(n)>1e-8}
            rating=ratings[method]['effective_rating']
            def band(c,t):return cc.band(c+t.get(f.e.RIVAL,0)*rating,{p:n for p,n in t.items() if p!=f.e.RIVAL},env[method])
            oldband=band(oldconstant,oldterms);newband=band(constant,terms)
            direction=lambda b:'HOME' if b[0]>0 else 'AWAY' if b[1]<0 else 'UNRESOLVED'
            result.append({**r,'status':'CONDITIONAL_IMPACT','control_home_margin_band':oldband,
                'control_home_margin_constant':oldconstant,'control_unknown_coefficients':oldterms,
                'home_margin_band':newband,'home_margin_constant':constant,'unknown_coefficients':terms,
                'control_direction':direction(oldband),'direction':direction(newband),
                'replacement_effect':effect,'incremental_workload_penalty':penalty,
                'opponent_unchanged':True,'fatigue_model': 'BOTH_TEAMS_B2B' if fatigue_enabled else 'UPSTREAM_CHI_ONLY',
                'changed_direction':direction(oldband)!=direction(newband)})
    # Pair different teams against one common control. Same-team removals
    # were already solved jointly by replace(), not by summing single shocks.
    grouped=defaultdict(list)
    for r in result:grouped[tuple(r[k] for k in ('policy','event_id','profile','method','availability'))].append(r)
    paired=[]
    for key,rr in sorted(grouped.items()):
        assert len(rr)==len({r['team'] for r in rr})
        policy,gid,profile,method,availability=key
        header={'policy':policy,'event_id':gid,'profile':profile,'method':method,'availability':availability,
                'fatigue':.5,'selected':False,'team_effects':rr}
        if any(r['status']=='CAPACITY_HOLD' for r in rr):
            paired.append({**header,'status':'CAPACITY_HOLD'});continue
        c0=rr[0]['control_home_margin_constant'];t0=rr[0]['control_unknown_coefficients']
        assert all(abs(r['control_home_margin_constant']-c0)<1e-7 and r['control_unknown_coefficients']==t0 for r in rr)
        c=c0+sum(r['home_margin_constant']-c0 for r in rr);terms=t0.copy()
        for r in rr:
            for p in sorted(set(t0)|set(r['unknown_coefficients'])):terms[p]=terms.get(p,0)+r['unknown_coefficients'].get(p,0)-t0.get(p,0)
        terms={p:n for p,n in terms.items() if abs(n)>1e-8}
        rating=ratings[method]['effective_rating']
        band=cc.band(c+terms.get(f.e.RIVAL,0)*rating,{p:n for p,n in terms.items() if p!=f.e.RIVAL},env[method])
        direction='HOME' if band[0]>0 else 'AWAY' if band[1]<0 else 'UNRESOLVED'
        paired.append({**header,'status':'CONDITIONAL_IMPACT','home_margin_constant':c,'unknown_coefficients':terms,
            'home_margin_band':band,'control_home_margin_band':rr[0]['control_home_margin_band'],
            'control_direction':rr[0]['control_direction'],'direction':direction,
            'changed_direction':direction!=rr[0]['control_direction']})
    return paired


def seasons(impacts):
    full=json.loads(f.OUT.read_text());schedule=bi.lb.normalized_games();ratings=json.loads(i.h.g.OUT.read_text())['rival_candidates'][0]['methods'];result=[]
    for policy,profile,method,availability in itertools.product(POLICIES,PROFILES,METHODS,('PORTER_ZERO','PORTER_CAPPED')):
        rating=ratings[method]['effective_rating']
        matches=[(idx,r) for idx,r in enumerate(full['season_bridge']) if
            r['source_condition']['path_id']==profile+'/RIVAL_28/FOURNIER_PATH_RETAINED' and
            (r['source_condition']['method'],r['source_condition']['availability'],r['source_condition']['fatigue'])==(method,availability,.5)
            and r['shared_rival_rating_open_interval'][0]<rating<r['shared_rival_rating_open_interval'][1]]
        assert len(matches)==1
        idx,old=matches[0];basecase=next(c['id'] for c in full['league_cases'] if idx in c['bridge_indices'])
        rr=[r for r in impacts if (r['policy'],r['profile'],r['method'],r['availability'])==(policy,profile,method,availability)]
        assert len(rr)==len({r['event_id'] for r in rr}), 'Joint same-game impacts must be recomputed, never summed'
        held=[r['event_id'] for r in rr if r['status']=='CAPACITY_HOLD' or r.get('direction')=='UNRESOLVED']
        header={'policy':policy,'profile':profile,'method':method,'availability':availability,'base_case_id':basecase,
            'rival_effective_rating':rating,'rival_minutes':28,'fatigue':.5,'selected':False,
            'affected_games':len(rr),'unresolved_game_ids':held}
        if held:
            result.append({**header,'status':'INCOMPLETE_NO_ACTUAL_RESULT_FILL','team_wins':None,'seeds':None});continue
        changed=set(old['changed_game_ids']);lookup={r['event_id']:r for r in rr};flips=[];games=[]
        for g in schedule:
            before=(g['away'] if g['winner']==g['home'] else g['home']) if g['id'] in changed else g['winner']
            after=before
            if g['id'] in lookup:
                r=lookup[g['id']]
                assert before==(g['home'] if r['control_direction']=='HOME' else g['away']), (g['id'],before,r)
                after=g['home'] if r['direction']=='HOME' else g['away']
            if before!=after:flips.append({'event_id':g['id'],'before':before,'after':after})
            games.append({**g,'winner':after})
        wins=bi.lb.record_wins(games);delta={t:wins[t]-old['team_wins'][t] for t in wins if wins[t]!=old['team_wins'][t]}
        assert sum(wins.values())==1080 and sum(delta.values())==0
        try:seeds=f.e.d.ps.order(games);tie=None
        except ValueError as err:seeds=None;tie=str(err)
        result.append({**header,'status':'FULL_CONDITIONAL_SCHEDULE' if seeds else 'TIE_HOLD',
            'team_wins':dict(sorted(wins.items())),'seeds':seeds,'tie_hold':tie,'team_win_delta':delta,'flips':flips,
            'chicago_seed_before':old['seeds']['EAST'].index('CHI')+1,
            'chicago_seed_after':seeds['EAST'].index('CHI')+1 if seeds else None,
            'changed_game_ids':sorted(g['id'] for g in games if g['winner']!=next(x['winner'] for x in schedule if x['id']==g['id']))})
    return result


def footprint():
    schedule,raw,branches,_,_=load();result=[]
    for gate,players in FOLLOWUPS.items():
        team=gate.rsplit('_',1)[1]
        for player in players:
            dates=[]
            for gid,g in sorted(schedule.items()):
                if team not in (g['home'],g['away']) or g['date']<'2021-03-25':continue
                bs=[branches.get((gid,team,p)) for p in PROFILES]
                # Predeadline CHI dates are outside this followup window.
                assert all(bs),(gid,team)
                minutes=[b['alternate_seconds'].get(player,0)/60 for b in bs]
                dates.append({'event_id':gid,'target_minutes_low_high':minutes,
                    'positive_allocated':any(n>0 for n in minutes)})
            result.append({'gate':gate,'team':team,'player':player,'audited_dates':len(dates),
                'positive_dates':sum(r['positive_allocated'] for r in dates),'calendar':dates,
                'scope':'Current conditional minute exposure, not a recovered contract or destination.'})
    return result


def build(minutes):
    impacts=impact_records(minutes);i_data=json.loads(i.OUT.read_text())
    policies=[{'id':key,'removals':value,'selected':False} for key,value in POLICIES.items()]
    pre=cc.read(cc.PRE);delta=cc.read(cc.ROLES.parent/'CHICAGO_2020_21_PREDEADLINE_DONOR_VECTOR.csv')
    winter=[]
    for ep in i_data['episodes']:
        if ep['id'] not in ('CARTER_WINTER','PORTER_BACK'):continue
        for gid in ep['event_ids']:
            actual=sum(int(r['seconds']) for r in pre if (r['date'],r['team'],r['player'])==(gid[:10],'CHI',ep['player']))
            change=sum(int(r['delta_seconds']) for r in delta if (r['date'],r['player'])==(gid[:10],ep['player']))
            assert actual==change==0
            winter.append({'episode':ep['id'],'event_id':gid,'player':ep['player'],
                'actual_seconds':actual,'alternate_seconds':actual+change,
                'status':'ALREADY_ZERO_IN_EXISTING_MINUTE_MODEL_NOT_MEDICAL_ONSET_PROOF'})
    return {'stage':'O-15F14-J','status':'POLICY_ALTERNATIVES_AND_SEASON_EFFECTS_NOT_AUTHOR_LOCK',
        'policies':policies,'replacement_records':len(minutes['records']),
        'recommended_review_candidate':'J1_TERRY_LEAVE','recommendation_is_author_approval':False,
        'j2_disposition':'NOT_EXECUTABLE_UNDER_CURRENT_MINUTE_AND_ROLE_POLICY',
        'chicago_winter_existing_zero_minutes':winter,
        'replacement_statuses':dict(Counter(r['variant']['status'] for r in minutes['records'])),
        'impacts':impacts,'season_diagnostics':seasons(impacts),'followup_exposure':footprint(),
        'episode_routes':i_data['episodes'],
        'decision_axes':['Existing Chicago observed health remains conditional; winter26 priority rows already represented, no new diagnosis.',
            'New-team old injury/assignment/protocol calendars are not automatically copied or erased; existing target minutes remain assumptions.',
            'Terry leave from March30 through season end is an explicit stress calendar based on H queue boundary, not verified onset/duration.',
            'J2 tests removal of ORL Hall/Wagner and BOS Parker only; their free-agent destinations, replacement contracts and Birch retention are not inferred.'],
        'scope':['R1 benchmark and fatigue0.5, LOW/HIGH and both Porter policies; not all1198 rating intervals.',
            'I Washington joint absence is a separate stress and is not silently included in J scenarios.',
            'Replacement-only policy keeps survivor minutes floors, fixes other targets and minimizes largest extra workload without scores or ratings.',
            'Missing capacity or margin signs stop a full-season result; no historical winner is inserted.',
            'All other health, registration and emergency-role costs remain existing conditional assumptions.'],
        'new_contract_or_medical_facts':False,'season_selected':False,'manuscript_allowed':False,
        'source_sha256':{p.name:cc.sha(p) for p in (i.OUT,i.SOURCES,i.h.OUT,i.h.CAL,i.h.APPROVAL,f.OUT,
            f.MINUTES,f.INPUTS,bi.OUT,f.e.d.OUT,f.e.OUT,cc.paired.OUT,cc.OUT,cc.PRE,
            S/'CHICAGO_2020_21_PREDEADLINE_DONOR_VECTOR.csv',MINUTES,Path(__file__))}}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    if args.write:
        minutes=solve();MINUTES.write_text(json.dumps(minutes,ensure_ascii=False,indent=2)+'\n')
    else:minutes=json.loads(MINUTES.read_text())
    verify_minutes(minutes);data=build(minutes)
    if args.write:OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    else:assert json.loads(OUT.read_text())==data
    print(json.dumps({'PASS':True,'records':data['replacement_records'],'statuses':data['replacement_statuses'],
        'seasons':dict(Counter(r['status'] for r in data['season_diagnostics']))}))
