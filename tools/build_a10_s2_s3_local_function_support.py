"""Select bounded A10 S2/S3 practice functions after reviewed A10 EF-001.

These functions select visible private-practice actions, not 2024–25 NBA
closing authority, first-option status, a playoff series, or a title.
"""

import argparse
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_a10_s2_s3_local_function_support.py"
OUT = Path("design/A10_S2_S3_LOCAL_FUNCTION_SUPPORT_2026_10_08.json")
REGISTER = "control/G13_A10_FUNCTION_EXECUTION_REGISTER_2026_10_08.json"
E1 = "design/A10_E1_FINAL_EPISODE_FUNCTION.json"
CF = "design/A10_2024_25_CONDITIONAL_FUNCTIONS.json"
WORKING = "design/A10_LIMITED_CREATION_CLOSING_WORKING_FAMILY_2026_10_07.json"
CP2 = "design/CP2_ACT_SUBACT_PACKET.json"
PINS = {
    REGISTER: "32680a5b29052ac3d6e3c267ad1acb9ede37f4741c0180fbe71cd22035cc634d",
    E1: "78f109d927d07e111f06a9bcb277cd0d7ecdfb867a184c6761f2dfe2d433eaf8",
    CF: "5cc22b948e12f37581d354e3fa9b508522d0c87968bbd9fc3892b8bacaafa437",
    WORKING: "caabcd6b0341d090a0a0144f52a52f8ad45424e987940a30797fa1ace957c45a",
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
    return next(row for row in rows if row["id"] == ident)


def build(root=ROOT):
    for name, pin in PINS.items():
        assert digest(root / name) == pin, f"source changed: {name}"
    reg, e1, cf, work, cp2 = (load(root, name) for name in PINS)
    for name, value in zip(PINS, (reg, e1, cf, work, cp2)):
        assert value == physical(root, name), f"loader differs from physical {name}"
    assert reg["counts"]["registered_local_functions"] == 46
    assert reg["functions"][-1]["id"] == e1["episode_function_id"] == "A10-EF-001"
    assert reg["functions"][-1]["exact_exit"] == e1["exit_state"]
    assert e1["exit_state"] == "짧은 직접 공격과 중단할 조건을 시험하지만 첫 옵션 지위와 효율은 별도 증명이 필요하다"
    assert not reg["whole_g13_complete"] and not reg["whole_g14_complete"]
    assert not e1["whole_A10_complete"] and not e1["actual_2024_25_NBA_game_or_coach_evaluation_certified"]

    c2, c3, c4 = (by_id(cf["functions"], key) for key in ("A10-CF02", "A10-CF03", "A10-CF04"))
    w2, w3 = (by_id(work["units"], key) for key in ("A10-W2", "A10-W3"))
    s2, s3 = (by_id(cp2["subacts"], key) for key in ("A10-S2", "A10-S3"))
    act = by_id(cp2["acts"], "A10")
    assert (act["allocation_start"], act["allocation_end"]) == (513, 582)
    assert c2["entry_state"] == e1["exit_state"]
    assert c2["next"] == c3["id"] and c2["changed_state"] == c3["entry_state"]
    assert c3["next"] == c4["id"] and c3["changed_state"] == c4["entry_state"]
    assert c4["next"] == "A11-S1"
    assert c2["choice"] == "허용된 영상의 자기 공격과 동료의 강점을 대조해 코치에게 제한된 클로징 시험 범위를 제안하고 실제 맡은 역할 안에서 직접 공격과 이양을 시험하려 한다"
    assert c3["choice"] == "받은 수비 과제를 유지하며 자신의 공격을 동료에게 이양할 구간을 시험하고 실제 부담이 드러나면 코치에게 조정할 과제를 구체적으로 설명하려 한다"
    assert c4["choice"] == "관측된 공백과 자신의 역할을 코치에게 설명하고 허용된 팀 반복에서 연결·수비 교대 중 먼저 고칠 과제를 시험하려 한다"
    assert c2["direct_cost"] == "자신이 모든 마무리를 독점하는 표본을 만들 기회를 줄이고 동료에게 넘긴 공격의 다음 위치를 준비하는 데 시간을 쓴다"
    assert c3["direct_cost"] == "일부 직접 공격을 더 시도할 기회를 내려놓고 그 몸과 시간을 수비 위치·리바운드 준비에 쓴다"
    assert c4["direct_cost"] == "자기 득점 하이라이트를 더 만들 연습 기회 대신 조합에서 먼저 고칠 연결·수비 반복에 시간을 쓴다"
    assert w2["source"] == ["A10-S2", "A10-CF02", "A10-CF03"]
    assert w3["source"] == ["A10-S3", "A10-CF04"]
    assert s2["choice"] == "LaVine의 퇴장을 전제로 자기 승계를 요구하지 않고 관측된 강점에 따라 클로징 역할을 조정할 근거를 제시한다"
    assert s2["cost"] == "클로징 권한 재배분" and s2["exit_state"] == "공동 에이스에서 최우선 코어로"
    assert s3["choice"] == "첫 선택지의 공격이 통해도 우승을 선언하지 않고 베테랑·벤치가 지불하는 역할 비용을 다음 보강 과제로 남긴다"
    assert s3["cost"] == "베테랑·벤치 역할 비용" and s3["exit_state"] == "첫 우승창의 미완성"
    assert not any(x["selected_event"] for x in (c2, c3, c4))

    f47 = {
        "episode_function_id": "A10-EF-002", "global_function_order": 47,
        "planned_allocation_slot": 514, "primary_subact": "A10-S2",
        "source_conditional_functions": ["A10-CF02", "A10-CF03"], "source_working_unit": "A10-W2",
        "previous_function": {"id": e1["episode_function_id"], "path": E1, "exact_full_exit": e1["exit_state"]},
        "entry_state": e1["exit_state"],
        "single_function": "자기 마무리와 동료의 첫 연결을 서로 제한한 국소 과제에서 공격 이양과 수비 복귀 비용을 보인다",
        "fictional_access_selection": "2024–25 Chicago의 한 번의 비공개 팀 과제에 기존 코어 LaMelo·LaVine이 주인공과 함께 참가할 수 있다고 좁게 선택한다. 이는 그날의 가상 연습 동석일 뿐 시즌 건강·명단·계약·공식 클로징 배정이 아니다.",
        "beats": [
            {"id": "A10-S2-C1", "action": "허용된 앞 기능의 자기 운반·이양 표본과 공개된 팀 역할만 다시 본 뒤 코치에게 LaMelo 첫 연결, 자기 짧은 운반, 열린 LaVine 위치로 이양, 곧바로 뒤 수비로 돌아오는 한정 과제를 제안한다.", "observed_other": "코치가 이 비공개 연습의 한정 과제만 허용한다. 공식 경기의 클로징 권한이나 비공개 평가를 전달하지 않는다."},
            {"id": "A10-S2-C2", "action": "LaMelo에게서 첫 연결을 받은 주인공은 짧은 길을 살핀 뒤 도움 발이 길을 닫자 자기 마지막 슛을 포기하고 열린 LaVine 위치로 공을 보낸 다음 뒤 수비 위치를 잡는다.", "observed_other": "LaVine이 공을 받는 것은 보인다. 슛 선택·득점·미래 마무리 권한은 보이지 않는다."},
            {"id": "A10-S2-C3", "action": "같은 허용 과제의 다음 표본에서 LaMelo가 자기 첫 운반 한 구간을 줄여 주인공에게 짧은 시험을 다시 열어 준다. 주인공은 닫힌 길에 매달리지 않고 수비 복귀선에 선다.", "observed_other": "LaMelo의 공 소유 양보와 주인공의 제한 복귀가 직접 보인다. 동료 내면·계약 양보·실전 효율은 알 수 없다."},
        ],
        "unit_choice": c2["choice"] + " " + c3["choice"],
        "direct_present_cost": c2["direct_cost"] + " " + c3["direct_cost"] + " LaMelo도 이 한 과제에서 자기 첫 운반 한 구간을 실제 양보한다.",
        "exit_state": c3["changed_state"],
        "source_cp2_exit": s2["exit_state"],
        "bounded_mutual_cost_observed": True,
        "whole_A10_S2_closing_authority_or_priority_certified": False,
        "next_conditional_function": c4["id"],
    }
    f48 = {
        "episode_function_id": "A10-EF-003", "global_function_order": 48,
        "planned_allocation_slot": 515, "primary_subact": "A10-S3",
        "source_conditional_functions": ["A10-CF04"], "source_working_unit": "A10-W3",
        "previous_function": {"id": f47["episode_function_id"], "path": str(OUT), "record_pointer": "/functions/0", "exact_full_exit": f47["exit_state"]},
        "entry_state": f47["exit_state"],
        "single_function": "자기 공격 뒤 빈 약한 쪽 위치와 동료의 보완 노동을 보고 한 번의 연결·수비 재시험을 선택한다",
        "fictional_access_selection": "앞 허용 과제에 이어 비공개 팀 훈련에서 코치가 약한 쪽 수비 교대와 연결 위치의 한 번의 비교 반복을 허용한다. 특정 2024–25 벤치 명단·공식 시리즈·경기 결과는 선택하지 않는다.",
        "beats": [
            {"id": "A10-S3-B1", "action": "자기 짧은 공격 시도 뒤 주인공의 약한 쪽 첫발이 늦자 가상의 벤치 역할 동료가 그 빈 공간으로 한 걸음 들어와 커터 길을 막으려 한다.", "observed_other": "커터가 먼저 공간에 들어왔고 동료가 그 틈을 메우려 움직이는 순서만 보인다. 상대 득점·동료 판단·전체 벤치 능력은 모른다."},
            {"id": "A10-S3-B2", "action": "주인공은 자기 공격 표본을 한 번 더 만드는 대신 같은 허용 반복에서 커터 출발 위치를 먼저 보고 자기 약한 쪽 발을 앞당긴 뒤 연결 위치로 돌아간다.", "observed_other": "동료는 앞 표본에서처럼 같은 빈 공간을 급히 메우지 않고 지정 연결선에 남는다. 한 번의 수비·연결 수정이지 득점 저지나 시즌 조합 개선은 아니다."},
        ],
        "unit_choice": c4["choice"],
        "direct_present_cost": c4["direct_cost"] + " 첫 표본에서는 동료가 자기 지연 때문에 한 걸음 추가 보완해야 했고, 재시험에는 자기 공격 반복 한 차례를 썼다.",
        "exit_state": c4["changed_state"],
        "source_cp2_exit": s3["exit_state"],
        "bounded_bench_role_cost_and_correction_observed": True,
        "whole_A10_S3_series_or_title_window_certified": False,
        "next_subact": c4["next"],
    }
    for row in (f47, f48):
        row.update({
            "classification": "SELECTED_FICTIONAL_PRIVATE_TEAM_PRACTICE_LOCAL_FUNCTION_PENDING_INDEPENDENT_REVIEW",
            "independent_review_completed": False, "registered_final_function_increment": 0,
            "information_access": "본인 움직임·공 소유·보이는 동료 위치·코치의 전달된 훈련 지시·허용 영상만. 동료 내면, 감독의 비공개 평가·실전 배정, 시즌 건강·계약·결과는 모른다.",
            "actual_NBA_game_score_shot_closing_role_certified": False,
            "whole_A10_complete": False, "whole_g13_complete": False, "whole_g14_complete": False,
            "actual_context_packs": 0, "manuscript_count": 0, "manuscript_allowed": False,
            "new_MVP_year_title_team_move_or_major_author_result": False,
        })
    assert f47["entry_state"] == e1["exit_state"]
    assert f48["entry_state"] == f47["exit_state"]
    assert f48["exit_state"] == c4["changed_state"]
    return {
        "schema": "A10_S2_S3_LOCAL_FUNCTION_SUPPORT_V1",
        "status": "TWO_BOUNDED_FUNCTIONS_PENDING_INDEPENDENT_REVIEW_NOT_REGISTERED",
        "source_scope": "One selected fictional private Chicago practice family, not 2024–25 NBA season/game or closing authority",
        "functions": [f47, f48],
        "cp2_whole_exit_scope": {"A10-S2": "최우선 코어·공식 클로징 배정 미증명", "A10-S3": "첫 우승창·시리즈별 약점·전체 벤치 비용 미증명"},
        "fictional_practice_co_presence_selected": True,
        "actual_2024_25_health_contract_roster_or_NBA_game_certified": False,
        "public_2023_tournament_game_certified": False,
        "new_final_functions_registered": 0,
        "whole_A10_complete": False, "whole_g13_complete": False, "whole_g14_complete": False,
        "actual_context_packs": 0, "manuscript_count": 0, "manuscript_allowed": False,
        "design_gate": "CLOSED", "new_author_lock": False,
        "source_hash_method": "SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF",
        "source_sha256": {SELF: digest(root / SELF), **PINS},
    }


def markdown(data):
    lines = ["# A10-S2/S3 · 비공개 팀 과제의 한정 연결", "",
             "검문된 A10-EF-001의 정확 출구에서 이어지는 2개의 가상 국소 기능이다. 기존 Chicago 코어의 한 차례 연습 동석만 선택했으며 공식 경기 가용성·클로징 권한·계약·시리즈·우승을 정하지 않았다.", ""]
    for row in data["functions"]:
        lines += [f"## {row['episode_function_id']} · {row['primary_subact']}", "",
                  f"진입: {row['entry_state']}", "",
                  f"기능: {row['single_function']}", "",
                  f"허용: {row['fictional_access_selection']}", "",
                  f"선택: {row['unit_choice']}", "",
                  f"현재 비용: {row['direct_present_cost']}", ""]
        for beat in row["beats"]:
            lines += [f"- {beat['id']}: {beat['action']} {beat['observed_other']}"]
        lines += ["", f"정확 출구: {row['exit_state']}",
                  f"원 CP2 소막 출구: {row['source_cp2_exit']} — {data['cp2_whole_exit_scope'][row['primary_subact']]}", ""]
    lines += ["계획 slot 514/515는 출판 회차가 아니다. 47/48 등록 증분 0, 전체 A10/G13/G14·Pack·원고 0, CLOSED. 독립검문 전 가상 국소 기능 두 개는 누적 등록부에 넣지 않는다.", ""]
    return "\n".join(lines)


def validate(data, root=ROOT):
    try:
        return [] if data == build(root) else ["A10 S2/S3 output differs from source-bound selection"]
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
