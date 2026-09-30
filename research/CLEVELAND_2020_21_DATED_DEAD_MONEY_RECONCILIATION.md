# Cleveland 2020–21 — 4/16 방출비 보고액 대조

- 기준 `main` `59889a3`, 확인 2026-10-01. `ARITHMETIC_RECONCILIATION_HYPOTHESIS / COMPLETE_LEGAL_BOUND_HOLD`.
- [입력](CLEVELAND_2020_21_C2_PAYROLL_SOURCES.json)의 `dated_dead_money_comparison`과 [기존 재현 도구](../tools/build_cleveland_2020_21_c2_payroll.py)를 사용한다. [산출 JSON](../simulation/CLEVELAND_2020_21_C2_PAYROLL_SCREEN.json)의 날짜 대조와 네 번째 감도안을 별도 판정한다.

## 사실과 귀속 가설

[Hoops Rumors 2021-04-16 기사](https://www.hoopsrumors.com/2021/04/pistons-grizzlies-thunder-carrying-most-202021-dead-money.html)는 **그날 원역사 Cleveland dead money $30,396,254**를 보고하며 Basketball Insiders 자료를 사용했다고 밝힌다. Cleveland 선수별 금액은 없다. 당시 기사라는 출처의 성격은 확인했지만 공식 리그 장부는 아니다.

[SalarySport 2020 보관 표](https://salarysport.com/basketball/nba/cleveland-cavaliers/2020/)의 `Additional contracts`에서 아래 7개 계약행을 대조했다. 오른쪽은 [기존 SalarySwish 입력](CLEVELAND_2020_21_C2_PAYROLL_SOURCES.json)의 cap 보고값이다. 금액의 출처와 법적 charge 인증을 분리한다.

두 계약 표는 2026-10-01에 접근한 후대 보관 자료이며 **4/16 저장본이라는 보장은 없다**. 아래 7행은 계약 날짜에 따라 4/16 비교 대상으로 골라낸 미인증 재구성이다. 총액 기사의 날짜와 두 표의 원장 날짜가 같다고 주장하지 않는다.

| 계약/잔액 | SalarySport 보고 cap | 기존 보고 cap | 차이 |
|---|---:|---:|---:|
| Drummond buyout | $27,957,238 | $27,957,238 | $0 |
| J.R. Smith stretch | $1,456,667 | $1,456,667 | $0 |
| Tucker 방출 | $340,000 | $340,000 | $0 |
| Maker 방출 | $309,355 | $288,594 | $20,761 |
| Cook 첫10일 | $110,998 | $110,998 | $0 |
| Cook 둘째10일 | $110,998 | $110,998 | $0 |
| Ferrell hardship | $110,998 | $0 | $110,998 |
| **7행 합계** | **$30,396,254** | **$30,264,495** | **$131,759** |

**추론:** Maker·Ferrell 두 행을 다른 보고 표의 값으로 바꾸면 기사 총액을 정확히 재현한다. 두 보고 관행의 차이로 총액 차이를 설명할 수 있다. 기사의 실제 선수별 귀속을 알아낸 것은 아니며 공급자 독립성도 미확인이다. Maker $309,355는 기존 표의 현금과 같지만 SalarySport는 cap 필드에 넣었다. Ferrell $110,998은 기존 표의 현금 $118,983과도 다르다. 어느 쪽도 공식 charge로 선택하지 않는다.

Kabengele 첫10일은 4/16 현재 진행 중이라 기사 정의상 만료 계약 대조에서 제외한다. 둘째10일은 4/21, Varejão 두 계약은 5월이므로 이 날짜 총액에 넣지 않는다. 기존 C2 시즌 비용 화면에는 Kabengele 두 의무를 계속 보존하고 승인된 Varejão C2 생략도 보존한다. 4/16 총액을 3/25로 당기거나 5월 최종 비용으로 복사하지 않는다.

## 감도와 S2 판정

기존 세 비용안은 수치와 가정을 그대로 보존한다. 네 번째 안은 이전 두 혜택0 시험 **$132,059,577**에 두 보고행 차이 **$131,759**를 더한 **$132,191,336**이다. tax/apron 기준선과의 산술 차이는 **$435,664 / $6,736,664**다. 두 대조행을 기존 값에 추가 의무로 중복 더하지 않고 차이만 치환한다.

이 안에도 Ferrell 현금 전액이나 모든 캠프 보너스·권리·상계·2020 수정 조정이 증명돼 있지 않다. 네 번째 안을 완전 상한 또는 실제 현금/tax/apron 비용이라고 부르지 않는다. `R_CLE=null`, `complete_domain=false`, 법적 귀속 미인증이며 F5 `HOLD`다. S2의 구간 전체 검증 요건을 총액 일치만으로 충족시키지 않는다. 새로운 계약 실행·건강·시즌 사건의 작가확정도 0건이다.

## 시점 혼합 검문과 다음 증거

SalarySport 보관 페이지의 별도 위젯에는 2027 거래·옵션이 섞여 있다. 해당 위젯의 Stevens `Non-Taxpayer Mid-Level` 표기를 2021 예외 사용 접수 증거로 채택하지 않는다. [Stevens 구단 공지](https://www.nba.com/cavaliers/releases/stevens-contract-210414)는 4/14 다년 서명까지만 확인하며 금액·예외 종류는 제공하지 않는다. [SalarySwish 계약 표](https://www.salaryswish.com/players/lamar-stevens)의 MLE·시즌별 금액은 후속 대조 후보이며 실제 hard-cap trigger는 계속 HOLD다.

다음은 2021 당시 계약 기간/예외 기록과 적용 CBA 조항을 연결하고, 캠프/권리 의무의 완전 구간을 증명하는 일이다. Lakers 건강 선택은 이 비용 대조와 독립적으로 대기한다. 실제 도구 결과는 [V2 검토 기록](../reviews/R02_CLEVELAND_DATED_DEAD_MONEY_REVIEW.md)에 둔다.

7행: 1완료·2번 진행·3번 조건부 선행·4~7 대기, 남은6. S2 법적 F0/5·A0/3·K0/4. freeze v0.30 PARTIAL·설계/원고 CLOSED.
