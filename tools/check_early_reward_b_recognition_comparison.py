"""Check source pins, award cutoffs, secondary cohorts and conference boundaries."""
import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = 'design/EARLY_REWARD_B_RECOGNITION_COMPARISON_2026_10_12.json'
COHORT_CUTOFFS = {'ROOKIE_2019': '2019-04-11', 'MIP_PREVIOUS': '2019-04-11', 'MIP_CUTOFF': '2020-03-12', 'ALLSTAR_2021': '2021-02-23', 'ALLSTAR_2022': '2022-02-03'}
P_CUTOFFS = {1: '2019-04-11', 2: '2020-03-12', 3: '2021-02-23', 4: '2022-02-03'}


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def rows(path):
    with (ROOT / path).open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def lf_hash(path):
    raw = (ROOT / path).read_bytes().removeprefix(b'\xef\xbb\xbf')
    return hashlib.sha256(raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n')).hexdigest()


def validate_cohorts(raw, aggregates):
    unique = set()
    for row in raw:
        assert row['cutoff_exclusive'] == COHORT_CUTOFFS[row['cohort']]
        key = (row['cohort'], row['actor'], row['game_id'])
        assert key not in unique, ('duplicate observation', key)
        unique.add(key)
        assert row['date'] < row['cutoff_exclusive'], ('future observation', row)
        assert int(row['observed_seconds']) > 0
        assert row['classification'] == 'PINNED_SECONDARY_OBSERVATION_NOT_SELECTED_WORLD_STATS'
    grouped = {(row['cohort'], row['actor']) for row in raw}
    assert grouped == {(row['cohort'], row['actor']) for row in aggregates}
    for item in aggregates:
        selected = [row for row in raw if (row['cohort'], row['actor']) == (item['cohort'], item['actor'])]
        assert len(selected) == item['games']
        assert sorted({row['actual_team'] for row in selected}) == item['actual_teams']
        for total, field in [('seconds', 'seconds'), ('points', 'pts'), ('rebounds', 'reb'), ('assists', 'ast')]:
            value = sum(int(row['observed_' + field]) for row in selected)
            assert value == item[total], (item['actor'], total)
            key = 'minutes' if total == 'seconds' else total
            expected = round(value / len(selected) / (60 if total == 'seconds' else 1), 6)
            assert abs(expected - item[key + '_per_game']) < 1e-7


def main():
    report = read(REPORT)
    for path, digest in report['source_sha256'].items():
        assert lf_hash(path) == digest, ('source pin', path)
    raw = rows('research/raw/EARLY_REWARD_B_RECOGNITION_COHORT_2026_10_12.csv')
    assert len(raw) == report['raw_rows']
    validate_cohorts(raw, report['cohort_rows'])
    mixed = rows('simulation/EARLY_REWARD_B_YEAR1_YEAR3_DATED_ATTACK_2026_10_12.csv')
    fourth = rows('simulation/EARLY_REWARD_B_YEAR4_DATED_ATTACK_2026_10_11.csv')
    second = read('simulation/EARLY_REWARD_B_YEAR2_CREDIT_BUDGET_2026_10_11.json')['P_game_expected_rows']
    assert [row['NBA_year'] for row in report['P_cutoff_contexts']] == [1, 2, 3, 4]
    for item in report['P_cutoff_contexts']:
        year = item['NBA_year']
        assert item['cutoff_exclusive'] == P_CUTOFFS[year]
        if year in [1, 3]:
            source = [row for row in mixed if row['NBA_year'] == str(year) and row['actor'] == 'Protagonist']
            secfield, ptsfield, multiplier = 'selected_seconds', 'expected_pts', 1
        elif year == 2:
            source = second
            secfield, ptsfield, multiplier = 'minutes_unchanged', 'B_expected_pts', 60
        else:
            source = [row for row in fourth if row['actor'] == 'Protagonist']
            secfield, ptsfield, multiplier = 'regulation_minutes', 'expected_pts', 60
        selected = [row for row in source if row['date'] < item['cutoff_exclusive'] and Decimal(str(row[secfield])) > 0]
        assert len(selected) == item['games']
        assert sum(Decimal(str(row[secfield])) * multiplier for row in selected) == Decimal(item['seconds'])
        points = sum(Decimal(str(row[ptsfield])) for row in selected)
        assert points == Decimal(item['expected_points'])
        assert round(float(points / len(selected)), 9) == item['expected_PPG']
        assert not item['rebounds_assists_defense_or_vote_evaluation_complete']
    third = [row for row in read('simulation/NBA_2020_21_SELECTED_REGULAR_OVERLAY.json')['regular_season_games'] if row['date'] < '2021-02-23' and 'CHI' in [row['home'], row['away']]]
    fourth = [row for row in read('simulation/CHICAGO_2021_22_SELECTED_RESULTS_LEDGER.json')['rows'] if row['date'] < '2022-02-03']
    assert report['P_cutoff_contexts'][2]['selected_CHI_record'] == [sum(row['winner'] == 'CHI' for row in third), sum(row['winner'] != 'CHI' for row in third)]
    assert report['P_cutoff_contexts'][3]['selected_CHI_record'] == [sum(row['working_regulation_result']['winner'] == 'CHI' for row in fourth), sum(row['working_regulation_result']['winner'] != 'CHI' for row in fourth)]
    sas = read('simulation/CHICAGO_SAN_ANTONIO_2021_22_SELECTED_KEEPER_RESULTS.json')
    derozan = next(row for row in sas['lawful_contract_family'] if row['player'] == 'DeMar DeRozan')
    assert derozan['route'] == 'VII6b2_FULL_BIRD' and derozan['new_nonoption_seasons'] == 5
    correction = report['conference_correction']
    assert correction['selected_DeRozan_team'] == 'SAS' and correction['conference'] == 'WEST'
    for row in correction['historical_East_guard_rank_top4']:
        assert (row['fan'] * 2 + row['players'] + row['media']) / 4 == row['weighted_score']
    routes = report['year4_mutually_exclusive_candidate_routes']
    assert len(routes) == 4 and len({row['id'] for row in routes}) == 4
    assert all(row['status'] == 'CANDIDATE' and len(set(row['East_guard_starters'])) == 2 for row in routes)
    assert [row['id'] for row in routes if row['recommended']] == ['A']
    assert report['gates']['new_personal_awards_selected'] == 0
    assert report['C01_fresh_confirmation']['selected_medal'] is None
    assert report['gates']['design'] == 'CLOSED' and report['gates']['manuscript'] == report['gates']['actual_Pack'] == 0
    print(json.dumps({'status': 'PASS_CODEX_DIRECT_CHECK_NOT_INDEPENDENT', 'source_pins': len(report['source_sha256']), 'dated_secondary_rows': len(raw), 'cohort_aggregates': len(report['cohort_rows']), 'P_cutoff_replays': 4, 'candidate_routes': 4}, ensure_ascii=False))


if __name__ == '__main__':
    main()
