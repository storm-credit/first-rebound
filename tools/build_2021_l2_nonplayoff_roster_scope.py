"""Attach source-scoped 15+2 roster candidates to four L2 play-in teams.

This does not register players, certify medical availability, or alter the
existing six dated minute models. It keeps transaction collisions explicit.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import build_2021_l2_working_minutes as selected

ROOT = Path(__file__).resolve().parents[1]
MINUTES = "simulation/NBA_2021_L2_WORKING_MINUTE_MODELS.json"
CHI_CSV = "simulation/CHICAGO_2021_POSTDEADLINE_ROSTER.csv"
WAS_CASCADE = "simulation/2021_WASHINGTON_CHICAGO_PORTLAND_TRANSACTION_CASCADE.md"
GSW_PATH = "simulation/CHICAGO_2020_21_CLOSE_GAME_PATHS.md"
CALENDAR = "simulation/NBA_2021_L2_DATED_WORKING_CALENDAR.json"
OUT = ROOT / "simulation/NBA_2021_L2_NONPLAYOFF_ROSTER_SCOPE.json"
MD = ROOT / "simulation/NBA_2021_L2_NONPLAYOFF_ROSTER_SCOPE.md"
LOCAL_SOURCES = (MINUTES, CHI_CSV, WAS_CASCADE, GSW_PATH, CALENDAR)

# These are transcriptions of official historical gamebooks, not alternate
# world registration certificates. The 2020-21 two-way classifications are
# cross-checked against NBA G League's official tracker and later transactions.
ROSTERS = {
    "WAS": {
        "standard": ["Alex Len", "Anthony Gill", "Bradley Beal", "Daniel Gafford",
                     "Davis Bertans", "Deni Avdija", "Gary Trent Jr.", "Isaac Bonga",
                     "Ish Smith", "Raul Neto", "Robin Lopez", "Rui Hachimura",
                     "Russell Westbrook", "Thomas Bryant", "Troy Brown Jr."],
        "two_way": ["Garrison Mathews", "Cassius Winston"],
        "status": "CANDIDATE_15_PLUS_2_HOMESLEY_OMISSION_UNSELECTED",
        "roster_source": WAS_CASCADE,
        "historical_difference": ["Gary Trent Jr. and Troy Brown Jr. retained; Chandler Hutchison absent in alternate path.",
                                  "Historical Caleb Homesley May 15 standard signing would create a 16th standard player; omission is a candidate, not selected."],
        "registration_complete": False,
    },
    "GSW": {
        "standard": ["Alen Smailagic", "Andrew Wiggins", "Damion Lee", "Draymond Green",
                     "Eric Paschall", "Gary Payton II", "James Wiseman", "Jordan Poole",
                     "Juan Toscano-Anderson", "Kent Bazemore", "Kelly Oubre Jr.",
                     "Kevon Looney", "Klay Thompson", "Mychal Mulder", "Stephen Curry"],
        "two_way": ["Jordan Bell", "Nico Mannion"],
        "status": "HISTORICAL_15_PLUS_2_CANDIDATE_HUTCHISON_REGISTRATION_HOLD",
        "roster_source": GSW_PATH,
        "historical_difference": ["Chandler Hutchison's 2018 GSW draft landing and later transaction/registration remain unresolved.",
                                  "Keeping Hutchison alongside all 15 historical standard names would exceed the standard limit; omitting Payton's May 16 signing is an unselected alternative."],
        "registration_complete": False,
    },
    "SAS": {
        "standard": ["DaQuan Jeffries", "DeMar DeRozan", "Dejounte Murray",
                     "Derrick White", "Devin Vassell", "Drew Eubanks", "Gorgui Dieng",
                     "Jakob Poeltl", "Keldon Johnson", "Lonnie Walker IV",
                     "Luka Samanic", "Patty Mills", "Rudy Gay", "Tre Jones", "Trey Lyles"],
        "two_way": ["Keita Bates-Diop", "Quinndary Weatherspoon"],
        "status": "HISTORICAL_15_PLUS_2_CONDITIONAL_CARRY",
        "roster_source": "https://statsdmz.nba.com/pdfs/20210519/20210519_SASMEM_book.pdf",
        "historical_difference": ["DaQuan Jeffries appears inactive and Not With Team in the historical May 19 scorer report; alternate registration and presence are not certified."],
        "registration_complete": False,
    },
}

EXTERNAL = {
    "WAS_MAY18_GAMEBOOK": {"url": "https://statsdmz.nba.com/pdfs/20210518/20210518_WASBOS.pdf",
                           "sha256_raw_pdf_bytes": "e25e0110b599f6d272e657485b2e82c1b26ee3a9fd5c6ec4c0568e2a567c99d6",
                           "locator": "page 1 final box and inactive line; historical roster only"},
    "GSW_MAY19_GAMEBOOK": {"url": "https://statsdmz.nba.com/pdfs/20210519/20210519_GSWLAL_book.pdf",
                           "sha256_raw_pdf_bytes": "e98f31556173d2d261ebf31b4e1652ef03e9cc7d5e56a8f433740931b597c594",
                           "locator": "page 1 final box and inactive line; historical roster only"},
    "SAS_MAY19_GAMEBOOK": {"url": "https://statsdmz.nba.com/pdfs/20210519/20210519_SASMEM_book.pdf",
                           "sha256_raw_pdf_bytes": "9bc963d51e51ed66f496724e084cecf425793afff2107858f84fd995f197ee78",
                           "locator": "page 1 final box and inactive line; historical roster only"},
    "MAY19_INJURY_REPORT": {"url": "https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-19_05PM.pdf",
                            "sha256_raw_pdf_bytes": "5a4bc6da820630da78e4b8ff36d53c98a328b9dedfb5ff93b4e884c99eae0766",
                            "locator": "historical GSW/SAS listed statuses"},
    "MAY21_INJURY_REPORT": {"url": "https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-21_05PM.pdf",
                            "sha256_raw_pdf_bytes": "0973c8d8b824375611ee2f141541e900916975eb5dddb8c6e388f30dccf0c965",
                            "locator": "historical GSW Lee questionable, Oubre/Thompson/Wiseman out"},
    "NBA_GLEAGUE_TWOWAY_TRACKER": {"url": "https://gleague.nba.com/news/two-way-tracker-for-2020-21-season",
                                   "locator": "2020-21 CHI/WAS/GSW/SAS two-way table; early season snapshot"},
    "NBA_GLEAGUE_CALLOUTS": {"url": "https://gleague.nba.com/nba-call-ups-for-the-2020-21-season",
                               "locator": "Caleb Homesley May 15 standard; Jordan Bell May 13 two-way"},
    "GSW_TRANSACTION_GUIDE": {"url": "https://cdn.nba.com/teams/uploads/sites/1610612744/2023/12/2324-gsw-media-guide.pdf",
                              "locator": "2020-21 May 13 JTA conversion/Jordan Bell two-way, May 16 Gary Payton II signing"},
}

HISTORICAL_INACTIVE = {
    ("WAS", "2021-05-18"): {"Deni Avdija": "RIGHT_ANKLE_FRACTURE",
                              "Thomas Bryant": "LEFT_KNEE_ACL_INJURY"},
    ("GSW", "2021-05-19"): {"Damion Lee": "HEALTH_AND_SAFETY_PROTOCOLS",
                              "Kelly Oubre Jr.": "LEFT_WRIST_SORENESS",
                              "Klay Thompson": "RIGHT_ACHILLES_REPAIR",
                              "James Wiseman": "RIGHT_KNEE_MENISCUS_TEAR"},
    ("GSW", "2021-05-21"): {"Damion Lee": "QUESTIONABLE_HEALTH_AND_SAFETY_PROTOCOLS",
                              "Kelly Oubre Jr.": "OUT_LEFT_WRIST_SORENESS",
                              "Klay Thompson": "OUT_RIGHT_ACHILLES_REPAIR",
                              "James Wiseman": "OUT_RIGHT_KNEE_MENISCUS_TEAR"},
    ("SAS", "2021-05-19"): {"DaQuan Jeffries": "NOT_WITH_TEAM",
                              "Trey Lyles": "RIGHT_ANKLE_SPRAIN_QUESTIONABLE_IN_REPORT",
                              "Luka Samanic": "LEFT_FOURTH_METACARPAL_FRACTURE",
                              "Derrick White": "RIGHT_ANKLE_SPRAIN"},
}


def read(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def sha(path: str) -> str:
    body = (ROOT / path).read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def chicago_roster() -> dict:
    with (ROOT / CHI_CSV).open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    standard = sorted(r["player"] for r in rows if r["contract_class"] == "STANDARD")
    tw = sorted(r["player"] for r in rows if r["contract_class"] == "TWO_WAY")
    assert len(standard) == 15 and len(tw) == 2
    return {"standard": standard, "two_way": tw,
            "status": "EXISTING_APPROVED_TRANSACTION_PATH_15_PLUS_2_WORKING_ROSTER",
            "roster_source": CHI_CSV,
            "historical_difference": ["Chicago's fictional protagonist and LaMelo are included; original NBA May 2021 roster cannot be copied."],
            "registration_complete": False}


def build() -> dict:
    minute_model = read(MINUTES)
    if minute_model != selected.build():
        raise ValueError('L2 upstream input differs from full source reconstruction')
    calendar = read(CALENDAR)
    assert len(minute_model["games"]) == len(calendar["games"]) == 6
    assert minute_model["working_team_vectors"] == 12
    rosters = {"CHI": chicago_roster(), **ROSTERS}
    out = []
    for game in minute_model["games"]:
        cal = next(g for g in calendar["games"] if g["event_id"] == game["event_id"])
        assert cal["date"] == game["date"] and cal["home"] == game["home"] and cal["away"] == game["away"]
        for team, minute in game["teams"].items():
            if team not in rosters:
                continue
            roster = rosters[team]
            standard = roster["standard"]
            tw = roster["two_way"]
            assert len(standard) <= 15 and len(tw) <= 2 and len(set(standard + tw)) == len(standard) + len(tw)
            all_names = set(standard + tw)
            players = minute["player_seconds"]
            positive = {p for p, sec in players.items() if sec > 1e-7}
            assert positive <= all_names, (game["event_id"], team, sorted(positive - all_names))
            entries = []
            for player in sorted(all_names):
                sec = players.get(player, 0)
                historical = HISTORICAL_INACTIVE.get((team, game["date"]), {}).get(player)
                entries.append({"player": player,
                                "contract_class_working": "STANDARD" if player in standard else "TWO_WAY",
                                "modeled_seconds": sec,
                                "working_positive_minute_selection": sec > 1e-7,
                                "reserve_health_input": "POSITIVE_MINUTE_MODEL_NOT_MEDICAL_CLEARANCE" if sec > 1e-7
                                                        else "UNSELECTED_ZERO_MINUTES_HEALTH_UNDETERMINED",
                                "historical_status_anchor": historical,
                                "historical_status_is_alternate_game_certification": False,
                                "actual_registration_certified": False,
                                "medical_certified": False})
            assert len(entries) == 17
            out.append({"event_id": game["event_id"], "date": game["date"], "team": team,
                        "standard_count": len(standard), "two_way_count": len(tw),
                        "positive_count": len(positive), "reserve_count": len(all_names - positive),
                        "roster_candidate_status": roster["status"],
                        "roster_source": roster["roster_source"],
                        "minute_source": MINUTES,
                        "entries": entries,
                        "positive_players_all_in_roster": True,
                        "zero_minutes_do_not_imply_injury": True,
                        "date_specific_health_selection_complete": False,
                        "working_roster_registration_complete": False})
    assert len(out) == 6 and Counter(r["team"] for r in out) == {"CHI": 2, "GSW": 2, "WAS": 1, "SAS": 1}
    for data in EXTERNAL.values():
        data["cache_location"] = None
        data["raw_body_preserved_in_repository"] = False
    return {"status": "FOUR_NONPLAYOFF_TEAM_DATED_ROSTER_CANDIDATES_WITH_REGISTRATION_HEALTH_HOLD",
            "authority": "canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json",
            "source_hash_method": "SHA256_UTF8_LF_NORMALIZED_LOCAL;PDF_RAW_BYTES_EXTERNAL",
            "local_source_sha256": {path: sha(path) for path in LOCAL_SOURCES},
            "official_external_sources": EXTERNAL,
            "roster_families": rosters, "dated_team_rosters": out,
            "working_team_roster_candidates": 6, "distinct_teams": 4,
            "existing_twelve_team_minute_vectors_preserved": True,
            "conflicts": {
                "WAS": {"type": "SIXTEENTH_STANDARD_IF_HISTORICAL_HOMESLEY_SIGNING_COPIED",
                        "candidate": "OMIT_MAY15_HOMESLEY_SIGNING_KEEP_BROWN_AND_TRENT",
                        "candidate_selected": False,
                        "salary_and_slot_followup": "Roster slot and nonzero or unknown salary charge differ; exact fee and filing remain HOLD."},
                "GSW": {"type": "HUTCHISON_DRAFT_ASSET_AND_REGISTRATION_PATH_UNRESOLVED",
                        "candidate": "HISTORICAL_17_WITHOUT_HUTCHISON_OR_RETAIN_HUTCHISON_AND_HOLD_LATE_STANDARD_SLOT",
                        "candidate_selected": False,
                        "salary_and_slot_followup": "Hutchison disposition and possible May16 Payton standard slot require explicit downstream transaction audit."}},
            "reserve_health_selection": "UNSELECTED_HOLD_EXCEPT_POSITIVE_MINUTE_WORKING_INPUT",
            "historical_inactive_reasons_are_source_anchors_only": True,
            "author_locked": False, "actual_homesley_omission_selected": False,
            "actual_active_lists_certified": False, "medical_certified": False,
            "legal_execution_cleared": False, "whole_league_health_cleared": False,
            "season_selected": False, "manuscript_allowed": False}


def validate(packet: dict, expected: dict | None = None) -> None:
    assert packet["local_source_sha256"] == {path: sha(path) for path in LOCAL_SOURCES}
    assert len(packet["dated_team_rosters"]) == 6
    assert not any(packet[k] for k in ("author_locked", "actual_homesley_omission_selected",
                                        "actual_active_lists_certified", "medical_certified",
                                        "legal_execution_cleared", "whole_league_health_cleared",
                                        "season_selected", "manuscript_allowed"))
    for record in packet["dated_team_rosters"]:
        assert record["standard_count"] <= 15 and record["two_way_count"] <= 2
        assert record["standard_count"] + record["two_way_count"] == len(record["entries"])
        assert record["positive_players_all_in_roster"] and record["zero_minutes_do_not_imply_injury"]
        assert not record["working_roster_registration_complete"]
        for entry in record["entries"]:
            assert not entry["actual_registration_certified"] and not entry["medical_certified"]
            if entry["modeled_seconds"] <= 1e-7:
                assert entry["reserve_health_input"] == "UNSELECTED_ZERO_MINUTES_HEALTH_UNDETERMINED"
    if packet != (build() if expected is None else expected):
        raise ValueError('roster candidate differs from full source reconstruction')


def markdown(packet: dict) -> str:
    lines = ["# L2 플레이인 비플레이오프 4팀 명단·예비 건강 입력 범위", "",
             f"상태: `{packet['status']}`. 기존 6경기·12팀 분은 변경하지 않았다.",
             "아래 6개 팀-날짜는 모두 15 표준+2 투웨이 **작업 명단 후보**다.",
             "양수 분 선수는 후보 명단에 들어가며, 0분은 부상이나 등록 제외를 뜻하지 않는다.", "",
             "|날짜|팀|표준+투웨이|양수/예비|범위|", "|---|---|---:|---:|---|"]
    for row in packet["dated_team_rosters"]:
        lines.append(f"|{row['date']}|{row['team']}|{row['standard_count']}+{row['two_way_count']}|"
                     f"{row['positive_count']}/{row['reserve_count']}|{row['roster_candidate_status']}|")
    lines += ["", "## 남은 등록 판단", "",
              "- WAS: 대체 역사에서는 Brown·Trent가 잔류하고 Hutchison이 없다. 원역사 5월 15일 Homesley 표준 계약까지 옮기면 표준 16명이다. Homesley 서명 생략은 슬롯 해결 **후보**이며 작가 선택·계약 접수로 확정하지 않았다. 급여·슬롯 후속 효과도 HOLD다.",
              "- GSW: Hutchison의 드래프트 후 거래·등록 경로가 미결이다. 원역사 15+2와 Hutchison을 동시에 확정할 수 없다. May 16 Payton 표준 계약을 생략하는 안도 미선택 후보로만 남긴다.",
              "- CHI: 기존 15+2 설계 CSV를 사용했다. Theis·Green 등 개별 거래 실행과 날짜별 의료 승인은 별개 HOLD다.",
              "- SAS: 원역사 May 19 경기책의 15+2를 조건부 입력으로 사용했다. Jeffries는 원역사 명단에서 Not With Team이며 대체 세계 등록은 미인증이다.",
              "", "## 공식 근거", ""]
    for name, source in packet["official_external_sources"].items():
        lines.append(f"- {name}: [{source['url']}]({source['url']}) — {source['locator']}"
                     + (f"; raw PDF SHA-256 `{source['sha256_raw_pdf_bytes']}`" if source.get("sha256_raw_pdf_bytes") else "")
                     + ". 저장소 원문 캐시 없음.")
    lines += ["", "공식 경기책과 상해 보고는 실제 역사 기준이다. 현재 날짜·상대가 다른 대체 경기의 의료 증명은 아니다.",
              "양수 분은 기존 감독 작업 모델의 선택일 뿐 의학적 허가가 아니다. 여섯 경기의 재계산·실제 출전 명단·계약 접수·시즌 확정·원고 게이트는 열지 않았다.",
              "", "재생성: `python tools/build_2021_l2_nonplayoff_roster_scope.py --write`",
              "검증: `python tools/build_2021_l2_nonplayoff_roster_scope.py --check`", ""]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = ap.parse_args()
    packet = build()
    validate(packet, expected=packet)
    body = json.dumps(packet, ensure_ascii=False, indent=2) + "\n"
    note = markdown(packet)
    if args.write:
        OUT.write_text(body, encoding="utf-8", newline="\n")
        MD.write_text(note, encoding="utf-8", newline="\n")
    else:
        assert OUT.read_text(encoding="utf-8") == body
        assert MD.read_text(encoding="utf-8") == note
    print(json.dumps({"dated_team_rosters": len(packet["dated_team_rosters"]),
                      "teams": packet["distinct_teams"], "registration_complete": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
