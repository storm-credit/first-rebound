"""Audit G11 minimum records' provenance and arithmetic, never novel meaning."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD_FILES = (
    'research/G11_SGRADE_COMMON_MINIMUM_2026_10_02.json',
    'research/G11_BUSINESS_COMMON_MINIMUM_2026_10_02.json',
    'research/G11_EXTRA_COMMON_MINIMUM_2026_10_02.json',
)
SGRADE_MD = 'research/G11_SGRADE_COMMON_MINIMUM_2026_10_02.md'
SHA = re.compile(r'^[0-9a-f]{64}$')
FALSE_FLAGS = (
    'whole_P3_final', 'G11_final', 'author_locked', 'season_selected',
    'manuscript_allowed', 'raw_novel_text_retained', 'raw_novel_text_uploaded',
    'independent_semantic_authentication',
)


def normalized_sha(path):
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def _source_for(work, sources):
    if work == '내가 키운 S급들':
        for source in sources.values():
            if (isinstance(source, dict) and source.get('work') == work
                    and source.get('records') and 'prefix_paragraph_intersections' in source['records'][0].get('metric', {})):
                return source
    for source in sources.values():
        if isinstance(source, dict) and source.get('work') == work and isinstance(source.get('metrics'), list):
            return source
    return None


def _prefix_from_source(source, chapter):
    if not source:
        return None
    if 'records' in source:
        matches = [r for r in source['records'] if r.get('chapter') == chapter]
        if matches:
            return matches[0]
    if 'metrics' in source:
        matches = [r for r in source['metrics'] if r.get('chapter') == chapter]
        if matches:
            return matches[0]
    return None


def _fourteen_fields(record, root):
    fields = record.get('minimum_comparison_fields', record.get('common_fourteen_fields'))
    if isinstance(fields, list):
        names = [f.get('item', f.get('id')) for f in fields]
        return len(fields) == 14 and len(set(names)) == 14 and all(
            name and f.get('status') and (f.get('scope') or f.get('scoped_observation'))
            and (f.get('evidence_path') or f.get('label')) for name, f in zip(names, fields)
        )
    if record.get('work') != '내가 키운 S급들':
        return False
    md = (root / SGRADE_MD).read_text(encoding='utf-8')
    section = md.split('## 공통 §4/5/5.1의 같은 비교 칸', 1)
    if len(section) != 2:
        return False
    table = section[1].split('\n## ', 1)[0]
    rows = [line for line in table.splitlines() if line.startswith('|') and not line.startswith('|---')]
    return len(rows) - 1 == 14


def _raw_text_embedded(value):
    if isinstance(value, dict):
        if any(k in value for k in ('raw_novel_text', 'novel_body_text', 'full_body_text', 'raw_body_text')):
            return True
        return any(_raw_text_embedded(v) for v in value.values())
    if isinstance(value, list):
        return any(_raw_text_embedded(v) for v in value)
    return isinstance(value, str) and len(value) > 1200


def _tag_indexes(tag):
    for key in ('raw_p_indexes', 'raw_FONT_indexes', 'raw_font_indexes'):
        if key in tag:
            return tag[key]
    return []


def validate(record, root=ROOT, ledger=None):
    """Return machine-checkable defects; a clean result cannot certify interpretation."""
    errors = []
    work = record.get('work')
    if not isinstance(work, str) or not work:
        errors.append('work identity')
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            errors.append('scope promotion: ' + flag)
    if record.get('checker_authenticates_semantics') is True:
        errors.append('scope promotion: checker_authenticates_semantics')
    if record.get('new_unique_readings') != 0 or record.get('actual_episode_packs') != 0:
        errors.append('reading/pack inflation')
    if record.get('minimum_comparison_record_ready') is not True or record.get('minimum_work_records_target') != 10:
        errors.append('minimum record scope')
    if _raw_text_embedded(record):
        errors.append('raw novel text payload')
    if not _fourteen_fields(record, root):
        errors.append('14-item minimum checklist')
    rubric = record.get('first1000_rubric', {})
    if rubric.get('all_tags_nonexclusive') is not True or rubric.get('fractions_must_not_be_summed') is not True:
        errors.append('prefix proxy boundary')
    hash_method = record.get('source_hash_method', '')
    if 'CRLF' not in hash_method or 'LF' not in hash_method:
        errors.append('source normalization proof')

    sources = {}
    source_hashes = record.get('source_hashes')
    if not isinstance(source_hashes, dict) or not source_hashes:
        errors.append('source hashes absent')
    else:
        for rel, digest in source_hashes.items():
            path = (root / rel).resolve()
            if not rel.startswith('research/') or not path.is_relative_to(root.resolve()) or not path.is_file() or not SHA.fullmatch(str(digest)):
                errors.append('source path/hash invalid')
                continue
            if normalized_sha(path) != digest:
                errors.append('source content changed')
            if path.suffix == '.json':
                sources[rel] = json.loads(path.read_text(encoding='utf-8'))
    source = _source_for(work, sources)
    if source is None:
        errors.append('source identity unavailable')

    records = record.get('records', [])
    if not isinstance(records, list) or len(records) != 5 or [r.get('chapter') for r in records] != [1, 2, 3, 4, 5]:
        errors.append('five unique chapters')
        return errors
    if ledger is None:
        ledger = json.loads((root / 'research/STYLE_READING_OBSERVATIONS.json').read_text(encoding='utf-8'))
    ledger_keys = {(r.get('work'), r.get('chapter'), r.get('url')) for r in ledger['readings']}

    for rec in records:
        chapter = rec['chapter']
        source_rec = _prefix_from_source(source, chapter)
        if source_rec is None:
            errors.append('source chapter missing')
            continue
        metric = source_rec.get('metric', source_rec)
        if rec.get('url') != source_rec.get('url') or rec.get('body_sha256') != metric.get('body_sha256'):
            errors.append('official identity/hash mismatch')
        source_prefix_sha = metric.get('first1000_sha256')
        if source_prefix_sha and rec.get('first1000_sha256') != source_prefix_sha:
            errors.append('official prefix hash mismatch')
        if (work, chapter, rec.get('url')) not in ledger_keys:
            errors.append('reading ledger identity mismatch')
        if not SHA.fullmatch(str(rec.get('body_sha256'))) or not SHA.fullmatch(str(rec.get('first1000_sha256'))):
            errors.append('body/prefix hash format')
        if rec.get('fresh_body_match') is not True:
            errors.append('fresh body proof absent')
        if 'fresh_first1000_match' in rec and rec['fresh_first1000_match'] is not True:
            errors.append('fresh prefix proof absent')
        meta = (rec.get('prefix_intersections') if work == '소설 속 엑스트라'
                else rec.get('prefix_intersection_metadata'))
        if meta is None:
            meta = metric.get('prefix_paragraph_intersections')
        if not isinstance(meta, list) or not meta:
            errors.append('prefix intersection metadata absent')
            continue
        if work == '소설 속 엑스트라' and rec.get('prefix_intersection_metadata') is not None:
            simple = rec['prefix_intersection_metadata']
            if len(simple) != len(meta) or any(
                a.get('raw_FONT_index') != b.get('raw_font_index')
                or a.get('body_start_utf16') != b.get('start_utf16')
                or a.get('full_display_block_utf16') != b.get('full_length_utf16')
                or a.get('covered_utf16') != b.get('covered_utf16')
                for a, b in zip(meta, simple)
            ):
                errors.append('prefix aliases disagree')
        index_key = next((key for key in ('raw_p_index', 'raw_FONT_index', 'raw_font_index') if key in meta[0]), None)
        if index_key is None:
            errors.append('prefix metadata invalid')
            continue
        indexes = [p.get(index_key) for p in meta]
        sizes = {p.get(index_key): p.get('covered_utf16') for p in meta}
        if len(indexes) != len(set(indexes)) or any(not isinstance(n, int) or n <= 0 for n in sizes.values()):
            errors.append('prefix metadata invalid')
        den = sum(n for n in sizes.values() if isinstance(n, int))
        if (rec.get('prefix_nonempty_intersections') != len(meta) or rec.get('prefix_text_utf16_without_join') != den
                or rec.get('prefix_join_utf16') != 1000 - den):
            errors.append('prefix denominator mismatch')
        if rec.get('prefix_intersection_metadata') is not None or rec.get('prefix_intersections') is not None:
            full_key = 'full_display_block_utf16' if 'full_display_block_utf16' in meta[0] else 'full_length_utf16'
            start_key = 'body_start_utf16' if 'body_start_utf16' in meta[0] else 'start_utf16'
            if any(p.get('covered_utf16', 0) > p.get(full_key, 0)
                   or ('complete' in p and p['complete'] != (p.get('covered_utf16') == p.get(full_key))) for p in meta):
                errors.append('prefix clipping metadata')
            starts = [p.get(start_key) for p in meta]
            if (starts[0] != 0 or any(not isinstance(x, int) for x in starts)
                    or any(starts[i + 1] != starts[i] + meta[i].get(full_key, 0) + 2
                           for i in range(len(meta) - 1))
                    or starts[-1] + meta[-1].get('covered_utf16', 0) not in (998, 999, 1000)):
                errors.append('prefix offset/coverage mismatch')
            paragraph_lengths = dict(metric.get('paragraph_meta', []))
            if paragraph_lengths and any(paragraph_lengths.get(p.get('legacy_raw_FONT_index', p.get('legacy_raw_font_index', p.get(index_key)))) != p.get(full_key) for p in meta):
                errors.append('prefix source paragraph length mismatch')
        tags = rec.get('first1000_all_display_blocks_coded', [])
        tagged = set()
        functions = set()
        for tag in tags:
            function = tag.get('function')
            inds = _tag_indexes(tag)
            if any(tag[key] != inds for key in ('raw_p_indexes', 'raw_FONT_indexes', 'raw_font_indexes') if key in tag):
                errors.append('prefix label alias mismatch')
            if function not in {'A', 'E', 'I', 'F'} or function in functions or len(inds) != len(set(inds)) or not set(inds) <= set(indexes):
                errors.append('prefix labels invalid')
                continue
            functions.add(function)
            tagged.update(inds)
            units = sum(sizes[i] for i in inds)
            if (tag.get('display_blocks') != len(inds) or tag.get('covered_utf16') != units
                    or tag.get('display_block_presence_fraction') != round(len(inds) / len(meta), 6)
                    or tag.get('text_presence_fraction') != round(units / den, 6)):
                errors.append('tag arithmetic mismatch')
        if tagged != set(indexes):
            errors.append('unmapped prefix block')
        if not {'A', 'E', 'I'} <= functions:
            errors.append('core prefix labels missing')
        fragment = next((set(_tag_indexes(t)) for t in tags if t.get('function') == 'F'), set())
        meaningful = set().union(*(set(_tag_indexes(t)) for t in tags if t.get('function') in {'A', 'E', 'I'}))
        if fragment & meaningful:
            errors.append('unassignable fragment overlaps meaningful label')
        if rec.get('distinct_human_count') is not None or rec.get('linguistic_sentence_count') is not None:
            errors.append('proxy certified as linguistic fact')
        if not rec.get('past_scene') or not rec.get('central_event', source_rec.get('central_event')):
            # SGRADE stores central-event and reward narratives in its companion MD.
            if work != '내가 키운 S급들' or not rec.get('past_scene'):
                errors.append('chapter temporal/event record absent')

    scenes = record.get('minimum_scene_samples', [])
    kinds = {s.get('kind') for s in scenes}
    if not isinstance(scenes, list) or 'DIALOGUE' not in kinds or 'EXPOSITION' not in kinds or not any(str(k).startswith('PHYSICAL_') for k in kinds):
        errors.append('three minimum scene kinds')
    for scene in scenes:
        chapter = scene.get('chapter')
        if chapter not in range(1, 6) or scene.get('text_utf16', 0) <= 0 or scene.get('blocks', 0) <= 0 or not SHA.fullmatch(str(scene.get('region_sha256'))):
            errors.append('scene address/hash invalid')
        raw_p = scene.get('raw_p', scene.get('raw_FONT'))
        if not isinstance(raw_p, list) or len(raw_p) != 2 or not all(isinstance(n, int) for n in raw_p) or raw_p[0] > raw_p[1]:
            errors.append('scene paragraph address invalid')
        if scene.get('url') and chapter in range(1, 6) and scene['url'] != records[chapter - 1].get('url'):
            errors.append('scene chapter URL mismatch')
        stages = scene.get('observed_function_stages')
        if stages is not None:
            if scene.get('function_stages_count') != len(stages) or scene.get('local_proxy_stages_per_1000_utf16') != round(1000 * len(stages) / scene['text_utf16'], 6):
                errors.append('scene density proxy arithmetic')
    return errors


def audit(root=ROOT):
    errors = []
    works = []
    ready_paths = []
    ready_works = set()
    for rel in RECORD_FILES:
        path = root / rel
        if not path.is_file():
            errors.append('record missing: ' + rel)
            continue
        data = json.loads(path.read_text(encoding='utf-8'))
        works.append(data.get('work'))
        problems = validate(data, root)
        errors.extend(rel + ': ' + problem for problem in problems)
        if not problems:
            ready_paths.append(rel)
            ready_works.add(data.get('work'))
    if len(works) != len(set(works)):
        errors.append('duplicate work')
    return {'PASS': not errors, 'errors': errors, 'ready_works': len(ready_works),
            'record_sources': ready_paths, 'whole_P3_final': False, 'G11_final': False,
            'scope': 'RECORD_PROVENANCE_ADDRESS_ARITHMETIC_NOT_ORIGINAL_SEMANTICS'}


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False))
    raise SystemExit(not audit()['PASS'])
