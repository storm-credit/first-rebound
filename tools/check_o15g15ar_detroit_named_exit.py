"""Check conditional exit/arrival roster charges without claiming a real trade."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ledger = json.loads((ROOT / "research/O15G15AL_DETROIT_PRE_OLYNYK_ROSTER_CHARGE_SEQUENCE.json").read_text(encoding="utf-8"))
route = json.loads((ROOT / "research/O15G15AQ_DETROIT_LEE_CAP_ROOM_AND_NONBIRD_ROUTE.json").read_text(encoding="utf-8"))
screen = json.loads((ROOT / "research/O15G15AR_DETROIT_NAMED_EXIT_AND_ROSTER_CHARGE.json").read_text(encoding="utf-8"))

assert screen["initial_room_candidate"] == route["starting_nominal_room_candidate"]
assert screen["zero_service_minimum_candidate"] == ledger["zero_service_minimum_candidate"]
assert ledger["alternate_counted_players_before"] == 12
assert screen["incoming_increment_candidates"]["Kelly Olynyk"] == route["olynyk_first_year_contract_candidate"]
assert screen["incoming_increment_candidates"]["Saben Lee hold-to-contract"] == route["saben_lee_incremental_team_salary_candidate"]
assert screen["incoming_increment_candidates"]["Trey Lyles"] == route["lyles_first_year_contract_candidate"]
assert screen["incoming_increment_candidates"]["Frank Jackson QO-to-contract"] == route["frank_first_year_contract_candidate"] - route["frank_qo_candidate"]

minimum = screen["zero_service_minimum_candidate"]
for case in screen["salary_free_exit_cases"].values():
    room = screen["initial_room_candidate"]
    count = 12
    for name in case["outgoing"]:
        old_irc = max(0, 12 - count) * minimum
        count -= 1
        new_irc = max(0, 12 - count) * minimum
        room += screen["outgoing_salary_candidates"][name] - (new_irc - old_irc)
    assert room == case["after_exit_room"]
    assert count == case["after_exit_count"]
    for name, salary, new_player, key in (
        ("Kelly Olynyk", screen["incoming_increment_candidates"]["Kelly Olynyk"], True, "after_olynyk_room"),
        ("Saben Lee", screen["incoming_increment_candidates"]["Saben Lee hold-to-contract"], False, "after_lee_room"),
        ("Trey Lyles", screen["incoming_increment_candidates"]["Trey Lyles"], True, "after_lyles_room"),
        ("Frank Jackson", screen["incoming_increment_candidates"]["Frank Jackson QO-to-contract"], False, "after_frank_room"),
    ):
        old_irc = max(0, 12 - count) * minimum
        if new_player:
            count += 1
        new_irc = max(0, 12 - count) * minimum
        room -= salary + (new_irc - old_irc)
        assert room == case[key], (name, room, case[key])

assert screen["salary_free_exit_cases"]["none"]["after_frank_room"] == route["room_after_olynyk_lee_lyles_frank_replacement_all_cap_room"]
jordan = screen["historical_september_jordan_trade_only"]
outgoing = sum(screen["outgoing_salary_candidates"][name] for name in jordan["outgoing"])
assert jordan["incoming_first_year_salary_candidate"] - outgoing == jordan["gross_trade_salary_increase_candidate"]
assert jordan["later_buyout_dead_cap_2021_22_candidate"] - outgoing == jordan["salary_increase_after_later_buyout_candidate"]
print("O-15G15AR conditional named-exit roster-charge arithmetic: PASS; counterparty and August execution HOLD")
