"""Two selected Oklahoma City keeper dates; direct physical sources, no ancestor builds."""
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
SELF='tools/build_okc_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_OKLAHOMA_CITY_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
PINS['simulation/TORONTO_2021_SELECTED_T1_OPERATING_FAMILY_2026_10_07.json']='676cb350acdd632dfc0a0b4cc82d8f1d085b243f21fe511caeb11bcc2b993118'
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100730','0022100852')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-okc-keeper-20261007/observed_profile.json')
PROFILE_SHA='09d7986f153b5f5a46fd6b90f27567bda34b8a1b39a6a54ee1089d82aef3df03'
LIVE=('Aleksej Pokusevski','Charlie Brown Jr','Darius Bazley','Gabriel Deck','Isaiah Roby','Kenrich Williams','Luguentz Dort','Shai Gilgeous-Alexander','Theo Maledon','Ty Jerome','Kemba Walker')
OPTIONS={}
SECOND=((35,'Jeremiah Robinson-Earl'),(36,'Dayron Sharpe'),(55,'Jason Preston'));SECOND_FIXED=tuple(SECOND)
ROLE_MINUTES={'PG':{'Kemba Walker':24,'Shai Gilgeous-Alexander':18,'Theo Maledon':6},'SG':{'Shai Gilgeous-Alexander':14,'Luguentz Dort':28,'Tre Mann':6},'SF':{'Scottie Barnes':24,'Kenrich Williams':18,'Luguentz Dort':6},'PF':{'Darius Bazley':24,'Aleksej Pokusevski':18,'Scottie Barnes':4,'Isaiah Roby':2},'C':{'Mike Muscala':24,'Isaiah Roby':18,'Gabriel Deck':6}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Kemba Walker','SG':'Shai Gilgeous-Alexander','SF':'Scottie Barnes','PF':'Darius Bazley','C':'Mike Muscala'}
ROLE_SHA='b2de8aec48211df7c0fc47dcc766cc99de1599f7116a5f89f61ddeb43acfa828'
PRICE={'route':'VII6b2_FULL_BIRD','nonoption_seasons':3,'first_base_function':'q in [4000000,8000000] intersect [legalMinimum,II7maximum]','later_base':'same q','new_bonus':0,'options':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None,'original2018LAL3priorServices_tradesOnlyDET_OKC_noBirdBreak':True}
PRICE_FIXED=deepcopy(PRICE)
QO={'ordinary':'max(125percentPriorBasePlusLikelyBonus,legalMinimum2021(YOS)+200000)','2018second47_notRSCanchor':True,'actual_price':None};QO_FIXED=deepcopy(QO)
MUS={'route':'VII6b3_EARLY_BIRD','two_prior2019_20_2020_21_OKCseasons':True,'nonoption_seasons':2,'first_base_function':'q in [3000000,5000000] intersect [legalMinimum,max(175percentPriorSalaryInclusiveRequiredBonus,105percentApplicableAveragePlayerSalary)]','later_base':'same q','new_bonus':0,'options':0,'full_standard_protection':True,'actual_price':None,'actual_acceptance':None};MUS_FIXED=deepcopy(MUS)
POLICY={'new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED','new_trade':False,'new_NTMLE_BAE_ROOMMLE_incoming_SandT':False,'Bradley':'originalexpiry/newOKCUPC0/alloldFAprotectedGamma retained; sourceCHIcurrentUPC notduplicated','AP1':'SelectedJuly28 old2020_21capYear asset6edges carriedonce, KembaOKC/HorfordMosesBOS; no newevent/current2021_22hardcapcarry fromoldyear','Svi':'originalownexpired_QO_FullBird_FAclaims_allGamma retained; no newOKCUPC, current selectedTOR ownsSvi', 'TW':'Hoard/Hall originalliveTW lawfulnonassignmentwaiver/fullGamma ORexpiredoperativevalidQOunacceptedunextendedOct1/FRN orlawfulconsensualwithdrawal,newUPC0 andnormalminimumFAfloor preserved.','availability':'12positive operationalavailable2dates, SGA/Kemba workingrecovery/cooperationselected; no actualSGAankle/knee/COVID/buyout/copiedJan2022tankingabsence; clinicalnullzerobench.','whole_private_or_actual_receipts':False}
POLICY_FIXED=deepcopy(POLICY)

def direct(root,p):
    t=(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
    return json.loads(t)if p.endswith('.json')else list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else t
SOURCE_MEANING_SHA={'simulation/NBA_2021_22_COMMON_26_OPPONENT_CAPACITY.json': '83a8033265a23be22a002465467225c02e20e56482be8703f2e9f0a46fc23805', 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json': '12456392c139ca9dbb71070e0a574d633728691d477eada592fd03cefc535cb9', 'simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json': '353acb80f6b12e4b67e2cc0cf56ab4f6551cc70efb63b20cf9febc9db21f0c33', 'simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json': '426de339ff1a1270eb41ed6b81caee8e10099e55e2176c4e9f31bd196da853d5', 'simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json': 'b42cfb6e0b895fb6a70eb1a9e32798eb0cda27b98a659b6e4e6fce85a7d431f7', 'canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json': '963c5b9d2967f70cf5770349df39f44f88878e4a3e884b7e0c3c103d7699c6be', 'simulation/CHICAGO_2021_22_CALENDAR.csv': '1c6d8cf8284dc3f88c0d6c7a2a7927f6ba0eb756fbf367da2a44fbfb402e7f68', 'simulation/NBA_2021_22_REGULAR_BASELINE.csv': '8d07a7ba2485a7a0fceeeb2ccfff7acfa1db394f4918459ec4fe30caef2bc4e6', 'simulation/CHICAGO_2020_21_BPM_MAR25_SNAPSHOT.csv': '1ef4eee6a701658c28db8fc611cab263ef8f83936b5badceb45415d35323bfd8', 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS.json': '04d2919b0c1525d0c00d40f7974e8fefd41ed931a1a18495f01b99d98270c317', 'tools/build_chicago_detroit_2021_two_date_selected_bpm_results.py': 'ef289a00d1d7394fefdc6c2d82b535c998f87b6978cddf06fd93319967ebc191', 'tools/build_nyk_2021_keeper_and_chicago_selected_results.py': '01c418a67b2345e60944e90fa602f8644d4bbefeb3456a25cbd0600ef53e9194', 'simulation/TORONTO_2021_SELECTED_T1_OPERATING_FAMILY_2026_10_07.json': '7e1558e6ed3e00caebbc54495c4f19773b69deaa7971c1b90dd661f8be5dad3f'}

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
    named={'Signing 1004195':('svi-mykhailiuk',1610612747),'Trade 2020060':('svi-mykhailiuk',1610612760),'Signing 1019060':('mike-muscala',1610612760),'Signing 1038899':('gabriel-deck',1610612760)}
    rows=[r for r in feed if r['GroupSort']in named and (r['PLAYER_SLUG'],r['TEAM_ID'])==named[r['GroupSort']]];need(len(rows)==4,'Named original own continuity changed')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'NBA_original_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'named_rows':rows},'NBA_profile_web_observation_not_raw_body':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs}}

def contracts():
    return ([{'player':p,'route':'RETAIN_CURRENT_UPC','all_original_Gamma_preserved':True,'operative_original_RSC_prior_option_validly_exercised_if_needed':p in('Shai Gilgeous-Alexander','Darius Bazley','Aleksej Pokusevski'),'actual_option_receipt':None,'KembaAP1existing_originalterm_and_bonuswaiver_sixmonth_descendants_retained':p=='Kemba Walker','no_originalfutureSGAextension_orFavorsOKCorNYKbuyout':True}for p in LIVE]+[{'player':'Mike Muscala','route':'NEW_OWN_FA','price_function':deepcopy(MUS),'new_contract_years':2,'old_Gamma_FAclaims_preserved':True}]+[{'player':p,'route':'VII6h_VIII1_RSC','pick':n,'holder':'OKC','component_scale':['4/5','6/5'],'salary_including_unlikely_ceiling':'6/5','base_and_protection_floor':'4/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'actual_price':None}for n,p in((4,'Scottie Barnes'),(18,'Tre Mann'))])
FIXED_CONTRACTS=contracts()
def assert_contracts(x):need(x==FIXED_CONTRACTS and PRICE==PRICE_FIXED and QO==QO_FIXED and MUS==MUS_FIXED and POLICY==POLICY_FIXED and SECOND==SECOND_FIXED,'Returned class/option/price/authority altered')

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
    for p,h in PINS.items():need(sha(root/p)==h and src[p]==direct(root,p)and digest(src[p])==SOURCE_MEANING_SHA[p],'Returned physical/source semantic differs '+p)
    raw=support();rows=contracts();assert_contracts(rows);seed=src[base.CAPACITY]['team_functions']['OKC'];standard=sorted(set(seed['standard_named_continuation_condition_max15'])-{'Al Horford','Moses Brown','Tony Bradley','Svi Mykhailiuk'}|{'Kemba Walker','Scottie Barnes','Tre Mann'})
    need(set(standard)=={r['player']for r in rows}and len(standard)==14,'Selected May16/current identities changed')
    picks=[x for x in src[base.DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='OKC'];need([(x['pick'],x['player'])for x in picks]==[(4,'Scottie Barnes'),(18,'Tre Mann'),*SECOND]and all(x['lawful_PS21_participant_model_selected']for x in picks),'Selected firstRSC rights changed')
    need('Tony Bradley' in src[base.CHI]['rows'][0]['standard_registered_candidate'] and 'Tony Bradley' not in standard,'CurrentCHI Bradley owner altered')
    asset={x['asset']:x['owner']for x in src[base.DRAFT]['final_asset_ownership']};need(asset['Kemba Walker']=='OKC' and asset['Al Horford']==asset['Moses Brown']=='BOS','Selected AP1 actors restored')
    need('Svi Mykhailiuk'in src['simulation/TORONTO_2021_SELECTED_T1_OPERATING_FAMILY_2026_10_07.json']['selected_roster']['standard'] and 'Svi Mykhailiuk'not in standard,'Selected TOR Svi owner restored')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds));inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==2 and set(active)<=set(standard),'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='OKC'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['OKC']=joint.pop('NYK')
        for b in pair:b['OKC']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need(not(set(joint['OKC'])&set(joint['CHI'])),'Actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Scottie Barnes','Tre Mann','Gabriel Deck'})
    for p in ('Scottie Barnes','Tre Mann'):
        rates[p]={'exact_fraction':'-728/1145','effective_rating':float(Fraction(-728,1145)),'classification':'SELECTED_FICTIONAL_CONSERVATIVE_ROOKIE_PRIOR','provenance':{'existing_Duarte_Suggs_comparison_reused':True,'not_realized2021_22NBAability_orstats':True}}
        need(Fraction(rates[p]['exact_fraction'])==Fraction(src[det.OUT]['player_ratings']['Chris Duarte']['exact_fraction']),'Existing selected rookie prior changed')
    need(not any(x['nba_player']=='Gabriel Deck'for x in src[det.BPM]),'Deck prior-cutoff observed NBA row changed')
    rates['Gabriel Deck']={'exact_fraction':'-728/1145','effective_rating':float(Fraction(-728,1145)),'classification':'SELECTED_FICTIONAL_CONSERVATIVE_POSTCUTOFF_NBA_NEWCOMER_PRIOR','provenance':{'original_NBA_signing_feed':'Signing 1038899','original_NBA_signing_date':'2021-04-10','March25_observed_NBA_row_absent':True,'existing_conservative_coefficient_reused':True,'not_historical_foreign_or_NBA_ability_or_future_statistics':True}}
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['OKC'])-int(back['CHI']));margin=impact['CHI']-impact['OKC']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'OKC_active':active,'OKC_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_OKC_impact_fraction':str(margin),'CHI_minus_OKC_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'OKC','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_OKLAHOMA_CITY_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_NPC_FAMILY_TWO_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':[],'STD':14,'TW_count':0,'active':active,'inactive':inactive,'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'interval':'Only Jan24/Feb12 same namedfamily; no originalKembaNYK/BradleyCHIduplicate/FavorsOKC/SGAextension/Deckdeparture ornewDrafttrade imported','butterfly_handoff':['Seed15-HorfordMoses+Kemba=14, Bradleyexpiry/newOKCUPC0=13, Scottie4/Tre18RSC=15, Svi newOKCUPC0/currentTORowner=14; sourceCHIownsBradley, BOSownsHorfordMoses.','SelectedAP1sixassetedges/SG16threeassetedges occuronceJuly28/29oldcapyear; originalJune18 date/buyout/actualKembaprice/acceptance notcopied.','Svi old ownFA/QO claims preserved/newOKCUPC0 because selectedTORUPC, andMuscala2019OKCtwoServiceEarly2; freshbonuses0 arechosenUPCterms notoldprivateabsence.','Scottie4 notoriginalGiddey6; JRE35/Sharpe36/Preston55 unsignedRT notoriginalNYK34/36exchange orAaronWiggins55 contract.','Kembacooperation/SGAworkingavailable2dates separatefromrealankle/COVID/tankabsence/clinicalproof; zeroreservesnull.'],'unsigned2R':[{'pick':n,'player':p,'holder':'OKC','UPC':False,'STD':False,'valid_first_RT':'team-signed oneSeason/legalMinYOS0 delivery inside operativeW21, beforeOct15, acceptanceUntilAtLeastOct15; selectedunaccepted','cost':'outstandingRequiredTender minimum/youngFAfloor normal-apron reservation retained, not new liveSTD','foreign_or_college_newfacts':'X5/X6 reopens; no perpetualrights or actualforeignlawcertificate'}for n,p in SECOND],'owner_correction':{'selected_TOR_Svi_UPC_preserved':True,'new_OKC_Svi_UPC':False,'all_prior_Svi_QO_FA_protected_Gamma_claims_preserved':True,'same_positive_roles_and_both_selected_winners':True,'previous_peer_is_historical_pre_correction_record':True},'summary':{'selected_games':2,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'OKC_wins':sum(g['selected_regulation_winner']=='OKC'for g in games),'STD':14,'TW':0,'active_each':12,'positive_each':12,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Oklahoma City keeper · 두 날짜 선택 결과','','선택된 가상 법적 가족·감독·건강·단일 BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_OKC_impact_per100']:.9f}|")
    a+=['','seed15−Horford/Moses+Kemba=14, Bradley원만료/noOKCUPC(현재Chicago소유·원FA/보호Γ유지)=13, Scottie4/Tre18 RSC=15−Svi 새OKCUPC0/currentTOR소유=14STD0TW. Charlie/Deck원live를추가방출해비용삭제하지않는다. 선택AP1July28oldcapyear6edges/SG16July293edges는이미실행된소유만carry하며거래재실행/원June18소급/새2021–22hardcap계승0. Kemba원term/당시허용bonuswaiver·후손6개월제약모두보존·실제가격/접수null.','',
    'Svi2018LAL3서비스→DET→OKC 거래만의 원FullBird/ordinaryQO=max(125%priorbase+likely,minimum+200k)·FA·보호Γ청구는유지하지만 현재TOR선행UPC소유가있어 새OKCUPC를체결하지않는다. 0분선수새계약만빼므로양수·두결과불변; originalTORTOreceipt인증이나옛권리무존재선언0. Muscala2019OKC 두서비스 EarlyBird2 새2년nonoptionflatq3–5m/법정minimum과max(175%원필요bonus포함salary,105%평균)교차. 새bonus0/options0/fullprotection은가상계약선택·기존Γ무존재사실아님. 모든oldcamp/waiver/stretch/FA/unsigned/exception함수 유지·newNTMLE/BAE/Room/S&T0.','',
    'Hoard/Hall 원TWlive면nonassignmentwaive/fullΓ,만료면해당유효QO미수락·미연장Oct1/FRN 또는합법동의철회·newUPC0/정상FAfloor유지. JRE35/Sharpe36/Preston55유효firstRT·operativeW21·최소Oct15수락창/미수락·법적만료/noUPC·RT/minimumFAfloor예약/X5/X6재개방을보존,권리만으로3UPC추가하거나무기한독점claim0.','',
    '[NBA 원프로필](https://www.nba.com/draft/2021/team-profiles/oklahoma-city-thunder)은원live/FA분류 web관측·direct403raw본문미채택. Scottie4/Tre18/2R35·36·55는원Giddey6/Jokubaitis34/McBride36/AaronWiggins55 및원NYK2Rexchange와다르다. 원KembaNYK/SGAextension/FavorsOKC/Deckdeparture/현금·미래픽삭제를자동복사하지않는다.','',
    'usual5 Kemba/SGA/Scottie/Bazley/Muscala. PGKemba24/SGA18/Theo6;SGSGA14/Dort28/Tre6;SFScottie24/Kenrich18/Dort6;PFBazley24/Poku18/Scottie4/Roby2;CMuscala24/Roby18/Deck6=240.12양수active12,Charlie/Jeromeinactive2. Kemba/SGA회복·협력은위임건강fiction·실제ankle/knee/COVID/tankabsence인증아님.','',
    '현재CHI Mark32/Caruso18/P32·canonhealth·단일March25 EB/BPM·홈2·연전.5. Scottie/Tre기존보수신인prior−728/1145는실제2022NBAstats아님.Deck은 원feed April10 첫NBA계약으로 March25 관측행이 없으며 동일 −728/1145를 명시적 가상 신규진입 계수로 선택한다. 실제 해외/미래NBA 능력 인증0.24×2분양팀2880초/14400선수초·score/OTnull·전체시즌/실제private비용인증false.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트|완료|','|2|2020–21|완료|','|3|2021–23|OKC2 선택·검문대기|','|4|장기 커리어|미완|','|5|결말·구조|미완|','|6|집필 규격·Pack|현행 등록기·Pack0|','|7|통합·최종 승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰묶음5/6번까지4·v0.30 PARTIAL/CLOSED/원고0·wholemacro3/실제의학·private인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved OKC differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong():
        x=old();next(r for r in x if r['player']=='Mike Muscala')['price_function']['actual_acceptance']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_OPTION_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==det.BPM:next(r for r in x if r['nba_player']=='Kemba Walker')['bpm']='70.5'
        return x
    with patch(__name__+'.physical',wrongsource):
        try:build()
        except ValueError:controls.append('RETURNED_PHYSICAL_FUTURE_BPM')
        else:raise AssertionError('FalsePASS BPM')
    return controls
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'OKC currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_OKC_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
