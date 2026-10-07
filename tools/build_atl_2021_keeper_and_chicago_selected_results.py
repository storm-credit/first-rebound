"""Four selected Atlanta keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_atl_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_ATLANTA_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100502','0022100519','0022100891','0022100710')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-atl-keeper-20261007/observed_profile.json')
PROFILE_SHA='2451068bce00bdee3c629d1ec7cbf42932e2291571b20030c5f072fec57abd2a'
LIVE=('Bogdan Bogdanovic','Bruno Fernando','Cam Reddish','Clint Capela','Danilo Gallinari','De\'Andre Hunter','Kevin Huerter','Onyeka Okongwu','Trae Young')
OPTIONS={'Kris Dunn':'valid original player option exercise'}
SECOND=((47,'Sharife Cooper'),)
SECOND_FIXED=tuple(SECOND)
ROLE_MINUTES={'PG':{'Trae Young':34,'Lou Williams':12,'Kevin Huerter':2},'SG':{'Bogdan Bogdanovic':28,'Kevin Huerter':20},'SF':{'De\'Andre Hunter':28,'Cam Reddish':16,'Kevin Huerter':4},'PF':{'John Collins':22,'Danilo Gallinari':16,'Cam Reddish':4,'Jalen Johnson':6},'C':{'Clint Capela':30,'Onyeka Okongwu':10,'John Collins':8}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Trae Young','SG':'Bogdan Bogdanovic','SF':'De\'Andre Hunter','PF':'John Collins','C':'Clint Capela'}
ROLE_SHA='f861ce42f9cbe5a14c606f46c1c5c80d5897de98d9e59c810caaeb62cea2fde6'
PRICE={'route':'VII6b2_FULL_BIRD','nonoption_seasons':5,'first_base_function':'q in [20000000,25000000] intersect [legalMinimum,II7maximum]','later_base':'same q','new_bonus':0,'options':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None,'continuous2017ATLoriginalRSCservice':True}
PRICE_FIXED=deepcopy(PRICE)
QO={'ordinary':'original4thRSCsalary*(1+operative2017pick19QOincrease)','nonstarter':'lesser(originalOrdinary,pick15RSC120percentQO_with_permitted_anchorBonuses)','latepick_starter_uplift_applies_to_pick19':False,'starter_function':'41GS or2000min priorSeason OR mean two priorSeasons, not actualfuturestats','actual_status_or_price':None}
QO_FIXED=deepcopy(QO)
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'Goodwin':'originalexpiry/applicablevalidQO unacceptedunextendedOct1 or lawfulconsensualwithdrawal,no newUPC; all earnedGamma/FA/FRNclaims preserved','TW':'Original Knight/Mays TWlive lawfulnonassignmentwaiver/fullGamma or expired applicableSTANDARD/TWQO operative2021 unaccepted/unextendedOct1/FRN; newUPC0. No realMIN Knight ornewMaysTW conversion assumed.','availability':'11positive operationalavailable on4selecteddates; Hunter/Reddishworkingrecovery, Okongwu no automaticoldactualshoulderprocedure/contact selected. No automaticCOVID/Hilltornhamstring/clinicalproof; zerobenchclinicalnull.','whole_private_or_actual_receipts':False}
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
    named={'Signing 989324':'john-collins','Signing 1033491':'kris-dunn','Trade 2020070':'lou-williams','Trade 2019145':'tony-snell','Signing 1028087':'brandon-goodwin','Signing 1018882':'bruno-fernando'}
    rows=[r for r in feed if r['TEAM_ID']==1610612737 and r['GroupSort']in named and r['PLAYER_SLUG']==named[r['GroupSort']]];need(len(rows)==6,'Named original own continuity changed')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True,'operative_original_RSC_prior_option_validly_exercised_if_needed':p in('Trae Young','Kevin Huerter','De\'Andre Hunter','Cam Reddish'),'actual_option_receipt':None,'Bruno_2019_second_round_not_RSC':p=='Bruno Fernando'}for p in LIVE]+[{'player':p,'route':q,'original_salary_term_and_Gamma_kept':True,'operative_original_deadline_notice_selected':True,'actual_notice_receipt':None}for p,q in OPTIONS.items()]+[{'player':'John Collins','route':'NEW_OWN_FA','price_function':deepcopy(PRICE),'applicable_prior_QO':deepcopy(QO),'new_contract_years':5,'old_Gamma_QO_FAclaims_preserved':True}]+[{'player':p,'route':'NEW_OWN_FA_MINIMUM','new_contract':'oneSeason applicable2021legalMinimum(YOS) UPC','old_Gamma_FAclaims_preserved':True,'new_bonus':0,'options':0,'full_standard_protection':True,'actual_price_or_receipt':None}for p in('Lou Williams','Tony Snell','Solomon Hill')]+[{'player':'Jalen Johnson','route':'VII6h_VIII1_RSC','pick':19,'holder':'ATL','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}])
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
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['ATL'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'Brandon Goodwin'}|{'Jalen Johnson'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==15,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='ATL'];need([(x['pick'],x['player'])for x in picks]==[(19,'Jalen Johnson'),*SECOND]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected firstRSC rights changed')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds)|{'Tony Snell'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='ATL'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['ATL']=joint.pop('NYK')
        for b in pair:b['ATL']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need(not(set(joint['ATL'])&set(joint['CHI'])),'Actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Jalen Johnson'})
    rates['Jalen Johnson']={'exact_fraction':'-728/1145','method':'SELECTED_FICTIONAL_CONSERVATIVE_ROOKIE_PRIOR_EXISTING_DUARTE_SUGGS_FAMILY','historical_BPM':None,'observed_minutes':None,'fictional_working_coefficient_selected':True,'source_boundary':'Existing conservative working rookie coefficient, not realized2021/22 productivity or originalGSWdraftteam'}
    need(Fraction(rates['Jalen Johnson']['exact_fraction'])==Fraction(src[det.OUT]['player_ratings']['Chris Duarte']['exact_fraction']),'Existing selected rookie prior changed')
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['ATL'])-int(back['CHI']));margin=impact['CHI']-impact['ATL']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'ATL_active':active,'ATL_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_ATL_impact_fraction':str(margin),'CHI_minus_ATL_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'ATL','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_ATLANTA_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_FOUR_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':[],'STD':15,'TW_count':0,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'interval':'Only Dec27/Dec29/Feb24/Mar3 same namedfamily; no automaticoriginalReddishNYK orDunnMEM/BrunoBOS assignment or contact/COVID event','butterfly_handoff':['Jalen19ATL RSC/Sharife47ATL unsignedRT; sourceoriginal20/48 and laterpage2022TyreseMartin51/Rollins44 trade not copied.','DunnoriginalPO/Brunolive retained, BOSselectedAP1keeper ThompsonBOS means no originalThompsonSAC/DunnBrunoBOS bundle.','CollinsownBird5 via original2017ATL RSC, Lou/Snell/Hillownmin1; no arbitraryexistingbonus deletion or newtrade price selected.','Goodwinexpiry newUPC0, TWKnight/Mays operativeQO/nonacceptance/fullGamma conditions preserved; no GoodwinCLE/NateKnightMIN/SharifeoriginalTW copied.','Hunter/Reddishworkingrecovery/Okongwuoperativeavailability separatefiction; no originalCOVID/Hillcontact/TraeHuerterCapelaextensions automatically imported.'],'unsigned2R':[{'pick':n,'player':p,'holder':'ATL','UPC':False,'STD':False,'valid_first_RT':'team-signed oneSeason/legalMinYOS0 delivery inside operativeW21, beforeOct15, acceptanceUntilAtLeastOct15; selectedunaccepted','cost':'outstandingRequiredTender minimum/youngFAfloor normal-apron reservation retained, not new liveSTD','foreign_or_college_newfacts':'X5/X6 reopens; no perpetualrights or actualforeignlawcertificate'}for n,p in SECOND],'summary':{'selected_games':4,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'ATL_wins':sum(g['selected_regulation_winner']=='ATL'for g in games),'STD':15,'TW':0,'active_each':12,'positive_each':11,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Atlanta keeper · 네 날짜 선택 결과','','선택된 가상 법적 가족·감독·건강·단일 BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_ATL_impact_per100']:.9f}|")
    a+=['','May16 seed15의 Goodwin만료/no newUPC 대신선택JalenJohnson19 RSC로15STD0TW. live9+Dunn원PO+CollinsBird5+Lou/Snell/Hill ownmin1+Jalen. Trae/Huerter4·Hunter/Reddish3 원operative옵션의유효통지조건과actualreceiptnull을유지하며원Trae/Huerter/Capela후년extension 자동복사0. Bruno2019secondround는RSC아니다.','',
    'Collins2017ATL RSC→3priorNBAseasons FullBird,5년nonoptionflatq20–25m/법정minimum·IImax교집합·bonus0/fullprotection. 원4thRSCpick19ordinaryQO와비선발15anchor120함수,실제스타터statusnull을별도보존하고같은UPC로서명한뒤hold를이중가산하지않는다. Lou/Snell/Hillownmin1·bonus0/options0/fullprotection은원보고가격이나사적수락인증아니다.','',
    'Goodwin 해당validQO/미수락Oct1 또는합법동의철회후UPC0,earnedΓ/FRN/FAclaims유지. Knight/MaysTWlive면비양도waive/fullΓ,만료면해당STANDARD/TWQO·Oct1미수락/FRN,새UPC0. Sharife47 팀서명1년legalminRT를operativeW21안에제공·최소Oct15수락창/미수락,STD0·FAfloor/RT비용예약·X5/X6재개방 보존. 모든oldcamp/waiver/stretch/FA/unsigned/unusedexception/불완전명단 비용함수 유지·새NTMLE/BAE/Room/S&T0·wholeprivatecert0.','',
    '[NBA 원프로필](https://www.nba.com/draft/2021/team-profiles/atlanta-hawks)의2021FA/PO분류는관측근거이나 페이지속2022TyreseMartin51/Rollins44 거래를2021로복사하지않는다. source원20/48과선택19/47을구분하고web본문관측/HTTP403raw미채택을보존한다. ThompsonBOS selectedAP1 유지로DunnBrunoBOS→ThompsonSAC 원bundle 복사0, CamNYK/GoodwinCLE/KnightMIN새경로도미선택.','',
    'usual5 Trae/Bogdan/Hunter/Collins/Capela. Trae34/Bogdan28/Hunter28/Collins30/Capela30/Huerter26/Reddish20/Gallinari16/Lou12/Okongwu10/Jalen6=240. PG Trae34/Lou12/Huerter2,SG Bogdan28/Huerter20,SF Hunter28/Reddish16/Huerter4,PF Collins22/Gallo16/Reddish4/Jalen6,C Capela30/Okongwu10/Collins8. 11양수+Snellactive12,Dunn/Bruno/Hillinactive3·0분임상사유null. 원common수학fixture를복사하지않고24개2분블록·양팀시계/역할/선수초검문.','',
    'Hunter/Reddish회복·Okongwu가용성/원COVID발생없음은건강위임작업모델,실제임상·백신·surgery부재인증아니다. 선택네날짜외시즌영구고정이나NYKCam캐리임포트주장0. Jalen계수는기존Duarte/Suggs보수적가상prior−728/1145·실제2022stats복사0. 현재CHI32Mark/18Caruso/32P·단일March25 EB/BPM·홈2·연전.5,score/OTnull.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|2020–21|완료|','|3|2021–23|ATL4 결과 작업선택·독립검문 대기|','|4|장기 커리어|미완|','|5|결말·구조|미완|','|6|집필 규격·Pack|현행 기능등록기 참조·Pack0|','|7|통합·최종 승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰묶음5,6번까지4. v0.30 PARTIAL/CLOSED/원고0. wholemacro3/실제기관·의학·사적비용인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved IND differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Kris Dunn')['actual_notice_receipt']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_OPTION_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Trae Young')['bpm']='70.5'
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
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_ATL_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
