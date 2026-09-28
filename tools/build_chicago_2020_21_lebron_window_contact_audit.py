"""Map the historical LeBron ankle calendar to existing conditional game ledgers.

This checks coverage and the saved model's historical-availability baseline. It
does not simulate an alternate medical history or certify a playoff bracket.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulation"
BASELINE = SIM / "NBA_2020_21_REGULAR_GAME_BASELINE.csv"
LEDGERS = {
    "F038_FINAL859": SIM / "NBA_2020_21_FULL_SEASON.json",
    "REMAINING_PAIRED": SIM / "CHICAGO_2020_21_REMAINING_PAIRED_IMPACT.json",
    "BOUNDARY_PAIRED": SIM / "CHICAGO_2020_21_BOUNDARY_PAIRED_IMPACT.json",
}
OUTPUT = SIM / "CHICAGO_2020_21_LEBRON_WINDOW_CONTACT_AUDIT.json"
METHODS = ("RAPTOR_RS_EB", "BPM_MAR25_EB")
PHASES = (
    ("INITIAL_ABSENCE", "2021-03-21", "2021-04-28", 20, 8),
    ("FIRST_RETURN", "2021-04-30", "2021-05-02", 2, 0),
    ("SECOND_ABSENCE", "2021-05-03", "2021-05-12", 6, 4),
    ("FINAL_RETURN", "2021-05-15", "2021-05-16", 2, 2),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ledgers = {name: json.loads(path.read_text(encoding="utf-8")) for name, path in LEDGERS.items()}
    index: dict[str, tuple[str, dict]] = {}
    for name, ledger in ledgers.items():
        for summary in ledger["game_summary"]:
            event_id = summary["event_id"]
            if event_id in index:
                raise ValueError(f"duplicate game summary: {event_id}")
            index[event_id] = name, summary

    f038 = next(case for case in ledgers["F038_FINAL859"]["league_cases"] if case["id"] == "F038")
    changed = set(f038["changed_game_ids"])
    rows = []
    with BASELINE.open(encoding="utf-8-sig", newline="") as handle:
        for game in csv.DictReader(handle):
            if "LAL" not in (game["home"], game["away"]):
                continue
            date = game["date"]
            phase = next((label for label, start, end, _, _ in PHASES if start <= date <= end), None)
            if date == "2021-03-20":
                phase = "PARTIAL_GAME_INCIDENT"
            if phase is None:
                continue
            event_id = f"{date}_{game['home']}_{game['away']}"
            source, summary = index[event_id]
            if summary["status"] != "ALL_TESTED_RETAIN":
                raise ValueError(f"unretained baseline: {event_id}")
            sign = 1 if game["home"] == "LAL" else -1
            margin = (int(game["home_score"]) - int(game["away_score"])) * sign
            if margin == 0:
                raise ValueError(f"drawn NBA game: {event_id}")
            bands = {}
            for method in METHODS:
                lo, hi = summary["method_bands"][method]
                band = [lo, hi] if sign == 1 else [-hi, -lo]
                if band[0] > band[1] or (margin > 0 and band[0] <= 0) or (margin < 0 and band[1] >= 0):
                    raise ValueError(f"conditional winner mismatch: {event_id} {method} {band}")
                bands[method] = band
            rows.append({
                "event_id": event_id,
                "phase": phase,
                "opponent": game["away"] if sign == 1 else game["home"],
                "historical_lakers_margin": margin,
                "historical_lakers_result": "W" if margin > 0 else "L",
                "ledger": source,
                "conditional_lakers_margin_bands": bands,
                "changed_in_f038": event_id in changed,
                "also_in_davis_30_game_absence_window": "2021-02-16" <= date <= "2021-04-19",
            })

    rows.sort(key=lambda row: row["event_id"])
    phase_summary = {}
    for label, _, _, expected_games, expected_wins in PHASES:
        group = [row for row in rows if row["phase"] == label]
        wins = sum(row["historical_lakers_result"] == "W" for row in group)
        if len(group) != expected_games or wins != expected_wins:
            raise ValueError(f"historical phase mismatch: {label}, games={len(group)}, wins={wins}")
        phase_summary[label] = {
            "games": len(group),
            "historical_wins": wins,
            "historical_losses": len(group) - wins,
            "game_ledgers": dict(sorted(Counter(row["ledger"] for row in group).items())),
            "losses_within_five_points": [row["event_id"] for row in group if -5 <= row["historical_lakers_margin"] < 0],
        }

    incident = [row for row in rows if row["phase"] == "PARTIAL_GAME_INCIDENT"]
    if len(incident) != 1 or incident[0]["historical_lakers_margin"] != -5:
        raise ValueError("March 20 partial-game incident mismatch")
    initial_overlap = sum(row["also_in_davis_30_game_absence_window"] for row in rows if row["phase"] == "INITIAL_ABSENCE")
    if initial_overlap != 16 or sum(row["changed_in_f038"] for row in rows) != 0:
        raise ValueError("Davis overlap or F038 changed-game mismatch")

    output = {
        "stage": "O-15F14-BB",
        "status": "HISTORICAL_20_PLUS_6_CALENDAR_RECONCILED / ALT_HEALTH_HOLD",
        "official_sources": {
            "march20_contact": "https://www.nba.com/news/lebron-james-leaves-lakers-game-with-right-ankle-injury-will-not-return",
            "march20_final_box": "https://statsdmz.nba.com/pdfs/20210320/20210320_ATLLAL.pdf",
            "april30_first_return_after_20": "https://www.nba.com/news/report-lebron-james-may-return-tonight-vs-kings",
            "may2_ankle_soreness": "https://www.nba.com/game/0022000974",
            "may15_return_after_6": "https://www.nba.com/watch/video/20210515gametimelakers",
            "may16_final_box": "https://www.nba.com/game/lal-vs-nop-0022001072/box-score",
        },
        "summary": {
            "march20_partial_game": incident[0]["event_id"],
            "phases": phase_summary,
            "first_absence_games_overlapping_davis_absence": initial_overlap,
            "march20_also_davis_absent": incident[0]["also_in_davis_30_game_absence_window"],
            "total_unique_games_including_partial_incident": len(rows),
            "all_tested_retain": len(rows),
            "f038_changed_games": 0,
        },
        "rows": rows,
        "input_sha256": {str(path.relative_to(ROOT)): sha256(path) for path in (BASELINE, *LEDGERS.values())},
        "selected": False,
        "health_calendar_author_locked": False,
        "manuscript_allowed": False,
    }
    if len(rows) != 31:
        raise ValueError(f"unexpected unique games: {len(rows)}")
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: 20+6 absence games, 4 return games, 1 partial incident; Davis overlap {initial_overlap}")


if __name__ == "__main__":
    main()
