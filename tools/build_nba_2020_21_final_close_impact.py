"""O-15F14-E: remaining80 close games under the existing conditional season policies.
The previous D artifact remains immutable. Final season/transactions/health unselected.
"""
import argparse
import copy
import itertools
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
import build_nba_2020_21_policy_queue as queue

d=queue.d
bi=d.bi
S=d.S
OBS=queue.OBS
OUT=S/'NBA_2020_21_FINAL_CLOSE_PAIRED_IMPACT.json'
PENDING=S/'NBA_2020_21_AFTER_80_PENDING_QUEUE.csv'
RIVAL=d.RIVAL
ROLES=copy.deepcopy(d.ROLES)
# Conditional small-ball interior coverage, not proof of historical center stints.
# Narrow big-only roles otherwise force Reid/Davis to absorb 15-20 extra minutes.
ROLES['MIN']['center'] += ['Jarred Vanderbilt']
ROLES['DET']['handler'] += ['Derrick Rose']
ROLES['NOP']['wing'] += ['Didi Louzada','James Nunnally','Sindarius Thornwell']
ROLES['ORL']['handler'] += ['Cole Anthony']
ROLES['ORL']['center'] += ['Donta Hall','Moritz Wagner']
ROLES['ORL']['wing'] += ['Terrence Ross']


def groups():
    result=defaultdict(list)
    for r in bi.cc.read(OBS):result[r['event_id'],r['team']].append(r)
    return result


def policy(team,day,high,rival_minutes=28):
    removed,targets,donors,recipients,swaps=d.policy(team,day,high,rival_minutes)
    # Original fixed policy is extended only where newly observed active depth was absent.
    if team=='MIN':
        donors=donors+[('Jarrett Culver',12),('Jaden McDaniels',20),('Malik Beasley',28),('Jaylen Nowell',16),('Jarred Vanderbilt',12),('Ricky Rubio',24),('Malik Beasley',26)]
        recipients=recipients+[('Jarrett Culver',28),('Malik Beasley',36),('Jaylen Nowell',30)]
    if team=='DET':
        donors=donors+[('Derrick Rose',20),('Cory Joseph',20),('Hamidou Diallo',20),('Sekou Doumbouya',16),('Derrick Rose',16),('Jerami Grant',28)]
        recipients=recipients+[('Josh Jackson',32),('Wayne Ellington',30),('Cory Joseph',30)]
    if team=='DEN':
        donors=donors+[('Paul Millsap',12),('PJ Dozier',12),('Monte Morris',20),('Will Barton',22)]
    if team=='NOP':
        donors=donors+[('Sindarius Thornwell',0),('Didi Louzada',0),('James Nunnally',0),('Nickeil Alexander-Walker',6),('JJ Redick',16),('Josh Hart',20)]
        recipients=recipients+[('James Johnson',30),('Wes Iwundu',24),('Didi Louzada',16),('James Nunnally',16)]
    if team=='ORL' and day>='2021-03-25':
        # Keep the same policy at all newly examined dates; May1 WCJ starter is replaced.
        swaps={**swaps,'Wendell Carter Jr.':'Nikola Vucevic','R.J. Hampton':'Cole Anthony'}
        recipients=[('Cole Anthony',32),('Gary Harris',30),('Chuma Okeke',34),('Dwayne Bacon',36),('James Ennis III',32),('Chasson Randle',32)]
        donors=donors+[('Moritz Wagner',16),('Dwayne Bacon',24)]
    return removed,targets,donors,recipients,swaps


def specs():
    result = []
    for (gid, team), rows in sorted(groups().items()):
        day = rows[0]['date']
        try:
            base, duration, clock = bi.baseline(rows)
        except AssertionError:
            # This newly observed team has a documented three-second source residue.
            raw = {r['player']:int(r['seconds']) for r in rows if int(r['seconds'])}
            assert (gid, team, sum(raw.values())) == ('2021-02-10_PHX_MIL', 'MIL', 14403)
            base = raw.copy(); duration = 2880
            fixed = max(base, key=lambda p:(base[p],p)); base[fixed] -= 3
            clock = {'player':fixed,'seconds':-3,'raw_total_seconds':14403,
                     'reason':'SOURCE_THREE_SECOND_RESIDUAL_EXPLICIT_EXCEPTION'}
        removed, targets, *_ = policy(team, day, False)
        changed = bool(targets or set(removed) & set(base))
        profiles = bi.PROFILES if changed else ('OBSERVED_HELD',)
        for profile, rival in itertools.product(profiles, (24, 28, 32) if team == 'MIN' else (None,)):
            removed, targets, donors, recipients, swaps = policy(team, day, profile == 'HIGH_MINUTES', rival)
            alt = {p: n for p, n in base.items() if p not in removed}
            alt.update({p: n * 60 for p, n in targets.items()})
            eligible = bi.allowed(rows) | set(targets)
            moves = []
            if changed:
                deficit = max(0, duration - sum(alt.get(p, 0) for p in ROLES[team]['center']))
                if deficit:
                    candidates = [p for p in ROLES[team]['center'] if p in eligible and p in alt]
                    p = max(candidates, key=lambda p: alt[p])
                    alt[p] += deficit
                    moves.append({'player': p, 'seconds': deficit, 'reason': 'CONDITIONAL_CENTER_COVERAGE_NOT_CLOCK_CORRECTION'})
            gap = 5 * duration - sum(alt.values())
            for p, limit in recipients if gap > 0 else donors:
                if p not in eligible or p in targets or p in removed:
                    continue
                old = alt.get(p, 0)
                delta = min(gap, max(0, limit * 60 - old)) if gap > 0 else -min(-gap, max(0, old - limit * 60))
                if delta:
                    alt[p] = old + delta
                    gap -= delta
                    moves.append({'player': p, 'seconds': delta, 'limit_minutes': limit})
                if gap == 0:
                    break
            assert gap == 0, (gid, team, profile, rival, gap)
            alt = {p: n for p, n in sorted(alt.items()) if n > 0}
            starters = [swaps.get(r['player'], r['player']) for r in rows if r['start'] == '1']
            # Replacement starter policies use roles/availability, never game score or ratings.
            if team == 'POR' and any(p in removed for p in starters):
                replacement = next(p for p in ['Anfernee Simons', 'Rodney Hood', 'Nassir Little', 'Derrick Jones Jr.']
                                   if alt.get(p, 0) >= 180 and p not in starters)
                starters = [replacement if p in removed else p for p in starters]
            if team == 'DET' and not (set(starters) & set(ROLES['DET']['handler'])):
                assert 'Rodney McGruder' in starters and 'Kira Lewis Jr.' not in starters
                starters = ['Kira Lewis Jr.' if p == 'Rodney McGruder' else p for p in starters]
                moves.append({'reason':'KIRA_STARTS_FOR_MCGRUDER_HANDLER_POLICY_NO_EXTRA_MINUTES'})
            if team == 'ORL' and changed:
                starters = ['Nikola Vucevic' if p == 'Khem Birch' else p for p in starters]
            if changed:
                # A required three-minute start with two center-role players needs
                # 48+3 center-role minutes, not just 48. Fund the overlap explicitly.
                centers = set(ROLES[team]['center'])
                overlap = 180 * max(0, len(set(starters) & centers) - 1)
                deficit = max(0, duration + overlap - sum(alt.get(p, 0) for p in centers))
                if deficit:
                    recipient = max((p for p in centers if p in alt), key=lambda p: alt[p])
                    donor = max((p for p in alt if p not in centers and p not in targets), key=lambda p: alt[p])
                    assert alt[donor] - deficit >= (180 if donor in starters else 0)
                    alt[recipient] += deficit
                    alt[donor] -= deficit
                    moves.append({'player': recipient, 'seconds': deficit, 'donor': donor,
                                  'reason': 'CONDITIONAL_STARTER_CENTER_OVERLAP_NOT_CLOCK_CORRECTION'})
                alt = dict(sorted(alt.items()))
            assert len(set(starters)) == 5 and set(starters) <= set(alt), (gid, starters)
            assert max(alt.values()) <= duration, (gid, team, alt)
            result.append({'event_id': gid, 'date': day, 'team': team, 'profile': profile,
                'rival_minutes': rival, 'changed': changed, 'game_duration_seconds': duration,
                'clock_correction': clock, 'actual_seconds': base, 'alternate_seconds': alt,
                'removed_players': removed, 'newcomers': sorted(targets), 'starters': sorted(starters),
                'balance_moves': moves,
                'delta_seconds': {p: alt.get(p, 0) - base.get(p, 0) for p in sorted(set(base) | set(alt)) if alt.get(p, 0) != base.get(p, 0)},
                'status': 'CONDITIONAL_MINUTES_NOT_AVAILABILITY_OR_TRANSACTION_APPROVAL'})
    return result


def verify_minutes(branches, witnesses):
    raw = groups()
    for b, witness in zip(branches, witnesses, strict=True):
        assert sum(b['delta_seconds'].values()) == 0
        assert sum(b['alternate_seconds'].values()) == 5 * b['game_duration_seconds']
        assert not set(b['removed_players']) & set(b['alternate_seconds'])
        eligible = bi.allowed(raw[b['event_id'], b['team']]) | set(b['newcomers'])
        assert all(p in eligible for p, n in b['delta_seconds'].items() if n > 0)
        if not b['changed']:
            assert witness is None and not b['delta_seconds']
            continue
        total = 0
        seen = defaultdict(float)
        start = 0
        for w in witness:
            assert len(w['players']) == 5 and bi.valid(w['players'], b['team'], ROLES)
            assert w['seconds'] > 0
            total += w['seconds']
            if sorted(w['players']) == b['starters']:
                start += w['seconds']
            for p in w['players']:
                seen[p] += w['seconds']
        assert abs(total - b['game_duration_seconds']) < 1e-5 and start >= 180 - 1e-5
        assert set(seen) == set(b['alternate_seconds'])
        assert all(abs(seen[p] - n) < 1e-5 for p, n in b['alternate_seconds'].items())


def paired_inputs(branches):
    actual = bi.lb.normalized_games()
    byid = {g['id']: g for g in actual}
    maps = bi.cc.rating_maps()
    env = bi.cc.envelopes(maps)
    # Link archive names by the common player ID, not by a guessed fuzzy match.
    alias = next(r for r in bi.cc.read(bi.cc.BPM) if r['player_id'] == 'kanteen01')
    assert alias['nba_player'] == 'Enes Freedom'
    source = next(r for r in bi.cc.read(bi.cc.paired.RAPTOR) if r['player_id'] == 'kanteen01')
    maps['RAPTOR_RS_EB'][bi.cc.paired.norm(alias['nba_player'])] = maps['RAPTOR_RS_EB'][bi.cc.paired.norm(source['player_name'])]
    schedule = defaultdict(list)
    for g in actual:
        for t in (g['home'], g['away']):
            schedule[t].append(g['date'])
    b2b = {(t, d): i > 0 and (date.fromisoformat(d) - date.fromisoformat(ds[i-1])).days == 1
           for t, days in schedule.items() for ds in [sorted(days)] for i, d in enumerate(ds)}
    raw = groups()
    lookup = defaultdict(list)
    for b in branches:
        lookup[b['event_id'], b['team']].append(b)
    inputs = []
    for gid in sorted({b['event_id'] for b in branches}):
        g = byid[gid]
        h, a, day = g['home'], g['away'], g['date']
        margin = sum(int(r['pts']) for r in raw[gid, h]) - sum(int(r['pts']) for r in raw[gid, a])
        assert abs(margin) == g['margin'] and (h if margin > 0 else a) == g['winner']
        for profile, rival in itertools.product(bi.PROFILES, (24, 28, 32) if 'MIN' in (h, a) else (None,)):
            def choose(t):
                found = [b for b in lookup[gid, t] if b['profile'] in (profile, 'OBSERVED_HELD') and b['rival_minutes'] in (None, rival)]
                assert len(found) == 1
                return found[0]
            hs, aws = choose(h), choose(a)
            assert hs['game_duration_seconds'] == aws['game_duration_seconds']
            for method, fatigue in itertools.product(bi.METHODS, (0, .5, 1)):
                home, hu = bi.cc.form(hs['delta_seconds'], maps[method], {})
                away, au = bi.cc.form(aws['delta_seconds'], maps[method], {})
                terms = {p: hu.get(p, 0) - au.get(p, 0) for p in set(hu) | set(au) if hu.get(p, 0) != au.get(p, 0)}
                # Missing coefficients stay symbolic; they are never zero-imputed.
                hp = sum(max(0, n) for n in hs['delta_seconds'].values()) / 2880 if b2b[h, day] else 0
                ap = sum(max(0, n) for n in aws['delta_seconds'].values()) / 2880 if b2b[a, day] else 0
                constant = margin + home - away - fatigue * hp + fatigue * ap
                band = bi.cc.band(constant, terms, env[method])
                inputs.append({'event_id': gid, 'profile': profile, 'rival_minutes': rival,
                    'method': method, 'fatigue': fatigue, 'actual_home_margin': margin,
                    'home_margin_constant': round(constant, 8), 'away_margin_constant': round(-constant, 8),
                    'unknown_coefficients': terms, 'home_margin_band': band,
                    'conditional_sign': 'HOME' if band[0] > 0 else 'AWAY' if band[1] < 0 else 'UNRESOLVED',
                    'workload_coefficients': [hp, ap], 'selected': False})
    return inputs


def bridges(inputs):
    upstream=json.loads(d.OUT.read_text())
    actual=bi.lb.normalized_games();actual_byid={g['id']:g for g in actual}
    result=[]
    for ix,previous in enumerate(upstream['season_bridge']):
        c=previous['source_condition'];profile,rival,_=c['path_id'].split('/');rival=int(rival.split('_')[1])
        chosen=[r for r in inputs if (r['profile'],r['method'],r['fatigue'])==(profile,c['method'],c['fatigue']) and r['rival_minutes'] in (None,rival)]
        assert len(chosen)==80
        assert all(set(r['unknown_coefficients'])<={RIVAL} for r in chosen)
        lo,hi=previous['shared_rival_rating_open_interval']
        cuts=sorted({-r['home_margin_constant']/r['unknown_coefficients'][RIVAL] for r in chosen if RIVAL in r['unknown_coefficients']})
        bounds=[lo,*[cut for cut in cuts if lo<cut<hi],hi]
        boundaries=[{'rating':cut,'event_ids':[r['event_id'] for r in chosen if r['unknown_coefficients'] and abs(r['home_margin_constant']+r['unknown_coefficients'][RIVAL]*cut)<1e-7]} for cut in cuts if lo<=cut<=hi]
        lookup={r['event_id']:r for r in chosen}
        for low,high in zip(bounds,bounds[1:]):
            rating=(low+high)/2;games=[];changed=set(previous['changed_game_ids'])
            for g in actual:
                winner=bi.lb.changed_game(g)['winner'] if g['id'] in changed else g['winner']
                if g['id'] in lookup:
                    r=lookup[g['id']];value=r['home_margin_constant']+r['unknown_coefficients'].get(RIVAL,0)*rating
                    assert abs(value)>1e-8
                    winner=g['home'] if value>0 else g['away']
                games.append({**g,'winner':winner})
            wins=bi.lb.record_wins(games)
            assert sum(wins.values())==1080 and wins['CHI']==previous['team_wins']['CHI']
            delta={t:wins[t]-previous['team_wins'][t] for t in wins if wins[t]!=previous['team_wins'][t]}
            assert sum(delta.values())==0
            try:seeds=d.ps.order(games);tie_hold=None
            except ValueError as error:seeds=None;tie_hold=str(error)
            result.append({'source_bridge_index':ix,'source_condition':c,'shared_rival_rating_open_interval':[low,high],
                'zero_boundaries_unresolved':boundaries,'team_wins':dict(sorted(wins.items())),
                'win_deltas_vs_D':delta,'seeds':seeds,'later_tie_hold':tie_hold,
                'chicago_rank':seeds['EAST'].index('CHI')+1 if seeds else None,
                'changed_game_ids':sorted(g['id'] for g in games if g['winner']!=actual_byid[g['id']]['winner']),
                'other_games_held':859,'selected':False})
    return result


def league_cases(bridge):
    grouped=defaultdict(list)
    for i,row in enumerate(bridge):grouped[tuple(row['changed_game_ids'])].append(i)
    cases=[]
    for i,(changed,indices) in enumerate(sorted(grouped.items()),1):
        row=bridge[indices[0]];seeds=row['seeds'];wins=row['team_wins']
        case={'id':f'E{i:03d}','bridge_indices':indices,'changed_game_ids':list(changed),'team_wins':wins,
              'seeds':seeds,'later_tie_hold':row['later_tie_hold'],'selected':False}
        if seeds:
            case['playin_seed_teams']={c:seeds[c][6:10] for c in seeds}
            fields=set();chi_positions={'LOTTERY':[],'PLAYOFF':[]}
            for east,west in itertools.product(d.ps.playin(seeds['EAST']),d.ps.playin(seeds['WEST'])):
                playoff=set(seeds['EAST'][:6]+seeds['WEST'][:6]+east['qualifiers']+west['qualifiers'])
                lottery=d.ps.ALL-playoff;assert len(lottery)==14
                fields.add(tuple(sorted(lottery)))
                section='LOTTERY' if 'CHI' in lottery else 'PLAYOFF'
                groups=d.ps.record_groups(lottery,wins)+d.ps.record_groups(playoff,wins,15)
                chi_positions[section].extend(next(g['positions'] for g in groups if 'CHI' in g['teams']))
            case['possible_distinct_lottery_fields']=len(fields)
            case['chicago_record_position_ranges']={k:[min(v),max(v)] for k,v in chi_positions.items() if v}
            case['joint_playin_outcome_count']=64
        cases.append(case)
    return cases


def build(witnesses):
    branches=specs();verify_minutes(branches,witnesses);inputs=paired_inputs(branches)
    actual={g['id']:g for g in bi.lb.normalized_games()};summaries=[]
    for gid in sorted({r['event_id'] for r in inputs}):
        rows=[r for r in inputs if r['event_id']==gid];g=actual[gid]
        actual_sign='HOME' if g['winner']==g['home'] else 'AWAY';signs={r['conditional_sign'] for r in rows}
        status='ALL_TESTED_RETAIN' if signs=={actual_sign} else 'ALL_TESTED_REVERSE' if signs==({'HOME','AWAY'}-{actual_sign}) else 'MODEL_DISAGREEMENT_OR_UNRESOLVED'
        summaries.append({'event_id':gid,'home':g['home'],'away':g['away'],'actual_winner':g['winner'],
            'status':status,'selected':False,'both_observed_held':all(not b['changed'] for b in branches if b['event_id']==gid),
            'method_bands':{m:[min(r['home_margin_band'][0] for r in rows if r['method']==m),max(r['home_margin_band'][1] for r in rows if r['method']==m)] for m in bi.METHODS}})
    bridge=bridges(inputs);cases=league_cases(bridge)
    return {'stage':'O-15F14-E','status':'CLOSE80_CONDITIONAL_IMPACT_AND_JOINT_RIVAL_PATHS_COMPLETE_FINAL_SEASON_HOLD',
        'branches':branches,'lineup_witnesses':witnesses,'paired_inputs':inputs,'game_summary':summaries,
        'season_bridge':bridge,'league_cases':cases,'roles':ROLES,'selected':False,'manuscript_allowed':False,
        'conditions':['Existing LOW/HIGH target minutes and rival24/28/32 retained. New date capacity extensions chosen before metric evaluation; donor/recipient lists are local coaching conditions, not a universal rotation.',
            'Newcomer registration and health conditional; incumbent observed-date injury/protocol/DNP preserved.',
            'MIN same effective rating on all nine new games and upstream Chicago dates; interval counts have no probability weight.',
            'MIN Vanderbilt may cover the interior in this conditional small-ball policy. This avoids forcing all 48 minutes onto conventional centers; actual stints, rim protection and role interaction efficiency remain unverified.',
            'ORL May1 Hall/Wagner incumbents require contracts under Vucevic retention; Nnaji PF and some three-center-role lineups are allowed analytically, not tactical proof.',
            'DET Mar26 Kira starts instead of McGruder to provide a handler; total minutes unchanged.',
            'All actual overtime exposures retained as a diagnostic, not an alternate overtime prediction.',
            'MIL Feb10 source total14403 has a separate documented -3-second normalization; other raw clocks unchanged.',
            'RAPTOR RS/BPM Mar25 retrospective shrink, actual margin residual,100possessions/48minutes, workload sensitivity; pace and interaction changes not estimated.',
            'Other859 games remain actual-held. Neither no-impact certification nor final standings. Exact transactions, health, playoffs and lottery unselected.'],
        'upstream_sha256':{p.name:bi.cc.sha(p) for p in (OBS,d.OUT,queue.OUT,queue.TEAM_QUEUE,bi.cc.BPM,bi.cc.paired.RAPTOR,Path(__file__))}}


def pending(data):
    complete={g['event_id'] for g in data['game_summary']}
    return [{**r,'boundary_screen_basis':'O-15F14-E_PRE_CLOSE80_SEVEN_PATHS_NOT_FINAL_BRIDGE'} for r in bi.cc.read(queue.QUEUE) if r['event_id'] not in complete]


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
    if a.write:
        data=build([bi.solve(b,ROLES) for b in specs()])
        # Compact JSON is deliberate: witnesses remain machine-readable without90k-line artifacts.
        OUT.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
        bi.cc.write_csv(PENDING,pending(data))
    else:
        data=json.loads(OUT.read_text());assert data==build(data['lineup_witnesses'])
        assert bi.cc.read(PENDING)==pending(data)
    print(json.dumps({'PASS':True,'branches':len(data['branches']),'changed':sum(b['changed'] for b in data['branches']),
        'inputs':len(data['paired_inputs']),'games':dict(Counter(r['status'] for r in data['game_summary'])),
        'bridge':len(data['season_bridge']),'league_cases':len(data['league_cases']),
        'later_ties':sum(bool(r['later_tie_hold']) for r in data['season_bridge']),
        'CHI_ranks':sorted({r['chicago_rank'] for r in data['season_bridge'] if r['chicago_rank']})}))
