"""Collect the source-preserving 2020-21 K1 working base, without overlays.

This is a join of existing evidence, not a season execution or approval.
Run with --write to refresh the JSON/Markdown and --check to verify them.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulation"
OUT = SIM / "NBA_2020_21_K1_BASE_INPUT_JOIN.json"
MD = SIM / "NBA_2020_21_K1_BASE_INPUT_JOIN.md"
sys.path.insert(0, str(ROOT / "tools"))
import build_chicago_2020_21_availability_policy as availability  # noqa: E402

SOURCES = [
    "simulation/NBA_2020_21_REGULAR_GAME_BASELINE.csv",
    "simulation/CHICAGO_2020_21_SEASON_RECOMMENDATION.json",
    "canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json",
    "simulation/CHICAGO_2020_21_BOUNDARY_PAIRED_IMPACT.json",
    "simulation/CHICAGO_2020_21_REMAINING_PAIRED_IMPACT.json",
    "simulation/NBA_2020_21_FINAL_CLOSE_PAIRED_IMPACT.json",
    "simulation/NBA_2020_21_FINAL859_MINUTES.json",
    "simulation/CHICAGO_2020_21_POSTDEADLINE_PAIRED_IMPACT.json",
    "simulation/CHICAGO_2020_21_PREDEADLINE_PAIRED_OBSERVATIONS.csv",
    "simulation/CHICAGO_2020_21_PREDEADLINE_DONOR_VECTOR.csv",
    "simulation/CHICAGO_2020_21_PREDEADLINE_MINUTE_LEDGER.csv",
    "simulation/CHICAGO_2020_21_POSTDEADLINE_CAPACITY_VECTOR.csv",
    "simulation/CHICAGO_2020_21_POSTDEADLINE_LINEUP_AUDIT.json",
    "simulation/CHICAGO_2020_21_INTEGRATED_PATHS.json",
    "simulation/CHICAGO_2020_21_CLOSE_GAME_PATHS.json",
    "simulation/NBA_2020_21_FULL_SEASON.json",
]


def _rows(name: str) -> list[dict]:
    with (SIM / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _source_hash(path: str) -> str:
    body = (ROOT / path).read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _row(event: str, date: str, team: str, players: dict[str, int | float], duration: int,
         source: dict, witness: list | None = None, starters: list[str] | None = None) -> dict:
    assert players and all(isinstance(v, (int, float)) and math.isfinite(v) and v >= 0
                           for v in players.values())
    raw = sum(players.values())
    gap = 5 * duration - raw
    assert abs(gap) <= 3.000001, (event, team, gap)
    # The lineup audit keeps tiny solver float residuals. Preserve its player
    # values exactly; only the reported team clock delta ignores <1e-6 noise.
    report_gap = int(round(gap)) if abs(gap - round(gap)) < 1e-6 else gap
    if starters is not None:
        assert len(starters) == len(set(starters)) == 5
        assert all(p in players for p in starters)
    return {
        "event_id": event, "date": date, "team": team,
        "profile": "LOW_MINUTES", "player_seconds": dict(sorted(players.items())),
        "game_duration_seconds": duration, "source": source,
        "raw_total_seconds": raw, "required_total_seconds": 5 * duration,
        "normalization_delta_seconds": report_gap, "normalization_applied": False,
        "solver_float_residual_seconds": gap - report_gap,
        "clock_status": "EXACT" if report_gap == 0 else "SOURCE_ROUNDING_GAP_UNAPPLIED",
        "starters": starters, "lineup_witness": witness,
    }


def build() -> dict:
    schedule, _actual, branches, _paired, origins = availability.load()
    rec = json.loads((SIM / "CHICAGO_2020_21_SEASON_RECOMMENDATION.json").read_text(encoding="utf-8"))
    primary = [c for c in rec["season_candidates"] if c["role"] == "PRIMARY_RECOMMENDATION"]
    assert len(primary) == 1
    primary = primary[0]
    assert (primary["policy"], primary["profile"], primary["method"], primary["availability"],
            primary["base_case_id"], primary["rival_minutes"], primary["fatigue"]) == (
                "J1_TERRY_LEAVE", "LOW_MINUTES", "BPM_MAR25_EB", "PORTER_ZERO", "F038", 28, 0.5)
    assert len(schedule) == len(primary["regular_season_games"]) == 1080
    winners = {}
    for item in primary["regular_season_games"]:
        event = item["event_id"]
        assert event in schedule and event not in winners
        assert item["winner"] in (schedule[event]["home"], schedule[event]["away"])
        winners[event] = item["winner"]
    assert set(winners) == set(schedule)
    full = json.loads((SIM / "NBA_2020_21_FULL_SEASON.json").read_text(encoding="utf-8"))
    f038 = [c for c in full["league_cases"] if c["id"] == "F038"]
    assert len(f038) == 1 and 114 in f038[0]["bridge_indices"]
    bridge = full["season_bridge"][114]
    condition = bridge["source_condition"]
    assert {k: condition[k] for k in ("path_id", "availability", "method", "prior", "fatigue")} == {
        "path_id": "LOW_MINUTES/RIVAL_28/FOURNIER_PATH_RETAINED", "availability": "PORTER_ZERO",
        "method": "BPM_MAR25_EB", "prior": "BASE", "fatigue": 0.5}
    assert (bridge["shared_rival_rating_open_interval"][0] < primary["rival_effective_rating"] <
            bridge["shared_rival_rating_open_interval"][1])
    assert bridge["team_wins"] == f038[0]["team_wins"] == primary["team_wins"]

    team_rows: dict[tuple[str, str], dict] = {}
    for (event, team, profile), branch in branches.items():
        if profile != "LOW_MINUTES":
            continue
        assert event in schedule and team in (schedule[event]["home"], schedule[event]["away"])
        key = (event, team)
        assert key not in team_rows
        origin = origins[(event, team, profile)]
        seconds = {p: int(v) for p, v in branch["alternate_seconds"].items()}
        assert all(v == seconds[p] for p, v in branch["alternate_seconds"].items())
        team_rows[key] = _row(event, schedule[event]["date"], team, seconds,
                              int(branch["game_duration_seconds"]),
                              {"path": "simulation/" + origin["artifact"],
                               "pointer": f"LOW_MINUTES branch event_id={event};team={team}",
                               "stage": origin["stage"], "source_profile": origin.get("source_profile", profile)},
                              None, branch["starters"])
    assert len(team_rows) == 2045

    integrated = json.loads((SIM / "CHICAGO_2020_21_INTEGRATED_PATHS.json").read_text(encoding="utf-8"))
    path = [p for p in integrated["season_paths"]
            if p["path_id"] == "LOW_MINUTES/RIVAL_28/FOURNIER_PATH_RETAINED"]
    assert len(path) == 1 and len(path[0]["games"]) == 72
    selected_pre = {g["date"]: g for g in path[0]["games"] if g["phase"] == "PRE"}
    assert len(selected_pre) == 43
    selected_branches = {}
    assert len(integrated["remaining_pre_branches"]) == len(integrated["lineup_witnesses"])
    for i, branch in enumerate(integrated["remaining_pre_branches"]):
        key = (branch["date"], branch["opponent"], branch["profile"])
        assert key not in selected_branches
        selected_branches[key] = (i, branch, integrated["lineup_witnesses"][i])
    close = json.loads((SIM / "CHICAGO_2020_21_CLOSE_GAME_PATHS.json").read_text(encoding="utf-8"))
    selected_close = {}
    assert len(close["branches"]) == len(close["lineup_witnesses"])
    for i, branch in enumerate(close["branches"]):
        key = (branch["date"], branch["opponent"], branch["policy"])
        assert key not in selected_close
        selected_close[key] = (i, branch, close["lineup_witnesses"][i])

    chi_by_date = {}
    for event, game in schedule.items():
        if "CHI" in (game["home"], game["away"]):
            assert game["date"] not in chi_by_date
            chi_by_date[game["date"]] = event
    assert len(chi_by_date) == 72

    pre = defaultdict(dict)
    pre_starts = defaultdict(dict)
    pre_rows = _rows("CHICAGO_2020_21_PREDEADLINE_PAIRED_OBSERVATIONS.csv")
    for row in pre_rows:
        key = (row["date"], row["team"])
        assert row["player"] not in pre[key]
        pre[key][row["player"]] = int(row["seconds"])
        pre_starts[key][row["player"]] = int(row["start"])
    donors = defaultdict(dict)
    donor_starts = defaultdict(dict)
    for row in _rows("CHICAGO_2020_21_PREDEADLINE_DONOR_VECTOR.csv"):
        assert row["player"] not in donors[row["date"]]
        donors[row["date"]][row["player"]] = int(row["delta_seconds"])
        donor_starts[row["date"]][row["player"]] = int(row["alternate_start"])
    ledger = _rows("CHICAGO_2020_21_PREDEADLINE_MINUTE_LEDGER.csv")
    assert len(ledger) == len({r["date"] for r in ledger}) == 43
    assert {d for d, _t in pre} == {r["date"] for r in ledger}
    assert set(donors) == {r["date"] for r in ledger}
    for entry in ledger:
        date = entry["date"]
        event = chi_by_date[date]
        game = schedule[event]
        assert date <= "2021-03-24"
        opponent = game["away"] if game["home"] == "CHI" else game["home"]
        assert {t for d, t in pre if d == date} == {"CHI", opponent}
        assert sum(pre[(date, "CHI")].values()) == int(entry["actual_team_seconds"])
        duration = 3180 if int(entry["actual_team_seconds"]) >= 15000 else 2880
        chi = pre[(date, "CHI")].copy()
        chi_starts = pre_starts[(date, "CHI")].copy()
        for player, delta in donors[date].items():
            assert player in chi
            chi[player] += delta
            chi_starts[player] = donor_starts[date][player]
        assert "Protagonist" not in chi and "LaMelo Ball" not in chi
        chi["Protagonist"] = int(entry["protagonist_seconds"])
        chi["LaMelo Ball"] = int(entry["lamelo_seconds"])
        chi_starts["Protagonist"] = int(entry["protagonist_start"])
        chi_starts["LaMelo Ball"] = int(entry["lamelo_start"])
        assert sum(chi.values()) == int(entry["alternate_team_seconds"])
        assert selected_pre[date]["opponent"] == opponent
        selected = selected_pre[date]["branch"]
        if selected in ("HUTCHISON_INACTIVE", "INCUMBENTS"):
            idx, opbranch, witness = selected_close[(date, opponent, selected)]
            oppath = "simulation/CHICAGO_2020_21_CLOSE_GAME_PATHS.json"
            pointer = f"branches[{idx}];policy={selected}"
        elif selected in ("LOW_MINUTES", "CORE_RETAINED", "RIVAL_28"):
            idx, opbranch, witness = selected_branches[(date, opponent, selected)]
            oppath = "simulation/CHICAGO_2020_21_INTEGRATED_PATHS.json"
            pointer = f"remaining_pre_branches[{idx}];profile={selected}"
        else:
            assert selected == "LIMITED_BASELINE", (date, selected)
            opbranch, witness, oppath, pointer = None, None, None, None
        opponent_players = (opbranch["alternate_seconds"] if opbranch else pre[(date, opponent)])
        opponent_starters = (opbranch["starters"] if opbranch else
                             [p for p, v in pre_starts[(date, opponent)].items() if v == 1])
        for team, players, starts in (("CHI", chi, [p for p, v in chi_starts.items() if v == 1]),
                                      (opponent, opponent_players, opponent_starters)):
            key = (event, team)
            assert key not in team_rows
            source = ({"path": "simulation/CHICAGO_2020_21_PREDEADLINE_PAIRED_OBSERVATIONS.csv",
                       "pointer": f"date={date};team={team}",
                       "donor_path": "simulation/CHICAGO_2020_21_PREDEADLINE_DONOR_VECTOR.csv",
                       "ledger_path": "simulation/CHICAGO_2020_21_PREDEADLINE_MINUTE_LEDGER.csv"}
                      if team == "CHI" else
                      {"path": oppath or "simulation/CHICAGO_2020_21_PREDEADLINE_PAIRED_OBSERVATIONS.csv",
                       "pointer": pointer or f"date={date};team={team}",
                       "selected_path": selected,
                       "selected_path_source": "simulation/CHICAGO_2020_21_INTEGRATED_PATHS.json"})
            team_rows[key] = _row(event, date, team, players, duration, source,
                                  witness if team == opponent else None, starts)

    audit = json.loads((SIM / "CHICAGO_2020_21_POSTDEADLINE_LINEUP_AUDIT.json").read_text(encoding="utf-8"))
    post = {g["date"]: g for g in audit["games"] if g["scenario"] == "PORTER_ZERO"}
    assert len(post) == 29
    for date, candidate in post.items():
        assert date >= "2021-03-27"
        event = chi_by_date[date]
        key = (event, "CHI")
        assert key not in team_rows
        chosen = candidate["minimum_change_candidate"]
        idx = audit["games"].index(candidate)
        team_rows[key] = _row(event, date, "CHI", chosen["player_seconds"], 2880,
                              {"path": "simulation/CHICAGO_2020_21_POSTDEADLINE_LINEUP_AUDIT.json",
                               "pointer": f"games[{idx}].minimum_change_candidate;scenario=PORTER_ZERO",
                               "capacity_vector_source": "simulation/CHICAGO_2020_21_POSTDEADLINE_CAPACITY_VECTOR.csv"},
                              chosen["segments"], candidate["candidate_starters"])

    assert len(team_rows) == 2160
    assert set(team_rows) == {(event, team) for event, g in schedule.items()
                              for team in (g["home"], g["away"])}
    gaps = Counter(str(r["normalization_delta_seconds"]) for r in team_rows.values())
    wins = Counter(winners.values())
    assert sum(wins.values()) == 1080 and wins["CHI"] == 31 and wins["MIN"] == 24
    games = [{"event_id": e, "date": g["date"], "home": g["home"], "away": g["away"],
              "winner": winners[e],
              "source": {"path": "simulation/CHICAGO_2020_21_SEASON_RECOMMENDATION.json",
                         "pointer": f"season_candidates[role=PRIMARY_RECOMMENDATION].regular_season_games[event_id={e}]"}}
             for e, g in sorted(schedule.items())]
    return {
        "stage": "NBA_2020_21_K1_BASE_INPUT_JOIN",
        "status": "COMPLETE_BASE_JOIN_NOT_APPROVED_OVERLAY_FINAL",
        "scope": "SOURCE_PRESERVING_REGULAR_SEASON_WORKING_INPUT_ONLY",
        "policy": {"route": "K1_BPM_F038_WITH_APPROVED_F4_F5_C2_OVERRIDES",
                   "base_case_id": "F038", "profile": "LOW_MINUTES", "availability": "PORTER_ZERO",
                   "rival_role": "R1", "rival_minutes": 28, "fatigue": 0.5,
                   "winner_method": "BPM_MAR25_EB", "base_join_overlay_applied": False},
        "winner_axis_proof": {"path": "simulation/NBA_2020_21_FULL_SEASON.json",
                              "league_case": "F038", "season_bridge_index": 114,
                              "source_condition": condition,
                              "shared_rival_rating_open_interval": bridge["shared_rival_rating_open_interval"],
                              "effective_rating": primary["rival_effective_rating"]},
        "limitations": [
            "K1 winner map is a selected working model; this join does not recompute its 1080 margins.",
            "J1 roster, Hall non-resign, McGee nontrade, and Varejao omission minutes remain in a separate pending overlay.",
            "Nonzero source clock gaps are disclosed but no player seconds are corrected in this base join.",
            "Lineup witnesses are copied only where a selected source provides segments; no new five-player stint reconstruction is claimed.",
        ],
        "team_games": [team_rows[k] for k in sorted(team_rows)],
        "regular_season_games": games,
        "summary": {"games": len(games), "team_games": len(team_rows),
                    "branch_team_games": 2045, "pre_team_games": 86, "post_chicago_team_games": 29,
                    "clock_delta_distribution": dict(sorted(gaps.items(), key=lambda kv: int(kv[0]))),
                    "wins_chicago": wins["CHI"], "wins_minnesota": wins["MIN"]},
        "source_hash_method": "SHA256_UTF8_LF_NORMALIZED",
        "source_sha256": {p: _source_hash(p) for p in SOURCES},
        "legal_execution_cleared": False, "season_selected": False,
        "whole_health_complete": False, "author_locked": False,
        "manuscript_allowed": False,
    }


def validate(data: dict) -> None:
    assert data["status"] == "COMPLETE_BASE_JOIN_NOT_APPROVED_OVERLAY_FINAL"
    assert not any(data[k] for k in ("legal_execution_cleared", "season_selected",
                                      "whole_health_complete", "author_locked", "manuscript_allowed"))
    assert data["policy"]["base_join_overlay_applied"] is False
    games = data["regular_season_games"]
    rows = data["team_games"]
    assert len(games) == 1080 and len(rows) == 2160
    by_event = {}
    for game in games:
        e = game["event_id"]
        assert e not in by_event and game["winner"] in (game["home"], game["away"])
        by_event[e] = game
    keys = set()
    for row in rows:
        key = (row["event_id"], row["team"])
        assert key not in keys and row["event_id"] in by_event
        keys.add(key)
        game = by_event[row["event_id"]]
        assert row["date"] == game["date"] and row["team"] in (game["home"], game["away"])
        assert sum(row["player_seconds"].values()) == row["raw_total_seconds"]
        assert row["required_total_seconds"] == 5 * row["game_duration_seconds"]
        assert math.isclose(row["normalization_delta_seconds"] + row["solver_float_residual_seconds"],
                            row["required_total_seconds"] - row["raw_total_seconds"], abs_tol=1e-8)
        assert row["normalization_applied"] is False
    assert keys == {(e, t) for e, g in by_event.items() for t in (g["home"], g["away"])}
    assert sum(g["winner"] == "CHI" for g in games) == 31
    assert sum(g["winner"] == "MIN" for g in games) == 24


def validate_against_sources(data: dict, expected: dict | None = None) -> None:
    """Catch same-total player swaps, starter changes, and stale source files."""
    validate(data)
    if expected is None:
        expected = build()
    assert data["source_sha256"] == expected["source_sha256"]
    assert data["winner_axis_proof"] == expected["winner_axis_proof"]
    assert data["regular_season_games"] == expected["regular_season_games"]
    assert data["team_games"] == expected["team_games"]


def markdown(data: dict) -> str:
    s = data["summary"]
    gap = ", ".join(f"{k}: {v}" for k, v in s["clock_delta_distribution"].items())
    return f"""# 2020–21 K1 정규시즌 단일 작업 입력: 원천 보존 기본 결합

상태: `{data['status']}`. 선택된 K1 / BPM F038의 승자 {s['games']}경기와
팀별 선수 출전 초 {s['team_games']}행을 공식 일정 event ID로 연결했다.
원천 구성: 기존 LOW_MINUTES 분기 {s['branch_team_games']}행,
시카고 트레이드 전 관측·도너 {s['pre_team_games']}행,
트레이드 후 PORTER_ZERO 시카고 {s['post_chicago_team_games']}행.

시계 차이(`필요 초 - 원천 합계`) 분포: {gap}. 0이 아닌 행의 선수별 초는
수정하지 않았다. 각 행에 원천 파일·선택자와 적용하지 않은 차이를 기록했다.
선택된 전반 상대팀 분기는 INTEGRATED_PATHS / CLOSE_GAME_PATHS의 선수 초와 기존 5인 조합
증인을 사용했다. 후반 시카고는 POSTDEADLINE_LINEUP_AUDIT의 최소 변경 선수 초,
후보 선발 5명과 구간 증인을 사용했다. 증인이 없는 행의 `lineup_witness`는 null이며
새 5인 조합을 생성하지 않았다. 감사 산출물의 1e-8초 수준 부동소수 잔차는
`solver_float_residual_seconds`로 따로 보존한다.

승자표는 K1 추천 원본을 그대로 참조하며 NBA_2020_21_FULL_SEASON의
F038 `season_bridge[114]` 조건 및 평점 구간과 교차 확인했다. CHI {s['wins_chicago']}승,
MIN {s['wins_minnesota']}승. J1, F4, F5, C2의 승인된 예외를 분 단위로
적용하고 겹치는 경기의 승패를 재계산하는 일은 이 기본 결합에 포함되지 않는다.
따라서 시즌 실행, 법률·계약, 건강 전체 및 원고 게이트는 열리지 않았다.

재생성: `python tools/collect_2020_21_single_policy_base_inputs.py --write`
검증: `python tools/collect_2020_21_single_policy_base_inputs.py --check`
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = ap.parse_args()
    data = build()
    validate(data)
    j = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    m = markdown(data)
    if args.write:
        OUT.write_text(j, encoding="utf-8", newline="\n")
        MD.write_text(m, encoding="utf-8", newline="\n")
    else:
        saved = json.loads(OUT.read_text(encoding="utf-8"))
        validate_against_sources(saved)
        assert OUT.read_text(encoding="utf-8") == j
        assert MD.read_text(encoding="utf-8") == m
    print(json.dumps(data["summary"], ensure_ascii=False))


if __name__ == "__main__":
    # The existing availability loader calls read_text() without encoding.
    # Re-enter in UTF-8 mode on Windows so its Korean source notes decode.
    if not sys.flags.utf8_mode:
        import subprocess

        raise SystemExit(subprocess.call([sys.executable, "-X", "utf8", __file__, *sys.argv[1:]]))
    main()
