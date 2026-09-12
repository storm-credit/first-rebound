"""Public execution evidence and bounded arithmetic; no season/contract adoption."""
import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = [ROOT / p for p in (
    'research/NBA_2020_21_L_EXECUTION_TERMS_SOURCES.json',
    'simulation/ORLANDO_2020_21_REGISTRATION_LEDGER.json',
    'simulation/ORLANDO_2020_21_RETAINED_BACKUP_LINEUPS.json',
)]
OUT = ROOT / 'simulation/CHICAGO_2020_21_EXECUTION_TERMS.json'
FOUR = {'Michael Carter-Williams', 'Markelle Fultz', 'Jonathan Isaac', 'Terrence Ross'}


def allowance(outgoing, taxpayer):
    outgoing = Fraction(outgoing)
    conservative = outgoing * Fraction(5, 4) + 100000
    return conservative if taxpayer else max(
        min(outgoing * Fraction(7, 4) + 100000, outgoing + 5000000), conservative)


def hardship_evidence(sources, registration, lineups):
    prior = [r for r in lineups['rows'] if r['event_id'][:10] < '2021-05-09'][-3:]
    dates = [r['event_id'][:10] for r in prior]
    assert dates == ['2021-05-03', '2021-05-05', '2021-05-07']
    at_signing = next(e for e in registration['epochs'] if e['date'] == '2021-05-09')
    players = []
    for player in sorted(FOUR):
        injuries = [r for r in sources['injury_rows'] if r['player'] == player]
        boxes = [r for r in sources['final_box_absences'] if r['player'] == player]
        historical = all(any(r['date'] == d and r['status'] == 'OUT' for r in injuries)
                         and any(r['date'] == d and not r['did_play'] for r in boxes) for d in dates)
        minutes = [r['control_minutes'].get(player, 0) for r in prior]
        followup = [r['control_minutes'].get(player, 0) for r in lineups['rows']
                    if r['event_id'][:10] >= '2021-05-09']
        players.append({'player': player, 'standard_contract_in_proposed_roster': player in at_signing['standard'],
                        'historical_three_consecutive_injury_absences': historical,
                        'prior_dates': dates, 'K_prior_assigned_minutes': minutes,
                        'K_remaining_five_assigned_minutes': followup,
                        'zero_minutes_do_not_prove_medical_condition': True,
                        'commissioner_continuing_inability_determination': None})
    return {'rule': '2019 NBA By-Laws 6.08', 'players': players,
            'documentary_absence_prerequisite_supported': all(
                r['historical_three_consecutive_injury_absences'] and
                r['standard_contract_in_proposed_roster'] and not any(r['K_prior_assigned_minutes'])
                for r in players),
            'uses_porter_carter_or_twoway_as_one_of_four': False,
            'fixed_fourteen_day_period_in_cited_clause': False,
            'doctor_always_mandatory_under_cited_clause': False,
            'alternate_world_approval_recorded': False,
            'recommendation': 'CARRY_FORWARD_FOUR_DOCUMENTED_ABSENCES_AND_SEEK_HARDSHIP_APPROVAL',
            'may9_report_time_et': '17:30',
            'may9_report_is_pre_signing_authorization': False}


def build():
    sources, registration, lineups = [json.loads(p.read_text()) for p in INPUTS]
    salary = {r['player']: r for r in sources['salary_rows']}
    base = lambda p: salary[p]['base_usd']
    # Nnaji at alternate pick24, 120% base, no added bonuses: explicit prior premise.
    den_out = base('Gary Harris') + 2193480
    orl_out = base('Aaron Gordon') + base('Gary Clark')
    matching = []
    for team, outgoing, incoming, bonus in [
        ('DEN', den_out, orl_out, salary['Aaron Gordon']['reported_unlikely_usd']),
        ('ORL', orl_out, den_out, salary['Gary Harris']['reported_unlikely_usd']),
    ]:
        for mode, additional in [('BASE_ONLY', 0), ('ALL_REPORTED_INCENTIVES_INCOMING_STRESS', bonus)]:
            allowed = allowance(outgoing, taxpayer=True)
            matching.append({'team': team, 'mode': mode, 'outgoing_base_usd': outgoing,
                             'incoming_test_usd': incoming + additional,
                             'allowed_under_125_percent_plus_100k_usd': float(allowed),
                             'margin_usd': float(allowed - incoming - additional),
                             'outgoing_incentive_credit_taken': False,
                             'unknown_trade_bonus_covered': False,
                             'actual_taxpayer_or_hard_cap_status_verified': False,
                             'exact_trade_cleared': False})
    chi_out = base('Daniel Gafford') + base('Luke Kornet')
    chi_in = base('Daniel Theis') + base('Javonte Green')
    data = {'stage': 'O-15F14-L_EXECUTION_TERMS',
            'baseline_main': '1946a22e8b9724f2ab284d369794b557d9769cbf',
            'hardship': hardship_evidence(sources, registration, lineups),
            'gordon_matching': matching,
            'CHI_matching': {'outgoing_base_usd': chi_out, 'incoming_base_usd': chi_in,
                             'reported_incentive_columns_sum_usd': sum(
                                 salary[p]['reported_likely_usd'] + salary[p]['reported_unlikely_usd']
                                 for p in ['Daniel Gafford', 'Luke Kornet', 'Daniel Theis', 'Javonte Green']),
                             'non_tax_margin_usd': float(allowance(chi_out, False) - chi_in),
                             'taxpayer_margin_usd': float(allowance(chi_out, True) - chi_in),
                             'non_tax_team_premise_verified': False, 'exact_trade_cleared': False},
            'Fournier_TPE': {'historical_march16_TPE_usd': 28500000,
                             'remaining_if_unused_before_trade': [
                                 {'incoming_test_usd': x, 'remaining_usd': 28500000 - x}
                                 for x in [17000000, 17150000, 17450000]],
                             'trade_date_TPE_balance_verified': False,
                             'exception_means_no_team_salary_or_tax_cost': False},
            'Hall_cash': {'ORL_reported_contract_total_usd': sum(r['cash_usd'] for r in sources['hall_cash_contracts']),
                          'rest_of_season_reported_cash_usd': 79216,
                          'reported_zero_cap_hit_adopted': False, 'exact_team_charge_usd': None},
            'picks': {'public_terms': sources['public_pick_terms'],
                      'conditional_calendar_not_complete_stepien_certification': [
                          {'preceding_conveys': year,
                           'earliest_nonconsecutive_gordon_year_within_reported_window': max(2025, year + 2)}
                          for year in [2023, 2024, 2025]],
                      'exact_obligations_adopted': False},
            'author_locked': False, 'season_selected': False, 'manuscript_allowed': False,
            'requirements_closed': 0, 'independent_review': 'NOT_INDEPENDENT',
            'source_sha256': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in INPUTS}}
    validate(data)
    return data


def validate(data):
    assert not any(data[k] for k in ['author_locked', 'season_selected', 'manuscript_allowed'])
    h = data['hardship']
    assert {r['player'] for r in h['players']} == FOUR
    assert h['documentary_absence_prerequisite_supported']
    assert not h['alternate_world_approval_recorded']
    assert all(r['commissioner_continuing_inability_determination'] is None for r in h['players'])
    assert all(r['historical_three_consecutive_injury_absences'] for r in h['players'])
    assert all(not any(r['K_remaining_five_assigned_minutes']) for r in h['players'])
    assert len(data['gordon_matching']) == 4
    assert all(r['margin_usd'] >= 0 and not r['exact_trade_cleared'] for r in data['gordon_matching'])
    assert data['CHI_matching']['non_tax_margin_usd'] == 175985.75
    assert data['CHI_matching']['taxpayer_margin_usd'] < 0
    assert not data['CHI_matching']['exact_trade_cleared']
    assert not data['Hall_cash']['reported_zero_cap_hit_adopted']
    assert data['Hall_cash']['exact_team_charge_usd'] is None
    assert not data['picks']['exact_obligations_adopted']
    assert data['requirements_closed'] == 0


if __name__ == '__main__':
    data = build()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'PASS': True, 'hardship_four_absence_basis': True,
                      'gordon_matching_conditions': 4, 'CHI_non_tax_margin': 175985.75,
                      'exact_execution_cleared': False, 'requirements_closed': 0}))
