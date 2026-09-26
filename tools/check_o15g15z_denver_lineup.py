"""Check only the five simultaneous slots and minute totals of the G15Z witness."""

import json
from collections import defaultdict
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "simulation/O15G15Z_DENVER_FIVE_MAN_WITNESS.json"


def seconds(value: str) -> int:
    minutes, remainder = map(int, value.split(":"))
    assert 0 <= remainder < 60, value
    return 60 * minutes + remainder


data = json.loads(PATH.read_text(encoding="utf-8"))
assert set(data["roles"]) == {"PG", "SG", "SF", "PF", "C"}
for branch, definition in data["branches"].items():
    intervals = {}
    totals = defaultdict(int)
    edges = {0, 48 * 60}
    for role, rows in data["roles"].items():
        parsed = []
        for start, end, name in rows:
            a, b = seconds(start), seconds(end)
            name = name.replace("{receiver}", definition["receiver"])
            assert 0 <= a < b <= 48 * 60, (branch, role, start, end)
            parsed.append((a, b, name))
            totals[name] += b - a
            edges.update((a, b))
        assert parsed[0][0] == 0 and parsed[-1][1] == 48 * 60
        assert all(left[1] == right[0] for left, right in zip(parsed, parsed[1:]))
        intervals[role] = parsed
    for a, b in zip(sorted(edges), sorted(edges)[1:]):
        players = [next(name for start, end, name in rows if start <= a and b <= end)
                   for rows in intervals.values()]
        assert len(players) == len(set(players)) == 5, (branch, a, b, players)
    expected = {name.replace("{receiver}", definition["receiver"]): seconds(value)
                for name, value in data["expected_minutes"].items()}
    assert dict(totals) == expected, (branch, dict(totals), expected)
    assert definition["excluded_receiver"] not in totals
    assert sum(totals.values()) == 240 * 60
    print(f"{branch}: 5 unique players at every interval; each role 48:00; team 240:00; minutes match")
