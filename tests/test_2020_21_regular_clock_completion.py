"""Clock completion and five-person existence-witness controls."""

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
import sys
sys.path.insert(0, str(TOOLS))
spec = importlib.util.spec_from_file_location("regular_clock", TOOLS / "build_2020_21_regular_clock_completion.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RegularClockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "simulation/NBA_2020_21_REGULAR_CLOCK_COMPLETION.json").read_text(encoding="utf-8"))

    def test_complete_working_input(self):
        module.validate(self.data)
        self.assertEqual(self.data["summary"]["existing_source_lineup_witnesses"], 107)
        self.assertEqual(self.data["summary"]["constructed_existence_witnesses"], 2053)
        self.assertEqual(self.data["summary"]["winner_changes_from_selected_overlay"], 0)
        for path, checksum in self.data["source_sha256"].items():
            self.assertEqual(checksum, module.sha(path))

    def test_greedy_existence_witness(self):
        players = {"A": 10, "B": 8, "C": 8, "D": 8, "E": 8, "F": 8}
        witness = module.construct_witness(players, 10)
        module.check_witness(players, 10, witness)
        self.assertTrue(all(len(s["players"]) == 5 for s in witness))

    def test_overcapacity_input_rejected(self):
        with self.assertRaises(AssertionError):
            module.construct_witness({"A": 11, "B": 8, "C": 8, "D": 8, "E": 8, "F": 7}, 10)

    def test_wrong_player_stint_rejected(self):
        row = next(r for r in self.data["team_games"] if r["lineup_witness_kind"] == "CONSTRUCTED_UNIFORM_MATROID_EXISTENCE_ONLY")
        segments = copy.deepcopy(row["lineup_witness"])
        segments[0]["players"][0] = "Not on roster"
        with self.assertRaises(AssertionError):
            module.check_witness(row["player_seconds"], row["game_duration_seconds"], segments)

    def test_six_raw_sources_and_no_gate_promotion(self):
        source = json.loads((ROOT / "simulation/NBA_2020_21_SELECTED_REGULAR_OVERLAY.json").read_text(encoding="utf-8"))
        raw = {(r["event_id"], r["team"]): r for r in source["team_games"]}
        changed = [r for r in self.data["team_games"] if r["working_clock_correction"]]
        self.assertEqual(len(changed), 6)
        for row in changed:
            old = raw[row["event_id"], row["team"]]
            who = row["working_clock_correction"]["player"]
            delta = row["working_clock_correction"]["delta_seconds"]
            self.assertEqual(row["player_seconds"][who] - old["player_seconds"][who], delta)
            self.assertEqual({p: s for p, s in row["player_seconds"].items() if p != who},
                             {p: s for p, s in old["player_seconds"].items() if p != who})
        self.assertFalse(self.data["whole_health_complete"])
        self.assertFalse(self.data["season_selected"])
        self.assertFalse(self.data["manuscript_allowed"])

    def test_duplicate_team_game_rejected(self):
        altered = copy.deepcopy(self.data)
        altered["team_games"][1] = altered["team_games"][0]
        with self.assertRaises(AssertionError):
            module.validate(altered)

    def test_same_total_new_witness_cannot_redefine_source_minutes(self):
        altered = copy.deepcopy(self.data)
        row = next(r for r in altered["team_games"] if r["lineup_witness_kind"] == "CONSTRUCTED_UNIFORM_MATROID_EXISTENCE_ONLY"
                   and r["working_clock_correction"] is None)
        names = [p for p, s in row["player_seconds"].items() if 1 < s < row["game_duration_seconds"] - 1]
        self.assertGreaterEqual(len(names), 2)
        row["player_seconds"][names[0]] += 1
        row["player_seconds"][names[1]] -= 1
        row["lineup_witness"] = module.construct_witness(row["player_seconds"], row["game_duration_seconds"])
        with self.assertRaises(AssertionError):
            module.validate(altered)

    def test_invented_health_and_starter_rejected(self):
        for mutation in (lambda r: r.__setitem__("medical_certified", True),
                         lambda r: r["starters"].__setitem__(0, "invented player")):
            altered = copy.deepcopy(self.data)
            mutation(altered["team_games"][0])
            with self.assertRaises(AssertionError):
                module.validate(altered)


if __name__ == "__main__":
    unittest.main()
