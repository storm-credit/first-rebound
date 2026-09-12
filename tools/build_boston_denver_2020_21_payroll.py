"""Cumulative BOS/DEN commitments and dated roster compatibility, not a league audit."""
import json
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/BOSTON_DENVER_2020_21_PAYROLL_SOURCES.json'
COSTS = ROOT / 'simulation/NBA_2020_21_REGISTRATION_COSTS.json'
MINUTES = ROOT / 'simulation/NBA_2020_21_FINAL859_MINUTES.json'
OUT = ROOT / 'simulation/BOSTON_DENVER_2020_21_PAYROLL.json'


def on_date(row, day):
    return row['start'] <= day <= row['end']


def build(source=None):
    s = json.loads(SOURCE.read_text()) if source is None else source
    costs = json.loads(COSTS.read_text())
    minutes = json.loads(MINUTES.read_text())
    paths = [SOURCE, COSTS, MINUTES] + [ROOT / p for p in s['existing_source_files']]
    ids = {r['id'] for r in s['references']}
    assert len(ids) == len(s['references'])
    ids |= {r['id'] for p in paths[3:] for r in json.loads(p.read_text())['references']}
    assert all(r['source_id'] in ids for r in s['earlier_standard'] + s['camp_stress'])
    result = {}
    for team in ('BOS', 'DEN'):
        core = s['core_players'][team]
        assert len(core) == len({r['player'] for r in core}) == 14
        assert all(r['source_id'] in ids for r in core if r['player'] != 'Saddiq Bey')
        late = [r for r in costs['rows'] if r['team'] == team]
        old = [r for r in s['earlier_standard'] if r['team'] == team]
        twoway = [r for r in s['twoway'] if r['team'] == team]
        roster = [dict(player=r['player'], **s['scope']) for r in core] + old + [
            # Multi-season/rest-season contracts have no termination in this scope.
            dict(player=r['player'], start=r['pay_start'], end=r['registration_end'] or s['scope']['end']) for r in late]
        branches = [b for b in minutes['branches'] if b['team'] == team and on_date(s['scope'], b['date'])]
        positive = sorted({(b['date'], p) for b in branches for p, sec in b['alternate_seconds'].items() if sec > 0})
        conflicts = [dict(date=d, player=p) for d, p in positive if not any(
            on_date(r, d) and r['player'] == p for r in roster + twoway)]
        base = sum(r['base_usd'] for r in core)
        bonus = sum(r['likely_usd'] + r['unlikely_usd'] for r in core)
        prior = sum(r['annual_charge_budget_usd'] for r in old)
        camp = sum(r['annual_base_usd'] for r in s['camp_stress'] if r['team'] == team)
        dates = sorted({s['scope']['start']} | {r['pay_start'] for r in late})
        epochs = []
        for day in dates:
            amount = base + bonus + prior + sum(r['ordinary_minimum_charge_usd'] for r in late if r['pay_start'] <= day)
            epochs.append(dict(date=day, listed_apron_budget_usd=amount,
                               with_camp_annual_stress_usd=amount + camp,
                               residual_allowance_usd=s['limits']['apron_usd'] - amount - camp))
        counts = [dict(date=d, standard=sum(on_date(r, d) for r in roster),
                       twoway=sum(on_date(r, d) for r in twoway)) for d in sorted({d for d, p in positive})]
        result[team] = dict(core_players=core, core_base_usd=base, all_disclosed_bonus_usd=bonus,
                            previous_contract_charge_budget_usd=prior, late_contracts=late,
                            camp_full_annual_stress_usd=camp, epochs=epochs, peak=epochs[-1],
                            mle_used_usd=sum(s['mle_uses'][team].values()),
                            reported_mle_path_implies_apron_limit=sum(s['mle_uses'][team].values()) > s['limits']['taxpayer_mle_usd'],
                            dated_roster_counts=counts, positive_player_dates_checked=len(positive),
                            positive_minute_registration_conflicts=conflicts,
                            complete_other_charge_inventory_verified=False, actual_residual_usd=None,
                            exact_apron_compliance=None, alternate_registration_approved=False)
    return dict(stage='O-15F14-L_BOSTON_DENVER_PAYROLL', baseline_main=s['baseline_main'],
                classification='PUBLIC_CONTRACT_CARRY_FORWARD_BOUND_NOT_EXACT_TEAM_CLEARANCE',
                scope=s['scope'], teams=result, unresolved=s['unresolved_ko'], requirements_closed=0,
                author_locked=False, season_selected=False, manuscript_allowed=False,
                independent_review='NOT_INDEPENDENT',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths})


if __name__ == '__main__':
    r = build()
    OUT.write_text(json.dumps(r, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({t:dict(margin_usd=x['peak']['residual_allowance_usd'],
                             conflicts=len(x['positive_minute_registration_conflicts']),
                             player_dates=x['positive_player_dates_checked']) for t, x in r['teams'].items()}))
