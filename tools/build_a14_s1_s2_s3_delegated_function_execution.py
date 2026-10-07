"""Build three bounded A14 function designs without executing the late-career history."""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_a14_s1_s2_s3_delegated_function_execution.py"
OUT = "design/A14_S1_S2_S3_DELEGATED_FUNCTION_EXECUTION_2026_10_08.json"
PINS = {
    "control/G13_A13_FUNCTION_EXECUTION_REGISTER_2026_10_08.json": "cbde663eb75cf02deba1ff07f1b1ed1614f6d1c563073d2eb09d1927c626f36a",
    "design/A13_S2_S3_DELEGATED_FUNCTION_EXECUTION_2026_10_08.json": "0f79ee52cf8697b85e2a562dac7b4c04cd159b81a21fdca9a1dd0da33320b6fe",
    "design/A13_2027_28_CONDITIONAL_FUNCTIONS.json": "f0f2add25e5279f01f52366657704dbac0262ef93f43246a72b05c965848da72",
    "design/A14_2028_35_CONDITIONAL_FUNCTIONS.json": "9d6bb34cf5097381245610ed1ba7468b130877482f8d83de4f914a669627c454",
    "design/CP2_ACT_SUBACT_PACKET.json": "2b291bca588302cbb254fc3417652f7d7532c46d7094221cdcceac60619c9db9",
    "design/ENDING_THEME.md": "929807f42a2d1ed0f8229ecf5bb1f2e3f00642732cbaa590cbce630fae0c34f3",
    "control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md": "91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d",
    "design/A09_A14_SEVENTEEN_ROUTE_CLOSURE_MATRIX_2026_10_07.json": "bc409b3226417bb345b6ca51ee5e7428915d0eb196effb7e133363ac248b7609",
}


def text(path):
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def digest(path):
    return hashlib.sha256(text(path).encode()).hexdigest()


def physical(root, name):
    return json.loads(text(root / name))


def load(root, name):
    return json.loads((root / name).read_text(encoding="utf-8-sig"))


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def by_id(rows, ident):
    matches = [row for row in rows if row["id"] == ident]
    need(len(matches) == 1, "Missing or duplicated original id " + ident)
    return matches[0]


def sources(root):
    for name, expected in PINS.items():
        need(digest(root / name) == expected, "Physical source changed: " + name)
    names = list(PINS)[:5]
    loaded = {name: load(root, name) for name in names}
    for name, item in loaded.items():
        need(item == physical(root, name), "Returned source differs from physical: " + name)
    need("동료가 결승 득점한다" in text(root / "design/ENDING_THEME.md"), "Locked winning basket missing")
    matrix = physical(root, "design/A09_A14_SEVENTEEN_ROUTE_CLOSURE_MATRIX_2026_10_07.json")
    need("A14 one-club retirement lock separated from proposed successor action." in str(matrix), "One-club and successor scope changed")
    need("MVP급 성장 연도·우승 횟수/장기 결말 변화" in text(root / "control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md"), "Authority scope changed")
    return loaded


def build(root=ROOT):
    src = sources(root)
    for name, item in src.items():
        need(item == physical(root, name), "Consumed source differs from physical: " + name)
    reg, prev, a13, a14, cp2 = [src[name] for name in list(PINS)[:5]]
    need(reg["counts"]["registered_local_functions"] == 57, "Prior register count changed")
    need(reg["counts"]["subacts_with_verified_local_function_route"] == 39, "Prior route count changed")
    need(reg["counts"]["subacts_without_verified_local_function_route"] == 3, "Prior route gap changed")
    last = reg["functions"][-1]
    p57 = prev["functions"][-1]
    need(last["id"] == p57["id"] == "A13-EF-003" and last["order"] == 57, "Previous function changed")
    need(last["exact_exit"] == p57["observable_exit"] == "직접 해결과 이양의 책임을 함께 시험하지만 그 시도의 성공·개인 클러치 기록은 미정이다", "Previous exact exit changed")
    locked = by_id(a13["functions"], "A13-CF04")
    need(locked["author_locked_function"] is True and locked["selected_event"] is False, "Locked ending wrongly executed")
    need(locked["entry_state"] == last["exact_exit"], "Locked ending handoff changed")
    need(locked["claim_authority"]["teammate_winning_basket"] == "AUTHOR_LOCKED_FUNCTION", "Winning basket lock changed")
    need(locked["claim_authority"]["exact_year_opponent_receiver_score_time"] == "CANDIDATE_UNSELECTED", "Ending coordinate promoted")
    cfs = {item["id"]: item for item in a14["functions"]}
    need(set(cfs) == {"A14-CF01", "A14-CF02", "A14-CF03", "A14-CF04", "A14-CF05", "A14-CF06"}, "A14 source causal units changed")
    for i in range(1, 6):
        left, right = cfs[f"A14-CF{i:02d}"], cfs[f"A14-CF{i+1:02d}"]
        need(left["next"] == right["id"] and left["changed_state"] == right["entry_state"], "A14 causal handoff changed")
        need(left["selected_event"] is False and right["selected_event"] is False, "Original conditional event promoted")
    subacts = [by_id(cp2["subacts"], f"A14-S{i}") for i in range(1, 4)]
    need([x["choice"] for x in subacts] == [
        "미선택 다음 우승창 후보에서 공격 시작을 동료에게 넘길 구간을 시험하고 자신은 무볼의 마무리 위치와 준비 역할을 맡는다",
        "줄어드는 분을 배신으로 단정하지 않고 짧은 시간에 수행할 판단·준비 역할을 선택한다",
        "원클럽을 명예 목록으로 끝내지 않고 주도권을 넘긴 뒤 후배의 준비 행동이 남는 은퇴 기능을 검토한다",
    ], "Original A14 choices changed")
    need([x["cost"] for x in subacts] == [
        "일부 공격 시작권과 무볼 재관여의 준비 부담", "선발·계약 지위", "마지막 주도권"
    ], "Original A14 costs changed")
    need([x["exit_state"] for x in subacts] == [
        "유산이 개인 기록과 분리", "짧은 시간의 판단과 준비", "후배의 준비 행동이 남음"
    ], "Original A14 exits changed")
    need(cfs["A14-CF06"]["changed_state"] == "Chicago 원클럽 은퇴로 자신의 선수 역할을 마치고 후배의 준비 행동이 남는다", "Original retirement function changed")

    bridge = {
        "source_locked_function": "A13-CF04",
        "locked_winning_basket_and_team_win_function_preserved": True,
        "locked_final_possession_performed_in_this_packet": False,
        "source_A14_after_win_cause_is_conditional": True,
        "actual_first_or_second_title_awarded": False,
        "exact_year_opponent_receiver_score_and_last_game_selected": False,
        "meaning": "A13-EF-003 뒤 잠긴 결말과 A14 시작 사이에는 미실행 인과 인계가 있다. 아래 세 과제는 후일 Chicago 허용 연습의 선택된 가상 설계이고 우승 직후 실제 역사 장면이 아니다.",
    }

    f58 = {
        "id": "A14-EF-001", "global_function_order_if_registered": 58, "planned_allocation_slot": 766,
        "subact": "A14-S1", "candidate_ids": ["A14-CF01", "A14-CF02"],
        "exact_entry": last["exact_exit"],
        "single_function": "자기 공격 시작을 LaMelo에게 한 번 넘긴 뒤 공 없는 위치와 낮은 첫 연결의 일을 직접 다시 맞춘다",
        "fictional_setting": "2028–2035의 연도·경기 미지정 Chicago 허용 실내 과제. 팀 승리 뒤의 역사 장면이 아니며, LaMelo·LaVine은 기존 코어 방향 아래 이 가상 과제의 참가자일 뿐 그해 실제 명단·계약·건강을 인증하지 않는다.",
        "named_people_and_access": "주인공·LaMelo·LaVine, 그리고 윙 차단자와 태그 수비를 맡은 가상 연습 조. 주인공은 직접 전달된 과제와 공·발 위치만 본다. 감독의 비공개 평가나 동료의 속마음에는 접근하지 않는다.",
        "goal": "이전 성공 순서를 자기 시작권으로 영구 보유하려는 습관 대신, 동료 시작 뒤에도 자신이 맡을 준비와 첫 연결을 만든다.",
        "obstacle": "윙 차단자는 주인공의 익숙한 공받기 길을 먼저 막고 낮은 태그 수비는 긴 운반을 유도한다.",
        "unit_choice": subacts[0]["choice"], "direct_present_cost": subacts[0]["cost"],
        "beats": [
            {"id": "S1-A", "action": "주인공이 과제 첫 시작권을 LaMelo에게 넘기고 무볼 윙 자리로 이동한다.", "response": "연습 윙 차단자가 첫 공받기 길을 끊어 주인공이 그 반복에서는 바로 끝내지 못한다.", "present_cost": "자기 첫 운반과 즉시 공격 표본 한 번을 잃고 공 없는 위치를 다시 읽는 시간을 쓴다."},
            {"id": "S1-B", "action": "다음 허용 반복에서 주인공은 윙으로 무리하게 뛰지 않고 낮은 박스아웃 위치를 먼저 잡은 뒤 LaVine에게 짧은 첫 연결을 건넨다.", "response": "LaVine이 공을 받아 다음 과제를 시작하고 태그 수비는 뒤늦게 따라간다. 슛과 경기 결과는 기록하지 않는다.", "present_cost": "직접 리바운드를 쫓아 긴 운반을 보일 기회를 버리고 다른 조합의 위치·연결 반복에 시간을 쓴다."},
        ],
        "observable_exit": cfs["A14-CF02"]["changed_state"],
        "cp2_exact_exit": subacts[0]["exit_state"],
        "cp2_cost_scope": "연습의 시작권 한 번과 무볼 준비 시간만 실제 가상비용으로 보인다. 미래 NBA 공격권·계약의 감소는 정하지 않는다.",
        "cp2_exit_scope": "원 출구의 개인 기록과 분리된 역할을 국소 선택·비용으로 보이는 설계. 둘째 우승 또는 장기 역할 지속의 역사 인증은 아니다.",
        "next_handoff": "A14-CF03",
    }
    f59 = {
        "id": "A14-EF-002", "global_function_order_if_registered": 59, "planned_allocation_slot": 773,
        "subact": "A14-S2", "candidate_ids": ["A14-CF03", "A14-CF04", "A14-CF05"],
        "exact_entry": f58["observable_exit"],
        "single_function": "짧게 허용된 과제에서 포스트 공격을 한 번만 고르고, 다음 수비 호출·첫 연결을 준비해 실제 수행한다",
        "fictional_setting": "A14-S1 뒤 날짜 미지정 Chicago 실내 세 부분 과제. 짧은 과제창은 가상 감독이 연습에서 허용한 횟수이지 실제 벤치 전환, 선발 지위, 경기 출전분 또는 의료 제한이 아니다.",
        "named_people_and_access": "가상 감독이 과제창을 전달하고 가상 젊은 팀원이 첫 연결의 수신과 수비 교대 역할을 맡는다. 주인공은 받은 역할·자기 몸 반응·수비 발과 동료 위치를 볼 수 있지만 의료 판정·급여·실제 로테이션은 알 수 없다.",
        "goal": "짧은 표본에서 모든 것을 혼자 증명하려 하지 않고 유리한 공격 한 번과 이어지는 수비·연결을 구분한다.",
        "obstacle": "연습 수비가 첫 포스트 위치를 바깥으로 밀고, 다음 수비에서는 빠른 상대를 끝까지 쫓으려는 주인공의 습관을 이용해 뒤 공간을 비운다.",
        "unit_choice": subacts[1]["choice"], "direct_present_cost": subacts[1]["cost"],
        "beats": [
            {"id": "S2-A", "action": "주인공은 전부 직접 끝내려던 첫 포스트 반복에서 유리한 짧은 공격 한 번만 시도한다.", "response": "수비가 몸을 밀어 완성되지 않은 시도가 남고 그는 두 번째 긴 공격 대신 공을 가까운 팀원에게 연결한다.", "present_cost": "추가 개인 슛 표본을 포기하고 자기 역할의 한계를 영상에 남긴다. 경기 득점·능력 상실의 증명은 아니다."},
            {"id": "S2-B", "action": "다음 수비 반복에서는 추격 범위를 멈추고 자기 위치에서 교대를 호출하며 젊은 팀원이 맡은 길로 빠진다.", "response": "연습 상대의 첫 진입이 막히지만 후속 슛 전에 과제가 멈춘다.", "present_cost": "모든 상대를 직접 막는 개인 수비 표본을 내려놓고 동료 판단에 위험 일부를 맡긴다."},
            {"id": "S2-C", "action": "짧은 재진입 과제 전 대기 시간에 그는 수비 발 위치를 확인하고 들어가 첫 박스아웃과 안전한 연결을 수행한다.", "response": "젊은 팀원이 다음 공을 잡고 후속 선택을 시작한다. 실제 벤치 기용이나 계약 갱신의 승인으로 보지 않는다.", "present_cost": "자기 공격 리듬을 되찾으려는 첫 시간을 작은 위치·호출 준비에 쓴다."},
        ],
        "observable_exit": cfs["A14-CF05"]["changed_state"],
        "cp2_exact_exit": subacts[1]["exit_state"],
        "cp2_cost_scope": "개인 포스트·수비 표본과 짧은 과제의 준비 시간은 잃지만 원 CP2의 실제 선발·계약 지위 손실은 아직 관측되지 않는다.",
        "cp2_exit_scope": "짧은 연습 과제의 판단과 준비만 관측된다. 원 CP2의 실제 선발·계약 지위 감소나 의료 원인은 아직 선택되지 않았다.",
        "next_handoff": "A14-CF06",
    }
    f60 = {
        "id": "A14-EF-003", "global_function_order_if_registered": 60, "planned_allocation_slot": 780,
        "subact": "A14-S3", "candidate_ids": ["A14-CF06"],
        "exact_entry": f59["observable_exit"],
        "single_function": "주인공이 자기 준비 순서를 후배에게 보여 준 뒤 물러나고, 후배가 지시 없이 다음 준비를 직접 실행한다",
        "fictional_setting": "정확 은퇴 연도·마지막 계약·후속 직책을 정하지 않은 Chicago 허용 실내 인계 과제. 원클럽 은퇴는 잠긴 종착 기능이며 이 연습 자체가 실제 은퇴 발표나 마지막 NBA 경기라는 주장은 아니다.",
        "named_people_and_access": "주인공과 신원·계약이 아직 정해지지 않은 Chicago 가상 후배 참가자 한 명, 공을 받을 다른 가상 팀원 한 명. 후배를 LaMelo·LaVine이나 잠긴 결말의 패스 수신자로 확정하지 않는다. 관측은 후배의 움직임과 공의 경로에 한정한다.",
        "goal": "원클럽의 이름을 명예 목록으로 남기는 대신, 자신 없이도 이어질 한 가지 준비 행동을 눈앞에 남긴다.",
        "obstacle": "후배가 주인공의 지시를 기다리면 준비가 후배의 일이 되지 않고, 주인공이 다시 공을 잡으면 마지막 주도권을 실제로 넘기지 못한다.",
        "unit_choice": subacts[2]["choice"], "direct_present_cost": subacts[2]["cost"],
        "beats": [
            {"id": "S3-A", "action": "주인공이 박스아웃 표시와 첫 연결 순서를 한 번 보여 준 뒤 다음 반복에는 공과 과제표를 후배 앞에 놓고 과제 밖으로 물러난다.", "response": "후배는 처음에 주인공을 보지만 그가 다시 들어오지 않자 자기 발 위치를 스스로 고친다.", "present_cost": "주인공은 마지막 반복의 공과 통제권을 직접 내려놓는다."},
            {"id": "S3-B", "action": "후배가 새 반복에서 수비 위치를 먼저 잡고 공을 확보한 뒤 다른 팀원에게 짧은 첫 연결을 건넨다.", "response": "다른 팀원이 공을 받아 다음 준비를 시작한다. 주인공이 후배의 행동을 대신하지 않는다.", "present_cost": "준비의 결과를 자신의 기록이나 마지막 명예 장면으로 돌릴 수 없고 후배의 다음 선택은 후배에게 남는다."},
        ],
        "observable_exit": "주인공이 물러난 다음 반복에서 후배가 스스로 위치·첫 연결을 준비하는 표본이 남지만 Chicago 원클럽 은퇴의 정확 시점과 후속 경력은 미정이다",
        "cp2_exact_exit": subacts[2]["exit_state"],
        "cp2_cost_scope": "연습 반복의 공과 통제권을 후배에게 넘긴다. 실제 마지막 선수 계약과 은퇴의 주도권 이양은 미실행이다.",
        "cp2_exit_scope": "후배 자신의 준비 행동을 가상 과제에서 직접 보이는 설계. 원클럽 은퇴의 잠긴 기능은 보존하지만 실제 발표·마지막 경기·은퇴 연도는 실행하지 않는다.",
        "next_handoff": "CP2_INTEGRATED_REVIEW",
        "one_club_retirement_function_preserved": True,
        "retirement_event_or_date_executed": False,
        "successor_identity_or_future_career_selected": False,
    }
    functions = [f58, f59, f60]
    need(f58["observable_exit"] == cfs["A14-CF03"]["entry_state"], "A14 S1 to S2 source exit changed")
    need(f59["observable_exit"] == cfs["A14-CF06"]["entry_state"], "A14 S2 to S3 source exit changed")
    for index, function in enumerate(functions):
        prior = last if index == 0 else functions[index - 1]
        prior_exit = prior["exact_exit"] if index == 0 else prior["observable_exit"]
        need(function["exact_entry"] == prior_exit, "Local function exact handoff changed")
        function.update({
            "episode_function_id": function["id"],
            "global_function_order": function["global_function_order_if_registered"],
            "primary_subact": function["subact"],
            "source_conditional_functions": function["candidate_ids"],
            "previous_function": {
                "id": prior["id"],
                "path": list(PINS)[0] if index == 0 else OUT,
                "record_pointer": "/functions/56" if index == 0 else f"/functions/{index-1}",
                "exact_full_exit": prior_exit,
            },
            "entry_state": function["exact_entry"], "choice": function["unit_choice"],
            "exit_state": function["observable_exit"], "source_cp2_exit": function["cp2_exact_exit"],
            "classification": "SELECTED_FICTIONAL_LOCAL_FUNCTION_DESIGN_PENDING_INDEPENDENT_REVIEW",
            "independent_review_completed": False, "registered_final_function_increment": 0,
            "fictional_observation_designed": True, "historical_observation_certified": False,
            "actual_NBA_game_or_contract_certified": False, "whole_parent_act_complete": False,
            "whole_g13_complete": False, "whole_g14_complete": False,
            "actual_context_packs": 0, "manuscript_count": 0, "manuscript_allowed": False,
        })
    need([f["planned_allocation_slot"] for f in functions] == [766, 773, 780], "A14 planned slots changed")
    need(all(766 <= f["planned_allocation_slot"] <= 780 for f in functions), "A14 slot outside source act")
    need(f60["observable_exit"].find("후배가 스스로") >= 0, "Successor independent action missing")
    need(f60["retirement_event_or_date_executed"] is False, "Retirement promoted")
    return {
        "schema": "A14_S1_S2_S3_DELEGATED_FUNCTION_EXECUTION_V1",
        "status": "FICTION_DESIGN_SELECTED_THREE_LOCAL_FUNCTIONS_PENDING_INDEPENDENT_REVIEW_AND_REGISTER",
        "selected_function_count": 3, "registered_function_increment": 0,
        "source_previous_exact_exit": last["exact_exit"], "functions": functions,
        "source_cp2_A14_exits": {f"S{i}": subacts[i-1]["exit_state"] for i in range(1, 4)},
        "conditional_inter_act_bridge": bridge,
        "handoff_contract": "A13-EF-003 exact exit -> unexecuted locked A13-CF04 historical bridge -> A14-EF-001 -> EF-002 -> EF-003; no actual title or retirement coordinate certified.",
        "locked_one_club_retirement_function_preserved": True,
        "retirement_event_or_exact_2035_coordinate_selected": False,
        "successor_preparation_observed_only_in_selected_fictional_training": True,
        "future_roster_health_contract_or_additional_title_selected": False,
        "new_title_count_MVP_year_or_ending_coordinate_selected": False,
        "whole_A14_act_or_CP2_exit_historically_certified": False,
        "remaining_act_exit_dependencies": [
            "잠긴 A13-CF04 결승 기능의 실제 가상경기 좌표와 팀 승리 인계는 별도이며 이 국소 과제의 성립을 과거 우승 인증으로 바꾸지 않는다.",
            "A14의 미래 명단·허용 역할·건강·계약 및 실제 선발/분 감소는 독립 시즌·기관 설계가 필요하지만 3개 훈련기능의 새 사실증명 관문은 아니다.",
            "Chicago 원클럽 은퇴 기능은 고정이고 후배 준비행동은 이 패킷의 가상 표본으로 선택됐다. 정확 은퇴 시기·후배 신원/미래 경력·전체 Act 출구는 별도 통합감사 전까지 인증하지 않는다.",
            "세 기능의 root 독립검문과 현재 G13 등록 후 42소막 기능경로를 재계산하고, 원 CP2 Act 출구·G14 Context Pack은 별도 유한 검문으로 남긴다. 780 계획칸을 780 새사건으로 요구하지 않는다.",
        ],
        "whole_g13_complete": False, "whole_g14_complete": False,
        "actual_context_packs": 0, "manuscript_count": 0, "manuscript_allowed": False,
        "design_gate": "CLOSED", "freeze": "v0.30 PARTIAL", "new_author_lock": False,
        "source_hash_method": "SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF",
        "source_sha256": {SELF: digest(root / SELF), **PINS},
    }


def markdown(data):
    lines = ["# A14 세 소막의 선택된 국소 기능", "",
             "직전 A13-EF-003의 정확 출구에서 시작한다. 잠긴 A13-CF04 결승 기능은 아직 실행되지 않았으므로 A14의 승리 뒤 원인은 조건부 인계다. 아래는 날짜 없는 허용 연습의 가상 선택과 비용이며 우승·노화·실제 은퇴의 인증이 아니다.", ""]
    for f in data["functions"]:
        lines += [f"## {f['id']} · {f['subact']}", "", f"- 계획 슬롯 {f['planned_allocation_slot']} (새 출판 회차 확정 아님)",
                  f"- 정확 진입: {f['exact_entry']}", f"- 기능: {f['single_function']}",
                  f"- 허용 범위: {f['fictional_setting']}", f"- 인물·접근: {f['named_people_and_access']}",
                  f"- 목표/방해: {f['goal']} / {f['obstacle']}", f"- 원 선택: {f['unit_choice']}",
                  f"- 원 비용: {f['direct_present_cost']}", ""]
        for beat in f["beats"]:
            lines.append(f"- {beat['id']}: {beat['action']} {beat['response']} 비용: {beat['present_cost']}")
        lines += ["", f"정확 국소 출구: {f['observable_exit']}",
                  f"원 CP2 출구: {f['cp2_exact_exit']} — {f['cp2_exit_scope']}",
                  f"원 비용 경계: {f['cp2_cost_scope']}", ""]
    lines += ["A14 원클럽 은퇴 기능은 보존한다. 정확 은퇴 연도·마지막 계약·후배 신원/경력·우승 횟수·A13 결승 좌표는 여기서 선택하지 않는다.",
              "후배의 행동은 가상 훈련 표본이다. 전체 Act 역사 출구와 G13/G14는 미인증, 새 등록 0, Pack/원고 0, v0.30 PARTIAL, CLOSED.", ""]
    lines += ["## 남은 유한 출구 검문", ""] + ["- " + x for x in data["remaining_act_exit_dependencies"]] + [""]
    return "\n".join(lines)


def validate(data, root=ROOT):
    try:
        return [] if data == build(root) else ["Saved A14 functions differ from source-bound build"]
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
        need(validate(saved) == [], "Saved A14 JSON invalid")
        need(text(ROOT / OUT.replace(".json", ".md")) == markdown(saved), "Saved A14 MD invalid")
    print(json.dumps({"current": True, "functions": [f["id"] for f in value["functions"]],
                      "registered_increment": value["registered_function_increment"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
