"""Check source-labelled DEN/LAL opening minute templates without selecting a series."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "simulation" / "CHICAGO_2020_21_DEN_LAL_OPENING_MINUTE_TEMPLATES.json"


def seconds(value: str) -> int:
    minutes, second = map(int, value.split(":"))
    assert 0 <= second < 60 and minutes >= 0, value
    return 60 * minutes + second


def main() -> None:
    record = json.loads(PATH.read_text(encoding="utf-8"))
    assert record["status"] == "HISTORICAL_TEAM_MINUTES_COMPARATOR_ONLY"
    assert record["selected"] is False
    for team in ("denver_home", "lakers_away"):
        template = record["historical_templates"][team]
        assert sum(map(seconds, template["played"].values())) == 240 * 60, team
        assert not (set(template["played"]) & set(template["historical_dnp"])), team
        assert not (set(template["played"]) & set(template["historical_inactive"])), team
    denver = record["historical_templates"]["denver_home"]
    lakers = record["historical_templates"]["lakers_away"]
    assert set(record["alternate_denver_name_level_check"]["absent_after_author_locked_transactions"]) == {
        "JaVale McGee", "Zeke Nnaji"
    }
    assert not set(denver["played"]) & {"JaVale McGee", "Zeke Nnaji"}
    assert lakers["played"]["Talen Horton-Tucker"] == "07:05"
    assert "Marc Gasol" in lakers["historical_dnp"]
    assert "Marc Gasol" not in lakers["played"]
    assert record["cross_team_five_man_timeline_verified"] is False
    assert record["matchup_specific_shots_possessions_or_score_verified"] is False
    assert record["series_winner_or_length_selected"] is False
    assert record["alternate_denver_or_lakers_minutes_selected"] is False
    print("PASS: separate DEN/LAL historical 240-minute comparators; no alternate minutes selected")


if __name__ == "__main__":
    main()
