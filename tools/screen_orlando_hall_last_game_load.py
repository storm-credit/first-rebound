"""Test an F4 last-game rotation capped at Bamba/Wagner's observed minutes.

The caps are a sensitivity test, not a claim of medical clearance or a selected
counterfactual lineup. Other four Hall-free games retain the existing screen.
"""

import json

import screen_orlando_hall_no_resign as hall


EVENT = "2021-05-16_PHI_ORL"
PLAYERS = ("Mo Bamba", "Moritz Wagner")


def screen():
    source = json.loads(hall.SOURCE.read_text(encoding="utf-8"))
    branch = next(b for b in source["branches"]
                  if b["event_id"] == EVENT and b["profile"] == "LOW_MINUTES")
    observed_caps = {p: branch["actual_seconds"][p] for p in PLAYERS}
    assert observed_caps == {"Mo Bamba": 1375, "Moritz Wagner": 2078}

    baseline = json.loads((hall.ROOT / "simulation/ORLANDO_2020_21_HALL_NO_RESIGN_SCREEN.json")
                          .read_text(encoding="utf-8"))
    old = next(r for r in baseline["rows"] if r["event_id"] == EVENT)
    revised = next(r for r in hall.screen({EVENT: observed_caps})["rows"]
                   if r["event_id"] == EVENT)
    assert revised["candidate_minutes"]["Mo Bamba"] == observed_caps["Mo Bamba"]
    assert revised["candidate_minutes"]["Moritz Wagner"] == observed_caps["Moritz Wagner"]
    assert abs(sum(revised["added_seconds"].values()) - revised["removed_hall_seconds"]) < 1e-5
    assert all(r["original_direction"] == r["candidate_direction"]
               for r in revised["rating_stress"])

    return {
        "stage": "O-15F14-F4_LAST_GAME_LOAD_SENSITIVITY",
        "selected": False,
        "event_id": EVENT,
        "observed_caps_seconds": observed_caps,
        "comparison_scope": "May 16 alone; other four games remain in the prior F4 screen",
        "baseline_candidate_minutes": {p: old["candidate_minutes"][p]
                                       for p in hall.CAP_SECONDS},
        "candidate": revised,
        "limits": "Actual minutes are exposure evidence, not alternate-world health approval",
    }


if __name__ == "__main__":
    print(json.dumps(screen(), ensure_ascii=False, indent=2))
