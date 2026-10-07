"""Join selected fictional transactions, all dated rosters and accepted S2 law.

No new trade, salary, draw or result is chosen. This leaf proposes a finite
A2/K_TRANSACTIONS execution certificate; only the root may promote the register.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

import build_2020_21_approved_transaction_execution_bridge as transaction
import build_2020_21_dated_roster_execution_bridge as roster
import build_2020_21_result_and_pick_execution_bridge as settlement
from check_chicago_d1_s2 import evaluate

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_2020_21_transaction_execution_closure_witness.py'
OUT = 'simulation/NBA_2020_21_TRANSACTION_EXECUTION_CLOSURE_WITNESS.json'
MD = OUT[:-5] + '.md'
REGISTER = 'control/CHICAGO_2020_21_D1_S2_REGISTER.json'
PROTOCOL = 'control/CHICAGO_2020_21_D1_S2_PROTOCOL.md'
BASELINE_MAIN = '446df4a13abc3c78e65b5459d698d2e455aef0b5'
# Previously directly reviewed 12 legal proofs. Mutable A/K flags are excluded.
# Replacing the proof objects and refreshing source SHA cannot invent approval.
REVIEWED_LEGAL_PROJECTION = '93fe86ffc52657f2282ba0d39474ea0a608e8f22c58a2affe63e2a169024a6f2'
REVIEWED_LEGAL_EVIDENCE_FILES = '997d5a2ff8f21e2222dfad93020b772b4e5cbfecb0b1c065bdb7bc640108bd48'
SOURCES = [SELF, transaction.SELF, transaction.OUT, roster.SELF, roster.OUT,
           'tools/build_2020_21_result_and_pick_execution_bridge.py', settlement.OUT,
           PROTOCOL, 'AGENTS.md', roster.AUTH, roster.DIRECTION, roster.F45, roster.C2,
           'simulation/GSW_G1_OPTION3_NY_WORKING_EXECUTION.json',
           'research/CHA_WAS_FINITE_ROSTER_WORKING_FAMILY_2026_10_07.json',
           'design/WORLD_BIBLE_COMPLETION_ROADMAP.md', roster.REG, roster.L2, roster.POST]


def text(p):
    return (ROOT / p).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def load(p): return json.loads(text(p))
def sha(p): return hashlib.sha256(text(p).encode()).hexdigest()
def object_sha(d): return hashlib.sha256(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def legal_evidence_paths(value):
    paths = []
    if isinstance(value, dict):
        for key, v in value.items():
            paths += v if key == 'evidence' else legal_evidence_paths(v)
    elif isinstance(value, list):
        for v in value: paths += legal_evidence_paths(v)
    return paths


def join_events(t, r):
    """Match original dated feed execution, not merely matching final counts."""
    indexed = r['dated_events']
    states = r['roster_states']
    result = []
    for e in t['events']:
        links = []
        for move in e['movements']:
            candidates = [x for x in indexed if x['date'] == e['date'] and
                          x['type'] == 'Trade' and x['team'] == move['to'] and
                          roster.norm(x['player']) == roster.norm(move['player'])]
            assert len(candidates) == 1, 'Approved move must have one dated arrival'
            x = candidates[0]
            assert not x['omitted_by_approved_direction'], 'Approved arrival was omitted'
            assert x['working_previous_team'] == move['from'], 'Approved source team changed'
            members = states[x['after_state_ids'][move['to']]]['players']
            assert any(roster.norm(n['player']) == roster.norm(move['player']) for n in members)
            links.append({'movement': copy.deepcopy(move), 'dated_event_id': x['id'],
                          'before_state_ids': x['before_state_ids'], 'after_state_ids': x['after_state_ids']})
        omitted_names = {
            'T2_VUCEVIC_NO_TRADE': [('2021-03-25', n) for n in ['Nikola Vucevic', 'Al-Farouq Aminu', 'Wendell Carter Jr.', 'Otto Porter Jr.']],
            'T4_POWELL_HOOD_RETAIN': [('2021-03-25', n) for n in ['Norman Powell', 'Gary Trent Jr.', 'Rodney Hood']],
            'F5_MCGEE_NO_TRADE': [('2021-03-25', n) for n in ['JaVale McGee', 'Isaiah Hartenstein']],
            'C2_VAREJAO_NO_RETURN': [('2021-05-04', 'Anderson Varejao'), ('2021-05-14', 'Anderson Varejao')],
            'F4_HALL_NO_RESIGN': [('2021-05-09', 'Donta Hall')],
        }.get(e['id'], [])
        omissions = []
        for day, player in omitted_names:
            matched = [x for x in indexed if x['date'] == day and roster.norm(x['player']) == roster.norm(player)]
            assert len(matched) == 1 and matched[0]['omitted_by_approved_direction'], 'Omitted event restored or lost'
            x = matched[0]
            assert x['before_state_ids'] == x['after_state_ids'], 'Omitted trade changes state'
            omissions.append({'player': player, 'date': day, 'dated_event_id': x['id'], 'state_change': False})
        for player, holder in e['retained'].items():
            # Retention is a working deadline-state fact, not a promise that
            # the player never signs/waives later. Approved named carriers
            # such as Trent have their own preserved alternate opening.
            snapshots = [b for b in r['team_game_bindings'] if b['team'] == holder and b['date'] >= e['date']]
            assert snapshots, 'Retained holder has no model date'
            first = min(snapshots, key=lambda b: (b['date'], b['event_id']))
            assert any(roster.norm(n['player']) == roster.norm(player) for n in states[first['state_id']]['players']), 'Approved retained actor missing at first selected game'
        assert set(e['legal_family_ids']) <= {p['id'] for p in load(REGISTER)['legal_proofs']}
        result.append({'id': e['id'], 'date': e['date'], 'kind': e['kind'],
                       'legal_family_ids': e['legal_family_ids'], 'movement_state_links': links,
                       'omitted_state_links': omissions, 'retained': e['retained'],
                       'actual_consent_or_receipt_certified': False})
    assert len(result) == 8
    assert sum(len(x['movement_state_links']) for x in result) == 10
    assert sum(len(x['omitted_state_links']) for x in result) == 12
    return result


def positive_player_index():
    """Read the exact minute vectors already fully reconstructed by roster.

    Season roster slots15+2 do not imply game-night active capacity15. Every
    positive player requires one active place, regardless of contract class.
    Zero-minute reserves are not medically classified or forced active here.
    """
    rows = {}
    def add(phase, event, day, team, seconds):
        key = (phase, event, day, team)
        assert key not in rows, 'Duplicate positive-player source'
        names = sorted(n for n, sec in seconds.items() if sec > 0)
        assert len(names) <= 15, 'Game-night active15 upper violated: ' + str(key)
        rows[key] = names
    for x in load(roster.REG)['team_games']:
        add('REGULAR', x['event_id'], x['date'], x['team'], x['player_seconds'])
    for g in load(roster.L2)['games']:
        for team, v in g['teams'].items(): add('PLAY_IN', g['event_id'], g['date'], team, v['player_seconds'])
    for g in load(roster.POST)['games']:
        for team, v in g['teams'].items(): add('PLAYOFF', f"{g['series']}_G{g['game']}", g['date_model'], team, v['planned_minutes'])
    assert len(rows) == 2348
    return rows


def join_games(r, s):
    required_active = positive_player_index()
    bindings = {}
    for b in r['team_game_bindings']:
        phase = 'PLAY_IN' if b['phase'] == 'PLAYIN' else b['phase']
        eid = b['event_id'].replace(':G', '_G') if phase == 'PLAYOFF' else b['event_id']
        key = (phase, eid, b['date'], b['team'])
        assert key not in bindings, 'Duplicate dated roster binding'
        assert not b['unresolved_gap_ids'] and b['positive_membership_covered']
        state = r['roster_states'][b['state_id']]
        assert state['team'] == b['team']
        assert state['standard_count'] <= 15 + b['working_named_hardship_capacity']
        assert state['two_way_count'] <= 2
        assert not state['actual_registration_certified']
        names = required_active[key]
        registered_names = {roster.norm(x['player']) for x in state['players']}
        assert all(roster.norm(n) in registered_names for n in names), 'Positive active player not registered'
        bindings[key] = b
    rows = []
    for g in s['games']:
        assert {g['winner'], g['loser']} == {g['home'], g['away']}
        joined = {}
        for team in [g['home'], g['away']]:
            key = (g['phase'], g['id'], g['date'], team)
            b = bindings.pop(key)
            joined[team] = {'state_id': b['state_id'], 'minute_source': b['minute_source'],
                            'positive_membership_covered': True,
                            'positive_required_active_players': required_active.pop(key),
                            'game_night_active_upper': 15,
                            'named_hardship_families': b['working_named_hardship_families']}
        rows.append({'id': g['id'], 'phase': g['phase'], 'date': g['date'],
                     'home': g['home'], 'away': g['away'], 'selected_winner': g['winner'],
                     'teams': joined})
    assert len(rows) == 1174 and not bindings and not required_active, 'Whole result-roster bijection incomplete'
    return rows


def build():
    reg = load(REGISTER)
    assert object_sha(reg['legal_proofs']) == REVIEWED_LEGAL_PROJECTION, 'Reviewed legal proof identity changed'
    evidence_shas = {p: sha(p) for p in sorted(set(legal_evidence_paths(reg['legal_proofs'])))}
    assert object_sha(evidence_shas) == REVIEWED_LEGAL_EVIDENCE_FILES, 'Previously reviewed legal evidence changed; independent legal prior must be refreshed'
    legal = evaluate(reg)
    assert len(legal['legal_fields']) == 12 and all(v == 'LEGAL_BOUND_PASS' for v in legal['legal_fields'].values())
    t = load(transaction.OUT)
    assert t == transaction.build(), 'Approved transaction source reconstruction changed'
    assert t['legal_projection_sha256'] == REVIEWED_LEGAL_PROJECTION
    r = load(roster.OUT)
    roster.validate(r)
    assert r['scope']['working_roster_execution_complete'] and not r['named_gaps']
    assert r['summary']['no_named_membership_or_slot_gap_team_games'] == 2348
    s = load(settlement.OUT)
    assert not settlement.validate(s), 'Result/pick source reconstruction changed'
    assert s['pre_promotion_result_input_coherence']['approved_F5_removed_player_positive_rows'] == []
    assert s['pre_promotion_result_input_coherence']['conflict_count'] == 0
    assert s['pick_control_snapshot']['scope'] == 'AS_OF_FROZEN_APPROVED_SEASON_ASSETS_BEFORE_OPTIONAL_OFFSEASON_MOVES'
    event_links = join_events(t, r)
    game_links = join_games(r, s)
    assert s['summary']['frozen_control_rows'] == 60 and s['summary']['unresolved_core_protection_settlements'] == 0
    return {
        'schema': 'S2_FINITE_TRANSACTION_EXECUTION_CLOSURE_WITNESS_V1',
        'status': 'FINITE_A2_K_TRANSACTION_EXECUTION_INDEPENDENTLY_REVIEWED',
        'baseline_main': BASELINE_MAIN,
        'source_hash_method': 'UTF8_BOM_STRIPPED_CRLF_CR_NORMALIZED_LF',
        'source_sha256': {p: sha(p) for p in SOURCES},
        'reviewed_legal_projection_sha256': REVIEWED_LEGAL_PROJECTION,
        'independent_review': {
            'accepted_by_root_2026_10_07': True,
            'chi_scope': 'Original S2,8events/10moves/12omissions,1174-to2348/control60 and legal12/83 prior identity directly read; four source join mutations rejected.',
            'root_and_den_active15_scope': 'Original NBA2020 rule and four full-vector donor/receiver corrections, independent Fraction BPM effects, unchanged2156 vectors and all1080 winners directly audited.',
            'full_G16_completed': False, 'new_legal_raw_audit_count': 0},
        'reused_legal_evidence_source_sha256': evidence_shas,
        'reused_legal_evidence_scope': '83 existing repository evidence files are frozen to the previously accepted legal prior. This join does not repeat all underlying original raw-source audits or claim new independent legal source collection.',
        'legal_fields': legal['legal_fields'],
        'authority': {'approved_directions': [roster.DIRECTION, roster.F45, roster.C2],
                      'routine_implementations': r['selected_finite_carriers'],
                      'new_author_lock': False, 'new_salary_or_bonus_cents_selected': None,
                      'actual_consent_or_trade_call_certified': False,
                      'actual_registration_or_medical_certified': False,
                      'conditional_2018_GSW_landing_author_locked': False},
        'selected_execution': {
            'approved_event_links': event_links, 'dated_result_roster_links': game_links,
            'full_roster_source': roster.OUT, 'state_count': len(r['roster_states']),
            'public_original_player_events': r['summary']['public_player_events'],
            'game_night_active_rule': {'url': 'https://www.nba.com/news/teams-allowed-to-carry-15-players-on-active-roster-for-2020-21-season',
                'NBA_publication_date': '2020-12-18', 'direct_web_body_read': True,
                'locator': 'Article paragraphs at web extraction176-180', 'raw_body_cache': None,
                'game_night_upper': 15, 'roster_standard_plus_TW_is_distinct': True,
                'zero_minute_active_choices_or_health_certified': False},
            'working_interval_ends_salary_erased': False,
            'lawful_financial_implementation': 'Reuse the previously accepted S2 public-family implementation existence. Exact q, salary/bonus/consent and receipt remain null; no new financial input is supplied.',
            'whole_private_financial_execution_certified': False,
            'F1_after_waiver_restriction': t['execution_design']['after_waiver_restriction'],
            'future_named_rights_family': s['descendant_rights'],
            'frozen_2021_control_snapshot': s['pick_control_snapshot'],
        },
        'resolved_previous_A2_named_connections': [
            {'previous': p, 'resolved_by': answer} for p, answer in zip(t['remaining_whole_A2_connections'], [
                'All2348 selected team-games, state membership/slots and dated source reconstruction',
                'Reviewed WAS44 finite tender family + preserved opening Trent, Bonga no NBA standard contract',
                'Reviewed Homesley May15/16 standard signing retained with no positive minutes',
                'Root-selected reviewed O3 routine conditional GSW28 operating family, exact landing lock unchanged',
                'A3 fixed origins/control60 before optional offseason moves'])],
        'summary': {'approved_events': 8, 'assignment_player_edges': 10,
                    'omitted_player_event_edges': 12, 'selected_games': 1174,
                    'selected_team_games': 2348, 'legal_fields_reused': 12,
                    'roster_named_gaps': 0, 'unjoined_result_or_roster_rows': 0,
                    'control_rows': 60, 'minutes_or_results_changed': 0},
        'closure_scope': {
            'finite_A2_execution_domain_complete': True,
            'finite_K_TRANSACTIONS_evidence_domain_complete': True,
            'repository_source_reconstruction_current': True,
            'independent_review_completed': True,
            'A2_promotion': False, 'K_TRANSACTIONS_promotion': False,
            'all_A_prerequisites_closed': False, 'closing_witness_written': False,
            'register_changed': False, 'season_selected': False,
            'manuscript_allowed': False,
            'private_receipts_or_all_hidden_terms_required_for_this_fictional_scope': False,
            'all_future_actual_pick_execution_certified': False},
        'separate_remaining_scope': [
            'Root A2 closing_witness certificate and register promotion',
            'A1 and all three A prerequisites before any K bundle can be closed',
            'Optional summer AP transactions/draftees are macro3; not new macro2 A2 prerequisites',
            'Actual consent, precise private financial terms, registration/medical receipts and future deliveries are not certified by this fictional execution witness'],
        'freeze': 'v0.30 PARTIAL', 'design_gate': 'CLOSED', 'manuscript_count': 0,
    }


def validate(d, expected=None):
    expected = build() if expected is None else expected
    if d != expected: raise ValueError('Transaction closure witness differs from current source reconstruction/authority')


def markdown(d):
    lines = ['# 2020–21 A2/거래 묶음 유한 실행 종료 증인', '',
        '[기계 입력](NBA_2020_21_TRANSACTION_EXECUTION_CLOSURE_WITNESS.json)은 기존 승인8사건·12법적 증인·1174경기/2348팀 명단·2021 control60을 연결한다. 거래·급여·추첨·승패를 새로 선택하거나 재계산하지 않았다.', '',
        '## 선택과 실행', '',
        '정확10선수 양도의 날짜/전소속/수취/전후 명단상태와 생략12선수사건의 상태 불변을 대조했다. T1–T4, Hall/McGee/C2를 복원하지 않는다. 전체 경기마다 양수분 소속·15+명명된hardship/2TW·승패의 양팀 명단을 1:1 연결했다.', '',
        '[NBA2020–21 규칙](https://www.nba.com/news/teams-allowed-to-carry-15-players-on-active-roster-for-2020-21-season)에 따라 경기별 양수 선수는 최대15명이다. standard15+TW2와 별도 검문이며 예비0의 active/의료는 미인증이다.', '',
        'GSW O3·CHA Terry TW/Riller 미서명·WAS Bonga 유한tender/Homesley/Bell은 독립검문된 routine 작업 가족을 소비한다. GSW2018 원착지 AUTHOR_LOCKED는false다. 영원한 Bonga독점이나 미래2021 계약을 추가하지 않는다.', '',
        '금융은 통과한 공개 가족의 합법적 구현 존재를 동일 사건에 연결한다. 기존 법적12행과83근거 파일의 검수 지문을 고정해 새지문만 붙인 변경을 거부하며 원raw독립감사를 다시 수행했다고 계수하지 않는다. 정확q/급여/bonus/실제수락·접수는null이며 면제 후 구계약 연장·재협상6개월 제한을 보존한다. 방출/만료가 부채삭제를 뜻하지 않는다. 전체30팀 private금융·실제 등록/의료를 인증하지 않는다.', '',
        '2021 픽은 승인된 시즌 자산의 optional 여름 이동 전 snapshot이다. 실제6/22 holder·60명 선수지명·미래2023–27 전달/수락을 복사하지 않는다.', '',
        '## 이전 A2 연결 빈칸 처리', '', '| 이전 입력 | 연결 증인 |', '|---|---|']
    for x in d['resolved_previous_A2_named_connections']:
        lines.append('| ' + x['previous'] + ' | ' + x['resolved_by'] + ' |')
    lines += ['', '## 판정 경계', '',
        'A2 실행 및 K_TRANSACTIONS 근거 도메인은 유한하게 연결됐고 root·chi의 한정 독립검문으로 수용됐다. chi의 원S2/전소속·생략·승자쌍·날짜 반증4와 root/den의 active15/4벡터·BPM 독립검문을 기록한다. 이 파일만으로 원장/closing_witness/K/시즌을 승격하지 않는다. K는 A1/A2/A3 전부를 먼저 닫아야 한다. 실제 비공개 접수증·모든 숨은조항 부재·모든 미래출력 동일성을 새 S2 필수조건으로 만들지 않는다.', '',
        '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 아래는 이 한정 검문이 수용된 시점의 진행표이며 후속 중앙 종료 판정을 대신하지 않는다.', '',
        '| 큰 묶음 | 검문 시점 |', '|---|---|',
        '| 1 2020드래프트 | 완료 |', '| 2 Chicago2020–21 | A2 새 실행증인 검문·통합 대기 |',
        '| 3 2021–23 | 승인방향 보존·후손 별도 |', '| 4 장기커리어 | 선행시즌 종료 대기 |',
        '| 5 결말·전체구조 | 골격 보존·기능표 계속 |', '| 6 집필규격·ContextPack | 기능배치 진행·실제Pack0 |',
        '| 7 통합·독립·작가승인 | 대기 |', '',
        '검문 시점 미완료 큰묶음6 · PROJECT_FREEZE v0.30 PARTIAL · 설계/원고 CLOSED · 원고0. 원장·중앙 변경0.', '']
    return '\n'.join(lines)


def self_test(d):
    changes = [
        ('wrong approved actor', lambda x: x['selected_execution']['approved_event_links'][0]['movement_state_links'][0]['movement'].update(to='CHI')),
        ('restore omitted state change', lambda x: x['selected_execution']['approved_event_links'][5]['omitted_state_links'][0].update(state_change=True)),
        ('drop one selected team', lambda x: x['selected_execution']['dated_result_roster_links'][0]['teams'].pop(next(iter(x['selected_execution']['dated_result_roster_links'][0]['teams'])))),
        ('wrong frozen holder', lambda x: x['selected_execution']['frozen_2021_control_snapshot']['rows'][6].update(control_holder='MIN')),
        ('actual consent from existence', lambda x: x['authority'].update(actual_consent_or_trade_call_certified=True)),
        ('automatic K promotion', lambda x: x['closure_scope'].update(K_TRANSACTIONS_promotion=True)),
    ]
    for label, mutate in changes:
        bad = copy.deepcopy(d); mutate(bad)
        try: validate(bad, d)
        except ValueError: continue
        raise AssertionError('False pass ' + label)
    from unittest.mock import patch
    original = load
    def wrong_legal(p):
        v = original(p)
        if p == REGISTER: v['legal_proofs'][0]['upper'] -= 1
        return v
    with patch(__name__ + '.load', side_effect=wrong_legal):
        try: build()
        except AssertionError: pass
        else: raise AssertionError('Fresh-hash changed legal proof falsely retains review')
    original_sha = sha
    def changed_legal_evidence(p):
        return '0' * 64 if p == 'research/CHI_F1_MATCHING_EXISTENCE_WITNESS_2026_10_07.json' else original_sha(p)
    with patch(__name__ + '.sha', side_effect=changed_legal_evidence):
        try: build()
        except AssertionError: pass
        else: raise AssertionError('Changed legal evidence falsely retains accepted prior')
    def over_active(p):
        v = original(p)
        if p == roster.REG:
            row = v['team_games'][0]
            row['player_seconds'] = {'Unsupported active ' + str(i): 1 for i in range(16)}
        return v
    with patch(__name__ + '.load', side_effect=over_active):
        try: positive_player_index()
        except AssertionError: pass
        else: raise AssertionError('16 positive players falsely satisfy game-night active15')
    return len(changes) + 3


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--write', action='store_true'); p.add_argument('--check', action='store_true'); p.add_argument('--self-test', action='store_true'); a = p.parse_args()
    d = build()
    if a.write:
        (ROOT / OUT).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MD).write_text(markdown(d), encoding='utf-8')
    if a.check:
        validate(load(OUT), d)
        assert text(MD) == markdown(d), 'Markdown stale'
    print(json.dumps({'current': a.check, 'summary': d['summary'], 'negative_controls': self_test(d) if a.self_test else 0, 'register_promotion': False}, ensure_ascii=False))
