"""Join fixed selected results and fixed draft origins; never draw or rate games.

The control snapshot is BEFORE optional 2021 offseason moves. The bridge does
not select a Kemba/NOP-MEM deal, a draftee, an actual receipt, or future slots.
"""
import argparse
import copy
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_2020_21_result_and_pick_execution_bridge.py'
OUT = 'simulation/NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json'
MD = OUT[:-5] + '.md'
BASELINE = '75a1d526e78ef53fbf3e72fa7cad8899a57debf9'
REG = 'simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.json'
OVERLAY = 'simulation/NBA_2020_21_SELECTED_REGULAR_OVERLAY.json'
PRIMARY = 'simulation/CHICAGO_2020_21_SEASON_RECOMMENDATION.json'
LEAGUE = 'simulation/NBA_2020_21_FULL_SEASON.json'
L2 = 'simulation/NBA_2021_L2_DATED_WORKING_CALENDAR.json'
BRACKET = 'simulation/CHICAGO_2020_21_K1_L2_BRACKET.json'
SERIES = 'simulation/NBA_2021_DELEGATED_PLAYOFF_RESULTS.json'
PLAYOFF = 'simulation/NBA_2021_DATED_PLAYOFF_RESULT_MODELS.json'
PREREG = 'simulation/NBA_2021_DRAW_PREREGISTRATION.json'
DRAW = 'simulation/NBA_2021_PROVISIONAL_DRAFT.json'
ASSET_INPUT = 'simulation/NBA_2021_DRAFT_ASSET_INPUTS.json'
ASSETS = 'simulation/NBA_2021_DRAFT_ASSETS.json'
CHAIN = 'simulation/NBA_2021_ASSET_CHAIN.json'
DEN = 'research/DEN_PUBLISHED_RIGHTS_TRANSITION_WITNESS_2026_10_07.json'
DEN_REVIEW = 'reviews/DEN_PUBLIC_LEGAL_AND_E8_E9_REVIEW_2026_10_07.md'
BOS = 'research/BOS_NAMED_RIGHTS_ASSIGNMENT_WITNESS_2026_10_06.json'
APPROVAL = 'canon/CHICAGO_2020_21_CP2_APPROVAL.json'
AUTH = 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
DIRECTION = 'canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json'
FOLLOW = 'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json'
SOURCES = [REG, OVERLAY, PRIMARY, LEAGUE, L2, BRACKET, SERIES, PLAYOFF,
           PREREG, DRAW, ASSET_INPUT, ASSETS, CHAIN, DEN, BOS, APPROVAL,
           AUTH, DIRECTION, FOLLOW, DEN_REVIEW]
# Reviewed immutable snapshots, not merely fresh hashes of arbitrary inputs.
# BOM-stripped UTF-8 with CRLF/CR normalized to LF; the generator itself is
# recorded separately to avoid a self-referential digest.
REVIEWED_INPUT_SHA256 = {'simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.json': 'a37f3a300f134422b4312d2d9c04ec34a687bb05ed59ccd68e27b9914a5540ea', 'simulation/NBA_2020_21_SELECTED_REGULAR_OVERLAY.json': '3f8f312d2d0c5fd45054b6d5945856d1db05dddaa7316a755c21f0bd7f4c3400', 'simulation/CHICAGO_2020_21_SEASON_RECOMMENDATION.json': '19427d536c0ef5bb136d570ad04ed6de6cb285e68e0c3ff06c88e65c718a70f9', 'simulation/NBA_2020_21_FULL_SEASON.json': 'fece775c14aa2784f05ab682c8ed0ffbe3b00096e00b3e1390fb2cb0003ae6b3', 'simulation/NBA_2021_L2_DATED_WORKING_CALENDAR.json': 'abf099ad6fc26df0b922c25abd71945c41066e4800eb1eb3fbd676a460661fd6', 'simulation/CHICAGO_2020_21_K1_L2_BRACKET.json': 'a9517ebac489711f744df6bb0edf65c82b47c43db9a647b9de3c140326e4d5b1', 'simulation/NBA_2021_DELEGATED_PLAYOFF_RESULTS.json': 'dc1d47563f8381a4b1bd98409f198e8df088ce782622071e22556e8f0c7a7cdb', 'simulation/NBA_2021_DATED_PLAYOFF_RESULT_MODELS.json': '6f8a5a9e140283c2453db230c6a57d38476046ab19bd34722b96563227d521d3', 'simulation/NBA_2021_DRAW_PREREGISTRATION.json': '224b9d9263d8b4519bae415f81d69826f5a6f25ca45f8e384c6cbca9bee1f276', 'simulation/NBA_2021_PROVISIONAL_DRAFT.json': 'feeeec4e28c79c2e0bed722b56ee6e5045bf92abce722b261084a6196c750e06', 'simulation/NBA_2021_DRAFT_ASSET_INPUTS.json': 'a2ab7bbb933a62d091ac43d72bea2888704c937c287b1c4103c16b412b7ad3e2', 'simulation/NBA_2021_DRAFT_ASSETS.json': 'eb1f204a56ffea45a3153b1067954e96331f35cba5910651b1e18d724a8dcaeb', 'simulation/NBA_2021_ASSET_CHAIN.json': '3c39c7baa777f70423394181b1a92870146a32db36c60a67f32ec75319c74c5e', 'research/DEN_PUBLISHED_RIGHTS_TRANSITION_WITNESS_2026_10_07.json': '1191f799df2d5be72292966423d54832a25b7f7fbfbe4b86e8e83bda128e1a73', 'research/BOS_NAMED_RIGHTS_ASSIGNMENT_WITNESS_2026_10_06.json': 'a697079527d2724ed11943246a8af64a1159354d57ae9cbc811a356ceb5254f0', 'canon/CHICAGO_2020_21_CP2_APPROVAL.json': '9cd4c1082dc56d8ceb07139bbeacb91837aa7a21611ff09c48bc4d6dd5002b74', 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json': '4ee9b74e37903a43b0bd50b35c7f24cbabdac13728097a848b553f874bbeef80', 'canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json': 'ab996ffb9f9f6e4471ad473633af1529eb4928e3aa9a17b99642c591691c3798', 'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json': 'c0166bba7a0874aa08dfa88e7d00c0f0d0e237ca2090459ddd6167cf1353c5ea', 'reviews/DEN_PUBLIC_LEGAL_AND_E8_E9_REVIEW_2026_10_07.md': '7a5f73569ca079141fe44c3a5ee53ba6ad7607f8974cda37f6b79b96d9f05b33'}

def text(p):
    return (ROOT / p).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')

def sha(p):
    return hashlib.sha256(text(p).encode()).hexdigest()

def load(p):
    return json.loads(text(p))

def guarded_sources(reader=load, hasher=sha):
    assert set(REVIEWED_INPUT_SHA256) == set(SOURCES), 'Reviewed source coverage'
    for p in SOURCES:
        assert hasher(p) == REVIEWED_INPUT_SHA256[p], 'Unreviewed source change: ' + p
    return {p: reader(p) for p in SOURCES if p != DEN_REVIEW}

def game_row(g, phase):
    date = g['date'] if phase != 'PLAYOFF' else g['date_model']
    home = g['home'] if phase != 'PLAYOFF' else g['home_team']
    away = g['away'] if phase != 'PLAYOFF' else next(t for t in g['teams'] if t != home)
    winner = g['winner'] if phase != 'PLAYOFF' else g['winner_model']
    assert home != away and winner in (home, away)
    id = g.get('event_id') if phase != 'PLAYOFF' else f"{g['series']}_G{g['game']}"
    return {'id': id, 'date': date, 'phase': phase, 'home': home, 'away': away,
            'winner': winner, 'loser': away if winner == home else home,
            'source': REG if phase == 'REGULAR' else L2 if phase == 'PLAY_IN' else PLAYOFF,
            'classification': 'EXISTING_AUTHOR_SELECTED_RESULT_WORKING_EXECUTION',
            'score': None, 'actual_box': None, 'actual_result_certified': False}

def join_regular(s):
    r, o = s[REG], s[OVERLAY]
    a = s[AUTH]
    assert a['authority_type'] == 'AUTHOR_DELEGATED_SELECTION'
    assert a['selected']['regular_season']['route'] == 'K1_BPM_F038_WITH_APPROVED_F4_F5_C2_OVERRIDES'
    assert a['selected']['play_in']['route'] == 'L2'
    assert r['policy'] == o['policy'] and r['method'] == o['method'] == 'BPM_MAR25_EB'
    assert not r['raptor_mixed'] and not o['raptor_mixed']
    primary = next(x for x in s[PRIMARY]['season_candidates'] if x['role'] == 'PRIMARY_RECOMMENDATION')
    primary_map = {x['event_id']: tuple(x['event_id'].split('_')) + (x['winner'],) for x in primary['regular_season_games']}
    overlay_map = {x['event_id']: (x['date'], x['home'], x['away'], x['winner']) for x in o['regular_season_games']}
    rows = [game_row(g, 'REGULAR') for g in r['regular_season_games']]
    for g in r['regular_season_games']:
        band = g['home_margin_band']
        assert band[0] <= band[1]
        assert (band[0] > 0 if g['winner'] == g['home'] else band[1] < 0), 'Saved selected margin direction inconsistent'
    assert len(rows) == len({g['id'] for g in rows}) == 1080
    joined = {g['id']: (g['date'], g['home'], g['away'], g['winner']) for g in rows}
    assert joined == overlay_map == primary_map, 'Selected1080 exact result identity'
    played, wins = Counter(), Counter()
    for g in rows:
        played.update([g['home'], g['away']]); wins.update([g['winner']])
        assert g['id'] == f"{g['date']}_{g['home']}_{g['away']}"
    assert len(played) == 30 and set(played.values()) == {72} and sum(wins.values()) == 1080
    assert dict(wins) == s[DRAW]['team_wins'] == s[PREREG]['team_wins']
    case = next(x for x in s[LEAGUE]['league_cases'] if x['id'] == 'F038')
    assert case['team_wins'] == dict(wins)
    standings = []
    for conf, teams in case['seeds'].items():
        assert len(teams) == len(set(teams)) == 15
        assert [wins[t] for t in teams] == sorted([wins[t] for t in teams], reverse=True)
        standings.extend({'conference': conf, 'seed': i + 1, 'team': t, 'played': 72,
                          'wins': wins[t], 'losses': 72 - wins[t],
                          'tie_resolution': 'PRESERVE_EXISTING_F038_CONFERENCE_ORDER_NOT_NEW_TIEBREAK'}
                         for i, t in enumerate(teams))
    assert len({x['team'] for x in standings}) == 30
    return rows, standings, case['seeds']

def join_postseason(s, seeds):
    l2 = [game_row(g, 'PLAY_IN') for g in s[L2]['games']]
    assert len(l2) == 6 and len({x['id'] for x in l2}) == 6
    assert [(g['home'], g['away'], g['winner']) for g in l2] == [
        (g['home'], g['away'], g['winner']) for g in s[DRAW]['playin_games']]
    qualifiers, first_pairs = {}, []
    for index, (conf, short) in enumerate([('EAST', 'east'), ('WEST', 'west')]):
        gs = l2[3 * index:3 * index + 3]; ordered = seeds[conf]
        assert [gs[0]['home'], gs[0]['away']] == ordered[6:8]
        assert [gs[1]['home'], gs[1]['away']] == ordered[8:10]
        assert [gs[2]['home'], gs[2]['away']] == [gs[0]['loser'], gs[1]['winner']]
        final = ordered[:6] + [gs[0]['winner'], gs[2]['winner']]
        assert final == s[BRACKET]['conferences'][short]['final_seeds']
        qualifiers[conf] = [{'seed': 7, 'team': gs[0]['winner'], 'via': gs[0]['id']},
                            {'seed': 8, 'team': gs[2]['winner'], 'via': gs[2]['id']}]
        for n, (high, low) in enumerate([(1, 8), (2, 7), (3, 6), (4, 5)], 1):
            first_pairs.append({'series': ('E' if conf == 'EAST' else 'W') + str(n),
                                'teams': [final[high - 1], final[low - 1]]})
    pg = [game_row(g, 'PLAYOFF') for g in s[PLAYOFF]['games']]
    assert len(pg) == len({g['id'] for g in pg}) == 88
    series = s[SERIES]['series']; sm = {x['id']: x for x in series}
    assert len(sm) == 15
    for p in first_pairs: assert sm[p['series']]['teams'] == p['teams']
    paths = []
    for x in series:
        id = x['id']; gs = [g for g in pg if g['id'].startswith(id + '_G')]
        assert len(gs) == x['winner_wins'] + x['loser_wins']
        assert len(gs) >= 4 and len(gs) <= 7
        counts = Counter()
        for n, g in enumerate(gs, 1):
            assert g['id'] == f'{id}_G{n}' and {g['home'], g['away']} == set(x['teams'])
            assert not any(v == 4 for v in counts.values()), 'No game after series decided'
            counts[g['winner']] += 1
        assert counts[x['winner']] == 4 and counts[x['loser']] == x['loser_wins']
        assert gs[-1]['winner'] == x['winner']
        if x['parents']:
            assert {sm[p]['winner'] for p in x['parents']} == set(x['teams'])
            parent_dates = [g['date'] for g in pg if g['id'].split('_G')[0] in x['parents']]
            assert min(g['date'] for g in gs) > max(parent_dates)
        paths.append({'series': id, 'round': x['round'], 'parents': x['parents'],
                      'teams': x['teams'], 'winner': x['winner'], 'loser': x['loser'],
                      'record': [4, x['loser_wins']], 'game_ids': [g['id'] for g in gs]})
    assert sm['F1']['winner'] == s[SERIES]['champion'] == 'MIL'
    assert sm['F1']['loser'] == s[SERIES]['runner_up'] == 'PHX'
    return l2, pg, qualifiers, paths

def join_fixed_draw(s, standings, qualifiers):
    p, pre = s[DRAW], s[PREREG]
    assert s[APPROVAL]['approved_procedure'] == 'CP2' and s[APPROVAL]['conditional_workflow_approved']
    assert p['seed_sha256'] == pre['seed_sha256'] and p['seed_text'] == pre['seed_text']
    assert p['algorithm_sha256'] == pre['algorithm_sha256']
    playoff = {x['team'] for x in standings if x['seed'] <= 6}
    playoff.update(x['team'] for conf in qualifiers.values() for x in conf)
    allteams = {x['team'] for x in standings}; lottery = allteams - playoff
    assert playoff == set(pre['playoff_teams']) and lottery == set(pre['lottery_teams'])
    assert len(playoff) == 16 and len(lottery) == 14
    log = p['tie_log']; flattened = []
    for x in log:
        assert set(x['members']) == set(x['order']) and len(set(x['order'])) == len(x['order'])
        assert all(p['team_wins'][t] == x['wins'] for t in x['order'])
        flattened.extend(x['order'])
    assert len(flattened) == len(set(flattened)) == 30
    assert flattened[:14] == p['lottery_pre_order'] and set(flattened[:14]) == lottery
    assert set(flattened[14:]) == playoff
    assignment = p['combination_assignment']; cs = list(combinations(range(1, 15), 4))
    assert len(assignment) == 1001
    assigned = Counter()
    for n, x in enumerate(assignment):
        assert x['index'] == n and x['balls'] == list(cs[n])
        assigned[x['origin']] += 1
    assert assigned.pop(None) == 1 and dict(assigned) == p['combinations_per_origin']
    assert sum(assigned.values()) == 1000
    accepted = []
    for n, x in enumerate(p['draw_log'], 1):
        assert x['attempt'] == n and x['for_pick'] == len(accepted) + 1
        fixed = assignment[x['index']]
        assert x['balls'] == fixed['balls'] and x['origin'] == fixed['origin']
        expected = 'UNASSIGNED' if x['origin'] is None else 'REPEAT_WINNER' if x['origin'] in accepted else 'ACCEPTED'
        assert x['decision'] == expected
        if expected == 'ACCEPTED': accepted.append(x['origin'])
    assert len(accepted) == 4 and accepted == p['top_four']
    first = accepted + [t for t in flattened[:14] if t not in accepted] + flattened[14:]
    assert p['first_round_origins'] == [{'pick': i + 1, 'origin': t} for i, t in enumerate(first)]
    position = {t: i for i, t in enumerate(first)}
    second = sorted(first, key=lambda t: (p['team_wins'][t], -position[t]))
    assert p['second_round_origins'] == [{'pick': i + 31, 'origin': t} for i, t in enumerate(second)]
    return first, second

def join_control(s, first, second):
    p = s[ASSET_INPUT]
    assert p['baseline'] == 'AFTER_MARCH_2021_BEFORE_JUNE_18_OPTIONAL_MOVES'
    assert s[ASSETS]['selected_scenario'] is None, 'Do not silently choose optional offseason trades'
    rows = []
    for rd, origins in [(1, first), (2, second)]:
        override = p['first_round_owner_by_origin_overrides'] if rd == 1 else p['second_round_owner_by_origin_overrides']
        for n, origin in enumerate(origins, 1 if rd == 1 else 31):
            rows.append({'round': rd, 'pick': n, 'origin': origin,
                         'control_holder': override.get(origin, origin),
                         'classification': 'FROZEN_PRESERVED_SEASON_RIGHTS_WORKING_SETTLEMENT',
                         'rights_source': ASSET_INPUT,
                         'actual_June_22_holder_certified': False, 'selected_draftee': None})
    ch = next(x for x in rows if x['round'] == 2 and x['origin'] == 'CHI')
    no = next(x for x in rows if x['round'] == 2 and x['origin'] == 'NOP')
    swap = no['pick'] < ch['pick']
    if swap: ch['control_holder'], no['control_holder'] = 'NOP', 'CHI'
    core = s[DRAW]['core_asset_settlement']
    mi = next(x for x in rows if x['round'] == 1 and x['origin'] == 'MIN')
    ci = next(x for x in rows if x['round'] == 1 and x['origin'] == 'CHI')
    assert mi['control_holder'] == ('MIN' if mi['pick'] <= 3 else 'GSW')
    assert (mi['pick'], mi['control_holder']) == (core['MIN_first']['pick'], core['MIN_first']['owner'])
    assert (ci['pick'], ci['control_holder']) == (core['CHI_first']['pick'], core['CHI_first']['owner'])
    assert ch['pick'] == core['CHI_NOP_second']['CHI_origin_pick']
    assert no['pick'] == core['CHI_NOP_second']['NOP_origin_pick']
    assert swap == core['CHI_NOP_second']['swap_exercised_conditionally']
    old_base = next(x for x in s[ASSETS]['scenarios'] if not x['boston_kemba'] and not x['nop_mem'])['rows']
    assert [(x['round'], x['pick'], x['origin'], x['control_holder']) for x in rows] == [
        (x['round'], x['pick'], x['origin'], x['owner']) for x in old_base], 'Preserved pre-optional asset identity'
    assert len(rows) == len({(x['round'], x['origin']) for x in rows}) == 60
    assert {x['pick'] for x in rows} == set(range(1, 61))
    den = s[DEN]
    assert den['whole_branch_complete_domain']
    assert den['positive_rule_scope_and_source_boundary']['root_scope_judgment'].startswith('Original S2 legal-existence domain')
    assert 'LEGAL_BOUND_PASS로 수용' in text(DEN_REVIEW), 'Root review accepted public scope'
    assert not den['prior_conditional_relation_lemma_repromoted']
    assert den['actual_future_delivery'] is None and den['actual_acceptance'] is None
    claims = den['positive_reported_rule_components']
    assert claims['P']['recipient'] == 'OKC' and claims['G']['recipient'] == 'ORL'
    assert claims['F5_2023']['omitted_by_approved_F5'] and claims['F5_2027']['omitted_by_approved_F5']
    den21 = next(x for x in rows if x['round'] == 2 and x['origin'] == 'DEN')
    assert den21['control_holder'] == 'OKC'
    den21['additional_preserved_named_right_source'] = DEN
    den21['future_P_G_resolution_used_for_2021'] = False
    assert s[BOS]['status'] == 'S2_SCOPED_NAMED_RIGHTS_ASSIGNMENT_LEGAL_BOUND_PASS'
    assert s[BOS]['2025_assignment']['actual_future_ranks'] is None
    assert s[BOS]['2027_assignment']['actual_future_rank'] is None
    return rows, {'MIN_top_three_first': {'origin': 'MIN', 'pick': mi['pick'], 'holder': mi['control_holder'],
                    'protected': mi['pick'] <= 3, 'future_2022_obligation_if_retained': core['MIN_first']['remaining_2022_obligation']},
                 'CHI_no_Vucevic_first': {'origin': 'CHI', 'pick': ci['pick'], 'holder': ci['control_holder']},
                 'CHI_NOP_second_swap': {'CHI_origin_pick': ch['pick'], 'NOP_origin_pick': no['pick'],
                    'swap_triggered': swap, 'CHI_holder_origin': 'NOP' if swap else 'CHI'},
                 'DEN_2021_second': {'origin': 'DEN', 'pick': den21['pick'], 'holder': den21['control_holder'],
                    'source': [ASSET_INPUT, DEN], '2023_2027_outcomes_copied': False}}

def build(reader=load, hasher=sha):
    s = guarded_sources(reader, hasher)
    reg, standings, seeds = join_regular(s)
    l2, playoff, qualifiers, paths = join_postseason(s, seeds)
    first, second = join_fixed_draw(s, standings, qualifiers)
    control, settlement = join_control(s, first, second)
    games = reg + l2 + playoff
    assert len(games) == len({(x['phase'], x['id']) for x in games}) == 1174
    f5_conflicts = []
    for row in s[REG]['team_games']:
        removed = 'JaVale McGee' if row['team'] == 'DEN' else 'Isaiah Hartenstein' if row['team'] == 'CLE' else None
        if removed and row['date'] >= '2021-03-25' and row['player_seconds'].get(removed, 0) > 0:
            f5_conflicts.append({'event_id': row['event_id'], 'team': row['team'], 'removed_player': removed,
                                 'seconds': row['player_seconds'][removed], 'correction_owner': 'ROOT',
                                 'selected_winner_descendant_recheck_complete': False})
    corrections = s[OVERLAY].get('f5_source_branch_completions', [])
    correction_joins = []
    for c in corrections:
        tg = next(x for x in s[REG]['team_games'] if x['event_id'] == c['event_id'] and x['team'] == c['team'])
        original = copy.deepcopy(c['original_full_vector'])
        sec = original.pop(c['original_donor'])
        original[c['retained_counterpart']] = original.get(c['retained_counterpart'], 0) + sec
        assert sec == c['seconds'] and original == tg['player_seconds']
        result = next(x for x in s[REG]['regular_season_games'] if x['event_id'] == c['event_id'])
        effect = next(x for x in result['non_j1_team_effects'] if x['team'] == c['team'] and x['overlay_stage'] == 'F5_SCOPE_COMPLETION')
        assert effect['moved_seconds'] == {c['original_donor']: -sec, c['retained_counterpart']: sec}
        correction_joins.append({'event_id': c['event_id'], 'team': c['team'],
            'original_donor': c['original_donor'], 'retained_counterpart': c['retained_counterpart'],
            'seconds': sec, 'selected_winner': result['winner'], 'selected_home_margin_band': result['home_margin_band'],
            'source': OVERLAY, 'new_BPM_recalculation_by_this_bridge': False})
    return {'schema': 'NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE_V1',
            'status': 'FINITE_SELECTED_RESULT_AND_FROZEN_SEASON_PICK_CONTROL_JOIN_ROOT_REVIEW_PENDING',
            'baseline_main': BASELINE, 'source_sha256': {p: hasher(p) for p in SOURCES + [SELF]},
            'source_hash_method': 'UTF8_BOM_STRIPPED_CRLF_CR_TO_LF',
            'classification': {'fact': 'Existing repository results/draw/rights sources and their exact identities; not actual counterfactual outcomes',
                'inference': 'Mechanical selected-winner aggregation, bracket parent joins and frozen-rights settlement',
                'candidate': 'Optional 2021 offseason AP branches and named draftees remain unselected',
                'author_selected': 'Existing delegated health/season results and approved transaction directions; no new outcome or asset selection'},
            'authority': {'selected_result_authority': AUTH, 'fixed_draw_procedure_authority': APPROVAL,
                'new_result_selection': False, 'lottery_redrawn': False, 'tie_redrawn': False,
                'game_ratings_recomputed': False, 'new_transaction_or_draftee_selection': False},
            'games': games, 'standings': standings, 'play_in_qualifiers': qualifiers,
            'series_paths': paths, 'champion': 'MIL', 'runner_up': 'PHX',
            'fixed_draw': {'source': DRAW, 'preregistration_source': PREREG,
                'seed_sha256': s[DRAW]['seed_sha256'], 'preregistered_commit': s[DRAW]['preregistration_public_commit'],
                'top_four': s[DRAW]['top_four'], 'existing_draw_log_verified_without_RNG': True,
                'first_round_origins': s[DRAW]['first_round_origins'],
                'second_round_origins': s[DRAW]['second_round_origins']},
            'pick_control_snapshot': {'scope': 'AS_OF_FROZEN_APPROVED_SEASON_ASSETS_BEFORE_OPTIONAL_OFFSEASON_MOVES',
                'not_real_June_22_holder_certificate': True, 'optional_scenario_selected': None,
                'rows': control, 'core_protection_settlement': settlement,
                'old_AP3_no_optional_projection_used_as_identity_comparator_only_not_selected': True},
            'descendant_rights': {'full_existing_asset_chain_source': CHAIN,
                'Boston_named_assignment_family': BOS, 'Denver_public_legal_family': DEN,
                'Denver_public_family_acceptance_review': DEN_REVIEW,
                'Boston_preserved_2025_named_rights': s[BOS]['related_rights'],
                'Boston_2025_right_function': s[BOS]['2025_assignment']['right_function'],
                'Boston_2027_right': s[BOS]['2027_assignment']['right'],
                'DEN_prior_P_and_G_objects_preserved': s[DEN]['positive_reported_rule_components'],
                'DEN_F5_conditional_claims_created': False,
                'DEN_future_2023_2027_actual_slots': None, 'DEN_future_actual_acceptance': None,
                'Boston_2025_split_and_2027_actual_delivery': None,
                'original_future_delivery_results_copied': False,
                'private_whole_relation_rejected_lemma_repromoted': False},
            'summary': {'regular_games': 1080, 'play_in_games': 6, 'playoff_games': 88,
                'total_result_games': 1174, 'regular_team_game_count': 2160, 'teams': 30,
                'regular_games_each_team': 72, 'play_in_qualifiers': 4, 'series': 15,
                'first_round_origins': 30, 'second_round_origins': 30, 'frozen_control_rows': 60,
                'result_changes': 0, 'unresolved_join_rows': 0, 'unresolved_core_protection_settlements': 0},
            'pre_promotion_result_input_coherence': {'approved_F5_removed_player_positive_rows': f5_conflicts,
                'approved_F5_scope_completion_joins': correction_joins,
                'conflict_count': len(f5_conflicts), 'selected_minutes_and_winner_descendants_coherent': not f5_conflicts,
                'all_result_rows_already_selected_not_recomputed_by_this_bridge': True},
            'remaining_named_gaps': ([{'id': 'F5_MINUTE_RESULT_COHERENCE', 'scope': 'Root correction of four positive-minute superseded McGee/Hartenstein rows and affected BPM/winner descendants; must be resolved before using this join to promote A3'}] if f5_conflicts else []) + [
                {'id': 'MACRO3_OPTIONAL_OFFSEASON', 'scope': 'AP1/AP2/Boston Kemba/NOP-MEM and draft-night transactions remain candidate; not an A3 season-snapshot prerequisite'},
                {'id': 'MACRO3_DRAFTEE_SELECTION', 'scope': 'All60 named draftees/rosters remain separate; fixed origins/control do not select players'},
                {'id': 'FUTURE_RIGHTS_EXECUTION', 'scope': '2022–27 actual slots/delivery/acceptance remain null; reopen relevant family only if input obligations change'},
                {'id': 'WHOLE_A_K_SEASON', 'scope': 'Root reviews this finite execution join alongside A1/A2 and closing witness; this packet does not promote gates'}],
            'scope_certification': {'finite_join_complete_domain': True,
                'finite_join_repository_sources_current': True, 'independent_review_completed': False,
                'actual_historical_all_team_rights_contract_audit': False,
                'actual_boxes_scores_or_medical_certified': False, 'actual_league_receipt_or_consent_certified': False,
                'whole_A3_closed': False, 'whole_K_METHOD_EVENTS_closed': False, 'closing_witness_written': False,
                'register_promotion': False, 'season_selected': False, 'manuscript_allowed': False},
            'freeze': 'v0.30 PARTIAL', 'design_gate': 'CLOSED',
            'tool_runs': {'Antigravity': 'NOT_RUN_FOR_THIS_REPOSITORY_JOIN', 'NotebookLM': 'NOT_RUN_FOR_THIS_REPOSITORY_JOIN',
                          'Claude': 'NOT_RUN_FOR_THIS_REPOSITORY_JOIN'}}

def validate(d, reader=load, hasher=sha):
    try:
        assert d == build(reader, hasher), 'Artifact differs from exact selected-source reconstruction'
        return []
    except (AssertionError, KeyError, ValueError, OSError, TypeError) as exc:
        return [str(exc) or type(exc).__name__]

def render(d):
    rows = ['# 2020–21 승패 → 순위 → 진출 → 고정 지명권 실행 연결', '',
        '기준 main `'+BASELINE+'`. [JSON](NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json)에 이미 선택된 1,174경기의 신원·날짜·승자를 연결한다. 새 승패 계산·재추첨·동률 추첨0이다.', '',
        '## 완료한 유한 연결', '',
        '정규1,080 → 30팀 각72경기/총2,160팀경기 → 기존F038 동률순서 → L2 6경기/4진출 → 15시리즈88경기/우승MIL·준우승PHX → 기존 추첨 1R30·2R30 origin → 시즌 권리틀60행을 결산했다. 개별 경기의 정확 점수·실제 박스·의료 인증을 새 종료조건으로 추가하지 않는다.', '',
        '| 동부 | 승–패 | 순위 | 서부 | 승–패 | 순위 |', '|---|---|---:|---|---|---:|']
    east = [x for x in d['standings'] if x['conference'] == 'EAST']
    west = [x for x in d['standings'] if x['conference'] == 'WEST']
    for a, b in zip(east, west):
        rows.append(f"| {a['team']} | {a['wins']}–{a['losses']} | {a['seed']} | {b['team']} | {b['wins']}–{b['losses']} | {b['seed']} |")
    rows += ['', '동부7/8위 BOS·IND, 서부7/8위 POR·MEM으로 기존8쌍을 연결했다. 각 후속시리즈 참가자는 부모시리즈 승자와 일치하며, 4승 뒤 추가 경기0이다.', '',
        '## 권리 결산의 정확한 시점', '',
        '**AS OF FROZEN APPROVED SEASON ASSETS BEFORE OPTIONAL OFFSEASON MOVES**. 3월 승인 거래·기존 권리틀에 시즌말 origin 순번을 적용한 작업 결산이다. 실제6월22일 보유자 인증이나 AP3 채택이 아니다. AP1 Boston Kemba 교환·NOP/MEM·드래프트 당일 교환·선수60명 지명은 다음 큰묶음의 후보로 남고 이번 A3의 신규 필수조건이 아니다.', '',
        '| 정산 | 결과 |', '|---|---|']
    c = d['pick_control_snapshot']['core_protection_settlement']
    rows += [f"| CHI 1R | {c['CHI_no_Vucevic_first']['pick']}번 CHI 보유; 승인 Vucevic 거래 생략 |",
        f"| MIN 1R | {c['MIN_top_three_first']['pick']}번 GSW; top3 보호 미발동 |",
        f"| CHI/NOP 2R | CHI {c['CHI_NOP_second_swap']['CHI_origin_pick']} / NOP {c['CHI_NOP_second_swap']['NOP_origin_pick']}; swap 미발동 |",
        f"| DEN 2R | {c['DEN_2021_second']['pick']}번 OKC; 원2021 명명 권리 보존 |", '',
        '전체 기존 [자산 사슬](NBA_2021_ASSET_CHAIN.json)의 과거 null/예제는 그대로 보존한다. [DEN 공개 권리 가족](../research/DEN_PUBLISHED_RIGHTS_TRANSITION_WITNESS_2026_10_07.json)에 2021 DEN 2R과 기존2022 객체를 연결하고, P→G의 미래 보호/전환/종료는 통과한 가족을 참조한다. F5 2023/2027 조건부청구권은 생성하지 않는다. 2023–27 실제 순번·동의·전달을 원역사에서 복사하거나, 기각된 전체 private 관계정리를 재승격하지 않는다.', '',
        '## 검문과 미완료 범위', '',
        '정규 승자와 원PRIMARY·overlay·clock결산의 정확 신원 일치, 30×72/승수합1080, 플레이인 진출과 시리즈 부모 연결, 고정 추첨 log→기존1001 배정/기존4승자, 양 라운드 각30 origin, 60 control, 기존 보호 정산을 검문한다. 입력 지문은 검토한 스냅샷 값과 비교하므로 변조한 입력의 새 SHA만 붙여 통과할 수 없다. 실제 원계약 전체·의료·접수·6월22일 holder·원고 인증은 false다.', '',
        '원장·closing witness·A3/K_METHOD_EVENTS/시즌 승격0, 독립 검문 pending. 후속 거래·선수 지명과 미래 실제 권리 실행은 각 범위에서 남는다. Antigravity/NotebookLM/Claude 이번 join 실행0.', '',
        ('현재 승인F5와 충돌하는 양수 선수분 '+str(d['pre_promotion_result_input_coherence']['conflict_count'])+'행이 남아 있어 승격 전 수정이 필요하다.' if d['pre_promotion_result_input_coherence']['conflict_count'] else
         '루트가 수리한 DEN4/9·4/28, CLE4/17·4/21의4분행을 정확 벡터 치환·기존 단일BPM 결과 band에 연결했다. 네 승자 DEN/CHI/CLE/DEN과 전체1,080 승자 변화0, 승인F5와 충돌하는 양수 선수분0을 확인했다. 이 도구는 BPM을 다시 계산하지 않고 수정된 저장 결과의 부호와 분 연결을 검문한다.'), '',
        '## 전체 7행 진행표', '',
        '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md) 기준 미완료 큰묶음 **6개**. 아래는 이 작업의 한정 보고이며 중앙 상태를 변경하지 않는다.', '',
        '| 번호 | 작업 | 상태 |', '|---:|---|---|',
        '| 1 | 2020 드래프트 연쇄 | 완료 |',
        '| 2 | Chicago 2020–21 | 법적12/12·F5/5; 결과/픽 실행 join 완료·A/K/시즌 종료 검문 대기 |',
        '| 3 | 2021–23 거래·계약 | 승인 방향 보존; optional offseason/정확 실행 미완료 |',
        '| 4 | 장기 커리어 | 선행 시즌 및 후손 연결 대기 |',
        '| 5 | 결말·전체 구조 | 골격 완료; 전체 회차 기능표 미완료 |',
        '| 6 | 집필 규격·Context Pack | A01 기능9/36·남은27; 전체780 중771 미배치·실제Pack0 |',
        '| 7 | 통합·독립·최종 승인 | 진행 중·최종 게이트 CLOSED |', '',
        'PROJECT_FREEZE v0.30 PARTIAL·설계/원고 CLOSED·원고0.', '']
    return '\n'.join(rows)

def self_test(d):
    changes = [('regular winner', lambda x: x['games'][0].update(winner=x['games'][0]['away'])),
        ('play-in qualifier', lambda x: x['play_in_qualifiers']['EAST'][1].update(team='CHI')),
        ('series winner', lambda x: x['series_paths'][0].update(winner='IND')),
        ('wrong fixed origin', lambda x: x['fixed_draw']['first_round_origins'][0].update(origin='CHI')),
        ('wrong MIN holder', lambda x: next(y for y in x['pick_control_snapshot']['rows'] if y['round']==1 and y['origin']=='MIN').update(control_holder='MIN')),
        ('restore omitted Vucevic pick', lambda x: next(y for y in x['pick_control_snapshot']['rows'] if y['round']==1 and y['origin']=='CHI').update(control_holder='ORL')),
        ('optional Kemba promoted', lambda x: x['pick_control_snapshot'].update(optional_scenario_selected='AP1')),
        ('future outcome invented', lambda x: x['descendant_rights'].update(DEN_future_2023_2027_actual_slots={'2025':6})),
        ('whole gate promoted', lambda x: x['scope_certification'].update(whole_A3_closed=True))]
    for name, change in changes:
        bad=copy.deepcopy(d); change(bad); assert validate(bad), name
    # Changed source semantics with a fresh calculated digest must still fail.
    p=load(DRAW); bad=copy.deepcopy(p); bad['first_round_origins'][0]['origin']='CHI'
    reader=lambda path: bad if path==DRAW else load(path)
    hasher=lambda path: hashlib.sha256(json.dumps(bad).encode()).hexdigest() if path==DRAW else sha(path)
    assert validate(d,reader,hasher), 'Fresh-SHA upstream wrong origin'
    return len(changes)+1

if __name__ == '__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--write',action='store_true'); ap.add_argument('--check',action='store_true'); ap.add_argument('--self-test',action='store_true'); a=ap.parse_args()
    d=build()
    if a.write:
        (ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (ROOT/MD).write_text(render(d),encoding='utf-8')
    errors=validate(d)
    if a.check:
        errors += validate(load(OUT))
        if text(MD) != render(load(OUT)): errors.append('Markdown differs')
    negatives=self_test(d) if a.self_test else 0
    print(json.dumps({'current':not errors,'summary':d['summary'],'negative_controls':negatives,'errors':errors},ensure_ascii=False))
    if errors: raise SystemExit(1)
