"""Source-bound PS22 candidate pool and complete 60-row working board.

No ancestor constructors; no historical draft-order/transaction import.
"""
import argparse, copy, hashlib, json, re, unicodedata
from datetime import date
from pathlib import Path
from unittest.mock import patch
import fitz

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_full_draft_working_board.py'
OUT='research/NBA_2022_FULL_DRAFT_WORKING_BOARD_2026_10_08.json'
MD=OUT[:-5]+'.md'
DRAW='simulation/NBA_2022_SELECTED_WORKING_DRAW_AND_CONTROL.json'
PRIOR='simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json'
GLOBAL='simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json'
CORE='simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json'
UNSIGNED='research/CHICAGO_2022_UNSIGNED_DRAFT_EXECUTION_FAMILY_2026_10_07.json'
LAW='research/SIMONOVIC_2022_23_SELECTED_RIGHTS_FAMILY_2026_10_07.json'
PINS={DRAW:'09d7c6613b3710a04600f567340e963d3a3d863851bafd1a8213618dee14ea39',PRIOR:'f8c78e99cce1b02a051c94339b550fdb52205d3988db8bbe69b780559c3bc306',GLOBAL:'93264d2dff86a58ad10ca6975315c6c2167961f94f2517b6f5f79fa3113f2af8',CORE:'e7d0f4b15bc06c7cd16a38d158b38a78871fb7372d412639e33bb20c31d225a7',UNSIGNED:'7c2ea95557f96a9156709aabb8574fcaea8993831aed5f2f6cc626be6829bafd',LAW:'c404fc401f6c30809ed5098663dd2b277b1c4cb7844d15c697991460f1290ac4','AGENTS.md':'67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2'}
CACHE=Path.home()/'AppData/Local/Temp/fr-draft2022-board-20261008'
WEB_URLS={'final_web_observation.json':'https://www.nba.com/news/24-early-entry-candidates-withdraw-from-nba-draft-2022','final_tail_web_observation.json':'https://www.nba.com/news/24-early-entry-candidates-withdraw-from-nba-draft-2022','prospects_web_observation.json':'https://www.nba.com/draft/2022/prospects','draftorder_web_observation.json':'https://www.nba.com/news/2022-nba-draft-order','kessler_web_observation.json':'https://www.nba.com/draft/2022/prospects/walker-kessler','ellis_web_observation.json':'https://www.nba.com/draft/2022/prospects/keon-ellis','terry_web_observation.json':'https://www.nba.com/draft/2022/prospects/dalen-terry','koloko_web_observation.json':'https://www.nba.com/draft/2022/prospects/christian-koloko','ignite_web_observation.json':'https://gleague.nba.com/news/marjon-beauchamp-signs-with-nba-g-league-ignite'}
RAW_PINS={'draftorder_web_observation.json': 'e977c12c13aa1d46db93ca404574ff216f0e31742c7f5283358e5a76ecce4363', 'ellis_web_observation.json': '4985a9b75d1ba854f04868ff4b355d6c918407cb1aafbc2df42a5796bfc5513f', 'final_tail_web_observation.json': 'df5cd91a80c16aa553f5010b28d3975de2ca6efd63624e44f0febb2d3f670f8e', 'final_web_observation.json': 'c9c1d58a371fbbfc14b2f69a8acbaca97aeab96527044119670a110faf618b18', 'ignite_web_observation.json': 'bc9adcfd83080ee4f5ba5519c85a9ff38beac85cd7f87280a98bcdb6e39d3dee', 'kessler_web_observation.json': '0d9f098e5fba82eb237da0b0c3b0c6709353464bd7385161b2bffb88ad87352c', 'koloko_web_observation.json': 'ad02b5466ffbfa513475642d751255b65b62b3e8b6b204443806b2b3b82fe9ac', 'prospects_web_observation.json': 'e07945a527711bd0d1ac4646e5abc3b15ca2683ed0bdcaf23ffc800b0b1a8e9c', 'terry_web_observation.json': '5bcd5bc2f022309d1d1623e5a3a5e7e067ecfbaf1064733c619bcfb82c6019c6', 'initial.pdf': '30c19c0b058a5a4fba976bdc73523dbb4b68810572ca98e84723a223ebdb6815', 'sources.json': '2eb515dff7db96e430029cf6d1b075b7a87d76fbafc43e55c2740dde62717744'}
MEANING_PINS={'initial': '19b6f4d996851e3e328063b2dc01a69fbd3022c0daf48c7425b5271eb5534cb0', 'final': 'e94473ff26739f71351a181ed6f7a306b87b7a7f82f2d099013743390c70cd21', 'withdrawn': '8c04002146adb6aafb68abbf8b63d7e661833cf112cd4daac1ba0f8aa505d860', 'prospects': 'a718493beb959bc57e62697d1071685c9a0358faf2d105bfaff5ed05e29e7cdf', 'actual_participant_identity_set': '492e6d18d192c56f2379dbd3513cce8f0ad9032691d5d92939eaf705b4033a95'}
NAMES=('Chet Holmgren','Paolo Banchero','Jabari Smith','Jaden Ivey','Keegan Murray','Bennedict Mathurin','Shaedon Sharpe','Dyson Daniels','Jeremy Sochan','Jalen Duren','Jalen Williams','Ousmane Dieng','Mark Williams','Ochai Agbaji','A.J. Griffin','Tari Eason','Malaki Branham','Walker Kessler','Dalen Terry','Johnny Davis','Nikola Jovic','Christian Braun','Jake LaRavia','MarJon Beauchamp','Wendell Moore Jr.','TyTy Washington Jr.','Christian Koloko','Blake Wesley','Patrick Baldwin Jr.','Peyton Watson','Andrew Nembhard','Caleb Houstan','Kennedy Chandler','Jaylin Williams','Max Christie','Gabriele Procida','David Roddy','Bryce McGowens','Trevor Keels','Moussa Diabate','Ryan Rollins','Josh Minott','Ismael Kamagate','Khalifa Diop','Vince Williams Jr.','Kendall Brown','Isaiah Mobley','JD Davison','Tyrese Martin','Matteo Spagnolo','Karlo Matkovic','Gui Santos','Yannick Nzosa','Luke Travers','Hugo Besson','Jabari Walker','Keon Ellis','Justin Lewis','Jaden Hardy','EJ Liddell')
AUTOMATIC=('Dyson Daniels','MarJon Beauchamp','Jaden Hardy')
POLICY={'board_id':'D22A_KESSLER_ELLIS','draft_date':'2022-06-23','board_selected':False,'NPC58_selected':False,'CHI_choices_selected':False,'new_draft_trades':0,'new_UPCs':0,'new_RequiredTenders':0,'actual_eligibility_papers_certified':False,'actual_medical_certified':False,'new_author_lock':False,'original_2022_order_or_forfeiture_or_trades_inherited':False}

def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def require(v,m):
 if not v:raise ValueError(m)
def key(n):
 s=''.join(x for x in unicodedata.normalize('NFKD',n) if not unicodedata.combining(x))
 return re.sub(r'[^a-z0-9]','',s.lower()).removesuffix('jr')
def physical(root,p):return json.loads(text(root/p))
def sources(root):
 d={}
 for p,h in PINS.items():
  require(sha(root/p)==h,'Source changed '+p)
  if p.endswith('.json'):
   d[p]=physical(root,p);require(d[p]==json.loads(text(root/p)),'Returned source differs from physical '+p)
 require(d[CORE]['summary']['standard']==15 and d[CORE]['summary']['two_way']==2,'Core slots changed')
 require(len(d[PRIOR]['selected_rows'])==60,'Prior selected draft incomplete')
 ranks=d[DRAW]['exact_sixty_rank_and_holder_rows']
 require(len(ranks)==60 and [x['working_exact_rank'] for x in ranks]==list(range(1,61)),'Draw ranks changed')
 require([(x['working_exact_rank'],x['current_public_family_holder']) for x in ranks if x['current_public_family_holder']=='CHI']==[(18,'CHI'),(57,'CHI')],'Chicago entitlement changed')
 return d
def observed(name):return json.loads((CACHE/name).read_text(encoding='utf-8'))
def web_lines(name):
 s=re.sub(r'(?<!\n)(L\d+:)',r'\n\1',observed(name))
 return [(int(a),b) for a,b in re.findall(r'L(\d+): ([^\n]*)',s)]
def public_inputs():
 evidence=[]
 for n,h in RAW_PINS.items():
  raw=(CACHE/n).read_bytes();require(hashlib.sha256(raw).hexdigest()==h,'Raw/capture changed '+n)
  evidence.append({'cache_path':str(CACHE/n),'sha256':h,'bytes':len(raw),'url':WEB_URLS.get(n) or ('https://ak-static.cms.nba.com/wp-content/uploads/sites/46/2022/04/2022-Early-Entry-Candidates.pdf' if n=='initial.pdf' else None),'classification':'SERIALIZED_WEB_TOOL_OBSERVATION_NOT_ORIGINAL_HTML' if n in WEB_URLS else 'RAW_HTTP_METADATA' if n=='sources.json' else 'ORIGINAL_OFFICIAL_PDF'})
 pdf=fitz.open(CACHE/'initial.pdf');initial=[]
 for p,pg in enumerate(pdf,1):
  ls=[x.strip() for x in pg.get_text().splitlines() if x.strip()]
  for i,v in enumerate(ls):
   if re.fullmatch(r'\d+-\d+',v) and i>=2 and i+1<len(ls):initial.append({'name':ls[i-2],'school_or_club':ls[i-1],'height':v,'status':ls[i+1],'PDF_1based':p})
 require(len(initial)==283 and sum('DOB' in r['status'] for r in initial)==36,'Initial 247/36 list changed')
 pool=[];withdraw=[]
 for n in ['final_web_observation.json','final_tail_web_observation.json']:
  for ln,l in web_lines(n):
   family='COLLEGE_OR_OTHER_EARLY_ENTRY' if 216<=ln<=439 else 'INTERNATIONAL_EARLY_ENTRY' if 444<=ln<=466 else 'WITHDRAWN' if 169<=ln<=211 else None
   if family and l.strip():
    cells=re.split(r'\s{2,}',l.strip())
    if len(cells)!=4 or not re.fullmatch(r'\d+-\d+',cells[2]):continue
    r={'name':cells[0],'school_or_club':cells[1],'reported_height':cells[2],'reported_2022_status':cells[3],'classification':family,'observation_cache':n,'web_line':ln}
    dest=withdraw if family=='WITHDRAWN' else pool
    if not any(key(x['name'])==key(r['name']) for x in dest):dest.append(r)
 require(len(pool)==149 and sum(x['classification']=='INTERNATIONAL_EARLY_ENTRY' for x in pool)==14,'Final 135/14 participant set changed')
 require(len(withdraw)==24 and {key('Leonard Miller'),key('Dhieu Deing')}<={key(x['name']) for x in withdraw},'Final withdrawals changed')
 initialkeys={key(x['name']) for x in initial}
 require(all(key(x['name']) in initialkeys for x in pool),'Final identity not initial positive entry')
 prospect={}
 for ln,l in web_lines('prospects_web_observation.json'):
  m=re.search(r'†([^†]+?) \| ([^\n]+)',l)
  if not m:continue
  cells=[x.strip() for x in m[2].split('|')]
  if len(cells)==7:prospect[key(m[1])]={'name':m[1],'position':cells[0],'school_or_club':cells[2],'web_line':ln,'current_age_height_weight_status_excluded':True}
 require(len(prospect)==85,'Prospect identity table changed')
 actual=[]
 for ln,l in web_lines('draftorder_web_observation.json'):
  m=re.search(r'^\d+\.\s*.*?draft\s*.*?†([^†]+)\s*\(([^)]+)\)',l)
  if m:actual.append({'name':m[1],'school_or_club':m[2],'web_line':ln})
 require(len(actual)==58 and len({key(x['name']) for x in actual})==58,'Actual participant crosscheck changed')
 # Only the set and public pre-NBA identity are consumed. Actual order/teams/trades are discarded.
 actual=sorted(actual,key=lambda r:key(r['name']))
 projections={'initial':initial,'final':pool,'withdrawn':withdraw,'prospects':prospect,'actual_participant_identity_set':actual}
 for k,h in MEANING_PINS.items():require(digest(projections[k])==h,'Returned public source meaning changed '+k)
 return projections,evidence
def law_observation(d):
 l=d[LAW]['primary_law'];raw=Path(l['cache_path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==l['raw_sha256'],'CBA raw changed')
 pdf=fitz.open(stream=raw,filetype='pdf');pg={str(i):sha_text(pdf[i-1].get_text()) for i in [300,301,302,308]}
 a,b,c,e=[pdf[i-1].get_text() for i in [300,301,302,308]]
 require('nineteen (19)' in a and 'one (1) NBA Season' in a and 'sixty (60)' in b and 'twenty-two (22)' in b,'Eligibility rule unavailable')
 require('in excess of a stipend' in c and 'ten (10) days prior' in e and 'two (2) NBA Drafts' in a,'Professional/withdrawal rule unavailable')
 return {'url':l['url'],'cache_path':l['cache_path'],'raw_sha256':l['raw_sha256'],'PDF_1based_text_sha256':pg}
def sha_text(s):return hashlib.sha256(s.replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()
def participation(name,p):
 final=next((x for x in p['final'] if key(x['name'])==key(name)),None)
 prof=p['prospects'].get(key(name));require(prof is not None,'No official public prospect '+name)
 require(key(name) not in {key(x['name']) for x in p['withdrawn']},'Withdrawn prospect selected '+name)
 require(final is not None or name in AUTOMATIC,'Unsupported legal participation route '+name)
 return {'public_final_entry':copy.deepcopy(final),'public_prospect_identity':copy.deepcopy(prof),'route':'X1biiG3_INTERNATIONAL_TIMELY_EARLY_ENTRY' if final and final['classification']=='INTERNATIONAL_EARLY_ENTRY' else 'X1biiF_TIMELY_EARLY_ENTRY' if final else 'X1biiE_OR_G2_PROFESSIONAL_IGNITE_AUTOMATIC_CONDITIONAL',
 'PS22_admitted_conditions':{'age_at_least_19_in_2022':True,'US_school_class_one_NBA_season_elapsed_if_noninternational':True,'applicable_early_entry_received_by_2022_04_24_and_not_withdrawn':final is not None,'professional_paid_service_rule_if_automatic':name in AUTOMATIC,'international_CBA_definition_required_only_if_G3_or_G2_route_used':True,'nationality_does_not_determine_CBA_international_class':True,'at_most_one_prior_eligible_Draft_and_no_prior_NBA_selection_or_existing_exclusive_NBA_rights':True,'actual_private_papers_or_compensation_certified':False},
 'college_or_international_prior_path_is_public_reference_not_counterfactual_stats':True,'Gonzaga_rival_changed_performance_awards_or_2022_NBA_stats_imported':False}
PARTICIPATION_MEANING_PINS={'Chet Holmgren': 'e37dfa0cb32fde879d66947922ec72fe32576371ddbdff61c745f809fe3caf20', 'Paolo Banchero': '7e1ec39385d058f9e6305ecb58310f3fca3c79607ea139c402781e6ad2457ac4', 'Jabari Smith': '511ee26aa9808347fbbc6ea359ec43b93585b770f47aefd079296997081176c9', 'Jaden Ivey': '2e1870aa0e0f14945a0195747b0b6fefb1831a6bac12cde531f6d08ad4e95ba4', 'Keegan Murray': '3ac29b7a1a028d47f2521ce9f97c6ee73fde9d007314e21ce891cf97b4ad84bb', 'Bennedict Mathurin': '0b07edc5f5ff3b3205680b23433a638aad55f918d80d5b969ade1de24cd2f8da', 'Shaedon Sharpe': '3a8b564140765555c6852d81dabec224e3d5a957c28942149b59e6815ab79fa7', 'Dyson Daniels': '872a5583ab1169c434cce1d14bc200db633145c9eeeb81833796f9c35a952843', 'Jeremy Sochan': 'b471af760c58bce58627c4ea46d199cfcf6875e5ccccc9fbed907826be84d49f', 'Jalen Duren': 'dc1437d4609d0add4187238e2b2c2896fb5bd6e00b4f8c724c71135058b0b602', 'Jalen Williams': 'db619f43265a854b32c13e781d4dfe89b5a987b6ca44c6a2529b9803e1175f2e', 'Ousmane Dieng': '71f796b241998b8a9aed1a1548f0d4532fdb3bdba6a6f830003eb00d00569bad', 'Mark Williams': 'b7f62a0adc8dfc1e5885172a282ba249c2651c260323ca755e69ae264cd18d54', 'Ochai Agbaji': '68648ec727ef4b17ee9ef1f3f09780d41a20853c4bf2545c808e00b322baad3d', 'A.J. Griffin': 'cde185529634848215b16569d19a71659f7e2bd5b86ac35d1cc1c6dd37666732', 'Tari Eason': '726d38448729d23a1a7fc5acea20c8a1d95a7992612760122377d9cd86462acd', 'Malaki Branham': '860911edf185274a8172bf80c18c3217567cda4cf26a38963f85fdc4b8e273ba', 'Walker Kessler': '287b0c4b33e0af28505b62025798bf34ca0643a6df20ec5359d80b7b4504305d', 'Dalen Terry': 'abda61264e8975e41c046a10eea58d19dfd8cf0fe6f2fe3af3989b862a923919', 'Johnny Davis': '35059f55d834589575438bd343ba53a69aea34371c78615fb1bc5536143f6ec4', 'Nikola Jovic': '744bf937f417ed86c209d1042619b0e51b9c5236aa44f34993fe8f523bdaba53', 'Christian Braun': '17bba7e641fe7e4d3aae23a727bcf2fa4dd6fc7b333bbc30ff747d7921abd3f0', 'Jake LaRavia': 'cc2aca1269dd1bd7ca642f4e4da6a79f32597030b1bc8ad93a9f2512e1c27fdc', 'MarJon Beauchamp': '98d9468b4a2f7f4b7991554ab8156ccb8649fb6c499732b79584cb4564275565', 'Wendell Moore Jr.': '374b3469cc4c4ce0b37b1e391aa90adff060725fe6e435d9df662fe32d8503a5', 'TyTy Washington Jr.': '1aac11b817ffbe774cc47c133ff395a6f87131017bb2be55d731153bf39a9165', 'Christian Koloko': 'dbe8648d962839c97e1797fc07a50c92e3fe8d35800462ba5f138688c1f07e36', 'Blake Wesley': '6a6812c3dc722f8436c4e0ed74d81b273cb0892f7cd1a50e1d37554e7ad909fa', 'Patrick Baldwin Jr.': '7855fa839aec6b686f68e321fbccdad81688b7daeb25033614676d80c5810fad', 'Peyton Watson': 'ff4520fe6cd32a379a30e74a494ab70c1f97f55ea116e8e64feaffdfa4ddd385', 'Andrew Nembhard': '372a15cfc573acfcc131b68b6c4b51c81ef2fd4a4d125e7a57f9df637b584a71', 'Caleb Houstan': 'c437fa26b87bc731dae37e56a9475dfe3cb735b91401832e90399f8a47a30887', 'Kennedy Chandler': '36377be0b86083a4fcb37c3684fe8d9ad1100374880d19a4605cc9840ac89add', 'Jaylin Williams': '2aed03050bdfad8c1a6439800fd28ab866500fe1e1ad9bac2f27aac1c67e7bc1', 'Max Christie': 'd1a417dc93e5539769de3c7b5c54f4a0152f38e540111158796e23a02743fa8d', 'Gabriele Procida': '7e3bf6b272a41682fa6ce657f86b4b70b45d428162ea5825f129c09904afeb76', 'David Roddy': '2e5f62043639f2de09d9aac03964dd38f1b379b340d2d994553979de0d7870e0', 'Bryce McGowens': '6f1e021dad087686646159d2d8192e6a9f9217571e97487578a1035c06917e6e', 'Trevor Keels': '1d784819e20e5f0ac3c3a3381b5af715278db25eba9f8b84744499dfd1d2044a', 'Moussa Diabate': '9199c1416f1c5b784ed314aa798dcf4291c4f2a1f3c4a7bd8d02f0b0dc4832da', 'Ryan Rollins': '9bd5451dff5caf100f47814fd86e796fac22e2043a171d39e4454a88e5112454', 'Josh Minott': '570abbc22e6ad18f9b9d2951741a3e0cc0d4a1a09fe13ee5213cd6f6dc470679', 'Ismael Kamagate': '412f485625ab0daf72f3c2f49b9ebab3a2ba52249b5d06c3d7e9fa44a1c47cb7', 'Khalifa Diop': 'ae961797859629705c7e9be160c798e8ee60ba09485576856ccea3a7c90e4113', 'Vince Williams Jr.': 'bdd7e6ce8e33a88fa0787697c6263d62d1068c7e8c53ff6bb1b61c99bf324755', 'Kendall Brown': '2bb0d38d9d30733420291dcbe8ee45ea01dd3feb705915b6b2e051a5754237e1', 'Isaiah Mobley': 'ed629c37361bc725e983b7864f644c5953d25d57ab008eae16571a8003af693e', 'JD Davison': '29703163ddc4b763350e7d361cc36413de1e8b22b2791ac43cdbd8c0af012e0c', 'Tyrese Martin': 'f35dbe6ca21f94338aa24b0d0b42ce723d6e8c3cbee5e73b09d7aee6650897af', 'Matteo Spagnolo': '6cf0cbc8896ae1f87ab24594b2d483fc0861e9316bf10656d6007147957b944a', 'Karlo Matkovic': 'c5b783393c3c18c6e7c17fa57bce4716611861e1d2413ab200908d4a917c8ea0', 'Gui Santos': 'd061c64303e5e4a9b7fb491e8062851c3fbb9e4c2bbb8cff1abe23c738cd3725', 'Yannick Nzosa': '0b0f1da6497d0f0a94e87a6603fc90f0dcca5eb17bf133fbfaeee22cd19136f3', 'Luke Travers': '6958e2b39ea6b7b15d57d488334e025eb829d7d57ab91f878e36d256ac9a9338', 'Hugo Besson': '8fef3170aa9199d074497b4dd7f1aa61dd30b9a11a8f3af89a0302bad8e24aff', 'Jabari Walker': '2603e7f45ed4eb9a9eec40d11bab7f8895772069a199838f79bb793be5f8fa77', 'Keon Ellis': '4e19500d076a29f347d47dd71902c7a8f2d39a746199abb7fd2c3dba99540eac', 'Justin Lewis': '50fe14599f46c5f1de1f2f7af33cedd8c7fcb9fe991a81553ec08abaf22e2c4f', 'Jaden Hardy': '636af764e503362211574bbf862f0b19854b5c21c4896b282411bcaa4b4fd6da', 'EJ Liddell': 'fd71cfae1a16f88144e9adab0ec8c4a8574d54a56242ffb0ba0c2c8cc1dbbf3c'}

def candidate_row(rank,player,entitlement,part,taken):
 return {'pick':rank,'date':'2022-06-23','round':1 if rank<=30 else 2,'origin':entitlement['origin'],'selecting_team':entitlement['current_public_family_holder'],'conditional_final_rights_holder':entitlement['current_public_family_holder'],'player':player,'participation':copy.deepcopy(part),'available_before_selection':player not in taken,'prior_candidate_count':len(taken),'already_taken_before_pick':list(taken),'execution_class':'UNSELECTED_CHICAGO_CORE_PRESERVING_RECOMMENDATION' if rank in [18,57] else 'UNSELECTED_ROUTINE_NPC_DRAFT_CANDIDATE','actual_historical_order_team_or_trade_imported':False,'new_NBA_UPC_or_RequiredTender':False,'new_author_lock':False}
def assert_row(r,k,n,e,part,taken):
 require(r=={'pick':k,'date':'2022-06-23','round':1 if k<=30 else 2,'origin':e['origin'],'selecting_team':e['current_public_family_holder'],'conditional_final_rights_holder':e['current_public_family_holder'],'player':n,'participation':part,'available_before_selection':n not in taken,'prior_candidate_count':len(taken),'already_taken_before_pick':list(taken),'execution_class':'UNSELECTED_CHICAGO_CORE_PRESERVING_RECOMMENDATION' if k in [18,57] else 'UNSELECTED_ROUTINE_NPC_DRAFT_CANDIDATE','actual_historical_order_team_or_trade_imported':False,'new_NBA_UPC_or_RequiredTender':False,'new_author_lock':False},'Returned candidate differs from source rank/identity/eligibility/authority')
def board(names,d,p):
 require(len(names)==60 and len({key(n) for n in names})==60,'Duplicate candidate')
 prior={key(x['player']) for x in d[PRIOR]['selected_rows']};live={key(n) for n in d[GLOBAL]['owner_catalog']}
 require(not ({key(n) for n in names}&(prior|live)),'Existing NBA owner/2021 selection reused')
 require({key(n) for n in names}=={key(x['name']) for x in p['actual_participant_identity_set']}|{key('Keon Ellis'),key('Justin Lewis')},'Complete 58+2 identity domain changed')
 rows=[];taken=[]
 for k,(n,e) in enumerate(zip(names,d[DRAW]['exact_sixty_rank_and_holder_rows']),1):
  part=participation(n,p);require(digest(part)==PARTICIPATION_MEANING_PINS[n],'Returned participation rule differs from inspected source family');r=candidate_row(k,n,e,part,taken);assert_row(r,k,n,e,part,taken);rows.append(r);taken.append(n)
 return rows
def build(root=ROOT):
 d=sources(root);p,raw=public_inputs();law=law_observation(d)
 attempts=json.loads((CACHE/'sources.json').read_text(encoding='utf8'))
 for r in attempts:
  if 'cache_path' in r:require(hashlib.sha256(Path(r['cache_path']).read_bytes()).hexdigest()==r['raw_sha256'],'HTTP attempt raw changed '+r['name'])
 failures=[{**r,'used_as_original_body':False} for r in attempts if r.get('http_status')!=200]
 require(len(failures)==6 and all(r.get('http_status')==403 for r in failures),'Failed HTTP provenance changed')
 require((date(2022,6,23)-date(2022,4,24)).days==60 and (date(2022,6,23)-date(2022,6,13)).days==10,'Calendar function changed')
 rows=board(NAMES,d,p)
 require(len(rows)==60,'Returned board cardinality altered')
 taken=[]
 for k,(n,e,r) in enumerate(zip(NAMES,d[DRAW]['exact_sixty_rank_and_holder_rows'],rows),1):
  part=participation(n,p);require(digest(part)==PARTICIPATION_MEANING_PINS[n],'Returned participation rule differs from inspected source family');assert_row(r,k,n,e,part,taken);taken.append(n)
 alternatives=[]
 for label,swaps in [('D22B_TERRY_WALKER',[(18,19),(56,57)]),('D22C_KOLOKO_LEWIS',[(18,27),(57,58)])]:
  ns=list(NAMES)
  for a,b in swaps:ns[a-1],ns[b-1]=ns[b-1],ns[a-1]
  br=board(ns,d,p);alternatives.append({'id':label,'CHI18':br[17]['player'],'CHI57':br[56]['player'],'candidate_local_swap_pairs':[list(x) for x in swaps],'all60_unique_and_source_entitlements_preserved':True,'selected':False})
 return {'id':'NBA_2022_FULL_DRAFT_WORKING_BOARD_2026_10_08','baseline_main':'bebabcf65be6af0d73d39b5a290249de52952397','status':'COMPLETE_60_ROW_WORKING_CANDIDATE_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'hash_convention':'UTF8BOMstrip;CRLF/CRtoLF','public_provenance':raw,'failed_direct_HTTP_attempts':failures,'initial_PDF_1based_text_sha256':{str(i+1):sha_text(pg.get_text()) for i,pg in enumerate(fitz.open(CACHE/'initial.pdf'))},'primary_law':law,'source_projection_sha256':MEANING_PINS,'participant_pool':p['final'],'final_withdrawals':p['withdrawn'],'automatic_professional_candidates':list(AUTOMATIC),'initial_entry_count':283,'initial_college_count':247,'initial_international_count':36,'final_early_entry_count':149,'reported_prior_withdrawal_count_scope_disagreement':{'June2_headline_total':112,'June15_college_previous':111,'not_equated_or_used_to_infer_eligibility':True},'policy':copy.deepcopy(POLICY),'rows':rows,'Chicago_comparison':{'recommendation':'D22A_KESSLER_ELLIS','CHI18':'Walker Kessler','CHI57':'Keon Ellis','reason':'Backup rim protection behind retained Carter/Mark; late defensive wing development without changing retained Chicago core. Uses pre-draft profiles only, not later NBA outcomes.','alternative_boards':alternatives,'first_UPC_if_later_selected_requires_one_named_standard_slot_resolution':True,'second_candidate_unsigned_RequiredTender_route_available_not_player_rejection_certified':True,'minimum_salary_acceptance_or_TW_conversion_not_selected':True,'existing15STD2TW_unchanged':True},'summary':{'rows':60,'round1':30,'round2':30,'unique_players':60,'source_final_early_entries_used':57,'source_automatic_IGNITE_used':3,'actual2022_draftee_identity_crosschecks':58,'additional_official_eligible_prospects':2,'CHI_picks':[18,57],'new_trades':0,'new_UPCs':0,'new_Tenders':0},'certification':{'independent_review_completed':False,'board_selected':False,'actual_participation_papers_or_foreign_contracts_certified':False,'actual_NBA_2022_draft_or_sanction_certified':False,'full_FY22_roster_cost_or_macro3_complete':False},'remaining_finite_inputs':['Independent source/caller review then root routine draft-board selection; no new human permission inferred.','If first-round Chicago UPC is selected later: named one standard-slot release/assignment with protected Gamma preserved and full rookie price/offer function. Current existing lawful unsigned July8/July15 and second Aug25/Sept5 functions remain applicable.','All 60 holders must exercise selected draft choices under X3, but each UPC/Tender/foreign signing remains a separate finite contract consumer; this candidate does not execute them.','2022 playoffs and 2022-23 dates/results remain separate unfinished work.'],'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0,'manuscript':0}
def validate(x,root=ROOT):
 try:require(x==build(root),'Saved board differs from source reconstruction');return []
 except (ValueError,AssertionError) as e:return [str(e)]
def render(x):
 lines=['# 2022 전체 지명 작업 후보 보드','', '독립 검문 전 후보다. 선택된 가상 추첨의 60순번/권리만 연결하며 지명·UPC·Tender·원역사 거래는 실행하지 않는다.','', '## 원천과 참가 범위','', 'NBA 초기 PDF는 HTTP200 원bytes로 283명(247/36)을 읽었다. 최종 공식 본문은 web 관측135/14와 철회24를 읽었으며 직접HTML403 bytes는 실패로 구분한다. 최종표와 초기표의 실명을 직접 조인했다. 원역사58지명은 이름·학교만 교차자료로 사용하고 순번·팀·거래는 버렸다. 나머지2명 Ellis/Lewis도 최종 참가 명단 안에 있다.','', 'X1/X8의 19세·비국제선수 one-season·60일 early-entry·10일 withdrawal 규칙에 맞는 PS22 참가 가족 조건이다. Ignite 3명은 원 공식 선수경로/실제 지명 양성 자료를 바탕으로 적법 전문팀 유급서비스 분기를 명시한다. 미국에서 학교를 다닌 Koloko 등의 국적을 CBA international 정의로 자동 바꾸지 않는다. 서류·보상·실제 접수 인증은 false다.','', '현재 NBA prospect 표의 나이/키/학년 오류와 철회 Leonard Miller 잔류를 배제했다. Gonzaga의 rival 변경은 Chet/Nembhard의 실제 대학 성적·상·2022 NBA 성장으로 수입하지 않는다. 해당 참가·진로는 별도 가상 적법조건이다.','', '## Chicago 비교','', '| 후보 | 18순위 | 57순위 | 이유 |','|---|---|---|---|','| D22A 권고 | Walker Kessler | Keon Ellis | 코어 유지·백업 림 수비/수비 윙 개발 |','| D22B | Dalen Terry | Jabari Walker | 가드·윙 연결/포워드 개발 |','| D22C | Christian Koloko | Justin Lewis | 센터 개발/윙 크기 |','', 'NBA predraft [Kessler](https://www.nba.com/draft/2022/prospects/walker-kessler), [Ellis](https://www.nba.com/draft/2022/prospects/keon-ellis), [Terry](https://www.nba.com/draft/2022/prospects/dalen-terry), [Koloko](https://www.nba.com/draft/2022/prospects/christian-koloko)에서 역할 방향만 비교했다. 이후 NBA 실력/건강/성과는 사용하지 않았다. 18순위 UPC를 후속 선택하면 기존15STD 중 명명된 한 슬롯을 원보호비용과 함께 해소해야 한다. 지금은 draft-rights/미수락RT 경로로15+2를 바꾸지 않는다. 실제 두 선수가 거절했다는 증거가 아니다.','', '## 60행 후보','', '| 순번 | 원점 | 현재권리 팀 | 선수 |','|---:|---|---|---|']
 for r in x['rows']:lines.append(f"| {r['pick']} | {r['origin']} | {r['selecting_team']} | {r['player']} |")
 lines+=['','## 검문과 다음 소비기','', '물리 repository JSON 독립로드·raw/capture 지문·파싱 의미핀·기존2021선택/459소유 중복 배제·철회배제·60순차가용성·현재권리·returned candidate/UPC/참가 의미를 caller에서 검문한다. 조상 전체 생성기는 재실행하지 않는다. 작성자 음성 controls는 독립검문으로 세지 않는다.','', '현재 법적 참가 family를 갖춘 60개 비교 후보다. 다음은 독립검문 후 루틴 보드 선택과 Chicago 첫RSC 슬롯/비용 소비다. 미공개 영수증이나58 NPC 모두UPC를 완료조건으로 추가하지 않는다. 원2022 58자리·징계·거래 복사는0이다.','', '## 전체 진행','', '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)을 따른다.','', '| 묶음 | 현황 |','|---|---|','| 1 2020 드래프트 | 완료 |','| 2 Chicago2020–21 | S2 완료 |','| 3 2021–23 | 1230/CHI82·60권리 완료, 추첨 검문 수용·2022보드 후보 |','| 4 장기커리어 | 선행 시즌·후속 구현 중 |','| 5 결말·전체구조 | 골격, 기능 배정 계속 |','| 6 규격·Context Pack | 검문 계속·Pack0 |','| 7 통합·독립·작가승인 | 최종 미완료 |','', '미완료 큰묶음5/6번까지4. v0.30 PARTIAL·CLOSED·원고0. 전체macro3 완료로 승격하지 않는다.']
 return '\n'.join(lines)+'\n'
def self_test(root):
 original=candidate_row;count=0
 for field,value in [('player','Leonard Miller'),('selecting_team','LAL'),('new_NBA_UPC_or_RequiredTender',True)]:
  def bad(*args,**kwargs):
   r=original(*args,**kwargs)
   if r['pick']==18:r[field]=value
   return r
  with patch(__name__+'.candidate_row',bad):
   try:build(root)
   except ValueError:count+=1
   else:raise AssertionError('False PASS '+field)
 original_physical=physical
 def badsource(r,p):
  d=original_physical(r,p)
  if p==DRAW:d['exact_sixty_rank_and_holder_rows'][17]['current_public_family_holder']='LAL'
  return d
 with patch(__name__+'.physical',badsource):
  try:build(root)
  except ValueError:count+=1
  else:raise AssertionError('False PASS source')
 return count
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();x=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(render(x),encoding='utf8')
 if a.check:require(not validate(json.loads(text(ROOT/OUT))),'Saved output not current');require(text(ROOT/MD)==render(x),'MD stale')
 print(json.dumps({'current':True,'summary':x['summary'],'writer_negative_controls':self_test(ROOT) if a.self_test else 0},ensure_ascii=False))
if __name__=='__main__':main()
