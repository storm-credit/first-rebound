"""Finite public OKC old-year cost family at the proposed AP1 July28 event.

The May26 public category model is preserved into this new working window,
not certified as Oklahoma City's actual July ledger. No private receipt gate.
"""
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from unittest.mock import patch
from bs4 import BeautifulSoup
import fitz
import build_2021_bos_okc_hou_pick16_working_execution as ap1

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_okc_2021_ap1_full_cost_family.py'
OUT = 'research/OKC_2021_AP1_FULL_COST_FAMILY_2026_10_07.json'
MD = OUT[:-5]+'.md'
BASELINE = 'db1a59ec55fcacf7bbbb042bb1b460ca5600fbad'
TEMP = Path('C:/Users/Storm Credit/AppData/Local/Temp')
SSDIR = TEMP/'first-rebound-okc-cost-20261007'
SS_INDEX_SHA = '4ee5bd579f2dadcd5379ffe8a599668f004981ad8585a905d2c7cdfec2a3bbe1'
BI = TEMP/'fr-okc-bi-2020-21-archive.html'
BI_SHA = '0fa4024ada9bd658b66d89d25cd14e44a2f5a7dbf139015f32d78b34d6e4ea94'
BI_URL = 'https://web.archive.org/web/20210625194118id_/https://www.basketballinsiders.com/oklahoma-city-thunder-team-salary/oklahoma-city-thunder-salary-archive-2020-21/'
BI_NEW = TEMP/'fr-okc-bi-20210706.html'
BI_NEW_SHA = '2c0b1646a0e8f8dfa15c64b805272ff66602294f4807e728722985b35795f90e'
SOURCE_FILES = [ap1.OUT, ap1.SELF, ap1.ROSTER, 'simulation/CAUSALITY_MODEL.md',
    'canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json',
    'control/CHICAGO_2020_21_D1_S2_PROTOCOL.md', 'AGENTS.md']
PINS = {'research/NBA_2021_PICK16_BOS_OKC_HOU_WORKING_EXECUTION_2026_10_07.json': '86b9989daa20eced72106c25b14fb8d8b3b32d201132a0b87ba466b0ce51fba0', 'tools/build_2021_bos_okc_hou_pick16_working_execution.py': '5570436100daf99fedd5f38f8a114dc558c7b40bfa365b60512cccbbf6ee9a47', 'simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json': 'cfa2f49bb82baa49b2298d90c97cd7fd8075e91380424d40bfd44772d8228a2b', 'simulation/CAUSALITY_MODEL.md': '00638830864e9503db4589464806cc0c4c0d94002b039a8bf661d96e6f6a7c45', 'canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json': 'e0d8ed1f82c494a3610a91c779eef5573737f9b818088c903786cb12afae7dc9', 'control/CHICAGO_2020_21_D1_S2_PROTOCOL.md': '18d92122c7dcc1e1fb91129aea342f16eb6f03875f3a5cf063c51d8b9f90f7c0', 'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2'}
CAP, APRON, FLOOR2, SUFFICIENT = 109140000, 138928000, 1620564, 133669464
LIVE = {'Al Horford':27500000,'Shai Gilgeous-Alexander':4141320,
    'Gabriel Deck':3870370,'Tony Bradley':3542060,'Aleksej Pokusevski':2964840,
    'Darius Bazley':2399160,'Ty Jerome':2303040,'Mike Muscala':2283034,
    'Kenrich Williams':2000000,'Theo Maledon':2000000,'Svi Mykhailiuk':1663861,
    'Isaiah Roby':1517981,'Luguentz Dort':1517981,'Moses Brown':1250000,
    'Charlie Brown Jr.':19804}
DEAD = {'Meyers Leonard':9400000,'Darius Miller':7000000,
    'Justin Jackson':5029650,'TJ Leaf':4326825,'Austin Rivers':3500000,
    'Josh Gray':1620564,'Admiral Schofield':1517981,'Zylan Cheatham':1445697,
    'Kyle Singler':999200,'Patrick Patterson':737067,'Frank Jackson':250000}
CAMP = {'Antonius Cleveland':1620564,'Melvin Frazier Jr.':1620564,
    'Jaylen Hoard':1445697,'Omer Yurtseven':898310,'Chasson Randle':1678854}
EXPIRED = [dict(player=p,occurrence=i,reported_current=99020)
    for p in ['Justin Robinson','Charlie Brown Jr.'] for i in [1,2]]
HOLDS = {'Nick Collison':1620564,'Deonte Burton':1620564,
    'Raymond Felton':1620564,'Norris Cole':1620564,'Jawun Evans':1445697,
    'Kevin Hervey':898310}
TPE = {'Chris Paul':908960,'Dennis Schroder':865853,'Ricky Rubio':850600,
    'Kelly Oubre':332940,'Steven Adams':27528088,'Danilo Gallinari':10100000,
    'Jalen Lecque':1517981,'Trevor Ariza':12800000,'George Hill':9590602}
SECOND_RIGHTS = ['Vit Krejci','Vasilije Micic','DeVon Hardin','Yotam Halperin',
    'Sofoklis Schortsanitis','Szymon Szewczyk','Paccelis Morlende','Abdul Shamsid-Deen']
SS_ALIAS = {'Al Horford':'al-horford','Shai Gilgeous-Alexander':'shai-gilgeousalexander',
    'Gabriel Deck':'gabriel-deck','Tony Bradley':'tony-bradley',
    'Aleksej Pokusevski':'aleksej-pokusevski','Darius Bazley':'darius-bazley',
    'Ty Jerome':'ty-jerome','Mike Muscala':'mike-muscala','Kenrich Williams':'kenrich-williams',
    'Theo Maledon':'theo-maledon','Svi Mykhailiuk':'sviatoslav-mykhailiuk',
    'Isaiah Roby':'isaiah-roby','Luguentz Dort':'luguentz-dort','Moses Brown':'moses-brown',
    'Charlie Brown Jr.':'charlie-brown-jr','Meyers Leonard':'meyers-leonard',
    'Darius Miller':'darius-miller','Justin Jackson':'justin-jackson','TJ Leaf':'tj-leaf',
    'Austin Rivers':'austin-rivers','Josh Gray':'josh-gray','Admiral Schofield':'admiral-schofield',
    'Zylan Cheatham':'zylan-cheatham','Kyle Singler':'kyle-singler',
    'Patrick Patterson':'patrick-patterson','Frank Jackson':'frank-jackson',
    'Antonius Cleveland':'antonius-cleveland','Melvin Frazier Jr.':'melvin-frazierjr',
    'Jaylen Hoard':'jaylen-hoard','Omer Yurtseven':'omer-yurtseven',
    'Chasson Randle':'chasson-randle','Justin Robinson':'justin-robinson'}
CBA_PAGES = [27,30,31,35,40,42,44,54,55,56,57,193,197,203,204,205,206,
    209,210,211,213,218,228,239,240,241,248,249,250,276,295,303,304,313,314,398,399,412]


def normalized(p):
    return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')


def sha(p): return hashlib.sha256(normalized(p).encode()).hexdigest()
def load(p): return json.loads(normalized(p))
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def amounts(s): return [int(x.replace(',','')) for x in re.findall(r'\$([\d,]+)',s)]


def raw_evidence():
    raw=BI.read_bytes();assert hashlib.sha256(raw).hexdigest()==BI_SHA
    soup=BeautifulSoup(raw,'html.parser'); body=soup.get_text(' ',strip=True)
    assert '(Updated on 5/26/21)' in body and 'Oklahoma City Thunder Salary Archive' in body
    assert 'First-rounders: None' in body and 'Trade Kickers None' in body
    assert 'Qualifying Offers None' in body
    assert 'Hard-capped by the Zylan Cheatham, Josh Gray and Kenrich Williams sign-and-trades.' in body
    table=[]
    for tr in soup.find('table').find_all('tr'):
        cells=[x.get_text(' ',strip=True) for x in tr.find_all(['td','th'])]
        if len(cells)==2: table.append(cells)
    expected=[['Name','2020-21']]
    # Source order is checked separately from the modeled canonical name aliases.
    financial=[x for x in table if x[1].startswith('$') and x[0]!='Total']
    assert len(financial)==30 and sum(amounts(x[1])[0] for x in financial)==95196515
    for player,value in {**LIVE,**DEAD}.items():
        key={'Charlie Brown Jr.':'Charlie Brown Jr'}.get(player,player)
        assert any(x[0].split(' (')[0]==key and amounts(x[1])==[value] for x in financial), player
    assert table[-1]==['Total','$95,196,515']
    raw_new=BI_NEW.read_bytes();assert hashlib.sha256(raw_new).hexdigest()==BI_NEW_SHA
    # This successful July body is deliberately not an old-cap-year salary input.
    index_raw=(SSDIR/'sources.json').read_bytes()
    assert hashlib.sha256(index_raw).hexdigest()==SS_INDEX_SHA
    index=json.loads(index_raw);actual={x['id']:x for x in index}
    used=[]; performances={}
    for player,slug in SS_ALIAS.items():
        row=actual[slug];b=Path(row['cache_path']).read_bytes()
        assert hashlib.sha256(b).hexdigest()==row['raw_sha256']
        s=BeautifulSoup(b,'html.parser')
        extracted=[' | '.join(t.stripped_strings) for t in s.find_all('tr') if '2020-21' in t.get_text()]
        assert extracted==row['rows'] and extracted, 'Contract row missing '+player
        item=copy.deepcopy(row);item['player']=player
        item['classification']='CURRENT_VENDOR_HISTORICAL_CONTRACT_TABLE_NOT_LEAGUE_LEDGER'
        item['collected_date']='2026-10-07';used.append(item)
        if player in LIVE:
            target=LIVE[player]
            chosen=[r for r in extracted if len(amounts(r))>=5 and amounts(r)[0]==target]
            assert chosen, 'Original live contract point not present '+player
            r=chosen[-1];cash=amounts(r)
            assert cash[-1]==0, 'New unreviewed Unlikely performance input '+player
            performances[player]={'cap_point':target,'source_contract_row':r,
                'reported_unlikely_reserved':cash[-1],
                'reported_likely_already_inside_cap_point':{'Tony Bradley':90250,'Aleksej Pokusevski':375000}.get(player,0)}
        if player in DEAD and player not in ['Kyle Singler','Patrick Patterson']:
            assert any(len(amounts(r))>=5 and amounts(r)[-1]==0 for r in extracted)
    # Positive finite contract endpoints: old ordinary claims have ended before
    # this capyear. Their named stretch is retained; no old guarantee=0 inference.
    singler=BeautifulSoup(Path(actual['kyle-singler']['cache_path']).read_bytes(),'html.parser').get_text(' ',strip=True)
    patterson=BeautifulSoup(Path(actual['patrick-patterson']['cache_path']).read_bytes(),'html.parser').get_text(' ',strip=True)
    assert 'Jul 9, 2015' in singler and 'Length : 5 years' in singler and '2019-20 W' in singler
    assert 'Jul 10, 2017' in patterson and '2019-20 W' in patterson
    for player,value in CAMP.items():
        needle={'Melvin Frazier Jr.':'Melvin Frazier Jr'}.get(player,player)
        assert f'Signed {needle} to a non-guaranteed ${value:,} minimum summer contract' in body
    return {'archive':{'id':'BI_OKC_2020_21_ARCHIVE','url':BI_URL,'cache_path':str(BI),
        'raw_sha256':BI_SHA,'bytes':len(raw),'http_status':200,
        'requested_timestamp':'20210706165256','actual_memento_datetime':'2021-06-25T19:41:18Z',
        'body_updated':'2021-05-26','salary_cap_year':'2020-21',
        'classification':'ORIGINAL_CONTEMPORANEOUS_PUBLIC_CATEGORY_MODEL_NOT_LEAGUE_LEDGER',
        'locators':['First static table:30 money rows/Total','Waived Players','Transactions',
            'Unsigned Draft Picks','Trade Kickers','Free Agents (with Cap Holds)','Qualifying Offers','Exceptions'],
        'observed_salary_rows':table,'body_text_sha256':hashlib.sha256(body.encode()).hexdigest()},
        'successful_july_page_not_used_for_old_year':{'cache_path':str(BI_NEW),'raw_sha256':BI_NEW_SHA,
            'url':'https://web.archive.org/web/20210706165256id_/https://www.basketballinsiders.com/oklahoma-city-thunder-team-salary/',
            'body_updated':'2021-07-02','rejection_reason':'New-year projection is not the old-year July28 whole ledger'},
        'contract_sources':used,'wrong_slug_responses_not_contract_evidence':[x for x in index if not x.get('rows')],
        'performances':performances,'positive_none_fields':['TradeKickers','QualifyingOffers','UnsignedFirstRounders']}


def rule_evidence():
    output=[]
    for ident,p,url,pin,pages in [
        ('CBA',ap1.CBA_PATH,ap1.PDF[0][2],ap1.PDF[0][3],CBA_PAGES),
        ('OKC_GUIDE',ap1.GUIDE_PATH,ap1.PDF[2][2],ap1.PDF[2][3],[49])]:
        raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==pin
        d=fitz.open(p);r=[]
        for n in pages:
            t=d[n-1].get_text().replace('\r\n','\n').replace('\r','\n')
            r.append({'PDF_1based':n,'text_sha256':hashlib.sha256(t.encode()).hexdigest()})
        output.append({'id':ident,'url':url,'cache_path':str(p),'raw_sha256':pin,
            'classification':'PRIMARY_ACTUAL_DOCUMENT_TEXT_READ','pages':r})
    calendar=next(x for x in ap1.RAW if x[0]=='CALENDAR_CAP')
    raw=(ap1.RAW_DIR/calendar[1]).read_bytes();assert hashlib.sha256(raw).hexdigest()==calendar[3]
    body=BeautifulSoup(raw,'html.parser').get_text(' ',strip=True)
    assert 'Tuesday, Aug. 3' in body and '112.414' in body
    output.append({'id':'NBA2021_CAP_START','url':calendar[2],'cache_path':str(ap1.RAW_DIR/calendar[1]),
        'raw_sha256':calendar[3],'classification':'PRIMARY_NBA_RELEASE_DIRECT_BODY_READ',
        'locator':'August3 new salary cap year; old-year AP1 dateJuly28 precedes it'})
    return output


def policy():
    return {'classification':'WORKING_LAWFUL_ROUTINE_IMPLEMENTATION_WITHIN_EXISTING_APPROVED_PORTFOLIO',
        'window':['2021-05-26','2021-07-28 AFTER_ATOMIC_AP1'],'salary_cap_year':'2020-21',
        'new_events_before_AP1':[],
        'preserved_live_contracts':copy.deepcopy(LIVE),'preserved_dead_points':copy.deepcopy(DEAD),
        'camp_full_cash_reservation':copy.deepcopy(CAMP),'no_new_grievance_resolution_selected':True,
        'legacy_future_stretch_additional_envelope':16371000,
        'new_QO_FirstRefusal_RequiredFirstTender_extension_renegotiation_buyout_or_loans':False,
        'new_draft_selections_before_July28':False,
        'Walker_existing_bonus_proposal':'FULL_CONSENSUAL_WAIVER_IF_EXISTS',
        'Brown_existing_bonus_proposal':'FULL_CONSENSUAL_WAIVER_IF_EXISTS',
        'Brown_next_year_protection_credit_family':[423280,1701593],
        'waiver_extension_renegotiation_floor':'max(2022-01-28,first_otherwise_eligible_date)',
        'unused_exception_treatment':'RESERVE_FULL_REPORTED_NOMINAL_NORMAL; EXCLUDE_ONLY_IN_APRON_VII6m3F',
        'actual_original_bonus_amounts':None,'actual_player_agreements_receipts':None,
        'new_author_draft_or_AP1_lock':False}


FROZEN_POLICY=copy.deepcopy(policy())


def checked_policy():
    p=policy();assert p==FROZEN_POLICY, 'Unreviewed working routine/contract input'
    assert p['preserved_live_contracts']==LIVE and p['preserved_dead_points']==DEAD
    assert p['camp_full_cash_reservation']==CAMP and len(CAMP)==5
    assert p['salary_cap_year']=='2020-21' and not p['new_events_before_AP1']
    assert p['Brown_next_year_protection_credit_family']==[423280,1701593]
    assert p['Walker_existing_bonus_proposal']==p['Brown_existing_bonus_proposal']=='FULL_CONSENSUAL_WAIVER_IF_EXISTS'
    assert p['waiver_extension_renegotiation_floor']=='max(2022-01-28,first_otherwise_eligible_date)'
    assert p['legacy_future_stretch_additional_envelope']==CAP*15//100
    return p


def fixed_inputs():
    assert set(PINS)==set(SOURCE_FILES)
    for p,pin in PINS.items():assert sha(p)==pin, 'Unreviewed repository source '+p
    prior=load(ap1.OUT);assert not ap1.validate(prior), 'AP1 source producer reconstruction failed'
    assert prior['calendar']['AP1_working_date']=='2021-07-28'
    assert prior['calendar']['new_salary_cap_year_start']=='2021-08-03'
    assert prior['cost_boundary']['OKC_pretrade_apron_sufficient_upper_usd']==SUFFICIENT
    assert prior['cost_boundary']['Brown_young_FA_apron_floor_two_YOS_usd']==FLOOR2
    roster=load(ap1.ROSTER)
    bindings=[b for b in roster['team_game_bindings'] if b['team']=='OKC']
    last=max(bindings,key=lambda b:b['date']);assert last['date']=='2021-05-16'
    state=roster['roster_states'][last['state_id']]
    aliases={'Charlie Brown Jr':'Charlie Brown Jr.'}
    standard={aliases.get(x['player'],x['player']) for x in state['players'] if x['contract_class']=='STANDARD'}
    tw={x['player'] for x in state['players'] if x['contract_class']=='TWO_WAY'}
    assert standard==set(LIVE) and tw=={'Josh Hall','Jaylen Hoard'}
    return prior,last,state


def cost_components():
    # Unlikely is reserved separately from CurrentSalary, where Likely already sits.
    table=sum(LIVE.values())+sum(DEAD.values())+sum(x['reported_current'] for x in EXPIRED)
    assert table==95196515
    # Replace every named zero/one YOS FA point below 2YOS. Full annual, not
    # prorated, Charlie Brown and each10day give deliberately broader upper sums.
    floors={n:FLOOR2-LIVE[n] for n in ['Isaiah Roby','Luguentz Dort','Moses Brown','Charlie Brown Jr.']}
    floors.update({n:FLOOR2-DEAD[n] for n in ['Admiral Schofield','Zylan Cheatham']})
    ten_day_extra=sum(FLOOR2-x['reported_current'] for x in EXPIRED)
    frank_extra=1678854-DEAD['Frank Jackson']
    extra={'young_FA_fullannual_floor_increments':sum(floors.values()),
        'four_expired_10day_fullannual_overreservation':ten_day_extra,
        'Frank_Jackson_full_original_current_base_grievance_reserve':frank_extra,
        'camp5_full_current_annual_cash_or_apron_floor_reserve':sum(max(v,FLOOR2) for v in CAMP.values()),
        'additional_prior_valid_stretch_annual_envelope':CAP*15//100,
        'all_reported_Unlikely_addition':0}
    upper=table+sum(extra.values());assert upper==129697595 and upper<=SUFFICIENT
    return table,floors,extra,upper


def build():
    p=checked_policy();prior,last,state=fixed_inputs();evidence=raw_evidence();rules=rule_evidence()
    table,floors,extra,upper=cost_components()
    assert all(x['reported_unlikely_reserved']==0 for x in evidence['performances'].values())
    ordinary_extra=sum(HOLDS.values())+sum(TPE.values())+3623000
    # Ordinary table point already contains signing/assignment allocations under
    # VII3b. Newly incoming Walker is the sole July delta; its legal waiver family
    # is proposed explicitly, never inherited as an actual negotiated fact.
    after=upper-LIVE['Al Horford']-FLOOR2+34379100
    assert after==134956131 and after<APRON
    pre_players=sorted(LIVE);post_players=sorted((set(LIVE)-{'Al Horford','Moses Brown'})|{'Kemba Walker'})
    dated=[]
    for ident,date,contract_players,apron_upper in [
        ('OKC_PUBLIC_OLD_YEAR_MODEL','2021-05-26',pre_players,upper),
        ('AP1_BEFORE','2021-07-28',pre_players,upper),
        ('AP1_AFTER_ATOMIC','2021-07-28',post_players,after)]:
        dated.append({'id':ident,'date':date,'cap_year':'2020-21',
            'standard_contract_players':contract_players,'two_way':['Jaylen Hoard','Josh Hall'],
            'offseason_total_including_TW':len(contract_players)+2,'offseason_maximum':20,
            'apron_upper_usd':apron_upper,'apron_margin_usd':APRON-apron_upper,
            'normal_conservative_upper_usd':apron_upper+ordinary_extra,
            'normal_to_apron_extra_is_actual_charge':False,
            'raw_point_is_whole_upper':False,'new_QO_or_FirstRefusal_or_RequiredFirstTender':False,
            'actual_registration_medical_or_private_fee_certified':False})
    return {'schema':'OKC_AP1_OLD_YEAR_FULL_PUBLIC_COST_FAMILY_V1',
        'status':'INDEPENDENTLY_REVIEWED_SOURCE_SUPPORTED_FULL_FAMILY_CANDIDATE',
        'baseline_main':BASELINE,'source_hash_method':'UTF8 BOM stripped; CRLF/CR to LF',
        'source_sha256':{**PINS,SELF:sha(SELF)},'raw_evidence':evidence,'primary_rule_sources':rules,
        'implementation':p,'last_selected_roster_binding':last,
        'scope':{'public_category_contract_family_preserved':True,
            'actual_July_ledger_or_absence_of_every_private_charge_certified':False,
            'arbitrary_unreported_future_settlement_events_included':False,
            'normal_TeamSalary_equals_apron_or_tax_salary':False,
            'old_year_only':'2020-21 through candidateJuly28; Aug3+ requires a new ledger',
            'no_original_June18_event_inserted_into_macro2':True,
            'AP1_SG16_author_selected':False,'macro3_complete':False,'season_complete':False,
            'REGISTER_promoted_here':False,'manuscript_permitted':False,'independent_review_completed':True},
        'categories':[
            {'id':'C1_CURRENT_LIVE','status':'CONSTRUCTED','reported_cap_by_player':LIVE,
             'source_likely_plus_currentSalary':evidence['performances'],
             'mapping':'VII3b/4a1 reported CurrentSalary includes prior allocated signing/assignment Salary. Preserve original named pre-divergence acquisitions; do not re-add their past kicker.'},
            {'id':'C2_NEW_AP1','status':'CONSTRUCTED_LAWFUL_IMPLEMENTATION_EXISTS',
             'incoming_base':34379100,'outgoing_Horford_apron':27500000,
             'outgoing_Brown_apron':FLOOR2,'delta_usd':5258536,
             'quantifier':'For every permitted existing Walker/Brown trade bonus, propose full consensual waiver when present; protect Brown q at least423280 under existing AP1 candidate. Exact consent/amount is unselected.',
             'six_month_constraint':p['waiver_extension_renegotiation_floor'],
             'Brown4year_MLE_hardcap_not_denied':True},
            {'id':'C3_DEAD_CAMP_GRIEVANCE','status':'CONSTRUCTED',
             'reported_dead_by_player':DEAD,'expired_10day':EXPIRED,
             'camp_full_cash_by_player':CAMP,
             'camp_full_cash_or_apron_floor_reserved':{n:max(v,FLOOR2) for n,v in CAMP.items()},
             'Frank_current_full_base_upper':1678854,
             'old_ordinary_endpoints':{'Kyle Singler':'2015-16 through2019-20, five-year original contract',
                 'Patrick Patterson':'2017-18 through2019-20, original three-year contract'},
             'additional_valid_future_stretch_upper':16371000,
             'stretch_scope':'VII7d6 valid prior stretched/former-player annual amount <=15% waiver-year cap; highest named prior cap109.14m. Extra16.371m is added on top of already reported Singler/Patterson amounts, deliberately double reserving them.',
             'grievance_scope':'All named current ordinary waiver annual amounts reserved at full public current base, including Frank rather than250k. Camp5 entire annual cash reserved even though Ex9/10 terminates before regular season. No new later unresolved settlement/award event selected; no factual zero-private-claim certificate.'},
            {'id':'C4_FA_UNSIGNED_RIGHTS','status':'CONSTRUCTED',
             'normal_FA_upper_by_player':HOLDS,'ordinary_FA_apron_excluded':'VII6m3D',
             'unsigned_first_reported_inventory':[], 'unsigned_second_rights':SECOND_RIGHTS,
             'second_rights_not_contracts':'VII4a4 unsigned1R charge distinction; no accepted second-round tender/new standard contract chosen before AP1',
             'new2021draft_beforeAP1':False,'no_new_QO_notice_before_AP1_selected':True,
             'next_year_Svi_QO_public_date':'2021-08-01 in original SalarySwish, not a July28 current-year financial selection'},
            {'id':'C5_TENDER_FLOOR','status':'CONSTRUCTED',
             'fullannual_young_FA_floor_increments':floors,'floor2':FLOOR2,
             'floor2_reused_from_reviewed_AP1_cost_boundary':True,
             'expired10day_fullannual_reserved_each':FLOOR2,
             'required_first_tender_inventory':[],
             'source_boundary':'Positive May26 None inventory + no new old-year first draft/event/tender beforeJuly28. July29 SG16 and all subsequent new capyear/draft contract costs excluded from this AP1 witness.'},
            {'id':'C6_EXCEPTIONS','status':'CONSTRUCTED',
             'full_nominal_TPE_reported':TPE,'nominal_BAE':3623000,'reported_remaining_MLE':0,
             'MLE_used_by':['Theo Maledon','Moses Brown','Gabriel Deck'],
             'normal_full_nominal_overreservation':sum(TPE.values())+3623000,
             'expiry_dates_not_certified':'Source has uncertain* dates; retain even ChrisPaul/Schroder nominal upper and do not infer their July expiration to0',
             'DPE_scope':'No named DPE awarded in the frozen source-supported category portfolio; no new application/acquisition is selected. This is a finite model boundary, not all-private-absence proof.',
             'apron_exception_removal':'VII6m3F excludes any deemed incorporated unusedexception from apron even if normal charge persists. Hardcap is retained, not inferred away.'}],
        'arithmetic':{'reported_table_point_usd':table,'extra_upper_by_component':extra,
            'OKC_pretrade_apron_upper_usd':upper,'sufficient_pretrade_usd':SUFFICIENT,
            'sufficient_pretrade_margin_usd':SUFFICIENT-upper,'post_AP1_apron_upper_usd':after,
            'post_AP1_apron_margin_usd':APRON-after,'cap_usd':CAP,'apron_usd':APRON,
            'whole_bound_is_reported_exact_sum':False,'unknowns_replaced_with_zero':False},
        'dated_states':dated,
        'lawful_family':{'continuous_Brown_protection_credit':[423280,1701593],
            'matching_reused_AP1_family':True,'all_bonus_waiver_branches_covered':True,
            'current_public_named_cost_intervals':'Every unresolved protected fraction/current camp or10day amount lies below its explicitly reserved fullannual upper; all listed performance inputs preserved.',
            'exact_actual_fees_guarantees_and_consents':None,
            'constructible_old_year_whole_apron_family':True,
            'whole_cost_candidate_pass':True,'author_chosen_exact_financial_terms':False},
        'summary':{'cost_categories':6,'dated_states':3,'standard_before':15,'TW_before':2,
            'standard_after':14,'TW_after':2,'remaining_named_cost_gaps':[],
            'new_legal_register_PASS':0,'whole_macro3_PASS':0}}


def validate(saved):
    try:
        current=build()
        assert saved==current, 'Saved source/amount/category/authority differs from exact reconstruction'
        assert len(saved['categories'])==6 and len(saved['dated_states'])==3
        assert all(x['offseason_total_including_TW']<=20 for x in saved['dated_states'])
        assert saved['arithmetic']['post_AP1_apron_upper_usd']<=APRON
        assert not saved['scope']['AP1_SG16_author_selected']
        return []
    except (AssertionError,ValueError,KeyError) as e:return [str(e)]


def markdown(o):
    a=o['arithmetic']
    return f'''# Oklahoma City AP1: July28 old-year 전체 비용 후보

Status: `{o['status']}`. 원 S2 공개 category/계약 family의 한정 구성 증인입니다. 실제July 원장·금액·선수동의/접수·AP1/SG16 선택·macro3 완료는 인증하지 않습니다. 원고 CLOSED.

## 날짜·원천과 포트폴리오

[BI2020–21 원 archive]({BI_URL})는 **Updated2021-05-26**, Memento2021-06-25의 static 표로, Horford와Brown이 남는 old-year 모델입니다. 30 money rows/Total **95,196,515**와 방출14인·캠프5 계약·FA6인·unsigned1R/TradeKickers/QO의 명시 None을 실제 읽었습니다. 이 점 자체는 전체 법적 상단이 아닙니다. 성공 회수한 July6 일반페이지는 UpdatedJuly2 새 capyear projection이어서 old-year 숫자에 사용하지 않습니다.

기존 최종 OKC May16 working standard15/TW2를 candidateJuly28까지 새 사건 없이 보존하고, AP1을 원자적으로 적용하면 standard14/TW2=16, XXIX off-season20 이내입니다. 원June18 트레이드는 완료macro2에 넣지 않습니다. [NBA 새 capyear August3](https://pr.nba.com/nba-salary-cap-for-2021-22-season-set-at-112-414-million/) 이전 2020–21 cap109.14m/apron138.928m만 검문합니다. July29 draft/tender/계약이나 Aug3+ 비용은 이 증인의 범위 밖입니다.

## 여섯 비용 범주 전체 상단

|범주|공개 입력과 보수적 처리|
|---|---|
|C1 retained live/모든 성과·기존 assignment|15명 현재 Salary/cap point 보존. SS원계약 행의 likely Bradley90,250/Poku375,000은 이미 cap에 들어 있음. 각 원행의 unlikely 추가0은 긍정 vendor 입력이지 실제 사적 bonus 부재 인증이 아님. 기존 취득 bonus를 다시 가산하지 않음.|
|C2 AP1|Walker34,379,100 수취; Horford27.5m/Brown2YOS floor1,620,564 송출. 순증가5,258,536. Γ가 있으면 full consensual waiver인 허용 구현과 q≥423,280 보호-only 후보를 기존 #16 증인대로 사용.|
|C3 dead/camp/grievance|표의 dead11개·expired10day4개를 보존. Frank250k 대신 원 fullbase1,678,854까지 예약. camp5 fullannual 원현금7,263,989를 전액 유지하고 각2YOS apronfloor와 큰 값을 선택해 **8,161,110** 추가. Singler/Patterson ordinary계약은 각각2019–20 종료의 긍정 기간 근거; 기존 stretch 포함 표 위에 valid annual stretch16,371,000을 **추가** 예약. 미보고 새 settlement를 임의 만들지 않으며 실제 비공개 지불0 인증도 하지 않음.|
|C4 FA/unsigned|명명 FA6 hold는 normal에 포함, apron VII6m3D 제외. unsigned1R 명시None, unsigned2R8인 권리는 계약과 구분. 새 QO/FirstRefusal/계약을 AP1 앞에 추가하지 않는 routine 실행.|
|C5 tender/minimum|live youngFA4·waived youngFA2의2YOS fullannual floor 인상분과 Charlie·4 expired10day의 fullannual 과대예약. 기존미서명1R없음+AP1전새draft없음으로 RequiredFirstTender없음.|
|C6 unusedexceptions|보고 TPE9개·BAE를 normal에 전액 예약, 불확실한2020 연장/만료일을0으로 확정하지 않음. VII6m3F에 따라 apron에서만 제외. MLE사용Maledon/Brown/Deck을 긍정 보존, Brown다년MLE나 기존S&T hardcap을 부정하지 않음.|

CBA PDF240–241의 A–G 조정을 원문 대조했습니다. 추가 원SS32개 페이지와2021–22 Thunder guidePDF49 거래표, CBA{len(CBA_PAGES)}쪽의 raw/쪽 SHA·실패 별칭3을 JSON에 보존합니다. live/current allocation·camp/grievance/validstretch가 포함된 같은 old-year publiccategory family입니다. 임의 모든 미공표 미래분쟁이 이 가족에 무한 추가되는 것으로 재정의하지 않습니다. 새 긍정 비용 사건이 발견되면 해당 명명 입력을 재검문합니다.

## 계산과 법적 존재 범위

95,196,515 + youngFA floor **{a['extra_upper_by_component']['young_FA_fullannual_floor_increments']:,}** + expired10day fullannual 추가 **6,086,176** + Frank fullbase 추가 **1,428,854** + camp5 cash/floor **8,161,110** + 추가 validstretch **16,371,000** = **{a['OKC_pretrade_apron_upper_usd']:,}**.

충분조건133,669,464와의 여유 **{a['sufficient_pretrade_margin_usd']:,}**. AP1 뒤 **{a['post_AP1_apron_upper_usd']:,}**, apron 여유 **{a['post_AP1_apron_margin_usd']:,}**. Normal TeamSalary는 FA·unusedexceptions를 보수적으로 더한 별도 상단이며 이 apron 상단과 같다고 하지 않습니다. 과대예약분 제거를 필요로 하지 않습니다.

기존 계약의 허용 Γ 전범위에 대해 합의 fullwaiver가 존재하는 후보: 실제 Γ/q/동의/서류는 null. 면제분기는 기존 계약 extension/renegotiation을 max(2022-01-28,원래가능일) 전 금지. 일반 새 FA 계약과 자동 혼동하지 않습니다. 이것은 candidate 법적 구현 존재 검문이며 실제 선수 승낙의 예측이 아닙니다.

## 7행 진도

|번호|묶음|현재 상태|
|---|---|---|
|1|2020 드래프트 연쇄|완료|
|2|Chicago2020–21|S2 유한 공개family 완료, 실제인증 아님|
|3|2021–23 거래·계약|Chi A whole600 완료; #16 후보 OKC old-year 6범주 독립수용, 거래방향/후속실행 남음|
|4|장기 커리어|선행 계약 실행 의존|
|5|결말·전체 구조|working 골격; 현재 기능21 한정|
|6|집필 규격·Context Pack|진행; 원고 CLOSED|
|7|통합·독립·작가 승인|진행; final gate CLOSED|

미완료 주요 묶음5. 이 leaf의 원장 승격0/AP1 새 작가잠금0/전체macro3 PASS0.
'''


def self_test(o):
    checks=[]
    mutations=[('wrong_capyear',lambda x:x['dated_states'][1].update(cap_year='2021-22')),
        ('drop_camp',lambda x:x['categories'][2]['camp_full_cash_by_player'].pop('Chasson Randle')),
        ('young_FA_floor',lambda x:x['categories'][4].update(floor2=1517981)),
        ('actual_waiver',lambda x:x['lawful_family'].update(exact_actual_fees_guarantees_and_consents=0)),
        ('hardcap_denial',lambda x:x['categories'][1].update(Brown4year_MLE_hardcap_not_denied=False)),
        ('AP1_author_lock',lambda x:x['scope'].update(AP1_SG16_author_selected=True)),
        ('same_total_actor_swap',lambda x:x['categories'][0]['reported_cap_by_player'].update({'Moses Brown':27500000,'Al Horford':1250000}))]
    for label,fn in mutations:
        v=copy.deepcopy(o);fn(v);assert validate(v),label;checks.append(label)
    v=copy.deepcopy(FROZEN_POLICY);v['camp_full_cash_reservation'].pop('Omer Yurtseven')
    with patch(__name__+'.policy',return_value=v):
        try:build()
        except AssertionError:checks.append('constructor_drop_camp')
        else:raise AssertionError('Constructor accepted missing named camp cost')
    v=copy.deepcopy(FROZEN_POLICY);v['Walker_existing_bonus_proposal']='ASSUME_ORIGINAL_ZERO'
    with patch(__name__+'.policy',return_value=v):
        try:build()
        except AssertionError:checks.append('constructor_bonus_zero')
        else:raise AssertionError('Constructor accepted bonus0 inference')
    return checks


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true')
    parser.add_argument('--check',action='store_true');parser.add_argument('--self-test',action='store_true')
    a=parser.parse_args();o=build();assert not validate(o)
    j=json.dumps(o,ensure_ascii=False,indent=2)+'\n';m=markdown(o)
    if a.write:(ROOT/OUT).write_text(j,encoding='utf-8');(ROOT/MD).write_text(m,encoding='utf-8')
    current=True
    if a.check:current=normalized(OUT)==j and normalized(MD)==m;assert current, 'Artifact stale'
    tests=self_test(o) if a.self_test else []
    print(json.dumps({'current':current,'pretrade_apron_upper':o['arithmetic']['OKC_pretrade_apron_upper_usd'],
        'post_apron_upper':o['arithmetic']['post_AP1_apron_upper_usd'],
        'margin':o['arithmetic']['post_AP1_apron_margin_usd'],'categories':6,'dated_states':3,
        'negative_controls':tests,'REGISTER_promotions':0,'macro3_complete':False}))


if __name__=='__main__':main()
