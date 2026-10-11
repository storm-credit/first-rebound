"""Audit the actual selected 2023 consumer, without adding B scoring to ratings.

The existing three stage proxies are absolute cumulative development choices.
Earlier expected boxes do not supply an additional rating or scoreboard delta.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import json
from pathlib import Path

from build_early_reward_b_year2_dated_shots import read, sha, jsonbytes, rounded

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = 'design/EARLY_REWARD_B_2023_CUMULATIVE_GROWTH_JOIN_2026_10_12.json'
GROWTH = 'simulation/THREEPEAT_2023_ACCELERATED_GROWTH_AND_ROLE_DESIGN_2026_10_09.json'
DIAGNOSTIC = 'simulation/THREEPEAT_2023_REVISED_REGULAR_AND_STANDINGS_EXECUTION_2026_10_09.json'
RESIDUAL = 'simulation/THREEPEAT_2023_PUBLIC_RESIDUAL_MODEL_CANDIDATES_2026_10_09.json'
SELECTION = 'canon/DELEGATED_THREEPEAT_2023_RESIDUAL_REGULAR_SELECTION_2026_10_09.json'
AUTHOR = 'canon/EARLY_REWARD_B_AUTHOR_SELECTION_2026_10_11.json'
EARLY = 'simulation/EARLY_REWARD_B_GROWTH_AND_YEAR4_ATTACK_2026_10_11.json'
PINS = [GROWTH, DIAGNOSTIC, RESIDUAL, SELECTION, AUTHOR, EARLY,
        'canon/DELEGATED_THREEPEAT_2023_FIRST_TITLE_USED_ROUTE_SELECTION_2026_10_09.json',
        'design/BASKETBALL_SCENE_RESEARCH_APPLICATION_2026_10_09.json']


def checked_rows(growth, diagnostic, residual, selection):
    stages = growth['proxy_model_input']['stages']
    by_stage = {s['id']: s for s in stages}
    assert len(by_stage) == 3
    for stage in stages:
        role = stage['same_minutes']
        assert sum(role.values()) == 240 and role['Protagonist'] == 32
        value = sum(F(minutes) * F(stage['player_proxy_fractions'][p])
                    for p, minutes in role.items()) / 48
        assert value == F(stage['team_proxy_fraction']), 'Added or omitted team bonus'
    candidate = next(c for c in residual['candidates'] if c['id'] == selection['selected_candidate'])
    assert candidate['id'] == 'B_EMPIRICAL_OT'
    common = residual['CHI82_common_reference_and_new_growth_inputs']
    selected = candidate['game_overrides']
    old = {r['calendar_key']: r for r in diagnostic['CHICAGO_82_revised_used_rows']}
    assert len(common) == len(selected) == len(old) == 82
    assert len({r['calendar_key'] for r in common}) == 82
    assert {r['common_row_index'] for r in selected} == set(range(82))
    rows = []
    for game in selected:
        basis = common[game['common_row_index']]
        assert basis['calendar_key'] == game['calendar_key']
        prior = old[basis['calendar_key']]
        stage = by_stage[basis['phase_id']]
        start, end = stage['inclusive_dates']
        assert start <= basis['published_date'] and (end is None or basis['published_date'] <= end)
        team = F(basis['new_CHI_proxy_fraction'])
        assert team == F(stage['team_proxy_fraction'])
        assert prior['phase_id'] == stage['id']
        side = 'revised_home_impact' if basis['home'] == 'CHI' else 'revised_away_impact'
        assert team == F(prior[side])
        zero = (team - F(basis['unchanged_opponent_proxy_fraction'])
                + F(basis['counterfactual_home_effect_CHI_oriented_fraction'])
                + F(basis['counterfactual_B2B_effect_CHI_oriented_fraction']))
        assert zero == F(basis['new_zero_variance_CHI_margin_fraction'])
        assert zero == F(prior['revised_CHI_margin'])
        final = zero + F(game['applied_residual_fraction'])
        assert final == F(game['counterfactual_CHI_margin_fraction']), 'Extra B growth or score delta'
        assert final != 0
        winner = 'CHI' if final > 0 else basis['opponent']
        assert winner == game['candidate_winner']
        assert game['fictional_point_score'] is None
        rows.append({'date': basis['published_date'], 'calendar_key': basis['calendar_key'],
                     'stage_id': stage['id'], 'P_absolute_proxy': stage['player_proxy_fractions']['Protagonist'],
                     'cumulative_team_proxy': str(team), 'zero_variance_margin': str(zero),
                     'selected_residual': game['applied_residual_fraction'], 'selected_margin': str(final),
                     'selected_winner': winner, 'additional_B_rating_or_score_delta': 0})
    wins = sum(r['selected_winner'] == 'CHI' for r in rows)
    assert [wins, 82 - wins] == selection['CHI_record'] == [52, 30]
    assert candidate['CHI_regular_seed']['seed'] == selection['CHI_seed'] == 6
    return rows


def make():
    source = {p: json.loads(read(p)) for p in PINS}
    assert source[AUTHOR]['B']['selected_option'] == 'B'
    rows = checked_rows(source[GROWTH], source[DIAGNOSTIC], source[RESIDUAL], source[SELECTION])
    core = source[GROWTH]['core_first_creation_budget']
    assert sum(core['selected_weights'].values()) == 100
    assert sum(core['selected_minus_comparison'].values()) == 0
    assert core['core_clock_seconds'] == 840
    assert core['selected_minus_comparison']['LaMelo Ball'] == -5
    assert core['selected_minus_comparison']['Zach LaVine'] == -5
    data = {'id': 'EARLY_REWARD_B_2023_CUMULATIVE_GROWTH_JOIN_2026_10_12',
            'status': 'SELECTED_2023_CONSUMER_REPLAY_AND_B_CUMULATIVE_STAGE_JOIN_COMPLETE_EARLIER_DATED_COSTS_PENDING',
            'classification': 'VERIFIED_REPOSITORY_MODEL_ARITHMETIC_AND_EDITORIAL_JOIN_NOT_OBSERVED_PLAYER_GROWTH',
            'source_sha256': {p: sha(p) for p in PINS},
            'author_locked': {'B_direction': True, 'new_exact_boxes_or_awards': False},
            'growth_interpretation': {
                'years1_to4': 'Earlier working expected attack vectors express the selected B direction. Their dated coactor/impact completion remains separate.',
                'year5': 'Existing2023 stage proxies are absolute cumulative2019–22 development assumptions, not increments to be added to the B inputs.',
                'original_negative_half_P_proxy': 'Immutable mathematical comparison baseline from the older zero-growth model; not a measurement of the B year4 scorer.',
                'points_to_proxy_conversion': None,
                'year4_expected20ppg_added_to_2023_score_or_rating': False,
                'chemistry_defense_training_bonus_added_again': False},
            'three_stage_counts': dict(Counter(r['stage_id'] for r in rows)),
            'selected82_replay': rows,
            'selected_regular_record': [52, 30], 'selected_East_seed': 6,
            'diagnostic79_3_is_not_selected_season': True,
            'earlier_learning_to_later_function': [
                {'function': 'P_FIRST_CREATION', 'B_earlier_capacity': 'Year3transition/short-roll own finish; year4elbow counter and early-return finish.',
                 'year5_advance': 'Use the existing limited drive/elbow window more reliably with help and receiver read before catch; do not describe open-lane finishing as first discovered in2023.',
                 'counter': 'Packed paint or denied return ends the attempt; no automatic isolation or second-trap mastery.',
                 'cost': 'The existing840-second core choice budget shifts10 normalized decisions toP atLM−5/LV−5. This is not a new shot quota.'},
                {'function': 'P_WEAK_HAND', 'B_earlier_capacity': 'Year2closeout attack survives an open first window, then gives the short pass if it closes.',
                 'year5_advance': 'Improve repeatability of one weak-hand angle change under the existing counter; keep the rookie opportunity loss and failed carry.',
                 'counter': 'Long switching defender or repeated direction changes can still force reset.',
                 'cost': 'Existing uncomfortable work substitutes for easier attack or rest; no new private training hours.'},
                {'function': 'P_SHORT_ROLL', 'B_earlier_capacity': 'Year3own finish or first visible pass afterLaMelo/Coby initiation.',
                 'year5_advance': 'Earlier help/receiver recognition and timely re-engagement; Carter remains the primary center roller.',
                 'counter': 'Denied cutter and covered center roll leave reset rather than a guaranteed good shot.',
                 'cost': 'Coby PG initiation and independent teammate finishes remain; teammate preparation is not free.'}],
            'remaining': ['Year1/year3 dated shot/coactor budgets', 'Earlier result impact and award competition joins',
                          'C01 exact public path', 'Current9-act history/finalallocation/individualBlueprint/actualPack'],
            'tool_scope': {'Codex_local_source_reads_and_exact_fraction_replay': True,
                           'fresh_Antigravity': False, 'fresh_NotebookLM': False,
                           'Claude': False, 'independent_agent_review': False,
                           'new_primary_box_acquired': False},
            'gates': {'freeze': 'v0.30 PARTIAL', 'design': 'CLOSED', 'manuscript': 'CLOSED', 'actual_Pack': 0},
            'unfinished_major_groups': 4, 'unfinished_through_group6': 3}
    return jsonbytes(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = make()
    target = ROOT / OUTPUT
    if args.write:
        assert not target.exists(), 'Refusing overwrite'
        target.write_bytes(result)
    else:
        assert target.read_bytes().replace(b'\r\n', b'\n') == result, OUTPUT
    print('PASS3 cumulative stages/82 selected margins/52–30/E6; no additional B or chemistry bonus')
