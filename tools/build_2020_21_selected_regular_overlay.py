"""Apply approved full-team minute overlays and recompute one BPM season.

Source minute vectors are preserved; source rounding gaps remain disclosed.
Positive-minute availability is an explicit author working model. Available
lineup witnesses do not define complete substitution chronology.
"""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import date
import hashlib
import json
from pathlib import Path

import collect_2020_21_single_policy_base_inputs as base_check
import build_chicago_2020_21_availability_policy as policy
import build_cleveland_c2_complete_working_minutes as c2_check
import audit_2020_21_selected_margin_join as margin_join

ROOT = Path(__file__).resolve().parents[1]
BASE = 'simulation/NBA_2020_21_K1_BASE_INPUT_JOIN.json'
J1 = 'simulation/CHICAGO_2020_21_POLICY_REPLACEMENT_MINUTES.json'
F4 = 'simulation/ORLANDO_2020_21_HALL_FIVE_GAME_LOAD_SCREEN.json'
F5 = 'simulation/DENVER_2020_21_MCGEE_NONTRADE_SCREEN.json'
C2 = 'simulation/CLEVELAND_2020_21_C2_COMPLETE_WORKING_MINUTES.json'
OLD = 'simulation/NBA_2020_21_FINAL859_MINUTES.json'
AUTHORITY = 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json'
BPM = 'simulation/CHICAGO_2020_21_BPM_MAR25_SNAPSHOT.csv'
OUT = 'simulation/NBA_2020_21_SELECTED_REGULAR_OVERLAY.json'
MD = 'simulation/NBA_2020_21_SELECTED_REGULAR_OVERLAY.md'
METHOD = 'BPM_MAR25_EB'
SOURCES = [BASE,J1,F4,F5,C2,OLD,AUTHORITY,BPM,
    'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json',
    'canon/CLEVELAND_2021_VAREJAO_C2_DECISION.json',
    'simulation/CHICAGO_2020_21_AVAILABILITY_POLICY.json',
    'tools/audit_2020_21_selected_margin_join.py',
    'tools/collect_2020_21_single_policy_base_inputs.py',
    'tools/build_2020_21_selected_regular_overlay.py']


def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))


def sha(path):
    value=(ROOT/path).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
    return hashlib.sha256(value.encode()).hexdigest()


def direction(band):
    return 'HOME' if band[0]>0 else 'AWAY' if band[1]<0 else 'UNRESOLVED'


def witness_minutes(witness):
    values=Counter()
    for stint in witness:
        if len(stint['players'])!=5 or len(set(stint['players']))!=5 or stint['seconds']<=0:
            raise ValueError('positive unique-five stint required')
        for p in stint['players']:values[p]+=stint['seconds']
    return dict(values)


def verify_witness(vector,witness,duration):
    values=witness_minutes(witness)
    positive={p:n for p,n in vector.items() if n>1e-7}
    if (set(values)!=set(positive) or any(abs(values[p]-n)>=1e-5 for p,n in positive.items())
            or abs(sum(s['seconds'] for s in witness)-duration)>=1e-5):
        raise ValueError('full-vector/common-clock witness mismatch')


def verify_starters(starters,vector,witness):
    if (starters is None or len(starters)!=5 or len(set(starters))!=5
            or not set(starters)<={p for p,n in vector.items() if n>1e-7}):
        raise ValueError('explicit unique-five positive-minute working starters required')
    if sum(w['seconds'] for w in witness if set(w['players'])==set(starters))<180-1e-5:
        raise ValueError('working starting-five 180-second witness missing')


def make_overlay(gid,team,vector,witness,duration,source,removed,starters):
    if abs(sum(vector.values())-5*duration)>=1e-5 or max(vector.values())>duration+1e-5:
        raise ValueError('overlay clock or player capacity')
    if set(removed)&set(vector):raise ValueError('superseded player in overlay vector')
    verify_witness(vector,witness,duration)
    verify_starters(starters,vector,witness)
    return dict(event_id=gid,team=team,player_seconds=vector,lineup_witness=witness,
        game_duration_seconds=duration,source=source,removed_players=removed,
        starters=starters,starters_classification='EXPLICIT_AUTHOR_WORKING_STARTING_FIVE_NOT_OBSERVED_ALTERNATE_LINEUP')


def authority_rules(authority,followups,c2_direction):
    if (authority['authority_type']!='AUTHOR_DELEGATED_SELECTION' or
            authority['selected']['regular_season']['route']!=
            'K1_BPM_F038_WITH_APPROVED_F4_F5_C2_OVERRIDES'):
        raise ValueError('existing delegation and exact selected K1 route required')
    expected={
        'F4_HALL':'Orlando does not re-sign Donta Hall on 2021-05-09; his April contracts and earlier appearances remain in the alternate ledger.',
        'F5_MCGEE':'Denver and Cleveland do not execute their 2021-03-25 JaVale McGee/Isaiah Hartenstein and two-second-round-pick trade; McGee remains with Cleveland and Hartenstein with Denver.'}
    if followups['selected']!=expected:
        raise ValueError('exact approved F4/F5 omission directions required')
    if c2_direction['selected']['route']!='C2_VAREJAO_NO_RETURN_SIGNING':
        raise ValueError('approved C2 omission route required')


def complete_f5_source_branches(base_rows, overlays):
    """Cover omitted-trade donors outside the old FINAL859-only screen.

    Four selected E/CHI_POST vectors still carried the historical trade.
    Keep their complete vectors, starters and clock; substitute only the
    retained counterpart under the already delegated minute model.
    """
    from build_2020_21_regular_clock_completion import construct_witness
    missing={}
    for row in base_rows:
        if row['date']<'2021-03-25' or row['team'] not in ('DEN','CLE'):continue
        key=row['event_id'],row['team']
        current=overlays.get(key,row)
        donor,receiver=('JaVale McGee','Isaiah Hartenstein') if row['team']=='DEN' else ('Isaiah Hartenstein','JaVale McGee')
        if current['player_seconds'].get(donor,0)<=1e-7:continue
        if key in overlays:raise ValueError('existing full overlay contradicts F5 omission')
        vector=deepcopy(row['player_seconds']);seconds=vector.pop(donor)
        if receiver in vector or donor in row['starters']:
            raise ValueError('F5 uncovered branch requires separate full-vector/start selection')
        vector[receiver]=seconds
        duration=row['game_duration_seconds'];starters=row['starters']
        residual={p:n-(180 if p in starters else 0) for p,n in vector.items()}
        if min(residual.values())<0:raise ValueError('F5 source starters lack starting-clock capacity')
        witness=[dict(players=list(starters),seconds=180)]+construct_witness(residual,duration-180)
        item=make_overlay(row['event_id'],row['team'],vector,witness,duration,
            dict(path=BASE,operation='F5_RETAINED_COUNTERPART_UNCOVERED_SOURCE_BRANCH',
                 original_branch_source=deepcopy(row['source'])),[donor],starters)
        item['f5_scope_completion']=dict(original_donor=donor,retained_counterpart=receiver,seconds=seconds,
            original_full_vector=row['player_seconds'],classification='AUTHOR_DELEGATED_WORKING_MODEL_NOT_MEDICAL_PROOF')
        item['overlay_stage']='F5_SCOPE_COMPLETION';missing[key]=item
    expected={('2021-04-09_DEN_SAS','DEN'),('2021-04-28_DEN_NOP','DEN'),
              ('2021-04-17_CHI_CLE','CLE'),('2021-04-21_CLE_CHI','CLE')}
    if set(missing)!=expected:raise ValueError('F5 uncovered source-branch domain changed; review named branches')
    return missing


def build():
    base=read(BASE);base_check.validate_against_sources(base)
    if base['source_sha256']!={p:sha(p) for p in base['source_sha256']}:
        raise ValueError('stale base source bridge')
    authority=read(AUTHORITY)
    authority_rules(authority,read('canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json'),
                    read('canon/CLEVELAND_2021_VAREJAO_C2_DECISION.json'))
    source_rows={(b['event_id'],b['team'],b['profile']):b for b in read(OLD)['branches']
                 if b.get('rival_minutes') in (None,28)}
    overlays={};history=[]
    def add(row,stage,replace=False):
        key=row['event_id'],row['team']
        if key in overlays and not replace:raise ValueError('same team resource overlaid twice')
        if replace and (key not in overlays or stage!='C2' or overlays[key]['overlay_stage']!='F5'):
            raise ValueError('only the two C2/F5 complete replacements allowed')
        if replace:history.append(dict(event_id=key[0],team=key[1],replaced='F5',replacement='C2'))
        overlays[key]=dict(**row,overlay_stage=stage)
    jrows=[x['variant'] for x in read(J1)['records']
           if x['policy']=='J1_TERRY_LEAVE' and x['variant']['profile']=='LOW_MINUTES']
    if len(jrows)!=27:raise ValueError('J1 twenty-seven full vectors required')
    for b in jrows:
        add(make_overlay(b['event_id'],b['team'],b['alternate_seconds'],b['lineup_witness'],
            b['game_duration_seconds'],dict(path=J1,policy='J1_TERRY_LEAVE',profile='LOW_MINUTES'),
            b['removed_players'],b['starters']),'J1')
    for b in read(F4)['rows']:
        source=source_rows[b['event_id'],'ORL','LOW_MINUTES']
        add(make_overlay(b['event_id'],'ORL',b['candidate_minutes'],b['lineup_witness'],
            source['game_duration_seconds'],dict(path=F4,selection='AUTHOR_DELEGATED_FIVE_GAME_LOAD_WORKING_PLAN'),
            ['Donta Hall'],source['starters']),'F4')
    for b in read(F5)['rows']:
        profile='LOW_MINUTES' if b['team']=='DEN' else 'OBSERVED_HELD'
        source=source_rows[b['event_id'],b['team'],profile]
        vector=deepcopy(source['alternate_seconds'])
        if vector.pop(b['removed'])!=b['seconds'] or b['added'] in vector:
            raise ValueError('F5 original named donor/matching seconds mismatch')
        vector[b['added']]=b['seconds']
        if b['team']=='CLE':witness=b['candidate_lineup_witness']
        else:
            witness=[dict(players=[b['added'] if p==b['removed'] else p for p in s['players']],
                          seconds=s['seconds']) for s in source['lineup_witness']]
        add(make_overlay(b['event_id'],b['team'],vector,witness,source['game_duration_seconds'],
            dict(path=F5,source_profile=profile),[b['removed']],b['candidate_starters']),'F5')
    c2=read(C2);c2_check.validate(c2)
    for b in c2['rows']:
        add(make_overlay(b['event_id'],'CLE',b['alternate_seconds'],b['lineup_witness'],
            b['game_duration_seconds'],dict(path=C2,operation=b['overlay_operation']),b['removed_players'],b['starters']),
            'C2',replace=b['prior_f5_same_team_override_replaced'])
    completion=complete_f5_source_branches(base['team_games'],overlays)
    overlays.update(completion)
    if len(overlays)!=64 or len({e for e,t in overlays})!=62 or len(history)!=2:
        raise ValueError('64-team/62-game/2-complete-replacement coverage')
    team_rows=deepcopy(base['team_games']);baseline={(b['event_id'],b['team']):b for b in base['team_games']}
    if not set(overlays)<=set(baseline):raise ValueError('overlay outside single-policy base')
    for row in team_rows:
        key=row['event_id'],row['team'];replacement=overlays.get(key)
        if replacement:
            if row['game_duration_seconds']!=replacement['game_duration_seconds']:
                raise ValueError('source duration changed silently')
            row.update(deepcopy(replacement))
            row.update(raw_total_seconds=sum(row['player_seconds'].values()),
                required_total_seconds=5*row['game_duration_seconds'],
                normalization_delta_seconds=0,normalization_applied=False,
                solver_float_residual_seconds=5*row['game_duration_seconds']-sum(row['player_seconds'].values()),
                clock_status='EXACT_AUTHOR_WORKING_OVERLAY',overlay_applied=True)
        else:row['overlay_applied']=False
        row['modeled_available']=sorted(p for p,n in row['player_seconds'].items() if n>1e-7)
        row['zero_player_health']={p:None for p,n in row['player_seconds'].items() if n<=1e-7}
        row['zero_player_reason']='UNSELECTED_SOURCE_ZERO_NOT_ABSENCE_OR_REGISTRATION_PROOF'
        row['availability_classification']='AUTHOR_DELEGATED_POSITIVE_MINUTE_WORKING_MODEL'
        row.update(actual_active_list_certified=False,medical_certified=False,legal_registration_cleared=False)
    final={(b['event_id'],b['team']):b for b in team_rows}
    # The margin join contains J1 already. Add only the 37 other complete-team
    # changes, measured from the un-overlaid base vector, once per team.
    margins=margin_join.build();margin_rows={x['event_id']:x for x in margins['rows']}
    if len(margin_rows)!=1080:raise ValueError('complete single BPM margin input required')
    bpm_rows=policy.cc.read(ROOT/BPM)
    ratings={policy.cc.paired.norm(r['nba_player']):float(r['bpm'])*int(r['archive_minutes'])/
             (int(r['archive_minutes'])+1000) for r in bpm_rows}
    values=[ratings[policy.cc.paired.norm(r['nba_player'])] for r in bpm_rows if int(r['archive_minutes'])>=120]
    envelope=dict(low=min(values),high=max(values),observed_players=len(values),
        status='EMPIRICAL_LEAGUE_RANGE_STRESS_NOT_PLAYER_PRIOR_OR_HARD_BOUND')
    rival=read('simulation/CHICAGO_2020_21_AUTHOR_PACKET.json')['rival_candidates'][0]['methods'][METHOD]['effective_rating']
    games_by_id={g['event_id']:g for g in base['regular_season_games']}
    dates=defaultdict(list)
    for g in games_by_id.values():
        for t in (g['home'],g['away']):dates[t].append(g['date'])
    b2b={(t,d):i>0 and (date.fromisoformat(d)-date.fromisoformat(ds[i-1])).days==1
         for t,days in dates.items() for ds in [sorted(days)] for i,d in enumerate(ds)}
    extra_by_game=defaultdict(list)
    completion_branches=policy.load()[2]
    for key,overlay in sorted(overlays.items()):
        if overlay['overlay_stage']=='J1':continue
        gid,team=key;old=baseline[key]['player_seconds'];new=final[key]['player_seconds']
        change={p:new.get(p,0)-old.get(p,0) for p in sorted(set(new)|set(old))
                if abs(new.get(p,0)-old.get(p,0))>1e-7}
        effect,terms=policy.cc.form(change,ratings,{})
        source_profile='OBSERVED_HELD' if team=='CLE' else 'LOW_MINUTES'
        if key in completion:
            branch=completion_branches[gid,team,'LOW_MINUTES']
            if branch['alternate_seconds']!=old:raise ValueError('F5 completion base differs from actual source branch')
            actual=branch['actual_seconds']
        else:actual=source_rows[gid,team,source_profile]['actual_seconds']
        old_delta={p:old.get(p,0)-actual.get(p,0) for p in set(old)|set(actual)}
        new_delta={p:new.get(p,0)-actual.get(p,0) for p in set(new)|set(actual)}
        incremental_penalty=(.5*(sum(max(0,n) for n in new_delta.values())-
            sum(max(0,n) for n in old_delta.values()))/2880 if b2b[team,games_by_id[gid]['date']] else 0.0)
        # Match the retained upstream policy: CHI postdeadline impacts charge
        # CHI workload only. No non-CHI fatigue is appended in those games.
        fatigue_enabled='CHI' not in (games_by_id[gid]['home'],games_by_id[gid]['away'])
        if not fatigue_enabled:incremental_penalty=0.0
        sign=1 if games_by_id[gid]['home']==team else -1
        extra_by_game[gid].append(dict(team=team,overlay_stage=overlay['overlay_stage'],
            moved_seconds=change,effect=effect,unknown_terms=terms,home_sign=sign,
            incremental_workload_penalty=incremental_penalty,b2b=b2b[team,games_by_id[gid]['date']],
            fatigue_enabled=fatigue_enabled,fatigue_scope='BOTH_TEAMS_B2B' if fatigue_enabled else 'UPSTREAM_CHI_ONLY'))
    if sum(map(len,extra_by_game.values()))!=37:raise ValueError('J1 excluded from 37 additional team shocks')
    games=[];joint=[]
    for original in base['regular_season_games']:
        gid=original['event_id'];source=margin_rows[gid];constant=source['home_margin_constant']
        terms=deepcopy(source['unknown_coefficients'])
        for extra in extra_by_game[gid]:
            sign=extra['home_sign'];constant+=sign*(extra['effect']-extra['incremental_workload_penalty'])
            for p,n in extra['unknown_terms'].items():terms[p]=terms.get(p,0)+sign*n
        terms={p:n for p,n in terms.items() if abs(n)>1e-9}
        rival_name=policy.f.e.RIVAL
        band=policy.cc.band(constant+terms.get(rival_name,0)*rival,
            {p:n for p,n in terms.items() if p!=rival_name},envelope)
        selected=direction(band)
        winner=original['home'] if selected=='HOME' else original['away'] if selected=='AWAY' else None
        row=deepcopy(original)
        row.update(winner=winner,initial_k1_winner=original['winner'],method=METHOD,
            home_margin_constant=constant,unknown_coefficients=terms,home_margin_band=band,
            j1_applied=source['j1_applied'],non_j1_team_effects=extra_by_game[gid],
            direction=selected,winner_recomputed=True,winner_changed_from_initial=winner!=original['winner'],
            score_model=None,actual_box=None,actual_result_certified=False)
        games.append(row)
        if gid in ('2021-04-14_CHA_CLE','2021-04-23_CHA_CLE'):
            if not source['j1_applied'] or len(extra_by_game[gid])!=1 or extra_by_game[gid][0]['team']!='CLE':
                raise ValueError('CHA/CLE joint input missing either team')
            if winner!=('CLE' if gid.startswith('2021-04-14') else 'CHA'):
                raise ValueError('joint CHA/CLE selected direction changed; requires review')
            joint.append(dict(event_id=gid,j1_cha_home_constant=source['home_margin_constant'],
                cle_extra_effect=extra_by_game[gid][0],joint_home_margin_band=band,winner=winner,
                both_team_full_overlays_present=all((gid,t) in overlays for t in ('CHA','CLE'))))
    unresolved=[g['event_id'] for g in games if g['winner'] is None]
    changes=[g['event_id'] for g in games if g['winner_changed_from_initial']]
    wins=Counter(g['winner'] for g in games if g['winner'] is not None)
    return dict(status='SINGLE_BPM_1080_RESULTS_AND_2160_TEAM_MINUTE_OVERLAY_ROOT_REVIEW_PENDING',
        baseline_main='94a672bd',date_local='2026-10-07',authority=AUTHORITY,
        source_sha256={p:sha(p) for p in SOURCES},margin_join_source_sha256=margins['source_sha256'],
        source_hash_convention='SHA256_UTF8_BOM_STRIPPED_CRLF_OR_CR_TO_LF_BYTES',
        policy={**base['policy'],'base_join_overlay_applied':True},method=METHOD,raptor_mixed=False,
        f4_selected_working_source=F4,f4_selection_classification='AUTHOR_DELEGATED_WORKING_HEALTH_COACH_MODEL',
        base_player_sources_preserved=True,team_games=team_rows,regular_season_games=games,
        overlay_sources={stage:path for stage,path in [('J1',J1),('F4',F4),('F5',F5),('C2',C2)]},
        complete_replacement_history=history,source_clock_gaps_retained=[dict(event_id=r['event_id'],
            team=r['team'],gap_seconds=r['normalization_delta_seconds']) for r in team_rows if r['normalization_delta_seconds']],
        additional_team_effects=37,joint_cha_cle_checks=joint,overlay_team_games=64,overlay_games=62,
        f5_source_branch_completions=[dict(event_id=e,team=t,**b['f5_scope_completion']) for (e,t),b in sorted(completion.items())],
        full_recomputed_regular_games=1080,total_team_games=2160,
        unresolved_games=unresolved,changed_winner_games=changes,recomputed_team_wins=dict(sorted(wins.items())),
        fatigue_policy='RETAINED_0_5_B2B_POSITIVE_DELTA_EXPOSURE_WITH_UPSTREAM_CHI_ONLY_SCOPE',
        rating_envelope=envelope,rival_rating=rival,
        scope='Single selected BPM execution of approved minute directions; empirical stress bands are not observed scores.',
        no_roster_medical_inference_from_zero=True,full_roster_registration_complete=False,
        actual_active_lists_certified=False,medical_certified=False,whole_health_complete=False,
        legal_execution_cleared=False,season_selected=False,manuscript_allowed=False)


def validate(packet,expected=None):
    if packet['source_sha256']!={p:sha(p) for p in SOURCES}:raise ValueError('stale overlay sources')
    if packet!=(build() if expected is None else expected):
        raise ValueError('selected overlay differs from source-linked complete reconstruction')
    keys={(r['event_id'],r['team']) for r in packet['team_games']}
    if len(keys)!=2160 or len(packet['team_games'])!=2160:raise ValueError('duplicate team resource')
    for row in packet['team_games']:
        if row['overlay_applied']:
            verify_witness(row['player_seconds'],row['lineup_witness'],row['game_duration_seconds'])
            verify_starters(row['starters'],row['player_seconds'],row['lineup_witness'])


def negative_tests(packet):
    ix=next(i for i,r in enumerate(packet['team_games']) if r.get('overlay_stage')=='C2')
    changes=[lambda p:p['team_games'][ix]['player_seconds'].__setitem__('JaVale McGee',1937),
        lambda p:p['team_games'][ix]['player_seconds'].__setitem__('Anderson Varejao',397),
        lambda p:p['team_games'][ix]['player_seconds'].__setitem__('Isaiah Hartenstein',770),
        lambda p:p['team_games'][ix]['starters'].__setitem__(0,'Isaiah Hartenstein'),
        lambda p:p['team_games'].append(deepcopy(p['team_games'][ix])),
        lambda p:p['joint_cha_cle_checks'][0].__setitem__('both_team_full_overlays_present',False),
        lambda p:p['regular_season_games'][0].__setitem__('winner','INVALID'),
        lambda p:p['source_sha256'].__setitem__(F4,'stale'),
        lambda p:p.__setitem__('authority','invented-authority'),
        lambda p:p.__setitem__('medical_certified',True),lambda p:p.__setitem__('season_selected',True)]
    for change in changes:
        candidate=deepcopy(packet);change(candidate)
        try:validate(candidate,expected=packet)
        except ValueError:continue
        raise AssertionError('invalid selected regular overlay accepted')
    # Source direction changes must not be legitimized merely by recomputing
    # hashes. These memory-only tests do not change any canon file.
    source_controls=[read(AUTHORITY),read('canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json'),
                     read('canon/CLEVELAND_2021_VAREJAO_C2_DECISION.json')]
    source_changes=[lambda a:a[0]['selected']['regular_season'].__setitem__('route','OTHER'),
        lambda a:a[1]['selected'].__setitem__('F4_HALL','SIGN_HALL'),
        lambda a:a[1]['selected'].__setitem__('F5_MCGEE','EXECUTE_TRADE'),
        lambda a:a[2]['selected'].__setitem__('route','C1_RETURN')]
    for change in source_changes:
        changed=deepcopy(source_controls);change(changed)
        try:authority_rules(*changed)
        except ValueError:continue
        raise AssertionError('changed source direction accepted as selected K1')
    changed_base=read(BASE)
    vector=changed_base['team_games'][0]['player_seconds']
    names=[p for p,n in vector.items() if n>0]
    vector[names[0]]+=1;vector[names[1]]-=1
    # This conserves the team sum but must fail the independent source join.
    base_check.validate(changed_base)
    try:base_check.validate_against_sources(changed_base)
    except (ValueError,AssertionError):pass
    else:raise AssertionError('equal-total source base minute redistribution accepted')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true')
    args=ap.parse_args();packet=build();validate(packet,expected=packet)
    if args.check:
        if read(OUT)!=packet:raise ValueError('saved overlay stale')
    else:(ROOT/OUT).write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.self_test:negative_tests(packet)
    print(json.dumps({k:packet[k] for k in ['overlay_team_games','overlay_games','full_recomputed_regular_games','total_team_games','unresolved_games','changed_winner_games']},ensure_ascii=False))
