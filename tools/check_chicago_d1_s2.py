"""Check S2 proof boundaries; do not infer evidence or author event choices."""
import argparse
import json
import math
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / 'control/CHICAGO_2020_21_D1_S2_REGISTER.json'

# Minimum legal domains already identified by the author-selected S2 protocol
# and register. Keep this independent of the editable proof/witness lists so
# deleting the same obligation from both cannot manufacture a complete proof.
# Additional required branches remain allowed and must also have witnesses.
# Numbers, evidence hashes and legal verdicts are intentionally not fixed here.
MINIMUM_PROOF_DOMAIN = {
    'CHI_TEAM_SALARY': ('F1', 'INTERVAL', ()),
    'CHI_MATCHING_RULE': ('F1', 'BRANCH_WITNESS',
                          ('post_assignment_rule_and_both_sides_charge',)),
    'BOS_TPE_AND_PICKS': ('F2', 'BRANCH_WITNESS',
                          ('dated_TPE_charge_and_capacity',
                           '2025_2R_ownership_priority', '2027_2R_ownership_priority')),
    'BOS_COMPLETE_COST': ('F2', 'INTERVAL', ()),
    'DEN_GORDON_PICKS_AND_CHARGE': ('F3', 'BRANCH_WITNESS',
                                    ('prior_1R_conveys', 'prior_1R_converts_to_2R',
                                     'subsequent_1R_protection_and_termination',
                                     'dated_matching_charge')),
    'DEN_COMPLETE_COST': ('F3', 'INTERVAL', ()),
    'ORL_COMPLETE_COST': ('F4', 'INTERVAL', ()),
    'ORL_DATED_REGISTRATION': ('F4', 'BRANCH_WITNESS',
                               ('game_days', 'intervening_days', 'all_other_transactions')),
    'CLE_COMPLETE_COST': ('F5', 'INTERVAL', ()),
    'DEN_CLE_DATED_REGISTRATION': ('F5', 'BRANCH_WITNESS',
                                   ('DEN_all_dates', 'CLE_all_dates',
                                    'prior_and_followup_contracts')),
    'ORL_F2_COMPLETE_COST': ('F2', 'INTERVAL', ()),
    'DEN_F5_COMPLETE_COST': ('F5', 'INTERVAL', ()),
}


def unique_names(value):
    return (isinstance(value, list) and
            all(isinstance(v, str) and bool(v) for v in value) and
            len(value) == len(set(value)))


def proof_domain_error(proof):
    if not isinstance(proof, dict):
        return 'proof must be an object'
    proof_id = proof.get('id')
    if not isinstance(proof_id, str) or proof_id not in MINIMUM_PROOF_DOMAIN:
        return 'unknown or missing proof id'
    group, kind, minimum_branches = MINIMUM_PROOF_DOMAIN[proof_id]
    if proof.get('group') != group or proof.get('kind') != kind:
        return f'{proof_id}: group/kind differs from the minimum domain'
    if kind == 'BRANCH_WITNESS':
        required = proof.get('required_branches')
        if not unique_names(required):
            return f'{proof_id}: required branches must be unique nonempty names'
        if not set(minimum_branches).issubset(required):
            return f'{proof_id}: required legal branch removed'
    return None


def validate_proof_domain(proofs):
    if not isinstance(proofs, list) or not all(isinstance(p, dict) for p in proofs):
        raise ValueError('S2 legal proofs must be a list of objects')
    ids = [p.get('id') for p in proofs]
    if not unique_names(ids) or set(ids) != set(MINIMUM_PROOF_DOMAIN):
        raise ValueError('S2 requires each of the twelve minimum proof ids exactly once')
    for proof in proofs:
        error = proof_domain_error(proof)
        if error:
            raise ValueError(error)


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def classify(proof):
    # An invalid minimum domain fails closed even if both certificate flags
    # are supplied as true. This does not assess source truth or completeness.
    if proof_domain_error(proof):
        return 'HOLD'
    # A supplied number without complete provenance/domain is not a proof.
    if proof.get('complete_domain') is not True or proof.get('source_verified') is not True:
        return 'HOLD'
    if proof['kind'] == 'INTERVAL':
        lo, hi, maximum = [proof.get(k) for k in ('lower', 'upper', 'maximum')]
        if not all(number(v) for v in (lo, hi, maximum)) or lo < 0 or hi < lo:
            return 'HOLD'
        if lo > maximum:
            return 'FAIL'
        return 'LEGAL_BOUND_PASS' if hi <= maximum else 'HOLD'
    if proof['kind'] == 'BRANCH_WITNESS':
        rows = proof.get('branches')
        if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
            return 'HOLD'
        ids = [r.get('id') for r in rows]
        required = proof['required_branches']
        if not unique_names(ids) or set(ids) != set(required):
            return 'HOLD'
        if any(r.get('verdict') == 'FAIL' for r in rows):
            return 'FAIL'
        if not rows or any(r.get('verdict') != 'LEGAL_BOUND_PASS' for r in rows):
            return 'HOLD'
        return 'LEGAL_BOUND_PASS'
    return 'HOLD'


def self_test():
    complete = dict(id='CHI_TEAM_SALARY', group='F1', kind='INTERVAL',
                    lower=100, upper=120, maximum=120,
                    complete_domain=True, source_verified=True)
    cases = [({}, 'LEGAL_BOUND_PASS'), ({'upper': None}, 'HOLD'),
             ({'upper': 121}, 'HOLD'), ({'lower': 121, 'upper': 122}, 'FAIL'),
             ({'complete_domain': False}, 'HOLD'),
             ({'source_verified': False}, 'HOLD'), ({'source_verified': 'true'}, 'HOLD'),
             ({'upper': math.inf}, 'HOLD')]
    for change, expected in cases:
        assert classify({**complete, **change}) == expected
    required = list(MINIMUM_PROOF_DOMAIN['DEN_GORDON_PICKS_AND_CHARGE'][2])
    branch = dict(id='DEN_GORDON_PICKS_AND_CHARGE', group='F3',
                  kind='BRANCH_WITNESS', complete_domain=True, source_verified=True,
                  required_branches=required,
                  branches=[dict(id=b, verdict='LEGAL_BOUND_PASS')
                            for b in required if b != 'prior_1R_converts_to_2R'])
    assert classify(branch) == 'HOLD', 'missing conversion branch must block'
    proofs = json.loads(REGISTER.read_text(encoding='utf-8'))['legal_proofs']
    validate_proof_domain(proofs)
    boston = deepcopy(next(p for p in proofs if p['id'] == 'BOS_TPE_AND_PICKS'))
    boston.update(complete_domain=True, source_verified=True,
                  branches=[dict(id=b, verdict='LEGAL_BOUND_PASS')
                            for b in boston['required_branches']])
    assert classify(boston) == 'LEGAL_BOUND_PASS'
    omitted = deepcopy(boston)
    omitted['required_branches'].remove('2027_2R_ownership_priority')
    omitted['branches'] = [r for r in omitted['branches']
                           if r['id'] != '2027_2R_ownership_priority']
    assert classify(omitted) == 'HOLD', 'deleting an obligation from both lists must block'
    duplicate = deepcopy(boston)
    duplicate['required_branches'].append('2025_2R_ownership_priority')
    assert classify(duplicate) == 'HOLD', 'duplicate required branches must block'
    duplicate_witness = deepcopy(boston)
    duplicate_witness['branches'].append(deepcopy(duplicate_witness['branches'][0]))
    assert classify(duplicate_witness) == 'HOLD', 'duplicate witness rows must block'
    for mutation in (dict(group='F3'), dict(kind='INTERVAL'), dict(id='UNKNOWN')):
        assert classify({**boston, **mutation}) == 'HOLD'
    # Adding a real future sub-obligation must remain possible, but its witness
    # is then required as well. No current evidence file/hash is a gate here.
    extension = deepcopy(boston)
    extension['required_branches'].append('additional_dated_obligation')
    assert classify(extension) == 'HOLD'
    extension['branches'].append(dict(id='additional_dated_obligation', verdict='LEGAL_BOUND_PASS'))
    assert classify(extension) == 'LEGAL_BOUND_PASS'
    invalid_registers = [proofs[:-1], proofs + [deepcopy(proofs[0])]]
    for key, value in (('group', 'F5'), ('kind', 'BRANCH_WITNESS')):
        changed = deepcopy(proofs)
        changed[0][key] = value
        invalid_registers.append(changed)
    for invalid_boston in (omitted, duplicate):
        changed = deepcopy(proofs)
        index = next(i for i, p in enumerate(changed) if p['id'] == boston['id'])
        changed[index] = invalid_boston
        invalid_registers.append(changed)
    for changed in invalid_registers:
        try:
            validate_proof_domain(changed)
        except ValueError:
            continue
        raise AssertionError('mutated register must fail minimum domain validation')
    print('S2 negative controls PASS: bounds/certificates, minimum proof/branch deletion, duplicates, group/kind; full future branches remain admissible')


def check():
    data = json.loads(REGISTER.read_text(encoding='utf-8'))
    authority = json.loads((ROOT / data['authority']).read_text(encoding='utf-8'))
    assert authority['selected']['route'] == 'S2_LEGAL_INTERVAL_PROOF_COUNTERFACTUAL_AUTHOR_MODEL'
    assert data['policy'] == 'S2'
    assert authority['season_selected'] is False and authority['manuscript_allowed'] is False
    proofs = data['legal_proofs']
    validate_proof_domain(proofs)
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
