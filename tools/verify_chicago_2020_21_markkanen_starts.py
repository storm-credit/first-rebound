"""Check conditional Markkanen starter policies against stored F6B player minutes.

Requires scipy/numpy. This is a mathematical lineup existence check, not an
alternate box score, coaching decision, or player-consent certificate.
"""

import hashlib
import json
from pathlib import Path

import audit_chicago_2020_21_postdeadline_lineups as lineup


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'simulation/CHICAGO_2020_21_POSTDEADLINE_LINEUP_AUDIT.json'
MARKKANEN = 'Lauri Markkanen'
POLICIES = {
    'S0': (False, False, 3, 0),
    'S1': (True, True, 28, 25),
    'S2': (True, False, 17, 14),
    'S3': (False, True, 14, 11),
}


def main():
    stored = json.loads(AUDIT.read_text(encoding='utf-8'))
    # The Git blob uses LF while Windows checkouts may use CRLF.
    source = lineup.SOURCE.read_bytes().replace(b'\r\n', b'\n')
    assert hashlib.sha256(source).hexdigest() == stored['source_sha256']
    games = sorted((g for g in stored['games'] if g['scenario'] == 'PORTER_ZERO'), key=lambda g: g['date'])
    assert len(games) == 29
    assert sum(MARKKANEN in g['minimum_change_candidate']['player_seconds'] for g in games) == 28

    for name, (replace_young, replace_theis, expected_starts, expected_swaps) in POLICIES.items():
        starts = swaps = 0
        for game in games:
            raw = game['minimum_change_candidate']['player_seconds']
            assert game['minimum_change_candidate']['status'] == 'CONDITIONAL_CERTIFICATE_PASS'
            target = {player: round(seconds) for player, seconds in raw.items()}
            assert max(abs(raw[player] - target[player]) for player in target) < 1e-5
            assert sum(target.values()) == 14400

            starters = set(game['candidate_starters'])
            if MARKKANEN in target and MARKKANEN not in starters:
                donor = ('Thaddeus Young' if replace_young and 'Thaddeus Young' in starters
                         else 'Daniel Theis' if replace_theis and 'Daniel Theis' in starters
                         else None)
                if donor:
                    starters.remove(donor)
                    starters.add(MARKKANEN)
                    swaps += 1
            starts += MARKKANEN in starters
            assert len(starters) == 5 and all(target.get(player, 0) >= 180 for player in starters)
            assert lineup.valid(starters, 2)

            witness = lineup.solve(target, sorted(starters), 2)
            assert witness['status'] == 'CONDITIONAL_CERTIFICATE_PASS', (name, game['date'], witness)
            assert abs(sum(segment['seconds'] for segment in witness['segments']) - 2880) < 1e-5
            assert max(abs(witness['player_seconds'][p] - target[p]) for p in target) < 1e-5

        assert (starts, swaps) == (expected_starts, expected_swaps), (name, starts, swaps)
        print(f'{name}: PASS 29/29 conditional 48-minute lineups; {starts} Markkanen starts; {swaps} swaps')


if __name__ == '__main__':
    main()
