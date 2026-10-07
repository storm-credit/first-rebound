"""Build the first uncovered source-bound G13 Blueprint and its finite queue."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_a06_local_blueprint_bundle.py"
BUNDLE = "design/A06_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json"
QUEUE = "design/G13_VERIFIED_BLUEPRINT_FINITE_BUILD_QUEUE_2026_10_08.json"
SKILL = "C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md"
FIRST = "design/A06_2020_21_FINITE_FUNCTION_BATCH_2026_10_07.json"
CF = "design/A06_2020_21_CONDITIONAL_FUNCTIONS.json"
PREVIOUS = "design/A05_E4_FINAL_EPISODE_FUNCTION.json"
CP2 = "design/CP2_ACT_SUBACT_PACKET.json"
REGISTER = "control/G13_A14_FUNCTION_EXECUTION_REGISTER_2026_10_08.json"
STABLE_PATHS = [FIRST, CF, PREVIOUS, CP2, "design/HOUSE_STYLE_FOUNDATION.md",
                "context-packs/README.md", SKILL]
MUTABLE_PATHS = [REGISTER, "canon/STORY_BIBLE.md", "canon/CAREER_TIMELINE.md"]
SNAPSHOT_MEANING = ("Historical full-file hashes record the creation snapshot; "
                    "current authority is checked through the exact live projection below.")
ACT_BATCHES = {
    "A06": FIRST,
    "A07": "design/A07_FINITE_FUNCTION_BATCH_2026_10_07.json",
    "A08": "design/A08_FINITE_FUNCTION_BATCH_2026_10_07.json",
    "A09": "design/A09_JOINT_ATTEMPT_SELECTED_EXECUTION_2026_10_08.json",
}


def path(name: str) -> Path:
    p = Path(name)
    return p if p.is_absolute() else ROOT / p


def normalized(name: str) -> bytes:
    return path(name).read_bytes().removeprefix(b"\xef\xbb\xbf").replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha(name: str) -> str:
    return hashlib.sha256(normalized(name)).hexdigest()


def read(name: str):
    return json.loads(path(name).read_text(encoding="utf-8-sig"))


def physical_json(name: str):
    return json.loads(normalized(name).decode("utf-8"))


def pretty(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def meaning_sha(value) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def current_mutable_meaning(reg):
    story = normalized("canon/STORY_BIBLE.md").decode("utf-8").splitlines()
    career = normalized("canon/CAREER_TIMELINE.md").decode("utf-8").splitlines()
    def line(rows, start):
        matches = [x for x in rows if x.startswith(start)]
        assert len(matches) == 1, f"Ambiguous or missing canon anchor: {start}"
        return matches[0]
    actor = next(x for x in reg["functions"] if x["id"] == "A06-EF-001")
    assert reg["design_gate"] == "CLOSED" and reg["manuscript_allowed"] is False
    return {
        "live_register_A06_function": actor,
        "live_register_design_gate": reg["design_gate"],
        "live_register_manuscript_allowed": reg["manuscript_allowed"],
        "story_role_lines": [line(story, prefix) for prefix in (
            "- 개막 명단은 `Hutchison→주인공`",
            "- 주인공은 3년차 선발 SF/PF",
            "- LaMelo는 첫 가드 교체",
            "- LaVine의 주득점원 지위",
            "- Coby는 LaMelo 선발 전환 뒤에도",
            "- LaMelo Chicago BASE는")],
        "career_role_row": line(career, "| 2020-21 |"),
        "career_A_trade_approval_override": line(career, "A Theis·Green의 3팀 5인 선수 이동은"),
    }


def full_snapshot():
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    result = {"git_head_at_creation": head,
              "full_file_sha256_at_creation": {name: sha(name) for name in MUTABLE_PATHS},
              "meaning": SNAPSHOT_MEANING}
    # This creation currently uses a clean committed source snapshot. A dirty mutable
    # ancestor requires a separate preserved snapshot, not a plausible-looking SHA.
    verify_snapshot(result)
    return result


def verify_snapshot(snapshot):
    assert set(snapshot) == {"git_head_at_creation", "full_file_sha256_at_creation", "meaning"}
    assert snapshot["meaning"] == SNAPSHOT_MEANING
    assert set(snapshot["full_file_sha256_at_creation"]) == set(MUTABLE_PATHS)
    head = snapshot["git_head_at_creation"]
    assert isinstance(head, str) and len(head) == 40 and all(c in "0123456789abcdef" for c in head)
    for name in MUTABLE_PATHS:
        committed = subprocess.check_output(["git", "show", f"{head}:{name}"], cwd=ROOT)
        committed = committed.removeprefix(b"\xef\xbb\xbf").replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert hashlib.sha256(committed).hexdigest() == snapshot["full_file_sha256_at_creation"][name], (
            f"Historical snapshot does not match committed file: {name}")


def sources():
    return {name: read(name) for name in (FIRST, CF, PREVIOUS, CP2, REGISTER)}


def check_sources(s):
    # The returned loader and its expected data do not share a mutable object.
    assert s == {name: physical_json(name) for name in s}, "Returned source differs from physical input"
    first = s[FIRST]
    f = first["functions"][0]
    old = s[PREVIOUS]
    reg = s[REGISTER]
    assert reg["design_gate"] == "CLOSED" and reg["manuscript_allowed"] is False
    cp = next(x for x in s[CP2]["subacts"] if x["id"] == "A06-S1")
    assert first["independent_review_completed"] is True
    assert f["id"] == "A06-EF-001" and f["global_function_order"] == 32
    assert f["planned_allocation_slot"] == 249 and f["primary_subact"] == "A06-S1"
    assert f["source_conditional_functions"] == ["A06-CF01", "A06-CF02"]
    assert first["previous_function"]["exact_full_exit"] == old["exit_state"] == f["entry_state"]
    assert [(b["id"], b["classification"]) for b in f["beats"]] == [
        ("A06-R1-B1", "SELECTED_BOUNDED_FICTIONAL_ACTION_WITH_EXISTING_RESULT_BACKGROUND"),
        ("A06-R1-B2", "SELECTED_BOUNDED_FICTIONAL_ACTION_WITH_EXISTING_RESULT_BACKGROUND")]
    cfs = [next(x for x in s[CF]["functions"] if x["id"] == k) for k in f["source_conditional_functions"]]
    assert f["unit_choice"] == [x["choice"] for x in cfs]
    assert f["direct_present_cost"] == [x["direct_cost"] for x in cfs]
    assert cp["choice"] == "LaMelo와 공격 시작 지점을 구분하고 자기 운반이 줄어드는 포제션에서는 다음 관여 위치를 만든다"
    assert cp["cost"] == "자기 운반 빈도"
    assert cp["exit_state"] == "각자 시작하는 공격을 구분"
    row = next(x for x in reg["functions"] if x["id"] == f["id"])
    assert row["path"] == FIRST and row["order"] == 32 and row["planned_slot"] == 249
    assert row["exact_entry"] == f["entry_state"] and row["exact_exit"] == f["exit_state"]
    skill = normalized(SKILL).decode("utf-8")
    for literal in ("## 13. ★계층형 장편 설계 파이프라인", "## 21. ★설계 메모와 본문은 같은 판본을 가리켜야 한다", "## 22. ★파일 존재와 실행 권위를 분리한다"):
        assert literal in skill
    assert "ACTUAL_VERIFIED" in normalized("context-packs/README.md").decode("utf-8")
    story = normalized("canon/STORY_BIBLE.md").decode("utf-8")
    career = normalized("canon/CAREER_TIMELINE.md").decode("utf-8")
    assert "LaMelo는 첫 가드 교체" in story and "Coby의 초기 PG 시험" in story
    assert "LaVine의 주득점원 지위" in story and "LaMelo Chicago BASE" in story
    assert "2020-21" in career and "LaMelo" in career
    return f, cfs, cp


def build_bundle(s, historical_snapshot=None):
    f, cfs, cp = check_sources(s)
    if historical_snapshot is not None:
        verify_snapshot(historical_snapshot)
    mutable_meaning = current_mutable_meaning(s[REGISTER])
    return {
        "schema": "G13_SOURCE_BOUND_LOCAL_BLUEPRINT_BUNDLE_V1",
        "status": "PHYSICAL_UNVERIFIED_PENDING_INDEPENDENT_COMPARISON",
        "target_function": f["id"],
        "function_order": f["global_function_order"],
        "planned_allocation_slot": f["planned_allocation_slot"],
        "published_episode_number": None,
        "source_batch_status": s[FIRST]["status"],
        "source_batch_independent_review_completed": True,
        "this_blueprint_independent_review_completed": False,
        "embedded_source_blueprint_exists": False,
        "single_function": f["single_function"],
        "entry_state": f["entry_state"],
        "unit_choice": f["unit_choice"],
        "direct_present_cost": f["direct_present_cost"],
        "beats": f["beats"],
        "beat_order": [x["id"] for x in f["beats"]],
        "exit_state": f["exit_state"],
        "next_question": f["reader_question_at_end"],
        "previous_function": s[FIRST]["previous_function"],
        "cp2_source": {"id": cp["id"], "choice": cp["choice"], "cost": cp["cost"],
                       "exit_state": cp["exit_state"], "primary_device": cp["primary_device"]},
        "conditional_source_rows": [{"id": x["id"], "choice": x["choice"],
                                     "direct_cost": x["direct_cost"],
                                     "information_access": x["information_access"],
                                     "status_in_original": x["status"]} for x in cfs],
        "information_boundary": {
            "global_style_direction": "S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY",
            "individual_scene_pov_verified": False,
            "protagonist_may_access": ["본인에게 전달된 역할 설명", "허용된 코트·영상 관측", "자기 운반·이양·다음 위치 행동"],
            "no_access_without_new_witness": ["동료·코치의 비공개 속마음", "프런트 내부 평가", "미래 선발·분·효율·득점·승리"],
            "exact_dialogue": None,
            "exact_game_or_training_date": None,
        },
        "current_canon_anchors": [
            {"path": "canon/STORY_BIBLE.md", "anchor": "Chicago 2020-21 개막 역할 — LOCKED STRUCTURE / PREDEADLINE OUTCOME PASS", "use": "LaMelo 초기 창출·Coby PG 시험·LaVine 득점 유지"},
            {"path": "canon/CAREER_TIMELINE.md", "anchor": "2020-21 3년차 Chicago 역할 행", "use": "소속·연차와 기존 Chicago 성장방향"},
            {"path": "design/HOUSE_STYLE_FOUNDATION.md", "anchor": "S1 주인공 밀착 3인칭 / 정보 접근", "use": "POV 방향만; 개별 장면 POV 인증은 아님"},
        ],
        "revision": {"source_hash_method": "UTF8_BOM_STRIPPED_CRLF_CR_TO_LF_SHA256",
                     "source_sha256": {name: sha(name) for name in STABLE_PATHS},
                     "historical_full_file_snapshot": historical_snapshot or full_snapshot(),
                     "current_relevant_canon_and_register_projection": mutable_meaning,
                     "current_relevant_projection_sha256": meaning_sha(mutable_meaning),
                     "producer_sha256": sha(SELF)},
        "scope_limits": {
            "beat_or_event_added_beyond_existing_function": False,
            "teammate_score_or_ball_acceptance_certified": False,
            "starter_minutes_win_or_future_growth_prepaid": False,
            "full_A06_subact_or_act_exit_certified": False,
            "whole_G13_G14_complete": False,
            "actual_context_packs": 0,
            "manuscript_allowed": False,
            "new_author_lock": False,
            "design_gate": "CLOSED",
        },
    }


def embedded_units(act):
    rows = []
    for p in sorted((ROOT / "design").glob(f"{act}_E*_FINAL_EPISODE_FUNCTION.json")):
        source = p.relative_to(ROOT).as_posix()
        d = read(source)
        assert d == physical_json(source), f"Returned embedded Blueprint differs from physical input: {source}"
        if d.get("episode_function_id") and d.get("local_blueprint", {}).get("status") == "ACTUAL_VERIFIED":
            rows.append({"id": d["episode_function_id"], "source_path": source,
                         "source_sha256": sha(source),
                         "coverage": "EMBEDDED_ACTUAL_VERIFIED_REUSE_SUBJECT_TO_CURRENT_CANON_COMPARISON",
                         "order": d["final_function_order"], "subact": d["primary_subact"],
                         **unit_fields(d)})
    return sorted(rows, key=lambda x: x["order"])


def batch_units(act, source):
    d = read(source)
    assert d == physical_json(source), f"Returned function batch differs from physical input: {source}"
    rows = d["functions"] if "functions" in d else [d]
    out = []
    for x in rows:
        ident = x.get("id", x.get("episode_function_id"))
        order = x.get("global_function_order", x.get("final_function_order"))
        out.append({"id": ident, "source_path": source, "source_sha256": sha(source),
                    "coverage": "FIRST_SOURCE_BOUND_BUNDLE_PENDING_INDEPENDENT_REVIEW" if ident == "A06-EF-001" else "FUNCTION_BEATS_EXIST_BLUEPRINT_INFORMATION_REVISION_CHECK_PENDING",
                    "order": order, "subact": x["primary_subact"], **unit_fields(x)})
    return sorted(out, key=lambda x: x["order"])


def unit_fields(d):
    return {"source_entry": d.get("entry_state", d.get("entry_after_fictional_bridge", d.get("entry_previous_full_exit"))),
            "source_choice": d.get("unit_choice"),
            "source_present_cost": d.get("direct_present_cost"),
            "source_exit": d.get("exit_state"),
            "source_beat_ids": [x["id"] for x in d.get("beats", [])]}


def build_queue(bundle):
    rows = []
    for act in ("A02", "A03", "A04", "A05"):
        rows.extend(embedded_units(act))
    for act in ("A06", "A07", "A08"):
        rows.extend(batch_units(act, ACT_BATCHES[act]))
    a9 = read("design/A09_E1_FINAL_EPISODE_FUNCTION.json")
    assert a9 == physical_json("design/A09_E1_FINAL_EPISODE_FUNCTION.json")
    rows.append({"id": a9["episode_function_id"], "source_path": "design/A09_E1_FINAL_EPISODE_FUNCTION.json",
                 "source_sha256": sha("design/A09_E1_FINAL_EPISODE_FUNCTION.json"),
                 "coverage": "FUNCTION_BEATS_EXIST_BLUEPRINT_INFORMATION_REVISION_CHECK_PENDING",
                 "order": a9["global_function_order"], "subact": a9["primary_subact"], **unit_fields(a9)})
    rows.extend(batch_units("A09", ACT_BATCHES["A09"]))
    assert len(rows) == 36 and [x["order"] for x in rows] == list(range(10, 46))
    assert sum(x["coverage"].startswith("EMBEDDED_ACTUAL_VERIFIED") for x in rows) == 22
    assert rows[22]["id"] == bundle["target_function"] == "A06-EF-001"
    return {"schema": "G13_VERIFIED_BLUEPRINT_FINITE_BUILD_QUEUE_V1",
            "status": "FINITE_COVERAGE_QUEUE_NOT_FINAL_G13_OR_PACK",
            "scope": "A02–A09 source functions in chronological order; existing embedded Blueprints count as coverage",
            "source_hash_method": "UTF8_BOM_STRIPPED_CRLF_CR_TO_LF_SHA256",
            "first_uncovered_target": "A06-EF-001",
            "first_bundle_path": BUNDLE,
            "first_bundle_pending_independent_comparison": True,
            "counts": {"source_functions_A02_to_A09": 36, "existing_embedded_ACTUAL_VERIFIED": 22,
                       "new_bundle_pending_review": 1, "later_function_blueprint_checks_remaining": 13,
                       "actual_context_packs": 0, "new_episode_functions": 0},
            "build_order": [
                {"phase": "A02_TO_A05", "action": "Reuse 22 embedded ACTUAL_VERIFIED Blueprints; compare current Canon and their exact function handoffs, repairing only a concrete revision mismatch."},
                {"phase": "A06_EF001", "action": "Review the new source-bound two-beat Blueprint against the selected A06 batch, CP2, current Canon and information access."},
                {"phase": "A06_REMAINDER_TO_A09", "action": "Project existing registered beats in order and verify revision/access without inventing dates, games, contracts or extra episodes."},
                {"phase": "G13_THEN_G14", "action": "Only after full function/history lock and ACTUAL_VERIFIED local Blueprint may G14 compile actual premanuscript Packs under CLOSED; no manuscript authorization."},
            ],
            "units": rows,
            "next_pending_units_in_exact_order": [x["id"] for x in rows if not x["coverage"].startswith("EMBEDDED_ACTUAL_VERIFIED")],
            "rules": {"planned_slots_are_not_mandatory_new_events": True,
                      "blueprint_file_absence_alone_is_not_a_gap": True,
                      "existing_function_or_embedded_blueprint_overwritten": False,
                      "actual_context_packs": 0, "whole_G13_G14_complete": False,
                      "manuscript_allowed": False, "design_gate": "CLOSED"},
            "producer_sha256": sha(SELF)}


def render_bundle(b):
    return "\n".join(["# A06-EF-001 국소 Blueprint 번들", "", f"상태: `{b['status']}`. 원 기능의 두 Beat를 그대로 투영했으며 독립 비교 전 `ACTUAL_VERIFIED`로 올리지 않는다.", "",
        f"- 진입: {b['entry_state']}", f"- 단일 기능: {b['single_function']}",
        *[f"- {x['id']}: {x['action']}" for x in b['beats']],
        *[f"- 선택: {x}" for x in b['unit_choice']],
        *[f"- 현재 비용: {x}" for x in b['direct_present_cost']],
        f"- 출구: {b['exit_state']}", f"- 다음 질문: {b['next_question']}", "",
        "정보 접근은 본인에게 전달된 역할·코트 관측·자기 행동으로 제한한다. 동료의 득점, 감독의 속마음, 미래 선발·분·승리를 이 기능에서 인증하지 않는다.",
        "원 CP2의 A06-S1 비용과 현행 Chicago 캐논을 함께 핀으로 보존한다. 계획 슬롯249는 출판 회차 번호가 아니다. 실제 Pack0·원고0·CLOSED.", ""])


def render_queue(q):
    return "\n".join(["# G13 A02–A09 Blueprint 유한 구축 순서", "",
        "기존 embedded `ACTUAL_VERIFIED` 22건은 파일이 따로 없다는 이유로 재작성하지 않는다. 현재 캐논과 정확 인계가 실제 맞는지만 비교한다.", "",
        "| 단계 | 유한 작업 |", "|---|---|",
        *[f"| {x['phase']} | {x['action']} |" for x in q['build_order']], "",
        f"첫 신규 대상: `{q['first_uncovered_target']}` → `{q['first_bundle_path']}`. 기존 두 Beat·선택·현재 비용·관측 출구를 투영하며 독립 비교 전 권위는 보류한다.",
        "후속 원기능 순서: " + ", ".join(q["next_pending_units_in_exact_order"]),
        "", "계획 빈 슬롯은 새 사건 의무가 아니다. G13 전체·역사 잠금 전 실제 Context Pack은 0, 원고도 0이며 게이트는 CLOSED다.", ""])


def validate(b, q):
    try:
        s = sources()
        assert b == build_bundle(s, b["revision"]["historical_full_file_snapshot"])
        assert q == build_queue(b)
        return []
    except (AssertionError, KeyError, ValueError, TypeError) as e:
        return [str(e)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    saved_snapshot = None
    if a.check and not a.write and path(BUNDLE).exists():
        saved_snapshot = read(BUNDLE)["revision"]["historical_full_file_snapshot"]
    b = build_bundle(sources(), saved_snapshot)
    q = build_queue(b)
    if a.write:
        for filename, value in ((BUNDLE, pretty(b)), (BUNDLE.replace(".json", ".md"), render_bundle(b)),
                                (QUEUE, pretty(q)), (QUEUE.replace(".json", ".md"), render_queue(q))):
            path(filename).write_text(value, encoding="utf-8", newline="\n")
    if a.check:
        assert read(BUNDLE) == b and read(QUEUE) == q
        assert path(BUNDLE.replace(".json", ".md")).read_text(encoding="utf-8") == render_bundle(b)
        assert path(QUEUE.replace(".json", ".md")).read_text(encoding="utf-8") == render_queue(q)
        assert not validate(b, q)
    print(json.dumps({"current": True, "embedded_reused": 22, "first_new": "A06-EF-001", "new_function_increment": 0, "actual_context_packs": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
