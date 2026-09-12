"""Conditional contract order and RFA amounts, not a certified NBA cap ledger."""
import json
from copy import deepcopy
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE_INPUTS.json'
OUT=ROOT/'simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json'


def ceiling(n,d):
    return (n+d-1)//d


def normal_cap(contracts,holds,rookie_min,extra=0):
    if set(contracts)&set(holds):raise ValueError('salary and FA hold double counted')
    if extra<0:raise ValueError('net additional charge must be nonnegative')
    empty=max(0,12-len(contracts)-len(holds))
    return dict(known_salaries=sum(contracts.values()),FA_holds=sum(holds.values()),incomplete_count=empty,incomplete_charge=empty*rookie_min,total=sum(contracts.values())+sum(holds.values())+empty*rookie_min+extra)


def run_route(p,final,route,bonus=0,normal_extra=0,apron_extra=0,late_first=False):
    contracts={k:v for k,v in final.items() if k not in {'Markkanen','Caruso',*p['late_minimum_order']}}
    if len(contracts)!=9:raise ValueError('entry requires nine proposed contracts including P')
    holds=dict(p['retained_FA']);ntmle=p['ntmle2021'];used_ntmle=False;hard=False;rows=[];checks=[]
    def snapshot(event,cap_required=False):
        nonlocal ntmle
        n=normal_cap(contracts,holds,p['rookie_min2021'],normal_extra+bonus)
        # Both public Markkanen QO references fit this upper budget; outside
        # offer-sheet matching and any other RFA tender are excluded conditions.
        q=p['Markkanen_apron_QO_upper_reference'] if 'Markkanen' in holds else 0
        apron=sum(contracts.values())+bonus+q+apron_extra
        if ntmle and n['total']<p['cap2021'] and p['cap2021']-n['total']>=ntmle:ntmle=0
        rec=dict(event=event,normal=n,standard_contracts=len(contracts),cap_room=p['cap2021']-n['total'],apron_upper_budget=apron,apron_room=p['apron2021']-apron,hard_cap_from_this_route=hard,unused_NTMLE_in_this_restricted_model=ntmle,cap_required=cap_required)
        if cap_required:checks.append(dict(event=event,kind='CAP_ROOM',room=rec['cap_room']))
        if hard:checks.append(dict(event=event,kind='APRON',room=rec['apron_room']))
        rows.append(rec)
    def sign(name,method):
        nonlocal ntmle,used_ntmle,hard
        if name in contracts:raise ValueError('duplicate signature')
        if method=='BIRD' and name not in holds:raise ValueError('Bird rights missing')
        if method=='NTMLE':
            before=normal_cap(contracts,holds,p['rookie_min2021'],normal_extra+bonus)['total']
            if ntmle<final[name] or (before<p['cap2021'] and p['cap2021']-before>=ntmle):raise ValueError('NTMLE no longer available')
            ntmle-=final[name];used_ntmle=True;hard=True
        contracts[name]=final[name];holds.pop(name,None)
        snapshot('SIGN_'+name+'_'+method,method=='CAP_ROOM')
    def renounce():
        nonlocal ntmle
        holds.pop('Theis',None);holds.pop('Denzel Valentine',None)
        if route['Caruso_route']=='CAP_ROOM':ntmle=0
        snapshot('RENOUNCE_UNUSED_FA_AND_APPLICABLE_EXCEPTIONS')
    snapshot('ENTRY_AFTER_DUARTE_AND_GREEN')
    # late_first is a comparison counterexample: every minimum contract is
    # signed before Caruso, consuming room even though minimum exceptions exist.
    if late_first:
        for name in p['late_minimum_order']:sign(name,'MINIMUM')
    if route['first_contract']=='Markkanen':sign('Markkanen','BIRD')
    if route['Caruso_route']=='CAP_ROOM':renounce()
    sign('Caruso',route['Caruso_route'])
    if route['first_contract']=='Caruso':sign('Markkanen','BIRD')
    if route['Caruso_route']=='NTMLE':renounce()
    if not late_first:
        for name in p['late_minimum_order']:sign(name,'MINIMUM')
    if contracts!=final or holds:raise ValueError('final proposed roster mismatch')
    return dict(rows=rows,conditional_numeric_pass=all(c['room']>=0 for c in checks),constraints=checks,normal_extra_upper_at_Caruso=min((c['room']+normal_extra for c in checks if c['kind']=='CAP_ROOM'),default=None),apron_extra_upper_after_trigger=min((c['room']+apron_extra for c in checks if c['kind']=='APRON'),default=None),final_slots=len(contracts),final_gross_budget=sum(contracts.values())+bonus,used_NTMLE=used_ntmle,room_MLE_eligible_under_assumed_prior_uses=not used_ntmle and route['Caruso_route']=='CAP_ROOM',actual_execution_certified=False)


def single_season_starter_sufficient(starts,minutes):
    if starts is not None and starts>=41:return True
    if minutes is not None and minutes>=2000:return True
    return None  # A prior-season adjusted two-year criterion may still apply.


def future_budget(g1,p,policy,dead_salary=None):
    if dead_salary is not None and dead_salary<0:raise ValueError('negative dead salary')
    c=p['second_year_named_costs'];reserve=p['replacement_reserve']
    delta=c['Wieskamp']-reserve
    delta+=(c['Bradley']-reserve) if policy['Bradley_option_exercised'] else 0
    delta+=(c['Valentine']-reserve) if policy['Valentine_retained'] else 0
    out=[]
    for row in g1['budget_2022_cases']:
        total=row['total_budget']+delta
        out.append(dict(policy=policy['id'],protagonist_first=row['protagonist_first'],Carter_first=row['carter_first'],Young_or_replacement=row['young_or_replacement'],draft2022_reserve=row['draft2022_reserve'],standard_slots=15,known_budget_excluding_dead_salary=total,delta_from_G1=delta,tax_room_before_dead_salary=150267000-total,apron_room_if_new_trigger_before_dead_salary=156983000-total,dead_salary=dead_salary,total_with_confirmed_dead_salary=None if dead_salary is None else total+dead_salary,Valentine_waiver_charge_requires_resolution=not policy['Valentine_retained'],new_hard_cap_trigger_selected=False))
    return out


def build():
    p=json.loads(INPUT.read_text());g7=json.loads((ROOT/p['parent_roster']).read_text());g1=json.loads((ROOT/p['parent_budget']).read_text())
    final=g7['scenarios'][0]['named_roster_without_protagonist'];routes=[]
    for route in p['routes']:
        cases=[];stage_ranges={}
        for pro in g1['rookie_fourth_cases']:
            for bonus in (0,1000000):
                roster=dict(final,Protagonist=pro['salary']);v=run_route(p,roster,route,bonus)
                for row in v['rows']:
                    z=stage_ranges.setdefault(row['event'],{k:[] for k in ['standard_contracts','cap_room','apron_room','unused_NTMLE_in_this_restricted_model']})
                    for k in z:z[k].append(row[k])
                cases.append(dict(protagonist=pro,Young_bonus_budget=bonus,normal_extra_upper_at_Caruso=v['normal_extra_upper_at_Caruso'],apron_extra_upper_after_trigger=v['apron_extra_upper_after_trigger'],numeric_pass_at_zero_extra=v['conditional_numeric_pass'],final_gross_budget=v['final_gross_budget']))
        worst=max(g1['rookie_fourth_cases'],key=lambda r:r['salary']);example=run_route(p,dict(final,Protagonist=worst['salary']),route,1000000)
        ranges={event:{k:dict(min=min(a),max=max(a)) for k,a in vals.items()} for event,vals in stage_ranges.items()}
        routes.append(dict(**route,cases=cases,stage_ranges=ranges,maximum_salary_example=example,min_normal_extra_limit=min((c['normal_extra_upper_at_Caruso'] for c in cases if c['normal_extra_upper_at_Caruso'] is not None),default=None),min_apron_extra_limit=min((c['apron_extra_upper_after_trigger'] for c in cases if c['apron_extra_upper_after_trigger'] is not None),default=None),actual_normal_extra=None,actual_apron_extra=None,executed=False))
    qos=[]
    for pro in g1['rookie_fourth_cases']:
        qos.append(dict(protagonist=pro,nonstarter_QO_budget_upper=ceiling(pro['salary']*(1000+p['rookie2018_QO_percent_permille'][str(pro['pick'])]),1000),starter_QO_reference=p['starter_QO2018_reference'],selected_QO=None,actual_starter_criteria_met=None,actual_rounding_charge_certified=False))
    future=[row for pol in p['followup_2022_policies'] for row in future_budget(g1,p,pol)]
    # Lower bound before the two preliminary signings. Unsigned #10's 120%
    # hold equals its proposed salary. Omit Green salary and any replacement
    # empty charge entirely to avoid using an unknown Green FA amount as proof.
    entry_lower=min(r['known_normal_cap_before_Caruso']+p['retained_FA']['Denzel Valentine']-final['Green'] for r in g1['ntmle_sequence'])
    return dict(stage='O-15G8',status='CONDITIONAL_ORDER_AND_CONTRACT_BRIDGE',recommended_route=p['recommended_route'],routes=routes,route_salary_cases=240,NTMLE_entry_lower_bound_excluding_Green=entry_lower,NTMLE_entry_lower_plus_exception_exceeds_cap=entry_lower+p['ntmle2021']>p['cap2021'],protagonist_QO_cases=qos,starter_single_season_only_is_sufficient_not_necessary=True,prior_season_proration_rounding_verified=False,Carter_options=[dict(**o,total=sum(o['salary_2022_to_2026']) if o['salary_2022_to_2026'] else None,contract_agreed=False) for o in p['Carter_options']],budget2022_cases=future,budget2022_case_count=len(future),selected_route=None,selected_Carter_contract=None,contracts_agreed=False,author_locked=False,season_selected=False,exact_execution_cleared=False,manuscript_allowed=False,independent_review='NOT_INDEPENDENT')


if __name__=='__main__':
    x=build();OUT.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(PASS=True,route_cases=x['route_salary_cases'],routes={r['id']:{k:r[k] for k in ['min_normal_extra_limit','min_apron_extra_limit']} for r in x['routes']},QO_cases=len(x['protagonist_QO_cases']),budget2022_cases=x['budget2022_case_count'],contracts_agreed=False)))
