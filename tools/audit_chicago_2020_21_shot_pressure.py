"""Audit conditional shooting-opportunity pressure; never create alternate box scores."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulation"
LINEUPS = SIM / "CHICAGO_2020_21_POSTDEADLINE_LINEUP_AUDIT.json"
PRIORS = SIM / "CHICAGO_2020_21_POSTDEADLINE_OBSERVED_PRIORS.csv"
BOX = SIM / "CHICAGO_2020_21_POSTDEADLINE_BOTH_TEAMS_ACTUAL.csv"
DESIGN = SIM / "CHICAGO_2020_21_PREDEADLINE_PRODUCTION_PRIORS.csv"
OUTPUT = SIM / "CHICAGO_2020_21_SHOT_OPPORTUNITY_PRESSURE.json"
NEW_PLAYERS = ("Protagonist", "LaMelo Ball")
MARK = "Lauri Markkanen"
FT_WEIGHT = 0.44


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def number(row: dict[str, str], key: str) -> int:
    return int(row[key] or 0)


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def rounded(value: float) -> float:
    return round(value, 6)


def build() -> dict:
    records = json.loads(LINEUPS.read_text(encoding="utf-8"))
    games = [game for game in records["games"] if game["scenario"] == "PORTER_ZERO"]
    assert len(games) == 29 and len({game["date"] for game in games}) == 29
    assert all(game["minimum_change_candidate"]["status"] == "CONDITIONAL_CERTIFICATE_PASS" for game in games)

    observed = {row["player"]: row for row in read_csv(PRIORS)}
    design = {(row["player"], row["scenario"]): row for row in read_csv(DESIGN)}
    chi_box: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(BOX):
        if row["team"] == "CHI":
            chi_box[row["date"]].append(row)
    assert set(chi_box) == {game["date"] for game in games}
    assert all(len({row["game_id"] for row in rows}) == 1 for rows in chi_box.values())

    mark_post = [row for rows in chi_box.values() for row in rows if row["player"] == MARK]
    assert sum(number(row, "seconds") > 0 for row in mark_post) == 28
    pre_seconds = number(observed[MARK], "seconds")
    post_seconds = sum(number(row, "seconds") for row in mark_post)
    assert pre_seconds == 41429 and post_seconds == 37617
    post_fga = sum(number(row, "fga") for row in mark_post)
    post_fta = sum(number(row, "fta") for row in mark_post)
    assert (number(observed[MARK], "fga"), number(observed[MARK], "fta")) == (303, 61)
    assert (post_fga, post_fta) == (218, 31)

    mark_rates = {
        "POST_HINDSIGHT": (post_fga / post_seconds, post_fta / post_seconds),
        "MID_HINDSIGHT": (
            (post_fga / post_seconds + number(observed[MARK], "fga") / pre_seconds) / 2,
            (post_fta / post_seconds + number(observed[MARK], "fta") / pre_seconds) / 2,
        ),
        "PRE_CUTOFF": (number(observed[MARK], "fga") / pre_seconds, number(observed[MARK], "fta") / pre_seconds),
    }
    scenario_names = ("LOW", "BASE", "HIGH")
    case_ids = [f"{mark}_{scenario}" for mark in mark_rates for scenario in scenario_names]
    totals = {
        case_id: {"incumbent_fga": 0.0, "incumbent_fta": 0.0, "new_pts": 0.0,
                  "new_shooting_equivalents": 0.0, "new_three_pa_floor": 0.0,
                  "pressure": 0.0, "positive_games": 0, "negative_games": 0}
        for case_id in case_ids
    }
    output_games = []
    limited = set()
    mark_k1_seconds = 0.0
    reference_fga = reference_fta = 0

    for game in sorted(games, key=lambda item: item["date"]):
        date = game["date"]
        seconds = game["minimum_change_candidate"]["player_seconds"]
        assert abs(sum(seconds.values()) - 14400) < 0.001, date
        assert all(player in seconds for player in NEW_PLAYERS), date
        mark_seconds = seconds.get(MARK, 0.0)
        mark_k1_seconds += mark_seconds
        rows = chi_box[date]
        fga = sum(number(row, "fga") for row in rows)
        fta = sum(number(row, "fta") for row in rows)
        reference_fga += fga
        reference_fta += fta
        reference_shooting = fga + FT_WEIGHT * fta

        incumbent_fga = incumbent_fta = 0.0
        for player, played_seconds in seconds.items():
            if player in (*NEW_PLAYERS, MARK):
                continue
            assert player in observed and number(observed[player], "seconds") > 0, (date, player)
            if observed[player]["sample_status"] != "OBSERVED_NOT_CAUSAL":
                limited.add(player)
            incumbent_fga += played_seconds * number(observed[player], "fga") / number(observed[player], "seconds")
            incumbent_fta += played_seconds * number(observed[player], "fta") / number(observed[player], "seconds")

        game_cases = {}
        for mark_name, (mark_fga_rate, mark_fta_rate) in mark_rates.items():
            with_mark_fga = incumbent_fga + mark_seconds * mark_fga_rate
            with_mark_fta = incumbent_fta + mark_seconds * mark_fta_rate
            for scenario in scenario_names:
                case_id = f"{mark_name}_{scenario}"
                new_pts = new_shooting = new_three_pa = 0.0
                for player in NEW_PLAYERS:
                    row = design[(player, scenario)]
                    pts = float(row["pts36"]) * seconds[player] / 2160
                    new_pts += pts
                    new_shooting += pts / (2 * float(row["ts"]))
                    new_three_pa += float(row["three_pa36"]) * seconds[player] / 2160
                pressure = with_mark_fga + FT_WEIGHT * with_mark_fta + new_shooting - reference_shooting
                result = totals[case_id]
                for key, value in (("incumbent_fga", with_mark_fga), ("incumbent_fta", with_mark_fta),
                                   ("new_pts", new_pts), ("new_shooting_equivalents", new_shooting),
                                   ("new_three_pa_floor", new_three_pa), ("pressure", pressure)):
                    result[key] += value
                result["positive_games" if pressure > 0 else "negative_games"] += 1
                game_cases[case_id] = rounded(pressure)

        output_games.append({"date": date, "event_id": rows[0]["event_id"],
                             "reference_fga": fga, "reference_fta": fta,
                             "mark_k1_seconds": rounded(mark_seconds),
                             "pressure_by_case": game_cases})

    assert abs(mark_k1_seconds - 36899) < 0.001
    assert (reference_fga, reference_fta) == (2558, 451)
    reference_shooting = reference_fga + FT_WEIGHT * reference_fta
    for result in totals.values():
        assert result["positive_games"] + result["negative_games"] == 29
        expected = result["incumbent_fga"] + FT_WEIGHT * result["incumbent_fta"] + result["new_shooting_equivalents"] - reference_shooting
        assert abs(result["pressure"] - expected) < 1e-6
        for key in ("incumbent_fga", "incumbent_fta", "new_pts", "new_shooting_equivalents", "new_three_pa_floor", "pressure"):
            result[key] = rounded(result[key])

    return {
        "stage": "O-15G8G",
        "status": "CONDITIONAL_SHOOTING_PRESSURE_NOT_ALTERNATE_BOX",
        "source_sha256_lf": {path.name: normalized_sha256(path) for path in (LINEUPS, PRIORS, BOX, DESIGN)},
        "policy": {"k1_minutes": "PORTER_ZERO minimum_change_candidate",
                   "incumbents": "2021-03-24 observed FGA/FTA per second, not causal",
                   "new_players": "existing LOW/BASE/HIGH pts36 and TS; FGA/FTA split unknown",
                   "mark_post_and_mid": "hindsight sensitivity only; unavailable at cutoff",
                   "weight": FT_WEIGHT,
                   "pressure_definition": "model FGA + 0.44*FTA shooting equivalents minus actual-history CHI total; not possessions or a hard alternate cap"},
        "reference": {"games": 29, "team_fga": reference_fga, "team_fta": reference_fta,
                      "shooting_equivalents": rounded(reference_shooting),
                      "mark_actual_post_fga": post_fga, "mark_actual_post_fta": post_fta},
        "limited_incumbent_priors": sorted(limited),
        "mark_k1_seconds": rounded(mark_k1_seconds),
        "cases": totals,
        "games": output_games,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    if args.write:
        OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"WROTE {OUTPUT}")
    else:
        assert OUTPUT.exists() and json.loads(OUTPUT.read_text(encoding="utf-8")) == result
        print("PASS: 29 games, 9 conditional cases, source hashes and arithmetic match")


if __name__ == "__main__":
    main()
