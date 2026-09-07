# Chicago 2020-21 Pre-Deadline Player-Game Donor & Starter Vector v0.1

- 상태: `PLAYER_GAME_CONSERVATION_PASS / PREDEADLINE_ROLE_PROVISIONAL_LOCK / PRODUCTION_AND_OUTCOME_HOLD`
- 적용 구간: 2020-12-23~2021-03-24, 실제 Chicago 43경기
- 선행 기준선: `CHICAGO_2020_21_OPENING_ROSTER_BASELINE`
- 원고 게이트: `CLOSED`

## 결론

마감일 전 같은 날짜 분·선발 보존을 통과한 BASE는 다음과 같다.

| 선수 | 경기 | 선발 | 총분 | 평균 |
|---|---:|---:|---:|---:|
| 주인공 | 43 | 43 | 1,219:00 | 28:20 |
| LaMelo Ball | 43 | 25 | 1,191:00 | 27:42 |
| 합계 | 86 player-games | 68 | 2,410:00 | — |

요약하면 주인공은 **43경기·43선발·1,219분**, LaMelo는 **43경기·25선발·1,191분**이다.

주인공은 3년차 선발 SF/PF로 전 경기 선발한다. LaMelo는 18경기 동안 첫 가드 교체·두 번째 유닛 창출자로 적응한 뒤 **2021-02-01 New York전부터 선발**한다. 전환일은 경기 결과나 후대 성과가 아니라 opening architecture의 `게임 10~20 평가창`을 18경기로 닫은 시간순 규칙이다.

이는 마감일 전 역할의 `PROVISIONAL_LOCK`이다. 개인 박스·효율·승패·LaMelo의 후속 부상·시즌 전체 GP/GS/분은 잠그지 않는다.

## 1. 실제 기준선

`CHICAGO_2020_21_PREDEADLINE_MINUTE_LEDGER.csv`가 43경기 팀 총초와 두 가상 선수의 분·선발을, `CHICAGO_2020_21_PREDEADLINE_DONOR_VECTOR.csv`가 실제 선수의 날짜별 actual→alternate 변화를 기록한다. `CHICAGO_2020_21_PREDEADLINE_PLAYER_BUDGET.csv`는 선수별 합계 원장이다.

| 항목 | 실제 값 | 보존 판정 |
|---|---:|---|
| 경기 | 43 | PASS |
| 성적 | 19승 24패 | 식별 기준선만 사용, 배정 규칙에는 미사용 |
| 팀 총분 | 10,420:02 | alternate와 일치 |
| 선발 자리 | 215 | 43×5 그대로 유지 |
| 연장 | 4회분 100분 | 날짜별 팀 총초에 포함 |

원자료는 NBA Stats의 team/player box-score 계열이며, NBA V3 필드를 보존한 공개 데이터 미러와 실제 시즌 합계로 교차했다. 미러를 별도 독립 출처로 세지 않는다.

## 2. 선발 자리 이전

| 새 선발 | 실제 source | 경기 수 | 규칙 |
|---|---|---:|---|
| 주인공 | Patrick Williams | 42 | Patrick의 실제 마감일 전 선발 전부 |
| 주인공 | Garrett Temple | 1 | Patrick이 결장한 2021-01-18 한 경기 |
| LaMelo | Coby White | 18 | 2021-02-01~2021-03-12 |
| LaMelo | Tomas Satoransky | 7 | 실제 Coby 벤치 전환 뒤 2021-03-14~24 |

주인공 43선발과 LaMelo 25선발을 더한 68자리는 실제 선발 68자리를 정확히 반환한다. LaVine·Markkanen·Carter·Young의 남은 선발 자리는 바꾸지 않는다.

## 3. 직접 대체분과 secondary donor

| 직접 제거 | 실제 GP/GS | 실제 분 |
|---|---:|---:|
| Patrick Williams | 42/42 | 1,192:50 |
| Chandler Hutchison | 7/0 | 63:35 |
| 합계 | — | **1,256:25** |

두 가상 선수의 2,410분에서 직접 대체분을 빼면 **1,153분 35초**가 필요하다. 같은 날짜로 이전한 순감은 다음과 같다.

| donor | actual 분 | alternate 분 | 순차감 | 보존 기능 |
|---|---:|---:|---:|---|
| Tomas Satoransky | 721:23 | 391:23 | 330:00 | 32경기 유지, 벤치 조직 역할 |
| Denzel Valentine | 719:28 | 359:28 | 360:00 | 39경기 유지, 보조 슈팅·창출 표본 |
| Ryan Arcidiacono | 296:06 | 156:44 | 139:22 | 18경기·비상 ball security 유지 |
| Coby White | 1,362:04 | 1,142:04 | 220:00 | 43경기·18선발·26:34 평균 유지 |
| Garrett Temple | 977:27 | 896:49 | 80:38 | 35경기·11선발·수비 바닥 유지 |
| Otto Porter Jr. | 540:19 | 516:44 | 23:35 | 실제 출전 25경기에서만 제한 차감 |
| 합계 | — | — | **1,153:35** | — |

LaVine·Markkanen과 센터진의 경기별 분은 전부 실제와 같다. Young은 시즌 순감 0이며, 2021-03-12의 38초 차감을 실제 출전일인 2020-12-31에 그대로 반환하는 gross bridge만 사용한다.

## 4. 당일 역할 바닥

실제 출전한 날짜에만 차감하며, 차감하는 경기의 alternate 하한은 다음과 같다.

| 선수 | 당일 하한 |
|---|---:|
| Satoransky | 10분 |
| Valentine | 6분 |
| Arcidiacono | 0분 |
| Coby | 20분 |
| Temple | 16분 |
| Porter | 12분 |

이는 목표 평균이 아니라 비정상적인 음수·역할 삭제를 막는 game-level floor다. Coby와 Temple은 시즌 평균이 각각 26:34·25:37로 남는다. 포지션이 다른 Carter·Gafford·Kornet·Felicio의 센터 분은 건드리지 않는다.

## 5. 부상·성과 방화벽

- LaMelo는 Chicago 고유 부상 원인이 아직 없으므로 계산 BASE에서 43경기 모두 active로 둔다. Charlotte의 손목 사건을 삭제했다는 뜻은 아니며 이후 구간은 `INJURY_EVENT_HOLD`다.
- 19승 24패는 실제 기준선이다. 이번 분 배정에 실제 승패·점수차를 사용하지 않았으므로 alternate 성적으로 쓰지 않는다.
- LaMelo의 실제 신인왕, Patrick의 실제 기록, 주인공의 미래 스타 지위를 박스 생산성에 선지급하지 않는다.
- Vučević 거래와 Washington–Chicago–Boston 3팀 거래는 2021-03-24 대체 성적·수요가 나온 뒤 별도로 판정한다.

## 6. 다음 계산

O-15F2에서 주인공·LaMelo의 공격·수비 생산성 prior와 여섯 donor의 생산성 이전량을 계산한다. 그 뒤 43경기 점수차 outcome을 실행해 마감일 직전 성적을 얻는다. 거래 발생 여부는 이 결과 전까지 `HOLD`다.

## 출처

- [NBA Stats — Chicago 2020-21 선수 box scores](https://www.nba.com/stats/players/boxscores?DateFrom=12%2F23%2F2020&DateTo=03%2F24%2F2021&Season=2020-21&SeasonType=Regular%20Season&TeamID=1610612741)
- [NBA Stats — Chicago 2020-21 team box scores](https://www.nba.com/stats/team/1610612741/boxscores?DateFrom=12%2F23%2F2020&DateTo=03%2F24%2F2021&Season=2020-21&SeasonType=Regular%20Season)
- [Chicago Bulls — 2021-03-14 실제 선발 변경](https://www.nba.com/bulls/gameday/bulls-cruise-past-raptors-donovan-tries-new-starting-lineup)
- [NocturneBear/NBA-Data-2010-2024 — NBA V3 box-score 공개 미러](https://github.com/NocturneBear/NBA-Data-2010-2024)
