"""Project the author-selected Markkanen M1 price onto G8's 2022 tests."""

import argparse
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
G8 = ROOT / "simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json"
BRIDGE = ROOT / "simulation/CHICAGO_2021_M1_AUTHOR_BRIDGE.json"
OUT = ROOT / "simulation/CHICAGO_2022_M1_TAX_SENSITIVITY.json"


def build(g8, bridge):
    delta = bridge["second_year"]["increment_usd"]
    tax = bridge["second_year"]["tax_reference_usd"]
    assert delta == 1_884_546 and tax == 150_267_000
    assert bridge["player_agreement_world_event_selected"] is True
    cases = g8["budget2022_cases"]
    assert len(cases) == g8["budget2022_case_count"] == 192
    assert Counter(c["policy"] for c in cases) == {f"RT{i}": 48 for i in range(1, 5)}

    counts = Counter()
    crossings = []
    for case in cases:
        old_budget = case["known_budget_excluding_dead_salary"]
        old_room = case["tax_room_before_dead_salary"]
        assert tax - old_budget == old_room
        assert case["dead_salary"] is None
        new_budget = old_budget + delta
        new_room = tax - new_budget
        counts["old_nonnegative"] += old_room >= 0
        counts["new_nonnegative"] += new_room >= 0
        counts["old_negative"] += old_room < 0
        counts["new_negative"] += new_room < 0
        if old_room >= 0 > new_room:
            crossings.append({
                "policy": case["policy"],
                "protagonist_first_usd": case["protagonist_first"],
                "Carter_first_usd": case["Carter_first"],
                "Young_or_replacement_usd": case["Young_or_replacement"],
                "draft2022_reserve_usd": case["draft2022_reserve"],
                "old_room_before_dead_salary_usd": old_room,
                "M1_room_before_dead_salary_usd": new_room,
            })
    assert counts == {
        "old_nonnegative": 168, "new_nonnegative": 156,
        "old_negative": 24, "new_negative": 36,
    }
    assert Counter(c["policy"] for c in crossings) == {f"RT{i}": 3 for i in range(1, 5)}
    return {
        "status": "CONDITIONAL_G1A_G8_RT1_TO_RT4_ONLY",
        "source_cases": str(G8.relative_to(ROOT)),
        "author_selected_price": str(BRIDGE.relative_to(ROOT)),
        "tax_reference_usd": tax,
        "M1_second_year_increment_usd": delta,
        "case_count": len(cases),
        "counts": dict(counts),
        "crossing_count": len(crossings),
        "crossings": crossings,
        "dead_salary_usd": None,
        "other_unknown_charges_usd": None,
        "actual_tax_status": None,
        "G1C_or_G1D_applicable": False,
        "season_selected": False,
        "exact_execution_cleared": False,
        "manuscript_allowed": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build(json.loads(G8.read_text(encoding="utf-8")),
                 json.loads(BRIDGE.read_text(encoding="utf-8")))
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(json.dumps({"PASS": True, "cases": data["case_count"],
                      "crossings": data["crossing_count"],
                      "actual_tax_status": data["actual_tax_status"]}))


if __name__ == "__main__":
    main()
