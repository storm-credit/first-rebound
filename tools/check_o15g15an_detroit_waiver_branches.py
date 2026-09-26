"""Check the waiver-window branches against the prior named salary ledger."""

import json
from pathlib import Path


root = Path(__file__).resolve().parents[1]
previous = json.loads((root / "research/O15G15AL_DETROIT_PRE_OLYNYK_ROSTER_CHARGE_SEQUENCE.json").read_text(encoding="utf-8"))
current = json.loads((root / "research/O15G15AN_DETROIT_WAIVER_AND_EXCEPTION_BRANCHES.json").read_text(encoding="utf-8"))
minimum = current["rookie_minimum_candidate"]
old_charge = current["old_mcgruder_non_guaranteed_candidate"]
cap = previous["cap"]
olynyk = previous["olynyk_first_year_candidate"]

for prefix, start_salary, start_count in (
    ("original", previous["original_candidate_team_salary_before"], previous["original_counted_players_before"]),
    ("alternate", previous["alternate_candidate_team_salary_before"], previous["alternate_counted_players_before"]),
):
    for suffix, included in (("old_charge_removed_and_not_counted", False), ("old_charge_still_included", True)):
        row = current["cases"][f"{prefix}_{suffix}"]
        count = start_count + int(included)
        salary = start_salary + (old_charge if included else 0) - (minimum if included and start_count < 12 else 0)
        room = cap - salary
        margin = room - olynyk
        after = margin + (minimum if count < 12 else 0)
        assert row == {
            "players_counted": count,
            "candidate_team_salary": salary,
            "nominal_room": room,
            "olynyk_pre_signature_margin": margin,
            "nominal_room_after_olynyk": after,
        }, f"{prefix}_{suffix}"

assert current["cases"]["alternate_old_charge_still_included"]["olynyk_pre_signature_margin"] < 0
print("O-15G15AN McGruder waiver-accounting branches: PASS; actual cap ledger HOLD")
