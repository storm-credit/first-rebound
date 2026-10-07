"""Four selected Orlando keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_orl_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_ORLANDO_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100283','0022100555','0022100701','0022100769')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-orl-keeper-20261007/observed_profile.json')
PROFILE_SHA='152410fae37dbfaeda3f0860fa5d34643276d25a84a8bf79758cb1a91b81f2ea'
LIVE=('Al-Farouq Aminu','Chuma Okeke','Cole Anthony','Dwayne Bacon','Gary Harris','Jonathan Isaac','Markelle Fultz','Michael Carter-Williams','Mo Bamba','Nikola Vucevic','Terrence Ross','Zeke Nnaji')
ROLE_MINUTES={
 'BASE_ABSENT':{'PG':{'Cole Anthony':32,'Michael Carter-Williams':16},'SG':{'Gary Harris':28,'Terrence Ross':8,'Dwayne Bacon':8,'Michael Carter-Williams':4},'SF':{'Terrence Ross':22,'Chuma Okeke':18,'Al-Farouq Aminu':8},'PF':{'Evan Mobley':28,'Chuma Okeke':10,'Al-Farouq Aminu':4,'Zeke Nnaji':6},'C':{'Nikola Vucevic':32,'Mo Bamba':16}},
 'RECOVERY':{'PG':{'Markelle Fultz':20,'Cole Anthony':24,'Michael Carter-Williams':4},'SG':{'Gary Harris':28,'Michael Carter-Williams':10,'Terrence Ross':10},'SF':{'Terrence Ross':20,'Chuma Okeke':12,'Jonathan Isaac':16},'PF':{'Evan Mobley':28,'Chuma Okeke':16,'Jonathan Isaac':4},'C':{'Nikola Vucevic':32,'Mo Bamba':16}}
}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'BASE_ABSENT':{'PG':'Cole Anthony','SG':'Gary Harris','SF':'Terrence Ross','PF':'Evan Mobley','C':'Nikola Vucevic'},'RECOVERY':{'PG':'Markelle Fultz','SG':'Gary Harris','SF':'Terrence Ross','PF':'Evan Mobley','C':'Nikola Vucevic'}}
ROLE_SHA={'BASE_ABSENT': '153de0e636db1e7f76dc4af955c79faf877a6cc8f53f26e7d0f1ec8d45a14332', 'RECOVERY': '52da529502c6b74166a368246708785da67d9707d698d3e4b731fdd1a89600d1'}
DATE_STATES={'0022100283':'BASE_ABSENT','0022100555':'BASE_ABSENT','0022100701':'RECOVERY','0022100769':'RECOVERY'}
DATE_STATES_FIXED=deepcopy(DATE_STATES)
QO={'ordinary':'max(5/4*originalPriorSalary,applicable2021OneSeasonMinimum+200000)','starter':False,'starter_if_qualifies':'greater original ordinary and pick21RSC100percent ordinaryQO including permitted anchor bonuses','starter_threshold_function':'41GS or2000min in priorSeason OR mean two priorSeasons; not observed future stats','actual_prior_salary':None,'actual_starter_status':None,'actual_tender_or_acceptance':None}
QO_FIXED=deepcopy(QO)
SECOND=((33,'Herbert Jones'),)
SECOND_FIXED=tuple(SECOND)
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'Ennis':'original expiry, no newUPC; all earnedGamma/FAclaims retained','TW':'Original liveTW nonassignmentwaiver/full currentGamma or expired applicable STANDARD/TWQO unaccepted/unextendedOct1; FRN/FAclaims preserved. Thornwell originalprofile UFA and S2TW class discrepancy not newUPC or inferred exactterm.','availability':'BASE_ABSENT Fultz/Isaac workingout Nov26/Jan3; RECOVERY Fultz20/Isaac20 operational available Jan23/Feb1. Separate fiction health selection, not originalclinical/actualreturndate. Zeroreserve not clinicalabsence.','whole_private_or_actual_receipts':False}
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
    need(hashlib.sha256(PROFILE.read_bytes()).hexdigest()==PROFILE_SHA,'Profile source observation changed');obs=json.loads(PROFILE.read_text())
    need(hashlib.sha256(Path(obs['raw_path']).read_bytes()).hexdigest()==obs['raw_sha256']and obs['status']==403 and not obs['raw_body_adopted'],'Failed raw promoted')
    need(hashlib.sha256(base.FEED.read_bytes()).hexdigest()==base.FEED_SHA,'Frozen source changed')
    feed=json.loads(base.FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    named={'Signing 1039949':'ignas-brazdeikis','Signing 1039576':'moritz-wagner','Signing 1034197':'jonathan-isaac','Signing 1034198':'markelle-fultz','Signing 1033368':'james-ennis-iii','Signing 1033285':'dwayne-bacon','Signing 1018794':'nikola-vucevic'}
    rows=[r for r in feed if r['TEAM_ID']==1610612753 and r['GroupSort']in named and r['PLAYER_SLUG']==named[r['GroupSort']]];need(len(rows)==7,'Named original own continuity changed')
    need('one hundred twenty-five percent (125%)'in flat(313),'Ordinary QO function missing')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True,'operative_original_RSC_prior_option_validly_exercised_if_needed':p=='Mo Bamba','actual_option_receipt':None,'original_RSC_firstSeason_2020_not_2019':p=='Chuma Okeke','original_Dec2020_extension_current_carry_not_new2021_signing':p in ('Markelle Fultz','Jonathan Isaac')}for p in LIVE]+[{'player':'Ignas Brazdeikis','route':'NEW_OWN_FA_MINIMUM','prior_applicable_ordinary_QO':deepcopy(QO),'new_contract':'voluntary oneSeason lawfulMinimum(YOS) UPC; player may agree after validQO; not QO accepted below required amount','old_Gamma_QO_FAclaims_preserved':True,'new_bonus':0,'full_standard_protection':True,'actual_price_or_receipt':None},{'player':'Moritz Wagner','route':'NEW_OWN_FA_MINIMUM','new_contract':'oneSeason lawfulMinimum(YOS) UPC','old_Gamma_FAclaims_preserved':True,'new_bonus':0,'full_standard_protection':True,'actual_price_or_receipt':None},{'player':'Evan Mobley','route':'VII6h_VIII1_RSC','pick':3,'holder':'ORL','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}])
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and QO==QO_FIXED and POLICY==POLICY_FIXED and SECOND==SECOND_FIXED and DATE_STATES==DATE_STATES_FIXED,'Returned class/option/price/authority altered')

def role_blocks(state):
    rem={r:{p:m//2 for p,m in ps.items()}for r,ps in ROLE_MINUTES[state].items()};roles=list(rem);out=[]
    for i in range(24):
        if i==0:a=deepcopy(STARTERS[state])
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

def assert_roles(blocks,state):
    need(ROLE_MINUTES==ROLE_FIXED and digest(blocks)==ROLE_SHA[state],'Selected chronology changed');seconds=Counter();rs={r:Counter()for r in ROLE_FIXED[state]}
    for i,b in enumerate(blocks):
        need((b['start_second'],b['end_second'],b['seconds'])==(i*120,(i+1)*120,120)and len(set(b['positions'].values()))==5,'Clock/identity invalid')
        for r,p in b['positions'].items():seconds[p]+=120;rs[r][p]+=120
    need(dict(rs)=={r:Counter({p:m*60 for p,m in ps.items()})for r,ps in ROLE_FIXED[state].items()}and sum(seconds.values())==14400,'Role/source budget changed');return seconds

def build(root=ROOT):
    src=sources(root)
    for p,h in PINS.items():need(sha(root/p)==h and src[p]==direct(root,p),'Returned physical source differs '+p)
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['ORL'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'James Ennis III'}|{'Evan Mobley'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==15,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='ORL'];need([(x['pick'],x['player'])for x in picks]==[(3,'Evan Mobley'),*SECOND]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected firstRSC rights changed')
    roles={};registrations={}
    for st in ROLE_FIXED:
        blocks=role_blocks(st);seconds=assert_roles(blocks,st);active=sorted(set(seconds)|({'Moritz Wagner'}if st=='BASE_ABSENT'else{'Moritz Wagner','Dwayne Bacon'}));inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated active nomination changed')
        roles[st]={'blocks':blocks,'player_seconds':dict(seconds),'active':active};registrations[st]={'active':active,'inactive':inactive,'positive':sorted(seconds),'working_absent':['Markelle Fultz','Jonathan Isaac']if st=='BASE_ABSENT'else[],'zero_nonabsent':sorted(set(standard)-set(seconds)-({'Markelle Fultz','Jonathan Isaac'}if st=='BASE_ABSENT'else set()))}
    prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='ORL'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        st=DATE_STATES[gid];r=roles[st];pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['ORL']=joint.pop('NYK')
        for b in pair:b['ORL']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need(not(set(joint['ORL'])&set(joint['CHI'])),'Actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint,st))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Evan Mobley','Jonathan Isaac'})
    rates['Evan Mobley']={'exact_fraction':'-728/1145','method':'SELECTED_FICTIONAL_CONSERVATIVE_ROOKIE_PRIOR_EXISTING_DUARTE_SUGGS_FAMILY','historical_BPM':None,'observed_minutes':None,'fictional_working_coefficient_selected':True,'source_boundary':'Same existing selected conservative rookie coefficient; no2021/22 realized rookie productivity or honors imported'}
    need(Fraction(rates['Evan Mobley']['exact_fraction'])==Fraction(src[det.OUT]['player_ratings']['Chris Duarte']['exact_fraction']),'Existing selected rookie prior changed')
    need(not any(x['nba_player']=='Jonathan Isaac'for x in src[det.BPM]),'Isaac source n0 changed')
    rates['Jonathan Isaac']={'exact_fraction':'0','method':'SELECTED_FICTIONAL_EB_N0_NEUTRAL_LIMIT','historical_BPM':None,'observed_minutes':None,'selected_pseudo_observation_minutes':0,'source_row_exists':False,'actual_ability_zero_certified':False,'fictional_working_coefficient_selected':True,'source_boundary':'March25 2021 missing row; current operational recovery is not productivity recovery or historical ability zero; no laterNBA stats imported'}
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint,st in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['ORL'])-int(back['CHI']));margin=impact['CHI']-impact['ORL']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'ORL_state':st,'ORL_active':registrations[st]['active'],'ORL_inactive':registrations[st]['inactive'],'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_ORL_impact_fraction':str(margin),'CHI_minus_ORL_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'ORL','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_ORLANDO_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_FOUR_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':[],'STD':15,'TW_count':0,'by_working_state':registrations,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':{st:r['blocks']for st,r in roles.items()},'selected_ratings':rates,'selected_games':games,'interval':'Only Nov26/Jan3 BASE_ABSENT and Jan23/Feb1 RECOVERY; not whole82or originalactualreturncalendar','butterfly_handoff':['Vucevic/AminuORL, CarterCHI, Harris/NnajiORL, GordonDEN, HamptonDAL,FournierBOS preserved. HallF4omitted; nooriginalHall signing imported.','Mobley3ORL RSC; Herbert33 unsigned validRT. NoSuggs5/Franz8/Preston33/LACdrafttrade copied.','Fultz/Isaac originalDec2020 extension carried, no fresh2021 QO fabricated. OriginalACL observation distinct from operationalfictionrecovery.','Ignas originalMayROS→ownstandardminimum with applicablevalidordinaryQO and consent, nooriginalAug11TW automatically copied; MoritzROS→ownmin.','Ennis originalexpiry/newUPC0, nooriginalAminuCHI/Baconwaiver copied; fulloldGamma costsretained.'],'unsigned2R':[{'pick':n,'player':p,'holder':'ORL','UPC':False,'STD':False,'valid_first_RT':'team-signed oneSeason/legalMinYOS0 delivery inside operativeW21, beforeOct15, acceptanceUntilAtLeastOct15; selectedunaccepted','cost':'outstandingRequiredTender minimum/youngFAfloor normal-apron reservation retained, not new liveSTD','foreign_or_college_newfacts':'X5/X6 reopens; no perpetualrights or actualforeignlawcertificate'}for n,p in SECOND],'summary':{'selected_games':4,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'ORL_wins':sum(g['selected_regulation_winner']=='ORL'for g in games),'STD':15,'TW':0,'active_each':12,'positive_by_state':{st:len(r['player_seconds'])for st,r in roles.items()},'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Orlando keeper · 네 날짜 선택 결과','','선택된 가상 법적 가족·감독·건강·단일 BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|ORL 상태|승자|CHI 영향/100|','|---|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['ORL_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_ORL_impact_per100']:.9f}|")
    a+=['','May16 seed15의 Ennis 만료·신규UPC0 대신 선택 Mobley3 RSC를 연결해15STD0TW. live12의 원급여·보호·보너스Γ 유지. Bamba4년차 원옵션의 적법통지는 가상조건/실접수null. Okeke RSC 개시2020과 Fultz/Isaac Dec2020 연장→2021 live를 보존한다. Vucevic/AminuORL, CarterCHI, NnajiORL, HamptonDAL/FournierBOS를 원역사와 구분한다.','',
    'Ignas MayROS가 만료되면 applicableordinaryRFAQO를 유효제공하고, 선수동의하는 별도ownminimum1년UPC를 구성한다. 125%prior와min+200k, 선발조건21번scale 함수를 보존하며 낮은별도계약을QO수락이라고 주장하지 않는다. MoritzROS 만료후ownminimum1년. 두 새UPC는법정최소함수/bonus0/fullprotection이고 원가격·서명·기관수락은null이다. 모든 camp/waiver/stretch/FA/unsigned/unusedexception/불완전명단Γ 함수 보존·신규NTMLE/BAE/Room/S&T0; wholeprivate비용확정이 아니다.','',
    'Herbert33은 팀서명1년legalminRT를operative2021 창 안에 제공하고 최소Oct15까지수락가능하지만 미수락선택으로STD0. FAfloor/RT 비용예약과 X5/X6 재개방을 보존한다. Randle/Thornwell originalTWlive면 비양도방출+fullΓ, 만료면해당STANDARD/TWQO·Oct1미수락/FRN 유지. Thornwell 원프로필UFA와 S2TW 구분을삭제하지 않는다.','',
    '[NBA 원프로필](https://www.nba.com/draft/2021/team-profiles/orlando-magic)의 원계약/FA 구분은 관측근거이며 직접HTTP403 bytes는본문증거가 아니다. 원Suggs5/Franz8/Preston33/LAC거래·Baconwaiver·AminuCHI·Hall계약을복사하지 않는다.','',
    'BASE_ABSENT Nov26/Jan3: Cole32/MCW20/Harris28/Ross30/Okeke28/Mobley28/Vucevic32/Bamba16/Aminu12/Bacon8/Nnaji6=240. Fultz/Isaac 작업부재, 양수11+Moritz active12. RECOVERY Jan23/Feb1: Cole24/MCW14/Harris28/Ross30/Okeke28/Mobley28/Vuc32/Bamba16/Fultz20/Isaac20=240. 양수10+Moritz/Bacon active12. PG48·각포지션48·usual5·24개2분블록·동시CHI2880초 직접검문. Isaac wing/PF/Fultz PG 회복은 건강위임의 작업선택이고 원역사복귀일·임상인증이 아니다. Nnaji후두경기0은 원커리어실패결론이 아니다.','',
    'Isaac은 March25 원행 부재의 EB n0중립한계0을 가상계수로 선택하며 과거실력0·회복능력확정이 아니다. Mobley는 기존Duarte/Suggs의 보수적가상rookieprior −728/1145를 선택하고 실제2022stats/상훈을가져오지 않는다. 현재CHI Mark32/Caruso18/P32·단일March25 EB/BPM·홈2·연전.5, 점수/OTnull.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|2020–21|완료|','|3|2021–23|ORL4 결과 작업선택·독립검문 대기|','|4|장기 커리어|미완|','|5|결말·구조|미완|','|6|집필 규격·Pack|현행 기능등록기 참조·Pack0|','|7|통합·최종 승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰 묶음5,6번까지4. v0.30 PARTIAL/CLOSED/원고0. whole82/wholemacro3/실제 기관·의학·사적 비용 인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved IND differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Moritz Wagner')['actual_price_or_receipt']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_PRICE_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Nikola Vucevic')['bpm']='70.5'
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
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_ORL_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
