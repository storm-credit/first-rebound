"""Audit G11 ten-work synthesis links and counts, never literary meaning."""
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'research/G11_TEN_WORK_SYNTHESIS_2026_10_02.json'
PROGRESS = 'research/G11_COMPONENT_PROGRESS_2026_10_01.json'
LEDGER = 'research/STYLE_READING_OBSERVATIONS.json'
SHA = re.compile(r'^[0-9a-f]{64}$')
EVIDENCE_SOURCES = {
    'research/G11_CORE_EXTENSION_2026_10_02.json',
    'research/G11_POPULARITY_PROVENANCE_2026_10_01.json',
    'research/G11_RECORDED_FUNCTION_CODING_2026_10_01.json',
    'research/G11_THREE_WORK_RANGES_2026_10_01.json',
    'research/G11_SGRADE_COMMON_MINIMUM_2026_10_02.json',
    'research/G11_BUSINESS_COMMON_MINIMUM_2026_10_02.json',
    'research/G11_EXTRA_COMMON_MINIMUM_2026_10_02.json',
    'research/G11_ORV_VISUAL_MINIMUM_2026_10_02.json',
    'research/G11_FIELD_VISUAL_MINIMUM_2026_10_02.json',
    'research/G11_KAKAO_SCOPED_MINIMUM_2026_10_02.json',
    'research/G11_MUNPIA_REMAINING_MINIMUM_2026_10_02.json',
}
ARTIFACT_SOURCES = {path for path in EVIDENCE_SOURCES if 'MINIMUM_2026' in path}
FALSE_FLAGS = (
    'whole_P3_final', 'FULL_TEXT_FINAL', 'G11_final', 'author_locked',
    'manuscript_allowed', 'season_selected', 'raw_novel_text_retained',
    'raw_novel_text_uploaded', 'screenshots_retained', 'screenshots_uploaded',
    'independent_semantic_authentication', 'independent_original_review',
    'whole_project_source_blind_complete', 'exact_dom_measurement_promoted',
    'canonical_reproduction_verified',
)
DOMAINS = {
    'www.munpia.com': 'Munpia', 'munpia.com': 'Munpia',
    'ridibooks.com': 'Ridi', 'www.joara.com': 'Joara',
    'page.kakao.com': 'KakaoPage', 'series.naver.com': 'NaverSeries',
}


def _normalized_sha(path):
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def _identity(url):
    try:
        parsed = urlsplit(url)
    except (TypeError, ValueError):
        return None
    return (parsed.netloc, parsed.path.rstrip('/')) if parsed.scheme == 'https' else None


def _embedded_raw(value):
    if isinstance(value, dict):
        if any(key in value for key in ('raw_novel_text', 'novel_body_text',
                                        'full_body_text', 'raw_body_text',
                                        'screenshot_data', 'image_base64')):
            return True
        return any(_embedded_raw(item) for item in value.values())
    if isinstance(value, list):
        return any(_embedded_raw(item) for item in value)
    return isinstance(value, str) and len(value) > 1200


def validate(data, root=ROOT, progress=None, ledger=None):
    """Return defects in provenance, reference links, counts and gate boundaries."""
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    if not isinstance(data, dict):
        return ['synthesis JSON object required']
    if progress is None:
        progress = json.loads((root / PROGRESS).read_text(encoding='utf-8'))
    if ledger is None:
        ledger = json.loads((root / LEDGER).read_text(encoding='utf-8'))

    for flag in FALSE_FLAGS:
        require(data.get(flag) is False, 'false gate/scope: ' + flag)
    require(data.get('freeze') == 'v0.30 PARTIAL' and
            data.get('design_gate') == 'CLOSED' and
            data.get('manuscript_gate') == 'CLOSED', 'freeze/design/manuscript gates')
    require(data.get('new_unique_readings') == 0 and data.get('actual_episode_packs') == 0 and
            data.get('manuscripts_written') == 0 and data.get('new_author_locked_decisions') == 0,
            'reading/pack/manuscript/decision inflation')
    require(not _embedded_raw(data), 'raw novel or screenshot payload')

    if data.get('sample_gate_complete') is True:
        require(data.get('sample_gate_scope') == 'QUALITATIVE_FUNCTION_COMPARISON_ONLY' and
                all(data.get(flag) is False for flag in
                    ('whole_P3_final', 'FULL_TEXT_FINAL', 'G11_final',
                     'author_locked', 'manuscript_allowed')),
                'sample gate exceeded qualitative function scope')
    else:
        require(data.get('sample_gate_complete') is False, 'sample gate boolean')

    hashes = data.get('source_hashes')
    require(isinstance(hashes, dict) and set(hashes) == EVIDENCE_SOURCES,
            'eleven evidence source identities')
    method = data.get('source_hash_method', '')
    require(isinstance(method, str) and 'UTF8' in method and 'LF' in method,
            'source hash normalization method')
    if isinstance(hashes, dict):
        for rel, digest in hashes.items():
            if not isinstance(rel, str):
                errors.append('evidence source path/hash format')
                continue
            path = (root / rel).resolve()
            if (not rel.startswith('research/') or not path.is_relative_to(root.resolve())
                    or not path.is_file() or not SHA.fullmatch(str(digest))):
                errors.append('evidence source path/hash format')
            elif _normalized_sha(path) != digest:
                errors.append('evidence source changed: ' + rel)

    expected_names = set(progress.get('common_minimum_work_names', []))
    expected_artifacts = set(progress.get('common_minimum_record_sources', []))
    require(progress.get('common_minimum_work_records_ready') == 10 and
            progress.get('common_minimum_work_records_target') == 10 and
            progress.get('common_minimum_work_records_remaining') == 0 and
            progress.get('unique_readings') == 110 and
            progress.get('unread') == 0 and
            progress.get('original_plan_unread') == 15 and
            len(expected_names) == 10 and expected_artifacts == ARTIFACT_SOURCES,
            'component progress 10/10 and seven artifacts')
    require(data.get('minimum_work_records_ready') == 10 and
            data.get('minimum_work_records_target') == 10 and
            data.get('minimum_work_records_remaining') == 0 and
            data.get('prepared_artifact_entries') == 10 and
            data.get('prepared_artifact_entries_are_final_ready_count') is False,
            'synthesis minimum count/scope')
    verification = data.get('minimum_artifact_verification')
    if not isinstance(verification, dict):
        errors.append('artifact verification absent')
    else:
        listed = verification.get('source_files')
        checker = verification.get('parent_final_checker_result', {})
        require(isinstance(listed, list) and len(listed) == 7 and
                set(listed) == expected_artifacts and
                isinstance(checker, dict) and checker.get('status') == 'PASS' and
                checker.get('unique_works') == 10 and checker.get('target_works') == 10 and
                checker.get('missing_common_fourteen_fields') == 0 and
                checker.get('authenticates_independent_original_semantics') is False,
                'artifact checker provenance')

    works = data.get('works')
    if not isinstance(works, list) or len(works) != 10 or not all(
            isinstance(work, dict) for work in works):
        errors.append('ten work entries')
        return errors
    names = [work.get('work') for work in works]
    require(len(set(names)) == 10 and set(names) == expected_names,
            'ten unique works match progress')
    work_artifacts = {work.get('work'): work.get('artifact') for work in works}
    require(set(work_artifacts.values()) == ARTIFACT_SOURCES and
            all(path in hashes for path in work_artifacts.values()) if isinstance(hashes, dict)
            else False, 'work artifact links')
    ledger_urls = {(row.get('work'), row.get('chapter')): _identity(row.get('url'))
                   for row in ledger.get('readings', [])}
    for work in works:
        name = work.get('work')
        artifact = work.get('artifact')
        require(work.get('source_record_ready_at_assembly') is True and
                work.get('new_unique_readings') == 0 and
                work.get('current_and_historical_addresses_are_interchangeable') is False,
                'work scoped readiness/address: ' + str(name))
        chapters = work.get('official_chapter_links')
        if (not isinstance(chapters, list) or len(chapters) != 5 or not all(
                isinstance(chapter, dict) for chapter in chapters) or
                [chapter.get('serial_chapter') for chapter in chapters] != [1, 2, 3, 4, 5]):
            errors.append('five official chapter links: ' + str(name))
        else:
            for chapter in chapters:
                serial = chapter['serial_chapter']
                require(_identity(chapter.get('official_url')) == ledger_urls.get((name, serial)) and
                        ledger_urls.get((name, serial)) is not None,
                        'official chapter link mismatch: ' + str(name))
        if artifact in ARTIFACT_SOURCES and (root / artifact).is_file():
            source_record = json.loads((root / artifact).read_text(encoding='utf-8'))
            contained = (set(item.get('work') for item in source_record.get('works', []))
                         if isinstance(source_record.get('works'), list)
                         else {source_record.get('work')})
            require(name in contained, 'work/artifact identity mismatch: ' + str(name))

    fields = data.get('common_fourteen_fields')
    if not isinstance(fields, list) or len(fields) != 14 or not all(
            isinstance(field, dict) for field in fields):
        errors.append('14 common fields')
    else:
        ids = [field.get('id') for field in fields]
        require(len(set(ids)) == 14 and all(ids), '14 unique field IDs')
        for field in fields:
            refs = field.get('source_artifacts')
            require(bool(field.get('label')) and bool(field.get('qualitative_conclusion')) and
                    isinstance(refs, list) and bool(refs) and
                    all(ref in ARTIFACT_SOURCES for ref in refs),
                    '14-field evidence links')

    rules = data.get('common_rule_candidates')
    if not isinstance(rules, list) or len(rules) != 6 or not all(
            isinstance(rule, dict) for rule in rules):
        errors.append('six cross-work candidates')
    else:
        ids = [rule.get('id') for rule in rules]
        require(len(set(ids)) == 6 and all(ids), 'six unique candidate IDs')
        for rule in rules:
            evidence = rule.get('evidence')
            if not isinstance(evidence, list):
                errors.append('candidate evidence absent')
                continue
            cited_works = {item.get('work') for item in evidence if isinstance(item, dict)}
            require(len(cited_works) >= 2 and cited_works <= expected_names and
                    all(isinstance(item, dict) and item.get('artifact') ==
                        work_artifacts.get(item.get('work')) and
                        type(item.get('chapter')) is int and 1 <= item['chapter'] <= 5 and
                        bool(item.get('address')) for item in evidence),
                    'candidate requires two linked works')

    blindspots = data.get('blindspot_gate')
    require(isinstance(blindspots, list) and len(blindspots) == 12 and
            all(isinstance(item, dict) for item in blindspots) and
            {item.get('id') for item in blindspots} == set(range(1, 13)) and
            all(item.get('topic') and item.get('finding') and item.get('status')
                for item in blindspots), 'twelve blind-spot entries')

    scope = data.get('reading_scope')
    if not isinstance(scope, dict):
        errors.append('reading scope absent')
    else:
        readings = ledger.get('readings', [])
        by_platform = Counter()
        work_platforms = defaultdict(set)
        for row in readings:
            identity = _identity(row.get('url'))
            platform = DOMAINS.get(identity[0]) if identity else None
            if platform is None:
                errors.append('unrecognized official reading platform')
                continue
            by_platform[platform] += 1
            work_platforms[row.get('work')].add(platform)
        chapter_counts = {platform: by_platform[platform] for platform in
                          ('Munpia', 'Ridi', 'KakaoPage', 'Joara', 'NaverSeries')}
        counted_works = Counter(next(iter(platforms)) for platforms in
                                work_platforms.values() if len(platforms) == 1)
        work_counts = {platform: counted_works[platform] for platform in
                       ('Munpia', 'Ridi', 'KakaoPage', 'Joara')}
        core = scope.get('core_first_twenty_works')
        counted_core = Counter(next(iter(work_platforms[name])) for name in core
                               if name in work_platforms and len(work_platforms[name]) == 1) \
            if isinstance(core, list) else Counter()
        core_counts = {platform: counted_core[platform] for platform in
                       ('Munpia', 'Ridi', 'Joara', 'KakaoPage')}
        require(len(readings) == 110 and
                len({(row.get('work'), row.get('chapter')) for row in readings}) == 110 and
                len(work_platforms) == 10 and
                all(len(platforms) == 1 for platforms in work_platforms.values()) and
                scope.get('P2_revised_actual_readings') == 110 and
                scope.get('P2_revised_target') == 110 and
                scope.get('first_five_works_read') == 10 and
                scope.get('chapter_platform_distribution') == chapter_counts and
                scope.get('work_platform_distribution') == work_counts and
                isinstance(core, list) and len(core) == 4 and len(set(core)) == 4 and
                all(sum(row.get('work') == name for row in readings) >= 20 for name in core) and
                scope.get('core_platform_distribution') == core_counts,
                '110-reading/platform distribution')
        debt = scope.get('original_plan_debt')
        require(scope.get('original_plan_readings') == 95 and
                scope.get('original_plan_target') == 110 and
                isinstance(debt, dict) and debt.get('work') == '데뷔 못 하면 죽는 병 걸림' and
                debt.get('chapters') == [6, 20] and debt.get('count') == 15 and
                debt.get('status') == 'AUTH_REQUIRED' and
                debt.get('substituted_core_scope_is_not_original_reading') is True and
                95 + 15 == 110,
                'original-plan access debt 15')
    return errors


def audit(root=ROOT):
    data = json.loads((root / SOURCE).read_text(encoding='utf-8'))
    errors = validate(data, root)
    return {'PASS': not errors, 'errors': errors,
            'ten_work_synthesis_structurally_verified': not errors,
            'whole_P3_final': False, 'FULL_TEXT_FINAL': False,
            'G11_final': False, 'author_locked': False,
            'manuscript_allowed': False,
            'scope': 'REFERENCE_LINKS_AND_COUNTS_NOT_NUMERIC_ESTIMATION_OR_SEMANTIC_AUTHENTICATION'}


if __name__ == '__main__':
    report = audit()
    print(json.dumps(report, ensure_ascii=False))
    raise SystemExit(not report['PASS'])
