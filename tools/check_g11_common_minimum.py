"""Check recorded scope/addresses/arithmetic; never authenticate novel semantics."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH='research/G11_SGRADE_COMMON_MINIMUM_2026_10_02.json'
OPENING='research/G11_RIDI_OPENING_BOUNDARY_COMPONENT_2026_10_01.json'
def validate(d,opening,root=ROOT):
    errors=[]
    for k in ['whole_P3_final','G11_final','author_locked','season_selected','manuscript_allowed','raw_novel_text_retained','raw_novel_text_uploaded','independent_semantic_authentication']:
        if d.get(k) is not False:errors.append('scope promotion: '+k)
    if d.get('new_unique_readings')!=0 or d.get('actual_episode_packs')!=0:errors.append('reading/pack inflation')
    if d.get('minimum_work_records_ready')!=1 or d.get('minimum_work_records_target')!=10:errors.append('work record count')
    if d.get('work')!=opening['work'] or [r['chapter'] for r in d['records']]!=list(range(1,6)):errors.append('chapter/work identity')
    for path,h in d['source_hashes'].items():
        if hashlib.sha256((root/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()!=h:errors.append('source content changed')
    for r,o in zip(d['records'],opening['records']):
        m=o['metric'];ints={a['raw_p_index']:a for a in m['prefix_paragraph_intersections']}
        if any(r.get(k)!=v for k,v in [('url',o['url']),('body_sha256',m['body_sha256']),('first1000_sha256',m['first1000_sha256'])]):errors.append('official identity/hash mismatch')
        den=sum(a['covered_utf16'] for a in ints.values())
        if r['prefix_nonempty_intersections']!=len(ints) or r['prefix_text_utf16_without_join']!=den or r['prefix_join_utf16']!=1000-den:errors.append('prefix denominator mismatch')
        seen=set()
        for t in r['first1000_all_display_blocks_coded']:
            inds=t['raw_p_indexes'];seen.update(inds)
            if len(inds)!=len(set(inds)) or not set(inds)<=set(ints):errors.append('tag outside prefix or duplicated');continue
            units=sum(ints[i]['covered_utf16'] for i in inds)
            if t['display_blocks']!=len(inds) or t['covered_utf16']!=units or t['display_block_presence_fraction']!=round(len(inds)/len(ints),6) or t['text_presence_fraction']!=round(units/den,6):errors.append('tag arithmetic mismatch')
        if seen!=set(ints):errors.append('unmapped prefix block')
        if r.get('distinct_human_count') is not None or r.get('linguistic_sentence_count') is not None:errors.append('proxy cannot certify human/sentence totals')
    if d['first1000_rubric'].get('fractions_must_not_be_summed') is not True:errors.append('multilabel totals misleading')
    if {s['kind'] for s in d['minimum_scene_samples']}!={'PHYSICAL_COMBAT','DIALOGUE','EXPOSITION'}:errors.append('minimum scene coverage')
    return errors
if __name__=='__main__':
    d=json.loads((ROOT/PATH).read_text(encoding='utf-8'));o=json.loads((ROOT/OPENING).read_text(encoding='utf-8'));errors=validate(d,o)
    print(json.dumps(dict(PASS=not errors,scope='RECORDED_MINIMUM_WORK_RECORD_SCOPE_ADDRESS_ARITHMETIC_NOT_SEMANTICS',errors=errors,minimum_work_records_ready=1,whole_P3_final=False,G11_final=False)))
    raise SystemExit(bool(errors))
