"""Check S2 proof boundaries; do not infer evidence or author event choices."""
import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / 'control/CHICAGO_2020_21_D1_S2_REGISTER.json'


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def classify(proof):
    # A supplied number without complete provenance/domain is not a proof.
    if proof['complete_domain'] is not True or proof['source_verified'] is not True:
        return 'HOLD'
    if proof['kind'] == 'INTERVAL':
        lo, hi, maximum = [proof[k] for k in ('lower', 'upper', 'maximum')]
        if not all(number(v) for v in (lo, hi, maximum)) or lo < 0 or hi < lo:
            return 'HOLD'
        if lo > maximum:
            return 'FAIL'
        return 'LEGAL_BOUND_PASS' if hi <= maximum else 'HOLD'
    if proof['kind'] == 'BRANCH_WITNESS':
        rows = proof['branches']
        ids = [r['id'] for r in rows]
        required = proof['required_branches']
        if len(ids) != len(set(ids)) or set(ids) != set(required):
            return 'HOLD'
        if any(r['verdict'] == 'FAIL' for r in rows):
            return 'FAIL'
        if not rows or any(r['verdict'] != 'LEGAL_BOUND_PASS' for r in rows):
            return 'HOLD'
        return 'LEGAL_BOUND_PASS'
    raise ValueError('unknown proof kind')


def self_test():
    complete = dict(kind='INTERVAL', lower=100, upper=120, maximum=120,
                    complete_domain=True, source_verified=True)
    cases = [({}, 'LEGAL_BOUND_PASS'), ({'upper': None}, 'HOLD'),
             ({'upper': 121}, 'HOLD'), ({'lower': 121, 'upper': 122}, 'FAIL'),
             ({'complete_domain': False}, 'HOLD'),
             ({'source_verified': False}, 'HOLD'), ({'source_verified': 'true'}, 'HOLD'),
             ({'upper': math.inf}, 'HOLD')]
    for change, expected in cases:
        assert classify({**complete, **change}) == expected
    branch = dict(kind='BRANCH_WITNESS', complete_domain=True, source_verified=True,
                  required_branches=['conveys', 'converts'],
                  branches=[dict(id='conveys', verdict='LEGAL_BOUND_PASS')])
    assert classify(branch) == 'HOLD', 'missing conversion branch must block'
    print('S2 negative controls PASS: null/unbounded, crossing limit, incomplete domain/source/branch')


def check():
    data = json.loads(REGISTER.read_text(encoding='utf-8'))
    authority = json.loads((ROOT / data['authority']).read_text(encoding='utf-8'))
    assert authority['selected']['route'] == 'S2_LEGAL_INTERVAL_PROOF_COUNTERFACTUAL_AUTHOR_MODEL'
    assert data['policy'] == 'S2'
    assert authority['season_selected'] is False and authority['manuscript_allowed'] is False
    proofs = data['legal_proofs']
    assert len({p['id'] for p in proofs}) == len(proofs)
    for proof in proofs:
        assert proof['evidence'] and all((ROOT / p).is_file() for p in proof['evidence'])
    rows = {p['id']: classify(p) for p in proofs}
    groups = {}
    for group in ('F1', 'F2', 'F3', 'F4', 'F5'):
        children = [rows[p['id']] for p in proofs if p['group'] == group]
        assert children, group
        groups[group] = ('FAIL' if 'FAIL' in children else
                         'LEGAL_BOUND_PASS' if all(v == 'LEGAL_BOUND_PASS' for v in children) else 'HOLD')
    models = data['model_gates']
    assert {m['id'] for m in models} == {'A1', 'A2', 'A3'}
    # This is the initial S2 transition, not a season-promotion command.
    assert not data['season_selected'] and not data['manuscript_allowed']
    assert not data['k_closed']
    print(json.dumps(dict(policy='S2', legal_fields=rows, F_legal=groups,
                          A_states={m['id']:m['state'] for m in models},
                          K_closed=0, season_selected=False, manuscript_allowed=False), ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
    check()
