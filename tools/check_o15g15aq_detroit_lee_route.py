"""Check the G15AQ multi-signature conditional cap-room arithmetic."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
prior = json.loads((ROOT / "research/O15G15AJ_DETROIT_AUG6_NAMED_SALARY_LEDGER.json").read_text(encoding="utf-8"))
base = json.loads((ROOT / "research/O15G15AL_DETROIT_PRE_OLYNYK_ROSTER_CHARGE_SEQUENCE.json").read_text(encoding="utf-8"))
route = json.loads((ROOT / "research/O15G15AQ_DETROIT_LEE_CAP_ROOM_AND_NONBIRD_ROUTE.json").read_text(encoding="utf-8"))

assert base["alternate_counted_players_before"] == 12
assert base["alternate_incomplete_roster_charges"] == 0
assert route["starting_nominal_room_candidate"] == base["alternate_nominal_room_before"]
assert route["saben_lee_free_agent_amount_candidate"] == base["saben_lee_free_agent_amount_candidate"]
assert route["saben_lee_first_year_contract_candidate"] == prior["original_common_additions"]["Saben Lee"]
assert route["olynyk_first_year_contract_candidate"] == prior["original_common_additions"]["Kelly Olynyk"]
assert route["lyles_first_year_contract_candidate"] == prior["original_common_additions"]["Trey Lyles"]
assert route["frank_qo_candidate"] == prior["original_optional_additions"]["Frank Jackson outstanding QO case"]
assert route["frank_first_year_contract_candidate"] == prior["original_optional_additions"]["Frank Jackson signed contract case"]

lee_increment = route["saben_lee_first_year_contract_candidate"] - route["saben_lee_free_agent_amount_candidate"]
assert lee_increment == route["saben_lee_incremental_team_salary_candidate"]
room = route["starting_nominal_room_candidate"] - route["olynyk_first_year_contract_candidate"] - lee_increment
assert room == route["room_after_olynyk_and_lee_both_cap_room"]
room -= route["lyles_first_year_contract_candidate"]
assert room == route["room_after_olynyk_lee_lyles_all_cap_room"]
assert -room == route["minimum_additional_net_room_needed_for_olynyk_lee_lyles"]
room -= route["frank_first_year_contract_candidate"] - route["frank_qo_candidate"]
assert room == route["room_after_olynyk_lee_lyles_frank_replacement_all_cap_room"]
assert route["nonbird_lee_first_year_ceiling_using_one_year_minimum_candidate"] == round(1.2 * route["saben_lee_first_year_contract_candidate"])
assert route["nonbird_lee_salary_within_ceiling_candidate"] is True
print("O-15G15AQ conditional cap-room route arithmetic: PASS; real method/order/ledger HOLD")
