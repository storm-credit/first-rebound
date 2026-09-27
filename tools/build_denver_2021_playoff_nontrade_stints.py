"""Arithmetic witness for a conditional McGee -> Hartenstein playoff swap.

The substitution timestamps below are transcribed from NBA official gamebooks.
This checks elapsed court time, not alternate-world health, coaching, or score.
"""

import json
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "simulation/DENVER_2021_PLAYOFF_NONTRADE_STINTS.json"

GAMES = [
    {
        "date": "2021-05-29", "opponent": "POR", "round": "first_round_game_4",
        "gamebook": "https://statsdmz.nba.com/pdfs/20210529/20210529_DENPOR_book.pdf",
        "official_mcgee_seconds": 434,
        "stints": [(4, "07:14.0", 4, "00:00.0")],
    },
    {
        "date": "2021-06-01", "opponent": "POR", "round": "first_round_game_5",
        "gamebook": "https://statsdmz.nba.com/pdfs/20210601/20210601_PORDEN_book.pdf",
        "official_mcgee_seconds": 2,
        "stints": [(1, "00:02.1", 1, "00:00.0")],
    },
    {
        "date": "2021-06-09", "opponent": "PHX", "round": "west_semifinal_game_2",
        "gamebook": "https://statsdmz.nba.com/pdfs/20210609/20210609_DENPHX_book.pdf",
        "official_mcgee_seconds": 413,
        "stints": [(4, "06:53.0", 4, "00:00.0")],
    },
    {
        "date": "2021-06-13", "opponent": "PHX", "round": "west_semifinal_game_4",
        "gamebook": "https://statsdmz.nba.com/pdfs/20210613/20210613_PHXDEN_book.pdf",
        "official_mcgee_seconds": 1180,
        "jokic_ejection": {"period": 3, "clock": "03:52.0"},
        "stints": [
            (1, "00:50.0", 2, "08:59.0"),
            (3, "03:52.0", 4, "00:21.4"),
            (4, "00:18.7", 4, "00:00.0"),
        ],
    },
]


def elapsed(period, clock):
    minutes, seconds = clock.split(":")
    remaining = Decimal(minutes) * 60 + Decimal(seconds)
    assert 0 <= remaining <= 720
    return Decimal(period - 1) * 720 + 720 - remaining


def build():
    rows = []
    for game in GAMES:
        stints = []
        for start_period, start_clock, end_period, end_clock in game["stints"]:
            begin = elapsed(start_period, start_clock)
            end = elapsed(end_period, end_clock)
            assert end > begin
            stints.append({
                "start_period": start_period, "start_clock": start_clock,
                "end_period": end_period, "end_clock": end_clock,
                "elapsed_seconds": float(end - begin),
            })
        assert all(
            elapsed(left["end_period"], left["end_clock"])
            <= elapsed(right["start_period"], right["start_clock"])
            for left, right in zip(stints, stints[1:])
        )
        total = sum(Decimal(str(stint["elapsed_seconds"])) for stint in stints)
        # The gamebook box rounds displayed tenths to a whole second.
        assert abs(total - game["official_mcgee_seconds"]) <= Decimal("0.5")
        row = {key: value for key, value in game.items() if key != "stints"}
        row["stints"] = stints
        row["transcribed_stint_seconds"] = float(total)
        if "jokic_ejection" in game:
            moment = elapsed(game["jokic_ejection"]["period"], game["jokic_ejection"]["clock"])
            row["mcgee_seconds_at_or_after_ejection"] = float(sum(
                max(Decimal(0), elapsed(s["end_period"], s["end_clock"])
                    - max(moment, elapsed(s["start_period"], s["start_clock"])))
                for s in stints
            ))
        rows.append(row)
    assert sum(row["official_mcgee_seconds"] for row in rows) == 2029
    return {
        "stage": "O-15F14-AC_DENVER_PLAYOFF_NONTRADE_STINT_WITNESS",
        "scope": "Original gamebook substitutions only; conditional direct name swap preserves on-court slot arithmetic, not playoff result or medical availability",
        "author_locked": {"mcgee_hartenstein_march25_trade": "omit"},
        "alternate_rotation_selected": False,
        "playoff_result_selected": False,
        "games": rows,
        "official_mcgee_total_seconds": 2029,
    }


if __name__ == "__main__":
    OUT.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT.relative_to(ROOT))
