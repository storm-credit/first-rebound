"""Source-bound three-team legal existence witness; no actual financial selection."""
from pathlib import Path
from copy import deepcopy
from decimal import Decimal as D
import argparse
import hashlib
import json
from bs4 import BeautifulSoup
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '43e359c'
OUT = ROOT / 'research/CHI_F1_MATCHING_EXISTENCE_WITNESS_2026_10_07.json'
MD = OUT.with_suffix('.md')
SELF = 'tools/build_chi_f1_matching_existence_witness.py'
SOURCES = [
    SELF,
    'canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json',
    'canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json',
    'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json',
    'simulation/CAUSALITY_MODEL.md',
    'simulation/2021_WASHINGTON_CHICAGO_PORTLAND_TRANSACTION_CASCADE.md',
    'research/CHI_CONSENSUAL_WAIVER_EXISTENCE_BOUNDARY_2026_10_07.json',
    'research/CHI_MINIMUM_ASSIGNMENT_BONUS_BOUNDARY_2026_10_06.json',
    'research/CHICAGO_PUBLIC_COMPONENT_BOUND_2026_10_06.json',
    'research/BOSTON_DATED_TPE_CAPACITY_WITNESS_2026_10_05.json',
    'research/DEN_T1_T3_DATED_MATCHING_WITNESS_2026_10_06.json',
    'research/NBA_2020_21_L_EXECUTION_TERMS_SOURCES.json',
    'research/CHICAGO_ANNUAL_EXCEPTION_SCOPE_2026_10_05.json',
]
TEMP = Path('C:/Users/Storm Credit/AppData/Local/Temp')
# These are the actually reviewed input versions, not hashes computed after a
# possibly altered upstream packet. A changed family needs a new source review.
REVIEWED_INPUT_SHA = {
    'canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json': 'e0d8ed1f82c494a3610a91c779eef5573737f9b818088c903786cb12afae7dc9',
    'canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json': 'ab996ffb9f9f6e4471ad473633af1529eb4928e3aa9a17b99642c591691c3798',
    'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json': 'c0166bba7a0874aa08dfa88e7d00c0f0d0e237ca2090459ddd6167cf1353c5ea',
    'simulation/CAUSALITY_MODEL.md': '00638830864e9503db4589464806cc0c4c0d94002b039a8bf661d96e6f6a7c45',
    'simulation/2021_WASHINGTON_CHICAGO_PORTLAND_TRANSACTION_CASCADE.md': '70c7b3b944cd745496e940a9336ac521513002fe2c170ad0782aeb626ed8fa37',
    'research/CHI_CONSENSUAL_WAIVER_EXISTENCE_BOUNDARY_2026_10_07.json': 'a5a5436faf05acbdb62f30248ff857e0f2e7d74f9ccfc9e6dd7058dece977791',
    'research/CHI_MINIMUM_ASSIGNMENT_BONUS_BOUNDARY_2026_10_06.json': 'ca191441eeccadb085f36248e92b1b1828f54c72cd2d433b00a41d34533b5ee2',
    'research/CHICAGO_PUBLIC_COMPONENT_BOUND_2026_10_06.json': '196cec339d3c3db24fd723c235b7a28efb0df37539adefc726b70bbc6716d7b3',
    'research/BOSTON_DATED_TPE_CAPACITY_WITNESS_2026_10_05.json': 'cf2776d3f9d9066ddebb54ac433771e74f924d3074d999c3ddf3754c8e8ef4aa',
    'research/DEN_T1_T3_DATED_MATCHING_WITNESS_2026_10_06.json': '4fe78e44c10e6a42e45dafda470b4a0c006b48e6b573dd8afbf8002c18020ee9',
    'research/NBA_2020_21_L_EXECUTION_TERMS_SOURCES.json': 'd0597187f18b3f1436c72ab50444156448a2b3e8c3477c1095579e298f60603b',
    'research/CHICAGO_ANNUAL_EXCEPTION_SCOPE_2026_10_05.json': 'c0997b4f9324650a27991426f906b845d15d32afdc41b114b0354475db9dd704',
}


def normalized(p):
    return p.read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def sha(p):
    return hashlib.sha256(normalized(p).encode()).hexdigest()


def load(f):
    return json.loads(normalized(ROOT / f))


def raw_record(path, expected, url, role):
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected:
        raise ValueError('raw source changed: ' + str(path))
    return dict(cache_path=str(path), raw_sha256=actual, bytes=len(raw), url=url, role=role)


def waiver(theis, green):
    t, g = D(str(theis)), D(str(green))
    if not (D(0) <= t <= D(750000) and D(0) <= g <= D('227697.15')):
        raise ValueError('outside external bonus model')
    q = max(D(0), t + g - D('175985.75'))
    qt = min(t, q)
    qg = q - qt
    assert D(0) <= qt <= t and D(0) <= qg <= g
    return qt, qg, D(6517981) + t + g - q


def build():
    if set(REVIEWED_INPUT_SHA) != set(SOURCES) - {SELF}:
        raise ValueError('reviewed source domain incomplete')
    for f,h in REVIEWED_INPUT_SHA.items():
        if sha(ROOT/f) != h:
            raise ValueError('reviewed upstream family changed: '+f)
    authority = load(SOURCES[1])
    if authority['selected']['route'] != 'S2_LEGAL_INTERVAL_PROOF_COUNTERFACTUAL_AUTHOR_MODEL':
        raise ValueError('authority changed')
    boundary = load(SOURCES[6])
    chi = load(SOURCES[8])
    bos = load(SOURCES[9])
    den = load(SOURCES[10])
    if boundary['formula']['domains'] != 'gammaTheis[0,750000],gammaGreen[0,227697.15]; eachwaiver[0,ownGamma]':
        raise ValueError('CHI external bonus family changed')
    if not chi['whole_cost_pass'] or not bos['closure']['branch_pass'] or not den['dated_matching_subbranch_pass']:
        raise ValueError('required prior supporting scope not passed')
    if D(str(chi['arithmetic']['upper_usd'])) != D('132367326.15'):
        raise ValueError('CHI current TeamSalary upper changed')
    cba = raw_record(TEMP / 'fr-2017-cba.pdf', '66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a',
                     boundary['source']['url'], 'PRIMARY_ORIGINAL_CBA')
    reader = PdfReader(cba['cache_path'])
    clauses = {}
    for n in [193, 233, 234, 235, 236, 248, 252, 398]:
        text = reader.pages[n - 1].extract_text()
        clauses[str(n)] = dict(pdf_page=n, printed_page=n-22,
                              extracted_text_sha256=hashlib.sha256(text.encode()).hexdigest())
    if 'all or any portion of a trade bonus' not in reader.pages[247].extract_text():
        raise ValueError('waiver clause missing')
    below = ' '.join(reader.pages[234].extract_text().split())
    if 'notwithstanding' not in below or 'Salary below the Salary Cap' not in below:
        raise ValueError('below-cap simultaneous path missing')
    guide = raw_record(TEMP / 'fr-2020-21-nba-officials-guide.pdf',
                       '60b6987a4adc6fa3b836c787b033e37299509c8af0d8afda770253e3dfa69d40',
                       load(SOURCES[12])['sources'][0]['url'] if 'sources' in load(SOURCES[12]) else
                       'https://697f6f9668a0bb24cd4b-78390edf330c094418f39edbaa9073b0.ssl.cf1.rackcdn.com/2021/02/2020-21-NBA-Officials-Guide-1-5-211.pdf',
                       'PRIMARY_NBA_SEASON_SPECIFIC_KEY_DATES')
    text = PdfReader(guide['cache_path']).pages[3].extract_text()
    if not all(x in text for x in ['Feb. 27', 'contracts guaranteed', 'March 25', 'May 16']):
        raise ValueError('season guarantee/deadline dates not present')
    guide.update(pdf_page=4, extracted_text_sha256=hashlib.sha256(text.encode()).hexdigest(),
                 facts={'standard_contract_guarantee_date':'2021-02-27', 'trade_deadline':'2021-03-25', 'regular_end':'2021-05-16'},
                 not_full_amendment_text=True)
    feed = raw_record(TEMP / 'fr-nba-player-movement-2026-10-04.json',
                      '3d9d7a6dd7ccd39ddfdd1799a26ef9901b44682d85a26f05239b468a8ae92e3a',
                      'https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json',
                      'PRIMARY_FROZEN_DATED_PUBLIC_EVENT_CATALOG')
    rows = json.loads(Path(feed['cache_path']).read_bytes())['NBA_Player_Movement']['rows']
    dates = {'daniel-gafford':'2019-07-08', 'luke-kornet':'2019-07-18',
             'daniel-theis':'2019-07-16', 'javonte-green':'2019-07-25', 'moritz-wagner':'2019-07-06'}
    timing = []
    for player, date in dates.items():
        found = [r for r in rows if r.get('PLAYER_SLUG') == player and r['TRANSACTION_DATE'][:10] == date]
        if len(found) != 1:
            raise ValueError('positive pre-existing contract event missing')
        recent = [r for r in rows if r.get('PLAYER_SLUG') == player and '2021-01-25' <= r['TRANSACTION_DATE'][:10] < '2021-03-25']
        if recent:
            raise ValueError('new recent event reopens aggregation/timing')
        timing.append(dict(player=player, positive_event=found[0], recent_public_rows=recent,
                           preservation='CAUSALITY unchanged contract/event family; not universal private absence'))
    gaf = raw_record(TEMP / 'fr-chi-f1-gafford-20261007.html',
                     'e03bfd35c6ab29f7f4e1152fdd60d84cb5d25ceacdd30a1bfe26206a61aee72d',
                     'https://www.salaryswish.com/players/daniel-gafford',
                     'CURRENT_VENDOR_HISTORICAL_CONTRACT_ROW_NOT_TRADE_DATE_LEDGER')
    table = [r.get_text(' | ', strip=True) for r in BeautifulSoup(Path(gaf['cache_path']).read_bytes(),'html.parser').select('tr')]
    expected_row = '2020-21 | $1,517,981 | $1,517,981 (+69%) | $1,517,981 | $0 | $0'
    if expected_row not in table:
        raise ValueError('Gafford current salary/performance model changed')
    gaf.update(locator='2019 four-year minimum contract table, 2020-21 row', current_salary_row=expected_row,
               future_rows=[r for r in table if r.startswith(('2021-22 | $1,782,621','2022-23 | Team | Yes (Oct 12, 2021)'))],
               no_guarantee_or_option_selection=True)
    hr_source = next(r for r in den['source_recoveries'] if 'hoops-rumors-glossary' in r.get('url',''))
    hr = raw_record(Path(hr_source['cache_path']),hr_source['raw_sha256'],hr_source['url'],hr_source['classification'])
    hr.update(locator=hr_source['locator'], not_full_amendment_text=True)
    bos_side = bos['sequence_existence_witness'][0]
    if bos_side['incoming_total_upper_usd'] != 4749420 or bos_side['conservative_matching_limit_usd'] != 8247476.25:
        raise ValueError('Boston reused full bound changed')
    salary = next(r for r in load(SOURCES[11])['salary_rows'] if r['player']=='Daniel Gafford')
    if [salary['base_usd'],salary['reported_likely_usd'],salary['reported_unlikely_usd']] != [1517981,0,0]:
        raise ValueError('preserved Gafford model conflict')
    ag_path='reviews/CHI_F1_ANTIGRAVITY_SOURCE_ATTEMPT_2026_10_07.json'
    ag=load(ag_path)
    if ag['source_certified'] is not False or ag['result']['elapsed_seconds'] != 53.001:
        raise ValueError('tool source-attempt record changed; review actual outcome')
    nlm_path='reviews/CHI_F1_NLM_EXISTENCE_ANALYSIS_2026_10_07.json'
    claude_path='reviews/CHI_F1_CLAUDE_EXISTENCE_BLIND_2026_10_07.json'
    nlm,claude=load(nlm_path),load(claude_path)
    if (nlm['analysis_success'] is not True or nlm['whole_gate_certified'] is not False or
        nlm['input_lf_sha256']!='c94f21a72c8f8cdad38c68d978973d797535b314f8471ac4ce3e62cea7c3aed3' or
        claude['result']['rebuttal_recovered'] is not True or claude['whole_gate_certified'] is not False):
        raise ValueError('tool recovered outcome/snapshot scope changed')
    return dict(
        schema_version=1, baseline_main=BASELINE, date_local='2026-10-07',
        status='ACCEPTED_LIMITED_THREE_TEAM_LEGAL_IMPLEMENTATION_EXISTENCE',
        classification={'fact':'CBA permissible amendments/matching and NBA season dates; public contract/event source records',
                        'inference':'For every admissible preserved external contract input there is a simultaneous three-team implementation with permissible consensual amendments',
                        'candidate':'Independently accepted legal-existence family; actual agreements and exact execution are separate',
                        'author_locked':'Prior F1 player directions only; no new financial choice'},
        source_hash_convention='SHA256_UTF8_NO_BOM_CRLF_CR_TO_LF',
        source_sha256={f:sha(ROOT/f) for f in SOURCES},
        reviewed_upstream_source_versions_pinned=True,
        raw_sources=dict(CBA=cba, NBA_2020_21_GUIDE=guide, NBA_FEED=feed, GAFFORD_CURRENT_VENDOR=gaf, CURRENT_MATCHING_HR=hr),
        CBA_clause_locations=clauses,
        scope_comparison=dict(original_author_rule=authority['selected']['legal_rule'],
            accepted_BOS_scope=bos['scope'], accepted_DEN_sequence_scope=den['sequence_scope'],
            interpretation='BRANCH_WITNESS: forall external source-supported contract parameters exists a legally permitted implementation; not forall discretionary implementation choices',
            scope_or_authority_changed=False, prior_unwaived_upper_retained=True,
            financial_selection_or_actual_consent_inferred=False),
        quantifiers=dict(external='Theis/Green complete Gamma intervals; Gafford all eligible total bonuses and all allocation/protection inputs; Kornet full Gamma bound; Wagner whole rookie envelope; all BOS/WAS cap/tax classes',
            controls='Only mathematical permissible amendment quantities and simultaneous route; no actual agreement assumed',
            statement='FOR_ALL external contract inputs EXISTS qT,qG,qGafford and simultaneous implementation satisfying every team matching constraint; IF the parties execute the permissible agreements',
            actual_all_waiver_choices_pass=False, actual_acceptance_certified=False),
        topology={'date':'2021-03-25','atomic':True,'edges':[
            {'from':'CHI','to':'WAS','player':'Daniel Gafford'}, {'from':'CHI','to':'BOS','player':'Luke Kornet'},
            {'from':'WAS','to':'BOS','player':'Moritz Wagner'}, {'from':'BOS','to':'CHI','player':'Daniel Theis'},
            {'from':'BOS','to':'CHI','player':'Javonte Green'}],
            'newly_acquired_contract_reaggregated':False,'minimum_exception_used':False,'combined_distinct_exceptions':False},
        CHI=dict(outgoing_lower_usd='3767981', rule='VII6(j)(1)(iii) full max/min; post-TeamSalary <= tax',
                 post_team_salary_upper_usd='132367326.15',tax_usd='132627000',tax_margin_usd='259673.85',
                 matching_limit_usd='6693966.75', incoming_base_usd='6517981',
                 external_gamma_intervals={'Theis':['0','750000'],'Green':['0','227697.15']},
                 algebra={'q':'max(0,gT+gG-175985.75)','qT':'min(gT,q)','qG':'q-qT',
                          'proof':'0<=qT<=gT, 0<=qG<=gG and gT+gG-q=min(gT+gG,175985.75)'},
                 incoming_after_candidate_waiver_upper_usd='6693966.75',max_permissible_candidate_q_sum_usd='801711.40',
                 all_incentives_in_preserved_model='Theis/Green reported likely/unlikely 0; full old-contract bonus intervals retained'),
        BOS=dict(outgoing_lower_usd='6517981',conservative_limit_usd='8247476.25',
                 incoming_full_upper_usd='4749420',margin_usd='3498056.25',
                 Kornet_base_fullGamma_upper_usd='2587500',Wagner_entire_rookie_upper_usd='2161920',
                 rule='125%+100000 safe for over-cap taxpayer/non-taxpayer and below-cap VII6(j)(3)',
                 candidate_waiver_reduces_BOS_outgoing_matching_salary=False,
                 reason='Outgoing uses pre-trade Salary; new assignment bonus and its waiver are post-assignment incoming effects',
                 Hayward_TPE_usage_usd=0, prior_four_cost_states=bos['cost_safety_link']['states_usd'],
                 maximum_prior_apron_usd='138716242',apron_usd='138928000',apron_margin_usd='211758'),
        WAS=dict(outgoing_Wagner_rookie_lower_usd='1441280',conservative_limit_usd='1901600',
                 incoming_Gafford_current_base_usd='1517981',performance_upper_in_preserved_model_usd='0',
                 external_Gafford_total_Gamma='Any bonus permitted by XXIV2(a), including all protected/allocation/remaining-year possibilities; actual value null',
                 candidate_qGafford='entire eligible total trade bonus',
                 post_assignment_current_bonus_after_candidate_waiver_usd='0',
                 proof='VII7(d)(3) permits entire waiver. VII3(b) allocation of zero total bonus is zero in every year regardless of protection weights.',
                 incoming_after_candidate_waiver_upper_usd='1517981',margin_usd='383619',
                 rule='125%+100000 is safe in all cap/tax classes, including below-cap VII6(j)(3); no new whole-WAS-cost certification',
                 original_future_bonus_and_protection_actual_values=None,
                 actual_assignment_bonus_zero_certified=False),
        date_and_rule_boundary=dict(contract_timing=timing,
            outgoing_base_protection='March25 after season-specific Feb27 standard-contract guarantee and before May16 regular end; VII6(j)(5)(ii) no unprotected current-base subtraction in this window',
            not_full_2020_amendment_certificate=True,
            applicability='Same original detailed rules plus NBA March16 current-season connection and March10 original cap-analyst current matching support as accepted BOS/DEN scope. NBA officials guide positively verifies the changed guarantee/deadline dates. No absence-of-change inferred from press silence.',
            after_waiver_restriction={'rule':'VII7(d)(3): old contract extension/renegotiation not before later of six months or otherwise eligible date',
                                     'trade_date':'2021-03-25','six_month_floor':'2021-09-25',
                                     'affected_candidate_contracts':['Theis','Green','Gafford'],
                                     'whole_2021_contract_execution_certified':False,
                                     'ordinary_new_FA_contract_is_not_automatically_old_contract_extension':True}),
        authority=dict(actual_gamma=None,actual_waiver_quantities=None,actual_player_consent=None,
            actual_assignor_agreement=None,actual_recipient_acceptance=None,actual_trade_call=None,
            new_financial_author_selection=None,actual_atomic_group_selection=None,
            source_supported_complete_legal_existence_family=True,
            independent_review_completed=True,register_promotion=0,whole_A2_K_or_season_pass=False,
            full_future_contract_execution_certified=False,manuscript_allowed=False),
        independent_review=dict(reviewer='/root/den_pick_full_branch',parent_acceptance='/root',
            verdict='ACCEPT_ONLY_THREE_TEAM_MATCHING_LEGAL_IMPLEMENTATION_EXISTENCE',
            actual_CBA_pages_read=[193,233,234,235,236,248,252,398],NBA_officials_guide_page_read=4,
            reviewed_repository_input_SHA_count=12,reviewed_raw_SHA_count=5,
            actual_source_bodies_and_all_three_team_Decimal_piecewise_interval_algebra_checked=True,
            independent_negative_tests=['actual_acceptance','drop_six_month_floor','WAS_current_only_waiver',
                                        'atomic_reaggregation','same_total_upstream_contract_mutation'],
            independent_negative_rejections=5,
            descendants=dict(affected_candidate_contracts=['Theis','Green','Gafford'],
                accepted_constraint='Old contract extension/renegotiation >= max(2021-09-25, otherwise eligible date) if consensual waiver implementation is actually selected',
                actual_waiver_or_consent_selected=False,ordinary_new_FA_contract_is_not_automatically_old_contract_extension=True,
                exact_2021_future_contract_execution_certified=False),
            new_source_collection_by_independent_reviewer=False,whole_G16_independent_pass=False),
        reopen=['New contract/performance/source input','Changed player direction or pretrade contract event',
                'Changed current TeamSalary upper or rule applicability evidence','Actual future extension/renegotiation before permissible date'],
        tools={'Antigravity':{'status':'SOURCE_ATTEMPT_RETURNED_EMPTY_NO_NEW_EVIDENCE',
                             'evidence':ag_path,'evidence_sha256':sha(ROOT/ag_path),
                             'elapsed_seconds':53.001,'new_verified_source_bodies':0,
                             'terminal_SUCCESS_does_not_certify_source_evidence':True},
               'NotebookLM':{'status':'TERMINAL_RECOVERED_ANALYSIS_ONLY',
                             'evidence':nlm_path,'evidence_sha256':sha(ROOT/nlm_path),
                             'source_id':nlm['source_id'],
                             'source_import_elapsed_seconds':nlm['source_import']['elapsed_seconds'],
                             'analysis_elapsed_seconds':nlm['analysis']['elapsed_seconds'],
                             'input_phase':'FROZEN_PRE_ACCEPTANCE_CANDIDATE_MD_SNAPSHOT_NOT_CURRENT_ACCEPTED_MD',
                             'candidate_MD_normalized_SHA256':'c94f21a72c8f8cdad38c68d978973d797535b314f8471ac4ce3e62cea7c3aed3',
                             'current_status_not_retroactively_attributed_to_snapshot':True,
                             'shorthand_September25_restriction_corrected_to_exact_max_boundary':True,
                             'source_code_independent_or_G16_certified':False},
               'Claude':{'status':'TERMINAL_RECOVERED_REBUTTAL_ALL_THREE_OBJECTIONS_REJECTED_BY_PRIMARY',
                         'evidence':claude_path,'evidence_sha256':sha(ROOT/claude_path),
                         'elapsed_seconds':claude['result']['elapsed_seconds'],
                         'disposition_evidence':'reviews/E1_FINAL_FUNCTION_AND_CHI_F1_SCOPE_REVIEW_2026_10_07.md',
                         'rejected_objections':['CHI125percent_only_omits_nonTax175percent_branch',
                                                'February_deadline_assumed_despite_2021_March25_primary_date',
                                                'Conflates_belowcap_matching_election_with_waiver_and_misreads_explicit_sixmonth_clause'],
                         'original_sources_supplied':0,'original_code_supplied':0,
                         'source_code_or_G16_certified':False}})


def validate(data):
    if data != build():
        raise ValueError('source, family, algebra or authority differs from full reconstruction')


def render(d):
    return '''# F1 Chicago–Washington–Boston — 전체 법적 구현 존재 증인

2026-10-07 / 기준 main43e359c / [JSON](CHI_F1_MATCHING_EXISTENCE_WITNESS_2026_10_07.json) / [검문기](../tools/build_chi_f1_matching_existence_witness.py)

**세 팀 전체 matching의 제한적 법적 구현 존재 범위 수용. 실제 financial 선택0·원고 CLOSED.** 이 산출물 자체의 원장 승격은0이며 중앙 판정은 부모가 별도 처리한다.

## 승인 기준과 정확한 양화 범위

원 S2는 닫힌 구간 또는 완전한 문서/분기 증인을 허용한다. 이미 통과한 BOS/TPE·DEN matching도 승인 선수 방향의 합법적 배정/동시 구현 존재를 검문하며 실제 순서·예외배정·승낙·정확 금융조건은 선택하지 않았다. 같은 권위로 외부 계약 입력 전부에 대해 허용 구현이 존재하는지 검문한다. 임의 실제 면제 선택 전부가 통과한다는 추가 ∀q 요구는 원 승인문/검사기에 없다. 기존 무면제 상단은 모든 구현 안전성을 반증하지만 구현 존재를 반증하지 않는다. 이 해석 수리는 원 S2의 범위 변경이나 금융 선택이 아니다.

외부 계약 입력 ∀Γ에 대해 허용 합의량 ∃q와 동일 선수 이동의 원자적 구현이 존재한다. 선수와 양도 구단이 그 합의를 실제로 체결했다는 사실은 주장하지 않는다. 실제 Γ/q/선수 동의/양도·수취 구단 합의/접수와 정확 금융 선택은 모두null이며 A2/K·시즌 실행과 분리한다.

## 한 원자 거래의 세 팀 전체 범위

CHI Gafford→WAS, Kornet→BOS; WAS Wagner→BOS; BOS Theis/Green→CHI. Wagner를 Chicago에 먼저 받은 뒤 재합산하지 않는다. 최저급 예외나 서로 다른 예외 합산도 쓰지 않는다.

| 팀 | 최소 송출 | 보수 한도 | 모든 외부 계약 입력에 대한 허용 수취 상한 | 여유 |
|---|---:|---:|---:|---:|
| CHI | 3,767,981 | 6,693,966.75 | 6,517,981 + min(ΓT+ΓG,175,985.75) | 최소0 |
| BOS | 6,517,981 | 8,247,476.25 | Kornet2,587,500 + Wagner2,161,920 =4,749,420 | 3,498,056.25 |
| WAS | Wagner1,441,280 | 1,901,600 | Gafford1,517,981 after permissible full bonus waiver | 383,619 |

CHI는 q=max(0,ΓT+ΓG−175,985.75), qT=min(ΓT,q), qG=q−qT를 허용 후보 함수로 둔다. ΓT∈[0,750,000], ΓG∈[0,227,697.15] 전 구간에서 각 면제량은 자기 보너스를 넘지 않으며 잔여 보너스 합은 한도 안이다. 이 전 구간 대수 증명은 일부 경계 샘플을 전체 증거로 올리지 않는다. 최대 후보 합의량801,711.40은 실제 면제/위법 금액이 아니다.

WAS의 빠졌던 Gafford 보너스도 포함한다. 남은 모든 연도·보호 배분의 eligible total trade bonus를 전부 면제할 수 있는 후보를 두면 VII3(b)의 모든 배분에서 당해 추가액도0이다. 미래 기본급/옵션/보호 금액을 임의 확정하거나 실제 보너스0을 인증하지 않는다. 현재 Gafford 기본급1,517,981과 성과0/0는 기존 입력과 이번 SalarySwish 본문 HTTP200 행이 일치한다. 원 계약/거래일 장부 인증은 아니다.

## 원문·당해 날짜와 비용

2017 CBA PDF193 VII3(b), PDF233–235 VII6(j)(1)/(3), PDF236 VII6(j)(5), PDF248 VII7(d)(3), PDF252 VII8(d), PDF398 XXIV2를 직접 읽었다. 특히 VII6(j)(3)은 cap미만팀도 6(m)에 우선해 동시 matching을 선택할 수 있게 한다. BOS/WAS의125%+100k는 cap상하·납세/비납세 모두 안전하므로 새 WAS 전체 비공개 급여 장부는 필요 없다. 보너스 면제는 post-assignment 수취액만 줄이며 송출 matching은 pre-trade Salary 하한을 사용한다.

CHI 기존 전체비용132,367,326.15는 무면제 전체상단까지 포함하며 tax132,627,000 이내다. 면제는 이 상단을 악화하지 않는다. BOS 기존 중간/후속 비용4상태 최대138,716,242도apron138,928,000 이내이고 Hayward사용0을 보존한다. WAS matching 종료는 전체 비용·실제 납세/하드캡 인증이 아니다.

NBA Officials 2020–21 Guide PDF4는2/27 standard-contract 잔여 보장·3/25 거래 마감·5/16 정규 종료를 직접 확인한다. 3/25 송출은 그 구간 안이다. 보존 공개 feed의2019 Gafford/Kornet/Theis/Green 서명과 Wagner 취득을 연결하고 직전2개월 신규 사건 없음을 지정 공개 가족에서 대조했다. 미공표 전역 부재 인증은 아니다. 후보 순서에 새 취득 후 즉시 재합산은 없다.

세부 숫자는 원 CBA이고 당해 적용 지원은 기존 수용 BOS/DEN과 같은 NBA3/16 연결 및 원 cap분석가3/10 설명이다. NBA 기사가175% 숫자를 직접 인증했다거나2020개정 전문을 회수했다는 뜻은 아니다. 공식 가이드는 변경된 날짜를 긍정 확인한다. 보도자료 침묵으로 규칙 불변을 추론하지 않는다.

면제 후보는 Theis/Green/Gafford 원 계약의 연장·재협상을9/25 또는 원래 가능일 중 늦은 날까지 제한한다. 만료 후 일반 새 FA 계약과 원 계약 연장은 구분하며2021 정확 계약의 전체 실행을 자동 통과시키지 않는다. 이 제약은 후손 실행 증인에 전달해야 한다.

## 독립 검문과 도구의 실제 회수 범위

den 독립 검문자는 실제 CBA8쪽·Officials PDF4·기존 입력SHA12·rawSHA5와 원본문, 세 팀 Decimal/piecewise 전구간 대수를 직접 대조했다. 추가 음성5개(actual acceptance 승격, 6개월 경계 제거, Gafford 현재연도만 면제, 신규 취득 재합산, 동일총액 upstream 개별 계약상한 변조)가 모두 거부됐다. 부모는 같은 S2 legal-existence 한 행 범위를 수용했다. 이 독립 검문은 실제 승낙/금융 선택·2021 정확 계약 실행·전체G16 완료가 아니다.

Theis/Green/Gafford 원 계약의 면제 후보를 실제 택하는 경우 연장·재협상≥max(2021-09-25,원래 가능일) 제약을 후손에 전달한다. 일반 만료 뒤 새 FA 계약은 자동으로 원 계약 연장이 되지 않는다. 정확한2021 후속 계약 전체는 여전히 미인증이다.

검문기는 원자료 SHA·본문/가이드 조항 지문·보존 계약 사건·검문된 기존 입력 버전·양화/세 팀/권한 전체 재구성을 검사한다. 실제 금융 선택·본인 원장/중앙 변경·원고0.

Antigravity는 [별도 Green 공식 서명 원문 시도](../reviews/CHI_F1_ANTIGRAVITY_SOURCE_ATTEMPT_2026_10_07.json)를53.001초 실행했지만 최종 응답이 비었고 새로운 검증 본문0이다. terminal SUCCESS를 원자료 회수 성공으로 올리지 않는다.

NotebookLM의 [불변 후보사본 분석](../reviews/CHI_F1_NLM_EXISTENCE_ANALYSIS_2026_10_07.json)은 수입17.199초·질의60.059초 뒤 회수됐다. source79e449fe…는 후보MD 지문c94f21…aed3인 수용 전 스냅샷이며 현재 수용 상태를 이전 입력에 소급하지 않는다. 사본의 관계분석만 회수했고 원CBA/코드/독립/G16 인증은false다. 응답의 “9/25까지”는 정확한max(9/25,원래가능일) 이후 제약으로 교정했다.

Claude의 [결과설명만 본 반증](../reviews/CHI_F1_CLAUDE_EXISTENCE_BLIND_2026_10_07.json)은56.285초 뒤 회수됐다. [부모 disposition](../reviews/E1_FINAL_FUNCTION_AND_CHI_F1_SCOPE_REVIEW_2026_10_07.md)에서 세 지적을 원문으로 대조해 모두 기각했다: CHI에125%만 적용한 지적은 비납세175% 분기를 누락했고, 2월 마감 가정은2021공식3/25 날짜에 반하며, 면제와cap미만 동시교환 election을 합친 오독/6개월 범주오류는 VII7(d)(3)의 명시 조항에 반한다. 회수 성공과 지적의 유효성은 별도이며 원자료/코드/G16 인증은false다.
'''


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    d=build();validate(d)
    body=json.dumps(d,ensure_ascii=False,indent=2)+'\n'; md=render(d)
    if args.check:
        if normalized(OUT)!=body or normalized(MD)!=md:
            raise ValueError('saved witness stale')
    else:
        OUT.write_text(body,encoding='utf-8',newline='\n');MD.write_text(md,encoding='utf-8',newline='\n')
    n=0
    if args.self_test:
        for label in ['omit_WAS_bonus','actual_consent','actual_waiver','tax_bound','drop_team','reaggregate','extension_clearance','own_SHA']:
            x=deepcopy(d)
            if label=='omit_WAS_bonus':x['WAS']['external_Gafford_total_Gamma']='zero'
            elif label=='actual_consent':x['authority']['actual_player_consent']=True
            elif label=='actual_waiver':x['authority']['actual_waiver_quantities']={'Theis':'750000'}
            elif label=='tax_bound':x['CHI']['post_team_salary_upper_usd']='132627001'
            elif label=='drop_team':x.pop('WAS')
            elif label=='reaggregate':x['topology']['newly_acquired_contract_reaggregated']=True
            elif label=='extension_clearance':x['authority']['full_future_contract_execution_certified']=True
            else:x['source_sha256'][SELF]='0'*64
            try:validate(x)
            except ValueError:n+=1
            else:raise AssertionError(label)
        original_normalized=normalized
        path=ROOT/'research/BOSTON_DATED_TPE_CAPACITY_WITNESS_2026_10_05.json'
        forged=load('research/BOSTON_DATED_TPE_CAPACITY_WITNESS_2026_10_05.json')
        forged['sequence_existence_witness'][0]['Kornet_full_base_bonus_upper_usd']=1
        def forged_read(p):
            return json.dumps(forged) if p==path else original_normalized(p)
        globals()['normalized']=forged_read
        try:
            try:build()
            except ValueError:n+=1
            else:raise AssertionError('same-total forged upstream source accepted')
        finally:globals()['normalized']=original_normalized
        for t,g in [('0','0'),('750000','227697.15'),('175985.76','0'),('0','227697.15')]:
            qt,qg,received=waiver(t,g)
            assert received<=D('6693966.75')
        # A real interval-crossing risk remains outside the existential implementation.
        assert D(6517981)+D(750000)+D('227697.15')>D('6693966.75')
    print(json.dumps({'status':d['status'],'teams':3,'external_interval_algebra':'PASS','negative_tests':n,
                      'register_promotion':0,'actual_financial_selection':False,'manuscript_allowed':False}))


if __name__=='__main__':main()
