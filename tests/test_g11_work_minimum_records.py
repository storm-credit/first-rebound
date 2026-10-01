"""Negative controls for machine checks; no original novel text is used."""
import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import check_g11_work_minimum_records as minimum
import build_g11_component_progress as progress
import check_g11_visual_minimum as visual
import check_g11_scoped_minimum_batch as scoped


class MinimumRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sg = json.loads((minimum.ROOT / minimum.RECORD_FILES[0]).read_text(encoding='utf-8'))
        cls.business = json.loads((minimum.ROOT / minimum.RECORD_FILES[1]).read_text(encoding='utf-8'))
        cls.extra = json.loads((minimum.ROOT / minimum.RECORD_FILES[2]).read_text(encoding='utf-8'))

    def defects(self, data):
        return minimum.validate(copy.deepcopy(data))

    def test_existing_three_valid(self):
        self.assertEqual(self.defects(self.sg), [])
        self.assertEqual(self.defects(self.business), [])
        self.assertEqual(self.defects(self.extra), [])

    def test_three_unique_ready(self):
        report = minimum.audit()
        self.assertTrue(report['PASS'])
        self.assertEqual(report['ready_works'], 3)
        self.assertEqual(len(report['record_sources']), 3)

    def test_fourteen_item_checklist(self):
        changed = copy.deepcopy(self.business)
        changed['minimum_comparison_fields'].pop()
        self.assertIn('14-item minimum checklist', self.defects(changed))

    def test_source_hash_changed(self):
        changed = copy.deepcopy(self.business)
        key = next(iter(changed['source_hashes']))
        changed['source_hashes'][key] = '0' * 64
        self.assertIn('source content changed', self.defects(changed))

    def test_normalization_method_absent(self):
        changed = copy.deepcopy(self.business)
        changed['source_hash_method'] = 'unspecified'
        self.assertIn('source normalization proof', self.defects(changed))

    def test_duplicate_chapter(self):
        changed = copy.deepcopy(self.business)
        changed['records'][1]['chapter'] = 1
        self.assertIn('five unique chapters', self.defects(changed))

    def test_wrong_source_body_hash(self):
        changed = copy.deepcopy(self.business)
        changed['records'][0]['body_sha256'] = '0' * 64
        self.assertIn('official identity/hash mismatch', self.defects(changed))

    def test_wrong_official_url(self):
        changed = copy.deepcopy(self.business)
        changed['records'][0]['url'] = 'https://example.com'
        self.assertIn('official identity/hash mismatch', self.defects(changed))

    def test_prefix_outside_1000(self):
        changed = copy.deepcopy(self.business)
        changed['records'][0]['prefix_intersection_metadata'][-1]['start_utf16'] = 1002
        self.assertIn('prefix offset/coverage mismatch', self.defects(changed))

    def test_extra_legacy_font_alias(self):
        changed = copy.deepcopy(self.extra)
        changed['records'][0]['prefix_intersection_metadata'][0]['raw_font_index'] += 1
        self.assertIn('prefix aliases disagree', self.defects(changed))

    def test_extra_first1000_denominator(self):
        changed = copy.deepcopy(self.extra)
        changed['records'][0]['prefix_join_utf16'] += 1
        self.assertIn('prefix denominator mismatch', self.defects(changed))

    def test_unmapped_prefix(self):
        changed = copy.deepcopy(self.sg)
        first_index = 3
        for tag in changed['records'][0]['first1000_all_display_blocks_coded']:
            tag['raw_p_indexes'] = [i for i in tag['raw_p_indexes'] if i != first_index]
        self.assertIn('unmapped prefix block', self.defects(changed))

    def test_wrong_prefix_label(self):
        changed = copy.deepcopy(self.business)
        changed['records'][0]['first1000_all_display_blocks_coded'][0]['function'] = 'CURRENT_FACT'
        self.assertIn('prefix labels invalid', self.defects(changed))

    def test_unassignable_fragment_must_be_separate(self):
        changed = copy.deepcopy(self.business)
        fragment = next(t for t in changed['records'][0]['first1000_all_display_blocks_coded'] if t['function'] == 'F')
        fragment['raw_p_indexes'] = changed['records'][0]['first1000_all_display_blocks_coded'][0]['raw_p_indexes'][:1]
        self.assertIn('unassignable fragment overlaps meaningful label', self.defects(changed))

    def test_missing_dialogue_scene(self):
        changed = copy.deepcopy(self.business)
        changed['minimum_scene_samples'] = [s for s in changed['minimum_scene_samples'] if s['kind'] != 'DIALOGUE']
        self.assertIn('three minimum scene kinds', self.defects(changed))

    def test_scene_density_arithmetic(self):
        changed = copy.deepcopy(self.business)
        scene = next(s for s in changed['minimum_scene_samples'] if 'observed_function_stages' in s)
        scene['local_proxy_stages_per_1000_utf16'] = 99
        self.assertIn('scene density proxy arithmetic', self.defects(changed))

    def test_raw_body_payload(self):
        changed = copy.deepcopy(self.business)
        changed['records'][0]['raw_body_text'] = 'unexpected body'
        self.assertIn('raw novel text payload', self.defects(changed))

    def test_false_gate(self):
        changed = copy.deepcopy(self.business)
        changed['G11_final'] = True
        self.assertIn('scope promotion: G11_final', self.defects(changed))

    def test_narrative_interpretation_is_outside_machine_scope(self):
        changed = copy.deepcopy(self.business)
        changed['records'][0]['central_event'] = '의미 감리 없이 바뀐 서사 해석'
        self.assertEqual(self.defects(changed), [])

    def test_duplicate_work(self):
        with patch.object(minimum, 'RECORD_FILES', (minimum.RECORD_FILES[0], minimum.RECORD_FILES[0])):
            report = minimum.audit()
        self.assertIn('duplicate work', report['errors'])

    def test_progress_uses_validated_unique_works(self):
        report = progress.build()
        self.assertEqual(report['common_minimum_work_records_ready'], 10)
        self.assertEqual(report['common_minimum_work_records_remaining'], 0)
        self.assertEqual(report['common_minimum_record_sources'], list(minimum.RECORD_FILES) + [v['source'] for v in visual.RECORDS.values()] + list(scoped.BATCHES))
        self.assertEqual(report['common_minimum_records_by_evidence_mode'], {
            'RETAINED_DOM_COMPONENT_RECORDS': 3, 'QUALITATIVE_VISUAL_INPUT_ONLY': 2,
            'QUALITATIVE_DOM_SCOPED_INPUT_ONLY': 2, 'QUALITATIVE_VISUAL_SCOPED_INPUT_ONLY': 3})
        self.assertEqual(report['components']['structure']['observed'], 15)
        self.assertEqual(report['components']['function']['observed'], 20)

    def test_progress_fails_closed_on_invalid_minimum(self):
        bad_audit = {'PASS': False, 'errors': ['source content changed'],
                     'ready_works': 2, 'record_sources': list(minimum.RECORD_FILES[:2])}
        with patch.object(minimum, 'audit', return_value=bad_audit):
            report = progress.build()
        self.assertEqual(report['status'], 'FAIL')
        self.assertIn('common minimum: source content changed', report['errors'])
        self.assertEqual(report['common_minimum_work_records_ready'], 0)

    def test_same_work_across_modes_does_not_increase_unique_count(self):
        duplicate = {'PASS': True, 'errors': [], 'ready_works': 1,
                     'record_sources': [minimum.RECORD_FILES[0]]}
        with patch.object(visual, 'audit', return_value=duplicate):
            report = progress.build()
        self.assertEqual(report['status'], 'FAIL')
        self.assertIn('common minimum: duplicate work across evidence modes', report['errors'])
        self.assertEqual(report['common_minimum_work_records_ready'], 0)


if __name__ == '__main__':
    unittest.main()
