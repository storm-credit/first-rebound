"""A complete named #16 transaction candidate; no optional macro3 selection.

Keep frozen macro2 intact. Explicit guarantee/bonus amendments are proposals,
not recovered private terms. Old-year matching is not whole club-cost clearance.
"""
import argparse
import copy
import hashlib
import itertools
import json
import re
from datetime import date
from fractions import Fraction
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_2021_bos_okc_hou_pick16_working_execution.py'
OUT = 'research/NBA_2021_PICK16_BOS_OKC_HOU_WORKING_EXECUTION_2026_10_07.json'
MD = OUT[:-5] + '.md'
BASELINE = '6f5ec1afe5c06ff711e08a265a9b5002c4265118'
A3 = 'simulation/NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json'
ROSTER = 'simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json'
ASSET_INPUT = 'simulation/NBA_2021_DRAFT_ASSET_INPUTS.json'
ASSETS = 'simulation/NBA_2021_DRAFT_ASSETS.json'
G6 = 'simulation/NBA_2021_FIRST_ROUND_CONTINUATION_INPUTS.json'
G7 = 'simulation/NBA_2021_FULL_DRAFT_COMPARISON.json'
BOS = 'research/BOSTON_APRON_COMPONENT_BOUND_2026_10_05.json'
SOURCE_PINS = {'simulation/NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json': '3e35fd2abfeb32e2bc5b66b7796f843ca117359be1a419d037844d29177a26d8', 'simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json': 'cfa2f49bb82baa49b2298d90c97cd7fd8075e91380424d40bfd44772d8228a2b', 'simulation/NBA_2021_DRAFT_ASSET_INPUTS.json': 'a2ab7bbb933a62d091ac43d72bea2888704c937c287b1c4103c16b412b7ad3e2', 'simulation/NBA_2021_DRAFT_ASSETS.json': 'eb1f204a56ffea45a3153b1067954e96331f35cba5910651b1e18d724a8dcaeb', 'simulation/NBA_2021_FIRST_ROUND_CONTINUATION_INPUTS.json': '77c4fedd24bdbef4fdaa67be660adb2bffb36e2d252e7bdf2ecb7c3f694d94a1', 'simulation/NBA_2021_FULL_DRAFT_COMPARISON.json': '31e524c981a07240c835150e7db1d753191c92e205a03bc5207208aca07dbb8f', 'research/BOSTON_APRON_COMPONENT_BOUND_2026_10_05.json': 'e8280ee188c16b1ce118706d6c205ad8a214004372372b82c674b9f6942e8bc0', 'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2'}
RAW_DIR = Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-pick16-20261007')
CBA_PATH = Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
BYLAWS_PATH = Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-2019-bylaws.pdf')
GUIDE_PATH = Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-den-primary-2026-10-07/OKC_2122.pdf')
RAW = [
 ('OKC_KEMBA','OKC_KEMBA.html','https://www.nba.com/thunder/news/release-walker-210618','d41cda1e682ec217cd27ff843c986599fb5bc5fc59e5bf472a17fde27e3c4c6e'),
 ('OKC_SG16','OKC_SG16.html','https://www.nba.com/thunder/news/giddey-mann-robinson-earl-wiggins-210730','b51fd692fda32ddbd01695eafdd80dc55ac2efab30c7b3217631cb85fb0a4236'),
 ('HOU_SG16','HOU_SG16.html','https://www.nba.com/rockets/news/rockets-acquire-four-players-2021-nba-draft','cbfe21d38c0b193102d9e01fa8608d53b593ffdec65d177a2f68fc425b8178d3'),
 ('HOU_WOOD','HOU_WOOD.html','https://www.nba.com/rockets/news/rockets-acquire-christian-wood','3e963955e9e192ded639abb0eae680c3edc579fc2f676de409d9106a85977cad'),
 ('HOU_WALL','HOU_WALL.html','https://www.nba.com/rockets/news/rockets-acquire-five-time-all-star-john-wall','11948cef5133057d19530a2fa3c2e47a4309e03ea0bbfbfcd369f7f2786b0a71'),
 ('BROWN_STANDARD','BROWN_STANDARD.html','https://www.nba.com/news/thunder-sign-moses-brown-to-multiyear-contract','26fa8b416491702268e929bd54f91626643a029f2a078c344fc742de336cdd15'),
 ('HORFORD_SALARY','HORFORD_SALARY.html','https://www.salaryswish.com/players/al-horford','df0233292c839b7495adb866a52944bb67cfd7c04865500caf0dff6668fcce1e'),
 ('BROWN_SALARY','BROWN_SALARY.html','https://www.salaryswish.com/players/moses-brown','284f60e7833866bbd545cd75bac708cfbd9ab2b6110dea3f97ef36a117356658'),
 ('WALKER_SALARY','WALKER_SALARY.html','https://www.salaryswish.com/players/kemba-walker','ac7ce97eb94239bdf7fe2e6d62dd21e05a0373cd6b885b9e4738d2d6c8d0cd6a'),
 ('CALENDAR_CAP','CALENDAR_CAP.html','https://pr.nba.com/nba-salary-cap-for-2021-22-season-set-at-112-414-million/','0e070a33da4b25b142bd27d402d3ffea9d224cec0dab3f090d8e36fd20299abe'),
 ('CALENDAR_DRAFT','CALENDAR_DRAFT.html','https://pr.nba.com/2021-nba-draft-combine-lottery-dates/','69f5e3e2fb89e2220aeeecbc43db520ac0565ddb81278bdac32280aca296335e'),
]
PDF = [
 ('CBA',CBA_PATH,'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf','66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a',[37,40,49,53,64,65,233,234,236,240,241,248,252,286,398,399,412]),
 ('BYLAWS',BYLAWS_PATH,'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019.pdf','6accb3d9633e15e8559d13228c27ae7b3b0b81eac0894050b06256eea6da3464',[72,73,87]),
 ('OKC_GUIDE',GUIDE_PATH,'https://okcthunder.com/web-includes/ThunderMediaGuide2021-22.pdf','94848cbdf59427f2dcd04db56bc6f924be88787ec4c5f252d917d7b378524564',[49]),
]
EXPECTED_CLAIMS = [
 {'origin':'DET','first_protection_by_year':{'2022':16,'2023':18,'2024':18,'2025':13,'2026':11,'2027':9},'if_never_conveys':[{'year':2027,'round':2,'origin':'DET'}]},
 {'origin':'WAS','first_protection_by_year':{'2023':14,'2024':12,'2025':10,'2026':8},'if_never_conveys':[{'year':2026,'round':2,'origin':'WAS'},{'year':2027,'round':2,'origin':'WAS'}]},
]

def normalized(p):
    return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p): return hashlib.sha256(normalized(p).encode()).hexdigest()
def load(p): return json.loads(normalized(p))
def fraction_record(f):
    f=Fraction(f)
    return int(f) if f.denominator==1 else {'numerator':f.numerator,'denominator':f.denominator}

def raw_sources():
    from bs4 import BeautifulSoup
    observations=[]; bodies={}
    for ident,name,url,pin in RAW:
        p=RAW_DIR/name; raw=p.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==pin, 'Raw source changed: '+ident
        soup=BeautifulSoup(raw,'html.parser')
        if ident.startswith(('OKC_','HOU_')):
            node=soup.find('script',id='__NEXT_DATA__'); assert node
            props=json.loads(node.string)['props']['pageProps']
            # Team-site release text is embedded content, not the visible iframe.
            def search(o):
                if isinstance(o,dict):
                    if 'contentStructured' in o: return o['contentStructured']
                    for v in o.values():
                        found=search(v)
                        if found is not None:return found
                if isinstance(o,list):
                    for v in o:
                        found=search(v)
                        if found is not None:return found
                return None
            content=search(props); assert content is not None
            body=BeautifulSoup(json.dumps(content,ensure_ascii=False),'html.parser').get_text(' ',strip=True)
            extraction='HTML __NEXT_DATA__: recursive contentStructured; HTML tags removed'
        else:
            body=soup.get_text(' ',strip=True); extraction='BeautifulSoup full HTML text; historical contract table only'
        bodies[ident]=body
        observations.append({'id':ident,'url':url,'cache_path':str(p),'raw_sha256':pin,'bytes':len(raw),
          'classification':'PUBLIC_ORIGINAL_CONTRACT_REPORTING_NOT_CLUB_CERTIFICATE' if ident.endswith('SALARY') else 'PRIMARY_NBA_RELEASE',
          'extraction':extraction,'normalized_extracted_text_sha256':hashlib.sha256(body.replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()})
    anchors={'OKC_KEMBA':['Walker','Horford','Brown','2025','2023','most favorable','least favorable'],
      'OKC_SG16':['Houston','Detroit','Washington','16th'], 'HOU_SG16':['Sengun','Detroit','Washington'],
      'HOU_WOOD':['Detroit','future Detroit first','Wood'], 'HOU_WALL':['Washington','future first','Wall'],
      'BROWN_STANDARD':['March 28','multiyear','not released'],
      'HORFORD_SALARY':['27,500,000','27,000,000'], 'BROWN_SALARY':['1,250,000','1,701,593'],
      'WALKER_SALARY':['34,379,100','32,742,000','15%'],
      'CALENDAR_CAP':['12:01 a.m. ET','Aug. 3','112.414'],
      'CALENDAR_DRAFT':['July 29','8 p.m. ET']}
    for ident,tokens in anchors.items():
        for token in tokens: assert token.lower() in bodies[ident].lower(), 'Body anchor '+ident+':'+token
    page_text={}
    for ident,p,url,pin,pages in PDF:
        raw=p.read_bytes(); assert hashlib.sha256(raw).hexdigest()==pin, 'PDF source changed '+ident
        doc=fitz.open(stream=raw,filetype='pdf'); pages_meta=[]
        for number in pages:
            t=doc[number-1].get_text().replace('\r\n','\n').replace('\r','\n')
            page_text[ident,number]=t
            pages_meta.append({'pdf_page_one_based':number,'normalized_fitz_text_sha256':hashlib.sha256(t.encode()).hexdigest()})
        observations.append({'id':ident,'url':url,'cache_path':str(p),'raw_sha256':pin,'bytes':len(raw),
                             'classification':'PRIMARY_OFFICIAL_PDF','extraction':'PyMuPDF page.get_text(); newline normalized','pages':pages_meta})
    required={('CBA',40):['Exhibit 2','protected'],('CBA',236):['lesser of','subsequent Salary Cap Year'],
      ('CBA',248):['six (6) months','waive'],('CBA',252):['three (3)','December 15'],
      ('CBA',412):['twenty (20)','Two-Way'],('OKC_GUIDE',49):['draft pick (best','Dec. 8'],
      ('BYLAWS',87):['consecutive future NBA Drafts']}
    for key,tokens in required.items():
        compact=' '.join(page_text[key].split())
        for token in tokens: assert token in compact, str(key)+':'+token
    return observations

def sources(reader=load,hasher=sha):
    assert set(SOURCE_PINS)=={A3,ROSTER,ASSET_INPUT,ASSETS,G6,G7,BOS,'AGENTS.md'}
    for p,pin in SOURCE_PINS.items(): assert hasher(p)==pin,'Unreviewed source change: '+p
    return {p:reader(p) for p in SOURCE_PINS if p.endswith('.json')}

def matching_family(q,walker_bonus_waiver=True,brown_bonus_waiver=True):
    assert isinstance(q,int) and 423280<=q<=1701593,'Brown protection proposal outside sufficient family'
    assert walker_bonus_waiver is True, 'Walker bonus waiver is an explicit proposal prerequisite'
    assert brown_bonus_waiver is True, 'Existing Brown bonus, if any, must be waived in the proposed implementation'
    w,h,b=34379100,27500000,1250000
    floor=Fraction(w-100000)*4/5-27000000
    assert floor==423280
    c_ordinary=h+b; c_conservative=27000000+min(b,q)
    ordinary=Fraction(c_ordinary)*5/4+100000
    conservative=Fraction(c_conservative)*5/4+100000
    boston=Fraction(w)*5/4+100000
    assert ordinary>=w and conservative>=w and boston>=h+b
    return {'Brown_next_year_protected_credit_usd':q,'OKC_ordinary_capacity_usd':fraction_record(ordinary),
      'OKC_conservative_postseason_credit_usd':c_conservative,
      'OKC_conservative_capacity_usd':fraction_record(conservative),
      'OKC_conservative_margin_usd':fraction_record(conservative-w),'BOS_capacity_usd':fraction_record(boston),
      'BOS_incoming_public_base_usd':h+b,'BOS_base_matching_margin_usd':fraction_record(boston-h-b)}

def candidate_edges():
    return [
      {'event':'AP1','kind':'STANDARD_CONTRACT','asset':'Kemba Walker','from':'BOS','to':'OKC'},
      {'event':'AP1','kind':'STANDARD_CONTRACT','asset':'Al Horford','from':'OKC','to':'BOS'},
      {'event':'AP1','kind':'STANDARD_CONTRACT','asset':'Moses Brown','from':'OKC','to':'BOS'},
      {'event':'AP1','kind':'CURRENT_FIRST_SELECTION','asset':'BOS_2021_16','from':'BOS','to':'OKC'},
      {'event':'AP1','kind':'CONDITIONAL_SECOND_CLAIM','asset':'EARLIER_BOS_MEM_2025_2R','from':'BOS','to':'OKC'},
      {'event':'AP1','kind':'CONDITIONAL_SECOND_CLAIM','asset':'LATEST_OKC_WAS_EARLIER_DAL_MIA_2023_2R','from':'OKC','to':'BOS'},
      {'event':'SG16','kind':'UNSIGNED_DRAFT_RIGHTS','asset':'BOS_2021_16:Alperen Sengun','from':'OKC','to':'HOU'},
      {'event':'SG16','kind':'PRESERVED_CONDITIONAL_FIRST_CLAIM','asset':'DET_FIRST_OR_2027_SECOND','from':'HOU','to':'OKC'},
      {'event':'SG16','kind':'PRESERVED_CONDITIONAL_FIRST_CLAIM','asset':'WAS_FIRST_OR_2026_2027_SECONDS','from':'HOU','to':'OKC'}]

def draft_and_claims(s):
    origins=s[A3]['pick_control_snapshot']['rows']; assert len(origins)==60
    assert [(x['pick'],x['round']) for x in origins]==[(i,1 if i<=30 else 2) for i in range(1,61)]
    assert (origins[15]['origin'],origins[15]['control_holder'])==('BOS','BOS')
    assert s[G6]['asset_policy']=='AP1' and s[G6]['recommended_comparison']=='DB1'
    assert s[G6]['sengun_future_picks']==EXPECTED_CLAIMS,'Conditional protection template changed'
    g=s[G7]; assert g['recommended_comparison']=='DB1'
    db=next(x for x in g['scenarios'] if x['id']=='DB1')
    assert (db['board'][15]['pick'],db['board'][15]['team'],db['board'][15]['proposed_player'])==(16,'HOU','Alperen Sengun')
    projection=[]
    for current,b in zip(origins,db['board']):
        assert b['pick']==current['pick']
        holder='HOU' if current['pick']==16 else current['control_holder']
        assert holder==b['team'],'Unexpected optional control edge'
        projection.append({'pick':current['pick'],'round':current['round'],'origin':current['origin'],
          'frozen_macro2_holder':current['control_holder'],'conditional_after_AP1_holder':'OKC' if current['pick']==16 else current['control_holder'],
          'conditional_after_SG16_holder':holder,'draftee':'Alperen Sengun' if current['pick']==16 else None,
          'working_trade_candidate_only':current['pick']==16,'new_draft_author_lock':False})
    ap=next(x for x in s[ASSETS]['scenarios'] if x['id']=='AP1')
    assert ap['boston_kemba'] is True and ap['nop_mem'] is False
    assert ap['rows'][15]['owner']=='OKC' and ap['trade_legal_execution_verified'] is False
    claims=[dict(copy.deepcopy(c),claim_holder_before='HOU',conditional_claim_holder_after='OKC',
      current_underlying_future_pick_owner=None,actual_future_conveyance=None,source=G6,
      classification='EXISTING_PUBLIC_REPORTED_CONDITIONAL_TEMPLATE_PRESERVED_NOT_PRIVATE_TERMS_CERTIFICATE') for c in EXPECTED_CLAIMS]
    complement=[]
    for bos,mem in [(31,60),(60,31)]:
        sold=min(bos,mem); kept=max(bos,mem)
        assert sold!=kept
        complement.append({'BOS_2025_pick':bos,'MEM_2025_pick':mem,'candidate_OKC_earlier':sold,'preserved_ORL_later':kept})
    triple=[]
    for values in itertools.permutations(range(31,35)):
        okc,was,dal,mia=values; assets=[okc,was,min(dal,mia)]
        to_bos=max(assets); retained=[x for x in assets if x!=to_bos]
        assert len(retained)==2 and len(set(assets))==3
        triple.append({'rank_order_only_example':dict(zip(['OKC','WAS','DAL','MIA'],values)),
          'candidate_BOS_latest':to_bos,'preserved_OKC_other_two':retained})
    return projection,claims,complement,triple

def roster_projection(s):
    r=s[ROSTER]; states={}; removed=[]
    for club in ['BOS','OKC','HOU']:
        binding=max((x for x in r['team_game_bindings'] if x['team']==club),key=lambda x:x['date'])
        old=r['roster_states'][binding['state_id']]
        players=copy.deepcopy(old['players']); before=len(players)
        for x in list(players):
            expiry=x['working_expiry_inclusive']
            if expiry and expiry<'2021-07-28':
                assert (club,x['player'],expiry) in [('HOU','Cameron Oliver','2021-05-19'),('HOU','Cameron Reynolds','2021-05-23')]
                removed.append({'team':club,'player':x['player'],'working_expiry_inclusive':expiry,'dead_cost_not_removed':True});players.remove(x)
        states[club]={'source_last_game_date':binding['date'],'source_state_id':binding['state_id'],
          'carry_before_AP1':[{'player':x['player'],'contract_class':x['contract_class']} for x in players],
          'source_total_including_original_hardships':before,'new_intervening_contracts_assumed':False}
    wanted={'BOS':('Kemba Walker',),'OKC':('Al Horford','Moses Brown')}
    traded={}
    for club,names in wanted.items():
        players=states[club]['carry_before_AP1']; traded[club]=[]
        for n in names:
            obj=next(x for x in players if x['player']==n);assert obj['contract_class']=='STANDARD';traded[club].append(obj)
    for club in states:
        players=copy.deepcopy(states[club]['carry_before_AP1'])
        for x in traded.get(club,[]):players.remove(x)
        if club=='BOS':players+=copy.deepcopy(traded['OKC'])
        if club=='OKC':players+=copy.deepcopy(traded['BOS'])
        assert len({x['player'] for x in players})==len(players)<=20
        states[club]['conditional_after_AP1']=players
        states[club]['conditional_after_SG16']=copy.deepcopy(players)
        states[club]['count_including_two_way_after_AP1']=len(players)
        states[club]['candidate_draft_rights_not_signed_contract']=True
    assert {k:v['count_including_two_way_after_AP1'] for k,v in states.items()}=={'BOS':18,'OKC':16,'HOU':17}
    return states,removed

def build(reader=load,hasher=sha):
    s=sources(reader,hasher); raw=raw_sources()
    rows,claims,complement,triple=draft_and_claims(s)
    roster,expired=roster_projection(s)
    assert s[BOS]['arithmetic']['bounded_sum_usd']==138716242
    # Same old-cap-year contracts carried in this new candidate; not a claim
    # that the old March-May certificate already certified July registration.
    upper=138716242-34379100+27500000+1620564
    assert upper==133457706 and upper<138928000
    endpoint=[matching_family(q) for q in [423280,1250000,1701593]]
    return {'schema':'PICK16_COMPLETE_ACTOR_WORKING_CHAIN_V1','status':'INDEPENDENTLY_REVIEWED_WORKING_CANDIDATE',
      'baseline_main':BASELINE,'source_sha256':dict(SOURCE_PINS,**{SELF:sha(SELF)}),'source_hash_method':'UTF8 BOM stripped; CRLF/CR to LF',
      'raw_sources':raw,'authority':{'new_author_lock':False,'long_term_trade_direction_selected':False,
        'exact_financial_cents_selected':False,'actual_contract_amendment_or_consent_certified':False,
        'all_58_remaining_draftees_selected':False,'macro2_reopened':False,'macro3_complete':False,
        'whole_financial_or_registration_clearance':False,'new_REGISTER_promotion':False},
      'classification':{'completed_2021_06_18_and_2021_07_29_announcements':'FACT_ORIGINAL_HISTORY_ONLY',
        'new_dates_amendments_roster_carry':'EXPLICIT_WORKING_CANDIDATE',
        'future_ranks_delivery_options':'NOT_SELECTED'},
      'calendar':{'AP1_working_date':'2021-07-28','SG16_working_date':'2021-07-29',
        'salary_cap_year':'2020-21','cap_usd':109140000,'apron_usd':138928000,
        'new_salary_cap_year_start':'2021-08-03','original_AP1_announcement_date':'2021-06-18',
        'actual_execution_time':None,'source_date_not_copied_into_macro2':True,
        'July_carry_assumption':'No intervening optional contracts; expired named hardship contracts removed from roster but not cost. All three last modeled games precede July28.',
        'later_date_alternative':'After Aug3 requires new-year Salary/budget/q recalculation; not certified by this old-year model.'},
      'events':[{'id':'AP1','date':'2021-07-28','atomic':True,'edges':[e for e in candidate_edges() if e['event']=='AP1']},
        {'id':'SG16','date':'2021-07-29','atomic':True,'requires_available_draftee':'Alperen Sengun',
         'rights_selected_but_unsigned_in_this_candidate':True,'edges':[e for e in candidate_edges() if e['event']=='SG16']}],
      'proposed_matching_implementation':{
        'Brown_existing_current_salary_usd':1250000,'Brown_next_year_base_usd':1701593,
        'Brown_existing_current_protection_percent':100,'Brown_actual_next_year_protected_credit_usd':None,
        'Brown_agreed_next_year_protection_family_usd':[423280,1701593],
        'Brown_amendment':'II3(g) Exhibit2 lack-of-skill AND injury/illness protection-only increase. Retain prior greater protection, base salary, term, options and existing later conditional guarantees; no new salary/extension/bonus. All consenting implementations in this interval support matching.',
        'Brown_protection_category_percent_upper':100,
        'Walker_existing_trade_bonus_percent':15,'Walker_completed_2020_21_seasons_YOS':10,
        'Walker_old_year_35percent_cap_max_usd':38199000,'Walker_no_waiver_current_bonus_headroom_upper_usd':3819900,
        'Walker_voluntary_full_trade_bonus_waiver_proposed':True,'actual_Walker_waiver':None,
        'Walker_current_matching_salary_if_proposal_accepted_usd':34379100,
        'Walker_no_extension_or_renegotiation_before':'2022-01-28',
        'Walker_extension_restriction':'Later of 6months and first otherwise eligible date; no automatic extension on Jan28.',
        'Horford_current_salary_usd':27500000,'Horford_next_year_fully_protected_public_salary_usd':27000000,
        'Horford_new_trade_bonus_for_old_2019_contract':0,
        'Horford_bonus_reason':'XXIV2(a)(i): prior PHI→OKC assignment already occurred (guide Dec8); no new extension assumed, no repeat bonus.',
        'Brown_bonus_public_reported_baseline_usd':0,'actual_Brown_trade_bonus_certified':False,
        'Brown_voluntary_full_existing_trade_bonus_waiver_if_any_proposed':True,
        'Brown_actual_original_trade_bonus_amount':None,
        'Brown_waiver_reason':'Do not select original unknown bonus0: VII7(d)(3) agreed full waiver if the existing contract contains a bonus; absent-bonus branch has nothing to waive. Candidate matching/current apron then use original public base/cap without additional earned assignment bonus.',
        'Brown_no_extension_or_renegotiation_before':'2022-01-28',
        'Brown_extension_restriction':'Any waiver branch retains later of 6months and first otherwise eligible date; no automatic extension on Jan28. No-extension working path also preserves the zero-bonus branch.',
        'Brown_future_or_unreported_bonus_not_automatically_selected':True,
        'all_matching_cases':endpoint,
        'proof':'125%+100000 is available at either tax status. Conservative outgoing Horford27m+min(Brown1.25m,q); monotone in q, minimum423280 gives exactly Walker34,379,100. Ordinary current-credit regime also passes.',
        'unmodified_zero_credit_counterexample':{'Brown_next_credit_usd':0,'OKC_capacity_usd':33850000,'Walker_incoming_usd':34379100,'shortfall_usd':529100,'not_evidence_actual_trade_illegal':True},
        'aggregation_dates':{'Brown_signed_standard':'2021-03-28','Brown_three_month_wait_ends':'2021-06-28',
          'Horford_prior_acquired_guide_date':'2020-12-08','Horford_two_month_wait_ends':'2021-02-08',
          'Walker_prior_contract_2019_07_assignment':True},
        'cash_or_signing_bonus_added':False,'new_player_option_exercise_selected':False},
      'cost_boundary':{'BOS_preserved_old_year_carry_upper_usd':138716242,
        'Brown_young_FA_apron_floor_two_YOS_usd':1620564,'BOS_candidate_after_AP1_upper_usd':upper,
        'BOS_candidate_after_AP1_apron_margin_usd':138928000-upper,
        'BOS_scope':'New July preserved public contract-cost carry family only; ordinary unsigned pick/FA holds excluded from apron per VII6m3, RFA tender could require separate input if newly chosen.',
        'OKC_old_year_whole_apron_upper_usd':None,
        'OKC_cost_delta_public_base_usd':34379100-27500000-1250000,
        'OKC_cost_delta_if_outgoing_Brown_young_FA_floor_usd':34379100-27500000-1620564,
        'OKC_pretrade_apron_sufficient_upper_usd':138928000-(34379100-27500000-1620564),
        'OKC_hardcap_not_assumed_absent':True,
        'remaining_finite_financial_input':'Whole old-year OKC apron-adjusted retained live/dead cost bound, including Brown/Deck/CharlieBrown contract exception and all performance components. Matching does not fill this budget.',
        'HOU_SG16_current_contract_salary_delta_usd':0,'HOU_new_signed_rookie_contract':False,
        'future_guarantee_cost_q_interval_usd':[423280,1701593],'future_year_whole_team_budget_certified':False,
        'whole_3_team_cost_PASS':False},
      'dated_working_rosters':roster,'expired_hardship_contracts':expired,
      'draft_control_candidate_rows':rows,
      'conditional_return_claims':claims,
      'conditional_second_claims':{
        'BOS_MEM_2025':{'origin_pair':['BOS','MEM'],'ORL_preserved_claim':'later=max','candidate_OKC_transferred_claim':'earlier=min',
          'rank_order_examples_not_actual_future':complement,'BOS2027_ORL_claim_unchanged':True},
        'OKC_2023':{'source_components':['OKC_2023_2R','WAS_2023_2R','EARLIER_DAL_MIA_2023_2R'],
          'candidate_BOS_claim':'latest=max(OKC,WAS,min(DAL,MIA))','rank_order_examples_not_actual_future':triple,
          'primary_source_connection':'Thunder release least favorable of3; official guide49 positively records WAS and best(DAL,MIA) acquisitions.'}},
      'asset_law_boundary':{'current_2021_first_origin_unchanged':'BOS',
        'new_own_future_first_obligations_created':False,
        'DET_WAS_original_obligations_modified':False,'HOU_only_assigns_preexisting_acquired_claims':True,
        'Stepien_relation':'Preserve preexisting DET/WAS future allocation branches; holder substitution HOU→OKC creates no new origin obligation. AP1 current BOS first transfer must retain BOS2022 own first in the working family; source is the completed original bundle and preserved BOS future-first inventory.',
        'BOS2022_first_retained_candidate_requirement':True,'current_selection_then_draft_rights_treatment':True,
        'latest_named_future_pick_year':2027,'conservative_pre_2021_draft_latest_year':2027,
        'horizon_provenance':'Preserve the named original DET/WAS claim families actually acquired in2020 and reassigned in2021, including2027 second endpoints; no2028 obligation is created. Bylaws7.03 is Stepien, not an express seven-year horizon clause in the cached edition.',
        'future_exact_ranks_or_receipts_required':False,'actual_full_private_terms_certified':False,
        'protections_unchanged_source_templates':True,'original_transactions_completed_anchor_not_alt_consent':True},
      'summary':{'actors':3,'working_events':2,'named_asset_or_contract_edges':9,
        'conditional_control_matches_G7':60,'all_remaining_58_draft_selections':0,
        '2025_complement_order_examples':2,'2023_order_examples':24,
        'whole_cost_named_gap_count':1,'whole_trade_family_legal_clearance':False},
      'independent_review_completed':True,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False,
      'remaining_major_groups_snapshot':5,'final_episode_functions_snapshot':19}

def validate(value):
    try:
        assert value==build(),'Saved packet not exactly reproducible from reviewed sources'
        assert value['events'][0]['edges']==candidate_edges()[:6]
        assert value['events'][1]['edges']==candidate_edges()[6:]
        assert value['conditional_return_claims']==draft_and_claims(sources())[1]
        assert not any(value['authority'].values()), 'Scope promotion'
        return []
    except (AssertionError,KeyError,ValueError) as exc:return [str(exc)]

def markdown(d):
    return f'''# 2021 #16 BOS→OKC→HOU: 전체 거래 후보 실행 연결

**{d['status']}**. 원역사 완료는 사실, July28/29 실행·보장 조정·보너스 waiver는 후보입니다. AP1/DB1/SG16의 장기 방향이나 58명의 나머지 지명 선택을 확정하지 않습니다. 고정 기준 main `{BASELINE}`.

## 선수와 모든 대가

AP1: BOS→OKC Walker·BOS2021 #16·2025 BOS/MEM **앞선** 2R 청구, OKC→BOS Horford·Moses Brown·2023 세 청구 중 **가장 뒤** 2R. 기존 Fournier ORL2025 뒤청구 및 ORL2027 청구를 다시 지출하지 않습니다.

SG16: Sengun이 DB1에서 남는 조건으로 OKC→HOU #16 지명 후 미계약 권리, HOU→OKC 기존 DET/WAS 조건부 1R 청구. 보호·전환·선행 참조를 G6 템플릿 그대로 보존합니다. 현재 미래 원지명권 소유자/실제 전달 연도는 null이며 실제2021 draft를 다른 58명 선택의 근거로 복사하지 않습니다.

## 날짜·매칭·비용

후보 AP1 7/28, SG16 7/29는 새 macro3 일정입니다. 원역사6/18을 완료된 macro2에 삽입하지 않습니다. 2020–21 cap109,140,000/apron138,928,000을 적용하며 Aug3 뒤 날짜는 별도 새 연도 계산이 필요합니다.

Brown 공개 표준계약 당해 base1,250,000/차년도1,701,593. 다음 연도 보장 credit의 실제 원금은 미확인입니다. 보수적 postseason 매칭에서 Horford credit27,000,000과 Brown `min(1,250,000,q)`를 합산합니다. **q≥423,280**이면 125%+100,000으로 Walker34,379,100을 충족합니다. II3(g)의 합의된 Exhibit2 보호-only 증가 후보 q∈[423,280,1,701,593]를 제시하며, 기존 더 큰 보장을 줄이거나 기본급/기간/옵션/새 보너스를 바꾸지 않습니다. q=0 가정은529,100 부족하며 실제 불법의 증거가 아닙니다. 문자상 postseason 종료일과 변경된 cap calendar 해석이 달라도 이 보수적 credit 및 ordinary credit 두 경우를 함께 덮습니다.

July Walker의 완료10시즌을 시작9YOS와 혼동하지 않습니다. 35% max38,199,000이라 current bonus 여지가 있습니다. **명시적 자발적 full trade-bonus waiver 후보**로 current 매칭34,379,100을 만들며 VII7(d)(3)의 trade 후6개월 및 원래 자격일 중 늦은 날까지 extension/renegotiation 제한을 보존합니다. 실제 동의·면제·새 계약은 미인증입니다. Horford는 기존 계약 첫양도가 이미 완료돼 새 extension 없는 두 번째 양도에 기존 kicker를 다시 붙이지 않습니다. Brown 원보너스가 존재한다면 같은 조항으로 기존 full bonus를 자발적으로 면제하는 후보를 구성하며, 원보너스 미존재분기는 면제할 금액이 없습니다. 양쪽 Brown 분기 모두 새 extension/renegotiation을 추가하지 않고, 면제분기는 max(2022-01-28,원래 자격일) 후손 제한을 유지합니다. 기존 원Γ를0으로 추정하지 않습니다.

BOS 비용은 기존 March–May 공개 완전 비용 모델을 **새 July 동일 계약 carry 후보**에 적용한 계산입니다. Brown youngFA apron floor는 자기1YOS1,517,981 대신 2YOS1,620,564. Upper138,716,242−34,379,100+27,500,000+1,620,564=**133,457,706**, 여유**5,470,294**. 기존 증인이 July 실제 등록까지 인증했다는 뜻이 아닙니다. OKC base 순증가5,629,100(youngFA floor 포함 순증가5,258,536); whole old-year retained/live/dead/bonus 비용이 null이므로 **OKC pretrade apron upper≤133,669,464** 충분조건을 아직 판정하지 못합니다. Brown 다년 MLE에 따른 hardcap 가능성을 없다고 가정하지 않습니다. HOU SG16은 미계약 권리 양도로 당해 계약급여 증가0입니다.

## 등록과 권리 규칙

선택된 마지막 시즌 로스터에서 새 계약 없이 July로 carry하는 후보. HOU Oliver5/19·Reynolds5/23 만료를 제거하되 기존 비용은 제거하지 않습니다. AP1 뒤 BOS18/OKC16/HOU17(모두 TW 포함)은 XXIX off-season max20 이내. SG16은 신인 표준계약을 체결하지 않아 등록 수를 올리지 않습니다. Brown Mar28 표준계약→June28 3개월, Horford Dec8 첫취득→Feb8 2개월 후의 날짜이므로 해당 대기기간이 지났습니다. 실제 등록·의료·서류 완료는 false입니다.

Stepien은 새로운 DET/WAS 미래 지출을 만드는 것이 아니라 원보호/전환 객체의 수령자 변경을 검문합니다. AP1 후보는 BOS2022 1R 보존 조건을 명시하며 completed 원bundle과 동일 첫권리 의무를 유지합니다. 2025 두 순서·2023 24 순서 검산은 순위 상대관계 예시로 모든 미래 실제 순위를 선택하는 검산이 아닙니다. 2020 취득·2021 재양도 완료로 지지되는 기존 claim의 가장 늦은 말단2027을 보존하고, draft 이전에2028 신규 의무를 만들지 않습니다. 캐시 규약7.03은 Stepien 조항이며 명시적 seven-year 조항으로 잘못 인용하지 않습니다.

## 원천과 남은 최소 입력

[Thunder 원 AP1 완료](https://www.nba.com/thunder/news/release-walker-210618), [Thunder SG16 완료](https://www.nba.com/thunder/news/giddey-mann-robinson-earl-wiggins-210730), [HOU SG16 완료](https://www.nba.com/rockets/news/rockets-acquire-four-players-2021-nba-draft), [DET 청구 취득](https://www.nba.com/rockets/news/rockets-acquire-christian-wood), [WAS 청구 취득](https://www.nba.com/rockets/news/rockets-acquire-five-time-all-star-john-wall), [새 cap 적용일](https://pr.nba.com/nba-salary-cap-for-2021-22-season-set-at-112-414-million/), [드래프트일](https://pr.nba.com/2021-nba-draft-combine-lottery-dates/). iframe만 반환된 웹 읽기는 본문 근거로 계수하지 않고 실제 다운로드 HTML의 __NEXT_DATA__ contentStructured를 읽었습니다. 공식 CBA17쪽/규약3쪽/OKCguide49 및 공개 SalarySwish 원계약3표 SHA는 JSON에 있습니다. 팀 발표는 Brown 사적 금액을 공개하지 않았으며 SalarySwish 표는 공식 인증과 구분합니다.

실제 남은 금융 입력은 **OKC 동일 old-year 전체 비용 상단** 한 묶음입니다. BOS 비용/양측 매칭/양도대가/날짜별 max20/기존 보호 참조를 각각 완료해도 이를0으로 채워 whole3team 법적PASS로 승격하지 않습니다. 새로운 비공개 접수증이나 미래 실제 순번은 필수로 추가하지 않습니다. consequential AP1/SG16 거래방향 및 보호-only 금융 후보는 비교·검문 뒤 선택 대상이며 현재 미선택입니다.

독립 Codex 검문과 root 읽기 검문으로 이 작업 후보를 수용했습니다. 실제 raw14·원문·q/비용 산술 및 원Γ면제·순서·수령자·origin 의미 변조를 검문했습니다. 전체 금융·방향 선택은 수용 범위에 포함하지 않습니다. 생성기/검사는 새3파일에 한정되며 기존 중앙/원장·완료macro2를 수정하지 않았습니다.

## 현행 진행표 (고정 작업 시점)

[전체 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)

| 번호 | 단계 | 상태 |
|---|---|---|
|1|2020 드래프트 연쇄|완료|
|2|Chicago2020–21|선택 시즌·법적12/12·F5/5 A3/3 K4/4 완료|
|3|2021–23 거래·계약|Chicago2 working 지명·SQ1 입력 완료; 전체 비용·AP1/SG16 후보 미확정|
|4|장기 커리어|후속 시즌 설계 남음|
|5|결말·전체 구조|골격 완료; 전체 회차 기능 미완료|
|6|집필 규격·Context Pack|현행19 final functions; Pack0·추가 기능/인계 작업 진행|
|7|통합·독립·작가 승인|전체 최종 미완료|

미완료 큰 묶음 **5**, freeze **v0.30 PARTIAL**, 설계/원고 게이트 **CLOSED**, 새 원고 **0**.
'''

def self_test():
    good=build(); controls=[]
    changes=[('wrong_origin',lambda d:d['draft_control_candidate_rows'][15].update(origin='OKC')),
      ('missing_full_return',lambda d:d['events'][0]['edges'].pop()),
      ('wrong_SG16_return',lambda d:d['conditional_return_claims'][0].update(claim_holder_before='DET')),
      ('wrong_protection',lambda d:d['conditional_return_claims'][0]['first_protection_by_year'].update({'2027':8})),
      ('double_spend_ORL',lambda d:d['conditional_second_claims']['BOS_MEM_2025'].update(candidate_OKC_transferred_claim='later=max')),
      ('old_date_copied',lambda d:d['calendar'].update(AP1_working_date='2021-06-18')),
      ('wholecost_zero_fill',lambda d:d['cost_boundary'].update(OKC_old_year_whole_apron_upper_usd=0)),
      ('waiver_silent',lambda d:d['proposed_matching_implementation'].update(Walker_voluntary_full_trade_bonus_waiver_proposed=False)),
      ('Brown_waiver_silent',lambda d:d['proposed_matching_implementation'].update(Brown_voluntary_full_existing_trade_bonus_waiver_if_any_proposed=False)),
      ('old_YOS',lambda d:d['proposed_matching_implementation'].update(Walker_completed_2020_21_seasons_YOS=9)),
      ('authority_escalation',lambda d:d['authority'].update(all_58_remaining_draftees_selected=True))]
    for label,change in changes:
        bad=copy.deepcopy(good);change(bad);assert validate(bad),label;controls.append(label)
    try:matching_family(423279)
    except AssertionError:controls.append('one_dollar_below_guarantee_floor')
    else:raise AssertionError('q floor')
    changed=copy.deepcopy(load(G6));changed['sengun_future_picks'][0]['first_protection_by_year']['2027']=8
    def reader(p):return changed if p==G6 else load(p)
    try:build(reader=reader)
    except AssertionError:controls.append('source_same_id_wrong_protection')
    else:raise AssertionError('Source semantic guard')
    return controls

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
    d=build()
    if args.write:
        (ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if args.check:
        errors=validate(load(OUT));assert not errors,errors
        assert normalized(MD)==markdown(d),'MD stale'
    controls=self_test() if args.self_test else []
    print(json.dumps({'current':True,'status':d['status'],'summary':d['summary'],'negative_controls':controls},ensure_ascii=False))
