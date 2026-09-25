"""Reproduce a pre-opening Suggs sensitivity and two conditional ORL minute witnesses.

No score, win, player contract, medical clearance, or season execution is selected.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
from statistics import median

import build_chicago_2021_22_paired as g14


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "research/O15G15B_COMPARATOR_INPUTS.json"
G14 = ROOT / "simulation/CHICAGO_2021_22_PAIRED_REVIEW.json"
G14_INPUT = ROOT / "simulation/CHICAGO_2021_22_PAIRED_INPUTS.json"
G14_PRIORS = ROOT / "simulation/CHICAGO_2021_22_OPPONENT_PRIORS.json"
OUTPUT = ROOT / "simulation/CHICAGO_2021_22_G15B_STRESS.json"
POSITIONS = ("PG", "SG", "SF", "PF", "C")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def witness(case, context):
    by_player, by_position = Counter(), {p: Counter() for p in POSITIONS}
    guards = set(case["designated_primary_guards"])
    unavailable = set(context["unavailable_if_historical_reasons_retained"])
    assert len(guards) == 2 and "Cole Anthony" in guards
    assert len(case["lineups"]) == 4
    assert sum(block["minutes"] for block in case["lineups"]) == 48
    for block in case["lineups"]:
        assert block["minutes"] == 12
        positions = block["positions"]
        assert set(positions) == set(POSITIONS) and len(set(positions.values())) == 5
        assert positions["PG"] in guards
        assert not set(positions.values()) & unavailable
        assert not set(positions.values()) & {"Franz Wagner", "Jalen Suggs", "RJ Hampton", "Wendell Carter Jr."}
        for position, player in positions.items():
            by_player[player] += block["minutes"]
            by_position[position][player] += block["minutes"]
    assert sum(by_player.values()) == 240
    assert max(by_player.values()) <= context["minute_ceiling_design_only"]
    assert all(sum(v.values()) == 48 for v in by_position.values())
    assert by_position["PG"]["Cole Anthony"] == 36
    assert sum(n for p, n in by_position["PG"].items() if p != "Cole Anthony") == 12
    return {
        "id": case["id"], "status": case["status"], "total_minutes": 240,
        "blocks": len(case["lineups"]), "player_minutes": dict(sorted(by_player.items())),
        "position_minutes": {p: dict(sorted(v.items())) for p, v in by_position.items()},
        "registration_cleared": False, "medical_cleared": False,
        "performance_cleared": False, "actual_substitution_order": None,
    }


def det_budget_stress(source, ratios):
    """Reuse G14's policy math, but keep every result in a separate stress artifact."""
    config, priors, prior = load(G14_INPUT), load(G14_PRIORS), load(G14)
    rotation = next(r for r in config["rotations"] if r["id"] == "DET_0022100004")
    assert rotation["status"] == "CONDITIONAL"
    cert = g14.certify(rotation)
    assert cert["player_minutes"]["Jalen Suggs"] == 24
    budget = next(r["player_box_totals"] for r in prior["historical"]
                  if r["game_id"] == rotation["game_id"] and r["team"] == "DET")
    assert {k: budget[k] for k in ("fga", "fta", "tov")} == {"fga": 90, "fta": 13, "tov": 16}
    rates = {name: g14.rate_from_totals(p) for name, p in priors["priors"].items()}
    assert set(cert["player_minutes"]) - set(rates) == {"Jalen Suggs"}
    cases = []
    college = source["suggs"]["college"]
    for comparator in source["comparators"]:
        name = comparator["name"]
        rate = {k: college[k] * 36 / college["minutes"] * ratios[name][k]
                for k in source["metrics"]}
        assert 0 <= rate["fg3a"] <= rate["fga"]
        rates["Jalen Suggs"] = rate
        for policy in config["policies"]:
            result, rows = g14.allocate(rotation, cert, rates, budget, policy,
                                        config["stress_ratio_design_only"])
            case = {"comparator": name, "policy": policy["id"], "status": result["status"]}
            if rows:
                suggs = next(r for r in rows if r["player"] == "Jalen Suggs")
                case.update(raw_totals=result["raw_totals"],
                            budget=result["budget"],
                            protected_players=result["protected_players"],
                            adjustment_ratio_suggs={k: suggs[f"ratio_{k}"] for k in ("fga", "fta", "tov")},
                            allocated_suggs={k: suggs[f"allocated_{k}"] for k in ("fga", "fta", "tov")},
                            stress_player_count=result["stress_player_count"])
            else:
                case["hold_reason"] = result
            cases.append(case)
    assert len(cases) == 12
    return cases


def build():
    source, prior = load(INPUT), load(G14)
    assert source["opening_information_cutoff"] == "2021-10-19"
    assert prior["orlando_guard_hold"]["conditional_missing_guard_minutes"] == 12
    assert prior["team_policy_counts"] == {"CONDITIONAL_NUMERIC": 16, "PRIOR_HOLD": 4, "ROLE_HOLD": 4}
    metrics = source["metrics"]
    assert metrics == ["fga", "fg3a", "fta", "tov"]
    assert source["suggs"]["college_season"] == "2020-21"
    assert source["suggs"]["conditional_det_minutes"] == 24
    ratios = {}
    for comp in source["comparators"]:
        assert comp["college_season"] == "2019-20" and comp["nba_rookie_season"] == "2020-21"
        college, nba = comp["college"], comp["nba"]
        assert college["minutes"] > 0 and nba["minutes"] > 0
        assert all(college[k] > 0 and nba[k] >= 0 for k in metrics)
        assert college["fg3a"] <= college["fga"] and nba["fg3a"] <= nba["fga"]
        ratios[comp["name"]] = {k: (nba[k] / nba["minutes"]) / (college[k] / college["minutes"])
                                for k in metrics}
    assert len(ratios) == 3
    candidates = {}
    for k in metrics:
        values = [rates[k] for rates in ratios.values()]
        college_24 = source["suggs"]["college"][k] * 24 / source["suggs"]["college"]["minutes"]
        candidates[k] = {"college_24_unadjusted": college_24,
                         "observed_ratio_min": min(values), "observed_ratio_median": median(values),
                         "observed_ratio_max": max(values),
                         "stress_min": college_24 * min(values),
                         "stress_median": college_24 * median(values),
                         "stress_max": college_24 * max(values)}
    assert candidates["fg3a"]["stress_max"] < candidates["fga"]["stress_min"]
    context = source["orlando"]
    assert context["game_id"] == prior["orlando_guard_hold"]["game_id"]
    assert not any(context["guardrails"].values())
    cases = [witness(case, context) for case in context["witnesses"]]
    assert {c["id"] for c in cases} == {"O15A_HERBERT_INTERNAL", "O15C_GRAVETT_CONTRACT"}
    return {
        "stage": source["stage"], "status": "SENSITIVITY_AND_MINUTE_WITNESSES_ONLY_NOT_SEASON_EXECUTION",
        "cutoff": source["opening_information_cutoff"],
        "comparator_ratios": ratios, "suggs_24_min_stress": candidates,
        "det_g14_policy_stress_not_adopted": det_budget_stress(source, ratios),
        "orlando_witnesses": cases, "g14_original_counts_unchanged": prior["team_policy_counts"],
        "new_g14_numeric_policy_rows": 0, "actual_score_or_wins": None,
        "author_locked": False, "season_selected": False,
        "exact_execution_cleared": False, "manuscript_allowed": False,
        "limitations": [
            "Three selected historical guards are not a representative predictive sample.",
            "Metric-wise medians combine different players and do not constitute a coherent joint outcome.",
            "College/NBA pace, team role, injury, and opponent effects are not identified.",
            "G14 prior/role HOLDs remain until calibration and alternate registration are audited.",
            "Lineup blocks are a capacity proof, not an actual substitution, contract, medical, or performance claim.",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(build(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert OUTPUT.read_text(encoding="utf-8") == rendered
        print("G15B reproduced; G14 HOLD and gates unchanged")
    else:
        OUTPUT.write_text(rendered, encoding="utf-8")
        print(OUTPUT)
