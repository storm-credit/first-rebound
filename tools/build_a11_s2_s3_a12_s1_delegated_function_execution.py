"""Select three bounded fictional function designs after A11-EF-001."""

import argparse
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_a11_s2_s3_a12_s1_delegated_function_execution.py"
OUT = "design/A11_S2_S3_A12_S1_DELEGATED_FUNCTION_EXECUTION_2026_10_08.json"
AUTH = "control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md"
AUTH_SHA = "91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d"
SOURCES = {
    "control/G13_A01_LITERAL_WITNESS_EXECUTION_REGISTER_2026_10_08.json": "8cffdcab62a153964f519c96954307e4d6579c58c81991493facdf2d947b8d93",
    "design/A11_E1_FINAL_EPISODE_FUNCTION.json": "4666a5265eb7286a9570c4f4c826154eb79b50b2c59b15377cd3d29e420b3d69",
    "design/A11_2025_26_CONDITIONAL_FUNCTIONS.json": "b8cab9a9e80de5713824493805839fdd485212d25d6582f7df04c8f8604aa8b2",
    "design/A12_2026_27_CONDITIONAL_FUNCTIONS.json": "10b428b9742f356f4a447c2d44e75c1dfdbe891c92669ace30ad399a2a6be2e7",
    "design/CP2_ACT_SUBACT_PACKET.json": "2b291bca588302cbb254fc3417652f7d7532c46d7094221cdcceac60619c9db9",
    "design/CHICAGO_MINNESOTA_LONG_CAREER_PACKET.json": "bb4b3d848717d2ccc8bac3635ff0b916c6d1e2bcf8ebf2f913ff6f21283a2f66",
    "design/CP2_PROMISE_LEDGER.json": "91fbb1bddca519cab9dc1eb9c7cae35f9c759925fd1171c2e41db3c9c83f31c4",
}


def normalized_text(path):
    return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def digest(path):
    return sha256(normalized_text(path).encode("utf-8")).hexdigest()


def physical(root, name):
    return json.loads(normalized_text(root / name))


def load(root, name):
    return json.loads((root / name).read_text(encoding="utf-8-sig"))


def by_id(rows, ident):
    return next(row for row in rows if row["id"] == ident)


def assert_source(root):
    assert digest(root / AUTH) == AUTH_SHA, f"source changed: {AUTH}"
    authority = normalized_text(root / AUTH)
    assert "승인 코어 안의 루틴 계약 설계" in authority
    assert "정확 계약 가격은 건강·시즌 위임에서 도출하지 않는다" in authority
    for path, expected in SOURCES.items():
        assert digest(root / path) == expected, f"source changed: {path}"
    values = {path: load(root, path) for path in SOURCES}
    for path, value in values.items():
        assert value == physical(root, path), f"loader differs from physical {path}"
    return values


def build(root=ROOT):
    src = assert_source(root)
    reg, e1, a11, a12, cp2, career, promises = src.values()
    assert reg["counts"]["registered_local_functions"] == 49
    assert reg["counts"]["subacts_without_verified_local_function_route"] == 11
    assert reg["functions"][-1]["id"] == e1["episode_function_id"] == "A11-EF-001"
    assert reg["functions"][-1]["exact_exit"] == e1["exit_state"]
    assert e1["exit_state"] == "직접 시작을 줄인 구간에서도 관여를 시험하지만 분담의 성공과 상대 압박에 대한 지속성은 별개다"
    assert not reg["whole_g13_complete"] and not e1["whole_A11_complete"]
    cf02 = by_id(a11["functions"], "A11-CF02")
    cf03 = by_id(a11["functions"], "A11-CF03")
    cf04 = by_id(a11["functions"], "A11-CF04")
    cf12 = by_id(a12["functions"], "A12-CF01")
    s2, s3, t1 = [by_id(cp2["subacts"], name) for name in ("A11-S2", "A11-S3", "A12-S1")]
    act11, act12 = [by_id(cp2["acts"], name) for name in ("A11", "A12")]
    assert (act11["allocation_start"], act11["allocation_end"], act12["allocation_start"]) == (583, 647, 648)
    assert cf02["entry_state"] == e1["exit_state"] and cf02["next"] == cf03["id"]
    assert cf03["entry_state"] == cf02["changed_state"] and cf03["next"] == cf04["id"]
    assert cf04["entry_state"] == cf03["changed_state"] and cf04["next"] == "A12-S1"
    assert cf12["entry_state"] == cf04["changed_state"]
    for candidate in (cf02, cf03, cf04, cf12):
        assert not candidate["selected_event"] and candidate["status"] == "CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE"
    assert s2["choice"] == "라이벌 한 명의 봉쇄에만 도움수비를 몰지 않고 상대 팀의 다른 위협과 동료가 맡는 비용을 비교한다"
    assert s3["cost"] == "자기 슛 우선권과 불리한 수행을 공개하는 평가 부담"
    assert t1["exit_state"] == "유지할 사람과 기능을 구분"
    assert career["recommended_path"] == "H2" and not career["season_selected"]
    assert career["protagonist_one_club"] == "CHI"
    assert by_id(promises["promises"], "P3")["payoff"] == "A13-S3"

    f50 = {
        "id": "A11-EF-002", "global_function_order_if_registered": 50,
        "planned_allocation_slot": 606, "subact": "A11-S2",
        "candidate_ids": [cf02["id"]], "previous_function": "A11-EF-001",
        "exact_entry": e1["exit_state"],
        "single_function": "한 사람에게 몰린 도움수비가 다른 공간과 동료에게 남기는 비용을 직접 비교한다",
        "fictional_setting": "날짜 미지정 2025–26 Chicago 비공개 팀 연습. 감독의 한정 스카우트 과제는 MIN 라이벌 R1의 윙 드라이브와 Towns 롤을 각각 카드로 모사한다. R1·Towns의 2025–26 실제 동시 소속, 허가, 경기 출전은 선택하지 않는다.",
        "named_people_and_access": "주인공·LaMelo·LaVine은 허용 훈련의 Chicago 참가자다. LaMelo는 스카우트 팀에서 R1 드라이브를 모사하고, LaVine은 약한 쪽 코너 수비를 맡는다. Towns는 카드의 조건부 안쪽 위협이며 실제 현장 참가자가 아니다. 감독 지시는 가상 권한 선택이지 실존 발언이 아니다.",
        "goal": "라이벌 공을 따라가는 도움과 자기 구역 유지 중 동료가 치르는 공간 비용을 보인다.",
        "obstacle": "LaMelo의 안쪽 진입 카드에 반응해 주인공이 페인트 쪽으로 먼저 움직이면 자신이 맡은 약한 쪽 연결 길이 열린다.",
        "choice": cf02["choice"], "source_direct_cost": cf02["direct_cost"],
        "beats": [
            {"id": "D1", "action": "주인공이 드라이브 카드만 보고 페인트로 한 걸음 먼저 돕는다.", "response": "LaMelo가 열린 약한 쪽으로 공을 돌리자 LaVine은 자신의 코너 과제와 새 패스길을 동시에 커버할 수 없어 한 걸음 늦게 이동한다.", "present_cost": "주인공의 원래 패스길이 열리고 LaVine에게 복귀 노동이 넘어간다. 실제 슛·득점은 배정하지 않는다."},
            {"id": "D2", "action": "같은 카드의 재시험에서 주인공은 도움 거리를 줄이고 자기 패스길에 남은 채 안쪽 위협을 동료에게 알린다.", "response": "LaVine이 코너에 먼저 남을 수 있지만 LaMelo의 안쪽 길에는 주인공의 즉시 압박이 사라진다.", "present_cost": "라이벌 쪽 직접 봉쇄 표본을 포기하고 어느 쪽 위험을 동료에게 맡기는지 가시화한다."},
        ],
        "observable_exit": cf02["changed_state"],
        "cp2_exact_exit": s2["exit_state"],
        "cp2_exit_scope": "두 배치의 공간·노동 비용을 보는 한정 증인. 실제 두 팀의 시즌 비용 충돌, 라이벌 봉쇄나 시리즈 결과는 미인증.",
        "next_handoff": cf03["id"],
    }
    f51 = {
        "id": "A11-EF-003", "global_function_order_if_registered": 51,
        "planned_allocation_slot": 630, "subact": "A11-S3",
        "candidate_ids": [cf03["id"], cf04["id"]], "previous_function": f50["id"],
        "exact_entry": f50["observable_exit"],
        "single_function": "선제 회전 앞 이른 이양 뒤 자기 재진입 오류를 공개하고 같은 과제에서 한 번 수정한다",
        "fictional_setting": "앞선 수비 시험 다음으로 감독이 허용한 Chicago 비공개 공격 과제. 상대의 선제 회전은 훈련 수비가 수행하며 실제 MIN 시리즈 수비나 경기 포제션으로 인증하지 않는다.",
        "named_people_and_access": "주인공·LaMelo·LaVine이 같은 허용 과제에서 보이는 선택만 안다. 감독은 가상 훈련 과제를 부여한다. 팀 검토의 범위는 이 과제의 허용 영상과 직접 수행뿐이다.",
        "goal": "막힌 첫 길에서 공을 연결한 뒤 동료의 다음 길을 해치지 않고 재관여한다.",
        "obstacle": "첫 이양 뒤 본인이 LaMelo의 돌파 길로 너무 빨리 들어가 공간을 다시 닫는다.",
        "choice": cf03["choice"] + "; " + cf04["choice"],
        "source_direct_cost": cf03["direct_cost"] + "; " + cf04["direct_cost"],
        "beats": [
            {"id": "O1", "action": "주인공이 첫 길이 닫히자 LaMelo에게 일찍 공을 보내고 바로 같은 안쪽 통로로 재진입한다.", "response": "LaMelo가 그 통로로 한 걸음 들어오다 주인공과 길이 겹쳐 공을 멈추고 바깥으로 되돌린다. LaVine의 바깥 준비도 한 박자 기다린다.", "present_cost": "주인공의 마지막 슛 기회가 사라지고 두 동료의 다음 동작을 늦춘 불리한 표본이 남는다."},
            {"id": "O2", "action": "주인공이 그 영상을 감독과 LaMelo 앞에서 자기 판단 오류로 표시한다. 받은 수정 과제에서 같은 이양 뒤 안쪽으로 뛰지 않고 바깥 빈 위치에 선다.", "response": "LaMelo가 첫 안쪽 길을 다시 사용하고 LaVine이 바깥 수신 위치로 움직일 시간을 얻는다. 공은 주인공에게 돌아오지 않는다.", "present_cost": "자기 슛·평가 만회 반복 시간을 포기하고 불리한 영상을 보여 준 채 위치 수정에 쓴다. 득점과 지속 효율은 없다."},
        ],
        "observable_exit": cf04["changed_state"],
        "intermediate_exact_cf03_exit": cf03["changed_state"],
        "cp2_exact_exit": s3["exit_state"],
        "cp2_exit_scope": "이 과제의 오류가 다음 훈련·비용 논의의 원인으로 남는 국소 증인. 첫 Finals 패배나 시즌 구조 실패는 선택하지 않는다.",
        "next_handoff": cf12["id"],
    }
    f52 = {
        "id": "A12-EF-001", "global_function_order_if_registered": 52,
        "planned_allocation_slot": 648, "subact": "A12-S1",
        "candidate_ids": [cf12["id"]], "previous_function": f51["id"],
        "exact_entry": f51["observable_exit"],
        "single_function": "같은 동료를 전부 같은 값에 묶는 요구와 실제 필요한 연결·수비 기능을 분리해 자신의 요구 비용을 제시한다",
        "fictional_setting": "2026–27 계약창의 정확 날짜를 지정하지 않은 선택세계의 팀 역할 영상 검토와 공개 수치 기반 가상 에이전트 상담. 기존 주인공 2022–26 계약이 끝나는 시점 이후라는 조건만 둔다. 법정 계약·명단·예산의 실제 완료를 인증하지 않는다.",
        "named_people_and_access": "주인공은 앞선 과제에서 LaMelo가 멈춘 길과 LaVine이 기다린 바깥 위치를 본다. LaMelo·LaVine의 미래 잔류/계약 동의는 안다고 쓰지 않는다. 주인공의 가상 에이전트는 공개 급여와 역할 비용의 조건표만 전달하며 팀 계약 승인권이나 두 동료의 대리권이 없다. 실존 에이전트의 발언으로 쓰지 않는다.",
        "goal": "자기 계약 요구와 LaMelo의 첫 연결·LaVine의 바깥 득점 준비·벤치 수비 기능 사이의 교환 비용을 한 장에서 구분한다.",
        "obstacle": "모두 같은 조합으로 남길 수 있다고 쓰면 자신의 더 큰 공격 권한과 벤치 방어 노동의 예산 경쟁을 숨긴다.",
        "choice": cf12["choice"], "source_direct_cost": cf12["direct_cost"],
        "beats": [
            {"id": "C1", "action": "주인공이 LaMelo가 멈춘 영상과 LaVine이 기다린 위치를 따로 표시하고 자신의 시작권을 늘릴 때 누가 다음 첫 연결·코너 수비를 맡는지 적는다.", "response": "주인공의 가상 에이전트는 공개 수치 조건표에서 세 사람 이름 유지 칸과 필요한 첫 연결·수비 기능 칸이 같지 않다고 되돌려 준다.", "present_cost": "자기 평가 표본을 더 찍을 준비 시간을 비교 자료와 부족한 기능 목록 작성에 쓴다."},
            {"id": "C2", "action": "주인공은 자신의 요구를 전원 유지·즉시 첫 옵션 요구와 분리하고, 다음 팀 검토에 필요한 연결·수비 역할을 먼저 질문한다.", "response": "에이전트는 팀의 계약 수락이나 동료 잔류를 약속하지 않고 가능한 기능과 비어 있는 비용 칸만 남겨 준다.", "present_cost": "높은 역할과 같은 동료 전원 유지를 동시에 당연하게 요구할 수 없다는 부담을 자기 자료에 남긴다."},
        ],
        "observable_exit": cf12["changed_state"],
        "cp2_exact_exit": t1["exit_state"],
        "cp2_exit_scope": "이름과 기능을 분리한 질문·자료 제출까지 관측. 새 계약·프런트 채택·벤치 구성의 전체 출구는 미인증.",
        "next_handoff": cf12["next"],
    }
    functions = [f50, f51, f52]
    assert f50["observable_exit"] == cf03["entry_state"]
    assert f51["observable_exit"] == cf12["entry_state"]
    assert f52["observable_exit"] == cf12["changed_state"]
    for index, function in enumerate(functions):
        prior_id = e1["episode_function_id"] if index == 0 else functions[index - 1]["id"]
        prior_exit = e1["exit_state"] if index == 0 else functions[index - 1]["observable_exit"]
        function.update({
            "episode_function_id": function["id"],
            "global_function_order": function["global_function_order_if_registered"],
            "primary_subact": function["subact"],
            "source_conditional_functions": function["candidate_ids"],
            "previous_function": {
                "id": prior_id,
                "path": "design/A11_E1_FINAL_EPISODE_FUNCTION.json" if index == 0 else OUT,
                "record_pointer": None if index == 0 else f"/functions/{index - 1}",
                "exact_full_exit": prior_exit,
            },
            "entry_state": function["exact_entry"],
            "unit_choice": function["choice"],
            "direct_present_cost": function["source_direct_cost"],
            "exit_state": function["observable_exit"],
            "source_cp2_exit": function["cp2_exact_exit"],
            "classification": "SELECTED_FICTIONAL_LOCAL_FUNCTION_DESIGN_PENDING_INDEPENDENT_REVIEW",
            "independent_review_completed": False,
            "registered_final_function_increment": 0,
            "fictional_observation_designed": True,
            "historical_observation_certified": False,
            "actual_NBA_game_or_contract_certified": False,
            "whole_parent_act_complete": False,
            "whole_g13_complete": False,
            "whole_g14_complete": False,
            "actual_context_packs": 0,
            "manuscript_count": 0,
            "manuscript_allowed": False,
        })
        assert function["entry_state"] == prior_exit
    return {
        "schema": "A11_S2_S3_A12_S1_DELEGATED_FUNCTION_EXECUTION_V1",
        "status": "FICTION_DESIGN_SELECTED_THREE_LOCAL_FUNCTIONS_PENDING_INDEPENDENT_REVIEW_AND_REGISTER",
        "fiction_design_selected": True, "independent_review_completed": False,
        "selected_function_count": 3, "registered_function_increment": 0,
        "source_previous_exact_exit": e1["exit_state"],
        "source_cp2_act_exits": {"A11": act11["exit_state"], "A12": act12["exit_state"]},
        "functions": functions,
        "handoff_contract": "A11-EF-001 exact exit -> A11-EF-002 D1/D2 -> A11-EF-003 O1/O2 -> A12-EF-001 C1/C2. The latter three are selected fictional local designs, not certified future season events.",
        "source_access_boundary": "허용된 비공개 팀 훈련·주인공의 가상 에이전트 상담과 본인의 직접 수행/영상/공개 조건표만. 에이전트는 팀 계약 승인권이나 동료 대리권이 없다. 타인 내면·실존 코치 대사·비공개 계약/의료·미래 경기 결과는 알지 못한다.",
        "actual_2025_27_nba_game_minutes_box_or_results_certified": False,
        "future_named_roster_legality_and_contract_acceptance_certified": False,
        "first_MIN_Finals_loss_or_MVP_year_selected": False,
        "H2_RC1_AW2_exact_coordinates_selected": False,
        "whole_A11_or_A12_act_exits_certified": False,
        "whole_g13_complete": False, "whole_g14_complete": False,
        "actual_context_packs": 0, "manuscript_count": 0,
        "manuscript_allowed": False, "design_gate": "CLOSED", "freeze": "v0.30 PARTIAL",
        "new_author_lock": False,
        "source_hash_method": "SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF",
        "source_sha256": {SELF: digest(root / SELF), AUTH: AUTH_SHA, **SOURCES},
    }


def markdown(data):
    lines = ["# A11-S2/S3 → A12-S1 선택된 세 국소 기능", "",
             "기존 A11-EF-001의 정확 출구에서 잇는 가상 편집 설계다. 세 기능의 선택·행동·상대 반응·현재 손실은 확정했지만 미래 NBA 경기와 계약의 역사 인증, 등록부 증분은 아직 없다.", ""]
    for f in data["functions"]:
        lines += [f"## {f['id']} · {f['subact']}", "",
                  f"- 계획 슬롯 {f['planned_allocation_slot']} (출판 회차 아님), 진입: {f['exact_entry']}",
                  f"- 과제: {f['single_function']}", f"- 허용: {f['fictional_setting']}",
                  f"- 인물·정보: {f['named_people_and_access']}",
                  f"- 목표/방해: {f['goal']} / {f['obstacle']}",
                  f"- 선택: {f['choice']}", f"- 원 후보의 직접 비용: {f['source_direct_cost']}", ""]
        for b in f["beats"]:
            lines.append(f"- {b['id']}: {b['action']} {b['response']} 비용: {b['present_cost']}")
        lines += ["", f"정확 국소 출구: {f['observable_exit']}",
                  f"원 CP2 출구: {f['cp2_exact_exit']} — {f['cp2_exit_scope']}", ""]
    lines += ["세 기능은 FICTION_DESIGN_SELECTED이며 실제 2025–27 경기·분·점수·명단 적법성·계약 수락이 아니다. H2 첫 Finals 패배, RC1 수신자, MVP 연도·추가 우승은 미선택이다. 등록 0, 전체 G13/G14 false, Pack/원고 0, v0.30 PARTIAL/CLOSED.", ""]
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
        if normalized_text(ROOT / OUT.replace(".json", ".md")) != markdown(saved):
            errors.append("Markdown differs")
        print(json.dumps({"current": not errors, "errors": errors}, ensure_ascii=False))
        if errors:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
