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

MODEL_IDS = ('A1', 'A2', 'A3')
K_IDS = ('K_HEALTH', 'K_REGISTRATION', 'K_TRANSACTIONS', 'K_METHOD_EVENTS')
SEASON = '2020-21'


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


def evidence_paths(value, label):
    """Validate references, not the truth or scope of their contents."""
    if not unique_names(value) or not value or any(not p.strip() for p in value):
        raise ValueError(f'{label}: nonempty unique evidence references required')
    resolved = []
    for reference in value:
        path = (ROOT / reference).resolve()
        if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
            raise ValueError(f'{label}: evidence must be an existing file within the repository')
        resolved.append(path)
    if len(resolved) != len(set(resolved)):
        raise ValueError(f'{label}: duplicate resolved evidence references')
    return set(resolved)


def exact_rows(value, expected, label):
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise ValueError(f'{label}: witness rows required')
    ids = [row.get('id') for row in value]
    if not unique_names(ids) or set(ids) != set(expected):
        raise ValueError(f'{label}: each required id must appear exactly once')
    return {row['id']: row for row in value}


def closing_certificate(row, label, *, separate_authority=False):
    if not isinstance(row, dict):
        raise ValueError(f'{label}: witness object required')
    if row.get('verdict') not in ('PASS', 'HOLD', 'FAIL'):
        raise ValueError(f'{label}: PASS/HOLD/FAIL verdict required')
    for key in ('complete_domain', 'source_verified'):
        if type(row.get(key)) is not bool:
            raise ValueError(f'{label}: {key} must be a boolean')
    # A HOLD/FAIL certificate may record work still missing. It cannot close.
    if row['verdict'] != 'PASS':
        return False
    if row['complete_domain'] is not True or row['source_verified'] is not True:
        raise ValueError(f'{label}: PASS requires both complete certificates')
    if separate_authority:
        evidence_paths(row.get('authority_evidence'), f'{label}.authority')
        evidence_paths(row.get('execution_evidence'), f'{label}.execution')
        # One packet may contain separate selection and execution sections.
        # Distinct roles are required; two physical files are not an S2 rule.
        # The reviewer must verify those sections, not just these path lists.
    else:
        evidence_paths(row.get('evidence'), label)
    return True


def calculate_closing(data, groups):
    """Conservative protocol order: all F -> final A execution -> four K -> season.

    Reviewer certificates remain necessary. The checker cannot independently
    authenticate source truth, domain completeness, or author selection meaning.
    Historical S2 selection-time season_selected=false is not a future veto.
    """
    if set(groups) != {'F1', 'F2', 'F3', 'F4', 'F5'}:
        raise ValueError('closing requires all five computed F groups')
    model_execution = {model_id: 'HOLD' for model_id in MODEL_IDS}
    closed = []
    season_selected = False
    witness = data.get('closing_witness')
    if witness is not None:
        if not isinstance(witness, dict) or type(witness.get('schema_version')) is not int or witness['schema_version'] != 1:
            raise ValueError('closing_witness: schema_version 1 required')
        models = exact_rows(witness.get('model_execution'), MODEL_IDS, 'model_execution')
        bundles = exact_rows(witness.get('k_bundles'), K_IDS, 'k_bundles')
        # No input-supplied dependency list may weaken this fixed prerequisite.
        legal_pass = all(value == 'LEGAL_BOUND_PASS' for value in groups.values())
        for model_id in MODEL_IDS:
            certified = closing_certificate(models[model_id], model_id, separate_authority=True)
            if legal_pass and certified:
                model_execution[model_id] = 'PASS'
        all_models_pass = all(value == 'PASS' for value in model_execution.values())
        for bundle_id in K_IDS:
            certified = closing_certificate(bundles[bundle_id], bundle_id)
            if all_models_pass and certified:
                closed.append(bundle_id)
        season = witness.get('season_execution')
        if not isinstance(season, dict) or season.get('season') != SEASON:
            raise ValueError('season_execution: 2020-21 witness required')
        certified = closing_certificate(season, 'season_execution', separate_authority=True)
        season_selected = len(closed) == len(K_IDS) and certified
    recorded = data.get('k_closed')
    if not unique_names(recorded) or set(recorded) != set(closed):
        raise ValueError('k_closed must equal the computed certified K ids')
    if type(data.get('season_selected')) is not bool or data['season_selected'] != season_selected:
        raise ValueError('season_selected must equal the computed season execution verdict')
    if data.get('manuscript_allowed') is not False:
        raise ValueError('S2/D1 closure does not authorize manuscript opening')
    return model_execution, closed, season_selected


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
    closing_self_test()


def evaluate(data, *, initial_snapshot=False):
    evidence_paths([data['authority']], 'S2 authority')
    authority = json.loads((ROOT / data['authority']).read_text(encoding='utf-8'))
    assert authority['selected']['route'] == 'S2_LEGAL_INTERVAL_PROOF_COUNTERFACTUAL_AUTHOR_MODEL'
    assert data['policy'] == 'S2'
    proofs = data['legal_proofs']
    validate_proof_domain(proofs)
    for proof in proofs:
        evidence_paths(proof.get('evidence'), proof['id'])
    rows = {p['id']: classify(p) for p in proofs}
    groups = {}
    for group in ('F1', 'F2', 'F3', 'F4', 'F5'):
        children = [rows[p['id']] for p in proofs if p['group'] == group]
        assert children, group
        groups[group] = ('FAIL' if 'FAIL' in children else
                         'LEGAL_BOUND_PASS' if all(v == 'LEGAL_BOUND_PASS' for v in children) else 'HOLD')
    models = exact_rows(data['model_gates'], MODEL_IDS, 'model_gates')
    execution, closed, season_selected = calculate_closing(data, groups)
    if initial_snapshot:
        # Explicit historical check, separate from future execution closure.
        assert authority['season_selected'] is False and authority['manuscript_allowed'] is False
        assert not closed and season_selected is False
    return dict(policy='S2', legal_fields=rows, F_legal=groups,
                A_states={model_id: row['state'] for model_id, row in models.items()},
                A_execution=execution, K_closed=len(closed),
                season_selected=season_selected, manuscript_allowed=False)


def initial_test_fixture(template):
    """Use the current schema/references without fixing real progress at zero."""
    fixture = deepcopy(template)
    for proof in fixture['legal_proofs']:
        proof.update(complete_domain=False, source_verified=False)
        if proof['kind'] == 'INTERVAL':
            proof.update(lower=None, upper=None)
        else:
            proof['branches'] = []
    fixture.pop('closing_witness', None)
    fixture.update(k_closed=[], season_selected=False, manuscript_allowed=False)
    return fixture


def closing_self_test():
    template = json.loads(REGISTER.read_text(encoding='utf-8'))
    initial_fixture = initial_test_fixture(template)
    initial = evaluate(initial_fixture, initial_snapshot=True)
    assert initial['K_closed'] == 0 and initial['season_selected'] is False
    assert all(value == 'HOLD' for value in initial['legal_fields'].values())
    positive = deepcopy(initial_fixture)
    for proof in positive['legal_proofs']:
        proof.update(complete_domain=True, source_verified=True)
        if proof['kind'] == 'INTERVAL':
            proof.update(lower=1, upper=1, maximum=1)
        else:
            proof['branches'] = [dict(id=name, verdict='LEGAL_BOUND_PASS')
                                 for name in proof['required_branches']]
    # Existing files are only synthetic reference fixtures, not new legal evidence.
    authority_reference = initial_fixture['authority']
    execution_reference = 'tools/check_chicago_d1_s2.py'
    certificate = dict(verdict='PASS', complete_domain=True, source_verified=True,
                       authority_evidence=[authority_reference],
                       execution_evidence=[execution_reference])
    positive['closing_witness'] = dict(
        schema_version=1,
        model_execution=[dict(id=model_id, **deepcopy(certificate)) for model_id in MODEL_IDS],
        k_bundles=[dict(id=bundle_id, verdict='PASS', complete_domain=True,
                        source_verified=True, evidence=[execution_reference]) for bundle_id in K_IDS],
        season_execution=dict(season=SEASON, **deepcopy(certificate)))
    positive.update(k_closed=list(K_IDS), season_selected=True)
    result = evaluate(positive)
    assert result['K_closed'] == 4 and result['season_selected'] is True
    assert all(value == 'PASS' for value in result['A_execution'].values())
    # Simulate an already-completed real register as the schema template. Its
    # progress must not turn these synthetic initial/negative tests into vetoes.
    reset = evaluate(initial_test_fixture(positive), initial_snapshot=True)
    assert reset['K_closed'] == 0 and reset['season_selected'] is False
    assert all(value == 'HOLD' for value in reset['legal_fields'].values())
    combined_packet = deepcopy(positive)
    combined_packet['closing_witness']['model_execution'][0]['execution_evidence'] = [authority_reference]
    assert evaluate(combined_packet)['K_closed'] == 4, 'a combined packet is not forbidden by S2'
    # The immutable selection-time authority still says false; future closure works.
    authority = json.loads((ROOT / authority_reference).read_text(encoding='utf-8'))
    assert authority['season_selected'] is False

    def must_reject(data, label, **options):
        try:
            evaluate(data, **options)
        except (ValueError, AssertionError):
            return
        raise AssertionError(f'closing negative control did not block: {label}')

    forged = deepcopy(initial_fixture)
    forged['season_selected'] = True
    must_reject(forged, 'season flag without witness')
    forged = deepcopy(initial_fixture)
    forged['k_closed'] = list(K_IDS)
    must_reject(forged, 'K flags without witness')
    must_reject(positive, 'future closure is not an initial snapshot', initial_snapshot=True)
    for field in ('model_execution', 'k_bundles'):
        for mutation in ('missing', 'duplicate', 'unknown'):
            changed = deepcopy(positive)
            records = changed['closing_witness'][field]
            if mutation == 'missing':
                records.pop()
            elif mutation == 'duplicate':
                records.append(deepcopy(records[0]))
            else:
                records[0]['id'] = 'UNKNOWN'
            must_reject(changed, f'{field} {mutation}')
    changed = deepcopy(positive)
    changed['model_gates'].append(deepcopy(changed['model_gates'][0]))
    must_reject(changed, 'duplicate register model gate')
    for key, value in (('complete_domain', False), ('source_verified', False),
                       ('source_verified', 'true'), ('verdict', 'UNVERIFIED'),
                       ('authority_evidence', []), ('execution_evidence', []),
                       ('execution_evidence', ['missing-closing-witness-file.json']),
                       ('execution_evidence', ['../outside-closing-witness.json']),
                       ('execution_evidence', [str(Path(json.__file__).resolve())]),
                       ('execution_evidence', [execution_reference, './' + execution_reference])):
        changed = deepcopy(positive)
        changed['closing_witness']['model_execution'][0][key] = value
        must_reject(changed, f'A certificate {key}={value!r}')
    for field in ('k_bundles', 'season_execution'):
        changed = deepcopy(positive)
        row = changed['closing_witness'][field]
        if isinstance(row, list):
            row = row[0]
        row['verdict'] = 'HOLD'
        must_reject(changed, f'{field} HOLD cannot certify recorded season')
    changed = deepcopy(positive)
    changed['closing_witness']['model_execution'][0]['verdict'] = 'HOLD'
    must_reject(changed, 'one A HOLD blocks all K/season')
    changed = deepcopy(positive)
    changed['closing_witness']['k_bundles'][0]['verdict'] = 'HOLD'
    changed.update(k_closed=list(K_IDS[1:]), season_selected=False)
    partial = evaluate(changed)
    assert partial['K_closed'] == 3 and partial['season_selected'] is False
    changed = deepcopy(positive)
    changed['legal_proofs'][0]['complete_domain'] = False
    must_reject(changed, 'one F HOLD blocks final A/K/season')
    changed.update(k_closed=[], season_selected=False)
    blocked = evaluate(changed)
    assert blocked['K_closed'] == 0 and all(v == 'HOLD' for v in blocked['A_execution'].values())
    changed = deepcopy(positive)
    changed['closing_witness']['season_execution']['season'] = '2021-22'
    must_reject(changed, 'wrong season')
    for key, value in (('manuscript_allowed', True), ('season_selected', 1), ('k_closed', True)):
        changed = deepcopy(positive)
        changed[key] = value
        must_reject(changed, f'invalid recorded {key}')
    changed = deepcopy(positive)
    changed['closing_witness']['schema_version'] = True
    must_reject(changed, 'boolean schema version')
    print('S2 closing controls PASS: synthetic future closure; F/A/K dependencies, unique ids, certificates, evidence scope, flag consistency, initial snapshot and manuscript prohibition')


def check(*, initial_snapshot=False):
    data = json.loads(REGISTER.read_text(encoding='utf-8'))
    print(json.dumps(evaluate(data, initial_snapshot=initial_snapshot), ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--initial-snapshot', action='store_true',
                        help='Also enforce the historical unclosed S2 transition snapshot')
    args = parser.parse_args()
    if args.self_test:
        self_test()
    check(initial_snapshot=args.initial_snapshot)
