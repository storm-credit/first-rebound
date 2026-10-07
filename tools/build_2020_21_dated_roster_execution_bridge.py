"""Audit all existing 1174 dated models against a compact public roster bridge.

This preserves source minutes, results and health models. Public date-only events
are a working candidate, not actual league registration/financial certification.
Unresolved membership and slot conflicts are emitted, never filled by zero.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import date, timedelta
import hashlib
import json
import os
from pathlib import Path
import re
import unicodedata

from pypdf import PdfReader
import build_2020_21_regular_clock_completion as clock
import build_2021_l2_working_minutes as playin
import build_2021_all_playoff_coach_plans as playoff
import build_orlando_registration_legal_domain as orl_domain
import build_den_cle_registration_domain as den_cle_domain

ROOT = Path(__file__).resolve().parents[1]
TEMP = Path(os.environ.get('TEMP', 'C:/Users/Storm Credit/AppData/Local/Temp'))
OUT = 'simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json'
MD = OUT.replace('.json', '.md')
SELF = 'tools/build_2020_21_dated_roster_execution_bridge.py'
REG = 'simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.json'
L2 = 'simulation/NBA_2021_L2_WORKING_MINUTE_MODELS.json'
POST = 'simulation/NBA_2021_ALL_DATED_PLAYOFF_COACH_PLANS.json'
NON = 'simulation/NBA_2021_L2_NONPLAYOFF_ROSTER_SCOPE.json'
AUTH = 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
MAP = 'control/AUTHORITY_MAP.md'
DIRECTION = 'canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json'
F45 = 'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json'
C2 = 'canon/CLEVELAND_2021_VAREJAO_C2_DECISION.json'
CASCADE = 'simulation/2021_WASHINGTON_CHICAGO_PORTLAND_TRANSACTION_CASCADE.md'
DRAFT = ['simulation/2020_DRAFT_' + x + '_RELANDING_BOARD.md' for x in
         ('PATRICK_WILLIAMS','KILLIAN_HAYES','KIRA_LEWIS','ISAIAH_STEWART',
          'SADDIQ_BEY','ZEKE_NNAJI','RJ_HAMPTON','TYRELL_TERRY')]
SOURCES = [REG,L2,POST,NON,AUTH,MAP,DIRECTION,F45,C2,CASCADE,
           'simulation/CAUSALITY_MODEL.md',
           'research/CHICAGO_2020_21_OPENING_ROSTER_BASELINE.md',
           'simulation/GSW_HUTCHISON_2018_2021_OPERATING_CANDIDATES.json',
           'research/GSW_G1_REMAINING_APRON_COSTS_2026_10_07.json',
           'research/EAST_2021_PLAYOFF_COACH_INPUTS_2026_10_07.json',
           'research/WEST_2021_PLAYOFF_COACH_INPUTS_2026_10_07.json',SELF] + DRAFT
SOURCES += ['research/DEN_LAL_2021_COACH_PLAN_SOURCE_BRIDGE.json',
            'tools/build_2020_21_regular_clock_completion.py',
            'tools/build_2021_l2_working_minutes.py',
            'tools/build_2021_all_playoff_coach_plans.py']
SOURCES += ['research/ORLANDO_REGISTRATION_LEGAL_DOMAIN_2026_10_05.json','research/DEN_CLE_REGISTRATION_LEGAL_DOMAIN_2026_10_05.json','research/ORLANDO_PUBLIC_EVENT_COVERAGE_2026_10_05.json','tools/build_orlando_registration_legal_domain.py','tools/build_den_cle_registration_domain.py']
RAW = {
 'opening': ('fr-den-lal-opening-20261006.pdf','75a981d64c87de34f7d7896f3a0b1e695b1ed0a3c0e8d4b6638cef71c489ffa0','https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/goduke.com/documents/2020/12/22/2020_21_Opening_Day_Rosters_12_22_20.pdf?timestamp=20201222074936'),
 'movement': ('fr-nba-player-movement-2026-10-04.json','3d9d7a6dd7ccd39ddfdd1799a26ef9901b44682d85a26f05239b468a8ae92e3a','https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json'),
 'cba2017': ('fr-2017-cba.pdf','66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a','https://nbpa.com/cba')}
RAW['tw2021'] = ('fr-shams-twoway20210311-oembed.json','048b552f91bc67e7f8084dbd06b0a62cad014a167a457166c70400dfd3c3a44d','https://publish.twitter.com/oembed?url=https://twitter.com/ShamsCharania/status/1370149027786932228&omit_script=true')
RAW['mem_hardship_guide']=('fr-roster-execution-source-20261007/MEM_GUIDE.pdf','036f34540f0086be21662033dc37727550fe8809f44b364cdbc8f74906235f9c','https://s3.grizzliesapp.com/assets/media_guides/MG_22-23_Media_Guide_FullBook.pdf')
TEAM_IDS = {2737:'ATL',2738:'BOS',2739:'CLE',2740:'NOP',2741:'CHI',2742:'DAL',2743:'DEN',2744:'GSW',2745:'HOU',2746:'LAC',2747:'LAL',2748:'MIA',2749:'MIL',2750:'MIN',2751:'BKN',2752:'NYK',2753:'ORL',2754:'IND',2755:'PHI',2756:'PHX',2757:'POR',2758:'SAC',2759:'SAS',2760:'OKC',2761:'TOR',2762:'UTA',2763:'MEM',2764:'WAS',2765:'DET',2766:'CHA'}
PDF_HEADERS = [
 ['ATLANTA','BOSTON','BROOKLYN','CHARLOTTE','CHICAGO'],
 ['CLEVELAND','DALLAS','DENVER','DETROIT','GOLDEN STATE'],
 ['HOUSTON','INDIANA','LA CLIPPERS','L.A. LAKERS','MEMPHIS'],
 ['MIAMI','MILWAUKEE','MINNESOTA','NEW ORLEANS','NEW YORK'],
 ['OKLAHOMA CITY','ORLANDO','PHILADELPHIA','PHOENIX','PORTLAND'],
 ['SACRAMENTO','SAN ANTONIO','TORONTO','UTAH','WASHINGTON']]
PDF_TEAMS = [['ATL','BOS','BKN','CHA','CHI'],['CLE','DAL','DEN','DET','GSW'],['HOU','IND','LAC','LAL','MEM'],['MIA','MIL','MIN','NOP','NYK'],['OKC','ORL','PHI','PHX','POR'],['SAC','SAS','TOR','UTA','WAS']]
FRANCHISE_NAMES = {'Atlanta Hawks':'ATL','Boston Celtics':'BOS','Brooklyn Nets':'BKN','Charlotte Hornets':'CHA','Chicago Bulls':'CHI','Cleveland Cavaliers':'CLE','Dallas Mavericks':'DAL','Denver Nuggets':'DEN','Detroit Pistons':'DET','Golden State Warriors':'GSW','Houston Rockets':'HOU','Indiana Pacers':'IND','LA Clippers':'LAC','Los Angeles Clippers':'LAC','Los Angeles Lakers':'LAL','L.A. Lakers':'LAL','Memphis Grizzlies':'MEM','Miami Heat':'MIA','Milwaukee Bucks':'MIL','Minnesota Timberwolves':'MIN','New Orleans Pelicans':'NOP','New York Knicks':'NYK','Oklahoma City Thunder':'OKC','Orlando Magic':'ORL','Philadelphia 76ers':'PHI','Phoenix Suns':'PHX','Portland Trail Blazers':'POR','Sacramento Kings':'SAC','San Antonio Spurs':'SAS','Toronto Raptors':'TOR','Utah Jazz':'UTA','Washington Wizards':'WAS'}

def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def digest(b): return hashlib.sha256(b).hexdigest()
def sha(p): return digest((ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode())
def norm(name):
    s=unicodedata.normalize('NFKD',name).encode('ascii','ignore').decode().lower()
    s=re.sub(r'[^a-z0-9]','',s)
    return {'nicolasclaxton':'nicclaxton','kjmartin':'kenyonmartinjr',
            'enesfreedom':'eneskanter','xaviertillmansr':'xaviertillman',
            'camreynolds':'cameronreynolds'}.get(s,s)

def input_models():
    r,l,p=read(REG),read(L2),read(POST)
    clock.validate(r); clock.validate_against_sources(r)
    if l != playin.build(): raise ValueError('L2 source reconstruction mismatch')
    playoff.validate(p)
    games=[]
    for row in r['team_games']:
        games.append(dict(phase='REGULAR',event_id=row['event_id'],date=row['date'],team=row['team'],
           seconds=row['player_seconds'],starters=row['starters'],duration=row['game_duration_seconds'],source=REG,
           pointer=f"team_games:event_id={row['event_id']};team={row['team']}",absent=[]))
    for g in l['games']:
        for t,v in g['teams'].items():
            games.append(dict(phase='PLAYIN',event_id=g['event_id'],date=g['date'],team=t,
              seconds=v['player_seconds'],starters=v['starters'],duration=g['duration_model_seconds'],source=L2,
              pointer=f"games:event_id={g['event_id']};teams.{t}",absent=v.get('modeled_absent',[])))
    for g in p['games']:
        for t,v in g['teams'].items():
            games.append(dict(phase='PLAYOFF',event_id=f"{g['series']}:G{g['game']}",date=g['date_model'],team=t,
              seconds={n:m*60 for n,m in v['planned_minutes'].items()},starters=g['blocks'][0][t],duration=2880,source=POST,
              pointer=f"games:series={g['series']};game={g['game']};teams.{t}",
              absent=[n for n,x in v['players'].items() if x['mode']=='MODELED_ABSENT']))
    if len(games)!=2348 or Counter(g['phase']for g in games)!={'REGULAR':2160,'PLAYIN':12,'PLAYOFF':176}: raise ValueError('model domain changed')
    keys=[(g['phase'],g['event_id'],g['team'])for g in games]
    if len(keys)!=len(set(keys)):raise ValueError('duplicate source team-game')
    return sorted(games,key=lambda g:(g['date'],g['team'],g['event_id']))

def opening():
    roster={t:{} for t in TEAM_IDS.values()};locators={}; reader=PdfReader(TEMP/RAW['opening'][0])
    for page_no,page in enumerate(reader.pages,1):
        lines=page.extract_text(extraction_mode='layout').splitlines(); active=None;columns=[]
        for line in lines:
            found=next((i for i,h in enumerate(PDF_HEADERS)if all(n in line for n in h)),None)
            if found is not None:
                active=found;columns=[line.index(n)for n in PDF_HEADERS[found]];continue
            if active is None:continue
            if line.lstrip().startswith('* Indicates') or 'PAGE ' in line or '- more' in line or '# #' in line:
                active=None;continue
            if not line.strip() or 'INACTIVE/TWO-WAY' in line:continue
            for j,t in enumerate(PDF_TEAMS[active]):
                cell=line[columns[j]:columns[j+1] if j<4 else None].strip()
                if not cell:continue
                if not re.fullmatch(r"[A-Za-z0-9 .'*’\-]+",cell):raise ValueError(('unparsed opening cell',cell))
                name=cell.rstrip('*');roster[t][norm(name)]={'name':name,'class':'TWO_WAY'if cell.endswith('*')else'STANDARD','origin':'OPENING_PDF','expiry':None}
                locators[t]={'pdf_page':page_no,'column_header':PDF_HEADERS[active][j],'inactive_nonstarred_is_standard':True}
    if len(roster)!=30 or any(not v for v in roster.values()):raise ValueError('opening 30team coverage')
    for t,v in roster.items():
        if sum(x['class']=='STANDARD'for x in v.values())>15 or sum(x['class']=='TWO_WAY'for x in v.values())>2:raise ValueError(('opening parse count',t))
    return roster,locators

def parse_event(i,x):
    if not x['PLAYER_SLUG']:return None
    desc=x['TRANSACTION_DESCRIPTION'];s=re.sub(r'^.*? (?:re-signed|signed|waived|received|claimed) (?:guard/forward |forward/center |guard |forward |center )?','',desc)
    s=re.split(r' to a | from | off waivers\.',s)[0].rstrip('.')
    if s==desc:raise ValueError(('unparsed movement',i,desc))
    origin=None
    if x['Transaction_Type']=='Trade':
        origin_name=desc.split(' from ',1)[1].rstrip('.')
        origin=FRANCHISE_NAMES.get(origin_name)
        if origin is None:raise ValueError(('trade origin unknown',i,origin_name))
    kind=x['Transaction_Type'];cls='TWO_WAY'if'Two-Way Contract'in desc else'STANDARD'
    return dict(id=f'FEED:{i}',date=x['TRANSACTION_DATE'][:10],type=kind,team=TEAM_IDS[int(x['TEAM_ID'])-1610610000],
       player=s,origin=origin,contract_class=cls,ten_day='10-Day Contract'in desc,
       source_row=i,source_row_sha256=digest(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()),
       classification='PUBLIC_ORIGINAL_DATE_EVENT_WORKING_CARRY',actual_execution_certified=False)

def approved_roster_delta(roster):
    changes=[('CHI','Chandler Hutchison','CHI','Protagonist'),('CHI','Patrick Williams','DET','Patrick Williams'),
      ('CHA','LaMelo Ball','CHI','LaMelo Ball'),('MIN','Anthony Edwards','CHA','Anthony Edwards'),
      ('MIN',None,'MIN','Fictional Rival'),('DET','Killian Hayes','NOP','Killian Hayes'),
      ('NOP','Kira Lewis Jr.','DET','Kira Lewis Jr.'),('DET','Saddiq Bey','DEN','Saddiq Bey'),
      ('DEN','R.J. Hampton','DAL','R.J. Hampton'),('DAL','Tyrell Terry','CHA','Tyrell Terry'),
      ('POR','Gary Trent Jr.','WAS','Gary Trent Jr.'),('POR',None,'POR','Jacob Evans')]
    # Remove first, then insert: chains never delete a newly inserted player.
    for old,name,_,_ in changes:
        if name:roster[old].pop(norm(name))
    for _,_,new,name in changes:
        roster[new][norm(name)]={'name':name,'class':'STANDARD','origin':'APPROVED_TEAM_LANDING_WORKING_STANDARD_FAMILY','expiry':None}
    return [{'id':f'OPEN_DELTA:{i}', 'old_team':o,'removed':n,'new_team':t,'added':a,
       'source':MAP,'classification':'APPROVED_DIRECTION_OR_CANDIDATE_CONTRACT_FAMILY_NOT_EXACT_FINANCIAL_SELECTION'}for i,(o,n,t,a)in enumerate(changes)]

def adjust_event(e):
    """Only named approved direction changes; no automatic hypothetical cut."""
    e=deepcopy(e);n=norm(e['player']);t=e['team'];d=e['date']
    omitted=False
    if d=='2021-03-25'and e['type']=='Trade':
        if n in map(norm,['Nikola Vucevic','Al-Farouq Aminu','Wendell Carter Jr.','Otto Porter Jr.','Norman Powell','Gary Trent Jr.','Rodney Hood','Troy Brown Jr.','Chandler Hutchison','JaVale McGee','Isaiah Hartenstein']):omitted=True
        if n==norm('R.J. Hampton')and t=='ORL':e['player']='Zeke Nnaji';e['classification']='APPROVED_T1_NNAJI_REPLACES_HAMPTON';e['direction_source']=DIRECTION
    if n==norm('Donta Hall')and t=='ORL'and d=='2021-05-09':omitted=True;e['direction_source']=F45
    if n==norm('Anderson Varejao')and t=='CLE'and d>='2021-05-04':omitted=True;e['direction_source']=C2
    e['omitted_by_approved_direction']=omitted
    return e

def expiry_for(e,regular_dates):
    if not e['ten_day']:return None
    third=[d for d in regular_dates[e['team']]if d>=e['date']]
    end=(date.fromisoformat(e['date'])+timedelta(days=9)).isoformat()
    return max(end,third[2]if len(third)>=3 else end)

def build():
    raw={}
    for key,(fn,pinned,url)in RAW.items():
        b=(TEMP/fn).read_bytes()
        if digest(b)!=pinned:raise ValueError(('raw cache mismatch',key))
        raw[key]={'url':url,'cache_path':str(TEMP/fn),'raw_sha256':pinned,'bytes':len(b),'new_collection':False}
    text=PdfReader(TEMP/RAW['cba2017'][0]).pages[68].extract_text()
    if 'encompassing three (3)'not in text or 'ten (10) days'not in text:raise ValueError('10day source changed')
    games=input_models();historical,locators=opening();roster=deepcopy(historical)
    authority=(ROOT/MAP).read_text(encoding='utf-8-sig')
    for term in ('Wiseman→Edwards→LaMelo AUTHOR_LOCKED','Hayes New Orleans 13 AUTHOR_LOCKED','Bey 22 AUTHOR_LOCKED','Nnaji 24 AUTHOR_LOCKED','Hampton Dallas 31 AUTHOR_LOCKED','Charlotte Terry 32 AUTHOR_LOCKED'):
        if term not in authority:raise ValueError(('draft authority semantic pin',term))
    direction=read(DIRECTION)['approved']
    if 'Gary Harris, Zeke Nnaji'not in direction['T1']or'Nikola Vucevic remains with Orlando'not in direction['T2']or'Norman Powell remains with Toronto'not in direction['T4']:raise ValueError('direction source changed')
    follow=read(F45)['selected']
    if follow != {'F4_HALL':'Orlando does not re-sign Donta Hall on 2021-05-09; his April contracts and earlier appearances remain in the alternate ledger.',
       'F5_MCGEE':'Denver and Cleveland do not execute their 2021-03-25 JaVale McGee/Isaiah Hartenstein and two-second-round-pick trade; McGee remains with Cleveland and Hartenstein with Denver.'}:raise ValueError('approved F4/F5 semantic direction changed')
    c2=read(C2)['selected']
    if c2['route']!='C2_VAREJAO_NO_RETURN_SIGNING'or c2['event_direction']!='Cleveland does not sign Anderson Varejao on 2021-05-04 or execute the 2021-05-14 follow-up contract in the alternate 2020-21 season.':raise ValueError('C2 direction changed')
    initial_deltas=approved_roster_delta(roster)
    initial={t:deepcopy(v)for t,v in roster.items()}
    feed=json.loads((TEMP/RAW['movement'][0]).read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    final_date=max(g['date']for g in games)
    # Explicit known opening-publication boundary: the NBA feed has the JTA
    # two-way signature Dec21, the existing official guide Dec22, while the
    # opening PDF lists only Mannion. Do not call the missing PDF row absence.
    events=[adjust_event(parse_event(i,x))for i,x in enumerate(feed)if
      ('2020-12-22'<=x['TRANSACTION_DATE'][:10]<=final_date or
       (x['PLAYER_SLUG']=='juan-toscano-anderson'and x['TRANSACTION_DATE'][:10]=='2020-12-21'and x['Transaction_Type']=='Signing'))and x['PLAYER_SLUG']]
    # Reuse accepted event complements, not feed absence: these three early
    # releases were positively recovered from official original team bodies.
    accepted_orl=read('research/ORLANDO_REGISTRATION_LEGAL_DOMAIN_2026_10_05.json')
    accepted_dc=read('research/DEN_CLE_REGISTRATION_LEGAL_DOMAIN_2026_10_05.json')
    if accepted_orl != orl_domain.build(TEMP) or accepted_dc != den_cle_domain.build(TEMP):
        raise ValueError('accepted registration witness reconstruction mismatch')
    coverage=read('research/ORLANDO_PUBLIC_EVENT_COVERAGE_2026_10_05.json')
    supplemental=[e for e in coverage['events']if e['event']=='RELEASE_TEN_DAY']
    expected_release=[('2021-04-13','Devin Cannady','hall_apr13'),('2021-04-27','Robert Franks','wagner_apr27'),('2021-05-02','Donta Hall','brazdeikis_may2')]
    if [(e['date'],e['player'],e['original_source_id'])for e in supplemental]!=expected_release:
        raise ValueError('original ORL release semantic source changed')
    for e in supplemental:
        events.append(dict(id='ORL_COMPLEMENT:'+e['original_source_id'],date=e['date'],type='Waive',team='ORL',player=e['player'],origin=None,contract_class='STANDARD',ten_day=False,source_row=None,source_row_sha256=None,source_path='research/ORLANDO_PUBLIC_EVENT_COVERAGE_2026_10_05.json',source_event=e,classification='PRESERVED_POSITIVE_ORIGINAL_TEAM_RELEASE',actual_execution_certified=False,omitted_by_approved_direction=False))
    events.sort(key=lambda e:(e['date'],0 if e['type']=='Waive'else 1,e['source_row']if e['source_row']is not None else -1))
    regular_dates={t:sorted({g['date']for g in games if g['phase']=='REGULAR'and g['team']==t})for t in roster}
    tw=json.loads((TEMP/RAW['tw2021'][0]).read_text(encoding='utf-8-sig'))
    if 'playoffs'not in tw['html'].lower()or'two-way'not in tw['html'].lower():raise ValueError('2021TW report semantic scope changed')
    mem_text=PdfReader(TEMP/RAW['mem_hardship_guide'][0]).pages[135].extract_text()
    if digest(mem_text.encode())!='0fc3ce8b5330464b7304a96b377fef7f11a1ade62955b0bcca779e37c9a9a4ed':
        raise ValueError('MEM original hardship guide page changed')
    if 'hardship roster rules on Jan. 4, 2021'not in mem_text or'Contract expired on Jan. 14, 2021'not in mem_text:
        raise ValueError('MEM named hardship positive statement changed')
    states={};bindings=[];issues=defaultdict(list);cursor=0;executed=[];expiry_events=[];checked_dates=set()
    def gap(kind,team,day,player=None,detail=None):
        key=':'.join(str(x)for x in(kind,team,player or''))
        issues[key].append({'date':day,'player':player,'detail':detail})
        return key
    def state(t):
        players=[{'player':v['name'],'contract_class':v['class'],'source_origin':v['origin'],'working_expiry_inclusive':v['expiry'],'medical_status':None}for k,v in sorted(roster[t].items())]
        key=t+':'+digest(json.dumps(players,sort_keys=True,ensure_ascii=False).encode())[:16]
        states[key]={'team':t,'players':players,'standard_count':sum(v['contract_class']=='STANDARD'for v in players),'two_way_count':sum(v['contract_class']=='TWO_WAY'for v in players),'actual_registration_certified':False}
        return key
    initial_state_ids={t:state(t)for t in sorted(roster)}
    for g in games:
        day=g['date']
        for t,v in roster.items():
            for k,x in list(v.items()):
                if x['expiry']and x['expiry']<day:
                    before=state(t);del v[k]
                    expiry_events.append({'team':t,'player':x['name'],'date_model':(date.fromisoformat(x['expiry'])+timedelta(days=1)).isoformat(),
                        'observed_at_next_league_model_date':day,'classification':'PROVISIONAL_WORKING_INTERVAL_END_NOT_ACTUAL_TERMINATION_CERTIFICATE',
                        'source_origin':x['origin'],'before_state_id':before,'after_state_id':state(t),'salary_erased':False})
        while cursor<len(events)and events[cursor]['date']<=day:
            e=events[cursor];cursor+=1;executed.append(e)
            e['before_state_ids']={o:state(o)for o in {e['team'],e['origin']}if o}
            if e['omitted_by_approved_direction']:
                e['after_state_ids']=deepcopy(e['before_state_ids']);continue
            t=e['team'];k=norm(e['player'])
            if e['type']=='Waive':roster[t].pop(k,None)
            elif e['type']=='Trade':
                owners=[o for o in roster if k in roster[o]]
                if owners==[t]:
                    e['application']='ALREADY_SAME_RECEIVING_TEAM_DUPLICATE_PUBLIC_ANNOUNCEMENT_NO_NEW_ASSIGNMENT'
                    e['after_state_ids']=deepcopy(e['before_state_ids'])
                    continue
                # Jan14 vs Jan16 feed rows describe preliminary/full four-team
                # arrivals, including LeVert's intermediate HOU assignment.
                # Unique current owner is removed once; the original reported
                # origin/date remain visible. No bonus is charged/zeroed here.
                if len(owners)==1:
                    e['before_state_ids'][owners[0]]=state(owners[0])
                    old=roster[owners[0]].pop(k)
                    e['application']='PUBLIC_UNIQUE_OWNER_TO_REPORTED_RECEIVER'
                    e['working_previous_team']=owners[0]
                    e['original_from_differs_from_intermediate']=owners[0]!=e['origin']
                else:
                    old=roster[e['origin']].pop(k,None)
                    gap('PUBLIC_TRADE_ORIGIN_MEMBERSHIP_GAP',e['origin'],e['date'],e['player'],e['id'])
                roster[t][k]={'name':e['player'],'class':old['class']if old else e['contract_class'],'origin':e['id'],'expiry':None}
            else:
                roster[t][k]={'name':e['player'],'class':e['contract_class'],'origin':e['id'],'expiry':expiry_for(e,regular_dates)}
            e['after_state_ids']={o:state(o)for o in e['before_state_ids']}
        if day not in checked_dates:
            registered=defaultdict(list)
            for o,rv in roster.items():
                for person in rv:registered[person].append(o)
            for person,owners in registered.items():
                if len(owners)>1:gap('SIMULTANEOUS_CANDIDATE_ROSTER_OWNERSHIP_GAP',','.join(sorted(owners)),day,person)
            checked_dates.add(day)
        t=g['team'];sid=state(t);v=roster[t];unresolved=[]
        for n,s in g['seconds'].items():
            if s>0 and norm(n)not in v:unresolved.append(gap('POSITIVE_PLAYER_NOT_IN_PUBLIC_WORKING_ROSTER',t,day,n,g['event_id']))
            if s>0 and n in g['absent']:raise ValueError(('modeled absent receives positive',g['event_id'],n))
            # The recovered March11 original report expressly covers 2020-21
            # postseason eligibility. Do not import another season's TW ban.
        for n in g['starters']:
            if g['seconds'].get(n,0)<=0:raise ValueError('source starter nonpositive')
        hardship=None
        if t=='MEM'and'2021-01-04'<=day<'2021-01-14'and norm('Tim Frazier')in v:
            hardship='MEM_FRAZIER_JAN04_POSITIVE_HARDSHIP_CANDIDATE_CARRY'
        if states[sid]['standard_count']>15 and not(hardship and states[sid]['standard_count']==16):
            unresolved.append(gap('STANDARD_COUNT_ABOVE15_NO_POSITIVE_EXCEPTION',t,day,detail=states[sid]['standard_count']))
        if states[sid]['two_way_count']>2:unresolved.append(gap('TW_COUNT_ABOVE2',t,day,detail=states[sid]['two_way_count']))
        if t=='GSW':unresolved.append('GSW_HUTCHISON_OPERATION_UNSELECTED')
        if t=='WAS':unresolved.append('WAS_BONGA_RIGHTS_TO_STANDARD_UNSELECTED')
        if t=='CHA':unresolved.append('CHA_RILLER_UDFA_CONTRACT_CARRY_UNSELECTED')
        bindings.append({'phase':g['phase'],'event_id':g['event_id'],'date':day,'team':t,'state_id':sid,
          'minute_source':{'path':g['source'],'pointer':g['pointer']},
          'positive_membership_covered':not any(x.startswith('POSITIVE_')for x in unresolved),
          'unresolved_gap_ids':sorted(set(unresolved)),
          'modeled_absent_source_names':g['absent'],'working_named_hardship_family':hardship})
    gaps=[{'id':key,'kind':key.split(':')[0],'occurrences':len(rows),'first_date':min(r['date']for r in rows),'last_date':max(r['date']for r in rows),'observations':rows}for key,rows in sorted(issues.items())]
    for key,description in [('GSW_HUTCHISON_OPERATION_UNSELECTED','G1/G2/G3 original-direction implementation remains unselected; historical GSW roster is only a candidate.'),('WAS_BONGA_RIGHTS_TO_STANDARD_UNSELECTED','Bonga44 rights/stash vs current positive NBA family needs a finite standard-contract bridge; no automatic removal.'),('WAS_HOMESLEY_SIGNING_UNSELECTED','May15 Homesley signing and retained Brown/Trent require a selected roster implementation; do not automatically omit.'),('CHA_RILLER_UDFA_CONTRACT_CARRY_UNSELECTED','Approved Riller UDFA status does not select original Charlotte two-way contract.')]:
        gaps.append({'id':key,'kind':'NAMED_CANDIDATE_EXECUTION_GAP','description':description,'actual_financial_or_destination_selection':None})
    covered=sum(b['positive_membership_covered']for b in bindings)
    return {'schema_version':1,'status':'FULL_1174_SCHEDULE_PUBLIC_ROSTER_BRIDGE_AUDITED_NAMED_EXECUTION_GAPS_HOLD',
      'baseline_main':'75a1d526e78ef53fbf3e72fa7cad8899a57debf9','source_hash_method':'UTF8_BOM_STRIPPED_CRLF_CR_NORMALIZED_LF',
      'source_sha256':{p:sha(p)for p in SOURCES},'raw_sources':raw,'authority':AUTH,
      'opening_source_locators':locators,'historical_opening':historical,'opening_working_delta':initial_deltas,
      'working_initial_rosters':initial,'initial_state_ids':initial_state_ids,'dated_events':executed,'working_interval_end_events':expiry_events,
      'roster_states':states,'team_game_bindings':bindings,'named_gaps':gaps,
      'summary':{'games':1174,'team_games':len(bindings),'teams':30,'public_player_events':sum(e['source_row']is not None for e in executed),'accepted_original_release_complements':len(supplemental),'distinct_roster_states':len(states),
        'positive_membership_covered_team_games':covered,'positive_membership_gap_team_games':len(bindings)-covered,
        'no_named_membership_or_slot_gap_team_games':sum(not b['unresolved_gap_ids']for b in bindings),
        'provisional_10day_interval_ends':len(expiry_events),'all30_candidate_owner_checks_dates':len(checked_dates),
        'observed_gap_kinds':dict(Counter(x['kind']for x in gaps))},
      'event_policy':{'public_feed_midnight_is_execution_clock':False,'same_date_events_applied_before_working_game':'RELEASES_BEFORE_ACQUISITIONS_EXPLICIT_WORKING_CANDIDATE_NOT_ACTUAL_ORDER_CERTIFICATE',
        'ten_day_interval':'2017II9(a): longer of10days/three regular scheduled games, provisional date-only working interval; 2020 season-specific amendments/actual start clock not certified.',
        'ten_day_expiry_inclusive_model':True,'ten_day_exact_2020_applicability_certified':False,
        'waiver_removes_roster_not_salary':True,'positive_health_and_minutes_unchanged':True,'zero_means_medical_absence':False,
        'positive_health':'EXISTING_AUTHOR_MODELED_MINUTE_AVAILABILITY_PRESERVED',
        'reserve_zero_health':None,'actual_registration_certified':False,
        'TW_2021_postseason_source':'TW_20210311_PRIMARY_REPORT in research/DEN_LAL_2021_COACH_PLAN_SOURCE_BRIDGE.json; original report, not full amended CBA',
        'name_aliases':{'Enes Freedom':'Enes Kanter','Xavier Tillman Sr.':'Xavier Tillman','Cam Reynolds':'Cameron Reynolds','Nicolas Claxton':'Nic Claxton','KJ Martin':'Kenyon Martin Jr.'},
        'JTA_boundary_dates':{'opening_PDF':'2020-12-22 row not printed','feed':'2020-12-21','existing_official_guide':'2020-12-22','exact_time':None},
        'unknown_private_event_absence_required':False,'unsupported_contract_or_waiver_selection_added':False},
      'scope':{'complete_schedule_index':True,'complete_supplied_public_30team_candidate_reconstruction':True,'all_positive_membership_complete':covered==2348,
        'complete_financial_execution':False,'working_roster_execution_complete':False,'actual_registration_certified':False,
        'medical_certified':False,'A1_A2_A3_promoted':False,'K_closed':[],'season_selected':False,'manuscript_allowed':False,
        'new_author_locked_choice':False,'new_source_collection':True},
      'upstream_validation':['regular validate + full source reconstruction','L2 full source reconstruction','playoff full source reconstruction','accepted ORL and DEN-CLE registration witness full reconstruction'],
      'named_hardship_source_and_working_application':{'MEM_FRAZIER_JAN04':{'source_raw_id':'mem_hardship_guide','pdf_page':136,'printed_page':134,'page_text_sha256':digest(mem_text.encode()),'positive_original_fact':'Team guide states Frazier January4 signing under hardship roster rules, January14 expiry.','contemporaneous_original_body_observation':{'url':'https://web.archive.org/web/20210106234526/https://www.nba.com/grizzlies/news/memphis-grizzlies-sign-tim-frazier-210104','date':'2021-01-04','locator':'heading134/date138/paragraph140 in directly read web extraction','raw_sha256':None,'original_body_read':True},'working_application':'Preserve this named 2021 hardship implementation family under existing delegated health/season design; not source-date count illegality or actual receipt/medical certification.','working_inclusive_dates':['2021-01-04','2021-01-13'],'actual_medical_prerequisites_certified':False,'reserve_zero_diagnosis':None,'actual_league_approval_certified':False}},
      'accepted_registration_reuse':{'ORL_release_complements':[list(x)for x in expected_release],'scope':'Positive original release events and season-specific legal domain reused; no actual receipt/medical certificate or private absence requirement added','source_rules':accepted_orl['contemporaneous_public_rules']} ,
      'CBA_locator':{'article':'II9(a)','pdf_page':69,'printed_page':47,'text_sha256':digest(text.encode())}}

def validate(data,expected=None):
    expected=build()if expected is None else expected
    if data!=expected:raise ValueError('roster bridge differs from source reconstruction/scope')

def markdown(d):
    s=d['summary'];lines=['# 2020–21 전체 날짜별 등록 실행 연결 감사','',
      '**전체 일정은 연결했으며 명단 실행 공백은 HOLD다.** 원NBA 등록 인증·새 재정 선택·최종시즌 확정이 아니다.',
      '',f"- 기존1174경기/2348팀/30팀 분·승패·건강 입력을 참조한다. 벡터나 결과 재계산0.",
      f"- 개막 원PDF4쪽+고정NBA 이동 feed의 선수 사건{s['public_player_events']}개, 명단상태{s['distinct_roster_states']}개와 기존 승인 원본문 해제 보완{s['accepted_original_release_complements']}건을 재현했다.",
      f"- 기존 양수분 선수 소속이 포함되는 팀경기{s['positive_membership_covered_team_games']}, 빠지는 팀경기{s['positive_membership_gap_team_games']}.",
      '- 소속 포함은 금융·수락·정확 리그접수 증명이 아니다. 명단 초과/변경 경로가 남으면 실행 완료로 세지 않는다. 원feed 날짜만으로 임시 초과나 hardship를 실제위법으로 판정하지 않는다.',
      '- 승인 드래프트 착지와F1–F5 변경만 적용했다. Bonga/Homesley/Hutchison/Riller를 임의삭제하거나 계약하지 않는다.',
      '', '| 남은 유한 관측 | 관측수 | 최초 | 마지막 |','|---|---:|---|---|']
    for x in d['named_gaps']:
        lines.append(f"| {x['id']} | {x.get('occurrences','—')} | {x.get('first_date','—')} | {x.get('last_date','—')} |")
    lines+=['','## 자료·모델·미인증 구분','',
      '개막명단의 inactive 비별표 선수는 standard이며 별표 선수만 two-way다. 실제 보장 급여는 이 파일에서 선택하지 않는다.',
      '원feed의00:00은 시각증거가 아니다. 같은 날짜 사건을 해당 작업 경기 전 적용하는 후보를 명시하여, 양수분과 충돌한 날짜를 감춘 채 실제 소속으로 인증하지 않는다.',
      'ORL/CLE/DEN의 이미 검문된 등록 증인을 재구성하고 원feed에 빠진 ORL 조기해제3건을 보존했다. 사건일 당일 해제를 취득보다 앞에 두는 작업 순서다. 그 밖의10일계약은 2017 CBA II9(a), PDF69/인쇄47의10일 또는3경기 중 긴 기간으로 잠정 끝을 계산했다. 2020수정 적용성·실제 시작시각은 미인증이며 그 한계를 exact 등록 완료로 승격하지 않는다.',
      '양수분은 기존 위임 건강·코치 모델이고 예비0분의 의료 상태는null이다. 방출·만료는 선수 자리만 제거하며 급여잔액0이라는 뜻이 아니다.',
      '가상 사건을 보존할 수 있다는 인과 모형과 실제 계약·당일 접수의 사실 인증을 구별한다. 모든 비공개 해제부재나 실제 의료기록을 새필수조건으로 요구하지 않는다.',
      '', '## 확인된 명명 예외와 작업 적용', '',
      'Memphis 구단 2022–23 가이드 PDF136/인쇄134는 Tim Frazier의2021-01-04 hardship 계약과1/14만료를 직접 명시한다. 당시 구단1/4원발표의보존본문도읽었다. 이명명된2021예외를작업family로보존해해당5경기일의일반16명을단순위법/미공표부재게이트로취급하지않는다. 원실제의료조건·리그접수·예비0진단인증은false다.',
      '', '## 다음 실제 실행','',
      'named_gaps의 각 선수/날짜에 이미 존재하는 구단 원문·계약기간·승인델타를 연결한다. 공백은 새 임의계약으로 채우지 않고 원자료의 누락/날짜 차이와 미선택 대체 경로를 구분한다.',
      '전체membership와자리/법적family 실행이 검문된 뒤 S2 closing_witness를 별도 판정한다. 이번파일A/K·원장·시즌승격0, v0.30 PARTIAL·설계/원고 CLOSED·원고0.',
      '', '[기계 입력](NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json)','']
    return '\n'.join(lines)

def self_test(expected):
    tests=[('actual_registration',lambda x:x['scope'].__setitem__('actual_registration_certified',True)),
      ('reserve_injury',lambda x:x['event_policy'].__setitem__('reserve_zero_health','INJURED')),
      ('drop_game',lambda x:x['team_game_bindings'].pop()),
      ('change_member_same_count',lambda x:x['roster_states'][next(iter(x['roster_states']))]['players'][0].__setitem__('player','Unsupported Player')),
      ('false_complete',lambda x:x['scope'].__setitem__('working_roster_execution_complete',True)),
      ('erase_gap',lambda x:x['named_gaps'].pop()),
      ('fake_raw_hash',lambda x:x['raw_sources']['movement'].__setitem__('raw_sha256','0'*64))]
    for label,mutate in tests:
        x=deepcopy(expected);mutate(x)
        try:validate(x,expected)
        except ValueError:continue
        raise ValueError('false pass '+label)
    return len(tests)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args()
    d=build();m=markdown(d)
    if a.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(m,encoding='utf-8')
    if a.check:
        validate(read(OUT),d)
        if (ROOT/MD).read_text(encoding='utf-8-sig')!=m:raise ValueError('MD stale')
    print(json.dumps({'current':a.check,'summary':d['summary'],'negative_tests':self_test(d)if a.self_test else 0},ensure_ascii=False))
