import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('parser', Path(__file__).parents[1] / 'tools/parse_antigravity_stream.py')
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)


class StreamTests(unittest.TestCase):
    def test_documented_event_and_nested_terminal(self):
        text = json.dumps({'event': 'result', 'result': {'status': 'SUCCESS', 'response': 'UNVERIFIED', 'unknown': 'private'}})
        value = parser.parse_stream(text)
        self.assertTrue(value['response_recovered'])
        self.assertEqual(value['terminal']['response'], 'UNVERIFIED')
        self.assertNotIn('private', str(value))
        self.assertEqual(value['evidence_verification'], 'NOT_AUTOMATIC')

    def test_no_or_empty_or_duplicate_terminal(self):
        for text in ('{}', 'null', '{"event":"result","result":{"status":"SUCCESS","response":""}}',
                     '\n'.join(['{"event":"result","result":{"status":"SUCCESS","response":"x"}}'] * 2)):
            self.assertFalse(parser.parse_stream(text)['response_recovered'])

    def test_tool_parameters_and_diagnostics_not_saved(self):
        text = 'private diagnostic\n' + json.dumps({'event': 'step_update', 'step_update': {
            'step_type': 'tool', 'tool_name': 'search_web', 'state': 'DONE',
            'tool_info': {'parameters': 'private parameter', 'output': 'private output'}}})
        value = parser.parse_stream(text)
        self.assertEqual(value['tool_steps'][0]['tool_name'], 'search_web')
        self.assertNotIn('private', str(value))
        self.assertEqual(value['malformed_line_count'], 1)


if __name__ == '__main__':
    unittest.main()
