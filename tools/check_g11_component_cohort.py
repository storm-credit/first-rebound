"""Validate retained numeric/position declarations, never original-source meaning."""
import hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA='research/G11_RIDI_BUSINESS_FIRST_FIVE_COMPONENTS_2026_10_01.json'
EXTRA_DATA='research/G11_JOARA_EXTRA_FIRST_FIVE_COMPONENTS_2026_10_01.json'
def canonical(m):
    payload={k:v for k,v in m.items() if k!='canonical_sha256'}
    return hashlib.sha256(json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def audit(d,ledger,cohort='BUSINESS'):
    errors=[]
    is_extra=cohort=='EXTRA'
    expected_work='소설 속 엑스트라' if is_extra else '재벌집 막내아들'
    if d.get('work')!=expected_work:errors.append('cohort source identity')
    forbidden=['author_locked','manuscript_allowed','G11_final','raw_novel_text_retained','raw_novel_text_uploaded','independent_original_semantic_review','universal_house_style_rule','complete_term_inventory','complete_space_cause_inventory']
    if any(d.get(k) is not False for k in forbidden) or d.get('freeze')!='v0.30 PARTIAL' or d.get('gate')!='CLOSED':errors.append('scope/gate promotion')
    counts=dict(readings_added=0,unique_readings_unchanged=95,unread_chapters_unchanged=15,component_chapters=15 if is_extra else 10,remaining_component_chapters=35 if is_extra else 40,component_denominator=50,whole_P3_completed_chapters=0,actual_episode_packs=0)
    if any(d.get(k)!=v for k,v in counts.items()) or d.get('components_share_same_chapters') is not True:errors.append('component/reading overcount')
    if d.get('professional_action_density','missing') is not None or d.get('total_inner_share','missing') is not None:errors.append('unmeasured semantic ratio')
    if d.get('browser_capture_sequence')!=[1,2,3,4,5]*3:errors.append('capture sequence')
    if [r['chapter'] for r in d['metrics']]!=[1,2,3,4,5] or [r['chapter'] for r in d['repeat']]!=[1,2,3,4,5] or [r['chapter'] for r in d['episodes']]!=[1,2,3,4,5]:errors.append('chapter cohort')
    def walk(o):
        if isinstance(o,dict):
            yield o
            for x in o.values():yield from walk(x)
        elif isinstance(o,list):
            for x in o:yield from walk(x)
    known={(r.get('work'),r.get('chapter'),r.get('url')) for r in walk(ledger) if r.get('scope')=='COMPLETE_CHAPTER'}
    for m,r,e in zip(d['metrics'],d['repeat'],d['episodes']):
        meta=m['paragraph_meta'];ids=[i for i,n in meta];sizes=[n for i,n in meta];lengths=dict(meta)
        if not is_extra:
            old=ledger['metrics']['chapters'][m['chapter']-1]
            if old['paragraph_lengths'][:-1]!=sizes or old['paragraph_lengths'][-1]!=13 or old['characters']!=sum(sizes)+13:errors.append('legacy scope reconciliation')
        if (d['work'],m['chapter'],m['url']) not in known:errors.append('official chapter missing in reading ledger')
        bounds=([16,96] if m['chapter']==1 else [15,[101,111,121,150][m['chapter']-2]]) if is_extra else [9,max(ids)]
        if ids!=sorted(set(ids)) or min(ids)!=bounds[0] or max(ids)!=bounds[1] or any(n<=0 for n in sizes):errors.append('body paragraph inventory')
        if sum(sizes)+2*(len(ids)-1)!=m['body_utf16']:errors.append('body/join denominator')
        if canonical(m)!=m['canonical_sha256']:errors.append('numeric canonical hash')
        if r['canonical_sha256']!=m['canonical_sha256'] or r['same'] is not True or r['intervening_chapter']!=(5 if m['chapter']==1 else m['chapter']-1):errors.append('repeat declaration')
        if m['raw_viewer_utf16']-m['normalized_viewer_utf16']!=sum(m['viewer_zero_width_removed'].values())+m['viewer_whitespace_trimmed_utf16']:errors.append('viewer normalization accounting')
        ordered=sorted(sizes);quant=[ordered[math.floor((len(ordered)-1)*q)] for q in [.1,.5,.9]]+[ordered[-1]]
        if list(m['paragraph_distribution'].values())!=quant:errors.append('paragraph quantile')
        cursor=0;last=None
        for i,n in meta:
            if cursor<1000:last=[i,cursor,n,min(n,1000-cursor)]
            cursor+=n+2
        if m['prefix_last_intersection']!=last:errors.append('first1000 clipping')
        voiced=[i for a in m['voice_indexes'].values() for i in a]
        if len(set(voiced))!=len(voiced) or not set(voiced)<=set(ids):errors.append('voice overlap or invalid address')
        blocks=e['blocks'];covered=[]
        for b in blocks:
            part=[i for i in ids if b['start']<=i<=b['end']];covered+=part
            if not part or b.get('body_block_count' if is_extra else 'body_p_count')!=len(part) or not b['selected_anchors'] or not set(b['selected_anchors'])<=set(part):errors.append('functional anchor/inventory')
        if covered!=ids:errors.append('functional blocks duplicate/gap/order')
        if e.get('semantic_status')!='INFERENCE' or e.get('past_inventory_complete') is not False or not e.get('unexecuted'):errors.append('semantic scope declaration')
    if sum(len(m['paragraph_meta']) for m in d['metrics'])!=(468 if is_extra else 615) or sum(len(e['blocks']) for e in d['episodes'])!=(25 if is_extra else 36):errors.append('total paragraph/block inventory')
    terms=d['terms']
    if len(terms)!=d.get('selected_literal_count') or len(terms)!=(21 if is_extra else 23) or sum(t['count'] for t in terms)!=d.get('selected_literal_matches') or sum(t['count'] for t in terms)!=(168 if is_extra else 121):errors.append('selected query totals')
    if len({t['id'] for t in terms})!=len(terms) or len({t['literal'] for t in terms})!=len(terms):errors.append('selected query identity')
    for t in terms:
        c,i,pos=t['first'];meta=dict(d['metrics'][c-1]['paragraph_meta']);n=len(t['literal'].encode('utf-16-le'))//2
        if i not in meta or pos<0 or pos+n>meta.get(i,0) or t['count']<=0:errors.append('literal position out of bounds')
    # These local exceptions encode reviewer decisions, not automatic semantic proof.
    voices=[m['voice_indexes'] for m in d['metrics']]
    if is_extra:
        if (voices[0].get('EVENT_ANNOUNCEMENT_SOURCE_UNSPECIFIED')!=[30,70] or voices[1].get('UI_EMAIL')!=[32,33] or 59 not in voices[2]['CHARACTER_SPEECH'] or voices[3].get('MEDIATED_MACHINE_SPEECH')!=[106] or voices[3].get('UI_ENVIRONMENT_TEXT')!=[112] or voices[4].get('UI_SYSTEM')!=list(range(114,138))+[148,149,150]):errors.append('context exception lost')
        if d.get('hidden_notice_excluded_from_body') is not True or d.get('footer_excluded_from_body') is not True:errors.append('wrapper exclusion missing')
    elif voices[1]['PAST_REPORTED_SPEECH']!=[100,115] or voices[0]['UI_TEXT_MESSAGE']!=[60,70] or voices[3]['NONVERBAL']!=[9] or 9 in voices[3]['CHARACTER_SPEECH']:errors.append('context exception lost')
    return errors
def main(cohort='BUSINESS'):
    read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
    is_extra=cohort=='EXTRA'
    errors=audit(read(EXTRA_DATA if is_extra else DATA),read('research/STYLE_READING_OBSERVATIONS.json'),cohort)
    report=dict(status='FAIL' if errors else 'PASS',errors=errors,paragraphs=468 if is_extra else 615,blocks=25 if is_extra else 36,component_chapters=15 if is_extra else 10,remaining_component_chapters=35 if is_extra else 40,scope='RETAINED_NUMERIC_AND_POSITION_DECLARATIONS_ONLY',browser_capture_authenticated=False,original_semantic_authentication=False,whole_P3_final=False,G11_final=False,manuscript_allowed=False)
    (ROOT/('reviews/G11_EXTRA_COMPONENT_REPORT.json' if is_extra else 'reviews/G11_BUSINESS_COMPONENT_REPORT.json')).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report));return bool(errors)
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--cohort',choices=['BUSINESS','EXTRA'],default='BUSINESS');args=parser.parse_args()
    raise SystemExit(main(args.cohort))
