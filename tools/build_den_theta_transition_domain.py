"""Finite ambiguity review of reported DEN pick calendars; not a legal certificate.

The two completions are hypothetical countermodels, not selected contract terms.
Historical raw caches and protected author/canonical files are read only.
"""
from pathlib import Path
from itertools import product
from collections import Counter
from copy import deepcopy
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
BASELINE_MAIN = '189dec0e39c7d05b1e1adf0cd4e95f55710679b7'
OUT = ROOT / 'research/DEN_THETA_TRANSITION_DOMAIN_2026_10_07.json'
MD = ROOT / 'reviews/DEN_THETA_TRANSITION_SCOPE_REVIEW_2026_10_07.md'
SOURCES = (
    'control/CHICAGO_2020_21_D1_S2_REGISTER.json',
    'control/CHICAGO_2020_21_D1_S2_PROTOCOL.md',
    'tools/check_chicago_d1_s2.py',
    'research/DEN_NAMED_CONDITIONAL_RIGHTS_WITNESS_2026_10_06.json',
    'research/DEN_NAMED_CONDITIONAL_RIGHTS_WITNESS_2026_10_06.md',
    'research/BOS_NAMED_RIGHTS_ASSIGNMENT_WITNESS_2026_10_06.json',
    'reviews/BOS_NAMED_RIGHTS_ASSIGNMENT_REVIEW_2026_10_06.md',
    'research/NBA_2021_L_ASSET_CHAIN_SOURCES.json',
    'simulation/NBA_2021_ASSET_CHAIN.md',
    'simulation/2020_DRAFT_ZEKE_NNAJI_RELANDING_BOARD.md',
    'canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json',
    'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json',
    'research/DEN_T1_T3_DATED_MATCHING_WITNESS_2026_10_06.json',
    'reviews/D1_DATED_EXECUTION_FOLLOWUP_REVIEW_2026_10_07.md',
)


def norm(path):
    return path.read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def load(path):
    return json.loads(norm(ROOT / path))


def sha(path):
    return hashlib.sha256(norm(path).encode()).hexdigest()


def rows():
    result = []
    # 2023/24 need only the lottery boundary; future Gordon cannot start before 2025.
    # 2025 needs both thresholds; 2026/27 need only the Gordon top-five boundary.
    for values in product((0, 1), (0, 1), (0, 1, 2), (0, 1), (0, 1)):
        cats = dict(zip(range(2023, 2028), values))
        prior = 2023 if cats[2023] == 1 else 2024 if cats[2024] == 1 else 2025 if cats[2025] == 2 else None
        completions = []
        for label in ('HYPOTHESIS_CONVERSION_RESOLVES_2025', 'HYPOTHESIS_FIRST_CONVEYANCE_TRIGGER_ONLY'):
            start = prior + 2 if prior else 2027 if label == 'HYPOTHESIS_CONVERSION_RESOLVES_2025' else None
            follow = next((year for year in range(start, 2028) if cats[year] >= 1), None) if start else None
            outgoing_firsts = sorted(year for year in (prior, follow) if year is not None)
            completions.append({
                'id': label, 'classification': 'HYPOTHETICAL_PUBLIC_PROJECTION_COMPLETION_NOT_CONTRACT',
                'first_eligible_year_within_reported_window': start,
                'Gordon_delivery_year': follow,
                'Gordon_no_first_delivery_in_2025_2027': follow is None,
                'prior_and_follow_only_no_adjacent_outgoing_firsts':
                    all(y - x >= 2 for x, y in zip(outgoing_firsts, outgoing_firsts[1:])),
                'whole_Stepien_or_priority_certified': False,
            })
        result.append({
            'id': f'P{len(result) + 1:02}', 'rank_categories': {str(k): v for k, v in cats.items()},
            'prior_first_delivery_year': prior,
            'reported_prior_conversion_second_round_years': [2025, 2026] if prior is None else [],
            'prior_conversion_allocation_certified': False,
            'completions': completions,
            'same_public_projection_different_Gordon_delivery':
                completions[0]['Gordon_delivery_year'] != completions[1]['Gordon_delivery_year'],
        })
    return result


def graphs():
    """Copy complete opaque rights objects; change approved public player edges only."""
    fixed = [
        ('ADAMS', 'PLAYER', 'OKC', 'NOP', 'Steven Adams'),
        ('BLEDSOE', 'PLAYER', 'MIL', 'NOP', 'Eric Bledsoe'),
        ('MIL_TWO_FIRSTS', 'OPAQUE_UNCHANGED_RIGHT_BUNDLE', 'MIL', 'NOP', 'theta.MIL_two_firsts'),
        ('MIL_TWO_SWAPS', 'OPAQUE_UNCHANGED_RIGHT_BUNDLE', 'MIL', 'NOP', 'theta.MIL_two_swaps'),
        ('HOLIDAY', 'PLAYER', 'NOP', 'MIL', 'Jrue Holiday'),
        ('MERRILL60', 'DRAFT_PLAYER_RIGHT', 'NOP', 'MIL', 'Sam Merrill'),
        ('HILL', 'PLAYER', 'MIL', 'OKC', 'George Hill'),
        ('CHEATHAM', 'PLAYER', 'NOP', 'OKC', 'Zylan Cheatham'),
        ('GRAY', 'PLAYER', 'NOP', 'OKC', 'Josh Gray'),
        ('MILLER', 'PLAYER', 'NOP', 'OKC', 'Darius Miller'),
        ('WILLIAMS', 'PLAYER', 'NOP', 'OKC', 'Kenrich Williams'),
        ('NOP_WAS2023_2R', 'UNCHANGED_DATED_RIGHT', 'NOP', 'OKC', 'WAS2023_2R'),
        ('NOP_CHA2024_2R', 'UNCHANGED_DATED_RIGHT', 'NOP', 'OKC', 'CHA2024_2R'),
        ('DEN_PRIOR_FIRST', 'OPAQUE_NAMED_CONDITIONAL_RIGHT', 'DEN', 'OKC', 'theta.P'),
        ('DEN24_PLAYER', 'DRAFT_PLAYER_RIGHT', 'MIL', 'DEN', 'R.J. Hampton'),
        ('T1_HARRIS', 'PLAYER', 'DEN', 'ORL', 'Gary Harris'),
        ('T1_ROOKIE', 'PLAYER', 'DEN', 'ORL', 'R.J. Hampton'),
        ('T1_GORDON', 'PLAYER', 'ORL', 'DEN', 'Aaron Gordon'),
        ('T1_CLARK', 'PLAYER', 'ORL', 'DEN', 'Gary Clark'),
        ('DEN_FOLLOW_FIRST', 'OPAQUE_NAMED_CONDITIONAL_RIGHT', 'DEN', 'ORL', 'theta.G'),
        ('T3_FOURNIER', 'PLAYER', 'ORL', 'BOS', 'Evan Fournier'),
        ('T3_TEAGUE', 'PLAYER', 'BOS', 'ORL', 'Jeff Teague'),
        ('T3_BOS2025_SECOND', 'OPAQUE_NAMED_CONDITIONAL_RIGHT', 'BOS', 'ORL', 'theta.BOS_MEM2025_less_favorable'),
        ('T3_BOS2027_SECOND', 'OPAQUE_NAMED_CONDITIONAL_RIGHT', 'BOS', 'ORL', 'theta.BOS2027_second'),
        ('F5_MCGEE', 'PLAYER', 'CLE', 'DEN', 'JaVale McGee'),
        ('F5_HARTENSTEIN', 'PLAYER', 'DEN', 'CLE', 'Isaiah Hartenstein'),
        ('F5_DEN2023_SECOND', 'OMITTED_DATED_RIGHT', 'DEN', 'CLE', 'theta.F5_DEN2023_second'),
        ('F5_DEN2027_SECOND', 'OMITTED_DATED_RIGHT', 'DEN', 'CLE', 'theta.F5_DEN2027_second'),
    ]
    original = [{'id': k, 'kind': kind, 'from': origin, 'to': target, 'payload': value}
                for k, kind, origin, target, value in fixed]
    alternate = deepcopy([edge for edge in original if not edge['id'].startswith('F5_')])
    for edge in alternate:
        if edge['id'] in ('DEN24_PLAYER', 'T1_ROOKIE'):
            edge['payload'] = 'Zeke Nnaji'
    contracts = {
        'theta.P': {'promisor': 'DEN', 'assignee': 'OKC', 'object_identity': 'historical_complete_prior_right_object',
                    'transition_body': 'theta.P.full_original_transition',
                    'resolution_event': 'theta.P.full_original_resolution_event',
                    'priority_refs': 'theta.P.all_original_priority_refs',
                    'second_round_conversion_refs': 'theta.P.all_original_conversion_refs',
                    'first_round_supply_refs': 'theta.P.all_original_first_round_supply_refs'},
        'theta.G': {'promisor': 'DEN', 'assignee': 'ORL', 'object_identity': 'historical_complete_Gordon_right_object',
                    'transition_body': 'theta.G.full_original_transition',
                    'prior_resolution_ref': 'theta.P.full_original_resolution_event',
                    'priority_refs': 'theta.G.all_original_priority_refs',
                    'protection_rollover_termination_refs': 'theta.G.all_original_protection_rollover_termination_refs',
                    'first_round_supply_refs': 'theta.G.all_original_first_round_supply_refs'},
        'theta.context': {'other_teams': 'all teams in the complete related rights state',
                          'all_other_nodes_and_refs': 'same historical related-state objects carried by identity',
                          'zero_or_no_other_burdens_assumed': False},
    }
    return {'original_public_edges': original, 'alternate_candidate_public_edges': alternate,
            'historical_contract_objects': contracts, 'alternate_candidate_contract_objects': deepcopy(contracts)}


def validate_graph(graph):
    original = {e['id']: e for e in graph['original_public_edges']}
    alternate = {e['id']: e for e in graph['alternate_candidate_public_edges']}
    omitted = {k for k in original if k.startswith('F5_')}
    if set(alternate) != set(original) - omitted:
        raise ValueError('extra/missing public graph edge')
    for key, edge in alternate.items():
        expected = deepcopy(original[key])
        if key in ('DEN24_PLAYER', 'T1_ROOKIE'): expected['payload'] = 'Zeke Nnaji'
        if edge != expected:
            raise ValueError('non-approved asset owner/reference/payload changed')
    if graph['historical_contract_objects'] != graph['alternate_candidate_contract_objects']:
        raise ValueError('opaque full transition/priority/context references not preserved')


def build():
    register = load(SOURCES[0])
    den = next(p for p in register['legal_proofs'] if p['id'] == 'DEN_GORDON_PICKS_AND_CHARGE')
    bos = next(p for p in register['legal_proofs'] if p['id'] == 'BOS_TPE_AND_PICKS')
    if den['required_branches'] != ['prior_1R_conveys', 'prior_1R_converts_to_2R',
                                    'subsequent_1R_protection_and_termination', 'dated_matching_charge']:
        raise ValueError('required DEN domain changed; fresh scope review needed')
    if [b['id'] for b in den['branches']] != ['dated_matching_charge']:
        raise ValueError('existing DEN branch conclusions changed')
    named = load(SOURCES[3])
    cache_audit = []
    for source in named['source_recoveries']:
        if not source.get('cache_path'):
            continue
        path = Path(source['cache_path'])
        raw = path.read_bytes()
        if len(raw) != source['bytes'] or hashlib.sha256(raw).hexdigest() != source['raw_sha256']:
            raise ValueError(f'previous raw source changed: {source["id"]}')
        cache_audit.append({'id': source['id'], 'path': str(path), 'raw_sha256': source['raw_sha256'],
                            'bytes': len(raw), 'new_collection': False,
                            'classification': source['classification']})
    bylaw = Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-2019-bylaws.pdf')
    raw = bylaw.read_bytes()
    bylaw_sha = hashlib.sha256(raw).hexdigest()
    if bylaw_sha != '6accb3d9633e15e8559d13228c27ae7b3b0b81eac0894050b06256eea6da3464':
        raise ValueError('NBA bylaw raw mismatch')
    paths = rows()
    graph = graphs()
    validate_graph(graph)
    counts = Counter('CONVERTS' if p['prior_first_delivery_year'] is None else str(p['prior_first_delivery_year']) for p in paths)
    return {
        'schema_version': 1, 'date_local': '2026-10-07', 'baseline_main': BASELINE_MAIN,
        'status': 'FINITE_REPORTED_CALENDAR_REPRODUCED_WHOLE_THREE_ASSET_BRANCHES_HOLD',
        'source_hash_convention': 'SHA256_UTF8_NO_BOM_CRLF_CR_TO_LF',
        'source_sha256': {f: sha(ROOT / f) for f in SOURCES},
        'previous_raw_sources_audited': cache_audit,
        'primary_rule': {'url': 'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf',
                         'path': str(bylaw), 'raw_sha256': bylaw_sha, 'bytes': len(raw),
                         'sections': {'4.02': {'printed_pages': [63, 64], 'pdf_pages_one_based': [72, 73]},
                                      '7.03': {'printed_page': 78, 'pdf_page_one_based': 87}},
                         'scope': '4.02 makes publicly completed assignment a positive anchor for its full enforceable original terms; 7.03 imposes future consecutive-first retention; no numerical conversion-link selection',
                         'seven_year_rule_not_derived_from_7_03': True, 'new_collection': False},
        'scope_comparison': {'BOS_registered_scope': bos['scope'], 'DEN_registered_scope': den['scope'],
                             'BOS_future_delivery_certification': False,
                             'DEN_named_assignment_is_not_whole_transition_proof': True,
                             'checker_only_checks_ids_verdicts_and_certificates_not_transition_semantics': True},
        'projection_domain': {
            'years': [2023, 2024, 2025, 2026, 2027], 'symbolic_paths': 48,
            'rank_category_definitions': {'2023_2024': {'0': '1..14', '1': '15..30'},
                                           '2025': {'0': '1..5', '1': '6..14', '2': '15..30'},
                                           '2026_2027': {'0': '1..5', '1': '6..30'}},
            'source_strength': 'REPORTED_PROJECTION_ONLY_NOT_RECOVERED_FULL_CONTRACT',
            'uses_known_reported_thresholds_not_new_collection': True,
            'Y_plus_2_only_on_prior_first_delivery': True,
            '2027_window_is_existing_report_not_new_policy': True,
            'hypotheses_exhaust_actual_contract_domain': False,
            'future_ranks_or_results_selected': False,
        },
        'paths': paths,
        'summary': {'prior_states': dict(counts), 'ambiguous_delivery_paths': sum(p['same_public_projection_different_Gordon_delivery'] for p in paths),
                    'convey_only_projected_legal_spacing_paths': sum(p['prior_first_delivery_year'] is not None for p in paths),
                    'conversion_paths': counts['CONVERTS'],
                    'source_supported_full_contract_completions': 0},
        'branch_reviews': [
            {'id': 'prior_1R_conveys', 'verdict': 'HOLD',
             'computed_scope': '40 categorical rank paths with prior first delivery in 2023/24/25; reported Y+2/top5 calendar reproduced',
             'missing': ['full joint ownership/priority transition for the retained named objects',
                         '2020 Denver24 changed-player economic template is preserved candidate, not automatic canon continuation'],
             'conditional_named_pair_spacing_valid': True, 'complete_domain': False, 'source_verified': False},
            {'id': 'prior_1R_converts_to_2R', 'verdict': 'HOLD',
             'computed_scope': '8 projected conversion paths; two hypothetical linkage completions disagree on 4',
             'missing': ['Gordon eligibility trigger when the prior first never conveys',
                         'priority and allocation of prior 2025/2026 seconds'],
             'exact_conversion_to_Gordon_year': None, 'complete_domain': False, 'source_verified': False},
            {'id': 'subsequent_1R_protection_and_termination', 'verdict': 'HOLD',
             'computed_scope': 'reported top5/year-window reproduction under explicit hypothetical trigger; no exact termination selection',
             'missing': ['complete conditional eligibility/deferral/termination function shared with the prior conversion branch',
                         'joint ownership/priority invariants across every reachable state'],
             'selected_protection_or_termination': None, 'complete_domain': False, 'source_verified': False},
            {'id': 'dated_matching_charge', 'verdict': 'PRESERVED_EXISTING_LEGAL_BOUND_PASS',
             'evidence': den['branches'][0]['evidence'], 'recomputed_in_this_packet': False},
        ],
        'implementable_next_interface': {
            'input_needed': ['dated named-right ownership state', 'source-supported joint transition relation T_theta(state,rank_categories)',
                             'resolution event definition for the conversion branch', 'related-right priority/second-round allocation relation',
                             'finite declared terminal-state domain'],
            'checker_can_then_verify': ['reachable-state closure', 'no duplicate allocation of one dated named right',
                                       'first-round retention for every consecutive future pair',
                                       'termination/conversion exhaust all declared live states'],
            'theta_identity_without_transition_witness_is_not_enough': True,
            'source_supported_branch_relation_or_invariant_witness_suffices_without_private_receipt': True,
            'source_type_private_ledger_contract_original_or_receipt_is_not_mandatory': True,
        },
        'potential_symbolic_identity_witness': {
            'classification': 'PROPOSED_PROOF_INTERFACE_NOT_CERTIFIED',
            'formula': 'For every reachable rank path r: Legal(T_hist(theta,r)) and T_alt(theta,r)=T_hist(theta,r) imply Legal(T_alt(theta,r))',
            'not_required': ['unique numerical future delivery outcome', 'new exact protection or conversion selection',
                             'private acceptance receipt as a mandatory source type'],
            'necessary_audited_premises': [
                'official completed historic assignment supports lawful complete named-right contract family, not merely one realized rank path',
                'same complete prior/follow transition and priority state are jointly preserved in the candidate',
                'DEN24 changed player choice has a consistent preserved economic-rights implementation',
                'approved deltas do not change any relevant ownership, prior burden or future asset allocation',
            ],
            'transition_equivalence_provenance_certified_in_existing_DEN_packet': False,
            'numeric_ambiguity_alone_proves_legal_impossibility': False,
            'reviewer_may_accept_source_supported_symbolic_family_invariance_without_recovering_all_numeric_terms': True,
            'promotion_without_review': False,
        },
        'joint_graph_transform': graph,
        'new_primary_public_graph_source': {
            'url': 'https://www.nba.com/news/pelicans-acquire-steven-adams-eric-bledsoe-in-4-team-trade-jrue-holiday-to-milwaukee',
            'cache_path': 'C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-den-graph-2026-10-07/nov2020-fourteam-release.html',
            'http_status': 200, 'bytes': 340331,
            'raw_sha256': '1d8fd539e7ec135a335622256de4bc7d662d5c470a6fd61a078767d0dba70938',
            'extraction': '__NEXT_DATA__.props.pageProps.article.contentText; completion table and exchange paragraph',
            'contentText_cache_path': 'C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-den-graph-2026-10-07/nov2020-fourteam-contentText.txt',
            'contentText_raw_sha256': 'd072ae0df2d303cd8ac19baa30cb82d5edd874ef462f8d3e9c735f46e5caf106',
            'article_date_UTC': '2020-11-24T15:51:58Z',
            'existing_guide_transaction_date': '2020-11-23',
            'source_role': 'official completed four-team public graph, not full numeric protections',
            'full_article_quoted_in_artifact': False,
        },
        'symbolic_graph_claim': {
            'status': 'CONDITIONAL_STRUCTURAL_RELATION_REPRODUCED_FRAME_AND_LEGAL_PREMISES_REVIEW_PENDING',
            'public_original_edges': 28, 'candidate_edges_after_approved_F5_omission': 24,
            'DEN24_and_T1_player_substitutions': 2,
            'opaque_named_rights_transition_or_priority_changes': 0,
            'formula': 'For all original theta and admissible joint rank paths r, named-asset projection(T_alt(theta,r)) = named-asset projection(T_hist(theta,r)), provided the complete related-state identity and F5 noninterference premises hold',
            'why_not_tautological_legal_theta_definition': 'theta is the same historically completed original right-object; legal inheritance uses public official completion and NBA rule, not theta:=legal by definition',
            'possible_candidate_not_actual_contract_selection': True,
            'DEN24_economic_identity_impossible_counterexample_found': False,
            'DEN24_bridge': 'same MIL-to-DEN 2020 pick24 right with changed player payload, same DEN prior obligation endpoint OKC; no public canon instruction changes its price/conditions',
            'F5_noninterference': {
                'removed_public_dated_rights': ['DEN2023_2R', 'DEN2027_2R'],
                'reported_prior_conversion_dated_rights': ['DEN2025_2R', 'DEN2026_2R'],
                'named_public_dated_right_collision': False,
                'all_contract_cross_ref_objects_copied_by_identity': True,
                'global_asset_state_unchanged': False,
                'deleted_edges_cannot_implicitly_erase_contract_cross_refs': True,
                'frame_noninterference_or_monotonicity_proved': False,
                'no_hidden_cross_reference_fact_certified': False,
                'if_source_shows_cross_reference_into_removed_edge': 'reopen or fail the affected candidate, never erase that reference',
            },
            'needed_root_review': ['complete relevant graph identity premise, including every opaque priority and resolution port',
                                   'official completion as source-supported lawful original contract-family anchor',
                                   'F5 deletion noninterference with the retained complete named asset family'],
            'numeric_conversion_link_null_does_not_refute_this_structural_witness': True,
            'new_policy_or_required_branch_reduction': False,
        },
        'positive_completed_original_anchor': {
            'classification': 'SOURCE_SUPPORTED_LEGAL_INFERENCE_PENDING_ROOT_REVIEW',
            'theta_star': 'the actual full enforceable historical right bundle, not an arbitrary contract from report-compatible possibilities',
            'premise_sources': ['NBA2019Bylaws4.02(a)(b)(d)', 'new official completed Nov2020 public graph',
                                'previous official completed Gordon source provenance'],
            'reason': 'completed assignment requires detailed conditions disclosed to Association Office on the Trade Call and NBA satisfaction/notice; undisclosed extra terms are unenforceable; public press release does not publish every private condition',
            'private_memorandum_original_mandatory': False,
            'relation_theorem_quantifier': 'syntactic equivalence is universal over theta; legal transfer instantiates the sourced actual theta_star, not every imagined theta',
            'future_exact_outcome_or_alternate_acceptance_certified': False,
        },
        'bounded_source_search': {'queries': [
            'Denver Orlando 2021 Gordon pick "2026" "2025 and 2026" "obligation"',
            'Denver Gordon first round pick "converts" "two years" ESPN 2021'],
            'new_primary_transition_evidence_recovered': 0,
            'secondary_snippets_not_adopted': True,
            'repeat_existing_primary_guides_or_failed_article_requests': 0},
        'authority': {'new_asset_terms_selected': False, 'new_financial_choices': 0, 'alternate_acceptance': None,
                      'full_row_PASS_claimed': False, 'policy_changed': False,
                      'register_or_central_edits': 0, 'manuscript_allowed': False,
                      'freeze': 'v0.30 PARTIAL', 'design_gate': 'CLOSED'},
        'independent_review': 'PENDING_ROOT',
        'tool_execution': {'Antigravity': 'NOT_RUN', 'NotebookLM': 'NOT_RUN', 'Claude': 'NOT_RUN'},
    }


def validate(data):
    if len(data['paths']) != 48 or data['summary']['ambiguous_delivery_paths'] != 4:
        raise ValueError('finite projection missing paths or ambiguity counterexample')
    if any(not c['prior_and_follow_only_no_adjacent_outgoing_firsts'] for p in data['paths'] for c in p['completions']):
        raise ValueError('named-pair spacing fails')
    if data['projection_domain']['hypotheses_exhaust_actual_contract_domain']:
        raise ValueError('hypothetical completions cannot certify actual contract completeness')
    if any(b['verdict'] != 'HOLD' for b in data['branch_reviews'][:3]):
        raise ValueError('whole asset branch promotion without source relation')
    validate_graph(data['joint_graph_transform'])
    new = data['new_primary_public_graph_source']
    raw = Path(new['cache_path']).read_bytes()
    if len(raw) != new['bytes'] or hashlib.sha256(raw).hexdigest() != new['raw_sha256']:
        raise ValueError('new official public graph source mismatch')
    txt = Path(new['contentText_cache_path']).read_bytes()
    if hashlib.sha256(txt).hexdigest() != new['contentText_raw_sha256']:
        raise ValueError('new source extraction mismatch')
    if data != build():
        raise ValueError('source or symbolic reconstruction mismatch')


def render(data):
    example = next(p for p in data['paths'] if p['same_public_projection_different_Gordon_delivery'])
    return '\n'.join([
        '# Denver 세 자산 분기 — θ 양도 범위와 공동 전이의 유한 감사', '',
        '2026-10-07 / [48경로·원자료 지문](../research/DEN_THETA_TRANSITION_DOMAIN_2026_10_07.json) / '
        '[재현 도구](../tools/build_den_theta_transition_domain.py).', '',
        '**기존 matching PASS 보존. 새 자산 PASS0. 세 자산 분기 전체는 HOLD다.**', '',
        '## Boston과 다른 정확한 요구 범위', '',
        'Boston의 현행 원장은 March25 특정 권리 양도의 법적 구현을 인증한다. 보호·전환·미래 전달 전체 인증은 제외한다. '
        'Denver 원장은 선행 전달·선행 2R 전환·후행 보호/종료의 모든 살아 있는 결과를 요구한다. '
        '양도 존재라는 같은 증명만 세 행에 반복해 넣으면 Denver의 넓은 요구 범위를 축소하게 된다.', '',
        '현재 S2 검사기는 필수 ID·verdict·complete_domain/source_verified 표지를 검사한다. '
        '그 자체가 공동 전이의 의미·원자료 진실·전체 범위를 증명하지 않는다. '
        '공개 증인이 전체 관계를 덮으면 충분하며 비공개 장부·접수 원본은 새로운 필수요건이 아니다.', '',
        '## 실제 새 계산', '',
        '기존 보고의 2023/24 lottery 경계,2025 두 보호 경계,2026/27 top5 경계를 압축해 '
        '2×2×3×2×2=48개의 상징 순번 경로를 재현했다. 실제 미래 순위는 선택하지 않았다. '
        '선행 전달40경로에서는 Y+2와 후행 보호 달력을 재현할 수 있고 두 named1R만의 연속 지출은 없다. '
        '다른 부담·권리 우선권까지 합친 전체 Stepien 인증은 아니다.', '',
        '전환8경로에는 두 가설을 각각 적용했다: 2025 전환이 의무 해결로 작동해2027부터 후행을 여는 가설과, '
        '선행1R 전달만 후행 개시를 여는 가설이다. 두 가설은 실제 계약 후보로 채택하지 않았다. '
        '공개 투영의 빈칸을 다르게 완성했을 때 무엇이 달라지는지 확인하는 반례다. '
        '둘이 실제 계약 전체를 망라하거나 모두 법적으로 인증됐다는 주장은 없다.', '',
        f"예 `{example['id']}`: 선행2023~25 모두보호,2027은top5밖이라는 같은 상징 경로에서 "
        '첫 가설은2027 후행1R,둘째는2025~27 후행1R 미전달이다. 두 named1R의 간격 제한은 둘 다 충족한다. '
        '즉 그 제한만으로 정확 연결을 결정할 수 없다. 이 차이가4경로에 존재한다.', '',
        '**이 반례는 정확 전달 결과가 결정되지 않는다는 증거이며 합법 구현 불가능의 증거가 아니다.** '
        '모든 살아 있는 결과에서 합법인 원권리 가족과 후보의 공동 전이 동일성이 공개 근거로 검수된다면 '
        '정확 수치 조건·미래 전달 결과를 정하지 않고도 법적 불변량을 증명할 수 있다.', '',
        '## 세 분기별 종료 가능 범위와 누락', '',
        '| 분기 | 구현한 범위 | 전체 종료에 필요한 입력 |', '|---|---|---|',
        '| prior_1R_conveys | 40경로의 보고된 전달/Y+2 달력 | 같은 권리의 공동 소유·우선권·전이 불변량과2020 DEN24 경제 보존 연결 |',
        '| prior_1R_converts_to_2R | 전환8경로·가설 차이4경로 | 선행1R 미전달 때 후행 개시 조건·2025/26 2R 우선권/배정 관계 |',
        '| subsequent_1R_protection_and_termination | 지정 가설하의top5/연도 범위 계산 | 전환과 공유하는 완전 개시·이연·종료 관계·모든 도달상태 불변량 |', '',
        'θ를 동일하게 보존한다고 쓰는 것과, 모든 도달상태에서 같은 권리의 배정이 법적이라는 전이 증인을 주는 것은 다르다. '
        'Θ를 처음부터 모든 미래 결과가 합법인 계약들의 집합으로 정의해 PASS라고 하면 그 합법성이 출처가 아닌 전제에 들어간다. '
        '역사상 양도 완료는 March25 존재를 지지하지만 미관측 전환 branch의 내용을 결정하지 않는다.', '',
        '## 구현 가능한 다음 증인 인터페이스', '',
        '공개 출처에 연결된 유한 Tθ(state,rank-category) 또는 동일 관계를 덮는 불변량 증인, '
        '전환 의무의 해결 사건 정의, 관련 2R 우선권과 말단 상태를 입력으로 받을 수 있다. '
        '그때 도달상태 폐쇄·중복 배정·연속1R 보유·전환/종료 포괄성을 전수 검문한다. '
        '정확 순번·미래 승수·대체세계 접수 원본은 필요하지 않다. '
        '현재 파일에는 이 관계 입력이 없으므로 임의 가설로 대체하지 않는다.', '',
        '별도 가능한 상징 증인은 모든 도달 순번 경로 r에서 T_alt(θ,r)=T_hist(θ,r)와 '
        '원가족의 전범위 합법성을 결합한다. 원완료 거래의 같은 권리 객체·공동 부담/우선권 보존·'
        'DEN24의 일관된 경제 가족·승인 변경의 자산 영향 부재가 그 전제다. '
        '현재 DEN 증인은 이 공동 전이 동일성을 독립 검수받지 않았으며 assignment 존재만 수용됐다. '
        '이를 새 관계증인으로 확인하는 길은 열려 있고 정확 조건 원문만을 유일한 종료 경로로 요구하지 않는다.', '',
        '## 새 공동 그래프 변환 증인', '',
        '[NBA Official release](https://www.nba.com/news/pelicans-acquire-steven-adams-eric-bledsoe-in-4-team-trade-jrue-holiday-to-milwaukee) '
        '전체 본문을 HTTP200으로 새 회수해4팀 완료표와 교환 문단을 읽었다. '
        '발표일Nov24와 기존 가이드 거래일Nov23을 분리한다. raw340331bytes/SHA와 contentText 추출 SHA를 JSON에 기록했다.', '',
        '공개 연결28개에서 승인F5의4개 연결을 제거해 후보24개를 만든다. '
        'DEN24와 T1의 신인 선수payload만Hampton→Nnaji로 바꾼다. '
        '나머지 공개 팀/권리 endpoint와 θ.P/θ.G의 원전이·해결·우선권·보호/종료·관련상태 참조 객체를 복사한다. '
        '불명확한 참조를 빈 배열로 만들지 않는다. DEN24의 경제 보존이 불가능하다는 원문 반례는 찾지 못했으며 '
        '같은 경제 가족은 후보 구현이지 자동 승인이나 실제 상대팀 수락이 아니다.', '',
        '§4.02(a)(b)(d)(인쇄63–64/PDF72–73)을 직접 읽었다. 완료 거래는 draftchoices 등 '
        '모든 조건을 리그 Association Office의 Trade Call에 고지하고 상세memo·조건 충족 및NBA통지를 거치는 절차를 전제한다. '
        '리그에 고지하지 않은 부가조건은 집행할 수 없다. 공개pressrelease가 모든 비공개조건을 게시했다는 뜻은 아니다. '
        '따라서 공식 완료는 바로 그 실제 원θ*의 전조건을 보존하는 긍정 앵커다. '
        '원memo 비공개라는 이유로 새 필수출처를 요구하지 않는다. '
        '이는 모든 임의 보도일치θ의 합법성이나 대체 거래 수락을 인증하지 않는다.', '',
        '구조 동일성은 모든θ에 대한 관계식이지만 법적 계승은 위 actualθ*에 적용한다. '
        'F5 제거 뒤 globalstate는 역사와 완전히 동일하지 않다. 제거DEN2023/2027 2R와 '
        '보고된 선행 전환DEN2025/2026 2R는 공개 datedright로 충돌하지 않지만 이것만으로 '
        '모든 opaque 우선권/조건 참조가F5와 무관하다고 증명하지 않는다. '
        '계약 참조는 지우지 않고 보존하며 frame비간섭 또는 추가로 남는2R의 법적 단조성이 별도 검문 전제다.', '',
        '이 한정 공동 그래프와 완료 앵커를 독립 검문해 frame까지 수용하면 세 requiredbranch를 '
        'assignment scope로 축소하지 않고 같은 관계증인으로 덮을 가능성이 있다. '
        '현재는 그 검문 전 세 branch PASS나 중앙 승격을 하지 않는다. '
        '48경로 가설의 수치 차이는 이 상징 증인의 법적 불가 근거가 아니다.', '',
        '## 출처와 중단 기준', '',
        '기존 Denver 권리 증인의 raw cache6개를 크기/SHA로 대조했으며 새 수집으로 계수하지 않았다. '
        'NBA2019규약 원PDF의 §7.03(인쇄78)을 읽었다. 이 조항은 연속 미래1R 보유를 다루며 '
        'Gordon 전환 연결을 규정하지 않는다. §7.03에서 seven-year 규칙을 도출하지 않는다.', '',
        '초기 전환 연결 검색2개에서 새 1차 수치조항 근거0이었다. 이후 공동 그래프 검색은 위 공식 완료 본문을 새 회수했다. '
        '2차 검색 조각·후대 실제 전달·이미읽은 보호/종료 보도·실패 구단 페이지를 새 근거로 채택하지 않았다. '
        '동일 자료 재수집을 반복하지 않고 위의 정확 관계 입력이 달라질 때 재개한다.', '',
        '사실: 기존 공개 원자료와 승인 이동/생략 방향. 추론: 공개 달력의 유한 투영. '
        '가설: 두 미인증 연결의 차이를 드러내는 반례. 작가확정: 새 선택0. '
        '원장·중앙·기존 source 변경0·정확 조항/수락 null·원고0·PARTIAL/CLOSED.', '',
        '자체 검문은 출처 지문·48경로·28→24 공개 그래프와 원계약 참조 복사·권위 범위에 한정한다. 독립 검문 대기. '
        'Antigravity/NotebookLM/Claude는 이번 NOT_RUN이다.', '',
        '`python -B -X utf8 tools/build_den_theta_transition_domain.py --check --self-test`', '',
    ])


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true')
    p.add_argument('--self-test', action='store_true')
    args = p.parse_args()
    data = build()
    validate(data)
    body = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    markdown = render(data)
    if args.check:
        if norm(OUT) != body or norm(MD) != markdown:
            raise ValueError('saved scope review stale or changed')
    else:
        OUT.write_text(body, encoding='utf-8', newline='\n')
        MD.write_text(markdown, encoding='utf-8', newline='\n')
    n = 0
    if args.self_test:
        for label in ('missing_path', 'fake_scope', 'fake_PASS', 'drop_ambiguity'):
            changed = deepcopy(data)
            if label == 'missing_path': changed['paths'].pop()
            elif label == 'fake_scope': changed['projection_domain']['hypotheses_exhaust_actual_contract_domain'] = True
            elif label == 'fake_PASS': changed['branch_reviews'][1]['verdict'] = 'LEGAL_BOUND_PASS'
            else: changed['summary']['ambiguous_delivery_paths'] = 0
            try: validate(changed)
            except ValueError: n += 1
            else: raise AssertionError(f'false complete-domain accepted: {label}')
        for label in ('owner', 'resolution_ref', 'priority_ref', 'F5_reinsertion'):
            changed = deepcopy(data)
            graph = changed['joint_graph_transform']
            if label == 'owner':
                next(e for e in graph['alternate_candidate_public_edges'] if e['id'] == 'DEN_PRIOR_FIRST')['to'] = 'MIL'
            elif label == 'resolution_ref':
                graph['alternate_candidate_contract_objects']['theta.G']['prior_resolution_ref'] = '2025_by_guess'
            elif label == 'priority_ref':
                graph['alternate_candidate_contract_objects']['theta.P']['priority_refs'] = []
            else:
                graph['alternate_candidate_public_edges'].append(next(e for e in graph['original_public_edges'] if e['id'] == 'F5_DEN2027_SECOND'))
            try: validate(changed)
            except ValueError: n += 1
            else: raise AssertionError(f'false graph identity accepted: {label}')
    print(json.dumps({'status': data['status'], 'symbolic_paths': 48, 'ambiguity_paths': 4,
                      'new_asset_PASS': 0, 'negative_tests': n}, ensure_ascii=False))


if __name__ == '__main__':
    main()
