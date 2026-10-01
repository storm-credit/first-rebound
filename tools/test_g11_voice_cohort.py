"""Negative controls for chapter, metric and completion boundary risks."""
from copy import deepcopy
import json
import unittest
from check_g11_voice_cohort import ROOT, COHORT, PILOT, STRUCTURAL, LEDGER, audit, metric_hash


class VoiceCohortTests(unittest.TestCase):
    def setUp(self):
        self.data, self.pilot, self.structural, self.ledger = [
            json.loads((ROOT / p).read_text(encoding='utf-8'))
            for p in (COHORT, PILOT, STRUCTURAL, LEDGER)]

    def check(self):
        return audit(self.data, self.pilot, self.structural, self.ledger)

    def rehash(self, row):
        row['metric']['canonical_sha256'] = metric_hash(row['metric'])
        for c in row['captures']:
            c['canonical_sha256'] = row['metric']['canonical_sha256']

    def test_supplied_cohort(self):
        self.assertEqual(self.check(), [])

    def test_duplicate_chapter(self):
        self.data['records'][1] = deepcopy(self.data['records'][0])
        self.assertTrue(self.check())

    def test_second_capture_disagrees(self):
        self.data['records'][0]['captures'][1]['canonical_sha256'] = '0' * 64
        self.assertTrue(self.check())

    def test_nonexistent_body_paragraph_even_after_rehash(self):
        row = self.data['records'][0]
        row['metric']['channels']['CHARACTER_SPEECH']['raw_p_indexes'][0] = 0
        self.rehash(row)
        self.assertTrue(self.check())

    def test_character_total_disagrees_even_after_rehash(self):
        row = self.data['records'][0]
        row['metric']['other_utf16_characters'] += 1
        self.rehash(row)
        self.assertTrue(self.check())

    def test_reinspection_cannot_add_new_reading(self):
        self.data['readings_added'] = 4
        self.assertTrue(self.check())

    def test_partial_component_cannot_promote_full_p3(self):
        self.data['whole_P3_final'] = True
        self.assertTrue(self.check())

    def test_checker_does_not_authenticate_semantic_paraphrase(self):
        self.data['records'][0]['semantic_observations']['central_event_paraphrase'] = 'unsupported interpretation'
        self.assertEqual(self.check(), [])


if __name__ == '__main__':
    unittest.main()
