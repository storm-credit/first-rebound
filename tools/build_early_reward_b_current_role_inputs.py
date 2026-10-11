"""Join existing non-scoring priors to B dated attack inputs, without award promotion."""
import argparse
import csv
import hashlib
import io
import json
import re
from collections import defaultdict
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = 'simulation/EARLY_REWARD_B_CURRENT_FULL_ROLE_INPUTS_2026_10_12'
BASE_MAIN = 'ba8c3a5610299b0c6f3d1939390aa6ace505b9c4'
SOURCES = [
    'simulation/CHICAGO_2018_19_PLAYER_PRODUCTION_PRIORS.md',
    'simulation/CHICAGO_2019_20_PRODUCTION_PRIORS.csv',
    'simulation/CHICAGO_2020_21_PREDEADLINE_PRODUCTION_PRIORS.csv',
    'simulation/CHICAGO_2021_22_GROWTH_INPUTS.json',
    'simulation/EARLY_REWARD_B_YEAR1_YEAR3_DATED_ATTACK_2026_10_12.csv',
    'simulation/EARLY_REWARD_B_YEAR2_DATED_SHOTS_2026_10_11.csv',
    'simulation/EARLY_REWARD_B_YEAR2_CREDIT_BUDGET_2026_10_11.json',
    'simulation/EARLY_REWARD_B_YEAR4_DATED_ATTACK_2026_10_11.csv',
    'design/EARLY_REWARD_B_RECOGNITION_COMPARISON_2026_10_12.json',
]


def normalized(path):
    return (ROOT / path).read_bytes().removeprefix(b'\xef\xbb\xbf').replace(b'\r\n', b'\n').replace(b'\r', b'\n')


def read(path):
    return json.loads(normalized(path))


def rows(path):
    return list(csv.DictReader(io.StringIO(normalized(path).decode())))


def amount(value):
    return format(D(value).quantize(D('0.000000001')), 'f')


def source_rates():
    text = normalized(SOURCES[0]).decode()
    first = {}
    for field, name in [('reb', 'TRB'), ('ast', 'AST'), ('stl', 'STL'), ('blk', 'BLK'), ('pf', 'PF')]:
        match = re.search(r'^\| ' + name + r' \|[^\n]+', text, re.M)
        assert match, (name, 'missing original prior table')
        first[field] = D(match.group().split('|')[3].strip().replace('*', ''))
    second = next(row for row in rows(SOURCES[1]) if row['scenario'] == 'BASE')
    third = next(row for row in rows(SOURCES[2]) if row['player'] == 'Protagonist' and row['scenario'] == 'BASE')
    fourth = next(row for row in read(SOURCES[3])['protagonist_candidates'] if row['id'] == 'P21A')
    result = {1: first}
    for year, source in [(2, second), (3, third), (4, fourth)]:
        result[year] = {field: D(str(source[field + '36'])) for field in first}
    return result


def build():
    rates = source_rates()
    attacks = {}
    made = defaultdict(D)
    for row in rows(SOURCES[4]):
        year, day = int(row['NBA_year']), row['date']
        made[(year, day)] += D(row['expected_two_pm']) + D(row['expected_three_pm'])
        if row['actor'] == 'Protagonist':
            attacks[(year, day)] = dict(row, seconds=row['selected_seconds'])
    clock2 = {row['date']: D(str(row['minutes_unchanged'])) * 60 for row in read(SOURCES[6])['P_game_expected_rows']}
    for year, path, actor_key in [(2, SOURCES[5], 'player'), (4, SOURCES[7], 'actor')]:
        for row in rows(path):
            day = row['date']
            made[(year, day)] += D(row['expected_two_pm']) + D(row['expected_three_pm'])
            if row[actor_key] == 'Protagonist':
                seconds = clock2[day] if year == 2 else D(row['regulation_minutes']) * 60
                attacks[(year, day)] = dict(row, seconds=str(seconds))
    outputs = []
    for (year, day), row in sorted(attacks.items()):
        seconds = D(row['seconds'])
        assert seconds > 0
        own_fg = D(row['expected_two_pm']) + D(row['expected_three_pm'])
        expected_ast = rates[year]['ast'] * seconds / 2160
        teammate_fg = made[(year, day)] - own_fg
        assert expected_ast <= teammate_fg, ('assist capacity', year, day, expected_ast, teammate_fg)
        output = {'NBA_year': year, 'date': day, 'game_id': row.get('game_id', row.get('event_id')), 'selected_seconds': str(seconds), 'expected_pts': row['expected_pts']}
        output.update({'expected_' + field: amount(value * seconds / 2160) for field, value in rates[year].items()})
        output.update({'expected_tov': row['expected_tov'], 'teammate_expected_FGM_capacity': amount(teammate_fg), 'assist_capacity_slack': amount(teammate_fg - expected_ast), 'source_non_scoring_prior': SOURCES[year - 1], 'classification': 'WORKING_FICTIONAL_ROLE_EXPECTATION_NOT_BOX_DEFENSIVE_IMPACT_OR_AWARD'})
        outputs.append(output)
    assert len(outputs) == 292
    assert len({(row['NBA_year'], row['game_id']) for row in outputs}) == len(outputs)
    summaries = []
    for year, name, start, end in [(1, 'YEAR1_73_ROLE_DATES', '', '2019-04-11'), (2, 'YEAR2_MIP_ELIGIBLE_65_DATES', '', '2020-03-12'), (3, 'YEAR3_ALLSTAR_PRIOR30', '', '2021-02-23'), (3, 'YEAR3_PREDEADLINE43', '', '2021-03-25'), (3, 'YEAR3_POSTDEADLINE29', '2021-03-25', '2021-05-17'), (3, 'YEAR3_SELECTED72_ROLE_MODEL', '', '2021-05-17'), (4, 'YEAR4_ALLSTAR_PRIOR50', '', '2022-02-03'), (4, 'YEAR4_REGULATION82', '', '2022-04-11')]:
        selected = [row for row in outputs if row['NBA_year'] == year and start <= row['date'] < end]
        sums = {field: sum(D(row['expected_' + field]) for row in selected) for field in ['pts', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf']}
        summaries.append({'NBA_year': year, 'scope': name, 'date_start_inclusive': start, 'date_end_exclusive': end, 'positive_role_dates': len(selected), 'seconds': str(sum(D(row['selected_seconds']) for row in selected)), 'expected_totals': {k: amount(v) for k, v in sums.items()}, 'expected_per_game': {k: round(float(v / len(selected)), 9) for k, v in sums.items()}, 'actual_integer_GP_GS_box_or_award': False})
    buffer = io.StringIO(newline='')
    writer = csv.DictWriter(buffer, fieldnames=list(outputs[0]), lineterminator='\n')
    writer.writeheader(); writer.writerows(outputs)
    csv_bytes = buffer.getvalue().encode()
    report = {
        'id': 'EARLY_REWARD_B_CURRENT_FULL_ROLE_INPUTS_2026_10_12',
        'baseline_main': BASE_MAIN,
        'status': 'B_ATTACK_AND_EXISTING_NONSCORING_PRIORS_DATED_JOIN_IMPLEMENTED_NOT_REALIZED_BOX_AWARD_OR_IMPACT_CERTIFICATE',
        'source_sha256': {path: hashlib.sha256(normalized(path)).hexdigest() for path in SOURCES},
        'rows': len(outputs), 'allocation_LF_SHA256': hashlib.sha256(csv_bytes).hexdigest(),
        'non_scoring_per36_working_inputs': {year: {k: str(v) for k, v in rate.items()} for year, rate in rates.items()},
        'selection_scope': 'Routine working carry of existing BASE years1–3 and P21A year4 non-scoring dimensions; B attack replaces only its own separately implemented scoring/shooting/TOV inputs. Not a promotion of old whole P21A or high scenario to final canon.',
        'summaries': summaries,
        'capacity_checks': {'P_assists_not_exceeding_teammate_expected_FGM_dates': len(outputs), 'assist_owner_assignment_or_whole_team_AST_cap_certified': False, 'P_self_assisted_basket_counted': False},
        'coactor_cost_scope': 'Date-specific B shooting costs remain in their existing authority. This join makes no additional P rebound/pass/steal/block gain versus the carried working non-scoring prior. No claim that teammate REB/AST stay unchanged in realized play or team event budgets are conserved.',
        'recognition_use': 'Compare scoring plus carried expected role contributions at original eligible cutoff; not an observed candidate record. Prior defensive events or rebounding do not establish POA mastery/defensive impact. First-year screen recovery and weak-hand failure remain.',
        'preserved': {'LM_primary_PG': True, 'Mark32_Caruso18_year4': True, 'year3_pre43_post29': True, '2019_2020_lottery_and_current_selected_results': True, 'original_sources_not_rewritten': True},
        'remaining': ['Joint team rebound/assist/opponent opportunity event budgets or a bounded explicit working assumption; no automatic box completion.', 'Total impact assumptions must be joined to the actual result consumer; do not map PTS/REB/STL directly to margin.', 'Counterfactual ballots and full East/West membership/position audit before exact personal selection.', 'C01 medal/year and admission outcome remain separate from mechanism question.', 'Final episode allocation/individual Blueprint/current Pack inputs.'],
        'gates': {'freeze': 'v0.30 PARTIAL', 'design': 'CLOSED', 'new_awards': 0, 'new_medal_selection': 0, 'manuscript': 0, 'actual_Pack': 0},
        'external_tools_this_pass': {'Antigravity': 'NOT_RUN', 'NotebookLM': 'NOT_RUN', 'Claude': 'NOT_RUN', 'independent_agent': 'NOT_RUN'},
        'unfinished_major_groups': 4, 'unfinished_through_group6': 3,
    }
    json_bytes = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode()
    return {STEM + '.csv': csv_bytes, STEM + '.json': json_bytes}, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    files, report = build()
    for path, raw in files.items():
        if args.check:
            assert normalized(path) == raw, ('replay differs', path)
        else:
            with (ROOT / path).open('xb') as handle:
                handle.write(raw)
    print(json.dumps({'status': 'PASS_WORKING_ROLE_REPLAY' if args.check else 'CREATED_WORKING_ROLE_INPUTS', 'dated_rows': report['rows'], 'source_pins': len(report['source_sha256']), 'summaries': report['summaries']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
