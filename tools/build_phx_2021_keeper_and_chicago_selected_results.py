"""Two selected Phoenix keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_phx_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_PHOENIX_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
PINS.update({'simulation/CHICAGO_CLEVELAND_2021_22_SELECTED_KEEPER_RESULTS.json': '57c3f5255d1970638aa1cf575e5c526c58de9fb9a5ba2198347e33a100ff499b', 'simulation/CHICAGO_BROOKLYN_2021_22_SELECTED_KEEPER_RESULTS.json': 'b29b621991a541396e952d2cdbbceda1a9025bbc9bc79598b8da3c735ae5743a'})
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100812','0022101056')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-phx-keeper-20261007/observed_profile.json')
PROFILE_SHA='16f34b277f8ce9e8b567508050bf26b6c34324373efee129f631b37d7aac627d'
LIVE=('Cameron Johnson','Dario Saric','Deandre Ayton','Devin Booker','Jae Crowder','Jalen Smith','Jevon Carter','Mikal Bridges','Chris Paul')
OPTIONS={}
SECOND=();SECOND_FIXED=tuple(SECOND)
ROLE_MINUTES={'PG':{'Chris Paul':32,'Cameron Payne':16},'SG':{'Devin Booker':32,'Cameron Payne':4,'Jevon Carter':8,"E'Twaun Moore":4},'SF':{'Mikal Bridges':32,'Abdel Nader':12,'Devin Booker':4},'PF':{'Jae Crowder':28,'Cameron Johnson':20},'C':{'Deandre Ayton':32,'Dario Saric':14,'Frank Kaminsky':2}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Chris Paul','SG':'Devin Booker','SF':'Mikal Bridges','PF':'Jae Crowder','C':'Deandre Ayton'}
ROLE_SHA='df0ecf34879b4bd2b65b4865b230ad28c10f9a39323827ec01476737f115c680'
NADER={'route':'VII6b2_FULL_BIRD','nonoption_seasons':3,'first_base_function':'q in [2000000,3000000] intersect [legalMinimum,II7maximum]','later_base':'same q','new_bonus':0,'options':0,'full_standard_protection':True,'prior2017BOS_2018OKC_2020PHX_tradesOnly_continuous4seasons':True,'actual_price':None,'actual_acceptance':None};NADER_FIXED=deepcopy(NADER)
PAYNE={'route':'VII6b3_EARLY_BIRD','two_prior2019_20_2020_21_PHXseasons':True,'nonoption_seasons':2,'first_base_function':'q in [4000000,6000000] intersect [legalMinimum,max(175percentPriorSalaryInclusiveRequiredBonus,105percentApplicableAveragePlayerSalary)]','later_base':'same q','new_bonus':0,'options':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None};PAYNE_FIXED=deepcopy(PAYNE)
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'Paul':'validoriginal2021playeroption exercise carrysame2018HOUcontract tradedOKC thenPHX; no originalnew2021extension/actualnoticeclaim','Galloway':'originalexpiry/newPHXUPC0/alloldFAprotectedGamma retained; no acquiredreplacementhistoricalactor','TW':'TyShonAlexander originalliveTW carriedvalidterm/originalGamma or eligibleownnew1yrTWafteroperativeQO; no activationcount used and no real2021release copied.','availability':'12positive operationalavailable2dates, SaricworkingrecoverydifferentS2contact+Paulworkingavailable selected; no actualSaricACL/fingerinjury/COVID diagnosis or automaticabsencecopy; clinicalnullzerobench.','whole_private_or_actual_receipts':False};POLICY_FIXED=deepcopy(POLICY)

def direct(root,p):
    t=(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
    return json.loads(t)if p.endswith('.json')else list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else t
SOURCE_MEANING_SHA={'simulation/NBA_2021_22_COMMON_26_OPPONENT_CAPACITY.json': '83a8033265a23be22a002465467225c02e20e56482be8703f2e9f0a46fc23805', 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json': '12456392c139ca9dbb71070e0a574d633728691d477eada592fd03cefc535cb9', 'simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json': '353acb80f6b12e4b67e2cc0cf56ab4f6551cc70efb63b20cf9febc9db21f0c33', 'simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json': '426de339ff1a1270eb41ed6b81caee8e10099e55e2176c4e9f31bd196da853d5', 'simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json': 'b42cfb6e0b895fb6a70eb1a9e32798eb0cda27b98a659b6e4e6fce85a7d431f7', 'canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json': '963c5b9d2967f70cf5770349df39f44f88878e4a3e884b7e0c3c103d7699c6be', 'simulation/CHICAGO_2021_22_CALENDAR.csv': '1c6d8cf8284dc3f88c0d6c7a2a7927f6ba0eb756fbf367da2a44fbfb402e7f68', 'simulation/NBA_2021_22_REGULAR_BASELINE.csv': '8d07a7ba2485a7a0fceeeb2ccfff7acfa1db394f4918459ec4fe30caef2bc4e6', 'simulation/CHICAGO_2020_21_BPM_MAR25_SNAPSHOT.csv': '1ef4eee6a701658c28db8fc611cab263ef8f83936b5badceb45415d35323bfd8', 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS.json': '04d2919b0c1525d0c00d40f7974e8fefd41ed931a1a18495f01b99d98270c317', 'tools/build_chicago_detroit_2021_two_date_selected_bpm_results.py': 'ef289a00d1d7394fefdc6c2d82b535c998f87b6978cddf06fd93319967ebc191', 'tools/build_nyk_2021_keeper_and_chicago_selected_results.py': '01c418a67b2345e60944e90fa602f8644d4bbefeb3456a25cbd0600ef53e9194', 'simulation/CHICAGO_CLEVELAND_2021_22_SELECTED_KEEPER_RESULTS.json': 'bab68853e43260ae13f77f11ad738b1e0467ead24ee8806906bb8752fc884eae', 'simulation/CHICAGO_BROOKLYN_2021_22_SELECTED_KEEPER_RESULTS.json': 'f1bd95da027cf1b247960290fec4c0ac5d182abdc7235332fd4983ace5c3cbf4'}

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
    named={'Signing 1004167':('chris-paul',1610612745),'Trade 2019028':('chris-paul',1610612760),'Trade 2019127':('chris-paul',1610612756),'Signing 1030994':('cameron-payne',1610612756),'Signing 989592':('abdel-nader',1610612738),'Trade 2018015':('abdel-nader',1610612760),'Signing 1033225':('jevon-carter',1610612756)}
    rows=[r for r in feed if r['GroupSort']in named and (r['PLAYER_SLUG'],r['TEAM_ID'])==named[r['GroupSort']]];need(len(rows)==7,'Named original own continuity changed')
    need(any(r['GroupSort']=='Trade 2019127'and r['PLAYER_SLUG']=='abdel-nader'and r['TEAM_ID']==1610612756 for r in feed),'NaderPHXcontinuity absent')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    rows=[{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True,'operative_original_RSC_prior_option_validly_exercised_if_needed':p in('Deandre Ayton','Mikal Bridges','Cameron Johnson'),'JalenSmith_first2guaranteednotsecondyearteamoption':p=='Jalen Smith','original2021Paul_PO_validlyexercised':p=='Chris Paul','actual_option_receipt':None,'Jevon2020ownmultiyearUPCcarrynotBKNtrade':p=='Jevon Carter'}for p in LIVE]
    rows+=[{'player':'Abdel Nader','route':'NEW_OWN_FA','price_function':deepcopy(NADER),'old_Gamma_FAclaims_preserved':True},{'player':'Cameron Payne','route':'NEW_OWN_FA','price_function':deepcopy(PAYNE),'old_Gamma_FAclaims_preserved':True}]
    rows+=[{'player':p,'route':'VII6f_OWN_MINIMUM','new_nonoption_seasons':1,'base_function':'legal2021minimum(YOS)','new_bonus':0,'options':0,'full_standard_protection':True,'old_Gamma_FAclaims_preserved':True,'actual_price':None,'actual_acceptance':None}for p in("E'Twaun Moore",'Torrey Craig','Frank Kaminsky')]
    rows+=[{'player':'Isaiah Jackson','route':'VII6h_VIII1_RSC','pick':29,'holder':'PHX','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}]
    return rows
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and NADER==NADER_FIXED and PAYNE==PAYNE_FIXED and POLICY==POLICY_FIXED and SECOND==SECOND_FIXED,'Returned class/option/price/authority altered')

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
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['PHX'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'Langston Galloway'}|{'Isaiah Jackson'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==15,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='PHX'];need([(x['pick'],x['player'])for x in picks]==[(29,'Isaiah Jackson')]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected firstRSC rights changed')
    need('JaVale McGee'in src['simulation/CHICAGO_CLEVELAND_2021_22_SELECTED_KEEPER_RESULTS.json']['selected_registration']['standard'] and 'JaVale McGee'not in standard,'McGeeF5 CLE owner restored')
    bkn=src['simulation/CHICAGO_BROOKLYN_2021_22_SELECTED_KEEPER_RESULTS.json']['selected_registration']['standard'];need('Landry Shamet'in bkn and 'Jevon Carter'not in bkn,'Original PHX BKN atom copied')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds));inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='PHX'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['PHX']=joint.pop('NYK')
        for b in pair:b['PHX']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need(not(set(joint['PHX'])&set(joint['CHI'])),'Actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby'})
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['PHX'])-int(back['CHI']));margin=impact['CHI']-impact['PHX']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'PHX_active':active,'PHX_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_PHX_impact_fraction':str(margin),'CHI_minus_PHX_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'PHX','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_PHOENIX_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_TWO_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':['Ty-Shon Alexander'],'STD':15,'TW_count':1,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'interval':'OnlyFeb7/Mar18; no originalPaulnewcontract/SaricACL/ShametBKN/McGeeCLE/SmithCraigIND atoms inherited','butterfly_handoff':['PHXseed15−Gallowayexpired/noUPCfullGamma+IsaiahJackson29RSC=15STD1TW; no Sharpe29BKN/JevonBKN/ShametPHX atom.','Paulvalid2021PO retainsoriginal2018HOUterm tradedOKCthenPHX; no original4yearre-sign copied.','Nader4continuousNBAservices tradesonlyFullBird3; Payne2020PHXROS+2020_21twoServiceEarly2; originalΓ preserved.','No originalMcGeePHX(CLEapprovedF5owner) orTorreyIND/JalenIND/PaytonLAL omitted, currentnamedkeeperrolesonly.'],'unsigned2R':[{'pick':n,'player':p,'holder':'PHX','UPC':False,'STD':False,'valid_first_RT':'team-signed oneSeason/legalMinYOS0 delivery inside operativeW21, beforeOct15, acceptanceUntilAtLeastOct15; selectedunaccepted','cost':'outstandingRequiredTender minimum/youngFAfloor normal-apron reservation retained, not new liveSTD','foreign_or_college_newfacts':'X5/X6 reopens; no perpetualrights or actualforeignlawcertificate'}for n,p in SECOND],'summary':{'selected_games':2,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'PHX_wins':sum(g['selected_regulation_winner']=='PHX'for g in games),'STD':15,'TW':1,'active_each':12,'positive_each':12,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    lines=['# Phoenix keeper · 두 날짜 선택 결과','','가상 법적 keeper·가용성·감독·단일BPM의 선택, 독립 검문 대기.','','|날짜|키|CHI상태|승자|CHI영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:lines.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_PHX_impact_per100']:.9f}|")
    lines+=['','seed15−Galloway원만료/no새UPC/allFA보호Γ+IsaiahJackson29RSC=15STD1TW. Paul원2018HOU계약→OKC→PHX 및2021PO유효행사를선택해carry, 원4년재서명/실제금액·notice인증0. Ayton/Bridges/Johnson원RSC옵션유효행사·JalenSmithfirst2보장(2년차option아님)·Jevon2020새UPC원Γ보존.','',
    'Nader2017BOS→2018OKC→2020PHX 거래만4서비스 FullBird3, q2–3m/법정min·IImax교차. Payne2020June30PHX ROS+2020–21서비스 EarlyBird2, q4–6m/법정min·max(175%priorrequiredbonus포함salary,105%평균)교차. 양계약2/3nonoptionflat·freshbonus0/fullprotection·정확수락null, Moore/Craig/Kaminskyownmin1년. 기존보호·camp·waiver·stretch·FA·unsigned·unusedexceptions함수유지. newNTMLE/BAE/Room/incomingS&T0, oldyearhardcap자동계승0.','',
    'TyShon원liveTW의유효term이어받기 또는operativeQO후owneligibleTW1년·원Γ유지. 경기active미사용·실제원2021release미복사. 새로운권리29는원Sharpe29BKN/CarterBKN/ShametPHX와다르며McGee는현재F5 CLE소유로PHX중복금지, 원Torrey/JalenIND거래도복사0.','',
    'usual5 Paul/Booker/Bridges/Crowder/Ayton. PGPaul32/Payne16;SGBooker32/Payne4/Carter8/Moore4;SFBridges32/Nader12/Booker4;PFCrowder28/Cam20;CAyton32/Saric14/Kaminsky2=240. active12양수, Craig/Jalen/Jacksoninactive3. Saric가상회복은S2접촉갈림·Paul가용성을두날짜위임선택, 원ACL/finger/COVID임상·지속결장 자동이식0.','',
    '[NBA 원프로필](https://www.nba.com/draft/2021/team-profiles/phoenix-suns) live/FA/PO관측·실패raw본문미채택을분리. currentCHI Mark32/Caruso18/P32/canonhealth·March25EB/BPM/홈2/연전.5. 각24×120초/2880clock/14400선수초, score/OTnull·private원장/82전체/실제기관수락인증false.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020드래프트|완료|','|2|2020–21|완료|','|3|2021–23|PHX2선택·검문대기|','|4|장기커리어|미완|','|5|결말·구조|미완|','|6|집필규격·Pack|현행등록기·Pack0|','|7|통합·최종승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은큰묶음5/6번까지4·v0.30 PARTIAL/CLOSED/원고0.','']
    return '\n'.join(lines)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved PHX differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Abdel Nader')['price_function']['actual_acceptance']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_OPTION_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Chris Paul')['bpm']='70.5'
        return x
    with patch(__name__+'.physical',wrongsource):
        try:build()
        except ValueError:controls.append('RETURNED_PHYSICAL_FUTURE_BPM')
        else:raise AssertionError('FalsePASS BPM')
    return controls
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'PHX currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_PHX_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
