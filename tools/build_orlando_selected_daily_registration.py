"""Expand selected contract occupancy across off days; no registration approval."""
import copy,hashlib,json
from datetime import date,timedelta
from pathlib import Path
import build_orlando_2020_21_registration_ledger as ledger
ROOT=Path(__file__).resolve().parents[1]
INPUT='simulation/ORLANDO_2020_21_REGISTRATION_LEDGER.json'
DECISION='canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json'
SOURCE='research/D1_ORLANDO_CALENDAR_SOURCES_2026_10_02.json'
OUT='simulation/ORLANDO_2020_21_SELECTED_DAILY_REGISTRATION.json'

def build(registration=None,decision=None,source=None,root=ROOT):
    load=lambda p:json.loads((root/p).read_text(encoding='utf-8'))
    registration=load(INPUT) if registration is None else registration
    decision=load(DECISION) if decision is None else decision
    source=load(SOURCE) if source is None else source
    assert decision['status']=='AUTHOR_SELECTED_F4_F5_FOLLOWUP_DIRECTIONS_ONLY'
    assert 'does not re-sign Donta Hall on 2021-05-09' in decision['selected']['F4_HALL']
    assert source['visual_table_check'] is True and source['historical_chronology_not_counterfactual_approval'] is True
    assert source['original_contracts_or_league_registration_certified'] is False
    assert len(source['events'])==15 and len({(e['date'],e['player'],e['action']) for e in source['events']})==15
    assert not any(registration[k] for k in ['author_locked','season_selected','manuscript_allowed'])
    contracts_in=registration['contracts']
    assert all(c['type'] in {'STANDARD','TWO_WAY'} for c in contracts_in),'unknown contract class'
    assert all(ledger.START<=c['start']<=c['end']<=ledger.END for c in contracts_in),'invalid contract window'
    baseline=[c for c in contracts_in if c['source']=='CONDITIONAL_CARRY_FORWARD_BASELINE']
    assert len(baseline)==13 and {c['player'] for c in baseline}==set(ledger.BASE_STANDARD),'carry-forward baseline changed'
    assert all(c['type']=='STANDARD' and (c['start'],c['end'])==(ledger.START,ledger.END) for c in baseline),'carry-forward window/class changed'
    games=registration['orl_game_checks']
    assert len(games)==19 and len({g['event_id'] for g in games})==19,'duplicate/missing game IDs'
    assert len({g['event_id'][:10] for g in games})==19,'duplicate game dates'
    assert all(ledger.START<=g['event_id'][:10]<=ledger.END for g in games),'game outside calendar'
    for event in source['events']:
        day,player,action=event['date'],event['player'],event['action']
        kind='TWO_WAY' if 'TWO_WAY' in action else 'STANDARD'
        intervals=[c for c in registration['contracts'] if c['player']==player and c['type']==kind]
        if action.startswith('SIGN_'):
            assert any(c['start']==day for c in intervals),'sign/start disagreement: '+str(event)
        elif action=='SECOND_TEN_DAY':
            assert any(c['start']<day<=c['end'] for c in intervals),'continuation window disagreement'
        elif action.startswith(('RELEASE_','WAIVE_')):
            prior=(date.fromisoformat(day)-timedelta(days=1)).isoformat()
            assert any(c['end']==prior for c in intervals),'release/end disagreement: '+str(event)
            assert not any(c['start']<=day<=c['end'] for c in intervals),'released class remains active'
        else:raise AssertionError('unknown historical action')
    start,end=registration['scope']['start'],registration['scope']['end']
    assert (start,end)==(ledger.START,ledger.END)
    contracts=copy.deepcopy(registration['contracts'])
    omitted=[c for c in contracts if c['player']=='Donta Hall' and c['start']=='2021-05-09']
    assert len(omitted)==1 and omitted[0]['end']==end
    contracts.remove(omitted[0])
    game_dates={r['event_id'][:10]:r for r in registration['orl_game_checks']}
    rows=[];cursor=date.fromisoformat(start)
    while cursor<=date.fromisoformat(end):
        day=cursor.isoformat();roster=ledger.roster_on(day,contracts)
        game=game_dates.get(day)
        roster.update(game_day=game is not None,event_id=game['event_id'] if game else None,
            period='END_OF_DAY_CONDITIONAL_OCCUPANCY_NOT_INTRADAY_LEAGUE_RECEIPT',
            historical_actions=[e for e in source['events'] if e['date']==day],
            selected_omission=[e for e in source['events'] if e['date']==day and e['player']=='Donta Hall' and e['action']=='SIGN_REST_OF_SEASON'])
        assert roster['ordinary_count_pass'] and not roster['registration_cleared']
        assert set(ledger.BASE_STANDARD)<=set(roster['standard'])
        rows.append(roster);cursor+=timedelta(days=1)
    assert len(rows)==35 and sum(r['game_day'] for r in rows)==19
    assert all(len(r['standard'])==15 for r in rows)
    assert 'Donta Hall' not in next(r for r in rows if r['date']=='2021-05-02')['standard']
    assert 'Donta Hall' in next(r for r in rows if r['date']=='2021-05-01')['standard']
    assert all('Donta Hall' not in r['standard'] for r in rows if r['date']>='2021-05-09')
    assert all('Ignas Brazdeikis' in r['standard'] for r in rows if r['date']>='2021-05-02')
    return dict(base_main='6e444eb',scope='2021-04-12_TO_2021-05-16_END_OF_DAY',
        status='CONDITIONAL_DAILY_OCCUPANCY_WITNESS_NOT_LEGAL_BOUND_PASS',
        source_sha256={p:hashlib.sha256((root/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in [INPUT,DECISION,SOURCE]},
        rows=rows,calendar_days=len(rows),game_days=sum(r['game_day'] for r in rows),
        off_days=sum(not r['game_day'] for r in rows),
        standard_count_max=max(r['standard_count'] for r in rows),two_way_count_max=max(r['two_way_count'] for r in rows),
        historical_source_actions=15,selected_omitted_actions=1,selected_retained_actions=14,
        complete_historical_action_inventory_claim='ONLY_TEAM_GUIDE_LISTED_EVENTS',
        complete_counterfactual_domain=False,source_verified_for_full_S2_legal_proof=False,
        legal_registration_cleared=False,exact_salary_cleared=False,health_cleared=False,
        F4_complete=False,season_selected=False,manuscript_allowed=False,author_locked=False)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args();d=build()
    if args.check:assert json.loads((ROOT/OUT).read_text(encoding='utf-8'))==d,'stale calendar witness'
    else:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in d.items() if k not in ['rows','source_sha256']},ensure_ascii=False))
