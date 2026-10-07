"""Select a bounded fictional A09 institutional route and two local functions.

Historical schedule and CBA pages are evidence of constraints, not evidence that
any real club, insurer, coach or athlete took the fictional actions below.
"""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_a09_joint_attempt_selected_execution.py"
OUTPUT = Path("design/A09_JOINT_ATTEMPT_SELECTED_EXECUTION_2026_10_08.json")
E1 = "design/A09_E1_FINAL_EPISODE_FUNCTION.json"
CONDITIONAL = "design/A09_S2_S3_CONDITIONAL_FINAL_FUNCTIONS_2026_10_07.json"
BRIDGE = "design/A09_2023_JOINT_ATTEMPT_INSTITUTIONAL_BRIDGE_2026_10_07.json"
CF = "design/A09_2023_24_CONDITIONAL_FUNCTIONS.json"
CP2 = "design/CP2_ACT_SUBACT_PACKET.json"
GATE = "control/NATIONAL_TEAM_MILITARY_SCOPE_GATE.md"
CAREER = "canon/CAREER_TIMELINE.md"
REPO_PINS = {
    E1: "0a0e4cf2c3f41fd16131f8cf43310ab44ae4ec1b26d7361f128889f14b4eaf58",
    CONDITIONAL: "d7279b3ecdb71421904c399080ec4d7bad11f7c933e5cd7710221ab86421697d",
    BRIDGE: "2b0431597543e31dc2d11cb191491e3dbb59c0c201c47dbfed6466252125de94",
    CF: "63a5ecf564c222541cf2a4179aaf203b42f7948971fc31b54813974873110a38",
    CP2: "2b291bca588302cbb254fc3417652f7d7532c46d7094221cdcceac60619c9db9",
    GATE: "340688b0459a22338688d2ad63d78b2ad64e6e8a877b3a73dea70c7fa233a3ef",
    CAREER: "0373c6c2d9ce41aa4c162dba1aa47b315f4d0893049e758c5af6fceac6a87696",
}
RAW_DIR = Path("C:/Users/Storm Credit/AppData/Local/Temp/fr-ag2023-20261007")
RAW_PINS = {
    "oca_kor.html": "3ff38fdce56fd7d911dc926637926b960503de89216b97f461a038e6e8fa18af",
    "oca_men_tournament_summary.pdf": "9417ce5df8f07d421b1827ff22a8bd25f320a01a819f524c491db4a8abaa22de",
    "nba_cba_2023.pdf": "bf178ca0f2d64f9dfe6fde095d3ae43d576b12e19ce7a679618d632584f7ab32",
}
ORIGINAL_ROSTER = [
    "HA Yungi", "LEE Junghyun", "HEO Hoon", "BYEON Junhyeong", "KIM Sunhyung",
    "LEE Woosuk", "YANG Hongseok", "MOON Jeonghyeon", "KIM Jongkyu",
    "RA Guna", "JEON Seonghyen", "LEE Seounghyun",
]
OUT = ["BYEON Junhyeong", "YANG Hongseok"]
IN = ["MIN rival (unnamed fictional character)", "Chicago protagonist (unnamed fictional character)"]


def normalized_sha(path):
    text = path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load(root, name):
    return json.loads((root / name).read_text(encoding="utf-8-sig"))


def direct_physical(root, name):
    return json.loads((root / name).read_bytes().decode("utf-8-sig"))


def source_guard(root):
    for name, expected in REPO_PINS.items():
        assert normalized_sha(root / name) == expected, f"repo source changed: {name}"
    for name, expected in RAW_PINS.items():
        assert hashlib.sha256((RAW_DIR / name).read_bytes()).hexdigest() == expected, f"raw source changed: {name}"
    # The cached OCA team page has an actual roster body; the schedule HTML is a shell.
    from bs4 import BeautifulSoup
    html = BeautifulSoup((RAW_DIR / "oca_kor.html").read_bytes(), "html.parser")
    text = html.get_text(" ", strip=True)
    roster_text = text.split("Team Overview Basketball Uniform Number Name Height Date of Birth", 1)[1].split("Team Officials", 1)[0]
    assert all(name in roster_text for name in ORIGINAL_ROSTER)
    assert len(ORIGINAL_ROSTER) == 12 and len(set(ORIGINAL_ROSTER)) == 12
    assert "Coach CHOO IS CHOO Il Seung" in text and "HEO Hoon" in roster_text
    import fitz
    summary = fitz.open(RAW_DIR / "oca_men_tournament_summary.pdf")
    assert len(summary) == 2
    p0, p1 = (page.get_text() for page in summary)
    assert "6 OCT 2023" in p0 and "Finals Rank 7/8" in p0
    assert "KOR" in p1 and "Game 37, 6 OCT" in p1
    cba = fitz.open(RAW_DIR / "nba_cba_2023.pdf")
    public_rule, article, upc = cba[432].get_text(), cba[435].get_text(), cba[584].get_text()
    assert hashlib.sha256(public_rule.encode("utf-8")).hexdigest() == "2de972a78a2e5f497b631d75b3b9787a9035e028dbb5510d3d452c21eee565f4"
    assert hashlib.sha256(article.encode("utf-8")).hexdigest() == "5706e20bb49fa51155c53696c5e988d45179922c08a99867dc2b5bab7e0b5277"
    assert "approved in writing" in public_rule and "September 15" in public_rule
    assert "express written consent" in public_rule and "disability insurance" in public_rule
    assert "international FIBA competition" in article and "Basketball Event" in article
    assert "training camp" in upc and "practices, meetings, workouts" in upc
    # The FIBA exception does not name the Asian Games or remove the public-event rule here.
    assert "Asian Games" not in article


def build(root=ROOT):
    source_guard(root)
    e1, prior, bridge, cf, cp2 = (load(root, name) for name in (E1, CONDITIONAL, BRIDGE, CF, CP2))
    for name, loaded in zip((E1, CONDITIONAL, BRIDGE, CF, CP2), (e1, prior, bridge, cf, cp2)):
        assert loaded == direct_physical(root, name), f"loader differs from physical {name}"
    assert e1["episode_function_id"] == "A09-EF-001" and e1["global_function_order"] == 43
    assert e1["exit_state"] == "공동 도전을 위해 자신이 할 준비를 시작하지만 명단·허가·보험·실제 이동은 아직 성립하지 않는다"
    assert not e1["national_team_roster_permission_insurance_travel_or_medal_certified"]
    assert prior["selected_institutional_bridge"] is False and bridge["selected_institutional_bridge"] is False
    assert [f["proposed_episode_function_id"] for f in prior["functions"]] == ["A09-EF-002", "A09-EF-003"]
    candidates = {f["id"]: f for f in cf["functions"]}
    subacts = {s["id"]: s for s in cp2["subacts"]}
    assert [candidates[k]["subact"] for k in ("A09-CF02", "A09-CF03", "A09-CF04", "A09-CF05")] == ["A09-S2", "A09-S2", "A09-S3", "A09-S3"]
    assert candidates["A09-CF02"]["entry_state"] == e1["exit_state"]
    assert candidates["A09-CF03"]["entry_state"] == candidates["A09-CF02"]["changed_state"]
    assert candidates["A09-CF04"]["entry_state"] == candidates["A09-CF03"]["changed_state"]
    assert candidates["A09-CF05"]["entry_state"] == candidates["A09-CF04"]["changed_state"]
    assert subacts["A09-S2"]["exit_state"] == "협력의 범위와 실패 후 관계"
    assert subacts["A09-S3"]["exit_state"] == "다음 시즌 별도 증명 필요"
    assert [x["step"] for x in bridge["b1_conditional_sequence"]] == [f"B1-{i}" for i in range(1, 6)]
    assert [x["step"] for x in bridge["b2_conditional_sequence"]] == [f"B2-{i}" for i in range(1, 4)]
    gate = (root / GATE).read_text(encoding="utf-8-sig")
    assert "2023_path: joint_attempt_selected" in gate and "2023_gold: R09_CAUSALITY_HOLD" in gate
    career = (root / CAREER).read_text(encoding="utf-8-sig")
    assert "2023 국가대표 공동 도전" in career and "Minnesota" in career

    roster = [name for name in ORIGINAL_ROSTER if name not in OUT] + IN
    assert len(roster) == len(set(roster)) == 12 and all(name in ORIGINAL_ROSTER for name in OUT)
    institution = {
        "classification": "AUTHOR_DELEGATED_FICTIONAL_INSTITUTIONAL_DESIGN_SELECTION",
        "actual_real_2023_roster_or_private_contract_certified": False,
        "historical_twelve": ORIGINAL_ROSTER,
        "replaced_historical_members": OUT,
        "added_fictional_members": IN,
        "selected_fictional_twelve": roster,
        "selection_cost": "두 원역사 선수의 명단 자리와 출전 기회가 대체세계에서 사라진다. 이들의 감정·발언·이후 경력은 설정하지 않는다.",
        "authorities": [
            {"id": "B1-1", "holder": "fictional Korean national-team selection authority", "action": "위 열두 명을 대체세계 최종 12인으로 결정", "limit": "원역사 명단이나 실제 대표팀 선발 문서가 아님"},
            {"id": "B1-2", "holder": "fictional Chicago club authorized personnel", "action": "주인공의 9/26–10/6 비공개 대표팀 공동훈련과 10/9 이동완료까지 구단 준비 결장을 한정 허용", "limit": "10/2 Media Day·10/3 Nashville·10/8 첫 시범경기 준비 손실; 공개 대회 경기 출전·향후 선발·완전 건강 허가 아님"},
            {"id": "B1-3", "holder": "fictional Minnesota club authorized personnel", "action": "라이벌의 같은 비공개 공동훈련 창과 10/9 복귀까지 별도 허용", "limit": "9/29 첫 연습, 9/30–10/1 지역 연습, 10/1–8 Abu Dhabi 팀 일정과 충돌; 공개 경기 출전이나 원역사 해외원정 명단·복귀 역할 허가 아님"},
            {"id": "B1-4", "holder": "fictional team and national-team risk administrators", "action": "양측 구단이 비공개 훈련·이동에 한정한 선수별 가상 보장 한도를 받아들이고 참가 전 건강 조건을 담당자가 확인", "limit": "가상 보장: 각 선수 기존 UPC의 2023–24 잔여 보장급여 위험액을 한도로 하고 치료·귀환 비용 별도 선수당 최대 USD 1,000,000; 공개 경기 보험의 NBA 수용이나 실제 보험 시장 견적·급여액·의료승인 인증이 아님"},
            {"id": "B1-5", "holder": "fictional national-team operations and coach CHOO Il Seung", "action": "이동·허용된 비공개 공동훈련 접근과 역할을 전달", "limit": "감독의 가상 과제 지시는 원역사 발언·공개 대회 경기 분·승패가 아님"},
            {"id": "B2-1", "holder": "fictional national-team operations", "action": "선택세계 비공개 공동훈련 창이 10/6까지 끝난 뒤 양 선수의 별도 귀환을 배치, 10/9까지 각 구단 소재지 접근", "limit": "10/6은 공개 일정의 마지막 가능 창을 참고한 비용 상한일 뿐 두 선수가 그날 경기했다는 뜻이 아님; 상대·라운드·결과·메달·항공편 미선택"},
            {"id": "B2-2", "holder": "fictional Chicago coach and training staff", "action": "주인공에게 놓친 연결/몸부하 과제와 10/10 이후 제한 팀 반복을 전달", "limit": "10/8 시범경기 참가·NBA 기술완성·시즌 분 보상 없음"},
            {"id": "B2-3", "holder": "fictional Minnesota authorized personnel", "action": "라이벌에게 별도 복귀 점검과 10/10 이후 허용 창을 전달", "limit": "원역사 Abu Dhabi 이동 또는 다음 경기 역할 자동 확정 아님"},
        ],
        "risk_limit_function": "per_player_max = guaranteed_2023_24_base_compensation_at_risk_under_existing_UPC + min(documented_treatment_and_return_cost, USD_1_000_000); existing UPC amounts and real premium not certified",
        "time_order": ["fictional_roster_and_two_club_private_training_permissions_before_2023_09_26", "risk_and_private_access_before_joint_training", "private_training_window_ends_no_later_than_2023_10_06", "separate_club_return_by_2023_10_09", "separate_allowed_training_from_2023_10_10"],
        "no_auto_FIBA_release": True,
        "no_actual_private_letter_or_policy_required": True,
        "public_tournament_game_performance_selected": False,
        "asian_games_FIBA_exception_classification_selected": False,
        "NBA_written_approval_or_public_game_insurance_accepted_selected": False,
        "public_game_legal_boundary": "2023 CBA Article XXIII §3(a)(i) 일반 공개 off-season Basketball Event에는 NBA 서면 승인, 9월 15일 이내 시점, 구단 명시 서면 동의 및 NBA가 수용할 보험이 요구된다. §3(c)의 국제 FIBA 대회 예외는 Asian Games 분류를 여기서 인증하지 않는다. 구단의 가상 비공개 훈련 허용만으로 9/26–10/6 공개 경기 출전을 적법화하지 않는다.",
    }
    e2exit = candidates["A09-CF03"]["changed_state"]
    e3exit = candidates["A09-CF05"]["changed_state"]
    functions = [
        {
            "episode_function_id": "A09-EF-002", "global_function_order": 44, "planned_allocation_slot": 444,
            "status": "SELECTED_FICTIONAL_LOCAL_FUNCTION_PENDING_INDEPENDENT_REVIEW",
            "primary_subact": "A09-S2", "previous_function": {"id": "A09-EF-001", "exact_full_exit": e1["exit_state"]},
            "entry_state": e1["exit_state"], "institutional_bridge": "B1-1 selected roster plus B1-2..B1-5 private access subset; public tournament performance unresolved",
            "single_function": prior["functions"][0]["single_function"],
            "unit_choice": candidates["A09-CF02"]["choice"],
            "direct_present_cost": candidates["A09-CF02"]["direct_cost"] + " 이어 " + candidates["A09-CF03"]["direct_cost"],
            "beats": [
                {"id": "S2-1", "action": "추일승 감독의 가상 한정 과제 전달 후 라이벌이 첫 이점을 만들고 주인공은 직접 짧은 공격 대신 허훈에게 공을 연결한다. 허훈은 연결을 받아 다음 쪽으로 옮긴다.", "observable": "라이벌의 첫 이점·허훈의 실제 공 인수·주인공의 득점 기회 포기", "knowledge": "주인공 자신의 코트 시야와 들은 과제"},
                {"id": "S2-2", "action": "같은 허용 훈련에서 주인공이 이양 뒤 스크린을 지나 다음 위치에 늦게 서고 허훈의 반환 길이 닫힌 것을 본다.", "observable": "자기 위치 지연과 닫힌 반환 통로", "knowledge": "동료 내면·경기 승패 추정 없음"},
                {"id": "S2-3", "action": "주인공이 허용 영상의 자기 발 위치와 받은 과제를 대조해 감독에게 다음 위치를 묻는다. 다시 라이벌의 첫 이점 뒤 허훈에게 연결하고 이번에는 스크린 뒤 다음 위치를 먼저 잡는다.", "observable": "질문·직접 재시도·한 번의 열린 반환 위치", "knowledge": "완전 화해나 반복 성공 판정 아님"},
            ],
            "exit_state": e2exit, "source_cp2_exit_target": subacts["A09-S2"]["exit_state"],
            "bounded_subact_exit_observed": True, "full_relationship_resolution_certified": False,
        },
        {
            "episode_function_id": "A09-EF-003", "global_function_order": 45, "planned_allocation_slot": 445,
            "status": "SELECTED_FICTIONAL_LOCAL_FUNCTION_PENDING_INDEPENDENT_REVIEW",
            "primary_subact": "A09-S3", "previous_function": {"id": "A09-EF-002", "exact_full_exit": e2exit},
            "entry_state": e2exit, "institutional_bridge": "B2-1..B2-3 selected fictional return after private training window, without public tournament endpoint claim",
            "single_function": prior["functions"][1]["single_function"],
            "unit_choice": candidates["A09-CF04"]["choice"] + " 이어 " + candidates["A09-CF05"]["choice"],
            "direct_present_cost": candidates["A09-CF04"]["direct_cost"] + " 이어 " + candidates["A09-CF05"]["direct_cost"],
            "beats": [
                {"id": "S3-1", "action": "대표팀 비공개 공동훈련 창 뒤 Chicago로 돌아온 주인공이 담당자로부터 놓친 팀 연결 과제와 허용 부하를 듣고, 자기 새 공격을 더 시험할 시간을 첫 팀 반복에 쓴다.", "observable": "전달받은 과제·개인 연습 시간 축소·허용된 팀 반복 참여", "knowledge": "Chicago 내부 평가나 Minnesota 복귀 결론은 알지 못함"},
                {"id": "S3-2", "action": "그 허용 반복에서 Chicago의 공 운반 담당 동료가 첫 연결을 맡고 주인공은 받은 공으로 미드포스트 짧은 발 위치를 시험한다. 수비 위치가 닫히자 억지 슛 대신 그 동료 쪽으로 공을 반환한다.", "observable": "발 위치 시험·닫힌 길·직접 공 반환", "knowledge": "슛 성공·실전 효율·동료 마음 추정 없음; 2023 특정 동료 소속을 새로 정하지 않음"},
                {"id": "S3-3", "action": "주인공이 제한 시험에서 공을 돌려준 사실과 다음 반복 과제를 구별해 기록한다.", "observable": "하나의 재시험 한계와 남은 하프코트 과제", "knowledge": "다음 시즌 역할이나 완성 기술 인증 없음"},
            ],
            "exit_state": e3exit, "source_cp2_exit_target": subacts["A09-S3"]["exit_state"],
            "bounded_subact_exit_observed": True, "nba_game_or_mastery_certified": False,
        },
    ]
    assert functions[0]["previous_function"]["exact_full_exit"] == e1["exit_state"]
    assert functions[1]["previous_function"]["exact_full_exit"] == functions[0]["exit_state"]
    assert functions[1]["entry_state"] == functions[0]["exit_state"]
    assert [f["exit_state"] for f in functions] == [f["exit_state"] for f in prior["functions"]]
    return {
        "schema": "A09_JOINT_ATTEMPT_SELECTED_EXECUTION_V1",
        "status": "AUTHOR_DELEGATED_FICTIONAL_INSTITUTION_AND_TWO_LOCAL_FUNCTIONS_SELECTED_PENDING_INDEPENDENT_REVIEW",
        "independent_review_completed": False,
        "existing_joint_attempt_author_locked": True,
        "new_author_lock": False,
        "selected_institutional_bridge": True,
        "fictional_private_joint_training_and_return_selected": True,
        "public_tournament_game_performance_selected": False,
        "public_tournament_legal_classification_selected": False,
        "institutional_execution": institution,
        "functions": functions,
        "local_function_count_proposed": 2,
        "registered_final_function_increment": 0,
        "registration_target_after_independent_review": 45,
        "historical_game_or_medal_military_result_selected": False,
        "actual_real_club_permission_insurance_or_medical_certified": False,
        "whole_A09_complete": False, "whole_g13_complete": False, "whole_g14_complete": False,
        "actual_context_packs": 0, "manuscript_allowed": False, "design_gate": "CLOSED",
        "ancestor_chain_currentness_revalidated": False,
        "ancestor_currentness_note": "A09-E1 through A05 historical source chain has a CAREER_TIMELINE text hash drift; physical E1/CF meanings are pinned here, root owns historical refresh before register.",
        "historical_primary_urls": bridge["primary_sources"],
        "physical_raw_sha256": RAW_PINS,
        "cba_pdf_page_text_sha256": {"physical_pdf_index_432_printed_409_public_event": "2de972a78a2e5f497b631d75b3b9787a9035e028dbb5510d3d452c21eee565f4", "physical_pdf_index_435_printed_412_fiba_exception": "5706e20bb49fa51155c53696c5e988d45179922c08a99867dc2b5bab7e0b5277"},
        "source_hash_method": "SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF",
        "source_sha256": {SELF: normalized_sha(root / SELF), **REPO_PINS},
    }


def render(data):
    ins = data["institutional_execution"]
    lines = ["# A09 공동 도전: 선택된 가상 기관 실행과 두 국소 기능", "",
             "기존 2023 공동 도전 방향 안에서 최종 12인 두 자리를 교체하고 Chicago·Minnesota가 각각 **비공개 공동훈련·이동·복귀**를 한정 허용하는 가상세계 모델이다. 공개 아시안게임 경기 출전은 선택하지 않았다. 실제 대표팀·구단·보험사의 역사적 결정이나 비공개 문서 인증은 아니다.", "",
             f"- 원역사에서 빠지는 자리: {', '.join(ins['replaced_historical_members'])}",
             "- 대체세계 포함: 이름 미선택인 Minnesota 라이벌, Chicago 주인공; 열두 명 유지",
             "- 보장 한도: 선수별 기존 UPC의 2023–24 잔여 보장급여 위험액 + 치료·귀환 비용 최대 USD 1,000,000. 보험료·실제 약관·기존 급여 수치는 인증하지 않는다.", ""]
    for row in ins["authorities"]:
        lines += [f"- {row['id']} ({row['holder']}): {row['action']} — {row['limit']}"]
    for row in data["functions"]:
        lines += ["", f"## {row['episode_function_id']} · {row['primary_subact']}", "",
                  f"- 정확 진입: {row['entry_state']}", f"- 기능: {row['single_function']}",
                  f"- 선택: {row['unit_choice']}", f"- 현재 비용: {row['direct_present_cost']}"]
        lines += [f"- {b['id']}: {b['action']} 관측: {b['observable']}" for b in row["beats"]]
        lines += [f"- 정확 출구: {row['exit_state']}", f"- 원 CP2 출구: {row['source_cp2_exit_target']} (국소 관측만)"]
    lines += ["", "2023 CBA Article XXIII §3(a)(i)의 일반 공개 비시즌 Basketball Event에는 NBA 서면 승인, 9월 15일 이내, 구단 명시 동의와 NBA 수용 보험 조건이 있다. §3(c)의 국제 FIBA 예외가 Asian Games에 적용되는지는 미확인이다. 이 가상 구단 허용·보장만으로 9월 26일~10월 6일 공개 경기 출전의 적법성이 증명되지 않는다.", "",
              "10월 6일은 비공개 훈련·이동 비용 창의 끝으로 선택한 날짜이며 두 선수의 공개 경기 참가·상대·결과·메달은 선택하지 않았다. 주인공의 Chicago 복귀 훈련은 10월 10일 이후 가상 허용 창이고 NBA 경기 성과가 아니다. 미국 구단 캠프 충돌은 각 구단 원역사 일정에 대한 비용 비교이며 원역사 라이벌 해외원정 참가를 인증하지 않는다.", "",
              "기존 후보 E2/E3 원본은 이력으로 보존한다. 이 새 패킷은 동료 독립 검문 전 등록 증분 0, 전체 A09/G13/G14·실제 Pack·원고 0, 게이트 CLOSED다. 기존 E1 조상 지문 드리프트는 root 소유로 별도 감사한다.", ""]
    return "\n".join(lines)


def validate(data, root=ROOT):
    try:
        return [] if data == build(root) else ["selected A09 packet differs from source-bound construction"]
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
