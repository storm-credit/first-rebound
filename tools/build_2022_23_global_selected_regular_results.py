"""Finite FY23 constructor; no ancestor builds, historical winners, or private receipts.

Physical input pins are reviewed snapshots. New season role/availability/0OT and
zero-growth productivity are explicit model selections, not factual NBA stats.
The first-round admission sensitivity remains separate from computing outcomes.
"""
from pathlib import Path
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import date, timedelta, datetime
from fractions import Fraction
from unittest.mock import patch
import argparse, csv, hashlib, io, json, re
import fitz
import build_nba_2022_23_published_calendar as published

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_23_global_selected_regular_results.py'
OUT='simulation/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS.json'
MD=OUT[:-5]+'.md'
BASELINE='d6bd960'
PORT='simulation/NBA_2022_23_NPC_CONTRACT_PORTFOLIO.json'
OLD='simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json'
LEAGUE='simulation/NBA_2022_23_PUBLISHED_CALENDAR.csv'
CHI='simulation/CHICAGO_2022_23_PUBLISHED_CALENDAR.csv'
PROV='simulation/NBA_2022_23_PUBLISHED_CALENDAR_PROVENANCE.json'
H22='simulation/CHICAGO_2022_23_SELECTED_DATED_ROLES.json'
AUTH='canon/DELEGATED_CHICAGO_2022_23_HEALTH_ROLES_2026_10_08.json'
DISPATCH='simulation/CHICAGO_2022_23_PAIRED_DATE_DISPATCH.json'
CALTOOL='tools/build_nba_2022_23_published_calendar.py'
BOARD='research/NBA_2022_FULL_DRAFT_WORKING_BOARD_2026_10_08.json'
RSC='simulation/NBA_2022_NPC_FIRST_ROUND_RSC_SLOT_JOIN.json'
RSCPEER='reviews/NBA_2022_NPC_FIRST_ROUND_RSC_SLOT_JOIN_G11_INDEPENDENT_REVIEW_2026_10_08.json'
OVERLAY='simulation/NBA_2022_23_EXPLICIT_NPC_AVAILABILITY_OVERLAY.json'
MILES_PLAN_MEANING='031252f7477b68a67289ada303c6453787e7b9bd10cb06c6779cb2c96041aab9'
# Source owner is producing this leaf. It is not inferred from the old rights-only ports.
ADMISSION_SOURCE_FROZEN=True
ROOKIE_PLAN_MEANING={'ATL': '617edb4a882a116cfb3fb2bb988b49abaaaa92879d41df9f7c2a966eb37b8f5c', 'BOS': '85bd32064b7bebdb12d2a4e53ccc708dab2c5a01614e932acbc914c584ed1164', 'CHA': '453fe7f79ca4ad287d88f3755984c84a14e8d889b3286dcefe4b54782d1b53fe', 'CLE': 'c6f02e078100f1c0e9f29512891b01dcface6ab440f77c19d0c453a5f89992fa', 'DAL': '81e73e63f0ce36526a54339c6870c3acf991e62b493b67aa79a354930d9144b6', 'DEN': 'ef452b651ab55d3884e07c9353bc5edd8669ad1a31578cda7c256a604a25ca0b', 'DET': '8bb2ad1a301226b406defee92588de5e0231bbb4dab3905c037cbd64a6e51224', 'GSW': '60f259f0646e7e46815ce8cb57b325562b5b47897d029fbd73cbb84ba23d49dc', 'HOU': '7e25f1b8a02f8466ee53765a4a72d18e0b943c7825f63bedaa102218730a241d', 'IND': '93fd456f56b1315804f40552907564f7aaaacf1d2af7f5e77af3e5a88075c67e', 'MEM': 'cf8ab1784596e3a00c1e455433ca723a4c7b0a03e737a5863d29f131878b4932', 'MIA': 'fc8d9aafa6d06aa8b52da4d33130b3ee5e3016bdf8f6bc89aee17501a997dfb9', 'MIL': 'f13d34e4b52bc8010642a11d64409f329db7339a8f6e130d72f2faea445c803c', 'MIN': '4f502a12e37cd353409b39a2b7cd16cfdc7a094ff42370a4f7684b3651661d17', 'NOP': '7dcb5b9ae44c196a124cd20140b91cbfdcab39a5ea146a1d612d146ccd957b00', 'NYK': '2b58f014784a562ca69cfe322be98e338a96671030098a4be2bd90c066193f08', 'OKC': '1983f5f5c595640966e3fe66615d148a9a9ff2e61963a6cda496ee1a3892a9ff', 'ORL': 'ab60771b40051cd8ff4ece264ab85b7d16fd6f03ecb8b0d59ec18706a098e8f6', 'PHI': 'fc45419253f37314a66a1c845213635ea9575cfae0af206fa57b946db857024d', 'POR': 'd921811f8fe2ba6123363622316c49845d60da752d638b1881ab108a554db68a', 'SAC': '5ed56f5e71326f09c917d4f0899b730a3bf50698a328b3c7b2b0780503d2b8fd', 'SAS': 'e02a3a29af24719cb335df40bda56052b0368973e3c6c10fa923810dc526b4f2', 'TOR': 'cdbb470a9991b088a02e3492344e6c84e8a23813c5683575e0805965579e96cd', 'WAS': '3b363b205191e41a5dbea4b6d98002513f9baa71093280acb5f25784f9e510de'}
# Public broad C/G/F class bounds an explicitly chosen basketball role. Wing F
# does not automatically becomePF just because more bench minutes exist there.
ROOKIE_POSITIONS={1:'C',2:'PF',3:'PF',4:'SG',5:'PF',6:'SF',7:'SG',8:'PG',9:'PF',10:'C',
 11:'SF',12:'SF',13:'C',14:'SF',15:'SF',16:'PF',17:'SG',19:'SG',20:'SG',21:'PF',
 22:'SF',23:'PF',24:'SG',25:'SF',26:'PG',27:'C',28:'PG',29:'PF',30:'SF'}
# Portfolio pin is filled only after its owner explicitly freezes the producer.
PINS={'simulation/NBA_2022_23_NPC_CONTRACT_PORTFOLIO.json': '123d07df572ac4350e9528b3f0b913b3013ad4d51584c88a94e78051b9c7af19', 'simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json': '93264d2dff86a58ad10ca6975315c6c2167961f94f2517b6f5f79fa3113f2af8', 'simulation/NBA_2022_23_PUBLISHED_CALENDAR.csv': '2ae22464127e12926b1da3a69346590d8c4a9269dd2e06ae6675339692fb19d2', 'simulation/CHICAGO_2022_23_PUBLISHED_CALENDAR.csv': 'bd78708fb1d58e4decede3723bd14829863d395366d30d202565e3c7f7729f4b', 'simulation/NBA_2022_23_PUBLISHED_CALENDAR_PROVENANCE.json': 'b0ed4235d17653b1272636f8197cb9eca3daacc1e279a157376f9ae227496e78', 'simulation/CHICAGO_2022_23_SELECTED_DATED_ROLES.json': 'c0650dbb07b75cc1523bf7ccc7f658576ac5b9a8784f1e80cc97178897703170', 'canon/DELEGATED_CHICAGO_2022_23_HEALTH_ROLES_2026_10_08.json': 'bf7bfdc1d64072196c1ec293c18c3410d722f67dd1a9014ef3d789999762bddf', 'tools/build_nba_2022_23_published_calendar.py': '2c9152e013f3371da56d671f4f6a18f052ba240359a244ae2d083a8b561156f0', 'research/NBA_2022_FULL_DRAFT_WORKING_BOARD_2026_10_08.json': '3bdad52ebaacda5abb23b9908b8ed3a9b85cfaa09d838819a959cd024a58e940', 'simulation/NBA_2022_NPC_FIRST_ROUND_RSC_SLOT_JOIN.json': '9e72b7b6f277d62a1462eae93548903278631a155698ec39fcfef82fae200933', 'reviews/NBA_2022_NPC_FIRST_ROUND_RSC_SLOT_JOIN_G11_INDEPENDENT_REVIEW_2026_10_08.json': '319d07c5505222057f0407be7433df0958672ea0a80b444e58d66b1df0dd3f7f', 'simulation/NBA_2022_23_EXPLICIT_NPC_AVAILABILITY_OVERLAY.json': '3bcb132b62595cef8490933d462b2c841ab3737777877cb4e687c8c60412a80b'}
POSITIONS={'PG','SG','SF','PF','C'}
ALIASES={'Carter':'Wendell Carter Jr.','LaVine':'Zach LaVine','LaMelo_pick4':'LaMelo Ball',
 'Coby':'Coby White','Young':'Thaddeus Young','Satoransky':'Tomas Satoransky',
 'Green':'Javonte Green','Caruso':'Alex Caruso','Markkanen':'Lauri Markkanen'}
SPECIAL={'BKN':'IRVING_AWAY_RETURN','GSW':'KLAY_WORKING_RETURN','ORL':'RECOVERY','NOP':'ZION_WORKING_RETURN'}
VENUES={439:('2022-12-17','SAS','MIA','A','Mexico City Arena, Mexico City',0),
 635:('2023-01-13','SAS','GSW','B','Alamodome, San Antonio',2),
 678:('2023-01-19','DET','CHI','C','Accor Arena, Paris',0),
 1199:('2023-04-06','SAS','POR','D','Moody Center, Austin',2),
 1214:('2023-04-08','SAS','MIN','D','Moody Center, Austin',2)}
POLICY={'model':'BPM_MARCH25_EB_FRACTION_HOME2_B2B_HALF',
 'new_FY23_zero_growth_zero_aging_proxy_selected':True,
 'prior_coefficient_is_not_FY23_observed_BPM':True,
 'new_NPC_regular_0OT_policy_selected':True,'CHI_STAT23_A_0OT_policy_separate':True,
 'ordinary_NPC_no_new_injury_or_coach_rest_episode_selected':True,
 'explicit_Chet_season_OUT_and_Miles_no_new_UPC_exceptions_applied':True,
 'GSW_Klay_return_ORL_recovery_NOP_Zion_return_all_FY23_dates_selected':True,
 'BKN_all_date_full_participant_club_nomination_selected':True,
 'old_NYC_and_Canada_vaccination_OUT_labels_not_inherited':True,
 'lawful_host_access_and_other_immigration_requirements_admitted_not_actual_receipts':True,
 'international_Mexico_Paris_home_effect':0,'SAS_Alamodome_Austin_home_effect':2,
 'regulation_seconds':2880,'exact_scores_selected':False,'new_midseason_transactions_selected':False,
 'rookie_admission_and_productivity_sensitivity_explicit':True,
 'all_58_rookies_UPC_required':False,'all_rookies_forever_non_NBA_selected':False,
 'actual_private_medical_or_registration_certified':False,'new_MVP_or_title_selected':False}
FIXED_POLICY=deepcopy(POLICY)
CANADA_CAPTURE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-2022-23-global-20261008/canada-observed.json')
CANADA_CAPTURE_SHA='fa9edb2fd7a732c652dbfd4a53726872767a11eeb708df6ade633299538bfd2a'
CHET_CAPTURE=CANADA_CAPTURE.parent/'chet-observed.json'
CHET_CAPTURE_SHA='23a44a286349b58f7f8d1e9bb45922fd42acab174e49f130b4a9d72ba4ce8fd7'

def need(ok,why):
 if not ok:raise AssertionError(why)
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def dump(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def load(root,p):
 s=text(root/p)
 return json.loads(s) if p.endswith('.json') else list(csv.DictReader(io.StringIO(s)))
def inputs(root=ROOT):
 required={PORT,OLD,LEAGUE,CHI,PROV,H22,AUTH,CALTOOL}
 if ADMISSION_SOURCE_FROZEN:required|={BOARD,RSC,RSCPEER,OVERLAY}
 need(set(PINS)==required,'Source freeze not yet completed')
 need(POLICY==FIXED_POLICY,'Selected new-year policy altered')
 out={}
 for p,checksum in PINS.items():
  need(sha(root/p)==checksum,'Physical source stale: '+p)
  if p.endswith('.py'):continue
  returned=load(root,p)
  raw=text(root/p)
  disk=json.loads(raw) if p.endswith('.json') else list(csv.DictReader(io.StringIO(raw)))
  need(returned==disk,'Returned physical source differs: '+p)
  out[p]=returned
 return out

def primary_context():
 need(hashlib.sha256(CANADA_CAPTURE.read_bytes()).hexdigest()==CANADA_CAPTURE_SHA,'Canada observed capture changed')
 c=json.loads(text(CANADA_CAPTURE))
 need(c['source_type']=='OFFICIAL_WEB_BODY_OBSERVED_CAPTURE_NOT_HTTP_RAW' and c['raw_sha256'] is None and
      c['direct_HTTP_download']=='TIMEOUT_NO_BYTES_PRESERVED' and c['observed_facts']['effective_date']=='2022-10-01',
      'Observed body or failed download promoted to raw evidence')
 need(hashlib.sha256(CHET_CAPTURE.read_bytes()).hexdigest()==CHET_CAPTURE_SHA,'Chet observation capture changed')
 h=json.loads(text(CHET_CAPTURE));raw=Path(h['direct_cache'])
 need(hashlib.sha256(raw.read_bytes()).hexdigest()==h['direct_bytes_sha256'] and h['HTTP_status']==200,'Chet direct raw changed')
 body=raw.read_text(encoding='utf-8')
 j=json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',body,re.S)[1])
 article=j['props']['pageProps']['article'];plain=article.get('contentText',article.get('contentFiltered',''))
 need(all(w in plain for w in ('Chet Holmgren','Lisfranc','pro-am')),'Chet raw article lacks named historical facts')
 return {'Canada':{'capture_path':str(CANADA_CAPTURE),'capture_bytes_sha256':CANADA_CAPTURE_SHA,
                   'capture_is_not_original_HTTP_bytes':True,**c},
         'Chet':{'capture_path':str(CHET_CAPTURE),'capture_bytes_sha256':CHET_CAPTURE_SHA,**h,
                 'historical_season_OUT_anchor_selected_by_root':True,
                 'healthy_24minute_role_is_unselected_sensitivity':True,
                 'same_OKC_draft_does_not_itself_erase_historical_injury':True,
                 'actual_proam_nonparticipation_or_medical_clearance_certified':False},
         'new_NPC_lawful_host_access':'Explicit admitted fictional condition; no athlete vaccination or border receipt certified.'}

def calendar_source(s):
 p=s[PROV]['primary_support']['league_bydate']
 raw=Path(p['cache_path']);need(hashlib.sha256(raw.read_bytes()).hexdigest()==p['raw_sha256'],'Calendar raw changed')
 rows=[]
 with fitz.open(raw) as doc:
  need(len(doc)==23,'Calendar page count')
  for page,pg in enumerate(doc,1):
   t=pg.get_text().replace('\r\n','\n').replace('\r','\n')
   need(hashlib.sha256(t.encode()).hexdigest()==p['page_text_LF_sha256'][str(page)],'Calendar text changed')
   ms=list(re.finditer(published.DAY_PATTERN,t))
   for i,m in enumerate(ms):
    n=int(m[1]);dt=datetime.strptime(m[3],'%m/%d/%y').date().isoformat()
    end=ms[i+1].start() if i+1<len(ms) else len(t)
    marks=[x.strip() for x in t[m.end():end].splitlines() if x.strip() in published.ARENAS]
    need(len(marks)<=1,'Arena ambiguous');mark=marks[0] if marks else ''
    rows.append({'published_game_number':str(n),'calendar_key':f'PUBLISHED_2022_{n:04}',
      'published_date':dt,'home':published.NAMES[m[5]],'away':published.NAMES[m[4]],
      'published_home_local_time':m[6],'published_ET':m[7],'bydate_PDF_page':str(page),
      'original_arena_marker':mark,'original_venue_note':published.ARENAS.get(mark,''),
      'actual_NBA_game_id':'','actual_played_date':'','alternate_date_selected':'','alternate_result_selected':''})
 need(rows==s[LEAGUE],'Calendar CSV differs from raw official PDF')
 need(len(rows)==1230 and [int(x['published_game_number']) for x in rows]==list(range(1,1231)),'Calendar1230')
 counts=Counter(t for g in rows for t in (g['home'],g['away']))
 need(len(counts)==30 and set(counts.values())=={82},'30x82 failed')
 chi=[g for g in rows if 'CHI' in (g['home'],g['away'])]
 need(len(chi)==82,'CHI82')
 for i,(g,c,h) in enumerate(zip(chi,s[CHI],s[H22]['dated_rows']),1):
  for k in ('calendar_key','published_date','home','away','original_venue_note'):need(g[k]==c[k]==h[k],'CHI calendar/H22 field altered '+k)
  need(int(c['team_game_number'])==h['team_game_number']==i and h['working_date_adopted'] and h['H22_state_selected_for_date'],'H22 date adoption altered')
 marked=[g for g in rows if g['original_arena_marker']]
 need({int(g['published_game_number']) for g in marked}==set(VENUES),'Venue coverage altered')
 for g in marked:
  n=int(g['published_game_number']);expected=VENUES[n]
  need(tuple(g[k] for k in ('published_date','home','away','original_arena_marker','original_venue_note'))==expected[:5],'Named venue source mismatch')
 return rows

def canonical_name(p):return ALIASES.get(p,p)
def selected_rates(s):
 out={}
 for name,v in s[OLD]['selected_productivity_inputs'].items():
  k=canonical_name(name);r=str(Fraction(v['fraction']))
  need(k not in out or out[k]['fraction']==r,'Alias coefficient collision')
  out[k]={'fraction':r,'prior_source':v['source'],'new_FY23_classification':'SELECTED_CONSERVATIVE_ZERO_GROWTH_PROXY_NOT_OBSERVED_FY23'}
 h=s[H22]['selected_role_template']['Kessler_new_NBA_productivity']
 need(h['chosen_point']==-1,'Kessler chosen point changed')
 out['Walker Kessler']={'fraction':'-1','prior_source':H22+'#/selected_role_template/Kessler_new_NBA_productivity','new_FY23_classification':'SELECTED_NEW_ROOKIE_PROXY_NOT_NBA_STATS'}
 return out

def assert_blocks(blocks,standard,active):
 clock=0;seconds=Counter();roles=defaultdict(Counter)
 need(len(set(standard))==len(standard) and 14<=len(standard)<=15,'STD minimum/maximum')
 need(len(active)==len(set(active)) and 12<=len(active)<=15 and set(active)<=set(standard),'Active nomination invalid')
 for b in blocks:
  a,z=b['start_second'],b['end_second'];ps=b['positions']
  need(type(a)==type(z)==int and a==clock and z>a and set(ps)==POSITIONS and len(set(ps.values()))==5,'Role clock/5 positions')
  need(set(ps.values())<=set(active),'Positive actor inactive/non-owner')
  clock=z
  for pos,p in ps.items():seconds[p]+=z-a;roles[pos][p]+=z-a
 need(clock==2880 and sum(seconds.values())==14400 and all(sum(v.values())==2880 for v in roles.values()),'48/240 role budgets')
 return dict(sorted(seconds.items()))

def team_template(team,s):
 if team=='CHI':
  h=s[H22]['selected_role_template']
  return {'team':team,'id':'CHI:H22_NORMAL_KESSLER12_REG48','blocks':[{k:deepcopy(b[k]) for k in ('start_second','end_second','positions')} for b in h['ordered_regulation_blocks']],
   'standard':deepcopy(h['registered_STANDARD']),'TW':deepcopy(h['registered_TWO_WAY']),
   'active':deepcopy(h['active_STANDARD']),'inactive':deepcopy(h['inactive_STANDARD']),
   'source_pointer':H22+'#/selected_role_template','new_FY23_availability_selected':True}
 f=s[PORT]['team_functions'][team];sid=team+':'+SPECIAL.get(team,'NORMAL')
 t=next(x for x in f['capacity_templates'] if x['id']==sid)
 return {'team':team,'id':sid,'blocks':deepcopy(t['blocks']),'standard':deepcopy(f['standard']),
  'TW':deepcopy(f['TW']),'active':deepcopy(t['active']),'inactive':deepcopy(t['inactive']),
  'source_pointer':PORT+'#/team_functions/'+team+'/capacity_templates',
  'source_state_name_is_not_FY23_medical_fact':True,'new_FY23_availability_selected':True}

def assert_template(t,team,s):
 f=s[PORT]['team_functions'][team]
 need(t['team']==team and t['standard']==f['standard'] and t['TW']==f['TW'],'Returned roster/class altered')
 if team=='CHI':
  h=s[H22]['selected_role_template'];blocks=[{k:deepcopy(b[k]) for k in ('start_second','end_second','positions')} for b in h['ordered_regulation_blocks']]
  active=h['active_STANDARD'];inactive=h['inactive_STANDARD']
  need(t['id']=='CHI:H22_NORMAL_KESSLER12_REG48' and t['source_pointer']==H22+'#/selected_role_template','Returned CHI role identity/source pointer changed')
 else:
  sid=team+':'+SPECIAL.get(team,'NORMAL');raw=next(x for x in f['capacity_templates'] if x['id']==sid)
  prior=s[OLD]['shared_role_templates'][sid]
  need(raw['blocks']==prior['blocks'] and raw['positive_player_seconds']==prior['positive_player_seconds'],'Portfolio prior chronology changed')
  blocks=raw['blocks'];active=raw['active'];inactive=raw['inactive']
  need(t['id']==sid and t['source_pointer']==PORT+'#/team_functions/'+team+'/capacity_templates' and t['source_state_name_is_not_FY23_medical_fact'] is True,'Returned NPC role identity or scope changed')
 need(t['blocks']==blocks and t['active']==active and t['inactive']==inactive,'Returned selected source role/nomination altered')
 need(t['new_FY23_availability_selected'] is True,'New-year policy selection missing')
 sec=assert_blocks(t['blocks'],t['standard'],t['active'])
 need(set(t['inactive'])==set(t['standard'])-set(t['active']),'Inactive partition')
 need(len(t['TW'])<=2 and not(set(t['TW'])&set(t['standard'])),'TW class invalid')
 return sec

def paired(home,away):
 points=sorted({0,720,1440,2160,2880}|{b[k] for t in (home,away) for b in t['blocks'] for k in ('start_second','end_second')})
 out=[]
 for a,z in zip(points,points[1:]):
  out.append({'start_second':a,'end_second':z,'seconds':z-a,'quarter':a//720+1,
   home['team']:deepcopy(next(b['positions'] for b in home['blocks'] if b['start_second']<=a<b['end_second'])),
   away['team']:deepcopy(next(b['positions'] for b in away['blocks'] if b['start_second']<=a<b['end_second']))})
 return out

def assert_pair(segments,home,away):
 counters={home['team']:Counter(),away['team']:Counter()};clock=0
 for q in segments:
  a,z=q['start_second'],q['end_second']
  need(a==clock and z>a and q['seconds']==z-a and q['quarter']==a//720+1 and (z-1)//720==a//720,'Returned simultaneous clock/quarter')
  for t in (home,away):
   original=next(b for b in t['blocks'] if b['start_second']<=a<b['end_second'])
   need(z<=original['end_second'] and q[t['team']]==original['positions'],'Returned simultaneous source positions changed')
   for p in q[t['team']].values():counters[t['team']][p]+=z-a
  clock=z
 need(clock==2880,'Simultaneous duration')
 for t in (home,away):need(dict(counters[t['team']])==t['positive_player_seconds'],'Simultaneous player budget')

def rookie_role_plan(t,rookies):
 """New coach selection from unchanged incumbent role identity, no future stats.

 Use 60-second atoms only internally, preserving every position at every second.
 Donors outside the original starting five precede starters. Higher-priority
 rookies are never donors for a later rookie. Top3 receive a chosen starting
 nomination; other first-rounders receive12minutes of development opportunity.
 """
 atoms=[]
 for a in range(0,2880,60):
  b=next(b for b in t['blocks'] if b['start_second']<=a<b['end_second'])
  need(a+60<=b['end_second'],'Incumbent source boundary not60-second compatible')
  atoms.append(deepcopy(b['positions']))
 core=set(atoms[0].values());new_names={r['player'] for r in rookies};details=[]
 for r in sorted(rookies,key=lambda r:r['pick']):
  name=r['player'];pick=r['pick'];cls=r['participation']['public_prospect_identity']['position']
  allowed={'C':['C'],'G':['SG','PG'],'F':['SF','PF']}[cls]
  need(name not in {p for x in atoms for p in x.values()},'New rookie already consumes incumbent role')
  pos=ROOKIE_POSITIONS[pick]
  need(pos in allowed,'Chosen basketball role outside public prospect class')
  target={1:24,2:22,3:20}.get(pick,12);n=target
  chosen=[0] if pick<=3 else []
  candidates=sorted((i for i,x in enumerate(atoms) if i not in chosen and x[pos] not in new_names),
    key=lambda i:(atoms[i][pos] in core, sum(x[pos]==atoms[i][pos] for x in atoms),i))
  chosen+=candidates[:n-len(chosen)]
  need(len(chosen)==n,'Insufficient same-position development capacity')
  donor=Counter(atoms[i][pos] for i in chosen)
  for i in chosen:
   need(name not in atoms[i].values(),'Duplicate rookie in5-player atom')
   atoms[i][pos]=name
  details.append({'player':name,'pick':pick,'public_prospect_position':cls,
    'chosen_role':pos,'minutes':target,'chosen_starting_nomination':pick<=3,
    'donor_player_seconds':{p:n*60 for p,n in sorted(donor.items())},
    'coefficient':'-1','actual_future_NBA_performance_or_starts_certified':False})
 blocks=[]
 for i,ps in enumerate(atoms):
  a,z=i*60,(i+1)*60
  if blocks and blocks[-1]['positions']==ps and a%720!=0:blocks[-1]['end_second']=z
  else:blocks.append({'start_second':a,'end_second':z,'positions':ps})
 return {'blocks':blocks,'rookie_development':details,
         'new_starting_nomination':list(atoms[0].values()),
         'all_rookies_permanently_unplayed_selected':False}

def miles_role_plan(t):
 """Remove a noncontract actor without creating a phantom waiver/salary saving."""
 atoms=[]
 for a in range(0,2880,60):
  b=next(b for b in t['blocks'] if b['start_second']<=a<b['end_second'])
  need(a+60<=b['end_second'],'Miles source boundary60')
  atoms.append(deepcopy(b['positions']))
 pf=[i for i,x in enumerate(atoms) if x['PF']=='Miles Bridges']
 sf=[i for i,x in enumerate(atoms) if x['SF']=='Miles Bridges']
 need(len(pf)==20 and len(sf)==6,'Miles prior20PF/6SF minutes altered')
 pj=[i for i in pf if 'P.J. Washington' not in atoms[i].values()][:10]
 need(len(pj)==10,'Insufficient distinct5 PJ PF recovery cells')
 for i in pf:atoms[i]['PF']='P.J. Washington' if i in pj else 'Jalen McDaniels'
 for i in sf:
  need('Gordon Hayward' not in atoms[i].values(),'Hayward same-atom duplicate')
  atoms[i]['SF']='Gordon Hayward'
 blocks=[]
 for i,ps in enumerate(atoms):
  a,z=i*60,(i+1)*60
  if blocks and blocks[-1]['positions']==ps and a%720!=0:blocks[-1]['end_second']=z
  else:blocks.append({'start_second':a,'end_second':z,'positions':ps})
 return {'blocks':blocks,'reallocated_minutes':{'P.J. Washington':10,'Jalen McDaniels':10,'Gordon Hayward':6},
   'Miles_no_new_UPC_not_a_zero_cost_waiver':True,'original_Gamma_FA_QO_hold_preserved':True}

def admitted_rookies(team,s):
 return [r for r in s[BOARD]['rows'][:30] if r['conditional_final_rights_holder']==team and team!='CHI' and r['player']!='Chet Holmgren']

def apply_first_admission(t,s,rates):
 """Consume selected contract rows and full protected waiver costs, then coach.

 This does not treat a source nominal inactive rookie as a chosen FY23 DNP.
 The source explicitly leaves the role choice to this consumer.
 """
 team=t['team'];a=s[RSC];reg=a['team_registration'][team]
 first=[x for x in a['selected_first_RSCs'] if x['owner']==team]
 all_rr=[x for x in s[BOARD]['rows'][:30] if x['conditional_final_rights_holder']==team and team!='CHI']
 rr=admitted_rookies(team,s)
 need(reg['source_standard']==s[PORT]['team_functions'][team]['standard'] and reg['TW']==t['TW'],'RSC prior registration altered')
 need([(x['pick'],x['player']) for x in first]==[(x['pick'],x['player']) for x in all_rr],'RSC board identity/holder differs')
 clears=[x for x in a['selected_zero_budget_reserve_clearances'] if x['owner_before_clearance']==team]
 need([x['player'] for x in clears]==reg['cleared_reserves'],'Clearance actor set altered')
 need(len(clears)==max(0,len(t['standard'])+len(first)-15),'STD clearance count')
 for w in clears:
  need(w['player'] not in t['positive_player_seconds'] and w['old_all_template_positive_regulation_seconds']==0,'Waiver removes consumed positive actor')
  need(w['all_original_Gamma_reserved'] is True and w['all_new_July7_renewal_or_option_protected_liabilities_reserved'] is True and
       w['remaining_guaranteed_future_salary_reserved'] is True and w['cash_buyout_stretch_setoff_or_refund_selected'] is False,
       'Protected waiver charge erased')
  need(w['new_owner_or_assignment'] is None and w['actual_waiver_receipt_or_no_claim_certified'] is False,'Waiver assignment/actual promotion')
 expected=[p for p in t['standard'] if p not in reg['cleared_reserves']]+[x['player'] for x in first]
 need(reg['standard']==expected and reg['roster_effective_from']=='2022-07-11T09:00:00-04:00','Signed roster interval altered')
 for x in first:
  need(x['signed_at']=='2022-07-11T09:00:00-04:00' and x['first_season']=='2022-23' and
       x['roster_class']=='STANDARD' and x['base_percent']==120 and x['guaranteed_capyears']==[2022,2023],
       'New RSC term/date/form altered')
  need(x['fictional_consent_and_legal_participation_selected'] is True and x['actual_receipt_or_real_player_consent_certified'] is False and
       x['new_bonuses_loan_buyout']==0 and x['future_options_automatically_exercised'] is False,'RSC scope or bonus altered')
  rates[x['player']]={'fraction':'-1','prior_source':BOARD+'#/rows/'+str(x['pick']-1),
   'new_FY23_classification':'EXPLICIT_NEW_ROOKIE_CONSERVATIVE_PROXY_NOT_FUTURE_NBA_STATS'}
 t=deepcopy(t);t['standard']=deepcopy(expected)
 if team=='CHA':
  change=miles_role_plan(t);need(digest(change)==MILES_PLAN_MEANING,'Returned Miles rights-only role replacement changed')
  t['blocks']=change['blocks'];t['standard'].remove('Miles Bridges');expected=t['standard']
  t['Miles_rights_and_obligations_port']=deepcopy(next(e for e in s[OVERLAY]['selected_fictional_events'] if e['player']=='Miles Bridges'))
  t['Miles_reallocation']=change['reallocated_minutes']
 if rr:
  plan=rookie_role_plan(t,rr)
  need(digest(plan)==ROOKIE_PLAN_MEANING[team],'Returned new rookie role chronology differs from chosen plan')
  t['blocks']=plan['blocks'];t['rookie_development']=plan['rookie_development'];t['starting_nomination']=plan['new_starting_nomination']
  t['id']+=':FY23_FIRST_RSC_DEVELOPMENT'
 else:t['rookie_development']=[];t['starting_nomination']=list(t['blocks'][0]['positions'].values())
 positive=Counter()
 for b in t['blocks']:
  for p in b['positions'].values():positive[p]+=b['end_second']-b['start_second']
 excluded={'Chet Holmgren'} if team=='OKC' else set()
 t['active']=sorted(positive)+[p for p in expected if p not in positive and p not in excluded][:max(0,12-len(positive))]
 t['inactive']=[p for p in expected if p not in t['active']]
 t['positive_player_seconds']=assert_blocks(t['blocks'],expected,t['active'])
 need(set(t['inactive'])==set(expected)-set(t['active']),'Post-admission active partition')
 for r in rr:
  need(t['positive_player_seconds'][r['player']]=={1:24*60,2:22*60,3:20*60}.get(r['pick'],12*60),'Rookie development budget')
  need(r['player'] in t['standard'] and r['player'] in t['active'],'Unsigned/nonactive rookie consumed')
 t['RSC_registration_source']=RSC+'#/team_registration/'+team
 t['protected_waiver_costs_not_subtracted']=deepcopy(clears)
 return t

def assert_first_admission_return(t,team,s):
 reg=s[RSC]['team_registration'][team]
 expected_std=[p for p in reg['standard'] if not(team=='CHA' and p=='Miles Bridges')]
 need(t['team']==team and t['standard']==expected_std and t['TW']==reg['TW'],'Returned post-RSC/overlay registration altered')
 rookies=admitted_rookies(team,s)
 if rookies:
  projection={'blocks':t['blocks'],'rookie_development':t['rookie_development'],
   'new_starting_nomination':t['starting_nomination'],'all_rookies_permanently_unplayed_selected':False}
  need(digest(projection)==ROOKIE_PLAN_MEANING[team],'Returned admitted rookie chronology/development changed')
  need(t['id']==team+':'+SPECIAL.get(team,'NORMAL')+':FY23_FIRST_RSC_DEVELOPMENT','Returned admitted role identity')
 else:
  if team=='CHI':expected=[{k:deepcopy(b[k]) for k in ('start_second','end_second','positions')} for b in s[H22]['selected_role_template']['ordered_regulation_blocks']]
  else:expected=s[OLD]['shared_role_templates'][team+':'+SPECIAL.get(team,'NORMAL')]['blocks']
  need(t['blocks']==expected and t['rookie_development']==[],'Unchanged team/H22 chronology altered')
 sec=assert_blocks(t['blocks'],expected_std,t['active'])
 excluded={'Chet Holmgren'} if team=='OKC' else set()
 expected_active=sorted(sec)+[p for p in expected_std if p not in sec and p not in excluded][:max(0,12-len(sec))]
 need(t['active']==expected_active and t['inactive']==[p for p in expected_std if p not in expected_active] and
      t['positive_player_seconds']==sec,'Returned admitted nominations/player budgets changed')
 if team=='OKC':need('Chet Holmgren' in t['standard'] and 'Chet Holmgren' in t['inactive'] and 'Chet Holmgren' not in sec,'Chet root OUT/RSC preservation failed')
 if team=='CHA':
  need('Miles Bridges' not in t['standard'] and 'Miles Bridges' not in sec and len(t['standard'])==14,'Miles no-UPC source failed')
  need(t['Miles_rights_and_obligations_port']==next(e for e in s[OVERLAY]['selected_fictional_events'] if e['player']=='Miles Bridges') and
       t['Miles_reallocation']=={'P.J. Washington':10,'Jalen McDaniels':10,'Gordon Hayward':6},'Returned Miles obligations/role interpretation altered')
 need(t['protected_waiver_costs_not_subtracted']==[x for x in s[RSC]['selected_zero_budget_reserve_clearances'] if x['owner_before_clearance']==team],
      'Returned protected waiver obligations changed')
 need(t['RSC_registration_source']==RSC+'#/team_registration/'+team,'Returned RSC source pointer')

def result_row(g,home,away,rates,b2b):
 impacts={t['team']:sum(Fraction(rates[p]['fraction'])*n for p,n in t['positive_player_seconds'].items())/2880 for t in (home,away)}
 effect=VENUES.get(int(g['published_game_number']),('',)*5+(2,))[5]
 margin=impacts[g['home']]-impacts[g['away']]+effect+Fraction(b2b[g['away']]-b2b[g['home']],2)
 need(margin!=0,'Exact tie requires named finite tie policy')
 return {'calendar_key':g['calendar_key'],'published_date':g['published_date'],'home':g['home'],'away':g['away'],
  'original_venue_note':g['original_venue_note'],'home_effect_selected':effect,'b2b':deepcopy(b2b),
  'home_impact':str(impacts[g['home']]),'away_impact':str(impacts[g['away']]),'home_margin':str(margin),
  'winner':g['home'] if margin>0 else g['away'],'loser':g['away'] if margin>0 else g['home'],
  'template_home':home['id'],'template_away':away['id'],'simultaneous_segments':paired(home,away),
  'selected_regulation_model_result':True,'selected_overtime_periods':0,'actual_NBA_game_id':None,
  'actual_NBA_score_or_health_certified':False,'fictional_score':None}

def assert_result(x,g,home,away,rates,b2b):
 for k in ('calendar_key','published_date','home','away','original_venue_note'):need(x[k]==g[k],'Returned result date/actors altered')
 need(x['b2b']==b2b and x['template_home']==home['id'] and x['template_away']==away['id'],'Returned state/fatigue altered')
 ih=sum(Fraction(rates[p]['fraction'])*n for p,n in home['positive_player_seconds'].items())/2880
 ia=sum(Fraction(rates[p]['fraction'])*n for p,n in away['positive_player_seconds'].items())/2880
 e=0 if int(g['published_game_number']) in (439,678) else 2
 m=ih-ia+e+Fraction(b2b[g['away']]-b2b[g['home']],2)
 need(x['home_effect_selected']==e and x['home_impact']==str(ih) and x['away_impact']==str(ia) and x['home_margin']==str(m),'Returned model arithmetic changed')
 need(x['winner']==(g['home'] if m>0 else g['away']) and x['loser']==(g['away'] if m>0 else g['home']),'Returned winner changed')
 need(x['selected_overtime_periods']==0 and x['actual_NBA_game_id'] is None and x['actual_NBA_score_or_health_certified'] is False and x['fictional_score'] is None,'Actual/OT/score promotion')
 assert_pair(x['simultaneous_segments'],home,away)

def build(root=ROOT):
 s=inputs(root);context=primary_context();calendar=calendar_source(s);portfolio=s[PORT];functions=portfolio['team_functions']
 need(calendar==s[LEAGUE],'Returned reconstructed calendar differs from frozen physical CSV')
 need(context['Canada']=={'capture_path':str(CANADA_CAPTURE),'capture_bytes_sha256':CANADA_CAPTURE_SHA,
   'capture_is_not_original_HTTP_bytes':True,**json.loads(text(CANADA_CAPTURE))},'Returned primary observation provenance changed')
 need(len(functions)==30,'30 contract functions missing')
 if ADMISSION_SOURCE_FROZEN:
  need(s[RSCPEER]['independent_review_completed'] is True and s[RSCPEER]['source_sha256'][RSC]==PINS[RSC],'RSC peer scope/staleness changed')
  need(len(s[RSC]['selected_first_RSCs'])==29 and len(s[RSC]['selected_zero_budget_reserve_clearances'])==25,'First29/waiver25 input changed')
  ov=s[OVERLAY]
  for p,pin in ov['source_normalized_sha256'].items():need(sha(root/p)==pin,'Overlay source stale '+p)
  events={x['player']:x for x in ov['selected_fictional_events']}
  need(events['Chet Holmgren']['selection']=='SEASON_OUT_WITH_RSC_PRESERVED' and events['Chet Holmgren']['positive_seconds_each_game']==0 and
       events['Chet Holmgren']['rookie_contract_and_protected_salary_retained'] is True,'Chet overlay altered')
  need(events['Miles Bridges']['selection']=='NO_NEW_UPC_RIGHTS_ONLY' and events['Miles Bridges']['new_standard_UPC'] is False and
       events['Miles Bridges']['standard_registration_delta']==-1,'Miles overlay altered')
 contract_rows={r['id']:r for r in portfolio['NPC_contract_rows']}
 templates={};catalog=[];rates=selected_rates(s)
 # Coefficients must remain direct prior fractions, even if a returned helper is patched.
 for p,v in s[OLD]['selected_productivity_inputs'].items():
  x=rates[canonical_name(p)]
  need(x=={'fraction':str(Fraction(v['fraction'])),'prior_source':v['source'],
   'new_FY23_classification':'SELECTED_CONSERVATIVE_ZERO_GROWTH_PROXY_NOT_OBSERVED_FY23'},'Returned prior productivity or classification altered')
 need(rates['Walker Kessler']=={'fraction':'-1','prior_source':H22+'#/selected_role_template/Kessler_new_NBA_productivity',
   'new_FY23_classification':'SELECTED_NEW_ROOKIE_PROXY_NOT_NBA_STATS'},'Returned Kessler productivity or classification changed')
 need(set(rates)=={canonical_name(p) for p in s[OLD]['selected_productivity_inputs']}|{'Walker Kessler'},'Unbound productivity name added')
 for team,f in functions.items():
  expected=[{k:g[k] for k in ('calendar_key','published_date','home','away')} for g in calendar if team in (g['home'],g['away'])]
  need(f['dates']==expected,'Portfolio dates differ from calendar: '+team)
  if team!='CHI':
   need(f['operator_function_selected'] is True,'NPC contract function not selected: '+team)
   for p in f['standard']:
    row=contract_rows.get(team+':'+p);need(row is not None and row['candidate_owner']==team and row['original_all_Gamma_reserved'] is True,'Named contract/owner/Gamma absent')
    ep=row.get('execution_policy',{})
    need(ep.get('delegated_same_owner_routine_implementation_selected') is True and ep.get('service_window')==['2022-07-07','2023-04-09'],'NPC current period not covered')
  t=team_template(team,s);t['positive_player_seconds']=assert_template(t,team,s)
  if ADMISSION_SOURCE_FROZEN:
   t=apply_first_admission(t,s,rates);assert_first_admission_return(t,team,s)
  need(set(t['positive_player_seconds'])<=set(rates),'Missing named productivity: '+team)
  templates[team]=t
  catalog.extend({'team':team,'player':p,'registration':kind} for kind,ps in [('STANDARD',t['standard']),('TWO_WAY',t['TW'])] for p in ps)
 need(len({x['player'] for x in catalog})==len(catalog),'Global named owner collision')
 if ADMISSION_SOURCE_FROZEN:
  need(len(catalog)==450 and sum(x['registration']=='STANDARD' for x in catalog)==448,'448STD2TW selected overlay roster count')
  for r in s[RSC]['selected_first_RSCs']:
   need(rates[r['player']]=={'fraction':'-1','prior_source':BOARD+'#/rows/'+str(r['pick']-1),
     'new_FY23_classification':'EXPLICIT_NEW_ROOKIE_CONSERVATIVE_PROXY_NOT_FUTURE_NBA_STATS'},'Returned rookie productivity changed')
 rows=[];last={};records={t:{'wins':0,'losses':0} for t in templates}
 for g in calendar:
  dt=date.fromisoformat(g['published_date']);b2b={t:int(last.get(t)==dt-timedelta(days=1)) for t in (g['home'],g['away'])}
  h,a=templates[g['home']],templates[g['away']];row=result_row(g,h,a,rates,b2b);assert_result(row,g,h,a,rates,b2b)
  rows.append(row);records[row['winner']]['wins']+=1;records[row['loser']]['losses']+=1
  for t in b2b:last[t]=dt
 need(all(sum(v.values())==82 for v in records.values()) and sum(v['wins'] for v in records.values())==1230,'Joint wins/losses')
 chi=[x for x in rows if 'CHI' in (x['home'],x['away'])]
 return {'id':'NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS','baseline_main':BASELINE,
  'status':('SELECTED_1230_BOUND_RESULTS_29_SIGNED_28_POSITIVE_ROOKIES_NAMED_AVAILABILITY_OVERLAY_INDEPENDENT_REVIEW_PENDING' if ADMISSION_SOURCE_FROZEN else
            'SELECTED_BOUND_FRACTION_RESULT_MODEL_ROOKIE_ADMISSION_SENSITIVITY_INDEPENDENT_REVIEW_PENDING'),
  'source_sha256':{**PINS,SELF:sha(root/SELF)},'policy':deepcopy(POLICY),'primary_context':context,
  'owner_catalog':catalog,'shared_team_templates':templates,'selected_productivity_inputs':rates,
  'rows':rows,'Chicago_rows':chi,'team_records':records,
  'rookie_admission_boundary':{'source_rights':len(portfolio['NPC_2022_rights']),
   'source_new_UPCs':len(s[RSC]['selected_first_RSCs']) if ADMISSION_SOURCE_FROZEN else sum(bool(x['new_UPC_selected']) for x in portfolio['NPC_2022_rights']),
  'first_RSC_and_selected_positive_development_executed':ADMISSION_SOURCE_FROZEN,
   'NPC_first_rookies_given_positive_development':sum(len(t.get('rookie_development',[])) for t in templates.values()),
   'Chet_signed_RSC_inactive_OUT_preserved':True,'Miles_no_UPC_rights_and_obligations_preserved':True,
   'all_first_round_rights_only_sensitivity_not_whole_season_acceptance':not ADMISSION_SOURCE_FROZEN,
   'same_owner_minimum_contract_form_not_named_core_market_price_ACCEPTANCE':True,
   'named_core_market_price_family_pending':portfolio.get('named_core_market_price_family_pending',True),
   'next_required_realism_refinement':('Named core renewal market-price family; no income/consent certification from minimum floor.' if ADMISSION_SOURCE_FROZEN else
    '29 NPC first-round120% RSC via legal vacancy or zero-minute reserve waiver preserving full Gamma; second29 may remain rights-only.'),
   'all_58_UPCs_new_completion_gate':False,'all_students_permanently_non_NBA':False},
  'named_availability_boundary':{'source':OVERLAY,'source_sha256':PINS[OVERLAY],
   'Chet_RSC_and_all_protected_salary_preserved_season_OUT':True,
   'Miles_independent_June27_incident_and_unresolved_contract_decision_preserved':True,
   'April2023_discipline_not_retroactive_cause':True,
   'Miles_standard_slot_removed_but_FA_QO_hold_and_obligations_not_erased':True,
   'new_replacement_contract_selected':False,'actual_clinical_or_private_receipts_certified':False},
  'venue_support':{'official_release':'https://pr.nba.com/2022-23-nba-schedule/',
   'classification':'Published PDF facts plus explicit model home-effect policy; later NBA game IDs are diagnostic locators only.',
   'rows':[{'published_game_number':n,'date':v[0],'home':v[1],'away':v[2],'venue':v[4],'home_effect':v[5],
            'NBA_observation_locator':f'https://www.nba.com/game/002220{n:04}'} for n,v in VENUES.items()]},
  'summary':{'league_games':len(rows),'team_dates':2460,'NPC_team_dates':2378,'Chicago_results':len(chi),
   'CHI_wins':records['CHI']['wins'],'CHI_losses':records['CHI']['losses'],'team_templates':len(templates),
   'unique_named_owners':len(catalog),'duplicate_owners':0,'new_non_CHI_results':1148,'historical_winners_copied':0,
   'standard_registration':448,'TW_registration':2,'NPC_signed_first_rookies':29,'NPC_positive_first_rookies':28,
   'international_neutral_games':2,'SAS_alternate_home_games':3,'total_wins':1230,'total_losses':1230},
  'certification':{'regulation_result_model_executed':True,'independent_review_completed':False,
   'selected_lawful_registration_role_and_1230_bound_model_executed':ADMISSION_SOURCE_FROZEN,
   'whole_FY23_six_cost_family_certified':False,'named_core_market_price_family_certified':False,
   'whole_FY23_accepted':False,'actual_contract_or_medical_receipts_certified':False,
   'standings_tiebreak_or_2023_draft_control_executed':False,'whole_macro3_complete':False},
  'remaining_finite_consumers':['Separate named core market-price and six-cost functions; this bound result calculation does not certify whole-team financial totals.',
   'Source-based conference/division tie-break, play-in/playoff and2023conditional rights functions.',
   'Separate2023QO/extension execution; model wins do not issue QO or certify actual stat receipts.'],
  'progress':{'1':'COMPLETE','2':'COMPLETE','3':'IN_PROGRESS','4':'IN_PROGRESS','5':'PENDING','6':'PENDING','7':'CLOSED'},
  'unfinished_macro_groups':5,'unfinished_through_6':4,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0,'manuscript_allowed':False}

def render(v):
 lines=['# 2022–23 전역 규정시간 결과 모델','',
  '공식 발표 일정1230키·30팀2460날짜와 명명 계약 함수를 결합한다. 기존2021–22 결과는 복사하지 않는다. '+
  'CHI는 H22의82날짜·Mark32/Caruso18/P32/Kessler12와 등록15STD2TW를 소비한다.','',
  f"작업 결과: CHI {v['summary']['CHI_wins']}승/{v['summary']['CHI_losses']}패. 이는 고정 생산성·가상 가용·규정시간 모델 결과이며 실제 NBA 예측·점수·MVP·우승 인증이 아니다.",'',
  '## 선택과 한계','',
  'March25/EB 계수를 새해의 보수적 성장0·노화0 proxy로 명시적으로 선택했다. 전성기 Klay의 능력0 또는 미래 NBA 관측값을 뜻하지 않는다. '+
  'NPC 전경기 OT0는 CHI STAT23_A와 별개 루틴 모델이다. BKN 전일 가용은 새 가상 구단 nomination이며 과거 NYC/Canada OUT를 소급하지 않는다.','',
  '멕시코시티·파리2경기는 모델 홈 효과0, Alamodome/Austin3경기는 명목 SAS 홈 효과2다. 공식 장소 사실과 효과 모델은 구분한다. '+
  '[NBA 공식 발표](https://pr.nba.com/2022-23-nba-schedule/).','',
  'NPC 첫29명은 120%RSC·기존 빈자리4/제로분 reserve방출25·원Γ 전액 보존으로 등록하고 28명에게 새 가상 기용분을 준다. 신인 BPM−1은 미래 관측이 아닌 보수적 작업계수다. Chet는 RSC/보호급여를 유지한 시즌 OUT이며 건강한24분안은 미선택 감도다. 모든58명 UPC가 새 필수조건인 것은 아니다.','',
  'Miles는 별도 선택된 신규UPC 없음/권리만 유지 분기다. 6월27일 독립 사건과 미해결 계약결정을 보존하며 2023년4월 징계를 과거 원인으로 소급하지 않는다. CHA는14STD·빈자리1을 유지하고 기존 등록선수에게만 분을 재배정한다. FA/QO hold·원채무를 삭제하거나 대체계약을 추가하지 않는다. 전체 명명 소유는448STD+2TW=450명이고 중복은0이다.','',
  '계약의 합법 가상 동의 함수와 선수분·명명 소유를 소비했다. 실제 사적 장부/기관 접수/의료/경기 점수 또는 현재 모든 비용의 정확 금액을 인증하지 않는다.','',
  '## 전역 작업 기록','', '| 팀 | 승 | 패 |','|---|---:|---:|']
 lines += [f"| {t} | {r['wins']} | {r['losses']} |" for t,r in sorted(v['team_records'].items())]
 lines += ['','## 다음 입력','']+['- '+x for x in v['remaining_finite_consumers']]
 lines += ['','[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','',
  '| 묶음 | 현황 |','|---|---|','| 1 | 완료 |','| 2 | 완료 |','| 3 | 진행 |','| 4 | 진행 |','| 5 | 대기 |','| 6 | 대기 |','| 7 | CLOSED |','',
  '미완료 큰 묶음5 · 6번까지4 · v0.30 PARTIAL · CLOSED · Pack0 · 원고0.']
 return '\n'.join(lines)+'\n'
def validate(v,root=ROOT):
 try:need(v==build(root),'Saved result differs from physical constructor');return []
 except (AssertionError,KeyError,ValueError) as e:return [str(e)]
def self_test():
 controls=[]
 def rejects(label,fn):
  try:fn()
  except (AssertionError,KeyError,ValueError):controls.append(label);return
  raise AssertionError('FALSE_PASS '+label)
 original_load=load
 def swapped(root,p):
  v=original_load(root,p)
  if p==OLD:v['selected_productivity_inputs']['Carter']['fraction']='100'
  return v
 with patch(__name__+'.load',side_effect=swapped):rejects('physical_prior_productivity_substitution',build)
 original_template=team_template
 def pos(team,s):
  t=original_template(team,s)
  if team=='ATL':p=t['blocks'][0]['positions'];p['PG'],p['SG']=p['SG'],p['PG']
  return t
 with patch(__name__+'.team_template',side_effect=pos):rejects('returned_same_budget_position_swap',build)
 original_result=result_row
 def fault(g,h,a,r,b):
  row=original_result(g,h,a,r,b);row['winner']=row['loser'];return row
 with patch(__name__+'.result_row',side_effect=fault):rejects('returned_wrong_winner',build)
 def venue(g,h,a,r,b):
  row=original_result(g,h,a,r,b)
  if int(g['published_game_number'])==635:row['home_effect_selected']=0
  return row
 with patch(__name__+'.result_row',side_effect=venue):rejects('Alamodome_false_international_neutral',build)
 original_admission=apply_first_admission
 def chet_active(t,s,r):
  v=original_admission(t,s,r)
  if v['team']=='OKC':
   v['active'].append('Chet Holmgren');v['inactive'].remove('Chet Holmgren')
  return v
 with patch(__name__+'.apply_first_admission',side_effect=chet_active):rejects('returned_Chet_OUT_actor_active',build)
 def miles_port(t,s,r):
  v=original_admission(t,s,r)
  if v['team']=='CHA':v['Miles_rights_and_obligations_port']['selection']='NO_UPC_AND_ALL_OBLIGATIONS_ZERO'
  return v
 with patch(__name__+'.apply_first_admission',side_effect=miles_port):rejects('returned_Miles_obligations_erased',build)
 return controls
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(dump(v),encoding='utf-8');(ROOT/MD).write_text(render(v),encoding='utf-8')
 result={'summary':v['summary']}
 if a.check:need(not validate(json.loads(text(ROOT/OUT))),'Saved JSON stale');need(text(ROOT/MD)==render(v),'MD stale');result['current']=True
 if a.self_test:result['negative_controls']=self_test()
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
