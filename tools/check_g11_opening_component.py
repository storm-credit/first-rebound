"""Validate derivative opening references and arithmetic; never authenticate semantics."""
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = 'research/G11_RIDI_OPENING_BOUNDARY_COMPONENT_2026_10_01.json'
STRUCTURAL = 'research/G11_RIDI_STRUCTURAL_MEASUREMENTS_2026_10_01.json'
LEDGER = 'research/STYLE_READING_OBSERVATIONS.json'


def metric_hash(m):
    payload = {k: v for k, v in m.items() if k != 'canonical_sha256'}
    return sha256(json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def audit(data, structural, ledger):
    errors = []
    for key in ('whole_P3_final', 'sample_gate_complete', 'G11_final', 'author_locked',
                'manuscript_allowed', 'raw_novel_text_retained', 'raw_novel_text_uploaded',
                'checker_authenticates_browser_capture', 'checker_authenticates_semantics'):
        if data.get(key) is not False:
            errors.append('forbidden promotion: ' + key)
    expected_counts = dict(readings_added=0, body_reinspected_chapters_this_batch=5,
                           opening_component_chapters=5, remaining_opening_component_chapters=45,
                           voice_component_chapters_unchanged=5, component_denominator=50)
    if any(data.get(k) != v for k, v in expected_counts.items()):
        errors.append('coverage denominator or new-reading mismatch')
    if data.get('browser_capture_sequence') != [1, 2, 3, 4, 5] * 2:
        errors.append('capture sequence mismatch')
    source_ids = {(r['work'], r['chapter'], r['url']) for r in ledger['readings']}
    old = {r['chapter']: r['first_pass'] for r in structural['measurements']}
    if len(data['records']) != 5 or {r['chapter'] for r in data['records']} != {1, 2, 3, 4, 5}:
        errors.append('chapter coverage mismatch')
    for row in data['records']:
        n, m = row['chapter'], row['metric']
        if n not in old or (data['work'], n, row['url']) not in source_ids:
            errors.append('unsupported source identity')
            continue
        prior = old[n]
        pairs = [('title', 'title_line'), ('body_sha256', 'body_sha256'),
                 ('raw_viewer_sha256', 'viewer_sha256'), ('body_utf16', 'body_characters'),
                 ('viewer_utf16', 'viewer_characters'), ('nonempty_body_p', 'nonempty_body_paragraphs')]
        if row['url'] != prior['url'] or any(m[a] != prior[b] for a, b in pairs):
            errors.append('structural identity or body mismatch')
        if m['first1000_sha256'] != prior['segment_sha256']['start']:
            errors.append('opening-window identity mismatch')
        if metric_hash(m) != m['canonical_sha256']:
            errors.append('canonical metric hash mismatch')
        c = row['captures']
        if (len(c) != 2 or [v['pass'] for v in c] != [1, 2]
                or any(v['canonical_sha256'] != m['canonical_sha256'] for v in c)
                or c[-1]['intervening_chapter'] != (5 if n == 1 else n - 1)):
            errors.append('separate capture mismatch')
        if m['linguistic_sentence_count'] is not None:
            errors.append('boundary proxy promoted to linguistic sentence count')
        if m['body_utf16'] != m['paragraph_character_denominator'] + 2 * (m['nonempty_body_p'] - 1):
            errors.append('paragraph join denominator mismatch')
        lengths = []
        for length, count in m['boundary_span_length_histogram'].items():
            if int(length) <= 0 or type(count) is not int or count <= 0:
                errors.append('invalid span histogram')
                continue
            lengths.extend([int(length)] * count)
        lengths.sort()
        if not lengths:
            errors.append('empty boundary distribution')
            continue
        stats = dict(min=lengths[0], p10=lengths[int((len(lengths) - 1) * .1)],
                     median=lengths[int((len(lengths) - 1) * .5)],
                     p90=lengths[int((len(lengths) - 1) * .9)], max=lengths[-1])
        if (len(lengths) != m['boundary_span_count'] or stats != m['boundary_span_percentiles']
                or sum(m['boundary_spans_by_existing_voice_channel'].values()) != len(lengths)
                or sum(lengths) > m['paragraph_character_denominator']):
            errors.append('boundary count, quantile or character denominator mismatch')
        locations = m['prefix_paragraph_intersections']
        seen, cursor = set(), 0
        for p in locations:
            i, s, size = p['raw_p_index'], p['start_utf16'], p['length_utf16']
            if i in seen or i <= 0 or s != cursor or not 0 <= s < 1000 or size <= 0:
                errors.append('prefix paragraph identity or continuity error')
            seen.add(i)
            cursor = s + size + 2
            if p['covered_utf16'] != min(size, 1000 - s) or p['complete'] != (s + size <= 1000):
                errors.append('truncated paragraph mismatch')
        if (not locations or m['first_body_p'] != {k: locations[0][k] for k in ('raw_p_index', 'start_utf16', 'length_utf16')}
                or cursor <= 1000
                or sum(p['covered_utf16'] for p in locations) + row['first1000_join_separator_units'] != 1000):
            errors.append('first-p or prefix denominator mismatch')
        obs = row['semantic_observations']
        if any(v['raw_p_index'] != m['first_body_p']['raw_p_index']
               for v in obs['first_paragraph_information_units']):
            errors.append('first-p coding belongs to another paragraph')
        for list_key, count_key in (
                ('first_paragraph_information_units', 'first_paragraph_information_unit_count'),
                ('first1000_action_groups', 'first1000_action_group_count'),
                ('first1000_person_referent_groups', 'first1000_person_referent_group_count'),
                ('first1000_setting_explanation_groups', 'first1000_setting_group_count')):
            if len(obs[list_key]) != obs[count_key]:
                errors.append('local coding count mismatch')
        groups = (obs['first1000_action_groups'] + obs['first1000_person_referent_groups']
                  + obs['first1000_setting_explanation_groups'] + obs['first1000_intentions_not_executed'])
        by_id = {p['raw_p_index']: p for p in locations}
        for group in groups:
            if not group['raw_p_indexes'] or not set(group['raw_p_indexes']).issubset(seen):
                errors.append('coding group outside prefix')
            elif 'contains_truncated_paragraph' in group and group['contains_truncated_paragraph'] != any(
                    not by_id[i]['complete'] for i in group['raw_p_indexes']):
                errors.append('semantic group cutoff declaration mismatch')
        for key in ('distinct_human_count', 'whole_chapter_action_explanation_inner_sequence',
                    'all_named_entity_first_positions'):
            if obs.get(key, 'missing') is not None:
                errors.append('unmeasured complete semantics populated')
        for key in ('selected_groups_are_exhaustive_semantic_inventory', 'independent_semantic_authentication',
                    'full_P3_complete'):
            if obs.get(key) is not False:
                errors.append('local coding promoted')
        for term in row['selected_literal_surface_positions']:
            full, prefix = term['full_body_first_utf16'], term['first_prefix_utf16']
            if full is not None and (type(full) is not int or not 0 <= full < m['body_utf16']):
                errors.append('literal position outside body')
            expected = full if full is not None and full + len(term['surface']) <= 1000 else None
            if prefix != expected:
                errors.append('prefix absence confused with full-body match')
    return errors


def main():
    load = lambda p: json.loads((ROOT / p).read_text(encoding='utf-8'))
    errors = audit(*[load(p) for p in (DATA, STRUCTURAL, LEDGER)])
    report = dict(status='FAIL' if errors else 'PASS', errors=errors,
                  scope='SUPPLIED_DERIVATIVE_METRICS_REFERENCES_AND_COUNTS_ONLY',
                  opening_component_chapters=5, remaining_component_chapters=45,
                  readings_added=0, linguistic_sentence_count_authenticated=False,
                  novel_body_authenticated=False, semantic_authentication=False,
                  whole_P3_final=False, G11_final=False, manuscript_allowed=False)
    (ROOT / 'reviews/G11_OPENING_COMPONENT_REPORT.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
