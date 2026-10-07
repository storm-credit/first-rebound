"""Project registered A10–A14 local functions without selecting future history."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_a10_a14_local_blueprint_bundle.py"
OUT = "design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json"
REG = "control/G13_A14_FUNCTION_EXECUTION_REGISTER_2026_10_08.json"
STORY = "canon/STORY_BIBLE.md"
CAREER = "canon/CAREER_TIMELINE.md"
CP2 = "design/CP2_ACT_SUBACT_PACKET.json"
ENDING = "design/ENDING_THEME.md"
PREVIOUS = "design/A09_JOINT_ATTEMPT_SELECTED_EXECUTION_2026_10_08.json"
SKILL = "C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md"
FUNCTION_PATHS = [
    "design/A10_E1_FINAL_EPISODE_FUNCTION.json",
    "design/A10_S2_S3_LOCAL_FUNCTION_SUPPORT_2026_10_08.json",
    "design/A11_E1_FINAL_EPISODE_FUNCTION.json",
    "design/A11_S2_S3_A12_S1_DELEGATED_FUNCTION_EXECUTION_2026_10_08.json",
    "design/A12_S2_S3_A13_S1_DELEGATED_FUNCTION_EXECUTION_2026_10_08.json",
    "design/A13_S2_S3_DELEGATED_FUNCTION_EXECUTION_2026_10_08.json",
    "design/A14_S1_S2_S3_DELEGATED_FUNCTION_EXECUTION_2026_10_08.json",
]
CF_PATHS = {a: f"design/{a}_{window}_CONDITIONAL_FUNCTIONS.json" for a, window in (
    ("A10", "2024_25"), ("A11", "2025_26"), ("A12", "2026_27"),
    ("A13", "2027_28"), ("A14", "2028_35"))}
STABLE_JSON = [CP2, PREVIOUS, *FUNCTION_PATHS, *CF_PATHS.values()]
STABLE_TEXT = [ENDING, "design/HOUSE_STYLE_FOUNDATION.md", "context-packs/README.md", SKILL]
MUTABLE = [REG, STORY, CAREER]
SNAPSHOT_NOTE = "Committed historical full files; current G13 and Canon authority is checked by the separate relevant semantic projection."
HOLD_BY_ACT = {
    "A10": "첫옵션의 실제 경기·시리즈 증거, 클로징 우선순위와 첫 우승창의 팀 결과는 이 국소 연습만으로 성립하지 않는다.",
    "A11": "지속 영향·실제 파이널 진출/패배·라이벌 수비 선택의 시리즈 결과와 후속 계약은 국소 시험 밖이다.",
    "A12": "인물/기능 비용 설명은 계약 수락·명단 재편·벤치 건강과 파이널 재대결 결과가 아니다.",
    "A13": "잠긴 결말 기능 A13-CF04의 실제 결승 수비·리바운드·전진·패스·동료 득점·승리는 아직 수행되지 않았다.",
    "A14": "후배의 독립 준비 표본과 Chicago 원클럽 은퇴의 잠긴 기능을 구분하며, 정확 은퇴 시점·동료 교체·두 번째 우승은 미선택이다.",
}


def path(name):
    p = Path(name)
    return p if p.is_absolute() else ROOT / p


def normalized(name):
    return path(name).read_bytes().removeprefix(b"\xef\xbb\xbf").replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha(name):
    return hashlib.sha256(normalized(name)).hexdigest()


def read(name):
    return json.loads(path(name).read_text(encoding="utf-8-sig"))


def physical(name):
    return json.loads(normalized(name).decode("utf-8"))


def meaning_sha(value):
    b = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(b).hexdigest()


def committed_sha(head, name):
    b = subprocess.check_output(["git", "show", f"{head}:{name}"], cwd=ROOT)
    b = b.removeprefix(b"\xef\xbb\xbf").replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(b).hexdigest()


def verify_snapshot(s):
    assert set(s) == {"git_head_at_creation", "full_file_sha256_at_creation", "meaning"}
    assert s["meaning"] == SNAPSHOT_NOTE
    assert set(s["full_file_sha256_at_creation"]) == set(MUTABLE)
    head = s["git_head_at_creation"]
    assert isinstance(head, str) and len(head) == 40 and all(c in "0123456789abcdef" for c in head)
    for name in MUTABLE:
        assert s["full_file_sha256_at_creation"][name] == committed_sha(head, name), name


def snapshot():
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    s = {"git_head_at_creation": head,
         "full_file_sha256_at_creation": {name: sha(name) for name in MUTABLE},
         "meaning": SNAPSHOT_NOTE}
    verify_snapshot(s)
    return s


def source_line(rows, prefix):
    hits = [x for x in rows if x.startswith(prefix)]
    assert len(hits) == 1, f"Missing or ambiguous relevant Canon line: {prefix}"
    return hits[0]


def current_meaning(reg):
    assert reg["design_gate"] == "CLOSED" and reg["manuscript_allowed"] is False
    assert reg["whole_g13_complete"] is False and reg["whole_g14_complete"] is False
    assert reg["actual_context_packs"] == 0
    rr = sorted((x for x in reg["functions"] if 45 <= x["order"] <= 60), key=lambda x: x["order"])
    assert [x["order"] for x in rr] == list(range(45, 61))
    story = normalized(STORY).decode("utf-8").splitlines()
    career = normalized(CAREER).decode("utf-8").splitlines()
    return {
        "live_function_rows_A09_EF003_to_A14_EF003": rr,
        "current_register_scope": {k: reg[k] for k in ("design_gate", "manuscript_allowed", "whole_g13_complete", "whole_g14_complete", "actual_context_packs")},
        "current_story_anchors": [source_line(story, p) for p in (
            "| 결말의 증명 |", "- 장기 경로는 Chicago 원클럽 프랜차이즈다.")],
        "current_career_anchors": [source_line(career, p) for p in (
            "- 기존 `Atlanta 5시즌=저사용 연결자→두 번째 팀에서 S급` 배정은 폐기 분기 계산 이력으로만 보존한다.",
            "- 2019-20부터 은퇴까지의 정확한 팀·계약·전성기·우승창·쇠퇴·은퇴 연표")],
    }


def sources():
    return {name: read(name) for name in [*STABLE_JSON, REG]}


def check_sources(s):
    assert set(s) == set([*STABLE_JSON, REG])
    assert s == {name: physical(name) for name in s}, "Returned source differs from physical file"
    assert "FUNCTION LOCKED, HISTORICAL COORDINATES HOLD" in normalized(ENDING).decode("utf-8")
    assert "동료가 결승 득점한다" in normalized(ENDING).decode("utf-8")
    assert "결말의 동료는 최소 세 Act" in normalized(ENDING).decode("utf-8")
    assert "ACTUAL_VERIFIED" in normalized("context-packs/README.md").decode("utf-8")
    skill = normalized(SKILL).decode("utf-8")
    assert all(k in skill for k in ("## 13. ★계층형 장편 설계 파이프라인",
                                   "## 21. ★설계 메모와 본문은 같은 판본을 가리켜야 한다",
                                   "## 22. ★파일 존재와 실행 권위를 분리한다"))
    house = normalized("design/HOUSE_STYLE_FOUNDATION.md").decode("utf-8")
    assert "S1 위임 선택" in house and "S1 선택이 개별 회차 POV 잠금은 아니다" in house
    return current_meaning(s[REG])


def source_function_and_pointer(source, ident):
    rows = source.get("functions", [source])
    hits = [(i, x) for i, x in enumerate(rows) if x.get("id", x.get("episode_function_id")) == ident]
    assert len(hits) == 1, ident
    i, f = hits[0]
    pointer = f"/functions/{i}" if "functions" in source else "/"
    return f, pointer


def selected_choice(f):
    return f.get("unit_choice", f.get("choice"))


def selected_cost(f):
    return f.get("direct_present_cost", f.get("source_direct_cost"))


def cf_rows(f, s, act):
    ids = f.get("source_conditional_functions", f.get("source_conditional_function"))
    if isinstance(ids, str):
        ids = [ids]
    assert ids and isinstance(ids, list)
    src = {x["id"]: x for x in s[CF_PATHS[act]]["functions"]}
    rows = [src[x] for x in ids]
    assert all(x["subact"] == f["primary_subact"] for x in rows)
    return [{"id": x["id"], "choice": x["choice"], "direct_cost": x["direct_cost"],
             "information_access": x["information_access"], "original_status": x["status"]} for x in rows]


def build(s, old_snapshot=None):
    live = check_sources(s)
    if old_snapshot is None:
        old_snapshot = snapshot()
    verify_snapshot(old_snapshot)
    rr = live["live_function_rows_A09_EF003_to_A14_EF003"]
    assert rr[0]["id"] == "A09-EF-003" and rr[0]["exact_exit"] == s[PREVIOUS]["functions"][1]["exit_state"]
    cp_sub = {x["id"]: x for x in s[CP2]["subacts"]}
    cp_act = {x["id"]: x for x in s[CP2]["acts"]}
    records = []
    for prior, row in zip(rr, rr[1:]):
        ident = row["id"]
        source = row["path"]
        assert source in FUNCTION_PATHS
        f, pointer = source_function_and_pointer(s[source], ident)
        act = ident[:3]
        sub = f["primary_subact"]
        located = s[source]["functions"][int(pointer.split("/")[-1])] if pointer != "/" else s[source]
        assert located == f, f"Source pointer does not identify selected function: {ident}"
        assert sub == row["subact"] and f["global_function_order"] == row["order"]
        assert f["planned_allocation_slot"] == row["planned_slot"]
        assert f["entry_state"] == row["exact_entry"] == prior["exact_exit"]
        assert f["exit_state"] == row["exact_exit"]
        original = cp_sub[sub]
        assert f.get("source_cp2_exit", f.get("cp2_exact_exit")) == original["exit_state"]
        assert not f.get("local_blueprint", {}).get("status") == "ACTUAL_VERIFIED", ident
        beats = f["beats"]
        assert beats and all("id" in b for b in beats)
        records.append({
            "id": ident, "global_function_order": row["order"],
            "planned_allocation_slot_not_episode_number": row["planned_slot"],
            "primary_subact": sub, "source_function_path": source,
            "source_function_json_pointer": pointer,
            "source_generation_status_is_historical": s[source]["status"],
            "registered_current_function_row": row,
            "exact_previous_function_id": prior["id"],
            "exact_entry_equal_prior_exit": row["exact_entry"],
            "single_function": f["single_function"],
            "selected_local_choice": selected_choice(f),
            "selected_direct_present_cost": selected_cost(f),
            "source_beats_ordered_unmodified": beats,
            "beat_ids": [x["id"] for x in beats],
            "exact_local_exit": f["exit_state"],
            "selected_function_information_access_if_present": f.get("information_access"),
            "original_CF_information_and_scope": cf_rows(f, s, act),
            "original_CP2_subact": {k: original[k] for k in ("id", "choice", "cost", "exit_state", "primary_device")},
            "local_exit_equals_full_CP2_subact_exit_literal": f["exit_state"] == original["exit_state"],
            "full_CP2_subact_exit_certified_by_this_blueprint": False,
            "new_beat_event_or_score_added": False,
            "actual_future_roster_health_contract_title_award_or_retirement_certified": False,
            "individual_episode_POV_locked": False,
            "published_episode_number": None,
        })
    assert len(records) == 15 and [x["global_function_order"] for x in records] == list(range(46, 61))
    assert [x["id"] for x in records] == [f"{act}-EF-00{n}" for act in ("A10", "A11", "A12", "A13", "A14") for n in (1, 2, 3)]
    act_comparison = []
    for act in ("A10", "A11", "A12", "A13", "A14"):
        a = cp_act[act]
        local = next(x for x in records if x["id"] == f"{act}-EF-003")
        act_comparison.append({"act": act, "cp2_window": a["window"],
                               "original_act_choice": a["choice"], "original_act_cost": a["cost"],
                               "original_act_exit": a["exit_state"],
                               "last_registered_local_exit": local["exact_local_exit"],
                               "full_original_act_exit_certified_by_local_blueprint": False,
                               "remaining_finite_history_or_ending_condition": HOLD_BY_ACT[act]})
    locked = next(x for x in s[CF_PATHS["A13"]]["functions"] if x["id"] == "A13-CF04")
    assert locked["subact"] == "A13-S3"
    final, final_pointer = source_function_and_pointer(s[FUNCTION_PATHS[-1]], "A14-EF-003")
    assert final_pointer == "/functions/2"
    assert final["one_club_retirement_function_preserved"] is True
    assert final["retirement_event_or_date_executed"] is False
    assert final["successor_identity_or_future_career_selected"] is False
    return {
        "schema": "G13_A10_A14_SOURCE_BOUND_LOCAL_BLUEPRINT_BUNDLE_V1",
        "status": "PENDING_INDEPENDENT_BLUEPRINT_COMPARISON_NOT_ACTUAL_VERIFIED",
        "registered_source_function_count": 15,
        "existing_embedded_ACTUAL_VERIFIED_in_these_fifteen": 0,
        "new_episode_functions_or_events": 0,
        "records": records,
        "act_exit_comparisons": act_comparison,
        "ending_boundary": {
            "ending_source": ENDING,
            "A13_CF04_locked_function_source": CF_PATHS["A13"],
            "A13_CF04_original_choice": locked["choice"],
            "A13_CF04_original_cost": locked["direct_cost"],
            "winning_pass_teammate_score_and_team_win_performed": False,
            "recipient_and_exact_Finals_year_selected": False,
            "A14_one_club_retirement_function_preserved": True,
            "A14_retirement_event_or_date_executed": False,
            "A14_successor_independent_preparation_local_witness_only": True,
        },
        "information_and_revision": {
            "global_style_direction": "S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY",
            "individual_episode_POV_or_exact_dialogue_selected": False,
            "third_party_mind_private_board_future_winner_access": False,
            "source_hash_method": "UTF8_BOM_STRIPPED_CRLF_CR_TO_LF_SHA256",
            "stable_source_sha256": {name: sha(name) for name in [*STABLE_JSON, *STABLE_TEXT]},
            "historical_full_file_snapshot": old_snapshot,
            "current_relevant_canon_register_projection": live,
            "current_relevant_projection_sha256": meaning_sha(live),
            "producer_sha256": sha(SELF),
        },
        "scope": {"blueprint_independent_review_completed": False,
                  "ACTUAL_VERIFIED_status_granted_by_writer": False,
                  "full_history_and_act_exits_certified": False,
                  "whole_G13_G14_complete": False,
                  "actual_context_packs": 0,
                  "manuscript_allowed": False,
                  "new_author_lock": False,
                  "design_gate": "CLOSED"},
    }


def render(d):
    lines = ["# A10–A14 등록 15기능 국소 Blueprint", "",
             f"상태: `{d['status']}`. 검문 전 ACTUAL_VERIFIED, 역사 실제 경기, 막 전체 출구로 승격하지 않는다.", "",
             "| 순서 | 기능 / 소막 | 원 Beat | 국소 출구 범위 |", "|---:|---|---|---|"]
    for x in d["records"]:
        lines.append(f"| {x['global_function_order']} | {x['id']} / {x['primary_subact']} | {', '.join(x['beat_ids'])} | 원기능의 행동·비용까지만 |")
    lines += ["", "## 막 전체 출구와 구분", ""]
    for x in d["act_exit_comparisons"]:
        lines.append(f"- {x['act']}: 원 CP2 출구 `{x['original_act_exit']}`. {x['remaining_finite_history_or_ending_condition']}")
    lines += ["", "A13-CF04의 잠긴 결승 패스·동료 득점은 아직 실제 결승 관측이 아니다. A14의 후배 독립 준비 표본은 원클럽 은퇴의 정확 시점·후속 경력을 선택하지 않는다.",
              "계획 슬롯은 출판 회차가 아니다. 실제 Context Pack0, 원고0, 전체 G13/G14 미완, 게이트 CLOSED.", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    old = physical(OUT)["information_and_revision"]["historical_full_file_snapshot"] if a.check and not a.write and path(OUT).exists() else None
    d = build(sources(), old)
    if a.write:
        path(OUT).write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        path(OUT.replace(".json", ".md")).write_text(render(d), encoding="utf-8", newline="\n")
    if a.check:
        assert physical(OUT) == d
        assert path(OUT.replace(".json", ".md")).read_text(encoding="utf-8") == render(d)
    print(json.dumps({"current": True, "registered_source_functions": len(d["records"]),
                      "new_events": 0, "actual_context_packs": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
