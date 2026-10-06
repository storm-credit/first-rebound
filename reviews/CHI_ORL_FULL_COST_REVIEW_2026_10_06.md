# Chicago·Orlando 전체 비용행 종료 검수 — 2026-10-06

- 기준 main `e05cf85d75825366cbc4407866029b1d3546f04e` / PR #422 이후.
- **신규 CHI_TEAM_SALARY·ORL_COMPLETE_COST·ORL_F2_COMPLETE_COST 비용행만 LEGAL_BOUND_PASS**. 원장 법적 **6완료/6HOLD**, F 법적 **1/5(F4)**, A 실행0/3·K0/4·시즌 미확정.
- 실제 새 작가 선택·정확 계약 금액 선택·원고 작성 0. v0.30 PARTIAL·설계/원고 CLOSED.

## 새 증인과 판정 범위

| 증인 | 직접 입력/독립 검문 | 종료 범위 |
|---|---|---|
| [새 annual 증인](../research/CHICAGO_NEW_ANNUAL_EXCEPTION_WITNESS_2026_10_06.json) | 11/27 수정 일정 원본문·11/10 적용 annual 값 원본문·CBA, d1_closeable_audit 직접 지문/본문 | 11/21~3/25 원자 F1 직후의 새 MLE/BAE 미사용 산입 0 |
| [CHI 구성 상한](../research/CHICAGO_PUBLIC_COMPONENT_BOUND_2026_10_06.json) | 동시대 긍정 cap inventory·보존 계약/사건·VII4(a) 전체지도, 별도 예외검문 및 independent_finish_scope 실제 재검문 | 3/25 원자 F1 직후의 보존 공개 비용모델 [0,132,367,326.15]≤132,627,000; 여유259,673.85 |
| [ORL F4 상한](../research/ORLANDO_F4_PUBLIC_COMPONENT_BOUND_2026_10_06.json) | 29 raw 캐시·기존 입력10 지문·원기자 Mozgov oEmbed·CBA·전체 A–G, independent_finish_scope 실제 재검문 | T1/T3 모두 완료 후~5/16 보존 공개 비용모델 [0,137,768,857]≤138,928,000; 여유1,159,143 |
| [ORL F2 순서 상한](../research/ORLANDO_F2_ATOMIC_COST_WITNESS_2026_10_06.json) | F4 원자료 재사용·추가 입력8 지문·SUMMER 실제 CBA 귀속 검문·independent_finish_scope 전체 재검문 | 거래 전/중간/후 상태138,303,543 / 122,653,009 / 131,350,601 / 137,768,857; 최대 여유624,457 |

각 상단은 사적 원장 접수증이나 실제 지불액을 인증하지 않는다. source-supported S2 유한 비용 증인이다. 새 실제 비용/계약/분기 입력이 확인되면 증인을 재개방한다. 미공표 모든 계약·예외의 절대 부재를 새 종료 조건으로 요구하지 않는다. 모든 공개 inventory를 단순 무변동 feed 하나로 대체하지도 않는다.

## 수용·정정·HOLD

- **수용:** annual 새 발생 시점과 전체 above-cap 창을 당해 예외 산입 기여에 연결한다. 이전 TPE/DPE 역사 자체의 존재 부재와 분리한다.
- **수용:** CHI는 현재 공개 예외/권리·방출 inventory와 승인 보존 경로를 일반 Team Salary 범주에 대응한다. 사용 선수 Salary는 남기며 Boston apron 제외를 복사하지 않는다. 기존 residual 실제값 null은 보존한다.
- **수용:** CHI 캠프3명 전액4,372,601 안에 Vonleh97,261이 이미 포함된다. Theis/Green 최종 시즌 보너스15% 전 범위977,697.15를 더해도 통과한다. 새 Theis2021 kicker를 소급하지 않는다.
- **수용:** ORL은 camp4명 모두 연간2YOS로 넓게 계산하고, unsigned Fran의 RequiredTender 전액4,033,440도 포함한다. unused 예외 hold의 제외는 apron 법리이며 선수 Salary의 삭제가 아니다.
- **정정:** II6(f)은 minimum도 trade bonus를 가질 수 있다고 한다. Teague 보너스0을 minimum에서 추론하지 않고 현금 원기본급 전액과15% 상단을 모두 더했다.
- **정정:** 독립 검문이 발견한 Nnaji 구판 `120_PERCENT_NO_BONUS_PREMISE` 분류를 80–120% 전체 Salary+Unlikely+assignment 상단으로 바꿨다. 실제 기본급·bonus 선택은 null이다.
- **범위 한정:** Mozgov 원기자 승인 보도·stretch 제외는 보존된 no-added-return 모델에 연결한다. 25NBA경기 환원 규칙 및 (2)(ii) 예외를 분리하고 현금0은 주장하지 않는다.
- **HOLD:** CHI matching 여유175,985.75보다 보너스 전 범위 상단이 크다. 비용행 PASS로 matching/F1 실행을 승격하지 않는다.
- **수용:** 별도 F2 증인이 거래 전·중간·후 전체 비용을 닫았다. SUMMER 정규 이전 종료에는 새 연간 FA 바닥이 없으며 잔류 보수 귀속64,000을 직접 법리로 감쌌다. F4 증인 자체의 범위는 확장하지 않는다. 전체F2 픽/실제 접수·전체F4 건강·시즌은 미확정이다.
- **정정:** F2 MD의 손상된 Ex9/UPC3(b) 숫자6,000/10,000을 원 PDF514–515/555와 대조해 복구했다.

## Research/Verification Layer 실제 실행

| 도구/역할 | 이번 실제 결과 | 계수 한계 |
|---|---|---|
| Antigravity CLI 1.2.11 | [지정 gemini-3.8-flash-low 36.987초 응답 회수](ANNUAL_CALENDAR_AG_2026_10_06.json); 원 기사 본문 BODY_UNAVAILABLE | 모델/service 응답 성공과 자료 본문 실패 분리; 새 법적 원본문 인증0 |
| Codex 자료 수집 | HR 원본문2·SS 계약행·BI archive/widget·Shams 공식oEmbed·CBA/guide 실제 읽기 | 원보도/당시 분석/현재 vendor 이력/공식 원문 분류와 시점 분리 |
| NotebookLM CLI | [초기 후보사본 등록](CHI_COST_NLM_SOURCE_2026_10_06.json), [54.168초 분석 회수](CHI_COST_NLM_2026_10_06.json); 압축 타임라인·비용 범주 비교 | 사본1개4인용은 독립 역사 출처4건 아님. 그 시점 pending 예외지도 지적은 이후 실제 독립 검문으로 종료 |
| 총괄 판정 | 실제 새 반례·법적 범주를 연결한 유한 비용모델만 승격 | fees/picks/건강·시즌·원고 선택 권한 확대0 |
| Codex 독립 검문 | d1_closeable_audit 실제 annual/예외원문; independent_finish_scope 실제 갱신파일·hash·CBA·산술 | 제한 비용행 검문이며 전체G16/기존 모든 설계 독립통과 아님 |
| Claude CLI | [70.079초 PROCESS_TIMEOUT](CHI_COST_CLAUDE_2026_10_06.json), rebuttal_recovered=false | 실행 시도와 실제 반증 회수 분리; 통과 계수0 |
| 전체 source-blind/G16 | NOT_RUN | 전체 통과0 |

NotebookLM의 보너스/waiver 실제값 미확정이라는 표현은 전 범위 상단의 산술 결함이 아니다. 정확값을 새 필수조건으로 추가하지 않는다. 모델은 초기 후보의 옛 예외지도 대기를 정확히 유지했으며, 이후 source/CBA를 읽은 독립자의 종료 판정이 상단 인증의 근거다. [불변 분석 입력](CHI_COST_ANALYSIS_INPUT_2026_10_06.json)의 후보 상태와 최종 증인을 구분한다.

## 재현·중단점

이번 배치 직접 재현: raw 캐시34개 및 저장소 입력40개 SHA, CHI Decimal 상단·ORL 네 상태·SUMMER/Tender/보너스·단기계약 일수·권위 null·MD 링크 모두 PASS. `git diff --check` PASS. S2 검사기의 음성 대조와 미래 정상 종료 경로 대조도 PASS.

S2 검사기 `python -B -X utf8 tools/check_chicago_d1_s2.py --self-test`로 legal6PASS/6HOLD, F4법적PASS·나머지F HOLD 및 A/K/시즌/원고 flags와 음성·종료 gate controls를 검문한다. 신규 JSON의 저장소 입력 SHA·raw cache SHA·서로 다른cap/apron/일수 산술·신인미선택·MD links도 직접 확인한다.

다음 미종료 법적6행은 CHI matching, BOS TPE의 두 픽, DEN Gordon 자산/charge, DEN F3 전체 비용, CLE 전체 비용, DEN F5 전체 비용이다. 건강/분/시즌 실행과 최종 회차기능·실제Pack도 별도 남는다. 큰묶음6개 미완료.
