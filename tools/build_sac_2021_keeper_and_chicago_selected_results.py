"""Two selected Sacramento keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_sac_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_SACRAMENTO_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
PINS.update({'research/DETROIT_2021_A_ROUTINE_OPERATING_EXECUTION_FAMILY_2026_10_07.json': '855371610d0f2b776b773bdf2ff02f27a43684b6c1407b1d54f698c6e0f093ef', 'simulation/CHICAGO_INDIANA_2021_22_SELECTED_KEEPER_RESULTS.json': '9e8358e08c41fd7cd99da99dc73618a6d1ed3d92a2de017fbc8aabf70d61965c', 'simulation/CHICAGO_UTAH_2021_SELECTED_KEEPER_RESULT.json': '0e2bb3a05a9e562872dcdb411f061693d55d8bfa408a9f8c7927a1a65eb8fc77'})
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100878','0022101026')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-sac-keeper-20261007/observed_profile.json')
PROFILE_SHA='a767088903fd5810743980a5b720f1ded11851eb30885b96f3d3d0e4ef7ceb79'
LIVE=('Buddy Hield','Chimezie Metu','Damian Jones',"De'Aaron Fox",'Delon Wright','Harrison Barnes',"Jahmi'us Ramsey",'Marvin Bagley III','Robert Woodard II','Tyrese Haliburton')
OPTIONS={}
SECOND=((41,'Neemias Queta'),);SECOND_FIXED=tuple(SECOND)
ROLE_MINUTES={'PG':{"De'Aaron Fox":32,'Tyrese Haliburton':12,'Davion Mitchell':4},'SG':{'Tyrese Haliburton':20,'Buddy Hield':20,'Terence Davis':8},'SF':{'Harrison Barnes':30,'Buddy Hield':8,'Maurice Harkless':10},'PF':{'Marvin Bagley III':24,'Maurice Harkless':10,'Chimezie Metu':14},'C':{'Richaun Holmes':30,'Hassan Whiteside':14,'Damian Jones':4}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':"De'Aaron Fox",'SG':'Tyrese Haliburton','SF':'Harrison Barnes','PF':'Marvin Bagley III','C':'Richaun Holmes'}
ROLE_SHA='a4c9af83766fc3dc852c27f4c8fa2c78e6316c9ad14222fa84b5c9bc58431b0d'
EARLY={'Richaun Holmes':{'original':'2019SACtwoServices','q':[8000000,10000000]},'Terence Davis':{'original':'2019TORtwoServiceSameContract_toSACMarch25_tradeonly','q':[4000000,6000000]}};EARLY_FIXED=deepcopy(EARLY)
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'JustinJames':'lawful nonassignmentwaiver fullcurrentprotectedGamma andallFAclaims retained, not originalsame-datewaiver fact','KyleGuy':'Original2019TW validownQO peractualcontracttype iftwoOneYearSameSACthenSTANDARD, ifoneTwoYearandotherwiseeligibleTWthenTWQO; unaccepted/unextendedOct1/FRN or lawfulconsensualwithdrawal; noUPC/normalFAfloor retained. No sourceproof oftwoseparateoneYearcontracts claimed.','LouisKing':'originalliveTW validterm carry or eligibleownnew1yearTWafteroperativeQO, alloldGamma retained/unusedactive.','availability':'12positive operationalavailable2dates; no actualHaliburtonIND/BagleyDET/Holmesinjury orCOVIDclinicalcopy, clinicalnullzeroreserves.','whole_private_or_actual_receipts':False};POLICY_FIXED=deepcopy(POLICY)

def direct(root,p):
    t=(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
    return json.loads(t)if p.endswith('.json')else list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else t
SOURCE_MEANING_SHA={'simulation/NBA_2021_22_COMMON_26_OPPONENT_CAPACITY.json': '83a8033265a23be22a002465467225c02e20e56482be8703f2e9f0a46fc23805', 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json': '12456392c139ca9dbb71070e0a574d633728691d477eada592fd03cefc535cb9', 'simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json': '353acb80f6b12e4b67e2cc0cf56ab4f6551cc70efb63b20cf9febc9db21f0c33', 'simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json': '426de339ff1a1270eb41ed6b81caee8e10099e55e2176c4e9f31bd196da853d5', 'simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json': 'b42cfb6e0b895fb6a70eb1a9e32798eb0cda27b98a659b6e4e6fce85a7d431f7', 'canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json': '963c5b9d2967f70cf5770349df39f44f88878e4a3e884b7e0c3c103d7699c6be', 'simulation/CHICAGO_2021_22_CALENDAR.csv': '1c6d8cf8284dc3f88c0d6c7a2a7927f6ba0eb756fbf367da2a44fbfb402e7f68', 'simulation/NBA_2021_22_REGULAR_BASELINE.csv': '8d07a7ba2485a7a0fceeeb2ccfff7acfa1db394f4918459ec4fe30caef2bc4e6', 'simulation/CHICAGO_2020_21_BPM_MAR25_SNAPSHOT.csv': '1ef4eee6a701658c28db8fc611cab263ef8f83936b5badceb45415d35323bfd8', 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS.json': '04d2919b0c1525d0c00d40f7974e8fefd41ed931a1a18495f01b99d98270c317', 'tools/build_chicago_detroit_2021_two_date_selected_bpm_results.py': 'ef289a00d1d7394fefdc6c2d82b535c998f87b6978cddf06fd93319967ebc191', 'tools/build_nyk_2021_keeper_and_chicago_selected_results.py': '01c418a67b2345e60944e90fa602f8644d4bbefeb3456a25cbd0600ef53e9194', 'research/DETROIT_2021_A_ROUTINE_OPERATING_EXECUTION_FAMILY_2026_10_07.json': 'f377c94a47f0bed93596fb65f8a24fdc2238a768f3ec3e243f4643cfb07b10b1', 'simulation/CHICAGO_INDIANA_2021_22_SELECTED_KEEPER_RESULTS.json': '9ed2c4959a43a8260cdec47631d0a5b7dd6ff68c24bafc0157223786d5d8bcc2', 'simulation/CHICAGO_UTAH_2021_SELECTED_KEEPER_RESULT.json': '4d0981b4b75a3e18d0611e1b18529460326316ff810f3a37951cbe6f679feb4a'}

def sources(root):return {p:physical(root,p)for p in PINS}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def support():
    need(hashlib.sha256(base.CBA.read_bytes()).hexdigest()==base.CBA_SHA,'CBA raw changed')
    d=fitz.open(base.CBA);pages=(26,29,30,54,55,58,212,222,223,224,233,240,241,294,303,311,312,313,314,317,318,332,333,334,561)
    tx={n:d[n-1].get_text().replace('\r\n','\n').replace('\r','\n')for n in pages};flat=lambda n:' '.join(tx[n].split())
    need('two (2) preceding Seasons'in flat(26)and 'at least two (2) Seasons'in flat(223)and 'one hundred five percent (105%)'in flat(224),'EarlyBird continuity/price absent')
    need('Minimum Player Salary Exception'in flat(233)and 'first Season covered by the player’s Contract'in flat(55),'Legal minimum family absent')
    need('October 1'in flat(317)and 'Right of First Refusal shall continue'in flat(318),'Unaccepted QO rights absent')
    need(hashlib.sha256(PROFILE.read_bytes()).hexdigest()==PROFILE_SHA,'Profile source observation changed');obs=json.loads(PROFILE.read_text(encoding='utf-8-sig'))
    need(hashlib.sha256(Path(obs['raw_path']).read_bytes()).hexdigest()==obs['raw_sha256']and obs['status']==403 and not obs['raw_body_adopted'],'Failed raw promoted')
    need(hashlib.sha256(base.FEED.read_bytes()).hexdigest()==base.FEED_SHA,'Frozen source changed')
    feed=json.loads(base.FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    named={'Signing 1019177':('richaun-holmes',1610612758),'Signing 1019094':('terence-davis',1610612761),'Trade 2020071':('terence-davis',1610612758),'Signing 1018900':('kyle-guy',1610612758),'Signing 1039682':('louis-king',1610612758),'Signing 1033362':('deaaron-fox',1610612758)}
    rows=[r for r in feed if r['GroupSort']in named and (r['PLAYER_SLUG'],r['TEAM_ID'])==named[r['GroupSort']]];need(len(rows)==6,'Named original own continuity changed')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    rows=[{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True,'operative_original_RSC_prior_option_validly_exercised_if_needed':p=='Marvin Bagley III','Haliburtonfirst2guaranteed_notsecondyearoption':p=='Tyrese Haliburton','Fox2020originalextension_carried_no_newagreement':p=="De'Aaron Fox",'actual_option_receipt':None}for p in LIVE]
    for p,v in EARLY.items():rows.append({'player':p,'route':'VII6b3_EARLY_BIRD','price_function':{'nonoption_seasons':2,'first_base_function':f"q in {v['q']} intersect [legalMinimum,max(175percentPriorSalaryInclusiveRequiredBonus,105percentApplicableAveragePlayerSalary)]",'later_base':'same q','new_bonus':0,'options':0,'full_standard_protection':True,'original_continuity':v['original'],'actual_price':None,'actual_acceptance':None},'old_Gamma_FAclaims_preserved':True,'Terenceordinary_nonRSCQO_if_validlytendered':'max125priorbasepluslikely_vs_minimumplus200k; historicalUFAcategorynotactualQOissue'} )
    rows+=[{'player':p,'route':'VII6f_OWN_MINIMUM','new_nonoption_seasons':1,'base_function':'legal2021minimum(YOS)','new_bonus':0,'options':0,'full_standard_protection':True,'old_Gamma_FAclaims_preserved':True,'actual_price':None,'actual_acceptance':None}for p in('Maurice Harkless','Hassan Whiteside')]
    rows+=[{'player':'Davion Mitchell','route':'VII6h_VIII1_RSC','pick':11,'holder':'SAC','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}]
    return rows
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and EARLY==EARLY_FIXED and POLICY==POLICY_FIXED and SECOND==SECOND_FIXED,'Returned class/option/price/authority altered')

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
        need(a is not None,'Five-player role matching unavailable')
        for r,p in a.items():need(rem[r].get(p,0)>0,'Role remainder invalid');rem[r][p]-=1
        out.append({'start_second':i*120,'end_second':(i+1)*120,'seconds':120,'positions':a})
    need(all(v==0 for ps in rem.values()for v in ps.values()),'Role minutes incomplete');return out

def assert_roles(blocks):
    need(ROLE_MINUTES==ROLE_FIXED and digest(blocks)==ROLE_SHA,'Selected chronology changed');seconds=Counter();rs={r:Counter()for r in ROLE_FIXED}
    for i,b in enumerate(blocks):
        need((b['start_second'],b['end_second'],b['seconds'])==(i*120,(i+1)*120,120)and len(set(b['positions'].values()))==5,'Clock/identity invalid')
        for r,p in b['positions'].items():seconds[p]+=120;rs[r][p]+=120
    need(dict(rs)=={r:Counter({p:m*60 for p,m in ps.items()})for r,ps in ROLE_FIXED.items()}and sum(seconds.values())==14400,'Role/source budget changed');return seconds

def build(root=ROOT):
    src=sources(root)
    for p,h in PINS.items():need(sha(root/p)==h and src[p]==direct(root,p)and digest(src[p])==SOURCE_MEANING_SHA[p],'Returned physical/source semantic differs '+p)
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['SAC'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'Justin James'}|{'Davion Mitchell'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==15,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='SAC'];need([(x['pick'],x['player'])for x in picks]==[(11,'Davion Mitchell'),*SECOND]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected firstRSC rights changed')
    ind=src['simulation/CHICAGO_INDIANA_2021_22_SELECTED_KEEPER_RESULTS.json']['selected_registration']['standard'];need({'Domantas Sabonis','Jeremy Lamb','Justin Holiday'}<=set(ind)and 'Tyrese Haliburton'not in ind,'Original IND SAC atom copied')
    need('Hassan Whiteside'not in src['simulation/CHICAGO_UTAH_2021_SELECTED_KEEPER_RESULT.json']['dated_registration']['standard'],'WhitesideUTA duplicate')
    need('Trey Lyles'in json.dumps(src['research/DETROIT_2021_A_ROUTINE_OPERATING_EXECUTION_FAMILY_2026_10_07.json']) and 'Trey Lyles'not in standard,'OriginalBagleyLylesatomcopied')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds));inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='SAC'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['SAC']=joint.pop('NYK')
        for b in pair:b['SAC']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need(not(set(joint['SAC'])&set(joint['CHI'])),'Actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Davion Mitchell'})
    rates['Davion Mitchell']={'exact_fraction':'-728/1145','effective_rating':float(Fraction(-728,1145)),'classification':'SELECTED_FICTIONAL_CONSERVATIVE_ROOKIE_PRIOR','provenance':{'existing_Duarte_Suggs_conservative_coefficient_reused':True,'not_actual2022NBAstats_orfutureability':True}}
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['SAC'])-int(back['CHI']));margin=impact['CHI']-impact['SAC']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'SAC_active':active,'SAC_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_SAC_impact_fraction':str(margin),'CHI_minus_SAC_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'SAC','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_SACRAMENTO_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_TWO_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':['Louis King'],'STD':15,'TW_count':1,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'interval':'OnlyFeb16/Mar14; no originalHaliburtonHieldIND/SabonisSAC/BagleyDET/LylesSAC/ThompsonSAC/DelonATL tradeatoms imported','butterfly_handoff':['SACseed15−JustinJames nonassignmentwaivefullGamma+Davion11RSC=15STD1TW; Queta41unsignedRTnotrealQueta39TW.','Holmes2019SACtwoServices/TD2019TORtoSACtradeEarly2, ownminHarklessWhiteside, liveFoxoriginal2020extension preserved.','CurrentDETownsLyles retained, currentUTAdoesnotownWhiteside; currentINDretainsSabonis/Lamb/Holiday so no realtradeevent imported.','KyleGuytermtype-dependent lawfulQO unaccepted/newUPC0 preservesFAfloors, LouisTWcarry/eligiblenewtermnoUPCtoSTDconversion.'],'unsigned2R':[{'pick':n,'player':p,'holder':'SAC','UPC':False,'STD':False,'valid_first_RT':'team-signed oneSeason/legalMinYOS0 delivery inside operativeW21, beforeOct15, acceptanceUntilAtLeastOct15; selectedunaccepted','cost':'outstandingRequiredTender minimum/youngFAfloor normal-apron reservation retained, not new liveSTD','foreign_or_college_newfacts':'X5/X6 reopens; no perpetualrights or actualforeignlawcertificate'}for n,p in SECOND],'summary':{'selected_games':2,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'SAC_wins':sum(g['selected_regulation_winner']=='SAC'for g in games),'STD':15,'TW':1,'active_each':12,'positive_each':12,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    lines=['# Sacramento keeper · 두 날짜 선택 결과','','가상 법적 keeper·감독·가용성·단일BPM 선택, 독립 검문 대기.','','|날짜|키|CHI상태|승자|CHI영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:lines.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_SAC_impact_per100']:.9f}|")
    lines+=['','seed15−JustinJames가상nonassignmentwaiver/fullcurrent보호Γ유지+Davion11 RSC=15STD1TW. Holmes2019SAC두서비스와Davis2019TOR두서비스→SAC원계약거래의EarlyBird2 flatq8–10m/4–6m를법정minimum·max(175%priorrequiredbonus포함salary,105%평균)와교차. freshbonus0/options0/fullprotection은새가상UPC조건·원Γ없음인증0. Harkless/Whitesideownmin1·현재Fox2020원extension/원보호·camp·waiver·stretch·FA·unsigned·unusedexceptions함수를보존. newNTMLE/BAE/Room/incomingS&T0·전체private비용미인증.','',
    'KyleGuy원2019TW의계약형태가두one-year라면STANDARDQO,단일two-year이며eligible이면TWQO로분리해유효operativeQO 미수락·미연장Oct1/FRN 또는합법동의철회·새UPC0·정상FAfloor를보존한다. 두별도one-year계약을원문없이사실로선언하지않는다. LouisKing원TW유효live term carry 또는eligibleownnewTW1·oldΓ유지·active미사용. Queta41유효operativefirstRT/minOct15미수락/STD0·youngFAfloor예약/X5/6후손재개방.','',
    'PGFox32/Hali12/Davion4;SGHali20/Hield20/TD8;SFBarnes30/Hield8/Harkless10;PFBagley24/Harkless10/Metu14;CHolmes30/Whiteside14/Jones4=240,12양수active12·Delon/Ramsey/Woodardinactive3. 건강·계수는두날짜위임모델·미래NBA평점/임상인증0. Davion−728/1145는기존보수신인계수재사용.','',
    '선택권리Davion11/Queta41은원9/39와다르다. IND현재Sabonis/Lamb/Holiday 및DET현재Lyles를보존하므로 원Hali/HieldIND·SabonisSAC·BagleyDET/LylesSAC·ThompsonSAC/DelonATL을복사하지않는다. UTA는현재Whiteside미보유.','',
    '[NBA 원프로필](https://www.nba.com/draft/2021/team-profiles/sacramento-kings)의분류web관측·failedHTTPraw본문미채택을분리. 현재CHI Mark32/Caruso18/P32/canonhealth·March25EB/BPM·홈2/연전.5, 각24×120초/2880clock/14400선수초·score/OTnull·82전체/clinical/actualreceiptfalse.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020드래프트|완료|','|2|2020–21|완료|','|3|2021–23|SAC2선택·검문대기|','|4|장기커리어|미완|','|5|결말·구조|미완|','|6|집필규격·Pack|현행등록기·Pack0|','|7|통합·최종승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은큰묶음5/6번까지4·v0.30 PARTIAL/CLOSED/원고0.','']
    return '\n'.join(lines)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved SAC differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Richaun Holmes')['price_function']['actual_acceptance']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_OPTION_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Richaun Holmes')['bpm']='70.5'
        return x
    with patch(__name__+'.physical',wrongsource):
        try:build()
        except ValueError:controls.append('RETURNED_PHYSICAL_FUTURE_BPM')
        else:raise AssertionError('FalsePASS BPM')
    return controls
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'SAC currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_SAC_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
