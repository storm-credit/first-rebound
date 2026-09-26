"""Cross-check the official final-box names against the prior roster reconstruction."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ledger = json.loads((ROOT / "research" / "O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.json").read_text(encoding="utf-8"))
book = json.loads((ROOT / "research" / "O15G15AG_DETROIT_2021_OPENING_GAMEBOOK.json").read_text(encoding="utf-8"))

groups = [book[k] for k in (
    "detroit_final_box_starters", "detroit_final_box_reserves_played",
    "detroit_final_box_dnp", "detroit_final_box_inactive"
)]
assert [len(g) for g in groups] == [5, 5, 4, 3]
named = [name for group in groups for name in group]
assert len(named) == len(set(named)) == book["expected_named_count"] == 17
two_way = set(book["two_way_from_separate_detroit_source"])
assert two_way == {"Jamorko Pickett", "Chris Smith"}
assert two_way <= set(named)
standard = set(named) - two_way
assert len(standard) == book["expected_standard_reconstruction_count"] == 15

original = set(ledger["historical_august_12_retained"] + ledger["historical_august_12_added_or_resigned"])
for event in ledger["historical_events_after_august_12"]:
    original.difference_update(event["out"])
    original.update(event["in"])
assert standard == original
assert set(book["detroit_final_box_inactive"]) == {"Cade Cunningham", "Isaiah Livers", "Chris Smith"}
assert "Patrick Williams" not in named
print("PASS: 17 official final-box names = 15 reconstructed standard names + 2 separately sourced two-way names")
