"""Reproduce P2 observation references; never certify novel-body or P3 quality."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODING = 'research/G11_RECORDED_FUNCTION_CODING_2026_10_01.json'
LEDGER = 'research/STYLE_READING_OBSERVATIONS.json'
POPULARITY = 'research/G11_POPULARITY_PROVENANCE_2026_10_01.json'
VOICE = 'research/G11_RIDI_CONTEXTUAL_VOICE_PILOT_2026_10_01.json'
NULL_FIELDS = ('central_event', 'reward_classification', 'retrospective_scene',
               'first_paragraph_new_information', 'first_1000_character_density',
               'sentence_length_distribution', 'voice_category_counts',
               'voice_character_shares', 'first_named_entity_positions')


def record_hash(row):
    return sha256(json.dumps(row, ensure_ascii=False, sort_keys=True,
                             separators=(',', ':')).encode()).hexdigest()


def audit(data, ledger, popularity):
    errors = []
    for key in ('whole_P3_final', 'sample_gate_complete', 'G11_final',
                'author_locked', 'manuscript_allowed', 'raw_novel_text_retained',
                'evidence_semantic_authentication_by_checker'):
        if data.get(key) is not False:
            errors.append('forbidden promotion: ' + key)
    if data.get('stage') != 'RECORDED_P2_FUNCTION_RECODING':
        errors.append('scope is not recorded-observation recoding')
    if data.get('readings_added') != 0 or data.get('actual_episode_packs') != 0:
        errors.append('recoding cannot create readings or episode packs')
    if data.get('missing_is_not_absent') is not True:
        errors.append('missing observations cannot prove absence')
    codes = set(data['functions'])
    if codes != {'SC', 'AE', 'SP', 'IR', 'EA', 'CT'}:
        errors.append('function coverage mismatch')
    expected = {i for i, r in enumerate(ledger['readings']) if r['chapter'] <= 5}
    seen = set()
    summary = {c: dict(chapter_records_supporting=0, works_supporting=set()) for c in codes}
    for row in data['rows']:
        index = row.get('reading_index')
        if type(index) is not int or index not in expected:
            errors.append('unsupported source record')
            continue
        if index in seen:
            errors.append('duplicate source record')
        seen.add(index)
        source = ledger['readings'][index]
        if (row['work'], row['chapter'], row['official_url']) != (
                source['work'], source['chapter'], source['url']):
            errors.append('source identity mismatch')
        if row['record_sha256'] != record_hash(source):
            errors.append('source observation changed')
        if any(k not in row or row[k] is not None for k in NULL_FIELDS):
            errors.append('unmeasured or unrecorded field populated')
        if set(row['cells']) != codes:
            errors.append('missing function cell')
        for code, cell in row['cells'].items():
            indexes = cell['observation_indexes']
            valid = (len(set(indexes)) == len(indexes) and all(
                type(i) is int and 0 <= i < len(source['observations']) for i in indexes))
            if not valid:
                errors.append('invalid observation reference')
            status = 'SUPPORTED_BY_RECORDED_OBSERVATION' if indexes else 'NOT_RECORDED'
            if cell['status'] != status:
                errors.append('missing observation reclassified as absence or support')
            if indexes and code in summary:
                summary[code]['chapter_records_supporting'] += 1
                summary[code]['works_supporting'].add(row['work'])
    if seen != expected or len(data['rows']) != 50 or data.get('row_count') != 50:
        errors.append('first-five record coverage mismatch')
    if data.get('function_cell_count') != 50 * len(codes):
        errors.append('function-cell denominator mismatch')
    for code, value in summary.items():
        value['works_supporting'] = sorted(value['works_supporting'])
        value['candidate_status'] = ('RECORDED_CROSS_WORK_CANDIDATE'
                                     if len(value['works_supporting']) >= 2
                                     else 'HOLD_LESS_THAN_TWO_WORKS')
        if value != data['cross_work_summary'].get(code):
            errors.append('cross-work support count mismatch')
    works = popularity['works']
    counts = Counter(r['work'] for r in works)
    if set(counts) != {r['work'] for r in data['rows']} or any(n != 1 for n in counts.values()):
        errors.append('popularity works differ from body sample')
    pairs = sum(r['status'] == 'TWO_KINDS_RECONCILED_NOT_FINAL_SAMPLE' for r in works)
    debts = sum(bool(r.get('metric_definition_hold')) for r in works)
    if pairs != popularity.get('two_kinds_reconciled') or pairs != 10:
        errors.append('declared official evidence pairs mismatch')
    if (popularity.get('remaining_primary_pair_holds') != len(works) - pairs
            or popularity.get('legacy_metric_definition_holds') != debts
            or popularity.get('remaining_provenance_or_metric_definition_holds') != debts):
        errors.append('unused counter debts confused with evidence-pair denominator')
    for key in ('sample_selection_final', 'whole_P3_final', 'G11_final',
                'author_locked', 'manuscript_allowed'):
        if popularity.get(key) is not False:
            errors.append('popularity cannot promote gates: ' + key)
    return errors


def audit_voice(data):
    """Check supplied metrics, not the manual context classification."""
    errors = []
    for key in ('whole_P3_final', 'G11_final', 'manuscript_allowed',
                'raw_novel_text_retained', 'checker_authenticates_browser_capture'):
        if data.get(key) is not False:
            errors.append('voice pilot cannot promote or authenticate: ' + key)
    if data.get('readings_added') != 0 or data.get('body_reinspected_chapters') != 1:
        errors.append('voice pilot is one reinspection, not new reading')
    if data.get('url') != 'https://ridibooks.com/books/2065016312/view':
        errors.append('voice pilot identity mismatch')
    if data['first_pass'] != data['second_pass']:
        errors.append('voice two-pass metrics disagree')
    for p in (data['first_pass'], data['second_pass']):
        canon = {k: v for k, v in p.items() if k != 'canonical_sha256'}
        digest = sha256(json.dumps(canon, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
        if digest != p['canonical_sha256']:
            errors.append('voice canonical metric hash mismatch')
        if (p['body_utf16_including_separators'] != p['paragraph_utf16_denominator']
                + 2 * (p['nonempty_body_p'] - 1)):
            errors.append('voice denominator confused with join separators')
        seen, units = set(), p['other_units']
        for channel in p['channels'].values():
            indexes = channel['raw_p_indexes']
            if len(set(indexes)) != len(indexes) or seen.intersection(indexes):
                errors.append('voice classification units overlap')
            seen.update(indexes)
            units += channel['paragraph_units']
            if channel['paragraph_units'] != len(indexes):
                errors.append('voice paragraph count mismatch')
            share = channel['utf16_characters'] / p['paragraph_utf16_denominator']
            if abs(share - channel['paragraph_character_share']) > 1e-12:
                errors.append('voice character share mismatch')
        if units != p['nonempty_body_p']:
            errors.append('voice classified and other unit count mismatch')
    return errors


def main():
    load = lambda p: json.loads((ROOT / p).read_text(encoding='utf-8'))
    data, ledger, popularity = load(CODING), load(LEDGER), load(POPULARITY)
    errors = audit(data, ledger, popularity) + audit_voice(load(VOICE))
    report = dict(status='FAIL' if errors else 'PASS',
                  scope='RECORDED_REFERENCES_HASHES_COVERAGE_AND_COUNTS_ONLY',
                  errors=errors, observation_records=50, function_cells=300,
                  novel_body_authenticated=False, semantic_classification_authenticated=False,
                  readings_added=0, whole_P3_final=False, sample_gate_complete=False,
                  G11_final=False, actual_episode_packs=0, manuscript_allowed=False)
    report['voice_component_reproduced_chapters'] = 1
    report['voice_semantic_classification_independently_verified'] = False
    (ROOT / 'reviews/G11_FUNCTION_CODING_REPORT.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
