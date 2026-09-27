"""Check conditional Denver roster slot parity and G15BI membership only."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ledger = json.loads((ROOT / "simulation/O15G15BJ_DENVER_JAN23_ROSTER_SWAP.json").read_text(encoding="utf-8"))
rotation = json.loads((ROOT / "simulation/O15G15BI_DENVER_QUARTER_ROTATION.json").read_text(encoding="utf-8"))
standard = ledger["historical_standard"]
two_way = ledger["historical_two_way"]
swap = ledger["conditional_swap"]
old = swap["outgoing_from_denver_by_approved_gordon_direction"]
new = swap["incoming_2020_denver_pick_if_signed_and_retained"]

assert len(standard) == len(set(standard)) == 15
assert len(two_way) == len(set(two_way)) == 2
assert not set(standard) & set(two_way)
assert old in standard and new not in standard and new not in two_way
alternative = (set(standard) - {old}) | {new}
assert len(alternative) == 15
assert len(alternative | set(two_way)) == 17
assert {"Bryn Forbes", "DeMarcus Cousins", "JaMychal Green"} <= alternative
assert not {"Bol Bol", "PJ Dozier", "Zeke Nnaji"} & alternative

# Jan 19 end-of-day count is an arithmetic backcast from the Jan 23 roster,
# contingent on no other roster-changing event; it is not a timestamped ledger.
assert len(alternative - {"DeMarcus Cousins"}) == 14

for branch, definition in rotation["branches"].items():
    on_court = {rotation["names"][code].replace("{receiver}", definition["receiver"])
                for quarter in rotation["quarters"] for slot in quarter for code in slot}
    assert on_court <= alternative | set(two_way), (branch, on_court - alternative - set(two_way))
    assert old not in on_court
    assert definition["receiver"] in on_court
    assert definition["excluded_receiver"] not in on_court
    assert definition["excluded_receiver"] in alternative
    print(f"{branch}: 15 standard + 2 two-way conditional entries; rotation members present; "
          "unselected receiver remains on roster at 0 minutes")
