# O-15F14-AG — Chicago 2020 FA 보류액 후보 후속

- 기준: `main` `55845be`, 조회일 2026-09-28, 적용일 2021-03-25.
- 분류: 원역사 계약 **FACT**, 승인 경로 적용 **CONDITIONAL**, 전체 R **HOLD**.
- 범위: 2020 오프시즌에 이름이 확인된 Denzel Valentine, Adam Mokoka, Max Strus 세 명. 이전 [Dunn·Harrison·Vonleh 판정](../simulation/CHICAGO_2020_21_RESIDUAL_COMPONENTS.md)을 재계산하지 않는다.

## 계약 사건과 중복 방지

| 후보 | 원역사 1차 자료 | 선택 경로에 적용할 때 |
|---|---|---|
| Valentine | [Chicago 공식 미디어 가이드 2022, 인쇄 399쪽](https://chibullsdigital.com/mediaGuide/2022_ChicagoBulls_MG_NBA_HI.pdf): 2020-11-21 qualifying offer 수락 | 이 재계약이 유지되면 종전 FA 보류액은 별도 행이 아니다. 2020–21 선수 급여는 [기존 Chicago 급여 출처](CHICAGO_2020_21_TAX_BOUND_SOURCES.json)에 이미 들어 있으므로 다시 더하거나 빼지 않는다. |
| Mokoka | 같은 구단 가이드 인쇄 399쪽: 2020-11-22 Chicago 투웨이 계약. [Chicago 2020–21 개막 명단](CHICAGO_2020_21_OPENING_ROSTER_BASELINE.md)도 투웨이 2명 중 한 명으로 기록 | 이 계약이 유지되면 2019–20 계약에서 넘어온 종전 FA 보류액을 별도 미서명 자유계약선수 행으로 세지 않는다. 투웨이 급여의 cap 처리와 일반계약 15명 급여를 혼동하지 않는다. |
| Strus | [NBA의 Miami 로스터 취득 연혁](https://www.nba.com/news/how-the-2023-nba-finals-rosters-were-built-miami-heat)은 2020-11-30 Miami 자유계약 영입을 명시한다. [Miami 구단 공지](https://www.nba.com/heat/news/max-strus-two-way-contract)는 2020-12-19 투웨이 전환을 명시 | Miami 영입 경로가 유지되면 Chicago의 종전 FA 보류액은 2021-03-25에 남지 않는다. Strus의 2019–20 Chicago 부상·출전 이력은 이 계약 사건의 대체세계 불변성을 증명하지 않는다. |

2017 [NBA–NBPA CBA](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf) Article VII §4(d)의 이전 팀 FA 금액 종료 규칙과 계약 날짜를 결합한 **조건부** 판정이다. 원역사의 계약 기록은 공식 자료로 확인되지만, 주인공이 있는 세계에서 같은 계약이 실제 발생하는지는 별도 인과 전제다. 이 세 명의 과거 보류액은 기존 알려진 선수 급여 상한에 더해진 적이 없으므로 이번 확인으로 `$5,609,972`의 R 한도가 증가하지 않는다.

## 여전히 열린 정확 조건

구단 가이드의 연혁과 NBA의 2020 오프시즌 [선수 이동표](https://www.nba.com/news/nba-player-movement-2020-offseason)는 당시 이름 있는 사건을 확인하는 자료다. 이동표의 Chicago 행에는 이탈 Dunn·Harrison·Strus와 `Free Agents: —`가 적혀 있다. 이는 **그 표의 2020 오프시즌 분류**이지 과거부터 남은 모든 FA 권리, 실제 renouncement, 미서명 1라운드 권리, 방출·stretch 부담, 분쟁·예외·코로나 수정 CBA를 완전 열거한 2021-03-25 cap sheet가 아니다. 따라서 `OTHER_FA_RIGHTS`, `UNSIGNED_FIRSTS`, `WAIVED_PAY`, `EXCEPTION_HISTORY`, `OTHER_ADJUSTMENTS`의 전체 금액과 R은 여전히 `null`이다. 거래 수취/송출액과 비납세·matching도 `HOLD`이며 D1 F1~F5 `0/5`, A1~A3 `0/3`, 네 K `0/4`다.

검토 상태: Codex 원자료 대조 자체 검토 `NOT_INDEPENDENT`. 이 증인에는 Anti-Gravity·NotebookLM·Claude·source-blind 재검사를 실행하지 않았다. 기존 V2 시범 실행 기록을 이 증인의 독립 검증으로 옮겨 세지 않는다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED` 유지.
