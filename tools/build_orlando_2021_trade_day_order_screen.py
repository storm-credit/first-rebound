"""Compare both March 25 Orlando trade orders using listed annual commitments.

This is a conditional stress screen, not an NBA transaction or hard-cap clearance.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORL = ROOT / "research/ORLANDO_2020_21_PAYROLL_SOURCES.json"
TERMS = ROOT / "research/NBA_2020_21_L_EXECUTION_TERMS_SOURCES.json"
POST = ROOT / "simulation/ORLANDO_2020_21_PAYROLL_BOUND.json"
OUT = ROOT / "simulation/ORLANDO_2021_MARCH25_TRADE_ORDER_SCREEN.json"


def listed_amount(row, include_unlikely):
    return (row["base_usd"] + row["reported_likely_usd"]
            + (row["reported_unlikely_usd"] if include_unlikely else 0))


def build():
    orl = json.loads(ORL.read_text(encoding="utf-8"))
    terms = json.loads(TERMS.read_text(encoding="utf-8"))
    post = json.loads(POST.read_text(encoding="utf-8"))
    core = {row["player"]: row for row in orl["core_players"]}
    salary = {row["player"]: row for row in terms["salary_rows"]}
    assert len(core) == len(orl["core_players"])
    names = ("Aaron Gordon", "Gary Clark", "Evan Fournier", "Gary Harris")
    assert all(name in salary for name in names)
    assert all(salary[name]["reported_cap_hit_usd"] == listed_amount(salary[name], False)
               for name in names)
    assert listed_amount(core["Gary Harris"], True) == listed_amount(salary["Gary Harris"], True)
    birch = next(row["budget_usd"] for row in orl["previous_contract_budgets"]
                 if row["player"] == "Khem Birch")
    teague = next(row["budget_usd"] for row in orl["previous_contract_budgets"]
                  if row["player"] == "Jeff Teague")
    camp = sum(row["annual_base_usd"] for row in orl["camp_stress"])
    apron = orl["thresholds"]["apron_usd"]
    tax = orl["thresholds"]["tax_usd"]

    def amounts(include_unlikely):
        static = sum(listed_amount(row, include_unlikely) for player, row in core.items()
                     if player not in ("Gary Harris", "Zeke Nnaji")) + birch
        gordon_clark = sum(listed_amount(salary[name], include_unlikely)
                           for name in ("Aaron Gordon", "Gary Clark"))
        fournier = listed_amount(salary["Evan Fournier"], include_unlikely)
        harris_nnaji = (listed_amount(salary["Gary Harris"], include_unlikely)
                        + listed_amount(core["Zeke Nnaji"], include_unlikely))
        before = static + gordon_clark + fournier
        gordon_first = before - gordon_clark + harris_nnaji
        fournier_first = before - fournier + teague
        after = static + harris_nnaji + teague
        assert gordon_first - fournier + teague == after
        assert fournier_first - gordon_clark + harris_nnaji == after
        return {"inputs": {"static_core_plus_birch": static, "gordon_clark": gordon_clark,
                           "fournier": fournier, "harris_alternate_nnaji": harris_nnaji,
                           "teague_provisional_charge": teague},
                "states": {"before_both": before, "gordon_first_intermediate": gordon_first,
                           "fournier_first_intermediate": fournier_first, "after_both": after}}

    ordinary = amounts(False)
    adjusted = amounts(True)
    assert adjusted["states"]["after_both"] == (
        post["core_base_usd"] + post["all_disclosed_core_bonus_usd"]
        + post["previous_contract_budget_total_usd"])
    assert ordinary["states"]["after_both"] == adjusted["states"]["after_both"] - 3533333
    assert (adjusted["inputs"]["gordon_clark"], adjusted["inputs"]["fournier"],
            adjusted["inputs"]["harris_alternate_nnaji"]) == (21136364, 17450000, 23887527)

    def state(label):
        regular = ordinary["states"][label]
        apron_listed = adjusted["states"][label]
        return {"state": label,
                "ordinary_listed_usd": regular,
                "ordinary_tax_threshold_distance_usd": tax - regular,
                "adjusted_apron_listed_usd": apron_listed,
                "apron_distance_usd": apron - apron_listed,
                "with_full_annual_camp_stress_usd": apron_listed + camp,
                "apron_distance_after_camp_stress_usd": apron - apron_listed - camp}

    return {
        "stage": "O-15F14-AJ_ORLANDO_MARCH25_TRADE_ORDER_SCREEN",
        "classification": "CONDITIONAL_LISTED_COMMITMENT_SCREEN_NOT_LEAGUE_CLEARANCE",
        "date": "2021-03-25",
        "ordinary_listed_inputs_usd": ordinary["inputs"],
        "apron_adjusted_listed_inputs_usd": adjusted["inputs"],
        "full_annual_camp_stress_usd": camp,
        "thresholds_usd": {"tax": tax, "apron": apron},
        "states": [state(label) for label in ("before_both", "gordon_first_intermediate",
                                              "fournier_first_intermediate", "after_both")],
        "official_completion_order_verified": False,
        "actual_team_salary_usd": None,
        "actual_hard_cap_trigger_verified": False,
        "actual_trade_charge_verified": False,
        "apron_compliance": None,
        "trade_matching_compliance": None,
        "source_files": [path.relative_to(ROOT).as_posix() for path in (ORL, TERMS, POST)],
    }


if __name__ == "__main__":
    result = build()
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({row["state"]: row["apron_distance_after_camp_stress_usd"]
                      for row in result["states"]}))
