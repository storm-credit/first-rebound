"""Two selected Clippers keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_lac_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_CLIPPERS_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100198','0022101149')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-lac-keeper-20261007/observed_profile.json')
PROFILE_SHA='66a7c307bc8418d47f0967afddd74e92e19e4939462938476ca905632221af0e'
PLAYOFF='simulation/NBA_2021_ALL_DATED_PLAYOFF_COACH_PLANS.json'
PINS[PLAYOFF]='27fb630174fb39653738a19e51f0a8d6c969c6397505284e794a7383f6030c99'
LIVE=('Daniel Oturu','Ivica Zubac','Luke Kennard','Marcus Morris Sr.','Patrick Beverley','Paul George','Rajon Rondo','Terance Mann')
OPTIONS={'Kawhi Leonard':'valid original player option exercise','Serge Ibaka':'valid original player option exercise'}
MINIMUM=('Nicolas Batum','Patrick Patterson','DeMarcus Cousins')
ROLE_MINUTES={'PG':{'Reggie Jackson':28,'Patrick Beverley':8,'Rajon Rondo':12},'SG':{'Paul George':12,'Luke Kennard':20,'Patrick Beverley':10,'Terance Mann':6},'SF':{'Kawhi Leonard':24,'Paul George':16,'Terance Mann':8},'PF':{'Marcus Morris Sr.':22,'Kawhi Leonard':10,'Nicolas Batum':10,'Paul George':6},'C':{'Ivica Zubac':26,'Serge Ibaka':10,'Nicolas Batum':6,'Marcus Morris Sr.':6}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Reggie Jackson','SG':'Paul George','SF':'Kawhi Leonard','PF':'Marcus Morris Sr.','C':'Ivica Zubac'}
ROLE_SHA='abbae1f27ba74f06d1f53f186c3c9a7def303a72057c3b615e638cae8a0b724c'
PRICE={'route':'VII6b3_EARLY_BIRD','nonoption_seasons':2,'first_base_function':'q in [max(signed2021LegalMinimum(YOS,years1_2),0.95E),E]','E':'min(ArticleII7maximum,max(1.75*(priorRegular+priorLikely+priorUnlikely),1.05*priorAveragePlayerSalary_or_statutoryEstimate))','later_base':'same q','new_bonus':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None,'original_22m_report_not_exact_new_salary':True}
PRICE_FIXED=deepcopy(PRICE)
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'Ferrell':'expiredROS or lawful nonassignmentwaiver iflive; full original current protected/earnedGamma kept beforeKeonUPC','TW':'If source TWlive, legal nonassignmentwaiver bySep30 and full currentprotectedGamma retained; ifexpired, applicable STANDARD/TW QO validoperative2021 unaccepted/unextendedOct1, FRN/FAclaims retained. No newUPC and no exactoldterm inferred.','Kawhi':'S2 selectedall19playoffgames36min availability carried as fictional prior, separately select working operational availability on both2021-22 dates; originalJuneACL/2022absence not copied','Ibaka':'separate working recovery availability on bothdates; source originalbackinjury not copied as clinical clearance','whole_private_or_actual_receipts':False}
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
    named={'Signing 1028264':'reggie-jackson','Signing 1033677':'reggie-jackson','Signing 1019063':'kawhi-leonard','Signing 1033418':'serge-ibaka','Signing 1033674':'nicolas-batum','Signing 1039668':'yogi-ferrell'}
    rows=[r for r in feed if r['TEAM_ID']==1610612746 and r['GroupSort']in named and r['PLAYER_SLUG']==named[r['GroupSort']]];need(len(rows)==6,'Named current continuity changed')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True}for p in LIVE]+[{'player':p,'route':q,'original_salary_term_and_Gamma_kept':True,'operative_original_deadline_notice_selected':True,'actual_notice_receipt':None}for p,q in OPTIONS.items()]+[{'player':'Reggie Jackson','route':'NEW_OWN_FA','price_function':deepcopy(PRICE),'old_Gamma_preserved':True}]+[{'player':p,'route':'VII6i_MINIMUM','seasons':1,'salary':'signed2021LegalMinimum(YOS)','new_bonus':0,'full_standard_protection':True,'old_Gamma_preserved':True}for p in MINIMUM]+[{'player':'Keon Johnson','route':'VII6h_VIII1_RSC','pick':25,'holder':'LAC','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}])
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and PRICE==PRICE_FIXED and POLICY==POLICY_FIXED,'Returned class/option/price/authority altered')

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
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['LAC'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'Yogi Ferrell'}|{'Keon Johnson'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==15,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='LAC'];need([(x['pick'],x['player'])for x in picks]==[(25,'Keon Johnson')]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected firstRSC rights changed')
    prior=[x for x in src[PLAYOFF]['games']if 'LAC'in x['teams']];need(len(prior)==19 and all(x['teams']['LAC']['planned_minutes']['Kawhi Leonard']==36 for x in prior),'SelectedS2Kawhi availability prior changed')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds)|{'Keon Johnson'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='LAC'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['LAC']=joint.pop('NYK')
        for b in pair:b['LAC']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby'})
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['LAC'])-int(back['CHI']));margin=impact['CHI']-impact['LAC']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'LAC_active':active,'LAC_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_LAC_impact_fraction':str(margin),'CHI_minus_LAC_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'LAC','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_CLIPPERS_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_TWO_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':[],'STD':15,'TW_count':0,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'S2_Kawhi_prior':{'source':PLAYOFF,'working19games36minutes_preserved':True,'actual_original_ACL_or_clinical_clearance_certified':False,'fictional_postseason_contact_not_identical_to_original':True},'interval':'Only selected Nov14/Mar31 dates; no later Bledsoe/Ibaka/Powell/Covington trade imported','butterfly_handoff':['Keon25 direct selected right→RSC; no originalGrimes25/Keon21/Preston33 transaction restored.','No BeverleyMEM/MIN, RondoLAL, BledsoeLAC orIbakaMIL atom copied.','Powellstays approvedPortland; no Powell/CovingtonLAC orWinslowPOR copied.','Kawhi/George/Ibaka datedworkingavailability is selected fiction, not originalACL/elbow/backdiagnosis or2022medical record.'],'summary':{'selected_games':2,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'LAC_wins':sum(g['selected_regulation_winner']=='LAC'for g in games),'STD':15,'TW':0,'active_each':12,'positive_each':11,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Clippers keeper · 두 날짜 선택 결과','','선택된 가상 법적 가족·감독·건강·단일BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_LAC_impact_per100']:.9f}|")
    a+=['','May16 seed15에서 Ferrell ROS만료 또는 live비양도방출을선택해전액원보호Gamma를남기고 Keon25RSC를넣는다. 현live8+Kawhi/Ibaka원PO유효행사+JacksonEarlyBird2년+Batum/Patterson/Cousins자기minimum1년+Keon25=15STD0TW. 실제옵션통지·가격·수락null.','',
    'Jackson은2020중DET방출뒤새LAC UPC와2020재서명으로두precedingseasons만확인되어EarlyBird다. 가격E=min(IImax,max(175%priorRegular+Likely+Unlikely,105%priorAverage_or_estimate)); flat q는[max(2년각법정minimum,95%E),E]의적법비공허가족조건을선택한다. exactAverage/실제q를꾸미지않는다. 기존원보고2년22m는새가격확정이아니다.','',
    '[NBA2021LAC프로필](https://www.nba.com/draft/2021/team-profiles/la-clippers)은원계약구분이다. 직접403본문미채택/웹본문관측분리. Coffey/Scrubb의원TW가live이면9/30까지적법비양도방출+원보호Γ전액보존, 만료이면해당STANDARD/TW QO의유효미수락Oct1종료뒤FRN/FAclaims보존. Scrubb원2년가능성을만료로자동지우지않는다.','',
    'usual5 Jackson/George/Kawhi/Morris/Zubac. Jackson28/George34/Kawhi34/Morris28/Zubac26/Beverley18/Rondo12/Kennard20/Mann14/Batum16/Ibaka10=240,11양수+Keon active12. BatumC6/MorrisC6의소규모smallball과GeorgePF6을명시감독선택했다. 24×2분을현재CHI Mark32/Caruso18/P32와동시초별조인.','',
    'S2선택W4/W5/W7의19경기 Kawhi36분가용prior를보존하며이번두날짜가상operational가용을별도선택. 실제JuneACL/Georgeelbow/Ibakaback/원2022전체부재를상속하지않으며원역사부상사실을삭제하지않는다. 모든oldGamma·미서명·FAhold·TPE·camp/dead/stretch/incomplete비용함수는남는다. 새hardcaptrigger없음, 원2020hardcap은2021새capyear에자동소급0.','',
    '원Bledsoe/MEM/MIN·IbakaMIL·Powell/CovingtonLAC·WinslowPOR·Grimes/Prestontrade자동복사0. 단일March25EB/BPM·홈2·연전.5, score/OTnull. Mar31원역사OT1은별도관측이고우리48분regulation결과에자동추가하지않는다.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020드래프트연쇄|완료|','|2|2020–21|완료|','|3|2021–23|LAC2결과 작업선택·독립검문 대기|','|4|장기커리어|미완|','|5|결말·구조|미완|','|6|집필규격·Pack|현행기능등록기 참조·Pack0|','|7|통합·최종승인|CLOSED|','',
    '[현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은큰묶음5,6번까지4. v0.30 PARTIAL/CLOSED/원고0. whole82/wholemacro3/실제기관·의학·사적비용인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved LAC differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Kawhi Leonard')['actual_notice_receipt']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_OPTION_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Kawhi Leonard')['bpm']='70.5'
        return x
    with patch(__name__+'.physical',wrongsource):
        try:build()
        except ValueError:controls.append('RETURNED_PHYSICAL_FUTURE_BPM')
        else:raise AssertionError('FalsePASS BPM')
    return controls
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'LAC currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_LAC_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
