"""Conditional registered roster: count inactive/zero-minute contracts too."""
import json
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = [
    ROOT / 'simulation/ORLANDO_2020_21_RETAINED_BACKUP_LINEUPS.json',
    ROOT / 'simulation/CHICAGO_2020_21_AVAILABILITY_POLICY.json',
    ROOT / 'research/NBA_2020_21_L_REGISTRATION_SOURCES.json',
    ROOT / 'research/NBA_2020_21_L_EXECUTION_SOURCES.json',
]
OUT = ROOT / 'simulation/ORLANDO_2020_21_REGISTRATION_LEDGER.json'
START, END = '2021-04-12', '2021-05-16'
# Proposed carry-forward baseline, NOT proof of an alternate-world registration.
# Aminu stays under the no-Vucevic-trade branch, even with zero assigned minutes.
BASE_STANDARD = [
    'Al-Farouq Aminu', 'Chuma Okeke', 'Cole Anthony', 'Dwayne Bacon',
    'Gary Harris', 'James Ennis III', 'Jonathan Isaac', 'Markelle Fultz',
    'Michael Carter-Williams', 'Mo Bamba', 'Nikola Vucevic',
    'Terrence Ross', 'Zeke Nnaji',
]


def intervals():
    result = [{'player': p, 'type': 'STANDARD', 'start': START, 'end': END,
               'source': 'CONDITIONAL_CARRY_FORWARD_BASELINE'} for p in BASE_STANDARD]
    changes = [
        ('Devin Cannady', 'STANDARD', START, '2021-04-12', 'LR_HALL_APR13'),
        ('Robert Franks', 'STANDARD', START, '2021-04-26', 'L_WAGNER'),
        ('Donta Hall', 'STANDARD', '2021-04-13', '2021-05-01', 'L_HALL'),
        ('Moritz Wagner', 'STANDARD', '2021-04-27', END, 'L_WAGNER'),
        ('Ignas Brazdeikis', 'STANDARD', '2021-05-02', '2021-05-11', 'LR_BRAZDEIKIS'),
        ('Ignas Brazdeikis', 'STANDARD', '2021-05-12', END, 'LR_BRAZ_ROS'),
        ('Donta Hall', 'STANDARD', '2021-05-09', END, 'L_HALL'),
        ('Chasson Randle', 'TWO_WAY', START, END, 'LR_RANDLE'),
        ('Karim Mane', 'TWO_WAY', START, '2021-04-12', 'LR_MANE_WAIVED'),
        ('Devin Cannady', 'TWO_WAY', '2021-04-16', '2021-05-03', 'LR_CANNADY_TW'),
        ('Sindarius Thornwell', 'TWO_WAY', '2021-05-04', END, 'LR_THORNWELL'),
    ]
    result += [dict(zip(('player', 'type', 'start', 'end', 'source'), row)) for row in changes]
    return result


def roster_on(date, contracts=None):
    assert START <= date <= END
    active = [r for r in (intervals() if contracts is None else contracts)
              if r['start'] <= date <= r['end']]
    assert len(active) == len({r['player'] for r in active}), 'duplicate registered player'
    standard = sorted(r['player'] for r in active if r['type'] == 'STANDARD')
    two_way = sorted(r['player'] for r in active if r['type'] == 'TWO_WAY')
    return {'date': date, 'standard': standard, 'two_way': two_way,
            'standard_count': len(standard), 'two_way_count': len(two_way),
            'extra_standard_slots_needed': max(0, len(standard) - 15),
            'ordinary_count_pass': len(standard) <= 15 and len(two_way) <= 2,
            'alternate_hardship_approved': False, 'registration_cleared': False}


def validate(data):
    assert not any(data[k] for k in ('author_locked', 'season_selected', 'manuscript_allowed'))
    assert data['baseline_classification'] == 'CONDITIONAL_REGISTERED_CARRY_FORWARD_NOT_AUTHOR_LOCK'
    for epoch in data['epochs']:
        assert epoch == roster_on(epoch['date'], data['contracts'])
        assert epoch['two_way_count'] <= 2
        assert {'Al-Farouq Aminu', 'Jonathan Isaac', 'Markelle Fultz'} <= set(epoch['standard'])
    assert len(data['orl_game_checks']) == 19
    assert not any(r['unregistered_positive_players'] for r in data['orl_game_checks'])
    assert len(data['extra_slot_game_ids']) == 5
    assert data['extra_slot_game_ids'] == [r['event_id'] for r in data['orl_game_checks']
                                          if r['extra_standard_slots_needed']]
    assert len(data['rivers_date_checks']) == 28
    assert sum(r['positive'] for r in data['rivers_date_checks']) == 15
    assert not any(r['violation'] for r in data['rivers_date_checks'])
    assert not data['salary_route']['exact_charge_cleared']
    assert data['salary_route']['exact_charge_usd'] is None
    assert data['requirements_closed'] == 0


def build():
    lineups, policy, sources, old_sources = [json.loads(p.read_text()) for p in INPUTS]
    contracts = intervals()
    ids = {r['id'] for r in sources['references'] + old_sources['references']}
    assert all(c['source'] in ids | {'CONDITIONAL_CARRY_FORWARD_BASELINE'} for c in contracts)
    dates = sorted({c['start'] for c in contracts} | {'2021-04-13'})
    epochs = [roster_on(d) for d in dates]
    checks = []
    for row in lineups['rows']:
        date = row['event_id'][:10]
        if date < START:
            continue
        registered = roster_on(date)
        positive = sorted(p for p, minutes in row['control_minutes'].items() if minutes > 0)
        checks.append({'event_id': row['event_id'], 'positive_players': positive,
                       'unregistered_positive_players': sorted(set(positive) -
                           set(registered['standard'] + registered['two_way'])),
                       'extra_standard_slots_needed': registered['extra_standard_slots_needed'],
                       'registration_cleared': False})
    rivers = next(r for r in policy['followup_exposure'] if r['player'] == 'Austin Rivers')
    rivers_checks = []
    for row in rivers['calendar']:
        date = row['event_id'][:10]
        positive = row['target_minutes_low_high'][0] > 0
        window = 'TEN_DAY' if '2021-04-20' <= date <= '2021-04-29' else (
            'REST_OF_SEASON' if '2021-04-30' <= date <= END else None)
        rivers_checks.append({'event_id': row['event_id'], 'positive': positive,
                              'contract_window': window, 'violation': positive and window is None,
                              'source': 'LR_RIVERS', 'registration_cleared': False})
    data = {'stage': 'O-15F14-L_REGISTRATION_FOLLOWUP',
            'baseline_main': 'd7ec1fca506c380e10b4feceb37e073a3e4de1f6',
            'baseline_classification': 'CONDITIONAL_REGISTERED_CARRY_FORWARD_NOT_AUTHOR_LOCK',
            'scope': {'team': 'ORL', 'start': START, 'end': END,
                      'roster_occupancy_not_medical_eligibility': True},
            'contracts': contracts, 'epochs': epochs, 'orl_game_checks': checks,
            'extra_slot_game_ids': [r['event_id'] for r in checks if r['extra_standard_slots_needed']],
            'rivers_date_checks': rivers_checks,
            'salary_route': {'classification': 'RECOMMENDED_MINIMUM_EXCEPTION_CONTRACT_FORM_NOT_ACTUAL_TERMS',
                             'source': 'LR_CBA_MINIMUM', 'maximum_seasons': 2,
                             'bonuses_permitted': False, 'exact_charge_usd': None,
                             'exact_charge_cleared': False,
                             'roster_hardship_granted_by_salary_exception': False},
            'requirements_closed': 0, 'author_locked': False, 'season_selected': False,
            'manuscript_allowed': False, 'independent_review': 'NOT_INDEPENDENT',
            'source_sha256': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in INPUTS}}
    validate(data)
    return data


if __name__ == '__main__':
    result = build()
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'PASS': True, 'orl_games': 19, 'extra_slot_games': 5,
                      'rivers_dates': 28, 'rivers_positive_dates': 15,
                      'unregistered_positive_players': 0, 'registration_cleared': False}))
