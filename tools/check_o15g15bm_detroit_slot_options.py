"""Rebuild G15AF's conditional 16 names and test named A/B slot arithmetic."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = json.loads((ROOT / "research/O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.json").read_text(encoding="utf-8"))
board = json.loads((ROOT / "simulation/O15G15BM_DETROIT_OPENING_SLOT_OPTIONS.json").read_text(encoding="utf-8"))

roster = set(source["historical_august_12_retained"] + source["historical_august_12_added_or_resigned"])
branch = source["conditional_same_other_events"]
assert set(branch["replaced_historical_players"]) <= roster
roster.difference_update(branch["replaced_historical_players"])
roster.update(branch["replacement_players"])
roster.add(branch["plumlee_retained"])
for event in source["historical_events_after_august_12"]:
    assert set(event["out"]) <= roster
    roster.difference_update(event["out"])
    roster.update(event["in"])
assert len(roster) == 16

rotation = set(board["required_g14_rotation"])
assert len(rotation) == 10 and rotation <= roster
for label, option in board["options"].items():
    assert option["status"] == "CANDIDATE_HOLD"
    removed = option["remove_from_standard"]
    assert removed in roster and removed not in rotation
    standard = roster - {removed}
    two_way = set(option["two_way"])
    assert len(standard) == 15 and len(two_way) == 2
    assert not standard & two_way
    assert rotation <= standard
    print(f"{label}: 15 standard + 2 two-way conditional names; G14 ten preserved")
assert board["options"]["A_garza_two_way_retained"]["future_active_list_cap"] == 50
assert board["options"]["A_garza_two_way_retained"]["excluded_from_two_way"] == "Jamorko Pickett"
assert board["author_locked"] is False and board["season_selected"] is False and board["gate_change"] is False
