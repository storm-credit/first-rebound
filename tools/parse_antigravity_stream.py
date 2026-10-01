"""Parse documented AG NDJSON; response recovery is not source verification."""
import hashlib
import json


def parse_stream(stdout):
    finals, tools = [], []
    malformed = 0
    for line in stdout.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError:
            malformed += 1
            continue
        if not isinstance(event, dict):
            malformed += 1
            continue
        if event.get('event') == 'result' and isinstance(event.get('result'), dict):
            body = event['result']
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
    return {'terminal_count': len(finals), 'terminal': final,
            'response_recovered': recovered, 'tool_steps': tools,
            'malformed_line_count': malformed,
            'stdout_sha256': hashlib.sha256(stdout.encode('utf-8')).hexdigest(),
            'raw_logs_retained': False, 'evidence_verification': 'NOT_AUTOMATIC'}
