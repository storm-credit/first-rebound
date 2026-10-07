"""One dated Utah keeper implementation and selected regulation BPM result.

Reuse physical source readers and the already selected BPM policy, never ancestor
constructors. Historical original moves are evidence, not this fictional trace.
"""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from datetime import date,timedelta
from unittest.mock import patch
import argparse,hashlib,json
import fitz
from bs4 import BeautifulSoup
import build_nyk_2021_keeper_and_chicago_selected_results as base
import build_chicago_detroit_2021_two_date_selected_bpm_results as det

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_uta_2021_keeper_and_chicago_selected_result.py'
OUT='simulation/CHICAGO_UTAH_2021_SELECTED_KEEPER_RESULT.json'
MD=OUT[:-5]+'.md'
BASELINE='f4e1ec1ecdf93509e8e7868f800ad04d8aafcafa'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
CAPACITY=base.CAPACITY;CHI=base.CHI;ROSTER=base.ROSTER;DRAFT=base.DRAFT;HEALTH=base.HEALTH;AUTH=base.AUTH
need=base.need;sha=base.sha;text=base.text;physical=base.physical
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-uta-keeper-20261007/observed_profile.json')
PROFILE_SHA='41c819446ed257b3fe0cb9c0019c38191fbc0b61cb4d6d214fe2a7146ca323b9'
GID='0022100083'
RETAINED=('Bojan Bogdanovic','Derrick Favors','Donovan Mitchell','Elijah Hughes','Joe Ingles','Jordan Clarkson','Miye Oni',"Royce O'Neale",'Rudy Gobert','Udoka Azubuike')
MINIMUM=('Juwan Morgan','Ersan Ilyasova')
BIRD={'Mike Conley':3,'Georges Niang':2}
TW_EXPIRED=('Jarrell Brantley','Trent Forrest')
ROLE_MINUTES={
 'PG':{'Mike Conley':30,'Jordan Clarkson':12,'Joe Ingles':6},
 'SG':{'Donovan Mitchell':34,'Jordan Clarkson':14},
 'SF':{'Bojan Bogdanovic':32,'Joe Ingles':16},
 'PF':{"Royce O'Neale":30,'Georges Niang':14,'Joe Ingles':2,'Ersan Ilyasova':2},
 'C':{'Rudy Gobert':32,'Derrick Favors':14,'Ersan Ilyasova':2}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
ROLE_SEQUENCE_SHA='5256babdb9f867fbb96abc15b7b610fd936b109459268cbfa883d0d490e116ce'
STARTERS={'PG':'Mike Conley','SG':'Donovan Mitchell','SF':'Bojan Bogdanovic','PF':"Royce O'Neale",'C':'Rudy Gobert'}
BIRD_PRICE={p:{'seasons':years,'nonoption_seasons':years,'route':'VII6b1_FULL_BIRD',
 'first_base_floor':'max(signed2021LegalMinimum(YOS+year-1,year) for year in contractYears)',
 'first_base_ceiling':'ArticleII7_applicable_first_year_maximum','later_base':'same_as_first_base',
 'new_bonus_allocations_likely_unlikely':0,'full_standard_protection':True,
 'actual_price':None,'actual_receipt':None}for p,years in BIRD.items()}
BIRD_FIXED=deepcopy(BIRD_PRICE)
POLICY={'route':'UTA_KEEP_PRIOR_ACTORS_PLUS_SELECTED_DB1_THOR30',
 'new_contracts_ET':'2021-08-06T12:02:00_ORDERED','Matt_Thomas_waiver_if_live_ET':'2021-08-06T12:01:30',
 'full_Matt_Thomas_protected_current_charge_retained':True,'Brantley_Forrest_QO_acceptance':False,
 'QO_acceptance_window_extended':False,'QO_ordinary_acceptance_deadline':'2021-10-01',
 'new_NTMLE_BAE_incoming_SandT':False,'new_trade':False,'new_TW_UPC':False,
 'new_canonical_author_lock':False,'actual_price_or_receipt_certified':False}
POLICY_FIXED=deepcopy(POLICY)

def sources(root):return {p:physical(root,p)for p in PINS}

def support():
    need(hashlib.sha256(base.CBA.read_bytes()).hexdigest()==base.CBA_SHA,'CBA raw changed')
    d=fitz.open(base.CBA);pages=(29,30,54,55,58,209,210,212,222,223,227,228,232,233,240,241,294,311,312,317,318,561)
    texts={n:d[n-1].get_text().replace('\r\n','\n').replace('\r','\n')for n in pages};flat=lambda n:' '.join(texts[n].split())
    need('three (3) preceding Seasons'in flat(29)and 'by means of trade'in flat(29),'FullBird continuity absent')
    need('Qualifying Veteran Free Agent'in flat(223)and 'maximum amount provided for in Article II, Section 7'in flat(223),'OwnBird salary exception absent')
    need('first Season covered by the player’s Contract'in flat(55),'Signed-year minimum scale absent')
    need('Minimum Player Salary Exception'in flat(233),'Minimum exception absent')
    need('may not accept a Qualifying Offer after the October 1'in flat(317)and 'Right of First Refusal shall continue'in flat(318),'Unaccepted QO expiry/FRN absent')
    need(hashlib.sha256(base.FEED.read_bytes()).hexdigest()==base.FEED_SHA,'Frozen NBA feed changed')
    feed=json.loads(base.FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    groups={'Signing 1004255':'georges-niang','Trade 2019003':'mike-conley','Signing 1033348':'derrick-favors','Signing 1019184':'jarrell-brantley','Signing 1033387':'jarrell-brantley','Signing 1033388':'trent-forrest'}
    rows=[x for x in feed if x['TEAM_ID']==1610612762 and x['GroupSort']in groups]
    need(len(rows)==len(groups)and all(x['PLAYER_SLUG']==groups[x['GroupSort']]for x in rows),'Named continuity or TW actors changed')
    need(hashlib.sha256(base.RFA.read_bytes()).hexdigest()==base.RFA_SHA,'Official RFA raw changed')
    j=json.loads(BeautifulSoup(base.RFA.read_text(encoding='utf-8'),'html.parser').find('script',id='__NEXT_DATA__').string)
    body=BeautifulSoup(j['props']['pageProps']['article']['contentText'],'html.parser').get_text(' ',strip=True)
    need('Juwan Morgan (UTA)'in body.split('Not issued (unrestricted free agents)')[1],'Morgan original no-QO classification absent')
    restricted=body.split('two-way free agents')[-1].split('Unrestricted')[0]
    need('Jarrell Brantley (UTA)'in restricted and 'Trent Forrest (UTA)'in restricted,'Original TW RFA list absent')
    need(hashlib.sha256(PROFILE.read_bytes()).hexdigest()==PROFILE_SHA,'Profile observation changed')
    obs=json.loads(PROFILE.read_text(encoding='utf-8'));need(obs['original_body_fields']['Joe_Ingles_role']=='F/G','Ingles role source changed')
    for x in [obs['direct_HTTP'],*obs['failed_original_conley_niang_raws']]:need(hashlib.sha256(Path(x['cache_path']).read_bytes()).hexdigest()==x['raw_sha256']and not x['body_adopted_as_primary'],'Failed HTTP counted as actual primary body')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,
      'normalized_fitz_page_text_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in texts.items()}},
      'movement':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'original_continuity_anchors':rows},
      'RFA':{'url':'https://www.nba.com/news/2021-free-agency-options-and-qualifying-offers','cache_path':str(base.RFA),'raw_sha256':base.RFA_SHA,
        'Morgan_original_no_QO':True,'Brantley_Forrest_original_restricted':True},
      'profile_observation':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'observation':obs,'failed_HTTP_body_counted_as_primary':0},
      'admitted_fullBird_continuity':'Niang original2018July13 standard through2018–19/2019–20/2020–21; Conley Memphis2018–19→2019UTAHtrade→2019–20/2020–21. Three-season source-compatible contract family; no unrelated free-agent move or fullBird renunciation in selected continuity.',
      'TW_QO_types':'Brantley two consecutive one-year UTA TW→standardminimum QO; Forrest one prior TW→applicable TWQO. Both valid operative2021 issuance, unaccepted/unextended acceptance expiresOctober1; FRN and applicable capclaims survive, no NBAUPC created.'}

def contracts():
    out=[{'player':p,'route':'VII6a_EXISTING','new_UPC':False,'prior_salary_protection_bonus_Γ_preserved':True,'current_valid_term':True,'actual_receipt':None}for p in RETAINED]
    for p in BIRD:out.append({'player':p,'new_UPC':True,'route':'VII6b1_FULL_BIRD','price_function':deepcopy(BIRD_PRICE[p]),'prior_Γ_preserved':True,'current_valid_term':True,'actual_receipt':None})
    for p in MINIMUM:out.append({'player':p,'new_UPC':True,'route':'VII6i_MINIMUM','term':1,'salary':'applicable2021MinimumPlayerSalary(YOS)','new_bonus':0,'full_standard_protection':True,'current_valid_term':True,'prior_Γ_preserved':True,'actual_receipt':None})
    out.append({'player':'JT Thor','new_UPC':True,'route':'VII6h_VIII1_RSC','pick':30,'holder':'UTA','component_scale':['4/5','6/5'],'base_protection_floor':'4/5','salary_including_unlikely_ceiling':'6/5','guaranteed':2,'options':2,'valid_first_RT_before_UPC':True,'current_valid_term':True,'actual_receipt':None})
    return out

def assert_contracts(rows):
    need(BIRD_PRICE==BIRD_FIXED and POLICY==POLICY_FIXED,'Selected legal policy changed')
    need(len(rows)==15 and {x['player']for x in rows}==set(RETAINED+MINIMUM+tuple(BIRD)+('JT Thor',)),'Keeper identity changed')
    for x in rows:
        p=x['player'];need(x['actual_receipt']is None and x['current_valid_term'],'Actual receipt promoted/current term lost')
        if p in RETAINED:need(x['route']=='VII6a_EXISTING'and not x['new_UPC']and x['prior_salary_protection_bonus_Γ_preserved'],'Existing obligations altered')
        elif p in BIRD:need(x['route']=='VII6b1_FULL_BIRD'and x['price_function']==BIRD_FIXED[p]and x['prior_Γ_preserved']and x['new_UPC'],'Returned fullBird price family changed')
        elif p in MINIMUM:need(x['route']=='VII6i_MINIMUM'and x['new_UPC']and x['term']==1 and x['salary']=='applicable2021MinimumPlayerSalary(YOS)'and x['new_bonus']==0 and x['full_standard_protection']and x['prior_Γ_preserved'],'Minimum UPC law changed')
        else:need(x['new_UPC']and x['route']=='VII6h_VIII1_RSC'and x['pick']==30 and x['holder']=='UTA'and x['component_scale']==['4/5','6/5']and x['base_protection_floor']=='4/5'and x['salary_including_unlikely_ceiling']=='6/5'and x['guaranteed']==2 and x['options']==2 and x['valid_first_RT_before_UPC'],'Thor RSC source changed')

def role_blocks():
    # Bipartite role/player edge coloring. Each two-minute slot matches all five
    # roles, and every player whose residual degree equals slots left must play.
    rem={r:{p:m//2 for p,m in ps.items()}for r,ps in ROLE_MINUTES.items()};roles=list(rem);out=[]
    for i in range(24):
        if i==0:assignment=deepcopy(STARTERS)
        else:
            totals=Counter()
            for ps in rem.values():totals.update(ps)
            required={p for p,v in totals.items()if v==24-i}
            def find(k,a):
                if k==5:return a if required<=set(a.values())else None
                r=roles[k]
                for p in sorted(rem[r],key=lambda p:(p not in required,-rem[r][p],p)):
                    if rem[r][p]>0 and p not in a.values():
                        found=find(k+1,{**a,r:p})
                        if found:return found
                return None
            assignment=find(0,{})
        need(assignment is not None,'Role capacity matching unavailable')
        for r,p in assignment.items():need(rem[r].get(p,0)>0,'Role residual invalid');rem[r][p]-=1
        out.append({'start_second':120*i,'end_second':120*(i+1),'seconds':120,'positions':assignment})
    need(all(v==0 for ps in rem.values()for v in ps.values()),'Role demand not covered')
    return out

def assert_role_blocks(rows):
    need(hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==ROLE_SEQUENCE_SHA,'Returned chosen role chronology differs from fixed selection')
    need(ROLE_MINUTES==ROLE_FIXED,'Fixed selected role budget changed');sums={r:Counter()for r in ROLE_FIXED};end=0
    for row in rows:
        need(row['start_second']==end and row['end_second']-end==row['seconds']==120,'Role elapsed clock changed')
        pos=row['positions'];need(set(pos)==set(ROLE_FIXED)and len(set(pos.values()))==5,'Role uniqueness lost')
        for r,p in pos.items():need(p in ROLE_FIXED[r],'Source selected role identity changed');sums[r][p]+=120
        end=row['end_second']
    need(end==2880 and rows[0]['positions']==STARTERS,'Clock or usual starters changed')
    need(all(dict(ps)=={p:m*60 for p,m in ROLE_FIXED[r].items()}for r,ps in sums.items()),'Returned selected role/player totals changed')
    return Counter({p:sum(ps[p]for ps in sums.values())for p in set().union(*(set(ps)for ps in sums.values()))})

def build(root=ROOT):
    src=sources(root)
    for p,h in PINS.items():need(sha(root/p)==h and src[p]==physical(root,p),'Physical source mismatch '+p)
    raw=support();n=src[CAPACITY]['team_functions']['UTA'];rows=contracts();assert_contracts(rows)
    last=next(x for x in reversed(src[ROSTER]['team_game_bindings'])if x['team']=='UTA');state=src[ROSTER]['roster_states'][last['state_id']]
    oldstd={x['player']for x in state['players']if x['contract_class']=='STANDARD'}
    need(oldstd==set(n['standard_named_continuation_condition_max15'])and oldstd-{'Matt Thomas'}|{'JT Thor'}=={x['player']for x in rows},'S2 keeper seed transport changed')
    picked=[x for x in src[DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='UTA'];need(len(picked)==1 and picked[0]['pick']==30 and picked[0]['player']=='JT Thor'and picked[0]['lawful_PS21_participant_model_selected'],'Selected Thor entitlement changed')
    blocks=role_blocks();seconds=assert_role_blocks(blocks);positive=set(seconds);standard=sorted(x['player']for x in rows)
    active=sorted(positive|{'Elijah Hughes','Juwan Morgan'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==3 and set(active)<=set(standard),'Dated active nomination changed')
    g=next(x for x in src[det.CAL]if x['game_id']==GID);h=next(x for x in src[HEALTH]['selected_dates']if x['game_id']==GID)
    need(g['date']=='2021-10-30'and g['home']=='CHI'and g['away']=='UTA'and(h['date'],h['home'],h['away'])==(g['date'],g['home'],g['away']),'Source calendar changed')
    need(src[AUTH]['selected']['selected_date_rows']['sha256']==PINS[HEALTH],'CHI health authority changed')
    c=next(x for x in src[CHI]['rows']if x['game_id']==GID and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'CHI health/source minutes changed')
    role={'blocks':blocks,'player_seconds':dict(seconds)};pair=base.paired(c,role);joint=base.assert_pair(c,role,pair)
    joint['UTA']=joint.pop('NYK')
    for seg in pair:seg['UTA']=seg.pop('NYK')
    need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
    names=set(joint['CHI'])|positive;ratings=det.expected_ratings({det.BPM:src[det.BPM]},names)
    for p in set(ratings)&set(src[det.OUT]['player_ratings']):need(ratings[p]==src[det.OUT]['player_ratings'][p],'Shared BPM productivity changed')
    impacts={t:sum(Fraction(ratings[p]['exact_fraction'])*v/2880 for p,v in ps.items())for t,ps in joint.items()}
    yesterday=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==yesterday and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};fatigue=Fraction(1,2)*(int(back['UTA'])-int(back['CHI']));margin=impacts['CHI']-impacts['UTA']+2+fatigue;need(margin!=0,'Tie needs overtime model')
    feed=json.loads(base.FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows'];events=[{'GroupSort':x['GroupSort'],'date':x['TRANSACTION_DATE'][:10],'player':x['PLAYER_SLUG'],'description':x['TRANSACTION_DESCRIPTION'],'applied_to_fiction':False}for x in feed if x['TEAM_ID']==1610612762 and '2021-07-29'<=x['TRANSACTION_DATE'][:10]<='2021-10-30']
    return {'id':'CHICAGO_UTAH_2021_SELECTED_KEEPER_RESULT','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_FAMILY_AND_ONE_REGULATION_RESULT_INDEPENDENT_REVIEW_PENDING',
      'source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,
      'dated_registration':{'standard':standard,'TW':[],'active':active,'inactive':inactive,'positive10_operationally_available':True,'zero_clinical_status':None,
        'expired_TW_names':list(TW_EXPIRED),'valid_QOs_issued_inside_operative2021_window':True,'unaccepted_no_extension_after_Oct1':True,'ROFR_and_applicable_prior_salary_cap_claims_preserved':True,
        'original_Matt_Thomas_live_waiver_or_legal_expiration':'fiction beforeThorUPC; alloriginalcurrentprotectedΓkept','new_UPCs_order':['JT Thor','Mike Conley','Georges Niang','Juwan Morgan','Ersan Ilyasova'],'final_STD':15,'final_TW':0},
      'selected_UTA_role_blocks':blocks,'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_ratings':ratings,
      'selected_game':{'game_id':GID,'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],
        'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impacts.items()},
        'back_to_back':back,'home_effect_CHI_per100':2,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_UTA_impact_fraction':str(margin),'CHI_minus_UTA_impact_per100':float(margin),
        'selected_regulation_winner':'CHI'if margin>0 else'UTA','score':None,'overtime_selection':None,'historical_score_used':False},
      'six_cost_categories':{'live':'Retained10 validcurrentΓ; fullBirdq Conley3/Niang2, legalminMorgan/Ilyasova1, ThorRSC. Oldallocated/likely/unlikely/currentprotection preserved; newUPCs bonus0.',
        'waived_former':'MattThomas originalcurrentprotected salary fullykept; all prior waived/former salary-year obligations/stretchΓ preserved.',
        'FA_holds':'Own signedFA claims replaced only by newUPC; Brantley/Forrest applicable unacceptedQO/FRN/FA costs preserved, no unreportedrenounce or0.',
        'unsigned_draft':'Current selectedThor30 firstRT/120%hold untilsignedRSC, thereafter actualfamilyRSC only. No originalAldama/Butler deal copied.',
        'unused_exceptions':'Inherited TPE/MLE/BAE accounted statutorynormal/apron, no newNTMLE/BAE/SandT or arbitrarycash0.',
        'incomplete':'Everyprefix max(0,12−lawfulcapcount)*YOS0min; unsignedfirst/FA counts preserved; finalSTD15 makescharge0 bycount.'},
      'cap_admissibility':{'all_new_standard_UPCs_fit_named_cap_exceptions':True,'nonempty_Bird_q':'Conleyservice14/Niangservice5: flat2/3year maxlegalminimum is below II7firstyear maximum. Function endpoints not actual salary; negotiatedlawfulpayment/protection.',
        'new_hardcap_trigger_count':0,'whole_private_normal_apron_total':None,'actual_no_other_obligation_or_trigger_absence_certified':False},
      'original_reported_event_controls':events,'butterfly_handoff':['Favors retained: no original OKC salary/future1R or returned2027second/cash copied. Review OKC descendants before consumption.',
        'Niang notPHI/Morgan notBOS, Gay/Whiteside/Paschall notUTA: counterparty families need owndatedimplementation.',
        'Thor30 selected, no Aldama/Butler40 drafttrade or originalfuturesecond returns.',
        'No Ingles into2022March16 without new dated injury/roster/legal decision; onlyOct30 capacity/availability selected.'],
      'summary':{'selected_games':1,'STD':15,'TW':0,'active':12,'positive_UTA':10,'new_standard_UPCs':5,'role_blocks':24,'paired_elapsed_seconds_each':2880,'player_seconds_each':14400,'selected_winner':'CHI'if margin>0 else'UTA'},
      'remaining_ports':{'next_chronological_key':'0022100098','opponent':'BOS','date':'2021-11-01','future_UTA_key_requires_newinterval':True},
      'certification':{'selected_fictional_lawful_NPC_family':True,'selected_date_working_health_and_result':True,'independent_review_completed':False,
        'actual_salary_receipt_or_medical_certificate':False,'actual_full_private_ledger':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    g=d['selected_game'];return '\n'.join(['# Utah keeper 가족·10/30 Chicago 작업 결과','',
      '**선택된 가상 법적 NPC 가족·규정시간 결과; 독립 검문 대기.**',
      f"2021-10-30 `{GID}`: CHI {g['CHI_state']}, 작업 승자 {g['selected_regulation_winner']}, CHI 방향 BPM 영향/100 {g['CHI_minus_UTA_impact_per100']:.9f}. 원107–99 점수/부상/OT는 사용하지 않았다.",'',
      '기존10명 계약/보호/보너스Γ를 보존하고 Conley3년·Niang2년 ownFullBird flatbase 법정구간, Morgan/Ilyasova1년 minimum, 현재DB1 Thor30 RSC를 적법 가상 합의로 선택한다. Conley의 옛Memphis→Utahtrade와 Niang2018표준서명·3시즌 연속 가족은 I1yy/VII6b1을 지원한다. 정확시장가격/실수락을 고르지 않았다. signed2021Year2/3 최저급여를 모두 충족하는 q 함수이며 초년II7최대 이하이다.','',
      'MattThomas의 적법만료/비양도방출 후 current 보호급여 전액을 남긴다. Brantley/Forrest의 유효QO는 미수락·비연장으로 October1 수락창만 끝나며 ROFR/FA/보호비용은 삭제하지 않는다. Brantley 연속2TW의 standard QO와 Forrest TWQO를 구별한다. 현재15STD0TW·active12로 미래TW가 반드시 계약돼야 하는 요구는 만들지 않는다.','',
      '새 감독240분: Conley30, Mitchell34, Bojan32, Royce30, Gobert32, Ingles24, Clarkson26, Niang14, Favors14, Ilyasova4. 기존공통수학 Gobert24/Ilyasova24를 실제분으로 복사하지 않았다. 각 포지션48분·선수10명 240분·초별양팀5명·분/active를 검문한다. [NBA 당시팀프로필](https://www.nba.com/draft/2021/team-profiles/utah-jazz)의 InglesF/G는 웹본문관측이며 직접403 HTML은 원문증거가 아니다.','',
      'live/waivedformer/FA/unsigned/unusedexceptions/incomplete 여섯Γ를 유지하고 ownBird/min/RSC만 사용한다. whole private normal/apron 총액은null이며 이 방식이 실제UTA 장부무부담 증명이라는 주장은 없다. [2017CBA](https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf) 원문 및 동결NBAfeed를 직접 소비했다.','',
      '원Favors→OKC/future1R/2027secondcash, Niang→PHI, Morgan→BOS, Gay/Whiteside/Paschall/Butler 영입을 자동실행하지 않는다. 기존현재권리는 그대로이며 상대팀 후손을 별도 재검문한다. March16 Utah 재사용에는 새로운 날짜별소속/건강입력이 필요하다. 다음연대기는11/1 BOS; 해당팀 법적가족 전까지 결과는 만들지 않는다.','',
      '## 7행 진행','', '|번호|작업|현황|','|---|---|---|','|1|2020드래프트연쇄|완료|','|2|Chicago2020–21|완료|','|3|2021–23|UTA1가족·1결과 선택/검문대기|','|4|장기커리어|미완|','|5|결말·구조|미완|','|6|집필규격·Pack|현행누적기능등록기 참조·Pack0|','|7|통합·최종승인|CLOSED|','',
      '[현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 미완료 큰묶음5·6번까지4. v0.30 PARTIAL/CLOSED/원고0. 작성자통제는 독립검문으로 계수하지 않는다.',''])

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved UTA result differs from physical source construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]

def self_test():
    out=[];cc=contracts
    def bad_price():
        x=cc();next(r for r in x if r['player']=='Mike Conley')['price_function']['new_bonus_allocations_likely_unlikely']=100000;return x
    with patch(__name__+'.contracts',bad_price):
        try:build()
        except ValueError:out.append('RETURNED_BIRD_NEW_BONUS_OUTSIDE_FAMILY')
        else:raise AssertionError('FalsePASS Bird bonus')
    rb=role_blocks
    def bad_role():
        x=rb();x[0]['positions']['PG'],x[0]['positions']['SG']=x[0]['positions']['SG'],x[0]['positions']['PG'];return x
    with patch(__name__+'.role_blocks',bad_role):
        try:build()
        except ValueError:out.append('RETURNED_SAME_TOTAL_ROLE_SWAP')
        else:raise AssertionError('FalsePASS role')
    ss=sources
    def bad_source(root):
        x=ss(root);next(r for r in x[DRAFT]['selected_rows']if r['pick']==30)['conditional_final_draft_rights_holder']='MEM';return x
    with patch(__name__+'.sources',bad_source):
        try:build()
        except ValueError:out.append('RETURNED_THOR_ORIGINAL_TRADE_OWNER_INHERITANCE')
        else:raise AssertionError('FalsePASS draft')
    return out

def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(physical(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'UTA currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'CHI_minus_UTA_impact':d['selected_game']['CHI_minus_UTA_impact_per100'],'writer_negative_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
