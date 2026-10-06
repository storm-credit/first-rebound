"""Join 1080 existing K1 symbolic margins and the selected J1 replacement.

Returns working expressions; does not select unknown ratings or certify health,
registration, financial execution, final scores, or a completed season.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import build_chicago_2020_21_availability_policy as j

ROOT = Path(__file__).resolve().parents[1]
PROFILE = "LOW_MINUTES"
METHOD = "BPM_MAR25_EB"
AVAILABILITY = "PORTER_ZERO"
SOURCES = [
    "canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json",
    "simulation/CHICAGO_2020_21_SEASON_RECOMMENDATION.json",
    "simulation/CHICAGO_2020_21_AUTHOR_PACKET.json",
    "simulation/CHICAGO_2020_21_AVAILABILITY_POLICY.json",
    "simulation/CHICAGO_2020_21_POLICY_REPLACEMENT_MINUTES.json",
    "simulation/NBA_2020_21_FULL_SEASON.json",
    "simulation/CHICAGO_2020_21_BOUNDARY_PAIRED_IMPACT.json",
    "simulation/CHICAGO_2020_21_REMAINING_PAIRED_IMPACT.json",
    "simulation/NBA_2020_21_FINAL_CLOSE_PAIRED_IMPACT.json",
    "simulation/NBA_2020_21_FINAL859_IMPACT.csv",
    "simulation/CHICAGO_2020_21_IMPACT_CROSSCHECK.json",
    "simulation/CHICAGO_2020_21_INTEGRATED_PATHS.json",
    "simulation/CHICAGO_2020_21_CLOSE_GAME_PATHS.json",
    "simulation/CHICAGO_2020_21_BPM_MAR25_SNAPSHOT.csv",
    "simulation/CHICAGO_2020_21_POSTDEADLINE_RAPTOR_RS.csv",
    "tools/build_chicago_2020_21_availability_policy.py",
    "tools/build_chicago_2020_21_integrated_paths.py",
    "tools/crosscheck_chicago_2020_21_impact.py",
    "tools/audit_2020_21_selected_margin_join.py",
]


def read(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def source_hash(path: str) -> str:
    text = (ROOT / path).read_bytes().decode("utf-8-sig")
    return hashlib.sha256(text.replace("\r\n", "\n").replace("\r", "\n").encode()).hexdigest()


def evaluated_band(constant: float, terms: dict, rating: float, envelope: dict) -> list:
    rival = j.f.e.RIVAL
    return j.cc.band(constant + terms.get(rival, 0) * rating,
                     {p: n for p, n in terms.items() if p != rival}, envelope)


def winner_for(band: list, game: dict) -> str | None:
    return game["home"] if band[0] > 0 else game["away"] if band[1] < 0 else None


def build() -> dict:
    schedule, _raw, _branches, inputs, origins = j.load()
    nonchi = {gid: r for (gid, profile, method), r in inputs.items()
              if (profile, method) == (PROFILE, METHOD)}
    chi = j.chi_inputs(PROFILE, METHOD, AVAILABILITY)
    assert len(schedule) == 1080 and len(nonchi) == 1008 and len(chi) == 72
    assert all("CHI" not in (schedule[g]["home"], schedule[g]["away"]) for g in nonchi)
    full = read("simulation/NBA_2020_21_FULL_SEASON.json")
    bridge = full["season_bridge"][114]
    assert bridge["source_condition"] == {
        "path_id": "LOW_MINUTES/RIVAL_28/FOURNIER_PATH_RETAINED",
        "availability": AVAILABILITY, "method": METHOD, "prior": "BASE",
        "fatigue": .5, "rating_open_interval": [-3.1967555, 7.33255543]}
    case = next(r for r in full["league_cases"] if r["id"] == "F038")
    assert 114 in case["bridge_indices"]
    rec = read("simulation/CHICAGO_2020_21_SEASON_RECOMMENDATION.json")
    primary = next(r for r in rec["season_candidates"] if r["role"] == "PRIMARY_RECOMMENDATION")
    assert (primary["policy"], primary["profile"], primary["method"],
            primary["availability"], primary["base_case_id"], primary["fatigue"]) == (
                "J1_TERRY_LEAVE", PROFILE, METHOD, AVAILABILITY, "F038", .5)
    rating = read("simulation/CHICAGO_2020_21_AUTHOR_PACKET.json")["rival_candidates"][0]["methods"][METHOD]["effective_rating"]
    assert rating == primary["rival_effective_rating"]
    assert bridge["shared_rival_rating_open_interval"][0] < rating < bridge["shared_rival_rating_open_interval"][1]
    envelope = j.cc.envelopes(j.f.rating_maps())[METHOD]
    impacts = [r for r in read("simulation/CHICAGO_2020_21_AVAILABILITY_POLICY.json")["impacts"]
               if (r["policy"], r["profile"], r["method"], r["availability"]) == (
                   "J1_TERRY_LEAVE", PROFILE, METHOD, AVAILABILITY)]
    j1 = {r["event_id"]: r for r in impacts}
    assert len(j1) == len(impacts) == 27
    primary_winners = {r["event_id"]: r["winner"] for r in primary["regular_season_games"]}
    assert len(primary_winners) == 1080
    changed = set(case["changed_game_ids"])
    rows = []
    for event, game in sorted(schedule.items()):
        ischi = "CHI" in (game["home"], game["away"])
        if ischi:
            r = chi[game["date"]]
            sign = 1 if game["home"] == "CHI" else -1
            constant = sign * r["constant"]
            terms = {p: sign * n for p, n in r.get("other_unknown_coefficients", {}).items()}
            if r["coefficient"]:
                terms[j.f.e.RIVAL] = sign * r["coefficient"]
            source = {"path": "tools/build_chicago_2020_21_integrated_paths.py",
                      "function": "season_games", "date": game["date"],
                      "phase": r["phase"], "branch": r["branch"], "home_sign": sign,
                      "prior": "BASE", "fatigue": .5,
                      "input_paths": ["simulation/CHICAGO_2020_21_IMPACT_CROSSCHECK.json",
                                      "simulation/CHICAGO_2020_21_INTEGRATED_PATHS.json",
                                      "simulation/CHICAGO_2020_21_CLOSE_GAME_PATHS.json"]}
        else:
            r = nonchi[event]
            assert float(r["fatigue"]) == .5
            assert r.get("status") != "CAPACITY_HOLD"
            constant = r["home_margin_constant"]
            terms = r["unknown_coefficients"].copy()
            source = {"function": "availability.load.inputs", "event_id": event,
                      "profile": PROFILE, "method": METHOD, "fatigue": .5,
                      "rival_minutes": r.get("rival_minutes"),
                      "team_branch_origins": {team: origins[event, team, PROFILE]
                                              for team in (game["home"], game["away"])},
                      "paired_input_pointer": f"event_id={event};profile={PROFILE};method={METHOD};fatigue=0.5"}
        baseconstant, baseterms = constant, terms.copy()
        baseband = evaluated_band(constant, terms, rating, envelope)
        basewinner = winner_for(baseband, game)
        expectedbase = (game["away"] if game["winner"] == game["home"] else game["home"]) if event in changed else game["winner"]
        assert basewinner == expectedbase, (event, "base F038 mismatch", baseband, basewinner, expectedbase)
        j1source = None
        if event in j1:
            replacement = j1[event]
            assert replacement["status"] == "CONDITIONAL_IMPACT"
            assert all(abs(x-y) < 1e-7 for x, y in zip(baseband, replacement["control_home_margin_band"]))
            # Replace the common symbolic expression once; never add a fully
            # computed replacement margin to the original margin.
            constant = replacement["home_margin_constant"]
            terms = replacement["unknown_coefficients"].copy()
            j1source = {"path": "simulation/CHICAGO_2020_21_AVAILABILITY_POLICY.json",
                        "pointer": f"impacts[event_id={event};J1_TERRY_LEAVE;LOW_MINUTES;BPM_MAR25_EB;PORTER_ZERO]"}
        band = evaluated_band(constant, terms, rating, envelope)
        winner = winner_for(band, game)
        assert winner == primary_winners[event], (event, "K1 J1 mismatch", band, winner, primary_winners[event])
        rows.append({"event_id": event, "date": game["date"], "home": game["home"], "away": game["away"],
                     "home_margin_constant": constant, "unknown_coefficients": terms,
                     "home_margin_band": band, "winner": winner,
                     "base_home_margin_constant": baseconstant, "base_unknown_coefficients": baseterms,
                     "base_home_margin_band": baseband, "base_winner": basewinner,
                     "j1_applied": event in j1, "source": source, "j1_source": j1source})
    assert len(rows) == 1080 and sum(r["j1_applied"] for r in rows) == 27
    wins = Counter(r["winner"] for r in rows)
    assert dict(wins) == primary["team_wins"]
    return {"stage": "K1_SELECTED_MARGIN_JOIN_AUDIT", "status": "1080_BASE_AND_J1_SYMBOLIC_EXPRESSIONS_REPRODUCED",
            "policy": {"base_case_id": "F038", "profile": PROFILE, "method": METHOD,
                       "availability": AVAILABILITY, "prior": "BASE", "fatigue": .5,
                       "rival_role": "R1", "rival_minutes": 28, "rival_effective_rating": rating},
            "envelope": envelope, "rows": rows,
            "summary": {"games": 1080, "non_chicago": 1008, "chicago": 72, "j1_replacements": 27,
                        "base_f038_winner_mismatches": 0, "j1_primary_winner_mismatches": 0,
                        "unresolved": 0, "wins_chicago": wins["CHI"], "wins_minnesota": wins["MIN"]},
            "source_hash_method": "SHA256_UTF8_LF_NORMALIZED",
            "source_sha256": {p: source_hash(p) for p in SOURCES},
            "limits": ["BPM before March25 uses future information; retrospective model only.",
                       "Empirical missing-rating envelope is conditional stress, not an actual ability certificate.",
                       "J1 is applied exactly once. F4/F5/C2 and other approved overlays are not applied here.",
                       "Chicago fatigue keeps the upstream Chicago-only policy; other games use the existing two-team policy.",
                       "Expressions are margin models, not exact scores or individual boxes."],
            "legal_execution_cleared": False, "medical_facts_certified": False,
            "season_selected": False, "manuscript_allowed": False}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    print(json.dumps(result["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
