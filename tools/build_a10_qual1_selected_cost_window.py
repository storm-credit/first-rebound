"""Selected QUAL1 setting and two cost observations; no series winner or NBA facts."""
from __future__ import annotations
import argparse, copy, hashlib, json
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a10_qual1_selected_cost_window.py'
OUT = 'simulation/A10_QUAL1_SELECTED_COST_WINDOW.json'
PACK = 'research/A10_2024_25_QUAL1_FINITE_ROUTE_PACKET_2026_10_08.json'
SELECT = 'canon/DELEGATED_A10_QUAL1_COST_WINDOW_SELECTION_2026_10_08.json'
PEER = 'reviews/A10_QUAL1_FINITE_ROUTE_CHI_INDEPENDENT_REVIEW_2026_10_08.json'
PINS = {PACK: '0f50db389c792fe80ffd41dd1609a47c3ae94c2e52dbb2c9cb2ecf8b7b49991a', SELECT: '668bf587ed008e9aeb96d73e062a053bbab6e009b18e77b6b8634dd5c4b37006', PEER: 'db1c67dbb90709dcd9373822da2540d6591b366a497be8a0bff08648e34bb0fb'}

def text(path):
    return (ROOT/path).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')

def sha(path): return hashlib.sha256(text(path).encode('utf-8')).hexdigest()
def serial(obj): return json.dumps(obj, ensure_ascii=False, indent=2)+'\n'

def physical():
    assert all(PINS.values()), 'Actual root selection and independent peer pins not yet supplied; output write prohibited'
    for path, digest in PINS.items():
        assert sha(path) == digest, 'Physical QUAL1 input changed: '+path
    return {path: json.loads(text(path)) for path in PINS}

def source_inputs(): return physical()

def assert_inputs(s):
    assert s == physical(), 'Returned source or source alias differs from independent physical input'
    q, z, peer = s[PACK], s[SELECT], s[PEER]
    assert z['root_selected'] is True and z['selected'] is True, 'Template is not a root selection'
    assert z['source_packet_sha256'] == PINS[PACK]
    assert z['independent_peer'] == PEER and z['independent_peer_sha256'] == PINS[PEER]
    assert peer['source_sha256'][PACK] == PINS[PACK], 'Peer reviewed a different packet'
    assert 'ACCEPT' in peer['status'] and 'PENDING' not in peer['status'], 'Independent packet acceptance required'
    assert z['selected_route'] == q['recommended_route'] == 'QUAL1_A_DIRECT6_PHI3_RECOMMENDED'
    assert z['East_order'] == q['qualification_port']['A_candidate_full_East_order']
    assert [r['rank'] for r in z['East_order']] == list(range(1, 16))
    assert len({r['team'] for r in z['East_order']}) == 15
    assert all(r['win_loss'] is None for r in z['East_order'])
    assert (z['CHI_playoff_seed'], z['PHI_playoff_seed'], z['qualification_date']) == (6, 3, '2025-04-13')
    assert z['setting_admission_not_82_derived'] and not z['whole_regular_season_executed']
    assert z['selected_contract_piecewise_service_notice_domain'] and z['all_original_Gamma_and_six_cost_functions_preserved']
    assert z['exact_private_prices_or_receipts'] is None
    assert z['selected_series_period'] == q['recommended_series_source_inputs']['period']
    assert z['registration_and_availability'] == q['proposed_registration_and_availability']
    assert z['new_series_fictional_availability_selected'] and z['selected_reference_capacity'] and z['fictional_0OT_selected']
    assert (z['regulation_seconds'], z['each_team_player_seconds']) == (2880, 14400)
    assert all(z[k] is None for k in ['series_winner', 'full_game_scores'])
    assert all(z[k] is False for k in ['first_option_efficiency_certified', 'whole_A10_complete', 'Chicago_title_MVP_or_new_author_lock', 'actual_clinical_or_registration_certified', 'manuscript_allowed'])
    f=q['recommended_series_source_inputs']['PHI_floor_and_trigger_conditions']
    assert f['published_minimum_team_salary24']==126529000 and f['law_derived_minimum_team_salary24']==140588000*9//10==126529200
    assert f['MTSgap_formula']=='max(0,126529200-min(MTS_current24,MTS_opening24))'

def construct(s):
    q,z=s[PACK],s[SELECT]
    return {'qualification': {'date': z['qualification_date'], 'East_order': copy.deepcopy(z['East_order']), 'CHI_seed':6,'PHI_seed':3,
            'selected_admitted_setting':True,'model_derived_82_wins':False,'whole_regular_season_executed':False},
        'contract_and_cost_family':copy.deepcopy(q['recommended_series_source_inputs']),
        'selected_registration':copy.deepcopy(z['registration_and_availability']),
        'selected_series_period':copy.deepcopy(z['selected_series_period']),
        'reference_capacity':copy.deepcopy(q['capacity_proposal']),
        'selected_observations':copy.deepcopy(z['selected_observations']),
        'bench_and_veteran_costs':copy.deepcopy(q['S3_cost_observation_proposal']['bench_and_veteran_costs']),
        'execution':{'admitted_qualification_setting_selected':True,'lawful_piecewise_service_notice_family_selected':True,
            'new_13_active_nomination_selected_as_fiction':True,'two_cost_observations_executed_as_fiction':True,
            'series_winner':None,'full_game_scores':None,'first_option_efficiency_certified':False,
            'whole_regular_season_executed':False,'whole_A10_complete':False,'actual_private_or_clinical_certification':False},
        'remaining_whole_A10_minimum_ports':copy.deepcopy(q['remaining_whole_A10_minimum_ports'])}

def assert_payload(p,s):
    q,z=s[PACK],s[SELECT]
    a=p['qualification']
    assert a=={'date':'2025-04-13','East_order':q['qualification_port']['A_candidate_full_East_order'],'CHI_seed':6,'PHI_seed':3,
        'selected_admitted_setting':True,'model_derived_82_wins':False,'whole_regular_season_executed':False}, 'Returned setting/rank scope altered'
    assert p['contract_and_cost_family']==q['recommended_series_source_inputs'], 'Returned service/price/Gamma/unknown cost family altered'
    assert p['selected_registration']==q['proposed_registration_and_availability'], 'Returned registration/availability altered'
    assert p['selected_series_period']==q['recommended_series_source_inputs']['period']
    assert p['reference_capacity']==q['capacity_proposal'], 'Returned source chronology/positions altered'
    totals={t:{} for t in ['CHI','PHI']}; pos={t:{k:0 for k in ['PG','SG','SF','PF','C']} for t in totals}
    for t in totals:
        r=p['selected_registration'][t]
        assert len(set(r['standard']))==15 and r['TW']==[] and len(set(r['active']))==13 and len(set(r['inactive']))==2
        assert set(r['active']).isdisjoint(r['inactive']) and set(r['active'])|set(r['inactive'])==set(r['standard'])
    assert not set(p['selected_registration']['CHI']['standard']) & set(p['selected_registration']['PHI']['standard'])
    last=0
    for b in p['reference_capacity']['paired_segments']:
        start,end=b['start_second'],b['end_second'];assert start==last and end>start and start//720==(end-1)//720
        assert b['quarter']==start//720+1;last=end
        for t in totals:
            names=b[t+'_positions'];assert set(names)==set(pos[t]) and len(set(names.values()))==5
            assert set(names.values())<=set(p['selected_registration'][t]['active'])
            for k,n in names.items():pos[t][k]+=end-start;totals[t][n]=totals[t].get(n,0)+end-start
    assert last==2880
    for t in totals:
        assert set(pos[t].values())=={2880} and sum(totals[t].values())==14400
        assert {k:v//60 for k,v in totals[t].items()}==q['capacity_proposal'][t+'_minutes']
    assert p['selected_observations']==z['selected_observations'], 'Returned selected observation altered'
    assert len(p['selected_observations'])==2
    first=q['S3_cost_observation_proposal']['first_trial']
    for i,o in enumerate(p['selected_observations']):
        source=q['S3_cost_observation_proposal'][['first_trial','correction_trial'][i]]
        for k in ['game','date','start_second','end_second','candidate_observation','team_player_seconds_each']:
            assert o[k]==source[k], 'Returned new-series observation identity/meaning altered'
        assert (o['game'],o['date'])==[('QUAL1_A_G1','2025-04-19'),('QUAL1_A_G2','2025-04-21')][i]
        assert (o['start_second'],o['end_second'])==(1680,1688)
        assert o['selected'] is True and o['own_Duarte_read_and_visible_Thybulle_cutter_required'] is True
        assert o['shot_score_stop_or_individual_efficiency'] is None
        for t in totals:
            assert o[t+'_positions']==first[t+'_positions']
            assert len(set(p['selected_registration'][t]['active'])-set(o[t+'_positions'].values()))==8
        assert any(b['start_second']<=1680<1688<=b['end_second'] and all(b[t+'_positions']==o[t+'_positions'] for t in totals)
                   for b in q['capacity_proposal']['paired_segments'])
        assert len(set(o['CHI_positions'].values())|set(o['PHI_positions'].values()))==10
        assert o['team_player_seconds_each']==(1688-1680)*5==40
    assert p['bench_and_veteran_costs']==q['S3_cost_observation_proposal']['bench_and_veteran_costs']
    assert p['remaining_whole_A10_minimum_ports']==q['remaining_whole_A10_minimum_ports']
    assert p['execution']=={'admitted_qualification_setting_selected':True,'lawful_piecewise_service_notice_family_selected':True,
        'new_13_active_nomination_selected_as_fiction':True,'two_cost_observations_executed_as_fiction':True,
        'series_winner':None,'full_game_scores':None,'first_option_efficiency_certified':False,
        'whole_regular_season_executed':False,'whole_A10_complete':False,'actual_private_or_clinical_certification':False}

def build():
    s=source_inputs();assert_inputs(s);p=construct(s)
    assert_inputs(s)  # Catch constructor contamination of the source alias before saving.
    assert_payload(p,physical())
    p.update(id='A10_QUAL1_SELECTED_COST_WINDOW', status='SELECTED_ADMITTED_QUALIFICATION_AND_TWO_COST_OBSERVATIONS_NOT_SERIES_RESULT',
        source_sha256={**PINS,SELF:sha(SELF)}, baseline_main='1e02e5458f7d6191fbeeae5eeaf526cacde866d5',
        independent_consumer_review_completed=False,project_progress=[{'group':i,'status':'COMPLETE' if i<=3 else 'INCOMPLETE'} for i in range(1,8)],
        unfinished_major_groups=4,unfinished_through_group6=3,freeze='v0.30 PARTIAL',design_gate='CLOSED',Pack_count=0,manuscript_count=0)
    return p

def validate(p):
    try:
        s=physical();assert_inputs(s);assert_payload(p,s);assert p==build(),'Saved output stale'
        return []
    except (AssertionError,KeyError,ValueError,FileNotFoundError) as e:return [str(e)]

def markdown(p):
    return '''# A10 QUAL1 — 선택된 자격 setting과 두 비용 관측

CHI6/PHI3 및 동부15팀 순서는 root가 위임 범위에서 선택한 admitted setting이다. 승수는 null이며 82경기 계산·실제 NBA 순위 인증이 아니다. PHI 동일소유의 live/expiry/service/notice 법적 함수와 여섯 비용 범주, 원 Γ 및 미가격 null을 보존한다. 일반 apron은 VII2(e)(1), 마지막 정규경기 시작 후 신규 UPC 제한은 VII5(e)(2)다. 보도 표시 floor126,529,000과 법식126,529,200을 분리하여 충분조건과 차액에 후자를 쓴다.

2025-04-19/04-21 서로 다른 가상 G1/G2의 Q3 1680–1688초에서 각팀40선수초의 공동 비용 관측을 선택했다. P의 이른 도움만으로 Duarte 행동을 보장하지 않는다. Duarte own read와 가시적인 Thybulle cutter 조건이 함께 필요하다. 두 팀 등록15STD0TW, 새13active/2inactive, court5+bench8이며 원24구간48/240분 reference를 직접 대조한다. 0분 reserve는 임상 결장이 아니다.

새 관측은 자신의 공격 뒤 동료가 떠맡는 연결 노동과 다음 준비의 제한적 수정이다. 득점·수비 성공·개인 효율·시리즈 승자·우승/MVP·전체2024–25·wholeA10을 인증하지 않는다. 관측 창 밖 사건도 만들지 않는다. source 준비 false는 생성 당시 이력이고 현재 선택 범위는 별도 root canon에서만 온다. before-write caller는 물리 원입력과 반환 객체를 독립 대조한다. writer 음성은 독립 리뷰로 세지 않는다.

|큰묶음|상태|
|---|---|
|1|COMPLETE|
|2|COMPLETE|
|3|COMPLETE|
|4|INCOMPLETE|
|5|INCOMPLETE|
|6|INCOMPLETE|
|7|INCOMPLETE|

미완료4개/6번까지3개. v0.30 PARTIAL·CLOSED·Pack0·원고0.
'''

def self_test():
    original=construct;count=0
    def alias(s):
        p=original(s);s[PACK]['recommended_series_source_inputs']['NPC_q_cash_bonus_and_residual_upper']=0
        p['contract_and_cost_family']['NPC_q_cash_bonus_and_residual_upper']=0;return p
    def role(s):
        p=original(s);x=p['reference_capacity']['paired_segments'][0]['PHI_positions'];x['PG'],x['SG']=x['SG'],x['PG'];return p
    def score(s):
        p=original(s);p['selected_observations'][1]['shot_score_stop_or_individual_efficiency']=2;return p
    for f in [alias,role,score]:
        with patch(__name__+'.construct',f):
            try:build()
            except AssertionError:count+=1
            else:raise AssertionError('Writer returned mutation accepted: '+f.__name__)
    return count

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args()
    p=build();assert not validate(p)
    if a.write:
        (ROOT/OUT).write_text(serial(p),encoding='utf-8');(ROOT/OUT).with_suffix('.md').write_text(markdown(p),encoding='utf-8')
    if a.check:
        saved=json.loads(text(OUT));assert not validate(saved);assert text(str(Path(OUT).with_suffix('.md')))==markdown(p)
    n=self_test() if a.self_test else None
    print(serial({'current':True,'selected_observations':2,'admitted_qualification_setting':True,'writer_returned_negative_controls':n,'series_winner':None,'whole_A10':False}))
if __name__=='__main__':main()
