"""Selected fictional credited-stat model and Coby ordinary-QO branch; no QO issuance."""
from __future__ import annotations
import argparse, copy, hashlib, json
from collections import Counter
from datetime import date
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import fitz
import build_coby_2023_ordinary_qo_function as coby
import build_chicago_2022_rookie_rfa_qo_family as pure

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2023_selected_stat_credit_and_qo.py'
OUT='simulation/CHICAGO_2023_SELECTED_STAT_CREDIT_AND_QO.json'
MD=OUT[:-5]+'.md'
CANON='canon/DELEGATED_CHICAGO_2023_STAT_CREDIT_MODEL_2026_10_08.json'
PORT='research/CHICAGO_2023_STAT_QO_AND_CBA_FINITE_PORTS_2026_10_08.json'
GLOBAL='simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json'
H22='simulation/CHICAGO_2022_23_SELECTED_DATED_ROLES.json'
P2022='simulation/PROTAGONIST_2022_QO_STARTER_JOIN.json'
M1='simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json'
QO='research/COBY_2023_ORDINARY_QO_FUNCTION_2026_10_07.json'
PRIMARY='research/COBY_2023_QO_PRIMARY_INPUT_2026_10_07.json'
BASELINE='31e424c1662f5fa03c2a27c9d0b3a88f8c420a78'
PINS={'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2', 'control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md': '91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d', 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json': '4ee9b74e37903a43b0bd50b35c7f24cbabdac13728097a848b553f874bbeef80', 'simulation/PROTAGONIST_2022_QO_STARTER_JOIN.json': 'dece52b96fa373af74e45674cc75ce888dbaca49c669c4b0aeeca02bad5f955f', 'research/COBY_2023_ORDINARY_QO_FUNCTION_2026_10_07.json': '5ee4c26f87c4e63b6cc812aff14382f2d1b522242707b5f65064b357f0522c54', 'research/COBY_2023_QO_PRIMARY_INPUT_2026_10_07.json': 'ee2c866fb0a098c1d09f43f2288b9df27f0d20db2c4630e99353fba95612eb2e', 'simulation/CHICAGO_2022_23_SELECTED_DATED_ROLES.json': 'c0650dbb07b75cc1523bf7ccc7f658576ac5b9a8784f1e80cc97178897703170', 'canon/DELEGATED_CHICAGO_2022_23_HEALTH_ROLES_2026_10_08.json': 'bf7bfdc1d64072196c1ec293c18c3410d722f67dd1a9014ef3d789999762bddf', 'simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json': '93264d2dff86a58ad10ca6975315c6c2167961f94f2517b6f5f79fa3113f2af8', 'research/MACRO3_2023_CBA_BOUNDARY_BRIDGE_2026_10_07.json': '404fde08b9d5fc9168b64f082c57a4ed6dff14711cf4d5990839267dc8a878f4', 'research/MACRO3_2023_CBA_BOUNDARY_PRIMARY_SOURCES_2026_10_07.json': '59b03c494187eb29177640806ae97427a837abff38bf4516f588758fc87a0112', 'simulation/CHICAGO_LONG_CORE_CBA_INPUTS.json': '7985e65cb5e184356aead888d4f016aca187dd2dd3185ea6de76527a6937fe0c', 'simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json': 'e7d0f4b15bc06c7cd16a38d158b38a78871fb7372d412639e33bb20c31d225a7', 'simulation/CHICAGO_2022_ROOKIE_OPTION_WINDOW_JOIN.json': 'e506efd28a54ceb61e34a8dfc107fb82236f783700f3aa610cd68ff4d62ba2cc', 'simulation/NBA_2022_SELECTED_FULL_POSTSEASON.json': 'b571c7645e006df1d63ead19e46343b4234034f10a9883539f52e0f9f7c7ff10', 'tools/build_coby_2023_ordinary_qo_function.py': 'ca95155db10345675254231c8b3bd2b53a5b9e70bbaaa000ffe947b3628a41da', 'reviews/CHICAGO_2022_23_SELECTED_DATED_ROLES_G11_INDEPENDENT_REVIEW_2026_10_08.json': 'bf867086e367fc90bf851c00cce2ac620e968b32c4a3ebc390a2e36b39a4e4e0', 'research/CHICAGO_2023_STAT_QO_AND_CBA_FINITE_PORTS_2026_10_08.json': 'ef82ac06ab1288cd95c9c415a32db62b1f1e9258d8fb1ed954cde7563aca7769', 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json': '73d51b630e9c9d4ec31b7e3952906165589bd8c49a48bb07c79bdc9ad02e8fca'}
STARTERS21=['LaMelo_pick4','LaVine','Protagonist','Markkanen','Carter']
STARTERS22=['LaMelo Ball','Zach LaVine','Protagonist','Lauri Markkanen','Wendell Carter Jr.']
POSITIONS=['PG','SG','SF','PF','C']


def need(v,m):
    if not v:raise ValueError(m)
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def direct(root,p):return json.loads(text(root/p)) if p.endswith('.json') else text(root/p)
def load(root,p):return direct(root,p)
def rat(v):return {'numerator':v.numerator,'denominator':v.denominator}

def sources(root):
    d={}
    for p,h in PINS.items():
        need(sha(root/p)==h,'Pinned physical source changed: '+p)
        d[p]=load(root,p)
        # Independent disk parse: patching load/direct cannot alter both comparisons.
        raw=text(root/p);actual=json.loads(raw) if p.endswith('.json') else raw
        need(d[p]==actual,'Returned physical source differs: '+p)
    return d

def policy():
    return dict(id='STAT23_A_ZERO_OT_BENCH',fictional_regular_seasons=['2021-22','2022-23'],
        overtime_periods_selected_per_regular_game=0,Coby_starter_nominations_per_game=0,
        fictional_credited_positive_regulation_participation=True,
        H22_positive_participation_policy_selected_for_all82=True,
        fourth_year_GP82_is_conditional_projection=True,
        fourth_year_all82_participations_executed_or_observed=False,
        source_lower_bounds_and_OTnull_preserved=True,
        unordered_or_coverage_clock0_is_official_starter_evidence=False,
        no_new_price_QO_issuance_acceptance_award_title_or_winner_selection=True)
FIXED_POLICY=copy.deepcopy(policy())

def primary_guard(src):
    p=src[PORT];reads=copy.deepcopy(p['primary_direct_reads']);bodies={}
    for a in reads:
        cache=Path(a['raw_cache'])
        need(hashlib.sha256(cache.read_bytes()).hexdigest()==a['raw_sha256'],'Primary raw bytes changed: '+a['id'])
        if 'directly_read_PDF_one_based_pages' in a:
            with fitz.open(cache) as doc:
                for n,h in a['current_fitz_text_LF_sha256'].items():
                    t=doc[int(n)-1].get_text().replace('\r\n','\n').replace('\r','\n')
                    need(hashlib.sha256(t.encode()).hexdigest()==h,'Primary extraction changed: '+a['id']+'/'+n)
                    bodies[(a['id'],int(n))]=' '.join(t.split())
        else:
            body=cache.read_text(encoding='utf-8-sig')
            need('July 1, 2023' in body and 'April 2023' in body,'NBPA effective periods changed')
    for key,words in {
        ('2017_CBA',310):['forty-one (41)','two thousand (2,000)','third and fourth Seasons'],
        ('2017_CBA',311):['Starter Criteria','fifteenth player','one hundred twenty'],
        ('2017_CBA',314):['Official NBA statistics','All other terms and conditions'],
        ('2017_CBA',315):['June 29','second Option Year'],
        ('2023_CBA',344):['October 1','July 13','Right of First Refusal'],
        ('2023_CBA',584):['Saturday, Sunday, or Federal Holiday','following business day']}.items():
        for w in words:need(w in bodies[key],'Primary operative rule differs: '+str(key)+'/'+w)
    return reads

def canonical(root):
    return dict(id='DELEGATED_CHICAGO_2023_STAT_CREDIT_MODEL_2026_10_08',baseline_main=BASELINE,
        status='ROOT_SELECTED_ROUTINE_FICTIONAL_STAT_CREDIT_PENDING_INDEPENDENT_REVIEW',
        authority='Existing health/season implementation delegation; root explicit STAT23_A instruction on2026-10-08',
        selection_instruction='Select two regulation-only fictional regular seasons, Coby bench GS0, positive participation credited: year3 GP58 MIN1044; year4 conditional GP82 MIN1476.',
        source_sha256={**PINS,SELF:sha(root/SELF)},hash_convention='UTF8 BOM strip; CRLF/CR to LF; raw external bytes separate',
        selected=FIXED_POLICY,
        source_generation_history='Existing lowerbound/OTnull/real-stat-false fields stay immutable; this distinct wrapper supplies explicitly chosen fictional statistics.',
        boundaries=dict(actual_NBA_GP_GS_minutes_box_or_clinical_certified=False,actual_private_receipt=None,
            QO_issuance_selected=False,player_acceptance_selected=False,exact_contract_price_selected=False,
            fourth_year_results_completed=False,whole_macro3_complete=False,author_locked=False,
            MVP_title_or_long_ending_changed=False,independent_review_completed=False),
        consumer=OUT,freeze='v0.30 PARTIAL',design_gate='CLOSED',Pack_count=0,manuscript_allowed=False)

def counts_from_blocks(blocks):
    counts=Counter();rolecounts={k:Counter() for k in POSITIONS};elapsed=0
    for b in blocks:
        s,e=b['start_second'],b['end_second'];need(type(s)is int and type(e)is int and s==elapsed and e>s,'Source regulation clock broken')
        pos=b['positions'];need(set(pos)==set(POSITIONS) and len(set(pos.values()))==5,'Source five positions invalid')
        for k,n in pos.items():counts[n]+=e-s;rolecounts[k][n]+=e-s
        elapsed=e
    need(elapsed==2880 and sum(counts.values())==14400,'Source regulation48/240 differs')
    need(all(sum(v.values())==2880 for v in rolecounts.values()),'Source position budget differs')
    return dict(counts),{k:dict(v) for k,v in rolecounts.items()}

def exposures(src):
    g=src[GLOBAL];h=src[H22];old=src[M1];p=src[P2022]
    need(p['routine_selection']['fourth_year_minutes_lower_bound']==2624 and p['routine_selection']['starter_criteria_selected']is True,'P2022 positive OR precedent changed')
    need(sum(r['selected_regular_P_seconds'] for r in p['dated_regular_witnesses'])==2624*60,'P2022 physical seconds changed')
    need('unordered_regulation_blocks' in old['rows'][0] and old['policy']['normal_role']=='M1_MARK32_CARUSO18_P32_NOT_OLD_R21A28_22','Old M1 coverage classification changed')
    need(old['policy']['OT_extension_selected']is False,'Old M1 OT generation history changed')
    templates={};witnesses=[]
    for state in ['NORMAL','COBY_OUT']:
        t=g['shared_role_templates']['CHI:'+state]
        c,roles=counts_from_blocks(t['blocks'])
        need(c==t['positive_player_seconds'] and roles==t['role_player_seconds'],'Source global CHI role totals differ')
        need(set(c)<=set(t['active'])<=set(t['registration']['standard']),'Source CHI participation/nomination membership differs')
        need([t['blocks'][0]['positions'][k] for k in POSITIONS]==STARTERS21 and 'Coby' not in STARTERS21,'Chosen year3 starter witness changed')
        templates[state]=t
        witnesses.append(dict(season='2021-22',state=state,selected_starting_nomination=STARTERS21,
            source_blocks=t['blocks'],source_block_count=len(t['blocks']),source_player_seconds=c,
            scope='Separate starting-consistent stat-credit witness with same source role/player budgets. Existing paired coverage arrays not overwritten or retroactively official GS.',
            actual_NBA_substitutions_or_starters_certified=False))
    t=h['selected_role_template'];c,roles=counts_from_blocks(t['ordered_regulation_blocks'])
    need(c==t['player_seconds'],'Source H22 player seconds differ')
    need(t['starters']==STARTERS22 and [t['ordered_regulation_blocks'][0]['positions'][k] for k in POSITIONS]==STARTERS22,'Source H22 fixed starting lineup conflicts with new GS0')
    need('Coby White' not in t['starters'] and c['Coby White']==1080,'Source H22 Coby18/bench changed')
    need(set(c)<=set(t['active_STANDARD'])<=set(t['registered_STANDARD']),'H22 positive membership changed')
    need(len(t['registered_STANDARD'])==15 and len(t['registered_TWO_WAY'])==2 and len(t['active_STANDARD'])==12,'H22 source15STD2TW/active12 changed')
    witnesses.append(dict(season='2022-23',state='H22_NORMAL_KESSLER12_REG48',selected_starting_nomination=STARTERS22,
        source_blocks=t['ordered_regulation_blocks'],source_block_count=len(t['ordered_regulation_blocks']),source_player_seconds=c,
        scope='Existing explicit selected starters and ordered first lineup; exact source budgets retained',actual_NBA_substitutions_or_starters_certified=False))
    third=[r for r in g['rows'] if 'CHI' in (r['home'],r['away'])]
    fourth=h['dated_rows'];need(len(third)==len(fourth)==82,'Each source season must have82 dates')
    need(len({r['game_id'] for r in third})==82 and len({r['calendar_key'] for r in fourth})==82,'Duplicate source dates')
    for r in third:
        x=r['team_date_models']['CHI'];t=templates[x['state']]
        need(x['positive_player_seconds']==t['positive_player_seconds'],'Dated year3 counts differ from selected template')
        need(x['active']==t['active'] and x['inactive']==t['inactive'],'Dated year3 nominations differ')
    for i,r in enumerate(fourth,1):
        need(r['team_game_number']==i and r['template']==h['selected_role_template']['id'],'Source H22 date/template join changed')
        need(r['H22_state_selected_for_date']is True and r['result']is None and r['overtime_periods']is None,'Source H22 participation/results generation boundary changed')
        need(r['regulation_elapsed_seconds']==2880 and r['regulation_team_seconds']==14400,'Source H22 clock budget changed')
    need(sum(r['team_date_models']['CHI']['positive_player_seconds'].get('Coby',0) for r in third)==1044*60,'Year3 Coby regulation1044 changed')
    need(sum(r['team_date_models']['CHI']['positive_player_seconds'].get('Coby',0)>0 for r in third)==58,'Year3 Coby GP58 source changed')
    need(len(fourth)*c['Coby White']==1476*60,'Year4 Coby regulation1476 changed')
    return third,fourth,witnesses

def row_expected(year,r,seconds):
    third=year==3
    return dict(season='2021-22' if third else '2022-23',RSC_year=year,
        key=r['game_id'] if third else r['calendar_key'],date=r['date'] if third else r['published_date'],home=r['home'],away=r['away'],
        source_state=r['team_date_models']['CHI']['state'] if third else r['template'],
        source_regulation_seconds=seconds,selected_fictional_OT_periods=0,selected_added_credited_seconds=0,
        selected_fictional_GP_credit=int(seconds>0),selected_fictional_GS_credit=0,
        selected_fictional_credited_seconds=seconds,
        credit_status='CHOSEN_FICTIONAL_CREDIT_OF_SELECTED_PARTICIPATION' if third else 'SELECTED_PARTICIPATION_POLICY_CONDITIONAL_CREDIT_PROJECTION',
        actual_future_all82_participations_observed_or_executed=False,
        current_selected_game_winner=r['selected_regulation_winner'] if third else None,
        winner_selected_by_this_stat_consumer=False,actual_NBA_statistics_certified=False)

def stat_row(year,r,seconds):return row_expected(year,r,seconds)

def summaries(rows):
    out=[]
    for year in (3,4):
        rs=[r for r in rows if r['RSC_year']==year]
        out.append(dict(season=rs[0]['season'],RSC_year=year,date_keys=len(rs),GP=sum(r['selected_fictional_GP_credit'] for r in rs),
            GS=sum(r['selected_fictional_GS_credit'] for r in rs),credited_minutes=sum(r['selected_fictional_credited_seconds'] for r in rs)//60,
            extra_credited_seconds=sum(r['selected_added_credited_seconds'] for r in rs),
            all_GP_is_selected_conditional_projection=year==4,actual_NBA_statistics_certified=False))
    need([(v['GP'],v['GS'],v['credited_minutes']) for v in out]==[(58,0,1044),(82,0,1476)],'Selected credited statistics changed')
    return out

def qo_family(scale):
    row=scale[7];s=row[2]
    corners=[('BASE80',(Fraction(4*s,5),0,0)),('BASE120',(Fraction(6*s,5),0,0)),('BASE80_LIKELY40',(Fraction(4*s,5),Fraction(2*s,5),0)),('BASE80_UNLIKELY40',(Fraction(4*s,5),0,Fraction(2*s,5)))]
    ws=[dict(id=n,third_year_components=[rat(Fraction(x)) for x in v],ordinary_QO=pure.result(row,v,False,scale)) for n,v in corners]
    return dict(original_2019_pick=7,original_2019_third_year_scale=s,
        original_component_family=dict(base_floor_fraction='4/5',total_ceiling_fraction='6/5',nonnegative_likely_preserved=True,nonnegative_unlikely_preserved=True,original_conditions_and_all_Gamma_retained=True),
        third_to_fourth_fraction='127/100',fourth_to_own_QO_fraction='1341/1000',
        selected_starter=False,rule='XI1c(ii)(B)_LESSER_OWN_COMPONENT_OFFER_OR_PICK15_BASE_ONLY',
        final_lesser_package_or_UPC_components_selected=False,original_exact_components_selected=False,
        own_sufficient_integer_cost_upper=9942120,nonstarter_sufficient_integer_cost_upper=7744602,upper_input_reduction=2197518,
        neither_amount_is_chosen_contract_price=True,corner_witnesses=ws,QO_issued=False,QO_accepted=False,
        MaximumQO_FAhold_FirstRefusal_signed_UPC_are_separate=True,actual_contract_or_rounding_certified=False)

def assert_qo(q,scale):
    s=scale[7][2];a=Fraction(6*scale[15][2],5)*Fraction(1533,1000)*Fraction(1398,1000)
    family=dict(base_floor_fraction='4/5',total_ceiling_fraction='6/5',nonnegative_likely_preserved=True,nonnegative_unlikely_preserved=True,original_conditions_and_all_Gamma_retained=True)
    need(q['original_component_family']==family,'Original component Gamma deleted or altered')
    need((q['selected_starter'],q['own_sufficient_integer_cost_upper'],q['nonstarter_sufficient_integer_cost_upper'],q['upper_input_reduction'])==(False,9942120,7744602,2197518),'QO branch or sufficient upper altered')
    vectors=[(Fraction(4*s,5),0,0),(Fraction(6*s,5),0,0),(Fraction(4*s,5),Fraction(2*s,5),0),(Fraction(4*s,5),0,Fraction(2*s,5))]
    for w,v in zip(q['corner_witnesses'],vectors,strict=True):
        own=[Fraction(x)*Fraction(127,100)*Fraction(1341,1000) for x in v]
        need(w['third_year_components']==[rat(Fraction(x)) for x in v],'Original QO components altered')
        expected=dict(rule='XI1c(ii)(B)_LESSER_OWN_COMPONENT_OFFER_OR_PICK15_BASE_ONLY',own_components=[rat(x) for x in own],anchor_base_only=rat(a),charge_upper_exact_rational=rat(min(sum(own),a)),final_UPC_components_selected=False)
        need(w['ordinary_QO']==expected,'Returned QO differs from independent source component formula')
    need(q['QO_issued']is False and q['QO_accepted']is False and q['neither_amount_is_chosen_contract_price']is True,'QO price/delivery/acceptance promoted')
    need(q['original_2019_pick']==7 and q['original_2019_third_year_scale']==4864800 and q['third_to_fourth_fraction']=='127/100' and q['fourth_to_own_QO_fraction']=='1341/1000','QO source pick/scale/factors altered')
    need(q['rule']=='XI1c(ii)(B)_LESSER_OWN_COMPONENT_OFFER_OR_PICK15_BASE_ONLY' and q['final_lesser_package_or_UPC_components_selected']is False and q['original_exact_components_selected']is False and q['MaximumQO_FAhold_FirstRefusal_signed_UPC_are_separate']is True and q['actual_contract_or_rounding_certified']is False,'Returned QO rule/scope promoted or altered')

def deadline_projection():
    need(date(2023,10,1).weekday()==6 and date(2023,10,2).weekday()==0,'2023 weekday calculation changed')
    return dict(ordinary_issue_law='2017_CBA',ordinary_issue_deadline='2023-06-29',
        issue_start='DAY_AFTER_SELECTED_2023_NBA_SEASON_END_TYPED_PORT',selected_2023_Season_end=None,
        acceptance_nominal_date='2023-10-01',acceptance_general_weekend_adjusted_date='2023-10-02',
        Oct1_is_only_nominal_or_sufficient_minimum_not_terminal=True,
        acceptance_after_July1_law='2023_XI4c_AND_XLII2',specific_override_or_written_extension_selected=False,
        original_function_through_Oct1_preserved_as_minimum=True,withdrawal_through='2023-07-13',
        later_withdrawal_requires_player_written_agreement=True,unaccepted_expiry_keeps_FirstRefusal=True,
        actual_QO_issuance_delivery_acceptance=None)
FIXED_DATES=copy.deepcopy(deadline_projection())

def build(root=ROOT):
    src=sources(root);primary=primary_guard(src);p=policy();need(p==FIXED_POLICY,'Selected stat policy altered')
    auth=canonical(root);need(direct(root,CANON)==auth,'Canonical model differs from explicit root selection')
    need(direct(root,CANON)==json.loads(text(root/CANON)),'Returned canon differs from physical bytes')
    third,fourth,witnesses=exposures(src)
    disk_g=json.loads(text(root/GLOBAL));disk_h=json.loads(text(root/H22))
    need(third==[r for r in disk_g['rows'] if 'CHI' in (r['home'],r['away'])] and fourth==disk_h['dated_rows'],'Returned exposure dates differ from physical selected seasons')
    expected_w=[]
    for state in ['NORMAL','COBY_OUT']:
        t=disk_g['shared_role_templates']['CHI:'+state]
        expected_w.append(dict(season='2021-22',state=state,selected_starting_nomination=STARTERS21,
            source_blocks=t['blocks'],source_block_count=len(t['blocks']),source_player_seconds=t['positive_player_seconds'],
            scope='Separate starting-consistent stat-credit witness with same source role/player budgets. Existing paired coverage arrays not overwritten or retroactively official GS.',
            actual_NBA_substitutions_or_starters_certified=False))
    t=disk_h['selected_role_template']
    expected_w.append(dict(season='2022-23',state='H22_NORMAL_KESSLER12_REG48',selected_starting_nomination=STARTERS22,
        source_blocks=t['ordered_regulation_blocks'],source_block_count=len(t['ordered_regulation_blocks']),source_player_seconds=t['player_seconds'],
        scope='Existing explicit selected starters and ordered first lineup; exact source budgets retained',actual_NBA_substitutions_or_starters_certified=False))
    need(witnesses==expected_w,'Returned starting witness differs from source budgets and selected nomination')
    rows=[]
    for year,items in [(3,third),(4,fourth)]:
        for r in items:
            seconds=r['team_date_models']['CHI']['positive_player_seconds'].get('Coby',0) if year==3 else src[H22]['selected_role_template']['player_seconds']['Coby White']
            x=stat_row(year,r,seconds)
            need(x==row_expected(year,r,seconds),'Returned dated credit differs from source participation/model; no false GP82 certification')
            rows.append(x)
    totals=summaries(rows)
    expected_totals=[dict(season=season,RSC_year=year,date_keys=82,GP=gp,GS=0,credited_minutes=minutes,extra_credited_seconds=0,all_GP_is_selected_conditional_projection=year==4,actual_NBA_statistics_certified=False) for season,year,gp,minutes in [('2021-22',3,58,1044),('2022-23',4,82,1476)]]
    need(totals==expected_totals,'Returned season totals differ from selected source credit')
    gs3,gs4=totals[0]['GS'],totals[1]['GS'];m3,m4=totals[0]['credited_minutes'],totals[1]['credited_minutes']
    arms=dict(fourth_GS_41=gs4>=41,fourth_MIN_2000=m4>=2000,third_fourth_mean_GS_41=gs3+gs4>=82,third_fourth_mean_MIN_2000=m3+m4>=4000)
    need(not any(arms.values()),'Credited statistics trigger Starter OR; cannot keep nonstarter')
    need(coby.starter_test(third_year_starts=gs3,third_year_credited_minutes=m3,fourth_year_starts=gs4,fourth_year_credited_minutes=m4)==any(arms.values()),'Pure starter function differs from direct CBA OR')
    primary_input,scale=coby.checked_primary(root)
    need(primary_input==src[PRIMARY],'QO function returned primary differs from physical input')
    need(scale=={7:(4422600,4643900,4864800,270,341),15:(2737600,2874500,3011400,533,398)},'Returned scale differs from source2019 named rows')
    q=qo_family(scale);assert_qo(q,scale);dates=deadline_projection();need(dates==FIXED_DATES,'QO deadline or actual receipt altered')
    need(src[QO]['conservative_integer_USD_cost_screens']['nonstarter']==q['nonstarter_sufficient_integer_cost_upper'],'Existing QO function cost join changed')
    return dict(id='CHICAGO_2023_SELECTED_STAT_CREDIT_AND_QO',baseline_main=BASELINE,
        status='ROOT_SELECTED_ROUTINE_FICTIONAL_STAT_CREDIT_AND_NONSTARTER_QO_INPUT_PENDING_INDEPENDENT_REVIEW',
        source_sha256={**PINS,SELF:sha(root/SELF),CANON:sha(root/CANON)},hash_convention='UTF8 BOM stripped; CRLF/CR to LF; external raw separate',
        primary_direct_support=primary,canonical_adoption=CANON,selected_policy=p,
        starting_nomination_and_same_budget_witnesses=witnesses,dated_stat_credit_rows=rows,season_stat_totals=totals,
        starter_test=dict(rule='GS4>=41 OR MIN4>=2000 OR GS3+GS4>=82 OR MIN3+MIN4>=4000',OR_arms=arms,selected_starter=False,
            combined_minutes=m3+m4,mean_minutes=rat(Fraction(m3+m4,2)),mean_starts=rat(Fraction(gs3+gs4,2)),
            opposite_P2022_OR_proof=dict(P_MIN4_lower_bound=2624,sufficient_OR_true=True,Coby_regulation_lower_bound_alone_does_not_exclude_OR=True),
            reevaluate_if_selected_extra_seconds_starts_or_participation_change=True),
        ordinary_QO_component_function=q,QO_clock=dates,
        source_history=dict(original_lowerbound_OTnull_files_preserved=True,source_H22_results_selected=src[H22]['summary']['results_selected'],
            source_H22_OT_selected=src[H22]['summary']['overtime_periods_selected'],current_2022_23_selected_winners=0,
            original_pair_coverage_clocks_not_official_stat_starters=True,original_pair_clocks_winners_not_rewritten=True),
        remaining_finite_consumers=['Select dated2022-23 opposing roles/productivity/winner outputs (currently0/82); conditional participation credit is not that result completion.',
            'Select2023 NBASeason endpoint; lawful ordinary QO issuance or alternative signed mechanism, normal/apron/FAhold/FirstRefusal cost join; no private receipt gate.',
            'LaMelo extension timeframe/conditional2024cap and eligible-honors agreed function remain distinct; no MVP/medal/long-ending selected.'],
        certification=dict(working_stat_credit_model_selected=True,working_nonstarter_branch_selected=True,
            fourth_year_positive_participation_policy_selected_for82=True,fourth_GP82_is_conditional_projection=True,
            all82_2022_23_results_or_future_participations_completed=False,actual_NBA_GP_GS_minutes_box_or_clinical_certified=False,
            QO_issued_or_accepted=False,actual_private_receipt=None,chosen_contract_price=False,original_Gamma_preserved=True,
            independent_review_completed=False,whole_macro3_complete=False,author_locked=False,MVP_title_or_long_ending_changed=False),
        freeze='v0.30 PARTIAL',design_gate='CLOSED',Pack_count=0,manuscript_allowed=False)

def markdown(v):
    return '\n'.join(['# Chicago2023 선택 가상 통계와 Coby ordinary QO 입력','',
        '**STAT23_A는 기존 시즌 위임으로 root가 명시 선택한 가상 credit 정책이다.** 원H21/H22 lowerbound/OTnull 기록과 실제NBA 미인증 필드는 그대로 보존했다. 새 독립검문은 아직 미완료다.','',
        '| RSC 정규연도 | GP credit | GS credit | 분 | 범위 |','|---|---:|---:|---:|---|',
        '|3 ·2021–22|58|0|1044|원82개 선택결과의 양수 참여 credit|','|4 ·2022–23|조건부82|0|1476|H22 82날짜 참여 정책을 모두 실행할 때의 projection|','',
        '두 시즌 가상 OT0·추가분0·Coby 벤치 GS0를 명시 선택했다. H22의 참여 정책 선택과 모든 미래 참여의 실행·관측은 별개다. **현재2022–23 승자0/82를 완료로 표시하지 않는다.** 이 소비자는 점수·승자·실제박스/임상증명·새가격을 선택하지 않는다.','',
        '## 선발과 clock 표현','',
        '원H21 M1은 unordered 용량 증인이고 기존 paired clock0는 공식 GS 인증이 아니다. 새 nomination은 LaMelo/LaVine/주인공/Markkanen/Carter5다. 원CHI NORMAL/COBY_OUT의 동일 선수·포지션 총초에서 이 선발로 시작 가능한 공유 증인을 검문한다. 기존 paired 시간배열/선수분/승패는 덮어쓰지 않는다. H22는 실제 선택된 fictional starters5와 ordered 첫블록이 일치하며 Coby가 없다. source coverage를 실제NBA 선발로 뒤집지 않는다.','',
        '## CBA OR와 QO','',
        'Starter는 GS4≥41 또는 MIN4≥2000 또는 GS3+GS4≥82 또는 MIN3+MIN4≥4000이다. 선택1044/1476·GS0은 합2520/평균1260, 네 OR 모두false다. P2022의2624 하한은 하나의 OR를 직접 충족했지만 Coby1476 하한 자체만으로는 비선발을 증명하지 않는다. 추가524분·GS41 등 변경 시 즉시 재평가한다.','',
        '원2019 CHI#7의80–120% base/likely/unlikely 성분 가족과 원조건Γ를 보존한다. 3→4년차×1.270,4년차→자기QO×1.341. 비선발은 자기 전체offer와2019#15 120% base-only offer 중 적법한 작은 패키지다. 원likely/unlikely를 삭제하거나 보너스를 항목별로 임의 상쇄하지 않는다.','',
        '**비선발 충분비용 상단7,744,602달러**, 자기offer 상단9,942,120달러와 차2,197,518달러. 이것은 미선택 가격 범위 입력이며 정확UPC/법정반올림/실제수락을 인증하지 않는다. ordinaryQO 발행·MaximumQO·FAhold·FirstRefusal·새 UPC는 별도다.','',
        '[2017 CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) XI1(c)/4 원쪽 및 [2023 CBA](https://imgix.cosmicjs.com/25da5eb0-15eb-11ee-b5b3-fbd321202bdf-Final-2023-NBA-Collective-Bargaining-Agreement-6-28-23.pdf) XI4(c)/XLII2를 직접 읽었다. June29 발행은2017법, July1 이후는2023법. 발행창 시작의2023 Season 말단은 typed 미입력이다. October1,2023은 일요일이므로 일반기한 projection은 Monday October2이며 원Oct1 최소/명목창을 정확 종료일로 확대하지 않는다. 실제발행/수락/연장/철회는 미선택이다.','',
        '## 재현·남은 작업','',
        '`python -B -X utf8 tools/build_chicago_2023_selected_stat_credit_and_qo.py --check --self-test`. 원JSON 독립 물리 파싱·rawPDF/쪽 SHA·2019표 원분수 함수를 소비한다. 조상 전체 생성기는 실행하지 않는다. 반환 OT추가524/GS41/Γ삭제/Oct1 종말오독/GP82실증승격을 거부하는 작성자 검문이며 독립감리로 세지 않는다.','',
        '다음은 FY23 날짜 결과82개, 선택2023 Season 말단 및 ordinaryQO 발행/서명 장부, 별도 LaMelo extension 함수다. 실제NBA 박스나 비공개 접수증을 새 완료 gate로 추가하지 않는다.','',
        '[원 정적 포트](../research/CHICAGO_2023_STAT_QO_AND_CBA_FINITE_PORTS_2026_10_08.md) · [현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md) · [누적 기능 등록기](../control/G13_FINAL_FUNCTION_REGISTER.md)','',
        '| 묶음 | 상태 |','|---|---|','|1 드래프트 연쇄|완료|','|2 Chicago2020–21|완료|','|3 2021–23|통계credit·QO 입력 선택, FY23 결과/계약 미완료|','|4 장기커리어|진행|','|5 전체구조|현행 기능등록기 참조|','|6 규격·Context Pack|현행 source등록기 참조·Pack0|','|7 통합·작가승인|미완료|','',
        '미완료 큰묶음5/6번까지4 · v0.30 PARTIAL · CLOSED · 원고0.',''])

def validate(v,root=ROOT):
    try:need(v==build(root),'Saved output differs from source-bound selected constructor');return []
    except (ValueError,KeyError,AssertionError,TypeError) as e:return [str(e)]

def self_test(root=ROOT):
    import sys
    module=sys.modules[__name__];tests=[]
    original=stat_row
    for name,mut in [
        ('OT_delta524_cannot_keep_nonstarter',lambda r:r.update(selected_added_credited_seconds=524*60,selected_fictional_credited_seconds=r['source_regulation_seconds']+524*60)),
        ('GS41_cannot_keep_nonstarter',lambda r:r.update(selected_fictional_GS_credit=41)),
        ('GP82_cannot_be_actual_future_cert',lambda r:r.update(actual_future_all82_participations_observed_or_executed=True))]:
        def badrow(year,r,seconds,mut=mut):
            v=original(year,r,seconds)
            if year==4:mut(v)
            return v
        with patch.object(module,'stat_row',badrow):
            try:build(root)
            except (ValueError,AssertionError) as e:tests.append({'id':name,'rejected':True,'message':str(e)})
            else:raise ValueError('False pass: '+name)
    oq=qo_family
    def badgamma(scale):
        q=oq(scale);q['original_component_family']['nonnegative_unlikely_preserved']=False;return q
    with patch.object(module,'qo_family',badgamma):
        try:build(root)
        except (ValueError,AssertionError) as e:tests.append({'id':'original_Gamma_deletion','rejected':True,'message':str(e)})
        else:raise ValueError('False pass: Gamma deletion')
    od=deadline_projection
    def baddate():
        d=od();d['acceptance_general_weekend_adjusted_date']='2023-10-01';return d
    with patch.object(module,'deadline_projection',baddate):
        try:build(root)
        except (ValueError,AssertionError) as e:tests.append({'id':'Oct1_as_exact_terminal','rejected':True,'message':str(e)})
        else:raise ValueError('False pass: Oct1 terminal')
    return tests

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    if a.write:
        sources(ROOT);(ROOT/CANON).write_text(json.dumps(canonical(ROOT),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    v=build()
    if a.write:
        (ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
    if a.check:need(direct(ROOT,OUT)==v,'Saved selected output stale');need(text(ROOT/MD)==markdown(v),'Saved MD stale')
    print(json.dumps({'current':True,'year3':v['season_stat_totals'][0],'year4':v['season_stat_totals'][1],'starter':v['starter_test']['selected_starter'],'QO_nonstarter_upper':v['ordinary_QO_component_function']['nonstarter_sufficient_integer_cost_upper']},ensure_ascii=False))
    if a.self_test:print(json.dumps({'writer_negative_controls':self_test()},ensure_ascii=False))
if __name__=='__main__':main()
