"""Reconstruct Denver's June 13 Game 4 five-man lineup clock from its NBA book.

Quarter starters and substitutions are manually transcribed from the official
play-by-play. This verifies a conditional McGee -> Hartenstein slot swap only;
it does not simulate health, fouls, possession outcomes, or the series.
"""

import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "simulation/DENVER_2021_PLAYOFF_GAME4_LINEUP_WITNESS.json"
BOOK = "https://statsdmz.nba.com/pdfs/20210613/20210613_PHXDEN_book.pdf"
JOKIC = "Nikola Jokic"
MCGEE = "JaVale McGee"
HARTENSTEIN = "Isaiah Hartenstein"
PORTER = "Michael Porter Jr."
GORDON = "Aaron Gordon"
BARTON = "Will Barton"
MORRIS = "Monte Morris"
RIVERS = "Austin Rivers"
CAMPAZZO = "Facundo Campazzo"
GREEN = "JaMychal Green"
HARRISON = "Shaquille Harrison"

# (clock, incoming, outgoing); simultaneous substitutions have no intervening
# playing time. Page numbers are the one-based pages in the NBA gamebook.
PERIODS = [
    {"period": 1, "pages": [9, 10],
     "starters": [MORRIS, PORTER, JOKIC, BARTON, GORDON],
     "subs": [("05:17.0", RIVERS, PORTER),
              ("03:27.0", CAMPAZZO, BARTON),
              ("02:58.0", GREEN, GORDON),
              ("00:50.0", PORTER, MORRIS),
              ("00:50.0", MCGEE, JOKIC)]},
    {"period": 2, "pages": [12, 13],
     "starters": [GREEN, PORTER, CAMPAZZO, RIVERS, MCGEE],
     "subs": [("08:59.0", JOKIC, MCGEE),
              ("08:50.0", BARTON, GREEN),
              ("07:57.0", MORRIS, PORTER),
              ("06:56.0", GORDON, RIVERS),
              ("05:50.0", PORTER, CAMPAZZO),
              ("01:12.0", RIVERS, GORDON),
              ("00:29.0", HARRISON, PORTER)]},
    {"period": 3, "pages": [15, 16],
     "starters": [BARTON, MORRIS, JOKIC, PORTER, GORDON],
     "subs": [("05:19.0", RIVERS, PORTER),
              ("03:52.0", CAMPAZZO, JOKIC),
              ("03:52.0", MCGEE, BARTON),
              ("01:49.0", BARTON, MORRIS),
              ("01:49.0", PORTER, GORDON)]},
    {"period": 4, "pages": [17, 18, 19],
     "starters": [PORTER, BARTON, CAMPAZZO, RIVERS, MCGEE],
     "subs": [("08:01.0", GORDON, RIVERS),
              ("05:21.0", MORRIS, CAMPAZZO),
              ("01:29.0", CAMPAZZO, PORTER),
              ("00:21.4", HARRISON, MCGEE),
              ("00:18.7", MCGEE, HARRISON),
              ("00:18.7", PORTER, GORDON)]},
]

BOX_SECONDS = {
    PORTER: 36 * 60 + 16,
    GORDON: 32 * 60 + 40,
    JOKIC: 28 * 60 + 17,
    BARTON: 39 * 60 + 20,
    MORRIS: 34 * 60 + 39,
    RIVERS: 20 * 60 + 51,
    CAMPAZZO: 21 * 60 + 37,
    GREEN: 6 * 60 + 8,
    MCGEE: 19 * 60 + 40,
    HARRISON: 32,
}


def seconds(clock):
    minute, second = clock.split(":")
    value = Decimal(minute) * 60 + Decimal(second)
    assert Decimal(0) <= value <= Decimal(720)
    return value


def build():
    player_seconds = defaultdict(Decimal)
    mcgee_rows = []
    elapsed_mcgee = Decimal(0)
    after_ejection = Decimal(0)
    for entry in PERIODS:
        period = entry["period"]
        lineup = set(entry["starters"])
        assert len(lineup) == 5
        remaining = Decimal(720)
        substitutions = entry["subs"] + [("00:00.0", None, None)]
        for clock, incoming, outgoing in substitutions:
            end = seconds(clock)
            assert end <= remaining
            duration = remaining - end
            for player in lineup:
                player_seconds[player] += duration
            if MCGEE in lineup and duration:
                row = {
                    "period": period,
                    "start_clock": f"{int(remaining // 60):02d}:{remaining % 60:04.1f}",
                    "end_clock": clock,
                    "duration_seconds": float(duration),
                    "original_denver_five": sorted(lineup),
                    "conditional_hartenstein_five": sorted((lineup - {MCGEE}) | {HARTENSTEIN}),
                    "after_jokic_ejection": period == 4 or (period == 3 and remaining <= seconds("03:52.0")),
                }
                mcgee_rows.append(row)
                elapsed_mcgee += duration
                if row["after_jokic_ejection"]:
                    assert JOKIC not in lineup
                    after_ejection += duration
            remaining = end
            if incoming is not None:
                assert outgoing in lineup and incoming not in lineup
                lineup.remove(outgoing)
                lineup.add(incoming)
                assert len(lineup) == 5
        assert remaining == 0

    assert set(player_seconds) == set(BOX_SECONDS)
    differences = {p: float(player_seconds[p] - official)
                   for p, official in BOX_SECONDS.items()}
    assert all(abs(delta) <= 1 for delta in differences.values()), differences
    assert sum(player_seconds.values()) == Decimal(5 * 48 * 60)
    assert abs(elapsed_mcgee - Decimal(1180)) <= Decimal("0.5")
    assert after_ejection == Decimal("949.3")
    assert sum(row["duration_seconds"] for row in mcgee_rows) == float(elapsed_mcgee)
    return {
        "stage": "O-15F14-F5_DENVER_GAME4_LINEUP_CLOCK_WITNESS",
        "official_gamebook": BOOK,
        "date": "2021-06-13",
        "selected": False,
        "period_starters_and_substitutions": PERIODS,
        "official_box_seconds": BOX_SECONDS,
        "reconstructed_seconds": {p: float(value) for p, value in player_seconds.items()},
        "box_minus_clock_differences_seconds": differences,
        "mcgee_on_court_rows": mcgee_rows,
        "mcgee_clock_seconds": float(elapsed_mcgee),
        "mcgee_clock_seconds_after_jokic_ejection": float(after_ejection),
        "limits": "Name-only M1 replacement preserves lineup clocks, not health, coach choice, score, fouls, or series outcome",
    }


if __name__ == "__main__":
    OUT.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT.relative_to(ROOT))
