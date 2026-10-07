"""Inventory finite CP2 functional coverage without treating allocation as episodes."""

import argparse
import copy
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from unittest.mock import patch

import build_cp2_design_packets as cp2_validator


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/CP2_FINITE_FUNCTION_COVERAGE_2026_10_07.json')
MARKDOWN = Path('design/CP2_FINITE_FUNCTION_COVERAGE_2026_10_07.md')
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
CANDIDATES = (
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'design/A02_PREP_CONDITIONAL_FUNCTIONS.json',
    'design/A03_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'design/A04_DRAFT_CONDITIONAL_FUNCTIONS.json',
    'design/A05_EARLY_NBA_CONDITIONAL_FUNCTIONS.json',
    'design/A06_2020_21_CONDITIONAL_FUNCTIONS.json',
    'design/A07_2021_22_CONDITIONAL_FUNCTIONS.json',
    'design/A08_2022_23_CONDITIONAL_FUNCTIONS.json',
    'design/A09_2023_24_CONDITIONAL_FUNCTIONS.json',
    'design/A10_2024_25_CONDITIONAL_FUNCTIONS.json',
    'design/A11_2025_26_CONDITIONAL_FUNCTIONS.json',
    'design/A12_2026_27_CONDITIONAL_FUNCTIONS.json',
    'design/A13_2027_28_CONDITIONAL_FUNCTIONS.json',
    'design/A14_2028_35_CONDITIONAL_FUNCTIONS.json',
)
FIRST_SIX = {
    'A01-S1': {
        'last_function_id': 'A01-EF-002',
        'cp2_exit': '참여와 회피가 분리됨',
        'last_exit_anchor': '같은 학년 라이벌에게 기술·판단·위치선정으로 완패했다',
        'support': '자기 선택으로 체험에 들어갔고 완패를 겪었다. 이후 재참여는 S2에서 따로 보인다.',
        'limit': '처음 훈련만으로 계속 참여하거나 회피를 완전히 끝냈다고 인증하지 않는다.',
    },
    'A01-S2': {
        'last_function_id': 'A01-EF-006',
        'cp2_exit': '재능 밖 의무를 처음 인식',
        'last_exit_anchor': '게임 한 판을 더 시작하지 않고 이번 한 번 맡은 공 준비에 참여했다',
        'support': '한 번의 맡은 준비를 게임 추가판보다 우선한 직접 행동이 있다.',
        'limit': '반복 습관·수면·학교생활 전체 통제나 팀 전체 신뢰는 관측되지 않았다.',
    },
    'A01-S3': {
        'last_function_id': 'A01-EF-009',
        'cp2_exit': '외부 환경 선택의 주체가 됨',
        'last_exit_anchor': '프렙 이동 방향의 준비를 계속하겠다고 직접 밝혔다',
        'support': '기존 프렙 이동 방향을 미답 질문을 보존한 채 본인이 계속한다고 밝혔다.',
        'limit': '이 기능 자체가 실제 입학·비자·입국을 실행한 것은 아니다. 별도 가상 전환 경로와 연결해야 한다.',
    },
    'A02-S1': {
        'last_function_id': 'A02-EF-003',
        'cp2_exit': '소속 자격을 책임짐',
        'last_exit_anchor': '다음 허용 하루에는 스스로 일어나 의무 스터디홀과 허용 기본 훈련을 먼저 맞춘',
        'support': '잃은 도움 시간은 되돌리지 않고 다음 한 허용 하루의 학업·훈련 우선순위를 실제 실행했다.',
        'limit': '하루 수행은 최종 학업 자격이나 반복된 생활 습관의 인증이 아니다.',
    },
    'A02-S2': {
        'last_function_id': 'A02-EF-006',
        'cp2_exit': '새 역할의 반복 과제',
        'last_exit_anchor': '코너 패스가 시작될 때 복귀를 시도했지만',
        'support': '코너 복귀 지연 원인을 좁히고 별도 허용 훈련에서 같은 판단의 반복 과제를 시작했다.',
        'limit': '제때 복귀·실전 성공·기술 숙련은 아직 확인되지 않았다.',
    },
    'A02-S3': {
        'last_function_id': 'A02-EF-010',
        'cp2_exit': 'Villanova 입학/역할 경로 연결',
        'last_exit_anchor': '2017년 봄 늦은 Villanova 체육장학금 오퍼와 입학 승인을 전달받고',
        'support': '봄 영입·입학, 5–6월 학교 졸업·성적표와 후순위 역할 준비가 연결됐다.',
        'limit': '여름 NCAA/대학 compliance는 A02 회차 밖 기관 연결이다. 대학 등록·첫 출전·정확 counter를 인증하지 않는다.',
    },
}


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    cp2 = load(root, CP2)
    assert cp2['total_planned_units'] == 780
    assert len(cp2['acts']) == 14 and len(cp2['subacts']) == 42
    assert cp2['planned_episode_outlines_completed'] == 0
    assert cp2['manuscript_allowed'] is False and cp2['author_locked'] is False
    assert cp2['final_episode_functions_completed'] == 19, 'wait for parent registry19'
    final_paths = cp2['final_episode_function_paths']
    assert len(final_paths) == len(set(final_paths)) == 19
    currentness_errors, current_records = cp2_validator.validate_final_functions(cp2, root=root)
    assert not currentness_errors, 'registered final function source/currentness failed: ' + '; '.join(currentness_errors)
    assert len(current_records) == 19
    subacts = {s['id']: s for s in cp2['subacts']}
    assert len(subacts) == 42
    assert set(FIRST_SIX).issubset(subacts)
    candidate_map = defaultdict(list)
    candidate_paths = {}
    for path in CANDIDATES:
        for item in load(root, path)['functions']:
            assert item['id'] not in candidate_paths, item['id']
            assert item['subact'] in subacts, item['id']
            assert item['status'] in ('CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE',
                                      'CONDITIONAL_EPISODE_FUNCTION_CANDIDATE'), item['id']
            assert item.get('selected_event', False) is False, item['id']
            assert item.get('author_locked', False) is False, item['id']
            candidate_paths[item['id']] = path
            candidate_map[item['subact']].append(item['id'])
    assert len(candidate_paths) == 85
    assert all(candidate_map[sid] for sid in subacts)
    final_map = defaultdict(list)
    final_ids = set()
    for index, path in enumerate(final_paths):
        item = load(root, path)
        assert item == current_records[index], 'registered function differs from producer-validated source: ' + path
        fid = item['episode_function_id']
        sid = item.get('primary_subact', item.get('subact'))
        assert fid not in final_ids and sid in subacts, fid
        assert item['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE', fid
        if 'local_blueprint' in item:
            assert item['local_blueprint']['status'] == 'ACTUAL_VERIFIED', fid
        else:
            assert fid in {'A01-EF-001', 'A01-EF-002', 'A01-EF-003'}, fid
            assert item['source_semantic_projection_sha256'], fid
        assert item['whole_g13_complete'] is False and item['manuscript_allowed'] is False, fid
        final_ids.add(fid)
        final_map[sid].append((item['final_function_order'], fid, path, item['exit_state']))
    assert set(final_map) == set(FIRST_SIX)
    assert sorted(n for items in final_map.values() for n, _, _, _ in items) == list(range(1, 20))
    for sid, pinned in FIRST_SIX.items():
        assert subacts[sid]['exit_state'] == pinned['cp2_exit'], sid
        last = max(final_map[sid])
        assert last[1] == pinned['last_function_id'], sid
        assert pinned['last_exit_anchor'] in last[3], sid
    source_paths = ('tools/build_cp2_finite_function_coverage.py', CP2, *CANDIDATES, *final_paths)
    hashes = {p: sha((root / p).read_bytes()) for p in source_paths}
    rows = []
    for subact in cp2['subacts']:
        sid = subact['id']
        selected = sorted(final_map.get(sid, []))
        pinned = FIRST_SIX.get(sid)
        rows.append({
            'subact_id': sid, 'parent_act': subact['parent_act'],
            'cp2_entry_state': subact['entry_state'],
            'cp2_exit_state': subact['exit_state'],
            'cp2_choice': subact['choice'], 'cp2_cost': subact['cost'],
            'candidate_ids': candidate_map[sid],
            'candidate_source_paths': sorted(set(candidate_paths[i] for i in candidate_map[sid])),
            'registered_function_ids': [fid for _, fid, _, _ in selected],
            'registered_function_paths': [path for _, _, path, _ in selected],
            'last_registered_exact_exit': selected[-1][3] if selected else None,
            'coverage_state': ('LOCAL_FUNCTION_ROUTE_PRESENT_WHOLE_EXIT_UNAUDITED' if selected
                               else 'CONDITIONAL_FUNCTIONS_ONLY_NO_FINAL_ROUTE'),
            'observed_support_for_cp2_exit': pinned['support'] if pinned else None,
            'unproven_or_conditional_boundary': pinned['limit'] if pinned else '채택된 국소 기능·정확 진입/출구·비용·정보 접근·역사 원장 검문이 아직 없다.',
            'whole_subact_exit_audited': False,
            'actual_published_episode_allocation_selected': False,
            'source_history_audit_status': subact['history_audit_status'],
            'research_dependencies': subact['research_dependencies'],
            'scenario_references': subact['scenario_references'],
            'historical_events_touched': subact['historical_events_touched'],
            'next_action': ('AUDIT_EXACT_WHOLE_EXIT_WITH_NO_NEW_EPISODE_ASSUMED' if selected
                            else 'PROJECT_EXISTING_CANDIDATES_INTO_A_FINITE_SELECTED_FUNCTION_ROUTE'),
        })
    acts = []
    for index, act in enumerate(cp2['acts']):
        aid = act['id']
        children = [r for r in rows if r['parent_act'] == aid]
        assert len(children) == 3
        next_act = cp2['acts'][index + 1] if index + 1 < len(cp2['acts']) else None
        next_first = next((s for s in cp2['subacts'] if next_act and s['id'] == next_act['id'] + '-S1'), None)
        acts.append({
            'act_id': aid, 'subact_ids': [r['subact_id'] for r in children],
            'cp2_exit_state': act['exit_state'],
            'next_act_id': next_act['id'] if next_act else None,
            'next_act_first_subact_entry': next_first['entry_state'] if next_first else None,
            'registered_function_count': sum(len(r['registered_function_ids']) for r in children),
            'candidate_unit_count': sum(len(r['candidate_ids']) for r in children),
            'whole_act_exit_and_handoff_audited': False,
            'published_episode_count_finalized': False,
        })
    counts = Counter(r['coverage_state'] for r in rows)
    assert counts == {'LOCAL_FUNCTION_ROUTE_PRESENT_WHOLE_EXIT_UNAUDITED': 6,
                      'CONDITIONAL_FUNCTIONS_ONLY_NO_FINAL_ROUTE': 36}
    return {
        'schema': 'CP2_FINITE_FUNCTION_COVERAGE_REGISTER_V1',
        'status': 'DERIVED_WORKING_AUDIT_NOT_G13_COMPLETION',
        'scope': '14_ACT_42_SUBACT_85_CANDIDATE_19_REGISTERED_FUNCTIONS',
        'counts': {
            'acts_total': 14, 'subacts_total': 42, 'candidate_causal_units_total': 85,
            'registered_local_functions_total': 19,
            'subacts_with_registered_local_function_route': 6,
            'subacts_with_only_conditional_units': 36,
            'whole_subact_exits_audited': 0, 'whole_act_exits_audited': 0,
            'planned_allocation_slots': 780,
            'planned_slots_are_mandatory_new_events': False,
            'final_published_episode_count': None,
            'future_episode_function_rows_required_count': None,
        },
        'closure_criterion': [
            'For each of 42 subacts, choose or combine existing causal units into a source-current function route and audit exact entry, observable choice, direct cost, bounded exit, information access and next handoff.',
            'For each of 14 acts, compare its three audited subact exits to the Act exit and adjacent Act entry, historical ledger and five promise paths; do not force provisional outcomes into author locks.',
            'After actual published episode allocation is selected, validate the function or explicit span of every chosen episode, its information access, continuity and source revision. The number is currently unselected.',
            'G13 whole PASS also requires selected historical/long-term outcomes and the canonical ledger to align; this register alone never certifies G13, G14 or manuscript.',
        ],
        'subact_rows': rows, 'act_handoffs': acts,
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'author_locked': False,
        'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }


def render(data):
    c = data['counts']
    lines = [
        '# CP2 유한 기능 포괄 원장', '',
        '**상태:** `DERIVED_WORKING_AUDIT_NOT_G13_COMPLETION`. 14막·42소막의 기능 근거와 미감사 범위를 추적한다. 780은 계획 분량 슬롯이며 새 사건 780개나 고정 공개 회차 수가 아니다.', '',
        f"- 조건부 인과 단위 {c['candidate_causal_units_total']}개, 중앙 등록 국소 기능 {c['registered_local_functions_total']}개.",
        f"- 국소 기능 경로가 있는 소막 {c['subacts_with_registered_local_function_route']}/42. 이 여섯 소막의 전체 종료 감사 {c['whole_subact_exits_audited']}/6.",
        f"- 조건부 자료만 있고 최종 기능 경로가 없는 소막 {c['subacts_with_only_conditional_units']}/42. 14막 전체 종료 감사 {c['whole_act_exits_audited']}/14.",
        '- 실제 공개 회차 수와 그 기능표의 남은 행수는 아직 산출할 수 없다. 42행 감사만으로 G13 전체 PASS가 되지 않는다.', '',
        '## 앞 여섯 소막의 실제 지점', '',
        '| 소막 | 국소 기능 | CP2 출구 | 현재 관측 근거 | 남은 좁은 경계 |',
        '| --- | --- | --- | --- | --- |',
    ]
    for row in data['subact_rows'][:6]:
        lines.append(f"| {row['subact_id']} | {', '.join(row['registered_function_ids'])} | {row['cp2_exit_state']} | {row['observed_support_for_cp2_exit']} | {row['unproven_or_conditional_boundary']} |")
    lines.extend(['', '## 남은 36소막의 기존 입력', '',
                  '| 막 | 소막 3개 | 조건부 단위 | 현행 최종 기능 |',
                  '| --- | --- | ---: | ---: |'])
    for act in data['act_handoffs'][2:]:
        lines.append(f"| {act['act_id']} | {', '.join(act['subact_ids'])} | {act['candidate_unit_count']} | {act['registered_function_count']} |")
    lines.extend(['', '## 닫는 순서', ''])
    for step in data['closure_criterion']:
        lines.append(f'- {step}')
    lines.extend(['', '- 다음 실제 배치: 앞 여섯 소막의 종료·인접막 인계 감사(새 회차0을 전제로 시작), 이어 나머지 36소막에 기존 63후보의 핵심 행동·비용을 중복 없이 투영한다.',
                  '- 기능표 범위만 추적한다. 전체 G13/G14, 실제 Pack, 원고는 미완료이고 설계/원고 게이트는 `CLOSED`다.', ''])
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['register differs from 42-row source-bound audit']


def self_test(data):
    mutations = [
        ('force 780 events', lambda d: d['counts'].update(planned_slots_are_mandatory_new_events=True)),
        ('invent episode count', lambda d: d['counts'].update(final_published_episode_count=780)),
        ('invent G13 PASS', lambda d: d.update(whole_g13_complete=True)),
        ('false first-six exit audit', lambda d: d['subact_rows'][0].update(whole_subact_exit_audited=True)),
        ('delete a candidate', lambda d: d['subact_rows'][6]['candidate_ids'].pop()),
        ('duplicate a function path', lambda d: d['subact_rows'][0]['registered_function_paths'].append(d['subact_rows'][0]['registered_function_paths'][0])),
        ('invent an act handoff audit', lambda d: d['act_handoffs'][0].update(whole_act_exit_and_handoff_audited=True)),
        ('claim actual pack', lambda d: d.update(actual_context_packs=1)),
        ('open manuscript', lambda d: d.update(manuscript_allowed=True)),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_load = load

    def changed_cp2_exit(root, path):
        source = original_load(root, path)
        if path == CP2:
            source = copy.deepcopy(source)
            next(s for s in source['subacts'] if s['id'] == 'A01-S1')['exit_state'] = '처음부터 훈련을 거부한다'
        return source
    with patch(__name__ + '.load', side_effect=changed_cp2_exit):
        assert validate(data), 'same-ID CP2 exit reversal'

    def changed_candidate_status(root, path):
        source = original_load(root, path)
        if path == CANDIDATES[0]:
            source = copy.deepcopy(source)
            source['functions'][0]['status'] = 'AUTHOR_LOCKED_FINAL_EPISODE'
        return source
    with patch(__name__ + '.load', side_effect=changed_candidate_status):
        assert validate(data), 'conditional source promoted to final'

    first_leaf = 'design/A01_E2_FINAL_EPISODE_FUNCTION.json'

    def changed_last_exit(root, path):
        source = original_load(root, path)
        if path == first_leaf:
            source = copy.deepcopy(source)
            source['exit_state'] = '체험에 들어가지 않고 승리했다'
        return source
    with patch(__name__ + '.load', side_effect=changed_last_exit):
        assert validate(data), 'same-ID first-six last exit reversal'

    for name, path, mutate in [
        ('first leaf full exit reversal', 'design/A01_E1_FINAL_EPISODE_FUNCTION.json',
         lambda source: source.update(exit_state='체험을 이미 성공했고 외부 환경에 입학했다')),
        ('second leaf entry reversal', 'design/A01_E2_FINAL_EPISODE_FUNCTION.json',
         lambda source: source.update(entry_state='감독 제안을 듣기 전에 해외 학교에 입학했다')),
        ('first leaf source revision falsified', 'design/A01_E1_FINAL_EPISODE_FUNCTION.json',
         lambda source: source['source_rev_sha256'].update({next(iter(source['source_rev_sha256'])): '0' * 64})),
    ]:
        def changed_registered_leaf(root, requested_path):
            source = original_load(root, requested_path)
            if requested_path == path:
                source = copy.deepcopy(source)
                mutate(source)
            return source
        with patch(__name__ + '.load', side_effect=changed_registered_leaf):
            assert validate(data), name
    return len(mutations) + 6


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MARKDOWN).write_text(render(data), encoding='utf-8')
    errors = validate(data)
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors.extend(validate(saved))
        if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'counts': data['counts'], 'negative_controls': tested,
                      'current': not errors, 'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
