"""Two selected Houston keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_hou_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_HOUSTON_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
RSC_PRICE='research/HOU_2021_SELECTED_ROOKIE_SCALE_PRICE_2026_10_07.json'
DET_CHOICE='simulation/DET_ROUTINE_OPERATING_FAMILY_SELECTION_2026_10_07.json'
PINS.update({RSC_PRICE:'eb4bcfe6c3b6be28b23dc6279654671790995b1a59f6c3707c4377f98e47b1eb',DET_CHOICE:'9f9c307f33975de3b3c05734e41f8401cad0439f0446f7bc87aa21d8c7752dc2'})
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100271','0022100459')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-hou-keeper-20261007/observed_profile.json')
PROFILE_SHA='b59acd95fd1699088a289d6479d7d347ce5b0888dd810d88c5a570dcdb36ab55'
LIVE=('Christian Wood','Danuel House Jr.','D.J. Augustin','Eric Gordon','Jae\'Sean Tate','John Wall','KJ Martin','Kevin Porter Jr','Khyri Thomas')
OPTIONS={'Avery Bradley':'valid original team option exercise'}
REMOVED={'Kelly Olynyk','Dante Exum','Sterling Brown','D.J. Wilson'}
ROOKIES=((2,'Jalen Green'),(16,'Alperen Sengun'),(21,'Usman Garuba'),(24,'Josh Christopher'))
ROOKIES_FIXED=tuple(ROOKIES)
ROLE_MINUTES={'PG':{'John Wall':28,'D.J. Augustin':20},'SG':{'Jalen Green':24,'Kevin Porter Jr':24},'SF':{'Danuel House Jr.':20,'Eric Gordon':24,'Kevin Porter Jr':4},'PF':{'Jae\'Sean Tate':30,'David Nwaba':10,'KJ Martin':8},'C':{'Christian Wood':32,'Alperen Sengun':16}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'John Wall','SG':'Jalen Green','SF':'Danuel House Jr.','PF':'Jae\'Sean Tate','C':'Christian Wood'}
ROLE_SHA='9606cef9a55222e2d8e1b121b6b113e2ae861cff73ed0fa595b428011a975a43'
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'expired_four':'Olynyk validexpired→selectedDET; Exum/Brown/Wilson originalexpiry no newHOUUPC; all oldGamma/FA/QO/FRN costclaims retained','TW':'If original TWlive, lawful nonassignmentwaiver bySep30/full currentprotectedGamma kept; ifexpired, applicable STANDARD/TWQO consecutiveSameTeam/term/service eligibility timelyoperative2021 unaccepted/unextendedOct1 FRN/FAclaims retained. No newUPC or inferred exactterm.','availability':'Wall selects cooperative mentor/player28minute role, no originalmutualsit/developmentpolicy automaticinheritance. Gordon/Wood/otherspositive operationalavailable onNov24/Dec20, not actualclinical/COVID/privatevaccination certificate. Zeroreserve notclinicalabsence.','whole_private_or_actual_receipts':False}
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
    named={'Signing 1030929':'david-nwaba','Signing 1040080':'khyri-thomas','Trade 2020073':'avery-bradley','Signing 1033414':'sterling-brown','Trade 2020063':'dj-wilson','Trade 2020053':'dante-exum'}
    rows=[r for r in feed if r['TEAM_ID']==1610612745 and r['GroupSort']in named and r['PLAYER_SLUG']==named[r['GroupSort']]];need(len(rows)==6,'Named original own continuity changed')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True,'operative_original_RSC_prior_option_validly_exercised_if_needed':p=='Kevin Porter Jr','actual_option_receipt':None,'second_round_not_RSC':p=='KJ Martin'}for p in LIVE]+[{'player':p,'route':q,'original_salary_term_and_Gamma_kept':True,'operative_original_deadline_notice_selected':True,'actual_notice_receipt':None}for p,q in OPTIONS.items()]+[{'player':'David Nwaba','route':'NEW_OWN_FA_MINIMUM','new_contract':'oneSeason applicable2021legalMinimum(YOS) UPC','old_Gamma_FAclaims_preserved':True,'new_bonus':0,'options':0,'full_standard_protection':True,'actual_price_or_receipt':None}]+[{'player':p,'route':'VII6h_VIII1_RSC','pick':n,'holder':'HOU','component_scale':['4/5','6/5'],'selected_first_two_salary_function':{f'202{1+y}-2{2+y}':f'1.2*operative_2021_RSC_scale(pick_{n},year_{1+y})'for y in range(2)},'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','new_bonus':0,'guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}for n,p in ROOKIES])
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and POLICY==POLICY_FIXED and ROOKIES==ROOKIES_FIXED,'Returned class/option/price/authority altered')

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
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['HOU'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-REMOVED|{p for n,p in ROOKIES})
    need(set(standard)=={r['player']for r in rows}and len(standard)==15,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='HOU'];need([(x['pick'],x['player'])for x in picks]==list(ROOKIES)and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected RSC rights changed')
    need(src[DET_CHOICE]['status']=='SELECTED_AND_TWO_DATED_REGULATION_IMPLEMENTATIONS_ACCEPTED_WITHIN_PUBLIC_LEGAL_FAMILY'and 'Olynyk3-year caproom'in src[DET_CHOICE]['selected_contract_functions']and 'Kelly Olynyk'not in standard,'Already selected DET Olynyk collision')
    for old in src[RSC_PRICE]['players']:
        r=next(x for x in rows if x['player']==old['player']);need(old['pick']in(2,16)and old['team']=='HOU'and all(r['selected_first_two_salary_function'][k]==v for k,v in old['selected_statutory_salary_function'].items()if k in('2021-22','2022-23'))and old['actual_selected_salary_usd_certified']is None,'Selected existing two rookie price functions changed')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds)|{'Usman Garuba'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='HOU'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['HOU']=joint.pop('NYK')
        for b in pair:b['HOU']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need(not(set(joint['HOU'])&set(joint['CHI'])),'Actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Jalen Green','Alperen Sengun','KJ Martin','Kevin Porter Jr'})
    for p,q in {'KJ Martin':'Kenyon Martin Jr.','Kevin Porter Jr':'Kevin Porter Jr.'}.items():
        rates[p]=det.expected_ratings({det.BPM:src[det.BPM]},{q})[q]
    for p in ('Jalen Green','Alperen Sengun'):
        rates[p]={'exact_fraction':'-728/1145','method':'SELECTED_FICTIONAL_CONSERVATIVE_ROOKIE_PRIOR_EXISTING_DUARTE_SUGGS_FAMILY','historical_BPM':None,'observed_minutes':None,'fictional_working_coefficient_selected':True,'source_boundary':'Existing conservative working rookie coefficient, not actual2021/22 productivity or foreignleagueconversion'}
        need(Fraction(rates[p]['exact_fraction'])==Fraction(src[det.OUT]['player_ratings']['Chris Duarte']['exact_fraction']),'Existing selected rookie prior changed')
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['HOU'])-int(back['CHI']));margin=impact['CHI']-impact['HOU']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'HOU_active':active,'HOU_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_HOU_impact_fraction':str(margin),'CHI_minus_HOU_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'HOU','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_HOUSTON_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_TWO_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':[],'STD':15,'TW_count':0,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'interval':'Only Nov24/Dec20; no original Housewaiver/Wallnonplay policy or later Gordon/Wood trade automatically inherited','butterfly_handoff':['Olynyk already selectedDET q family; no duplicateHOU signing. Olynyk/Exum/SterlingBrown/DJWilson expired newHOUUPC0, existingearnedGamma/FAhold/QO/FRN retained.','Selected T1 Green2/Sengun16/Garuba21/Christopher24 rights become separate routineRSC. Sengun OKC→HOU atom already selected, no duplicateassets/fees. Original Garuba23 not copied.','BradleyvalidTO/Khyricurrentprotectedlive/Nwabaminimum preserved; no originalBradleywaiverLAL/Khyriwaiver/ExumEurope imported.','No GarrisonMathewsclaim/DanielTheis incomingS_and_T/KellyDET originalexactprice copied; oldHarden/Westbrook rights burdens unchanged.','Wall28 cooperative participation selected, no automaticrealmutualsitpolicy; KPJ developmental28/Green24/Sengun16/KJ8 opportunities retained. No2022realstats/clinic imported.'],'rookie_reference_prices':{'source':RSC_PRICE,'selected_statutory_functions_not_exact_reported_UPC':True,'Green_Sengun_prior_selected_functions_preserved':True,'Garuba_Christopher_new_routine_RSC_functions_selected':True,'actual_scale_rounding_or_cents_certified':False},'summary':{'selected_games':2,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'HOU_wins':sum(g['selected_regulation_winner']=='HOU'for g in games),'STD':15,'TW':0,'active_each':12,'positive_each':11,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Houston keeper · 두 날짜 선택 결과','','선택된 가상 법적 가족·감독·건강·단일 BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_HOU_impact_per100']:.9f}|")
    a+=['','May16 seed15에서 Olynyk/Exum/SterlingBrown/DJWilson 만료후새HOU UPC0. 선택 T1의 Green2/Sengun16/Garuba21/Christopher24 RSC로15STD0TW. Olynyk는 이미선택 DET caproom가족에속해HOU중복금지. 기존 HOU earnedΓ/FA/QO/FRN·camp/waiver/stretch/unsigned/exception 비용함수는제거하지않는다.','',
    'live9+Bradley유효TO+Nwaba ownminimum1년+rookie4. KPJ 원RSC operative3년차옵션의 합법통지조건 보존, KJ는2020secondround UPC로RSC취급금지. KhyriMay14 currentcontract를원보호Γ까지유지하며 불필요방출하지않는다. Nwaba2020ownUPC→원profileUFA, 새min법정함수/bonus0/options0/fullprotection, actualprice/수락null. OriginalS&T Wood의2020hardcap은2021연도에자동소급하지않고새NTMLE/BAE/Room/incomingS&T0.','',
    'Green/Sengun은 이미선택된 statutory120% scale 함수2021/22·2022/23을 그대로소비한다. 참고reportedprices를원UPC/법정반올림확정으로승격하지않는다. Garuba21/Christopher24도새루틴RSC120%함수·첫2년보장/후2년옵션·유효RT후합법가상수락으로연결, 실제접수·사적원문null. 기존 Sengun 원자양도는재실행하지않는다.','',
    '[NBA 원프로필](https://www.nba.com/draft/2021/team-profiles/houston-rockets)은 원계약/FA/TO를구분하며 원Garuba23/원역사seasonrecord는대체세계선택이아니다. 현재원webbody관측과직접HTTP403raw를구분한다. TWBrooks/Lamb live면비양도waive/fullΓ; 만료면해당QO·Oct1미수락/FRN·FAclaim보존. 새Garrisonclaim/TheisS&T/BradleyLAL/Khyriwaiver/Exum해외계약/House12월waiver를복사하지않는다.','',
    'usual5 Wall/Green/House/Tate/Wood. Wall28/KPJ28/Green24/Gordon24/Tate30/Wood32/Sengun16/House20/Nwaba10/KJ8/Augustin20=240. PF Tate30/Nwaba10/KJ8, 센터Wood32/Sengun16, 원common수학fixture의Wood48·Olynyk양수를복사하지않는다. 양수11+Garuba active12, Bradley/Khyri/Christopher inactive3·0분임상사유null. Wall은협력하는베테랑/멘토출전28을가상선택하여 원실제mutualsit정책을필수로복사하지않는다. 실제수락/임상진단/백신·프로토콜인증0.','',
    'Green/Sengun 가상prior는 기존Duarte/Suggs와같은 −728/1145, 실제2022stats나유럽리그변환인증없음. 단일March25 EB/BPM·홈2·연전.5·현재CHI32Mark/18Caruso/32P,score/OTnull.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|2020–21|완료|','|3|2021–23|HOU2 결과 작업선택·독립검문 대기|','|4|장기 커리어|미완|','|5|결말·구조|미완|','|6|집필 규격·Pack|현행 기능등록기 참조·Pack0|','|7|통합·최종 승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰 묶음5,6번까지4. v0.30 PARTIAL/CLOSED/원고0. whole82/wholemacro3/실제기관·의학·사적비용 인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved IND differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Avery Bradley')['actual_notice_receipt']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_OPTION_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Christian Wood')['bpm']='70.5'
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
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_HOU_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
