"""Compact author working chronology for all 2,160 clock-completed team games.

Preserve every clock-completed player vector and starter. The 107 pre-existing
witnesses remain source references with their original order unaltered; their
array order is NOT newly certified as chronology. No tactical/dead-ball claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path

import build_2020_21_regular_clock_completion as clock

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.json"
OUT = ROOT / "simulation/NBA_2020_21_REGULAR_WORKING_CHRONOLOGY.json"
MD = OUT.with_suffix(".md")
SELF = "tools/build_2020_21_regular_working_chronology.py"
SOURCES = (SOURCE, "tools/build_2020_21_regular_clock_completion.py", SELF)
CAP = 180.0
TOL = 1e-5


def normalized(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def sha(path: str) -> str:
    return hashlib.sha256(normalized(path).encode("utf-8")).hexdigest()


def period_ends(duration: int) -> list[int]:
    assert duration >= 2880 and (duration - 2880) % 300 == 0
    return [720, 1440, 2160, 2880] + list(range(3180, duration + 1, 300))


def make_plan(row: dict, ids: dict[str, int]) -> dict:
    """Reserve a feasible starter prefix, then order exact five-person buckets.

    Subtract t from all starters and from the game clock. t <= T - max(nonstarter
    seconds) and t <= min(starter seconds) keep every residual in [0,T-t] and
    sum = 5(T-t), so the same uniform-matroid decomposition still exists.

    For each next <=180-second bucket, minimize the change per elapsed second
    in squared deviation from the linear share of APPROVED player seconds. This is a
    deterministic editorial order, not an NBA tactical or medical prescription.
    """
    v = {p: float(n) for p, n in row["player_seconds"].items() if n > 1e-7}
    starters = row["starters"]
    duration = row["game_duration_seconds"]
    assert len(starters) == len(set(starters)) == 5 and all(v.get(p, 0) > 0 for p in starters)
    nonstarter_max = max((n for p, n in v.items() if p not in starters), default=0)
    prefix = min(CAP, min(v[p] for p in starters), duration - nonstarter_max)
    assert prefix > TOL, (row["event_id"], row["team"], prefix)
    remaining = {p: n - prefix if p in starters else n for p, n in v.items()}
    residual_duration = duration - prefix
    buckets = defaultdict(float)
    for segment in clock.construct_witness(remaining, residual_duration):
        buckets[tuple(segment["players"])] += segment["seconds"]
    assigned = {p: prefix if p in starters else 0.0 for p in v}
    elapsed = prefix
    blocks = [[prefix] + sorted(ids[p] for p in starters)]
    previous = set(starters)
    boundaries = period_ends(duration)
    while elapsed < duration - TOL:
        boundary = next(b for b in boundaries if b > elapsed + TOL)
        choices = []
        prior_error = sum((assigned[p] - v[p] * elapsed / duration) ** 2 for p in v)
        for people, budget in buckets.items():
            if budget <= TOL:
                continue
            step = min(CAP, budget, boundary - elapsed, duration - elapsed)
            target_time = elapsed + step
            team = set(people)
            error = sum((assigned[p] + (step if p in team else 0)
                         - v[p] * target_time / duration) ** 2 for p in v)
            choices.append(((error - prior_error) / step, len(previous & team), people, step))
        assert choices, (row["event_id"], row["team"], elapsed)
        _, _, people, step = min(choices)
        assert step > TOL
        for p in people:
            assigned[p] += step
        buckets[people] -= step
        elapsed += step
        if abs(elapsed - boundary) <= TOL:
            elapsed = float(boundary)
        if abs(elapsed - duration) <= TOL:
            elapsed = float(duration)
        blocks.append([elapsed] + sorted(ids[p] for p in people))
        previous = set(people)
        assert len(blocks) < 2000
    assert all(abs(n) <= TOL for n in buckets.values())
    assert all(math.isclose(assigned[p], n, abs_tol=TOL, rel_tol=0) for p, n in v.items())
    return {"source_row_index": None, "blocks": blocks}


def verify_plan(plan: dict, row: dict, names: list[str]) -> dict:
    """Validate the compact continuous timeline and reconstruct every player's total."""
    elapsed = 0.0
    totals = defaultdict(float)
    runs = defaultdict(float)
    maximum_run = 0.0
    maximum_block = 0.0
    boundaries = period_ends(row["game_duration_seconds"])
    for i, block in enumerate(plan["blocks"]):
        assert len(block) == 6 and all(type(n) is int and 0 <= n < len(names) for n in block[1:])
        assert len(set(block[1:])) == 5
        end = block[0]
        assert isinstance(end, (int, float)) and not isinstance(end, bool) and math.isfinite(end)
        step = end - elapsed
        assert TOL < step <= CAP + TOL
        assert not any(elapsed + TOL < b < end - TOL for b in boundaries)
        people = {names[n] for n in block[1:]}
        assert people <= set(row["modeled_available"])
        if i == 0:
            assert people == set(row["starters"])
        for p in row["player_seconds"]:
            if p in people:
                totals[p] += step
                runs[p] += step
                maximum_run = max(maximum_run, runs[p])
            else:
                runs[p] = 0.0
        maximum_block = max(maximum_block, step)
        elapsed = end
    assert math.isclose(elapsed, row["game_duration_seconds"], abs_tol=TOL, rel_tol=0)
    assert all(math.isclose(totals[p], n, abs_tol=TOL, rel_tol=0)
               for p, n in row["player_seconds"].items())
    assert all(any(abs(b[0] - t) <= TOL for b in plan["blocks"]) for t in boundaries)
    return {"blocks": len(plan["blocks"]), "opening_seconds": plan["blocks"][0][0],
            "max_block_seconds": maximum_block, "max_continuous_player_assignment_seconds": maximum_run,
            "max_player_total_arithmetic_residual_seconds": max(abs(totals[p] - n) for p, n in row["player_seconds"].items())}


def build(source: dict | None = None, verify_source: bool = True) -> dict:
    if source is None:
        source = json.loads(normalized(SOURCE))
    if verify_source:
        clock.validate_against_sources(source)
    rows = source["team_games"]
    names = sorted({p for row in rows for p in row["player_seconds"]})
    ids = {p: i for i, p in enumerate(names)}
    plans, preserved, stats, preserved_stats = [], [], [], []
    for index, row in enumerate(rows):
        existing = row["lineup_witness_kind"] == "EXISTING_SOURCE_SEGMENTS_ORDER_NOT_CHRONOLOGY"
        if existing:
            preserved.append(index)
        else:
            assert row["lineup_witness_kind"] == "CONSTRUCTED_UNIFORM_MATROID_EXISTENCE_ONLY"
        plan = make_plan(row, ids)
        plan["source_row_index"] = index
        plan["source_witness_preserved_separately"] = existing
        row_stats = verify_plan(plan, row, names)
        stats.append(row_stats)
        if existing:
            preserved_stats.append(row_stats)
        plans.append(plan)
    assert len(plans) == 2160 and len(preserved) == len(preserved_stats) == 107
    counts = Counter(r["game_duration_seconds"] for r in rows)
    return {
        "schema": "COMPACT_REGULAR_WORKING_CHRONOLOGY_V1",
        "status": "AUTHOR_WORKING_ORDER_2160_NOT_ACTUAL_NBA_SUBSTITUTIONS",
        "classification": "NEW_WORKING_COACH_ORDER_ON_PRESERVED_CLOCK_INPUTS_NOT_CANON_EVENT_LOCK",
        "source": SOURCE, "source_hash_convention": "SHA256_UTF8_NO_BOM_LF_NORMALIZED",
        "numeric_tolerance_seconds": TOL, "source_fractional_player_seconds_rounded": False,
        "source_sha256": {p: sha(p) for p in SOURCES},
        "compact_schema": {"row_identity": "source.team_games[source_row_index] supplies event/date/team/seconds/starters/availability",
                           "block": "[end_elapsed_game_seconds, five integer indexes into player_dictionary]; start is prior end or zero",
                           "period_clock": "four 720-second quarters then 300-second overtime periods; breaks consume no game time"},
        "policy": {"starter_prefix": "min(180,minimum starter seconds,game duration minus maximum nonstarter seconds)",
                   "residual_decomposition": "EXISTING_UNIFORM_MATROID_DECOMPOSITION",
                   "next_bucket": "MIN_CHANGE_PER_SECOND_IN_SQUARED_DEVIATION_FROM_LINEAR_MINUTE_SHARE_THEN_MIN_OVERLAP_THEN_LEXICOGRAPHIC",
                   "max_assignment_block_seconds": CAP, "split_at_all_period_boundaries": True,
                   "continuous_player_stint_cap_selected": None,
                   "block_cap_is_not_player_rest_or_workload_limit": True},
        "player_dictionary": names, "working_plans": plans,
        "preserved_existing_source_row_indexes": preserved,
        "preserved_existing_witnesses": "SOURCE_REFERENCE_EXACT_ORDER_AND_SECONDS_UNCHANGED_NEW_WORKING_ORDER_IS_SEPARATE_DERIVED_MODEL",
        "summary": {"source_games": 1080, "source_team_games": 2160,
                    "new_working_chronological_team_plans": len(plans), "preserved_existing_witnesses": len(preserved),
                    "new_working_orders_over_preserved_source_witnesses": len(preserved),
                    "new_working_orders_over_prior_unordered_constructed_witnesses": len(plans) - len(preserved),
                    "minimum_opening_seconds_over_preserved_source_witnesses": min(s["opening_seconds"] for s in preserved_stats),
                    "blocks": sum(s["blocks"] for s in stats), "minimum_starter_opening_seconds": min(s["opening_seconds"] for s in stats),
                    "maximum_block_seconds": max(s["max_block_seconds"] for s in stats),
                    "maximum_continuous_player_assignment_seconds": max(s["max_continuous_player_assignment_seconds"] for s in stats),
                    "maximum_player_total_arithmetic_residual_seconds": max(s["max_player_total_arithmetic_residual_seconds"] for s in stats),
                    "source_duration_counts": {str(k): v for k, v in sorted(counts.items())},
                    "new_working_plans_with_exact_source_starters": len(plans),
                    "player_seconds_changed": 0, "health_states_changed": 0, "results_or_margins_changed": 0},
        "source_clock_corrections_reused_not_new": 6,
        "all_period_boundaries_covered_for_new_plans": True,
        "new_working_order_selected": True,
        "full_2160_team_working_chronology_complete": True,
        "actual_substitution_sequence_certified": False, "actual_dead_ball_or_timeout_schedule_certified": False,
        "tactical_roles_certified": False, "position_assignment_certified": False,
        "full_2160_team_coaching_complete": False, "whole_health_complete": False,
        "medical_certified": False, "actual_active_lists_certified": False,
        "legal_execution_cleared": False, "season_selected": False,
        "new_final_episode_or_context_pack": False, "manuscript_allowed": False,
        "limits": ["107 existing unordered source witnesses remain unchanged; their original first lineup need not match source starters, and their new working order is separate",
                   "180-second blocks limit representation; a player can continue across adjacent blocks or period breaks",
                   "modeled_available and zero-player unknown health inherit source without new clearance",
                   "no score, foul, timeout, possession, dead-ball, opponent-matchup or medical event is invented",
                   "source minutes and results stay unchanged; no tactical strength is fed into BPM"]}


def validate(data: dict, source: dict | None = None, expected: dict | None = None) -> None:
    if source is None:
        source = json.loads(normalized(SOURCE))
    clock.validate_against_sources(source)
    assert data["source_sha256"] == {p: sha(p) for p in SOURCES}
    for key in ("actual_substitution_sequence_certified", "actual_dead_ball_or_timeout_schedule_certified",
                "tactical_roles_certified", "position_assignment_certified", "full_2160_team_coaching_complete",
                "whole_health_complete", "medical_certified", "actual_active_lists_certified",
                "legal_execution_cleared", "season_selected", "new_final_episode_or_context_pack", "manuscript_allowed"):
        assert data[key] is False
    assert data["new_working_order_selected"] is True
    assert data["source_fractional_player_seconds_rounded"] is False
    assert data["numeric_tolerance_seconds"] == TOL
    assert data["full_2160_team_working_chronology_complete"] is True
    assert data["policy"]["continuous_player_stint_cap_selected"] is None
    assert data["policy"]["block_cap_is_not_player_rest_or_workload_limit"] is True
    rows = source["team_games"]
    assert data["player_dictionary"] == sorted({p for row in rows for p in row["player_seconds"]})
    preserved = set(data["preserved_existing_source_row_indexes"])
    assert len(preserved) == len(data["preserved_existing_source_row_indexes"]) == 107
    for i in preserved:
        assert type(i) is int and 0 <= i < len(rows)
        assert rows[i]["lineup_witness_kind"] == "EXISTING_SOURCE_SEGMENTS_ORDER_NOT_CHRONOLOGY"
    used = set()
    for plan in data["working_plans"]:
        i = plan["source_row_index"]
        assert type(i) is int and 0 <= i < len(rows) and i not in used
        assert plan["source_witness_preserved_separately"] is (i in preserved)
        used.add(i)
        verify_plan(plan, rows[i], data["player_dictionary"])
    assert used == set(range(2160))
    if expected is None:
        expected = build(source, verify_source=False)
    assert data == expected, "full source/policy reconstruction required, not only equal minute sums"


def markdown(data: dict) -> str:
    s = data["summary"]
    return f"""# 2020–21 정규시즌 작업용 교대 순서 — compact

상태 `{data['status']}`. [JSON](NBA_2020_21_REGULAR_WORKING_CHRONOLOGY.json)과
[생성·검문기](../tools/build_2020_21_regular_working_chronology.py)는 기존
[시계 입력](NBA_2020_21_REGULAR_CLOCK_COMPLETION.json)의 분·선발·건강·승패를 바꾸지 않는다.
전체 {s['new_working_chronological_team_plans']}팀의 새 순서를 작업 감독 모델로 채택했다.
기존 {s['preserved_existing_witnesses']}개 증인은 원순서·초를 그대로 참조한다. 그 배열을
실제 교대 순서로 인증하지 않았다. 이107행의 새 작업 순서는 별도로 파생한 선택이며
원증인을 수정하거나 그 순서를 자동 채택한 것이 아니다.

## 순서 정책과 가능성

선발5인으로 먼저 `t=min(180,선발 최소 초,경기 길이−비선발 최대 초)`를 배치한다.
양수 t를 뺀 뒤 개인 잔여 초는 남은 경기 길이 이하이고 합계는 그5배여서 동일5인
분해가 가능하다. 이번 {s['new_working_chronological_team_plans']}행 모두 가능하며 최소 첫 배치는
{s['minimum_starter_opening_seconds']:g}초다. 이후 원분을 선형으로 나눴을 때의 누적 편차를
늘리거나 줄이는 초당 변화가 가장 작은5인조 잔여 묶음을 먼저 고른다. 동률은 직전5인과 덜 겹치는 묶음,
이후 이름순이다. 블록은180초 이하이고4개720초 쿼터·각300초 연장 경계에서 끊는다.
각 블록 끝을 누적 경기 초로 저장해 시작부터 마지막까지 빈틈·겹침 없이 덮는다.

## 수치 검문과 한계

- 새 {s['blocks']}블록: 각5인 고유·양수분 선수만·첫5인 원선발 일치.
- 개인 초 전원 원벡터와1e-5초 허용오차 안에서 일치하고 팀합계는 경기 길이의5배다.
  관측된 최대 선수합 산술 오차는{s['maximum_player_total_arithmetic_residual_seconds']:.12g}초다.
  원벡터를 정수 반올림하지 않으며 원천6개 최소 초 보정만 재사용한다.
- 기존107행에도 같은 정책의 새 순서를 별도로 만들었고, 모두 원선발로180초 시작한다.
  원분의 소수값도 그대로 사용하며 정수 반올림이나 새 분배를 하지 않는다.
- 최대 블록 {s['maximum_block_seconds']:g}초, 관측된 최대 연속 선수 배치
  {s['maximum_continuous_player_assignment_seconds']:g}초. 연속 선수 stint 상한은 미선택이다.
  블록을 나누어도 같은 선수가 계속 뛰면 휴식으로 계산하지 않고 쿼터 휴식도 경기 초에서 빼지 않는다.
- 2,160팀 대형 JSON을 복제하지 않는다. 원행 인덱스와 공통 선수사전·누적 끝초·5인 인덱스로 연결한다.
- 이것은 작업용 시간 순서다. 실제 NBA 교대·공이 멈추는 때·타임아웃·포제션·포지션·전술 적합성·
  건강 또는 활성 등록을 인증하지 않는다. 분0의 건강 미상은 그대로이고 모델 양수 가용성도 바뀌지 않는다.
- 분과 BPM·피로·마진·승패·시즌 선택은 변경0. 전체2,160팀의 작업용 시간 순서 소범위는 완료했다.
  실제 감독 교대·전술·의료·등록·최종 시즌 완료를 뜻하지 않는다.
- 추가 포지션 정책을 새 완료 요건으로 만들지 않는다. 최종 회차·Context Pack·원고 생성0이며 게이트 CLOSED다.

출처 지문은 UTF-8 BOM 제거 및CRLF/CR→LF 정규화다. 원시 NBA 캐시 지문과 혼동하지 않는다.
파일 존재만으로 실행 권위를 승격하지 않고 upstream 시계 입력을 원천에서 재구성한 뒤 비교한다.
동일한 선수합을 가진 임의 순서도 정책 재현이 다르면 거부한다.

`python -B -X utf8 tools/build_2020_21_regular_working_chronology.py --write`

`python -B -X utf8 tools/build_2020_21_regular_working_chronology.py --check --self-test`
"""


def self_test(data: dict, source: dict) -> int:
    tests = []
    for label in ("coverage", "duplicate_player", "wrong_starter", "equal_sum_order", "medical",
                  "zero_health_promotion", "preserved_reference", "source_hash"):
        altered = deepcopy(data)
        if label == "coverage": altered["working_plans"][0]["blocks"][-1][0] += 1
        elif label == "duplicate_player": altered["working_plans"][0]["blocks"][0][2] = altered["working_plans"][0]["blocks"][0][1]
        elif label == "wrong_starter": altered["working_plans"][0]["blocks"][0], altered["working_plans"][0]["blocks"][1] = altered["working_plans"][0]["blocks"][1], altered["working_plans"][0]["blocks"][0]
        elif label == "equal_sum_order":
            b = altered["working_plans"][0]["blocks"]
            # Same end clocks and totals when equal-length blocks are reordered.
            pair = next((i, j) for i in range(1, len(b)) for j in range(i + 1, len(b))
                        if abs((b[i][0]-b[i-1][0])-(b[j][0]-b[j-1][0])) <= TOL and b[i][1:] != b[j][1:])
            i, j = pair
            b[i][1:], b[j][1:] = b[j][1:], b[i][1:]
        elif label == "medical": altered["medical_certified"] = True
        elif label == "zero_health_promotion": altered["whole_health_complete"] = True
        elif label == "preserved_reference": altered["preserved_existing_source_row_indexes"][0] = altered["working_plans"][0]["source_row_index"]
        else: altered["source_sha256"][SOURCE] = "0" * 64
        try:
            validate(altered, source, expected=data)
        except AssertionError:
            tests.append(label)
            continue
        raise AssertionError(f"invalid promotion/order accepted: {label}")
    return len(tests)


def main() -> None:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    source = json.loads(normalized(SOURCE))
    data = build(source)
    validate(data, source, expected=data)
    body = json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n"
    note = markdown(data)
    if args.write:
        OUT.write_text(body, encoding="utf-8", newline="\n")
        MD.write_text(note, encoding="utf-8", newline="\n")
    else:
        saved = json.loads(normalized(OUT.as_posix()))
        validate(saved, source, expected=data)
        assert normalized(OUT.as_posix()) == body and normalized(MD.as_posix()) == note
    tests = self_test(data, source) if args.self_test else 0
    print(json.dumps({"summary": data["summary"], "negative_tests": tests,
                      "compact_json_bytes": len(body.encode("utf-8"))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
