"""One finite 1230-key consumer; new fictional interval selection, no ancestor builds.

Physical source bytes and consumed source meanings are pinned independently.
Already selected CHI82 clocks and winners are conserved, not overwritten by an
observed winner column. Other dates receive an explicit new delegated model.
"""
from pathlib import Path
from collections import Counter, defaultdict
from fractions import Fraction
from datetime import date, timedelta
from copy import deepcopy
from unittest.mock import patch
import argparse, csv, hashlib, io, json

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2021_22_global_selected_regular_results.py'
OUT='simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json'
MD=OUT[:-5]+'.md'
BASELINE='18ab12a167a3e0885743171ff534c4573fa349ef'
LEAGUE='simulation/NBA_2021_22_REGULAR_BASELINE.csv'
CAL='simulation/CHICAGO_2021_22_CALENDAR.csv'
M1='simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json'
HEALTH='simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json'
AUTH='canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json'
DET='simulation/CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS.json'
DETROLE='simulation/CHICAGO_DETROIT_2021_TWO_DATE_WORKING_EXECUTION.json'
DETLAW='research/DETROIT_2021_A_ROUTINE_OPERATING_EXECUTION_FAMILY_2026_10_07.json'
DETSELECT='simulation/DET_ROUTINE_OPERATING_FAMILY_SELECTION_2026_10_07.json'
TOR='simulation/CHICAGO_TORONTO_2021_22_SELECTED_BPM_RESULTS_2026_10_07.json'
TORLAW='simulation/TORONTO_2021_SELECTED_T1_OPERATING_FAMILY_2026_10_07.json'
NOPLATE='simulation/CHICAGO_NEW_ORLEANS_2022_LATER_SELECTED_KEEPER_RESULT.json'
UTALATE='simulation/CHICAGO_UTAH_2022_LATER_SELECTED_KEEPER_RESULT.json'
TEAM_FILES={
 'ATL':'ATLANTA','BOS':'BOSTON','BKN':'BROOKLYN','CHA':'CHARLOTTE',
 'CLE':'CLEVELAND','LAC':'CLIPPERS','DAL':'DALLAS','DEN':'DENVER',
 'GSW':'GOLDEN_STATE','HOU':'HOUSTON','IND':'INDIANA','LAL':'LAKERS',
 'MEM':'MEMPHIS','MIA':'MIAMI','MIL':'MILWAUKEE','MIN':'MINNESOTA',
 'NYK':'NEW_YORK','OKC':'OKLAHOMA_CITY','ORL':'ORLANDO','PHI':'PHILADELPHIA',
 'PHX':'PHOENIX','POR':'PORTLAND','SAC':'SACRAMENTO','SAS':'SAN_ANTONIO',
 'WAS':'WASHINGTON'}
TEAM_FILES={k:f'simulation/CHICAGO_{v}_2021_22_SELECTED_KEEPER_RESULTS.json' for k,v in TEAM_FILES.items()}
TEAM_FILES.update(UTA='simulation/CHICAGO_UTAH_2021_SELECTED_KEEPER_RESULT.json',
 NOP='simulation/CHICAGO_NEW_ORLEANS_2021_SELECTED_KEEPER_RESULT.json',
 DET='simulation/CHICAGO_DETROIT_2022_LATER_SELECTED_KEEPER_RESULTS.json',TOR=TOR)
FILES=list(dict.fromkeys([LEAGUE,CAL,M1,HEALTH,AUTH,DET,DETROLE,DETLAW,DETSELECT,TORLAW,NOPLATE,UTALATE,*TEAM_FILES.values()]))
PINS={'simulation/NBA_2021_22_REGULAR_BASELINE.csv': '92869bc987896a4172c5e54e3684d2604c5c24d828e9bcf3cc27af30ebc83644', 'simulation/CHICAGO_2021_22_CALENDAR.csv': 'c59ea19a5515d64ed03cae8e0481847b6572d4087bbcefef15896bb7a2489183', 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json': '73d51b630e9c9d4ec31b7e3952906165589bd8c49a48bb07c79bdc9ad02e8fca', 'simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json': '274a35e163c7f6fd7f0d3e5494b3c46753aaf9900036676be935f17a9d538c32', 'canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json': '51b24c8a6bc1eb703568adced46b3ffa15845e85e8da10da1242bddf941df960', 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS.json': '66c1c862a179648aa72dd81ff13a07345b36889043995ecb583ae57019618c80', 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_WORKING_EXECUTION.json': 'fc44fe1b28318c2004529fc68a3b3d6b090f9b3a100265ca5e9517c0da3676b3', 'research/DETROIT_2021_A_ROUTINE_OPERATING_EXECUTION_FAMILY_2026_10_07.json': '855371610d0f2b776b773bdf2ff02f27a43684b6c1407b1d54f698c6e0f093ef', 'simulation/DET_ROUTINE_OPERATING_FAMILY_SELECTION_2026_10_07.json': '9f9c307f33975de3b3c05734e41f8401cad0439f0446f7bc87aa21d8c7752dc2', 'simulation/TORONTO_2021_SELECTED_T1_OPERATING_FAMILY_2026_10_07.json': '676cb350acdd632dfc0a0b4cc82d8f1d085b243f21fe511caeb11bcc2b993118', 'simulation/CHICAGO_NEW_ORLEANS_2022_LATER_SELECTED_KEEPER_RESULT.json': '3fdbe7820b77264834d386ad0e4f1a4f18d46b75583cc34bfae957ff6bc1fa89', 'simulation/CHICAGO_UTAH_2022_LATER_SELECTED_KEEPER_RESULT.json': '45f930a7982e8041d2d9aca9c844469fcb777a55cdaa1e40c53f202ac8ecc5bd', 'simulation/CHICAGO_ATLANTA_2021_22_SELECTED_KEEPER_RESULTS.json': 'cbba94c48498e68506c257e8b05116b6d8210acd64bda29063d20875b015d19c', 'simulation/CHICAGO_BOSTON_2021_22_SELECTED_KEEPER_RESULTS.json': '62dc644588257b0330e14aee478f6d4e37b1a127addadbfeb0415113199f23c1', 'simulation/CHICAGO_BROOKLYN_2021_22_SELECTED_KEEPER_RESULTS.json': 'b29b621991a541396e952d2cdbbceda1a9025bbc9bc79598b8da3c735ae5743a', 'simulation/CHICAGO_CHARLOTTE_2021_22_SELECTED_KEEPER_RESULTS.json': '2bd7be0084130c019d53b875591fdf07e55773ef3536f6c2e9b329c68c7e2b4a', 'simulation/CHICAGO_CLEVELAND_2021_22_SELECTED_KEEPER_RESULTS.json': '57c3f5255d1970638aa1cf575e5c526c58de9fb9a5ba2198347e33a100ff499b', 'simulation/CHICAGO_CLIPPERS_2021_22_SELECTED_KEEPER_RESULTS.json': 'e771fbe025fd8833c2418f2de89cd8fbd03cf4cd68f66051b20ab2a96416f143', 'simulation/CHICAGO_DALLAS_2021_22_SELECTED_KEEPER_RESULTS.json': 'c3024b2cd74bd61e2317d8e5ce925678305651ff5811a312a4611fe0206d696a', 'simulation/CHICAGO_DENVER_2021_22_SELECTED_KEEPER_RESULTS.json': 'a6c4a8fd934c3da9e0b78b767b33193ba8a922d85ed58071c5eec5afebd7f01d', 'simulation/CHICAGO_GOLDEN_STATE_2021_22_SELECTED_KEEPER_RESULTS.json': '6fdb37fda8b1b2f22fb17287f61af22d12039bcb8b65449550e6c0188a06cb3f', 'simulation/CHICAGO_HOUSTON_2021_22_SELECTED_KEEPER_RESULTS.json': 'b2ba4278dc1d6e25961ee9fa10d3dd0b0afd55d563088660b55f449c2badca0d', 'simulation/CHICAGO_INDIANA_2021_22_SELECTED_KEEPER_RESULTS.json': '9e8358e08c41fd7cd99da99dc73618a6d1ed3d92a2de017fbc8aabf70d61965c', 'simulation/CHICAGO_LAKERS_2021_22_SELECTED_KEEPER_RESULTS.json': '69ba2ac011cfcb9b8e5a8230f5109109265825cdcd7192786007aa65eb908595', 'simulation/CHICAGO_MEMPHIS_2021_22_SELECTED_KEEPER_RESULTS.json': '074e8cf4ddd60fcd1f3752985626f654bad5e9fa326e2f0f07f1923ab069de1c', 'simulation/CHICAGO_MIAMI_2021_22_SELECTED_KEEPER_RESULTS.json': '5864b0a89f674f89a2fe081be3529fb69d4081e1b6938a27c36289f509e1fd8f', 'simulation/CHICAGO_MILWAUKEE_2021_22_SELECTED_KEEPER_RESULTS.json': 'fcb8298501701dc21bef9199ffac2d10456384f808ffe2a8b4222cd9e7b0e583', 'simulation/CHICAGO_MINNESOTA_2021_22_SELECTED_KEEPER_RESULTS.json': '64e4cd9abddc2005fc06f621a24c9583eb51b4b99a9f9aa8f9d9a38b79e5fde9', 'simulation/CHICAGO_NEW_YORK_2021_22_SELECTED_KEEPER_RESULTS.json': '4ad346a5f58bbf125c7378cd6ac5fc1f347a8a5bfccb2ed70f6fe9df0bf6831f', 'simulation/CHICAGO_OKLAHOMA_CITY_2021_22_SELECTED_KEEPER_RESULTS.json': '6bd6b3a9aecfb2f24175b33c9e5868a490212b34234cb5872495a538620b99f3', 'simulation/CHICAGO_ORLANDO_2021_22_SELECTED_KEEPER_RESULTS.json': '0b028cd28271954dc78c547475f128457cc9194d08797787e7fcd4ebf619c147', 'simulation/CHICAGO_PHILADELPHIA_2021_22_SELECTED_KEEPER_RESULTS.json': '84b8e1126086dc68da0fec8f4c462dd0a4be74941deacf6ea687c201b0ed1206', 'simulation/CHICAGO_PHOENIX_2021_22_SELECTED_KEEPER_RESULTS.json': '25967455666a7e956ece57ab741d41c91359c028c6c96cac109261592028e2d0', 'simulation/CHICAGO_PORTLAND_2021_22_SELECTED_KEEPER_RESULTS.json': 'f3fb709734752810c1b79db46e3bfac2cb6109ceb83105038fef5684a49cbd92', 'simulation/CHICAGO_SACRAMENTO_2021_22_SELECTED_KEEPER_RESULTS.json': '9c16ce17d02ea5f4e7e4f308b8626e0c55f91e7e0e996ebda43d828bfb5d58cb', 'simulation/CHICAGO_SAN_ANTONIO_2021_22_SELECTED_KEEPER_RESULTS.json': '8a855d70fb97195e77caaca8062e093b7de2c9d2217c79c701fb4de1fd4fd14f', 'simulation/CHICAGO_WASHINGTON_2021_22_SELECTED_KEEPER_RESULTS.json': 'b6a69e452e3277ae92b4b535db5d7845046286e2548b70e829ae0874c87d505b', 'simulation/CHICAGO_UTAH_2021_SELECTED_KEEPER_RESULT.json': '0e2bb3a05a9e562872dcdb411f061693d55d8bfa408a9f8c7927a1a65eb8fc77', 'simulation/CHICAGO_NEW_ORLEANS_2021_SELECTED_KEEPER_RESULT.json': 'd1975077c8879807d63763d77d58a2d89f8b481ec6c2964f0a6a9bf7a96138fd', 'simulation/CHICAGO_DETROIT_2022_LATER_SELECTED_KEEPER_RESULTS.json': 'e36230ee245762be758b81991d1f5d1f1136103ae01e5eee0dd5e7c318cc00fb', 'simulation/CHICAGO_TORONTO_2021_22_SELECTED_BPM_RESULTS_2026_10_07.json': '333f5bd496ed59260d21e26bb42615b13cb0a11560409a798c9f905cfe66dac6'}
MEANING={'simulation/NBA_2021_22_REGULAR_BASELINE.csv': '8d07a7ba2485a7a0fceeeb2ccfff7acfa1db394f4918459ec4fe30caef2bc4e6', 'simulation/CHICAGO_2021_22_CALENDAR.csv': '1c6d8cf8284dc3f88c0d6c7a2a7927f6ba0eb756fbf367da2a44fbfb402e7f68', 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json': '12456392c139ca9dbb71070e0a574d633728691d477eada592fd03cefc535cb9', 'simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json': 'b42cfb6e0b895fb6a70eb1a9e32798eb0cda27b98a659b6e4e6fce85a7d431f7', 'canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json': '963c5b9d2967f70cf5770349df39f44f88878e4a3e884b7e0c3c103d7699c6be', 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS.json': '04d2919b0c1525d0c00d40f7974e8fefd41ed931a1a18495f01b99d98270c317', 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_WORKING_EXECUTION.json': 'ec3f7b98866cf36b7e839a1d4b6d11a5c9997de8687d055916e0defe6bf0d21d', 'research/DETROIT_2021_A_ROUTINE_OPERATING_EXECUTION_FAMILY_2026_10_07.json': 'f377c94a47f0bed93596fb65f8a24fdc2238a768f3ec3e243f4643cfb07b10b1', 'simulation/DET_ROUTINE_OPERATING_FAMILY_SELECTION_2026_10_07.json': 'dc4c58de7e08f574f079b9596c1392ca2434fdae6f07b1b8d8c9ed7bbe3e32dd', 'simulation/TORONTO_2021_SELECTED_T1_OPERATING_FAMILY_2026_10_07.json': '7e1558e6ed3e00caebbc54495c4f19773b69deaa7971c1b90dd661f8be5dad3f', 'simulation/CHICAGO_NEW_ORLEANS_2022_LATER_SELECTED_KEEPER_RESULT.json': '2089ec7fe50dbbaf9f1ae77db28a81da78ac42b79389851c4da667d15a6f6391', 'simulation/CHICAGO_UTAH_2022_LATER_SELECTED_KEEPER_RESULT.json': '6988627361bb42f2dce4185f47c3c54d7a2d7e45cb9b1528455d4d79bde09c7b', 'simulation/CHICAGO_ATLANTA_2021_22_SELECTED_KEEPER_RESULTS.json': 'abaf8fe6dff30cd8beaecb4026c2f161c4ee081ee22b90e26fd98982bdb4493c', 'simulation/CHICAGO_BOSTON_2021_22_SELECTED_KEEPER_RESULTS.json': 'e9ac21d26b83047c97d4aef437395b131bb3f218b78022ce7eb291dd4f7c9355', 'simulation/CHICAGO_BROOKLYN_2021_22_SELECTED_KEEPER_RESULTS.json': 'f1bd95da027cf1b247960290fec4c0ac5d182abdc7235332fd4983ace5c3cbf4', 'simulation/CHICAGO_CHARLOTTE_2021_22_SELECTED_KEEPER_RESULTS.json': '5fcd16c785f16d87415ab9b13a0ffcbffd026a6f25640658861a6ca89721c2d7', 'simulation/CHICAGO_CLEVELAND_2021_22_SELECTED_KEEPER_RESULTS.json': 'bab68853e43260ae13f77f11ad738b1e0467ead24ee8806906bb8752fc884eae', 'simulation/CHICAGO_CLIPPERS_2021_22_SELECTED_KEEPER_RESULTS.json': '61d9825233e60536846906c73dd1b545281331434166e6b96cbaf74f929c26cd', 'simulation/CHICAGO_DALLAS_2021_22_SELECTED_KEEPER_RESULTS.json': 'e2164959da4257337af06baa0b5c94583ca0c91767476121169535ca18f8edc6', 'simulation/CHICAGO_DENVER_2021_22_SELECTED_KEEPER_RESULTS.json': '2ef8a8e501be3cb6764a1240082fb7a0d6096871202ea344de65c31b8eaa7b05', 'simulation/CHICAGO_GOLDEN_STATE_2021_22_SELECTED_KEEPER_RESULTS.json': '5294805ff22f15202cc87da8fc97061e413679811ec2b96686108565f086ceb3', 'simulation/CHICAGO_HOUSTON_2021_22_SELECTED_KEEPER_RESULTS.json': 'c733633bfff968959149cd89e4d3099483279ad603778e070f110682e8cd66e9', 'simulation/CHICAGO_INDIANA_2021_22_SELECTED_KEEPER_RESULTS.json': '9ed2c4959a43a8260cdec47631d0a5b7dd6ff68c24bafc0157223786d5d8bcc2', 'simulation/CHICAGO_LAKERS_2021_22_SELECTED_KEEPER_RESULTS.json': '8880f08a7281b1033c813571c07b74ae02dc6b43d62c3bee4ee21561a8dbb608', 'simulation/CHICAGO_MEMPHIS_2021_22_SELECTED_KEEPER_RESULTS.json': '641d6d63e319cd9987cf63b94fdb6e821e710215abb3187f13cdc31de8c69f8d', 'simulation/CHICAGO_MIAMI_2021_22_SELECTED_KEEPER_RESULTS.json': 'ae7358350a381712799df529bb7ed3dd00400541e8f587f14dec1653a2dca72f', 'simulation/CHICAGO_MILWAUKEE_2021_22_SELECTED_KEEPER_RESULTS.json': 'ce34af3e478b9c15424da46a02b896f3cf7da98e6c2226f975c49072d70ce24e', 'simulation/CHICAGO_MINNESOTA_2021_22_SELECTED_KEEPER_RESULTS.json': '1d81b28ece01357c8f4567a06e1edf9ba807eb969b4f1ef2ec5bbaeb93937079', 'simulation/CHICAGO_NEW_YORK_2021_22_SELECTED_KEEPER_RESULTS.json': 'b95cc223d094dc90561e44333e6728347e1c36af80396b899d01bbfcd2b286b6', 'simulation/CHICAGO_OKLAHOMA_CITY_2021_22_SELECTED_KEEPER_RESULTS.json': '18c5a9e3cbbfce13d9e99cf194ad4976935b617a5cd81889929d9d4056d433ff', 'simulation/CHICAGO_ORLANDO_2021_22_SELECTED_KEEPER_RESULTS.json': 'a3c1c8b0298008f0b02ae69dce9675c463a2040ee6ff2239233cf01e611ff1af', 'simulation/CHICAGO_PHILADELPHIA_2021_22_SELECTED_KEEPER_RESULTS.json': 'e040e8bfa9c14f7c4a801eeac15fb1b4240237139397d3a52a2db322ef279e20', 'simulation/CHICAGO_PHOENIX_2021_22_SELECTED_KEEPER_RESULTS.json': 'a1f1589688ff89201fc63edd8b1872d9af32acc6286d6c81e7d48bd502dbfaf8', 'simulation/CHICAGO_PORTLAND_2021_22_SELECTED_KEEPER_RESULTS.json': '8cf9f9c5704b6e6a301ba149c5a677828e42fd262e26793638fca8be0c66a1ef', 'simulation/CHICAGO_SACRAMENTO_2021_22_SELECTED_KEEPER_RESULTS.json': 'bd4fbd52cd8463bb7a3d4f4dd0b1c1a5ab3683bd05a7f0c3870e6d659f61e197', 'simulation/CHICAGO_SAN_ANTONIO_2021_22_SELECTED_KEEPER_RESULTS.json': '29e9566ef9c782a1c96fc73cbc8e29440e577919b65fc980229a5547be91673d', 'simulation/CHICAGO_WASHINGTON_2021_22_SELECTED_KEEPER_RESULTS.json': '44f76dbf612a662e02446093cec8e02bc5428d01955b93a8378f6423aaf638c3', 'simulation/CHICAGO_UTAH_2021_SELECTED_KEEPER_RESULT.json': '4d0981b4b75a3e18d0611e1b18529460326316ff810f3a37951cbe6f679feb4a', 'simulation/CHICAGO_NEW_ORLEANS_2021_SELECTED_KEEPER_RESULT.json': '5bd89b70fd046f758f6830f427502188efff74d6282c1172e1ca81d0164b3495', 'simulation/CHICAGO_DETROIT_2022_LATER_SELECTED_KEEPER_RESULTS.json': '78e2a109aa619d59b942c7c6dcb6ebea6d3a1345e65d6afb4984ac1f2cdb6059', 'simulation/CHICAGO_TORONTO_2021_22_SELECTED_BPM_RESULTS_2026_10_07.json': '8c0b973cee02c8177ac3d9ae832cde3c0cfb2bf6c99a905040589cd88f8180e5'}
ALIASES={'LaVine':'Zach LaVine','LaMelo_pick4':'LaMelo Ball','Coby':'Coby White',
 'Carter':'Wendell Carter Jr.','Young':'Thaddeus Young','Satoransky':'Tomas Satoransky',
 'Green':'Javonte Green','Caruso':'Alex Caruso','Markkanen':'Lauri Markkanen'}
POSITIONS={'PG','SG','SF','PF','C'}
POLICY={
 'model':'BPM_MAR25_EB_PLUS_HOME2_PLUS_B2B_HALF',
 'regulation_seconds':2880,'overtime_selected':False,'scores_selected':False,
 'contract_interval':'2021-10-19 through 2022-04-10, salary year 2021-22',
 'new_interval_family_selection':True,
 'new_midseason_assignments_or_waivers':False,
 'original_live_terms_selected_legal_UPCs_and_all_Gamma_preserved':True,
 'contracts_must_cover_consumed_dates_in_admitted_lawful_family':True,
 'old_claims_unpaid_bonus_waived_camp_stretch_FA_unsigned_exception_not_zeroed':True,
 'no_future_amendment_resolution_selected':True,
 'source_prior_only_dates_not_retroactively_whole_year_certified':True,
 'ordinary_teams':'New operational-availability/coach interval selection: same retained roster and selected positive rotation, no newly occurring contact injury modeled. This is not historical medical fact.',
 'GSW':'REHAB_OUT before 2022-01-14; KLAY_WORKING_RETURN from that selected anchor. Wiseman remains modeled absent. No real clinical certification.',
 'ORL':'BASE_ABSENT before 2022-01-23; RECOVERY from that selected anchor, not actual recovery dates.',
 'NOP':'ZION_OUT before 2022-03-24; ZION_WORKING_RETURN from selected late anchor. Original season absence is not imported.',
 'BKN':'IRVING_INSTITUTIONAL_OUT through 2021-12-17. From Dec18, AWAY_RETURN only for non-NYC, non-TOR US road dates with lawful host-access admitted condition; all BKN/NYK/TOR dates OUT. Later legal access expansion is not automatically participation.',
 'BKN_road_access':'Existing team road-policy/Chicago competitor exception template plus new lawful host-access/nonresident competition fiction condition, no vaccination or official receipt assertion.',
 'CHI':'Use canonical 58NORMAL/24COBY_OUT exact dated selection and current M1 Mark32/Caruso18/P32; no new CHI health selection.',
 'actual_private_medical_contract_or_receipt_certified':False,
 'new_author_lock_or_title':False,
}
FIXED_POLICY=deepcopy(POLICY)

def need(ok,message):
    if not ok:raise AssertionError(message)
def normalized(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(normalized(p).encode()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def direct(root,p):
    s=normalized(root/p)
    return json.loads(s) if p.endswith('.json') else list(csv.DictReader(io.StringIO(s)))
def physical(root,p):return direct(root,p)
def sources(root):
    need(POLICY==FIXED_POLICY,'Selected interval policy changed')
    out={}
    for p in FILES:
        need(sha(root/p)==PINS[p],'Physical source stale: '+p)
        x=physical(root,p)
        need(x==direct(root,p) and digest(x)==MEANING[p],'Returned physical source meaning changed: '+p)
        out[p]=x
    return out

def game_rows(d):
    if 'selected_games'in d:return d['selected_games']
    if 'selected_game'in d:return [d['selected_game']]
    if 'selected_result'in d:return [d['selected_result']]
    return d['rows']
def segments(g):return g.get('simultaneous_segments',g.get('paired_segments'))
def primitive(segs,team):
    blocks=[];clock=0;seconds=Counter();role=defaultdict(Counter)
    for s in segs:
        a,b=int(s['start_second']),int(s['end_second']);ps=s[team]
        need(a==clock and b>a and set(ps)==POSITIONS and len(set(ps.values()))==5,'Source clock/positions not 5 distinct')
        need(int(s['seconds'])==b-a,'Source clock length changed')
        clock=b
        blocks.append({'start_second':a,'end_second':b,'positions':deepcopy(ps)})
        for r,p in ps.items():seconds[p]+=b-a;role[r][p]+=b-a
    need(clock==2880 and sum(seconds.values())==14400,'Source regulation budgets changed')
    need(all(sum(v.values())==2880 for v in role.values()),'Source position budget changed')
    return blocks,dict(sorted(seconds.items())),{r:dict(sorted(v.items())) for r,v in sorted(role.items())}
def clock_projection(blocks):
    out=[]
    for b in blocks:
        if out and out[-1]['positions']==b['positions'] and out[-1]['end_second']==b['start_second']:out[-1]['end_second']=b['end_second']
        else:out.append(deepcopy(b))
    return digest(out)
def registration(d,g,team,src):
    if team=='TOR':r=src[TORLAW]['selected_roster']
    elif team=='NYK':r=g['selected_NYK_date_nomination']
    elif team=='NOP'and 'selected_date_role_and_availability'in d:r=d['selected_date_role_and_availability']['nominations']['NOP']
    else:r=d.get('selected_registration',d.get('dated_registration'))
    return {'standard':sorted(r['standard']),'TW':sorted(r.get('TW',r.get('two_way',[])))}
def rates_of(d):return d.get('selected_ratings',d.get('player_ratings',{}))
def compiled(src):
    templates={};rates={};anchors={};rosters={};selected={}
    for p in list(dict.fromkeys([DET,*TEAM_FILES.values(),NOPLATE,UTALATE])):
        for name,v in rates_of(src[p]).items():
            f=str(Fraction(v.get('exact_fraction',v.get('fraction'))))
            if name in rates:need(rates[name]['fraction']==f,'Conflicting selected productivity: '+name)
            else:rates[name]={'fraction':f,'source':p,'classification':v.get('classification')}
        for g in game_rows(src[p]):
            need(g['game_id']not in selected,'Duplicate selected CHI anchor')
            ss=segments(g)
            if ss is None and p==DET:ss=next(r for r in src[DETROLE]['rows']if r['game_id']==g['game_id'])['simultaneous_segments']
            if ss is None and p==TEAM_FILES['NOP']:ss=src[p]['selected_date_role_and_availability']['simultaneous_segments']
            need(ss is not None,'Selected CHI anchor has no clock')
            other=g['away']if g['home']=='CHI'else g['home']
            selected[g['game_id']]={'date':g['date'],'home':g['home'],'away':g['away'],'winner':g['selected_regulation_winner'],'source':p,'clock_projections':{t:clock_projection(primitive(ss,t)[0])for t in ('CHI',other)}}
    for team,p in TEAM_FILES.items():
        d=src[p];gs=game_rows(d)
        if team=='NOP':
            original=d['selected_date_role_and_availability'];g={**d['selected_result'],'simultaneous_segments':original['simultaneous_segments']};pairs=[('ZION_OUT',g,p,d)]
            late=src[NOPLATE];pairs += [('ZION_WORKING_RETURN',late['selected_games'][0],NOPLATE,late)]
        else:
            pairs=[]
            for g in gs:
                state=g.get(team+'_state','NORMAL')
                if not any(z[0]==state for z in pairs):pairs.append((state,g,p,d))
        for state,g,path,doc in pairs:
            b,secs,pos=primitive(segments(g),team);r=registration(doc,g,team,src)
            active=g.get(team+'_active')
            if team=='NYK':active=g['selected_NYK_date_nomination']['active']
            if team=='TOR':active=src[TORLAW]['selected_roster']['active']
            if team=='NOP'and state=='ZION_OUT':active=doc['selected_date_role_and_availability']['nominations']['NOP']['active']
            if active is None:active=doc.get('selected_registration',doc.get('dated_registration',{})).get('active')
            if active is None:active=sorted(secs)+[p for p in r['standard'] if p not in secs][:max(0,12-len(secs))]
            active=sorted(active)
            need(12<=len(active)<=15 and len(set(active))==len(active),'Source active nomination size')
            need(set(secs)<=set(active)<=set(r['standard']),'Source active ownership mismatch')
            need(all(p in rates for p in secs),'Missing selected positive productivity')
            key=team+':'+state
            templates[key]={'team':team,'state':state,'source':path,'source_game_id':g['game_id'],'blocks':b,'positive_player_seconds':secs,'role_player_seconds':pos,'registration':r,'active':active,'inactive':sorted(set(r['standard'])-set(active)),'zero_reserve_clinical_status':None,'actual_active_or_medical_certified':False}
            if team in rosters:need(rosters[team]==r,'State changes retained roster unexpectedly')
            rosters[team]=r
    m1=src[M1]['rows'];chitemplates={}
    for state in ('NORMAL','COBY_OUT'):
        c=next(r for r in m1 if r['state']==state);a=0;ss=[]
        for b in c['unordered_regulation_blocks']:
            n=int(b['minutes']*60);ss.append({'start_second':a,'end_second':a+n,'seconds':n,'CHI':b['positions']});a+=n
        b,secs,pos=primitive(ss,'CHI');r={'standard':sorted(c['standard_registered_candidate']),'TW':sorted(c['two_way_registered_candidate'])}
        templates['CHI:'+state]={'team':'CHI','state':state,'source':M1,'source_game_id':c['game_id'],'blocks':b,'positive_player_seconds':secs,'role_player_seconds':pos,'registration':r,'active':sorted(c['working_active_nominees']),'inactive':sorted(c['standard_inactive_nominees']),'unavailable':c['conditional_unavailable'],'zero_reserve_clinical_status':None,'actual_active_or_medical_certified':False}
        rosters['CHI']=r
    need(len(selected)==82 and set(selected)=={g['game_id']for g in src[CAL]},'Selected CHI82 coverage changed')
    need(len(rosters)==30,'Thirty roster families not compiled')
    for t,r in rosters.items():need(14<=len(r['standard'])<=15 and len(r['TW'])<=2,'Roster slot range')
    catalog=defaultdict(list)
    for t,r in rosters.items():
        for klass,ps in r.items():
            for p in ps:catalog[ALIASES.get(p,p)].append({'team':t,'class':klass,'source_name':p})
    need(all(len(v)==1 for v in catalog.values()),'Duplicate selected owner')
    need(len(catalog)==459 and sum(len(r['standard'])for r in rosters.values())==445,'Owner catalog cardinality changed')
    return templates,rates,rosters,selected,dict(sorted(catalog.items()))

def selected_state(team,day,home,away,health):
    if team=='CHI':return health
    if team=='GSW':return 'REHAB_OUT'if day<'2022-01-14'else 'KLAY_WORKING_RETURN'
    if team=='ORL':return 'BASE_ABSENT'if day<'2022-01-23'else 'RECOVERY'
    if team=='NOP':return 'ZION_OUT'if day<'2022-03-24'else 'ZION_WORKING_RETURN'
    if team=='BKN':return 'IRVING_AWAY_RETURN'if day>='2021-12-18'and away=='BKN'and home not in ('BKN','NYK','TOR')else 'IRVING_INSTITUTIONAL_OUT'
    return 'NORMAL'
def team_view(team,g,templates,health):
    state=selected_state(team,g['date'],g['home'],g['away'],health)
    key=team+':'+state;v=templates[key]
    return {'team':team,'state':state,'template':key,'positive_player_seconds':deepcopy(v['positive_player_seconds']),'active':deepcopy(v['active']),'inactive':deepcopy(v['inactive']),'actual_medical_or_private_receipt':False}
def assert_view(v,team,g,templates,health):
    state=selected_state(team,g['date'],g['home'],g['away'],health);key=team+':'+state;t=templates[key]
    need(v=={'team':team,'state':state,'template':key,'positive_player_seconds':t['positive_player_seconds'],'active':t['active'],'inactive':t['inactive'],'actual_medical_or_private_receipt':False},'Returned dated template/state/ownership altered')
def selected_game(g,views,rates,played):
    day=date.fromisoformat(g['date']);prior=(day-timedelta(days=1)).isoformat()
    back={t:(t,prior)in played for t in (g['home'],g['away'])}
    impact={t:sum(Fraction(rates[p]['fraction'])*n/2880 for p,n in views[t]['positive_player_seconds'].items())for t in views}
    fatigue=Fraction(int(back[g['away']])-int(back[g['home']]),2)
    margin=impact[g['home']]-impact[g['away']]+2+fatigue
    need(margin!=0,'Exact tied proxy requires a finite result selection')
    return {'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'team_date_models':views,'weighted_BPM_fraction':{t:str(v)for t,v in impact.items()},'home_advantage_fraction':'2','back_to_back':back,'fatigue_fraction':str(fatigue),'exact_home_margin':str(margin),'selected_regulation_winner':g['home']if margin>0 else g['away'],'score':None,'overtime_selection':None,'historical_winner_used':False,'actual_game_or_medical_receipt_certified':False}
def assert_game(r,g,views,rates,played):
    # Caller arithmetic independent of the returned constructor, no recall.
    need((r['game_id'],r['date'],r['home'],r['away'])==(g['game_id'],g['date'],g['home'],g['away']),'Returned result date/actors changed')
    prior=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat()
    back={t:(t,prior)in played for t in (g['home'],g['away'])}
    sums={t:sum(Fraction(rates[p]['fraction'])*n for p,n in views[t]['positive_player_seconds'].items())/2880 for t in views}
    m=sums[g['home']]-sums[g['away']]+2+Fraction(int(back[g['away']])-int(back[g['home']]),2)
    need(r['weighted_BPM_fraction']=={t:str(v)for t,v in sums.items()}and r['exact_home_margin']==str(m)and r['selected_regulation_winner']==(g['home']if m>0 else g['away']),'Returned winner/model arithmetic changed')
    need(r['team_date_models']==views and r['back_to_back']==back and r['home_advantage_fraction']=='2'and r['fatigue_fraction']==str(Fraction(int(back[g['away']])-int(back[g['home']]),2)),'Returned model ingredients changed')
    need(r['score']is None and r['overtime_selection']is None and r['historical_winner_used']is False and r['actual_game_or_medical_receipt_certified']is False,'Actual score/OT/receipt promoted')

def build(root=ROOT):
    src=sources(root);templates,rates,rosters,anchors,catalog=compiled(src)
    schedule=src[LEAGUE];need(len(schedule)==1230 and len({g['game_id']for g in schedule})==1230,'League 1230-key domain changed')
    counts=Counter(t for g in schedule for t in (g['home'],g['away']));need(counts==Counter({t:82 for t in rosters}),'30x82 schedule changed')
    health={r['game_id']:r['selected_chicago_state']for r in src[HEALTH]['selected_dates']}
    need(src[AUTH]['selected']['selected_date_rows']['sha256']==PINS[HEALTH]and Counter(health.values())==Counter(NORMAL=58,COBY_OUT=24),'Canonical CHI health selection differs')
    played={(t,g['date'])for g in schedule for t in (g['home'],g['away'])};rows=[];records={t:{'played':0,'wins':0,'losses':0}for t in rosters}
    for g in schedule:
        hs=health.get(g['game_id']);views={}
        for t in (g['home'],g['away']):
            v=team_view(t,g,templates,hs);assert_view(v,t,g,templates,hs);views[t]=v
        r=selected_game(g,views,rates,played);assert_game(r,g,views,rates,played)
        if g['game_id']in anchors:
            a=anchors[g['game_id']];need((a['date'],a['home'],a['away'],a['winner'])==(r['date'],r['home'],r['away'],r['selected_regulation_winner']),'Existing CHI82 winner changed')
            need(all(clock_projection(templates[v['template']]['blocks'])==a['clock_projections'][t]for t,v in views.items()),'Existing CHI82 source role clock changed')
            r['existing_CHI_anchor']={'source':a['source'],'winner_conserved':True,'both_exact_position_clocks_conserved':True}
        else:r['existing_CHI_anchor']=None
        for t in views:
            records[t]['played']+=1;records[t]['wins']+=int(r['selected_regulation_winner']==t);records[t]['losses']+=int(r['selected_regulation_winner']!=t)
        rows.append(r)
    need(sum(r['wins']for r in records.values())==1230 and all(r['played']==82 and r['wins']+r['losses']==82 for r in records.values()),'Global records inconsistent')
    return {'id':'NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS','baseline_main':BASELINE,'status':'SELECTED_FICTIONAL_INTERVAL_FAMILY_1230_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'policy':deepcopy(POLICY),'owner_catalog':catalog,'team_rosters':rosters,'shared_role_templates':templates,'selected_productivity_inputs':rates,'rows':rows,'team_records':records,'summary':{'league_games':1230,'team_dates':2460,'team_families':30,'shared_role_templates':len(templates),'original_CHI_results_conserved':82,'new_non_CHI_model_results':1148,'historical_winners_copied':0,'standard_owners':445,'two_way_owners':14,'unique_named_owners':459,'duplicate_named_owners':0,'total_wins':1230,'total_losses':1230,'CHI_wins':records['CHI']['wins'],'CHI_losses':records['CHI']['losses']},'certification':{'new_delegated_operating_health_coach_and_result_family_selected':True,'source_prior_limited_scope_preserved':True,'independent_review_completed':False,'all_date_actual_contract_registration_medical_receipts_certified':False,'private_whole_ledger_or_future_resolution_absence_certified':False,'standings_tiebreak_play_in_playoff_or_2022_pick_selected':False,'whole_macro3_G13_G16_or_manuscript':False},'remaining_finite_consumers':['Conference/division records and actual applicable tie-break functions from these joint1230 outcomes; no historical conference order copy.','Play-in/playoff selected results and2022lottery/right-control settlement using contingent prior rights; no future actual pick rank/receipt invented.','Remaining2022-23 and2023 career/legal/event consumers.'],'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}

def validate(d,root=ROOT):return []if d==build(root)else ['Saved output differs from bound physical source/family']
def markdown(v):
    s=v['summary'];a=['# 2021–22 전역 정규시간 작업 결과','',f"30팀·1230키를 한 소비기로 계산했다. Chicago 기존82 결과 보존, 나머지1148은 같은 단일 Fraction/EB/BPM·홈2·연전0.5 모델의 새 위임 선택이다. 원역사 승자 복사0. 상태: **{v['status']}**.",'','## 새로운 날짜 범위 선택','',POLICY['contract_interval']+'의 명명된 live/선택UPC/원Γ를 보존하는 합법 가상 가족, 새중간양도·방출·resolution0을 선택한다. 기존 only2date 검문 자체를 연간 역사 인증으로 승격하지 않는다. 공개 합법 가족의 계약조건·서명/비용의무는 그대로이고 실제 계약서·접수·임상 인증false다.','',POLICY['ordinary_teams'],'',POLICY['GSW'],'',POLICY['ORL'],'',POLICY['NOP'],'',POLICY['BKN'],'',POLICY['BKN_road_access'],'','CHI58NORMAL/24COBY_OUT은 새선택 없이 현재canon을 그대로 소비한다. Mark32/Caruso18/P32·원82승자를 정확 검문했다.','',f"원소유 카탈로그: 30팀 STD{s['standard_owners']}+TW{s['two_way_owners']}=459명, 중복0. 부상0분·reserve는 임상null, 모든 양수는 선택가용/active소속을 검문한다. 각공유시계2880초/14400선수초·5역할을 물리source에서 재구축한다. 원NBA 실제 건강/능력/미래통계/점수/OT는 인증하지 않는다.",'','## 결과와 다음 유한 입력','','| 팀 | 승 | 패 |','|---|---:|---:|']
    a += [f"| {t} | {r['wins']} | {r['losses']} |"for t,r in sorted(v['team_records'].items())]
    a += ['','총승·총패 각각1230/각팀82. 이표는 기록이며 동률해소된 시드/포스트시즌/2022픽은 아직 아니다. '+ ' '.join(v['remaining_finite_consumers']),'','[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','','| 묶음 | 현황 |','|---|---|','| 1 드래프트 연쇄 | 완료 |','| 2 Chicago2020–21 | 완료 |','| 3 2021–23 거래·계약·시즌 | 82CHI·전역1230 작업결과, 순위/픽·후속시즌 미완료 |','| 4 장기 커리어 | 진행 |','| 5 결말·구조 | 기능43/후속 미완료 |','| 6 집필규격·ContextPack | source53/Pack0 |','| 7 통합·독립·작가승인 | 미완료 |','','미완료 큰묶음5/6번까지4. v0.30 PARTIAL·CLOSED·원고0. 작성자 검사는 독립 검문으로 계수하지 않는다.','']
    return '\n'.join(a)
def self_test():
    original=team_view
    def bad(t,g,ts,h):
        v=original(t,g,ts,h)
        if t=='GSW'and g['date']<'2022-01-14':v['state']='KLAY_WORKING_RETURN'
        return v
    with patch(__name__+'.team_view',side_effect=bad):
        try:build()
        except AssertionError:pass
        else:raise AssertionError('Returned dated recovery false-pass')
    original_result=selected_game
    def wrong(g,views,rates,played):
        r=original_result(g,views,rates,played);r['selected_regulation_winner']=g['away']if r['selected_regulation_winner']==g['home']else g['home'];return r
    with patch(__name__+'.selected_game',side_effect=wrong):
        try:build()
        except AssertionError:pass
        else:raise AssertionError('Returned winner false-pass')
    return 2
def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();v=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
    if a.check:need(direct(ROOT,OUT)==v and normalized(ROOT/MD)==markdown(v),'Saved global consumer stale')
    n=self_test()if a.self_test else None
    print(json.dumps({'current':True,'summary':v['summary'],'writer_controls':n}))
if __name__=='__main__':main()
