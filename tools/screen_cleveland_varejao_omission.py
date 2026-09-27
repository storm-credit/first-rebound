"""C2-only Cleveland five-game minute/lineup/rating sensitivity; never adopts C2."""

import hashlib
import json
from datetime import date
from pathlib import Path

import build_chicago_2020_21_season_recommendation as k
import screen_denver_mcgee_nontrade as f5


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "simulation/NBA_2020_21_FINAL859_MINUTES.json"
F5_SCREEN = ROOT / "simulation/DENVER_2020_21_MCGEE_NONTRADE_SCREEN.json"
FULL_SEASON = ROOT / "simulation/NBA_2020_21_FULL_SEASON.json"
RATING_FILES = (k.j.f.bi.cc.BPM, k.j.f.bi.cc.paired.RAPTOR)
GAMES = k.j.bi.lb.sb.GAMES
OFFICIAL_SECONDS = {
    "2021-05-05_CLE_POR": 397,
    "2021-05-07_DAL_CLE": 277,
    "2021-05-09_CLE_DAL": 983,
    "2021-05-12_CLE_BOS": 192,
    "2021-05-14_WAS_CLE": 307,
}


def digest(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def screen():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    prior_f5 = json.loads(F5_SCREEN.read_text(encoding="utf-8"))
    league = json.loads(FULL_SEASON.read_text(encoding="utf-8"))
    assert league["stage"] == "O-15F14-F"
    league_games = {g["event_id"]: g for g in league["game_summary"]}
    old_by_event = {r["event_id"]: r for r in prior_f5["rows"] if r["team"] == "CLE"}
    schedule, _, _, _, _ = k.j.load()
    rating_maps = k.j.f.rating_maps()
    envelopes = k.j.cc.envelopes(rating_maps)
    cle_dates = sorted({g["date"] for g in schedule.values() if "CLE" in (g["home"], g["away"])})
    previous = {d: cle_dates[i - 1] if i else None for i, d in enumerate(cle_dates)}
    branches = {b["event_id"]: b for b in source["branches"]
                if b["event_id"] in OFFICIAL_SECONDS and b["team"] == "CLE"
                and b["profile"] == "OBSERVED_HELD"}
    assert set(branches) == set(OFFICIAL_SECONDS)
    rows = []
    for event_id, observed in OFFICIAL_SECONDS.items():
        b = branches[event_id]
        assert b["alternate_seconds"]["Anderson Varejao"] == observed
        hart = b["alternate_seconds"].get("Isaiah Hartenstein", 0)
        prior = old_by_event.get(event_id)
        assert (prior is None) == (hart == 0)
        if prior:
            assert prior["seconds"] == hart
        candidate = {p: sec for p, sec in b["alternate_seconds"].items()
                     if p not in ("Anderson Varejao", "Isaiah Hartenstein")}
        assert "JaVale McGee" not in candidate
        candidate["JaVale McGee"] = observed + hart
        assert sum(candidate.values()) == 5 * b["game_duration_seconds"]
        assert candidate["JaVale McGee"] <= b["game_duration_seconds"]
        assert "Anderson Varejao" not in b["starters"]
        assert "Isaiah Hartenstein" not in b["starters"]
        witness = f5.cleveland_lineup_witness(candidate, b["starters"], b["game_duration_seconds"])
        assert witness is not None
        game = schedule[event_id]
        sign = 1 if game["home"] == "CLE" else -1
        original_margin = game["margin"] if game["winner"] == game["home"] else -game["margin"]
        moved = {"Anderson Varejao": -observed, "JaVale McGee": observed + hart}
        if hart:
            moved["Isaiah Hartenstein"] = -hart
        stress = []
        for method in k.j.METHODS:
            delta, delta_terms = k.j.cc.form(moved, rating_maps[method], {})
            terms = {p: sign * coefficient for p, coefficient in delta_terms.items()}
            prev = previous[b["date"]]
            fatigue = 0.0
            if prev and (date.fromisoformat(b["date"]) - date.fromisoformat(prev)).days == 1:
                old_positive = sum(max(0, n) for n in b["delta_seconds"].values())
                new_delta = b["delta_seconds"].copy()
                for p, change in moved.items():
                    new_delta[p] = new_delta.get(p, 0) + change
                fatigue = -sign * .5 * (sum(max(0, n) for n in new_delta.values()) - old_positive) / 2880
            proposed = k.j.cc.band(original_margin + sign * delta + fatigue, terms, envelopes[method])
            prior_band = league_games[event_id]["method_bands"][method]
            # An interval sum deliberately retains unknown-rating uncertainty from both screens.
            # It is an outer bound, not a newly fitted season model.
            league_plus_c2 = [prior_band[0] + proposed[0] - original_margin,
                              prior_band[1] + proposed[1] - original_margin]
            assert f5.direction(league_plus_c2) == f5.direction(prior_band)
            stress.append({"method": method, "actual_home_margin": original_margin,
                           "candidate_home_band": proposed,
                           "f14f_home_band": prior_band,
                           "f14f_plus_c2_outer_band": [round(n, 8) for n in league_plus_c2],
                           "actual_direction": f5.direction([original_margin, original_margin]),
                           "candidate_direction": f5.direction(proposed),
                           "f14f_direction": f5.direction(prior_band),
                           "f14f_plus_c2_direction": f5.direction(league_plus_c2),
                           "fatigue_adjustment": fatigue,
                           "unrated_delta_players": sorted(delta_terms)})
        rows.append({"event_id": event_id, "varejao_removed_seconds": observed,
                     "hartenstein_removed_seconds": hart, "mcgee_candidate_seconds": observed + hart,
                     "lineup_witness_count": len(witness), "lineup_feasible_conditional": True,
                     "rating_stress": stress})
    assert sum(r["varejao_removed_seconds"] for r in rows) == 2156
    assert sum(r["mcgee_candidate_seconds"] for r in rows) == 3681
    return {"stage": "O-15F14_C2_CLEVELAND_VAREJAO_OMISSION_SCREEN", "selected": False,
            "scope": "five Cleveland regular-season games only; Varejao omission plus selected McGee/Hartenstein nontrade",
            "source_sha256": {str(p.relative_to(ROOT)): digest(p)
                              for p in (SOURCE, F5_SCREEN, FULL_SEASON, *RATING_FILES, GAMES)},
            "rows": rows, "limits": ["health and coaching choice not proved", "conditional role-only lineup witnesses",
                                  "F14F opponent inputs included by conservative interval addition only",
                                  "later K1 season inputs and all causal health changes still open",
                                  "rating direction is local, not final season", "C1 hardship path remains open",
                                  "registration, cap, subsequent transactions and playoff effects open"]}


if __name__ == "__main__":
    print(json.dumps(screen(), ensure_ascii=False, indent=2))
