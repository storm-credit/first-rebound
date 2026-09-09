"""O-15F8 conditional opponent minutes and paired RAPTOR sensitivity.

Default verifies saved witnesses without re-solving. --write solves new witnesses.
--raptor-source ingests a local 2021 RS by-team subset before writing.
No event selection, injury calendar, standings or final wins are produced.
"""
import argparse
import csv
import hashlib
import itertools
import json
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'simulation'
PREFIX = 'CHICAGO_2020_21_'
SNAP = S / (PREFIX + 'POSTDEADLINE_BOTH_TEAMS_ACTUAL.csv')
QUEUE = S / (PREFIX + 'POSTDEADLINE_OPPONENT_QUEUE.csv')
RATES = S / (PREFIX + 'POSTDEADLINE_OBSERVED_PRIORS.csv')
CHI = S / (PREFIX + 'POSTDEADLINE_LINEUP_AUDIT.json')
PRIORS = S / (PREFIX + 'PREDEADLINE_IMPACT_PRIORS.csv')
RAPTOR = S / (PREFIX + 'POSTDEADLINE_RAPTOR_RS.csv')
SUPPLEMENT = S / (PREFIX + 'POSTDEADLINE_SUPPLEMENT_OBSERVATIONS.csv')
OUT = S / (PREFIX + 'POSTDEADLINE_PAIRED_IMPACT.json')
METRICS = ('pts', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf')
VIRTUAL = 'Fictional Rival'
ROLES = {
    'GSW': {'center': ['Draymond Green', 'James Wiseman', 'Kevon Looney'],
            'handler': ['Stephen Curry', 'Jordan Poole', 'Nico Mannion', 'Draymond Green'],
            'wing': ['Andrew Wiggins', 'Kelly Oubre Jr.', 'Kent Bazemore', 'Damion Lee', 'Juan Toscano-Anderson', 'Mychal Mulder']},
    'MIN': {'center': ['Karl-Anthony Towns', 'Naz Reid'],
            'handler': ["D'Angelo Russell", 'Ricky Rubio', 'Jordan McLaughlin'],
            'wing': [VIRTUAL, 'Jaden McDaniels', 'Josh Okogie', 'Jarrett Culver', 'Juancho Hernangomez']},
    'CHA': {'center': ['Bismack Biyombo', 'Cody Zeller', 'Nick Richards', 'Vernon Carey Jr.', 'P.J. Washington'],
            'handler': ['Terry Rozier', "Devonte' Graham", 'Brad Wanamaker', 'Tyrell Terry', 'Malik Monk'],
            'wing': ['Anthony Edwards', 'Caleb Martin', 'Cody Martin', 'Jalen McDaniels', 'Miles Bridges', 'Nate Darling']},
    'DET': {'center': ['Isaiah Stewart', 'Jahlil Okafor', 'Tyler Cook'],
            'handler': ['Kira Lewis Jr.', 'Saben Lee', 'Frank Jackson'],
            'wing': ['Patrick Williams', 'Sekou Doumbouya', 'Deividas Sirvydis']},
    'TOR': {'center': ['Aron Baynes', 'Chris Boucher', 'Freddie Gillespie', 'Khem Birch'],
            'handler': ['Malachi Flynn', 'Jalen Harris', "DeAndre' Bembry", 'Pascal Siakam'],
            'wing': ['Norman Powell', 'O.G. Anunoby', 'Stanley Johnson', 'Yuta Watanabe', "DeAndre' Bembry"]},
    'BOS': {'center': ['Tristan Thompson', 'Luke Kornet', 'Tacko Fall', 'Grant Williams'],
            'handler': ['Kemba Walker', 'Marcus Smart', 'Payton Pritchard', 'Tremont Waters', 'Jayson Tatum', 'Carsen Edwards'],
            'wing': ['Evan Fournier', 'Jaylen Brown', 'Jayson Tatum', 'Aaron Nesmith', 'Romeo Langford', 'Semi Ojeleye', 'Jabari Parker']},
    'ORL': {'center': ['Nikola Vucevic', 'Donta Hall'],
            'handler': ['Cole Anthony', 'Michael Carter-Williams'],
            'wing': ['Gary Harris', 'James Ennis III', 'Terrence Ross', 'Dwayne Bacon', 'Chuma Okeke']},
}


def read(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(name):
    return ''.join(c for c in unicodedata.normalize('NFD', name) if not unicodedata.combining(c)).replace('’', "'").lower()


def ingest(path):
    rows = read(path)
    assert rows and all(r['season'] == '2021' and r['season_type'] == 'RS' for r in rows)
    assert len(rows) == len({(r['player_id'], r['team']) for r in rows})
    # Save the observed team rows: re-aggregation and scope remain independently auditable.
    fields = ['player_name', 'player_id', 'season', 'season_type', 'team', 'poss', 'mp', 'raptor_total']
    with RAPTOR.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        w.writerows({k: r[k] for k in fields} for r in sorted(rows, key=lambda r: (r['player_id'], r['team'])))


def actuals():
    groups = defaultdict(list)
    for r in read(SNAP):
        groups[(r['date'], r['team'])].append(r)
    return groups


def ingest_supplement(path):
    from build_chicago_2020_21_postdeadline_inputs import seconds, METRICS as columns
    rows = [r for r in read(path) if r['season_year'] == '2020-21' and r['personName'] == 'Kira Lewis Jr.' and r['game_date'] <= '2021-03-24' and seconds(r)]
    assert rows
    with SUPPLEMENT.open('w', newline='') as f:
        fields = ['date', 'game_id', 'player', 'team', 'seconds', *METRICS]
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        w.writerows({'date': r['game_date'], 'game_id': r['gameId'].zfill(10), 'player': r['personName'], 'team': r['teamTricode'], 'seconds': seconds(r),
                     **{k: int(float(r[v] or 0)) for k, v in columns.items()}} for r in sorted(rows, key=lambda r: r['game_date']))


def box_rates():
    rates = {r['player']: r for r in read(RATES)}
    rows = read(SUPPLEMENT)
    assert rows and len(rows) == len({(r['game_id'], r['player']) for r in rows})
    assert all(r['date'] <= '2021-03-24' and r['player'] == 'Kira Lewis Jr.' and r['team'] == 'NOP' and int(r['seconds']) > 0 for r in rows)
    sec = sum(int(r['seconds']) for r in rows)
    rates['Kira Lewis Jr.'] = {'seconds': sec, 'sample_status': 'LIMITED_UNDER_120_MIN' if sec < 7200 else 'OBSERVED_NOT_CAUSAL',
                             **{k + '36': sum(int(r[k]) for r in rows) * 2160 / sec for k in METRICS}}
    return rates


def baseline(rows):
    seconds = {r['player']: int(r['seconds']) for r in rows if int(r['seconds'])}
    delta = 14400 - sum(seconds.values())
    assert abs(delta) <= 2
    player = sorted(seconds, key=lambda p: (-seconds[p], p))[0] if delta else None
    if player:
        seconds[player] += delta
    return seconds, [r['player'] for r in rows if r['start'] == '1'], {'player': player, 'seconds': delta}


def move_balance(vector, choices):
    """Sequential named recipients/cost donors, with stated minute caps/floors."""
    balance = 14400 - sum(vector.values())
    moves = []
    for player, limit in choices:
        if not balance:
            break
        old = vector.get(player, 0)
        change = min(balance, max(0, limit * 60 - old)) if balance > 0 else -min(-balance, max(0, old - limit * 60))
        if change:
            vector[player] = old + change
            balance -= change
            moves.append({'player': player, 'seconds': change, 'limit_minutes': limit})
    assert balance == 0, (balance, choices, vector)
    return moves


def branch_specs():
    groups = actuals()
    result = []
    for q in read(QUEUE):
        date, team = q['date'], q['opponent']
        base, start, clock = baseline(groups[(date, team)])

        def add(name, removals=(), targets=None, balance_choices=(), swaps=None, assumptions=()):
            alt = dict(base)
            for player in removals:
                alt.pop(player, None)
            for player, minutes in (targets or {}).items():
                alt[player] = minutes * 60
            moves = move_balance(alt, balance_choices)
            starters = [(swaps or {}).get(p, p) for p in start]
            alt = {p: v for p, v in sorted(alt.items()) if v > 0}
            result.append({'event_id': q['event_id'], 'date': date, 'opponent': team, 'branch': name,
                           'scope': 'LIMITED_BASELINE_ASSUMPTION' if q['opponent_input_status'] == 'NO_NEW_DIRECT_CHANGE_IDENTIFIED' else 'CONDITIONAL_CHANGED_PATH',
                           'assumptions': list(assumptions), 'canon_evidence': q['canon_evidence'].split(';'),
                           'clock_correction': clock, 'actual_seconds': dict(sorted(base.items())),
                           'alternate_seconds': alt, 'starters': sorted(starters), 'balance_moves': moves,
                           'delta_seconds': {p: alt.get(p, 0) - base.get(p, 0) for p in sorted(set(base) | set(alt)) if alt.get(p, 0) != base.get(p, 0)}})

        if q['opponent_input_status'] == 'NO_NEW_DIRECT_CHANGE_IDENTIFIED':
            add('OBSERVED_OPPONENT_HELD', assumptions=['상대 실제 가용성·분·후속 거래를 이 경기의 제한적 기준선으로만 유지; 리그 전체 무영향 아님'])
        elif team == 'GSW':
            add('WIGGINS_CORE_HUTCHISON_INACTIVE', assumptions=['Russell–Wiggins 핵심 이동 유지 가정', 'Hutchison은 이 경기 비활성 가정; 행선지·가용성 사건 미확정'])
        elif team == 'MIN':
            for minutes in (24, 28, 32):
                add(f'RIVAL_{minutes}', ['Anthony Edwards'], {VIRTUAL: minutes},
                    [("D'Angelo Russell", 30), ('Ricky Rubio', 30), ('Jordan McLaughlin', 12)],
                    {'Anthony Edwards': VIRTUAL}, ['라이벌 등록·가용성 조건부', '라이벌 impact와 박스 실력은 미정 변수', 'Russell/Rubio 추가 분도 의료적 허용 시간 아님'])
        elif team == 'CHA':
            for minutes in (24, 28):
                add(f'EDWARDS_{minutes}_TERRY_6', ['LaMelo Ball', 'Grant Riller'], {'Anthony Edwards': minutes, 'Tyrell Terry': 6},
                    [('Caleb Martin', 12), ('Jalen McDaniels', 20), ('Cody Martin', 10)],
                    {'LaMelo Ball': 'Anthony Edwards'} if date == '2021-05-06' else {'Jalen McDaniels': 'Anthony Edwards'},
                    ['Edwards/Terry 등록·가용성 가정; 실제 타팀 부상/개인사 일정 복사 없음', 'Riller 미지명 후 Charlotte 미계약 조건; Richards/Carey 등록은 유지 조건'])
        elif team == 'DET':
            for patrick, kira in ((28, 20), (30, 24)):
                add(f'PATRICK_{patrick}_KIRA_{kira}', ['Saddiq Bey', 'Killian Hayes'], {'Patrick Williams': patrick, 'Kira Lewis Jr.': kira},
                    [('Saben Lee', 36), ('Sekou Doumbouya', 36), ('Tyler Cook', 30), ('Jahlil Okafor', 22), ('Deividas Sirvydis', 30)],
                    {'Saddiq Bey': 'Patrick Williams', 'Killian Hayes': 'Kira Lewis Jr.'},
                    ['Patrick/Kira 이 날짜 가용성 조건부', 'Frank Jackson 실제 8:16은 증분 배정하지 않음'])
        elif team == 'TOR':
            for minutes in (28, 32):
                choices = [('Yuta Watanabe', 32)] if date == '2021-04-08' else [("DeAndre' Bembry", 24), ('Stanley Johnson', 30), ('Jalen Harris', 24), ('Malachi Flynn', 40)]
                add(f'POWELL_RETAINED_{minutes}', ['Gary Trent Jr.', 'Rodney Hood'], {'Norman Powell': minutes}, choices,
                    {'Gary Trent Jr.': 'Norman Powell'} if date == '2021-04-08' else {'Yuta Watanabe': 'Norman Powell'},
                    ['Powell 대체 거래 결렬·Toronto 잔류·가용성 조건; Portland 실제 거래 무효가 잔류를 자동 확정하지 않음'])
        elif team == 'BOS':
            add('FOURNIER_PATH_RETAINED', assumptions=['Fournier 영입 및 Wagner 방출 등 실제 후속 경로를 조건부 유지'])
            add('NO_FOURNIER', ['Evan Fournier'], {},
                [('Payton Pritchard', 24), ('Aaron Nesmith', 24), ('Romeo Langford', 12), ('Carsen Edwards', 6), ('Grant Williams', 30)],
                {'Evan Fournier': 'Aaron Nesmith'}, ['Fournier 미영입 가정', 'Wagner 방출·Parker 영입은 별도 유지 조건', 'Grant Williams 소형 센터 역할을 허용하는 조합 정책'])
        elif team == 'ORL':
            for nnaji in (8, 12):
                add(f'VUCEVIC_STAYS_GORDON_A_NNAJI_{nnaji}', ['Wendell Carter Jr.', 'R.J. Hampton'], {'Nikola Vucevic': 30, 'Zeke Nnaji': nnaji, 'Donta Hall': 18},
                    [('Cole Anthony', 30), ('Michael Carter-Williams', 30)], {'Wendell Carter Jr.': 'Nikola Vucevic'},
                    ['Vučević 잔류·가용성, Aminu 잔류 0분 역할 조건', '미승인 Gordon A로 Harris/Nnaji 이동; 정확 급여·픽 실행 HOLD',
                     'Fournier 이탈 별도 조건', 'Hall 10일 계약과 가용성을 유지하는 추가 가정; Carter 부재만으로 자동 복원 금지', 'Nnaji는 PF 후보이며 전업 센터로 계산하지 않음'])
        else:
            raise AssertionError(team)
    return result


def valid(players, team):
    roles = ROLES[team]
    return len(players) == len(set(players)) == 5 and all(set(players) & set(names) for names in roles.values()) and len(set(players) & set(roles['center'])) <= 2


def solve(spec):
    import numpy as np
    from scipy.optimize import linprog
    players = list(spec['alternate_seconds'])
    lineups = [c for c in itertools.combinations(players, 5) if valid(c, spec['opponent'])]
    starts = tuple(spec['starters'])
    assert starts in lineups, (spec['date'], spec['branch'], starts)
    matrix = np.array([[int(p in c) for c in lineups] for p in players] + [[1] * len(lineups)])
    target = np.array([spec['alternate_seconds'][p] for p in players] + [2880])
    bounds = [(180 if c == starts else 0, None) for c in lineups]
    result = linprog(np.zeros(len(lineups)), A_eq=matrix, b_eq=target, bounds=bounds, method='highs')
    assert result.success, (spec['date'], spec['branch'], result.message)
    return [{'players': list(c), 'seconds': round(float(t), 8)} for c, t in zip(lineups, result.x) if t > 1e-6]


def rating_inputs():
    groups = defaultdict(list)
    for r in read(RAPTOR):
        assert r['season'] == '2021' and r['season_type'] == 'RS'
        groups[norm(r['player_name'])].append(r)
    values = {}
    for name, rows in groups.items():
        poss = sum(int(r['poss']) for r in rows)
        minutes = sum(int(r['mp']) for r in rows)
        assert poss > 0 and minutes > 0
        raw = sum(float(r['raptor_total']) * int(r['poss']) for r in rows) / poss
        values[name] = {'source_player': rows[0]['player_name'], 'player_id': rows[0]['player_id'],
                        'teams': [r['team'] for r in rows], 'possessions': poss, 'minutes': minutes,
                        'raw_raptor': raw, 'eb_1000': raw * minutes / (minutes + 1000)}
    return values


def impact(delta, ratings, virtual_ratings=None):
    known = 0.0
    terms = {}
    for p, seconds in delta.items():
        if abs(seconds) < 1e-7:
            continue
        if p == VIRTUAL:
            terms['rival_raptor_eb'] = seconds / 2880
        elif virtual_ratings and p in virtual_ratings:
            known += seconds / 2880 * virtual_ratings[p]
        else:
            assert norm(p) in ratings, p
            known += seconds / 2880 * ratings[norm(p)]['eb_1000']
    return known, terms


def box(delta, rates):
    known = dict.fromkeys(METRICS, 0.0)
    missing = {}
    limited = []
    for p, seconds in delta.items():
        if abs(seconds) < 1e-7:
            continue
        r = rates.get(p)
        if p == VIRTUAL or not r or not int(r['seconds']):
            missing[p] = seconds / 2160
            continue
        if r['sample_status'] == 'LIMITED_UNDER_120_MIN':
            limited.append(p)
        for k in METRICS:
            known[k] += seconds / 2160 * float(r[k + '36'])
    return {'known_delta': {k: round(v, 8) for k, v in known.items()},
            'missing_per36_coefficients': {k: round(v, 8) for k, v in missing.items()},
            'limited_sample_players': sorted(limited),
            'status': 'PARTIAL_SYMBOLIC_NO_ZERO_IMPUTATION' if missing else 'CONDITIONAL_ATTRIBUTION_NOT_SCORE'}


def build(witnesses):
    groups = actuals()
    ratings = rating_inputs()
    rates = box_rates()
    priors = {r['scenario']: r for r in read(PRIORS) if r['proxy'] == 'RAPTOR_EB'}
    branches = branch_specs()
    output = []
    used_players = set()
    for b in branches:
        b['lineup_witness'] = witnesses.get((b['date'], b['branch']))
        b['box_attribution'] = box(b['delta_seconds'], rates)
        constant, terms = impact(b['delta_seconds'], ratings)
        b['opponent_impact'] = {'constant': round(constant, 8), 'coefficients': {k: round(v, 8) for k, v in terms.items()}}
        used_players.update(p for p in b['delta_seconds'] if p != VIRTUAL)
    for g in json.loads(CHI.read_text())['games']:
        rows = groups[(g['date'], 'CHI')]
        base = {r['player']: int(r['seconds']) for r in rows}
        correction = g['clock_correction']
        if correction['player']:
            base[correction['player']] += correction['seconds']
        alt = g['minimum_change_candidate']['player_seconds']
        delta = {p: alt.get(p, 0) - base.get(p, 0) for p in set(base) | set(alt) if abs(alt.get(p, 0) - base.get(p, 0)) > 1e-7}
        assert abs(sum(delta.values())) < 1e-6
        used_players.update(p for p in delta if p not in ('Protagonist', 'LaMelo Ball'))
        for b in branches:
            if b['date'] != g['date']:
                continue
            actual_margin = sum(int(r['pts']) for r in rows) - sum(int(r['pts']) for r in groups[(g['date'], b['opponent'])])
            for scenario, prior in priors.items():
                chi_impact, _ = impact(delta, ratings, {'Protagonist': float(prior['protagonist_rating']), 'LaMelo Ball': float(prior['lamelo_rating'])})
                opp_constant, terms = impact(b['delta_seconds'], ratings)
                net = chi_impact - opp_constant
                output.append({'event_id': b['event_id'], 'date': b['date'], 'opponent': b['opponent'], 'branch': b['branch'],
                               'availability_scenario': g['scenario'], 'impact_scenario': scenario, 'actual_margin': actual_margin,
                               'chi_impact': round(chi_impact, 8), 'opponent_impact_constant': round(opp_constant, 8),
                               'paired_delta_constant': round(net, 8),
                               'paired_delta_coefficients': {k: round(-v, 8) for k, v in terms.items()},
                               'margin_proxy_constant': round(actual_margin + net, 8),
                               'opponent_margin_proxy_constant': round(-actual_margin - net, 8),
                               'status': 'SYMBOLIC_RETROSPECTIVE_SENSITIVITY' if terms else 'CONDITIONAL_RETROSPECTIVE_SENSITIVITY'})
    numeric = [g for g in output if not g['paired_delta_coefficients']]
    symbolic = [g for g in output if g['paired_delta_coefficients']]
    thresholds = [-g['margin_proxy_constant'] / g['paired_delta_coefficients']['rival_raptor_eb'] for g in symbolic]
    summary = {'numeric_inputs': len(numeric), 'symbolic_inputs': len(symbolic),
               'numeric_dates': len({g['date'] for g in numeric}),
               'numeric_sign_changes': sum((g['actual_margin'] > 0) != (g['margin_proxy_constant'] > 0) for g in numeric),
               'minimum_absolute_numeric_margin_proxy': min(abs(g['margin_proxy_constant']) for g in numeric),
               'rival_chi_positive_margin_requires_rating_below': {'minimum': min(thresholds), 'maximum': max(thresholds)},
               'box_branches_with_missing_rates': sum(bool(b['box_attribution']['missing_per36_coefficients']) for b in branches),
               'note': 'Thresholds are algebraic break-even points, not rival ability priors or selected outcomes'}
    inputs = {p.name: sha(p) for p in (SNAP, QUEUE, RATES, CHI, PRIORS, RAPTOR, SUPPLEMENT, Path(__file__))}
    return {'stage': 'O-15F8', 'status': 'CONDITIONAL_PAIRED_INPUT_PASS_OUTCOME_HOLD', 'input_sha256': inputs,
            'method': {'proxy': 'RAPTOR_EB', 'independent_families': 1, 'scope': '2021_RS_ALL_TEAMS_RETROSPECTIVE',
                       'source_url': 'https://github.com/fivethirtyeight/data/blob/master/nba-raptor/modern_RAPTOR_by_team.csv',
                       'supplement_source_url': 'https://github.com/NocturneBear/NBA-Data-2010-2024/blob/a5f108b5b1f08074d78b9e8e901926a9ce4c06c5/regular_season_box_scores_2010_2024_part_2.csv',
                       'supplement_cutoff': '2021-03-24',
                       'aggregation': 'possessions-weighted team ratings; minutes/(minutes+1000) shrink toward zero',
                       'normalization': 'sum(delta_seconds*rating/2880); 100 possessions per 48 minutes assumed',
                       'residual': 'actual_margin + chi_delta - opponent_delta; box attribution is never added',
                       'role_policy': 'coarse center/handler/wing coverage and <=2 listed center candidates; not NBA rule',
                       'opening_seconds': 180, 'lineup_order': 'existence witness only, no substitution chronology',
                       'interaction_and_pace_change': 'not estimated', 'canon_outcomes': False},
            'roles': ROLES, 'used_real_ratings': {p: ratings[norm(p)] for p in sorted(used_players)},
            'summary': summary, 'opponent_branches': branches, 'paired_inputs': output}


def verify(data):
    expected = branch_specs()
    assert len(expected) == 39 and len(data['paired_inputs']) == 234
    witnesses = {}
    for b, spec in zip(data['opponent_branches'], expected, strict=True):
        for k, v in spec.items():
            assert b[k] == v, (k, b['branch'])
        assert sum(b['alternate_seconds'].values()) == sum(b['actual_seconds'].values()) == 14400
        assert sum(b['delta_seconds'].values()) == 0
        assert len(set(b['starters'])) == 5
        assert all(0 < n <= 2880 for n in b['alternate_seconds'].values())
        for ref in b['canon_evidence']:
            assert (ROOT / ref).is_file(), ref
        witness = b['lineup_witness']
        if b['scope'] == 'LIMITED_BASELINE_ASSUMPTION':
            assert b['delta_seconds'] == {} and witness is None
            continue
        assert witness
        assert abs(sum(s['seconds'] for s in witness) - 2880) < 1e-5
        seconds = defaultdict(float)
        opening = 0
        for segment in witness:
            assert valid(segment['players'], b['opponent']) and segment['seconds'] > 0
            if set(segment['players']) == set(b['starters']):
                opening += segment['seconds']
            for p in segment['players']:
                seconds[p] += segment['seconds']
        assert opening >= 180 - 1e-5
        assert set(seconds) == set(b['alternate_seconds'])
        assert all(abs(seconds[p] - n) < 1e-5 for p, n in b['alternate_seconds'].items())
        witnesses[(b['date'], b['branch'])] = witness
    assert data == build(witnesses)
    assert len({b['date'] for b in expected}) == 29
    assert sum(b['scope'] == 'CONDITIONAL_CHANGED_PATH' for b in expected) == 20
    for g in data['paired_inputs']:
        assert abs(g['margin_proxy_constant'] + g['opponent_margin_proxy_constant']) < 1e-7
        assert abs(g['chi_impact'] - g['opponent_impact_constant'] - g['paired_delta_constant']) < 2e-8
        assert 'win' not in g and 'loss' not in g
    print('PASS: 39 opponent branches / 29 dates; 20 changed-path lineup witnesses; 234 paired impact inputs; no final outcomes')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raptor-source', type=Path)
    parser.add_argument('--supplement-source', type=Path)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    if args.raptor_source:
        assert args.write
        ingest(args.raptor_source)
    if args.supplement_source:
        assert args.write
        ingest_supplement(args.supplement_source)
    if args.write:
        witnesses = {(b['date'], b['branch']): solve(b) for b in branch_specs() if b['scope'] == 'CONDITIONAL_CHANGED_PATH'}
        data = build(witnesses)
        verify(data)
        OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n')
    else:
        verify(json.loads(OUT.read_text()))
