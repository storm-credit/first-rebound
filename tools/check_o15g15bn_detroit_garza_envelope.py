"""Calculate the 2021-22 Detroit schedule ceiling for conditional Garza two-way use."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "simulation/NBA_2021_22_REGULAR_BASELINE.csv").open(encoding="utf-8-sig", newline="") as handle:
    games = [row for row in csv.DictReader(handle) if "DET" in (row["home"], row["away"])]

assert len(games) == 82
assert len({game["game_id"] for game in games}) == 82
assert [game["date"] for game in games] == sorted(game["date"] for game in games)
assert all(game["official_reference_url"].startswith("https://www.nba.com/game/") for game in games)

milestones = {
    1: ("2021-10-20", "CHI", "DET"),
    46: ("2022-01-23", "DET", "DEN"),
    50: ("2022-02-01", "NOP", "DET"),
    51: ("2022-02-03", "MIN", "DET"),
    55: ("2022-02-10", "MEM", "DET"),
    82: ("2022-04-10", "DET", "PHI"),
}
for ordinal, expected in milestones.items():
    game = games[ordinal - 1]
    actual = (game["date"], game["away"], game["home"])
    assert actual == expected, (ordinal, actual, expected)
    print(f"DET game {ordinal:02}: {game['date']} {game['away']}@{game['home']}; all-active count {ordinal}; opening-limit-only stress {ordinal}/50")

assert 55 - 50 == 5  # conditional only: opening 50-game limit retained through game 55
assert 82 - 50 == 32  # conditional only: opening 50-game limit retained all season
print("PASS: 82-date calendar and conditional arithmetic; season-long 50-game limit NOT certified; exception effective dates/payroll HOLD")
