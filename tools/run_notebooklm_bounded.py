"""Run one read-only NLM query directly, with a separate process deadline.

No source import, login, account configuration, schedules, or raw RPC logging.
"""
import argparse
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import subprocess
import sys
import time
from uuid import UUID


def identifier(value):
    return str(UUID(value))


def safe_response(value):
    """Keep answer/provenance, hash source quotations instead of saving them."""
    if isinstance(value, list):
        return [safe_response(v) for v in value]
    if not isinstance(value, dict):
        return value
    result = {}
    for key, item in value.items():
        if key in {'cited_text', 'source_text', 'full_text', 'raw_response', 'raw_rpc'}:
            text = item if isinstance(item, str) else json.dumps(item, ensure_ascii=False)
            result[key + '_sha256'] = hashlib.sha256(text.encode('utf-8')).hexdigest()
            result[key + '_retained'] = False
        elif key in {'answer', 'question', 'conversation_id', 'sources_used', 'citations',
                     'references', 'source_id', 'citation_number', 'error', 'is_error', 'success'} or key.isdigit():
            result[key] = safe_response(item)
    return result


def analysis_success(result):
    response = result.get('response')
    return (result.get('status') == 'RETURNED' and result.get('exit_code') == 0
            and isinstance(response, dict) and isinstance(response.get('answer'), str)
            and bool(response['answer'].strip()) and not response.get('error')
            and not response.get('is_error') and response.get('success') is not False)


def run_process(command, process_seconds):
    started = time.monotonic()
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, encoding='utf-8', errors='replace')
    except OSError as exc:
        return {'status': 'START_FAILED', 'error_type': type(exc).__name__,
                'elapsed_seconds': round(time.monotonic() - started, 3)}
    status = 'RETURNED'
    stdout = stderr = ''
    drain_complete = True
    try:
        stdout, stderr = process.communicate(timeout=process_seconds)
    except subprocess.TimeoutExpired:
        status = 'PROCESS_TIMEOUT'
        process.kill()  # Only this directly owned process; no shared service kill.
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            drain_complete = False
            for pipe in (process.stdout, process.stderr):
                if pipe:
                    pipe.close()
    result = {'status': status, 'exit_code': process.returncode,
              'elapsed_seconds': round(time.monotonic() - started, 3),
              'process_budget_seconds': process_seconds,
              'pipe_drain_complete': drain_complete,
              'stderr_sha256': hashlib.sha256(stderr.encode('utf-8')).hexdigest(),
              'stderr_retained': False}
    if status == 'RETURNED':
        try:
            result['response'] = safe_response(json.loads(stdout))
        except ValueError:
            result['stdout_sha256'] = hashlib.sha256(stdout.encode('utf-8')).hexdigest()
            result['stdout_retained'] = False
            result['response_format'] = 'NON_JSON_NOT_ANALYSIS_SUCCESS'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--notebook-id', required=True, type=identifier)
    parser.add_argument('--source-id', action='append', required=True, type=identifier)
    parser.add_argument('--question-file', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--query-seconds', type=float, default=120)
    parser.add_argument('--process-seconds', type=float, default=150)
    args = parser.parse_args()
    if (not all(math.isfinite(v) for v in (args.query_seconds, args.process_seconds))
            or args.query_seconds <= 0 or args.process_seconds <= args.query_seconds
            or args.process_seconds > 600):
        parser.error('process budget must exceed positive query budget')
    if len(args.source_id) != 1:
        parser.error('exactly one source is required')
    question = args.question_file.read_text(encoding='utf-8').strip()
    if not question or '\0' in question:
        parser.error('question must be nonempty UTF-8 text without NUL')
    # Same installed entry point as nlm.cmd, without cmd.exe/PATH indirection.
    entry = "import sys; from notebooklm_tools.cli.main import cli_main; sys.argv[0]='nlm'; sys.exit(cli_main())"
    command = [sys.executable, '-B', '-X', 'utf8', '-c', entry, 'notebook', 'query',
               args.notebook_id, question, '--source-ids', ','.join(args.source_id),
               '--new-conversation', '--timeout', str(args.query_seconds), '--json']
    record = {'scope': 'ONE_SPECIFIED_SOURCE_QUERY_NOT_INDEPENDENT_EVIDENCE',
              'runner_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'python': sys.executable,
              'installed_cli_version': importlib.metadata.version('notebooklm-mcp-cli'),
              'notebook_id': args.notebook_id, 'source_ids': args.source_id,
              'question_sha256': hashlib.sha256(question.encode('utf-8')).hexdigest(),
              'query_budget_seconds': args.query_seconds,
              'result': run_process(command, args.process_seconds)}
    record['analysis_success'] = analysis_success(record['result'])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(record, ensure_ascii=False))
    return 0 if record['analysis_success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
