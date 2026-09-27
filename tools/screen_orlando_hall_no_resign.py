"""Screen a Hall-free May 9-16 Orlando rotation without changing the K ledger.

This is a feasibility witness for an unapproved counterfactual, not a game or
contract selection. It reuses K's LOW minutes, player roles, and lineup rules.
"""

import itertools
import json
from datetime import date
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

import build_chicago_2020_21_season_recommendation as k


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "simulation/NBA_2020_21_FINAL859_MINUTES.json"
REGISTRATION = ROOT / "simulation/ORLANDO_2020_21_REGISTRATION_LEDGER.json"
HALL = "Donta Hall"
DATES = {"2021-05-09", "2021-05-11", "2021-05-13", "2021-05-14", "2021-05-16"}
CAP_SECONDS = {
    "Nikola Vucevic": 36 * 60,
    "Moritz Wagner": 36 * 60,
    "Mo Bamba": 30 * 60,
    "Zeke Nnaji": 16 * 60,
}
WEIGHTS = {"Nikola Vucevic": 4, "Moritz Wagner": 2, "Mo Bamba": 2, "Zeke Nnaji": 3}


def screen():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    registration = json.loads(REGISTRATION.read_text(encoding="utf-8"))
    expected = {r["event_id"] for r in registration["orl_game_checks"]
                if r["extra_standard_slots_needed"] == 1}
    assert expected == {b["event_id"] for b in source["branches"]
                        if b["team"] == "ORL" and b["date"] in DATES
                        and b["profile"] == "LOW_MINUTES"}
    assert all(len(set(epoch["standard"]) - {HALL}) == 15
               and len(epoch["two_way"]) == 2
               for epoch in registration["epochs"] if epoch["date"] >= "2021-05-09")
    schedule, _, _, inputs, _ = k.j.load()
    rating_maps = k.j.f.rating_maps()
    envelopes = k.j.cc.envelopes(rating_maps)
    rival_ratings = json.loads(k.j.i.h.g.OUT.read_text())["rival_candidates"][0]["methods"]
    orlando_dates = sorted({g["date"] for g in schedule.values()
                            if "ORL" in (g["home"], g["away"])})
    previous_date = {day: orlando_dates[i - 1] if i else None
                     for i, day in enumerate(orlando_dates)}
    branches = [b for b in source["branches"] if b["team"] == "ORL"
                and b["date"] in DATES and b["profile"] == "LOW_MINUTES"]
    assert len(branches) == 5
    rows = []
    for branch in sorted(branches, key=lambda b: b["date"]):
        prior = branch["alternate_seconds"]
        players = sorted(p for p, seconds in prior.items() if p != HALL and seconds > 0)
        assert HALL in prior and HALL not in branch["starters"]
        roles = k.j.roles_for(branch)
        combos = [list(c) for c in itertools.combinations(players, 5)
                  if k.j.bi.valid(c, "ORL", {"ORL": roles})]
        assert branch["starters"] in combos
        duration = branch["game_duration_seconds"]
        additions = sorted(set(players) & CAP_SECONDS.keys())
        fixed = sorted(set(players) - set(additions))
        equal = [[int(p in c) for c in combos] for p in fixed]
        equal.append([1] * len(combos))
        targets = [prior[p] for p in fixed] + [duration]
        bounds = [(180 if c == branch["starters"] else 0, None) for c in combos]
        upper, limits = [], []
        for p in additions:
            line = np.array([int(p in c) for c in combos])
            upper.extend((line, -line))
            limits.extend((CAP_SECONDS[p], -prior[p]))
        objective = [100 * max(0, len(set(c) & k.BIGS) - 2)
                     + sum(WEIGHTS.get(p, 0) for p in c) for c in combos]
        solved = linprog(objective, A_eq=equal, b_eq=targets,
                         A_ub=upper, b_ub=limits, bounds=bounds, method="highs")
        assert solved.success, (branch["event_id"], solved.message)
        witness = [{"players": c, "seconds": float(value)} for c, value in zip(combos, solved.x)
                   if value > 1e-7]
        minutes = {p: float(sum(w["seconds"] for w in witness if p in w["players"]))
                   for p in players}
        assert abs(sum(minutes.values()) - 5 * duration) < 1e-5
        assert all(abs(minutes[p] - prior[p]) < 1e-5 for p in fixed)
        assert all(prior[p] - 1e-5 <= minutes[p] <= CAP_SECONDS[p] + 1e-5
                   for p in additions)
        assert abs(sum(minutes[p] - prior[p] for p in additions) - prior[HALL]) < 1e-5
        assert sum(w["seconds"] for w in witness if w["players"] == branch["starters"]) >= 180
        moved = {HALL: -prior[HALL]}
        moved.update({p: minutes[p] - prior[p] for p in additions
                      if minutes[p] - prior[p] > 1e-5})
        stress = []
        for method in k.j.METHODS:
            baseline = inputs[branch["event_id"], "LOW_MINUTES", method]
            base_terms = baseline["unknown_coefficients"].copy()
            base_constant = (baseline["home_margin_constant"]
                             + base_terms.pop(k.j.f.e.RIVAL, 0)
                             * rival_ratings[method]["effective_rating"])
            change_constant, change_terms = k.j.cc.form(moved, rating_maps[method], {})
            sign = 1 if schedule[branch["event_id"]]["home"] == "ORL" else -1
            fatigue_change = 0.0
            prev = previous_date[branch["date"]]
            if prev and (date.fromisoformat(branch["date"]) - date.fromisoformat(prev)).days == 1:
                old_positive = sum(max(0, n) for n in branch["delta_seconds"].values())
                new_delta = branch["delta_seconds"].copy()
                for p, change in moved.items():
                    new_delta[p] = new_delta.get(p, 0) + change
                new_positive = sum(max(0, n) for n in new_delta.values())
                fatigue_change = -sign * .5 * (new_positive - old_positive) / 2880
            new_terms = base_terms.copy()
            for p, coefficient in change_terms.items():
                new_terms[p] = new_terms.get(p, 0) + sign * coefficient
            original_band = k.j.cc.band(base_constant, base_terms, envelopes[method])
            candidate_band = k.j.cc.band(base_constant + sign * change_constant + fatigue_change,
                                          new_terms, envelopes[method])
            classify = lambda band: "HOME" if band[0] > 0 else "AWAY" if band[1] < 0 else "UNRESOLVED"
            stress.append({"method": method, "original_home_band": original_band,
                           "candidate_home_band": candidate_band,
                           "original_direction": classify(original_band),
                           "candidate_direction": classify(candidate_band),
                           "fatigue_adjustment": fatigue_change,
                           "unrated_delta_players": sorted(change_terms)})
        assert all(row["original_direction"] == row["candidate_direction"] for row in stress)
        rows.append({"event_id": branch["event_id"], "removed_hall_seconds": prior[HALL],
                     "added_seconds": {p: minutes[p] - prior[p] for p in additions
                                       if minutes[p] - prior[p] > 1e-5},
                     "candidate_minutes": minutes, "lineup_witness": witness,
                     "rating_stress": stress})
    return {"stage": "O-15F14-F4_HALL_NO_RESIGN_SCREEN", "selected": False,
            "scope": "Five May 9-16 Orlando games only; no new injury or league approval assumed",
            "player_caps_seconds": CAP_SECONDS, "rows": rows}


if __name__ == "__main__":
    result = screen()
    print(json.dumps(result, ensure_ascii=False, indent=2))
