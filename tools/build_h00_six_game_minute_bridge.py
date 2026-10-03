"""Link H00 partial/return cells to raw observations and normalized team budgets."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = [
    'simulation/LAKERS_2020_21_H00_DATED_HEALTH_APPLICATION.json',
    'simulation/NBA_2020_21_FINAL859_OBSERVATIONS.csv',
    'simulation/NBA_2020_21_FINAL859_MINUTES.json',
    'research/H00_SIX_GAME_PRIMARY_ACCESS_2026_10_03.json',
]
OUT = 'simulation/LAKERS_2020_21_H00_SIX_GAME_MINUTE_BRIDGE.json'


def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))


def build(health=None, branches=None, observations=None):
    health = read(INPUTS[0]) if health is None else health
    branches = read(INPUTS[2])['branches'] if branches is None else branches
    if observations is None:
        with (ROOT/INPUTS[1]).open(encoding='utf-8-sig', newline='') as handle:
            observations = list(csv.DictReader(handle))
    assert health['selected_route'] == 'H00' and health['scope_selected'] is True
    assert health['manuscript_allowed'] is False
    primary = read(INPUTS[3])['web_tool_primary_text_checks']
    primary_map = {(r['event_id'], r['focal_player']): r for r in primary}
    assert len(primary_map) == len(primary) == 2
    focus = [r for r in health['rows'] if any(p['mode'] in
        ('PARTIAL_GAME_EXIT_LOAD_HOLD', 'RETURN_LOAD_HOLD') for p in r['players'])]
    assert len(focus) == 6
    output = []
    for row in focus:
        event = row['event_id']
        candidates = [b for b in branches if b['event_id'] == event and b['team'] == 'LAL']
        assert len(candidates) == 1, 'ambiguous team minute branch'
        branch = candidates[0]
        assert branch['profile'] == 'OBSERVED_HELD' and branch['changed'] is False
        assert branch['actual_seconds'] == branch['alternate_seconds']
        obs = [o for o in observations if o['event_id'] == event and o['team'] == 'LAL']
        assert len(obs) == len({o['player'] for o in obs}), 'duplicate observed player'
        raw = {o['player']: int(o['seconds']) for o in obs if int(o['seconds']) > 0}
        clock = branch['clock_correction']
        assert sum(raw.values()) == clock['raw_total_seconds'], 'raw clock total mismatch'
        normalized = dict(raw)
        if clock['player'] is not None:
            assert clock['player'] in normalized
            normalized[clock['player']] += clock['seconds']
        assert normalized == branch['alternate_seconds'], 'normalized team budget mismatch'
        assert sum(normalized.values()) == 5 * branch['game_duration_seconds'] == 14400
        assert all(0 <= n <= 2880 for n in normalized.values())
        loads = []
        for player in row['players']:
            name = player['player']
            if player['mode'] == 'ABSENT':
                assert normalized.get(name, 0) == 0, 'H00 absence assigned minutes'
            if player['mode'] not in ('PARTIAL_GAME_EXIT_LOAD_HOLD', 'RETURN_LOAD_HOLD'):
                continue
            assert name in raw and player['modeled_seconds'] is None
            assert raw[name] == normalized[name], 'rounding altered focal player'
            observation = next(o for o in obs if o['player'] == name)
            check = primary_map.get((event, name))
            if check is not None:
                assert check['seconds'] == raw[name], 'primary time disagrees with raw observation'
            loads.append(dict(player=name, phase=player['phase'], raw_observed_seconds=raw[name],
                held_candidate_seconds=normalized[name], adopted_seconds=None,
                medical_max_seconds=None, legal_active_list_cleared=False,
                official_reference_url=observation['official_url'],
                primary_seconds_checked_this_run=check is not None,
                primary_pdf_url=None if check is None else check['url'],
                classification='EXISTING_HELD_MINUTE_CANDIDATE_NOT_MEDICAL_LIMIT'))
        output.append(dict(date=row['date'], event_id=event, focal_loads=loads,
            raw_observed_team_total_seconds=sum(raw.values()), clock_normalization=clock,
            held_candidate_team_seconds=normalized, normalized_team_total_seconds=14400,
            exact_substitution_timeline=None, incident_exit_clock=None,
            minute_design_selected=False, legal_registration_cleared=False))
    assert sum(len(r['focal_loads']) for r in output) == 6
    return dict(status='SIX_EXISTING_MINUTE_COMPARATORS_LINKED_NOT_NEW_SELECTION',
        source_sha256={p: hashlib.sha256((ROOT/p).read_bytes().replace(b'\r\n', b'\n')).hexdigest() for p in INPUTS},
        rows=output, focal_cells_linked=6, team_budget_checks=6,
        primary_focal_cells_checked_this_run=2,
        raw_numeric_source='PINNED_PUBLIC_NBA_V3_MIRROR_NOT_ALL_PRIMARY_PDF_AUTHENTICATED',
        health_route_selected='H00', minute_design_selected=False,
        full_health_cleared=False, season_selected=False, manuscript_allowed=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.check:
        assert read(OUT) == result
    else:
        (ROOT/OUT).write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS: 6 focal loads / 6 normalized 240-minute team budgets; medical/legal/final minute HOLD')
