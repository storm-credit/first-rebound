"""Check supplied numeric references and scope; cannot certify term or narrative meaning."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA='research/G11_RIDI_INFORMATION_DELIVERY_FIRST_FIVE_2026_10_01.json'
BASE='research/G11_RIDI_FUNCTION_SEQUENCE_FIRST_FIVE_2026_10_01.json'

def audit(data, base):
    errors=[]
    forbidden=('raw_novel_text_retained','raw_novel_text_uploaded','complete_entity_inventory',
               'complete_term_inventory','complete_space_cause_inventory',
               'independent_original_semantic_review','universal_house_style_rule',
               'author_locked','manuscript_allowed','G11_final',
               'aliases_or_coreferences_resolved','literal_count_is_distinct_entity_count','lexical_counts_are_density')
    if any(data.get(k) is not False for k in forbidden):
        errors.append('unsupported promotion of substring or selected interpretation scope')
    if data.get('professional_action_density','missing') is not None:
        errors.append('unmeasured professional density')
    counts=dict(readings_added=0,unique_readings_unchanged=95,unread_chapters_unchanged=15,
                component_chapters=5,remaining_component_chapters=45,component_denominator=50,
                whole_P3_completed_chapters=0,actual_episode_packs=0)
    if any(data.get(k)!=v for k,v in counts.items()) or data.get('components_share_same_chapters') is not True:
        errors.append('same cohort counted as additional chapters or gate completion')
    if data.get('freeze')!='v0.30 PARTIAL' or data.get('gate')!='CLOSED':
        errors.append('freeze or gate promotion')
    if data.get('browser_capture_sequence')!=[1,2,3,4,5]*2:
        errors.append('capture sequence mismatch')
    if data.get('nested_matches_not_deduplicated') is not True:
        errors.append('literal overlap silently converted to distinct mentions')
    prior={r['chapter']:r['first_capture'] for r in base['records']}
    rows=data['records']
    if [r['chapter'] for r in rows]!=[1,2,3,4,5]:
        errors.append('cohort order or coverage mismatch')
    for r in rows:
        c=r['chapter']; p=prior[c]
        if (any(r[k]!=p[k] for k in ('url','document_title','body_sha256','body_utf16'))
                or r['body_p_count']!=len(p['paragraph_meta'])
                or r['second_capture']['body_sha256']!=r['body_sha256']
                or r['second_capture']['same_selected_literal_positions'] is not True
                or r['second_capture']['intervening_chapter']!=(5 if c==1 else c-1)):
            errors.append('supplied body reference or repeat declaration mismatch')
    terms=data['selected_terms']
    if (len(terms)!=data['selected_literal_count'] or len(terms)!=37
            or sum(t['selected_literal_match_count'] for t in terms)!=data['selected_literal_match_count']
            or data['selected_literal_match_count']!=174
            or len({t['id'] for t in terms})!=len(terms)
            or len({t['literal'] for t in terms})!=len(terms)):
        errors.append('selected query set or substring count inconsistent')
    for t in terms:
        f=t['first_in_cohort']; meta=dict(prior[f['chapter']]['paragraph_meta'])
        length=len(t['literal'].encode('utf-16-le'))//2
        if (f['raw_p_index'] not in meta or f['utf16_offset']<0
                or f['utf16_offset']+length>meta.get(f['raw_p_index'],0)
                or t['selected_literal_match_count']<=0):
            errors.append('first literal location outside supplied paragraph size')
    cases=data['selected_cases']
    if len(cases)!=17 or len({c['id'] for c in cases})!=17:
        errors.append('case index inconsistent')
    for c in cases:
        ids={p[0] for p in prior[c['chapter']]['paragraph_meta']}
        if (not c['anchors'] or c['anchors']!=sorted(set(c['anchors'])) or not set(c['anchors']).issubset(ids)
                or c['interpretation_status']!='INFERENCE' or not c['boundary']):
            errors.append('case anchors outside body or interpretation promoted')
    expected={'X01':('NESTED_MATCH',{'T06','T18'}),
              'X02':('HOMOGRAPH_IN_COMPOUND',{'T16'}),
              'X03':('DIFFERENT_LITERAL_RELATED_LABEL',{'T07','T28'})}
    supplied={x['id']:(x['kind'],set(x['term_ids'])) for x in data['exceptions']}
    if supplied!=expected:
        errors.append('nested, homograph or related-label exception missing')
    return errors

def main():
    read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
    errors=audit(read(DATA),read(BASE))
    report=dict(status='FAIL' if errors else 'PASS',errors=errors,
        scope='SUPPLIED_NUMERIC_REFERENCES_AND_SELECTED_ANNOTATION_BOUNDARIES_ONLY',
        selected_literals=37,substring_matches=174,selected_cases=17,
        component_chapters=5,remaining_component_chapters=45,readings_added=0,
        browser_capture_authenticated=False,literal_positions_authenticated=False,
        entity_inventory_authenticated=False,semantic_authentication=False,
        whole_P3_final=False,G11_final=False,manuscript_allowed=False)
    (ROOT/'reviews/G11_DELIVERY_COMPONENT_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report));return bool(errors)
if __name__=='__main__':raise SystemExit(main())
