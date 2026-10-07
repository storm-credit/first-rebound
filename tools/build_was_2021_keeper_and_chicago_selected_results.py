"""Three selected Washington keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_was_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_WASHINGTON_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100541','0022100585','0022101132')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-was-keeper-20261007/observed_profile.json')
PROFILE_SHA='1000dbec56806bedf5f9a82e17557aba4fe35fb37e37c1c31e54878cfa6efb24'
LIVE=('Anthony Gill','Bradley Beal','Daniel Gafford','Davis Bertans','Deni Avdija','Rui Hachimura','Russell Westbrook','Thomas Bryant','Troy Brown Jr.')
OPTIONS={}
SECOND=();SECOND_FIXED=tuple(SECOND)
ROLE_MINUTES={'PG':{'Russell Westbrook':34,'Raul Neto':14},'SG':{'Bradley Beal':32,'Gary Trent Jr.':16},'SF':{'Gary Trent Jr.':12,'Deni Avdija':20,'Corey Kispert':10,'Troy Brown Jr.':6},'PF':{'Rui Hachimura':26,'Davis Bertans':18,'Deni Avdija':4},'C':{'Daniel Gafford':24,'Robin Lopez':16,'Alex Len':8}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Russell Westbrook','SG':'Bradley Beal','SF':'Gary Trent Jr.','PF':'Rui Hachimura','C':'Daniel Gafford'}
ROLE_SHA='b4346cca981c7d94eed3069aae7ce2226603116900dd4b0d1a3d8d8444582c45'
PRICE={'route':'VII6b2_FULL_BIRD','nonoption_seasons':3,'first_base_function':'q in [10000000,14000000] intersect [legalMinimum,II7maximum]','later_base':'same q','new_bonus':0,'options':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None,'original2018POR3seasons_trades_only_do_not_break_Bird':True}
PRICE_FIXED=deepcopy(PRICE)
QO={'ordinary':'max(125percentPriorBasePlusLikelyBonus,legalMinimum2021(YOS)+200000)','rookie_scale_QO_anchor_not_applicable_to_2018secondround37':True,'actual_status_or_price':None}
QO_FIXED=deepcopy(QO)
ISH={'route':'VII6b3_EARLY_BIRD','two_prior2019_20_2020_21_WASseasons':True,'nonoption_seasons':2,'first_base_function':'q in [5000000,7000000] intersect [legalMinimum,max(175percentPriorSalaryInclusiveRequiredBonus,105percentApplicableAveragePlayerSalary)]','later_base':'same q','new_bonus':0,'options':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None}
ISH_FIXED=deepcopy(ISH)
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'Homesley':'lawful nonassignmentwaiver beforeKispertUPC/full currentearned protected bonusGamma retained; no stretch/setoff/actualwaiverreceipt','Bonga':'selected existing X6 nonprofessional-development branch; natural2021SubsequentDraft noRedraft in selected60/noNBAUPC yieldsRookieFA; oldRT/earnedGamma preserved, no foreverexclusive rights. Actual foreignclassification oroldpastnotice certifiedfalse.','TW':'Mathews consecutiveWAS twooneSeasonTW->STANDARDQO notTW50k; Winston firstTW ordinaryTWQO/YOSeligibility with normalminimumFAfloor retained. Applicable unaccepted/unextendedQOsOct1/FRN orlawfulconsensualwithdrawal, no newUPCs/conversion; no livingQO renouncedfirst.','availability':'12positive operationalavailable on3dates; Bryant0 explicitly delayedworkingrecovery notclinicalproof; Rui/Beal cooperation/contactavailability selected, no copiedrealmentalhealth/COVID/BealFebsurgery ororiginalJan12Bryantreturn.','whole_private_or_actual_receipts':False}
POLICY_FIXED=deepcopy(POLICY)
EXTRA=('research/CHA_WAS_FINITE_ROSTER_WORKING_FAMILY_2026_10_07.json','research/WASHINGTON_2021_REMAINING_INVENTORY_FAMILY_2026_10_07.json')
PINS.update({EXTRA[0]:'b06b071a0bf77bbff05d01d8adfa62472b4c3b90cca8aa2373ced9034712899a',EXTRA[1]:'aff173a27d8338382699ef2981d1e376945e1dd60a98beb6b8453f3a175898ce'})
EXTRA_MEANING={EXTRA[0]:'11c76907330a54e7ed5126e8268a37de37a8c5777b4ab842569e6f65ea8d006f',EXTRA[1]:'9509e65c7c37d8ca27396a026021a057d5b9c4eb85c2d96d5b8dda6ae211b5cb'}

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
    named={'Signing 1004098':('gary-trent-jr',1610612757),'Signing 1019023':('ish-smith',1610612764),'Signing 1040131':('caleb-homesley',1610612764)}
    rows=[r for r in feed if r['GroupSort']in named and (r['PLAYER_SLUG'],r['TEAM_ID'])==named[r['GroupSort']]];need(len(rows)==3,'Named original own continuity changed')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True,'operative_original_RSC_prior_option_validly_exercised_if_needed':p in('Deni Avdija','Rui Hachimura','Troy Brown Jr.'),'actual_option_receipt':None,'no_new_originalBealGaffordextension_orWestbrooktrade':True}for p in LIVE]+[{'player':'Gary Trent Jr.','route':'NEW_OWN_FA','price_function':deepcopy(PRICE),'applicable_prior_QO':deepcopy(QO),'new_contract_years':3,'old_Gamma_QO_FAclaims_preserved':True}]+[{'player':'Ish Smith','route':'NEW_OWN_FA','price_function':deepcopy(ISH),'new_contract_years':2,'old_Gamma_FAclaims_preserved':True}]+[{'player':p,'route':'NEW_OWN_FA_MINIMUM','new_contract':'oneSeason applicable2021legalMinimum(YOS) UPC','old_Gamma_FAclaims_preserved':True,'new_bonus':0,'options':0,'full_standard_protection':True,'actual_price_or_receipt':None}for p in('Raul Neto','Alex Len','Robin Lopez')]+[{'player':'Corey Kispert','route':'VII6h_VIII1_RSC','pick':12,'holder':'WAS','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}])
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and PRICE==PRICE_FIXED and QO==QO_FIXED and ISH==ISH_FIXED and POLICY==POLICY_FIXED and SECOND==SECOND_FIXED,'Returned class/option/price/authority altered')

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
    need(all(digest(src[p])==EXTRA_MEANING[p] for p in EXTRA),'Selected Bonga/Mathews/Winston ancestor meaning changed');raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['WAS'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'Caleb Homesley'}|{'Corey Kispert'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==15,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='WAS'];need([(x['pick'],x['player'])for x in picks]==[(12,'Corey Kispert'),*SECOND]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected firstRSC rights changed')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds));inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='WAS'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['WAS']=joint.pop('NYK')
        for b in pair:b['WAS']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need(not(set(joint['WAS'])&set(joint['CHI'])),'Actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Corey Kispert'})
    rates['Corey Kispert']={'exact_fraction':'-728/1145','method':'SELECTED_FICTIONAL_CONSERVATIVE_ROOKIE_PRIOR_EXISTING_DUARTE_SUGGS_FAMILY','historical_BPM':None,'observed_minutes':None,'fictional_working_coefficient_selected':True,'source_boundary':'Existing conservative working rookie coefficient, not realized2021/22 productivity or originalpick15price'}
    need(Fraction(rates['Corey Kispert']['exact_fraction'])==Fraction(src[det.OUT]['player_ratings']['Chris Duarte']['exact_fraction']),'Existing selected rookie prior changed')
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['WAS'])-int(back['CHI']));margin=impact['CHI']-impact['WAS']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'WAS_active':active,'WAS_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_WAS_impact_fraction':str(margin),'CHI_minus_WAS_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'WAS','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_WASHINGTON_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_THREE_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':[],'STD':15,'TW_count':0,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'interval':'Only Jan1/Jan7/Mar29 same namedfamily; no copiedWestbrookLAL/P1Dinwiddie/PorzingisWAS/KCPKuzmaHarrellWAS orIshDEN atoms','butterfly_handoff':['Kispert12 RSC replaceslawfullynonassignmentwaived Homesley/allprotectedGamma retained. OriginalNBA15Kispert/IsaiahTodd31 notselectedrights.','TrentWAS/TroyWAS preserved from approvedS2, noTrentTOR orBrownCHI originalcopy.','OwnTrentBird3/IshEarly2/NetoLenLopezmin do notimportactualnegotiationprice orreceipt; allformer/camp/stretch/FA/unsigned/unusedexceptionGamma preserved.','Bonga nonprofessionalX6 finitebranch selected withselected2021draftnoRedraft/noUPC; originalLALWASUPC/TORsigning notcopied. MathewsSTANDARDQO/WinstonTWQO withnormalminimumFAhold notconflated.','Bryantworkingout/Ruicooperation/Bealavailable exact3dates asfiction; no actualsurgery/COVID/mentalhealth orclinicalcertainty.'],'unsigned2R':[{'pick':n,'player':p,'holder':'WAS','UPC':False,'STD':False,'valid_first_RT':'team-signed oneSeason/legalMinYOS0 delivery inside operativeW21, beforeOct15, acceptanceUntilAtLeastOct15; selectedunaccepted','cost':'outstandingRequiredTender minimum/youngFAfloor normal-apron reservation retained, not new liveSTD','foreign_or_college_newfacts':'X5/X6 reopens; no perpetualrights or actualforeignlawcertificate'}for n,p in SECOND],'summary':{'selected_games':3,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'WAS_wins':sum(g['selected_regulation_winner']=='WAS'for g in games),'STD':15,'TW':0,'active_each':12,'positive_each':12,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Washington keeper · 세 날짜 선택 결과','','선택된 가상 법적 가족·감독·건강·단일 BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_WAS_impact_per100']:.9f}|")
    a+=['','May16 seed15의 Homesley만 비양도 방출·모든 보호급여/earned/bonus Γ를 보존하고 Kispert12 RSC를 선택해15STD0TW. 실제NBA원15Kispert·IsaiahTodd31/WestbrookLAL·P1Dinwiddie·Kuzma/KCP/HarrellWAS·PorzingisWAS·IshDEN 원자거래는 자동복사하지 않는다. Trent/Troy의 승인 S2 소유는 유지한다.','',
    'Trent2018 POR3시즌 계약→거래만 거친 Bird3의 새3년nonoptionflat q10–14m을 법정minimum/IImax와 교차한다. 2018second37은 RSC QO가 아니라 max(125% priorbase+likely,minimum+200k)함수다. Ish2019WAS 두시즌 EarlyBird2의 새2년nonoptionflat q5–7m을 법정minimum과 max(175% 원필요bonus포함salary,105%평균)상한에 교차한다. Neto/Len/Lopez ownmin1 모두newbonus0/options0/fullprotection. 실제가격/사적동의 null, 원Γ/earned/camp/stretch/FA/RT/unusedexception 전체 함수 보존, 새hardcap trigger0.','',
    'Bonga 기존 비professional-development X6 자연2021 SubsequentDraft/noRedraft/noNBAUPC 가족을 선택해 RookieFA·권리 재개방을 명시하며 실제외국분류/기관접수/과거통지부재를 인증하지 않는다. Mathews 연속WAS 두1시즌TW의 STANDARDQO와 Winston 첫TW QO/normalFAfloor를 분리, 유효미수락·미연장Oct1 또는 적법동의철회/FRN 보존·newUPC0. QO살아있는상태에서renounce0·foreverrights0. 원Homesley다년 계약은 전액 보호비용이 남으며 가상waiver접수만 후보절차다.','',
    '[NBA 원프로필](https://www.nba.com/draft/2021/team-profiles/washington-wizards)의live/FA분류는 web관측이고 direct403raw는본문아니다. 원HutchisonWAS는 현재선택Troy/Trent사슬로 바뀌었으며 원BongaUPC나원2021draft거래를 복원하지 않는다.','',
    'usual5 Westbrook/Beal/Trent/Rui/Gafford. PG Westbrook34/Neto14;SG Beal32/Trent16;SF Trent12/Avdija20/Kispert10/Troy6;PF Rui26/Bertans18/Avdija4;C Gafford24/Lopez16/Len8=240. 양수12명 active12, Gill/Ish/Bryant inactive3. Bryant0은 선택된 회복지연, Rui·Beal 양수는 위임된 가상가용성·관계/접촉모델이며 원Jan12복귀/FebBeal수술/정신건강·백신·임상 인증이 아니다.','',
    '현재CHI Mark32/Caruso18/P32, 선택건강 상태·단일March25 EB/BPM·홈2·연전.5. Kispert기존보수prior−728/1145는 실제2022신인실력아님. 24×2분양팀2880초/각14400선수초,score/OTnull·세날짜외동일소속영구고정0.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|2020–21|완료|','|3|2021–23|WAS3 선택 결과·독립검문 대기|','|4|장기 커리어|미완|','|5|결말·구조|미완|','|6|집필 규격·Pack|현행 기능등록기 참조·Pack0|','|7|통합·최종 승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰묶음5/6번까지4·v0.30 PARTIAL/CLOSED/원고0·wholemacro3/실제의료·private비용인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved WAS differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Ish Smith')['price_function']['actual_acceptance']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_OPTION_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Russell Westbrook')['bpm']='70.5'
        return x
    with patch(__name__+'.physical',wrongsource):
        try:build()
        except ValueError:controls.append('RETURNED_PHYSICAL_FUTURE_BPM')
        else:raise AssertionError('FalsePASS BPM')
    return controls
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'WAS currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_WAS_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
