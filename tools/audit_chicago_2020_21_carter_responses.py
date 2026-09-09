"""Compare bounded Carter-absence policies; never assign an actual injury.

--write requires scipy. Default checks saved witnesses and capacity cuts.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
import audit_chicago_2020_21_availability_stress as stress

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'simulation/CHICAGO_2020_21_AVAILABILITY_STRESS.json'
OUTPUT = ROOT / 'simulation/CHICAGO_2020_21_CARTER_RESPONSES.json'
POLICIES = ('ONE_CENTER_OPENING', 'THEIS_30', 'THEIS_YOUNG_30', 'FELICIO_18')
ACTUAL = ROOT / 'simulation/CHICAGO_2020_21_POSTDEADLINE_ACTUAL.csv'
P = stress.prior


def setup(case, policy):
    target = dict(case['target_seconds'])
    bounds = {p: tuple(b) for p, b in case['bounds'].items()}
    starters = set(case['starters'])
    if len(starters & P.CENTER) > 1:
        # Change only one center slot. Preserve all other original starters.
        remove = sorted(starters & P.CENTER, key=lambda p: (p != 'Thaddeus Young', p))[0]
        order = ['Garrett Temple', 'Tomas Satoransky', 'Coby White', 'Javonte Green',
                 'Denzel Valentine', 'Otto Porter Jr.', 'Ryan Arcidiacono', 'Devon Dotson', 'Adam Mokoka']
        choices = [p for p in order if p in target and p not in starters
                   and P.valid((starters-{remove}) | {p}, 2)]
        if choices:
            starters = (starters-{remove}) | {choices[0]}
    if policy in ('THEIS_30', 'THEIS_YOUNG_30', 'FELICIO_18') and 'Daniel Theis' in bounds:
        low, high = bounds['Daniel Theis']
        bounds['Daniel Theis'] = (low, max(high, 1800))
    if policy in ('THEIS_YOUNG_30', 'FELICIO_18') and 'Thaddeus Young' in bounds:
        low, high = bounds['Thaddeus Young']
        bounds['Thaddeus Young'] = (low, max(high, 1800))
    if policy == 'FELICIO_18':
        rows = list(csv.DictReader(ACTUAL.open()))
        row = next((r for r in rows if r['date']==case['date'] and r['player']=='Cristiano Felicio'), None)
        eligible = row is not None and (int(row['actual_seconds'])>0 or row['comment']=="DNP - Coach's Decision")
        if eligible:
            target.setdefault('Cristiano Felicio', 0)
            low, high = bounds.get('Cristiano Felicio', (0, 0))
            bounds['Cristiano Felicio'] = (low, max(high, 1080))
    groups = [('TOTAL', set(target), 14400, 5),
              ('CENTER', P.CENTER, 2880, 1), ('HANDLER', P.HANDLER, 2880, 1),
              ('WING', P.WING, 2880, 1), ('PERIMETER', set(target)-P.BIG, 8640, 3)]
    cuts = []
    for name, group, base, minimum in groups:
        need = base + 180*max(0, len(starters & group)-minimum)
        upper = sum(bounds[p][1] for p in target if p in group)
        if upper < need-1e-6:
            cuts.append({'kind': name, 'shortfall_seconds': round(need-upper, 8)})
    return target, bounds, sorted(starters), cuts


def build():
    cases = [c for c in json.loads(SOURCE.read_text())['cases'] if c['absent']=='Wendell Carter Jr.']
    output = []
    for c in cases:
        for policy in POLICIES:
            target, bounds, starters, cuts = setup(c, policy)
            result = {'status':'CAPACITY_CUT_FAIL', 'cuts':cuts} if cuts else P.solve(target, starters, 2, bounds)
            output.append({'date':c['date'], 'policy':policy, 'starters':starters,
                           'bounds':bounds, 'result':result})
    return {'stage':'O-15F6D', 'status':'CONDITIONAL_RESPONSES_NOT_ACTUAL_AVAILABILITY',
            'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'actual_sha256':hashlib.sha256(ACTUAL.read_bytes()).hexdigest(), 'cases':output}


def verify(data):
    stress.verify(json.loads(SOURCE.read_text()))
    assert data['source_sha256']==hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert data['actual_sha256']==hashlib.sha256(ACTUAL.read_bytes()).hexdigest()
    original = {c['date']:c for c in json.loads(SOURCE.read_text())['cases'] if c['absent']=='Wendell Carter Jr.'}
    assert {(c['date'], c['policy']) for c in data['cases']} == {(d,p) for d in original for p in POLICIES}
    assert len(data['cases'])==116
    for c in data['cases']:
        target, bounds, starters, cuts = setup(original[c['date']], c['policy'])
        assert c['starters']==starters and {p:tuple(b) for p,b in c['bounds'].items()}==bounds
        r = c['result']
        if cuts:
            assert r=={'status':'CAPACITY_CUT_FAIL', 'cuts':cuts}
            continue
        assert r['status']=='CONDITIONAL_CERTIFICATE_PASS', (c['date'],c['policy'],r)
        segments = r['segments']
        assert abs(sum(s['seconds'] for s in segments)-2880)<1e-5
        assert sum(s['seconds'] for s in segments if sorted(s['players'])==starters)>=180-1e-5
        assert set(r['player_seconds'])==set(target)
        for s in segments:
            assert s['seconds']>0 and P.valid(s['players'],2)
            assert set(s['players'])<=set(target) and 'Wendell Carter Jr.' not in s['players']
        for p, (low, high) in bounds.items():
            total = sum(s['seconds'] for s in segments if p in s['players'])
            assert low-1e-5<=total<=high+1e-5
            assert abs(total-r['player_seconds'][p])<1e-5
        assert abs(r['l1_seconds']-sum(abs(r['player_seconds'][p]-target[p]) for p in target))<1e-5
        # Each absent second must be absorbed; no extra transfers are needed in saved solutions.
        assert abs(r['l1_seconds']-original[c['date']]['missing_seconds'])<1e-5
    print('PASS: 116 Carter response certificates/cuts; fixed core and observed playing/DNP eligibility')
    for p in POLICIES:
        cases = [c for c in data['cases'] if c['policy']==p]
        print(p, dict(Counter(c['result']['status'] for c in cases)))
        print([(c['date'], c['result']['cuts']) for c in cases if c['result']['status']=='CAPACITY_CUT_FAIL'])


if __name__=='__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--write', action='store_true'); args=parser.parse_args()
    data = build() if args.write else json.loads(OUTPUT.read_text())
    verify(data)
    if args.write: OUTPUT.write_text(json.dumps(data, ensure_ascii=False, separators=(',',':'))+'\n')
