"""Complete six source clock gaps and construct conditional five-player witnesses.

Only six one-to-three-second adjustments are new author working choices. All
other player seconds and 107 existing lineup witnesses are preserved.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import date
from pathlib import Path

import build_2020_21_selected_regular_overlay as selected

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "simulation/NBA_2020_21_SELECTED_REGULAR_OVERLAY.json"
PRE = "simulation/CHICAGO_2020_21_PREDEADLINE_PAIRED_OBSERVATIONS.csv"
BPM = "simulation/CHICAGO_2020_21_BPM_MAR25_SNAPSHOT.csv"
OUT = ROOT / "simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.json"
MD = ROOT / "simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.md"
SOURCES = (SOURCE, PRE, BPM)
TOL = 1e-5


def read(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def sha(path: str) -> str:
    body = (ROOT / path).read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def same(a: float, b: float) -> bool:
    return math.isclose(a, b, abs_tol=TOL, rel_tol=0)


def check_witness(players: dict[str, int | float], duration: int, witness: list[dict]) -> None:
    assert witness and all(len(s["players"]) == len(set(s["players"])) == 5
                           and s["seconds"] > 0 for s in witness)
    assert same(sum(s["seconds"] for s in witness), duration)
    rebuilt = defaultdict(float)
    for segment in witness:
        for person in segment["players"]:
            assert person in players
            rebuilt[person] += segment["seconds"]
    for person, seconds in players.items():
        assert same(rebuilt[person], seconds), (person, rebuilt[person], seconds)


def construct_witness(players: dict[str, int | float], duration: int) -> list[dict]:
    """Decompose the uniform-matroid base polytope into five-person sets.

    The segments are an existence witness. Their order is arbitrary and must
    never be read as actual substitution or tactical chronology.
    """
    remaining = {p: float(s) for p, s in players.items()}
    clock = float(duration)
    assert len([s for s in remaining.values() if s > TOL]) >= 5
    assert same(sum(remaining.values()), 5 * clock)
    assert max(remaining.values()) <= clock + TOL
    result = []
    for _ in range(1000):
        if clock <= TOL:
            break
        ordered = sorted(remaining, key=lambda p: (-remaining[p], p))
        chosen = ordered[:5]
        assert len(chosen) == 5 and min(remaining[p] for p in chosen) > TOL
        largest_unselected = max((remaining[p] for p in ordered[5:]), default=0.0)
        step = min(clock, min(remaining[p] for p in chosen), clock - largest_unselected)
        assert step > 1e-7, (clock, chosen, step, largest_unselected)
        result.append({"players": sorted(chosen), "seconds": step})
        for person in chosen:
            remaining[person] -= step
            if abs(remaining[person]) < 1e-7:
                remaining[person] = 0.0
        clock -= step
        if abs(clock) < 1e-7:
            clock = 0.0
    assert clock <= TOL and all(abs(x) <= TOL for x in remaining.values())
    check_witness(players, duration, result)
    return result


def _actual_pre() -> dict[tuple[str, str], dict[str, int]]:
    result = defaultdict(dict)
    with (ROOT / PRE).open(encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            key = (row["date"], row["team"])
            assert row["player"] not in result[key]
            result[key][row["player"]] = int(row["seconds"])
    return result


def _ratings() -> dict[str, float]:
    rows = selected.policy.cc.read(ROOT / BPM)
    return {selected.policy.cc.paired.norm(r["nba_player"]):
            float(r["bpm"]) * int(r["archive_minutes"]) /
            (int(r["archive_minutes"]) + 1000) for r in rows}


def _band(constant: float, terms: dict, rival: float, envelope: dict) -> list[float]:
    rival_name = selected.policy.f.e.RIVAL
    # Use the same symbol and empirical stress interval as the selected overlay.
    return selected.policy.cc.band(constant + terms.get(rival_name, 0) * rival,
                                   {p: n for p, n in terms.items() if p != rival_name}, envelope)


def build() -> dict:
    source = read(SOURCE)
    # The upstream overlay must itself match its source-linked reconstruction;
    # a new hash on a silently redistributed player vector is insufficient.
    selected.validate(source)
    assert source["method"] == "BPM_MAR25_EB" and not source["raptor_mixed"]
    assert len(source["team_games"]) == 2160 and len(source["regular_season_games"]) == 1080
    assert not source["unresolved_games"] and source["overlay_team_games"] == 64
    games = deepcopy(source["regular_season_games"])
    by_game = {g["event_id"]: g for g in games}
    assert len(by_game) == 1080
    team_rows = deepcopy(source["team_games"])
    original_by_key = {(r["event_id"], r["team"]): r for r in source["team_games"]}
    assert len(original_by_key) == 2160
    expected_gaps = {("2020-12-31_WAS_CHI", "CHI"): -1,
                     ("2021-01-10_LAC_CHI", "LAC"): -1,
                     ("2021-01-15_OKC_CHI", "OKC"): 1,
                     ("2021-01-25_CHI_BOS", "BOS"): -1,
                     ("2021-03-12_CHI_MIA", "CHI"): -1,
                     ("2021-03-12_CHI_MIA", "MIA"): -3}
    actual = _actual_pre()
    ratings = _ratings()
    corrections = []
    effects = defaultdict(list)
    original_witness_count = 0
    constructed_witness_count = 0
    team_dates = defaultdict(list)
    for game in games:
        for team in (game["home"], game["away"]):
            team_dates[team].append(game["date"])
    b2b = {(team, day): i > 0 and (date.fromisoformat(day) - date.fromisoformat(days[i-1])).days == 1
           for team, dates in team_dates.items() for days in [sorted(dates)] for i, day in enumerate(days)}

    for row in team_rows:
        key = (row["event_id"], row["team"])
        gap = row["normalization_delta_seconds"]
        assert gap == expected_gaps.get(key, 0), (key, gap)
        duration = row["game_duration_seconds"]
        before = row["player_seconds"].copy()
        if gap:
            positive = [(seconds, player) for player, seconds in before.items() if seconds > 0]
            assert len(positive) >= 5
            bench = [(seconds, person) for seconds, person in positive
                     if person not in (row["starters"] or [])]
            seconds, person = min(bench or positive)
            after_seconds = seconds + gap
            assert 0 <= after_seconds <= duration
            row["player_seconds"][person] = after_seconds
            row["working_clock_correction"] = {"player": person, "delta_seconds": gap,
                "raw_player_seconds": seconds, "working_player_seconds": after_seconds,
                "raw_player_vector": before,
                "selection_rule": "MIN_POSITIVE_NONSTARTER_ELSE_MIN_POSITIVE",
                "raw_source": row["source"], "source_player_vector_preserved_in": SOURCE,
                "classification": "NEW_CONDITIONAL_AUTHOR_WORKING_CLOCK_CHOICE"}
            current = by_game[row["event_id"]]
            change = {person: gap}
            effect, unknown = selected.policy.cc.form(change, ratings, {})
            prior_actual = actual[(row["date"], row["team"])]
            before_delta = {p: before.get(p, 0) - prior_actual.get(p, 0)
                            for p in set(before) | set(prior_actual)}
            after_delta = {p: row["player_seconds"].get(p, 0) - prior_actual.get(p, 0)
                           for p in set(row["player_seconds"]) | set(prior_actual)}
            exposure_change = sum(max(0, v) for v in after_delta.values()) - sum(max(0, v) for v in before_delta.values())
            fatigue_eligible = row["team"] == "CHI" if "CHI" in (current["home"], current["away"]) else True
            penalty = (.5 * exposure_change / 2880 if b2b[(row["team"], row["date"])] and fatigue_eligible else 0.0)
            sign = 1 if row["team"] == current["home"] else -1
            item = {"event_id": row["event_id"], "date": row["date"], "team": row["team"],
                    "player": person, "delta_seconds": gap, "raw_player_seconds": seconds,
                    "working_player_seconds": after_seconds, "raw_total_seconds": row["raw_total_seconds"],
                    "required_total_seconds": row["required_total_seconds"],
                    "bpm_effect": effect, "unknown_coefficients": unknown,
                    "home_sign": sign, "actual_pre_source": PRE,
                    "b2b": b2b[(row["team"], row["date"])],
                    "positive_exposure_delta_seconds": exposure_change,
                    "fatigue_scope": "UPSTREAM_CHI_ONLY" if "CHI" in (current["home"], current["away"]) else "BOTH_TEAMS_B2B",
                    "fatigue_applied": fatigue_eligible and b2b[(row["team"], row["date"])],
                    "incremental_fatigue_penalty": penalty}
            corrections.append(item)
            effects[row["event_id"]].append(item)
        else:
            row["working_clock_correction"] = None
        assert same(sum(row["player_seconds"].values()), 5 * duration)
        assert max(row["player_seconds"].values()) <= duration + TOL
        row["modeled_available"] = sorted(p for p, n in row["player_seconds"].items() if n > 1e-7)
        row["zero_player_health"] = {p: None for p, n in row["player_seconds"].items() if n <= 1e-7}
        row["working_total_seconds"] = 5 * duration
        row["working_clock_exact"] = True
        if row.get('f5_scope_completion'):
            # A new F5 completion witness is not one of the old 107 segments.
            row["lineup_witness"] = construct_witness(row["player_seconds"], duration)
            row["lineup_witness_kind"] = "CONSTRUCTED_UNIFORM_MATROID_EXISTENCE_ONLY"
            constructed_witness_count += 1
        elif row["lineup_witness"]:
            assert not gap
            check_witness(row["player_seconds"], duration, row["lineup_witness"])
            row["lineup_witness_kind"] = "EXISTING_SOURCE_SEGMENTS_ORDER_NOT_CHRONOLOGY"
            original_witness_count += 1
        else:
            row["lineup_witness"] = construct_witness(row["player_seconds"], duration)
            row["lineup_witness_kind"] = "CONSTRUCTED_UNIFORM_MATROID_EXISTENCE_ONLY"
            constructed_witness_count += 1
        row["actual_substitution_sequence_certified"] = False
        row["tactical_roles_certified"] = False
        row["medical_certified"] = False
        row["actual_active_list_certified"] = False
    assert len(corrections) == len(expected_gaps) == 6
    assert original_witness_count == 107 and constructed_witness_count == 2053
    assert len(team_rows) == 2160

    for game in games:
        added = effects[game["event_id"]]
        constant = game["home_margin_constant"]
        terms = game["unknown_coefficients"].copy()
        for item in added:
            constant += item["home_sign"] * (item["bpm_effect"] - item["incremental_fatigue_penalty"])
            for person, coefficient in item["unknown_coefficients"].items():
                terms[person] = terms.get(person, 0) + item["home_sign"] * coefficient
        band = _band(constant, terms, source["rival_rating"], source["rating_envelope"])
        direction = "HOME" if band[0] > 0 else "AWAY" if band[1] < 0 else "UNRESOLVED"
        winner = game["home"] if direction == "HOME" else game["away"] if direction == "AWAY" else None
        assert winner is not None and winner == game["winner"], (game["event_id"], band, winner, game["winner"])
        game["home_margin_constant"] = constant
        game["unknown_coefficients"] = terms
        game["home_margin_band"] = band
        game["direction"] = direction
        game["winner"] = winner
        game["clock_correction_effects"] = added
        game["winner_recomputed_after_clock_correction"] = True
    wins = Counter(g["winner"] for g in games)
    assert len(games) == 1080 and sum(wins.values()) == 1080
    assert wins["CHI"] == 31 and wins["MIN"] == 24
    return {"status": "CONDITIONAL_1080_GAME_CLOCK_COMPLETE_WORKING_INPUT_ONLY",
            "source": SOURCE, "source_hash_method": "SHA256_UTF8_LF_NORMALIZED",
            "source_sha256": {p: sha(p) for p in SOURCES},
            "policy": source["policy"], "method": "BPM_MAR25_EB", "raptor_mixed": False,
            "team_games": team_rows, "regular_season_games": games,
            "clock_corrections": corrections,
            "summary": {"games": 1080, "team_games": 2160, "source_clock_gaps": 6,
                        "working_clock_corrections": 6, "existing_source_lineup_witnesses": original_witness_count,
                        "constructed_existence_witnesses": constructed_witness_count,
                        "wins_chicago": wins["CHI"], "wins_minnesota": wins["MIN"],
                        "winner_changes_from_selected_overlay": 0},
            "scope": "Six minimal source-clock choices plus existence witnesses; no real substitution sequence, tactical role, roster, medical, or legal certification.",
            "source_player_vectors_modified": False,
            "working_player_vectors_selected": True,
            "whole_health_complete": False, "full_roster_registration_complete": False,
            "actual_active_lists_certified": False, "medical_certified": False,
            "legal_execution_cleared": False, "season_selected": False,
            "manuscript_allowed": False}


def validate(data: dict) -> None:
    assert data["status"] == "CONDITIONAL_1080_GAME_CLOCK_COMPLETE_WORKING_INPUT_ONLY"
    assert data["source_sha256"] == {p: sha(p) for p in SOURCES}
    assert not any(data[k] for k in ("whole_health_complete", "full_roster_registration_complete",
                                      "actual_active_lists_certified", "medical_certified",
                                      "legal_execution_cleared", "season_selected", "manuscript_allowed"))
    assert len(data["regular_season_games"]) == 1080 and len(data["team_games"]) == 2160
    assert len(data["clock_corrections"]) == 6
    source = read(SOURCE)
    source_rows = {(r["event_id"], r["team"]): r for r in source["team_games"]}
    assert len(source_rows) == 2160
    games = {g["event_id"]: g for g in data["regular_season_games"]}
    assert len(games) == 1080
    keys = set()
    witness_modes = Counter()
    for row in data["team_games"]:
        key = (row["event_id"], row["team"])
        assert key not in keys and key in source_rows and row["event_id"] in games
        keys.add(key)
        game = games[row["event_id"]]
        assert row["team"] in (game["home"], game["away"]) and row["date"] == game["date"]
        raw = source_rows[key]
        assert row["starters"] == raw["starters"]
        assert row["source"] == raw["source"]
        correction = row["working_clock_correction"]
        if correction:
            assert correction["raw_player_vector"] == raw["player_seconds"]
            who = correction["player"]
            assert correction["raw_player_seconds"] == raw["player_seconds"][who]
            assert correction["delta_seconds"] == raw["normalization_delta_seconds"]
            assert row["player_seconds"][who] == correction["working_player_seconds"]
            assert {p: n for p, n in row["player_seconds"].items() if p != who} == {
                p: n for p, n in raw["player_seconds"].items() if p != who}
        else:
            assert row["player_seconds"] == raw["player_seconds"]
        if row["lineup_witness_kind"] == "EXISTING_SOURCE_SEGMENTS_ORDER_NOT_CHRONOLOGY":
            assert row["lineup_witness"] == raw["lineup_witness"]
        assert same(sum(row["player_seconds"].values()), 5 * row["game_duration_seconds"])
        assert max(row["player_seconds"].values()) <= row["game_duration_seconds"] + TOL
        assert row["modeled_available"] == sorted(p for p, n in row["player_seconds"].items() if n > 1e-7)
        assert row["zero_player_health"] == {p: None for p, n in row["player_seconds"].items() if n <= 1e-7}
        check_witness(row["player_seconds"], row["game_duration_seconds"], row["lineup_witness"])
        assert row["actual_substitution_sequence_certified"] is False
        assert row["tactical_roles_certified"] is False
        assert row["medical_certified"] is False
        assert row["actual_active_list_certified"] is False
        assert row["legal_registration_cleared"] is False
        witness_modes[row["lineup_witness_kind"]] += 1
    assert keys == {(event, team) for event, game in games.items()
                    for team in (game["home"], game["away"])}
    assert witness_modes == {"EXISTING_SOURCE_SEGMENTS_ORDER_NOT_CHRONOLOGY": 107,
                             "CONSTRUCTED_UNIFORM_MATROID_EXISTENCE_ONLY": 2053}
    assert sum(g["winner"] == "CHI" for g in data["regular_season_games"]) == 31
    assert sum(g["winner"] == "MIN" for g in data["regular_season_games"]) == 24


def validate_against_sources(data: dict, expected: dict | None = None) -> None:
    """Require full source-linked reconstruction, including all margins."""
    validate(data)
    if expected is None:
        expected = build()
    assert data == expected


def markdown(data: dict) -> str:
    s = data["summary"]
    table = "\n".join(f"|{c['date']}|{c['team']}|{c['player']}|{c['delta_seconds']:+d}|{c['bpm_effect']:+.8f}|{c['incremental_fatigue_penalty']:+.8f}|"
                      for c in data["clock_corrections"])
    return f"""# 2020–21 정규시즌 시계·5인조 작업 입력

상태: `{data['status']}`. 선택된 BPM 1,080경기와 2,160팀을 소비하여
기존 원천의 6개 초 차이만 새 작업 모델로 최소 보정했다. 원천 선수 초는
`{SOURCE}`에 그대로 남아 있으며 이 파일에는 보정 전 값·원천 주소·선택규칙을 함께 남겼다.

|날짜|팀|선택 선수|초 보정|BPM 효과|적용 피로 벌점|
|---|---|---|---:|---:|---:|
{table}

모든 팀의 합계는 경기 길이의 5배, 개인 초는 경기 길이 이하이다. 기존
{s['existing_source_lineup_witnesses']}개 5인조 구간은 원천 그대로 검증해 재사용했고,
나머지 {s['constructed_existence_witnesses']}개는 5인 동시 투입의 **수학적 존재증인**이다.
구간 배열 순서는 실제 교대 순서가 아니며 포지션·전술·감독 선택을 증명하지 않는다.
승자는 1,080경기 모두 같은 방향이며 CHI {s['wins_chicago']}승,
MIN {s['wins_minnesota']}승이다. 전체 건강·활성 명단·계약·시즌 확정·원고 게이트는 CLOSED다.

재생성: `python tools/build_2020_21_regular_clock_completion.py --write`
검증: `python tools/build_2020_21_regular_clock_completion.py --check`
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = ap.parse_args()
    data = build()
    validate(data)
    body = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    note = markdown(data)
    if args.write:
        OUT.write_text(body, encoding="utf-8", newline="\n")
        MD.write_text(note, encoding="utf-8", newline="\n")
    else:
        saved = json.loads(OUT.read_text(encoding="utf-8"))
        validate_against_sources(saved, data)
        assert OUT.read_text(encoding="utf-8") == body
        assert MD.read_text(encoding="utf-8") == note
    print(json.dumps(data["summary"], ensure_ascii=False))


if __name__ == "__main__":
    import subprocess
    import sys

    if not sys.flags.utf8_mode:
        raise SystemExit(subprocess.call([sys.executable, "-X", "utf8", __file__, *sys.argv[1:]]))
    main()
