"""Validate supplied voice metrics and reference continuity, not novel semantics."""
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COHORT = 'research/G11_RIDI_CONTEXTUAL_VOICE_FIRST_FIVE_2026_10_01.json'
PILOT = 'research/G11_RIDI_CONTEXTUAL_VOICE_PILOT_2026_10_01.json'
STRUCTURAL = 'research/G11_RIDI_STRUCTURAL_MEASUREMENTS_2026_10_01.json'
LEDGER = 'research/STYLE_READING_OBSERVATIONS.json'


def metric_hash(metric):
    payload = {k: v for k, v in metric.items() if k != 'canonical_sha256'}
    return sha256(json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def audit(data, pilot, structural, ledger):
    errors = []
    for key in ('whole_P3_final', 'sample_gate_complete', 'G11_final', 'author_locked',
                'manuscript_allowed', 'raw_novel_text_retained',
                'independent_semantic_reclassification', 'checker_authenticates_browser_capture',
                'raw_body_upload_to_other_models'):
        if data.get(key) is not False:
            errors.append('forbidden promotion: ' + key)
    counts = dict(readings_added=0, body_reinspected_chapters_this_batch=4,
                  inherited_voice_component_chapters=1, cumulative_voice_component_chapters=5,
                  planned_first_five_coding_chapters=50, remaining_voice_component_chapters=45)
    if any(data.get(k) != v for k, v in counts.items()):
        errors.append('coverage or reading denominator mismatch')
    if data.get('inherited_pilot_path') != PILOT or data.get('inherited_pilot_canonical_sha256') != pilot['first_pass']['canonical_sha256']:
        errors.append('inherited pilot mismatch')
    if data.get('captures_order') != [2, 3, 4, 5, 2, 3, 4, 5]:
        errors.append('capture sequence mismatch')
    originals = {r['chapter']: r['first_pass'] for r in structural['measurements']}
    source_ids = {(r['work'], r['chapter'], r['url']) for r in ledger['readings']}
    records = data['records']
    if len(records) != 4 or {r['chapter'] for r in records} != {2, 3, 4, 5}:
        errors.append('added chapter coverage mismatch')
    for row in records:
        n = row['chapter']
        if (data['work'], n, row['url']) not in source_ids or n not in originals:
            errors.append('chapter identity not in recorded sample')
            continue
        m, old = row['metric'], originals[n]
        if row['url'] != old['url'] or m['title'] != old['title_line']:
            errors.append('official episode identity mismatch')
        pairs = [('body_sha256', 'body_sha256'),
                 ('raw_viewer_sha256', 'viewer_sha256'),
                 ('body_utf16_including_separators', 'body_characters'),
                 ('raw_viewer_utf16', 'viewer_characters'),
                 ('nonempty_body_p', 'nonempty_body_paragraphs')]
        if any(m[a] != old[b] for a, b in pairs) or m['first1000_sha256'] != old['segment_sha256']['start']:
            errors.append('body differs from structural evidence')
        if metric_hash(m) != m['canonical_sha256']:
            errors.append('canonical hash mismatch')
        captures = row['captures']
        if (len(captures) != 2 or [c['pass'] for c in captures] != [1, 2]
                or any(c['canonical_sha256'] != m['canonical_sha256'] for c in captures)
                or captures[-1]['intervening_chapter'] != (5 if n == 2 else n - 1)):
            errors.append('two separate capture declarations disagree')
        body = m['body_raw_p_indexes']
        if (len(body) != m['nonempty_body_p'] or len(set(body)) != len(body)
                or body != sorted(body) or any(type(i) is not int or i <= 0 for i in body)):
            errors.append('body paragraph identities invalid')
        den = m['paragraph_utf16_denominator']
        if den <= 0 or m['body_utf16_including_separators'] != den + 2 * (m['nonempty_body_p'] - 1):
            errors.append('join separator denominator mismatch')
        units, chars, seen = m['other_units'], m['other_utf16_characters'], set()
        for ch in m['channels'].values():
            ids = ch['raw_p_indexes']
            if len(set(ids)) != len(ids) or not set(ids).issubset(body) or seen.intersection(ids):
                errors.append('channel paragraph identity or overlap error')
            seen.update(ids)
            units += ch['paragraph_units']
            chars += ch['utf16_characters']
            if ch['paragraph_units'] != len(ids) or ch['utf16_characters'] < 0:
                errors.append('channel unit mismatch')
            if (not ids and ch['utf16_characters'] != 0) or abs(ch['paragraph_character_share'] - ch['utf16_characters'] / den) > 1e-12:
                errors.append('channel character share mismatch')
        if units != len(body) or chars != den:
            errors.append('classified and remaining totals disagree')
        ui = m['channels']['UI_SYSTEM']['raw_p_indexes']
        blocks = sum(i == 0 or p != ui[i - 1] + 1 for i, p in enumerate(ui))
        if blocks != m['ui_contiguous_blocks']:
            errors.append('UI contiguous group count mismatch')
        obs = row['semantic_observations']
        if not set(obs['unquoted_thought_witness_raw_p']).issubset(body):
            errors.append('unquoted thought witness outside body')
        for key in ('total_inner_share', 'first_paragraph_new_information',
                    'first1000_event_density', 'sentence_distribution',
                    'all_action_explanation_inner_order', 'all_named_entity_first_positions'):
            if obs.get(key, 'missing') is not None:
                errors.append('unmeasured semantic or P3 field populated')
        if obs.get('complete_retrospective_boundary_coding') is not False:
            errors.append('partial scene coding promoted')
    return errors


def main():
    load = lambda p: json.loads((ROOT / p).read_text(encoding='utf-8'))
    errors = audit(*[load(p) for p in (COHORT, PILOT, STRUCTURAL, LEDGER)])
    report = dict(status='FAIL' if errors else 'PASS', errors=errors,
                  scope='SUPPLIED_METRICS_AND_REFERENCE_CONTINUITY_ONLY',
                  readings_added=0, added_reinspections=4, cumulative_voice_components=5,
                  remaining_voice_components=45, novel_body_authenticated=False,
                  semantic_classification_authenticated=False, whole_P3_final=False,
                  G11_final=False, manuscript_allowed=False)
    (ROOT / 'reviews/G11_VOICE_COHORT_REPORT.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
