"""Recompute A08-S1 RT1–RT4 against one current FY22 six-category basis."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

import fitz
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path("design/A08_S1_CURRENT_RT_COST_SLOT_FAMILY_2026_10_07.json")
MARKDOWN = OUTPUT.with_suffix(".md")
SELF = Path("tools/build_a08_s1_current_rt_cost_slot_family.py")
PINS = {
    "design/A08_FINITE_FUNCTION_BATCH_2026_10_07.json": "b84f4d08ede9015934b6d91287c21588bee9443fbaa8bf9ae6d3b1804f8c3b07",
    "research/CHICAGO_2022_COMBINED_CONTRACT_COST_MATRIX_2026_10_07.json": "1ba9e120872bdfab40f26fe2b56a6cff8c6265d94280ea84b5970ffb0d537d33",
    "research/CHICAGO_2022_FULL_COST_ROSTER_FAMILY_2026_10_07.json": "16830b560cf4f2008053ac236202010ff87188f42536a5d36870433933feccf0",
    "research/CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT_2026_10_07.json": "bf8087a89af09a817c0a3eb5d4df906a906575a56016c873912db00eccdca9db",
    "research/CHICAGO_2022_LEGACY_CARRY_REFINEMENT_2026_10_07.json": "ec95c68e5f4fb0ae6a799f2c74705c5c733945719c740b0349bf128be6832c81",
    "simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json": "7d3ab9d0d9e4234e728d4549616acaf84d5b57c4110603cf0114c8bf2c55b8d4",
}
EXIT = "자기 역할 요구를 필요한 동료 기능과 함께 제안하지만 계약과 코어 유지의 결과는 아직 얻지 않는다"
BRADLEY = 2_036_328
VALENTINE = 2_193_930
MINIMUM_FULLCASH_SCREEN = 3_000_000
# Publicly reported 2022-23 full-season Year-1 minimum points, 10 means
# 10+ YOS.  Official successive-year rounding has not been certified here.
REPORTED_MINIMUM_BY_YOS = (1_017_781, 1_637_966, 1_836_090, 1_902_133, 1_968_175,
                  2_133_278, 2_298_385, 2_463_490, 2_628_597, 2_641_682,
                  2_905_851)
PUBLIC_ROUNDING_SCREEN = 10
TWO_YOS_POINT = REPORTED_MINIMUM_BY_YOS[2]
RAW_CACHE = Path(tempfile.gettempdir()) / "fr-a08-rt-minimum-sources-20261007"
RAW_SOURCES = {
    "cba2017.pdf": ("https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf", "65642a3c15990696169d97e55a911cc60e7899aef0d0ecffffe2be28e10f1dfb", 2_186_284),
    "nba2022cap.html": ("https://www.nba.com/news/nba-salary-cap-for-2022-23-season-set-at-just-over-123-million", "818f6ff9daff61df480822954473e33f421fde8559653497eb74bcaaf46c4292", 314_959),
    "minimum2022table.html": ("https://www.hoopsrumors.com/2022/07/nba-minimum-salaries-for-2022-23.html", "35d5aea610753ec8f529c33a770c24b630e32973501d91f5ab7d965ac90ad60c", 71_785),
}
REMOVED_DRAFT_OVERSUPPLY = 407_740_000
SIX = ["LIVE_AND_PROPOSED", "LEGACY_WAIVED_CAMP", "COMPLETED_TW_FA_QO_FRN", "DRAFT_REQUIRED_TENDER", "ROSTER_INCOMPLETE", "ANNUAL_EXCEPTIONS"]
POLICIES = {
    "RT1": (False, False, "Bradley 옵션 유지·Valentine 유지"),
    "RT2": (True, False, "Bradley 옵션 거절·Valentine 유지"),
    "RT3": (False, True, "Bradley 유지·Valentine 방출"),
    "RT4": (True, True, "Bradley 옵션 거절·Valentine 방출"),
}


def sha(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode()).hexdigest()


def verify_raw_sources() -> dict:
    result = {}
    for name, (url, expected, size) in RAW_SOURCES.items():
        path = RAW_CACHE / name
        raw = path.read_bytes()
        assert len(raw) == size and hashlib.sha256(raw).hexdigest() == expected, f"Raw evidence differs: {name}"
        result[name] = {"url": url, "raw_sha256": expected, "bytes": size, "cache_path": str(path)}
    pdf = fitz.open(RAW_CACHE / "cba2017.pdf")
    assert "preceding Salary Cap Year" in pdf[54].get_text()
    assert "1,471,382" in pdf[552].get_text() and "815,615" in pdf[552].get_text()
    assert "two (2) Years of Service" in pdf[281].get_text()
    cap = BeautifulSoup((RAW_CACHE / "nba2022cap.html").read_bytes(), "html.parser").get_text(" ", strip=True)
    assert "$123.655 million" in cap
    soup = BeautifulSoup((RAW_CACHE / "minimum2022table.html").read_bytes(), "html.parser")
    table = soup.find("table")
    assert table is not None
    rows = [[c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])] for tr in table.find_all("tr")]
    reported = []
    for y, row in enumerate(rows[1:12]):
        assert len(row) >= 2 and row[0] == (str(y) if y < 10 else "10+")
        reported.append(int(row[1].replace("$", "").replace(",", "")))
    assert tuple(reported) == REPORTED_MINIMUM_BY_YOS
    result["cba2017.pdf"]["PDF1based_text_sha256"] = {
        str(i+1): hashlib.sha256(pdf[i].get_text().encode()).hexdigest()
        for i in (54, 280, 281, 552)
    }
    pdf.close()
    result["extracted_scope"] = "CBA PDF one-based pages55/281/282/553 rule/base, NBA cap HTML $123.655m, published 11-row reported Year1 scale. Public reported points do not certify official successive-year rounding or a signed UPC."
    return result


def load(root: Path = ROOT) -> dict:
    data = {}
    for rel, expected in PINS.items():
        path = root / rel
        assert sha(path) == expected, f"Reviewed input changed: {rel}"
        data[rel] = json.loads(path.read_text(encoding="utf-8"))
    return data


def branch_cost(base_normal: int, base_apron: int, policy: str, center_signed: bool, guard_signed: bool,
                q_center: int, q_guard: int, bradley_hold_normal: int, *, center_yos: int | None = None,
                guard_yos: int | None = None, center_kind: str = "FA", guard_kind: str = "FA") -> dict:
    """One conditional reported-scale FA proposal; no signed UPC certificate."""
    leave_b, waive_v, _ = POLICIES[policy]
    assert center_signed <= leave_b and guard_signed <= waive_v
    for signed, q, yos, kind in ((center_signed, q_center, center_yos, center_kind),
                                  (guard_signed, q_guard, guard_yos, guard_kind)):
        if signed:
            assert kind == "FA", "Unsigned draft rights and rookie UPCs are not this replacement FA"
            assert type(yos) is int and 0 <= yos <= 10, "Exact YOS is required for a signed FA"
            point = REPORTED_MINIMUM_BY_YOS[yos]
            assert point-PUBLIC_ROUNDING_SCREEN <= q <= point+PUBLIC_ROUNDING_SCREEN, "Proposed full-season cash must stay within the public YOS rounding screen"
            assert q <= MINIMUM_FULLCASH_SCREEN
        else:
            assert q == 0 and yos is None, "Unsigning has no UPC salary or YOS"
    assert bradley_hold_normal >= 0 and (leave_b or bradley_hold_normal == 0)
    live_delta = -BRADLEY * leave_b - VALENTINE * waive_v + q_center + q_guard
    legacy_delta = VALENTINE * waive_v  # full public protected-salary reservation, not paid-money proof
    normal = base_normal + live_delta + legacy_delta + bradley_hold_normal
    # Art. VII §12(f)(2)(ii): the tax screen uplifts 0/1-YOS FA salary to
    # at least a 2-YOS minimum.  Reported point + $10 is a conservative
    # screen, not an official rounding certificate or actual tax invoice.
    apron_center = max(q_center, TWO_YOS_POINT+PUBLIC_ROUNDING_SCREEN) if center_signed and center_yos < 2 else q_center
    apron_guard = max(q_guard, TWO_YOS_POINT+PUBLIC_ROUNDING_SCREEN) if guard_signed and guard_yos < 2 else q_guard
    apron = base_apron - BRADLEY * leave_b - VALENTINE * waive_v + apron_center + apron_guard + legacy_delta
    return {"normal": normal, "apron": apron, "live_delta": live_delta, "legacy_delta": legacy_delta,
            "FA_hold_normal": bradley_hold_normal,
            "signed_FA_fullcash": q_center + q_guard,
            "signed_FA_apron_charge_screen": apron_center + apron_guard,
            "official_minimum_rounding_or_signed_UPC_certified": False,
            "veteran_STD_delta": -int(leave_b) - int(waive_v) + int(center_signed) + int(guard_signed)}


def build(root: Path = ROOT) -> dict:
    docs = load(root)
    raw_evidence = verify_raw_sources()
    e, combined, full, named, legacy, old = (docs[p] for p in PINS)
    e40 = next(r for r in e["functions"] if r["id"] == "A08-EF-001")
    assert e40["global_function_order"] == 40 and e40["exit_state"] == EXIT
    assert e40["published_episode_number"] is None and e40["manuscript_word_count"] is None
    assert len(combined["core10"]) == 10
    core = {r["player"]: r["2022_23_screen_upper_usd"] for r in combined["core10"]}
    assert core["Tony Bradley"] == BRADLEY and core["Denzel Valentine"] == VALENTINE
    assert full["six_category_map"] and [r["id"] for r in full["six_category_map"]] == SIX
    assert full["six_category_map"][1]["upper"] == 20_743_601
    assert full["six_category_map"][3]["first_salary_plus_unlikely_widened_upper"] == 11_060_000
    assert full["six_category_map"][4]["closed_template"]
    assert named["cost_interface"]["removed_overreservation"] == REMOVED_DRAFT_OVERSUPPLY
    assert named["cost_interface"]["new_draft_envelope_total"] == 14_060_000
    assert named["certification"]["independent_review_completed"] and full["certification"]["independent_review_completed"]
    assert legacy["certification"]["independent_review_completed"]
    assert legacy["summary"]["removed_reservation"] == 4_372_601
    assert legacy["summary"]["legacy_upper_after"] == 16_371_000
    assert len(named["refined_compact_cost_cells"]) == len(full["compact_joined_cost_cells"]) == 192
    assert len(old["budget2022_cases"]) == 192 and {r["policy"] for r in old["budget2022_cases"]} == set(POLICIES)
    assert old["selected_route"] is None and not old["contracts_agreed"]
    source_cells = {(c["case"], c["Carter"], c["Protagonist"]): c for c in full["compact_joined_cost_cells"]}
    assert len(source_cells) == 192
    legacy_rows = {(r["case"], r["Carter"], r["Protagonist"], r["source_leaf_stage"]): r for r in legacy["refined_rows"]}
    assert len(legacy_rows) == 576
    rows = []
    for refined in named["refined_compact_cost_cells"]:
        key = (refined["case"], refined["Carter"], refined["Protagonist"])
        base = source_cells[key]
        assert len(refined["states"]) == len(base["states"]) == 3
        for r, b in zip(refined["states"], base["states"]):
            assert r["date"] == b["date"] and r["source_STD_range"] == b["source_STD_range"]
            assert r["normal_full_public_category_outer"] == b["normal_full_public_category_outer"] - REMOVED_DRAFT_OVERSUPPLY
            assert r["apron_full_public_category_outer"] == b["apron_full_public_category_outer"] - REMOVED_DRAFT_OVERSUPPLY
            l = legacy_rows[(*key, r["source_leaf_stage"])]
            assert l["date"] == r["date"] and l["source_normal_upper"] == r["normal_full_public_category_outer"]
            assert l["source_apron_upper"] == r["apron_full_public_category_outer"]
            assert l["normal_upper"] == r["normal_full_public_category_outer"] - 4_372_601
            assert l["apron_upper"] == r["apron_full_public_category_outer"] - 4_372_601
        stage = refined["states"][2]
        assert stage["date"] == "2022-07-07" and stage["source_leaf_stage"] == 2
        assert stage["source_STD_range"][0] == stage["source_STD_range"][1]
        n = stage["source_STD_range"][0]
        current = legacy_rows[(*key, 2)]
        base_n, base_a = current["normal_upper"], current["apron_upper"]
        policies = []
        for policy, (leave_b, waive_v, label) in POLICIES.items():
            # 0 replacement is a conditional no-signing branch, not a lawful $0 signed UPC.
            lower = branch_cost(base_n, base_a, policy, False, False, 0, 0, 0)
            # Upper is the source's deliberately widened fullcash screen, not
            # an actual signed $3m minimum.  Every Year-1 minimum is <= $3m.
            upper_normal_screen = lower["normal"] + MINIMUM_FULLCASH_SCREEN * (int(leave_b)+int(waive_v))
            upper_apron_screen = lower["apron"] + MINIMUM_FULLCASH_SCREEN * (int(leave_b)+int(waive_v))
            possible_incomplete = max(0, 12-(n-int(leave_b)-int(waive_v)))
            assert possible_incomplete <= 1
            incomplete_screen = possible_incomplete * MINIMUM_FULLCASH_SCREEN
            policies.append({
                "policy": policy, "conditional_decision": label,
                "six_category_adjustments": {
                    "LIVE_AND_PROPOSED": f"-{BRADLEY if leave_b else 0} Bradley live -{VALENTINE if waive_v else 0} Valentine live + q_center + q_guard",
                    "LEGACY_WAIVED_CAMP": VALENTINE if waive_v else 0,
                    "COMPLETED_TW_FA_QO_FRN": "Bradley lawful unsigned FA hold H_B >=0 in normal only if option declined and rights not validly renounced; 0 if rights renounced" if leave_b else "unchanged",
                    "DRAFT_REQUIRED_TENDER": "same one-first/one-second economic claims; live rookie UPC requires a free STD place",
                    "ROSTER_INCOMPLETE": f"{n} - {int(leave_b)+int(waive_v)} vacated veterans + signed replacement count + signed rookies <=15; TW <=2 separately. Recompute cap-count incl lawful FA holds; if below12 reserve incomplete screen I_R.",
                    "ANNUAL_EXCEPTIONS": "same candidate no-new-trigger/renunciation family only for lawful minimum replacements; reopen for different signing mechanism",
                },
                "Valentine_full_protected_public_charge_reserved": VALENTINE if waive_v else 0,
                "replacement_contract_variables": {"q_center": "0 if none, else reported 2022-23 full-season minimum(YOS) ±$10 conditional screen, with <=3m separate widened upper" if leave_b else "0",
                                                   "q_guard": "0 if none, else reported 2022-23 full-season minimum(YOS) ±$10 conditional screen, with <=3m separate widened upper" if waive_v else "0",
                                                   "H_B_normal_FA_hold": "0 if validly renounced; otherwise CBA rights hold, value not selected" if leave_b else "0"},
                "normal_public_outer_without_unselected_H_B_range": [lower["normal"], upper_normal_screen+incomplete_screen],
                "apron_conservative_fullcash_outer_range": [lower["apron"], upper_apron_screen+incomplete_screen],
                "H_B_added_to_normal_only_if_retained": leave_b,
                "incomplete_roster_charge_screen_I_R_range": [0, incomplete_screen],
                "incomplete_charge_apron_statutory_classification_certified": False,
                "signed_veteran_STD_before_new_rookie_range": [n-int(leave_b)-int(waive_v), n],
                "available_STD_before_new_rookie_range": [15-n, 15-n+int(leave_b)+int(waive_v)],
                "actual_replacement_or_waiver_selected": False,
            })
        assert policies[0]["normal_public_outer_without_unselected_H_B_range"] == [base_n, base_n]
        assert policies[0]["apron_conservative_fullcash_outer_range"] == [base_a, base_a]
        rows.append({"case": key[0], "Carter": key[1], "Protagonist": key[2],
                     "source_stage": 2, "date": stage["date"], "RT1_source_STD": n,
                     "RT1_current_named_rights_normal_outer": base_n,
                     "RT1_current_named_rights_apron_outer": base_a, "policies": policies})
    assert len(rows) == 192
    # One current source denominator produces all four policy functions; old G8 deltas are excluded.
    return {
        "id": "A08_S1_CURRENT_RT_COST_SLOT_FAMILY_2026_10_07",
        "status": "INDEPENDENTLY_REVIEWED_CONDITIONAL_CURRENT_POLICY_COMPARISON_NOT_CONTRACT_EXECUTION",
        "independent_review_completed": True,
        "independent_review_basis": "Root directly read CBA one-based55/282/553 and published11-row table; raw bytes and source pins checked. Same $1/draft-as-FA counterexamples rejected; 0YOS FA normal148981453/apron149799772 separated. Independently recalculated all768 lower policy rows; legacy protected amount and authority limits preserved.",
        "source_sha256": {**PINS, str(SELF): sha(root / SELF)},
        "source_hash_method": "BOM-stripped LF-normalized UTF-8 bytes SHA-256; external raw bytes separate",
        "raw_source_evidence": raw_evidence,
        "E40_exact_exit": EXIT,
        "cost_basis": "2022-07-07 stage2 current named-rights 192 public-category cells, joined one-to-one to fullcost and reviewed 576-row legacy correction (duplicate camp reservation removed, old stretch preserved); RT1 retained Bradley/Valentine baseline is a conditional reconstruction, not a selected policy",
        "six_public_categories": SIX,
        "core_public_screen_upper": {"Tony Bradley": BRADLEY, "Denzel Valentine": VALENTINE},
        "replacement_family": "Only optional one-year full-season 2022-23 no-bonus FA minimum proposals within each publicly reported YOS point ±$10. This interval is a conservative proposal screen, not an official rounded salary or a signed UPC. $1 is rejected; $3m is only the reviewed widened fullcash upper screen, never chosen as a minimum wage. For 0/1 YOS, apron screen uses max(candidate cash, reported 2-YOS point+$10); for 3+ YOS fullcash is retained as an upper despite possible reimbursement. Actual YOS, contract, notice, signatures remain null. Draft rookie UPCs are separate. Nonminimum signing reopens the formula. One possible incomplete-roster fullcash screen up to3m is separately reserved if RT4 leaves only11 signed STD and other cap-count identities do not cover it; statutory apron inclusion is not asserted.",
        "minimum_salary_reference": {
            "CBA_2017_ArtII6_ExhibitC_and_ArtVII12f": "https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf",
            "NBA_2022_23_cap_release": "https://www.nba.com/news/nba-salary-cap-for-2022-23-season-set-at-just-over-123-million",
            "published_reported_fullseason_year1_points_2022_23_by_YOS_0_to_10plus": list(REPORTED_MINIMUM_BY_YOS),
            "public_proposal_rounding_screen_usd_each_side": PUBLIC_ROUNDING_SCREEN,
            "two_YOS_apron_floor_upper_screen": TWO_YOS_POINT+PUBLIC_ROUNDING_SCREEN,
            "official_successive_year_rounding_verified": False,
            "exact_legal_UPC_salary_or_actual_contract_certified": False,
        },
        "formula_rows": rows,
        "summary": {"current_source_cells": 192, "RT_policy_functions": 4,
                    "current_policy_cell_rows": 192*4,
                    "old_G8_48x4_partial_deltas_added_to_current": False,
                    "Valentine_full_protected_charge_reserved_if_waived": VALENTINE,
                    "Bradley_FA_hold_if_option_declined": "H_B symbolic normal-only until rights/renunciation resolved",
                    "unselected_formula_is_final_budget_or_contract": False},
        "fictional_agent_handoff": {
            "same_E40_proposal_material": True,
            "observable_action": "주인공은 기존 역할 제안 한 장에 같은 192조건 기준의 RT1–RT4 자리·공개 비용 함수 범위를 붙여 가상 에이전트에게 건넨다. Bradley 권리 H_B와 Valentine 보호급여를 별도 표시하고 어떤 대체선수도 서명한 것으로 쓰지 않는다.",
            "direct_present_cost": "자기 공격 역할만 밀어붙이는 시간을 줄이고, 필요한 센터·가드 기능의 상실 가능성과 예산 책임을 함께 설명한다.",
            "observable_exit": "에이전트가 네 정책의 동일 기준 비교와 미정 H_B·대체선수 질문을 접수한다. 실제 협상 답·프런트 선택·다른 선수 동의는 미관측이다.",
            "new_final_function_or_planned_slot": 0,
        },
        "RT_policy_selected": None,
        "actual_contract_price_or_acceptance": None,
        "actual_FY22_roster_or_tax_bill_certified": False,
        "A08_S1_original_CP2_whole_success_certified": False,
        "whole_A08_or_G13_complete": False,
        "actual_context_packs": 0,
        "manuscript_count": 0,
        "manuscript_allowed": False,
        "design_gate": "CLOSED",
        "new_author_lock": False,
    }


def render(data: dict) -> str:
    rows = data["formula_rows"]
    def span(policy: str, field: str) -> tuple[int, int]:
        nums = [r["policies"][list(POLICIES).index(policy)][field] for r in rows]
        return min(n[0] for n in nums), max(n[1] for n in nums)
    lines = ["# A08-S1 현재 FY22 RT1–RT4 비용·자리 함수", "", "기존 E40의 역할 제안과 같은 가상 에이전트에게 전달할 조건부 비교표다. 2022-07-07 stage2 현재 192개 명명 드래프트권 공개 범주 셀을 원 전체비용 셀과 조인하고, 검토된 576행 legacy 보정에서 중복 캠프 예약 $4,372,601을 제거했다. 과거 stretch 보수 $16,371,000의 보수적 보호는 남겼다. 기존 G8의 48×4 부분 예산 차이는 현재 금액에 더하지 않았다.", "", "| 정책 | 현재 normal 공개 외곽 구간, H_B 제외 | 보수적 apron 전액 스크린 | 명단 조건 |", "|---|---:|---:|---|",]
    for policy, (leave_b, waive_v, label) in POLICIES.items():
        n, a = span(policy, "normal_public_outer_without_unselected_H_B_range"), span(policy, "apron_conservative_fullcash_outer_range")
        lines.append(f"| {policy} {label} | ${n[0]:,}–${n[1]:,} | ${a[0]:,}–${a[1]:,} | 기존 STD −{int(leave_b)+int(waive_v)} + 실제 서명 대체 0..{int(leave_b)+int(waive_v)} + 실제 서명 신인 ≤15 |")
    lines += ["", "표의 하한은 대체선수 미서명, 상한은 떠난 자리마다 최소계약을 제안할 수 있는 경우 각각 $3m 공개 보수 스크린과 명단 미달 가능액을 보수적으로 예약한 값이다. $3m를 실제 최소계약 급여로 선택한 것이 아니다. 원 CBA는 전년 캡 대비 매년 조정하므로 2017→2022 단일 비율로 11행의 법정 정확 반올림을 증명하지 않았다. 별도 공개 2022–23 급여표의 YOS별 보고점 ±$10을 조건부 제안 범위로 사용하고 실제 서명·정확 UPC를 인증하지 않는다. 예컨대 0YOS 일반 FA 보수 보고점 $1,017,781의 제안은 0/1YOS 세금 규칙에 따라 2YOS 보고점 $1,836,090의 보수적 상단 $1,836,100으로 에이프런 스크린을 따로 비교한다. 하한의 $0은 선수 계약이 아니라 미서명이다. RT4가 기존 서명 13명인 조합에서 둘 다 이탈하고 대체선수가 없으면 11명일 수 있어 incomplete charge I_R을 0–$3m로 별도 예약한다. 다른 유효 FA 보류 인원이 cap-count를 메울 수 있으므로 실제 I_R은 미선택이며, apron에 법정 산입된다고 주장하지 않는 보수적 전액 스크린이다. RT2·RT4의 Bradley 옵션 거절 후 FA 보류액 H_B를 권리 유지 시 normal에 별도로 더한다. 유효 권리 포기 시 H_B=0이며 실제 포기는 선택되지 않았다. 현재 공개 자료만으로 H_B의 값을 정하지 않는다.", "", f"Valentine 방출 RT3·RT4는 기존 live ${VALENTINE:,}를 빼고 같은 전액 공개보수 ${VALENTINE:,}를 보호급여/legacy 예약으로 되돌려 놓았다. 실제 지급·합의액 또는 방출이 확정됐다는 뜻이 아니다. Bradley 옵션 거절 RT2·RT4만 기존 live ${BRADLEY:,}를 빼며, 대체 센터 q_C를 별도 더한다. 에이전트 자료에는 여섯 범주별 변환과 192×4 조건식이 JSON에 있다.", "", "최종 표준 15자리/투웨이 2자리, 새 신인 실제 서명, CBA 권리·보류액, 추가 예외·하드캡, 모든 선수 계약·프런트 RT 선택은 미확정이다. E40 뒤 같은 자료 전달만 관측하며 새 회차·최종 기능은 0. 전체 A08/G13·원고 게이트는 닫혀 있다.", "", "## 법규·수치 근거", "", "- [2017 NBA–NBPA CBA, Article II §6·Exhibit C·Article VII §12(f)(2)(ii)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf): 전시즌 YOS별 최소 보수의 매년 조정과 0/1YOS 일반 FA의 2YOS 세금 기준.", "- [NBA 2022–23 샐러리캡 공지](https://www.nba.com/news/nba-salary-cap-for-2022-23-season-set-at-just-over-123-million): 적용 캡연도와 공개 캡 수준.", "- [2022–23 공개 최소급여표](https://www.hoopsrumors.com/2022/07/nba-minimum-salaries-for-2022-23.html): 11개 YOS 보고점. 이는 원 CBA의 공식 반올림 인증이나 개별 계약 영수증이 아니다.", "", "세 원문 raw 바이트의 SHA-256·크기·임시 캐시 경로와 읽은 페이지/표는 JSON `raw_source_evidence`에 있다.", "", "## 출처", ""]
    lines += [f"- `{p}` — LF SHA-256 `{h}`" for p, h in data["source_sha256"].items()]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    data = build()
    raw = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    md = render(data)
    if args.write:
        (ROOT / OUTPUT).write_text(raw, encoding="utf-8", newline="\n")
        (ROOT / MARKDOWN).write_text(md, encoding="utf-8", newline="\n")
    if args.check:
        assert (ROOT / OUTPUT).read_text(encoding="utf-8") == raw
        assert (ROOT / MARKDOWN).read_text(encoding="utf-8") == md
        print("A08-S1 current RT policy cost/slot family current; conditional comparison independently reviewed")


if __name__ == "__main__":
    main()
