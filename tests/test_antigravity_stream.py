import importlib.util
import hashlib
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('parser', Path(__file__).parents[1] / 'tools/parse_antigravity_stream.py')
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)


class StreamTests(unittest.TestCase):
    def test_mixed_terminal_formats_cannot_hide_error(self):
        direct = json.dumps({'status': 'ERROR', 'response': 'failed'})
        wrapped = json.dumps({'event': 'result', 'result': {
            'status': 'SUCCESS', 'response': 'ok'}})
        for text in (direct + '\n' + wrapped, wrapped + '\n' + direct):
            value = parser.parse_stream(text)
            self.assertEqual(value['terminal_count'], 2)
            self.assertFalse(value['response_recovered'])

    def test_duplicate_keys_cannot_overwrite_failure(self):
        for text in ('{"status":"ERROR","status":"SUCCESS","response":"ok"}',
                     '{"event":"result","result":{"status":"ERROR",'
                     '"status":"SUCCESS","response":"ok"}}'):
            self.assertFalse(parser.parse_stream(text)['response_recovered'])

    def test_print_json_terminal_compact_and_multiline(self):
        payload = {'status': 'SUCCESS', 'response': 'AGY_OK',
                   'num_turns': 1, 'usage': {'private': 'private usage'}}
        for indent in (None, 2):
            value = parser.parse_stream(json.dumps(payload, indent=indent))
            self.assertTrue(value['response_recovered'])
            self.assertEqual(value['output_format'], 'json')
            self.assertEqual(value['terminal_count'], 1)
            self.assertEqual(value['terminal']['response'], 'AGY_OK')
            self.assertNotIn('private', str(value))

    def test_json_failure_empty_or_ambiguous_is_not_success(self):
        for text in ('{"status":"ERROR","response":"not success"}',
                     '{"status":"SUCCESS","response":""}',
                     '{"status":"SUCCESS","response":null}',
                     '{"status":"SUCCESS","response":{"text":"x"}}',
                     '[{"status":"SUCCESS","response":"x"}]',
                     '\n'.join(['{"status":"SUCCESS","response":"x"}'] * 2)):
            self.assertFalse(parser.parse_stream(text)['response_recovered'])

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

    def test_opt_in_partial_agent_text_is_not_terminal_recovery(self):
        text = '\n'.join(json.dumps(item) for item in [
            {'event': 'step_update', 'step_update': {
                'step_type': 'agent_response', 'state': 'ACTIVE', 'text_delta': 'Partial '}},
            {'event': 'step_update', 'step_update': {
                'step_type': 'agent_response', 'state': 'DONE', 'text_delta': 'answer'}},
            {'event': 'result', 'result': {'status': 'SUCCESS', 'response': ''}},
        ])
        basic = parser.parse_stream(text)
        self.assertNotIn('partial_agent_response', basic)
        captured = parser.parse_stream(text, safe_capture=True)
        self.assertFalse(captured['response_recovered'])
        self.assertEqual(captured['partial_agent_response']['text'], 'Partial answer')
        self.assertTrue(captured['partial_agent_response']['available'])
        self.assertFalse(captured['partial_agent_response']['terminal_response_certified'])
        self.assertFalse(captured['partial_agent_response']['source_evidence_certified'])

    def test_opt_in_tool_output_is_metadata_only_and_missing_body_stays_missing(self):
        secret = 'PRIVATE_TOOL_BODY_NOT_FOR_RECORD'
        text = '\n'.join(json.dumps(item) for item in [
            {'event': 'step_update', 'step_update': {'step_type': 'tool',
                'tool_name': 'search_web', 'state': 'DONE',
                'tool_info': {'parameters': 'PRIVATE_PARAMETERS', 'output': secret}}},
            {'event': 'step_update', 'step_update': {'step_type': 'tool',
                'tool_name': 'search_web', 'state': 'DONE', 'tool_info': {}}},
            {'event': 'result', 'result': {'status': 'SUCCESS', 'response': ''}},
        ])
        captured = parser.parse_stream(text, safe_capture=True)
        first, second = captured['tool_steps']
        self.assertEqual(first['tool_output_kind'], 'string')
        self.assertEqual(first['tool_output_char_count'], len(secret))
        self.assertEqual(first['tool_output_sha256'], hashlib.sha256(secret.encode()).hexdigest())
        self.assertFalse(second['tool_output_present'])
        self.assertNotIn(secret, str(captured))
        self.assertNotIn('PRIVATE_PARAMETERS', str(captured))
        self.assertFalse(captured['response_recovered'])

    def test_opt_in_duplicate_or_error_terminal_cannot_promote_partial(self):
        agent = json.dumps({'event': 'step_update', 'step_update': {
            'step_type': 'agent_response', 'text_delta': 'Apparently complete'}})
        success = json.dumps({'event': 'result', 'result': {
            'status': 'SUCCESS', 'response': 'final'}})
        error = json.dumps({'event': 'result', 'result': {
            'status': 'ERROR', 'response': 'error', 'error': 'PRIVATE_ERROR'}})
        for text in (agent + '\n' + success + '\n' + success,
                     agent + '\n' + error):
            value = parser.parse_stream(text, safe_capture=True)
            self.assertFalse(value['response_recovered'])
            self.assertTrue(value['partial_agent_response']['available'])
            self.assertNotIn('PRIVATE_ERROR', str(value))

    def test_opt_in_partial_is_bounded_without_changing_final_status(self):
        long_text = 'x' * 5000
        text = '\n'.join((json.dumps({'event': 'step_update', 'step_update': {
            'step_type': 'agent_response', 'text_delta': long_text}}),
            json.dumps({'event': 'result', 'result': {'status': 'SUCCESS', 'response': 'done'}})))
        value = parser.parse_stream(text, safe_capture=True)
        self.assertTrue(value['response_recovered'])
        self.assertEqual(len(value['partial_agent_response']['text']), 4096)
        self.assertEqual(value['partial_agent_response']['char_count'], 5000)
        self.assertTrue(value['partial_agent_response']['truncated'])


if __name__ == '__main__':
    unittest.main()
