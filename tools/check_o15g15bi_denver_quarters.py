"""Verify the conditional two-minute Denver rotation witness, not game realism."""

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "simulation/O15G15BI_DENVER_QUARTER_ROTATION.json").read_text(encoding="utf-8"))
earlier = json.loads((ROOT / "simulation/O15G15Z_DENVER_FIVE_MAN_WITNESS.json").read_text(encoding="utf-8"))
assert data["roles"] == ["PG", "SG", "SF", "PF", "C"]
assert len(data["quarters"]) == 4
assert data["slot_minutes"] == 2
assert data["branches"] == earlier["branches"]


def seconds(value):
    minutes, sec = map(int, value.split(":"))
    return minutes * 60 + sec


for branch, branch_data in data["branches"].items():
    slots = []
    for quarter in data["quarters"]:
        assert len(quarter) == 6
        for lineup in quarter:
            assert len(lineup) == 5
            assert all(code in data["names"] for code in lineup)
            names = [data["names"][code].replace("{receiver}", branch_data["receiver"])
                     for code in lineup]
            assert len(set(names)) == 5, (branch, names)
            assert branch_data["excluded_receiver"] not in names
            slots.append(dict(zip(data["roles"], names)))

    totals = Counter(player for slot in slots for player in slot.values())
    expected = {name.replace("{receiver}", branch_data["receiver"]): minutes
                for name, minutes in data["expected_minutes"].items()}
    assert {name: count * 2 for name, count in totals.items()} == expected
    assert sum(expected.values()) == 240
    assert all(sum(player == name for slot in slots for player in slot.values()) * 2 == minutes
               for name, minutes in expected.items())
    assert all(len({slot[role] for role in data["roles"]}) == 5 for slot in slots)
    assert all(len(quarter) * data["slot_minutes"] * len(data["roles"]) == 60
               for quarter in data["quarters"])

    longest = {}
    for player in expected:
        run = longest[player] = 0
        for slot in slots:
            run = run + 2 if player in slot.values() else 0
            longest[player] = max(longest[player], run)
    assert max(longest.values()) <= data["max_continuous_minutes"], longest

    historical = {name.replace("{receiver}", branch_data["receiver"]): seconds(value)
                  for name, value in earlier["expected_minutes"].items()}
    assert set(expected) == set(historical)
    deviations = {name: expected[name] * 60 - historical[name] for name in expected}
    assert sum(deviations.values()) == 0
    assert max(abs(value) for value in deviations.values()) <= 64, deviations
    print(f"{branch}: 4x12-minute quarters, 5 distinct players/slot, 240 team minutes, "
          f"max continuous {max(longest.values())} minutes, max reference deviation "
          f"{max(abs(value) for value in deviations.values())} seconds")
