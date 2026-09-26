"""Cross-check the G15AL conditional cap sequence against the G15AJ named ledger."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
prior = json.loads((ROOT / "research/O15G15AJ_DETROIT_AUG6_NAMED_SALARY_LEDGER.json").read_text(encoding="utf-8"))
ledger = json.loads((ROOT / "research/O15G15AL_DETROIT_PRE_OLYNYK_ROSTER_CHARGE_SEQUENCE.json").read_text(encoding="utf-8"))

minimum = ledger["zero_service_minimum_candidate"]
qos = prior["original_optional_additions"]
additions = prior["original_common_additions"]
original_count = len(prior["original_core"]) + 1 + 2  # core, Cade hold, Frank/Diallo QOs
original_count += 1  # Saben Lee's two-way-completion Free Agent Amount
alternate_count = original_count + 1  # retained Plumlee
assert original_count == ledger["original_counted_players_before"]
assert alternate_count == ledger["alternate_counted_players_before"]
assert max(0, 12 - original_count) == ledger["original_incomplete_roster_charges"]
assert max(0, 12 - alternate_count) == ledger["alternate_incomplete_roster_charges"]
assert ledger["saben_lee_free_agent_amount_candidate"] == minimum

base = (
    sum(prior["original_core"].values())
    + sum(prior["candidate_dead_money"].values())
    + additions["Cade Cunningham unsigned rookie hold"]
    + qos["Frank Jackson outstanding QO case"]
    + qos["Hamidou Diallo outstanding QO case"]
    + ledger["saben_lee_free_agent_amount_candidate"]
)
original_salary = base + max(0, 12 - original_count) * minimum
alternate_salary = base + sum(prior["alternate_replacements"].values()) + max(0, 12 - alternate_count) * minimum
assert original_salary == ledger["original_candidate_team_salary_before"]
assert alternate_salary == ledger["alternate_candidate_team_salary_before"]
assert original_salary + ledger["original_nominal_room_before"] == ledger["cap"]
assert alternate_salary + ledger["alternate_nominal_room_before"] == ledger["cap"]

olynyk = additions["Kelly Olynyk"]
room = ledger["alternate_nominal_room_before"]
assert room - olynyk == ledger["alternate_olynyk_first_pre_signature_room_margin"]
assert room - olynyk + (minimum if alternate_count < 12 else 0) == ledger["alternate_nominal_room_after_olynyk_first"]
assert room - ledger["alternate_dead_money_delta_hoopshype"] - olynyk == ledger["alternate_olynyk_first_pre_signature_margin_with_hoopshype_dead_money"]
for name, key in (
    ("Trey Lyles", "alternate_olynyk_margin_if_lyles_first"),
    ("Isaiah Livers", "alternate_olynyk_margin_if_livers_first"),
):
    assert room - additions[name] - olynyk == ledger[key]
lee_increment = additions["Saben Lee"] - ledger["saben_lee_free_agent_amount_candidate"]
assert room - lee_increment - olynyk == ledger["alternate_olynyk_margin_if_lee_first"]
frank_increment = qos["Frank Jackson signed contract case"] - qos["Frank Jackson outstanding QO case"]
assert room - frank_increment - olynyk == ledger["alternate_olynyk_margin_if_frank_3m_first"]
print("O-15G15AL conditional roster-charge arithmetic: PASS; legal cap eligibility remains HOLD")
