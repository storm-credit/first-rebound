"""O-15F12: remaining predeadline allocations and coherent conditional 72-game paths.
Default verifies saved witnesses; --write solves only new opponent allocations.
"""
import argparse
import itertools
import json
from collections import defaultdict
from pathlib import Path
import crosscheck_chicago_2020_21_impact as cc
import build_chicago_2020_21_paired_impact as paired
import build_chicago_2020_21_close_games as close

S=cc.S
OUT=S/'CHICAGO_2020_21_INTEGRATED_PATHS.json'
METHODS=('RAPTOR_RS_EB','BPM_MAR25_EB')
PROFILES=('LOW_MINUTES','HIGH_MINUTES')
RIVAL='Fictional Rival'
ROLES={
 'WAS':{'handler':['Russell Westbrook','Bradley Beal','Ish Smith','Raul Neto'],
        'center':['Thomas Bryant','Robin Lopez','Moritz Wagner','Alex Len','Anthony Gill'],
        'wing':['Gary Trent Jr.','Bradley Beal','Deni Avdija','Troy Brown Jr.','Davis Bertans','Rui Hachimura','Garrison Mathews']},
 'DAL':{'handler':['Luka Doncic','Jalen Brunson','Trey Burke','R.J. Hampton'],
        'center':['Dwight Powell','Willie Cauley-Stein','Boban Marjanovic','Maxi Kleber','Kristaps Porzingis'],
        'wing':['Josh Richardson','Tim Hardaway Jr.','Dorian Finney-Smith','Wes Iwundu','Josh Green','James Johnson','R.J. Hampton']},
 'CHA':{'handler':["Devonte' Graham",'Terry Rozier','Tyrell Terry','Malik Monk'],
        'center':['Bismack Biyombo','Cody Zeller','P.J. Washington'],
        'wing':['Anthony Edwards','Gordon Hayward','Caleb Martin','Cody Martin','Miles Bridges']},
 'LAL':{'handler':['LeBron James','Dennis Schroder','Alex Caruso','Quinn Cook','Talen Horton-Tucker'],
        'center':['Marc Gasol','Montrezl Harrell','Anthony Davis','Markieff Morris'],
        'wing':['LeBron James','Kyle Kuzma','Wesley Matthews','Kentavious Caldwell-Pope','Talen Horton-Tucker','Alfonzo McKinnie']},
 'NOP':{'handler':['Lonzo Ball','Eric Bledsoe','Killian Hayes','Nickeil Alexander-Walker'],
        'center':['Steven Adams','Willy Hernangomez','Jaxson Hayes','Zion Williamson'],
        'wing':['Brandon Ingram','Josh Hart','JJ Redick','Zion Williamson']},
 'DET':{'handler':['Delon Wright','Dennis Smith Jr.','Kira Lewis Jr.','Saben Lee','Frank Jackson'],
        'center':['Mason Plumlee','Isaiah Stewart'],
        'wing':['Patrick Williams','Jerami Grant','Josh Jackson','Wayne Ellington','Svi Mykhailiuk','Frank Jackson','Sekou Doumbouya']},
 'DEN':{'handler':['Jamal Murray','Monte Morris','Facundo Campazzo','PJ Dozier','Nikola Jokic'],
        'center':['Nikola Jokic','Isaiah Hartenstein','Paul Millsap','JaMychal Green'],
        'wing':['Saddiq Bey','Will Barton','Michael Porter Jr.','Vlatko Cancar','PJ Dozier']},
 'MIN':{'handler':['Ricky Rubio','Jordan McLaughlin','Jaylen Nowell'],
        'center':['Karl-Anthony Towns','Naz Reid','Ed Davis'],
        'wing':[RIVAL,'Malik Beasley','Jaden McDaniels','Josh Okogie','Jarrett Culver']}}


def valid(players,team):
 return len(players)==len(set(players))==5 and all(set(players)&set(v) for v in ROLES[team].values())


def balance(alt,total,donors,recipients):
 gap=total-sum(alt.values());moves=[]
 choices=recipients if gap>0 else donors
 for player,minutes in choices:
  old=alt.get(player,0)
  change=min(gap,max(0,minutes*60-old)) if gap>0 else -min(-gap,max(0,old-minutes*60))
  if change:
   alt[player]=old+change;gap-=change;moves.append({'player':player,'seconds':change,'limit_minutes':minutes})
  if gap==0:break
 assert gap==0,(gap,alt)
 return moves


def specs():
 obs=cc.read(cc.PRE);queue=cc.read(cc.QUEUE);result=[]
 for q in queue:
  if q['status']!='OPPONENT_DELTA_UNALLOCATED' or q['opponent'] in ('GSW','POR'):continue
  date,team=q['date'],q['opponent'];rows=[r for r in obs if (r['date'],r['team'])==(date,team)]
  base={r['player']:int(r['seconds']) for r in rows if int(r['seconds'])};raw_total=sum(base.values())
  # Normalize only the source's <=2-second residual; preserve five-minute OT periods.
  overtime=round((raw_total-14400)/1500);duration=2880+300*overtime;total=duration*5
  assert overtime>=0 and abs(total-raw_total)<=2
  fix=total-raw_total;fixed=max(base,key=lambda p:(base[p],p)) if fix else None
  if fixed:base[fixed]+=fix
  starts=sorted(r['player'] for r in rows if r['start']=='1')
  profiles=('CORE_RETAINED',) if team=='LAL' else ('RIVAL_24','RIVAL_28','RIVAL_32') if team=='MIN' else PROFILES
  for profile in profiles:
   hi=profile=='HIGH_MINUTES';alt=dict(base);starters=list(starts);targets={};donors=[];recipients=[];notes=[]
   removed=q['removed_actual_players'].split(';') if q['removed_actual_players'] else []
   for p in removed:alt.pop(p,None)
   if team=='WAS':
    targets={'Gary Trent Jr.':28 if hi else 24}
    donors=[('Troy Brown Jr.',0),('Garrison Mathews',0),('Davis Bertans',20),('Deni Avdija',16),('Bradley Beal',32)]
    starters=['Gary Trent Jr.' if p=='Isaac Bonga' else p for p in starters]
   elif team=='DAL':
    targets={'R.J. Hampton':18 if hi else 12}
    donors=[('Trey Burke',8),('Nate Hinton',0),('Josh Green',16),('Wes Iwundu',20),('Tim Hardaway Jr.',28),('Jalen Brunson',32)]
    recipients=[('Nate Hinton',12),('Josh Green',36)]
   elif team=='CHA':
    targets={'Anthony Edwards':28 if hi else 24,'Tyrell Terry':6}
    donors=[('Caleb Martin',6),('Miles Bridges',12)]
   elif team=='NOP':
    targets={'Killian Hayes':20 if hi else 16}
    donors=[('Eric Bledsoe',32),('JJ Redick',20),('Josh Hart',28)]
    recipients=[('Nickeil Alexander-Walker',18),('Josh Hart',32)]
   elif team=='DET':
    targets={'Patrick Williams':30 if hi else 28,'Kira Lewis Jr.':24 if hi else 20}
    donors=[('Dennis Smith Jr.',6),('Saben Lee',0),('Delon Wright',30),('Josh Jackson',24),('Wayne Ellington',20)]
    starters=['Patrick Williams' if p=='Saddiq Bey' else p for p in starters]
   elif team=='DEN':
    targets={'Saddiq Bey':24 if hi else 20}
    donors=[('Vlatko Cancar',0),('JaMychal Green',8),('Paul Millsap',8),('Will Barton',30),('Michael Porter Jr.',32)]
    # Avoid assigning Nnaji a full-time center role to cover a 39-second hole.
    center_sum=sum(alt.get(p,0) for p in ROLES[team]['center'])
    if center_sum<duration:
     deficit=duration-center_sum
     assert 'Isaiah Hartenstein' in alt
     alt['Isaiah Hartenstein']+=deficit
     notes.append({'center_coverage_extra_seconds':deficit,'player':'Isaiah Hartenstein'})
   elif team=='MIN':
    targets={RIVAL:int(profile.split('_')[1])}
    center_gap=max(0,duration-sum(alt.get(p,0) for p in ROLES[team]['center']))
    if center_gap:
     alt['Naz Reid']+=center_gap;notes.append({'center_coverage_extra_seconds':center_gap,'player':'Naz Reid'})
    recipients=[('Jaden McDaniels',26),('Josh Okogie',24)]
    starters=[RIVAL if p=='Anthony Edwards' else p for p in starters]
    notes.append({'role_cost':'Rival rating is a shared effective impact variable; no extra Towns/Russell creation bonus. Russell absent from this date source stays unallocated.'})
   else:
    assert team=='LAL';notes.append({'condition':'AD/Trent upstream cascade and incumbent roster retained; observed minutes held only under this condition'})
   alt.update({p:m*60 for p,m in targets.items()})
   moves=balance(alt,total,donors,recipients);alt={p:n for p,n in sorted(alt.items()) if n>0}
   result.append({'event_id':q['event_id'],'date':date,'opponent':team,'profile':profile,'raw_total_seconds':raw_total,'game_duration_seconds':duration,'clock_correction':{'player':fixed,'seconds':fix},'actual_seconds':base,'alternate_seconds':alt,'delta_seconds':{p:alt.get(p,0)-base.get(p,0) for p in sorted(set(base)|set(alt)) if alt.get(p,0)!=base.get(p,0)},'starters':sorted(starters),'target_minutes':targets,'balance_moves':moves,'notes':notes,'source':q['canon_evidence'],'status':'CONDITIONAL_ALLOCATION_NOT_AVAILABILITY_LOCK'})
 return result


def solve(b):
 import numpy as np
 from scipy.optimize import linprog
 players=list(b['alternate_seconds']);ls=[c for c in itertools.combinations(players,5) if valid(c,b['opponent'])];starts=tuple(b['starters']);assert starts in ls,(b['date'],starts)
 mat=np.array([[int(p in c) for c in ls] for p in players]+[[1]*len(ls)])
 target=list(b['alternate_seconds'].values())+[b['game_duration_seconds']]
 result=linprog(np.zeros(len(ls)),A_eq=mat,b_eq=target,bounds=[(180 if c==starts else 0,None) for c in ls],method='highs')
 assert result.success,(b['date'],b['profile'],result.message)
 return [{'players':list(c),'seconds':round(float(n),8)} for c,n in zip(ls,result.x) if n>1e-6]


def paired_inputs(branches):
 cross=json.loads(cc.OUT.read_text());maps=cc.rating_maps();result=[]
 for b in branches:
  for row in cross['pre_opponent_held_inputs']:
   if row['date']!=b['date'] or row['method'] not in METHODS:continue
   opp,terms=cc.form(b['delta_seconds'],maps[row['method']],{})
   assert set(terms)<= {RIVAL},terms
   for i,fatigue in enumerate(cc.FATIGUE):
    margin=row['opponent_held_margin'][i]-opp
    result.append({'date':b['date'],'opponent':b['opponent'],'profile':b['profile'],'method':row['method'],'prior':row['prior'],'fatigue':fatigue,'margin_constant':round(margin,8),'rival_coefficient':-terms.get(RIVAL,0),'opponent_margin_constant':round(-margin,8),'opponent_rival_coefficient':terms.get(RIVAL,0),'numeric_outcome':None if terms else 'POSITIVE' if margin>0 else 'NEGATIVE' if margin<0 else 'ZERO_UNRESOLVED'})
 return result


def post_choice(team,profile,rival,boston):
 hi=profile=='HIGH_MINUTES'
 return {'GSW':'WIGGINS_CORE_HUTCHISON_INACTIVE','TOR':'POWELL_RETAINED_32' if hi else 'POWELL_RETAINED_28','ORL':'VUCEVIC_STAYS_GORDON_A_NNAJI_12' if hi else 'VUCEVIC_STAYS_GORDON_A_NNAJI_8','MIN':rival,'CHA':'EDWARDS_28_TERRY_6' if hi else 'EDWARDS_24_TERRY_6','DET':'PATRICK_30_KIRA_24' if hi else 'PATRICK_28_KIRA_20','BOS':boston}.get(team,'OBSERVED_OPPONENT_HELD')


def season_games(inputs,cross,close_data,profile,rival,boston,availability,method,prior,fatigue):
 fi=list(cc.FATIGUE).index(fatigue);pre=[r for r in cross['pre_opponent_held_inputs'] if (r['method'],r['prior'])==(method,prior)];games=[]
 for r in pre:
  t=r['opponent'];m=r['opponent_held_margin'][fi];co=0;policy='LIMITED_BASELINE';phase='PRE'
  if t in ('GSW','POR'):
   policy='INCUMBENTS' if t=='POR' else 'HUTCHISON_INACTIVE'
   matching=[a for a in close_data['paired_inputs'] if (a['date'],a['policy'],a['method'],a['prior'],a['fatigue'])==(r['date'],policy,method,prior,fatigue)]
   assert len(matching)==1 and not matching[0]['unknown_rating_coefficients'];m=matching[0]['margin_constant']
  elif any(a['date']==r['date'] for a in inputs):
   policy=rival if t=='MIN' else 'CORE_RETAINED' if t=='LAL' else profile
   matching=[a for a in inputs if (a['date'],a['profile'],a['method'],a['prior'],a['fatigue'])==(r['date'],policy,method,prior,fatigue)]
   assert len(matching)==1; m=matching[0]['margin_constant'];co=matching[0]['rival_coefficient']
  games.append({'date':r['date'],'opponent':t,'phase':phase,'branch':policy,'constant':m,'coefficient':co,'actual_margin':r['actual_margin']})
 postdates=sorted({r['date'] for r in cross['post_inputs']})
 for d in postdates:
  rows=[r for r in cross['post_inputs'] if r['date']==d];team=rows[0]['opponent'];policy=post_choice(team,profile,rival,boston)
  rows=[r for r in rows if (r['branch'],r['availability'],r['method'],r['prior'])==(policy,availability,method,prior)]
  assert len(rows)==1,(d,policy)
  r=rows[0];constant=r['margin_constant']+r['fatigue_deltas'][fi]
  nuisance={p:v for p,v in r['unknown_rating_coefficients'].items() if p!=RIVAL}
  assert not (nuisance and RIVAL in r['unknown_rating_coefficients'])
  nb=cc.band(constant,nuisance,cross['envelopes'][method])
  # Other unknowns may be omitted from the count only after proving sign stability.
  assert not nuisance or nb[0]>0 or nb[1]<0,(d,nuisance,nb)
  games.append({'date':d,'opponent':team,'phase':'POST','branch':policy,'constant':constant,'actual_margin':r['actual_margin'],'coefficient':r['unknown_rating_coefficients'].get(RIVAL,0),'other_unknown_coefficients':nuisance,'other_unknown_margin_band':nb})
 assert len(games)==len({g['date'] for g in games})==72
 return games


def interval_summary(games,lower,upper):
 """Exact sign partitions for a single shared rating; zero is not a loss."""
 cuts=sorted({-g['constant']/g['coefficient'] for g in games if g['coefficient']})
 bounds=[lower,*[c for c in cuts if lower<c<upper],upper];intervals=[];totals=[]
 for lo,hi in zip(bounds,bounds[1:]):
  r=(lo+hi)/2;positive=[g['date'] for g in games if g['constant']+g['coefficient']*r>0]
  zeros=[g['date'] for g in games if abs(g['constant']+g['coefficient']*r)<1e-9]
  transfer={}
  if all('actual_margin' in g for g in games):
   actual_wins=sum(g['actual_margin']>0 for g in games);opponent_delta=defaultdict(int)
   assert not zeros, 'Zero-margin interval needs an unresolved result, not a win transfer'
   for g in games:opponent_delta[g['opponent']]+=int(g['actual_margin']>0)-int(g['date'] in positive)
   transfer={'chicago_win_delta_vs_actual':len(positive)-actual_wins,'opponent_win_deltas_from_chicago_games':{t:n for t,n in sorted(opponent_delta.items()) if n}}
   assert transfer['chicago_win_delta_vs_actual']+sum(opponent_delta.values())==0
  intervals.append({'rating_open_interval':[round(lo,8),round(hi,8)],'positive_margin_games':len(positive),'zero_margin_dates':zeros,**transfer});totals.append(len(positive))
 critical=[]
 for c in [lower,*[c for c in cuts if lower<=c<=upper],upper]:
  zero=[g['date'] for g in games if abs(g['constant']+g['coefficient']*c)<1e-7]
  if zero:critical.append({'rating':round(c,8),'unresolved_dates':zero})
 return {'rating_band':[lower,upper],'positive_margin_count_range':[min(totals),max(totals)],'rating_intervals':intervals,'zero_margin_boundaries':critical,'rival_break_even_ratings':{g['date']:round(-g['constant']/g['coefficient'],8) for g in games if g['coefficient']},'other_unknown_sign_checks':[{'date':g['date'],'coefficients':g['other_unknown_coefficients'],'margin_band':g['other_unknown_margin_band']} for g in games if g.get('other_unknown_coefficients')],'rival_margin_forms':{g['date']:{'constant':round(g['constant'],8),'coefficient':g['coefficient']} for g in games if g['coefficient']}}


def build(witnesses):
 branches=specs();inputs=paired_inputs(branches);cross=json.loads(cc.OUT.read_text());cd=json.loads(close.OUT.read_text());scenarios=[];paths=[]
 for profile,rival,boston in itertools.product(PROFILES,('RIVAL_24','RIVAL_28','RIVAL_32'),('FOURNIER_PATH_RETAINED',)):
  path_id=f'{profile}/{rival}/{boston}'
  path_games=season_games(inputs,cross,cd,profile,rival,boston,'PORTER_ZERO',METHODS[0],'BASE',0)
  paths.append({'path_id':path_id,'games':[{'date':g['date'],'phase':g['phase'],'opponent':g['opponent'],'branch':g['branch']} for g in path_games]})
  for availability,method,prior,fatigue in itertools.product(('PORTER_ZERO','PORTER_CAPPED'),METHODS,cc.SCENARIOS,cc.FATIGUE):
   games=season_games(inputs,cross,cd,profile,rival,boston,availability,method,prior,fatigue)
   env=cross['envelopes'][method];summary=interval_summary(games,env['low'],env['high'])
   scenarios.append({'path_id':path_id,'availability':availability,'method':method,'prior':prior,'fatigue':fatigue,**summary})
 disagreement=[]
 for profile,rival,boston in itertools.product(PROFILES,('RIVAL_24','RIVAL_28','RIVAL_32'),('FOURNIER_PATH_RETAINED',)):
  for availability,fatigue in itertools.product(('PORTER_ZERO','PORTER_CAPPED'),cc.FATIGUE):
   pair=[season_games(inputs,cross,cd,profile,rival,boston,availability,m,'BASE',fatigue) for m in METHODS]
   dates=[a['date'] for a,b in zip(*pair) if not a['coefficient'] and not b['coefficient'] and (a['constant']>0)!=(b['constant']>0)]
   disagreement.append({'path_id':f'{profile}/{rival}/{boston}','availability':availability,'fatigue':fatigue,'base_prior_method_disagreement_dates':dates})
 return {'stage':'O-15F12','status':'CONDITIONAL_72_GAME_PATHS_CONNECTED_NOT_CANON','base_main':'197637f762ca0b1571162b68eb7acd9928018209','remaining_pre_branches':branches,'lineup_witnesses':witnesses,'remaining_pre_paired_inputs':inputs,'season_paths':paths,'season_scenarios':scenarios,'method_disagreements':disagreement,'scope':{'prior_and_fatigue':'same method-specific prior and fatigue policy before/after deadline','rival':'same effective impact rating on both dates within each method, including role friction; not an approved ability prior','rival_band':'O-15F9 empirical league stress range; not player prior or a hard bound','overlap_cost':'no extra Towns/Russell synergy; actual causal cost still unmeasured','portland':'O-15F11 incumbents on both dates; Evans alternatives remain outside these paths','gsw':'Hutchison inactive on both dates, Wiggins core retained conditionally','orlando':'Gordon A/Harris/Nnaji, Vucevic stays, Hall contract/availability assumed; exact execution HOLD','boston':'Fournier Orlando-to-Boston retained across dates; NO_FOURNIER is excluded until Orlando retention/other destination is modeled','toronto':'Powell retained, Portland actual Powell trade absent','other_rosters_and_schedule':'historical incumbent transactions/availability and schedule retained conditionally','final_outcomes_selected':False,'standings_computed':False,'opponent_win_transfers':'only Chicago-involving games; other league games are not modeled'},'manuscript_allowed':False,'input_sha256':{p.name:cc.sha(p) for p in (cc.PRE,cc.QUEUE,cc.OUT,close.OUT,Path(__file__))}}


def verify(j):
 assert len(j['remaining_pre_branches'])==29 and len({b['date'] for b in j['remaining_pre_branches']})==15
 assert len(j['remaining_pre_paired_inputs'])==522
 assert len(j['season_paths'])==6 and len(j['season_scenarios'])==216
 obs=cc.read(cc.PRE);new={'WAS':{'Gary Trent Jr.'},'DAL':{'R.J. Hampton'},'CHA':{'Anthony Edwards','Tyrell Terry'},'NOP':{'Killian Hayes'},'DET':{'Patrick Williams','Kira Lewis Jr.'},'DEN':{'Saddiq Bey'},'MIN':{RIVAL},'LAL':set()}
 for b,w in zip(j['remaining_pre_branches'],j['lineup_witnesses'],strict=True):
  assert sum(b['delta_seconds'].values())==0 and sum(b['alternate_seconds'].values())==5*b['game_duration_seconds']
  seen=defaultdict(float);total=0;starting=0
  for x in w:
   assert x['seconds']>0 and valid(x['players'],b['opponent']);total+=x['seconds'];starting+=x['seconds'] if sorted(x['players'])==b['starters'] else 0
   for p in x['players']:seen[p]+=x['seconds']
  assert abs(total-b['game_duration_seconds'])<1e-5 and starting>=180-1e-5
  assert set(seen)==set(b['alternate_seconds']) and all(abs(seen[p]-n)<1e-5 for p,n in b['alternate_seconds'].items())
  for p,n in b['delta_seconds'].items():
   if n>0 and p not in new[b['opponent']]:
    r=next(r for r in obs if (r['date'],r['team'],r['player'])==(b['date'],b['opponent'],p))
    assert int(r['seconds'])>0 or r['comment']=="DNP - Coach's Decision"
  for p,n in b['alternate_seconds'].items():assert n<=max(b['actual_seconds'].get(p,0),2400 if b['game_duration_seconds']==2880 else 2700)
  if b['date'] in ('2021-02-24','2021-03-19'):assert b['game_duration_seconds']==3180
 for r in j['remaining_pre_paired_inputs']:
  assert abs(r['margin_constant']+r['opponent_margin_constant'])<1e-7
  assert r['rival_coefficient']==-r['opponent_rival_coefficient']
  if r['rival_coefficient']:assert r['numeric_outcome'] is None
 for p in j['season_paths']:
  assert len(p['games'])==len({g['date'] for g in p['games']})==72
  rival_branches={g['branch'] for g in p['games'] if g['opponent']=='MIN'};assert len(rival_branches)==1
  assert len({g['branch'] for g in p['games'] if g['opponent']=='BOS' and g['phase']=='POST'})==1
 for r in j['season_scenarios']:assert set(r['rival_margin_forms'])=={'2021-02-24','2021-04-11'}
 assert j==build(j['lineup_witnesses'])
 print('PASS O-15F12: 15 pre dates / 29 allocations / 522 paired inputs; 6 date-consistent conditional 72-game paths / 216 scenarios; shared rival and OT preserved; no canon outcomes')

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
 if args.write:
  j=build([solve(b) for b in specs()]);verify(j);OUT.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
 else:verify(json.loads(OUT.read_text()))
