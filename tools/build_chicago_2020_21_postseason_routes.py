"""O15F14-C: conditional conference order, play-in routes and remaining-game sensitivity.
Does not estimate missing impacts, choose outcomes, or perform a lottery draw.
"""
import argparse
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction
import build_chicago_2020_21_boundary_impact as bi

S=bi.S
OUT=S/'CHICAGO_2020_21_POSTSEASON_ROUTES.json'
QUEUE=S/'NBA_2020_21_REMAINING_BOUNDARY_QUEUE.csv'
EAST=bi.lb.sb.EAST
ALL=set('ATL BKN BOS CHA CHI CLE DAL DEN DET GSW HOU IND LAC LAL MEM MIA MIL MIN NOP NYK OKC ORL PHI PHX POR SAC SAS TOR UTA WAS'.split())
WEST=ALL-EAST
DIVS=bi.lb.DIVISIONS+[set(x.split()) for x in ('DEN MIN OKC POR UTA','GSW LAC LAL PHX SAC','DAL HOU MEM NOP SAS')]


def stats(games):
    wins=Counter();pair=Counter();gp=Counter()
    for g in games:
        h,a,w=g['home'],g['away'],g['winner'];l=a if w==h else h
        wins[w]+=1;pair[w,l]+=1;gp[h,a]+=1;gp[a,h]+=1
    return wins,pair,gp


def order(games):
    wins,pair,gp=stats(games)
    def pct(t,opponents):
        n=sum(gp[t,o] for o in opponents if o!=t)
        assert n
        return Fraction(sum(pair[t,o] for o in opponents if o!=t),n)
    champs=set()
    def tie(teams,division=False):
        teams=set(teams)
        if len(teams)==1:return sorted(teams)
        same=next((d for d in DIVS if teams<=d),None)
        conf=EAST if teams<=EAST else WEST
        h2h={t:pct(t,teams) for t in teams}
        champ={t:int(t in champs) for t in teams}
        criteria=([h2h,champ] if len(teams)==2 else [champ,h2h]) if not division else [h2h]
        if same:criteria.append({t:pct(t,same) for t in teams})
        criteria.append({t:pct(t,conf) for t in teams})
        for values in criteria:
            levels=sorted(set(values.values()),reverse=True)
            if len(levels)>1:
                return [t for v in levels for t in tie({t for t in teams if values[t]==v},division)]
        raise ValueError('Later criteria required: '+','.join(sorted(teams)))
    for d in DIVS:
        best=max(wins[t] for t in d)
        champs.add(tie({t for t in d if wins[t]==best},True)[0])
    result={}
    for name,conf in [('EAST',EAST),('WEST',WEST)]:
        result[name]=[t for w in sorted({wins[t] for t in conf},reverse=True) for t in tie({t for t in conf if wins[t]==w})]
    return result


def playin(seeds):
    s7,s8,s9,s10=seeds[6:10];out=[]
    for a,b,c in itertools.product((0,1),repeat=3):
        seven=(s7,s8)[a];upper_loser=(s8,s7)[a]
        lower_winner=(s9,s10)[b];lower_loser=(s10,s9)[b]
        eight=(upper_loser,lower_winner)[c];final_loser=(lower_winner,upper_loser)[c]
        out.append({'bits':[a,b,c],'games':[
            {'home':s7,'away':s8,'winner':seven},
            {'home':s9,'away':s10,'winner':lower_winner},
            {'home':upper_loser,'away':lower_winner,'winner':eight}],
            'qualifiers':[seven,eight],'eliminated':sorted([lower_loser,final_loser]),'selected':False})
    return out


def record_groups(teams,wins,start=1):
    result=[];n=start
    for w in sorted({wins[t] for t in teams}):
        group=sorted(t for t in teams if wins[t]==w)
        result.append({'wins':w,'teams':group,'positions':[n,n+len(group)-1],'tie_draw_selected':False})
        n+=len(group)
    return result


def build():
    upstream=json.loads(bi.OUT.read_text());actual=bi.lb.normalized_games()
    priority={r['event_id'] for r in upstream['game_summary']}
    remaining=[g for g in actual if 'CHI' not in (g['home'],g['away']) and g['id'] not in priority]
    assert len(remaining)==979
    # Equal records alone are insufficient: preserve all changed game IDs as identity.
    grouped=defaultdict(list)
    for r in upstream['season_bridge']:
        assert not r['unresolved_games']
        grouped[tuple(sorted(r['changed_game_ids']))].append(r)
    cases=[];queue={g['id']:{**g,'contact_status':bi.lb.contact(g)[0],
        'six_seed_cases':[],'ten_seed_cases':[],'CHI_rank_cases':[],'later_tie_cases':[],
        'impact_status':'NOT_CALCULATED','selected':False} for g in remaining}
    for ix,(changed,conditions) in enumerate(sorted(grouped.items()),1):
        cid=f'L{ix:02d}';changed=set(changed)
        games=[bi.lb.changed_game(g) if g['id'] in changed else dict(g) for g in actual]
        wins=bi.lb.record_wins(games);seeds=order(games)
        assert dict(wins)==conditions[0]['team_wins'] and sum(wins.values())==1080
        ep,wp=playin(seeds['EAST']),playin(seeds['WEST']);routes=[]
        direct=set(seeds['EAST'][:6]+seeds['WEST'][:6])
        for ei,e in enumerate(ep):
            for wi,w in enumerate(wp):
                playoff=direct|set(e['qualifiers']+w['qualifiers']);lottery=ALL-playoff
                assert len(playoff)==16 and len(lottery)==14
                pool=record_groups(lottery,wins);post=record_groups(playoff,wins,15)
                chi_group=next(g for g in pool+post if 'CHI' in g['teams'])
                routes.append({'east_route':ei,'west_route':wi,'lottery_teams':sorted(lottery),
                    'lottery_record_groups':pool,'CHI_in_lottery':'CHI' in lottery,
                    'CHI_record_positions':chi_group['positions'],'CHI_tied_teams':chi_group['teams'],
                    'CHI_pick_owner':'CHI','draw_selected':False,'selected':False})
        sensitivity=Counter()
        for gi,g in enumerate(games):
            if g['id'] not in queue:continue
            games[gi]=bi.lb.changed_game(g)
            try:
                alt=order(games)
                if any(set(alt[c][:6])!=set(seeds[c][:6]) for c in seeds):
                    queue[g['id']]['six_seed_cases'].append(cid);sensitivity['six_seed']+=1
                if any(set(alt[c][:10])!=set(seeds[c][:10]) for c in seeds):
                    queue[g['id']]['ten_seed_cases'].append(cid);sensitivity['ten_seed']+=1
                if alt['EAST'].index('CHI')!=seeds['EAST'].index('CHI'):
                    queue[g['id']]['CHI_rank_cases'].append(cid);sensitivity['CHI_rank']+=1
            except ValueError:
                queue[g['id']]['later_tie_cases'].append(cid);sensitivity['later_tie']+=1
            games[gi]=g
        cases.append({'id':cid,'source_conditions':[r['source_condition'] for r in conditions],
            'changed_game_ids':sorted(changed),'wins':dict(sorted(wins.items())),'seeds':seeds,
            'east_playin':ep,'west_playin':wp,'postseason_routes':routes,
            'distinct_lottery_fields':len({tuple(r['lottery_teams']) for r in routes}),
            'remaining_single_flip_trials':979,'sensitivity_counts':dict(sensitivity),'selected':False})
    rows=[]
    for q in queue.values():
        urgent=bool(q['six_seed_cases'] or q['ten_seed_cases'] or q['CHI_rank_cases'] or q['later_tie_cases'])
        rows.append({**q,'priority':'BOUNDARY_OR_TIE_REVIEW' if urgent else 'NO_SINGLE_FLIP_BOUNDARY_CERTIFICATE',
            **{k:'|'.join(q[k]) for k in ('six_seed_cases','ten_seed_cases','CHI_rank_cases','later_tie_cases')}})
    return {'stage':'O-15F14-C','status':'POSTSEASON_DEPENDENCIES_COMPLETE_REMAINING_IMPACT_AND_EXECUTION_HOLD',
        'scope':'29+CHI inputs held fixed; other979 actual results in base routes. Single flips are hypothetical, not impact estimates.',
        'cases':cases,'source_conditions':sum(len(c['source_conditions']) for c in cases),
        'queue_counts':dict(Counter(r['priority'] for r in rows)),
        'upstream_sha256':{p.name:bi.cc.sha(p) for p in (bi.OUT,bi.lb.QUEUE)},
        'probabilities_assigned':False,'lottery_draw_performed':False,'manuscript_allowed':False},rows


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    data,rows=build()
    if args.write:
        OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');bi.cc.write_csv(QUEUE,rows)
    else:
        assert json.loads(OUT.read_text())==data
        assert bi.cc.read(QUEUE)==[{k:str(v) for k,v in r.items()} for r in rows]
    print(json.dumps({'PASS':True,'cases':len(data['cases']),'conditions':data['source_conditions'],'queue':data['queue_counts'],
        'seeds':[{c['id']:{k:v[4:11] for k,v in c['seeds'].items()}} for c in data['cases']]}))
