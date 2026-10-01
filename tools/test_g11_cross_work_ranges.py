import json
import tempfile
import unittest
from pathlib import Path
from build_g11_cross_work_ranges import ROOT, SOURCES, SG_FUNCTION, SG_PILOT, SG_VOICE, BUSINESS, build


class CrossWorkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for p in SOURCES:
            target = self.root / p
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / p).read_bytes())

    def edit(self, p, fn):
        target = self.root / p
        d = json.loads(target.read_text(encoding='utf-8'))
        fn(d)
        target.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')

    def test_gate_and_deduplication(self):
        d = build(self.root)
        self.assertEqual(len({(r['work'], r['chapter']) for r in d['rows']}), 15)
        self.assertEqual(d['new_component_chapters'], 0)
        self.assertFalse(d['G11_final'])
        self.assertFalse(d['range_is_prose_target'])
        self.assertIsNone(d['total_inner_share'])
        self.assertEqual(d['semantic_comparability'], 'NOT_CALIBRATED_ACROSS_COHORTS')
        self.assertFalse(d['cross_work_difference_computed'])

    def test_separator_denominator_rejected(self):
        self.edit(BUSINESS, lambda d: d['metrics'][0].update(body_utf16=d['metrics'][0]['body_utf16']+2))
        with self.assertRaisesRegex(ValueError, 'separator'):
            build(self.root)

    def test_wrong_voice_body_rejected(self):
        self.edit(SG_PILOT, lambda d: d['first_pass'].update(body_sha256='0'*64))
        with self.assertRaisesRegex(ValueError, 'body mismatch'):
            build(self.root)

    def test_channel_overlap_rejected(self):
        self.edit(BUSINESS, lambda d: d['metrics'][0]['voice_indexes']['UI_SYSTEM'].append(9))
        with self.assertRaisesRegex(ValueError, 'overlap'):
            build(self.root)

    def test_unreported_category_not_zero_filled(self):
        self.edit(SG_PILOT, lambda d: d['first_pass']['channels'].pop('QUOTED_INNER'))
        d = build(self.root)
        self.assertNotIn('QUOTED_INNER', d['explicitly_reported_common_categories'])
        self.assertNotIn('QUOTED_INNER', d['rows'][0]['channels'])
        self.assertEqual(d['rows'][0]['category_reporting']['QUOTED_INNER'], 'NOT_REPORTED')
        self.assertEqual(d['missing_category_policy'], 'NOT_REPORTED_NOT_ZERO')

    def test_unweighted_chapter_median(self):
        d = build(self.root)
        values = sorted(r['channels']['CHARACTER_SPEECH']['share_of_container_text'] for r in d['rows'][:5])
        self.assertEqual(d['summaries'][0]['channel_share_ranges']['CHARACTER_SPEECH']['median'], values[2])

    def test_numeric_validator_does_not_certify_meaning(self):
        self.edit(SG_FUNCTION, lambda d: d['records'][0]['story_observations'].update(central_event='검증되지 않은 의미를 고쳐 넣어도 수치검사는 인증하지 않는다.'))
        d = build(self.root)
        self.assertFalse(d['independent_original_review'])
        self.assertFalse(d['whole_P3_final'])


if __name__ == '__main__':
    unittest.main()
