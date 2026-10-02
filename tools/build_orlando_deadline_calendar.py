"""Join the conditional March baseline to the existing April-May witness."""
import copy, hashlib, json
from datetime import date, timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INPUTS=['simulation/ORLANDO_2021_BASELINE_CONTINUITY.json','simulation/ORLANDO_2020_21_SELECTED_DAILY_REGISTRATION.json']
OUT='simulation/ORLANDO_2021_DEADLINE_TO_FINAL_CALENDAR.json'
def build(base=None,late=None):
    if base is None: base=json.loads((ROOT/INPUTS[0]).read_text(encoding='utf-8'))
    if late is None: late=json.loads((ROOT/INPUTS[1]).read_text(encoding='utf-8'))
    assert all(base[k] is False for k in ['complete_domain','source_verified','legal_execution_cleared','season_selected','manuscript_allowed'])
    assert all(late[k] is False for k in ['complete_counterfactual_domain','source_verified_for_full_S2_legal_proof','legal_registration_cleared','season_selected','manuscript_allowed'])
    prior=set(base['original_standard_reconstruction'])
    previous_date='2021-03-25'
    for step in base['steps']:
        assert previous_date<=step['date']<'2021-04-12', 'step chronology'
        previous_date=step['date']
        removed,added=step['removed'],step['added']
        assert len(removed)==len(set(removed)) and len(added)==len(set(added)), 'duplicate transition'
        assert set(removed).issubset(prior), 'removing absent player'
        assert not set(added)&(prior-set(removed)), 'adding existing player'
        expected=(prior-set(removed))|set(added)
        assert len(step['standard'])==len(set(step['standard'])), 'duplicate snapshot'
        assert expected==set(step['standard']), 'snapshot disagrees with transition'
        assert step['standard_count']==len(expected)<=15, 'snapshot count'
        prior=expected
    steps=base['steps']; standard=None; rows=[]; day=date(2021,3,25)
    while day<date(2021,4,12):
        iso=day.isoformat()
        for step in steps:
            if step['date']==iso: standard=step['standard']; carry_from=iso
        assert standard is not None
        names=sorted(standard)
        assert len(names)==len(set(names)) and len(names)<=15
        rows.append(dict(date=iso,standard=names,two_way=['Chasson Randle','Karim Mane'],standard_count=len(names),two_way_count=2,period='END_OF_DAY_CONDITIONAL_OCCUPANCY_NOT_INTRADAY_LEAGUE_RECEIPT',registration_cleared=False,game_day=None,derivation='CONDITIONAL_BASELINE_CARRY_FORWARD',carry_from_date=carry_from,carry_span_days=(day-date.fromisoformat(carry_from)).days))
        day+=timedelta(days=1)
    # Franks is the sole named transition at the join; compare identities, not counts.
    assert 'Robert Franks' not in rows[-1]['standard'] and len(rows[-1]['standard'])<15
    assert set(rows[-1]['standard'])|{'Robert Franks'}==set(late['rows'][0]['standard'])
    assert set(rows[-1]['two_way'])==set(late['rows'][0]['two_way'])
    rows+=copy.deepcopy(late['rows'])
    assert len(rows)==53
    assert rows[0]['date']=='2021-03-25' and rows[-1]['date']=='2021-05-16'
    for row in rows:
        ordinary,tw=row['standard'],row['two_way']
        assert len(ordinary)==len(set(ordinary))<=15, 'ordinary uniqueness/capacity'
        assert len(tw)==len(set(tw))<=2, 'two-way uniqueness/capacity'
        assert not set(ordinary)&set(tw), 'dual contract class'
        assert row['standard_count']==len(ordinary) and row['two_way_count']==len(tw), 'row count mismatch'
        assert row['registration_cleared'] is False, 'false registration promotion' 
    for a,b in zip(rows,rows[1:]):
        assert date.fromisoformat(b['date'])-date.fromisoformat(a['date'])==timedelta(days=1)
    assert all(set(base['retained_zero_minute_contracts']).issubset(r['standard']) for r in rows)
    assert rows[18:]==late['rows']
    return dict(status='CONDITIONAL_53_DAY_OCCUPANCY_NOT_LEGAL_BOUND_PASS',scope='2021-03-25_TO_2021-05-16_END_OF_DAY',rows=rows,calendar_days=53,newly_explicit_dates=18,existing_dates_preserved=35,early_game_day_classification='NOT_CHECKED',source_sha256={p:hashlib.sha256((ROOT/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in INPUTS},complete_domain=False,source_verified=False,legal_execution_cleared=False,season_selected=False,manuscript_allowed=False)
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();d=build()
    if a.check: assert json.loads((ROOT/OUT).read_text(encoding='utf-8'))==d
    else: (ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('53 contiguous dates; 18 early dates; 35 existing rows preserved; Franks identity join PASS; legal HOLD')
