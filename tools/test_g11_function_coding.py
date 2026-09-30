"""Negative controls for recorded-evidence boundaries, not literary judgments."""
from copy import deepcopy
import json
import unittest
from check_g11_function_coding import ROOT, CODING, LEDGER, POPULARITY, VOICE, audit, audit_voice


class EvidenceBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.data, self.ledger, self.popularity = [
            json.loads((ROOT / p).read_text(encoding='utf-8')) for p in (CODING, LEDGER, POPULARITY)]

    def rejects(self, mutate):
        mutate()
        self.assertTrue(audit(self.data, self.ledger, self.popularity))

    def test_recorded_packet(self):
        self.assertEqual(audit(self.data, self.ledger, self.popularity), [])

    def test_duplicate_record(self):
        self.rejects(lambda: self.data['rows'].__setitem__(1, deepcopy(self.data['rows'][0])))

    def test_nonexistent_observation(self):
        self.rejects(lambda: self.data['rows'][0]['cells']['SC'].__setitem__('observation_indexes', [99]))

    def test_source_observation_changed(self):
        self.rejects(lambda: self.ledger['readings'][0]['observations'].__setitem__(0, 'changed'))

    def test_missing_is_not_absence(self):
        self.rejects(lambda: self.data['rows'][0]['cells']['AE'].__setitem__('status', 'ABSENT'))

    def test_p3_promotion(self):
        self.rejects(lambda: self.data.__setitem__('whole_P3_final', True))

    def test_voice_measurement_invented(self):
        self.rejects(lambda: self.data['rows'][0].__setitem__('voice_category_counts', {'speech': 0}))

    def test_counter_debt_disappeared(self):
        self.rejects(lambda: self.popularity.__setitem__('legacy_metric_definition_holds', 0))

    def test_single_work_cannot_promote_cross_work_candidate(self):
        self.rejects(lambda: self.data['cross_work_summary']['CT'].__setitem__(
            'candidate_status', 'RECORDED_CROSS_WORK_CANDIDATE'))


class VoiceMetricBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / VOICE).read_text(encoding='utf-8'))

    def test_supplied_metrics(self):
        self.assertEqual(audit_voice(self.data), [])

    def test_second_capture_disagrees(self):
        self.data['second_pass']['body_sha256'] = '0' * 64
        self.assertTrue(audit_voice(self.data))

    def test_wrong_share_denominator(self):
        for p in (self.data['first_pass'], self.data['second_pass']):
            p['channels']['CHARACTER_SPEECH']['paragraph_character_share'] = 465 / 3809
        self.assertTrue(audit_voice(self.data))

    def test_gate_promotion(self):
        self.data['whole_P3_final'] = True
        self.assertTrue(audit_voice(self.data))


if __name__ == '__main__':
    unittest.main()
