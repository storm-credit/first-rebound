"""Dated pre-Jordan candidate carrier with source-bound contracts and honest residual ports.
No fiveway adoption, complete private ledger, future clinical choice, or exact salary lock.
"""
import argparse,copy,hashlib,itertools,json,re
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
from bs4 import BeautifulSoup
import fitz
import build_detroit_2021_initial_residual_cost_family as tab
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_bkn_was_2021_pre_jordan_named_execution_family.py'
OUT='research/BKN_WAS_2021_PRE_JORDAN_NAMED_EXECUTION_FAMILY_2026_10_07.json'
MD=OUT[:-5]+'.md'
BASELINE='892fdb4c5cca8be7a33c3fe5362d30cad2145104'
BOARD='research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json'
JOINT='research/DETROIT_BROOKLYN_2021_JORDAN_JOINT_TRADE_FAMILY_2026_10_07.json'
CW='research/CHA_WAS_FINITE_ROSTER_WORKING_FAMILY_2026_10_07.json'
GSW='simulation/GSW_G1_OPTION3_NY_WORKING_EXECUTION.json'
CBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'

def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def dollar(s):return int(re.sub('[^0-9]','',s.split(' ')[0]))
def canonical(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def policy():
 return {'selected':False,'candidate':'P1_SEPARATE_LAL_WAS_THEN_BKN_WAS_SAS','working_dated_scope':['2021-08-02','2021-09-04'],
  'named_NBA_UPCs_for_BKN_pre_Jordan':14,'new_BKN_two_way_UPCs':0,
  'new_BKN_contracts':['Cameron Thomas','Bruce Brown','Blake Griffin','Patty Mills',"DeAndre\u0027 Bembry",'LaMarcus Aldridge'],
  'BKN_Alize_current_contract_retained':True,'BKN_Shamet_trade_NOT_SELECTED_preserved':True,
  'historical_new_Carter_Sharpe_Johnson_Millsap_not_copied':True,
  'new_Bruce_one_year_Bird_offer_upper':5000000,'new_Bruce_offer_is_not_original_QO_acceptance':True,
  'new_minimum_fullcash_upper':2650000,'new_minimum_signing_performance_bonuses':0,
  'new_Patty_TaxpayerMLE_first_year':5890000,'new_Patty_two_year_schedule':[5890000,6184500],
  'new_rookie_RSC_80_120_of_applicable_official_scale':True,'conditional_rookie_up_to_3m_BKN27_4m_WAS12_2_5m_LAL22':True,
  'WAS_Homesley_waiver_before_first_rookie_UPC_with_full_current_1517981_reserved':True,
  'WAS_Gary_Trent_new_Bird_offer_upper':5000000,'WAS_new_Dinwiddie_three_full_seasons_no_option_no_bonus_first_fully_protected':True,
  'Dinwiddie_valid_prior_option_nonexercise_at_applicable_deadline':True,
  'Dinwiddie_original_actual_17142857_plus_2571428_NOT_copied':True,
  'applicable_original_tradebonuses_full_consensual_waiver':True,'waiver_six_month_restriction':'2022-02-06_OR_LATER_IF_OTHERWISE_ELIGIBLE',
  'preserve_all_retained_likely_and_unlikely_reported_components':True,
  'candidate_BKN_paid_trade_cash_before_Sep4':0,'candidate_WAS_to_SAS_trade_cash':0,
  'candidate_unused_exception_written_renounce_after_TPE_use':True,'old_unpaid_earned_or_protected_money_erased':False,
  'future_health_minutes_result_selected':False,'new_author_lock':False,'actual_acceptance':None}
FIXED_POLICY=copy.deepcopy(policy())
CORE_BKN={'Kevin Durant':('kevin-durant',42018900,40918900,1100000,0),
 'Kyrie Irving':('kyrie-irving',35328700,34916200,412500,687500),
 'James Harden':('james-harden',44310840,44310840,0,0),
 'Joe Harris':('joe-harris',17357143,17357143,0,500000),
 'Nicolas Claxton':('nicolas-claxton',1782621,1782621,0,0),
 'Landry Shamet':('landry-shamet',3768342,3768342,0,0),
 'Alize Johnson':('alize-johnson',1762796,1762796,0,0)}
CORE_WAS={'Russell Westbrook':('russell-westbrook',44211146,44211146,0,0),
 'Bradley Beal':('bradley-beal',34502129,34502129,0,0),
 'Davis Bertans':('davis-bertans',16000000,16000000,0,0),
 'Thomas Bryant':('thomas-bryant',8666667,8666667,0,0),
 'Rui Hachimura':('rui-hachimura',4916160,4916160,0,0),
 'Deni Avdija':('deni-avdija',4692840,4267840,425000,0),
 'Daniel Gafford':('daniel-gafford',1782621,1782621,0,0),
 'Troy Brown Jr.':('troy-brownjr',5170564,5170564,0,0),
 'Anthony Gill':('anthony-gill',1517981,1517981,0,0)}
LAL_OUT={'Kentavious Caldwell-Pope':('kentavious-caldwellpope',13038862,13038862,0,0),
 'Kyle Kuzma':('kyle-kuzma',13000000,13000000,0,0),
 'Montrezl Harrell':('montrezl-harrell',9720900,9720900,0,0)}
FIXED_CORE_BKN=copy.deepcopy(CORE_BKN);FIXED_CORE_WAS=copy.deepcopy(CORE_WAS);FIXED_LAL_OUT=copy.deepcopy(LAL_OUT)

def read_sources():
 assert CORE_BKN==FIXED_CORE_BKN and CORE_WAS==FIXED_CORE_WAS and LAL_OUT==FIXED_LAL_OUT,'Retained named salary/performance template changed'
 repository={}
 for p,h in PINS.items():
  assert sha(p)==h,'Unreviewed repository source: '+p
  if p.endswith('.json'):
   o=load(p);assert o==json.loads(text(p)),'Reader returned different source meaning: '+p;repository[p]=o
 joint=repository[JOINT];assert joint['certification']['independent_review_completed'] and not joint['certification']['whole_BKN_cost_PASS']
 assert joint['BKN']['normal_and_adjusted_apron_delta']==-4137895
 board={r['pick']:r for r in repository[BOARD]['rows']}
 expected={12:('WAS','Corey Kispert'),22:('LAL','Jared Butler'),27:('BKN','Cameron Thomas'),31:('MIL','Kai Jones'),43:('BKN','Isaiah Todd'),51:('BKN','Marcus Zegarowski'),59:('BKN','RaiQuan Gray')}
 for k,(team,name)in expected.items():assert (board[k]['conditional_final_draft_rights_holder'],board[k]['player'])==(team,name),'Changed-world draft identity/holder changed'
 assert 'Troy Brown Jr.와 Gary Trent Jr.는 Washington에 남는다.' in text('simulation/2021_WASHINGTON_CHICAGO_PORTLAND_TRANSACTION_CASCADE.md')
 assert repository[CW]['selection']['WAS_HOMESLEY']['working_signing_date']=='2021-05-15'
 assert repository[GSW]['independent_review_complete'] and repository[GSW]['authority']['root_working_selection']
 bodies={};raw=[]
 for r in RAW:
  b=Path(r['cache_path']).read_bytes();assert hashlib.sha256(b).hexdigest()==r['raw_sha256'],'External raw changed '+r['id']
  soup=BeautifulSoup(b,'html.parser');title=soup.title.get_text(' ',strip=True)if soup.title else ''
  adopted=r['status']==200 and 'Player not found'not in title
  raw.append({**r,'body_adopted':adopted,'not_adopted_reason':None if adopted else 'HTTP200_PLAYER_NOT_FOUND_NOT_CONTRACT_BODY'})
  if adopted:bodies[r['id']]=b
 def row(spec):
  slug,cap,base,likely,unlikely=spec
  rr=[r for t in tab.tables(bodies[slug])for r in t if len(r)==8 and r[0].split(' ')[0]=='2021-22' and dollar(r[3])==cap and dollar(r[4])==base and dollar(r[6])==likely and dollar(r[7])==unlikely]
  assert rr,'Named salary/performance row missing '+slug
  return {'reported_row':rr[0],'normal_cap_component':cap,'base':base,'likely':likely,'unlikely':unlikely,'apron_all_performance_component':cap+unlikely,'actual_contract_terms_certified':False}
 contracts={k:row(v)for k,v in {**CORE_BKN,**CORE_WAS,**LAL_OUT}.items()}
 contracts['DeAndre Jordan']={'reported_row':joint['original_contract_reported_rows']['Jordan'],'normal_cap_component':9881598,'base':9881598,'likely':0,'unlikely':0,'apron_all_performance_component':9881598,'actual_contract_terms_certified':False}
 contracts['Caleb Homesley']=row(('caleb-homesley',1517981,1517981,0,0))
 rr=[r for t in tab.tables(bodies['spencer-dinwiddie'])for r in t if len(r)==8 and r[0]=='2020-21' and dollar(r[3])==11454048]
 assert rr and rr[0][-2:]==['$0','$0'],'Dinwiddie prior reported salary changed'
 contracts['Spencer Dinwiddie prior']={'reported_row':rr[0],'prior_base':11454048,'new_contract_accepted':None}
 assert 'Yes (Dec 21, 2020)'in str(contracts['Landry Shamet']['reported_row'])
 assert 'Yes (Dec 28, 2020)'in str(contracts['Troy Brown Jr.']['reported_row'])
 assert 'Yes (Jul 29, 2021)'in str(contracts['Montrezl Harrell']['reported_row'])
 observations=[]
 for r in OBS:
  b=Path(r['cache_path']).read_bytes();assert hashlib.sha256(b).hexdigest()==r['capture_sha256'];observations.append({**r,**json.loads(b)})
 assert hashlib.sha256(CBA.read_bytes()).hexdigest()==CBA_SHA
 with fitz.open(CBA) as d:
  nums=[54,55,197,198,204,210,226,228,233,234,235,236,240,241,248,249,251,252,253,254,255,292,294,302,303,305,311,312,313,398,561]
  pages={str(n):hashlib.sha256(d[n-1].get_text().replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()for n in nums}
  assert 'at least three (3) Seasons' in ' '.join(d[252].get_text().split())and 'first Season' in ' '.join(d[253].get_text().split())
  assert 'fifty percent (50%)'in d[235].get_text()
  assert 'any time renounce'in ' '.join(d[239].get_text().split())
  assert '2,328,652'in d[560].get_text()
 assert hashlib.sha256(Path(LAL_GUIDE['cache_path']).read_bytes()).hexdigest()==LAL_GUIDE['raw_sha256']
 with fitz.open(LAL_GUIDE['cache_path']) as d:
  p96=d[95].get_text();assert '8/5/21' in p96 and 'five-team' in p96
  lalpage={'PDF1based':96,'text_LF_sha256':hashlib.sha256(p96.replace('\r\n','\n').replace('\r','\n').encode()).hexdigest(),'reported_transaction_date':'2021-08-05','release_date_disagreement_preserved':'NBA/WAS/Nets completed release2021-08-06','future_pick_selector_clause_recovered':False}
 return repository,contracts,raw,observations,pages,lalpage

def bkn_roster_states():
 current=list(CORE_BKN)+['DeAndre Jordan'];states=[]
 events=[('2021-08-06','S_AND_T_OUT_DINWIDDIE',None),('2021-08-07','NEW_ROOKIE_RSC','Cameron Thomas'),('2021-08-08','NEW_BIRD_ONE_YEAR','Bruce Brown'),('2021-08-09','NEW_MINIMUM','Blake Griffin'),('2021-08-10','NEW_TAXPAYER_MLE','Patty Mills'),('2021-08-11','NEW_MINIMUM',"DeAndre\u0027 Bembry"),('2021-09-03','NEW_MINIMUM','LaMarcus Aldridge'),('2021-09-04','JORDAN_JOINT_TRANSFER',None)]
 for day,typ,player in events:
  if player:current.append(player)
  if typ=='JORDAN_JOINT_TRANSFER':current.remove('DeAndre Jordan');current+=['Sekou Doumbouya','Jahlil Okafor']
  states.append({'date_hypothesis':day,'event':typ,'standard':list(current),'two_way':[],'STD_count':len(current),'TW_count':0,'cash_paid_cumulative_before_Jordan':0,'actual_signing_or_registration':False})
 return states

def assert_bkn_states(states):
 expected=list(FIXED_CORE_BKN)+['DeAndre Jordan']
 names=[None,'Cameron Thomas','Bruce Brown','Blake Griffin','Patty Mills',"DeAndre\u0027 Bembry",'LaMarcus Aldridge',None]
 dates=['2021-08-06','2021-08-07','2021-08-08','2021-08-09','2021-08-10','2021-08-11','2021-09-03','2021-09-04']
 events=['S_AND_T_OUT_DINWIDDIE','NEW_ROOKIE_RSC','NEW_BIRD_ONE_YEAR','NEW_MINIMUM','NEW_TAXPAYER_MLE','NEW_MINIMUM','NEW_MINIMUM','JORDAN_JOINT_TRANSFER']
 assert len(states)==8
 for i,(r,n,day)in enumerate(zip(states,names,dates)):
  assert r['event']==events[i],'Returned BKN exception/event route differs'
  if n:expected.append(n)
  if i==7:expected.remove('DeAndre Jordan');expected+=['Sekou Doumbouya','Jahlil Okafor']
  assert r['standard']==expected and r['date_hypothesis']==day and r['STD_count']==len(expected),'Returned BKN named dated roster differs'
  assert len(set(expected))==len(expected)<=15 and r['two_way']==[]and r['TW_count']==0
  assert r['cash_paid_cumulative_before_Jordan']==0 and r['actual_signing_or_registration']is False,'Candidate cash/authority moved'
 assert states[-2]['STD_count']==14 and states[-1]['STD_count']==15
 assert 'Landry Shamet'in expected and 'Alize Johnson'in expected
 assert not any(n in expected for n in ['Jevon Carter','Day\u0027Ron Sharpe','Isaiah Jackson','Chandler Hutchison','James Johnson','Paul Millsap'])

def transition_cells(contracts):
 was_old=sum(contracts[n]['apron_all_performance_component']for n in CORE_WAS)
 lal=sum(contracts[n]['normal_cap_component']for n in LAL_OUT)
 assert was_old==121460108 and lal==35759762
 tpe=44211146-lal;assert tpe==8451384
 # Year1 upper offers remain callable parameters, not exact original salaries.
 closing_fixed=was_old-44211146+lal+1517981+4000000+2500000+5000000
 assert closing_fixed==126026705
 rows=[]
 for X,r in itertools.product([0,5000000,8523911],[3000000,tpe]):
  total=closing_fixed+X+r
  if total>143002000:continue
  rows.append({'WAS_public_residual_X':X,'new_Dinwiddie_first_salary_r':r,'WAS_closing_apron_upper':total,'apron_margin':143002000-total,'E1_TPE_created':tpe,'E2_r_consumption':r,'remaining_TPE_valid_written_renunciation':tpe-r,'WAS_final_STD':15,'actual_ledger_or_chosen_salary':False})
 return rows

def build():
 p=policy();assert p==FIXED_POLICY,'Candidate policy/authority changed'
 s,c,raw,obs,pages,lalpage=read_sources()
 rr=bkn_roster_states();assert_bkn_states(rr)
 cells=transition_cells(c)
 for r in cells:
  assert 0<=r['WAS_public_residual_X']<=13975295 and 3000000<=r['new_Dinwiddie_first_salary_r']<=8451384
  assert r['WAS_closing_apron_upper']==126026705+r['WAS_public_residual_X']+r['new_Dinwiddie_first_salary_r']
  assert r['E1_TPE_created']==8451384 and r['E2_r_consumption']==r['new_Dinwiddie_first_salary_r'] and r['remaining_TPE_valid_written_renunciation']==8451384-r['E2_r_consumption']
  assert r['apron_margin']==143002000-r['WAS_closing_apron_upper']>=0 and r['actual_ledger_or_chosen_salary']is False
 bnormal=sum(c[n]['normal_cap_component']for n in list(CORE_BKN)+['DeAndre Jordan'])
 bapron=sum(c[n]['apron_all_performance_component']for n in list(CORE_BKN)+['DeAndre Jordan'])
 assert bapron-bnormal==1187500 and bnormal>143002000
 new_upper=3000000+5000000+5890000+3*2650000
 pre=bapron+new_upper+3*2650000 # includes allthree unaccepted secondRT overreserve; no STD addition
 post=pre-4137895
 lal_limit=Fraction(35759762*5,4)+100000
 was_limit=Fraction(44211146*5,4)+100000
 assert lal_limit>=44211146 and was_limit>=35759762
 # Demonstrate condition geometry, not a source upper bound on X.
 x_all_r=143002000-126026705-8451384;x_exists_r=143002000-126026705-3000000
 assert (x_all_r,x_exists_r)==(8523911,13975295)
 was_final=[n for n in CORE_WAS if n!='Russell Westbrook']+list(LAL_OUT)+['Gary Trent Jr.','Spencer Dinwiddie','Corey Kispert','Jared Butler']
 assert len(was_final)==len(set(was_final))==15 and 'Troy Brown Jr.'in was_final and 'Gary Trent Jr.'in was_final
 assert 'Caleb Homesley'not in was_final and c['Caleb Homesley']['normal_cap_component']==1517981
 return {'id':'BKN_WAS_2021_PRE_JORDAN_NAMED_EXECUTION_FAMILY','status':'INDEPENDENTLY_REVIEWED_CONDITIONAL_PREFIX_WITH_NAMED_WAS_RIGHTS_COST_GAPS','baseline_main':BASELINE,
  'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'Repo BOMstrip LF, external raw bytes, attributed observation captures not provider raw HTML',
  'policy':p,'external_raw_attempts':raw,'primary_web_observation_captures':obs,'CBA':{'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(CBA),'raw_sha256':CBA_SHA,'PDF1based_text_LF_sha256':pages},'additional_LAL_official_guide':{**LAL_GUIDE,**lalpage},'source_contract_rows':c,
  'facts_inferences_candidates':{'facts':['Official completed original Aug6 exchange and current Nets named2024/2025 claims are positive anchors, not alternate-world acceptance.','SS reported salary rows are secondary templates, not original private contracts.'], 'inferences':['BKN core normal salaries already exceed apron; its valid TaxpayerMLE/minimum/Bird/RSC route has no new hardcap trigger.','Original fiveway cannot be copied because approved Hutchison GSW/MIN/NY path and proposed22/31/43 identities differ.'], 'candidates':['P1 below remains unselected. New Brown/Trent/Dinwiddie/rookie/FA offers and omissions require party agreement; no chosen exact cents.']},
  'BKN':{'dated_roster_states':rr,'core_normal':bnormal,'core_apron_all_performance':bapron,'retained_unlikely_preserved':1187500,'retained_KD_likely':1100000,'retained_Kyrie_likely':412500,'new_UPC_fullcash_upper':new_upper,'three_second_required_tenders_overreserve':7950000,'dated_pre_Jordan_apron_function':{'constant':pre,'residual_symbol':'X_BKN_legacy_current_owed_ge0','actual_residual':None},'dated_post_Jordan_apron_function':{'constant':post,'same_residual_symbol':True,'delta':-4137895},'whole_public_cost_upper':None,'unused_exceptions_normal_before_renunciation':None,'negative_apron_is_illegal':False,
   'six_categories':[{'id':'CURRENT_AND_NEW','scope':'Eight live retained plus six lawful proposed UPCs; actual oldlikely/unlikely preserved; newminbonus0 proposal.'},{'id':'PAST_DEAD_CAMP','scope':'X_BKN retains allcurrent earned/protected ordinarydead,camp,priorstretch/settlement liabilities; nozero/privateabsence claimed. Source-supported namedlegacy inventory not yet completed.'},{'id':'FA_HOLDS','scope':'Expired JeffGreen/TylerJohnson/TLC/MikeJames and oldTW holds valid writtenrenounce afterexpiry; Bruce/Blake replace bysignedproposals, Dinwiddie validoptionnonexercise then S&T; noold debt deleted.'},{'id':'DRAFT_AND_TENDER','scope':'BKN27Thomas candidateRSC 80–120%;43Todd/51Zegarowski/59Gray retained rights, applicabletimelyRT unaccepted wholecash7950000 overreserve; noCarter29/Sharpe autoassignment.'},{'id':'ROSTER_INCOMPLETE','scope':'14STD0TW preJordan/15STD0TW post; no incomplete-roster charge (<12) and no unsignedplayer treatedasregistered.'},{'id':'EXCEPTIONS','scope':'Patty candidateTaxpayerMLE5890000 with2year5%schedule. NoNTMLE/BAE orincomingS&Ttrigger. Otherunusedexceptions/newDinTPE validwrittenrenounce beforeaftercomparison; actualusage0notcert.'}],
   'conditional_exception_route_supported':True,'all_six_category_scalar_cost_closed':False,'actual_registration':False},
  'P1_two_atomic_events':[{'id':'E1_LAL_WAS','date_hypothesis':'2021-08-06_BEFORE_E2','players':{'LAL_to_WAS':list(LAL_OUT),'WAS_to_LAL':['Russell Westbrook']},'rights':{'LAL22_JaredButler_unsigned_to_WAS':True,'WAS_to_LAL_named_2023_2024_2028_original_claims':'Unselected preserved condition-bearing objects; exact2023 origin and2024 complement require explicitreview beforefulladoption.'},'LAL_outgoing':35759762,'LAL_incoming':44211146,'LAL_any_tax_minimum_matching_limit':str(lal_limit),'WAS_outgoing':44211146,'WAS_incoming':35759762,'WAS_any_tax_minimum_matching_limit':str(was_limit),'new_WAS_TPE':8451384,'rights_transfer_before_rookie_UPC_30daybar_not_triggered':True},
   {'id':'E2_BKN_WAS_SAS','date_hypothesis':'2021-08-06_AFTER_E1','BKN_to_WAS':'Spencer Dinwiddie new3seasonS&T','WAS_to_BKN':['OriginalmoreMEM/WAS2024claim','OriginalGSW/WAS2025swap'],'SAS_to_BKN':'Nikola Milutinov unsigned2015rights','WAS_to_SAS':'Originalnamed2022secondclaimwithallpriorconditions','Hutchison_transferred':False,'IND_AaronHoliday_Todd31_cash_leg_imported':False,'BKN_incoming_player_salary':0,'SAS_incoming_player_salary':0,'WAS_TPE_consumption_salary_r_domain':'[3000000,min(8451384,16975295-X_WAS)]','WAS_new_apron_hardcap':143002000,'BYC_outgoing_credit':'ifnewr>1.2*11454048 thenmax(11454048,r/2),else r; incomingBKNplayer0so nocapacityobstruction','new_TPE_remaining_renounce_only_AFTER_use':True,'initialS_and_T_exception_toFA3mo_Dec15_bar':True,'all_contract_parties_acceptance':None}],
  'WAS':{'nine_retained_original_apron':121460108,'published_Deni_likely_preserved':425000,'Troy_Brown_year4_option_reported_applied':5170564,'Homesley_waiver_full_2021_charge_reserved':1517981,'Homesley_NBA_signing_deleted_from_history':False,'new_Trent_offer_upper_NOT_realTOR_contract':5000000,'Corey12_rookie_firstupper':4000000,'Butler22_rookie_firstupper':2500000,'rookie_uppers_are_conditional_applicable_scale_functions_not_primary_exactcents':True,'closing_fixed_without_Din_or_residual':126026705,'unresolved_public_residual_X':None,'all_r_lawful_if_source_X_le':x_all_r,'some_r_lawful_if_source_X_le':x_exists_r,'example_parameter_cells':cells,'examples_are_source_X_upper_certificate':False,'modeled_final_standard':was_final,'modeled_final_two_way':[],'unsigned_Bonga_after_SubsequentDraft_window_status':None,'new_CAPyear_Neto_Lopez_Len_extraUPC_imported':False,'whole_cost_family_complete':False},
  'cash_prefix':{'BKN_paid_before_Jordan_candidate':0,'WAS_paid_to_SAS_candidate':0,'actual_paid_or_received_certified':False,'BKN_tradecash_usage_from_new_FAs_or_salaries':False,'Sep4_joint_previous_BKN_paid_upper':5000,'guard_satisfied_with_this_named_prefix':True,'any_new_cash_event_reopens_prefix':True},
  'changed_world_exclusions':[{'actor':'Chandler Hutchison','reason':'ReviewedGSW28/MIN/NYwaiver route; neverWAS-owned in thiscandidate.'},{'actor':'Isaiah Jackson22','reason':'Current22JaredButlerLAL, nothistoricalJacksonIND.'},{'actor':'Isaiah Todd31','reason':'Current31KaiJonesMIL;Todd43BKN remainsunassigned.'},{'actor':'Jevon Carter/Day\u0027Ron Sharpe','reason':'Shamettrade is unselected; currentBKNShamet retained; neitherautoregistered.'}],
  'remaining_named_gaps':[{'id':'WAS_PUBLIC_RESIDUAL_X','next':'Enumerateknownpastdead/camp/formerordinaryendpoints/FAorRTcharges andretainedperformance toshow X<=8523911 orfinite r-interval. Actualprivateallledgerreceipt isnotneeded. NoX=0guess.'},{'id':'LAL_WAS_2024_COUPLED_RIGHT','next':'PositiveBKNmoreMEM/WASclaim retained; LAL same-yearclaimmustpreservecomplement/priorpriority, notunconditionalWAS2024twice. ExactprimaryLALselector notyetrecovered fromguide; mayconstructexplicitlawfulnewcandidate butnotcall ithistoricalfact.'},{'id':'LAL2023_CURRENT_NAMED_ORIGIN','next':'WASofficialcompletionlists2023/24/28; prereportlists24/28. Preserve source disagreement andmatch currentCHI2023/WASnamedsource beforeownerassignment.'},{'id':'BKN_PUBLIC_LEGACY_SCALAR','next':'Exception/rosterfamily works foranyfinite carriedlegacy X withoutnewhardcap; explicitpublicnamedcostinventoryremainsunclosed. Costnonincreasealone isnot wholeledgercert.'},{'id':'P1_CONSEQUENTIAL_DIRECTION','next':'Westbrook/#22branch, newoffers/INDlegomission remaincomparisoncandidates, notroot/userauthorlocks. Othercounterpartyacceptanceunselected.'}],
  'certification':{'independent_review_completed':True,'whole_BKN_prior_cost':False,'whole_changed_fiveway_legal':False,'current_rights_family_fully_adopted':False,'actual_private_ledger_or_acceptance':False,'actual_opening_rosters_or_2021_22_results':False,'new_author_lock':False,'whole_macro3_complete':False,'REGISTER_changed':False,'manuscript_written':0}}

def validate(o):
 try:assert o==build(),'Saved prefix differs from sources/current constructed family';return[]
 except(AssertionError,KeyError,ValueError,OSError)as e:return[str(e)]
def markdown(o):
 b=o['BKN'];w=o['WAS']
 return '\n'.join(['# BKN/WAS: Jordan 이전의 명명 실행 후보','',o['status'],'',
 '독립 검문: chi가 raw36/DOM22 명명 계약행·필요 CBA본문·8명단/6비용셀을 직접 대조했고, 같은 Patty/날짜/명단의 TMLE→NTMLE 반환변조를 caller가 거부함을 회수했다. 작성자 자체4건은 독립 검문으로 계수하지 않는다. 전체 비용/권리/중요 방향은 미완 상태다.','', '## 실제 완료한 구성과 한계','',
 '새36개 HTTP 응답의 원바이트를 보존했다. HTTP200이라도 Player not found인6개 응답은 계약 본문으로 채택하지 않았다. 올바른 URL의 보고 계약행과 성과 성분을 파싱했다. 원문은 vendor 계약 보고이며 실제 비공개 계약 인증은 아니다. NBA indexed 본문4개는 attribution capture로 보존하고 raw HTML이라고 부르지 않는다. 새 Lakers 공식2022–23 guide도 받았으나 PDF96은8/5 거래일만 적고 정확2024 비교권을 제공하지 않았다. 구단8/6 발표일과 혼동하지 않는다.','',
 '## BKN의 실제 날짜별 명단·비용 함수','',
 '보존8명에 Thomas27 RSC, Brown Bird, Griffin/Bembry/Aldridge 법정 최소, Mills TMLE를 추가하는 여덟 상태를 실제 구성했다. Sep3 14STD0TW → Sep4 Jordan 양도/두 선수 수취 후15STD0TW다. Shamet와 Alize를 유지하며 Carter/Sharpe/JamesJohnson/Millsap를 자동 추가하지 않는다. 이 명단은 새로운 작업 비교 후보이며 원역사 계약 체결 또는 개막 등록이 아니다.','',
 f'보존8명의 normal {b["core_normal"]:,}, 모든 보고 성과를 포함한 apron {b["core_apron_all_performance"]:,}. Kyrie/Harris unlikely1,187,500 및 KD/Kyrie likely 성분을 삭제하지 않는다. 제안UPC 상단과 미수락2R tender3개의 fullcash 과대예약을 더하면 Sep3 {b["dated_pre_Jordan_apron_function"]["constant"]:,}+X_BKN → Sep4 {b["dated_post_Jordan_apron_function"]["constant"]:,}+X_BKN다. X_BKN은 과거 지급·방출·캠프 채무를 보존하는 미완 입력이다. 큰 비용이나 음수apron이 새 hardcap 없는 팀의 위법 증거는 아니다.','',
 '기존 core만 apron보다 높으므로 Patty의5.89m TMLE·3년 이상 유지된 Brown의 Bird·법정 최소·rookie 예외를 사용하는 후보 경로를 지지한다. Dinwiddie를 S&T로 송출하는 것은 수취 hardcap을 BKN에 만들지 않는다. unused예외/새 TPE는 유효 서면정리 이후 비교하며 원래 없었다거나 지급0이었다고 가정하지 않는다. whole BKN 과거 원장 상단은 아직 닫히지 않았다.','',
 '## 두 원자 사건으로 비교한 P1','',
 '원역사 fiveway에서 Hutchison은 현재 GSW/MIN/NY 경로와 충돌하고, #22는 Jared Butler(LAL), #31은 Kai Jones(MIL), Todd는 #43(BKN)다. IND의 Holiday/Todd31/현금 leg를 그대로 복사하지 않는다. 먼저 LAL–WAS 일반거래를 비교한다: LAL35,759,762 송출·44,211,146 수취는125%+100k 한계44,799,702.5 이내이며 WAS는44,211,146 송출·35,759,762 수취다. 미서명 Butler22 권리는 WAS로 가는 후보라 새 rookiesigned30일 제한을 만들지 않는다.','',
 '다음 별도 BKN/WAS/SAS 비교에서 새3시즌 Dinwiddie S&T, 원Nets2024 비교권/2025swap 및 Milutinov 권리를 운반한다. WAS는 앞 사건의8,451,384 TPE 중 r≤8,451,384를 사용하며 남은 예외는 사용 후 정리한다. 새 r는3m 이상 합의 함수이고 원17.142857m+2.571428m 성과를 사실 또는 계약으로 복사하지 않는다. BKN/SAS에는 incoming UPC가0이라 BYC/outgoingbonus 조건을 희생해 matching을 꾸밀 필요가 없다. 원 tradebonus가 있으면 적법한 fullwaiver 후보와 후손 max(2022-02-06,otherwiseeligible) 제한을 함께 보존한다.','',
 f'WAS에서 Troy5,170,564·Trent 새제안≤5m를 보존했다. Homesley는 신인 추가 전에 waiver하는 비교지만 원현재1,517,981을 전액 비용 예약했다. 두 rookie 함수 상단4m/2.5m는 해당 실제scale 80–120% 범위가 이 상단에 포함되는 후보 조건이며 정확 공식 cents 인증이 아니다. 최종15STD0TW 목록을 구성했다. closing 비용은126,026,705+X_WAS+r이고, 모든 r∈[3m,8,451,384]에 대해 X≤8,523,911이면 apron143,002,000 이내다. 일부 r의 비공허함은 X≤13,975,295로 표현된다. 실제 예시셀{len(w["example_parameter_cells"])}개를 검산했으나 이것이 X의 원자료 상단 증거는 아니다.','',
 '## 권리·현금의 정확한 남은 입력','',
 'BKN은 새 UPC 급여를 팀 간 tradecash로 합산하지 않는다. 이 후보 선행 사건에는 BKN 지급 현금이 없으므로 Sep4 이전 지급≤5,000 충분조건을 만족한다. 이는 실제 장부의0 인증이 아니다. 새 현금 사건을 채택하면 prefix를 재계산한다.','',
 '[Wizards8/6](https://www.nba.com/wizards/washington-acquires-six-players-five-team-trade)은 LAL2023/24/28을 명명하지만 [NBA7/30 최초 보도](https://www.nba.com/news/numbers-to-know-breaking-down-the-big-draft-week-trades)는24/28만 적었다. 정확 현재2023 원권리와2024의 반대편 비교권은 아직 새전이를 닫는 입력이다. [Nets8/6](https://www.nba.com/nets/news/2021/08/06/brooklyn-nets-acquire-future-draft-considerations-five-team-trade)의 more MEM/WAS2024를 보존하면서 LAL에도 unconditional WAS2024를 줘서는 안 된다. 원문 부족을0으로 채우지 않았다. [Spurs8/6](https://www.nba.com/spurs/spurs-complete-trade)의 Milutinov/2022/Hutchison 원사건에서 Hutchison만 바뀐 것을 숨기지 않는다.','',
 '다음 국소 작업은 WAS 공개 residual 원장 상단과 LAL 두 명명권리의 현재 포트폴리오를 연결하는 것이다. 새 중요 Westbrook/IND/Butler 방향·새 협상은 미선택 비교이며, 원actual접수·모든private조항 무존재 인증을 새 gate로 요구하지 않는다. 기존 건강·승패·제목·이적 승인·원고는 변경0이다.','',
 '[DET/BKN 수용된 국소 전이](DETROIT_BROOKLYN_2021_JORDAN_JOINT_TRADE_FAMILY_2026_10_07.md) · [현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','',
 '|번호|묶음|상태|','|---|---|---|','|1|2020드래프트 연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23거래·계약|BKN14→15/WAS15 날짜·비용함수 후보; residual·공동권리·방향 미완|','|4|장기커리어|후속시즌대기|','|5|결말·전체구조|전체기능표 미완료|','|6|집필규격·ContextPack|현행 등록기·Pack0|','|7|통합·독립·작가승인|최종 CLOSED|','','미완료 큰 묶음5 / v0.30 PARTIAL / 설계·원고 CLOSED / 원고0.',''])

def self_test():
 count=0
 orig=bkn_roster_states
 def badroster():
  r=orig();r[-2]['standard'][0]='Jevon Carter';return r
 with patch(__name__+'.bkn_roster_states',side_effect=badroster):
  try:build();raise RuntimeError('FALSE_PASS same_count_wrong_actor')
  except AssertionError:count+=1
 old=transition_cells
 def badbudget(c):
  r=old(c);r[0]['WAS_closing_apron_upper']-=1000000;return r
 with patch(__name__+'.transition_cells',side_effect=badbudget):
  try:build();raise RuntimeError('FALSE_PASS returned_budget_hidden')
  except AssertionError:count+=1
 bad=copy.deepcopy(CORE_BKN);x=list(bad['Kyrie Irving']);x[-1]=0;bad['Kyrie Irving']=tuple(x)
 with patch(__name__+'.CORE_BKN',bad):
  try:build();raise RuntimeError('FALSE_PASS unlikely_deleted')
  except AssertionError:count+=1
 def bad_event():
  r=orig();r[4]['event']='NEW_NON_TAXPAYER_MLE';return r
 with patch(__name__+'.bkn_roster_states',side_effect=bad_event):
  try:build();raise RuntimeError('FALSE_PASS returned_exception_route')
  except AssertionError:count+=1
 return count
PINS={'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2',
 'research/CHA_WAS_FINITE_ROSTER_WORKING_FAMILY_2026_10_07.json': 'b06b071a0bf77bbff05d01d8adfa62472b4c3b90cca8aa2373ced9034712899a',
 'research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json': '7244beff7a120c5ca246a04e72b61586f3cfbe245487d5fc6479f5245fd78d9f',
 'research/DETROIT_BROOKLYN_2021_JORDAN_JOINT_TRADE_FAMILY_2026_10_07.json': '747fd807624c4e84242f8e8b3cc5935abe1133085dff3f7e3294eddb8bc1ea7a',
 'research/EAST_2021_PLAYOFF_COACH_INPUTS_2026_10_07.json': 'ee9e61621fbe908722b772cf53e1c1f49ca6f3c83563aaa0ea4e8448c8f88992',
 'research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json': '90099928f9133c4087ee7871939ce58216d183bd186f5ebd3575a56c2348eeed',
 'simulation/2021_WASHINGTON_CHICAGO_PORTLAND_TRANSACTION_CASCADE.md': '70c7b3b944cd745496e940a9336ac521513002fe2c170ad0782aeb626ed8fa37',
 'simulation/GSW_G1_OPTION3_NY_WORKING_EXECUTION.json': '05933c0d976e9854c9b1bae4d5c36e7f4b50f05010940bb43f516a6157cd822f',
 'simulation/NBA_2020_21_APPROVED_TRANSACTION_EXECUTION_BRIDGE.json': '51755e614cd9827c7f60c0c07ef75851f1b20cdfdfb13348db7c512e84dcb968',
 'simulation/NBA_2021_ASSET_CHAIN.json': '3c39c7baa777f70423394181b1a92870146a32db36c60a67f32ec75319c74c5e',
 'tools/build_detroit_brooklyn_2021_jordan_joint_trade_family.py': '936e9685f361e147a0dc4d98b9986ac3fcf2d46ffabe7b1fd9df7c716c9d1f2c'}
RAW=[{'bytes': 141470,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\russell-westbrook.html',
  'final_url': 'https://www.salaryswish.com/players/russell-westbrook',
  'id': 'russell-westbrook',
  'raw_sha256': '54a5f9013e71de97bd2e469cc7278a5db183b22a94a8f671ec60135eea3e8b8f',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/russell-westbrook'},
 {'bytes': 81159,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\kentavious-caldwell-pope.html',
  'final_url': 'https://www.salaryswish.com/players/kentavious-caldwell-pope',
  'id': 'kentavious-caldwell-pope',
  'raw_sha256': '24413809092f83d4adce46cd308d216b021a945c43998291aa4ca3c8e09e15b5',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/kentavious-caldwell-pope'},
 {'bytes': 106373,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\kyle-kuzma.html',
  'final_url': 'https://www.salaryswish.com/players/kyle-kuzma',
  'id': 'kyle-kuzma',
  'raw_sha256': 'c8202d3d6f782eb17b7749e7d4a27d98e4a653fd214afaa7808ff0e9ceb79b4e',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/kyle-kuzma'},
 {'bytes': 117748,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\montrezl-harrell.html',
  'final_url': 'https://www.salaryswish.com/players/montrezl-harrell',
  'id': 'montrezl-harrell',
  'raw_sha256': 'e07b3062d4001406884f4b26b359731c763cb945dcb0bb8b4746a4d27320e923',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/montrezl-harrell'},
 {'bytes': 130433,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\bradley-beal.html',
  'final_url': 'https://www.salaryswish.com/players/bradley-beal',
  'id': 'bradley-beal',
  'raw_sha256': 'd8ee7bd94a418bdb029902e4c746abaa6453d0797324d930c33ab9b7549c8ba9',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/bradley-beal'},
 {'bytes': 106461,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\davis-bertans.html',
  'final_url': 'https://www.salaryswish.com/players/davis-bertans',
  'id': 'davis-bertans',
  'raw_sha256': 'be3f794e24e189cdcde49b53d993cc14d28c6d000b614ff73d43720cb53c83ea',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/davis-bertans'},
 {'bytes': 127622,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\thomas-bryant.html',
  'final_url': 'https://www.salaryswish.com/players/thomas-bryant',
  'id': 'thomas-bryant',
  'raw_sha256': 'defd1646905284e3b29106f7d6609c17ef02c5d55c91716bf4e4aaac61494f05',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/thomas-bryant'},
 {'bytes': 106031,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\rui-hachimura.html',
  'final_url': 'https://www.salaryswish.com/players/rui-hachimura',
  'id': 'rui-hachimura',
  'raw_sha256': '8b5eac9f36a2c2709b84ba9d5108a0db52cf0858bbd5b82cf3208421c882d43b',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/rui-hachimura'},
 {'bytes': 100078,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\deni-avdija.html',
  'final_url': 'https://www.salaryswish.com/players/deni-avdija',
  'id': 'deni-avdija',
  'raw_sha256': '752fbd761a2d1c95db5f7e0d91becb67c2ad88cfe9c1c52ab6b457e8aa7b2fe7',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/deni-avdija'},
 {'bytes': 104747,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\daniel-gafford.html',
  'final_url': 'https://www.salaryswish.com/players/daniel-gafford',
  'id': 'daniel-gafford',
  'raw_sha256': 'e03bfd35c6ab29f7f4e1152fdd60d84cb5d25ceacdd30a1bfe26206a61aee72d',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/daniel-gafford'},
 {'bytes': 81159,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\troy-brown.html',
  'final_url': 'https://www.salaryswish.com/players/troy-brown',
  'id': 'troy-brown',
  'raw_sha256': '24413809092f83d4adce46cd308d216b021a945c43998291aa4ca3c8e09e15b5',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/troy-brown'},
 {'bytes': 117297,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\anthony-gill.html',
  'final_url': 'https://www.salaryswish.com/players/anthony-gill',
  'id': 'anthony-gill',
  'raw_sha256': '309924a41f025bfec7f43c043df71393aff8163ff6dff8f40e9be9858bb8ba63',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/anthony-gill'},
 {'bytes': 81159,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\gary-trent.html',
  'final_url': 'https://www.salaryswish.com/players/gary-trent',
  'id': 'gary-trent',
  'raw_sha256': '24413809092f83d4adce46cd308d216b021a945c43998291aa4ca3c8e09e15b5',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/gary-trent'},
 {'bytes': 137936,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\kevin-durant.html',
  'final_url': 'https://www.salaryswish.com/players/kevin-durant',
  'id': 'kevin-durant',
  'raw_sha256': '41703f4388a6ef3d1fd1ab8cfdbbf39305285246824b7f64e5be959ee10e1d95',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/kevin-durant'},
 {'bytes': 120718,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\kyrie-irving.html',
  'final_url': 'https://www.salaryswish.com/players/kyrie-irving',
  'id': 'kyrie-irving',
  'raw_sha256': 'cabc35820a7f924c3f6724cdfde782147a693f77487cf8eecffa9dd8f1b5a568',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/kyrie-irving'},
 {'bytes': 140165,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\james-harden.html',
  'final_url': 'https://www.salaryswish.com/players/james-harden',
  'id': 'james-harden',
  'raw_sha256': '8a051c7aa2741faa9dbac138cc612c6e8e56010b62c1812cb0f8ad8cf26bbb32',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/james-harden'},
 {'bytes': 113038,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\joe-harris.html',
  'final_url': 'https://www.salaryswish.com/players/joe-harris',
  'id': 'joe-harris',
  'raw_sha256': 'd7c73608ec43c0a5e739c19ae9678faefaa2f70e9393b0d5d3a27a9dd756fadb',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/joe-harris'},
 {'bytes': 105714,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\nicolas-claxton.html',
  'final_url': 'https://www.salaryswish.com/players/nicolas-claxton',
  'id': 'nicolas-claxton',
  'raw_sha256': '4722cf6a5ee6a68dc918210c81db5580064f47674a33fc80b0fd0803107fee1b',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/nicolas-claxton'},
 {'bytes': 126413,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\landry-shamet.html',
  'final_url': 'https://www.salaryswish.com/players/landry-shamet',
  'id': 'landry-shamet',
  'raw_sha256': '3c179db7761a676964bca2dc2c4ec92946ab853d963c46d421e8aa0894bd2632',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/landry-shamet'},
 {'bytes': 81159,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\bruce-brown.html',
  'final_url': 'https://www.salaryswish.com/players/bruce-brown',
  'id': 'bruce-brown',
  'raw_sha256': '24413809092f83d4adce46cd308d216b021a945c43998291aa4ca3c8e09e15b5',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/bruce-brown'},
 {'bytes': 160583,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\alize-johnson.html',
  'final_url': 'https://www.salaryswish.com/players/alize-johnson',
  'id': 'alize-johnson',
  'raw_sha256': 'd8699304970a48201efaa2a3f3bf2239982a93250f39452624425fe4a84f2efb',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/alize-johnson'},
 {'bytes': 160770,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\jeff-green.html',
  'final_url': 'https://www.salaryswish.com/players/jeff-green',
  'id': 'jeff-green',
  'raw_sha256': '14599467ae47062c10bc0b090f7b31c2ae472584bea96167b80c22541d083ee8',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/jeff-green'},
 {'bytes': 120114,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\mike-james.html',
  'final_url': 'https://www.salaryswish.com/players/mike-james',
  'id': 'mike-james',
  'raw_sha256': '0daaa80eecfcf5efcb6c3d339b7bbb9e7d9f5f5b9b1fafb77ff46fc52ad37eb6',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/mike-james'},
 {'bytes': 81159,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\timothe-luwawu-cabarrot.html',
  'final_url': 'https://www.salaryswish.com/players/timothe-luwawu-cabarrot',
  'id': 'timothe-luwawu-cabarrot',
  'raw_sha256': '24413809092f83d4adce46cd308d216b021a945c43998291aa4ca3c8e09e15b5',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/timothe-luwawu-cabarrot'},
 {'bytes': 139570,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\tyler-johnson.html',
  'final_url': 'https://www.salaryswish.com/players/tyler-johnson',
  'id': 'tyler-johnson',
  'raw_sha256': '94011f8592e70fcd69d5fec134ca09cf546981451acfebae7bf4a559cbbfbcbc',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/tyler-johnson'},
 {'bytes': 136757,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\kentavious-caldwellpope.html',
  'final_url': 'https://www.salaryswish.com/players/kentavious-caldwellpope',
  'id': 'kentavious-caldwellpope',
  'raw_sha256': '99f9c1a22d1bbd844e3149c33b91253d5fb9448b2e927a8b0c608ac525ffe364',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/kentavious-caldwellpope'},
 {'bytes': 105790,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\troy-brownjr.html',
  'final_url': 'https://www.salaryswish.com/players/troy-brownjr',
  'id': 'troy-brownjr',
  'raw_sha256': 'f4576363be13b1b8fe9058d12239a6cc8e3afa3177a42fb7e65db5be59ddb277',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/troy-brownjr'},
 {'bytes': 116960,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\gary-trentjr.html',
  'final_url': 'https://www.salaryswish.com/players/gary-trentjr',
  'id': 'gary-trentjr',
  'raw_sha256': 'c0b9549cf236d294f258f667241fcadefd4d830b604b3173f1790d80a7527c82',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/gary-trentjr'},
 {'bytes': 81159,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\bruce-brownjr.html',
  'final_url': 'https://www.salaryswish.com/players/bruce-brownjr',
  'id': 'bruce-brownjr',
  'raw_sha256': '24413809092f83d4adce46cd308d216b021a945c43998291aa4ca3c8e09e15b5',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/bruce-brownjr'},
 {'bytes': 132518,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\timothe-luwawucabarrot.html',
  'final_url': 'https://www.salaryswish.com/players/timothe-luwawucabarrot',
  'id': 'timothe-luwawucabarrot',
  'raw_sha256': '6cc65d897011fe43a69d6d4c55df1d6f37439937629c03d07f384fd2e0ab4e3a',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/timothe-luwawucabarrot'},
 {'bytes': 138262,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\spencer-dinwiddie.html',
  'final_url': 'https://www.salaryswish.com/players/spencer-dinwiddie',
  'id': 'spencer-dinwiddie',
  'raw_sha256': 'f34ebd9ce56aef575f51e9347a03d79708e153a120feabfbf6cba28d97791158',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/spencer-dinwiddie'},
 {'bytes': 143649,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\patty-mills.html',
  'final_url': 'https://www.salaryswish.com/players/patty-mills',
  'id': 'patty-mills',
  'raw_sha256': '214e3a0f5482d8c6365c9691f5d1ebf420c1032d9a8af7f779cbbe070c416d1a',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/patty-mills'},
 {'bytes': 125605,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\blake-griffin.html',
  'final_url': 'https://www.salaryswish.com/players/blake-griffin',
  'id': 'blake-griffin',
  'raw_sha256': '38102508aeffa8834030feb0b1f9ffaeca3b7fca6dd9608aae9791ef0062e78b',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/blake-griffin'},
 {'bytes': 114602,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\deandre-bembry.html',
  'final_url': 'https://www.salaryswish.com/players/deandre-bembry',
  'id': 'deandre-bembry',
  'raw_sha256': '5a694d483f8891ccf22fd324eacaa7365a68d61b22d5d1cd06fae7436fea5d5b',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/deandre-bembry'},
 {'bytes': 125937,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\lamarcus-aldridge.html',
  'final_url': 'https://www.salaryswish.com/players/lamarcus-aldridge',
  'id': 'lamarcus-aldridge',
  'raw_sha256': 'f0a979aa19307fd63e87c5d7653f9c54960c0e378c10bde6e2b8001578ad6cec',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/lamarcus-aldridge'},
 {'bytes': 98725,
  'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\caleb-homesley.html',
  'final_url': 'https://www.salaryswish.com/players/caleb-homesley',
  'id': 'caleb-homesley',
  'raw_sha256': '7d0214922bb45f1fc88e1c1966698a317696fb14b84dec467b8d14c0816bae2a',
  'source_tier': 'SECONDARY_CONTRACT_REPORT',
  'status': 200,
  'url': 'https://www.salaryswish.com/players/caleb-homesley'}]
OBS=[{'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\CAM_ORIGINAL_SIGN_observation.json',
  'capture_sha256': '7e6e2a18253da895542562aaefba7255c572a25eb98d639efc5a3aa714830ec0'},
 {'cache_path': 'C:\\Users\\Storm '
                'Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\NBA_JUL30_INITIAL_REPORT_observation.json',
  'capture_sha256': '059ad1c265c358fa23c8a50a0e278948cf796ae69952d82e896c9f8bc8604dae'},
 {'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\SAS_AUG6_observation.json',
  'capture_sha256': '37c409b06c891fa480582f01d7c3e0ae62ffed3e7cf819453e307c3a7bf0fb63'},
 {'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\WAS_AUG6_observation.json',
  'capture_sha256': '7b0cbd82bec449ed9a7e90c341c1fd99ce92e291ce1f2b71e3fcb4d733c02a0c'}]
LAL_GUIDE={'bytes': 16302060,
 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-bkn-was-prefix-20261007\\LAL2223.pdf',
 'final_url': 'https://lalweb.blob.core.windows.net/public/lakers/media-relations/2022-23-Lakers-Media-Guide.pdf',
 'raw_sha256': '8a9b6bd67b067d91150dbb761a50be578d827bde70a068822ad82c5520c96921',
 'status': 200,
 'url': 'https://lalweb.blob.core.windows.net/public/lakers/media-relations/2022-23-Lakers-Media-Guide.pdf'}

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');args=a.parse_args();o=build()
 if args.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
 if args.check:assert not validate(load(OUT));assert text(MD)==markdown(o)
 print(json.dumps({'current':True,'BKN_states':len(o['BKN']['dated_roster_states']),'BKN_pre_STD':o['BKN']['dated_roster_states'][-2]['STD_count'],'BKN_post_STD':o['BKN']['dated_roster_states'][-1]['STD_count'],'WAS_STD':len(o['WAS']['modeled_final_standard']),'WAS_cells':len(o['WAS']['example_parameter_cells']),'whole_prefix':False,'self_controls':self_test()if args.self_test else None}))
