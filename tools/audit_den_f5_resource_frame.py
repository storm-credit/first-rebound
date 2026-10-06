"""Finite resource-frame review only; no legal/canon promotion and no old file writes."""
from pathlib import Path
from copy import deepcopy
from itertools import product
import argparse
import hashlib
import json
import build_den_theta_transition_domain as domain

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '903895165f671274387b2ca9685fd959361f01b5'
OUT = ROOT / 'research/DEN_F5_RESOURCE_FRAME_REVIEW_2026_10_07.json'
MD = ROOT / 'reviews/DEN_F5_RESOURCE_FRAME_REVIEW_2026_10_07.md'
SOURCES = (
    'tools/build_den_theta_transition_domain.py',
    'research/DEN_THETA_TRANSITION_DOMAIN_2026_10_07.json',
    'research/DEN_NAMED_CONDITIONAL_RIGHTS_WITNESS_2026_10_06.json',
    'research/NBA_2021_L_ASSET_CHAIN_SOURCES.json',
    'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json',
    'research/DEN_T1_T3_DATED_MATCHING_WITNESS_2026_10_06.json',
    'tools/audit_den_f5_resource_frame.py',
    'design/WORLD_BIBLE_COMPLETION_ROADMAP.md',
)


def norm(p):
    return p.read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def sha(p):
    return hashlib.sha256(norm(p).encode()).hexdigest()


def resource_lemma():
    # Universal finite abstraction, NOT the actual complete NBA debt ledger.
    # Each right has three feasible original states: absent, unused, assigned.
    rights = ['DEN2023_2R', 'DEN2025_2R', 'DEN2026_2R', 'DEN2027_2R']
    cases = []
    for states in product((0, 1, 2), repeat=4):
        supply = {r for r, s in zip(rights, states) if s != 0}
        demand = {r for r, s in zip(rights, states) if s == 2}
        additional = {'DEN2023_2R', 'DEN2027_2R'}
        alternate_supply = supply | additional
        cases.append({'id': len(cases) + 1, 'original_supply': sorted(supply),
                      'unchanged_demand': sorted(demand), 'alternate_supply': sorted(alternate_supply),
                      'same_allocation_feasible': demand <= alternate_supply})
    first_cases = []
    for bits in product((0, 1), repeat=5):
        outgoing = [y for y, b in zip(range(2023, 2028), bits) if b]
        no_adjacent = all(b - a > 1 for a, b in zip(outgoing, outgoing[1:]))
        first_cases.append({'outgoing_first_years': outgoing,
                            'named_first_no_adjacent': no_adjacent,
                            'adding_only_seconds_changes_first_predicate': False})
    return {'classification': 'ABSTRACT_RESOURCE_INCLUSION_THEOREM_NOT_ACTUAL_LEDGER',
            'formula': 'D subset S and S subset S_alt implies D subset S_alt, for unchanged allocations D',
            'cases': cases, 'first_predicate_cases': first_cases,
            'actual_existing_demands_or_contract_read_footprint_recovered': False,
            'not_a_proof_that_contract_outputs_are_unchanged': True}


def build():
    prior = json.loads(norm(ROOT / SOURCES[1]))
    # Full upstream reconstruction, not a new hash over a possibly forged packet.
    domain.validate(prior)
    approval = json.loads(norm(ROOT / SOURCES[4]))
    if 'do not execute' not in approval['selected']['F5_MCGEE']:
        raise ValueError('F5 omission direction changed')
    graph = prior['joint_graph_transform']
    historical = {e['id']: e for e in graph['original_public_edges']}
    candidate = {e['id']: e for e in graph['alternate_candidate_public_edges']}
    deleted = sorted(set(historical) - set(candidate))
    expected_deleted = ['F5_DEN2023_SECOND', 'F5_DEN2027_SECOND', 'F5_HARTENSTEIN', 'F5_MCGEE']
    if deleted != expected_deleted:
        raise ValueError('unexpected graph deletion')
    if graph['historical_contract_objects'] != graph['alternate_candidate_contract_objects']:
        raise ValueError('opaque contract bodies changed')
    delta = []
    for key, year in [('F5_DEN2023_SECOND', 2023), ('F5_DEN2027_SECOND', 2027)]:
        e = historical[key]
        if (e['from'], e['to']) != ('DEN', 'CLE'):
            raise ValueError('F5 asset origin/target changed')
        delta.append({'edge': key, 'dated_right_reference': f'DEN{year}_2R',
                      'historical_conditional_claim_holder': 'CLE',
                      'historical_outgoing_claim_exists': True, 'candidate_F5_outgoing_claim_exists': False,
                      'candidate_F5_claim_holder': None,
                      'historical_underlying_future_pick_owner': None,
                      'candidate_underlying_future_pick_owner': None,
                      'reported_protection': 'top-46 protected' if year == 2023 else None,
                      'reported_protection_author_selected': False,
                      'retained_other_claim_objects_preserved_in_candidate': True,
                      'free_unencumbered_title_certified': False})
    named = json.loads(norm(ROOT / SOURCES[2]))
    archive = next(x for x in named['source_recoveries'] if x['id'] == 'BI_DEN_ARCHIVE')
    archived_raw = Path(archive['cache_path']).read_bytes()
    if hashlib.sha256(archived_raw).hexdigest() != archive['raw_sha256'] or b'top-46 protected' not in archived_raw:
        raise ValueError('existing reported F5 protection source mismatch')
    rule = prior['primary_rule']
    raw = Path(rule['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != rule['raw_sha256']:
        raise ValueError('NBA primary rule raw changed')
    def probe(outgoing_claim_exists):
        return 2025 if outgoing_claim_exists else 2026
    historical_probe = probe(True)
    candidate_probe = probe(False)
    return {
        'schema_version': 1, 'date_local': '2026-10-07', 'baseline_main': BASELINE,
        'status': 'PUBLIC_RESOURCE_MONOTONICITY_REPRODUCED_ACTUAL_CONTRACT_FRAME_UNRESOLVED',
        'source_hash_convention': 'SHA256_UTF8_NO_BOM_CRLF_CR_TO_LF',
        'source_sha256': {f: sha(ROOT / f) for f in SOURCES},
        'upstream_full_source_reconstruction_passed': True,
        'independent_review_completed': True,
        'independent_review_scope': 'Limited source/type/resource review only; not whole asset legality or G16',
        'independent_review_evidence': {
            'source_hashes_checked': 8, 'resource_cases_recomputed': 81,
            'first_projection_cases_recomputed': 32, 'independent_mutations_rejected': 7,
            'corrections': ['conditional claim holder is not unconditional underlying pick owner',
                            'upstream full reconstruction and own-tool SHA are required'],
            'root_raw_SHA_and_top46_report_body_checked': True,
            'whole_asset_or_final_design_review_complete': False,
        },
        'roadmap_report': {'source': SOURCES[-1], 'unfinished_major_groups': 6,
                           'freeze': 'v0.30 PARTIAL', 'design_and_manuscript_gate': 'CLOSED',
                           'manuscript_count': 0,
                           'rows': [line for line in norm(ROOT / SOURCES[-1]).splitlines()
                                    if any(line.startswith(f'| {n} |') for n in range(1, 8))][:7]},
        'primary_rule_audit': {'path': rule['path'], 'raw_sha256': rule['raw_sha256'],
                               'bytes': len(raw), 'new_collection': False,
                               'scope': '4.02 actual completed original theta_star anchor; 7.03 first-round predicate'},
        'approved_delta': {'deleted_edges': deleted, 'direct_outgoing_claim_changes': delta,
                           'direct_first_round_owner_changes': [],
                           'prior_reported_conversion_resources': ['DEN2025_2R', 'DEN2026_2R'],
                           'named_public_resource_collision': False,
                           'player_changes': ['McGee remains CLE', 'Hartenstein remains DEN'],
                           'matching_recomputed': False},
        'existing_reported_F5_claim_source': {**archive, 'new_collection': False,
                                               'fresh_raw_SHA_check': True,
                                               'supports': '2023 F5 second is top-46 protected; future underlying owner not unconditional CLE',
                                               'not_full_contract_or_author_selection': True},
        'resource_inclusion_lemma': resource_lemma(),
        'dependency_edges': [
            {'from': 'F5_DEN2023_SECOND', 'to': 'F5_DEN2023_conditional_claim.presence', 'kind': 'SOURCE_GRAPH_DIRECT_WRITE', 'changed': True},
            {'from': 'F5_DEN2027_SECOND', 'to': 'F5_DEN2027_claim.presence', 'kind': 'SOURCE_GRAPH_DIRECT_WRITE', 'changed': True},
            {'from': 'F5_DEN2023_conditional_claim.presence', 'to': 'theta.P/theta.G/theta.context read ports',
             'kind': 'OPAQUE_READ_POSSIBILITY_NOT_ACTUAL_CLAUSE', 'actual_dependency': None},
            {'from': 'F5_DEN2027_claim.presence', 'to': 'theta.P/theta.G/theta.context read ports',
             'kind': 'OPAQUE_READ_POSSIBILITY_NOT_ACTUAL_CLAUSE', 'actual_dependency': None},
            {'from': 'unchanged first supply', 'to': 'named first-round retention predicate',
             'kind': 'PRESERVED_INPUT', 'changed': False},
            {'from': 'unchanged DEN2025_2R/DEN2026_2R', 'to': 'reported prior conversion resource capacity',
             'kind': 'PRESERVED_PUBLIC_DATED_RESOURCE', 'changed': False},
        ],
        'same_AST_different_state_probe': {
            'classification': 'ABSTRACT_FUNCTION_PROBE_NOT_SOURCE_CONTRACT_OR_LEGAL_COUNTEREXAMPLE',
            'read_port': 'F5_DEN2023_conditional_claim_presence',
            'same_function': 'return 2025 if read_port else 2026',
            'historical_read_value': True, 'candidate_read_value': False,
            'historical_output': historical_probe, 'candidate_output': candidate_probe,
            'earlier_prior_first_for_spacing_probe': 2023,
            'both_named_pairs_no_adjacent': all(y - 2023 >= 2 for y in [historical_probe, candidate_probe]),
            'conclusion': 'Copying a function/opaque AST alone does not imply equal outputs on changed inputs',
            'reported_contract_compatibility_claimed': False,
            'actual_theta_star_illegal_or_changed_claimed': False,
            'new_terms_selected': False,
        },
        'available_closure': {
            'direct_public_resource_deletion_frame': 'REPRODUCTION_PASS',
            'unchanged_allocation_resource_inclusion': 'MATHEMATICAL_PASS_WITH_EXPLICIT_UNCHANGED_DEMAND_PREMISE',
            'first_supply_predicate_noninterference': 'PASS_IN_DECLARED_FIRST_SUPPLY_PROJECTION',
            'actual_complete_theta_star_output_frame_or_constraint_monotonicity': 'HOLD',
            'actual_illegal_counterexample_found': False,
            'original_theta_star_exists_from_completed_source': True,
            'every_report_compatible_theta_legality_assumed': False,
            'whole_three_required_asset_branches_PASS': False,
        },
        'one_remaining_relation': {
            'id': 'ACTUAL_THETA_STAR_F5_DELETION_FRAME_OR_LEGAL_MONOTONICITY',
            'statement': 'Deleting the F5 outgoing conditional claim objects does not invalidate the complete retained historical P/G related-right obligations; exact underlying owner and future outcomes remain unselected',
            'adequate_alternative_witnesses': [
                'source-supported read/write footprint frame covering the two deleted outgoing claim objects and the retained rights',
                'source-supported invariant establishing lawful retained obligations under extra second-round supply, even if outputs differ',
            ],
            'numeric_terms_original_private_receipt_or_all_hidden_clause_absence_not_mandatory': True,
            'what_is_not_yet_proved': 'The pure resource lemma applies to actual theta_star constraints, rather than only unchanged demands',
            'exact_terms_selected': None, 'future_rank_selected': None,
            'new_required_branch_or_policy': False,
        },
        'authority': {'new_asset_PASS': 0, 'new_financial_or_pick_selection': False,
                      'actual_alternate_acceptance': None, 'central_edits': 0,
                      'manuscript_allowed': False, 'full_medical_or_season_certification': False},
        'tool_execution': {'Antigravity': 'NOT_RUN', 'NotebookLM': 'NOT_RUN', 'Claude': 'NOT_RUN'},
    }


def validate(data):
    if data != build():
        raise ValueError('source, theorem domain, graph or authority differs from reconstruction')
    cases = data['resource_inclusion_lemma']['cases']
    if len(cases) != 81 or any(not x['same_allocation_feasible'] for x in cases):
        raise ValueError('resource inclusion theorem failed')
    first = data['resource_inclusion_lemma']['first_predicate_cases']
    if len(first) != 32 or any(x['adding_only_seconds_changes_first_predicate'] for x in first):
        raise ValueError('first supply frame failed')


def render(d):
    return """# DEN F5 거래 생략 — 자원 증가와 조건 조회 범위 검문

2026-10-07 / [재현 입력](../research/DEN_F5_RESOURCE_FRAME_REVIEW_2026_10_07.json) / [검문 도구](../tools/audit_den_f5_resource_frame.py)

**새 자산 PASS 0. 원고 CLOSED. 실제 원 θ*의 불법 반례는 발견하지 않았다.** 기존 433 파일·중앙 문서는 변경하지 않았다.

## 정확한 변경 연결

승인된 F5 생략은 McGee의 CLE 잔류와 Hartenstein의 DEN 잔류를 보존한다. 공개 지명권 그래프에서 삭제되는 두 연결은 DEN2023/2027 2R에 연결된 F5 청구권/부담의 DEN→CLE 양도다. 기존 BI 보관본문의 보고는2023권리를top46보호로 명시한다. 따라서 역사상 CLE는 조건부 청구권 holder이지 모든 보호결과에서 underlying pick의 무조건 소유자가 아니다. 이 보고는 실제 계약 전부나 새 작가 선택이 아니다. 이 두 양도를 생략하면 해당 F5 지출을 만들지 않는다. 다른 기존 청구권까지 없는 자유 소유권을 인증하는 뜻은 아니다.

이 변경의 직접 write footprint는 두 F5 outgoing claim의 존재/holder/부담이다. 실제 underlying futurepick owner는 양쪽 모두null로 유지하며 보호결과는 선택하지 않는다. 1R 공급은 바뀌지 않고, 기존 보고의 prior 전환 자원 DEN2025/2026 2R도 이 두 연결과 직접 겹치지 않는다. 기존 θ.P/G AST·전이·우선권 참조는 복사돼 있다. 그러나 opaque 참조의 실제 read footprint는 아직 전개되지 않았다. 두 conditional-claim-presence→P/G/context 읽기 연결은 확인된 조항이 아닌 미해결 함수 입력 가능성으로 기록했다.

## 이번에 실제로 닫은 작은 정리

D⊆S와 S⊆S_alt이면 같은 배정 D는 S_alt에서도 가능하다. 네 named-second 자원의 원 공급/미사용/배정 상태 3^4=81개를 모두 검산했다. 추상 자원집합에 DEN2023/2027 기호를 추가해도 기존의 **변하지 않는 배정**은 자원 부족이나 중복 배정을 새로 만들지 않는다. 이것은 실제 전체 장부나 조건부 공급의 확정이 아닌 추상 집합의 유한 자원 포함 정리다. 실제 F5 생략은 outgoing claim 제거이며 underlying pick의 무조건 추가 소유를 인증하지 않는다.

또한 2023~27의 1R 지출 여부 2^5=32개에서 second만 추가하면 같은 first 보유 판정이 바뀌지 않음을 검문했다. 전체 Stepien/모든 우선권 인증으로 확대하지 않는다. 원 θ*의 조건이 바뀐 claim-presence를 읽어 다른 청구를 활성화하는지까지 이 자원 정리가 자동 증명하지는 않는다.

## AST 동일성만으로 결과 동일성을 주장할 수 없는 이유

같은 함수 f(b)가 b=true이면2025, false이면2026을 반환하는 순수 함수 probe를 실행한다. historical/candidate의 F5 conditional-claim-presence로 b가 달라지면 동일 AST도 출력이 다르다. prior2023에 대해 양쪽 named-first 간격은 모두 적법한 간격이므로 이 probe는 **결과 동일성의 논리 공백**을 드러낸다. 실제 계약 조항·공개 보고와 호환하는 계약 후보·actual θ*의 불법 반례·새 선택으로 취급하지 않는다.

따라서 정확한 미래 전달 결과 동일성이 법적 종료의 필수 목표도 아니다. 결과가 달라도 동일 원 θ* 의무를 계속 합법적으로 이행할 수 있다는 불변량이 있으면 법적 단조성 경로로 충분할 수 있다. 모든 임의 보도호환 θ가 합법이라고 전제하지 않는다.

## 남은 일반관계 하나

원 θ*의 완전한 retained P/G 관련 의무가 F5의 두 outgoing conditional claim 제거로 무효나 충돌을 일으키지 않는 관계를 검문해야 한다. 두 changed claim-presence의 실제 read/write frame 또는 추가 second 공급하의 source-supported 법적 불변량 중 하나면 충분하다. 정확 보호·전환 숫자, 비공개 영수증, 모든 미공개 조항 부재의 인증을 새 필수 출처로 요구하지 않는다.

기존 NBA2019 §4.02의 공식 완료 앵커는 그 실제 원 θ*에 적용한다. 조건 고지는 Association Office Trade Call 대상이며 대중 보도자료의 전체 공개를 뜻하지 않는다. §7.03의 1R 보유 조건은 second-only 직접 변경으로 악화하지 않는다. 이 두 근거만으로 모든 다른 조건의 read footprint까지 결정되지는 않는다.

현재 증거로 작은 자원 정리와 first 공급 projection은 재현 완료다. 실제 retained-contract frame/제약 단조성은 HOLD이며 법적 세 행 승격은 하지 않았다. 원자료·기존 계산 재수집이나 동일 48경로 재계산은 하지 않았다. 도구 Antigravity/NotebookLM/Claude는 NOT_RUN이다.

업스트림 prior는 `domain.validate`로 원자료부터 완전히 재구성해 검문하며 같은 삭제ID라도 조건AST가 조작됐으면 거절한다. 자체 검문 도구SHA도 기록한다.

## 현행 7행 진행표

[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md) / 미완료 큰묶음6 / v0.30 PARTIAL / 설계·원고 CLOSED / 원고0.

독립 원자료·타입·자원 검문을 실제 회수했다: SHA8 일치, 81자원/32first 투영 재산, 독립 변조7 거절. 조건부 holder/underlying owner 혼동과 상위 AST 변조 허점을 수리했고 root도 raw SHA와 top46 보고 본문을 직접 대조했다. 이 한정 검문 완료는 전체 자산 법적 PASS나 G16 전체 통과가 아니다.

| 번호 | 큰묶음 | 최신 상태 |
|---|---|---|
""" + '\n'.join(d['roadmap_report']['rows']) + """

`python -B -X utf8 tools/audit_den_f5_resource_frame.py --check --self-test`
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true')
    p.add_argument('--self-test', action='store_true')
    args = p.parse_args()
    d = build()
    validate(d)
    body = json.dumps(d, ensure_ascii=False, indent=2) + '\n'
    md = render(d)
    if args.check:
        if norm(OUT) != body or norm(MD) != md:
            raise ValueError('saved review stale')
    else:
        OUT.write_text(body, encoding='utf-8', newline='\n')
        MD.write_text(md, encoding='utf-8', newline='\n')
    n = 0
    if args.self_test:
        for label in ['resource_loss', 'fake_monotonicity', 'drop_changed_owner', 'AST_equals_outputs', 'fake_PASS', 'stale_source']:
            changed = deepcopy(d)
            if label == 'resource_loss': changed['resource_inclusion_lemma']['cases'][0]['alternate_supply'] = []
            elif label == 'fake_monotonicity': changed['available_closure']['actual_complete_theta_star_output_frame_or_constraint_monotonicity'] = 'PASS'
            elif label == 'drop_changed_owner': changed['approved_delta']['direct_outgoing_claim_changes'].pop()
            elif label == 'AST_equals_outputs': changed['same_AST_different_state_probe']['candidate_output'] = 2025
            elif label == 'fake_PASS': changed['authority']['new_asset_PASS'] = 3
            else: changed['source_sha256'][SOURCES[0]] = '0' * 64
            try: validate(changed)
            except ValueError: n += 1
            else: raise AssertionError('false witness accepted: ' + label)
        changed_prior = json.loads(norm(ROOT / SOURCES[1]))
        for side in ('historical_contract_objects', 'alternate_candidate_contract_objects'):
            changed_prior['joint_graph_transform'][side]['theta.G']['transition_body'] = 'forged_same_AST_in_both_sides'
        original_norm = norm
        def changed_prior_read(path):
            if path == ROOT / SOURCES[1]:
                return json.dumps(changed_prior)
            return original_norm(path)
        globals()['norm'] = changed_prior_read
        try:
            try: build()
            except ValueError: n += 1
            else: raise AssertionError('same IDs/counts forged upstream AST accepted')
        finally:
            globals()['norm'] = original_norm
        changed = deepcopy(d)
        changed['source_sha256']['tools/audit_den_f5_resource_frame.py'] = '0' * 64
        try: validate(changed)
        except ValueError: n += 1
        else: raise AssertionError('forged own-tool SHA accepted')
    print(json.dumps({'status': d['status'], 'resource_cases': 81, 'first_supply_cases': 32, 'negative_tests': n, 'new_asset_PASS': 0}))


if __name__ == '__main__':
    main()
