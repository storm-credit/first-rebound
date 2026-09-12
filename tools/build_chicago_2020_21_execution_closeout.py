"""L: source/date checks and four concrete postseason proposals; no canon lock."""
import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

from build_chicago_2020_21_postseason_routes import ALL, playin, record_groups

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'simulation'
OUT = S / 'CHICAGO_2020_21_EXECUTION_CLOSEOUT.json'
INPUTS = [
    S / 'CHICAGO_2020_21_SEASON_RECOMMENDATION.json',
    S / 'CHICAGO_2020_21_AVAILABILITY_POLICY.json',
    S / 'ORLANDO_2020_21_RETAINED_BACKUP_LINEUPS.json',
    ROOT / 'research/NBA_2020_21_L_EXECUTION_SOURCES.json',
    ROOT / 'canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json',
]


def matching_margin(extra_incoming=0, extra_outgoing=0):
    # Existing non-tax bracket is a premise, not a newly verified team status.
    return (Fraction(3767981) + Fraction(extra_outgoing)) * Fraction(7, 4) + 100000 - 6517981 - Fraction(extra_incoming)


def date_allowed(player, date):
    # Date consistency only: not roster, waiver clearance, cap or medical approval.
    windows = {
        'Donta Hall': [('2021-04-13', '2021-05-01'), ('2021-05-09', '2021-05-16')],
        'Moritz Wagner': [('2021-04-27', '2021-05-16')],
        'Jabari Parker': [('2021-04-16', '2021-05-16')],
        'JaVale McGee': [('2021-03-26', '2021-05-16')],
        'Robert Franks': [('2021-04-12', '2021-04-26')],
    }
    return any(a <= date <= b for a, b in windows[player])


def validate(data):
    assert not data['author_locked'] and not data['season_selected']
    assert not data['manuscript_allowed'] and not data['draw_selected']
    assert len(data['registration_date_checks']) == 140
    assert not [r for r in data['registration_date_checks'] if r['violation']]
    assert all(not r['registration_cleared'] for r in data['registration_date_checks'])
    assert len(data['postseason_proposals']) == 4
    for p in data['postseason_proposals']:
        assert not p['selected'] and p['classification'] == 'AUTHOR_EVENT_PROPOSAL_NOT_GAME_MODEL'
        assert len(p['lottery_teams']) == 14 and len(p['playoff_teams']) == 16
        assert not set(p['lottery_teams']) & set(p['playoff_teams'])
        assert set(p['lottery_teams']) | set(p['playoff_teams']) == ALL
        assert all(g['winner'] in [g['home'], g['away']] for g in p['east_games'] + p['west_games'])
        assert p['final_CHI_pick'] is None and p['final_MIN_pick'] is None
    assert {r['id'] for r in data['requirements']} == {'K_HEALTH', 'K_REGISTRATION', 'K_TRANSACTIONS', 'K_METHOD_EVENTS'}
    assert all(not r['closed'] for r in data['requirements'])
    assert data['matching']['margin_usd'] == 175985.75


def build():
    k, j, lineups, sources, approval = [json.loads(p.read_text()) for p in INPUTS]
    c = next(c for c in k['season_candidates'] if c['role'] == 'PRIMARY_RECOMMENDATION')
    assert c['base_case_id'] == 'F038' and c['team_wins']['CHI'] == 31
    assert len(c['regular_season_games']) == 1080 and sum(c['team_wins'].values()) == 1080
    checks = []
    source_ids = {'Donta Hall': 'L_HALL', 'Moritz Wagner': 'L_WAGNER',
                  'Jabari Parker': 'L_PARKER', 'JaVale McGee': 'L_MCGEE'}
    for group in j['followup_exposure']:
        if group['player'] not in source_ids:
            continue
        for row in group['calendar']:
            positive = row['target_minutes_low_high'][0] > 0  # K LOW only
            checks.append({'team': group['team'], 'player': group['player'],
                           'event_id': row['event_id'], 'positive': positive,
                           'source': source_ids[group['player']],
                           'violation': positive and not date_allowed(group['player'], row['event_id'][:10]),
                           'registration_cleared': False})
    for row in lineups['rows']:
        positive = row['control_minutes'].get('Robert Franks', 0) > 0
        checks.append({'team': 'ORL', 'player': 'Robert Franks', 'event_id': row['event_id'],
                       'positive': positive, 'source': 'L_WAGNER',
                       'violation': positive and not date_allowed('Robert Franks', row['event_id'][:10]),
                       'registration_cleared': False})
    east, west = playin(c['seeds']['EAST']), playin(c['seeds']['WEST'])
    direct = set(c['seeds']['EAST'][:6] + c['seeds']['WEST'][:6])
    # Four mutually exclusive event packages. Western results are a shared proposal.
    choices = [('L1', 1, 'Washington 첫 경기 탈락'),
               ('L2', 2, 'Washington 승리 뒤 Indiana 원정 탈락'),
               ('L3', 3, 'Washington·Indiana 연승, 8번시드 진출'),
               ('L4', 6, 'Washington 승리 뒤 Boston 원정 탈락')]
    proposals = []
    for pid, ei, name in choices:
        e, w = east[ei], west[1]
        playoff = direct | set(e['qualifiers'] + w['qualifiers'])
        lottery = ALL - playoff
        lottery_groups = record_groups(lottery, c['team_wins'])
        playoff_groups = record_groups(playoff, c['team_wins'], 15)
        chi = next(g for g in lottery_groups + playoff_groups if 'CHI' in g['teams'])
        min_group = next(g for g in lottery_groups if 'MIN' in g['teams'])
        proposals.append({'id': pid, 'name_ko': name, 'recommended': pid == 'L2', 'selected': False,
                          'classification': 'AUTHOR_EVENT_PROPOSAL_NOT_GAME_MODEL',
                          'east_games': e['games'], 'west_games': w['games'],
                          'east_qualifiers': e['qualifiers'], 'west_qualifiers': w['qualifiers'],
                          'lottery_teams': sorted(lottery), 'playoff_teams': sorted(playoff),
                          'lottery_record_groups': lottery_groups,
                          'CHI_in_lottery': 'CHI' in lottery, 'CHI_record_positions': chi['positions'],
                          'CHI_tied_teams': chi['teams'], 'MIN_record_positions': min_group['positions'],
                          'CHI_pick_owner_under_approved_no_vucevic_trade': 'CHI',
                          'MIN_owner_if_historical_obligation_adopted': {'picks_1_to_3': 'MIN', 'picks_4_plus': 'GSW'},
                          'MIN_obligation_adopted': False, 'final_CHI_pick': None, 'final_MIN_pick': None,
                          'score_or_box_score_inferred': False})
    requirements = [
        {'id': 'K_HEALTH', 'closed': False, 'status': 'CONCRETE_SCENARIO_RECOMMENDED',
         'next_ko': 'K1의 1079행 노출 달력 채택 여부. 주인공·LaMelo 각72 양수일과 Terry27 공백을 명시; 새 진단을 붙이지 않는다.'},
        {'id': 'K_REGISTRATION', 'closed': False, 'status': 'PRIMARY_DATES_RECOVERED_SLOT_EXCEPTION_CHARGE_HOLD',
         'next_ko': '등록 후속 장부에서 ORL 5/9 이후 일반계약16+투웨이2 및 Rivers 잔여시즌 본문을 확보했다. Hall 추가1자리의 허가·정확charge·다른팀 자리 실행을 처리한다.'},
        {'id': 'K_TRANSACTIONS', 'closed': False, 'status': 'PRIMARY_FACTS_PARTLY_RECOVERED_EXACT_FIELDS_HOLD',
         'next_ko': 'CHI 비납세 전제·당일 charge, Gordon 선행/후행1R, Fournier BOS 예외 잔액·픽 연도를 같은 장부로 완성한다.'},
        {'id': 'K_METHOD_EVENTS', 'closed': False, 'status': 'FOUR_EVENT_PACKAGES_L2_RECOMMENDED_NOT_ADOPTED',
         'next_ko': 'BPM F038·L2와 공통 서부 사건을 검토하고 실제 채택 후 동률/lottery·픽 소유를 확정한다.'},
    ]
    result = {'stage': 'O-15F14-L', 'status': 'PARTIAL_FACT_RECOVERY_AND_EVENT_PROPOSALS_FINAL_EXECUTION_HOLD',
              'baseline_main': 'c78fbe8b8055b2ace673ec5a349d37389cacacd6', 'baseline_pr': 155,
              'primary_source_bodies': len(sources['references']),
              'registration_date_checks': checks,
              'matching': {'premise': 'EXISTING_NON_TAX_175_PERCENT_PLUS_100K_NOT_NEW_CAP_CLEARANCE',
                           'margin_usd': float(matching_margin()), 'old_rounded_margin_usd': 175986,
                           'extra_incoming_charge_usd': None, 'extra_outgoing_charge_usd': None,
                           'exact_matching_cleared': False},
              'postseason_proposals': proposals, 'recommended_proposal': 'L2',
              'requirements': requirements, 'author_locked': False, 'season_selected': False,
              'draw_selected': False, 'manuscript_allowed': False,
              'independent_review': 'NOT_INDEPENDENT',
              'source_sha256': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in INPUTS}}
    validate(result)
    return result


if __name__ == '__main__':
    data = build()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'PASS': True, 'primary_bodies': data['primary_source_bodies'],
                      'date_checks': len(data['registration_date_checks']), 'event_proposals': 4,
                      'requirements_closed': 0, 'season_selected': False}))
