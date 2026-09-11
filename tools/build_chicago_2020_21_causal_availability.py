"""I: primary report anchors, causal episode routing and bounded absence stress.
No historical diagnosis is automatically transferred into the alternate world.
"""
import argparse
import copy
import json
from collections import Counter,defaultdict
from contextlib import contextmanager
from datetime import date
from pathlib import Path
import build_chicago_2020_21_availability_reconciliation as h

f=h.g.f
S=f.S
SOURCES=S.parent/'research/NBA_2020_21_CAUSAL_AVAILABILITY_SOURCES.json'
OUT=S/'CHICAGO_2020_21_CAUSAL_AVAILABILITY.json'
MINUTES=S/'CHICAGO_2020_21_REPORTED_ABSENCE_STRESS.json'
JOINT=S/'CHICAGO_2020_21_JOINT_ABSENCE_STRESS.json'
EPISODES={
 'LAM_WRIST':('LaMelo Ball',['IR05','IR10','IR20'],'NEW_TEAM_INJURY_CONTEXT_REQUIRED'),
 'PORTER_BACK':('Otto Porter Jr.',['IR02'],'INCUMBENT_OBSERVED_MINUTES_RETAINED_CONDITIONALLY'),
 'PORTER_FOOT':('Otto Porter Jr.',['IR08','IR15','IR23','IR28','IR32','IR38'],'NEW_TEAM_INJURY_CONTEXT_REQUIRED'),
 'CARTER_WINTER':('Wendell Carter Jr.',[],'PRIMARY_REASON_UNRECOVERED'),
 'CARTER_ANKLE':('Wendell Carter Jr.',['IR14'],'NEW_TEAM_INJURY_CONTEXT_REQUIRED'),
 'CARTER_EYE':('Wendell Carter Jr.',['IR27','IR31','IR37'],'NEW_TEAM_INJURY_CONTEXT_REQUIRED'),
 'TERRY_ASSIGNMENT':('Tyrell Terry',['IR03'],'OLD_TEAM_ASSIGNMENT_NOT_CARRIED'),
 'TERRY_PERSONAL':('Tyrell Terry',['IR09','IR18','IR24','IR30','IR34'],'PERSONAL_CAUSE_PRIVATE_ALTERNATE_AVAILABILITY_HOLD'),
 'HAMPTON_PROTOCOL':('R.J. Hampton',['IR04'],'OLD_TEAM_EXPOSURE_NOT_CARRIED_AUTOMATICALLY'),
 'HAYES_HIP':('Killian Hayes',['IR01','IR07'],'NEW_TEAM_INJURY_CONTEXT_REQUIRED'),
 'VUCEVIC_ADDUCTOR':('Nikola Vucevic',['IR22'],'QUESTIONABLE_PLUS_OBSERVED_DNP_NOT_AUTOMATIC_TRANSFER'),
 'HOOD_HIP':('Rodney Hood',['IR06','IR19'],'NEW_TEAM_INJURY_CONTEXT_REQUIRED'),
 'HOOD_HAND':('Rodney Hood',['IR36'],'NEW_TEAM_INJURY_CONTEXT_REQUIRED'),
 'BROWN_ANKLE':('Troy Brown Jr.',['IR17','IR21','IR29','IR33','IR35'],'NEW_TEAM_INJURY_CONTEXT_REQUIRED')}
# Four explicit same-game-date OUT anchors in the already computed F subset.
# This is a sensitivity sample, not a calendar-wide injury choice.
STRESS=[('IR07','2021-04-06_ATL_NOP','NOP','Killian Hayes'),
        ('IR06','2021-04-06_LAC_POR','POR','Rodney Hood'),
        ('IR24','2021-05-01_CHA_DET','CHA','Tyrell Terry'),
        ('IR36','2021-05-16_POR_DEN','POR','Rodney Hood')]


def episode(row):
    p,day=row['player'],row['date']
    if p=='Otto Porter Jr.':return 'PORTER_BACK' if day<'2021-03-12' else 'PORTER_FOOT'
    if p=='Wendell Carter Jr.':return 'CARTER_WINTER' if day<'2021-02-16' else ('CARTER_ANKLE' if day=='2021-04-22' else 'CARTER_EYE')
    if p=='Tyrell Terry':return 'TERRY_ASSIGNMENT' if day<'2021-03-16' else 'TERRY_PERSONAL'
    if p=='Rodney Hood':return 'HOOD_HIP' if day<'2021-05-01' else 'HOOD_HAND'
    return {'LaMelo Ball':'LAM_WRIST','R.J. Hampton':'HAMPTON_PROTOCOL','Killian Hayes':'HAYES_HIP',
            'Nikola Vucevic':'VUCEVIC_ADDUCTOR','Troy Brown Jr.':'BROWN_ANKLE'}[p]


@contextmanager
def unavailable(player):
    original=f.e.policy
    def altered(team,day,high,rival_minutes=28):
        removed,targets,donors,receivers,swaps=original(team,day,high,rival_minutes)
        assert player in targets
        return list(set(removed)|{player}),{p:v for p,v in targets.items() if p!=player},donors,receivers,swaps
    f.e.policy=altered
    try:yield
    finally:f.e.policy=original


def solve_stress():
    raw=f.groups();saved=json.loads(f.MINUTES.read_text());variants=[]
    for fact,gid,team,player in STRESS:
        control=next(b for b in saved['branches'] if b['event_id']==gid and b['team']==team and b['profile']=='LOW_MINUTES')
        # Recompute control to ensure no allocator/model change is masquerading as a health effect.
        check=f.allocate(raw[gid,team],'LOW_MINUTES',None,control['role_tier']=='EMERGENCY_CONDITIONAL')
        assert check['alternate_seconds']==control['alternate_seconds']
        with unavailable(player):
            variant=f.allocate(raw[gid,team],'LOW_MINUTES',None)
        variants.append({'source_fact_id':fact,'absent_player':player,'control':control,'variant':variant,
            'scope':'Conditional one-date absence stress only; actual alternate absence is not selected'})
    return {'stage':'O-15F14-I','variants':variants,'selected':False,
            'upstream_minutes_sha256':f.bi.cc.sha(f.MINUTES)}


def verify_minutes(data):
    f.verify_minutes({'branches':[r['variant'] for r in data['variants']]})
    for r in data['variants']:
        b=r['variant'];assert r['absent_player'] in b['removed_players']
        if b['status']=='CAPACITY_HOLD':continue
        assert r['absent_player'] not in b['alternate_seconds']
        assert r['absent_player'] not in b['newcomers']
        assert set(b['newcomers'])==set(r['control']['newcomers'])-{r['absent_player']}


def impacts(data):
    original=f.bi.cc.read(f.INPUTS);maps=f.rating_maps();env=f.bi.cc.envelopes(maps)
    schedule=f.bi.lb.normalized_games();result=[]
    for item in data['variants']:
        control,new=item['control'],item['variant'];gid=control['event_id'];team=control['team']
        game=next(g for g in schedule if g['id']==gid);sign=1 if game['home']==team else -1
        dates=sorted(g['date'] for g in schedule if team in (g['home'],g['away']));i=dates.index(game['date'])
        b2b=i>0 and (date.fromisoformat(dates[i])-date.fromisoformat(dates[i-1])).days==1
        for method in f.bi.METHODS:
            old=next(r for r in original if (r['event_id'],r['profile'],r['method'],r['fatigue'])==(gid,'LOW_MINUTES',method,'0.5'))
            row={'event_id':gid,'team':team,'absent_player':item['absent_player'],'method':method,
                 'fatigue':.5,'source_fact_id':item['source_fact_id'],'selected':False}
            if new['status']=='CAPACITY_HOLD':result.append({**row,'status':'CAPACITY_HOLD'});continue
            diff={p:new['delta_seconds'].get(p,0)-control['delta_seconds'].get(p,0)
                  for p in set(new['delta_seconds'])|set(control['delta_seconds'])}
            effect,unknown=f.bi.cc.form(diff,maps[method],{})
            terms=json.loads(old['unknown_coefficients'])
            for p,n in unknown.items():terms[p]=terms.get(p,0)+sign*n
            terms={p:n for p,n in terms.items() if abs(n)>1e-9}
            workload=lambda b:sum(max(0,n) for n in b['delta_seconds'].values())/2880 if b2b else 0
            increment=sign*(effect-.5*(workload(new)-workload(control)))
            constant=float(old['home_margin_constant'])+increment
            band=f.bi.cc.band(constant,terms,env[method])
            direction='HOME' if band[0]>0 else 'AWAY' if band[1]<0 else 'UNRESOLVED'
            result.append({**row,'status':'CONDITIONAL_STRESS_ONLY','control_home_margin_band':json.loads(old['home_margin_band']),
                'control_direction':old['conditional_sign'],'stress_home_margin_band':band,
                'stress_direction':direction,'direction_changed':direction!=old['conditional_sign'],
                'home_margin_increment_constant':increment,'stress_unknown_coefficients':terms,
                'other_team_minutes_unchanged':True,'opponent_win_transfer_if_chosen':direction in ('HOME','AWAY')})
    return result


def solve_joint():
    d=f.e.d;gid='2021-05-01_DAL_WAS';saved=json.loads(d.OUT.read_text())
    original_groups,original_policy=d.groups,d.policy
    raw={k:v for k,v in original_groups().items() if k[0]==gid}
    try:
        d.groups=lambda:raw
        controls=d.specs()
        expected=[b for b in saved['branches'] if b['event_id']==gid]
        assert controls==expected
        def policy(team,day,high,rival_minutes=28):
            removed,targets,donors,recipients,swaps=original_policy(team,day,high,rival_minutes)
            if team=='WAS':
                absent={'Gary Trent Jr.','Troy Brown Jr.'}
                removed=list(set(removed)|absent)
                targets={p:n for p,n in targets.items() if p not in absent}
            return removed,targets,donors,recipients,swaps
        d.policy=policy
        branches=d.specs()
        witnesses=[d.bi.solve(b,d.ROLES) for b in branches]
        d.verify_minutes(branches,witnesses)
        inputs=d.paired_inputs(branches)
    finally:d.groups,d.policy=original_groups,original_policy
    control_inputs=[r for r in saved['paired_inputs'] if r['event_id']==gid]
    return {'stage':'O-15F14-I','event_id':gid,'source_fact_ids':['IR21','IR25'],
        'absent_players':['Gary Trent Jr.','Troy Brown Jr.'],'branches':branches,'witnesses':witnesses,
        'control_branches':controls,'control_inputs':control_inputs,'paired_inputs':inputs,
        'scope':'Joint same-date absence stress using unchanged D allocator and both-player removal. Not an approved health event.',
        'selected':False,'upstream_sha256':f.bi.cc.sha(d.OUT)}


def joint_season_diagnostics():
    joint=json.loads(JOINT.read_text());full=json.loads(f.OUT.read_text())
    ratings=json.loads(h.g.OUT.read_text())['rival_candidates'][0]['methods']
    schedule=f.bi.lb.normalized_games();gid=joint['event_id'];result=[]
    for stress in joint['paired_inputs']:
        if stress['fatigue']!=.5:continue
        method=stress['method'];rating=ratings[method]['effective_rating']
        matches=[(idx,r) for idx,r in enumerate(full['season_bridge']) if
            r['source_condition']['path_id']==stress['profile']+'/RIVAL_28/FOURNIER_PATH_RETAINED'
            and r['source_condition']['method']==method and r['source_condition']['fatigue']==.5
            and r['shared_rival_rating_open_interval'][0]<rating<r['shared_rival_rating_open_interval'][1]]
        assert len(matches)==2
        ids={c['id'] for c in full['league_cases'] if any(idx in c['bridge_indices'] for idx,r in matches)}
        assert len(ids)==1
        old=matches[0][1];changed=set(old['changed_game_ids'])
        game=next(g for g in schedule if g['id']==gid)
        oldwinner=(game['away'] if game['winner']==game['home'] else game['home']) if gid in changed else game['winner']
        newwinner=game['home'] if stress['conditional_sign']=='HOME' else game['away']
        assert stress['conditional_sign'] in ('HOME','AWAY')
        if newwinner!=oldwinner:changed.symmetric_difference_update({gid})
        games=[{**g,'winner':(g['away'] if g['winner']==g['home'] else g['home']) if g['id'] in changed else g['winner']} for g in schedule]
        wins=f.bi.lb.record_wins(games);seeds=f.e.d.ps.order(games)
        delta={t:wins[t]-old['team_wins'][t] for t in wins if wins[t]!=old['team_wins'][t]}
        assert sum(delta.values())==0 and sum(wins.values())==1080
        result.append({'profile':stress['profile'],'method':method,'fatigue':.5,'rival_minutes':28,
            'rival_effective_rating':rating,'base_case_id':next(iter(ids)),
            'source_bridge_indices':[idx for idx,r in matches],
            'joint_home_margin_band':stress['home_margin_band'],'old_winner':oldwinner,'stress_winner':newwinner,
            'team_win_delta':delta,'team_wins':dict(sorted(wins.items())),'seeds':seeds,
            'chicago_seed_before':old['seeds']['EAST'].index('CHI')+1,'chicago_seed_after':seeds['EAST'].index('CHI')+1,
            'changed_game_ids':sorted(changed),'selected':False,
            'scope':'Only May1 WAS joint absence added to this existing full-season condition; other health assumptions remain unchanged and unapproved.'})
    return result


def build(minutes):
    evidence=json.loads(SOURCES.read_text());facts={r['id']:r for r in evidence['facts']}
    rows=[r for r in f.bi.cc.read(h.CAL) if r['priority']!='NO_AUTOMATIC_HEALTH_INFERENCE']
    groups=defaultdict(list)
    for r in rows:groups[episode(r)].append(r)
    episodes=[]
    for key,rr in sorted(groups.items()):
        player,ids,decision=EPISODES[key]
        assert all(facts[i]['player']==player for i in ids)
        episodes.append({'id':key,'player':player,'source_fact_ids':ids,
            'reason_anchor_found':bool(ids),'causal_onset_and_transferability_verified':False,
            'routing':decision,'priority_row_count':len(rr),'event_ids':[r['event_id'] for r in rr],
            'scope':'Report anchors help investigate these dates; they do not prove identical diagnosis or absence on every date.'})
    # Check for official OUT target-date anchors outside H's prioritization heuristic.
    allrows=f.bi.cc.read(h.CAL);extra=[]
    for fact in facts.values():
        if fact['reported_status']!='OUT':continue
        for r in allrows:
            if (r['scope'],r['player'],r['date'])==('NEW_TEAM_TARGET',fact['player'],fact['game_date']) and r['priority']=='NO_AUTOMATIC_HEALTH_INFERENCE':
                extra.append({'fact_id':fact['id'],'event_id':r['event_id'],'player':r['player'],
                              'meaning':'Primary OUT anchor missed by long-gap/DNP heuristic; exact alternate absence remains unselected'})
    return {'stage':'O-15F14-I','status':'PRIMARY_REASON_ANCHORS_AND_BOUNDED_STRESS_COMPLETE_NOT_SEASON_LOCK',
        'official_reports':len(evidence['sources']),'official_fact_rows':len(facts),'episodes':episodes,
        'priority_rows_routed':len(rows),'rows_with_episode_reason_anchor':sum(x['priority_row_count'] for x in episodes if x['reason_anchor_found']),
        'rows_without_primary_reason':sum(x['priority_row_count'] for x in episodes if not x['reason_anchor_found']),
        'extra_target_date_out_anchors':extra,'bounded_stress':impacts(minutes),
        'joint_restriction_case':{'event_id':'2021-05-01_DAL_WAS',
            'players':['Gary Trent Jr.','Troy Brown Jr.'],'source_fact_ids':['IR21','IR25'],
            'status':'JOINT_STRESS_COMPUTED_NOT_SELECTED','artifact':JOINT.name,
            'reason':'Both official OUT anchors fall on one new-team game date; calculated jointly rather than adding independent single-player effects.'},
        'joint_low_fatigue_half_inputs':[r for r in json.loads(JOINT.read_text())['paired_inputs'] if r['profile']=='LOW_MINUTES' and r['fatigue']==.5],
        'joint_season_diagnostics':joint_season_diagnostics(),
        'source_sha256':{p.name:f.bi.cc.sha(p) for p in (SOURCES,h.CAL,h.OUT,h.APPROVAL,f.OUT,f.MINUTES,f.INPUTS,MINUTES,JOINT,Path(__file__))},
        'rules':['G/H directions remain approved. No new medical event, exact season or impact method is author-locked.',
            'Old-team G League assignment is not automatically carried to Charlotte; this does not approve full-season fitness.',
            'Old-team protocols and private personal reasons are not diagnosed or automatically removed in the new team.',
            'Snapshot reasons, onset mechanisms, recovery intervals and alternate-world causation are separate claims.',
            'Stress changes one targeted player on one date with all other F policies fixed; it is not a new season result.',
            'H priority170/147 is not a coverage guarantee: extra official OUT anchors are retained explicitly.'],
        'new_contract_facts_recovered':False,'season_selected':False,'manuscript_allowed':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    if args.write:
        minutes=solve_stress();MINUTES.write_text(json.dumps(minutes,ensure_ascii=False,indent=2)+'\n')
        JOINT.write_text(json.dumps(solve_joint(),ensure_ascii=False,indent=2)+'\n')
    else:minutes=json.loads(MINUTES.read_text())
    verify_minutes(minutes);data=build(minutes)
    joint=json.loads(JOINT.read_text());f.e.d.verify_minutes(joint['branches'],joint['witnesses'])
    assert f.e.d.paired_inputs(joint['branches'])==joint['paired_inputs']
    if args.write:OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    else:assert json.loads(OUT.read_text())==data
    print(json.dumps({'PASS':True,'reports':data['official_reports'],'episodes':len(data['episodes']),
        'anchored_rows':data['rows_with_episode_reason_anchor'],'unrecovered_rows':data['rows_without_primary_reason'],
        'stress_conditions':len(data['bounded_stress']),'extra_out_anchors':len(data['extra_target_date_out_anchors'])}))
