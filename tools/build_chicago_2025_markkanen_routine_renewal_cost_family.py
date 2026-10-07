"""Finite, unselected same-Chicago Bird renewal forms; no private-cost certification."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
OUT = 'research/CHICAGO_2025_MARKKANEN_ROUTINE_RENEWAL_COST_FAMILY_2026_10_08.json'
MD = OUT[:-5] + '.md'
SELF = 'tools/build_chicago_2025_markkanen_routine_renewal_cost_family.py'
BASELINE = '1e02e5458f7d6191fbeeae5eeaf526cacde866d5'
PINS = {'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json': '253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088', 'research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json': '7244beff7a120c5ca246a04e72b61586f3cfbe245487d5fc6479f5245fd78d9f', 'simulation/CHICAGO_2022_23_NAMED_CONTRACT_WINDOW.json': '21e860056c2654d5e4837911dac39e7f45f4d26388d353bc57594afefcecf1f4', 'simulation/CHICAGO_2023_SELECTED_ROUTINE_EXECUTION.json': '9a4f6db21d6ad50e2c6d6897f1c2dedbdf440cee89bae47019f4bd131f341790', 'simulation/CHICAGO_2024_A10_SELECTED_RENEWAL_EXECUTION.json': 'ef48f0a1931037ec58ec59e53fde30baedddf8d96f13e2bc86120da2a7572cf5'}
RAW = {'CBA2023': {'path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\fr-2023-cba-boundary-20261007\\cba2023.pdf', 'sha256': 'bf178ca0f2d64f9dfe6fde095d3ae43d576b12e19ce7a679618d632584f7ab32', 'url': 'https://imgix.cosmicjs.com/25da5eb0-15eb-11ee-b5b3-fbd321202bdf-Final-2023-NBA-Collective-Bargaining-Agreement-6-28-23.pdf', 'source_kind': 'OFFICIAL_NBPA_PDF_REUSED'}, 'NBA_CAP2025': {'path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\fr-markkanen-2025-renewal-20261008\\NBA_CAP2025.html', 'sha256': '8b20484615b529dbcb0b6e6ba3f08997db4b2cdd259d8ffb4d9ed44f75320988', 'url': 'https://pr.nba.com/nba-salary-cap-2025-26-season/', 'source_kind': 'OFFICIAL_DIRECT_PROVIDER_RAW_HTTP200'}, 'NBA_MARK_IDENTITY': {'path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\fr-markkanen-2025-renewal-20261008\\NBA_MARK_IDENTITY.html', 'sha256': 'a178c240a92276fa167bc496dc82396931d90b9574915ae94647ca8d7dda3383', 'url': 'https://www.nba.com/player/1628374/lauri-markkanen', 'source_kind': 'OFFICIAL_DIRECT_PROVIDER_RAW_HTTP200'}}
PAGE_SHA = {'29': '51adc90d5cf76f61c80346ee0d8275f53870b0af2e622d43d8e18e96f1b8768f', '30': 'fb8a5f15dd0c766cdb373c0535a71ea36d4ed96a46106a36a6774dc28742a429', '31': 'f1cf878da1d9b554ff242e52975f67f0bda1127300045f04b5188ebd4e506b52', '33': '397f25af16b982f0ab5a0199789aab9c9b9e577fe0fd3b010fdb0f5fc3012d5e', '37': 'b6bb7c88266158f4be0c1118ce0523057218d1f5c0422304f404fe3df61adfcd', '39': 'bf8d1060b154dd48d9533b7e33601dce2bf69d9c583863b4c1b9a74c8addd319', '40': '0b9cb0202700be2519404170ab0b4287b534fa2b2e6350cc012a4011d3ebcb7a', '47': '64c29e97826b68ae5d1c991ed21a989d896b8ad7c6a6d11cb16332f52118e1b7', '50': 'd2d3053300a4ca707b05b18429e006683fb1f87943b72d934bffec2b3fb3345b', '57': 'ffac47dda5504cb4f3055fbf983e08e59255ece054c36c8507b497066e226dd0', '58': 'baeea9999ef9d320408ad5714b7c743944ddaaac84eb7f0f8dd191cd6be87921', '60': 'd2527b2a4e3848652305308ea38e1c97fedbb97fd34c93d5527df5864491f24b', '61': '5fef2298ad1156ebe3e3fe2b922cdf9c2b99e143153ea9e08171808b6230a8e9', '210': '51ee1bb8eb26216488f7dd4ef8a82edde1a0b89df4ae4850e16454b200de8715', '211': '75790dcb58ccfe4b37e2fa83b35690e50c643c084d6d55e1e359dedfc2295c03', '214': 'e6c0b186ade730ba06c28f93dd80af284601bcbc091601fd4641b35729693a57', '215': '446ea99ef827b851e3fde4138921d15a07f3a8d78f4fb8903fdf4fa03f14dd13', '222': '2757fd36981c6564f49efff9ced2f383584f1a4c07a2a182f3fbf4947974bc11', '240': '1712263b1347992499d49e999935d6eb6dee0dd493850ff7f1f08284f7d04862', '241': 'ee2a3f22c495aa8d226353dda9013722cf188ebb2a12e2bd69de50ce7ac8bac9', '242': '0311d26d906d460858db1f315c6cf989093478ccca08a25a5ebc3703386a4e6b', '243': 'dbbd018d9ac268a74a2783409b3dbd6c67f4e2bd433c75fe6d61b61f9bb56238', '251': '54c7fce4b1bec13fa95072281f9c34b964da19fc0a17406f6f5f99d6a113d0f1', '255': '1d13b211bee94e0c95de5faaa63b5754c7470d9e8ff520043d8ee4f651f59620', '272': 'df690e7bbb754f22d0126e67d754fac6f198eb047f4c3c1613c888bfba31a555', '319': '6640ea05858483ed302458cb0db48a3ba5bdcd4bda4a75ded8b34212bceabeac', '343': '4e9e3d70f8098c531813df6e6d43e0cd9a7fa5aa628d353f5cee70ac3238c098', '360': 'd4f33383c6d18bcf719d102674fdd817b04739ee12fd172fb040cc7f069e5466', '453': '9da339767ac6d4e7bd545030bfda4e31576058d367a326c9ec6459575a56fcc9', '454': '426c49f712e6b0dd1064f80a6fdd259269440b31cc2d3011c1a34ff542ab76eb', '632': '165c16335e87e8a9ab8e07b79f8c179da5f679cc556a9ac4b44dd53ee462d70b'}
CBA = Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-2023-cba-boundary-20261007/cba2023.pdf')
CACHE = Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-markkanen-2025-renewal-20261008')
CAP = 154647000
PRIOR = 21080000
SPECS = [('M25A', 3, 20, 0), ('M25B', 4, 25, 8), ('M25C', 5, 30, 8)]
CAP_URL = 'https://pr.nba.com/nba-salary-cap-2025-26-season/'
CBA_URL = 'https://imgix.cosmicjs.com/25da5eb0-15eb-11ee-b5b3-fbd321202bdf-Final-2023-NBA-Collective-Bargaining-Agreement-6-28-23.pdf'
SCOPE = 'Primary rules and published league amounts; hypothetical UPC forms, not NBA receipt, exact private cents, or market acceptance'

def norm(b):
    return b.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n').encode('utf-8')

def sha(b):
    return hashlib.sha256(b).hexdigest()

def load_sources():
    src = {}
    for f, h in PINS.items():
        b = (ROOT / f).read_bytes()
        assert sha(norm(b)) == h, f'Source changed: {f}'
        src[f] = json.loads(b.decode('utf-8-sig'))
    return src

def check_sources(src):
    m = src['canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json']['selected']
    assert m['route'] == 'M1'
    assert m['proposed_salary_by_season_usd'] == {'2021-22': 17000000, '2022-23': 18360000, '2023-24': 19720000, '2024-25': PRIOR}
    c = src['research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json']['routine_implementation']['new_contracts']['Markkanen']
    assert c == {'first_year_regular_salary': 17000000, 'years': 4, 'annual_raise': 1360000, 'signing_performance_trade_promotional_loan_or_buyout_additions': 0}, 'Original M1 form changed'
    rows = [src['simulation/CHICAGO_2022_23_NAMED_CONTRACT_WINDOW.json']['working_implementation']['named_contracts'][0],
            src['simulation/CHICAGO_2023_SELECTED_ROUTINE_EXECUTION.json']['named_contracts_and_rights'][0],
            src['simulation/CHICAGO_2024_A10_SELECTED_RENEWAL_EXECUTION.json']['execution']['live10'][0]]
    for r in rows:
        assert r['player'] == 'Lauri Markkanen' and r['holder'] == 'CHI'
    assert rows[0]['normal_upper'] == 18360000 and rows[0]['last_selected_salary_capyear_start'] == 2024
    assert rows[1]['FY23_normal_upper'] == 19720000 and rows[1]['original_Gamma_full_components_and_protected_cash_preserved'] is True
    assert rows[2]['annual_component_upper'] == PRIOR and rows[2]['last_currently_guaranteed_or_exercised_salary_capyear'] == 2024
    assert rows[2]['original_Gamma_and_protection_preserved'] is True and rows[2]['fiscal_end_is_exact_service_term'] is False

def primary():
    import fitz
    from bs4 import BeautifulSoup
    observations = []
    for name, info in RAW.items():
        p = Path(info['path']); b = p.read_bytes()
        assert sha(b) == info['sha256'], f'Raw changed: {name}'
        observations.append(dict(info, id=name, bytes=len(b), adopted_body=True))
    d = fitz.open(CBA)
    pages = []
    for n, h in PAGE_SHA.items():
        t = d[int(n)-1].get_text()
        assert sha(norm(t.encode())) == h, f'CBA page changed: {n}'
        pages.append({'pdf_page': int(n), 'text_sha256': h})
    cap_body = BeautifulSoup((CACHE/'NBA_CAP2025.html').read_bytes(), 'html.parser').get_text(' ', strip=True).split('Related Posts')[0]
    for s in ['$154.647 million', '$187.895 million', '$195.945 million', '$207.824 million', '$139.182 million', 'noon ET on Sunday, July 6']:
        assert s in cap_body, f'Official 2025 amount/calendar not found: {s}'
    identity = BeautifulSoup((CACHE/'NBA_MARK_IDENTITY.html').read_bytes(), 'html.parser').get_text(' ', strip=True)
    assert 'May 22, 1997' in identity and '2017 R1 Pick 7' in identity
    return {'raw_sources': observations, 'CBA_pages_directly_read': pages, 'source_scope': SCOPE,
            'profile_use': 'Birthdate 1997-05-22 and 2017 draft only; current Utah, experience 9, and 2024 Utah extension are not transferred'}

def candidates():
    out = []
    for id, years, pct, raise_pct in SPECS:
        first = CAP*pct//100
        vals = [first + first*raise_pct*k//100 for k in range(years)]
        out.append({'id': id, 'team': 'CHI', 'player': 'Lauri Markkanen', 'mechanism': 'OWN_FULL_BIRD_NEW_UPC_NOT_EXTENSION_OR_SIGN_AND_TRADE',
                    'first_salary_cap_percent_design_scenario': pct, 'years': years, 'salary_capyear_start': 2025,
                    'salary_by_capyear': {str(2025+i): v for i, v in enumerate(vals)}, 'total_regular_salary': sum(vals),
                    'annual_raise_percent_of_first_salary': raise_pct, 'compound_raise': False,
                    'protection_lack_of_skill_and_injury_or_illness_percent': 100,
                    'protection_subject_to_standard_CBA_Exhibit2_conditions': True, 'death_protection_selected': False,
                    'new_signing_likely_unlikely_trade_promotional_loan_buyout_additions': 0,
                    'option': None, 'ETO': None, 'actual_player_team_consent': None, 'selected': False,
                    'first_normal_apron_salary_equal': first, 'first_salary_delta_from_M1_last_year': first-PRIOR,
                    'new_STD': 1, 'new_TW': 0, 'original_Gamma_preserved': True,
                    'new_automatic_hardcap_trigger': False, 'agreement_is_economically_predicted': False})
    return out

def evaluate_claim(route_id, *, signed, prior_ge_average, old_Gamma, other_STD=14):
    """One named claim only. Gamma is supplied, never inferred absent."""
    assert type(signed) is bool and type(prior_ge_average) is bool
    assert isinstance(other_STD, int) and 0 <= other_STD <=14
    assert old_Gamma >=0
    spec = next(x for x in SPECS if x[0]==route_id)
    first = CAP*spec[2]//100
    hold = PRIOR*(150 if prior_ge_average else 190)//100
    return {'route_id': route_id, 'signed': signed, 'prior_ge_average': prior_ge_average,
            'normal_Mark_claim_only': (first if signed else hold)+old_Gamma,
            'apron_Mark_claim_only': (first if signed else 0)+old_Gamma,
            'new_STD': int(signed), 'new_TW': 0, 'old_Gamma_carried': old_Gamma,
            'unpriced_team_components_included': False, 'new_base_salary_obligation': first if signed else 0}

def claim_witness():
    rows=[]
    for id, years, pct, raise_pct in SPECS:
        for ge in [True,False]:
            pre=evaluate_claim(id,signed=False,prior_ge_average=ge,old_Gamma=0)
            post=evaluate_claim(id,signed=True,prior_ge_average=ge,old_Gamma=0)
            rows.append({'route_id': id, 'prior_ge_average': ge, 'zero_Gamma_is_arithmetic_basis_not_selected_absence': True,
                         'before': pre, 'after': post,
                         'normal_delta': post['normal_Mark_claim_only']-pre['normal_Mark_claim_only'],
                         'apron_delta': post['apron_Mark_claim_only']-pre['apron_Mark_claim_only'],
                         'for_every_preserved_Gamma': 'Add the same lawful fiscal-attributed original Gamma amount to both sides; it cancels from delta and is never erased'})
    return rows

def costs():
    return {'prior_salary_for_max_and_FA_hold': PRIOR,
            'ordinary_max': max(CAP*30//100, PRIOR*105//100),
            'higher_max_35_percent_port': {'amount': CAP*35//100, 'required': 'Eight/nine YOS, original-team/permitted early-trade history, Higher Max Criteria at signing', 'criteria_selected': False, 'used_by_these_forms': False},
            'FA_hold_cases': [{'condition': 'Prior Salary >= FY24 Estimated Average Player Salary', 'normal': PRIOR*150//100, 'apron': 0},
                              {'condition': 'Prior Salary < FY24 Estimated Average Player Salary', 'normal': PRIOR*190//100, 'apron': 0}],
            'FA_hold_case_selection': None,
            'hold_formula': 'max(unreimbursed applicable minimum, min(applicable maximum, multiplier * prior Salary)); figures assume the legal minimum <= 31,620,000',
            'FA_hold_removed_only_by': 'New valid same-team UPC, other-team signing, or valid renunciation; this Bird route does not renounce Markkanen before signing',
            'hold_once_replacement': 'On proposed July7 valid UPC: normal subtract exactly the chosen Markkanen FA hold and add new Salary once; apron add new Salary once, no prior UFA hold included',
            'six_categories': [
                {'id': 'LIVE25', 'normal': 'L25 + selected-form first Salary', 'apron': 'A_live25 + selected-form first Salary', 'scope': 'Mark new bonuses 0 are proposed terms; other retained UPC and all original Gamma obligations survive'},
                {'id': 'OLD_GAMMA25', 'normal': 'R25_normal', 'apron': 'R25_apron', 'scope': 'Original named residual/grievance/waiver obligations and their lawful fiscal attribution; R24 ceiling is not silently certified for FY25'},
                {'id': 'FA_QO_FRN25', 'normal': 'Other_FA25 + Mark hold before UPC; Other_FA25 only after replacement', 'apron': 'Other_QO_FRN25; Mark ordinary UFA hold excluded', 'scope': 'Eight-YOS veteran finishing non-RSC: no Mark QO/ROFR manufactured; other players rights remain'},
                {'id': 'DRAFT25', 'normal': 'N25', 'apron': 'A25', 'scope': 'Unsigned first-round 120% hold vs applicable Required Tender/apron; second-round reservation is not an automatic statutory charge or UPC'},
                {'id': 'EXCEPTIONS25', 'normal': 'E25 as lawfully included until used/expired/validly renounced', 'apron': 'No unused-exception face amount; transaction/signed-player charges still included', 'scope': 'Own Bird does not spend MLE; no blanket exception renunciation selected here'},
                {'id': 'ROSTER_FLOOR_TAX_CASH25', 'normal': 'Applicable incomplete-roster/floor or other deemed-Salary adjustments', 'apron': 'Applicable law-specific adjustments', 'scope': 'Official floor139182000 is the published value; Tax is not Salary, and cash payment timing is not a new capyear charge'}],
            'typed_other_inputs': {'L25': None, 'A_live25': None, 'R25_normal': None, 'R25_apron': None, 'Other_FA25': None, 'Other_QO_FRN25': None, 'N25': None, 'A25': None, 'E25': None},
            'whole_FY25_normal_upper': None, 'whole_FY25_apron_upper': None, 'whole_FY25_tax_bill': None,
            'actual_fullcash_receipt': None, 'new_regular_cash_obligation_by_form_is_known': True,
            'hardcap_condition': 'Own Bird renewal alone is absent from VII2(e) transaction-trigger table; any other current/prior post-season trigger and its applicable apron must still be respected',
            'apron_excess_alone_is_illegal': False, 'team_floor_compliance_certified': False}

def construct(src):
    return {'id': 'CHICAGO_2025_MARKKANEN_ROUTINE_RENEWAL_COST_FAMILY', 'baseline_main': BASELINE,
            'status': 'SOURCE_SUPPORTED_SAME_CHICAGO_CONSENSUAL_CANDIDATES_REVIEW_PENDING',
            'source_sha256': dict(PINS, **{SELF: sha(norm((ROOT/SELF).read_bytes()))}),
            'primary': primary(),
            'official_2025': {'cap': CAP, 'tax': 187895000, 'first_apron': 195945000, 'second_apron': 207824000,
                              'published_minimum_team_salary': 139182000, 'NTMLE': 14104000, 'TMLE': 5685000, 'RoomMLE': 8781000,
                              'moratorium_end_ET': '2025-07-06T12:00:00', 'candidate_signing_ET': '2025-07-07T12:02:00'},
            'M1_preserved': {'seasons': ['2021-22','2022-23','2023-24','2024-25'], 'salary_schedule': [17000000,18360000,19720000,PRIOR],
                             'total': 76160000, 'last_fiscal_end': '2025-06-30', 'fiscal_end_is_exact_service_end': False,
                             'original_Gamma_preserved': True, 'prior_new_M1_bonus_additions': 0, 'new_2024_Utah_extension_copied': False},
            'admitted_input_family': {'team': 'CHI', 'player': 'Lauri Markkanen', 'YOS': 8,
                'service_seasons': [f'{y}-{str(y+1)[2:]}' for y in range(2017,2025)],
                'service_condition': 'Each of the eight named Seasons has at least one qualifying NBA Active/Inactive day; no withholding>30day, disapproved-UPC, or unsigned outstanding-QO exception; actual clinical results/stat totals not required',
                'own_Bird_three_seasons': ['2022-23','2023-24','2024-25'],
                'Bird_condition': 'Preserved selected M1 CHI UPC covers all three preceding Seasons and same team; no rights renunciation/assignment/termination inserted; services rendered within lawful family',
                'old_UPC_completion_condition': 'Final 2024-25 covered NBA Season/service term completed before new valid UPC; fiscal June30 is not substituted for service expiry',
                'minimum_condition': 'Each salary >= applicable 2025 signing-year eight-YOS Minimum Annual Salary Scale column for that contract year, pursuant to II6 and I1(jj)',
                'minimum_unrounded_design_reference': [str(Fraction(x*CAP,123655000)) for x in [2628597,2760026,2891458,3022889,3154319]],
                'minimum_reference_is_published_official_adjusted_table': False,
                'minimum_exact_statutory_rounding_certified': False,
                'consensual_UPC_condition': 'Both parties voluntarily agree to one lawful Exhibit1 salary schedule and Exhibit2 protection; no actual consent/payment/filing asserted',
                'other_STD_capacity_condition': 'Other operative ordinary STD <=14 when Mark signs; no replacement of another live contract or protected cash by metadata',
                'other_TW_capacity_condition': 'Other roster/TW rules applicable independently; this proposal creates zero TW or conversions',
                'future_assignment_condition': 'Any later assignment separately satisfies VII8 waiting-period/Bird raise conditions, matching and apron restrictions; no automatic trade approval/date'},
            'candidates': candidates(), 'recommendation': {'candidate_id': 'M25B', 'status': 'PLANNING_RECOMMENDATION_NOT_SELECTION',
                'reason': 'Middle scenario and four-year form preserves growth core while displaying greater annual and term cost than M25A; M25C supplies an ordinary-maximum sensitivity. No discount or market acceptance inferred'},
            'cost_family': costs(), 'claim_transition_witness': claim_witness(),
            'dated_transition': [{'date': '2025-06-30', 'Mark_new_STD': 0, 'new_salary': 0, 'cost_scope': 'Last M1 year plus old Gamma; no June retrospective renewal'},
                {'date': '2025-07-01', 'Mark_new_STD': 0, 'new_salary': 0, 'cost_scope': 'Ordinary UFA hold retained in normal; excluded from apron; own Bird remains'},
                {'date': '2025-07-07', 'Mark_new_STD': 1, 'new_salary': 'chosen unselected scenario first Salary only if candidate agreement executed', 'cost_scope': 'One Mark UPC replaces one Mark normal FA hold, apron receives Salary once; no double charge'},
                {'date': '2026-06-30', 'Mark_new_STD': 1, 'new_salary': 'same first-year selected-form obligation, no new cash event inferred', 'cost_scope': 'Next FY26 schedule and any option/assignment require their own operative inputs'}],
            'certification': {'independent_review_completed': False, 'selected_form': None, 'actual_private_cents': False, 'actual_player_consent': False,
                'actual_NBA_receipt': False, 'actual_market_agreement_predicted': False, 'whole_FY25_team_cost': False, 'whole_career_or_A10_performance': False,
                'new_franchise_MVP_title_retirement_choice': False}, 'freeze': 'v0.30 PARTIAL', 'design_gate': 'CLOSED', 'Pack_count': 0, 'manuscript_allowed': False}

def assert_output(o, src):
    check_sources(src)
    assert o['M1_preserved']['salary_schedule'] == [17000000,18360000,19720000,PRIOR]
    assert o['M1_preserved']['original_Gamma_preserved'] is True and o['M1_preserved']['new_2024_Utah_extension_copied'] is False
    assert o['M1_preserved']['fiscal_end_is_exact_service_end'] is False
    assert o['primary']['source_scope'] == SCOPE
    assert o['primary']['raw_sources'] == [dict(i,id=n,bytes=Path(i['path']).stat().st_size,adopted_body=True) for n,i in RAW.items()]
    assert o['primary']['CBA_pages_directly_read'] == [{'pdf_page': int(n),'text_sha256': h} for n,h in PAGE_SHA.items()]
    assert o['official_2025']=={'cap':154647000,'tax':187895000,'first_apron':195945000,'second_apron':207824000,
        'published_minimum_team_salary':139182000,'NTMLE':14104000,'TMLE':5685000,'RoomMLE':8781000,
        'moratorium_end_ET':'2025-07-06T12:00:00','candidate_signing_ET':'2025-07-07T12:02:00'}
    a = o['admitted_input_family']
    assert a['team'] == 'CHI' and a['YOS'] == 8 and a['own_Bird_three_seasons'] == ['2022-23','2023-24','2024-25']
    assert a['service_seasons'] == [f'{y}-{str(y+1)[2:]}' for y in range(2017,2025)]
    assert a['minimum_reference_is_published_official_adjusted_table'] is False and a['minimum_exact_statutory_rounding_certified'] is False
    assert a['minimum_unrounded_design_reference']==[str(Fraction(x*154647000,123655000)) for x in [2628597,2760026,2891458,3022889,3154319]]
    assert len(o['candidates']) == 3
    for r, (id, years, pct, raise_pct) in zip(o['candidates'], SPECS):
        first = Fraction(CAP*pct,100)
        expected = {str(2025+k): int(first*(1+Fraction(raise_pct*k,100))) for k in range(years)}
        assert r['id'] == id and r['years'] == years and r['salary_by_capyear'] == expected, 'Salary/term/linear raise differs'
        assert r['total_regular_salary'] == sum(expected.values()) and r['first_normal_apron_salary_equal'] == first
        assert r['first_salary_delta_from_M1_last_year'] == first-PRIOR
        assert first <= max(Fraction(CAP*30,100), Fraction(PRIOR*105,100)) and years <=5
        assert r['annual_raise_percent_of_first_salary'] == raise_pct and raise_pct <=8 and r['compound_raise'] is False
        for k in ['original_Gamma_preserved','protection_subject_to_standard_CBA_Exhibit2_conditions']: assert r[k] is True
        assert r['protection_lack_of_skill_and_injury_or_illness_percent'] == 100
        assert r['new_signing_likely_unlikely_trade_promotional_loan_buyout_additions'] == 0
        for k in ['selected','agreement_is_economically_predicted','new_automatic_hardcap_trigger','death_protection_selected']: assert r[k] is False
        assert r['option'] is None and r['ETO'] is None and r['actual_player_team_consent'] is None
        assert r['team'] == 'CHI' and r['new_STD'] == 1 and r['new_TW'] == 0
        assert r['mechanism'] == 'OWN_FULL_BIRD_NEW_UPC_NOT_EXTENSION_OR_SIGN_AND_TRADE'
    c = o['cost_family']
    assert c['prior_salary_for_max_and_FA_hold'] == PRIOR and c['ordinary_max'] == 46394100
    assert c['FA_hold_cases'] == [{'condition': 'Prior Salary >= FY24 Estimated Average Player Salary','normal':31620000,'apron':0}, {'condition':'Prior Salary < FY24 Estimated Average Player Salary','normal':40052000,'apron':0}], 'FA claims erased or apron/normal confused'
    assert c['FA_hold_case_selection'] is None and c['apron_excess_alone_is_illegal'] is False
    assert c['hold_once_replacement'] == 'On proposed July7 valid UPC: normal subtract exactly the chosen Markkanen FA hold and add new Salary once; apron add new Salary once, no prior UFA hold included'
    assert [x['id'] for x in c['six_categories']] == ['LIVE25','OLD_GAMMA25','FA_QO_FRN25','DRAFT25','EXCEPTIONS25','ROSTER_FLOOR_TAX_CASH25']
    category_charges = [
        ('L25 + selected-form first Salary', 'A_live25 + selected-form first Salary'),
        ('R25_normal', 'R25_apron'),
        ('Other_FA25 + Mark hold before UPC; Other_FA25 only after replacement', 'Other_QO_FRN25; Mark ordinary UFA hold excluded'),
        ('N25', 'A25'),
        ('E25 as lawfully included until used/expired/validly renounced', 'No unused-exception face amount; transaction/signed-player charges still included'),
        ('Applicable incomplete-roster/floor or other deemed-Salary adjustments', 'Applicable law-specific adjustments')]
    for row, (normal, apron) in zip(c['six_categories'], category_charges):
        assert row['normal']==normal and row['apron']==apron, 'Named six-category charge expressions changed or erased'
    assert all(v is None for v in c['typed_other_inputs'].values())
    for k in ['whole_FY25_normal_upper','whole_FY25_apron_upper','whole_FY25_tax_bill','actual_fullcash_receipt']: assert c[k] is None
    assert c['hardcap_condition'] == 'Own Bird renewal alone is absent from VII2(e) transaction-trigger table; any other current/prior post-season trigger and its applicable apron must still be respected'
    assert len(o['claim_transition_witness'])==6
    for cell, (id,pct,ge) in zip(o['claim_transition_witness'], [(id,pct,ge) for id,years,pct,r in SPECS for ge in [True,False]]):
        first=CAP*pct//100;hold=PRIOR*(150 if ge else 190)//100
        assert cell['route_id']==id and cell['prior_ge_average']==ge
        assert cell['zero_Gamma_is_arithmetic_basis_not_selected_absence'] is True
        assert cell['normal_delta']==first-hold and cell['apron_delta']==first
        for side, is_signed in [('before',False),('after',True)]:
            row=cell[side]
            assert row['normal_Mark_claim_only']==(first if is_signed else hold)
            assert row['apron_Mark_claim_only']==(first if is_signed else 0)
            assert row['new_STD']==int(is_signed) and row['new_TW']==0 and row['old_Gamma_carried']==0
            assert row['unpriced_team_components_included'] is False and row['new_base_salary_obligation']==(first if is_signed else 0)
    assert o['certification']['selected_form'] is None and all(v is False for k,v in o['certification'].items() if k!='selected_form')
    assert o['design_gate']=='CLOSED' and o['Pack_count']==0 and o['manuscript_allowed'] is False

def build():
    src=load_sources(); check_sources(src)
    o=construct(copy.deepcopy(src))
    fresh=load_sources()
    assert src==fresh, 'Physical source changed during construction'
    assert_output(o,fresh)
    return o

def validate(o):
    try:
        assert_output(o,load_sources())
        assert o==build(), 'Saved artifact is not current producer output'
        return []
    except (AssertionError,KeyError,ValueError) as e:return [str(e)]

def md(o):
    lines=['# Chicago 2025 Markkanen: same-team renewal cost family','',
        'PR505 main 고정 기준. 원 M1 네 시즌의 마지막 급여 구성 상단은 $21,080,000이다. 다음 세 가격은 새 Chicago 합의의 **미선택 후보**이며 실제 시장가격·할인·수락 예측이 아니다. M25B는 검문 후 선택할 수 있는 작업 권고다. 실제 2024 Utah 연장을 복사하지 않는다.','',
        '## 가격·기간 비교','', '|후보|첫해|기간|연간 인상|급여 합계|첫해 Δ|','|---|---:|---:|---|---:|---:|']
    for r in o['candidates']:lines.append(f"|{r['id']}|${r['first_normal_apron_salary_equal']:,}|{r['years']}년|첫해의 {r['annual_raise_percent_of_first_salary']}%·선형|${r['total_regular_salary']:,}|+${r['first_salary_delta_from_M1_last_year']:,}|")
    lines += ['', '모든 후보는 skill/injury·illness Base Compensation 100% 보호와 표준 CBA/Exhibit2 조건을 사용한다. death 전액보호·옵션·ETO·새 signing/performance/trade/promotional/loan/buyout 금액은 제안하지 않는다. 과거 Γ를 지우거나 5년을 넘어 옵션을 덧붙이지 않는다.', '',
      '## 법적 입력과 날짜', '',
      '- 2017–18부터 2024–25까지 각 시즌의 적격 NBA 명단 하루와 예외 없는 경력 가족이면 8YOS다. 현재 웹 프로필의 경력 9년을 2025에 이식하지 않는다.',
      '- M1이 Chicago에서 2022–23/2023–24/2024–25 세 시즌을 덮고 서비스·권리가 보존되면 own Bird다. 기존 네 시즌의 완료가 새 UPC보다 앞서야 하며 fiscal June30을 정확 서비스 만료일로 바꾸지 않는다.',
      '- 기본 첫해 최대는 max(30% C25,105%×21.08m)=$46,394,100이다. 35% Designated Veteran는 별도 적격 이력·Higher Max 조건 포트다. 개인 수상을 선택하거나 30%를 모든 가능한 계약의 절대최대로 부르지 않는다.',
      '- 새 UPC 작업일은 2025-07-07 12:02 ET다. 법정 최대5시즌/첫해 기준 8% 인상에 따라 계산한다. 1997-05-22 생일 기준 최장 후보도 Over38 창에 들지 않는다.',
      '- 최소연봉은 2025 서명연도의 8YOS 각 계약연차 표다. ExhibitC×C25/C22의 미반올림 참고 함수와 법정 minimum 충족 조건을 기록하며, 공식 조정표·정확 rounding 인증은 하지 않는다. 30m 이상인 제안은 minimum 준수 범위에서 실행한다.', '',
      '## 동일 claim의 hold·슬롯·6비용', '',
      '원 신규 M1 bonus0 조건에서 prior Salary21.08m를 사용한다. FY24 Estimated Average와 비교한 normal hold 두 분기는 $31,620,000/$40,052,000이며 법정 min/max clip을 유지한다. 평균값을 임의 선택하지 않는다. UFA hold는 apron에서 제외한다. 재서명 전 normal hold를 유지하고, 유효 UPC 당일 그 한 hold를 새 급여로 한 번만 교체한다. Markkanen은 이 non-RSC/8YOS 종료에서 새 QO·ROFR 대상이 아니다.', '',
      '다른 STD가 14 이하인 당일 새 Mark UPC STD1/TW0이 가능하다. 다른 만료선수를 살려 둔 FY25 전체15명을 이미 구성했다고 주장하지 않는다. 여름 최대21·정규 일반14/15 및 경기 active/bench 규칙은 후속 명단에서 따로 충족한다.', '',
      '|범주|보존·반환 범위|','|---|---|']
    for c in o['cost_family']['six_categories']:lines.append(f"|{c['id']}|{c['normal']}; apron: {c['apron']}. {c['scope']}|")
    lines += ['', 'R25/다른 live·FA·신인·예외는 typed 미가격 입력이다. 이전 R24 상단을 FY25 전체부채 상단으로 자동 복사하지 않는다. 미보고 새 미래분쟁을 무한 추가하는 가족이나 사적 부재증명을 새 gate로 요구하지 않는다. 실제 full cash/Tax bill/전체 FY25 비용 상단은 null이다. 새 Bird 자체는 apron hardcap trigger가 없지만 다른 당해·직전 postseason trigger의 적용 apron을 보존한다. apron 초과만으로 위법이라고 하지 않는다. 이후 재양도는 VII8·matching·apron 조건을 별도로 확인한다.', '',
      '## 원문·현행성', '',
      f'[NBA Communications 2025 발표]({CAP_URL})는 cap $154.647m, tax $187.895m, 1차/2차 apron $195.945m/$207.824m, 공개 floor $139.182m, 세 MLE $14.104m/$5.685m/$8.781m와 July6 noon 종료를 명명한다. 공개 floor의 표시값을 90% 계산의 정확 센트로 바꾸지 않는다.', '',
      f'[2023 NBA–NBPA CBA]({CBA_URL}): I1(yy)/(iiii)/minimum 정의, II3/4/6/7, VII2(e)/4(d)/5(a)(2)/6(b)/(n), IX1, XI4(b), XII, XXIX. 직접 읽은 PDF 쪽과 text/raw SHA는 JSON primary에 있다. [NBA Markkanen 프로필](https://www.nba.com/player/1628374/lauri-markkanen)은 생일·2017 지명 식별만 사용했다.', '',
      '원 M1 canon→2021 비용의 명명된 새 UPC→2022/2023/2024 selected continuation 행을 각각 물리핀·의미로 확인한다. 새 producer는 반환 후 fresh physical source를 다시 읽고 핵심 salary/hold/Γ/authority를 caller에서 검문한다. writer 통제는 독립 검문으로 세지 않는다. 독립 수용 전 REVIEW_PENDING, 추천/선택/actual consent를 구분한다.', '',
      '## 진행표', '', '|단계|현행 상태|','|---|---|','|1|완료|','|2|완료|','|3|완료·원 유한 계약가족|','|4|후기 역할·선택 좌표 미완료; 이번 갱신은 후보 검문|','|5|설정집 미완료|','|6|집필규격·Context Pack 미완료|','|7|통합·독립·최종승인 CLOSED|','',
      '미완료4/6번까지3. 기존 franchise/MVP/title/retirement 및 실제 2025 가격·건강·경기 결과는 선택하지 않았다. Pack0·원고0·전체 커리어/A10 완료false.', '']
    return '\n'.join(lines)

def self_test():
    base=build(); tests=[]
    def rejected(label, helper, obj):
        with patch(__name__+'.'+helper, return_value=obj):
            try:build()
            except AssertionError:tests.append(label);return
        raise AssertionError('FALSE_PASS '+label)
    x=copy.deepcopy(base['candidates']);x[1]['salary_by_capyear']['2027']=45002_000
    rejected('compound_or_wrong_raise', 'candidates', x)
    x=copy.deepcopy(base['candidates']);x[0]['original_Gamma_preserved']=False
    rejected('original_Gamma_erased','candidates',x)
    x=copy.deepcopy(base['cost_family']);x['FA_hold_cases'][0]['normal']=0
    rejected('expired_FA_hold_erased','costs',x)
    x=copy.deepcopy(base['cost_family']);x['hardcap_condition']='Own Bird always triggers first-apron hardcap'
    rejected('Bird_hardcap_reversal','costs',x)
    x=copy.deepcopy(base['primary']);x['source_scope']='NBA exact private receipt certified'
    rejected('primary_authority_promotion','primary',x)
    x=copy.deepcopy(base['cost_family']);x['six_categories'][1]['normal']='0';x['six_categories'][1]['apron']='0'
    rejected('returned_old_Gamma_both_charge_erased','costs',x)
    return tests

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    o=build()
    if a.write:
        (ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        (ROOT/MD).write_text(md(o),encoding='utf8')
    current=(ROOT/OUT).exists() and json.loads((ROOT/OUT).read_text(encoding='utf-8-sig'))==o and norm((ROOT/MD).read_bytes())==md(o).encode()
    if a.check:assert current,'Saved JSON/MD stale'
    print(json.dumps({'current':current,'forms':len(o['candidates']),'self_tests':self_test() if a.self_test else []},ensure_ascii=False))

if __name__=='__main__':main()
