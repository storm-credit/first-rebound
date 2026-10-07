"""Source-bound bounded 2021–22 opening operation after selected T1.

Select Houston's two named first-round rookie signings as a fictional routine
contract family. BOS/OKC/HOU reports through first Chicago meetings remain
typed inputs until their atomic contracts, rights and costs are resolved.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_bos_okc_hou_2021_post_t1_intervals.py"
OUT = "research/BOS_OKC_HOU_2021_POST_T1_OPENING_INTERVALS_2026_10_07.json"
MD = OUT.replace(".json", ".md")
SELECTED = "simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json"
WORKING = "research/NBA_2021_PICK16_BOS_OKC_HOU_WORKING_EXECUTION_2026_10_07.json"
SCOPE = "design/CHICAGO_2021_22_OPPONENT_FINITE_DISPATCH_SCOPE_2026_10_07.json"
CALENDAR = "simulation/CHICAGO_2021_22_CALENDAR.csv"
CBA = Path("C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf")
PINS = {
    SELECTED: "f8c78e99cce1b02a051c94339b550fdb52205d3988db8bbe69b780559c3bc306",
    WORKING: "86b9989daa20eced72106c25b14fb8d8b3b32d201132a0b87ba466b0ce51fba0",
    SCOPE: "a57bec4bc61e2bf2030ebc25f800f06e2c64cd86e9ed573a2ccc4c4d958af203",
    CALENDAR: "c59ea19a5515d64ed03cae8e0481847b6572d4087bbcefef15896bb7a2489183",
}
CBA_SHA = "66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a"
CBA_PAGE_TEXT_SHA = {
    84: "00b16f51fee21ba4893fef9ac2baedf8e56c2cfe02b28e027742b3941e51357d",
    85: "6effe0b5d5b2bff97c84c942c9f02fe945eccfc6e733c8e46cbd2784c6011bc7",
    292: "2ed44d760dbba5187d614c95001dfb164deb4a368ddcbc5fdbdcb8964dfcbda6",
    293: "f56e14e36fa254d1265bd51ec7b1930df33d4280181cf76fa5fc65d6c90a3464",
    294: "17a15e17207724b7bd9314d9fd2276e8a52d3460d6c062e5641d4fb682a900f7",
    295: "a2986cbc32e01c65a10496c1f4e8a1360dbd5a538f5ef19b5d516e16f7d80d2c",
}
FIRST_CHI = {"BOS": ("2021-11-01", "0022100098"), "HOU": ("2021-11-24", "0022100271"), "OKC": ("2022-01-24", "0022100730")}
SELECTED_SIGNINGS = (("2021-08-04", "jalen-green", "Signing 1042544", 2, "Jalen Green"), ("2021-08-06", "alperen-sengun", "Signing 1042640", 16, "Alperen Sengun"))


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def normalized_sha(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")).hexdigest()


def load(root: Path, relative: str):
    return json.loads((root / relative).read_text(encoding="utf-8-sig"))


def verify_cba_pages():
    """Bind legal claims to the cached original PDF and its relevant printed text."""
    page_text = {}
    for page, expected in CBA_PAGE_TEXT_SHA.items():
        process = subprocess.run(
            ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(CBA), "-"],
            check=True, capture_output=True,
        )
        body = process.stdout.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").rstrip("\x0c")
        require(hashlib.sha256(body.encode("utf-8")).hexdigest() == expected, f"CBA PDF page {page} text changed")
        page_text[page] = " ".join(body.split())
    require("Section 15. Moratorium Period." in page_text[84], "CBA moratorium locator changed")
    require("a First Round Pick and the Team that holds his draft rights may enter into a Rookie Scale Contract" in page_text[85], "CBA rookie moratorium exception changed")
    require("ARTICLE VIII ROOKIE SCALE" in page_text[292] and "two (2) Seasons" in page_text[292] and "a second Option in favor of the Team for the player's fourth Season" in page_text[292], "CBA rookie term or options changed")
    require("at least eighty percent (80%)" in page_text[294] and "Salary plus Unlikely Bonuses" in page_text[294] and "one hundred twenty percent (120%)" in page_text[294], "CBA rookie salary ceiling changed")
    require("protection for lack of skill and injury or illness" in page_text[294] and "not less than eighty percent" in page_text[294], "CBA rookie protection changed")
    require("second Option Year" in page_text[295] and "applicable percentage specified in the applicable Rookie Salary Scale" in page_text[295], "CBA fourth-year option terms changed")


def source_inputs(root: Path):
    for path, expected in PINS.items():
        require(normalized_sha(root / path) == expected, "Source changed: " + path)
    require(CBA.exists() and hashlib.sha256(CBA.read_bytes()).hexdigest() == CBA_SHA, "CBA source changed")
    verify_cba_pages()
    selected, working, scope = (load(root, x) for x in (SELECTED, WORKING, SCOPE))
    for path, value in ((SELECTED, selected), (WORKING, working), (SCOPE, scope)):
        require(value == json.loads((root / path).read_text(encoding="utf-8-sig")), "JSON loader differed from physical source: " + path)
    raw_path = Path(scope["raw_feed_source"]["path"])
    raw_bytes = raw_path.read_bytes()
    require(hashlib.sha256(raw_bytes).hexdigest() == scope["raw_feed_source"]["raw_sha256"], "NBA reported movement body changed")
    movement = json.loads(raw_bytes)["NBA_Player_Movement"]["rows"]
    require(len(movement) == scope["raw_feed_source"]["rows"] == 9927, "NBA report row count changed")
    import csv
    with (root / CALENDAR).open(encoding="utf-8-sig", newline="") as stream:
        calendar = list(csv.DictReader(stream))
    with (root / CALENDAR).open(encoding="utf-8-sig", newline="") as stream:
        require(calendar == list(csv.DictReader(stream)), "Calendar loader differed from physical source")
    return selected, working, scope, calendar, movement


def build(root: Path = ROOT):
    selected, working, scope, calendar, movement = source_inputs(root)
    require(selected["chosen_path"].startswith("T1_AP1_AND_SG16") and selected["summary"]["working_draft_choices"] == 60, "T1 60-choice direction changed")
    require(selected["summary"]["asset_edges"] == 9 and selected["summary"]["new_UPCs_or_RequiredTenders"] == 0, "T1 pre-rookie-contract state changed")
    require(selected["whole_macro3_or_82_game_season_complete"] is False and selected["manuscript_allowed"] is False, "Selected draft scope promoted")
    require(len(working["events"]) == 2 and [x["id"] for x in working["events"]] == ["AP1", "SG16"], "T1 asset predecessor changed")
    hou = working["dated_working_rosters"]["HOU"]
    before = hou["conditional_after_SG16"]
    require(sum(x["contract_class"] == "STANDARD" for x in before) == 15 and sum(x["contract_class"] == "TWO_WAY" for x in before) == 2, "Houston conditional pre-Aug3 roster count changed")
    require(all(x["player"] not in ("Jalen Green", "Alperen Sengun") for x in before), "Rookie already in predecessor UPC")
    require(any(x["kind"] == "UNSIGNED_DRAFT_RIGHTS" and x["asset"] == "BOS_2021_16:Alperen Sengun" and x["owner"] == "HOU" for x in selected["final_asset_ownership"]), "Sengun HOU rights missing")
    selected_rows = {x["pick"]: x for x in selected["selected_rows"]}
    require((selected_rows[2]["player"], selected_rows[2]["conditional_final_draft_rights_holder"], selected_rows[16]["player"], selected_rows[16]["conditional_final_draft_rights_holder"]) == ("Jalen Green", "HOU", "Alperen Sengun", "HOU"), "Houston rookie rights differ")
    require(all(selected_rows[p]["new_NBA_UPC_or_RequiredTender"] is False for p in (2, 16)), "Rookie contract prepaid by T1")
    first_games = {}
    reports = {}
    for team, (date, game_id) in FIRST_CHI.items():
        matches = [x for x in calendar if x["game_id"] == game_id and x["date"] == date and team in (x["home"], x["away"]) and "CHI" in (x["home"], x["away"])]
        require(len(matches) == 1, "First CHI anchor changed: " + team)
        require(not any(x["date"] < date and team in (x["home"], x["away"]) and "CHI" in (x["home"], x["away"]) for x in calendar), "Earlier CHI game omitted: " + team)
        first_games[team] = {"game_id": game_id, "date": date, "opponent": team, "historical_score_not_selected": True}
        events = scope["teams"][team]["reported_event_source"]["events"]
        filtered = []
        for event in events:
            if "2021-07-28" <= event["reported_date"] <= date:
                raw = movement[event["source_row_index"]]
                pid = int(raw["PLAYER_ID"]) if raw["PLAYER_ID"] is not None else 0
                require((raw["GroupSort"], raw["TRANSACTION_DATE"][:10], raw["Transaction_Type"], int(raw["TEAM_ID"]), pid or None, raw["PLAYER_SLUG"] or "") == (event["GroupSort"], event["reported_date"], event["transaction_type"], int(event["TEAM_ID"]), event["player_id"], event["player_slug"]), "Report/physical row mismatch")
                filtered.append(event)
        reports[team] = filtered
    selected_actions = []
    for date, slug, group, pick, name in SELECTED_SIGNINGS:
        rows = [x for x in reports["HOU"] if (x["reported_date"], x["player_slug"], x["GroupSort"], x["transaction_type"]) == (date, slug, group, "Signing")]
        require(len(rows) == 1 and selected_rows[pick]["player"] == name, "Selected Houston signing source absent")
        require(sum(raw["GroupSort"] == group for raw in movement) == 1, "Signing source group not single-player")
        selected_actions.append({
            "date": date, "reported_GroupSort": group, "source_row_index": rows[0]["source_row_index"],
            "pick": pick, "player": name, "team": "HOU", "fictional_routine_contract_event_selected": True,
            "contract_class": "STANDARD_ROOKIE_SCALE", "first_year_salary_design_family": f"[0.80*S2021_PICK_{pick}, 1.20*S2021_PICK_{pick}]",
            "selected_policy": "120_PERCENT_OF_OFFICIAL_PICK_SCALE_SUBJECT_TO_SCALE_INPUT",
            "lawful_UPC_term": {"initial_seasons": ["2021-22", "2022-23"], "third_season_team_option": "2023-24_NOT_EXERCISED", "fourth_season_team_option": "2024-25_NOT_EXERCISED", "third_and_fourth_options_separate": True},
            "scale_constraints": {"first_two_and_first_option_current_base_at_least": "80_PERCENT_OF_APPLICABLE_SCALE", "salary_plus_unlikely_bonuses_each_year_at_most": "120_PERCENT_OF_APPLICABLE_SCALE", "fourth_option_raise": "APPLICABLE_SCALE_PERCENTAGE_IF_EXERCISED", "new_signing_bonus": 0, "unlikely_bonus": 0, "loan": 0},
            "protection": {"lack_of_skill": "AT_LEAST_80_PERCENT_SCALE_FIRST_TWO_AND_FIRST_OPTION", "injury_or_illness": "AT_LEAST_80_PERCENT_SCALE_FIRST_TWO_AND_FIRST_OPTION", "fictional_selected_full_base_protection_first_two": True, "first_option_protection_if_exercised": True},
            "moratorium_rule": "2017_CBA_ARTICLE_II_SECTION_15_FIRST_ROUND_RIGHTS_HOLDER_RSC_EXCEPTION",
            "reported_calendar_day_not_exact_signing_time": True,
            "foreign_contract_obstacle_lawfully_resolved_before_UPC": True if pick == 16 else None,
            "actual_foreign_release_document_certified": False,
            "numeric_scale_amount_certified_here": False, "actual_signed_contract_or_private_receipt_certified": False,
            "actual_medical_or_clinical_certified": False,
        })
    require(len(reports["BOS"]) == 20 and len(reports["HOU"]) == 27 and len(reports["OKC"]) == 35, "First-CHI reported source range changed")
    named_followups = {}
    for label, group, expected in (
        ("BOS_MOSES_BROWN_TO_DAL_JULY31", "Trade 2020091", (("josh-richardson", 1610612738), ("moses-brown", 1610612742))),
        ("OKC_FAVORS_JULY30", "Trade 2020090", (("derrick-favors", 1610612760), ("", 1610612760), ("", 1610612762))),
        ("OKC_KEMBA_WAIVE_AUG6", "Waive 1042646", (("kemba-walker", 1610612760),)),
    ):
        group_rows = [(i, r["TRANSACTION_DATE"][:10], r["Transaction_Type"], r.get("PLAYER_SLUG") or "", int(r["TEAM_ID"])) for i, r in enumerate(movement) if r["GroupSort"] == group]
        require(tuple((slug, team_id) for _, _, _, slug, team_id in group_rows) == expected, "Named downstream raw event actor changed: " + label)
        named_followups[label] = {"GroupSort": group, "raw_rows": [{"source_row_index": i, "date": date, "type": kind, "player_slug": slug, "TEAM_ID": team_id} for i, date, kind, slug, team_id in group_rows], "selected_for_fictional_execution": False, "cost_or_counterparty_effect_certified": False}
    pending = {}
    for team, events in reports.items():
        selected_groups = {x["reported_GroupSort"] for x in selected_actions} if team == "HOU" else set()
        pending[team] = {"first_CHI_game": first_games[team], "reported_rows_after_T1_before_new_capyear_unexecuted": sum(x["reported_date"] < "2021-08-03" for x in events), "reported_rows_before_first_CHI": len(events), "selected_named_routine_signing_rows": sum(x["GroupSort"] in selected_groups for x in events), "not_executed_reported_rows": len(events) - sum(x["GroupSort"] in selected_groups for x in events), "unapplied_GroupSorts": sorted({x["GroupSort"] for x in events if x["GroupSort"] not in selected_groups}), "contract_roster_cost_interval_to_first_game_certified": False}
    return {
        "schema": "BOS_OKC_HOU_POST_T1_BOUNDED_OPENING_INTERVAL_V1",
        "status": "HOU_TWO_NAMED_ROOKIE_CONTRACT_ROUTINES_SELECTED_BOS_OKC_HOU_FIRST_CHI_INTERVAL_PENDING",
        "source_sha256": dict(PINS), "source_hash_method": "UTF8_LF_SHA256", "self_sha256": normalized_sha(root / SELF),
        "raw_feed": {"path": scope["raw_feed_source"]["path"], "sha256": scope["raw_feed_source"]["raw_sha256"], "total_rows": 9927},
        "CBA": {"path": str(CBA), "sha256": CBA_SHA, "page_text_sha256": {str(k): v for k, v in CBA_PAGE_TEXT_SHA.items()}, "page_text_method": "pdftotext_-layout_single_PDF_page_UTF8_LF_strip_final_formfeed", "rule_locator": "Article II Section 15 PDF84–85: first-round rights holder may enter Rookie Scale Contract during moratorium; Article VIII Section 1 PDF292–295: two seasons, separate third/fourth team options, scale/protection; Article VII unsigned hold is replaced by signed salary only in selected fictional family", "actual_2021_scale_table_cents_loaded": False},
        "selected_T1_source": SELECTED,
        "old_year_to_new_year_boundary": {"T1_old_year_last_atomic_date": "2021-07-29", "new_year_start": "2021-08-03", "old_year_apron_numbers_auto_carried": False, "HOU_pre_signing_conditional_carry_standard": 15, "HOU_pre_signing_conditional_carry_two_way": 2, "all_May16_contracts_proven_live_on_Aug3": False},
        "selected_named_contract_events": selected_actions,
        "named_T1_downstream_reported_events_not_yet_executed": named_followups,
        "HOU_offseason_slot_witness_if_all_old_named_retained": {"STANDARD": 17, "TWO_WAY": 2, "total_including_TW": 19, "offseason_max_including_TW": 20, "regular_season_15_STANDARD_rule_satisfied_by_this_snapshot": False, "named_hardship_Oliver_Reynolds_not_carried": True, "candidate_rookie_signed_salaries_replace_unsigned_holds": True},
        "six_cost_categories": {"existing_live_and_retained_contracts": "UNKNOWN_AFTER_AUG3", "new_selected_RSC_salary": "1.2*S2021_PICK_2 + 1.2*S2021_PICK_16", "dead_camp_grievance": "PRESERVE_UNKNOWN_NOT_ZERO", "FA_unsigned_rights": "RECOMPUTE_HOU_NEVER_ZERO_BY_ABSENCE", "tender_floor": "SIGNED_ROOKIES_REPLACE_THEIR_OWN_HOLDS_OTHER_TENDERS_UNSELECTED", "exceptions": "RECOMPUTE_NEW_YEAR", "whole_team_salary_or_apron_certified": False},
        "first_CHI_operating_interval": pending,
        "summary": {"teams": 3, "first_CHI_anchor_games": 3, "source_reported_rows_in_requested_ranges": 82, "new_selected_named_RSC_events": 2, "remaining_unexecuted_reported_rows_in_requested_ranges": 80, "full_15_plus_2_opening_teams_completed": 0, "date_intervals_to_first_CHI_fully_legal": 0, "actual_2021_22_opponent_health_or_game_result_selected": 0},
        "exact_remaining_inputs": ["Published 2021–22 #2/#16 official rookie scale cents or a clearly bounded scale interval for numeric new-year salary; the lawful RSC percentage policy is selected, actual contract paper is not a gate.", "BOS/OKC and HOU post-8/6 GroupSort counterparty/contract-class events, old-contract expiry/waive-dead-money, six new-year cost categories and final 15+2 roster by each first CHI date.", "Date-specific available 5-player role and opponent health/result choices after legal interval; historical first-CHI box score is not automatically copied."],
        "authority": {"new_human_question_required_by_NPC_unselected_label": False, "selected_routine_NPC_signing_family": True, "actual_private_contract_receipt_certified": False, "new_author_lock": False, "whole_macro3_or_2021_22_season_complete": False, "manuscript_allowed": False},
        "freeze": "v0.30 PARTIAL", "design_gate": "CLOSED",
    }


def validate(packet, root: Path = ROOT):
    require(packet == build(root), "Saved interval differs from source-bound reconstruction")
    return []


def render(p):
    return "\n".join([
        "# T1 후 BOS·OKC·HOU 첫 Chicago 경기 전 운영구간", "",
        "**HOU 1라운드 신인 서명 루틴 2건만 선택.** 나머지 계약·명단·건강·결과는 실행하지 않았다. T1의 7/28·7/29 old-year 숫자를 8/3 이후에 그대로 이월하지 않는다.", "",
        "| 첫 CHI 경기 | 원 보고행 | 이번 실행 | 미실행 원 보고행 |", "|---|---:|---:|---:|",
        *[f"| {team} {v['first_CHI_game']['date']} | {v['reported_rows_before_first_CHI']} | {v['selected_named_routine_signing_rows']} | {v['not_executed_reported_rows']} |" for team, v in p["first_CHI_operating_interval"].items()], "",
        "## 실제 줄어든 입력", "",
        "T1에서 HOU가 보유한 #2 Jalen Green과 #16 Alperen Sengun 권리를 잇고, NBA 원 보고의 8/4·8/6 서명 GroupSort를 별도 가상 루틴 계약으로 선택했다. 각자는 2021–22 해당 순번 공식 scale의 80–120% 안에서 120% 정책을 선택한다. 공식 scale 정확 달러·사적 계약서·영수증은 인증하지 않는다. 미서명 1라운드 hold를 해당 서명 급여로 교체한다.", "",
        "법적 근거는 2017 CBA Article VIII §1(PDF 292–295)의 2시즌 계약·독립적인 3/4년차 팀 옵션·연도별 Salary+Unlikely Bonuses 120% 상한·기본급/기술 부족 및 부상 보호 하한이다. 두 옵션은 아직 행사하지 않았다. 신규 보너스·대여는 0으로 선택했고, Sengun은 NBA 계약 전 해외 계약 장애가 적법하게 해소되는 조건으로만 실행했다(실제 해제 문서 인증 0). Article II §15(PDF 84–85)는 권리 보유팀의 1라운드 신인 계약을 모라토리엄 중에도 허용한다. 8/4·8/6은 보고 날짜이며 정확 서명 시각은 인증하지 않는다.", "",
        "HOU의 T1 직후 명명 carry 15STD+2TW를 전원 유지한다고 가정해도 두 신인 추가 시 17STD+2TW=19명으로 오프시즌 20명 이내다. 이것이 정규시즌 15STD+2TW 또는 실제 8/6 live roster 인증은 아니다. May16 계약 만료·타팀 이전은 후속 GroupSort/권리·비용과 함께 처리한다.", "",
        "## 비용과 후속", "",
        "6범주 중 새 신인 RSC 급여 정책만 연결했고 나머지 live/dead/FA/tender/exception은 `six_cost_categories`의 typed input이다. BOS 20·HOU 25·OKC 35 원 보고행은 미실행이며, 실제 명단·계약여부를 보고 feed에서 자동 추론하지 않는다. Kemba waive, Horford/Moses 후속과 거래 상대, HOU 15+2 정리는 다음 원자 적용대상이다.", "",
        *[f"{i}. {s}" for i, s in enumerate(p["exact_remaining_inputs"], 1)], "",
        "실제 의료·거래/계약 접수·사적 급여 인증 0, 원고 0, Freeze v0.30 PARTIAL, 설계/원고 CLOSED.", "",
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    p = build()
    if args.write:
        (ROOT / OUT).write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (ROOT / MD).write_text(render(p), encoding="utf-8")
    if args.check:
        validate(load(ROOT, OUT))
        require((ROOT / MD).read_text(encoding="utf-8") == render(load(ROOT, OUT)), "MD differs from packet")
    if args.self_test:
        q = json.loads(json.dumps(p))
        q["selected_named_contract_events"][1]["player"] = "Kemba Walker"
        try:
            validate(q)
        except ValueError:
            pass
        else:
            raise AssertionError("Sengun actor swap accepted")
    print("PASS", p["summary"])


if __name__ == "__main__":
    main()
