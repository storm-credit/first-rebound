"""A source-supported PHI keeper family and four delegated working results."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from datetime import date,timedelta
from unittest.mock import patch
import argparse,hashlib,json
import fitz
import build_nyk_2021_keeper_and_chicago_selected_results as base
import build_chicago_detroit_2021_two_date_selected_bpm_results as det
ROOT=Path(__file__).resolve().parents[1];SELF='tools/build_phi_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_PHILADELPHIA_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='372ea5577230f22ac07d6d5f2a268f883918f837'
PLAYOFF='simulation/NBA_2021_DELEGATED_PLAYOFF_RESULTS.json'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397',PLAYOFF:'dc1d47563f8381a4b1bd98409f198e8df088ce782622071e22556e8f0c7a7cdb'}
COMPLETED_RESULT_PINS={'simulation/CHICAGO_TORONTO_2021_22_SELECTED_BPM_RESULTS_2026_10_07.json': '333f5bd496ed59260d21e26bb42615b13cb0a11560409a798c9f905cfe66dac6', 'simulation/CHICAGO_NEW_ORLEANS_2021_SELECTED_KEEPER_RESULT.json': 'd1975077c8879807d63763d77d58a2d89f8b481ec6c2964f0a6a9bf7a96138fd', 'simulation/CHICAGO_NEW_YORK_2021_22_SELECTED_KEEPER_RESULTS.json': '4ad346a5f58bbf125c7378cd6ac5fc1f347a8a5bfccb2ed70f6fe9df0bf6831f', 'simulation/CHICAGO_UTAH_2021_SELECTED_KEEPER_RESULT.json': '0e2bb3a05a9e562872dcdb411f061693d55d8bfa408a9f8c7927a1a65eb8fc77', 'simulation/CHICAGO_BOSTON_2021_22_SELECTED_KEEPER_RESULTS.json': '62dc644588257b0330e14aee478f6d4e37b1a127addadbfeb0415113199f23c1'}
PINS.update(COMPLETED_RESULT_PINS)
need=base.need;sha=base.sha;physical=base.physical;text=base.text
CAPACITY=base.CAPACITY;CHI=base.CHI;ROSTER=base.ROSTER;DRAFT=base.DRAFT;HEALTH=base.HEALTH;AUTH=base.AUTH
IDS=('0022100111','0022100135','0022100802','0022100969')
LIVE=('Ben Simmons','George Hill','Isaiah Joe','Joel Embiid','Matisse Thybulle','Paul Reed','Seth Curry','Shake Milton','Tobias Harris','Tyrese Maxey')
MINIMUM=('Dwight Howard','Mike Scott')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-phi-keeper-20261007/observed_profile.json')
PROFILE_SHA='9f854e6692e65b87e68ce17dcee77ce79ec9fccb649b31cad695ab0d50eaa7ee'
ROLE_MINUTES={'PG':{'Ben Simmons':20,'Tyrese Maxey':22,'Shake Milton':6},
 'SG':{'Seth Curry':30,'Shake Milton':12,'Furkan Korkmaz':6},
 'SF':{'Danny Green':24,'Matisse Thybulle':16,'Furkan Korkmaz':8},
 'PF':{'Tobias Harris':32,'Ben Simmons':12,'Mike Scott':4},
 'C':{'Joel Embiid':34,'Dwight Howard':14}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Ben Simmons','SG':'Seth Curry','SF':'Danny Green','PF':'Tobias Harris','C':'Joel Embiid'}
PRICES={'Danny Green':{'route':'VII6b3_EARLY_BIRD','seasons':2,'nonoption_seasons':2,'first_base_floor':'max(legalMin2021(YOS),signed2021Year2Min(YOS+1))',
 'first_base_ceiling':'min(II7max,max(7/4*priorRegularSalary,21/20*priorAveragePlayerSalary))','later_base':'same_first_base','new_bonus':0,'full_standard_protection':True},
 'Furkan Korkmaz':{'route':'VII6b1_FULL_BIRD','seasons':2,'nonoption_seasons':2,'first_base_floor':'max(legalMin2021(YOS),signed2021Year2Min(YOS+1))',
 'first_base_ceiling':'ArticleII7_applicable_first_year_maximum','later_base':'same_first_base','new_bonus':0,'full_standard_protection':True,
 'VII6m4_current_applicability':'No:2021FA follows2019nonRSCstandardcontract, notsecond/thirdseasonofRSC. Original2019postoptioncontractceiling retained in oldGamma.'}}
PRICES_FIXED=deepcopy(PRICES)
POLICY={'new_UPCs_ET':'2021-08-06T12:02:00_ORDERED','Tolliver_exit':'legalexpirationROS or valid nonassignmentwaiver iflive; oldcurrentprotectedGamma remains',
 'new_NTMLE_BAE_incoming_SandT':False,'new_trade':False,'new_TW_UPCs':False,
 'Simmons_working_relationship':'PreservePHI3–4ATLexit; select consensualcoach/teammate offseason role discussion and campreturn, fullcurrentcontractretained, 32minutes atfourdates; not originalincident/holdout/privateclinical diagnosis.',
 'four_date_positive11_operational_availability_selected':True,'real_medical_or_private_receipts_certified':False}
POLICY_FIXED=deepcopy(POLICY)

def sources(root):return {p:physical(root,p)for p in PINS}

def support():
    need(hashlib.sha256(base.CBA.read_bytes()).hexdigest()==base.CBA_SHA,'CBA raw changed')
    d=fitz.open(base.CBA);pages=(26,29,30,54,55,58,209,210,212,222,223,224,227,228,232,233,240,241,294,303,311,312,317,318,561)
    tx={n:d[n-1].get_text().replace('\r\n','\n').replace('\r','\n')for n in pages};flat=lambda n:' '.join(tx[n].split())
    need('two (2) preceding Seasons'in flat(26)and 'three (3) preceding Seasons'in flat(29),'Veterancontinuity source absent')
    need('seventy-five percent (175%)'in flat(224)and 'at least two (2) Seasons'in flat(223),'EarlyBird price/term absent')
    need('following the second or third Season of his Rookie Scale Contract'in flat(241),'DeclinedRSC ceiling scope absent')
    need('Minimum Player Salary Exception'in flat(233)and 'first Season covered by the player’s Contract'in flat(55),'Minimum/source scale absent')
    need(hashlib.sha256(base.FEED.read_bytes()).hexdigest()==base.FEED_SHA,'Frozen feed changed')
    feed=json.loads(base.FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    gs={'Trade 2020022':'danny-green','Signing 1019294':'furkan-korkmaz','Signing 989371':'furkan-korkmaz','Signing 1019096':'mike-scott','Signing 1033131':'dwight-howard','Signing 1039698':'anthony-tolliver','Trade 2020068':'george-hill','Signing 1039938':'gary-clark','Signing 1036470':'rayjon-tucker'}
    rows=[x for x in feed if x['TEAM_ID']==1610612755 and x['GroupSort']in gs and x['PLAYER_SLUG']==gs[x['GroupSort']]]
    need(len(rows)==len(gs),'Original continuity/live/expired source actors absent')
    need(hashlib.sha256(PROFILE.read_bytes()).hexdigest()==PROFILE_SHA,'Profile observation changed');obs=json.loads(PROFILE.read_text(encoding='utf-8'));http=obs['direct_HTTP']
    need(hashlib.sha256(Path(http['cache_path']).read_bytes()).hexdigest()==http['raw_sha256']and not http['adopted_primary_body'],'Failed profile HTTP promoted')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},
      'frozen_NBA_movement':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_original_anchors':rows},
      'NBA_profile_web_observation':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs,'direct403body_evidence':False},
      'class_continuity':'Green2019LALcontract→tradeonlyOKC→2020DecPHI, two precedingseasons EarlyBird. Korkmaz2017RSC→2019newstandard→2021FA; continuous2018–19/2019–20/2020–21 supportsFullBird; VII6m4 original2019ceiling not retroactively erased, current2021nonRSCexpiration distinguished.'}

def contracts():
    rows=[{'player':p,'route':'VII6a_EXISTING','new_UPC':False,'old_Gamma_preserved':True,'valid_current_term_to_March7':True,'actual_receipt':None}for p in LIVE]
    rows +=[{'player':p,'route':PRICES[p]['route'],'new_UPC':True,'price_function':deepcopy(PRICES[p]),'old_Gamma_preserved':True,'actual_price':None,'actual_receipt':None}for p in PRICES]
    rows +=[{'player':p,'route':'VII6i_MINIMUM','term':1,'salary':'applicable2021Minimum(YOS)','new_bonus':0,'full_standard_protection':True,'old_Gamma_preserved':True,'actual_receipt':None}for p in MINIMUM]
    rows.append({'player':'Jaden Springer','route':'VII6h_VIII1_RSC','pick':28,'holder':'PHI','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None,'actual_receipt':None})
    return rows

def assert_contracts(rows):
    need(PRICES==PRICES_FIXED and POLICY==POLICY_FIXED,'Fixed lawful family policy altered')
    need(len(rows)==15 and {r['player']for r in rows}==set(LIVE+MINIMUM+tuple(PRICES)+('Jaden Springer',)),'Keeper contract15 identities changed')
    for r in rows:
        p=r['player'];need(r['actual_receipt']is None,'Real institutionreceipt promoted')
        if p in LIVE:need(r['route']=='VII6a_EXISTING'and not r['new_UPC']and r['old_Gamma_preserved']and r['valid_current_term_to_March7'],'Existingoldobligation dropped')
        elif p in PRICES:need(r['route']==PRICES_FIXED[p]['route']and r['price_function']==PRICES_FIXED[p]and r['new_UPC']and r['old_Gamma_preserved']and r['actual_price']is None,'Returned FAclass/pricefunction altered')
        elif p in MINIMUM:need(r['route']=='VII6i_MINIMUM'and r['term']==1 and r['salary']=='applicable2021Minimum(YOS)'and r['new_bonus']==0 and r['full_standard_protection']and r['old_Gamma_preserved'],'Minimum UPC law altered')
        else:need(r['route']=='VII6h_VIII1_RSC'and r['pick']==28 and r['holder']=='PHI'and r['component_scale']==['4/5','6/5']and r['salary_including_unlikely_ceiling']=='6/5'and r['base_and_protection_floor']=='4/5'and r['guaranteed']==2 and r['options']==2 and r['valid_first_RT_before_UPC']and r['actual_price']is None,'Springer entitlement/UPC altered')

def role_blocks():
    rem={r:{p:m//2 for p,m in ps.items()}for r,ps in ROLE_MINUTES.items()};roles=list(rem);out=[]
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
        need(a is not None,'Selected coach matching unavailable')
        for r,p in a.items():need(rem[r].get(p,0)>0,'Coach role leftover invalid');rem[r][p]-=1
        out.append({'start_second':i*120,'end_second':(i+1)*120,'seconds':120,'positions':a})
    need(all(v==0 for ps in rem.values()for v in ps.values()),'240minute demand uncovered');return out

def assert_roles(blocks):
    need(ROLE_MINUTES==ROLE_FIXED,'Fixed roles changed');sums={r:Counter()for r in ROLE_FIXED};end=0
    for b in blocks:
        need(b['start_second']==end and b['end_second']-end==b['seconds']==120,'Roleclock changed');pos=b['positions']
        need(set(pos)==set(ROLE_FIXED)and len(set(pos.values()))==5,'Role fiveuniqueness lost')
        for r,p in pos.items():need(p in ROLE_FIXED[r],'Player outside selected role');sums[r][p]+=120
        end=b['end_second']
    need(end==2880 and blocks[0]['positions']==STARTERS,'Usualstarters/clock changed')
    need(all(dict(ps)=={p:m*60 for p,m in ROLE_FIXED[r].items()}for r,ps in sums.items()),'Selectedrole minute function changed')
    # A literal semantic pin is filled from this initial explicit chosen plan.
    need(hashlib.sha256(json.dumps(blocks,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==ROLE_SEQUENCE_SHA,'Returned chosen sequence differs from fixed selection')
    return Counter({p:sum(ps[p]for ps in sums.values())for p in set().union(*(set(ps)for ps in sums.values()))})
ROLE_SEQUENCE_SHA='6ea1ddf6951a3413473f82c6c2360ab8b5cb3a467cfcf5d6c60b9dbee06295ea'



def build(root=ROOT):
    src=sources(root)
    for p,h in PINS.items():need(sha(root/p)==h and src[p]==physical(root,p),'Returned physical source differs '+p)
    raw=support();rows=contracts();assert_contracts(rows);n=src[CAPACITY]['team_functions']['PHI']
    old=set(n['standard_named_continuation_condition_max15']);standard=sorted(old-{'Anthony Tolliver'}|{'Jaden Springer'})
    need(set(standard)=={r['player']for r in rows},'Selectedseed/Tolliver/Springer roster join changed')
    picked=[x for x in src[DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='PHI'];need([(x['pick'],x['player'])for x in picked]==[(28,'Jaden Springer'),(50,'Charles Bassey')]and all(x['lawful_PS21_participant_model_selected']for x in picked),'Selected PHI draft rights changed')
    series={x['id']:x for x in src[PLAYOFF]['series']};need(series['E1']['teams']==['PHI','IND']and series['E1']['winner']=='PHI'and series['E5']['teams']==['PHI','ATL']and series['E5']['winner']=='ATL'and series['E5']['loser_wins']==3 and 'no automatic original Simmons/Young scenes'in series['E5']['reason'],'Preserved playoff relationship precursor changed')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds)|{'Jaden Springer'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Nominated identity changed')
    prepared=[];names=set(seconds)
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='PHI'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Four dated source identities changed')
        c=next(x for x in src[CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health/minutes changed')
        role={'blocks':blocks,'player_seconds':dict(seconds)};pair=base.paired(c,role);joint=base.assert_pair(c,role,pair);joint['PHI']=joint.pop('NYK')
        for x in pair:x['PHI']=x.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        names.update(joint['CHI']);prepared.append((g,h,pair,joint))
    need(src[AUTH]['selected']['selected_date_rows']['sha256']==PINS[HEALTH],'CHIcurrentauthority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby'}|({'Coby White'}if 'Coby'in names else set()))
    if 'Coby'in names:rates['Coby']=rates.pop('Coby White')
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'SharedsingleBPM model changed')
    games=[]
    for g,h,pair,joint in prepared:
        impacts={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['PHI'])-int(back['CHI']));m=impacts['CHI']-impacts['PHI']+home+fatigue;need(m!=0,'Tie requires new overtime model')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impacts.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_PHI_impact_fraction':str(m),'CHI_minus_PHI_impact_per100':float(m),'selected_regulation_winner':'CHI'if m>0 else'PHI','score':None,'overtime_selection':None})
    feed=json.loads(base.FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows'];events=[{'GroupSort':x['GroupSort'],'date':x['TRANSACTION_DATE'][:10],'player':x['PLAYER_SLUG'],'description':x['TRANSACTION_DESCRIPTION'],'applied_to_selected_family':False}for x in feed if x['TEAM_ID']==1610612755 and '2021-07-29'<=x['TRANSACTION_DATE'][:10]<='2022-03-07']
    completed_rows=list(src[det.OUT]['rows'])
    for p in COMPLETED_RESULT_PINS:
        d=src[p]
        completed_rows.extend(d['selected_games'] if 'selected_games'in d else d['rows'] if 'rows'in d else [d['selected_result']]if 'selected_result'in d else [d['selected_game']])
    completed={g['game_id']for g in completed_rows};need(len(completed)==15 and len(completed_rows)==15,'Preceding selected15 key join changed')
    selected_keys=completed|set(IDS);need(len(selected_keys)==19,'PHI fourkeys duplicate completed inputs')
    following=next(x for x in sorted(src[det.CAL],key=lambda x:int(x['game_number']))if x['game_id']not in selected_keys)
    need(following['game_id']=='0022100148'and following['opponent']=='BKN'and following['date']=='2021-11-08','Next unresolved physicalcalendar key changed')
    return {'id':'CHICAGO_PHILADELPHIA_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_FAMILY_AND_FOUR_REGULATION_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,
      'selected_registration':{'standard':standard,'TW':[],'active':active,'inactive':inactive,'positive11_operational_availability_selected':True,'zero_unused_clinical_status':None,'STD':15,'TW_count':0,'Tolliver_original_currentprotectedGamma_retained':True,
        'GaryClark':'originalTWexpired, no newUPC, applicableFAhold/priorprotectedGamma kept','RayjonTucker':'validoperative2021TWQO unaccepted/unextendedOctober1 acceptanceend, FRN/FAclaims retained; no newUPC',
        'Bassey50':'validoperativeW21 one-yearlegalYOS0min firstRT, unaccepteduntilatleastOct15, UPC0/STD0; laterdraft/foreignnotice boundaries reopen'},
      'Simmons_causality_and_availability':{'source_E1':series['E1'],'source_E5':series['E5'],'original_specific_pass_coach_quote_media_holdout_not_inherited':True,
        'selected_fictional_summer_relationship_repair':'Coach/teammates and Simmons agree an on-ball facilitation/defensive role and campreturn while keeping currentUPC; 32minutes at four dates including12PF, no originalpublicincident copied.',
        'actual_mental_health_diagnosis_or_private_party_acceptance_certified':False,'new_institutional_actual_acceptance':None,'fourdate32minuteavailability_selected_as_NPC_working_model':True,'all_future_health_or_Harden_trade_selected':False},
      'selected_PHI_role_blocks':blocks,'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_ratings':rates,'selected_games':games,
      'six_cost_categories':{'live':'Retained10 currentlawfulterms/currentGamma plus GreenEarly2/KorkmazFullBird2/HowardScottminimum1/SpringerRSC. Priorbonuses/protection retained, newUPCs bonus0.',
        'waived_former':'Tolliver protectedcurrent costs retained whetherROSexpiration or validwaiver; allpast salary-year/stretchedGamma kept.',
        'FA_holds':'SignedFA statutoryreplacement only, expiredClark/Tucker applicableFA/QO/FRN claims retained, no arbitrary0/fullrenunciation.',
        'unsigned':'Springer28 unsigned120% firsthold untilsignedRSC, Bassey50 validunacceptedRT/minimumyoungFAfloor, olderadmittedrights preserved; UPC not forced.',
        'unused_exceptions':'InheritedTPE/MLE/BAE lawfulnormal/apron amounts retained; new2021NTMLE/BAE/incomingSandT0, no currenttrade/no hardcap trigger invented.',
        'incomplete':'Eachprefix max(0,12−lawfulcapcount)*YOS0min, live15final means0bycount.'},
      'cap_admissibility':{'all_new_UPCs_use_named_lawful_cap_exception_family':True,'new2021_hardcap_trigger_count':0,'whole_private_normal_apron_total':None,'actual_all_other_obligation_absence_certified':False},
      'original_reported_event_controls':events,'butterfly_handoff':['No Simmons/Curry/Drummond/BKN Harden trade automatically applied, no originalmentalhealth/holdoutdiagnosis copied.',
        'Niang retainedUTA so noNiangPHIUPC; Howard/Scott/Hill remain, no originalHowardLAL/HillMIL/Furkan3yr/newDannyactualsalary copied.',
        'Embiidfuture2023extension/newbackupDrummond/currentSpringerBasseyoriginalpick53/Petrusev50 not copied; only currentDB1Springer28/Bassey50 rights consumed.',
        'Fourdates modelNPCretention and positiveavailability; originaltrade/waiver/extension reports enumeratednotabsenceproof. Counterparties need their own lawfuldatedfamily.'],
      'summary':{'selected_games':4,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'PHI_wins':sum(g['selected_regulation_winner']=='PHI'for g in games),'STD':15,'TW':0,'active':12,'positive_PHI':11,'role_blocks':24,'paired_seconds_each':2880,'player_seconds_each':14400},
      'remaining_ports':{'preceding_selected15_keys':sorted(completed),'completed_with_PHI19_keys':sorted(selected_keys),'next_chronological_key':following['game_id'],'date':following['date'],'opponent':following['opponent'],'new_named_legal_family_required_before_result':True},
      'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_salary_private_receipt_or_clinical_certificate':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    lines=['# Philadelphia keeper 가족·Chicago 네 날짜 작업 결과','','**선택된 가상 NPC 법적·관계·감독 가족; 독립 검문 대기.**','','|날짜|키|CHI상태|작업승자|CHI영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:lines.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_PHI_impact_per100']:.9f}|")
    lines+=['','기존PHI10current계약 유지+GreenEarlyBird2년/KorkmazFullBird2년/HowardScott1년minimum/Springer28RSC=15STD0TW다. TolliverROS만료 또는 적법비양도방출의 원current보호Γ를 남긴다. Bassey50은 미수락RT·NBA슬롯0, Clark/Tucker는 새UPC없음·기존FA/보호/QO·FRN비용 보존이다.','',
      'Green2019LAL→OKC→PHItrade만 거친2시즌은 EarlyBird이며 FullBird3으로 복사하지 않았다. Korkmaz2017RSC→2019새nonRSC계약→2021만료의3시즌 연속 가족은 FullBird다. [2017CBA](https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf) VII6(m)(4)의 RSCsecond/third직후미행사option상한을2019가족에서보존하지만 이미새standard계약뒤2021FA에 영구상속하지 않는다. q는올해·signedYear2최저급여 모두이상/법정exception ceiling 이하이며 새bonus0·fullprotection·flat2년이다. 실제q/실수락이 아니다.','',
      'S2 E1 PHI–IND4–1/E5 PHI–ATL3–4를 보존한다. E5 자체가 원Simmons/Young장면자동복사를 금지하므로 원특정패스·coach발언·언론·holdout·정신건강진단을 결과에서 역추론하지 않았다. 여름coach/동료와역할합의·훈련복귀를 가상NPC관계선택으로 명시하고 네날짜32분출전을 작업가용모델로 선택한다. 실제임상/서명인증과 모든미래정신건강·Harden거래는false다.','',
      '새usual5 Simmons/Curry/Green/Harris/Embiid, 240분은 Embiid34/Harris32/Simmons32/Curry30/Green24/Maxey22/Milton18/Thybulle16/Korkmaz14/Howard14/Scott4다. 각48분·포지션·양수11·active11+Springer/inactiveJoeReedHill를 currentM1 Mark32/Caruso18/P32·위임CHI상태와 초별조인한다. 원공통Embiid16/Green48/Korkmaz48 수학표와 원점수·부상·OT를 복사하지 않는다. 단일March25 EB/BPM·홈2·연전.5만 사용했다.','',
      '[NBA당시팀프로필](https://www.nba.com/draft/2021/team-profiles/philadelphia-76ers) 웹본문의 계약/FA 명단과 원동결feed를 분리해 핀했다. directHTTP403은본문인증아니다. live/waivedformer/FA/draftRT/unusedexceptions/incomplete 여섯Γ를 삭제하지 않는다. ownFA/min/RSC외 신규2021하드캡유발행동이없고 whole실제normal/apron총액은null이다. 이예외가족은 비공개전역장부0 증명이 아니다.','',
      'NiangUTA유지·HowardScottHillPHI유지·Simmons/CurryPHI유지 때문에 원이적/Drummond/Harden/Niang영입/Embiid미래연장·원Petrusev50/Bassey53를 자동복사하지 않는다. 원보고event들을적용하지않는작업모델로열거하고 상대팀후손은 별도재개방한다.','',
      '## 7행 진행','','|번호|작업|현황|','|---|---|---|','|1|2020드래프트연쇄|완료|','|2|Chicago2020–21|완료|','|3|2021–23|PHI1가족·4결과 선택/검문대기|','|4|장기커리어|미완|','|5|결말·구조|미완|','|6|집필규격·Pack|현행기능등록기 참조·Pack0|','|7|통합·최종승인|CLOSED|','',
      '[현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 미완료 큰묶음5·6번까지4. v0.30 PARTIAL/CLOSED/원고0. 작성자음성검사는 독립검문으로 계수하지 않는다.','']
    return '\n'.join(lines)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved PHI family differs from source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]

def self_test():
    out=[];old=contracts
    def wrongclass():
        x=old();next(r for r in x if r['player']=='Danny Green')['price_function']['route']='VII6b1_FULL_BIRD';return x
    with patch(__name__+'.contracts',wrongclass):
        try:build()
        except ValueError:out.append('RETURNED_GREEN_EARLY_TO_FULLBIRD_CLASS')
        else:raise AssertionError('FalsePASS class')
    ss=sources
    def wrongscene(root):
        x=ss(root);next(r for r in x[PLAYOFF]['series']if r['id']=='E5')['reason']='COPY_ALL_ORIGINAL_Simmons_INCIDENTS';return x
    with patch(__name__+'.sources',wrongscene):
        try:build()
        except ValueError:out.append('RETURNED_ORIGINAL_INCIDENT_INHERITANCE')
        else:raise AssertionError('FalsePASS causal')
    rb=role_blocks
    def wrongorder():
        x=rb();x[1]['positions'],x[3]['positions']=x[3]['positions'],x[1]['positions'];return x
    with patch(__name__+'.role_blocks',wrongorder):
        try:build()
        except ValueError:out.append('RETURNED_CHOSEN_POSITION_CHRONOLOGY_SWAP')
        else:raise AssertionError('FalsePASS chronology')
    return out

def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(physical(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'PHI source currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'results':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_PHI_impact_per100')}for g in d['selected_games']],'writer_negative_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
