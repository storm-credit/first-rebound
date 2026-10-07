"""Four selected Cleveland keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_cle_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_CLEVELAND_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
F5='canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json'
PINS[F5]='c0166bba7a0874aa08dfa88e7d00c0f0d0e237ca2090459ddd6167cf1353c5ea'
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100367','0022100673','0022101006','0022101110')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-cle-keeper-20261007/observed_profile.json')
PROFILE_SHA='ac973040d60d974b97ef0c274f3b8cedd5d19e6d5b6438d6d56496c33fe3a3a0'
LIVE=('Cedi Osman','Collin Sexton','Damyean Dotson','Darius Garland','Dean Wade','Dylan Windler','Isaac Okoro','Kevin Love','Lamar Stevens','Larry Nance Jr.','Mfiondu Kabengele','Taurean Prince')
ROLE_MINUTES={'PG':{'Darius Garland':30,'Collin Sexton':18},'SG':{'Collin Sexton':12,'Isaac Okoro':24,'Cedi Osman':12},'SF':{'Taurean Prince':20,'Cedi Osman':6,'Jonathan Kuminga':14,'Larry Nance Jr.':8},'PF':{'Larry Nance Jr.':20,'Kevin Love':18,'Dean Wade':10},'C':{'Jarrett Allen':30,'JaVale McGee':12,'Kevin Love':6}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Darius Garland','SG':'Collin Sexton','SF':'Taurean Prince','PF':'Larry Nance Jr.','C':'Jarrett Allen'}
ROLE_SHA='47887986f64c43a091c4c9597efa313a219fc839908778bc506fee2b663049a4'
PRICE={'route':'VII6b2_FULL_BIRD','nonoption_seasons':3,'first_base_function':'q in [15000000,20000000] intersect [legalMinimum,II7maximum]','later_base':'same q','new_bonus':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None,'continuous2017BKNcontract_transferredJan2021CLE_notnewservice':True}
PRICE_FIXED=deepcopy(PRICE)
QO={'ordinary':'original4thRSCsalary*(1+operative2017pick22QOincrease)','starter_if_qualifies':'max(originalOrdinary,pick21RSC100percentQO_with_permitted_anchorBonuses)','nonstarter':'lesser(originalOrdinary,pick15RSC120percentQO_with_permitted_anchorBonuses)','starter_function':'41GS or2000min priorSeason OR mean two priorSeasons, not actualfuturestats','actual_status_or_price':None}
QO_FIXED=deepcopy(QO)
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'Dellavedova':'originalexpiry/no newNBAUPC, all earnedGamma/FAclaims preserved; no realMelbourne signing certificate','TW':'If original TWlive, lawful nonassignmentwaiver bySep30/full currentprotectedGamma kept; ifexpired, applicable STANDARD/TWQO consecutiveSameTeam/term/service eligibility timelyoperative2021 unaccepted/unextendedOct1 FRN/FAclaims retained. No newUPC or inferred exactterm.','availability':'11positive operationalavailable on4selecteddates; Love/Nanceworkingrecovery, Sexton no changedcontactkneeinjury selected; not actualclinical/positiveCOVID/wholeyearhealthcertification. zeroreserveclinicalnull.','whole_private_or_actual_receipts':False}
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
    named={'Trade 2020053':'jarrett-allen','Trade 2020007':'javale-mcgee','Signing 1033353':'matthew-dellavedova','Signing 1039683':'mfiondu-kabengele','Signing 1006569':'larry-nance-jr','Trade 2020052':'taurean-prince'}
    rows=[r for r in feed if r['TEAM_ID']==1610612739 and r['GroupSort']in named and r['PLAYER_SLUG']==named[r['GroupSort']]];need(len(rows)==6,'Named original own continuity changed')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True,'operative_original_RSC_prior_option_validly_exercised_if_needed':p in('Collin Sexton','Darius Garland'),'actual_option_receipt':None,'Kabengele_ROS_multiyear_original_uncertainty_preserved':p=='Mfiondu Kabengele'}for p in LIVE]+[{'player':'Jarrett Allen','route':'NEW_OWN_FA','price_function':deepcopy(PRICE),'applicable_prior_QO':deepcopy(QO),'new_contract_years':4,'old_Gamma_QO_FAclaims_preserved':True},{'player':'JaVale McGee','route':'NEW_OWN_FA_MINIMUM','new_contract':'oneSeason applicable2021legalMinimum(YOS) UPC','old_Gamma_FAclaims_preserved':True,'new_bonus':0,'options':0,'full_standard_protection':True,'actual_price_or_receipt':None},{'player':'Jonathan Kuminga','route':'VII6h_VIII1_RSC','pick':6,'holder':'CLE','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}])
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and PRICE==PRICE_FIXED and QO==QO_FIXED and POLICY==POLICY_FIXED,'Returned class/option/price/authority altered')

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
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['CLE'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'Matthew Dellavedova'}|{'Jonathan Kuminga'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==15 and 'JaVale McGee'in standard and 'Isaiah Hartenstein'not in standard,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='CLE'];need([(x['pick'],x['player'])for x in picks]==[(6,'Jonathan Kuminga')]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected firstRSC rights changed')
    need(src[F5]['selected']['F5_MCGEE']=='Denver and Cleveland do not execute their 2021-03-25 JaVale McGee/Isaiah Hartenstein and two-second-round-pick trade; McGee remains with Cleveland and Hartenstein with Denver.','Approved omitted F5 direction changed')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds)|{'Lamar Stevens'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='CLE'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['CLE']=joint.pop('NYK')
        for b in pair:b['CLE']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need(not(set(joint['CLE'])&set(joint['CHI'])),'Actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Jonathan Kuminga'})
    rates['Jonathan Kuminga']={'exact_fraction':'-728/1145','method':'SELECTED_FICTIONAL_CONSERVATIVE_ROOKIE_PRIOR_EXISTING_DUARTE_SUGGS_FAMILY','historical_BPM':None,'observed_minutes':None,'fictional_working_coefficient_selected':True,'source_boundary':'Existing conservative working rookie coefficient, not realized2021/22 productivity or originalGSWdraftteam'}
    need(Fraction(rates['Jonathan Kuminga']['exact_fraction'])==Fraction(src[det.OUT]['player_ratings']['Chris Duarte']['exact_fraction']),'Existing selected rookie prior changed')
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['CLE'])-int(back['CHI']));margin=impact['CHI']-impact['CLE']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'CLE_active':active,'CLE_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_CLE_impact_fraction':str(margin),'CHI_minus_CLE_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'CLE','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_CLEVELAND_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_FOUR_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':[],'STD':15,'TW_count':0,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'interval':'Only Dec8/Jan19/Mar12/Mar26 retainedfamily; no automaticFebLeVertdeal or originalknee/protocol/calendar imported','butterfly_handoff':['ApprovedF5omission McGeeCLE/HartensteinDEN preserved; originalPHX McGeesigning no duplicate. Kuminga6CLE notMobley3CLE; Mobley3ORLselected.','Allen2017BKNsamecontract→Jan2021CLE transfer qualifiesFullBird3; ordinaryRSCQO/latepickstarter21/nonstarter15 functions preserved before separate4yearUPC.','No originalMarkkanenCHI→CLE/NanceCLE→POR/PrinceMIN/RubioMIN→CLE or FebLeVertIND→CLE copied; currentM1MarkCHI/retainedCLEactors unchanged.','Dellavedovaexpiry/noUPC, nooriginalMelbourne orVarejaoC2signing copied; originalKabengele termuncertainty/Gamma retained.','Love/Nancerecovery/Sextonnewcontactnotselected operationmodel notrealdiagnosis or actualknee injurydisproved.'],'summary':{'selected_games':4,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'CLE_wins':sum(g['selected_regulation_winner']=='CLE'for g in games),'STD':15,'TW':0,'active_each':12,'positive_each':11,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Cleveland keeper · 네 날짜 선택 결과','','선택된 가상 법적 가족·감독·건강·단일 BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_CLE_impact_per100']:.9f}|")
    a+=['','May16 seed15의 Dellavedova만료/newUPC0 대신 선택Kuminga6 RSC를연결해15STD0TW. live12+AllenFullBird4년+McGeeownmin1+Kuminga. 승인F5 omission McGeeCLE/HartensteinDEN을exactsource로대조하며원McGeePHX계약을복사하지않는다. Sexton4/Garland3 원operative옵션통지조건, Kabengele originalROS/후년조항불확실성·급여Γ 유지·actualreceipt null.','',
    'Allen2017BKN원RSC가Jan2021CLE로양도되어3priorseasons FullBird를보존한다. 원4thRSCordinaryraise/latepick22스타터21anchor·비선발15anchor120 QO함수와별도로4년nonoptionflatq15–20m/법정minimum·IImax 교집합·bonus0/fullprotection UPC를가상선택한다. 실제수락/가격/스타터/원급여추정0. McGeeownminimum1년/bonus0/options0/fullprotection, earnedΓ와모든과거FA/QO/FRN/camp/waiver/stretch/unsigned/unusedexception/불완전명단 비용함수 유지. 신규NTMLE/BAE/Room/S&T0,원2020hardcap을자동재사용하지않는다.','',
    'Brodric/Jeremiah TWlive면법적비양도waive/fullΓ, 만료면해당STANDARD/TWQO·Oct1미수락/FRN 유지; 원2021NBA기관접수/해외새계약이나임상인증이아니다. [NBA 원프로필](https://www.nba.com/draft/2021/team-profiles/cleveland-cavaliers)의원HartPO/Mobley3와selectedMcGeeCLE/Kuminga6를구분하고web관측과HTTP403raw본문미채택을보존한다.','',
    'usual5 Garland/Sexton/Prince/Nance/Allen. Garland30/Sexton30/Okoro24/Prince20/Cedi18/Nance28/Love24/Allen30/McGee12/Wade10/Kuminga14=240. PG Garland30/Sexton18,SG Sexton12/Okoro24/Cedi12,SF Prince20/Cedi6/Kuminga14/Nance8,PF Nance20/Love18/Wade10,C Allen30/McGee12/Love6. 양수11+Lamar active12,Dotson/Windler/Kabengeleinactive3. 선택감독24개2분블록·소속/포지션/선수초/CHI동시시계 원형대조. Love/Nance회복·Sexton새접촉부재는운영가상건강이고실제knee/protocol/wholeyear임상인증아니다.','',
    'M1MarkChicago잔류 보존, 원MarkCLE/NancePOR/PrinceMIN/RubioCLE/LeVertCLE/MobleyCLE 나비효과거래를자동복사하지않는다. VarejaoC2생략도새복귀로되돌리지않는다. Kuminga계수는기존Duarte/Suggs와같은 보수적가상rookieprior−728/1145, 실제2022stats/원GSW활약복사0.','',
    '현재CHI Mark32/Caruso18/P32·날짜별선택건강,단일March25 EB/BPM·홈2·연전.5,원역사점수·OT복사0. score/OTnull,whole82/순위/미래우승자동확정0.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|2020–21|완료|','|3|2021–23|CLE4 결과 작업선택·독립검문 대기|','|4|장기 커리어|미완|','|5|결말·구조|미완|','|6|집필 규격·Pack|현행 기능등록기 참조·Pack0|','|7|통합·최종 승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰묶음5,6번까지4. v0.30 PARTIAL/CLOSED/원고0. wholemacro3/실제기관·의학·사적비용인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved IND differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='JaVale McGee')['actual_price_or_receipt']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_PRICE_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Darius Garland')['bpm']='70.5'
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
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_CLE_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
