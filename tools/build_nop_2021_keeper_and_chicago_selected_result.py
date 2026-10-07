"""A named cap-exempt NOP keeper family and October22 working BPM result.

This selects an admitted lawful fiction, not actual contract signatures. Current
cost components remain symbolic; no hardcap budget is inferred from a null
ledger. Prior reviewed capacities are consumed without ancestor constructors.
"""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from datetime import date,timedelta
from statistics import median
from unittest.mock import patch
import argparse,csv,hashlib,io,json
import fitz
from bs4 import BeautifulSoup
import build_chicago_detroit_2021_two_date_selected_bpm_results as det

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_nop_2021_keeper_and_chicago_selected_result.py'
OUT='simulation/CHICAGO_NEW_ORLEANS_2021_SELECTED_KEEPER_RESULT.json'
MD=OUT[:-5]+'.md'
BASELINE='560e507db94f2d52c1fb56eeaccc62bb1675e726'
PAIR='simulation/CHICAGO_NEW_ORLEANS_2021_SECOND_PAIRED_REGULATION_CARRIER.json'
CHI='simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json'
ROSTER='simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json'
DRAFT='simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json'
HEALTH='simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json'
AUTH='canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json'
KILLIAN='simulation/2020_DRAFT_KILLIAN_HAYES_RELANDING_BOARD.csv'
DET_RESULT=det.OUT
MINIMUM='research/DETROIT_2021_A_ROUTINE_OPERATING_EXECUTION_FAMILY_2026_10_07.json'
PINS={
 PAIR:'bbb3288f239d5a181be19e0f2ac615c4acb46b13f7d11eecfa1d90990b3cbc8e',
 CHI:'73d51b630e9c9d4ec31b7e3952906165589bd8c49a48bb07c79bdc9ad02e8fca',
 ROSTER:'cfa2f49bb82baa49b2298d90c97cd7fd8075e91380424d40bfd44772d8228a2b',
 DRAFT:'f8c78e99cce1b02a051c94339b550fdb52205d3988db8bbe69b780559c3bc306',
 HEALTH:'274a35e163c7f6fd7f0d3e5494b3c46753aaf9900036676be935f17a9d538c32',
 AUTH:'51b24c8a6bc1eb703568adced46b3ffa15845e85e8da10da1242bddf941df960',
 KILLIAN:'1b4d42934dcfad4569f7a0a8495c2a1972f2cbff194397f7b35bf04d73acedb0',
 DET_RESULT:'66c1c862a179648aa72dd81ff13a07345b36889043995ecb583ae57019618c80',
 det.SELF:'ebe05a0c9b886cee62cf00c82ba0c69b72778e24ca621d1028f3e58544524e6e',
 MINIMUM:'855371610d0f2b776b773bdf2ff02f27a43684b6c1407b1d54f698c6e0f093ef',
 det.CAL:'c59ea19a5515d64ed03cae8e0481847b6572d4087bbcefef15896bb7a2489183',
 det.LEAGUE:'92869bc987896a4172c5e54e3684d2604c5c24d828e9bcf3cc27af30ebc83644',
 det.BPM:'1d1455f7f4ddd73ef46e3ce16752b558c392ed2d284434acd295ca6659e937ef',
}
CBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
TEMP=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-nop-keeper-20261007')
FEED=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-nba-player-movement-2026-10-04.json')
FEED_SHA='3d9d7a6dd7ccd39ddfdd1799a26ef9901b44682d85a26f05239b468a8ae92e3a'
GAME='0022100022'
RETAINED=('Brandon Ingram','Eric Bledsoe','Jaxson Hayes','Killian Hayes','Naji Marshall',
 'Nickeil Alexander-Walker','Steven Adams','Wenyen Gabriel','Wes Iwundu','Zion Williamson')
RFA=('Lonzo Ball','Josh Hart','Didi Louzada')
SECOND=((34,'Kessler Edwards'),(40,'Miles McBride'),(42,'Greg Brown'),(52,'Jericho Sims'))
POLICY={'keeper_route':'NOP_RETAINED_CORE_NO_OPTIONAL_SUMMER_TRADES',
 'ordinary_QO_acceptances':list(RFA),'QO_acceptance_datetime_ET':'2021-08-06T12:02:00',
 'Maximum_QO_used':False,'offer_sheet_or_new_team_assignment':False,
 'Willy_new_contract':'ONE_YEAR_LEGAL_MINIMUM_EXCEPTION_NO_BONUS',
 'Moody_contract':'PICK9_ROOKIE_SCALE_80_TO_120_PERCENT_LAWFUL_COMPONENT_FAMILY',
 'Gabriel_Oct12_waiver_in_model':False,'Nunnally_new_TW_or_Johnson_new_UPC':False,
 'new_incoming_sign_and_trade':False,'new_NTMLE':False,'new_BAE':False,
 'new_TMLE_or_RoomMLE':False,'new_counterparty_trade':False,
 'positive_availability_and_Zion0_working_selected':True,
 'old_protection_bonus_FA_holds_TPE_claims_deleted':False,'new_actual_acceptance_certified':False}
POLICY_FIXED=deepcopy(POLICY)
QO_RULES={
 'Lonzo Ball':{'article':'XI1c(ii)(B)','draft_class':2017,'pick':2,
   'ordinary_components':'FourthYearSalaryComponents*(1+applicable_pick2_QO_increase)',
   'if_nonstarter':'lesser_of_ordinary_and_pick15_120_percent_scale_QO_package',
   'anchor_rank':15,'anchor_scale_fraction':'6/5','anchor_bonuses':0},
 'Josh Hart':{'article':'XI1c(ii)(A)','draft_class':2017,'pick':30,
   'ordinary_components':'FourthYearSalaryComponents*(1+applicable_pick30_QO_increase)',
   'if_starter':'pick9_120_percent_scale_QO_base_only',
   'anchor_rank':9,'anchor_scale_fraction':'6/5','anchor_bonuses':0},
 'Didi Louzada':{'article':'XI1c(iv)','draft_class':2019,'pick':35,'YOS':1,
   'ordinary_components':'PriorSalaryComponents*5/4',
   'minimum_plus_if_greater':'MinimumAnnualSalary(YOS1,2021)+200000_base_only',
   'minimum_plus_bonuses':0,'two_or_three_YOS_starter_override_applies':False}}
QO_RULES_FIXED=deepcopy(QO_RULES)

def need(ok,msg):
    if not ok:raise ValueError(msg)
def txt(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(txt(p).encode()).hexdigest()
def physical(root,p):
    t=txt(root/p)
    return json.loads(t) if p.endswith('.json') else list(csv.DictReader(io.StringIO(t))) if p.endswith('.csv') else t
def sources(root):return {p:physical(root,p)for p in PINS}

def raw_support(pair):
    need(hashlib.sha256(CBA.read_bytes()).hexdigest()==CBA_SHA,'CBA raw changed')
    d=fitz.open(CBA);pages=(30,210,222,223,227,228,232,233,240,241,292,294,303,309,310,311,313,315,317,318,558)
    text={i:d[i-1].get_text().replace('\r\n','\n').replace('\r','\n')for i in pages}
    need('the Salary and Unlikely Bonuses required to be provided in a' in ' '.join(text[223].split()) and 'Qualifying Offer' in text[223], 'Own-RFA exception absent')
    need('Rookie Exception' in text[232] and 'two (2)' in text[233], 'RSC/minimum exception source absent')
    need('October 1' in text[317], 'QO acceptance source absent')
    rfa=pair['raw_sources']['NBA_RFA'];p=Path(rfa['cache_path']);need(hashlib.sha256(p.read_bytes()).hexdigest()==rfa['raw_sha256'],'RFA raw changed')
    j=json.loads(BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser').find('script',id='__NEXT_DATA__').string)
    body=BeautifulSoup(j['props']['pageProps']['article']['contentText'],'html.parser').get_text(' ',strip=True)
    need('Lonzo Ball (NOP)'in body and 'Josh Hart (NOP)'in body and "Louzada's team option was declined"in body,'Issued-QO positive source changed')
    guide=pair['raw_sources']['official_guide'];p=Path(guide['cache_path']);need(hashlib.sha256(p.read_bytes()).hexdigest()==guide['raw_sha256'],'Official guide raw changed')
    doc=fitz.open(p);history=doc[147].get_text()
    need('October 12, 2021'in history and 'forward Wenyen Gabriel'in history and 'Naji Marshall to multi-year contract'in history,'Existing named contract history absent')
    observations=[]
    for name,h in [('louzada_april','cd14404ea835ba22394eb4ba4822785431ae26bef2bdb2d12302c706b073e75b'),('freeagency2021','6628a4c0163a4fcee8fc7fdeabb797a0b7cdf4c37178eb4b99f0452205963ad3')]:
        p=TEMP/(name+'.html');need(hashlib.sha256(p.read_bytes()).hexdigest()==h,'New primary raw changed')
        j=json.loads(BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser').find('script',id='__NEXT_DATA__').string)
        pp=j['props']['pageProps']
        if name=='louzada_april':
            b=' '.join(x.get('text')or''for x in pp['pageObject']['contentStructured']if isinstance(x,dict));loc='__NEXT_DATA__.props.pageProps.pageObject.contentStructured[*].text'
            need('multi-year contract'in b and 'terms of the deal were not disclosed'in b,'April original contract source absent')
            url='https://www.nba.com/pelicans/news/pelicans-sign-didi-louzada'
        else:
            b=BeautifulSoup(pp['article']['contentText'],'html.parser').get_text(' ',strip=True);loc='__NEXT_DATA__.props.pageProps.article.contentText'
            need('Aug. 6 at 12:01 p.m.'in b or 'Aug. 6 at 12:01'in b,'2021 signing clock source absent')
            url='https://www.nba.com/news/nba-announces-start-date-for-2021-free-agency'
        observations.append({'url':url,'cache_path':str(p),'HTTP':200,'raw_sha256':h,'body_locator':loc,
          'exact_extracted_string_sha256':hashlib.sha256(b.encode()).hexdigest(),'body_successfully_read':True,'actual_counterfactual_receipt_certified':False})
    need(hashlib.sha256(FEED.read_bytes()).hexdigest()==FEED_SHA,'Frozen NBA movement raw changed')
    f=json.loads(FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    l=[x for x in f if 'Louzada'in x['TRANSACTION_DESCRIPTION'] and x['TRANSACTION_DATE'].startswith('2021-04-27')]
    need(len(l)==1 and l[0]['TEAM_ID']==1610612740 and 'Rest-of-Season'in l[0]['TRANSACTION_DESCRIPTION'],'Selected ROS feed observation changed')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(CBA),'raw_sha256':CBA_SHA,
      'normalized_fitz_page_text_sha256':{str(i):hashlib.sha256(t.encode()).hexdigest()for i,t in text.items()},
      'direct_positive_rules':{'VII6a_PDF222_223':'Valid existing contracts may exceed cap.',
        'VII6b2iii_PDF223':'Prior-team restricted free agent may sign at required QO Salary+Unlikely, even if ordinary NonBird120% lower.',
        'VII6h_i_PDF232_233':'Rookie-scale and bonus-free one/two-season legal-minimum exceptions.',
        'VII6d_e_8e_PDF227_228':'Selected family uses no BAE/NTMLE or incoming sign-and-trade apron trigger.',
        'XI1c_4_PDF309_318':'OrdinaryQO component/protection/timely acceptance; RSC starter/nonstarter and otherRFA rules.',
        'VIII1_X4_PDF292_303':'RSC terms/options and timely required-tender draft rights; operative2021 calendar is a typed condition.'}},
      'reused_primary_RFA':deepcopy(rfa),'reused_primary_guide':deepcopy(guide),
      'new_primary_bodies':observations,'frozen_feed':{'cache_path':str(FEED),'raw_sha256':FEED_SHA,
        'Louzada_original_event':l[0],'disagreement':'Feed ROS vs club Aprilmulti-year. Neither fixes exact years; S2 selected expiry is null. August multi-year re-sign is a separate event.'}}

def contract_family(src):
    plan=src[PAIR]['NOP_named_proposal'];standard=plan['standard_candidate']
    keep=[{'player':p,'route':'VII6a_EXISTING_LAWFUL_CONTRACT_CARRY','new_UPC':False,
      'current_term_covers_2021_10_22':True,'salary_components':'Original lawful current-year base/allocatedbonus/likely/unlikely/protection Γ unchanged.',
      'actual_component_dollars':None,'actual_receipt':None}for p in RETAINED]
    for x in keep:
        if x['player']in ['Zion Williamson','Jaxson Hayes','Nickeil Alexander-Walker']:
            x['prior_valid_Year3_option']='Preserve a valid exercise in operative2020 optionwindow; original Oct2021 Year4 notices concern nextyear and are not selected here.'
        if x['player']=='Killian Hayes':x['rookie_identity']={'pick':13,'holder':'NOP','year':2,'Kira_salary_or_Detroit_pick7_not_copied':True}
        if x['player']=='Wenyen Gabriel':x['carry_basis']='Original Nov2020 signing and positive Oct12 waiver prove a live-contract family; choose noOct12 waiver, retaining all original current charge/bonus. No new salary or guessed exact2-year UPC.'
    rfa=[]
    for p in RFA:
        func=('RSC components×applicableQOincrease; rank2 nonstarter lesser#15 or original; rank30 starter fixed#9, otherwise original.' if p!='Didi Louzada'
          else 'OtherRFA: componentwise1.25×priorSalary; if minimumPlus exceeds priorQO, legalMin(YOS1,2021)+200000 base and zeroQObonuses (XI1civ).')
        rfa.append({'player':p,'route':'VII6b_PRIOR_TEAM_VALID_ORDINARY_QO',
          'QO_salary_function':func,'starter_state':'SOURCE_PARAMETER_NOT_HISTORICAL_STAT_CHOICE'if p!='Didi Louzada'else'NOT_TWO_OR_THREE_YOS_STARTER_BRANCH',
          'pick':2 if p=='Lonzo Ball' else 30 if p=='Josh Hart' else 35,
          'componentwise_QO_rule':deepcopy(QO_RULES[p]),
          'team_signed_and_timely_delivered_in_operative2021_window':True,'withdrawn_or_rescinded':False,
          'acceptance_datetime_ET':POLICY['QO_acceptance_datetime_ET'],'acceptance_before_applicable_QO_cutoff':True,
          'known_disability_requires_disclosure_and_team_consent_if_applicable':True,
          'ordinary_QO_only_not_MaximumQO':True,'QO_base_fully_protected_and_payment_paragraph3':True,
          'old_QO_component_entitlement_and_II7_maximum_preserved':True,
          'new_UPC':True,'current_term_covers_2021_10_22':True,'actual_component_dollars':None,'actual_receipt':None})
    extra=[{'player':'Willy Hernangomez','route':'VII6i_ONE_YEAR_LEGAL_MINIMUM','years':1,'salary_function':'MinimumAnnualSalary(YOS5, signed2021 schedule)','bonuses':0,
      'new_UPC':True,'current_term_covers_2021_10_22':True,'acceptance_datetime_ET':'2021-08-06T12:02:00','actual_component_dollars':None,'actual_receipt':None},
      {'player':'Moses Moody','route':'VII6h_PICK9_ROOKIE_SCALE','pick':9,'holder':'NOP','years_guaranteed':2,'team_options':2,
       'CBC_scale_fraction_interval':[0.8,1.2],'CBC_minimum_protection_scale_fraction':0.8,'salary_plus_unlikely_scale_ceiling':1.2,
       'valid_first_RequiredTender_in_operative_W21_before_new_UPC':True,'UPC_datetime_ET':'2021-08-06T12:02:00',
       'actual_first_RT_delivery_date':None,'noncompeting_foreign_or_intercollegiate_impediment_in_selected_participation_family':True,
       'new_UPC':True,'current_term_covers_2021_10_22':True,'actual_component_dollars':None,'actual_receipt':None}]
    return keep+rfa+extra

def assert_family(rows,src):
    # Independent caller authority mapping, not a second call to contract_family.
    standard=src[PAIR]['NOP_named_proposal']['standard_candidate']
    need(len(rows)==15 and len({x['player']for x in rows})==15 and {x['player']for x in rows}==set(standard),'Named live contract membership changed')
    need(QO_RULES==QO_RULES_FIXED,'Source QO policy changed')
    for x in rows:
        p=x['player'];need(x['current_term_covers_2021_10_22']and x['actual_receipt']is None and x['actual_component_dollars']is None,'Term or actual receipt promoted')
        route='VII6a_EXISTING_LAWFUL_CONTRACT_CARRY'if p in RETAINED else'VII6b_PRIOR_TEAM_VALID_ORDINARY_QO'if p in RFA else'VII6i_ONE_YEAR_LEGAL_MINIMUM'if p=='Willy Hernangomez'else'VII6h_PICK9_ROOKIE_SCALE'
        need(x['route']==route and x['new_UPC']==(p not in RETAINED),'Cap exception or signing identity changed')
        if p in RFA:
            need(x['componentwise_QO_rule']==QO_RULES_FIXED[p] and x['pick']==QO_RULES_FIXED[p]['pick'],'Returned QO salary/anchor function changed')
            need(x['team_signed_and_timely_delivered_in_operative2021_window']and not x['withdrawn_or_rescinded']and x['ordinary_QO_only_not_MaximumQO']and x['QO_base_fully_protected_and_payment_paragraph3']and x['old_QO_component_entitlement_and_II7_maximum_preserved'],'Valid-QO source function lost')
            need(x['acceptance_datetime_ET']=='2021-08-06T12:02:00'and x['acceptance_before_applicable_QO_cutoff'],'QO signing calendar changed')
        if p=='Willy Hernangomez':need(x['years']==1 and x['bonuses']==0,'Minimum exception term/bonus changed')
        if p=='Moses Moody':need(x['pick']==9 and x['holder']=='NOP'and x['years_guaranteed']==2 and x['team_options']==2 and x['CBC_scale_fraction_interval']==[.8,1.2]and x['valid_first_RequiredTender_in_operative_W21_before_new_UPC'],'RSC entitlement or terms changed')

def build(root=ROOT):
    src=sources(root)
    need(set(src)==set(PINS),'Source domain changed')
    for p,h in PINS.items():need(sha(root/p)==h and src[p]==physical(root,p),'Returned source/physical field changed: '+p)
    need(POLICY==POLICY_FIXED,'Keeper fixed policy changed')
    pair=src[PAIR];need(pair['certification']['independent_review_completed'],'Pair capacity unreviewed')
    need(pair['game']=={'game_id':GAME,'game_number':2,'date':'2021-10-22','home':'CHI','away':'NOP'},'Calendar key changed')
    raw=raw_support(pair);draft=[x for x in src[DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='NOP']
    need([(x['pick'],x['player'])for x in draft]==[(9,'Moses Moody'),*SECOND]and all(x['lawful_PS21_participant_model_selected']for x in draft),'Selected draft identity/eligibility family changed')
    k=[x for x in src[KILLIAN]if x['pick']=='13'and x['branch']=='PRIMARY'];need(len(k)==1 and k[0]['rival_world_selection']=='Killian Hayes'and k[0]['status']=='AUTHOR_LOCKED','Approved Killian13 landing changed')
    last=next(x for x in reversed(src[ROSTER]['team_game_bindings'])if x['team']=='NOP');old=src[ROSTER]['roster_states'][last['state_id']]
    standard=[x['player']for x in old['players']if x['contract_class']=='STANDARD'];need(set(pair['NOP_named_proposal']['standard_candidate'])==(set(standard)-{'James Johnson'})|{'Moses Moody'},'S2 roster→keeper membership changed')
    louzada=next(x for x in old['players']if x['player']=='Didi Louzada');need(louzada['working_expiry_inclusive']is None,'Selected old Louzada term changed')
    contracts=contract_family(src);assert_family(contracts,src)
    witness=deepcopy(next(x for x in pair['witnesses']if x['CHI_state']=='COBY_OUT'))
    health=next(x for x in src[HEALTH]['selected_dates']if x['game_id']==GAME)
    need(health['selected_chicago_state']=='COBY_OUT'and src[AUTH]['selected']['selected_date_rows']['sha256']==PINS[HEALTH],'Current CHI state missing')
    calendar=src[det.CAL];next_game=next(calendar[i+2]for i,g in enumerate(calendar)if g['game_id']==GAME)
    need(next_game['game_id']=='0022100046'and next_game['date']=='2021-10-25'and next_game['home']=='TOR'and next_game['away']=='CHI','Next calendar source changed')
    sums={t:Counter()for t in ['CHI','NOP']};end=0
    for s in witness['simultaneous_segments']:
        need(s['start_second']==end and s['seconds']==s['end_second']-end>0 and s['quarter']==end//720+1 and s['end_second']<=(end//720+1)*720,'Common date clock mismatch')
        for t in sums:
            need(set(s[t])=={'PG','SG','SF','PF','C'}and len(set(s[t].values()))==5,'Position/identity conflict')
            for p in s[t].values():sums[t][p]+=s['seconds']
        end=s['end_second']
    need(end==2880,'Regulation not48')
    for t,sec in sums.items():
        n=witness['nominations'][t];need(sum(sec.values())==14400 and max(sec.values())<=2880 and set(sec)<=set(n['active'])and not(set(sec)&set(n['unavailable'])),'Positive budget/nomination unavailable')
        need(len(n['standard'])==len(set(n['standard']))==15 and len(n['active'])==len(set(n['active']))==12 and len(n['TW'])<=2 and not(set(n['TW'])&set(n['standard'])),'15+2/active family mismatch')
    need(dict(sums['CHI'])=={p:60*m for p,m in health['selected_regulation_player_minutes'].items()}and dict(sums['NOP'])==pair['NOP_named_proposal']['positive_player_seconds'],'Selected complete clock differs')
    names=set(sums['CHI'])|set(sums['NOP']);ds={det.BPM:src[det.BPM]}
    rate=det.expected_ratings(ds,names-{'Moses Moody'})
    comp={p:Fraction(next(x for x in src[det.BPM]if x['nba_player']==p)['bpm'])*int(next(x for x in src[det.BPM]if x['nba_player']==p)['archive_minutes'])/(1000+int(next(x for x in src[det.BPM]if x['nba_player']==p)['archive_minutes']))for p in det.COMPARATORS}
    v=median(comp.values());rate['Moses Moody']={'effective_rating':float(v),'exact_fraction':str(v),'classification':'SELECTED_FICTIONAL_ROOKIE_PRIOR_NOT_OBSERVED_NBA_RATING','provenance':{'comparators_effective':{p:float(v)for p,v in comp.items()},'selected_statistic':'median','not_fitted_or_future_NBA_observation':True}}
    need(all(rate[p]==src[DET_RESULT]['player_ratings'][p]for p in sums['CHI']),'Selected shared Chicago productivity changed')
    impact={t:sum(Fraction(rate[p]['exact_fraction'])*n/2880 for p,n in sums[t].items())for t in sums}
    yesterday='2021-10-21';back={t:any(x['date']==yesterday and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in sums}
    margin=impact['CHI']-impact['NOP']+2+Fraction(1,2)*(int(back['NOP'])-int(back['CHI']))
    result={'game_id':GAME,'date':'2021-10-22','home':'CHI','away':'NOP','CHI_state':'COBY_OUT',
      'method':'BPM_MAR25_EB','team_weighted_BPM_per100':{t:float(v)for t,v in impact.items()},
      'home_effect_in_CHI_direction_per100':2,'back_to_back_model':back,'fatigue_effect_in_CHI_direction_per100':float(Fraction(1,2)*(int(back['NOP'])-int(back['CHI']))),
      'CHI_minus_NOP_regulation_impact_per100':float(margin),'exact_impact_fraction':str(margin),
      'selected_regulation_winner':'CHI'if margin>0 else'NOP'if margin<0 else None,'score':None,'overtime_selection':None,
      'classification':'AUTHOR_DELEGATED_SELECTED_FICTIONAL_REGULATION_WINNER_MODEL','actual_game_or_clinical_certificate':False}
    need(result['selected_regulation_winner']is not None,'Tie requires separate result design')
    cost={'live_contracts':{'players':[x['player']for x in contracts],'normal':'sum of each legal current salary/base allocation/likely Γ','apron':'same + every unlikely Γ and applicable young-FA floor'},
      'waived_or_former':{'normal':'All original named source-family year charges retained; no waived money deletion by roster absence.','apron':'Normal plus applicable possible arbitration/resolution adjustment Γ; no new resolution event selected.'},
      'free_agent_holds':{'players':['James Johnson','James Nunnally','other original source-family FA entitlements'],'normal':'All surviving FA amounts retained; live-signed15 not double-counted with their old holds.','apron':'Exclude ordinary FA amounts per VII6m3D; prior unacceptedTWQO, if applicable, retained with its legal treatment; no renunciation selected.'},
      'draft_tenders_and_unsigned':{'players':[p for _,p in SECOND],'normal':'Four timely first RT legalMin(YOS0,2021); no newUPC/STD. Moody prior120% RSC hold replaced only after RSCsign.','apron':'Four legal RT/youngFA floor components retained as required VII6m3; none assumed0.'},
      'unused_exceptions':{'normal':'Existing unused exceptions/TPE amounts and expiry/offset functions preserved VII6m2; no arbitrary renunciation/zero.','apron':'Only the CBA-defined adjustments/exclusions; no hardcap budget waived by marking costnull.'},
      'incomplete_roster':{'normal':'max(0,12−applicablecapcount)*legalYOS0minimum at each stage; first stage retainedSTD10 plus originalFA/draft counts; finalSTD15 term0 by count.','apron':'Apply VII6m3 statutory count, not actualvacancy guess.'}}
    stages=[{'id':'AFTER_ORIGINAL_OPTION_AND_EXPIRY_CONTROLS','date_parameter':'lawful operative2021 expiration/option window beforeAug6','standard_players':list(RETAINED),'STD':10,'TW':0,'cost_Γ_preserved':True}]
    additions=['Moses Moody','Willy Hernangomez',*RFA];live=list(RETAINED)
    for p in additions:
        live.append(p);stages.append({'id':'NEW_VALID_UPC_'+p.replace(' ','_'),'datetime_ET':'2021-08-06T12:02:00_ORDERED_AFTER_PREVIOUS_EVENT','player':p,'standard_players':live.copy(),'STD':len(live),'TW':0,'cost_Γ_preserved':True})
    return {'id':'CHICAGO_NEW_ORLEANS_2021_SELECTED_KEEPER_RESULT','baseline_main':BASELINE,
      'status':'SELECTED_NAMED_LAWFUL_KEEPER_AND_REGULATION_RESULT_INDEPENDENT_REVIEW_PENDING',
      'source_sha256':{**PINS,SELF:sha(root/SELF)},'hash_convention':'BOMstrip CRLF/CR→LF for repository; external raw unchanged',
      'selected_policy':deepcopy(POLICY),'primary_support':raw,
      'classification':{'fact':'Original primary signings/issuedQOs/waiver/events and approved Killian13/selectedDB1 rights.','selected_model':'Lawful keeper agreements/notices and unchanged-obligation cost functions; positive12/Zion0/active12 and one BPM winner.','actual_private_receipt_or_contract_terms':'NOT_CERTIFIED'},
      'lawful_contract_family':contracts,'dated_registration_prefix':stages,
      'unsigned_second_round_family':{'claims':[{'pick':n,'player':p,'holder':'NOP','UPC':False,'STD':False,'new_author_lock':False}for n,p in SECOND],
        'selected_valid_first_RT_function':{'delivery':'Team-signed valid delivery τ chosen inside operative2021 X4a second-round window W21, following July29 InitialDraft; before this Oct22 game.',
        'window_not_invented_from_inoperative_July15_literal':True,'delivery_before_acceptance_cutoff_and_this_game':True,'salary':'legalMin(YOS0,2021)','stated_seasons':1,'acceptance_until_at_least':'2021-10-15',
          'unaccepted_by_player':True,'actual_delivery_date':None,'rights_scope_end':'2022 SubsequentDraft; reopens then or on newNonNBA/intercollegiate facts'}},
      'six_cost_categories_preserved_symbolically':cost,
      'cap_admissibility_proof':{'existing10_VII6a':True,'own_valid_QO3_VII6b_including_NonBird_b2iii':True,'minimum1_VII6i':True,'rookie1_VII6h':True,
        'new2021_BAE_NTMLE_incoming_SandT_trigger_count':0,'previous_year_hardcap_not_automatically_carried':True,
        'all_current_components_retained_not_zeroed':True,'lawful_Γ_NBA_exception_capacity_independent_of_unknown_total':True,
        'scope':'Each parameter realization uses actual CBA-valid inherited contracts and ordinaryQO functions; exceptions support the15 UPCs without a cap-room/apron spending assumption. Original issuedQO/completedcontract anchors support nonempty templates. This is not all-private-ledger certification.',
        'whole_NOP_scalar_cost_upper':None,'actual_current_cost':None,'actual_no_other_hardcap_trigger_certified':False},
      'selected_date_role_and_availability':{'game_id':GAME,'CHI_state':'COBY_OUT','NOP_positive12':sorted(sums['NOP']),
        'Zion_operational_unavailable':True,'zero_minute_clinical_status':None,'nominations':deepcopy(witness['nominations']),
        'player_seconds':{t:dict(sorted(c.items()))for t,c in sums.items()},'simultaneous_segments':deepcopy(witness['simultaneous_segments']),
        'selected_working_nomination_and_availability':True,'real_medical_or_registration_receipt':False},
      'selected_ratings':rate,'selected_result':result,
      'butterfly_handoff':['NoBall→Chicago/Satoransky→NOP. NoGraham→NOP/SandT.',
        'NoAdams/Bledsoe/Moody/2Rclaims→MEM and noJV/TreyMurphy/JaredButler/NOP2022first obligation automatically imported.',
        'Iwundu keptNOP; originalCHA relocation asset/cash requires freshjointmodel elsewhere.',
        'Gabriel kept live insteadofOct12waiver: actualsubsequentwaiver/10day moves are not copied. NoHerbJones/Alvarado/Hommes signing added.',
        '2022McCollum deadline package cannot inherit Satoransky or unchangedHart/Louzada money; new source-backed jointcheck required.'],
      'summary':{'selected_game_count':1,'STD':15,'TW':0,'active_each':12,'positive_NOP':12,'regulation_seconds':2880,'team_player_seconds':14400,
        'named_live_existing_contracts':10,'new_lawful_UPCs':5,'unsigned2Rclaims':4,'six_cost_categories':6,'caproom_trade_or_newhardcap_dependency':0,
        'selected_winner':result['selected_regulation_winner'],'CHI_minus_NOP_impact_per100':float(margin),'combined_DET2_plus_NOP_results':3,'remaining_CHI_dates':79},
      'remaining_ports':{'next_ready_paired_key':next_game['game_id'],'next_opponent':'TOR','next_date':next_game['date'],
        'TOR_current_legal_interval':'Consume reviewed selectedTOR atoms and unresolvedextraaproncost scope; no automaticMIAwholebudgetpass.',
        'actual_receipts_not_required_for_fictional_result':True,'whole82_standings_2022pick_not_certified':True},
      'certification':{'named_lawful_cap_exception_family_constructed':True,'selected_fictional_keeper_and_regulation_result':True,
        'independent_review_completed':False,'actual_contract_medical_receipt_certified':False,'actual_salary_cents_or_NOPwholeledger_certified':False,
        'whole82_or_macro3_certified':False,'new_major_author_lock':False,'manuscript_allowed':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED'}}

def markdown(d):
    x=d['selected_result'];return '\n'.join(['# NOP keeper 가족과 Chicago 10월22일 선택 결과','',
      '**법적 가상 keeper 가족과 규정시간 승자 작업모델을 선택했다. 독립 검문 대기.** 기존 조건부 용량 파일의 미선택 상태는 작성 이력이며 새 선택은 이 소비기의 범위다.',
      f"2021-10-22 `0022100022` CHI 홈: **{x['selected_regulation_winner']} 작업 승리**, CHI−NOP 영향 {x['CHI_minus_NOP_regulation_impact_per100']:.9f}/100. 새 최종점수·연장·실제 경기 인증이 아니다.",'',
      '## 계약·권리·비용을 실제 연결한 범위','',
      '- S2말단15에서 JamesJohnson 신규계약0, Nunnally 신규TW0, 기존live10 보존 +Moody9RSC/Willy1년minimum/Ball·Hart·Louzada 유효ordinaryQO 수락으로 STD15/TW0이다. 현재 선택DB1의 NOP #9 및2R34/40/42/52를 직접 조인했다. 승인 Killian13은 Kira 또는Detroit7 계약가격으로 치환하지 않는다.',
      '- [2017CBA](https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf) VII6a/b/h/i와 XI1c/4가 경로를 지원한다. 특히 NonBird RFA도 VII6b2iii의 요구QO금액 예외가 있으므로 Louzada를 일반120% 한도로 잘못 막지 않는다. Ball/Hart는 RSC starter/nonstarter 및 원salary/likely/unlikely 성분 함수로 계산하며 실제 선택한 과거 GS/분이나 정확QO가격을 발명하지 않는다.',
      '- [공식2021서명달력](https://www.nba.com/news/nba-announces-start-date-for-2021-free-agency)의 Aug6 12:01ET 이후, Aug6 12:02부터 유효합의를 순서대로 구현하는 모델이다. QO는 유효한 operative2021 통지·미철회·적용수락기한·필요장애고지/팀동의를 가진 가족으로 선택한다. 실제통지일·실수락·사적가격은null이다.',
      '- [구단April영입](https://www.nba.com/pelicans/news/pelicans-sign-didi-louzada) 원raw는 multi-year이고 원feed는ROS라 기간 해석을 분리했다. [공식RFA raw](https://www.nba.com/news/2021-free-agency-options-and-qualifying-offers)의 여름 옵션거절·QO와 August재계약은 별개다. S2선택은 expiry:null이다. April4년10m 또는자동1년만료를 사실로 확정하지 않았다.',
      '- Gabriel은 원영입·Oct12양성waiver 원문에 따른 기존live가족을 보존하고 그날방출을 모델에서 적용하지 않는다. 보호급여·bonus를 삭제하지 않고 정확2년 계약서를 추정하지 않는다. 원2019RSC Year3의 적법옵션을 보존하며 Oct2021 Year4옵션은 다음급여년도 조건이다.',
      '- 4명의2R는 법정최소1년 유효RT 함수만 선택한 미수락 권리로 STD4를 추가하지 않는다. operativeW21 통지창을 인자로 두고 2021지연드래프트에 무효July15를 쓰지 않는다. 실제RT일/후속Draft이후권리까지 인증하지 않는다.','',
      '## 장부0과 구별한 cap 예외 증인','',
      '기존live/QO/minimum/RSC만 쓰고 신규incomingS&T·NTMLE·BAE를 선택하지 않아 새2021하드캡을 만들지 않는다. 각 적법Γ의 기존급여·보호·bonus·FAhold·unusedexceptions/TPE·4RT·incomplete 함수, 여섯 범주를 그대로 보존한다. caproom 지출이나 apron 상단 조건으로 서명하지 않으므로 미입력 총액을0으로 만들 필요가 없다. 이는 명명된 CBA예외 구현 가족의 증인이며 실제NOP전체원장 상단은null이다. 잘못된 미공개원계약까지 합법이라 정의한 것은 아니다. 새로운비용/무효통지/다른예외사용/경쟁UPC가 밝혀지면 해당typedfamily를 재개방한다.','',
      '## 현재 시계·건강·영향','',
      'CHI COBY_OUT와 현재M1 주인공32/Mark32/Caruso18, NOP양수12/Zion운영상0, 양팀active12·48분/240분·14동시구간을 원paired에서 대조했다. 임상진단은null이다. 기존DET2와 같은 BPM shrink/초÷2880·홈2·연전.5 정책을 사용한다. Moody는 같은신인비교 중앙값 작업prior, 다른선수는2021Mar25관측을 대체세계proxy로 선택한다. 과거 Naji/Gabriel 표본은20분뿐이라 강한shrink가 걸리며 실제능력·신뢰구간으로 읽지 않는다. 원점수/OT는승자에 사용하지 않는다.','',
      'Adams/Bledsoe→MEM, JV/Graham→NOP, Ball→CHI, Iwundu→CHA 및 해당픽·cash를 원역사대로 가져오지 않았다. McCollum2022 후속도 새공동검문이 필요하다. 다른팀에 이미발생한충돌을 이 NOP부분만으로 닫지 않는다.','',
      '## 다음 결과 소비와 진행표','',
      'DET2+NOP1이면 선택된Chicago 결과는3/82, 잔여79. 다음readypaired는 10/25 TOR `0022100046`; 현재법적거래/잔여apron범위와 날짜가용을 먼저 소비한다. 전체순위·2022픽은미완료다.','',
      '|번호|작업|상태|','|---|---|---|','|1|2020드래프트연쇄|완료|','|2|Chicago2020–21|완료|',
      '|3|2021–23거래·계약|진행: NOP keeper와1결과 선택·검문대기|','|4|장기커리어|진행·후속시즌입력|','|5|결말·구조|전체미완료|',
      '|6|집필규격·ContextPack|현행기능등록기참조·Pack0|','|7|통합·독립·작가승인|최종CLOSED|','',
      '[현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 미완료큰묶음5·6번까지4. v0.30 PARTIAL/CLOSED/원고0. 작성자검사는독립검수로계수하지 않는다.',''])

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved selected family differs from source-bound reconstruction']
    except(ValueError,KeyError,AssertionError,StopIteration)as e:return[str(e)]

def self_test():
    f=contract_family;s=sources;out=[]
    def wrongq(src):
        x=f(src);next(v for v in x if v['player']=='Didi Louzada')['route']='NEW_NTMLE';return x
    def falseaccept(src):
        x=f(src);next(v for v in x if v['player']=='Lonzo Ball')['actual_receipt']=True;return x
    for label,fn in [('LOUZADA_OWN_QO_TO_NTMLE',wrongq),('ACTUAL_QO_RECEIPT_PROMOTION',falseaccept)]:
        with patch(__name__+'.contract_family',fn):
            try:build()
            except ValueError:out.append(label)
            else:raise AssertionError('FalsePASS '+label)
    def wrongsource(root):
        x=s(root);next(v for v in x[DRAFT]['selected_rows']if v['pick']==9)['conditional_final_draft_rights_holder']='MEM';return x
    with patch(__name__+'.sources',wrongsource):
        try:build()
        except ValueError:out.append('RETURNED_MOODY_HOLDER_WITH_UNCHANGED_SOURCE_SHA')
        else:raise AssertionError('FalsePASS source')
    return out

def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(physical(ROOT,OUT)==d and txt(ROOT/MD)==markdown(d),'Saved selected family stale')
    print(json.dumps({'current':True,'summary':d['summary'],'writer_negative_controls':self_test()if v.self_test else None}))
if __name__=='__main__':main()
