"""Source-bound, bounded A08-S1 RT policy comparison; no contract selection."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path("design/A08_S1_COSTED_POLICY_ADDENDUM_2026_10_07.json")
MD = OUT.with_suffix(".md")
PINS = {
    "design/A08_FINITE_FUNCTION_BATCH_2026_10_07.json": "b84f4d08ede9015934b6d91287c21588bee9443fbaa8bf9ae6d3b1804f8c3b07",
    "research/CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT_2026_10_07.json": "bf8087a89af09a817c0a3eb5d4df906a906575a56016c873912db00eccdca9db",
    "research/CHICAGO_2022_FULL_COST_ROSTER_FAMILY_2026_10_07.json": "16830b560cf4f2008053ac236202010ff87188f42536a5d36870433933feccf0",
    "simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json": "7d3ab9d0d9e4234e728d4549616acaf84d5b57c4110603cf0114c8bf2c55b8d4",
}
EXPECTED_EXIT = "자기 역할 요구를 필요한 동료 기능과 함께 제안하지만 계약과 코어 유지의 결과는 아직 얻지 않는다"
POLICY = {
    "RT1": (0, 0, False, "Bradley 옵션과 Valentine 유지", "기존 두 기능 보유"),
    "RT2": (1, 1, False, "Bradley 이탈·Valentine 유지", "센터 기능 대체 1자리 조건"),
    "RT3": (1, 1, True, "Bradley 유지·Valentine 방출", "가드 기능 대체 1자리 조건"),
    "RT4": (2, 2, True, "Bradley 이탈·Valentine 방출", "센터·가드 기능 대체 2자리 조건"),
}


def sha(path: Path) -> str:
    normalized = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode()).hexdigest()


def load_sources(root: Path = ROOT) -> dict:
    docs = {}
    for rel, expected in PINS.items():
        path = root / rel
        assert sha(path) == expected, f"Reviewed source changed: {rel}"
        docs[rel] = json.loads(path.read_text(encoding="utf-8"))
    return docs


def build(root: Path = ROOT) -> dict:
    docs = load_sources(root)
    e = docs["design/A08_FINITE_FUNCTION_BATCH_2026_10_07.json"]
    n = docs["research/CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT_2026_10_07.json"]
    full = docs["research/CHICAGO_2022_FULL_COST_ROSTER_FAMILY_2026_10_07.json"]
    g = docs["simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json"]
    f = next(x for x in e["functions"] if x["id"] == "A08-EF-001")
    assert f["global_function_order"] == 40 and f["exit_state"] == EXPECTED_EXIT
    assert f["published_episode_number"] is None and f["manuscript_word_count"] is None
    assert n["status"].startswith("INDEPENDENTLY_REVIEWED_")
    assert full["status"].startswith("INDEPENDENTLY_REVIEWED_")
    assert n["cost_interface"]["new_draft_envelope_total"] == 14_060_000
    assert len(n["refined_compact_cost_cells"]) == 192
    assert len(g["budget2022_cases"]) == 192
    cells = n["refined_compact_cost_cells"]
    assert all(len(c["states"]) == 3 and c["states"][2]["source_leaf_stage"] == 2 for c in cells)
    stage2 = [c["states"][2] for c in cells]
    costs = {
        "normal_public_outer_range": [min(s["normal_full_public_category_outer"] for s in stage2), max(s["normal_full_public_category_outer"] for s in stage2)],
        "apron_public_outer_range": [min(s["apron_full_public_category_outer"] for s in stage2), max(s["apron_full_public_category_outer"] for s in stage2)],
        "signed_veteran_STD_range": [min(s["source_STD_range"][0] for s in stage2), max(s["source_STD_range"][1] for s in stage2)],
        "named_first_claim_upper": 1,
        "named_second_claim_upper": 1,
        "new_draft_rights_reservation_outer": n["cost_interface"]["new_draft_envelope_total"],
        "scope": "2022-07-07 stage2, 192 unselected public-category cells; no RT1–RT4 selection or verified alignment to an old G8 case; not a selected roster, salary, tax payment or cap clearance",
    }
    # Pair all four old G8 policies on identical 48 parameter tuples. These deltas
    # never become current full-category FY22 deltas.
    key = lambda c: (c["protagonist_first"], c["Carter_first"], c["Young_or_replacement"], c["draft2022_reserve"])
    by_policy = {p: {key(c): c for c in g["budget2022_cases"] if c["policy"] == p} for p in POLICY}
    assert all(len(v) == 48 and set(v) == set(by_policy["RT1"]) for v in by_policy.values())
    base = by_policy["RT1"]
    rows = []
    for p, (vacated, replacement, waiver, label, function) in POLICY.items():
        diffs = {by_policy[p][k]["known_budget_excluding_dead_salary"] - base[k]["known_budget_excluding_dead_salary"] for k in base}
        assert len(diffs) == 1
        assert all(by_policy[p][k]["standard_slots"] == 15 for k in base)
        assert all(by_policy[p][k]["Valentine_waiver_charge_requires_resolution"] == waiver for k in base)
        rows.append({
            "policy": p,
            "conditional_action": label,
            "role_function_at_risk": function,
            "veteran_slots_vacated_if_executed": vacated,
            "replacement_signings_assumed_in_old_G8_partial": replacement,
            "old_G8_48_paired_partial_budget_delta_vs_RT1_USD": diffs.pop(),
            "old_G8_partial_budget_excludes_confirmed_dead_salary": True,
            "current_FY22_named_rights_full_category_policy_delta_USD": None,
            "current_FY22_delta_expression": "recompute this RT policy and RT1 independently from current six public categories under identical contract/draft assumptions; subtract recomputed RT1, not the older G8 partial delta or a bare current cell",
            "slot_expression": "reviewed stage2 signed_veteran_STD - vacated veterans + actually signed replacements + actually signed rookies; must be <=15, TW separately <=2",
            "Valentine_waiver_charge_unresolved": waiver,
            "contract_or_roster_selected": False,
        })
    assert [r["old_G8_48_paired_partial_budget_delta_vs_RT1_USD"] for r in rows] == [0, -36_318, -193_920, -230_238]
    return {
        "id": "A08_S1_COSTED_POLICY_ADDENDUM_2026_10_07",
        "status": "INDEPENDENTLY_REVIEWED_ROUTINE_QUESTIONS_NOT_CURRENT_RT_COST_EXECUTION",
        "independent_review_completed": True,
        "source_sha256": {**PINS, "tools/build_a08_s1_costed_policy_addendum.py": sha(root / "tools/build_a08_s1_costed_policy_addendum.py")},
        "source_hash_method": "UTF-8 BOM removed CRLF/CR to LF SHA-256",
        "previous_final_function": {"id": f["id"], "global_function_order": 40, "exact_exit": f["exit_state"]},
        "decision_source": "G8 RT1–RT4 old 48-parameter paired budget cases + current named-rights 192-cell FY22 public-category envelope; separate denominators",
        "reviewed_public_category_stage2_unselected_RT": costs,
        "paired_G8_policies": rows,
        "fictional_operating_addendum": {
            "authority": "주인공은 역할 제안과 공개 조건부 비교를 가상 에이전트에게 전달한다. 프런트만 계약·명단을 결정하고 다른 선수의 동의는 미확인이다.",
            "action": "E40에서 건넨 같은 역할 자료에 RT1 유지 및 RT2–RT4 대체 조건별 빠질 수 있는 기능, 표준 명단 자리 식과 잔여 공개 급여 비용의 재계산 항목을 덧붙여 에이전트에게 건넨다.",
            "direct_present_cost": "허용된 준비 시간 일부를 추가 비교와 질문 정리에 써서 자기 공격 역할만 주장하는 제안보다 좁은 자기 몫을 받아들인다.",
            "observable_exit": "에이전트가 네 조건부 정책의 자리·비용 질문을 받은 상태이며, 계약 수락·가격·프런트 선택·선수 방출은 관측되지 않는다.",
            "information_access": "주인공은 자기 제안과 공개 예산 구간만 안다. 에이전트가 비공개 프런트 판정, 타 선수 계약 의사, 정확 2022 지명 결과를 안다고 가정하지 않는다.",
            "new_episode_function_or_slot": 0,
        },
        "unresolved_inputs": ["RT별 6공개범주 재산출", "Bradley 옵션 및 Valentine 방출 실제 실행과 waiver charge", "대체선수 실제 서명·가격", "2022 신인 실제 지명·서명", "LaVine/주인공/Carter/Young/Satoransky 정확 새 계약", "기관 명단·하드캡 합법성 최종 판단"],
        "G8_RT1_or_alternative_selected": False,
        "actual_2022_contract_accepted": False,
        "full_FY22_roster_and_cost_certified": False,
        "original_CP2_G8_current_remaining_salary_and_slot_comparison_certified": False,
        "whole_A08_or_G13_complete": False,
        "actual_context_packs": 0,
        "manuscript_count": 0,
        "manuscript_allowed": False,
        "design_gate": "CLOSED",
        "new_author_lock": False,
    }


def render(d: dict) -> str:
    c = d["reviewed_public_category_stage2_unselected_RT"]
    lines = ["# A08-S1 G8 자리·잔여 급여 비교 보강", "", "E40의 동일 역할 제안 자료에 덧붙이는 국소 운영 설계다. 새 최종 기능·회차·계약 선택은 없다.", "", "## 현재 공개 비용 범위", "", f"2022-07-07 3단계 명명 드래프트권 192개 미선택 조합에서 공개 범주 외곽은 normal ${c['normal_public_outer_range'][0]:,}–${c['normal_public_outer_range'][1]:,}, apron ${c['apron_public_outer_range'][0]:,}–${c['apron_public_outer_range'][1]:,}이다. 이 192개는 기존 G8 RT1–RT4 각 사례와 검증된 1:1 연결이 아니다. 기존 서명 선수 자리 범위는 {c['signed_veteran_STD_range'][0]}–{c['signed_veteran_STD_range'][1]}이며, 2022 첫·둘째 지명권 경제 예약의 합계 상한은 ${c['new_draft_rights_reservation_outer']:,}이다. 이는 계약 확정액이나 최종 명단이 아니다.", "", "## G8 같은 조건 48건의 부분 예산 차이", "", "| 정책 | 조건 | 위험 기능 | RT1 대비 과거 부분 예산 차이 | 빈 자리/대체 가정 |", "|---|---|---|---:|---|",]
    for r in d["paired_G8_policies"]:
        lines.append(f"| {r['policy']} | {r['conditional_action']} | {r['role_function_at_risk']} | ${r['old_G8_48_paired_partial_budget_delta_vs_RT1_USD']:,} | {r['veteran_slots_vacated_if_executed']} / {r['replacement_signings_assumed_in_old_G8_partial']} |")
    lines += ["", "이 차이는 옛 G8 부분 예산의 동일 48조건 비교다. 새 FY22 공개 범주 총액에 가산할 값이 아니다. 각 대안의 현재 총비용은 옵션·방출 비용·대체 계약·보유권·신인 예약을 같은 계약/지명 가정으로 RT1과 각 대안을 각각 재계산해야 한다. RT3·RT4의 Valentine 방출 비용은 미해결이다. 표준 15자리와 투웨이 2자리는 실제 서명 후 다시 검문한다.", "", "## 가상 제안 행동과 출구", "", d["fictional_operating_addendum"]["action"], "", f"직접 비용: {d['fictional_operating_addendum']['direct_present_cost']}", "", f"관측 출구: {d['fictional_operating_addendum']['observable_exit']}", "", "프런트 결정·다른 선수 서명·정확 가격·2022 지명/명단·의료·실제 계약은 인증하지 않는다. 전체 A08/G13 및 원고 게이트는 닫혀 있다.", "", "## 출처", ""]
    lines += [f"- `{p}` — LF SHA-256 `{h}`" for p, h in d["source_sha256"].items()]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    d = build()
    raw = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
    md = render(d)
    if args.write:
        (ROOT / OUT).write_text(raw, encoding="utf-8", newline="\n")
        (ROOT / MD).write_text(md, encoding="utf-8", newline="\n")
    if args.check:
        assert (ROOT / OUT).read_text(encoding="utf-8") == raw
        assert (ROOT / MD).read_text(encoding="utf-8") == md
        print("A08-S1 routine questions current; current RT cost execution remains pending")


if __name__ == "__main__":
    main()
