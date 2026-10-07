"""Project the thirteen already registered A06–A09 functions as local Blueprints."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_a06_a09_remaining_blueprint_bundle.py"
OUT = "design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json"
REGISTER = "control/G13_A14_FUNCTION_EXECUTION_REGISTER_2026_10_08.json"
STORY = "canon/STORY_BIBLE.md"
CAREER = "canon/CAREER_TIMELINE.md"
CP2 = "design/CP2_ACT_SUBACT_PACKET.json"
A06 = "design/A06_2020_21_FINITE_FUNCTION_BATCH_2026_10_07.json"
A07 = "design/A07_FINITE_FUNCTION_BATCH_2026_10_07.json"
A08 = "design/A08_FINITE_FUNCTION_BATCH_2026_10_07.json"
A09_E1 = "design/A09_E1_FINAL_EPISODE_FUNCTION.json"
A09_JOINT = "design/A09_JOINT_ATTEMPT_SELECTED_EXECUTION_2026_10_08.json"
A09_COND = "design/A09_S2_S3_CONDITIONAL_FINAL_FUNCTIONS_2026_10_07.json"
CF_PATHS = {
    "A06": "design/A06_2020_21_CONDITIONAL_FUNCTIONS.json",
    "A07": "design/A07_2021_22_CONDITIONAL_FUNCTIONS.json",
    "A08": "design/A08_2022_23_CONDITIONAL_FUNCTIONS.json",
    "A09": "design/A09_2023_24_CONDITIONAL_FUNCTIONS.json",
}
JOIN = "design/A06_A08_A09_CURRENT_SEASON_EXIT_JOIN_2026_10_08.json"
PO23 = "simulation/NBA_2023_SELECTED_FULL_POSTSEASON.json"
PO23_PEER = "reviews/NBA_2023_SELECTED_FULL_POSTSEASON_G11_INDEPENDENT_REVIEW_2026_10_08.json"
H2 = "design/CHICAGO_MINNESOTA_LONG_CAREER_PACKET.md"
H21 = "canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json"
H22 = "canon/DELEGATED_CHICAGO_2022_23_HEALTH_ROLES_2026_10_08.json"
SKILL = "C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md"
STABLE_JSON = [CP2, A06, A07, A08, A09_E1, A09_JOINT, A09_COND, H21, H22,
               *CF_PATHS.values(), JOIN, PO23, PO23_PEER,
               "reviews/A09_JOINT_ATTEMPT_SELECTED_EXECUTION_ROOT_INDEPENDENT_REVIEW_2026_10_08.json"]
STABLE_TEXT = [H2, "design/HOUSE_STYLE_FOUNDATION.md", "context-packs/README.md", SKILL]
MUTABLE = [REGISTER, STORY, CAREER]
SNAPSHOT_NOTE = "Committed full-file historical source; live authority is the separate exact relevant projection."


def path(name):
    p = Path(name)
    return p if p.is_absolute() else ROOT / p


def normalized(name):
    return path(name).read_bytes().removeprefix(b"\xef\xbb\xbf").replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha(name):
    return hashlib.sha256(normalized(name)).hexdigest()


def physical(name):
    return json.loads(normalized(name).decode("utf-8"))


def read(name):
    return json.loads(path(name).read_text(encoding="utf-8-sig"))


def meaning_sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


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


def line(rows, prefix):
    found = [x for x in rows if x.startswith(prefix)]
    assert len(found) == 1, f"Missing/ambiguous relevant Canon line: {prefix}"
    return found[0]


def relevant_live_projection(reg):
    assert reg["design_gate"] == "CLOSED" and reg["manuscript_allowed"] is False
    assert reg["whole_g13_complete"] is False and reg["whole_g14_complete"] is False
    assert reg["actual_context_packs"] == 0
    rr = sorted((x for x in reg["functions"] if 32 <= x["order"] <= 45), key=lambda x: x["order"])
    assert [x["order"] for x in rr] == list(range(32, 46))
    story = normalized(STORY).decode("utf-8").splitlines()
    career = normalized(CAREER).decode("utf-8").splitlines()
    return {
        "live_register_function_rows_32_to_45": rr,
        "live_register_scope": {k: reg[k] for k in ("design_gate", "manuscript_allowed", "whole_g13_complete", "whole_g14_complete", "actual_context_packs")},
        "story_roles_and_joint_attempt": [line(story, p) for p in (
            "- 개막 명단은 `Hutchison→주인공`", "- LaMelo는 첫 가드 교체",
            "- LaVine의 주득점원 지위", "- 두 사람의 공동 국가대표 선택은 2023 아시안게임에서 회수한다.",
            "- 공동 도전은 LOCK이지만 금메달은 LOCK이 아니다.")],
        "career_relative_year_anchors": [line(career, p) for p in (
            "| 2020-21 |", "| 2023 |", "- **2021 여름:**", "- **2021–22:**",
            "- **2022–23 이후:**", "- 두 사람은 2023 Hangzhou 아시안게임 공동 도전을 선택한다.")],
    }


def load_sources():
    return {name: read(name) for name in [*STABLE_JSON, REGISTER]}


def check_sources(s):
    assert set(s) == set([*STABLE_JSON, REGISTER])
    assert s == {name: physical(name) for name in s}, "Returned source differs from physical file"
    assert s[A06]["independent_review_completed"] is True
    assert s[A07]["independent_review_completed"] is True
    assert s[A08]["independent_review_completed"] is True
    assert s[A09_JOINT]["public_tournament_game_performance_selected"] is False
    assert s[A09_JOINT]["public_tournament_legal_classification_selected"] is False
    assert s["reviews/A09_JOINT_ATTEMPT_SELECTED_EXECUTION_ROOT_INDEPENDENT_REVIEW_2026_10_08.json"]["independent_review_completed"] is True
    assert s[PO23_PEER]["independent_review_completed"] is True
    assert s[PO23_PEER]["verdict"] == "BOUNDED_ACCEPTED_FICTIONAL_FIFTEEN_SERIES_AFTER_SOURCE_RETURN_REPAIR"
    assert "2023·2024 2라운드 탈락" in normalized(H2).decode("utf-8")
    assert "ACTUAL_VERIFIED" in normalized("context-packs/README.md").decode("utf-8")
    skill = normalized(SKILL).decode("utf-8")
    assert all(k in skill for k in ("## 13. ★계층형 장편 설계 파이프라인", "## 21. ★설계 메모와 본문은 같은 판본을 가리켜야 한다", "## 22. ★파일 존재와 실행 권위를 분리한다"))
    house = normalized("design/HOUSE_STYLE_FOUNDATION.md").decode("utf-8")
    assert "S1 위임 선택" in house and "S1 선택이 개별 회차 POV 잠금은 아니다" in house
    return relevant_live_projection(s[REGISTER])


def selected_functions(s):
    a06 = s[A06]["functions"]
    a07 = s[A07]["functions"]
    a08 = s[A08]["functions"]
    a9e1 = s[A09_E1]
    a09 = s[A09_JOINT]["functions"]
    chain = [*a06, *a07, *a08, a9e1, *a09]
    ids = [x.get("id", x.get("episode_function_id")) for x in chain]
    assert len(chain) == 14 and len(set(ids)) == 14
    assert [x["global_function_order"] for x in chain] == list(range(32, 46))
    assert [x["planned_allocation_slot"] for x in chain] == [249, 250, 251, 252, 253, 323, 324, 325, 383, 384, 385, 443, 444, 445]
    for prev, cur in zip(chain, chain[1:]):
        assert cur["entry_state"] == prev["exit_state"], (prev.get("id"), cur.get("id"))
    return chain


def original_cf_ids(selected, s):
    ident = selected.get("id", selected.get("episode_function_id"))
    if ident.startswith("A09-EF-00") and ident != "A09-EF-001":
        proposal = next(x for x in s[A09_COND]["functions"] if x["proposed_episode_function_id"] == ident)
        assert proposal["primary_subact"] == selected["primary_subact"]
        assert proposal["entry_state"] == selected["entry_state"]
        return proposal["source_conditional_functions"], "ORIGINAL_CONDITIONAL_IDS_WITH_SELECTED_PRIVATE_EXECUTION_OVERRIDE"
    return selected["source_conditional_functions"], "DIRECT_SELECTED_FUNCTION_SOURCE_IDS"


def physical_function_locator(ident, selected, s):
    act = ident[:3]
    if ident == "A09-EF-001":
        source, pointer, actual = A09_E1, "/", s[A09_E1]
    else:
        source = {"A06": A06, "A07": A07, "A08": A08, "A09": A09_JOINT}[act]
        matches = [(i, x) for i, x in enumerate(s[source]["functions"])
                   if x.get("id", x.get("episode_function_id")) == ident]
        assert len(matches) == 1, f"Function locator ambiguous or missing: {ident}"
        i, actual = matches[0]
        pointer = f"/functions/{i}"
    assert actual == selected, f"Function source body differs from selected chain: {ident}"
    assert actual["entry_state"] == selected["entry_state"]
    assert actual["exit_state"] == selected["exit_state"]
    assert actual["beats"] == selected["beats"]
    assert actual["unit_choice"] == selected["unit_choice"]
    assert actual["direct_present_cost"] == selected["direct_present_cost"]
    return source, pointer


def cf_projection(selected, s):
    ident = selected.get("id", selected.get("episode_function_id"))
    act = ident[:3]
    ids, mapping = original_cf_ids(selected, s)
    rows = {x["id"]: x for x in s[CF_PATHS[act]]["functions"]}
    cf = [rows[x] for x in ids]
    assert [x["subact"] for x in cf] == [selected["primary_subact"]] * len(cf)
    if act in ("A06", "A07", "A08"):
        choices = [x["choice"] for x in cf]
        costs = [x["direct_cost"] for x in cf]
        expected_choices = choices[0] if len(choices) == 1 and isinstance(selected["unit_choice"], str) else choices
        expected_costs = costs[0] if len(costs) == 1 and isinstance(selected["direct_present_cost"], str) else costs
        assert selected["unit_choice"] == expected_choices and selected["direct_present_cost"] == expected_costs
    return {
        "mapping": mapping,
        "original_CF_ids": ids,
        "original_CF_choice_cost_and_information_access": [
            {"id": x["id"], "choice": x["choice"], "direct_cost": x["direct_cost"],
             "information_access": x["information_access"], "status_in_original": x["status"]} for x in cf],
        "selected_function_choice_cost_is_original_literal": act in ("A06", "A07", "A08"),
    }


def selected_po_context(s):
    p = s[PO23]["Chicago_postseason"]
    assert p["opponent"] == "MIL" and p["round"] == "R1" and p["wins"] == {"MIL": 4, "CHI": 0}
    assert p["H2_recommended_R2_not_preserved_as_fake_result"] is True
    return {"historical_H2_recommendation_source": H2,
            "historical_H2_2023_target": "R2 recommendation subject to feasibility",
            "current_selected_source": PO23, "independent_selected_source_review": PO23_PEER,
            "current_selected_2023_CHI_result": {"opponent": p["opponent"], "round": p["round"], "wins": p["wins"], "last_game": p["last_game"]},
            "selected_result_overrides_unrealized_recommendation": True,
            "A08_local_training_beats_are_not_retroactively_NBA_game_wins": True}


def build(s, old_snapshot=None):
    live = check_sources(s)
    if old_snapshot is None:
        old_snapshot = snapshot()
    verify_snapshot(old_snapshot)
    chain = selected_functions(s)
    cp = {x["id"]: x for x in s[CP2]["subacts"]}
    reg = {x["id"]: x for x in live["live_register_function_rows_32_to_45"]}
    records = []
    for prior, f in zip(chain, chain[1:]):
        ident = f.get("id", f.get("episode_function_id"))
        act = ident[:3]
        source_path, source_pointer = physical_function_locator(ident, f, s)
        row = reg[ident]
        assert row["order"] == f["global_function_order"] and row["planned_slot"] == f["planned_allocation_slot"]
        assert row["exact_entry"] == f["entry_state"] and row["exact_exit"] == f["exit_state"]
        c = cp[f["primary_subact"]]
        assert c["id"] == f["primary_subact"]
        records.append({
            "function_id": ident,
            "global_function_order": f["global_function_order"],
            "planned_allocation_slot_not_episode_number": f["planned_allocation_slot"],
            "primary_subact": f["primary_subact"],
            "source_function_path": source_path,
            "source_function_json_pointer": source_pointer,
            "exact_prior_id": prior.get("id", prior.get("episode_function_id")),
            "exact_prior_exit_and_entry": f["entry_state"],
            "single_function": f["single_function"],
            "selected_unit_choice": f["unit_choice"],
            "selected_direct_present_cost": f["direct_present_cost"],
            "source_beats_ordered_unmodified": f["beats"],
            "beat_ids": [x["id"] for x in f["beats"]],
            "exact_exit": f["exit_state"],
            "reader_question_at_end": f.get("reader_question_at_end"),
            "cp2_target": {"choice": c["choice"], "cost": c["cost"], "exit_state": c["exit_state"], "primary_device": c["primary_device"]},
            "original_conditional_information": cf_projection(f, s),
            "relative_clock": {"A06": "2020–21 Chicago selected season, local role beats only",
                               "A07": "2021–22 Chicago M1/H21 role family, routine coach trial",
                               "A08": "2022–23 contract and training family; separate selected 2022-10-19 bounded game-call witness",
                               "A09": "2023 joint-attempt private practice and Chicago return; public tournament games unselected"}[act],
            "current_season_join_pointer": JOIN if act in ("A06", "A08", "A09") else None,
            "information_access_boundary": "Protagonist's own acts, directly observed court/film and actually delivered role/agent information only; no private third-party mind or future board.",
            "global_S1_close_third_selected_individual_scene_POV_not_locked": True,
            "source_beat_or_new_event_added": False,
            "exact_game_or_practice_date_invented": False,
            "actual_historical_NBA_or_public_tournament_play_certified": False,
            "whole_subact_or_act_performance_certified_by_this_blueprint": False,
            "actual_context_pack_created": False,
        })
    assert len(records) == 13 and [x["global_function_order"] for x in records] == list(range(33, 46))
    join = s[JOIN]
    a8 = join["A08_selected_contract_and_game_join"]
    h21 = s[H21]["selected"]
    h22 = s[H22]["selected"]
    assert (h21["date_state_count"], h21["normal"], h21["coby_out"]) == (82, 58, 24)
    assert h21["hypothetical_positive_player_availability_adopted"] is True
    assert h22["H22"] == "NORMAL_NO_NEW_SUSTAINED_MAJOR_ABSENCE_IN_WORKING_MODEL"
    assert h22["date_keys"] == 82 and h22["registered_TWO_WAY"] == ["Devon Dotson", "Tyler Cook"]
    assert h22["player_minutes"]["Protagonist"] == 32 and h22["TW_active_game_count"] == 0
    assert a8["selected_dated_game_key"] == "PUBLISHED_2022_0007" and a8["date"] == "2022-10-19"
    assert a8["selected_winner_preserved"] == "MIA" and a8["calls_are_fictional_observations_not_actual_NBA_possessions"] is True
    assert len(a8["new_bounded_coached_game_calls"]) == 5 and a8["elapsed_sample_seconds"] == 100
    assert s[A09_JOINT]["institutional_execution"]["public_tournament_game_performance_selected"] is False
    return {
        "schema": "G13_A06_A09_REMAINING_SOURCE_BOUND_BLUEPRINT_BUNDLE_V1",
        "status": "PENDING_INDEPENDENT_BLUEPRINT_COMPARISON_NOT_ACTUAL_VERIFIED",
        "first_A06_EF001_embedded_or_separate_bundle_preserved": True,
        "source_function_count": 13,
        "new_episode_function_count": 0,
        "records": records,
        "selected_season_authority_separate_from_local_beats": {
            "2021_22_source": H21, "82_date_states": {"NORMAL": h21["normal"], "COBY_OUT": h21["coby_out"]},
            "2022_23_source": H22, "working_role_template": h22["role_template"],
            "2022_23_protagonist_regulation_minutes_per_template": h22["player_minutes"]["Protagonist"],
            "actual_clinical_or_official_player_stat_certified": False,
        },
        "A08_recommendation_vs_selected_result": selected_po_context(s),
        "bounded_A08_later_game_call_context_not_rewriting_training_beats": {
            "source": JOIN, "selected_game_key": a8["selected_dated_game_key"],
            "date": a8["date"], "winner_preserved": a8["selected_winner_preserved"],
            "five_calls": [x["id"] for x in a8["new_bounded_coached_game_calls"]],
            "fictional_sample_seconds": a8["elapsed_sample_seconds"],
            "actual_NBA_play_by_play_or_score_certified": False,
        },
        "A09_private_vs_public_boundary": {
            "source": A09_JOINT,
            "selected_private_joint_practice_and_return": s[A09_JOINT]["fictional_private_joint_training_and_return_selected"],
            "public_tournament_game_performance_selected": False,
            "public_tournament_legal_classification_selected": False,
            "medal_military_result_selected": False,
        },
        "revision": {"source_hash_method": "UTF8_BOM_STRIPPED_CRLF_CR_TO_LF_SHA256",
                     "stable_source_sha256": {name: sha(name) for name in [*STABLE_JSON, *STABLE_TEXT]},
                     "historical_full_file_snapshot": old_snapshot,
                     "current_relevant_canon_register_projection": live,
                     "current_relevant_projection_sha256": meaning_sha(live),
                     "producer_sha256": sha(SELF)},
        "scope": {"blueprint_independent_review_completed": False,
                  "ACTUAL_VERIFIED_status_granted_by_this_writer": False,
                  "registered_function_count_changed": False,
                  "future_act_or_G13_final_exit_certified": False,
                  "whole_G13_G14_complete": False,
                  "actual_context_packs": 0,
                  "manuscript_allowed": False,
                  "new_author_lock": False,
                  "design_gate": "CLOSED"},
    }


def render(d):
    rows = ["# A06–A09 남은 13기능 국소 Blueprint", "",
            f"상태: `{d['status']}`. 원 기능의 Beat·선택·현재 비용·정확 인계를 투영한다. 독립 검문 전 ACTUAL_VERIFIED로 올리지 않는다.", "",
            "| 순서 | 기능 / 소막 | 원 Beat | 상대 시간 |", "|---:|---|---|---|"]
    for x in d["records"]:
        rows.append(f"| {x['global_function_order']} | {x['function_id']} / {x['primary_subact']} | {', '.join(x['beat_ids'])} | {x['relative_clock']} |")
    rows += ["", "A08의 예전 H2 2023 2라운드 추천은 현재 선택된 MIL 상대 1라운드 0–4 결과보다 우선하지 않는다. 원 훈련 Beat는 뒤 게임 호출의 실제 NBA 플레이를 소급 인증하지 않는다.",
             "A09의 비공개 공동훈련·귀환은 공개 대회 경기 출전, 금메달 또는 병역 결과를 뜻하지 않는다. 정확 회차·경기/훈련일, 원고와 실제 Context Pack은 아직 없다.",
             "", "원 계획 슬롯은 출판 회차가 아니다. 막 전체 출구·G13 최종 배치·원고 허가는 별도이며 게이트는 CLOSED다.", ""]
    return "\n".join(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    saved = physical(OUT)["revision"]["historical_full_file_snapshot"] if a.check and not a.write and path(OUT).exists() else None
    d = build(load_sources(), saved)
    if a.write:
        path(OUT).write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        path(OUT.replace(".json", ".md")).write_text(render(d), encoding="utf-8", newline="\n")
    if a.check:
        assert physical(OUT) == d
        assert path(OUT.replace(".json", ".md")).read_text(encoding="utf-8") == render(d)
    print(json.dumps({"current": True, "records": len(d["records"]), "new_events": 0, "packs": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
