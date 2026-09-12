"""Budget/role proposals under CP2; neither contract execution nor game forecasts."""
import json
from collections import Counter
from itertools import product
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'simulation/CHICAGO_2021_23_CONTINUATION_INPUTS.json'
OUT=ROOT/'simulation/CHICAGO_2021_23_CONTINUATION.json'


def rookie_fourth(third, increase_permille, scale_percent):
    # Upward dollar rounding for a budget ceiling, not an exact contract charge.
    n=third*(1000+increase_permille)*scale_percent
    return (n+99999)//100000


def grow(first,years,annual_percent=8):
    return [first+first*annual_percent*i//100 for i in range(years)]


def rotation_allocation():
    return {'PG':{'LaMelo_pick4':32,'Coby':10,'Caruso':6},
            'SG':{'LaVine':34,'Coby':8,'Caruso':6},
            'SF':{'Protagonist':24,'Draft2021_10':14,'Caruso':10},
            'PF':{'Markkanen':28,'Protagonist':8,'Young':12},
            'C':{'Carter':28,'Young':8,'Reserve_center':12}}


def build():
    p=json.loads(INPUT.read_text());d=json.loads((ROOT/p['draft_file']).read_text())
    assert d['conditional_workflow_approved'] and not d['author_locked']
    a=d['core_asset_settlement']
    assert a['CHI_first']['pick']==10 and a['CHI_NOP_second']['CHI_receives_pick']==39
    s=p['salary_reference_2021_2022'];reserve=p['minimum_slot_budget_reserve']
    fourth=[dict(pick=i,percent=q,salary=rookie_fourth(p['rookie_2018_year3_100pct'][str(i)],p['rookie_2018_year4_increase_permille'][str(i)],q)) for i,q in product(range(16,31),(80,120))]
    common=['LaVine','LaMelo_pick4','Coby','Carter','Young','Satoransky','Markkanen','Caruso','Green','Draft2021_10']
    roster={t:s[t][0] for t in common}
    roster.update(Draft2021_39=p['second_round_2021_budget_reserve'],Reserve_center=reserve,Reserve_wing=reserve,Reserve_guard=reserve)
    options={}
    for id in ('G1A','G1B','G1C','G1D'):
        r=dict(roster)
        if id=='G1B':
            del r['Markkanen'];r['DJJ']=s['DJJ'][0]
            del r['Reserve_center'];r['Theis']=s['Theis'][0]
        elif id=='G1C':
            del r['Satoransky'];del r['Caruso'];r['Lonzo']=s['Lonzo'][0];r['Reserve_extra_guard']=reserve
        elif id=='G1D':
            del r['Young'];del r['Satoransky'];r['DeRozan']=s['DeRozan'][0];r['Reserve_extra_forward']=reserve
        cases=[]
        for f,bonus in product(fourth,(0,1000000)):
            bonuses=bonus if 'Young' in r else 0
            if 'Lonzo' in r:bonuses+=1000000 # all reported unlikely bonus reserved for apron comparison
            total=sum(r.values())+f['salary']+bonuses
            cases.append(dict(protagonist=f,young_bonus=bonus if 'Young' in r else 0,total_budget=total,apron_room=p['apron2021']-total))
        options[id]=dict(roster_without_protagonist=r,standard_slots=len(r)+1,min_budget=min(x['total_budget'] for x in cases),max_budget=max(x['total_budget'] for x in cases),min_apron_room=min(x['apron_room'] for x in cases),cases=cases,transaction_approved=False)
    # G1A: retain Markkanen/Theis FA amounts for normal cap accounting. Budget
    # reserves are not signed salaries and cannot preserve an exception.
    # Report the additional real cap amount needed, e.g. a retained Porter hold.
    # FA amounts do not all count in the separate hard-cap calculation.
    seq=[]
    for f in fourth:
        normal_before=sum(roster.values())-3*reserve-p['second_round_2021_budget_reserve']+f['salary']-s['Caruso'][0]-s['Markkanen'][0]+p['markkanen_cap_hold']+p['theis_cap_hold']
        gap=max(0,p['cap2021']-normal_before)
        seq.append(dict(protagonist=f,known_normal_cap_before_Caruso=normal_before,below_cap_gap=gap,additional_real_cap_amount_required=max(0,gap-p['ntmle2021']+1),eligibility_cleared=False))
    rota=rotation_allocation();byplayer=Counter()
    for pos,rows in rota.items():
        assert sum(rows.values())==48,pos
        byplayer.update(rows)
    assert sum(byplayer.values())==240 and len(byplayer)==10 and max(byplayer.values())<=48
    assert set(byplayer)<=set(roster)|{'Protagonist'}
    future={t:s[t][1] for t in ['LaVine','LaMelo_pick4','Coby','Markkanen','Caruso','Green','Draft2021_10']}
    future.update(Draft2021_39=p['second_round_2022_budget_reserve'],Reserve_center=reserve,Reserve_wing=reserve,Reserve_guard=reserve)
    cases=[]
    for pro,carter,young,pick in product(p['protagonist_2022_first_salary_candidates'],p['carter_2022_first_salary_candidates'],p['young_2022_including_bonus_candidates'],p['rookie_2022_reserve_scenarios']):
        r=dict(future,Protagonist=pro,Carter=carter,Young_or_replacement=young,Draft2022_reserve=pick)
        total=sum(r.values());assert len(r)==15
        cases.append(dict(protagonist_first=pro,carter_first=carter,young_or_replacement=young,draft2022_reserve=pick,standard_slots=15,total_budget=total,tax_room=p['tax2022']-total,apron_room_if_triggered=p['apron2022']-total))
    contracts=[dict(id='E1',structure='2021 extension, 2022 start',salary=grow(18000000,4)),dict(id='E2',structure='2022 direct Bird RFA, recommended budget',salary=grow(22000000,4)),dict(id='E3',structure='2022 five-year Bird max, conditional earned value',salary=grow(p['cap2022']//4,5)),dict(id='E4',structure='2022 one-year QO then 2023 UFA',salary=None)]
    for c in contracts:c['total']=sum(c['salary']) if c['salary'] else None
    return dict(stage='O-15G1',status='CONDITIONAL_DESIGN_AND_BUDGET',recommended_offseason='G1A',recommended_contract='E2',rookie_fourth_cases=fourth,offseason_2021=options,ntmle_sequence=seq,healthy_rotation_position_budget=rota,healthy_rotation_player_budget=dict(byplayer),rotation_scope='ARITHMETIC_ALLOCATION_ONLY_NOT_STINTS_OR_SEASON_GP',outside_healthy_rotation=['Satoransky','Green','Draft2021_39','Reserve_wing','Reserve_guard'],contract_options=contracts,budget_2022_cases=cases,budget_2022_fixed_without_four_variables=future,exact_nonroster_charge=None,actual_contracts_agreed=False,author_locked=False,season_selected=False,exact_execution_cleared=False,manuscript_allowed=False,independent_review='NOT_INDEPENDENT')


if __name__=='__main__':
    x=build();OUT.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(options={k:{v:o[v] for v in ['standard_slots','min_budget','max_budget','min_apron_room']} for k,o in x['offseason_2021'].items()},future_cases=len(x['budget_2022_cases']),rotation_minutes=sum(x['healthy_rotation_player_budget'].values())),ensure_ascii=False))
