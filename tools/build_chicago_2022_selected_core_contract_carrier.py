"""Select the reviewed E2/CX1 continuity family; preserve upstream comparisons."""
from pathlib import Path
from copy import deepcopy
import argparse, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_chicago_2022_selected_core_contract_carrier.py'
OUT = 'simulation/CHICAGO_2022_SELECTED_CORE_CONTRACT_CARRIER.json'
MD = OUT[:-5] + '.md'
AUTH = 'reviews/MACRO3_FINITE_EXIT_AND_CORE_ROUTINE_AUTHORITY_AUDIT_2026_10_07.md'
JOIN = 'research/CHICAGO_2022_JULY7_NAMED_ROSTER_CONTRACT_COST_JOIN_2026_10_07.json'
P = 'research/PROTAGONIST_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07.json'
C = 'research/CARTER_2021_EXTENSION_CANDIDATE_FAMILY_2026_10_07.json'
L = 'research/LAVINE_2022_CONTRACT_CANDIDATE_FAMILY_2026_10_07.json'
YS = 'research/CHICAGO_2022_YOUNG_SATORANSKY_ROSTER_FAMILY_2026_10_07.json'
PINS = {
    'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2',
    AUTH: '22e422447f84051a18ffdfcef710f90d54c2bc7dc6d30fc9447936930646a83a',
    JOIN: '9f3e19c38f7be2a7259158cf4ba8f7440aca400593092d400cac23fa2917074a',
    P: '84040384319b79d9bd2d87575d3f7061337c8978775278e1fa4dd8677e5b3228',
    C: '070f1393070644540642284e9f1a6b49a2c6d1c1903fade2610d8570344d1f21',
    L: '2c7cf936b8387521e46f67cd245358bbd5c8191c99c466da9ae8b4b7c7d635d0',
    YS: '9a1e49c1f0b9d3c95279ff675ac3c42c2a72384c8ed6d11cbeb917e5903ac363',
}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def text(p):
    return p.read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def sha(p):
    return hashlib.sha256(text(p).encode()).hexdigest()


def read(root, name):
    return json.loads(text(root / name))


def build(root=ROOT):
    for p, h in PINS.items():
        need(sha(root / p) == h, 'Reviewed source changed: ' + p)
    src = {p: read(root, p) for p in (JOIN, P, C, L, YS)}
    for p, value in src.items():
        need(value == json.loads(text(root / p)), 'Returned source differs: ' + p)
    j, p, c, l, ys = (src[f] for f in (JOIN, P, C, L, YS))
    need(j['certification']['independent_review_completed'], 'Existing named join unreviewed')
    # Validate consumed frozen upstream pins, without invoking ancestor constructors.
    for f, h in j['source_sha256'].items():
        need(sha(root / f) == h, 'Named join ancestor changed: ' + f)
    e2 = deepcopy(next(x for x in p['alternatives'] if x['id'] == 'E2'))
    cx1 = deepcopy(next(x for x in c['alternatives'] if x['id'] == 'CX1'))
    lav = deepcopy(l['terms_candidate'])
    young = deepcopy(next(x for x in ys['forms']['Young'] if x['id'] == 'Y_BIRD_8M'))
    sato = deepcopy(next(x for x in ys['forms']['Satoransky'] if x['id'] == 'S_MINIMUM'))
    need(e2['salary_2022_onward'] == [22000000, 23760000, 25520000, 27280000]
         and e2['total_known_schedule'] == 98560000 and not e2['franchise_move_or_offer_sheet_selected'], 'E2 continuity changed')
    need(cx1['total_extended_regular_salary'] == 50000000 and not cx1['2022_QO_RFA_or_FAhold_arises_if_extension_is_actually_implemented'], 'CX1 live term/QO changed')
    need(lav['salary'] == [37096500, 40064220, 43031940, 45999660, 48967380]
         and lav['one_player_option_cap_year'] == 2026 and lav['option_exercise_selected'] is None, 'LaVine future option changed')
    need(young['base_schedule'] == [8000000, 8000000]
         and sato['base_schedule'] == 'L_2022_23(creditedYOS,Year1)', 'Veteran family changed')
    rows = deepcopy(j['named_contract_rows'])
    standard = [x['player'] for x in rows if x['roster_type'] == 'STANDARD']
    tw = [x['player'] for x in rows if x['roster_type'] == 'TWO_WAY']
    # A producer must not turn a lawful minimum upper into an exact salary.
    need(len(standard) == 15 and len(tw) == 2 and len(set(standard + tw)) == 17, 'Selected identities/slots changed')
    need(set(tw) == {'Devon Dotson', 'Tyler Cook'}, 'Named TW family changed')
    cost = deepcopy(j['joined_cost'])
    live = sum(x['normal_upper'] for x in rows if x['roster_type'] == 'STANDARD')
    need(live == cost['live15_normal_upper'] == 141378541, 'Live cost join changed')
    need(live + cost['legacy_original_stretch_upper'] + cost['named_first_and_two_second_reservations_normal'] == cost['normal_public_family_upper'] == 170845541, 'Normal upper changed')
    need(live + cost['legacy_original_stretch_upper'] + cost['named_first_and_two_second_reservations_apron'] == cost['apron_public_family_upper'] == 172483541, 'Apron upper changed')
    need(cost['apron_no_FY22_trigger'] and not cost['negative_margin_is_actual_illegal'], 'No hardcap family changed')
    events = [
        {'date': '2021-10-01', 'action': 'Valid Coby fourth-year and LaMelo third-year signed option notices selected in the fictional model; actual delivery not certified.'},
        {'date': '2021-10-15', 'action': 'Consensual CX1 extension selected; old term and accrued obligations retained; extended term starts July1 2022.'},
        {'date': '2022-06-29', 'action': 'Do not issue Dotson/Cook QOs. Issue timely ordinary protagonist QO using the complete reviewed starter/pick/component function, unaccepted before E2; not a flat surrogate salary.'},
        {'date': '2022-07-01', 'action': 'Carry10 plus CX1 live; keep expired-player FA/QO claims and TW UFA holds pending replacement. No accepted new rookie UPC.'},
        {'date': '2022-07-07', 'time_ET': '12:00:00_ORDERED', 'action': 'Consensual LaVine directBird5 -> E2 directBird4 -> Young Bird2 -> Satoransky statutory minimum1 -> Dotson/Cook eligible one-year TW -> valid written unused annual exception renunciation.'},
    ]
    return {
        'id': 'CHICAGO_2022_SELECTED_CORE_CONTRACT_CARRIER',
        'baseline_main': '4fa062ddabbe97403700544b87d95bb6f8560e0d',
        'status': 'ROOT_ROUTINE_DESIGN_IMPLEMENTATION_SELECTED_INDEPENDENT_REVIEW_PENDING',
        'source_sha256': {**PINS, SELF: sha(root / SELF)},
        'authority': {'routine_continuity_audit': AUTH, 'new_human_price_lock': False, 'health_delegation_is_price_authority': False, 'new_important_franchise_or_title_choice': False},
        'selected_working_forms': {'Protagonist': e2, 'Carter': cx1, 'LaVine': lav, 'Young': young, 'Satoransky': sato},
        'selection_semantics': 'Upstream candidate flags are preserved quotations. This carrier selects those existing forms and fictional mutual acceptance for the working design under the continuity audit. It does not certify real acceptance or create an exact author lock.',
        'why': 'Existing E2+CX1 Chicago continuity, LaVine banner/coace progression and M1/A growth core. E2 does not reduce core status or impose a performance ceiling. Retain Young and Satoransky support without a new core-changing trade.',
        'selected_working_events': events,
        'selected_registration_July7': {'STANDARD': standard, 'TWO_WAY': tw, 'STD': 15, 'TW': 2, 'actual_game_active_or_clinical_status_certified': False},
        'named_contract_cost_rows': rows,
        'preserved_public_cost_family': cost,
        'preserved_TW_eligibility': deepcopy(j['named_TW_prior_bridge']),
        'unregistered_draft_and_foreign_ports': deepcopy(j['rights_and_unregistered_ports']),
        'old_obligations': 'All original accrued/protected/bonus/legacy costs remain in their reviewed categories. New plain terms are consensual modeled terms; no historical private bonus absence or retrospective salary haircut is asserted.',
        'future_boundaries': ['CHI2022 draft rank/identity and timely required tenders remain next inputs; unsigned rights consume no STD; acceptance would need a named roster replacement.', 'Simonovic after July29 needs the separate X5/X6 notice/tender/foreign availability branch.', 'LaVine 2026 option decision and new 2026 protagonist price remain unselected; future option salary is not removed.', '2022-23 dated roles/health, playoff result, 2023 Coby RFA/LaMelo extension and July1 new CBA remain unfinished.'],
        'certification': {'selected_fictional_acceptance_and_existing_forms': True, 'exact_author_price_lock': False, 'actual_private_receipt_or_consent': None, 'whole_FY22_or_macro3_complete': False, 'new_external_AGY_NLM_Claude_run': 'NOT_RUN', 'manuscript_allowed': False, 'design_gate': 'CLOSED', 'freeze': 'v0.30 PARTIAL'},
    }


def markdown(v):
    lines = ['# Chicago 2022 코어 계약 선택 소비기', '',
             '기존 독립 검문 가족의 **routine 설계 선택**이다. 새 작가 금액 잠금·실제 접수 인증과 구분한다. 원 후보 문서를 덮어쓰지 않는다.', '',
             'E2 Chicago 4년98.56m / CX1 4년50m / LaVine directBird5년(마지막2026 선수옵션) / Young Bird2년8m씩 / Satoransky 법정최소1년을 선택한다. 옵션행사·주인공2026 새급여는 미선택이다.', '',
             '기존 Chicago 원클럽·LaVine 간판→공동에이스·M1/Caruso 성장코어의 구현이며, E2를 성장 제한 또는 코어 지위 할인과 교환하지 않는다.', '',
             '| 날짜 | 선택된 가상 작업 |', '|---|---|']
    lines += [f"| {x['date']} | {x['action']} |" for x in v['selected_working_events']]
    lines += ['', 'July7 15STD/2TW. 실제 경기 active/건강·신인 UPC·whole FY22는 미인증이다. 새 TW의 필수 전환옵션·기간·YOS 조건을 보존한다.', '',
              '동일 명단 공개 비용의 보수 상단은 normal170,845,541 / apron172,483,541. 정확 급여가 아니며 Sato3m는 법정 최소의 상단이다. FY22 NTMLE/BAE/S&T를 쓰지 않아 apron 초과만으로 위법을 판정하지 않는다. 과거 보호비용·성과·stretch를 지우지 않는다.', '',
              '남은 실제 입력: 2022 픽/선수·Tender, 수락 시 명단 치환, Simonovic 후속 권리, 2022–23 날짜별 역할/결과, 2023 후손. 기존17명 연결의 검사만 재사용하며 82경기 뒤에만 계약을 처리하는 새 게이트를 만들지 않는다.', '',
              f'[권한 감사](../{AUTH}) · [원 조건부17명 연결](../{JOIN[:-5]}.md)', '',
              '외부 CLI 신규 NOT_RUN. v0.30 PARTIAL·설계/원고 CLOSED·원고0. 미완료5묶음 /6번까지4.', '']
    return '\n'.join(lines)


def main():
    a = argparse.ArgumentParser(); a.add_argument('--write', action='store_true'); a.add_argument('--check', action='store_true'); o = a.parse_args(); v = build()
    if o.write:
        (ROOT / OUT).write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MD).write_text(markdown(v), encoding='utf-8')
    if o.check:
        need(read(ROOT, OUT) == v and text(ROOT / MD) == markdown(v), 'Selected contract carrier stale')
    print(json.dumps({'STD': 15, 'TW': 2, 'core_forms': 'E2/CX1/Bird5', 'normal_upper': v['preserved_public_cost_family']['normal_public_family_upper'], 'apron_upper': v['preserved_public_cost_family']['apron_public_family_upper'], 'whole_macro3_complete': False}))


if __name__ == '__main__':
    main()
