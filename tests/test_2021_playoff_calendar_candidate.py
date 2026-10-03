import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('calendar_candidate', Path(__file__).parents[1] / 'tools/build_2021_playoff_calendar_candidate.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CalendarControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = module.build()

    def test_parent_still_playing_blocks_next_round(self):
        packet = copy.deepcopy(self.packet)
        row = next(s for s in packet['series'] if s['id'] == 'W7')
        row['games'][0]['date_candidate'] = '2021-06-19'
        with self.assertRaises(ValueError):
            module.validate(packet)

    def test_duplicate_series_cannot_disappear_from_counts(self):
        packet = copy.deepcopy(self.packet)
        packet['series'].append(copy.deepcopy(packet['series'][0]))
        with self.assertRaises(ValueError):
            module.validate(packet)

    def test_final_homecourt_must_follow_F038_record(self):
        packet = copy.deepcopy(self.packet)
        row = next(s for s in packet['series'] if s['id'] == 'F1')
        row['higher_homecourt_team_candidate'] = 'MIL'
        for g in row['games']:
            g['home_team_candidate'] = 'MIL' if g['home_team_candidate'] == 'PHX' else 'PHX'
        with self.assertRaises(ValueError):
            module.validate(packet)

    def test_stale_source_fingerprint_is_not_current_witness(self):
        packet = copy.deepcopy(self.packet)
        packet['source_sha256'][module.RESULTS] = '0' * 64
        with self.assertRaises(ValueError):
            module.validate(packet)

    def test_earlier_result_cannot_be_changed_by_calendar(self):
        packet = copy.deepcopy(self.packet)
        row = next(s for s in packet['series'] if s['id'] == 'W3')
        row['games'][0]['selected_game_winner'] = 'LAL'
        with self.assertRaises(ValueError):
            module.validate(packet)

    def test_same_series_length_does_not_allow_scoreline_drift(self):
        packet = copy.deepcopy(self.packet)
        row = next(s for s in packet['series'] if s['id'] == 'W2')
        row['winner_wins'], row['loser_wins'] = 5, 1
        with self.assertRaises(ValueError):
            module.validate(packet)

    def test_candidate_calendar_cannot_clear_health(self):
        packet = copy.deepcopy(self.packet)
        packet['series'][0]['games'][0]['health_verified'] = True
        with self.assertRaises(ValueError):
            module.validate(packet)

    def test_home_pattern_and_calendar_authority_are_checked(self):
        for field, value in (('home_team_candidate', 'IND'), ('date_selected', True)):
            packet = copy.deepcopy(self.packet)
            packet['series'][0]['games'][0][field] = value
            with self.assertRaises(ValueError):
                module.validate(packet)


if __name__ == '__main__':
    unittest.main()
