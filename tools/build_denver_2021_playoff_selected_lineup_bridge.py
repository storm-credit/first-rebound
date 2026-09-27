"""Expose the selected Gordon/McGee transaction route's playoff roster collision.

Hartenstein replaces the absent McGee on four original-game clock windows;
Bey replaces Nnaji where the two original players overlapped. This is a
role/count witness for a conditional schedule, not a score or health model.
"""

import json
from pathlib import Path

import build_chicago_2020_21_season_recommendation as k
import build_denver_2021_playoff_game4_lineups as game4
import build_denver_2021_playoff_other_lineups as other


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "simulation/DENVER_2021_PLAYOFF_SELECTED_LINEUP_BRIDGE.json"
BEY = "Saddiq Bey"
NNAJI = "Zeke Nnaji"

# NBA original boxes for Nnaji's three additional positive-minute games.
# Their five-man substitutions are not reconstructed in this local bridge.
NNAJI_OTHER_GAMES = [
    {"date": "2021-05-24", "seconds": 163,
     "source": "https://www.nba.com/game/por-vs-den-0042000162/box-score"},
    {"date": "2021-06-07", "seconds": 135,
     "source": "https://www.nba.com/game/den-vs-phx-0042000231/box-score"},
    {"date": "2021-06-11", "seconds": 84,
     "source": "https://www.nba.com/game/phx-vs-den-0042000233/box-score"},
]


def build():
    original = json.loads((ROOT / "simulation/NBA_2020_21_FINAL859_MINUTES.json")
                          .read_text(encoding="utf-8"))
    roles = {"DEN": original["roles"]["DEN"]}
    short = other.build()
    long = game4.build()
    windows = [(game["date"], row) for game in short["games"]
               for row in game["mcgee_lineup_rows"]]
    windows += [(long["date"], row) for row in long["mcgee_on_court_rows"]]
    assert len(windows) == 14
    rows = []
    overlap = 0.0
    for date, row in windows:
        original_five = row["original_denver_five"]
        assert game4.MCGEE in original_five
        candidate = [game4.HARTENSTEIN if p == game4.MCGEE else
                     BEY if p == NNAJI else p for p in original_five]
        assert len(candidate) == len(set(candidate)) == 5
        assert game4.MCGEE not in candidate and NNAJI not in candidate
        role_valid = k.j.bi.valid(candidate, "DEN", roles)
        assert role_valid, (date, candidate)
        if NNAJI in original_five:
            overlap += row["duration_seconds"]
        rows.append({"date": date, "period": row["period"],
                     "start_clock": row["start_clock"], "end_clock": row["end_clock"],
                     "seconds": row["duration_seconds"],
                     "original_five": original_five, "candidate_five": sorted(candidate),
                     "original_nnaji_present": NNAJI in original_five,
                     "role_model_pass": role_valid})
    assert sum(row["seconds"] for row in rows) == 2029.4
    assert overlap == 677.0
    assert sum(game["seconds"] for game in NNAJI_OTHER_GAMES) == 382
    return {
        "stage": "O-15F14-F5_DENVER_PLAYOFF_SELECTED_ROSTER_COLLISION_BRIDGE",
        "selected": False,
        "author_locked_directions": {"gordon_a_sends_nnaji_to_orlando": True,
                                     "mcgee_hartenstein_trade": "omit"},
        "original_mcgee_box_seconds_four_games": 2029,
        "original_mcgee_clock_seconds_four_games": 2029.4,
        "original_nnaji_overlap_with_mcgee_clock_seconds": overlap,
        "original_nnaji_other_positive_game_box_seconds": NNAJI_OTHER_GAMES,
        "original_nnaji_positive_box_seconds_at_least": int(overlap) + 382,
        "mcgee_windows": rows,
        "limits": "Conditional Bey/Hartenstein role/count witness only; three other Nnaji games lack lineup clocks and no score, health, roster eligibility, or series result is certified",
    }


if __name__ == "__main__":
    OUT.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT.relative_to(ROOT))
