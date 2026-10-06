"""Structural controls for the source-preserving regular-season base join."""

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/collect_2020_21_single_policy_base_inputs.py"
spec = importlib.util.spec_from_file_location("single_policy_base", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SinglePolicyBaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "simulation/NBA_2020_21_K1_BASE_INPUT_JOIN.json").read_text(encoding="utf-8"))

    def test_valid_join_and_reproducible_sources(self):
        module.validate(self.data)
        self.assertEqual(self.data["summary"]["clock_delta_distribution"],
                         {"-3": 1, "-1": 4, "0": 2154, "1": 1})
        for path, sha in self.data["source_sha256"].items():
            self.assertEqual(sha, module._source_hash(path), path)

    def test_duplicate_team_game_rejected(self):
        altered = copy.deepcopy(self.data)
        altered["team_games"][1] = altered["team_games"][0]
        with self.assertRaises(AssertionError):
            module.validate(altered)

    def test_missing_winner_rejected(self):
        altered = copy.deepcopy(self.data)
        altered["regular_season_games"].pop()
        with self.assertRaises(AssertionError):
            module.validate(altered)

    def test_hidden_clock_adjustment_rejected(self):
        altered = copy.deepcopy(self.data)
        gap = next(r for r in altered["team_games"] if r["normalization_delta_seconds"])
        gap["normalization_applied"] = True
        with self.assertRaises(AssertionError):
            module.validate(altered)

    def test_premature_season_gate_rejected(self):
        altered = copy.deepcopy(self.data)
        altered["season_selected"] = True
        with self.assertRaises(AssertionError):
            module.validate(altered)

    def test_same_total_player_swap_rejected_by_source_comparison(self):
        altered = copy.deepcopy(self.data)
        row = next(r for r in altered["team_games"] if r["date"] == "2021-03-31" and r["team"] == "CHI")
        row["player_seconds"]["Protagonist"] += 1
        row["player_seconds"]["LaMelo Ball"] -= 1
        module.validate(altered)  # A team clock alone cannot catch this.
        with self.assertRaises(AssertionError):
            module.validate_against_sources(altered, self.data)

    def test_lineup_audit_selected_starter_and_source(self):
        row = next(r for r in self.data["team_games"] if r["date"] == "2021-03-31" and r["team"] == "CHI")
        self.assertIn("Tomas Satoransky", row["starters"])
        self.assertNotIn("Thaddeus Young", row["starters"])
        self.assertEqual(row["source"]["path"], "simulation/CHICAGO_2020_21_POSTDEADLINE_LINEUP_AUDIT.json")
        self.assertTrue(row["lineup_witness"])
        self.assertEqual(self.data["winner_axis_proof"]["season_bridge_index"], 114)


if __name__ == "__main__":
    unittest.main()
