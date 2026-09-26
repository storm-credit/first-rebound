"""Check the NBA original-history Detroit box and two conditional exit sets."""

import json
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "simulation/NBA_2022_01_23_DET_ORIGINAL_BOX.json"
data = json.loads(PATH.read_text(encoding="utf-8"))
assert data["status"] == "ORIGINAL_HISTORY_OBSERVATION_ONLY"
assert data["game_id"] == "0022100707" and data["team"] == "DET"


def seconds(value: str) -> int:
    minutes, remainder = map(int, value.split(":"))
    assert 0 <= remainder < 60
    return minutes * 60 + remainder


players = data["players"]
assert len(players) == 13 and len({p["person_id"] for p in players}) == 13
assert len([p for p in players if seconds(p["minutes"]) > 0]) == 10
assert len([p for p in players if p["minutes"] == "0:00"]) == 3
for key in ("fga", "fta", "points", "tov"):
    assert sum(p[key] for p in players) == data["team_totals"][key], key
assert sum(seconds(p["minutes"]) for p in players) == seconds(data["team_totals"]["minutes"]) == 240 * 60


def totals(names: set[str]) -> tuple[int, int, int, int]:
    rows = [p for p in players if p["name"] in names]
    assert len(rows) == len(names)
    return (sum(seconds(p["minutes"]) for p in rows),
            sum(p["fga"] for p in rows),
            sum(p["points"] for p in rows),
            sum(p["tov"] for p in rows))


locked_2020 = {"Saddiq Bey", "Killian Hayes"}
db1_extra = {"Cade Cunningham"}
assert totals(locked_2020) == (55 * 60 + 24, 16, 19, 6)
assert totals(locked_2020 | db1_extra) == (91 * 60 + 38, 31, 37, 12)
other_positive = {p["name"] for p in players if seconds(p["minutes"]) and p["name"] not in locked_2020 | db1_extra}
assert len(other_positive) == 7
assert totals(other_positive) == (148 * 60 + 22, 44, 74, 10)
print("original DET: 10 positive + 3 DNP; 240:00 / 75 FGA / 19 FTA / 111 PTS / 22 TOV PASS")
print("2020 locked exits: 55:24 / 16 FGA / 19 PTS / 6 TOV PASS")
print("2020 + conditional DB1 exits: 91:38 / 31 FGA / 37 PTS / 12 TOV PASS")
print("other seven original positive rows: 148:22 / 44 FGA / 74 PTS / 10 TOV PASS")
