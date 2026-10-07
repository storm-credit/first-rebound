"""Select a bounded Chicago 2021-22 operational availability path, not medical facts."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json"
MARKDOWN = OUTPUT.with_suffix(".md")
CARRIER = "simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json"
AVAILABILITY = "simulation/CHICAGO_2021_22_AVAILABILITY.csv"
CALENDAR = "simulation/CHICAGO_2021_22_CALENDAR.csv"
INPUT_SOURCES = "research/CHICAGO_2021_22_INPUT_SOURCES.json"
DELEGATION = "canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json"
PINS = {
    CARRIER: "73d51b630e9c9d4ec31b7e3952906165589bd8c49a48bb07c79bdc9ad02e8fca",
    AVAILABILITY: "29ac2747811b44f80dcfe3fc21ae8bafac8be54f2fe1f236a070150f0a3d9ca8",
    CALENDAR: "c59ea19a5515d64ed03cae8e0481847b6572d4087bbcefef15896bb7a2489183",
    INPUT_SOURCES: "25851ed46e6c6cc8765b2d6c1400f1a00e8535ce1e916a503fd4d5a9b7893359",
    DELEGATION: "4ee9b74e37903a43b0bd50b35c7f24cbabdac13728097a848b553f874bbeef80",
}


def normalized_sha(path: Path) -> str:
    body = path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def read_inputs():
    for relative, expected in PINS.items():
        assert normalized_sha(ROOT / relative) == expected, f"Source changed: {relative}"
    carrier = json.loads((ROOT / CARRIER).read_text(encoding="utf-8-sig"))
    # The accepted carrier is immutable by its source pin. Check consumed rows
    # below without rerunning its ancestor constructor for every query/check.
    assert len(carrier["rows"]) == 164
    with (ROOT / AVAILABILITY).open(encoding="utf-8-sig", newline="") as stream:
        availability = list(csv.DictReader(stream))
    with (ROOT / CALENDAR).open(encoding="utf-8-sig", newline="") as stream:
        calendar = list(csv.DictReader(stream))
    return carrier, availability, calendar


def choose_state(game_number: int, coby_evidence: dict) -> tuple[str, str]:
    if game_number <= 13:
        assert coby_evidence["evidence"] == "NO_SAME_DAY_ROW"
        return "COBY_OUT", "PRE_RETURN_NO_SAME_DAY_PLAYER_ROW"
    if 14 <= game_number <= 16:
        assert coby_evidence["evidence"] == "OBSERVED_PLAYED"
        assert 0 < int(coby_evidence["source_seconds"]) < 18 * 60
        return "COBY_OUT", "COUNTERFACTUAL_BINARY_FULL_ROLE_DEFERRAL_AFTER_REAL_DEBUT"
    if coby_evidence["evidence"] == "OBSERVED_PLAYED":
        return "NORMAL", "DELEGATED_FULL_ROLE_MODEL_WITH_HISTORICAL_PLAYED_ANCHOR"
    assert coby_evidence["evidence"] in {"NO_SAME_DAY_ROW", "OBSERVED_HEALTH_RESTRICTION"}
    return "COBY_OUT", "DELEGATED_OPERATIONAL_UNAVAILABILITY_NO_NEW_DIAGNOSIS"


def build():
    carrier, availability, calendar = read_inputs()
    assert len(calendar) == 82 and len({x["game_id"] for x in calendar}) == 82
    coby = {x["game_id"]: x for x in availability if x["player"] == "Coby"}
    assert len(coby) == 82
    options = {(x["game_id"], x["state"]): (i, x) for i, x in enumerate(carrier["rows"])}
    assert len(options) == 164
    assert calendar[13]["game_id"] == "0022100209" and coby["0022100209"]["source_seconds"] == "657"
    assert calendar[16]["game_id"] == "0022100250" and int(coby["0022100250"]["source_seconds"]) >= 1080
    selected = []
    for expected_number, game in enumerate(calendar, 1):
        assert int(game["game_number"]) == expected_number
        game_id = game["game_id"]
        history = coby[game_id]
        assert history["date"] == game["date"]
        state, reason = choose_state(expected_number, history)
        carrier_index, row = options[(game_id, state)]
        assert (row["candidate_date"], row["home"], row["away"]) == (game["date"], game["home"], game["away"])
        assert row["conditional_unavailable"] == (["Coby"] if state == "COBY_OUT" else [])
        assert len(row["standard_registered_candidate"]) == 15
        assert len(row["two_way_registered_candidate"]) == 2
        assert len(row["working_active_nominees"]) == 12 and len(row["standard_inactive_nominees"]) == 3
        assert sum(row["player_minutes"].values()) == 240
        observed_seconds = int(history["source_seconds"]) if history["source_seconds"] else None
        selected.append({
            "game_number": expected_number,
            "game_id": game_id,
            "date": game["date"],
            "home": game["home"],
            "away": game["away"],
            "opponent": game["opponent"],
            "selected_chicago_state": state,
            "selection_reason": reason,
            "historical_coby": {
                "evidence": history["evidence"],
                "historical_played": history["evidence"] == "OBSERVED_PLAYED",
                "observed_seconds": observed_seconds,
                "observed_minutes_display": None if observed_seconds is None else f"{observed_seconds // 60}:{observed_seconds % 60:02d}",
                "primary_report_status": history["primary_status"] or None,
                "primary_report_reason": history["primary_reason"] or None,
            },
            "fictional_role_decision": {
                "existing_normal_18minute_role_used": state == "NORMAL",
                "existing_coby_out_absence_candidate_used": state == "COBY_OUT",
                "real_played_not_rewritten": True,
                "medical_reason_certified": False,
            },
            "working_chicago_operational_availability": {
                "positive_minute_players": row["positive_minute_availability_condition"],
                "working_active_nominees": row["working_active_nominees"],
                "standard_inactive_nominees": row["standard_inactive_nominees"],
                "two_way_active_nominees": row["TW_active_nominees"],
                "all_named_players_medically_cleared": None,
                "actual_active_list_or_contract_certified": False,
            },
            "selected_regulation_player_minutes": row["player_minutes"],
            "selected_carrier_source": {"path": CARRIER, "pointer": f"/rows/{carrier_index}"},
            "opponent_29_team_health": {"type": "NOT_MODELED", "player_availability": None},
            "regulation_clock_complete": False,
            "overtime_selected": False,
            "game_result": None,
        })
    states = Counter(x["selected_chicago_state"] for x in selected)
    assert states == {"NORMAL": 58, "COBY_OUT": 24}, states
    assert [(x["game_number"], x["historical_coby"]["observed_seconds"], x["selected_chicago_state"]) for x in selected[13:16]] == [(14, 657, "COBY_OUT"), (15, 629, "COBY_OUT"), (16, 654, "COBY_OUT")]
    assert selected[16]["selected_chicago_state"] == "NORMAL"
    return {
        "id": "CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION_2026_10_07",
        "status": "AUTHOR_DELEGATED_DESIGN_SELECTION_PROPOSED_WITH_82_DATE_STATES_EXECUTED_FOR_ROOT_REVIEW",
        "scope": "Chicago named-player operational availability and existing M1 regulation state only",
        "source_hash_method": "UTF8_BOM_REMOVED_LF_NORMALIZED_SHA256",
        "source_hashes": {**PINS, "tools/build_chicago_2021_22_delegated_health_state.py": normalized_sha(Path(__file__))},
        "official_primary_evidence": [
            {"url": "https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-11-14_05PM.pdf", "locator": "PDF page 3: CHI@LAC / Chicago Bulls / White, Coby / Out / Left Shoulder; Injury Management", "raw_sha256": "ff6dbd0355dd063026af4d93d857d32d41bf38e22ae467f55a4cbe0c14bfb8ee", "raw_bytes": 36062, "temporary_cache": "C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-coby-20211007/Injury-Report_2021-11-14_05PM.pdf", "body_bytes_directly_verified": True},
            {"url": "https://www.nba.com/bulls/game/0022100209-bulls-vs-lakers-los-angeles-ca-11-15-2021", "locator": "Official NBA indexed box table: White 10:57; existing availability CSV records 657 seconds", "raw_sha256": None, "body_bytes_directly_verified": False, "access_limit": "Direct NBA request HTTP 403; web open returned iframe shell. Indexed table and pinned repository mirror only."},
            {"url": "https://www.nba.com/bulls/news/coby-white-and-patrick-williams-injury-updates", "locator": "Bulls 2021-09-24 return expectation; no exact clearance decision imported", "raw_sha256": None, "body_bytes_directly_verified": False, "access_limit": "Direct request blocked; contextual official source only."},
        ],
        "model_choice": {
            "chosen": "58_NORMAL_24_COBY_OUT",
            "basis": "Use real pre-return no-row window as anchor; defer the existing binary full 18-minute role for the first three real limited appearances as an explicit counterfactual; start NORMAL at the first >=18-minute observed return, 2021-11-21. Later no-row/restriction days use operational unavailability, not diagnosis.",
            "alternatives": [
                {"name": "61_NORMAL_21_COBY_OUT", "decision": "not_selected", "reason": "Respects real participation on Nov 15/17/19 but imports the carrier's 18-minute full role into three historical ~10-minute return appearances."},
                {"name": "69_NORMAL_13_COBY_OUT", "decision": "not_selected", "reason": "Treats every date after the first 13 as full-role availability, including documented no-row and observed-restriction days; it overstates support for the binary carrier."},
                {"name": "NEW_LIMITED_STATE", "decision": "possible_later_model", "reason": "Could preserve limited participation on the first three return dates, but requires a new player-minute, donor, lineup and nomination carrier. It is not necessary for this bounded 82-state selection."},
            ],
            "old_H00_copied": False,
            "fictional_absence_on_historical_played_dates": ["2021-11-15", "2021-11-17", "2021-11-19"],
        },
        "summary": {"date_states_executed": 82, "normal": 58, "coby_out": 24, "historical_coby_real_played_but_fictionally_unavailable": 3, "historical_no_row": 18, "historical_health_restriction": 3, "standard_slots_conditional": 15, "two_way_slots_conditional": 2, "opponent_teams_health_modeled": 0},
        "selected_dates": selected,
        "certification": {"working_delegated_recommendation_selected": True, "canonical_delegated_selection_recorded_by_root_at_proposal_generation": False, "root_adoption_record": "canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json", "root_adoption_must_be_checked_separately": True, "accepted_ancestor_constructors_repeated": 0, "actual_medical_or_clinical_clearance": False, "actual_15_plus_2_registration": False, "all_opponent_health_modeled": False, "whole_game_5player_clock": False, "overtime_completed": False, "season_results_selected": False, "new_author_lock": False, "whole_G13_or_G14_complete": False, "actual_context_pack": False, "manuscript_allowed": False, "antigravity_cli_collection": "NOT_RUN_DIRECT_PRIMARY_AND_PINNED_LEDGER_USED"},
    }


def validate(packet):
    try:
        assert packet == build(), "Selected states or source-bound evidence differ from reconstruction"
        return []
    except (AssertionError, KeyError, ValueError, OSError) as exc:
        return [str(exc)]


def markdown(packet):
    s = packet["summary"]
    return "\n".join([
        "# 2021–22 Chicago 위임 건강·가용성 작업 선택", "",
        f"상태: `{packet['status']}`. M1 carrier의 82개 날짜에 **NORMAL {s['normal']}개 / COBY_OUT {s['coby_out']}개**를 배정했다. Chicago의 양수 분 선수와 12명 작업 명단도 각 날짜에서 같은 선택 행에 연결했다. 이는 가상 운영 선택이며 실제 의료 판정이나 법적 명단 인증이 아니다.", "",
        "## 실제 역사와 선택을 분리한 지점", "",
        "- 2021-11-14 NBA 공식 부상 보고서 3쪽은 Coby White를 Out(왼쪽 어깨 관리)으로 적는다. 원 PDF 36,062바이트 SHA-256 `ff6dbd0355dd063026af4d93d857d32d41bf38e22ae467f55a4cbe0c14bfb8ee`를 임시 캐시에 회수했다.",
        "- 실제 11월 15일 Lakers전 Coby의 출전은 10:57이다. 11월 17일 10:29, 19일 10:54도 기존 관측 원장에 있다. 선택한 `COBY_OUT`은 이 세 실제 출전을 부정하지 않는다. 대체 세계에서 18분짜리 기존 NORMAL 역할을 아직 쓰지 않고 **결장을 3경기 연장하는 별도 가상 선택**이다.",
        "- 11월 21일 원장의 실제 출전은 20:59로 첫 NORMAL 선택의 보수적 역할 기준이다. 이후 미출전일을 임상 사유로 단정하지 않고 운영상 비가용으로 모델링했다.",
        "- NBA 게임 페이지의 10:57은 검색 색인과 기존 원장에서 교차했으며 페이지 원바이트는 HTTP 403/iframe 때문에 확보하지 못했다. 원바이트 인증으로 주장하지 않는다.", "",
        "## 비교와 범위", "",
        "- **권고 58/24:** 첫 13경기 OUT, 실제 제한 출전 3경기에는 명시적 대체세계 OUT, 11월 21일부터 출전 앵커가 있는 날짜 NORMAL, 이후 미출전/제한 8경기 OUT.",
        "- **61/21 대안:** 실제 첫 3회 출전을 보존하지만 10분대 관측에 기존 18분 NORMAL을 곧바로 대입한다. 이번에는 선택하지 않았다.",
        "- **69/13 대안:** 첫 13회만 OUT이며 이후의 원장 미출전·제한일도 NORMAL로 놓는다. 기존 원장에 비해 근거가 약하다.",
        "- LIMITED 신규 상태는 이후 donor·5인 블록·명단을 새로 계산하면 가능하다. 현재 82일 상태 연결을 위해 필수 조건으로 만들지 않았다.",
        "- 상대 29팀 가용성은 `NOT_MODELED` typed null이다. Chicago 외 건강·승패·연장·전 경기 시간순 5인 교대·실제 계약/의료·원고 허가는 모두 미완료다. 15+2는 기존 조건부 carrier의 작업 명단이다.", "",
        "## 출처", "",
        "- [NBA 2021-11-14 공식 부상 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-11-14_05PM.pdf), 3쪽.",
        "- [NBA Bulls 2021-11-15 경기표](https://www.nba.com/bulls/game/0022100209-bulls-vs-lakers-los-angeles-ca-11-15-2021): 공식 검색 색인 10:57, 원바이트 미회수.",
        "- [Bulls 복귀 전망 공지](https://www.nba.com/bulls/news/coby-white-and-patrick-williams-injury-updates): 정확 복귀 허가로 사용하지 않음.",
        "- 날짜별 JSON의 `selected_carrier_source.pointer`가 기존 M1 조건부 행으로 연결된다. 원천 파일의 정규화 SHA-256은 JSON `source_hashes`에 기록했다.", "",
    ]) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    packet = build()
    assert validate(packet) == []
    prose = markdown(packet)
    if args.self_test:
        mutated = copy.deepcopy(packet)
        mutated["selected_dates"][13]["selected_chicago_state"] = "NORMAL"
        assert validate(mutated), "Historical first-return / fictional state mutation escaped"
    if args.write:
        OUTPUT.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        MARKDOWN.write_text(prose, encoding="utf-8")
    if args.check:
        assert json.loads(OUTPUT.read_text(encoding="utf-8-sig")) == packet
        assert MARKDOWN.read_text(encoding="utf-8-sig") == prose
    print(f"PASS 82 states NORMAL={packet['summary']['normal']} COBY_OUT={packet['summary']['coby_out']}")


if __name__ == "__main__":
    main()
