"""Prove the selected path's registration domain, separately from full cost/execution."""
import argparse
from collections import Counter
import csv
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT='research/ORLANDO_REGISTRATION_LEGAL_DOMAIN_2026_10_05.json'
INPUTS=['simulation/ORLANDO_2021_DEADLINE_TO_FINAL_CALENDAR.json',
        'simulation/ORLANDO_2020_21_PAYROLL_BOUND.json',
        'research/ORLANDO_PUBLIC_EVENT_COVERAGE_2026_10_05.json',
        'simulation/NBA_2020_21_REGULAR_GAME_BASELINE.csv',
        'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json',
        'simulation/ORLANDO_2021_BASELINE_CONTINUITY.json',
        'canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json']
TEN_IDS=('CANNADY_APR06','FRANKS_APR12','HALL_APR13','FRANKS_APR22','HALL_APR23','BRAZDEIKIS_MAY02')


def replay_public_events(coverage, baseline, rows, ten):
    """Replay evidence-backed events; capacity alone cannot justify a new player."""
    events=coverage['events']
    assert len({(e['date'],e['event'],e.get('player')) for e in events})==21
    standard=set(baseline['original_standard_reconstruction'])
    two_way={'Chasson Randle','Karim Mane'}
    sequences=[]; mapped=[]
    for row in rows:
        dated=[e for e in events if e['date']==row['date']]
        # Sources establish the date, not receipt timestamps. This is a lawful
        # order witness: outgoing contracts precede same-day incoming ones.
        dated.sort(key=lambda e:0 if e['event'].startswith(('WAIVE','RELEASE')) else 1)
        operations=[]
        for e in dated:
            key=e['event'];player=e.get('player')
            evidence_id=f"{e['date']}:{key}:{player or ''}"
            before=(len(standard),len(two_way))
            authority=None; action='CARRY_FORWARD_PUBLIC_EVENT'
            if key=='CHI_ORL_TRADE':
                action='OMITTED_UNDER_APPROVED_T2'
                authority=INPUTS[6]+'#T2'
                assert {'Nikola Vucevic','Al-Farouq Aminu'}<=standard
            elif key=='DEN_ORL_TRADE':
                authority=INPUTS[6]+'#T1'
                assert {'Aaron Gordon','Gary Clark'}<=standard
                assert not {'Gary Harris','Zeke Nnaji'}&standard
                standard=(standard-{'Aaron Gordon','Gary Clark'})|{'Gary Harris','Zeke Nnaji'}
                action='APPROVED_T1_HAMPTON_TO_NNAJI_TRANSFORMATION'
            elif key=='BOS_ORL_TRADE':
                authority=INPUTS[6]+'#T3'
                assert 'Evan Fournier' in standard and 'Jeff Teague' not in standard
                standard.remove('Evan Fournier');standard.add('Jeff Teague')
            elif key=='WAIVE_TEAGUE':
                assert 'Jeff Teague' in standard;standard.remove('Jeff Teague')
            elif key=='WAIVE_BIRCH':
                assert 'Khem Birch' in standard;standard.remove('Khem Birch')
            elif key=='SIGN_CANNADY_TEN_DAY':
                assert 'Devin Cannady' not in standard;standard.add('Devin Cannady')
            elif key=='RELEASE_TEN_DAY':
                assert player in standard;standard.remove(player)
            elif key=='WAIVE_TWO_WAY':
                assert player in two_way;two_way.remove(player)
            elif key=='SIGN_TWO_WAY':
                assert player not in two_way|standard;two_way.add(player)
            elif e['date']=='2021-05-09' and player=='Donta Hall':
                assert key=='SIGN_REST_OF_SEASON' and player not in standard
                action='OMITTED_UNDER_APPROVED_F4_HALL'
                authority=INPUTS[4]+'#F4_HALL'
            elif key in ('SIGN_TEN_DAY','SECOND_TEN_DAY','SIGN_REST_OF_SEASON'):
                if player in standard:
                    prior=[c for c in ten if c['player']==player and c['ten_day_end']<e['date']]
                    assert prior and max(c['ten_day_end'] for c in prior)==(date.fromisoformat(e['date'])-timedelta(days=1)).isoformat()
                    standard.remove(player)
                    assert 14<=len(standard)<=15
                    action='TEN_DAY_EXPIRY_BEFORE_RENEWAL'
                else:assert key!='SECOND_TEN_DAY'
                assert player not in two_way
                standard.add(player)
            else:raise AssertionError(f'unmapped published event {e}')
            assert 14<=len(standard)<=15 and len(two_way)<=2 and not standard&two_way
            active=[c for c in ten if c['start']<=row['date']<=c['registration_end'] and c['player'] in standard]
            assert len(active)<={13:1,14:2,15:3}[len(standard)]
            item=dict(evidence_id=evidence_id,source=INPUTS[2]+'#events',author_direction=authority,
                      action=action,standard_counts=[before[0],len(standard)],two_way_counts=[before[1],len(two_way)],
                      ten_day_count=len(active),capacity_pass=True)
            operations.append(item);mapped.append(item)
        assert standard==set(row['standard']) and two_way==set(row['two_way']), f"unexplained roster change on {row['date']}"
        if operations:sequences.append(dict(date=row['date'],order='RELEASE_OR_EXPIRY_BEFORE_SIGNATURE',
                                            evidence_backed_operations=operations,capacity_pass=True,
                                            actual_receipt_time_certified=False))
    assert len(mapped)==21
    return sequences,mapped


def digest(raw):return hashlib.sha256(raw).hexdigest()


def build(cache, *, calendar_override=None):
    import fitz
    cba_raw=(cache/'fr-2017-cba.pdf').read_bytes()
    assert digest(cba_raw)=='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
    pages=[32,69,70,74,292,294,295,296]
    with fitz.open(stream=cba_raw,filetype='pdf') as pdf:
        text={i:pdf[i-1].get_text() for i in pages}
    assert 'eighty percent (80%)' in text[294] and 'twenty percent (120%)' in text[294]
    assert 'two (2) Seasons' in text[292] and 'fourth Season' in text[292]
    assert 'ten (10) days' in text[69] and 'three (3)' in text[69]
    assert 'written notice' in text[70]
    data=[json.loads((ROOT/p).read_text(encoding='utf-8')) for p in INPUTS[:3]]
    calendar,payroll,coverage=data
    if calendar_override is not None:calendar=calendar_override
    assert coverage['defined_public_inventory_reconciled'] is True and coverage['public_event_count']==21
    assert 'HALL_MAY09' not in TEN_IDS
    decision=json.loads((ROOT/INPUTS[4]).read_text(encoding='utf-8'))
    assert decision['selected']['F4_HALL']=='Orlando does not re-sign Donta Hall on 2021-05-09; his April contracts and earlier appearances remain in the alternate ledger.'
    rows=calendar['rows']; assert len(rows)==53
    assert [r['date'] for r in rows]==[(date(2021,3,25)+timedelta(days=i)).isoformat() for i in range(53)]
    assert all('Donta Hall' not in r['standard'] for r in rows if r['date']>='2021-05-09')
    baseline=json.loads((ROOT/INPUTS[5]).read_text(encoding='utf-8'))
    direction=json.loads((ROOT/INPUTS[6]).read_text(encoding='utf-8'))
    assert direction['approved']['T1'].startswith('Denver sends Gary Harris, Zeke Nnaji')
    roster=set(baseline['original_standard_reconstruction']);assert len(roster)==15
    for step in [s for s in baseline['steps'] if s['date']=='2021-03-25']:
        assert set(step['removed']).issubset(roster)
        assert not set(step['added'])&roster
        roster=(roster-set(step['removed']))|set(step['added'])
        assert len(roster)==15 and roster==set(step['standard'])
    assert roster==set(rows[0]['standard']) and {'Nikola Vucevic','Al-Farouq Aminu'}.issubset(roster)
    with (ROOT/INPUTS[3]).open(encoding='utf-8-sig',newline='') as h:
        games=[g for g in csv.DictReader(h) if 'ORL' in (g['home'],g['away'])]
    assert len(games)==72
    last=date.fromisoformat(games[-1]['date']); assert last==date(2021,5,16)
    contracts={c['id']:c for c in payroll['short_contracts']}
    ten=[]; counts=Counter()
    for cid in TEN_IDS:
        c=contracts[cid]; start=date.fromisoformat(c['pay_start']); end=start+timedelta(days=9)
        third=date.fromisoformat([g['date'] for g in games if g['date']>=c['pay_start']][2])
        assert start>=date(2021,2,23) and third<=end<last
        assert c['pay_end']==end.isoformat()
        counts[c['player']]+=1
        ten.append(dict(id=cid,player=c['player'],start=start.isoformat(),ten_day_end=end.isoformat(),
                        third_team_game=third.isoformat(),registration_end=c['registration_end'],
                        compensation_preserved_to=end.isoformat(),duration_and_season_end_pass=True))
    assert max(counts.values())<=2
    sequences,mapped=replay_public_events(coverage,baseline,rows,ten)
    traces=[]
    for i,row in enumerate(rows):
        ordinary=set(row['standard']);tw=set(row['two_way'])
        assert len(ordinary)==row['standard_count'] and 14<=len(ordinary)<=15
        assert len(tw)==row['two_way_count'] and len(tw)<=2 and not ordinary&tw
        assert 'Zeke Nnaji' in ordinary and 'Zeke Nnaji' not in tw
        active=[c for c in ten if c['start']<=row['date']<=c['registration_end']]
        assert all(c['player'] in ordinary for c in active)
        limit={13:1,14:2,15:3}[len(ordinary)]
        assert len(active)<=limit
        traces.append(dict(date=row['date'],game_day=row['game_day'],standard_count=len(ordinary),
                           two_way_count=len(tw),ten_day_count=len(active),ten_day_limit=limit,
                           slot_and_ten_day_capacity_pass=True))
    return dict(schema='ORLANDO_REGISTRATION_LEGAL_DOMAIN_V1',baseline_main='e3ef70bef8b96c7ae79ede6d6cde5a985431118b',
                status='LEGAL_BOUND_PASS_FOR_REGISTRATION_DOMAIN_NOT_FULL_EXECUTION',
                scope='2021-03-25_TO_2021-05-16_CONTRACT_CLASS_DURATION_SLOT_CAPACITY_AND_EVENT_SEQUENCE',
                source_cba=dict(url='https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf',
                                sha256=digest(cba_raw),pdf_pages=pages,
                                page_text_sha256={str(i):digest(t.encode()) for i,t in text.items()}),
                contemporaneous_public_rules=[dict(url='https://gleague.nba.com/news/2020-21-nba-g-league-key-dates',
                                                   published='2021-02-01',observed='2026-10-05',body_read_by='Codex parent and separate collector via web',
                                                   ten_day_start_allowed='2021-02-23',original_html_sha256=None),
                                               dict(url='https://www.nba.com/news/teams-allowed-to-carry-15-players-on-active-roster-for-2020-21-season',
                                                    published='2020-12-18',observed='2026-10-05',body_read_by='Codex parent and separate collector via web',
                                                    active_limit=15,two_way_slots=2,original_html_sha256=None)],
                input_sha256={p:digest((ROOT/p).read_bytes().replace(b'\r\n',b'\n')) for p in INPUTS},
                enforced_legal_domain=dict(nnaji='VALID_FIRST_2020_PICK24_ROOKIE_SCALE_CONTRACT_HELD_AND_ASSIGNED_IN_T1',
                                            current_base_lower='0.8*S24',salary_plus_unlikely_upper='1.2*S24',
                                            nnaji_standard_slots_for_entire_domain=1,exact_120_percent_required=False,
                                            nnaji_contract_loss_or_new_two_way_path_included=False,
                                            signing_and_assignment_eligibility_required=True,
                                            ten_day_and_rest_of_season_salary_at_least_applicable_minimum=True,
                                            early_ten_day_release_by_written_notice=True,
                                            actual_counterfactual_contract_receipt_claimed=False),
                march25_trades=dict(gordon_swap_standard_counts=[15,15],fournier_swap_standard_counts=[15,15],
                                   order_permutations=2,vucevic_trade_omitted=True,transaction_matching_certified=False),
                retained_ten_day_contracts=ten,daily_capacity=traces,event_sequences=sequences,
                reconciled_public_events=mapped,unexplained_roster_changes=0,
                legal_branches=[dict(id=b,verdict='LEGAL_BOUND_PASS') for b in ('game_days','intervening_days','all_other_transactions')],
                registration_domain_complete=True,source_verified_for_registration_domain=True,
                boundaries=dict(whole_salary_or_apron_proof_pass=False,actual_T5_events_author_locked=False,
                                full_F4_pass=False,health_active_list_or_minutes_pass=False,
                                season_selected=False,manuscript_allowed=False))


def self_test(cache):
    from copy import deepcopy
    original=json.loads((ROOT/INPUTS[0]).read_text(encoding='utf-8'))
    cases=[]
    wrong_class=deepcopy(original)
    row=wrong_class['rows'][20]
    row['standard'].remove('Zeke Nnaji');row['standard_count']-=1
    row['two_way']=['Zeke Nnaji'];row['two_way_count']=1
    cases.append(wrong_class)
    hidden_slot=deepcopy(original);row=hidden_slot['rows'][20]
    row['standard'].append('UNLISTED_PLAYER');row['standard_count']+=1
    cases.append(hidden_slot)
    missing_day=deepcopy(original);missing_day['rows'][20]['date']=missing_day['rows'][19]['date']
    cases.append(missing_day)
    unsourced=deepcopy(original);row=unsourced['rows'][20]
    row['standard'].remove('Al-Farouq Aminu');row['standard'].append('UNSOURCED_REPLACEMENT')
    cases.append(unsourced)
    for mutated in cases:
        try:build(cache,calendar_override=mutated)
        except AssertionError:continue
        raise AssertionError('contract class, overcapacity or missing day must block')
    print('Registration domain negative controls PASS: wrong Nnaji class, hidden slot, duplicate/missing day, unsourced replacement at valid capacity')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cache-dir',required=True,type=Path);p.add_argument('--check',action='store_true')
    p.add_argument('--self-test',action='store_true')
    a=p.parse_args()
    if a.self_test:self_test(a.cache_dir)
    d=build(a.cache_dir)
    if a.check:assert json.loads((ROOT/OUT).read_text(encoding='utf-8'))==d
    else:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('53 dates /6 ten-day contracts / event sequences PASS; exact120 not needed; whole cost/F4/season HOLD')
