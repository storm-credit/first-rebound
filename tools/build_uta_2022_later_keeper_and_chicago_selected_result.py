"""Late-date selected legal-contract continuation and working role/result; no ancestor build."""
from __future__ import annotations
import argparse,csv,io,json,hashlib
from pathlib import Path
from copy import deepcopy
from collections import Counter
from datetime import date,timedelta
from fractions import Fraction
from unittest.mock import patch
import build_nyk_2021_keeper_and_chicago_selected_results as base
import build_chicago_detroit_2021_two_date_selected_bpm_results as det
ROOT=Path(__file__).resolve().parents[1]
need=base.need;sha=base.sha;text=base.text;physical=base.physical
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
def direct(root,p):
    t=(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
    return json.loads(t)if p.endswith('.json')else list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else t
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
SOURCE_MEANING_SHA={'simulation/NBA_2021_22_COMMON_26_OPPONENT_CAPACITY.json': '83a8033265a23be22a002465467225c02e20e56482be8703f2e9f0a46fc23805', 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json': '12456392c139ca9dbb71070e0a574d633728691d477eada592fd03cefc535cb9', 'simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json': '353acb80f6b12e4b67e2cc0cf56ab4f6551cc70efb63b20cf9febc9db21f0c33', 'simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json': '426de339ff1a1270eb41ed6b81caee8e10099e55e2176c4e9f31bd196da853d5', 'simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json': 'b42cfb6e0b895fb6a70eb1a9e32798eb0cda27b98a659b6e4e6fce85a7d431f7', 'canon/DELEGATED_2021_22_CHICAGO_AVAILABILITY_DECISION_2026_10_07.json': '963c5b9d2967f70cf5770349df39f44f88878e4a3e884b7e0c3c103d7699c6be', 'simulation/CHICAGO_2021_22_CALENDAR.csv': '1c6d8cf8284dc3f88c0d6c7a2a7927f6ba0eb756fbf367da2a44fbfb402e7f68', 'simulation/NBA_2021_22_REGULAR_BASELINE.csv': '8d07a7ba2485a7a0fceeeb2ccfff7acfa1db394f4918459ec4fe30caef2bc4e6', 'simulation/CHICAGO_2020_21_BPM_MAR25_SNAPSHOT.csv': '1ef4eee6a701658c28db8fc611cab263ef8f83936b5badceb45415d35323bfd8', 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS.json': '04d2919b0c1525d0c00d40f7974e8fefd41ed931a1a18495f01b99d98270c317', 'tools/build_chicago_detroit_2021_two_date_selected_bpm_results.py': 'ef289a00d1d7394fefdc6c2d82b535c998f87b6978cddf06fd93319967ebc191', 'tools/build_nyk_2021_keeper_and_chicago_selected_results.py': '01c418a67b2345e60944e90fa602f8644d4bbefeb3456a25cbd0600ef53e9194', 'simulation/CHICAGO_UTAH_2021_SELECTED_KEEPER_RESULT.json': '4d0981b4b75a3e18d0611e1b18529460326316ff810f3a37951cbe6f679feb4a'}

def sources(root):return {p:physical(root,p)for p in PINS}
SELF='tools/build_uta_2022_later_keeper_and_chicago_selected_result.py';OUT='simulation/CHICAGO_UTAH_2022_LATER_SELECTED_KEEPER_RESULT.json';MD=OUT[:-5]+'.md';TEAM='UTA';NAME='UTAH';PARENT='simulation/CHICAGO_UTAH_2021_SELECTED_KEEPER_RESULT.json';GID='0022101041'
PINS[PARENT]='0e2bb3a05a9e562872dcdb411f061693d55d8bfa408a9f8c7927a1a65eb8fc77'
BASELINE='95641e53eec6035a750611e00292e422e331144e'
ROLE_MINUTES={'PG': {'Mike Conley': 30, 'Jordan Clarkson': 12, 'Joe Ingles': 6}, 'SG': {'Donovan Mitchell': 34, 'Jordan Clarkson': 14}, 'SF': {'Bojan Bogdanovic': 32, 'Joe Ingles': 16}, 'PF': {"Royce O'Neale": 30, 'Georges Niang': 14, 'Joe Ingles': 2, 'Ersan Ilyasova': 2}, 'C': {'Rudy Gobert': 32, 'Derrick Favors': 14, 'Ersan Ilyasova': 2}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG': 'Mike Conley', 'SG': 'Donovan Mitchell', 'SF': 'Bojan Bogdanovic', 'PF': "Royce O'Neale", 'C': 'Rudy Gobert'}
ROLE_SHA='5256babdb9f867fbb96abc15b7b610fd936b109459268cbfa883d0d490e116ce'
STANDARD=['Bojan Bogdanovic', 'Derrick Favors', 'Donovan Mitchell', 'Elijah Hughes', 'Ersan Ilyasova', 'Georges Niang', 'JT Thor', 'Joe Ingles', 'Jordan Clarkson', 'Juwan Morgan', 'Mike Conley', 'Miye Oni', "Royce O'Neale", 'Rudy Gobert', 'Udoka Azubuike']
ACTIVE=['Bojan Bogdanovic', 'Derrick Favors', 'Donovan Mitchell', 'Elijah Hughes', 'Ersan Ilyasova', 'Georges Niang', 'Joe Ingles', 'Jordan Clarkson', 'Juwan Morgan', 'Mike Conley', "Royce O'Neale", 'Rudy Gobert']
POLICY={'contract_interval': 'Previously selected 2021 valid UPCs explicitly continued through this consumed late date until June30,2022 or later statedterm, all prior Gamma preserved; no new transaction or fake tender', 'original_actors_retained': 'No originalJanuaryACL_InglesPORT/FavorsOKC/NiangPHI/PaschallGayWhitesideUTA copied', 'selected_health': 'Late March16 positive10 including Ingles24/Conley30 available as new working recovery family, not historicalACL absence/actualposttrade roster', 'current_primary_prior_cutoff': '2021-03-25', 'result_policy': 'SingleBPM EB prior, currentM1/selectedhealth, home2/b2b0.5; no actualNBApoints/automaticOT', 'clinical_or_actual_receipts_certified': False}
POLICY_FIXED=deepcopy(POLICY)
def role_blocks():
    rem={r:{p:m//2 for p,m in ps.items()}for r,ps in ROLE_MINUTES.items()};roles=list(rem);out=[]
    for i in range(24):
        if i==0:a=deepcopy(STARTERS)
        else:
            total=Counter()
            for ps in rem.values():total.update(ps)
            forced={p for p,v in total.items()if v==24-i}
            def find(k,a):
                if k==5:return a if forced<=set(a.values())else None
                r=roles[k]
                for p in sorted(rem[r],key=lambda p:(p not in forced,-rem[r][p],p)):
                    if rem[r][p]>0 and p not in a.values():
                        b=find(k+1,{**a,r:p})
                        if b:return b
                return None
            a=find(0,{})
        need(a is not None,'Five-player role matching unavailable')
        for r,p in a.items():need(rem[r].get(p,0)>0,'Role remainder invalid');rem[r][p]-=1
        out.append({'start_second':i*120,'end_second':(i+1)*120,'seconds':120,'positions':a})
    need(all(v==0 for ps in rem.values()for v in ps.values()),'Role minutes incomplete');return out

def assert_roles(blocks):
    need(ROLE_MINUTES==ROLE_FIXED and digest(blocks)==ROLE_SHA,'Selected chronology changed');seconds=Counter();rs={r:Counter()for r in ROLE_FIXED}
    for i,b in enumerate(blocks):
        need((b['start_second'],b['end_second'],b['seconds'])==(i*120,(i+1)*120,120)and len(set(b['positions'].values()))==5,'Clock/identity invalid')
        for r,p in b['positions'].items():seconds[p]+=120;rs[r][p]+=120
    need(dict(rs)=={r:Counter({p:m*60 for p,m in ps.items()})for r,ps in ROLE_FIXED.items()}and sum(seconds.values())==14400,'Role/source budget changed');return seconds

def continuation(parent):
    rows=deepcopy(parent['lawful_contract_family'])
    for x in rows:x['explicit_working_term_continued_to_this_late_date']=True
    return rows

def build(root=ROOT):
    src=sources(root)
    for p,h in PINS.items():need(sha(root/p)==h and src[p]==direct(root,p) and digest(src[p])==SOURCE_MEANING_SHA[p],'Returned late-source semantic differs '+p)
    need(POLICY==POLICY_FIXED,'Selected operating policy altered')
    parent=src[PARENT];contracts=continuation(parent)
    expected=deepcopy(parent['lawful_contract_family'])
    for x in expected:x['explicit_working_term_continued_to_this_late_date']=True
    need(contracts==expected and {x['player']for x in contracts}==set(STANDARD),'Returned late contract continuation changed')
    need(len(STANDARD)==15 and 12<=len(ACTIVE)<=15 and set(ACTIVE)<=set(STANDARD),'Late registration minimum/identity altered')
    blocks=role_blocks();seconds=assert_roles(blocks)
    need(set(seconds)<=set(ACTIVE),'Late positive unavailable/inactive')
    inactive=sorted(set(STANDARD)-set(ACTIVE));need(len(inactive)==15-len(ACTIVE),'Late inactive partition changed')
    g=next(x for x in src[det.CAL]if x['game_id']==GID);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==GID)
    need(g['opponent']==TEAM and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact late date/state changed')
    c=next(x for x in src[base.CHI]['rows']if x['game_id']==GID and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHIhealth changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':ACTIVE};pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint[TEAM]=joint.pop('NYK')
    for x in pair:x[TEAM]=x.pop('NYK')
    need(not(set(joint['CHI'])&set(joint[TEAM])) and set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'Shared actor/inactive positive')
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Canonical health source changed')
    names=set(joint['CHI'])|set(joint[TEAM]);rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Moses Moody'})
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    if 'Moses Moody'in names:
        rates['Moses Moody']=deepcopy(parent['selected_ratings']['Moses Moody']);need(Fraction(rates['Moses Moody']['exact_fraction'])==Fraction(-728,1145),'Existing rookie prior changed')
    for p in set(rates)&set(parent['selected_ratings']):need(rates[p]==parent['selected_ratings'][p],'Late productivity source altered')
    impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back[TEAM])-int(back['CHI']));margin=impact['CHI']-impact[TEAM]+home+fatigue;need(margin!=0,'Tie requires separately selected OT')
    game={'game_id':GID,'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_opponent_impact_fraction':str(margin),'CHI_minus_opponent_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else TEAM,'score':None,'overtime_selection':None}
    return {'id':OUT.split('/')[-1][:-5],'baseline_main':BASELINE,'status':'SELECTED_NAMED_LATE_DATE_CONTINUATION_RESULT_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'selected_policy':deepcopy(POLICY),'previously_reviewed_primary_support':deepcopy(parent['primary_support']),'lawful_contract_continuation':contracts,'six_cost_categories':deepcopy(parent.get('six_cost_categories',parent.get('six_cost_categories_preserved_symbolically'))),'cap_admissibility':deepcopy(parent.get('cap_admissibility',parent.get('cap_admissibility_proof'))),'unsigned_prior_claims':deepcopy(parent.get('unsigned_second_round_family',{'RSC_JTThor30_ALREADY_SIGNED':True})),'selected_registration':{'standard':STANDARD,'TW':[],'STD':15,'TW_count':0,'active':ACTIVE,'inactive':inactive,'positive_operational_available':sorted(seconds),'zero_minutes_clinical_status':None,'all_original_Gamma_preserved':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':[game],'summary':{'selected_games':1,'CHI_wins':int(margin>0),'opponent_wins':int(margin<0),'STD':15,'TW':0,'active':len(ACTIVE),'positive':len(seconds),'blocks':24,'clock_seconds':2880,'player_seconds':14400},'remaining_ports':['Any laterdate/newcontract/actor/health needs its own selected family; not wholesale-year assumption.','Global1148nonCHI outcomes/standings/picks remain separate nextmodelconsumer.'],'certification':{'selected_working_lawful_contract_continuation_and_health_role_result':True,'independent_review_completed':False,'actual_private_receipts_foreign_or_clinical_certified':False,'whole_private_team_cost':False,'actual_original_future_events_absent_certified':False,'new_author_lock':False,'whole82_or_macro3_certified':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    g=d['selected_games'][0]
    lines=[f'# {TEAM} 후반 날짜 keeper·선택 결과','',f"{g['date']} {GID} ·CHI {g['CHI_state']}·승자 {g['selected_regulation_winner']}·CHI 영향/100 {g['CHI_minus_opponent_impact_per100']:.9f}. 독립 검문 대기.",'','새거래/새계약가격을선택하지않고 기존검문된15STD0TW·법적UPC가해당후반날짜까지유효한가상연속가족을명시채택. 원term/보호/보너스Γ·FA/waiver/camp/stretch/unsigned/exception계수와법적예외증인을그대로carry, 사적완전원장·실제수락·이벤트부재인증0.','',POLICY['original_actors_retained'],POLICY['selected_health'],'',f'원 계약·원근거·선택권리: [동결 선행가족](../{PARENT}). 새후반역할은 source분/5자리/24×120순서의 별도실제검문대상이며선행첫날짜의 건강을시즌전체로소급확대하지않는다.','',str(ROLE_FIXED),'',f"15STD0TW·active{len(ACTIVE)}·양수{d['summary']['positive']}·각2880clock/14400선수초. CurrentCHI Mark32/Caruso18/P32·canonhealth·March25EB/BPM·홈2/연전.5. 현재생산성가상계수는역사실제2022능력아님. score/OTnull·원NBA결과복사0.",'','## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020드래프트|완료|','|2|2020–21|완료|',f'|3|2021–23|{TEAM}후반1선택·검문대기|','|4|장기커리어|미완|','|5|결말·구조|미완|','|6|집필규격·Pack|현행등록기·Pack0|','|7|통합·최종승인|CLOSED|','','[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은큰묶음5/6번까지4·v0.30 PARTIAL/CLOSED/원고0.','']
    return '\n'.join(lines)
def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved late result differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    old=role_blocks
    def wrong():
        x=old();x[6]['positions'],x[8]['positions']=x[8]['positions'],x[6]['positions'];return x
    with patch(__name__+'.role_blocks',wrong):
        try:build()
        except ValueError:return ['RETURNED_SAME_TOTAL_ROLE_CHRONOLOGY']
        else:raise AssertionError('FalsePASS returned chronology')
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'Late currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_opponent_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None}))
if __name__=='__main__':main()
