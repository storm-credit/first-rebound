"""Negative controls for full-body coverage and scope promotion."""
import json
import unittest
from check_g11_function_sequence import ROOT, DATA, STRUCTURAL, LEDGER, audit


class FunctionSequenceTests(unittest.TestCase):
    def setUp(self):
        self.data, self.structural, self.ledger = [
            json.loads((ROOT / p).read_text(encoding='utf-8')) for p in (DATA, STRUCTURAL, LEDGER)]

    def check(self):
        return audit(self.data, self.structural, self.ledger)

    def test_supplied_partition(self):
        self.assertEqual(self.check(), [])

    def test_uncovered_first_body_p(self):
        self.data['records'][0]['macro_blocks'][0]['start_raw_p'] = 4
        self.assertTrue(self.check())

    def test_overlap_between_blocks(self):
        self.data['records'][0]['macro_blocks'][1]['start_raw_p'] = 5
        self.assertTrue(self.check())

    def test_anchor_does_not_belong_to_its_block(self):
        self.data['records'][0]['macro_blocks'][0]['anchors'][0]['raw_p_index'] = 107
        self.assertTrue(self.check())

    def test_raw_and_normalized_viewer_are_not_same(self):
        self.data['records'][0]['first_capture']['raw_viewer_utf16'] -= 66
        self.assertTrue(self.check())

    def test_current_reaction_is_not_past_reporter(self):
        win = self.data['records'][0]['story_observations']['retrospective']['memory_window']
        win['past_reporter_raw_p'].append(win['current_reaction_raw_p'][0])
        self.assertTrue(self.check())

    def test_macro_partition_is_not_full_inner_share(self):
        self.data['records'][4]['all_inner_character_share'] = 0.5
        self.assertTrue(self.check())

    def test_more_components_do_not_mean_more_chapters(self):
        self.data['function_sequence_component_chapters'] = 15
        self.assertTrue(self.check())

    def test_semantically_wrong_paraphrase_can_pass_mechanics(self):
        self.data['records'][4]['macro_blocks'][-1]['paraphrase'] = 'Unsupported recruitment-completed assertion.'
        self.assertEqual(self.check(), [])
        self.assertFalse(self.data['checker_authenticates_semantics'])


if __name__ == '__main__':
    unittest.main()
