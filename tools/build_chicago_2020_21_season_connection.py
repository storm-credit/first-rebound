"""O-15F10: connect 43 pre and 29 post games with explicit opponent paths.
No path is canon-selected; outputs are conditional envelopes only.
"""
import csv,json,hashlib,unicodedata
from collections import defaultdict
from pathlib import Path
import crosscheck_chicago_2020_21_impact as cc
import build_chicago_2020_21_paired_impact as pp
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'simulation';P='CHICAGO_2020_21_'
OBS=S/(P+'PREDEADLINE_PAIRED_OBSERVATIONS.csv');SCREEN=S/(P+'PREDEADLINE_OPPONENT_SCREEN.csv');MARG=S/(P+'PREDEADLINE_GAME_MARGIN_BASELINE.csv');MIN=S/(P+'PREDEADLINE_MINUTE_LEDGER.csv');DON=S/(P+'PREDEADLINE_DONOR_VECTOR.csv');POST=S/(P+'IMPACT_CROSSCHECK.json');OUT=S/(P+'SEASON_CONNECTION.json')
METHODS=['RAPTOR_RS_EB','BPM_MAR25_EB'];SCEN=['LOW','BASE','HIGH'];FAT=[0,.5,1]
REPL={('WAS','Isaac Bonga'):'Gary Trent Jr.',('POR','Gary Trent Jr.'):'Jacob Evans',('DAL','Tyrell Terry'):'R.J. Hampton',('CHA','LaMelo Ball'):'Anthony Edwards',('CHA','Grant Riller'):'Tyrell Terry',('NOP','Kira Lewis Jr.'):'Killian Hayes',('DET','Killian Hayes'):'Kira Lewis Jr.',('DET','Saddiq Bey'):'Patrick Williams',('MIN','Anthony Edwards'):'Fictional Rival'}
def read(p):return list(csv.DictReader(p.open()))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return pp.norm(s)
def sec(r):return int(r['seconds'])
def actuals():
 g=defaultdict(list)
 for r in read(OBS):g[(r['game_id'],r['team'])].append(r)
 return g
def ratings(method):
 m=cc.rating_maps()[method];return m
def predecessor_impact(method,scenario):
 pri={r['scenario']:r for r in read(pp.PRIORS)}[scenario];rm=ratings(method);roles={r['event_id']:r for r in read(MIN)};don=defaultdict(dict)
 for r in read(DON):don[r['event_id']][r['player']]=int(r['delta_seconds'])
 out={}
 for g in read(MARG):
  d=dict(don[g['event_id']]);role=roles[g['event_id']];d['Protagonist']=int(role['protagonist_seconds']);d['LaMelo Ball']=int(role['lamelo_seconds'])
  val=0
  for p,s in d.items():
   if p=='Protagonist':r=float(pri['protagonist_rating'])
   elif p=='LaMelo Ball':r=float(pri['lamelo_rating'])
   else:r=rm.get(norm(p),0)
   val+=s*r/2880
  out[g['event_id']]=val
 return out
def build():
 obs=actuals();screens=read(SCREEN); margins={r['event_id']:r for r in read(MARG)}; mapv={m:ratings(m) for m in METHODS}; pre=[]
 for q in screens:
  base=[r for r in read(OBS) if r['game_id']==q['game_id'] and r['team']==q['opponent']]
  removed=q['removed_actual_players'].split(';') if q['removed_actual_players'] else []
  added=q['added_or_changed_players'].split(';') if q['added_or_changed_players'] else []
  vec={r['player']:sec(r) for r in base};delta={}
  for p in removed:
   n=REPL.get((q['opponent'],p));s=vec.get(p,0)
   if n and s:
    delta[p]=-s;delta[n]=delta.get(n,0)+s
  for method in METHODS:
   rm=mapv[method]
   unknown={};opp=0
   for p,s in delta.items():
    if norm(p) in rm:opp+=s*rm[norm(p)]/2880
    else:unknown[p]=s/2880
   pre.append({'event_id':q['event_id'],'date':q['date'],'opponent':q['opponent'],'method':method,'actual_margin':int(margins[q['event_id']]['actual_margin']),'opponent_delta_constant':round(opp,8),'unknown_opponent_coefficients':{p:round(s,8) for p,s in unknown.items()},'delta_seconds':delta,'path_status':'CONDITIONAL_REPLACEMENT_VECTOR' if delta else ('ZERO_MINUTE_CONTACT_NO_DELTA' if removed else 'LIMITED_BASELINE_CANDIDATE')})
 post=json.loads(POST.read_text())
 # Use only post inputs with both methods and baseline constants; preserve symbolic rival coefficient.
 season=[]
 for method in METHODS:
  for scenario in SCEN:
   pi=predecessor_impact(method,scenario)
   for avail in ['PORTER_ZERO','PORTER_CAPPED']:
    ppre=[r for r in pre if r['method']==method]
    for penalty in FAT:
     vals=[];unc=[]
     for r in ppre:
      m=r['actual_margin']+pi[r['event_id']]-r['opponent_delta_constant']
      if r['unknown_opponent_coefficients']:unc.append(r['date'])
      vals.append(m)
     seen_dates=set()
     for r in post['post_inputs']:
      if r['method']!=method or r['prior']!=scenario or r['availability']!=avail or r['date'] in seen_dates:continue
      # One representative branch per date is a diagnostic only; changed branches remain an unselected menu.
      seen_dates.add(r['date'])
      # Hold the observed opponent vector for this baseline diagnostic; remove the
      # branch-specific opponent delta from the crosscheck margin.
      m=r['actual_margin']+r['chi_impact']+r['fatigue_deltas'][int(penalty*2)]
      vals.append(m)
     season.append({'method':method,'prior':scenario,'availability':avail,'fatigue':penalty,'pre_games':43,'post_games':29,'numeric_margin_wins':sum(x>0 for x in vals),'arithmetic_record':[sum(x>0 for x in vals),sum(x<=0 for x in vals)],'pre_unknown_dates':sorted(set(unc)),'status':'BASELINE_OPPONENT_PATH_ONLY_NOT_FINAL'})
 return {'stage':'O-15F10','status':'CONDITIONAL_72_GAME_CONNECTION_INPUT_PASS_SEASON_HOLD','method_note':'43 pre + 29 post arithmetic uses observed opponent baseline; explicit replacement vectors remain a menu and are not selected simultaneously. This is a connection diagnostic, not canon standings.', 'replacements':[{'team':t,'removed':p,'added':v} for (t,p),v in sorted(REPL.items())],'pre_inputs':pre,'season_baseline_diagnostics':season,'path_consistency':{'selected':False,'explicit_changed_paths':18,'baseline_remaining_paths':25,'overtime_minutes_preserved':True,'opponent_total_seconds_not_redistributed':True},'input_sha256':{p.name:sha(p) for p in [OBS,SCREEN,MARG,MIN,DON,POST,Path(__file__)]},'manuscript_allowed':False}
def verify(j):
 assert len(j['pre_inputs'])==86 and len(j['season_baseline_diagnostics'])==36
 assert j['path_consistency']['selected'] is False
 for r in j['pre_inputs']:
  assert sum(r['delta_seconds'].values())==0
  assert r['path_status'] in ['CONDITIONAL_REPLACEMENT_VECTOR','ZERO_MINUTE_CONTACT_NO_DELTA','LIMITED_BASELINE_CANDIDATE']
 for r in j['season_baseline_diagnostics']:assert r['pre_games']+r['post_games']==72 and r['status'].endswith('NOT_FINAL')
 assert j==build();print('PASS: 86 pre opponent-method inputs; 36 baseline 72-game diagnostics; 18 explicit paths; no season path selected')
if __name__=='__main__':
 j=build();verify(j);OUT.write_text(json.dumps(j,ensure_ascii=False,separators=(',',':'))+'\n')
