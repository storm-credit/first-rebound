"""Check named Detroit slots in a hypothetical Feb. 10 Bagley follow-up to option A."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = json.loads((ROOT / "research/O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.json").read_text(encoding="utf-8"))
options = json.loads((ROOT / "simulation/O15G15BM_DETROIT_OPENING_SLOT_OPTIONS.json").read_text(encoding="utf-8"))
bridge = json.loads((ROOT / "simulation/O15G15BO_DETROIT_GARZA_BAGLEY_SLOT_BRIDGE.json").read_text(encoding="utf-8"))

standard = set(source["historical_august_12_retained"] + source["historical_august_12_added_or_resigned"])
branch = source["conditional_same_other_events"]
standard.difference_update(branch["replaced_historical_players"])
standard.update(branch["replacement_players"])
standard.add(branch["plumlee_retained"])
for event in source["historical_events_after_august_12"]:
    if event["event"] == "Garza two-way conversion":
        continue
    assert set(event["out"]) <= standard
    standard.difference_update(event["out"])
    standard.update(event["in"])

assert bridge["opening_option"] == "A_garza_two_way_retained"
two_way = set(options["options"][bridge["opening_option"]]["two_way"])
assert len(standard) == 15 and two_way == {"Luka Garza", "Chris Smith"}
assert "Jamorko Pickett" not in standard | two_way
print("A opening: 15 standard + Garza/Smith two-way")

trade = bridge["trade_assumed"]
assert set(trade["standard_out"]) <= standard
standard.difference_update(trade["standard_out"])
standard.update(trade["standard_in"])
assert len(standard) == 14 and len(two_way) == 2
print("conditional Bagley trade completion: 14 standard + 2 two-way")

convert = bridge["conversion_assumed"]
assert convert in two_way and convert not in standard
two_way.remove(convert)
standard.add(convert)
assert len(standard) == 15 and len(two_way) == 1
print("conditional Garza conversion: 15 standard + Smith two-way")

pickett = bridge["later_two_way_candidate"]
assert pickett not in standard | two_way
two_way.add(pickett)
assert len(standard) == 15 and two_way == {"Chris Smith", "Jamorko Pickett"}
print("conditional Pickett signing: 15 standard + Smith/Pickett two-way")

assert not bridge["trade_assumed"]["other_teams_and_assets_verified_in_alt"]
assert not bridge["pickett_available_and_accepts"]
assert not bridge["author_locked"] and not bridge["gate_change"]
print("PASS: four named sets only; trade, conversion, Pickett and cap remain HOLD")
