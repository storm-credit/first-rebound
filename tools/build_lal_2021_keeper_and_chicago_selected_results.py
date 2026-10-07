"""Two selected Lakers keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_lal_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_LAKERS_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100209','0022100448')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-lal-keeper-20261007/observed_profile.json')
PROFILE_SHA='34a132a241f8adaffb7f3e6805eb00690f65f09647ce0f7c9bdbcb186e0de574'
A='simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json'
PINS[A]='11140e49baa665f18e267fa6419efa238302250b724fa51cfd3262b010b4a312'
LIVE=('Alfonzo McKinnie','Anthony Davis','Kentavious Caldwell-Pope','Kyle Kuzma','LeBron James','Marc Gasol')
OPTIONS={'Montrezl Harrell':'valid original player option exercise'}
MINIMUM=('Andre Drummond','Wesley Matthews','Ben McLemore','Markieff Morris')
ROLE_MINUTES={'PG':{'Dennis Schroder':30,'LeBron James':6,'Talen Horton-Tucker':12},'SG':{'Kentavious Caldwell-Pope':28,'Wesley Matthews':12,'Talen Horton-Tucker':8},'SF':{'LeBron James':28,'Kyle Kuzma':20},'PF':{'Anthony Davis':22,'Montrezl Harrell':12,'Markieff Morris':10,'Kyle Kuzma':4},'C':{'Marc Gasol':14,'Andre Drummond':14,'Montrezl Harrell':8,'Anthony Davis':12}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Dennis Schroder','SG':'Kentavious Caldwell-Pope','SF':'LeBron James','PF':'Anthony Davis','C':'Marc Gasol'}
ROLE_SHA='3b961b878de1f7fd53e2ba78a38f39340e72cfd8dab6fd3616ee0010acd548ca'
EARLY={'route':'VII6b3_EARLY_BIRD','nonoption_seasons':2,'first_base_function':'q in [max(signed2021LegalMinimum(YOS,years1_2),applicable_QO),E]','E':'min(ArticleII7maximum,max(1.75*(priorRegular+priorLikely+priorUnlikely),1.05*priorAveragePlayerSalary_or_statutoryEstimate))','admitted_nonempty_legal_price_domain':True,'later_base':'same q','new_bonus':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None,'timely_operative_2021_QO_before_new_UPC':True,'ordinary_QO':'max(125percent prior regular/likely/unlikely components,applicable minimum+200000; if starter test satisfied and larger,100percent21stRSCanchor base/no bonuses)','starter_criterion':'prior two-season mean or priorseason 41starts/2000minutes; criterion branch not observed certification'}
PRICE={'route':'VII6b2_FULL_BIRD','nonoption_seasons':3,'first_base_function':'q in [14000000,18000000] intersect [legalMinimum,II7maximum]','later_base':'same q','new_bonus':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None,'contract_trade_only_continuity_ATL_OKC_LAL':True}
PRICE_FIXED=deepcopy(PRICE);EARLY_FIXED=deepcopy(EARLY)
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'Caruso':'original LAL expiry then already selected CHI A UPC; no LAL newUPC, all old earnedGamma/FAcharge retained until lawful signedelsewhere adjustment','Dudley':'original expiry, no newUPC; earnedGamma/FAclaims retained, no actual retirement forced','TW':'If original TWlive, lawful nonassignmentwaiver bySep30/full currentprotectedGamma kept; ifexpired, applicable STANDARD/TWQO including consecutive2sameTeam rule timelyoperative2021, unaccepted/unextendedOct1, FRN/FAclaims kept. No newUPC or inferred exactterm.','LeBron_AD':'separate selected operational availability on bothdates; original injury/COVID/postponement not cloned, clinical clearance not certified','whole_private_or_actual_receipts':False}
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
    named={'Trade 2018016':'dennis-schroder','Trade 2019131':'dennis-schroder','Signing 1019145':'talen-horton-tucker','Signing 1033264':'marc-gasol','Trade 2020007':'alfonzo-mckinnie','Signing 1033208':'montrezl-harrell'}
    rows=[r for r in feed if r['GroupSort']in named and r['PLAYER_SLUG']==named[r['GroupSort']]and (r['TEAM_ID']==1610612747 or r['GroupSort']=='Trade 2018016'and r['TEAM_ID']==1610612760)];need(len(rows)==6,'Named tradeonly/own continuity changed')
    need('one hundred twenty-five percent (125%)'in flat(313) and 'twenty-first player'in flat(314),'Nonrookie RFA QO law absent')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True}for p in LIVE]+[{'player':p,'route':q,'original_salary_term_and_Gamma_kept':True,'operative_original_deadline_notice_selected':True,'actual_notice_receipt':None}for p,q in OPTIONS.items()]+[{'player':'Dennis Schroder','route':'NEW_OWN_FA','price_function':deepcopy(PRICE),'old_Gamma_preserved':True},{'player':'Talen Horton-Tucker','route':'NEW_OWN_RFA','price_function':deepcopy(EARLY),'old_Gamma_preserved':True}]+[{'player':p,'route':'VII6i_MINIMUM','seasons':1,'salary':'signed2021LegalMinimum(YOS)','new_bonus':0,'full_standard_protection':True,'old_Gamma_preserved':True}for p in MINIMUM]+[{'player':'Jared Butler','route':'VII6h_VIII1_RSC','pick':22,'holder':'LAL','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}])
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and PRICE==PRICE_FIXED and EARLY==EARLY_FIXED and POLICY==POLICY_FIXED,'Returned class/option/price/authority altered')

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
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['LAL'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'Alex Caruso','Jared Dudley'}|{'Jared Butler'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==14,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='LAL'];need([(x['pick'],x['player'])for x in picks]==[(22,'Jared Butler')]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected firstRSC rights changed')
    need(any(e['id']=='SIGN_CARUSO'and e['player']=='Caruso'for e in src[A]['working_events'])and 'G1A_CARUSO_GROWTH_CORE_DIRECTION'in src[A]['authority']['already_selected'],'Caruso CHI authority missing')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds)|{'Jared Butler'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==2 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='LAL'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['LAL']=joint.pop('NYK')
        for b in pair:b['LAL']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need('Alex Caruso'not in standard and not(set(joint['LAL'])&set(joint['CHI'])),'Caruso/actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby'})
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['LAL'])-int(back['CHI']));margin=impact['CHI']-impact['LAL']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'LAL_active':active,'LAL_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_LAL_impact_fraction':str(margin),'CHI_minus_LAL_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'LAL','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_LAKERS_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_TWO_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':[],'STD':14,'TW_count':0,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'interval':'Only selected Nov15/Dec19 dates; no Westbrook/LAL-WAS trade or original COVID/injury cascade imported','butterfly_handoff':['Caruso already CHI A/18min; no duplicate LAL newUPC or positive role.','Butler22 direct selected right→RSC, no IsaiahJackson22 original Westbrook chain.','No SchroderBOS, Harrell/KCP/KuzmaWAS orGasolMEM assignment copied.','No Howard/Melo/Monk/Ariza/Nunn originalLAL newUPC copied.','LAL two selected allavailable dates are fiction, not actualdiagnosis or COVIDclearance.'],'summary':{'selected_games':2,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'LAL_wins':sum(g['selected_regulation_winner']=='LAL'for g in games),'STD':14,'TW':0,'active_each':12,'positive_each':11,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Lakers keeper · 두 날짜 선택 결과','','선택된 가상 법적 가족·감독·건강·단일 BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_LAL_impact_per100']:.9f}|")
    a+=['','May16 seed15에서 만료 Caruso·Dudley의 새 LAL UPC를 선택하지 않고 Butler22 RSC를 넣어14STD0TW. Caruso는 이미 승인된 Chicago A 계약/18분이며 양팀 동시 소유·출전 중복을 직접 거부한다. Dudley 실제 은퇴/코치직은 자동 복사하지 않는다.','',
    'live6+Harrell 원PO 유효행사+Schroder FullBird3년+THT EarlyBird2년+Drummond/Matthews/McLemore/Markieff 자기 minimum1년+Butler22. Schroder는 ATL→OKC→LAL 원계약 trade-only 연속으로 Bird를 보존하며, THT는2019–21 두 시즌 EarlyBird다. 새 THT 가격은 두 법정minimum·적용 QO 이상이고 VII6b3 E 이하인 비공허 합법 가족. QO는125% 원성분/min+200k/선발조건이면100%21stRSC anchor 함수이며 실제 선발통계·가격·수락을 인증하지 않는다.','',
    '선택된 모든 새 UPC는2021 Aug6 12:02 이후 순서로 체결되는 적법 가상 동의 모델. 기존 보호·earnedΓ, FAhold, waiver/camp/stretch, unsigned, unusedexception, incomplete 비용 함수는 보존된다. 새 hardcap trigger0·2020 hardcap의2021 자동소급0이며 실제 전체 사적 장부 비용 인증은 아니다. TW live면 적법 비양도방출+원 보호Γ, 만료면 해당STANDARD/TWQO 미수락 Oct1 종료와 FRN/FAclaims 유지.','',
    '[원 NBA 프로필](https://www.nba.com/draft/2021/team-profiles/los-angeles-lakers)은 원 계약 구분만 제공한다. Gasol/McKinnie 누락을 만료 증거로 쓰지 않고 S2 live 권리를 유지한다. 원 웹 본문 관측과 직접HTTP403 byte를 분리한다. 실제 원Westbrook 거래·GasolMEM·SchroderBOS·KCP/Kuzma/HarrellWAS와 다른 신규 LAL FA 영입을 복사하지 않는다.','',
    'usual5 Schroder/KCP/LeBron/AD/Gasol. LeBron34/AD34/Schroder30/KCP28/Kuzma24/Harrell20/THT20/Drummond14/Gasol14/Matthews12/Markieff10=240.11양수+Butler active12, McKinnie/McLemore inactive2. Butler는 발달용 active reserve이며 원역사 즉시 기여를 지우는 증거가 아니다. 포지션별48분/24×2분과 CHI32Mark/18Caruso/32P를 동시 연결한다.','',
    'Nov15 연전은 원일정으로 계산하며 Dec19 원COVID/연기 및 LeBron/AD 부상을 가상 건강에 자동복사하지 않는다. 단일March25 EB/BPM·홈2·연전.5 사용, score/OTnull. 원Nov15 clock14398과 대체세계14400은 별도이다. 두 날짜 외 미래 건강/원장 결과를 인증하지 않는다.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|2020–21|완료|','|3|2021–23|LAL2 결과 작업선택·독립검문 대기|','|4|장기 커리어|미완|','|5|결말·구조|미완|','|6|집필 규격·Pack|현행 기능등록기 참조·Pack0|','|7|통합·최종 승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰 묶음5,6번까지4. v0.30 PARTIAL/CLOSED/원고0. whole82/wholemacro3/실제 기관·의학·사적 비용 인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved LAL differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Montrezl Harrell')['actual_notice_receipt']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_OPTION_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='LeBron James')['bpm']='70.5'
        return x
    with patch(__name__+'.physical',wrongsource):
        try:build()
        except ValueError:controls.append('RETURNED_PHYSICAL_FUTURE_BPM')
        else:raise AssertionError('FalsePASS BPM')
    return controls
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'LAL currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_LAL_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
