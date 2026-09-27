# O-15F14-AI — Boston TPE 공개 용량 검토

- 기준: [AI 공개 용량 증인](../research/O15F14AI_BOSTON_FOURNIER_TPE_CAPACITY_BOUND.md), `main` `c635aee`.
- 판정: `ARITHMETIC_PASS / SOURCE_SHARED / EXACT_F2_HOLD`.

| 검문 | 실제 실행·입력 | 판정 |
|---|---|---|
| Anti-Gravity Evidence Lane | 절대 경로 `agy.exe`에 NBA 3/16 TPE 기사·시즌 거래표 두 URL만 지정하고 읽기 전용 `read_url_content→view_file` 요청. JSON `SUCCESS`, 한 턴 응답은 두 본문에 맞는 `$28.5m` 및 3/25 Boston 거래 두 건을 인용 | 실제 개별 도구 이벤트는 JSON에 없어 본문 접근 **자체 보고만** 관측했다. Codex·NLM과 동일 NBA URL이므로 새로운 독립 원자료는 0건. |
| NotebookLM Analysis Lane | 작업실 `a3f30584-3a9d-4a8b-8960-b661615d98e9`에 두 NBA URL을 추가: source `e0c7b83e-9f3a-46f3-a8c6-6703905dbc45`, `ea73dacd-c72b-4777-8217-1ca5fedb2ad7`. `nlm content source`로 두 저장 본문을 확인한 뒤 두 source ID만 새 대화에서 질의 | 3/16 약 `$28.5m`, 3/25 Fournier·3팀 거래, 3/16~24 목록 내 Boston 거래 없음 반환. 정확 선수 급여·3/25 순서 부재도 명시. 같은 두 NBA 자료의 연결 분석이며 독립 출처 추가 아님. |
| Codex CBA·산술 | NBA 기사/거래표/거래일 해설, CBA Article VII §4(a)·§6(j)(1), 기존 2차 급여표 | `$2,250,000+$2,161,920=$4,411,920`; `$28,000,000−$4,411,920−$17,450,000=$6,138,080`. 3/25 다른 Boston 수취 선수 두 명을 먼저 같은 예외에 넣는 스트레스. 수취 시 Team Salary는 별개로 남김. |
| Claude 제한 반증 | AI 문서 전문만 제공, 외부 도구 없음 | 산술 오류 없음. 공개 거래 목록의 누락 가능성·정확 charge/픽 미확정을 확인. `F2 PASS`로 확대하지 말라는 지적 수용. 원자료 독립 감사가 아님. |
| Source-blind 편집 검수 | 이전 분석/추천 없이 결과 요약·고정 제약만 Claude 새 대화에 제공 | 기사 약액과 `$28m` 시험값의 구분, 선수 급여의 2차 출처, 동일 예외의 비동시 사용 근거를 요구해 CBA §6(j)(1) 설명을 AI에 보강. Wagner `$2,161,920`을 일할 추정으로 본 의심은 기존 연간 계약표와 다르고, Basketball-Reference를 공식 NBA 데이터베이스로 부른 부분도 잘못됐다. Orlando 자체 TPE가 Boston Hayward 잔액을 바꿀 수 있다는 의심은 다른 팀의 예외를 혼동해 기각. |

독립성: 두 CLI·Codex가 같은 NBA 두 자료를 읽었으며 Claude 두 실행은 같은 모델의 문서 논리/편집 의심이다. G16 독립 전체 설계 감사가 아니다. 용량 시험은 F2 한 소항목의 조건부 경계이며 **법적 하한·정확 Team Salary·픽 권리·Orlando 상대 거래·F2 전체 통과를 증명하지 않는다**. F1~F5 `0/5`, A1~A3 `0/3`, K `0/4`, freeze v0.30 PARTIAL·설계/원고 CLOSED 유지.
