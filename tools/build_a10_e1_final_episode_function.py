"""Select one bounded late-clock A10 function after current A09 EF-003.

The same permitted fictional team-practice task contains the first failure
and one correction. It is neither a 2024-25 NBA game nor first-option status.
"""

import argparse
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_a10_e1_final_episode_function.py"
OUTPUT = Path("design/A10_E1_FINAL_EPISODE_FUNCTION.json")
CURRENT = "control/G13_CURRENT_FUNCTION_EXECUTION_REGISTER_2026_10_08.json"
PREVIOUS = "design/A09_JOINT_ATTEMPT_SELECTED_EXECUTION_2026_10_08.json"
CF = "design/A10_2024_25_CONDITIONAL_FUNCTIONS.json"
W = "design/A10_LIMITED_CREATION_CLOSING_WORKING_FAMILY_2026_10_07.json"
ROUTINE = "design/A09_A14_LOCAL_ROUTINE_BATCH_2026_10_07.json"
CP2 = "design/CP2_ACT_SUBACT_PACKET.json"
PINS = {
    CURRENT: "6671a0492e88bd9d9db8ac499df265616581d78a467542437f4db6626ca1ec85",
    PREVIOUS: "038b0227a74c7abbb94061776f9cf5c0cc33841bd6de3d5694ffdb6f7341b3be",
    CF: "5cc22b948e12f37581d354e3fa9b508522d0c87968bbd9fc3892b8bacaafa437",
    W: "caabcd6b0341d090a0a0144f52a52f8ad45424e987940a30797fa1ace957c45a",
    ROUTINE: "34b146d68364dde7692adc4631c889f563add7d67149a2963cbc423799206e8b",
    CP2: "2b291bca588302cbb254fc3417652f7d7532c46d7094221cdcceac60619c9db9",
}


def norm_sha(path):
    data = path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return sha256(data.encode("utf-8")).hexdigest()


def load(root, name):
    return json.loads((root / name).read_text(encoding="utf-8-sig"))


def physical(root, name):
    return json.loads((root / name).read_bytes().decode("utf-8-sig"))


def build(root=ROOT):
    for name, expected in PINS.items():
        assert norm_sha(root / name) == expected, f"source changed: {name}"
    current, previous, cf, working, routine, cp2 = (load(root, name) for name in (CURRENT, PREVIOUS, CF, W, ROUTINE, CP2))
    for name, value in zip((CURRENT, PREVIOUS, CF, W, ROUTINE, CP2), (current, previous, cf, working, routine, cp2)):
        assert value == physical(root, name), f"loader differs from physical {name}"
    assert current["counts"]["registered_local_functions"] == 45
    assert current["counts"]["subacts_with_verified_local_function_route"] == 27
    last = current["functions"][-1]
    prior = previous["functions"][-1]
    assert last["id"] == prior["episode_function_id"] == "A09-EF-003"
    assert last["exact_exit"] == prior["exit_state"]
    assert last["exact_exit"] == "협력에서 필요한 자기 역할과 NBA 카운터의 제한 시험을 다음 연차로 가져가지만 개인 기술·몸 관리·관계 과제는 남는다"
    assert not previous["public_tournament_game_performance_selected"]
    assert not current["whole_g13_complete"] and not current["manuscript_allowed"]
    candidate = next(x for x in cf["functions"] if x["id"] == "A10-CF01")
    w1 = next(x for x in working["units"] if x["id"] == "A10-W1")
    r1 = next(x for x in routine["rows"] if x["id"] == "A10-RF-001")
    source_s1 = next(x for x in cp2["subacts"] if x["id"] == "A10-S1")
    act = next(x for x in cp2["acts"] if x["id"] == "A10")
    assert candidate["entry_state"] == last["exact_exit"]
    assert candidate["changed_state"] == "짧은 직접 공격과 중단할 조건을 시험하지만 첫 옵션 지위와 효율은 별도 증명이 필요하다"
    assert candidate["next"] == "A10-CF02" and not candidate["selected_event"]
    assert w1["source"] == ["A10-S1", "A10-CF01"] and working["local_working_family_prepared"]
    assert not working["whole_A10_or_subacts_certified"] and not working["new_final_functions_registered"]
    assert r1["source_subact"] == "A10-S1" and r1["local_routine_observation_selected"]
    assert not r1["source_whole_subact_exit_certified"]
    assert source_s1["choice"] == "전환이 막혀도 즉시 공을 반납하는 데 그치지 않고 늦은 시계에서 가능한 짧은 자가 창조를 시험한다"
    assert source_s1["cost"] == "짧은 자가 창조 반복"
    assert source_s1["exit_state"] == "첫 선택지의 공격 증거"
    assert (act["allocation_start"], act["allocation_end"]) == (513, 582)

    beats = [
        {
            "id": "A10-S1-L1",
            "objective": "8초짜리 가상 팀 반코트 과제에서 정렬된 수비를 향해 오른쪽 미드포스트의 기존 짧은 발동작 뒤 한 번 운반한다",
            "opposition_and_action": "주수비는 길을 지키고 안쪽 도움수비가 발을 먼저 놓는다. 주인공은 자기 길을 더 확인하려다 열린 측면 동료에게 늦게 공을 돌린다.",
            "visible_other_response": "측면 동료가 공을 받았을 때 연습시계에는 2초가 남는다. 동료의 슛이나 생각은 보이지 않는다.",
            "observable_failure": "자기 운반 지연이 같은 동료의 다음 결정 시간을 줄였다",
            "classification": "SELECTED_FICTIONAL_TEAM_PRACTICE_FAILURE_NOT_NBA_GAME",
        },
        {
            "id": "A10-S1-L2",
            "objective": "코치가 같은 위치·8초 시계·한 번 운반 제한으로 과제를 다시 연다",
            "opposition_and_action": "주인공이 안쪽 도움수비의 첫 발을 먼저 보고 깊은 돌파를 멈춘 뒤 열린 측면으로 공을 보낸다.",
            "visible_other_response": "같은 측면 동료가 5초를 남기고 공을 받아 다음 결정을 시작할 수 있다. 슛·득점 결과는 배정하지 않는다.",
            "observable_correction": "첫 표본보다 공을 세 초 빨리 넘긴 한 번의 제한 수정이며 수비가 달라지면 재검증이 필요하다",
            "classification": "SELECTED_FICTIONAL_BOUNDED_RETRY_NOT_FIRST_OPTION_CERTIFICATION",
        },
    ]
    assert beats[0]["visible_other_response"].find("2초") >= 0
    assert beats[1]["visible_other_response"].find("5초") >= 0
    return {
        "schema": "A10_E1_FINAL_EPISODE_FUNCTION_V1",
        "status": "SELECTED_LOCAL_FINAL_FUNCTION_PENDING_INDEPENDENT_REVIEW",
        "independent_review_completed": False,
        "episode_function_id": "A10-EF-001",
        "global_function_order": 46,
        "planned_allocation_slot": 513,
        "primary_subact": "A10-S1",
        "source_conditional_function": "A10-CF01",
        "source_working_unit": "A10-W1",
        "prior_routine_reused_in_same_task": "A10-RF-001 first failed try; L2 is one correction inside the same authorized practice task",
        "previous_function": {"id": last["id"], "path": PREVIOUS, "record_pointer": "/functions/1", "exact_full_exit": last["exact_exit"]},
        "entry_state": last["exact_exit"],
        "single_function": "막힌 전환 뒤 짧은 자가 창조를 시험하고 동료에게 넘기는 시점을 한 번 수정한다",
        "fictional_access_selection": "2024–25 Chicago 코치가 같은 팀의 가용한 다섯 명에게 한 번의 비공개 8초 반코트 과제와 동일조건 재시도를 허용한다. 실제 2024–25 명단·경기 가용·부상·계약은 이 선택으로 확정하지 않는다.",
        "unit_choice": candidate["choice"],
        "direct_present_cost": candidate["direct_cost"] + " 첫 표본에서 본인이 공을 오래 잡아 동료의 남은 연습시계가 2초가 되는 현재 비용을 보이고, 같은 과제 재시도에 다른 전환 반복 한 번을 쓰며 다음 표본에서는 5초를 남긴다.",
        "beats": beats,
        "information_access": "주인공의 공 소유·수비 발위치·보이는 연습시계·동료 공 수신·코치가 허용한 과제만. 코치의 비공개 평가, 동료 내면, 실제 NBA 게임 통계나 미래 계약은 알지 못한다.",
        "exit_state": candidate["changed_state"],
        "source_cp2_exit": source_s1["exit_state"],
        "bounded_first_option_evidence_observed": True,
        "whole_A10_S1_first_option_success_certified": False,
        "next_conditional_function": candidate["next"],
        "new_2024_25_health_or_team_contract_selection": False,
        "actual_2024_25_NBA_game_or_coach_evaluation_certified": False,
        "public_tournament_2023_game_or_medal_military_certified": False,
        "new_MVP_year_title_team_move_or_major_author_result": False,
        "registered_final_function_increment": 0,
        "whole_A10_complete": False, "whole_g13_complete": False, "whole_g14_complete": False,
        "actual_context_packs": 0, "manuscript_count": 0, "manuscript_allowed": False,
        "design_gate": "CLOSED", "new_author_lock": False,
        "source_hash_method": "SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF",
        "source_sha256": {SELF: norm_sha(root / SELF), **PINS},
    }


def render(data):
    lines = ["# A10-EF-001 · 늦은 시계의 한정 자가 창조", "",
             "2024–25 Chicago 가상 비공개 팀 훈련의 동일 과제 두 표본이다. 첫 실패와 한 번의 수정은 국소 기능이며 실제 NBA 경기·첫 옵션 권한·시즌 효율은 아니다.", "",
             f"- 정확 진입: {data['entry_state']}",
             f"- 기능: {data['single_function']}",
             f"- 허용: {data['fictional_access_selection']}",
             f"- 선택: {data['unit_choice']}",
             f"- 현재 비용: {data['direct_present_cost']}", ""]
    for b in data["beats"]:
        lines += [f"- {b['id']}: {b['objective']} {b['opposition_and_action']} {b['visible_other_response']}"]
    lines += ["", f"정확 출구: {data['exit_state']}",
              f"원 CP2 소막 출구: {data['source_cp2_exit']} (반복 실전/첫 옵션 권한 미검증)", "",
              "계획 슬롯 513은 출판 회차가 아니다. 현재45 등록부에 이 기능을 넣지 않았다. 독립검문 전 등록 증분0, 전체 A10/G13/G14·Pack·원고0, 게이트 CLOSED.", ""]
    return "\n".join(lines)


def validate(data, root=ROOT):
    try:
        return [] if data == build(root) else ["A10 local function differs from source-bound selection"]
    except (AssertionError, KeyError, OSError, TypeError, ValueError, IndexError) as exc:
        return [f"source construction: {exc}"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (ROOT / OUTPUT.with_suffix(".md")).write_text(render(data), encoding="utf-8")
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors = validate(saved)
        if (ROOT / OUTPUT.with_suffix(".md")).read_text(encoding="utf-8") != render(saved):
            errors.append("Markdown differs")
        print(json.dumps({"current": not errors, "errors": errors}, ensure_ascii=False))
        if errors:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
