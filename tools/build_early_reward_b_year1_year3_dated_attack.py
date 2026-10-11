"""Dated B attack budgets from preserved roles and explicitly bounded priors.

Mirror observations are secondary evidence, not fresh NBA primary certification.
The conserved envelope is the previous working attack model at selected minutes,
not an invariant historical game cap. No scoreboard or rating delta is inferred.
"""
import argparse
from collections import defaultdict
import csv
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from build_early_reward_b_year2_dated_shots import read, sha, csvrows, csvbytes, jsonbytes, rounded
from build_early_reward_b_growth_and_year4_attack import coherent

ROOT = Path(__file__).resolve().parents[1]
RAW = 'research/raw/EARLY_REWARD_B_YEAR1_YEAR3_MIRROR_BOXES_2026_10_12.csv'
PROVENANCE = 'research/raw/EARLY_REWARD_B_YEAR1_YEAR3_SOURCE_SCOPE_2026_10_12.json'
MODEL = 'simulation/EARLY_REWARD_B_YEAR1_YEAR3_DATED_ATTACK_2026_10_12.json'
CSV = 'simulation/EARLY_REWARD_B_YEAR1_YEAR3_DATED_ATTACK_2026_10_12.csv'
ROOKIE = 'simulation/LC1_CHICAGO_2018_2019_USED_DEVELOPMENT_AND_RESULT_CONTACT_IMPLEMENTATION_2026_10_09.json'
OVERLAY = 'simulation/NBA_2020_21_SELECTED_REGULAR_OVERLAY.json'
OLD1 = 'simulation/CHICAGO_2018_19_OUTCOME_LEDGER.csv'
PRIOR3 = 'simulation/CHICAGO_2020_21_POSTDEADLINE_OBSERVED_PRIORS.csv'
PRE3 = 'simulation/CHICAGO_2020_21_PREDEADLINE_PAIRED_OBSERVATIONS.csv'
POST3 = 'simulation/CHICAGO_2020_21_POSTDEADLINE_BOTH_TEAMS_ACTUAL.csv'
B = 'simulation/EARLY_REWARD_B_GROWTH_AND_YEAR4_ATTACK_2026_10_11.json'
AUTHOR = 'canon/EARLY_REWARD_B_AUTHOR_SELECTION_2026_10_11.json'
FIELDS = {'fgm': 'fieldGoalsMade', 'fga': 'fieldGoalsAttempted',
          'three_pm': 'threePointersMade', 'three_pa': 'threePointersAttempted',
          'ftm': 'freeThrowsMade', 'fta': 'freeThrowsAttempted', 'tov': 'turnovers', 'pts': 'points'}
CATEGORIES = ('two_pa', 'three_pa', 'fta', 'tov')
W1 = {p: F(1, 5) for p in ['Zach LaVine', 'Lauri Markkanen', 'Wayne Selden', 'Shaquille Harrison', 'Antonio Blakeney']}
W3 = {'Zach LaVine': F(3, 10), 'LaMelo Ball': F(1, 4), 'Lauri Markkanen': F(1, 5),
      'Coby White': F(3, 20), 'Thaddeus Young': F(1, 10)}
PINS = [RAW, PROVENANCE, ROOKIE, OVERLAY, OLD1, PRIOR3, PRE3, POST3, B, AUTHOR,
        'simulation/CHICAGO_2020_21_PREDEADLINE_PRODUCTION_PRIORS.csv',
        'simulation/CHICAGO_2018_19_PLAYER_PRODUCTION_PRIORS.md',
        'research/raw/EARLY_REWARD_B_YEAR2_PRIMARY_BOXES_2026_10_11.csv']


def seconds(value):
    if not value:
        return 0
    minutes, second = value.split(':')
    total = F(minutes) * 60 + F(second)
    assert total.denominator == 1
    return int(total)


def collect(cache):
    records = json.loads((cache / 'mirror_download_receipt.json').read_text())
    all_rows = []
    for rec in records:
        data = (cache / rec['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == rec['sha256_raw']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == rec['git_blob_sha1']
        with (cache / rec['path']).open(encoding='utf-8-sig', newline='') as inp:
            for row in csv.DictReader(inp):
                if row['teamTricode'] == 'CHI' and row['season_year'] in ['2018-19', '2019-20', '2020-21']:
                    vals = {k: F(row[v]) for k, v in FIELDS.items()}
                    assert all(x.denominator == 1 for x in vals.values())
                    all_rows.append({'season': row['season_year'], 'date': row['game_date'],
                        'game_id': row['gameId'].zfill(10), 'player': row['personName'],
                        'seconds': seconds(row['minutes']), 'start': int(bool(row['position'])),
                        **{k: int(v) for k, v in vals.items()}})
    assert len({(r['season'], r['date'], r['player']) for r in all_rows}) == len(all_rows)
    index = {(r['season'], r['date'], r['player']): r for r in all_rows}
    clock_differences = []
    official = csvrows('research/raw/EARLY_REWARD_B_YEAR2_PRIMARY_BOXES_2026_10_11.csv')
    for obs in official:
        row = index[('2019-20', obs['date'], obs['player'])]
        assert all(row[k] == int(obs[k]) for k in FIELDS)
        if row['seconds'] != int(obs['seconds']):
            clock_differences.append({'date': row['date'], 'actor': row['player'],
                                     'mirror_minus_official_seconds': row['seconds'] - int(obs['seconds'])})
    retained = sorted([r for r in all_rows if r['season'] != '2019-20'],
                      key=lambda r: (r['season'], r['date'], r['player']))
    metadata = {'id': 'EARLY_REWARD_B_YEAR1_YEAR3_SOURCE_SCOPE_2026_10_12',
        'classification': 'PINNED_SECONDARY_NBA_V3_PUBLIC_MIRROR_NOT_NEW_PRIMARY_BOX_CERTIFICATION',
        'mirror_commit': 'a5f108b5b1f08074d78b9e8e901926a9ce4c06c5',
        'files': records, 'filtered_rows': len(retained),
        'year2_official_overlap': {'rows': len(official), 'FGM_FGA_3PM_3PA_FTM_FTA_TOV_PTS_equal': True,
                                 'path': 'research/raw/EARLY_REWARD_B_YEAR2_PRIMARY_BOXES_2026_10_11.csv',
                                 'LF_SHA256': sha('research/raw/EARLY_REWARD_B_YEAR2_PRIMARY_BOXES_2026_10_11.csv'),
                                 'clock_precision_differences': clock_differences,
                                 'scope_limit': 'Agreement on2019–20 fields does not certify all2018–19/2020–21 primary boxes; preserve77 clock differences.'},
        'fresh_primary': {'NBA_live_2020_12_23': '403_NO_BOX', 'NBA_PDF_2020_12_23': 'READ_TIMEOUT_NO_BOX'},
        'raw_hash_method': 'SHA256 raw download bytes; Git blobSHA1 includes blob header',
        'DNP_health_comment_transferred': False}
    return {RAW: csvbytes(retained), PROVENANCE: jsonbytes(metadata)}


def debit(values, amount, weights):
    result = dict(values)
    assert amount >= 0 and amount <= sum(result.values())
    remaining = amount
    while remaining:
        active = {p for p, v in result.items() if v > 0 and p in weights}
        if not active:
            active = {p for p, v in result.items() if v > 0}
        assert active
        total = sum(weights.get(p, F(1)) for p in active)
        wanted = remaining
        for p in sorted(active):
            cut = min(result[p], wanted * weights.get(p, F(1)) / total)
            result[p] -= cut
            remaining -= cut
    assert sum(values.values()) - sum(result.values()) == amount and min(result.values()) >= 0
    return result


def observed_rate(obs):
    scale = F(2160, int(obs['seconds']))
    two_a = F(obs['fga']) - F(obs['three_pa'])
    return {'two_pa': two_a * scale, 'three_pa': F(obs['three_pa']) * scale,
            'fta': F(obs['fta']) * scale, 'tov': F(obs['tov']) * scale,
            'two_p': (F(obs['fgm']) - F(obs['three_pm'])) / two_a if two_a else F(0),
            'three_p': F(obs['three_pm']) / F(obs['three_pa']) if F(obs['three_pa']) else F(0),
            'ft': F(obs['ftm']) / F(obs['fta']) if F(obs['fta']) else F(0)}


def build():
    assert json.loads(read(AUTHOR))['B']['selected_option'] == 'B'
    raw = csvrows(RAW)
    index = {(r['season'], r['date'], r['player']): r for r in raw}
    assert len(index) == len(raw), 'Duplicate observed actor/date'
    by_day = defaultdict(list)
    for r in raw:
        by_day[(r['season'], r['date'])].append(r)
        assert 2 * int(r['fgm']) + int(r['three_pm']) + int(r['ftm']) == int(r['pts'])
    assert all(len({r['game_id'] for r in rows}) == 1 for rows in by_day.values())
    rookie = json.loads(read(ROOKIE))
    returns = {r['date']: r for r in rookie['returned4_selected_receiver_rows']}
    extra = {r['date']: r for r in rookie['post33_selected_donor_rows']}
    old_proxy = {r['date']: r for r in csvrows(OLD1)}
    games = []
    precision1 = []
    six = {c['date']: c for c in rookie['six_C02_opponent_contacts']}
    for (season, day), obs in sorted(by_day.items()):
        if season != '2018-19':
            continue
        role = {r['player']: F(r['seconds']) for r in obs if int(r['seconds']) > 0}
        original_total = sum(role.values())
        hut = role.pop('Chandler Hutchison', F(0))
        role['Protagonist'] = hut
        p_start = int(index.get((season, day, 'Chandler Hutchison'), {}).get('start', 0))
        if day in returns:
            ret = returns[day]
            assert hut == seconds(ret['Hutch_removed'])
            assert sum(seconds(v) for v in ret['receivers'].values()) == hut
            role['Protagonist'] = F(0)
            p_start = 0
            for p, value in ret['receivers'].items():
                assert role.get(p, 0) > 0
                role[p] += seconds(value)
        if day in extra:
            entry = extra[day]
            assert hut == 0 and sum(d['debit_minutes'] for d in entry['donors']) == entry['P_minutes']
            role['Protagonist'] += entry['P_minutes'] * 60
            for d in entry['donors']:
                role[d['actor']] -= d['debit_minutes'] * 60
                assert role[d['actor']] >= 0
        assert sum(role.values()) == original_total
        if day in six:
            contact = six[day]
            for p, minutes in contact['historical_CHI_minutes'].items():
                assert int(index.get((season, day, p), {}).get('seconds', 0)) == seconds(minutes)
            assert {p: role.get(p, F(0)) for p in contact['selected_CHI_minutes']} == {p: F(seconds(v)) for p, v in contact['selected_CHI_minutes'].items()}
        old_seconds = round(float(old_proxy[day]['protagonist_minutes']) * 60)
        if old_seconds != role['Protagonist']:
            precision1.append({'date': day, 'legacy_proxy_seconds': old_seconds,
                               'selected_exact_seconds': int(role['Protagonist'])})
        games.append({'year': 1, 'season': season, 'date': day, 'game_id': obs[0]['game_id'],
                      'role': role, 'P_start': p_start, 'selected_clock_gap_seconds': None,
                      'lineup_witness_replayed': False})
    selected3 = sorted([g for g in json.loads(read(OVERLAY))['team_games'] if g['team'] == 'CHI'], key=lambda g: g['date'])
    for g in selected3:
        role = {p: F(str(s)) for p, s in g['player_seconds'].items() if s > 0}
        obs = by_day[('2020-21', g['date'])]
        games.append({'year': 3, 'season': '2020-21', 'date': g['date'], 'game_id': obs[0]['game_id'],
                      'role': role, 'P_start': int('Protagonist' in g['starters']),
                      'selected_clock_gap_seconds': str(sum(role.values()) - F(g['required_total_seconds'])),
                      'lineup_witness_replayed': False})
    assert len([g for g in games if g['year'] == 1]) == 82
    assert len(selected3) == 72
    assert sum(g['role'].get('Protagonist', F(0)) for g in games if g['year'] == 1) == 76442
    assert sum(g['role'].get('Protagonist', F(0)) > 0 for g in games if g['year'] == 1) == 73
    assert sum(g['P_start'] for g in games if g['year'] == 1) == 11
    # Historical observations are inputs, not certification of alternate efficiency.
    post_prior = {r['player']: r for r in csvrows(PRIOR3)}
    old = {1: coherent('9.5', '.500', '2.3', '.280', '4', '.700', '1.8'),
           3: coherent('14.5', '.555', '3.6', '.335', '5.4', '.750', '2.3')}
    new = {1: coherent(F(584 * 2160, 76442), '.530', '2.3', '.280', '4', '.700', '1.8'),
           3: coherent('21.1', '.580', '3.6', '.335', '5.4', '.750', '2.3')}
    # Consume the current B vectors, rather than merely attaching their hash.
    current = {r['NBA_year']: r['per36'] for r in json.loads(read(B))['growth_vectors']}
    for year in [1, 3]:
        for key in ['pts', 'ts', 'three_pa', 'three_p', 'fta', 'ft', 'tov']:
            assert abs(new[year][key] - F(str(current[year][key]))) < F(1, 100000000)
    base3 = next(r for r in csvrows('simulation/CHICAGO_2020_21_PREDEADLINE_PRODUCTION_PRIORS.csv')
                 if r['player'] == 'Protagonist' and r['scenario'] == 'BASE')
    assert F(base3['pts36']) == old[3]['pts'] and F(base3['ts']) == old[3]['ts']
    assert F(base3['three_pa36']) == old[3]['three_pa'] and F(base3['three_p']) == old[3]['three_p']
    lm = coherent('18', '.535', '6', '.335', '4', '.750', '3.7')
    output, dated, fallback, costs = [], [], [], defaultdict(F)
    p_seconds = defaultdict(F)
    p_points = defaultdict(F)
    for game in games:
        year, day, season = game['year'], game['date'], game['season']
        role = game['role']
        rates = {}
        for p, sec in role.items():
            if not sec:
                continue
            if p == 'Protagonist':
                rates[p] = old[year]
            elif p == 'LaMelo Ball':
                rates[p] = lm
            else:
                obs = index.get((season, day, p))
                if obs and int(obs['seconds']) > 0:
                    rates[p] = observed_rate(obs)
                else:
                    assert year == 3 and day > '2021-03-24'
                    prior = post_prior[p]
                    assert prior['last_observed_date'] <= '2021-03-24' < day
                    translated = dict(prior, three_pa=prior['fg3a'], three_pm=prior['fg3m'])
                    rates[p] = observed_rate(translated)
                    fallback.append({'date': day, 'actor': p, 'source': PRIOR3,
                                     'last_observed_date': prior['last_observed_date'],
                                     'classification': 'PRIOR_SCALED_TO_SELECTED_ROLE_NOT_SAME_DAY_CHI_BOX'})
        before = {p: {k: rates[p][k] * role[p] / 2160 for k in CATEGORIES} for p in rates}
        after = {p: dict(v) for p, v in before.items()}
        if role.get('Protagonist', 0):
            after['Protagonist'] = {k: new[year][k] * role['Protagonist'] / 2160 for k in CATEGORIES}
            demand = after['Protagonist']['two_pa'] - before['Protagonist']['two_pa']
            allocated = debit({p: v['two_pa'] for p, v in before.items() if p != 'Protagonist'}, demand, W1 if year == 1 else W3)
            for p, value in allocated.items():
                after[p]['two_pa'] = value
        for cat in CATEGORIES:
            assert sum(v[cat] for v in after.values()) == sum(v[cat] for v in before.values())
        team_before = team_after = F(0)
        for p in sorted(rates):
            a, b, r = after[p], before[p], new[year] if p == 'Protagonist' else rates[p]
            prev = 2 * b['two_pa'] * rates[p]['two_p'] + 3 * b['three_pa'] * rates[p]['three_p'] + b['fta'] * rates[p]['ft']
            pts = 2 * a['two_pa'] * r['two_p'] + 3 * a['three_pa'] * r['three_p'] + a['fta'] * r['ft']
            assert min(a.values()) >= 0
            costs[(year, p)] += pts - prev
            team_before += prev
            team_after += pts
            if p == 'Protagonist':
                p_seconds[year] += role[p]
                p_points[year] += pts
                assert pts == new[year]['pts'] * role[p] / 2160
            output.append({'NBA_year': year, 'date': day, 'game_id': game['game_id'], 'actor': p,
                'selected_seconds': rounded(role[p]),
                **{f'expected_{k}': rounded(v) for k, v in a.items()},
                'expected_fga': rounded(a['two_pa'] + a['three_pa']),
                **{f'delta_{k}': rounded(a[k] - b[k]) for k in CATEGORIES},
                'expected_two_pm': rounded(a['two_pa'] * r['two_p']),
                'expected_three_pm': rounded(a['three_pa'] * r['three_p']),
                'expected_ftm': rounded(a['fta'] * r['ft']), 'expected_pts': rounded(pts),
                'before_B_comparison_pts': rounded(prev), 'PTS_delta': rounded(pts - prev),
                'actual_box_or_game_result': False})
        dated.append({'NBA_year': year, 'date': day, 'game_id': game['game_id'],
                      'P_seconds': rounded(role.get('Protagonist', F(0))), 'P_start': game['P_start'],
                      'before_team_expected_pts': rounded(team_before), 'after_team_expected_pts': rounded(team_after),
                      'prior_model_envelope': {k: rounded(sum(v[k] for v in before.values())) for k in CATEGORIES},
                      'selected_clock_gap_seconds': game['selected_clock_gap_seconds'],
                      'new_court_or_actual_substitution_certified': False})
    # Existing observations are checked before using the mirror's additional fields.
    for obs in csvrows(PRE3):
        if obs['team'] == 'CHI':
            mirror = index[('2020-21', obs['date'], obs['player'])]
            assert int(obs['seconds']) == int(mirror['seconds']) and int(obs['pts']) == int(mirror['pts'])
    for obs in csvrows(POST3):
        if obs['team'] == 'CHI':
            mirror = index[('2020-21', obs['date'], obs['player'])]
            for k, mk in [('fgm', 'fgm'), ('fga', 'fga'), ('fg3m', 'three_pm'), ('fg3a', 'three_pa'),
                          ('ftm', 'ftm'), ('fta', 'fta'), ('pts', 'pts'), ('tov', 'tov')]:
                assert int(obs[k]) == int(mirror[mk])
    assert p_seconds[1] == 76442 and p_points[1] == 584
    pre = [g for g in dated if g['NBA_year'] == 3 and g['date'] <= '2021-03-24']
    post = [g for g in dated if g['NBA_year'] == 3 and g['date'] > '2021-03-24']
    early = [g for g in games if g['year'] == 3 and g['date'] < '2021-02-23']
    assert len(pre) == 43 and len(post) == 29 and len(early) == 30
    assert sum(F(str(g['P_seconds'])) for g in pre) == 73140
    assert abs(sum(F(str(g['P_seconds'])) for g in post) - 52200) < F(1, 100000)
    summary = {'id': 'EARLY_REWARD_B_YEAR1_YEAR3_DATED_ATTACK_2026_10_12',
        'status': 'DATED_WORKING_ATTACK_COACTOR_BUDGETS_IMPLEMENTED_RESULT_IMPACT_AND_RECOGNITION_PENDING',
        'source_sha256': {p: sha(p) for p in PINS}, 'source_classification': 'SECONDARY_MIRROR_PLUS_EXISTING_SELECTED_ROLE_AUTHORITY',
        'comparison_completions': {'rookie': 'Original9.5PTS36/.500 plus explicitly completedFTA4/FT.700; no historical FTA claim.',
                                   'year3': 'Original14.5PTS36/.555 plus completedFTA5.4/FT.750.',
                                   'LaMelo': 'OriginalBASE18PTS36/.535/3PA6/.335/TOV3.7 plus completedFTA4/FT.750 across both periods; no realCHA box copied.'},
        'team_envelope': 'Each dated pre-B working vector at selected role seconds. Conserved FGA/3PA/FTA/playerTOV; not historical invariant cap, actual possession limit, or NBA rule.',
        'category_scope': 'Only2PA transferred; selected P3PA/FTA/TOV per36 match the completed comparison. Other categories fixed within this conditional model, not demonstrated invariant in reality.',
        'coactor_conversion_assumption': 'Retain same-day observed finishing fractions or explicit preMar25 prior where no same-day positiveCHI sample. Retrospective expected attribution, not actor knowledge, training efficacy or causal forecast.',
        'weights': {'year1': {p: str(v) for p, v in W1.items()}, 'year3': {p: str(v) for p, v in W3.items()}},
        'year1': {'GP': 73, 'GS': 11, 'seconds': 76442, 'expected_pts': 584, 'expected_ppg': 8,
                  'legacy_4_second_gap': precision1, 'six_selected_C02_roles_preserved': True,
                  'old_donor_integer_reference_not_overwritten': True, 'new_injury_or_early_slot_restored': False},
        'year3': {'pre_games': 43, 'pre_minutes': 1219, 'post_games': 29,
                  'post_reference_minutes': rounded(p_seconds[3] / 60 - 1219),
                  'expected_pts_in_selected72_role_model': rounded(p_points[3]),
                  'expected_ppg_in_selected72_role_model': rounded(p_points[3] / 72),
                  'actual_historical_or_author_locked_full_season_box': False,
                  'before_Feb23_ET': {'games': 30, 'minutes': rounded(sum(g['role']['Protagonist'] for g in early) / 60),
                                     'P_expected_pts': rounded(sum(new[3]['pts'] * g['role']['Protagonist'] / 2160 for g in early)),
                                     'same_day_and_future_games_used_for_recognition': False}},
        'fallback_prior_uses': fallback, 'dates': dated,
        'coactor_and_P_point_changes': [{'NBA_year': year, 'actor': p, 'expected_pts_delta': rounded(value)}
                                       for (year, p), value in sorted(costs.items())],
        'guarded': {'new_REB_AST_award_rating_or_score': False, 'selected_year1_22_60_or_year3_31_41_recomputed': False,
                    'LaMelo_primary_PG_preserved': True, 'exact_substitution_or_whole_health_certified': False},
        'gates': {'freeze': 'v0.30 PARTIAL', 'design': 'CLOSED', 'manuscript': 'CLOSED', 'actual_Pack': 0},
        'remaining': ['Used result impact join and recognition competition/selection', 'C01 public path',
                      'Current9-act history/finalallocation/individualBlueprint/actualPack'],
        'unfinished_major_groups': 4, 'unfinished_through_group6': 3}
    return {MODEL: jsonbytes(summary), CSV: csvbytes(output)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--import-mirror', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.import_mirror:
        assert not args.check
        collected = collect(args.import_mirror)
        assert all(not (ROOT / p).exists() for p in [RAW, PROVENANCE, MODEL, CSV]), 'Refusing overwrite'
        for p, data in collected.items():
            (ROOT / p).write_bytes(data)
    outputs = build()
    if args.check:
        for p, data in outputs.items():
            assert (ROOT / p).read_bytes().replace(b'\r\n', b'\n') == data, p
    else:
        assert all(not (ROOT / p).exists() for p in outputs), 'Refusing overwrite'
        for p, data in outputs.items():
            (ROOT / p).write_bytes(data)
    print('PASS82rookie/72year3 dated budgets,73GP11GS1274:02/43+29 and four opportunity categories; impact/awards pending')
