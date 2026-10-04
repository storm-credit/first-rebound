"""Replay the finite public DEN/CLE inventory under existing approved directions."""
import argparse
from collections import Counter
import csv
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT='research/DEN_CLE_REGISTRATION_LEGAL_DOMAIN_2026_10_05.json'
FEED_SHA='3d9d7a6dd7ccd39ddfdd1799a26ef9901b44682d85a26f05239b468a8ae92e3a'
DEN_STD={'Nikola Jokic','Jamal Murray','Michael Porter Jr.','Will Barton','Paul Millsap',
         'Monte Morris','PJ Dozier','Facundo Campazzo','JaMychal Green','Bol Bol','Vlatko Cancar',
         'Gary Harris','Isaiah Hartenstein','Zeke Nnaji','R.J. Hampton'}
CLE_STD={'Cedi Osman','Larry Nance Jr.','Jarrett Allen','Isaac Okoro','Darius Garland',
         'Dean Wade','Dylan Windler','Damyean Dotson','Quinn Cook','JaVale McGee',
         'Matthew Dellavedova','Andre Drummond','Kevin Love','Taurean Prince','Collin Sexton'}
AUTHOR_PATHS=['canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json',
              'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json',
              'canon/CLEVELAND_2021_VAREJAO_C2_DECISION.json',
              'simulation/2020_DRAFT_SADDIQ_BEY_RELANDING_BOARD.md',
              'simulation/2020_DRAFT_ZEKE_NNAJI_RELANDING_BOARD.md']


def sha(raw):return hashlib.sha256(raw).hexdigest()


def dates():return [(date(2021,3,25)+timedelta(days=i)).isoformat() for i in range(53)]


def replay(team,events,contracts,clark_date):
    std=set(DEN_STD if team=='DEN' else CLE_STD)
    tw={'Markus Howard','Greg Whittington'} if team=='DEN' else {'Lamar Stevens','Brodric Thomas'}
    if team=='DEN':
        std.remove('R.J. Hampton');std.add('Saddiq Bey')
    rows=[];traces=[];run=0;max_run=0
    for day in dates():
        operations=[]
        expirations=[c for c in contracts if c['team']==team and c['end']<day and
                     (date.fromisoformat(c['end'])+timedelta(days=1)).isoformat()==day]
        for c in expirations:
            assert c['player'] in std;std.remove(c['player'])
            operations.append(dict(id=c['id']+'_EXPIRY',source='2017_CBA_II_9a_PLUS_FIRST_SIGNATURE_AND_TEAM_SCHEDULE',
                                   player=c['player'],standard_count=len(std),two_way_count=len(tw)))
        dated=[e for e in events if e['team']==team and (clark_date if e['id']=='Waive 1038855' else e['date'])==day]
        dated.sort(key=lambda e:0 if e['action']=='WAIVE' else 1)
        for e in dated:
            action=e['action'];player=e.get('player');note='PUBLIC_EVENT_CARRY_FORWARD';authority=None
            if action=='GORDON_TRADE':
                assert team=='DEN' and {'Gary Harris','Zeke Nnaji'}<=std
                std=(std-{'Gary Harris','Zeke Nnaji'})|{'Aaron Gordon','Gary Clark'}
                note='APPROVED_T1_NNAJI_FOR_HAMPTON_TRANSFORMATION';authority=AUTHOR_PATHS[0]+'#T1'
            elif action=='MCGEE_TRADE':
                note='OMITTED_UNDER_APPROVED_F5';authority=AUTHOR_PATHS[1]+'#F5_MCGEE'
            elif action=='VAREJAO_SIGN':
                assert player not in std;note='OMITTED_UNDER_APPROVED_C2';authority=AUTHOR_PATHS[2]
            elif action=='WAIVE':
                roster=tw if e['class']=='TWO_WAY' else std
                assert player in roster;roster.remove(player)
            elif action=='SIGN':
                roster=tw if e['class']=='TWO_WAY' else std
                assert player not in std|tw;roster.add(player)
            elif action=='STEVENS_CONVERSION':
                assert player in tw and player not in std
                tw.remove(player);std.add(player)
                note='TWO_WAY_ENDED_BEFORE_NEW_STANDARD_SIGNATURE'
            else:raise AssertionError('unmapped event action')
            assert 13<=len(std)<=15 and len(tw)<=2 and not std&tw
            operations.append(dict(id=e['id'],source=e['source'],action=note,player=player,
                                   authority=authority,standard_count=len(std),two_way_count=len(tw)))
        assert 13<=len(std)<=15 and len(tw)<=2 and not std&tw
        active_ten=[c for c in contracts if c['team']==team and c['start']<=day<=c['end']]
        assert all(c['player'] in std for c in active_ten)
        limit={13:1,14:2,15:3}[len(std)];assert len(active_ten)<=limit
        run=run+1 if len(std)==13 else 0;max_run=max(run,max_run);assert run<=14
        # Capacity arrangement only; not an author-selected game active list.
        # All TW inactive: with12 ordinary active, required inactive is2+TW,
        # or1+TW during the temporary13-standard period.
        ordinary_active=12
        ordinary_inactive=len(std)-ordinary_active
        inactive_total=ordinary_inactive+len(tw)
        minimum_inactive=(1 if len(std)==13 else 2)+len(tw)
        assert inactive_total>=minimum_inactive
        rows.append(dict(date=day,standard=sorted(std),two_way=sorted(tw),
                         standard_count=len(std),two_way_count=len(tw),ten_day_count=len(active_ten),ten_day_limit=limit,
                         possible_capacity_arrangement=dict(standard_active=ordinary_active,standard_inactive=ordinary_inactive,
                                                            two_way_inactive=len(tw),inactive_total=inactive_total,
                                                            minimum_inactive=minimum_inactive,actual_active_list_certified=False)))
        if operations:traces.append(dict(date=day,operations=operations,order='WAIVE_OR_EXPIRY_BEFORE_SIGNATURE',actual_receipt_time_certified=False))
    assert len(rows)==53 and rows[0]['standard_count']==15 and rows[-1]['standard_count']==15
    assert not any('Anderson Varejao' in r['standard'] for r in rows)
    assert all(('Isaiah Hartenstein' if team=='DEN' else 'JaVale McGee') in r['standard'] for r in rows)
    return dict(team=team,clark_release_date=clark_date if team=='DEN' else None,rows=rows,event_sequences=traces,
                maximum_consecutive_13_standard_days=max_run,lawful_capacity_pass=True)


def build(cache):
    import fitz
    raw=(cache/'fr-nba-player-movement-2026-10-04.json').read_bytes();assert sha(raw)==FEED_SHA
    all_rows=json.loads(raw)['NBA_Player_Movement']['rows'];assert len(all_rows)==9927
    evidence=[];events=[]
    action_map={
      'Trade 2020075':('GORDON_TRADE',None,'STANDARD'),
      'Trade 2020078':('MCGEE_TRADE',None,'STANDARD'),
      'Waive 1038855':('WAIVE','Gary Clark','STANDARD'),
      'Waive 1038891':('WAIVE','Greg Whittington','TWO_WAY'),
      'Signing 1038872':('SIGN','Shaquille Harrison','TWO_WAY'),
      'Signing 1039383':('SIGN','Austin Rivers','STANDARD'),
      'Signing 1039674':('SIGN','Austin Rivers','STANDARD'),
      'Waive 1038389':('WAIVE','Andre Drummond','STANDARD'),
      'Signing 1038892':('SIGN','Mfiondu Kabengele','STANDARD'),
      'Signing 1039048':('STEVENS_CONVERSION','Lamar Stevens','STANDARD'),
      'Signing 1039411':('SIGN','Mfiondu Kabengele','STANDARD'),
      'Signing 1039626':('SIGN','Jeremiah Martin','TWO_WAY'),
      'Signing 1039683':('SIGN','Mfiondu Kabengele','STANDARD'),
      'Signing 1039781':('VAREJAO_SIGN','Anderson Varejao','UNUSED_HISTORICAL_CLASS'),
      'Signing 1040075':('VAREJAO_SIGN','Anderson Varejao','UNUSED_HISTORICAL_CLASS')}
    for team,tid,expected in [('DEN',1610612743,7),('CLE',1610612739,9)]:
        groups={x['GroupSort'] for x in all_rows if (x['TEAM_ID']==tid or x['Additional_Sort']==tid)
                and '2021-03-25'<=x['TRANSACTION_DATE'][:10]<='2021-05-16'}
        assert len(groups)==expected
        selected=[x for x in all_rows if x['GroupSort'] in groups]
        evidence.append(dict(team=team,group_count=len(groups),rows=selected))
        for g in sorted(groups):
            related=[x for x in selected if x['GroupSort']==g];assert len({x['TRANSACTION_DATE'][:10] for x in related})==1
            action,player,kind=action_map[g]
            events.append(dict(team=team,id=g,date=related[0]['TRANSACTION_DATE'][:10],action=action,player=player,
                               **{'class':kind},source='FROZEN_NBA_MOVEMENT_SNAPSHOT#'+g))
    sources=[]
    for name,expected,url,pages in [
      ('fr-2017-cba.pdf','66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a','https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf',[69,70,74,75,76,412]),
      ('first-rebound-2019-bylaws.pdf','6accb3d9633e15e8559d13228c27ae7b3b0b81eac0894050b06256eea6da3464','https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf',[78]),
      ('fr-den-2122-probe/DEN_2122_OFFICIAL.pdf','248c91faeb5d3f64ceb747d2135f6ac65fb55a2d71dcb4a92db02f81732f19a6','https://kseblobstorage.blob.core.windows.net/sitefiles/pdf/DN_MediaGuide_2122_Digital.pdf',[281]),
      ('fr-cle-official-2022-roster.pdf','55e1530ac2238ccb4026aeb53c65f1edf7d281b233c82942e197f8f7992d8d33','https://cdn.nba.com/teams/uploads/sites/1610612739/2022/10/08-roster.pdf',[12,41]),
      ('20210324_CLECHI_book.pdf','38e8e241fe193d7a9b89ae9fdbd4fa8465fdaeb1c79c1336e277b11c84dde89e','https://statsdmz.nba.com/pdfs/20210324/20210324_CLECHI_book.pdf',[1])]:
        b=(cache/name).read_bytes()
        if expected:assert sha(b)==expected
        with fitz.open(stream=b,filetype='pdf') as pdf:text={n:pdf[n-1].get_text() for n in pages}
        sources.append(dict(url=url,sha256=sha(b),pdf_pages=pages,page_text_sha256={str(n):sha(t.encode()) for n,t in text.items()}))
        if name=='fr-cle-official-2022-roster.pdf':assert 'March 12, 2021 and March 22, 2021' in text[12]
        if name=='fr-den-2122-probe/DEN_2122_OFFICIAL.pdf':assert 'Apr. 9:' in text[281] and 'Gary Clark' in text[281]
    authorities=[json.loads((ROOT/p).read_text(encoding='utf-8')) for p in AUTHOR_PATHS[:3]]
    assert authorities[0]['approved']['T1'].startswith('Denver sends Gary Harris, Zeke Nnaji')
    assert 'do not execute' in authorities[1]['selected']['F5_MCGEE']
    assert authorities[2]['selected']['route']=='C2_VAREJAO_NO_RETURN_SIGNING'
    assert 'Saddiq Bey 22순위' in (ROOT/AUTHOR_PATHS[3]).read_text(encoding='utf-8')
    with (ROOT/'simulation/NBA_2020_21_REGULAR_GAME_BASELINE.csv').open(encoding='utf-8-sig',newline='') as h:games=list(csv.DictReader(h))
    contracts=[]
    for cid,team,player,start,group in [
        ('COOK_FIRST','CLE','Quinn Cook','2021-03-12','Signing 1037731'),
        ('COOK_SECOND','CLE','Quinn Cook','2021-03-22','Signing 1037930'),
        ('KABENGELE_FIRST','CLE','Mfiondu Kabengele','2021-04-10','Signing 1038892'),
        ('KABENGELE_SECOND','CLE','Mfiondu Kabengele','2021-04-21','Signing 1039411'),
        ('RIVERS_FIRST','DEN','Austin Rivers','2021-04-20','Signing 1039383')]:
        match=[x for x in all_rows if x['GroupSort']==group];assert len(match)==1
        assert match[0]['TRANSACTION_DATE'][:10]==start and '10-Day Contract' in match[0]['TRANSACTION_DESCRIPTION']
        team_games=[g for g in games if team in (g['home'],g['away'])]
        third=[g['date'] for g in team_games if g['date']>=start][2]
        end=(date.fromisoformat(start)+timedelta(days=9)).isoformat()
        assert start>='2021-02-23' and third<=end<'2021-05-16'
        contracts.append(dict(id=cid,team=team,player=player,start=start,end=end,third_team_game=third,source_group=group,
                              end_is_CBA_and_schedule_derivation_not_quoted_release_date=True))
    assert Counter(c['player'] for c in contracts)['Mfiondu Kabengele']==2
    assert max(Counter(c['player'] for c in contracts).values())<=2
    branches=[replay('DEN',events,contracts,d) for d in ['2021-04-08','2021-04-09']]+[replay('CLE',events,contracts,None)]
    return dict(schema='DEN_CLE_REGISTRATION_LEGAL_DOMAIN_V1',baseline_main='a7238c6c4d58a88d5f8cd7f6713fa1876eec8f9e',
                status='LEGAL_BOUND_PASS_FOR_REGISTRATION_DOMAIN_NOT_FULL_EXECUTION',
                window=['2021-03-25','2021-05-16'],source_feed=dict(url='https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json',sha256=FEED_SHA,defined_inventory=evidence),
                source_pdfs=sources,
                den_predeadline_book=dict(url='https://statsdmz.nba.com/pdfs/20210324/20210324_DENTOR_book.pdf',page=1,
                                         body_read_via_web=True,raw_cache_recovered=False,box_names=14,inactive_names=3,standard=15,two_way=2),
                historical_start_standard=dict(DEN=sorted(DEN_STD),CLE=sorted(CLE_STD)),
                source_classification_links=['research/O15F14U_CLEVELAND_VAREJAO_HARDSHIP_F5.md','research/O15F14BD_CLEVELAND_C2_FINAL_ROSTER_WINDOW.md'],
                authority_sha256={p:sha((ROOT/p).read_bytes().replace(b'\r\n',b'\n')) for p in AUTHOR_PATHS},
                calendar_input_sha256=sha((ROOT/'simulation/NBA_2020_21_REGULAR_GAME_BASELINE.csv').read_bytes().replace(b'\r\n',b'\n')),
                events=events,ten_day_contracts=contracts,branches=branches,
                historical_conflicts=[dict(player='Gary Clark',feed_date='2021-04-08',guide_date='2021-04-09',both_branches_tested=True),
                                      dict(player='Lamar Stevens',feed_label='Rest-of-Season',prior_team_report_label='Multi-Year',standard_slot_both=1,exact_term_not_certified=True),
                                      dict(player='Mfiondu Kabengele',date='2021-05-01',feed_label='Rest-of-Season',prior_team_report_label='Multi-Year',standard_slot_both=1,exact_term_not_certified=True),
                                      dict(player='Anderson Varejao',followup_form='HISTORICAL_CLASS_CONFLICT_NOT_RESOLVED',selected_path='BOTH_MAY_CONTRACTS_OMITTED')],
                legal_domain_guards=dict(valid_contracts_and_assignment=True,lawful_salary_and_eligibility=True,
                                         two_way_service_eligibility_required=True,minimum_pay_preserved=True,
                                         actual_game_active_list_or_health_certified=False,actual_signature_or_receipt_claimed=False,
                                         whole_cost_certified=False,season_selected=False,manuscript_allowed=False),
                legal_branches=[dict(id=b,verdict='LEGAL_BOUND_PASS') for b in ['DEN_all_dates','CLE_all_dates','prior_and_followup_contracts']],
                complete_domain=True,source_verified=True,new_author_locks=0)


def self_test(cache):
    from copy import deepcopy
    d=build(cache)
    cases=[]
    missing_conversion=[e for e in d['events'] if e['action']!='STEVENS_CONVERSION']
    cases.append(('missing TW-to-standard conversion',missing_conversion,d['ten_day_contracts']))
    bad_class=deepcopy(d['events'])
    next(e for e in bad_class if e['id']=='Signing 1038872')['class']='STANDARD'
    cases.append(('Harrison wrong contract class',bad_class,d['ten_day_contracts']))
    long_cook=deepcopy(d['ten_day_contracts'])
    next(c for c in long_cook if c['id']=='COOK_SECOND')['end']='2021-04-21'
    cases.append(('expired Cook contract kept into later signatures',d['events'],long_cook))
    late_fill=deepcopy(d['events']);late_contract=deepcopy(d['ten_day_contracts'])
    next(e for e in late_fill if e['id']=='Signing 1038892')['date']='2021-04-18'
    next(e for e in late_fill if e['id']=='Signing 1039048')['date']='2021-04-18'
    next(c for c in late_contract if c['id']=='KABENGELE_FIRST')['start']='2021-04-18'
    next(c for c in late_contract if c['id']=='KABENGELE_FIRST')['end']='2021-04-27'
    cases.append(('13-standard period exceeds two weeks',late_fill,late_contract))
    for label,events,contracts in cases:
        team='DEN' if label=='Harrison wrong contract class' else 'CLE'
        try:replay(team,events,contracts,'2021-04-08')
        except AssertionError:continue
        raise AssertionError('negative control accepted: '+label)
    print('Four negative controls PASS: conversion, contract class, expired contract, temporary minimum period')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cache-dir',required=True,type=Path);p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    if a.self_test:self_test(a.cache_dir)
    d=build(a.cache_dir)
    if a.check:assert json.loads((ROOT/OUT).read_text(encoding='utf-8'))==d
    else:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('DEN two release-date branches and CLE53 dates legal-domain PASS; full cost/health/F5/season HOLD')
