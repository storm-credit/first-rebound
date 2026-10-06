"""Reviewable GSW operating candidates; no transaction, contract or roster promotion."""
from pathlib import Path
from copy import deepcopy
import argparse
import hashlib
import json
import fitz

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "b48fb829756fc8c9ee943a440a13a2b2d4426d08"
SELF = "tools/build_gsw_hutchison_operating_candidates.py"
OUT = ROOT / "simulation/GSW_HUTCHISON_2018_2021_OPERATING_CANDIDATES.json"
MD = OUT.with_suffix(".md")
CACHE = Path("C:/Users/Storm Credit/AppData/Local/Temp")
NEW = CACHE / "first-rebound-gsw-hutchison-20261007"
INPUTS = [
    "control/AUTHORITY_MAP.md",
    "simulation/2018_DRAFT_22_60_REOPEN.md",
    "simulation/2018_DRAFT_28_43_EVANS_CASCADE.md",
    "simulation/2018_DRAFT_37_60_TRENT_CASCADE.md",
    "research/2018_HUTCHISON_24_28_TEAM_BOARD.md",
    "simulation/CAUSALITY_MODEL.md",
    "simulation/NBA_2021_L2_NONPLAYOFF_ROSTER_SCOPE.json",
    "simulation/NBA_2021_L2_WORKING_MINUTE_MODELS.json",
    "simulation/NBA_2021_L2_WORKING_CHRONOLOGY.json",
]
# Filled after the actual source/authority read; not dynamically accepted at build time.
REVIEWED_SHA = {'control/AUTHORITY_MAP.md': '693ee88e93614a1bcaa470747f7986d267b6a35ec3bffd95aaff5e6467eaf4c1', 'simulation/2018_DRAFT_22_60_REOPEN.md': 'f1781c1bd43cfcadf2fcce0cc6b0d63879315b5f55224e8cd639de7583754509', 'simulation/2018_DRAFT_28_43_EVANS_CASCADE.md': '006be16c10213127352087409c52512dd18bc3d084a4bd1d0588c6ec50fb5bfb', 'simulation/2018_DRAFT_37_60_TRENT_CASCADE.md': '1b947c463247fd1c4bfd76cb80df63f2b82aca0cd319c3b7ea53840ea5694c24', 'research/2018_HUTCHISON_24_28_TEAM_BOARD.md': '2eced96d772c5d816f87580f05b0cfc3032469cf020bd5df3f85e9bbc2168a97', 'simulation/CAUSALITY_MODEL.md': '00638830864e9503db4589464806cc0c4c0d94002b039a8bf661d96e6f6a7c45', 'simulation/NBA_2021_L2_NONPLAYOFF_ROSTER_SCOPE.json': '044897a7030a117bc4bcfcf7240895aa6dc7ad0876a001312dfd463e09428fbf', 'simulation/NBA_2021_L2_WORKING_MINUTE_MODELS.json': 'f3b09ab0ca20d21e1257d6777a4fd84cb46fb9479a46d3306603a9a16c1ee431', 'simulation/NBA_2021_L2_WORKING_CHRONOLOGY.json': '8d268860f3835814236e92c9d0022b6504a817d8a0cfd221575195afaa915354'}
RAW = {
    "GSW_GUIDE": (NEW / "GSW_2324.pdf", "1f229c48c478e78079a7c47ba1b9e0baa69f7867a1cfa8ff9c8185bca12dfd45", "https://cdn.nba.com/teams/uploads/sites/1610612744/2023/12/2324-gsw-media-guide.pdf", [432, 433, 434], "NEW_PRIMARY_COLLECTION_RETROSPECTIVE_TRANSACTION_LEDGER"),
    "NBA_SCALE": (NEW / "NBA_2018_19_CBA101.pdf", "c5ce40b61ae6287afaf173d067b6eb20eee72a58a9dc3d24552c1a424dafb213", "https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf", [10, 11, 29], "NEW_PRIMARY_COLLECTION_PUBLISHED_2018_SCALE"),
    "CBA": (CACHE / "fr-2017-cba.pdf", "66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a", "https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf", [69, 70, 202, 292, 294, 295, 296, 297], "EXISTING_PRIMARY_RULES_DIRECT_READ"),
    "OPENING": (CACHE / "fr-den-lal-opening-20261006.pdf", "75a981d64c87de34f7d7896f3a0b1e695b1ed0a3c0e8d4b6638cef71c489ffa0", "https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/goduke.com/documents/2020/12/22/2020_21_Opening_Day_Rosters_12_22_20.pdf?timestamp=20201222074936", [2], "EXISTING_PRIMARY_DATED_OPENING_ROSTER_DIRECT_READ"),
    "KEY_DATES": (CACHE / "fr-2020-21-nba-officials-guide.pdf", "60b6987a4adc6fa3b836c787b033e37299509c8af0d8afda770253e3dfa69d40", "https://697f6f9668a0bb24cd4b-78390edf330c094418f39edbaa9073b0.ssl.cf1.rackcdn.com/2021/02/2020-21-NBA-Officials-Guide-1-5-211.pdf", [4], "EXISTING_PRIMARY_SEASON_KEY_DATES_DIRECT_READ"),
    "NBA_FEED": (CACHE / "fr-nba-player-movement-2026-10-04.json", "3d9d7a6dd7ccd39ddfdd1799a26ef9901b44682d85a26f05239b468a8ae92e3a", "https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json", [], "EXISTING_FROZEN_PRIMARY_EVENT_FEED"),
}
HUT = "Chandler Hutchison"
GP = "Gary Payton II"
OPEN_STANDARD = sorted(["Kent Bazemore", "Marquese Chriss", "Stephen Curry", "Draymond Green", "Damion Lee", "Kevon Looney", "Mychal Mulder", "Kelly Oubre Jr.", "Eric Paschall", "Jordan Poole", "Alen Smailagic", "Brad Wanamaker", "Andrew Wiggins", "James Wiseman", "Klay Thompson"])
L2_EVENTS = ["2021-05-19_POR_GSW", "2021-05-21_GSW_MEM"]


def normalized(p):
    return p.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def sha(p):
    return hashlib.sha256(normalized(p).encode("utf-8")).hexdigest()


def load(f):
    return json.loads(normalized(ROOT / f))


def build():
    for f in INPUTS:
        if sha(ROOT / f) != REVIEWED_SHA[f]:
            raise ValueError("reviewed source changed: " + f)
    raw = {}
    for key, (p, h, url, pages, role) in RAW.items():
        b = p.read_bytes()
        if hashlib.sha256(b).hexdigest() != h:
            raise ValueError("raw source changed: " + key)
        item = {"cache_path": str(p), "url": url, "raw_sha256": h, "bytes": len(b), "role": role, "pdf_pages": pages}
        if pages:
            doc = fitz.open(p)
            item["page_text_sha256"] = {str(page): hashlib.sha256(doc[page - 1].get_text().replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")).hexdigest() for page in pages}
            item["text_extraction"] = "PyMuPDF get_text(), UTF8 no BOM, CRLF/CR normalized LF; raw PDF bytes unchanged"
        raw[key] = item
    roster = load("simulation/NBA_2021_L2_NONPLAYOFF_ROSTER_SCOPE.json")["roster_families"]["GSW"]
    historic = sorted(roster["standard"])
    tw = sorted(roster["two_way"])
    l2 = load("simulation/NBA_2021_L2_WORKING_MINUTE_MODELS.json")
    preserved = {g["event_id"]: deepcopy(g["teams"]["GSW"]) for g in l2["games"] if g["event_id"] in L2_EVENTS}
    candidates = []
    definitions = [
        ("G1", "2020-02-06_HUTCHISON_TO_MIN", historic, OPEN_STANDARD, ["2020-02-06: substitute Hutchison for original outgoing Evans in Russell/Spellman package"], "MIN_ACCEPTANCE_AND_HUTCHISON_VALUE;FULL_MATCHING_AND_HARDCAP;MIN_DOWNSTREAM_PATH", True),
        ("G2", "RETAIN_HUTCHISON_OMIT_WANAMAKER_AND_MAY16_PAYTON", sorted((set(historic) - {GP}) | {HUT}), sorted((set(OPEN_STANDARD) - {"Brad Wanamaker"}) | {HUT}), ["2020-02-06: retain Hutchison; modified outgoing Russell/Spellman package", "2020-11-24: omit Wanamaker signing", "2021-03-25: omit original Wanamaker/CHA transaction, including its named outgoing/incoming claims", "2021-05-16: omit Payton rest-of-season signing"], "MODIFIED_MIN_PACKAGE;FULL_HARDCAP;THIRD_OPTION;CHA_REGULAR_MINUTES_AND_PICK_CASCADE;PAYTON_FUTURE", False),
        ("G3", "RETAIN_THEN_PREOPENING_WAIVER_PAYTON_PRESERVED", historic, OPEN_STANDARD, ["2020-02-06: retain Hutchison; modified outgoing Russell/Spellman package", "2020-12-18: candidate waiver request before opening roster deadline; completed waiver/list removal timing must satisfy the December21 deadline"], "MODIFIED_MIN_PACKAGE;FULL_HARDCAP;THIRD_OPTION_LIVE_CONTRACT_BEFORE_WAIVER;WAIVER_COMPLETION_TIMING;PROTECTED_AND_FOURTH_OPTION_COST", False),
    ]
    for cid, route, standard, opening, changes, gaps, recommended in definitions:
        candidates.append({"id": cid, "route": route, "status": "COMPARISON_CANDIDATE_NOT_SELECTED", "recommended": recommended, "author_locked": False, "may_standard": standard, "may_two_way": tw, "opening_standard": opening, "opening_two_way_in_official_pdf": ["Nico Mannion"], "JTA_two_way_event_is_separate_from_opening_pdf_observation": True, "JTA_source_dates": {"guide":"2020-12-22", "frozen_feed":"2020-12-21T00:00:00", "exact_execution_time":None}, "dated_changes": changes, "hutchison_in_gsw_may": cid == "G2", "third_option_required_for_may_hutchison": cid == "G2", "third_option_required_for_december_waiver_live_contract": cid == "G3", "new_contract_after_nonexercise_automatically_added": False, "third_option_actual_selection": None, "fourth_option_actual_selection": None, "financial_percentage_selected": None, "underlying_pick_conditions_changed_or_selected": False, "future_min_ny_evans_path_copied": False, "actual_acceptance": None, "actual_registration_cleared": False, "full_cost_bound_certified": False, "candidate_waiver_request_date": "2020-12-18" if cid == "G3" else None, "candidate_waiver_completion_date": None, "waiver_erases_all_salary": False, "stretch_selected": False, "claiming_team_or_setoff_assumed": False, "new_standard_financial_contract_selected": False, "l2_positive_vectors_preserved": True, "other_teams_minutes_certified_unchanged": False, "remaining_gaps": gaps.split(";"), "reserve_hutchison_health": None})
    return {
        "status": "THREE_CONDITIONAL_GSW_OPERATING_CANDIDATES_READY_FOR_REVIEW_NO_PROMOTION",
        "baseline_main": BASELINE,
        "source_hash_method": "SHA256_UTF8_NO_BOM_LF_REPOSITORY;RAW_BYTES_CACHES;NORMALIZED_PYMUPDF_PAGE_TEXT",
        "source_sha256": {**REVIEWED_SHA, SELF: sha(ROOT / SELF)},
        "raw_sources": raw,
        "authority": {"gsw_2018_28_landing": "TEAM_BOARD_PASS_DRAFT_NIGHT_PRIMARY_CANDIDATE_EXACT_LANDING_HOLD", "landing_author_locked": False, "source": "control/AUTHORITY_MAP.md", "new_transaction_selection": False, "health_season_style_delegation_is_new_financial_selection": False, "approved_T1_T4_direction_preserved": True},
        "historical_fact_anchors": [
            {"date": "2018-07-02", "event": "original Evans rookie signing in GSW guide", "source": "GSW_GUIDE", "pdf_page": 432, "feed_date": "2018-07-01", "date_disagreement_preserved": True, "hutchison_signing_date": None},
            {"date": "2019-07-07", "event": "Russell/Napier/Graham acquired via Durant sign-and-trade; hardcap trigger", "source": "GSW_GUIDE", "pdf_page": 433},
            {"date": "2019-07-08", "event": "Spellman from ATL for Damian Jones/named2026second; Napier/Graham to MIN", "source": "GSW_GUIDE", "pdf_page": 433},
            {"date": "2020-02-06", "event": "Wiggins/named top3protected2021first/named2021second to GSW; Evans/Russell/Spellman to MIN", "source": "GSW_GUIDE", "pdf_page": 433, "candidate_hutchison_assignment_observed": False},
            {"date": "2020-11-24", "event": "original Wanamaker GSW signing in guide", "source": "GSW_GUIDE", "pdf_page": 434, "feed_date": "2020-11-23T00:00:00", "date_disagreement_preserved": True, "exact_execution_time": None},
            {"date": "2020-11-24", "event": "original Evans MIN to NY", "source": "NBA_FEED", "hutchison_min_ny_assignment_observed": False},
            {"date": "2020-12-09", "event": "original Evans NY waiver in frozen feed", "source": "NBA_FEED", "candidate_hutchison_waiver_copied": False},
            {"date": "2020-12-22", "event": "original JTA two-way signing guide; frozenfeed dates it2020-12-21T00:00:00", "source": "GSW_GUIDE+NBA_FEED", "pdf_page": 434, "date_disagreement_preserved": True, "exact_execution_time": None},
            {"date": "2020-12-21", "event": "opening roster deadline11pmET", "source": "KEY_DATES", "pdf_page": 4},
            {"date": "2021-03-25", "event": "GSW moves Wanamaker to CHA and Chriss to SAS", "source": "GSW_GUIDE", "pdf_page": 434},
            {"date": "2021-04-08", "event": "Payton first10day", "source": "GSW_GUIDE", "pdf_page": 434},
            {"date": "2021-04-19", "event": "Payton second10day", "source": "GSW_GUIDE", "pdf_page": 434},
            {"date": "2021-05-13", "event": "JTA standard/Bell two-way", "source": "GSW_GUIDE", "pdf_page": 434},
            {"date": "2021-05-16", "event": "Payton standard rest-of-season contract", "source": "GSW_GUIDE", "pdf_page": 434},
        ],
        "money_and_option_model": {
            "source": "NBA_SCALE.PDF29+2017CBA_VIII1_and4",
            "pick": 28, "contract_first_season_condition": "2018-19_ROOKIE_SCALE_ONLY",
            "published_table_units": "USD_THOUSANDS_ONE_DECIMAL",
            "displayed_scale_reference_dollars": [1370200, 1604900, 1681100],
            "displayed_fourth_option_increase_percent": 80.5,
            "salary_plus_unlikely_range_formula": "0.8*actual_applicable_scale <= salary_plus_unlikely <= 1.2*actual_applicable_scale; base salary itself >=0.8*scale",
            "display_reference_80_120_arithmetic": [[1096160, 1644240], [1283920, 1925880], [1344880, 2017320]],
            "display_reference_fourth_arithmetic": [2427508.4, 3641262.6],
            "display_arithmetic_is_exact_operative_dollar_certificate": False,
            "table_rounding_method_and_exact_underlying_dollars": None,
            "actual_contract_salary_or_bonuses": None,
            "third_option_exercise_notice_date": None,
            "ordinary_third_option_deadline_under_CBA": "2019-10-31",
            "fourth_option_exercise_notice_date": None,
            "season_specific_2020_fourth_option_deadline": None,
            "ordinary_CBA_deadline_must_not_overwrite_2020_adjustment": True,
            "third_fourth_options_not_automatic": True,
            "2019_hardcap_constraint": "GSW_apron_adjusted_other_cost(t) + Hutchison_apron_charge(t) <= 2019_apron at S&T completion and every subsequent state through that capyear",
            "gsw_2019_other_cost_domain": None,
            "gsw_2019_full_hardcap_proof": False,
            "2020_matching_constraints": {"G1": "apply VII6(j) to GSW Russell+Spellman+Hutchison outgoing and MIN Wiggins outgoing; Hutchison receiving trade-bonus capped by VIII1(d)", "G2_G3": "recompute BOTH teams with Russell+Spellman only outgoing and unchanged Wiggins/namedpick incoming; no automatic original matched-salary certificate"},
            "2020_full_matching_cost_proof": False,
            "waiver_rule": "VII4(a)(1)(i): paid/payable terminated-contract salary remains Team Salary; no automatic zero or stretch",
            "waiver_cost_if_third_exercised": "2020-21 protected salary remains; fourth option protection retained only if exercised; exact charge/setoff null",
            "gp2_ten_day_end_dates": None,
            "ten_day_rule": "II9(a): longer of10days or3teamgames; no exact expiry inferred from signing alone",
        },
        "conflict_witnesses": {"opening": {"historical_standard": OPEN_STANDARD, "actual_pdf_standard_count_including_inactive_Klay": 15, "two_way_pdf_names": ["Nico Mannion"], "unadjusted_hutchison_retention_count": 16, "inactive_Klay_is_standard_not_two_way": True}, "may": {"historical_standard": historic, "historical_two_way": tw, "unadjusted_hutchison_retention_count": 16, "only_may16_payton_omission_does_not_resolve_opening_conflict": True}},
        "preserved_l2_gsw_team_inputs": preserved,
        "candidates": candidates,
        "recommendation": {"candidate": "G1", "reason": "Existing2020 auxiliary-rookie assignment candidate solves both opening and May slot issues without deleting Wanamaker/Payton events; source supports cap-role comparison, not Minnesota valuation/acceptance or full legal implementation.", "selected": False, "exact_hutchison_destination_after_min": None, "no_gsw_return_in_G1_candidate_family": True},
        "new_primary_documents_collected": 2,
        "tools": {"Antigravity": "NOT_RUN_FOR_THIS_PACKET", "NotebookLM": "NOT_RUN_FOR_THIS_PACKET", "Claude": "NOT_RUN_FOR_THIS_PACKET", "independent_review": "PENDING"},
        "full_actual_registration_complete": False,
        "medical_certified": False, "whole_legal_certified": False,
        "season_selected_by_this_packet": False, "new_financial_selection": False,
        "actual_pack_count_changed": 0, "manuscript_count": 0,
        "freeze": "v0.30 PARTIAL", "design_gate": "CLOSED", "manuscript_gate": "CLOSED",
    }


def validate(d):
    if d != build():
        raise ValueError("candidate/source/preservation reconstruction mismatch")
    if list(d["preserved_l2_gsw_team_inputs"]) != L2_EVENTS:
        raise ValueError("GSW dates missing")
    for event, team in d["preserved_l2_gsw_team_inputs"].items():
        seconds = team["player_seconds"]
        if len(seconds) != 8 or sum(seconds.values()) != 14400:
            raise ValueError("positive vector changed")
        for c in d["candidates"]:
            if len(set(c["may_standard"])) != 15 or len(set(c["opening_standard"])) != 15 or len(set(c["may_two_way"])) != 2:
                raise ValueError("candidate15+2/opening invalid")
            if set(c["may_standard"]) & set(c["may_two_way"]) or not set(seconds) <= set(c["may_standard"]):
                raise ValueError("contract class/positive identity")
    return {"candidate_count": 3, "opening_conflicts_exposed": 1, "may_conflicts_exposed": 1, "preserved_l2_gsw_vectors": 2, "positive_seconds_per_team": 14400, "new_canonical_selections": 0, "whole_legal_passes": 0}


def markdown(d):
    return """# GSW Hutchison 2018–2021 운영 비교 후보

상태: **3후보 검토 준비 / 선택·정본 승격0**. 기준 main `b48fb82` 고정. [현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md), [원권위](../control/AUTHORITY_MAP.md), [검문 입력](GSW_HUTCHISON_2018_2021_OPERATING_CANDIDATES.json).

## 먼저 복구한 권위와 실제 빈칸

GSW28 Hutchison은 TEAM_BOARD_PASS/주 계산 후보이며 정확 착지 HOLD이다. 이전 Evans의 계약·건강·성과·MIN→NY→방출 날짜를 Hutchison 사실로 대입할 수 없다. 건강·시즌·문체 위임도 새 거래·정확 금융 선택을 확정하지 않는다. 승인 T1/T4 큰 방향과 두 GSW L2 작업 입력은 보존한다.

## 새 공식자료 및 사실

[Warriors 공식2324 guide](https://cdn.nba.com/teams/uploads/sites/1610612744/2023/12/2324-gsw-media-guide.pdf)의 PDF432–434/인쇄431–433을 읽었다. 원2019 Russell S&T와 Spellman/Jones, 2020 Wiggins 거래의 Evans 보조계약, 2021 Wanamaker/Chriss 이탈·Payton 두10일 계약·JTA/Bell·5/16 Payton 서명이 연결된다. 이 자료는 회고 거래 연표이며 전체 계약 조항은 아니다. 원Evans 서명은 guide7/2와 NBA frozenfeed7/1이 달라 둘 다 보존하며 Hutchison 서명일은 null이다. Wanamaker 서명도 guide11/24와 feed11/23T00:00:00이 달라 양쪽 날짜를 보존한다. 원Evans MIN→NY11/24 feed 사건은 별도이며 Hutchison에게 복사하지 않는다.

[NBA 실제2018 rookie 표](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf) PDF29의 #28 표시는 $000s로 1,370.2/1,604.9/1,681.1, 4년차 +80.5%이다. 80–120% 표시값 산술은 1,096,160–1,644,240 / 1,283,920–1,925,880 / 1,344,880–2,017,320이다. 표의 표시 정밀도·정확 계약원장·옵션 선택을 인증한 값이 아니며 exact operative-dollar certificate=false다. Chicago22 급여 복사0이다.

[2017 CBA 원문](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf) VIII1의 두 보장시즌/두 팀옵션과 80–120%·거래보너스 제한, VII4의 방출 후 paid/payable charge를 직접 읽었다. 2019 S&T 후에는 capyear 내 모든 상태에서 apron-adjusted 전체 비용을 확인해야 하며 2020 Wiggins 양팀 matching도 새 보조자산으로 다시 계산한다. 전체 비용표·정확 계약금액은 아직 null이다. 2020 코로나 변경 옵션기한을 평상시 Oct31로 복사하지 않는다. 10일 계약 만료는 날짜10일/팀3경기 중 긴 기간이므로 정확 끝 날짜를 자동 계산하지 않았다.

## 슬롯의 새 구체 반례

NBA Dec22 개막 PDF2에서 GSW는 **standard15**이다. 하단 inactive Klay Thompson도 standard이며 별표 Nico Mannion만 TW이다. JTA TW 서명은 guide12/22와 frozenfeed12/21T00:00:00이 달라 두 source 날짜를 보존하고 정확 실행시각은null이다. Nico만TW인 개막PDF 관측과 별도로 연결한다. Hutchison을 2020 거래에서 빼고 기존 모든 서명을 유지하면 **개막부터16**이다. 5/16 Payton만 생략해도 이 앞선 충돌은 해결되지 않는다. May 작업 명단은 기존 standard15/TW2이며 Hutchison 추가시16이다.

| 후보 | 구체 운영 | May 후보 | 추가 비용·인과 | 판정 |
|---|---|---|---|---|
| G1 | 2020-02-06 Russell/Spellman과 Hutchison을 MIN으로; 원Evans 자리만 교체 | 기존15+2 | MIN 평가/수락·양팀 matching·전체 hardcap·Hutchison 후속 경로 미완 | **권고 후보** |
| G2 | 2020 Hutchison 유지; 11/24 Wanamaker 영입과 그3/25 CHA 거래 생략; 5/16 Payton 생략 | Hutchison 포함15+2 | 3년차 옵션 필요; CHA 분·양측 픽·Payton 후속 영향 재계산 필요 | 추가 사건 가장 많음 |
| G3 | 2020 Hutchison 유지 후 개막 전 waiver; Wanamaker/Payton 가족 보존 | 기존15+2 | 요청일12/18 후보, 실제 list 제거 완료일 null; 현재·행사된 미래 옵션 보호급여가 남음 | 금융·방출 후손 HOLD |

G1 권고 근거는 기존 보조 루키 자산 후보로 두 슬롯 충돌을 함께 없애는 운영 비교다. Minnesota가 받아들인다는 사실·Hutchison과 Evans의 동가치·후대 원NY 방출을 뜻하지 않는다. G2는 기존 CHA 정규 작업분도 보존 인증하지 않는다. G3는 2019년에3년차 옵션이 유효하게 행사되어 December에 살아 있는 계약이 있을 때만 가능하다. 미행사면2020 만료/FA이며 신규계약을 자동 추가하지 않는다. G3의 12/18은 작가확정 날짜가 아니며 12/21 개막명단 마감 전 waiver 완료/리스트 제거 가능 여부를 추가 검문해야 한다. 방출로 급여가0이 되거나 stretch/setoff가 자동 발생한다는 가정0이다.

## 보존 검문과 후속

5/19 POR–GSW, 5/21 GSW–MEM의 기존 GSW8명/팀14,400초/선발·가용·원증인을 객체 전체로 보존했다. 세 후보 모두 해당8명이 standard명단에 남는다. 세 후보의 opening15/May15+2 구조를 검문하지만 actual 등록·의료·전체법적·시즌은 false다. Hutchison의0분 건강 원인은 null이다. 원자산의 새 지출·정확 계약 선택·독서/실제Pack/원고 추가0이다.

재현: `python tools/build_gsw_hutchison_operating_candidates.py --check`.
원자료6 raw지문·새PDF2·페이지 추출지문 및 기존정본9 LF지문은 JSON에 있다. Antigravity/NotebookLM/Claude는 이번 패킷에서 NOT_RUN, 독립검문 PENDING이다. 부모 독립검토 전 원장·중앙·선택 승격0.

## 7행 진행표 — 작성 시점 현행표의 한정 복구

| 번호 | 큰 묶음 | 현황 |
|---|---|---|
|1|2020 드래프트 연쇄|완료|
|2|Chicago2020–21|법적11/12, F4/5, A0/3, K0/4; 작업 분/교대 완료·전체 시즌 미완|
|3|2021–23 거래·계약|승인 방향 반영; 정확 실행 미완|
|4|장기 커리어|선행 시즌 확정 대기|
|5|결말·전체 구조|골격 보존; 전체 회차기능표 미완|
|6|집필 규격·Context Pack|E1/E2 기능2/A01잔여34; 전체780 중 미배정778·실제Pack0|
|7|통합·독립·작가 승인|전체 게이트 미완|

**미완료 큰 묶음6 / v0.30 PARTIAL / 설계·원고 CLOSED / 원고0.** 이번 완료는 GSW 세 후보와 새 슬롯 반례·급여표 입력 복구이며 큰 묶음 종료가 아니다.
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    d = build()
    stats = validate(d)
    if args.self_test:
        mutations = [
            ("landing_lock", lambda x: x["authority"].update(landing_author_locked=True)),
            ("same_total_minute_move", lambda x: x["preserved_l2_gsw_team_inputs"][L2_EVENTS[0]]["player_seconds"].update({"Stephen Curry":2396, "Andrew Wiggins":2228})),
            ("inactive_Klay_to_TW", lambda x: x["candidates"][0]["may_two_way"].append("Klay Thompson")),
            ("G2_keep_Wanamaker_opening16", lambda x: x["candidates"][1]["opening_standard"].append("Brad Wanamaker")),
            ("waiver_zero_charge", lambda x: x["candidates"][2].update(waiver_erases_all_salary=True)),
            ("display_number_exact_cert", lambda x: x["money_and_option_model"].update(display_arithmetic_is_exact_operative_dollar_certificate=True)),
        ]
        for name, change in mutations:
            bad = deepcopy(d)
            change(bad)
            try:
                validate(bad)
            except ValueError:
                continue
            raise ValueError("mutation accepted: " + name)
        stats["negative_rejected"] = [name for name, _ in mutations]
    if args.check:
        validate(load(str(OUT.relative_to(ROOT)).replace("\\", "/")))
        if normalized(MD) != markdown(d):
            raise ValueError("MD stale")
    else:
        OUT.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        MD.write_text(markdown(d), encoding="utf-8", newline="\n")
    print(json.dumps({"status":d["status"], **stats}, ensure_ascii=False))


if __name__ == "__main__":
    main()
