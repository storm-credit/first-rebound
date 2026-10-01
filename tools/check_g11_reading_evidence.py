"""Audit recorded reading evidence and irreversible metrics, not literary quality."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

ROOT = Path(__file__).resolve().parents[1]
READINGS = 'research/STYLE_READING_OBSERVATIONS.json'
METRICS = 'research/G11_RIDI_STRUCTURAL_MEASUREMENTS_2026_10_01.json'
OUT = 'reviews/G11_READING_EVIDENCE_REPORT.json'
HOSTS = {'www.munpia.com': 'Munpia', 'ridibooks.com': 'Ridi',
         'page.kakao.com': 'KakaoPage', 'www.joara.com': 'Joara'}
CORE = {'필드의 고인물', '재벌집 막내아들', '아포칼립스에 집을 숨김',
        '데뷔 못 하면 죽는 병 걸림'}
FIRST_FIVE_ONLY = {'나 혼자만 레벨업', '내가 키운 S급들', '닥터, 조선 가다',
                   '소설 속 엑스트라', '전지적 독자 시점', '홈 플레이트의 빌런'}
MUNPIA_WORK_IDS = {'필드의 고인물': '153525', '아포칼립스에 집을 숨김': '342817',
                   '전지적 독자 시점': '104753', '홈 플레이트의 빌런': '100495',
                   '닥터, 조선 가다': '103757'}
KAKAO_WORK_IDS = {'데뷔 못 하면 죽는 병 걸림': '56325530', '나 혼자만 레벨업': '48787313'}


def recorded_work_url_matches(work, chapter, url):
    """Bind recorded edition IDs, without authenticating the live viewer body."""
    if work in MUNPIA_WORK_IDS:
        return (url.hostname == 'www.munpia.com' and
                url.path.startswith('/novel/viewer/' + MUNPIA_WORK_IDS[work] + '/'))
    if work in KAKAO_WORK_IDS:
        return (url.hostname == 'page.kakao.com' and
                url.path.startswith('/content/' + KAKAO_WORK_IDS[work] + '/viewer/'))
    if work == '소설 속 엑스트라':
        query = dict(parse_qsl(url.query))
        return (url.hostname == 'www.joara.com' and url.path == '/viewer'
                and query.get('bookCode') == '1301411' and query.get('sortno') == str(chapter))
    if work in {'재벌집 막내아들', '내가 키운 S급들'} and type(chapter) is int:
        # Recorded serial IDs for this sample; do not extrapolate to unread chapters.
        first_id = 3586025015 if work == '재벌집 막내아들' else 2065016312
        return url.hostname == 'ridibooks.com' and url.path == f'/books/{first_id + chapter - 1}/view'
    return False


def audit(data, measured):
    errors = []
    core=set(data['planned'].get('core_work_names', CORE))
    works=CORE | FIRST_FIVE_ONLY
    replacement=(CORE-{'데뷔 못 하면 죽는 병 걸림'})|{'소설 속 엑스트라'}
    if core not in (CORE,replacement):
        errors.append('unreviewed core revision')
    if core!=CORE:
        path=data['planned'].get('research_revision_evidence')
        if path!='research/G11_CORE_EXTENSION_2026_10_02.json':
            errors.append('core revision evidence missing')
        else:
            revision=json.loads((ROOT/path).read_text(encoding='utf-8'))
            if set(revision['selected_core_work_names'])!=core or revision['original_unread_debt']['count']!=15 or revision['G11_final'] is not False:
                errors.append('core revision/debt mismatch')
            debt=data.get('original_access_debt',{})
            if (debt.get('work')!='데뷔 못 하면 죽는 병 걸림' or debt.get('count')!=15
                    or debt.get('chapters')!=list(range(6,21)) or debt.get('status')!='AUTH_REQUIRED'):
                errors.append('original access debt lost')
            identities={r['chapter']:r for r in revision['chapter_identity']}
            for rec in revision['records']:
                ch=rec[0]
                matches=[r for r in data['readings'] if r['work']==revision['work'] and r['chapter']==ch]
                if (len(matches)!=1 or matches[0].get('body_sha256')!=rec[6]
                        or matches[0]['url']!=identities[ch]['url']):
                    errors.append('extension record does not match ledger')
    for key in ('author_locked', 'season_selected', 'exact_execution_cleared',
                'manuscript_allowed', 'raw_text_retained'):
        if data.get(key) is not False:
            errors.append('reading ledger cannot promote gates or retain raw text: ' + key)
    seen, seen_urls = set(), set()
    chapters, platforms = defaultdict(set), Counter()
    for row in data['readings']:
        key = (row['work'], row['chapter'])
        url = urlsplit(row['url'])
        # Joara's chapter identity is in its query; Munpia's viewRateType is UI only.
        canonical_url = (url.hostname, url.path,
                         tuple(sorted((k, v) for k, v in parse_qsl(url.query)
                                      if not (url.hostname == 'www.munpia.com' and k == 'viewRateType'))))
        if key in seen or canonical_url in seen_urls:
            errors.append('duplicate chapter or official viewer URL')
        seen.add(key)
        seen_urls.add(canonical_url)
        valid = (row.get('scope') == 'COMPLETE_CHAPTER' and
                 bool(row.get('body_read_pages')) and bool(row.get('observations')) and
                 url.scheme == 'https' and url.hostname in HOSTS and
                 type(row['chapter']) is int and
                 row['work'] in works and
                 1 <= row['chapter'] <= (20 if row['work'] in core else 5))
        valid = valid and recorded_work_url_matches(row['work'], row['chapter'], url)
        if not valid:
            errors.append('incomplete or unsupported reading evidence')
            continue
        if row.get('raw_text_retained') is not False or row.get('verbatim_excerpt') is not None:
            errors.append('raw text retention forbidden')
        chapters[row['work']].add(row['chapter'])
        platforms[HOSTS[url.hostname]] += 1
    first_five = sum(set(range(1, 6)) <= cs for cs in chapters.values())
    first_twenty = sum(set(range(1, 21)) <= chapters[w] for w in core)
    planned = data['planned']
    target = (planned['works'] * planned['first_five_chapters_per_work'] +
              planned['core_works'] * (planned['core_chapters'] - planned['first_five_chapters_per_work']))
    if (target != planned['total_chapters'] or planned['core_works'] != len(core)
            or planned['works'] != len(works)
            or planned['first_five_chapters_per_work'] != 5 or planned['core_chapters'] != 20):
        errors.append('planned target mismatch')
    observed = data['observed']
    actual = dict(complete_chapters=sum(platforms.values()), works_first_five_complete=first_five,
                  works_first_twenty_complete=first_twenty,
                  unread_chapters_against_default_target=target - sum(platforms.values()))
    if any(observed[k] != v for k, v in actual.items()):
        errors.append('declared counts differ from recorded readings')
    if core!=CORE and (observed.get('original_plan_complete_chapters')!=sum(len(cs & set(range(1,21 if w in CORE else 6))) for w,cs in chapters.items())
                      or observed.get('original_plan_unread_chapters')!=15):
        errors.append('original plan counts rewritten')
    if set(observed['body_platforms']) != set(platforms):
        errors.append('declared platforms differ from recorded readings')
    if measured.get('readings_added') != 0 or measured.get('raw_text_retained') is not False:
        errors.append('remeasurement cannot add readings or retain raw text')
    measures = measured['measurements']
    if [r['chapter'] for r in measures] != list(range(1, 6)):
        errors.append('measurement chapter coverage')
    for row in measures:
        first, second = row['first_pass'], row['second_pass']
        body = {k: v for k, v in first.items() if k != 'canonical_measurement_sha256'}
        canonical = json.dumps(body, ensure_ascii=False, separators=(',', ':'))
        if sha256(canonical.encode('utf-8')).hexdigest() != first['canonical_measurement_sha256']:
            errors.append('canonical metric hash mismatch')
        if any(first[k] != second[k] for k in ('url', 'viewer_sha256', 'body_sha256', 'canonical_measurement_sha256')):
            errors.append('two opens do not reproduce')
        if second.get('match') is not True:
            errors.append('second-open observation not confirmed')
        if first['speech_function_ratios'] is not None:
            errors.append('unclassified prefix counts cannot become speech ratios')
        if not any(r['work'] == measured['work'] and r['chapter'] == row['chapter'] and
                   r['url'] == first['url'] for r in data['readings']):
            errors.append('measurement not mapped to reading evidence')
    if len({r['first_pass']['body_sha256'] for r in measures}) != len(measures):
        errors.append('duplicate measured body across chapters')
    return dict(PASS=not errors, scope='RECORDED_EVIDENCE_ARITHMETIC_AND_MEASUREMENT_REPRODUCTION',
                observed=actual, target_chapters=target, chapter_platform_counts=dict(platforms),
                missing_core_chapters={w: sorted(set(range(1, 21)) - chapters[w]) for w in sorted(core)
                                       if not set(range(1, 21)) <= chapters[w]},
                original_core_missing_chapters={w:sorted(set(range(1,21))-chapters[w]) for w in sorted(CORE) if not set(range(1,21))<=chapters[w]},
                research_revision_not_original_plan_completion=core!=CORE,
                structurally_remeasured_chapters=len(measures), new_readings=0,
                new_readings_scope='THIS_CHECKER_ADDS_NO_READINGS; BATCH_ADDED_15_RECORDED_ELSEWHERE',
                literary_P3_final=False, G11_final=False, actual_episode_packs=0,
                manuscript_allowed=False, independent_body_verification=False,
                captures_authenticated_by_checker=False, errors=errors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = audit(*[json.loads((ROOT / path).read_text(encoding='utf-8')) for path in (READINGS, METRICS)])
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if result['errors']:
        print(rendered)
        raise SystemExit(1)
    if args.check:
        assert (ROOT / OUT).read_text(encoding='utf-8') == rendered, 'stale G11 evidence report'
    else:
        (ROOT / OUT).write_text(rendered, encoding='utf-8')
    print(rendered)
