"""Compare retained container metrics; never infer utterances or target prose."""
import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = 'research/G11_THREE_WORK_RANGES_2026_10_01'
SG_FUNCTION = 'research/G11_RIDI_FUNCTION_SEQUENCE_FIRST_FIVE_2026_10_01.json'
SG_PILOT = 'research/G11_RIDI_CONTEXTUAL_VOICE_PILOT_2026_10_01.json'
SG_VOICE = 'research/G11_RIDI_CONTEXTUAL_VOICE_FIRST_FIVE_2026_10_01.json'
BUSINESS = 'research/G11_RIDI_BUSINESS_FIRST_FIVE_COMPONENTS_2026_10_01.json'
EXTRA = 'research/G11_JOARA_EXTRA_FIRST_FIVE_COMPONENTS_2026_10_01.json'
SOURCES = [SG_FUNCTION, SG_PILOT, SG_VOICE, BUSINESS, EXTRA]


def build(root=ROOT):
    data = {p: json.loads((root / p).read_text(encoding='utf-8')) for p in SOURCES}
    hashes = {p: hashlib.sha256((root / p).read_bytes().replace(b'\r\n', b'\n')).hexdigest() for p in SOURCES}
    rows = []
    sg_voice = {1: data[SG_PILOT]['first_pass']}
    sg_voice.update({v['chapter']: v['metric'] for v in data[SG_VOICE]['records']})
    for work, path, unit in [
        ('내가 키운 S급들', SG_FUNCTION, 'DOM_P'),
        ('재벌집 막내아들', BUSINESS, 'DOM_P'),
        ('소설 속 엑스트라', EXTRA, 'DOM_FONT'),
    ]:
        source = data[path]
        if source.get('work') != work:
            raise ValueError('source work mismatch: ' + path)
        records = source['records'] if path == SG_FUNCTION else source['metrics']
        if [v['chapter'] for v in records] != [1, 2, 3, 4, 5]:
            raise ValueError('chapter coverage: ' + path)
        for v in records:
            chapter = v['chapter']
            metric = v['first_capture'] if path == SG_FUNCTION else v
            pairs = metric['paragraph_meta']
            sizes = dict(pairs)
            if len(sizes) != len(pairs) or any(n <= 0 for n in sizes.values()):
                raise ValueError('duplicate/empty container')
            denominator = sum(sizes.values())
            if metric['body_utf16'] != denominator + 2 * (len(pairs) - 1):
                raise ValueError('body/separator denominator mismatch')
            voice_path = SG_PILOT if chapter == 1 else SG_VOICE
            if path == SG_FUNCTION:
                voice = sg_voice[chapter]
                if voice['body_sha256'] != metric['body_sha256'] or voice['paragraph_utf16_denominator'] != denominator:
                    raise ValueError('structure/voice body mismatch')
                channels = {k: c['raw_p_indexes'] for k, c in voice['channels'].items()}
            else:
                channels = metric['voice_indexes']
                voice_path = path
            seen = set()
            channel_rows = {}
            for kind, indexes in channels.items():
                if len(set(indexes)) != len(indexes) or not set(indexes) <= sizes.keys() or seen.intersection(indexes):
                    raise ValueError('voice duplicate/overlap/outside body')
                seen.update(indexes)
                n = sum(sizes[i] for i in indexes)
                if path == SG_FUNCTION:
                    original = voice['channels'][kind]
                    if original['utf16_characters'] != n or original['paragraph_units'] != len(indexes):
                        raise ValueError('retained voice amount mismatch')
                channel_rows[kind] = dict(status='REPORTED', containers=len(indexes),
                                          utf16=n, share_of_container_text=n / denominator)
            ordered = sorted(sizes.values())
            q = lambda t: ordered[math.floor((len(ordered)-1)*t)]
            rows.append(dict(work=work, chapter=chapter, url=metric['url'],
                selection='FIRST_FIVE_SERIAL_INSTALLMENTS_ORDER_1_TO_5_NOT_MATCHED_STORY_PHASES',
                unit=unit, containers=len(pairs), text_utf16=denominator,
                joined_body_utf16=metric['body_utf16'],
                paragraph_distribution=dict(p10=q(.1), median=q(.5), p90=q(.9), maximum=ordered[-1]),
                channels=channel_rows,
                other_container_text_utf16=denominator-sum(x['utf16'] for x in channel_rows.values()),
                other_text_is_not_pure_narration=True,
                body_sha256=metric['body_sha256'], metric_source=path, voice_source=voice_path,
                annotation_provenance=dict(
                    source_identifier=voice_path,
                    recorded_stage=data[voice_path].get('schema', data[voice_path].get('stage')),
                    recorded_date=data[voice_path].get('observed_on'),
                    source_date_missing_is_unknown=True,
                    source_baseline=data[voice_path].get('base_commit', data[voice_path].get('baseline_main')),
                    canonical_metric_sha256=voice.get('canonical_sha256') if path == SG_FUNCTION else metric['canonical_sha256'],
                    independent_same_pass_recoding=False)))
    all_categories = sorted(set.union(*(set(r['channels']) for r in rows)))
    for row in rows:
        row['category_reporting'] = {k: 'REPORTED' if k in row['channels'] else 'NOT_REPORTED'
                                     for k in all_categories}
    # Only explicitly present categories may enter a comparable summary.
    common = sorted(set.intersection(*(set(r['channels']) for r in rows)))
    summaries = []
    for work in dict.fromkeys(r['work'] for r in rows):
        group = [r for r in rows if r['work'] == work]
        spans = {}
        for category in common:
            values = [r['channels'][category]['share_of_container_text'] for r in group]
            spans[category] = dict(min=min(values), median=statistics.median(values), max=max(values))
        summaries.append(dict(work=work, chapter_count=5, channel_share_ranges=spans,
                              weighting='UNWEIGHTED_CHAPTER_MIN_MEDIAN_MAX_NOT_POOLED'))
    return dict(schema='G11_RETAINED_THREE_WORK_COMPARISON_V1', base_commit='4029f0b',
        source_hashes=hashes, rows=rows, summaries=summaries,
        explicitly_reported_common_categories=common,
        category_name_equivalence_is_semantic_certification=False,
        semantic_comparability='NOT_CALIBRATED_ACROSS_COHORTS',
        numeric_comparability='RETAINED_LENGTH_ACCOUNTING_ONLY',
        cross_work_difference_computed=False,
        missing_category_policy='NOT_REPORTED_NOT_ZERO',
        additional_readings=0, unique_readings=95, unread=15,
        compared_existing_chapters=15, new_component_chapters=0,
        whole_P3_completed_chapters=0, actual_episode_packs=0,
        numeric_source_consistency_checked=True, independent_original_review=False,
        total_inner_share=None, professional_action_density=None,
        sentence_count=None, author_paragraph_count=None, utterance_count=None,
        whole_P3_final=False, G11_final=False, author_locked=False,
        manuscript_allowed=False, freeze='v0.30 PARTIAL', gate='CLOSED',
        range_is_prose_target=False, cross_platform_causal_effect=None)


def render(report):
    lines = [
        '# G11 세 작품 비교 — 관측 대역과 집필 규격의 경계', '',
        '기준 main `4029f0b`. 기존 공식 연재판 첫5화 계측만 재계산한 파생 비교다. 새 본문 열람·독서 추가0, 새 구성요소 추가0. 세 작품·15화는 항목별15/50에 이미 포함된 회차이며 독서95/110·미독15·전체P3완료0을 유지한다.', '',
        '## 비교 단위', '',
        '- 길이는 공백 포함 UTF16 코드 유닛이다. 실제 글자·문법적 문장·작가 문단·발화 횟수가 아니다.',
        '- 비율 분모는 선택 표시 컨테이너의 정규화 텍스트 길이 합이며 인공 합류 개행은 제외한다. 결합 본문 길이와 분모를 함께 보인다.',
        '- 범주별로 분류된 컨테이너 전체 텍스트를 합한다. 혼합 절이 있을 수 있으므로 순수 발화 음절 비율이 아니다.',
        '- 빠진 범주는 NOT_REPORTED로 두고0으로 채우지 않는다. 명시된 QUOTED_INNER의0은 무인용 사고/전체 내면이0이라는 뜻이 아니다.',
        '- DOM_P와 DOM_FONT는 표시 단위다. 같은 정규화 길이로 관측 대조는 가능하지만 플랫폼 효과·작가의 호흡 차이를 인증하지 않는다.',
        '- 표본은 각 작품 연재 첫5회차다. 프롤로그 포함 여부·사건 단계·설명/대화 기능이 같다는 뜻이 아니며, 전체 분량 분위에 맞춘 표본도 아니다.',
        '- 작품별 주석 단계·버전·생성 기준의 독립 정렬 검수는 미수행이다. 같은 범주명도 의미 동등성 인증이 아니므로 작품 간 의미 비교는 NOT_CALIBRATED_ACROSS_COHORTS다. 차이값·효과 크기·순위는 산출하지 않는다.',
        '- 과거 보고/매개 기억/원격 전화/행사 호명/로봇/UI를 현장 인물 발화 범주로 합치지 않는다. 현지 발신자의 전화 발화가 CHARACTER_SPEECH일 수 있어 이 범주 전체를 대면이라고 부르지 않는다. 원문·긴 인용은 보존/전송하지 않았다.', '',
        '## 회차별 관측', '',
        '| 작품·화 | 표시 단위 수 | 분모 / 결합 본문 UTF16 | 표시 길이 p10/중앙/p90/최대 | CHARACTER_SPEECH 컨테이너·비중 |',
        '|---|---:|---:|---|---:|',
    ]
    for row in report['rows']:
        q = row['paragraph_distribution']
        c = row['channels']['CHARACTER_SPEECH']
        lines.append(f"| {row['work']} {row['chapter']} | {row['unit']} {row['containers']} | {row['text_utf16']} / {row['joined_body_utf16']} | {q['p10']}/{q['median']}/{q['p90']}/{q['maximum']} | {c['containers']} · {c['share_of_container_text']:.2%} |")
    lines += ['', '## 명시된 같은 범주명 — 작품별 기술 통계', '',
        '다음 값은 각 작품의5개 회차 비율을 동일 가중치로 정렬한 최소/중앙/최대다. 수치의 의미를 독립 교정한 작품 간 비교는 아니다. 합산 비율·시장 평균·품질 순위·권장 목표가 아니다. 전화 등 별도 범주는 JSON 회차 행에 모두 유지한다.', '',
        '| 작품 | 범주 | 회차 최소 / 중앙 / 최대 |', '|---|---|---:|']
    for s in report['summaries']:
        for kind, q in s['channel_share_ranges'].items():
            lines.append(f"| {s['work']} | {kind} | {q['min']:.2%} / {q['median']:.2%} / {q['max']:.2%} |")
    lines += ['', '## 주석 출처와 범주 누락', '',
        '아래 출처는 동일한 재코딩 패스가 아니다. JSON의 회차별 annotation_provenance는 파일/단계/기록 날짜/기준 커밋/계측 지문을 연결한다. 날짜 필드가 없는 원장에는 null을 남긴다. category_reporting은 모든 범주의 REPORTED/NOT_REPORTED를 분리한다. REPORTED는 원문상의 범주 부재까지 독립 인증했다는 뜻이 아니다.', '',
        '| 작품 | 음성 주석 출처 | 작품의5화 중 NOT_REPORTED 범주 |', '|---|---|---|']
    for work in dict.fromkeys(r['work'] for r in report['rows']):
        group = [r for r in report['rows'] if r['work'] == work]
        paths = sorted({r['voice_source'] for r in group})
        missing = sorted({k for r in group for k, v in r['category_reporting'].items() if v == 'NOT_REPORTED'})
        lines.append(f"| {work} | {'; '.join(paths)} | {', '.join(missing)} |")
    lines += ['', '범주 누락만으로 현재 발화를 하한/상한으로 재분류하지 않는다. 누락 범주의 원문이 현재 발화에 흡수됐는지 알려면 동일한 문맥 재코딩이 필요하다. 그 검수 전에는 각 작품 기록의 기술 통계만 보존한다.', '',
        '## 집필 규격 연결 — 기존 질문의 하위 사례', '',
        '본문 계측과 지문은 기존 관측 기록 FACT, 사건/보상/시간의 문맥 코딩은 INFERENCE, 아래 프로젝트 검사 질문은 CANDIDATE다. 새 AUTHOR_LOCKED0. 기존 규칙에 증인을 붙이며 활성 전역 규칙을 추가하지 않는다.', '',
        '| 기존 질문 | S급들 증인 | 재벌집 증인 | 엑스트라 증인 | 적용 경계 |',
        '|---|---|---|---|---|',
        '| 성과와 다음 조건 | 2화 승리와 시간 변경,5화 모집 구상 분리 | 2화 서류·출국과 승진/송금,5화 환대와 조건 약속 분리 | 3화 무기 수령,4화 물건 수령,5화 권능 통지 분리 | 훈련 성과·역할 제안·등록·출전을 한 성공으로 승격하지 않는지 묻는다. |',
        '| 정보 접근 | 1화 기억 음성과 현재 반응 | 1화 SMS/전화,2화 과거 발화 | 2화 보고 메일,5화 타 인물 무인용 사고 | 검토자에게 보인 정보가 주인공에게 전달됐는지 따로 확인한다. |',
        '| 이동과 실행 | 5화 이사 지시와 현재 검사/복귀 | 3화 탈출 제지와 실제 은행 이동 | 2화 출발,4화 조준 중 배달 도착 | 계획·지시·시도·완료를 분리하며 선택된 위치만으로 완전 인과를 인증하지 않는다. |',
        '| 시간층 | 1화 기억 창과2화 현행 시간 변경 | 1~3화 전제 이전 삶의 순차 도입,2화 개인 과거 | 1화 프로필/현재 행사,2화 개인 과거,5화 별도 시점 | 변환 전 삶 전체를 회상으로, 타 인물 생각을 주인공 기억으로 합치지 않는다. |',
        '',
        '증인 위치는 S급들 기능 원장의 records[].story_observations와 macro_blocks, 재벌집/엑스트라 원장의 episodes[].blocks/selected_anchors를 따른다. 전수 과거 분량·전체 내면/용어/전문 활동 밀도는 미측정이다.', '',
        '## KEEP / ADOPT / AVOID / RANGE', '',
        '- KEEP: 승인된 주인공 성격·리바운드 동작·선수/코치/프런트 권한. 외부 장르 장치를 정본 사실로 사용하지 않는다.',
        '- ADOPT 후보: 성과/다음 조건과 정보 출처는 기존 House Style 평가·권한·정보 검문의 하위 질문으로 흡수한다. 실제 회차가 준비되면 주매력1과 필요한 보조 기능1을 먼저 정한다.',
        '- AVOID: 정보를 얻거나 물건을 받은 장면을 무조건 실력 성장으로 판정하기, 현재 사람 발화와 모든 음성/UI를 합치기, 형식 차이를 문체 우열로 바꾸기.',
        '- RANGE: 위15화의 관측 대역만 보존한다. 프로젝트200자 점검 기준은 코드포인트/낭독 검문이 별도로 필요하며 UTF16 표시 길이로 통과/실패를 인증하지 않는다.',
        '',
        '현재 원고/실제 회차Pack이0이므로 A/B 장면 적용·낭독·인간 keep/revert 실적은0이다. 다음 필요한 결함이 없는 한 기법을 추가하지 않는다. 실제 결함1과 단일 기능1의 격리 비교가 준비될 때만 보조 기능을 활성화한다.', '',
        '## 남은 범위', '',
        '나머지7작품35화의 구성요소, 핵심 미독15화, 같은 전체 검사표의 의미 검수·표본 편향/반례·프로젝트 적용 판정이 남았다. 이번 비교는 전체P3/SAMPLE/FULL/G11 최종 통과가 아니다. freeze v0.30 PARTIAL·설계/원고 CLOSED·큰 묶음 미완료6.', '',
        '소스 경로·내용 SHA256·회차별 원 URL·본문 지문·범주별 수치는 [JSON 비교 원장](G11_THREE_WORK_RANGES_2026_10_01.json)에 있다. 검사기는 보존 수치의 일관성만 인증하며 원문 접근/독립 의미 인증은 하지 않는다.', '',
    ]
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    report = build()
    outputs = {STEM+'.json': json.dumps(report, ensure_ascii=False, indent=2)+'\n',
               STEM+'.md': render(report)}
    for path, content in outputs.items():
        if args.check:
            if (ROOT/path).read_text(encoding='utf-8') != content:
                raise ValueError('stale derived comparison: ' + path)
        else:
            (ROOT/path).write_text(content, encoding='utf-8')
    print(json.dumps(dict(status='PASS', existing_chapters=15, new_readings=0,
                          new_components=0, whole_P3_final=False, manuscript_allowed=False)))


if __name__ == '__main__':
    main()
