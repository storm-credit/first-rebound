"""Construct a bounded five-player clock witness for the fictional 11-minute vector."""

import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_a03_texas_tech_game_source_and_insertion as source_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('research/A03_TEXAS_TECH_FICTIONAL_STINT_WITNESS_2026_10_07.json')
MARKDOWN = OUTPUT.with_suffix('.md')
SOURCE = source_builder.OUTPUT
GUARDS = {'Jalen Brunson', 'Phil Booth', 'Donte DiVincenzo', 'Collin Gillespie'}
P = 'FICTIONAL_PROTAGONIST'

# Six fictional clock blocks are an existence witness, not 2018 substitutions.
# The first five-person block keeps the official starters. The protagonist's
# 11 minutes happen continuously in blocks three through five.
BLOCKS = (
    (16, ('Jalen Brunson', 'Eric Paschall', 'Mikal Bridges', 'Omari Spellman', 'Phil Booth')),
    (11, ('Jalen Brunson', 'Eric Paschall', 'Mikal Bridges', 'Donte DiVincenzo', 'Dhamir Cosby-Roundtree')),
    (1, ('Jalen Brunson', 'Phil Booth', 'Donte DiVincenzo', 'Dhamir Cosby-Roundtree', P)),
    (5, ('Jalen Brunson', 'Eric Paschall', 'Phil Booth', 'Donte DiVincenzo', P)),
    (5, ('Eric Paschall', 'Omari Spellman', 'Phil Booth', 'Donte DiVincenzo', P)),
    (2, ('Jalen Brunson', 'Omari Spellman', 'Phil Booth', 'Donte DiVincenzo', 'Collin Gillespie')),
)


def normalized_sha(path):
    raw = path.read_bytes()
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def source_record(root):
    source = json.loads((root / SOURCE).read_text(encoding='utf-8-sig'))
    # Validate the complete upstream artifact against both official raw caches
    # and its own producer; a same-total player-minute mutation is not enough.
    assert source == source_builder.build(root), 'source record differs from official-source construction'
    assert not source_builder.validate(source, root=root)
    assert source['independent_review_completed'] is True
    assert source['fictional_working_insertion']['fictional_score_or_all_player_box_verified'] is False
    return source


def construct(source):
    rows = source['fictional_working_insertion']['rows']
    targets = {row['player']: row['fictional_working_minutes'] for row in rows}
    assert len(targets) == len(rows) == 9
    original_starters = {row['player'] for row in rows if row['starter_preserved_from_official']}
    assert len(original_starters) == 5
    assert targets[P] == 11 and sum(targets.values()) == 200
    assert sum(duration for duration, _ in BLOCKS) == 40
    assert set(BLOCKS[0][1]) == original_starters and P not in BLOCKS[0][1]
    seen = {name: 0 for name in targets}
    clock = 0
    blocks = []
    for ordinal, (duration, lineup) in enumerate(BLOCKS, 1):
        assert isinstance(duration, int) and duration > 0
        assert len(lineup) == len(set(lineup)) == 5
        assert set(lineup) <= set(targets)
        guards = [name for name in lineup if name in GUARDS]
        assert guards, 'each minute needs at least one bounded ball-handling guard'
        assert clock + duration <= 40
        blocks.append({
            'block': ordinal, 'clock_start_minute': clock,
            'clock_end_minute': clock + duration, 'duration_minutes': duration,
            'five_on_court': list(lineup), 'guard_witnesses': guards,
            'protagonist_on_court': P in lineup,
            'evidence_class': 'FICTIONAL_CONSTRUCTIVE_CLOCK_ONLY_NOT_ACTUAL_STINT',
        })
        for name in lineup:
            seen[name] += duration
        clock += duration
    assert clock == 40 and seen == targets
    assert sum(len(block['five_on_court']) * block['duration_minutes'] for block in blocks) == 200
    assert blocks[0]['clock_start_minute'] == 0 and blocks[-1]['clock_end_minute'] == 40
    assert all(a['clock_end_minute'] == b['clock_start_minute'] for a, b in zip(blocks, blocks[1:]))
    return blocks, seen


def build(root=ROOT, source=None):
    trusted = source_record(root)
    if source is not None:
        assert source == trusted, 'injected source differs from official-source-bound record'
    blocks, totals = construct(trusted)
    return {
        'schema': 'A03_TEXAS_TECH_FICTIONAL_STINT_WITNESS_V1',
        'status': 'CONSTRUCTIVE_FIVE_PERSON_CLOCK_WITNESS_NOT_REAL_COACH_ROTATION',
        'independent_review_completed': True,
        'scope': 'ONE_VILLANOVA_TEXAS_TECH_2018_03_25_FICTIONAL_11_MINUTE_INSERTION',
        'source_record': str(SOURCE).replace('\\', '/'),
        'official_box_raw_source_rechecked_by_upstream_builder': True,
        'time_unit': 'FICTIONAL_INTEGER_MINUTE_BLOCK_NOT_OFFICIAL_SUBSTITUTION_TIMESTAMP',
        'blocks': blocks,
        'total_clock_minutes': 40, 'total_five_person_minutes': 200,
        'starting_five_preserved': True, 'fictional_protagonist_starts': False,
        'all_nine_exact_player_minutes': totals,
        'protagonist_minutes': totals[P], 'guard_present_every_block': True,
        'historical_box_first_lineup_and_integer_minute_display_used_as_model_inputs': True,
        'actual_2018_substitution_order_or_time_certified': False,
        'actual_play_by_play_or_possessions_certified': False,
        'coach_tactics_or_lineup_choice_certified': False,
        'historical_71_59_or_player_box_preserved_under_fictional_stints_certified': False,
        'historical_official_box_replaced': False,
        'technical_note': 'Six blocks are a short arithmetic witness; their lengths and order are fictional selections, not an inferred 2018 substitution chart.',
        'next_A03_F03_function_executed': False,
        'prior_practice_auto_proves_tournament_success': False,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'author_locked': False,
        'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {
            'tools/build_a03_texas_tech_fictional_stint_witness.py': normalized_sha(root / 'tools/build_a03_texas_tech_fictional_stint_witness.py'),
            str(SOURCE).replace('\\', '/'): normalized_sha(root / SOURCE),
        },
    }


def render(data):
    lines = [
        '# Texas Tech전 가상 11분의 5인 코트 시간표', '',
        '이 시간표는 2018년 [공식 경기 박스](https://villanova.com/sports/mens-basketball/stats/2017-18/texas-tech/boxscore/2694)의 선수별 정수 분과 선발을 입력으로 삼은 **가상 산술 증인**이다. 실제 교체 시점·감독 결정·포제션·점수 보존을 인증하지 않는다.', '',
        '| 가상 분 구간 | 5인 코트 | 가드 증인 |', '| --- | --- | --- |',
    ]
    for block in data['blocks']:
        lines.append(f"| {block['clock_start_minute']}–{block['clock_end_minute']} | "
                     f"{', '.join(block['five_on_court'])} | {', '.join(block['guard_witnesses'])} |")
    lines += [
        '', '- 원 선발 5인이 첫 블록에 있고 주인공은 벤치에서 시작한다. 매 구간 정확히 5인·가드 최소 1명이다.',
        '- 40분 내내 5인 = 팀 200분이며 공식 8인과 가상 주인공 1인의 분 합계가 앞선 11분 배분안과 정확히 같다.',
        '- 가상 주인공은 27–38분 구간에서 11분이다. 이 구간은 실제 2018 경기의 교체 증거가 아니다.',
        '- 원 박스의 정수 분 표시는 모델 입력이다. 원초 단위의 출전시각이나 실제 5인조 순서를 복구했다는 뜻이 아니다.',
        '- Paschall 14리바운드·Cosby-Roundtree 7리바운드·71–59는 보존 설계 목표이며 이 시간표만으로 대체 사건을 증명하지 않는다.',
        '- F03 장면·대표경기3 상한 확대·전체 G13/G14·Pack·원고는 실행/완료하지 않았다. 게이트 `CLOSED`.', '',
    ]
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source or construction: {exc}']
    return [] if data == expected else ['fictional stint witness differs from source-bound construction']


def self_test(data, root=ROOT):
    mutations = [
        ('lose a player minute', lambda d: d['blocks'][0].update(duration_minutes=15)),
        ('six on court', lambda d: d['blocks'][1]['five_on_court'].append(P)),
        ('remove guard', lambda d: d.update(guard_present_every_block=False)),
        ('start protagonist', lambda d: d.update(fictional_protagonist_starts=True)),
        ('certify real substitutions', lambda d: d.update(actual_2018_substitution_order_or_time_certified=True)),
        ('claim PBP', lambda d: d.update(actual_play_by_play_or_possessions_certified=True)),
        ('prepay F03', lambda d: d.update(next_A03_F03_function_executed=True)),
    ]
    for label, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed, root), label
    source = source_record(root)
    altered = copy.deepcopy(source)
    alt_rows = altered['fictional_working_insertion']['rows']
    # Total still 200, but one individual minute has moved without source support.
    alt_rows[0]['fictional_working_minutes'] -= 1
    alt_rows[1]['fictional_working_minutes'] += 1
    try:
        build(root, source=altered)
    except AssertionError:
        pass
    else:
        raise AssertionError('same-total source player-minute shift accepted')
    return len(mutations) + 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MARKDOWN).write_text(render(data), encoding='utf-8')
    errors = validate(data)
    if args.check:
        saved = json.loads((ROOT / OUTPUT).read_text(encoding='utf-8-sig'))
        errors += validate(saved)
        if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'current': not errors, 'errors': errors, 'negative_controls': tested,
                      'blocks': len(data['blocks']), 'clock_minutes': data['total_clock_minutes'],
                      'team_minutes': data['total_five_person_minutes'],
                      'protagonist_minutes': data['protagonist_minutes']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
