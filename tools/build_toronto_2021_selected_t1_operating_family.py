"""Select a finite Toronto T1 operating route without certifying private NBA papers."""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_toronto_2021_selected_t1_operating_family.py"
OUT = "simulation/TORONTO_2021_SELECTED_T1_OPERATING_FAMILY_2026_10_07.json"
MD = OUT[:-5] + ".md"
BANK = "research/TORONTO_2021_10_25_NAMED_OPERATING_INPUT_BANK_2026_10_07.json"
CAPACITY = "simulation/TORONTO_2021_NAMED_ROSTER_CAPACITY_CONDITIONAL_FAMILY.json"
HEALTH = "simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json"
CALENDAR = "simulation/CHICAGO_2021_22_CALENDAR.csv"
PINS = {
    BANK: "7b6cba6e74044f3b52a79fa966498bca1771294c8bf109bb2213e712210c7096",
    CAPACITY: "ef43ee3052540099aa33263dbe5688ca8a1231df61a6291e432894d2b61541dd",
    HEALTH: "274a35e163c7f6fd7f0d3e5494b3c46753aaf9900036676be935f17a9d538c32",
    CALENDAR: "c59ea19a5515d64ed03cae8e0481847b6572d4087bbcefef15896bb7a2489183",
}
GAME_IDS = ("0022100046", "0022100472", "0022100430", "0022101076")
REMOVED = ("DeAndre' Bembry", "Paul Watson", "Freddie Gillespie")
WANTED_COST_UPPER = 145_895_320


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    data = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def load_json(root, name):
    return json.loads((root / name).read_text(encoding="utf-8-sig"))


def sources(root=ROOT):
    for name, digest in PINS.items():
        require(sha(root / name) == digest, "Reviewed source changed: " + name)
    bank = load_json(root, BANK)
    cap = load_json(root, CAPACITY)
    health = load_json(root, HEALTH)
    with (root / CALENDAR).open(encoding="utf-8-sig", newline="") as stream:
        calendar = list(csv.DictReader(stream))
    require(bank == json.loads((root / BANK).read_text(encoding="utf-8-sig")), "Bank loader differs from physical source")
    require(cap == json.loads((root / CAPACITY).read_text(encoding="utf-8-sig")), "Capacity loader differs from physical source")
    require(health == json.loads((root / HEALTH).read_text(encoding="utf-8-sig")), "Health loader differs from physical source")
    require(bank["operating_paths"]["both"]["selected_path"] is None, "Input bank was silently selected")
    require(bank["operating_paths"]["T1"]["STD_count"] == 15 and bank["operating_paths"]["T1"]["TW_count"] == 2, "T1 source class changed")
    require(bank["whole_cost_boundary"]["whole_normal_TeamSalary_upper"] is None, "Historical whole cost was promoted")
    require([(r["pick"], r["player"]) for r in bank["DB1_conditional_TOR_draft_ports"]] == [(8, "Josh Giddey"), (46, "Dalano Banton"), (48, "Sam Hauser")], "Toronto draft identities changed")
    require(not cap["authority"]["Lowry_direction_selected"] and len(cap["rows"]) == 4, "Conditional capacity authority changed")
    require(len(health["selected_dates"]) == 82, "Chicago health dates changed")
    return bank, cap, health, calendar


def selected_names(bank):
    original = bank["operating_paths"]["T1"]["standard"]
    require(original.count("Isaac Bonga") == 1 and "Aron Baynes" not in original, "Original T1 variation changed")
    standard = ["Aron Baynes" if n == "Isaac Bonga" else n for n in original]
    require(len(standard) == len(set(standard)) == 15, "Selected standard 15 invalid")
    tw = bank["operating_paths"]["T1"]["two_way"]
    require(tw == ["Sam Hauser", "Justin Champagnie"] and not set(standard) & set(tw), "Selected two-way pair invalid")
    return standard, tw


def cost_family(bank, standard, tw):
    old = {r["name"]: r for r in bank["live_original_contract_ports"]}
    require(set(REMOVED) <= set(old) and set(REMOVED).isdisjoint(standard), "Waiver identities changed")
    require("Aron Baynes" in standard and "Kyle Lowry" not in standard and "Norman Powell" in standard, "Selected transaction carrier changed")
    retained = {n: old[n]["reported_current_cap_hit"] for n in standard if n in old}
    require(sum(retained.values()) == 86_932_127, "Retained original contract public sum changed")
    dead_upper = {n: old[n]["reported_current_cap_hit"] for n in REMOVED}
    require(sum(dead_upper.values()) == 5_196_585, "Three protected-release full-salary screen changed")
    incoming = {"Goran Dragic": 19_440_000, "Precious Achiuwa": 2_711_280}
    require(bank["expired_option_and_new_contract_ports"][0]["name"] == "Norman Powell" and bank["expired_option_and_new_contract_ports"][0]["old_PO_2021_22_reported"] == 11_615_328, "Powell option source changed")
    require(next(r for r in bank["expired_option_and_new_contract_ports"] if r["name"] == "Goran Dragic")["reported_current_salary"] == incoming["Goran Dragic"], "Dragic option source changed")
    require(next(r for r in bank["expired_option_and_new_contract_ports"] if r["name"] == "Precious Achiuwa")["reported_current_cap"] == incoming["Precious Achiuwa"], "Precious public cap source changed")
    offers = {
        "Norman Powell": {"form": "TIMELY_EXERCISED_TOR_2021_22_PLAYER_OPTION", "public_point": 11_615_328},
        "Khem Birch": {"form": "ONE_YEAR_APPLICABLE_YOS_MINIMUM_NON_BIRD", "salary_function": "minimum_2021_22(YOS_Birch)", "screen_ceiling": 3_000_000},
        "Josh Giddey": {"form": "TWO_PLUS_TWO_ROOKIE_SCALE_100_PERCENT_OPTIONS_UNEXERCISED", "salary_function": "operative_2021_22_RSC_scale(pick_8,year_1)", "screen_ceiling": 8_000_000},
        "Dalano Banton": {"form": "ONE_YEAR_DRAFT_ROOKIE_YOS0_MINIMUM", "salary_function": "minimum_2021_22(0)", "screen_ceiling": 3_000_000},
        "Svi Mykhailiuk": {"form": "ONE_YEAR_FA_APPLICABLE_YOS_MINIMUM", "salary_function": "minimum_2021_22(YOS_Svi)", "screen_ceiling": 3_000_000},
        "Sam Dekker": {"form": "ONE_YEAR_FA_APPLICABLE_YOS_MINIMUM_FOREIGN_RELEASE_CONDITION", "salary_function": "minimum_2021_22(YOS_Dekker)", "screen_ceiling": 3_000_000},
    }
    require(set(offers) <= set(standard) and set(incoming) <= set(standard), "Offer or incoming actor not registered")
    categories = {
        "live_original_contract_public_cap_points": {"names": retained, "screen_upper": sum(retained.values())},
        "trade_incoming_public_cap_points": {"names": incoming, "screen_upper": sum(incoming.values()), "extra_assignment_bonus_allowed_in_selected_family": False},
        "option_and_new_agreement_conditional_ceiling": {"names": offers, "screen_upper": sum(v.get("public_point", v.get("screen_ceiling", 0)) for v in offers.values())},
        "three_releases_full_remaining_salary_screen": {"names": dead_upper, "screen_upper": sum(dead_upper.values()), "protection_zero_inferred": False},
        "disqualified_Harris_and_two_way": {"Harris_new_2021_22_UPC": False, "two_way_players": tw, "normal_and_apron_TeamSalary_selected_increment": 0, "actual_stipend_or_prior_liability_zero_certified": False},
        "FA_unsigned_and_exception_state": {"Lowry_hold_resolved_by_selected_sign_and_trade": True, "other_expired_FA_rights_renounced_or_signed_before_opening": True, "new_NTMLE_or_BAE_used": False, "first_RSC_hold_replaced_when_signed": True, "selected_increment": 0, "actual_private_ledger_zero_certified": False},
    }
    total = sum(x.get("screen_upper", x.get("normal_and_apron_TeamSalary_selected_increment", x.get("selected_increment", 0))) for x in categories.values())
    require(total == WANTED_COST_UPPER, "Six-category selected public ceiling changed")
    return {"categories": categories, "conditional_named_public_upper": total, "normal_and_apron_same_screen_after_named_signings": True,
            "legal_inputs_for_screen": ["operative #8 100% scale <= 8m", "each named applicable minimum charge <= 3m", "no bonus beyond public current contract cap points", "Lowry sign-and-trade and all listed contracts/renunciations lawfully effective", "three releases retain at most original full current salary each"],
            "current_NBA_TeamSalary_upper_certified": False, "private_unknown_residual_gamma": None, "Toronto_receives_not_S_and_T_player": True, "Toronto_new_NTMLE_BAE_hardcap_trigger": False,
            "Miami_receives_S_and_T_and_must_independently_match_and_obey_apron": True, "MIA_whole_cost_certified": False}


def selected_role(cap, standard, tw):
    rows = [r for r in cap["rows"] if r["path"] == "T1" and r["availability_parameter"] == "SIAKAM_AVAILABLE"]
    require(len(rows) == 1, "T1 available capacity missing")
    source = rows[0]
    require(source["inactive"] == ["Dalano Banton", "Sam Dekker", "Isaac Bonga"] and "Isaac Bonga" not in source["player_seconds"], "Bonga was not a zero-minute inactive slot")
    row = copy.deepcopy(source)
    row["standard"] = standard
    row["two_way"] = tw
    row["inactive"] = ["Dalano Banton", "Sam Dekker", "Aron Baynes"]
    row["working_active_nomination_eligible"] = row["active"]
    row["reserve_zero_clinical_status"].pop("Isaac Bonga")
    row["reserve_zero_clinical_status"]["Aron Baynes"] = None
    row["actual_medical_status"].pop("Isaac Bonga")
    row["actual_medical_status"]["Aron Baynes"] = None
    row["source_capacity_variant"] = "T1_LOWRY_DIRECTION_WITH_BAYNES_RETAINED_INSTEAD_OF_UNRESOLVED_BONGA"
    row["working_health_selection"] = "SIAKAM_MODELED_AVAILABLE_CONTACT_HISTORY_NOT_COPIED"
    row["required_legal_and_economic_inputs"] = ["Lowry/MIA sign-and-trade complete atom and receiving MIA matching/apron", "Baynes live original contract retained; Bembry/Watson/Gillespie releases and protected charge", "Powell Toronto player option; Birch/minimum/DB1 rookie and two-way agreements", "Dekker foreign obligation lawfully resolved before one-year agreement"]
    require(len(row["active"]) == 12 and len(row["inactive"]) == 3 and set(row["active"] + row["inactive"]) == set(standard), "12+3 nomination differs from chosen roster")
    require(len(row["blocks"]) == 12 and all(len(set(b["positions"].values())) == 5 for b in row["blocks"]), "Original role block invalid")
    require(sum(row["player_seconds"].values()) == 14_400 and row["total_team_seconds"] == 14_400, "Toronto clock changed")
    require(set(row["player_seconds"]) <= set(row["active"]) and not set(row["player_seconds"]) & {"Kyle Lowry", "Isaac Bonga", "Aron Baynes"}, "Unauthorized player in selected minutes")
    return row


def build(root=ROOT):
    bank, cap, health, calendar = sources(root)
    standard, tw = selected_names(bank)
    role = selected_role(cap, standard, tw)
    cost = cost_family(bank, standard, tw)
    old = {r["name"]: r["reported_current_cap_hit"] for r in bank["live_original_contract_ports"]}
    expected_standard = ["Aron Baynes" if n == "Isaac Bonga" else n for n in bank["operating_paths"]["T1"]["standard"]]
    require(standard == expected_standard and tw == bank["operating_paths"]["T1"]["two_way"], "Returned roster differs from selected source variation")
    source_role = next(r for r in cap["rows"] if r["path"] == "T1" and r["availability_parameter"] == "SIAKAM_AVAILABLE")
    require(role["blocks"] == source_role["blocks"] and role["player_seconds"] == source_role["player_seconds"], "Returned positive role or actor differs from physical T1 capacity")
    require(role["active"] == source_role["active"] and role["inactive"] == ["Aron Baynes" if n == "Isaac Bonga" else n for n in source_role["inactive"]], "Returned active/inactive variation changed")
    categories = cost["categories"]
    expected_live = {n: old[n] for n in standard if n in old}
    expected_incoming = {"Goran Dragic": 19440000, "Precious Achiuwa": 2711280}
    for key, names in [("live_original_contract_public_cap_points", expected_live), ("trade_incoming_public_cap_points", expected_incoming), ("three_releases_full_remaining_salary_screen", {n: old[n] for n in REMOVED})]:
        require(categories[key]["names"] == names and categories[key]["screen_upper"] == sum(names.values()), "Returned named category or subtotal differs from physical public sources: " + key)
    require(not cost["current_NBA_TeamSalary_upper_certified"] and cost["private_unknown_residual_gamma"] is None and not cost["MIA_whole_cost_certified"], "Returned conditional screen falsely promoted to whole legal cost")
    require(cost["categories"]["three_releases_full_remaining_salary_screen"]["screen_upper"] == sum(old[n] for n in REMOVED), "Returned protected-release upper differs from physical old contracts")
    require(cost["conditional_named_public_upper"] == sum(c.get("screen_upper", c.get("normal_and_apron_TeamSalary_selected_increment", c.get("selected_increment", 0))) for c in cost["categories"].values()), "Returned six-category upper differs")
    games = {r["game_id"]: r for r in calendar if r["game_id"] in GAME_IDS and r["opponent"] == "TOR"}
    selected = {r["game_id"]: r for r in health["selected_dates"] if r["game_id"] in GAME_IDS}
    require(set(games) == set(selected) == set(GAME_IDS), "Four Chicago–Toronto dates not source-bound")
    dated = []
    for gid in GAME_IDS:
        game, chi = games[gid], selected[gid]
        require((game["date"], game["home"], game["away"]) == (chi["date"], chi["home"], chi["away"]), "CHI/TOR date or teams differ")
        require(chi["selected_chicago_state"] in ("COBY_OUT", "NORMAL"), "Chicago state not selected")
        dated.append({"game_id": gid, "date": game["date"], "home": game["home"], "away": game["away"], "Chicago_selected_state": chi["selected_chicago_state"], "Toronto_selected_role_variant": role["source_capacity_variant"], "Toronto_selected_working_availability": role["working_health_selection"], "Toronto_regulation_player_seconds": copy.deepcopy(role["player_seconds"]), "Toronto_blocks": copy.deepcopy(role["blocks"]), "Toronto_team_seconds": 14_400, "Chicago_source_pointer": chi["selected_carrier_source"], "historical_OT_diagnostic": game["inferred_historical_ot"] == "1", "new_OT_selected": False, "score": None, "winner": None, "actual_game_roster_or_medical_certified": False})
    return {"schema": 1, "status": "AUTHOR_DELEGATED_NPC_T1_LOWRY_DIRECTION_AND_FOUR_TOR_WORKING_CLOCKS_SELECTED_WITH_CONDITIONAL_LEGAL_COST_INPUTS", "source_sha256": {**PINS, SELF: sha(root / SELF)}, "source_hash_method": "UTF8_BOM_STRIPPED_LF_SHA256", "selected_transaction_atom": {"path": "T1_LOWRY_TO_MIA_DRAGIC_PRECIOUS_TO_TOR", "chosen_as_routine_fictional_NPC_direction": True, "NBA2021_offseason_action_order": ["Miami exercises Dragic live option before assignment", "Toronto/Miami use one consented Lowry sign-and-trade with Dragic and Precious incoming", "Toronto retains Powell by timely original player option and Baynes by live original contract; three other live contracts released with protected costs preserved", "Toronto signs source-named Birch, Giddey, Banton, Svi, Dekker, Hauser and Champagnie under stated lawful forms"], "Lowry_first_year_price": "CONDITIONAL_PUBLIC_TRADE_COMPARATOR_NOT_PRIVATE_UPC", "actual_party_consent_or_league_receipt_certified": False, "Miami_match_and_apron_condition": "MIA_receiving_S_and_T_whole_family_must_pass_before_transaction_is_executed", "Powell_original_POR_trade_reinstated": False, "Bonga_WAS_draft_right_acquired": False, "Baynes_original_waiver_adopted": False, "future_Dragic_to_SAS_Young_to_TOR_trade_adopted": False, "Chicago_M1_A_and_S2_picks_changed": False}, "selected_roster": {"standard": standard, "two_way": tw, "standard_count": 15, "two_way_count": 2, "active": role["active"], "inactive": role["inactive"], "actual_registration_certified": False}, "selected_cost_screen": cost, "selected_role": role, "Chicago_Toronto_dates": dated, "date_count": 4, "Toronto_conditional_role_function_selected": True, "original_2020_21_minutes_carried_forward": False, "Toronto_full_82_dates_or_results_selected": False, "MIA_downstream_date_roster_updated_here": False, "remaining_typed_inputs": ["MIA whole receiving S&T matching/apron and named post-atom roster", "operative legal #8 scale/minimum charges and any public-contract bonus/assignment revisions beyond conditional screen", "TOR/MIA other opponents' dated availability and any actual overtime/results"], "author_lock": False, "whole_macro3_G13_G14_complete": False, "manuscript_allowed": False, "freeze": "v0.30 PARTIAL / CLOSED"}


def validate(value, root=ROOT):
    try:
        require(value == build(root), "Selected Toronto packet differs from source-bound construction")
        return []
    except (ValueError, KeyError, TypeError) as exc:
        return [str(exc)]


def markdown(value):
    rows = ["# Toronto 2021–22 T1 명명 운영 선택", "", "Lowry→Miami, Dragic·Precious→Toronto의 **가상 NPC 루틴 방향**을 선택한다. Chicago M1/A·S2와 Powell Toronto 잔류는 유지한다. 개인 계약 접수/리그 등록·실제 경기 결과는 인증하지 않는다.", "", "## 원자 행동·명단", "", "원 Miami Dragic 옵션 행사→한 Lowry 사인 앤 트레이드→Toronto 수취를 한 거래로 묶고 Miami의 수취 구단 매칭·apron을 별도 적법조건으로 둔다. 원 Portland Powell 거래는 불성립, Powell은 Toronto 기존 옵션을 적기에 행사하는 가상선택이다. Bonga의 WAS 미서명 권리를 새 Toronto 계약으로 건너뛰지 않는다. 대신 기존 live Baynes 계약을 유지하고 Bembry·Watson·Gillespie 세 선수만 방출하여 15STD+2TW를 이룬다. 보호급여는 삭제하지 않는다.", "", "양수 11명의 T1 기존 12×240초 배치는 보존한다. Baynes는 Bonga가 차지하던 0분 inactive 자리이며 0분은 건강 진단이 아니다. Siakam은 원 May8 접촉·수술의 대체세계 재발을 자동 복사하지 않는 **가상 작업 가용** 선택이다. 실제 임상 완치 주장이 아니다.", "", "| Chicago 상대 | 선택된 CHI 상태 | Toronto 분 | 원역사 OT 진단 | 대체 결과 |", "|---|---|---:|---|---|"]
    for r in value["Chicago_Toronto_dates"]:
        rows.append(f"| {r['date']} `{r['game_id']}` | {r['Chicago_selected_state']} | 240 | {'있음' if r['historical_OT_diagnostic'] else '없음'} | 미선택 |")
    rows += ["", "## 이름 있는 여섯 비용 범주", "", "기존 Toronto 원계약 명명점, Dragic·Precious 공개 cap점, Powell 옵션·최저급/신인스케일 **함수**, 세 방출의 원급여 전액 보수 상한, Harris/TW, 잔여 FA·지명권·예외를 따로 합산한다. Baynes 7.35m은 live에 포함된다. 선택된 조건은 Birch/Banton/Svi/Dekker 각 최저급 charge≤3m, #8 신인 100% scale≤8m, 추가 보너스·예외 없음이다. 이 넓은 조건부 공개 screen 상단은 **$145,895,320**이다. 정확 법정 scale 반올림/비공개 보너스·과거잔액을 0으로 증명한 NBA 전체 Team Salary 상단이 아니며, 해당 조건이 벗어나면 재산출한다.", "", "Toronto가 Dragic·Precious를 받는다고 *수취 S&T* hard cap을 Toronto에 잘못 부과하지 않는다. Lowry를 받는 Miami의 whole matching/apron은 거래 실행 전 별도 남은 입력이다. 실제 Lowry·신인·최저급 계약 수락/영수증을 인증하지 않는다.", "", "## 범위", "", "10/25·1/26·2/3·3/21 네 Chicago 상대 역할시계만 묶었다. 2/3 원역사 연장 진단은 대체 연장 선택이 아니며 점수/승패는 모두 null이다. Dragic→Spurs/Young→Toronto의 후속 원거래도 Chicago Young 잔류와 충돌하므로 자동 이월하지 않는다. 전체 Toronto 82일 건강·Miami 후손·리그 결과·G13/G14·원고는 완료가 아니다.", "", "## 7행 진행", "", "1. 이전 완료 지점 보존", "2. 2020–21 S2 완료", "3. Toronto T1 네 날짜 명명 역할·조건부 비용 가족 선택; Miami 법적 원자 후손 미완", "4. NBA 장기 커리어 후속 미완", "5. 전체 G13 미완", "6. 실제 Pack0·게이트 CLOSED", "7. 통합·독립 검문·최종 승인 미완", "", "[선택 데이터](TORONTO_2021_SELECTED_T1_OPERATING_FAMILY_2026_10_07.json) · 원고0 · v0.30 PARTIAL."]
    return "\n".join(rows) + "\n"


def self_test(root=ROOT):
    original = selected_names
    def wrong_actor(bank):
        std, tw = original(bank)
        return ["Isaac Bonga" if n == "Aron Baynes" else n for n in std], tw
    with patch(__name__ + ".selected_names", side_effect=wrong_actor):
        try:
            build(root)
        except ValueError:
            name_rejected = True
        else:
            name_rejected = False
    require(name_rejected, "Unresolved Bonga registration falsely accepted")
    original_cost = cost_family
    def bad_cost(bank, standard, tw):
        item = original_cost(bank, standard, tw)
        item["categories"]["three_releases_full_remaining_salary_screen"]["screen_upper"] = 0
        return item
    with patch(__name__ + ".cost_family", side_effect=bad_cost):
        try:
            build(root)
        except ValueError:
            cost_rejected = True
        else:
            cost_rejected = False
    require(cost_rejected, "Protected salary omission falsely accepted")
    return ["Bonga_unresolved_slot_rejected", "protected_cost_omission_rejected"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    value = build()
    if args.write:
        (ROOT / OUT).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (ROOT / MD).write_text(markdown(value), encoding="utf-8")
    if args.check:
        saved = load_json(ROOT, OUT)
        require(not validate(saved), "Saved selected TOR packet stale")
        require((ROOT / MD).read_text(encoding="utf-8-sig").replace("\r\n", "\n") == markdown(saved), "Selected TOR MD stale")
    tests = self_test() if args.self_test else []
    print(json.dumps({"current": True, "dates": value["date_count"], "standard": 15, "two_way": 2, "public_screen_upper": value["selected_cost_screen"]["conditional_named_public_upper"], "self_controls": tests}, ensure_ascii=False))


if __name__ == "__main__":
    main()
