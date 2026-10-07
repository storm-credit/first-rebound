"""Audit four omitted-trade source branches against the fixed PR442 baseline."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '75a1d526e78ef53fbf3e72fa7cad8899a57debf9'
OVERLAY = 'simulation/NBA_2020_21_SELECTED_REGULAR_OVERLAY.json'
CLOCK = 'simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.json'
OUT = 'reviews/F5_FOUR_SOURCE_BRANCH_COMPLETION_REVIEW_2026_10_07.json'
EXPECTED = {
    ('2021-04-09_DEN_SAS', 'DEN'): ('JaVale McGee', 'Isaiah Hartenstein', 579),
    ('2021-04-28_DEN_NOP', 'DEN'): ('JaVale McGee', 'Isaiah Hartenstein', 691),
    ('2021-04-17_CHI_CLE', 'CLE'): ('Isaiah Hartenstein', 'JaVale McGee', 962),
    ('2021-04-21_CLE_CHI', 'CLE'): ('Isaiah Hartenstein', 'JaVale McGee', 973),
}


def read(path, baseline=False):
    if baseline:
        return json.loads(subprocess.check_output(['git', 'show', BASELINE+':'+path], cwd=ROOT).decode('utf-8-sig'))
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256((ROOT/path).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n').encode()).hexdigest()


def verify(old, new):
    before = {(r['event_id'], r['team']): r for r in old['team_games']}
    after = {(r['event_id'], r['team']): r for r in new['team_games']}
    assert len(after) == len(new['team_games']) == 2160 and set(before) == set(after)
    changed = {k for k in before if before[k]['player_seconds'] != after[k]['player_seconds']}
    assert changed == set(EXPECTED), 'exact four source branches required'
    for key, (donor, receiver, seconds) in EXPECTED.items():
        source, target = before[key], after[key]
        vector = deepcopy(source['player_seconds'])
        assert vector.pop(donor) == seconds and receiver not in vector
        vector[receiver] = seconds
        assert target['player_seconds'] == vector, 'source-correct counterpart and every other player-second required'
        assert target['overlay_stage'] == 'F5_SCOPE_COMPLETION'
        assert target['f5_scope_completion']['original_full_vector'] == source['player_seconds']
        assert target['f5_scope_completion']['original_donor'] == donor
        assert target['f5_scope_completion']['retained_counterpart'] == receiver
        assert target['f5_scope_completion']['seconds'] == seconds
    assert all(before[k]['starters'] == after[k]['starters'] for k in before)
    assert all(before[k]['game_duration_seconds'] == after[k]['game_duration_seconds'] for k in before)
    results = {g['event_id']: g for g in new['regular_season_games']}
    prior = {g['event_id']: g for g in old['regular_season_games']}
    assert len(results) == 1080 and set(results) == set(prior)
    assert all(results[k]['winner'] == prior[k]['winner'] for k in results)
    assert new['unresolved_games'] == new['changed_winner_games'] == []
    assert new['recomputed_team_wins'] == old['recomputed_team_wins']
    return before, after, results


def build():
    old, new = read(OVERLAY, True), read(OVERLAY)
    before, after, games = verify(old, new)
    old_clock, clock = read(CLOCK, True), read(CLOCK)
    # All pre-existing source witnesses remain byte-for-value identical.
    retained = [r for r in old_clock['team_games'] if r['lineup_witness_kind'] == 'EXISTING_SOURCE_SEGMENTS_ORDER_NOT_CHRONOLOGY']
    current = {(r['event_id'], r['team']): r for r in clock['team_games']}
    assert len(retained) == 107
    assert all(current[(r['event_id'], r['team'])]['lineup_witness'] == r['lineup_witness'] for r in retained)
    return dict(baseline_main=BASELINE, source_sha256={p:sha(p) for p in [OVERLAY, CLOCK, 'tools/audit_2020_21_f5_source_branch_completion.py']},
        classification='MECHANICAL_CORRECTION_WITHIN_APPROVED_F5_AND_DELEGATED_MINUTE_MODEL',
        changed_vectors=4, unchanged_vectors=2156, changed_starters=0, changed_team_clocks=0,
        existing_witnesses_preserved=107, changed_regular_winners=0, unresolved_regular_winners=0,
        changed_standings=0,
        corrections=[dict(event_id=k[0], team=k[1], removed=v[0], retained_counterpart=v[1], seconds=v[2],
                          selected_winner=games[k[0]]['winner'], home_margin_band=games[k[0]]['home_margin_band'])
                     for k,v in sorted(EXPECTED.items())],
        historical_raw_inputs_modified=False, new_author_choice_required=False,
        actual_medical_or_registration_certified=False, season_selected=False, manuscript_allowed=False)


def self_test():
    old, new = read(OVERLAY, True), read(OVERLAY)
    for key in EXPECTED:
        bad = deepcopy(new)
        row = next(r for r in bad['team_games'] if (r['event_id'], r['team']) == key)
        source = next(r for r in old['team_games'] if (r['event_id'], r['team']) == key)
        row['player_seconds'] = deepcopy(source['player_seconds'])
        try: verify(old, bad)
        except AssertionError: continue
        raise AssertionError('historical traded donor restoration accepted: '+str(key))
    return 4


if __name__ == '__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); ap.add_argument('--self-test', action='store_true')
    args=ap.parse_args(); data=build()
    if args.check: assert read(OUT)==data, 'saved F5 correction review stale'
    else: (ROOT/OUT).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(changed_vectors=4, unchanged_vectors=2156, winner_changes=0,
                         negative_tests=self_test() if args.self_test else 0)))
