"""Select a named NYK keeper/rookie family and its four CHI regulation models.

Prices are lawful component functions, not fabricated historical dollars. No
ancestor constructors or whole private ledger certification are used.
"""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from datetime import date,timedelta
from unittest.mock import patch
import argparse,csv,hashlib,io,json
import fitz
from bs4 import BeautifulSoup
import build_chicago_detroit_2021_two_date_selected_bpm_results as det

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_nyk_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_NEW_YORK_2021_22_SELECTED_KEEPER_RESULTS.json'
MD=OUT[:-5]+'.md'
BASELINE='f4e1ec1ecdf93509e8e7868f800ad04d8aafcafa'
CAPACITY='simulation/NBA_2021_22_COMMON_26_OPPONENT_CAPACITY.json'
CHI='simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json'
ROSTER='simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json'
DRAFT='simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json'
HEALTH='simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json'
AUTH='canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json'
PINS={CAPACITY:'a0ecb8e362e51344ca2cc2de53ff0713901bc4d50432a5efef621641fd0c00b7',
 CHI:'73d51b630e9c9d4ec31b7e3952906165589bd8c49a48bb07c79bdc9ad02e8fca',
 ROSTER:'cfa2f49bb82baa49b2298d90c97cd7fd8075e91380424d40bfd44772d8228a2b',
 DRAFT:'f8c78e99cce1b02a051c94339b550fdb52205d3988db8bbe69b780559c3bc306',
 HEALTH:'274a35e163c7f6fd7f0d3e5494b3c46753aaf9900036676be935f17a9d538c32',
 AUTH:'51b24c8a6bc1eb703568adced46b3ffa15845e85e8da10da1242bddf941df960',
 det.CAL:'c59ea19a5515d64ed03cae8e0481847b6572d4087bbcefef15896bb7a2489183',
 det.LEAGUE:'92869bc987896a4172c5e54e3684d2604c5c24d828e9bcf3cc27af30ebc83644',
 det.BPM:'1d1455f7f4ddd73ef46e3ce16752b558c392ed2d284434acd295ca6659e937ef',
 det.OUT:'66c1c862a179648aa72dd81ff13a07345b36889043995ecb583ae57019618c80',
 det.SELF:'ebe05a0c9b886cee62cf00c82ba0c69b72778e24ca621d1028f3e58544524e6e'}
CBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
FEED=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-nba-player-movement-2026-10-04.json')
FEED_SHA='3d9d7a6dd7ccd39ddfdd1799a26ef9901b44682d85a26f05239b468a8ae92e3a'
RFA=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-nop-rfa-20261007/NBA2021_RFA.html')
RFA_SHA='c3791cc30b1a1eec3422778868a56a24b702fe2c42ce9ffe9cc2a42719b33611'
TEMP=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-nyk-keeper-20261007')
OBS_SHA='c89781a4303af04da8844c8807f8b1709f08ed6781e43ba0a12c34a40d52bef4'
FAILED_SHA='61b08b7f1df727c1d701d282a31b28100b22f81f526c368ecfe1fa8a8253e96c'
IDS=('0022100067','0022100250','0022100328','0022101126')
RETAINED=('Immanuel Quickley','Julius Randle','Kevin Knox II','Mitchell Robinson','Obi Toppin','RJ Barrett')
EARLY=('Derrick Rose','Reggie Bullock')
NONBIRD=('Alec Burks','Elfrid Payton','Nerlens Noel','Taj Gibson')
REMOVE=('Norvel Pelle','Luca Vildoza')
ROOKIES=((20,'Quentin Grimes'),(23,'Ayo Dosunmu'))
SECOND=((32,'Rokas Jokubaitis'),(57,'Balsa Koprivica'))
TW={'Jared Harper':2,'Theo Pinson':3}
ROLE_MINUTES={
 'PG':{'Elfrid Payton':20,'Derrick Rose':24,'Immanuel Quickley':4},
 'SG':{'RJ Barrett':14,'Immanuel Quickley':18,'Alec Burks':16},
 'SF':{'RJ Barrett':18,'Reggie Bullock':26,'Alec Burks':4},
 'PF':{'Julius Randle':34,'Obi Toppin':14},
 'C':{'Mitchell Robinson':28,'Nerlens Noel':14,'Taj Gibson':6}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
ROLE_SEQUENCE_SHA='93b7ec555bd80a2d5b69bc98e75aa948e7180dcaddab1e5e4d117963c859b967'
STARTERS={'PG':'Elfrid Payton','SG':'RJ Barrett','SF':'Reggie Bullock','PF':'Julius Randle','C':'Mitchell Robinson'}
PRICE_RULES={
 'EARLY_BIRD':{'article':'VII6b3','nonoption_seasons':2,'first_base_floor':'max(legalMin(YOS,2021),signed2021MinimumYear2(YOS+1))',
  'first_base_ceiling':'min(II7maximum,max(7/4*priorRegularSalary,21/20*priorAveragePlayerSalary))',
  'second_base':'first_base','new_likely':0,'new_unlikely':0,'new_allocated_bonus':0},
 'NON_BIRD':{'article':'VII6b2','nonoption_seasons':2,'first_base_floor':'max(legalMin(YOS,2021),signed2021MinimumYear2(YOS+1))',
  'first_base_ceiling':'min(II7maximum,max(6/5*priorRegularSalary,6/5*currentLegalMinimum))',
  'second_base':'first_base','new_likely':0,'new_unlikely':0,'new_allocated_bonus':0,
  'if_early_eligible':'VII4d2 written limited renunciation of Early exception only; deemed NonQualifying. No full player renunciation.'}}
PRICE_FIXED=deepcopy(PRICE_RULES)
FRANK_QO_FIXED={'ordinary':'originalFourthYearSalaryComponents*(1+applicablePick8_QOincrease)',
 'nonstarter':'lesser original package vs pick15_120percent_scale_QO_base_only','anchor_rank':15,'anchor_fraction':'6/5','anchor_bonuses':0}
POLICY={'named_route':'NYK_KEEPERS_WITH_TWO_EXISTING_DB1_ROOKIE_UPCS',
 'Frank_QO_issued_fictionally':'2021-07-31','QO_accepted_fictionally_ET':'2021-08-06T12:02:00',
 'new_UPCs_and_TWs_start_ET':'2021-08-06T12:02:00_ORDERED',
 'new_NTMLE_BAE_incoming_SandT':False,'new_counterparty_trade':False,
 'actual_dollars_or_receipts_selected':False,'old_waived_protection_deleted':False,
 'positive11_NYK_operationally_available_at_four_dates':True,
 'all_unused_zero_minute_clinical_status':None,'new_canonical_author_lock':False}
POLICY_FIXED=deepcopy(POLICY)

def need(ok,msg):
    if not ok:raise ValueError(msg)
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def physical(root,p):
    t=text(root/p);return json.loads(t)if p.endswith('.json')else list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else t
def sources(root):return {p:physical(root,p)for p in PINS}

def support():
    need(hashlib.sha256(CBA.read_bytes()).hexdigest()==CBA_SHA,'CBA raw changed')
    d=fitz.open(CBA);pages=(26,29,30,31,54,55,58,71,72,74,75,208,209,210,212,222,223,224,227,228,232,233,240,241,292,294,303,309,310,311,315,317,318,561)
    texts={i:d[i-1].get_text().replace('\r\n','\n').replace('\r','\n')for i in pages}
    flat=lambda i:' '.join(texts[i].split())
    need('two (2) preceding Seasons'in flat(26)and 'by means of trade'in flat(26),'EarlyBird history rule absent')
    need('one hundred twenty percent (120%)'in flat(223)and 'at least two (2) Seasons'in flat(223)and 'seventy-five percent (175%)'in flat(224),'Veteran exception price function absent')
    need('deemed a Non-Qualifying Veteran Free Agent'in flat(209),'Limited EarlyBird renunciation rule absent')
    need('Rookie Exception'in flat(232)and 'one hundred twenty percent'in flat(294),'RSC route absent')
    need('first Season covered by the player’s Contract'in flat(55)and 'for each Season of the Contract'in flat(55),'Signed-year minimum scale rule absent')
    need('may not include any Option Year'in flat(74)and 'more than two (2) Two-Way Players'in flat(74)and 'four (4) or more'in flat(74),'TW term/roster/service rule absent')
    need('more than three (3) Salary Cap Years with the same NBA Team'in flat(75),'Same-team TW year ceiling absent')
    # The common minimum scale multiplier cancels. All six veterans are at
    # least seven-YOS in the admitted history; Year2 after advancing service
    # is strictly below 120% current minimum, leaving a nonempty flat-base
    # interval without choosing the minimum endpoint as their actual price.
    minimum_pairs=((7,1974159,2211794),(8,2106470,2222803),(9,2116955,2445085),(10,2328652,2445085))
    for _,first,second in minimum_pairs:
        need(f'{first:,}'in texts[561]and f'{second:,}'in texts[561]and Fraction(second,first)<Fraction(6,5),'Two-season minimum feasibility source changed')
    need(hashlib.sha256(FEED.read_bytes()).hexdigest()==FEED_SHA,'Frozen movement raw changed')
    rows=json.loads(FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    groups=('Signing 1019175','Trade 2020056','Signing 1033185','Signing 1033366','Signing 1033534','Signing 1035618','Waive 1032225','Waive 1032226','Signing 1039869','Signing 1039459','Waive 1041603','Waive 1043626','Signing 1039777','Signing 1033535','Signing 1033247','AwardedOnWaivers 1032013','AwardedOnWaivers 1030944')
    observed=[x for x in rows if x['TEAM_ID']==1610612752 and x['GroupSort']in groups]
    need({x['GroupSort']for x in observed}==set(groups),'Named original NYK event source absent')
    need(hashlib.sha256(RFA.read_bytes()).hexdigest()==RFA_SHA,'RFA raw changed')
    j=json.loads(BeautifulSoup(RFA.read_text(encoding='utf-8'),'html.parser').find('script',id='__NEXT_DATA__').string)
    body=BeautifulSoup(j['props']['pageProps']['article']['contentText'],'html.parser').get_text(' ',strip=True)
    need('Frank Ntilikina (NYK)'in body.split('Not issued (unrestricted free agents)')[1],'Original Frank no-QO classification absent')
    unrestricted=body.split('Unrestricted')[1].split('Qualifying offers')[0]
    need('Jared Harper (NYK)'in unrestricted and 'Theo Pinson (NYK)'in unrestricted,'Original TW FA classification absent')
    need(hashlib.sha256((TEMP/'web_observed_facts.json').read_bytes()).hexdigest()==OBS_SHA,'Web observation projection changed')
    obs=json.loads((TEMP/'web_observed_facts.json').read_text(encoding='utf-8'))
    need(hashlib.sha256((TEMP/'metadata.json').read_bytes()).hexdigest()==FAILED_SHA,'Failed-fetch record changed')
    failures=json.loads((TEMP/'metadata.json').read_text(encoding='utf-8'))
    for x in failures:need(hashlib.sha256(Path(x['cache_path']).read_bytes()).hexdigest()==x['raw_sha256']and x['HTTP']==403,'Failed body promoted or changed')
    return {'CBA_raw':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(CBA),'raw_sha256':CBA_SHA,
      'normalized_fitz_page_text_sha256':{str(i):hashlib.sha256(t.encode()).hexdigest()for i,t in texts.items()}},
      'frozen_movement_raw':{'cache_path':str(FEED),'raw_sha256':FEED_SHA,'named_original_events_not_automatically_executed':observed},
      'TW_eligibility_family':{'new_season':'2021-22','same_NYK_TW_cap_years_including_new':['2019-20','2020-21','2021-22'],
        'same_team_years_maximum':3,'one_year_no_option_before_January15':True,
        'original_waiver_claims_and_2020_2021_TW_signings_are_provenance_not_new_receipts':True,
        '2021_operatively_amended_cash_function_not_original_45day_or_50000_protection_imported':True,
        'TW_players_not_nominated_for_NBA_active_service_in_four_selected_plans':True},
      'NBA_RFA':{'url':'https://www.nba.com/news/2021-free-agency-options-and-qualifying-offers','cache_path':str(RFA),'raw_sha256':RFA_SHA,
        'original_Frank_QO_not_issued':True,'original_Harper_Pinson_TW_unrestricted':True,'fictional_2021_tender_not_historical_certificate':True},
      'web_observation_projection':{'cache_path':str(TEMP/'web_observed_facts.json'),'raw_capture_sha256':OBS_SHA,'projection':obs,'original_HTTP_body_certified':False},
      'two_season_flat_minimum_nonempty_support':{'ExhibitC_PDF561_pairs':[list(x)for x in minimum_pairs],
        'ratio_below_120_percent_with_large_rounding_margin':True,'common_signed_year_scale_factor_cancels':True,
        'q120percent_minimum_is_existence_example_not_selected_price':True,'admitted_veteran_YOS_at_least7':True},
      'failed_direct_HTTP':failures,'failed_bodies_counted_as_primary_content':0}

def contracts():
    out=[{'player':p,'route':'VII6a_EXISTING_LAWFUL_CARRY','new_UPC':False,'valid_current_term_to_2022_03_28':True,
      'original_salary_protection_allocated_bonus_likely_unlikely_Γ_preserved':True,'actual_dollars':None,'actual_receipt':None}for p in RETAINED]
    for p in EARLY+NONBIRD:
        cls='EARLY_BIRD'if p in EARLY else'NON_BIRD'
        out.append({'player':p,'route':'VII6b_'+cls,'new_UPC':True,'price_function':deepcopy(PRICE_RULES[cls]),
          'q_is_consensual_parameter_in_legal_interval_not_minimum_selected':True,'valid_current_term_to_2022_03_28':True,
          'actual_dollars':None,'actual_receipt':None})
    out.append({'player':'Frank Ntilikina','route':'VII6b_VALID_OWN_ORDINARY_RSC_QO','new_UPC':True,'original_draft_class':2017,'original_pick':8,
      'QO_function':{'ordinary':'originalFourthYearSalaryComponents*(1+applicablePick8_QOincrease)',
        'nonstarter':'lesser original package vs pick15_120percent_scale_QO_base_only','anchor_rank':15,'anchor_fraction':'6/5','anchor_bonuses':0},
      'timely_team_signed_delivery':'2021-07-31','accepted_ET':'2021-08-06T12:02:00','unwithdrawn':True,
      'valid_current_term_to_2022_03_28':True,'actual_dollars':None,'actual_receipt':None})
    for pick,p in ROOKIES:
        out.append({'player':p,'route':'VII6h_VIII1_ROOKIE_SCALE','new_UPC':True,'pick':pick,'holder':'NYK',
          'component_scale_interval':['4/5','6/5'],'minimum_base_protection_fraction':'4/5','salary_plus_unlikely_ceiling':'6/5',
          'guaranteed_seasons':2,'option_seasons':2,'valid_first_RT_inside_operative_W21_before_UPC':True,
          'valid_current_term_to_2022_03_28':True,'actual_dollars':None,'actual_receipt':None})
    return out

def assert_contracts(rows):
    need(PRICE_RULES==PRICE_FIXED and POLICY==POLICY_FIXED,'Fixed lawful family policy changed')
    need(len(rows)==15 and len({x['player']for x in rows})==15,'Contract family membership count changed')
    need({x['player']for x in rows}==set(RETAINED+EARLY+NONBIRD+('Frank Ntilikina',)+tuple(p for _,p in ROOKIES)),'Contract family identity changed')
    for x in rows:
        p=x['player'];need(x['actual_dollars']is None and x['actual_receipt']is None and x['valid_current_term_to_2022_03_28'],'Actual receipt or current term changed')
        if p in RETAINED:need(x['route']=='VII6a_EXISTING_LAWFUL_CARRY'and not x['new_UPC']and x['original_salary_protection_allocated_bonus_likely_unlikely_Γ_preserved'],'Inherited Γ deleted')
        elif p in EARLY+NONBIRD:
            cls='EARLY_BIRD'if p in EARLY else'NON_BIRD';need(x['route']=='VII6b_'+cls and x['price_function']==PRICE_FIXED[cls]and x['q_is_consensual_parameter_in_legal_interval_not_minimum_selected'],'Returned veteran price/class function differs from source')
        elif p=='Frank Ntilikina':need(x['route']=='VII6b_VALID_OWN_ORDINARY_RSC_QO'and x['original_pick']==8 and x['original_draft_class']==2017 and x['QO_function']==FRANK_QO_FIXED and x['timely_team_signed_delivery']=='2021-07-31'and x['accepted_ET']=='2021-08-06T12:02:00'and x['unwithdrawn'],'Frank QO authority/calendar changed')
        else:
            pick=next(n for n,v in ROOKIES if v==p);need(x['route']=='VII6h_VIII1_ROOKIE_SCALE'and x['pick']==pick and x['holder']=='NYK'and x['component_scale_interval']==['4/5','6/5']and x['guaranteed_seasons']==2 and x['option_seasons']==2 and x['valid_first_RT_inside_operative_W21_before_UPC'],'Selected rookie contract identity/terms changed')

def paired(c,n):
    ct=[b['positions']for b in c['unordered_regulation_blocks']for _ in range(int(b['minutes']*60))]
    nt=[b['positions']for b in n['blocks']for _ in range(int(b['seconds']))]
    need(len(ct)==len(nt)==2880,'Source regulation clock changed')
    out=[]
    for i,(cp,np)in enumerate(zip(ct,nt)):
        if out and out[-1]['quarter']==i//720+1 and out[-1]['CHI']==cp and out[-1]['NYK']==np:out[-1]['end_second']=i+1;out[-1]['seconds']+=1
        else:out.append({'start_second':i,'end_second':i+1,'seconds':1,'quarter':i//720+1,'CHI':deepcopy(cp),'NYK':deepcopy(np)})
    return out

def assert_pair(c,n,rows):
    expected={'CHI':[tuple(sorted(b['positions'].items()))for b in c['unordered_regulation_blocks']for _ in range(int(b['minutes']*60))],
      'NYK':[tuple(sorted(b['positions'].items()))for b in n['blocks']for _ in range(int(b['seconds']))]}
    sums={t:Counter()for t in expected};end=0
    for r in rows:
        need(r['start_second']==end and r['seconds']==r['end_second']-end>0 and r['quarter']==end//720+1 and r['end_second']<=(end//720+1)*720,'Returned date/quarter clock changed')
        for t in sums:
            pos=r[t];need(set(pos)=={'PG','SG','SF','PF','C'}and len(set(pos.values()))==5,'Five unique roles changed')
            need(all(tuple(sorted(pos.items()))==z for z in expected[t][end:r['end_second']]),'Returned position sequence differs from physical source')
            for p in pos.values():sums[t][p]+=r['seconds']
        end=r['end_second']
    need(end==2880 and all(sum(v.values())==14400 for v in sums.values()),'Full paired regulation budget changed')
    need(dict(sums['CHI'])=={p:int(m*60)for p,m in c['player_minutes'].items()}and dict(sums['NYK'])==n['player_seconds'],'Returned positive budget changed')
    return sums

def role_blocks():
    # Bipartite role/player edge coloring. Each two-minute slot matches all five
    # roles, and every player whose residual degree equals slots left must play.
    rem={r:{p:m//2 for p,m in ps.items()}for r,ps in ROLE_MINUTES.items()};roles=list(rem);out=[]
    for i in range(24):
        if i==0:assignment=deepcopy(STARTERS)
        else:
            totals=Counter()
            for ps in rem.values():totals.update(ps)
            required={p for p,v in totals.items()if v==24-i}
            def find(k,a):
                if k==5:return a if required<=set(a.values())else None
                r=roles[k]
                for p in sorted(rem[r],key=lambda p:(p not in required,-rem[r][p],p)):
                    if rem[r][p]>0 and p not in a.values():
                        found=find(k+1,{**a,r:p})
                        if found:return found
                return None
            assignment=find(0,{})
        need(assignment is not None,'Role capacity matching unavailable')
        for r,p in assignment.items():need(rem[r].get(p,0)>0,'Role residual invalid');rem[r][p]-=1
        out.append({'start_second':120*i,'end_second':120*(i+1),'seconds':120,'positions':assignment})
    need(all(v==0 for ps in rem.values()for v in ps.values()),'Role demand not covered')
    return out

def assert_role_blocks(rows):
    need(hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==ROLE_SEQUENCE_SHA,'Returned chosen role chronology differs from fixed selection')
    need(ROLE_MINUTES==ROLE_FIXED,'Fixed selected role budget changed');sums={r:Counter()for r in ROLE_FIXED};end=0
    for row in rows:
        need(row['start_second']==end and row['end_second']-end==row['seconds']==120,'Role elapsed clock changed')
        pos=row['positions'];need(set(pos)==set(ROLE_FIXED)and len(set(pos.values()))==5,'Role uniqueness lost')
        for r,p in pos.items():need(p in ROLE_FIXED[r],'Source selected role identity changed');sums[r][p]+=120
        end=row['end_second']
    need(end==2880 and rows[0]['positions']==STARTERS,'Clock or usual starters changed')
    need(all(dict(ps)=={p:m*60 for p,m in ROLE_FIXED[r].items()}for r,ps in sums.items()),'Returned selected role/player totals changed')
    return Counter({p:sum(ps[p]for ps in sums.values())for p in set().union(*(set(ps)for ps in sums.values()))})

def build(root=ROOT):
    src=sources(root);need(set(src)==set(PINS),'Source domain changed')
    for p,h in PINS.items():need(sha(root/p)==h and src[p]==physical(root,p),'Returned source differs from pinned physical source: '+p)
    raw=support();n_source=src[CAPACITY]['team_functions']['NYK'];rows=contracts();assert_contracts(rows)
    role=role_blocks();secs=assert_role_blocks(role);n={'blocks':role,'player_seconds':dict(secs)}
    old=src[ROSTER];last=next(x for x in reversed(old['team_game_bindings'])if x['team']=='NYK');state=old['roster_states'][last['state_id']]
    oldstd={x['player']for x in state['players']if x['contract_class']=='STANDARD'}
    need(oldstd==set(n_source['standard_named_continuation_condition_max15']),'S2 seed membership changed')
    standard=sorted(oldstd-set(REMOVE)|{p for _,p in ROOKIES});need(set(standard)=={x['player']for x in rows},'Waiver/rookie roster join changed')
    selected=[x for x in src[DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='NYK']
    need([(x['pick'],x['player'])for x in selected]==[*ROOKIES,*SECOND]and all(x['lawful_PS21_participant_model_selected']for x in selected),'Selected draft entitlement differs from keeper rights')
    active=sorted(set(n['player_seconds'])|{'Quentin Grimes'})
    need(len(set(active))==12 and set(active)<=set(standard)and set(n['player_seconds'])<=set(active),'NYK nomination identity changed')
    inactive=sorted(set(standard)-set(active));need(len(inactive)==3 and 'Ayo Dosunmu'in inactive,'Rookie bench nomination changed')
    names=set(n['player_seconds']);prepared=[]
    health={x['game_id']:x for x in src[HEALTH]['selected_dates']};cal={x['game_id']:x for x in src[det.CAL]}
    need(src[AUTH]['selected']['selected_date_rows']['sha256']==PINS[HEALTH],'Selected CHI health authority changed')
    for gid in IDS:
        g=cal[gid];h=health[gid];need(g['opponent']=='NYK'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Four dated calendar identities changed')
        c=next(v for v in src[CHI]['rows']if v['game_id']==gid and v['state']==h['selected_chicago_state'])
        need(c['player_minutes']==h['selected_regulation_player_minutes'],'CHI selected health/role source differs')
        pr=paired(c,n);secs=assert_pair(c,n,pr);need(set(secs['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        names.update(secs['CHI']);prepared.append((g,h,c,pr,secs))
    rate_names=(names-{'Coby'})|({'Coby White'}if 'Coby'in names else set())
    rates=det.expected_ratings({det.BPM:src[det.BPM]},rate_names)
    if 'Coby'in names:rates['Coby']=rates.pop('Coby White')
    for p in set(src[det.OUT]['player_ratings'])&set(rates):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected BPM productivity changed')
    games=[]
    for g,h,c,pr,secs in prepared:
        impacts={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in secs.items()}
        yesterday=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==yesterday and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in secs}
        home=2 if g['home']=='CHI'else -2;fatigue=Fraction(1,2)*(int(back['NYK'])-int(back['CHI']));margin=impacts['CHI']-impacts['NYK']+home+fatigue;need(margin!=0,'Tie needs separate overtime design')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],
          'selected_NYK_date_nomination':{'standard':standard,'TW':sorted(TW),'active':active,'inactive':inactive,'unavailable':[],
            'positive11_working_availability_selected':True,'zero_minute_clinical_status':None,'actual_NBA_active_or_medical_certificate':False},
          'simultaneous_segments':pr,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in secs.items()},
          'team_weighted_BPM_per100':{t:float(v)for t,v in impacts.items()},'home_effect_CHI_direction_per100':home,
          'back_to_back_model':back,'fatigue_effect_CHI_direction_per100':float(fatigue),'exact_CHI_minus_NYK_impact_fraction':str(margin),
          'CHI_minus_NYK_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'NYK',
          'score':None,'overtime_selection':None,'classification':'DELEGATED_FICTIONAL_REGULATION_WINNER_NOT_ACTUAL_GAME'} )
    teamfeed=json.loads(FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    mid=[x for x in teamfeed if x['TEAM_ID']==1610612752 and '2021-08-07'<x['TRANSACTION_DATE'][:10]<='2022-03-28']
    eventstates=[]
    for x in mid:
        disposition='ORIGINAL_REPORT_NOT_APPLIED_TO_SELECTED_KEEPER_FAMILY'
        if x['PLAYER_SLUG']in('norvel-pelle','luca-vildoza')and x['Transaction_Type']=='Waive':disposition='ORIGINAL_POSITIVE_WAIVER_ANCHOR_SEPARATE_FICTIONAL_WAIVER_SELECTED'
        if x['PLAYER_SLUG']=='kevin-knox-ii'and x['Transaction_Type']=='Trade':disposition='NO_KNOX_ASSIGNMENT_NO_CAM_REDDISH_RETURN_OR_ORIGINAL_CONDITIONAL_PICK_SPEND_IN_MODEL'
        eventstates.append({'GroupSort':x['GroupSort'],'date':x['TRANSACTION_DATE'][:10],'type':x['Transaction_Type'],'player_slug':x['PLAYER_SLUG'],'reported_description':x['TRANSACTION_DESCRIPTION'],'working_disposition':disposition,'actual_execution_or_absence_certified':False})
    return {'id':'CHICAGO_NEW_YORK_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,
      'status':'SELECTED_NAMED_LAWFUL_FAMILY_AND_FOUR_REGULATION_RESULTS_INDEPENDENT_REVIEW_PENDING',
      'source_sha256':{**PINS,SELF:sha(root/SELF)},'hash_convention':'repository BOMstrip+LF; external raw bytes unchanged','primary_support':raw,
      'selected_policy':deepcopy(POLICY),'lawful_live_contract_family':rows,
      'original_class_history_and_selected_price':{'Rose':'2019 DET signing→2021 NYK trade; two preceding contract seasons through trade, I1u; do not assign fullBird3 from older MIN season.',
        'Bullock':'2019 NYK signing plus continued2020–21; I1u two-season original-compatible family.',
        'Burks_Noel':'2020 original NYK first signings support NonQualifying branch.',
        'Payton_Gibson':'2020 waiver/newsign separate from2019 contract. If I1u still gives Early eligibility in a realization, limited VII4d2 notice makes chosen NB route valid; no unsupported assertion waiver alone resets allBird rights.',
      'all_q':'q remains max(currentlegalMin,signed2021Year2legalMin)≤q≤named cap-exception ceiling, bonus-free new2-season flat base, full standard protection and lawful paragraph3 payment/consensualUPC; no exactcent or forcedminimum and no real-market acceptance assertion.',
        'all_prior_Γ':'Past/current obligations and allocated old bonuses preserved in applicable salary-cap years; new UPC bonus0 is a fictional negotiated term, not a claim originalbonuses0.'},
      'dated_registration_family':{'old_S2_STD':sorted(oldstd),'selected_exit_or_nonassignment_waiver':['Norvel Pelle','Luca Vildoza'],
        'waiver_datetime_if_live_ET':'2021-08-06T12:01:30_BEFORE_ROOKIE_UPCs','both_original_current_protected_charges_fully_retained':True,
        'original_waiver_dates_are_positive_sources_not_fictional_receipts':True,
        'Mitchell_Robinson_option':'valid exercise in operative2021 contractual notice window beforeUPCsequence',
        'Barrett_Knox_old_RSC_options':'valid prior operative2020 options preserved; October2021 futureoptions not automatically copied',
        'Randle':'existing2021–22 contract/protection preserved; originalAug2021 futureextension not imported',
        'selected_start_after_valid_expiries_options_exits':{'standard_existing':list(RETAINED),'STD':6,'TW':0},
        'new_UPC_order':[p for _,p in ROOKIES]+list(EARLY+NONBIRD)+['Frank Ntilikina'],
        'final_STD':15,'final_TW':2,'offseason_including_TW_maximum_used':17,'no_future_roster_absence_certified':True},
      'draft_and_TW_family':{'signed_RSCs':[{'pick':n,'player':p,'holder':'NYK'}for n,p in ROOKIES],
        'unsigned2R':[{'pick':n,'player':p,'holder':'NYK','UPC':False,'STD':False,
          'valid_first_RT':'team-signed oneSeason/legalMinYOS0 delivery inside operativeW21, beforeOct15, acceptanceUntilAtLeastOct15; selectedunaccepted',
          'foreign_or_college_newfacts':'X5/X6 reopens; no perpetual rights, actualNonNBAnotice/date/foreignlawcertificate null'}for n,p in SECOND],
        'new_TW_contracts':[{'player':p,'admitted_YOS':y,'YOS_less_than_four':True,'stated_seasons':1,'option':False,'same_NYK_TW_salary_cap_year_count_including_new':3,'new_bonus_deferred_compensation_loan_advance':0,'NBAcash':'2021 applicable TwoWay salary function; not TeamSalary0 compensation0',
          'prior_unaccepted_QO':False,'new_QO_not_issued_family':True,'standard_UPC':False,'actual_receipt':None}for p,y in TW.items()],
        'rookie_development':'RSCs signed and practice/bench eligibility admitted; Grimes0active/Ayo0inactive only these four coach plans, not a career-wide zero-minute lock. Future role changes remain callable input.',
        'future2022_RT_boundary':'Reopen at SubsequentDraft/newnotice; four requested games all before that boundary.'},
      'six_cost_categories':{'live':'Retained6 original current-year salary/protection/allocated/likely/unlikely Γ plus 9 valid newlysignedUPCs; TW actualcash separately, CBA TeamSalary treatment preserved.',
        'waived_former':'Pelle/Vildoza current originalprotectedcharges fully kept; all earlier waived/former salary-year obligations and existingstretch Γ untouched.',
        'FA_holds':'Originalstilloutstanding named/unselected FA claims held until statutory UPC replacement; signed15 oldgenericFAhold not doublecounted; TW no-QO priorFA amount kept untilTW signing; apron distinct.',
        'draft_unsigned':'FirstRSC120% unsignedhold only until signedUPC; two2RT legalminimum/youngfloor retained in applicablenormal/apron. No30+30 unnecessary reserve and nounsignedfutureUPC.',
        'unused_exceptions':'All inherited unusedTPE/MLE/BAE amounts preserved perVII6m2 and statutoryapronadjustments; nofullrenounce or arbitrary0 selected.',
        'incomplete':'max(0,12−lawfulcapcount)*legalYOS0minimum at eachprefix; unrenouncedFA/unsigned1R counts retained, finalSTD15 gives0 bycount.'},
      'cap_admissibility':{'existing6_VII6a':True,'valid_own_Veteran6_VII6b':True,'valid_own_QO1_VII6b':True,'RSC2_VII6h':True,
        'new2021_NTMLE_BAE_incoming_SandT_trigger_count':0,'whole_private_normal_apron_total':None,
        'scope':'Validoriginal Γ with I1 class or explicit limitedEarly→NB action, validtender and playerconsensualq interval; eachNPCUPC fits its namedCBAexception at every family point. No caproom/apron finance assumed from nulltotal.',
        'actual_no_other_trigger_or_private_absence_certified':False},
      'dated_intervening_reported_event_controls':eventstates,
      'four_date_working_contract_interval':'2021-10-28 through2022-03-28: explicitlyselectedretention/validliveUPC dates, nointerveningKnox/Randleextension/Fournier/Kemba/hardshipNPCtransaction adopted; originalreports independently enumerated, not proof ofactualabsence.',
      'selected_NYK_role_blocks':role,'selected_NYK_role_minutes':deepcopy(ROLE_FIXED),
      'role_selection':'Routine coach selection replaces conditional uniform fixture, usual Payton/Barrett/Bullock/Randle/Robinson starters and source-compatible roles; four-date positive11 availability selected, not actual clinical proof.',
      'historical_old_uniform_role_input':{'metadata_path':str(TEMP/'pre_plausible_role_metadata.json'),'current':False},
      'selected_ratings':rates,'selected_games':games,
      'butterfly_handoff':['Payton notPHX, Bullock/Ntilikina notDAL: revise their subsequentNPCfamily before thoseleagueeffects are consumed.',
        'NoKembaNYK buyout/signing copied from selectedOKCAP1; noFournierBOS→NYK SandT/2023pick/cash inherited.',
        'NooriginalNYKdraft19/21/58 transactions; currentselected20/23/32/57 holders unchanged.',
        'NoKnoxATL/CamReddishSolomonHillNYK orCHAconditional1R expenditure automatically executed; olderHolddigest preserved.' ],
      'summary':{'selected_games':4,'CHI_wins':sum(x['selected_regulation_winner']=='CHI'for x in games),'NYK_wins':sum(x['selected_regulation_winner']=='NYK'for x in games),
        'STD':15,'TW':2,'active':12,'positive_NYK':11,'new_UPCs':9,'new_TW_UPCs':2,'removed_zero_STD':2,'signed_existing_draft1R':2,'unsigned2R':2,
        'paired_elapsed_seconds_each':2880,'team_player_seconds_each':14400,'typed_reported_event_rows':len(eventstates),'whole82_results_certified':False},
      'remaining_ports':{'next_chronological_unjoined_key':'0022100083','opponent':'UTA','date':'2021-10-30',
        'requires':'Use selectedsourceparent and newnamedlawfulUTA interval beforeownregulationwinner; no firstseasonhistoryautomaticclone.',
        'whole2022_standings_picks_and_future_contract_choices':False},
      'certification':{'selected_fictional_lawful_NPC_family':True,'selected_working_positive_availability_and_result':True,
        'independent_review_completed':False,'actual_contract_medical_receipt_or_exactprice':False,'wholeprivate_teamcost':False,
        'new_important_author_lock':False,'whole82_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    lines=['# New York keeper·신인 가족과 Chicago 네 날짜 결과','',
      '**선택된 법적 NPC 작업 가족·승자 모델, 독립 검문 대기.** 최초10/28과 같은계약기간 안의11/21·12/2·3/28을 한가족으로 연결했다. 현재실계약/의료/가격 인증이 아니다.','',
      '|날짜|키|CHI 상태|작업 승자|CHI 방향 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:lines.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_NYK_impact_per100']:.9f}|")
    lines +=['','## 법적 경로와 실제값의 구별','',
      '원S2 소속을 보존하고 usual Payton/Barrett/Bullock/Randle/Robinson 선발·양수11의 별도 감독240분을 선택했다. 이전 uniform수학표는 Temp 역사snapshot으로 보존했고 현재분으로 사용하지 않는다. Pelle/Vildoza의 만료 또는 적법 nonassignment방출 뒤 원보호비용을 전액남기고 DB1 #20Grimes/#23Dosunmu RSC를 받는다. STD15/TW2·active12이며 Grimes0active/Ayo0inactive는 네 감독계획만의 선택이다. 신인 영구0분/경력삭제를 잠그지 않는다.','',
      '기존live6는 currentΓ와 적법옵션을 보존한다. 만료UFA6는 [2017CBA](https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf) I1u/VII6b의 EarlyBird 또는 NonBird 구간을 사용하는 2년·flatbase·새bonus0 가족이다. Rose/Bullock의 두시즌 가족과 신규 Burks/Noel을 구별한다. Payton/Gibson의 2020방출만으로 Bird초기화라고 단정하지 않고, Early가있으면 VII4d2 제한고지로 NonBird로 만드는 가상법적행동을 명명했다. fullFArenounce가 아니다.','',
      'flat 첫base는 올해와 signed2021의 2년차 법정최소 둘 이상이며 Early는 min(II7max,max(175%priorRegular,105%priorAverage)), NonBird는 min(II7max,max(120%priorRegular,120%currentMinimum)) 이하이다. ExC의7YOS이상 네유형은 2년차최소가 올해최소120% 아래여서 구간이 비지 않는 것을 지원한다. 새bonus0라 예전bonus상단을 base에 몰래 옮기지 않는다. 정확q/최저값/시장수락을 선택하지 않았다. 보호·지급조건이 적법한 가상합의이며 과거 원급여·bonus·방출잔액은 별도 유지한다.','',
      '[공식RFA목록](https://www.nba.com/news/2021-free-agency-options-and-qualifying-offers)의 원Frank 미발급과 Harper/Pinson UFA를 사실로 보존한다. Frank는 7/31 적법ordinaryRSCQO 가상발급·8/6수락 경로, Harper/Pinson은 YOS<4·1년·무옵션 새TW를 선택한다. 원실발급을 주장하지 않는다. 2R32/57은 operativeW21 유효미수락RT이며 표준계약2명을 더하지 않는다. 새해외통지·다음드래프트에서는 재개방한다.','',
      'NBA[당시팀프로필](https://www.nba.com/draft/2021/team-profiles/new-york-knicks)의 계약/FA 구분은 웹본문관측이다. 직접HTTP5개는403으로 보존했고 그실패HTML을 원문인증으로 계수하지 않았다. 기존동결NBAfeed의 실명계약·방출원천과 원CBA를 직접 소비한다.','',
      'live/waivedformer/FAholds/draftRT/unusedexceptions/incomplete 여섯 범주의 Γ를 삭제하지 않는다. 신규NTMLE/BAE/수취S&T 없이 ownVeteran/QO/RSC/TW를 사용하므로 caproom/apron숫자0에 기대지 않는다. 정상/apron총액은null이며 실제전역미공개장부가 무부담이라는 인증은 아니다.','',
      '## 날짜·분·나비효과','',
      'currentM1 Mark32/Caruso18/P32와 위임된CHI일별상태, 새NYK24개2분블록을 초별로 조인한다. Payton20/Rose24/Quickley22/Barrett32/Burks20/Bullock26/Randle34/Toppin14/Robinson28/Noel14/Gibson6=240분이다. active11+Grimes, inactiveFrank/Ayo/Knox를 네날짜 감독·양수가용 모델로 선택했다. 각48/240·5포지션·active/양수분을 대조한다. 원2020–21 G/F/C는 작업역할원천이며 실제2021–22 분이 아니다. 같은singleBPM shrink/홈2/연전.5·주인공−.5를 사용하며 원점수/부상/OT는 결과에 복사하지 않는다.','',
      '다른NYK 날짜는 원계약기간+명시적가상retention을 소비한다. 중간원보고 GroupSort/선수를 열거해 원Knox→ATL·Fournier/Kemba영입·Randle미래연장·hardship계약을 자동적용하지 않는다. NYK행만으로 DAL/PHX/BOS의 상대계약·결과까지 닫지 않는다. 다음은10/30 UTA0022100083의 명명된법적가족이다.','',
      '## 7행 진행','',
      '|번호|작업|현황|','|---|---|---|','|1|2020드래프트연쇄|완료|','|2|Chicago2020–21|완료|',
      '|3|2021–23 계약·시즌|NYK 1가족4결과 선택·검문대기|','|4|장기커리어|후속시즌 미완|','|5|결말·전체구조|미완|',
      '|6|집필규격·ContextPack|현행누적기능등록기 참조·Pack0|','|7|통합·독립·작가승인|최종CLOSED|','',
      '[현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 미완료 큰묶음5·6번까지4. v0.30 PARTIAL/CLOSED/원고0. 이4건의작성자통제를 독립검문으로 계수하지 않는다.','']
    return '\n'.join(lines)
def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved NYK family differs from source-bound construction']
    except(ValueError,KeyError,StopIteration,AssertionError)as e:return[str(e)]
def self_test():
    out=[];old=contracts
    def wrongprice():
        x=old();next(r for r in x if r['player']=='Alec Burks')['price_function']['first_base_ceiling']='UNBOUNDED_100_MILLION';return x
    with patch(__name__+'.contracts',wrongprice):
        try:build()
        except ValueError:out.append('RETURNED_VETERAN_PRICE_CLASS_BYPASS')
        else:raise AssertionError('FalsePASS price')
    pp=paired
    def wrongroles(c,n):
        x=pp(c,n);x[0]['NYK']['PG'],x[0]['NYK']['SG']=x[0]['NYK']['SG'],x[0]['NYK']['PG'];return x
    with patch(__name__+'.paired',wrongroles):
        try:build()
        except ValueError:out.append('RETURNED_SAME_TOTAL_POSITION_SWAP')
        else:raise AssertionError('FalsePASS roles')
    ss=sources
    def wrongrights(root):
        x=ss(root);next(r for r in x[DRAFT]['selected_rows']if r['pick']==23)['conditional_final_draft_rights_holder']='HOU';return x
    with patch(__name__+'.sources',wrongrights):
        try:build()
        except ValueError:out.append('RETURNED_DOSUNMU_HOLDER_WITH_UNCHANGED_SOURCE_SHA')
        else:raise AssertionError('FalsePASS rights')
    return out
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(physical(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'NYK source currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'results':[{k:x[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_NYK_impact_per100')}for x in d['selected_games']],
      'writer_negative_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
