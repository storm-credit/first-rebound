"""O-15F6C leave-one-out capacity stress; no injury dates or outcome claims.

--write runs scipy and saves witnesses. Default verifies saved witnesses/cuts.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
import audit_chicago_2020_21_postdeadline_lineups as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'simulation/CHICAGO_2020_21_POSTDEADLINE_LINEUP_AUDIT.json'
OUTPUT = ROOT / 'simulation/CHICAGO_2020_21_AVAILABILITY_STRESS.json'
ABSENCES = ('Wendell Carter Jr.', 'LaMelo Ball', 'Otto Porter Jr.')


def setup(game, absent, rows):
    old = game['minimum_change_candidate']['player_seconds']
    target = {p: t for p, t in old.items() if p != absent and t > 0}
    observed = {r['player']: int(r['actual_seconds']) for r in rows}
    bounds = {}
    for p, t in target.items():
        if p in prior.FIXED:
            bounds[p] = (t, t)
        else:
            lower = min(t, prior.FLOORS.get(p, 30))
            upper = max(t, min(2160 if p not in prior.BIG else 1800, observed.get(p, 0)+360))
            if p == 'Daniel Theis':
                upper = min(1440, upper)
            bounds[p] = (lower, upper)
    starters = set(game['candidate_starters']) - {absent}
    if len(starters) == 4:
        order = (['Daniel Theis','Thaddeus Young','Cristiano Felicio','Lauri Markkanen']
                 if absent == 'Wendell Carter Jr.' else ['Tomas Satoransky','Coby White','Ryan Arcidiacono','Devon Dotson','Garrett Temple'])
        candidates = [p for p in order if p in target and p not in starters and prior.valid(starters | {p}, 2)]
        if not candidates:
            return target, bounds, sorted(starters), {'kind': 'STARTER_REPLACEMENT_POLICY', 'shortfall_seconds': None}
        starters.add(candidates[0])
    # Any feasible five-player allocation must satisfy these simple capacity cuts.
    cuts = [('TOTAL_UPPER', sum(b[1] for b in bounds.values()), 14400),
            ('CENTER_UPPER_WITH_OPENING', sum(bounds[p][1] for p in target if p in prior.CENTER), 2880+180*max(0,len(starters & prior.CENTER)-1)),
            ('HANDLER_UPPER_WITH_OPENING', sum(bounds[p][1] for p in target if p in prior.HANDLER), 2880+180*max(0,len(starters & prior.HANDLER)-1)),
            ('WING_UPPER_WITH_OPENING', sum(bounds[p][1] for p in target if p in prior.WING), 2880+180*max(0,len(starters & prior.WING)-1)),
            ('PERIMETER_UPPER_WITH_OPENING', sum(bounds[p][1] for p in target if p not in prior.BIG), 8640+180*max(0,len(starters-prior.BIG)-3))]
    failing = [{'kind': k, 'shortfall_seconds': round(need-have, 8)} for k, have, need in cuts if have < need-1e-6]
    return target, bounds, sorted(starters), failing[0] if failing else None


def build():
    inputs = json.loads(SOURCE.read_text())
    rows_by_game = prior.inputs()
    output = []
    for game in inputs['games']:
        if game['scenario'] != 'PORTER_CAPPED':
            continue
        rows = rows_by_game[('PORTER_CAPPED',game['date'])]
        for absent in ABSENCES:
            target, bounds, starters, cut = setup(game, absent, rows)
            result = {'status': 'CAPACITY_CUT_FAIL', 'cut': cut} if cut else prior.solve(target, starters, 2, bounds)
            output.append({'date': game['date'], 'absent': absent, 'missing_seconds': game['minimum_change_candidate']['player_seconds'].get(absent,0),
                           'target_seconds': target, 'bounds': bounds, 'starters': starters, 'result': result})
    return {'stage': 'O-15F6C', 'status': 'COUNTERFACTUAL_STRESS_NOT_INJURY_FORECAST',
            'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(), 'cases': output}


def verify(data):
    assert data['source_sha256'] == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    source = {g['date']: g for g in json.loads(SOURCE.read_text())['games'] if g['scenario']=='PORTER_CAPPED'}
    rows_by_game = prior.inputs()
    assert len(data['cases']) == len({(c['date'],c['absent']) for c in data['cases']}) == 87
    for case in data['cases']:
        target, bounds, starters, cut = setup(source[case['date']],case['absent'],rows_by_game[('PORTER_CAPPED',case['date'])])
        assert target == case['target_seconds'] and starters == case['starters']
        assert {p:tuple(b) for p,b in case['bounds'].items()} == bounds
        assert abs(case['missing_seconds'] + sum(target.values()) - 14400) < 1e-5
        result = case['result']
        if result['status'] == 'CAPACITY_CUT_FAIL':
            assert cut == result['cut'] and cut is not None
            continue
        assert cut is None and result['status']=='CONDITIONAL_CERTIFICATE_PASS', case
        segments = result['segments']
        assert abs(sum(s['seconds'] for s in segments)-2880)<1e-5
        for s in segments:
            assert s['seconds'] > 0 and prior.valid(s['players'],2)
            assert set(s['players']) <= set(target) and case['absent'] not in s['players']
        assert sum(s['seconds'] for s in segments if sorted(s['players'])==starters)>=180-1e-5
        for p in target:
            total=sum(s['seconds'] for s in segments if p in s['players'])
            assert bounds[p][0]-1e-5 <= total <= bounds[p][1]+1e-5
            assert abs(total-result['player_seconds'][p])<1e-5
        assert abs(result['l1_seconds']-sum(abs(result['player_seconds'][p]-target[p]) for p in target))<1e-5


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--write',action='store_true'); args=parser.parse_args()
    data=build() if args.write else json.loads(OUTPUT.read_text())
    verify(data)
    if args.write: OUTPUT.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
    for p in ABSENCES:
        cases=[c for c in data['cases'] if c['absent']==p]
        print(p,dict(Counter(c['result']['status'] for c in cases)))
        print([(c['date'],c['result']['cut']) for c in cases if c['result']['status']=='CAPACITY_CUT_FAIL'])
    print('PASS: 87 independent date stresses; no actual absence, GP, production or outcome selected')
