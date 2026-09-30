# Cleveland C2 — 2020–21 공개 계약 비용 화면

- 기준: `main` `634bb70`, 2026-09-30. [입력·출처](../research/CLEVELAND_2020_21_C2_PAYROLL_SOURCES.json), [산출](CLEVELAND_2020_21_C2_PAYROLL_SCREEN.json), [재현 도구](../tools/build_cleveland_2020_21_c2_payroll.py).
- 판정: `LISTED_COST_REPRODUCTION / COMPLETE_TEAM_SALARY_HOLD`. 기존 작가의 McGee 거래 생략·Varejão C2만 반영한 **조건부 비용 화면**이다. 아래 다른 원역사 계약/방출을 그대로 유지하는 것은 검사 전제이며 새 작가확정이 아니다.
- 범위: 최종 경기일 명단의 시즌 계약 산입 보고값과 확인한 이전 비용. 실제 날짜별 Team Salary, 시즌 현금 총액, 전체 미포함 부담의 법적 상한이 아니다. [8경기 명단 검문](../research/O15F14BD_CLEVELAND_C2_FINAL_ROSTER_WINDOW.md)과 함께 사용한다.

## 1. 15명 계약 보고값

각 금액은 링크된 **SalarySwish 2020–21 계약 표의 2차 보고값**이다. 같은 페이지의 뒤 시즌·현재 경력연수·다른 팀 계약을 사용하지 않았다. cap hit에는 아래 Allen·Windler의 likely 금액이 이미 들어 있어 재가산하지 않는다.

| 선수 | 보고 cap hit | 보고 기본급 | 추가 unlikely 시험 |
|---|---:|---:|---:|
| [Love](https://www.salaryswish.com/players/kevin-love) | $31,258,256 | $31,258,256 | $0 |
| [Prince](https://www.salaryswish.com/players/taurean-prince) | $12,250,000 | $12,250,000 | $1,837,500 |
| [Nance](https://www.salaryswish.com/players/larry-nancejr) | $11,709,091 | $11,709,091 | $0 |
| [Osman](https://www.salaryswish.com/players/cedi-osman) | $8,840,580 | $8,840,580 | $0 |
| [Garland](https://www.salaryswish.com/players/darius-garland) | $6,720,720 | $6,720,720 | $0 |
| [Okoro](https://www.salaryswish.com/players/isaac-okoro) | $6,400,920 | $6,400,920 | $0 |
| [Sexton](https://www.salaryswish.com/players/collin-sexton) | $4,991,880 | $4,991,880 | $0 |
| [Windler](https://www.salaryswish.com/players/dylan-windler) | $2,137,440 | $2,037,440 | $0 |
| [Allen](https://www.salaryswish.com/players/jarrett-allen) | $3,909,902 | $3,745,402 | $0 |
| [Dellavedova](https://www.salaryswish.com/players/matthew-dellavedova) | $1,620,564 | $2,174,318 | $0 |
| [Dotson](https://www.salaryswish.com/players/damyean-dotson) | $2,000,000 | $2,000,000 | $0 |
| [Wade](https://www.salaryswish.com/players/dean-wade) | $1,517,981 | $1,517,981 | $0 |
| [McGee](https://www.salaryswish.com/players/javale-mcgee) | $4,200,000 | $4,200,000 | $0 |
| [Stevens](https://www.salaryswish.com/players/lamar-stevens) | $652,366 | $652,366 | $0 |
| [Kabengele 5/1](https://www.salaryswish.com/players/mfiondu-kabengele) | $158,433 | $158,433 | $0 |

일반 15명 보고 cap 합계 **$98,368,133**다. Allen $164,500·Windler $100,000 likely는 이 합계에 포함돼 있다. Prince의 $1,837,500 unlikely를 전액 추가하는 것은 보수적 비용 시험이며 실제 bonus 달성이나 세금 정산 판정이 아니다.

Stevens는 [구단 4/14 다년 계약](https://www.nba.com/cavaliers/releases/stevens-contract-210414) 뒤 일반계약이다. 2차 표의 앞 투웨이 계약은 cap hit $0이고, 전환 계약은 $652,366이라고 보고한다. 앞 투웨이 **현금 $449,115를 다시 더하지 않는다**. 전환 계약 실제 보수와 2020 수정 적용은 확인하지 못했으므로 $652,366을 공식 접수액이나 일할 최저급 재현 PASS로 올리지 않는다. Thomas·Martin의 투웨이 현금을 일반계약 자리/위 cap 합계에 더하지 않되 특별 조정은 미포함 목록에 남긴다.

## 2. 현재 명단에서 빠져도 남는 비용

| 별도 의무 | 보고 cap hit | 처리 |
|---|---:|---|
| [Drummond 3/26 buyout](https://www.salaryswish.com/players/andre-drummond) | $27,957,238 | Cleveland dead cap. Lakers 새 계약 $794,536을 Cleveland에 다시 더하지 않음 |
| [J.R. Smith stretch](https://www.salaryswish.com/players/jr-smith) | $1,456,667 | 2019 방출의 2020–21 잔액; 일반 명단 자리 없음 |
| [Cook 3/12·22](https://www.salaryswish.com/players/quinn-cook) | $110,998 × 2 | 선수 보수 $118,983 × 2와 다름; 이전 두 계약 비용 보존 |
| [Kabengele 4/10·21](https://www.salaryswish.com/players/mfiondu-kabengele) | $99,020 × 2 | 5/1 새 계약 비용만 세어 앞선 두 계약을 지우지 않음 |
| [Maker 1/14 방출](https://www.salaryswish.com/players/thon-maker) | $288,594 | 보고 현금 $309,355와 다름. 연간 미보장 $1,737,145를 다시 더하지 않음 |
| [Tucker 11/28 방출](https://www.salaryswish.com/players/rayjon-tucker) | $340,000 | UTA 계약 승계 뒤 CLE dead cap. 뒤 PHI 투웨이 보수를 CLE에 더하지 않음 |
| [Ferrell 1/11 hardship](https://www.salaryswish.com/players/yogi-ferrell) | $0 | 현금 $118,983 보고와 분리. 정확 면제/2020 수정 인증 HOLD |

별도 9개 보고 계약/잔액 합계 **$30,462,535**다. 최종 명단에서 빠진 Maker·Tucker의 **+$628,594**를 회수했다. Ferrell의 cap hit 0은 2차 보고를 재현한 값이며 현금 0이나 대체세계 hardship 면제 인증을 뜻하지 않는다. 일반 계약의 자동 최소급 $110,998을 넣는 것도 실제 법적 판정이 아니므로 별도 미확인 항목으로 남긴다. [Kabengele 구단 공지](https://www.nba.com/cavaliers/releases/kabengele-210501)는 5/1 다년 서명 및 앞선 4/10·21 두 10일을 확인한다. 이 공지는 금액이나 5월 전체 거래 부재를 인증하지 않는다. [Cook 첫 구단 공지](https://www.nba.com/cavaliers/releases/cook-10-day-210312)는 3/12 10일 서명을 확인한다. 둘째 비용은 2차 표의 별도 계약행이다.

## 3. cap 보고값과 tax/apron 화면의 차이

[2017 CBA VII §12(f)(2), §6(m)(3)(B)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)는 0·1년 경력 FA 계약의 tax/apron 산입 하한을 2년 경력 최저급에 연결한다. Kabengele는 Sacramento에서 기존 rookie 계약이 방출된 뒤 Cleveland와 **새 FA 계약**을 맺은 경로이므로 보유 draft rookie 계약과 구분한다. 기존 [146일 최소급 원장](NBA_2020_21_REGISTRATION_COSTS.md)의 $1,620,564를 10·10·16일에 적용한 **조건부** 차지는 $110,998·$110,998·$177,596, 보고값 대비 총 **+$43,119**다. 원계약·보너스·2020 수정 규정까지 인증한 실제 tax/apron 금액은 아니다. Sacramento 이전 rookie 방출비를 Cleveland에 가져오지 않는다.

아래 네 안은 첫 목록에 각 줄의 증분을 **순서대로 누적**한 시험이다. `season_selected=false`는 작품 대체 시즌을 작가확정하지 않았다는 뜻이며 자료의 2020–21 시즌 필터와 별개다. 실제 비용과 누락 구간 미인증 때문에 actual tax/apron은 미판정(null)이다.

| 같은 공개 입력의 비용안 | 목록 비용 | tax $132,627,000까지 숫자 차이 | apron $138,928,000까지 숫자 차이 |
|---|---:|---:|---:|
| 보고 cap 목록+Prince bonus 전액 | $130,668,168 | $1,958,832 | $8,259,832 |
| 위+Kabengele 조건부 FA 하한 | $130,711,287 | $1,915,713 | $8,216,713 |
| 위+Drummond 감액 혜택 0+Dellavedova 보전 혜택 0 시험 | **$132,059,577** | **$567,423** | **$6,868,423** |
| 위+Maker/Ferrell 다른 보고행 차이 치환(10/1 추가, 완전 상한 아님) | **$132,191,336** | **$435,664** | **$6,736,664** |

세 번째 줄은 Drummond 원래 연간 $28,751,774를 전액 남겨 **+$794,536**, Dellavedova의 보고 현금 $2,174,318을 넣어 **+$553,754**한 시험이다. buyout가 취소됐다는 사건 선택도, 현금이 실제 tax 차지라는 주장도 아니다. [공식 NBA 2020–21 cap/tax 발표](https://pr.nba.com/nba-nbpa-2020-21-season/)와 [apron 이력](https://www.salaryswish.com/salary-cap)을 기준선으로 쓴다. 양수 차이는 공개 목록에서만 성립하며 실제 비납세/하드캡 PASS가 아니다.

동일한 다른 계약 가정에서 원역사 Hartenstein 보고액 $1,620,564와 Varejão 조건부 $144,297 대신 McGee $4,200,000을 유지하면 C2 목록은 **+$2,435,139**다. 이 연간 비용 차이에 시즌 잔여 일수 비율을 다시 곱하지 않는다. 3/25 거래 생략은 신규 McGee 영입이 아니며 선수의 현금 지급 팀 배분과 리그 Team Salary는 다른 장부다.

## 4. 남은 조건과 V2

캠프·기타 방출잔액/상계·과거 권리/예외·정확 bonus 및 2020 수정·실제 hard-cap 발생·Stevens 전환액·다른 대체 거래를 전수 확인하지 못했다. [12/19 구단 계열 공지](https://cleveland.gleague.nba.com/news/cavs-convert-bolden-to-two-way-contract)는 Mooney·Randolph·Matthews 방출, Bolden 투웨이 전환, Pelle 서명을 확인하지만 이들의 미보장·Exhibit 10 보너스·권리 소멸/상계 비용을 전부 인증하지 못한다. Maker의 현금/cap 차이 $20,761과 Ferrell 현금 $118,983도 위 두 혜택0 시험에는 들어 있지 않다. 따라서 세 번째 줄은 전체 비용 상한이 아니다. 2026-10-01 추가한 네 번째 줄은 [4/16 보고액 대조](../research/CLEVELAND_2020_21_DATED_DEAD_MONEY_RECONCILIATION.md)의 Maker +$20,761/Ferrell +$110,998만 치환한 감도다. Ferrell 현금 $118,983이나 모든 잔여 의무의 완전 구간을 증명하지 않아 이 줄 역시 전체 비용 상한이 아니다. 그 때문에 `R_CLE=null`, 정확 Team Salary와 tax/apron PASS는 `null`이며 위 숫자 차이는 **미포함 부담을 담을 수 있는 조건부 폭**이다. 미확인 항목을 더했을 때 비용이 얼마나 달라지는지 다음 검증에 사용할 수 있게 처음으로 15명+이전 9의무를 연결했다.

Codex는 2차 계약 본문/행과 기존 결정·급여 규칙을 대조하고 산술을 재현했다. Antigravity 공식 Kabengele 본문 요청은 45초 뒤 빈 응답으로 **증거 0건**이었다. NotebookLM의 같은 공식 URL 추가도 실패했다. 후속 분석과 반증의 실제 결과는 별도 [V2 기록](../reviews/R01_CLEVELAND_C2_PAYROLL_SCREEN.md)을 따른다. 도구 상태를 독립 원자료 수로 세지 않는다.

F5·A1/A3·네 K와 정확 시즌은 `HOLD`, F 전체 PASS `0/5`·A 최종 `0/3`·K 종료 `0/4`. 7행 1완료·1진행·5대기, 남은6. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, 원고0.
