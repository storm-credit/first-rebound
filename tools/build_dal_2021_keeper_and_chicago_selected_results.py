"""Two selected Dallas keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_dal_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_DALLAS_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='4fa062ddabbe97403700544b87d95bb6f8560e0d'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100163','0022100603')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-dal-keeper-20261007/observed_profile.json')
PROFILE_SHA='0241ad6ada7c66dba5716ee68394f777da5f7dc4f1b0db3009f348cf47a185c8'
LIVE=('Dorian Finney-Smith','Dwight Powell','Jalen Brunson','Josh Green','Kristaps Porzingis','Luka Doncic','Maxi Kleber','Trey Burke','R.J. Hampton')
OPTIONS={'Josh Richardson':'valid player option exercise','Willie Cauley-Stein':'valid team option exercise'}
ROLE_MINUTES={'PG':{'Luka Doncic':34,'Jalen Brunson':14},'SG':{'Tim Hardaway Jr.':24,'Jalen Brunson':12,'Josh Richardson':12},'SF':{'Dorian Finney-Smith':18,'Tim Hardaway Jr.':6,'Josh Richardson':10,'R.J. Hampton':6,'Josh Green':8},'PF':{'Dorian Finney-Smith':14,'Kristaps Porzingis':20,'Maxi Kleber':14},'C':{'Kristaps Porzingis':12,'Dwight Powell':22,'Maxi Kleber':8,'Willie Cauley-Stein':6}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Luka Doncic','SG':'Tim Hardaway Jr.','SF':'Dorian Finney-Smith','PF':'Kristaps Porzingis','C':'Dwight Powell'}
ROLE_SHA='765361c438b8d643dd1dd4b4b1d99f5fb7004e66ee9b22697a94e1163aab314f'
PRICE={'route':'VII6b1_FULL_BIRD','seasons':3,'flat_first_base_interval':[14000000,18000000],'new_bonus':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None}
PRICE_FIXED=deepcopy(PRICE)
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'Redick':'expired current UPC, no new agreement; old protected/FA claims retained, retirement not automatically selected','Hampton':'selected DAL current RSC and all Gamma kept; not original ORL or Terry identity','TW':'Hinton/Bey lawful applicable QO, unaccepted/unextended Oct1; no new UPC, FA/FRN claims retained','Melli':'operative timely ordinary nonRSC QO before voluntary minimum UPC replacement; no original foreign signing copied','whole_private_or_actual_receipts':False}
POLICY_FIXED=deepcopy(POLICY)

def direct(root,p):
    t=(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
    return json.loads(t)if p.endswith('.json')else list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else t
def sources(root):return {p:physical(root,p)for p in PINS}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def support():
    need(hashlib.sha256(base.CBA.read_bytes()).hexdigest()==base.CBA_SHA,'CBA raw changed')
    d=fitz.open(base.CBA);pages=(29,30,54,55,58,212,222,223,224,233,240,241,311,312,313,317,318,332,333,334,561)
    tx={n:d[n-1].get_text().replace('\r\n','\n').replace('\r','\n')for n in pages};flat=lambda n:' '.join(tx[n].split())
    need('three (3) preceding Seasons'in flat(29)and 'by means of trade'in flat(29),'FullBird continuity absent')
    need('Minimum Player Salary Exception'in flat(233)and 'first Season covered by the player’s Contract'in flat(55),'Legal minimum family absent')
    need('October 1'in flat(317)and 'Right of First Refusal shall continue'in flat(318),'Unaccepted QO rights absent')
    need(hashlib.sha256(PROFILE.read_bytes()).hexdigest()==PROFILE_SHA,'Profile source observation changed');obs=json.loads(PROFILE.read_text())
    need(hashlib.sha256(Path(obs['raw_path']).read_bytes()).hexdigest()==obs['raw_sha256']and obs['status']==403 and not obs['raw_body_adopted'],'Failed raw promoted')
    need(hashlib.sha256(base.FEED.read_bytes()).hexdigest()==base.FEED_SHA,'Frozen source changed')
    feed=json.loads(base.FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    named={'Trade 2018089':'tim-hardaway-jr','Signing 1019261':'boban-marjanovic','Trade 2020079':'nicolo-melli','Trade 2019132':'josh-richardson','Signing 1033648':'willie-cauley-stein','Signing 1033650':'nate-hinton','Signing 1033574':'tyler-bey'}
    rows=[r for r in feed if r['TEAM_ID']==1610612742 and r['GroupSort']in named and r['PLAYER_SLUG']==named[r['GroupSort']]];need(len(rows)==7,'Named current continuity changed')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True}for p in LIVE]+[{'player':p,'route':q,'original_salary_term_and_Gamma_kept':True,'operative_original_deadline_notice_selected':True,'actual_notice_receipt':None}for p,q in OPTIONS.items()]+[{'player':'Tim Hardaway Jr.','route':'NEW_OWN_FA','price_function':deepcopy(PRICE),'old_Gamma_preserved':True}]+[{'player':p,'route':'VII6i_MINIMUM','seasons':1,'salary':'signed2021LegalMinimum(YOS)','new_bonus':0,'full_standard_protection':True,'old_Gamma_preserved':True}for p in ('Boban Marjanovic','Nicolo Melli')])
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
    need(0<PRICE['flat_first_base_interval'][0]<=PRICE['flat_first_base_interval'][1]<Fraction(112414000,4),'Bird firstyear maximum exceeded')
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['DAL'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'JJ Redick'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==14,'Selected May16/current identities changed')
    need(not seed['DB1_unsigned_conditional_rights']and not[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='DAL'],'Unexpected new drafted actor')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds)|{'Boban Marjanovic'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==2 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='DAL'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['DAL']=joint.pop('NYK')
        for b in pair:b['DAL']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby'})
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['DAL'])-int(back['CHI']));margin=impact['CHI']-impact['DAL']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'DAL_active':active,'DAL_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_DAL_impact_fraction':str(margin),'CHI_minus_DAL_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'DAL','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_DALLAS_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_TWO_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':[],'STD':14,'TW_count':0,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'interval':'Only selected Nov10/Jan9 dates; no later Porzingis trade or fullseason transfer assumption','butterfly_handoff':['Hampton is current DAL identity; neither original ORL Hampton nor original Terry arrival copied. Josh Green remains a separate actor.','No RichardsonBOS/BullockDAL/FrankDAL/SterlingBrownDAL newUPC copied.','No PorzingisWAS/DinwiddieDAL/BertansDAL February atom inherited.','Redick expiration/newagreement0 is working contract choice, not automatic real retirement decision. Hinton/Bey QO/FA/FRN survive without new UPC.'],'summary':{'selected_games':2,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'DAL_wins':sum(g['selected_regulation_winner']=='DAL'for g in games),'STD':14,'TW':0,'active_each':12,'positive_each':11,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Dallas keeper · 두 날짜 선택 결과','','선택된 가상 법적 가족과 감독·건강·단일BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_DAL_impact_per100']:.9f}|")
    a+=['','May16의15명에서 Redick 만료·새UPC0만 선택하여14STD0TW. 원live9/Hampton 실제선택귀속·Richardson/WCS 원옵션 유효행사·THJ FullBird3년14–18m flat/새bonus0·Boban/Melli 자기minimum1년을 구성한다. exact급여·실제수락은null이며 모든원Γ와FA권리·비용을 남긴다. 새NTMLE/BAE/RoomMLE/S&T가 없어 새hardcap을 발명하지 않는다.','',
    '[NBA 공식2021 DAL 프로필](https://www.nba.com/draft/2021/team-profiles/dallas-mavericks)의 계약구분과 동결NBA원거래를 사용했다. 직접HTTP403본문은미채택, 성공한웹본문관측 projection은 rawarticle인증이아니다. Hinton/Bey미수락QO가Oct1뒤expire해도FRN/FAclaim은남는다. Melli의원외국계약/Redick실제은퇴를자동복사하지않는다.','',
    'usual5 Luka/THJ/DFS/KP/Powell. Luka34/THJ30/DFS32/KP32/Powell22/Brunson26/Richardson22/Kleber22/Hampton6/JoshGreen8/WCS6=240.11양수+Boban active12, Trey/Melli inactive2. 각24×2분을 currentCHI Mark32/Caruso18/P32와동시초별조인한다. 원RichardsonBOS/새Bullock·FrankDAL/KP후속WAS거래를자동상속하지않는다.','',
    '동일March25 EB/BPM·홈2·연전.5 작업모델만사용. 원역사score/OT/감염·부상은선택하지않는다. Jan9원minute잔차1초는우리48분계획과별도역사진단이다. 두날짜밖계약·건강·후속거래는재개방.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020드래프트연쇄|완료|','|2|2020–21|완료|','|3|2021–23|DAL2결과 작업선택·독립 검문 대기|','|4|장기커리어|미완|','|5|결말·구조|미완|','|6|집필규격·Pack|현행기능등록기 참조·Pack0|','|7|통합·최종승인|CLOSED|','',
    '[현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은큰묶음5, 6번까지4. v0.30 PARTIAL/CLOSED/원고0. 실제사적·의학·whole82·wholemacro3 인증false.','']
    return '\n'.join(a)
def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved DAL differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Josh Richardson')['actual_notice_receipt']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_OPTION_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Luka Doncic')['bpm']='70.5'
        return x
    with patch(__name__+'.physical',wrongsource):
        try:build()
        except ValueError:controls.append('RETURNED_PHYSICAL_FUTURE_BPM')
        else:raise AssertionError('FalsePASS BPM')
    return controls
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'DAL currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_DAL_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
