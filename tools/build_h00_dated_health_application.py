"""Apply the selected H00 window, preserving unknown dates and legal HOLDs."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = [
    'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json',
    'simulation/NBA_2020_21_REGULAR_GAME_BASELINE.csv',
    'simulation/CHICAGO_2020_21_DAVIS_WINDOW_CONTACT_AUDIT.json',
    'simulation/CHICAGO_2020_21_LEBRON_WINDOW_CONTACT_AUDIT.json',
]
OUT = 'simulation/LAKERS_2020_21_H00_DATED_HEALTH_APPLICATION.json'


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def build(authority=None, davis=None, lebron=None):
    authority = read(INPUTS[0]) if authority is None else authority
    davis = read(INPUTS[2]) if davis is None else davis
    lebron = read(INPUTS[3]) if lebron is None else lebron
    assert authority['selected']['health']['route'] == 'H00', 'H00 not selected'
    assert authority['selected']['health']['classification'] == 'AUTHOR_MODELED_NOT_HISTORICAL_PROOF'
    assert authority['manuscript_allowed'] is False
    with (ROOT / INPUTS[1]).open(encoding='utf-8-sig', newline='') as handle:
        games = [g for g in csv.DictReader(handle) if 'LAL' in (g['home'], g['away'])]
    ids = [f"{g['date']}_{g['home']}_{g['away']}" for g in games]
    assert len(ids) == len(set(ids)) == 72
    assert [g['date'] for g in games] == sorted(g['date'] for g in games)
    dr = {r['event_id']: 'ABSENT' for r in davis['rows']}
    assert len(dr) == len(davis['rows']) == 30
    dr['2021-02-14_DEN_LAL'] = 'PARTIAL_GAME_INCIDENT'
    lr = {r['event_id']: r['phase'] for r in lebron['rows']}
    assert len(lr) == len(lebron['rows']) == 31
    assert set(dr) | set(lr) <= set(ids), 'health event outside schedule'
    assert Counter(lr.values()) == Counter(
        PARTIAL_GAME_INCIDENT=1, INITIAL_ABSENCE=20, FIRST_RETURN=2,
        SECOND_ABSENCE=6, FINAL_RETURN=2), 'LeBron window phase mismatch'
    rows = []
    for g, event in zip(games, ids):
        players = []
        for player, window in [('Anthony Davis', dr), ('LeBron James', lr)]:
            phase = window.get(event)
            mode = ('OUTSIDE_H00_SCOPE_HOLD' if phase is None else
                    'ABSENT' if phase in ('ABSENT', 'INITIAL_ABSENCE', 'SECOND_ABSENCE') else
                    'PARTIAL_GAME_EXIT_LOAD_HOLD' if phase == 'PARTIAL_GAME_INCIDENT' else
                    'RETURN_LOAD_HOLD')
            players.append(dict(player=player, phase=phase, mode=mode,
                authority='OUTSIDE_SELECTED_SCOPE' if phase is None else 'AUTHOR_MODELED_H00',
                modeled_seconds=0 if mode == 'ABSENT' else None,
                full_health_certified=False, active_list_cleared=False,
                causal_contact_reproduced=False))
        rows.append(dict(date=g['date'], event_id=event, home=g['home'], away=g['away'], players=players))
    counts = Counter(p['mode'] for r in rows for p in r['players'])
    assert counts == Counter(ABSENT=56, PARTIAL_GAME_EXIT_LOAD_HOLD=2,
                            RETURN_LOAD_HOLD=4, OUTSIDE_H00_SCOPE_HOLD=82)
    assert len(set(dr) | set(lr)) == 45
    return dict(status='H00_SELECTED_DATE_APPLICATION_NOT_FULL_HEALTH_PASS',
        baseline_main='ac7985668e07e8e29c490c8a941cbbe83f6ac5c2',
        classification='AUTHOR_MODELED_NOT_HISTORICAL_PROOF',
        source_sha256={p: hashlib.sha256((ROOT/p).read_bytes().replace(b'\r\n', b'\n')).hexdigest() for p in INPUTS},
        selected_route='H00', rows=rows, regular_season_games=72,
        player_game_cells=144, selected_window_cells=62, outside_scope_cells=82,
        distinct_selected_window_games=45, mode_counts=dict(counts),
        scope_selected=True, full_league_health_complete=False,
        postseason_health_inherited=False, legal_execution_cleared=False,
        season_selected=False, manuscript_allowed=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = build()
    if args.check:
        assert read(OUT) == output, 'dated application is stale'
    else:
        (ROOT/OUT).write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS: 72 games / 62 selected cells / 82 HOLD cells; full health/legal/season HOLD')
