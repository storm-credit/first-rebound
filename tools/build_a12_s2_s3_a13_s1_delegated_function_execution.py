"""Select three bounded fictional functions after A12-EF-001."""

import argparse
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_a12_s2_s3_a13_s1_delegated_function_execution.py"
OUT = "design/A12_S2_S3_A13_S1_DELEGATED_FUNCTION_EXECUTION_2026_10_08.json"
SOURCES = {
    "design/A11_S2_S3_A12_S1_DELEGATED_FUNCTION_EXECUTION_2026_10_08.json": "b964d64e7c595dda97bdcb2ebf61c43937e1ea9068be9bac6fb2a55700d89f79",
    "design/A12_2026_27_CONDITIONAL_FUNCTIONS.json": "10b428b9742f356f4a447c2d44e75c1dfdbe891c92669ace30ad399a2a6be2e7",
    "design/A13_2027_28_CONDITIONAL_FUNCTIONS.json": "f0f2add25e5279f01f52366657704dbac0262ef93f43246a72b05c965848da72",
    "design/CP2_ACT_SUBACT_PACKET.json": "2b291bca588302cbb254fc3417652f7d7532c46d7094221cdcceac60619c9db9",
    "design/ENDING_THEME.md": "929807f42a2d1ed0f8229ecf5bb1f2e3f00642732cbaa590cbce630fae0c34f3",
    "control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md": "91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d",
}


def text(path):
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def digest(path):
    return sha256(text(path).encode()).hexdigest()


def physical(root, path):
    return json.loads(text(root / path))


def load(root, path):
    return json.loads((root / path).read_text(encoding="utf-8-sig"))


def source(root):
    for path, expected in SOURCES.items():
        assert digest(root / path) == expected, f"source changed: {path}"
    objects = {path: load(root, path) for path in list(SOURCES)[:4]}
    for path, value in objects.items():
        assert value == physical(root, path), f"returned source differs from physical: {path}"
    assert "더 나은 선택이 동료라면 넘김" in text(root / "design/ENDING_THEME.md")
    assert "승인 코어 안의 루틴 계약 설계" in text(root / "control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md")
    return objects


def row(rows, ident):
    return next(value for value in rows if value["id"] == ident)


def build(root=ROOT):
    s = source(root)
    for path, value in s.items():
        assert value == physical(root, path), f"consumed source differs from physical: {path}"
    prior, a12, a13, cp2 = [s[path] for path in list(SOURCES)[:4]]
    assert prior["selected_function_count"] == 3 and prior["registered_function_increment"] == 0
    last = prior["functions"][-1]
    assert last["id"] == "A12-EF-001" and last["global_function_order_if_registered"] == 52
    assert last["observable_exit"] == "자기 요구와 유지할 기능을 함께 설명하지만 새 계약·동료 감액·이적·벤치 구성이 합의되지는 않는다"
    assert last["actual_NBA_game_or_contract_certified"] is False
    cf2, cf3, cf4 = [row(a12["functions"], ident) for ident in ("A12-CF02", "A12-CF03", "A12-CF04")]
    cf13 = row(a13["functions"], "A13-CF01")
    s2, s3, t1 = [row(cp2["subacts"], ident) for ident in ("A12-S2", "A12-S3", "A13-S1")]
    act12, act13 = [row(cp2["acts"], ident) for ident in ("A12", "A13")]
    assert (act12["allocation_start"], act12["allocation_end"], act13["allocation_start"]) == (648, 705, 706)
    assert cf2["entry_state"] == last["observable_exit"]
    assert cf3["entry_state"] == cf2["changed_state"] and cf2["next"] == cf3["id"]
    assert cf4["entry_state"] == cf3["changed_state"] and cf3["next"] == cf4["id"]
    assert cf13["entry_state"] == cf4["changed_state"] and cf4["next"] == "A13-S1"
    assert [v["selected_event"] for v in (cf2, cf3, cf4, cf13)] == [False] * 4
    assert s2["exit_state"] == "속도와 책임의 분산"
    assert s3["exit_state"] == "재대결을 선지급하지 않음"
    assert t1["exit_state"] == "정답을 알아도 막기 어려운 공격"

    f53 = {
        "id": "A12-EF-002", "global_function_order_if_registered": 53,
        "planned_allocation_slot": 676, "subact": "A12-S2", "candidate_ids": [cf2["id"], cf3["id"]],
        "exact_entry": last["observable_exit"],
        "single_function": "동료마다 다른 속도에서 자기 점유를 줄인 첫 연결과 수비 재배치의 비용을 두 조합으로 시험한다",
        "fictional_setting": "2026–27 날짜 미지정 Chicago 허용 비공개 연습의 두 조합. LaMelo·LaVine이 이 과제에 참여하는 것은 가상 운영 선택이며 미래 정규 명단·계약 합의를 인증하지 않는다.",
        "named_people_and_access": "주인공은 LaMelo의 빠른 안쪽 출발과 LaVine의 늦게 열린 바깥 위치를 직접 본다. 감독은 가상 과제만 준다. 두 동료의 마음·미래 계약이나 실제 경기 출전은 알지 못한다.",
        "goal": "공을 더 오래 잡을 때 동료의 첫 길이 닫히는 비용을 보이고 두 번째 조합에서 짧은 연결 뒤 수비 위치를 맡는다.",
        "obstacle": "첫 조합에서 주인공의 한 번 더 운반이 LaMelo의 출발 통로와 LaVine의 패스 준비 시간을 겹치게 한다.",
        "unit_choice": cf2["choice"] + "; " + cf3["choice"],
        "direct_present_cost": cf2["direct_cost"] + "; " + cf3["direct_cost"],
        "beats": [
            {"id": "V1", "action": "주인공이 첫 조합에서 익숙한 자기 운반을 한 번 더 하다 LaMelo의 안쪽 출발을 늦춘다.", "response": "LaMelo가 멈추고 LaVine은 열려 있던 바깥 수신 위치에서 다시 방향을 바꾼다.", "present_cost": "자기 점유를 유지한 시간이 두 동료의 준비를 지연시킨 불리한 영상으로 남는다."},
            {"id": "V2", "action": "역할을 바꾼 두 번째 조합에서 주인공은 LaVine의 첫 운반 뒤 공을 짧게 LaMelo에게 넘기고 빈 바깥 위치로 움직인다.", "response": "LaMelo는 공을 멈추지 않고 다음 훈련 동료에게 연결한다. 주인공은 수비 전환 신호에 먼저 자기 코너 위치로 돌아간다.", "present_cost": "자기 드리블·슛 반복을 포기하고 연결 후 위치 노동을 맡는다. 득점·승리는 부여하지 않는다."},
        ],
        "intermediate_cf02_exit": cf2["changed_state"], "observable_exit": cf3["changed_state"],
        "cp2_exact_exit": s2["exit_state"],
        "cp2_exit_scope": "두 허용 조합의 속도와 책임 배분만 보였다. 정규시즌 지배·수상·전체 벤치 보강은 미인증.",
        "next_handoff": cf4["id"],
    }
    f54 = {
        "id": "A12-EF-003", "global_function_order_if_registered": 54,
        "planned_allocation_slot": 701, "subact": "A12-S3", "candidate_ids": [cf4["id"]],
        "exact_entry": f53["observable_exit"],
        "single_function": "허용된 수행 영상의 늦은 수비 복귀를 듣고 자신의 반복·휴식 시간을 수정 과제에 사용한다",
        "fictional_setting": "2026–27 연차의 날짜 미지정 비공개 훈련 피드백과 다음 허용 재시험. 실제 플레이오프 진출·탈락, 첫 파이널이나 재대결은 발생 사실로 선택하지 않는다.",
        "named_people_and_access": "가상 감독은 앞선 허용 영상의 주인공 복귀 한 박자 지연만 지적한다. 주인공은 LaMelo의 다음 패스와 LaVine의 코너 이동을 직접 보며 비공개 평점·미래 명단은 받지 않는다.",
        "goal": "자기 하이라이트 반복을 줄이고 다음 조합에서 짧은 연결과 수비 위치를 제때 잇는다.",
        "obstacle": "익숙한 자기 공격을 다시 연습하면 앞선 늦은 복귀가 영상에 남은 채 다음 과제에도 반복된다.",
        "unit_choice": cf4["choice"], "direct_present_cost": cf4["direct_cost"],
        "beats": [
            {"id": "F1", "action": "주인공이 자기 운반 뒤 수비 복귀가 늦었던 지점을 영상에 표시하고 가상 감독의 좁은 피드백을 받는다.", "response": "감독은 다음 허용 반복에서 패스 뒤 먼저 코너 위치를 확인하라는 과제를 준다.", "present_cost": "좋았던 자기 장면을 늘리거나 쉴 시간을 영상 대조와 재준비에 쓴다."},
            {"id": "F2", "action": "다음 허용 반복에서 주인공은 짧게 공을 넘긴 직후 열린 코너로 먼저 돌아간다.", "response": "LaVine은 같은 코너를 두 사람이 쫓지 않는 것을 보고 바깥 수신 길로 이동하고 LaMelo는 첫 연결을 늦추지 않는다.", "present_cost": "자기 공격을 한 번 더 할 기회를 쓰지 않는다. 이 한 번의 위치 수정은 시즌 효율이나 다음 진출을 보증하지 않는다."},
        ],
        "observable_exit": cf4["changed_state"], "cp2_exact_exit": s3["exit_state"],
        "cp2_exit_scope": "재준비를 직접 수행한 국소 증인. 봄이 짧아졌다는 실제 시리즈 이력, 파이널·재대결은 미선택.",
        "next_handoff": "A13-S1",
    }
    f55 = {
        "id": "A13-EF-001", "global_function_order_if_registered": 55,
        "planned_allocation_slot": 706, "subact": "A13-S1", "candidate_ids": [cf13["id"]],
        "exact_entry": f54["observable_exit"],
        "single_function": "훈련공 확보 뒤 운반 대신 전진 패스를 선택하고 공 없이 다시 빈 위치에 들어간다",
        "fictional_setting": "2027–28 날짜 미지정 Chicago 허용 비공개 연속 과제. LaMelo·LaVine의 이 훈련 참여는 선택된 가상 범위이며 해당 연차의 실제 계약·명단·경기 가용성을 증명하지 않는다.",
        "named_people_and_access": "주인공은 훈련 상대의 중앙 차단과 LaMelo의 열린 측면 길, LaVine의 후속 외곽 위치를 본다. 실제 상대팀·실존 코치 발언이나 마지막 패스 수신자는 정하지 않는다.",
        "goal": "리바운드 뒤 한 동작의 성공에 그치지 않고 공을 넘긴 뒤에도 다음 패스의 위치를 만든다.",
        "obstacle": "중앙 수비가 주인공의 직접 운반 길을 닫고, 공을 넘긴 후 멈추면 다음 연결에 관여할 수 없다.",
        "unit_choice": cf13["choice"], "direct_present_cost": cf13["direct_cost"],
        "beats": [
            {"id": "R1", "action": "주인공이 허용 과제의 수비 위치를 먼저 잡아 훈련공을 확보한다. 중앙 길이 닫힌 것을 보고 자기 운반을 멈춘다.", "response": "훈련 수비는 주인공의 첫 운반 방향을 계속 막지만 LaMelo의 측면 길은 열린다.", "present_cost": "자기 운반과 첫 슛 표본을 포기한다. 훈련공 확보는 정규 경기 개인 리바운드 통계가 아니다."},
            {"id": "R2", "action": "주인공이 LaMelo에게 전진 패스를 보낸 뒤 공 없는 바깥 길로 달려 다음 패스를 받을 위치에 선다.", "response": "LaMelo가 측면으로 전진하고 LaVine은 반대편 외곽으로 이동한다. 주인공은 새 위치에서 공을 다시 받을 수 있지만 이번 반복은 슛·득점 전에 멈춘다.", "present_cost": "볼 소유와 마지막 슛의 기회를 넘긴 채 재진입 노동을 맡는다. 성공한 결승 패스·압박 전반의 숙련은 인증하지 않는다."},
        ],
        "observable_exit": cf13["changed_state"], "cp2_exact_exit": t1["exit_state"],
        "cp2_exit_scope": "한 허용 과제에서 리바운드→전진 패스→무볼 위치를 연결한 증인. 상대가 알아도 막지 못한다는 전체 공격력은 미인증.",
        "next_handoff": cf13["next"],
    }
    functions = [f53, f54, f55]
    for index, function in enumerate(functions):
        previous = last if index == 0 else functions[index - 1]
        previous_id = previous["id"]
        previous_exit = previous["observable_exit"]
        assert function["exact_entry"] == previous_exit
        function.update({
            "episode_function_id": function["id"],
            "global_function_order": function["global_function_order_if_registered"],
            "primary_subact": function["subact"],
            "source_conditional_functions": function["candidate_ids"],
            "previous_function": {"id": previous_id, "path": list(SOURCES)[0] if index == 0 else OUT,
                                  "record_pointer": "/functions/2" if index == 0 else f"/functions/{index - 1}",
                                  "exact_full_exit": previous_exit},
            "entry_state": function["exact_entry"], "choice": function["unit_choice"],
            "exit_state": function["observable_exit"], "source_cp2_exit": function["cp2_exact_exit"],
            "classification": "SELECTED_FICTIONAL_LOCAL_FUNCTION_DESIGN_PENDING_INDEPENDENT_REVIEW",
            "independent_review_completed": False, "registered_final_function_increment": 0,
            "fictional_observation_designed": True, "historical_observation_certified": False,
            "actual_NBA_game_or_contract_certified": False, "whole_parent_act_complete": False,
            "whole_g13_complete": False, "whole_g14_complete": False,
            "actual_context_packs": 0, "manuscript_count": 0, "manuscript_allowed": False,
        })
    assert [v["planned_allocation_slot"] for v in functions] == [676, 701, 706]
    assert f53["intermediate_cf02_exit"] == cf3["entry_state"]
    assert f53["observable_exit"] == cf4["entry_state"]
    assert f54["observable_exit"] == cf13["entry_state"]
    return {
        "schema": "A12_S2_S3_A13_S1_DELEGATED_FUNCTION_EXECUTION_V1",
        "status": "FICTION_DESIGN_SELECTED_THREE_LOCAL_FUNCTIONS_PENDING_INDEPENDENT_REVIEW_AND_REGISTER",
        "selected_function_count": 3, "registered_function_increment": 0,
        "source_previous_exact_exit": last["observable_exit"], "functions": functions,
        "source_cp2_act_exits": {"A12": act12["exit_state"], "A13": act13["exit_state"]},
        "handoff_contract": "A12-EF-001 exact exit -> A12-EF-002 V1/V2 -> A12-EF-003 F1/F2 -> A13-EF-001 R1/R2; fictional local design, no future historical game certification.",
        "access_boundary": "허용 비공개 훈련·가상 감독 과제·직접 관측 영상만. 계약·명단·의료·시리즈 자격·실제 승패와 타인 내면은 인증하지 않는다.",
        "future_roster_contract_series_eligibility_certified": False,
        "season_domination_MVP_title_or_final_winning_pass_selected": False,
        "one_club_retirement_prepaid": False,
        "whole_A12_or_A13_act_exits_certified": False, "whole_g13_complete": False, "whole_g14_complete": False,
        "actual_context_packs": 0, "manuscript_count": 0, "manuscript_allowed": False,
        "design_gate": "CLOSED", "freeze": "v0.30 PARTIAL", "new_author_lock": False,
        "source_hash_method": "SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF",
        "source_sha256": {SELF: digest(root / SELF), **SOURCES},
    }


def markdown(data):
    lines = ["# A12-S2/S3 → A13-S1 선택된 세 국소 기능", "",
             "앞 A12-EF-001의 정확 출구에서 이어지는 가상 편집 설계다. 훈련에서 직접 보는 손실·수정·다음 행동을 정했으며 실제 미래 경기·계약·명단 적법성은 인증하지 않는다.", ""]
    for f in data["functions"]:
        lines += [f"## {f['id']} · {f['subact']}", "", f"- 계획 슬롯 {f['planned_allocation_slot']} (출판 회차 아님)",
                  f"- 정확 진입: {f['exact_entry']}", f"- 기능: {f['single_function']}",
                  f"- 허용: {f['fictional_setting']}", f"- 인물·접근: {f['named_people_and_access']}",
                  f"- 목표/방해: {f['goal']} / {f['obstacle']}", f"- 원 선택: {f['unit_choice']}",
                  f"- 원 직접 비용: {f['direct_present_cost']}", ""]
        for beat in f["beats"]:
            lines.append(f"- {beat['id']}: {beat['action']} {beat['response']} 비용: {beat['present_cost']}")
        lines += ["", f"정확 국소 출구: {f['observable_exit']}",
                  f"원 CP2 출구: {f['cp2_exact_exit']} — {f['cp2_exit_scope']}", ""]
    lines += ["세 기능은 FICTION_DESIGN_SELECTED이지만 등록 0이다. 실제 시즌 지배·시리즈·MVP·우승·결승 패스·장기결말 선지급 0, 전체 G13/G14 false, Pack/원고 0, v0.30 PARTIAL/CLOSED.", ""]
    return "\n".join(lines)


def validate(data, root=ROOT):
    try:
        return [] if data == build(root) else ["selected function packet differs from source-bound build"]
    except (AssertionError, KeyError, OSError, TypeError, ValueError, IndexError) as exc:
        return [f"source construction: {exc}"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        (ROOT / OUT.replace(".json", ".md")).write_text(markdown(data), encoding="utf-8", newline="\n")
    if args.check:
        saved = physical(ROOT, OUT)
        errors = validate(saved)
        assert not errors, errors
        assert text(ROOT / OUT.replace(".json", ".md")) == markdown(saved)
    print(json.dumps({"current": True, "functions": [v["id"] for v in data["functions"]],
                      "registered_increment": data["registered_function_increment"]}))


if __name__ == "__main__":
    main()
