"""Two selected Indiana keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_ind_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_INDIANA_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100257','0022100499','0022100530','0022100789')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-ind-keeper-20261007/observed_profile.json')
PROFILE_SHA='e7a2bdbecd364dc96142c62e88a5e82a9e7fee0587a4f83d41535b5adc29aa8c'
LIVE=('Aaron Holiday','Caris LeVert','Domantas Sabonis','Goga Bitadze','Jeremy Lamb','Justin Holiday','Kelan Martin','Malcolm Brogdon','Myles Turner','Oshae Brissett','T.J. Warren')
OPTIONS={'Edmond Sumner':'valid original team option exercise'}
ROLE_MINUTES={'PG':{'Malcolm Brogdon':26,'T.J. McConnell':22},'SG':{'Caris LeVert':32,'Malcolm Brogdon':6,'Jeremy Lamb':2,'Edmond Sumner':8},'SF':{'Justin Holiday':26,'Doug McDermott':10,'Jeremy Lamb':12},'PF':{'Domantas Sabonis':30,'Oshae Brissett':6,'Doug McDermott':12},'C':{'Myles Turner':30,'Domantas Sabonis':4,'Goga Bitadze':14}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Malcolm Brogdon','SG':'Caris LeVert','SF':'Justin Holiday','PF':'Domantas Sabonis','C':'Myles Turner'}
ROLE_SHA='c48a68a2d29c00b5be95c19a1dbe5baa034f1b2f183327f6619d044369608b70'
EARLY={'route':'VII6b3_EARLY_BIRD','nonoption_seasons':2,'first_base_function':'q in [max(signed2021LegalMinimum(YOS,years1_2),0.95E),E]','E':'min(ArticleII7maximum,max(1.75*(priorRegular+priorLikely+priorUnlikely),1.05*priorAveragePlayerSalary_or_statutoryEstimate))','admitted_nonempty_legal_price_domain':True,'later_base':'same q','new_bonus':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None}
PRICE={'route':'VII6b2_FULL_BIRD','nonoption_seasons':3,'first_base_function':'q in [8000000,12000000] intersect [legalMinimum,II7maximum]','later_base':'same q','new_bonus':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None,'three_seasons_2018_2021_own_contract_continuity':True}
PRICE_FIXED=deepcopy(PRICE);EARLY_FIXED=deepcopy(EARLY)
SECOND=((54,'Aaron Wiggins'),(60,'Sandro Mamukelashvili'))
SECOND_FIXED=tuple(SECOND)
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'Sampson':'original expiry, no newUPC; all earnedGamma/FAclaims retained; no actualShanghai signing certificate or mandatoryretirement','TW':'If original TWlive, lawful nonassignmentwaiver bySep30/full currentprotectedGamma kept; ifexpired, applicable STANDARD/TWQO consecutiveSameTeam/term/service eligibility timelyoperative2021 unaccepted/unextendedOct1 FRN/FAclaims retained. No newUPC or inferred exactterm. Brimahprofileundercontract notstandardcertificate.','availability':'Warren workingabsent on4dates; Turner separate workingrecovery, Sumner no newselected Achillescontact on4dates; operational available positive11 notactualclinical/positiveCOVIDcertificate','whole_private_or_actual_receipts':False}
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
    named={'Signing 1019311':'tj-mcconnell','Signing 1004104':'doug-mcdermott','Signing 1019312':'edmond-sumner','Signing 1033538':'jakarr-sampson','Signing 1003867':'aaron-holiday','Signing 1039412':'oshae-brissett','Signing 1038629':'oshae-brissett'}
    rows=[r for r in feed if r['TEAM_ID']==1610612754 and r['GroupSort']in named and r['PLAYER_SLUG']==named[r['GroupSort']]];need(len(rows)==7,'Named original own continuity changed')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True,'operative_original_RSC_prior_option_validly_exercised_if_needed':p=='Aaron Holiday','actual_option_receipt':None}for p in LIVE]+[{'player':p,'route':q,'original_salary_term_and_Gamma_kept':True,'operative_original_deadline_notice_selected':True,'actual_notice_receipt':None}for p,q in OPTIONS.items()]+[{'player':'Doug McDermott','route':'NEW_OWN_FA','price_function':deepcopy(PRICE),'old_Gamma_preserved':True},{'player':'T.J. McConnell','route':'NEW_OWN_FA','price_function':deepcopy(EARLY),'old_Gamma_preserved':True}]+[{'player':'Trey Murphy','route':'VII6h_VIII1_RSC','pick':15,'holder':'IND','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}])
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and PRICE==PRICE_FIXED and EARLY==EARLY_FIXED and POLICY==POLICY_FIXED and SECOND==SECOND_FIXED,'Returned class/option/price/authority altered')

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
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['IND'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'JaKarr Sampson'}|{'Trey Murphy'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==15,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='IND'];need([(x['pick'],x['player'])for x in picks]==[(15,'Trey Murphy'),*SECOND]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected firstRSC rights changed')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds)|{'Trey Murphy'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='IND'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['IND']=joint.pop('NYK')
        for b in pair:b['IND']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need(not(set(joint['IND'])&set(joint['CHI'])),'Actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Oshae Brissett'})
    need(not any(x['nba_player']=='Oshae Brissett'for x in src[det.BPM]),'Brissett source n0 changed')
    rates['Oshae Brissett']={'exact_fraction':'0','method':'SELECTED_FICTIONAL_EB_N0_NEUTRAL_LIMIT','historical_BPM':None,'observed_minutes':None,'selected_pseudo_observation_minutes':0,'source_row_exists':False,'actual_ability_zero_certified':False,'fictional_working_coefficient_selected':True,'source_boundary':'FirstIND 10day April1 afterMarch25cutoff; later2021/2022 productivity not imported'}
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['IND'])-int(back['CHI']));margin=impact['CHI']-impact['IND']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'IND_active':active,'IND_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_IND_impact_fraction':str(margin),'CHI_minus_IND_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'IND','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_INDIANA_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_FOUR_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':[],'STD':15,'TW_count':0,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'interval':'Only selected Nov22/Dec26/Dec31/Feb4 dates; no original Feb8 Sabonis/Haliburton or LeVertCLE chain imported','butterfly_handoff':['DuarteCHI preserved; Murphy15 INDselectedright→RSC; Wiggins54/Mamu60 unsigned2R legalRT, no originalIsaiahJackson22/Todd31/MIL chain.','No AaronHolidayWAS/Brogdonextension/LeVertCLE/SabonisSAC/HaliburtonIND/LambSAC newevent copied.','No SumnerBKN original Achillescontact orMcDermottSAS/Brissettstandard↔TWclass copied.','Warren workingabsent on4dates; Turnerrecovery/Sumnernewcontactabsence operationalmodel notactualmedical.'],'unsigned2R':[{'pick':n,'player':p,'holder':'IND','UPC':False,'STD':False,'valid_first_RT':'team-signed oneSeason/legalMinYOS0 delivery inside operativeW21, beforeOct15, acceptanceUntilAtLeastOct15; selectedunaccepted','cost':'outstandingRequiredTender minimum/youngFAfloor normal-apron reservation retained, not new liveSTD','foreign_or_college_newfacts':'X5/X6 reopens; no perpetualrights or actualforeignlawcertificate'}for n,p in SECOND],'summary':{'selected_games':4,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'IND_wins':sum(g['selected_regulation_winner']=='IND'for g in games),'STD':15,'TW':0,'active_each':12,'positive_each':11,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Indiana keeper · 네 날짜 선택 결과','','선택된 가상 법적 가족·감독·건강·단일 BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_IND_impact_per100']:.9f}|")
    a+=['','May16 seed15에서 Sampson 만료후 신규UPC0 대신 선택 Murphy15 RSC를 넣어15STD0TW. live11+Sumner 원teamoption 유효행사+McDermottFullBird3년+McConnellEarlyBird2년+Murphy15. AaronHoliday 원RSC operative4년차 옵션 조건은 유지하고 실제통지 receipt null.','',
    'McDermott2018IND UPC→3priorseasons, McConnell2019IND UPC→2priorseasons이므로 권리를 구분한다. McDermott flat q는8–12m와legalmin/IImax 교집합, McConnell은 두minimum 이상·VII6b3 E이하의 적법 비공허 가족으로 선택. 새보너스0/fullprotection, 실제 원기사 가격·접수·수락은null. 모든 기존Γ·FAhold·camp/waiver/stretch·unsigned·unusedexception/incomplete 함수를 보존하고 새NTMLE/Room/BAE/S&T trigger0,2020hardcap자동소급0.','',
    'Wiggins54/Mamu60은 selectedT1 권리만 연결한다. 팀서명1년minRT를operative2021 창 안에 제공하고 최소Oct15까지수락가능하지만 미수락을선택해NBAUPC0/STD0. 정상·apron 최소/youngfloor예약 보존, X5/X6새notice/foreign계약은 재개방이고 무기한권리나실제기관접수 인증은 아니다. 원Duarte13·IsaiahJackson22·Todd31·MIL 거래를 복사하지 않는다.','',
    '[NBA 원프로필](https://www.nba.com/draft/2021/team-profiles/indiana-pacers)은 원형FA/TO와 계약자를 분리한다. AmidaBrimah undercontract만으로STD 승격하지 않고 S2TW를 따른다. Brimah/Stanley liveTW면 합법비양도방출+원Γ, 만료면해당QO/Oct1미수락종료/FRN·FAclaims 보존. 원retirement/Shanghai/SumnerBKN사건 및 미보고비용0 인증을 추가하지 않는다.','',
    'usual5 Brogdon/LeVert/JustinHoliday/Sabonis/Turner. Brogdon32/LeVert32/JHoliday26/Sabonis34/Turner30/McConnell22/McDermott22/Lamb14/Brissett6/Sumner8/Goga14=240. Goga14 센터·McDermottPF12 stretch4은 명시 감독 선택.11양수+Murphy active12, AaronHoliday/KelanMartin/Warren inactive3. Brissett는원officialGL3년계약/피드ROS불일치를분리보존하고원급여Γ를유지한다. April1원첫10일이cutoff후라가상n0중립prior를선택하며실제능력0이아니다. Warren 작업부재, Turner 가상회복·Sumner 새Achilles접촉 없음은 임상인증이 아닌 건강위임 모델이다.','',
    '네날짜 마지막Feb4는 원Feb8SabonisSAC/LeVertCLE변화 이전이고 거래자동복사0. 단일March25 EB/BPM·홈2·연전.5·현재CHI32Mark/18Caruso/32P, score/OTnull. 네 날짜외 미래 결과/건강/권리재통지 자동실행을 주장하지 않는다.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|2020–21|완료|','|3|2021–23|IND4 결과 작업선택·독립검문 대기|','|4|장기 커리어|미완|','|5|결말·구조|미완|','|6|집필 규격·Pack|현행 기능등록기 참조·Pack0|','|7|통합·최종 승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰 묶음5,6번까지4. v0.30 PARTIAL/CLOSED/원고0. whole82/wholemacro3/실제 기관·의학·사적 비용 인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved IND differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Edmond Sumner')['actual_notice_receipt']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_OPTION_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Malcolm Brogdon')['bpm']='70.5'
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
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_IND_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
