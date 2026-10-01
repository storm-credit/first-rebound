"""Structural negative controls for the G11 ten-work synthesis."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import check_g11_ten_work_synthesis as synthesis


class TenWorkSynthesisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((synthesis.ROOT / synthesis.SOURCE).read_text(encoding='utf-8'))

    def current_sources(self):
        data = copy.deepcopy(self.record)
        data['source_hashes'] = {
            path: synthesis._normalized_sha(synthesis.ROOT / path)
            for path in synthesis.EVIDENCE_SOURCES
        }
        return data

    def defects(self, mutate):
        data = self.current_sources()
        mutate(data)
        return synthesis.validate(data)

    def test_current_source_content_links_and_ten_work_structure(self):
        self.assertEqual(synthesis.validate(self.current_sources()), [])

    def test_changed_source_fails(self):
        self.assertIn('evidence source changed: research/G11_SGRADE_COMMON_MINIMUM_2026_10_02.json',
                      self.defects(lambda d: d['source_hashes'].__setitem__(
                          'research/G11_SGRADE_COMMON_MINIMUM_2026_10_02.json', '0' * 64)))

    def test_duplicate_work_fails(self):
        self.assertIn('ten unique works match progress',
                      self.defects(lambda d: d['works'][1].__setitem__(
                          'work', d['works'][0]['work'])))

    def test_candidate_reference_needs_registered_work_and_its_artifact(self):
        self.assertIn('candidate requires two linked works',
                      self.defects(lambda d: d['common_rule_candidates'][0]['evidence'][0]
                          .__setitem__('work', '없는 작품')))

    def test_closed_gate_cannot_be_promoted(self):
        self.assertIn('false gate/scope: manuscript_allowed',
                      self.defects(lambda d: d.__setitem__('manuscript_allowed', True)))

    def test_chapter_platform_distribution_must_match_ledger(self):
        self.assertIn('110-reading/platform distribution',
                      self.defects(lambda d: d['reading_scope']
                          ['chapter_platform_distribution'].__setitem__('Munpia', 56)))

    def test_original_plan_debt_cannot_disappear(self):
        self.assertIn('original-plan access debt 15',
                      self.defects(lambda d: d['reading_scope']['original_plan_debt']
                          .__setitem__('count', 0)))

    def test_sample_gate_if_true_is_qualitative_only(self):
        self.assertIn('sample gate exceeded qualitative function scope',
                      self.defects(lambda d: (
                          d.__setitem__('sample_gate_complete', True),
                          d.__setitem__('sample_gate_scope', 'UNBOUNDED'))))
        self.assertEqual(self.defects(lambda d: (
            d.__setitem__('sample_gate_complete', True),
            d.__setitem__('sample_gate_scope', 'QUALITATIVE_FUNCTION_COMPARISON_ONLY'))), [])


if __name__ == '__main__':
    unittest.main()
