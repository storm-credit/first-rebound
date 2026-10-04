"""Reconcile a finite public event inventory; never prove secret-event absence."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEED = 'research/NBA_MOVEMENT_WINDOW_EVIDENCE_2026_10_04.json'
RELEASES = 'research/ORLANDO_ORIGINAL_RELEASE_CROSSCHECK_2026_10_04.json'
OUT = 'research/ORLANDO_PUBLIC_EVENT_COVERAGE_2026_10_05.json'
GUIDE_SHA = '63550e97068a14cbd60d8b461d1f15c0bb898652c9813fdbfa113509f5a8f92c'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def reconcile(feed, releases, guide_pages):
    """Guide entries are transcribed observations, checked against frozen pages."""
    early = [
        ('2021-03-25', 'CHI_ORL_TRADE', 'Trade 2020065', 'Acquire Wendell Carter Jr., Otto Porter Jr.'),
        ('2021-03-25', 'DEN_ORL_TRADE', 'Trade 2020075', 'R.J. Hampton, Gary Harris and a future first round draft pick from Denver'),
        ('2021-03-25', 'BOS_ORL_TRADE', 'Trade 2020077', 'draft picks and Jeff Teague from Boston'),
        ('2021-03-27', 'WAIVE_TEAGUE', 'Waive 1038409', 'Waive Jeff Teague.'),
        ('2021-04-06', 'SIGN_CANNADY_TEN_DAY', 'Signing 1038773', 'Devin Cannady to a 10-day contract.'),
        ('2021-04-08', 'WAIVE_BIRCH', 'Waive 1038858', 'Waive Khem Birch.'),
    ]
    page116 = ' '.join(guide_pages[116].split())
    # The final dated entry in this window precedes June 5 on page 117.
    page117 = ' '.join(guide_pages[117].split())
    assert 'May 12, 2021' in page117 and 'June 5, 2021' in page117
    public = []
    for day, event, group, marker in early:
        assert marker in page116, 'guide observation missing: ' + event
        matches = [r for r in feed['orlando']['related_rows'] if r['GroupSort'] == group]
        assert matches and all(r['TRANSACTION_DATE'][:10] == day for r in matches)
        public.append(dict(date=day, event=event, printed_page=229, feed_groups=[group],
                           resolution='GUIDE_FEED_DATE_AND_EVENT_RECONCILED'))
    release_by_key = {(r['date'], r['player']): r for r in releases['events']}
    for row in feed['orlando']['comparison']:
        event = row['guide_event']
        record = dict(date=event['date'], event=event['action'], player=event['player'],
                      printed_page=event['printed_page'], feed_groups=row['feed_groups'])
        state = row['status']
        if state == 'DATE_PLAYER_ACTION_MATCH':
            record['resolution'] = 'GUIDE_FEED_DATE_AND_EVENT_RECONCILED'
        else:
            original = release_by_key.get((event['date'], event['player']))
            assert original and original['source_fact_verified'] is True
            assert original['prior_feed_status'] == state
            if state == 'GUIDE_ONLY_EVENT_NOT_DELETED':
                assert event['action'] == 'RELEASE_TEN_DAY' and not row['feed_groups']
                record['resolution'] = 'GUIDE_RELEASE_CONFIRMED_BY_ORIGINAL_TEAM_BODY'
            elif state == 'CONTRACT_CLASS_CONFLICT':
                assert (event['date'], event['player'], event['action']) == (
                    '2021-05-09', 'Donta Hall', 'SIGN_REST_OF_SEASON')
                assert 'rest of regular season' in original['historical_claim']
                record['resolution'] = 'TEAM_BODY_AND_GUIDE_LABEL_PREFERRED_FEED_CONFLICT_RETAINED'
            else:
                raise ValueError('unhandled discrepancy: ' + state)
            record['original_source_id'] = original['source_id']
        public.append(record)
    assert len(public) == 21 and len({(r['date'], r['event'], r.get('player')) for r in public}) == 21
    represented = [g for r in public for g in r['feed_groups']]
    assert len(represented) == len(set(represented)) == 18
    observed = {r['GroupSort'] for r in feed['orlando']['related_rows']}
    assert set(represented) == observed, 'unreconciled feed group'
    assert feed['orlando']['feed_only_groups'] == []
    assert feed['orlando']['date_window'] == ['2021-03-25', '2021-05-16']
    assert feed['orlando']['guide_comparison_window'] == ['2021-04-12', '2021-05-16']
    return sorted(public, key=lambda r: (r['date'], r['event'], r.get('player', '')))


def build(cache):
    import fitz
    raw = (cache / 'orlando-magic-media-guide-2022-23.pdf').read_bytes()
    assert digest(raw) == GUIDE_SHA, 'frozen guide changed'
    with fitz.open(stream=raw, filetype='pdf') as pdf:
        assert len(pdf) == 222
        pages = {i: pdf[i-1].get_text() for i in (116, 117)}
    feed = json.loads((ROOT / FEED).read_text(encoding='utf-8'))
    releases = json.loads((ROOT / RELEASES).read_text(encoding='utf-8'))
    rows = reconcile(feed, releases, pages)
    return dict(schema='ORLANDO_FINITE_PUBLIC_EVENT_COVERAGE_V1',
                baseline_main='cf50c92c58d997d67e74b5684337edf9aa5fac2c',
                observed_local_date='2026-10-05', window=feed['orlando']['date_window'],
                scope='PUBLISHED_PLAYER_CONTRACT_AND_TRADE_EVENTS_IN_FROZEN_NBA_FEED_AND_TEAM_GUIDE',
                guide=dict(url='https://cdn.nba.com/teams/uploads/sites/1610612753/2022/11/orlando-magic-media-guide-2022-23.pdf',
                           sha256=GUIDE_SHA, pdf_pages=[116, 117], printed_pages=[229, 230],
                           text_sha256={str(i): digest(t.encode()) for i, t in pages.items()},
                           table_visually_checked=True),
                inputs={p: digest((ROOT/p).read_bytes().replace(b'\r\n', b'\n')) for p in (FEED, RELEASES)},
                events=rows, public_event_count=21, represented_feed_groups=18,
                represented_feed_rows=len(feed['orlando']['related_rows']),
                original_body_release_complements=3, resolved_label_conflicts=1,
                unresolved_events_in_defined_public_inventory=0,
                defined_public_inventory_reconciled=True,
                boundaries=dict(unpublished_event_absence_proved=False,
                                actual_intraday_receipt_order_proved=False,
                                historical_trades_copied_to_selected_world=False,
                                modeled_contract_terms_author_locked=False,
                                unknown_salary_residual_zero=False,
                                full_alternative_registration_pass=False,
                                source_verified_legal_proofs_added=0,
                                manuscript_allowed=False))


def self_test(cache):
    import fitz
    with fitz.open(cache/'orlando-magic-media-guide-2022-23.pdf') as pdf:
        pages = {i: pdf[i-1].get_text() for i in (116, 117)}
    f = json.loads((ROOT/FEED).read_text(encoding='utf-8'))
    r = json.loads((ROOT/RELEASES).read_text(encoding='utf-8'))
    assert len(reconcile(f, r, pages)) == 21
    bad_release = deepcopy(r); bad_release['events'] = bad_release['events'][1:]
    bad_feed = deepcopy(f)
    bad_feed['orlando']['related_rows'].append(dict(GroupSort='UNKNOWN', TRANSACTION_DATE='2021-04-20'))
    bad_label = deepcopy(f)
    next(x for x in bad_label['orlando']['comparison'] if x['status']=='CONTRACT_CLASS_CONFLICT')['guide_event']['action']='SIGN_TEN_DAY'
    bad_source = deepcopy(r); bad_source['events'][0]['source_fact_verified']='true'
    for ff, rr in ((f, bad_release), (bad_feed, r), (bad_label, r), (f, bad_source)):
        try:
            reconcile(ff, rr, pages)
        except (AssertionError, ValueError):
            continue
        raise AssertionError('unreconciled event/unsupported source must block')
    print('Public inventory negative controls PASS: missing release, extra feed group, wrong label, false certificate')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache-dir', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test(args.cache_dir)
    result = build(args.cache_dir)
    if args.check:
        assert json.loads((ROOT/OUT).read_text(encoding='utf-8')) == result
    else:
        (ROOT/OUT).write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('21 public events / 18 feed groups reconciled; selected-world registration remains HOLD')
