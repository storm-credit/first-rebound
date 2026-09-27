"""Local 2021 McGee nontrade sensitivity; never changes the K1 ledger."""

import json
import itertools
from datetime import date
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

import build_chicago_2020_21_season_recommendation as k


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "simulation/NBA_2020_21_FINAL859_MINUTES.json"
DEN_OUT, DEN_IN = "JaVale McGee", "Isaiah Hartenstein"
CLE_ROLES = {
    "handler": {"Darius Garland", "Collin Sexton", "Matthew Dellavedova", "Damyean Dotson", "Jeremiah Martin", "Cedi Osman"},
    "center": {"JaVale McGee", "Jarrett Allen", "Anderson Varejao", "Mfiondu Kabengele", "Kevin Love", "Dean Wade"},
    "wing": {"Isaac Okoro", "Cedi Osman", "Taurean Prince", "Lamar Stevens", "Brodric Thomas", "Larry Nance Jr.", "Damyean Dotson", "Dean Wade", "Kevin Love"},
}


def direction(band):
    return "HOME" if band[0] > 0 else "AWAY" if band[1] < 0 else "UNRESOLVED"


def cleveland_lineup_witness(candidate, starters, duration):
    players = sorted(candidate)
    assert set(players) <= set().union(*CLE_ROLES.values())
    lineups = [list(combo) for combo in itertools.combinations(players, 5)
               if all(set(combo) & role for role in CLE_ROLES.values())]
    start = sorted(starters)
    assert start in lineups
    matrix = np.array([[int(p in lineup) for lineup in lineups] for p in players] +
                      [[1] * len(lineups)], dtype=float)
    target = [candidate[p] for p in players] + [duration]
    result = linprog(np.zeros(len(lineups)), A_eq=matrix, b_eq=target,
                     bounds=[(180 if lineup == start else 0, None) for lineup in lineups],
                     method="highs")
    if not result.success:
        return None
    witness = [{"players": lineup, "seconds": round(float(value), 8)}
               for lineup, value in zip(lineups, result.x) if value > 1e-6]
    assert all(abs(sum(w["seconds"] for w in witness if p in w["players"]) - candidate[p]) < 1e-5
               for p in players)
    assert abs(sum(w["seconds"] for w in witness) - duration) < 1e-5
    return witness


def screen():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    schedule, _, _, inputs, _ = k.j.load()
    rating_maps = k.j.f.rating_maps()
    envelopes = k.j.cc.envelopes(rating_maps)
    rival_ratings = json.loads(k.j.i.h.g.OUT.read_text(encoding="utf-8"))["rival_candidates"][0]["methods"]
    dates = {team: sorted({g["date"] for g in schedule.values()
                           if team in (g["home"], g["away"])}) for team in ("DEN", "CLE")}
    prior_date = {team: {d: days[i - 1] if i else None for i, d in enumerate(days)}
                  for team, days in dates.items()}
    selected = [b for b in source["branches"] if b["date"] >= "2021-03-25"
                and ((b["team"] == "DEN" and b["profile"] == "LOW_MINUTES"
                      and b["alternate_seconds"].get(DEN_OUT, 0) > 0)
                     or (b["team"] == "CLE" and b["profile"] == "OBSERVED_HELD"
                         and b["alternate_seconds"].get(DEN_IN, 0) > 0))]
    assert sum(b["team"] == "DEN" for b in selected) == 11
    assert sum(b["team"] == "CLE" for b in selected) == 14
    rows = []
    for b in sorted(selected, key=lambda x: (x["date"], x["team"])):
        old, new = (DEN_OUT, DEN_IN) if b["team"] == "DEN" else (DEN_IN, DEN_OUT)
        seconds = b["alternate_seconds"][old]
        assert b["alternate_seconds"].get(new, 0) == 0
        assert seconds <= 36 * 60
        candidate = b["alternate_seconds"].copy()
        candidate.pop(old)
        candidate[new] = seconds
        assert abs(sum(candidate.values()) - 5 * b["game_duration_seconds"]) < 1e-5
        new_starters = [new if p == old else p for p in b["starters"]]
        assert len(set(new_starters)) == 5
        lineup = b.get("lineup_witness")
        lineup_valid = None
        if lineup:
            roles = k.j.roles_for(b)
            lineup_valid = all(k.j.bi.valid([new if p == old else p for p in w["players"]],
                                               b["team"], {b["team"]: roles}) for w in lineup)
            assert lineup_valid
            assert abs(sum(w["seconds"] for w in lineup) - b["game_duration_seconds"]) < 1e-5
        elif b["team"] == "CLE":
            lineup = cleveland_lineup_witness(candidate, new_starters, b["game_duration_seconds"])
            lineup_valid = lineup is not None
        game = schedule[b["event_id"]]
        sign = 1 if game["home"] == b["team"] else -1
        moved = {old: -seconds, new: seconds}
        stress = []
        for method in k.j.METHODS:
            if b["team"] == "DEN":
                baseline = inputs[b["event_id"], b["profile"], method]
                terms = baseline["unknown_coefficients"].copy()
                constant = baseline["home_margin_constant"] + terms.pop(k.j.f.e.RIVAL, 0) * rival_ratings[method]["effective_rating"]
            else:
                terms = {}
                constant = game["margin"] if game["winner"] == game["home"] else -game["margin"]
            delta, delta_terms = k.j.cc.form(moved, rating_maps[method], {})
            for p, coefficient in delta_terms.items():
                terms[p] = terms.get(p, 0) + sign * coefficient
            prev = prior_date[b["team"]][b["date"]]
            fatigue = 0.0
            if prev and (date.fromisoformat(b["date"]) - date.fromisoformat(prev)).days == 1:
                old_positive = sum(max(0, n) for n in b["delta_seconds"].values())
                new_delta = b["delta_seconds"].copy()
                for p, change in moved.items():
                    new_delta[p] = new_delta.get(p, 0) + change
                fatigue = -sign * .5 * (sum(max(0, n) for n in new_delta.values()) - old_positive) / 2880
            original_terms = baseline["unknown_coefficients"].copy() if b["team"] == "DEN" else {}
            if b["team"] == "DEN":
                original_terms.pop(k.j.f.e.RIVAL, None)
            original = k.j.cc.band(constant, original_terms, envelopes[method])
            proposed = k.j.cc.band(constant + sign * delta + fatigue, terms, envelopes[method])
            stress.append({"method": method, "original_home_band": original,
                           "candidate_home_band": proposed,
                           "original_direction": direction(original),
                           "candidate_direction": direction(proposed),
                           "fatigue_adjustment": fatigue,
                           "unrated_delta_players": sorted(delta_terms)})
        rows.append({"event_id": b["event_id"], "team": b["team"], "removed": old,
                     "added": new, "seconds": seconds, "candidate_starters": new_starters,
                     "candidate_lineup_valid": lineup_valid,
                     "candidate_lineup_witness": lineup if b["team"] == "CLE" else None,
                     "rating_stress": stress})
    return {"stage": "O-15F14_F5_MCGEE_NONTRADE_SCREEN", "selected": False,
            "scope": "25 played game rows only; CLE 5-man proof uses conditional roles, not observed coaching; registration, health, playoffs and pick chain not cleared",
            "cleveland_conditional_roles": {role: sorted(players) for role, players in CLE_ROLES.items()},
            "rows": rows}


if __name__ == "__main__":
    print(json.dumps(screen(), ensure_ascii=False, indent=2))
