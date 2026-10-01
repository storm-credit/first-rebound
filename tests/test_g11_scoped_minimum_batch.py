"""Focused negative controls for five source-scoped G11 minimum records."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import check_g11_scoped_minimum_batch as scoped

KAKAO = 'research/G11_KAKAO_SCOPED_MINIMUM_2026_10_02.json'
MUNPIA = 'research/G11_MUNPIA_REMAINING_MINIMUM_2026_10_02.json'


class ScopedMinimumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kakao = json.loads((scoped.ROOT / KAKAO).read_text(encoding='utf-8'))
        cls.munpia = json.loads((scoped.ROOT / MUNPIA).read_text(encoding='utf-8'))

    def kakao_defects(self, mutate):
        changed = copy.deepcopy(self.kakao)
        mutate(changed)
        return scoped.validate(changed, KAKAO)

    def munpia_defects(self, mutate):
        changed = copy.deepcopy(self.munpia)
        mutate(changed)
        return scoped.validate(changed, MUNPIA)

    def test_kakao_current_two_work_scope(self):
        self.assertEqual(scoped.validate(copy.deepcopy(self.kakao), KAKAO), [])
        report = scoped.audit(sources=[KAKAO])
        self.assertTrue(report['PASS'], report['errors'])
        self.assertEqual(report['ready_works'], 2)
        self.assertFalse(report['whole_P3_final'])
        self.assertFalse(report['G11_final'])

    def test_all_five_unique_work_records_without_gate_promotion(self):
        self.assertEqual(scoped.validate(copy.deepcopy(self.munpia), MUNPIA), [])
        report = scoped.audit()
        self.assertTrue(report['PASS'], report['errors'])
        self.assertEqual(report['ready_works'], 5)
        self.assertEqual(len(set(report['ready_work_names'])), 5)
        self.assertFalse(report['whole_P3_final'])
        self.assertFalse(report['G11_final'])

    def test_duplicate_work_cannot_inflate_count(self):
        self.assertIn('registered work identity/duplicates', self.kakao_defects(
            lambda d: d['works'][1].__setitem__('work', d['works'][0]['work'])))

    def test_cross_work_official_url(self):
        self.assertIn('데뷔 못 하면 죽는 병 걸림: official chapter URL/work',
                      self.kakao_defects(lambda d: d['works'][0]['chapters'][0].__setitem__(
                          'official_url', d['works'][1]['chapters'][0]['official_url'])))

    def test_reused_p2_source_required(self):
        self.assertIn('나 혼자만 레벨업: Kakao P2 original source',
                      self.kakao_defects(lambda d: d['works'][1]['chapters'][0]
                          ['provenance'].__setitem__('original_p2_source', 'unverified')))

    def test_single_open_snapshot_cannot_be_canonical_1000(self):
        self.assertIn('데뷔 못 하면 죽는 병 걸림: Kakao single-open display-p scope',
                      self.kakao_defects(lambda d: d['works'][0]
                          ['fresh_opening_observation'].__setitem__(
                              'exact_author_text_first1000_verified', True)))

    def test_snapshot_number_cannot_be_publishable_metric(self):
        self.assertIn('나 혼자만 레벨업: Kakao 2LF snapshot diagnostic',
                      self.kakao_defects(lambda d: d['works'][1]
                          ['fresh_opening_observation']['display_join_diagnostic']
                          .__setitem__('publishable_metric', True)))

    def test_snapshot_last_p_number_must_match_boundary(self):
        self.assertIn('나 혼자만 레벨업: Kakao 2LF snapshot diagnostic',
                      self.kakao_defects(lambda d: d['works'][1]
                          ['manual_first1000_boundary'].__setitem__(
                              'last_p_included_text_utf16', 999)))

    def test_unmeasured_chapter_density_rejected(self):
        self.assertIn('데뷔 못 하면 죽는 병 걸림: unmeasured chapter quantity promoted',
                      self.kakao_defects(lambda d: d['works'][0]['chapters'][0]
                          ['quantitative_metrics'].__setitem__('first1000_density', 3.2)))

    def test_work_gate_promotion_rejected(self):
        self.assertIn('나 혼자만 레벨업: scope promotion: manuscript_allowed',
                      self.kakao_defects(lambda d: d['works'][1]
                          .__setitem__('manuscript_allowed', True)))

    def test_changed_source_hash_rejected(self):
        self.assertIn('source content changed', self.kakao_defects(
            lambda d: d['source_hashes'].__setitem__(scoped.LEDGER, '0' * 64)))

    def test_unregistered_batch_fails_closed(self):
        report = scoped.audit(sources=['research/not-a-registered-batch.json'])
        self.assertFalse(report['PASS'])
        self.assertEqual(report['ready_works'], 0)

    def test_munpia_historical_address_cannot_claim_current_identity(self):
        defects = self.munpia_defects(lambda d: d['works'][0]['chapters'][1]
            ['viewer_pages'].__setitem__('current_page_identity_certified', True))
        self.assertIn('아포칼립스에 집을 숨김: historical viewer address promoted', defects)

    def test_munpia_unmeasured_first1000_cannot_gain_numeric_boundary(self):
        defects = self.munpia_defects(lambda d: d['works'][0]
            ['manual_first1000_boundary'].__setitem__('first1000_exact_boundary', 1000))
        self.assertIn('아포칼립스에 집을 숨김: scoped opening uncertainty', defects)

    def test_munpia_visual_pages_do_not_make_exact_1000(self):
        defects = self.munpia_defects(lambda d: d['works'][2]
            ['manual_first1000_boundary'].__setitem__('diagnostic', {'utf16': 1000}))
        self.assertIn('닥터, 조선 가다: scoped opening uncertainty', defects)

    def test_munpia_separate_window_required(self):
        defects = self.munpia_defects(lambda d: d['works'][1]
            ['fresh_opening_observation'].__setitem__('selected_window_separately_read', False))
        self.assertIn('홈 플레이트의 빌런: fresh opening source/window', defects)

    def test_munpia_scene_cannot_claim_unmeasured_hash(self):
        defects = self.munpia_defects(lambda d: d['works'][2]
            ['minimum_scene_samples'][0].__setitem__('scene_sha256', '0' * 64))
        self.assertIn('닥터, 조선 가다: scene scope/address', defects)

    def test_munpia_scene_needs_root_targeted_address(self):
        defects = self.munpia_defects(lambda d: d['works'][0]
            ['minimum_scene_samples'][2].__setitem__('viewer_pages', None))
        self.assertIn('아포칼립스에 집을 숨김: Munpia scene conditional address/provenance', defects)


if __name__ == '__main__':
    unittest.main()
