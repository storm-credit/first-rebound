"""Apply approved deadline directions to a dated fictional execution ledger.

This verifies a finite transaction subscope; roster/health and whole A2 are
separate. Public legal families stay symbolic instead of invented cents.
"""
import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = 'simulation/NBA_2020_21_APPROVED_TRANSACTION_EXECUTION_BRIDGE.json'
MD = OUT[:-5] + '.md'
SELF = 'tools/build_2020_21_approved_transaction_execution_bridge.py'
REGISTER = 'control/CHICAGO_2020_21_D1_S2_REGISTER.json'
SOURCES = [SELF, 'canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json',
           'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json',
           'canon/CLEVELAND_2021_VAREJAO_C2_DECISION.json',
           'simulation/CHICAGO_2021_THEIS_GREEN_TRANSACTION_LEDGER.csv',
           'simulation/2021_WASHINGTON_CHICAGO_PORTLAND_TRANSACTION_CASCADE.md',
           'research/CHI_F1_MATCHING_EXISTENCE_WITNESS_2026_10_07.json',
           'research/DEN_PUBLISHED_RIGHTS_TRANSITION_WITNESS_2026_10_07.json',
           'control/CHICAGO_2020_21_D1_S2_PROTOCOL.md']

def text(p):
    return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')

def sha(p): return hashlib.sha256(text(p).encode()).hexdigest()
def load(p): return json.loads(text(p))

def expected_events():
    directions=load(SOURCES[1]);follow=load(SOURCES[2]);c2=load(SOURCES[3])
    assert directions['status']=='AUTHOR_APPROVED_DIRECTIONS_ONLY'
    assert 'Gary Harris, Zeke Nnaji' in directions['approved']['T1']
    assert 'remains with Orlando' in directions['approved']['T2']
    assert 'Boston route retained' in directions['approved']['T3']
    assert 'Norman Powell remains with Toronto' in directions['approved']['T4']
    assert 'does not re-sign Donta Hall on 2021-05-09' in follow['selected']['F4_HALL']
    assert 'do not execute their 2021-03-25' in follow['selected']['F5_MCGEE']
    assert c2['selected']['route']=='C2_VAREJAO_NO_RETURN_SIGNING'
    names={'GAFFORD':'Daniel Gafford','KORNET':'Luke Kornet','THEIS':'Daniel Theis',
           'GREEN':'Javonte Green','WAGNER':'Moritz Wagner'}
    ledger=list(csv.DictReader(text(SOURCES[4]).splitlines()))
    assert {x['team'] for x in ledger}=={'CHI','WAS','BOS'}
    moves=[]
    for row in ledger:
        for token in row['outgoing_players'].split('|'):
            holders=[x['team'] for x in ledger if token in x['incoming_players'].split('|')]
            assert len(holders)==1 and holders[0]!=row['team']
            moves.append({'player':names[token],'from':row['team'],'to':holders[0]})
    assert len(moves)==5 and len({x['player'] for x in moves})==5
    approved_edges={('Daniel Gafford','CHI','WAS'),('Luke Kornet','CHI','BOS'),
                    ('Daniel Theis','BOS','CHI'),('Javonte Green','BOS','CHI'),
                    ('Moritz Wagner','WAS','BOS')}
    assert {(m['player'],m['from'],m['to']) for m in moves}==approved_edges, 'F1 recipient/source identity differs from the accepted five-player matching family'
    def event(id,date,kind,law,movements=None,retained=None,omitted=None,authority=None):
        return {'id':id,'date':date,'kind':kind,'classification':'FICTIONAL_WORKING_EXECUTION',
                'authority':authority or SOURCES[1], 'legal_family_ids':law,
                'movements':movements or [],'retained':retained or {},'omitted_events':omitted or [],
                'actual_world_receipt_certified':False,'actual_private_terms_selected':None}
    result=[
        event('F1_FIVE_PLAYER_ATOMIC','2021-03-25','ASSIGNMENT',['CHI_TEAM_SALARY','CHI_MATCHING_RULE','BOS_COMPLETE_COST'],moves,
              {'Troy Brown Jr.':'WAS','Gary Trent Jr.':'WAS'},authority=SOURCES[2]),
        event('F2_FOURNIER','2021-03-25','ASSIGNMENT',['BOS_TPE_AND_PICKS','BOS_COMPLETE_COST','ORL_F2_COMPLETE_COST'],
              [{'player':'Evan Fournier','from':'ORL','to':'BOS'}]),
        event('F3_GORDON','2021-03-25','ASSIGNMENT',['DEN_GORDON_PICKS_AND_CHARGE','DEN_COMPLETE_COST','ORL_COMPLETE_COST'],
              [{'player':'Gary Harris','from':'DEN','to':'ORL'},{'player':'Zeke Nnaji','from':'DEN','to':'ORL'},
               {'player':'Aaron Gordon','from':'ORL','to':'DEN'},{'player':'Gary Clark','from':'ORL','to':'DEN'}]),
        event('T2_VUCEVIC_NO_TRADE','2021-03-25','RETAIN',['CHI_TEAM_SALARY','ORL_COMPLETE_COST'],retained={
              'Nikola Vucevic':'ORL','Al-Farouq Aminu':'ORL','Wendell Carter Jr.':'CHI','Otto Porter Jr.':'CHI'},
              omitted=['Historical CHI-ORL Vucevic assignment and its two first-round obligations']),
        event('T4_POWELL_HOOD_RETAIN','2021-03-25','RETAIN',[],retained={'Norman Powell':'TOR','Rodney Hood':'POR','Gary Trent Jr.':'WAS'},
              omitted=['Historical POR-TOR Powell/Hood/Trent assignment']),
        event('F5_MCGEE_NO_TRADE','2021-03-25','OMIT',['DEN_F5_COMPLETE_COST','CLE_COMPLETE_COST','DEN_CLE_DATED_REGISTRATION'],
              retained={'JaVale McGee':'CLE','Isaiah Hartenstein':'DEN'},
              omitted=['McGee/Hartenstein assignment','DEN conditional2023 second toCLE','DEN2027 second toCLE'],authority=SOURCES[2]),
        event('C2_VAREJAO_NO_RETURN','2021-05-04','OMIT',['CLE_COMPLETE_COST','DEN_CLE_DATED_REGISTRATION'],
              omitted=['2021-05-04 Anderson Varejao return contract','2021-05-14 Anderson Varejao follow-up contract'],authority=SOURCES[3]),
        event('F4_HALL_NO_RESIGN','2021-05-09','OMIT',['ORL_COMPLETE_COST','ORL_DATED_REGISTRATION'],
              omitted=['2021-05-09 Donta Hall re-signing'],authority=SOURCES[2])]
    for row in result:
        delta={}
        for move in row['movements']:
            delta[move['from']]=delta.get(move['from'],0)-1
            delta[move['to']]=delta.get(move['to'],0)+1
        row['standard_slot_delta']=delta
        row['atomic_group']='DEADLINE_2021_03_25_PRESERVED_LAWFUL_IMPLEMENTATION' if row['kind']=='ASSIGNMENT' else None
    return result

def build():
    from check_chicago_d1_s2 import evaluate
    register=load(REGISTER);legal=evaluate(register)
    assert all(x=='LEGAL_BOUND_PASS' for x in legal['legal_fields'].values())
    # Do not hash mutable A/K flags as the immutable legal-family identity.
    projection=register['legal_proofs']
    digest=hashlib.sha256(json.dumps(projection,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    restriction=load(SOURCES[6])['date_and_rule_boundary']['after_waiver_restriction']
    assert restriction['six_month_floor']=='2021-09-25'
    return {'schema':'APPROVED_TRANSACTION_EXECUTION_BRIDGE_V1',
            'status':'APPROVED_DIRECTION_DATED_WORKING_EXECUTION_SUBSCOPE',
            'source_rev_sha256':{p:sha(p) for p in SOURCES},
            'legal_projection_sha256':digest,'events':expected_events(),
            'execution_design':{'same_approved_atomic_moves_applied':True,
                'public_cost_and_matching_witnesses_reused':True,
                'financial_implementation':'Reference the lawful implementation within the accepted whole public family; do not choose unsupported bonus cents or certify real consent.',
                'all_public_picks_and_prior_burdens_preserved_as_same_objects':True,
                'Gordon_protection_resolution_family':'research/DEN_PUBLISHED_RIGHTS_TRANSITION_WITNESS_2026_10_07.json',
                'Fournier_named_rights_family':'research/BOS_NAMED_RIGHTS_ASSIGNMENT_WITNESS_2026_10_06.json',
                'F5_new_pick_claims_created':False,
                'Hall_April_contracts_and_appearances_preserved':True,
                'all_other_lawful_baseline_contract_events_preserved':True,
                'after_waiver_restriction':restriction},
            'remaining_whole_A2_connections':['Full dated registration/member join','WAS Bonga rights-to-standard and opening Trent slot','WAS Homesley final signing slot','GSW Hutchison exact landing/operating branch','2021 finite origin/control pick settlement'],
            'authority':{'new_author_lock':False,'whole_A2_complete':False,'whole_K_complete':False,
                         'actual_trade_call_or_consent_certified':False,'actual_financial_terms':None,
                         'actual_future_pick_outputs':None,'season_selected':False,'manuscript_allowed':False}}

def validate(d):
    try:
        current=build()
        return [] if d==current else ['Source, approved event, public-family or authority projection differs from current reproduction']
    except (AssertionError,KeyError,ValueError,OSError) as exc:return [str(exc)]

def render(d):
    rows=['# 2020–21 승인 거래의 날짜별 가상 실행 연결','',
          '승인된 방향을 통과한 법적 가족에 적용한 유한 작업 장부다. [JSON](NBA_2020_21_APPROVED_TRANSACTION_EXECUTION_BRIDGE.json)에 원천 지문·정확 이동·생략을 기록한다. 실제현실 거래 접수나 전체A2 종료를 인증하지 않는다.','',
          '| 사건 | 날짜 | 실행 종류 | 일반계약 자리 변화 |','|---|---|---|---|']
    for e in d['events']:rows.append(f"| {e['id']} | {e['date']} | {e['kind']} | {json.dumps(e['standard_slot_delta'],sort_keys=True)} |")
    rows+=['','F1은 정확5인, Brown·Trent는WAS에 남고 Hutchison을 그 원자거래에 넣지 않는다. F2/F3는 같은 마감일의 별도 수취 경로를 통과한 공통 법적 구조에 연결한다. T2/T4의 생략 양도와 F5 두2R 생략은 실제역사로 복원하지 않는다. C2의 두 계약과 Hall5/9 계약을 생략하지만 Hall4월 계약/출전은 보존한다.','',
           '공개 비용/차지/면제/픽은 기존 전체 가족 증인을 재사용한다. 조건별 합법적 금융 구현을 참조하며 실제bonus·합의·접수·미래순번을 사실로 채우지 않는다. 면제 후 구계약 연장/재협상은6개월과 다른 자격일 중 늦은 날짜까지 제한하며, 일반 신규FA 계약과 동일시하지 않는다.','',
           '## 남은 유한 연결','']+['- '+s for s in d['remaining_whole_A2_connections']]+['',
           '전체 명단·등록과2021픽 결산을 연결하기 전 wholeA2/K/season 승격0이다. PROJECT_FREEZE v0.30 PARTIAL·설계/원고 CLOSED, 원고0.','']
    return '\n'.join(rows)

def self_test(d):
    changes=[('wrong destination',lambda x:x['events'][0]['movements'][0].update(to='CHI')),
             ('restore omitted trade',lambda x:x['events'][5].update(kind='ASSIGNMENT')),
             ('restore Hall resign',lambda x:x['events'][7].update(omitted_events=[])),
             ('move actual date',lambda x:x['events'][2].update(date='2021-03-24')),
             ('claim full A2',lambda x:x['authority'].update(whole_A2_complete=True)),
             ('consent from existence',lambda x:x['authority'].update(actual_trade_call_or_consent_certified=True)),
             ('drop extension floor',lambda x:x['execution_design']['after_waiver_restriction'].update(six_month_floor=None)),
             ('invent pick claim',lambda x:x['execution_design'].update(F5_new_pick_claims_created=True))]
    for name,change in changes:
        candidate=copy.deepcopy(d);change(candidate);assert validate(candidate),name
    from unittest.mock import patch
    actual_reader=text
    def swapped_source(p):
        body=actual_reader(p)
        if p!=SOURCES[4]:return body
        rows=list(csv.DictReader(body.splitlines()))
        for row in rows:
            if row['team']=='WAS':row['incoming_players']='KORNET'
            if row['team']=='BOS':row['incoming_players']='WAGNER|GAFFORD'
        import io
        f=io.StringIO();w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
        return f.getvalue()
    with patch(__name__+'.text',side_effect=swapped_source):
        try:build()
        except AssertionError:pass
        else:raise AssertionError('same-five upstream F1 recipient swap accepted after source SHA refresh')
    return len(changes)+1

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    d=build()
    if a.write:
        (ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (ROOT/MD).write_text(render(d),encoding='utf-8')
    errors=validate(d)
    if a.check:
        errors+=validate(load(OUT))
        if text(MD)!=render(load(OUT)):errors.append('Markdown stale')
    tests=self_test(d) if a.self_test else 0
    print(json.dumps({'current':not errors,'events':len(d['events']),'negative_controls':tests,'whole_A2_complete':False,'errors':errors},ensure_ascii=False))
    if errors:raise SystemExit(1)
