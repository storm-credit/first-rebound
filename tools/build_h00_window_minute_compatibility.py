"""Check selected H00 cells against complete held budgets, including overtime."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEALTH = 'simulation/LAKERS_2020_21_H00_DATED_HEALTH_APPLICATION.json'
FOCAL = 'simulation/LAKERS_2020_21_H00_SIX_GAME_MINUTE_BRIDGE.json'
LEDGERS = [
    'simulation/NBA_2020_21_FINAL859_MINUTES.json',
    'simulation/CHICAGO_2020_21_REMAINING_PAIRED_IMPACT.json',
    'simulation/CHICAGO_2020_21_BOUNDARY_PAIRED_IMPACT.json',
]
OUT = 'simulation/LAKERS_2020_21_H00_WINDOW_MINUTE_COMPATIBILITY.json'


def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))


def build(ledgers=None):
    health = read(HEALTH)
    assert health['selected_route'] == 'H00' and health['scope_selected'] is True
    assert not health['manuscript_allowed'] and not health['full_league_health_complete']
    if ledgers is None:
        ledgers = {path: read(path)['branches'] for path in LEDGERS}
    focal = {(r['event_id'], p['player']): p for r in read(FOCAL)['rows'] for p in r['focal_loads']}
    output = []
    cells = Counter()
    source_counts = Counter()
    for row in health['rows']:
        selected = [p for p in row['players'] if p['authority'] == 'AUTHOR_MODELED_H00']
        if not selected:
            continue
        # Latest final ledger first; earlier supplemental ledgers only fill missing dates.
        branch = None
        for source in LEDGERS:
            matches = [b for b in ledgers[source] if b['event_id'] == row['event_id'] and b['team'] == 'LAL']
            if matches:
                assert len(matches) == 1, 'ambiguous Lakers budget'
                branch = matches[0]
                break
        assert branch is not None, 'missing selected-window budget'
        assert branch['profile'] == 'OBSERVED_HELD' and branch['changed'] is False
        assert branch['actual_seconds'] == branch['alternate_seconds'], 'held budget altered'
        duration = branch['game_duration_seconds']
        assert duration >= 2880 and (duration - 2880) % 300 == 0, 'invalid overtime duration'
        minutes = branch['alternate_seconds']
        assert all(isinstance(v, int) and 0 < v <= duration for v in minutes.values())
        assert sum(minutes.values()) == duration * 5, 'team clock conservation'
        clock = branch['clock_correction']
        assert clock['raw_total_seconds'] + clock['seconds'] == duration * 5
        checked = []
        for player in selected:
            name = player['player']
            assigned = minutes.get(name, 0)
            if player['mode'] == 'ABSENT':
                assert player['modeled_seconds'] == assigned == 0, 'selected absence has positive minutes'
                rule = 'NO_POSITIVE_ASSIGNMENT_TO_SELECTED_ABSENCE'
            else:
                assert player['modeled_seconds'] is None
                assert assigned == focal[(row['event_id'], name)]['held_candidate_seconds']
                rule = 'EXISTING_PARTIAL_OR_RETURN_COMPARATOR_ONLY'
            cells[player['mode']] += 1
            checked.append(dict(player=name, health_mode=player['mode'], held_seconds=assigned,
                check=rule, compatible=True, exact_minutes_adopted=False,
                medical_maximum_certified=False, active_list_cleared=False))
        source_counts[source] += 1
        output.append(dict(event_id=row['event_id'], date=row['date'], source_ledger=source,
            profile=branch['profile'], duration_seconds=duration,
            overtime_periods=(duration-2880)//300, team_budget_seconds=sum(minutes.values()),
            clock_normalization=clock, checked_cells=checked,
            outside_H00_scope_players='NOT_MEDICALLY_TESTED', legal_registration_cleared=False))
    assert len(output) == 45
    assert cells == Counter(ABSENT=56, PARTIAL_GAME_EXIT_LOAD_HOLD=2, RETURN_LOAD_HOLD=4)
    overtime = [r['event_id'] for r in output if r['overtime_periods']]
    assert overtime == ['2021-02-22_LAL_WAS', '2021-04-17_LAL_UTA', '2021-05-11_LAL_NYK']
    inputs = [HEALTH, FOCAL] + LEDGERS
    return dict(status='SELECTED_H00_WINDOW_COMPATIBLE_WITH_EXISTING_HELD_BUDGETS',
        baseline_main='a6cf40f63a9c0edb8abf2b3b1f797c57b7e6c9fb',
        source_sha256={p: hashlib.sha256((ROOT/p).read_bytes().replace(b'\r\n', b'\n')).hexdigest() for p in inputs},
        rows=output, selected_window_games_checked=45, selected_cells_checked=62,
        mode_counts=dict(cells), source_game_counts=dict(source_counts),
        overtime_games=overtime, missing_selected_window_games=0, conflicting_cells=0,
        comparison_priority=LEDGERS, raw_source_scope='EXISTING_PINNED_NUMERIC_INPUTS_NOT_NEW_PRIMARY_AUTHENTICATION',
        all_72_games_medically_cleared=False, whole_league_health_cleared=False,
        exact_minutes_selected=False, legal_registration_cleared=False,
        season_selected=False, manuscript_allowed=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.check:
        assert read(OUT) == result
    else:
        (ROOT/OUT).write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS: selected H00 45 games / 62 cells / 56 absence checks; 3 overtime games; full health/legal HOLD')
