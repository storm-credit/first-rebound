"""Check the conditional named-charge arithmetic, not CBA eligibility."""

import json
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "research" / "O15G15AJ_DETROIT_AUG6_NAMED_SALARY_LEDGER.json"
data = json.loads(path.read_text(encoding="utf-8"))
base = sum(data["original_core"].values()) + sum(data["candidate_dead_money"].values()) + sum(data["original_common_additions"].values())
delta = sum(data["alternate_replacements"].values())
qos = data["original_optional_additions"]
cases = {
    "no Frank/Diallo charge": base,
    "Diallo QO only": base + qos["Hamidou Diallo outstanding QO case"],
    "Diallo and Frank QOs": base + qos["Hamidou Diallo outstanding QO case"] + qos["Frank Jackson outstanding QO case"],
    "Diallo QO and Frank signed": base + qos["Hamidou Diallo outstanding QO case"] + qos["Frank Jackson signed contract case"],
}
assert base == 107216181
assert delta == 5133060
assert cases["Diallo QO and Frank signed"] == 112296007
for name, original in cases.items():
    alternate = original + delta
    print(f"{name}: original={original:,}; alternate={alternate:,}; alternate-minus-cap={alternate-data['cap']:+,}")
