"""Two selected Portland keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_por_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_PORTLAND_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100223','0022100753')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-por-keeper-20261007/observed_profile.json')
PROFILE_SHA='021d78ab896fb43b399ec2c43379c7b89796d20d6e866d463f3714c6edc00608'
T4='canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json'
PINS[T4]='ab996ffb9f9f6e4471ad473633af1529eb4928e3aa9a17b99642c591691c3798'
LIVE=('Anfernee Simons','CJ Elleby','CJ McCollum','Damian Lillard','Jusuf Nurkic','Nassir Little','Robert Covington','Rodney Hood')
OPTIONS={'Derrick Jones Jr.':'valid original player option exercise'}
MINIMUM=('Carmelo Anthony','Enes Kanter','Harry Giles III','Rondae Hollis-Jefferson')
ROLE_MINUTES={'PG':{'Damian Lillard':34,'Anfernee Simons':14},'SG':{'CJ McCollum':28,'Anfernee Simons':6,'Jacob Evans':6,'Rodney Hood':8},'SF':{'Derrick Jones Jr.':22,'Rodney Hood':12,'Nassir Little':8,'CJ McCollum':6},'PF':{'Robert Covington':28,'Carmelo Anthony':20},'C':{'Jusuf Nurkic':30,'Enes Kanter':16,'Robert Covington':2}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Damian Lillard','SG':'CJ McCollum','SF':'Derrick Jones Jr.','PF':'Robert Covington','C':'Jusuf Nurkic'}
ROLE_SHA='7d60ec0a179cde967702600d455d40827b574f541d5f2a00b11f3fa0629e852b'
PRICE={'route':'VII6b2_FULL_BIRD_OWN_RFA','nonoption_seasons':3,'first_base_function':'q in [max(signed2021LegalMinimum(YOS),applicableOrdinaryQO),II7maximum] admitted nonempty legal family','later_base':'same q','new_bonus':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None,'timely_operative2021_QO_if_required':True,'ordinary_QO_function':{'pick':10,'class':2017,'normal':'originalYear4SalaryComponents*(1+pick10_ExhibitBpercentage)','nonstarter':'lesser original package vs pick15_120percent_scale_QO_base/no bonuses','starter':'normal pick10 package; no pick16+ uplift'},'original_SAS_signing_not_imported':True}
PRICE_FIXED=deepcopy(PRICE)
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'JacobEvans':'SourceS2 POR standard contract retained iflive; ifexpired, timely applicableRFAQO and consensual own legalminimum1year newUPC. All original earned/protectedGamma retained. POR37 has no rookie scale; no originalGSW28 RSC or NYwaiver copied.','TW':'If original TWlive, lawful nonassignmentwaiver bySep30/full currentprotectedGamma kept; ifexpired, applicable STANDARD/TWQO including sameTeam term/service eligibility, timelyoperative2021 unaccepted/unextendedOct1 FRN/FAclaims retained. Leaf YOS4 mayrequire STANDARDQO, not newTW by default. No newUPC or inferred exactterm.','availability':'Two selected allpositive operational dates, including Lillard/CJ/Nurkic/Hood and developmentalEvans6. Original Lillard abdominalsurgery/CJlung/Collinsclinicalabsence not copied; reserveclinicalnull.','whole_private_or_actual_receipts':False}
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
    named={'Signing 1033175':'rodney-hood','Signing 1033176':'derrick-jones-jr','Signing 989365':'zach-collins','Signing 1033199':'carmelo-anthony','Signing 1033201':'harry-giles-iii','Signing 1039628':'rondae-hollis-jefferson','Signing 1004041':'anfernee-simons','Signing 1018639':'nassir-little','Signing 1033200':'cj-elleby'}
    rows=[r for r in feed if r['TEAM_ID']==1610612757 and r['GroupSort']in named and r['PLAYER_SLUG']==named[r['GroupSort']]];need(len(rows)==9,'Named original live/own continuity changed')
    need('fifteenth player'in flat(311) and 'lesser of'in flat(311),'OrdinaryRSC nonstarter law absent')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True,'operative_original_RSC_prior_option_validly_exercised_if_needed':p in ('Anfernee Simons','Nassir Little'),'actual_option_receipt':None}for p in LIVE]+[{'player':p,'route':q,'original_salary_term_and_Gamma_kept':True,'operative_original_deadline_notice_selected':True,'actual_notice_receipt':None}for p,q in OPTIONS.items()]+[{'player':'Zach Collins','route':'NEW_OWN_RFA','price_function':deepcopy(PRICE),'old_Gamma_preserved':True}]+[{'player':p,'route':'VII6i_MINIMUM','seasons':1,'salary':'signed2021LegalMinimum(YOS)','new_bonus':0,'full_standard_protection':True,'old_Gamma_preserved':True}for p in MINIMUM]+[{'player':'Jacob Evans','route':'S2_SELECTED_POR_STANDARD_LIVE_OR_EXPIRED_NEW_OWN_MINIMUM','source2018_pick':37,'no_RSC':True,'original_price_term_not_copied':True,'iflive':'retain original UPC salary/term/Gamma','ifexpired':'operative applicable QO ifRFA then voluntary own1year legalminimum UPC/no new bonus/full protection','all_old_Gamma_preserved':True,'actual_new_price':None,'actual_acceptance':None}])
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
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['POR'];standard=sorted(seed['standard_named_continuation_condition_max15'])
    need(set(standard)=={r['player']for r in rows}and len(standard)==15,'Selected May16/current identities changed')
    need(not any(x['conditional_final_draft_rights_holder']=='POR'for x in src[base.DRAFT]['selected_rows']),'No originalGregBrown43 rights imported')
    need(src[T4]['approved']['T4']=='Norman Powell remains with Toronto and Rodney Hood remains with Portland'and 'Norman Powell'not in standard and 'Jacob Evans'in standard,'SelectedT4 actors changed')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds)|{'CJ Elleby'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='POR'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['POR']=joint.pop('NYK')
        for b in pair:b['POR']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need(not(set(joint['POR'])&set(joint['CHI'])),'Actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Enes Kanter','Jacob Evans'})
    rates['Enes Kanter']=det.expected_ratings({det.BPM:src[det.BPM]},{'Enes Freedom'})['Enes Freedom'];rates['Enes Kanter']['source_alias']='March25CSV archive EnesKanter/NBAnameEnesFreedom; dated2021actor unchanged'
    need(not any(x['nba_player']=='Jacob Evans'for x in src[det.BPM]),'Evans n0 source changed')
    rates['Jacob Evans']={'exact_fraction':'0','method':'SELECTED_FICTIONAL_EB_N0_NEUTRAL_LIMIT','historical_BPM':None,'observed_minutes':None,'selected_pseudo_observation_minutes':0,'source_row_exists':False,'actual_ability_zero_certified':False,'fictional_working_coefficient_selected':True}
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['POR'])-int(back['CHI']));margin=impact['CHI']-impact['POR']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'POR_active':active,'POR_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_POR_impact_fraction':str(margin),'CHI_minus_POR_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'POR','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_PORTLAND_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_TWO_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':[],'STD':15,'TW_count':0,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'interval':'Only selected Nov17/Jan30 dates; no original later Portland transactions/medical cascade imported','butterfly_handoff':['T4 Hood POR/Powell TOR preserved; no originalPowellPOR newUPC orTOR3actor assignment.','JacobEvansPOR37 standard notTyrekeEvans/notGSW28 RSC; EnesKanter alias source notnewactor.','No NanceCHI(MarkM1 changedchain),JonesCHI,GilesLAC,HoodTOR/MIL,KanterBOS,MeloLAL,CollinsSAS newatom imported.','No original CJ/NanceNOP orPowell/CovingtonLAC February trades imported; Jan30 scope precedes them anyway.','No originalGregBrown43 cash/pick trade ornewUPC imported.','Datedfictional availability and Evans n0 coefficient are not NBAclinical/ability records.'],'summary':{'selected_games':2,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'POR_wins':sum(g['selected_regulation_winner']=='POR'for g in games),'STD':15,'TW':0,'active_each':12,'positive_each':11,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Portland keeper · 두 날짜 선택 결과','','선택된 가상 법적 가족·감독·건강·단일 BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_POR_impact_per100']:.9f}|")
    a+=['','S2 May16 명명15를 보존하고 새 DB1 신인권리0. 원T4 Hood POR/Powell TOR를 유지한다. Simons4년차/Little3년차는 원RSC 옵션의 유효한 기존 operative 통지·행사 가족을 명시하고 실제 receipt는null이다. live8+Jones 원PO 유효행사+Collins FullBird3년+Anthony/Kanter/Giles/RHJ 자기 minimum1년+JacobEvans 기존표준 live 또는 만료후 자기 minimum1년=15STD0TW. 모든 oldΓ 보존, 정확 원가격/사적 수락·접수 인증은 아니다.','',
    'Evans는 POR37이라 Rookie Scale Contract를 새로 만들지 않는다. 현재 live면 원UPC 유지, 만료면 해당RFA QO를 유효하게 제공하고 가상 합의로 법정minimum 신규1년을 체결한다. 실제 GSW28 원계약·NY방출·다른소속을 복사하지 않는다. 양수6분은 성장과 기회를 여는 감독 선택, n0 EB중립prior는 March25행 없음의 작업계수 한계이며 실제 능력0/실패 판정이 아니다.','',
    'Collins는2017 POR#10 원RSC 연속으로 FullBird이며 새3년 비옵션 flat q는 max(법정minimum,적용ordinaryQO)와II최대 사이의 합법 비공허 가족이다. #10 ordinary의 성분증가와 비선발일때 lesser original vs15번120%anchor를 구분한다. 실제 SAS계약·가격·원건강을 소급하지 않는다. TW Blevins/Leaf 원term 살아 있으면 비양도방출+전액보호Γ, 만료면 해당STANDARD/TWQO·Oct1미수락 종료/FRN·FAclaims 유지; Leaf4YOS면 STANDARDQO 필요성을 보존한다.','',
    '[NBA 원 프로필](https://www.nba.com/draft/2021/team-profiles/portland-trail-blazers)의 Powell POR분류는 승인T4와 다르다. Hood/Evans의 원본문 누락을 만료로 해석하지 않는다. originalmovement는 원관측만이며 실제기사 가격·접수와 대체세계 합의를 분리한다. 새NTMLE/BAE/Room/S&T hardcaptrigger없음, 기존부채/FA/unsigned/예외/incomplete 함수는 남긴다.','',
    'Dame34/CJ34/Nurk30/Cov30/Jones22/Hood20/Simons20/Carmelo20/Kanter16/Little8/Evans6=240. usual5 Dame/CJ/Jones/Cov/Nurk,11양수+Elleby active12, Giles/RHJ/Collins inactive3. SF·PF와 Cov C2 smallball을 명시. 모든currentCHI Mark32/Caruso18/P32와 각2880초 동시 연결. 두 날짜 새가상 operational가용이고 Lillard수술/CJ기흉/Collins부재 실제임상 복사0.','',
    '원Nance3팀 거래는 Markkanen M1변경으로 그대로 연결하지 않으며 JonesCHI/원PowellPOR/GregBrown43/CJ_NanceNOP/PowellCovingtonLAC/HoodTOR_MIL 자동복사0. 단일March25 EB/BPM·홈2·연전.5, score/OTnull. 기존경기승패를 결과로 복사하지 않는다.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|2020–21|완료|','|3|2021–23|POR2 결과 작업선택·독립검문 대기|','|4|장기 커리어|미완|','|5|결말·구조|미완|','|6|집필 규격·Pack|현행 기능등록기 참조·Pack0|','|7|통합·최종 승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰 묶음5,6번까지4. v0.30 PARTIAL/CLOSED/원고0. whole82/wholemacro3/실제 기관·의학·사적 비용 인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved POR differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Derrick Jones Jr.')['actual_notice_receipt']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_OPTION_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Damian Lillard')['bpm']='70.5'
        return x
    with patch(__name__+'.physical',wrongsource):
        try:build()
        except ValueError:controls.append('RETURNED_PHYSICAL_FUTURE_BPM')
        else:raise AssertionError('FalsePASS BPM')
    return controls
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'POR currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_POR_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
