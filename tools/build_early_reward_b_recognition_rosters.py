"""Build four noncanon 2022 nomination pools from current selected club roles.

Ballots are declared ordinal fiction witnesses, not observed votes. They show
slot feasibility without promoting a personal award or copying injuries.
"""
import argparse
import csv
import hashlib
import io
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT='design/EARLY_REWARD_B_RECOGNITION_ROSTER_CANDIDATES_2026_10_12.json'
FULL='simulation/EARLY_REWARD_B_CURRENT_FULL_ROLE_INPUTS_2026_10_12.csv'
ATTACK='simulation/EARLY_REWARD_B_YEAR4_DATED_ATTACK_2026_10_11.csv'
LEDGER='simulation/CHICAGO_2021_22_SELECTED_RESULTS_LEDGER.json'
PRIOR='simulation/CHICAGO_2021_22_PRESEASON_PRIORS.json'
ROLE='simulation/CHICAGO_2021_22_ROLE_PLAN_INPUTS.json'
SOURCES=[FULL,ATTACK,LEDGER,PRIOR,ROLE,
 'design/EARLY_REWARD_B_RECOGNITION_COMPARISON_2026_10_12.json',
 'simulation/EARLY_REWARD_B_JOINT_RESULT_RESPONSE_2026_10_12.json',
 'canon/EARLY_REWARD_B_AUTHOR_SELECTION_2026_10_11.json']
TEAM_FILES={
 'ATL':'simulation/CHICAGO_ATLANTA_2021_22_SELECTED_KEEPER_RESULTS.json',
 'BKN':'simulation/CHICAGO_BROOKLYN_2021_22_SELECTED_KEEPER_RESULTS.json',
 'MIL':'simulation/CHICAGO_MILWAUKEE_2021_22_SELECTED_KEEPER_RESULTS.json',
 'PHI':'simulation/CHICAGO_PHILADELPHIA_2021_22_SELECTED_KEEPER_RESULTS.json',
 'BOS':'simulation/CHICAGO_BOSTON_2021_22_SELECTED_KEEPER_RESULTS.json',
 'MIA':'simulation/CHICAGO_MIAMI_2021_22_SELECTED_KEEPER_RESULTS.json',
 'CLE':'simulation/CHICAGO_CLEVELAND_2021_22_SELECTED_KEEPER_RESULTS.json',
 'TOR':'simulation/TORONTO_2021_SELECTED_T1_OPERATING_FAMILY_2026_10_07.json',
 'GSW':'simulation/CHICAGO_GOLDEN_STATE_2021_22_SELECTED_KEEPER_RESULTS.json',
 'MEM':'simulation/CHICAGO_MEMPHIS_2021_22_SELECTED_KEEPER_RESULTS.json',
 'LAL':'simulation/CHICAGO_LAKERS_2021_22_SELECTED_KEEPER_RESULTS.json',
 'DEN':'simulation/CHICAGO_DENVER_2021_22_SELECTED_KEEPER_RESULTS.json',
 'DAL':'simulation/CHICAGO_DALLAS_2021_22_SELECTED_KEEPER_RESULTS.json',
 'PHX':'simulation/CHICAGO_PHOENIX_2021_22_SELECTED_KEEPER_RESULTS.json',
 'UTA':'simulation/CHICAGO_UTAH_2021_SELECTED_KEEPER_RESULT.json',
 'MIN':'simulation/CHICAGO_MINNESOTA_2021_22_SELECTED_KEEPER_RESULTS.json',
 'SAS':'simulation/CHICAGO_SAN_ANTONIO_2021_22_SELECTED_KEEPER_RESULTS.json'}
EAST={'ATL','BKN','MIL','PHI','BOS','MIA','CLE','TOR','CHI'}
DEFS=[('TY','Trae Young','ATL','G'),('LV','Zach LaVine','CHI','G'),('JH','James Harden','BKN','G'),
 ('FV','Fred VanVleet','TOR','G'),('DG','Darius Garland','CLE','G'),('KI','Kyrie Irving','BKN','G'),
 ('LM','LaMelo Ball','CHI','G'),('KD','Kevin Durant','BKN','F'),('GA','Giannis Antetokounmpo','MIL','F'),
 ('JE','Joel Embiid','PHI','F'),('JT','Jayson Tatum','BOS','F'),('JB','Jimmy Butler','MIA','F'),
 ('KM','Khris Middleton','MIL','F'),('JA','Jarrett Allen','CLE','F'),('P','Protagonist','CHI','F'),
 ('SC','Stephen Curry','GSW','G'),('JM','Ja Morant','MEM','G'),('LJ','LeBron James','LAL','F'),
 ('NJ','Nikola Jokic','DEN','F'),('AW','Andrew Wiggins','GSW','F'),('LD','Luka Doncic','DAL','G'),
 ('DB','Devin Booker','PHX','G'),('RG','Rudy Gobert','UTA','F'),('KT','Karl-Anthony Towns','MIN','F'),
 ('CP','Chris Paul','PHX','G'),('DM','Donovan Mitchell','UTA','G'),('DD','DeMar DeRozan','SAS','F'),
 ('GR','Draymond Green','GSW','F'),('DJ','Dejounte Murray','SAS','G'),('RV','Fictional Rival','MIN','G')]

def norm(path):
 return (ROOT/path).read_bytes().removeprefix(b'\xef\xbb\xbf').replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def read(path): return json.loads(norm(path))
def csvrows(path): return list(csv.DictReader(io.StringIO(norm(path).decode())))
def team_pointer(team,name):
 path=TEAM_FILES[team];data=read(path)
 if team=='TOR':
  i=data['selected_roster']['standard'].index(name)
  return path+'#/selected_roster/standard/'+str(i)
 for i,row in enumerate(data['lawful_contract_family']):
  if row.get('player')==name: return path+'#/lawful_contract_family/'+str(i)
 raise AssertionError((team,name,'not in current contract family'))
def pool(starter_g,any_players):
 return {'starter_G':starter_g,'starter_F':['KD','GA','JE'],
 'reserve_G':['DG','FV'] if 'FV' not in starter_g else ['DG','LV'],
 'reserve_F':['JT','JB','KM'],'reserve_ANY':any_players}
def check_pool(pool,index,conference):
 expected={'starter_G':2,'starter_F':3,'reserve_G':2,'reserve_F':3,'reserve_ANY':2}
 flat=[]
 for slot,size in expected.items():
  assert len(pool[slot])==size,(slot,size)
  for who in pool[slot]:
   assert index[who]['conference']==conference,(who,conference)
   if slot.endswith('_G'): assert index[who]['candidate_ballot_group']=='G',(who,slot)
   if slot.endswith('_F'): assert index[who]['candidate_ballot_group']=='F',(who,slot)
   flat.append(who)
 assert len(flat)==12 and len(set(flat))==12,'duplicate or25th member'
 return {'initial_pool':12,'starters':5,'reserves':7,'unique':12,'position_slots_valid':True}

def build():
 pins={p:hashlib.sha256(norm(p)).hexdigest() for p in SOURCES+list(TEAM_FILES.values())}
 index={}
 for key,name,team,group in DEFS:
  if team=='CHI':
   alias={'LV':'LaVine','LM':'LaMelo_pick4','P':'Protagonist'}[key]
   candidates=['PG','SG'] if group=='G' else ['SF','PF','C']
   positions=[pos for pos in candidates if alias in read(ROLE)['position_eligibility_design_only'][pos]]
   assert positions
   authority=ROLE+'#/position_eligibility_design_only/'+positions[0]
  else: authority=team_pointer(team,name)
  index[key]={'player':name,'selected_club':team,'conference':'EAST' if team in EAST else 'WEST',
   'candidate_ballot_group':group,'current_club_authority':authority,
   'ballot_group_classification':'DECLARED_CANDIDATE_USING_CURRENT_ROLE_NOT_LEAGUE_CONFIRMED_BALLOT'}
 assert read(TEAM_FILES['SAS'])['selected_role_minutes']['SF']['DeMar DeRozan']==28
 assert read(TEAM_FILES['SAS'])['selected_role_minutes']['PF']['DeMar DeRozan']==6
 # A witness of possible relative ranks, with all unlisted guards below7.
 # This is not a complete league ballot or actual vote-count reconstruction.
 orders={'A':(['TY','LV','JH','FV','DG','LM','KI'],['LV','TY','JH','FV','DG','KI','LM'],['TY','LV','JH','FV','DG','LM','KI']),
 'B':(['TY','JH','LV','FV','DG','LM','KI'],['JH','LV','TY','FV','DG','KI','LM'],['TY','JH','LV','FV','DG','LM','KI']),
 'C':(['TY','FV','LV','JH','DG','LM','KI'],['LV','FV','TY','JH','DG','KI','LM'],['FV','TY','JH','LV','DG','LM','KI']),
 'D':(['TY','LV','JH','FV','DG','LM','KI'],['LV','TY','JH','FV','DG','KI','LM'],['TY','LV','JH','FV','DG','LM','KI'])}
 east={'A':pool(['TY','LV'],['JH','P']),'B':pool(['TY','JH'],['LV','P']),
       'C':pool(['TY','FV'],['JH','P']),'D':pool(['TY','LV'],['JH','JA'])}
 west={'starter_G':['SC','JM'],'starter_F':['LJ','NJ','AW'],
       'reserve_G':['LD','DB'],'reserve_F':['RG','KT','DD'],'reserve_ANY':['CP','DM']}
 routes=[]
 for key in 'ABCD':
  ballot=[]
  for who in orders[key][0]:
   fan,players,media=[order.index(who)+1 for order in orders[key]]
   ballot.append({'player_id':who,'fan_rank':fan,'player_rank':players,'media_rank':media,
    'weighted_score':str(F(2*fan+players+media,4)),'classification':'FICTIONAL_ORDINAL_WITNESS_NOT_OBSERVED_VOTES'})
  leaders=sorted(ballot,key=lambda r:(F(r['weighted_score']),r['fan_rank']))[:2]
  assert {r['player_id'] for r in leaders}==set(east[key]['starter_G'])
  checks={'EAST':check_pool(east[key],index,'EAST'),'WEST':check_pool(west,index,'WEST')}
  assert len(set(sum(east[key].values(),[])+sum(west.values(),[])))==24
  routes.append({'id':key,'status':'CANDIDATE_NOT_SELECTED','recommended':key=='A',
   'initial_nomination_pools':{'EAST':east[key],'WEST':west},'East_guard_ordinal_ballot':ballot,
   'unlisted_guard_rank_assumption':'All other eligible East guards rank>=8 in each group; assumed, not observed. No exact counts or full ballot certified.',
   'structural_check':checks,'P_first_AllStar_if_selected':2022 if key!='D' else None,
   'coactor_cost':{'LV':'starter' if key in 'AD' else 'reserve','LM':'initial shortlist outside12; no fake injury replacement',
   'DD':'SAS WEST frontcourt reserve; cannot import historicalCHI2022scoring',
   'GR':'initial outside12 on this shared candidate branch; not assigned injury',
   'DJ':'initial outside12; historicalMurrayinjuryreplacement not copied',
   'RV':'MIN SG shortlist outside12; current32minute role retained; no invented breakup/medical event'},
   'declared_voter_reason_family':{
    'A':'Fans prefer existingCHIleadscorer visibility plus team rebound; players value own shotcreation; media favors sustained34minute leadscoring. P reserve coaches prefer wing rebounding/secondary finishing; no proof of superior defense.',
    'B':'Fans andmedia prefer BKNprimary ballcreation/starrecognition, players elevate Harden; LV stays reserve. P nomination still needs separate opposing-coach judgment.',
    'C':'Fans emphasize Toronto primaryguard leadership, media rewards own creation/control; player order keepsLVstrong whileVVwins weightedsecond. This requires larger fictitious visibility change thanA.',
    'D':'Same guard ballots asA; coaches give wildcard to an independent center/rebounding role instead ofP. Growth evidence earns shortlist only; no consolation injury invented.'}[key],
   'reason_status':'AUTHOR_FICTION_CANDIDATE_NOT_REAL_VOTER_STATEMENT_OR_MEASURED_CAUSAL_EFFECT'})
 scopes=[]
 for label,cut in [('VOTING_CLOSE','2022-01-22'),('STARTER_ANNOUNCEMENT','2022-01-27'),('RESERVE_ANNOUNCEMENT','2022-02-03')]:
  games=[r for r in read(LEDGER)['rows'] if r['date']<cut]
  own=[r for r in csvrows(FULL) if r['NBA_year']=='4' and r['date']<cut]
  actors=[]
  for actor in ['LaVine','LaMelo_pick4','Protagonist']:
   rows=[r for r in csvrows(ATTACK) if r['actor']==actor and r['date']<cut]
   actors.append({'actor':actor,'games':len(rows),'expected_PPG':float(sum((F(r['expected_pts']) for r in rows),F(0))/len(rows)),
    'source':'CURRENT_B_WORKING_DATED_ATTACK_NOT_ACTUAL_BOX','expected_mean_minutes':float(sum((F(r['regulation_minutes']) for r in rows),F(0))/len(rows))})
  scopes.append({'id':label,'cutoff_exclusive':cut,'same_day_games_excluded':True,'CHI_games':len(games),
   'CHI_W':sum(r['working_regulation_result']['winner']=='CHI' for r in games),
   'CHI_L':sum(r['working_regulation_result']['winner']!='CHI' for r in games),
   'P_expected_PTS_REB_AST':[float(sum((F(r[k]) for r in own),F(0))/len(own)) for k in ['expected_pts','expected_reb','expected_ast']],
   'coactor_context':actors,'later_context_cannot_be_used_for_prior_ballot':True,
   'cutoff_limit':'Announcement upper bound, not independently established coach ballot deadline' if label=='RESERVE_ANNOUNCEMENT' else 'Conservative date cutoff; same-day time not inferred'})
 assert [(s['CHI_games'],s['CHI_W'],s['CHI_L']) for s in scopes]==[(44,27,17),(47,30,17),(50,33,17)]
 return {'id':'EARLY_REWARD_B_RECOGNITION_ROSTER_CANDIDATES_2026_10_12',
  'baseline_main':'58d6c8aa0bcc9b2cbda1525eeeca0a371f8e18b2',
  'status':'FOUR_FULL_NOMINATION_POOL_CANDIDATES_POSITION_DATE_PROVENANCE_CHECKED_NOT_SELECTED',
  'source_sha256':pins,'player_index':index,'date_context':scopes,'candidate_routes':routes,
  'sources_web_read':[
   {'url':'https://pr.nba.com/nba-all-star-voting-tissot-2022/','fact':'Jan22midnightET close,Jan27starters,Feb3reserves. Conservative local cutoffs exclude same-day games.'},
   {'url':'https://pr.nba.com/voting-results-2022-nba-all-star-game-starters/','fact':'2G3F weighted ordinal selection; original ranks do not prove altered ballots.'},
   {'url':'https://www.nba.com/raptors/news/vanvleet-selected-to-2022-nba-all-star-game','fact':'2022coach seven=2G+3F+2ANY; own players excluded.'},
   {'url':'https://pr.nba.com/2022-nba-all-star-game-draft-rosters/','fact':'Historical pool/team draft and replacements distinguished; no actual2022HardenPHItrade copied to selectedBKN.'}],
  'historical_2022_replacements_not_imported':['Durant→LaMelo(CHA)','Green→Dejounte','Harden(PHI)→Allen'],
  'guardrail':'Initial conference nomination pools only; captain draft, game minutes, injury replacements and AllStarMVP not selected.',
  'recommended_candidate':'A','recommendation_limit':'Structurally feasible shortlist under declared fictitious ballots; P20/8.71/3.2 andCHI33–17 do not prove coach votes or superiority over peers.',
  'year1_to_year3':'Keep own attack/AllRookie/MIP/2021AllStar competition. No automatic exactaward; P thirdyear cutoff16.45/7.64/2.49 and14–16 remains.',
  'contract_incentive_scope':'P fixed2022E2=98.56m preserved. No AllNBA/MVP qualifying trigger or new guaranteed incentive is manufactured from AllStar nomination.',
  'remaining':['Exact personal recognition selections under author choice; declared voter reasons do not replace proof of real ballots.',
   'C01 exactmedal/militarybranch; currenthistory/finalallocation/individualBlueprint/Pack; independent/finalgate.'],
  'gates':{'new_personal_awards_selected':0,'C01_selected':0,'freeze':'v0.30 PARTIAL','design':'CLOSED','manuscript':0,'actual_Pack':0},
  'unfinished_major_groups':4,'unfinished_through_group6':3}

def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
 report=build();raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
 if args.check: assert norm(OUT)==raw,'candidate replay mismatch'
 else:
  with (ROOT/OUT).open('xb') as f:f.write(raw)
 print(json.dumps({'status':'PASS_REPLAY' if args.check else 'BUILT_CANDIDATES','candidates':4,'club_role_players':len(report['player_index']),'source_pins':len(report['source_sha256']),'context_games':[s['CHI_games'] for s in report['date_context']]},ensure_ascii=False))
if __name__=='__main__':main()
