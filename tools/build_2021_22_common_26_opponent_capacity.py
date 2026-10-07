"""One conditional capacity compiler for the 26 Chicago opponents not covered by DET/NOP/TOR.

This constructs fictional regulation role witnesses from named S2 seed players.
It deliberately does not execute reported transactions, contracts, health or results.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_2021_22_common_26_opponent_capacity.py"
OUT = "simulation/NBA_2021_22_COMMON_26_OPPONENT_CAPACITY.json"
MD = OUT.replace(".json", ".md")
SCOPE = "design/CHICAGO_2021_22_OPPONENT_FINITE_DISPATCH_SCOPE_2026_10_07.json"
CALENDAR = "simulation/CHICAGO_2021_22_CALENDAR.csv"
SEED = "simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json"
BOARD = "research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json"
OLD_CLOCK = "simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.json"
OLD_ROLE = "simulation/NBA_2020_21_FINAL859_OBSERVATIONS.csv"
CHI_CHOICE = "simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json"
CHI_AUTHORITY = "canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json"
DETROIT = "research/DETROIT_2021_OPENING_NAMED_OPERATING_FAMILY_2026_10_07.json"
TORONTO = "simulation/TORONTO_2021_NAMED_ROSTER_CAPACITY_CONDITIONAL_FAMILY.json"
PINS = {
    SCOPE: "a57bec4bc61e2bf2030ebc25f800f06e2c64cd86e9ed573a2ccc4c4d958af203",
    CALENDAR: "c59ea19a5515d64ed03cae8e0481847b6572d4087bbcefef15896bb7a2489183",
    SEED: "cfa2f49bb82baa49b2298d90c97cd7fd8075e91380424d40bfd44772d8228a2b",
    BOARD: "90099928f9133c4087ee7871939ce58216d183bd186f5ebd3575a56c2348eeed",
    OLD_CLOCK: "e1590fa1c652c7c9d2f04b70fba5453e62aac49531a104acc7aabf24f540b665",
    OLD_ROLE: "c67a059489be1e34cf998c0cfa59dadb0ffcc46ba175f1781747fd380e20e0fb",
    CHI_CHOICE: "274a35e163c7f6fd7f0d3e5494b3c46753aaf9900036676be935f17a9d538c32",
    CHI_AUTHORITY: "51b24c8a6bc1eb703568adced46b3ffa15845e85e8da10da1242bddf941df960",
    DETROIT: "7490b1a46a744088980c115680140383615a2e6ec92901e1fdd901c326861be0",
    TORONTO: "ef43ee3052540099aa33263dbe5688ca8a1231df61a6291e432894d2b61541dd",
}
EXCLUDED = frozenset({"DET", "NOP", "TOR"})
IMPORTANT_BRANCHES = {
    "BOS": ["AP1_KEMBA_HORFORD_BROWN_16_UNSELECTED"],
    "OKC": ["AP1_SG16_ACTORS_ASSETS_UNSELECTED"],
    "SAC": ["S14A_D_SABONIS_FOUR_TEAM_DIRECTION_UNSELECTED"],
    "HOU": ["SG16_PICK16_SENGUN_ASSIGNMENT_UNSELECTED"],
}
POSITIONS = ("PG", "SG", "SF", "PF", "C")
GENERIC_CAUSAL = "Reconcile S2 contract expiry/options, DB1 rights-versus-UPC and any reported assignments with the chosen candidate family. No actual opening roster automatically adopted."


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def normalized_sha(path: Path) -> str:
    source = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def json_file(root: Path, relative: str):
    return json.loads((root / relative).read_text(encoding="utf-8-sig"))


def csv_file(root: Path, relative: str):
    with (root / relative).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def source_inputs(root: Path):
    for relative, expected in PINS.items():
        require(normalized_sha(root / relative) == expected, "Source changed: " + relative)
    scope = json_file(root, SCOPE)
    seed = json_file(root, SEED)
    board = json_file(root, BOARD)
    clock = json_file(root, OLD_CLOCK)
    calendar = csv_file(root, CALENDAR)
    old_roles = csv_file(root, OLD_ROLE)
    chi = json_file(root, CHI_CHOICE)
    authority = json_file(root, CHI_AUTHORITY)
    for relative, loaded in ((SCOPE, scope), (SEED, seed), (BOARD, board), (OLD_CLOCK, clock), (CHI_CHOICE, chi), (CHI_AUTHORITY, authority)):
        require(loaded == json.loads((root / relative).read_text(encoding="utf-8-sig")), "Loaded JSON differs from physical source: " + relative)
    for relative, loaded in ((CALENDAR, calendar), (OLD_ROLE, old_roles)):
        with (root / relative).open(encoding="utf-8-sig", newline="") as stream:
            require(loaded == list(csv.DictReader(stream)), "Loaded CSV differs from physical source: " + relative)
    raw_file = Path(scope["raw_feed_source"]["path"])
    raw_bytes = raw_file.read_bytes()
    require(hashlib.sha256(raw_bytes).hexdigest() == scope["raw_feed_source"]["raw_sha256"], "Reported event raw feed changed")
    movement = json.loads(raw_bytes)["NBA_Player_Movement"]["rows"]
    require(len(movement) == scope["raw_feed_source"]["rows"] == 9927, "Raw feed count changed")
    require(len(calendar) == 82 and len({x["game_id"] for x in calendar}) == 82, "Calendar domain changed")
    require(len(chi["selected_dates"]) == 82 and authority["selected"]["selected_date_rows"]["sha256"] == PINS[CHI_CHOICE], "Chicago delegated state source changed")
    require((chi["summary"]["normal"], chi["summary"]["coby_out"]) == (58, 24), "Chicago selected counts changed")
    require(authority["selected"]["date_state_count"] == 82, "Chicago selected authority changed")
    require(scope["source_sha256"][SEED] == PINS[SEED] and scope["source_sha256"][BOARD] == PINS[BOARD], "Scope seed/rights ancestry changed")
    return scope, seed, board, clock, calendar, old_roles, chi, movement


def role_evidence(rows):
    positions: dict[str, Counter] = defaultdict(Counter)
    observed_teams: dict[str, set] = defaultdict(set)
    for row in rows:
        if row["observed_start_position"] in ("G", "F", "C"):
            positions[row["player"]][row["observed_start_position"]] += 1
            observed_teams[row["player"]].add(row["team"])
    return positions, observed_teams


def check_team_source(team, item, seed, board, movement):
    old = item["seed_S2_May16"]
    pointer = old["binding_pointer"]
    require(pointer.startswith("team_game_bindings[") and pointer.endswith("]"), "Bad S2 binding pointer")
    binding = seed["team_game_bindings"][int(pointer[len("team_game_bindings["):-1])]
    require(binding["team"] == team and binding["event_id"] == old["binding_event_id"], "S2 team/date identity changed")
    require(old["roster_state_pointer"] == "roster_states." + binding["state_id"], "S2 state pointer changed")
    state = seed["roster_states"][binding["state_id"]]
    standard = [x["player"] for x in state["players"] if x["contract_class"] == "STANDARD"]
    two_way = [x["player"] for x in state["players"] if x["contract_class"] == "TWO_WAY"]
    require((standard, two_way) == (old["STANDARD"], old["TWO_WAY"]), "S2 source roster differs")
    require((len(standard), len(two_way)) == (old["standard_count"], old["two_way_count"]), "S2 reported roster count changed")
    hardship_excluded = []
    if len(standard) > 15:
        require(team == "HOU" and old["named_hardship_working_capacity"] == 2, "Oversize S2 roster has no named hardship boundary")
        hardship_excluded = ["Cameron Oliver", "Cameron Reynolds"]
        require(all(name in standard for name in hardship_excluded), "Named HOU hardship identities changed")
        standard = [name for name in standard if name not in hardship_excluded]
    require(12 <= len(standard) <= 15 and len(two_way) <= 2, "Conditional opening nomination slot domain changed")
    for right in item["DB1_conditional_draft_rights"]:
        rows = [x for x in board["rows"] if x["pick"] == right["pick"]]
        require(len(rows) == 1, "DB1 pick missing")
        entry = rows[0]
        require((entry["player"], entry["conditional_final_draft_rights_holder"], entry["selecting_team"]) == (right["player"], team, right["selecting_team"]), "DB1 rights/member source differs")
        require(not right["NBA_UPC_created"] and not right["RequiredTender_created"], "Unsigned right promoted")
    events = item["reported_event_source"]["events"]
    for event in events:
        raw = movement[event["source_row_index"]]
        player_id = int(raw["PLAYER_ID"]) if raw["PLAYER_ID"] is not None else 0
        require((raw["GroupSort"], raw["TRANSACTION_DATE"][:10], raw["Transaction_Type"], int(raw["TEAM_ID"]), player_id or None, raw["PLAYER_SLUG"] or "") == (event["GroupSort"], event["reported_date"], event["transaction_type"], int(event["TEAM_ID"]), event["player_id"], event["player_slug"]), "Reported event actor/date/type differs from raw")
        require(event["fictional_event_applied"] is False, "Unreviewed historical movement applied")
    return standard, two_way, state, events, hardship_excluded


def build_team_role(team, item, old, old_positions, observed_teams, standard, two_way, events, hardship_excluded):
    latest = [x for x in old["team_games"] if x["event_id"] == item["seed_S2_May16"]["binding_event_id"] and x["team"] == team]
    require(len(latest) == 1, "May S2 prior player vector missing")
    historical_seconds = latest[0]["player_seconds"]
    role_class = {}
    for name in standard:
        counts = old_positions[name]
        if counts:
            role_class[name] = sorted(counts, key=lambda v: (-counts[v], ("G", "F", "C").index(v)))[0]
    pools = {kind: sorted((n for n in standard if role_class.get(n) == kind), key=lambda n: (-historical_seconds.get(n, 0), n)) for kind in ("G", "F", "C")}
    require(len(pools["G"]) >= 2 and len(pools["F"]) >= 2 and len(pools["C"]) >= 1, team + " prior role position domain incomplete")
    chosen = set(pools["G"][:2] + pools["F"][:2] + pools["C"][:1])
    remainder = sorted((n for n in role_class if n not in chosen), key=lambda n: (-historical_seconds.get(n, 0), n))
    chosen.update(remainder[: min(10, len(role_class)) - len(chosen)])
    selected = {k: [n for n in pools[k] if n in chosen] for k in pools}
    require(8 <= len(chosen) <= 10 and all(selected[k] for k in selected), "Positive role cohort outside 8..10")
    blocks = []
    seconds = Counter()
    position_seconds = {p: Counter() for p in POSITIONS}
    for i in range(12):
        guards = selected["G"]
        forwards = selected["F"]
        centers = selected["C"]
        five = {"PG": guards[i % len(guards)], "SG": guards[(i + 1) % len(guards)], "SF": forwards[i % len(forwards)], "PF": forwards[(i + 1) % len(forwards)], "C": centers[i % len(centers)]}
        require(len(set(five.values())) == 5, team + " duplicate five-player role")
        for pos, player in five.items():
            seconds[player] += 240
            position_seconds[pos][player] += 240
        blocks.append({"index": i, "start_second": 240 * i, "end_second": 240 * (i + 1), "seconds": 240, "positions": five, "primary_creator": five["PG"]})
    require(set(seconds) == chosen and sum(seconds.values()) == 14400, team + " role clock did not use selected cohort")
    require(all(sum(v.values()) == 2880 for v in position_seconds.values()), team + " position total differs")
    require(max(seconds.values()) <= 2880, team + " player exceeds 48 minutes")
    active = [n for n in standard if n in seconds]
    active.extend([n for n in standard if n not in seconds][: 12 - len(active)])
    inactive = [n for n in standard if n not in active]
    require(len(active) == 12 and len(inactive) == len(standard) - 12 and set(seconds) <= set(active), team + " nomination size changed")
    named_conflicts = [x for x in item["named_causal_inputs"] if x != GENERIC_CAUSAL]
    return {
        "team": team,
        "function_id": "COMMON_2021_22_CONDITIONAL_OPPONENT_CAPACITY::" + team,
        "status": "MATHEMATICAL_ROLE_CAPACITY_CONDITIONAL_ON_NAMED_LEGAL_RETENTION_AND_AVAILABILITY",
        "source_seed_pointer": item["seed_S2_May16"]["binding_pointer"],
        "source_role_prior": {"path": OLD_ROLE, "season": "2020-21", "meaning": "historically observed G/F/C start class used only as fictional role eligibility; not 2021-22 minutes or health"},
        "source_S2_event_id": item["seed_S2_May16"]["binding_event_id"],
        "source_May16_positive_seconds_used_only_for_ranking": {n: historical_seconds.get(n, 0) for n in chosen},
        "standard_named_continuation_condition_max15": standard,
        "two_way_named_continuation_condition_max2": two_way,
        "source_hardship_names_not_carried_to_2021_22": hardship_excluded,
        "open_standard_slots_to_15_not_filled_here": 15 - len(standard),
        "open_two_way_slots_to_2_not_filled_here": 2 - len(two_way),
        "DB1_unsigned_conditional_rights": copy.deepcopy(item["DB1_conditional_draft_rights"]),
        "reported_event_source_row_indices_not_applied": [x["source_row_index"] for x in events],
        "reported_atomic_GroupSort_not_applied": sorted({x["GroupSort"] for x in events}),
        "known_causal_conflict_inputs": named_conflicts,
        "important_unselected_branch_inputs": IMPORTANT_BRANCHES.get(team, []),
        "role_class_prior": {n: role_class[n] for n in sorted(chosen)},
        "role_class_observed_teams_prior": {n: sorted(observed_teams[n]) for n in chosen},
        "fictional_positive_players": sorted(seconds),
        "working_active12": active,
        "working_inactive_standard": inactive,
        "two_way_regular_active_used": [],
        "zero_minute_reserve_clinical_status": None,
        "all_named_medical_clearance_certified": False,
        "starters_working": list(blocks[0]["positions"].values()),
        "blocks": blocks,
        "player_seconds": dict(sorted(seconds.items())),
        "position_seconds": {p: dict(sorted(position_seconds[p].items())) for p in POSITIONS},
        "elapsed_seconds": 2880,
        "team_player_seconds": 14400,
        "legal_operating_interval_selected": False,
        "actual_2021_22_contracts_or_active_list_certified": False,
        "score": None,
        "winner": None,
    }


def assert_returned_fixture(team, item, fixture, old, old_positions, standard, two_way, events):
    """Check a returned role against primitive sources without trusting its counters."""
    prior = [x for x in old["team_games"] if x["event_id"] == item["seed_S2_May16"]["binding_event_id"] and x["team"] == team]
    require(len(prior) == 1, "Returned fixture prior source missing")
    seconds_prior = prior[0]["player_seconds"]
    role = {}
    for name in standard:
        counts = old_positions[name]
        if counts:
            role[name] = max(("G", "F", "C"), key=lambda value: (counts[value], -("G", "F", "C").index(value)))
    pools = {kind: sorted((n for n in standard if role.get(n) == kind), key=lambda n: (-seconds_prior.get(n, 0), n)) for kind in ("G", "F", "C")}
    selected = set(pools["G"][:2] + pools["F"][:2] + pools["C"][:1])
    remainder = sorted((n for n in role if n not in selected), key=lambda n: (-seconds_prior.get(n, 0), n))
    selected.update(remainder[: min(10, len(role)) - len(selected)])
    lists = {kind: [n for n in pools[kind] if n in selected] for kind in pools}
    require(fixture["role_class_prior"] == {n: role[n] for n in sorted(selected)}, "Returned role class differs from primitive observation")
    require(set(fixture["fictional_positive_players"]) == selected, "Returned positive cohort differs from old source-ranked fixture")
    require(fixture["standard_named_continuation_condition_max15"] == standard and fixture["two_way_named_continuation_condition_max2"] == two_way, "Returned named membership differs")
    require(fixture["reported_event_source_row_indices_not_applied"] == [x["source_row_index"] for x in events], "Returned event lineage differs")
    total = Counter()
    positions = {p: Counter() for p in POSITIONS}
    require(len(fixture["blocks"]) == 12, "Returned block count differs")
    for i, block in enumerate(fixture["blocks"]):
        expected = {"PG": lists["G"][i % len(lists["G"])], "SG": lists["G"][(i + 1) % len(lists["G"])], "SF": lists["F"][i % len(lists["F"])], "PF": lists["F"][(i + 1) % len(lists["F"])], "C": lists["C"][i % len(lists["C"])]}
        require((block["index"], block["start_second"], block["end_second"], block["seconds"]) == (i, i * 240, (i + 1) * 240, 240), "Returned clock segment differs")
        require(block["positions"] == expected and block["primary_creator"] == expected["PG"] and len(set(expected.values())) == 5, "Returned PG/SG/position or creator differs from primitive role policy")
        for position, name in expected.items():
            total[name] += 240
            positions[position][name] += 240
    require(fixture["player_seconds"] == dict(sorted(total.items())) and fixture["position_seconds"] == {p: dict(sorted(v.items())) for p, v in positions.items()}, "Returned player/position seconds differ")
    require(sum(total.values()) == 14400 and all(sum(v.values()) == 2880 for v in positions.values()), "Returned team/position clock differs")
    active = [n for n in standard if n in total]
    active.extend([n for n in standard if n not in total][:12 - len(active)])
    require(fixture["working_active12"] == active and fixture["working_inactive_standard"] == [n for n in standard if n not in active], "Returned active partition differs")
    require(fixture["source_S2_event_id"] == item["seed_S2_May16"]["binding_event_id"] and fixture["legal_operating_interval_selected"] is False and fixture["actual_2021_22_contracts_or_active_list_certified"] is False, "Returned source/date authority changed")


def build(root: Path = ROOT):
    scope, seed, board, clock, calendar, old_roles, chi, movement = source_inputs(root)
    old_positions, observed_teams = role_evidence(old_roles)
    choice = {x["game_id"]: x for x in chi["selected_dates"]}
    require(len(choice) == 82, "Chicago selected date identity duplicates")
    team_codes = sorted(set(scope["teams"]) - EXCLUDED)
    require(len(team_codes) == 26, "Remaining opponent team domain changed")
    fixtures = {}
    for team in team_codes:
        item = scope["teams"][team]
        standard, two_way, _, events, hardship_excluded = check_team_source(team, item, seed, board, movement)
        fixtures[team] = build_team_role(team, item, clock, old_positions, observed_teams, standard, two_way, events, hardship_excluded)
        assert_returned_fixture(team, item, fixtures[team], clock, old_positions, standard, two_way, events)
    names_to_teams = defaultdict(list)
    for team, fixture in fixtures.items():
        for name in fixture["standard_named_continuation_condition_max15"]:
            names_to_teams[name].append(team)
    require(all(len(teams) == 1 for teams in names_to_teams.values()), "Same player simultaneously retained on two of 26 teams")
    external = []
    detroit = json_file(root, DETROIT)
    toronto = json_file(root, TORONTO)
    for branch in detroit["roster_candidates"]:
        for name in branch["standard_candidate"]:
            if name in names_to_teams:
                external.append({"player": name, "this_seed_team": names_to_teams[name][0], "other_conditional_team": "DET", "other_branch": branch["id"], "simultaneous_membership_allowed_without_lawful_transfer": False})
    for row in toronto["rows"]:
        if row["availability_parameter"] != "SIAKAM_AVAILABLE":
            continue
        for name in row["standard"]:
            if name in names_to_teams:
                external.append({"player": name, "this_seed_team": names_to_teams[name][0], "other_conditional_team": "TOR", "other_branch": row["path"], "simultaneous_membership_allowed_without_lawful_transfer": False})
    require(len(external) == 6, "DET/TOR shared-player conflict boundary changed")
    dates = []
    for calendar_row in calendar:
        team = calendar_row["opponent"]
        if team in EXCLUDED:
            continue
        game_id = calendar_row["game_id"]
        require(game_id in scope["teams"][team]["all_game_ids"], "Date team source mapping changed")
        selected = choice[game_id]
        require((selected["date"], selected["home"], selected["away"], selected["opponent"]) == (calendar_row["date"], calendar_row["home"], calendar_row["away"], team), "CHI delegated state date/source differs")
        require(selected["selected_chicago_state"] in ("NORMAL", "COBY_OUT"), "CHI state outside reviewed carrier")
        fixture = fixtures[team]
        dates.append({"game_id": game_id, "date": calendar_row["date"], "home": calendar_row["home"], "away": calendar_row["away"], "opponent": team, "selected_CHI_state": selected["selected_chicago_state"], "CHI_source_pointer": CHI_CHOICE + ":/selected_dates/game_id=" + game_id, "opponent_conditional_function_id": fixture["function_id"], "opponent_positive_players_if_conditions_met": fixture["fictional_positive_players"], "opponent_regulation_seconds_if_conditions_met": fixture["elapsed_seconds"], "opponent_team_player_seconds_if_conditions_met": fixture["team_player_seconds"], "source_S2_May16_event_not_this_requested_game": fixture["source_S2_event_id"], "named_legal_operating_interval_proven_on_date": False, "important_branch_selected": False, "opponent_health_selected": False, "score": None, "winner": None, "overtime_selected": False, "executable_2021_22_game_capacity": False, "typed_gap": "NAMED_CONTINUATION_OR_RENEWAL_AND_REPORTED_ATOMIC_EVENTS_NOT_SELECTED_FOR_THIS_DATE"})
    require(len(dates) == 72 and len({x["game_id"] for x in dates}) == 72, "26-team requested date count changed")
    require(len([x for x in dates if x["opponent"] in ("SAC", "ORL")]) == 6, "Old stencil scope changed")
    event_count = sum(len(scope["teams"][t]["reported_event_source"]["events"]) for t in team_codes)
    return {
        "id": "NBA_2021_22_COMMON_26_OPPONENT_CONDITIONAL_CAPACITY",
        "status": "SOURCE_BOUND_CONDITIONAL_ROLE_FUNCTIONS_26_NOT_DATED_LEGAL_EXECUTION",
        "source_hash_method": "UTF8_BOM_REMOVED_LF_NORMALIZED_SHA256",
        "source_hashes": PINS | {SELF: normalized_sha(root / SELF)},
        "raw_player_movement_sha256": scope["raw_feed_source"]["raw_sha256"],
        "facts_vs_design": {"fact": "S2 May16 named working roster, conditional DB1 draft-rights board, 1034 scoped reported-event observations, old G/F/C starter labels and 82 historical calendar keys.", "design": "A hypothetical continuation of each prior 15+2 name set plus 8..10 positive fictional role players, 12 active nominees and 12 four-minute regulation blocks.", "not_selected": "Every date's opponent contract interval, reported trade atom, medical availability, result and overtime."},
        "policy": {"reported_event_application": "NONE; 1034 reports are indexed source observations, not 1034 required new tasks or silently executed transactions", "old_May16_contracts_automatically_current": False, "DB1_rights_are_UPC": False, "role_position_is_actual_2021_22_box": False, "creator_role_is_fictional_guard_assignment_from_prior_G_class": True, "zero_minutes_imply_injury": False},
        "summary": {"opponent_teams_excluding_DET_NOP_TOR": 26, "requested_dates": 72, "conditional_role_functions_constructed": 26, "role_fixture_missing_teams": 0, "positive_player_range": [min(len(x["fictional_positive_players"]) for x in fixtures.values()), max(len(x["fictional_positive_players"]) for x in fixtures.values())], "working_active_each": 12, "working_standard_range": [min(len(x["standard_named_continuation_condition_max15"]) for x in fixtures.values()), max(len(x["standard_named_continuation_condition_max15"]) for x in fixtures.values())], "working_two_way_range": [min(len(x["two_way_named_continuation_condition_max2"]) for x in fixtures.values()), max(len(x["two_way_named_continuation_condition_max2"]) for x in fixtures.values())], "blocks_each": 12, "total_role_blocks": 312, "team_seconds_each": 14400, "elapsed_seconds_each": 2880, "reported_source_rows_in_these_26_team_views": event_count, "reported_source_rows_executed": 0, "shared_named_player_conflicts_with_conditional_DET_TOR_branches": len(external), "legal_operating_interval_pending_teams": 26, "executable_requested_dates": 0, "typed_date_interval_gaps": 72, "important_branch_teams": sorted(IMPORTANT_BRANCHES), "opponent_health_or_result_selected": 0},
        "external_conditional_membership_conflicts": external,
        "team_functions": fixtures,
        "requested_dates": dates,
        "certification": {"conditional_mathematical_role_function_constructed": True, "actual_15_plus_2_contracts_executed": False, "all_26_legal_intervals_completed": False, "all_72_opponent_health_selected": False, "whole_82_result_or_OT_selected": False, "new_consequential_author_choice": False, "whole_macro3_complete": False, "central_dispatcher_changed": False, "REGISTER_changed": False, "manuscript_allowed": False},
    }


def validate(packet, root: Path = ROOT):
    try:
        require(packet == build(root), "Conditional capacity differs from source-bound construction")
        return []
    except (ValueError, KeyError, TypeError, OSError, IndexError, AssertionError) as exc:
        return [str(exc)]


def markdown(packet):
    s = packet["summary"]
    lines = ["# 2021–22 Chicago 상대 26팀 공통 조건부 역할 함수", "", packet["status"], "", f"기존 DET/NOP와 TOR을 제외한 **26팀·72날짜**에 한 생성기를 적용했다. 각 팀은 2020–21 S2 May16 명명 seed를 **가상으로 유지하거나 합법 갱신한다는 조건**에서 9–10명 양수, 12명 작업 active, 12×240초 블록, 팀 14,400선수초를 구성한다. HOU 원17STD에는 당시 hardship2가 포함돼 해당2를 이월하지 않고15명만 사용한다. MIN14STD/1TW, PHX15STD/1TW의 빈 슬롯은 임의 선수로 채우지 않았다. 2021–22 실제 등록·건강·승패를 선택한 것이 아니다.", "", "## 소스와 경계", "", "- `design/CHICAGO_2021_22_OPPONENT_FINITE_DISPATCH_SCOPE_2026_10_07.json#/teams/{TEAM}`의 May16 S2 roster state/DB1 권리/전체1034개 raw 보고행 중 해당26팀916개/원인 충돌을 한 번에 소비한다. `NBA_Player_Movement` raw SHA와 소비행916개의 actor·일자·유형·GroupSort를 직접 대조했다.", "- `simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.json`의 May16 선수분은 가상 역할 후보 우선순위에만 쓴다. `simulation/NBA_2020_21_FINAL859_OBSERVATIONS.csv`의 G/F/C 선발 분류는 가능한 가상 포지션 입력이며 2021–22 출전분이나 의료 근거가 아니다. PG 창조자는 해당 G 선수에게 부여한 가상 코칭 과제다.", "- 원역사 Signing/Waive/Trade/Conversion/Claim을 자동 실행하지 않는다. 같은 GroupSort 거래는 상대 팀/선수·권리·보호급여를 원자로 대조해야 한다. DB1 미선택 권리는 NBA UPC나 명단 선수가 아니다. DET A/B와 TOR T1을 함께 보면 Kelly Olynyk(HOU↔DET), Trey Lyles(SAS↔DET), Dragic·Achiuwa(MIA↔TOR), Mykhailiuk(OKC↔TOR)의 조건부 중복이 생긴다. 원자 이동 없이 동시 명단으로 승격하지 않는다.", "- Chicago 상태는 채택된 58 NORMAL/24 COBY_OUT 원장의 정확 game_id/date/home/away를 조인했다. 상대 명단·건강·경제·승패/OT는 모두 날짜별 typed HOLD이고 원 May16 이벤트 ID를 요청된 2021–22 게임 ID로 바꿔 쓰지 않는다.", "", "## 완료와 실제 남은 입력", "", f"조건부 **역할 함수 {s['conditional_role_functions_constructed']}/26**, 요청 날짜 **{s['requested_dates']}/72**를 원천 연결했다. 역할 fixture 누락팀 {s['role_fixture_missing_teams']}개. 그러나 합법 계약/선수이동 interval 미실행 **{s['legal_operating_interval_pending_teams']}팀·{s['typed_date_interval_gaps']}날짜**, 실제 실행 가능한 상대 날짜 {s['executable_requested_dates']}개다. 이 gap은 각 팀별 새 조사 프로젝트가 아니라 명명된 계약갱신과 원자 거래의 공통 compiler 입력이다.", "", "BOS의 AP1, OKC의 AP1/SG16, HOU의 SG16, SAC의 S14A–D는 실제 중요한 미선택 분기다. 다른 팀의 `known_causal_conflict_inputs`도 역사 거래 자동복사 전에 확인한다. 한 팀의 미선택을 26팀 전체 정지 사유로 삼지 않는다.", "", "## 팀별 역할 요약", "", "| 팀 | 양수 | G/F/C 원형 출처 | 경기키 | 별도 중요 분기 |", "|---|---:|---|---:|---|" ]
    counts = Counter(x["opponent"] for x in packet["requested_dates"])
    for team, item in sorted(packet["team_functions"].items()):
        role_counts = Counter(item["role_class_prior"].values())
        lines.append(f"| {team} | {len(item['fictional_positive_players'])} | {role_counts['G']}/{role_counts['F']}/{role_counts['C']} | {counts[team]} | {', '.join(item['important_unselected_branch_inputs']) or '없음'} |")
    lines += ["", "원고 0. PROJECT_FREEZE v0.30 PARTIAL, 설계·원고 CLOSED. 새 정본/REGISTER/중앙 dispatcher 변경 없음.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    options = parser.parse_args()
    packet = build()
    require(validate(packet) == [], "Constructed packet is not current")
    prose = markdown(packet)
    if options.self_test:
        damaged = copy.deepcopy(packet)
        damaged["requested_dates"][0]["selected_CHI_state"] = "UNSELECTED"
        require(validate(damaged), "Wrong delegated Chicago state escaped source comparison")
    if options.write:
        (ROOT / OUT).write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (ROOT / MD).write_text(prose, encoding="utf-8")
    if options.check:
        require(json_file(ROOT, OUT) == packet, "Saved JSON differs")
        require((ROOT / MD).read_text(encoding="utf-8-sig") == prose, "Saved MD differs")
    print("PASS", packet["summary"])


if __name__ == "__main__":
    main()
