"""Selected two-date Warriors keeper family, rehabilitation and single-BPM model."""
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
SELF='tools/build_gsw_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_GOLDEN_STATE_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='309e6560b5c7edb519c30f652989c4d45ff005fc'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100183','0022100637')
OBS=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-gsw-keeper-20261007/observed_support.json')
OBS_SHA='ba803df9342fbf4732d7d187821e7617c17aa4640df045414e0200b59b1d1dae'
LIVE=('Stephen Curry','Andrew Wiggins','Draymond Green','Klay Thompson','James Wiseman','Jordan Poole','Damion Lee','Eric Paschall')
RESET=('Gary Payton II','Juan Toscano-Anderson')
ROLE_MINUTES={
 'REHAB_OUT':{'PG':{'Stephen Curry':34,'Jordan Poole':14},'SG':{'Jordan Poole':14,'Damion Lee':18,'James Bouknight':8,'Gary Payton II':8},'SF':{'Andrew Wiggins':32,'Kelly Oubre Jr.':12,'Gary Payton II':4},'PF':{'Draymond Green':22,'Kelly Oubre Jr.':12,'Franz Wagner':12,'Juan Toscano-Anderson':2},'C':{'Kevon Looney':24,'Draymond Green':10,'Juan Toscano-Anderson':14}},
 'KLAY_WORKING_RETURN':{'PG':{'Stephen Curry':34,'Jordan Poole':14},'SG':{'Jordan Poole':10,'Klay Thompson':20,'Damion Lee':10,'James Bouknight':4,'Gary Payton II':4},'SF':{'Andrew Wiggins':32,'Kelly Oubre Jr.':8,'Gary Payton II':4,'Jordan Poole':4},'PF':{'Draymond Green':22,'Kelly Oubre Jr.':12,'Franz Wagner':12,'Juan Toscano-Anderson':2},'C':{'Kevon Looney':24,'Draymond Green':10,'Juan Toscano-Anderson':14}}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'REHAB_OUT':{'PG':'Stephen Curry','SG':'Jordan Poole','SF':'Andrew Wiggins','PF':'Draymond Green','C':'Kevon Looney'},'KLAY_WORKING_RETURN':{'PG':'Stephen Curry','SG':'Klay Thompson','SF':'Andrew Wiggins','PF':'Draymond Green','C':'Kevon Looney'}}
ROLE_SHAS={'REHAB_OUT':'8800985144277bc52eaa8793d5d7235675437878b0133360617b553e28075c44','KLAY_WORKING_RETURN':'4ba4234a4df8dd1e8ad9cc917ce591dc16601a63c15e5685ab75999c9d407380'}
PRICE={'route':'VII6b1_FULL_BIRD','seasons':2,'flat_first_base_interval':[14000000,16000000],'new_bonus':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None}
PRICE_FIXED=deepcopy(PRICE)
POLICY={'new_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'two_RSC_slots':'Smailagic/Mulder lawful nonassignmentwaiver; full old protected/earnedGamma retained','Payton_JTA_source_term_branches':'ROS expired→new minimum; if live UPC, voluntary lawful nonassignmentwaiver then new minimum with entire current originalprotectedGamma retained; no silent oldcontract deletion','Klay_Nov12':'selected rehabilitation operational absence','Klay_Jan14':'selected operational return20minutes, neither originalJan9date nor actualclinicalclearance copied','Wiseman_both':'selected continued rehabilitation absence, not originalwhole2022season imported','actual_private_receipts_or_medical':False}
POLICY_FIXED=deepcopy(POLICY)
ROOKIE_COEFFICIENT=Fraction(-728,1145)

def direct(root,p):
    t=(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
    return json.loads(t)if p.endswith('.json')else list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else t
def sources(root):return {p:physical(root,p)for p in PINS}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def support():
    need(hashlib.sha256(base.CBA.read_bytes()).hexdigest()==base.CBA_SHA,'CBA raw changed')
    d=fitz.open(base.CBA);pages=(29,30,54,55,58,212,222,223,233,240,241,294,303,311,312,313,317,318,561)
    tx={n:d[n-1].get_text().replace('\r\n','\n').replace('\r','\n')for n in pages};flat=lambda n:' '.join(tx[n].split())
    need('three (3) preceding Seasons'in flat(29)and 'by means of trade'in flat(29),'Bird continuity absent')
    need('Minimum Player Salary Exception'in flat(233)and 'first Season covered by the player’s Contract'in flat(55),'Minimum price family absent')
    need('Rookie'in flat(294)and 'one hundred twenty percent'in flat(294),'RSC components absent')
    need('not eligible to enter into another Two-Way'in flat(312)and 'October 1'in flat(317)and 'Right of First Refusal shall continue'in flat(318),'TW QO eligibility/expiry absent')
    need(hashlib.sha256(base.FEED.read_bytes()).hexdigest()==base.FEED_SHA,'Frozen source changed');feed=json.loads(base.FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    named={'Signing 1038863':'gary-payton-ii','Signing 1040136':'gary-payton-ii','Signing 1039997':'juan-toscano-anderson','Signing 1033257':'kent-bazemore','Trade 2020002':'kelly-oubre-jr','Trade 2019127':'kelly-oubre-jr','Signing 1019176':'kelly-oubre-jr','Trade 2018071':'kelly-oubre-jr','Signing 1019102':'kevon-looney'}
    rows=[r for r in feed if r['GroupSort']in named and r['PLAYER_SLUG']==named[r['GroupSort']]and r['TEAM_ID']in(1610612744,1610612760,1610612756)];need(len(rows)==9,'Named original continuity changed')
    need(hashlib.sha256(OBS.read_bytes()).hexdigest()==OBS_SHA,'Primary web observation changed');obs=json.loads(OBS.read_text())
    for a in obs['HTTP_attempts']:need(a['status']==403 and not a['raw_body_adopted']and hashlib.sha256(Path(a['raw_path']).read_bytes()).hexdigest()==a['raw_sha256'],'Failed HTTP source promoted')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_frozen_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_original_rows':rows},'web_body_observations_not_raw_certificates':{'cache_path':str(OBS),'raw_sha256':OBS_SHA,'projection':obs}}
def contracts():
    rows=[{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True}for p in LIVE]
    rows.extend({'player':p,'route':'VII6i_MINIMUM_AFTER_LAWFUL_SOURCE_TERM_BRANCH','source_term_branches':POLICY['Payton_JTA_source_term_branches'],'seasons':1,'salary':'signed2021LegalMinimum(YOS)','new_bonus':0,'full_standard_protection':True,'all_original_Gamma_preserved':True}for p in RESET)
    rows.append({'player':'Kevon Looney','route':'valid original player option exercise','operative_original_deadline_notice_selected':True,'original_salary_term_and_Gamma_kept':True,'actual_notice_receipt':None})
    rows.append({'player':'Kelly Oubre Jr.','route':'NEW_OWN_FA','price_function':deepcopy(PRICE),'old_Gamma_preserved':True})
    rows.append({'player':'Kent Bazemore','route':'VII6i_MINIMUM','seasons':1,'salary':'signed2021LegalMinimum(YOS)','new_bonus':0,'full_standard_protection':True,'old_Gamma_preserved':True})
    rows.extend({'player':p,'route':'VII6h_VIII1_RSC','pick':k,'holder':'GSW','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}for k,p in((7,'Franz Wagner'),(14,'James Bouknight')))
    return rows
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and PRICE==PRICE_FIXED and POLICY==POLICY_FIXED,'Returned contract/price/source term changed')
def role_blocks(state):
    rem={r:{p:m//2 for p,m in ps.items()}for r,ps in ROLE_MINUTES[state].items()};roles=list(rem);out=[]
    for i in range(24):
        if i==0:a=deepcopy(STARTERS[state])
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
        need(a is not None,'Five-player matching unavailable')
        for r,p in a.items():need(rem[r].get(p,0)>0,'Role remainder invalid');rem[r][p]-=1
        out.append({'start_second':i*120,'end_second':(i+1)*120,'seconds':120,'positions':a})
    need(all(v==0 for ps in rem.values()for v in ps.values()),'240minute role capacity incomplete');return out
def assert_roles(state,blocks):
    need(ROLE_MINUTES==ROLE_FIXED and digest(blocks)==ROLE_SHAS[state],'Selected chronology altered');seconds=Counter();rs={r:Counter()for r in ROLE_FIXED[state]}
    for i,b in enumerate(blocks):
        need((b['start_second'],b['end_second'],b['seconds'])==(i*120,(i+1)*120,120)and len(set(b['positions'].values()))==5,'Clock/identity invalid')
        for r,p in b['positions'].items():seconds[p]+=120;rs[r][p]+=120
    need(rs=={r:Counter({p:m*60 for p,m in ps.items()})for r,ps in ROLE_FIXED[state].items()}and sum(seconds.values())==14400,'Role source budget changed');return seconds
def special_ratings():
    return {'Klay Thompson':{'exact_fraction':'0','rating':0.0,'classification':'SELECTED_FICTIONAL_NEUTRAL_EB_N0_LIMIT','NBA_March25_row_absent':True,'historical_Klay_BPM_or_ability_zero_certified':False,'recovery_equals_prior_or_prime_ability':False},'Gary Payton II':{'exact_fraction':'0','rating':0.0,'classification':'SELECTED_FICTIONAL_NEUTRAL_EB_N0_LIMIT','NBA_March25_row_absent':True,'historical_NBA_BPM_or_ability_zero_certified':False,'April2021_first_GSW_signing_not_pre_cutoff_sample':True},**{p:{'exact_fraction':str(ROOKIE_COEFFICIENT),'rating':float(ROOKIE_COEFFICIENT),'classification':'SELECTED_FICTIONAL_REUSED_CONSERVATIVE_ROOKIE_COMPARATOR','historical_NBA_2022_stats_or_productivity_certified':False}for p in ('Franz Wagner','James Bouknight')}}
SPECIAL_FIXED=special_ratings()
def build(root=ROOT):
    src=sources(root)
    for p,h in PINS.items():need(sha(root/p)==h and src[p]==direct(root,p),'Returned physical source differs '+p)
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['GSW'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'Alen Smailagic','Mychal Mulder'}|{'Franz Wagner','James Bouknight'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==15,'Current roster/RSC slot identity changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='GSW'];need([(x['pick'],x['player'])for x in picks]==[(7,'Franz Wagner'),(14,'James Bouknight')]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected draft rights changed')
    need(0<PRICE['flat_first_base_interval'][0]<=PRICE['flat_first_base_interval'][1]<Fraction(112414000,4),'Named price exceeds minimum25percentmaximum')
    need(not[x for x in src[det.BPM]if x['nba_player']in SPECIAL_FIXED],'Special NBA pre-cutoff sample unexpectedly exists')
    need(ROOKIE_COEFFICIENT==Fraction(src[det.OUT]['player_ratings']['Chris Duarte']['exact_fraction']),'Existing rookie comparator changed')
    states={};prepared=[];names=set()
    for s in ROLE_FIXED:
        b=role_blocks(s);ps=assert_roles(s,b);active=sorted(set(ps)|({'Kent Bazemore'}if s=='REHAB_OUT'else set()));inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Nomination/availability changed')
        need('James Wiseman'not in active and('Klay Thompson'in active)==(s=='KLAY_WORKING_RETURN'),'Rehabilitation availability changed')
        states[s]={'blocks':b,'player_seconds':dict(ps),'active':active,'inactive':inactive,'positive_operational_availability_selected':True,'zero_minute_reserve_clinical_status':None}
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='GSW'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Calendar/CHI state altered');s='REHAB_OUT'if gid==IDS[0]else'KLAY_WORKING_RETURN'
        need(g['date']==('2021-11-12'if s=='REHAB_OUT'else'2022-01-14'),'Rehabilitation state moved to wrong date')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        r=states[s];pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['GSW']=joint.pop('NYK')
        for b in pair:b['GSW']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,s,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'CHI authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-set(SPECIAL_FIXED)-{'Coby'})
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM altered')
    specials=special_ratings();need(specials==SPECIAL_FIXED,'Returned fictional coefficient/authority altered');rates.update(specials);games=[]
    for g,h,s,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['GSW'])-int(back['CHI']));margin=impact['CHI']-impact['GSW']+home+fatigue;need(margin!=0,'Separate OT selection needed')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'GSW_state':s,'GSW_active':states[s]['active'],'GSW_inactive':states[s]['inactive'],'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_GSW_impact_fraction':str(margin),'CHI_minus_GSW_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'GSW','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_GOLDEN_STATE_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_TWO_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':[],'STD':15,'TW_count':0,'two_nonassignment_waivers_current_fullGamma_preserved':['Alen Smailagic','Mychal Mulder'],'JordanBell_QO':'XI1ciiiC StandardQO iffourplusYOS TW-ineligible; validoperative2021, unaccepted/unextendedOct1, FRN/FAclaims retained','NicoMannion_QO':'XI1ciiiB applicableTWQO ifeligible; validoperative2021, unaccepted/unextendedOct1, no newUPC, FRN/FAclaims retained','all_existing_FA_unsigned_oldTPE_earned_protected_camp_stretch_Gamma_preserved':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_states':states,'selected_ratings':rates,'selected_games':games,'fictional_productivity_limit':{'Klay':'NBA March25 sample missing; explicitly select EBneutral n0limit0, not observed NBA0 or prime talent erased. Operational return20 does not certify skill recovery.','GaryPaytonII':'April8originalGSWfirstsigning lies afterMarch25 samplecutoff; currentrowmissing, selectneutraln0limit0, notobservedNBAabilityzero.','rookies':'Reuse previously selected conservative comparator -728/1145 forFranz/Bouknight initial scenario; no future2022statistics used.','precutoff':'NBA2020–21 through2021-03-25 only for positive veteran prior; originalrehab observations are distinct from fictionalhealth.'},'six_cost_categories':{'live':'Current8 Gamma + source-term2keepfullGamma/recontract +optionLooney +ownOubre/Bazemore+2RSC. No originalbonus protected deletion.','waived_former':'Smailagic/Mulder current fullprotection plus allold earned/dead/camp/stretch retained. No buyoutdiscount.','FA_holds':'Only validnewUPCs replaceassociatedholds; Bell/Mannion FRN/FAclaims retained afterunacceptedQOs.','unsigned':'Two firstRT→newRSC onlyaftervalidUPC; allotheradmitted unsigned rights/costs kept.','unused_exceptions':'OnlyBird/min/Rookie/optioncarry; no newNTMLE/BAE/Room/S&T. AllcurrentTPE/exceptions keep legalnormal vsapron treatment. No2019hardcap carriedacrosscapyears.','incomplete':'At everyprefix legalcapcount inclFA/unsigned amounts; max(0,12-count)*YOS0minimum. Final15UPCcount implies0without omittingothercosts.'},'butterfly_handoff':['Franz7/Bouknight14 notoriginalKuminga7/Moody14. Bothrights→UPC modeled onlywithlegalfirstRT,2waiversretainallcost.','No originalOubreCHA/BazemoreLAL/PaschallUTA/PorterBjelicaIguodalaGSW atom orcash/2R imported.','No automatic 2022Wisemanwholeabsence/Draymondcalfback/actualCOVID protocol orJanuaryKlayoriginalreturndate. Onlytwochosenrehab/coachstates.','ExistingHutchison2018→MIN→NY O3 preserved; not a newcurrentGSWactor. CurrycurrentUPCkept; laterextensions/prices/2022rights requirefutureconsumer.'],'summary':{'selected_games':2,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'GSW_wins':sum(g['selected_regulation_winner']=='GSW'for g in games),'STD':15,'TW':0,'active_each':12,'positive_by_state':{s:len(x['player_seconds'])for s,x in states.items()},'role_states':2,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'historical_Klay_or_rookie_NBA_productivity_certified':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}
def markdown(d):
    a=['# Golden State keeper · 두 날짜 선택 결과','','가상 법적 가족·감독·재활·단일BPM 모델. 독립 검문 대기.','','|날짜|키|GSW 상태|CHI 상태|작업승자|CHI 영향/100|','|---|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['GSW_state']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_GSW_impact_per100']:.9f}|")
    a+=['','S2 May16 seed15에서 Smailagic/Mulder를 비양도방출하고 현재보호Γ 전액을남겨 Franz7/Bouknight14 두RSC를 넣는다. 원live8·JTA/GPII의 원기간live/ROS분기와새minimum·LooneyPO·OubreFullBird2년14–16m·Bazemoreminimum1년=15STD0TW. 기존서명원문불명료를ROS사실로자동치환하지않고 합법조건부유효방출/재합의로원Γ를보존한다.','',
    '[공식GSW2021프로필](https://www.nba.com/draft/2021/team-profiles/golden-state-warriors)의 원FA/option/currentclass와 동결NBA원행을분리사용. Bell TW신규부적격이면STANDARDQO, Mannion적격TWQO를유효미수락Oct1로종료하되FRN/FAclaims를남긴다. 현금·과거dead/camp/stretch·FAhold·미서명·TPE·초기12예약을0으로지우지않는다. 새hardcaptrigger없고원2019hardcap의2021소급0.','',
    '[원November재활발표](https://santacruz.gleague.nba.com/news/warriors-assign-klay-thompson-james-wiseman-to-santa-cruz)는역사조건관측이다. Nov12Klay0/Jan14가상20분복귀·Wiseman두날짜재활0를별도위임작업선택했다. 실제Jan9복귀일/임상승인/감염/Draymond후속부상을복사하지않는다. 직접HTTP403들은미채택이며성공웹본문관측은raw본문인증과다르다.','',
    'Nov12 Curry34/Poole28/Wiggins32/Dray32/Looney24/Oubre24/Lee18/JTA16/Franz12/GPII12/Bouknight8=240,11양수+Bazemore active12. Jan14 Lee−8/Bouknight−4/Oubre−4/GPII−4→Klay20,12양수active12. JTA small-ball C14와DrayC10·FranzPF12는선택감독역할이다. 각각24×2분을현재CHI Mark32/Caruso18/P32와동시에대조한다.','',
    'Klay와April첫GSW계약GPII의 March25행이없어 **가상 EB n0중립limit0**를선택했다. 원Klay실제BPM/전성기능력이나GPII능력0이라는사실이아니다. 재활복귀20분과실력회복은동치가아니다. 두rookie도원NBA관측없으므로기존보수Duarte comparator−728/1145를초기작업상정으로재사용; 실제2022rookie성장/능력 인증0. 다른veteran은동일March25 EB/BPM·홈2·연전.5만사용한다. score/OTnull.','',
    'Kuminga/Moody·OubreCHA·BazemoreLAL·PaschallUTA·Porter/Bjelica/Iguodala원영입·Hutchison현재GSW영입은자동선택하지않는다. 두날짜밖계약/재활/2022rights/추가가격은후속consumer로재개방.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020드래프트연쇄|완료|','|2|2020–21|완료|','|3|2021–23|GSW2결과 작업선택·독립검문 대기|','|4|장기커리어|미완|','|5|결말·구조|미완|','|6|집필규격·Pack|현행기능등록기 참조·Pack0|','|7|통합·최종승인|CLOSED|','',
    '[현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은큰묶음5,6번까지4. v0.30 PARTIAL/CLOSED/원고0. whole82/wholemacro3/실제사적기관·의학인증false.','']
    return '\n'.join(a)
def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved GSW differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    out=[];old=special_ratings
    def wrong():
        x=old();x['Klay Thompson']['historical_Klay_BPM_or_ability_zero_certified']=True;return x
    with patch(__name__+'.special_ratings',wrong):
        try:build()
        except ValueError:out.append('RETURNED_FICTIONAL_KLAY_PRIOR_AS_HISTORICAL')
        else:raise AssertionError('FalsePASS productivity')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==base.DRAFT:next(r for r in x['selected_rows']if r['pick']==7)['player']='Jonathan Kuminga'
        return x
    with patch(__name__+'.physical',wrongsource):
        try:build()
        except ValueError:out.append('RETURNED_ORIGINAL_DRAFT_IDENTITY')
        else:raise AssertionError('FalsePASS selected draft')
    return out
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'GSW currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','GSW_state','selected_regulation_winner','CHI_minus_GSW_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
