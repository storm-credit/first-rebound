"""Audit one-game seed sensitivity around the conditional K1/F038 + L2 bracket.

The scenarios change only one historical game's winner. They are standings
stress tests, not a health forecast or a selected counterfactual result.
"""

import argparse
import csv
import json
from pathlib import Path

from build_chicago_2020_21_k1_l2_bracket import PAIRINGS, qualifiers, read


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "simulation" / "CHICAGO_2020_21_K1_L2_SEED_SENSITIVITY.json"
SCENARIOS = (
    (
        "F038_L2_BASE",
        None,
        {},
    ),
    (
        "APR15_LAL_BOS_FLIP_ONLY",
        "2021-04-15_LAL_BOS",
        {"BOS": -1, "LAL": 1},
    ),
    (
        "FEB14_DEN_LAL_FLIP_ONLY",
        "2021-02-14_DEN_LAL",
        {"DEN": -1, "LAL": 1},
    ),
)


def davis_absence_window(observed, changed_game_ids):
    rows = [
        (event, row) for event, row in observed.items()
        if "2021-02-14" < row["date"] < "2021-04-22"
        and "LAL" in (row["home"], row["away"])
    ]
    rows.sort(key=lambda item: item[0])
    assert len(rows) == 30
    assert not {event for event, _ in rows} & set(changed_game_ids)
    games = []
    for event, row in rows:
        home_margin = int(row["home_score"]) - int(row["away_score"])
        lakers_margin = home_margin if row["home"] == "LAL" else -home_margin
        games.append({
            "event_id": event,
            "date": row["date"],
            "opponent": row["away"] if row["home"] == "LAL" else row["home"],
            "lakers_margin": lakers_margin,
        })
    wins = sum(game["lakers_margin"] > 0 for game in games)
    losses = [game for game in games if game["lakers_margin"] < 0]
    assert (wins, len(losses)) == (14, 16)
    before = [game for game in games if game["date"] < "2021-03-20"]
    on = [game for game in games if game["date"] == "2021-03-20"]
    after = [game for game in games if game["date"] > "2021-03-20"]
    assert (len(before), len(on), len(after)) == (13, 1, 16)
    assert (sum(game["lakers_margin"] > 0 for game in before),
            sum(game["lakers_margin"] > 0 for game in after)) == (7, 7)
    assert on[0]["opponent"] == "ATL" and on[0]["lakers_margin"] == -5
    return {
        "status": "HISTORICAL_SCHEDULE_ONLY_NOT_ALTERNATE_HEALTH",
        "first_absent_game": games[0]["event_id"],
        "last_absent_game": games[-1]["event_id"],
        "games": len(games),
        "lakers_wins": wins,
        "lakers_losses": len(losses),
        "f038_changed_game_ids_in_window": [],
        "before_march20_james_injury": {"games": 13, "wins": 7, "losses": 6},
        "march20_atl_james_injury_game": on[0],
        "after_march20_james_injury": {"games": 16, "wins": 7, "losses": 9},
        "original_losses": losses,
    }


def build():
    season = read("simulation/NBA_2020_21_FULL_SEASON.json")
    closeout = read("simulation/CHICAGO_2020_21_EXECUTION_CLOSEOUT.json")
    with (ROOT / "simulation" / "NBA_2020_21_REGULAR_GAME_BASELINE.csv").open(
        encoding="utf-8", newline=""
    ) as source:
        observed = {
            f"{row['date']}_{row['home']}_{row['away']}": row
            for row in csv.DictReader(source)
        }
    summaries = {item["event_id"]: item for item in season["game_summary"]}
    case = next(item for item in season["league_cases"] if item["id"] == "F038")
    proposal = next(item for item in closeout["postseason_proposals"] if item["id"] == "L2")
    assert not case["selected"] and not proposal["selected"]
    assert proposal["recommended"]
    assert not {item[1] for item in SCENARIOS if item[1]} & set(case["changed_game_ids"])
    results = []
    for name, event, deltas in SCENARIOS:
        assert sum(deltas.values()) == 0
        original_game = None
        if event:
            assert event in observed and event in summaries, (name, event)
            assert summaries[event]["status"] == "ALL_TESTED_RETAIN"
            row = observed[event]
            home_score, away_score = int(row["home_score"]), int(row["away_score"])
            assert home_score != away_score
            winner, loser = (
                (row["home"], row["away"])
                if home_score > away_score else (row["away"], row["home"])
            )
            assert deltas == {winner: -1, loser: 1}, (name, deltas, row)
            original_game = {
                "home": row["home"], "away": row["away"],
                "home_score": home_score, "away_score": away_score,
            }
        wins = case["team_wins"] | {
            team: case["team_wins"][team] + delta for team, delta in deltas.items()
        }
        conferences = {}
        for key, label in (("EAST", "east"), ("WEST", "west")):
            original = case["seeds"][key]
            order = {team: index for index, team in enumerate(original)}
            changed = set(deltas) & set(original)
            # A newly tied changed team needs an explicit NBA tiebreak audit.
            for team in changed:
                assert all(
                    wins[team] != wins[other]
                    for other in original if other != team
                ), (name, team, "new tie requires separate tiebreak")
            regular = sorted(original, key=lambda team: (-wins[team], order[team]))
            if not deltas:
                assert regular == original
            assert regular[6:10] == original[6:10], (name, label, "play-in field changed")
            qualified = qualifiers(proposal[f"{label}_games"], regular)
            assert qualified == proposal[f"{label}_qualifiers"]
            final = regular[:6] + qualified
            conferences[label] = {
                "regular_top10": [{"team": team, "wins": wins[team]} for team in regular[:10]],
                "first_round": [
                    {
                        "higher_seed": higher,
                        "higher_team": final[higher - 1],
                        "lower_seed": lower,
                        "lower_team": final[lower - 1],
                    }
                    for higher, lower in PAIRINGS
                ],
            }
        west = conferences["west"]["first_round"]
        denver_pair = next(pair for pair in west if "DEN" in (pair["higher_team"], pair["lower_team"]))
        other_pair = west[1] if denver_pair is west[2] else west[0]
        assert denver_pair is west[2] or denver_pair is west[3]
        results.append({
            "id": name,
            "flipped_game": event,
            "original_game": original_game,
            "win_deltas": deltas,
            "conferences": conferences,
            "denver_first_round": denver_pair,
            "denver_possible_second_round_from": other_pair,
        })
    assert [
        (item["denver_first_round"]["higher_seed"], item["denver_first_round"]["lower_team"])
        for item in results
    ] == [(3, "LAL"), (3, "DAL"), (4, "LAL")]
    assert [(item["denver_possible_second_round_from"]["higher_team"],
             item["denver_possible_second_round_from"]["lower_team"])
            for item in results] == [("PHX", "POR"), ("PHX", "POR"), ("UTA", "MEM")]
    return {
        "status": "STRUCTURAL_STRESS_ONLY_NOT_SELECTED",
        "source_season_case": "F038",
        "source_playin_proposal": "L2",
        "historical_davis_absence_window": davis_absence_window(observed, case["changed_game_ids"]),
        "scope": "one game winner reversed, all other F038/L2 results held fixed",
        "tie_policy": "original F038 order retained only for unchanged win ties; no newly tied changed team allowed",
        "health_or_coaching_inferred": False,
        "series_winner_selected": False,
        "scenarios": results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = json.dumps(build(), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        assert OUTPUT.read_text(encoding="utf-8") == content
        print("K1/L2 one-game seed sensitivity: PASS")
    else:
        OUTPUT.write_text(content, encoding="utf-8")
        print(OUTPUT)
