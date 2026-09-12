"""CP2 draft simulation. Publish inputs/code before the first project-seed run."""
import json
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'simulation/NBA_2021_DRAW_PREREGISTRATION.json'
APPROVAL = ROOT / 'canon/CHICAGO_2020_21_CP2_APPROVAL.json'
OUT = ROOT / 'simulation/NBA_2021_PROVISIONAL_DRAFT.json'
WEIGHTS = [140,140,140,125,105,90,75,60,45,30,20,15,10,5]
COMBINATIONS = list(combinations(range(1,15),4))


class HashStream:
    def __init__(self, seed, domain):
        self.seed, self.domain, self.counter = seed, domain.encode(), 0
    def below(self, n):
        if type(n) is not int or n < 1: raise ValueError('positive integer bound required')
        limit = (1 << 256) - ((1 << 256) % n)
        while True:
            raw = sha256(self.seed+b'|'+self.domain+b'|'+self.counter.to_bytes(8,'big')).digest()
            self.counter += 1
            value = int.from_bytes(raw,'big')
            if value < limit: return value % n
    def permutation(self, members):
        out = sorted(members)
        for i in range(len(out)-1,0,-1):
            j=self.below(i+1);out[i],out[j]=out[j],out[i]
        return out


def record_groups(teams, wins):
    return [sorted(t for t in teams if wins[t]==w) for w in sorted({wins[t] for t in teams})]


def pre_order(teams, wins, seed, preserved):
    out=[];logs=[]
    for group in record_groups(teams,wins):
        key=','.join(group)
        if len(group)==1: order=group;method='NO_TIE'
        elif key in preserved:
            order=preserved[key];method='UNCHANGED_HISTORICAL_TIE'
            assert set(order)==set(group) and len(order)==len(group)
        else:
            order=HashStream(seed,'tie:'+key).permutation(group);method='HASH_DRAW'
        out += order
        logs.append(dict(wins=wins[group[0]],members=group,order=order,method=method))
    return out,logs


def allocate(ordered, wins):
    if len(ordered)!=14 or len(set(ordered))!=14: raise ValueError('14 distinct lottery origins required')
    tickets={};cursor=0
    for group in record_groups(ordered,wins):
        ordered_group=[t for t in ordered if t in group]
        total=sum(WEIGHTS[cursor:cursor+len(group)])
        q,r=divmod(total,len(group))
        for i,t in enumerate(ordered_group):tickets[t]=q+(i<r)
        cursor+=len(group)
    owners=[t for t in ordered for _ in range(tickets[t])]+[None]
    assert len(owners)==1001 and sum(tickets.values())==1000
    return tickets,owners


def draw_four(owners, next_index):
    winners=[];log=[]
    while len(winners)<4:
        index=next_index(1001);owner=owners[index]
        reason='UNASSIGNED' if owner is None else 'REPEAT_WINNER' if owner in winners else 'ACCEPTED'
        log.append(dict(attempt=len(log)+1,for_pick=len(winners)+1,index=index,
                        balls=list(COMBINATIONS[index]),origin=owner,decision=reason))
        if reason=='ACCEPTED':winners.append(owner)
    return winners,log


def second_round(first_order, wins):
    if len(first_order)!=30 or len(set(first_order))!=30: raise ValueError('30 first-round origins required')
    position={t:i for i,t in enumerate(first_order)}
    return sorted(first_order,key=lambda t:(wins[t],-position[t]))


def core_settlement(first_order, second_order):
    f={t:i+1 for i,t in enumerate(first_order)};s={t:i+31 for i,t in enumerate(second_order)}
    swap=s['NOP']<s['CHI']
    min_retains=f['MIN']<=3
    return dict(
        CHI_first=dict(pick=f['CHI'],owner='CHI',basis='APPROVED_NO_VUCEVIC_ROUTE'),
        MIN_first=dict(pick=f['MIN'],owner='MIN' if min_retains else 'GSW',
                       basis='CONDITIONAL_CARRY_FORWARD_TOP3_TERMS',
                       remaining_2022_obligation='UNPROTECTED_FIRST_TO_GSW' if min_retains else None),
        CHI_NOP_second=dict(CHI_origin_pick=s['CHI'],NOP_origin_pick=s['NOP'],
                            swap_exercised_conditionally=swap,CHI_receives_pick=min(s['CHI'],s['NOP']),
                            CHI_receives_origin='NOP' if swap else 'CHI',
                            NOP_receives_pick=max(s['CHI'],s['NOP'])),
        MIN_second=dict(pick=s['MIN'],owner_if_reported_prior_routes_retained='OKC'),
        complete_all_team_ownership_audit=False)


def build(prereg_public_commit):
    p=json.loads(INPUT.read_text());approval=json.loads(APPROVAL.read_text())
    assert approval['conditional_workflow_approved'] and approval['approved_procedure']=='CP2'
    assert not any(approval[k] for k in ('author_locked','season_selected','manuscript_allowed'))
    assert len(prereg_public_commit)==40 and all(c in '0123456789abcdef' for c in prereg_public_commit)
    for name,expected in p['input_sha256'].items():
        assert sha256((ROOT/name).read_bytes()).hexdigest()==expected,name
    assert sha256(Path(__file__).read_bytes()).hexdigest()==p['algorithm_sha256']
    k=json.loads((ROOT/p['k_input']).read_text())
    c=next(c for c in k['season_candidates'] if c['role']=='PRIMARY_RECOMMENDATION')
    l=json.loads((ROOT/p['l_input']).read_text())
    route=next(x for x in l['postseason_proposals'] if x['id']=='L2')
    wins=c['team_wins']
    assert c['base_case_id']=='F038' and wins==p['team_wins']
    assert route['lottery_teams']==p['lottery_teams'] and route['playoff_teams']==p['playoff_teams']
    assert Counter(g['winner'] for g in c['regular_season_games'])==Counter(wins)
    seed=sha256(p['seed_text'].encode()).digest()
    assert seed.hex()==p['seed_sha256']
    before,tie_log=pre_order(p['lottery_teams'],wins,seed,p['preserved_ties'])
    post,post_log=pre_order(p['playoff_teams'],wins,seed,p['preserved_ties'])
    tickets,owners=allocate(before,wins)
    rng=HashStream(seed,'lottery')
    winners,draw_log=draw_four(owners,rng.below)
    first=winners+[t for t in before if t not in winners]+post
    second=second_round(first,wins)
    return dict(stage='O-15F14-M',status='PROVISIONAL_CONDITIONAL_RESULT',
                preregistration_public_commit=prereg_public_commit,seed_text=p['seed_text'],seed_sha256=p['seed_sha256'],
                algorithm_sha256=p['algorithm_sha256'],preregistration_sha256=sha256(INPUT.read_bytes()).hexdigest(),
                conditional_workflow_approved=True,upstream_regular_season='K1_BPM_F038',postseason='L2',
                team_wins=wins,playin_games=route['east_games']+route['west_games'],
                tie_log=tie_log+post_log,lottery_pre_order=before,combinations_per_origin=tickets,
                combination_assignment=[dict(index=i,balls=list(b),origin=owners[i]) for i,b in enumerate(COMBINATIONS)],
                top_four=winners,draw_log=draw_log,hash_blocks_used=rng.counter,
                first_round_origins=[dict(pick=i+1,origin=t) for i,t in enumerate(first)],
                second_round_origins=[dict(pick=i+31,origin=t) for i,t in enumerate(second)],
                core_asset_settlement=core_settlement(first,second),
                exact_execution_cleared=False,author_locked=False,season_selected=False,manuscript_allowed=False,
                independent_review='NOT_INDEPENDENT')


if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser();a.add_argument('--preregistered-commit',required=True);args=a.parse_args()
    result=build(args.preregistered_commit)
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','top_four','core_asset_settlement')},ensure_ascii=False))
