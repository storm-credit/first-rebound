"""Join the reviewed AP1/SG16 T1 candidate to its draft and cost sources.

This prepares a root-reviewable fictional NPC operating selection. It does not
certify consent, receipts, all draft choices, or a new author lock.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_2021_pick16_t1_operating_family.py"
OUT = "research/NBA_2021_PICK16_T1_OPERATING_FAMILY_2026_10_07.json"
MD = OUT.replace(".json", ".md")
WORKING = "research/NBA_2021_PICK16_BOS_OKC_HOU_WORKING_EXECUTION_2026_10_07.json"
COST = "research/NBA_2021_PICK16_COST_CLOSURE_BRIDGE_2026_10_07.json"
OKC = "research/OKC_2021_AP1_FULL_COST_FAMILY_2026_10_07.json"
BOARD = "research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json"
SEASON = "simulation/NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json"
M1 = "canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json"
A = "canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json"
DECISION = "design/NBA_2021_PICK16_AP1_SG16_DIRECTION_DECISION_PACKET_2026_10_07.md"
PINS = {
    WORKING: "86b9989daa20eced72106c25b14fb8d8b3b32d201132a0b87ba466b0ce51fba0",
    COST: "e1a9809fabcf4a63b703479df8eeb0fc9db615670e23a24f5f61f707003c37b1",
    OKC: "0f1b2c384be7043f6bacecf336d925a2905bc1ca8a07b7089ba350d481b8acb0",
    BOARD: "90099928f9133c4087ee7871939ce58216d183bd186f5ebd3575a56c2348eeed",
    SEASON: "3e35fd2abfeb32e2bc5b66b7796f843ca117359be1a419d037844d29177a26d8",
    M1: "253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088",
    A: "9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce",
    DECISION: "4c39cb640c607accda1fd0063c5f28c93e6ed654e21ff52c92734429fff4a839",
}
EXPECTED_AP1 = (
    ("STANDARD_CONTRACT", "Kemba Walker", "BOS", "OKC"),
    ("STANDARD_CONTRACT", "Al Horford", "OKC", "BOS"),
    ("STANDARD_CONTRACT", "Moses Brown", "OKC", "BOS"),
    ("CURRENT_FIRST_SELECTION", "BOS_2021_16", "BOS", "OKC"),
    ("CONDITIONAL_SECOND_CLAIM", "EARLIER_BOS_MEM_2025_2R", "BOS", "OKC"),
    ("CONDITIONAL_SECOND_CLAIM", "LATEST_OKC_WAS_EARLIER_DAL_MIA_2023_2R", "OKC", "BOS"),
)
EXPECTED_SG16 = (
    ("UNSIGNED_DRAFT_RIGHTS", "BOS_2021_16:Alperen Sengun", "OKC", "HOU"),
    ("PRESERVED_CONDITIONAL_FIRST_CLAIM", "DET_FIRST_OR_2027_SECOND", "HOU", "OKC"),
    ("PRESERVED_CONDITIONAL_FIRST_CLAIM", "WAS_FIRST_OR_2026_2027_SECONDS", "HOU", "OKC"),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def normalized_sha(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")).hexdigest()


def load_json(root: Path, relative: str):
    return json.loads((root / relative).read_text(encoding="utf-8-sig"))


def sources(root: Path):
    for relative, expected in PINS.items():
        require(normalized_sha(root / relative) == expected, "Source changed: " + relative)
    loaded = {relative: load_json(root, relative) for relative in PINS if relative.endswith(".json")}
    for relative, value in loaded.items():
        require(value == json.loads((root / relative).read_text(encoding="utf-8-sig")), "Loaded source differs from physical file: " + relative)
    return loaded


def edges(event):
    return tuple((e["kind"], e["asset"], e["from"], e["to"]) for e in event["edges"])


def build(root: Path = ROOT):
    s = sources(root)
    w, cost, okc, board, season, m1, a = (s[x] for x in (WORKING, COST, OKC, BOARD, SEASON, M1, A))
    require(w["independent_review_completed"] is True and cost["independent_review_completed"] is True, "Reviewed ancestor missing")
    require(len(w["events"]) == 2 and cost["candidate_events"] == w["events"], "AP1/SG16 source event mismatch")
    ap1, sg16 = w["events"]
    require(all(edge.get("event") == parent["id"] for parent in (ap1, sg16) for edge in parent["edges"]), "Atomic child event differs from parent event identity")
    require((ap1["id"], ap1["date"], ap1["atomic"], edges(ap1)) == ("AP1", "2021-07-28", True, EXPECTED_AP1), "AP1 actors or rights differ")
    require((sg16["id"], sg16["date"], sg16["atomic"], edges(sg16)) == ("SG16", "2021-07-29", True, EXPECTED_SG16), "SG16 actors or rights differ")
    require(sg16["requires_available_draftee"] == "Alperen Sengun" and sg16["rights_selected_but_unsigned_in_this_candidate"] is True, "SG16 selection/tender boundary differs")
    cal = w["calendar"]
    require(cal["original_AP1_announcement_date"] == "2021-06-18" and cal["source_date_not_copied_into_macro2"] is True, "Historical AP1 announcement misdated")
    require(cal["salary_cap_year"] == "2020-21" and cal["new_salary_cap_year_start"] == "2021-08-03" and cal["apron_usd"] == 138928000, "Old-year legal window differs")
    require(w["summary"]["conditional_control_matches_G7"] == 60 and len(w["draft_control_candidate_rows"]) == 60, "Control60 incomplete")
    require(season["summary"]["frozen_control_rows"] == 60 and season["authority"]["new_transaction_or_draftee_selection"] is False, "Frozen season control not preserved")
    require(m1["selected"]["route"] == "M1" and a["selected"]["route"] == "G1A_PLUS_M1", "Approved Chicago direction changed")
    require(all(e["from"] != "CHI" and e["to"] != "CHI" for event in w["events"] for e in event["edges"]), "T1 unexpectedly changes Chicago assets")
    require(board["policy"]["conditional_asset_scenario"] == "T1_AP1_AND_SG16" and board["policy"]["AP1_direction_author_selected"] is False, "Board scenario/source authority differs")
    rows = board["rows"]
    require(len(rows) == 60 and len({r["pick"] for r in rows}) == 60 and len({r["player"] for r in rows}) == 60, "Candidate board control/identity mismatch")
    pick16 = next(r for r in rows if r["pick"] == 16)
    require((pick16["origin"], pick16["conditional_holder_at_selection"], pick16["selecting_team"], pick16["conditional_final_draft_rights_holder"], pick16["player"], pick16["available_when_selected_in_this_board"]) == ("BOS", "OKC", "OKC", "HOU", "Alperen Sengun", True), "Candidate #16 holder/availability differs")
    require(sum(r["player"] == "Alperen Sengun" for r in rows[:15]) == 0 and board["summary"]["Sengun_pre16_consumption"] == 0, "Candidate Sengun pre16 collision")
    candidate16 = next(r for r in w["draft_control_candidate_rows"] if r["pick"] == 16)
    require((candidate16["frozen_macro2_holder"], candidate16["conditional_after_AP1_holder"], candidate16["conditional_after_SG16_holder"], candidate16["draftee"]) == ("BOS", "OKC", "HOU", "Alperen Sengun"), "G7 #16 control source differs")
    require(board["summary"]["other_unselected_candidate_rows"] == 58 and board["summary"]["new_NBA_UPCs_or_Tenders"] == 0, "Other board candidates promoted")
    budget = cost["budget"]
    require((budget["cap_year"], budget["apron_usd"], budget["BOS_after_AP1_upper_usd"], budget["OKC_before_AP1_upper_usd"], budget["OKC_after_AP1_upper_usd"], budget["HOU_unsigned_rights_apron_delta_usd"]) == ("2020-21", 138928000, 133457706, 129697595, 134956131, 0), "Public old-year cost family differs")
    require(budget["BOS_apron_margin_usd"] == 138928000 - 133457706 and budget["OKC_apron_margin_usd"] == 138928000 - 134956131, "Public apron margin differs")
    require(okc["arithmetic"]["post_AP1_apron_upper_usd"] == budget["OKC_after_AP1_upper_usd"] and okc["lawful_family"]["whole_cost_candidate_pass"] is True, "OKC reviewed cost not consumed")
    match = cost["matching_and_asset_evidence"]
    require((match["three_actors_nine_edges_and_control60"], match["Brown_q_min_usd"], match["Brown_q_max_usd"], match["all_existing_bonus_branches_use_proposed_consensual_waivers"], match["future_protected_DET_WAS_claims_unchanged"]) == (True, 423280, 1701593, True, True), "Matching or protected claims differ")
    require(budget["HOU_SG16_working_instant_before_first_RequiredTender"] is True and budget["HOU_new_RequiredFirstTender_outstanding_at_SG16"] is False, "Tender-cost ordering changed")
    require(w["authority"]["actual_contract_amendment_or_consent_certified"] is False and not cost["whole_actual_legal_or_registration_certified"], "Private consent certified without evidence")
    result = {
        "schema": "PICK16_T1_REVIEWABLE_ROUTINE_OPERATING_FAMILY_V1",
        "status": "ROOT_REVIEWABLE_T1_ROUTINE_DIRECTION_NOT_CANON_OR_ACTUAL_RECEIPT",
        "source_hash_method": "UTF8_LF_SHA256",
        "source_sha256": dict(PINS),
        "self_sha256": normalized_sha(root / SELF),
        "authority": {"approved_Chicago_M1_A_preserved": True, "frozen_macro2_S2_preserved": True, "new_human_question_required_by_unselected_label_alone": False, "root_routine_selection_recorded_by_this_file": False, "new_author_lock": False, "macro3_whole_complete": False, "manuscript_allowed": False},
        "working_order": [
            {"date": "2021-07-28", "step": "AP1", "atomic_edges": ap1["edges"], "predecessor": "frozen BOS #16 and BOS/OKC current contracts and conditional seconds", "old_salary_cap_year": "2020-21"},
            {"date": "2021-07-29", "step": "SELECT16", "selector": "OKC", "player": "Alperen Sengun", "candidate_board_available": True, "other_58_author_selected": False, "selection_actual_receipt_certified": False},
            {"date": "2021-07-29", "step": "SG16", "atomic_edges": sg16["edges"], "predecessor": "OKC selected #16; no new rookie UPC or outstanding RequiredFirstTender", "old_salary_cap_year": "2020-21"},
        ],
        "after_candidate": {"BOS": {"incoming_contracts": ["Al Horford", "Moses Brown"], "outgoing_contract": "Kemba Walker", "rights_from_OKC": "LATEST_OKC_WAS_EARLIER_DAL_MIA_2023_2R"}, "OKC": {"incoming_contract": "Kemba Walker", "incoming_claims": ["EARLIER_BOS_MEM_2025_2R", "DET_FIRST_OR_2027_SECOND", "WAS_FIRST_OR_2026_2027_SECONDS"], "outgoing_contracts": ["Al Horford", "Moses Brown"], "selected16_rights_outgoing_to_HOU": True}, "HOU": {"incoming_unsigned_rights": "BOS_2021_16:Alperen Sengun", "outgoing_preserved_claims": ["DET_FIRST_OR_2027_SECOND", "WAS_FIRST_OR_2026_2027_SECONDS"], "new_UPC_or_tender_at_atomic_instant": False}},
        "public_cost_family": {"apron_usd": 138928000, "BOS_upper_after_AP1_usd": budget["BOS_after_AP1_upper_usd"], "BOS_margin_usd": budget["BOS_apron_margin_usd"], "OKC_upper_after_AP1_usd": budget["OKC_after_AP1_upper_usd"], "OKC_margin_usd": budget["OKC_apron_margin_usd"], "HOU_SG16_unsigned_rights_apron_delta_usd": 0, "Brown_future_protection_q_interval_usd": [423280, 1701593], "bonus_waivers": "CONSENSUAL_IF_APPLICABLE_NOT_ACTUAL_RECEIPT", "future_tender_or_UPC_reopens_cost": True, "Aug3_new_cap_year_auto_carry": False},
        "candidate_board_scope": {"control_rows": 60, "pick16_board_available": True, "other_58_draftees_author_selected": False, "actual_counterfactual_participation_certified": False, "other_58_player_duplicate_count_in_candidate_board": 0},
        "collision_review": {"approved_CHI_asset_edge_conflict": False, "approved_M1_A_role_or_salary_modified": False, "macro2_June18_retroactivity": False, "NBA_opponent_future_rights_and_roles_changed": True, "later_BOS_OKC_HOU_contract_roster_and_pick_descendants_required": True},
        "exact_remaining_inputs": [
            "Root's routine T1 direction selection and conditional DB1 predecessor-draftee choice; candidate board availability is not actual draft/consent.",
            "Player/club consent and exact Brown q/bonus waiver if an actual contract execution is modeled; public cost upper is a fictional lawful family, not receipt proof.",
            "After August 3, new-year rookie tender/UPC, BOS/OKC/HOU roster/finance and protected-pick descendants require a separate dated continuation.",
        ],
        "design_gate": "CLOSED", "freeze": "v0.30 PARTIAL",
    }
    validate(result, root=root, source_bound=False)
    return result


def validate(packet, root: Path = ROOT, source_bound: bool = True):
    require(packet["self_sha256"] == normalized_sha(root / SELF), "Producer changed")
    require(packet["source_sha256"] == PINS, "Source pin set changed")
    require(packet["authority"]["new_author_lock"] is False and packet["authority"]["manuscript_allowed"] is False, "False authority promotion")
    require(packet["candidate_board_scope"]["other_58_draftees_author_selected"] is False, "58 other candidates promoted")
    require(packet["public_cost_family"]["future_tender_or_UPC_reopens_cost"] is True and packet["public_cost_family"]["Aug3_new_cap_year_auto_carry"] is False, "Old-year boundary promoted")
    require(packet["after_candidate"]["HOU"]["new_UPC_or_tender_at_atomic_instant"] is False, "Unsigned right promoted to contract")
    require(packet["working_order"][0]["atomic_edges"] and len(packet["working_order"][0]["atomic_edges"]) == 6 and len(packet["working_order"][2]["atomic_edges"]) == 3, "Atomic edges incomplete")
    if source_bound:
        require(packet == build(root), "Saved output differs from source-bound reconstruction")
    return []


def render(packet):
    b = packet["public_cost_family"]
    return "\n".join([
        "# 2021 #16 AP1·SG16 T1 루틴 실행 가족", "",
        "**Root 검토용 실행 가족. 정본 선택·현실 접수·새 작가 잠금 아님.** 승인된 Chicago M1/A와 2020–21 S2를 보존한다.", "",
        "## 원자적 순서와 권리", "",
        "| 후보 시점 | 필요한 동작 | 경계 |", "|---|---|---|",
        "| 2021-07-28 | BOS↔OKC AP1: Walker·Horford·Moses Brown, BOS #16과 두 조건부 2R 청구를 6개 원자 edge로 이동 | 실제 6/18 발표를 완료된 시즌에 소급하지 않음 |",
        "| 2021-07-29 | OKC가 후보 보드에서 #16 Sengun 선택 | 선행 15명 중 Sengun 중복 0; 다른 58명 실제 지명·참가 미확정 |",
        "| 2021-07-29 | OKC→HOU 미서명 #16 권리, HOU→OKC 기존 DET/WAS 보호 청구를 3개 edge로 이동 | UPC·RequiredTender 전 순간만; 이후 비용 재검문 |",
        "", "선수·권리 수령자는 `after_candidate`에 분리했고, DET/WAS 원보호·전환 조건은 유지한다. 이 T1은 Chicago의 기존 선수·급여·지명권을 이동시키지 않는다. BOS/OKC/HOU의 후년 계약·픽·역할에는 실질적인 변경이 생기므로 후속 원장에 연결해야 한다.", "",
        "## 공개 old-year 비용 가족", "",
        f"2020–21 apron ${b['apron_usd']:,}; AP1 후보 후 BOS 상단 ${b['BOS_upper_after_AP1_usd']:,} (여유 ${b['BOS_margin_usd']:,}), OKC 상단 ${b['OKC_upper_after_AP1_usd']:,} (여유 ${b['OKC_margin_usd']:,}). Brown 보호 q 범위 ${b['Brown_future_protection_q_interval_usd'][0]:,}–${b['Brown_future_protection_q_interval_usd'][1]:,}. Walker와 필요한 경우 Brown의 원보너스는 자발적 면제 후보이지 실제 서명이 아니다. HOU 미서명 권리 원자이동의 당해 apron 증분은 0이고, Tender·UPC가 생기면 재계산한다. 2021-08-03 이후 capyear에 이 숫자를 자동 이월하지 않는다.", "",
        "## 실제 남은 입력 3개", "",
        *[f"{i}. {item}" for i, item in enumerate(packet["exact_remaining_inputs"], 1)], "",
        "법적 준비·후보보드와 실제 거래 승낙·원장 접수를 구분한다. Freeze v0.30 PARTIAL, 설계/원고 게이트 CLOSED, 원고 0.", "",
    ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    packet = build()
    if args.write:
        (ROOT / OUT).write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (ROOT / MD).write_text(render(packet), encoding="utf-8")
    if args.check:
        saved = load_json(ROOT, OUT)
        validate(saved)
        require((ROOT / MD).read_text(encoding="utf-8") == render(saved), "MD differs from JSON")
    if args.self_test:
        changed = json.loads(json.dumps(packet))
        changed["public_cost_family"]["future_tender_or_UPC_reopens_cost"] = False
        try:
            validate(changed)
        except ValueError:
            pass
        else:
            raise AssertionError("Tender-cost negative control accepted")
        changed = json.loads(json.dumps(packet))
        changed["working_order"][0]["atomic_edges"][0]["to"] = "HOU"
        try:
            validate(changed)
        except ValueError:
            pass
        else:
            raise AssertionError("Wrong asset receiver accepted")
    print("PASS T1 working events=2 edges=9 control=60, board58 unselected, public apron BOS/OKC margins", packet["public_cost_family"]["BOS_margin_usd"], packet["public_cost_family"]["OKC_margin_usd"])


if __name__ == "__main__":
    main()
