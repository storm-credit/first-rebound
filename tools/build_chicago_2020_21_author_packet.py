"""G: auditable author candidates from existing full-season results, not new canon.
Choose role/benchmark construction before looking up standings. No new game sim.
"""
import json
import statistics
import argparse
from pathlib import Path
from collections import Counter,defaultdict
import build_nba_2020_21_full_season as f

OUT=f.S/'CHICAGO_2020_21_AUTHOR_PACKET.json'
TOP_CREATORS=['LaMelo Ball','Tyrese Haliburton','Immanuel Quickley']
BROAD_CREATORS=TOP_CREATORS+['Anthony Edwards','Cole Anthony','Killian Hayes']
PROFILES=[
 {'id':'R1','name':'기본 적응형','minutes':28,'players':TOP_CREATORS,'aggregation':'median','recommended':True,
  'meaning':'상위 동기 창조자 비교선, 득점·감속·선제 패스는 강점이나 팀 전체 구원은 선지급하지 않음'},
 {'id':'R2','name':'완만한 적응형','minutes':24,'players':BROAD_CREATORS,'aggregation':'median','recommended':False,
  'meaning':'더 넓은 동기 비교선과 제한된 역할; 재활 이력만으로 부상·능력 저하를 확정한 것은 아님'},
 {'id':'R3','name':'신인 상단형','minutes':32,'players':TOP_CREATORS,'aggregation':'max','recommended':False,
  'meaning':'상위 동기 계수 상단과 높은 부하; 지표별 상단 선수가 다르므로 특정 선수 복제가 아님'},
 {'id':'R4','name':'즉시 스타 스트레스','minutes':32,'players':['Luka Doncic'],'aggregation':'median','recommended':False,
  'meaning':'2020–21의3년차 스타를 쓰는 의도적 과상향 반례; 신인 비교표본으로 사용 금지'}]


def build():
    source=json.loads(f.OUT.read_text());maps=f.rating_maps()
    refs={p:{m:maps[m][f.bi.cc.paired.norm(p)] for m in f.bi.METHODS}
          for p in sorted(set(BROAD_CREATORS+['Luka Doncic']))}
    candidates=[]
    for profile in PROFILES:
        candidate={**profile,'selected':False,'methods':{}}
        for method in f.bi.METHODS:
            values=[refs[p][method] for p in profile['players']]
            rating=max(values) if profile['aggregation']=='max' else statistics.median(values)
            rows=[(i,r) for i,r in enumerate(source['season_bridge'])
                  if r['source_condition']['path_id']==f"LOW_MINUTES/RIVAL_{profile['minutes']}/FOURNIER_PATH_RETAINED"
                  and r['source_condition']['method']==method and r['source_condition']['fatigue']==.5]
            matches=[(i,r) for i,r in rows if r['shared_rival_rating_open_interval'][0]<rating<r['shared_rival_rating_open_interval'][1]]
            assert len(matches)==2 and {r['source_condition']['availability'] for i,r in matches}=={'PORTER_ZERO','PORTER_CAPPED'}
            ids={c['id'] for c in source['league_cases'] if any(i in c['bridge_indices'] for i,r in matches)}
            assert len(ids)==1
            case=next(c for c in source['league_cases'] if c['id'] in ids)
            neighborhood=[(i,r) for i,r in rows if max(rating-.5,r['shared_rival_rating_open_interval'][0])<min(rating+.5,r['shared_rival_rating_open_interval'][1])]
            nearcases={c['id'] for c in source['league_cases'] if any(i in c['bridge_indices'] for i,r in neighborhood)}
            candidate['methods'][method]={
                'effective_rating':rating,'bridge_indices':[i for i,r in matches],'case_id':case['id'],
                'chicago_record':[case['team_wins']['CHI'],72-case['team_wins']['CHI']],
                'chicago_seed':case['seeds']['EAST'].index('CHI')+1,
                'minnesota_record':[case['team_wins']['MIN'],72-case['team_wins']['MIN']],
                'minnesota_seed':case['seeds']['WEST'].index('MIN')+1,
                'first_playin_pairings':case['chicago_first_playin_pairings'],
                'full_seeds':case['seeds'],'team_wins':case['team_wins'],
                'changed_game_ids':case['changed_game_ids'],
                'chicago_record_position_ranges':case['chicago_record_position_ranges'],
                'both_porter_conditions_same_game_ids':True,
                'plus_minus_half_point_stress':{
                    'rating_interval':[rating-.5,rating+.5],'case_ids':sorted(nearcases),
                    'chicago_wins':sorted({r['team_wins']['CHI'] for i,r in neighborhood}),
                    'minnesota_wins':sorted({r['team_wins']['MIN'] for i,r in neighborhood}),
                    'scope':'Local parameter sensitivity, not a confidence interval or an approved player prior'}}
        candidates.append(candidate)
    # All existing conditional new-team targets across the actual schedule.
    # This is an assumption calendar, not proof of health/registration or exact GP.
    availability=defaultdict(list)
    schedule=f.bi.lb.normalized_games()
    for g in schedule:
        for team in (g['home'],g['away']):
            _,targets,*_=f.e.policy(team,g['date'],False,28)
            for player,minutes in targets.items():availability[team,player].append(g['id'])
    exposure=[{'team':team,'player':player,'target_game_count':len(ids),'event_ids':sorted(ids),
               'meaning':'Conditional target-date availability, not observed GP or author-approved health'}
              for (team,player),ids in sorted(availability.items())]
    rec=candidates[0];primary=rec['methods']['BPM_MAR25_EB'];cross=rec['methods']['RAPTOR_RS_EB']
    changed=sorted(set(primary['changed_game_ids'])^set(cross['changed_game_ids']))
    scenario_events=[
        {'id':'T1','event':'Gordon/Clark to DEN for Harris/Nnaji and one protected future1R','authority':'GORDON_A_NEGOTIATION_LEAN_NOT_AUTHOR_LOCKED',
         'cost':'Nnaji acquired at24 and the separate acquisition-pick debt both remain costs; exact transfer terms/charges still HOLD'},
        {'id':'T2','event':'Vucevic stays in ORL for remainder of2020–21','authority':'WORKING_CONDITION_NOT_AUTHOR_LOCKED',
         'cost':'No Carter/Porter/Chicago1R return; Bamba/Nnaji development congestion remains'},
        {'id':'T3','event':'Fournier Boston route retained independently','authority':'WORKING_CONDITION_NOT_AUTHOR_LOCKED',
         'cost':'Boston exception/picks/registration and Orlando objective separate from Gordon'},
        {'id':'T4','event':'Powell stays TOR; Hood stays POR','authority':'WORKING_CONDITION_NOT_AUTHOR_LOCKED',
         'cost':'Portland loses actual Powell reinforcement; future contracts and asset path must follow this branch'},
        {'id':'T5','event':'Incumbent followup contracts/core structures retained conditionally','authority':'EX04_EX06_HOLD',
         'cost':'Hall/Wagner/Parker and other registrations require causal justification, not automatic actual-history copying'}]
    return {'stage':'O-15F14-G','status':'AUTHOR_PACKET_READY_NOT_SEASON_LOCK',
        'benchmark_players':refs,'rival_candidates':candidates,'recommended_rival_profile':'R1',
        'recommended_identity':{'attack':'SG/SF 창조 윙, 감속·풋워크·풀업·선제 패스로 첫 이점 생성',
            'personality':'차분한 분석형, 강한 승부욕·통제욕; 상시 모욕/허세가 아닌 선택 책임으로 에고 표현',
            'limits':'정확 신체·수비 전성기 상한·신인 박스/수상은 미승인. POA 신체 도구를 삭제하거나 즉시 전업PG로 변경하지 않음'},
        'primary_method_proposal':'BPM_MAR25_EB','primary_method_reason':'후반 평가의 기준시점과 맞는3/25 snapshot을 임시 주판정,시즌전체 RAPTOR는 사후 교차검사. 전반에는3/25도미래정보이므로예측모델주장금지.',
        'recommended_primary_case':primary['case_id'],'crosscheck_case':cross['case_id'],
        'cross_method_changed_game_ids':changed,'scoring_results_not_locked':True,
        'transaction_scenario_events':scenario_events,'conditional_target_calendar':exposure,
        'approval_scope':{
            'creative_choices':['R1공격/성격/초기역할 방향','T1~T4 사건 방향과 대가'],
            'not_approved_by_this_choice':['정확 거래 charge·보호/이연/전환 조항','T5 후속 계약·실제 건강 사건','72경기 완전가용·개별선수초·정확박스/수상','최종시즌승패·플레이인·lottery','원고 개방']},
        'conditions':['Fixed LOW_MINUTES, BASE protagonist/LaMelo prior, fatigue0.5. No daily metric/rival-rating mixing.',
            'R1 benchmark median of three successful same-class perimeter creators; a transparent design calibration, not a validated transfer model or unseen scouting evidence.',
            'R4 explicitly uses a third-year star; prohibited from masquerading as a rookie cohort.',
            'F emergency-role costs0..3 preserve seven directions;6-point stress counterexample remains unresolved outside these baseline cases.',
            'The target calendar exposes full target-date availability assumptions. It does not approve them or treat empirical coefficient ranges as hard bounds.'],
        'upstream_sha256':{p.name:f.bi.cc.sha(p) for p in (f.OUT,f.MINUTES,f.bi.cc.BPM,f.bi.cc.paired.RAPTOR,Path(__file__))},
        'selected':False,'manuscript_allowed':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args();data=build()
    if args.write:OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    else:assert json.loads(OUT.read_text())==data
    print(json.dumps({'PASS':True,'candidates':len(data['rival_candidates']),
        'primary':data['recommended_primary_case'],'crosscheck':data['crosscheck_case'],
        'cross_method_changed_games':len(data['cross_method_changed_game_ids']),
        'availability_targets':len(data['conditional_target_calendar'])}))
