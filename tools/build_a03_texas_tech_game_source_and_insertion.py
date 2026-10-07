"""Record the 2018 Texas Tech official box and a bounded fictional 11-minute vector."""

import argparse
import copy
import hashlib
import json
import re
import tempfile
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('research/A03_TEXAS_TECH_GAME_SOURCE_AND_INSERTION_2026_10_07.json')
MARKDOWN = OUTPUT.with_suffix('.md')
SOURCES = (
    'tools/build_a03_texas_tech_game_source_and_insertion.py',
    'research/VILLANOVA_ELIGIBILITY_ROTATION_MODEL.md',
    'control/COLLEGE_ARC_SCOPE_GATE.md',
    'design/A03_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'design/ACT_MAP.md',
)
VILLANOVA_URL = 'https://villanova.com/sports/mens-basketball/stats/2017-18/texas-tech/boxscore/2694'
TEXAS_TECH_PDF_URL = 'https://texastech.com/documents/download/2018/3/25/Game37TexasTech_Villanova.pdf'
VILLANOVA_HTML_SHA256 = 'b3c413c173e6d4d64b9250240997769c77df0e963ac817beec1b54c28810dade'
TEXAS_TECH_PDF_SHA256 = '40578ef36eddf935b708268c78ab7fa3ed1df3b2b7ffb2f9e8a6a0510db9648b'
HTML_CACHE = Path(tempfile.gettempdir()) / 'fr-a03-texastech-box-20261007.html'
PDF_CACHE = Path(tempfile.gettempdir()) / 'fr-a03-texastech-official-20261007.pdf'
HTML_BYTES = 1258731
PDF_BYTES = 205250
JERSEYS = ('01', '04', '25', '14', '05', '10', '21', '02')
HTML_NAMES = ('01 Brunson, Jalen', '04 Paschall, Eric', '25 Bridges, Mikal',
              '14 Spellman, Omari', '05 Booth, Phil', '10 DiVincenzo, Donte',
              '21 Cosby-Roundtree, Dhamir', '02 Gillespie, Collin')
PDF_NAMES = ('Brunson, J.', 'Paschall, E.', 'Bridges, M.', 'Spellman, O.',
             'Booth, P.', 'Divincenzo, D.', 'Cosby-Roundtree,D', 'Gillespie, C.')

# The eight positive-minute Villanova rows in both official game boxes; TEAM has 1 rebound.
OFFICIAL_ROWS = (
    ('Jalen Brunson', True, 36, 15, 6, 1, 5),
    ('Eric Paschall', True, 37, 12, 14, 6, 8),
    ('Mikal Bridges', True, 30, 12, 5, 1, 4),
    ('Omari Spellman', True, 26, 11, 6, 2, 4),
    ('Phil Booth', True, 31, 5, 4, 0, 4),
    ('Donte DiVincenzo', False, 26, 12, 8, 4, 4),
    ('Dhamir Cosby-Roundtree', False, 12, 4, 7, 5, 2),
    ('Collin Gillespie', False, 2, 0, 0, 0, 0),
)

# Fictional working choice: no exact substitution times or source play-by-play changes selected.
DONOR_MINUTES = {
    'Jalen Brunson': 1,
    'Eric Paschall': 0,
    'Mikal Bridges': 3,
    'Omari Spellman': 3,
    'Phil Booth': 2,
    'Donte DiVincenzo': 2,
    'Dhamir Cosby-Roundtree': 0,
    'Collin Gillespie': 0,
}


def normalized_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def source_bytes(root, path):
    return (root / path).read_bytes()


def verified_raw(path, expected_bytes, expected_sha):
    raw = path.read_bytes()
    assert len(raw) == expected_bytes, f'official raw byte count changed: {path}'
    assert hashlib.sha256(raw).hexdigest() == expected_sha, f'official raw SHA changed: {path}'
    return raw


def extract_html_rows(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    tables = [t for t in soup.find_all('table') if 'Villanova 71' in t.get_text(' ', strip=True)]
    assert len(tables) == 1, 'Villanova 71 full-game HTML table ambiguous'
    lines = [[c.get_text(' ', strip=True) for c in tr.find_all(['th', 'td'])]
             for tr in tables[0].find_all('tr')]
    assert lines[0] == ['##', 'Player', 'GS', 'MIN', 'FG', '3PT', 'FT', 'ORB-DRB',
                        'REB', 'PF', 'A', 'TO', 'BLK', 'STL', 'PTS']
    parsed = []
    for expected_jersey, expected_name in zip(JERSEYS, HTML_NAMES):
        cells = lines[len(parsed) + 1]
        assert cells[0] == expected_jersey
        assert cells[1] == expected_name
        surname, given = cells[1].removeprefix(expected_jersey + ' ').split(', ', 1)
        canonical_name = given + ' ' + surname
        offensive, defensive = map(int, cells[7].split('-'))
        parsed.append((canonical_name, cells[2] == '*', int(cells[3]), int(cells[14]),
                       int(cells[8]), offensive, defensive))
    assert lines[9][0] == 'TM' and int(lines[9][8]) == 1
    assert lines[10][1] == 'Totals' and (int(lines[10][3]), int(lines[10][8]),
                                             int(lines[10][14])) == (200, 51, 71)
    return tuple(parsed)


def extract_pdf_rows(path, html_rows):
    reader = PdfReader(str(path))
    assert len(reader.pages) == 1
    text = reader.pages[0].extract_text(extraction_mode='layout')
    assert '2018 NCAA East Regional Final' in text
    assert 'Texas Tech 59' in text and 'No. 2 Villanova 71' in text
    villanova = text.split('No. 2 Villanova 71', 1)[1]
    lines = villanova.splitlines()
    by_jersey = {}
    for line in lines:
        tokens = line.split()
        if not tokens or tokens[0] not in JERSEYS:
            continue
        number = tokens[0]
        assert number not in by_jersey, 'duplicate Villanova jersey in PDF'
        first_shot = next(i for i, token in enumerate(tokens) if re.fullmatch(r'\d+-\d+', token))
        is_starter = tokens[first_shot - 1] in ('f', 'g')
        stats = tokens[first_shot + 3:]
        assert len(stats) == 10 and all(item.isdigit() for item in stats)
        name = ' '.join(tokens[1:first_shot - int(is_starter)])
        by_jersey[number] = (name, is_starter, int(stats[-1]), int(stats[4]),
                             int(stats[2]), int(stats[0]), int(stats[1]))
    assert set(by_jersey) == set(JERSEYS)
    assert all(by_jersey[number][0] == expected for number, expected in zip(JERSEYS, PDF_NAMES))
    # The PDF uses abbreviated given names. The already parsed HTML row for the
    # same jersey supplies its full canonical name, never OFFICIAL_ROWS.
    parsed = tuple((html_row[0], *by_jersey[number][1:])
                   for number, html_row in zip(JERSEYS, html_rows))
    assert re.search(r'Team\s+1\s+0\s+1', villanova)
    assert re.search(r'Totals\s+19-57\s+4-24\s+29-35\s+20\s+31\s+51\s+17\s+71\s+7\s+12\s+4\s+6\s+200', villanova)
    return parsed


def build(root=ROOT):
    html_raw = verified_raw(HTML_CACHE, HTML_BYTES, VILLANOVA_HTML_SHA256)
    verified_raw(PDF_CACHE, PDF_BYTES, TEXAS_TECH_PDF_SHA256)
    html_rows = extract_html_rows(html_raw)
    assert html_rows == OFFICIAL_ROWS, 'HTML player rows changed'
    assert extract_pdf_rows(PDF_CACHE, html_rows) == OFFICIAL_ROWS, 'PDF player rows changed'
    rotation = source_bytes(root, SOURCES[1]).decode('utf-8-sig')
    scope = source_bytes(root, SOURCES[2]).decode('utf-8-sig')
    candidate = json.loads(source_bytes(root, SOURCES[3]).decode('utf-8-sig'))
    act_map = source_bytes(root, SOURCES[4]).decode('utf-8-sig')
    assert 'Paschall의 14리바운드와 Cosby-Roundtree의 7리바운드는 유지' in rotation
    assert '정확한 개인 리바운드·득점·교체 시점' in rotation
    assert '대표 경기 기능 | 3개' in scope and '40경기 전체 분·스탯 재계산' in scope
    assert '| A03 | 2017–18 | 맡은 역할의 크기 | 54 |' in act_map
    assert candidate['status'] == 'THREE_CONDITIONAL_FUNCTIONS_NOT_FINAL_G13'
    f03 = candidate['functions'][2]
    assert (f03['id'], f03['subact'], f03['function'], f03['opponent']) == (
        'A03-F03', 'A03-S3', 'Texas Tech 증명', 'Texas Tech')
    assert f03['observation_limit'] == 'Texas Tech는 기존 대표 경기; 실제 개인 기록/200분 재분배/교체초 HOLD'
    assert f03['choice'] == '맡은 상대의 박스아웃과 스위치 연결을 먼저 수행'
    assert candidate['final_episode_functions'] == 0
    assert len(OFFICIAL_ROWS) == 8 and sum(row[2] for row in OFFICIAL_ROWS) == 200
    assert sum(row[3] for row in OFFICIAL_ROWS) == 71
    assert sum(row[4] for row in OFFICIAL_ROWS) == 50  # plus one TEAM rebound = 51
    assert sum(row[1] for row in OFFICIAL_ROWS) == 5
    assert set(DONOR_MINUTES) == {row[0] for row in OFFICIAL_ROWS}
    assert sum(DONOR_MINUTES.values()) == 11
    assert DONOR_MINUTES['Eric Paschall'] == DONOR_MINUTES['Dhamir Cosby-Roundtree'] == 0

    historical = [
        {'player': name, 'starter': starter, 'minutes': minutes, 'points': points,
         'rebounds': rebounds, 'offensive_rebounds': offensive, 'defensive_rebounds': defensive,
         'evidence_class': 'OFFICIAL_2018_VILLANOVA_AND_TEXAS_TECH_GAME_BOX'}
        for name, starter, minutes, points, rebounds, offensive, defensive in OFFICIAL_ROWS
    ]
    alternate = [
        {'player': row['player'], 'historical_minutes': row['minutes'],
         'fictional_minute_delta': -DONOR_MINUTES[row['player']],
         'fictional_working_minutes': row['minutes'] - DONOR_MINUTES[row['player']],
         'starter_preserved_from_official': row['starter'],
         'historical_reference_points': row['points'],
         'historical_reference_rebounds': row['rebounds'],
         'fictional_points': None, 'fictional_rebounds': None,
         'evidence_class': 'FICTIONAL_MINUTE_VECTOR_NOT_REAL_BOX_OR_PBP'}
        for row in historical
    ]
    alternate.append({
        'player': 'FICTIONAL_PROTAGONIST', 'historical_minutes': 0,
        'fictional_minute_delta': 11, 'fictional_working_minutes': 11,
        'starter_preserved_from_official': False,
        'historical_reference_points': None, 'historical_reference_rebounds': None,
        'fictional_points': None, 'fictional_rebounds': None,
        'evidence_class': 'FICTIONAL_BENCH_FORWARD_WORKING_SELECTION',
    })
    assert len(alternate) == 9 and sum(row['fictional_working_minutes'] for row in alternate) == 200
    assert all(0 < row['fictional_working_minutes'] <= 40 for row in alternate)
    assert sum(row['starter_preserved_from_official'] for row in alternate) == 5
    assert next(row for row in alternate if row['player'] == 'Eric Paschall')['fictional_working_minutes'] == 37
    assert next(row for row in alternate if row['player'] == 'Dhamir Cosby-Roundtree')['fictional_working_minutes'] == 12
    return {
        'schema': 'A03_TEXAS_TECH_GAME_SOURCE_AND_INSERTION_V1',
        'status': 'OFFICIAL_BOX_VERIFIED_FICTIONAL_11_MINUTE_VECTOR_WORKING_NOT_PBP_CERTIFIED',
        'independent_review_completed': True,
        'scope': 'ONE_2018_03_25_REPRESENTATIVE_GAME_ONLY_NOT_40_GAME_SEASON',
        'historical_official': {
            'date': '2018-03-25', 'event': 'NCAA East Regional Final',
            'winner': 'Villanova', 'loser': 'Texas Tech', 'score': '71-59',
            'team_player_minutes': 200, 'positive_minute_villanova_players': 8,
            'villanova_starters': 5, 'villanova_points': 71,
            'villanova_player_rebounds': 50, 'villanova_team_rebounds': 1,
            'villanova_total_rebounds': 51,
            'texas_tech_points': 59, 'texas_tech_total_rebounds': 33,
            'rows': historical,
            'source_documents': [
                {'url': VILLANOVA_URL, 'publisher': 'Villanova Athletics',
                 'format': 'HTML official game box', 'table_selector': 'full-game Villanova 71 box, eight positive-minute rows',
                 'retrieved_date': '2026-10-07', 'temporary_raw_cache': str(HTML_CACHE), 'raw_bytes': HTML_BYTES,
                 'raw_sha256': VILLANOVA_HTML_SHA256},
                {'url': TEXAS_TECH_PDF_URL, 'publisher': 'Texas Tech Athletics',
                 'format': 'Official Basketball Box Score PDF, one page',
                 'table_selector': 'No. 2 Villanova 71 full-game box',
                 'retrieved_date': '2026-10-07', 'temporary_raw_cache': str(PDF_CACHE), 'raw_bytes': PDF_BYTES,
                 'raw_sha256': TEXAS_TECH_PDF_SHA256},
            ],
        },
        'fictional_working_insertion': {
            'selection_class': 'ROUTINE_DESIGN_CANDIDATE_NOT_FINAL_ALTERNATE_GAME_BOX',
            'protagonist_minutes': 11, 'protagonist_starter': False,
            'historical_positive_players': 8, 'fictional_positive_players': 9,
            'minute_donor_policy': 'Spread eleven minutes across five existing players; retain all five actual starters and keep Paschall/Cosby-Roundtree minutes untouched to protect their rebound anchor roles.',
            'rows': alternate,
            'team_player_minutes': 200,
            'preserved_historical_contribution_targets': [
                {'player': 'Eric Paschall', 'historical_rebounds': 14,
                 'fictional_target_rebounds': 14, 'minute_delta': 0,
                 'verification': 'DESIGN_TARGET_NOT_PLAY_BY_PLAY_PROVED'},
                {'player': 'Dhamir Cosby-Roundtree', 'historical_rebounds': 7,
                 'fictional_target_rebounds': 7, 'minute_delta': 0,
                 'verification': 'DESIGN_TARGET_NOT_PLAY_BY_PLAY_PROVED'},
            ],
            'historical_score_71_59_preservation_target': True,
            'fictional_score_or_all_player_box_verified': False,
            'five_person_stint_chronology_or_substitution_times_verified': False,
            'actual_play_by_play_events_kept_identical_claimed': False,
            'fictional_protagonist_points_rebounds_assigned': False,
            'actual_2018_game_box_replaced': False,
        },
        'next_A03_F03_boundary': {
            'status': 'SOURCE_CONNECTED_ROLE_PRESSURE_NOT_EXECUTED',
            'first_two_A03_practice_functions_auto_prove_tournament_success': False,
            'specific_switch_boxout_possession_or_real_player_reaction_selected': False,
            'exact_individual_box_or_substitution_times_require_further_PBP_review': True,
            'whole_A03_S3_or_F03_final_function_completed': False,
        },
        'mechanical_limits': [
            'The official eight rows were matched to the public Villanova HTML and Texas Tech PDF. Raw documents remain in a temporary cache, not in this repository.',
            'The 11-minute alternate vector is a fictional arithmetic witness only. It does not preserve historical play-by-play or prove a legal chronological five-player substitution schedule.',
            'Historical points and rebounds in the alternate rows are reference values, not certified alternate box statistics. Paschall 14 and Cosby-Roundtree 7 are selected preservation targets pending event-level review.',
            'The 71-59 result is the selected historical outcome target, not yet proved under the alternate minute/stint events.',
            'No complete 40-game Villanova season, 200-minute individual stint reconstruction or published episode is certified here.',
        ],
        'new_representative_games': 0, 'representative_function_cap': 3,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'author_locked': False,
        'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {p: normalized_sha(source_bytes(root, p)) for p in SOURCES},
    }


def render(data):
    official = data['historical_official']
    alternate = data['fictional_working_insertion']
    lines = ['# 2018 Villanova–Texas Tech 공식 박스와 가상 11분 삽입', '',
             '**범위:** NCAA East Regional Final 한 경기의 원자료와 가상 분 수지 증인. 원고·완성 대체세계 박스·실제 포제션 재구성은 아니다.', '',
             f"- 공식 기록: {official['date']} Villanova {official['score']} Texas Tech, Villanova 200 player-minutes·양수 선수 8명·선발 5명·리바운드 51(선수 50+TEAM 1).",
             '- 근거: [Villanova 공식 경기 박스](' + VILLANOVA_URL + '), [Texas Tech 공식 경기책 PDF](' + TEXAS_TECH_PDF_URL + '). 양쪽의 8명·분·득점·리바운드를 대조했다.', '',
             '- 원자료는 저장소 밖 임시 캐시에 있다. 생성·검사 시 두 파일의 바이트 수와 SHA-256을 재확인하고, 공식 표에서 선수별 분·선발·득점·리바운드를 다시 추출한다. 경로·해시는 JSON `historical_official.source_documents`에 기록했다.', '',
             '| 선수 | 공식 분 | 공식 선발 | 공식 득점 | 공식 리바운드 | 가상 분 차이 | 가상 작업 분 |',
             '| --- | ---: | --- | ---: | ---: | ---: | ---: |']
    official_by_name = {row['player']: row for row in official['rows']}
    for row in alternate['rows']:
        old = official_by_name.get(row['player'])
        lines.append(f"| {row['player']} | {row['historical_minutes']} | {'예' if old and old['starter'] else '아니오'} | "
                     f"{old['points'] if old else '—'} | {old['rebounds'] if old else '—'} | "
                     f"{row['fictional_minute_delta']:+d} | {row['fictional_working_minutes']} |")
    lines += ['', '- 실제 공식 양수 선수는 **8명**이고 가상 주인공을 넣은 작업본만 9명이다. 작업본 합계 200분, 기존 선발 5명 보존.',
              '- Paschall 14리바운드·Cosby-Roundtree 7리바운드는 핵심 공로 보존 목표이며 두 선수의 분은 감축하지 않았다. 대체 사건·박스의 검증된 기록이라고 주장하지 않는다.',
              '- 분 기증 선택은 Brunson 1, Bridges 3, Spellman 3, Booth 2, DiVincenzo 2분이다. 정확 교체 시점·5인조 시간표·PBP 연속성은 아직 검증하지 않았다.',
              '- 공식 71–59는 역사 결과와 작품의 보존 목표다. 바뀐 분 아래 정확 득점·리바운드·승패를 기계적으로 재현했다는 뜻은 아니다.',
              '- F03 Texas Tech 장면은 아직 실행하지 않았다. 앞 두 훈련 기능이 토너먼트에서 자동 성공을 보장하지 않으며 실제 상대·동료의 내면이나 실존 발언을 만들지 않는다.',
              '- 40경기 전수·대표 기능3 상한 확대·새 대표 경기·원고는 없다. 전체 G13/G14·Pack 미완료, 설계/원고 게이트 `CLOSED`.', '']
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['Texas Tech source/working vector differs from pinned evidence and arithmetic']


def self_test(data):
    global OFFICIAL_ROWS
    changes = [
        ('invent ninth official player', lambda d: d['historical_official'].update(positive_minute_villanova_players=9)),
        ('steal Paschall rebound', lambda d: d['fictional_working_insertion']['preserved_historical_contribution_targets'][0].update(fictional_target_rebounds=13)),
        ('break 200-minute total', lambda d: d['fictional_working_insertion']['rows'][0].update(fictional_working_minutes=34)),
        ('prepay exact stints', lambda d: d['fictional_working_insertion'].update(five_person_stint_chronology_or_substitution_times_verified=True)),
        ('turn official game into fiction', lambda d: d['fictional_working_insertion'].update(actual_2018_game_box_replaced=True)),
        ('prepay F03', lambda d: d['next_A03_F03_boundary'].update(whole_A03_S3_or_F03_final_function_completed=True)),
    ]
    for name, mutate in changes:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    # The total stays 71, but neither public box supports moving a point.
    original = OFFICIAL_ROWS
    try:
        changed_rows = list(original)
        first, second = list(changed_rows[0]), list(changed_rows[1])
        first[3] += 1
        second[3] -= 1
        changed_rows[0], changed_rows[1] = tuple(first), tuple(second)
        OFFICIAL_ROWS = tuple(changed_rows)
        assert sum(row[3] for row in OFFICIAL_ROWS) == 71
        try:
            build()
        except AssertionError:
            pass
        else:
            raise AssertionError('same-total official player-stat forgery passed construction')
    finally:
        OFFICIAL_ROWS = original
    try:
        changed_rows = list(original)
        bridges, booth = list(changed_rows[2]), list(changed_rows[4])
        bridges[0], booth[0] = booth[0], bridges[0]
        changed_rows[2], changed_rows[4] = tuple(bridges), tuple(booth)
        OFFICIAL_ROWS = tuple(changed_rows)
        try:
            build()
        except AssertionError:
            pass
        else:
            raise AssertionError('same-number swapped official player names passed construction')
    finally:
        OFFICIAL_ROWS = original
    return len(changes) + 2


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
                      'official_players': data['historical_official']['positive_minute_villanova_players'],
                      'working_players': data['fictional_working_insertion']['fictional_positive_players'],
                      'working_minutes': data['fictional_working_insertion']['team_player_minutes']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
