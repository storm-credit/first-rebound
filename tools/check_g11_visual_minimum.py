"""Check registered visual minimum records' scope and addresses, not pixels or meaning."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'research/G11_ORV_VISUAL_MINIMUM_2026_10_02.json'
READING_LEDGER = 'research/STYLE_READING_OBSERVATIONS.json'
WORK = '전지적 독자 시점'
FIELD_WORK = '필드의 고인물'
FIELD_SOURCE = 'research/G11_FIELD_VISUAL_MINIMUM_2026_10_02.json'
RECORDS = {
    WORK: {'source': SOURCE, 'novel_id': '104753', 'main_episode_offset': -1,
           'manual_diagnostic_expected': True},
    FIELD_WORK: {
        'source': FIELD_SOURCE,
        'novel_id': '153525', 'main_episode_offset': -1,
        'manual_diagnostic_expected': False,
    },
}
SHA = re.compile(r'^[0-9a-f]{64}$')
FALSE_FLAGS = (
    'whole_P3_final', 'G11_final', 'author_locked', 'season_selected',
    'manuscript_allowed', 'raw_novel_text_retained', 'raw_novel_text_uploaded',
    'screenshots_retained', 'screenshots_uploaded', 'independent_semantic_authentication',
    'exact_dom_measurement_promoted', 'canonical_reproduction_verified',
)
NULL_METRICS = (
    'first1000_density', 'sentence_length_distribution',
    'paragraph_length_distribution', 'voice_ratios',
)
REWARD_STATES = ('actual', 'conditional', 'unexecuted', 'premise', 'information')
SCENE_KINDS = {'EXPOSITION', 'DIALOGUE', 'PHYSICAL'}


def _normalized_sha(path):
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def _url_identity(url):
    try:
        parsed = urlsplit(url)
    except (TypeError, ValueError):
        return None
    if parsed.scheme != 'https' or parsed.netloc not in {'www.munpia.com', 'munpia.com'}:
        return None
    return parsed.path.rstrip('/')


def _raw_payload(value):
    if isinstance(value, dict):
        if any(k in value for k in ('raw_novel_text', 'novel_body_text', 'full_body_text',
                                    'raw_body_text', 'screenshot_data', 'image_base64')):
            return True
        return any(_raw_payload(v) for v in value.values())
    if isinstance(value, list):
        return any(_raw_payload(v) for v in value)
    return isinstance(value, str) and len(value) > 1200


def validate(data, root=ROOT, ledger=None):
    """Return structural defects. A clean result does not authenticate original text."""
    errors = []

    def require(ok, message):
        if not ok:
            errors.append(message)

    work = data.get('work')
    config = RECORDS.get(work)
    require(config is not None, 'work identity')
    require(data.get('evidence_mode') == 'VISUAL_SCOPED_MINIMUM', 'visual evidence mode')
    require(data.get('current_mode') == 'QUALITATIVE_VISUAL_INPUT_ONLY', 'visual-only scope')
    require(data.get('minimum_comparison_record_ready') is True and
            data.get('minimum_record_prepared') is True and
            'QUALITATIVE_VISUAL_INPUT_ONLY' in str(data.get('minimum_ready_scope')),
            'prepared qualitative scope declaration')
    snapshot = data.get('minimum_work_records_ready')
    target = data.get('minimum_work_records_target')
    require(snapshot is None or (isinstance(snapshot, int) and isinstance(target, int)
            and 0 < snapshot <= target), 'prepared count snapshot metadata')
    require(data.get('freeze') == 'v0.30 PARTIAL' and data.get('design_gate') == 'CLOSED'
            and data.get('manuscript_gate') == 'CLOSED', 'freeze/design/manuscript gate')
    require(data.get('first1000_boundary') is None and data.get('exact_dom_metrics') is None
            and data.get('body_sha256') is None and data.get('canonical_measurement_sha256') is None
            and data.get('separate_exact_prefix_pending') is True,
            'exact DOM/prefix measurement promoted')
    for key in FALSE_FLAGS:
        require(data.get(key) is False, 'forbidden promotion/retention: ' + key)
    require(data.get('new_unique_readings') == 0 and data.get('actual_episode_packs') == 0,
            'new reading or pack inflation')
    require(not _raw_payload(data), 'raw novel or screenshot payload')

    hashes = data.get('source_hashes')
    require(isinstance(hashes, dict) and bool(hashes), 'source hashes absent')
    method = data.get('source_hash_method', '')
    require(isinstance(method, str) and 'LF' in method and ('UTF8' in method or 'UTF-8' in method),
            'source normalization method')
    if isinstance(hashes, dict):
        for rel, digest in hashes.items():
            if not isinstance(rel, str):
                errors.append('source path/hash format')
                continue
            path = (root / rel).resolve()
            if (not rel.startswith('research/')
                    or not path.is_relative_to(root.resolve()) or not path.is_file()
                    or not SHA.fullmatch(str(digest))):
                errors.append('source path/hash format')
            elif _normalized_sha(path) != digest:
                errors.append('source content changed')

    fields = data.get('common_fourteen_fields')
    if not isinstance(fields, list) or len(fields) != 14:
        errors.append('14-item checklist')
    else:
        ids = [f.get('id') if isinstance(f, dict) else None for f in fields]
        require(len(set(ids)) == 14 and all(ids), '14-item duplicate or missing ID')
        require(all(isinstance(f, dict) and f.get('label') and f.get('status') and
                    (f.get('scoped_observation') or f.get('limitation')) for f in fields),
                '14-item observation/limit')

    boundary = data.get('manual_first1000_boundary', {})
    require(isinstance(boundary, dict) and boundary.get('first1000_exact_boundary') is None,
            'exact first1000 promoted')
    if not isinstance(boundary, dict):
        boundary = {}
    page_range = boundary.get('visual_page_range')
    first_end = None
    chapters_preview = data.get('chapters')
    if isinstance(chapters_preview, list) and chapters_preview and isinstance(chapters_preview[0], dict):
        view = chapters_preview[0].get('viewer_pages', {})
        ends = view.get('body_end', []) if isinstance(view, dict) else []
        if isinstance(ends, list) and ends and all(isinstance(p, int) for p in ends):
            first_end = max(ends)
    require(boundary.get('diagnostic_only') is True and boundary.get('serial_chapter') == 1
            and isinstance(page_range, list) and len(page_range) == 2
            and all(type(p) is int for p in page_range)
            and first_end is not None and 1 <= page_range[0] <= page_range[1] <= first_end,
            'manual first1000 range/mode')
    neighborhood_valid = (bool(boundary.get('boundary_neighborhood'))
                          if work == WORK else
                          boundary.get('boundary_neighborhood') is None and
                          boundary.get('range_status') ==
                          'FULL_PROLOGUE_OPENING_WINDOW_LENGTH_UNMEASURED')
    require(neighborhood_valid and bool(boundary.get('assumptions'))
            and bool(boundary.get('limitations')) and bool(boundary.get('range_status'))
            and bool(boundary.get('selected_qualitative_function_order')),
            'manual first1000 basis/uncertainty')
    require(boundary.get('temporary_transcription_retained') is False and
            boundary.get('temporary_transcription_sent_to_other_models') is False,
            'manual temporary transcription retained/sent')
    diagnostic = boundary.get('diagnostic')
    require('diagnostic' in boundary, 'manual diagnostic absent')
    if config is not None:
        require((diagnostic is not None) == config['manual_diagnostic_expected'],
                'registered manual diagnostic scope')
    if diagnostic is None:
        # A separately observed opening window can be prepared as qualitative
        # input without inventing a manual character count or an exact boundary.
        fresh = data.get('fresh_opening_observation')
        first = chapters_preview[0] if isinstance(chapters_preview, list) and chapters_preview else {}
        if not isinstance(fresh, dict):
            fresh = {}
        if not isinstance(first, dict):
            first = {}
        spreads = fresh.get('observed_spreads')
        pages = ([page for spread in spreads for page in spread]
                 if isinstance(spreads, list) and all(isinstance(s, list) for s in spreads) else [])
        first_view = first.get('viewer_pages')
        if not isinstance(first_view, dict):
            first_view = {}
        window_valid = (isinstance(page_range, list) and len(page_range) == 2 and
                        all(type(p) is int for p in page_range) and
                        first_end is not None and page_range == [1, first_end] and
                        pages == list(range(1, first_end + 1)))
        require(window_valid and fresh.get('selected_window_separately_read') is True and
                fresh.get('full_body_read') is True and fresh.get('body_end_observed') is True and
                fresh.get('window_length_measured') is False and
                bool(fresh.get('observer')) and bool(fresh.get('date')) and
                bool(fresh.get('display_mode')) and fresh.get('viewport_override') is False and
                _url_identity(fresh.get('official_url')) == _url_identity(first.get('official_url')) and
                fresh.get('body_end_page') == first_end and
                fresh.get('total_viewer_pages') == first_view.get('total') and
                first_view.get('unit') == 'CONDITIONAL_VISUAL_VIEWER_PAGE',
                'unmeasured opening window not separately observed')
        require(not any(key in boundary for key in (
            'utf16_under_assumption', 'manual_display_blocks', 'assumed_join_LF_total',
            'join_sensitivity_variants', 'character_count', 'sentence_count',
            'paragraph_count', 'first1000_count', 'first1000_density')) and
                not any(key in fresh for key in (
                    'utf16_under_assumption', 'manual_display_blocks',
                    'character_count', 'sentence_count', 'paragraph_count',
                    'first1000_count', 'first1000_density')),
            'unmeasured manual quantity promoted')
    elif isinstance(diagnostic, dict):
        require(diagnostic.get('publishable_metric') is False and
                type(diagnostic.get('utf16_under_assumption')) is int and
                diagnostic['utf16_under_assumption'] > 0 and
                type(diagnostic.get('manual_display_blocks')) is int and
                diagnostic['manual_display_blocks'] > 0 and bool(diagnostic.get('assumed_join')),
                'manual diagnostic misrepresented')
        require(diagnostic.get('original_text_error_bound') is None and
                diagnostic.get('variants_are_original_text_error_bounds') is False,
                'manual join variants misrepresented as original-text bounds')
        variants = diagnostic.get('join_sensitivity_variants')
        if (isinstance(variants, list) and type(diagnostic.get('manual_display_blocks')) is int and
                type(diagnostic.get('utf16_under_assumption')) is int and
                type(diagnostic.get('assumed_join_LF_total')) is int):
            gaps = diagnostic['manual_display_blocks'] - 1
            base = diagnostic['utf16_under_assumption'] - diagnostic['assumed_join_LF_total']
            require(gaps >= 0 and base > 0 and diagnostic['assumed_join_LF_total'] == gaps * 2
                    and len(variants) == 3 and
                    {v.get('join_LF_per_gap') for v in variants if isinstance(v, dict)} == {0, 1, 2}
                    and all(isinstance(v, dict) and type(v.get('join_LF_per_gap')) is int
                            and type(v.get('utf16_under_assumption')) is int
                            and v['utf16_under_assumption'] == base + gaps * v['join_LF_per_gap']
                            for v in variants),
                    'manual join sensitivity arithmetic')
        else:
            errors.append('manual join sensitivity arithmetic')
    else:
        errors.append('manual diagnostic misrepresented')
    require(not any(k in boundary for k in ('body_sha256', 'first1000_sha256', 'canonical_sha256')),
            'manual range labeled DOM hash')

    if ledger is None:
        ledger = json.loads((root / READING_LEDGER).read_text(encoding='utf-8'))
    official = {r['chapter']: _url_identity(r['url']) for r in ledger['readings']
                if r.get('work') == work and r.get('chapter') in range(1, 6)}
    require(len(official) == 5 and all(official.values()) and config is not None and
            all(path.startswith('/novel/viewer/' + config['novel_id'] + '/')
                for path in official.values() if path),
            'reading ledger first-five identity')

    chapters = data.get('chapters')
    if (not isinstance(chapters, list) or len(chapters) != 5 or
            not all(isinstance(c, dict) for c in chapters) or
            [c.get('serial_chapter') for c in chapters] != [1, 2, 3, 4, 5]):
        errors.append('five unique ordered chapters')
        return errors
    for index, chapter in enumerate(chapters, 1):
        identity = _url_identity(chapter.get('official_url'))
        require(identity is not None and identity == official.get(index), 'official chapter URL/work')
        require(config is not None and chapter.get('main_episode') ==
                index + config['main_episode_offset'] and bool(chapter.get('title')),
                'prologue/main episode identity')
        require(chapter.get('full_body_read') is True and chapter.get('body_end_observed') is True,
                'body start/end reading declaration')
        view = chapter.get('viewer_pages', {})
        if not isinstance(view, dict):
            view = {}
        end = view.get('body_end')
        total = view.get('total')
        unit = view.get('unit')
        historical = unit == 'HISTORICAL_CONDITIONAL_VISUAL_VIEWER_PAGE'
        require((unit == 'CONDITIONAL_VISUAL_VIEWER_PAGE' or
                 (work == FIELD_WORK and historical and
                  view.get('current_page_identity_certified') is False and
                  bool(view.get('observation_date'))))
                and view.get('conditional_address') is True,
                'conditional viewer address')
        require(isinstance(total, int) and total > 0 and isinstance(end, list) and bool(end)
                and all(isinstance(p, int) and 1 <= p <= total for p in end),
                'body end/total address')
        for key in ('body_sha256', 'canonical_measurement_sha256', 'first1000_sha256'):
            require(chapter.get(key) is None, 'unmeasured DOM hash promoted: ' + key)
        metrics = chapter.get('quantitative_metrics')
        require(isinstance(metrics, dict) and all(key in metrics and metrics[key] is None for key in NULL_METRICS)
                and all(value is None for value in metrics.values()),
                'unmeasured first1000/length/voice metric promoted')
        require(bool(chapter.get('central_event')) and bool(chapter.get('past_scene'))
                and bool(chapter.get('observed_sequence')),
                'chapter function/temporal record')
        reward = chapter.get('reward_states')
        require(isinstance(reward, dict) and all(k in reward and isinstance(reward[k], list)
                for k in REWARD_STATES), 'reward actual/conditional/unexecuted distinction')
        if isinstance(reward, dict) and all(isinstance(reward.get(k), list) for k in REWARD_STATES):
            require(all(isinstance(item, str) and item for key in REWARD_STATES
                        for item in reward[key]), 'reward status entries')
            actual = set(map(str, reward['actual']))
            pending = set(map(str, reward['conditional'] + reward['unexecuted']))
            require(not actual & pending, 'same reward both actual and pending')

    scenes = data.get('minimum_scene_samples')
    if (not isinstance(scenes, list) or not all(isinstance(s, dict) for s in scenes) or
            {s.get('kind') for s in scenes} != SCENE_KINDS):
        errors.append('three minimum scene kinds')
    else:
        for scene in scenes:
            serial = scene.get('serial_chapter')
            pages = scene.get('viewer_pages')
            require(isinstance(serial, int) and serial in range(1, 6), 'scene chapter address')
            if isinstance(serial, int) and serial in range(1, 6):
                last = chapters[serial - 1].get('viewer_pages', {}).get('body_end', [])
                body_end = max(last) if isinstance(last, list) and last else 0
            else:
                body_end = 0
            require(isinstance(pages, list) and len(pages) == 2 and all(isinstance(p, int) for p in pages)
                    and 1 <= pages[0] <= pages[1] <= body_end and
                    scene.get('address_is_conditional') is True,
                    'scene conditional page range')
            require(bool(scene.get('scoped_observation')), 'scene scoped observation')
            for key in ('display_block_count', 'character_count', 'scene_sha256'):
                require(scene.get(key) is None, 'scene unmeasured quantity promoted: ' + key)
    return errors


def audit(root=ROOT, sources=None):
    """Audit every registered record, or selected registered sources for diagnostics."""
    registered = {config['source']: work for work, config in RECORDS.items()}
    selected = list(registered) if sources is None else list(dict.fromkeys(sources))
    errors, ready_names, ready_sources, hashes = [], [], [], {}
    for source in selected:
        if source not in registered:
            errors.append(source + ': unregistered visual source')
            continue
        path = root / source
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(source + ': unreadable visual source: ' + str(exc))
            continue
        defects = validate(data, root)
        if data.get('work') != registered[source]:
            defects.append('registered source/work mismatch')
        if defects:
            errors.extend(source + ': ' + defect for defect in defects)
        else:
            ready_names.append(registered[source])
            ready_sources.append(source)
            hashes[source] = _normalized_sha(path)
    return {'PASS': not errors, 'errors': errors,
            'ready_works': len(set(ready_names)) if not errors else 0,
            'ready_work_names': ready_names if not errors else [],
            'record_sources': ready_sources if not errors else [],
            'record_source_hashes': hashes if not errors else {},
            'scope': 'VISUAL_ADDRESS_AND_DECLARATION_NOT_PIXEL_OR_SEMANTIC_AUTHENTICATION',
            'prepared_qualitative_visual': not errors, 'whole_P3_final': False, 'G11_final': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', action='append', help='registered repository-relative JSON path')
    args = parser.parse_args()
    result = audit(sources=args.source)
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(not result['PASS'])
