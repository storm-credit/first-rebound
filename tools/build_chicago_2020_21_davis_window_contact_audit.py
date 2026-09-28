"""Reconcile the historical Davis absence window with three conditional game ledgers."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "simulation/NBA_2020_21_REGULAR_GAME_BASELINE.csv"
LEDGERS = {
    "F038_FINAL859": ROOT / "simulation/NBA_2020_21_FULL_SEASON.json",
    "REMAINING_PAIRED": ROOT / "simulation/CHICAGO_2020_21_REMAINING_PAIRED_IMPACT.json",
    "BOUNDARY_PAIRED": ROOT / "simulation/CHICAGO_2020_21_BOUNDARY_PAIRED_IMPACT.json",
}
OUTPUT = ROOT / "simulation/CHICAGO_2020_21_DAVIS_WINDOW_CONTACT_AUDIT.json"
METHODS = ("RAPTOR_RS_EB", "BPM_MAR25_EB")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ledgers = {name: json.loads(path.read_text(encoding="utf-8")) for name, path in LEDGERS.items()}
    index: dict[str, tuple[str, dict]] = {}
    for name, ledger in ledgers.items():
        for game in ledger["game_summary"]:
            event_id = game["event_id"]
            if event_id in index:
                raise ValueError(f"duplicate game summary: {event_id}")
            index[event_id] = (name, game)

    f038 = next(case for case in ledgers["F038_FINAL859"]["league_cases"] if case["id"] == "F038")
    changed = set(f038["changed_game_ids"])
    rows = []
    with BASELINE.open(encoding="utf-8-sig", newline="") as handle:
        for game in csv.DictReader(handle):
            date = game["date"]
            if not ("2021-02-16" <= date <= "2021-04-19") or "LAL" not in (game["home"], game["away"]):
                continue
            event_id = f"{date}_{game['home']}_{game['away']}"
            source, summary = index[event_id]
            if summary["status"] != "ALL_TESTED_RETAIN":
                raise ValueError(f"window game not retained: {event_id}")
            home_margin = int(game["home_score"]) - int(game["away_score"])
            lakers_sign = 1 if game["home"] == "LAL" else -1
            lakers_margin = home_margin * lakers_sign
            if lakers_margin == 0:
                raise ValueError(f"drawn NBA game: {event_id}")
            lakers_bands = {}
            for method in METHODS:
                lo, hi = summary["method_bands"][method]
                band = [lo, hi] if lakers_sign == 1 else [-hi, -lo]
                if not (band[0] <= band[1]):
                    raise ValueError(f"reversed band: {event_id}, {method}")
                if lakers_margin > 0 and band[0] <= 0 or lakers_margin < 0 and band[1] >= 0:
                    raise ValueError(f"method changes original winner: {event_id}, {method}, {band}")
                lakers_bands[method] = band
            rows.append(
                {
                    "event_id": event_id,
                    "opponent": game["away"] if lakers_sign == 1 else game["home"],
                    "historical_lakers_margin": lakers_margin,
                    "historical_lakers_result": "W" if lakers_margin > 0 else "L",
                    "ledger": source,
                    "conditional_lakers_margin_bands": lakers_bands,
                    "changed_in_f038": event_id in changed,
                }
            )

    rows.sort(key=lambda row: row["event_id"])
    source_counts = Counter(row["ledger"] for row in rows)
    wins = sum(row["historical_lakers_result"] == "W" for row in rows)
    close_losses = [row["event_id"] for row in rows if -5 <= row["historical_lakers_margin"] < 0]
    close_wins = [row["event_id"] for row in rows if 0 < row["historical_lakers_margin"] <= 5]
    if len(rows) != 30 or wins != 14 or len(rows) - wins != 16:
        raise ValueError("NBA-reported 30-game, 14-16 historical absence window mismatch")
    if source_counts != Counter({"F038_FINAL859": 26, "REMAINING_PAIRED": 3, "BOUNDARY_PAIRED": 1}):
        raise ValueError(f"unexpected ledger coverage: {source_counts}")
    if any(row["changed_in_f038"] for row in rows):
        raise ValueError("F038 changed a game in the historical Davis absence window")

    output = {
        "stage": "O-15F14-AZ",
        "status": "HISTORICAL_WINDOW_RECONCILED / ALTERNATE_HEALTH_HOLD",
        "historical_window": ["2021-02-16", "2021-04-19"],
        "official_sources": {
            "davis_30_game_return": "https://www.nba.com/news/lakers-anthony-davis-ends-30-game-injury-absence-against-mavs",
            "lebron_separate_march20_event": "https://www.nba.com/news/lebron-james-leaves-lakers-game-with-right-ankle-injury-will-not-return",
        },
        "summary": {
            "games": len(rows),
            "historical_wins": wins,
            "historical_losses": len(rows) - wins,
            "game_ledgers": dict(sorted(source_counts.items())),
            "f038_changed_games": 0,
            "historical_losses_within_five_points": close_losses,
            "historical_wins_within_five_points": close_wins,
        },
        "rows": rows,
        "input_sha256": {str(path.relative_to(ROOT)): sha256(path) for path in (BASELINE, *LEDGERS.values())},
        "selected": False,
        "health_calendar_author_locked": False,
        "manuscript_allowed": False,
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(rows)} games, {wins}-{len(rows)-wins}, {dict(source_counts)}")


if __name__ == "__main__":
    main()
