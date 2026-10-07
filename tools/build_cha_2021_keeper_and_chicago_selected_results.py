"""Three selected Charlotte keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_cha_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_CHARLOTTE_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
MIA_ATOM='research/TORONTO_MIAMI_2021_SELECTED_ATOM_LEGAL_BRIDGE_2026_10_07.json'
PINS[MIA_ATOM]='719b2ff19583d6373a2c165988c9fc55b298fce3728dc8763df2d3f327357278'
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100307','0022100826','0022101208')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-cha-keeper-20261007/observed_profile.json')
PROFILE_SHA='05bab86c5b744ff34a12387629f6efacea853a1163e30b329fbcc541fc90f94b'
LIVE=('Anthony Edwards','Cody Martin','Gordon Hayward','Jalen McDaniels','Miles Bridges','Nick Richards','P.J. Washington','Terry Rozier','Vernon Carey Jr.')
ROLE_MINUTES={'PG':{'Cade Cunningham':28,'Devonte\' Graham':14,'Terry Rozier':6},'SG':{'Anthony Edwards':20,'Terry Rozier':20,'Malik Monk':8},'SF':{'Gordon Hayward':30,'Anthony Edwards':12,'Miles Bridges':6},'PF':{'Miles Bridges':20,'P.J. Washington':14,'Jalen McDaniels':14},'C':{'Cody Zeller':26,'Bismack Biyombo':12,'P.J. Washington':10}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Cade Cunningham','SG':'Anthony Edwards','SF':'Gordon Hayward','PF':'Miles Bridges','C':'Cody Zeller'}
ROLE_SHA='29aaaf8ec4b5dbf7197181a16e6a55cc55e9168fba598e607b603a7e40848383'
SECOND=((56,'Scottie Lewis'),(58,'Jay Huff'))
SECOND_FIXED=tuple(SECOND)
QO_FUNCTIONS={'Devonte\' Graham':{'ordinary':'max(5/4*originalPriorSalary,applicable2021oneSeasonMinimum+200000)','starter_if_qualifies':'max(originalOrdinary,pick21RSC100percentQO_with_permitted_anchorBonuses)'},'Malik Monk':{'ordinary':'original4thRSCsalary*(1+operative2017pick11QOincrease)','nonstarter':'lesser(originalOrdinary,pick15RSC120percentQO_with_permitted_anchorBonuses)','latepick_starter_uplift_applies_to_pick11':False}}
QO_FIXED=deepcopy(QO_FUNCTIONS)
BIRD={'Devonte\' Graham':{'route':'VII6b2_FULL_BIRD','nonoption_seasons':3,'first_base_function':'q in [10000000,14000000] intersect [legalMinimum,II7maximum]','later_base':'same q','new_bonus':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None},'Malik Monk':{'route':'VII6b2_FULL_BIRD','nonoption_seasons':3,'first_base_function':'q in [6000000,10000000] intersect [legalMinimum,II7maximum]','later_base':'same q','new_bonus':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None}}
BIRD_FIXED=deepcopy(BIRD)
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'Caleb_prior_cleanup':{'route':'LAWFUL_NONASSIGNMENT_WAIVER','request':'2021-08-01 workingproposal','effectively_cleared_before':'first selectedMIA TW agreement','all_original_protected_salary_bonus_and_earned_Gamma_preserved':True,'new_stretch_setoff_or_assignment':False,'actual_receipt':None},'Wanamaker':'originalexpiry, timelyapplicableordinaryQO unaccepted/unextendedOct1 or lawfulconsensualwithdrawal; newUPC0; all earnedGamma/FA/FRN claims retained','TW':'NateDarling/TyrellTerry original selected2020oneSeasonTW expiry and applicableoperative2021QO unaccepted/unextendedOct1, newUPC0 and fulloldGamma/FA/FRNclaims retained. No realGrantRillerTW replacement or Tyrellclinicalleave inferred.','availability':'11positive operationalavailable onthree selecteddates; Hayward no newcontactfoot/protocolinjury selected. Actualclinical/mentalhealth/crossyear servicecertification false, zeroreserveclinicalnull.','whole_private_or_actual_receipts':False}
POLICY_FIXED=deepcopy(POLICY)

def direct(root,p):
    t=(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
    return json.loads(t)if p.endswith('.json')else list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else t
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
    named={'Signing 1004114':'devonte-graham','Signing 989343':'malik-monk','Trade 2020074':'brad-wanamaker','Signing 1033614':'bismack-biyombo','Signing 979044':'cody-zeller','Trade 2019011':'terry-rozier','Signing 1021129':'caleb-martin','Signing 1019331':'cody-martin'}
    rows=[r for r in feed if r['TEAM_ID']==1610612766 and r['GroupSort']in named and r['PLAYER_SLUG']==named[r['GroupSort']]];need(len(rows)==8,'Named original own continuity changed')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True,'operative_original_RSC_prior_option_validly_exercised_if_needed':p in('Miles Bridges','P.J. Washington'),'actual_option_receipt':None,'selected2020EdwardsnotoriginalLaMelo':p=='Anthony Edwards','second_round_not_RSC':p in('Nick Richards','Vernon Carey Jr.')}for p in LIVE]+[{'player':p,'route':'NEW_OWN_FA','price_function':deepcopy(BIRD[p]),'applicable_prior_QO':deepcopy(QO_FUNCTIONS[p]),'prior_starter_function':'41GS or2000min priorSeason OR mean two precedingSeasons; status a legalinput not assumedfuturestats','old_Gamma_QO_FAclaims_preserved':True}for p in BIRD]+[{'player':p,'route':'NEW_OWN_FA_MINIMUM','new_contract':'oneSeason applicable2021legalMinimum(YOS) UPC','old_Gamma_FAclaims_preserved':True,'new_bonus':0,'options':0,'full_standard_protection':True,'actual_price_or_receipt':None}for p in('Cody Zeller','Bismack Biyombo')]+[{'player':'Cade Cunningham','route':'VII6h_VIII1_RSC','pick':1,'holder':'CHA','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}])
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and BIRD==BIRD_FIXED and QO_FUNCTIONS==QO_FIXED and POLICY==POLICY_FIXED and SECOND==SECOND_FIXED,'Returned class/option/price/authority altered')

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
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['CHA'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'Brad Wanamaker','Caleb Martin'}|{'Cade Cunningham'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==14 and 'Anthony Edwards'in standard and 'LaMelo Ball'not in standard,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='CHA'];need([(x['pick'],x['player'])for x in picks]==[(1,'Cade Cunningham'),*SECOND]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected firstRSC rights changed')
    need('Caleb Martin'in src[MIA_ATOM]['MIA_roster_handoff']['opening_2021_10_25_two_way']and 'Caleb Martin'not in standard and src[MIA_ATOM]['selected_atom']['fictional_NPC_direction_selected'],'Current MIA Caleb ownership not preserved')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds)|{'Nick Richards'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==2 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='CHA'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['CHA']=joint.pop('NYK')
        for b in pair:b['CHA']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need(not(set(joint['CHA'])&set(joint['CHI'])),'Actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Cade Cunningham'})
    rates['Cade Cunningham']={'exact_fraction':'-728/1145','method':'SELECTED_FICTIONAL_CONSERVATIVE_ROOKIE_PRIOR_EXISTING_DUARTE_SUGGS_FAMILY','historical_BPM':None,'observed_minutes':None,'fictional_working_coefficient_selected':True,'source_boundary':'Existing conservative working rookie coefficient, not realized2021/22 productivity or originaldraftteam'}
    need(Fraction(rates['Cade Cunningham']['exact_fraction'])==Fraction(src[det.OUT]['player_ratings']['Chris Duarte']['exact_fraction']),'Existing selected rookie prior changed')
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['CHA'])-int(back['CHI']));margin=impact['CHI']-impact['CHA']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'CHA_active':active,'CHA_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_CHA_impact_fraction':str(margin),'CHI_minus_CHA_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'CHA','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_CHARLOTTE_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_CALEB_PRIOR_WAIVER_THREE_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_prior_cleanup':deepcopy(POLICY['Caleb_prior_cleanup']),'selected_registration':{'standard':standard,'TW':[],'STD':14,'TW_count':0,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'interval':'Only Nov29/Feb9/Apr8; originalFebruaryHarrelltrade or COVID/contacthealth notautomatically inherited','butterfly_handoff':['EdwardsCHA selected2020 RSC, Cade1CHA2021RSC; noLaMeloCHA/Bouknight11/KaiJones19/Thor37 originalchain copied.','Wanamakerexpiry noUPC, GrahamownBird3/MonkownBird3/Zellerownmin/Biyomboownmin with sourceQO/oldGamma preserved; noGrahamNOP/MonkLAL/ZellerPOR/BiyomboPHX copied.','Scottie56/Huff58 unsignedvalidRT, noKoprivica57DETswap/newfuturefirstNYK copied. PlumleeDET retained, noHarrellWAS→CHA/SmithNOPtrade copied.','RozieroriginalcurrentUPC preserved, nooriginal2021extension chose; Haywardoperationalavailability fictional notactualclinical/protocolcert.','TyrellTerry selectedCHA TW notoriginalRiller; J1priorleave remainspriorphase, currentnewUPC0 notfuturemedicalinference.'],'unsigned2R':[{'pick':n,'player':p,'holder':'CHA','UPC':False,'STD':False,'valid_first_RT':'team-signed oneSeason/legalMinYOS0 delivery inside operativeW21, beforeOct15, acceptanceUntilAtLeastOct15; selectedunaccepted','cost':'outstandingRequiredTender minimum/youngFAfloor normal-apron reservation retained, not new liveSTD','foreign_or_college_newfacts':'X5/X6 reopens; no perpetualrights or actualforeignlawcertificate'}for n,p in SECOND],'summary':{'selected_games':3,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'CHA_wins':sum(g['selected_regulation_winner']=='CHA'for g in games),'STD':14,'TW':0,'active_each':12,'positive_each':11,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Charlotte keeper · 세 날짜 선택 결과','','선택된 가상 법적 가족·감독·건강·단일 BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_CHA_impact_per100']:.9f}|")
    a+=['','May16 seed15의 Wanamaker만료·새UPC0 대신 선택Cade1 RSC를연결해14STD0TW. 선택된 MIA CalebTW보다 먼저 CHA 비양도방출을 합법가상선택한다. 원liveCaleb의 보호급여·bonus·earnedΓ 전액보존, stretch/setoff/assignment0, actualreceipt null. live9+GrahamBird3/MonkBird3+Zeller/Biyomboownmin1+Cade. Edwards 선택2020RSC는원LaMelo3이아니며 둘째보장시즌, Bridges4/PJ3 원operativeoption유효통지조건을보존한다. Richards/Carey는2R이라RSC취급금지. 원Caleb방출비용·Cody/McDaniels Γ 유지·실제계약끝추정삭제0.','',
    'Graham2018ownUPC/Monk2017ownRSC→3priorseasons FullBird. 3년nonoptionflatq10–14m/6–10m와legalmin/IImax교집합·새bonus0/fullprotection으로선택, actualmoney/수락null. Grahamordinary125%prior/min+200k·선발21anchor, Monk원4thRSCraise/비선발15anchor120함수와구별하며 별도동의UPC를낮은QO수락이라고주장하지않는다. 원스타터상태와옵션접수 실제인증0.','',
    'WanamakerapplicableQO를미수락/unextendedOct1 또는합법동의철회로정리하고earnedΓ/FA/FRN은유지한다. Zeller/Biyomboownmin1 법정급여/bonus0/options0/fullprotection. Darling/Terry 원selected2020한시즌TW만료·해당2021QO·Oct1미수락/FRN/earnedΓ를보존하고UPC0,원RillerTW/임상leave자동이식0. 모든oldcamp/waiver/stretch/FA/unsigned/unusedexception/불완전명단 비용함수 보존·새NTMLE/BAE/Room/S&T0·wholeprivate장부인증0.','',
    'Scottie56/Huff58 팀서명1년legalminRT를operative2021창안에제공·최소Oct15까지수락가능하지만미수락선택STD0,FAfloor/RT 비용예약 및 X5/X6새notice 재개방. 새Kai19보호futurefirstNYK나Thor37/Koprivica57swap를복사하지않는다. [NBA 원프로필](https://www.nba.com/draft/2021/team-profiles/charlotte-hornets)의 계약/FA관측과HTTP403raw본문미채택을구별한다. 원PlumleeCHA·HarrellWAS→CHA·SmithNOP·GrahamNOP거래도미선택.','',
    'usual5 Cade/Edwards/Hayward/Bridges/Zeller. Cade28/Graham14/Rozier26/Edwards32/Hayward30/Bridges26/PJ24/Zeller26/Biyombo12/McDaniels14/Monk8=240. PG Cade28/Graham14/Rozier6,SG Edwards20/Rozier20/Monk8,SF Hayward30/Edwards12/Bridges6,PF Bridges20/PJ14/McDaniels14,C Zeller26/Biyombo12/PJ10. 양수11+Richards active12, Cody/Careyinactive2·0분임상사유null. Edwards wing12/BridgesPF/PJ smallcenter10은명시감독선택,common수학fixture복사0. Hayward 새접촉/protocol없음은실제임상증명이아닌health위임모델.','',
    'Cade 가상prior는 기존Duarte/Suggs같은−728/1145. Edwards는frozenMarch25계수를사용해미관측성장을실력사실로확정하지않는다. 단일EB/BPM·홈2·연전.5·CHI32Mark/18Caruso/32P,score/OTnull.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|2020–21|완료|','|3|2021–23|CHA3 결과 작업선택·독립검문 대기|','|4|장기 커리어|미완|','|5|결말·구조|미완|','|6|집필 규격·Pack|현행 기능등록기 참조·Pack0|','|7|통합·최종 승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰 묶음5,6번까지4. v0.30 PARTIAL/CLOSED/원고0. whole82/wholemacro3/실제기관·의학·사적비용 인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved CHA differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Cody Zeller')['actual_price_or_receipt']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_PRICE_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Gordon Hayward')['bpm']='70.5'
        return x
    with patch(__name__+'.physical',wrongsource):
        try:build()
        except ValueError:controls.append('RETURNED_PHYSICAL_FUTURE_BPM')
        else:raise AssertionError('FalsePASS BPM')
    return controls
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'IND currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_CHA_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
