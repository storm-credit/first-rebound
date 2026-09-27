# O-15F14-AR — Chicago 2020–21 방출잔액의 날짜 경계

- 판정: `ORIGINAL_APR16_TEAM_TOTAL_REPORTED / ALTERNATE_MAR25_CHARGE_HOLD`.
- 범위: F1 `WAIVED_PAY` 한 항목. [기존 R 상한](../simulation/CHICAGO_2020_21_TAX_BOUND.md)과 [부분 원장](../simulation/CHICAGO_2020_21_RESIDUAL_COMPONENTS.md)을 이어 쓰며 전체 R이나 거래 matching을 인증하지 않는다.

| 분류 | 확인·적용 |
|---|---|
| 사실 — 동시대 2차 보도 | [Hoops Rumors 2021-04-16 집계](https://www.hoopsrumors.com/2021/04/pistons-grizzlies-thunder-carrying-most-202021-dead-money.html)는 그날 기준 **원역사 Chicago의 2020–21 dead money 총액 $97,261**을 보고한다. 기사 자체는 선수별 내역이 없고 Basketball Insiders 데이터를 사용했다고 밝힌다. NBA 리그 cap sheet가 아니다. |
| 2차 대조 | [Salary Sport의 2020 시즌 보관 급여표](https://salarysport.com/basketball/nba/chicago-bulls/2020/)는 `Additional contracts`의 Vonleh에 **$97,261**을 표시한다. 그러나 페이지의 후대 실시간 위젯에는 그 시즌과 무관한 항목도 섞여 있으므로 Vonleh 귀속은 **후보 대조**로만 둔다. [SalarySwish의 Vonleh 계약표](https://www.salaryswish.com/players/noah-vonleh)는 Chicago 계약의 원래 보장액 `$0`과 12/14 방출을 적는다. `$0` 계약 보장 표기와 나중에 보고된 실제 잔액을 같은 필드로 단순 대체하지 않는다. |
| 추론 — 조건부 산술 | 이 $97,261이 선택된 3/25 세계에서도 **동일한 WAIVED_PAY**였다면, 기존 명단 밖 R 상한 `$5,609,972` 중 다른 항목에 허용되는 금액은 `$5,512,711`이다. 이는 `5,609,972−97,261`의 감도 계산이며 실제 R 값이 아니다. |
| 후보 / 작가 확정 | 12월 Chicago Vonleh 방출 경로를 유지하는 후보에서도 방출일 이후 원장 차액·다른 선수 잔액을 확인해야 한다. 새 작가 선택은 없고 기존 승인 방향만 유지한다. |

4/16은 거래일 **3/25 뒤**다. 원역사 팀 총액을 앞당겨 리그의 3/25 정확 charge로 쓰거나, 원역사 3/25 이후 다른 선수 이동이 대체 세계에서도 같았다고 확정할 수 없다. Hoops Rumors 총액과 Salary Sport의 이름을 결합해 **원역사 Vonleh $97,261 정확 계약 원문**을 만들지도 않는다. `WAIVED_PAY`, `OTHER_FA_RIGHTS`, `UNSIGNED_FIRSTS`, `EXCEPTION_HISTORY`, `OTHER_ADJUSTMENTS`를 모두 포함한 R은 계속 `null`; F1 `HOLD`다.

Codex가 동시대 기사 본문·두 2차 표와 기존 [CBA 분류](../simulation/CHICAGO_2020_21_RESIDUAL_COMPONENTS.md)를 직접 대조했다. Antigravity CLI는 기사 본문 대신 탐색 영역까지만 회수해 금액 증거 0건이었다. NotebookLM CLI는 **해당 기사 URL 본문을 소스로 저장**해 4/16 `$97,261`과 선수명 부재·3/25 대체 원장 미증명을 다시 확인했다. 두 도구의 동일 기사 접근을 독립 원자료 두 건으로 세지 않는다. Claude/source-blind 결과는 별도 검토 기록에 둔다. F `0/5`, A `0/3`, K `0/4`, 7행 1완료·1진행·5대기·미완료 6개; `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, 원고 금지.
