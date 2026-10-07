"""Join the reviewed AP1/SG16 candidate to its reviewed OKC cost witness."""
import argparse
import hashlib
import json
from pathlib import Path

import build_2021_bos_okc_hou_pick16_working_execution as trade
import build_okc_2021_ap1_full_cost_family as cost

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_2021_pick16_cost_closure_bridge.py'
OUT = 'research/NBA_2021_PICK16_COST_CLOSURE_BRIDGE_2026_10_07.json'
MD = OUT[:-5] + '.md'

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

def sha(path):
    text = (ROOT / path).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(text.encode()).hexdigest()

def build(reader=read):
    t, c = reader(trade.OUT), reader(cost.OUT)
    assert not trade.validate(t), 'Reviewed transaction candidate not current'
    assert not cost.validate(c), 'Reviewed OKC cost family not current'
    assert t['independent_review_completed'] is True
    assert c['scope']['independent_review_completed'] is True
    assert t['authority']['long_term_trade_direction_selected'] is False
    assert c['scope']['AP1_SG16_author_selected'] is False
    assert t['calendar']['AP1_working_date'] == '2021-07-28'
    assert t['calendar']['SG16_working_date'] == '2021-07-29'
    assert t['calendar']['new_salary_cap_year_start'] == '2021-08-03'
    a, b = c['arithmetic'], t['cost_boundary']
    assert a['cap_usd'] == t['calendar']['cap_usd'] == 109140000
    assert a['apron_usd'] == t['calendar']['apron_usd'] == 138928000
    assert a['sufficient_pretrade_usd'] == b['OKC_pretrade_apron_sufficient_upper_usd']
    assert a['OKC_pretrade_apron_upper_usd'] <= a['sufficient_pretrade_usd']
    assert a['post_AP1_apron_upper_usd'] == a['OKC_pretrade_apron_upper_usd'] + b['OKC_cost_delta_if_outgoing_Brown_young_FA_floor_usd']
    assert a['post_AP1_apron_upper_usd'] <= a['apron_usd']
    assert b['BOS_candidate_after_AP1_upper_usd'] <= a['apron_usd']
    assert b['HOU_SG16_current_contract_salary_delta_usd'] == 0
    assert b['HOU_new_signed_rookie_contract'] is False
    assert c['implementation']['Brown_next_year_protection_credit_family'] == t['proposed_matching_implementation']['Brown_agreed_next_year_protection_family_usd']
    assert t['summary']['actors'] == 3 and t['summary']['named_asset_or_contract_edges'] == 9
    assert t['summary']['conditional_control_matches_G7'] == len(t['draft_control_candidate_rows']) == 60
    assert all(len(r['conditional_after_AP1']) <= 20 for r in t['dated_working_rosters'].values())
    assert c['dated_states'][-1]['offseason_total_including_TW'] == len(t['dated_working_rosters']['OKC']['conditional_after_AP1']) == 16
    sources = [SELF, trade.SELF, trade.OUT, cost.SELF, cost.OUT]
    return {
        'schema': 'PICK16_REVIEWED_FINANCIAL_INPUT_CLOSURE_BRIDGE_V1',
        'status': 'INDEPENDENTLY_REVIEWED_FINANCIAL_INPUT_CLOSURE_BRIDGE',
        'source_rev_sha256': {p: sha(p) for p in sources},
        'scope': 'SAME_OLD_YEAR_PUBLIC_CATEGORY_FAMILY_AND_PROPOSED_CONSENTING_IMPLEMENTATION_ONLY',
        'public_family_AP1_remaining_OKC_budget_gap_closed': True,
        'prior_AP1_null_is_preserved_historical_snapshot': True,
        'candidate_events': t['events'],
        'budget': {
            'cap_year': '2020-21', 'apron_usd': a['apron_usd'],
            'BOS_after_AP1_upper_usd': b['BOS_candidate_after_AP1_upper_usd'],
            'BOS_apron_margin_usd': b['BOS_candidate_after_AP1_apron_margin_usd'],
            'OKC_before_AP1_upper_usd': a['OKC_pretrade_apron_upper_usd'],
            'OKC_after_AP1_upper_usd': a['post_AP1_apron_upper_usd'],
            'OKC_apron_margin_usd': a['post_AP1_apron_margin_usd'],
            'HOU_unsigned_rights_apron_delta_usd': 0,
            'HOU_scope': 'At the modeled atomic SG16 instant after selection and before any new #16 RequiredFirstTender, no executed UPC or outstanding tender is acquired; preexisting DET/WAS claims change holder. The ordinary unsigned first-round hold is distinct and excluded from apron by VII6(m)(3)(ii)(E), which includes outstanding RequiredTenders. For any valid preserved prior HOU budget this restricted event leaves apron cost invariant. Later tender/UPC issuance reopens cost. No actual HOU whole-ledger certificate is claimed.',
            'HOU_SG16_working_instant_before_first_RequiredTender': True,
            'HOU_new_RequiredFirstTender_outstanding_at_SG16': False,
            'HOU_required_tender_absence_is_routine_candidate_not_actual_receipt_claim': True,
        },
        'matching_and_asset_evidence': {
            'three_actors_nine_edges_and_control60': True,
            'Brown_q_min_usd': 423280, 'Brown_q_max_usd': 1701593,
            'all_existing_bonus_branches_use_proposed_consensual_waivers': True,
            'extension_renegotiation_limits_preserved': True,
            'future_protected_DET_WAS_claims_unchanged': True,
            'no_new_2028_obligation_created': True,
        },
        'remaining': [
            'AP1/SG16 material author direction remains unselected.',
            'Sengun must remain available at16 after the preceding draft selections; the other58 selections are not promoted by this bridge.',
            'No actual contract consent, q, waiver, league filing, future claim delivery or cents is certified.',
            'A new outstanding #16 RequiredTender, Aug3 new-year budgets, executed rookie UPCs and 2021–23 future events require their own implementation.',
        ],
        'independent_review_completed': True,
        'author_selected': False, 'canon_promoted': False, 'macro3_complete': False,
        'whole_actual_legal_or_registration_certified': False,
        'manuscript_allowed': False, 'design_gate': 'CLOSED', 'freeze': 'v0.30 PARTIAL',
    }

def render(d):
    b = d['budget']
    return f"""# #16 후보의 OKC 비용 입력 종료 연결

상태 `{d['status']}`. 기존 #16 후보의 null/HOLD는 과거 스냅샷으로 보존하고, 독립 검토된 동일 old-year OKC 비용 가족을 새 연결 파일에서 소비한다.

| 팀 | July28 후보 뒤 비용 경계 | apron 여유 |
|---|---:|---:|
|BOS|{b['BOS_after_AP1_upper_usd']:,}|{b['BOS_apron_margin_usd']:,}|
|OKC|{b['OKC_after_AP1_upper_usd']:,}|{b['OKC_apron_margin_usd']:,}|
|HOU|July29 최초 #16 RequiredTender 전인 후보 순간의 미서명 권리 취득: apron 차액0|유효한 이전 보존 예산의 여유 불변; 전체 실제 원장 재인증 아님|

OKC 거래 전 상단 {b['OKC_before_AP1_upper_usd']:,}은 충분조건133,669,464 이하다. July28/29는 Aug3 새 capyear 전이므로112.414m을 사용하지 않는다. 3팀9양도·control60·Brown 보호-only q≥423,280·기존 bonus의 합의 면제·후속 extension 제한·원 보호객체를 같은 후보에서 연결한다.

이 연결은 공개 가족의 남은 OKC 예산 입력을 닫는다. AP1/SG16 방향, Sengun의16번까지 가용성과 다른58선택, 실제 q/동의/접수, 이후 신인 계약·새 capyear·후속 시즌을 확정하지 않는다. HOU는 같은 draft-day 원자적 순간에 아직 #16 RequiredFirstTender를 제안하지 않는 routine 후보 조건이다. VII6(m)(3)(ii)(E)는 일반 unsigned1R hold를 apron에서 제외하지만 outstanding RequiredTender를 포함하므로, 새 Tender 제안이나 UPC는 비용 재개방이다. 실제 제안·접수 부재를 인증하지 않는다. 기존 #16 및 OKC 파일의 직접 원문·지문·독립 검토 기록을 참조한다.

전체macro3·실제 법적/등록 인증·정본 승격0, freeze v0.30 PARTIAL·설계/원고CLOSED.
"""

def validate(saved):
    try:
        return [] if saved == build() else ['Financial closure bridge differs from reviewed inputs']
    except (AssertionError, KeyError, ValueError, TypeError, OSError) as exc:
        return [str(exc)]

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--write', action='store_true'); p.add_argument('--check', action='store_true')
    args = p.parse_args(); data = build()
    if args.write:
        (ROOT / OUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MD).write_text(render(data), encoding='utf-8')
    if args.check:
        assert not validate(read(OUT))
        assert (ROOT / MD).read_text(encoding='utf-8-sig') == render(data)
    print(json.dumps({'current': True, 'OKC_budget_gap_closed': True, 'budget': data['budget'], 'author_selected': False}, ensure_ascii=False))
