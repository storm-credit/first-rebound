"""Bound the five selected Hall-free Orlando games by observed big-man loads.

This fixes other K1 minutes, keeps Bamba absent on May 11/13, and permits
Wagner's minimum residual above his observed minutes on those two dates.
Observed exposure is a comparison bound, not alternate-world medical approval.
"""

import json

import screen_orlando_hall_no_resign as hall


BIGS = ("Mo Bamba", "Moritz Wagner")


def screen():
    source = json.loads(hall.SOURCE.read_text(encoding="utf-8"))
    branches = {b["event_id"]: b for b in source["branches"]
                if b["team"] == "ORL" and b["date"] in hall.DATES
                and b["profile"] == "LOW_MINUTES"}
    assert len(branches) == 5
    overrides = {}
    lower_bounds = {}
    for event_id, branch in branches.items():
        caps = {p: branch["actual_seconds"][p] for p in BIGS
                if p in branch["alternate_seconds"] and p in branch["actual_seconds"]}
        if "Mo Bamba" not in branch["alternate_seconds"]:
            hall_seconds = branch["alternate_seconds"][hall.HALL]
            other_room = sum(hall.CAP_SECONDS[p] - branch["alternate_seconds"][p]
                             for p in ("Nikola Vucevic", "Zeke Nnaji"))
            residual = max(0, hall_seconds - other_room)
            caps["Moritz Wagner"] = max(caps["Moritz Wagner"],
                                          branch["alternate_seconds"]["Moritz Wagner"] + residual)
            lower_bounds[event_id] = residual
        overrides[event_id] = caps

    result = hall.screen(overrides)
    assert len(result["rows"]) == 5
    for row in result["rows"]:
        branch = branches[row["event_id"]]
        for p, cap in overrides[row["event_id"]].items():
            assert row["candidate_minutes"][p] <= cap + 1e-5
        if "Mo Bamba" in branch["actual_seconds"]:
            assert row["candidate_minutes"]["Mo Bamba"] == branch["actual_seconds"]["Mo Bamba"]
        assert abs(sum(w["seconds"] for w in row["lineup_witness"]) - 2880) < 1e-5
        assert all(s["candidate_direction"] == s["original_direction"]
                   for s in row["rating_stress"])
    for event_id, residual in lower_bounds.items():
        row = next(r for r in result["rows"] if r["event_id"] == event_id)
        branch = branches[event_id]
        assert abs(row["added_seconds"]["Moritz Wagner"] - residual) < 1e-5
        assert row["candidate_minutes"]["Nikola Vucevic"] == hall.CAP_SECONDS["Nikola Vucevic"]
        assert row["candidate_minutes"]["Zeke Nnaji"] == hall.CAP_SECONDS["Zeke Nnaji"]

    return {
        "stage": "O-15F14-F4_FIVE_GAME_OBSERVED_LOAD_BOUND",
        "selected": False,
        "comparison_scope": "Five May 9-16 Hall-free games; unchanged K1 other-player minutes",
        "model_caps_seconds": hall.CAP_SECONDS,
        "observed_or_residual_caps_seconds": overrides,
        "minimum_wagner_extra_on_bamba_absence_seconds": lower_bounds,
        "source_observation_sha256": source["observation_sha256"],
        "rows": result["rows"],
        "limits": "Original minutes do not establish counterfactual health, coaching, contract, or season outcomes",
    }


if __name__ == "__main__":
    print(json.dumps(screen(), ensure_ascii=False, indent=2))
