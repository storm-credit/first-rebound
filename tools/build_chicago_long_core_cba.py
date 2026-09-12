"""Apply public CBA conditions to a fictional budget; never select future events."""
import json
from pathlib import Path
from itertools import product
from fractions import Fraction

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'simulation/CHICAGO_LONG_CORE_CBA_INPUTS.json'
OUT=ROOT/'simulation/CHICAGO_LONG_CORE_CBA.json'


def ceil_fraction(f):return -(-f.numerator//f.denominator)


def contract_salary(first,years,raise_percent=8):
    return [first+first*raise_percent*i//100 for i in range(years)]


def transaction_apron_limits(row,year,after_regular=False,prior_taxpayer_mle_used=False):
    if row not in 'ABCDEFGHIJK' or len(row)!=1:raise ValueError('unknown table row')
    if year<2023:return dict(status='PRE_2023_CBA_NOT_APPLIED',current=None,next_year=None)
    if row=='G' and year>=2024:return dict(status='TRANSITION_TPE_ENDED_REQUIRES_OTHER_ROUTE',current=None,next_year=None)
    level='first' if row in 'ABCDEFG' else 'second'
    current=None if year==2023 and row in 'FGHIJ' else level
    blocked=prior_taxpayer_mle_used and row in ('ABCDE' if year==2023 else 'ABCDEF')
    return dict(status='PRIOR_TAXPAYER_MLE_BLOCK' if blocked else 'APRON_TABLE_SCOPE_ONLY',current=current,next_year=level if after_regular and row in 'EFGHIJ' else None)


def second_apron_at_last_game(apron_salary,second_level):
    if apron_salary is None or second_level is None:return None
    return apron_salary>second_level


def frozen_pick(start_year,above_at_last_game_start,future):
    if start_year<2024:return dict(status='RULE_NOT_YET_ACTIVE',pick_year=None)
    if above_at_last_game_start is None:return dict(status='LAST_GAME_ACCOUNTING_UNKNOWN',pick_year=None)
    if not above_at_last_game_start:return dict(status='NO_FREEZE_FROM_THIS_YEAR',pick_year=None)
    over=under=0;pick=start_year+8
    for year in range(start_year+1,start_year+5):
        a=future.get(str(year))
        if a is None:return dict(status='FROZEN_PENDING_CHRONOLOGICAL_INPUT',pick_year=pick,first_unknown_season_start_year=year,exact_pick_number=None)
        if type(a) is not bool:raise ValueError('future apron status must be boolean or null')
        if a is True:over+=1
        if a is False:under+=1
        if over>=2:return dict(status='FINAL_FIRST_ROUND_GROUP_PENALTY',pick_year=pick,determined_after_season_start_year=year,exact_pick_number=None)
        if under>=3:return dict(status='UNFROZEN_AFTER_THIRD_NON_SECOND_APRON_SEASON',pick_year=pick,determined_after_season_start_year=year,exact_pick_number=None)
    return dict(status='FROZEN_PENDING_FOUR_YEAR_TEST',pick_year=pick,exact_pick_number=None)


def award_requirement(award,year,minutes,injury_exception=None,challenge_approved=False):
    if year>=2030:return dict(status='FUTURE_CBA_NOT_VERIFIED',count=None,result_selected=False)
    applicable={'MVP','DPOY','MIP','All-NBA','All-Defensive'}
    if award not in applicable or year<2023:return dict(status='65_GAME_RULE_NOT_APPLICABLE',count=None,result_selected=False)
    if minutes is None or any(m is None for m in minutes):return dict(status='MINUTES_UNKNOWN',count=None,result_selected=False)
    if any(m<0 for m in minutes):raise ValueError('negative minutes')
    count=sum(m>=20 for m in minutes)+min(2,sum(15<=m<20 for m in minutes))
    standard=count>=65
    injury=False
    if injury_exception:
        e=injury_exception
        qualified=e.get('qualified_games_before_injury');team=e.get('team_games_before_injury')
        if qualified is not None and qualified>count:raise ValueError('more qualifying games before injury than total')
        if qualified is not None and team is not None and qualified>team:raise ValueError('qualifying games exceed team games')
        injury=count>=62 and e.get('joint_physician_season_ending_confirmed') is True and qualified is not None and team is not None and team>0 and qualified*100>=team*85
    return dict(status='CRITERION_MET_NOT_AWARD_WON' if standard or injury or challenge_approved else 'STANDARD_NOT_MET_EXCEPTION_OR_REVIEW_UNRESOLVED',count=count,standard_met=standard,injury_exception_met=injury,challenge_approved=challenge_approved,result_selected=False,actual_health_certified=False)


def core_cost(p,capcase,price,Ppct):
    cap=capcase['cap'];lmfirst=p['cap_references']['2024']['cap']*price['LaMelo_initial_cap_percent']//100
    lm=contract_salary(lmfirst,5)[2]
    lv=p['LaVine_2022_reference_base'][4] if price['LaVine_path']=='EXERCISE_EXISTING_PLAYER_OPTION' else cap*18//100
    pro=cap*Ppct//100;core=pro+lm+lv;other=cap*sum(p['other_player_role_budget_percent'].values())//100;contingency=cap*p['unallocated_contingency_percent']//100
    players=core+other;envelope=players+contingency
    return dict(cap_case=capcase['id'],price_case=price['id'],P_first_cap_percent=Ppct,cap=cap,P_salary=pro,LaMelo_salary=lm,LaVine_salary=lv,core_salary=core,other_role_budget=other,player_budget=players,unallocated_contingency=contingency,planning_envelope=envelope,original_123pct_envelope=cap*123//100,extra_vs_G2_123pct=envelope-cap*123//100,player_budget_room_to_first=capcase['first']-players,player_budget_room_to_second=capcase['second']-players,full_envelope_room_to_second=capcase['second']-envelope,LaVine_option_minus_18pct_target=p['LaVine_2022_reference_base'][4]-cap*18//100,requires_P_pre_signing_35pct_eligibility=Ppct==35,requires_LaMelo_Higher_Max=price['LaMelo_initial_cap_percent']==30,requires_LaVine_opt_out_and_new_acceptance=price['LaVine_path']!='EXERCISE_EXISTING_PLAYER_OPTION',actual_apron_team_salary=None,actual_player_agreements=False,actual_second_apron_team_selected=False)


def build():
    p=json.loads(INPUT.read_text());base=p['cap_references']['2023'];c2024=p['cap_references']['2024']['cap'];caps=[]
    for g in p['cap_growth_cases_percent']:
        if not 0<=g<=10:raise ValueError('growth outside current CBA smoothing range')
        cap=ceil_fraction(Fraction(c2024*(100+g)**2,10000))
        # Conservative upper-dollar projection from published 2023 levels;
        # exact league rounding/BRI in the fictional world remain unselected.
        caps.append(dict(id='G'+str(g),cap=cap,first=ceil_fraction(Fraction(base['first']*cap,base['cap'])),second=ceil_fraction(Fraction(base['second']*cap,base['cap'])),type='FICTIONAL_GROWTH_STRESS_NOT_FORECAST'))
    caps.append(dict(id='ACTUAL2026_REFERENCE',**p['cap_references']['2026'],type='PUBLIC_REAL_WORLD_REFERENCE_NOT_WORLD_SELECTED'))
    cases=[core_cost(p,c,s,a) for c,s,a in product(caps,p['core_price_cases'],p['P_2026_first_cap_percent_cases'])]
    lmoffers=[]
    for opt in p['LaMelo_offer_options']:
        price_paths=[]
        if opt['years']:
            for pct in sorted({opt['initial_cap_percent'],opt['higher_max_cap_percent_if_qualified']}):
                amounts=contract_salary(c2024*pct//100,opt['years'])
                price_paths.append(dict(initial_percent=pct,annual_salaries=amounts,total=sum(amounts),agreement_and_criteria_verified=False))
        lmoffers.append(dict(**opt,price_paths=price_paths,selected=False))
    actions=[dict(row=r,season_start=y,after_regular=phase,**transaction_apron_limits(r,y,phase)) for r,y,phase in product('ABCDEFGHIJK',(2023,2024),(False,True))]
    award=[dict(**r,rule_check=award_requirement(r['award'],r['season'],r['official_minutes'])) for r in p['award_targets']]
    sample_freezes=[dict(label='2024_ABOVE_TWICE_LATER',result=frozen_pick(2024,True,{'2025':True,'2026':False,'2027':False,'2028':True})),dict(label='2024_THREE_LATER_BELOW',result=frozen_pick(2024,True,{'2025':False,'2026':False,'2027':False})),dict(label='2026_UNKNOWN_WORLD',result=frozen_pick(2026,None,{}))]
    return dict(stage='O-15G9',status='LONG_CORE_COST_AND_2023_CBA_CONDITIONS',recommended_contract_offer='LM1',recommended_budget_case='BC1_P30',cap_cases=caps,core_cases=cases,core_case_count=len(cases),LaMelo_offers=lmoffers,LaVine_reference_annual_base=p['LaVine_2022_reference_base'],LaVine_18pct_is_not_existing_contract_price=True,apron_table_cases=actions,award_targets=award,pick_freeze_examples_only=sample_freezes,actual_future_frozen_picks=[],CBA_after_2030_verified=False,actual_contracts_agreed=False,selected_case=None,author_locked=False,season_selected=False,exact_execution_cleared=False,manuscript_allowed=False,independent_review='NOT_INDEPENDENT')


if __name__=='__main__':
    x=build();OUT.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
    primary=next(r for r in x['core_cases'] if r['cap_case']=='ACTUAL2026_REFERENCE' and r['price_case']=='BC1' and r['P_first_cap_percent']==30)
    print(json.dumps(dict(PASS=True,core_cases=x['core_case_count'],table_cases=len(x['apron_table_cases']),primary_reference={k:primary[k] for k in ['LaVine_salary','LaVine_option_minus_18pct_target','player_budget','planning_envelope','full_envelope_room_to_second']},actual_contracts_agreed=False)))
