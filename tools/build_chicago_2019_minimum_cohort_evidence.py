"""Source-backed minimum cohort and reported guarantee timing, not full R."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = 'research/CHICAGO_2019_MINIMUM_COHORT_EVIDENCE_2026_10_05.json'
REPORTS = [
    ('harrison', 'fr-harrison-2018-andrews-oembed.json', 'cddcd2f11026f9748d874c181874d6d47a5162b3dda323a6694bfe3d9fc31c75', '2018-10-22', ['two-year minimum contract', '$175,000 guaranteed', '8/15/19']),
    ('lemon', 'fr-lemon-2019-charania-oembed.json', '5543fed992a62a82bdf77ca18eb53ed42c8bfe169316968529e8507470a86007', '2019-03-28', ['remainder of the season']),
    ('asik_application', 'fr-asik-medical-1121524384953511936-oembed.json', 'eebb685eaa558a67419fc14e073c436b9456e7618009d359e113449ca740dc87', '2019-04-25', ['have requested', 'removed from team salary']),
    ('asik_grant_report', 'fr-asik-medical-1143922858416050176-oembed.json', '36267408204b70258b5c6f4e0d9af86d8441c96301a01e69aa0a85bf727d0880', '2019-06-26', ['NBA has removed', 'career-ending injury/illness']),
]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def build(cache):
    import fitz
    sources = []
    for key, name, expected, day, markers in REPORTS:
        raw = (cache/name).read_bytes()
        assert sha(raw) == expected, 'frozen reporter body changed: '+key
        data = json.loads(raw)
        text = html.unescape(re.sub('<[^>]*>', '', data['html']))
        assert all(marker in text for marker in markers)
        sources.append(dict(id=key, url=data['url'], author=data['author_name'],
                            publication_date=day, raw_sha256=expected, bytes=len(raw),
                            access='PUBLIC_X_OEMBED_BODY_READ_DIRECT_X_PAGE_UNAVAILABLE',
                            tier='ORIGINAL_REPORTER_LEAGUE_SOURCE_REPORT_NOT_REGISTERED_CONTRACT'))
    documents = [
        ('cba2017', 'fr-2017-cba.pdf', '66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a', [36,55,56], 'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf'),
        ('scale2018', 'fr-2018-19-cba101-harrison.pdf', 'c5ce40b61ae6287afaf173d067b6eb20eee72a58a9dc3d24552c1a424dafb213', [30], 'https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf'),
        ('harrison_history', 'fr-bulls-2019-20-guide-ia.pdf', 'c89c69ea29d8a68395267133fa4edff9280c36c6335a4a274f649da75168e82e', [52], 'https://archive.org/download/chicago-bulls-2019-2020-media-guide/Chicago%20Bulls%202019-2020%20Media%20Guide.pdf'),
    ]
    texts = {}
    for key, name, expected, pages, url in documents:
        raw = (cache/name).read_bytes(); assert sha(raw) == expected
        with fitz.open(stream=raw, filetype='pdf') as pdf:
            texts[key] = {i: pdf[i-1].get_text() for i in pages}
        sources.append(dict(id=key, url=url, raw_sha256=expected, bytes=len(raw),
                            pdf_pages=pages, text_sha256={str(i):sha(t.encode()) for i,t in texts[key].items()},
                            access='DIRECT_LOCAL_PDF_TEXT_READ',
                            table_visual_checked=(key=='scale2018'),
                            official_host=(key!='harrison_history'),
                            official_mirror_byte_equivalence_verified=False if key=='harrison_history' else None))
    cohort = ' '.join(texts['cba2017'][55].split())
    assert 'first Season covered by a player’s Contract is the 2018-19 Season' in cohort
    assert 'shall apply for each Season of the Contract' in cohort
    assert 'On July 1 of each Salary Cap Year' in cohort
    assert 'Minimum Annual Salary Scale applicable to the player' in cohort
    assert 'with no bonuses of any kind' in ' '.join(texts['cba2017'][56].split())
    scale = ' '.join(texts['scale2018'][30].split())
    assert '2 1,512,601 1,588,231 1,663,861' in scale
    history = ' '.join(texts['harrison_history'][52].split())
    assert '2018-19 (CHICAGO): Appeared in 73 games' in history
    assert '2017-18 (PHOENIX): Appeared in 23 games' in history
    # July 6 waiver is separately supported by the already recovered official body.
    prior = 'research/CHICAGO_2019_DATED_SOURCE_RECOVERY_2026_10_04.json'
    recovered = json.loads((ROOT/prior).read_text(encoding='utf-8'))
    assert recovered['findings']['young_july6_signing_and_harrison_lemon_waivers']=='OFFICIAL_BODY_CONFIRMED'
    return dict(schema='CHICAGO_MINIMUM_COHORT_AND_REPORTED_TRIGGER_V1',
                baseline_main='cf50c92c58d997d67e74b5684337edf9aa5fac2c', observed_local_date='2026-10-05',
                sources=sources, official_waiver_evidence=dict(path=prior,sha256=sha((ROOT/prior).read_bytes())),
                harrison=dict(status='SOURCE_BACKED_CONDITIONAL_BASE_AND_REPORT_TIMING',
                              first_contract_season='2018-19', upcoming_season='2019-20',
                              credited_YOS=2, contract_year=2, applicable_scale='2018-19',
                              ordinary_annual_base_if_reported_contract_unchanged_usd=1588231,
                              rejected_new_2019_scale_year1_substitution_usd=1620564,
                              substitution_difference_usd=32333,
                              rejected_2018_scale_1YOS_year2_usd=1416852,
                              reported_future_protection_usd=175000, reported_trigger_date='2019-08-15',
                              official_waiver_date='2019-07-06',
                              reported_trigger_satisfied_if_unchanged=False,
                              prior_season_250000_guarantee_carried_to_2019=False,
                              actual_full_post_waiver_residual_usd=None),
                lemon=dict(original_report_covers='REMAINDER_OF_2018_19_SEASON',
                           future_2019_20_salary_or_protection_disclosed=False,
                           future_contract_absence_proved=False),
                asik=dict(application_report_date='2019-04-25', exclusion_grant_report_date='2019-06-26',
                          rounded_reported_relief_usd=3000000,
                          grant_report_is_not_exact_3000001_charge_certificate=True,
                          additional_deduction_to_existing_anchor_usd=0,
                          alternative_world_medical_decision_certified=False),
                boundaries=dict(full_R_upper_usd=None, amended_terms_or_injury_claims_zero=False,
                                historical_reporting_is_alternative_author_lock=False,
                                legal_proofs_promoted=0, manuscript_allowed=False))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache-dir',type=Path,required=True);p.add_argument('--check',action='store_true')
    a=p.parse_args();d=build(a.cache_dir)
    if a.check: assert json.loads((ROOT/OUT).read_text(encoding='utf-8'))==d
    else:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Harrison 2018 scale / 2YOS / Year2 = 1,588,231; reported Aug15 trigger not met by July6 waiver; full residual HOLD')
