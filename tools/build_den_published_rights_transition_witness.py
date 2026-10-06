"""Audit the positive published DEN rights read-set, without whole-row promotion.

This compiles four existing cap-analyst rows and one NBA rule. It does not
make unspecified contract predicates members of the domain, select exact
terms, or revive the rejected complete-economic-relation projection proof.
"""
import argparse
import copy
import hashlib
import json
import itertools
import re
from pathlib import Path
from unittest.mock import patch

import fitz
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_den_published_rights_transition_witness.py'
OUT = 'research/DEN_PUBLISHED_RIGHTS_TRANSITION_WITNESS_2026_10_07.json'
MD = OUT[:-5] + '.md'
BASELINE = 'ae7678e224e842a7598cc733e49bd14e81be80d2'
PINS = {
    'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2',
    'canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json': 'e0d8ed1f82c494a3610a91c779eef5573737f9b818088c903786cb12afae7dc9',
    'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json': 'c0166bba7a0874aa08dfa88e7d00c0f0d0e237ca2090459ddd6167cf1353c5ea',
    'research/DEN_COMPLETE_RIGHTS_EXISTENCE_SCOPE_AUDIT_2026_10_07.json': '23d8fcbd15cf9e23f954358cd8343ec949b0daf7d9df5865f76700317329fcd1',
    'simulation/CAUSALITY_MODEL.md': '00638830864e9503db4589464806cc0c4c0d94002b039a8bf661d96e6f6a7c45',
}
BI = Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-denver-cost-2026-10-06/BI_DEN_archive.html')
BI_SHA = 'd6a41cd3209a62c428578ea14c7acc1fe7338df4c206bf871b8e4de41b5af942'
BYLAWS = Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-2019-bylaws.pdf')
BYLAWS_SHA = '6accb3d9633e15e8559d13228c27ae7b3b0b81eac0894050b06256eea6da3464'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def normalized(path):
    return path.read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def read_bytes(path):
    return path.read_bytes()


def read_json(path):
    return json.loads(normalized(ROOT / path))


def collect():
    b = read_bytes(BI)
    assert digest(b) == BI_SHA, 'original analyst raw body changed'
    soup = BeautifulSoup(b, 'html.parser')
    lis = [(i, li.get_text(' ', strip=True)) for i, li in enumerate(soup.find_all('li'))]
    rules = {
        'P': ('2023', 'first-rounder', 'Oklahoma City Thunder'),
        'G': ('2025', 'first-rounder', 'Orlando Magic'),
        'F5_2023': ('2023', 'second-rounder', 'Cleveland Cavaliers'),
        'F5_2027': ('2027', 'second-rounder', 'Cleveland Cavaliers'),
    }
    rows = {}
    for key, tokens in rules.items():
        found = [(i, s) for i, s in lis if s.startswith(tokens[0]) and all(t in s for t in tokens[1:])]
        assert len(found) == 1, 'published future-pick row not unique: ' + key
        i, text = found[0]
        rows[key] = {'html_li_zero_based': i, 'text_sha256': digest(text.encode()), 'authority': 'ORIGINAL_CAP_ANALYST_REPORTED_INPUT_NOT_EXACT_CONTRACT'}
        if key == 'P':
            assert 'lottery protected through 2025' in text and '2025 and 2026 second-rounders' in text
        if key == 'G':
            assert 'two years after the obligation' in text and 'top-5 protected through 2027, otherwise does not convey' in text
        if key == 'F5_2023':
            assert 'top-46 protected' in text
    raw = read_bytes(BYLAWS)
    assert digest(raw) == BYLAWS_SHA, 'NBA by-laws raw body changed'
    doc = fitz.open(stream=raw, filetype='pdf')
    text = doc[86].get_text().replace('\r\n', '\n').replace('\r', '\n')
    assert '7.03. First Round Draft Choice.' in text
    assert 'two (2)' in text and 'consecutive future NBA Drafts' in text
    return rows, digest(text.encode())


def first_projection_cases():
    """Only the named P/G pair; no assumption that other first-round claims vanish."""
    cases = []
    for p in [2023, 2024, 2025]:
        for g in list(range(p + 2, 2028)) + [None]:
            cases.append({'P_branch': 'FIRST_CONVEYS', 'P_first_year': p, 'G_first_year': g,
                          'named_firsts_not_adjacent': g is None or g - p >= 2,
                          'G_start_relation': 'P_FIRST_DELIVERY_YEAR_PLUS_TWO_OR_LATER_ROLLOVER'})
    # The wording of P's "obligation" after conversion is not numerically fixed.
    # This over-envelope tests every published G year and no-conveyance, without
    # asserting that every envelope member is an actual contracted live branch.
    for g in [2025, 2026, 2027, None]:
        cases.append({'P_branch': 'CONVERTS_TO_SECONDS', 'P_first_year': None, 'G_first_year': g,
                      'named_firsts_not_adjacent': True,
                      'G_start_relation': 'BROAD_REPORTED_YEAR_ENVELOPE_NOT_POSITIVE_CONVERTED_LINK'})
    return cases


def public_protection_transitions():
    """Exhaust the published rank-predicate cells, not private contract programs.

    A bit is a protected outcome, not an adopted future pick or lottery result.
    P conversion's unresolved obligation date is over-covered by all reported
    G start years and no start; no exact converted-link clause is selected.
    """
    cells = []
    for pbits in itertools.product([False, True], repeat=3):
        pyear = next((2023 + i for i, protected in enumerate(pbits) if not protected), None)
        starts = [pyear + 2] if pyear is not None else [2025, 2026, 2027, None]
        for start in starts:
            for gbits in itertools.product([False, True], repeat=3):
                gyear = next((2025 + i for i, protected in enumerate(gbits)
                              if start is not None and 2025 + i >= start and not protected), None)
                retained_seconds = [2025, 2026] if pyear is None else []
                assert pyear is None or gyear is None or gyear - pyear >= 2
                assert not set(retained_seconds) & {2023, 2027}
                cells.append({'P_protected_predicate_bits_2023_25': list(pbits),
                              'P_first_delivery': pyear, 'P_second_conversion_years': retained_seconds,
                              'G_candidate_start_envelope': start,
                              'G_protected_predicate_bits_2025_27': list(gbits),
                              'G_first_delivery': gyear,
                              'source_pinned_P_first_holder': 'OKC',
                              'source_pinned_G_first_holder': 'ORL',
                              'source_pinned_P_conversion_holder': 'OKC',
                              'source_pinned_P_conversion_years_if_triggered': [2025,2026],
                              'source_pinned_F5_holder_and_years': {'holder':'CLE','years':[2023,2027]},
                              'named_first_pair_nonadjacent': True,
                              'P_conversion_supply_disjoint_from_F5_deleted_years': True})
    assert len(cells) == 88
    return cells


def completed_assignment_anchors():
    """Positive original named transactions, not unpublished complete terms."""
    p = Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-den-graph-2026-10-07/nov2020-fourteam-release.html')
    raw = read_bytes(p)
    want = '1d8fd539e7ec135a335622256de4bc7d662d5c470a6fd61a078767d0dba70938'
    assert digest(raw) == want
    soup = BeautifulSoup(raw, 'html.parser')
    paragraphs = [a.get_text(' ', strip=True) for a in soup.find_all('p')]
    found = [a for a in paragraphs if 'Denver has acquired the draft rights to R.J. Hampton' in a
             and 'Oklahoma City has acquired a future first round draft pick (via Denver)' in a]
    assert len(found) == 1, 'original P assignment paragraph not unique'
    ptext = found[0]
    common = [a for a in paragraphs if 'two future first round draft picks from Milwaukee' in a
              and 'swap two additional first round picks with the Bucks' in a]
    assert len(common) == 1
    g = Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-den-primary-2026-10-07/ORL_2223.pdf')
    grow = read_bytes(g)
    gwant = '63550e97068a14cbd60d8b461d1f15c0bb898652c9813fdbfa113509f5a8f92c'
    assert digest(grow) == gwant
    page = fitz.open(stream=grow, filetype='pdf')[115].get_text().replace('\r\n', '\n').replace('\r', '\n')
    compact = re.sub(r'\s+', ' ', page)
    assert 'March 25, 2021' in compact
    assert 'R.J. Hampton, Gary Harris and a future first round draft pick from Denver' in compact
    assert 'in exchange for Gary Clark and Aaron Gordon' in compact
    return {
        'P': {'url': 'https://www.nba.com/news/pelicans-acquire-steven-adams-eric-bledsoe-in-4-team-trade-jrue-holiday-to-milwaukee',
              'cache_path': str(p), 'raw_sha256': want,
              'locator': 'single original completion paragraph naming Denver Hampton and OKC Denver future first',
              'paragraph_sha256': digest(ptext.encode()),
              'other_positive_common_first_and_swap_claims': {
                  'promisor': 'MIL', 'recipient': 'NOP', 'future_first_count': 2,
                  'future_first_swap_count': 2, 'paragraph_sha256': digest(common[0].encode()),
                  'exact_years_and_protection': None,
                  'preserved_as_same_original_public_claim_objects': True,
                  'not_assumed_absent': True},
              'scope': 'Positive original completed named P assignment and rights counterparty, not full original conditions'},
        'G': {'url': 'https://cdn.nba.com/teams/uploads/sites/1610612753/2022/11/orlando-magic-media-guide-2022-23.pdf',
              'cache_path': str(g), 'raw_sha256': gwant, 'pdf_page_one_based': 116,
              'printed_pages': [228, 229], 'page_text_sha256': digest(page.encode()),
              'locator': 'All-time transactions March 25 2021',
              'scope': 'Original Gordon/Clark named assignment with DEN future first, not post-divergence preservation proof'},
        'original_actual_nonempty_implementation_supported': True,
        'original_completion_implies_F5_deletion_full_relation_monotone': False,
        'original_24_pick_identity_reused_in_alternate_Nnaji_selection': False,
    }


def named_other_obligations():
    raw = read_bytes(BI)
    assert digest(raw) == BI_SHA
    lis = [(i, li.get_text(' ', strip=True))
           for i, li in enumerate(BeautifulSoup(raw, 'html.parser').find_all('li'))]
    out = []
    for year, tokens in [(2021, ['second-rounder', 'Oklahoma City Thunder']),
                         (2022, ['Philadelphia 76ers', 'swap second-rounders',
                                 'Minnesota Timberwolves', 'Miami HEAT'])]:
        found = [(i, text) for i, text in lis if text.startswith(str(year))
                 and all(token in text for token in tokens)]
        assert len(found) == 1
        i, text = found[0]
        out.append({'year': year, 'round': 2, 'html_li_zero_based': i,
                    'text_sha256': digest(text.encode()),
                    'priority_and_swap_output': 'SAME_ORIGINAL_SYMBOLIC_OBJECT_UNCHANGED',
                    'actual_numerical_order_or_final_holder': None,
                    'disjoint_from_P_conversion_and_F5_removed_years': True})
    assert {o['year'] for o in out}.isdisjoint({2023, 2025, 2026, 2027})
    return out


def public_legal_frame(cells):
    """Construct the changed-resource frame of the accepted public-rule family.

    Public P/G decisions read protection bits and P resolution. They do not read
    the two omitted F5 assignments. The family is explicitly these sourced
    economic components, not every imagined private contract program.
    Other original first coverage stays symbolic and is never set to zero.
    """
    years = list(range(2021, 2029))
    first_checks = 0
    resource_checks = 0
    for cell in cells:
        named = {y for y in [cell['P_first_delivery'], cell['G_first_delivery']] if y is not None}
        assert len(named) == sum(y is not None for y in [cell['P_first_delivery'], cell['G_first_delivery']])
        old_alloc = resolve_public_assignments(cell, [True, True])['first_allocations']
        new_alloc = resolve_public_assignments(cell, [False, False])['first_allocations']
        assert_public_allocation_policy(cell, [True, True], resolve_public_assignments(cell, [True, True]))
        assert_public_allocation_policy(cell, [False, False], resolve_public_assignments(cell, [False, False]))
        deltas = {}
        for team in ['DEN', 'OKC', 'ORL']:
            def net_first(allocations, year):
                return sum(int(a['to'] == team)-int(a['from'] == team)
                           for a in allocations if a['year'] == year)
            deltas[team] = {y: net_first(new_alloc,y)-net_first(old_alloc,y) for y in years}
        assert all(delta == 0 for v in deltas.values() for delta in v.values())
        for bits in itertools.product([False, True], repeat=len(years)):
            # Bits already include every common ownership/priority/retention
            # effect. The theorem transfers a predicate; it does not certify
            # every arbitrary original bit vector to be legally executable.
            original = dict(zip(years, bits))
            stepien = lambda v: all(v[a] or v[b] for a, b in zip(years, years[1:]))
            for team, delta in deltas.items():
                candidate = {y: int(original[y])+delta[y] for y in years}
                assert all(v in [0,1] for v in candidate.values())
                assert stepien(original) == stepien(candidate)
            first_checks += 1
        for f5_2023_conveys, f5_2027_conveys in itertools.product([False, True], repeat=2):
            # 2027's public unqualified label is not selected as an exact
            # unprotected contract; both resource possibilities are covered.
            freed = {2023: int(f5_2023_conveys), 2027: int(f5_2027_conveys)}
            p_conversion = set(cell['P_second_conversion_years'])
            assert p_conversion.isdisjoint(freed)
            assert all(v >= 0 for v in freed.values())
            original_assignments = resolve_public_assignments(cell, [f5_2023_conveys, f5_2027_conveys])
            candidate_assignments = resolve_public_assignments(cell, [False, False])
            assert_public_allocation_policy(cell, [f5_2023_conveys, f5_2027_conveys], original_assignments)
            assert_public_allocation_policy(cell, [False, False], candidate_assignments)
            assert original_assignments['first_allocations'] == candidate_assignments['first_allocations']
            assert original_assignments['P_conversion_allocations'] == candidate_assignments['P_conversion_allocations']
            assert candidate_assignments['F5_allocations'] == []
            assert len(original_assignments['F5_allocations']) == sum(freed.values())
            resource_checks += 1
    return {
        'source_supported_family': 'POSITIVE_P_G_PROTECTION_RESOLUTION_TERMINATION_AND_NAMED_SECOND_CLAIMS',
        'scope_adopted_by_root_review': True,
        'scope_is_new_author_financial_selection': False,
        'quantifiers': 'Every actual admissible input of the accepted public economic family lies in the tested protection over-envelope. For that input, the same public P/G allocation and omission of F5 seconds preserves the necessary legal predicates. Original completed assignments anchor a nonempty implementation; no arbitrary envelope cell is asserted an actual lawful contract.',
        'actual_admissible_public_rule_family_is_subset_of_tested_envelope': True,
        'all_88_envelope_cells_asserted_actual_contract_branches': False,
        'all_88_envelope_cells_asserted_lawful_executions': False,
        'first_coverage_years': years,
        'all_first_coverage_boolean_vectors_tested_per_cell': 256,
        'first_retention_predicate_comparisons': first_checks,
        'named_actor_net_first_allocation_deltas_derived_not_assumed': True,
        'source_expected_holder_year_round_promisor_policy_guarded': True,
        'first_retention_named_actor_predicate_evaluations': first_checks * 3,
        'public_second_resource_frame_cases': resource_checks,
        'first_retention_predicate_identical_for_all_symbolic_common_states': True,
        'symbolic_common_retention_identity_applies_to_every_team': True,
        'arbitrary_common_state_asserted_lawful': False,
        'other_common_first_rights_or_priority_assumed_zero': False,
        'common_nonfirst_allocations_preserved_by_public_rule_identity': True,
        'freed_F5_second_resources_may_be_left_unused': True,
        'P_first_and_G_first_demand_unchanged': True,
        'P_conversion_second_demand_unchanged_and_disjoint_from_F5': True,
        'no_new_second_or_first_obligation_created_by_F5_omission': True,
        'all_teams_named_first_projections_preserved': ['DEN', 'OKC', 'ORL'],
        'other_teams_common_dated_claims_preserved': ['MIL', 'NOP', 'PHI', 'MIN', 'MIA', 'HOU'],
        'CLE_named_F5_conditional_second_assignments_omitted': True,
        'source_anchor_inference': 'Completed original NBA assignments provide the nonempty public economic template. By-Laws7.03 regulates possible consecutive-first losses, so preservation of the entire first-retention predicate transfers that legal constraint without asserting all arbitrary states lawful.',
        'forbidden_shortcut': 'Neither original completion alone nor Dret<=C supplies a full private-contract deletion theorem. The constructed witness uses the accepted positive public rule read-set and its actual changed-resource frame.',
        'complete_public_legal_implementation_witness': True,
        'full_original_private_contract_relation_certified': False,
        'exact_future_outputs_of_all_private_functions_required': False,
        'three_branches': {'P_CONVEYS': 'same protected first allocation to OKC',
                           'P_CONVERTS': 'same conditional 2025/2026 second allocations to OKC',
                           'G': 'same P-linked protected first or terminal no-conveyance to ORL'},
        'actual_terms': None, 'actual_acceptance': None, 'actual_future_delivery': None,
        'REGISTER_promotion': False,
        'application_theorem': [
            'First establish source-correct promisor/holder/year/round allocations in every public protection envelope cell.',
            'Interpret the original F5 assignments and candidate omission separately; derive net first deltas of zero for DEN/OKC/ORL and unchanged common first/swap objects of all other teams.',
            'Apply that derived equality to every original common first-retention state. The predicate is preserved; arbitrary original states are not all asserted lawful.',
            'Use the positive completed original public economic template as the lawful nonempty anchor, then transfer only this preserved public legal constraint to the actual admissible family subset.',
            'Keep every positive common second allocation and the P25/26 conversion allocation; remove only distinct F5 23/27 assignments and leave freed resources unused.',
        ],
        'local_13_pair_projection_alone_is_not_the_whole_application_theorem': True,
        'whole_source_coverage_is_not_actual_22528_contract_certificates': True,
    }


def resolve_public_assignments(cell, f5_delivery_bits):
    """Source-scoped public allocation policy, separately applied to each frame.

    The input P/G protection decisions are computed from source predicates;
    F5 has two distinct second-round payloads. No ownership-read portfolio
    function from the rejected full-private AST theorem is used here.
    """
    pbits = cell['P_protected_predicate_bits_2023_25']
    gbits = cell['G_protected_predicate_bits_2025_27']
    pyear = next((2023+i for i, protected in enumerate(pbits) if not protected), None)
    start = normalize_public_G_start(pyear+2 if pyear is not None else cell['G_candidate_start_envelope'])
    gyear = next((2025+i for i, protected in enumerate(gbits)
                  if start is not None and 2025+i >= start and not protected), None)
    assert pyear == cell['P_first_delivery'] and gyear == cell['G_first_delivery']
    return {
        'first_allocations': [{'from': 'DEN', 'to': to, 'year': y, 'round': 1}
                              for y, to in [(pyear, 'OKC'), (gyear, 'ORL')] if y is not None],
        'P_conversion_allocations': ([{'from': 'DEN', 'to': 'OKC', 'year': y, 'round': 2}
                                      for y in [2025, 2026]] if pyear is None else []),
        'F5_allocations': [{'from': 'DEN', 'to': 'CLE', 'year': y, 'round': 2}
                           for y, conveys in zip([2023, 2027], f5_delivery_bits) if conveys],
    }


def normalize_public_G_start(start):
    """The positive public terminal makes every start after 2027 no-convey.

    This collapses an unbounded date interval by a source-stated termination,
    not by guessing an actual conversion resolution year or new second debt.
    """
    assert start is None or isinstance(start, int) and start >= 2025
    return None if start is None or start > 2027 else start


def assert_public_allocation_policy(cell, flags, allocations):
    """Independent positive-source semantic guard, not equal wrong outputs."""
    expected_first = []
    if cell['P_first_delivery'] is not None:
        expected_first.append({'from':'DEN','to':'OKC','year':cell['P_first_delivery'],'round':1})
    if cell['G_first_delivery'] is not None:
        expected_first.append({'from':'DEN','to':'ORL','year':cell['G_first_delivery'],'round':1})
    expected_conversion = ([{'from':'DEN','to':'OKC','year':y,'round':2} for y in [2025,2026]]
                           if cell['P_first_delivery'] is None else [])
    expected_f5 = [{'from':'DEN','to':'CLE','year':y,'round':2}
                   for y, flag in zip([2023,2027],flags) if flag]
    assert allocations == {'first_allocations':expected_first,
                           'P_conversion_allocations':expected_conversion,
                           'F5_allocations':expected_f5}, 'allocation differs from positive source policy'


def legal_procedure_sources():
    raw = read_bytes(BYLAWS)
    assert digest(raw) == BYLAWS_SHA
    bylaws = fitz.open(stream=raw, filetype='pdf')
    bt = {n: bylaws[n-1].get_text().replace('\r\n', '\n').replace('\r', '\n')
          for n in [72, 73, 87]}
    assert 'terms and conditions' in bt[72] and 'Trade Call' in bt[72]
    assert 'not disclosed to' in bt[72] and 'not be enforceable' in bt[72]
    assert 'Trade Memorandum shall govern' in bt[73]
    assert 'consecutive future NBA Drafts' in bt[87]
    cp = Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-2017-cba.pdf')
    cb = read_bytes(cp)
    want = '66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
    actual = digest(cb)
    assert actual == want, 'original CBA raw changed'
    cd = fitz.open(stream=cb, filetype='pdf')
    ct = {n: cd[n-1].get_text().replace('\r\n', '\n').replace('\r', '\n') for n in [302,303]}
    assert 'Draft shall consist of two (2) rounds' in ct[302]
    assert 'exclusive right to negotiate' in ct[303]
    return {'NBA_BYLAWS': {'raw_sha256': BYLAWS_SHA, 'pdf_pages': [72,73,87],
                           'page_text_sha256': {str(n):digest(t.encode()) for n,t in bt.items()},
                           'scope': 'Trade procedure/disclosure to league and first-retention predicate; not public private terms certificate'},
            'CBA2017': {'url':'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf',
                        'cache_path':str(cp),'raw_sha256':actual,'pdf_pages':[302,303],
                        'page_text_sha256':{str(n):digest(t.encode()) for n,t in ct.items()},
                        'scope':'Draft rounds and exclusive negotiating-right rules; no actual medical/financial/registration certification'}}


def build():
    for p, want in PINS.items():
        assert digest(normalized(ROOT / p).encode()) == want, 'reviewed source changed: ' + p
    s2 = read_json('canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json')
    assert s2['status'] == 'AUTHOR_SELECTED_S2_STANDARD_ONLY'
    prior = read_json('research/DEN_COMPLETE_RIGHTS_EXISTENCE_SCOPE_AUDIT_2026_10_07.json')
    assert prior['status'] == 'CONDITIONAL_RELATION_LEMMA_VALID_WHOLE_BRANCH_PROMOTION_REJECTED'
    assert prior['authority']['whole_branch_source_verified'] is False
    assert prior['authority']['new_asset_PASS'] == 0
    # Positive BI rule names P/OKC, not F5. This pins the consumed semantic
    # reference only; it is not a full revalidation of the rejected prior proof.
    refs = prior['joint_public_graph']['retained_contract_objects']
    assert refs['theta.P']['resolution_event'] == 'theta.P.full_original_resolution_event'
    assert refs['theta.G']['prior_resolution_ref'] == 'theta.P.full_original_resolution_event'
    assert refs['theta.G']['promisor'] == 'DEN' and refs['theta.G']['assignee'] == 'ORL'
    rows, page_sha = collect()
    cases = first_projection_cases()
    transitions = public_protection_transitions()
    anchors = completed_assignment_anchors()
    others = named_other_obligations()
    legal_frame = public_legal_frame(transitions)
    procedures = legal_procedure_sources()
    assert all(c['named_firsts_not_adjacent'] for c in cases)
    return {
        'schema': 'DEN_PUBLISHED_RIGHTS_TRANSITION_WITNESS_V1',
        'status': 'COMPLETE_PUBLIC_RIGHTS_LEGAL_EXISTENCE_WITNESS_INDEPENDENT_REVIEW_PENDING',
        'baseline_main': BASELINE,
        'source_sha256': {**PINS, SELF: digest(normalized(ROOT / SELF).encode())},
        'source_hash_convention': 'REPOSITORY_UTF8_NO_BOM_CRLF_CR_TO_LF;CACHE_RAW_BYTES',
        'source_records': {
            'ORIGINAL_COMPLETED_ASSIGNMENTS': anchors,
            'LEGAL_PROCEDURES': procedures,
            'BI': {'url': 'https://web.archive.org/web/20210422002709id_/https://www.basketballinsiders.com/denver-nuggets-team-salary/',
                   'cache_path': str(BI), 'raw_sha256': BI_SHA, 'capture': '2021-04-22', 'body_updated': '2021-04-20',
                   'scope': 'Four positive published future-pick list rows; not all private terms or a pre-trade snapshot', 'rows': rows},
            'NBA_BYLAWS': {'url': 'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf',
                           'cache_path': str(BYLAWS), 'raw_sha256': BYLAWS_SHA, 'pdf_page': 87, 'printed_page': 78,
                           'section': '7.03', 'page_text_sha256': page_sha,
                           'scope': 'First-round two-consecutive-future-drafts constraint; not whole-contract deletion monotonicity'},
        },
        'positive_reported_rule_components': {
            'P': {'promisor': 'DEN', 'recipient': 'OKC', 'first_years': [2023, 2024, 2025],
                  'protection_predicate': 'LOTTERY_PROTECTED', 'first_protection_terminal_year': 2025,
                  'conversion_seconds': [2025, 2026], 'reported_reads': ['P.first_pick_protection_result', 'P.year', 'P.conversion_event']},
            'G': {'promisor': 'DEN', 'recipient': 'ORL', 'published_first_year_label': 2025,
                  'start_relation': 'TWO_YEARS_AFTER_OKC_OBLIGATION', 'protection_predicate': 'TOP_FIVE_PROTECTED',
                  'first_terminal_year': 2027, 'terminal_reported_outcome': 'DOES_NOT_CONVEY',
                  'reported_reads': ['P.obligation_event', 'G.year', 'G.first_pick_protection_result'],
                  'meaning_of_P_obligation_after_conversion': None,
                  'actual_conversion_to_G_start_selected': None},
            'F5_2023': {'claim_round': 2, 'year': 2023, 'reported_protection': 'TOP_46', 'omitted_by_approved_F5': True},
            'F5_2027': {'claim_round': 2, 'year': 2027, 'reported_protection': None,
                        'null_does_not_certify_unprotected_exact_contract': True, 'omitted_by_approved_F5': True},
        },
        'dependency_findings': {
            'classification': 'REPORTED_RULE_COMPONENT_MODEL_NOT_FULL_CONTRACT_READSET_CERTIFICATE',
            'positive_G_reference_names_P_obligation': True,
            'F5_deletion_changes_named_second_claims_only': True,
            'P_conversion_years_disjoint_from_deleted_F5_years': sorted(set([2025, 2026]) & set([2023, 2027])) == [],
            'G_reported_terminal_is_no_conveyance_not_new_second_compensation': True,
            'absence_of_F5_tokens_proves_no_private_dependency': False,
            'all_hidden_predicates_added_to_domain': False,
            'full_actual_contract_read_set_certified': False,
            'all_other_original_burdens_assumed_zero': False,
        },
        'named_first_pair_projection': {
            'cases': cases, 'case_count': len(cases),
            'all_named_pair_cases_avoid_adjacent_outgoing_firsts': True,
            'conversion_envelope_is_actual_complete_live_contract_domain': False,
            'other_first_pick_rights_or_encumbrances_assumed_absent': False,
            'whole_team_Stepien_certificate': False,
            'scope': 'Named pair component only. Unchanged other first-rights burdens remain original opaque state, not zero.',
        },
        'f5_incremental_projection': {
            'within_declared_reported_components_first_round_projection_changed': False,
            'within_declared_reported_components_conversion_resource_years_changed': False,
            'all_exact_future_outputs_identical_required': False,
            'whole_relation_deletion_monotonicity_proved': False,
            'old_48_or_81_state_probes_repeated': False,
        },
        'published_rule_transition_witness': {
            'scope': 'ALL_POSITIVE_REPORTED_PROTECTION_PREDICATE_CELLS_AND_CONVERTED_START_OVER_ENVELOPE_ONLY',
            'cells': transitions, 'cell_count': len(transitions),
            'protected_rank_cells': {'P': {'protected': [1, 14], 'unprotected': [15, 30]},
                                     'G': {'protected': [1, 5], 'unprotected': [6, 30]}},
            'positive_G_read_reference': 'P/OKC obligation; source BI row G',
            'upstream_G_reference_semantically_pinned': True,
            'upstream_rejected_complete_relation_reconstructed': False,
            'named_first_round_rule_and_P_conversion_resource_checks_complete': True,
            'exact_converted_obligation_date_needed_for_these_checks': False,
            'retained_other_first_rights': 'ORIGINAL_UNCHANGED_SYMBOLIC_STATE_NOT_ZERO',
            'whole_team_Stepien_from_named_pair_alone': False,
            'scope_admissibility': 'ROOT_ACCEPTED_PUBLIC_ECONOMIC_LEGAL_EXISTENCE_SCOPE; independent witness review pending; not full private-contract relation preservation',
            'actual_F5_dependency_or_original_illegal_branch_found': False,
            'new_exact_protection_or_future_delivery_selected': False,
            'whole_asset_row_certified': False,
        },
        'other_positive_named_claims_preserved': others,
        'whole_public_legal_implementation_witness': legal_frame,
        'positive_rule_scope_and_source_boundary': {
            'root_scope_judgment': 'Original S2 legal-existence domain is the source-supported public economic template; full private AST invariance and every unreported portfolio function are not additional mandatory gates.',
            'NBA_trade_call_all_terms_disclosure_not_public_all_terms_disclosure': True,
            'source_reported_link_P_obligation_not_F5_deletion': True,
            'whole_private_contract_monotonicity_assumed': False,
            'actual_receipt_or_recipient_consent_needed_for_this_witness': False,
            'P_resolution_exact_post_conversion_date_can_remain_symbolic': True,
            'future_rank_path_chosen': False,
            'G_post_2027_start_interval': {'condition': 'start_year > 2027',
                                          'source_positive_terminal': 'top-5 protected through 2027, otherwise does not convey',
                                          'normalization': 'NO_CONVEY_EQUIVALENCE_CELL',
                                          'all_integers_after_2027_share_no_eligible_delivery_year_through_terminal': True,
                                          'actual_start_year_selected': None,
                                          'new_unreported_G_second_conversion_added': False},
        },
        'remaining_minimum_gap': {
            'id': 'INDEPENDENT_COMPLETE_PUBLIC_LEGAL_EXISTENCE_WITNESS_REVIEW',
            'statement': 'The accepted public economic family has a complete constructed protection/resource/first-retention witness. Independent original-source and blind review are pending; no full-private relation theorem is claimed.',
            'exact_converted_future_year_required': False,
            'all_private_clauses_absence_required': False,
            'actual_receipt_consent_or_acceptance_required_for_this_legal_existence_scope': False,
            'next_finite_work': 'Independently inspect positive rule semantics, original completion/procedure anchors and all predicate/resource frame cases; root alone decides register promotion.',
        },
        'prior_conditional_relation_lemma_repromoted': False,
        'whole_branch_source_verified': False, 'whole_branch_complete_domain': True,
        'complete_domain_scope': 'ROOT_ACCEPTED_SOURCE_SUPPORTED_PUBLIC_ECONOMIC_FAMILY_ONLY',
        'whole_legal_pass': False, 'new_asset_PASS': 0,
        'actual_theta': None, 'actual_future_delivery': None, 'actual_acceptance': None,
        'new_exact_asset_or_financial_selection': False, 'register_promotion': False,
        'independent_review_completed': False, 'fresh_primary_documents_collected': 0,
        'tools': {'Antigravity': 'NOT_RUN', 'NotebookLM': 'NOT_RUN', 'Claude': 'NOT_RUN'},
        'manuscript_allowed': False, 'design_gate': 'CLOSED',
    }


def validate(data):
    try:
        expected = build()
    except (AssertionError, KeyError, OSError, ValueError) as exc:
        return ['source construction: ' + str(exc)]
    return [] if data == expected else ['public rule boundary differs from original-source reconstruction']


def render(d):
    return '\n'.join([
        '# DEN 공개 보호 규칙의 유한 전이 증인', '',
        '**상태:** `COMPLETE_PUBLIC_RIGHTS_LEGAL_EXISTENCE_WITNESS_INDEPENDENT_REVIEW_PENDING`. 전체 법적 PASS0, 기존 조건부 정리의 전체 승격 기각 유지. 공개 경제템플릿 가족의 법적 구현 존재만 검문한다.', '',
        '## 실제로 읽은 범위', '',
        '[기존 원 cap analyst 단면](https://web.archive.org/web/20210422002709id_/https://www.basketballinsiders.com/denver-nuggets-team-salary/)의 future-pick 네 행을 직접 대조했다. 업데이트4/20·수집단면4/22이며 새 원문 회수는 아니다. [원문 지문·구조 입력](DEN_PUBLISHED_RIGHTS_TRANSITION_WITNESS_2026_10_07.json)에 rawSHA, li 위치, 행텍스트SHA를 보존한다. 보고 모델이며 원계약 전문으로 승격하지 않는다.', '',
        '- P: 2023–25 보호되는 1R, 종료 뒤 2025·26의 2R 전환.',
        '- G: OKC 의무 뒤 두 해라는 연결, 2027까지 보호, 이후 전달 없음.',
        '- F5: 2023 조건부2R와 2027 2R. 승인된 거래 생략은 이 두 청구를 발생시키지 않는다. 두번째의 미공표 보호를 무조건 없음으로 고르지 않는다.', '',
        '## 보호·전환 규칙 검문', '',
        '[NBA 규약](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf) PDF87/인쇄78 §7.03과 대조했다. P 전달 뒤 G의 두 해 이상 간격 및 P 미전달 시 G 단일1R라는 named-pair 투영은 연속 두 해의 두 named 1R 방출을 만들지 않는다. 다른 1R 권리·부담은 0으로 놓지 않으며 팀 전체 Stepien 인증은 아니다.',
        f"- 공개 보고 범위의 투영 {d['named_first_pair_projection']['case_count']}개. 전환 뒤 G 개시의 정확 계약 의미는 미선택이며 넓은 보고연도 envelope를 실제 전분기 계약으로 인증하지 않는다.",
        '- P의 보고 전환2R 연도25/26과 삭제된 F5 연도23/27은 직접 겹치지 않는다. G의 보고 말단은 전달 없음이다. 이 긍정적 규칙 범위에서 첫픽 투영과 전환연도는 F5 삭제로 변하지 않는다.', '',
        '## 공개 규칙의 실제 보호 전이 증인', '',
        f"- P의 세 해 보호/비보호 입력과 G의 세 해 보호/비보호 입력을 전부 순회한 {d['published_rule_transition_witness']['cell_count']}개 과대포괄 전이를 별도로 생성했다. 실제 허용 공개가족은 이 envelope의 부분집합이며 모든 셀이 실제 계약분기 또는 합법적 실행이라고 주장하지 않는다. 숫자 미래순번은 선택하지 않는다.",
        '- P가1R을 전달하면 G는 두 해 뒤부터, P가2R로 전환하면 G개시를 보고연도25/26/27 및 미개시 전체로 과대포괄한다. 모든 셀에서 두 named1R 비인접과 전환2R25/26 대 삭제F5 23/27 불겹침을 직접 검사했다. 이 국소 검사에 전환 뒤 정확 obligation 완료일은 필요하지 않다.',
        '- 실제 BI의 긍정 참조가 P/OKC라는 점과 소비하는 상위 G참조를 의미로 고정했다. 기각된 상위 전체관계 증인을 전재구성하거나 재승격하지는 않는다.',
        '- 공개 규칙 가족의 국소 법적 구현과 실제 완전계약 관계 불변성은 구분한다. 원S2가 모든 가상 비공개 포트폴리오 함수를 자동 포함하는 것은 아니지만, 이88셀만으로 다른1R부담/전체팀 Stepien/원경제관계 단조성을 인증하지 않는다.', '',
        '## 공개 가족 전체의 법적 구현 증인', '',
        '- 총괄은 원S2의 검문 범위를 source-supported 공개 경제템플릿의 법적 구현 존재로 확인했다. 원비공개full AST나 모든 가상 미공표함수의 실제불변성을 새 필수게이트로 추가하지 않는다. 이는 새 정확 조항의 작가 잠금이 아니다.',
        '- 원NBA 2020년 완료 단락과 ORL공식guide의2021-03-25 양도 행을 실제읽어 원경제템플릿의 비어 있지 않은 선행 구현을 연결했다. By-Laws4.02/7.03과 CBA X3/X4를 직접대조했다. Trade Call에 조건을 고지한다는 규칙은 공개 보도자료에 모든 조건이 게시된다는 뜻이 아니다.',
        '- 같은 원NBA 완료 본문에 있는 MIL→NOP 미래1R두장·1Rswap두장도 원공통객체로 보존한다. 그 정확 연도/보호를 0이나 새 숫자로 대입하지 않는다. 다른 팀의 공통1R 보유판정에도 아래 변수 불변 논증이 적용된다.',
        '- 원보고의2021 DEN2R→OKC와2022 PHI/MIN/MIA swap/양도는 해당 해의 같은 우선권 객체로 보존한다. 이 해들은 P전환25/26·삭제F5 23/27과 겹치지 않는다. 실제 순번·말단 소유자는 선택하지 않는다.',
        '-88보호셀에서 원F5 자원운반4경우를 별도 해석해 P/G의1R배정과P전환2R배정이 동일하고 F5두2R배정만 사라지는 것을 검사한다. 해방 자원을 새 의무에 쓰지 않는 구현을 구성한다.',
        f"- 다른 모든 공통1R 보유/우선권 효과는 0으로 놓지 않고 원상태 변수로 보존한다. 각 보호셀의2021–28 first-retention256상태, 총{d['whole_public_legal_implementation_witness']['first_retention_predicate_comparisons']}번에서 연속 두 해 무픽 판정이 동일하다. 공개 second-resource frame은{d['whole_public_legal_implementation_witness']['public_second_resource_frame_cases']}경우다. 임의 원상태 전부가 합법이라고 주장하지 않고, 원합법 템플릿의 제도 제약을 같은1R투영으로 이월하는 증인이다.",
        '- 모든 팀의 공개1R 투영/공통 배정이 불변이고 F5의2R 공급만 감소하지 않는다. 이는 공개된 보호·해결·종료 참조 규칙에 대한 직접 전이 증명이며 기존 full 경제관계 Dret≤C 조건부 보조정리의 재승격이 아니다.', '',
        '- P전환 뒤 obligation 해결일의 실제 의미에 맞지 않는 envelope셀이 있을 수 있다. 법규 불변성은 넓은88셀 전체에서 검사했으므로 그보다 좁은 실제 허용 공개가족에 투영한다. 넓힌 셀을 새로운 G개시/정확조항/합법적q의 작가선택으로 채택하지 않는다.', '',
        '- 2027뒤의 가능한 G개시는 누락하지 않는다. 원보고의 긍정 종료문구 `top-5 protected through 2027, otherwise does not convey`로 시작연도>2027 전체구간은 전달없음 셀과 동치다. 정확 전환해결일을 선택하지 않으며, 미보고 G→2R재전환이나 새 계약개정은 원공개가족에 자동 추가하지 않는다.',
        '- 적용 순서는 공개 수령자/연도/round 정답확립→원/후보 배정의 first delta0 유도→모든 공통first-retention변수에 제도판정 동일성 적용이다. 13개 named-pair 국소 표나22,528번 비교를 실제계약 전체 인증으로 승격하지 않는다.', '',
        '## 남은 검수와 권위 경계', '',
        '완전한 공개 가족 증인을 독립 원문검문·blind반증에 넘길 준비가 됐다. 실제 모든 비공개 참조 입력의 부재나 full private 계약 단조성을 인증하지 않는다. 원장 승격은 총괄의 독립검문 뒤 별도로 처리한다.',
        '정확 미래출력의 동일성, 모든 숨은 조항의 무존재, 비공개 원장·접수·실동의는 새 필수요건으로 추가하지 않는다. 실제 미래 연도·보호·승낙은null이고 다음 검문도 공개 규칙/그 연결의 적용범위에 한정한다.', '',
        '재현: `python tools/build_den_published_rights_transition_witness.py --check --self-test`. 중앙/REGISTER·정본선택0·원고CLOSED. 외부 CLI 미실행, 독립 검문 대기.', '',
    ])


def self_test(data):
    mutations = [
        ('rejected_lemma_to_PASS', lambda z: z.update(whole_legal_pass=True)),
        ('private_absence_requirement', lambda z: z['remaining_minimum_gap'].update(all_private_clauses_absence_required=True)),
        ('converted_link_chosen', lambda z: z['positive_reported_rule_components']['G'].update(actual_conversion_to_G_start_selected=2027)),
        ('pair_to_whole_Stepien', lambda z: z['named_first_pair_projection'].update(whole_team_Stepien_certificate=True)),
        ('other_burdens_zero', lambda z: z['dependency_findings'].update(all_other_original_burdens_assumed_zero=True)),
        ('future_equivalence_required', lambda z: z['f5_incremental_projection'].update(all_exact_future_outputs_identical_required=True)),
        ('public_cells_to_whole_row', lambda z: z['published_rule_transition_witness'].update(whole_asset_row_certified=True)),
        ('G_reference_to_F5', lambda z: z['published_rule_transition_witness'].update(positive_G_read_reference='F5/2027 second obligation')),
        ('private_relation_false_certificate', lambda z: z['whole_public_legal_implementation_witness'].update(full_original_private_contract_relation_certified=True)),
        ('all_ambient_states_lawful', lambda z: z['whole_public_legal_implementation_witness'].update(arbitrary_common_state_asserted_lawful=True)),
        ('all_envelope_cells_actual_lawful', lambda z: z['whole_public_legal_implementation_witness'].update(all_88_envelope_cells_asserted_lawful_executions=True)),
        ('unreported_G_second_conversion', lambda z: z['positive_rule_scope_and_source_boundary']['G_post_2027_start_interval'].update(new_unreported_G_second_conversion_added=True)),
    ]
    for name, mutate in mutations:
        z = copy.deepcopy(data); mutate(z)
        assert validate(z), name
    actual_reader = read_bytes
    def altered(path):
        b = actual_reader(path)
        return b + b' changed' if path == BI else b
    with patch(__name__ + '.read_bytes', side_effect=altered):
        assert validate(data), 'raw source mutation'
    reader = read_json
    def wrong_ref(path):
        d = reader(path)
        if path == 'research/DEN_COMPLETE_RIGHTS_EXISTENCE_SCOPE_AUDIT_2026_10_07.json':
            d['joint_public_graph']['retained_contract_objects']['theta.G']['prior_resolution_ref'] = 'theta.F5_DEN2027_second'
        return d
    with patch(__name__ + '.read_json', side_effect=wrong_ref):
        assert validate(data), 'consumed upstream G semantic reference mutation'
    resolver = resolve_public_assignments
    def corrupted_allocations(cell, flags):
        ans = resolver(cell, flags)
        if flags == [False, False]:
            ans['first_allocations'].append({'from':'DEN', 'to':'CLE', 'year':2024, 'round':1})
        return ans
    with patch(__name__ + '.resolve_public_assignments', side_effect=corrupted_allocations):
        assert validate(data), 'F5 omission creates an unsourced first allocation'
    for label, kind in [('common P conversion year corruption','P'),
                        ('common G first recipient corruption','G')]:
        def shared_wrong_output(cell, flags):
            ans = resolver(cell, flags)
            if kind == 'P' and ans['P_conversion_allocations']:
                ans['P_conversion_allocations'][0]['year'] = 2024
            if kind == 'G':
                for a in ans['first_allocations']:
                    if a['to'] == 'ORL': a['to'] = 'CLE'
            return ans
        with patch(__name__ + '.resolve_public_assignments', side_effect=shared_wrong_output):
            assert validate(data), label
    assert normalize_public_G_start(2028) is None and normalize_public_G_start(1000000) is None
    resolver = resolve_public_assignments
    for cell in data['published_rule_transition_witness']['cells']:
        if cell['P_first_delivery'] is None and cell['G_candidate_start_envelope'] is None:
            beyond = copy.deepcopy(cell); beyond['G_candidate_start_envelope'] = 2028
            assert resolver(beyond,[False,False]) == resolver(cell,[False,False])
    return len(mutations) + 5


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    d = build()
    if args.write:
        (ROOT / OUT).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MD).write_text(render(d), encoding='utf-8')
    errors = validate(d)
    if args.check:
        saved = read_json(OUT); errors += validate(saved)
        if normalized(ROOT / MD) != render(saved): errors.append('Markdown stale')
    tests = self_test(d) if args.self_test else 0
    print(json.dumps({'current': not errors, 'errors': errors,
                      'named_projection_cases': d['named_first_pair_projection']['case_count'],
                      'negative_controls': tests, 'new_asset_PASS': 0}, ensure_ascii=False))
    if errors: raise SystemExit(1)


if __name__ == '__main__':
    main()
