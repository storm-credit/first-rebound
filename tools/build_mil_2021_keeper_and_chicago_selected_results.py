"""Four selected Milwaukee keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_mil_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_MILWAUKEE_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100690','0022100949','0022101082','0022101183')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-mil-keeper-20261007/observed_profile.json')
PROFILE_SHA='f4f9d6c54e65efe9f91d09ce322288285d335d18987e131e214b0daf09d095f3'
LIVE=('Brook Lopez','Donte DiVincenzo','Elijah Bryant','Giannis Antetokounmpo','Jordan Nwora','Jrue Holiday','Khris Middleton','Mamadi Diakite','Pat Connaughton','Sam Merrill')
OPTIONS={'Bobby Portis':'valid original player option exercise','Bryn Forbes':'valid original player option exercise'}
SECOND=();SECOND_FIXED=tuple(SECOND)
ROLE_MINUTES={'PG':{'Jrue Holiday':32,'Jeff Teague':10,'Bryn Forbes':6},'SG':{'Donte DiVincenzo':26,'Bryn Forbes':8,'Pat Connaughton':14},'SF':{'Khris Middleton':32,'Pat Connaughton':8,'Elijah Bryant':6,'Jordan Nwora':2},'PF':{'Giannis Antetokounmpo':28,'Jordan Nwora':10,'Thanasis Antetokounmpo':6,'Bobby Portis':4},'C':{'Brook Lopez':26,'Bobby Portis':16,'Giannis Antetokounmpo':6}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Jrue Holiday','SG':'Donte DiVincenzo','SF':'Khris Middleton','PF':'Giannis Antetokounmpo','C':'Brook Lopez'}
ROLE_SHA='b02ba7d60c72bb87071433fec75ab1e4e5ceb395f008c16c41183aab6d7a6f54'
PRICE={'route':'VII6b3_EARLY_BIRD','nonoption_seasons':2,'first_base_function':'q in [2000000,3000000] intersect [legalMinimum,max(175percentPriorSalaryInclusiveRequiredBonus,105percentApplicableAveragePlayerSalary)]','later_base':'same q','new_bonus':0,'options':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None,'continuous2019MILtwo_prior_seasons':True}
PRICE_FIXED=deepcopy(PRICE)
QO={'ordinary':'max(125percentPriorBasePlusLikelyBonus,legalMinimum2021(YOS)+200000)','nonRSC_notpickAnchor':True,'actual_price':None};QO_FIXED=deepcopy(QO)
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'Tucker':'Originalexpiry no newMILUPC, originalFA/owedGamma retained; currentMIA selectedUPC notduplicated.','TW':'Original Toupane/JustinJackson liveTW lawfulnonassignmentwaiver/fullGamma OR expired applicablelegalQO unaccepted/unextendedOct1/FRN orconsensualwithdrawal,newUPC0; Justin4YOS STANDARDQO not50kTW, standardFAfloor preserved. NotlivingQOrenouncedfirst.','availability':'12positive operationalavailable4dates; Brookback/Donteankleworkingrecovery selected and no copiedoriginalCOVID/Gianniscontactinjuries; no actualclinical orvaccination proof.','whole_private_or_actual_receipts':False}
POLICY_FIXED=deepcopy(POLICY)
MIA='research/TORONTO_MIAMI_2021_SELECTED_ATOM_LEGAL_BRIDGE_2026_10_07.json';PINS[MIA]='719b2ff19583d6373a2c165988c9fc55b298fce3728dc8763df2d3f327357278'

def direct(root,p):
    t=(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
    return json.loads(t)if p.endswith('.json')else list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else t
SOURCE_MEANING_SHA={'simulation/NBA_2021_22_COMMON_26_OPPONENT_CAPACITY.json': '83a8033265a23be22a002465467225c02e20e56482be8703f2e9f0a46fc23805', 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json': '12456392c139ca9dbb71070e0a574d633728691d477eada592fd03cefc535cb9', 'simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json': '353acb80f6b12e4b67e2cc0cf56ab4f6551cc70efb63b20cf9febc9db21f0c33', 'simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json': '426de339ff1a1270eb41ed6b81caee8e10099e55e2176c4e9f31bd196da853d5', 'simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json': 'b42cfb6e0b895fb6a70eb1a9e32798eb0cda27b98a659b6e4e6fce85a7d431f7', 'canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json': '963c5b9d2967f70cf5770349df39f44f88878e4a3e884b7e0c3c103d7699c6be', 'simulation/CHICAGO_2021_22_CALENDAR.csv': '1c6d8cf8284dc3f88c0d6c7a2a7927f6ba0eb756fbf367da2a44fbfb402e7f68', 'simulation/NBA_2021_22_REGULAR_BASELINE.csv': '8d07a7ba2485a7a0fceeeb2ccfff7acfa1db394f4918459ec4fe30caef2bc4e6', 'simulation/CHICAGO_2020_21_BPM_MAR25_SNAPSHOT.csv': '1ef4eee6a701658c28db8fc611cab263ef8f83936b5badceb45415d35323bfd8', 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS.json': '04d2919b0c1525d0c00d40f7974e8fefd41ed931a1a18495f01b99d98270c317', 'tools/build_chicago_detroit_2021_two_date_selected_bpm_results.py': 'ef289a00d1d7394fefdc6c2d82b535c998f87b6978cddf06fd93319967ebc191', 'tools/build_nyk_2021_keeper_and_chicago_selected_results.py': '01c418a67b2345e60944e90fa602f8644d4bbefeb3456a25cbd0600ef53e9194', 'research/TORONTO_MIAMI_2021_SELECTED_ATOM_LEGAL_BRIDGE_2026_10_07.json': '91b359478481e9fdc49cdfef9a6c83ddb240a7422f3e068671e73f87edeabd7d'}
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
    named={'Signing 1019181':'thanasis-antetokounmpo','Signing 1038698':'jrue-holiday','Signing 1038628':'jeff-teague','Signing 1039979':'elijah-bryant'}
    rows=[r for r in feed if r['TEAM_ID']==1610612749 and r['GroupSort']in named and r['PLAYER_SLUG']==named[r['GroupSort']]];need(len(rows)==4,'Named original own continuity changed')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True,'operative_original_RSC_prior_option_validly_exercised_if_needed':p=='Donte DiVincenzo','actual_option_receipt':None,'currentJrueApril4_originalextension_carry_notnewPO':p=='Jrue Holiday','originalGiannisDec2020extension_allGamma_preserved':p=='Giannis Antetokounmpo','ElijahROS_multiyearoriginal_uncertainty_carried_notnewQO':p=='Elijah Bryant'}for p in LIVE]+[{'player':p,'route':q,'original_salary_term_and_Gamma_kept':True,'operative_original_deadline_notice_selected':True,'actual_notice_receipt':None}for p,q in OPTIONS.items()]+[{'player':'Thanasis Antetokounmpo','route':'NEW_OWN_FA','price_function':deepcopy(PRICE),'applicable_prior_QO':deepcopy(QO),'new_contract_years':2,'old_Gamma_QO_FAclaims_preserved':True}]+[{'player':'Jeff Teague','route':'NEW_OWN_FA_MINIMUM','new_contract':'oneSeason applicable2021legalMinimum(YOS) UPC','old_Gamma_FAclaims_preserved':True,'new_bonus':0,'options':0,'full_standard_protection':True,'actual_price_or_receipt':None}]+[{'player':'Kai Jones','route':'VII6f_STANDARD_MINIMUM_SECOND_ROUND','pick':31,'holder':'MIL','new_contract':'twoSeasons applicable2021signedLegalMinimumYOS0_and_year2_scale','new_bonus':0,'options':0,'full_standard_protection':True,'valid_first_RT_before_UPC':True,'old_RT_replaced_no_doublehold':True,'actual_price':None,'not_RSC80_120':True}])
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and PRICE==PRICE_FIXED and QO==QO_FIXED and POLICY==POLICY_FIXED and SECOND==SECOND_FIXED,'Returned class/option/price/authority altered')

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
    for p,h in PINS.items():need(sha(root/p)==h and src[p]==direct(root,p),'Returned physical source differs '+p)
    need(all(digest(src[p])==SOURCE_MEANING_SHA[p] for p in PINS),'Returned consumed source semantic differs from reviewed physical source');raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['MIL'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'P.J. Tucker'}|{'Kai Jones'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==15,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='MIL'];need([(x['pick'],x['player'])for x in picks]==[(31,'Kai Jones'),*SECOND]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected firstRSC rights changed')
    need('P.J. Tucker' not in standard and 'P.J. Tucker' in str(src[MIA]),'Selected currentMIA Tucker owner altered')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds));inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='MIL'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['MIL']=joint.pop('NYK')
        for b in pair:b['MIL']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need(not(set(joint['MIL'])&set(joint['CHI'])),'Actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Kai Jones','Elijah Bryant'})
    rates['Kai Jones']={'exact_fraction':'-728/1145','method':'SELECTED_FICTIONAL_CONSERVATIVE_ROOKIE_PRIOR_EXISTING_DUARTE_SUGGS_FAMILY','historical_BPM':None,'observed_minutes':None,'fictional_working_coefficient_selected':True,'source_boundary':'Existing conservative working rookie coefficient; reserve0 not realizedNBAstats or RSCtemplate'}
    need(not any(x['nba_player']=='Elijah Bryant' for x in src[det.BPM]),'Elijah pre-cutoff missing row changed')
    rates['Elijah Bryant']={'exact_fraction':'-728/1145','effective_rating':float(Fraction(-728,1145)),'classification':'SELECTED_FICTIONAL_CONSERVATIVE_NBA_N0_NEWCOMER_PRIOR','provenance':{'NBAoriginalsigning_after_March25':True,'no_pre_cutoff_BPM_row':True,'existing_Duarte_Suggs_comparator_prior_reused':True,'not_actualIsraeli_orNBArealizedability':True}}
    need(Fraction(rates['Kai Jones']['exact_fraction'])==Fraction(src[det.OUT]['player_ratings']['Chris Duarte']['exact_fraction']),'Existing selected rookie prior changed')
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['MIL'])-int(back['CHI']));margin=impact['CHI']-impact['MIL']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'MIL_active':active,'MIL_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_MIL_impact_fraction':str(margin),'CHI_minus_MIL_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'MIL','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_MILWAUKEE_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_FOUR_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':[],'STD':15,'TW_count':0,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'interval':'Only Jan21/Mar4/Mar22/Apr5 same namedfamily; no originalGraysonMEMtoMIL/MerrillMEM/HoodMIL/DonteSAC/IbakaMIL trades or realinjury events imported','butterfly_handoff':['MIAselectedTucker currentUPC preserved/MILnewUPC0, alloldowedFAclaim kept; Kai31secondminimum2year replacesexpiredslot and rights≠automaticRSC.','CurrentJrueApril2021originalextension/GiannisDec2020extension allterm/Gamma carry, not inventedexpired2021PO ornewexactextensionprice.','Portis/Forbes originalPO lawfulfictionexercise, Thanasis2019MILtwoSeasonEarly2/ordinarynonRSCQO andTeagueownmin1 separatefromrealnegotiation.','No original2021#31Todd trade54/60+picks; Kai31 remainsMIL, correspondingconditionalsecondoldRTcostreplaced once on acceptedUPC.','MEMkeepsGraysonAllen/SamMerrillMIL retained, no realAllenMIL/DonteSAC/RodneyHoodMIL/SergeMIL/JordanNworaCHI events copied.'],'unsigned2R':[{'pick':n,'player':p,'holder':'MIL','UPC':False,'STD':False,'valid_first_RT':'team-signed oneSeason/legalMinYOS0 delivery inside operativeW21, beforeOct15, acceptanceUntilAtLeastOct15; selectedunaccepted','cost':'outstandingRequiredTender minimum/youngFAfloor normal-apron reservation retained, not new liveSTD','foreign_or_college_newfacts':'X5/X6 reopens; no perpetualrights or actualforeignlawcertificate'}for n,p in SECOND],'summary':{'selected_games':4,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'MIL_wins':sum(g['selected_regulation_winner']=='MIL'for g in games),'STD':15,'TW':0,'active_each':12,'positive_each':12,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Milwaukee keeper · 네 날짜 선택 결과','','선택된 가상 법적 가족·감독·건강·단일 BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_MIL_impact_per100']:.9f}|")
    a+=['','May16 seed15의 Tucker원만료/MILnewUPC0·원FA/보호비용유지→KaiJones31 2R minimum2년UPC로15STD0TW. 현재MIA선택Tucker와소유중복0. live10+Portis/Forbes원PO+ThanasisEarly2+Teagueownmin1+Kai. Jrue4/4/2021 원연장/Giannis12/2020 원연장은현재live전체Γ조건으로carry하며새2021PO/정확가격을복원하지않는다. Elijah원ROS/다년형태불확실성도전체원기간조건carry이며새QO아님.','',
    'Thanasis2019MIL 두시즌 EarlyBird2 새nonoptionflatq2–3m은법정minimum·max(175%원필요bonus포함급여,105%평균)교집합. ordinarynonRSCQO는max(125%priorbase+likely,minimum+200k),실제수락/가격null. Teague min1·Kai31secondmin2/YOS0후년scale는newbonus0/options0/fullprotection·유효firstRT뒤UPC·oldRT중복hold없음. Kai는RSC80–120%가아니다. 모든oldcamp/waiver/stretch/FA/unsigned/unusedexceptionΓ유지·newNTMLE/BAE/Room/S&T0·actualprivatecert0.','',
    'Toupane/JustinJackson TWlive면비양도waive/fullΓ,만료면형태/YOS별유효QO미수락·미연장Oct1/FRN 또는합법동의철회·newUPC0. Justin4YOS는STANDARDQO/정상FAfloor이며50kTW보호로지우지않는다. 살아있는QO를먼저renounce하지않는다.','',
    '[NBA 원프로필](https://www.nba.com/draft/2021/team-profiles/milwaukee-bucks)은원live/PO/RFA관측·direct403raw미채택. 원#31Todd→54/60/2픽과선택Kai31권리를분리. MEMGrayson/원MILMerrill소유유지로원AllenMIL/MerrillMEM·원HoodMIL/DonteSAC/SergeMIL거래복사0.','',
    'usual5 Jrue/Donte/Khris/Giannis/Brook. PGJrue32/Teague10/Forbes6;SGDonte26/Forbes8/Pat14;SFKhris32/Pat8/Elijah6/Nwora2;PFGiannis28/Nwora10/Thanasis6/Portis4;CBrook26/Portis16/Giannis6=240.12양수active12,Merrill/Mamadi/Kaiinactive3. Brookback/Donteankle작업회복·네날짜양수가용선택은실제medical/COVID/접촉부상부재증거아님.0분clinicalnull.','',
    '현재CHI Mark32/Caruso18/P32·선택canonhealth·단일March25 EB/BPM·홈2·연전.5. Kai0분reserve와NBA5월13일첫서명Elijah(March25원행부재)는기존보수NBA신입prior−728/1145를선택·실제NBA후대stats/이스라엘실력을인증하지않는다.24×2분 양팀2880초/14400선수초·score/OTnull·전체시즌비용/기관접수인증false.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|2020–21|완료|','|3|2021–23|MIL4 선택결과·검문대기|','|4|장기 커리어|미완|','|5|결말·구조|미완|','|6|집필 규격·Pack|현행 등록기·Pack0|','|7|통합·최종 승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰묶음5/6번까지4·v0.30 PARTIAL/CLOSED/원고0·wholemacro3/실제private·의료인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved MIL differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Bobby Portis')['actual_notice_receipt']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_OPTION_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Giannis Antetokounmpo')['bpm']='70.5'
        return x
    with patch(__name__+'.physical',wrongsource):
        try:build()
        except ValueError:controls.append('RETURNED_PHYSICAL_FUTURE_BPM')
        else:raise AssertionError('FalsePASS BPM')
    return controls
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'MIL currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_MIL_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
