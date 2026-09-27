"""Bridge the author's F4/F5 choices to K1 results without rewriting K1."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json"
SEASON = ROOT / "simulation/CHICAGO_2020_21_SEASON_RECOMMENDATION.json"
SCREENS = (
    ROOT / "simulation/ORLANDO_2020_21_HALL_NO_RESIGN_SCREEN.json",
    ROOT / "simulation/DENVER_2020_21_MCGEE_NONTRADE_SCREEN.json",
)
ORLANDO_REGISTRATION = ROOT / "simulation/ORLANDO_2020_21_REGISTRATION_LEDGER.json"
ORLANDO_PAYROLL = ROOT / "simulation/ORLANDO_2020_21_PAYROLL_BOUND.json"
DENVER_PAYROLL = ROOT / "simulation/BOSTON_DENVER_2020_21_PAYROLL.json"
MCGEE_FUNDING = ROOT / "simulation/NBA_2021_EXECUTION_RESOLUTION.json"
APRON = 138_928_000


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build():
    decision = read(DECISION)
    assert decision["status"] == "AUTHOR_SELECTED_F4_F5_FOLLOWUP_DIRECTIONS_ONLY"
    assert "does not re-sign" in decision["selected"]["F4_HALL"]
    assert "do not execute" in decision["selected"]["F5_MCGEE"]
    season = read(SEASON)
    candidates = {c["method"]: c for c in season["season_candidates"]}
    rows = [r for path in SCREENS for r in read(path)["rows"]]
    assert len(rows) == 30 and len({r["event_id"] for r in rows}) == 30
    cle = [r for r in rows if r.get("team") == "CLE"]
    assert len(cle) == 14 and all(r["candidate_lineup_valid"] for r in cle)
    impacts = {}
    for method, candidate in candidates.items():
        winners = {g["event_id"]: g["winner"] for g in candidate["regular_season_games"]}
        assert len(winners) == 1080
        for row in rows:
            event_id = row["event_id"]
            home = event_id.split("_")[1]
            stress = next(x for x in row["rating_stress"] if x["method"] == method)
            original_direction = "HOME" if winners[event_id] == home else "AWAY"
            assert stress["original_direction"] == original_direction
            assert stress["candidate_direction"] == original_direction
            assert stress["candidate_direction"] != "UNRESOLVED"
        impacts[method] = {
            "checked_events": len(rows),
            "direction_changes": 0,
            "unresolved": 0,
            "conditional_team_wins_unchanged": candidate["team_wins"],
            "conditional_seeds_unchanged": candidate["seeds"],
        }
    registration = read(ORLANDO_REGISTRATION)
    selected_epochs = []
    for epoch in registration["epochs"]:
        standard = set(epoch["standard"])
        if epoch["date"] >= "2021-05-09":
            assert "Donta Hall" in standard
            standard.remove("Donta Hall")
        assert len(standard) <= 15 and len(epoch["two_way"]) <= 2
        selected_epochs.append({"date": epoch["date"], "standard": len(standard),
                                "two_way": len(epoch["two_way"]),
                                "extra_standard_slots_needed": max(0, len(standard) - 15)})
    orl = read(ORLANDO_PAYROLL)
    den = read(DENVER_PAYROLL)["teams"]["DEN"]
    hall = next(c for c in orl["short_contracts"] if c["id"] == "HALL_MAY09")
    assert hall["apron_budget_usd"] == 88_798
    den_core = {p["player"]: p for p in den["core_players"]}
    assert den_core["JaVale McGee"]["base_usd"] == 4_200_000
    funding = read(MCGEE_FUNDING)["mcgee_funding"]
    hart = int((funding["simple_175_allowance_usd"] - 100_000) / 1.75)
    assert hart == 1_620_564 and funding["incoming_test_usd"] == 4_200_000
    orl_selected_stress = orl["peak"]["with_camp_full_annual_stress_usd"] - hall["apron_budget_usd"]
    den_selected_stress = den["peak"]["with_camp_annual_stress_usd"] - 4_200_000 + hart
    assert all(c["standard"] <= 15 for c in den["dated_roster_counts"])
    return {
        "stage": "O-15F14-Q_SELECTED_F4_F5_K1_BRIDGE",
        "scope": "30 local regular-season substitutions against both K1 methods only",
        "author_followup_selected": True,
        "season_selected": False,
        "exact_execution_cleared": False,
        "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (DECISION, SEASON, *SCREENS, ORLANDO_REGISTRATION,
                                    ORLANDO_PAYROLL, DENVER_PAYROLL, MCGEE_FUNDING)},
        "events": [r["event_id"] for r in rows],
        "method_results": impacts,
        "orlando_selected_registration_epochs": selected_epochs,
        "denver_one_for_one_standard_slot_preserved": True,
        "cleveland_one_for_one_standard_slot_preserved": True,
        "cleveland_conditional_lineup_witnesses": len(cle),
        "listed_apron_stress_only": {
            "ORL": {"selected_usd": orl_selected_stress,
                    "residual_allowance_usd": APRON - orl_selected_stress},
            "DEN": {"selected_usd": den_selected_stress,
                    "residual_allowance_usd": APRON - den_selected_stress},
        },
        "limits": ["health and accumulated workload open", "Cleveland 14 lineups use conditional roles, including Osman as handler on April 11",
                   "playoffs and later roster choices open", "F1-F3 exact execution open",
                   "unlisted salary burden remains null", "Cleveland cap and roster audit not independently completed"],
    }


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2))
