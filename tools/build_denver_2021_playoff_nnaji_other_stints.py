"""Bound Nnaji's three 2021 playoff appearances outside McGee windows.

Minute totals come from NBA official game boxes. The five-man names and
substitution clocks are manually transcribed from FOX Sports play-by-play,
a secondary source. This is a conditional roster/role witness, not a
health, score, or coaching simulation.
"""

import json
from pathlib import Path

import build_chicago_2020_21_season_recommendation as season
import build_denver_2021_playoff_game4_lineups as game4


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "simulation/DENVER_2021_PLAYOFF_NNAJI_OTHER_STINTS.json"
NNAJI = "Zeke Nnaji"
BEY = "Saddiq Bey"
HARTENSTEIN = game4.HARTENSTEIN

# Quarter 4 in all three games. Clock endpoints are from FOX; positive-minute
# game totals are checked against the NBA boxes below.
GAMES = [
    {
        "date": "2021-05-24", "fox_game_id": 37619,
        "nba_box": "https://www.nba.com/game/por-vs-den-0042000162/box-score",
        "official_nnaji_box_seconds": 163,
        "windows": [
            {"start_clock": "02:43", "end_clock": "02:17",
             "original_five": ["Shaquille Harrison", "Facundo Campazzo",
                               "Markus Howard", "Vlatko Cancar", NNAJI]},
            {"start_clock": "02:17", "end_clock": "00:00",
             "original_five": ["Shaquille Harrison", "Markus Howard",
                               "Bol Bol", "Vlatko Cancar", NNAJI]},
        ],
    },
    {
        "date": "2021-06-07", "fox_game_id": 37674,
        "nba_box": "https://www.nba.com/game/den-vs-phx-0042000231/box-score",
        "official_nnaji_box_seconds": 135,
        "windows": [
            {"start_clock": "02:15", "end_clock": "00:00",
             "original_five": ["Shaquille Harrison", "Markus Howard",
                               NNAJI, "Vlatko Cancar", "Bol Bol"]},
        ],
    },
    {
        "date": "2021-06-11", "fox_game_id": 37687,
        "nba_box": "https://www.nba.com/game/phx-vs-den-0042000233/box-score",
        "official_nnaji_box_seconds": 84,
        "windows": [
            {"start_clock": "01:24", "end_clock": "00:00",
             "original_five": ["Markus Howard", NNAJI,
                               "Shaquille Harrison", "Bol Bol", "Vlatko Cancar"]},
        ],
    },
]


def seconds(clock):
    minute, second = clock.split(":")
    return int(minute) * 60 + int(second)


def build():
    source = json.loads((ROOT / "simulation/NBA_2020_21_FINAL859_MINUTES.json")
                        .read_text(encoding="utf-8"))
    roles = {"DEN": source["roles"]["DEN"]}
    out = []
    for game in GAMES:
        windows = []
        for row in game["windows"]:
            original = row["original_five"]
            assert len(original) == len(set(original)) == 5
            assert NNAJI in original and game4.MCGEE not in original
            duration = seconds(row["start_clock"]) - seconds(row["end_clock"])
            assert duration > 0
            bey = [BEY if p == NNAJI else p for p in original]
            hartenstein = [HARTENSTEIN if p == NNAJI else p for p in original]
            assert len(set(bey)) == len(set(hartenstein)) == 5
            windows.append({
                **row,
                "duration_seconds": duration,
                "fox_play_by_play": (
                    "https://www.foxsports.com/nba/boxscore?id="
                    f"{game['fox_game_id']}&tab=playbyplay"
                ),
                "conditional_bey_five": sorted(bey),
                "conditional_bey_k1_role_pass": season.j.bi.valid(bey, "DEN", roles),
                "conditional_hartenstein_five": sorted(hartenstein),
                "conditional_hartenstein_k1_role_pass":
                    season.j.bi.valid(hartenstein, "DEN", roles),
            })
        assert sum(w["duration_seconds"] for w in windows) == game["official_nnaji_box_seconds"]
        out.append({key: value for key, value in game.items() if key != "windows"} | {"windows": windows})
    assert sum(g["official_nnaji_box_seconds"] for g in out) == 382
    all_windows = [w for g in out for w in g["windows"]]
    assert len(all_windows) == 4
    assert [w["conditional_bey_k1_role_pass"] for w in all_windows] == [False, True, True, True]
    assert all(w["conditional_hartenstein_k1_role_pass"] for w in all_windows)
    return {
        "stage": "O-15F14-F5_DENVER_NNAJI_OTHER_PLAYOFF_STINTS",
        "selected": False,
        "original_nnaji_box_seconds_three_games": 382,
        "positive_windows": 4,
        "games": out,
        "limits": "FOX five-man clocks are secondary; NBA official boxes confirm only minute totals. K1 roles are a model, not proof of NBA positional eligibility, health, coaching choice, score, or series outcome.",
    }


if __name__ == "__main__":
    OUT.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT.relative_to(ROOT))
