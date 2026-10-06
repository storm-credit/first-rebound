"""Complete the five approved C2 working vectors; never rerun rating screens.

Historical source seconds support arithmetic only. McGee availability and the
ordered LP stints below are delegated author models, not observed substitutions.
"""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import screen_denver_mcgee_nontrade as f5

ROOT = Path(__file__).resolve().parents[1]
BASE = 'simulation/NBA_2020_21_FINAL859_MINUTES.json'
F5 = 'simulation/DENVER_2020_21_MCGEE_NONTRADE_SCREEN.json'
C2 = 'simulation/CLEVELAND_2020_21_VAREJAO_OMISSION_SCREEN.json'
DIRECTION = 'canon/CLEVELAND_2021_VAREJAO_C2_DECISION.json'
PRIOR = 'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json'
AUTHORITY = 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
OUT = 'simulation/CLEVELAND_2020_21_C2_COMPLETE_WORKING_MINUTES.json'
SOURCES = [BASE, F5, C2, DIRECTION, PRIOR, AUTHORITY,
           'tools/screen_denver_mcgee_nontrade.py',
           'tools/screen_cleveland_varejao_omission.py',
           'tools/build_cleveland_c2_complete_working_minutes.py']
REMOVED = ('Anderson Varejao', 'Isaiah Hartenstein')


def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))


def sha(path):
    text = (ROOT/path).read_text(encoding='utf-8-sig')
    return hashlib.sha256(text.replace('\r\n', '\n').replace('\r', '\n').encode()).hexdigest()


def minutes_from_witness(witness):
    result = Counter()
    for stint in witness:
        if stint['seconds'] <= 0 or len(stint['players']) != 5 or len(set(stint['players'])) != 5:
            raise ValueError('positive unique-five witness required')
        result.update({p: stint['seconds'] for p in stint['players']})
    return dict(result)


def equal_minutes(a, b):
    return set(a) == set(b) and all(abs(a[p]-b[p]) < 1e-5 for p in a)


def build():
    source, prior, screen = read(BASE), read(F5), read(C2)
    if read(DIRECTION)['selected']['route'] != 'C2_VAREJAO_NO_RETURN_SIGNING':
        raise ValueError('approved C2 direction required')
    if 'do not execute' not in read(PRIOR)['selected']['F5_MCGEE']:
        raise ValueError('approved prior nontrade required')
    lookup = {(b['event_id'], b['team'], b['profile']): b
              for b in source['branches'] if b.get('rival_minutes') in (None, 28)}
    previous = {r['event_id']: r for r in prior['rows'] if r['team'] == 'CLE'}
    if len(previous) != 14:
        raise ValueError('fourteen prior CLE positive-minute substitutions required')
    # Check the stored 14 witnesses against the original vector, without
    # invoking the previous rating/season calculation or regenerating it.
    for gid, row in previous.items():
        branch = lookup[gid, 'CLE', 'OBSERVED_HELD']
        vector = branch['alternate_seconds'].copy()
        seconds = vector.pop('Isaiah Hartenstein')
        if seconds != row['seconds'] or 'JaVale McGee' in vector:
            raise ValueError('historical donor/prior screen mismatch')
        vector['JaVale McGee'] = seconds
        witness = row['candidate_lineup_witness']
        if not equal_minutes(vector, minutes_from_witness(witness)):
            raise ValueError('prior CLE witness does not conserve full vector')
        if abs(sum(w['seconds'] for w in witness)-branch['game_duration_seconds']) >= 1e-5:
            raise ValueError('prior CLE common clock mismatch')
    rows = []
    for row in screen['rows']:
        gid = row['event_id']
        branch = lookup[gid, 'CLE', 'OBSERVED_HELD']
        control = branch['alternate_seconds']
        varejao, hart = control.get(REMOVED[0], 0), control.get(REMOVED[1], 0)
        if (varejao, hart, varejao+hart) != (row['varejao_removed_seconds'],
                row['hartenstein_removed_seconds'], row['mcgee_candidate_seconds']):
            raise ValueError('C2 source amounts differ')
        if (gid in previous) != bool(hart):
            raise ValueError('C2/F5 overlap mismatch')
        vector = {p:n for p,n in control.items() if p not in REMOVED}
        if 'JaVale McGee' in vector:
            raise ValueError('McGee must replace donors once, not accumulate')
        vector['JaVale McGee'] = varejao+hart
        duration = branch['game_duration_seconds']
        if sum(vector.values()) != 5*duration or max(vector.values()) > duration:
            raise ValueError('full vector/player common-clock capacity')
        starters = branch['starters']
        if set(starters) & set(REMOVED):
            raise ValueError('removed donor in preserved starters')
        witness = f5.cleveland_lineup_witness(vector, starters, duration)
        if witness is None or not equal_minutes(vector, minutes_from_witness(witness)):
            raise ValueError('C2 declared-role full-vector witness missing')
        # Ordering is a new working coach selection: start with the selected
        # starting five, then stable name order. It is no historical chronology.
        witness.sort(key=lambda w: (sorted(w['players']) != sorted(starters), w['players']))
        clock, stints = 0.0, []
        for item in witness:
            end = clock+item['seconds']
            stints.append(dict(start_seconds=clock, end_seconds=end, **item))
            clock = end
        if abs(clock-duration) >= 1e-5 or stints[0]['seconds'] < 180-1e-5:
            raise ValueError('ordered full-clock/start-five witness failure')
        delta = {p:vector.get(p,0)-branch['actual_seconds'].get(p,0)
                 for p in sorted(set(vector)|set(branch['actual_seconds']))
                 if abs(vector.get(p,0)-branch['actual_seconds'].get(p,0)) > 1e-7}
        rows.append(dict(event_id=gid, team='CLE', date=branch['date'],
            source_profile='OBSERVED_HELD', game_duration_seconds=duration,
            actual_seconds=branch['actual_seconds'], source_control_seconds=control,
            alternate_seconds=vector, delta_seconds=delta, starters=starters,
            removed_players=list(REMOVED), modeled_available=sorted(vector),
            modeled_absent=[], reserve_health_unselected=None,
            varejao_removed_seconds=varejao, hartenstein_removed_seconds=hart,
            mcgee_candidate_seconds=varejao+hart,
            prior_f5_same_team_override_replaced=gid in previous,
            prior_f5_seconds_already_included=hart,
            overlay_operation='REPLACE_FULL_TEAM_VECTOR_DO_NOT_ADD_PRIOR_F5_AGAIN',
            lineup_witness=witness, ordered_working_stints=stints,
            health_classification='AUTHOR_DELEGATED_POSITIVE_MINUTE_AVAILABILITY_MODEL',
            coaching_classification='AUTHOR_DELEGATED_WORKING_STINT_ORDER_NOT_OBSERVED_SUBSTITUTIONS',
            actual_active_list_certified=False, medical_certified=False,
            legal_registration_cleared=False))
    if len(rows) != 5 or sum(r['varejao_removed_seconds'] for r in rows) != 2156:
        raise ValueError('five-game historical donor coverage mismatch')
    if sum(r['hartenstein_removed_seconds'] for r in rows) != 1525:
        raise ValueError('two-overlap historical donor coverage mismatch')
    if sum(r['mcgee_candidate_seconds'] for r in rows) != 3681:
        raise ValueError('retained McGee full five-game sum mismatch')
    return dict(status='FIVE_C2_COMPLETE_WORKING_TEAM_VECTORS_AND_ORDERED_STINTS_ROOT_REVIEW_PENDING',
        baseline_main='94a672bd', date_local='2026-10-07', authority=AUTHORITY,
        direction_sources=[DIRECTION, PRIOR], source_sha256={p:sha(p) for p in SOURCES},
        source_hash_convention='SHA256_UTF8_BOM_STRIPPED_CRLF_OR_CR_TO_LF_BYTES',
        input_join_key=['event_id','team'], units='SECONDS_NOT_MINUTES',
        working_design_selected_under_existing_delegation=True,
        scope='Five CLE dates only; replaces full team vector, including two prior F5 overlaps once.',
        fact='Preserved source donor seconds and the approved omission directions.',
        inference='Removed donor total can be assigned once to retained McGee within declared LP roles.',
        author_model='Positive-minute health availability and ordered working coach stints under existing delegation.',
        unverified='Counterfactual medical diagnosis, official active list, complete roster, contract receipt and actual game outcomes.',
        prior_cleveland_f5_witnesses_checked=14,
        cleveland_conditional_roles={k:sorted(v) for k,v in f5.CLE_ROLES.items()},
        rows=rows, complete_team_vectors=5, overlap_team_vectors=2,
        original_varejao_seconds=2156, prior_hartenstein_seconds=1525,
        retained_mcgee_seconds=3681, modeled_full_rosters_included=False,
        actual_registration_certified=False, medical_certified=False,
        whole_league_health_cleared=False, whole_legal_execution_cleared=False,
        season_selected=False, manuscript_allowed=False)


def validate(packet):
    if packet != build():
        raise ValueError('C2 complete model differs from source-linked reconstruction')


def negative_tests(packet):
    changes = [lambda p:p['rows'][0]['alternate_seconds'].__setitem__('JaVale McGee',1937),
        lambda p:p['rows'][0]['alternate_seconds'].__setitem__('Anderson Varejao',397),
        lambda p:p['rows'][0]['alternate_seconds'].__setitem__('Isaiah Hartenstein',770),
        lambda p:p['rows'][0]['ordered_working_stints'][0].__setitem__('end_seconds',99999),
        lambda p:p.__setitem__('medical_certified',True),
        lambda p:p.__setitem__('season_selected',True),
        lambda p:p.__setitem__('authority','invented-authority'),lambda p:p['rows'].pop()]
    for change in changes:
        altered=deepcopy(packet);change(altered)
        try:validate(altered)
        except ValueError:continue
        raise AssertionError('invalid C2 model accepted')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args();packet=build();validate(packet)
    if args.check:
        if read(OUT) != packet:raise ValueError('saved C2 packet stale')
    else:(ROOT/OUT).write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.self_test:negative_tests(packet)
    print('PASS: CLE5 complete vectors/stints, overlap2 once, McGee3681 seconds; overall health/legal/season HOLD')
