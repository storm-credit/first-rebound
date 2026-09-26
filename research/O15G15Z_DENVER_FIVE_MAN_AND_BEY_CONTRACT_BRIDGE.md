# O-15G15Z — Denver 1/23 5인 동시 배치와 Bey 계약 다리

- 시작점: `main` `310d846`, [G15X](O15G15X_DENVER_JAN23_FRONTCOURT_RECEIVER.md)의 X1 및 [G15Y](O15G15Y_2022_01_23_THREE_GAME_PLAYER_FLOW.md)의 X2. 원역사 [NBA DET@DEN 박스](https://www.nba.com/game/det-vs-den-0022100707/box-score)의 선수별 분을 기준값으로 삼되 대체 경기의 실제 기록으로 선언하지 않는다.
- 판정: `FIVE_SIMULTANEOUS_PLAYERS_MATH_PASS / CONTRACT_AND_BASKETBALL_HOLD`. 두 분기는 상호 배타적인 수학적 존재 증명이다. 새 작가확정 0건.
- `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`.

## 1. X1/X2의 같은 5인 증명

[교대 증명 JSON](../simulation/O15G15Z_DENVER_FIVE_MAN_WITNESS.json)은 경기 48분을 추상적인 연속 시계로 나타낸다. `X1`의 `{receiver}`는 JaMychal Green, `X2`는 Saddiq Bey다. 다른 수신자는 이 증명에서 **0분**이다. [검증기](../tools/check_o15g15z_denver_lineup.py)는 각 자리의 48:00 연속 피복, 모든 시각 구간의 서로 다른 선수 5명, 선수별 분 및 팀 240:00을 재계산한다.

| 자리 | 순서대로 배정한 구간 | 합 |
|---|---|---:|
| PG | Morris `0–29:51`, Campazzo `29:51–48:00` | `48:00` |
| SG | Campazzo `0–2:27`, Forbes `2:27–23:11`, Rivers `23:11–48:00` | `48:00` |
| SF | Rivers `0–8:56`, Barton `8:56–35:52`, Reed `35:52–48:00` | `48:00` |
| PF | Gordon `0–31:15`, `{receiver}` `31:15–48:00` | `48:00` |
| C | Jokić `0–36:06`, Cousins `36:06–48:00` | `48:00` |

Campazzo는 SG를 마친 뒤 PG를 맡고 Rivers는 SF를 마친 뒤 SG를 맡는다. 누구도 같은 시각 두 자리에 들어가지 않는다. 이 증명은 G15X의 **Cousins `+0:05` / Reed `−0:05`**를 명시적으로 반영한다. 수신자 `16:45`는 원역사 Nnaji의 그날 출전시간과 같지만, 그 선수의 12점·5 FGA나 실제 Nnaji 교체 시각을 수신자에게 이식하지 않는다.

이 시각표는 **현실적인 4쿼터 로테이션이 아니다.** 예컨대 Jokić을 첫 36:06 연속, Gordon을 첫 31:15 연속 뛰게 하며, Campazzo의 SG·Rivers의 SF·Bey의 PF 적합성도 입증하지 않는다. 쿼터별 휴식, 실제 동시 출전 조합, 파울·체력·의료, 공격 점유·FGA·점수·승패가 모두 `HOLD`다. 따라서 G15Y의 `5인 동시 가능성 미증명`만 **추상 분 배정 수준**에서 닫혔다. 실제 경기 설계의 5인 교대는 계속 `HOLD`다.

## 2. Bey의 2021–22 계약 연결은 조건부

[2020–21 Denver 급여 작업안](../simulation/BOSTON_DENVER_2020_21_PAYROLL.md)은 정본인 Bey22에 **2020–21 신인 스케일 계약을 서명했다는 조건**으로 첫해 급여를 넣었다. [2021 드래프트 계속안](../simulation/NBA_2021_FIRST_ROUND_CONTINUATION.md)은 Bey의 Denver 잔류를 입력으로 쓴다. 둘 다 2022-01-23의 서명·보유·등록 사실을 작가확정하지 않는다.

[NBA CBA 101, 2018–19판 4쪽·17쪽](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf)은 **서명된** 1라운드 신인 스케일 계약을 보장 2시즌과 3·4년차 각각의 팀 옵션으로 설명한다. 그러므로 대체 Denver가 2020 Bey22와 표준 신인 계약을 실제 체결했다면 2021–22는 원칙적으로 그 계약의 **두 번째 보장 시즌**이며, 3년차 옵션 행사를 2022년 1월 출전의 전제처럼 요구하지 않는다. 그러나 지명권·급여 시뮬레이션만으로 서명, 이후 무거래·무방출, 당일 등록 및 건강을 증명할 수 없다. `X2`는 그 모든 사건이 이어지는 **조건부 분기**다. `X1`에서는 Bey가 Denver에 보유된 경우 왜 0분인지 코치/성장 비용을 설명해야 한다.

## 3. 근거 계층과 다음 비용

| 구분 | 판정 |
|---|---|
| 사실 | 원역사 NBA 박스의 분; NBA CBA 101의 서명된 신인 계약 2+1+1 구조; 프로젝트의 2020 Bey DEN22 작가확정 |
| 추론 | 서명·잔류 조건이면 Bey의 2021–22 계약은 3년차 옵션 없이도 이어질 수 있다; X1/X2 각 5인 수학 증명은 성립한다 |
| 후보 | X1 JaMychal PF16:45 또는 X2 Bey PF16:45, Cousins11:54·Reed12:08 공통 |
| 작가확정 | 이번 0건. Bey 서명/거래/등록·X1 JaMychal 건강/코치 선택·X2 PF 적합성·실제 쿼터 교대·공격/승패 `HOLD` |

다음은 Denver의 조건부 **날짜별 계약·15인 자리와 쿼터별 실전 가능한 휴식 로테이션**, 이어 Detroit의 Bey/Cade 이탈과 Patrick/Kira/Suggs 당일 가용성·분·FGA를 확인한다. G14 Detroit `PRIOR_HOLD`와 Orlando `ROLE_HOLD`, Chicago 2020–21 정확 시즌, G16/G17은 그대로다. 7개 매크로 게이트는 1완료·1진행·5대기이며 진행 중 포함 6개가 남는다.

[이번 CLI·제한 반증·결과물 단독 맹점 검수](../reviews/R01_O15G15Z_CLI_AND_LIMITED_BLIND_REVIEW.md)는 Antigravity의 NBA 기사 본문 성공, NotebookLM의 CBA 출처 제한 분석, Claude의 수학 확인과 잘못된 Monte Morris 의심의 기각을 기록한다. 어느 단계도 G16/G17을 대체하지 않는다.
