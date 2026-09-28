"""Join Davis and LeBron historical Lakers windows for an A1 choice packet.

The output is a minimum regular-season recheck set, not a counterfactual
medical forecast or an alternate NBA schedule.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulation"
DAVIS = SIM / "CHICAGO_2020_21_DAVIS_WINDOW_CONTACT_AUDIT.json"
LEBRON = SIM / "CHICAGO_2020_21_LEBRON_WINDOW_CONTACT_AUDIT.json"
OUTPUT = SIM / "CHICAGO_2020_21_DUAL_HEALTH_EXPOSURE.json"
BASELINE = SIM / "NBA_2020_21_REGULAR_GAME_BASELINE.csv"
DAVIS_INCIDENT = "2021-02-14_DEN_LAL"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    davis = json.loads(DAVIS.read_text(encoding="utf-8"))
    lebron = json.loads(LEBRON.read_text(encoding="utf-8"))
    davis_ids = {row["event_id"] for row in davis["rows"]}
    lebron_ids = {row["event_id"] for row in lebron["rows"]}
    if len(davis_ids) != 30 or len(lebron_ids) != 31:
        raise ValueError("source window count mismatch")
    with BASELINE.open(encoding="utf-8-sig", newline="") as handle:
        incident_rows = [row for row in csv.DictReader(handle) if f"{row['date']}_{row['home']}_{row['away']}" == DAVIS_INCIDENT]
    if len(incident_rows) != 1 or (incident_rows[0]["home_score"], incident_rows[0]["away_score"]) != ("122", "105"):
        raise ValueError("Davis February 14 incident baseline mismatch")
    # The Davis audit starts with his first full absence on February 16.
    # A changed 2/14 collision also requires rechecking that partial game.
    davis_recheck = davis_ids | {DAVIS_INCIDENT}
    overlap = davis_recheck & lebron_ids
    union = davis_recheck | lebron_ids
    if len(overlap) != 17 or len(union) != 45:
        raise ValueError(f"unexpected overlap/union {len(overlap)}/{len(union)}")
    if "2021-03-20_LAL_ATL" not in overlap:
        raise ValueError("LeBron incident must also be in Davis absence window")
    first_absence = {row["event_id"] for row in lebron["rows"] if row["phase"] == "INITIAL_ABSENCE"}
    if len(first_absence & davis_ids) != 16:
        raise ValueError("first LeBron absence / Davis overlap mismatch")

    out = {
        "stage": "O-15F14-BC",
        "status": "A1_LAKERS_HEALTH_RECHECK_SET_READY / NO_ALT_HEALTH_OR_RESULT_SELECTED",
        "description": "Minimum observed-date input sets if either historical health calendar is changed; downstream games and postseason remain additional work.",
        "historical_game_sets": {
            "davis_30_absence": sorted(davis_ids),
            "davis_feb14_incident": DAVIS_INCIDENT,
            "lebron_31_incident_absence_return": sorted(lebron_ids),
            "intersection_17": sorted(overlap),
            "union_45": sorted(union),
        },
        "candidate_recheck_sets": {
            "H00_retain_both": [],
            "H10_change_davis_only": sorted(davis_recheck),
            "H01_change_lebron_only": sorted(lebron_ids),
            "H11_change_both": sorted(union),
        },
        "cautions": [
            "H00 still requires alternate roster/coach/transaction and playoff checks; empty health-change set is not a season PASS.",
            "A change to either health calendar can alter earlier or later game flow, transactions, seeding and postseason beyond these date sets.",
            "These are games to recheck, not predicted winner flips or certified alternative diagnoses.",
        ],
        "input_sha256": {
            str(BASELINE.relative_to(ROOT)): sha256(BASELINE),
            str(DAVIS.relative_to(ROOT)): sha256(DAVIS),
            str(LEBRON.relative_to(ROOT)): sha256(LEBRON),
        },
        "selected": False,
        "health_calendar_author_locked": False,
        "manuscript_allowed": False,
    }
    OUTPUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote 31 Davis (2/14+30) / 31 LeBron / 17 shared / 45 unique Lakers historical-date inputs")


if __name__ == "__main__":
    main()
