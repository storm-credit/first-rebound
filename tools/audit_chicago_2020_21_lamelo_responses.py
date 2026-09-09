"""Resolve only three prior policy failures; no actual injury assignment."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import audit_chicago_2020_21_availability_stress as prior
P=prior.prior
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'simulation/CHICAGO_2020_21_AVAILABILITY_STRESS.json'
ACTUAL=ROOT/'simulation/CHICAGO_2020_21_POSTDEADLINE_ACTUAL.csv'
OUTPUT=ROOT/'simulation/CHICAGO_2020_21_LAMELO_RESPONSES.json'
POLICIES=('RESTORE_OBSERVED_RESERVES','ACTIVE_RESERVE_12')
RESERVES={'Ryan Arcidiacono','Javonte Green','Adam Mokoka','Devon Dotson'}


def setup(case,policy):
    target=dict(case['target_seconds']);bounds={p:tuple(b) for p,b in case['bounds'].items()}
    evidence=[]
    for row in csv.DictReader(ACTUAL.open()):
        p=row['player']
        if row['date']!=case['date'] or p not in RESERVES:continue
        seconds=int(row['actual_seconds'])
        if seconds>0:
            upper=seconds
        elif policy=='ACTIVE_RESERVE_12' and row['comment']=="DNP - Coach's Decision":
            upper=720
        else:continue
        if p in target and bounds[p][1]>=upper:continue
        target.setdefault(p,0)
        low,old=bounds.get(p,(0,0));bounds[p]=(low,max(old,upper))
        evidence.append({'player':p,'observed_seconds':seconds,'comment':row['comment'],'new_upper':bounds[p][1]})
    starters=case['starters']
    groups=[('TOTAL',set(target),14400,5),('CENTER',P.CENTER,2880,1),('HANDLER',P.HANDLER,2880,1),('WING',P.WING,2880,1),('PERIMETER',set(target)-P.BIG,8640,3)]
    cuts=[]
    for name,group,base,minimum in groups:
        required=base+180*max(0,len(set(starters)&group)-minimum)
        have=sum(bounds[p][1] for p in target if p in group)
        if have<required-1e-6:cuts.append({'kind':name,'shortfall_seconds':round(required-have,8)})
    return target,bounds,starters,evidence,cuts


def cases():
    return [c for c in json.loads(SOURCE.read_text())['cases'] if c['absent']=='LaMelo Ball' and c['result']['status']=='CAPACITY_CUT_FAIL']


def build():
    out=[]
    for c in cases():
        for policy in POLICIES:
            target,bounds,starters,evidence,cuts=setup(c,policy)
            r={'status':'CAPACITY_CUT_FAIL','cuts':cuts} if cuts else P.solve(target,starters,2,bounds)
            out.append({'date':c['date'],'policy':policy,'evidence':evidence,'result':r})
    return {'stage':'O-15F7','status':'CONDITIONAL_RESERVE_RESPONSE_NOT_INJURY_EVENT',
            'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'actual_sha256':hashlib.sha256(ACTUAL.read_bytes()).hexdigest(),'cases':out}


def verify(data):
    prior.verify(json.loads(SOURCE.read_text()))
    assert data['source_sha256']==hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert data['actual_sha256']==hashlib.sha256(ACTUAL.read_bytes()).hexdigest()
    original={c['date']:c for c in cases()}
    assert len(original)==3 and len(data['cases'])==6
    assert {(c['date'],c['policy']) for c in data['cases']}=={(d,p) for d in original for p in POLICIES}
    for c in data['cases']:
        old=original[c['date']];target,bounds,starters,evidence,cuts=setup(old,c['policy'])
        assert c['evidence']==evidence
        r=c['result']
        if cuts:
            assert r=={'status':'CAPACITY_CUT_FAIL','cuts':cuts};continue
        assert r['status']=='CONDITIONAL_CERTIFICATE_PASS'
        assert set(r['player_seconds'])==set(target)
        segments=r['segments']
        assert abs(sum(s['seconds'] for s in segments)-2880)<1e-5
        assert sum(s['seconds'] for s in segments if sorted(s['players'])==starters)>=180-1e-5
        for s in segments:
            assert s['seconds']>0 and P.valid(s['players'],2) and set(s['players'])<=set(target)
            assert 'LaMelo Ball' not in s['players']
        for p,(low,high) in bounds.items():
            total=sum(s['seconds'] for s in segments if p in s['players'])
            assert low-1e-5<=total<=high+1e-5 and abs(total-r['player_seconds'][p])<1e-5
        assert abs(r['l1_seconds']-sum(abs(r['player_seconds'][p]-target[p]) for p in target))<1e-5
        assert abs(r['l1_seconds']-old['missing_seconds'])<1e-5
    print('PASS: six targeted LaMelo response certificates/cuts; fixed protagonist role')
    for c in data['cases']:print(c['date'],c['policy'],c['result']['status'])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    data=build() if args.write else json.loads(OUTPUT.read_text());verify(data)
    if args.write:OUTPUT.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
