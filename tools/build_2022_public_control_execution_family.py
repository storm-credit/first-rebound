"""Sixty current origin allocations in a preserved, public named-rights family.

No ancestor constructors, network requests, lottery draw, draftee or UPC choice.
Public templates and explicit lawful fictional negotiation conditions are distinct
from actual private portfolio/disciplinary certification.
"""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from itertools import permutations
from unittest.mock import patch
import argparse,csv,hashlib,io,json
import fitz
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_public_control_execution_family.py'
OUT='simulation/NBA_2022_PUBLIC_CONTROL_EXECUTION_FAMILY.json';MD=OUT[:-5]+'.md'
MAP='simulation/NBA_2022_NAMED_ASSET_CONTROL_MAP.json'
FIRST='research/NBA_2022_PRIOR_FIRST_CLAIM_REFINEMENT_2026_10_08.json'
SEED='simulation/NBA_2021_22_STANDINGS_PLAYIN_AND_2022_RIGHTS.json'
T1='simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json'
S2='simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json'
CHI='research/CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT_2026_10_07.json'
A='canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json'
MIA='research/MIAMI_2021_SELECTED_APRON_CLOSURE_2026_10_07.json'
MIL='simulation/CHICAGO_MILWAUKEE_2021_22_SELECTED_KEEPER_RESULTS.json'
CLE2020='simulation/2020_DRAFT_PATRICK_WILLIAMS_RELANDING_BOARD.csv'
PINS={MAP:'ca1be50a889fa8aa1ad47cc696d64c7bfc00cc7ebd77b2bdf9ede815ca88d4f2',FIRST:'0af7a125c8441129c0fd6f2aed242109bd2bca72ad44959ca65c2977c18f541b',SEED:'139c1d6a90d1bd7ee672020af96e03bf6767599637902c329b1e772fdfcf63d9',T1:'f8c78e99cce1b02a051c94339b550fdb52205d3988db8bbe69b780559c3bc306',S2:'cfa2f49bb82baa49b2298d90c97cd7fd8075e91380424d40bfd44772d8228a2b',CHI:'bf8087a89af09a817c0a3eb5d4df906a906575a56016c873912db00eccdca9db',A:'9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce',MIA:'3007e4a2407a02e97998826c3cb8ee352ac2a75353b3c8c5822c16aa55fdbb48',MIL:'fcb8298501701dc21bef9199ffac2d10456384f808ffe2a8b4222cd9e7b0e583',CLE2020:'5a80a0dab1573afe65d50f85a5620fecc75c327ccea651cbd0bcadf1208f957d'}
TEMP=Path('C:/Users/Storm Credit/AppData/Local/Temp');CACHE=TEMP/'fr-control2022-20261007'
RAW={
 'BULLS':(TEMP/'first-rebound-bulls-guide.pdf','113bf68ccc0d5b891f3bbc942a96f2c32b96caa6d3438299ebe92fc3ffebfe9e',[398,400],'https://chibullsdigital.com/mediaGuide/2022_ChicagoBulls_MG_NBA_HI.pdf'),
 'ORL':(TEMP/'orlando-magic-media-guide-2022-23.pdf','63550e97068a14cbd60d8b461d1f15c0bb898652c9813fdbfa113509f5a8f92c',[116],'https://cdn.nba.com/teams/uploads/sites/1610612753/2022/11/orlando-magic-media-guide-2022-23.pdf'),
 'ATL2018':(CACHE/'hawks2018.pdf','e269c7a00691037c4cadf63782718102a28bd0b8dd8722458c37988bea3e891a',[2],'https://atlantahawkspr.wordpress.com/wp-content/uploads/2018/05/atlanta-hawks-2018-nba-draft-lottery-fact-sheet.pdf'),
 'ATL2020':(CACHE/'hawks_2020_fact_sheet.pdf','ef82b33affc3c0243129d40f10c06a95cadd4ae2d6e254094aeb0de82f4e59cf',[2],'https://atlantahawkspr.wordpress.com/wp-content/uploads/2020/08/atlanta-hawks-2020-nba-draft-lottery-fact-sheet.pdf'),
 'CLE':(CACHE/'cle2022.pdf','505fc2b82cf6fa44006d76380a0c8314c335265fd85a0c7cd29ff2a4097e364c',[7],'https://cdn.nba.com/teams/uploads/sites/1610612739/2022/10/04-season.pdf'),
 'GSW':(CACHE/'gsw2022.pdf','322a7a509a8f2f9da01f8e6c70f185c855cae9b9c20aa5e201672ebdca3fa45b',[457,458],'https://cdn.nba.com/teams/uploads/sites/1610612744/2022/10/Golden_State_Warriors_2022_23_Media_Guide.pdf'),
 'BI_CHI':(TEMP/'fr-chi-bi-cap-20210422.html','332a9ea81c3f01a934b31d61c2a57ea8a287c9cb1956741545c97b09ccdfb985',[],'https://web.archive.org/web/20210422012709id_/http://www.basketballinsiders.com/chicago-bulls-team-salary/'),
 'BI_DEN':(TEMP/'first-rebound-denver-cost-2026-10-06/BI_DEN_archive.html','d6a41cd3209a62c428578ea14c7acc1fe7338df4c206bf871b8e4de41b5af942',[],'https://web.archive.org/web/20210422002709id_/https://www.basketballinsiders.com/denver-nuggets-team-salary/')}
# Read observations, not fabricated downloaded article bytes. Failed HTTP bodies
# are retained in the collection log and never used as positive body evidence.
WEB=[
 {'id':'OLADIPO_REPORT','url':'https://www.miamiherald.com/sports/spt-columns-blogs/barry-jackson/article251588273.html','date':'2021-06-01','channel':'ORIGINAL_REPORTER_BODY_READ','ref':'turn2332view1','facts':'MIA lottery protected; HOU two best HOU/BKN/MIA; MIA worst. Protected fallback DEN/PHI lesser second to HOU.','raw_body_adopted':False},
 {'id':'OLADIPO_ORIGINAL_REPORT','url':'https://www.espn.com/nba/story/_/id/31135332/houston-rockets-trade-victor-oladipo-miami-heat-source-says','date':'2021-03-25','channel':'ORIGINAL_REPORTER_INDEXED_BODY_READ','ref':'turn2330search5','facts':'Oladipo/Olynyk/Bradley; first swap. S2 separately preserves the three-player event.','raw_body_adopted':False},
 {'id':'IND_LINK_REPORT','url':'https://www.thescore.com/nba/news/2054177','date':'2020-11-18','channel':'SECONDARY_REPORT_OF_MAGIC_ANNOUNCEMENT_NUMERIC_TEMPLATE','ref':'turn2332view2','facts':'IND second to ORL the year after IND conveys to BKN; BKN 45–60 protection until 2023.','raw_body_adopted':False,'exact_original_contract_certified':False},
 {'id':'IND_CURRENT_TEAM','url':'https://www.nba.com/pacers/news/pacers-enter-2022-nba-draft-lottery-eyes-top-pick','date':'2022-04','channel':'INDEXED_TEAM_BODY_READ_NORMAL_OPEN_IFRAME','ref':'turn2335search0','facts':'Original current IND second owed ORL via MIL; original ranks not transported.','raw_body_adopted':False},
 {'id':'TILLMAN_COMPLETED','url':'https://www.nba.com/news/2020-nba-draft-trade-tracker','date':'2020-11-19','channel':'INDEXED_NBA_TRANSACTION_TRACKER_READ','ref':'turn2323search6','facts':'Tillman rights to MEM; Woodard rights and 2022 second to SAC.','raw_body_adopted':False,'separate_team_release_HTTP403_not_adopted':True},
 {'id':'ENNIS_COMPLETED','url':'https://www.nba.com/pistons/news/detroit-pistons-acquire-forward-james-ennis-iii','date':'2018-02-08','channel':'INDEXED_TEAM_BODY_READ','ref':'turn2315search4','facts':'Ennis to DET; Brice Johnson and 2022 second to MEM. Composite identity supported by BI_CHI.','raw_body_adopted':False},
 {'id':'CLARKSON_COMPLETED','url':'https://www.nba.com/cavaliers/news/features/exum-trade-191224','date':'2019-12-24','channel':'TEAM_BODY_READ','ref':'turn2336search1','facts':'Clarkson to UTA; Exum and SAS2022/GSW2023 seconds to CLE.','raw_body_adopted':False},
 {'id':'HUGHES_COMPLETED','url':'https://www.nba.com/pelicans/pelicans-complete-trade-jazz-nba-draft-2020-elijah-hughes','date':'2020-11-19','channel':'INDEXED_TEAM_BODY_READ','ref':'turn2316search0','facts':'Hughes rights to UTA for UTA2022 second to NOP.','raw_body_adopted':False},
 {'id':'CLE_ATL_NOP_SECONDARY_CROSS_CHECK','url':'https://www.basketball-reference.com/teams/NOP/2020_transactions.html','date':'2019-07-06','channel':'SECONDARY_TRANSACTION_CROSS_CHECK','ref':'turn2339search4','facts':'ATL transfers CLE conditional first family to NOP. T1 separately preserves NOP2021 second.','raw_body_adopted':False,'nominal_team_release_unread':'https://www.nba.com/pelicans/pelicans-acquire-rights-alexander-walker-hayes-silva'},
 {'id':'CLE_NAMED_FIRST_REPORT','url':'https://www.nba.com/news/busy-night-reported-trades-early-nba-draft','date':'2019-06-21','channel':'ORIGINAL_AP_REPORT_ON_NBA_INDEXED_BODY_READ','ref':'turn2342search4','facts':'ATL sends protected Cleveland2020 first to NOP.','raw_body_adopted':False},
 {'id':'ATL_NOP_COMPLETED_PUBLIC_FAMILY','url':'https://www.nba.com/pelicans/news/clone-pelicans-news-around-web-7-5-2019','date':'2019-07-08','channel':'INDEXED_TEAM_COMPLETED_AND_SIGNING_BODY_READ','ref':'turn2342search1','facts':'Completed July6 ATL trade includes future first to NOP; specific Cleveland identity from original AP report.','raw_body_adopted':False},
 {'id':'FREE_AGENCY_2020_CLOCK','url':'https://www.nba.com/news/nba-board-of-governors-approves-adjustments-to-collective-bargaining-agreement','date':'2020-11-11','channel':'INDEXED_NBA_OFFICIAL_RELEASE_BODY_READ','ref':'turn2341search2','facts':'Negotiations Nov20 18ET; signing Nov22 12:01ET.','raw_body_adopted':False},
 {'id':'FREE_AGENCY_2021_CLOCK','url':'https://pr.nba.com/nba-salary-cap-for-2021-22-season-set-at-112-414-million/','date':'2021-08-02','channel':'NBA_COMMUNICATIONS_OFFICIAL_RELEASE_BODY_READ','ref':'turn2341search6','facts':'Negotiations Aug2 18ET; moratorium ends Aug6 noonET.','raw_body_adopted':False},
 {'id':'MIL_PENALTY','url':'https://www.nba.com/news/nba-imposes-penalty-on-bucks-for-early-free-agency-discussions','date':'2020-12-21','channel':'INDEXED_NBA_BODY_READ','ref':'turn2323search5','facts':'Original MIL2022 second rescinded for Bogdanovic early discussions; no completed player contract needed.','raw_body_adopted':False},
 {'id':'CHI_MIA_PENALTY','url':'https://www.nba.com/news/chicago-bulls-miami-heat-free-agency-violations','date':'2021-12-01','channel':'INDEXED_NBA_BODY_READ_IN_UPSTREAM_MAP','facts':'Original CHI/MIA next-available seconds rescinded for early Lonzo/Lowry discussions.','raw_body_adopted':False}]
POLICY={'preserved_public_prior_assignment_family_selected':True,'exercise_beneficial_existing_swaps':True,'new_2022_offseason_or_deadline_trade':False,'MIL_Bogdanovic_early_contact_selected':False,'CHI_Lonzo_early_contact_selected':False,'MIA_Lowry_early_contact_selected':False,'2020_free_agent_talks_not_before_ET':'2020-11-20T18:00:00','2021_free_agent_talks_not_before_ET':'2021-08-02T18:00:00','fictional_permitted_contacts_only':True,'actual_past_contact_absence_certified':False,'actual_discipline_absence_certified':False,'original_MIL_PHI_forfeitures_automatically_copied':False,'player_or_UPC_or_Tender_selection':False}
FIXED_POLICY=deepcopy(POLICY);FIXED_WEB=deepcopy(WEB)

def need(v,m):
 if not v:raise AssertionError(m)
def txt(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(txt(p).encode()).hexdigest()
def disk(root,p):return list(csv.DictReader(io.StringIO(txt(root/p))))if p.endswith('.csv')else json.loads(txt(root/p))
def physical(root,p):return disk(root,p)
def sources(root):
 out={}
 for p,h in PINS.items():
  need(sha(root/p)==h,'Source stale '+p);v=physical(root,p)
  need(v==disk(root,p),'Returned physical source differs '+p);out[p]=v
 need(POLICY==FIXED_POLICY and WEB==FIXED_WEB,'Public family/timing source semantics changed')
 return out

def raw_provenance():
 out=[];texts={}
 for k,(p,h,pages,u)in RAW.items():
  need(hashlib.sha256(p.read_bytes()).hexdigest()==h,'Raw source stale '+k)
  if pages:
   with fitz.open(p)as d:ts={str(i):d[i-1].get_text()for i in pages}
  else:ts={'HTML':BeautifulSoup(p.read_bytes(),'html.parser').get_text(' ',strip=True)}
  texts[k]=' '.join(' '.join(ts.values()).split());out.append({'id':k,'path':str(p),'url':u,'raw_sha256':h,'classification':'ORIGINAL_JOURNALIST_PUBLISHED_RESEARCH_NOT_TEAM_CONTRACT_CERT'if k.startswith('BI_')else'OFFICIAL_TEAM_PDF','PDF_pages_1_based':pages,'extraction':'PyMuPDF get_text() UTF8; HTML BeautifulSoup get_text space strip; clause matching collapses whitespace only','extracted_text_sha256':{i:hashlib.sha256(t.encode()).hexdigest()for i,t in ts.items()}})
 checks={'BULLS':['Jameer Nelson','2022','Lakers','whichever is more favorable'],'ORL':['Indiana in either 2022, 2023 or 2024','2026'],'ATL2018':['protected #1-10','2021 and 2022'],'ATL2020':['#31-55','Los Angeles Clippers'],'GSW':['2022 second-round draft pick (from Toronto via Philadelphia; top 54','2022 second-round pick via Toronto'],'CLE':['via Washington','via Houston','via Miami'],'BI_CHI':['James Ennis, Xavier Tillman','Los Angeles Lakers'],'BI_DEN':['higher pick going to the Minnesota','lower going to the Miami']}
 for k,items in checks.items():need(all(x in texts[k]for x in items),'Positive public source clause missing '+k)
 return out

def dependencies(src):
 # Actual atom objects, not merely names in an old report.
 e={x['id']:x for x in src[S2]['dated_events']}
 atom=[]
 for id,p,a,b in [('FEED:5455','Kelly Olynyk','MIA','HOU'),('FEED:5456','Avery Bradley','MIA','HOU'),('FEED:5458','Victor Oladipo','HOU','MIA')]:
  x=e[id];need((x['player'],x['origin'],x['team'],x['date'])==(p,a,b,'2021-03-25')and x['omitted_by_approved_direction']is False,'Oladipo original common atom not retained')
  atom.append({'id':id,'player':p,'from':a,'to':b,'date':x['date'],'classification':x['classification'],'row_sha256':x['source_row_sha256']})
 ind=next(x for x in src[T1]['selected_rows']if x['round']==2 and x['origin']=='IND')
 cle=next(x for x in src[T1]['selected_rows']if x['round']==2 and x['origin']=='CLE')
 need((ind['pick'],ind['conditional_final_draft_rights_holder'])==(43,'BKN'),'IND prior2021 settlement not BKN43')
 need(cle['conditional_final_draft_rights_holder']=='NOP','CLE prior second family lost NOP')
 c=[x for x in src[CLE2020]if x['branch']=='PRIMARY'and x['pick']=='5']
 need(len(c)==1 and c[0]['team']=='Cleveland Cavaliers'and c[0]['status']=='AUTHOR_LOCKED','CLE2020 first nonconvey input changed')
 need(src[A]['selected']['route']=='G1A_PLUS_M1'and 'G1C_PLUS_M1_LONZO'in src[A]['mutually_exclusive_routes_not_selected'],'CHI Lonzo direction changed')
 need(src[CHI]['positive_claim_bridge'][0]['count_upper']==1 and src[CHI]['positive_claim_bridge'][1]['count_upper']==1,'CHI cardinality changed')
 return {'S2_Oladipo_completed_working_player_atom':atom,'IND2021_second_to_BKN':{'pick':43,'year':2021},'CLE2020_retained_first':5,'CLE2021_second_to_NOP_preserved':True,'CHI_route':'G1A_PLUS_M1','nonselected_original_deadline_atoms':['NOP/MEM JV+Graham','CLE/MIN Rubio','CLE/IND LeVert','BKN/DET Jordan','DAL/WAS Porzingis','PHX/IND JalenSmith','UTA/MEM Aldama/Butler','UTA/POR Ingles','CHI/SAS DeRozan','WAS/SAS Dinwiddie-fiveway','TOR/SAS Dragic/Young','PHI/BKN Harden/Simmons','BOS/SAS White/Richardson/Langford']}

def domains(src):return {(x['round'],x['origin']):x['origin_rank_domain']for x in src[MAP]['typed_control_rows']}

def allocation_family(ranks,src):
 """Evaluate one admissible rank input; no draw is performed or selected."""
 ds=domains(src);need(set(ranks)==set(ds),'Rank origin domain missing')
 for k,v in ranks.items():need(type(v)is int and v in ds[k],'Rank outside current symbolic domain')
 need(sorted(ranks[k]for k in ranks if k[0]==1)==list(range(1,31)),'First rank collision')
 need(sorted(ranks[k]for k in ranks if k[0]==2)==list(range(31,61)),'Second rank collision')
 pool=[t['team']if isinstance(t,dict)else t for t in src[SEED]['nonplayoff_lottery_origins']]
 ordered=sorted(pool,key=lambda t:ranks[(1,t)])
 # The first four are supplied draw outcomes; every undrawn origin keeps the
 # frozen inverse-record order. Individually legal ranks alone are insufficient.
 need(ordered[4:]==[t for t in pool if t not in ordered[:4]],'Supplied lottery ranks break undrawn origin order')
 # Nonlottery ties obey §7.02(c); first lottery rank parameters are not sampled.
 for t in ('CHI','GSW'):need(ranks[(1,t)]+ranks[(2,t)]==65,'CHI/GSW second tie not reverse first')
 for t in ('BOS','LAC','LAL','PHX'):need(ranks[(1,t)]+ranks[(2,t)]==81,'Four-way second tie not reverse first')
 h={k:k[1]for k in ranks};why={k:'PRESERVED_POSITIVE_OWN_ORIGIN_PUBLIC_TEMPLATE'for k in ranks}
 for x in src[FIRST]['refined_first_rows']:
  k=(1,x['origin']);need(any(c['rank_parameter']==ranks[k]and c['underlying_pick_holder']==x['invariant_holder_in_current_rank_domain']for c in x['allocation_cells']),'Prior first function mismatch')
  h[k]=x['invariant_holder_in_current_rank_domain'];why[k]='REVIEWED_PRIOR_FIRST_CURRENT_DOMAIN_FUNCTION'
 for t,owner in [('LAC','OKC'),('BKN','HOU')]:h[(1,t)]=owner;why[(1,t)]='PRESERVED_PG_OR_HARDEN_PRIOR_FIRST'
 # March25 Oladipo family replaces MIA identity; includes both counterpart picks.
 o=sorted(('HOU','BKN','MIA'),key=lambda t:ranks[(1,t)])
 need(ranks[(1,'MIA')]>14 and o[-1]=='BKN','Current Oladipo unprotected swap branch changed')
 for t in o:h[(1,t)]='MIA'if t==o[-1]else'HOU';why[(1,t)]='PRESERVED_OLADIPO_JOINT_FIRST_SWAP'
 # Sequential existing claims: CHI better of CHI/DET, SAC residual via MEM;
 # WAS then exchanges its LAL pick for that better claim.
 better=min(('CHI','DET'),key=lambda t:ranks[(2,t)]);less=max(('CHI','DET'),key=lambda t:ranks[(2,t)])
 need(ranks[(2,better)]<ranks[(2,'LAL')],'Current beneficial Satoransky exchange fails')
 h[(2,better)]='WAS';h[(2,less)]='SAC';h[(2,'LAL')]='CHI'
 for t in ('CHI','DET','LAL'):why[(2,t)]='NELSON_ENNIS_TILLMAN_SATORANSKY_JOINT_EXERCISE'
 dn=min(('DEN','PHI'),key=lambda t:ranks[(2,t)]);dp=max(('DEN','PHI'),key=lambda t:ranks[(2,t)])
 h[(2,dn)]='MIN';h[(2,dp)]='MIA'
 for t in ('DEN','PHI'):why[(2,t)]='CHANDLER_BUTLER_BOL_SECOND_COMPOSITE'
 for t,owner,reason in [('HOU','CLE','PRIOR_KNIGHT_SHUMPERT_CLAIM_LEVERT_NOT_EXECUTED'),('MIA','IND','PRIOR_OKPALA_CLAIM_LEVERT_NOT_EXECUTED'),('WAS','CLE','PRIOR_HILL_DELLAVEDOVA_CLAIM_RUBIO_NOT_EXECUTED'),('IND','ORL','PRIOR2021_BKN_DELIVERY_THEN_BROGDON_ORL_SECOND'),('SAS','CLE','DIAW_THEN_CLARKSON_PRIOR_SECOND'),('TOR','GSW','BURKS_GRIII_PRIOR_SECOND_CHA_TOP54_NOT_CONVEYED'),('UTA','NOP','HUGHES2020_PRIOR_SECOND'),('CLE','NOP','KORVER2020_TOP10_NONCONVEY_THEN_TWO_SECONDS_JV_NOT_EXECUTED')]:h[(2,t)]=owner;why[(2,t)]=reason
 need(ranks[(2,'ATL')]<=55 and ranks[(2,'TOR')]<=54,'Protected second current branch changed')
 # MIL/PHI claims survive only in the explicitly chosen lawful timing family.
 need(POLICY['fictional_permitted_contacts_only']and not POLICY['MIL_Bogdanovic_early_contact_selected']and not POLICY['MIA_Lowry_early_contact_selected'],'Causal forfeiture port cannot silently close')
 return [{'id':f'{t}_2022_R{n}','year':2022,'round':n,'origin':t,'rank_parameter':ranks[(n,t)],'current_public_family_holder':h[(n,t)],'rule':why[(n,t)],'player':None,'new_UPC_or_Tender':False,'actual_private_control_certified':False}for n,t in sorted(ranks)]

def assert_allocation(rows,ranks):
 # Independently pinned positive policy outputs: shared wrong resolver outputs
 # cannot pass merely because original and candidate are equal.
 f={'LAC':'OKC','LAL':'NOP','PHX':'OKC','UTA':'MEM','BKN':'MIA','MIA':'HOU'}
 s={'CHI':'SAC','DET':'WAS','LAL':'CHI','DEN':'MIN','PHI':'MIA','HOU':'CLE','MIA':'IND','WAS':'CLE','IND':'ORL','SAS':'CLE','TOR':'GSW','UTA':'NOP','CLE':'NOP'}
 need(len(rows)==60 and len({x['id']for x in rows})==60,'Allocation cardinality collision')
 for x in rows:
  n,t=x['round'],x['origin'];owner=(f if n==1 else s).get(t,t)
  need(x['id']==f'{t}_2022_R{n}'and x['year']==2022 and x['rank_parameter']==ranks[(n,t)]and x['current_public_family_holder']==owner,'Returned holder/origin/rank differs from public allocation policy')
  need(x['player']is None and x['new_UPC_or_Tender']is False and x['actual_private_control_certified']is False,'Unselected player/UPC or private certification promoted')
 need(sum(x['current_public_family_holder']=='CHI'for x in rows if x['round']==1)==1 and sum(x['current_public_family_holder']=='CHI'for x in rows if x['round']==2)==1,'CHI one first plus one composite second violated')

def rank_inputs(src):
 """48 tie endpoint realizations; lottery placeholders are tests, not draws."""
 ds=domains(src);base={k:min(v)for k,v in ds.items()}
 # This no-upset lottery realization is a valid test input only. It is neither
 # the selected lottery nor a set of duplicate rank-one placeholders.
 for i,t in enumerate(src[SEED]['nonplayoff_lottery_origins']):
  if isinstance(t,dict):t=t['team']
  base[(1,t)]=i+1
 for cs in permutations(('CHI','GSW')):
  for ws in permutations(('BOS','LAC','LAL','PHX')):
   r=deepcopy(base)
   for i,t in enumerate(cs):r[(1,t)]=17+i;r[(2,t)]=48-i
   for i,t in enumerate(ws):r[(1,t)]=24+i;r[(2,t)]=57-i
   yield r

def build(root=ROOT):
 src=sources(root);raw=raw_provenance();dep=dependencies(src);ds=domains(src)
 need(len(ds)==60,'Sixty origins missing');reference=None;cells=0
 for ranks in rank_inputs(src):
  rows=allocation_family(ranks,src);assert_allocation(rows,ranks);cells+=len(rows)
  projection=[{k:v for k,v in x.items()if k!='rank_parameter'}for x in rows]
  if reference is None:reference=projection
  else:need(reference==projection,'Current holder not invariant under unresolved coupled ties')
 ports=[]
 for x in reference:
  r=deepcopy(x);r['rank_domain']=ds[(x['round'],x['origin'])];r['exact_rank']=None;r['callable']='allocation_family(rank_parameters, pinned_sources)';ports.append(r)
 return {'id':'NBA_2022_PUBLIC_CONTROL_EXECUTION_FAMILY','baseline_main':'f943e0983b4e3df96d452a61e0402a3a7877dada','status':'SIXTY_PUBLIC_NAMED_CONTROL_FUNCTIONS_ROUTINE_WORKING_FAMILY_PREPARED_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'hash_convention':'Repository BOMstrip CRLF/CR→LF UTF8; raw bytes unchanged','raw_provenance':raw,'web_body_observations':deepcopy(WEB),'failed_collection_log':str(CACHE/'remaining_prefix_collection.json'),'failed_HTTP403_or_timeout_bodies_adopted':False,'policy':deepcopy(POLICY),'positive_and_omission_dependencies':dep,'sixty_origin_control_functions':ports,'joint_groups':[{'id':'CHI_DET_LAL','origins':['CHI','DET','LAL'],'holders_by_origin':{'CHI':'SAC','DET':'WAS','LAL':'CHI'},'existing_beneficial_options_exercised_as_working_family':True},{'id':'DEN_PHI','origins':['DEN','PHI'],'holders_by_origin':{'DEN':'MIN','PHI':'MIA'},'MIA_lottery_fallback_to_HOU_not_triggered':True},{'id':'HOU_BKN_MIA_FIRST','origins':['HOU','BKN','MIA'],'holders_by_origin':{'HOU':'HOU','BKN':'MIA','MIA':'HOU'},'source_S2_three_player_atom_preserved':True}],'source_map_identity_candidates_superseded':[{'origin':'MIA','round':1,'reason':'Positive preserved Oladipo swap; MIA16/BKN23.'},{'origin':'CLE','round':2,'reason':'Positive original Korver first conversion; CLE2020locked5 and JV atom omission.'}],'sanction_causality':{'historical_2022_forfeited_origin_claims':['MIL_R2','PHI_R2_MIA_HELD'],'selected_lawful_contact_family_no_forfeiture':True,'this_is_fictional_timing_choice_not_actual_absence_certification':True,'CHI_Lonzo_cause_not_selected':True,'new_evidence_of_preserved_illegal_contact_reopens_relevant_claim':True},'summary':{'origin_functions':60,'first_functions':30,'second_functions':30,'coupled_tie_inputs_checked':48,'allocation_cells_checked':cells,'current_holder_invariant_origins':60,'CHI_first_claims':1,'CHI_second_claims':1,'holder_counts':dict(sorted(Counter(x['current_public_family_holder']for x in ports).items())),'exact_draws_selected':0,'players_selected':0,'UPC_or_Tender_selected':0},'scope':{'whole_sixty_public_control_function_candidate_complete':True,'published_original_family_plus_explicit_lawful_fictional_conditions':True,'every_unreported_private_claim_absent_certified':False,'full_private_contract_AST_equivalence_certified':False,'exact_2022_lottery_or_tie_draw_selected':False,'source_numeric_IND_link_is_reported_template_not_original_contract_cert':True,'future_2023_2027_rank_delivery_acceptance_certified':False,'new_author_lock':False,'root_adoption_of_this_new_family_recorded':False,'independent_review_completed':False,'whole_macro3':False,'season_winners_or_health_modified':False},'remaining_finite_consumers':['Select recorded working lottery/top4 and first-tie draws, then evaluate coupled second order; holders here are invariant in current domains.','New2022draftee/participation/Tender/UPC uses are separate; no forced sixty signed rookies.','2022–23 result/postseason and2023entitlements remain separate macro3 exit inputs.'],'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0,'manuscript':False}

def validate(v,root=ROOT):return []if v==build(root)else['Public control family differs from source-bound reconstruction']
def markdown(v):
 lines=['# 2022 공개 권리: 60원점 공동 배정 함수','',v['status'],'','기존 지도와 네 prior first 증인은 불변 입력이다. 추첨이나 선수지명 없이 현재 순번 구간의 60권리 함수를 완성한 작업 가족이다. 모든 사적 장부나 실제 접수·징계의 인증은 아니다. 루트의 독립 검문·채택 전 상태를 보존한다.','','## 공동 배정','', '| 원점 | 현재 가족의 수령자 | 연결 |','|---|---|','| HOU/BKN/MIA first | HOU/MIA/HOU | 승인된 March25 Oladipo 선수 원자행 + 원 first 교환 |','| CHI/DET/LAL second | SAC/WAS/CHI | Nelson → Ennis/Tillman 잔여 → Satoransky 비교 |','| DEN/PHI second | MIN/MIA | Chandler/Butler와 Bol의 유리·불리 비교 |','| CLE second | NOP | locked2020 first5 비전달 → 두 second; JV 원자행 생략 |','| IND second | ORL | selected2021 second43→BKN 뒤의 연도 함수 |','| HOU/MIA/WAS second | CLE/IND/CLE | LeVert·Rubio 생략 전의 명명된 보유권 |','| TOR/UTA/SAS second | GSW/NOP/CLE | Burks/GRIII, Hughes, Diaw/Clarkson 원 연결 |','','[Miami 원 취재](https://www.miamiherald.com/sports/spt-columns-blogs/barry-jackson/article251588273.html)의 교환 구조를 S2의 Olynyk·Bradley·Oladipo 원자행에 연결했다. MIA16/BKN23 관계에서 first 두 상대 원점의 수령자가 바뀐다. MIA가 lottery 밖이므로 별도 second fallback은 미발동이다. 기존 identity 후보를 최종 소유로 복사하지 않았다.','','Bulls 공식 guide PDF398/400은 두 기존 교환의 순서, BI 원 연구는 Ennis/Tillman 잔여 수령자를 지원한다. 기존 옵션의 유리한 행사를 작업 가족으로 구성하되 새 DeRozan·fiveway·Dragic 거래를 추가하지 않는다. 세 원점은 정확히 세 권리이며 Chicago에는 first 하나와 composite second 하나만 남는다.','','[Hawks2018 공식 PDF](https://atlantahawkspr.wordpress.com/wp-content/uploads/2018/05/atlanta-hawks-2018-nba-draft-lottery-fact-sheet.pdf) 2쪽의 CLE 전환을 locked2020 pick5·selected2021 NOP second와 연결했다. 원2022 MEM 수령을 발생시킨 JV 교환은 미선택이다. IND의 연도 연결은 [발표를 전한 숫자 템플릿](https://www.thescore.com/nba/news/2054177)과 [구단의 현재 권리 설명](https://www.nba.com/pacers/news/pacers-enter-2022-nba-draft-lottery-eyes-top-pick)을 구분한다. 이는 사적 원 계약서의 정확 조항 인증이 아니다.','','## 징계와 선택의 경계','','원 [MIL 조기 접촉 징계](https://www.nba.com/news/nba-imposes-penalty-on-bucks-for-early-free-agency-discussions)와 [CHI/MIA 징계](https://www.nba.com/news/chicago-bulls-miami-heat-free-agency-violations)를 인과 포트로 보존한다. 새 family는 허용 시간 이후의 접촉만 구성하고 Chicago Lonzo 경로를 추가하지 않는다. 원징계를 자동 복사하지 않으며 실제 과거 위반·징계 부재를 인증하지 않는다. 원 위반 원인이 정본에서 새로 확인되면 해당 권리는 재개방한다.','','## 검문과 후속','','원 저장소10핀+SELF, raw8, PDF쪽별 추출 지문, 관측 본문과 실패 HTTP 바이트를 분리한다. caller는 48연동 tie입력×60배정을 독립 명명 정답과 대조한다. lottery 값은 테스트용 기호 입력이며 추첨 선택이 아니다. first17/18의 second48/47, first24–27의 second57–54를 강제한다. 원 승패·건강·계약·미래 실제 순번 변경0.','','다음 소비기는 선택된 draw를 넣어 exact rank를 출력할 수 있다. 선수·계약·Tender는 별도이며 60명 UPC를 강요하지 않는다. 전체 macro3·원고 gate는 열지 않는다.','','[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','','| 묶음 | 현황 |','|---|---|','| 1 드래프트 연쇄 | 완료 |','| 2 Chicago2020–21 | 완료 |','| 3 2021–23 |1230·순위·play-in 완료 /2022 공개 control 함수 후속 |','| 4 장기 커리어 | 진행 |','| 5 전체 구조 | 진행 |','| 6 집필 규격·Context Pack | 진행·Pack0 |','| 7 통합·작가 승인 | 미완료 |','','미완료 큰 묶음5 /6번까지4. v0.30 PARTIAL·CLOSED·원고0.','']
 return '\n'.join(lines)
def main():
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');q=a.parse_args();v=build()
 if q.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if q.check:need(disk(ROOT,OUT)==v and txt(ROOT/MD)==markdown(v),'Saved public control family stale')
 n=0
 if q.self_test:
  original=allocation_family
  for fault in ('CHI_holder','MIA_first','UPC'):
   def bad(r,s):
    rows=original(r,s);x=next(x for x in rows if(x['round'],x['origin'])==((1,'MIA')if fault=='MIA_first'else(2,'LAL')))
    if fault=='UPC':x['new_UPC_or_Tender']=True
    else:x['current_public_family_holder']='MIA'if fault=='MIA_first'else'SAC'
    return rows
   try:
    with patch(__name__+'.allocation_family',bad):build()
   except AssertionError:n+=1
   else:raise AssertionError('Wrong allocation accepted '+fault)
  old=physical
  def badsource(root,p):
   z=deepcopy(old(root,p))
   if p==S2:next(x for x in z['dated_events']if x['id']=='FEED:5458')['team']='HOU'
   return z
  try:
   with patch(__name__+'.physical',badsource):build()
  except AssertionError:n+=1
  else:raise AssertionError('Wrong same-SHA Oladipo atom accepted')
  src=sources(ROOT);r=next(rank_inputs(src));r[(1,'CLE')],r[(1,'WAS')]=r[(1,'WAS')],r[(1,'CLE')]
  try:allocation_family(r,src)
  except AssertionError:n+=1
  else:raise AssertionError('Undrawn lottery origins silently reordered')
 print(json.dumps({'current':True,'functions':60,'tie_cases':48,'cells':2880,'writer_negative_controls':n}))
if __name__=='__main__':main()
