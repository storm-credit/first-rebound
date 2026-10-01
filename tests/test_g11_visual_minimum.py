"""Negative controls for visual evidence; no novel text or screenshot fixtures."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import check_g11_visual_minimum as visual


class VisualMinimumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((visual.ROOT / visual.SOURCE).read_text(encoding='utf-8'))
        cls.field_data = json.loads((visual.ROOT / visual.FIELD_SOURCE).read_text(encoding='utf-8'))

    def defects(self, mutate):
        changed = copy.deepcopy(self.data)
        mutate(changed)
        return visual.validate(changed)

    def field_defects(self, mutate):
        changed = copy.deepcopy(self.field_data)
        mutate(changed)
        return visual.validate(changed)

    def test_current_record_scope(self):
        self.assertEqual(visual.validate(copy.deepcopy(self.data)), [])
        report = visual.audit(sources=[visual.SOURCE])
        self.assertTrue(report['PASS'])
        self.assertEqual(report['ready_works'], 1)
        self.assertEqual(report['record_sources'], [visual.SOURCE])
        self.assertFalse(report['whole_P3_final'])

    def test_duplicate_chapter(self):
        self.assertIn('five unique ordered chapters', self.defects(
            lambda d: d['chapters'][1].__setitem__('serial_chapter', 1)))

    def test_wrong_book_id(self):
        self.assertIn('official chapter URL/work', self.defects(
            lambda d: d['chapters'][0].__setitem__('official_url',
                'https://www.munpia.com/novel/viewer/999999/1618519')))

    def test_wrong_main_episode_number(self):
        self.assertIn('prologue/main episode identity', self.defects(
            lambda d: d['chapters'][0].__setitem__('main_episode', 1)))

    def test_missing_body_end(self):
        self.assertIn('body start/end reading declaration', self.defects(
            lambda d: d['chapters'][0].__setitem__('body_end_observed', False)))

    def test_viewer_page_is_conditional(self):
        self.assertIn('conditional viewer address', self.defects(
            lambda d: d['chapters'][0]['viewer_pages'].__setitem__('conditional_address', False)))

    def test_scene_outside_body(self):
        self.assertIn('scene conditional page range', self.defects(
            lambda d: d['minimum_scene_samples'][0].__setitem__('viewer_pages', [1, 999])))

    def test_scene_page_cannot_be_character_count(self):
        self.assertIn('scene unmeasured quantity promoted: character_count', self.defects(
            lambda d: d['minimum_scene_samples'][0].__setitem__('character_count', 1000)))

    def test_false_dom_body_hash(self):
        self.assertIn('unmeasured DOM hash promoted: body_sha256', self.defects(
            lambda d: d['chapters'][0].__setitem__('body_sha256', '0' * 64)))

    def test_false_first1000_sha(self):
        self.assertIn('unmeasured DOM hash promoted: first1000_sha256', self.defects(
            lambda d: d['chapters'][0].__setitem__('first1000_sha256', '0' * 64)))

    def test_false_first1000_density(self):
        self.assertIn('unmeasured first1000/length/voice metric promoted', self.defects(
            lambda d: d['chapters'][0]['quantitative_metrics'].__setitem__('first1000_density', 2.5)))

    def test_reading_whole_start_is_not_exact1000(self):
        self.assertIn('exact first1000 promoted', self.defects(
            lambda d: d['manual_first1000_boundary'].__setitem__('first1000_exact_boundary', 1000)))

    def test_missing_manual_boundary_blocks_prepared(self):
        self.assertIn('manual first1000 basis/uncertainty', self.defects(
            lambda d: d['manual_first1000_boundary'].__setitem__('boundary_neighborhood', None)))

    def test_invalid_manual_page_range(self):
        self.assertIn('manual first1000 range/mode', self.defects(
            lambda d: d['manual_first1000_boundary'].__setitem__('visual_page_range', [0, 999])))

    def test_manual_diagnostic_not_publishable(self):
        self.assertIn('manual diagnostic misrepresented', self.defects(
            lambda d: d['manual_first1000_boundary']['diagnostic'].__setitem__('publishable_metric', True)))

    def test_manual_variants_not_original_text_error_bounds(self):
        self.assertIn('manual join variants misrepresented as original-text bounds', self.defects(
            lambda d: d['manual_first1000_boundary']['diagnostic'].__setitem__(
                'variants_are_original_text_error_bounds', True)))

    def test_manual_variant_arithmetic_only(self):
        self.assertIn('manual join sensitivity arithmetic', self.defects(
            lambda d: d['manual_first1000_boundary']['diagnostic']['join_sensitivity_variants'][0].__setitem__(
                'utf16_under_assumption', 999)))

    def test_prepared_scope_requires_manual_visual_mode(self):
        self.assertIn('prepared qualitative scope declaration', self.defects(
            lambda d: d.__setitem__('minimum_ready_scope', 'EXACT_DOM_CERTIFIED')))

    def test_snapshot_count_can_grow_in_later_work(self):
        self.assertEqual(self.defects(
            lambda d: d.__setitem__('minimum_work_records_ready', 5)), [])

    def test_exact_dom_metrics_cannot_be_inferred_from_pages(self):
        self.assertIn('exact DOM/prefix measurement promoted', self.defects(
            lambda d: d.__setitem__('exact_dom_metrics', {'paragraphs': 31})))

    def test_no_whole_p3_promotion(self):
        self.assertIn('forbidden promotion/retention: whole_P3_final', self.defects(
            lambda d: d.__setitem__('whole_P3_final', True)))

    def test_screenshot_upload_prohibited(self):
        self.assertIn('forbidden promotion/retention: screenshots_uploaded', self.defects(
            lambda d: d.__setitem__('screenshots_uploaded', True)))

    def test_fourteen_items(self):
        self.assertIn('14-item checklist', self.defects(
            lambda d: d['common_fourteen_fields'].pop()))

    def test_reward_status_columns(self):
        self.assertIn('reward actual/conditional/unexecuted distinction', self.defects(
            lambda d: d['chapters'][0]['reward_states'].pop('unexecuted')))

    def test_same_reward_cannot_be_actual_and_pending(self):
        def change(d):
            d['chapters'][0]['reward_states']['actual'] = ['same step']
            d['chapters'][0]['reward_states']['conditional'] = ['same step']
        self.assertIn('same reward both actual and pending', self.defects(change))

    def test_raw_payload(self):
        self.assertIn('raw novel or screenshot payload', self.defects(
            lambda d: d.__setitem__('raw_body_text', 'unexpected')))

    def test_changed_source_hash(self):
        def change(d):
            key = next(iter(d['source_hashes']))
            d['source_hashes'][key] = '0' * 64
        self.assertIn('source content changed', self.defects(change))

    def test_semantic_truth_is_outside_checker_scope(self):
        self.assertEqual(self.defects(
            lambda d: d['chapters'][0].__setitem__('central_event', '검증되지 않은 해석')), [])

    def test_all_registered_records_are_two_distinct_visual_works(self):
        self.assertEqual(visual.validate(copy.deepcopy(self.field_data)), [])
        report = visual.audit()
        self.assertTrue(report['PASS'], report['errors'])
        self.assertEqual(report['ready_works'], 2)
        self.assertEqual(set(report['ready_work_names']), {visual.WORK, visual.FIELD_WORK})
        self.assertEqual(set(report['record_sources']), {visual.SOURCE, visual.FIELD_SOURCE})
        self.assertFalse(report['whole_P3_final'])
        self.assertFalse(report['G11_final'])

    def test_field_cross_work_chapter_url_rejected(self):
        self.assertIn('official chapter URL/work', self.field_defects(
            lambda d: d['chapters'][0].__setitem__(
                'official_url', self.data['chapters'][0]['official_url'])))

    def test_field_cross_work_opening_url_rejected(self):
        self.assertIn('unmeasured opening window not separately observed', self.field_defects(
            lambda d: d['fresh_opening_observation'].__setitem__(
                'official_url', self.data['chapters'][0]['official_url'])))

    def test_field_unmeasured_number_rejected(self):
        self.assertIn('unmeasured manual quantity promoted', self.field_defects(
            lambda d: d['fresh_opening_observation'].__setitem__('character_count', 1000)))

    def test_field_false_measurement_rejected(self):
        self.assertIn('unmeasured opening window not separately observed', self.field_defects(
            lambda d: d['fresh_opening_observation'].__setitem__('window_length_measured', True)))

    def test_field_no_separate_opening_read_rejected(self):
        self.assertIn('unmeasured opening window not separately observed', self.field_defects(
            lambda d: d['fresh_opening_observation'].__setitem__(
                'selected_window_separately_read', False)))

    def test_field_missing_assumptions_rejected(self):
        self.assertIn('manual first1000 basis/uncertainty', self.field_defects(
            lambda d: d['manual_first1000_boundary'].__setitem__('assumptions', [])))

    def test_field_historical_page_cannot_be_current_certified(self):
        self.assertIn('conditional viewer address', self.field_defects(
            lambda d: d['chapters'][1]['viewer_pages'].__setitem__(
                'current_page_identity_certified', True)))

    def test_field_numeric_diagnostic_cannot_be_invented(self):
        self.assertIn('registered manual diagnostic scope', self.field_defects(
            lambda d: d['manual_first1000_boundary'].__setitem__(
                'diagnostic', {'utf16_under_assumption': 1000})))

    def test_orv_numeric_diagnostic_cannot_be_silently_removed(self):
        self.assertIn('registered manual diagnostic scope', self.defects(
            lambda d: d['manual_first1000_boundary'].__setitem__('diagnostic', None)))

    def test_unregistered_source_and_duplicate_selection_do_not_inflate(self):
        self.assertFalse(visual.audit(sources=['research/not-a-record.json'])['PASS'])
        self.assertEqual(visual.audit(sources=[visual.SOURCE, visual.SOURCE])['ready_works'], 1)


if __name__ == '__main__':
    unittest.main()
