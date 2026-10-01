"""Count chapter coverage per component, without combining component counts."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT='research/G11_COMPONENT_PROGRESS_2026_10_01.json'
SG='research/G11_RIDI_'
SOURCES={
 '내가 키운 S급들':{
  'structure':[SG+'STRUCTURAL_MEASUREMENTS_2026_10_01.json'],
  'voice':[SG+'CONTEXTUAL_VOICE_PILOT_2026_10_01.json',SG+'CONTEXTUAL_VOICE_FIRST_FIVE_2026_10_01.json'],
  'opening':[SG+'OPENING_BOUNDARY_COMPONENT_2026_10_01.json'],
  'function':[SG+'FUNCTION_SEQUENCE_FIRST_FIVE_2026_10_01.json'],
  'delivery':[SG+'INFORMATION_DELIVERY_FIRST_FIVE_2026_10_01.json']},
 '재벌집 막내아들':{k:['research/G11_RIDI_BUSINESS_FIRST_FIVE_COMPONENTS_2026_10_01.json'] for k in ['structure','voice','opening','function','delivery']},
 '소설 속 엑스트라':{k:['research/G11_JOARA_EXTRA_FIRST_FIVE_COMPONENTS_2026_10_01.json'] for k in ['structure','voice','opening','function','delivery']}}
def chapters(o):
    out=set()
    if isinstance(o,dict):
        if isinstance(o.get('chapter'),int):out.add(o['chapter'])
        for v in o.values():out.update(chapters(v))
    elif isinstance(o,list):
        for v in o:out.update(chapters(v))
    return out
def build(root=ROOT):
    rows=[];union={k:set() for k in ['structure','voice','opening','function','delivery']};errors=[]
    for work,components in SOURCES.items():
        for component,files in components.items():
            seen=set();hashes={}
            for file in files:
                path=root/file;data=json.loads(path.read_text(encoding='utf-8'))
                if data.get('work')!=work:errors.append('source work mismatch: '+file)
                seen.update(chapters(data));hashes[file]=hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
            if seen!={1,2,3,4,5}:errors.append('chapter coverage mismatch: '+work+'/'+component)
            union[component].update((work,c) for c in seen)
            rows.append(dict(work=work,component=component,chapters=sorted(seen),source_hashes=hashes,scope='SCOPED_OBSERVATIONS_NOT_COMPLETE_P3'))
    counts={k:dict(observed=len(v),denominator=50,remaining=50-len(v)) for k,v in union.items()}
    all_chapters=set().union(*union.values())
    return dict(status='FAIL' if errors else 'PASS',errors=errors,rows=rows,components=counts,unique_component_chapters=len(all_chapters),components_not_added=True,unique_readings=95,unread=15,new_unique_readings=0,whole_P3_completed_chapters=0,G11_final=False,author_locked=False,manuscript_allowed=False)
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    report=build()
    if args.check:
        stored=json.loads((ROOT/REPORT).read_text(encoding='utf-8'))
        if stored!=report:report['errors'].append('stored coverage/hash report stale');report['status']='FAIL'
    else:(ROOT/REPORT).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='rows'},ensure_ascii=False));raise SystemExit(bool(report['errors']))
