"""Two selected Denver keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_den_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_DENVER_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='8b8e451fd4d30804bb27f4ae820953be84ddbb6a'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100236','0022100357')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-den-keeper-20261007/observed_profile.json')
PROFILE_SHA='7d3df9393290c03ff90ffe44606714f30ae3e518943382def31487ea92ed2a70'
PLAYOFF='simulation/NBA_2021_ALL_DATED_PLAYOFF_COACH_PLANS.json'
PINS[PLAYOFF]='27fb630174fb39653738a19e51f0a8d6c969c6397505284e794a7383f6030c99'
T4='canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json'
PINS[T4]='ab996ffb9f9f6e4471ad473633af1529eb4928e3aa9a17b99642c591691c3798'
F5='canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json'
PINS[F5]='c0166bba7a0874aa08dfa88e7d00c0f0d0e237ca2090459ddd6167cf1353c5ea'
LIVE=('Aaron Gordon','Bol Bol','Facundo Campazzo','Jamal Murray','Michael Porter Jr.','Monte Morris','Nikola Jokic','PJ Dozier','Saddiq Bey','Vlatko Cancar')
OPTIONS={'Will Barton':'valid original player option exercise','JaMychal Green':'valid original player option exercise','Isaiah Hartenstein':'valid original player option exercise'}
MINIMUM=('Austin Rivers',)
ROLE_MINUTES={'PG':{'Facundo Campazzo':24,'Monte Morris':24},'SG':{'Will Barton':24,'Austin Rivers':18,'Monte Morris':2,'PJ Dozier':4},'SF':{'Michael Porter Jr.':28,'Will Barton':6,'Saddiq Bey':14},'PF':{'Aaron Gordon':30,'JaMychal Green':12,'Michael Porter Jr.':4,'Saddiq Bey':2},'C':{'Nikola Jokic':34,'Isaiah Hartenstein':12,'JaMychal Green':2}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Facundo Campazzo','SG':'Will Barton','SF':'Michael Porter Jr.','PF':'Aaron Gordon','C':'Nikola Jokic'}
ROLE_SHA='1160ec399c53b94981260abeea38f5ee1db204160cbd492380f5dce0708d0a53'
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'Millsap':'original expiry, no newUPC; full old earnedGamma/FAclaims retained; no originalBKN assignment imported','TW':'If originalTWlive, lawful nonassignmentwaiver bySep30/full currentprotectedGamma kept; ifexpired, applicable STANDARD/TWQO term/service eligibility timelyoperative2021 unaccepted/unextendedOct1 FRN/FAclaims retained. No newUPC or inferred exactterm.','Murray':'PriorS2 selected MODELED_ABSENT carried on bothdates, not sourceclinicaldiagnosis or eternalabsence','Barton_PJ_MPJ':'Barton andPJ separately selected operationalrecovery; MPJ no newchangedcontact backinjury on these2dates. Originalfutureinjury/protocol not imported or diagnosed.','whole_private_or_actual_receipts':False}
POLICY_FIXED=deepcopy(POLICY)

def direct(root,p):
    t=(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
    return json.loads(t)if p.endswith('.json')else list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else t
def sources(root):return {p:physical(root,p)for p in PINS}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def support():
    need(hashlib.sha256(base.CBA.read_bytes()).hexdigest()==base.CBA_SHA,'CBA raw changed')
    d=fitz.open(base.CBA);pages=(26,29,30,54,55,58,212,222,223,224,233,240,241,294,303,311,312,313,317,318,332,333,334,561)
    tx={n:d[n-1].get_text().replace('\r\n','\n').replace('\r','\n')for n in pages};flat=lambda n:' '.join(tx[n].split())
    need('two (2) preceding Seasons'in flat(26)and 'at least two (2) Seasons'in flat(223)and 'one hundred five percent (105%)'in flat(224),'EarlyBird continuity/price absent')
    need('Minimum Player Salary Exception'in flat(233)and 'first Season covered by the player’s Contract'in flat(55),'Legal minimum family absent')
    need('October 1'in flat(317)and 'Right of First Refusal shall continue'in flat(318),'Unaccepted QO rights absent')
    need(hashlib.sha256(PROFILE.read_bytes()).hexdigest()==PROFILE_SHA,'Profile source observation changed');obs=json.loads(PROFILE.read_text())
    need(hashlib.sha256(Path(obs['raw_path']).read_bytes()).hexdigest()==obs['raw_sha256']and obs['status']==403 and not obs['raw_body_adopted'],'Failed raw promoted')
    need(hashlib.sha256(base.FEED.read_bytes()).hexdigest()==base.FEED_SHA,'Frozen source changed')
    feed=json.loads(base.FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    named={'Signing 1004185':'will-barton','Signing 1033635':'jamychal-green','Signing 1033563':'isaiah-hartenstein','Signing 1039674':'austin-rivers','Signing 1033702':'paul-millsap'}
    rows=[r for r in feed if r['TEAM_ID']==1610612743 and r['GroupSort']in named and r['PLAYER_SLUG']==named[r['GroupSort']]];need(len(rows)==5,'Named original current/own continuity changed')
    need(obs['F5_original_CLE_Hartenstein_PO_observation']['class']=='PLAYER_OPTION'and obs['F5_original_CLE_Hartenstein_PO_observation']['selected_S2_F5_holder']=='DEN','Original Hart option/candidate ownership conflated')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True,'operative_original_RSC_option_validly_exercised_if_needed':p=='Michael Porter Jr.','actual_option_receipt':None}for p in LIVE]+[{'player':p,'route':q,'original_salary_term_and_Gamma_kept':True,'operative_original_deadline_notice_selected':True,'actual_notice_receipt':None}for p,q in OPTIONS.items()]+[{'player':p,'route':'VII6i_MINIMUM','seasons':1,'salary':'signed2021LegalMinimum(YOS)','new_bonus':0,'full_standard_protection':True,'old_Gamma_preserved':True}for p in MINIMUM]+[{'player':'Nahshon Hyland','route':'VII6h_VIII1_RSC','pick':26,'holder':'DEN','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}])
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and POLICY==POLICY_FIXED,'Returned class/option/price/authority altered')

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
    need(src[T4]['approved']['T4']=='Norman Powell remains with Toronto and Rodney Hood remains with Portland','Author T4 owners changed')
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['DEN'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'Paul Millsap'}|{'Nahshon Hyland'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==15,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='DEN'];need([(x['pick'],x['player'])for x in picks]==[(26,'Nahshon Hyland')]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected firstRSC rights changed')
    prior=[x for x in src[PLAYOFF]['games']if 'DEN'in x['teams']];need(len(prior)==6 and all(x['teams']['DEN']['players']['Jamal Murray']['mode']=='MODELED_ABSENT'for x in prior),'SelectedS2Murray absence prior changed')
    need(src[F5]['selected']['F5_MCGEE']=='Denver and Cleveland do not execute their 2021-03-25 JaVale McGee/Isaiah Hartenstein and two-second-round-pick trade; McGee remains with Cleveland and Hartenstein with Denver.'and 'Isaiah Hartenstein'in standard and 'JaVale McGee'not in standard and 'Zeke Nnaji'not in standard,'ApprovedF5/T1 actor direction altered')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds)|{'Nahshon Hyland'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='DEN'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['DEN']=joint.pop('NYK')
        for b in pair:b['DEN']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby'})
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['DEN'])-int(back['CHI']));margin=impact['CHI']-impact['DEN']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'DEN_active':active,'DEN_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_DEN_impact_fraction':str(margin),'CHI_minus_DEN_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'DEN','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_DENVER_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_TWO_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':[],'STD':15,'TW_count':0,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'S2_Murray_prior':{'source':PLAYOFF,'selected6games_modeled_absent_preserved':True,'actual_original_ACL_diagnosis_or_clinical_clearance_certified':False,'new_Barton_and_PJ_operational_recovery_separately_selected':True},'interval':'Only selected Nov19/Dec6 dates; no later original DEN/CLE/ORL or injury/protocol cascade imported','butterfly_handoff':['T1 GordonDEN/NnajiORL plus2020selectedBeyDEN preserved; no originalNnajiDEN roster.','F5 omitted: HartensteinDEN originaloption kept,McGeeCLE; no outgoingtwo2R orLAC_Hartenstein newUPC copied.','Hyland26 selectedright→RSC insteadexpiredMillsap newUPC; originalMillsapBKN not imported.','No JeffGreenDEN/ForbesDEN/HernangomezMEM/BolBOS_ORL/HarrisonPOR orfutureGordonMPJextensions imported.','Murray stays selectedabsent on2dates; BartonPJfiction recovery andMPJworkingavailability notactualclinicalcert.'],'summary':{'selected_games':2,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'DEN_wins':sum(g['selected_regulation_winner']=='DEN'for g in games),'STD':15,'TW':0,'active_each':12,'positive_each':11,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Denver keeper · 두 날짜 선택 결과','','선택된 가상 법적 가족·감독·건강·단일 BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_DEN_impact_per100']:.9f}|")
    a+=['','May16 명명15에서 만료Millsap의 새UPC0와 선택Hyland26 RSC를 연결해15STD0TW. live10+Barton/Green/Hartenstein 원PO 유효행사+Rivers 자기minimum1년+Hyland26. 원earned/protectedΓ·FAhold·waiver/camp/stretch·unsigned·unusedexception/incomplete 비용 함수는 보존한다. 새로운 hardcap trigger없음·과거연도hardcap 소급0이며 wholeprivateledger 인증false.','',
    '원NBA 프로필은 NnajiDEN/McGeeDEN를 포함하지만 승인T1은 NnajiORL/GordonDEN이고 F5거래생략은 HartensteinDEN/McGeeCLE다. 이를 현재S2 seed와 승인원문으로 직접 검문한다. Hartenstein 원PO는 [원Cleveland 프로필](https://www.nba.com/draft/2021/team-profiles/cleveland-cavaliers)의 양도된 동일계약 옵션 분류이며 CLE의 가상소유권이 아니다. 기존원옵션 조건/급여/보호는 유지하고 적법한 가상 통지·행사만 선택한다.','',
    'MPJ RSC의 기존operative4년차 옵션 행사 조건을 보존한다. Gordon/MPJ 실제2021연장은 현재2021급여를 바꾸지 않는 별도 후년 사건이며 자동복사하지 않는다. Howard/Harrison 원TW가 살아 있으면 비양도방출+fullΓ, 만료면 해당STANDARD/TWQO·Oct1미수락 종료·FRN/FAclaims 유지. Howard두시즌/Harrison서비스자격을 둘다신규TW로 자동확정하지 않는다.','',
    '선택S2 여섯 playoff게임의 Murray MODEL_ABSENT를 두 날짜에 유지한다. Barton/PJ는 별도 가상operational회복, MPJ는 선택된 두 날짜 새접촉 backinjury 없음이다. 원MurrayACL·PJACL·MPJ수술/실제COVID/protocol은 임상인증도 자동상속도 아니다. 원역사 사실 자체는 지우지 않는다.','',
    'usual5 Campazzo/Barton/MPJ/Gordon/Jokic. Campazzo24/Barton30/MPJ32/Gordon30/Jokic34/Monte26/Rivers18/Bey16/Green14/Hartenstein12/PJ4=240.11양수+Hyland active12, Murray/Bol/Cancar inactive3. 모든 포지션48분·24×2분 원역할과 CHI Mark32/Caruso18/P32를 동시 연결. 단일March25 EB/BPM·홈2·연전.5, score/OTnull. 원JeffGreen/Forbes/BolBOS_ORL/MillsapBKN/HartensteinLAC/이후원트레이드·신규FA 자동복사0.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|2020–21|완료|','|3|2021–23|DEN2 결과 작업선택·독립검문 대기|','|4|장기 커리어|미완|','|5|결말·구조|미완|','|6|집필 규격·Pack|현행 기능등록기 참조·Pack0|','|7|통합·최종 승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰 묶음5,6번까지4. v0.30 PARTIAL/CLOSED/원고0. whole82/wholemacro3/실제 기관·의학·사적 비용 인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved DEN differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Isaiah Hartenstein')['actual_notice_receipt']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_OPTION_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Nikola Jokic')['bpm']='70.5'
        return x
    with patch(__name__+'.physical',wrongsource):
        try:build()
        except ValueError:controls.append('RETURNED_PHYSICAL_FUTURE_BPM')
        else:raise AssertionError('FalsePASS BPM')
    return controls
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'DEN currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_DEN_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
