"""Check the named original-history roster and a strictly conditional branch."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research" / "O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.json"
ledger = json.loads(DATA.read_text(encoding="utf-8"))

retained = ledger["historical_august_12_retained"]
added = ledger["historical_august_12_added_or_resigned"]
assert len(retained) == 7 and len(added) == 8
assert len(set(retained + added)) == 15
assert "Mason Plumlee" not in retained + added
assert "Hamidou Diallo" not in retained + added
assert "Luka Garza" not in retained + added

branch = ledger["conditional_same_other_events"]
original = set(retained + added)
replaced = branch["replaced_historical_players"]
replacements = branch["replacement_players"]
assert len(replaced) == len(replacements) == 3
assert set(replaced) <= original
assert not (set(replacements) & original)
conditional = (original - set(replaced)) | set(replacements) | {branch["plumlee_retained"]}
assert len(conditional) == branch["expected_standard_counts"][0] == 16

historical = original.copy()
for idx, event in enumerate(ledger["historical_events_after_august_12"], 1):
    departing = set(event["out"])
    incoming = set(event["in"])
    assert len(departing) == len(event["out"])
    assert len(incoming) == len(event["in"])
    assert departing <= historical, event["event"]
    assert departing <= conditional, event["event"]
    historical -= departing
    conditional -= departing
    assert not incoming & historical, event["event"]
    assert not incoming & conditional, event["event"]
    historical |= incoming
    conditional |= incoming
    assert len(historical) == event["expected_standard_count"], event["event"]
    assert len(conditional) == branch["expected_standard_counts"][idx], event["event"]
    print(f"{event['event']}: original={len(historical)}, conditional={len(conditional)}")

assert len(historical) == 15 and len(conditional) == 16
assert conditional - historical == {"Patrick Williams", "Kira Lewis Jr.", "Jalen Suggs", "Mason Plumlee"}
assert historical - conditional == {"Killian Hayes", "Saddiq Bey", "Cade Cunningham"}
print("PASS: named original roster 15; conditional same-other-events opening roster 16")
