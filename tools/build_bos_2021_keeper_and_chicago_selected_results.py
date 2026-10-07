"""Selected AP1 carry plus a three-date Boston keeper/result implementation.

Physical leaf fields are consumed directly; no ancestor build is called.
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
import build_uta_2021_keeper_and_chicago_selected_result as utility
import build_chicago_detroit_2021_two_date_selected_bpm_results as det

ROOT=Path(__file__).resolve().parents[1];SELF='tools/build_bos_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_BOSTON_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='f4e1ec1ecdf93509e8e7868f800ad04d8aafcafa'
T1='research/NBA_2021_PICK16_T1_OPERATING_FAMILY_2026_10_07.json'
PRIOR='simulation/CHICAGO_2020_21_POSTDEADLINE_OBSERVED_PRIORS.csv'
PINS={**utility.PINS,utility.SELF:'def07d588c90319963d592e98ce092cd638f2637adc38ba3c6423b1533af818d',T1:'ba20c3378be3fa2ed9883b3990d315f8b889455ab0bc429a8cee4ec99fb4d128',PRIOR:'5aee8ea2d013fb367a38730bbbb5fff757e43dce9c7963f5088fe5c933b7d0dd'}
need=base.need;sha=base.sha;physical=base.physical;text=base.text
CAPACITY=base.CAPACITY;CHI=base.CHI;ROSTER=base.ROSTER;DRAFT=base.DRAFT;HEALTH=base.HEALTH;AUTH=base.AUTH
IDS=('0022100098','0022100647','0022101193')
LIVE=('Aaron Nesmith','Carsen Edwards','Grant Williams','Jaylen Brown','Jayson Tatum','Marcus Smart','Payton Pritchard','Robert Williams III','Romeo Langford','Tristan Thompson','Al Horford','Moses Brown')
PROFILE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-bos-keeper-20261007/observed_profile.json')
PROFILE_SHA='41e611163d7b185b5c2e8aec7fe9ab17a13e55c35dc83affa28ebf7d5388adf9'
ROLE_MINUTES={
 'PG':{'Marcus Smart':32,'Payton Pritchard':16},
 'SG':{'Jaylen Brown':18,'Evan Fournier':22,'Romeo Langford':8},
 'SF':{'Jayson Tatum':22,'Jaylen Brown':14,'Aaron Nesmith':10,'Romeo Langford':2},
 'PF':{'Jayson Tatum':14,'Grant Williams':20,'Al Horford':10,'Jabari Parker':4},
 'C':{'Al Horford':20,'Robert Williams III':28}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Marcus Smart','SG':'Jaylen Brown','SF':'Jayson Tatum','PF':'Al Horford','C':'Robert Williams III'}
PRICE={'route':'VII6b1_FULL_BIRD','nonoption_seasons':3,'first_base_floor':'max(signed2021LegalMinimum(YOS+year-1,year) for year in 1..3)',
 'first_base_ceiling':'ArticleII7_applicable_first_year_maximum','later_base':'same_as_first_base',
 'new_bonus':0,'full_standard_protection':True,'actual_price':None,'actual_receipt':None}
PRICE_FIXED=deepcopy(PRICE)
POLICY={'selected_AP1_date':'2021-07-28','new_FA_UPCs_ET':'2021-08-06T12:02:00_ORDERED',
 'Kornet':'valid oldterm expiration, or lawful nonassignmentwaiver beforeUPC; fulloriginal currentprotectedΓkept',
 'Parker':'source-term Γ branch: valid2021live carry OR expiredROS→newone-year lawfulminimumUPC; no retrospective term fabrication',
 'TW':'Fall/Waters valid standardQO afterconsecutiveTW; unaccepted/unextendedOctober1; no newUPC, ROFR/capclaims retained',
 'new_NTMLE_BAE_incoming_SandT':False,'new_trade_after_AP1':False,'exact_price_or_real_receipts_certified':False}
POLICY_FIXED=deepcopy(POLICY)

def sources(root):return {p:physical(root,p)for p in PINS}

def support():
    need(hashlib.sha256(base.CBA.read_bytes()).hexdigest()==base.CBA_SHA,'CBA raw changed')
    d=fitz.open(base.CBA);pages=(29,30,54,55,58,212,222,223,227,228,232,233,240,241,303,311,312,317,318,561)
    tx={n:d[n-1].get_text().replace('\r\n','\n').replace('\r','\n')for n in pages};flat=lambda n:' '.join(tx[n].split())
    need('three (3) preceding Seasons'in flat(29)and 'by means of trade'in flat(29),'Bird continuity rule absent')
    need('maximum amount provided for in Article II, Section 7'in flat(223)and 'Minimum Player Salary Exception'in flat(233),'FA capexceptions absent')
    need('first Season covered by the player’s Contract'in flat(55),'Multiyear signedminimum source absent')
    need('Right of First Refusal shall continue'in flat(318),'Unaccepted QO survivingclaims absent')
    need(hashlib.sha256(base.FEED.read_bytes()).hexdigest()==base.FEED_SHA,'Frozen movement source changed')
    feed=json.loads(base.FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    group={'Trade 2020077':'evan-fournier','Signing 989624':'semi-ojeleye','Signing 1039170':'jabari-parker','Trade 2020067':'luke-kornet','Signing 1033566':'tristan-thompson','Signing 1033227':'tacko-fall','Signing 1033231':'tremont-waters','ContractConverted 1020514':'tacko-fall','Signing 1019285':'tremont-waters'}
    rows=[x for x in feed if x['TEAM_ID']==1610612738 and x['GroupSort']in group and x['PLAYER_SLUG']==group[x['GroupSort']]]
    need(len(rows)==len(group)and all(x['PLAYER_SLUG']==group[x['GroupSort']]for x in rows),'Original named contract/claim actors changed')
    need(hashlib.sha256(PROFILE.read_bytes()).hexdigest()==PROFILE_SHA,'Profile observation changed');obs=json.loads(PROFILE.read_text(encoding='utf-8'))
    http=obs['direct_HTTP'];need(hashlib.sha256(Path(http['cache_path']).read_bytes()).hexdigest()==http['raw_sha256']and not http['adopted_primary_body'],'Failed HTTP counted as official body')
    return {'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,
      'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},
      'frozen_NBA_feed':{'cache_path':str(base.FEED),'raw_sha256':base.FEED_SHA,'original_named_anchors':rows},
      'official_profile_observation':{'cache_path':str(PROFILE),'raw_sha256':PROFILE_SHA,'projection':obs,'direct_failed_HTTP_adopted_as_body':False},
      'Fournier_fullBird_admitted_history':'ORL currentcontract covers2018–19/2019–20/2020–21→approvedMarch25BOStrade; no intervening nontrade move or fullrenunciation in preserved family. This is source-compatible legal continuity, not actual private receipt certification.',
      'Parker_boundary':'NBAprofile lists undercontract but frozenApril16 feed saysROS; do not assert one resolves the other. Both lawful currenttermcarry or expiredROS/minUPC branches preserve alloriginal currentprotectedΓ.'}

def contracts():
    rows=[{'player':p,'route':'VII6a_EXISTING','new_UPC':False,'old_Γ_preserved':True,'valid_current_term_to_Apr6':True,'actual_receipt':None}for p in LIVE]
    rows +=[{'player':'Evan Fournier','route':'VII6b1_FULL_BIRD','new_UPC':True,'price_function':deepcopy(PRICE),'old_Γ_preserved':True,'actual_receipt':None},
      {'player':'Semi Ojeleye','route':'VII6i_MINIMUM','new_UPC':True,'salary':'applicable2021Minimum(YOS)','term':1,'new_bonus':0,'full_standard_protection':True,'old_Γ_preserved':True,'actual_receipt':None},
      {'player':'Jabari Parker','route':'CURRENT_TERM_OR_ROS_MINIMUM_RENEWAL','admitted_term_branches':['valid2021live carry','expired2020–21ROS→VII6i oneYear applicable2021Minimum(YOS),bonus0,fullstandardprotection'],
       'term_branch_actual_selected':None,'old_Γ_preserved':True,'actual_receipt':None}]
    return rows

def assert_contracts(rows):
    need(PRICE==PRICE_FIXED and POLICY==POLICY_FIXED,'Chosen lawful contract policy altered')
    need(len(rows)==15 and {x['player']for x in rows}==set(LIVE+('Evan Fournier','Semi Ojeleye','Jabari Parker')),'Currentkeeper15 identities changed')
    for x in rows:
        p=x['player'];need(x['old_Γ_preserved']and x['actual_receipt']is None,'Prior obligation dropped or actualreceipt promoted')
        if p in LIVE:need(x['route']=='VII6a_EXISTING'and not x['new_UPC']and x['valid_current_term_to_Apr6'],'Valid existingcontract branch altered')
        elif p=='Evan Fournier':need(x['route']=='VII6b1_FULL_BIRD'and x['new_UPC']and x['price_function']==PRICE_FIXED,'Returned Fournier priceexception changed')
        elif p=='Semi Ojeleye':need(x['route']=='VII6i_MINIMUM'and x['new_UPC']and x['salary']=='applicable2021Minimum(YOS)'and x['term']==1 and x['new_bonus']==0 and x['full_standard_protection'],'Minimumfamily changed')
        else:need(x['route']=='CURRENT_TERM_OR_ROS_MINIMUM_RENEWAL'and x['admitted_term_branches']==['valid2021live carry','expired2020–21ROS→VII6i oneYear applicable2021Minimum(YOS),bonus0,fullstandardprotection']and x['term_branch_actual_selected']is None,'Parker current/ROS boundary lost')

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
        need(a is not None,'Selected coach matching unavailable')
        for r,p in a.items():need(rem[r].get(p,0)>0,'Coach role leftover invalid');rem[r][p]-=1
        out.append({'start_second':i*120,'end_second':(i+1)*120,'seconds':120,'positions':a})
    need(all(v==0 for ps in rem.values()for v in ps.values()),'240minute demand uncovered');return out

def assert_roles(blocks):
    need(ROLE_MINUTES==ROLE_FIXED,'Fixed roles changed');sums={r:Counter()for r in ROLE_FIXED};end=0
    for b in blocks:
        need(b['start_second']==end and b['end_second']-end==b['seconds']==120,'Roleclock changed');pos=b['positions']
        need(set(pos)==set(ROLE_FIXED)and len(set(pos.values()))==5,'Role fiveuniqueness lost')
        for r,p in pos.items():need(p in ROLE_FIXED[r],'Player outside selected role');sums[r][p]+=120
        end=b['end_second']
    need(end==2880 and blocks[0]['positions']==STARTERS,'Usualstarters/clock changed')
    need(all(dict(ps)=={p:m*60 for p,m in ROLE_FIXED[r].items()}for r,ps in sums.items()),'Selectedrole minute function changed')
    # A literal semantic pin is filled from this initial explicit chosen plan.
    need(hashlib.sha256(json.dumps(blocks,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==ROLE_SEQUENCE_SHA,'Returned chosen sequence differs from fixed selection')
    return Counter({p:sum(ps[p]for ps in sums.values())for p in set().union(*(set(ps)for ps in sums.values()))})
ROLE_SEQUENCE_SHA='2b760fea952fbafbdcff7cd9d932c67816f5bdc652e0f06b807c81dc0c349c05'

def build(root=ROOT):
    src=sources(root)
    for p,h in PINS.items():need(sha(root/p)==h and src[p]==physical(root,p),'Physical sourcefield substitution '+p)
    raw=support();rows=contracts();assert_contracts(rows);n=src[CAPACITY]['team_functions']['BOS']
    prior=set(n['standard_named_continuation_condition_max15']);expected=prior-{'Kemba Walker','Luke Kornet'}|{'Al Horford','Moses Brown'}
    need(expected=={x['player']for x in rows},'May16/AP1/expiry exactroster join changed')
    ap=src[DRAFT]['event_trace'][0];edges=ap['edges'];need(ap['event']=='AP1'and ap['date']=='2021-07-28'and len(edges)==6,'AP1 selectiondate/atomicity changed')
    for asset,fr,to in [('Kemba Walker','BOS','OKC'),('Al Horford','OKC','BOS'),('Moses Brown','OKC','BOS')]:need(any(e['kind']=='STANDARD_CONTRACT'and e['asset']==asset and e['from']==fr and e['to']==to and e['event']=='AP1'for e in edges),'AP1 currentcontract ownership lost')
    cost=src[T1]['public_cost_family'];need(cost['Brown_future_protection_q_interval_usd']==[423280,1701593]and not cost['Aug3_new_cap_year_auto_carry'],'AP1 Brownprotection/NewYear boundary changed')
    picks=[x for x in src[DRAFT]['selected_rows']if x['conditional_final_draft_rights_holder']=='BOS'];need(len(picks)==1 and picks[0]['pick']==45 and picks[0]['player']=='Juhann Begarin'and picks[0]['lawful_PS21_participant_model_selected'],'Currentunsigned45 entitlement changed')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds)|{'Semi Ojeleye'});standard=sorted(expected);inactive=sorted(expected-set(active));need(len(active)==12 and len(inactive)==3,'Standard nomination changed')
    games=[];names=set(seconds);prepared=[]
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[HEALTH]['selected_dates']if x['game_id']==gid)
        need(g['opponent']=='BOS'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Three calendar joins changed')
        c=next(x for x in src[CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'SelectedCHIminutes changed')
        role={'blocks':blocks,'player_seconds':dict(seconds)};pair=base.paired(c,role);joint=base.assert_pair(c,role,pair);joint['BOS']=joint.pop('NYK')
        for x in pair:x['BOS']=x.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positiveinactive')
        names.update(joint['CHI']);prepared.append((g,h,pair,joint))
    need(src[AUTH]['selected']['selected_date_rows']['sha256']==PINS[HEALTH],'CHIauthority changed')
    langford=next(x for x in src[PRIOR]if x['player']=='Romeo Langford')
    need(langford['gp']=='0'and langford['seconds']=='0'and langford['cutoff']=='2021-03-24'and langford['sample_status']=='NO_PREDEADLINE_SAMPLE','Langford preopening sample boundary changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Romeo Langford'}|({'Coby White'}if 'Coby'in names else set()))
    rates['Romeo Langford']={'effective_rating':0.0,'exact_fraction':'0','classification':'SELECTED_FICTIONAL_ZERO_SAMPLE_EB_PRIOR_CENTER_NOT_OBSERVED_BPM',
      'provenance':{'source':PRIOR,'source_gp':0,'source_seconds':0,'source_cutoff':'2021-03-24','same_EB_zero_center_n0_limit':True,'historical_reported_BPM':None,'actual_future_ability_or_medical_certificate':False}}
    if 'Coby'in names:rates['Coby']=rates.pop('Coby White')
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'SharedsingleBPM product changed')
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*v/2880 for p,v in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['BOS'])-int(back['CHI']));m=impact['CHI']-impact['BOS']+home+fatigue;need(m!=0,'Tie needsOTmodel')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_BOS_impact_fraction':str(m),'CHI_minus_BOS_impact_per100':float(m),'selected_regulation_winner':'CHI'if m>0 else'BOS','score':None,'overtime_selection':None})
    feed=json.loads(base.FEED.read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows'];events=[{'GroupSort':x['GroupSort'],'date':x['TRANSACTION_DATE'][:10],'player':x['PLAYER_SLUG'],'description':x['TRANSACTION_DESCRIPTION'],'applied_to_this_model':False}for x in feed if x['TEAM_ID']==1610612738 and '2021-07-29'<=x['TRANSACTION_DATE'][:10]<='2022-04-06']
    first_number=min(int(x['game_number'])for x in src[det.CAL]if x['game_id']in IDS)
    following=next(x for x in src[det.CAL]if int(x['game_number'])==first_number+1)
    return {'id':'CHICAGO_BOSTON_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_NAMED_LAWFUL_FAMILY_AND_THREE_REGULATION_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,
      'selected_registration':{'standard':standard,'TW':[],'active':active,'inactive':inactive,'positive11_working_health_selected':True,'unused_zero_clinical_status':None,'STD':15,'TW_count':0,'original_protected_Kornet_salary_fully_retained':True,'AP1_existing_amendment_bonus_waiver_and_minimum_floor_conditions_preserved':deepcopy(src[DRAFT]['contract_implementation_family']),
        'Begarin45':'validoperativeW21 one-year minimum unaccepted firstRT; NBAUPC0/STD0; foreignX5/newnotice/subsequentdraft boundaries reopen','TW_expired':['Tacko Fall','Tremont Waters'],'TW_unaccepted_standard_QOs_oct1_end_no_extension':True,'TW_ROFR_FAclaims_and_priorprotectedΓ_preserved':True},
      'selected_BOS_role_blocks':blocks,'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_ratings':rates,'selected_games':games,
      'six_cost_categories':{'live':'Retained13 validcurrentterms (ParkerROS→minimum renewal whenneeded) +FournierBird3/Semi1min. AP1Horford/Moses originalcurrentΓ/q/waiverconditions inherited; newUPCs bonus0, fullstandardprotection.',
        'waived_former':'Kornet originalcurrentprotectedcharges and all older waived/former salary-year/stretchΓ retained. Parker oldcurrentΓ retained in bothbranches.',
        'FA_holds':'SignedFA only statutorilyreplaced; expiredFall/WatersQO/FRN/FA applicablecharges retained. NofullFArenounce0.',
        'unsigned':'Begarin45 and anyolderadmitted unsigned rights remain applicablelawfulRT/minimum-floor functions, noforcedUPC/foreverrights/extraSTD.',
        'unused_exceptions':'All currentapplicable inheritedTPE/MLE/BAE normal/apron treatment retained, no new2021NTMLE/BAE/incomingS&T; July28oldyearbudget notcarrypastAug3.',
        'incomplete':'lawfulcapcounts atprefix max(0,12−count)*YOS0min; finalSTD15=>0 bycount.'},
      'cap_admissibility':{'all_new_UPC_paths_named_exceptions':True,'new_2021_hardcap_trigger_count':0,'whole_private_normal_apron_total':None,'actual_private_no_other_obligation_certified':False},
      'original_reported_event_controls':events,'butterfly_handoff':['Fournier notNYK: no2021originalS&T/cash/2023second/newTPE imported. ExistingMarchORL→BOS rights remain.',
        'Thompson/Carsen/Semi retained, no originalRichardson/Dunn/Fernando/Schroder/White/Theis/SmartRobertWilliamsfutureextension trades/signings copied. Counterparties need ownfamily beforeconsumption.',
        'Kemba alreadyselectedOKC July28, no newJune18event orNYKbuyout copied; allAP1conditional2R ownership preserved.',
        'Parker two sourcecompatible live/minimumbranches are explicit, not newhistoricalguarantee claim. Three dates have chosennointerveningtransaction model; sourceevents enumerated, realabsencefalse.'],
      'summary':{'selected_games':3,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'BOS_wins':sum(g['selected_regulation_winner']=='BOS'for g in games),'STD':15,'TW':0,'active':12,'positive_BOS':11,'role_blocks':24,'paired_seconds_each':2880,'player_seconds_each':14400},
      'remaining_ports':{'next_chronological_key':following['game_id'],'opponent':following['opponent'],'date':following['date'],'needs':'named lawful PHI datedfamily/roles beforeselectedresult'},
      'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_salary_or_medical_or_private_receipt':False,'wholeprivate_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    lines=['# Boston AP1 keeper 가족·Chicago 세 날짜 결과','','**선택된 법적 NPC 가족·감독 역할·승자 모델; 독립 검문 대기.**','','|날짜|키|CHI상태|작업승자|CHI영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:lines.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_BOS_impact_per100']:.9f}|")
    lines+=['','selectedAP1은July28 Kemba→OKC/Horford·Moses→BOS 및 조건부2R의 기존실행이다. 원6/18 거래를 다시실행하지 않았다. current15 seed→Kemba제외+Horford/Moses→16, Kornet 유효만료/비양도방출 후 원current 보호Γ 보존으로15이다.','',
      'Fournier는 원ORL3시즌→승인MarchBOStrade의 ownFullBird3year flatbase 합법 q구간, Semi는1년 법정minimum. Parker는 공식프로필undercontract와 동결feedAprilROS의 차이를 숨기지 않고 currentlive Γ 또는 만료ROS→새1년minimum으로 이름붙였다. 실제term/금액을 하나로 발명하지 않았다. 각양태에서 기존원보호비용·보너스는 유지한다.','',
      'Fall/Waters의 연속두TW에서 유효standardQO는 미수락·비연장으로October1 수락기한만끝난다. ROFR/FAclaims를 삭제하지 않는다. Begarin45는 유효미수락RT이며 원래admitted 해외권리도 보존·날짜함수로재개방한다. final15STD0TW·active12이며 신인모두서명/모든TW재계약을 요구하지 않는다.','',
      '새usual5 Smart/Brown/Tatum/Horford/RobertWilliams, 240분 Smart32/Brown32/Tatum36/Horford30/Robert28/Fournier22/Grant20/Pritchard16/Nesmith10/Langford10/Parker4를 선택했다. 양팀규정시간48/240·초별fiveunique/포지션·선수분·CHI위임상태를 직접조인한다. 원Kornet48 수학fixture/원실점수·부상·OT를 복사하지 않는다. 3날짜 양수11의 가상건강선택이며 임상인증은false다.','',
      'live/waivedformer/FA/unsigned/unusedexception/incomplete Γ를 유지하고 source-supported ownBird/minimum/currentUPCs를 사용한다. AP1의과거July비용상단을Aug3후새해총액으로복사하지 않는다. 전체실제normal/apron총액은null·신규2021NTMLE/BAE/S&T없음이다. [NBA당시팀프로필](https://www.nba.com/draft/2021/team-profiles/boston-celtics) 웹본문·[2017CBA](https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf) 원PDF·동결feed를 소비한다. 직접profile403은본문증거로계수하지않았다.','',
      'FournierNYK/Thompson이탈/Schroder·Richardson·Dunn·Fernando·White·Theis 영입과 Smart/Robert 미래연장을 자동실행하지 않았다. 3날짜같은가족은 명시retention 모델이며 실제원보고 GroupSort가 발생하지않았다는 인증은 아니다. 상대팀·후속연도효과는 이름있는재개방입력이다.','',
      '## 7행 진행','','|번호|작업|현황|','|---|---|---|','|1|2020드래프트연쇄|완료|','|2|Chicago2020–21|완료|','|3|2021–23|Boston1가족·3결과 선택/검문대기|','|4|장기커리어|미완|','|5|결말·구조|미완|','|6|집필규격·Pack|현행누적기능등록기 참조·Pack0|','|7|통합·최종승인|CLOSED|','',
      '[현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 미완료 큰묶음5·6번까지4. v0.30 PARTIAL/CLOSED/원고0. 작성자음성통제는 독립검문으로 계수하지 않는다.','']
    return '\n'.join(lines)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved BOS family differs from source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]

def self_test():
    out=[];old=contracts
    def badprice():
        x=old();next(r for r in x if r['player']=='Evan Fournier')['price_function']['new_bonus']=100000;return x
    with patch(__name__+'.contracts',badprice):
        try:build()
        except ValueError:out.append('RETURNED_FOURNIER_UNSUPPORTED_NEW_BONUS')
        else:raise AssertionError('FalsePASS salary')
    oldsource=sources
    def badowner(root):
        x=oldsource(root);x[DRAFT]['event_trace'][0]['edges'][1]['to']='OKC';return x
    with patch(__name__+'.sources',badowner):
        try:build()
        except ValueError:out.append('RETURNED_SELECTED_AP1_HORFORD_OWNER_REVERSAL')
        else:raise AssertionError('FalsePASS owner')
    oldrole=role_blocks
    def badsequence():
        x=oldrole();x[6]['positions'],x[8]['positions']=x[8]['positions'],x[6]['positions'];return x
    with patch(__name__+'.role_blocks',badsequence):
        try:build()
        except ValueError:out.append('RETURNED_SELECTED_COACH_SEQUENCE_REORDER')
        else:raise AssertionError('FalsePASS order')
    return out

def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(physical(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'BOS currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'results':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_BOS_impact_per100')}for g in d['selected_games']],'writer_negative_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
