"""Check the supplied full-body partition, not literary or semantic validity."""
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = 'research/G11_RIDI_FUNCTION_SEQUENCE_FIRST_FIVE_2026_10_01.json'
STRUCTURAL = 'research/G11_RIDI_STRUCTURAL_MEASUREMENTS_2026_10_01.json'
LEDGER = 'research/STYLE_READING_OBSERVATIONS.json'


def metric_hash(metric):
    payload = {k: v for k, v in metric.items() if k != 'canonical_sha256'}
    return sha256(json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def audit(data, structural, ledger):
    errors = []
    for k in ('raw_novel_text_retained', 'raw_novel_text_uploaded',
              'checker_authenticates_browser_capture', 'checker_authenticates_semantics',
              'whole_P3_final', 'sample_gate_complete', 'G11_final', 'author_locked',
              'manuscript_allowed'):
        if data.get(k) is not False:
            errors.append('forbidden promotion: ' + k)
    counts = dict(readings_added=0, function_sequence_component_chapters=5,
                  remaining_function_sequence_component_chapters=45, component_denominator=50,
                  voice_component_chapters_unchanged=5, opening_component_chapters_unchanged=5,
                  whole_P3_completed_chapters=0, nonempty_body_p_partitioned=568, macro_block_count=54)
    if any(data.get(k) != v for k, v in counts.items()):
        errors.append('component, reading or partition denominator mismatch')
    if data.get('browser_capture_sequence') != [1, 2, 3, 4, 5] * 2:
        errors.append('capture order mismatch')
    rows = data['records']
    if len(rows) != 5 or [r['chapter'] for r in rows] != [1, 2, 3, 4, 5]:
        errors.append('chapter coverage mismatch')
    prior = {r['chapter']: r['first_pass'] for r in structural['measurements']}
    sources = {(r['work'], r['chapter'], r['url']) for r in ledger['readings']}
    total_p, total_blocks = 0, 0
    for row in rows:
        n, m = row['chapter'], row['first_capture']
        if n not in prior or (data['work'], n, m['url']) not in sources:
            errors.append('unrecorded official chapter')
            continue
        old, second = prior[n], row['second_capture']
        pairs = [('url', 'url'), ('document_title', 'document_title'), ('title_line', 'title_line'),
                 ('body_utf16', 'body_characters'), ('body_sha256', 'body_sha256'),
                 ('normalized_viewer_utf16', 'viewer_characters'),
                 ('normalized_viewer_sha256', 'viewer_sha256')]
        if any(m[a] != old[b] for a, b in pairs):
            errors.append('structural body or identity mismatch')
        if metric_hash(m) != m['canonical_sha256']:
            errors.append('numeric capture canonical mismatch')
        if (any(second[k] != m[k] for k in ('canonical_sha256', 'body_sha256',
                                          'normalized_viewer_sha256', 'raw_viewer_sha256'))
                or second['intervening_chapter'] != (5 if n == 1 else n - 1)):
            errors.append('separate second capture mismatch')
        meta = m['paragraph_meta']
        ids = [p[0] for p in meta]
        if (ids != sorted(set(ids)) or any(i <= 0 or size <= 0 for i, size in meta)
                or len(meta) != old['nonempty_body_paragraphs']
                or sum(p[1] for p in meta) + 2 * (len(meta) - 1) != m['body_utf16']):
            errors.append('paragraph metadata or join denominator mismatch')
        if m['raw_viewer_utf16'] - m['normalized_viewer_utf16'] != sum(m['viewer_zero_width_removed'].values()):
            errors.append('raw and normalized viewer units confused')
        total_p += len(meta)
        total_blocks += len(row['macro_blocks'])
        covered, block_ids = [], []
        for block in row['macro_blocks']:
            start, end = block['start_raw_p'], block['end_raw_p']
            block_ids.append(block['id'])
            subset = [i for i in ids if start <= i <= end]
            covered.extend(subset)
            if start not in ids or end not in ids or start > end or block['paragraph_count'] != len(subset):
                errors.append('block endpoints or count mismatch')
            anchors = block['anchors']
            apos = [a['raw_p_index'] for a in anchors]
            if not anchors or apos != sorted(apos) or not set(apos).issubset(subset):
                errors.append('function anchor outside block or out of order')
            for a in anchors:
                if not a['functions'] or len(a['functions']) != len(set(a['functions'])) or not set(a['functions']).issubset({'A', 'E', 'I'}):
                    errors.append('unknown or duplicate function tag')
        if covered != ids or len(block_ids) != len(set(block_ids)):
            errors.append('partition gap, overlap, order or duplicate block')
        if (row.get('functions_are_not_exclusive') is not True
                or any(row.get(k) is not False for k in ('whole_chapter_lexical_sequence_complete',
                       'independent_semantic_authentication', 'full_P3_complete'))
                or row.get('all_inner_character_share', 'missing') is not None):
            errors.append('macro anchors promoted to full lexical or inner measurement')
        story = row['story_observations']
        lists = [story['ending']['anchors']] + [item['anchors'] for key in (
            'visible_outcomes', 'information_rewards', 'premise_events', 'unexecuted') for item in story[key]]
        retro = story['retrospective']
        lists += [retro['selected_summary_anchors'], retro.get('future_knowledge_anchors', [])]
        if any(not set(points).issubset(ids) for points in lists):
            errors.append('story annotation outside observed body')
        if retro['complete_past_content_inventory'] is not False or retro['total_past_content_utf16'] is not None:
            errors.append('selected past markers promoted to full inventory')
        win = retro['memory_window']
        if win is not None:
            members = [i for i in ids if win['start_raw_p'] <= i <= win['end_raw_p']]
            parts = [win[k] for k in ('memory_voice_raw_p', 'past_reporter_raw_p', 'current_reaction_raw_p')]
            flattened = [i for group in parts for i in group]
            if (n != 1 or len(members) != 14 or len(parts[0]) != 10 or len(parts[1]) != 2 or len(parts[2]) != 2
                    or sorted(flattened) != members or len(flattened) != len(set(flattened))
                    or win['independent_past_scene'] is not False
                    or not win['trigger_raw_p'] < win['start_raw_p'] < win['end_raw_p'] < win['return_raw_p']
                    or not {win['trigger_raw_p'], win['return_raw_p']}.issubset(ids)):
                errors.append('embedded memory window and current reactions confused')
    if total_p != data['nonempty_body_p_partitioned'] or total_blocks != data['macro_block_count']:
        errors.append('aggregate partition count mismatch')
    return errors


def main():
    read = lambda p: json.loads((ROOT / p).read_text(encoding='utf-8'))
    errors = audit(*[read(p) for p in (DATA, STRUCTURAL, LEDGER)])
    report = dict(status='FAIL' if errors else 'PASS', errors=errors,
                  scope='SUPPLIED_CAPTURE_REFERENCES_AND_FULL_BODY_MACRO_PARTITION_ONLY',
                  body_p_partitioned=568, macro_blocks=54, component_chapters=5,
                  remaining_component_chapters=45, readings_added=0,
                  lexical_sequence_authenticated=False, semantic_authentication=False,
                  novel_body_authenticated=False, whole_P3_final=False, G11_final=False,
                  manuscript_allowed=False)
    (ROOT / 'reviews/G11_FUNCTION_SEQUENCE_COMPONENT_REPORT.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
