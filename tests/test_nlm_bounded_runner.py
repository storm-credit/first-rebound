import importlib.util
from pathlib import Path
import sys
import unittest

spec = importlib.util.spec_from_file_location('runner', Path(__file__).parents[1] / 'tools/run_notebooklm_bounded.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class RunnerTests(unittest.TestCase):
    def test_empty_and_error_not_success(self):
        for response in (None, {}, [], {'error': 'failed'}, {'answer': ' '},
                         {'answer': 'x', 'success': False}):
            self.assertFalse(runner.analysis_success({'status': 'RETURNED', 'exit_code': 0, 'response': response}))

    def test_actual_child_json_answer(self):
        result = runner.run_process([sys.executable, '-c', 'print(\'{"answer":"ok"}\')'], 3)
        self.assertTrue(runner.analysis_success(result))

    def test_timeout_own_child(self):
        result = runner.run_process([sys.executable, '-c', 'import time; time.sleep(10)'], .1)
        self.assertEqual(result['status'], 'PROCESS_TIMEOUT')
        self.assertIsNotNone(result['exit_code'])
        self.assertTrue(result['pipe_drain_complete'])

    def test_quotation_and_unknown_fields(self):
        result = runner.safe_response({'answer': 'ok', 'access_token': 'secret', 'unexpected': 'secret',
                                      'references': [{'cited_text': 'quotation', 'authorization': 'secret'}]})
        self.assertNotIn('secret', str(result))
        self.assertNotIn('quotation', str(result))
        self.assertFalse(result['references'][0]['cited_text_retained'])

    def test_non_json_hash_only(self):
        result = runner.run_process([sys.executable, '-c', 'print("private-output")'], 3)
        self.assertNotIn('private-output', str(result))
        self.assertFalse(runner.analysis_success(result))


if __name__ == '__main__':
    unittest.main()
