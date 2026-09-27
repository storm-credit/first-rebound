"""Reproduce the conditional K1/F038 + L2 first-round bracket.

This is a structural audit, not a selected season or a simulated series result.
"""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "simulation" / "CHICAGO_2020_21_K1_L2_BRACKET.json"
PAIRINGS = ((1, 8), (2, 7), (3, 6), (4, 5))


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def qualifiers(games, regular_seeds):
    assert len(games) == 3
    assert (games[0]["home"], games[0]["away"]) == tuple(regular_seeds[6:8])
    assert (games[1]["home"], games[1]["away"]) == tuple(regular_seeds[8:10])
    for game in games:
        assert game["winner"] in (game["home"], game["away"])
    loser_78 = next(team for team in regular_seeds[6:8] if team != games[0]["winner"])
    assert {games[2]["home"], games[2]["away"]} == {loser_78, games[1]["winner"]}
    return [games[0]["winner"], games[2]["winner"]]


def build():
    season = read("simulation/NBA_2020_21_FULL_SEASON.json")
    closeout = read("simulation/CHICAGO_2020_21_EXECUTION_CLOSEOUT.json")
    case = next(c for c in season["league_cases"] if c["id"] == "F038")
    proposal = next(p for p in closeout["postseason_proposals"] if p["id"] == "L2")
    assert not case["selected"] and not proposal["selected"]
    assert proposal["recommended"]
    bracket = {}
    for conference, name in (("EAST", "east"), ("WEST", "west")):
        regular = case["seeds"][conference]
        final_two = qualifiers(proposal[f"{name}_games"], regular)
        assert final_two == proposal[f"{name}_qualifiers"]
        final_seeds = regular[:6] + final_two
        assert len(set(final_seeds)) == 8
        bracket[name] = {
            "final_seeds": final_seeds,
            "first_round": [
                {"higher_seed": high, "higher_team": final_seeds[high - 1],
                 "lower_seed": low, "lower_team": final_seeds[low - 1]}
                for high, low in PAIRINGS
            ],
        }
    assert {team for conf in bracket.values() for team in conf["final_seeds"]} == set(proposal["playoff_teams"])
    assert bracket["west"]["first_round"][2]["higher_team"] == "DEN"
    assert bracket["west"]["first_round"][2]["lower_team"] == "LAL"
    return {
        "status": "CONDITIONAL_BRACKET_ONLY_NOT_SELECTED",
        "source_case": "F038",
        "source_proposal": "L2",
        "nba_rule": "2021 play-in winner 7/8 gets seed 7; final winner gets seed 8; first round 1-8, 2-7, 3-6, 4-5",
        "conferences": bracket,
        "historical_denver_portland_phoenix_games": "COMPARATOR_ONLY_NOT_K1_L2_EXECUTION",
        "series_winners_or_dates_selected": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = json.dumps(build(), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        assert OUTPUT.read_text(encoding="utf-8") == content
        print("K1/L2 bracket source and artifact: PASS")
    else:
        OUTPUT.write_text(content, encoding="utf-8")
        print(OUTPUT)
