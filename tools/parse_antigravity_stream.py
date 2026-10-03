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


def parse_stream(stdout):
    finals, tools = [], []
    malformed = 0
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
                tools.append({key: step[key] for key in ('step_index', 'state', 'tool_name') if key in step})
    final = finals[-1] if len(finals) == 1 else None
    response = final.get('response') if final else None
    recovered = bool(final and final.get('status') == 'SUCCESS'
                     and isinstance(response, str) and response.strip())
    return {'output_format': output_format,
            'terminal_count': len(finals), 'terminal': final,
            'response_recovered': recovered, 'tool_steps': tools,
            'malformed_line_count': malformed,
            'stdout_sha256': hashlib.sha256(stdout.encode('utf-8')).hexdigest(),
            'raw_logs_retained': False, 'evidence_verification': 'NOT_AUTOMATIC'}
