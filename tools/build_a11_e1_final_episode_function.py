"""Select one bounded A11 S1 off-ball practice function after A10 EF-003."""

import argparse
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_a11_e1_final_episode_function.py"
OUT = Path("design/A11_E1_FINAL_EPISODE_FUNCTION.json")
REGISTER = "control/G13_A10_THREE_FUNCTION_REGISTER_2026_10_08.json"
PREVIOUS = "design/A10_S2_S3_LOCAL_FUNCTION_SUPPORT_2026_10_08.json"
CF = "design/A11_2025_26_CONDITIONAL_FUNCTIONS.json"
ROUTINE = "design/A09_A14_LOCAL_ROUTINE_BATCH_2026_10_07.json"
CP2 = "design/CP2_ACT_SUBACT_PACKET.json"
PINS = {
    REGISTER: "def711fd705443c7e7bcce53996e2d825b99ae973e42b211b0e3385033d57bd9",
    PREVIOUS: "91e887856ce31873686d3e13c4f46de22ca88768f4142f94d0faf285d5fcec95",
    CF: "b8cab9a9e80de5713824493805839fdd485212d25d6582f7df04c8f8604aa8b2",
    ROUTINE: "34b146d68364dde7692adc4631c889f563add7d67149a2963cbc423799206e8b",
    CP2: "2b291bca588302cbb254fc3417652f7d7532c46d7094221cdcceac60619c9db9",
}


def normalized_text(path):
    return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def digest(path):
    return sha256(normalized_text(path).encode("utf-8")).hexdigest()


def load(root, name):
    return json.loads((root / name).read_text(encoding="utf-8-sig"))


def physical(root, name):
    return json.loads(normalized_text(root / name))


def by_id(rows, ident):
    return next(x for x in rows if x["id"] == ident)


def build(root=ROOT):
    for path, pin in PINS.items():
        assert digest(root / path) == pin, f"source changed: {path}"
    register, previous, cf, routine, cp2 = (load(root, name) for name in PINS)
    for path, value in zip(PINS, (register, previous, cf, routine, cp2)):
        assert value == physical(root, path), f"loader differs from physical {path}"
    assert register["counts"]["registered_local_functions"] == 48
    prior = previous["functions"][1]
    assert prior["episode_function_id"] == register["functions"][-1]["id"] == "A10-EF-003"
    assert prior["exit_state"] == register["functions"][-1]["exact_exit"]
    assert prior["exit_state"] == "자기 공격과 동료 기능의 공백을 함께 다음 준비에 가져가지만 우승 자격·최우선 권한·팀 결과는 확정되지 않는다"
    assert not register["whole_g13_complete"] and not register["whole_g14_complete"]
    assert not prior["whole_A10_complete"] and not prior["actual_NBA_game_score_shot_closing_role_certified"]
    candidate = by_id(cf["functions"], "A11-CF01")
    r1 = by_id(routine["rows"], "A11-RF-001")
    s1 = by_id(cp2["subacts"], "A11-S1")
    act = by_id(cp2["acts"], "A11")
    assert (act["allocation_start"], act["allocation_end"]) == (583, 647)
    assert candidate["entry_state"] == prior["exit_state"]
    assert candidate["next"] == "A11-CF02" and not candidate["selected_event"]
    assert candidate["choice"] == "받은 공격수비 과제를 코치에게 확인하고 직접 시작을 동료에게 넘길 구간에서 스크린·컷·리바운드 준비로 다시 관여하려 한다"
    assert candidate["direct_cost"] == "직접 공을 소유하고 첫 수비를 모두 맡는 자기 표본을 일부 줄이고 공 없는 움직임의 몸·시간을 쓴다"
    assert candidate["changed_state"] == "직접 시작을 줄인 구간에서도 관여를 시험하지만 분담의 성공과 상대 압박에 대한 지속성은 별개다"
    assert r1["source_candidate_ids"] == [candidate["id"]] and r1["local_routine_observation_selected"]
    assert not r1["source_whole_subact_exit_certified"] and not r1["registered_by_this_packet"]
    assert s1["choice"] == "온볼과 POA를 모두 최대 출력으로 떠안지 않고 동료와 업무를 나누며 무볼 재배치로 관여한다"
    assert s1["cost"] == "온볼·POA 업무 분담" and s1["exit_state"] == "무볼 재배치로 영향 유지"
    beats = [
        {
            "id": "A11-S1-O1",
            "assignment_and_action": "2025–26 Chicago 가상 비공개 팀 연습에서 코치는 첫 공격 시작과 다음 수비 첫 압박을 한 사람이 모두 맡는 표본을 허용한다. 주인공이 첫 공을 오래 운반하고 바로 첫 공 수비까지 따라간다.",
            "visible_failure": "그 두 직접 과제 뒤 주인공이 약한 쪽 리바운드 준비 위치에 늦게 도착해 연습용 공이 먼저 그 구역을 지나간다. 공 소유·득점·실제 경기 통계는 배정하지 않는다.",
            "present_cost": "자기 시작과 첫 수비를 모두 쥐려는 동안 다음 관여의 위치 준비를 잃는다.",
        },
        {
            "id": "A11-S1-O2",
            "assignment_and_action": "코치가 같은 제한 과제를 다시 열자 주인공은 첫 공격 공을 동료에게 넘기고 그 동료의 진행선에 한 번 스크린을 건 뒤 빈 쪽으로 컷한다. 다음 수비의 첫 압박은 전달된 동료 몫으로 두고 자신은 리바운드 준비 위치로 이동한다.",
            "visible_correction": "동료가 첫 공을 운반하고 주인공은 스크린 뒤 빈 공간을 지나 공 없는 리바운드 자리까지 먼저 닿는다. 실제 리바운드 획득·동료 득점·지속 효율은 보이지 않는다.",
            "present_cost": "자기 첫 공 소유와 첫 수비 압박 표본 한 번을 동료에게 양보하고 스크린·컷·리바운드 위치에 몸과 시간을 쓴다.",
        },
    ]
    return {
        "schema": "A11_E1_FINAL_EPISODE_FUNCTION_V1",
        "status": "SELECTED_LOCAL_FINAL_FUNCTION_PENDING_INDEPENDENT_REVIEW",
        "independent_review_completed": False,
        "episode_function_id": "A11-EF-001", "global_function_order": 49,
        "planned_allocation_slot": 583, "primary_subact": "A11-S1",
        "source_conditional_function": candidate["id"], "source_selected_routine": r1["id"],
        "prior_routine_reused_in_same_task": "A11-RF-001 is the O2 split-role action, not an extra later episode",
        "previous_function": {"id": prior["episode_function_id"], "path": PREVIOUS, "record_pointer": "/functions/1", "exact_full_exit": prior["exit_state"]},
        "entry_state": prior["exit_state"],
        "single_function": "직접 공격 시작과 첫 수비 압박을 분담하고 스크린·컷·리바운드 위치로 다시 관여하는 한정 시험",
        "fictional_access_selection": "2025–26 Chicago 코치가 가용한 팀 동료와 비공개 두 표본 훈련을 허용한다는 국소 가상 선택이다. 특정 시즌 명단·건강·공식 출전·MVP 연도·시리즈 결과는 선택하지 않는다.",
        "unit_choice": candidate["choice"],
        "direct_present_cost": candidate["direct_cost"] + " 첫 표본에서 다음 리바운드 위치를 놓치고 두 번째에는 자신의 첫 공·첫 압박 표본을 실제로 양보한다.",
        "beats": beats,
        "information_access": "본인의 공 소유·첫 수비 압박·코치가 전달한 분담·보이는 동료 운반과 리바운드 자리만. 동료 내면, 비공개 평가, 실제 경기 통계·시즌 결과는 모른다.",
        "exit_state": candidate["changed_state"],
        "source_cp2_exit": s1["exit_state"],
        "bounded_off_ball_reposition_observed": True,
        "whole_A11_S1_sustained_impact_certified": False,
        "next_conditional_function": candidate["next"],
        "actual_2025_26_NBA_game_score_minutes_or_health_certified": False,
        "MVP_year_or_Finals_loss_selected": False,
        "new_major_author_result_or_team_move_selected": False,
        "registered_final_function_increment": 0,
        "whole_A11_complete": False, "whole_g13_complete": False, "whole_g14_complete": False,
        "actual_context_packs": 0, "manuscript_count": 0, "manuscript_allowed": False,
        "design_gate": "CLOSED", "new_author_lock": False,
        "source_hash_method": "SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF",
        "source_sha256": {SELF: digest(root / SELF), **PINS},
    }


def markdown(data):
    lines = ["# A11-EF-001 · 온볼 분담 뒤 무볼 재배치", "",
             "검문된 A10-EF-003의 정확 출구에서 이어지는 2025–26 Chicago 가상 비공개 팀 과제 두 표본이다. A11-RF-001의 이미 선택된 동작을 두 번째 표본으로 소비하며 별도 사건으로 중복하지 않는다.", "",
             f"- 진입: {data['entry_state']}", f"- 기능: {data['single_function']}",
             f"- 허용: {data['fictional_access_selection']}", f"- 선택: {data['unit_choice']}",
             f"- 현재 비용: {data['direct_present_cost']}", ""]
    for beat in data["beats"]:
        lines += [f"- {beat['id']}: {beat['assignment_and_action']} {beat.get('visible_failure', beat.get('visible_correction'))} {beat['present_cost']}"]
    lines += ["", f"정확 출구: {data['exit_state']}",
              f"원 CP2 소막 출구: {data['source_cp2_exit']} — 공 없는 위치 한 번의 관측만이며 지속 효율은 미증명.", "",
              "계획 slot 583은 출판 회차가 아니다. 기능49 등록 증분0. MVP연도·파이널 패배·공식 시즌결과를 선택하지 않는다. 전체 A11/G13/G14·Pack·원고0, CLOSED.", ""]
    return "\n".join(lines)


def validate(data, root=ROOT):
    try:
        return [] if data == build(root) else ["A11 local function differs from source-bound selection"]
    except (AssertionError, KeyError, OSError, TypeError, ValueError, IndexError) as exc:
        return [f"source construction: {exc}"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (ROOT / OUT.with_suffix(".md")).write_text(markdown(data), encoding="utf-8")
    if args.check:
        saved = load(ROOT, str(OUT))
        errors = validate(saved)
        if normalized_text(ROOT / OUT.with_suffix(".md")) != markdown(saved):
            errors.append("Markdown differs")
        print(json.dumps({"current": not errors, "errors": errors}, ensure_ascii=False))
        if errors:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
