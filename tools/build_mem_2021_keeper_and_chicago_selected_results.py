"""Two selected Memphis keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_mem_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_MEMPHIS_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100658','0022100909')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-mem-keeper-20261007/observed_profile.json')
PROFILE_SHA='d7d9c1e2d81098c96924a265dc03af3fd58f8be6c09fc2803597295016015151'
LIVE=('Brandon Clarke',"De'Anthony Melton",'Desmond Bane','Dillon Brooks','Grayson Allen','Ja Morant','Jaren Jackson Jr.','John Konchar','Jonas Valanciunas','Jontay Porter','Kyle Anderson','Tyus Jones','Xavier Tillman Sr.')
OPTIONS={'Justise Winslow':'valid original team option exercise'}
SECOND=((49,'Filip Petrusev'),);SECOND_FIXED=tuple(SECOND)
ROLE_MINUTES={'PG':{'Ja Morant':32,'Tyus Jones':12,"De'Anthony Melton":4},'SG':{'Dillon Brooks':22,'Desmond Bane':24,"De'Anthony Melton":2},'SF':{'Dillon Brooks':10,'Kyle Anderson':22,"De'Anthony Melton":12,'Justise Winslow':4},'PF':{'Jaren Jackson Jr.':28,'Brandon Clarke':18,'Kyle Anderson':2},'C':{'Jonas Valanciunas':30,'Xavier Tillman Sr.':12,'Brandon Clarke':6}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Ja Morant','SG':'Desmond Bane','SF':'Dillon Brooks','PF':'Jaren Jackson Jr.','C':'Jonas Valanciunas'}
ROLE_SHA='604c0075f4d4a34a536db2f87242cd32eabff5947144fa619dd854930515fabe'
POLICY={'new_RSC_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'Frazier':'expiry/newUPC0; alloldearned protected/FAclaims preserved, no laterORL hardshipcopy','TW':'KillianTillie/SeanMcDermott originalTWlive retained fullGamma OR expiredownFA eligibleoperative2021newoneSeasonTW/nooption lawfulagreedUPC afterapplicableQO handling; oldTWprotection/FAfloor/FRN preserved. OperativeQO standardvsTW determined bypriorform/currentYOS, no false50kstandardQO; 0NBAactivations/conversions at2dates.','availability':'11positive available2dates includingBrooks/JJJ selectedfictioncontact-recovery, no copiedrealCOVID/ankleorJaavailability; zerobenchclinicalnull.','whole_private_or_actual_receipts':False}
POLICY_FIXED=deepcopy(POLICY)

def direct(root,p):
    t=(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
    return json.loads(t)if p.endswith('.json')else list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else t
SOURCE_MEANING_SHA={'simulation/NBA_2021_22_COMMON_26_OPPONENT_CAPACITY.json': '83a8033265a23be22a002465467225c02e20e56482be8703f2e9f0a46fc23805', 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json': '12456392c139ca9dbb71070e0a574d633728691d477eada592fd03cefc535cb9', 'simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json': '353acb80f6b12e4b67e2cc0cf56ab4f6551cc70efb63b20cf9febc9db21f0c33', 'simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json': '426de339ff1a1270eb41ed6b81caee8e10099e55e2176c4e9f31bd196da853d5', 'simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json': 'b42cfb6e0b895fb6a70eb1a9e32798eb0cda27b98a659b6e4e6fce85a7d431f7', 'canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json': '963c5b9d2967f70cf5770349df39f44f88878e4a3e884b7e0c3c103d7699c6be', 'simulation/CHICAGO_2021_22_CALENDAR.csv': '1c6d8cf8284dc3f88c0d6c7a2a7927f6ba0eb756fbf367da2a44fbfb402e7f68', 'simulation/NBA_2021_22_REGULAR_BASELINE.csv': '8d07a7ba2485a7a0fceeeb2ccfff7acfa1db394f4918459ec4fe30caef2bc4e6', 'simulation/CHICAGO_2020_21_BPM_MAR25_SNAPSHOT.csv': '1ef4eee6a701658c28db8fc611cab263ef8f83936b5badceb45415d35323bfd8', 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS.json': '04d2919b0c1525d0c00d40f7974e8fefd41ed931a1a18495f01b99d98270c317', 'tools/build_chicago_detroit_2021_two_date_selected_bpm_results.py': 'ef289a00d1d7394fefdc6c2d82b535c998f87b6978cddf06fd93319967ebc191', 'tools/build_nyk_2021_keeper_and_chicago_selected_results.py': '01c418a67b2345e60944e90fa602f8644d4bbefeb3456a25cbd0600ef53e9194'}
def sources(root):return {p:physical(root,p)for p in PINS}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def support():
    need(hashlib.sha256(base.CBA.read_bytes()).hexdigest()==base.CBA_SHA,'CBA raw changed')
    d=fitz.open(base.CBA);pages=(26,29,30,54,55,58,74,75,212,222,223,224,233,240,241,294,303,311,312,313,314,317,318,332,333,334,561)
    tx={n:d[n-1].get_text().replace('\r\n','\n').replace('\r','\n')for n in pages};flat=lambda n:' '.join(tx[n].split())
    need('two (2) preceding Seasons'in flat(26)and 'at least two (2) Seasons'in flat(223)and 'one hundred five percent (105%)'in flat(224),'EarlyBird continuity/price absent')
    need('Minimum Player Salary Exception'in flat(233)and 'first Season covered by the player’s Contract'in flat(55),'Legal minimum family absent')
    need('October 1'in flat(317)and 'Right of First Refusal shall continue'in flat(318),'Unaccepted QO rights absent')
    need(hashlib.sha256(PROFILE.read_bytes()).hexdigest()==PROFILE_SHA,'Profile source observation changed');obs=json.loads(PROFILE.read_text(encoding='utf-8-sig'))
    need(hashlib.sha256(Path(obs['raw_path']).read_bytes()).hexdigest()==obs['raw_sha256']and obs['status']==403 and not obs['raw_body_adopted'],'Failed raw promoted')
    need(hashlib.sha256(base.FEED.read_bytes()).hexdigest()==base.FEED_SHA,'Frozen source changed')
    feed=json.loads(base.FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    named={'Signing 1039533':'tim-frazier','Trade 2019100':'justise-winslow','Signing 1019117':'jonas-valanciunas'}
    rows=[r for r in feed if r['TEAM_ID']==1610612763 and r['GroupSort']in named and r['PLAYER_SLUG']==named[r['GroupSort']]];need(len(rows)==3,'Named original own continuity changed')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True,'operative_original_RSC_prior_option_validly_exercised_if_needed':p in('Ja Morant','Brandon Clarke','Jaren Jackson Jr.','Grayson Allen'),'actual_option_receipt':None,'no_originalnewJJJextension_orAllenMIL_orJVNOPtrade':True,'Jontay_retainedfullOriginalProtection_notpresumedwaived_ornewUPC':p=='Jontay Porter'}for p in LIVE]+[{'player':p,'route':q,'original_salary_term_and_Gamma_kept':True,'operative_original_deadline_notice_selected':True,'actual_notice_receipt':None}for p,q in OPTIONS.items()]+[{'player':'Ziaire Williams','route':'VII6h_VIII1_RSC','pick':17,'holder':'MEM','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}])
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and POLICY==POLICY_FIXED and SECOND==SECOND_FIXED,'Returned class/option/price/authority altered')

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
    need(all(digest(src[p])==SOURCE_MEANING_SHA[p] for p in PINS),'Returned consumed source semantic differs from reviewed physical source');raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['MEM'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'Tim Frazier'}|{'Ziaire Williams'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==15,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='MEM'];need([(x['pick'],x['player'])for x in picks]==[(17,'Ziaire Williams'),*SECOND]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected firstRSC rights changed')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds)|{'Ziaire Williams'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='MEM'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['MEM']=joint.pop('NYK')
        for b in pair:b['MEM']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need(not(set(joint['MEM'])&set(joint['CHI'])),'Actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Ziaire Williams','Xavier Tillman Sr.','Jaren Jackson Jr.'})
    need(not any(x['nba_player']=='Jaren Jackson Jr.' for x in src[det.BPM]),'Missing-row EB prior boundary changed')
    rates['Jaren Jackson Jr.']={'exact_fraction':'0','effective_rating':0.0,'classification':'SELECTED_FICTIONAL_EB_NEUTRAL_PRIOR_LIMIT_N0','provenance':{'March25_snapshot_row_missing':True,'observed_minutes':None,'not_historical_career_BPM0_or_actual_skill0':True,'selected_working_limit':'No positive pre-cutoff observation enters EB; choose neutral EB n0 limit, not later2021/22 observed stats.'}}
    rates['Xavier Tillman Sr.']=det.expected_ratings({det.BPM:src[det.BPM]},{'Xavier Tillman'})['Xavier Tillman']
    rates['Ziaire Williams']={'exact_fraction':'-728/1145','method':'SELECTED_FICTIONAL_CONSERVATIVE_ROOKIE_PRIOR_EXISTING_DUARTE_SUGGS_FAMILY','historical_BPM':None,'observed_minutes':None,'fictional_working_coefficient_selected':True,'source_boundary':'Existing conservative working rookie coefficient, not realized2021/22 productivity or originalGSWdraftteam'}
    need(Fraction(rates['Ziaire Williams']['exact_fraction'])==Fraction(src[det.OUT]['player_ratings']['Chris Duarte']['exact_fraction']),'Existing selected rookie prior changed')
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['MEM'])-int(back['CHI']));margin=impact['CHI']-impact['MEM']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'MEM_active':active,'MEM_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_MEM_impact_fraction':str(margin),'CHI_minus_MEM_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'MEM','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_MEMPHIS_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_TWO_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':['Killian Tillie','Sean McDermott'],'STD':15,'TW_count':2,'TW_NBAactivations':0,'TW_form_function':deepcopy(POLICY['TW']),'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'interval':'Only Jan17/Feb26 same namedfamily; no originalJVtoNOP/AdamsBledsoeMEM/AllenMIL/WinslowLAC/JJJextension/SantiMEM atoms imported','butterfly_handoff':['Ziaire17MEM RSC replacesTimFrazierexpiry/newUPC0, Filip49MEMunsignedRT; original10Ziaire/30Aldama/40Butler/51BJ trades notcopied.','JV2019liveMEM preserved and NOPkeeper retainsAdams/Bledsoe; no automaticdoubleownership orfuture2R/burden cancellation.','GraysonAllen originalRSC operativeoption preserved/noMILtrade, WinslowvalidoriginalTO retained/fullGamma, Jontaycurrentprotection preserved.','TWsourceMcDermott isnotstandard simplybecauseNBAprofileundercontract listsF; currentTWcarry orlawfulownoneSeasonnewTW conditionalform only.','Brooks/JJJworkingrecovery positive2dates, no originalJaabsence/COVID/clincert.'],'unsigned2R':[{'pick':n,'player':p,'holder':'MEM','UPC':False,'STD':False,'valid_first_RT':'team-signed oneSeason/legalMinYOS0 delivery inside operativeW21, beforeOct15, acceptanceUntilAtLeastOct15; selectedunaccepted','cost':'outstandingRequiredTender minimum/youngFAfloor normal-apron reservation retained, not new liveSTD','foreign_or_college_newfacts':'X5/X6 reopens; no perpetualrights or actualforeignlawcertificate'}for n,p in SECOND],'summary':{'selected_games':2,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'MEM_wins':sum(g['selected_regulation_winner']=='MEM'for g in games),'STD':15,'TW':2,'active_each':12,'positive_each':11,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Memphis keeper · 두 날짜 선택 결과','','선택된 가상 법적 가족·감독·건강·단일 BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_MEM_impact_per100']:.9f}|")
    a+=['','May16 seed15 TimFrazier만료/no newUPC→Ziaire17 RSC로15STD2TW. live13+Winslow원TO+ZiaireRSC. Morant/Clarke3·JJJ/Allen4 operativeRSCoption 조건/actualreceiptnull, Jontay원보호전체Γ를 보존한다. 원JVNOP/AdamsBledsoeMEM/AllenMIL/WinslowLAC·JJJextension은 미실행. NOPkeeper의Adams/Bledsoe와소유일치·원픽/현금의역사bundle도복사0.','',
    'Tillie/McDermott 원TW가살아있으면원보호/기간유지, 만료면<4YOS 등법정eligible인 해당ownFA oneSeasonTW/nooption을 유효QO처리후합법가상수락한다. 원STANDARD vsTWQO는이전형태/현재YOS함수로정하며standardQO를50k로바꾸지않고원minimumFAfloor/FRN/earnedΓ유지. 두날짜NBAactivation0/standardconversion0·TW급여현금0인증아님. NBA프로필McDermott의F표기만으로STD전환하지않는다.','',
    'Filip49 팀서명1년법정minRT를operativeW21내유효제공·최소Oct15수락창/미수락후적법만료·NBAUPC0/STD0. outstandingRT/최소FAfloor예약 및X5/X6권리재개방유지, 무기한독점0. Frazier원earned/FA/waiver/camp/stretch/모든oldΓ보존·newNTMLE/BAE/Room/S&T0·원privatebonus없음인증0.','',
    '[NBA 원프로필](https://www.nba.com/draft/2021/team-profiles/memphis-grizzlies)의FA/TO분류는web직독관측·direct403raw는본문미채택. 원17TreyMurphy/51BJ·10Ziaire/30Aldama거래와선택17Ziaire/49Filip를분리한다. Santi37DET/TreyMurphy23NOP·JaredButler22LAL 소유복사금지.','',
    'usual5 Ja/Bane/Brooks/JJJ/JV. PGJa32/Tyus12/Melton4;SGBrooks22/Bane24/Melton2;SFBrooks10/Kyle22/Melton12/Winslow4;PFJJJ28/Clarke18/Kyle2;CJV30/Tillman12/Clarke6=240. 11양수+Ziaireactive12,Allen/Konchar/Jontayinactive3. Brooks/JJJ의회복·접촉가용은선택fiction이며realCOVID/ankle/Jaabsence나의료인증아님·0분clinicalnull.','',
    '현재CHI Mark32/Caruso18/P32·canonhealth·단일March25 EB/BPM·홈2·연전.5. sourceXavierTillman alias로고정, 미래stats0. JJJ의March25원행부재는EB n0중립계수0을작업선택한것이며역사능력/전성기/BPM0이아니다. 회복가용28분과실력복구를동일시하지않는다. Ziaire0분reserve도별도기존보수rookieprior−728/1145로두고실제실력0인증아님.24×2분 양팀2880초/14400선수초·score/OTnull·두날짜외시즌불변주장0.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|2020–21|완료|','|3|2021–23|MEM2 선택결과·검문대기|','|4|장기 커리어|미완|','|5|결말·구조|미완|','|6|집필 규격·Pack|현행 등록기·Pack0|','|7|통합·최종 승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰묶음5/6번까지4·v0.30 PARTIAL/CLOSED/원고0·wholemacro3/실제private·의학인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved MEM differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Justise Winslow')['actual_notice_receipt']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_OPTION_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Ja Morant')['bpm']='70.5'
        return x
    with patch(__name__+'.physical',wrongsource):
        try:build()
        except ValueError:controls.append('RETURNED_PHYSICAL_FUTURE_BPM')
        else:raise AssertionError('FalsePASS BPM')
    return controls
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'MEM currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_MEM_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
