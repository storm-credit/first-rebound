"""October22 pair capacity under a named, unselected NOP operating proposal."""
from pathlib import Path
from collections import Counter
from unittest.mock import patch
import argparse, copy, csv, hashlib, io, json
import fitz
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_new_orleans_2021_second_paired_regulation_carrier.py'
OUT='simulation/CHICAGO_NEW_ORLEANS_2021_SECOND_PAIRED_REGULATION_CARRIER.json'
MD=OUT[:-5]+'.md'
BASELINE='820f3df'
CHI='simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json'
CAL='simulation/CHICAGO_2021_22_CALENDAR.csv'
ROSTER='simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json'
BOARD='research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json'
CHOICE='canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json'
ROLE='simulation/CHICAGO_2021_22_ROLE_PLAN_INPUTS.json'
PINS={'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json': '73d51b630e9c9d4ec31b7e3952906165589bd8c49a48bb07c79bdc9ad02e8fca', 'simulation/CHICAGO_2021_22_CALENDAR.csv': 'c59ea19a5515d64ed03cae8e0481847b6572d4087bbcefef15896bb7a2489183', 'simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json': 'cfa2f49bb82baa49b2298d90c97cd7fd8075e91380424d40bfd44772d8228a2b', 'research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json': '90099928f9133c4087ee7871939ce58216d183bd186f5ebd3575a56c2348eeed', 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json': '9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce', 'simulation/CHICAGO_2021_22_ROLE_PLAN_INPUTS.json': '0b8f9e4ac212596d0966f82f7f8317f7a7c86645a239a5a73587dd121f77e171', 'tools/build_chicago_2021_22_m1_dated_working_minutes.py': 'fe26befaf33d0da47a5614021ec2ed7f403e5f087ecf1acdc0e63e91fd2e9e1b'}
TEMP=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-chi-nop-paired-20261007')
RFA=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-nop-rfa-20261007/NBA2021_RFA.html')
RFA_SHA='c3791cc30b1a1eec3422778868a56a24b702fe2c42ce9ffe9cc2a42719b33611'
GUIDE=TEMP/'pelicans2324.pdf'
GUIDE_SHA='10102132eb90c4a8cebdcf8bbbffad5a2c541cf254b0592baf2cad3d1c42d6a0'
POS=('PG','SG','SF','PF','C')
GAME={'game_id':'0022100022','game_number':2,'date':'2021-10-22','home':'CHI','away':'NOP'}
POSITIONS={'PG':{'Lonzo Ball':28,'Killian Hayes':20},'SG':{'Eric Bledsoe':24,'Nickeil Alexander-Walker':16,'Moses Moody':8},
           'SF':{'Brandon Ingram':32,'Josh Hart':16},'PF':{'Josh Hart':8,'Naji Marshall':24,'Wenyen Gabriel':16},
           'C':{'Steven Adams':28,'Jaxson Hayes':12,'Willy Hernangomez':8}}
# New coach proposal, not observed Pelicans rotation or an imported DET stencil.
NOP_BLOCKS=[{'minutes':8,'positions':{'PG':'Lonzo Ball','SG':'Eric Bledsoe','SF':'Brandon Ingram','PF':'Josh Hart','C':'Steven Adams'}},
 {'minutes':16,'positions':{'PG':'Lonzo Ball','SG':'Eric Bledsoe','SF':'Brandon Ingram','PF':'Naji Marshall','C':'Steven Adams'}},
 {'minutes':4,'positions':{'PG':'Lonzo Ball','SG':'Nickeil Alexander-Walker','SF':'Brandon Ingram','PF':'Naji Marshall','C':'Steven Adams'}},
 {'minutes':4,'positions':{'PG':'Killian Hayes','SG':'Nickeil Alexander-Walker','SF':'Brandon Ingram','PF':'Naji Marshall','C':'Jaxson Hayes'}},
 {'minutes':8,'positions':{'PG':'Killian Hayes','SG':'Nickeil Alexander-Walker','SF':'Josh Hart','PF':'Wenyen Gabriel','C':'Jaxson Hayes'}},
 {'minutes':8,'positions':{'PG':'Killian Hayes','SG':'Moses Moody','SF':'Josh Hart','PF':'Wenyen Gabriel','C':'Willy Hernangomez'}}]
FIXED_POSITIONS=copy.deepcopy(POSITIONS)
FIXED_BLOCKS=copy.deepcopy(NOP_BLOCKS)
NOP_PLAN_SHA='dc772f74724c565186cdff3786585291c3fb1054ee787f0b5006ccb4ef3a6dad'  # Pin the complete reviewed proposal meaning, including contract conditions.

def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))

def sources():
 assert PINS and all(sha(p)==h for p,h in PINS.items()),'Reviewed source changed'
 data={p:load(p)for p in (CHI,ROSTER,BOARD,CHOICE,ROLE)}
 for p,v in data.items():assert v==json.loads(text(p)),'Source loader returned changed document'
 assert all(sha(p)==h for p,h in data[CHI]['source_sha256'].items()),'CHI carrier upstream stale'
 assert data[CHI]['certification']['independent_review_completed']
 cal=list(csv.DictReader(io.StringIO(text(CAL))))
 assert [(x['game_id'],x['date'],x['home'],x['away'])for x in cal[:2]]==[('0022100004','2021-10-20','DET','CHI'),('0022100022','2021-10-22','CHI','NOP')]
 cr=[x for x in data[CHI]['rows']if x['game_id']==GAME['game_id']]
 assert len(cr)==2 and {x['state']for x in cr}=={'NORMAL','COBY_OUT'}
 for x in cr:
  assert (x['game_number'],x['candidate_date'],x['home'],x['away'])==(2,'2021-10-22','CHI','NOP')
  assert x['state_selected_for_date']is False and x['player_minutes']['Markkanen']==32 and x['player_minutes']['Caruso']==18 and x['player_minutes']['Protagonist']==32
 rb=data[ROSTER]
 last=next(x for x in reversed(rb['team_game_bindings'])if x['team']=='NOP')
 assert last['date']=='2021-05-16' and last['event_id']=='2021-05-16_NOP_LAL'
 state=rb['roster_states'][last['state_id']]
 assert state['standard_count']==15 and state['two_way_count']==1
 board=[x for x in data[BOARD]['rows']if x['conditional_final_draft_rights_holder']=='NOP']
 assert [(x['pick'],x['player'])for x in board]==[(9,'Moses Moody'),(34,'Kessler Edwards'),(40,'Miles McBride'),(42,'Greg Brown'),(52,'Jericho Sims')]
 assert all(x['new_author_lock']is False and x['new_NBA_contract_or_tender']is False for x in board)
 assert data[CHOICE]['selected']['route']=='G1A_PLUS_M1' and 'G1C_PLUS_M1_LONZO'in data[CHOICE]['mutually_exclusive_routes_not_selected']
 return data,cr,state,board

def raw_sources():
 assert hashlib.sha256(RFA.read_bytes()).hexdigest()==RFA_SHA
 r=BeautifulSoup(RFA.read_text(encoding='utf-8'),'html.parser')
 j=json.loads(r.find('script',id='__NEXT_DATA__').string)
 body=BeautifulSoup(j['props']['pageProps']['article']['contentText'],'html.parser').get_text(' ',strip=True)
 assert 'Lonzo Ball (NOP)'in body and 'Josh Hart (NOP)'in body and "Louzada's team option was declined"in body and 'qualifying offer'in body
 assert 'as of Aug. 1.'in body
 assert hashlib.sha256(GUIDE.read_bytes()).hexdigest()==GUIDE_SHA
 doc=fitz.open(GUIDE);t=doc[147].get_text()
 assert 'Re-signed center Willy Hernangómez and guard Didi Louzada'in t and 'Re-signed guard Josh Hart'in t
 assert 'Wenyen Gabriel'in t and 'October 12, 2021'in t and 'August 7, 2021'in t and 'Steven Adams'in t and 'Eric Bledsoe'in t
 return {'NBA_RFA':{'url':'https://www.nba.com/news/2021-free-agency-options-and-qualifying-offers','cache_path':str(RFA),'raw_sha256':RFA_SHA,
          'locator':'__NEXT_DATA__.props.pageProps.article.contentText: Aug1 issuedRFA list and Louzada** footnote',
          'observed_scope':'Ball/Hart issuedQO; Louzada optiondeclined+issuedQO. No money, acceptance or counterfactual contract certified.'},
         'official_guide':{'url':'https://cdn.nba.com/teams/uploads/sites/1610612740/2023/10/Pelicans-2324-Media-Guide.pdf','cache_path':str(GUIDE),'raw_sha256':GUIDE_SHA,
          'PDF_1based':148,'printed_page':147,'fitz_text_sha256':hashlib.sha256(t.encode()).hexdigest(),
          'observed_scope':'Historical Aug16 Willy/Louzada and Aug19 Hart renewals; Aug7 asset event and Oct12 Gabriel waiver. These are comparison facts, not candidate acceptances.'},
         'web_observations_without_adopted_raw':[
          {'url':'https://www.nba.com/draft/2021/team-profiles/new-orleans-pelicans','observation':'Primary indexed body distinguishes contracted players and pending free agents; original Kira substituted by approved Killian in working roster.',
           'direct_HTTP_status':403,'raw_cache_path':str(TEMP/'roster_profile.raw'),'raw_sha256':'09694c20b7e55daff6a3d8caf452a2e2f8e5d73faefbcbfb8e949d82c280b309','raw_body_adopted':False},
          {'url':'https://www.nba.com/news/zion-williamson-foot-to-be-reevaluated-in-2-weeks','observation':'Oct14 club executive announcement: opening availability restricted. Counterfactual clinical state is not inferred.',
           'direct_HTTP_status':403,'raw_cache_path':str(TEMP/'zion.raw'),'raw_sha256':'472a8b3e0c491acd7288e60b5a6092e9cb5a133b24dd8d50ae6fefac41cc1e44','raw_body_adopted':False}],
         'fresh_successful_official_PDFs':1,'reused_root_RFA_raws':1,'new_league_medical_or_receipt_certificate':False}

def nop_plan(state, board):
 assert POSITIONS==FIXED_POSITIONS and NOP_BLOCKS==FIXED_BLOCKS,'New proposed role input changed without review'
 old=[x['player']for x in state['players']if x['contract_class']=='STANDARD']
 std=[n for n in old if n!='James Johnson']+['Moses Moody']
 assert len(std)==len(set(std))==15 and 'Killian Hayes'in std and 'Kira Lewis Jr.'not in std
 positive=Counter()
 for p,players in POSITIONS.items():
  assert sum(players.values())==48
  for n,v in players.items():positive[n]+=v*60
 assert len(positive)==12 and sum(positive.values())==14400 and set(positive)<=set(std)
 active=[n for n in std if n in positive];inactive=[n for n in std if n not in positive]
 assert len(active)==12 and set(inactive)=={'Zion Williamson','Didi Louzada','Wes Iwundu'}
 return {'standard_candidate':std,'two_way_candidate':[],'active_standard_12':active,'inactive_standard_3':inactive,
         'positive_player_seconds':dict(sorted(positive.items())),'position_minutes':copy.deepcopy(POSITIONS),'ordered_working_blocks':copy.deepcopy(NOP_BLOCKS),
         'operational_unavailable_condition':['Zion Williamson'],'unused_reserve_clinical_status':None,
         'proposed_operating_family':'NOP_RETAINED_CORE_NO_OPTIONAL_SUMMER_TRADES_PLUS_CONDITIONAL_MOODY9_UPC',
         'selected':False,'actual_medical_or_registration_certified':False,
         'dated_contract_conditions':[
          {'players':['Lonzo Ball','Josh Hart','Didi Louzada'],'condition':'Valid2021 required QO where applicable, not withdrawn or rescinded; consensually accept applicable legal one-year QO before its operative acceptance cutoff and Oct22. For Louzada no expired option silently carried. QO numbers/actual receipts/acceptance remain null.','actual_acceptance':None,'new_author_lock':False},
          {'players':['Willy Hernangomez'],'condition':'New lawful minimum-exception contract1or2years/bonus0, valid consent before Oct22; original Aug16 newcontract is fact, its exact terms not copied. No 2020expired salary carried as live UPC.','actual_acceptance':None,'new_author_lock':False},
          {'players':['Moses Moody'],'condition':'Only if unselected DB1 pick9 and NOP ownership are implemented: valid rookie-scale UPC80–120% as applicable with consent before game. Salary/guarantee/bonus inputs remain parameters and no amount is certified.','actual_acceptance':None,'new_author_lock':False},
          {'players':['Wenyen Gabriel'],'condition':'Carry lawful existing 2021–22 contracted identity subject to live-term/guarantee control; no Oct12 waiver in this candidate. This is an unselected routine roster alternative, not erasure of original reported waiver/dead money.','actual_acceptance':None,'new_author_lock':False},
          {'players':['Steven Adams','Eric Bledsoe','Wes Iwundu'],'condition':'No optional Aug7 MEM/CHA multi-party transaction in this proposal. Retain existing live contracts and all original obligations; no counterparty acceptance or matching capacity inferred.','actual_acceptance':None,'new_author_lock':False},
          {'players':['Nickeil Alexander-Walker','Jaxson Hayes','Zion Williamson','Killian Hayes','Brandon Ingram','Naji Marshall'],
           'condition':'Each retained UPC must actually cover2021–22 within this candidate. Required2019rookie Year3 option notices must be validly exercised in the preceding operative window; Oct2021 fourthyear notices concern2022–23, not permission for this game. Killian valid2020 rookie secondyear family is preserved without importing historical Kira contract cents.','actual_acceptance':None,'new_author_lock':False},
          {'players':['James Johnson','James Nunnally'],'condition':'Old terms expire; no newNOP UPC/TW signed before this game. Old FA/QO/RT/settlement charges and rights are not zeroed by roster exclusion. Nunnally priorTW is not automatically renewed.','actual_acceptance':None,'new_author_lock':False}],
         'unaccepted_second_round_rights':[{'pick':x['pick'],'player':x['player'],'holder':'NOP','UPC_selected':False,'valid_RT_and_cost_family_still_required':True}for x in board if x['round']==2],
         'counterfactual_new_Ball_to_CHI_or_Graham_to_NOP_or_Valanciunas_to_NOP':False,
         'whole_cost_upper':None,'whole_legal_operating_family_pass':False}

def clock(blocks):
 t=0;out=[]
 for i,b in enumerate(blocks):
  n=b['minutes']*60;assert isinstance(n,int)and n>0
  out.append({'block_index':i,'start':t,'end':t+n,'positions':copy.deepcopy(b['positions'])});t+=n
 assert t==2880
 return out

def assert_source_clock(timeline,blocks):
 assert len(timeline)==len(blocks)
 t=0
 for i,(x,b)in enumerate(zip(timeline,blocks)):
  n=int(b['minutes'])*60
  assert x=={'block_index':i,'start':t,'end':t+n,'positions':b['positions']},'Returned clock differs from source block order'
  t+=n
 assert t==2880

def pair(c,n,ct,nt):
 cuts=sorted({0,720,1440,2160,2880}|{x['end']for x in ct+nt})
 segs=[]
 for a,b in zip(cuts,cuts[1:]):
  cc=next(x for x in ct if x['start']<=a<x['end']);nn=next(x for x in nt if x['start']<=a<x['end']);q=a//720+1
  segs.append({'start_second':a,'end_second':b,'seconds':b-a,'quarter':q,'clock_start_remaining':q*720-a,'clock_end_remaining':q*720-b,
               'CHI_block_index':cc['block_index'],'NOP_block_index':nn['block_index'],'CHI':copy.deepcopy(cc['positions']),'NOP':copy.deepcopy(nn['positions'])})
 return {'id':c['state']+'__NOP_ZION0_CONDITIONAL_RETAINED_CORE','CHI_state':c['state'],'selected_for_date':False,
         'nominations':{'CHI':{'standard':c['standard_registered_candidate'],'TW':c['two_way_registered_candidate'],'active':c['working_active_nominees'],'inactive':c['standard_inactive_nominees'],'unavailable':c['conditional_unavailable']},
                        'NOP':{'standard':n['standard_candidate'],'TW':n['two_way_candidate'],'active':n['active_standard_12'],'inactive':n['inactive_standard_3'],'unavailable':n['operational_unavailable_condition']}},
         'simultaneous_segments':segs,'regulation_elapsed_seconds':2880,'player_seconds_each':{'CHI':14400,'NOP':14400},'score':None,'winner':None,'OT_selected':False}

def assert_pair(row,c,n,ct,nt,eligibility):
 assert row['CHI_state']==c['state'] and row['id']==c['state']+'__NOP_ZION0_CONDITIONAL_RETAINED_CORE'
 assert row['selected_for_date']is False and row['score']is None and row['winner']is None and row['OT_selected']is False
 expected={'CHI':{'standard':c['standard_registered_candidate'],'TW':c['two_way_registered_candidate'],'active':c['working_active_nominees'],'inactive':c['standard_inactive_nominees'],'unavailable':c['conditional_unavailable']},
           'NOP':{'standard':n['standard_candidate'],'TW':[],'active':n['active_standard_12'],'inactive':n['inactive_standard_3'],'unavailable':['Zion Williamson']}}
 assert row['nominations']==expected,'Roster/active/conditional availability changed'
 for team,nom in expected.items():
  assert len(nom['standard'])==len(set(nom['standard']))==15 and len(nom['TW'])<=2
  assert len(nom['active'])==len(set(nom['active']))==12 and len(nom['inactive'])==3
  assert set(nom['active'])|set(nom['inactive'])==set(nom['standard']) and not set(nom['active'])&set(nom['inactive'])
  assert not set(nom['active'])&set(nom['unavailable']) and not set(nom['standard'])&set(nom['TW'])
 assert not set(expected['CHI']['standard']+expected['CHI']['TW'])&set(expected['NOP']['standard'])
 cuts=sorted({0,720,1440,2160,2880}|{x['end']for x in ct+nt})
 assert len(row['simultaneous_segments'])==len(cuts)-1
 count={t:Counter()for t in ('CHI','NOP')};poscount={t:{p:Counter()for p in POS}for t in count}
 for i,s in enumerate(row['simultaneous_segments']):
  a,b=cuts[i:i+2];q=a//720+1
  assert (s['start_second'],s['end_second'],s['seconds'],s['quarter'],s['clock_start_remaining'],s['clock_end_remaining'])==(a,b,b-a,q,q*720-a,q*720-b),'Returned simultaneous clock changed'
  for team,timeline,elig,creators in [('CHI',ct,eligibility,['LaMelo_pick4','LaVine']),('NOP',nt,{p:list(v)for p,v in FIXED_POSITIONS.items()},['Lonzo Ball','Killian Hayes','Brandon Ingram','Eric Bledsoe'])]:
   src=next(x for x in timeline if x['start']<=a<x['end'])
   assert b<=src['end'] and s[team+'_block_index']==src['block_index'] and s[team]==src['positions'],'Returned lineup/source order changed'
   line=s[team];assert set(line)==set(POS)and len(set(line.values()))==5
   assert set(line.values())<=set(expected[team]['active'])and set(line.values())&set(creators)
   for p,name in line.items():assert name in elig[p];count[team][name]+=b-a;poscount[team][p][name]+=b-a
 for team,pm in [('CHI',c['position_minutes']),('NOP',FIXED_POSITIONS)]:
  for p in POS:assert dict(poscount[team][p])=={k:v*60 for k,v in pm[p].items()}and sum(poscount[team][p].values())==2880
  targets={k:v*60 for k,v in c['player_minutes'].items()}if team=='CHI'else n['positive_player_seconds']
  assert dict(count[team])==targets and sum(count[team].values())==14400
 assert row['regulation_elapsed_seconds']==2880 and row['player_seconds_each']=={'CHI':14400,'NOP':14400}

def assert_nop(n,state,board):
 # Direct caller guard, not a second invocation of the patched proposal constructor.
 old=[x['player']for x in state['players']if x['contract_class']=='STANDARD']
 assert n['standard_candidate']==[x for x in old if x!='James Johnson']+['Moses Moody'] and n['two_way_candidate']==[],'NOP source identities changed'
 assert n['position_minutes']==FIXED_POSITIONS and n['ordered_working_blocks']==FIXED_BLOCKS,'NOP proposed minutes changed'
 assert n['selected']is False and n['whole_cost_upper']is None and n['whole_legal_operating_family_pass']is False and n['actual_medical_or_registration_certified']is False
 assert [x['pick']for x in n['unaccepted_second_round_rights']]==[34,40,42,52]
 assert all(x['UPC_selected']is False and x['valid_RT_and_cost_family_still_required']is True for x in n['unaccepted_second_round_rights'])
 assert hashlib.sha256(json.dumps(n,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()==NOP_PLAN_SHA,'NOP proposal conditions or authority changed'

def build():
 data,cr,state,board=sources();raw=raw_sources();n=nop_plan(state,board);assert_nop(n,state,board)
 nt=clock(n['ordered_working_blocks']);assert_source_clock(nt,n['ordered_working_blocks']);rows=[]
 for c in cr:
  ct=clock(c['unordered_regulation_blocks']);assert_source_clock(ct,c['unordered_regulation_blocks']);row=pair(c,n,ct,nt)
  assert_pair(row,c,n,ct,nt,data[ROLE]['position_eligibility_design_only']);rows.append(row)
 assert len(rows)==2
 return {'id':'CHICAGO_NEW_ORLEANS_2021_SECOND_PAIRED_REGULATION_CARRIER','status':'INDEPENDENTLY_REVIEWED_NAMED_OPERATING_PROPOSAL_AND_CONDITIONAL_PAIR','baseline_main':BASELINE,
         'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'Repository BOMstrip, CRLF/CR to LF; external raw bytes unchanged',
         'game':GAME,'calendar_class':'SAME_OBSERVED_KEY_IS_WORKING_HYPOTHESIS_NOT_RESULT_ADOPTION','raw_sources':raw,
         'classification':{'fact':'Existing approved2020 Killian NOP landing and S2 May16 working roster; original2021 RFA/renewals/transactions only as public comparator facts.',
                           'candidate':'No optionalNOP summertrades, lawful conditional renewals+Moody9 UPC, new coach minutes/ordered6blocks and Zion0 operational state; no author lock.',
                           'inference':'If all named live-contract, availability and active conditions hold, this simultaneous regulation capacity exists.'},
         'NOP_named_proposal':n,'witnesses':rows,
         'summary':{'game_keys':1,'CHI_states':2,'NOP_new_ordered_blocks':6,'NOP_positive_players':12,'NOP_STD':15,'NOP_TW':0,'active_standard_each':12,'inactive_standard_each':3,
                    'simultaneous_segments_each':len(rows[0]['simultaneous_segments']),'regulation_seconds':2880,'player_seconds_each':14400,'pair_player_seconds':28800,
                    'Markkanen_minutes':32,'Caruso_minutes':18,'Protagonist_minutes':32,'new_selected_date_states':0,'new_scores_or_winners':0},
         'remaining_named_inputs':['NOP retained-core versus optionalMEM/CHA/Ball otherdestination paths are still alternatives, not selected transactions.',
            'Lawful live2021 UPC/QO acceptance for Ball/Hart/Louzada, Willy newminimum and Moody conditionalrookie; consent and exactmoney remain input conditions.',
            'NOP wholepublic sixcategory costs including oldFA/waiver/TPE/2R tender charges not bounded here; noprivate wholeledger evidence gate added.',
            'A different Zion/other availability state requires a new explicit minute/nomination witness; no historical injury or contact outcome automatically inherited.',
            'Result method, scoring/OT choice and remaining80 games still separate. DET carrier not copied as NOP minutes.'],
         'certification':{'independent_review_completed':True,'independent_review_basis':'Root independent fr-root-nop-468.py imported no producer: all2880-second arrays matched CHI11 and NOP6 source blocks, player budgets/active/ownership, S2May16STD15 minusJamesJohnson plusMoody, unsigned2R4 and falsecost/health/result conditions. Root directly matched raw2SHA and officialguidePDF148 Aug16/19 renewals, Aug7/8 transfers and Oct12Gabrielwaiver against candidate separation. Only conditional rotation capacity accepted; writer3controls are not independent review.',
                          'simultaneous_conditional_capacity_constructed':True,'whole_legal_roster_cost_family_pass':False,
                          'actual_contract_acceptance_medical_or_registration':False,'dated_NBA_acquisition_health_OT_or_result_selected':False,
                          'new_author_lock':False,'whole2021_22_or_macro3_complete':False,'central_or_REGISTER_changed':False,'actual_context_packs':0,'manuscript_written':0}}

def validate(o):
 try:assert o==build(),'Saved carrier differs from source-bound reconstruction';return []
 except(AssertionError,KeyError,OSError,ValueError,StopIteration)as e:return[str(e)]

def markdown(o):
 s=o['summary']
 return '\n'.join(['# Chicago–New Orleans: 두 번째 경기 전체 정규시간 후보 입력','',o['status'],'',
 '기존82일정의 다음 키는 **0022100022 / 2021-10-22 / CHI 홈·NOP 원정**이다. 기존 paired에 NOP 분 입력은 없어 새 조건부 감독 배분을 만들었다. DET 분/선수나 원역사 점수·부상·OT를 복사하지 않았다.','',
 f"CHI NORMAL·COBY_OUT × 한 NOP 조건부 명단의2조합. 각 **{s['simultaneous_segments_each']}개 동시구간·48분·팀별240분**, 포지션마다48분, 양쪽5인·소속·active12/STDinactive3 전수 검산. M1 Mark32/Caruso18/주인공32 보존. NOP 새6블록의 양수12명은 모두 active이며 TW는0(최대2와 구별).",'',
 '## 명명된 제안과 권한','',
 'S2 NOP 말단STD15에서 만료한 James Johnson의 신규NOP 계약은 제안하지 않고, 미선택DB1의 Moody9 신인UPC를 조건으로 넣었다. 승인 Killian Hayes 귀속을 유지한다. Ball/Hart/Louzada는 자동 재계약이 아니라 유효QO 존속·적법시한 내 조건부 수락, Willy는 새로운 합법최소계약을 제안한다. 원실제 금액·수락을 복사하지 않는다. Gabriel의 기존live계약 보존과 원10/12 waiver 미적용은 **미선택 운영 대안**이다.','',
 'Adams/Bledsoe/Iwundu를 원MEM/CHA 거래로 자동 제거하지 않는다. Graham/Valanciunas/Murphy/HerbJones 및 Ball→CHI·Satoransky→NOP 영입은 없다. 현재 후보는 이들 거래를 실행하지 않은 명명가족이며 해당 중요방향을 선택한 것은 아니다. DB1 두번째라운드4명은 별도 미서명 권리/유효RT/비용 조건이고 새로운STD4명이 아니다. Nunnally의 과거TW도 자동연장하지 않으며 오래된FA/보호 차지는 소속제외로 삭제되지 않는다.','',
 'Zion0은 이번 **조건부 운영 입력**이다. 10/14 리그의 프리시즌 제한 발표를 관측했으나 그것을 대체세계 진단/전체건강 사실로 상속하지 않는다. 양수12명의 가용성·작업active nomination과 미출전STD3명의 임상null을 구분한다. 특히 Josh Hart PF8분은 새small-lineup 감독 가정이며 원역사 역할이나 효율 인증이 아니다.','',
 '## 원천과 실패 구분','',
 '[NBA RFA 목록](https://www.nba.com/news/2021-free-agency-options-and-qualifying-offers)의 raw본문을 직접 읽어 Aug1 QO 상태만 연결했다. [NOP 공식가이드](https://cdn.nba.com/teams/uploads/sites/1610612740/2023/10/Pelicans-2324-Media-Guide.pdf) PDF148/인쇄147의 거래·재서명 행을 새 회수했다. 후대가이드의2021역사만 비교하며 미래기록을 계약조건/대체미래로 사용하지 않는다. 일부NBA직접HTTP403은 원문수집 성공이 아니며 indexed본문 관측과 raw를 분리했다.','',
 '전체비용·QO실수락·신인권리/UPC·해외/타팀조건의 실행은 아직 조건이다. 그와 별도로 두 팀 정규시계의 완전한 용량 증인은 구성했다. Root는 생성기를 import하지 않고2880초 배열·CHI11/NOP6 블록·선수분/소속/active·말단15인 치환·미서명2R4·미인증조건을 직접 대조했다. raw2SHA·공식가이드PDF148 본문도 별도 읽어 후보 교대 용량만 독립 수용했다. 작성자 음성3건을 독립으로 계수하지 않는다. 원천목록·rawSHA·의미 검문은 JSON/producer에 기록했다.','',
 '## 7행 현황','', '| 번호 | 작업 | 상태 |','|---|---|---|',
 '|1|2020 드래프트 연쇄|완료|','|2|Chicago 2020–21|S2 완료|','|3|2021–23 거래·계약|DET/NOP 전체 정규시계 조건부 용량 독립수용|',
 '|4|장기 커리어|후속 시즌 실행 대기|','|5|결말·전체 구조|전체 기능표 미완료|','|6|집필 규격·Context Pack|현행 누적기능 등록기 참조·실제Pack0|','|7|통합·독립·작가 승인|최종CLOSED|','',
 '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 미완료큰묶음5·freeze v0.30 PARTIAL·설계/원고CLOSED·원고0. 중앙/원장/Git 변경0.',''])

def self_test():
 count=0;original=pair
 def wrong_clock(*a):
  o=original(*a);o['simultaneous_segments'][0]['seconds']+=1;return o
 def wrong_owner(*a):
  o=original(*a);o['simultaneous_segments'][0]['NOP']['PG']='Satoransky';return o
 for fn in(wrong_clock,wrong_owner):
  with patch(__name__+'.pair',fn):
   try:build()
   except AssertionError:count+=1
   else:raise AssertionError('Returned paired meaning mutation passed')
 old=nop_plan
 def silent_signed_second(*a):
  o=old(*a);o['unaccepted_second_round_rights'][0]['UPC_selected']=True;return o
 with patch(__name__+'.nop_plan',silent_signed_second):
  try:build()
  except AssertionError:count+=1
  else:raise AssertionError('Unsigned rights promoted to contract')
 return count

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();o=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(o),encoding='utf-8')
 r={'summary':o['summary']}
 if a.check:assert load(OUT)==o and text(MD)==markdown(o),'Saved carrier stale';r['current']=True
 if a.self_test:r['writer_negative_controls_rejected']=self_test()
 print(json.dumps(r,ensure_ascii=False))
