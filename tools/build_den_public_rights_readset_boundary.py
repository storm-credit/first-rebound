"""Audit the positive published DEN rights read-set, without whole-row promotion.

This compiles four existing cap-analyst rows and one NBA rule. It does not
make unspecified contract predicates members of the domain, select exact
terms, or revive the rejected complete-economic-relation projection proof.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import fitz
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_den_public_rights_readset_boundary.py'
OUT = 'research/DEN_PUBLIC_RIGHTS_READSET_BOUNDARY_2026_10_07.json'
MD = OUT[:-5] + '.md'
BASELINE = 'ae7678e224e842a7598cc733e49bd14e81be80d2'
PINS = {
    'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2',
    'canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json': 'e0d8ed1f82c494a3610a91c779eef5573737f9b818088c903786cb12afae7dc9',
    'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json': 'c0166bba7a0874aa08dfa88e7d00c0f0d0e237ca2090459ddd6167cf1353c5ea',
    'research/DEN_COMPLETE_RIGHTS_EXISTENCE_SCOPE_AUDIT_2026_10_07.json': '23d8fcbd15cf9e23f954358cd8343ec949b0daf7d9df5865f76700317329fcd1',
    'simulation/CAUSALITY_MODEL.md': '00638830864e9503db4589464806cc0c4c0d94002b039a8bf661d96e6f6a7c45',
}
BI = Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-denver-cost-2026-10-06/BI_DEN_archive.html')
BI_SHA = 'd6a41cd3209a62c428578ea14c7acc1fe7338df4c206bf871b8e4de41b5af942'
BYLAWS = Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-2019-bylaws.pdf')
BYLAWS_SHA = '6accb3d9633e15e8559d13228c27ae7b3b0b81eac0894050b06256eea6da3464'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def normalized(path):
    return path.read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def read_bytes(path):
    return path.read_bytes()


def read_json(path):
    return json.loads(normalized(ROOT / path))


def collect():
    b = read_bytes(BI)
    assert digest(b) == BI_SHA, 'original analyst raw body changed'
    soup = BeautifulSoup(b, 'html.parser')
    lis = [(i, li.get_text(' ', strip=True)) for i, li in enumerate(soup.find_all('li'))]
    rules = {
        'P': ('2023', 'first-rounder', 'Oklahoma City Thunder'),
        'G': ('2025', 'first-rounder', 'Orlando Magic'),
        'F5_2023': ('2023', 'second-rounder', 'Cleveland Cavaliers'),
        'F5_2027': ('2027', 'second-rounder', 'Cleveland Cavaliers'),
    }
    rows = {}
    for key, tokens in rules.items():
        found = [(i, s) for i, s in lis if s.startswith(tokens[0]) and all(t in s for t in tokens[1:])]
        assert len(found) == 1, 'published future-pick row not unique: ' + key
        i, text = found[0]
        rows[key] = {'html_li_zero_based': i, 'text_sha256': digest(text.encode()), 'authority': 'ORIGINAL_CAP_ANALYST_REPORTED_INPUT_NOT_EXACT_CONTRACT'}
        if key == 'P':
            assert 'lottery protected through 2025' in text and '2025 and 2026 second-rounders' in text
        if key == 'G':
            assert 'two years after the obligation' in text and 'top-5 protected through 2027' in text and 'does not convey' in text
        if key == 'F5_2023':
            assert 'top-46 protected' in text
    raw = read_bytes(BYLAWS)
    assert digest(raw) == BYLAWS_SHA, 'NBA by-laws raw body changed'
    doc = fitz.open(stream=raw, filetype='pdf')
    text = doc[86].get_text().replace('\r\n', '\n').replace('\r', '\n')
    assert '7.03. First Round Draft Choice.' in text
    assert 'two (2)' in text and 'consecutive future NBA Drafts' in text
    return rows, digest(text.encode())


def first_projection_cases():
    """Only the named P/G pair; no assumption that other first-round claims vanish."""
    cases = []
    for p in [2023, 2024, 2025]:
        for g in list(range(p + 2, 2028)) + [None]:
            cases.append({'P_branch': 'FIRST_CONVEYS', 'P_first_year': p, 'G_first_year': g,
                          'named_firsts_not_adjacent': g is None or g - p >= 2,
                          'G_start_relation': 'P_FIRST_DELIVERY_YEAR_PLUS_TWO_OR_LATER_ROLLOVER'})
    # The wording of P's "obligation" after conversion is not numerically fixed.
    # This over-envelope tests every published G year and no-conveyance, without
    # asserting that every envelope member is an actual contracted live branch.
    for g in [2025, 2026, 2027, None]:
        cases.append({'P_branch': 'CONVERTS_TO_SECONDS', 'P_first_year': None, 'G_first_year': g,
                      'named_firsts_not_adjacent': True,
                      'G_start_relation': 'BROAD_REPORTED_YEAR_ENVELOPE_NOT_POSITIVE_CONVERTED_LINK'})
    return cases


def build():
    for p, want in PINS.items():
        assert digest(normalized(ROOT / p).encode()) == want, 'reviewed source changed: ' + p
    s2 = read_json('canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json')
    assert s2['status'] == 'AUTHOR_SELECTED_S2_STANDARD_ONLY'
    prior = read_json('research/DEN_COMPLETE_RIGHTS_EXISTENCE_SCOPE_AUDIT_2026_10_07.json')
    assert prior['status'] == 'CONDITIONAL_RELATION_LEMMA_VALID_WHOLE_BRANCH_PROMOTION_REJECTED'
    assert prior['authority']['whole_branch_source_verified'] is False
    assert prior['authority']['new_asset_PASS'] == 0
    rows, page_sha = collect()
    cases = first_projection_cases()
    assert all(c['named_firsts_not_adjacent'] for c in cases)
    return {
        'schema': 'DEN_POSITIVE_PUBLIC_RIGHTS_READSET_BOUNDARY_V1',
        'status': 'PUBLIC_RULE_COMPONENTS_AUDITED_COMPLETE_RELATION_BRIDGE_HOLD',
        'baseline_main': BASELINE,
        'source_sha256': {**PINS, SELF: digest(normalized(ROOT / SELF).encode())},
        'source_hash_convention': 'REPOSITORY_UTF8_NO_BOM_CRLF_CR_TO_LF;CACHE_RAW_BYTES',
        'source_records': {
            'BI': {'url': 'https://web.archive.org/web/20210422002709id_/https://www.basketballinsiders.com/denver-nuggets-team-salary/',
                   'cache_path': str(BI), 'raw_sha256': BI_SHA, 'capture': '2021-04-22', 'body_updated': '2021-04-20',
                   'scope': 'Four positive published future-pick list rows; not all private terms or a pre-trade snapshot', 'rows': rows},
            'NBA_BYLAWS': {'url': 'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf',
                           'cache_path': str(BYLAWS), 'raw_sha256': BYLAWS_SHA, 'pdf_page': 87, 'printed_page': 78,
                           'section': '7.03', 'page_text_sha256': page_sha,
                           'scope': 'First-round two-consecutive-future-drafts constraint; not whole-contract deletion monotonicity'},
        },
        'positive_reported_rule_components': {
            'P': {'promisor': 'DEN', 'recipient': 'OKC', 'first_years': [2023, 2024, 2025],
                  'protection_predicate': 'LOTTERY_PROTECTED', 'first_protection_terminal_year': 2025,
                  'conversion_seconds': [2025, 2026], 'reported_reads': ['P.first_pick_protection_result', 'P.year', 'P.conversion_event']},
            'G': {'promisor': 'DEN', 'recipient': 'ORL', 'published_first_year_label': 2025,
                  'start_relation': 'TWO_YEARS_AFTER_OKC_OBLIGATION', 'protection_predicate': 'TOP_FIVE_PROTECTED',
                  'first_terminal_year': 2027, 'terminal_reported_outcome': 'DOES_NOT_CONVEY',
                  'reported_reads': ['P.obligation_event', 'G.year', 'G.first_pick_protection_result'],
                  'meaning_of_P_obligation_after_conversion': None,
                  'actual_conversion_to_G_start_selected': None},
            'F5_2023': {'claim_round': 2, 'year': 2023, 'reported_protection': 'TOP_46', 'omitted_by_approved_F5': True},
            'F5_2027': {'claim_round': 2, 'year': 2027, 'reported_protection': None,
                        'null_does_not_certify_unprotected_exact_contract': True, 'omitted_by_approved_F5': True},
        },
        'dependency_findings': {
            'classification': 'REPORTED_RULE_COMPONENT_MODEL_NOT_FULL_CONTRACT_READSET_CERTIFICATE',
            'positive_G_reference_names_P_obligation': True,
            'F5_deletion_changes_named_second_claims_only': True,
            'P_conversion_years_disjoint_from_deleted_F5_years': sorted(set([2025, 2026]) & set([2023, 2027])) == [],
            'G_reported_terminal_is_no_conveyance_not_new_second_compensation': True,
            'absence_of_F5_tokens_proves_no_private_dependency': False,
            'all_hidden_predicates_added_to_domain': False,
            'full_actual_contract_read_set_certified': False,
            'all_other_original_burdens_assumed_zero': False,
        },
        'named_first_pair_projection': {
            'cases': cases, 'case_count': len(cases),
            'all_named_pair_cases_avoid_adjacent_outgoing_firsts': True,
            'conversion_envelope_is_actual_complete_live_contract_domain': False,
            'other_first_pick_rights_or_encumbrances_assumed_absent': False,
            'whole_team_Stepien_certificate': False,
            'scope': 'Named pair component only. Unchanged other first-rights burdens remain original opaque state, not zero.',
        },
        'f5_incremental_projection': {
            'within_declared_reported_components_first_round_projection_changed': False,
            'within_declared_reported_components_conversion_resource_years_changed': False,
            'all_exact_future_outputs_identical_required': False,
            'whole_relation_deletion_monotonicity_proved': False,
            'old_48_or_81_state_probes_repeated': False,
        },
        'remaining_minimum_gap': {
            'id': 'SOURCE_SUPPORTED_P_RESOLUTION_TO_G_APPLICABILITY_BRIDGE',
            'statement': 'Positive published relation and dated unchanged-right bridge must cover the candidate legal-existence family; do not assume complete feasible relation survives F5 deletion.',
            'exact_converted_future_year_required': False,
            'all_private_clauses_absence_required': False,
            'actual_receipt_consent_or_acceptance_required_for_this_legal_existence_scope': False,
            'next_finite_work': 'Independently assess the four positive reported components plus dated preserved P/G bridge as source coverage; a converted-link source can refine it, but private-original-only requirements are forbidden.',
        },
        'prior_conditional_relation_lemma_repromoted': False,
        'whole_branch_source_verified': False, 'whole_branch_complete_domain': False,
        'whole_legal_pass': False, 'new_asset_PASS': 0,
        'actual_theta': None, 'actual_future_delivery': None, 'actual_acceptance': None,
        'new_exact_asset_or_financial_selection': False, 'register_promotion': False,
        'independent_review_completed': False, 'fresh_primary_documents_collected': 0,
        'tools': {'Antigravity': 'NOT_RUN', 'NotebookLM': 'NOT_RUN', 'Claude': 'NOT_RUN'},
        'manuscript_allowed': False, 'design_gate': 'CLOSED',
    }


def validate(data):
    try:
        expected = build()
    except (AssertionError, KeyError, OSError, ValueError) as exc:
        return ['source construction: ' + str(exc)]
    return [] if data == expected else ['public rule boundary differs from original-source reconstruction']


def render(d):
    return '\n'.join([
        '# DEN 공개 권리 규칙의 긍정적 참조 범위', '',
        '**상태:** `PUBLIC_RULE_COMPONENTS_AUDITED_COMPLETE_RELATION_BRIDGE_HOLD`. 전체 법적 PASS0, 기존 조건부 정리의 전체 승격 기각 유지.', '',
        '## 실제로 읽은 범위', '',
        '[기존 원 cap analyst 단면](https://web.archive.org/web/20210422002709id_/https://www.basketballinsiders.com/denver-nuggets-team-salary/)의 future-pick 네 행을 직접 대조했다. 업데이트4/20·수집단면4/22이며 새 원문 회수는 아니다. [원문 지문·구조 입력](DEN_PUBLIC_RIGHTS_READSET_BOUNDARY_2026_10_07.json)에 rawSHA, li 위치, 행텍스트SHA를 보존한다. 보고 모델이며 원계약 전문으로 승격하지 않는다.', '',
        '- P: 2023–25 보호되는 1R, 종료 뒤 2025·26의 2R 전환.',
        '- G: OKC 의무 뒤 두 해라는 연결, 2027까지 보호, 이후 전달 없음.',
        '- F5: 2023 조건부2R와 2027 2R. 승인된 거래 생략은 이 두 청구를 발생시키지 않는다. 두번째의 미공표 보호를 무조건 없음으로 고르지 않는다.', '',
        '## 닫힌 국소 검문', '',
        '[NBA 규약](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf) PDF87/인쇄78 §7.03과 대조했다. P 전달 뒤 G의 두 해 이상 간격 및 P 미전달 시 G 단일1R라는 named-pair 투영은 연속 두 해의 두 named 1R 방출을 만들지 않는다. 다른 1R 권리·부담은 0으로 놓지 않으며 팀 전체 Stepien 인증은 아니다.',
        f"- 공개 보고 범위의 투영 {d['named_first_pair_projection']['case_count']}개. 전환 뒤 G 개시의 정확 계약 의미는 미선택이며 넓은 보고연도 envelope를 실제 전분기 계약으로 인증하지 않는다.",
        '- P의 보고 전환2R 연도25/26과 삭제된 F5 연도23/27은 직접 겹치지 않는다. G의 보고 말단은 전달 없음이다. 이 긍정적 규칙 범위에서 첫픽 투영과 전환연도는 F5 삭제로 변하지 않는다.', '',
        '## 남은 한정 경계', '',
        '실제 모든 계약 참조 입력이 위 목록뿐이라는 부재증명이나 전체 경제관계 삭제 단조성은 증명하지 않았다. 기존 Dret≤C 보조정리를 다시 전체 PASS로 올리지 않는다. 남은 공백은 P 해결 사건→G 적용과 유한 보존 사건의 공개 근거가 후보 법적존재 가족을 덮는지에 대한 source-scope 판단이다.',
        '정확 미래출력의 동일성, 모든 숨은 조항의 무존재, 비공개 원장·접수·실동의는 새 필수요건으로 추가하지 않는다. 실제 미래 연도·보호·승낙은null이고 다음 검문도 공개 규칙/그 연결의 적용범위에 한정한다.', '',
        '재현: `python tools/build_den_public_rights_readset_boundary.py --check --self-test`. 중앙/REGISTER·정본선택0·원고CLOSED. 외부 CLI 미실행, 독립 검문 대기.', '',
    ])


def self_test(data):
    mutations = [
        ('rejected_lemma_to_PASS', lambda z: z.update(whole_legal_pass=True)),
        ('private_absence_requirement', lambda z: z['remaining_minimum_gap'].update(all_private_clauses_absence_required=True)),
        ('converted_link_chosen', lambda z: z['positive_reported_rule_components']['G'].update(actual_conversion_to_G_start_selected=2027)),
        ('pair_to_whole_Stepien', lambda z: z['named_first_pair_projection'].update(whole_team_Stepien_certificate=True)),
        ('other_burdens_zero', lambda z: z['dependency_findings'].update(all_other_original_burdens_assumed_zero=True)),
        ('future_equivalence_required', lambda z: z['f5_incremental_projection'].update(all_exact_future_outputs_identical_required=True)),
    ]
    for name, mutate in mutations:
        z = copy.deepcopy(data); mutate(z)
        assert validate(z), name
    actual_reader = read_bytes
    def altered(path):
        b = actual_reader(path)
        return b + b' changed' if path == BI else b
    with patch(__name__ + '.read_bytes', side_effect=altered):
        assert validate(data), 'raw source mutation'
    return len(mutations) + 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    d = build()
    if args.write:
        (ROOT / OUT).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MD).write_text(render(d), encoding='utf-8')
    errors = validate(d)
    if args.check:
        saved = read_json(OUT); errors += validate(saved)
        if normalized(ROOT / MD) != render(saved): errors.append('Markdown stale')
    tests = self_test(d) if args.self_test else 0
    print(json.dumps({'current': not errors, 'errors': errors,
                      'named_projection_cases': d['named_first_pair_projection']['case_count'],
                      'negative_controls': tests, 'new_asset_PASS': 0}, ensure_ascii=False))
    if errors: raise SystemExit(1)


if __name__ == '__main__':
    main()
