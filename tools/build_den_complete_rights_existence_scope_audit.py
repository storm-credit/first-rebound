"""Preserved named-rights legal existence family; no actual future or private-world certification."""
from pathlib import Path
from copy import deepcopy
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "43e359c3a5c0dffb4d3c02f401ad0ed286b202bd"
SELF = "tools/build_den_complete_rights_existence_scope_audit.py"
OUT = ROOT / "research/DEN_COMPLETE_RIGHTS_EXISTENCE_SCOPE_AUDIT_2026_10_07.json"
MD = OUT.with_suffix(".md")
REVIEWED_INPUT_SHA = {'canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json': 'e0d8ed1f82c494a3610a91c779eef5573737f9b818088c903786cb12afae7dc9', 'canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json': 'ab996ffb9f9f6e4471ad473633af1529eb4928e3aa9a17b99642c591691c3798', 'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json': 'c0166bba7a0874aa08dfa88e7d00c0f0d0e237ca2090459ddd6167cf1353c5ea', 'simulation/CAUSALITY_MODEL.md': '00638830864e9503db4589464806cc0c4c0d94002b039a8bf661d96e6f6a7c45', 'simulation/2020_DRAFT_RJ_HAMPTON_RELANDING_BOARD.md': '9c78d49f12b8068ea2c8dd91999b64e535a716d5dadedbbad3abdcc1cf6d1c22', 'research/BOS_NAMED_RIGHTS_ASSIGNMENT_WITNESS_2026_10_06.json': 'a697079527d2724ed11943246a8af64a1159354d57ae9cbc811a356ceb5254f0', 'research/DEN_NAMED_CONDITIONAL_RIGHTS_WITNESS_2026_10_06.json': 'db0c3fb87c5a6d6b04c6bc8f0e612278e6381285cc86672c044b6a20ff5198f2', 'research/DEN_THETA_TRANSITION_DOMAIN_2026_10_07.json': '21abc9a6b4d4c33cdd97e91cf5c4d9074ee77df9a06d6b96d40494094300cb85', 'research/DEN_F5_RESOURCE_FRAME_REVIEW_2026_10_07.json': 'ae1ac9ae5720c61aeabf5260bcbbd809cd293e2bfe62de8f0272dd7e1bf9e0bb', 'research/DEN_PRIMARY_GUIDE_TERMS_COLLECTION_2026_10_07.json': '3ee186b2f63578c486c977d5d6f2ae567bfe5ede245cd37195f0927d41390ad2', 'research/DEN_T1_T3_DATED_MATCHING_WITNESS_2026_10_06.json': '4fe78e44c10e6a42e45dafda470b4a0c006b48e6b573dd8afbf8002c18020ee9', 'control/CHICAGO_2020_21_D1_S2_PROTOCOL.md': 'a403bc5dfde53294601f094f2022f1d9ed4336593611d6f45d92cf137fc9b309'}


def normalized(p):
    return p.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def sha(p):
    return hashlib.sha256(normalized(p).encode("utf-8")).hexdigest()


def load(f):
    return json.loads(normalized(ROOT / f))


def build():
    for f, h in REVIEWED_INPUT_SHA.items():
        if sha(ROOT / f) != h:
            raise ValueError("reviewed original family changed: " + f)
    s2 = load("canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json")
    if s2["selected"]["route"] != "S2_LEGAL_INTERVAL_PROOF_COUNTERFACTUAL_AUTHOR_MODEL":
        raise ValueError("S2 authority changed")
    choice = load("canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json")
    if choice["selected"]["F5_MCGEE"] != "Denver and Cleveland do not execute their 2021-03-25 JaVale McGee/Isaiah Hartenstein and two-second-round-pick trade; McGee remains with Cleveland and Hartenstein with Denver.":
        raise ValueError("approved F5 omission changed")
    prior = load("research/DEN_THETA_TRANSITION_DOMAIN_2026_10_07.json")
    named = load("research/DEN_NAMED_CONDITIONAL_RIGHTS_WITNESS_2026_10_06.json")
    guides = load("research/DEN_PRIMARY_GUIDE_TERMS_COLLECTION_2026_10_07.json")
    match = load("research/DEN_T1_T3_DATED_MATCHING_WITNESS_2026_10_06.json")
    if not match["dated_matching_subbranch_pass"]:
        raise ValueError("matching prerequisite not passed")
    graph = prior["joint_graph_transform"]
    original = graph["original_public_edges"]
    deleted = ["F5_MCGEE", "F5_HARTENSTEIN", "F5_DEN2023_SECOND", "F5_DEN2027_SECOND"]
    candidate = []
    for edge in original:
        if edge["id"] in deleted:
            continue
        e = deepcopy(edge)
        if e["id"] in ["DEN24_PLAYER", "T1_ROOKIE"]:
            e["payload"] = "Zeke Nnaji"
        candidate.append(e)
    if candidate != graph["alternate_candidate_public_edges"]:
        raise ValueError("candidate delta differs from reviewed complete public graph")
    if graph["historical_contract_objects"] != graph["alternate_candidate_contract_objects"]:
        raise ValueError("original contractual object identity changed")
    raw = []
    primary = prior["primary_rule"]
    raw.append(dict(id="NBA2019_BYLAWS", path=primary["path"], raw_sha256=primary["raw_sha256"], url=primary["url"]))
    official = prior["new_primary_public_graph_source"]
    raw.append(dict(id="NBA_COMPLETED_NOV2020", path=official["cache_path"], raw_sha256=official["raw_sha256"], url=official["url"]))
    for s in guides["sources"]:
        raw.append(dict(id=s["id"], path=s["cache_path"], raw_sha256=s["raw_sha256"], url=s["url"], locator=s["read_locator"]))
    for source in named["source_recoveries"]:
        if source.get("cache_path") and source.get("raw_sha256"):
            raw.append(dict(id=source["id"], path=source["cache_path"], raw_sha256=source["raw_sha256"], url=source["url"]))
    for source in raw:
        if hashlib.sha256(Path(source["path"]).read_bytes()).hexdigest() != source["raw_sha256"]:
            raise ValueError("original raw changed: " + source["id"])
    branch_ids = ["prior_1R_conveys", "prior_1R_converts_to_2R", "subsequent_1R_protection_and_termination"]
    family = {
        "identity": "Same source-anchored complete historical P/G economic rights and all retained prior burdens, priorities, conversion, linkage, protection and termination obligations",
        "preservation_kind": "CANDIDATE_IMPLEMENTATION_FAMILY_CONDITION_NOT_GLOBAL_PRIVATE_FACT",
        "preserve_retained_obligation_relation_not_AST_only": True,
        "preserve_all_other_already_committed_claim_realizations": True,
        "rank_paths": "Every admissible external rank/event path of the original conditional rights; no actual future path chosen",
        "changed_players": ["DEN24 and T1 rookie payload Hampton->Nnaji", "F5 McGee remains CLE and Hartenstein remains DEN"],
        "deleted_F5_claim_objects": ["theta.F5_DEN2023_second", "theta.F5_DEN2027_second"],
        "released_capacity_not_newly_spent": True,
        "underlying_future_pick_owner": None,
        "historical_F5_claims_made_unconditional": False,
        "new_contract_terms_selected": False,
        "all_private_portfolio_clauses_absent_certified": False,
        "authority_support": ["Existing approved T1/DEN24 economic template preservation", "Existing F5 omission direction", "CAUSALITY_MODEL changed-inputs-only and source-preserved baseline family", "Same accepted BOS named-right assignment existence scope"],
        "counterfactual_family_is_not_actual_negotiated_acceptance": True,
    }
    proof = {
        "classification": "SYMBOLIC_SIMULATION_RELATION_FOR_PRESERVED_CANDIDATE_FAMILY",
        "original_anchor": "NBA publicly completed Nov2020 P acquisition and March2021 G assignment; 4.02 provides actual full enforceable original theta_star anchor",
        "not_legal_by_definition": "theta_star names the actual original source-anchored economic rights, not an arbitrary member of a set defined to be lawful",
        "theorem": "For every feasible original complete retained-right realization H(theta,r), project away the omitted conditional F5 outgoing claims and keep every retained obligation realization. The resulting candidate H_alt is feasible in this preserved family.",
        "construction": [
            "Choose the original complete feasible rights realization anchored by the original completed assignments, parametrically in every admissible future path r.",
            "Carry P/G and every other retained contractual economic obligation realization and original priority/reference identities unchanged, including prior conversion and G rollover/termination.",
            "Remove only the F5 conditional allocations to CLE when they would be active; if protection would make the allocation zero, remove zero. Do not infer unconditional CLE or DEN underlying ownership.",
            "Leave any released resource unused; every other team retains its already committed original claim realization. New future CLE spending of an omitted F5 receipt is outside March25 proof and reopens descendants.",
            "First-round claim/retention projection is unchanged. For each dated resource u, retained used_alt(u)=used_hist(u)-used_F5(u)<=used_hist(u)<=capacity_hist(u). Every surviving allocation and its priority still has its original witness.",
            "The changed rookie/player payloads are handled by the previously accepted matching/registration/cost witnesses and do not silently change P/G asset consideration.",
        ],
        "conditional_resource_algebra": {
            "symbols": ["C(u,r)", "D_ret(u,theta,r)", "D_F5(u,theta,r)"],
            "premise": "D_ret>=0, D_F5>=0, D_ret+D_F5<=C in a feasible original realization",
            "conclusion": "D_ret<=C after omission; the released amount is not committed to a new claim",
            "proof": "D_ret<=D_ret+D_F5<=C, including D_F5=0 on protected/terminated outcomes",
            "sample_enumeration_used_as_whole_proof": False,
        },
        "quantifiers": "For every admissible original source-preserved theta and future path with a lawful original realization, there exists the projected candidate realization; instantiate source-anchored actual theta_star. Not every imagined report-compatible theta is asserted lawful.",
        "all_three_asset_branches_covered_in_declared_family": True,
        "same_future_rank_or_delivery_required": False,
        "actual_unreported_global_state_simulation_proved": False,
        "private_hidden_clause_absence_required": False,
        "root_review_of_family_scope_support_required": True,
    }
    branches = []
    for bid in branch_ids:
        branches.append(dict(id=bid, status="CONDITIONAL_RELATION_LEMMA_ONLY_NOT_LEGAL_BOUND_PASS", witness="Same complete symbolic original obligation realization and omission projection; no branch numeric realization omitted", exact_terms=None, actual_future_delivery=None))
    return {
        "schema_version": 2, "baseline_main": BASELINE, "date_local": "2026-10-07",
        "status": "CONDITIONAL_RELATION_LEMMA_VALID_WHOLE_BRANCH_PROMOTION_REJECTED",
        "source_hash_convention": "SHA256_UTF8_NO_BOM_CRLF_CR_TO_LF",
        "source_sha256": {**REVIEWED_INPUT_SHA, SELF: sha(ROOT / SELF)},
        "source_versions_pinned": True, "raw_sources": raw,
        "original_S2_rule": s2["selected"]["legal_rule"],
        "classification": {"fact": "Actual completed original acquisitions and published original rights/dated transactions; existing author directions", "inference": "Existence of projected feasible rights realization in the expressly preserved economic family", "candidate": "Complete P/G economic obligation relation retained while F5 allocations are omitted and freed resources left unused", "author_locked": "Existing directions only; exact theta, numeric protections, waiver or future outcome not selected"},
        "scope_comparison": {"same_named_assignment_existence_scope_as_BOS": True, "DEN_all_required_asset_branch_categories_present": True, "March25_legal_existence_not_actual_future_execution": True, "prior_scope_audit_correction": "Unknown general portfolio predicates are not automatically members of the approved source-supported public family. Same output or no hidden clause is not a new mandatory S2 condition.", "policy_changed": False},
        "family": family, "symbolic_witness": proof,
        "joint_public_graph": {"original_edges": original, "candidate_edges": candidate, "removed_edges": deleted, "retained_contract_objects": graph["historical_contract_objects"], "global_full_state_equals_history": False},
        "branches": branches,
        "matching": {"already_passed": True, "source": "research/DEN_T1_T3_DATED_MATCHING_WITNESS_2026_10_06.json", "new_matching_execution_count": 0},
        "previous_probe_interpretation": {"actual_F5_dependent_clause_found": False, "actual_theta_star_illegal_counterexample_found": False, "abstract_same_AST_probe_is_actual_source_counterexample": False, "unknown_hypothetical_nonmonotone_obligations_must_be_added_to_public_family": False},
        "reopen": ["Source-supported retained-right obligation depends on omitted F5 transaction in a way that defeats this preserved candidate economic realization", "New related rights/priority/spending or changed P/G consideration", "Candidate no longer preserves the complete original economic rights relation", "Actual acceptance/future execution requested; descendants require dated verification"],
        "authority": {"proposed_all_three_asset_legal_bound_pass": False, "whole_branch_source_verified": False, "whole_branch_complete_domain": False, "new_asset_PASS": 0, "whole_row_promoted": False, "independent_review_completed": False, "actual_theta_values": None, "actual_waiver_or_new_financial_choice": None, "actual_future_delivery": None, "actual_recipient_acceptance": None, "private_global_absence_certified": False, "register_central_prior_file_edits": 0, "manuscript_allowed": False},
        "verification_scope": {"pinned_source_and_direct_graph_delta": True, "symbolic_nonnegative_resource_inequality": True, "old_48_or_81_abstract_enumerations_reexecuted": 0, "additional_same_AST_test_counted_as_legal_proof": 0, "whole_actual_private_contract_world_verified": False, "family_preservation_source_support_complete": False, "original_nonempty_anchor_implies_projected_same_contract_family_coverage": False},
        "tools": {"Antigravity": "NOT_RUN", "NotebookLM": "PROCESS_TIMEOUT_ANALYSIS_NOT_RECOVERED", "Claude": "RETURNED_LIMITED_LOGIC_REBUTTAL"},
        "external_tool_records": {"NotebookLM": {"path": "reviews/DEN_PRESERVED_RIGHTS_NLM_2026_10_07.json", "source_sha256": sha(ROOT/"reviews/DEN_PRESERVED_RIGHTS_NLM_2026_10_07.json"), "import_seconds": 18.345, "query_seconds": 70.041, "analysis_recovered": False}, "Claude": {"path": "reviews/DEN_PRESERVED_RIGHTS_CLAUDE_BLIND_2026_10_07.json", "source_sha256": sha(ROOT/"reviews/DEN_PRESERVED_RIGHTS_CLAUDE_BLIND_2026_10_07.json"), "elapsed_seconds": 31.362, "direct_sources_supplied": 0, "whole_gate_certified": False}},
        "rebuttal_disposition": {"finding1_family_support": "SUBSTANTIVE_ACCEPTED: preserving feasible realization is a sufficient premise, not a source-derived candidate coverage fact", "finding2_original_anchor": "SUBSTANTIVE_ACCEPTED: original H nonempty does not establish that its projected H_alt satisfies the same full retained contract relation", "finding3_cross_branch": "Conditional algebra covers every branch with unchanged economic realizations, but actual joint priority/termination response remains unproved; no actual future execution certification added", "finding4_acceptance": "Actual acceptance stays null as separate A2/execution; actual consent is not a new prerequisite for a sound lawful-existence witness", "primary_authority_support_limit": "NBA4.02 supports original enforceable theta_star; NBA7.03 supports first-round retention predicate; neither supplies full-contract F5 deletion monotonicity", "canon_permission_support_limit": "CAUSALITY and T1/DEN24 directions permit testing preserved original economic terms but do not directly certify feasible relation preservation on changed F5 state", "actual_source_backed_illegal_counterexample_found": False, "new_required_private_source_or_all_hidden_clause_absence": False},
        "report": {"roadmap": "design/WORLD_BIBLE_COMPLETION_ROADMAP.md", "unfinished_major_groups": 6, "freeze": "v0.30 PARTIAL", "gates": "CLOSED", "manuscript_count": 0},
    }


def validate(data):
    if data != build():
        raise ValueError("complete preserved family, source, graph, branch or authority reconstruction differs")


def render(d):
    return """# DEN 세 자산 분기 — 보존 원권리 법적 구현 존재 제안

2026-10-07 / 고정 기준 main43e359c / [전체 증인](DEN_COMPLETE_RIGHTS_EXISTENCE_SCOPE_AUDIT_2026_10_07.json) / [검문기](../tools/build_den_complete_rights_existence_scope_audit.py).

**조건부 관계 보조정리는 유효하지만 전체 세 분기의 법적 승격은 기각했다. source_verified/complete_domain false·새 PASS0·원장 승격0·정확 금융 선택0·원고0.**

## 독립 반증 처분과 남은 정확 연결

[Claude 반증 기록](../reviews/DEN_PRESERVED_RIGHTS_CLAUDE_BLIND_2026_10_07.json)의1/2를 실질 수용한다. retained feasible relation 보존은 이 정리의 충분 전제이며, 원 공개 출처에서 도출한 후보 coverage 사실은 아니다. 원θ*의 feasible H가 존재한다는 §4.02 앵커는 H_alt가 같은 실제 계약 관계를 만족한다는 연결까지 주지 않는다. §7.03은 첫픽 제약의 국소 보존을 지지할 뿐 전체 계약의 삭제 단조성 정리는 아니다.

CAUSALITY/T1/DEN24 방향은 원경제 template를 후보로 시험할 권한을 주지만, 바뀐 F5 입력 아래 경제 의무 실현 관계의 보존을 사실 인증하지 않는다. 이 조건부 family를 그대로 source_verified 전체 PASS로 올리면 가정에 의한 S1 승격 위험이 있다. 따라서 정리는 보존하고 법적 전체 승격은 기각한다. 실제 불법 반례를 발견한 것은 아니다.

3의 전분기 대수와 실제 joint priority/termination 동작은 구분한다. 후자를 입증하는 관계 또는 법적 invariant가 남는다.4의 actual acceptance는 계속null이며 A2/실제 실행에서 분리한다. 실승낙·미래 실제전달·모든 숨은조항 부재를 새로운 S2 필수 출처로 만들지 않는다.

[NotebookLM 기록](../reviews/DEN_PRESERVED_RIGHTS_NLM_2026_10_07.json)은 import18.345초 뒤 query70.041초 PROCESS_TIMEOUT으로 분석 회수0이다. Claude31.362초의 논리 반증만 회수했으며 원자료 본문 검문·전체 G16 인증으로 계수하지 않는다. imported 이전proposal snapshot은 이 수정된 판정의 인증 자료가 아니다.

## 원 S2와 BOS에 맞춘 범위

S2는 source-supported 공개 보존 가족의 전체 분기 증인을 허용한다. BOS와 같은 March25 이름권리 양도의 법적 구현 존재를 검문하며, DEN의 prior1R 전달/2R전환·후행 보호/종료 세 범주는 모두 그대로 둔다. 실제 미래 전달·미공표 모든 계약 전역·실제 수락/접수는 인증하지 않는다. 원역사의 실제 미래 순번이나 결과를 복사하지 않는다.

기존 범위 감사에서 남겨 둔 일반 비단조 포트폴리오 함수는 **실제 source-backed 계약 반례가 아니다**. 이를 모든 공개 보존 가족의 필수 구성원으로 무한 추가하거나 모든 숨은조항의 부재를 요구할 원 S2 권위는 없다. 동일 미래 출력·unchanged demand는 특정 증명의 충분 조건이며 전역 private-state 인증을 뜻하는 추가 게이트가 아니다.

## 보존 가족과 실제 후보 구성

원θ*는 공식 완료된 Nov2020 DEN→OKC P와 March2021 DEN→ORL G의 완전한 경제 권리 객체다. NBA §4.02의 완료 절차는 그 원조건의 긍정 앵커이며 임의 보도호환θ를 합법으로 정의하는 전제가 아니다. 실제 값은 공개되지 않아도 같은 원조건·우선권·전환/해결·보호/말단 **경제 의무 관계**를 보존하는 후보 가족을 사용할 수 있다.

이 가족은 단순 AST 복사보다 강하다. 모든 retained original claim의 feasible realization 자체를 보존하고, F5의 두 조건부 outgoing claim만 제거한다. freed resource는 새 청구에 쓰지 않는다. 이 **후보 구현 가족의 조건**은 실제 모든 private 상태가 그렇게 작동한다는 사실 인증이나 새 수치조건의 작가 잠금이 아니다. 이 범위의 정당성은 부모 독립 검문에서 별도로 확인한다.

Nov2020 원 P는 F5 이전에 이미 완료된 긍정 앵커다. DEN24와 T1의 rookie payload만 Hampton→Nnaji이며 다른 원 픽경제를 고르지 않는다. McGee는 CLE, Hartenstein은 DEN에 남는다. 선수·등록·matching·비용은 기존 통과 증인과 연결하며 이를 이번 새 계산으로 계수하지 않는다.

## 전 분기 상징 증인

임의 허용 미래 입력r와 원가족의 feasible realization H(θ,r)를 둔다. 모든 P/G·다른 기존 의무의 실현과 우선권을 그대로 운반하고 F5 allocation만 제거한 H_alt를 구성한다. 각 dated resource u에서 D_ret≥0, D_F5≥0, D_ret+D_F5≤C였으므로 D_ret≤C이다. F5 보호/종료로 원 allocation이0이면0을 제거한다. CLE나 DEN의 underlying future pickowner를 무조건 확정하지 않는다.

first-round retention projection은 변하지 않는다. P가1R을 전달하든2R로 전환하든 원 complete relation을 보존하며, G가전달/rollover/보호/종료하든 같은 방식으로 기존 경제 의무 실현을 운반한다. 따라서 이 **선언된 보존 가족**의 모든 살아있는 분기에서 후보 구현이 존재한다. 이전48달력이나81자원 샘플을 전체 증명으로 반복하지 않았다.

양화는 원본 feasible realization에 대한 일반 투영 정리이며 실제 source-anchoredθ*에 적용한다. 임의 보고호환θ가 모두 합법이라는 주장도, 실제 미래 사건이 원역사와 같다는 주장도 아니다. 이 proof의 family 조건을 넘어선 실제 새 권리/후속 지출은 자동 통과되지 않는다. 특히 CLE가 받지 않은 F5 권리를 나중에 새로 쓰는 거래는 보존하지 않으며 후손 입력이 나오면 재개방한다.

## 출처와 검문 경계

새 공식 guide4는 원권리와 거래를 긍정 확인하며 정확 P/G 조건 전문을 회수한 것으로 쓰지 않는다. 원 NBA 완료 본문·규약·기존 직접 출처를 raw 지문으로 연결한다. 보호/전환 수치·G 개시 연도·실제θ/q/수락·미래 전달은null이다. 실제 F5-dependent조항 또는 실제θ*의 위법 반례를 찾은 것은 아니다.

출처 있는 retained obligation이 이 후보 realization을 깨는 F5 의존을 보이면 해당 가족을 재개방한다. 지금 그런 조항의 무존재를 전역 인증하지 않고도 **동일 S2 공개 보존 구현 가족**의 제안을 검문할 수 있다. 현재 family/support 근거 부족 지적을 수용하여 세 branch 전체 승격을 기각했다. 이 조건을 지원하는 새 관계/법적 invariant 없이 원장을 승격하지 않는다. A2/K/시즌·2021 정확 계약·원고 게이트는 별도다.

## 현행 7행 진행표

[로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md) / 미완료 큰묶음6 / v0.30 PARTIAL / 설계·원고CLOSED / 원고0.

| 번호 | 큰묶음 | 현행 범위 |
|---|---|---|
| 1 | 2020 드래프트 연쇄 | 완료·기존 승인 보존 |
| 2 | Chicago 2020–21 | 정규1080/2160+L2 6/12+playoff88 작업 모델 완료. 법적11PASS/1HOLD·F4/5·A0/3·K0/4; DEN세분기는 조건부 보조정리만 수용·전체승격 기각/HOLD·시즌false |
| 3 | 2021–23 거래·계약 | 승인 M1/G1A 방향 보존·정확 계약/시즌 실행 미완료 |
| 4 | 장기 커리어 | 17시즌 골격·행동/비용 후보 보존·중요 결과/후손 미완료 |
| 5 | 결말·전체 구조 | 14막/42소막/780배분·E1최종기능1/slot1·A01잔여35/전체미배정779 |
| 6 | 집필 규격·Context Pack | G11표본문체 규격 완료·최종기능1·설계샘플2/실제Pack0·전체 미완료 |
| 7 | 통합·독립·작가 승인 | G15/G16/G17 전체 미완료·조건부 논리 검문과 전체법적 승격기각을 구분 |
"""


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--check",action="store_true");parser.add_argument("--self-test",action="store_true");args=parser.parse_args()
    d=build();validate(d);body=json.dumps(d,ensure_ascii=False,indent=2)+"\n";md=render(d)
    if args.check:
        if normalized(OUT)!=body or normalized(MD)!=md:
            raise ValueError("saved witness differs")
    else:
        OUT.write_text(body,encoding="utf-8",newline="\n");MD.write_text(md,encoding="utf-8",newline="\n")
    rejected=[]
    if args.self_test:
        for label in ["AST_only", "respend_freed_resource", "drop_conversion_branch", "actual_future_delivery", "unconditional_F5_owner", "new_contract_selection"]:
            x=deepcopy(d)
            if label=="AST_only":x["family"]["preserve_retained_obligation_relation_not_AST_only"]=False
            elif label=="respend_freed_resource":x["family"]["released_capacity_not_newly_spent"]=False
            elif label=="drop_conversion_branch":x["branches"]=[b for b in x["branches"] if b["id"]!="prior_1R_converts_to_2R"]
            elif label=="actual_future_delivery":x["authority"]["actual_future_delivery"]={"G":2027}
            elif label=="unconditional_F5_owner":x["family"]["underlying_future_pick_owner"]="DEN"
            else:x["family"]["new_contract_terms_selected"]=True
            try:validate(x)
            except ValueError:rejected.append(label)
            else:raise AssertionError(label)
    print(json.dumps({"status":d["status"],"branches":len(d["branches"]),"raw_sources":len(d["raw_sources"]),"negative_rejections":rejected,"new_asset_PASS":0,"actual_financial_selection":False,"manuscript_allowed":False},ensure_ascii=False))


if __name__=="__main__":main()
