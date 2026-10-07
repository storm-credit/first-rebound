"""Select bounded A13-S2/S3 functions while preserving the locked ending separately."""

import argparse
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_a13_s2_s3_delegated_function_execution.py"
OUT = "design/A13_S2_S3_DELEGATED_FUNCTION_EXECUTION_2026_10_08.json"
PINS = {
    "design/A12_S2_S3_A13_S1_DELEGATED_FUNCTION_EXECUTION_2026_10_08.json": "c835907cc5673dc427fec1e6adbdc27f994991177ed8449edfbb36999ff4a139",
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


def sources(root):
    for path, expected in PINS.items():
        assert digest(root / path) == expected, f"physical source changed: {path}"
    objects = {path: load(root, path) for path in list(PINS)[:3]}
    for path, value in objects.items():
        assert value == physical(root, path), f"returned source differs from physical: {path}"
    assert "동료가 결승 득점한다" in text(root / "design/ENDING_THEME.md")
    assert "MVP급 성장 연도·우승 횟수/장기 결말 변화" in text(root / "control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md")
    return objects


def by_id(rows, ident):
    return next(row for row in rows if row["id"] == ident)


def build(root=ROOT):
    src = sources(root)
    for path, value in src.items():
        assert value == physical(root, path), f"consumed source differs from physical: {path}"
    prev, a13, cp2 = [src[path] for path in list(PINS)[:3]]
    assert prev["selected_function_count"] == 3 and prev["registered_function_increment"] == 0
    last = prev["functions"][-1]
    assert last["id"] == "A13-EF-001" and last["global_function_order_if_registered"] == 55
    assert last["observable_exit"] == "운반·이양·다음 위치를 이어 시험하지만 어느 압박에서도 자동으로 통하는 통합 능력을 얻지는 않는다"
    assert last["actual_NBA_game_or_contract_certified"] is False
    cf2, cf3, locked = [by_id(a13["functions"], ident) for ident in ("A13-CF02", "A13-CF03", "A13-CF04")]
    s2, s3 = [by_id(cp2["subacts"], ident) for ident in ("A13-S2", "A13-S3")]
    assert cf2["entry_state"] == last["observable_exit"] and cf2["next"] == cf3["id"]
    assert cf3["entry_state"] == cf2["changed_state"] and cf3["next"] == locked["id"]
    assert locked["entry_state"] == cf3["changed_state"] and locked["author_locked_function"] is True
    assert locked["selected_event"] is False and locked["historical_coordinates_author_locked"] is False
    assert locked["claim_authority"]["teammate_winning_basket"] == "AUTHOR_LOCKED_FUNCTION"
    assert locked["claim_authority"]["exact_year_opponent_receiver_score_time"] == "CANDIDATE_UNSELECTED"
    assert s2["choice"] == "이전 해법을 복사하지 않고 다시 만난 상대와 동료의 달라진 역할에 맞는 대응을 비교한다"
    assert s3["exit_state"] == "수비→리바운드→전진→패스→동료 득점"
    assert cf2["selected_event"] is False and cf3["selected_event"] is False

    f56 = {
        "id": "A13-EF-002", "global_function_order_if_registered": 56,
        "planned_allocation_slot": 730, "subact": "A13-S2", "candidate_ids": [cf2["id"]],
        "exact_entry": last["observable_exit"],
        "single_function": "익숙한 전진 패스가 윙 상단 차단에 걸리자 다른 동료 위치를 보고 스크린 뒤 낮은 연결로 바꾼다",
        "fictional_setting": "2027–28 날짜 미지정 Chicago 허용 비공개 전술 과제. 연습 수비는 지난 과제의 중앙 차단과 달리 외곽 수신자를 먼저 막고 뒤 수비가 낮은 패스길을 늦게 좁힌다. 실제 라이벌 팀 재대결이나 대진은 선택하지 않는다.",
        "named_people_and_access": "LaMelo는 앞선 과제에서 공을 받은 윙 수신 역할을, LaVine은 새로 열린 낮은 반대편 연결 위치를 맡는 가상 훈련 참가자다. 두 수비는 가상 연습 조의 윙 차단자와 낮은 태그 수비자다. 주인공이 보는 것은 움직임과 공의 경로뿐이며 미래 명단·내면은 알지 못한다.",
        "goal": "전 과제의 LaMelo 전진 패스를 같은 높이로 반복하다 막힌 뒤 LaVine의 새 위치와 수비 태그를 대조해 한정 조정한다.",
        "obstacle": "윙 수비가 LaMelo의 첫 수신을 미리 가로막고 낮은 태그 수비는 주인공이 다시 중앙으로 운반하면 LaVine의 새 길까지 닫는다.",
        "unit_choice": cf2["choice"], "direct_present_cost": cf2["direct_cost"],
        "beats": [
            {"id": "A1", "action": "주인공은 앞서 통했던 LaMelo 쪽 전진 패스를 같은 높이로 시도한다.", "response": "연습 윙 수비가 먼저 길을 막아 공이 수신자에게 가지 못하고, LaMelo는 제자리에서 멈춘다.", "present_cost": "익숙한 순서를 급히 복사한 한 번의 허용 공격 표본을 잃는다. 실제 턴오버 통계는 아니다."},
            {"id": "A2", "action": "다음 허용 반복에서 주인공은 중앙 운반을 멈추고 LaMelo의 스크린 뒤 LaVine이 낮은 빈 위치로 옮기는 것을 확인해 짧은 연결을 건넨다.", "response": "낮은 태그 수비가 LaVine 쪽으로 뒤늦게 이동하고 LaMelo는 막혔던 윙에서 다음 수신 공간으로 빠져나온다. 슛 전에 과제가 멈춘다.", "present_cost": "자기 전진 운반·기록 기회를 포기하고 다른 경로를 맞추는 반복 시간을 쓴다."},
        ],
        "observable_exit": cf2["changed_state"], "cp2_exact_exit": s2["exit_state"],
        "cp2_exit_scope": "새 외곽 차단에 대응한 한 번의 연습 선택. 정확 상대·재대결·시리즈 승패와 동료 전체 대응은 미인증.",
        "next_handoff": cf3["id"],
    }
    f57 = {
        "id": "A13-EF-003", "global_function_order_if_registered": 57,
        "planned_allocation_slot": 754, "subact": "A13-S3", "candidate_ids": [cf3["id"]],
        "exact_entry": f56["observable_exit"],
        "single_function": "직접 공격이 열린 표본에서는 짧게 시도하고, 더 유리한 동료 길이 열린 표본에서는 이양 책임을 맡는다",
        "fictional_setting": "A13-S2 뒤 날짜 미지정 Chicago 비공개 두 조건 과제. 두 표본은 허용된 훈련 분기이며 Finals Game 7 마지막 포제션이나 실제 클러치 기록이 아니다.",
        "named_people_and_access": "가상 감독이 같은 출발 위치에서 수비 각도만 다르게 주고, LaVine이 반대편 윙 수신 위치를 맡는다. 주인공은 수비의 가까운 발과 동료의 열린 길을 직접 본다. 이 훈련의 LaVine은 잠긴 결말의 최종 패스 수신자 인증이 아니다.",
        "goal": "모든 공을 넘겨 책임을 피하거나 모든 공을 쏘는 습관 대신 관측된 두 조건에 각각 비용을 건다.",
        "obstacle": "첫 조건에는 자신의 짧은 길이 열렸지만 동료에게 무조건 넘기고 싶은 유혹이 있고, 다음 조건에는 LaVine의 더 넓은 길보다 자신의 슛을 남기고 싶은 유혹이 있다.",
        "unit_choice": cf3["choice"], "direct_present_cost": cf3["direct_cost"],
        "beats": [
            {"id": "B1", "action": "첫 수비 각도에서 주인공은 자신의 짧은 한 드리블 길이 열려 있음을 보고 직접 올라간다.", "response": "가상 수비가 뒤늦게 붙어 슛을 방해하고 공은 림을 벗어난다. LaVine에게 바로 넘겼을 다른 공격 기회는 이 반복에서 사라진다.", "present_cost": "자기 공과 시간을 실제로 쓰고 실패 영상이 남는다. 성공한 개인 클러치 슛이나 경기 득점으로 기록하지 않는다."},
            {"id": "B2", "action": "두 번째 수비 각도에서 수비가 주인공의 짧은 길을 먼저 닫자 그는 LaVine의 더 넓은 윙 길에 공을 넘기고 바깥 위치로 재진입한다.", "response": "LaVine이 공을 받지만 연습 수비가 회전하므로 과제는 슛 전에 멈춘다. 주인공은 수신 뒤 결과를 통제하지 못한다.", "present_cost": "자신의 마지막 슛 표본과 공 소유를 넘기고 패스 선택의 실패 가능성을 맡는다."},
        ],
        "observable_exit": cf3["changed_state"], "cp2_exact_exit": s3["exit_state"],
        "cp2_exit_scope": "직접 시도와 이양의 조건·손실을 보인 국소 증인. 원 CP2의 결승 득점·승리까지 충족한 것으로 보지 않는다.",
        "next_handoff": locked["id"],
        "locked_ending_function_retained_unexecuted": True,
        "locked_ending_coordinates_selected": False,
    }
    functions = [f56, f57]
    for index, function in enumerate(functions):
        prior = last if index == 0 else functions[index - 1]
        exact = prior["observable_exit"]
        assert function["exact_entry"] == exact
        function.update({
            "episode_function_id": function["id"],
            "global_function_order": function["global_function_order_if_registered"],
            "primary_subact": function["subact"],
            "source_conditional_functions": function["candidate_ids"],
            "previous_function": {"id": prior["id"], "path": list(PINS)[0] if index == 0 else OUT,
                                  "record_pointer": "/functions/2" if index == 0 else "/functions/0",
                                  "exact_full_exit": exact},
            "entry_state": function["exact_entry"], "choice": function["unit_choice"],
            "exit_state": function["observable_exit"], "source_cp2_exit": function["cp2_exact_exit"],
            "classification": "SELECTED_FICTIONAL_LOCAL_FUNCTION_DESIGN_PENDING_INDEPENDENT_REVIEW",
            "independent_review_completed": False, "registered_final_function_increment": 0,
            "fictional_observation_designed": True, "historical_observation_certified": False,
            "actual_NBA_game_or_contract_certified": False, "whole_parent_act_complete": False,
            "whole_g13_complete": False, "whole_g14_complete": False,
            "actual_context_packs": 0, "manuscript_count": 0, "manuscript_allowed": False,
        })
    assert f56["observable_exit"] == cf3["entry_state"]
    assert f57["observable_exit"] == locked["entry_state"]
    return {
        "schema": "A13_S2_S3_DELEGATED_FUNCTION_EXECUTION_V1",
        "status": "FICTION_DESIGN_SELECTED_TWO_LOCAL_FUNCTIONS_PENDING_INDEPENDENT_REVIEW_AND_REGISTER",
        "selected_function_count": 2, "registered_function_increment": 0,
        "source_previous_exact_exit": last["observable_exit"], "functions": functions,
        "source_cp2_A13_S2_S3_exits": {"S2": s2["exit_state"], "S3": s3["exit_state"]},
        "handoff_contract": "A13-EF-001 exact exit -> A13-EF-002 A1/A2 -> A13-EF-003 B1/B2 -> locked A13-CF04 conditional final possession, unexecuted.",
        "locked_ending": {"function_source_id": locked["id"], "function_locked": True,
                          "teammate_winning_basket_and_team_win_function_preserved": True,
                          "finals_game7_possession_performed": False,
                          "exact_year_opponent_receiver_score_time_selected": False},
        "access_boundary": "가상 허용 훈련에서 직접 본 수비 각도·동료 위치·공의 경로만. 실제 미래 명단·계약·건강·시리즈 참가·마지막 포제션은 미인증.",
        "new_title_count_MVP_year_or_ending_coordinate_selected": False,
        "whole_A13_act_or_CP2_S3_exit_certified": False,
        "whole_g13_complete": False, "whole_g14_complete": False,
        "actual_context_packs": 0, "manuscript_count": 0, "manuscript_allowed": False,
        "design_gate": "CLOSED", "freeze": "v0.30 PARTIAL", "new_author_lock": False,
        "source_hash_method": "SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF",
        "source_sha256": {SELF: digest(root / SELF), **PINS},
    }


def markdown(data):
    lines = ["# A13-S2/S3 선택된 두 국소 기능", "",
             "앞 A13-EF-001의 정확 출구에서 잇는다. 이번에는 윙 상단 차단과 낮은 태그, 두 수비 각도를 직접 보이는 허용 연습으로 좁힌다. 잠긴 결말의 경기·수신자·승리 좌표는 실행하지 않는다.", ""]
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
    lines += ["A13-CF04의 Finals Game 7 수비→리바운드→전진→동료 결승 패스·득점·팀 승리 기능은 원잠금 그대로이며 여기서 실행하지 않는다. 수신자·연도·상대·점수·시간, 새 MVP/우승횟수 미선택. 등록 0, 전체 G13/G14 false, Pack/원고 0.", ""]
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
    value = build()
    if args.write:
        (ROOT / OUT).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        (ROOT / OUT.replace(".json", ".md")).write_text(markdown(value), encoding="utf-8", newline="\n")
    if args.check:
        saved = physical(ROOT, OUT)
        assert validate(saved) == []
        assert text(ROOT / OUT.replace(".json", ".md")) == markdown(saved)
    print(json.dumps({"current": True, "functions": [f["id"] for f in value["functions"]],
                      "registered_increment": value["registered_function_increment"]}))


if __name__ == "__main__":
    main()
