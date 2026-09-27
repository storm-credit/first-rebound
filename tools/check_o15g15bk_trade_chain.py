"""Guard against double-spending Bol in the conditional January 2022 trade chain."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "simulation/O15G15BK_DET_DEN_JAN2022_TRADE_BRANCHES.json").read_text(encoding="utf-8"))
events = data["historical_events"]
assert [e["date"] for e in events] == ["2022-01-10", "2022-01-13", "2022-01-19"]
assert events[0]["status"] == "later_rescinded"
assert events[2]["denver_sends"] == ["Bol Bol", "P.J. Dozier"]
assert events[2]["denver_receives"] == ["Bryn Forbes"]

branches = data["branches"]
for name, branch in branches.items():
    assert branch["author_locked"] is False, name
    compatible = branch["bol_owner_before_jan19"] == "Denver"
    assert branch["original_forbes_trade_ownership_compatible"] is compatible, name
    assert branch["bol_owner_before_jan19"] != branch["mcgruder_owner_before_jan19"], name
assert branches["C_trade_completes"]["detroit_mcgruder_minutes"] == "REMOVED"
assert branches["R_rescission_persists"]["forbes_trade_other_conditions"] == "HOLD"
assert data["canon_change"] is False and data["gate_change"] is False
print("O-15G15BK PASS: dated historical events and Bol ownership dependency; all alternate outcomes HOLD")
