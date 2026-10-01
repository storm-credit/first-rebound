"""Check G11 scoped minimum records' provenance and boundaries, not novel meaning."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LEDGER = 'research/STYLE_READING_OBSERVATIONS.json'
BATCHES = {
    'research/G11_KAKAO_SCOPED_MINIMUM_2026_10_02.json': {
        '데뷔 못 하면 죽는 병 걸림': ('page.kakao.com', '56325530'),
        '나 혼자만 레벨업': ('page.kakao.com', '48787313'),
    },
    'research/G11_MUNPIA_REMAINING_MINIMUM_2026_10_02.json': {
        '아포칼립스에 집을 숨김': ('www.munpia.com', '342817'),
        '홈 플레이트의 빌런': ('www.munpia.com', '100495'),
        '닥터, 조선 가다': ('www.munpia.com', '103757'),
    },
}
SHA = re.compile(r'^[0-9a-f]{64}$')
FALSE_FLAGS = (
    'whole_P3_final', 'G11_final', 'author_locked', 'season_selected',
    'manuscript_allowed', 'raw_novel_text_retained', 'raw_novel_text_uploaded',
    'screenshots_retained', 'screenshots_uploaded',
    'independent_semantic_authentication', 'exact_dom_measurement_promoted',
    'canonical_reproduction_verified',
)
NULL_METRICS = (
    'body_sha256', 'canonical_measurement_sha256', 'first1000_sha256',
    'first1000_boundary', 'exact_dom_metrics', 'first1000_density',
    'information_density',
    'sentence_length_distribution', 'paragraph_length_distribution', 'voice_ratios',
)
SCENE_KINDS = {'EXPOSITION', 'DIALOGUE', 'PHYSICAL'}


def _normalized_sha(path):
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def _url_identity(value):
    try:
        parts = urlsplit(value)
    except (TypeError, ValueError):
        return None
    if parts.scheme != 'https':
        return None
    return (parts.netloc, parts.path.rstrip('/'))


def _raw_payload(value):
    if isinstance(value, dict):
        if any(key in value for key in ('raw_novel_text', 'novel_body_text',
                                        'full_body_text', 'raw_body_text',
                                        'screenshot_data', 'image_base64')):
            return True
        return any(_raw_payload(item) for item in value.values())
    if isinstance(value, list):
        return any(_raw_payload(item) for item in value)
    return isinstance(value, str) and len(value) > 1200


def _hash_errors(data, root):
    hashes = data.get('source_hashes')
    if not isinstance(hashes, dict) or not hashes:
        return ['source hashes absent']
    method = data.get('source_hash_method', '')
    errors = []
    if not isinstance(method, str) or 'LF' not in method or not (
            'UTF8' in method or 'UTF-8' in method):
        errors.append('source normalization method')
    if LEDGER not in hashes:
        errors.append('reading ledger source hash absent')
    for rel, digest in hashes.items():
        if not isinstance(rel, str):
            errors.append('source path/hash format')
            continue
        path = (root / rel).resolve()
        if (not rel.startswith('research/') or not path.is_relative_to(root.resolve())
                or not path.is_file() or not SHA.fullmatch(str(digest))):
            errors.append('source path/hash format')
        elif _normalized_sha(path) != digest:
            errors.append('source content changed')
    return errors


def validate(data, source, root=ROOT, ledger=None):
    """Return structural defects; a clean result does not certify semantics."""
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    expected = BATCHES.get(source)
    if expected is None or not isinstance(data, dict):
        return ['unregistered source or malformed batch']
    for flag in FALSE_FLAGS:
        require(data.get(flag) is False, 'scope promotion: ' + flag)
    require(data.get('freeze') == 'v0.30 PARTIAL' and
            data.get('design_gate') == 'CLOSED' and
            data.get('manuscript_gate') == 'CLOSED',
            'freeze/design/manuscript gate')
    require(data.get('checker_authenticates_semantics') is not True,
            'semantic certification promoted')
    require(data.get('new_unique_readings') == 0 and data.get('actual_episode_packs') == 0,
            'reading/pack inflation')
    require(not _raw_payload(data), 'raw novel or screenshot payload')
    errors.extend(_hash_errors(data, root))
    for key in NULL_METRICS:
        if key in data:
            require(data[key] is None, 'unmeasured batch metric promoted: ' + key)
    works = data.get('works')
    if (not isinstance(works, list) or len(works) != len(expected)
            or not all(isinstance(item, dict) for item in works)):
        return errors + ['registered work count']
    names = [item.get('work') for item in works]
    require(len(set(names)) == len(expected) and set(names) == set(expected),
            'registered work identity/duplicates')
    if ledger is None:
        ledger = json.loads((root / LEDGER).read_text(encoding='utf-8'))
    ledger_urls = {(r.get('work'), r.get('chapter')): _url_identity(r.get('url'))
                   for r in ledger['readings']}
    for item in works:
        name = item.get('work')
        if name not in expected:
            continue
        domain, book_id = expected[name]
        for flag in FALSE_FLAGS:
            if flag in item:
                require(item[flag] is False, name + ': scope promotion: ' + flag)
        require(item.get('checker_authenticates_semantics') is not True,
                name + ': semantic certification promoted')
        if 'new_unique_readings' in item:
            require(item['new_unique_readings'] == 0, name + ': reading inflation')
        if 'actual_episode_packs' in item:
            require(item['actual_episode_packs'] == 0, name + ': pack inflation')
        require(item.get('minimum_comparison_record_ready') is True and
                item.get('minimum_record_prepared') is True,
                name + ': minimum record not prepared')
        for key in NULL_METRICS:
            if key in item:
                require(item[key] is None, name + ': unmeasured metric promoted: ' + key)
        fields = item.get('common_fourteen_fields')
        if not isinstance(fields, list) or len(fields) != 14 or not all(
                isinstance(field, dict) for field in fields):
            errors.append(name + ': 14-item checklist')
        else:
            ids = [field.get('id') for field in fields]
            require(len(set(ids)) == 14 and all(ids) and all(
                field.get('status') and (field.get('scoped_observation') or
                                         field.get('limitation')) for field in fields),
                name + ': 14-item checklist')
        chapters = item.get('chapters')
        if (not isinstance(chapters, list) or len(chapters) != 5 or not all(
                isinstance(chapter, dict) for chapter in chapters) or
                [chapter.get('serial_chapter') for chapter in chapters] != [1, 2, 3, 4, 5]):
            errors.append(name + ': five unique ordered chapters')
            continue
        for serial, chapter in enumerate(chapters, 1):
            identity = _url_identity(chapter.get('official_url'))
            require(identity is not None and identity == ledger_urls.get((name, serial)) and
                    identity[0] == domain and
                    (('/content/' + book_id + '/') in identity[1] if domain == 'page.kakao.com'
                     else ('/novel/viewer/' + book_id + '/') in identity[1]),
                    name + ': official chapter URL/work')
            require(chapter.get('full_body_read') is True and
                    chapter.get('body_end_observed') is True,
                    name + ': P2 first-five full-body provenance')
            if domain == 'page.kakao.com':
                provenance = chapter.get('provenance')
                require(item.get('original_p2_source') == LEDGER and
                        isinstance(provenance, dict) and
                        provenance.get('original_p2_source') == LEDGER and
                        provenance.get('work') == name and
                        provenance.get('chapter') == serial and
                        _url_identity(provenance.get('official_url')) == identity and
                        provenance.get('scope') == 'EXISTING_COMPLETE_CHAPTER_P2_REUSED',
                        name + ': Kakao P2 original source')
                ending = chapter.get('ending_observation')
                if not isinstance(ending, dict):
                    errors.append(name + ': Kakao ending provenance')
                else:
                    scope = ending.get('scope')
                    address = ending.get('raw_display_p_range')
                    require(bool(ending.get('scoped_observation')) and
                            (scope == 'EXISTING_P2_BODY_END_FUNCTION_REUSED' or
                             (scope == 'ROOT_FRESH_TARGETED_END' and
                              isinstance(address, list) and len(address) == 2 and
                              all(type(p) is int for p in address) and
                              1 <= address[0] <= address[1])),
                            name + ': Kakao ending provenance')
            else:
                provenance = chapter.get('provenance')
                require(isinstance(provenance, dict) and
                        provenance.get('source') == LEDGER and
                        provenance.get('scope') == 'COMPLETE_CHAPTER' and
                        type(provenance.get('fresh_current_body_end_reobserved')) is bool,
                        name + ': Munpia P2 original source/current distinction')
                ending = chapter.get('ending')
                require(isinstance(ending, dict) and bool(ending.get('scope')) and
                        (ending.get('current_end_marker_observed') is False or
                         (ending.get('current_end_marker_observed') is True and
                          bool(ending.get('viewer_pages')) and bool(ending.get('function')))),
                        name + ': Munpia ending provenance')
                view = chapter.get('viewer_pages')
                if not isinstance(view, dict):
                    view = {}
                unit = view.get('unit')
                if unit == 'HISTORICAL_CONDITIONAL_VISUAL_RANGE':
                    require(view.get('current_page_identity_certified') is False and
                            view.get('body_end') is None and view.get('total') is None,
                            name + ': historical viewer address promoted')
                elif unit == 'CONDITIONAL_VISUAL_VIEWER_PAGE':
                    end = view.get('body_end')
                    total = view.get('total')
                    require(view.get('current_page_identity_certified') is True and
                            bool(view.get('observation_date')) and
                            isinstance(end, list) and bool(end) and
                            type(total) is int and total > 0 and
                            all(type(page) is int and 1 <= page <= total for page in end),
                            name + ': current viewer address invalid')
                else:
                    errors.append(name + ': viewer provenance unit')
            for key in NULL_METRICS:
                if key in chapter:
                    require(chapter[key] is None, name + ': unmeasured chapter metric: ' + key)
            metrics = chapter.get('quantitative_metrics')
            if metrics is not None:
                require(isinstance(metrics, dict) and all(value is None for value in metrics.values()),
                        name + ': unmeasured chapter quantity promoted')
            require(bool(chapter.get('central_event')) and bool(chapter.get('past_scene'))
                    and bool(chapter.get('observed_sequence') or chapter.get('observed_functions')),
                    name + ': chapter function/temporal record')
        boundary = item.get('manual_first1000_boundary')
        if not isinstance(boundary, dict):
            errors.append(name + ': scoped opening boundary absent')
        else:
            require(boundary.get('serial_chapter') == 1 and
                    boundary.get('first1000_exact_boundary') is None and
                    boundary.get('diagnostic') is None and
                    bool(boundary.get('assumptions')) and bool(boundary.get('limitations')),
                    name + ': scoped opening uncertainty')
        fresh = item.get('fresh_opening_observation')
        if not isinstance(fresh, dict):
            errors.append(name + ': fresh opening observation absent')
        else:
            for flag in FALSE_FLAGS:
                if flag in fresh:
                    require(fresh[flag] is False,
                            name + ': fresh scope promotion: ' + flag)
            require(fresh.get('selected_window_separately_read') is True and
                    _url_identity(fresh.get('official_url')) ==
                    _url_identity(chapters[0].get('official_url')) and
                    fresh.get('window_length_measured') is False,
                    name + ': fresh opening source/window')
        if isinstance(boundary, dict) and isinstance(fresh, dict):
            if domain == 'page.kakao.com':
                raw_range = boundary.get('raw_display_p_range')
                snapshot = fresh.get('display_join_diagnostic')
                require(boundary.get('diagnostic_only') is True and
                        isinstance(raw_range, list) and len(raw_range) == 2 and
                        all(type(p) is int for p in raw_range) and
                        1 <= raw_range[0] <= raw_range[1] and
                        raw_range == fresh.get('observed_raw_display_p_range') and
                        fresh.get('observer') == 'ROOT_CODEX' and
                        fresh.get('exact_author_text_first1000_verified') is False and
                        fresh.get('scope') ==
                        'SINGLE_OPEN_DISPLAY_P_JOIN_DIAGNOSTIC_NOT_CANONICAL',
                        name + ': Kakao single-open display-p scope')
                require(isinstance(snapshot, dict) and
                        snapshot.get('utf16_under_assumption') == 1000 and
                        type(snapshot.get('last_p_included_text_utf16')) is int and
                        snapshot['last_p_included_text_utf16'] > 0 and
                        snapshot.get('last_p_included_text_utf16') ==
                        boundary.get('last_p_included_text_utf16') and
                        snapshot.get('publishable_metric') is False and
                        snapshot.get('variants_are_original_text_error_bounds') is False and
                        '2LF' in str(boundary.get('separator_assumption')),
                        name + ': Kakao 2LF snapshot diagnostic')
            else:
                visual_range = boundary.get('visual_page_range')
                observed = fresh.get('observed_pages')
                pages = ([page for pair in observed for page in pair]
                         if isinstance(observed, list) and all(
                             isinstance(pair, list) for pair in observed) else [])
                safe_page_max = max((page for page in pages if type(page) is int), default=0)
                require(isinstance(visual_range, list) and len(visual_range) == 2 and
                        all(type(p) is int for p in visual_range) and
                        1 <= visual_range[0] <= visual_range[1] and
                        all(type(page) is int and page > 0 for page in pages) and
                        pages == list(range(visual_range[0], safe_page_max + 1)) and
                        set(range(visual_range[0], visual_range[1] + 1)) <= set(pages) and
                        (fresh.get('actual_body_page_range') is None or
                         fresh.get('actual_body_page_range') == visual_range) and
                        boundary.get('boundary_neighborhood') is None and
                        'LENGTH_UNMEASURED' in str(boundary.get('range_status')) and
                        type(fresh.get('full_body_read')) is bool,
                        name + ': Munpia visual window is not exact1000')
                view = chapters[0].get('viewer_pages')
                if not isinstance(view, dict):
                    view = {}
                require(view.get('unit') == 'CONDITIONAL_VISUAL_VIEWER_PAGE' and
                        isinstance(fresh.get('body_end_pages'), list) and
                        isinstance(view.get('body_end'), list) and
                        bool(view['body_end']) and
                        all(type(page) is int for page in view['body_end'] +
                            fresh['body_end_pages']) and
                        set(view['body_end']) <= set(fresh['body_end_pages']) and
                        max(view['body_end']) == max(fresh['body_end_pages']) and
                        fresh.get('total_viewer_pages') == view.get('total') and
                        fresh.get('body_end_observed') is True and
                        (fresh.get('full_body_read') is False or
                         (isinstance(fresh.get('body_end_pages'), list) and
                          bool(fresh['body_end_pages']) and
                          safe_page_max >= max((page for page in fresh['body_end_pages']
                                                if type(page) is int), default=0))) and
                        fresh.get('observer') == 'ROOT_CODEX' and
                        bool(fresh.get('display_mode')),
                        name + ': Munpia fresh viewer/source identity')
        scenes = item.get('minimum_scene_samples')
        if not isinstance(scenes, list) or len(scenes) != 3 or not all(
                isinstance(scene, dict) for scene in scenes):
            errors.append(name + ': three scene samples')
        else:
            require({scene.get('kind') for scene in scenes} == SCENE_KINDS and all(
                scene.get('serial_chapter') in range(1, 6) and
                bool(scene.get('scoped_observation')) and
                scene.get('character_count') is None and scene.get('scene_sha256') is None
                for scene in scenes), name + ': scene scope/address')
            for scene in scenes:
                if domain == 'page.kakao.com':
                    address = scene.get('raw_display_p_range')
                    require(scene.get('address_is_snapshot') is True and
                            isinstance(address, list) and len(address) == 2 and
                            type(address[0]) is int and address[0] > 0 and
                            (address[1] is None or
                             (type(address[1]) is int and address[1] >= address[0])) and
                            bool(scene.get('address_method')) and
                            scene.get('observer') == 'ROOT_CODEX' and
                            scene.get('scope') ==
                            'FRESH_TARGETED_SCENE_NOT_FRESH_WHOLE_CHAPTER',
                            name + ': Kakao scene snapshot address')
                else:
                    address = scene.get('viewer_pages')
                    serial = scene.get('serial_chapter')
                    view = chapters[serial - 1].get('viewer_pages') if serial in range(1, 6) else {}
                    ends = view.get('body_end') if isinstance(view, dict) else None
                    last = max((page for page in ends if type(page) is int), default=None) \
                        if isinstance(ends, list) else None
                    require(scene.get('address_is_conditional') is True and
                            isinstance(address, list) and len(address) == 2 and
                            all(type(p) is int for p in address) and
                            1 <= address[0] <= address[1] and
                            (last is None or address[1] <= last) and
                            scene.get('status') == 'ROOT_FRESH_TARGETED_VISUAL_READ' and
                            scene.get('observer') == 'ROOT_CODEX',
                            name + ': Munpia scene conditional address/provenance')
    return errors


def audit(root=ROOT, sources=None):
    selected = list(BATCHES) if sources is None else list(dict.fromkeys(sources))
    errors, names, records, hashes = [], [], [], {}
    for source in selected:
        if source not in BATCHES:
            errors.append(source + ': unregistered scoped batch')
            continue
        try:
            data = json.loads((root / source).read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(source + ': unreadable scoped batch: ' + str(exc))
            continue
        defects = validate(data, source, root)
        if defects:
            errors.extend(source + ': ' + defect for defect in defects)
        else:
            names.extend(item['work'] for item in data['works'])
            records.append(source)
            hashes[source] = _normalized_sha(root / source)
    if len(names) != len(set(names)):
        errors.append('duplicate work across batches')
    return {'PASS': not errors, 'errors': errors,
            'ready_works': len(names) if not errors else 0,
            'ready_work_names': names if not errors else [],
            'record_sources': records if not errors else [],
            'record_source_hashes': hashes if not errors else {},
            'scope': 'SCOPED_SOURCE_AND_ADDRESS_NOT_CANONICAL_TEXT_OR_SEMANTIC_AUTHENTICATION',
            'whole_P3_final': False, 'G11_final': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', action='append', help='registered repository-relative JSON path')
    args = parser.parse_args()
    report = audit(sources=args.source)
    print(json.dumps(report, ensure_ascii=False))
    raise SystemExit(not report['PASS'])
