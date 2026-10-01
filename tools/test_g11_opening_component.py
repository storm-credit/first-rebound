"""Negative controls for scope, cutoffs, proxies and reader-count confusion."""
import json
import unittest
from check_g11_opening_component import ROOT, DATA, STRUCTURAL, LEDGER, audit, metric_hash


class OpeningBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.data, self.structural, self.ledger = [
            json.loads((ROOT / p).read_text(encoding='utf-8'))
            for p in (DATA, STRUCTURAL, LEDGER)]

    def check(self):
        return audit(self.data, self.structural, self.ledger)

    def rehash(self, row):
        row['metric']['canonical_sha256'] = metric_hash(row['metric'])
        for c in row['captures']:
            c['canonical_sha256'] = row['metric']['canonical_sha256']

    def test_supplied_opening_records(self):
        self.assertEqual(self.check(), [])

    def test_second_capture_disagrees(self):
        self.data['records'][0]['captures'][1]['canonical_sha256'] = '0' * 64
        self.assertTrue(self.check())

    def test_partial_p_cannot_be_complete_after_rehash(self):
        row = self.data['records'][0]
        row['metric']['prefix_paragraph_intersections'][-1]['complete'] = True
        self.rehash(row)
        self.assertTrue(self.check())

    def test_proxy_is_not_linguistic_sentence_count(self):
        row = self.data['records'][0]
        row['metric']['linguistic_sentence_count'] = row['metric']['boundary_span_count']
        self.rehash(row)
        self.assertTrue(self.check())

    def test_referent_groups_are_not_distinct_person_count(self):
        self.data['records'][2]['semantic_observations']['distinct_human_count'] = 5
        self.assertTrue(self.check())

    def test_two_components_cannot_be_added_as_more_chapters(self):
        self.data['opening_component_chapters'] = 10
        self.assertTrue(self.check())

    def test_prefix_absence_is_not_later_body_match(self):
        term = next(t for t in self.data['records'][0]['selected_literal_surface_positions']
                    if t['surface'] == '게이트석')
        term['first_prefix_utf16'] = term['full_body_first_utf16']
        self.assertTrue(self.check())

    def test_first_p_code_cannot_point_to_later_p(self):
        self.data['records'][0]['semantic_observations']['first_paragraph_information_units'][0]['raw_p_index'] = 4
        self.assertTrue(self.check())


if __name__ == '__main__':
    unittest.main()
