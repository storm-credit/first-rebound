"""Brooklyn keeper UPC family, jurisdiction-aware availability, three working results."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from datetime import date,timedelta
from unittest.mock import patch
import argparse,csv,hashlib,io,json
import fitz
import build_nyk_2021_keeper_and_chicago_selected_results as base
import build_chicago_detroit_2021_two_date_selected_bpm_results as det
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_bkn_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_BROOKLYN_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='759ae823c184e9a48c47435151fe8bd4aa3a1c90'
PREFIX='research/BKN_WAS_2021_PRE_JORDAN_NAMED_EXECUTION_FAMILY_2026_10_07.json'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
PRICE='design/P1_DINWIDDIE_PRICE_AND_ROLE_PLAUSIBILITY_2026_10_07.json'
PINS[PRICE]='058cd87115c41535344e5882157c9114b6839e1065cfaa56613c72158e9df7ad'
PREFIX_PIN='a0e9ede786047a43abac4d21785b68ae55190e3d768096618ed010147906017b'
need=base.need;sha=base.sha;physical=base.physical;text=base.text
CAPACITY=base.CAPACITY;CHI=base.CHI;DRAFT=base.DRAFT;HEALTH=base.HEALTH;AUTH=base.AUTH
IDS=('0022100148','0022100343','0022100625')
LIVE=('Alize Johnson','DeAndre Jordan','James Harden','Joe Harris','Kevin Durant','Kyrie Irving','Landry Shamet','Nicolas Claxton')
MINIMUM=('Blake Griffin','Timothe Luwawu-Cabarrot','Tyler Johnson')
OBS=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-bkn-keeper-20261007/observed_support.json')
OBS_SHA='9bc959146979df9f23e0b570bc80cb00e9846b3dcf73f7f1c30b01b36f856b23'
CHI_ORDER=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-bkn-keeper-20261007/CHI2021_2_archived.pdf')
CHI_ORDER_SHA='34b6dfbb87f65b54b6e5ddd0e77cf2c210d06fc722857e2f347ae283ea0f3903'
ROLE_MINUTES={
 'IRVING_INSTITUTIONAL_OUT':{'PG':{'James Harden':32,'Spencer Dinwiddie':16},'SG':{'Joe Harris':30,'Landry Shamet':18},'SF':{'Kevin Durant':18,'Bruce Brown':18,'Landry Shamet':12},'PF':{'Kevin Durant':16,'Jeff Green':18,'Blake Griffin':14},'C':{'Nicolas Claxton':28,'Blake Griffin':6,'DeAndre Jordan':14}},
 'IRVING_AWAY_RETURN':{'PG':{'James Harden':32,'Kyrie Irving':16},'SG':{'Joe Harris':30,'Kyrie Irving':16,'Landry Shamet':2},'SF':{'Kevin Durant':18,'Bruce Brown':18,'Landry Shamet':12},'PF':{'Kevin Durant':16,'Jeff Green':18,'Blake Griffin':14},'C':{'Nicolas Claxton':28,'Blake Griffin':6,'DeAndre Jordan':14}}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'James Harden','SG':'Joe Harris','SF':'Bruce Brown','PF':'Kevin Durant','C':'Nicolas Claxton'}
ROLE_SEQUENCE_SHAS={'IRVING_INSTITUTIONAL_OUT': '896518de935e9e817e42d2e72894b99e911099efe3f7bca668ba6180a8d82961', 'IRVING_AWAY_RETURN': '420eddd30ccdfb977b71e30a3b5b25cd1cc86fa3efe5ae73a0c2cb46868d0980'}
PRICES={
 'Bruce Brown':{'route':'VII6b1_FULL_BIRD','seasons':2,'flat_first_base_interval':[5000000,6000000],'new_bonus':0,'full_standard_protection':True,'ordinary_QO_preserved_until_new_UPC':'XI1civ max(125%priorcomponents,min+200k,starter21anchor_ifapplicable), operative2021timely; newBirdUPC replacesQO bylaw not copiedoriginalQOacceptance'},
 'Spencer Dinwiddie':{'route':'VII6b1_FULL_BIRD','seasons':2,'flat_first_base_interval':[17000000,18000000],'new_bonus':0,'full_standard_protection':True,'valid_prior_player_option_nonexercise':True,'reported_price_comparator_not_actual_salary':17142857,'actual_acceptance':None},
 'Jeff Green':{'route':'VII6f_TAXPAYER_MLE','seasons':2,'flat_first_base_interval':[4800000,5200000],'new_bonus':0,'full_standard_protection':True,'aggregate_first_Salary_plus_unlikely_max':5890000,'unused_first_capacity_lower':690000,'other_sameyear_NTMLE_BAE_ROOMMLE_incoming_SandT':False}}
PRICES_FIXED=deepcopy(PRICES)
POLICY={'new_UPCs_ET':'2021-08-06T12:02:00_ORDERED','MikeJames':'ROS expiration or lawful nonassignmentwaiver iflive; protectedGamma retained','P1_Dinwiddie_SandT_selected':False,'Jordan_DET_assignment_selected':False,'Kyrie_11_8':'Team no-part-time workingpolicy: no participation, not clinicaldiagnosis','Kyrie_12_4':'NYC home-team access restriction preserved: no participation, no visitingathlete exemption','Kyrie_1_12':'Choose road-only teampolicy plus nonresident Chicago competitor exception and fictional operational availability; no actual vaccination/testing certificate','new_trade':False,'new_NTMLE_BAE_incoming_SandT':False,'new_TW_UPCs':False,'real_medical_private_receipts_certified':False}
POLICY_FIXED=deepcopy(POLICY)

def sources(root):return {p:physical(root,p)for p in PINS}

def direct_physical(root,p):
    # Bind a returned loader object to the pinned disk bytes through a separate parser.
    t=(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
    return json.loads(t)if p.endswith('.json')else list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else t

def support():
    need(hashlib.sha256(base.CBA.read_bytes()).hexdigest()==base.CBA_SHA,'CBA raw changed')
    d=fitz.open(base.CBA);pages=(26,29,30,54,55,58,209,210,222,223,224,229,230,233,240,241,294,303,311,312,313,314,317,318,561)
    tx={n:d[n-1].get_text().replace('\r\n','\n').replace('\r','\n')for n in pages};flat=lambda n:' '.join(tx[n].split())
    need('three (3) preceding Seasons'in flat(29)and 'Minimum Player Salary Exception'in flat(233),'Bird/minimum source absent')
    need('Team Salary immediately following'in flat(229)and 'Tax Apron Amount'in flat(229)and 'not to exceed three (3) Seasons'in flat(230),'TMLE eligibility/term absent')
    need('twenty-first player'in flat(314)and 'one hundred twenty-five percent (125%)'in flat(313),'Brown nonRSC QO family absent')
    need('consecutive Two-Way Contracts'in flat(312)and 'October 1'in flat(317),'TW/QO boundaries absent')
    need(hashlib.sha256(base.FEED.read_bytes()).hexdigest()==base.FEED_SHA,'Frozen movement feed changed')
    feed=json.loads(base.FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    named={'Signing 1010390':'spencer-dinwiddie','Signing 1033224':'jeff-green','Trade 2019138':'bruce-brown','Signing 1037603':'blake-griffin','Signing 1039991':'mike-james','Signing 1033428':'tyler-johnson','Signing 1027790':'timothe-luwawu-cabarrot','Signing 1025548':'chris-chiozza','Signing 1034279':'chris-chiozza','ContractConverted 1034074':'reggie-perry'}
    rows=[x for x in feed if x['TEAM_ID']==1610612751 and x['GroupSort']in named and x['PLAYER_SLUG']==named[x['GroupSort']]]
    need(len(rows)==len(named),'Named BKN continuity/term anchors absent')
    need(hashlib.sha256(OBS.read_bytes()).hexdigest()==OBS_SHA,'Web observation projection changed');obs=json.loads(OBS.read_text(encoding='utf-8'))
    for a in obs['failed_HTTP_raw_attempts']:need(hashlib.sha256(Path(a['cache_path']).read_bytes()).hexdigest()==a['raw_sha256']and not a['body_adopted'],'Failed direct HTTP promoted')
    need(hashlib.sha256(CHI_ORDER.read_bytes()).hexdigest()==CHI_ORDER_SHA,'Chicago originalorder raw changed')
    cd=fitz.open(CHI_ORDER);ct=[p.get_text().replace('\r\n','\n').replace('\r','\n')for p in cd]
    need(len(ct)==4 and 'First Amended and Re-issued'in ct[0]and 'January 3, 2022'in ct[0]and 'December'in ct[3]and '30'in ct[3],'Wrong Chicago operative revision')
    need('nonresident professional athlete'in ' '.join(ct[2].split()).lower()and 'regular employment'in ct[2]and 'competition'in ct[2],'Chicago visitor employment exception absent')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_frozen_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_original_rows':rows},'web_observations_not_raw_article':{'cache_path':str(OBS),'raw_sha256':OBS_SHA,'projection':obs},'Chicago_operative_primary_order':{'cache_path':str(CHI_ORDER),'raw_sha256':CHI_ORDER_SHA,'archive_url':'https://web.archive.org/web/20220106014725if_/https://www.chicago.gov/content/dam/city/sites/covid/health-orders/Health%20Order%202021-2_12-30-21_FINAL.pdf','issued':'2021-12-30','effective':'2022-01-03','exception':'section5(3):nonresidentprofessionalathlete regular employmentcompetition','normalized_fitz_page_sha256':{str(i+1):hashlib.sha256(t.encode()).hexdigest()for i,t in enumerate(ct)},'January26_revision_not_used':True}}

def contracts():
    x=[{'player':p,'route':'RETAIN_CURRENT_UPC','old_Gamma_preserved':True}for p in LIVE]
    x.extend({'player':p,'route':'NEW_OWN_FA','price_function':deepcopy(q),'old_Gamma_preserved':True}for p,q in PRICES.items())
    x.extend({'player':p,'route':'VII6i_MINIMUM','seasons':1,'salary':'applicable2021Minimum(YOS)','new_bonus':0,'full_standard_protection':True,'old_Gamma_preserved':True}for p in MINIMUM)
    x.append({'player':'Cameron Thomas','route':'VII6h_VIII1_RSC','pick':27,'holder':'BKN','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None})
    return x

def assert_contracts(rows):
    need(POLICY==POLICY_FIXED and PRICES==PRICES_FIXED,'Selected fixed contract/policy changed')
    need(len(rows)==15 and len({x['player']for x in rows})==15,'15 lawful UPC identities lost')
    for r in rows:
        p=r['player']
        if p in LIVE:need(r=={'player':p,'route':'RETAIN_CURRENT_UPC','old_Gamma_preserved':True},'Retained current obligations altered')
        elif p in PRICES_FIXED:need(r=={'player':p,'route':'NEW_OWN_FA','price_function':PRICES_FIXED[p],'old_Gamma_preserved':True},'Returned FA class/price/exception altered')
        elif p in MINIMUM:need(r=={'player':p,'route':'VII6i_MINIMUM','seasons':1,'salary':'applicable2021Minimum(YOS)','new_bonus':0,'full_standard_protection':True,'old_Gamma_preserved':True},'Minimum law altered')
        else:need(r=={'player':'Cameron Thomas','route':'VII6h_VIII1_RSC','pick':27,'holder':'BKN','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None},'RSC identity altered')

def role_blocks(state):
    rem={r:{p:m//2 for p,m in ps.items()}for r,ps in ROLE_MINUTES[state].items()};roles=list(rem);out=[]
    for i in range(24):
        if i==0:a=deepcopy(STARTERS)
        else:
            total=Counter()
            for ps in rem.values():total.update(ps)
            forced={p for p,v in total.items()if v==24-i}
            def find(k,a):
                if k==5:return a if forced<=set(a.values())else None
                r=roles[k]
                for p in sorted(rem[r],key=lambda p:(p not in forced,-rem[r][p],p)):
                    if rem[r][p]>0 and p not in a.values():
                        b=find(k+1,{**a,r:p})
                        if b:return b
                return None
            a=find(0,{})
        need(a is not None,'Chosen role matching unavailable')
        for r,p in a.items():need(rem[r].get(p,0)>0,'Role remainder invalid');rem[r][p]-=1
        out.append({'start_second':i*120,'end_second':(i+1)*120,'seconds':120,'positions':a})
    need(all(v==0 for ps in rem.values()for v in ps.values()),'240minute role capacity incomplete');return out

def assert_role_blocks(state,blocks):
    need(ROLE_MINUTES==ROLE_FIXED,'Chosen role source changed');sums={r:Counter()for r in ROLE_FIXED[state]};end=0
    for b in blocks:
        need(b['start_second']==end and b['end_second']-end==b['seconds']==120,'Chosen clock changed');pos=b['positions']
        need(set(pos)==set(sums)and len(set(pos.values()))==5,'Five distinct roles lost')
        for r,p in pos.items():need(p in ROLE_FIXED[state][r],'Player outside chosen natural role');sums[r][p]+=120
        end=b['end_second']
    need(end==2880 and blocks[0]['positions']==STARTERS,'Starters/clock changed')
    need(all(dict(ps)=={p:m*60 for p,m in ROLE_FIXED[state][r].items()}for r,ps in sums.items()),'Role minute budget changed')
    need(hashlib.sha256(json.dumps(blocks,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==ROLE_SEQUENCE_SHAS[state],'Returned selected chronology altered')
    return Counter({p:sum(ps[p]for ps in sums.values())for p in set().union(*(set(ps)for ps in sums.values()))})

def build(root=ROOT):
    src=sources(root)
    for p,h in PINS.items():need(sha(root/p)==h and src[p]==direct_physical(root,p),'Returned physical source differs '+p)
    need(sha(root/PREFIX)==PREFIX_PIN,'Reviewed source price/retained Gamma changed');prefix=physical(root,PREFIX)
    need(prefix==direct_physical(root,PREFIX),'Returned retained cost source differs')
    need(prefix['BKN']['core_normal']==156210940 and prefix['BKN']['retained_unlikely_preserved']==1187500 and prefix['policy']['new_Patty_TaxpayerMLE_first_year']==5890000,'Admitted public current lower/TMLE template changed')
    need(prefix['BKN']['core_normal']>143002000,'No source lower witness for TMLE aboveapron eligibility')
    need(src[PRICE]['price_comparators']['reported_first_base']==17142857 and src[PRICE]['price_comparators']['reported_option_not_exercised']==12302496,'Dinwiddie reported price comparison changed')
    need(all(0<q['flat_first_base_interval'][0]<=q['flat_first_base_interval'][1]<Fraction(112414000,4)for q in PRICES.values()),'Named price intervals exceed applicable25percent maximum lower bound')
    need(PRICES['Jeff Green']['flat_first_base_interval'][1]<=5890000 and PRICES['Jeff Green']['seasons']<=3,'TMLE first use/term limit failed')
    raw=support();rows=contracts();assert_contracts(rows);seed=src[CAPACITY]['team_functions']['BKN'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'Mike James'}|{'Cameron Thomas'})
    need(set(standard)=={r['player']for r in rows},'Current seed/MikeJames/RSC identity mismatch')
    picks=[x for x in src[DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='BKN'];need([(x['pick'],x['player'])for x in picks]==[(27,'Cameron Thomas'),(43,'Isaiah Todd'),(51,'Marcus Zegarowski'),(59,'RaiQuan Gray')]and all(x['lawful_PS21_participant_model_selected']for x in picks),'BKN selected rights changed')
    states={};prepared=[];names=set()
    for state in ROLE_FIXED:
        blocks=role_blocks(state);seconds=assert_role_blocks(state,blocks);active=sorted(set(seconds)|{'Cameron Thomas','Alize Johnson'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated nomination identity changed')
        states[state]={'blocks':blocks,'player_seconds':dict(seconds),'active':active,'inactive':inactive,'positive_availability_selected':True,'unused_zero_clinical_status':None}
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='BKN'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Calendar/current CHI state mismatch')
        state='IRVING_AWAY_RETURN'if gid=='0022100625'else'IRVING_INSTITUTIONAL_OUT'
        if state=='IRVING_AWAY_RETURN':need(g['date']=='2022-01-12'and g['away']=='BKN'and g['home']=='CHI','Chicago visitor policy applied outside selected date')
        r=states[state];need(('Kyrie Irving'in r['player_seconds'])==(state=='IRVING_AWAY_RETURN'),'Institutional nonparticipant returned positive')
        c=next(x for x in src[CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'CHI selected health/minutes changed')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['BKN']=joint.pop('NYK')
        for x in pair:x['BKN']=x.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        for t in joint:names.update(joint[t])
        prepared.append((g,h,state,pair,joint))
    need(src[AUTH]['selected']['selected_date_rows']['sha256']==PINS[HEALTH],'CHI current authority changed')
    aliases={'Nicolas Claxton':'Nic Claxton','Coby':'Coby White'};rates=det.expected_ratings({det.BPM:src[det.BPM]},{aliases.get(p,p)for p in names})
    for p,q in aliases.items():
        if p in names:rates[p]=rates.pop(q)
    need(next(x for x in src[det.BPM]if x['nba_player']=='Nic Claxton')['archive_player']=='Nicolas Claxton','Source Claxton identity alias changed')
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared single BPM selected model changed')
    games=[]
    for g,h,state,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['BKN'])-int(back['CHI']));margin=impact['CHI']-impact['BKN']+home+fatigue;need(margin!=0,'Tie requires separate overtime choice')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'BKN_state':state,'BKN_active':states[state]['active'],'BKN_inactive':states[state]['inactive'],'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_BKN_impact_fraction':str(margin),'CHI_minus_BKN_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'BKN','score':None,'overtime_selection':None})
    feed=json.loads(base.FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows'];events=[{'GroupSort':x['GroupSort'],'date':x['TRANSACTION_DATE'][:10],'player':x['PLAYER_SLUG'],'description':x['TRANSACTION_DESCRIPTION'],'applied_to_selected_family':False}for x in feed if x['TEAM_ID']==1610612751 and '2021-07-29'<=x['TRANSACTION_DATE'][:10]<='2022-01-12']
    return {'id':'CHICAGO_BROOKLYN_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_THREE_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,PREFIX:PREFIX_PIN,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,
      'selected_registration':{'standard':standard,'TW':[],'STD':15,'TW_count':0,'MikeJames_expiry_or_nonassignment_waiver_full_currentprotectedGamma_retained':True,'ChrisChiozza':'two consecutive same-team one-yearTW→STANDARDQO validoperative2021 delivery, unaccepted/unextendedOct1; no newUPC, FA/FRN claims retained','ReggiePerry':'one-yearTW→TWQO ifotherwiseeligible, validoperative2021 delivery, unaccepted/unextendedOct1; no newUPC, applicableFA/FRN claims retained','unsigned_second_round':'43Todd/51Zegarowski/59Gray validoperativeW21 firstRT YOS0min/one-year, unaccepteduntilatleastOct15, UPC0/STD0; lateravailability/foreignnotice reopens','exact_private_amounts_or_actual_acceptance':None},
      'selected_role_states':states,'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_ratings':rates,'selected_games':games,
      'institutional_participation':{'original_Nets_no_part_time_policy_preserved_in_first_two_working_dates':True,'January12_new_road_only_policy_selected':True,'Chicago_nonresident_regular_employment_competition_condition_selected':True,'Chicago_January26_revision_retroactive_claim':False,'NYC_home_team_not_visiting_exempt':True,'actual_vaccination_testing_or_clinical_receipt_certified':False,'Dinwiddie':{'original_ACL_injury_not_erased_as_history':True,'fictional_rehabilitation_operative_availability_selected_firsttwo':True,'Jan12_zero_is_rotation_reserve_not_new_injury':True},'other_positive_dated_health':'Working operational availability, not original infections/protocols or NBA medical facts copied.'},
      'public_cost_family':{'retained_core_reported_normal_template_lower':156210940,'apron2021':143002000,'positive_lower_margin_for_TMLE_before_new_nonnegative_costs':13208940,'JeffGreen_new_TMLE_upper':5200000,'TMLE_limit':5890000,'unused_capacity_lower':690000,'other_new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'whole_private_team_salary_actual':None,'public_template_is_not_actual_contract_cent_certificate':True},
      'six_cost_categories':{'live':'All8 currentGamma retained; six new ownFA exception/min contracts and27RSC. No protected/bonus current cost removed. Newpricefunctions are fictional offer family not receipts.','waived_former':'MikeJames ROSexpiration/conditionalwaiver and allpast earned/protected/camp/stretchGamma retained, no current owed zero claim.','FA_holds':'OwnFA lawful UPC replacement only; Chiozza/Perry QO/FRN and oldunsigned holdings preserved; not blanket FA renunciation.','unsigned':'27RSC firsthold replaced only onvalidUPC;3secondRT/minimumyoungFAfloors preserved withoutSTD. OlderadmittedrightGamma kept.','unused_exceptions':'OnlyJeffTMLE new use, remaining690k-or-more reservation preserved, allotherunexpiredTPE/exceptionnormal amounts retained withstatutoryapron exclusions.','incomplete':'At everyprefix max(0,12−lawfulcapcount)*YOS0min; final15registered means0bycount.'},
      'butterfly_handoff':['NoP1 DinwiddieWAS/Fiveway orJordanDET/cash4second assignment copied; unchanged conditionalpriorholders retained, no newTPE fromomittedmoves.','No ShametPHX/SharpeCarterdrafttrade/MillsBembryAldridgeMillsapnewUPC copied; JeffBKNretained and Thomas27onlysigned; noSixtyrookies automaticUPC.','NoHardenPHI/SimmonsBKN/DrummondCurryBKNfuturetrade inherited; actual star extensions remainlaterchoice; current UPC unchanged.','FirsttwoKyrie0 is institution/team policy, January12positive is roadpolicy/legalvisitor/fictionavailability; sourceCOVIDpositive/protocols are not copied.'],
      'original_reported_events_not_applied':events,'summary':{'selected_games':3,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'BKN_wins':sum(g['selected_regulation_winner']=='BKN'for g in games),'STD':15,'TW':0,'active_each':12,'positive_each':10,'role_states':2,'blocks_each':24,'paired_seconds_each':2880,'player_seconds_each':14400},
      'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_salary_private_receipt_or_clinical_certificate':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    lines=['# Brooklyn keeper 법적 가족·세 날짜 작업 결과','','**선택된 가상 NPC 가족·독립 검문 대기.**','','|날짜|키|BKN상태|CHI상태|작업승자|CHI영향/100|','|---|---|---|---|---|---|']
    for g in d['selected_games']:lines.append(f"|{g['date']}|{g['game_id']}|{g['BKN_state']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_BKN_impact_per100']:.9f}|")
    lines+=['','May16의15명에서 MikeJames ROS만료 또는 비양도방출의 보호Γ를 남기고 Thomas27 RSC를 넣는다. 원live8+BrownFullBird2년5–6m/DinFullBird2년17–18m/JeffTaxpayerMLE2년4.8–5.2m/Griffin·TLC·Tyler1년minimum+Thomas=15STD0TW다. 새계약bonus0·fullprotection·flat급여는 가상동의가족이다. Brown의 원125%/최저+200k/Starter21앵커QO 함수는 새Bird계약 전까지 보존한다. Din의 실제원보고17.142857m는 가격비교이며 실제수락금액이아니다.','',
      'Jeff는1시즌NonBird한계를FullBird로바꾸지않고 새TaxpayerMLE를 사용한다. 검문된 원공개current8 template normal156,210,940은 apron143,002,000보다13,208,940 높다. 모든기존Γ/새비용을삭제하지않는 가족에서 TMLE 사용후 초과 조건이보존된다. 5.2m상단은5.89m TMLE이하이며 남은최소690k를 지운것이 아니다. 새NTMLE/BAE/RoomMLE/수입S&T는없다. 음수apron을위법으로오인하거나 실제whole장부를인증하지않는다.','',
      'Kyrie의 NYC홈경기접근·Nets팀방침·가상임상가용을분리했다. [원Nets10/12팀성명](https://www.nba.com/nets/news/2021/10/12/brooklyn-nets-statement)과 원[12월도로복귀보고](https://www.nba.com/news/brooklyn-nets-to-allow-kyrie-irving-to-rejoin-road-games)를 참고해 Nov8부분참여금지/Dec4홈비적격은0, Jan12CHI원정은 새도로참가작업정책과 비거주경쟁목적을 선택한다. 실백신·검사·감염진단으로 승격하지않는다.','',
      '[Chicago2021-2 원공식Jan6아카이브](https://web.archive.org/web/20220106014725if_/https://www.chicago.gov/content/dam/city/sites/covid/health-orders/Health%20Order%202021-2_12-30-21_FINAL.pdf)의 Issued12/30·Jan3시행·§5(3) 비거주직업선수 경쟁목적예외를 actualPDF4쪽/rawSHA로핀했다. Jan26개정소급0. 직접실패HTTP와 성공웹본문관측을 구분한다. NYC홈팀을 방문선수로 위장하지않는다.','',
      'usual5 Harden/Harris/Brown/Durant/Claxton. 첫2일 Harden32/Din16/Harris30/Shamet30/Durant34/Brown18/Green18/Griffin20/Claxton28/Jordan14=240. Jan12는Din16+Shamet16을Kyrie32로교체해240. 각상태24개2분블록을 currentM1 Mark32/Caruso18/P32·위임CHI상태와 초별조인한다. 골대·포지션·quarter·active12를검문하며 공통Jordan48 수학표를 실행으로읽지않는다. 단일March25 EB/BPM·홈2·연전.5만사용; score/OTnull이다.','',
      'P1/DinWAS/Fiveway/JordanDET와현금4second는미선택으로유지한다. 기존계약/권리흐름을 새ThomasUPC와혼동하지않는다. Todd43/Zegarowski51/Gray59 미수락RT는NBA슬롯0. Chiozza동일팀연속2TW의STANDARDQO와Perry1TW의TWQO를구분하고 유효미수락Oct1뒤FRN/FA비용을남긴다. 기존TPE·보호·pastdead·camp·stretch·FAhold·초기12capcount예약Γ를없애지않는다.','',
      '## 7행 진행','','|번호|작업|현황|','|---|---|---|','|1|2020드래프트연쇄|완료|','|2|Chicago2020–21|완료|','|3|2021–23|BKN1가족·3날짜 작업결과 선택/독립검문 대기|','|4|장기커리어|미완|','|5|결말·구조|미완|','|6|집필규격·Pack|현행기능등록기 참조·Pack0|','|7|통합·최종승인|CLOSED|','',
      '[현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 미완료큰묶음5·6번까지4. v0.30 PARTIAL/CLOSED/원고0. 작성자검사를 독립검문으로 계수하지않는다. whole82/wholemacro3/실제사적기관수락은false.','']
    return '\n'.join(lines)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved BKN family differs from source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]

def self_test():
    out=[];old=contracts
    def wrongroute():
        x=old();next(r for r in x if r['player']=='Jeff Green')['price_function']['route']='VII6e_NON_TAXPAYER_MLE';return x
    with patch(__name__+'.contracts',wrongroute):
        try:build()
        except ValueError:out.append('RETURNED_TMLE_TO_HARDCAP_NTMLE')
        else:raise AssertionError('FalsePASS exception')
    rb=role_blocks
    def wrongorder(state):
        x=rb(state);i,j=next((i,j)for i in range(1,24)for j in range(i+1,24)if i//6==j//6 and x[i]['positions']!=x[j]['positions']);x[i]['positions'],x[j]['positions']=x[j]['positions'],x[i]['positions'];return x
    with patch(__name__+'.role_blocks',wrongorder):
        try:build()
        except ValueError:out.append('RETURNED_SELECTED_SAME_TOTAL_CHRONOLOGY')
        else:raise AssertionError('FalsePASS roleorder')
    loader=physical
    def wrongbpm(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Nic Claxton')['bpm']='20.8'
        return x
    with patch(__name__+'.physical',wrongbpm):
        try:build()
        except ValueError:out.append('RETURNED_PHYSICAL_CLAXTON_BPM')
        else:raise AssertionError('FalsePASS physical BPM')
    return out

def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(physical(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'BKN source currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'results':[{k:g[k]for k in('game_id','date','CHI_state','BKN_state','selected_regulation_winner','CHI_minus_BKN_impact_per100')}for g in d['selected_games']],'writer_negative_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
