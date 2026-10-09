"""Validate supplied current nine-act authority; write packs only with --write.

Hashes bind reviewed bytes, not human authorship or private institutional truth.
No candidate table, producer flag, or unused personal award creates a selection.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]
SCOPE = 'control/THREEPEAT_CURRENT_PACK_SCOPE_AUTHORITY.json'
HISTORY = 'canon/THREEPEAT_CURRENT_SELECTED_HISTORY_AND_EXIT_LOCK.json'
ALLOCATION = 'design/THREEPEAT_FINAL_EPISODE_ALLOCATION.json'
BLUEPRINT = 'control/THREEPEAT_CURRENT_EPISODE_BLUEPRINT_AUTHORITY.json'
OUT = 'context-packs/threepeat-actual'
UNITS = [f'M{i:02}' for i in range(1, 10)] + ['EPI']
CLAIM_STATUSES = {'CANON_FUNCTION', 'AUTHOR_MODELED_DESIGN', 'FACT', 'INFERENCE'}
CRITICAL_CHOICES = {'C01_CALENDAR': 'CALENDAR_AVAILABILITY',
                    'EARLY_REWARD_IMPLEMENTATION': 'EARLY_CAREER_REWARD'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalized(path):
    return path.read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def digest(path):
    return hashlib.sha256(normalized(path).encode('utf-8')).hexdigest()


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError(f'Non-finite JSON value: {value}')


def safe_path(root, relative, must_exist=True):
    require(isinstance(relative, str) and relative, 'Empty source path')
    rel = Path(relative)
    require(not rel.is_absolute() and not rel.drive and '..' not in rel.parts,
            f'Source path must stay inside repository: {relative}')
    path = (root / rel).resolve()
    require(path.is_relative_to(root.resolve()), f'Source path escapes repository: {relative}')
    if must_exist:
        require(path.is_file(), f'Required current input is not issued: {relative}')
    return path


def load(root, relative):
    value = json.loads(normalized(safe_path(root, relative)), object_pairs_hook=unique_pairs,
                       parse_constant=invalid_constant)
    def finite(item):
        if isinstance(item, float):
            require(math.isfinite(item), 'Non-finite JSON number')
        elif isinstance(item, dict):
            for child in item.values():
                finite(child)
        elif isinstance(item, list):
            for child in item:
                finite(child)
    finite(value)
    return value


def resolve_pointer(value, pointer):
    require(isinstance(pointer, str), 'JSON pointer must be a string')
    if pointer == '':
        return value
    require(pointer.startswith('/'), 'JSON pointer must be absolute')
    try:
        for escaped in pointer[1:].split('/'):
            require(re.search(r'~(?![01])', escaped) is None, 'Invalid JSON pointer escape')
            token = escaped.replace('~1', '/').replace('~0', '~')
            if isinstance(value, list):
                require(re.fullmatch(r'0|[1-9][0-9]*', token) is not None,
                        'Array pointer requires a nonnegative canonical integer')
                value = value[int(token)]
            else:
                require(isinstance(value, dict), 'Pointer descends through a scalar')
                value = value[token]
    except (IndexError, KeyError) as exc:
        raise ValueError(f'JSON pointer does not exist: {pointer}') from exc
    return value


def text(value, label):
    require(isinstance(value, str) and bool(value.strip()), f'Missing {label}')


def integer(value):
    return type(value) is int


def clock(value, label):
    require(type(value) is int or (type(value) is float and math.isfinite(value)),
            f'Invalid finite clock: {label}')
    return value


def strings(values, label, nonempty=True):
    require(isinstance(values, list) and (bool(values) or not nonempty), f'Invalid {label}')
    require(all(isinstance(v, str) and v.strip() for v in values), f'Invalid {label} values')
    require(len(values) == len(set(values)), f'Duplicate {label}')
    return set(values)


def gates(value):
    require(value.get('manuscript_allowed') is False and value.get('design_gate') == 'CLOSED',
            'Manuscript boundary must remain CLOSED')
    require(value.get('freeze') == 'v0.30 PARTIAL', 'Freeze changed')


def authority_payload_digest(authority):
    payload = {key: value for key, value in authority.items() if key != 'independent_review'}
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
                         allow_nan=False).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


class Sources:
    def __init__(self, root, reviewed):
        self.root = root
        self.reviewed = reviewed
        self.used = {}

    def read(self, ref):
        require(isinstance(ref, dict), 'Source reference must be an object')
        unsupported_epochs = {'source_snapshot_commit', 'source_snapshot_commits',
                              'snapshot_commit', 'source_epoch', 'epoch'}
        require(not (unsupported_epochs & set(ref)),
                'Snapshot/epoch source references are unsupported; never interpret declared history as live bytes')
        path = ref.get('path')
        actual = digest(safe_path(self.root, path))
        require(ref.get('source_sha256') == actual, f'Stale source: {path}')
        require(self.reviewed.get(path) == actual, f'Source not in exact independent review: {path}')
        pointer = ref.get('json_pointer')
        source_format = ref.get('format', 'JSON')
        if source_format == 'JSON':
            result = resolve_pointer(load(self.root, path), pointer)
        elif source_format == 'UTF8_TEXT':
            require(pointer == '', 'Text source cannot use a JSON pointer')
            body = normalized(safe_path(self.root, path))
            locator = ref.get('text_locator', {})
            if locator.get('kind') == 'WHOLE_TEXT':
                result = body
            else:
                require(locator.get('kind') == 'LINE_RANGE', 'Explicit text locator missing')
                start, end = locator.get('start_line'), locator.get('end_line')
                lines = body.splitlines()
                require(integer(start) and integer(end) and 1 <= start <= end <= len(lines),
                        'Text locator line range is invalid')
                result = '\n'.join(lines[start - 1:end])
            text(result, 'located text body')
            if 'expected_text' in locator:
                require(locator['expected_text'] == result, 'Text locator expected body mismatch')
        else:
            raise ValueError('Unsupported source format; binary evidence needs an existing typed receipt')
        self.used[path] = actual
        return result


def selected_record(record, kind=None):
    require(isinstance(record, dict), 'Selection source must resolve to an object')
    require(record.get('selected') is True and record.get('status') == 'SELECTED_FICTIONAL_USED_RESOLUTION',
            'Consequential choice is not selected in its source')
    require(record.get('authority_class') in {'AUTHOR_SELECTED', 'DELEGATED_SELECTED'},
            'Consequential choice has no supplied author/delegated authority')
    if kind:
        require(record.get('kind') == kind, f'Selection kind mismatch: {kind}')
    text(record.get('resolution'), 'selected resolution')
    require(record.get('unresolved_used_dependencies') == [], 'Selected source still has used dependencies on HOLD')
    return record


def validate_access(bp, sources, choices):
    claims = bp.get('claims')
    require(isinstance(claims, list) and claims, 'Blueprint needs typed claims')
    boundary = bp.get('information_boundary', {})
    require(boundary.get('status') == 'LOCKED_SELECTED_SCENE_ACCESS'
            and boundary.get('clock_order_verified') is True, 'Individual access is not locked')
    text(boundary.get('pov_character'), 'POV character')
    text(boundary.get('clock_basis'), 'scene/acquisition clock basis')
    segments = boundary.get('scene_segments')
    require(isinstance(segments, list) and segments, 'Actual scene segments missing')
    by_segment = {}
    known = set()
    previous = -math.inf
    for segment in segments:
        sid = segment.get('segment_id')
        text(sid, 'segment ID')
        require(sid not in by_segment, 'Duplicate scene segment')
        order = clock(segment.get('scene_order'), sid)
        require(order > previous, 'Scene clock must increase')
        previous = order
        actor = segment.get('pov_character')
        text(actor, 'segment POV')
        if actor != boundary['pov_character']:
            require(segment.get('pov_switch_approved') is True, 'POV switch not approved')
            text(segment.get('boundary_marker'), 'POV switch boundary')
        indexes = segment.get('known_claim_indexes')
        require(isinstance(indexes, list) and len(indexes) == len(set(indexes)), 'Invalid known indexes')
        require(all(integer(i) and 0 <= i < len(claims) for i in indexes), 'Known index out of range')
        by_segment[sid] = segment
        known.update(indexes)
    require(known == set(range(len(claims))), 'Orphan typed claim has no scene access')
    covered = {sid: set() for sid in by_segment}
    witnesses = boundary.get('access_witnesses')
    require(isinstance(witnesses, list) and witnesses, 'Access witnesses missing')
    for witness in witnesses:
        sid = witness.get('segment_id')
        require(sid in by_segment, 'Ghost witness has no actual scene')
        segment = by_segment[sid]
        require(witness.get('owner') == segment['pov_character'], 'Witness owner is not scene POV')
        require(clock(witness.get('scene_order'), 'witness scene') == segment['scene_order'],
                'Witness scene clock does not match segment')
        acquired = clock(witness.get('acquired_order'), 'acquisition')
        require(acquired <= segment['scene_order'], 'Knowledge acquired after scene')
        text(witness.get('access_method'), 'actual access method')
        indexes = witness.get('claim_indexes')
        require(isinstance(indexes, list) and indexes and len(indexes) == len(set(indexes)),
                'Witness indexes missing or duplicated')
        require(all(integer(i) and i in segment['known_claim_indexes'] for i in indexes),
                'Witness claims outside its actual scene access')
        kind = witness.get('knowledge_kind')
        require(kind in {'OBSERVED_EVENT', 'CURRENT_PLAN', 'EXPLICIT_INFERENCE'}, 'Invalid knowledge kind')
        if kind == 'OBSERVED_EVENT':
            require(clock(witness.get('event_order'), 'observed event') <= acquired,
                    'Observed event occurs after acquisition')
        for index in indexes:
            claim = claims[index]
            require(claim.get('temporal_kind') == kind, 'Witness/claim temporal kind mismatch')
            if kind == 'EXPLICIT_INFERENCE':
                require(claim.get('status') == 'INFERENCE', 'Inference is disguised as observed fact')
        covered[sid].update(indexes)
    for sid, segment in by_segment.items():
        require(covered[sid] == set(segment['known_claim_indexes']), 'Scene knowledge lacks a witness')
    bp_choices = strings(bp.get('consequential_choice_ids', []), 'Blueprint choices', False)
    require(bp_choices <= set(choices), 'Blueprint uses unknown consequential choice')
    for claim in claims:
        require(claim.get('status') in CLAIM_STATUSES, 'Candidate or untyped claim cannot become actual')
        text(claim.get('text'), 'typed claim text')
        refs = claim.get('source_refs')
        require(isinstance(refs, list) and refs, 'Claim source missing')
        for ref in refs:
            sources.read(ref)
        if claim['status'] == 'FACT':
            require(claim.get('temporal_kind') == 'OBSERVED_EVENT',
                    'FACT cannot be CURRENT_PLAN or inferred knowledge')
            require(claim.get('primary_source_body_verified') is True, 'FACT has no verified primary body')
        if claim['status'] == 'INFERENCE':
            require(claim.get('inference_visible') is True, 'Inference must stay visible')
        ids = strings(claim.get('requires_selected_choice_ids', []), 'Claim selected choices', False)
        require(ids <= bp_choices, 'Claim choice not declared in Blueprint')
        require(all(choices[c].get('status') == 'RESOLVED_SELECTED' for c in ids),
                'Used claim depends on an unselected choice')
        if claim.get('effect_kind') == 'PERSONAL_AWARD_MAX_SALARY':
            require(ids and any(choices[c]['selected_source']['kind'] == 'PERSONAL_AWARD' for c in ids),
                    'HigherMax award claim needs a selected personal award source')


def compile_inputs(root):
    root = Path(root).resolve()
    scope, history, allocation, authority = [load(root, p) for p in (SCOPE, HISTORY, ALLOCATION, BLUEPRINT)]
    expected = ('LOCKED_CURRENT_PACK_SCOPE', 'LOCKED_CURRENT_SELECTED_HISTORY',
                'LOCKED_CURRENT_FINAL_EPISODE_FUNCTION_TABLE', 'ACTUAL_CURRENT_BLUEPRINT_AUTHORITY')
    scope_id = scope.get('scope_id')
    text(scope_id, 'scope ID')
    producers = set()
    for value, status in zip((scope, history, allocation, authority), expected):
        require(value.get('status') == status, f'Current input is not locked: {status}')
        require(value.get('scope_id') == scope_id, 'Current scope ID mismatch')
        gates(value)
        text(value.get('producer_id'), 'input producer')
        producers.add(value['producer_id'])
    require(scope.get('active_unit_ids') == UNITS, 'Current scope must be M01–M09 plus brief EPI')
    review_ref = authority.get('independent_review', {})
    review = load(root, review_ref.get('path'))
    require(digest(safe_path(root, review_ref['path'])) == review_ref.get('source_sha256'), 'Stale independent review')
    require(review.get('status') == 'ACCEPTED_CURRENT_THREEPEAT_PACK_INPUTS'
            and review.get('independent_review_completed') is True, 'Current exact-scope acceptance missing')
    text(review.get('reviewer_id'), 'independent reviewer')
    require(review['reviewer_id'] not in producers, 'Producer cannot be independent reviewer')
    require(review.get('reviewed_authority_payload_sha256') == authority_payload_digest(authority),
            'Blueprint authority payload changed after review')
    reviewed = review.get('reviewed_artifacts_sha256')
    require(isinstance(reviewed, dict), 'Reviewed artifact pins missing')
    sources = Sources(root, reviewed)
    for path in (SCOPE, HISTORY, ALLOCATION):
        require(reviewed.get(path) == digest(safe_path(root, path)), f'Current input not independently reviewed: {path}')
    targets = sources.read(scope.get('selected_scope_ref'))
    require(scope['selected_scope_ref'].get('format', 'JSON') == 'JSON', 'Scope selection must use JSON authority')
    selected_scope_doc = load(root, scope['selected_scope_ref']['path'])
    require(selected_scope_doc.get('status') in {'DELEGATED_SELECTED_DESIGN_TARGET_REVISED_EXECUTION_PENDING',
                                               'AUTHOR_SELECTED_DESIGN_TARGET', 'DELEGATED_SELECTED_DESIGN_TARGET'},
            'Current scope must join supplied selected target authority')
    require(isinstance(targets, dict) and targets.get('Chicago_title_years') == [2023, 2024, 2025]
            and targets.get('main_story_climax_and_end_year') == 2025 and targets.get('retirement_epilogue_year') == 2035,
            'Scope target differs from current threepeat/main-end/EPI authority')
    policy = scope.get('category_policy', {})
    require(policy.get('minimum_percent') == 75 and policy.get('maximum_percent') == 85
            and policy.get('denominator') == 'ALL_FINAL_EPISODES', 'Approved NBA 75–85 policy must be preserved')
    counted = strings(policy.get('counted_categories'), 'counted NBA categories')
    require(counted in ({'NBA'}, {'NBA', 'NBA_DRAFT'}), 'Draft counting must be explicit')
    definitions = policy.get('category_definitions')
    require(isinstance(definitions, dict) and {'NBA', 'NBA_DRAFT', 'PRE_NBA', 'POST_NBA'} <= set(definitions),
            'Explicit final category definitions missing')
    for definition in definitions.values():
        text(definition, 'category definition')
    policy_source = selected_record(sources.read(policy.get('selection_source_ref')), 'EPISODE_CATEGORY_POLICY')
    require(policy_source.get('policy') == {k: v for k, v in policy.items() if k != 'selection_source_ref'},
            'Category policy differs from selected policy source')
    require(history.get('current_used_scope_complete') is True, 'Current used history is incomplete')
    port_ids = strings(scope.get('required_exit_port_ids'), 'required finite exit ports')
    ports = history.get('finite_used_exit_ports')
    require(isinstance(ports, list), 'Finite used exit ports missing')
    port_map = {}
    for port in ports:
        pid = port.get('port_id')
        require(pid in port_ids and pid not in port_map, 'Unknown or duplicate finite exit port')
        require(port.get('unit_id') in UNITS and port.get('status') == 'SELECTED_RESOLVED', 'Used exit is not resolved')
        for key in ('entry_state', 'changed_action', 'durable_cost', 'exit_state'):
            text(port.get(key), f'finite port {key}')
        refs = port.get('source_refs')
        require(isinstance(refs, list) and refs, 'Finite exit source missing')
        for ref in refs:
            sources.read(ref)
        port_map[pid] = port
    require(set(port_map) == port_ids, 'Finite used exit coverage incomplete')
    units = history.get('unit_exits')
    require(isinstance(units, list) and [u.get('unit_id') for u in units] == UNITS, 'Current unit exits incomplete')
    for index, unit in enumerate(units):
        for key in ('entry_state', 'exit_state'):
            text(unit.get(key), f'unit {key}')
        ids = strings(unit.get('port_ids'), 'unit exit port IDs')
        require(ids == {pid for pid, p in port_map.items() if p['unit_id'] == unit['unit_id']},
                'Unit exit port ownership mismatch')
        if index < len(UNITS) - 1:
            require(unit.get('next_unit_id') == UNITS[index + 1]
                    and unit.get('next_entry_state') == units[index + 1].get('entry_state'), 'Unit transition mismatch')
        else:
            require(unit.get('next_unit_id') is None and unit.get('next_entry_state') is None, 'Brief EPI must terminate scope')
    requirements = scope.get('consequential_choice_requirements')
    require(isinstance(requirements, list), 'Consequential choice requirements missing')
    required_choices = {r['choice_id']: r for r in requirements}
    require(len(required_choices) == len(requirements), 'Duplicate choice requirement')
    for cid, kind in CRITICAL_CHOICES.items():
        require(required_choices.get(cid, {}).get('kind') == kind
                and required_choices[cid].get('use_mode') == 'USED', f'Current critical selection missing: {cid}')
    choice_rows = history.get('consequential_choices', [])
    choices = {c['choice_id']: c for c in choice_rows}
    require(len(choices) == len(choice_rows) and set(choices) == set(required_choices), 'Choice registry mismatch')
    for cid, requirement in required_choices.items():
        choice = choices[cid]
        use = requirement.get('use_mode')
        require(use in {'USED', 'NOT_USED'}, 'Invalid choice use mode')
        used_ports = strings(choice.get('used_port_ids', []), 'choice used ports', False)
        require(used_ports <= port_ids, 'Choice uses unknown finite port')
        if use == 'USED':
            require(choice.get('status') == 'RESOLVED_SELECTED' and used_ports, 'Used consequential choice is pending/HOLD')
            source = selected_record(sources.read(choice.get('selection_source_ref')), requirement.get('kind'))
            require(source.get('choice_id') == cid, 'Selection source choice ID mismatch')
            require(choice.get('resolution') == source['resolution'], 'Choice resolution differs from actual selected source')
            if requirement['kind'] == 'CALENDAR_AVAILABILITY':
                require(source.get('used_calendar_status') == 'SELECTED_RESOLVED', 'Calendar availability remains pending')
                covered_ports = strings(source.get('covered_exit_port_ids'), 'selected calendar covered ports')
                require(used_ports <= covered_ports <= port_ids, 'Actual used calendar port coverage missing')
            choices[cid] = dict(choice, selected_source=source)
        else:
            require(choice.get('status') == 'NOT_USED' and not used_ports, 'Unused award cannot have used ports')
    for pid, port in port_map.items():
        ids = strings(port.get('consequential_choice_ids', []), 'port choices', False)
        require(ids <= set(choices) and all(choices[c]['status'] == 'RESOLVED_SELECTED' for c in ids),
                'Finite exit consumes an unresolved choice')
        for cid in ids:
            require(pid in choices[cid]['used_port_ids'], 'Choice/port backlink mismatch')
    for cid, choice in choices.items():
        for pid in choice.get('used_port_ids', []):
            require(cid in port_map[pid].get('consequential_choice_ids', []), 'Choice claimed without an actual used exit')
    episodes = allocation.get('episodes')
    n = allocation.get('final_episode_count')
    require(integer(n) and n > 0 and isinstance(episodes, list) and len(episodes) == n, 'Final N is not explicitly locked')
    require(all(integer(e.get('episode')) for e in episodes)
            and [e['episode'] for e in episodes] == list(range(1, n + 1)), 'Final episode numbering not contiguous')
    unit_indexes = [UNITS.index(e['unit_id']) if e.get('unit_id') in UNITS else -1 for e in episodes]
    require(set(unit_indexes) == set(range(len(UNITS))) and unit_indexes == sorted(unit_indexes), 'Current unit order/coverage invalid')
    require(all(e.get('category') in definitions for e in episodes), 'Unknown final episode category')
    nba = sum(e['category'] in counted for e in episodes)
    require(75 * n <= 100 * nba <= 85 * n, 'Final approved NBA proportion is outside 75–85')
    require(all(e['category'] == 'POST_NBA' for e in episodes if e['unit_id'] == 'EPI'), 'Brief EPI must be POST_NBA')
    for unit in units:
        rows = [e for e in episodes if e['unit_id'] == unit['unit_id']]
        require(rows[0].get('entry_state') == unit['entry_state']
                and rows[-1].get('exit_state_required') == unit['exit_state'], 'Final allocation unit boundary differs from selected history')
    authorities = authority.get('episode_authorities', [])
    require(isinstance(authorities, list) and all(integer(a.get('episode')) for a in authorities),
            'Actual authority episode IDs must be integers, not Boolean or float')
    by_episode = {a['episode']: a for a in authorities}
    require(len(authorities) == n and len(by_episode) == n and set(by_episode) == set(range(1, n + 1)), 'Actual authority coverage incomplete')
    consumed = set()
    packs = []
    for episode in episodes:
        row = by_episode[episode['episode']]
        require(row.get('qualified_status') == 'ACTUAL_VERIFIED', 'Candidate Blueprint cannot become actual')
        ref = row.get('blueprint')
        bp = sources.read(ref)
        bp_doc = load(root, ref['path'])
        require(bp_doc.get('status') == 'ACTUAL_VERIFIED_CURRENT_BLUEPRINT_BUNDLE', 'Blueprint bundle is not actual verified')
        text(bp_doc.get('producer_id'), 'Blueprint producer')
        require(bp_doc['producer_id'] != review['reviewer_id'], 'Blueprint producer cannot review own bundle')
        require(isinstance(bp, dict) and bp.get('status') == 'ACTUAL_VERIFIED', 'Individual Blueprint is not actual verified')
        require(integer(bp.get('episode')), 'Individual Blueprint episode must be an exact integer')
        require(bp.get('scope_id') == scope_id, 'Individual Blueprint does not belong to current scope')
        gates(bp)
        for key in ('episode', 'unit_id', 'category', 'episode_function', 'action_choice', 'durable_cost',
                    'state_change', 'entry_state', 'exit_state_required',
                    'consumed_exit_port_ids', 'consequential_choice_ids'):
            require(bp.get(key) == episode.get(key), f'Blueprint/allocation mismatch: {key}')
        ids = strings(episode.get('consumed_exit_port_ids', []), 'episode exit ports', False)
        require(ids <= port_ids and all(port_map[p]['unit_id'] == episode['unit_id'] for p in ids), 'Episode consumes another unit exit')
        consumed.update(ids)
        choices_here = strings(episode.get('consequential_choice_ids', []), 'episode choices', False)
        require(choices_here <= set(choices)
                and all(choices[c]['status'] == 'RESOLVED_SELECTED' for c in choices_here), 'Episode consumes unselected choice')
        require(set(c for p in ids for c in port_map[p].get('consequential_choice_ids', [])) <= choices_here,
                'Episode omits its used exit consequential choice')
        for key in ('episode_function', 'action_choice', 'durable_cost', 'state_change',
                    'timeline_window', 'unit_question', 'setup_to_plant', 'payoff_to_consume',
                    'reader_question', 'relationship_state', 'physical_state', 'basketball_goal', 'forbidden_changes'):
            text(bp.get(key), f'Blueprint {key}')
        devices = bp.get('primary_devices')
        strings(devices, 'primary devices')
        require(1 <= len(devices) <= 2, 'Primary device budget must be 1–2')
        require(bp.get('unresolved_used_dependencies') == [], 'Blueprint has unresolved used availability or choice')
        validate_access(bp, sources, choices)
        packs.append({'status': 'ACTUAL_VERIFIED_CURRENT_CONTEXT_PACK', 'scope_id': scope_id,
                      'manuscript_allowed': False, 'design_gate': 'CLOSED', 'freeze': 'v0.30 PARTIAL',
                      'blueprint_source': ref, 'blueprint': bp})
    require(consumed == port_ids, 'Final episodes do not consume every finite used exit')
    return {'scope_id': scope_id, 'final_episode_count': n, 'nba_count': nba,
            'nba_percent': 100 * nba / n,
            'strict_draft_excluded_percent': 100 * sum(e['category'] == 'NBA' for e in episodes) / n,
            'category_policy': policy, 'packs': packs, 'used_sources_sha256': sources.used,
            'authority_payload_sha256': authority_payload_digest(authority), 'independent_review': review_ref}


def serialized(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def write_outputs(root, result, check=False):
    """Preflight every file before any creation; never replace existing bytes."""
    root = Path(root).resolve()
    out = safe_path(root, OUT, must_exist=False)
    outputs = {f"EP{p['blueprint']['episode']:04}.json": serialized(p) for p in result['packs']}
    manifest = {key: value for key, value in result.items() if key != 'packs'}
    manifest.update(status='ACTUAL_CURRENT_PACK_MANIFEST', manuscript_allowed=False,
                    design_gate='CLOSED', freeze='v0.30 PARTIAL')
    outputs['manifest.json'] = serialized(manifest)
    if out.exists():
        require(out.is_dir() and not (root / OUT).is_symlink(), 'Output directory is unsafe')
        require(set(p.name for p in out.iterdir()) <= set(outputs), 'Unexpected stale output entries')
    for name, content in outputs.items():
        path = out / name
        if path.exists() or path.is_symlink():
            require(path.is_file() and not path.is_symlink() and path.read_bytes() == content,
                    f'Refusing stale or different existing pack: {name}')
        elif check:
            raise ValueError(f'Actual output missing: {name}')
    if check:
        return
    out.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        for name, content in outputs.items():
            path = out / name
            if not path.exists():
                with path.open('xb') as handle:
                    created.append(path)
                    handle.write(content)
    except Exception:
        for path in created:
            path.unlink()
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true', help='Create all validated packs without overwriting')
    mode.add_argument('--check', action='store_true', help='Validate existing complete outputs without writing')
    args = parser.parse_args()
    try:
        result = compile_inputs(ROOT)
        if args.write or args.check:
            write_outputs(ROOT, result, check=args.check)
        print(json.dumps({'validated': True, 'episodes': result['final_episode_count'],
                          'nba_percent': result['nba_percent'], 'packs_written': bool(args.write)}, ensure_ascii=False))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f'Current pack generation blocked: {exc}\n')


if __name__ == '__main__':
    main()
