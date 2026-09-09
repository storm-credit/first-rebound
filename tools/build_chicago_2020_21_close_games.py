"""O-15F11 close-game allocation witnesses and paired margins; no canon outcomes.
--write solves only these new opponent allocations. Default checks saved witnesses.
"""
import argparse
import itertools
import json
from collections import defaultdict
from pathlib import Path
import build_chicago_2020_21_season_connection as connection
import crosscheck_chicago_2020_21_impact as cc

S=connection.S
OUT=S/'CHICAGO_2020_21_CLOSE_GAME_PATHS.json'
DATES={'2020-12-27':'GSW','2021-01-05':'POR','2021-01-30':'POR'}
POLICIES=('INCUMBENTS','EVANS_CAP_12','EVANS_CAP_24','EVANS_FULL_SLOT')
ROLES={
 'POR':{'handler':{'Damian Lillard','CJ McCollum','Anfernee Simons'},
        'center':{'Enes Freedom','Jusuf Nurkic','Harry Giles III','Robert Covington'},
        'wing':{'Carmelo Anthony','Derrick Jones Jr.','Nassir Little','Rodney Hood','Robert Covington','Jacob Evans'}},
 'GSW':{'handler':{'Stephen Curry','Jordan Poole','Brad Wanamaker'},
        'center':{'James Wiseman','Kevon Looney','Eric Paschall'},
        'wing':{'Andrew Wiggins','Kelly Oubre Jr.','Damion Lee','Juan Toscano-Anderson','Mychal Mulder','Chandler Hutchison'}}}

def valid(players,team):
 return len(players)==len(set(players))==5 and all(set(players)&r for r in ROLES[team].values())

def specs():
 obs=cc.read(cc.PRE); result=[]
 for date,team in DATES.items():
  rows=[r for r in obs if (r['date'],r['team'])==(date,team)]
  base={r['player']:int(r['seconds']) for r in rows if int(r['seconds'])}
  clock=14400-sum(base.values());assert abs(clock)<=2
  fixed=max(base,key=lambda p:(base[p],p)) if clock else None
  if fixed:base[fixed]+=clock
  starts=sorted(r['player'] for r in rows if r['start']=='1')
  choices=POLICIES if team=='POR' else ('HUTCHISON_INACTIVE','HUTCHISON_12','HUTCHISON_24')
  for policy in choices:
   alt=dict(base); starters=list(starts); assumptions=[]
   if team=='POR':
    removed=alt.pop('Gary Trent Jr.'); evans=0 if policy=='INCUMBENTS' else min(removed,720 if policy=='EVANS_CAP_12' else 1440 if policy=='EVANS_CAP_24' else removed)
    if evans:alt['Jacob Evans']=evans
    remaining=removed-evans
    # Fixed recipient order/caps, chosen for roles before observing impact results.
    choices=[('Anfernee Simons',600),('Nassir Little',516)] if date=='2021-01-05' else [('Anfernee Simons',480),('Rodney Hood',600),('Nassir Little',600),('Carmelo Anthony',522)]
    for p,capacity in choices:
     n=min(remaining,capacity)
     if n:alt[p]=alt.get(p,0)+n
     remaining-=n
    assert remaining==0
    if 'Gary Trent Jr.' in starters:
     starters[starters.index('Gary Trent Jr.')]='Anfernee Simons'
    assumptions=['Trent absent under existing Portland cascade', 'Existing players retain this date availability; added workload is a coaching assumption', 'Evans minutes require Portland registration and availability; zero minutes do not establish release or injury']
   else:
    if policy!='HUTCHISON_INACTIVE':
     donor=[('Kelly Oubre Jr.',360),('Mychal Mulder',360)] if policy=='HUTCHISON_12' else [('Kelly Oubre Jr.',600),('Mychal Mulder',634),('Damion Lee',206)]
     for p,n in donor:alt[p]-=n
     alt['Chandler Hutchison']=sum(n for _,n in donor)
    assumptions=['Russell-Wiggins core transaction retained conditionally', 'Hutchison inactive/active is a scenario; destination and availability unresolved', 'Active scenarios conditionally retain Hutchison at GSW; no roster place or transaction authorization implied']
   alt={p:n for p,n in sorted(alt.items()) if n>0}
   result.append({'date':date,'opponent':team,'policy':policy,'actual_seconds':base,'alternate_seconds':alt,'starters':sorted(starters),'delta_seconds':{p:alt.get(p,0)-base.get(p,0) for p in sorted(set(base)|set(alt)) if alt.get(p,0)!=base.get(p,0)},'clock_correction':{'player':fixed,'seconds':clock},'assumptions':assumptions})
 return result

def solve(spec):
 import numpy as np
 from scipy.optimize import linprog
 players=list(spec['alternate_seconds']);lineups=[c for c in itertools.combinations(players,5) if valid(c,spec['opponent'])]
 starts=tuple(spec['starters']);assert starts in lineups
 matrix=np.array([[int(p in c) for c in lineups] for p in players]+[[1]*len(lineups)])
 target=[spec['alternate_seconds'][p] for p in players]+[2880]
 result=linprog(np.zeros(len(lineups)),A_eq=matrix,b_eq=target,bounds=[(180 if c==starts else 0,None) for c in lineups],method='highs')
 assert result.success,(spec['date'],spec['policy'],result.message)
 return [{'players':list(c),'seconds':round(float(v),8)} for c,v in zip(lineups,result.x) if v>1e-6]

def build(witnesses):
 cross=json.loads(cc.OUT.read_text());maps=cc.rating_maps();branches=specs();inputs=[]
 for b in branches:
  for r in cross['pre_opponent_held_inputs']:
   if r['date']!=b['date'] or r['method'] not in connection.METHODS:continue
   opp,terms=cc.form(b['delta_seconds'],maps[r['method']],{})
   terms={p:-v for p,v in terms.items()}
   for i,penalty in enumerate(cc.FATIGUE):
    intercept=r['opponent_held_margin'][i]-opp
    # Unknown coefficients remain symbolic; never count intercept-only as outcome.
    band=cc.band(intercept,terms,cross['envelopes'][r['method']])
    inputs.append({'date':b['date'],'opponent':b['opponent'],'policy':b['policy'],'method':r['method'],'prior':r['prior'],'fatigue':penalty,'margin_constant':round(intercept,8),'unknown_rating_coefficients':terms,'opponent_margin_constant':round(-intercept,8),'opponent_unknown_rating_coefficients':{p:-v for p,v in terms.items()},'margin_stress_band':band,'numeric_sign':('CHI_POSITIVE' if intercept>0 else 'CHI_NEGATIVE' if intercept<0 else 'ZERO_UNRESOLVED') if not terms else None,'break_even_ratings':{p:round(-intercept/v,8) for p,v in terms.items()} if len(terms)==1 else {},'status':'CONDITIONAL_DIAGNOSTIC_NOT_GAME_RESULT'})
 joint=[]
 for policy in POLICIES:
  for method in connection.METHODS:
   for prior in connection.SCEN:
    rows=[r for r in inputs if r['opponent']=='POR' and (r['policy'],r['method'],r['prior'],r['fatigue'])==(policy,method,prior,0)]
    assert len(rows)==2
    # Same Evans rating on both dates; method families have different units.
    cuts=sorted(set(v for r in rows for v in r['break_even_ratings'].values()))
    bounds=[None,*cuts,None]
    for lo,hi in zip(bounds,bounds[1:]):
     rating=(hi-1 if lo is None and hi is not None else lo+1 if hi is None and lo is not None else (lo+hi)/2 if lo is not None else 0)
     signs=[r['margin_constant']+sum(v*rating for v in r['unknown_rating_coefficients'].values())>0 for r in rows]
     joint.append({'policy':policy,'method':method,'prior':prior,'open_interval_evans_rating':[lo,hi],'chi_positive_dates':[r['date'] for r,pos in zip(rows,signs) if pos],'equality_at_break_even':'UNRESOLVED_ZERO_MARGIN','meaning':'JOINT_CONDITIONAL_SIGNS_NOT_WINS'})
 return {'stage':'O-15F11','status':'CLOSE_GAME_ALLOCATION_AND_SENSITIVITY_PASS_SEASON_HOLD','base_main':'e74e3da37cd91bd4bf305c494394084ddac6eca9','branches':branches,'lineup_witnesses':witnesses,'paired_inputs':inputs,'portland_joint_rating_intervals':joint,'recommended_working_policies':{'POR':'INCUMBENTS','GSW':'HUTCHISON_INACTIVE'},'recommendation_scope':'Conditional working allocation only; active alternatives retained, not a canon transaction/availability/outcome selection','selected_season_path':False,'manuscript_allowed':False,'input_sha256':{p.name:cc.sha(p) for p in (cc.PRE,cc.OUT,connection.OUT,Path(__file__))},'roles':{t:{k:sorted(v) for k,v in roles.items()} for t,roles in ROLES.items()}}

def verify(j):
 obs=cc.read(cc.PRE)
 assert len(j['branches'])==11 and len(j['paired_inputs'])==198
 for b,w in zip(j['branches'],j['lineup_witnesses'],strict=True):
  assert sum(b['alternate_seconds'].values())==14400 and sum(b['delta_seconds'].values())==0
  assert max(b['alternate_seconds'].values())<=2400
  seen=defaultdict(float);total=0;starter=0
  for x in w:
   assert x['seconds']>0 and valid(x['players'],b['opponent'])
   total+=x['seconds'];starter+=x['seconds'] if sorted(x['players'])==b['starters'] else 0
   for p in x['players']:seen[p]+=x['seconds']
  assert abs(total-2880)<1e-5 and starter>=180-1e-5
  assert set(seen)==set(b['alternate_seconds'])
  assert all(abs(seen[p]-n)<1e-5 for p,n in b['alternate_seconds'].items())
  for p,n in b['delta_seconds'].items():
   if n>0 and p not in ['Jacob Evans','Chandler Hutchison']:
    r=next(r for r in obs if (r['date'],r['team'],r['player'])==(b['date'],b['opponent'],p))
    assert int(r['seconds'])>0 or r['comment']=="DNP - Coach's Decision"
 for r in j['paired_inputs']:
  assert abs(r['margin_constant']+r['opponent_margin_constant'])<1e-7
  assert all(r['opponent_unknown_rating_coefficients'][p]==-v for p,v in r['unknown_rating_coefficients'].items())
  if r['unknown_rating_coefficients']:assert r['numeric_sign'] is None
 assert j==build(j['lineup_witnesses'])
 print('PASS O-15F11: 11 allocations / 198 paired conditions; 5-player witnesses, 240 minutes, symbolic Evans and joint-date intervals; no canon outcomes')

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
 if args.write:
  j=build([solve(b) for b in specs()]);verify(j);OUT.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
 else:verify(json.loads(OUT.read_text()))
