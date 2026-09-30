import copy
import json
import unittest
import check_g11_reading_evidence as m


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data, self.measured = [json.loads((m.ROOT / p).read_text(encoding='utf-8'))
                                    for p in (m.READINGS, m.METRICS)]

    def test_existing_joara_query_identity_and_counts(self):
        result = m.audit(self.data, self.measured)
        self.assertTrue(result['PASS'], result['errors'])
        self.assertEqual(result['chapter_platform_counts']['Joara'], 5)
        self.assertEqual(result['observed']['complete_chapters'], 95)

    def test_duplicate_cannot_fill_target(self):
        self.data['readings'].append(copy.deepcopy(self.data['readings'][0]))
        self.assertIn('duplicate chapter or official viewer URL', m.audit(self.data, self.measured)['errors'])

    def test_auth_metadata_cannot_count_as_reading(self):
        self.data['readings'][0]['scope'] = 'AUTH_REQUIRED'
        self.assertIn('incomplete or unsupported reading evidence', m.audit(self.data, self.measured)['errors'])

    def test_ui_query_change_does_not_create_new_munpia_chapter(self):
        row = copy.deepcopy(next(r for r in self.data['readings'] if 'munpia' in r['url']))
        row['chapter'] = 900
        row['url'] = row['url'].split('?')[0] + '?viewRateType=OTHER'
        self.data['readings'].append(row)
        self.assertIn('duplicate chapter or official viewer URL', m.audit(self.data, self.measured)['errors'])

    def test_changed_second_open_cannot_pass(self):
        self.measured['measurements'][0]['second_pass']['body_sha256'] = '0' * 64
        self.assertIn('two opens do not reproduce', m.audit(self.data, self.measured)['errors'])

    def test_remeasurement_is_not_new_reading(self):
        self.measured['readings_added'] = 5
        self.assertTrue(m.audit(self.data, self.measured)['errors'])

    def test_unreviewed_work_or_out_of_scope_chapter_cannot_fill_target(self):
        self.data['readings'][0]['work'] = 'unreviewed replacement'
        self.assertFalse(m.audit(self.data, self.measured)['PASS'])
        self.setUp()
        self.data['readings'][0]['chapter'] = 21
        self.assertFalse(m.audit(self.data, self.measured)['PASS'])

    def test_ledger_cannot_open_manuscript_gate(self):
        self.data['manuscript_allowed'] = True
        self.assertFalse(m.audit(self.data, self.measured)['PASS'])

    def test_other_work_viewer_cannot_satisfy_named_work(self):
        self.data['readings'][0]['url'] = 'https://page.kakao.com/content/48787313/viewer/1234567/'
        self.assertFalse(m.audit(self.data, self.measured)['PASS'])


if __name__ == '__main__':
    unittest.main()
