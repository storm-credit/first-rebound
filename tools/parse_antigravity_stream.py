"""Parse AG json or stream-json; response recovery is not source verification."""
import hashlib
import json


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def _safe_output_metadata(tool_info):
    """Describe tool output without retaining its body or call parameters."""
    if not isinstance(tool_info, dict) or 'output' not in tool_info:
        return {'tool_output_present': False}
    output = tool_info['output']
    kind = ('null' if output is None else 'boolean' if isinstance(output, bool)
            else 'string' if isinstance(output, str) else 'object' if isinstance(output, dict)
            else 'array' if isinstance(output, list) else 'number' if isinstance(output, (int, float))
            else 'unsupported')
    if kind == 'unsupported':
        return {'tool_output_present': True, 'tool_output_kind': kind}
    encoded = (output if isinstance(output, str) else
               json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(',', ':')))
    return {'tool_output_present': True, 'tool_output_kind': kind,
            'tool_output_char_count': len(encoded),
            'tool_output_sha256': hashlib.sha256(encoded.encode('utf-8')).hexdigest()}


def parse_stream(stdout, *, safe_capture=False):
    """Parse a run. Opt-in capture keeps bounded agent prose, never tool bodies."""
    finals, tools = [], []
    malformed = 0
    agent_deltas = []
    # --output-format json returns the terminal object itself. It may be
    # pretty-printed; stream-json wraps terminals in NDJSON result events.
    try:
        document = json.loads(stdout, object_pairs_hook=unique_object)
    except ValueError:
        document = None
    standalone = (isinstance(document, dict) and 'event' not in document
                  and 'status' in document and 'response' in document)
    lines = [json.dumps(document)] if standalone else stdout.splitlines()
    output_format = 'json' if standalone else 'stream-json'
    for line in lines:
        if not line.strip():
            continue
        try:
            event = json.loads(line, object_pairs_hook=unique_object)
        except ValueError:
            malformed += 1
            continue
        if not isinstance(event, dict):
            malformed += 1
            continue
        direct_terminal = ('event' not in event and 'status' in event
                           and 'response' in event)
        if (direct_terminal or (event.get('event') == 'result'
                           and isinstance(event.get('result'), dict))):
            body = event if direct_terminal else event['result']
            finals.append({key: body[key] for key in ('conversation_id', 'status', 'response',
                                                      'duration_seconds', 'num_turns') if key in body})
        elif event.get('event') == 'step_update' and isinstance(event.get('step_update'), dict):
            step = event['step_update']
            if step.get('step_type') == 'tool':
                record = {key: step[key] for key in ('step_index', 'state', 'tool_name') if key in step}
                if safe_capture:
                    record.update(_safe_output_metadata(step.get('tool_info')))
                tools.append(record)
            elif (safe_capture and step.get('step_type') == 'agent_response'
                  and isinstance(step.get('text_delta'), str)):
                agent_deltas.append(step['text_delta'])
    final = finals[-1] if len(finals) == 1 else None
    response = final.get('response') if final else None
    recovered = bool(final and final.get('status') == 'SUCCESS'
                     and isinstance(response, str) and response.strip())
    result = {'output_format': output_format,
              'terminal_count': len(finals), 'terminal': final,
              'response_recovered': recovered, 'tool_steps': tools,
              'malformed_line_count': malformed,
              'stdout_sha256': hashlib.sha256(stdout.encode('utf-8')).hexdigest(),
              'raw_logs_retained': False, 'evidence_verification': 'NOT_AUTOMATIC'}
    if safe_capture:
        # This is partial model prose, not a terminal response or source fact.
        partial = ''.join(agent_deltas)
        limit = 4096
        result['partial_agent_response'] = {
            'text': partial[:limit], 'char_count': len(partial),
            'sha256': hashlib.sha256(partial.encode('utf-8')).hexdigest(),
            'truncated': len(partial) > limit,
            'available': bool(partial.strip()),
            'terminal_response_certified': False,
            'source_evidence_certified': False,
        }
    return result
