"""Aggregate G8G's dated reference pressure without canceling different games."""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "simulation/CHICAGO_2020_21_SHOT_OPPORTUNITY_PRESSURE.json"
OUTPUT = ROOT / "simulation/CHICAGO_2020_21_DAILY_SHOT_PRESSURE.json"


def build() -> dict:
    data = json.loads(SOURCE.read_text(encoding="utf-8"), parse_float=Decimal)
    assert data["stage"] == "O-15G8G" and len(data["games"]) == 29
    names = list(data["cases"])
    assert len(names) == 9
    games = data["games"]
    assert len({game["date"] for game in games}) == 29
    cases = {}
    for name in names:
        dated = [(game["date"], game["pressure_by_case"][name]) for game in games]
        positives = [(date, value) for date, value in dated if value > 0]
        negatives = [(date, value) for date, value in dated if value < 0]
        assert len(positives) == data["cases"][name]["positive_games"]
        assert len(negatives) == data["cases"][name]["negative_games"]
        gross_excess = sum((value for _, value in positives), Decimal(0))
        gross_shortfall = -sum((value for _, value in negatives), Decimal(0))
        net = gross_excess - gross_shortfall
        assert abs(net - data["cases"][name]["pressure"]) < Decimal("0.00002")
        max_date, max_value = max(dated, key=lambda item: item[1])
        min_date, min_value = min(dated, key=lambda item: item[1])
        cases[name] = {
            "positive_games": len(positives),
            "negative_games": len(negatives),
            "gross_positive_pressure": float(gross_excess.quantize(Decimal("0.000001"))),
            "gross_negative_magnitude": float(gross_shortfall.quantize(Decimal("0.000001"))),
            "net_pressure_from_dated_values": float(net.quantize(Decimal("0.000001"))),
            "largest_positive": {"date": max_date, "pressure": float(max_value)},
            "largest_negative": {"date": min_date, "pressure": float(min_value)},
        }
    universally_positive = [game["date"] for game in games if all(game["pressure_by_case"][name] > 0 for name in names)]
    universally_negative = [game["date"] for game in games if all(game["pressure_by_case"][name] < 0 for name in names)]
    assert not set(universally_positive) & set(universally_negative)
    return {
        "stage": "O-15G8H",
        "status": "DATED_REFERENCE_PRESSURE_ONLY_NOT_ALTERNATE_POSSESSIONS",
        "source_file": SOURCE.name,
        "source_sha256_lf": hashlib.sha256(SOURCE.read_bytes().replace(b"\r\n", b"\n")).hexdigest(),
        "reference_policy": "Hypothetically hold each actual-history game FGA+0.44FTA fixed; sum positive pressure by date without intergame offset. This is not an NBA rule or alternate-game possession cap.",
        "games": len(games),
        "universally_positive_dates": universally_positive,
        "universally_negative_dates": universally_negative,
        "sign_varies_by_case_dates": [game["date"] for game in games if game["date"] not in set(universally_positive + universally_negative)],
        "cases": cases,
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
        assert json.loads(OUTPUT.read_text(encoding="utf-8")) == result
        print("PASS: 29 dated pressures, 9 cases, non-canceling totals and source hash")


if __name__ == "__main__":
    main()
