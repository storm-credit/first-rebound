"""Candidate availability and named budget examples, never draft/contract execution."""
import json
from itertools import product
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'simulation/CHICAGO_2021_NAMED_ROSTER_INPUTS.json'
OUT=ROOT/'simulation/CHICAGO_2021_NAMED_ROSTER_OPTIONS.json'


def choose_remaining(priority, already_taken):
    """A supplied board condition only; no invented upstream team choices."""
    return next((x for x in priority if x not in set(already_taken)), None)


def replace_slots(roster, mapping, prices):
    if len(set(mapping.values())) != len(mapping):
        raise ValueError('duplicate candidate occupies multiple slots')
    out=dict(roster)
    for slot,name in mapping.items():
        if slot not in out or name in out:
            raise ValueError('missing slot or duplicated player')
        del out[slot]
        out[name]=prices[name]
    return out


def build():
    p=json.loads(INPUT.read_text())
    s=json.loads((ROOT/p['source_file']).read_text())
    g=json.loads((ROOT/p['parent_file']).read_text())
    d=json.loads((ROOT/p['draft_file']).read_text())
    assert not any(p[x] for x in ['author_locked','season_selected','exact_execution_cleared','manuscript_allowed'])
    assert d['core_asset_settlement']['CHI_first']['pick']==10
    assert d['core_asset_settlement']['CHI_NOP_second']['CHI_receives_pick']==39
    public={c['player']:c for c in s['contracts']}
    roster=g['offseason_2021']['G1A']['roster_without_protagonist']
    prices={name:row['reported_2021_base'] for name,row in public.items()}
    prices.update({'Moses Moody':roster['Draft2021_10'],'Kessler Edwards':p['minimum_39_first']})
    named=replace_slots(roster,p['named_slot_mapping'],prices)
    assert len(named)+1==15
    alternatives={}
    for center in p['backup_center_candidates']:
        r=dict(named)
        del r['Tony Bradley'];r[center]=prices[center]
        cases=[]
        for f,bonus in product(g['rookie_fourth_cases'],(0,1000000)):
            # Gross player salary + bonus reserve: a conservative budget lane,
            # not proof of the complete cap/apron ledger or exception eligibility.
            total=sum(r.values())+f['salary']+bonus
            cases.append(dict(protagonist=f,young_bonus_reserve=bonus,total_gross_budget=total,
                              apron_minus_gross_budget=143002000-total))
        minimum_route=center!='Gorgui Dieng'
        alternatives[center]=dict(standard_slots=len(r)+1,min_budget=min(x['total_gross_budget'] for x in cases),max_budget=max(x['total_gross_budget'] for x in cases),min_conditional_apron_gap=min(x['apron_minus_gross_budget'] for x in cases),cap_minus_max_gross_budget=112414000-max(x['total_gross_budget'] for x in cases),cases=cases,reported_minimum_route=minimum_route,contract_executable=None)
    availability={}
    for label,key in [('pick10','first_round_candidates'),('pick39','second_round_candidates')]:
        priority=p[key];cases=[]
        for bits in product((False,True),repeat=len(priority)):
            taken=[n for n,b in zip(priority,bits) if b]
            cases.append(dict(taken_test_only=taken,recommendation_if_that_condition=choose_remaining(priority,taken)))
        availability[label]=dict(cases=cases,actual_upstream_board=None,selected_player=None)
    rotation={pos:{p['named_slot_mapping'].get(n,n):mins for n,mins in alloc.items()} for pos,alloc in g['healthy_rotation_position_budget'].items()}
    assert all(sum(x.values())==48 for x in rotation.values())
    remaining_mle=9536000-p['caruso_NTMLE_reserved']
    # A real retained FA amount may support the normal-cap sequence; reserves
    # cannot. This remains conditional on the existing rights/contract route.
    retained_hold=p['valentine_retained_FA_amount_reference']
    sequence=[dict(protagonist=c['protagonist'],normal_cap_plus_retained_Valentine=c['known_normal_cap_before_Caruso']+retained_hold,additional_real_amount_still_required=max(0,c['additional_real_cap_amount_required']-retained_hold),exact_sequence_executed=False) for c in g['ntmle_sequence']]
    future_base=g['budget_2022_fixed_without_four_variables']
    second_changes=dict(Bradley_player_option_if_exercised=public['Tony Bradley']['reported_2022_base']-future_base['Reserve_center'],Valentine_second_year_if_retained=public['Denzel Valentine']['reported_2022_base']-future_base['Reserve_guard'],rookie39_if_second_minimum_year=p['minimum_39_second_reference']-future_base['Draft2021_39'])
    return dict(stage='O-15G3',status='NAMED_CONDITIONAL_ROSTER_AND_BUDGET',
                recommended_if_available=p['recommended_if_available'],
                named_roster_without_protagonist=named,named_standard_slots=len(named)+1,
                literal_named_status='CONDITIONAL_EXAMPLE_NOT_ASSIGNED_OR_SIGNED',
                parent_G1A_max_budget=g['offseason_2021']['G1A']['max_budget'],
                gross_budget_delta_from_G1A=sum(named.values())-sum(roster.values()),
                centers=alternatives,availability=availability,
                primary_healthy_position_budget=rotation,rotation_scope='NAME_SUBSTITUTION_OF_G1A_ARITHMETIC_ONLY_NOT_PLAYER_FIT_OR_GAME_AVAILABILITY',
                exception_counterexample=dict(player='Gorgui Dieng',reported_first_salary=4000000,remaining_NTMLE=remaining_mle,BAE_standalone=p['BAE2021'],remaining_NTMLE_sufficient=remaining_mle>=4000000,BAE_sufficient=p['BAE2021']>=4000000,exceptions_may_be_added_together=False,verdict='NO_STANDALONE_IDENTIFIED_EXCEPTION_IN_G1A_SEQUENCE'),
                Dieng_cap_room_alternative='POST_SIGNING_RENUNCIATION_AND_ACTUAL_RESIDUAL_HOLD_NOT_PROVEN_IMPOSSIBLE',
                valentine_hold_sequence=sequence,
                rookie39_classification=dict(primary='DRAFT_ROOKIE_WITH_EXCLUSIVE_RIGHTS',salary=p['minimum_39_first'],is_rookie_free_agent=False,FA_zero_YOS_counterexample_tax_apron_salary=1669178,FA_counterexample_extra=1669178-p['minimum_39_first'],counterexample_selected=False),
                second_year_delta_conditions=second_changes,second_year_all_three_if_retained_delta=sum(second_changes.values()),
                pending_second_year_market_slot='Stanley Johnson one-year offer expires; G1A 2m replacement reserve remains only a budget',
                actual_nonroster_charge=None,actual_contracts_agreed=False,draft_players_selected=False,
                author_locked=False,season_selected=False,exact_execution_cleared=False,manuscript_allowed=False,
                independent_review='NOT_INDEPENDENT')


if __name__=='__main__':
    x=build();OUT.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(PASS=True,standard_slots=x['named_standard_slots'],gross_delta=x['gross_budget_delta_from_G1A'],centers={n:{k:v for k,v in r.items() if k in ['min_budget','max_budget','min_conditional_apron_gap']} for n,r in x['centers'].items()},availability_cases=sum(len(a['cases']) for a in x['availability'].values()),second_year_conditional_delta=x['second_year_all_three_if_retained_delta']),ensure_ascii=False))
